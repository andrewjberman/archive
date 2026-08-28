# TO ADVI_INSURE.TO-A3-AE — the insurance leg becomes REACHABLE and SCHEDULED: handler event-dispatch + ONE Scheduler entry (LAPTOP)

<task_order id="ADVI_INSURE.TO-A3-AE" project="ADVI_INSURE">
⛔ <distribution>NOT TO 4.0.0_SA_CRO, at every relay (ADVI_INSURE PRD s.3).</distribution>
<decomp_ref>workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md — cell INS-a-5 (issuer amendment 2026-08-28)</decomp_ref>
<decomp_context>ONE cell. The deployed Lambda `opal-assets-bd49f-reporting-pull` (LastModified 2026-08-27T17:49:22Z, deploy ledger 20260827T1718Z CLOSED 7/7) carries `insurance_leg.py` as a vendored module and its configured entrypoint cannot reach it: `lambda_function.py` has 0 insurance references and `lambda_handler` (:307) reads `event["q_start"]`/`event["q_end"]` unconditionally; `insurance_leg.py` has no handler. Every insurance capture to date (08-25, 08-27) was a manual module invocation — QA evidence, never production (CLAUDE.md NEVER: production pipelines MUST be scheduled). No trigger exists on any plane: Scheduler 0 of 18 target the function, events rules 0, no invoke policy, 0 event-source mappings, and `infra/aws/terraform/opal-assets/bd49f_reporting_pull.tf` declares manual-invoke-only with "WS-5 owns the trigger" — that WS-5 is OPAL_TAXSMA_PT2's, for the REPORTING payload. Trigger owner RULED by 1.0.0_SA_CTO 78326 on 2.0.0_SA_COO 78310 (D2-D3 ledger row 12): D2 owns the INSURE trigger; TAXSMA WS-5 keeps the reporting payload's; one Lambda, two payloads, dispatch BY EVENT. TO-A1-AE stays COMPLETE as scoped (IAM + package): this is a NEW cell, not a reopen.</decomp_context>
<certification>PENDING 3.0.0_SA_CVO cert step-zero on the INS-a-5 amendment + this face (alternate: base 1.0.0_SA_CTO, never CRO). 3.0.0_SA_CVO base is NOT LIVE at cut time; the cut proceeds on the issuer's disclosure, the ACCEPTANCE waits on the cert. Round-bank class riding this TO (CTO 78326 item 4): an acceptance row that read a MEMBER LIST accepted presence where the criterion needed reachability from the configured entrypoint.</certification>
<issued_to>0.6.0_AE_PartnerETL</issued_to>
<executor_class>AE-class (partner ETL vehicle; Terraform + Lambda package owner for this producer).</executor_class>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-28T16:5xZ</issued>
<status>pending</status>
<priority>P1 -- INSURE's P2 vehicle cadence (docs/briefs/d2-critical-path-sequencing-20260827.md sec 4 :60); AC2/AC3 of TO-R1-DS (APPLIED-gated) read against the first scheduled fire; the D2 serve gate (P3) needs P2's QA emission.</priority>
<placement>LAPTOP (Rule 26).</placement>
<scope_guard>ONE cell, FOUR ordered acts (a)-(d) below, on ONE Lambda + ONE .tf. ⛔ The REPORTING payload (q_start/q_end path) is OPAL_TAXSMA_PT2's and stays UNCHANGED in behaviour: the dispatch is additive, the existing path is the `else`. ⛔ NO alarm / SNS / monitor / twin (INS-inv-5, standing moratorium) -- a Scheduler entry is a trigger, not an alarm. ⛔ /account-api/* stays carved out. ⛔ Never `aws lambda update-function-code`; Terraform + safe-apply only; a begun deploy FINISHES in-session or rolls back (NEVER#6, ledger via .tools/deploy_ledger.py open at deploy-start). ⛔ Vendor egress: the 49F reporting API per-use grant (Andrew 07-17, .tf:12-13) covers this producer and the schedule does not widen the surface it calls; if 0.6.0_AE_PartnerETL reads the insurance endpoints as OUTSIDE that grant's stated surface, STOP and surface it to 2.0.0_SA_COO as a RESERVED card -- never an inference either way. Adjacent findings: one line to 3.0.0_SA_CVO cc 2.0.0_SA_COO (queued while CVO is dark), keep working.</scope_guard>

