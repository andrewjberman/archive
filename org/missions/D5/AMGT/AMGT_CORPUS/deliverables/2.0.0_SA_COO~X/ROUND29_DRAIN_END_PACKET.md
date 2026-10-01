# AMGT_CORPUS round 29 -- drain-end packet (L8 input) to `3.0.0_SA_CVO~Z`

**Issuer:** `2.0.0_SA_COO~X`. **Decomposition:** v29.0 @`3168bccb85` on the round-28 analysis @`bd50135e57` (rulings 1-3).

## 1. The cell

| cell | state | issuer re-grade (pins read by blob at portal c8119301) |
|---|---|---|
| `CRPS-ae-1` the Model sheet reads like the analyst's | complete; drained `bb5bb5ceba` | face29.cjs 6/6 (144 cells over 15 printed rows; round-28 face.cjs 9/9 and sheet.cjs 6/6 inside it); bound 4/4; tsc -b rc 0; proof VALID |

**What changed on the face (all display-only; `data-model-cell` and `data-full-value` keep the full served value):**
1. The subtitle reads "Reported figures and Bloomberg consensus estimates, from the model block". A spanning header,
   "Consensus (Bloomberg)", sits above 2026E-2028E.
2. Each row has one type, declared in `modelSheet.ts`:
   - millions: 0 dp with separators (EBITDA `8,416 | 12,391 ... 4,343 | 8,498 | 12,322`);
   - per-share: 2 dp (Revenue/Sh `147.12`);
   - multiples: 1 dp + `x`;
   - percent: 1 dp + `%` (Dividend yield `3.6% ... 0.0% | 0.1% | 0.6%`).
3. "Figures in USD" appears once above the sheet. It comes from the header's `EQY_FUND_CRNCY`, then `CRNCY`. Row labels read
   "(per share)", "(millions)", "(%)" and "(multiple)". BA's Revenue/Sh, EPS, BVPS and EBITDA carry `*` (no measured currency on
   their figures), and exactly one footnote line reads "* currency not stated by the source for marked rows".
4. Harness re-anchor (necessary): `modelPattern` `negative_values_signed` now reads the formatted text through the same
   `formatSheetValue`. The floor stays at 12; `tabs` needed no edit.

**Portal:** chain c8119301, merged with DSGN's DEV 03311745 in the worktree (1f059ad1). Local portal DEV moved by fast-forward
03311745 -> 1f059ad1. The full page suite reads 15 of 16; `posture.harness.cjs` is RED on DEV too. Push state: LOCAL (MSTR
pushes).

## 2. Rows

| row | class | state |
|---|---|---|
| `Z-W1-S28` | OBSERVATION, ARMED | **disarmed by `Z-S76` `c12a0d6ffb` (issuer ruling).** BEST_DIV_YLD's values ARE percent: BA consensus DPS / price 196.8 x 100 = 0.00254, 0.14533, 0.60315 = the served values. The page's percent print is correct. Only the producer's unit LABEL "DECIMAL" is wrong, which is a candidate enrichment item |
| `Z-S74` | OBSERVATION, INERT | carried |

## 3. The ONE REAL RUN

`/ui-walk --route /security-analysis --security BA`, 09:31-09:34Z (`tmp/ui-walk/20261001T093108Z`). It ran on the walk checkout
94adface, which carries DEV 1f059ad1 (MSTR merged it at my ask). Vite served the round-29 ModelTab, confirmed by module fetch.
ARM and DISARMED were posted to `0.0.0_AB_MSTR~Z`, and the post-disarm login was REFUSED. **Looked at, `030-BA-Model.png`:**
- "Reported figures and Bloomberg consensus estimates, from the model block" sits under MODEL. "Figures in USD" appears once
  above the sheet. "CONSENSUS (BLOOMBERG)" spans 2026E-2028E.
- Every figure is at its row's precision:
  - EPS 7.92 ... 2.49 | -0.83 | 3.91 | 8.02;
  - P/E 14.7x ... 21.8x | -- | 50.3x | 24.6x;
  - ROE 140.8% / 684.0% / 1,048.6%;
  - Diluted shares 644 ... 762;
  - EBITDA 8,416 ... 6,752 | 4,343 | 8,498 | 12,322;
  - Dividend yield 3.6% ... | 0.0% | 0.1% | 0.6%.
- Revenue/Sh*, EPS*, BVPS* and EBITDA* carry the mark, with one footnote line below the sheet. No "currency not stated"
  appears beside any row.
- **Still on the face (round-28 packet item 2, not ruled in round 29):** "147 of 342 fiscal figure(s) on the block rendered; 0
  sheet row(s) not in the pack". It reads as a loss now that Other lines leave by design, and "not in the pack" presupposes a
  pack. A candidate enrichment item, together with Z-S76's unit label.

## 4. Judgment for L9

- **`CRPS-ae-1` AC4:** the sheet reads like the analyst's. Grade it on
  `tmp/ui-walk/20261001T093108Z/shots/030-BA-Model.png` (site Z, gitignored, local only).
