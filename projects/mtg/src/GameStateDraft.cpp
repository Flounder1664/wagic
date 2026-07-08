#include "PrecompiledHeader.h"

#include "GameStateDraft.h"
#include "GameApp.h"
#include "MTGDraft.h"
#include "MTGPack.h"
#include "MTGDeck.h"
#include "MTGCard.h"
#include "MTGCardInstance.h"
#include "CardGui.h"
#include "DebugRoutines.h"
#include "WFont.h"
#include "WResourceManager.h"
#include "SimpleMenu.h"
#include "GameOptions.h"
#include "Rules.h"
#include <JFileSystem.h>
#include <JRenderer.h>
#include <algorithm>

namespace
{
// Fixed, deliberately high-numbered AI deck slots reserved for draft-mode
// bot decks. AIPlayerFactory::createAIPlayer() hardcodes "ai/baka/deck%i.txt"
// (AIPlayer.cpp:231) -- it doesn't go through DeckManager at all, so these
// files can't live anywhere else and still be loadable. Numbers this high
// are extremely unlikely to collide with any shipped or player-added AI
// deck (which start at 1 and count up), but they DO become visible to
// normal Quest/casual opponent selection (DeckManager has no unlock/
// visibility filter) for as long as the files exist -- cleaned up at the
// start of each new draft to bound that window, not perfectly, but without
// needing a hook into GameStateDuel's own end-of-tournament flow.
const int kDraftBotDeckIdBase = 9001;
const char* kDraftProfileName = "WagicDraftTemp";
}

namespace
{
const int kPoolCols = 7;
const int kPoolMaxRows = 4;
const int kDraftQuitMenuId = 500;
const int kDraftQuitMenuResume = 1;
const int kDraftQuitMenuConfirm = 2;
const int kDraftSetMenuId = 501;
const int kDraftModeMenuId = 502;
const int kDraftSetMenuCancel = -1; // matches kCancelMenuID; set ids are >= 0 so no collision
// Mode-menu item ids. Negative so they never collide with a set id (>= 0),
// which the set-list menu uses directly as item ids.
const int kModeCancel = -1;
const int kModeRandom = -2;
const int kModeOld = -3;
const int kModeNew = -4;
const int kModePickOne = -5;
const int kModePickThree = -6;
// Era boundaries for the "old cards" / "new cards" quick options (inclusive).
const int kOldEraMaxYear = 2003; // through the 8th Edition era
const int kNewEraMinYear = 2018;
// A set needs at least this many cards per rarity to draft the 1 rare /
// 3 uncommon / 10 common pack with reasonable variety. Marginal sets don't
// crash (MTGPackSlot::add just yields a smaller pack), but a healthy margin
// keeps picks interesting.
const int kMinCommons = 15;
const int kMinUncommons = 6;
const int kMinRares = 3;
const float kPoolColStep = 30.0f;
const float kPoolRowStep = 45.0f;

// CardDisplay::Render() unconditionally draws an enlarged preview of the
// focused card at a fixed screen position (CardGui::BigWidth/2, roughly the
// left third of the screen) -- fine for the interactive pack, but a read-only
// "picked so far" strip shouldn't fight it for the same space. This overrides
// just the thumbnail-row part of CardDisplay::Render (Render(bool) isn't
// virtual, so this only needs to be called through a DraftPoolDisplay*, which
// GameStateDraft does), and lays cards out in a grid (kPoolCols per row)
// instead of AddCard()'s single-row formula, with an "xN" count badge per
// unique card instead of one thumbnail per duplicate copy.
class DraftPoolDisplay: public CardDisplay
{
public:
    DraftPoolDisplay(int id, int px, int py) :
        // nb_displayed_items must be the per-row count (kPoolCols), not the
        // grid's total capacity (kPoolCols*kPoolMaxRows) -- CardDisplay's
        // constructor clamps x assuming nb_displayed_items cards side by side
        // in one row (CardDisplay.cpp: "if (x + nb_displayed_items*30+25 >
        // SCREEN_WIDTH) x = ..."). Passing 28 there clamped x to -385,
        // silently rendering the whole grid off-screen to the left.
        CardDisplay(id, NULL, px, py, NULL, NULL, kPoolCols)
    {
    }

    void AddCardAt(MTGCardInstance* card, int slot, int count)
    {
        int col = slot % kPoolCols;
        int row = slot / kPoolCols;
        CardGui* view = NEW CardView(CardView::nullZone, card, static_cast<float> (x + 20 + col * kPoolColStep),
                static_cast<float> (y + 25 + row * kPoolRowStep));
        Add(view);
        mCounts.push_back(count);
    }

