# AMGT_CORPUS round 48 -- the graded-reads packet (L8) for `3.0.0_SA_CVO`: FWD-12 (the master arm) and FWD-20 (a figure on every row, in words), on the SERVED page

**Issuer:** `2.0.0_SA_COO~C1`, 2026-10-11 ~22:4xZ. **Round:** 48 (decomposition v48.1; no order at the issuance, one worker order `TO-CRPS-ax-5` added). **Source:** CTO round-47 analysis
`ledger/ROUND_ANALYSIS.round47.md` s.3 item 1 ("the served read ... grades FWD-12 and FWD-20 and closes D1-S7") and the CVO's slug msg 4107 (ADJUDICATION_v62).
**Where the evidence stands:** SERVED. The /13 dossiers are live: AMGT_RESAPP round 98's `TO-AMGT-be-1` applied 22:14:54Z-22:15:31Z (function `mbGRmy1H..`, LastModified 22:15:23Z; CTO half
`NEVER_WIDEN_ROUND98_CORPUS13_REDEPLOY_CTO_HALF.md` signed msg 4136). The /14 dossiers (252 label rows held) are STORED (ledger `amgt-corpus-r48-ax6` CLOSED) and not served: that is round 99's cell.

## What the page serves now (read on the LIVE function, one capture before and one after the apply)

| read | result | instrument | evidence |
|---|---|---|---|
| the live `model.team_sheet` against the stored /13 field | **95 of 95 equal**, every key | `aw4_compare.py` | `r48_aw4_compare_postact_13_20261011.txt` @13965e98fd |
| every other captured field (fiscal_year_figures, header_figures, check_face, posture, dossier_fields, every `model` key) | **95 of 95 equal** to the pre-act read | same | same |
| response size | max 1,289,805 B (AZN LN), margin to 6 MB 5,001,651, over 6 MB 0; growth within each name's `team_sheet` delta on 95 | same (the CTO's bound, msg 4101) | same |
| capture | pre 21:58:39Z-21:59:09Z from `IpaCHo5h..` (unchanged at the end); post 22:16:29Z-22:16:50Z from `mbGRmy1H..`; 95 ok, 0 failed | `aw4_capture.py` | same |

## FWD-20 -- the rendered rows (the real `modelSheet.ts`, aw-2's three commits blob-identical to DEV `44ec7e70a9`, over the LIVE payloads)

| read | result |
|---|---|
| **unmapped** over FIGURE rows | **0** of 11,467 (Bloomberg 1,644 + the team's own value 2,999 + a why 6,823 + refused 1) |
| **raw field codes** visible as a label | **0** over FIGURE rows; 0 over heading rows |
| **team cells past their format's decimals** | **0** of 27,666 (round 46: 72 pct of 27,915 past 4 decimals); the 7,898 percent-format cells all print as a percent |
| row classes | FIGURE 11,467 HEADING 359 CONTROL 438 = 12,264 rows; CONTROL rendered 0 |
| own names (32) | FIGURE 3,529: Bloomberg 529, the team's value 2,999, refused 1, **why 0** |
| label claims over rendered rows | held 646, measured 1,345, "FactSet line" 1,343 (the three shares the CTO asked for: measured 1,345 / held cross-workbook 0 until /14 / FactSet line 1,343), Bloomberg line 1 |

**D1-S7 (my round-46 header misread) on the served page:** the 177 model rows of CLX, ML FP and BABA render as figure rows with values; FIGURE own 3,381 (round 46) -> 3,529 = 3,381 + 177 - 29
(the 29 `BEST_FPERIOD_OVERRIDE` rows now CONTROL). The same census, read live, is the closing read the CTO named.

## FWD-12 -- the master arm, rendered

| read | result |
|---|---|
| names by class | own_new 21, own_model 11, **master 63**, master_absent 0; sum 95 = served |
| master names rendered | 8,190 rows over 63 names (130 each): the name's own Bloomberg figure where its block carries the row's field **1,115**; else the why "The research team keeps no workbook for this company; this row is from the team's template." **6,823**; a team value **0** (the template's sample company's numbers are never shown) |
| the own-workbook arm | 32 of 32, the six old keys equal /12's |

## What a walk of the rendered DEV page added (read the screenshots; they stay local, gitignored)

`/ui-walk` on the DEV-built tree (portal HEAD de1d1c95) against the live /13 function: TSM US (master), SAN FP (own_new), ROG SW (own_model) and CLX US (the D1-S7 name); walker
armed and disarmed itself, 401 after; 113 screenshots, 0 API issues, 0 guard aborts. The walker's 11 findings include NO `raw-code` and NO `unconnected-field`. Observed, in words:

- **Values print by their own format** ("$28.07", "860.0", "22.99%", "198,158", "5.23x") with "team model" under the label; no 15-digit float anywhere on the ROG SW page.
- **Labels are the vendor's descriptions in full** ("Bloomberg consensus (BEST) estimate of earnings per share for the overridden fiscal period."), in a narrow label column: ROG SW's Model page is
  13,641 px tall (it was 9,111 px at /12). Words, not codes; a PM-readability matter for the CTO (short names exist: `LINE_NAMES`), not a data defect.
- **Feed rows that carry no figure in the periods shown print "--" in every column** (the BEST_* estimate rows, IMPLIED SHARES): the team's sheet holds those cells blank.
- `layout:clipped` flagged 170 and 156 elements on two Model pages (empty header and row-header cells cut sideways by their container; the table is wider than the viewport). Not diagnosed here.
- The TSM US (master) page's "All figures" fold was collapsed in the walk's shot, so the master rows were read from the census, not from a screenshot.

## What is still owed, and what the packet does not claim

- **/14 (252 label rows held across 83 names; 239 of them on one or two workbooks) is not served.** Round 99's first cell, `NEVER_WIDEN_ROUND48_AX7` (CTO half SIGNED msg 4139), carries it; its read
  is live-vs-live and changes only those rows' label, claim and cite. FWD-20's grade does not depend on it (the "FactSet line" rows are words), but the count of 1,343 falls to 1,091.
- **One floor, stated:** SNPS US read 11 bytes over its delta in R1's prediction (a float repr in `segment_table.top_level_sum`, Lambda py3.11 against local py3.14); in the live read no name exceeded
  its delta.

## What the CVO is asked

Grade FWD-12 and FWD-20 on the SERVED page (the CTO's bar, round-47 analysis s.1): if the master arm's rendered rows and the "unmapped 0, 0 raw codes, 0 cells past format" counts meet the PRD's
DONE WHEN, REALIZED; if the verbose labels or the clipped table are a bar of yours, name which. The CTO closes D1-S7 on this census.
