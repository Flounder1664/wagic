#!/usr/bin/env python3
"""
build_ability_icons_from_sheet.py -- generate ability-icon badges for the keywords
that the Mana project does not ship (see build_ability_icons.sh / issue #31), from a
user-supplied contact sheet of icons.

Like the Mana generator, the *output* PNGs are derived from third-party artwork and
are for a private build only -- do not commit them (.gitignore guards the local
Res/graphics/keywords/ output). This script is code and carries no artwork itself.

The expected source is a 4-column x 2-row grid (any resolution) laid out as:

    row 1:  intimidate | shroud | fear        | unblockable(bars)
    row 2:  unblockable(moon) | infect | (unused) | wither(wilted)

Each glyph is recoloured to a flat white silhouette on the same dark rounded box the
Mana badges use; internal white areas (e.g. the devil's eyes) become transparent so
they read as dark cut-outs. Adjust CELLS below if your sheet differs.

Usage:
    python build_ability_icons_from_sheet.py <source-image> <output-dir>

Requires Pillow (PIL).
"""
import os
import sys
from PIL import Image, ImageDraw

SIZE = 96          # output badge is SIZE x SIZE px
INNER = SIZE - 24  # glyph is fitted within this

# Fractional crop boxes (x0, y0, x1, y1) of the icon *inside* each cell frame, above
# the label -- expressed as fractions of the sheet so they scale to any resolution.
# Grid is 4 columns wide; a cell is 1/4 in x. Rows are 1/2 in y.
def cell(col, row):
    cw, ch = 1.0 / 4.0, 1.0 / 2.0
    x0 = col * cw + 0.043
    x1 = col * cw + cw - 0.043
    y0 = row * ch + 0.054
    y1 = row * ch + 0.402
    return (x0, y0, x1, y1)

# keyword -> (fractional box, alpha threshold). shroud is light-grey fill, not black
# line-art, so it uses a lower threshold to retain more of the figure.
CELLS = {
    "intimidate":  (cell(0, 0), 45),
    "shroud":      (cell(1, 0), 25),
    "fear":        (cell(2, 0), 45),
    "unblockable": (cell(0, 1), 45),   # bottom-row (moon) variant
    "infect":      (cell(1, 1), 45),
    "wither":      (cell(3, 1), 45),   # right-hand (wilted) variant
}


def dark_box():
    bg = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle([4, 4, SIZE - 5, SIZE - 5], radius=14,
                        fill=(30, 30, 40, 255), outline=(220, 220, 230, 255), width=2)
    return bg


def make(sheet, key, frac, thresh, outdir):
    W, H = sheet.size
    x0, y0, x1, y1 = frac
    region = sheet.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))).convert("L")
    # dark art -> opaque white; white background -> transparent
    alpha = region.point(lambda p: 0 if (255 - p) < thresh else (255 - p))
    glyph = Image.new("RGBA", region.size, (255, 255, 255, 255))
    glyph.putalpha(alpha)
    bbox = alpha.getbbox()
    if bbox:
        glyph = glyph.crop(bbox)
    glyph.thumbnail((INNER, INNER), Image.LANCZOS)
    box = dark_box()
    box.alpha_composite(glyph, ((SIZE - glyph.width) // 2, (SIZE - glyph.height) // 2))
    box.save(os.path.join(outdir, key + ".png"))
    print(f"  {key}.png")


def main():
    if len(sys.argv) != 3:
        print("usage: build_ability_icons_from_sheet.py <source-image> <output-dir>", file=sys.stderr)
        return 2
    src, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    sheet = Image.open(src).convert("RGB")
    for key, (frac, thresh) in CELLS.items():
        make(sheet, key, frac, thresh, outdir)
    print(f"generated {len(CELLS)} ability icons in {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
