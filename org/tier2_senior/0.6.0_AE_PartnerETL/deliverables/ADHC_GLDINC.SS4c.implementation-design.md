# ADHC_GLDINC.SS4c — periodic-oracle re-validation: implementation design
**author:** 0.6.0_AE_PartnerETL · **2026-06-17** · built to CVO cvo_1330Z + PRD §4c (PRD:247-282)
**status:** DESIGN — pending CloudOps cost-footprint sign-off (binding pre-deploy) + CVO re-cert at build

## Phase-1 grounding (compiler mandate — done; avoids the windowed-vs-windowed tautology)
- **Oracle (independent, preserved for exactly this job):** `nna_flows.load_flows_from_transactions_full_scan()`
  (nna_flows.py:141) — reads EVERY `silver/transactions/*.parquet` via `_transform_events_to_daily`, NO
  cache/watermark. The TO's "point at the preserved full_scan, not the delegating name" = THIS (not
  `load_flows_from_transactions()` :92, which delegates to windowed = the tautology to avoid).
- **Served incremental path:** `load_flows_from_transactions()` -> windowed + `write_load_flows_state()`.
- **Cache/state (daily-canary target):** `S3_LF_CACHE_KEY = gold/_state/load_flows/preflt_events.parquet`
  (+ `watermark.json`), bucket opal-data-bd.
- **Scorecard (weekly diff):** `gldinc_p1_shadow.compute_scorecard(inc, ora)` (:105) — emits §4b
  key_set_symmetric_diff / row_count_delta / exact_match_rate / within_epsilon_rate / max_abs_diff /
  headline_metric_diffs / is_clean (gate vs FROZEN_EPSILON_USD). REUSE verbatim.
- **Dtype-trap canary already prototyped:** `test_gldinc_cache_roundtrip.py` asserts transaction_id int/str
  TYPE-EXACT (int 999 vs str '999' kept DISTINCT — the over-dedup trap) + trade_date datetime. The daily
  canary lifts these assertions onto the LIVE cache parquet.

## Two-tier mechanism (PRD §4c)
### TIER 1 — DAILY structural canary (cheap, NO full_scan) -> Lambda
- Trigger: EventBridge daily (~after the nightly chain completes; staggered off the chain-complete event).
- Reads ONLY `gold/_state/load_flows/preflt_events.parquet` (one parquet, ~MB) + `watermark.json`.
- Asserts (lift from test_gldinc_cache_roundtrip): transaction_id preserves int/str (no flat-str over-dedup
  collision loss); trade_date is datetime64; LF_RAW_COLS present; watermark advanced since prior run
  (cache not frozen). Emits CW metric `GLDINC/SS4c CanaryStructuralOK` (1/0) + cache_row_count +
  dtype_fingerprint. Cost ~ trivial (sub-second Lambda); independent of the c6i runner.
- Closes the <=7-day weekly blind window (catches a dtype-drift the DAY a drift-partition enters).

### TIER 2 — WEEKLY full value-diff (heavy) -> piggyback the c6i gold runner
- Runs 1x/week (+ on reconcile-triggers: injection-date / period-rebaseline / reassignment) APPENDED to the
  scheduled nightly on the c6i runner — NOT a manufactured run (NFRA_COSTAWS / compute-discipline; the c6i
  is 34% of the bill). The runner is already up for the nightly; this adds the full_scan oracle compute.
- Runs `load_flows_from_transactions_full_scan()` (oracle) vs the SERVED incremental `daily`; computes
  `compute_scorecard`. Emits CW metrics `WeeklyMaxAbsDiff` / `KeySetSymmetricDiff` / `RowCountDelta` /
  `ExactMatchRate`. DELTA=0 expected on the clean cutover (byte-identical-by-construction).

## Alarms (egress-verified, 4) -> SNS `gldinc-ss4c-alerts` (real subscriber)
1. CanaryStructuralBreak — CanaryStructuralOK < 1.
2. CanaryAbsence — no CanaryStructuralOK datapoint in >26h (missing = breach).
3. WeeklyDivergence — WeeklyMaxAbsDiff > FROZEN_EPSILON_USD OR KeySetSymmetricDiff > 0 OR RowCountDelta != 0.
4. WeeklyAbsence — no Weekly* datapoint in >8d (missing = breach).
All on SNS with a verified subscriber (the absence alarms are the anti-"globgrph 0-sub-topic" coverage).

## Watch-the-watcher (unknown-unknown #2)
Register the 4 alarms + SNS-subscriber-PRESENCE into the critical-surface registry
(`org/modules/graph/critical-surfaces.yaml`) so a later subscriber-removal RE-FLAGS via comp-surface-check.
Authored through 0.7.0_AE_CloudOps owner-review (LD-0193 cross-tool — base-AE is reworking that registry in
NFRA_GRAPHS.D8-FP).

## Cost-model (unknown-unknown #3) — CloudOps co-owns, BINDING before deploy
Add the standing verifier to NFRA_COSTAWS §7 as a PERMANENT recurring line. Daily canary ~ negligible
(Lambda). Weekly full_scan = the cost lever (full silver/transactions scan, 1x/week on the c6i). STAGGER
the per-phase weekly oracles (P1..P5) across different weekdays so the heavy diffs never collide/spike.
**CloudOps signs the runner-compute footprint before the Terraform schedule applies.**

## Terraform (deploy — after CloudOps sign-off + CVO re-cert)
infra/aws/terraform/: canary Lambda + role (s3:GetObject on gold/_state/load_flows/* + cloudwatch:PutMetricData)
+ 2 EventBridge schedules (daily canary / weekly diff-on-runner) + 4 CW alarms + SNS topic + subscription.
comp-iam gaps after iam.tf. Phase-3 verify: synthetic injected divergence FIRES WeeklyDivergence; a skipped
run FIRES the absence alarm (egress-verified, not success-only).

## Open decisions for CloudOps (cost consult — the binding gate)
1. Weekly diff piggyback mechanism: append a `--ss4c-weekly` leg to the nightly gold_dispatch chain on the
   runner (1 weekday/run-night), vs a separate runner-start (rejected — manufactured run). Recommend append.
2. Which weekday for P1's weekly slot (stagger anchor for P2-P5).
3. Cost line magnitude for NFRA_COSTAWS §7 (full_scan added compute, 1x/week).
