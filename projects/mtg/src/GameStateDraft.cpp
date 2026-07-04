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
    mPack = NULL;
    mPackDisplay = NULL;
    mPoolDisplay = NULL;
    mQuitMenu = NULL;
    mHumanSeatId = 0;
    mDraftComplete = false;
    mReviewingPool = false;
    mQuitConfirmed = false;
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
    SAFE_DELETE(mSession);
    SAFE_DELETE(mPack);
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
    if (controllerId != kDraftQuitMenuId || !mQuitMenu)
        return;

    // ButtonPressed() runs from inside mQuitMenu->CheckUserInput() -- deleting
    // mQuitMenu here (as a previous version of this did) deletes the object
    // out from under its own still-running call, a use-after-free that
    // crashed on "Quit to Main Menu". SimpleMenu::Close() (SimpleMenu.cpp:
    // 368-372) only sets a flag/starts a brief close animation; the actual
    // delete happens later in Update(), once isClosed() is true and we're no
    // longer anywhere on mQuitMenu's own call stack.
    mQuitConfirmed = (controlId == kDraftQuitMenuConfirm);
    mQuitMenu->Close();
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
    closeQuitMenu();
    mHumanPickOrder.clear();

    mLoadError = "";

    if (!mPack)
    {
        mPack = NEW MTGPack();
        mPack->load("packs/ecl_draft_booster.txt");
        if (!mPack->isValid())
            mPack->load("Res/packs/ecl_draft_booster.txt"); // see MTGDraft.cpp's smoke test: some
                                                              // run configurations resolve resource
                                                              // paths relative to a folder above Res/
    }

    if (!mPack->isValid())
    {
        mLoadError = "Draft pack failed to load: packs/ecl_draft_booster.txt";
        DebugTrace("[Draft] " << mLoadError);
        return;
    }

    SAFE_DELETE(mSession);
    mSession = NEW DraftSession(8, MTGCollection(), 3, 14);
    mSession->setPackTemplate(mPack);
    mSession->getSeat(mHumanSeatId)->setIsBot(false);

    mSession->beginRound(0);
    mSession->resolveBotPicksForStep();
    refreshPackDisplay();
    refreshPoolDisplay();

    if (mDisplayInstances.empty())
    {
        mLoadError = "Draft pack loaded but produced 0 cards (check pool filter / set id)";
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

    options[Options::ACTIVE_PROFILE] = string(kDraftProfileName);
    options.reloadProfile();

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

void GameStateDraft::startTournamentMatch()
{
    materializeDecks();

    GameApp::players[0] = PLAYER_TYPE_HUMAN;
    GameApp::players[1] = PLAYER_TYPE_CPU;
    mParent->gameType = GAME_TYPE_CLASSIC;
    mParent->rules = Rules::getRulesByFilename("classic.txt");
    GameApp::pendingDraftTournament = true;

    mParent->DoTransition(TRANSITION_FADE, GAME_STATE_DUEL);
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

    if (!mSession)
    {
        if (btn == JGE_BTN_OK || btn == JGE_BTN_SEC || btn == JGE_BTN_MENU)
            mParent->DoTransition(TRANSITION_FADE, GAME_STATE_MENU);
        return;
    }

    if (mDraftComplete)
    {
        if (btn == JGE_BTN_OK)
            startTournamentMatch();
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
            font->DrawString("OK: play your KO bracket now   SEC/MENU: return to the main menu", 10.0f, 30.0f);
        }
    }

    if (mQuitMenu)
        mQuitMenu->Render();
}
