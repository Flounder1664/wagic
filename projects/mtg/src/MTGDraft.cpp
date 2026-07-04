#include "PrecompiledHeader.h"

#include <algorithm>
#include <cctype>

#include "MTGDraft.h"
#include "MTGDeck.h"
#include "MTGCard.h"
#include "CardPrimitive.h"
#include "WDataSrc.h"
#include "MTGPack.h"
#include "MTGDefinitions.h"
#include "DebugRoutines.h"

DraftSeat::DraftSeat(int seatId, bool isBot, MTGAllCards* database) :
    mSeatId(seatId), mIsBot(isBot), mTotalPicks(0)
{
    mPool = NEW MTGDeck(database);
}

DraftSeat::~DraftSeat()
{
    SAFE_DELETE(mPool);
}

void DraftSeat::recordPick(MTGCard* card)
{
    if (!card || !card->data)
        return;

    mPool->add(card);
    mTotalPicks++;

    for (int c = Constants::MTG_COLOR_GREEN; c <= Constants::MTG_COLOR_WHITE; c++)
    {
        if (card->data->hasColor(c))
            mColorPickCounts[c]++;
    }
}

int DraftSeat::getColorPickCount(int mtgColor) const
{
    std::map<int, int>::const_iterator it = mColorPickCounts.find(mtgColor);
    return it == mColorPickCounts.end() ? 0 : it->second;
}

void DraftSeat::getTopColors(int& first, int& second) const
{
    first = -1;
    second = -1;
    int firstCount = 0, secondCount = 0;

    for (std::map<int, int>::const_iterator it = mColorPickCounts.begin(); it != mColorPickCounts.end(); ++it)
    {
        if (it->second > firstCount)
        {
            second = first;
            secondCount = firstCount;
            first = it->first;
            firstCount = it->second;
        }
        else if (it->second > secondCount)
        {
            second = it->first;
            secondCount = it->second;
        }
    }
}

float BotDraftPicker::scoreCard(MTGCard* card, const DraftSeat& seat)
{
    if (!card || !card->data)
        return -1000.f;

    CardPrimitive* data = card->data;
    if (data->isLand())
        return -1000.f;

    float score = 0.f;
    switch (card->getRarity())
    {
        case Constants::RARITY_M:
            score += 40.f;
            break;
        case Constants::RARITY_R:
            score += 30.f;
            break;
        case Constants::RARITY_U:
            score += 15.f;
            break;
        default:
            score += 10.f;
            break;
    }

    if (data->isCreature())
        score += 5.f;

    string lc = data->text;
    std::transform(lc.begin(), lc.end(), lc.begin(), ::tolower);
    if (lc.find("destroy target") != string::npos || lc.find("damage to target") != string::npos
            || lc.find("damage to any target") != string::npos)
        score += 8.f;

    bool colorless = true;
    for (int c = Constants::MTG_COLOR_GREEN; c <= Constants::MTG_COLOR_WHITE; c++)
    {
        if (data->hasColor(c))
        {
            colorless = false;
            break;
        }
    }
    if (colorless)
        return score;

    if (seat.getTotalPicks() < kColorCommitThreshold)
        return score;

    int first, second;
    seat.getTopColors(first, second);
    bool matchesTop = (first >= 0 && data->hasColor(first)) || (second >= 0 && data->hasColor(second));

    if (matchesTop)
    {
        int weight = 0;
        if (first >= 0 && data->hasColor(first))
            weight += seat.getColorPickCount(first);
        if (second >= 0 && data->hasColor(second))
            weight += seat.getColorPickCount(second);
        score += (std::min)(weight, 20) * 0.5f;
    }
    else
    {
        score -= 15.f;
    }

    return score;
}

MTGCard* BotDraftPicker::pick(DraftSeat& seat, MTGDeck& pack)
{
    MTGCard* best = NULL;
    float bestScore = -1e9f;

    for (map<int, int>::iterator it = pack.cards.begin(); it != pack.cards.end(); ++it)
    {
        if (it->second <= 0)
            continue;
        MTGCard* card = pack.getCardById(it->first);
        if (!card)
            continue;
        float s = scoreCard(card, seat);
        if (s > bestScore)
        {
            bestScore = s;
            best = card;
        }
    }
    return best;
}

