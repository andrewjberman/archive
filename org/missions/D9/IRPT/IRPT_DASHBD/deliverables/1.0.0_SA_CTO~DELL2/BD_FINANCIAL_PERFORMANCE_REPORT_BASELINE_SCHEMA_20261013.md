# The baseline: Black Diamond's "49 Financial Performance Report", by section and column (structure only, no client data)

**Source:** a 32-page Black Diamond export Andrew supplied 2026-10-13 ~19:0xZ ("I have included the Black Diamond export here so you can have
a baseline schema that we can work toward for the 'performance' tab as well as the export"). The file is kept OFF the repo, at
`C:/dev/_irpt_private_evidence_20261009/bd_baseline/BD_49F_FINANCIAL_PERFORMANCE_REPORT_20261007.pdf`, because it names a real household and
its accounts. This page carries only its structure, read from the text of every page by `1.0.0_SA_CTO~DELL2`. Its subject is one 49
Financial household of 11 accounts, as of 10/7/2026.

## Report order

| # | section | grain | contents |
|---|---|---|---|
| 0 | Cover | household | Household name; every account as "<registration name> - XXXX<last 4>"; "49 Financial Performance Report"; "As of <date>"; "Accounts" |
| 1 | Portfolio Overview | household | (a) chart Allocation by Asset Class; (b) chart Portfolio Performance Last 12 Months; (c) table **Portfolio Value Summary**; the custom-benchmark disclosure paragraph |
| 2 | Summary of Portfolio Accounts | household + each account | (a) chart Allocation by Account; (b) chart Ending Value & Net Additions Last 12 Months; (c) table **Activity Summary, Last 12 Months** |
| 3 | Holdings Overview | household, by class | table **Holdings Overview** |
| then, per account (taxable first where applicable): | | | |
| 4 | Taxable Realized Gain/Loss Summary, Year To Date | account | only for taxable accounts with realized activity |
| 5 | Account Overview | account | as section 1 at account grain: allocation chart, performance chart, **Account Value Summary** |
| 6 | Gain/Loss Review by Account, Last 12 Months | account, by class | table |
| end | disclosure page | -- | every page says "This report is incomplete without the accompanying disclosure page"; the export Andrew sent does not include it |

Page footer on every page: "<household or account> 49 Financial Performance Report", "As of <date>", "Page n of N".

## The tables, column by column

**Portfolio Value Summary (household) and Account Value Summary (account)**
- Columns: Quarter To Date | Year To Date | Last 12 Months | Since <inception date of that household or account>.
- Rows:
  - Beginning Value
  - Net Additions
  - Net Gain * ("*Net Gain includes Fees")
  - Ending Value
  - Return (Cumulative)
  - one row per benchmark: "Benchmark: Ultra-Short Term / Short-Term / Intermediate-Term / Long-Term Return (Cumulative)". These are the Opal model benchmarks, the same four on every page.
- A window the account did not exist for prints "—¹" with "¹ Not held for the entire period".

**Activity Summary, Last 12 Months**: rows are the household, then each account as "XXXX<last4> - <registration>". Columns: Beginning Value |
Contributions | Withdrawals | Net Gain * | Income | Ending Value.

**Holdings Overview** (household): rows are the class hierarchy (class, then sub-class). Columns: Ending Value | Allocation | then Net Gain and
Return for each of Last 12 Months, Year To Date, Quarter To Date, Month To Date and Since <inception>. Footnotes: "¹ Annualized return",
"² Not held for the entire period".

**Taxable Realized Gain/Loss Summary, Year To Date**: Cost Basis | Proceeds | Realized ST | Realized LT | Total RGL.

**Gain/Loss Review by Account, Last 12 Months**: rows are the account, then the class hierarchy. Columns: Cost Basis | Ending Value | Total RGL |
Total UGL. A class with no holding prints "—".

## The class hierarchy it uses (49 Financial's, in report order)

- **US:** Large Cap Core, Large Cap Growth, Large Cap Value, Mid Cap Core, and single-sector rows (e.g. Industrials, Information Technology).
- **INTL:** Intl - Dev Market, Intl - Emerging Mkts.
- **Taxable:** High Yield, International Bonds, Corporate Bonds Short, Corporate Bonds Intermediate, Government Short.
- **Non-Taxable:** Municipal Bonds Short, Municipal Bonds Intermediate.
- **Real Estate:** US Real Estate.
- **Cash:** Cash.
- **To Be Classified**, **Unclassified**.

## Conventions it shows

- Money in whole dollars with thousands separators; percentages to one decimal.
- Returns are cumulative for windows under a year. Since-inception is annualized past a year (¹).
- "Net Gain includes Fees". Opal's served return is total return BEFORE advisory fees (IRPT_DASHBD FWD-8). This difference must be
  labeled wherever the two sit side by side; it is not to be silently matched.
- Inception is per household and per account ("Since 1/13/2025", "Since 10/1/2025"), not a firm-wide date.

-- read by 1.0.0_SA_CTO~DELL2
