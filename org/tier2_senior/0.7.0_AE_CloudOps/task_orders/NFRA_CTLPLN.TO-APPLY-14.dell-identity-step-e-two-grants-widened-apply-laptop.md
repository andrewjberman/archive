<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-14.dell-identity-step-e-two-grants-widened-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc> (workstream ACCESS, where cell `CT-a-1` is defined), the issuer's acts after the drain: the apply leg of cell `CT-a-1` cell 2 (AMENDMENTS 16 and 17 built it).
<owned_cells>CT-a-1</owned_cells>
</decomp_ref>

  <closure>
    COMPLETE (issuer, 2026-10-08 ~18:1xZ). APPLIED 2026-10-08T18:00:17Z by 0.7.0_AE_CloudOps, exactly 2/3/0, re-plan exit 0,
    ledger closed; report org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_CTLPLN.TO-APPLY-14.step-e-report.md
    (commits 4522e616b7, 41361dfefe). Issuer read-back, live, ~18:1xZ: the Dell group holds seven managed policies incl.
    cloudops-dell-agent-platform-secrets-policy; secretsmanager:GetSecretValue on opal/mcp/graph-read-token = allowed and
    cloudtrail:StopLogging = explicitDeny, for dell1 and dell2. APPLIED, not EXERCISED: graph F1 waits on one comp-kuzu
    query on each Dell.
    EXERCISED (issuer, 2026-10-09 ~06:1xZ; 4.0.0_SA_CRO GRAPH_COHERENCE_LOOSE_ENDS_20261009.md row 2): each Dell ran
    comp-kuzu "MATCH (n:CloudNode) RETURN count(*)" at 06:1xZ, relayed by 0.0.0_AB_MSTR msg 107771 -- dell1 (0.0.0_AB_MSTR~DELL1) and dell2
    (as cloudops-dell2-agent-user) each COUNT_STAR() = 29700, no refusal, the same VINTAGE: "Built from the estate as of 2026-10-09 06:01:04
    UTC ... manifest=694d3ea6b5dc".
  </closure>

  <objective>
    Apply STEP E on the Dell identity root: the two grants widened (Andrew-direct ~13:2xZ "WIDEN THE TWO GRANTS, YES").
    One new policy (the 28 platform-key secrets read, the graph read token among them) and its group attachment created;
    three policies changed in place. Steps A, B, C are applied.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`. The commit is the CLOUD trunk containing the merge of branch
    `wk-NFRA_CTLPLN-16`; the issuer's GO names that hash. The issuer planned it read-only at ~17:2xZ on the branch tree,
    untargeted, default variables (exit 2): `Plan: 2 to add, 3 to change, 0 to destroy.` -- 67 added lines, 32 removed;
    28 secret ARNs added; zero `"iam:` added; zero `secretsmanager:PutResourcePolicy`/`DeleteResourcePolicy` added.
    `apply_respol_allow` defaults to true: a plain plan keeps the step-C Allow. YOU READ NO SECRET VALUE AND MAKE NO
    RESOURCE-POLICY CALL YOURSELF: read-back by simulation only.
  </context>

  <the_act>
    The apply runs only when BOTH never-widen halves are SIGNED. ONE go; the issuer's GO names the CTO half and the trunk hash.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_E_TWO_GRANTS_WIDENED_20261008.md (@9a8758bddf)
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_E_TWO_GRANTS_WIDENED_20261008.md (@ee3578d886)
    Read both in full first and carry every condition of both. The CTO half's condition 2 (both Dell fabric managers told the
    extended before-rule) is the issuer's: the GO is sent only after 0.0.0_AB_MSTR confirms that relay.

    THE COMMIT: the shared tree at its HEAD on CLOUD, which must contain the hash in the GO. Show `git status --porcelain --
    infra/aws/terraform/nfra-ctlpln-identity/` is empty.

    1. Load /cloud-ops. Immediately before the plan, run and record the last line of
       `python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py`
       (expect `freed_allowed=72/72 freed_excluded=3 undo_freed=167/167 undo_still_denied=443 selfsim_ok=9/9 ssm_ok=15/15 routes_ok=5/5 vendor_ok=245/245 all_ok=True`).
       A failing line is a STOP.
    2. BEFORE: save the Dell agent group's attached-policy list, and the current DEFAULT VERSION id of each of
       `cloudops-dell-agent-deploy-policy`, `cloudops-dell-agent-create-policy`, `cloudops-dell-agent-respol-allow-policy`.
    3. Plan (no -target, no -var):
       - EXACTLY `2 to add, 3 to change, 0 to destroy`: created `aws_iam_policy.dell_agent_platform_secrets[0]` and
         `aws_iam_group_policy_attachment.dell_agent_platform_secrets[0]`; changed in place `aws_iam_policy.dell_agent_deploy`,
         `aws_iam_policy.dell_agent_create`, `aws_iam_policy.dell_agent_respol_allow[0]`; no other address. In the ADDED
         lines: `arn:aws:secretsmanager` 28 times; `"iam:` zero; `secretsmanager:PutResourcePolicy` and
         `secretsmanager:DeleteResourcePolicy` zero (record each count) -> go to 4.
       - ANY other count, any destroy, any change to `aws_iam_policy.dell_agent_vendor_secrets[0]` or a routes resource, or a
         grep count other than above -> apply NOTHING; report the plan as read and stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop, the saved attached-policy list, the three version ids, both halves, and
       the rollback (re-apply the root at the merge's first parent; or detach and delete the new policy and set each changed
       policy's default version back to the saved id).
    5. ONE apply through `.tools/safe-apply.sh`, the same plan shape.
    6. Read-back LIVE with `aws iam simulate-principal-policy` on EACH Dell user, every matched statement named. ALLOWED:
       `secretsmanager:GetSecretValue` on the ARN of `opal/mcp/graph-read-token`; `cloudtrail:PutResourcePolicy`;
       `s3:PutBucketPolicy` on `arn:aws:s3:::opal-cloudtrail-logs-313476888478`; `lambda:AddPermission` on one of the ten
       protected functions; `sqs:SetQueueAttributes` on one agentbus queue. REFUSED: `cloudtrail:StopLogging`;
       `s3:PutLifecycleConfiguration` on the audit bucket; `lambda:UpdateFunctionCode` on one protected function;
       `secretsmanager:GetSecretValue` on `schwab/sdd/session` and on one OTHER-class secret (take one from
       `infra/aws/terraform/nfra-ctlpln-identity/tests/vendor_secrets_census.json`, decision OTHER); `iam:CreateRole`.
       `sqs:ReceiveMessage` on the user's own queue and `sqs:SendMessage` allowed as before. The group's attached-policy list
       read live (seven expected). A re-plan reads no changes. Close the entry. APPLIED, not EXERCISED, until a Dell's own
       first use (graph F1: one `comp-kuzu` query on dell1 and on dell2).
  </the_act>

  <bounds>
    - This root only, one apply. No edit to any `.tf`, policy document or test file.
    - `safe-apply` only. No push of a shared branch. No secret value read. No resource-policy call on any resource. No other root.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's simulation (72 of 72 freed actions allowed, 167 freed arms allowed, 443 still-denied arms explicitDeny with statement named, vendor 245 of 245) and re-run by the issuer at ~17:2xZ and by the applier immediately before the plan; step 6 repeats the named arms against the LIVE policies.
comp-adversary: RUN -- an IAM or Secrets Manager resource-policy action riding in (grep zero at step 3, iam:CreateRole refused live at step 6); a withheld secret granted (the 28 count at step 3; schwab/sdd/session and an OTHER secret refused live); a Deny that must stay dropped (StopLogging, the bucket's lifecycle, protected-function code refused live); the step-C Allow destroyed (default true; the exact plan shape at step 3 has no destroy); no way back (saved version ids; first-parent re-apply); BLIND: secret values (never read), organization policies, the resource policies already on each resource, and a Dell's own first use (reported by the Dell).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>freed_allowed=72/72 freed_excluded=3 undo_freed=167/167</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the pre-plan line; the plan's count and
    the three grep counts; the three saved version ids; every live simulator arm per user with its decision and matched
    statement; the group's attached-policy list; the re-plan's exit; THE APPLIED TIME in UTC, in the subject line; the
    seat-gate WARN lines the wrapper printed; the ledger entry's path and close; the proof-of-spec instance path and its check
    result; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
