"""
Apply text= fields to ECL card primitives that are missing them.
Translates auto= Wagic syntax into human-readable card text,
then patches mtg.txt / planeswalkers.txt in place.
"""
import re


# ─────────────────────────── translation helpers ─────────────────────────────

def target_phrase(spec):
    """Convert a bare target specifier string (inside target(...)) to English."""
    inner = spec.strip()
    # split on | to get what|where
    pipe = inner.find('|')
    if pipe < 0:
        what, where = inner, ''
    else:
        what, where = inner[:pipe], inner[pipe+1:]

    # extract bracket filters
    filters = re.findall(r'\[([^\]]*)\]', what)
    what_clean = re.sub(r'\[.*?\]', '', what).strip()

    # map type nouns
    noun_map = {
        '*': 'permanent',
        'any': 'any target',
    }
    noun = noun_map.get(what_clean, what_clean)
    if noun == 'permanent':
        # check for negation like *[-land]
        for f in filters:
            if f.startswith('-land'):
                noun = 'nonland permanent'
                filters = [x for x in filters if x != f]
                break

    # qualifier modifiers from filters
    quals = []
    for f in filters:
        f = f.strip()
        if f.startswith('-') or f == '':
            continue
        if re.match(r'^manacost<=(\d+)$', f):
            n = re.match(r'^manacost<=(\d+)$', f).group(1)
            quals.append(f'with mana value {n} or less')
        elif re.match(r'^power<=(\d+)$', f):
            n = re.match(r'^power<=(\d+)$', f).group(1)
            quals.append(f'with power {n} or less')
        elif f == 'tapped':
            quals.append('that is tapped')
        elif f == 'flying':
            quals.append('with flying')
        elif f == 'artifact':
            noun = 'artifact or enchantment'  # common combo
        elif re.match(r'^[a-z]+$', f):
            quals.append(f'({f})')  # subtype or qualifier

    loc_map = {
        'mybattlefield':        'you control',
        'opponentbattlefield':  'an opponent controls',
        'mygraveyard':          'in your graveyard',
        'opponentgraveyard':    "in an opponent's graveyard",
        'myhand':               'in your hand',
        'opponenthand':         "in an opponent's hand",
        'opponentstack':        'on the stack',
        'combat':               'in combat',
        'mystack':              'on the stack',
    }
    loc = loc_map.get(where, where)

    result = f'target {noun}'
    if quals:
        result += ' ' + ' '.join(quals)
    if loc:
        result += ' ' + loc
    return result


def token_phrase(spec):
    parts = [p.strip() for p in spec.split(',')]
    name   = parts[0] if parts else 'Token'
    types  = parts[1] if len(parts) > 1 else ''
    pt     = parts[2] if len(parts) > 2 else ''
    colors = parts[3] if len(parts) > 3 else ''

    types = re.sub(r'^creature\s*', '', types, flags=re.I).strip()
    color_words = [c for c in colors.split()
                   if c.lower() in ('white','blue','black','red','green','colorless')]
    color_str = ' '.join(color_words) + ' ' if color_words else ''
    abilities = [c for c in colors.split()
                 if c.lower() in ('flying','haste','vigilance','trample','lifelink',
                                  'deathtouch','menace','reach','defender','hexproof')]
    ab_str = (' with ' + ', '.join(abilities)) if abilities else ''
    return f'Create a {pt} {color_str}{name} creature token{ab_str}'


KEYWORD_SUBS = {
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
    '_SCRY1_':          'Scry 1',
    '_SCRY2_':          'Scry 2',
    '_TREASURE_':       'Create a Treasure token',
    '_LANDFALL_':       '',   # handled separately
}

KEYWORD_NAMES = ('hexproof','indestructible','trample','first strike','double strike',
                 'lifelink','deathtouch','menace','flying','haste','vigilance','reach',
                 'persist','wither')


def apply_keyword_subs(s):
    for k, v in KEYWORD_SUBS.items():
        s = s.replace(k, v)
    return s


