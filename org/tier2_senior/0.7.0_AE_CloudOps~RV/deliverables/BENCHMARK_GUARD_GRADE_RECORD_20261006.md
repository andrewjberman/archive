# OPAL_BBGTML.TO-GUARD-1 -- the stale-benchmark guard, graded record

**Executor:** `0.7.0_AE_CloudOps~RV` (seat act) | **Date:** 2026-10-06 | **Risk class:** WORLD
**Order:** `OPAL_BBGTML.TO-GUARD-1.stale-benchmark-guard` @416573eac2
**Bound by:** COO half @1253afc83c + CTO half @78a9e8a39e, **ADDENDUM 1** @99f67b52e5
**Route:** track 1 of `CTO_RULING_INDEX_BENCHMARK_FIX_ROUTE_20261006.md` @5e0c045e8d
**Priority:** Andrew-direct, singular for site Z (@f42219ebfe)

**VERDICT: all three criteria PASS. Three legs landed; NEVER-2 entry closed.**

---

## What the guard does

`yang-model-portfolio-benchmarks` now reads, per model and per series, the last non-null bar at or
before `data_as_of` (`last_non_null_bar`). A series whose frontier is BEFORE `data_as_of` returns
`None` on every period -- return, volatility, and both spreads with it -- and the frontier is served
beside the nulls as `benchmark_last_date {index, etf}` on the comprehensive AND legacy keys.

**The defect it stops.** `compound_returns` `dropna()`s a missing tail. The four short periods
(1D/WTD/MTD/QTD) therefore fell to null -- the N/A the portal already showed -- while the six long
ones (1M/1Q/YTD/1Y/Since Inception/TTW) served a **wrong number, unmarked**: compounded only through
2026-09-29 against a model compounded through 2026-10-05. The guard refuses the SERIES, never a
period, so a window is never silently shortened. Model rows and the daily timeseries are untouched.

---

## AC1 -- the plant test, 3 of 3, before any deploy act

```
python -m pytest infra/aws/lambda/v2_portal/yang_pipeline/portfolios/\
yang-model-portfolio-benchmarks/test_stale_benchmark_guard.py -q
-> 3 passed in 2.23s
```

The test drives the REAL `lambda_handler` over a synthetic data PKL with only the S3 boundary patched
(`load_pkl`, `upload_json`, the monotonic guard), so the model loop, both output builds and the
timeseries build are the deployed code paths. Its fixture mirrors the live asymmetry: 9 stale series
at 2026-09-29, Intermediate Term ETF current at 2026-10-05.

**Two-arm negative control** -- the test is graded on BEHAVIOUR, not on the additive field:

| arm | bytes under test | result | what it establishes |
|---|---|---|---|
| 1 | pre-patch HEAD | 3 failed, all `KeyError: 'benchmark_last_date'` | only that the FIELD is absent |
| 2 | `benchmark_last_date` PRESENT, the nulling REMOVED | failed on the guard: `UST 1D index_benchmark served nan`; `assert np.float64(2.95) is None` (INT YTD) | that a stale series serving 2.95 is caught |

Arm 1 alone would have been a check conjoining its own precondition with what it measures. Arm 2 is
the discriminator.

---

## AC2 -- the deploy moved the bytes

| object | before | after |
|---|---|---|
| `CodeSha256` | `dHTjheKzauUziiPc6Jkwn7Ys+C36Xb5KS0aAWPh7Th8=` | **`FLFjTpvIDptT+YqJGG9w3XaWN/Cwq4WJkNlmPd4p0tg=`** |
| `LastModified` | 2026-08-04T19:44:48Z | 2026-10-06T16:14:11Z |
| `s3_object_version` | `Pzl.iT8IkhL0_Ob8sE6NQBzZ43BUyw5K` | `g0NaQztkPzEyQXXiV2a4utvW1Er0V5dS` |
| runtime / memory | python3.12 / 512 MB | unchanged |

The live hash **differs from the base AND equals the artifact built from code-leg commit
`513b25f522`** -- not an unchanged-hash 0-diff deploy. The artifact was verified by CONTENT, never by
filename: packaged bytes 37,573 identical to the committed source, `def last_non_null_bar` present, a
`ZZZ_NOT_PRESENT` negative control reading 0, and the test file NOT shipped.

**ADDENDUM 1 route (a), under its four conditions:**

1. **The plan moves exactly those 2 resources and attributes** -- re-planned and graded by
   `terraform show -json` on address (69 `resource_changes`, 2 not no-op):
   `module.model_portfolio_benchmarks.aws_lambda_function.this` -> exactly
   `{source_code_hash, s3_object_version, last_modified}`; `aws_sfn_state_machine.yang_pipeline` ->
   exactly `{definition}`. Both MATCH. The human-readable plan tail showed only one of the two, which
   is why the JSON is the instrument.
2. **`describe-state-machine` saved before the apply** -- 35,730 chars, 1,012 CR, status ACTIVE.
3. **After the apply the definition reads 0 CR and its parsed JSON equals the saved one** -- 34,718
   chars, **0 CR**; a per-leaf walk compared **481 leaf values and found 0 differing**; `roleArn`
   unchanged; status still ACTIVE.
