#include "PrecompiledHeader.h"

#include "MTGRules.h"
#include "CardSelector.h"
#include "GuiCombat.h"
#include "GuiBackground.h"
#include "GuiFrame.h"
#include "GuiPhaseBar.h"
#include "GuiAvatars.h"
#include "GuiHand.h"
#include "GuiPlay.h"
#include "GuiMana.h"
#include "GuiStatic.h"
#include "Trash.h"
#include "DuelLayers.h"
#include "MTGDeck.h"
#include "WResourceManager.h"
#include "GameApp.h"
#include "GameOptions.h"
#include <ctime>
#include <cstring>

void DuelLayers::CheckUserInput(int isAI)
{
    JButton key;
    int x, y;
    JGE* jge = observer->getInput();
    if(!jge) return;

    while ((key = jge->ReadButton()) || jge->GetLeftClickCoordinates(x, y))
    {
        if ((!isAI) && ((0 != key) ||  jge->GetLeftClickCoordinates(x, y)))
        {
            if (key == JGE_BTN_TAGBUG || key == JGE_BTN_VERIFY || key == JGE_BTN_PARTIAL) {
                RecordCardStatus(key == JGE_BTN_VERIFY ? "VERIFIED"
                                 : key == JGE_BTN_PARTIAL ? "PARTIAL" : "BROKEN");
                jge->LeftClickedProcessed();
                break;
            }
            if (stack->CheckUserInput(key)) {
                jge->LeftClickedProcessed();
                break;
            }
            if (combat->CheckUserInput(key)) {
                jge->LeftClickedProcessed();
                break;
            }
            if (avatars->CheckUserInput(key)) {
                jge->LeftClickedProcessed();
                break; //avatars need to check their input before action (CTRL_CROSS)
            }
            if (action->CheckUserInput(key)) {
                jge->LeftClickedProcessed();
                break;
            }
            if (hand->CheckUserInput(key)) {
                jge->LeftClickedProcessed();
                break;
            }
            if (mCardSelector->CheckUserInput(key)) {
                jge->LeftClickedProcessed();
                break;
            }
        }
        jge->LeftClickedProcessed();
    }
}

// Record a human verification status for the currently-selected card, from the
// in-duel hotkeys: T=BROKEN, V=VERIFIED, P=PARTIAL. A specific card (hand,
// battlefield, or the highlighted card in an opened zone pile) is appended to
// card_status.tsv, which the audit worklist (projects/mtg/audits/) reads.
// BROKEN additionally writes the rich, human-readable block to bugreports.txt
// (and may flag a whole zone pile, so the key is never a silent no-op).
void DuelLayers::RecordCardStatus(const char* status)
{
    const bool broken = (strcmp(status, "BROKEN") == 0);

    MTGCardInstance* card = NULL;
    string pileDesc;

    // If a zone pile (graveyard/exile/library/command zone/sideboard) is open for
    // browsing, use the specific card highlighted in it. OpenedDisplay is set by
    // GuiGameZone::toggleDisplay while a pile browser is up; its highlighted item
    // is mObjects[mCurr] (a CardView).
    if (CardDisplay* disp = observer->OpenedDisplay)
    {
        if (disp->mCurr >= 0 && disp->mCurr < (int) disp->mObjects.size())
            if (CardGui* cg = dynamic_cast<CardGui*>(disp->mObjects[disp->mCurr]))
                card = cg->card;
    }

    // Otherwise the card under the selection cursor (hand/battlefield), or the
    // pile itself when the cursor is on a closed zone pile.
    if (!card)
    {
        PlayGuiObject* sel = mCardSelector ? mCardSelector->getActiveObject() : NULL;
        if (CardGui* cg = dynamic_cast<CardGui*>(sel))
            card = cg->card;
        else if (GuiGameZone* gz = dynamic_cast<GuiGameZone*>(sel))
        {
            if (gz->zone)
            {
                char buf[128];
                sprintf(buf, "%s (%d cards)", gz->zone->getName(), gz->zone->nb_cards);
                pileDesc = buf;
            }
        }
    }

    if (!card && pileDesc.empty())
    {
        mTagMessage = "Nothing selected";
        mTagMessageTimer = 2.0f;
        return;
    }
    // VERIFIED / PARTIAL apply to a specific card, not a whole pile.
    if (!card && !broken)
    {
        mTagMessage = "Select a card, not a pile";
        mTagMessageTimer = 2.0f;
        return;
    }

    // Debounce: skip a repeat of the same card+status while its toast is still up.
    if (card && card == mLastTagged && mLastStatus == status && mTagMessageTimer > 0.0f)
        return;

    // shared context strings
    char ctx[96] = "", pt[48] = "";
    sprintf(ctx, "turn %d %s", observer->turn,
            observer->getCurrentGamePhaseName().c_str());
    if (card)
        sprintf(pt, "%d/%d (printed %d/%d)", card->getCurrentPower(),
                card->getCurrentToughness(), card->getPower(), card->getToughness());

    // --- record the result mapped to Wagic's grade vocabulary in the deduped
    //     card_grades.tsv (one row per card). Also updates the live badge store.
    //     V=Supported, P=Borderline, T(broken)=Crappy.
    if (card)
    {
        int grade = broken ? Constants::GRADE_CRAPPY
                  : (strcmp(status, "VERIFIED") == 0 ? Constants::GRADE_SUPPORTED
                                                     : Constants::GRADE_BORDERLINE);
        CardStatusStore::set(card->getName(), grade);
    }

    // --- bugreports.txt: rich block, BROKEN only (preserves the bug-report flow)
    if (broken)
    {
        std::ofstream file;
        if (JFileSystem::GetInstance()->openForWrite(file, "bugreports.txt", ios_base::app))
        {
            file << "==== BUG FLAG ====" << std::endl;
            file << ctx << std::endl;
            if (card)
            {
                int ctrl = -1;
                for (int i = 0; i < observer->getPlayersNumber(); ++i)
                    if (observer->getPlayer(i) == card->controller()) ctrl = i;
                file << "card: " << card->getName() << " [id " << card->getId()
                     << ", set " << setlist[card->setId] << "]" << std::endl;
                file << "zone: " << (card->getCurrentZone() ? card->getCurrentZone()->getName() : "?")
                     << ", controller: player " << ctrl << std::endl;
                file << "power/toughness: " << pt << std::endl;
                file << "tapped: " << (card->isTapped() ? "yes" : "no") << std::endl;
            }
            else
                file << "zone pile: " << pileDesc << std::endl;
            file << std::endl;
            file.close();
        }
    }

    // --- on-screen confirmation
    const char* label = broken ? "Broken -> Crappy"
                        : (strcmp(status, "VERIFIED") == 0 ? "Verified -> Supported"
                                                           : "Partial -> Borderline");
    if (card)
        mTagMessage = string(label) + ": " + card->getName();
    else
        mTagMessage = string(label) + " pile: " + pileDesc;
    mLastTagged = card;
    mLastStatus = status;
    mTagMessageTimer = 2.5f;
}