def split_top_and(s):
    """Split on && but not inside parentheses."""
    parts, depth, cur = [], 0, ''
    i = 0
    while i < len(s):
        if s[i] == '(':
            depth += 1; cur += s[i]; i += 1
        elif s[i] == ')':
            depth -= 1; cur += s[i]; i += 1
        elif s[i:i+2] == '&&' and depth == 0:
            parts.append(cur.strip()); cur = ''; i += 2
        else:
            cur += s[i]; i += 1
    if cur.strip():
        parts.append(cur.strip())
    return parts


def translate_auto(auto, card_name='this card'):
    if not auto:
        return ''
    s = auto.strip()
    s = apply_keyword_subs(s)

    # ── detect trigger prefix ────────────────────────────────────────────────
    trigger = ''
    trigger_patterns = [
        (r'^@movedTo\(this\|mybattlefield\):',
         'When ~ enters the battlefield, '),
        (r'^@movedTo\(this\|opponentbattlefield\):',
         "When ~ enters the battlefield under an opponent's control, "),
        (r'^@each my endstep:',
         'At the beginning of your end step, '),
        (r'^@each my upkeep:',
         'At the beginning of your upkeep, '),
        (r'^@each my combatbegin:',
         'At the beginning of combat on your turn, '),
        (r'^@each opponent upkeep:',
         "At the beginning of each opponent's upkeep, "),
        (r'^@each my draw:',
         'Whenever you draw a card, '),
        (r'^_DIES_:',
         'When ~ dies, '),
        (r'^_ATTACKING_:',
         'Whenever ~ attacks, '),
        (r'^_BLOCKING_:',
         'Whenever ~ blocks, '),
        (r'^_BLOCKED_:',
         'Whenever ~ becomes blocked, '),
        (r'^_LANDFALL_:',
         'Landfall — Whenever a land enters the battlefield under your control, '),
    ]
    for pat, repl in trigger_patterns:
        m = re.match(pat, s)
        if m:
            trigger = repl
            s = s[m.end():]
            break

    # ── activated-ability prefix: {cost}: ───────────────────────────────────
    act_m = re.match(r'^(\{[^}]+\}(?:\{[^}]+\})*(?:,\s*\{[^}]+\})*):(.+)$', s, re.DOTALL)
    if act_m and not trigger:
        cost = act_m.group(1)
        body = act_m.group(2).strip()
        body_txt = _translate_body(body, card_name)
        return f'{cost}: {body_txt}.'

    # ── pure keyword statics ─────────────────────────────────────────────────
    for kw_name in KEYWORD_NAMES:
        if s.strip() == kw_name:
            return kw_name.capitalize() + '.'

    # ── enchant static bonus ─────────────────────────────────────────────────
    enc_m = re.match(r'^enchanted\s+([+-]?\d+)/([+-]?\d+)$', s.strip())
    if enc_m:
        p, t = enc_m.group(1), enc_m.group(2)
        sp = '+' if not p.startswith('-') else ''
        st = '+' if not t.startswith('-') else ''
        return f'Enchanted creature gets {sp}{p}/{st}{t}.'

    enc_kw = re.match(r'^enchanted\s+(\w+)$', s.strip())
    if enc_kw:
        return f'Enchanted creature gains {enc_kw.group(1)}.'

    enc_cant = re.match(r'^enchanted\s+(cant\w+)$', s.strip())
    if enc_cant:
        kw = enc_cant.group(1).replace('cantattack', "can't attack").replace('cantblock', "can't block")
        return f'Enchanted creature {kw}.'

    enc_becomes = re.match(r'^enchanted\s+becomes\(,(\d+)/(\d+)\)$', s.strip())
    if enc_becomes:
        p, t = enc_becomes.group(1), enc_becomes.group(2)
        return f'Enchanted creature becomes a {p}/{t}.'

    # ── choice ───────────────────────────────────────────────────────────────
    choice_m = re.match(r'^choice\s+(.+)', s, re.DOTALL)
    if choice_m:
        rest = choice_m.group(1)
        options = re.findall(r'name\(([^)]+)\)', rest)
        if options:
            bullets = '\n• '.join(o.capitalize() for o in options)
            prefix = trigger if trigger else ''
            return f'{prefix}Choose one —\n• {bullets}.'

    # ── translate body (possibly multi-part) ────────────────────────────────
    body_txt = _translate_body(s, card_name)
    result = body_txt

    if trigger:
        # lowercase first letter of body
        if result:
            result = result[0].lower() + result[1:]
        result = trigger.replace('~', card_name) + result
    result = result.replace('~', card_name)

    if result and not result.endswith('.'):
        result += '.'
    return result


