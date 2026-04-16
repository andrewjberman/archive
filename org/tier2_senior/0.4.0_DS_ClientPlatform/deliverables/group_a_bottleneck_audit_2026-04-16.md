# Group A Gold Script Bottleneck Audit
**Prepared by:** 0.4.0_DS_ClientPlatform~C
**Date:** 2026-04-16
**PRD:** docs/architecture/GOLD_PERF_PRD.md
**Scope:** A_00, A_01, A_02, A_03, A_04

---

## 1. Inter-Script Dependency Graph (A group)

All A scripts read from `accounts_dimension_latest.parquet` (A_00's output). Within the group:

| Script | Reads from (A group) | Writes to | Can start when |
|--------|---------------------|-----------|----------------|
| A_00 | — | `accounts_dimension_latest.parquet` → all others | Immediately |
| A_01 | A_00 (accounts_dimension) | `advisor_assignments_history.parquet` | After A_00 |
| A_02 | A_00 (accounts_dimension) | `fee_rate_history.parquet` | After A_00 |
| A_03 | A_00 (accounts_dimension) | `positions_cube/{date}.parquet` | After A_00 |
| A_04 | A_00 (accounts_dimension) | `client_dimension.parquet` | After A_00 |

**Parallelization potential:**
- Wave 1: A_00 alone (must run first)
- Wave 2: A_01, A_02, A_03, A_04 — fully concurrent (all read A_00's output, no inter-dependencies)

**Current execution: 5 scripts in series. With dispatch restructure: 2 waves.**
A_01–A_04 running concurrently cuts A-group wall time by up to 4x after A_00.

---

## 2. Per-Script Bottleneck Classification

### A_00 — accounts_dimension.py (735 lines)
**Primary class:** Already-parallelized (S3 reads via TPE)

| Type | Location | Detail |
|------|----------|--------|
| TPE | L215–222 | `ThreadPoolExecutor(max_workers=128)` for transaction parquet reads — GOOD |
| iterrows | L246 | `build_history_for_account()`: iterates deduplicated daily transactions per account — **bounded by per-account row count**, not full table. Low impact. |
| Sequential S3 | L336 | Single `get_object()` for latest allocation in `load_alloc_enrichment()` — one-time reference read, acceptable |
| Vectorization | — | All DataFrame ops vectorized. No apply(axis=1). |

**Bottleneck:** None significant. A_00 is S3-read-parallelized and compute-vectorized.
**Concrete fix:** None required. Minor: pull allocation read at L336 into the main TPE if other reads are in-flight at same time.
**Est. impact:** < 1 min

---

### A_01 — advisor_assignments.py (548 lines)
**Primary class:** Pandas-CPU bound (`.at[]` row updates in SCD normalization loop)

| Type | Location | Detail |
|------|----------|--------|
| **MEDIUM iterrows** | L316–343 | `_normalize_multi_role_splits()`: `for idx in history.index:` with **`.at[idx, split_col] = avg`** on each iteration — row-by-row DataFrame updates. Scales with SCD record count (~thousands). `.at[]` is 100–1000x slower than vectorized assign. |
| LOW iterrows | L246 | `build_history_for_account()`: per-account daily dedup, bounded by account transaction count. Acceptable. |
| TPE | L175–185 | `ThreadPoolExecutor(max_workers=64)` for transaction reads — GOOD |
| Sequential S3 | L209 | Single accounts_dimension load — one-time reference, acceptable |

**Concrete fix (L316–343):** Replace `.at[]` loop with vectorized `DataFrame.loc[]` bulk assign:
```python
# BEFORE: row-by-row .at[] updates
for idx in history.index:
    for role_col, split_col in available:
        avg = ...
        history.at[idx, split_col] = avg  # SLOW

# AFTER: vectorized per-group assignment
mask = ...  # boolean mask for multi-role rows
history.loc[mask, split_col] = history.loc[mask].apply(
    lambda r: compute_avg_split(r, role_col, split_col), axis=1
)
# Or better: precompute avg as a Series and .loc[] bulk assign
```
**Est. impact:** 2–4 min → < 1 min (SCD dataset ~thousands of records; `.at[]` penalty compounds)

---

### A_02 — fee_rate_history.py (456 lines)
**Primary class:** Already-parallelized

| Type | Location | Detail |
|------|----------|--------|
| TPE | L141–151 | `ThreadPoolExecutor(max_workers=64)` for fee parquet reads — GOOD |
| LOW iterrows | L205 | `build_fee_history_for_account()`: per-account daily dedup, bounded. Acceptable. |
| LOW iterrows | L376 | `cross_validate_allocations()`: `mismatches.head(10).iterrows()` — 10 rows max, logging only |
| Sequential S3 | L337 | Single allocation read for validation — one-time, acceptable |

**Bottleneck:** None significant. A_02 mirrors A_00/A_01 pattern and is well-optimized.
**Concrete fix:** None required.
**Est. impact:** N/A

---

### A_03 — positions_cube.py (1,739 lines)
**Primary class:** Already-parallelized (most sophisticated parallelism in the A group)

| Type | Location | Detail |
|------|----------|--------|
| ProcessPoolExecutor | L1145–1147 | `ProcessPoolExecutor(max_workers=max(cpu_count-4, 4), mp_context='fork')` for position-pair expansion — **correct choice for CPU-bound work**. Uses all available cores. |
| TPE (reads) | L869–876 | `ThreadPoolExecutor(max_workers=128)` for transaction reads |
| TPE (writes) | L1282–1285, L1293–1301 | `ThreadPoolExecutor(max_workers=64)` for partition prep + writes |
| LOW iterrows | L1122 | `expand_pairs_to_daily()`: `itertuples()` over `group_meta` to build work items for ProcessPool — metadata only (~10K groups max). Low impact (one-time setup). |
| Sequential S3 | L150, 173, 223, 373, 386, 514, 533, 653, 666, 691 | 9 single `_read_parquet_from_s3()` calls — all reference files (allocations, prices, unrealized). All one-time lookups. Acceptable. |

**Bottleneck:** None. A_03 is the best-engineered script in the group — ProcessPool for CPU, ThreadPool for I/O, configurable worker counts, Windows fallback, no row-wise operations.
**Concrete fix:** None required. Already saturating cores during pair expansion.
**Est. impact:** N/A

---

### A_04 — client_dimension.py (477 lines)
**Primary class:** Already-parallelized

| Type | Location | Detail |
|------|----------|--------|
| TPE | L112–115 | `ThreadPoolExecutor(max_workers=64)` for transaction reads — GOOD |
| iterrows | None | Zero iterrows in the script |
| Sequential S3 | L72 | Single accounts_dimension read in `load_accounts()` — one-time reference, acceptable |
| Vectorization | L158, L298–300, L312 | All operations vectorized (str.contains, agg lambdas, groupby agg). No apply(axis=1). |

**Bottleneck:** None. A_04 is clean.
**Concrete fix:** None required.
**Est. impact:** N/A

---

## 3. Summary Table

| Script | Lines | Primary Class | Critical Issues | TPE/PPE | Est. Current Wall Time | Fix |
|--------|-------|--------------|-----------------|---------|----------------------|-----|
| A_00 | 735 | Already-parallelized | None | TPE 128 (reads) | 3–6 min | None |
| A_01 | 548 | Pandas-CPU bound | L316–343 `.at[]` loop | TPE 64 (reads) | 4–8 min | Vectorize SCD update loop |
| A_02 | 456 | Already-parallelized | None | TPE 64 (reads) | 2–4 min | None |
| A_03 | 1,739 | Already-parallelized | None | TPE 128 + PPE all-cores + TPE 64 writes | 8–20 min | None |
| A_04 | 477 | Already-parallelized | None | TPE 64 (reads) | 2–4 min | None |

---

## 4. Prioritized Remediation TO List (A group)

| Priority | Script | Bottleneck Class | Specific Change | Est. Speedup | Risk |
|----------|--------|-----------------|-----------------|--------------|------|
| P1 | Dispatcher | Parallelizable-across-scripts | Wave 2: run A_01, A_02, A_03, A_04 concurrently after A_00. A_03 is the longest (up to 20 min) — if others finish in 4–8 min while A_03 runs, A-group wall time = A_00 + A_03 instead of A_00 + A_01 + A_02 + A_03 + A_04 | ~3x A-group wall time | Low (no script changes) |
| P2 | A_01 | Pandas-CPU bound | L316–343: Replace `.at[]` loop with vectorized bulk assign on SCD normalization | 3–8x A_01 alone | Low |

**A group finding: the primary bottleneck is dispatch serialization, not intra-script compute.** A_03 uses ProcessPool correctly and already saturates cores during expansion. The inter-script gain (P1) dwarfs any intra-script fix.