    // CardDisplay::CheckUserInput's LEFT/RIGHT case calls rotateLeft()/
    // rotateRight() once the cursor crosses start_item+nb_displayed_items --
    // those shift every object's x by +-30 assuming a single scrolling row
    // (CardDisplay.cpp:56-76). This grid shows everything at once (no
    // scrolling window), so reusing that navigation would silently drift
    // every card's x left/right by 30 each time the cursor crosses a row
    // boundary. Plain bounded index movement instead, with the same
    // Entering()/Leaving() focus-transition calls the base class makes (for
    // the focused-card zoom animation).
    bool CheckUserInput(JButton key)
    {
        if (mObjects.empty())
            return false;

        int n = mCurr;
        if (key == JGE_BTN_LEFT)
            n = (std::max)(0, mCurr - 1);
        else if (key == JGE_BTN_RIGHT)
            n = (std::min)((int) mObjects.size() - 1, mCurr + 1);
        else if (key == JGE_BTN_UP)
            n = (std::max)(0, mCurr - kPoolCols);
        else if (key == JGE_BTN_DOWN)
            n = (std::min)((int) mObjects.size() - 1, mCurr + kPoolCols);
        else
        {
            // Mouse/touch click -- mirrors CardDisplay::CheckUserInput's
            // default case (nearest object to the click point), minus the
            // rotateLeft()/rotateRight() calls, which don't apply here.
            int x1, y1;
            JGE* jge = observer ? observer->getInput() : JGE::GetInstance();
            if (!jge || !jge->GetLeftClickCoordinates(x1, y1))
                return false;

            unsigned int minDistance2 = (unsigned int) -1;
            for (size_t i = 0; i < mObjects.size(); i++)
            {
                float top, left;
                if (mObjects[i]->getTopLeft(top, left))
                {
                    unsigned int distance2 = static_cast<unsigned int> ((top - y1) * (top - y1) + (left - x1) * (left - x1));
                    if (distance2 < minDistance2)
                    {
                        minDistance2 = distance2;
                        n = (int) i;
                    }
                }
            }
            jge->LeftClickedProcessed();
        }

        if (n != mCurr && mObjects[mCurr] != NULL && mObjects[mCurr]->Leaving(key))
        {
            mCurr = n;
            mObjects[mCurr]->Entering();
        }
        return true;
    }

    void Render(bool /*norect*/ = false)
    {
        JRenderer* r = JRenderer::GetInstance();
        int rows = mObjects.empty() ? 1 : (std::min)(kPoolMaxRows, ((int) mObjects.size() + kPoolCols - 1) / kPoolCols);
        r->DrawRect(static_cast<float> (x), static_cast<float> (y), static_cast<float> (kPoolCols * kPoolColStep + 20),
                kPoolRowStep * rows + 5, ARGB(255,255,255,255));

        WFont* font = WResourceManager::Instance()->GetWFont(Fonts::MAIN_FONT);
        for (size_t i = 0; i < mObjects.size(); i++)
        {
            if (!mObjects[i])
                continue;
            mObjects[i]->Render();
            if (font && i < mCounts.size() && mCounts[i] > 1)
            {
                // Horizontal centering used manual (bw-textW)/2 math before;
                // switched to the font's own JGETEXT_CENTER alignment mode
                // (WFont.h:31-33) instead of re-deriving the same offset by
                // hand, since that's the tested, already-used-elsewhere path
                // rather than one more manual computation to get subtly
                // wrong. Vertical still centered from GetHeight() -- there's
                // no vertical alignment mode, only horizontal.
                CardGui* cardg = (CardGui*) mObjects[i];
                char buffer[8];
                sprintf(buffer, "x%i", mCounts[i]);
                font->SetScale(0.6f);
                float textH = font->GetHeight();
                float bw = font->GetStringWidth(buffer) + 4.0f;
                float bh = textH + 2.0f;
                float bx = cardg->x - bw / 2.0f;
                float by = cardg->y + 6.0f;
                r->FillRect(bx, by, bw, bh, ARGB(200,0,0,0));
                r->DrawRect(bx, by, bw, bh, ARGB(220,240,240,240));
                font->DrawString(buffer, bx + bw / 2.0f, by + (bh - textH) / 2.0f, JGETEXT_CENTER);
                font->SetScale(1.0f);
            }
        }
    }

    // Only called while GameStateDraft is in "review" mode -- the focused
    // pack's own big preview (CardDisplay::Render()) isn't drawn then, so
    // this doesn't need to fight it for the same screen space.
    void RenderFocusedBig()
    {
        if (mObjects.empty() || mCurr < 0 || mCurr >= (int) mObjects.size())
            return;
        CardGui* cardg = (CardGui*) mObjects[mCurr];
        if (!cardg || !cardg->card)
            return;
        Pos pos((CardGui::BigWidth / 2), CardGui::BigHeight / 2 - 10, 0.80f, 0.0, 220);
        CardGui::DrawCard(cardg->card, pos, DrawMode::kNormal);
    }

private:
    std::vector<int> mCounts; // parallel to mObjects, by add order
};
}