def _translate_body(s, card_name):
    """Translate the body (after trigger stripping) with && splits."""
    parts = split_top_and(s)
    clauses = [_translate_part(p.strip(), card_name) for p in parts]
    return '. '.join(c for c in clauses if c)


def _translate_part(part, card_name):
    if not part:
        return ''
    part = apply_keyword_subs(part)

    # if/then conditional - just render the parts
    cond_m = re.match(r'^if\s+.+then\s+(.+)$', part)
    if cond_m:
        body = _translate_part(cond_m.group(1), card_name)
        return body or part

    # pump(X/Y) target(...) [ueot]
    pump_m = re.match(r'^pump\(([+-]?\d+)/([+-]?\d+)\)\s+(target\([^)]+\))(\s+ueot)?', part)
    if pump_m:
        p, t = pump_m.group(1), pump_m.group(2)
        sp = '+' if not p.startswith('-') else ''
        st = '+' if not t.startswith('-') else ''
        tgt = target_phrase(pump_m.group(3)[7:-1])
        ueot = ' until end of turn' if pump_m.group(4) else ''
        return f'{tgt.capitalize()} gets {sp}{p}/{st}{t}{ueot}'

    # pump(X/Y) self
    pump_self = re.match(r'^pump\(([+-]?\d+)/([+-]?\d+)\)(\s+ueot)?$', part)
    if pump_self:
        p, t = pump_self.group(1), pump_self.group(2)
        sp = '+' if not p.startswith('-') else ''
        st = '+' if not t.startswith('-') else ''
        ueot = ' until end of turn' if pump_self.group(3) else ''
        return f'{card_name} gets {sp}{p}/{st}{t}{ueot}'

    # all(TYPE|ZONE) EFFECT
    all_m = re.match(r'^all\(([^)]+)\)\s+(.+)$', part)
    if all_m:
        spec = all_m.group(1)
        effect = all_m.group(2).strip()
        pipe = spec.find('|')
        if pipe >= 0:
            what, where = spec[:pipe], spec[pipe+1:]
        else:
            what, where = spec, ''
        what_clean = re.sub(r'\[.*?\]', '', what).strip()
        loc_map = {
            'mybattlefield': 'you control',
            'opponentbattlefield': 'an opponent controls',
        }
        loc = loc_map.get(where, '')
        noun = what_clean if what_clean != '*' else 'permanent'
        all_phrase = f'all {noun}s {loc}'.strip()

        # effect translation
        eff_parts = []
        for kw in KEYWORD_NAMES:
            if effect == kw or effect == kw + ' ueot':
                ueot = ' until end of turn' if 'ueot' in effect else ''
                eff_parts.append(f'gain {kw}{ueot}')
                break
        if not eff_parts:
            mv_all_m = re.match(r'^moveto\((\w+)\)$', effect)
            if mv_all_m:
                dest = mv_all_m.group(1)
                dest_map = {'hand': 'their owner\'s hand',
                            'myhand': 'your hand',
                            'exile': 'exile',
                            'mybattlefield': 'the battlefield'}
                eff_parts.append(f'return to {dest_map.get(dest, dest)}')
        if eff_parts:
            return f'{all_phrase.capitalize()} {" ".join(eff_parts)}'
        return part  # fallback

    # damage:N target(...)
    dmg_tgt = re.match(r'^damage:(\d+)\s+(target\([^)]+\))', part)
    if dmg_tgt:
        n   = dmg_tgt.group(1)
        tgt = target_phrase(dmg_tgt.group(2)[7:-1])
        return f'Deal {n} damage to {tgt}'

    # damage:N opponent/controller
    dmg_who = re.match(r'^damage:(\d+)\s+(opponent|controller)$', part)
    if dmg_who:
        n, who = dmg_who.group(1), dmg_who.group(2)
        who_txt = 'each opponent' if who == 'opponent' else 'you'
        return f'Deal {n} damage to {who_txt}'

    # counter(-1/-1,N) target(...) or counter(+1/+1,N) target(...)
    ctr_m = re.match(r'^counter\(([+-]?\d+)/([+-]?\d+),(\d+)\)\s+(target\([^)]+\))', part)
    if ctr_m:
        p, t, n = ctr_m.group(1), ctr_m.group(2), ctr_m.group(3)
        sp = '+' if not p.startswith('-') else ''
        st = '+' if not t.startswith('-') else ''
        tgt = target_phrase(ctr_m.group(4)[7:-1])
        return f'Put {n} {sp}{p}/{st}{t} counter{"s" if int(n)!=1 else ""} on {tgt}'

    # counter(-1/-1,N) self
    ctr_self = re.match(r'^counter\(([+-]?\d+)/([+-]?\d+),(\d+)\)$', part)
    if ctr_self:
        p, t, n = ctr_self.group(1), ctr_self.group(2), ctr_self.group(3)
        sp = '+' if not p.startswith('-') else ''
        st = '+' if not t.startswith('-') else ''
        return f'Put {n} {sp}{p}/{st}{t} counter{"s" if int(n)!=1 else ""} on {card_name}'

    # moveto(dest) target(...)
    mv_tgt = re.match(r'^moveto\((\w+)\)\s+(target\([^)]+\))', part)
    if mv_tgt:
        dest = mv_tgt.group(1)
        tgt  = target_phrase(mv_tgt.group(2)[7:-1])
        dest_map = {
            'mybattlefield':       'the battlefield',
            'exile':               'exile',
            'mygraveyard':         'your graveyard',
            'myhand':              'your hand',
            'hand':                'its owner\'s hand',
        }
        dest_txt = dest_map.get(dest, dest)
        if dest == 'exile':
            return f'Exile {tgt}'
        return f'Put {tgt} onto {dest_txt}'

    # moveto(dest) [controller/opponent]
    mv_self = re.match(r'^moveto\((\w+)\)(?:\s+(?:controller|opponent))?$', part)
    if mv_self:
        dest = mv_self.group(1)
        dest_map = {
            'mybattlefield': 'the battlefield',
            'exile': 'exile',
            'mygraveyard': 'your graveyard',
            'myhand': 'your hand',
        }
        dest_txt = dest_map.get(dest, dest)
        return f'Put {card_name} onto {dest_txt}'

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

    # fizzle all(...)
    fiz_all = re.match(r'^fizzle\s+all\(\*\|opponentstack\)', part)
    if fiz_all:
        return 'Counter all spells and abilities your opponents control'

    # fizzle target(...)
    fiz_tgt = re.match(r'^fizzle\s+(target\([^)]+\))', part)
    if fiz_tgt:
        tgt = target_phrase(fiz_tgt.group(1)[7:-1])
        return f'Counter {tgt}'

    # fight target(...)
    fight_m = re.match(r'^fight\s+(target\([^)]+\))', part)
    if fight_m:
        tgt = target_phrase(fight_m.group(1)[7:-1])
        return f'{card_name} fights {tgt}'

    # draw:N [controller]
    draw_m = re.match(r'^draw:(\d+)(?:\s+controller)?$', part)
    if draw_m:
        n = draw_m.group(1)
        return f'Draw {n} card{"s" if int(n)!=1 else ""}'

    # life:N [controller]
    life_m = re.match(r'^life:(\d+)(?:\s+controller)?$', part)
    if life_m:
        n = life_m.group(1)
        return f'You gain {n} life'

    # life:-N
    losel_m = re.match(r'^life:-(\d+)(?:\s+(?:controller|opponent))?$', part)
    if losel_m:
        n = losel_m.group(1)
        return f'You lose {n} life'

    # mill:N [controller]
    mill_m = re.match(r'^mill:(\d+)(?:\s+controller)?$', part)
    if mill_m:
        n = mill_m.group(1)
        return f'Mill {n} card{"s" if int(n)!=1 else ""}'

    # discard:N [controller]
    disc_m = re.match(r'^discard:(\d+)(?:\s+controller)?$', part)
    if disc_m:
        n = disc_m.group(1)
        return f'Discard {n} card{"s" if int(n)!=1 else ""}'

    # keyword [ueot] target(...)
    for kw in KEYWORD_NAMES:
        tgt_kw = re.match(r'^' + re.escape(kw) + r'(\s+ueot)?\s+(target\([^)]+\))', part)
        if tgt_kw:
            ueot = ' until end of turn' if tgt_kw.group(1) else ''
            tgt = target_phrase(tgt_kw.group(2)[7:-1])
            return f'{tgt.capitalize()} gains {kw}{ueot}'

    # token(...)
    tok_m = re.match(r'^token\((.+)\)$', part)
    if tok_m:
        return token_phrase(tok_m.group(1))

    # Scry N plain
    if part == 'Scry 1' or part == 'Scry 2':
        return part

    # Ward {N}
    ward_m = re.match(r'^Ward \{(\d+)\}$', part)
    if ward_m:
        return part

    # Create a Treasure token
    if 'Treasure token' in part:
        return part

    return part  # fallback: return as-is


