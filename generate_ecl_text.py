"""
Generate text= fields for ECL card primitives that are missing them.
Translates auto= Wagic syntax into human-readable card text.
"""
import re

# ── helpers ──────────────────────────────────────────────────────────────────

def target_phrase(spec):
    """Convert target(...) specifiers to English."""
    # strip brackets
    inner = re.sub(r'[\[\]]', '', spec)
    parts = [p.strip() for p in inner.split('|')]
    what = parts[0] if parts else ''
    where = parts[1] if len(parts) > 1 else ''

    # qualifiers embedded in 'what'
    qty_match  = re.search(r'manacost<=(\d+)', what)
    tapped     = 'tapped' in what
    what_clean = re.sub(r'\[(.*?)\]', '', what).strip()

    noun = what_clean
    # common type rewrites
    noun = re.sub(r'^\*$', 'permanent', noun)
    noun = re.sub(r'^\*\[-land\]$', 'nonland permanent', noun)

    loc = ''
    if 'mybattlefield'        in where: loc = 'you control'
    elif 'opponentbattlefield' in where: loc = 'an opponent controls'
    elif 'mygraveyard'         in where: loc = 'in your graveyard'
    elif 'opponentgraveyard'   in where: loc = "in an opponent's graveyard"
    elif 'myhand'              in where: loc = 'in your hand'
    elif 'opponenthand'        in where: loc = "in an opponent's hand"
    elif 'opponentstack'       in where: loc = 'your opponents control on the stack'

    qualifiers = []
    if qty_match:
        qualifiers.append(f'with mana value {qty_match.group(1)} or less')
    if tapped:
        qualifiers.append('that is tapped')

    result = f'target {noun}'
    if qualifiers:
        result += ' ' + ' '.join(qualifiers)
    if loc:
        result += ' ' + loc
    return result


def token_phrase(spec):
    """Convert token(...) to English."""
    # token(Name, type string, P/T, colors)
    parts = [p.strip() for p in spec.split(',')]
    name    = parts[0] if parts else 'Token'
    types   = parts[1] if len(parts) > 1 else ''
    pt      = parts[2] if len(parts) > 2 else ''
    colors  = parts[3] if len(parts) > 3 else ''

    # clean type string
    types = re.sub(r'^creature\s*', '', types, flags=re.I).strip()
    color_map = {'white':'white','blue':'blue','black':'black','red':'red','green':'green'}
    color_words = [c for c in colors.split() if c.lower() in color_map]
    color_str = ' '.join(color_words) + ' ' if color_words else ''

    return f'Create a {pt} {color_str}{name} creature token with the {types} subtype'


