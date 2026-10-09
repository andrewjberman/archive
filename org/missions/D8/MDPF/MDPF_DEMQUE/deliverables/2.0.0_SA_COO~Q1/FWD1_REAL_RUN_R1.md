# MDPF_DEMQUE round 1 -- the issuer's one real run of FWD-1 (2.0.0_SA_COO~Q1, 2026-10-08T23:50:07Z)

**Thread: n.** Hops 2-4 work on a real security; hop 5 lands nothing; hop 6 is BUILD-NEEDED (DQ-t-5). FWD-1 is NOT realized.

Code at merge @921d20bcb6 (`data/mdpf/scripts/demque/`). Driver: a session scratch script that calls the merged modules directly (draw does
not keep prices, so the one Yahoo answer is reused by the draw and the lock). One live Yahoo request (Andrew @489e1cd24c); S3 reads only;
the lander ran dry (no `--apply`, no PutObject). Drain hygiene before the run: `py_compile` OK, `ruff --target-version py39` clean, 23 of
23 tests passed across the four test files.

Security: CUSIP `00162Q866`, Commonwealth Symbol `AMLP` (ETF), from ADVI_COTBKF's price-need file (YAHOO, window 2013-04-08..2026-06-23,
3,323 days). Chosen as the first need-file row with trade prices (DQ-t-1 probe: 206). Its living-client tier (crosswalk P1) is NOT read
here: a claim of `held`, not `measured`.

| hop | result (verbatim output) | reading |
|---|---|---|
| 4 quote | `QUOTE {"cells": {"yahoo": 3447}, "finish_date": "2026-10-08", "request_id": "R1-FWD1-AMLP", "requests": 1}` | priced in cells before anything ran |
| 3 pull | `PULL status=OK rows=4055 splits=1 first=2010-08-25 last=2026-10-08` | one request, whole history with actions |
| 4 draw | `LEDGER [{"cells_drawn": 3323, "cells_quoted": 3447, ..., "outcome": "DRAWN", "page": "advisor-intelligence/cottonwood", "vendor": "yahoo"}]` | actual 3.6% under quote (weekdays vs trading days) |
| 2 lock | `LOCK {"state": "LOCKED", "claim": "measured", "method": "C1", "observations_checked": 108, "observations_passed": 100, "median_abs_error": 0.00502...}` | proved against the client's own trade prices |
| 5 land | `LAND hist_rows_to_add=0 lookup_to_add=0 unmatched=1 conflicts=0` | **break**: the CUSIP is not in the one transactions object the lander reads (`opal-data-cot` latest day: 14,198 rows, 864 assets, DQ-t-4 probe) |
| 6 page | DQ-t-5 `VERDICT: BUILD-NEEDED` | **break**: `opal-cot-gold-run` runs no S_00; S_00 would FATAL on the two absent Tier-2 objects; no page reads `canonical_prices` (pages value from BD-reported market value via `gold/canonical/holdings`) |

**What this changes.** The round-1 landing target (Cottonwood's Tier-2 inputs to `build_canonical_prices_v2.py`) reaches no page. FWD-1's
"shows its daily prices on that client's pages" needs a decision the decomposition cannot make: which page shows a client's per-security
daily prices (none does today), and which store it reads (Cottonwood's own price build, or MDPF_SECHIST's one series per security, C-SERIES).
That is an ENDPOINT-level question for `1.0.0_SA_CTO`.
