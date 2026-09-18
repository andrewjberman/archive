# DSGN_REBRND.TO-RB-s-4 -- ordered scales -- result (RESUME under Amendments 1 + 1a, REOPENED under Amendment 2)

## Amendment 2 round (2026-09-14) -- current state

The order was reopened on row `W1-S15`, and the issuer ruled that the CANON LOCK governs
`ReturnVolatilityScatter`'s `ULT_COLOR` / `LT_COLOR`. The act, and only this act:
`src/components/ReturnVolatilityScatter.tsx:121-122` set back to their pre-cell bytes at portal `dc1d8020`
(`'#ef4444'  // Red`, `'#3b82f6'  // Blue`). After the edit, `git diff --stat dc1d8020` on that file is
empty. Portal commit `a08497a5d22cf0993ee6b4f0bd6d0eac2c7c95ac` (1 file, +2/-2), LOCAL on
`wk-dsgn_rebrnd-1e`, on top of the issuer's merge `547d12fd`. Workspace base `fb274b50c6` carries
Amendment 2 and the issuer-upgraded `rb4-canon-check.py`.

Every mechanical criterion was re-run on the Amendment 2 tree:

| id | verdict | deciding line |
|---|---|---|
| RB4-AC1 | PASS-by-output | `rc=0` (tsc -b --noEmit) |
| RB4-AC2 | PASS-by-output | `CANVAS: rgb(244, 246, 250)` then `rc=0`; PNG read -- canon chips in duration order |
| RB4-AC3 | PASS-by-output | `CANVAS: rgb(244, 246, 250)` then `rc=0`; PNG read -- Fear & Greed arc a one-hue ramp |
| RB4-AC4R | PASS-by-output | `VERDICT: CANON-INTACT` (30 sites / 5 files, 5 of 5 rungs, lookahead 5, ARM-E 2 at :121/:122, ARM-B 2 of 2, ARM-D 4 of 4) |
| RB4-AC5 | RECORDED (judgment) | graded by `3.0.0_SA_CVO` at L9; the scatter is on neither graded route |
| RB4-AC6 | PASS-by-output | `VERDICT: ONE-HUE-RAMPED` (10 decls, 1 hue; 6 of 6 sentiment tokens) |

