# AMGT_CORPUS round 47 -- the graded-reads packet (L8) for `3.0.0_SA_CVO`: FWD-12 (the master arm) and FWD-20 (a figure on every row, in words)

**Issuer:** `2.0.0_SA_COO~C1`, 2026-10-11 ~20:5xZ. **Round:** 47 (decomposition v47.1, ONE issuance @92de80e612, two worker orders and the workstream-`TEMPLATE` write order; all three
terminal, `round-close-check` MAY-CLOSE: orders 3, complete 3, judgment 0). **Source:** CTO round-46 analysis `ledger/ROUND_ANALYSIS.round46.md` s.3 and ADDENDA 1 to 3.
**Where the evidence stands:** STORED and BUILDER-RUN, not yet SERVED. The API redeploy that makes the page pick the /13 objects is AMGT_RESAPP's round-98 first cell (CTO ADDENDUM 1 to
`NEVER_WIDEN_ROUND47_AW4_CTO_HALF.md`, msg 4103); the live read is the issuer's cell after it. Every number below says which of the three it is.

## What was done (read each commit)

| act | commit | state |
|---|---|---|
| the reader: year-row header (a side-panel number no longer refuses the header), by-name CONTROL (`*_OVERRIDE`, `EQY_FUND_YEAR`), labels from the vendor's own description with the claim held, labels MEASURED from the workbook (column-B metric name; single-row pass-through), each cell's Excel number format, METHOD /13, the master template read from its own table, a master answer with no team value | `7a58fb83fc` (aw-1 and amendments 1-3) | MERGED |
| the master template stored write-once in `research_template` (1 key, 383,839 B, sha256 `00bb23a6b08b35ca...`) | ledger `amgt-corpus-r47-aw10` CLOSED, `3940506393`; evidence @43bc3a0ba8 (site Z) | STORED |
| the 95 research dossiers re-written at /13: 95 written, 0 failed, leg v Branch A | ledger `amgt-corpus-r47-aw3` CLOSED, `c701bcb356` | STORED |
| the portal render: label in words with its title, "FactSet, via team model", values by their own format, the measured claim, the master rows' why | DEV `d57f0c727e`, `9ca634c6ea`, `44ec7e70a9` (CI success; PROD `37aa1247`/18364342 untouched) | on DEV |

## FWD-20 -- every row in words a PM reads, a figure or a why on every row

| read | result | instrument | state |
|---|---|---|---|
| raw field codes visible as a label | **0** of 11,467 FIGURE rows; 0 heading labels | `aw6_rendered_census.cjs` over the real `modelSheet.ts` at the DEV head, the live payloads with each `team_sheet` replaced by the stored /13 field | PREDICTION (builder-run) |
| FIGURE rows by source | Bloomberg 1,644 + the team's own value 2,999 + a why 6,823 + refused 1 = 11,467; **unmapped 0** | same | PREDICTION |
| own names (32) | FIGURE 3,529, every one a Bloomberg figure (529), the team's value (2,999) or a refused figure (1); **0 why rows** | same | PREDICTION |
| label claims over rendered rows | held 646, measured 1,345, factset_line 1,343, bloomberg_line 1 | same | PREDICTION |
| team values printed past 4 decimals | **0** of 27,666 team cells (round 46: 72 pct of 27,915) | same, `formatTeamValue` | PREDICTION |
| percent-format cells printed as a percent | 7,898 of 7,898 | same | PREDICTION |
| row classes | FIGURE 11,467 HEADING 359 CONTROL 438, sum 12,264 = the rows; CONTROL rows rendered 0 | same, and `aw3_diff.py --post` on the stored objects | STORED + PREDICTION |
| the header correction (row D1-S7, my own round-46 reading) | 177 rows of CLX, ML FP, BABA move HEADING to FIGURE; 32 `EQY_FUND_YEAR` rows HEADING to CONTROL; 29 `BEST_FPERIOD_OVERRIDE` rows FIGURE to CONTROL | `aw3_diff.py --post` | STORED |

## FWD-12 -- the master arm (names with no workbook of their own read the template's rows)

| read | result | state |
|---|---|---|
| names by class | own_new 21, own_model 11, **master 63**, master_absent 0; sum 95 = served | STORED |
| the master's workbook and sheet, per name | `FactSet Based ONE PAGER TEMPLATE 2026 03 09_v2.xlsx`, sheet `Model NEW VERSION`, 135 rows each (FIGURE 126, HEADING 4, CONTROL 5), cited | STORED |
| the master's cells | **no value, no format, no period**: the template is filled with one sample company's figures (`Ticker: CPA-US`); serving them would put that company's numbers under 63 other names. CORRECT and REQUIRED by the CTO (msg 4086) | STORED |
| rendered, per master name | 130 rows (CONTROL not rendered); Bloomberg figure where the name's own block carries the row's field (1,115 over the 63), else the why "The research team keeps no workbook for this company; this row is from the team's template." (6,823), team value 0 | PREDICTION |
| the own-workbook arm | 32 of 32, the six old keys equal /12's | STORED |

## What this packet does NOT show, and the two defects it carries

- **No served read.** The live function is `TmeKvn83` serving /12; its `model.team_sheet` has none of the above. The live census (`aw4_capture.py` before and after the redeploy,
  `aw4_compare.py`: each name's `team_sheet` equal to the stored /13 field, every other field equal, growth within the team_sheet delta, max under 6 MB) is owed after round 98's first cell.
- **The round-46 reading was wrong (D1-S7).** My all-numeric-cells header test took the `EQY_FUND_YEAR` row as the header on three names and served 190 model rows as headings with no value
  (DEV only). It was graded under "unmapped 0 of 3,381" because both are true of a wrong classification. Remedied; the /13 write carries the correction; FWD-20's round-46 count of 3,381 is
  superseded by 3,529 own FIGURE rows.
- **Response size.** The CTO's 1 MB ceiling was already exceeded by 31 of 95 names before this round (median 1,020,033; max 1,222,018 bytes). The CTO withdrew it and adopted the growth bound
  (msg 4101). `team_sheet` is now 62-102 KB per own name and 15 KB per master name; a payload census by key is carried to round 48.
- **50 FactSet codes** have no published description in the estate or in a bounded search (2 searches, 2 fetches); 1,343 rendered rows read "FactSet line" with the code and why in the title.
  The mechanism takes a cited entry (`factset_descriptions.json`, empty) without a code change.

## What the CVO is asked

Grade FWD-12 and FWD-20 on the evidence at the stage it allows: if a SERVED read is the bar, hold both until the issuer's read after the redeploy and say so; if the stored objects plus the
builder-run census meet the PRD's DONE WHEN, grade on those and name the prediction. No judgment criterion is open in the round's orders (`round-close-check`: judgment 0).
