#ifndef _MANACOST_H_
#define _MANACOST_H_

#include "utils.h"
#include "MTGDefinitions.h"
#include "ObjectAnalytics.h"

class ManaCostHybrid;
class ExtraCosts;
class ExtraCost;
class MTGAbility;
class MTGCardInstance;
class Player;

class ManaCost
#ifdef TRACK_OBJECT_USAGE
    : public InstanceCounter<ManaCost>
#endif
{

    friend std::ostream& operator<<(std::ostream& out, ManaCost& m);
    friend std::ostream& operator<<(std::ostream& out, ManaCost* m);
    friend std::ostream& operator<<(std::ostream& out, ManaCost m);
    
protected:
    std::vector<int16_t> cost;
    std::vector<ManaCostHybrid> hybrids;

    virtual void init();
    ManaCost * suspend;
    ManaCost * manaUsedToCast;
    ManaCost * morph;
    ManaCost * Retrace;
    ManaCost * Bestow;
    ManaCost * FlashBack;
    ManaCost * BuyBack;
    ManaCost * kicker;
    ManaCost * alternative;

public:
    enum
    {
        MANA_UNPAID = 0,
        MANA_PAID = 1,
        MANA_PAID_WITH_KICKER = 2,
        MANA_PAID_WITH_ALTERNATIVE = 3,
        MANA_PAID_WITH_BUYBACK = 4,
        MANA_PAID_WITH_FLASHBACK = 5,
        MANA_PAID_WITH_RETRACE = 6,
        MANA_PAID_WITH_MORPH = 7,
        MANA_PAID_WITH_SUSPEND = 8,
        MANA_PAID_WITH_OVERLOAD = 9,
        MANA_PAID_WITH_BESTOW = 10,
        MANA_PAID_WITH_OTHERCOST = 11
    };
    ExtraCosts * extraCosts;

    ManaCost * getAlternative(){ return alternative; };
    void setAlternative(ManaCost * aMana){ SAFE_DELETE(alternative); alternative = aMana;};

    ManaCost * getKicker(){ return kicker; };
    void setKicker(ManaCost * aMana){ SAFE_DELETE(kicker); kicker = aMana;};

    ManaCost * getBuyback(){ return BuyBack; };
    void setBuyback(ManaCost * aMana){ SAFE_DELETE(BuyBack); BuyBack = aMana;};

    ManaCost * getFlashback(){ return FlashBack; };
    void setFlashback(ManaCost * aMana){ SAFE_DELETE(FlashBack); FlashBack = aMana;};

    ManaCost * getRetrace(){ return Retrace; };
    void setRetrace(ManaCost * aMana){ SAFE_DELETE(Retrace); Retrace = aMana;};

    ManaCost * getMorph(){ return morph; };
    void setMorph(ManaCost * aMana){ SAFE_DELETE(morph); morph = aMana;};

    ManaCost * getSuspend(){ return suspend; };
    void setSuspend(ManaCost * aMana){ SAFE_DELETE(suspend); suspend = aMana;};

    ManaCost * getBestow() { return Bestow; };
    void setBestow(ManaCost * aMana) { SAFE_DELETE(Bestow); Bestow = aMana; };

    ManaCost * getManaUsedToCast(){ return manaUsedToCast; };
    void setManaUsedToCast(ManaCost * aMana){ SAFE_DELETE(manaUsedToCast); manaUsedToCast = aMana;};

    string alternativeName;
    bool isMulti;
    static ManaCost * parseManaCost(string value, ManaCost * _manacost = NULL, MTGCardInstance * c = NULL);
    static int parseManaSymbol(char symbol);

    virtual void resetCosts();
    void x();
    int hasX();
    void specificX(int color = 0);
    int hasSpecificX();
    int xColor;
    int hasAnotherCost();
    ManaCost(std::vector<int16_t>& _cost, int nb_elems = 1);
    ManaCost();
    virtual ~ManaCost();
    ManaCost(ManaCost * _manaCost);
    ManaCost(const ManaCost& manaCost);
    ManaCost& operator= (const ManaCost& manaCost);
    void copy(ManaCost * _manaCost);
    void changeCostTo(ManaCost * _manaCost);
    int isNull();
    int getConvertedCost();
    string toString();
    int getCost(int color);
    int getManaSymbols(int color);
    int getManaSymbolsHybridMerged(int color);
    int countHybridsNoPhyrexian();
    void removeHybrid(ManaCost * _cost);

    //Returns NULL if i is greater than nbhybrids
    ManaCostHybrid * getHybridCost(unsigned int i);
    int hasColor(int color);
    int remove(int color, int value);
    int add(int color, int value);

    //
    // Extra Costs (sacrifice,counters...)
    //
    int addExtraCost(ExtraCost * _cost);
    int addExtraCosts(ExtraCosts *_cost);
    int setExtraCostsAction(MTGAbility * action, MTGCardInstance * card);
    int isExtraPaymentSet();
    int canPayExtra();
    int doPayExtra();
    ExtraCost * getExtraCost(unsigned int i);

    int addHybrid(int c1, int v1, int c2, int v2);
    int tryToPayHybrids(const std::vector<ManaCostHybrid> &_hybrids, int _nbhybrids, std::vector<int16_t>& diff);
    void randomDiffHybrids(ManaCost * _cost, std::vector<int16_t>& diff);
    int add(ManaCost * _cost);
    int remove(ManaCost * _cost);
    int removeAll(int color);
    int pay (ManaCost * _cost);

    //return 1 if _cost can be paid with current data, 0 otherwise
    int canAfford(ManaCost * _cost, int anytypeofmana);

    int isPositive();
    ManaCost * Diff(ManaCost * _cost);
#ifdef WIN32
    void Dump();
#endif


};

//Mana in a pool that may only be spent on some things ("Spend this mana only to cast a creature spell",
//"...only to activate abilities", "can't be spent to cast spells from your hand"). A tag holds how much of one
//colour is restricted and what it accepts; untagged mana in the pool is free. See ManaPool::accepts().
struct ManaTag
{
    int color;            //pool colour (colorless is MTG_COLOR_WASTE)
    int amount;
    string spells;        //target filter a SPELL must match to use it ("" = no spells)
    string abilities;     //target filter an ability's SOURCE must match ("" = no abilities)
    bool notFromHand;     //spells cast from hand can't use it (Heartwood Crafter)
};

class ManaPool:public ManaCost{
protected:
    Player * player;
public:
    vector<ManaTag> tags;
    MTGCardInstance * spender;   //who the next pay() is for - set just before paying, cleared by pay()
    bool spenderIsSpell;
    void addTagged(int color, int amount, string spells, string abilities, bool notFromHand);
    bool accepts(const ManaTag & tag, MTGCardInstance * card, bool spell);
    //Copy of `pool` without the tagged mana that `card` (a spell, or an ability's source) may not spend.
    //`pool` is usually this pool or a snapshot of it; the caller deletes the result.
    ManaCost * spendableFor(ManaCost * pool, MTGCardInstance * card, bool spell);
    void setSpender(MTGCardInstance * card, bool spell);
    void reconcileTags(int * before);
    void Empty();
    ManaPool(Player * player);
    ManaPool(ManaCost * _manaCost, Player * player);
    int remove (int color, int value);
    int add(int color, int value, MTGCardInstance * source = NULL, bool extra = false);
    int add(ManaCost * _cost, MTGCardInstance * source = NULL);
    int pay (ManaCost * _cost);
};

#endif