DraftSession::DraftSession(int numSeats, MTGAllCards* database, int numRounds, int cardsPerPack) :
    mNumRounds(numRounds), mCardsPerPack(cardsPerPack), mCurrentRound(-1), mPickInRound(0), mDirection(1)
{
    mRoundPacks.resize(numRounds, (MTGPack*) NULL);
    mSeats.resize(numSeats, NULL);
    mPickers.resize(numSeats, (DraftPicker*) NULL);
    mCurrentPacks.resize(numSeats, (MTGDeck*) NULL);
    mPickedThisStep.resize(numSeats, false);
    for (int i = 0; i < numSeats; i++)
        mSeats[i] = NEW DraftSeat(i, true, database);
}

DraftSession::~DraftSession()
{
    for (size_t i = 0; i < mCurrentPacks.size(); i++)
        SAFE_DELETE(mCurrentPacks[i]);
    for (size_t i = 0; i < mSeats.size(); i++)
        SAFE_DELETE(mSeats[i]);
}

void DraftSession::setPackTemplate(MTGPack* pack)
{
    for (size_t i = 0; i < mRoundPacks.size(); i++)
        mRoundPacks[i] = pack;
}

void DraftSession::setPackTemplateForRound(int round, MTGPack* pack)
{
    if (round >= 0 && round < (int) mRoundPacks.size())
        mRoundPacks[round] = pack;
}

void DraftSession::setPicker(int seatId, DraftPicker* picker)
{
    if (seatId >= 0 && seatId < (int) mPickers.size())
        mPickers[seatId] = picker;
}

DraftSeat* DraftSession::getSeat(int seatId) const
{
    if (seatId >= 0 && seatId < (int) mSeats.size())
        return mSeats[seatId];
    return NULL;
}

bool DraftSession::beginRound(int round)
{
    if (mSeats.empty() || round < 0 || round >= mNumRounds)
        return false;
    MTGPack* roundPack = mRoundPacks[round];
    if (!roundPack)
        return false;

    for (size_t i = 0; i < mCurrentPacks.size(); i++)
        SAFE_DELETE(mCurrentPacks[i]);

    int n = (int) mSeats.size();
    for (int i = 0; i < n; i++)
    {
        mCurrentPacks[i] = NEW MTGDeck(mSeats[i]->getPool()->database);
        roundPack->assemblePack(mCurrentPacks[i]);
    }

    mCurrentRound = round;
    mPickInRound = 0;
    mDirection = (round % 2 == 0) ? 1 : -1;
    std::fill(mPickedThisStep.begin(), mPickedThisStep.end(), false);
    return true;
}

MTGDeck* DraftSession::getPackForSeat(int seatId) const
{
    if (seatId < 0 || seatId >= (int) mCurrentPacks.size())
        return NULL;
    return mCurrentPacks[seatId];
}

bool DraftSession::submitPick(int seatId, MTGCard* card)
{
    if (seatId < 0 || seatId >= (int) mSeats.size() || !card)
        return false;
    if (mPickedThisStep[seatId])
        return false;
    MTGDeck* pack = mCurrentPacks[seatId];
    if (!pack || pack->totalCards() <= 0)
        return false;

    pack->remove(card);
    mSeats[seatId]->recordPick(card);
    mPickedThisStep[seatId] = true;
    return true;
}

bool DraftSession::hasPickedThisStep(int seatId) const
{
    if (seatId < 0 || seatId >= (int) mPickedThisStep.size())
        return false;
    return mPickedThisStep[seatId];
}

void DraftSession::resolveBotPicksForStep()
{
    for (size_t i = 0; i < mSeats.size(); i++)
    {
        if (mPickedThisStep[i] || !mSeats[i]->isBot())
            continue;
        MTGDeck* pack = mCurrentPacks[i];
        if (!pack || pack->totalCards() <= 0)
        {
            mPickedThisStep[i] = true; // nothing to pick; don't block the step on an empty pack
            continue;
        }
        DraftPicker* picker = mPickers[i] ? mPickers[i] : (DraftPicker*) &mDefaultBotPicker;
        MTGCard* chosen = picker->pick(*mSeats[i], *pack);
        if (chosen)
        {
            pack->remove(chosen);
            mSeats[i]->recordPick(chosen);
        }
        mPickedThisStep[i] = true;
    }
}

bool DraftSession::allSeatsPickedThisStep() const
{
    for (size_t i = 0; i < mPickedThisStep.size(); i++)
        if (!mPickedThisStep[i])
            return false;
    return true;
}

