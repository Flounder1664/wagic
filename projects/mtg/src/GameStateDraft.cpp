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
        CardDisplay(id, NULL, px, py, NULL, NULL, kPoolCols * kPoolMaxRows)
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
                CardGui* cardg = (CardGui*) mObjects[i];
                char buffer[8];
                sprintf(buffer, "x%i", mCounts[i]);
                font->SetScale(0.8f);
                font->DrawString(buffer, cardg->x + 10, cardg->y + 20);
                font->SetScale(1.0f);
            }
        }
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
    // card id, not pick order).
    vector<MTGCard*> uniqueCards;
    map<int, int> countByCardId;
    map<int, int> slotByCardId;
    for (size_t i = 0; i < mHumanPickOrder.size(); i++)
    {
        MTGCard* card = mHumanPickOrder[i];
        int id = card->getMTGId();
        map<int, int>::iterator it = slotByCardId.find(id);
        if (it == slotByCardId.end())
        {
            slotByCardId[id] = (int) uniqueCards.size();
            uniqueCards.push_back(card);
            countByCardId[id] = 1;
        }
        else
        {
            countByCardId[id]++;
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
        pool->AddCardAt(ci, i - startIdx, countByCardId[card->getMTGId()]);
    }
}

void GameStateDraft::Start()
{
    mDraftComplete = false;
    mHumanSeatId = 0;
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

    if (btn == JGE_BTN_OK)
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
}

void GameStateDraft::Render()
{
    if (mPoolDisplay)
        ((DraftPoolDisplay*) mPoolDisplay)->Render();

    if (mPackDisplay)
        mPackDisplay->Render();

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
