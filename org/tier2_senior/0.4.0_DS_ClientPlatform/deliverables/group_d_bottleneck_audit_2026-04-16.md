# Group D Gold Script Bottleneck Audit
**Prepared by:** 0.4.0_DS_ClientPlatform~C
**Date:** 2026-04-16
**PRD:** docs/architecture/GOLD_PERF_PRD.md
**Scope:** D_00, D_00b, D_00c, D_01, D_02, D_03, D_04

---

## 1. Inter-Script Dependency Graph (D group)

The critical question from COO/CTO: can D scripts run concurrently? **Yes — with structure.**

D_04 is the only terminal aggregator. All other D scripts feed it. But within that, there are three real D→D dependencies that define the critical path:

```
Wave 1 (concurrent, fire immediately):
  D_00          — writes aua_certification → needed by D_00b, D_01
  D_00c         — no D→D read deps (reads C-group + canonical only)
  D_03          — no D→D read deps (reads C-group + canonical only)

Wave 2 (after D_00 completes):
  D_00b         — reads aua_certification_key from D_00
  D_01          — reads aua_certification_key from D_00

Wave 3 (after D_01 completes):
  D_02          — reads canonical_role_aua_key updated by D_01

Wave 4 (after all above):
  D_04          — reads from D_00, D_00b, D_00c, D_01, D_02, D_03
```

**Current execution: 7 scripts in series.**
**With concurrent dispatch: 4 waves, D_00c and D_03 run free in Wave 1.**

Critical path: D_00 → D_01 → D_02 → D_04