void DraftSession::endRound()
{
    for (size_t i = 0; i < mCurrentPacks.size(); i++)
        SAFE_DELETE(mCurrentPacks[i]);
}

bool DraftSession::advanceStep()
{
    if (mCurrentRound < 0 || !allSeatsPickedThisStep())
        return false;

    int n = (int) mSeats.size();
    if (mDirection > 0)
        std::rotate(mCurrentPacks.begin(), mCurrentPacks.begin() + (n - 1), mCurrentPacks.end());
    else
        std::rotate(mCurrentPacks.begin(), mCurrentPacks.begin() + 1, mCurrentPacks.end());

    mPickInRound++;
    std::fill(mPickedThisStep.begin(), mPickedThisStep.end(), false);

    if (mPickInRound >= mCardsPerPack)
        endRound();

    return true;
}

bool DraftSession::isRoundComplete() const
{
    return mCurrentRound >= 0 && mPickInRound >= mCardsPerPack;
}

bool DraftSession::isDraftComplete() const
{
    return isRoundComplete() && mCurrentRound == mNumRounds - 1;
}

bool DraftSession::runFullDraft()
{
    if (mSeats.empty())
        return false;

    for (int round = 0; round < mNumRounds; round++)
    {
        if (!beginRound(round))
            return false;

        do
        {
            resolveBotPicksForStep();
            if (!allSeatsPickedThisStep())
                return false; // a non-bot seat never got a pick submitted
            advanceStep();
        } while (!isRoundComplete());
    }

    return true;
}

MTGCard* DraftDeckBuilder::getBasicLand(MTGAllCards* database, int mtgColor)
{
    switch (mtgColor)
    {
        case Constants::MTG_COLOR_GREEN:
            return database->getCardByName("Forest");
        case Constants::MTG_COLOR_BLUE:
            return database->getCardByName("Island");
        case Constants::MTG_COLOR_RED:
            return database->getCardByName("Mountain");
        case Constants::MTG_COLOR_BLACK:
            return database->getCardByName("Swamp");
        case Constants::MTG_COLOR_WHITE:
            return database->getCardByName("Plains");
        default:
            return NULL;
    }
}

namespace
{
struct DraftDeckCandidate
{
    MTGCard* card;
    float score;
};

struct DraftDeckCandidateScoreDesc
{
    bool operator()(const DraftDeckCandidate& a, const DraftDeckCandidate& b) const
    {
        return a.score > b.score;
    }
};
}

MTGDeck* DraftDeckBuilder::buildDeck(DraftSeat* seat, MTGAllCards* database, int deckSize, int numLands)
{
    MTGDeck* result = NEW MTGDeck(database);
    if (!seat || !seat->getPool())
        return result;

    int first, second;
    seat->getTopColors(first, second);

    vector<DraftDeckCandidate> candidates;
    MTGDeck* pool = seat->getPool();
    for (map<int, int>::iterator it = pool->cards.begin(); it != pool->cards.end(); ++it)
    {
        MTGCard* card = pool->getCardById(it->first);
        if (!card || !card->data || card->data->isLand())
            continue;

        bool colorless = true;
        for (int c = Constants::MTG_COLOR_GREEN; c <= Constants::MTG_COLOR_WHITE; c++)
        {
            if (card->data->hasColor(c))
            {
                colorless = false;
                break;
            }
        }
        bool onColor = colorless || (first >= 0 && card->data->hasColor(first)) || (second >= 0 && card->data->hasColor(second));
        if (!onColor)
            continue;

        for (int copy = 0; copy < it->second; copy++)
        {
            DraftDeckCandidate c;
            c.card = card;
            c.score = BotDraftPicker::scoreCard(card, *seat);
            candidates.push_back(c);
        }
    }

    std::sort(candidates.begin(), candidates.end(), DraftDeckCandidateScoreDesc());

    int numSpells = deckSize - numLands;
    int keep = (std::min)((int) candidates.size(), numSpells);

    int weight[Constants::MTG_NB_COLORS];
    for (int c = 0; c < Constants::MTG_NB_COLORS; c++)
        weight[c] = 0;

    for (int i = 0; i < keep; i++)
    {
        MTGCard* card = candidates[i].card;
        result->add(card);
        ManaCost* mc = card->data->getManaCost();
        if (mc)
        {
            for (int c = Constants::MTG_COLOR_GREEN; c <= Constants::MTG_COLOR_WHITE; c++)
                weight[c] += mc->getCost(c);
        }
    }

    int firstWeight = (first >= 0) ? weight[first] : 0;
    int secondWeight = (second >= 0) ? weight[second] : 0;
    int totalWeight = firstWeight + secondWeight;

    int firstLands, secondLands;
    if (second < 0 || totalWeight <= 0)
    {
        firstLands = numLands;
        secondLands = 0;
    }
    else
    {
        firstLands = (int) ((float) firstWeight / (float) totalWeight * numLands + 0.5f);
        firstLands = (std::max)(0, (std::min)(numLands, firstLands));
        secondLands = numLands - firstLands;
    }

    MTGCard* firstBasic = (first >= 0) ? getBasicLand(database, first) : NULL;
    MTGCard* secondBasic = (second >= 0) ? getBasicLand(database, second) : NULL;

    if (firstBasic)
        for (int i = 0; i < firstLands; i++)
            result->add(firstBasic);
    if (secondBasic)
        for (int i = 0; i < secondLands; i++)
            result->add(secondBasic);

    return result;
}

