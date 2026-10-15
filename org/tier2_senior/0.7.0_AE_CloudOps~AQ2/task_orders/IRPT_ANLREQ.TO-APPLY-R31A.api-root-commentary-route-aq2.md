<task_order>
  <metadata>
    <id>IRPT_ANLREQ.TO-APPLY-R31A.api-root-commentary-route-aq2</id>
    <issued_by>2.0.0_SA_COO~Y2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~AQ2</issued_to>
    <date>2026-10-15</date>
    <status>complete</status>
    <project_code>IRPT_ANLREQ</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<placeholders>NONE</placeholders>
<preflight>
comp-blast: DECLARED-NOT-APPLICABLE -- the blast radius is named in the signed addendum (section 3, W8): one new authenticated route on the shared API 7k3ed8px20 in front of the existing irpt-status integration; nothing else moves in this leg.
comp-routes: RUN-AS-A-READ -- the plan and the get-routes read are this order's instruments; the one route change is the act itself. comp-cache: DECLARED-NOT-APPLICABLE. comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule or trigger.
comp-iam: DECLARED-NOT-APPLICABLE -- no IAM statement and no Lambda permission is added (the existing permission covers the prefix, integrations.tf:73); the route is released through Terraform only.
comp-adversary: RUN -- by reading AQ2's hold (msg 8078, row D2-S115) and the contract at HEAD against this cell; the lens: a plan that carries more than the one route (another project's unapplied declaration), a route pointed at the wrong integration or without the authorizer, a signed-out probe that cannot discriminate, a rollback by hand-deleting the route. The order requires the plan shape before any apply, the readback of the route's target and authorizer, and Terraform-only rollback. NOT seen (blind): the live api-root state and the live route list until steps 2 and 3; denominator: 5 after-reads, 1 route.
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/IRPT_ANLREQ_DECOMP_R40A_Y.md</decomp_doc> round 40, workstream ZZ8: the apply of release 31, leg A (the api-root route for commentary-pdf).
<owned_cells>AR-y-347</owned_cells>
</decomp_ref>

  <objective>
    Leg A of release 31, and nothing else: create the one gateway route for `commentary-pdf` through the `api` Terraform root, read it back, then STOP and report to 2.0.0_SA_COO~Y2. Leg L is a different order and must be closed first; leg R is a different order to a different seat; do not touch either.
  </objective>

  <context>
    Load /cloud-ops first. Signed pair and addendum: the pair org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~Y2/release31/NEVER_WIDEN_PAIR_ANLREQ_RELEASE31_COMMENTARY_CHAIN.md (blob 8fb19a33566830e264dfa73ffa6897ba4d6f7c8f) and ADDENDUM 1 in the same folder, NEVER_WIDEN_PAIR_ANLREQ_RELEASE31_ADDENDUM1_API_ROOT_ROUTE_COO_HALF.md (blob 322dbb24102ca1cbf40b94967f40ae59fe23e2d4), with its CTO half signed on that blob (CTO msg 8088, commit e138abf69d; org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ANLREQ_RELEASE31_ADDENDUM1_API_ROOT_ROUTE_CTO_HALF.md). A different blob voids it: STOP. The addendum is the plan: sections 2 (what moves), 3 (W8), 4 (gates, reads, rollback).
    THE FACTS (RECORD, read by the issuer): infra/aws/terraform/investor-reporting/api/routes.tf creates one aws_apigatewayv2_route per row of docs/contracts/investor-reporting/v1/routes.json whose status is DECLARED, target the integration of its handler, authorization CUSTOM, authorizer naqxlm; the row for GET /api/scoped/investor-reporting/analysis/requests/{requestId}/commentary-pdf is DECLARED, handler irpt-status. State key s3://opal-313476888478-terraform-state/investor-reporting/api/tfstate. The precedent apply is HISTORY_ROUTES_APPLY_20260924.json (plan 2 to add, replan No changes, get-routes readback). Use the worktree-provisioned .tools/terraform.exe by that path, never a PATH substitute.
  </context>

  <the_act>
    GO: the addendum's CTO half is signed at the blob above. This order runs AFTER leg L (TO-APPLY-R31L, amended): step 1 reads A_AFTER_R31L.txt and STOPS if L1 is not there. Start at step 1 and go on only while each step reads green. Otherwise tell 2.0.0_SA_COO~Y2 and wait.
    1. `git hash-object` of the addendum COO half must print 322dbb24102ca1cbf40b94967f40ae59fe23e2d4; read the CTO half at HEAD and print its signed blob. Read A_AFTER_R31L.txt: L1 holds (PcGK...). Open the NEVER-2 ledger irpt-api-r31a-20261015 and commit it; read every live worktree's org/critical_paths/.open_deploys/ first (git worktree list, then git -C <wt> ls-tree) and print the denominator: another open entry naming the api root, API 7k3ed8px20 routes or this key is a STOP.
    2. R0s. In infra/aws/terraform/investor-reporting/api (trunk HEAD that contains the contract row; print the sha and `git hash-object` of docs/contracts/investor-reporting/v1/routes.json): `terraform init` (existing backend, no change), then `terraform plan -lock=false -out` a saved plan. The summary MUST read `Plan: 1 to add, 0 to change, 0 to destroy` and the one address MUST be aws_apigatewayv2_route.irpt["GET /api/scoped/investor-reporting/analysis/requests/{requestId}/commentary-pdf"]. Print every resource line of the plan. ANY other line: STOP, nothing applied, write the lines to the proof file and tell 2.0.0_SA_COO~Y2.
    3. Read the live route list before the apply (get-routes of 7k3ed8px20, the whole JSON, never a paged count) and print the count (AQ2 read 121) and whether any key ends in /commentary-pdf (expect none). Record the id of the integration whose uri is irpt-status.
    4. `.tools/safe-apply.sh` on the saved plan. Never a bare terraform apply, never `aws apigatewayv2 create-route`.
    5. After-reads (V-A): A1 get-routes: the new route present, target integrations/<the irpt-status integration id of step 3>, authorizer naqxlm, authorization type CUSTOM, and the route count equal to step 3's plus one. A2 a replan of the same root reads `No changes`. A3 a credential-less GET on the new route answers the edge refusal (status and body sha256), and the control (a made-up path under /api/scoped/investor-reporting/) answers the same: write both; this arm does not discriminate and the line says so. A4 the existing report PDF route answers as before (print what it answers, credential-less).
    6. Write org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/A_AFTER_R31A.txt with, ONE line each, exactly: `A1 route present irpt-status naqxlm CUSTOM count 122`, `A2 replan No changes`, `A3 edge refusal equal to control (non-discriminating)`, `A4 report pdf route as before`; then the route id and the step 3 count (not a credential). A line that did not hold is written `<tag> FAIL <what was read>`; if A1 failed, do NOT repair by hand: write it and wait for 2.0.0_SA_COO~Y2.
    7. Commit, close the ledger, and report ONCE to 2.0.0_SA_COO~Y2: "leg A closed" with the route id, the counts, the plan sha and the output path. Report the Terraform apply to 0.0.0_AB_MSTR~DELL2 after the fact. Remove every throwaway worktree you made (git worktree remove; a recursive delete of anything you did not create needs Andrew's word).
  </the_act>

  <bounds>
    One route resource. No Lambda code, permission, integration, authorizer, IAM, CloudFront or other Terraform change. No ticket, request or mail is created. Not in this order: leg L, leg R, the intake Lambda, the portal. Rollback (the addendum's section 4): the contract row's status off DECLARED in a committed edit by 2.0.0_SA_COO~Y2, plan 0 to add, 0 to change, 1 to destroy, safe-apply; never a hand delete; roll leg R back before this leg and this leg before leg L.
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/IRPT_ANLREQ.TO-APPLY-R31A.api-root-commentary-route-aq2.proof_of_spec.json`.
    <criterion id="R31A-AC1" cell_refs="AR-y-347">The route is present with the irpt-status target and the authorizer, and the replan reads No changes.<invocation>grep -c -E '^(A1 route present irpt-status naqxlm CUSTOM count 122|A2 replan No changes)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/A_AFTER_R31A.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="R31A-AC2" cell_refs="AR-y-347">The edge probe is recorded as non-discriminating and the report PDF route answers as before.<invocation>grep -c -E '^(A3 edge refusal equal to control \(non-discriminating\)|A4 report pdf route as before)$' org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_r31/A_AFTER_R31A.txt</invocation><expect>^2$</expect></criterion>
    <criterion id="R31A-AC3" cell_refs="AR-y-347">The ledger irpt-api-r31a-20261015 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-api-r31a-20261015_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
  </proof_of_spec>
</task_order>
# pipeline-override: an APPLY order to a tier-2 applier under a signed pair addendum (not a worker cell); the cell AR-y-347 is the issuer's, as for TO-APPLY-R31L.
