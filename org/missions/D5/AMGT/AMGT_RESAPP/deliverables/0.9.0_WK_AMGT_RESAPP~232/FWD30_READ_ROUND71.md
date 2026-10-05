# FWD-30 page-against-export read, round 71 (AMGT-au-2, 0.9.0_WK_AMGT_RESAPP~232)

Read, classified and NOT graded: the grade of FWD-30 is the CVO's at L9. Instrument: the repaired copies in `grader/` (page_render.cjs: GraphicCard, HeroGraphic+PanelEyebrow+ICON_GLOW, useCollectedChatter stubs, real PageEnd and dateUtils (row Z-W232-S1); sweep.py: `self.years` reset at each header `<tr>`, `x` ratio suffix read). Page: portal DEV e6ab82ad rendered from the capture of the DEPLOYED `opal-amgt-scoped-api`; export: the deployed `print?format=rich` body of the same capture (`--served`). Run 2026-10-05, read_at 2026-10-05T16:10:36Z; TSV `fwd30_r71.tsv`; full diff output `ac1_diff_output.txt`.

## Run lines (verbatim, diff lines omitted)

```
population: LIVE research library C:\Users\Opal Bloomberg\OneDrive - Opal Capital\Shared - Documents\Asset Management\Research, 97 folders, read_at 2026-10-05T16:10:36Z
2/97 AMD_US_Equity NOT_OK FIGURES+ABSENCES+CASES differ
3/97 ASML_NA_Equity NOT_OK FIGURES+ABSENCES+CASES differ
13/97 BA_US_Equity NOT_OK FIGURES+ABSENCES+CASES differ
15/97 Brookfield Corporation BN CA UNIDENTIFIED (identity does not resolve; not graded)
served over 3 of 97 folders: OK 0, NOT_OK 3, CAPTURE_FAILED 0
cases over 3 of 3 compared names: page=0 rich=9 same=0 missing=0 extra=9
unidentified folders (1 of 97): Brookfield Corporation BN CA
value facts over 3 compared names: compared=1674 differ=0; value-unchecked (identity only, the page carries no value attribute)=19; digits compared, scale unchecked (export unit UNRESOLVED)=0
FWD-30 GRADE: equal 0 of 3 identified names; values equal 3 of 3; unidentified 1 of 97 folders; keyed on: data-attributes
exit=1
```

## Per-name counts by class

| Class | BA_US_Equity | AMD_US_Equity | ASML_NA_Equity | Product or grader |
|---|---|---|---|---|
| FIGURES page-only (fiscal, 2026E-2028E) | 20 | 21 | 21 | PRODUCT |
| FIGURES export-only (fiscal, history 2016-2025) | 195 | 198 | 200 | PRODUCT |
| ABSENCES export-only (MODEL_NOTE) | 1 | 1 | 1 | PRODUCT |
| CASES export-only (Base, Downside, Upside) | 3 | 3 | 3 | PRODUCT |
| VALUE differences (of 1674 value facts compared over the 3 names) | 0 | 0 | 0 | was GRADER fault (x suffix), repaired |
| Value-unchecked (identity only, page carries no value attribute) | 19 over the 3 names | | | grader limit as written, not changed |

Cases: page=0 export=9 same=0 missing=0 extra=9. No ABSENCES or CASES fact is page-only. FIGURES export-only ARD_* rows: 0 (the page renders its ARD_GOODWLL, ARD_OTHER_INTANGIBLE_ASSET, ARD_SHARES_OUTSTANDING, ARD_TOTAL_CURRENT_LIABILITIES, ARD_TOT_ASSETS rows and they match the export).

## Class 1 -- FIGURES export-only: 20 block mnemonics the page does not render  (PRODUCT difference)

The same 20 mnemonics on all three names, every fiscal year 2016-2025 the block carries (195 / 198 / 200 figures): BS_CASH_NEAR_CASH_ITEM, BS_TOTAL_LIABILITIES, CAPITAL_EXPEND, CF_FREE_CASH_FLOW, CURRENT_EV_TO_T12M_EBITDA, EBITDA_TO_REVENUE, EQY_DPS, GROSS_MARGIN, IS_ADJUSTED_GROSS_PROFIT, IS_ADJUSTED_OPERATING_INCOME, IS_COMP_EPS_ADJUSTED, IS_DIL_EPS_CONT_OPS, IS_OPER_INC, NET_INCOME, OPER_MARGIN, PX_LAST, PX_TO_FREE_CASH_FLOW, RETURN_ON_CAP, RETURN_ON_INV_CAPITAL, SALES_REV_TURN.

Why PRODUCT: the served thesis fixture carries them (BA `fiscal_year_figures`: 686 figures, 80 mnemonics; PX_LAST, SALES_REV_TURN, NET_INCOME present), the export lists each under `## Fiscal year Y`, and the rendered BA page has 61 `data-model-row` rows, none of them these 20 (SALES_REV_TURN occurs once in the page HTML, in a cite id, not a row). `modelSheet.ts` builds three groups (Financial Summary, EBITDA and margin history, Valuation/return/balance-sheet lines) from named row specs; its former third group `Other lines the block carries` (`OTHER_LINES_TITLE`, `modelSheet.ts:27`) has no remaining use in `portal/src`, while the file's header comment still says every fiscal figure the block carries renders once. This is a page absence of figures the export carries, not a grader key fault: the grader reads the page's 10 history columns correctly for the 61 rows it has (value differences 0).