GameStateDraft::GameStateDraft(GameApp* parent) :
    GameState(parent, "draft")
{
    mSession = NULL;
    mPackDisplay = NULL;
    mPoolDisplay = NULL;
    mQuitMenu = NULL;
    mSetMenu = NULL;
    mHumanSeatId = 0;
    mSelectingSet = false;
    mSetSelectStage = SEL_MODE;
    mChosenControlId = 0;
    mChosenMenuId = 0;
    mSetChosen = false;
    mDraftComplete = false;
    mReviewingPool = false;
    mQuitConfirmed = false;
}

void GameStateDraft::clearDraftPacks()
{
    for (size_t i = 0; i < mDraftPacks.size(); i++)
        SAFE_DELETE(mDraftPacks[i]);
    mDraftPacks.clear();
}

GameStateDraft::~GameStateDraft()
{
}

void GameStateDraft::Create()
{
}

void GameStateDraft::Destroy()
{
    clearDisplayInstances();
    clearPoolDisplayInstances();
    SAFE_DELETE(mPackDisplay);
    SAFE_DELETE(mPoolDisplay);
    SAFE_DELETE(mQuitMenu);
    SAFE_DELETE(mSetMenu);
    SAFE_DELETE(mSession); // holds raw ptrs into mDraftPacks -- delete it first
    clearDraftPacks();
}

void GameStateDraft::openQuitMenu()
{
    if (mQuitMenu)
        return;
    mQuitMenu = NEW SimpleMenu(JGE::GetInstance(), WResourceManager::Instance(), kDraftQuitMenuId, this, Fonts::MENU_FONT,
            SCREEN_WIDTH / 2 - 100, 25);
    mQuitMenu->Add(kDraftQuitMenuResume, "Resume Draft");
    mQuitMenu->Add(kDraftQuitMenuConfirm, "Quit to Main Menu");
}

void GameStateDraft::closeQuitMenu()
{
    SAFE_DELETE(mQuitMenu);
}

void GameStateDraft::ButtonPressed(int controllerId, int controlId)
{
    // ButtonPressed() runs from inside the menu's own CheckUserInput() --
    // deleting the menu here (as a previous version did) frees the object out
    // from under its still-running call, a use-after-free. So just record the
    // choice; Update() acts on it once we're off the menu's call stack.
    if (controllerId == kDraftQuitMenuId && mQuitMenu)
    {
        // SimpleMenu::Close() (SimpleMenu.cpp:368-372) only starts a brief
        // close animation; the actual delete happens later in Update() once
        // isClosed() is true.
        mQuitConfirmed = (controlId == kDraftQuitMenuConfirm);
        mQuitMenu->Close();
    }
    else if ((controllerId == kDraftSetMenuId || controllerId == kDraftModeMenuId) && mSetMenu)
    {
        mChosenMenuId = controllerId;
        mChosenControlId = controlId;
        mSetChosen = true;
    }
}

void GameStateDraft::clearDisplayInstances()
{
    for (size_t i = 0; i < mDisplayInstances.size(); i++)
        SAFE_DELETE(mDisplayInstances[i]);
    mDisplayInstances.clear();
}

void GameStateDraft::clearPoolDisplayInstances()
{
    for (size_t i = 0; i < mPoolDisplayInstances.size(); i++)
        SAFE_DELETE(mPoolDisplayInstances[i]);
    mPoolDisplayInstances.clear();
}

void GameStateDraft::refreshPackDisplay()
{
    SAFE_DELETE(mPackDisplay);
    clearDisplayInstances();

    // Bottom-right, matching GameStateShop's BoosterDisplay placement -- clear
    // of the big-card preview CardDisplay::Render() always draws over the
    // left third of the screen.
    mPackDisplay = NEW CardDisplay(1, NULL, SCREEN_WIDTH - 255, SCREEN_HEIGHT - 65, NULL, NULL, 7);

    MTGDeck* pack = mSession->getPackForSeat(mHumanSeatId);
    if (!pack)
        return;

    for (map<int, int>::iterator it = pack->cards.begin(); it != pack->cards.end(); ++it)
    {
        MTGCard* card = pack->getCardById(it->first);
        if (!card)
            continue;
        for (int copy = 0; copy < it->second; copy++)
        {
            MTGCardInstance* ci = NEW MTGCardInstance(card, NULL);
            mDisplayInstances.push_back(ci);
            mPackDisplay->AddCard(ci);
        }
    }
}

