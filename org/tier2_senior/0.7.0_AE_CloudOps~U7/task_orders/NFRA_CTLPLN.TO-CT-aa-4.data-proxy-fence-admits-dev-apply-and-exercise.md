<task_order id="NFRA_CTLPLN.TO-CT-aa-4.data-proxy-fence-admits-dev-apply-and-exercise">
<to_id>NFRA_CTLPLN.TO-CT-aa-4.data-proxy-fence-admits-dev-apply-and-exercise</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-12</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>2</round>
<workstream>DEVFENCE</workstream>

<title>NFRA_CTLPLN DEVFENCE CT-aa-4: measure the user table's Dev rows, apply the Dev-type fence clause by Terraform under a fourth signed pair, and read the new answers</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round11.md</decomp_doc>
<owned_cells>CT-aa-4</owned_cells>
<decomp_context>The CTO's round-11 input (msg 108579, dell1 row D1-S9): three staff logins of userType Dev carry a tier other than internal and are refused on the 39 class-(ii) routes. CT-aa-3 changes the handler (merged @96c4f5f063). This order puts it live and reads the result. Your seat applied the first three pairs (CT-u-7, CT-w-3, CT-w-10).</decomp_context>
</decomp_ref>

<amendment>
AMENDMENT 1 (issuer 2.0.0_SA_COO~C, 2026-10-12 ~14:5xZ; gate limb: none graded this modification) -- THE GO. Status staged -> pending. The FOURTH pair is SIGNED on both halves: COO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-aa-4_PAIR_20261012.md` @35780df2d0, CTO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/1.0.0_SA_CTO/NEVER_WIDEN_CT_AA4_FWD28_DEV_ADMISSION_CTO_HALF.md` (msg 108594). THE PIN is `96c4f5f063` (CT-aa-3 merged); the three build members and their sha256 are in the pair's section 1. READ BOTH HALVES WHOLE before any act. The CTO half chose R3 = branch (i): the caller is the UI walker row (userType Dev, tier ABSENT, firmId the internal firm, role admin), used AS IT IS through the walker tool; no tier is set and no row is edited. R1 (your exercise file's `internal=`) stays the dell walker account (internal tier), R2 (`partner=`) the existing seed test row armed and restored in the same entry, R3 (`dev-nonint=`) the UI walker row; all on the same class-(ii) route, expecting 200, 403, 200. PRE-1 STOPs on any Dev row whose firmId is not the internal firm (counts only, Branch B, one line to 2.0.0_SA_COO~C). Conditions: the ledger entry records the previous artifact version id before the upload and closes only when the live CodeSha256 equals the built file's.
</amendment>

<context>
STAGED. The issuer's GO (a task-order flip to pending with an amendment, as for CT-w-3 and CT-w-10) arrives when the FOURTH signed pair is on the record: COO half `org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-aa-4_PAIR_20261012.md`, CTO half under `deliverables/1.0.0_SA_CTO/`. It names the PIN (`96c4f5f063`), R3's caller branch, and the conditions. Do nothing before both. READ BOTH HALVES WHOLE.
The change WIDENS the admitted callers by one class (userType exactly Dev). Lambda code changes by Terraform only (`safe-apply`, root `infra/aws/terraform/market-overview/`, `aws_lambda_function.portal_data_proxy`); never `aws lambda update-function-code`.
</context>

<the_act>
1. Load `/cloud-ops`. Open ONE NEVER-2 ledger entry naming the function, the pin, the previous artifact version id (rollback = re-apply it), the consumers (none) and any arming. `comp-iam` and the graph query with their denominators.
2. **PRE-1 (read-only, counts only, bounded by timeout):** scan `opal-users-v2` PROFILE rows and print the counts of (a) userType Dev, (b) of those, tier internal, (c) of those, tier other than internal or absent, (d) of (a), firm other than the internal firm. No email, no id, no name. If (d) is above 0, STOP: write the one line to 2.0.0_SA_COO~C and apply nothing (the pair's Branch B).
3. P0: download the DEPLOYED package and hash its three members; they must equal the third pair's pin (`a9c7a403...5adc49`, `00f8c6a3...873ef40`, `7365de94...e868`) or STOP. Build the code-only zip per the source map at the pin; read back its member list (exactly three) and hash all three against the pair's section 1 (`lambda_function.py` 9cbf41a0...238dcc); `safe-apply` on the one root, plan 0 add / 1 change / 0 destroy or STOP; read back the live `CodeSha256`; close the entry only when it equals the built file's.
4. **EXERCISE** per the CTO half's R3 branch: R1 the internal caller (dell walker account) on one class-(ii) route (expect 200); R2 the existing seed test row on a partner firm, armed and restored in the same ledger entry, on the same route (expect 403); R3 the Dev-type non-internal caller the CTO half names (or none if the half holds branch (iii)); R4 read ONLY the log events written after the apply: count, JWT-shaped (expect 0), `Bearer` (expect 0). Write all of it to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-aa-4.dev-fence-exercise.txt`. Final lines, exact form: `internal=<code>`, `partner=<code>`, `dev-nonint=<code or NOT-RUN>`, `POST-APPLY events=<n> jwt_shaped=<k> bearer=<k>`.
5. Report to 2.0.0_SA_COO~C through 0.0.0_AB_MSTR: the pin, CodeSha256 before and after, the plan counts, the PRE-1 counts, the ledger entry, the codes and the post-apply counts.
</the_act>

<bounds>
- One Lambda's code only. No IAM, API Gateway, authorizer, log-group, retention or table change; no user record edited except an arming the CTO half names (restored byte for byte in the same entry). No `update-function-code`. No `terraform apply` except through `safe-apply`. A plan that moves anything but the one resource is a STOP. No credential minted; no token or cookie VALUE printed or stored, anywhere.
</bounds>

<proof_of_spec>
<criterion id="CTaa4-AC1" cell_refs="CT-aa-4"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-aa-4.dev-fence-exercise.txt</invocation><expect>jwt_shaped=0 bearer=0</expect></criterion>
<criterion id="CTaa4-AC2" cell_refs="CT-aa-4"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-aa-4.dev-fence-exercise.txt</invocation><expect>partner=403</expect></criterion>
</proof_of_spec>
<expected_criteria>CTaa4-AC1,CTaa4-AC2</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-aa-4.data-proxy-fence-admits-dev-apply-and-exercise.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTaa4-AC1,CTaa4-AC2`, and leave the status flip to the issuer.

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
comp-iam: RUN at step 1 -- denominator one function; the seat's own apply grant on the one root; BLIND to the readers of the user table.
comp-adversary: RUN -- a Dev row on a partner firm admitted by the clause (PRE-1(d) STOPs above 0); a partner caller admitted (R2 expects 403 and rolls back on 200); a token or cookie value copied into a report (counts and codes only); BLIND: Dev logins created after the apply, and whether the live authorizer sets userType for every Dev login (R3 measures one).
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, the one Terraform root and the surprise channel.
</preflight>

Source: CTO msg 108579 and PRD v0.26; the CT-w-10 shape (record CTO_RULING_NFRA_CTLPLN_S9110...).
</task_order>