#ifdef TESTSUITE
bool runDraftEngineSmokeTest()
{
    MTGPack pack;
    pack.load("packs/ecl_draft_booster.txt");
    if (!pack.isValid())
    {
        // The WSL console test harness runs with cwd=projects/mtg/bin, one level
        // above Res/, so TiXmlDocument's raw fopen() misses the resource-relative
        // path that the shipped game (and MTGPacks::loadAll()) resolves correctly.
        // Real gameplay never hits this fallback; it's here only so the smoke
        // test runs the same way under the harness as it will in the shipped game.
        pack.load("Res/packs/ecl_draft_booster.txt");
    }
    if (!pack.isValid())
    {
        DebugTrace("[DraftSmokeTest] FAILED: ecl_draft_booster.txt did not load from either path");
        return false;
    }

    const int kNumSeats = 8;
    const int kNumRounds = 3;
    const int kCardsPerPack = 14; // 1 rare/mythic + 3 uncommon + 10 common; basics are added at deck-build time, not drafted

    DraftSession session(kNumSeats, MTGCollection(), kNumRounds, kCardsPerPack);
    session.setPackTemplate(&pack);

    if (!session.runFullDraft())
    {
        DebugTrace("[DraftSmokeTest] FAILED: runFullDraft() returned false");
        return false;
    }

    bool ok = true;
    int expectedPicks = kNumRounds * kCardsPerPack;
    for (int i = 0; i < kNumSeats; i++)
    {
        DraftSeat* seat = session.getSeat(i);
        if (!seat || seat->getTotalPicks() != expectedPicks)
        {
            DebugTrace("[DraftSmokeTest] FAILED: seat " << i << " ended with " << (seat ? seat->getTotalPicks() : -1)
                    << " picks, expected " << expectedPicks);
            ok = false;
            continue;
        }
        if (seat->getPool()->totalCards() != expectedPicks)
        {
            DebugTrace("[DraftSmokeTest] FAILED: seat " << i << " pool has " << seat->getPool()->totalCards()
                    << " cards, expected " << expectedPicks);
            ok = false;
            continue;
        }
        int first, second;
        seat->getTopColors(first, second);
        DebugTrace(
                "[DraftSmokeTest] seat " << i << ": " << seat->getTotalPicks() << " picks, top colors " << first
                        << "(" << seat->getColorPickCount(first) << ") / " << second << "("
                        << seat->getColorPickCount(second) << ")");

        MTGDeck* deck = DraftDeckBuilder::buildDeck(seat, MTGCollection());
        int deckSize = deck ? deck->totalCards() : -1;
        if (!deck || deckSize < 30 || deckSize > 40)
        {
            DebugTrace("[DraftSmokeTest] FAILED: seat " << i << " built deck has " << deckSize << " cards, expected 30-40");
            ok = false;
        }
        else
        {
            DebugTrace("[DraftSmokeTest] seat " << i << " built deck: " << deckSize << " cards");
        }
        SAFE_DELETE(deck);
    }

    if (ok)
        DebugTrace("[DraftSmokeTest] PASSED: " << kNumSeats << " seats each drafted " << expectedPicks
                << " cards across " << kNumRounds << " rounds");

    return ok;
}
#endif
