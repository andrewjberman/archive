# Gold Chain Performance Bottleneck Audit — Group B + C
**Agent:** 0.4.0_DS_ClientPlatform~B  
**Date:** 2026-04-16  
**PRD:** docs/architecture/GOLD_PERF_PRD.md  
**Method:** comp-pipescript io (all scripts) + selective code read for loops, executor patterns, worker constants  

---

## Executive Summary

**CTO hypothesis: C scripts are the critical path — PARTIALLY CORRECT.**

The critical path within C is: C_00 → C_02 → C_03 → C_07 → (C_06 || C_08). But the
largest CPU waste is not inside individual scripts — most Group B and C scripts are
already internally parallelized with ProcessPoolExecutor (fork) or ThreadPoolExecutor
at 60–256 workers. The machine is idle because the chain dispatcher runs scripts
sequentially even when they have no dependency on each other.

**Primary finding:** At least 5 independent parallelization opportunities exist at the
dispatcher level. Estimated chain wall-time reduction: 35–45%.

---

## Dependency Graph (actual, not dispatch order)

```
A_00 → [all scripts needing accounts_dimension]

B_00 (Schwab reconciliation)  ||  B_01 (holdings lots) ← A_00 only
  |                                   |
  +→ B_02 (canonical lots)      B_01b (new security classify) ← B_01
  +→ B_03 (account gains)
         |
         +→ C_00 (canonical perf)  ||  C_01 (canonical NNA) ← B_03 + [prior C_02]
                  |
                 C_02 (client perf)     C_05 (tax liability) ← B_01b + external only
                  |
                 C_03 (account perf)
                  |
                  +→ C_07 (advisor attribution)  ||  C_04 (validate AUA) ← C_02
                          |
                          +→ C_06 (client mix TS)  ||  C_08 (fee efficiency) ← C_07
```

Dispatch order today:  
`B_00 → B_01 → B_01b → B_02 → B_03 → C_00 → C_01 → C_02 → C_03 → C_04 → C_05 → C_06 → C_07 → C_08`

---

## Script-Level Bottleneck Analysis

---

### B_00 — canonical_holdings.py (1,107 lines)

**Bottleneck type:** Already well-parallelized internally. Residual: sequential forward-fill writes for non-Schwab dates.

**Internal parallelism:**
- L904: `ThreadPoolExecutor(256)` — bulk loads all positions_cube + Schwab partitions into memory
- L950–965: `ProcessPoolExecutor(fork, max_workers=cpu_count-4=60)` — per-date BD×Schwab reconciliation
- Good: per-date reconcile_date() is fully independent, 60 workers saturate CPU for Schwab dates

**Remaining bottleneck (L974–1040):** Non-Schwab forward-fill is a sequential for-loop. For each weekend/holiday date (~690 total), it reads the prior Schwab canonical file and writes the forward-filled output one at a time.

**Specific:** L984: `_read_s3(canonical_holdings_key(prior))` + L1017+: `_s3.put_object(...)` inside `for date_str in non_schwab_dates` — sequential.

**Concrete fix:** The prior-date reads collapse to a small set of distinct prior dates (~5–10 unique dates for 690 non-Schwab dates). Preload them once, then dispatch writes via `ThreadPoolExecutor(64)`.

**Estimated impact:** 690 sequential writes × ~0.08s each = ~55s → ~2s with parallel writes.

**Blocking deps:** Script-only fix.

---

### B_01 — holdings_lots.py (large, >1,600 lines)

**Bottleneck type:** Already parallelized. Residual: sequential price-file loading.

**Internal parallelism:**
- L246: `ThreadPoolExecutor(128)` — transaction loads
- L1650: `ProcessPoolExecutor(fork, FIFO_WORKERS=cpu_count-4=60)` — FIFO lot computation per account

**Remaining bottleneck (L289–303):** `load_latest_prices()` loops sequentially over silver price files: `for k in sorted(keys): raw = s3.get_object(...)`. Number of keys depends on price history depth but is O(N) sequential reads.

**Concrete fix:** Replace sequential loop with `ThreadPoolExecutor(min(len(keys), 32))`.