def translate_auto(auto, card_name='it', card_type=''):
    """Best-effort translation of a Wagic auto= line to card text."""
    s = auto.strip()

    # ── triggered / static prefix ───────────────────────────────────────────
    trigger = ''
    if s.startswith('@movedTo(this|mybattlefield):'):
        trigger = 'When ~ enters the battlefield, '
        s = s[len('@movedTo(this|mybattlefield):'): ]
    elif s.startswith('@movedTo(this|opponentbattlefield):'):
        trigger = 'When ~ enters the battlefield under an opponent\'s control, '
        s = s[len('@movedTo(this|opponentbattlefield):'): ]
    elif s.startswith('@each my endstep:'):
        trigger = 'At the beginning of your end step, '
        s = s[len('@each my endstep:'):]
    elif s.startswith('@each my upkeep:'):
        trigger = 'At the beginning of your upkeep, '
        s = s[len('@each my upkeep:'):]
    elif s.startswith('@each my combatbegin:'):
        trigger = 'At the beginning of combat on your turn, '
        s = s[len('@each my combatbegin:'):]
    elif s.startswith('@each opponent upkeep:'):
        trigger = "At the beginning of each opponent's upkeep, "
        s = s[len('@each opponent upkeep:'):]
    elif s.startswith('_ATTACKING_:'):
        trigger = 'Whenever ~ attacks, '
        s = s[len('_ATTACKING_:'):]
    elif s.startswith('_BLOCKING_:'):
        trigger = 'Whenever ~ blocks, '
        s = s[len('_BLOCKING_:'):]
    elif s.startswith('_BLOCKED_:'):
        trigger = 'Whenever ~ becomes blocked, '
        s = s[len('_BLOCKED_:'):]

    # ── static keywords (no trigger) ────────────────────────────────────────
    keyword_map = {
        '_WARD2_':          'Ward {2}',
        '_WARD1_':          'Ward {1}',
        '_WARD3_':          'Ward {3}',
        '_FLYING_':         'Flying',
        '_HASTE_':          'Haste',
        '_VIGILANCE_':      'Vigilance',
        '_TRAMPLE_':        'Trample',
        '_LIFELINK_':       'Lifelink',
        '_DEATHTOUCH_':     'Deathtouch',
        '_MENACE_':         'Menace',
        '_REACH_':          'Reach',
        '_FIRSTSTR_':       'First strike',
        '_DOUBLESTRIKE_':   'Double strike',
        '_HEXPROOF_':       'Hexproof',
        '_INDESTRUCTIBLE_': 'Indestructible',
        '_FLASH_':          'Flash',
        '_DEFENDER_':       'Defender',
    }

    for kw, text in keyword_map.items():
        if s.strip() == kw:
            return text

    # ── enchant static bonus ─────────────────────────────────────────────────
    enchant_m = re.match(r'^enchanted\s+([+-]?\d+)/([+-]?\d+)$', s.strip())
    if enchant_m:
        p, t = enchant_m.group(1), enchant_m.group(2)
        sign_p = '+' if not p.startswith('-') else ''
        sign_t = '+' if not t.startswith('-') else ''
        return f'Enchanted creature gets {sign_p}{p}/{sign_t}{t}.'

    # ── choice ───────────────────────────────────────────────────────────────
    choice_m = re.match(r'^choice\s+(.+)', s, re.I | re.DOTALL)
    if choice_m:
        rest = choice_m.group(1)
        options = re.findall(r'name\(([^)]+)\)', rest)
        if options:
            bullets = ';\n• '.join(o.capitalize() for o in options)
            return f'Choose one —\n• {bullets}.'

    # ── split on && for multi-part effects ───────────────────────────────────
    parts = [p.strip() for p in s.split('&&')]
    clauses = []

    for part in parts:
        clauses.append(_translate_part(part, card_name))

    result = ' '.join(c for c in clauses if c)
    if trigger:
        result = trigger + result[0].lower() + result[1:] if result else trigger.rstrip(', ') + '.'
    if result and not result.endswith('.'):
        result += '.'
    return result if result else auto  # fallback: raw auto