# ─────────────────────────── load ECL primitive names ────────────────────────

with open('M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/ECL/_cards.dat', 'rb') as f:
    content = f.read().decode('utf-8', errors='ignore')

blocks = re.findall(r'\[card\](.*?)\[/card\]', content, re.DOTALL)
ecl_primitives = set()
for block in blocks:
    m_prim = re.search(r'primitive=(.+)', block)
    if m_prim:
        prim = m_prim.group(1).strip().split(' // ')[0].strip()
        ecl_primitives.add(prim.lower())

# ─────────────────────────── patch primitives files ──────────────────────────

def patch_file(fpath):
    with open(fpath, encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Split on [card] / [/card] boundaries, preserving them
    raw_parts = re.split(r'(\[card\]|\[/card\])', text)

    out_parts = []
    i = 0
    patched = 0
    while i < len(raw_parts):
        part = raw_parts[i]
        if part == '[card]' and i+2 < len(raw_parts):
            block = raw_parts[i+1]
            close = raw_parts[i+2]
            if close == '[/card]':
                m_name = re.search(r'^name=(.+)', block, re.MULTILINE)
                if m_name:
                    name = m_name.group(1).strip()
                    if name.lower() in ecl_primitives:
                        has_text = bool(re.search(r'^text=.+', block, re.MULTILINE))
                        if not has_text:
                            m_auto = re.search(r'^auto=(.+)', block, re.MULTILINE)
                            auto = m_auto.group(1).strip() if m_auto else ''
                            translated = translate_auto(auto, card_name=name)
                            if translated:
                                # Insert text= after 'name=...' line
                                # Find where to insert: before 'auto=' or at end of block
                                # Insert before the first ability line (auto/type)
                                insert_after = re.search(r'^(type=.+\n)', block, re.MULTILINE)
                                if insert_after:
                                    pos = insert_after.end()
                                    block = block[:pos] + f'text={translated}\n' + block[pos:]
                                else:
                                    # just append before [/card]
                                    block = block.rstrip('\n') + f'\ntext={translated}\n'
                                patched += 1
                out_parts.append(part)
                out_parts.append(block)
                out_parts.append(close)
                i += 3
                continue
        out_parts.append(part)
        i += 1

    with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(out_parts))
    return patched


for fpath in [
    'M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/primitives/mtg.txt',
    'M:/Claude_projects/wagic/projects/mtg/bin/Res/sets/primitives/planeswalkers.txt',
]:
    n = patch_file(fpath)
    print(f'Patched {n} cards in {fpath}')

print('Done.')
