# Layout baseline of one 49 Financial client Performance Report (CU-g-3)

Worker `0.9.0_WK_IRPT_CUSTDY~17`. **Structure only**: no value, name, account number or date. It is the input for the statement template (the Performance client statement, portal `ClientReportDocument`). Page-level facts come from `bd_field_map.py` (`extract`); chart contents were read from the rendering. Companion: `BD_FIELD_MAP_CU-g-3.md` (which source serves each field).

## 1. Page count and page order

**32 pages**, landscape letter (792 x 612 points). Page 1 is the unnumbered cover; the other 31 carry a header `Page n of 31`. Order of Run Report bases:

| pages | Run Report base | scope |
|---|---|---|
| 1 | Cover | unnumbered |
| 2 | Portfolio Overview | portfolio |
| 3 | Summary of Portfolio Accounts | portfolio |
| 4 | Holdings Overview | portfolio |
| 5 to 32 | **per account, in this order:** [Taxable Realized/Gain Loss Summary, taxable accounts only] then Account Overview then Gain/Loss Review by Account | account |

The portfolio-level run covered 11 accounts: 11 Account Overview pages, 11 Gain/Loss Review pages, 6 Taxable Realized/Gain Loss Summary pages (taxable accounts only). Total: 1 cover + 3 portfolio pages + 11 x 2 + 6 = 32 pages. Pages by base:

- Cover: page 1
- Portfolio Overview: page 2
- Summary of Portfolio Accounts: page 3
- Holdings Overview: page 4
- Taxable Realized/Gain Loss Summary: pages 5, 10, 17, 24, 27, 30
- Account Overview: pages 6, 8, 11, 13, 15, 18, 20, 22, 25, 28, 31
- Gain/Loss Review by Account: pages 7, 9, 12, 14, 16, 19, 21, 23, 26, 29, 32

No disclosure page follows the last page: the footer of each page says the report is incomplete without the accompanying disclosure page, and the PDF holds none (it is a separate document).

## 2. The page frame (every numbered page)

- **Header band** (grey, top right half; the firm logo sits left of it): left cell, the ENTITY LABEL (the portfolio on portfolio-scope pages, the account registration and masked number on account pages, one or two lines, bold) with `As of <date>` under it; right cell, right aligned: the report title (bold), the BASE TITLE, then `Page n of N`.
- **Footer:** a small boilerplate line on every page (`This report is incomplete without the accompanying disclosure page.`; on the Summary of Portfolio Accounts page it also carries `*Net Gain includes Fees.`). Overview pages add a three-line custom-benchmark disclaimer.
- **Mark:** an image across the lower left of every page, a not-for-client-distribution mark; it is consistent with the Run Report dialog's `Internal Use Only = Yes` setting (inferred, not proven) and it is not in the text layer.
- Section titles are 12 point, left aligned over their block; table headers 9 point; figures 7.5 to 8.8 point.

## 3. Block order and table columns, per base

### Portfolio Overview (portfolio scope; page 2)

1. **chart** `Allocation by Asset Class` -- raster image, left column.
2. **table** `Portfolio Value Summary` -- labelled-figure rows; columns are periods; 9 data row(s) on the first page.
   - column order: `Quarter To Date`; `Year To Date`; `Last 12 Months`; `Since <date>`
   - row labels, in order: `Beginning Value`; `Net Additions`; `Net Gain *`; `Ending Value`; `Return (Cumulative)`; `Benchmark: <benchmark> Return (Cumulative)`
3. **chart** `Portfolio Performance Last 12 Months` -- raster image, full width.

### Summary of Portfolio Accounts (portfolio scope; page 3)

1. **chart** `Allocation by Account` -- raster image, left column.
2. **chart** `Ending Value & Net Additions Last 12 Months` -- raster image, right column.
3. **table** `Activity Summary` -- entity rows; columns are measures; 12 data row(s) on the first page. Table-wide period header `Last 12 Months`. First row is a bold total row.
   - column order: `Beginning Value`; `Contributions`; `Withdrawals`; `Net Gain *`; `Income`; `Ending Value`

### Holdings Overview (portfolio scope; page 4)

1. **table** `Holdings Overview` -- entity rows; columns are measures; 19 data row(s) on the first page. Row hierarchy: 3 indent level(s). First row is a bold total row.
   - column order: `Ending Value`; `Allocation`; `Last 12 Months / Net Gain`; `Last 12 Months / Return`; `Year To Date / Net Gain`; `Year To Date / Return`; `Quarter To Date / Net Gain`; `Quarter To Date / Return`; `Month To Date / Net Gain`; `Month To Date / Return`; `Since <date> / Net Gain`; `Since <date> / Return`
   - footnote marks on figure cells: 1, 2
   - table footnote (legend): `(1) Annualized return, (2) Not held for the entire period`

### Taxable Realized/Gain Loss Summary (account scope; pages 5, 10, 17, 24, 27, 30)

1. **table** `Taxable Realized/Gain Loss Summary Year To Date` -- entity rows; columns are measures; 1 data row(s) on the first page. Table-wide period header `Year To Date`.
   - column order: `Cost Basis`; `Proceeds`; `Realized ST`; `Realized LT`; `Total RGL`

