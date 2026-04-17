# Gold Chain Performance — Empirical Analysis
**Agent:** 0.4.0_DS_ClientPlatform~B
**Date:** 2026-04-17
**Source:** `[PERF]` entries in `s3://opal-data-bd/logs/gold-layer/gold_full_2026-04-17_20260417_012341.log` and B_01 `--single` re-run `perf_report.json` @ 2026-04-17T02:56:59Z
**PRD:** `docs/architecture/GOLD_PERF_PRD.md`
**Audit under scrutiny:** `gold_perf_bottleneck_audit_group_bc_2026-04-16.md` (5f8d5c88)

**Caveat:** PROD full-chain run at 04:00 UTC is the definitive artifact. This document covers only the QA full-chain run that halted at B_01. C/D-group empirical data is deferred to Section 2 (post-04:00 UTC).

---

## 1. Data Summary Table

QA full chain run, 2026-04-17 01:00:16Z through 01:23:41Z. Chain halted on B_01 RPS safety guard.

| Script | wall_s | cpu_avg_% | mem_peak_MB* | Notes |
|---|---:|---:|---:|---|
| build_canonical_prices_v2 (S_00) | 103.6 | 3.27 | 239,315 | silver prep, pre-gate |
| A_00 accounts_dimension | 60.5 | 2.76 | 8,129 | |
| A_01 advisor_assignments | 51.3 | 3.91 | 3,141 | |
| A_02 fee_rate_history | 26.0 | 4.22 | 5,086 | trivial |
| A_03 positions_cube | **558.8** | 10.32 | 227,378 | **A-group dominator** |
| A_04 client_dimension | 32.6 | 6.21 | 2,165 | trivial |
| B_00 canonical_holdings | 217.9 | 6.93 | 799,801 | |
| B_01 holdings_lots (pre-fix) | **1408.6** | 1.81 | 530,933 | **halted on RPS safety** |
| B_01 holdings_lots (post-fix, --single) | 117.2 | 4.86 | 529,215 | **12x improvement after stale-RPS + df.attrs fixes** |

\* **Mem peak is untrustworthy** — values exceed 128 GB physical RAM on c6i.16xlarge (e.g. B_00 reports 780 GB, A_03 222 GB, build_canonical_prices 234 GB). Instrumentation is almost certainly summing RSS across subprocess workers or counting virtual memory. Disregard column for absolute sizing; relative ordering may or may not be meaningful. D1 instrumentation is owed a fix here.

**Full-chain QA wall to halt:** 2459.3s (41 min) sequential.
**Max single-script wall:** B_01 pre-fix 1408.6s = 57% of chain time.
**Sum of A-group:** 729.2s (A_03 alone = 76% of A-group).

---

## 2. PRD Hypothesis Scorecard

**Hypotheses from `docs/architecture/GOLD_PERF_PRD.md`:**

| # | Hypothesis | Status | Evidence |
|---|---|---|---|
| H1 | A group is I/O-bound, not compute-bound (suspect 5-10x via parallel batch reads) | **PARTIALLY VALIDATED** | All A scripts 2.76-10.32% CPU. Low CPU across the board is consistent with I/O-bound, BUT A_03 at 558.8s is 11x longer than the next A script, not evenly distributed I/O. Something specific in A_03 is the actual sink. Parallelizing A as a group saves ~15-20% because A_03 dominates, not the advertised 5-10x. |
| H2 | C scripts are the critical path | **DEFERRED** | Chain halted before any C script ran. Cannot confirm from this run. |
| H3 | D scripts are parallelizable | **DEFERRED** | Chain halted before D. |
| H4 | S3 writes are blocking unnecessarily | **DEFERRED** | No s3_reads / s3_writes in perf_report (instrumentation nulled). Cannot quantify. |

Section 2 APPEND (post-04:00 UTC PROD): C/D-group perf data will be appended when `perf_report.json` for the full PROD chain lands on S3.

---

## 3. Audit Predictions vs. Empirical Observations

### Where the audit was right

