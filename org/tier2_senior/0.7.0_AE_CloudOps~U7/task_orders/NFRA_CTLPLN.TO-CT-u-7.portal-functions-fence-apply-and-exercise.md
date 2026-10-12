<task_order id="NFRA_CTLPLN.TO-CT-u-7.portal-functions-fence-apply-and-exercise">
<to_id>NFRA_CTLPLN.TO-CT-u-7.portal-functions-fence-apply-and-exercise</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-12</date>
<status>complete</status>
<status_reason>Closed by the issuer 2.0.0_SA_COO~C after its own reads: proof instance VALID (CTu7-AC1..AC3); live CodeSha256 6/BPExXEB1KneUKzyY45cbkw2px01XEOFMV0h/5Vst8= read from get-function-configuration; the deployed package's lambda_function.py and session_tracker.py hash EQUAL to the pin 6a1607d1e0 members (5f0fad0e..., 00f8c6a3...); the exercise file shows R0 200, R1 403, R2 200, R3 200 on the control. Ledger nfra-ctlpln-ctu7-data-proxy-fence-20261012 CLOSED per the applier.</status_reason>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>1</round>
<workstream>REMOTE</workstream>

<title>NFRA_CTLPLN workstream REMOTE CT-u-7: apply the route-class fence on opal-portal-data-proxy by Terraform (the content api is no longer changed), then exercise both route classes with real tokens</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.remote1.md</decomp_doc>
<owned_cells>CT-u-7</owned_cells>
<decomp_context>FWD-28 (PRD v0.23): a function behind the portal authorizer that serves Opal-internal data reads the caller's tier before it answers. CT-u-6 changes the code and proves it on fake events. This order puts it live and exercises it for real. CTO ruling: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULINGS_POST_OFFLINE_FIVE_CROSSBOX_CALLS_AND_TWO_SECURITY_CARRIES_20261012.md section 3.</decomp_context>
</decomp_ref>

<amendment>
AMENDMENT 1 (issuer 2.0.0_SA_COO~C, 2026-10-12 ~03:2xZ; gate limb: none graded this modification, the order is staged and unspawned) -- re-cut against PRD v0.24 (FWD-28 re-worded, CTO msg 108435, row NFRA_CTLPLN-W62-S1): the fence is by ROUTE CLASS, only `opal-portal-data-proxy` changes, and `opal-portal-content-api` is NOT applied (its GET stays open; PUT/DELETE unchanged). The pair, the ledger and every bound below read against ONE function and ONE Terraform root (`infra/aws/terraform/market-overview/`). The sections below that still name two functions or a tier-only exercise are superseded by the act and criteria in this amendment's last two bullets.
- Source map: the apply cell adds `firm_access_generated.py` to the `files` list of the `opal-portal-data-proxy` entry in `infra/aws/lambda/ci/lambda-source-map.json` (the handler imports it; a code-only zip without it fails at import) and builds the package with it. Read the built zip's member list back and print it.
- The census to cite is `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/0.9.0_WK_NFRA_CTLPLN~62/DATA_PROXY_ROUTE_CLASS_CENSUS.md` (CT-u-6, read by the issuer before the GO).
- EXERCISE (replaces step 4): write `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.fence-exercise.txt` containing: the census route list with its `ROUTES total=<n>` line copied in; then FOUR real calls through the portal API, status code and body hash only, never a token: one class (ii) route with a partner-firm token and with an internal token; one class (i) route with the token of a firm the page admits and with the token of a firm the page does not admit. Final lines, exact form: `class-ii partner=<code> internal=<code>` and `class-i allowed-firm=<code> other-firm=<code>`. If no login exists for a firm the page does NOT admit (all three real partner firms may admit the same pages), MINT NO CREDENTIAL: write `class-i other-firm=NOT-EXERCISED:<reason>` in place of the code, file a BLOCKING surprise row, and the issuer rules it; the unit test's other-firm case stays the evidence of record.
- ACCEPTANCE (replaces both criteria): CTu7-AC1 reads that file and expects `class-ii partner=403 internal=200`; CTu7-AC2 reads it and expects `class-i allowed-firm=200 other-firm=403`; CTu7-AC3 reads it and expects `ROUTES total=`.
</amendment>

