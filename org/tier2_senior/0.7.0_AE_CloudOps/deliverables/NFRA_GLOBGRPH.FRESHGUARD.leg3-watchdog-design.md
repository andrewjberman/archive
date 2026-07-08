# FRESHGUARD leg-3: derive-non-delivery WATCHDOG -- design for CTO arch-gate

**Author:** 0.7.0_AE_CloudOps · **Date:** 2026-07-08 · **Status:** DESIGN (staged for CTO arch-gate; NOT applied)
**TO:** NFRA_GLOBGRPH.FRESHGUARD (CTO GOV-A I1 ruling) · **Incident:** derive silent fail-closed ~a day (07-07 -> 07-08), edge-staleness

## Problem (recap)
`derive_runner` is the SOLE writer of `graph_edges`. It failed CLOSED for ~a day (NODE_TYPE_LAYER_GAP) with NO alarm -- the marker HEAD kept advancing on cse/incremental (node/cse) writers, so the graph read "fresh" while edges froze. Silent. leg-3 converts this class to LOUD.

## Design (reuse-first, mirrors the live `inf-gold-runner-overrun` CW-alarm pattern; NO new Lambda, NO new topic)

**Signal:** `derive_runner.py` prints `OK: DERIVE_RUNNER_COMPLETE ...` (L1797) ONLY on a successful commit-and-finish. A fail-closed / crash / non-launch emits NO such line. So "count of DERIVE_RUNNER_COMPLETE" is a true delivery signal.

**Mechanism (pure Terraform, in `infra/aws/terraform/globgrph/`):**
1. `aws_cloudwatch_log_metric_filter` on log-group `/ecs/globgrph/derive-runner`, pattern `"DERIVE_RUNNER_COMPLETE"` -> metric `Opal/Globgrph::DeriveRunnerCompletions` (value=1, default 0).
2. `aws_cloudwatch_metric_alarm`:
   - `metric` sum over `period=86400` (24h), `evaluation_periods=1`
   - `threshold=1`, `comparison=LessThanThreshold`  (i.e. <1 completion in 24h -> ALARM)
   - `treat_missing_data="breaching"`  (NO data = the failure mode = ALARM -- inverted vs the gold-runner overrun alarm, by design)
   - `alarm_actions=[opal-critical-surface-alerts]` + `ok_actions=[same]`  (REUSE, no sprawl)
   - `alarm_description` carries the rich context: expected daily derive ~02:00-03:30Z; `graph_edges` sole-writer=derive_runner; if firing, no successful derive in 24h -> edges freezing -> check the derive ECS task + the NODE_TYPE_LAYER fail-closed class + snapshots/<date>/.

**Deadline note (the one design trade for your call):** CW alarms are rolling-window, not clock-aligned. A 24h sum window catches non-delivery ~24h after the last completion (~03:30Z next day = ~1.5h past the 02:00Z cron, close to your ~04:00Z target). It CANNOT emit the dynamic `{expected_date, latest_actual, staleness_hours}` payload -- a CW alarm's SNS message is the fixed alarm-state + the (static) description. 
- OPTION A (this design): pure-TF CW alarm. Loud, robust, zero new compute, reuses the topic. Payload = static description (says "sole_writer=derive_runner", names the failure class). Meets the CORE bar (silent->loud) but not the dynamic payload.
- OPTION B: a small EventBridge(~04:15Z)->Lambda that reads snapshots/<today>/ + the marker graph_edges vintage and SNS-publishes the exact `{expected_date, latest_actual, staleness_hours}`. Meets the full payload + precise deadline, at the cost of a new Lambda+schedule+IAM.
Recommend A for speed/robustness + fold the rich payload into leg-4 (per-table vintage) if you want it; your arch-call.

## I3 exercise (exists != fires) -- CVO exercise-verifies
- **RED (the real incident IS the fixture):** over 07-07 03:38Z -> 07-08 03:22Z the log-group had ZERO `DERIVE_RUNNER_COMPLETE` (a genuine ~24h non-delivery). The alarm math (sum<1/24h, breaching) = ALARM across that whole window. Demonstrable by a log query over the incident window (0 hits). This is a real non-delivery the alarm MUST catch -- satisfies I3 with the actual event, not a synthetic.
- **GREEN:** tonight's fixed derive emitted `DERIVE_RUNNER_COMPLETE` @ 03:22Z -> metric=1 in the current window -> alarm OK. Demonstrable now.
- Post-apply: I confirm the alarm's live state = OK (green now), and provide the red-window log-query evidence; CVO exercise-verifies the red-test.

## Blast radius / rollback
Additive (1 metric filter + 1 alarm, reusing an existing topic). No change to the derive or any writer. Rollback = destroy the 2 resources. Zero data-plane impact.

## Ask
Arch-gate GO on Option A (or steer to B). On GO: land the TF (coordinated) -> safe-apply -> confirm alarm OK (green) + supply the red-window evidence -> RAVC you + CVO for the exercise-verify.
