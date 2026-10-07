# AMGT_HARVST round 50 -- close run (`2.0.0_SA_COO~H`, 2026-10-06 ~20:1xZ)

Issuance @40e9fdb0a9 (2 orders, fanout 2 of 2). Both terminal: `aw-1` merged @7f92ce3dfa, `aw-2` merged @a1cd91d953.
Harvest suite on merged CLOUD: 674 passed, 1 skipped.

## aw-2 -- SA on the tab pattern (the real entry point)

The sa leg was resumed at 20:05Z through `backfill_driver` (`.runtime/harvest-backfill/r50_launch_sa.json`, checkpoint
`r47_sa_checkpoint.json`, root `.runtime/opal-data-harvest-sa`, `--clear-stop sa`). From `events.jsonl` of that root:
- `GET /api/v3/account/53673840/info` -> 200, 5,150 B (20:05:43Z). The same request answered 402 at 01:12:40Z through the proxy.
- `GET /api/v3/symbols/amx/news` -> 200, 91,447 B (20:06:03Z).
No proxy is in the path: the sa contract reads `transport: tab`, egress native in-tab, profile `browser-profiles/sa`
(Andrew's Google sign-in, ~19:3xZ).

## aw-1 -- the origin load wait

Jobs started since the 18:39Z resume, by run-record `started_at`, split at the merge (19:55Z). Denominator: every run file
of the three roots in that window.

| leg | before the fix | after the fix (to ~20:10Z) |
|---|---|---|
| barrons | 10 jobs: 2 TimeoutError, 1 RuntimeError (HTTP 400 on one article) | 5 started: 0 TimeoutError |
| wsj | 8 jobs: 2 TimeoutError | 0 started yet (one long job in flight) |
| bbg | 5 jobs: 1 TimeoutError, 2 TargetClosedError | 1 finished: 0 errors |

- TimeoutError before any request: 5 of 23 before; 0 of 6 after. The sample after the fix is small; the legs keep running.
- **Correction to the issuance text:** decomposition section 63 and the `aw-1` face count the 5 TimeoutError jobs as bbg 2,
  wsj 2, barrons 1 "of 15". Measured from the run records: barrons 2, wsj 2, bbg 1, and bbg's other two errors were
  `TargetClosedError`, a different class that `aw-1` does not address (bbg stopped on it at 19:4xZ).
- **CORRECTED 2026-10-07 ~03:3xZ (row AMGT_HARVST-Z-S94): the sentence that stood here was WRONG.** It said the five
  TimeoutError pairs were undone in their checkpoints and re-ran at each leg's resume. They were recorded DONE with status
  `error` (`backfill_driver.py:314`), and a resume skips every done pair (`:120`), so none of them re-ran. Across the four
  checkpoints 37 pairs ended on a stop status and were never retried
  (`deliverables/2.0.0_SA_COO_H/round52/stop_status_pairs.json`). They are re-run with `--names` on their own checkpoints.

## Open at the close

- bbg `TargetClosedError`: 2 of 5 jobs before the fix (3 of 199 historically). Cause unread.
- barrons `listing_empty_200`: 3 of the 5 jobs since the fix (CTO 29759: pause at a majority of the last 25).
