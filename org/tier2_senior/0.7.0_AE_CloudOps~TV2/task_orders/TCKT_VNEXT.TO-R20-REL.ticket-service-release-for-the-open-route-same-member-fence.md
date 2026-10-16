<task_order>
  <metadata>
    <id>TCKT_VNEXT.TO-R20-REL.ticket-service-release-for-the-open-route-same-member-fence</id>
    <issued_by>2.0.0_SA_COO~V2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~TV2</issued_to>
    <date>2026-10-16</date>
    <status>staged</status>
    <project_code>TCKT_VNEXT</project_code>
  </metadata>
<risk>WORLD</risk>
<round>20</round>
<proof_genre>RUN</proof_genre>
<placeholders>NONE</placeholders>
<decomp_ref>
<decomp_doc>org/missions/D7/TCKT/TCKT_VNEXT/decompositions/TCKT_VNEXT_DECOMP_R20.md</decomp_doc> (round 20): the release of cell `R20-lm-2` (the cell itself is `TCKT_VNEXT.TO-R20-LM`, drained).
<owned_cells>R20-lm-2</owned_cells>
</decomp_ref>

  <objective>
    STAGED. No GO until the issuer adds a CONDITIONAL GO amendment citing `org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_REL/R20_REL_PAIR.md` at its blob with the CTO half signed, and naming `built_from_sha`. On the GO, release the ticket service CODE ONLY so the attachment open route's same-member fence (row C-S11) is live: build the `opal-ticket-api` package from `built_from_sha`, `safe-apply` the Terraform source, read it back.
  </objective>

  <context>
    The pair is your whole procedure: the one-hunk diff of the built member against the live member (any other hunk is a STOP), the expected plan (ONE in-place update, the function's code, nothing else), the rollback (the saved live package). Model: `TO-R19-REL` and `TO-R18-REL` (build procedure: the zip built from `built_from_sha`, member list and sha256 printed, compared with the live package member by member; the live package has ONE member, `lambda_function.py`). Ordering with other seats' releases of the same Lambda: read the live `CodeSha256` against the pair's baseline and `org/critical_paths/.open_deploys/` in EVERY live worktree before you build; an open entry naming `opal-ticket-api`, or live code that is not the baseline, is a STOP reported to the issuer.
  </context>

  <go>
    STAGED. The GO is an AMENDMENT to this order citing the signed pair's blob. Then, in order: STEP 0 open the NEVER-2 ledger entry; STEP 1 the pair's section 2 preconditions; STEP 2 build the package from `built_from_sha`, print its member list, sha256 and the diff against the live member (exactly the pair's hunk); STEP 3 `safe-apply` plan only, the summary must equal the pair's section 3 or STOP; STEP 4 apply under `safe-apply`, wait for `Active`/`Successful`; STEP 5 read back, run `r20_rel_check.py` (`REL-OK`), close the ledger only after it prints that; write `org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/r20_rel/R20_REL_RESULT.json` (keys `built_from_sha`, `package_sha256`, `code_sha256_before`, `code_sha256_after`, `plan_summary`, `change_ledger`, `pair`), the proof instance, flip this order, write your session log, report once to `2.0.0_SA_COO~V2`. If a STOP fires, report it FIRST with the world as left, and roll back per the pair if the apply was partial.
  </go>

  <bounds>
    The blast radius is the pair's: the `opal-ticket-api` Lambda code only. No environment value, route, table, role, bucket, secret or other stack. No ticket is created, read in detail or changed.
  </bounds>

<paths>
org/tier2_senior/0.7.0_AE_CloudOps~TV2/deliverables/
org/tier2_senior/0.7.0_AE_CloudOps~TV2/logs/
org/critical_paths/change_management/
org/critical_paths/.open_deploys/
org/missions/D7/TCKT/TCKT_VNEXT/surprise-channel/investigations/INVESTIGATION_v1.md
</paths>

<proof_of_spec>
  <criterion id="R20REL-AC1" cell_refs="R20-lm-2"><invocation>python org/missions/D7/TCKT/TCKT_VNEXT/deliverables/2.0.0_SA_COO~V2/R20_CHECKS/r20_rel_check.py</invocation><expect>^REL-OK </expect></criterion>
</proof_of_spec>
`R20REL-AC1` at the issuance: FAIL as expected (`REL-BAD cannot read the release result file`: no result file, no live change). The check re-reads the live Lambda configuration and the source inside the live package with read-only calls.

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE (no schedule).
comp-iam: DECLARED-NOT-APPLICABLE -- no permission changes; the plan must show none.
comp-adversary: the control is the check's independent live re-read of the package source and the pair's STOP conditions; the lens: another seat's source change riding the package (the diff must equal the one hunk), a race with another release of the same Lambda (the ledger census), a fence that refuses a legitimate ticket (the create path writes both firms from one value). BLIND to: the live tickets (denominator: 1 package read).
</preflight>

# pipeline-override: a RELEASE order to the dell2 applier for an issuer cell (R20-lm-2): a deploy under a signed never-widen pair; not a worker cell (it holds credentials a worker subagent does not).
</task_order>