The aua_certification cross-reads between D_00 and D_01 (each reads the other's cert) are prior-run baseline reads — not blocking serial deps for the current run. The canonical_role_aua cross between D_01 and D_02 is real: D_01 updates the canonical store, D_02 reads the updated version.

**Dependency source:** comp-pipescript io + gold_pipeline_deps.yaml (no additional D→D declarations in deps YAML; aua_certification and canonical_role_aua cross-reads are implicit via the S3 manifest).

---

## 2. Per-Script Bottleneck Classification

### D_00 — portal_aggregates.py
**Primary class:** S3-I/O bound (marginal) / Already-parallelized

| Type | Detail |
|------|--------|
| ThreadPoolExecutor | `load_all()` (L294-318): 4 workers, parallelizes perf + cdim + adim + tax reads — GOOD |
| Sequential S3 reads | L238: `_load_aua_certification()` — single get_object, not in pool. Low impact (one call). |
| iterrows | L498 (tax cost_basis loop), L513 (top_gain_positions cap=20), L571 (client_list_df) — all small-N (<100 rows), low impact |
| Vectorization | No major un-vectorized DataFrame ops detected |

**Estimated impact:** D_00 is likely already near its floor. Minor gain from pulling aua_certification into the main TPE pool.
**Concrete fix:** Add aua_certification load as a 5th future in `load_all()` TPE at L294. 1-line change.
**Est. impact:** < 1 min

---

### D_00b — portal_timeseries.py
**Primary class:** Pandas-CPU bound (iterrows on full account_team, nested iterrows)

| Type | Location | Detail |
|------|----------|--------|
| **CRITICAL iterrows** | L233 | `_build_account_office_dim_d00b()`: iterates full account_team (unbounded) to map account → office via priority chain. Should be a merge on office priority columns. |
| **CRITICAL iterrows** | L259 | `_build_rel_office_dim_d00b()`: iterates full account_team again for relationship→office mapping. Same fix: merge + groupby. |
| **HIGH iterrows** | L1105 | `_nna_drill_data()`: **nested** — outer `groupby('date')`, inner `iterrows()` on each date group. Cascades O(dates × accounts). Replace with `groupby(['date', ...]).apply()`. |
| **LOW iterrows** | L847, L866, L887, L905, L933, L980, L996 | JSON-formatting list/dict comprehensions, bounded by TOP_N (9-20 rows each). Acceptable. |
| S3 reads | All multi-file reads (role_aua, NNA, holdings_lots) are inside TPE — GOOD | |
| TPE | L338, L474, L692, L1293: 4 TPE pools, well-distributed | |

**Concrete fixes:**
1. L233 `_build_account_office_dim_d00b()`: Replace iterrows with `account_team.sort_values(office_priority_col).groupby('relationship_id').first()['office_id']` merge pattern.
2. L259 `_build_rel_office_dim_d00b()`: Same — `groupby('relationship_id').agg({'office': lambda x: x.mode()[0]})` merge.
3. L1105 `_nna_drill_data()`: Replace `for dt, dt_grp in daily.groupby('date'): for _, row in dt_grp.iterrows()` with `daily.groupby('date').apply(lambda g: g.to_dict('records'))`.

**Est. impact:** 10–20 min → 3–6 min (L233/259 are the heaviest; account_team is full-table width)

---

### D_00c — portal_leaderboard.py
**Primary class:** Pandas-CPU bound (advisor entry builder, apply(axis=1) weight resolver)

| Type | Location | Detail |
|------|----------|--------|
| **CRITICAL iterrows** | L505 | `_employee_entries_for_window()`: itertuples over all advisors (200+), builds complex nested dict per advisor including role_breakdown, fee_breakdown, rank fields. Most expensive single loop in D_00 group. |
| **HIGH apply(axis=1)** | L800-803 | Split-weight resolver: `apply(lambda r: ..., axis=1)` with conditional dict lookups on full account_team. Three-case rule requires row-wise eval; NumPy `.where()` chain could replace for 2-case branches. |
| **MEDIUM iterrows** | L227 | `_compute_tagged_window_metrics()`: iterates aggregated adv_sum (all advisors) to build metrics dict. Replace with `adv_sum.set_index('advisor').to_dict('index')`. |
| **MEDIUM iterrows** | L290 | `_compute_tagged_window_metrics_by_role()`: iterates (advisor, role) pairs. Same: `grp.set_index(['advisor','role']).to_dict('index')`. |
| S3 reads | L93, L139: multi-file reads inside TPE — GOOD | |
| TPE | L1096: 8-worker pool for 8 source parquets in load_for_leaderboard — GOOD | |

**Concrete fixes:**
1. L505: Convert to two passes — (a) vectorized aggregation to build flat DataFrame of all entry fields, (b) single `df.to_dict('records')` for serialization. Role_breakdown and fee_breakdown can be built as nested DataFrames then `groupby().apply(lambda g: g.to_dict(...))`.
2. L227/290: `adv_sum.set_index('advisor').to_dict('index')` replaces iterrows. Same for role pairs.
3. L800-803: Decompose into 3 vectorized `np.where()` branches where branch conditions are mutually exclusive boolean masks.

**Est. impact:** 15–25 min → 5–8 min (L505 and L800 are the bottleneck pair)

---

### D_01 — partner_analytics.py
**Primary class:** Pandas-CPU bound (highest iterrows count in D group)

| Type | Location | Detail |
|------|----------|--------|
| **HIGH iterrows** | L1116-1145 | Advisor daily segmentation: iterates `adv_day` (all advisors per date) building segments with nested account filtering. Full-table, per-date outer loop compounds this. |
| **HIGH iterrows** | L984-990 | Rebuilds `_ap_aua` lookup dict and advisor AUA per-day from account_performance + account_team. Should be precomputed outside the date loop as a MultiIndex lookup. |
| **HIGH iterrows** | L1882-1916 | Office/role mapping build: iterates full account_team twice (L1882 for office, L1906 for architect) — same pattern as D_00b L233/259. |
| **MEDIUM iterrows** | L803-809 | Geo daily state segments — iterates state summary per date. |
| **MEDIUM iterrows** | L906-918 | City rankings with nested state query. |
| **MEDIUM iterrows** | L1358-1374, L1437-1448, L1544-1561, L2029-2038, L2195-2212 | NNA segment builders (advisor, geo, office) — repeated pattern, all unbounded by advisor count. |
| **MEDIUM iterrows** | L1180-1198 | Top client builder — bounded by TOP_N (acceptable). |
| Sequential S3 reads | L2404-2409 | `_load_role_aua_snapshot()` called 4 times in a loop (4 periods). Should be parallelized with TPE. |
| TPE | L327-330: 7-worker pool for main data load — GOOD. No write parallelism (single-object writes). |

**Concrete fixes:**
1. L984-990: Precompute `ap_aua_lookup = account_performance.set_index(['date','relationship_id'])['total_aua']` before any date loop. Replace inner loop with `.loc[(date, rel_id)]` lookups.
2. L1882-1916: Same vectorized merge fix as D_00b L233 — `account_team.groupby(['relationship_id'])` aggregation instead of row iteration.
3. L2404-2409: Wrap 4 `_load_role_aua_snapshot()` calls in `ThreadPoolExecutor(max_workers=4)`.
4. L1116-1145, L803-809, L1358-1374 etc.: These are JSON-serialization loops — convert aggregated DataFrames to `to_dict('records')` and restructure downstream.

**Est. impact:** 20–35 min → 8–12 min (D_01 is likely the single longest D script)

---

### D_02 — advisor_client_detail.py
**Primary class:** Pandas-CPU bound (highest iterrows count: 15 loops) + S3-I/O (holdings_lots post-pool)

| Type | Location | Detail |
|------|----------|--------|
| **CRITICAL iterrows** | L1808-1843 | Canonical role_aua lookup build with cumsum arrays per group: 3 nested loops over sorted groups/advisors. Precompute as MultiIndex DataFrame. |
| **HIGH iterrows** | L1924-1945, L2034-2046, L2085-2095 | Timeseries builders (advisor, relationship, account): row-by-row JSON construction for each entity. Convert to `groupby().apply(lambda g: g[cols].to_dict('list'))`. |
| **HIGH iterrows** | L2496, L2501 | Dict comprehensions with iterrows on rel_totals — `rel_totals.set_index('relationship_id').to_dict()` replaces both. |
| **MEDIUM iterrows** | L651-671 | Implementor change entries — bounded by change count, moderate. |
| **MEDIUM iterrows** | L1375-1405 | Client list builder — all clients, JSON construction per row. `to_dict('records')` pattern. |
| **MEDIUM iterrows** | L2526-2529 | share_daily_lookup build after groupby — `groupby().agg().to_dict()`. |
| **LOW iterrows** | L785-799, L822-831, L1040-1048, L1120-1122, L2276, L2309, L2631 | Position/year/account builders, bounded by TOP_N or small aggregates. |
| **HIGH S3 read** | L499-520 | holdings_lots sequential read AFTER main TPE pool completes — add as future inside main pool (L427-470). |
| TPE | L427-470: 8-worker load pool — GOOD. L146-168: parallel writes — GOOD. |

**Concrete fixes:**
1. L1808-1843: `canon_df.set_index(['date','advisor','role'])` → direct `.loc[]` lookup replaces 3 nested loops.
2. L1924-1945, L2034-2046, L2085-2095: `df.groupby(entity_key)[value_cols].apply(lambda g: g.values.tolist())` → dict → JSON.
3. L499-520: Move holdings_lots read into the main TPE pool at L427-470 as `fut_lots`.
4. L2496/L2501: `rel_totals.set_index('relationship_id')[col].to_dict()` — 2-line fix.

**Est. impact:** 25–40 min → 10–15 min (D_02 is the most iterrows-dense script)

---

### D_03 — composition_artifacts.py
**Primary class:** S3-I/O bound (no parallel reads — only writes are parallelized)

| Type | Location | Detail |
|------|----------|--------|
| **CRITICAL S3** | L270, L578, L630, L639 | All data loads (`_read_parquet()`) are sequential — account_performance, holdings_lots, architect lookup (2 calls). No TPE for reads. |
| **MEDIUM iterrows** | L678 | `lots[['relationship_id','architect']].drop_duplicates().iterrows()` building per-architect AUA lookup. Replace with `lots.groupby('architect')['total_aua'].sum().to_dict()`. |
| **LOW iterrows** | L356, L387 | Top holdings builders, TOP_N=9 — acceptable. |
| TPE | L195-204: write batch only (64 workers). No read parallelism. |

**Concrete fixes:**
1. Add `load_for_composition()` function with `ThreadPoolExecutor(max_workers=4)` parallelizing: account_performance, holdings_lots prefix (paginate + parallel load), firm_composition, mix_daily_summary.
2. L678: `lots.groupby('architect')['total_aua'].sum().to_dict()` replaces iterrows.

**Est. impact:** 8–15 min → 2–4 min (D_03 is almost entirely S3-bound on reads; parallelizing loads is the entire fix)

---

### D_04 — client_portal_summary.py
**Primary class:** S3-I/O bound (terminal assembler — 23 reads, large platinum write volume)

| Type | Location | Detail |
|------|----------|--------|
| **HIGH S3 read** | L363-365 | 3 firm JSON reads (EMPLOYEE_LEADERBOARD, CLIENTS_TAB, ADVISOR_FEE_EFFICIENCY) called sequentially via `_read_json()` — not in batch reader. Should use `_batch_read_json()`. |
| **MEDIUM iterrows** | L223-235 | Account AUA histogram build — mirrors D_01 L223. Precompute with groupby. |
| **LOW iterrows** | L1314-1338, L1687-1700 | Top holdings (TOP_N=10) and inflow/outflow dict — small-N, acceptable. |
| TPE | L283-293 (writes), L301-310 (batch JSON reads), L1632-1637 (batch parquet reads) — GOOD. Platinum writes already fully parallelized with 64 workers. |

**Concrete fixes:**
1. L363-365: Replace 3 sequential `_read_json()` calls with `_batch_read_json([EMPLOYEE_LEADERBOARD, CLIENTS_TAB, ADVISOR_FEE_EFFICIENCY])`.
2. L223-235: `account_team.groupby('architect')['total_aua'].agg(list).to_dict()` replaces iterrows.

**Est. impact:** Moderate. D_04 is already well-parallelized on writes. Main gain from L363 batch read and Wave 4 scheduling ensuring it doesn't start until all predecessors complete.

---

## 3. Dependency Map Summary

| Script | Reads from (D group) | Writes to (D group) | Can start when |
|--------|---------------------|--------------------|----|
| D_00 | — | D_00b (aua_cert), D_01 (aua_cert), D_04 | Immediately (Wave 1) |
| D_00b | D_00 (aua_cert) | D_04 | After D_00 (Wave 2) |
| D_00c | — | D_04 | Immediately (Wave 1) |
| D_01 | D_00 (aua_cert) | D_02 (role_aua), D_04 | After D_00 (Wave 2) |
| D_02 | D_01 (role_aua) | D_04 | After D_01 (Wave 3) |
| D_03 | — | D_04 | Immediately (Wave 1) |
| D_04 | D_00, D_00b, D_00c, D_01, D_02, D_03 | platinum (terminal) | After all (Wave 4) |

**Critical path:** D_00 → D_01 → D_02 → D_04 (4 serial hops)
**Free lanes:** D_00c and D_03 run fully concurrent in Wave 1 with no blocker.

---

## 4. Prioritized Remediation TO List

| Priority | Script | Bottleneck Class | Specific Change | Est. Speedup | Risk |
|----------|--------|-----------------|-----------------|--------------|------|
| P1 | Dispatcher | Parallelizable-across-scripts | Restructure gold_dispatch.sh D-group execution into 4 waves per dependency map above | 3–4x D-group wall time | Low (no script changes) |
| P2 | D_03 | S3-I/O bound | Add `load_for_composition()` with TPE(max_workers=4) covering all 4 sequential reads | 4–5x D_03 alone | Low |
| P3 | D_02 | Pandas-CPU bound | L1808-1843 MultiIndex lookup + L1924-2095 timeseries builders → `to_dict` pattern + holdings_lots into main pool | 2–3x D_02 alone | Medium |
| P4 | D_01 | Pandas-CPU bound | L984 precompute ap_aua_lookup + L2404 TPE for 4 role_aua snapshot loads + L1882 office merge vectorization | 2x D_01 alone | Medium |
| P5 | D_00b | Pandas-CPU bound | L233/259 account_team office mapping → merge; L1105 nested iterrows → groupby.apply | 3–4x D_00b alone | Medium |
| P6 | D_00c | Pandas-CPU bound | L505 advisor entry builder → vectorized flat DataFrame + to_dict; L227/290 → set_index.to_dict | 2–3x D_00c alone | Medium |
| P7 | D_04 | S3-I/O bound | L363-365 sequential firm JSON reads → _batch_read_json | < 1 min | Low |
| P8 | D_00 | Already-parallelized | Add aua_certification load as 5th future in load_all() TPE | < 1 min | Low |

**P1 (dispatcher restructure) is highest leverage: no script changes, pure orchestration, and captures all cross-script parallelism immediately.** Estimated D-group wall time reduction: 7-script serial chain → 4-wave concurrent execution = 3–4x wall time reduction before any intra-script fixes.

Combined with P2–P6 intra-script fixes, target 40%+ CPU utilization during D-group execution is achievable.

---

## 5. Notes on CTO Hypothesis Validation

**Hypothesis 3 (D scripts parallelizable): CONFIRMED with structure.**
D_00c and D_03 are fully free. D_00b and D_01 gate on D_00 (fast, Wave 1). D_02 gates on D_01 (slow — critical path). D_04 gates on all. This is not "run all 7 concurrently" but it's 4 waves vs. 7 sequential scripts — meaningful compression.

The binding constraint on total D-group time after dispatcher restructure is the D_01 → D_02 → D_04 serial chain. D_01 and D_02 are the heaviest scripts by iterrows count (13 and 15 respectively). Intra-script fixes on those two (P3, P4) are the highest-leverage CPU improvements after the dispatcher restructure (P1).