void DuelLayers::Update(float dt, Player * currentPlayer)
{
    for (int i = 0; i < nbitems; ++i)
        objects[i]->Update(dt);

    if (mTagMessageTimer > 0.0f)
        mTagMessageTimer -= dt;

    int isAI = currentPlayer->isAI() || currentPlayer != getObserver()->players[mPlayerViewIndex]; // Fix for 2 players hand.
    if (isAI && !currentPlayer->getObserver()->isLoading())
        currentPlayer->Act(dt);

    CheckUserInput(isAI);
}

ActionStack * DuelLayers::stackLayer()
{
    return stack;
}

GuiCombat * DuelLayers::combatLayer()
{
    return combat;
}

ActionLayer * DuelLayers::actionLayer()
{
    return action;
}

GuiAvatars * DuelLayers::GetAvatars()
{
    return avatars;
}

DuelLayers::DuelLayers(GameObserver* go, int playerViewIndex) :
    nbitems(0), mPlayerViewIndex(playerViewIndex), mTagMessageTimer(0.0f), mLastTagged(NULL)
{
    observer = go;
    observer->mLayers = this;

    // Bind 'T' to the bug-flag button at every duel start. Required because the
    // game loads saved keybindings at startup (GameOptionKeyBindings::read calls
    // ClearBindings() then re-applies only the saved pairs), which wipes any JGE
    // default binding the user hasn't saved — so binding 'T' only in SDLmain's
    // defaults is not enough. Re-binding here, after options are loaded and once
    // per duel, guarantees it works. Unbind first so we never stack duplicates.
    // SDLK_t == 't' == 116 on the SDL/Windows build.
    if (JGE* je = observer->getInput())
    {
        je->UnbindKey((LocalKeySym) 't'); JGE::BindKey((LocalKeySym) 't', JGE_BTN_TAGBUG);
        je->UnbindKey((LocalKeySym) 'v'); JGE::BindKey((LocalKeySym) 'v', JGE_BTN_VERIFY);
        je->UnbindKey((LocalKeySym) 'p'); JGE::BindKey((LocalKeySym) 'p', JGE_BTN_PARTIAL);
    }
    CardStatusStore::reload();   // load card_status.tsv for the in-duel badges

    mCardSelector = NEW CardSelector(go, this);
    //1 Action Layer
    action = NEW ActionLayer(go);
    action->Add(phaseHandler = NEW MTGGamePhase(go, action->getMaxId())); //Phases handler
    action->Add(NEW OtherAbilitiesEventReceiver(go, -1)); //autohand, etc... handler
    //Other display elements
    action->Add(NEW HUDDisplay(go, -1));

    Add(NEW GuiMana(20, 20, getRenderedPlayerOpponent()));
    Add(NEW GuiMana(440, 20, getRenderedPlayer()));
    Add(stack = NEW ActionStack(go));
    Add(combat = NEW GuiCombat(go));
    Add(action);
    Add(mCardSelector);
    Add(hand = NEW GuiHandSelf(go, getRenderedPlayer()->game->hand));
    Add(avatars = NEW GuiAvatars(this));
    Add(NEW GuiHandOpponent(go, getRenderedPlayerOpponent()->game->hand));
    Add(NEW GuiPlay(this));
    Add(NEW GuiPhaseBar(this));
    Add(NEW GuiFrame(go));
    Add(NEW GuiBackground(go));
}

