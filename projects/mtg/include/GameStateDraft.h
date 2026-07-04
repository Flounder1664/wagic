#ifndef _GAME_STATE_DRAFT_H_
#define _GAME_STATE_DRAFT_H_

#include <vector>
#include <JGE.h>
#include "GameState.h"
#include "CardDisplay.h"

class DraftSession;
class MTGPack;
class MTGCardInstance;

// First interactive slice of draft mode (see GH issue #27): the human opens a
// pack, picks one card, bots resolve automatically, repeat until all 3
// rounds are done. Deliberately minimal -- no deck-build step yet, no
// materializing decks to disk, no tournament wiring. Entry point is an
// always-visible "Draft (test)" item in the Play submenu (GameStateMenu.cpp)
// while this is still feature-branch work in progress.
//
// Card focus/selection reuses CardDisplay entirely unmodified: CardDisplay's
// GameObserver/JGuiListener callback paths are for duel- and shop-specific
// flows that don't fit picking a card from a synthesized pack (see the design
// discussion in the GH issue), so this reads CardDisplay's already-public
// mCurr/mObjects state directly instead, and checks JGE_BTN_OK -- the single
// abstract "confirm" button JGE already normalizes Android touch/gamepad/PC
// input into (GuiLayers.cpp: mActionButton = JGE_BTN_OK).
class GameStateDraft: public GameState
{
public:
    GameStateDraft(GameApp* parent);
    virtual ~GameStateDraft();

    virtual void Create();
    virtual void Destroy();
    virtual void Start();
    virtual void End();
    virtual void Update(float dt);
    virtual void Render();

private:
    void refreshPackDisplay();
    void clearDisplayInstances();
    void handleHumanPick(int cardId);
    void logDraftSummary();

    DraftSession* mSession;
    MTGPack* mPack;
    CardDisplay* mPackDisplay;
    std::vector<MTGCardInstance*> mDisplayInstances;
    int mHumanSeatId;
    bool mDraftComplete;
};

#endif
