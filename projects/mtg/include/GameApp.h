/*
 *  Wagic, The Homebrew ?! is licensed under the BSD license
 *  See LICENSE in the Folder's root
 *  http://wololo.net/wagic/
 */

#ifndef _GAMEAPP_H_
#define _GAMEAPP_H_

#include <JApp.h>
#include <JGE.h>
#include <JSprite.h>
#include <JLBFont.h>
#include <hge/hgeparticle.h>
#include "WResourceManager.h"

#include "GameState.h"

#include "MTGDeck.h"
#include "MTGCard.h"
#include "MTGGameZones.h"

#ifdef NETWORK_SUPPORT
#include "JNetwork.h"
#endif //NETWORK_SUPPORT
#include "GameObserver.h"

#include "Wagic_Version.h"
class Rules;
class MTGAllCards;
class TransitionBase;

class GameApp: public JApp
{

private:
#ifdef DEBUG
    int nbUpdates;
    float totalFPS;
#endif
    bool mShowDebugInfo;
    int mScreenShotCount;

    GameState* mCurrentState;
    GameState* mNextState;
    GameState* mGameStates[GAME_STATE_MAX];
public:

    GameType gameType;
    Rules * rules;
    bool quickGame;
#ifdef NETWORK_SUPPORT
    string mServerAddress;
    JNetwork* mpNetwork;
#endif //NETWORK_SUPPORT

    GameApp();
    virtual ~GameApp();

    virtual void Create();
    virtual void Destroy();
    virtual void Update();
    virtual void Render();
    virtual void Pause();
    virtual void Resume();

    virtual void OnScroll(int inXVelocity, int inYVelocity);

    void LoadGameStates();
    void SetNextState(int state);
    void SetCurrentState(GameState * state);
    void DoTransition(int trans, int tostate, float dur = -1, bool animonly = false);
    void DoAnimation(int trans, float dur = -1);
    static hgeParticleSystem * Particles[6];
    static bool HasMusic;
    static string systemError;
    static char mynbcardsStr[512];
    static int mycredits;
    static JMusic* music;
    static string currentMusicFile;
    static void playMusic(string filename = "", bool loop = true);
    static void stopMusic();
    static void pauseMusic();
    static void resumeMusic();
    static PlayerType players[2];

    // Set by GameStateDraft before transitioning to GAME_STATE_DUEL, consumed
    // once by GameStateDuel::Start(). GameStateDraft can't reach the live
    // GameStateDuel instance directly (GameApp::mGameStates is private, no
    // accessor) to configure its Tournament object across the transition, so
    // this mirrors the existing `players[2]` pattern of passing config via a
    // static rather than adding a new access path.
    static bool pendingDraftTournament;
    static int pendingDraftHumanDeckId;
    static vector<int> pendingDraftBotDeckIds;

    // Set by GameStateDraft before transitioning to GAME_STATE_DECK_VIEWER so
    // the human can tweak their auto-built draft deck before the bracket.
    // Consumed by GameStateDeckViewer: while set, the editor's exit routes
    // into the draft tournament (sets pendingDraftTournament + transitions to
    // GAME_STATE_DUEL) instead of back to the main menu.
    static bool pendingDraftDeckEdit;

    // Set by GameStateDraft to the player's real ACTIVE_PROFILE value right
    // before switching to the temp draft profile; consumed by
    // GameStateMenu::Start() (reached both when the tournament finishes
    // normally and when the player quits mid-tournament back to the main
    // menu -- one hook catches both exits rather than needing a second one
    // inside GameStateDuel). Empty string means "nothing pending" -- also
    // the correct value when no profile was active to begin with, since
    // ACTIVE_PROFILE's own default is "".
    static bool pendingProfileRestore;
    static string pendingProfileRestoreValue;
};

extern vector<JQuadPtr> manaIcons;

#endif
