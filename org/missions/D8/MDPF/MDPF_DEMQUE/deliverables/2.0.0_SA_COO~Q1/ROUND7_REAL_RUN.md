# MDPF_DEMQUE round 7 -- the one real run of each outcome (2.0.0_SA_COO~Q1)

Run 2026-10-11 ~03:5xZ on dell1 against origin/CLOUD dcb15f35bb (read-only worktree; every R7 check script run from its root).
Terminal orders: t22 @4c6a16ded6, t23 @00a33f63ee (both merged on dell1 2026-10-09), t24 closed by `0.7.0_AE_CloudOps~ZQ` @794152a492
(status complete; world act ran 2026-10-10 10:00 ET at site Z). `round-close-check --round 7` at this base: 3 of 3 complete, proof_ok=3,
judgment=0, verdict=MAY-CLOSE.

| outcome | run | result (verbatim, trimmed) |
|---|---|---|
| R1 quote over non-trading days (t22) | `dq_t22_quote.py` | `2026-10-10: finish_date=2026-10-17 allowance_today=5858`; `2026-10-09: ... allowance_today=0` (the negative arm, a trading day); `NTDQ-OK finish 2026-10-17; trading day 0; Saturday 5858; ceiling measured` |
| R1 first non-trading-day backfill (t24) | `dq_t24_tests.py`, `dq_t24_draw.py` | `BKF-OK` (8 passed, 3 of 3 required names); `DRAW-OK 2026-10-10 drawn 5858 of 5858 allowed; verdict=OPEN cells_drawn_total=5858 of 15720`. Actuals row carried at cdfed4dca9 (drawer ~ZQ, outcome DRAWN). |
| R2 `--all` read (t23) | `dq_t23_all.py` | `QALL-OK 6 of 6 quote files read`: DEMQUE-TR row `cells_drawn 5858 of 15720, finish_date 2026-10-13, verdict OPEN`; SECHIST card A `UNQUOTED` (no finish_date key, the D1-S4 shape, read not crashed); 3 SECHIST/preflight rows `ON_TIME`. |
| C-PRICES served write (t-21, carried) | `served_tr_read.py` (read-only, served store) | index written 2026-10-11T02:34:22Z; `109 with the 7 columns, 32 with the original 3, 0 other`; `SERVED-TR-OK`. The 32 are the symbols whose last Yahoo attempt is 2026-10-09 (set intersection 32 of 32); row D1-S8. |
| Lock floor at the draw (carried) | `~/.opal/demque/unresolved.csv` + `pacer.json` (dell1 device-local) | 2026-10-10 draw: 35 `REJECTED:LOW_TRADE_AGREEMENT` and 3 `REJECTED:PRICE_MISMATCH` (agreement floor 90 pct, `lock.py`); 147 symbols OK, 200. 2026-10-11 02:3xZ draw (ledger rows dated 2026-10-10 local): 22 `UNRESOLVED:YAHOO_NO_DATA`, attempts 2 each, 0 cells drawn on all three standing requests. |

## What is not read

- The lock floor read is the per-symbol REJECTED counts above, taken from the dell1 device-local draw state. The locked-accepted count and the
  per-CUSIP trade-date agreement were not read here, so "the floor held" is NOT claimed; only that 38 rejections carry their reasons.
- The 15,720-cell request is OPEN at 5,858 drawn; the quote's finish date is 2026-10-17 (t22). The quote file the t23 read loads carries
  finish_date 2026-10-13 while t22's quote reads 2026-10-17; which of the two the 15,720-cell request is held to was not adjudicated here.

## Hygiene (once, here)

`py_compile` OK on the four touched scripts; ruff py39 clean on `bbg_backfill.py`, `bbg_quote.py`, `quote_vs_actual.py`.
`pytest data/mdpf/scripts/demque` ends in INTERNALERROR at collection (`land_cot.py` cannot read its consumer's key after ADVI_COTBKF
moved it onto legacy_addresses; row D1-S7). With `test_demque_land.py` ignored: 89 passed, 1 failed
(`test_demque_bbg_ledger_upload.py::test_reads_record_lines_and_converts_rows_to_cells_per_mode`, `[48, 64, 5, None, 2] != [48, 64, 5, 14, 2]`,
the open row D1-S6). Neither red touches t22, t23 or t24.

## Rows at this close

Open: D1-W19-S1, D1-W19-S2, D1-S5, D1-S6, D1-S7, D1-S8 (OBSERVATION, INERT); `Z-W1-S4` (BLOCKING, INERT). 0 ARMED, 0 defects.
`Z-W1-S4` is the order's own refusal; the issuer amendment @9c613dea5b granted the opt-in diagnostics and `outcome`/`stop_reason`, the three
vendor-warning tests pass (`BKF-OK`), and the draw read 0 vendor diagnostics in 2,929 attempts. No ADJUDICATION file carries its id (0 of 6),
so the CVO's disposition is the carrier; the issuer's recommendation is RESOLVED.
