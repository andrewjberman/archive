<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-3.dell-policy-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-07</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round3.md</decomp_doc> (round 3), "The issuer's acts after the drain" act 1: the apply leg of cells `CT-c-1`, `CT-c-3` and `CT-c-5`, all three complete as builds.
<owned_cells>CT-c-1,CT-c-3,CT-c-5</owned_cells>
</decomp_ref>
# pipeline-override: the laptop apply leg of NFRA_CTLPLN round 3 (cells CT-c-1, CT-c-3, CT-c-5, complete as builds with VALID proof instances); this is an issuer's post-drain act named in the frozen decomposition, not a new cell; executor and box ruled by 1.0.0_SA_CTO msg 106056 ("a cloud-operations seat 2.0.0_SA_COO~C seats under its own order")

  <objective>
    Apply ONE Terraform root on the laptop so the two Dell machines hold the round-3 policy: they may create, update and tag non-IAM
    resources, still change no access, cannot update ten access-deciding functions, and cannot read API Gateway keys.
    Andrew, verbatim (record org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261007_063xZ_DELLS_CREATE_RESOURCES_NO_IAM_DEPLOYS_NOT_GATED_ON_SITEZ.md):
    "Regarding DELLs, they shouldnt need to create or touch IAMs, they should be allowed to create resources though."
    It is an IAM-changing apply, so the plan's exact shape gates the apply.
  </objective>

  <context>
    The root is `infra/aws/terraform/nfra-ctlpln-identity/`. Round 2 applied its first version at site Z (group, two users, the deploy
    policy, two bus policies). Round 3 changed it in three cells, all merged by `eda2919e6b`, which is on origin CLOUD:
    a new managed policy `cloudops-dell-agent-create-policy` (`dell_create_policy.json`) and its attachment to
    `cloudops-dell-agents-group`; and a new version of `cloudops-dell-agent-deploy-policy` (`dell_deploy_policy.json`) carrying
    `DenyPassRoleExceptNamed`, `DenyProtectedFunctions` (rendered from `protected_functions.json`) and `DenyApiKeyReads`.
    The issuer planned it read-only on the laptop at ~07:5xZ: `aws_iam_group_policy_attachment.dell_agent_create` created,
    `aws_iam_policy.dell_agent_create` created, `aws_iam_policy.dell_agent_deploy` updated in place; 2 to add, 1 to change, 0 to destroy.
    The shared tree's copy of the root already has `.terraform/` initialised against the backend.
    UNMEASURED, and your first real read: whether the laptop's AWS identity holds IAM write on these three objects.
  </context>

  <the_act>
    BOTH never-widen halves are SIGNED and each binds on the plan shape below. There is ONE go and no second message: you grade the
    plan yourself, and the plan's shape decides whether you apply.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_ROUND3_DELL_POLICY_20261007.md (@d3ffdf3)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_ROUND3_DELL_POLICY_APPLY_AT_THE_LAPTOP_20261007.md (@2d27f79524)
    Read both in full first and carry every condition of both.

    THE COMMIT: work in the shared tree at its HEAD on branch CLOUD. Before anything else, show that the root's bytes at HEAD equal
    its bytes at `eda2919e6b`: `git diff --stat eda2919e6b HEAD -- infra/aws/terraform/nfra-ctlpln-identity/` must print nothing, and
    `git status --porcelain -- infra/aws/terraform/nfra-ctlpln-identity/` must show no tracked change. Either one non-empty is a STOP.

    1. Load /cloud-ops. Run the root's checks: `tests/check_identity.py`, `tests/simulate_policy.py`,
       `tests/render_passrole.py --check`, `tests/derive_protected_functions.py --check`. A failing check is a STOP.
    2. Read live, BEFORE: the default version id and document of `cloudops-dell-agent-deploy-policy`; that
       `cloudops-dell-agent-create-policy` does not exist; the policies attached to `cloudops-dell-agents-group`. Save them in your
       deliverables folder: they are the rollback's reference.
    3. Plan the root UNTARGETED with terraform directly (`safe-apply.sh` gates `apply` only; `plan` is called on terraform itself):
       `terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color`.
       - The plan reads EXACTLY `2 to add, 1 to change, 0 to destroy`, and the three addresses are the three the context lists
         -> go to 4.
       - ANY other plan -> apply NOTHING. Report the plan as read to 2.0.0_SA_COO~C and stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop as the box and the rollback per key as the COO half states it.
    5. ONE apply of the root through the wrapper: `.tools/safe-apply.sh -chdir=infra/aws/terraform/nfra-ctlpln-identity apply ...` (read the
       wrapper's header for the halt checkpoint and `HALT_ACK`; an audited halt override is used only if /cloud-ops says this case needs one, and is named in your report).
       - If it is refused for want of IAM write: nothing is half-applied by a refused first call. Close the entry REFUSED, and report
         the refusal line verbatim to 2.0.0_SA_COO~C. Do not retry, and do not look for another identity.
       - If it errors part-way: finish or roll back in-session per the entry, and say which.
    6. Prove it (the criteria below), then: compare both policies' LIVE default-version documents to the repo JSON files (parsed JSON
       equality); read from the LIVE deploy policy document that the four round-2 Deny statements are still there
       (`DenyEveryIamWrite`, `DenyCloudTrailWrites`, `DenyS3DeletesOnProductionData`, `DenyTableAndDatabaseDeletes`); run one
       simulation against the LIVE principal `cloudops-dell1-agent-user` (`iam simulate-principal-policy`) that repeats the arms of
       `tests/simulate_policy.py`'s first and third blocks; run `comp-iam gaps`; close the entry.
  </the_act>

  <bounds>
    - This root only. No other Terraform root, no edit to any file of the root, no IAM write outside step 5's apply.
    - `safe-apply` only; never a bare `terraform apply`. No access key, by any means. No push of a shared branch.
    - No act as a Dell identity, and no test that creates a resource: the live round trip is a later act by another route.
    - A plan that differs from the expected three lines is a STOP with a report.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-c-1"><invocation>.tools/aws iam list-attached-group-policies --group-name cloudops-dell-agents-group --query "sort(AttachedPolicies[].PolicyName)" --output json</invocation><expect>exactly ["cloudops-dell-agent-create-policy", "cloudops-dell-agent-deploy-policy"]</expect></criterion>
  <criterion id="AC2" cell_refs="CT-c-3,CT-c-5"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>POLICY-SIM allowed_ok=22/22 denied_ok=19/19 passrole_ok=5/5 protected_ok=8/8 all_ok=True</expect></criterion>
  <criterion id="AC3" cell_refs="CT-c-1,CT-c-3,CT-c-5"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>after the apply the re-plan reads no changes: exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes (or at a STOP): the plan's counts and addresses; the before and after default
    version ids of the deploy policy; the live-versus-repo document comparison for both policies; the four round-2 Deny statements read
    live; the live-principal simulation's result; `comp-iam gaps`; the ledger entry's path and its close; commit hashes and the
    measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
