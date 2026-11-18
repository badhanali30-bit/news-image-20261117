#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a newspaper front page summing up
Tuesday 17 November 2026. Deterministic: fixed content, no timestamps,
no randomness — running it twice yields byte-identical entry.png.

Usage: python3 draw.py   (writes entry.png next to this script)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ----------------------------------------------------------------
PAPER = (248, 244, 233)
INK = (24, 24, 24)
RED = (178, 34, 34)
NAVY = (26, 43, 77)
BLUE = (47, 102, 168)
LIGHT_BLUE = (205, 224, 240)
GREY = (110, 110, 104)
RULE = (24, 24, 24)
CARD = (255, 255, 255)
SOFT = (238, 232, 216)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FONT_DIR}/noto/NotoSerif-Bold.ttf"
SANS_B = f"{FONT_DIR}/noto/NotoSans-Bold.ttf"
SANS_R = f"{FONT_DIR}/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def hline(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# --- icons (flat vector-style shapes, drawn with PIL) -----------------------

def icon_bridge(d, x, y, s):
    """Kerch Bridge pictogram: deck, two towers, cables, water."""
    w, h = s, int(s * 0.72)
    # sky panel
    d.rectangle([x, y, x + w, y + h], fill=LIGHT_BLUE)
    deck_y = y + int(h * 0.62)
    # towers
    for tx in (x + int(w * 0.22), x + int(w * 0.70)):
        d.rectangle([tx, y + int(h * 0.12), tx + 8, deck_y], fill=NAVY)
    # cables fan out from each tower top to its own half of the deck
    for tx, ends in ((x + int(w * 0.22) + 4, (x + 6, x + int(w * 0.45))),
                     (x + int(w * 0.70) + 4, (x + int(w * 0.55), x + w - 6))):
        top_y = y + int(h * 0.14)
        for ex in ends:
            d.line([(tx, top_y), (ex, deck_y)], fill=NAVY, width=2)
    # deck
    d.rectangle([x + 4, deck_y, x + w - 4, deck_y + 8], fill=INK)
    # blast mark over the deck centre
    cx, cy = x + w // 2, deck_y - 6
    for dx, dy in ((-14, -8), (0, -16), (14, -8), (-18, 4), (18, 4)):
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=RED, width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    # water
    for wy in (deck_y + 16, deck_y + 26):
        d.line([(x + 8, wy), (x + w - 8, wy)], fill=BLUE, width=3)


def icon_tanker(d, x, y, s):
    w, h = s, s
    d.rectangle([x, y, x + w, y + h], fill=LIGHT_BLUE)
    hull_y = y + 34
    # hull
    d.polygon([(x + 6, hull_y), (x + w - 6, hull_y),
               (x + w - 16, hull_y + 14), (x + 16, hull_y + 14)], fill=NAVY)
    # containers
    d.rectangle([x + 10, hull_y - 16, x + 24, hull_y - 1], fill=RED)
    d.rectangle([x + 27, hull_y - 16, x + 41, hull_y - 1], fill=(214, 138, 32))
    # funnel
    d.rectangle([x + 44, hull_y - 22, x + 52, hull_y - 1], fill=INK)
    # mine in the water
    mx, my = x + 46, hull_y + 20
    d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=INK)
    for dx, dy in ((-7, -7), (7, -7), (-7, 7), (7, 7), (0, -8), (0, 8)):
        d.line([(mx, my), (mx + dx, my + dy)], fill=INK, width=2)
    # waves
    d.line([(x + 4, hull_y + 18), (x + 34, hull_y + 18)], fill=BLUE, width=3)