void GameStateDraft::refreshPoolDisplay()
{
    SAFE_DELETE(mPoolDisplay);
    clearPoolDisplayInstances();

    // Top-right -- same column as the pack row below, clear of the big-card
    // preview on the left.
    DraftPoolDisplay* pool = NEW DraftPoolDisplay(2, SCREEN_WIDTH - 255, 10);
    mPoolDisplay = pool;

    // Collapse duplicates into one thumbnail + an "xN" badge instead of one
    // thumbnail per copy, ordered by when each card was first picked
    // (mHumanPickOrder -- the pool MTGDeck's cards map is keyed/ordered by
    // card id, not pick order). Dedup by name, not getMTGId(): a set can have
    // multiple distinct printings/ids sharing the same card name (same
    // pattern as basic lands having many ids in _cards.dat), so two picks of
    // the same-named card can land on different ids and dodge an id-keyed dedup.
    vector<MTGCard*> uniqueCards;
    map<string, int> countByName;
    map<string, int> slotByName;
    for (size_t i = 0; i < mHumanPickOrder.size(); i++)
    {
        MTGCard* card = mHumanPickOrder[i];
        const string& name = card->data->name;
        map<string, int>::iterator it = slotByName.find(name);
        if (it == slotByName.end())
        {
            slotByName[name] = (int) uniqueCards.size();
            uniqueCards.push_back(card);
            countByName[name] = 1;
        }
        else
        {
            countByName[name]++;
        }
    }

    int maxShown = kPoolCols * kPoolMaxRows;
    int total = (int) uniqueCards.size();
    int shown = (std::min)(total, maxShown);
    int startIdx = total - shown;

    for (int i = startIdx; i < total; i++)
    {
        MTGCard* card = uniqueCards[i];
        MTGCardInstance* ci = NEW MTGCardInstance(card, NULL);
        mPoolDisplayInstances.push_back(ci);
        pool->AddCardAt(ci, i - startIdx, countByName[card->data->name]);
    }
}

void GameStateDraft::Start()
{
    mDraftComplete = false;
    mHumanSeatId = 0;
    mReviewingPool = false;
    mQuitConfirmed = false;
    mSetChosen = false;
    mMultiSets.clear();
    closeQuitMenu();
    mHumanPickOrder.clear();

    mLoadError = "";

    mSetSelectStage = SEL_MODE;
    buildModeMenu();
    mSelectingSet = true;
}

bool GameStateDraft::isDraftableSet(MTGSetInfo* info) const
{
    return info && info->counts[MTGSetInfo::COMMON] >= kMinCommons
            && info->counts[MTGSetInfo::UNCOMMON] >= kMinUncommons && info->counts[MTGSetInfo::RARE] >= kMinRares;
}

int GameStateDraft::randomDraftableSet(int minYear, int maxYear) const
{
    vector<int> candidates;
    for (int i = 0; i < setlist.size(); i++)
    {
        MTGSetInfo* info = setlist.getInfo(i);
        if (!isDraftableSet(info))
            continue;
        if (minYear >= 0 && info->year < minYear)
            continue;
        if (maxYear >= 0 && info->year > maxYear)
            continue;
        candidates.push_back(i);
    }
    if (candidates.empty())
        return -1;
    return candidates[rand() % candidates.size()];
}

void GameStateDraft::buildModeMenu()
{
    SAFE_DELETE(mSetMenu);
    mSetMenu = NEW SimpleMenu(JGE::GetInstance(), WResourceManager::Instance(), kDraftModeMenuId, this, Fonts::MENU_FONT,
            SCREEN_WIDTH / 2 - 110, 20, "Draft format");
    mSetMenu->Add(kModeRandom, "Random set");
    mSetMenu->Add(kModeOld, "Old cards (random early set)");
    mSetMenu->Add(kModeNew, "New cards (random recent set)");
    mSetMenu->Add(kModePickOne, "Choose one set (3 packs)...");
    mSetMenu->Add(kModePickThree, "Choose 3 sets (1 pack each)...");
    mSetMenu->Add(kModeCancel, "Cancel");
}

void GameStateDraft::buildSetListMenu()
{
    SAFE_DELETE(mSetMenu);
    string title = "Choose a set to draft";
    if (mSetSelectStage == SEL_THREE)
    {
        char buf[48];
        sprintf(buf, "Choose set %d of 3", (int) mMultiSets.size() + 1);
        title = buf;
    }
    mSetMenu = NEW SimpleMenu(JGE::GetInstance(), WResourceManager::Instance(), kDraftSetMenuId, this, Fonts::MENU_FONT,
            SCREEN_WIDTH / 2 - 100, 20, title.c_str());

    for (int i = 0; i < setlist.size(); i++)
    {
        MTGSetInfo* info = setlist.getInfo(i);
        if (!isDraftableSet(info))
            continue;
        // Item id is the set id itself (>= 0); ButtonPressed reads it back
        // directly. Label with the long name plus the short code.
        string label = info->getName();
        if (label != info->id)
            label += " (" + info->id + ")";
        mSetMenu->Add(i, label.c_str());
    }

    mSetMenu->Add(kDraftSetMenuCancel, "Back");
}

