# RB7-AC5 -- REJECTION BY CLAUSE NUMBER: `/positioning`

**For:** `RB7-AC5` of `DSGN_REBRND.TO-RB-s-7`. It is graded at L9 by `3.0.0_SA_CVO`; no verdict here.
**Rejected by:** `0.9.0_WK_DSGN_REBRND~2`, against `portal/DESIGN.md` at portal commit
`000478c9655409eae13f357106d2f5277e16d628`.
**Page:** `/positioning`, rendered live from portal `dc1d8020`. The `src/` tree is byte-unchanged at
`000478c9`, whose only edit is `DESIGN.md`.
**Author's agreement:** OWED. See the last section. This record is the on-demand half; the second
actor's word is the other half.

## The page as rendered

Capture: `rb-s-7_positioning_1440.png` in this folder. It was taken with
`node scripts/ui-smoke.mjs positioning <png> --port 5182` from `C:/tmp/wk-dsgn-2b/portal`, rc=0,
VIEWPORT 1440x900 (full-page image 1440x1419), and read by this worker. The harness printed
`CANVAS: rgb(244, 246, 250)`. The words it prints after that, "(the silver -- light fg on this is
the footgun)", are a fixed suffix and not a reading, because rgb(244, 246, 250) is `#F4F6FA`.

The colours below are measured at the pixel (`.scratch/sample_png.py`, PIL, 13 points), not judged
by eye. Where a sample landed on a glyph, this record says so and does not count that point.

| point | (x,y) | measured |
|---|---|---|
| page field | (60,20) | `#F4F6FA` |
| POSITIONING SUMMARY panel body | (700,300) | `#0A1733` |
| PORTFOLIO COMPOSITION panel body | (700,750) | `#0A1733` |
| HOLDINGS BREAKDOWN panel body | (700,1230) | `#0A1733` |
| swatch beside "Fixed Income" | (128,282) | `#10B981` |
| swatch beside "Equities" | (128,334) | `#3B82F6` |
| Characteristics chip (active) | (1215,1142) | `#5F3BE3` |
| sidebar active item | (12,284) | `#5F3BE3` |
| avatar "D" | (12,870) | `#5F3BE3` |
| title accent rule | (81,80) | `#5F3BE3` |
| INT chip (active) | (1244,570) | `#10B981` |
| MODELS tab (active) | (1170,81) | `#7492F8` -- the sample hit the label glyph; not counted |
| Portfolio view chip (active) | (1095,168) | `#FFFFFF` -- the sample hit the label glyph; not counted |

## REJECTED -- the clauses

**Primary: C3 (surface role, Option A).** C3 reads: *"panel | `palette.surface` | `#FFFFFF` | every
container, marked by a 1px `palette.mutedTint` `#C4CBDB` hairline"* and *"band | `palette.darkField`
| `#0A1733` | ONE deliberate full-bleed band per page, never the default container"*, and it names
the violation: *"A dark card sitting on the light canvas ... or a second band on one page violates
this clause."* On this page all three containers are `#0A1733` cards sitting on the `#F4F6FA`
canvas, measured at three points. That makes the dark field the default container, and the page has
three dark containers where C3 allows one band. Panel titles are drawn in light ink, not the navy
C3 requires.

**Supporting clauses, each rejectable on its own:**

- **C8 (one persistent primary action per view).** C8 reads: *"`palette.indigo` `#5F3BE3` fills
  **exactly one** persistent element per view"*, and it is *"not a tab indicator ... not a chip
  fill"*. Four `#5F3BE3` fills are measured in one view: the Characteristics chip, the sidebar
  active item, the avatar and the title accent rule. The MODELS tab and the Portfolio chip look
  like purple fills too, but they are not counted because their samples landed on glyphs.
- **C4 (canon ladder, legibility bullet).** C4 says *"text naming a model is navy ink, never the
  canon hex"*. The chip row's model labels (UST, ST, LT, ULT) are drawn as text in the canon
  hues. This one is by eye: those labels were not sampled. **C4's order bullet is MET and is not
  part of this rejection.** The chip row reads UST, ST, INT, LT, ULT left to right, and the column
  heads read ULTRA SHORT-TERM through ULTRA LONG-TERM left to right.
- **C6 (the data family is the token file's, byte-equal).** The asset-class legend paints Fixed
  Income `#10B981` and Equities `#3B82F6`, measured. The token file's `data.assetClass` gives
  `#10B981` to equity and `#3B82F6` to fixedIncome. This is filed as row `DSGN_REBRND-W2-S11`; the
  row does not decide which carrier is intended.
- **C12 (the four empty states).** PORTFOLIO COMPOSITION and HOLDINGS BREAKDOWN each render a bare
  "No holdings data available". C12 says: *"A blank panel, a bare "No data" ... is a violation"*,
  and EMPTY must *"name what would appear here, and the one action that would create it"*.
  Qualifier: the harness ran with no data fixture. That is still the state C12 governs, because
  it is what this page renders when there are no holdings.

Not cited, so the rejection is not over-broad: C1 and C2 (the capture cannot show which font
rendered or whether figures are tabular, and it has no figures), C9 (no ratio is claimed here
beyond the measured hexes), C10, C11 and C12's split bullet (the page has no two-column split).

## THE AUTHOR'S AGREEMENT -- OWED

RB7-AC5 needs *"the author's agreement that the clause was violated"*. This worker cannot send or
receive messages, so it leaves the agreement for the page's author, routed by `2.0.0_SA_COO~D`.
Most likely that is the seat that owns `/positioning`'s panels in the current round (slot ~1's
`portal/src/` queue). One line per clause:

| clause | violation as recorded above | author's word (AGREED / DISPUTED + reason) | author serial | at commit |
|---|---|---|---|---|
| C3 | three `#0A1733` containers on the canvas; the dark field is the default container | owed | owed | owed |
| C8 | four measured `#5F3BE3` fills in one view | owed | owed | owed |
| C4 | model chip labels drawn in the canon hues | owed | owed | owed |
| C6 | asset-class legend colours reversed against the token file | owed | owed | owed |
| C12 | bare "No holdings data available" in two panels | owed | owed | owed |
