<task_order id="NFRA_CTLPLN.TO-CT-w-3.data-proxy-firm-check-apply-and-exercise">
<to_id>NFRA_CTLPLN.TO-CT-w-3.data-proxy-firm-check-apply-and-exercise</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-12</date>
<status>staged</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>8</round>
<workstream>THREAD</workstream>

<title>NFRA_CTLPLN round 8 CT-w-3: read the data proxy's live callers by firm, apply the firm check on its two open routes by Terraform under a second signed pair, and exercise it</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round8.md</decomp_doc>
<owned_cells>CT-w-3</owned_cells>
<decomp_context>FWD-28 (PRD v0.25), the plan of record's steps 5-7 (org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/0.9.0_WK_NFRA_CTLPLN~64/PROPOSAL_FIRM_ACCESS_REGISTRY_ROW.md section 7). CT-w-1 and CT-w-2 build and test the change; this order puts it live and proves it. The first pair (CT-u-7) put the 39 internal-only routes live and is closed.</decomp_context>
</decomp_ref>

<context>
STAGED. The issuer's GO (a crossbox file) arrives when `CT-w-2` is merged AND the SECOND signed pair is on the record: COO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-w-3_PAIR_*.md`, CTO half under `deliverables/1.0.0_SA_CTO/`. It names the PIN (the merge commit carrying `firm_page_access.py`, the handler and the source map). Do nothing before both. READ BOTH HALVES WHOLE.
The change NARROWS: after it, a verified login whose `firmId` is outside a route's admitted set loses the two open routes (`POST /sentiment/keyword-intelligence`, `GET /aum/metrics`). Lambda code changes by Terraform only (`safe-apply`, root `infra/aws/terraform/market-overview/`, resource `aws_lambda_function.portal_data_proxy`); never `aws lambda update-function-code`.
</context>

<the_act>
1. Load `/cloud-ops`. Open ONE NEVER-2 ledger entry (`deploy_ledger.py open`) naming the function, the pin, the artifact key `market-overview/opal-portal-data-proxy.zip` and its PREVIOUS version id (rollback = re-apply it), and the consumers (a Lambda has none; say so). `comp-iam` and the graph query for the function with their denominators.
2. **PRE-APPLY READ (read-only, bounded by timeout).** From the function's CloudWatch logs (the handler prints the full event) over a stated window of at least 24 hours, tabulate every request to the two routes by `firmId` and `tier`. Every non-internal `firmId` must be in that route's `ROUTE_FIRMS` set of the pin. Print the table, the window, the denominator (requests read), and the count NOT admitted. Any `null`, empty or unlisted `firmId` is a named exception: STOP and report it; the CTO rules before any apply. Also confirm once on a live request that `requestContext.authorizer.lambda` carries `firmId`.
3. P0: download the DEPLOYED package and hash `lambda_function.py` and `session_tracker.py`; they must equal the CT-u-7 pin's members (`5f0fad0e...87427`, `00f8c6a3...873ef40`) or you STOP before the build. Build the code-only zip per the source map (which now lists `firm_page_access.py`); read back the zip's MEMBER LIST (3 members) and hash all three against the pin; `safe-apply` on the one root, plan 0 add / 1 change / 0 destroy or STOP; read back the live `CodeSha256`; close the ledger entry only when it equals the built file's.
4. **EXERCISE**, status code and body hash only, never a token, to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-3.firm-check-exercise.txt`: the callers are the CTO half's (b'), as for CT-u-7: the dell walker account armed the walker's way for the INTERNAL caller; an existing seed test row on a partner firm for the PARTNER caller, armed and restored byte for byte in the same ledger entry. Calls: (R1) the partner caller on `GET /aum/metrics`: 200 if its firm is in the route's set, which it is; (R2) a caller of a firm NOT in the set: if no login of such a firm exists, write `NOT-EXERCISED:<reason>` and mint nothing; (R3) the internal caller on both routes: 200; (R4) the partner caller on one class-(ii) route: 403. Final lines, exact form: `class-i admitted-firm=<code> internal=<code>`, `class-i unadmitted-firm=<code or NOT-EXERCISED>`, `class-ii partner=<code>`.
5. Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR: the pin, CodeSha256 before and after, the plan counts, the pre-apply table, the ledger entry and the status codes.
</the_act>

<bounds>
- One Lambda's code only. No IAM, API Gateway, authorizer, table or portal change. No `update-function-code`. No `terraform apply` except through `safe-apply`. A plan that moves anything but the one resource is a STOP. No credential minted; no token printed.
- A pre-apply table that shows a non-internal request NOT admitted is a STOP: report; do not apply.
</bounds>

<proof_of_spec>
<criterion id="CTw3-AC1" cell_refs="CT-w-3"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-3.firm-check-exercise.txt</invocation><expect>class-i admitted-firm=200 internal=200</expect></criterion>
<criterion id="CTw3-AC2" cell_refs="CT-w-3"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-3.firm-check-exercise.txt</invocation><expect>class-ii partner=403</expect></criterion>
<criterion id="CTw3-AC3" cell_refs="CT-w-3"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-3.firm-check-exercise.txt</invocation><expect>PRE-APPLY not_admitted=0</expect></criterion>
</proof_of_spec>
<expected_criteria>CTw3-AC1,CTw3-AC2,CTw3-AC3</expected_criteria>
The exercise file also carries the line `PRE-APPLY window=<h>h requests=<n> not_admitted=<k>` from step 2. Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-w-3.data-proxy-firm-check-apply-and-exercise.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTw3-AC1,CTw3-AC2,CTw3-AC3`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~U7/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
infra/aws/terraform/market-overview/
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one-time apply.
comp-iam: RUN at step 1 -- denominator one function; the seat's own apply grant on the one root; BLIND to every other function behind the authorizer.
comp-adversary: RUN -- a partner firm refused that a page it may open calls (the pre-apply table is the gate, not_admitted must be 0); the zip missing the new module at its root (member list read back); the live code not being the CT-u-7 pin (P0); a minted credential (forbidden); BLIND: callers outside the authorizer path (direct invokes, ruled c404) and any caller of the two routes outside the 24-hour window.
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, the one Terraform root and the surprise channel.
</preflight>

Source: `ROUND_ANALYSIS.round7.md` section 3 (E10), CTO msg 108481 and 108494, the proposal section 7.
</task_order>
