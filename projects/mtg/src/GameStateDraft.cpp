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
#include <JRenderer.h>
#include <algorithm>

namespace
{
const int kPoolCols = 7;
const int kPoolMaxRows = 4;
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
            return false;

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
                // Kept inside the card's own ~38-unit-tall footprint (badge
                // spans y+6..y+17) -- it previously sat at y+20..y+35, which
                // overran into the row below's cards, drawn after it in
                // index order and so painted over it.
                CardGui* cardg = (CardGui*) mObjects[i];
                char buffer[8];
                sprintf(buffer, "x%i", mCounts[i]);
                font->SetScale(0.6f);
                float bx = cardg->x - 10.0f;
                float by = cardg->y + 6.0f;
                float bw = font->GetStringWidth(buffer) + 4.0f;
                r->FillRect(bx, by, bw, 11.0f, ARGB(200,0,0,0));
                r->DrawRect(bx, by, bw, 11.0f, ARGB(220,240,240,240));
                font->DrawString(buffer, bx + 2.0f, by - 1.0f);
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
    mHumanSeatId = 0;
    mDraftComplete = false;
    mReviewingPool = false;
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
    SAFE_DELETE(mSession);
    SAFE_DELETE(mPack);
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
        if (btn == JGE_BTN_OK || btn == JGE_BTN_SEC || btn == JGE_BTN_MENU)
            mParent->DoTransition(TRANSITION_FADE, GAME_STATE_MENU);
        return;
    }

    if (!mPackDisplay)
        return;

    if (btn == JGE_BTN_MENU)
    {
        mParent->DoTransition(TRANSITION_FADE, GAME_STATE_MENU);
        return;
    }

    if (btn == JGE_BTN_CTRL)
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
            font->DrawString("Reviewing picks (CTRL to go back)", 10.0f, 10.0f);
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
            font->DrawString("Draft complete! (press any button to return to the menu)", 10.0f, 10.0f);
    }
}