// Loads a fresh copy of the rarity-slot template (1 rare / 3 uncommon /
// 10 common) and points it at one set. A fresh copy per set is needed because
// the three-sets mode drafts a different pool each round, and DraftSession
// holds a distinct pack pointer per round. NULL if the template file is
// missing.
MTGPack* GameStateDraft::makePackForSet(const string& setCode)
{
    MTGPack* p = NEW MTGPack();
    p->load("packs/draft_booster.txt");
    if (!p->isValid())
        p->load("Res/packs/draft_booster.txt"); // some run configs resolve resources one level up
    if (!p->isValid())
    {
        SAFE_DELETE(p);
        return NULL;
    }
    p->setPool("all set:" + setCode + ";");
    return p;
}

void GameStateDraft::beginDraftSingle(int setId)
{
    if (setId < 0)
    {
        mLoadError = "No draftable set found for that option";
        DebugTrace("[Draft] " << mLoadError);
        return;
    }
    string code = setlist[setId];
    MTGPack* p = makePackForSet(code);
    if (!p)
    {
        mLoadError = "Draft pack template failed to load: packs/draft_booster.txt";
        DebugTrace("[Draft] " << mLoadError);
        return;
    }

    clearDraftPacks();
    mDraftPacks.push_back(p);

    SAFE_DELETE(mSession);
    mSession = NEW DraftSession(8, MTGCollection(), 3, 14);
    mSession->setPackTemplate(p);
    DebugTrace("[Draft] drafting set " << code << " (all rounds)");
    startDraftSession();
}

void GameStateDraft::beginDraftMulti(const vector<int>& setIds)
{
    SAFE_DELETE(mSession);
    mSession = NEW DraftSession(8, MTGCollection(), (int) setIds.size(), 14);

    clearDraftPacks();
    for (size_t r = 0; r < setIds.size(); r++)
    {
        string code = setlist[setIds[r]];
        MTGPack* p = makePackForSet(code);
        if (!p)
        {
            mLoadError = "Draft pack template failed to load: packs/draft_booster.txt";
            DebugTrace("[Draft] " << mLoadError);
            return;
        }
        mDraftPacks.push_back(p);
        mSession->setPackTemplateForRound((int) r, p);
        DebugTrace("[Draft] round " << r << " set " << code);
    }
    startDraftSession();
}

void GameStateDraft::startDraftSession()
{
    mSession->getSeat(mHumanSeatId)->setIsBot(false);
    mSession->beginRound(0);
    mSession->resolveBotPicksForStep();
    refreshPackDisplay();
    refreshPoolDisplay();

    if (mDisplayInstances.empty())
    {
        mLoadError = "Draft pack produced 0 cards (check set has enough cards)";
        DebugTrace("[Draft] " << mLoadError);
    }
}

void GameStateDraft::End()
{
}

void GameStateDraft::logDraftSummary()
{
    for (int i = 0; i < mSession->getNumSeats(); i++)
    {
        DraftSeat* seat = mSession->getSeat(i);
        int first, second;
        seat->getTopColors(first, second);
        DebugTrace(
                "[Draft] seat " << i << (i == mHumanSeatId ? " (human)" : " (bot)") << ": " << seat->getTotalPicks()
                        << " picks, top colors " << first << "/" << second);
    }
}

