<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-13.dell-identity-step-c-resource-policy-allow-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc> (workstream ACCESS, where cell `CT-a-1` is defined), the issuer's acts after the drain: the last apply leg of cell `CT-a-1` (the Dell identity root; its AMENDMENTS 10, 12 and 13 built this step).
<owned_cells>CT-a-1</owned_cells>
</decomp_ref>

  <objective>
    Apply STEP C, the last of three on the Dell identity root: create one Allow policy of 70 resource-policy actions and attach
    it to the Dell agent group. Steps A and B are applied (09:19:39Z and 11:33:48Z).
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`. Trunk @203344e1b1 or later. The Allow sits behind the variable
    `apply_respol_allow`, default false. THIS ORDER PASSES `-var apply_respol_allow=true` ON BOTH THE PLAN AND THE APPLY; it is
    the only order that does. The issuer planned it read-only at ~12:1xZ (exit 2): `Plan: 2 to add, 0 to change, 0 to
    destroy.` 100 added lines, zero removed, 70 actions. Without the variable the root reads "No changes" (measured).
    YOU MAKE NO RESOURCE-POLICY CALL YOURSELF (no put-bucket-policy, put-key-policy, add-permission, set-queue-attributes, on
    anything): the read-back is by simulation only.
  </context>

  <the_act>
    The apply runs only when BOTH never-widen halves are SIGNED. ONE go; the issuer's GO names the CTO half.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_C_RESOURCE_POLICY_ALLOW_20261008.md
    - CTO half: named in the GO message.
    Read both in full first and carry every condition of both.

    THE COMMIT: the shared tree at its HEAD on CLOUD, which must contain 203344e1b1. Show `git status --porcelain --
    infra/aws/terraform/nfra-ctlpln-identity/` is empty.

    1. Load /cloud-ops. Immediately before the plan, run and record the last line of
       `python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py`
       (expect `freed_allowed=70/70 freed_excluded=5 undo_denied=181/181 selfsim_ok=9/9 ssm_ok=15/15 routes_ok=5/5 vendor_ok=235/235 all_ok=True`).
       A failing line is a STOP.
    2. BEFORE: first plan WITHOUT the variable and record that it reads no changes (exit 0): this proves steps A and B are as
       applied. Any change there is a STOP. Save the Dell agent group's attached-policy list.
    3. Plan WITH `-var apply_respol_allow=true`.
       - EXACTLY `2 to add, 0 to change, 0 to destroy`: `aws_iam_policy.dell_agent_respol_allow[0]` and
         `aws_iam_group_policy_attachment.dell_agent_respol_allow[0]`, no other; ZERO removed lines; ONE statement, Effect
         Allow, exactly 70 actions (count them in the plan); a grep of the plan for each of `"iam:`, `"secretsmanager:`,
         `"cloudtrail:` reads ZERO (record each) -> go to 4.
       - ANY other count, a third resource, any change to an existing policy, an action count other than 70, any `iam:`,
         `secretsmanager:` or `cloudtrail:` action -> apply NOTHING; report the plan as read and stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop, the saved attached-policy list, both halves, and the rollback (apply
       the root again WITHOUT the variable; or detach and delete the one policy).
    5. ONE apply through `.tools/safe-apply.sh` WITH `-var apply_respol_allow=true`. If the wrapper does not pass a `-var`
       through to terraform, STOP before applying and report how it takes one: do not work around the wrapper.
    6. Read-back LIVE with `aws iam simulate-principal-policy` on EACH Dell user, every matched statement named. ALLOWED:
       `s3:PutBucketPolicy` on `arn:aws:s3:::opal-data-assets`; `lambda:AddPermission` on a function that is NOT one of the
       ten protected; `kms:PutKeyPolicy` on a key ARN of this account. REFUSED: `lambda:AddPermission` on one protected
       function; `s3:PutBucketPolicy` and `s3:PutLifecycleConfiguration` on the audit-trail bucket; `sqs:SetQueueAttributes`
       on one agentbus queue; `secretsmanager:PutResourcePolicy` on the ARN of `opal/auth/jwt-private-key`;
       `iam:UpdateAssumeRolePolicy` on a role; one routes arm as before. `sqs:ReceiveMessage` on the user's own queue and
       `sqs:SendMessage` allowed as before. The group's attached-policy list read live (six expected). A re-plan WITH the
       variable reads no changes. Close the entry. APPLIED, not EXERCISED, until a Dell's own first use.
  </the_act>

  <bounds>
    - This root only, one apply, with the variable. No edit to any `.tf`, policy document or test file.
    - `safe-apply` only. No push of a shared branch. No resource-policy call on any resource. No other root.
    - FIRST LINE OF YOUR REPORT, verbatim: "Until the variable's default is made true in the root, any plan or apply of
      nfra-ctlpln-identity WITHOUT -var apply_respol_allow=true will plan to DESTROY the Allow." The issuer cuts that change
      next; do not make it yourself.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's simulation (70 of 70 freed actions allowed on representative resources, five excluded reading their stated decision, 181 undo arms with controls, the queue receive and send arms unchanged) and re-run by the applier immediately before the plan; step 6 repeats the named arms against the LIVE policies with matched statements.
comp-adversary: RUN -- an IAM, Secrets Manager or trail action riding in the Allow (three zero-hit greps and the 70 count at step 3; three live refused arms at step 6); the three ruled Denies not live (the no-variable plan at step 2 reads no changes; live refused arms); the applier exercising the grant (forbidden in context and bounds); the Allow destroyed by the next plain plan (the report's first line; the issuer's next cell); no way back (one apply without the variable); BLIND: the resource policies already on each resource, organization policies, and a real resource-policy change by a Dell (its own act, reported).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>freed_allowed=70/70 freed_excluded=5 undo_denied=181/181</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode -var apply_respol_allow=true; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the first line the bounds require; the
    pre-plan line; the no-variable plan's exit; the with-variable plan's count, the action count and the three grep counts;
    every live simulator arm per user with its decision and every matched statement; the group's attached-policy list; the
    re-plan's exit; THE APPLIED TIME in UTC, in the subject line; the seat-gate WARN lines the wrapper printed; the ledger
    entry's path and close; the proof-of-spec instance path and its check result with every artifact row pinned to the commit
    that carried it; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