def _translate_part(part, card_name):
    part = part.strip()
    if not part:
        return ''

    # Keyword suffixes
    kw_suffix = {
        'hexproof ueot':        '~ gains hexproof until end of turn',
        'indestructible ueot':  '~ gains indestructible until end of turn',
        'trample ueot':         '~ gains trample until end of turn',
        'first strike ueot':    '~ gains first strike until end of turn',
        'double strike ueot':   '~ gains double strike until end of turn',
        'lifelink ueot':        '~ gains lifelink until end of turn',
        'deathtouch ueot':      '~ gains deathtouch until end of turn',
        'menace ueot':          '~ gains menace until end of turn',
        'flying ueot':          '~ gains flying until end of turn',
        'haste ueot':           '~ gains haste until end of turn',
        'vigilance ueot':       '~ gains vigilance until end of turn',
        'reach ueot':           '~ gains reach until end of turn',
    }
    for kw, repl in kw_suffix.items():
        if part == kw:
            return repl.replace('~', card_name)
        if part.startswith(kw + ' ') or part.endswith(' ' + kw):
            pass  # handled below

    # pump(+X/+Y) target(...) [ueot]
    pump_m = re.match(r'^pump\(([+-]?\d+)/([+-]?\d+)\)\s+(target\([^)]+\))(\s+ueot)?', part)
    if pump_m:
        p, t = pump_m.group(1), pump_m.group(2)
        sign_p = '+' if not p.startswith('-') else ''
        sign_t = '+' if not t.startswith('-') else ''
        tgt = target_phrase(pump_m.group(3)[7:-1])
        ueot = ' until end of turn' if pump_m.group(4) else ''
        return f'{tgt.capitalize()} gets {sign_p}{p}/{sign_t}{t}{ueot}'

    # pump self ueot  (no explicit target = self)
    pump_self_m = re.match(r'^pump\(([+-]?\d+)/([+-]?\d+)\)(\s+ueot)?$', part)
    if pump_self_m:
        p, t = pump_self_m.group(1), pump_self_m.group(2)
        sign_p = '+' if not p.startswith('-') else ''
        sign_t = '+' if not t.startswith('-') else ''
        ueot = ' until end of turn' if pump_self_m.group(3) else ''
        return f'~ gets {sign_p}{p}/{sign_t}{t}{ueot}'.replace('~', card_name)

    # damage:N target(...)
    dmg_tgt_m = re.match(r'^damage:(\d+)\s+(target\([^)]+\))', part)
    if dmg_tgt_m:
        n   = dmg_tgt_m.group(1)
        tgt = target_phrase(dmg_tgt_m.group(2)[7:-1])
        return f'Deal {n} damage to {tgt}'

    # damage:N opponent / controller
    dmg_m = re.match(r'^damage:(\d+)\s+(opponent|controller)', part)
    if dmg_m:
        n, who = dmg_m.group(1), dmg_m.group(2)
        who_txt = 'each opponent' if who == 'opponent' else 'you'
        return f'Deal {n} damage to {who_txt}'

    # counter(-1/-1, N) target(...)
    ctr_m = re.match(r'^counter\((-?\d+)/(-?\d+),(\d+)\)\s+(target\([^)]+\))', part)
    if ctr_m:
        p, t, n = ctr_m.group(1), ctr_m.group(2), ctr_m.group(3)
        tgt = target_phrase(ctr_m.group(4)[7:-1])
        return f'Put {n} {p}/{t} counter{"s" if int(n)!=1 else ""} on {tgt}'

    # counter(+1/+1, N) target(...)
    ctrp_m = re.match(r'^counter\(\+(\d+)/\+(\d+),(\d+)\)\s+(target\([^)]+\))', part)
    if ctrp_m:
        p, t, n = ctrp_m.group(1), ctrp_m.group(2), ctrp_m.group(3)
        tgt = target_phrase(ctrp_m.group(4)[7:-1])
        return f'Put {n} +{p}/+{t} counter{"s" if int(n)!=1 else ""} on {tgt}'

    # counter(+1/+1, N) self
    ctrs_m = re.match(r'^counter\(\+(\d+)/\+(\d+),(\d+)\)$', part)
    if ctrs_m:
        p, t, n = ctrs_m.group(1), ctrs_m.group(2), ctrs_m.group(3)
        return f'Put {n} +{p}/+{t} counter{"s" if int(n)!=1 else ""} on ~'.replace('~', card_name)

    # moveto(dest) target(...)
    mv_tgt_m = re.match(r'^moveto\((\w+)\)\s+(target\([^)]+\))', part)
    if mv_tgt_m:
        dest = mv_tgt_m.group(1)
        tgt  = target_phrase(mv_tgt_m.group(2)[7:-1])
        dest_map = {
            'mybattlefield':       'the battlefield',
            'opponentbattlefield': 'the battlefield under an opponent\'s control',
            'exile':               'exile',
            'mygraveyard':         'your graveyard',
            'myhand':              'your hand',
            'bottom':              'the bottom of its owner\'s library',
        }
        dest_txt = dest_map.get(dest, dest)
        if dest == 'exile':
            return f'Exile {tgt}'
        if dest == 'mybattlefield':
            return f'Put {tgt} onto the battlefield'
        return f'Move {tgt} to {dest_txt}'

    # moveto(dest) controller/opponent (self-target)
    mv_self_m = re.match(r'^moveto\((\w+)\)\s*(controller|opponent)?$', part)
    if mv_self_m:
        dest = mv_self_m.group(1)
        dest_map = {
            'mybattlefield': 'the battlefield',
            'exile':         'exile',
            'mygraveyard':   'your graveyard',
            'myhand':        'your hand',
        }
        dest_txt = dest_map.get(dest, dest)
        return f'Put ~ onto {dest_txt}'.replace('~', card_name)

    # tap target(...)
    tap_m = re.match(r'^tap\s+(target\([^)]+\))', part)
    if tap_m:
        tgt = target_phrase(tap_m.group(1)[7:-1])
        return f'Tap {tgt}'

    # untap target(...)
    untap_m = re.match(r'^untap\s+(target\([^)]+\))', part)
    if untap_m:
        tgt = target_phrase(untap_m.group(1)[7:-1])
        return f'Untap {tgt}'

    # destroy target(...)
    dest_m = re.match(r'^destroy\s+(target\([^)]+\))', part)
    if dest_m:
        tgt = target_phrase(dest_m.group(1)[7:-1])
        return f'Destroy {tgt}'

    # draw:N controller
    draw_m = re.match(r'^draw:(\d+)\s*(?:controller)?$', part)
    if draw_m:
        n = draw_m.group(1)
        return f'Draw {n} card{"s" if int(n)!=1 else ""}'

    # life:N controller  (gain)
    life_m = re.match(r'^life:(\d+)\s*(?:controller)?$', part)
    if life_m:
        n = life_m.group(1)
        return f'You gain {n} life'

    # life:-N  (lose)
    lose_m = re.match(r'^life:-(\d+)\s*(?:controller|opponent)?$', part)
    if lose_m:
        n = lose_m.group(1)
        return f'You lose {n} life'

    # mill:N controller
    mill_m = re.match(r'^mill:(\d+)\s*(?:controller)?$', part)
    if mill_m:
        n = mill_m.group(1)
        return f'Mill {n} card{"s" if int(n)!=1 else ""}'

    # discard:N controller
    disc_m = re.match(r'^discard:(\d+)\s*(?:controller)?$', part)
    if disc_m:
        n = disc_m.group(1)
        return f'Discard {n} card{"s" if int(n)!=1 else ""}'

    # fizzle all(*|opponentstack)
    fizzle_m = re.match(r'^fizzle\s+all\(\*\|opponentstack\)', part)
    if fizzle_m:
        return "Counter all spells and abilities your opponents control on the stack"

    # fizzle target(...)
    fizzle_t = re.match(r'^fizzle\s+(target\([^)]+\))', part)
    if fizzle_t:
        tgt = target_phrase(fizzle_t.group(1)[7:-1])
        return f'Counter {tgt}'

    # fight target(...)
    fight_m = re.match(r'^fight\s+(target\([^)]+\))', part)
    if fight_m:
        tgt = target_phrase(fight_m.group(1)[7:-1])
        return f'~ fights {tgt}'.replace('~', card_name)

    # token(...)
    tok_m = re.match(r'^token\((.+)\)$', part)
    if tok_m:
        return token_phrase(tok_m.group(1))

    # hexproof ueot / indestructible ueot (inline, possibly after target)
    for kw in ('hexproof','indestructible','trample','first strike','double strike',
               'lifelink','deathtouch','menace','flying','haste','vigilance','reach'):
        kw_ueot = kw + ' ueot'
        tgt_kw_m = re.match(r'^(target\([^)]+\))\s+' + re.escape(kw_ueot), part)
        if tgt_kw_m:
            tgt = target_phrase(tgt_kw_m.group(1)[7:-1])
            return f'{tgt.capitalize()} gains {kw} until end of turn'
        tgt_kw_nm = re.match(r'^(target\([^)]+\))\s+' + re.escape(kw), part)
        if tgt_kw_nm:
            tgt = target_phrase(tgt_kw_nm.group(1)[7:-1])
            return f'{tgt.capitalize()} gains {kw}'

    # last resort: return raw part
    return part