**Estimated impact:** If 50+ price files, ~5s → sub-1s. Minor.

**Blocking deps:** Script-only fix.

**Chain note:** B_01 depends only on A_00 output. It can run in parallel with B_00 — currently blocked by sequential dispatcher. This is the bigger win (see dispatcher section).

---

### B_01b — classify_new_securities.py

**Bottleneck type:** Trivial/fast. Watermark-gated scan of holdings_lots prefix for new security CUSIPs. Not on critical path.

**Internal parallelism:** None needed — small data, incremental by watermark.

**Blocking deps:** None.

---

### B_02 — canonical_lots.py

**Bottleneck type:** S3-I/O bound on prefix listings; internally parallelized for loads.

**comp-pipescript io shows 10 inputs including:** CANONICAL_HOLDINGS_PREFIX, SCHWAB_RLD_PREFIX, SCHWAB_ULN_PREFIX, SCHWAB_ULT_PREFIX — all date-partitioned prefixes.

**Internal parallelism:** L241: `ThreadPoolExecutor(256)` for silver allocation preloads. Per-date lot computation uses ProcessPoolExecutor.

**Remaining bottleneck:** Three Schwab prefixes (ULN/ULT/RLD) are paginated sequentially at listing time. The listing itself is fast (S3 list is paginated), but per-date lot loading inside `build_unrealized_lots_for_date()` (L323) loops over Schwab lot keys — potentially sequential inner loop per date.

**Concrete fix:** Ensure Schwab ULN/ULT per-date reads inside the worker function use `_s3.get_object()` (already fork-safe) rather than a list comprehension. Currently appears to be in the per-date worker — no change needed if ProcessPoolExecutor dispatches each date independently.

**Critical path note:** B_02 depends on B_00 canonical_holdings. B_02 and B_03 can run in parallel once B_00 completes — dispatcher currently runs them sequentially.

**Blocking deps:** Dispatcher change needed for cross-script gain.

---

### B_03 — account_gains.py (823 lines)

**Bottleneck type:** CPU-bound (gains decomposition per date). Already parallelized.

**Internal parallelism:**
- L722: `ThreadPoolExecutor(256)` — bulk load all holdings + lot prefixes into memory
- L757–765: `ProcessPoolExecutor(fork, max_workers=cpu_count-4=60)` — per-date gains computation
- Per-date worker: AUA diff, price return (merge + groupby), realized GL, unrealized GL, income

**Assessment:** This is the heaviest B script and the gate for C_00 + C_01. Already at 60-worker ProcessPool. CPU utilization for this script should be near 95%. If it's still low, suspect I/O dominates (holdings + lot prefix loads) before the compute phase.

**Remaining bottleneck:** None identified at code level. On full backfill, the 60-worker pool should keep CPU hot. On incremental (1 new date), trivially fast.

**Blocking deps:** None. Already optimal.

---

### C_00 — canonical_performance.py (355 lines)

**Bottleneck type:** S3-I/O bound on loads, then single-threaded pandas cumsum.

**Internal parallelism:**
- L193: `ThreadPoolExecutor(min(total, 256))` — parallel load of all account_gains partitions
- L310: `ThreadPoolExecutor(min(nunique_dates, 256))` — parallel writes per date

**Remaining bottleneck (L231, L268):** After bulk load, aggregation uses a single `groupby(['_date_str', 'relationship_id'])` (L231) and per-column `groupby('relationship_id').cumsum()` (L268). These are single-threaded pandas on the full concatenated DataFrame.

For a full 2,294-date backfill: gains_all could be ~2,294 dates × ~5,000 accounts/day ≈ 11.5M rows. A groupby on 11.5M rows with cumsum is O(N log N) single-threaded.

**Concrete fix:** No quick fix — groupby cumsum is inherently order-dependent. Polars would be 5–10x faster here (`groupby(...).agg(pl.col('...').cumsum())`). Medium effort, high impact.

**Estimated impact:** 11.5M row pandas groupby ~30–90s → Polars ~5–15s. Meaningful on full backfill; trivial on incremental.

**Blocking deps:** Script-only (Polars already available in layer or easily added).

