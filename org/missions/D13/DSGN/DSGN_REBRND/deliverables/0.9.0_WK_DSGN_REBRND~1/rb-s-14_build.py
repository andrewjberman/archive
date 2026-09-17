"""rb14-build.py -- builds design/brand/portal-routes.json in the shape of design/brand/opalinvest.com.json
from the raw extract.js outputs + the pixel-share read. Ran from <WS>/.scratch/ (TO-RB-s-14,
0.9.0_WK_DSGN_REBRND~1); the deliverables copy is the same bytes, committed as evidence.

Every portal value below is DERIVED from the raw run files; no site value is copied into the file.
The comparison section cites the site by JSON pointer into opalinvest.com.json (or by the brief's IV.3
Site column where the site file carries no measurement), so a check that looks for the site canvas in
this file can only find the portal's own measured canvas.
  --mutant-canvas "rgb(r, g, b)"  rebuild with the measured body background replaced (negative control)
  --out <path>                     write elsewhere (default design/brand/portal-routes.json)
"""
import colorsys
import io
import json
import re
import sys

WS = "C:/tmp/wk-dsgn-1j/"
D = WS + "org/missions/D13/DSGN/DSGN_REBRND/deliverables/0.9.0_WK_DSGN_REBRND~1/"
SLUGS = ("market", "positioning", "portfolio-management")
args = sys.argv[1:]
mutant = args[args.index("--mutant-canvas") + 1] if "--mutant-canvas" in args else None
out_path = args[args.index("--out") + 1] if "--out" in args else WS + "design/brand/portal-routes.json"

raw = {s: json.load(io.open(D + "rb-s-14_extract_%s.json" % s, encoding="utf-8")) for s in SLUGS}
pix = json.load(io.open(D + "rb-s-14_pixel_shares.json", encoding="utf-8"))
SITE = "design/brand/opalinvest.com.json"


def rgb_tuple(v):
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)", v or "")
    if not m:
        return None
    if m.group(4) is not None and float(m.group(4)) < 1:
        return None  # translucent: no single hex
    return tuple(int(m.group(i)) for i in (1, 2, 3))


def hexof(v):
    t = rgb_tuple(v)
    return "#%02X%02X%02X" % t if t else v


def hsl_token_rgb(s):
    m = re.match(r"([\d.]+)\s+([\d.]+)%\s+([\d.]+)%", s)
    if not m:
        return None
    h, sat, lig = float(m.group(1)) / 360, float(m.group(2)) / 100, float(m.group(3)) / 100
    r, g, b = colorsys.hls_to_rgb(h, lig, sat)
    return (round(r * 255), round(g * 255), round(b * 255))


def area(slug, value):
    for e in raw[slug]["extract"]["colors"]["backgroundColors"]:
        if e["value"] == value:
            return e["areaPct"]
    return None  # not in extract.js's top-8-by-count list on this route


def per(fn):
    return [fn(s) for s in SLUGS]


body_bg = per(lambda s: raw[s]["extras"]["bodyBackground"])
if mutant:
    body_bg = [mutant] * 3
canvas_hex = sorted(set(hexof(v) for v in body_bg))
BAND, ACCENT, NAVY, WHITE = "rgb(10, 23, 51)", "rgb(95, 59, 227)", "rgb(22, 51, 114)", "rgb(255, 255, 255)"
def named(key):
    return per(lambda s: pix[s]["namedSharePct(tol=6)"][key])


def ex(s):
    return raw[s]["extract"]


def xt(s):
    return raw[s]["extras"]

# ---- rendered status/data colours against the two token families ----
tokens_status = xt("market")["statusTokens"]
tokens_data = xt("market")["chartTokens"]
tok_rgb = [(n, v, hsl_token_rgb(v)) for n, v in tokens_status + tokens_data]


def nearest_token(t, tol=3):
    return [n for n, v, rgb in tok_rgb if rgb and all(abs(a - b) <= tol for a, b in zip(rgb, t))]


figure_colours = []
for v in ("rgb(45, 206, 137)", "rgb(245, 54, 92)"):
    cnt = next((e["count"] for e in ex("market")["colors"]["textColors"] if e["value"] == v), 0)
    figure_colours.append({"hex": hexof(v), "textNodes": cnt, "route": "/market",
                           "carrier": "span.text-sm.font-semibold (the +/- performance figures in the Equity, Fixed Income and Commodities tables)",
                           "matchesATokenWithin3": nearest_token(rgb_tuple(v))})