Examples, BA_US_Equity (5 of 195): BS_CASH_NEAR_CASH_ITEM 2016; CF_FREE_CASH_FLOW 2025; IS_ADJUSTED_GROSS_PROFIT 2016; IS_DIL_EPS_CONT_OPS 2025; PX_LAST 2024

Examples, AMD_US_Equity (5 of 198): BS_CASH_NEAR_CASH_ITEM 2016; CF_FREE_CASH_FLOW 2025; GROSS_MARGIN 2025; IS_DIL_EPS_CONT_OPS 2024; PX_LAST 2023

Examples, ASML_NA_Equity (5 of 200): BS_CASH_NEAR_CASH_ITEM 2016; CURRENT_EV_TO_T12M_EBITDA 2016; IS_ADJUSTED_GROSS_PROFIT 2016; IS_OPER_INC 2016; PX_TO_FREE_CASH_FLOW 2016

## Class 2 -- FIGURES page-only: 2026E-2028E forecast columns the export does not carry  (PRODUCT difference)

Seven row mnemonics on each name: BEST_CPS, BOOK_VAL_PER_SH, EBITDA, EQY_DVD_YLD_IND, IS_DIV_PER_SHR, IS_EPS, PE_RATIO; 3 years each (2026E, 2027E, 2028E), except BA PE_RATIO 2027E and 2028E only = 20 / 21 / 21. The page renders served `forecast_figures` in the sheet's E columns (FWD-21, `ModelTab.tsx:7-9`); the export has no forecast line at all, and its `## Model Notes` still reads `2026E, 2027E, 2028E: ABSENT -- the block carries fiscal years 2016 to 2025 only.` (Class 3).

Examples, BA_US_Equity (5 of 20): BEST_CPS 2026E; BOOK_VAL_PER_SH 2027E; EBITDA 2028E; IS_DIV_PER_SHR 2026E; IS_EPS 2027E

Examples, AMD_US_Equity (5 of 21): BEST_CPS 2026E; BOOK_VAL_PER_SH 2027E; EBITDA 2028E; IS_DIV_PER_SHR 2026E; IS_EPS 2027E

Examples, ASML_NA_Equity (5 of 21): BEST_CPS 2026E; BOOK_VAL_PER_SH 2027E; EBITDA 2028E; IS_DIV_PER_SHR 2026E; IS_EPS 2027E

## Class 3 -- ABSENCES export-only: the Model Notes line  (PRODUCT difference)

One per name: `('MODEL_NOTE', 'the block carries fiscal years 2016 to 2025 only.')`. The page no longer carries this absence (it shows the E columns, Class 2); the deployed export still states it, so the export states the opposite of what the page shows. Examples: this line, 3 of 3 names.

## Class 4 -- CASES export-only: Base / Downside / Upside  (PRODUCT difference)

The page renders no case lines (`ModelTab.tsx:7-8`, FWD-12 amended); the export's `## Model Cases` still carries three per name. All 9:

- BA_US_Equity: ('CASE', 'Base', 'ABSENT', 'forward EPS (FY1 BEST_EPS) is -0.834, not positive -- the case cannot be right')
- BA_US_Equity: ('CASE', 'Downside', 'ABSENT', 'methodology to be discussed with Andrew')
- BA_US_Equity: ('CASE', 'Upside', 'ABSENT', 'methodology to be discussed with Andrew')
- AMD_US_Equity: ('CASE', 'Base', 'SERVED', 'Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)')
- AMD_US_Equity: ('CASE', 'Downside', 'ABSENT', 'methodology to be discussed with Andrew')
- AMD_US_Equity: ('CASE', 'Upside', 'ABSENT', 'methodology to be discussed with Andrew')
- ASML_NA_Equity: ('CASE', 'Base', 'SERVED', 'Bloomberg consensus EPS (FY1, BEST_EPS) x adjusted trailing-median P/E (PX_LAST / IS_COMP_EPS_ADJUSTED)')
- ASML_NA_Equity: ('CASE', 'Downside', 'ABSENT', 'methodology to be discussed with Andrew')
- ASML_NA_Equity: ('CASE', 'Upside', 'ABSENT', 'methodology to be discussed with Andrew')

## Class 5 -- VALUE differences  (was a GRADER fault; none remain)

The 19 value differences the issuer measured were `x`-suffixed ratios (`117.6x` on the page against `117.5987` in the export): `read_number` stopped at the `x` (the regex lookahead `(?![A-Za-z])` refused it) and fell to a text comparison. After the one-token repair `x?` there are 0 differences over 1674 compared facts; BA's page carries 148 `x`-suffixed value cells. Controls on the repaired module: `values_agree('117.6x','117.6','')` True, `('117.6x','117.7','')` False, `('117.6x','1176','')` False. Separately, the header-row reset is what lines the cells up under their years: with it disabled the same copies print `compared=1495 differ=1348` and FIGURES export-only 772 over the 3 names (row Z-W232-S2).

## Grader faults standing after the repair

None found that move a count. Limits left as written (bound 2): 19 facts are identity-only (OFFICER rows' other cells, served CASE values: the page carries no value attribute); cites: no CITES class differs on any of the 3 names.

## For the L9 reader

FWD-30 DONE WHEN: the SAME figures, the SAME cites, the SAME absences, NOTHING in the export that is not on the page. Read per name: values equal on every compared fact (0 of 1674 differ) but the figure sets differ both ways (Classes 1 and 2), the absences differ (Class 3), cases appear only in the export (Class 4), no cite differs. Every remaining class is a PRODUCT difference; none is a grader fault. Run line: `FWD-30 GRADE: equal 0 of 3 identified names; values equal 3 of 3`. Not graded here.

