# TO OPAL_ADVIPOINTERS.P2-FLOOR-49F — schedule FLOOR for the canonical 49F runner chain + silver-completeness event accelerator (TF) (push plan §3 row 2, AE half)

<task_order id="OPAL_ADVIPOINTERS.P2-FLOOR-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-19 build (TF draft today is fine — read-only prep per your 152834Z order; NO APPLY before tonight's 23:01Z bd platinum fixture passes). Unattended cycles 08-20/21/22 are the proof bar.</dated>
<status>staged -- GO paired; prep now, apply after the fixture + CTO per-apply gate</status>
<priority>P1 — the canonical chain's only trigger today is a session act; NEVER#4: a production pipeline MUST have a schedule</priority>
<authority>Push plan @a2f27c8d0a §3 row 2 + CTO HOST RULING (verbatim in-row: the runner executes under the S3-code standard as its OWN scheduled stage — NOT appended to the legacy chain's stage list; revisable on your read only with new evidence). Ratified P2 spec: org/tier1_exec/4.0.0_SA_CRO/deliverables/P2_UNIFIED_MORNING_SCHEDULE_TIMING_MAP_SPEC_20260811.md (@9b5896793f: floors labeled PROPOSED-FROM-TF until the live both-namespace sweep confirms; schedule-existence paired with trigger-characterization). 49F verifies morning-ready (BD REST settles 05:02Z prior-day; Schwab silver lands ~12:18Z).</authority>
</task_order>

## Objective
Stand up the production trigger for the canonical 49F runner chain: an EventBridge SCHEDULE FLOOR
(fires daily after the ~12:18Z Schwab silver landing) plus the silver-completeness EVENT as an
ACCELERATOR — event-driven as accelerator only, never the sole trigger (NEVER#4). The invocation
target is DS~A's entrypoint per their P2D-4 contract (S3-code standard; own scheduled stage).

## Compiler tools (three-phase)
Phase 1: `comp-blast` on the mdpf-pipeline scheduled-floor TF precedent + `comp-iam gaps` after any
iam.tf change (necessary NOT sufficient — new resource ARNs verified on the live primitive,
`simulate-principal-policy` ONE --resource-arns per call, positive control as a SEPARATE invocation).
Phase 2: commit before apply (Deployment Rule 2). Phase 3: plan 0-diff after apply + tag
(`git tag -a` + push --follow-tags); `comp-freshness` row NOT added (moratorium — no monitors).

## Cross-domain coordination
- shared_resource: DS~A's entrypoint S3 code key — also_in_to OPAL_ADVIPOINTERS.P2-DISPATCH-49F. DS~A
  is last_write_owner on the script; you on the TF. Do not apply until P2D-4's written contract is in
  hand; MCP DS~A the schedule expression before apply.
- shared_resource: `opal-data-assets/portal/gold/advi/49financial/**` — written by the scheduled
  chain; read by DS~B (P4-EMIT) + CVO (pins). No writes from TF itself.

## Acceptance criteria
- P2F-1 PLAN EXPECTED-ROWS-BOUNDED: the TF plan's expected rows enumerated IN WRITING before apply
  (draft to COO+CTO for the pre-apply read — your 152834Z posture, kept); apply via `safe-apply` only;
  CTO per-apply gate honored.
- P2F-2 0-DIFF + TAG: post-apply plan 0-diff; tag pushed --follow-tags.
- P2F-3 FLOOR + ACCELERATOR: the schedule floor exists with a concrete ScheduleExpression (never
  event-only — print the expression); the silver-completeness event is wired as accelerator; both
  target DS~A's entrypoint under the S3-code standard as its OWN stage (host ruling; any contrary
  finding goes to CTO as new evidence, not silently implemented).
- P2F-4 THREE UNATTENDED WRITES: 08-20, 08-21, 08-22 each produce
  `portal/gold/advi/49financial/*/date={T-1}` written by the SCHEDULED run (TO-2 precedent bar) —
  evidence per day: the run's own log + S3 listing with LastModified in the scheduled window; T-1 per
  the trading calendar, never wall-clock.
- P2F-5 NO SESSION-LOCAL INPUT: the fired path resolves everything from S3 (attested from the run log
  of cycle 1; an expected log's ABSENCE is a finding, not a pass).
- P2F-6 proof instance VALID rc=0 positional: ids P2F-1,P2F-2,P2F-3,P2F-4,P2F-5,P2F-6.

<proof_of_spec>
  <expected_criteria>P2F-1,P2F-2,P2F-3,P2F-4,P2F-5,P2F-6</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/OPAL_ADVIPOINTERS.P2-FLOOR-49F_PROOF_OF_SPEC.json</instance_path>
</proof_of_spec>

## Do not
- No bare `terraform apply` (safe-apply), no bare commits (safe-commit), no
  `aws lambda update-function-code` (Terraform only).
- No alarms / SNS / SES / freshness checkers / monitors (moratorium, Andrew 07-28 standing).
- No applies before the 23:01Z fixture verdict; if PHASE_B1 fails tonight, the fixture outcome routes
  first — do not interleave.

## Reporting
COO (cc CTO, DS~A, MSTR) at plan-drafted, at applied, and after each unattended cycle (one line each).
Surprise channel: one banked line to COO. Session log with Compiler Tools section = deliverable.
