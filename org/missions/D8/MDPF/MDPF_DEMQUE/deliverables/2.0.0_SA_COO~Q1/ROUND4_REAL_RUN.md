# MDPF_DEMQUE round 4 -- the one real run of each outcome (2.0.0_SA_COO~Q1; DQ-t-14 run; drain pending the site-Z integrate)

Run 2026-10-09T04:27:39Z at the base after merges @0134f2f797 (t-11), @ba79175a8a (t-12), @5c962f6372 (t-13), @0016840aed (t-10) and the
hookup @d579c0279a. Hygiene: `py_compile` OK, ruff py39 clean, 54 of 54 tests. No vendor call (quotes read files; the ranking reads
Commonwealth's silver objects read-only).

| outcome | run | result (verbatim, trimmed) |
|---|---|---|
| FWD-3 reserve (t-10) | `bbg_quote.py --quote requests/SITEZ-SIGNIN-PREFLIGHT-REFDATA-20261009.json` | `"cells": {"bloomberg_reference": 1}, "claims": {"ceiling": "absent", "reserve": "held"}, "allowance_gap": "reference.ceiling absent"` |
| FWD-4 quote (r3 + t-10) | `bbg_quote.py --quote requests/AMGT_RESAPP-107a-ABNB-MODEL-BLOCK.json` | `"cells": {"bloomberg_model_block": 989}`, breakdown forecast 51 / header 25 / history 913, `"claims": {"ceiling": "absent", "reserve": "absent"}` |
| FWD-4 standing request | `bbg_quote.py --quote requests/ETFS_RIVALS-HISTORY-OWED-DAILY.json` | `ValueError: request has no securities` -- a standing request (daily-changing set, run cap) is not priceable by the quote; its file carries the cap as a held quote. **Round-5 candidate.** |
| FWD-9 ranking (t-13) | `rank.py --probe 5` (real crosswalk + transactions) | `RANK 1 cusip=00162Q866 priority=P1 ... (17 of 99 holding accounts matched); score 2598 held days x 99 accounts x largest purchase 221479.04` ... `RANK 3 ... priority=P2 ... no purchase on record` |
| FWD-5 unresolved (t-12 + hookup) | `unresolved.seed(unresolved_seed.csv)`; draw fold QA (stubbed) | 5 rows, state `UNRESOLVED:YAHOO_NO_DATA`; fold QA: an empty pull opens its window, a LOCKED security stays off |
| FWD-1/5 lock floor (t-11) | the next scheduled draw (2026-10-10T02:30Z) re-locks the 16 cleared pilot funds and PONPX under the floor | **pending the fire** |
| FWD-2/3 ledger (t-14) | site Z `0.7.0_AE_CloudOps~ZQ`: candidate @492cb5a2f1 (box/sitez), CTO~Z half @3607c76017, deploy closed @ca3b056946; re-run at dell1 2026-10-09 ~08:2xZ: `dq_t14_ledger.py 2026-10-08` + `s3api head-object` | `LEDGER-OK rows=4 cells=17878 under s3://opal-data-assets/bloomberg/global/bronze/demand_ledger/dt=2026-10-08`; object 1040 bytes, LastModified 08:14:16Z (matches ~ZQ's served sha256 record); daily task OPAL_DEMQUE_bbg_ledger_upload 08:30 ET, previous UTC day (~ZQ read-back). Cells are HELD (request-side counts), not metered. Rows Z-W1-S1 (shared `backfill` mode; split by batch id) and Z-W1-S2 (OPAL_BBGTML notebooks record no budget rows) |

Requests on the queue's books: tier 1 pre-flight (1 reference cell), tier 2 R4-P1-SLICE-1 (150 ranked P1, 516,900 close cells; Yahoo,
next draw), tier 3 Rival Funds standing (cap 20,000 points a run), tier 4 the two AMGT_RESAPP requests (4 and 989 cells).
