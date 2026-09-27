# DSGN_IRPTV1.TO-IV-e-49 -- result (0.9.0_WK_DSGN_IRPTV1~30)

CTO 101649: `MIX_PIE`'s commodities (yellow500) and cash (amber500) landed in the same pie for a
partner whose mix includes cash and were not legend-distinguishable (UIR-44). Picked
`PALETTE.gray900` (#111827) for both `MIX_PIE.commodities` and `ASSET_CLASS.commodities`: the
highest-margin EXISTING palette token (measured CIEDE2000 dE00 = 30.07 against its closest
neighbour, `gray500`/"other") that clears the CTO's dE00 >= 20 bar against every `MIX_PIE`
colour, every `ASSET_CLASS` colour and every model primary in `modelPortfolioColors.ts`, and the
only such token outside a hue family another class already owns (green7/8/900 = Fixed Income's
own sub-asset ramp, blue9/950 = Equity's, pink6/7/800 = Structured's).

## IVE49-AC1

`src/pages/AdvisorIntelligence/__tests__/iv-e-49.commodities-distance.test.ts` (new): CIEDE2000
(sRGB -> linear -> XYZ D65 -> CIELAB -> dE00) implemented from scratch (no new dependency).
4 tests: (1) reproduces a published CIEDE2000 reference pair (Sharma/Wu/Dalal 2005, pair #1) to
4 decimal places; (2) the OLD yellow500/amber500 pair measures below the bar (negative control,
9.8943 < 20); (3) `MIX_PIE.commodities === ASSET_CLASS.commodities`; (4) the new colour clears
dE00 >= 20 against every MIX_PIE colour, every ASSET_CLASS colour, and every model primary
(`MODEL_PORTFOLIO_COLORS` read directly; the 6 unexported `EXTENDED_MODEL_COLORS` primaries
discovered mechanically via `getModelColor`'s own public fallback, 60 deterministic probes
covering all 6 hash buckets). Measured minimum: dE00 = 30.0741 against `ASSET_CLASS.other`
(#6b7280). `VERDICT: COMMODITIES-DISTANCE-OK`.

## IVE49-AC2

`iv-e-46.class-readers.test.ts` gains the CTO-named assertion (`dE00(MIX_PIE.commodities,
MIX_PIE.cash) >= 20`, embedded CIEDE2000 computation independent of AC1's own copy) alongside
its pre-existing file-census test; both tests pass. `iv-e-46.composition-tags.test.ts` and
`iv-e-44.securities-map.test.tsx` (regression) both pass unchanged. Combined run: 4 pass, 0 fail
across 3 files.

## Surprise

`DSGN_IRPTV1-W30-S2` (workspace channel): two comments/data sites in `chartColors.ts`
(`SUB_ASSET_COLORS`'s "class base PALETTE.yellow500" comment, `getAssetClassTextColor`'s
`lightBackgrounds` array + WCAG doc table) still describe a commodities-yellow500 mapping the
class no longer produces. Left untouched: outside this cell's "no other existing colour value
changes" bound. Inert today only because the function's fallback happens to return the correct
white-on-dark text for the new (dark) replacement colour.
