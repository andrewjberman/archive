# NEVER-WIDEN -- COO HALF: the CACHED-PATH span-bearing Lenovo run -- wsj only -- its upload and the daily rebuild (`HVST-aa-2`)

**Signer:** `2.0.0_SA_COO~H`, 2026-09-30 ~12:0xZ (08:0x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed; it signs the same tick).
**Ruling served:** `ROUND_ANALYSIS.round27.md` AMENDMENT 2 @`cb107ff848` (msg 27091). `aa-2` runs TODAY, after `aa-3`, as the
**CACHED-PATH arm only**. It does not claim the live path (row `Z-W76-S1`: a live wsj job records only a `stop_bound`).
**Vendor authority:** R-21 @`b390c36444`, on its mechanism: the collector script.
**Code pin:** CLOUD `717cbb0a14`. It carries `aa-1` (cached reach, rejected-key hold), `aa-3`'s phase A (bbg empty-struct
pruning) and `q-5` (`publishers_found_codes`). The act prints `git diff --stat 717cbb0a14 HEAD -- lib/opal_data_harvest
lib/research/harvest` and STOPs on any line.

## ISSUER AMENDMENT 1 (this half): wsj ONLY, bbg EXCLUDED

- `aa-1`'s hold table (`rejected_hold`) is populated only by a rejection made under the new code. `NM5NLQ6K50XZ01`'s rejection
  predates it, and the runtime DB has no `rejected_hold` table today.
- bbg's listings are cached today, so a bbg job's first live request would re-fetch that key into the 403 and the failed
  press-and-hold. That is `q-1`'s failure (row `Z-S45`), and it would press Bloomberg's bot check again for no evidence.
- `aa-1`'s replay already proved the hold on the recorded shapes. So bbg runs NO job, and its root joins the no-write set.

## ROUND-25 RULING 1 -- put paths, config defaults, stub evidence

| # | command | puts |
|---|---|---|
| 1 | `run --harvest-grammar --retrieval-mode backfill --floor 2026-01-01 --new-only --security-json org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~65/o5_lenovo.security.json --publishers wsj --max-jobs 1 --runtime-root "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"` | **1**: the persisted run record (`_persist_run_record` -> `bronze_put("amgt","run_record",...)`). Articles and listings queue locally. Stub evidence: `test_o1_run_record_reach.py`. |
| 2 | `upload-harvest --max-objects 60 --retrieval-mode backfill --runtime-root <main>` | Per queued wsj row: bronze plus a silver row (`o-5` act-3 receipt shape). Expected **0 new articles**: `o-5`'s 11 wsj Lenovo articles and 16 held keys are stored already, so it may be a no-op. |
| 3 | `build-daily --securities-json org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json --as-of 2026-09-30` | **1**: `chatter_daily` (stub-captured in `p-3`(a), `p-3.signing.py`). |

**Config defaults the argv leaves unset:**
- `jobs_per_run` is 1, which matches the one wsj job;
- `minimum_request_seconds` is 15 and `jitter_seconds` is 10;
- `max_listing_pages` is 25;
- `SUCCESSFUL_RUN_STATUSES` (publication_gold ~:561).

## VERDICT: SIGNED

- **Blast radius:** 1 run-record object; new wsj objects only if new articles are found (expected 0); 1 new `chatter_daily`
  part.
- **No-write roots:** bbg, barrons, ft and sa gain nothing.
- **Rollback:** forward only.

## 1. BEFORE -- measured at signing (`round28/aa2_signing_before.json`)

| root | objects |
|---|---|
| bbg | 1007 (includes `aa-3`'s part) |
| wsj | 84 |
| barrons | 30 |
| ft | 28 |
| sa | 106 |
| `amgt` `run_record` | 1 (`q-1`'s) |
| `chatter_daily` | 9 parts |

The outbox holds 0 pending rows. The act-start gate (`aa-2.before.py`) STOPs on any difference.

## 2. EXPECTED OUTCOME, BOTH BRANCHES

**Branch A (wsj concludes):**
- The run record carries a wsj `reached_span` marked `from_cache` from today's cached pages. `aa-1`'s replay of `q-1` read
  2025-11-20..2026-09-23.
- The daily rebuild then reads **run records >= 1**.
- Lenovo's coverage from THIS run record ALONE (`run_record_spans`) holds the wsj span, and the served Lenovo rows carry
  `wsj` in `publishers_covered_codes` on those days.
- **This is the positive arm the round owes:** the run-record path as the SOURCE of coverage.
- `publishers_found_codes` is SERVED on the rebuilt snapshot.
- RESOLVED stays 0 of 191, and the declared set stays `[]` (a per-name trial).

**Branch B (wsj refuses):** recorded and not retried. There is no span, and the rebuild shows the refusal in the run record.
AC1 fails honestly.

## 3. ROLLBACK

Forward only: every put is never-overwrite, and readers take the newest. A delete is a human word.
