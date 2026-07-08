#ifndef _GAME_STATE_DRAFT_H_
#define _GAME_STATE_DRAFT_H_

#include <vector>
#include <string>
#include <JGE.h>
#include "GameState.h"
#include "CardDisplay.h"

class DraftSession;
class MTGPack;
class MTGCard;
class MTGCardInstance;
class MTGSetInfo;
class SimpleMenu;

// First interactive slice of draft mode (see GH issue #27): the human opens a
// pack, picks one card, bots resolve automatically, repeat until all 3
// rounds are done, then every seat's deck is built (DraftDeckBuilder) and
// saved -- the human's under a dedicated profile (WagicDraftTemp), the 7
// bots' at fixed high-numbered ai/baka/ slots (neither DeckManager nor a
// scratch folder is an option here: both AIPlayerFactory::createAIPlayer()
// and GameObserver::loadPlayer() hardcode their deck paths, see
// GameStateDraft.cpp). Pressing OK on the "draft complete" screen then feeds
// all 8 decks into a real KO Tournament (GameStateDuel::
// setupPendingDraftTournament(), triggered via GameApp::pendingDraftTournament
// since GameStateDraft has no direct access to the live GameStateDuel
// instance) and starts playing the bracket. Deliberately minimal still -- no
// human deck-build/editing step (the human gets an auto-built deck like the
// bots do, for now), and the temp profile doesn't auto-restore to the
// player's real one after the tournament ends (known gap). Entry point is an
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
class GameStateDraft: public GameState, public JGuiListener
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
    virtual void ButtonPressed(int controllerId, int controlId);

private:
    void refreshPackDisplay();
    void refreshPoolDisplay();
    void clearDisplayInstances();
    void clearPoolDisplayInstances();
    void handleHumanPick(int cardId);
    void logDraftSummary();
    void materializeDecks();
    void seedEditorCollection();
    void enterDeckEditor();
    void openQuitMenu();
    void closeQuitMenu();
    // Set-selection flow, shown before the first pack. A two-level menu: a
    // "mode" menu (random / era / one set / three sets) then, for the last
    // two, the set list itself.
    void buildModeMenu();
    void buildSetListMenu();
    bool isDraftableSet(MTGSetInfo* info) const;
    int randomDraftableSet(int minYear, int maxYear) const; // -1 bounds = unbounded; -1 return = none
    MTGPack* makePackForSet(const std::string& setCode); // NULL on template-load failure
    void beginDraftSingle(int setId); // all 3 rounds from one set
    void beginDraftMulti(const std::vector<int>& setIds); // one pack each from N sets
    void startDraftSession(); // shared tail: seat 0 -> human, begin round 0, refresh
    void clearDraftPacks();

    // Which menu is showing during set selection.
    enum SetSelectStage
    {
        SEL_MODE,   // the top mode menu
        SEL_ONE,    // pick a single set for all 3 rounds
        SEL_THREE   // pick 3 sets, one pack each
    };

    DraftSession* mSession;
    std::vector<MTGPack*> mDraftPacks; // owned; must outlive mSession (it holds raw ptrs)
    CardDisplay* mPackDisplay; // the current pack, interactive
    CardDisplay* mPoolDisplay; // cards picked so far this draft -- browsable in review mode
    SimpleMenu* mQuitMenu; // confirm before actually leaving to the main menu
    SimpleMenu* mSetMenu; // reused for both the mode menu and the set list
    std::vector<MTGCardInstance*> mDisplayInstances;
    std::vector<MTGCardInstance*> mPoolDisplayInstances;
    std::vector<MTGCard*> mHumanPickOrder; // not owned -- cards live in MTGCollection()
    std::vector<int> mMultiSets; // accumulates the 3 chosen sets in SEL_THREE
    int mHumanSeatId;
    bool mSelectingSet; // true while a set-selection menu is up, before drafting
    int mSetSelectStage;
    int mChosenControlId; // set by ButtonPressed(), acted on next Update() (avoid delete-in-callback)
    int mChosenMenuId; // which menu fired the choice (kDraftModeMenuId / kDraftSetMenuId)
    bool mSetChosen;
    bool mDraftComplete;
    bool mReviewingPool; // toggles between picking and browsing the pool
    bool mQuitConfirmed; // set by ButtonPressed(), acted on later once mQuitMenu->isClosed()
    std::string mLoadError; // non-empty if the pack failed to load or produced no cards
};

#endif
