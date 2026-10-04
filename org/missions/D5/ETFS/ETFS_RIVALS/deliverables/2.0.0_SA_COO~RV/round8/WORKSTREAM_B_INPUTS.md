# ETFS_RIVALS round 8 workstream B -- measured inputs (2.0.0_SA_COO~RV, 2026-10-04 ~21:3xZ)

Read-only investigations run on Andrew's signed-in smoke (record @1c31a5f6ce). Served page 2026-10-02 at
`s3://opal-data-etfs/rivalfunds/etfs/platinum/page/date=2026-10-02/index.html`; holding_contribution revision
20261004T110855Z-a34b481440f1, buying_trend 20261004T110934Z-6dd5fc42aa38 (manifest.json). Workstream B is cut after the
2026-10-05 grades, against PRD v0.14 (@4cc8e40575) once its ratified-text half is re-signed.

## S2 -- the grounding fail is an incomplete citation list, not an invented figure

- Account: IDVZ "The last 30 days" (research_hypotheses-20261002T110438Z-ai.parquet; re-grade -ai-rg4 still FAIL). Reason:
  "figures not in any cited row: $1.6 million, $1.3 million", from the Observed line "... Reckitt Benckiser Group PLC for
  $1.6 million, Iberdrola SA for $1.3 million ...".
- Both are real fact-pack rows the model did not list in `cited`: T7 Reckitt add 1,564,110.98 (`IDVZ|756255303|2026-09-14`),
  T9 Iberdrola add 1,292,762.88 (`IDVZ|450737101|2026-09-14`), both in trades-20260930T151340Z-b03-07a8cd274f3a.parquet.
  Re-grading with T7 and T9 cited returns PASS.
- Grader: `ai_accounts.py:396` (cited set), `:274-277` (compare), `:283` (reason), `:201-207` (matcher, correct here),
  `:466` (re-grade reuses stored citations).
- Candidate cell: attach a fund-pack fact whose value matches a stated figure (a fact counterpart to `used_readings`,
  `:357-360`), or keep the FAIL but reason it "uncited fact T7, T9". Caveat: "$1.3 million" also matches T8 and Y-away5, so a
  value match is ambiguous. CGIC's "$5.7 million" fail not measured.

## S3/S5 -- the YTD window and the toggle

- YTD is clipped to the fund's first report: `gold_holding_contribution.py:122` (YTD start 01-01), `:411` (`first =
  min(book)`), `:417` (`start = max(period start, first)`); `render.py:837-838` labels "Year to date (2026)" from the as-of
  year. IDVZ YTD = 08-21..10-01 (28 return days), PFOE 08-24..10-01 (27). Not a 30-day rule: 08-21..10-01 is 29 NYSE days.
- The as-of 2026-10-01 is the first day of October and Q4, so MTD = QTD = one day for every fund.
- IDVZ MTD/QTD: 0 of 40 holdings priced ("Nothing ranked"); BIDD 0 of 48; MTD totals exactly 0.0 for BIDD, CGIC, GQGU, SCHY.
- The buying trend ignores the toggle: YTD-only table (`gold_buying_trend.py:157`, clip `:210`); the toggle CSS switches the
  ranking panels only (`render.py:1380`). PRD v0.14 (S7/S8) replaces the period model.

## S6 -- history depth (gold canonical_shape, 1,169 objects / 504 date partitions, newest revision per date)

| fund | source | earliest | report dates | vs 2026-01-02 |
|---|---|---|---|---|
| IDVZ | home_producer | 2026-08-21 | 23 | 7.5 months late |
| PFOE | home_producer | 2026-08-24 | 24 | 7.5 months late |
| WCMG | issuer_first | 2026-04-23 | 93 | ~4 months late |
| TXUE, BIDD, CGIC, INEQ, SCHY | bloomberg_primary | 2024-09-30..2025-01-29 | 420-502 | covered |
| GQGU, TSEL, BASG, ETFT, PCLG | issuer_first | 2024-12-31..2025-12-02 | 209-396 | covered |
| ACWI, IWM | bloomberg_primary (pending) | absent | 0 | not live |

- IDVZ/PFOE come only from the home-producer files (`home_producer.py:4-8`), first present in the 2026-08-21 folder. The
  remedy is D12 (lg-1, then the IDVZ/PFOE backfill to inception). WCMG (~4 months short) is a new finding with no cell yet.