DuelLayers::~DuelLayers()
{
    int _nbitems = nbitems;
    nbitems = 0;
    for (int i = 0; i < _nbitems; ++i)
    {
        if (objects[i] != mCardSelector)
        {
            SAFE_DELETE(objects[i]);
            objects[i] = NULL;
        }
    }

    for (size_t i = 0; i < waiters.size(); ++i)
        delete (waiters[i]);
    observer->mTrash->cleanup();

    SAFE_DELETE(mCardSelector);
}

void DuelLayers::Add(GuiLayer * layer)
{
    objects.push_back(layer);
    nbitems++;
}

void DuelLayers::Remove()
{
    --nbitems;
}

void DuelLayers::Render()
{
    bool focusMakesItThrough = true;
    for (int i = 0; i < nbitems; ++i)
    {
        objects[i]->hasFocus = focusMakesItThrough;
        if (objects[i]->modal)
            focusMakesItThrough = false;
    }
    for (int i = nbitems - 1; i >= 0; --i)
        objects[i]->Render();

    // Transient confirmation for the bug-flag hotkey, drawn on top of everything.
    if (mTagMessageTimer > 0.0f && !mTagMessage.empty())
    {
        WFont * font = WResourceManager::Instance()->GetWFont(Fonts::MAIN_FONT);
        if (font)
        {
            float x = SCREEN_WIDTH / 2;
            float y = 8;
            font->SetScale(1.0f);
            // colour by status: green=verified, amber=partial, red=broken, else yellow
            PIXEL_TYPE col = ARGB(255, 255, 220, 60);
            if (mLastStatus == "VERIFIED")     col = ARGB(255, 90, 220, 90);
            else if (mLastStatus == "PARTIAL") col = ARGB(255, 255, 170, 40);
            else if (mLastStatus == "BROKEN")  col = ARGB(255, 255, 80, 80);
            font->SetColor(ARGB(255, 0, 0, 0));
            font->DrawString(mTagMessage.c_str(), x + 1, y + 1, JGETEXT_CENTER);
            font->SetColor(col);
            font->DrawString(mTagMessage.c_str(), x, y, JGETEXT_CENTER);
            font->SetColor(ARGB(255, 255, 255, 255));
        }
    }
}

int DuelLayers::receiveEvent(WEvent * e)
{

#if 0
#define PRINT_IF(type) { type *foo = dynamic_cast<type*>(e); if (foo) cout << "Is a " #type " " << *foo << endl; }
    cout << "Received event " << e << " ";
    PRINT_IF(WEventZoneChange);
    PRINT_IF(WEventDamage);
    PRINT_IF(WEventPhaseChange);
    PRINT_IF(WEventCardUpdate);
    PRINT_IF(WEventCardTap);
    PRINT_IF(WEventCreatureAttacker);
    PRINT_IF(WEventCreatureBlocker);
    PRINT_IF(WEventCreatureBlockerRank);
    PRINT_IF(WEventCombatStepChange);
    PRINT_IF(WEventEngageMana);
    PRINT_IF(WEventConsumeMana);
    PRINT_IF(WEventEmptyManaPool);
#endif

    int used = 0;
    for (int i = 0; i < nbitems; ++i)
        used |= objects[i]->receiveEventPlus(e);
    if (!used)
    {
        Pos* p;
        if (WEventZoneChange *event = dynamic_cast<WEventZoneChange*>(e))
        {
            MTGCardInstance* card = event->card;
            if (card->view)
                waiters.push_back(p = NEW Pos(*(card->view)));
            else
                waiters.push_back(p = NEW Pos(0, 0, 0, 0, 255));
            const Pos* ref = card->view;
            while (card)
            {
                if (ref == card->view)
                    card->view = p;
                card = card->next;
            }
        }
    }
    for (int i = 0; i < nbitems; ++i)
        objects[i]->receiveEventMinus(e);

    if (WEventPhaseChange *event = dynamic_cast<WEventPhaseChange*>(e))
        if (MTG_PHASE_BEFORE_BEGIN == event->to->id)
            observer->mTrash->cleanup();

    return 1;
}

float DuelLayers::RightBoundary()
{
    return MIN (hand->LeftBoundary(), avatars->LeftBoundarySelf());
}

Player* DuelLayers::getRenderedPlayer()
{
    return observer->players[mPlayerViewIndex]; 
};

Player* DuelLayers::getRenderedPlayerOpponent()
{ 
    return observer->players[mPlayerViewIndex]->opponent(); 
};