def icon_globe(d, x, y, s):
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LIGHT_BLUE, outline=NAVY, width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=NAVY, width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=NAVY, width=2)
    # three small flags on top
    for i, col in enumerate((RED, (214, 138, 32), (46, 125, 50))):
        fx = x + i * (s // 3) + 4
        d.line([(fx + 8, y + 2), (fx + 8, y + 14)], fill=INK, width=2)
        d.polygon([(fx + 8, y + 2), (fx + 24, y + 6), (fx + 8, y + 10)], fill=col)


def icon_laptop(d, x, y, s):
    w = s
    # screen
    d.rectangle([x + 6, y + 6, x + w - 6, y + 36], fill=NAVY)
    d.rectangle([x + 11, y + 11, x + w - 11, y + 31], fill=(235, 240, 245))
    # warning triangle on screen
    cx, cy = x + w // 2, y + 21
    d.polygon([(cx, cy - 12), (cx + 14, cy + 9), (cx - 14, cy + 9)], fill=RED)
    d.text((cx - 3, cy - 6), "!", font=font(SANS_B, 15), fill=(255, 255, 255))
    # base
    d.polygon([(x + 2, y + 40), (x + w - 2, y + 40),
               (x + w - 10, y + 50), (x + 10, y + 50)], fill=INK)


def icon_gavel(d, x, y, s):
    # gavel: head (two stacked bars), long handle, sounding block
    d.rectangle([x + 8, y + 8, x + s - 8, y + 24], fill=NAVY)
    d.rectangle([x + 14, y + 28, x + s - 14, y + 36], fill=NAVY)
    d.rectangle([x + s // 2 - 4, y + 36, x + s // 2 + 4, y + s - 8], fill=(122, 84, 40))
    d.rectangle([x + 6, y + s - 8, x + s - 6, y + s - 2], fill=GREY)


def icon_jet(d, x, y, s):
    # simple jet silhouette
    d.polygon([(x + 6, y + s // 2), (x + s - 6, y + s // 2 - 8),
               (x + s - 22, y + s // 2 + 2), (x + int(s * 0.55), y + s // 2 + 6),
               (x + int(s * 0.42), y + s - 8), (x + int(s * 0.30), y + s // 2 + 8),
               (x + int(s * 0.18), y + s // 2 + 10)], fill=NAVY)
    d.polygon([(x + int(s * 0.45), y + s // 2 - 4), (x + int(s * 0.62), y + 6),
               (x + int(s * 0.72), y + s // 2 - 2)], fill=NAVY)


def icon_cricket(d, x, y, s):
    # bat
    d.rounded_rectangle([x + 10, y + 8, x + 30, y + s - 18], radius=8, fill=(214, 178, 110))
    d.rectangle([x + 16, y + s - 22, x + 24, y + s - 4], fill=(122, 84, 40))
    # ball
    bx, by = x + s - 22, y + 22
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=RED, outline=(255, 255, 255), width=2)
    d.arc([bx - 12, by - 12, bx + 12, by + 12], 200, 340, fill=(255, 255, 255), width=2)
    # stumps
    for i in range(3):
        sx = x + s - 34 + i * 9
        d.rectangle([sx, y + s - 26, sx + 4, y + s - 6], fill=(214, 178, 110))


def icon_ship(d, x, y, s):
    w, h = s, s
    d.rectangle([x, y, x + w, y + h], fill=LIGHT_BLUE)
    deck_y = y + 32
    # hull
    d.polygon([(x + 4, deck_y), (x + w - 4, deck_y),
               (x + w - 14, deck_y + 14), (x + 14, deck_y + 14)], fill=NAVY)
    # island tower
    d.rectangle([x + 36, deck_y - 18, x + 46, deck_y - 1], fill=INK)
    d.rectangle([x + 38, deck_y - 24, x + 44, deck_y - 18], fill=INK)
    # flight deck line + jets
    d.line([(x + 8, deck_y - 2), (x + w - 8, deck_y - 2)], fill=(255, 255, 255), width=2)
    for jx in (x + 10, x + 22):
        d.polygon([(jx, deck_y - 10), (jx + 12, deck_y - 10), (jx + 6, deck_y - 3)], fill=RED)
    # waves
    d.line([(x + 4, deck_y + 18), (x + w - 4, deck_y + 18)], fill=BLUE, width=3)


ICONS = {
    "bridge": icon_bridge,
    "tanker": icon_tanker,
    "globe": icon_globe,
    "laptop": icon_laptop,
    "gavel": icon_gavel,
    "jet": icon_jet,
    "cricket": icon_cricket,
    "ship": icon_ship,
}

# --- stories ----------------------------------------------------------------
# (kicker, headline, summary, icon) — all verified events of 17 Nov 2026.
LEAD = (
    "LEAD STORY  •  UKRAINE",
    "Ukraine strikes the Kerch Bridge again",
    "Kyiv hits the Crimean Bridge for a second day in a row; Russia "
    "strikes two bridges in Kyiv.",
    "bridge",
)

STORIES = [
    ("GULF", "Mines hit tankers near Hormuz",
     "Iran's Guard drones strike a US radar in Bahrain; Bahrain says "
     "all intercepted, no casualties.",
     "tanker"),
    ("DIPLOMACY", "Xi, Trump and Putin to meet",
     "China confirms the first Xi–Trump–Putin summit, Thursday "
     "19 November in Shenzhen.",
     "globe"),
    ("CYBER", "Malware hits 178 major websites",
     "Malicious code via Optimizely hits BBC, CNN, Zoom and HSBC, "
     "aiming to steal crypto and card data.",
     "laptop"),
    ("UK / ISRAEL", "Britain sanctions Israeli firms",
     "UK sanctions eight Israeli settlement firms; Netanyahu camp "
     "accused over election-day arrests.",
     "gavel"),
    ("ASIA / EUROPE", "Japan protests Russian jets",
     "Japan protests suspected Russian jets in its airspace; EU "
     "sanctions 12 people and 101 entities.",
     "jet"),
    ("SPORT", "Jay Shah re-elected ICC chairman",
     "ICC re-elects Jay Shah chairman for a second term, unopposed.",
     "cricket"),
    ("US NAVY", "Third US carrier reaches the Gulf",
     "USS Theodore Roosevelt arrives in the Middle East — the third "
     "US carrier group in the region.",
     "ship"),
]

NUMBERS = [("178", "websites hit"), ("8", "firms hit"),
           ("101", "entities hit"), ("3", "carriers")]


# --- page -------------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 44                      # side margin
    CW = W - 2 * MX              # content width

    # outer frame
    d.rectangle([18, 18, W - 19, H - 19], outline=RULE, width=3)
    d.rectangle([24, 24, W - 25, H - 25], outline=RULE, width=1)

    # masthead
    f_mast = font(SERIF_B, 76)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 34), title, font=f_mast, fill=INK)
    f_tag = font(SANS_B, 17)
    tag = "ONE DAY  •  ONE PAGE  •  THE WORLD IN BRIEF"
    tw = d.textlength(tag, font=f_tag)
    d.text(((W - tw) / 2, 122), tag, font=f_tag, fill=GREY)
    hline(d, MX, W - MX, 152, width=3)

    # date band — the day this page sums up, big and prominent
    d.rectangle([MX, 164, W - MX, 216], fill=NAVY)
    f_date = font(SANS_B, 38)
    date = "TUESDAY 17 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 174), date, font=f_date, fill=(255, 255, 255))

    # ---- lead story ------------------------------------------------------
    ly0, ly1 = 230, 470
    d.rectangle([MX, ly0, W - MX, ly1], fill=CARD, outline=RULE, width=2)
    f_kick = font(SANS_B, 19)
    d.text((MX + 22, ly0 + 14), LEAD[0], font=f_kick, fill=RED)
    f_lead = font(SANS_B, 41)
    lines = wrap(d, LEAD[1], f_lead, 560)
    y = draw_lines(d, MX + 22, ly0 + 44, lines, f_lead, INK, 48)
    f_sum = font(SANS_R, 23)
    lines = wrap(d, LEAD[2], f_sum, 560)
    draw_lines(d, MX + 22, y + 10, lines, f_sum, INK, 30)
    # lead pictogram (bridge) on the right
    px, py, ps = W - MX - 22 - 300, ly0 + 18, 300
    ICONS[LEAD[3]](d, px, py, ps)
    d.rectangle([px, py, px + ps, py + int(ps * 0.72)], outline=RULE, width=2)

    # ---- story grid: 2 columns x 4 rows ----------------------------------
    gx, gy = MX, 484
    cell_w, cell_h = (CW - 16) // 2, 116
    f_k = font(SANS_B, 15)
    f_h = font(SANS_B, 21)
    f_s = font(SANS_R, 17)

    cells = list(STORIES) + [None]  # last cell = numbers box
    for idx, story in enumerate(cells):
        col, row = idx % 2, idx // 2
        x0 = gx + col * (cell_w + 16)
        y0 = gy + row * (cell_h + 8)
        d.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], fill=CARD, outline=RULE, width=1)
        if story is None:
            # "the day in numbers" box
            d.text((x0 + 16, y0 + 10), "THE DAY IN NUMBERS", font=f_k, fill=RED)
            nx = x0 + 16
            f_n = font(SANS_B, 30)
            f_nl = font(SANS_R, 15)
            for num, lab in NUMBERS:
                d.text((nx, y0 + 36), num, font=f_n, fill=NAVY)
                d.text((nx, y0 + 74), lab, font=f_nl, fill=GREY)
                nx += 110
            continue
        kicker, headline, summary, icon = story
        d.text((x0 + 78, y0 + 8), kicker, font=f_k, fill=RED)
        lines = wrap(d, headline, f_h, cell_w - 94)
        draw_lines(d, x0 + 78, y0 + 26, lines[:2], f_h, INK, 24)
        lines = wrap(d, summary, f_s, cell_w - 32)
        draw_lines(d, x0 + 16, y0 + 74, lines[:2], f_s, INK, 19)
        ICONS[icon](d, x0 + 10, y0 + 8, 58)

    # footer
    f_f = font(SANS_R, 16)
    foot = "All stories verified from live news reporting on 17 November 2026"
    tw = d.textlength(foot, font=f_f)
    d.text(((W - tw) / 2, H - 46), foot, font=f_f, fill=GREY)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
