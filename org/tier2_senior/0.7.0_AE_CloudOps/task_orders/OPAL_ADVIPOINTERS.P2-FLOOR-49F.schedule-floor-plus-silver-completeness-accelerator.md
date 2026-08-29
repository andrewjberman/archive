# TO OPAL_ADVIPOINTERS.P2-FLOOR-49F — schedule FLOOR for the canonical 49F runner chain + silver-completeness event accelerator (TF) (push plan §3 row 2, AE half)

<task_order id="OPAL_ADVIPOINTERS.P2-FLOOR-49F" project="OPAL_ADVIPOINTERS">
<issued_to>0.7.0_AE_CloudOps</issued_to>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-18T16:05Z</issued>
<dated>2026-08-19 build (TF draft today is fine — read-only prep per your 152834Z order; NO APPLY before tonight's 23:01Z bd platinum fixture passes). Unattended cycles 08-20/21/22 are the proof bar.</dated>
<status>pending -- GO 160648Z @49dd8469d1. ISSUER RE-SCOPE 2026-08-29T16:4xZ on 0.7.0_AE_CloudOps 83241, which measured the LIVE plane and found the apply this TO was waiting to make ALREADY DONE. P2F-3 SPLIT by the issuer (a criterion whose halves have different remedies was never one criterion): P2F-3a FLOOR = DISCHARGED -- advi-49f-gold-floor ENABLED since 2026-08-19T17:32:28Z, cron(45 12 * * ? *) UTC, target advi-49f-gold-dispatch (DS~A entrypoint), never modified since; corroborated to the SECOND by the P2-DISPATCH-49F close note already on record. P2F-3b ACCELERATOR = OPEN, not started -- list-rule-names-by-target returns [] and the function policy carries exactly ONE statement (scheduler principal), so no event source is PERMITTED to invoke it. P2F-4 = 2 of 3 and NOT relaxed: 08-21 and 08-22 PASS; 08-20 FIRED then REFUSED. The 08-20 refusal is a FINDING, not a miss -- the chain requested date=<wall-clock run date> where P2F-4 says T-1 per the trading calendar, NEVER wall-clock. Same defect shape as gold_dispatch.sh RUN_DATE. NOT ASSERTED as proven: the discriminating read is the date resolution inside advi-49f-gold-dispatch, which 83241 correctly declined to infer from three log lines and which is DS-class, not AE. RE-RUNNING three more days would re-measure the defect rather than discharge the criterion. AE owes P2F-3b only; the date read needs its own owner (COO allocation, not a re-open of the COMPLETE P2-DISPATCH-49F). Prep authorisation from COO 82885(a) stands and nothing here is an apply.</status>
<priority>P1 — the canonical chain's only trigger today is a session act; NEVER#4: a production pipeline MUST have a schedule</priority>
<authority>Push plan @a2f27c8d0a §3 row 2 + CTO HOST RULING (verbatim in-row: the runner executes under the S3-code standard as its OWN scheduled stage — NOT appended to the legacy chain's stage list; revisable on your read only with new evidence). Ratified P2 spec: org/tier1_exec/4.0.0_SA_CRO/deliverables/P2_UNIFIED_MORNING_SCHEDULE_TIMING_MAP_SPEC_20260811.md (@9b5896793f: floors labeled PROPOSED-FROM-TF until the live both-namespace sweep confirms; schedule-existence paired with trigger-characterization). 49F verifies morning-ready (BD REST settles 05:02Z prior-day; Schwab silver lands ~12:18Z).</authority>
</task_order>
> **ROOT SUPERSEDED BY REFERENCE (COO, 2026-08-18 ~17:42Z): Andrew-direct ~1730Z moved the ADVI gold home to `opal-data-49financial/gold/advi/` (per-client bucket; ANDREW_DIRECT_20260818_CLIENT_GOLD_BUCKET_SUPERSESSION.md). Every `opal-data-assets/portal/gold/advi/49financial` root reference in this TO reads through OPAL_ADVIPOINTERS.GOLDHOME-REPOINT-49F (one act, before the P2 apply). Key names, criteria ids, dates unchanged.**


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


## EXECUTING LANES ON THIS TO'S CELLS -- issuer record, 2026-08-29T18:0xZ (2.0.0_SA_COO)

⛔ **WRITTEN BECAUSE THE ALLOCATIONS BELOW WERE MADE BY MESSAGE AND APPEAR ON NO FACE ANYWHERE.**
`to-check --all --assignee 0.4.0_DS_ClientPlatform~V` returned ZERO rows while that lane was doing this
work -- **not misattributed, ABSENT.** A face-reading census cannot see a cell allocated to a lane other
than the TO's owner, because there is nowhere for it to be recorded. Surfaced by `1.0.0_SA_CTO` 83447 as
a property of its own instrument; this is the instance.

| cell | executing lane | allocated | state |
|---|---|---|---|
| **P2F-4 wall-clock date read** on `advi-49f-gold-dispatch` | `0.4.0_DS_ClientPlatform~V` | COO 83394 | READ-ONLY, first. **CONFIRM-OR-REFUTE, not confirm.** Do NOT fix if found. |
| **composite `_SILVER_COMPLETE.json` emit** (P2F-3b route (a)) | `0.4.0_DS_ClientPlatform~V` | COO 83406 | BUILD, sequenced AFTER the read. Marker carries a **DECLARED** table list, never one derived from a listing. |

**TO OWNER REMAINS `0.7.0_AE_CloudOps`** -- these are cells executed by a DS lane, not a re-address of the TO.
**Rule 27 holds: both cells are `OPAL_ADVIPOINTERS`, so `~V` remains a one-project instance.**
⛔ **P2F-3b's TF rows stay with `0.7.0_AE_CloudOps` and are NOT started until the marker emit lands.**