- **Primary finding: dispatcher sequentiality dominates.** Every measured script ran at 2-10% CPU avg. The 64-vCPU machine is idle 90%+ of the time even when ProcessPoolExecutor is in the script. Audit claim confirmed.
- **B_01 price loader a "minor" win.** Audit ranked this Rank 4 ("~5s saved"). Log confirms: "Loading canonical prices... 11,183,142 rows loaded ... 43.6s" — already fast before the 22736cf7 parallelization. Rank was correct.
- **B_01b, C_04, C_05, C_07 listed as trivial/fast.** Cannot verify for C scripts. A_04 (not in my scope) did come in at 32.6s, consistent with "thin assembler" intuition.

### Where the audit was wrong

- **B_00 "already well-parallelized, CPU should be near 95%"** — **WRONG.** Actual 6.93% CPU. My audit read the ProcessPoolExecutor code at L950 and concluded the script saturates cores; the data says it doesn't. Either the ProcessPool dispatches too briefly relative to the surrounding I/O setup, or the per-date worker workload is itself I/O-bound. Audit over-indexed on code structure and didn't predict the actual utilization profile.
- **B_01 L302 price loader called out as the fix.** Technically correct as a parallelization, but cosmetic: the price loader was 43.6s in a 1408.6s script. The real wall-time sink was the RPS sell_correction injection and downstream force-close processing, which the audit did not examine because it's not a loop-over-dates-and-read-from-S3 pattern. **The audit looked for S3 loops and missed compute-heavy in-place transforms.**
- **"Polars port for C_00 = 5-10x on 11.5M rows"** — **UNVERIFIED.** Chain halted before C_00. Port is shipped (f177240b). Claim rests on Polars marketing + my pandas-vs-Polars prior, not on measurement. Will be validated or refuted by PROD run.
- **Group A was out of scope for ~B's audit** (assigned to ~C). So not strictly a ~B miss. But the audit's architectural claim "A group is I/O-bound with room for 5-10x parallel reads" (from PRD H1) is contradicted by the data — A_03 alone is 76% of A-group wall and no amount of A-group dispatch parallelization fixes that. The A-group needs **intra-script** optimization in A_03, not inter-script.

### Net assessment

The audit's **ranking was directionally right** (dispatcher first, Polars/TPE second). It was **wrong on which scripts needed work**:
- It didn't identify A_03 as a problem because A wasn't in scope.
- It said B_00 was "done." Data says B_00 is doing I/O-bound sequential work wrapped in a ProcessPoolExecutor shell — the pool isn't actually saturating.
- It missed the RPS sell_correction loop in B_01 because that path wasn't a visible S3 loop pattern.

---

## 4. Surprises + New Bottlenecks

### S1 — A_03 positions_cube is the A-group whale (558.8s, 10.32% CPU)

Not in either ~B or ~C's original bottleneck audit scope as a priority item. 558.8s at ~10% CPU = ~52s of single-core compute + ~505s of I/O wait. This is the second-largest wall-time script in the chain after pre-fix B_01. Not explored in any audit. Needs a dedicated I/O read review.

### S2 — B_00 cpu_avg only 6.93% despite ProcessPoolExecutor

B_00 code has `ProcessPoolExecutor(fork, max_workers=cpu_count-4=60)` at L950. Observed CPU avg: 6.93%. Interpretation: the ProcessPool does work, but the dominant wall time is the pre-pool bulk-load-into-memory phase (L904 ThreadPoolExecutor(256) reading thousands of partitions) and the sorted-Schwab-date forward-fill phase (L974). The compute phase is short relative to I/O. The audit's mental model of "B_00 is CPU-saturated by the ProcessPool" is wrong.

### S3 — B_01 stale-RPS + df.attrs fixes produced a 12x speedup, not a rounding win

a9f42c3b (stale-RPS auto-skip) + b320426b (df.attrs wipe) dropped B_01 from 1408.6s to 117.2s. That's a 1291s saving on a single script — larger than the combined theoretical savings across all of my audit's Rank 2-5 items. The real bottleneck was operational (stale Schwab data causing a hung RPS injection path), not compute. No audit of code-level bottlenecks would have surfaced this; only live execution did.

### S4 — Mem instrumentation is broken

`mem_peak_MB` consistently reports values > 128 GB physical RAM. Almost certainly summing RSS across forked subprocesses or misreading procfs virtual size. Cannot use mem column for decision-making until D1 perf instrumentation is fixed.