### Account Overview (account scope; pages 6, 8, 11, 13, 15, 18, 20, 22, 25, 28, 31)

1. **chart** `Allocation by Asset Class` -- raster image, left column.
2. **table** `Account Value Summary` -- labelled-figure rows; columns are periods; 9 data row(s) on the first page.
   - column order: `Quarter To Date`; `Year To Date`; `Last 12 Months`; `Since <date>`
   - row labels, in order: `Beginning Value`; `Net Additions`; `Net Gain *`; `Ending Value`; `Return (Cumulative)`; `Benchmark: <benchmark> Return (Cumulative)`
3. **chart** `Account Performance Last 12 Months` -- raster image, full width.

### Gain/Loss Review by Account (account scope; pages 7, 9, 12, 14, 16, 19, 21, 23, 26, 29, 32)

1. **table** `Gain/Loss Review by Account` -- entity rows; columns are measures; 20 data row(s) on the first page. Table-wide period header `Last 12 Months`. Row hierarchy: 3 indent level(s). First row is a bold total row.
   - column order: `Cost Basis`; `Ending Value`; `Total RGL`; `Total UGL`

Variation inside Account Overview: 2 of 11 pages show dash cells (no figure) with footnote mark 1 (`Not held for the entire period`); the other pages do not.

### Cover (page 1)

Top to bottom: firm logo; a rule; the portfolio name (large, right aligned); the label `Accounts` over a right-aligned list (registration name and masked number, one line per account, 11 lines); lower left, `As of <date>` over the report title in capitals.

## 4. The screenshot

The PNG is the **Run Report dialog**, not a page: Basis radio (Portfolio / Relationship), Portfolio selector, Date Range preset, As of Date, and Advanced Settings (Exclude History Data, Internal Use Only, Performance Returns Net/Gross of Fees, Sample Mode, Supervised Filter). It fixes no page layout, so the layout baseline above comes from the PDF alone; the dialog's parameters are mapped in `BD_FIELD_MAP_CU-g-3.md`. Reading it with the PDF: the Internal Use Only setting is consistent with the mark on every page (inferred), and the Gross of Fees setting is what Opal's returns already are.

## 5. Against `ClientReportDocument.tsx` (read only, portal @dbeb6764 in the main checkout)

The template composes (in order): cover; household page (returns table, accounts table); one page per account (returns, market value, holdings, activity, fees); a data-status and disclosure page. Page count `3 + accounts` (14 for 11 accounts) against the BD report's 32. Portrait letter against BD's landscape.

**Sections BD has that the template LACKS:**

| BD section | template today | Opal source |
|---|---|---|
| Portfolio Overview and Account Overview pages: the Value Summary table (beginning value, net additions, net gain, ending value, cumulative return across QTD, YTD, last 12 months, since) | the template has a returns table (period, return, window, status, basis) and market value start and end only | MAPPED (account_activity_daily) |
| the four benchmark return rows and the benchmark lines on the performance chart | none | MISSING (no benchmark library) |
| Allocation by Asset Class donut (portfolio and account) | none; holdings carry class and sector per security | MISSING for BD's class shares; per-holding weights MAPPED |
| Performance Last 12 Months line chart (portfolio and account) | none | MAPPED for the return line (series.json.gz); benchmark lines MISSING |
| Summary of Portfolio Accounts: allocation-by-account donut, ending value and net additions chart, Activity Summary table (beginning value, contributions, withdrawals, net gain, income, ending value per account) | the household page lists account, registration, market value start and end | MAPPED |
| Holdings Overview by class: ending value, allocation, net gain and return over five periods, two-level class rows | per-security holdings table on each account page (symbol, cusip, quantity, value, weight, class, sector) -- a different grain | total row MAPPED, class rows MISSING, month-to-date return MISSING |
| Taxable Realized/Gain Loss Summary (cost basis, proceeds, realized ST and LT, total) | none | MAPPED (account_lot_realized) |
| Gain/Loss Review by Account (cost basis, ending value, total RGL, total UGL by class) | none | account total MAPPED, class rows MISSING |
| the page header band on every page (entity label, report title, base title, as-of, page n of N) | kicker, title and a footer with as-of and `n / N` | layout only |
| periods `Month To Date` and `Last 12 Months` | the template's periods are the document's own QTD, YTD, 1Y, SI | month to date not ruled |
| the annualized and not-held-for-the-entire-period footnote marks | a per-figure status word in place of the figure | layout only |

**What the template has that BD lacks (keep):** the activity list (dated rows with type, symbol, amount); the fees block with its source label and the billed-fee flag; the since-inception anchor label; per-figure status (`NO_DATA`, `NOT_AVAILABLE`, `WINDOW_NOT_RULED`) in place of a dash; the data-status page; the disclosure slot (BD's disclosure is a separate document); the not-covered account page.

**Ordered differently:** BD opens with portfolio pages (overview, accounts summary, holdings) before any account, then repeats [taxable realized, account overview, gain/loss review] per account; the template puts one household page first, then one page per account, then status. BD puts the accounts summary on its own page after the overview; the template merges the account list into the household page. BD shows returns and value together in one table per scope; the template splits returns and market value into two tables.

