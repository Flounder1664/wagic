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

GameStateDraft::GameStateDraft(GameApp* parent) :
    GameState(parent, "draft")
{
    mSession = NULL;
    mPack = NULL;
    mPackDisplay = NULL;
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
    SAFE_DELETE(mPackDisplay);
    SAFE_DELETE(mSession);
    SAFE_DELETE(mPack);
}

void GameStateDraft::clearDisplayInstances()
{
    for (size_t i = 0; i < mDisplayInstances.size(); i++)
        SAFE_DELETE(mDisplayInstances[i]);
    mDisplayInstances.clear();
}

void GameStateDraft::refreshPackDisplay()
{
    SAFE_DELETE(mPackDisplay);
    clearDisplayInstances();

    mPackDisplay = NEW CardDisplay(1, NULL, 40, 40, NULL, NULL, 7);

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

void GameStateDraft::Start()
{
    mDraftComplete = false;
    mHumanSeatId = 0;

    if (!mPack)
    {
        mPack = NEW MTGPack();
        mPack->load("packs/ecl_draft_booster.txt");
    }

    SAFE_DELETE(mSession);
    mSession = NEW DraftSession(8, MTGCollection(), 3, 14);
    mSession->setPackTemplate(mPack);
    mSession->getSeat(mHumanSeatId)->setIsBot(false);

    mSession->beginRound(0);
    mSession->resolveBotPicksForStep();
    refreshPackDisplay();
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
}

void GameStateDraft::Update(float dt)
{
    if (!mSession)
        return;

    JButton btn = mEngine->ReadButton();

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
    if (mPackDisplay)
        mPackDisplay->Render();
}