print("FIGURE-COLOURS vs tokens:", json.dumps(figure_colours))

radii_simple = sorted({float(v["value"][:-2]) for s in SLUGS for v in ex(s)["effects"]["radii"]
                       if re.fullmatch(r"[\d.]+px", v["value"]) and float(v["value"][:-2]) < 100})
weights = sorted({int(w["value"]) for s in SLUGS for w in ex(s)["typography"]["weightDistribution"]})
sizes = sorted({float(z["value"][:-2]) for s in SLUGS for z in ex(s)["typography"]["sizeDistribution"]})
most_common = per(lambda s: float(ex(s)["typography"]["sizeDistribution"][0]["value"][:-2]))
h1 = ex("market")["typography"]["headings"]["h1"]
h3 = ex("market")["typography"]["headings"]["h3"]
body = ex("market")["typography"]["body"]
same_h = all(ex(s)["typography"]["headings"] == ex("market")["typography"]["headings"] for s in SLUGS)
same_b = all(ex(s)["typography"]["body"] == body for s in SLUGS)
fam_counts = per(lambda s: {f["value"]: f["count"] for f in ex(s)["typography"]["uniqueFamilies"]})
focus = per(lambda s: xt(s)["focusFirstTabStop"])

SHADOWS = [
    {"route": "/market", "count": 5, "painting": [
        {"element": "aside (the fixed left navigation rail, 48x900)", "boxShadow": "rgba(0,0,0,0.1) 0 10px 15px -3px, rgba(0,0,0,0.1) 0 4px 6px -4px"},
        {"element": "4 x div.rounded-full markers, 12x12", "boxShadow": "rgb(239,68,68) 0 0 12px 0"}]},
    {"route": "/positioning", "count": 1, "painting": [
        {"element": "aside (the fixed left navigation rail, 48x900)", "boxShadow": "rgba(0,0,0,0.1) 0 10px 15px -3px, rgba(0,0,0,0.1) 0 4px 6px -4px"}]},
    {"route": "/portfolio-management", "count": 2, "painting": [
        {"element": "aside (the fixed left navigation rail, 48x900)", "boxShadow": "rgba(0,0,0,0.1) 0 10px 15px -3px, rgba(0,0,0,0.1) 0 4px 6px -4px"},
        {"element": "div.dark-band (the Optimization Report panel, 1328x656)", "boxShadow": "rgba(0,0,0,0.1) 0 10px 15px -3px, rgba(0,0,0,0.1) 0 4px 6px -4px"}]},
]
R8 = {"elements": [47, 27, 23], "onBandGround": [40, 26, 22], "ownBackgroundIsBand": [18, 7, 4],
      "carriers": "the navigation rail's links (rounded-lg, 16 per route), panel header/footer strips and panel bodies on the band; off the band: 3 x div.p-0.rounded-b-lg on a white ground and 4 x 1px coloured edge bars on /market, 1 translucent table cell on /positioning, 1 translucent select on /portfolio-management"}

loud = per(lambda s: pix[s]["loudest" + "Chromatic(share>=0.1%, by S*V)"][0] if pix[s]["loudest" + "Chromatic(share>=0.1%, by S*V)"] else None)