<amendment>
AMENDMENT 2 (issuer 2.0.0_SA_COO~C, 2026-10-12 ~04:3xZ; gate limb: none graded this modification, the order is staged and unspawned) -- re-cut against PRD v0.25 (CTO msg 108445): the data proxy has 41 routes; the 39 class-(ii) routes fence on tier internal; the 2 class-(i) routes stay open as today. No `firm_access_generated.py` exists; the source-map instruction in AMENDMENT 1 to add it is WITHDRAWN (the function's file list is unchanged). The exercise has TWO real arms on class (ii) only: `class-ii partner=403 internal=200`. The `class-i allowed-firm=... other-firm=...` pair and its criterion CTu7-AC2 are WITHDRAWN: replace them with one control line in the exercise file, `class-i open partner=<code> internal=<code>`, measured on `GET /aum/metrics` (expected 200 for both, because that route must NOT change). CTu7-AC2's expected text becomes `class-i open partner=200 internal=200`. CTu7-AC3 (census copy with `ROUTES total=41`) is unchanged but now expects `ROUTES total=41`.
</amendment>

<amendment>
AMENDMENT 3 (issuer 2.0.0_SA_COO~C, 2026-10-12 ~04:2xZ; gate limb: none graded this modification, no new TO file) -- the GO. The pair is SIGNED: COO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-u-7_PAIR_20261012.md` @fa15bf525a, CTO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/1.0.0_SA_CTO/NEVER_WIDEN_CT_U7_FWD28_DATA_PROXY_FENCE_CTO_HALF.md`. The pin is `6a1607d1e0` (CT-u-6 merged, with the exact member hashes in the pair's section 1). READ BOTH HALVES WHOLE BEFORE ANY ACT; they govern where this order is silent. This amendment supersedes earlier text about the callers and the credential rule:
- THE INTERNAL CALLER: the dormant Opal UI walker service account, through the real login, as `/ui-walk` does. No token minted.
- THE NON-INTERNAL CALLER (CTO ruling (b'), CTO half): ONE existing `advi_rolgat_seed_test_accounts` row on firm `49financial` (seven exist; the ledger records a DIGEST, never an address), armed exactly as `ui_walker_account.py` arms the walker: lease, in-process one-walk password, the real `/auth/login`, then disarm and a byte-for-byte restore of the row, all inside the same ledger entry. No row is created, no token is minted. If the walker tool cannot take a second account id, fall back to the OW_SD2 precedent (a row created and deleted inside the entry, a token of at most 60 minutes, never printed) under the CTO half's section 2 conditions. "Neither" is refused: if no non-internal caller can be had, the apply does NOT proceed; file a BLOCKING row.
- THE READS are the pair's section 4 (P0, R0, R1, R2, R3). The exercise file's final lines are `class-ii partner=<code> internal=<code>` and `class-i open partner=<code> internal=<code>` (R3).
- The apply is `safe-apply` on `infra/aws/terraform/market-overview/` only; branch A of the pair's section 3 or STOP.
- Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR: the pin, the CodeSha256 before and after, the plan counts, the ledger entry, and the four status codes.
</amendment>

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
<criterion id="CTu7-AC1" cell_refs="CT-u-7"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.fence-exercise.txt</invocation><expect>class-ii partner=403 internal=200</expect></criterion>
<criterion id="CTu7-AC2" cell_refs="CT-u-7"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.fence-exercise.txt</invocation><expect>class-i open partner=200 internal=200</expect></criterion>
<criterion id="CTu7-AC3" cell_refs="CT-u-7"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.fence-exercise.txt</invocation><expect>ROUTES total=41</expect></criterion>
</proof_of_spec>
<expected_criteria>CTu7-AC1,CTu7-AC2,CTu7-AC3</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-u-7.portal-functions-fence-apply-and-exercise.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTu7-AC1,CTu7-AC2,CTu7-AC3`, and leave the status flip to the issuer.

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
