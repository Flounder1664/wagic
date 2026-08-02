#ifndef _PLAYER_H_
#define _PLAYER_H_

#include "JGE.h"
#include "MTGGameZones.h"
#include "Damage.h"
#include "Targetable.h"

class MTGDeck;
class MTGPlayerCards;
class MTGInPlay;
class ManaPool;

class Player: public Damageable
{
protected:
    ManaPool * manaPool;
    JTexture * mAvatarTex;
    JQuadPtr mAvatar;
    bool loadAvatar(string file, string resName = "playerAvatar");
    bool premade;

public:
    enum Mode
    {
        MODE_TEST_SUITE,
        MODE_HUMAN,
        MODE_AI
    };

    int deckId;
    string mAvatarName;
    Mode playMode;
    bool nomaxhandsize;
    //Ascend: once you control 10+ permanents, you have the city's blessing
    //for the rest of the game -- never resets once true.
    bool cityBlessing;
    //Storied: once you control 3+ artifacts/legendaries/Sagas, you have an
    //enduring story for the rest of the game -- never resets once true.
    bool enduringStory;
    MTGPlayerCards * game;
    MTGDeck * mDeck;
    string deckFile;
    string deckFileSmall;
    string deckName;
    string phaseRing;
    int offerInterruptOnPhase;
    int skippingTurn;
    int extraTurn;
    int drawCounter;
    int energyCount;
    int experienceCount;
    int yidaroCount;
    int ringTemptations;
    int dungeonCompleted;
    int numOfCommandCast;
    int monarch;
    int initiative;
    int surveilOffset;
    int devotionOffset;
    int lastShuffleTurn;
    //Number of cards this player exiled via Serum Powder's redraw. The
    //opening-hand rules (Leylines, the Mulligan menu) detect the pre-game
    //window by "graveyard and exile are empty"; Serum Powder legitimately
    //fills exile before the game starts, so those checks compare against
    //this count instead of zero.
    int exiledBySerum;
    //London mulligan: number of times this player has mulliganed. On each
    //mulligan the player redraws a FULL opening hand; when they keep, they
    //put this many cards from hand on the bottom of their library.
    int handMulligans;
    //>0 while the player is choosing which cards to put on the bottom after
    //keeping a mulliganed hand (one click per card). Serialized so save/undo
    //mid-selection is consistent.
    int cardsToBottom;
    //Set when the player commits to keeping a mulliganed hand. Until then,
    //a player who has mulliganed (handMulligans>0) is held in the opening
    //window: they must Mulligan again or Keep Hand (which bottoms cards).
    bool keptOpeningHand;
    //Move a card from this player's hand to the bottom of their library
    //(London-mulligan bottoming). Mirrors AALibraryBottom's placement.
    void bottomCardFromHand(MTGCardInstance * card);
    int epic;
    int forcefield;
    int dealsdamagebycombat;
    int initLife;
    int raidcount;
    int cycledCount;
    int handmodifier;
    int snowManaG;
    int snowManaR;
    int snowManaB;
    int snowManaU;
    int snowManaW;
    int snowManaC;
    string lastChosenName;
    vector<string> prowledTypes;
    Player(GameObserver *observer, string deckFile, string deckFileSmall, MTGDeck * deck = NULL);
    virtual ~Player();
    virtual void setObserver(GameObserver*g);
    virtual void End();
    virtual int displayStack()
    {
        return 1;
    }
    const string getDisplayName() const;

    int afterDamage();

    // Added source of life gain/loss in order to check later a possible exception.
    int gainLife(int value, MTGCardInstance* source);
    int loseLife(int value, MTGCardInstance* source);
    int gainOrLoseLife(int value, MTGCardInstance* source);

    bool isPoisoned() {return (poisonCount > 0);}
    int poisoned();
    int damaged();
    int prevented();
    void unTapPhase();
    MTGInPlay * inPlay();
    ManaPool * getManaPool();
    void takeMulligan();
    void serumMulligan();
    bool hasPossibleAttackers();
    bool noPossibleAttackers();
    bool DeadLifeState(bool check = false);
    ManaCost * doesntEmpty;
    ManaCost * poolDoesntEmpty;
    ManaCost * AuraIncreased;
    ManaCost * AuraReduced;
    void cleanupPhase();
    virtual int Act(float)
    {
        return 0;
    }

    virtual int isAI()
    {
        return 0;
    }

    bool isHuman()
    {
        return (playMode == MODE_HUMAN);
    }

    Player * opponent();
    int getId();
    JQuadPtr getIcon();

    virtual int receiveEvent(WEvent *)
    {
        return 0;
    }

    virtual void Render()
    {
    }

    /**
    ** Returns the path to the stats file of currently selected deck. 
    */
    std::string GetCurrentDeckStatsFile();
    virtual bool parseLine(const string& s);
    friend ostream& operator<<(ostream&, const Player&);
    friend istream& operator>>(istream&, Player&);
    bool operator<(Player& aPlayer);
    bool isDead();
};

class HumanPlayer: public Player
{
public:
    HumanPlayer(GameObserver *observer, string deckFile, string deckFileSmall, bool premade = false, MTGDeck * deck = NULL);
    void End();
    friend ostream& operator<<(ostream&, const HumanPlayer&);
};

#endif
