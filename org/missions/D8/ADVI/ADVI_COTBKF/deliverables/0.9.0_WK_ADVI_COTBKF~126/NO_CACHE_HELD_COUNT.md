# NO_CACHE_HELD_COUNT (round 73, CB-bu-4)

Count over local files; nothing was fetched.

- 270 fund series; 73 substituted; 197 left on the store; 76 with a cached close; 121 without.
- 27 of the 121 fund series with no cached unadjusted close are held on a served account-day: 1875 priced holding account-days, 115 measured account-days (distinct); 121 of the 121 (27 of the held) have a ticker, which a fetch needs.
- Held: 27; not held: 94. Held with a ticker: 27.
- Held tickers: ACTSX, CDSIX, CEM, CEMIX, EIBIX, EIHYX, FAX, FFC, FLCOX, FPNIX, FSGGX, FSPGX, FSSZX, FTHSX, FXNAX, JBALX, MFEIX, MSD, NUV, PEIYX, PFORX, VADFX, VBITX, VBTLX, VTIFX, VVOAX, WOBDX

Not established: Whether the vendor would return a close for any of these tickers (nothing was fetched). Whether an unadjusted close would differ from the stored price on any of them. Measured account-days are distinct (account, date) pairs with a non-null return on which a held series is valued; the per-series sum can exceed the distinct count. Reinvestment rows are counted from the custodian transaction cache dvr rows by stripped CUSIP.

Detail: NO_CACHE_HELD_COUNT.json and .csv.
