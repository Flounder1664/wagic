#!/usr/bin/env bash
#
# build_ability_icons.sh -- generate keyword ability-icon badges for Wagic's card
# preview (see CardGui::RenderAbilityIconsBig / issue #31).
#
# The icon artwork is NOT distributed with Wagic: the source glyphs are from the
# Mana project (https://github.com/andrewgioia/mana), whose README notes the
# symbol images are copyright Wizards of the Coast. This script fetches those
# glyphs to *your* machine and rasterises them into local PNGs; the output is
# intended for a private build and must not be committed to the repository. Any
# keyword without a generated PNG falls back to the built-in two-letter badge.
#
# Usage:
#   tools/build_ability_icons.sh <output-dir> [mana-svg-dir]
#
#   <output-dir>    where the <keyword>.png files are written, e.g.
#                   G:/Wagic-windows/Res/graphics/keywords
#   [mana-svg-dir]  optional path to a local checkout's svg/ folder; if omitted
#                   the SVGs are downloaded from the Mana repo over HTTPS.
#
# Requires ImageMagick (magick) and, when downloading, curl.

set -euo pipefail

OUT="${1:-}"
MANA_SVG_DIR="${2:-}"
if [ -z "$OUT" ]; then
    echo "usage: $0 <output-dir> [mana-svg-dir]" >&2
    exit 2
fi

command -v magick >/dev/null 2>&1 || { echo "error: ImageMagick 'magick' not found on PATH" >&2; exit 1; }

MANA_RAW="https://raw.githubusercontent.com/andrewgioia/mana/master/svg"

# Wagic keyword name (matches kKeywords[].icon in CardGui.cpp)  ->  Mana ability slug.
# Only keywords that Mana actually ships are listed; the rest keep the letter badge.
MAP="
flying:ability-flying
firststrike:ability-firststrike
doublestrike:ability-doublestrike
deathtouch:ability-deathtouch
trample:ability-trample
lifelink:ability-lifelink
vigilance:ability-vigilance
menace:ability-menace
reach:ability-reach
haste:ability-haste
flash:ability-flash
defender:ability-defender
hexproof:ability-hexproof
indestructible:ability-indestructible
changeling:ability-changeling
"

SIZE=96          # output badge is SIZE x SIZE px
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$OUT"

# Shared dark rounded-rect background with a light outline (matches the built-in badge).
BG="$TMP/_bg.png"
magick -size ${SIZE}x${SIZE} xc:none \
    -fill "#1e1e28" -draw "roundrectangle 4,4 $((SIZE-5)),$((SIZE-5)) 14,14" \
    -stroke "#dcdce6" -strokewidth 2 -fill none -draw "roundrectangle 4,4 $((SIZE-5)),$((SIZE-5)) 14,14" \
    "$BG"

count=0
for entry in $MAP; do
    key="${entry%%:*}"
    slug="${entry##*:}"
    svg="$TMP/$slug.svg"

    if [ -n "$MANA_SVG_DIR" ]; then
        cp "$MANA_SVG_DIR/$slug.svg" "$svg" || { echo "error: $MANA_SVG_DIR/$slug.svg not found" >&2; exit 1; }
    else
        command -v curl >/dev/null 2>&1 || { echo "error: curl needed to download SVGs" >&2; exit 1; }
        curl -fsSL "$MANA_RAW/$slug.svg" -o "$svg" || { echo "error: failed to download $slug.svg" >&2; exit 1; }
    fi

    # Rasterise the glyph as solid white on transparent, then centre it on the badge.
    glyph="$TMP/$key.glyph.png"
    magick -background none -density 300 "$svg" -resize $((SIZE-24))x$((SIZE-24)) \
        -fill white -colorize 100 "$glyph"
    magick "$BG" "$glyph" -gravity center -composite "$OUT/$key.png"
    count=$((count + 1))
    echo "  $key.png"
done

echo "generated $count ability icons in $OUT"
