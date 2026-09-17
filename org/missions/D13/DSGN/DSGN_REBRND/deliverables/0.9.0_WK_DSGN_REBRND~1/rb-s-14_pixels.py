"""Pixel-share read of the three full-page renders. Ran from <WS>/.scratch/ (TO-RB-s-14,
0.9.0_WK_DSGN_REBRND~1); the deliverables copy is the same bytes, committed as evidence.
A second instrument beside extract.js's DOM areaPct: it counts painted pixels, not element boxes."""
import colorsys
import json
from collections import Counter
from PIL import Image

D = "C:/tmp/wk-dsgn-1j/org/missions/D13/DSGN/DSGN_REBRND/deliverables/0.9.0_WK_DSGN_REBRND~1/"
NAMED = {"canvas #F4F6FA": (0xF4, 0xF6, 0xFA), "darkField #0A1733": (0x0A, 0x17, 0x33),
         "accent #5F3BE3": (0x5F, 0x3B, 0xE3), "navy #163372": (0x16, 0x33, 0x72),
         "white #FFFFFF": (0xFF, 0xFF, 0xFF), "coolGrey #C4CBDB": (0xC4, 0xCB, 0xDB)}
TOL = 6
out = {}
for slug in ("market", "positioning", "portfolio-management"):
    im = Image.open(D + "rb-s-14_%s_extract_1440.png" % slug).convert("RGB")
    w, h = im.size
    px = Counter(im.getdata())
    total = w * h
    shares = {}
    for name, (r0, g0, b0) in NAMED.items():
        n = sum(c for (r, g, b), c in px.items() if abs(r - r0) <= TOL and abs(g - g0) <= TOL and abs(b - b0) <= TOL)
        shares[name] = round(100.0 * n / total, 2)
    # chromatic buckets (4-bit/channel), share and chroma = S*V
    buckets = Counter()
    for (r, g, b), c in px.items():
        buckets[(r >> 4, g >> 4, b >> 4)] += c
    chroma = []
    for (r, g, b), c in buckets.items():
        rr, gg, bb = (r * 16 + 8) / 255.0, (g * 16 + 8) / 255.0, (b * 16 + 8) / 255.0
        hh, s, v = colorsys.rgb_to_hsv(rr, gg, bb)
        share = 100.0 * c / total
        if s >= 0.35 and v >= 0.35:
            chroma.append({"hex": "#%02X%02X%02X" % (r * 16 + 8, g * 16 + 8, b * 16 + 8), "sharePct": round(share, 3),
                           "chroma": round(s * v, 3), "hueDeg": round(hh * 360)})
    by_share = sorted(chroma, key=lambda d: -d["sharePct"])[:8]
    loud = sorted([d for d in chroma if d["sharePct"] >= 0.1], key=lambda d: -d["chroma"])[:5]
    out[slug] = {"png": "rb-s-14_%s_extract_1440.png" % slug, "sizePx": [w, h], "pixels": total,
                 "namedSharePct(tol=6)": shares, "chromaticBySharePct": by_share,
                 "loudestChromatic(share>=0.1%, by S*V)": loud}
    print("===", slug, w, "x", h, "pixels", total)
    print(" named", json.dumps(shares))
    print(" chromatic-by-share", json.dumps(by_share))
    print(" loudest", json.dumps(loud))
json.dump(out, open(D + "rb-s-14_pixel_shares.json", "w", encoding="utf-8", newline="\n"), indent=2)
print("SAVED", D + "rb-s-14_pixel_shares.json")