void GameStateDraft::materializeDecks()
{
    // Both AIPlayerFactory::createAIPlayer() (AIPlayer.cpp:231) and
    // GameObserver::loadPlayer() (GameObserver.cpp:2335) hardcode their deck
    // paths ("ai/baka/deck%i.txt" and "<profile>/deck%i.txt" respectively) --
    // neither goes through DeckManager, so there's no scratch folder that
    // works for actually loading these into a match. A dedicated ai/draft/
    // folder (the previous version of this function) produces files nothing
    // in the engine will ever read.
    //
    // The human's deck is made safe by switching to a dedicated profile
    // first (below) -- deckN.txt then lands under profiles/WagicDraftTemp/,
    // never the player's real profile. Bot decks have no such isolation
    // available (ai/baka/ isn't profile-scoped -- confirmed by checking
    // every ai/baka reference in src/), so they use fixed high-numbered
    // slots instead, cleaned up at the start of the next draft.
    JFileSystem* fs = JFileSystem::GetInstance();
    for (int i = 0; i < 7; i++)
    {
        char stale[64];
        sprintf(stale, "ai/baka/deck%i.txt", kDraftBotDeckIdBase + i);
        fs->Remove(stale);
    }

    // Give the temp draft profile sensible settings instead of raw
    // GameOptions defaults (which show fancy mana, an invisible closed hand,
    // and every tutorial popup during the draft's matches).
    //
    // Two parts, in order:
    //   A. best-effort carry of the *real* profile's settings (key bindings,
    //      interrupt settings, tutorial-seen flags, etc.) applied directly to
    //      the live in-memory options -- immune to the newline/reload-resave
    //      issues that sank every file-copy attempt, since nothing depends on
    //      on-disk bytes being read back.
    //   B. force the two display options the player specifically wanted
    //      (simple mana, visible closed hand) AFTER the carry, so they're
    //      correct even if the carry read nothing.
    //
    // The real profile is whatever's active now -- but never let it be the
    // temp profile itself. If a previous draft left the player stuck on
    // WagicDraftTemp (the old restore bug), reading settings from it and, worse,
    // setting the restore target back to it, would cascade: empty carry, and
    // never returning to a real profile. Treat that case as "no known real
    // profile" and restore to the default profile ("") instead.
    string realProfile = options[Options::ACTIVE_PROFILE].str;
    if (realProfile == string(kDraftProfileName))
        realProfile = "";

    string originalSettings;
    JFileSystem::GetInstance()->readIntoString(options.profileFile(PLAYER_SETTINGS), originalSettings);
    DebugTrace("[Draft] carrying settings from profile '" << realProfile << "' (" << originalSettings.size() << " bytes)");

    // See GameApp.h -- GameStateMenu::Start() switches back to this once the
    // tournament ends or the player quits back to the main menu.
    GameApp::pendingProfileRestoreValue = realProfile;
    GameApp::pendingProfileRestore = true;

    options[Options::ACTIVE_PROFILE] = string(kDraftProfileName);
    options.reloadProfile();

    // A. best-effort carry
    if (originalSettings.size())
    {
        std::stringstream stream(originalSettings);
        string line;
        while (std::getline(stream, line))
        {
            if (!line.size())
                continue;
            if (line[line.size() - 1] == '\r')
                line.erase(line.size() - 1); // handle DOS line endings, like GameOptions::load
            if (!line.size())
                continue;
            size_t eq = line.find('=');
            if (eq == string::npos)
                continue;
            string name = line.substr(0, eq);
            string val = line.substr(eq + 1);
            int id = Options::getID(name);
            // Skip the global options (ACTIVE_PROFILE, LANG): applying
            // ACTIVE_PROFILE from the source would immediately switch us back
            // off the temp profile. Everything above LAST_GLOBAL is
            // profile-scoped and safe to carry.
            if (id != INVALID_OPTION && id > Options::LAST_GLOBAL)
                options[id].read(val);
            else if (id == INVALID_OPTION)
                options[name].read(val); // unknown keys (tuto_*, unlocked_*, ...)
        }
    }

    // B. guaranteed display defaults (must match the label strings in
    // OptionManaDisplay/OptionClosedHand, GameOptions.cpp)
    options[Options::MANADISPLAY].read("Simple");
    options[Options::CLOSEDHAND].read("visible");
    options.save();

    GameApp::pendingDraftBotDeckIds.clear();
    int botSlot = kDraftBotDeckIdBase;

    for (int i = 0; i < mSession->getNumSeats(); i++)
    {
        DraftSeat* seat = mSession->getSeat(i);
        if (!seat)
            continue;
        MTGDeck* deck = DraftDeckBuilder::buildDeck(seat, MTGCollection());

        if (i == mHumanSeatId)
        {
            string path = options.profileFile() + "/deck1.txt";
            deck->save(path, false, "My Draft Deck", "");
            GameApp::pendingDraftHumanDeckId = 1;
            DebugTrace("[Draft] human deck saved to " << path << " (" << deck->totalCards() << " cards)");
        }
        else
        {
            char path[64];
            sprintf(path, "ai/baka/deck%i.txt", botSlot);
            deck->save(path, false, "Bot Draft Deck", "");
            GameApp::pendingDraftBotDeckIds.push_back(botSlot);
            DebugTrace("[Draft] bot seat " << i << " deck saved to " << path << " (" << deck->totalCards() << " cards)");
            botSlot++;
        }
        SAFE_DELETE(deck);
    }
}

