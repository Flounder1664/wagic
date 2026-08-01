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

// Booster draft mode (see GH issue #27): choose a draft format (one set for
// 3 packs, 3 different sets, random, or an era filter) and set, draft a pod
// against 7 bots, tweak the auto-built deck in the reused deck editor
// (GameStateDeckViewer, entered via GameApp::pendingDraftDeckEdit), then play
// a best-of-3 KO bracket against the bots' decks. Every seat's deck is built
// by DraftDeckBuilder and saved -- the human's under a dedicated profile
// (WagicDraftTemp, auto-restored to the player's real profile once the
// session ends), the 7 bots' at fixed high-numbered ai/baka/ slots (neither
// DeckManager nor a scratch folder is an option here: both
// AIPlayerFactory::createAIPlayer() and GameObserver::loadPlayer() hardcode
// their deck paths, see GameStateDraft.cpp). The bracket itself is fed via
// GameStateDuel::setupPendingDraftTournament(), triggered through
// GameApp::pendingDraftTournament since GameStateDraft has no direct access
// to the live GameStateDuel instance. Entry point is "Draft" in the Play
// submenu (GameStateMenu.cpp).
//
// Known gaps: no sideboarding between games of the best-of-3 (tracked
// separately in GH issue #28, alongside constructed/Quest); the whole-profile
// settings carry (key bindings, interrupt settings, tutorial-seen flags) into
// the temp profile is best-effort and can silently carry nothing -- mana
// style and closed-hand visibility are forced explicitly so those two are
// reliable regardless; only tested on Windows so far, Android unverified.
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
