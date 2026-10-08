<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-19.dell-identity-step-f-iam-roles-and-plan-reads-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>The apply leg of cell 3 (AMENDMENT 20, merged @db7ecaa46b): item 4 (IAM roles and policies, PassRole) and the Dells' plan reads.</decomp_context>
</decomp_ref>

  <objective>
    Apply STEP F on the Dell identity root: two new group policies (IAM roles/policies + PassRole; read-only plan reads) and their
    attachments; the deploy policy loses DenyEveryIamWrite and DenyPassRoleExceptNamed. After this the Dells apply their own IAM.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`, trunk containing merge db7ecaa46b. Measured by the issuer ~23:1xZ (read-only,
    untargeted, default variables): `Plan: 4 to add, 1 to change, 0 to destroy.` Halves: COO
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_F_IAM_ROLES_AND_PLAN_READS_20261008.md`;
    CTO named in the GO. YOU MAKE NO IAM WRITE YOURSELF beyond the apply; read-back by simulation only.
  </context>

  <the_act>
    1. Load /cloud-ops. `git status --porcelain -- infra/aws/terraform/nfra-ctlpln-identity/` empty; the simulation's last line contains
       `iamw_ok=225/225 planread_ok=422/422` and ends `all_ok=True`. A failing line is a STOP.
    2. Save the group's attached-policy list and `cloudops-dell-agent-deploy-policy`'s default version id.
    3. Plan (default variables): EXACTLY `4 to add, 1 to change, 0 to destroy`, the five addresses the COO half lists. In the plan:
       `ssm:PutParameter` added 0, `secretsmanager:` added 0. Anything else -> apply nothing, report.
    4. One NEVER-2 entry (rollback: re-apply the root at the merge's first parent).
    5. ONE `.tools/safe-apply.sh`.
    6. Read-back live per the COO half's condition 3 (both Dells, matched statement named); the group's attached list (nine); re-plan
       no changes. Close the entry. Report the applied time to me, and to both Dells via 0.0.0_AB_MSTR.
  </the_act>

  <bounds>
    - This root only, one apply. No edit to any file. `safe-apply` only. No IAM write of your own. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat.
comp-iam: RUN at the cut by the cell's simulation (iamw 225/225, planread 422/422) and by the applier before the plan; live read-back per the COO half.
comp-adversary: RUN -- a parameter or secret write riding in (greps at step 3); a wider plan (exact 4/1/0); user/key creation (the narrow Deny, refused live); BLIND: what a Dell does with IAM write afterwards (its own acts; the COO half states it can make itself an administrator); the held portal-auth read (row W14-S31); PutParameter already allowed (row W14-S32).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>iamw_ok=225/225 planread_ok=422/422</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C: the pre-plan line; the plan count and greps; the saved list and version id; every live arm with
    decision and matched statement; the group list; THE APPLIED TIME in UTC in the subject; the ledger path and close; the proof
    instance (full id) and its check; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