// Populate the temp draft profile's collection.dat with exactly the human's
// drafted pool plus a stock of basic lands, so the reused deck editor
// (GameStateDeckViewer reads playerdata->collection from the active profile)
// shows only what was drafted -- the player can't add cards they didn't
// draft, but has enough basics to build any mana base. Must run after
// materializeDecks() has switched to the temp profile.
void GameStateDraft::seedEditorCollection()
{
    DraftSeat* human = mSession->getSeat(mHumanSeatId);
    if (!human || !human->getPool())
        return;

    MTGDeck* collection = NEW MTGDeck(MTGCollection());
    collection->add(human->getPool()); // every drafted card, with its counts

    const int kBasicsPerColor = 30; // plenty for any 40-card mana base
    for (int c = Constants::MTG_COLOR_GREEN; c <= Constants::MTG_COLOR_WHITE; c++)
    {
        MTGCard* land = DraftDeckBuilder::getBasicLand(MTGCollection(), c);
        if (!land)
            continue;
        for (int i = 0; i < kBasicsPerColor; i++)
            collection->add(land);
    }

    collection->save(options.profileFile(PLAYER_COLLECTION), false, "collection", "");
    DebugTrace("[Draft] seeded editor collection with " << collection->totalCards() << " cards");
    SAFE_DELETE(collection);
}

void GameStateDraft::enterDeckEditor()
{
    // Saves the auto-built human deck1 + bot decks and switches to the temp
    // profile; seedEditorCollection() then fills that profile's collection so
    // the editor is scoped to the drafted pool.
    materializeDecks();
    seedEditorCollection();

    // Pre-configure everything the tournament needs now, while we have the
    // context -- none of it changes while the player edits, and it means the
    // editor's exit only has to flip pendingDraftTournament and transition.
    GameApp::players[0] = PLAYER_TYPE_HUMAN;
    GameApp::players[1] = PLAYER_TYPE_CPU;
    mParent->gameType = GAME_TYPE_CLASSIC;
    mParent->rules = Rules::getRulesByFilename("classic.txt");

    GameApp::pendingDraftDeckEdit = true;
    mParent->DoTransition(TRANSITION_FADE, GAME_STATE_DECK_VIEWER);
}

void GameStateDraft::handleHumanPick(int cardId)
{
    MTGDeck* pack = mSession->getPackForSeat(mHumanSeatId);
    if (!pack)
        return;
    MTGCard* originalCard = pack->getCardById(cardId);
    if (!originalCard)
        return;
    if (!mSession->submitPick(mHumanSeatId, originalCard))
        return;
    mHumanPickOrder.push_back(originalCard);

    mSession->resolveBotPicksForStep();
    if (!mSession->allSeatsPickedThisStep())
        return;

    mSession->advanceStep();

    if (mSession->isRoundComplete())
    {
        if (mSession->isDraftComplete())
        {
            mDraftComplete = true;
            logDraftSummary();
            return;
        }
        mSession->beginRound(mSession->getCurrentRound() + 1);
        mSession->resolveBotPicksForStep();
    }

    refreshPackDisplay();
    refreshPoolDisplay();
}

