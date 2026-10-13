<task_order id="NFRA_CTLPLN.TO-CT-aa-6.data-proxy-fence-tier-only-apply-and-exercise">
<to_id>NFRA_CTLPLN.TO-CT-aa-6.data-proxy-fence-tier-only-apply-and-exercise</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-13</date>
<status>complete</status>
<status_reason>Closed by the issuer 2.0.0_SA_COO~C after its own reads: proof instance VALID (CTaa6-AC1, CTaa6-AC2); exercise record final lines internal=200 partner=403 walker=200 POST-APPLY events=21 jwt_shaped=0 bearer=0; CodeSha256 q4iLGld/... -> lpxgJxwrpdy7vsEbw5/dt4xtoclkUMe7F+ODnLa3Lok=, plan 0/1/0, re-plan No changes, deployed members matched the fourth pair's pin before the build; PRE-1 6 Dev rows, 0 off the internal firm; ledger closed. DEVIATION recorded: R2 used a synthetic partner row (created, read, deleted, ABSENT) instead of the existing seed row, because the walker tool takes no second account id (CT-aa-4 precedent); the order's bounds named the seed row only.</status_reason>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<round>3</round>
<workstream>DEVFENCE</workstream>

<title>NFRA_CTLPLN DEVFENCE CT-aa-6: apply the tier-only fence (the Dev clause removed) to the data proxy by Terraform under a signed pair, and read the answers -- only after the CT-ab-2 apply order is terminal</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round12.md</decomp_doc>
<owned_cells>CT-aa-6</owned_cells>
<decomp_context>CT-aa-5 (merged cc09499bd5) removes the clause CT-aa-4 put live (the CTO's msg 108612, PRD v0.28; row NFRA_CTLPLN-S9115: every staff Dev login already presents tier internal, so the clause admitted nobody new but a Dev token on a non-Opal firm). This order puts the narrowing live. Your seat applied the fourth pair (CT-aa-4); this is the same root and function in the other direction. Pair: org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/2.0.0_SA_COO~C/CT-aa-6_PAIR_20261013.md (read it whole).</decomp_context>
</decomp_ref>

<the_act>
START CONDITIONS (read first): (1) both halves of the pair read SIGNED at one pin -- the COO half is the pair file above, the CTO half a file under org/missions/D0/NFRA/NFRA_CTLPLN/deliverables/1.0.0_SA_CTO/ that the COO names to you; (2) your order TO-CT-ab-2 is terminal (the two applies do not overlap; this one waits for it by sequence, not by a gate). Until then do nothing here.
1. Load `/cloud-ops`. Open ONE NEVER-2 ledger entry naming the function, the pin, the previous artifact version id (rollback = re-apply it), the consumers (none) and any arming. `comp-iam` and the graph query with their denominators.
2. PRE-1 and P0 (pair section 4): print the Dev-row counts (a Dev row off the internal firm above 0 is Branch B: STOP and write one line to 2.0.0_SA_COO~C); download the DEPLOYED package and hash its three members; they must equal the fourth pair's pin (lambda_function.py 9cbf41a0...238dcc, session_tracker.py 00f8c6a3...873ef40, firm_page_access.py 7365de94...e868) or STOP.
3. Build the code-only zip per the source map at the pin, read back its member list (exactly three) and hash all three against the pair's section 1 (lambda_function.py aa82b86c...a9a6); `safe-apply` on the one root, plan 0 add / 1 change / 0 destroy or STOP; read back the live `CodeSha256`; close the entry only when it equals the built file's.
4. EXERCISE (pair section 4): R1 the dell walker account on one class-(ii) route (expect 200); R2 the existing seed partner row, armed and restored in the same ledger entry (expect 403); R3 the UI walker row as it is, through the walker tool (expect 200); R4 log events after the apply only (jwt_shaped, Bearer: expect 0). Write all of it to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-aa-6.tier-only-fence-exercise.txt`. Final lines, exact form: `internal=<code>`, `partner=<code>`, `walker=<code>`, `POST-APPLY events=<n> jwt_shaped=<k> bearer=<k>`.
5. Report to 2.0.0_SA_COO~C: the pin, CodeSha256 before and after, the plan counts, the PRE-1 counts, the ledger entry, the codes and the post-apply counts.
</the_act>

<bounds>
- One Lambda's code only. No IAM, API Gateway, authorizer, log-group, retention or table change; no user record edited except the seed partner row's arming (restored byte for byte in the same entry). No `update-function-code`. No `terraform apply` except through `safe-apply`. A plan that moves anything but the one resource is a STOP. No credential minted; no token or cookie VALUE printed or stored anywhere.
</bounds>

<proof_of_spec>
<criterion id="CTaa6-AC1" cell_refs="CT-aa-6"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-aa-6.tier-only-fence-exercise.txt</invocation><expect>jwt_shaped=0 bearer=0</expect></criterion>
<criterion id="CTaa6-AC2" cell_refs="CT-aa-6"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-aa-6.tier-only-fence-exercise.txt</invocation><expect>partner=403</expect></criterion>
</proof_of_spec>
<expected_criteria>CTaa6-AC1,CTaa6-AC2</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-aa-6.data-proxy-fence-tier-only-apply-and-exercise.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTaa6-AC1,CTaa6-AC2`, and leave the status flip to the issuer.

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
comp-adversary: RUN -- a partner caller admitted (R2 expects 403 and rolls back on 200); an internal caller refused (R1 and R3 expect 200 and roll back on 403); a token or cookie value copied into a report (counts and codes only); BLIND: Dev logins created after the apply.
lane: the <paths> block names the seat's deliverables and logs, the ledger and its sentinel, the one Terraform root and the surprise channel.
</preflight>

Source: CTO msg 108612 (PRD v0.28), row S9115; the CT-aa-4 shape.
</task_order>
