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
        score += std::min(weight, 20) * 0.5f;
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
    mNumRounds(numRounds), mCardsPerPack(cardsPerPack), mPackTemplate(NULL)
{
    mSeats.resize(numSeats, NULL);
    mPickers.resize(numSeats, (DraftPicker*) NULL);
    for (int i = 0; i < numSeats; i++)
        mSeats[i] = NEW DraftSeat(i, true, database);
}

DraftSession::~DraftSession()
{
    for (size_t i = 0; i < mSeats.size(); i++)
        SAFE_DELETE(mSeats[i]);
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

bool DraftSession::runFullDraft()
{
    if (!mPackTemplate || mSeats.empty())
        return false;

    int n = (int) mSeats.size();

    for (int round = 0; round < mNumRounds; round++)
    {
        vector<MTGDeck*> packs(n);
        for (int i = 0; i < n; i++)
        {
            packs[i] = NEW MTGDeck(mSeats[i]->getPool()->database);
            mPackTemplate->assemblePack(packs[i]);
        }

        int direction = (round % 2 == 0) ? 1 : -1;

        for (int pickNum = 0; pickNum < mCardsPerPack; pickNum++)
        {
            for (int i = 0; i < n; i++)
            {
                MTGDeck* currentPack = packs[i];
                if (currentPack->totalCards() <= 0)
                    continue;

                DraftPicker* picker = mPickers[i] ? mPickers[i] : (DraftPicker*) &mDefaultBotPicker;
                MTGCard* chosen = picker->pick(*mSeats[i], *currentPack);
                if (!chosen)
                    continue;

                currentPack->remove(chosen);
                mSeats[i]->recordPick(chosen);
            }

            if (direction > 0)
                std::rotate(packs.begin(), packs.begin() + (n - 1), packs.end());
            else
                std::rotate(packs.begin(), packs.begin() + 1, packs.end());
        }

        for (int i = 0; i < n; i++)
            SAFE_DELETE(packs[i]);
    }

    return true;
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
    }

    if (ok)
        DebugTrace("[DraftSmokeTest] PASSED: " << kNumSeats << " seats each drafted " << expectedPicks
                << " cards across " << kNumRounds << " rounds");

    return ok;
}
#endif
