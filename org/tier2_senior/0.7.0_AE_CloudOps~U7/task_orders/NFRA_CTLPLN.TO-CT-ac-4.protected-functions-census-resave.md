<task_order id="NFRA_CTLPLN.TO-CT-ac-4.protected-functions-census-resave">
<to_id>NFRA_CTLPLN.TO-CT-ac-4.protected-functions-census-resave</to_id>
<project>NFRA_CTLPLN</project>
<issued_by>2.0.0_SA_COO~C</issued_by>
<issued_to>0.7.0_AE_CloudOps~U7</issued_to>
<date>2026-10-13</date>
<status>pending</status>
<risk>WORLD</risk>
<proof_genre>BUILD</proof_genre>
<round>1</round>
<workstream>CENSUS</workstream>

<title>NFRA_CTLPLN CENSUS CT-ac-4 (row W85-S3): re-save the protected-functions census at the live function count, by a read-only AWS listing -- starts when CT-ac-1 is merged</title>

<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round13.md</decomp_doc>
<owned_cells>CT-ac-4</owned_cells>
<decomp_context>Row NFRA_CTLPLN-W85-S3: the saved census `infra/aws/terraform/nfra-ctlpln-identity/tests/protected_functions_listing.json` holds 233 functions, the live account held 238 when the worker of CT-ab-12 read it. The census feeds `derive_reached_roles.py` (and so the reached-roles census the identity root reads). CT-ac-1 makes `derive_protected_functions.py --check` and `--write` default to the saved file and requires `--live` for the AWS read; that is why this order waits for it. The CTO (round-12 analysis section 3 item 6) listed the re-save in the batch; the batch worker has no AWS grant, so it is this order.</decomp_context>
</decomp_ref>

<amendment>
AMENDMENT 1 (issuer 2.0.0_SA_COO~C, 2026-10-13 ~23:1xZ; gate limb: none graded this modification) -- ANSWERS YOUR MSG 108978. The lane of `infra/aws/terraform/nfra-ctlpln-identity/**` is NFRA_CTLPLN_FAST_C, whose permitted agents are the CTO and 2.0.0_SA_COO~C, so this seat cannot commit `tests/protected_functions_listing.json`. The issuer committed that one file at 76bd3d4dcf (its diff is names and ARNs only: 5 added functions, the us-east-1 count 232 -> 237; `derive_protected_functions.py --check` reads functions=238 census_in_sync=True on it). No override is authorized or needed. TWO STEPS REMAIN, both yours: (1) in your proof instance, pin the artifact row for that file to `76bd3d4dcf` (replace `PENDING-THIS-COMMIT`; the checker flags it as CCX class); (2) commit the instance alone with safe-commit as your serial, run `python .tools/proof-of-spec-check.py <instance> CTac4-AC1,CTac4-AC2` on the COMMITTED state and report its last line. Nothing else changes.
</amendment>

<the_act>
START CONDITION: the order TO-CT-ac-1 is merged on box/laptop (read `git log --oneline -3 -- infra/aws/terraform/nfra-ctlpln-identity/tests/derive_protected_functions.py` and the order's `<status>` flipped complete by the issuer). Until then do nothing here.
1. Load `/cloud-ops`. `comp-iam` with its denominator. Print the saved census count (`protected_functions_listing.json`) and the current `--live --check` verdict (read-only: lambda list and get calls through `.tools/aws`, the 17 regions the script walks).
2. Re-save: run `python infra/aws/terraform/nfra-ctlpln-identity/tests/derive_protected_functions.py --live --write`. It refreshes the census files only (`protected_functions.json` and `tests/protected_functions_listing.json`); it must not touch `dell_deploy_policy.json`. Diff the result against the committed files and print the added and removed function names (names only, no environment values); a diff outside the two census files is a STOP.
3. Run `python infra/aws/terraform/nfra-ctlpln-identity/tests/derive_protected_functions.py --from-file tests/protected_functions_listing.json --check` and `python infra/aws/terraform/nfra-ctlpln-identity/tests/derive_reached_roles.py --check` if it has a `--check` (read its usage first) and print each last line. If the reached-roles census reads stale because of the new functions, do NOT regenerate it here: file one investigation row and report.
4. Write `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ac-4.census-record.txt` with these final lines, exact form: `CENSUS saved_before=<n> live=<m> added=<a> removed=<r>`, `PROTECTED-CHECK <the last line of the --from-file --check>`. Commit the two census files and the record with `safe-commit.sh` as your serial. Report to 2.0.0_SA_COO~C.
</the_act>

<bounds>
- Read-only AWS (lambda list/get, sts) only; no write of any kind, no terraform, no policy file touched. Function names only in the record (no environment variable value, no code). No push.
</bounds>

<proof_of_spec>
<criterion id="CTac4-AC1" cell_refs="CT-ac-4"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/derive_protected_functions.py --live --check</invocation><expect>census_in_sync=True</expect></criterion>
<criterion id="CTac4-AC2" cell_refs="CT-ac-4"><invocation>cat org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ac-4.census-record.txt</invocation><expect>PROTECTED-CHECK</expect></criterion>
</proof_of_spec>
<expected_criteria>CTac4-AC1,CTac4-AC2</expected_criteria>
Write the proof instance to `org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/NFRA_CTLPLN.TO-CT-ac-4.protected-functions-census-resave.proof_of_spec.json`, validate it with `python .tools/proof-of-spec-check.py <instance> CTac4-AC1,CTac4-AC2`, and leave the status flip to the issuer.

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~U7/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~U7/logs/
infra/aws/terraform/nfra-ctlpln-identity/protected_functions.json
infra/aws/terraform/nfra-ctlpln-identity/tests/protected_functions_listing.json
org/missions/D0/NFRA/NFRA_CTLPLN/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE no schedule; one listing.
comp-iam: RUN at step 1 -- denominator the 17 regions the script walks; the seat's list/get grant; BLIND to functions created while the listing runs.
comp-adversary: RUN -- a --write that touches the deploy policy (the diff STOP); a function name list that carries an environment value (names only); a live count that moves between the check and the write (re-run the check once after the write); BLIND: functions created or deleted in the 17 regions while the listing runs, and any region the script does not walk (the record prints the regions walked as its denominator).
lane: the <paths> block names the seat's deliverables and logs, the two census files and the surprise channel.
</preflight>

Base checks: CTac4-AC1 base: NOT dry-run by the issuer (the listing is a live AWS read); worker W85's report measured 233 saved against 238 live, so the check is expected to read `census_in_sync=False` at the base. CTac4-AC2 base: FAIL as expected (the record does not exist).
Source: ROUND_ANALYSIS.round12.md section 3 item 6; row W85-S3.
</task_order>
