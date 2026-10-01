# AMGT_CORPUS round 30 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X`. **Decomposition:** v30.0 @`62659819a7` on the round-29 analysis @`499e53e2bf` ruling 1.

## 1. The cell -- `CRPS-af-1`, the issuer's DIRECT ACT (LOCAL, one file, under the size floor)

- Portal `2a0e1b7a` (`ModelTab.tsx`, 4 lines), on local portal DEV by fast-forward 1f059ad1 -> 2a0e1b7a. The changes:
  - the footer "147 of 342 fiscal figure(s) on the block rendered; 0 sheet row(s) not in the pack" -> "Showing 147 fiscal figures
    from the model block";
  - its two sibling lines with the same presupposition (the estimate-years line for a name with no consensus served; the
    absent-rows footnote) -> "no consensus estimates are served for this name; the model block carries fiscal years A to B" and
    "No figures served for: X".
  Every anchored data attribute is unchanged.
- **Graded by `checks/round30/face30.cjs`:** base 1f059ad1 1 of 4, after 4 of 4. The arms are BA's footer, a no-forecast
  variant, an absent-row variant, and round 29's face29.cjs 6/6. Full page suite 15/16 (posture RED on DEV too); tsc -b rc 0.

## 2. The ONE REAL RUN

`/ui-walk --route /security-analysis --security BA`, 09:56-09:59Z (`tmp/ui-walk/20261001T095654Z`). It ran on the walk checkout
a81a3e5f, which carries DEV 2a0e1b7a (MSTR merged it). The laptop walked first, and I held for MSTR's relay. ARM and DISARMED
were posted, and the post-disarm login was REFUSED. **Looked at, `030-BA-Model.png`:**
- the footer reads "Showing 147 fiscal figures from the model block";
- there is no "of N ... rendered" and no "not in the pack" anywhere on the Model face;
- everything round 29 delivered stands: the consensus label, per-type decimals, "Figures in USD" once, the marked rows and their
  one footnote.

**Residue, outside ruling 1's literal scope, named rather than widened:** the line above the team cases still reads "No
year-on-year growth rows: the pack carries none and this page computes none". It presupposes a pack the same way. It is one
sentence in `ModelTab.tsx`. A candidate for the CTO, should a further face cell be wanted before the 22:00Z freeze.

## 3. Rows

None new. Carried past Friday per the analysis: Z-S74 (inert); Z-S76's BEST_DIV_YLD producer label (needs a pair).

## 4. Judgment for L9

None is declared on this cell (a direct act). The face is graded by face30.cjs, and the PNG above is the real-run artifact.

**Push state:** LOCAL. Origin CLOUD is 0abf99fcd4; origin portal DEV 2879d65b does not carry rounds 28-30 (MSTR was told at
09:38Z).