### S5 — s3_reads / s3_writes counters return N/A

Every row shows `s3_reads=N/A  s3_writes=N/A`. The instrumentation collects wall/CPU/mem but not S3 ops. H4 from PRD ("S3 writes blocking unnecessarily") cannot be tested without this.

---

## 5. Next-Priority Optimizations — Empirical Ranking

Ranked by **observed wall-time impact** from this single QA chain, not theoretical estimates.

| Rank | Target | Observed wall | Fix class | Expected empirical gain |
|---|---|---:|---|---|
| 1 | A_03.positions_cube | 558.8s | Unknown — needs profiling pass. I/O batch reads, vectorization, or parallelism. | Target 100-200s (3-5x). Single biggest remaining improvable script. |
| 2 | B_00.canonical_holdings | 217.9s | Audit said "done" but 6.93% CPU says otherwise. Investigate: is the ProcessPool actually dispatching, or is wall time dominated by the pre-pool I/O bulk-load? If the latter, parallelize the 2,294-partition read with larger TPE or s3transfer multipart concurrency. | Target 80-100s (2-3x). |
| 3 | Dispatcher phase parallelization (gold_dispatch.sh) | -- | Independent of per-script. Deploys the 10-phase map from 856855f3 DAG validation. A_02 / A_04 trivial; A_03 is the serialization gate. Savings dominated by PHASE_B3 (B_03 \|\| C_05) and PHASE_C5 (C_06 \|\| C_08). | Estimate 20-30% chain wall reduction, but hard to pin without C/D data. |
| 4 | Restore D1 instrumentation — s3_reads/s3_writes and a sane mem metric | -- | Essential for future audits. Without these, the PRD's H4 cannot be tested and we cannot distinguish I/O-bound from memory-bound scripts. | Prerequisite for further empirical work. |
| 5 | B_01 price loader TPE (already shipped, 22736cf7) | ~5s saved | Shipped, keep. Cosmetic scale. | Already realized. |

Rank 3 (dispatcher) moves DOWN from my audit's #1 because the empirical data shows a single-script (A_03) dominates far more than inter-script serialization does. Fixing A_03 first has a larger absolute wall-time impact than any dispatcher rework.

---

## 6. Unknowns — What This Run Cannot Tell Us

Chain halted at B_01. We have **zero empirical data** on:

- B_02 canonical_lots wall/CPU
- B_03 account_gains wall/CPU (audit said "already optimal 60-worker ProcessPool")
- All C scripts (C_00 through C_08)
- All D scripts (all of Group D)

Specifically cannot yet answer:
- **H2 (C critical path):** Did C_00 Polars port deliver the expected 5-10x? Does C_02 dominate the C-group as the audit predicted? No data yet.
- **H3 (D parallelizable):** Do D_00/D_00b/D_00c/D_01/D_02/D_03/D_04 have meaningful inter-dependencies that block the DAG parallelization gain? ~C's DAG validation says no. Empirical: not yet tested.
- **H4 (S3 writes):** Instrumentation doesn't yet report s3_reads/s3_writes. Cannot test.
- **B_03 reality:** Audit claimed B_03 should hit 95% CPU. No measurement.

**Next data point:** PROD full-chain at 04:00 UTC. When `perf_report.json` updates with B_02+B_03+C+D rows, this document gets a **Section 2 APPEND** covering H2/H3 and a revised empirical ranking.

---

## Meta-critique of the audit process

One sentence: the 5f8d5c88 audit over-trusted code reading as a proxy for empirical behavior. Where the code wore a `ProcessPoolExecutor` label (B_00), the audit concluded the problem was solved; where the code had a `.apply()` on millions of rows (B_01 normalize, not audited), it was invisible. Static code review **under-weighted what actually dominates wall time** — stale-data halts, sparse CPU utilization in "parallelized" scripts, and one specific script (A_03) out of scope. Future audits should pair static reading with at least one empirical run before ranking is final.

---

*Section 2 APPEND reserved for post-04:00 UTC PROD perf_report.json data. Ranking table will be revised once C/D numbers land.*

*Delivered by 0.4.0_DS_ClientPlatform~B | 2026-04-17*
