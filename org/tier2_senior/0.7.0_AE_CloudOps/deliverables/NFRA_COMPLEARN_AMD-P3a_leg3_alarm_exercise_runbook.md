# AMD-P3a leg-3 B3 — freshness-gate EXERCISE runbook (AC-L3a "exercised by going stale + observing the alarm")

**Author:** `0.7.0_AE_CloudOps~B` · 2026-07-10 · **GATED:** do NOT run until CTO~A green-lights + the Andrew-awareness on the SMS page is handled (see Blast Radius). Option-independent (the alarm exists under both design options).

## BANKED LESSON (2026-07-10, incident-derived, CTO~A-ratified) -- NEW-ALARM CREATION-PAGE RACE

Creating the telemetry alarm in the B2 apply fired a STRAY ~2-min ALARM->OK on a brand-new alarm
(2 SMS to the sovereign's phone, 2 SQS to COO), self-recovered. Root cause: a new CloudWatch metric
alarm with `treat_missing_data=breaching` evaluates missing-data -> ALARM within ~1-2 min of creation,
while a PutMetricData datapoint takes ~1-2 min to become alarm-visible. So **seeding AFTER the alarm
is created (with actions enabled) is structurally racy -- the alarm fires empty before the seed lands.**

**CORRECT PATTERN for any new breaching alarm on a paging path (NEVER seed-after-create-with-actions-enabled):**
1. CREATE the alarm with `actions_enabled=false` (or `treat_missing_data=missing`).
2. `PutMetricData` a fresh seed datapoint (or invoke the producer).
3. CONFIRM the datapoint is alarm-visible AND the alarm reads OK (poll `describe-alarms`).
4. THEN enable actions / flip `treat_missing_data` to `breaching`.

This is a SHARED miss (the arch-gate ratified seed-after-create too). It is banked in
`memory/feedback_new_alarm_creation_page_race_seed_before_enable.md`. The exercise below is
unaffected (it drives an EXISTING alarm), but any FUTURE alarm-creation on a sovereign-paging path
follows the 4-step pattern above.

## What we are proving
Invariant #2 / AC-L3a: the freshness gate is not merely *configured* but *fires*. The alarm `opal-globgrph-tool-activity-stale` has been OK since 2026-07-06 and has **never** transitioned to ALARM. An alarm never shown to fire has not been shown to work ("census of survived failures"). This drives it OK→ALARM and back, capturing the transition + the SNS delivery as evidence.

## Blast radius (VERIFIED LIVE 2026-07-10)
Alarm `AlarmActions`/`OKActions` → SNS `arn:aws:sns:us-east-1:313476888478:opal-critical-surface-alerts`, whose live subscriptions are:
- **SMS → `+17862617679`** — the PRODUCTION critical-alert number (also on opal-infrastructure / ec2-long-running / find-insure-budget; docs: Andrew-sourced). **A real text WILL be sent on both the ALARM fire and the OK recovery.**
- **SQS → `opal-critical-surface-alerts-coo`** — COO's alert queue.

→ Firing the real alarm pages the sovereign's phone (twice: fire + recover). This is *the loud path working* — but it must be announced/authorized, not a surprise.

## Alarm timing (VERIFIED)
`Period=3600, EvaluationPeriods=1, DatapointsToAlarm=1(default), Statistic=Maximum, GreaterThanThreshold=30`. One datapoint >30 in the trailing 3600s → ALARM (CloudWatch re-evaluates ~1/min → transition in ~1-3 min). **Recovery caveat:** because statistic=Maximum over a 3600s window, a low datapoint does NOT immediately recover — the breaching datapoint stays in the trailing hour, so the alarm holds ALARM until it ages out (**up to ~60 min**) or the window's Maximum drops below 30. Plan the window as ~60-70 min occupied.

## Two exercise modes — CTO~A picks
- **MODE R (real-alarm, gold standard):** drive the REAL metric; proves the exact prod metric→alarm→SNS→SMS/SQS path end-to-end incl. the SMS to the sovereign. Pages `+17862617679` twice. Needs Andrew-awareness (his number).
- **MODE T (parallel test-alarm, page-sparing):** clone the alarm onto a TEST metric `Opal/ToolActivity ParquetAgeHours_EXERCISE` wired to a TEST SNS with only an SQS sub (no SMS); drive it stale; observe OK→ALARM→SNS(SQS). Proves the metric-driven-alarm-fires-SNS MECHANISM without paging; the real SMS hop is then evidenced by subscription inspection (already captured above). Tear down the test alarm+topic after.

**My recommendation:** MODE R, in a tight announced window, with CTO~A owning the Andrew heads-up (proving Andrew's own critical-surface SMS delivers is worth one coordinated text). Fall back to MODE T if the sovereign page is unwanted for a non-urgent leg.

---

## MODE R — exact commands (run only on GO)
```bash
export AWS_PAGER=""
A=opal-globgrph-tool-activity-stale
# 1. BASELINE — capture pre-state
aws cloudwatch describe-alarms --alarm-names $A \
  --query 'MetricAlarms[0].{State:StateValue,Reason:StateReason,Updated:StateUpdatedTimestamp}' --output json | tee /tmp/ax_baseline.json
# 2. DRIVE STALE — one breaching datapoint (31h > 30h threshold)
aws cloudwatch put-metric-data --namespace Opal/ToolActivity \
  --metric-data 'MetricName=ParquetAgeHours,Value=31,Unit=None'
# 3. OBSERVE the transition (poll ~1/min up to ~5 min; expect StateValue -> ALARM)
for i in $(seq 1 6); do sleep 60; \
  aws cloudwatch describe-alarms --alarm-names $A --query 'MetricAlarms[0].StateValue' --output text; done
# 4. EVIDENCE — the ALARM-state reason + history item (the transition record)
aws cloudwatch describe-alarms --alarm-names $A \
  --query 'MetricAlarms[0].{State:StateValue,Reason:StateReason,Updated:StateUpdatedTimestamp}' --output json | tee /tmp/ax_alarm.json
aws cloudwatch describe-alarm-history --alarm-name $A --history-item-type StateUpdate --max-items 3 \
  --query 'AlarmHistoryItems[].{ts:Timestamp,summary:HistorySummary}' --output json | tee /tmp/ax_history.json
# 5. SNS-delivery evidence — pull the ALARM message off COO's SQS (proves the topic delivered)
aws sqs receive-message --queue-url \
  $(aws sqs get-queue-url --queue-name opal-critical-surface-alerts-coo --query QueueUrl --output text) \
  --max-number-of-messages 5 --wait-time-seconds 10 --visibility-timeout 0 \
  --query 'Messages[].Body' --output json | tee /tmp/ax_sns_delivered.json
#    (+ confirm the SMS receipt out-of-band with Andrew — his number is the endpoint.)
# 6. RECOVER — let the breaching datapoint age out of the trailing 3600s window (~<=60 min) so the
#    next real hourly probe's Maximum (~7h) drops the alarm to OK, which fires the OK-action (recovery text).
#    Do NOT delete the metric or tamper with the real Lambda. Confirm return to OK:
aws cloudwatch describe-alarms --alarm-names $A --query 'MetricAlarms[0].StateValue' --output text
```
**Do NOT** modify the SNS subscriptions, the alarm config, or the real freshness Lambda during the exercise — the point is to prove the PRODUCTION wiring, not a modified one.

## Evidence bundle (attach to RAVC2)
`ax_baseline.json` (OK pre), `ax_alarm.json` (ALARM + reason citing the 31h datapoint), `ax_history.json` (the OK→ALARM StateUpdate at a timestamp inside the window), `ax_sns_delivered.json` (the alarm payload off COO's SQS), + Andrew's SMS-receipt confirmation, + the final OK. That set discriminates "fires" from "looks configured."