# ── Main ──────────────────────────────────────────────────────────────────────
import re

# Load ECL primitive names
with open('M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/ECL/_cards.dat', 'rb') as f:
    content = f.read().decode('utf-8', errors='ignore')

blocks = re.findall(r'\[card\](.*?)\[/card\]', content, re.DOTALL)
ecl_primitives = set()
for block in blocks:
    m_prim = re.search(r'primitive=(.+)', block)
    if m_prim:
        prim = m_prim.group(1).strip().split(' // ')[0].strip()
        ecl_primitives.add(prim.lower())

# Find missing cards in primitives files
missing = {}  # name -> (filename, auto, type_string)

for fname in ['M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/primitives/mtg.txt',
              'M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/primitives/planeswalkers.txt']:
    with open(fname, encoding='utf-8', errors='ignore') as f:
        prim_content = f.read()

    card_blocks = re.findall(r'\[card\](.*?)\[/card\]', prim_content, re.DOTALL)
    for block in card_blocks:
        m_name = re.search(r'name=(.+)', block)
        if not m_name:
            continue
        name = m_name.group(1).strip()
        if name.lower() not in ecl_primitives:
            continue
        has_text = bool(re.search(r'^text=.+', block, re.MULTILINE))
        if not has_text:
            m_auto = re.search(r'^auto=(.+)', block, re.MULTILINE)
            m_type = re.search(r'^type=(.+)', block, re.MULTILINE)
            auto = m_auto.group(1).strip() if m_auto else ''
            card_type = m_type.group(1).strip() if m_type else ''
            missing[name] = (fname, auto, card_type)

print(f"Cards missing text=: {len(missing)}")
print()

# Generate translations
for name in sorted(missing):
    fname, auto, card_type = missing[name]
    translated = translate_auto(auto, card_name=name, card_type=card_type)
    print(f"=== {name} ===")
    print(f"  auto={auto[:120]}")
    print(f"  text={translated}")
    print()