## The four acts, in this order (CTO 78326 item 2, verbatim)

(a) `lambda_function.lambda_handler` gains an event dispatch -- `event.get("leg") == "insurance"` -> insurance_leg's run path (pull_date from the event or today UTC), else the existing reporting path unchanged; a missing/unknown leg with no q_start fails CLOSED with a named reason, never a KeyError;
(b) package rebuild via the existing BUILD_MANIFEST path, Terraform only (never update-function-code), safe-apply, Rule-20 graph query first, NEVER#6 ledger opened at deploy-start;
(c) ONE aws_scheduler_schedule in the .tf targeting the function with input {"leg":"insurance"}, daily, cadence 11:35Z (before the 12:45Z gold floor so the bronze lands ahead of the chain fire that will consume it; off the fleet marks; the campaign blackout is a runner-side rule and does not bind a Lambda pull);
(d) acceptance = ONE scheduled fire's own CloudWatch log showing the insurance branch ran AND the bronze key landed at the ruled 49financial/ grammar for that pull_date (head-object), with the reporting branch NOT run as the negative control; a manual invoke is QA evidence only.

Plus, from CTO 78326 item 1: the `.tf` comment ("NO schedule ... WS-5 owns the trigger") is amended IN THE SAME COMMIT as (c) to say exactly: reporting payload manual-invoke-only pending OPAL_TAXSMA_PT2 WS-5; insurance leg scheduled by ADVI_INSURE INS-a-5 via event dispatch -- so the two records agree on disk.

## Acceptance criteria

