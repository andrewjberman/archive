<task_order id="NFRA_CTLPLN.TO-CT-u-7.portal-functions-fence-apply-and-exercise">
<to_id>NFRA_CTLPLN.TO-CT-u-7.portal-functions-fence-apply-and-exercise</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-12</date>
<status>staged</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>1</round>
<workstream>REMOTE</workstream>

<title>NFRA_CTLPLN workstream REMOTE CT-u-7: apply the caller-tier fence on opal-portal-data-proxy and opal-portal-content-api by Terraform, then call each with a partner token (403) and an internal token (200)</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.remote1.md</decomp_doc>
<owned_cells>CT-u-7</owned_cells>
<decomp_context>FWD-28 (PRD v0.23): a function behind the portal authorizer that serves Opal-internal data reads the caller's tier before it answers. CT-u-6 changes the code and proves it on fake events. This order puts it live and exercises it for real. CTO ruling: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_POST_OFFLINE_FIVE_CROSSBOX_CALLS_AND_TWO_SECURITY_CARRIES_20261012.md section 3.</decomp_context>
</decomp_ref>

<context>
STAGED. The issuer's GO (a crossbox file) arrives when `CT-u-6` is merged and the signed pair is on the record. It names the merge commit (the PIN) carrying the changed `infra/aws/lambda/portal_data_proxy/lambda_function.py` and `infra/aws/lambda/portal_content/lambda_function.py`, and the path of the pair. Do nothing before both.
The pair: the COO half is written by the issuer and the CTO half by `1.0.0_SA_CTO`, at `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-u-7_PAIR_*.md`. It names the blast radius: the change NARROWS access (partner callers get 403 on 11 data routes and on the content GET). The risk is the opposite one: a page a partner login can open that calls these routes breaks. CT-u-6's worker lists any such page in the surprise channel; read those rows before you apply. Rollback per function: re-apply the previous package version recorded in the ledger entry.
Terraform resources, two roots: `aws_lambda_function.portal_data_proxy` in `infra/aws/terraform/market-overview/lambdas.tf`; `module.opal_portal_content_api.aws_lambda_function.this` in `infra/aws/terraform/portal-content/main.tf`. Lambda code is changed by Terraform only, never `aws lambda update-function-code`. Build and upload follow each function's entry in `infra/aws/lambda/ci/lambda-source-map.json`.
</context>

<the_act>
1. Load `/cloud-ops`. Open ONE NEVER-2 ledger entry (`deploy_ledger.py open`) naming both functions, every task family or consumer that pulls them (a Lambda has none, say so), the pin, and the per-function rollback. Run `comp-iam` and the dependency-graph query for both functions and record the denominator.
2. For each function in turn: build the code-only package per the source map, upload it, run `safe-apply` on its Terraform root with the plan read from the plan JSON. EXACTLY ONE resource may move per root (the function's code hash and version); anything else is a STOP, not an apply.
3. Record each apply (`record-terraform-deploy.sh`), read back the live `CodeSha256` for each function against the built file, and close the ledger entry only when both match.
4. EXERCISE, real calls through the portal API, written to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.fence-exercise.txt`:
   - one call to `opal-portal-data-proxy` (any of its GET routes) with a PARTNER-tier token, and the same with an INTERNAL token;
   - one `GET` to `opal-portal-content-api` with a PARTNER-tier token, and the same with an INTERNAL token.
   Tokens: obtain an internal token the way `/ui-walk` does (the dormant Opal UI walker service account, local dev channel). For the partner-tier token use an existing partner-tier test login in the portal users pool. If NO partner-tier login exists, MINT NO CREDENTIAL: file a BLOCKING surprise row, write what you did read, and stop that arm; the issuer rules it. Never print a token; print only the HTTP status and a hash of the response body.
   Final lines of the file, exact form: `data-proxy partner=<code> internal=<code>` and `content-api partner=<code> internal=<code>`.
5. Report the pin, the two CodeSha256 values, the plan counts, the ledger entry and the four status codes to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR.
</the_act>

<bounds>
- Two Lambda code packages only. No IAM, API Gateway, authorizer or table change. No `aws lambda update-function-code`. No `terraform apply` except through `safe-apply`. No push of CLOUD. A plan that moves anything other than the one resource per root is a STOP.
- No credential minted; no token printed. No alert, monitor or timeout is built.
</bounds>

<proof_of_spec>
<criterion id="CTu7-AC1" cell_refs="CT-u-7"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.fence-exercise.txt</invocation><expect>data-proxy partner=403 internal=200</expect></criterion>
<criterion id="CTu7-AC2" cell_refs="CT-u-7"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.fence-exercise.txt</invocation><expect>content-api partner=403 internal=200</expect></criterion>
</proof_of_spec>
<expected_criteria>CTu7-AC1,CTu7-AC2</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.portal-functions-fence-apply-and-exercise.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTu7-AC1,CTu7-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~U7/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
infra/aws/lambda/ci/lambda-source-map.json
infra/aws/terraform/market-overview/
infra/aws/terraform/portal-content/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one-time apply.
comp-iam: RUN at the act's step 1 -- denominator two functions; the seat's own apply grant on the two roots; BLIND to every other function behind the authorizer (separate cells and owners).
comp-adversary: RUN -- a partner page breaking silently (CT-u-6's rows are read first); a plan moving more than one resource per root (STOP); a code change landed outside Terraform (forbidden); an internal user 403'd because the authorizer omits `tier` for some token type (the internal-token arm exercises it live, and the rollback is one re-apply); a minted partner credential (forbidden); BLIND: other consumers of the two functions that do not pass the authorizer.
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, the source map, the two Terraform roots and the surprise channel.
</preflight>

Source: PRD `prd/NFRA_CTLPLN_PRD.md` v0.23 FWD-28; CTO msg 108406; ruling section 3 of the CTO rulings file above.
</task_order>
