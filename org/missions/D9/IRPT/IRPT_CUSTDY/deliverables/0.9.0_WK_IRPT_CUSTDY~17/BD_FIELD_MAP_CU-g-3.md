# BD field map of one 49 Financial client Performance Report (CU-g-3, FWD-9)

Worker `0.9.0_WK_IRPT_CUSTDY~17`, TO `IRPT_CUSTDY.TO-CU-g-3a`. Machine form: `BD_FIELD_MAP_CU-g-3.json` (same folder). **Field names and structure only: no client value, name, account number, date, holding or amount is in this file.** The PDF was read in place from outside the repo and never copied; `bd_leak_check.py` proves the claim (CU20-AC2).

## Denominator

The PDF has 32 pages (a cover, then 31 numbered pages) and **7 Run Report bases**: the cover plus the six sections its page header titles. The extractor (`bd_field_map.py`) found **49 fields**; the map has **70 rows** because a chart's series are read from the rendering (the charts are raster images with no text layer) and a class-hierarchy table is split into its total row and its class rows, which map differently (21 derived rows).

| Run Report base | pages | scope | extracted fields | rows | MAPPED | MISSING |
|---|---|---|---|---|---|---|
| Cover | 1 (1) | unnumbered | 4 | 4 | 4 | 0 |
| Portfolio Overview | 1 (2) | portfolio | 8 | 10 | 7 | 3 |
| Summary of Portfolio Accounts | 1 (3) | portfolio | 8 | 9 | 9 | 0 |
| Holdings Overview | 1 (4) | portfolio | 12 | 24 | 11 | 13 |
| Taxable Realized/Gain Loss Summary | 6 (5, 10, 17, 24, 27, 30) | account | 5 | 5 | 5 | 0 |
| Account Overview | 11 (6, 8, 11, 13, 15, 18, 20, 22, 25, 28, 31) | account | 8 | 10 | 7 | 3 |
| Gain/Loss Review by Account | 11 (7, 9, 12, 14, 16, 19, 21, 23, 26, 29, 32) | account | 4 | 8 | 4 | 4 |
| **Total** | 32 | | **49** | **70** | **47** | **23** |

The Run Report dialog (the screenshot) adds 10 parameters, counted apart: 4 MAPPED, 6 MISSING (section below).

## Reading