---

### C_01 — canonical_nna.py

**Bottleneck type:** Sequential cumsum loop (by design), already parallelized for I/O.

**Internal parallelism:**
- L739: `ThreadPoolExecutor(256)` — bulk load all account_gains partitions
- L771–781: `ProcessPoolExecutor(fork, cpu_count-4)` — per-date NNA computation + write

**Remaining bottleneck (L389–396):** `for d in sorted_dates: ...` — sequential cumsum accumulator. This is computing running totals across dates. Inherently sequential by design (each day's cum_inflow depends on the prior day). The loop itself is O(N) Python, but the inner work is fast pandas ops on small per-date slices.

**Assessment:** Not fixable without algorithm change. For incremental (1 new date), trivially fast. For full backfill, the sequential loop adds ~1–3 min but is unavoidable.

**Chain note:** C_01 reads CLIENT_PERFORMANCE from a prior run (not the current run's C_02 output). It can run in parallel with C_00 — both depend only on B_03.

**Blocking deps:** Dispatcher change for parallel C_00 + C_01 execution.

---

### C_01b — role_aua_backfill.py (292 lines)

**Bottleneck type:** Already parallelized. Not in standard nightly chain.

**Internal parallelism:**
- L260: `ThreadPoolExecutor(WORKERS)` — parallel per-date partition writes

**Assessment:** Not in CHAIN_FULL / CHAIN_CANONICAL / CHAIN_DOWNSTREAM. One-time or on-demand backfill only. No nightly bottleneck.

---

### C_02 — client_performance.py (524 lines)

**Bottleneck type:** Well-parallelized. Gate for C_03 — wall-clock dominated by 3 parallel prefix reads.

**Internal parallelism:**
- L121: `ThreadPoolExecutor(S3_READ_WORKERS=256)` — canonical_performance prefix load
- L162: `ThreadPoolExecutor(256)` — canonical_holdings prefix load  
- L235: `ThreadPoolExecutor(256)` — canonical_account_gains prefix load
- L380: `ThreadPoolExecutor(4)` — parallel launch of load functions

**Assessment:** Reads dominate. With 256-worker ThreadPool, 3 prefixes × 2,294 keys = 6,882 parallel reads. Time dominated by S3 throughput, not Python.

**Remaining bottleneck:** The 3 prefix loads run concurrently (L380), but each pool is still bounded by S3 throughput per client. With per-region S3 limits, 256 threads may not all be active simultaneously.

**Concrete fix:** The ThreadPoolExecutor(4) at L380 launches 3 blocking loaders. The loads themselves are already parallel. No significant gain from further changes here.

**Not a bottleneck.** Fast script, well-designed.

---

### C_03 — account_performance.py

**Bottleneck type:** Fast assembler. Not a bottleneck.

**Internal parallelism:**
- L120: `ThreadPoolExecutor(S3_READ_WORKERS=256)` — account_gains prefix load
- L187: `ThreadPoolExecutor(2)` — parallel: load gains + optionally load NNA flows

**Assessment:** C_03 is a thin assembler from canonical stack. Single merge + cumsum. Fast. Wall time dominated by gains prefix load (same 2,294 keys as C_00/C_01 — loaded in parallel).

**No significant fix needed.**

---

### C_04 — validate_aua.py

**Bottleneck type:** Trivial. Validation-only, reads small JSON validation artifacts.

**S3-DYNAMIC reads:** `gold/validation/aua_validation_{*}.json` — a handful of date-keyed validation records.

**Assessment:** Fast. Not on critical path. Could run in parallel with C_03 (it reads aua_certification written by C_02 and aua_validation written by B_03/C_00 — depends on C_02).

---

### C_05 — client_tax_liability.py

**Bottleneck type:** Single-snapshot I/O. Fast.

**Reads:** Latest `holdings_lots` partition (single file from B_01 output) + latest `canonical_lots_unrealized` (single file). No date loop — reads only the most recent snapshot.

**Assessment:** Trivial wall time. More importantly: C_05 depends on B_01b (holdings_lots prefix) but NOT on C_00/C_02/C_03. In the current chain it runs after C_03 (position 11 of 14). Could move to immediately after B_01b — saving ~4 scripts worth of blocking time.

**Concrete fix:** Move C_05 to run after B_01b in the dependency-aware dispatcher. Script-level change: none needed.

**Blocking deps:** Dispatcher restructure.

---

### C_06 — client_mix_timeseries.py (906 lines)

**Bottleneck type:** Already well-parallelized. Most sophisticated script in the chain.

**Internal parallelism:**
- L571–574: `ProcessPoolExecutor(fork, 32 workers)` for partition processing
- L600: `ThreadPoolExecutor(min(len(keys), 256))` for canonical_holdings prefix preload
- L624: `ProcessPoolExecutor(32 workers)` for incremental partition processing
- L667+: Parallel `ThreadPoolExecutor` for merge + write
- Write workers: 64 (ThreadPoolExecutor)

**Remaining bottleneck (L493, L519):**
- L493: `for rel_id, grp in pos.groupby('relationship_id', sort=False)` — inside `_process_partition` (called from ProcessPoolExecutor worker). This per-relationship loop is fine — it's per-partition CPU work, and the partitions are dispatched in parallel.
- L519: `for _, row in conc_grp.iterrows()` — iterrows on concentration groups per relationship. ~50–200 rows max. Acceptable.

**Assessment:** This script already does what the PRD asks for. 32 process workers on 64 vCPU leaves room for the other concurrent scripts.

**No significant fix needed.** C_06 + C_08 should run in parallel (see dispatcher).

---

### C_07 — advisor_attribution.py

**Bottleneck type:** Fast single-pass. Not a bottleneck.

**Reads:** 2 flat files (accounts_dimension + account_performance). Single-pass groupby aggregation to produce account_team, relationship_team, rel_architect_lookup.

**L139:** `iterrows()` on advisor stats DataFrame — small (N advisors ≈ 30–50 rows). Not a concern.

**Assessment:** Wall time < 30s. Not a bottleneck. Gate for C_06 and C_08.

---

### C_08 — advisor_fee_efficiency.py (922 lines)

**Bottleneck type:** Parallelized I/O. Residual: iterrows on advisor×role aggregation.

**Internal parallelism:**
- L608: `ThreadPoolExecutor(min(len(nna_keys), S3_READ_WORKERS=256))` — parallel load of all nna_atomic partitions
- L823: `ThreadPoolExecutor(min(len(date_groups), S3_WRITE_WORKERS=256))` — parallel writes of all fee_detail partitions

**Remaining bottleneck (L429):** `for _, rr in role_merged.iterrows()` — iterrows over advisor×role breakdown. Dataset size: ~50 advisors × 5 roles = ~250 rows max. Minor but easily fixed.

**Concrete fix:** Replace L429 iterrows block with vectorized pandas operations (set_index + apply or just vectorized assignment). Saves ~100ms. Not worth prioritizing.

**ADVISOR_FEE_DETAIL_PREFIX read:** C_08 reads this prefix for existing fee_detail partitions (to avoid reprocessing). The paginator listing is sequential but listing is fast (no per-key reads). Actual data reads use `get_object` only for the NNA and role_aua latest snapshot — not per-date.

**Assessment:** Well-parallelized. Wall time dominated by nna_atomic parallel read (2,294 keys × parallel) and vectorized SCD PIT joins. Not a primary bottleneck.

**C_06 + C_08 run sequentially today but have no shared dependencies** — both depend on C_07. Should run in parallel (see dispatcher).

---

## Primary Finding: Dispatcher Sequentiality

### Problem

`gold_dispatch.sh run_chain()` (L246–271) is:

```bash
for id in $script_ids; do
    run_script "$id"
done
```

Every script waits for the prior script to fully complete regardless of whether there is a data dependency. On a 64-vCPU machine, when B_01 runs (which only needs A_00 output), B_00 is idle. When C_05 runs (which only needs B_01b), C_00 through C_03 are done but C_05 could have run 4 scripts earlier.

### Proposed parallel dispatch groupings

```
PHASE_B1:  B_00 || B_01                         (no deps between them)
PHASE_B2:  B_01b                                 (after B_01)
           B_02 || B_03                          (after B_00)
PHASE_C1:  C_00 || C_01 || C_05                  (C_00+C_01 after B_03; C_05 after B_01b)
PHASE_C2:  C_02                                  (after C_00)
PHASE_C3:  C_03                                  (after C_02)
PHASE_C4:  C_04 || C_07                          (C_04 after C_02; C_07 after C_03)
PHASE_C5:  C_06 || C_08                          (both after C_07)
```

### Implementation

Replace the sequential `run_chain()` for B+C with a `run_parallel()` helper that launches scripts as background processes, captures their PIDs, and waits for all before advancing to the next phase. Each phase is a `run_parallel(script_ids)` call; between phases is a `wait` + exit-code check.

```bash
run_parallel() {
    local pids=()
    for id in "$@"; do
        run_script "$id" &
        pids+=($!)
    done
    for pid in "${pids[@]}"; do
        wait "$pid" || { echo "ERROR: script PID $pid failed"; exit 1; }
    done
}
```

**Estimated wall-time reduction:** Conservative estimate assuming B_01 takes 15 min, C_05 takes 5 min, C_07 takes 2 min, C_06/C_08 take 20 min each:
- B_01 runs in parallel with B_00 → save ~15 min
- B_02||B_03 parallel → save slower one (say 10 min)
- C_05 moves earlier → save ~5 min (no longer waiting for C_03)
- C_06||C_08 parallel → save ~18 min (20 min becomes max(20, 20) ≈ 20 min, but saves cumulative wait)

**Total estimated savings: 30–45 min on a full backfill chain.** On incremental (1 new date), all scripts are near-instant so absolute savings are smaller but CPU idle time is proportional.

**Blocking deps:** gold_dispatch.sh change only. All scripts already write independent S3 keys — no write collisions.

---

## Prioritized TO List (D4)

| Rank | Script(s) | Bottleneck class | Change | Estimated speedup | Risk |
|------|-----------|-----------------|--------|-------------------|------|
| 1 | gold_dispatch.sh | Parallelizable-across-scripts | Parallel phase dispatcher — 8 phases with intra-phase concurrency | 35–45 min wall time reduction | Medium — phase ordering must be correct; exit-code propagation required |
| 2 | C_00 | Pandas-CPU bound | Polars groupby + cumsum replacing L231 + L268 pandas ops | 30–90s → 5–15s on full backfill | Medium — Polars migration, test cumsum correctness |
| 3 | B_00 | S3-I/O bound | ThreadPoolExecutor for non-Schwab forward-fill writes (L974–1040) | ~55s → ~2s | Low — write path only, no compute change |
| 4 | B_01 | S3-I/O bound | ThreadPoolExecutor for price-file sequential load (L302) | ~5s → < 1s | Low |
| 5 | C_08 | Pandas-CPU bound | Replace L429 iterrows with vectorized ops | ~100ms | Low — trivial refactor |

---

## CTO Hypothesis Verdict

> "C scripts are on the critical path."

**CORRECT** for the current sequential chain: B_03 → C_00 → C_02 → C_03 → C_07 → C_06/C_08 is the critical path. C_06 and C_08 are the terminal compute-heavy scripts.

**BUT**: The reason CPU is at 5% is not that C scripts are slow — it's that B+C scripts are serialized. Most scripts are already internally parallelized at 60 ProcessPool workers. The machine goes idle because Script N+1 waits for Script N even when there is no data dependency.

The fix that gets CPU utilization to 40%+ is the dispatcher phase restructure, not per-script optimization. Per-script fixes (Polars in C_00, B_00 forward-fill) are secondary.

---

## What's Not a Bottleneck

- B_01b: trivial watermark-gated scan
- C_01: sequential cumsum is by design (date-ordered cumulative); ProcessPool handles per-date writes
- C_02: thin assembler, already 3×256-thread parallel reads
- C_03: thin assembler, same
- C_04: validation-only, fast
- C_05: single-snapshot reads, fast
- C_07: single-pass groupby, fast

---

*Delivered by 0.4.0_DS_ClientPlatform~B | 2026-04-16*