4. **No third resource.**

`safe-apply`: `comp-tagauthz` PASSED, `tombstone-gate` CLEAN, `Apply complete! Resources: 0 added, 2
changed, 0 destroyed`. The 0-diff re-plan returns exitcode 0, `No changes. Your infrastructure
matches the configuration.`

---

## AC3 -- the served output, graded at the cell

CTO section 4 condition 3 was re-read **immediately before** the invoke: served `data_as_of`
2026-10-05 equals the base, so **BRANCH A**. Leg 3 was ONE invoke on `benchmarks/data_20261005_v1.pkl`
(the key `LATEST.json` names), payload 159 bytes, **no `force_publish`**. StatusCode 200, no
`FunctionError`; `model_count` 5, `timeseries_row_count` 3175, all three keys written at
2026-10-06T16:16:52Z.

Staleness is **classified from the served artifact's own `benchmark_last_date`**, so the 9-stale /
1-current split is an output of the grade, not an assumption inside it. The grader refuses to grade
when that field is absent -- and did exactly that when run before the deploy.

### The comprehensive key -- 300 benchmark-derived cells (5 models x 10 periods x 6 fields)

| bucket at the base | cells | after | expected by CTO section 3 |
|---|---|---|---|
| stale-sourced, serving a number (**the silent half**) | 171 | **null** | null |
| stale-sourced, serving null (the visible N/A) | 99 | null | null |
| current-sourced (INT `etf_*`), serving a number | 27 | **byte-equal to the base** | byte-equal |
| current-sourced, null (`min_points=5`) | 3 | null, unchanged | unchanged |
| **DENOMINATOR** | **300** | **273 null / 27 numbers** | 273 / 27 |

`benchmark_last_date`: index **2026-09-29** on all 5 models; etf **2026-09-29** on UST, ST, LT, ULT
and **2026-10-05** on INT.

**Model cells (`model` + `model_volatility`): 100 of 100 equal to the base, denominator 100.**

### The legacy key

| partition | count |
|---|---|
| number -> null | 95 |
| null unchanged | 55 |
| number unchanged | 0 |
| **number CHANGED** | **0** (a changed number anywhere means rollback) |
| **DENOMINATOR** | **150** |

Model cells 100 of 100 equal. `benchmark_last_date` present on every legacy model.

**One clause named rather than silently passed:** the legacy format carries ONE benchmark field,
sourced from the INDEX series only. It has no ETF-sourced value, so the CTO half's "INT's ETF-sourced
values are byte-equal" clause is **VACUOUS** on this key. All 150 legacy benchmark cells are
index-sourced and all 5 index series are stale, which is why 0 numbers remain.

### The timeseries key

Rows **byte-identical** -- 3,175 rows and 768,530 B on both sides; only `generated_at` differs
(12:31:20Z -> 16:16:50Z). The guard did not reach `build_timeseries`.

### CTO section 2's named watch -- the dormant smartx exporter

13 legacy versions retained, **0 unpaired** with a comprehensive version inside 60 s. No
dormant-exporter write occurred, so nothing was misread as this act's failure.

---

## What a reader of the portal will see, and why it is not an outage

**171 cells turn from a number into N/A in the Benchmark Comparison panel.** That is the intended
outcome of this act: those numbers were wrong, compounded through 2026-09-29 against a model through
2026-10-05. The panel already rendered 99 nulls as N/A, which was the live positive control that a
null renders. Anyone reading the panel without the ruling will read this as a new outage. It is not.

When the CIX source reaches `data_as_of` (track 2, Yang's re-save and re-pull), the guard serves
numbers again **with no code change**, each carrying `benchmark_last_date == data_as_of`. That is
track 3's proof, not this act's.

---

## Commits, and the surprise row

| commit | what |
|---|---|
| `513b25f522` | code leg -- ONLY `lambda_function.py` + `test_stale_benchmark_guard.py`, 305 insertions |
| `9ea9161ff4` | the HELD state: row Z-S6, NEVER-2 entry + sentinel, the AC3 grader, source-map sha |

**Row `OPAL_BBGTML-Z-S6`** (BLOCKING / ARMED, `disarm_owner` `1.0.0_SA_CTO~Z`) recorded that the
untargeted plan moved a second resource. It is **DISARMED by ADDENDUM 1** @99f67b52e5, whose route (a)
this record executes. The row stands as filed; the addendum is its disposition.

**One blemish stated plainly:** ledger leg G3 carries the token `CLOSED` from the HELD phase, because
`close-leg` is the only way to attach proof and the ledger (correctly) refuses a HELD state for an
unfinished deploy. Its proof text leads with "HELD, NOT APPLIED". G4 carries the real activation
proof, including the full ADDENDUM 1 condition set.

**Push state, measured at `git ls-remote`:** LOCAL. The CLOUD push is `0.0.0_AB_MSTR~Z`'s on Andrew's
word.