| id | criterion | layer |
|---|---|---|
| **INSA3AE-AC1** | (a) DISPATCH: `lambda_handler` routes `{"leg":"insurance"}` to the insurance leg's run path and leaves the reporting path byte-identical in behaviour; a bare/unknown event with no `q_start` fails CLOSED with a NAMED reason. Exercised locally on the packaged bytes with THREE arms: `{"leg":"insurance"}` -> insurance path entered (mocked HTTP, no live call); `{"q_start","q_end"}` -> reporting path entered, insurance NOT entered; `{}` -> named refusal, no KeyError. Arms differ on the field under test. | DESIRED -> BUILT |
| **INSA3AE-AC2** | (b) DEPLOYED BYTES: package rebuilt via BUILD_MANIFEST, Terraform plan saved and applied via `.tools/safe-apply.sh` (apply counts == plan counts), 0-diff re-plan; the deployed zip re-downloaded and the dispatch resolved via BUILD_MANIFEST (not filename) -- CodeSha256 changed from D89ozvtWzeQQwwow8iCg2pEyaqhZTtgFbbF/GaYJJPw=. Rule-20 graph query recorded BEFORE the change. NEVER#6 ledger opened at deploy-start and CLOSED with every leg proven. | APPLIED |
| **INSA3AE-AC3** | (c) TRIGGER: exactly ONE `aws_scheduler_schedule` targeting `opal-assets-bd49f-reporting-pull` with input `{"leg":"insurance"}`, `cron(35 11 * * ? *)` UTC, state ENABLED, read back from the LIVE primitive (`aws scheduler get-schedule`), both trigger planes re-censused client-side (Scheduler N of M; events rules for the function = 0 -- the reporting payload gains NO trigger here); the `.tf` comment amended in the same commit. | APPLIED |
| **INSA3AE-AC4** | (d) EXERCISED ON THE SCHEDULED PLANE: the FIRST scheduled fire's own CloudWatch log shows the insurance branch ran; `head-object` on the bronze key at `blackdiamond/49financial/bronze/insurance_*/{pull_date}/` for that fire's pull_date (LastModified within the fire's window, s3api UTC); the reporting branch NOT run in that fire (negative control, from the same log). A manual invoke before the fire is QA evidence and does NOT close this row. | EXERCISED |
| **INSA3AE-AC5** | Proof instance VALID rc=0 positional, ids INSA3AE-AC1..AC5, TRUE rc bare, validator invocation + rc recorded IN the instance (D2 lock-in); every arm's output quoted, not summarised. | — |

<compiler_tools_mandate>
BEFORE WRITE: `comp-blast` on infra/aws/terraform/opal-assets/bd49f_reporting_pull.tf + the Lambda dir (the shared-Lambda blast radius: OPAL_TAXSMA_PT2's reporting payload rides the same handler); Rule-20 dependency-graph query per org/modules/graph/graph-call-manifest.yaml (QUERY, never rebuild; provenance header read); `comp-iam service opal-assets-bd49f-reporting-pull` (no iam.tf change is expected -- if one becomes necessary, `comp-iam gaps` + `simulate-principal-policy` one --resource-arns per call with a SEPARATE positive control, and the seat STOPS to surface it, since IAM is not in this cell).
BEFORE COMMIT: `.tools/commit-gate.sh` on every .py touched (py_compile + ds-precommit + ruff py39); `terraform fmt -check` (never `-diff`, it WRITES); `terraform validate`; the AC1 three-arm exercise green with its RED arm shown.
AFTER COMMIT / DEPLOY: `comp-pipescript deployed` is NOT the instrument for a Lambda package -- verify by re-downloading the deployed zip and reading members via BUILD_MANIFEST; `aws scheduler get-schedule` on the live primitive; the first fire's CloudWatch log read from the fire itself.
</compiler_tools_mandate>

<cross_domain_coordination>
- OPAL_TAXSMA_PT2 (reporting payload, same Lambda, same handler): behaviour UNCHANGED; its WS-5 trigger design (PRD :73, sentinel->EventBridge) untouched and named in the .tf comment. No live TAXSMA seat; nothing to coordinate on the wire, everything to preserve in the code.
- 0.4.0_DS_ClientPlatform~R (ADVI_INSURE.TO-R1-DS): AC2/AC3 (APPLIED-gated) read against this TO's first scheduled fire; the 4-table silver extension of `data/assets/scripts/silver/bd49f_insurance_conversion.py` is DS~R's act (COO 16:32Z ruling); the silver STAGE in the 49F chain (production silver, the c0x pattern) is DS~R's design in this INSURE round, sequenced by 2.0.0_SA_COO AFTER INS-a-5's first scheduled fire (CTO 78326 item 3, ledger row 12 unblocks (3)).
- ADVI_49F P14-VEHICLE campaign (0.7.0_AE_CloudOps~L, running on the EC2 runner): disjoint substrate (Lambda vs runner); the 12:45Z blackout is a runner-side rule and does not bind this Lambda pull; the 11:35Z cadence lands the bronze before the floor fire.
- Shared S3 keys: writes ONLY under `opal-data-assets/blackdiamond/49financial/bronze/insurance_*` (the existing landing tree; firm-separation guard `.tools/ds-precommit-check.py` enumerations unchanged).
</cross_domain_coordination>

## Compiler tools
Mandate above is three-phase and binding; the deploy-side runs from TO-A1-AE's ledger (comp-iam gaps, manifest parity) are CITED for the unchanged IAM and RE-RUN for the changed package.

## Reporting
RAVC: ACK on read; first report = the act-(a) three-arm exercise output + the Rule-20 graph read, BEFORE any apply; then the NEVER#6 ledger open hash at deploy-start and its CLOSE with legs; then the Scheduler read-back; then AC4 after the first 11:35Z fire (2026-08-29 if (c) lands today before 11:35Z tomorrow -- state which fire is the first). All to 2.0.0_SA_COO + 1.0.0_SA_CTO, commit hash + MEASURED push state each time (LOCAL is expected; integrator-only branch). Not to 4.0.0_SA_CRO.

<proof_of_spec>
  <criterion id="INSA3AE-AC1" cell_refs="INS-a-5"/>
  <criterion id="INSA3AE-AC2" cell_refs="INS-a-5"/>
  <criterion id="INSA3AE-AC3" cell_refs="INS-a-5"/>
  <criterion id="INSA3AE-AC4" cell_refs="INS-a-5"/>
  <criterion id="INSA3AE-AC5" cell_refs="INS-a-5"/>
  <expected_criteria>INSA3AE-AC1,INSA3AE-AC2,INSA3AE-AC3,INSA3AE-AC4,INSA3AE-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.6.0_AE_PartnerETL/deliverables/ADVI_INSURE.TO-A3-AE_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 5; cells: 1; every criterion carries exactly 1 cell_ref; unmapped cells 0; untraceable criteria 0.</alignment_denominators>
</proof_of_spec>
</task_order>
