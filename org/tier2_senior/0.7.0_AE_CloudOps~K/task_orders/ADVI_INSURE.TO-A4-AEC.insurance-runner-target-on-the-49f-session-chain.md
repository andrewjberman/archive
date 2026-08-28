# TO ADVI_INSURE.TO-A4-AEC — INSURE becomes the canonical 49F session chain's THIRD RUNNER TARGET: cron + marker vocabulary + payload map + ONE invoke-policy ARN in bd-pipeline (LAPTOP)

<task_order id="ADVI_INSURE.TO-A4-AEC" project="ADVI_INSURE">
⛔ <distribution>NOT TO 4.0.0_SA_CRO, at every relay (ADVI_INSURE PRD s.3).</distribution>
<decomp_ref>workflows/atom_decomposition/runs/advi-insure-snapshot-plane/20260825T122500Z/DECOMP.md — cell INS-a-5 (issuer amendment 2026-08-28; VEHICLE RE-RULED ~17:5xZ on Andrew-direct 17:40Z + CTO ledger row 14)</decomp_ref>
<decomp_context>ONE cell, TWO lanes, ONE acceptance. Andrew-direct at the CTO terminal 2026-08-28 ~17:40Z, VERBATIM: "Yeah this would be a pipeline function, not an agent, we would need to build it in the same bd api lambda route that is canonical in data/assets/docs/ or wherver" and "agents have egress to do research and check it out" (record: org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20260828_1740Z_INSURE_PULL_IS_A_PIPELINE_FUNCTION_ON_THE_CANONICAL_BD_API_LAMBDA_ROUTE.md). CTO ruling (D2-D3 ledger row 14, measured at source): the canonical route is the bd-pipeline 49F session chain (data/assets/docs/BD_API_DESIGN.md Design of Record :29-51) -- per-target daily EventBridge cron -> bd-49f-session-trigger {mode: session-refresh, runner: <target>} -> fresh .bd.identity mint (or Lever-A live-probe skip) -> bd-49f-session-complete -> runner-run reads the cycle marker -> _fire_runner(target). It already carries two targets: main (00:00Z) and fees (22:20Z MON-FRI) via _RUNNER_BY_TARGET (infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py:57) and the invoke policy (infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf:120-121). INSURE becomes the THIRD target 'insurance' = opal-assets-bd49f-reporting-pull invoked WITH PAYLOAD {"leg":"insurance"} -- the leg is already REACHABLE in that Lambda's deployed handler (ADVI_INSURE.TO-A3-AE act (b) @d0f9a8f7e4, ledger 20260828T1725Z CLOSED 5/5, CodeSha256 JyQp8pROQ0lZFHjQ5NzO4AAaWsVja/MvTmcVrUB9MXw=; QA invoke 17:43:19Z landed 77/77 across 2 pages with the reporting branch NOT run). NOT inside bd-49f-runner: it is firm-bound to opal-data-bd only; the insurance mint is ruled at opal-data-assets/blackdiamond/49financial/. The reporting-pull side (INSURANCE_EGRESS ON, .tf comment) is 0.6.0_AE_PartnerETL's under TO-A3-AE (c'). This TO is the CHAIN-WIRING half.</decomp_context>
<certification>PENDING 3.0.0_SA_CVO cert step-zero on the amended INS-a-5 + this face (CVO base LIVE since 17:40Z). "Alt base CTO" is refused for this cell (CTO 78482: the cell was ruled at that seat; the verifier is not the do-er).</certification>
<issued_to>0.7.0_AE_CloudOps~K</issued_to>
<executor_class>AE-class (cloud/infra: bd-pipeline EventBridge + session-trigger Lambda + IAM, Terraform). The 0.7.0 base owns bd-pipeline per the session-trigger docstring; the base is dark and ~L holds the campaign, so this lane is seated for THIS TO only.</executor_class>
<issued_by>2.0.0_SA_COO</issued_by>
<issued>2026-08-28T17:5xZ</issued>
<status>pending</status>
<priority>P1 -- the production cadence of INSURE's P2 vehicle (docs/briefs/d2-critical-path-sequencing-20260827.md sec 4 :60); ADVI_INSURE.TO-R1-DS AC2/AC3 and the silver STAGE build (DS lane, re-seated on this TO's first fire) read against it; the D2 serve gate (P3) needs P2's QA emission.</priority>
<placement>LAPTOP (Rule 26).</placement>
<scope_guard>ONE cell, the chain-wiring half ONLY, in bd-pipeline. ⛔ main and fees targets keep their EMPTY payload and their :206-208 invariant UNTOUCHED -- the payload map is additive and keyed on 'insurance' only. ⛔ bd-49f-runner is NOT touched (firm-bound to opal-data-bd). ⛔ ONE ARN added to the session-trigger's lambda:InvokeFunction Resource list -- no wildcard, no second action; no resource policy on the reporting-pull (same-account role invoke). ⛔ NO alarm / SNS / monitor / twin (INS-inv-5, standing moratorium) -- a cron is a trigger, not an alarm. ⛔ Terraform + safe-apply ONLY on a SAVED, -target'd plan; never `aws lambda update-function-code`; a begun deploy FINISHES in-session or rolls back (NEVER#6, ledger via .tools/deploy_ledger.py opened at deploy-start). ⛔ CTO PLAN-GATE BEFORE APPLY on the IAM diff (CTO row 14 item 2(c)): send the saved plan's diff to 1.0.0_SA_CTO + 2.0.0_SA_COO; apply only on 1.0.0_SA_CTO's GO. ⛔ The reporting-pull Lambda's own code/env is 0.6.0's (TO-A3-AE) -- do not edit it here; coordinate the deploy ORDER with 0.6.0 (the flag ON must be live before the first fire, or the first fire refuses fail-closed and is a negative control, not an acceptance). ⛔ The untargeted plan in infra/aws/terraform/opal-assets carries another seat's un-applied X-ii-a changes -- that root is NOT this TO's; if any plan here shows a foreign change, STOP and surface. Adjacent findings: one line to 3.0.0_SA_CVO cc 2.0.0_SA_COO, keep working.</scope_guard>

## The acts, in this order (CTO row 14 item 2, verbatim intent)

(a) bd-49f-session-trigger (infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py): `_RUNNER_BY_TARGET['insurance'] = INSURANCE_RUNNER_FUNCTION_NAME` read from env (default "opal-assets-bd49f-reporting-pull"); the cycle-marker vocabulary gains `insurance`; `_fire_runner` gains `_PAYLOAD_BY_TARGET = {'insurance': {'leg': 'insurance'}}` and passes that payload for the insurance target ONLY -- main/fees keep the EMPTY payload (:206-208 invariant untouched, asserted by a test arm). Exercised locally with THREE arms before any deploy: target=insurance -> the reporting-pull function name + payload {"leg":"insurance"}; target=main -> bd-49f-runner + EMPTY payload (unchanged); target=bogus -> the existing :98 refusal. Package rebuilt via the chain's existing build path (source map verified BEFORE building; members read from the BUILT zip; deployed members resolved via the manifest, never by filename).
(b) infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf: (i) env `INSURANCE_RUNNER_FUNCTION_NAME = "opal-assets-bd49f-reporting-pull"` on the session-trigger; (ii) the session-trigger policy's `lambda:InvokeFunction` Resource gains the reporting-pull function ARN (ONE ARN, :120-121); (iii) EventBridge rule `bd-49f-insurance-session-daily`, `cron(35 4 * * ? *)` UTC, daily incl. weekends, input `{"mode":"session-refresh","runner":"insurance"}`, target = the session-trigger (the existing fees template :235-260 is the model); (iv) the file's stagger comment (:16-17, :33) amended to name insurance 04:35Z and the measured gaps (>= 2h35m clear of fees 22:20Z / main 00:00Z / cot 02:00Z; > the 1h40m stagger floor + the 1500s mint timeout). `terraform fmt -check` (never `-diff`), `validate`, SAVED -target'd plan; PLAN DIFF to 1.0.0_SA_CTO + 2.0.0_SA_COO; apply on CTO's GO via safe-apply; counts == plan; 0-diff re-plan.
(c) IAM acceptance on the LIVE primitive (one --resource-arns per call, controls as SEPARATE invocations): the session-trigger role -> `allowed` lambda:InvokeFunction on the reporting-pull ARN; the same role -> `allowed` on bd-49f-runner (unchanged, positive control); the same role -> `implicitDeny` on advi-49f-gold-dispatch (the fence is real); comp-iam gaps re-run after the iam edit (necessary, not sufficient).
(d) ACCEPTANCE on the SCHEDULED plane = the FIRST chain fire with runner=insurance (2026-08-29T04:35Z if (b) lands today AND 0.6.0's INSURANCE_EGRESS=ON is live before it): session-trigger's own CloudWatch log (marker runner=insurance; invoked target=insurance with the payload), the reporting-pull's own log (BD49F-INSURANCE line: insurance branch ran, pages to the attested total, completeness=measured-complete; NO BD49F-REPORTING line), head-object at blackdiamond/49financial/bronze/insurance_*/{pull_date}/ (s3api UTC) for every page; NEGATIVE CONTROL = the same day's main run (00:00Z) did NOT enter insurance (its own log). A manual invoke is QA evidence only.

## Acceptance criteria

| id | criterion | layer |
|---|---|---|
| **INSA4AEC-AC1** | (a) built + exercised: three arms (insurance -> reporting-pull + payload; main -> runner + EMPTY; bogus -> refusal), main/fees payload invariant asserted; source map verified before build; deployed members via the manifest. | DESIRED -> BUILT |
| **INSA4AEC-AC2** | (b) landed: safe-apply on the SAVED -target'd plan after 1.0.0_SA_CTO's GO on the diff; apply counts == plan counts; 0-diff re-plan; the rule, its target, its input and the env var read back LIVE (`aws events describe-rule` / `list-targets-by-rule`; `get-function-configuration`); NEVER#6 ledger opened at deploy-start and CLOSED with every leg proven. | APPLIED |
| **INSA4AEC-AC3** | (c) IAM: the three-arm live acceptance above, quoted; comp-iam gaps output quoted. | APPLIED |
| **INSA4AEC-AC4** | (d) the FIRST chain fire with runner=insurance, read from BOTH Lambdas' own logs + head-object per page + the same-day main run as the negative control. Closes only on a SCHEDULED fire. | EXERCISED |
| **INSA4AEC-AC5** | Proof instance VALID rc=0 positional, ids INSA4AEC-AC1..AC5, TRUE rc bare, validator invocation + rc recorded IN the instance (D2 lock-in); every arm's output quoted. | — |

<compiler_tools_mandate>
BEFORE WRITE: Rule-20 dependency-graph query per org/modules/graph/graph-call-manifest.yaml on bd-49f-session-trigger + the reporting-pull ARN (QUERY, never rebuild; provenance header read); `comp-blast` on infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf + the session-trigger dir (the chain's other two targets ride the same trigger); `comp-iam service bd-49f-session-trigger` (the policy Resource list is the change).
BEFORE COMMIT: `.tools/commit-gate.sh` on the .py; `terraform fmt -check` + `validate`; the three-arm exercise green with a RED arm shown (e.g. a planted non-empty payload for main must fail the invariant assertion).
AFTER COMMIT / DEPLOY: live reads (describe-rule, list-targets-by-rule, get-function-configuration env, simulate-principal-policy x3); the first fire's logs read from the fires themselves.
</compiler_tools_mandate>

<cross_domain_coordination>
- 0.6.0_AE_PartnerETL (ADVI_INSURE.TO-A3-AE (c')): the reporting-pull side -- INSURANCE_EGRESS ON in the deployed env + the .tf comment; DEPLOY ORDER: 0.6.0's flag must be live before this TO's first fire (else the fire refuses fail-closed = a negative control, not the acceptance). Coordinate the timestamp by broker; 2.0.0_SA_COO sequences.
- 0.7.0_AE_CloudOps~L (ADVI_49F P14-VEHICLE campaign on the EC2 runner): disjoint substrate; the campaign's runner-side blackout (12:45Z) does not bind a Lambda chain; the 04:35Z slot is measured clear of every existing chain fire.
- The main (00:00Z) and fees (22:20Z) targets: behaviour UNCHANGED, asserted by the exercise's main arm; their owners are not on the wire -- everything to preserve in code.
- OPAL_TAXSMA_PT2 (the reporting payload of the same Lambda): untouched; its WS-5 trigger design stays its own.
- DS lane (INSURE silver STAGE): re-seated on this TO's first fire (COO ruling 78492); the stage consumes the 04:35Z bronze at the 12:45Z floor.
- Shared S3: this TO writes NO S3 objects; the fire writes under opal-data-assets/blackdiamond/49financial/bronze/insurance_* via the reporting-pull's own role (already granted, TO-A1-AE L6).
</cross_domain_coordination>

## Compiler tools
Mandate above is three-phase and binding; the session-trigger's own two-target invariant is the thing every instrument here protects.

## Reporting
RAVC: ACK on read; FIRST REPORT to 2.0.0_SA_COO + 1.0.0_SA_CTO = the (a) three-arm exercise output + the Rule-20 read + the saved plan's DIFF (the gate artifact), BEFORE any apply; then the ledger open hash at deploy-start and its CLOSE with legs; then the live read-backs; then AC4 after the first 04:35Z fire (state which fire is the first). Commit hash + MEASURED push state each time (LOCAL is expected; integrator-only branch). Not to 4.0.0_SA_CRO.

<proof_of_spec>
  <criterion id="INSA4AEC-AC1" cell_refs="INS-a-5"/>
  <criterion id="INSA4AEC-AC2" cell_refs="INS-a-5"/>
  <criterion id="INSA4AEC-AC3" cell_refs="INS-a-5"/>
  <criterion id="INSA4AEC-AC4" cell_refs="INS-a-5"/>
  <criterion id="INSA4AEC-AC5" cell_refs="INS-a-5"/>
  <expected_criteria>INSA4AEC-AC1,INSA4AEC-AC2,INSA4AEC-AC3,INSA4AEC-AC4,INSA4AEC-AC5</expected_criteria>
  <instance_path>org/tier2_senior/0.7.0_AE_CloudOps~K/deliverables/ADVI_INSURE.TO-A4-AEC_PROOF_OF_SPEC.json</instance_path>
  <alignment_denominators>criteria: 5; cells: 1; every criterion carries exactly 1 cell_ref; unmapped cells 0; untraceable criteria 0.</alignment_denominators>
</proof_of_spec>
</task_order>
