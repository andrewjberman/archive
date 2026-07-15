# OPAL_STNDRD phase 3 -- absence-twin rollout design (for CTO plan-shape ruling)

**From:** 0.7.0_AE_CloudOps~Z | **Date:** 2026-07-15 ~20:2xZ | **Status:** DESIGN -- no TF authored,
nothing applied; plan-shape RAVC precedes any diff per the Z1 gates.
**Scope:** the ratified 4-unit list (brief B(iii) / TO phase 3): ingest-mirror x2 (inf, cot),
bd49f-daily-pull, schwab-si2 x2 masters, etfs-netassets. Grounding: trigger-map.json @ ab6d37ba2
(154-trigger census; 149 run-triggers have no twin -- the other ~145 stay a findings list).

## 1. The exemplar (prior art, live)

`astn-wsjft-4am-absence-check` + `etfs-reports-monthly-absence-check` (both Scheduler): a twin
schedule fires ~1h after the run and invokes THE SAME lambda with `input={mode: absence_check}`;
the lambda re-checks its own expected artifact exists and SNS-alarms on absence. The check is
ARTIFACT-BASED (did the thing land), never producer self-report -- that property must survive
generalization.

## 2. The fork the 4-unit list forces

Per-unit `absence_check` mode (exemplar shape) requires every target to be a lambda we can add a
mode to. The list breaks that: **canonical-schwab-si2 x2 are EventBridge->SSM RunPowerShellScript
targets on an EC2 box** -- there is no lambda to carry a mode. And the ingest-mirror lambda is
OPAL_ASSETS core (inf side = 0.4.0_DS~B active surface; code motions there are exactly what the
scope pin defers).

## 3. Options

**A (RECOMMENDED): one generic absence-check lambda + per-unit Scheduler twins.**
A single new small lambda (`opal-assets-absence-check`): input = `{unit, bucket, prefix_template,
alarm_topic}`; resolves today's expected S3 landing (trading-day-aware via lib/trading_calendar
semantics -- a T-1 unit's twin checks the T-1 key; NEVER#1 stays structural), ListObjectsV2 on the
expected prefix, SNS to opal-critical-surface-alerts on absence. Per unit: one
`aws_scheduler_schedule` `{unit}-absence-check-daily` (ratified grammar; Scheduler per ratified
B(i) -- new cron-class rides Scheduler) firing 60-90min after the unit's run, carrying that unit's
input. Properties: zero code motions on existing units (scope-pin-clean for ~B; parity-path-clean
for tonight's ETF legs); covers EC2/SSM-target units identically (the check reads the ARTIFACT,
which every unit has); one lambda to own, N config rows; each twin is a pure-to-add TF resource.
Cost: a new lambda + role (s3:ListBucket scoped to the checked prefixes + sns:Publish scoped to
the topic) -- new-territory, pure to-add.

**B: exemplar-faithful per-unit modes.** Adds `absence_check` mode to each target lambda.
Fails on schwab-si2 (no lambda), touches ~B's surface (ingest-mirror code), touches tonight's
parity path (etfs-netassets code). Not recommended for this list; stays the right shape for
future self-contained orchestrator units.

## 4. Placement + sequencing (under A)

- New TF: a dedicated module (proposal: `infra/aws/terraform/opal-assets-absence/`) so the twins
  do not entangle with the pending UNDECLARED-family import wave (the 13 CLI-built triggers routed
  to CTO in the phase-2 RAVC). If CTO prefers the import wave to land first and carry the twins in
  one module, phase 3 sequences behind it -- CTO's routing call.
- Lambda source under `infra/aws/lambda/opal-assets-absence-check/` + lambda-source-map entry
  (Rule 4) + trigger-map rows land in the SAME commit (registry moves with the estate).
- Expected-prefix per unit (from the census + monolith grammar):
  ingest-mirror-inf -> `orion/inflection/bronze/` + `eclipse/inflection/bronze/` (T-1 basis);
  ingest-mirror-cot -> `blackdiamond/cottonwood/bronze/`; bd49f -> `blackdiamond/49f/bronze/`
  (T-1); schwab-si2 -> `schwab/{master}/bronze/` (T-1, per master); etfs-netassets ->
  `trueshares/{DIVZ,IDVZ}/bronze/` + `pathfinder/filepoint/bronze/` (post-C4; confirm vs 0.5.0's
  owner-claim answer).
- Sequencing gates honored: NOTHING before tonight 22:00Z clears; ingest-mirror-inf twin
  MCP-0.4.0_DS~B-first (even though A avoids their code, the twin ALARMS on their surface --
  they should know the instrument exists before it can page anyone); every apply at CTO's
  safe-apply gate after plan-shape RAVC (expected shape: pure to-add, 0 change / 0 destroy).

## 5. What phase 3 does NOT do

No renames (natural touches only -- phase 4 standing rule). No twin rollout beyond the 4-unit
list (the remaining ~145 no-twin rows are census findings, prioritized separately). No touching
the two DISABLED-by-design classes surfaced in the census (17 DISABLED rows include deliberate
parks; absence twins guard ENABLED daily producers only).
