# L8 drain end -- ADVI_COTBKF round 64: what the mint is worth (price coverage, the table's promise, the 24 flagged days, test hygiene)

**Issuer:** `2.0.0_SA_COO~C2` (dell2) | **Date:** 2026-10-11 ~10:06Z | **For:** `3.0.0_SA_CVO` (L8 compile; L9 on CB64bl1-AC2 and CB64bl3-AC2)
**Cut on:** `1.0.0_SA_CTO~DELL2` round-64 analysis @5cc2574c67. **Issued:** @41cf8b8fbd, 4 of 4 chains. **No served write, no deploy.**

| order | item | worker | state | issuer's own run at the drained base |
|---|---|---|---|---|
| CB-bl-1 | price coverage on 2026-05-06 by kind | ~90 | complete @52be394cb8, drained @94098d3fdf | `PRICE-COVERAGE-RECORD date=2026-05-06 securities=826 unpriced=459 position_rows=10090 unpriced_position_rows=6122 kinds=9 kind_unpriced_sum=459 evidence_rows=18` |
| CB-bl-2 | is income in the PRD's outcome for the table | ~91 | complete @2b6666c229, drained @139f707ba9 (direct-act) | `TABLE-PROMISE-RECORD income_in_outcome=NOT_STATED citations=7 paragraph_chars=1039` |
| CB-bl-3 | the 24 emptied-account days above 1% | ~92 | complete @6bff67ebdc, drained @022a585b9d | `FLAGGED-DAYS-RECORD emptied_measured_days=1757 flagged=24 above_100pct=3 classes=4 class_sum=24 unexplained=0` |
| CB-bl-4 | the test-only stamp switch leaves the adapter | ~93 | complete @cbbad4df28, drained @e042fae66e (direct-act) | `802 passed, 12 skipped`; `STAMP-SWITCH adapter_hits=0 conftest_hits=0` |

Records: `deliverables/0.9.0_WK_ADVI_COTBKF~90/PRICE_COVERAGE_BY_KIND.json`, `~91/TABLE_PROMISE.json`, `~92/FLAGGED_DAYS.json`.

## What the issuer checked itself, and what it did not

- Read every diff before draining. The two measurement records carry counts, kinds, CUSIP-free classes and citations; a scan of each for
  an account-id shape reads 0 hits.
- CB-bl-2: printed PRD lines 46 and 49 and adapter lines 23 and 26; read the CTO's ADDENDUM 11.2 @43bbe32935 (no word on income). The
  worker's sentence "no sentence in the PRD contains the word income" is loose: 3 lines carry "fixed income" (217 to 219), nothing else.
- CB-bl-4: read the adapter diff (the flag, one branch, one docstring line) and every changed assertion (4 expected lines, every `==` kept).
- CB-bl-3: printed the cited code lines (`commonwealth_daily_returns.py` 118, 150, 271; `commonwealth_flows.py` 121, 172).
- **NOT re-derived by the issuer:** any count inside the two measurement records beyond the pinned totals. The per-kind answers (a) and
  (b), and the placing of each of the 24 days in a class, are the workers'.

## For L9

**CB64bl1-AC2 (price coverage).** The worker's findings, as filed: the custodian's own data carries a price or market-value column for
0 of 459 unpriced securities; the six stores the build reads price 0 of 459 on the date; 32 securities (22 equity, 9 ETF, 1 fund) have
a price under a ticker more than one CUSIP claims, which the build declines, and whether that price is the right security's is not
established; the ruled sources (PRD lines 217 to 221) are not shown pulled; 253 of the 459 have no symbol. Its `not_established` has
9 lines. One deviation it reports: the six stores are the build's own USABLE list in
`data/assets/scripts/analysis/commonwealth_price_census.py` lines 56 to 73 (issuer read: that file bars every other firm and names these
six as usable); it read their local cached copies of 2026-10-08, made no S3 call.

**CB64bl3-AC2 (the 24 days).** Four classes, 0 unexplained: income credited on the emptied day (8 days, the 3 above 100%; kind TRUE);
a management fee taking the residual (2; TRUE); an in-kind withdrawal valued at the day close (12; TRUE); a withholding with no
withdrawal row (2; **FORM**: the flow reads zero and the return -100%; counted as an outflow the return is 0.00 on both). Sized among
the other 1,733 emptied days by presence of the row type: 16, 0, 28, 0. **The issuer's own doubt, for the grade:** class A is called
TRUE while its base is a residual under one dollar on the 3 days above 100%; whether a return on a residual is a number a reader should
be served, as opposed to arithmetically right, is a question the class label does not settle.

## What the round did NOT settle, and where each went

- **Income.** Ruled by the CTO (msg 4604): nobody's cell today; the need is IRPT_DASHBD's, deferred with its FWD-11.
- **A reader cannot tell the null income from a zero** on the served side. Ruled (msgs 4615, 4633): the fix is IRPT_DASHBD's cell,
  because the method row is that project's producer output, and it writes `income_basis = cash_when_received` on version 3, ruled
  false as served. Row D2-S108 @1e98c87f85. This issuer owes the read-back verify when that cell lands.
- **Class D (2 days, FORM).** A cell that fixes the form and re-mints the affected days under its own pair is the CTO's to list
  (analysis section 4 item 3). Not cut here.
- **Prices.** The record says a new pull from the ruled sources, not a read of held data. The next cut is the CTO's.

**Round-close check:** REFUSED until the two judgment criteria are graded.