Controls for this round:
- **Mutant:** the upgraded checker was run over `git archive 547d12fd src`, the tree just before this
  round's edit. It printed `VERDICT: CANON-BROKEN`, and its only OFF-CANON lines are `:121` (#183B86) and
  `:122` (#2650AB).
- **Determinism:** each checker was run twice on the final bytes, and the outputs were identical (canon 12
  lines, ramp 3 lines).

**One gate refusal on the way, recorded here.** The first attempt to commit the `complete` flip was
REFUSED by `.tools/to-pipeline-gate.py` (`flips to 'complete' but its instance is NOT VALID (rc=1)`), while
manual `proof-of-spec-check` runs returned rc=0 both with the six ids and with the gate's own id-less argv.
Cause: the `/positioning` re-render is byte-identical to the capture already committed at `4202b447a8`, so git
had nothing to stage for it. Its `PENDING-THIS-COMMIT` pin therefore named a file the commit could not touch,
and the checker refuses that (CCX class) only when the instance is staged, which is why the manual runs passed.
Fix: the PNG is pinned to `4202b447a8` as COMMITTED. Nothing else changed, and the gate's own re-run is the
verdict.

No new surprise row: the act was exactly as stated and every premise held. Amendment 2 disarmed `W1-S13` and
`W1-S17`. `W1-S14` and `W1-S16` ride to L10.

---

## Amendment 1 round (2026-09-13/14) -- the record below is that round's, kept as written

Worker: `0.9.0_WK_DSGN_REBRND~1` (slot ~1). Workspace worktree `C:/tmp/wk-dsgn-1e`, branch
`wk-dsgn_rebrnd-1e` (base @1cceadbf81, carries the amended order and both issuer checkers). Portal worktree
`C:/tmp/wk-dsgn-1e/portal`, branch `wk-dsgn_rebrnd-1e`. Dev server on 5181 (never 5173).

## What the first instance did (carried, not redone)

Portal `0e87cb9f99` moved the duration ladder, and several non-canon ordered scales, onto one navy ramp.
Rows `W1-S13` (the retired RB4-AC4 could not see the ladder) and `W1-S14` (four writers of one encoding)
at workspace `f6aa9c7e19`. The old proof instance carried an RB4-AC4 FAIL. Amendment 1 retired RB4-AC4 and
ruled the ladder canon.

## What this instance did

1. **Reverted the four ladder writers to their pre-cell bytes** (`0e87cb9f99^`), whole-file, because each
   one changed in `0e87cb9f99` only for the ramp. Afterwards, `git diff 0e87cb9f99^` over the four files is
   empty (rc=0, no output):
   `holdings-shared.tsx` PORTFOLIOS, `HoldingsTab.tsx` BOOK_COLOR_CYCLE, `chartColors.ts` MODEL_COLORS (AGG
   keeps opalIndigo), `modelPortfolioColors.ts` MODEL_PORTFOLIO_COLORS and all aliases. The "- Red" / "- Blue"
   comments sit beside the hexes they name again. `inkOnRamp()` in HoldingsTab went back out with the
   revert. Its stated reason was legibility at the ramp's light end, and that end no longer exists. The
   active chip ink is white again, as it was before the cell. `FactorTilts/constants.ts` was already canon
   and was not touched.
2. **`aum.ts` getModelColor()**: the five legacy-keyed entries were moved onto canon (ULT #EF4444, LT #3B82F6,
   INT #10B981, ST #F59E0B, UST #F97316). The UST shadowing bug is fixed by trying the longest key first, so
   'Ultra Short-Term' no longer falls to the 'Short-Term' branch. The keys were NOT renamed; that is row `W1-S16`.
3. **Kept**, per the amendment: `--ramp-1..5`, the six `--sentiment-*` tokens, the Fear & Greed arc,
   EmotionalIntensityMeter, the TopicCloud stops, and the two ReturnVolatilityScatter benchmark colours.
   The scatter pair is row `W1-S15`: pre-cell they were exactly canon ULT red and LT blue, and the canon
   checker does not read their grammar.

Portal commit: `46d2bc59a1b5c57dc1d4d532ac3126f39fe2d658` (5 files, +61/-90), LOCAL on `wk-dsgn_rebrnd-1e`.

## Criteria (outputs verbatim in the proof instance)

| id | verdict | deciding line |
|---|---|---|
| RB4-AC1 | PASS-by-output | `rc=0` (tsc -b --noEmit) |
| RB4-AC2 | PASS-by-output | `CANVAS: rgb(244, 246, 250)` then `rc=0`; PNG read |
| RB4-AC3 | PASS-by-output | `CANVAS: rgb(244, 246, 250)` then `rc=0`; PNG read |
| RB4-AC4R | PASS-by-output | `VERDICT: CANON-INTACT` (23 sites / 4 files, 5 of 5 rungs, ARM B 2 of 2 OK, ARM D 4 of 4 OK) |
| RB4-AC5 | RECORDED (judgment) | graded by `3.0.0_SA_CVO` at L9 |
| RB4-AC6 | PASS-by-output | `VERDICT: ONE-HUE-RAMPED` (10 ramp decls, 1 hue '221'; 6 of 6 sentiment tokens on the ramp) |

Retired `RB4-AC4` was not run and is not an acceptance row (Amendment 1a).

## PNGs, read

- `rb-s-4_positioning_1440.png`: the book chips read UST orange, ST amber, INT green (active, white ink),
  LT blue, ULT red, left to right in duration order. The asset-class swatches (Fixed Income green,
  Equities blue) are unchanged. Holdings panels read "No holdings data available", which is the dev
  environment, not this cell.
- `rb-s-4_market_1440.png`: the Fear & Greed arc is one navy-blue ramp, not a rainbow. The U.S. Regime panel
  shows a 401 from the public API, and the page shows "Failed to fetch market returns". Both are environment
  data failures, not caused by this cell.

## Controls

- **Mutant:** `rb4-canon-check.py` was run against the pre-revert portal tree (`git archive 0e87cb9f99 src`
  into `.scratch/mut_prerevert`; neither repo mutated). It printed `VERDICT: CANON-BROKEN` with 18 OFF-CANON
  lines (aum.ts 5, modelPortfolioColors aliases 8, holdings-shared 5), both positional writers MISSING all five
  canon hexes, and both ARM-D arrays out of order. On the final tree the same checker prints `CANON-INTACT`,
  so the PASS discriminates. The same output shows the five multi-line canonical MODEL_PORTFOLIO_COLORS
  entries were never flagged while they were navy: row `W1-S17`.
- **Determinism:** each checker was run twice on the final bytes, with identical output.

## Rows filed on this order

`W1-S13` (BLOCKING, ARMED; retired criterion), `W1-S14` (OBSERVATION, ARMED; four writers), `W1-S15`
(OBSERVATION, ARMED; scatter pair vs the canon lock and the checker's blind grammar), `W1-S16` (OBSERVATION,
INERT; legacy-name holdouts for L10), `W1-S17` (OBSERVATION, ARMED; the canon checker cannot see the five
multi-line canonical entries in MODEL_PORTFOLIO_COLORS).
