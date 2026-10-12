# FETCH_HELD_27 -- round 74 CB-bv-4

27 held tickers listed at 2026-10-11T20:31:30Z... then each asked once from Yahoo (yfinance 1.2.0, auto_adjust=False, 2020-06-27 onward).

- returned 25, empty 2 (CEM, FPNIX), errors 0; no ticker asked twice, no unheld asked, no Bloomberg.
- landed in the new folder yahoo_census_fetch_r74 (25 files); existing yahoo_census cache 3580 files before and after.
- readings: {'looks unadjusted': 25, 'no fetched close': 2} -- all NOT CUSTODIAN-VALIDATED.
- VBTLX is an outlier (min ratio 0.1823); not investigated.

Per-ticker detail in FETCH_HELD_27.csv.