- **What Opal reads (47 rows MAPPED).** Every value, flow, gain, income, return and lot figure at account and household grain has an Opal source: `account_activity_daily` (beginning and ending value, contributions, withdrawals, realized, unrealized change, income), `account_return_daily` (daily value, flow and return), `account_lot_realized` and `account_lot_unrealized_daily` (cost basis, proceeds, term, gains) and the hop-3 producer `client_report_figures.py` (returns over QTD, YTD, 1Y and SI, market value, registration, holdings weight). Each row names the table and column, and its `reason` states the caveat (value basis, fee treatment, anchor).
- **What Opal does not read (23 rows MISSING), three causes:** (1) **18 rows: BD's classification tree.** The class and segment rows of the holdings and gain/loss tables, and the class shares of the allocation donuts, use BD's own tree (held only by BD); Opal classifies into six classes and holds no class-grain gain table. (2) **4 rows: benchmarks.** The four benchmark return rows and the benchmark lines of the performance chart; Opal has no benchmark return library (HAR teardown 4.3). (3) **1 row: month-to-date return.** A ruling, not a data gap: RULED_PERIODS is QTD, YTD, 1Y, SI, though the daily series holds the days.
- **Same name, not the same figure (flagged on the rows).** Value (BD adds its accrual), net additions and net gain (BD folds fees in), income (BD accrues, Opal books on receipt), contributions and withdrawals (Opal nets within a day), cost basis (Opal's in-kind and wash-sale rules), since-inception start (anchor rules). None of these was measured against this report's values: the map is structural, and a tie-out is the next cell's work.
- **BD sources by evidence.** `pull-code` rows name an endpoint and response field the estate's own code reads (`bd_adapter.py`, `opal-assets-bd49f-reporting-pull`); `har-teardown` rows are named only in `docs/research/bd_dashboard_teardown/BD_DASHBOARD_HAR_TEARDOWN_20260721.md` section 3.1 (activitySummary, capitalmarkets, costBasis response fields, the series arrays beyond the cumulatives); `inferred` rows are matched by field name; `read-from-rendering` rows are chart series a person read from the rendered page. No row's BD source is `UNKNOWN`: every figure has at least an inferred endpoint.
  Row counts by basis: har-teardown 20, inferred 5, pull-code 43, read-from-rendering 2.
- **Commonwealth.** FWD-9 asks where Commonwealth's history holds more than Black Diamond's feed. Commonwealth is the Cottonwood predecessor custodian (FWD-4); this report is a 49 Financial report whose Opal history is Schwab silver from the floor, so **no row of this map claims Commonwealth history**. The reverse holds for since-inception figures: BD can hold earlier history than Opal's Schwab floor, which the since-inception rows flag through the anchor rule.
- **Chart series are read, not extracted.** The PDF's charts (two on each overview page and two on the accounts summary) are raster images with no text layer, so the extractor lists each chart as one field and the series (legend entries, lines) were read from the rendering by the worker (basis `read-from-rendering`). Surprise row `IRPT_CUSTDY-W17-S1`.

## MISSING rows

| id | base | field | reason (short) |
|---|---|---|---|
| R005 | Portfolio Overview | Allocation by Asset Class [class shares] | BD classification tree (class and segment rows), held only by BD |
| R012 | Portfolio Overview | Benchmark: <benchmark> Return (Cumulative) | benchmark returns, held only by BD |
| R014 | Portfolio Overview | Portfolio Performance Last 12 Months [benchmark cumulative return lines (four)] | benchmark returns, held only by BD |
| R025 | Holdings Overview | Ending Value [class rows (two levels)] | BD classification tree (class and segment rows), held only by BD |
| R027 | Holdings Overview | Allocation [class rows (two levels)] | BD classification tree (class and segment rows), held only by BD |
| R029 | Holdings Overview | Last 12 Months / Net Gain [class rows (two levels)] | no class-grain gain table in Opal; BD classification tree |
| R031 | Holdings Overview | Last 12 Months / Return [class rows (two levels)] | class return contribution is a different figure; BD classification tree |
| R033 | Holdings Overview | Year To Date / Net Gain [class rows (two levels)] | no class-grain gain table in Opal; BD classification tree |
| R035 | Holdings Overview | Year To Date / Return [class rows (two levels)] | class return contribution is a different figure; BD classification tree |
| R037 | Holdings Overview | Quarter To Date / Net Gain [class rows (two levels)] | no class-grain gain table in Opal; BD classification tree |
| R039 | Holdings Overview | Quarter To Date / Return [class rows (two levels)] | class return contribution is a different figure; BD classification tree |
| R041 | Holdings Overview | Month To Date / Net Gain [class rows (two levels)] | no class-grain gain table in Opal; BD classification tree |
| R042 | Holdings Overview | Month To Date / Return [household total row] | month to date is not a ruled period |
| R043 | Holdings Overview | Month To Date / Return [class rows (two levels)] | class return contribution is a different figure; BD classification tree |
| R045 | Holdings Overview | Since <date> / Net Gain [class rows (two levels)] | no class-grain gain table in Opal; BD classification tree |
| R047 | Holdings Overview | Since <date> / Return [class rows (two levels)] | class return contribution is a different figure; BD classification tree |
| R053 | Account Overview | Allocation by Asset Class [class shares] | BD classification tree (class and segment rows), held only by BD |
| R060 | Account Overview | Benchmark: <benchmark> Return (Cumulative) | benchmark returns, held only by BD |
| R062 | Account Overview | Account Performance Last 12 Months [benchmark cumulative return lines (four)] | benchmark returns, held only by BD |
| R064 | Gain/Loss Review by Account | Cost Basis [class rows (three levels)] | BD classification tree (class and segment rows), held only by BD |
| R066 | Gain/Loss Review by Account | Ending Value [class rows (three levels)] | BD classification tree (class and segment rows), held only by BD |
| R068 | Gain/Loss Review by Account | Total RGL [class rows (three levels)] | BD classification tree (class and segment rows), held only by BD |
| R070 | Gain/Loss Review by Account | Total UGL [class rows (three levels)] | BD classification tree (class and segment rows), held only by BD |

## Run Report dialog (the screenshot), parameters counted apart

| id | parameter | status | Opal source or reason |
|---|---|---|---|
| D01 | Basis: Portfolio or Relationship (radio) | MAPPED | data/assets/scripts/gold/irpt_custody/client_report_figures.py: build_documents groups the accounts file by household id (one document per household). Opal's unit is the household (dim_relationship.relationship_id); it has no user-built 'portfolio' set, the run's accounts file is the set. |
| D02 | Portfolio selector | MAPPED | data/assets/scripts/gold/irpt_custody/client_report_figures.py: parse_accounts (household_id, account, household_name). Chosen by the accounts file, not a picker. |
| D03 | Date Range (preset) | MISSING | Opal has no date-range picker: the periods are fixed (RULED_PERIODS QTD, YTD, 1Y, SI). The report shows its own four period columns whatever the preset. |
| D04 | As of Date | MAPPED | data/assets/scripts/gold/irpt_custody/client_report_figures.py: build_documents(as_of) -> as_of_date. The same date, set by --as-of. |
| D05 | Exclude History Data (Yes/No) | MISSING | No Opal equivalent: Opal reads its own partitioned history and has no BD history-range switch. |
| D06 | Internal Use Only (Yes/No) | MISSING | ClientReportDocument.tsx has no internal-use mark or flag. |
| D07 | Performance Returns = Gross of Fees (the choice selected in the screenshot) | MAPPED | data/assets/scripts/gold/irpt_reporting/account_return_daily.py (COLUMNS, table account_return_daily): total_return_daily (gross of advisory fees; fee_amount null, FEE_RAIL_UNUSED). Opal's returns are gross by construction. |
| D08 | Performance Returns = Net of Fees (the other choice) | MISSING | Opal computes no net return (account_return_daily.py: no net return, no annualization); the advisory fee rail is unused. |
| D09 | Sample Mode (Yes/No) | MISSING | No Opal equivalent. |
| D10 | Supervised Filter: Supervised / Unsupervised / All Assets | MISSING | Opal carries no supervised/unsupervised flag in the silver or gold tables read here. |

The dialog's first control is the Run Report BASIS (Portfolio or Relationship). This PDF is a Portfolio-basis run: its header entity label on pages 2 to 4 is the portfolio, then each account. A Relationship-basis run would sit one level up; this input does not exercise it.

