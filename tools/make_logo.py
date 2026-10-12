"""Builds the Brilio "Sparkle Dots" logo SVGs in brand/ with the lettering converted to outlines.

Usage: python3 tools/make_logo.py PlusJakartaSans-ExtraBold.ttf brand   (needs: pip install fonttools)
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

FONT = TTFont(sys.argv[1]); OUT = sys.argv[2]
cmap = FONT.getBestCmap(); gs = FONT.getGlyphSet(); upm = FONT["head"].unitsPerEm
hmtx = FONT["hmtx"]
NAVY, SKY, WHITE = "#0d2233", "#41b6e6", "#ffffff"
SPARK = "M0,-10 C1.2,-3 3,-1.2 10,0 C3,1.2 1.2,3 0,10 C-1.2,3 -3,1.2 -10,0 C-3,-1.2 -1.2,-3 0,-10Z"

def kern_pairs():
    """Pair kerning from GPOS (format 1 and 2 PairPos), in font units."""
    out = {}
    if "GPOS" not in FONT: return out
    for lookup in FONT["GPOS"].table.LookupList.Lookup:
        subs = lookup.SubTable
        for st in subs:
            if lookup.LookupType == 9: st = st.ExtSubTable
            if getattr(st, "LookupType", lookup.LookupType) != 2: continue
            cov = st.Coverage.glyphs
            if st.Format == 1:
                for i, g1 in enumerate(cov):
                    for pvr in st.PairSet[i].PairValueRecord:
                        v = getattr(pvr.Value1, "XAdvance", 0) if pvr.Value1 else 0
                        if v: out.setdefault((g1, pvr.SecondGlyph), v)
            elif st.Format == 2:
                c1 = st.ClassDef1.classDefs; c2 = st.ClassDef2.classDefs
                for g1 in cov:
                    for g2 in gs.keys():
                        r = st.Class1Record[c1.get(g1, 0)].Class2Record[c2.get(g2, 0)]
                        v = getattr(r.Value1, "XAdvance", 0) if r.Value1 else 0
                        if v: out.setdefault((g1, g2), v)
    return out
KERN = kern_pairs()

def text_path(text, size, x0, baseline, tracking=0.0):
    """Outlined path for text; returns (path d, list of per-glyph (x, width), right edge)."""
    s = size / upm; pen = SVGPathPen(gs); x = x0; boxes = []
    names = [cmap[ord(c)] for c in text]
    for i, g in enumerate(names):
        tp = TransformPen(pen, (s, 0, 0, -s, x, baseline))
        gs[g].draw(tp)
        bp = BoundsPen(gs); gs[g].draw(bp)
        xmin, ymin, xmax, ymax = bp.bounds or (0, 0, 0, 0)
        boxes.append((x + xmin * s, x + xmax * s, baseline - ymax * s))
        adv = hmtx[g][0]
        if i + 1 < len(names): adv += KERN.get((g, names[i + 1]), 0)
        x += adv * s + tracking
    return pen.getCommands(), boxes, x - tracking

def spark(cx, cy, size, fill):
    k = size / 20
    return f'<path transform="translate({cx:.2f} {cy:.2f}) scale({k:.4f})" fill="{fill}" d="{SPARK}"/>'

# Wordmark: "brılıo" (dotless i) with sparkles where the dots go
SIZE = 56
d, boxes, right = text_path("brılıo", SIZE, 0, 60, tracking=-1)
sparks = [((boxes[i][0] + boxes[i][1]) / 2, 11) for i in (2, 4)]
ink_top = 1; ink_bottom = max(60 + 0, 60)  # baseline; no descenders in "brilio"
left = boxes[0][0]
pad = 2
vb = (left - pad, ink_top - pad, (right - left) + 2 * pad, (60 - ink_top) + 2 * pad)
def wordmark(text_fill):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{vb[2]*4:.0f}" height="{vb[3]*4:.0f}" viewBox="{vb[0]:.2f} {vb[1]:.2f} {vb[2]:.2f} {vb[3]:.2f}">'
            f'<title>Brilio</title><path fill="{text_fill}" d="{d}"/>'
            + "".join(spark(x, y, 18, SKY) for x, y in sparks) + "</svg>\n")
open(f"{OUT}/brilio-logo.svg", "w").write(wordmark(NAVY))
open(f"{OUT}/brilio-logo-white.svg", "w").write(wordmark(WHITE))

# Icon: sky tile, white "b", white sparkle
def b_glyph(size, cx, baseline, fill):
    d, boxes, _ = text_path("b", size, 0, baseline)
    w = boxes[0][1] - boxes[0][0]
    dx = cx - (boxes[0][0] + w / 2)
    return f'<path transform="translate({dx:.2f} 0)" fill="{fill}" d="{d}"/>'
icon = ('<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 64 64"><title>Brilio</title>'
        f'<rect width="64" height="64" rx="14" fill="{SKY}"/>' + b_glyph(42, 30, 47, WHITE) + spark(47.5, 16.5, 15, WHITE) + "</svg>\n")
open(f"{OUT}/brilio-icon.svg", "w").write(icon)

# Profile picture: full-bleed square, content kept inside the circle crop
profile = ('<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 64 64"><title>Brilio</title>'
           f'<rect width="64" height="64" fill="{SKY}"/>' + b_glyph(36, 30, 44.5, WHITE) + spark(44.5, 19, 12, WHITE) + "</svg>\n")
open(f"{OUT}/brilio-profile-picture.svg", "w").write(profile)
print("viewBox", [round(v, 1) for v in vb], "sparks", [(round(x, 1), y) for x, y in sparks], "kern pairs", len(KERN))
