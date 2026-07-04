#ifndef _MTGDRAFT_H_
#define _MTGDRAFT_H_

#include <vector>
#include <map>
#include <string>

class MTGCard;
class MTGDeck;
class MTGPack;
class MTGAllCards;

// One drafter's accumulated state: everything picked so far, and a running
// tally of colors picked (used by BotDraftPicker to judge color commitment).
class DraftSeat
{
public:
    DraftSeat(int seatId, bool isBot, MTGAllCards* database);
    ~DraftSeat();

    int getSeatId() const
    {
        return mSeatId;
    }
    bool isBot() const
    {
        return mIsBot;
    }
    MTGDeck* getPool() const
    {
        return mPool;
    }
    int getTotalPicks() const
    {
        return mTotalPicks;
    }

    void recordPick(MTGCard* card);
    int getColorPickCount(int mtgColor) const;
    // The (up to) two colors this seat has picked the most of so far.
    void getTopColors(int& first, int& second) const;

    // The human seat(s) default to bot-controlled at construction; the UI
    // flips this once it takes over a seat so resolveBotPicksForStep() knows
    // to leave that seat's pick to an explicit submitPick() call instead.
    void setIsBot(bool isBot)
    {
        mIsBot = isBot;
    }

private:
    int mSeatId;
    bool mIsBot;
    MTGDeck* mPool;
    std::map<int, int> mColorPickCounts;
    int mTotalPicks;
};

// Abstracts "given this pack, which card does this seat take" so the human
// seat can later be driven by UI input without the rotation engine caring.
class DraftPicker
{
public:
    virtual ~DraftPicker()
    {
    }
    virtual MTGCard* pick(DraftSeat& seat, MTGDeck& pack) = 0;
};

class BotDraftPicker: public DraftPicker
{
public:
    virtual MTGCard* pick(DraftSeat& seat, MTGDeck& pack);
    static float scoreCard(MTGCard* card, const DraftSeat& seat);

private:
    // Below this many total picks, a bot hasn't committed to colors yet and
    // just takes the best card in the pack.
    static const int kColorCommitThreshold = 6;
};

// Runs the pack-passing rotation for a full booster draft: numRounds packs
// of cardsPerPack cards, direction alternating each round, one pick per seat
// per step.
//
// Driving model: a GameState's Update()/Render() loop can't block waiting for
// a click, so the rotation is exposed as incremental steps (beginRound() /
// getPackForSeat() / submitPick() / resolveBotPicksForStep() / advanceStep())
// rather than a single call that runs the whole draft. runFullDraft() is a
// thin convenience wrapper around those same primitives for headless
// simulation/testing, where every seat is bot-controlled.
class DraftSession
{
public:
    // Seats default to bot-controlled (BotDraftPicker); call
    // getSeat(id)->setIsBot(false) to hand a seat to interactive (human)
    // input instead -- resolveBotPicksForStep() then leaves it for an
    // explicit submitPick() call rather than auto-resolving it.
    // Default cardsPerPack is 14, not 15: real packs have a free basic land
    // slot that isn't part of the draft pick pool (see the deck-build addendum
    // in the GH issue -- basics are seeded separately, not drafted).
    DraftSession(int numSeats, MTGAllCards* database, int numRounds = 3, int cardsPerPack = 14);
    ~DraftSession();

    // Every seat opens the same set each round (like real draft -- one booster
    // pool per round, not a per-seat choice), but the set can change between
    // rounds 1/2/3 (e.g. round 1 from set A, rounds 2-3 from set B). Which set
    // to use for which round is a selection-process decision for later; this
    // just makes the plumbing not assume "one set for the whole draft.
    // Not owned -- caller loads/keeps the MTGPack definitions alive.
    void setPackTemplate(MTGPack* pack); // convenience: same pack for every round
    void setPackTemplateForRound(int round, MTGPack* pack);

    // Not owned by the session; pass NULL to revert the seat to the shared bot picker.
    void setPicker(int seatId, DraftPicker* picker);

    // -- Incremental driving (what the interactive UI calls) --
    bool beginRound(int round); // assembles that round's N packs; call once per round
    MTGDeck* getPackForSeat(int seatId) const; // pack currently in front of a seat, or NULL
    bool submitPick(int seatId, MTGCard* card); // records one seat's pick for the current step
    bool hasPickedThisStep(int seatId) const;
    void resolveBotPicksForStep(); // auto-resolves every bot seat that hasn't picked yet this step
    bool allSeatsPickedThisStep() const;
    bool advanceStep(); // rotates packs to the next pick; false if nothing left to advance
    bool isRoundComplete() const;
    bool isDraftComplete() const;
    int getCurrentRound() const
    {
        return mCurrentRound;
    }
    int getPickInRound() const
    {
        return mPickInRound;
    }

    // -- Headless convenience: drives the above for every seat via pickers --
    bool runFullDraft();

    DraftSeat* getSeat(int seatId) const;
    int getNumSeats() const
    {
        return (int) mSeats.size();
    }
    int getNumRounds() const
    {
        return mNumRounds;
    }
    int getCardsPerPack() const
    {
        return mCardsPerPack;
    }

private:
    void endRound();

    int mNumRounds;
    int mCardsPerPack;
    std::vector<MTGPack*> mRoundPacks; // one slot per round, sized to mNumRounds
    std::vector<DraftSeat*> mSeats;
    std::vector<DraftPicker*> mPickers;
    BotDraftPicker mDefaultBotPicker;

    int mCurrentRound; // -1 until beginRound() is first called
    int mPickInRound;
    int mDirection;
    std::vector<MTGDeck*> mCurrentPacks; // valid between beginRound() and the round ending
    std::vector<bool> mPickedThisStep;
};

#ifdef TESTSUITE
bool runDraftEngineSmokeTest();
#endif

#endif
