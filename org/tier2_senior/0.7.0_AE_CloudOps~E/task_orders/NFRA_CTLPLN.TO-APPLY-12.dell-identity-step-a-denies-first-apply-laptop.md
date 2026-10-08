<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-12.dell-identity-step-a-denies-first-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~E</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.round4.md</decomp_doc> (round 4), "The issuer's acts after the drain": a further apply leg of cell `CT-a-1` (the Dell identity root; its AMENDMENTS 11 to 13 built this step).
<owned_cells>CT-a-1</owned_cells>
</decomp_ref>

  <objective>
    Apply STEP A of three on the Dell identity root: two managed policies changed in place. It adds three explicit Denies ahead
    of the later steps, and one public parameter read that a dell2 seat has been refused for hours. It runs BEFORE
    NFRA_CTLPLN.TO-APPLY-11 (1.0.0_SA_CTO ruling 106838), which stays on hold until the issuer says so.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`. Trunk @5cff7df18d or later. The issuer planned it read-only at ~08:2xZ
    (exit 2): `Plan: 0 to add, 2 to change, 0 to destroy.` 54 added lines, zero removed.
    The root now has a variable `apply_respol_allow` that defaults to false. DO NOT pass it in this order. With the default, no
    plan of this root contains the resource-policy Allow.
    You read no secret's value and list no queue, bucket or function from AWS beyond what the read-back names.
  </context>

  <the_act>
    The apply runs only when BOTH never-widen halves are SIGNED. ONE go; the issuer's GO names the CTO half.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_A_DENIES_FIRST_20261008.md
    - CTO half: named in the GO message.
    Read both in full first and carry every condition of both.

    THE COMMIT: the shared tree at its HEAD on CLOUD, which must contain 5cff7df18d. Show `git status --porcelain --
    infra/aws/terraform/nfra-ctlpln-identity/` is empty.

    1. Load /cloud-ops. Immediately before the plan, run and record the last line of
       `python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py`
       (expect `undo_denied=181/181 selfsim_ok=9/9 ssm_ok=15/15 routes_ok=5/5 vendor_ok=235/235 all_ok=True`). A failing line
       is a STOP.
    2. BEFORE: save the LIVE default-version documents of `cloudops-dell-agent-create-policy` and
       `cloudops-dell-agent-deploy-policy`, each with SHA-256, and note each policy's current default version id.
    3. Plan, TARGETED at exactly `aws_iam_policy.dell_agent_create` and `aws_iam_policy.dell_agent_deploy`, no `-var`.
       - EXACTLY `0 to add, 2 to change, 0 to destroy`, those two and no other; ZERO removed lines. The create policy gains
         exactly four statements: `SimulateOwnPolicyOnly`, `ReadPublicAmiParameter`, `DenyAuditTrailBucketPolicy`,
         `DenyAgentbusQueuePolicy`. `ReadPublicAmiParameter` is one action, `ssm:GetParameter`, on exactly
         `arn:aws:ssm:us-east-1::parameter/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64` (empty account
         field). `DenyAgentbusQueuePolicy` is exactly three actions (`sqs:AddPermission`, `sqs:RemovePermission`,
         `sqs:SetQueueAttributes`) on exactly four queue ARNs, no wildcard. `DenyAuditTrailBucketPolicy` is 21 `s3` actions on
         the audit bucket and its objects. The deploy policy's `DenyProtectedFunctions` gains exactly four `lambda` actions.
         None of `respol_allow`, `vendor_secrets`, `dell_agent_respol` appears as a resource in the plan -> go to 4.
       - ANY other count, a third resource, a removed line, a fifth statement, a wildcard in a new Deny's resources or in the
         parameter's ARN, an account id inside the parameter's ARN -> apply NOTHING; report the plan as read and stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop, the two saved documents by path and hash with their version ids, both
       halves, and the rollback (set each policy's default version back to the noted id).
    5. ONE apply through `.tools/safe-apply.sh` with the SAME two `-target` flags and no `-var`.
    6. Read-back LIVE with `aws iam simulate-principal-policy` on EACH Dell user, every matched statement named:
       `s3:PutLifecycleConfiguration` and `s3:PutBucketPolicy` on the audit bucket -> refused; `sqs:SetQueueAttributes` on each
       of the four agentbus queues -> refused (name every matched statement: the old Deny policy still matches too);
       `sqs:ReceiveMessage` on the user's OWN queue -> allowed; `sqs:SendMessage` on another box's queue -> allowed;
       `lambda:AddPermission` on one protected function -> refused; `ssm:GetParameter` on the exact ARN -> allowed, on
       `.../al2023-ami-kernel-6.1-x86_64` -> refused; `iam:SimulatePrincipalPolicy` on its own user allowed and on the other
       Dell's user refused (context key `aws:username`). A re-plan with the same two targets reads no changes. Close the entry.
       APPLIED, not EXERCISED, until dell2's own plan reads the parameter.
  </the_act>

  <bounds>
    - These two resources only, one apply, no `-var`. No edit to any `.tf`, policy document or test file.
    - `safe-apply` only. No push of a shared branch. No other root. TO-APPLY-11 stays on hold.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~E/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~E/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's simulation (181 undo arms with controls, the queue receive and send arms identical before and after, six parameter arms) and re-run by the applier immediately before the plan; step 6 repeats the named arms against the LIVE policies with matched statements.
comp-adversary: RUN -- a Deny that breaks the bus (receive and send read-back on the live policies); the Allow riding along (the variable defaults false; the plan-shape check names the three resource stems that must not appear); a wildcard or a wrong account field in the parameter grant (exact-string check at step 3); no way back (documents and version ids saved; the previous policy version is kept by IAM); BLIND: a Dell job in flight that writes one of the seven audit-bucket settings (none is placed there by the register; not swept), and organization policies.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>undo_denied=181/181</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode -target=aws_iam_policy.dell_agent_create -target=aws_iam_policy.dell_agent_deploy; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the pre-plan line; the saved documents'
    paths, hashes and version ids; the plan's count and the statements and actions added per policy; every live simulator arm
    per user with its decision and every matched statement; the re-plan's exit; THE APPLIED TIME in UTC; the seat-gate WARN
    lines the wrapper printed; the ledger entry's path and close; the proof-of-spec instance path and its check result; commit
    hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