void GameStateDraft::Update(float dt)
{
    JButton btn = mEngine->ReadButton();

    if (mSelectingSet)
    {
        if (mSetMenu)
        {
            mSetMenu->CheckUserInput(btn);
            mSetMenu->Update(dt);
        }
        // mSetChosen is set by ButtonPressed (from inside CheckUserInput);
        // act on it here, off the menu's call stack, so deleting mSetMenu is safe.
        if (mSetChosen)
        {
            mSetChosen = false;
            int id = mChosenControlId;

            if (mChosenMenuId == kDraftModeMenuId)
            {
                SAFE_DELETE(mSetMenu);
                switch (id)
                {
                    case kModeCancel:
                        mSelectingSet = false;
                        mParent->DoTransition(TRANSITION_FADE, GAME_STATE_MENU);
                        break;
                    case kModeRandom:
                        mSelectingSet = false;
                        beginDraftSingle(randomDraftableSet(-1, -1));
                        break;
                    case kModeOld:
                        mSelectingSet = false;
                        beginDraftSingle(randomDraftableSet(-1, kOldEraMaxYear));
                        break;
                    case kModeNew:
                        mSelectingSet = false;
                        beginDraftSingle(randomDraftableSet(kNewEraMinYear, -1));
                        break;
                    case kModePickOne:
                        mSetSelectStage = SEL_ONE;
                        buildSetListMenu();
                        break;
                    case kModePickThree:
                        mSetSelectStage = SEL_THREE;
                        mMultiSets.clear();
                        buildSetListMenu();
                        break;
                    default:
                        break;
                }
            }
            else // kDraftSetMenuId (the set list)
            {
                if (id == kDraftSetMenuCancel)
                {
                    // "Back" -- return to the mode menu.
                    SAFE_DELETE(mSetMenu);
                    mSetSelectStage = SEL_MODE;
                    buildModeMenu();
                }
                else if (mSetSelectStage == SEL_ONE)
                {
                    SAFE_DELETE(mSetMenu);
                    mSelectingSet = false;
                    beginDraftSingle(id);
                }
                else // SEL_THREE
                {
                    mMultiSets.push_back(id);
                    SAFE_DELETE(mSetMenu);
                    if (mMultiSets.size() >= 3)
                    {
                        mSelectingSet = false;
                        beginDraftMulti(mMultiSets);
                    }
                    else
                    {
                        buildSetListMenu(); // pick the next set
                    }
                }
            }
        }
        return;
    }

    if (!mSession)
    {
        if (btn == JGE_BTN_OK || btn == JGE_BTN_SEC || btn == JGE_BTN_MENU)
            mParent->DoTransition(TRANSITION_FADE, GAME_STATE_MENU);
        return;
    }

    if (mDraftComplete)
    {
        if (btn == JGE_BTN_OK)
            enterDeckEditor();
        else if (btn == JGE_BTN_SEC || btn == JGE_BTN_MENU)
            mParent->DoTransition(TRANSITION_FADE, GAME_STATE_MENU);
        return;
    }

    if (!mPackDisplay)
        return;

    if (mQuitMenu)
    {
        mQuitMenu->CheckUserInput(btn);
        mQuitMenu->Update(dt);
        if (mQuitMenu->isClosed())
        {
            bool confirmed = mQuitConfirmed;
            closeQuitMenu();
            mQuitConfirmed = false;
            if (confirmed)
                mParent->DoTransition(TRANSITION_FADE, GAME_STATE_MENU);
        }
        return;
    }

    if (btn == JGE_BTN_MENU)
    {
        openQuitMenu();
        return;
    }

    // Same button GuiHand uses to toggle the hand open/closed
    // (GuiHand.cpp: "options[Options::REVERSETRIGGERS] ? JGE_BTN_PREV :
    // JGE_BTN_NEXT") -- JGE_BTN_CTRL has no on-screen Android control, this
    // one already does since it's used for exactly this kind of toggle
    // elsewhere.
    JButton reviewToggle = (options[Options::REVERSETRIGGERS].number ? JGE_BTN_PREV : JGE_BTN_NEXT);

    if (btn == reviewToggle)
    {
        mReviewingPool = !mReviewingPool;
    }
    else if (mReviewingPool)
    {
        // CheckUserInput isn't virtual, and DraftPoolDisplay overrides it
        // (like Render()) -- must call through the derived type or this
        // silently resolves to CardDisplay::CheckUserInput instead.
        if (mPoolDisplay)
            ((DraftPoolDisplay*) mPoolDisplay)->CheckUserInput(btn);
    }
    else if (btn == JGE_BTN_OK)
    {
        if (mPackDisplay->mCurr >= 0 && mPackDisplay->mCurr < (int) mPackDisplay->mObjects.size())
        {
            CardGui* focused = (CardGui*) mPackDisplay->mObjects[mPackDisplay->mCurr];
            if (focused && focused->card)
                handleHumanPick(focused->card->getMTGId());
        }
    }
    else
    {
        mPackDisplay->CheckUserInput(btn);
    }

    mPackDisplay->Update(dt);
    if (mPoolDisplay)
        mPoolDisplay->Update(dt);
}

void GameStateDraft::Render()
{
    if (mSelectingSet)
    {
        if (mSetMenu)
            mSetMenu->Render();
        return;
    }

    if (mPoolDisplay)
        ((DraftPoolDisplay*) mPoolDisplay)->Render();

    // CardDisplay::Render() always draws its own big-card preview of the
    // focused card at the same fixed screen position -- while reviewing the
    // pool, show the pool's preview there instead of the pack's, rather than
    // have both fight for the same space.
    if (mReviewingPool)
    {
        if (mPoolDisplay)
            ((DraftPoolDisplay*) mPoolDisplay)->RenderFocusedBig();

        WFont* font = WResourceManager::Instance()->GetWFont(Fonts::MAIN_FONT);
        if (font)
            font->DrawString("Reviewing picks (press the same button again to go back)", 10.0f, 10.0f);
    }
    else if (mPackDisplay)
    {
        mPackDisplay->Render();
    }

    if (!mLoadError.empty())
    {
        WFont* font = WResourceManager::Instance()->GetWFont(Fonts::MAIN_FONT);
        if (font)
        {
            font->DrawString(mLoadError, 10.0f, 10.0f);
            font->DrawString("(press any button to return to the menu)", 10.0f, 30.0f);
        }
    }

    if (mDraftComplete)
    {
        WFont* font = WResourceManager::Instance()->GetWFont(Fonts::MAIN_FONT);
        if (font)
        {
            font->DrawString("Draft complete!", 10.0f, 10.0f);
            font->DrawString("OK: edit your deck, then play the KO bracket   SEC/MENU: return to the main menu", 10.0f,
                    30.0f);
        }
    }

    if (mQuitMenu)
        mQuitMenu->Render();
}