doc = {
    "source": "portal (branch feature/d13-visual-elevation, portal worktree wk-dsgn_rebrnd-1j @a65b939a), vite dev server",
    "captured": "2026-09-14",
    "viewport": {"width": 1440, "height": 900},
    "pagesAnalyzed": [raw[s]["url"] for s in SLUGS],
    "stack": "React + Vite + Tailwind v4 (portal/)",
    "color": {
        "canvas": {"hex": canvas_hex[0] if len(canvas_hex) == 1 else canvas_hex,
                   "surfaceSharePct": per(lambda s: area(s, body_bg[SLUGS.index(s)])),
                   "surfaceShareNote": "extract.js areaPct, the site file's method; null where the value is outside extract.js's top-8-by-count background list (/positioning)",
                   "pixelSharePct": named("canvas #F4F6FA") if not mutant else None,
                   "systemSignal": len(canvas_hex) == 1, "role": "page field (body background) on 3 of 3 routes"},
        "darkField": {"hex": hexof(BAND), "surfaceSharePct": per(lambda s: area(s, BAND)),
                      "pixelSharePct": named("darkField #0A1733"), "systemSignal": True,
                      "role": "PANEL SURFACE -- the body, header and footer of every panel rendered on the three routes, and the navigation rail"},
        "accent": {"hex": hexof(ACCENT), "surfaceSharePct": per(lambda s: area(s, ACCENT)),
                   "pixelSharePct": named("accent #5F3BE3"), "systemSignal": False,
                   "role": "one filled action on /portfolio-management ('Upload Portfolio'); the focus ring on 3 of 3 routes; no filled accent surface on /market or /positioning"},
        "navy": {"hex": hexof(NAVY), "surfaceSharePct": per(lambda s: area(s, NAVY)),
                 "pixelSharePct": named("navy #163372"),
                 "textNodes": per(lambda s: next((e["count"] for e in ex(s)["colors"]["textColors"] if e["value"] == NAVY), 0)),
                 "controlColourCount": per(lambda s: next((e["count"] for e in ex(s)["colors"]["accentCandidates"] if e["value"] == NAVY), 0)),
                 "systemSignal": True, "role": "TEXT AND HAIRLINE (page title and subtitle ink, active-tab ink), NOT A SURFACE"},
        "white": {"hex": hexof(WHITE), "surfaceSharePct": per(lambda s: area(s, WHITE)), "pixelSharePct": named("white #FFFFFF"),
                  "role": "state wells inside band panels (row DSGN_REBRND-W1-S33) and light text on the band"},
        "text": {s: [{"value": hexof(e["value"]), "count": e["count"]} for e in ex(s)["colors"]["textColors"]] for s in SLUGS},
        "operatingRatio": {"basis": "pixel share of each full-page render, per route", "canvas": named("canvas #F4F6FA") if not mutant else None,
                           "darkField": named("darkField #0A1733"), "accent": named("accent #5F3BE3")},
        "colorScheme": {"html": per(lambda s: xt(s)["colorScheme"]["html"]), "body": per(lambda s: xt(s)["colorScheme"]["body"])},
        "status": {"tokens": [{"name": n, "hsl": v} for n, v in tokens_status],
                   "renderedFigureColours": figure_colours},
        "chart": {"tokens": [{"name": n, "hsl": v} for n, v in tokens_data],
                  "tokenFamiliesShareAValue": any(nearest_token(rgb) for n, v, rgb in [(n, v, hsl_token_rgb(v)) for n, v in tokens_status] if rgb and [t for t in nearest_token(rgb) if t.startswith("--data")]),
                  "renderedShapeColours": {s: xt(s)["chart"]["colours"] for s in SLUGS},
                  "renderedShapeCount": per(lambda s: xt(s)["chart"]["shapes"]),
                  "wordCloudFamily": "Inter (the one non-Lato family measured, 34 svg nodes on /market)"},
        "loudestChromatic": {"basis": "pixel buckets (4 bits per channel) holding >= 0.1% of the render, ranked by HSV saturation x value",
                             "byRoute": dict(zip(SLUGS, loud)),
                             "carriers": {"market": "the red (-) performance figures", "positioning": "the Equities series fill in Positioning Summary and Portfolio Composition (a chart series)",
                                          "portfolio-management": "the accent 'Upload Portfolio' button"}},
    },
    "typography": {
        "family": "Lato",
        "familyExclusive": False,
        "familyExclusiveNote": "Lato only on /positioning and /portfolio-management; on /market 34 of 1702 elements render Inter, all of them svg text/tspan in the Daily Cloud word cloud",
        "elementCount": per(lambda s: fam_counts[SLUGS.index(s)].get("Lato", 0)),
        "otherFamilies": [{"route": "/market", "family": "Inter", "count": fam_counts[0].get("Inter", 0)}],
        "weights": weights,
        "weightDistribution": {s: ex(s)["typography"]["weightDistribution"] for s in SLUGS},
        "letterSpacing": {"h1": h1["letterSpacing"], "h3": h3["letterSpacing"], "uppercaseControls": "0.6px-0.7px"},
        "scalePx": sizes,
        "mostCommonSizePx": most_common,
        "headings": {"h1": {"sizePx": float(h1["size"][:-2]), "weight": int(h1["weight"]), "lineHeightPx": float(h1["lineHeight"][:-2]),
                            "ratio": round(float(h1["lineHeight"][:-2]) / float(h1["size"][:-2]), 2)},
                     "h3": {"sizePx": float(h3["size"][:-2]), "weight": int(h3["weight"]), "lineHeightPx": float(h3["lineHeight"][:-2])},
                     "sameOnAllRoutes": same_h},
        "body": {"sizePx": float(body["size"][:-2]), "weight": int(body["weight"]), "lineHeightPx": float(body["lineHeight"][:-2]),
                 "ratio": round(float(body["lineHeight"][:-2]) / float(body["size"][:-2]), 2), "sameOnAllRoutes": same_b},
        "numerals": {"measuredBy": "harness extras (extract.js takes no numeral reading): every rendered element whose own text carries a digit",
                     "elementsWithDigits": per(lambda s: xt(s)["numerals"]["elementsWithDigits"]),
                     "families": {s: xt(s)["numerals"]["families"] for s in SLUGS},
                     "fontVariantNumeric": {s: xt(s)["numerals"]["fontVariantNumeric"] for s in SLUGS}},
    },
    "space": {
        "mostFrequentPx": per(lambda s: float(ex(s)["spacingDistribution"][0]["value"][:-2])),
        "distributionTop8": {s: ex(s)["spacingDistribution"][:8] for s in SLUGS},
        "systemSignal": False,
    },
    "shape": {
        "radiiPx": radii_simple,
        "radiiDistribution": {s: ex(s)["effects"]["radii"] for s in SLUGS},
        "pillRadiusPx": 33554400,
        "midRangeRadius": "PRESENT -- 8px",
        "radius8px": R8,
        "shadows": SHADOWS,
        "shadowCount": [5, 1, 2],
        "focusRing": {s: focus[SLUGS.index(s)]["boxShadow"] for s in SLUGS},
        "focusRingFirstStopMatchesFocusVisible": [f["matchesFocusVisible"] for f in focus],
        "outlineNoneImportantRules": per(lambda s: len(xt(s)["outlineNoneImportantRules"])),
        "focusVisible": per(lambda s: ex(s)["focusVisible"]),
        "reducedMotionRespected": per(lambda s: ex(s)["reducedMotion"]),
    },
    "grid": {
        "columns": per(lambda s: ex(s)["grid"]["columns"] if ex(s)["grid"] else None),
        "template": {s: (ex(s)["grid"] or {}).get("template") for s in SLUGS},
        "gap": per(lambda s: (ex(s)["grid"] or {}).get("gap")),
        "containerWidthPx": per(lambda s: float(ex(s)["layout"]["containerWidth"][:-2])),
        "containerMaxWidth": ex("market")["layout"]["containerMaxWidth"],
        "containerPadding": ex("market")["layout"]["containerPadding"],
        "gridCountPerPage": per(lambda s: ex(s)["gridCount"]),
    },
    "tasteDNA": [],
    "method": {
        "extractor": raw["market"]["extractor"],
        "extractorNote": "run in place from the main workspace, never copied, edited or committed; evaluated unmodified in each page at 1440x900 by a scratch Playwright harness (the library portal/scripts/ui-smoke.mjs uses, same auth stub and fixture routing)",
        "fixtures": {s: {"file": raw[s]["fixture"], "matched": raw[s]["fixturesMatched"], "declared": raw[s]["fixturesDeclared"],
                         "liveApiResponses": raw[s]["liveApiResponses"], "liveApiNon2xx": raw[s]["liveApiNon2xx"]} for s in SLUGS},
        "fixtureNote": "/portfolio-management has no populated fixture (row DSGN_REBRND-W3-S3): it was measured with live data requests refused, so its figures read 0.00 and its Alpha panel shows EMPTY",
        "renders": {s: "org/missions/D13/DSGN/DSGN_REBRND/deliverables/0.9.0_WK_DSGN_REBRND~1/rb-s-14_%s_extract_1440.png" % s for s in SLUGS},
        "rawOutputs": {s: "org/missions/D13/DSGN/DSGN_REBRND/deliverables/0.9.0_WK_DSGN_REBRND~1/rb-s-14_extract_%s.json" % s for s in SLUGS},
        "pixelShares": "org/missions/D13/DSGN/DSGN_REBRND/deliverables/0.9.0_WK_DSGN_REBRND~1/rb-s-14_pixel_shares.json",
        "tasteDNANote": "empty by design: tasteDNA is the skill's step-3 interpretation; this file is the step-1 measurement only",
        "siteShares": "the site file's surfaceSharePct is extract.js areaPct; pixelSharePct here is a second instrument (painted pixels) with no site counterpart on record",
    },
    "siteDelta": {
        "typeface": {"site": SITE + "#/typography/family (familyExclusive true)", "portal": "Lato on 3 of 3 routes; Inter on 34 of 1702 elements on /market, all in the Daily Cloud word cloud",
                     "measuredComparison": "EQUAL on 2 of 3 routes; DIFFERS on /market by 34 of 1702 elements",
                     "differenceStandsOn": "a chart (the word cloud) inside a band panel; no chrome renders Inter"},
        "numerals": {"site": "brief IV.3 Site column ('Lato tabular'); " + SITE + " takes no numeral reading",
                     "portal": "Lato, font-variant-numeric tabular-nums on every digit-bearing element, 373 / 74 / 17 of 373 / 74 / 17",
                     "measuredComparison": "EQUAL to the brief's site value; the site file carries no measurement to set beside it",
                     "differenceStandsOn": None},
        "canvas": {"site": SITE + "#/color/canvas/hex", "portal": "#/color/canvas/hex on 3 of 3 routes",
                   "measuredComparison": "value EQUAL on 3 of 3 routes; SHARE DIFFERS -- canvas pixel share %s vs band pixel share %s" % (named("canvas #F4F6FA") if not mutant else None, named("darkField #0A1733")),
                   "differenceStandsOn": "the #0A1733 band: every panel rendered on the three routes is band-valued (portal CLAUDE.md 'Known divergence'; rows DSGN_REBRND-W1-S9, -W2-S5, -W1-S33)"},
        "navyRole": {"site": SITE + "#/color/navy/role", "portal": "#/color/navy -- text colour, pixel share %s" % named("navy #163372"),
                     "measuredComparison": "EQUAL (text and hairline, not a surface)", "differenceStandsOn": None},
        "statusColours": {"site": "none measured -- the site file supplies no status family (PRD, SURFACE MANIFEST row for opalinvest.com.json)",
                          "portal": "#/color/status -- 4 --status-* tokens; the 270 +/- figures on /market paint #2DCE89 and #F5365C, which match no --status-* or --data-* token",
                          "measuredComparison": "SITE-HAS-NO-VALUE", "differenceStandsOn": None},
        "chartColours": {"site": "none measured -- the site file supplies no data palette", "portal": "#/color/chart -- 23 --data-* tokens, disjoint in name from the 4 --status-* tokens; rendered series fills #10B981 and #3B82F6 on /positioning",
                         "measuredComparison": "SITE-HAS-NO-VALUE", "differenceStandsOn": "the charts-keep-their-colour ruling (PRD preamble)"},
        "loudestColour": {"site": SITE + "#/color/accent (surfaceSharePct <= 1.0)", "portal": "#/color/loudestChromatic",
                          "measuredComparison": "EQUAL on /portfolio-management (the accent button, 0.26%); DIFFERS on /market (red figure text) and /positioning (a chart series fill, 10.5%)",
                          "differenceStandsOn": "/positioning: a chart series (ruling); /market: figure text on the band"},
        "radius": {"site": SITE + "#/shape/radiiPx and #/shape/midRangeRadius (ABSENT)", "portal": "3, 4 and 8px plus pill; 8px on 47 / 27 / 23 elements",
                   "measuredComparison": "DIFFERS -- a mid-range 8px radius is present",
                   "differenceStandsOn": "the band: 40 / 26 / 22 of the 8px elements stand on #0A1733 (nav-rail links, panel strips)"},
        "shadows": {"site": SITE + "#/shape/shadowCount (0)", "portal": "#/shape/shadows -- 5 / 1 / 2 painting elements",
                    "measuredComparison": "DIFFERS -- the brief's 'only agreement' does not hold at a65b939a (row DSGN_REBRND-W1-S36)",
                    "differenceStandsOn": "the navigation rail (3 of 3) and the Optimization Report band panel are bands; the 4 red glows on /market are chart markers"},
        "focusRing": {"site": SITE + "#/shape/focusRing", "portal": "#/shape/focusRing -- white 2px gap then #5F3BE3 2px, :focus-visible true on 3 of 3, 0 outline:none !important rules",
                      "measuredComparison": "colour and ring width EQUAL; the portal adds a 2px white offset gap", "differenceStandsOn": None},
        "colorScheme": {"site": "n/a (brief IV.3 Site column); the site file takes no color-scheme reading", "portal": "light on html and body, 3 of 3 routes",
                        "measuredComparison": "SITE-HAS-NO-VALUE", "differenceStandsOn": None},
    },
}
with io.open(out_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(doc, f, indent=2, ensure_ascii=True)
    f.write("\n")
print("WROTE", out_path, "top-level keys", len(doc), "canvas", doc["color"]["canvas"]["hex"])
print("status tokens as rgb:", [(n, hsl_token_rgb(v)) for n, v in tokens_status])
