<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-27.dell-parity-mdpf-shell-transcripts-key-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>

  <closure>
    COMPLETE (issuer, ~05:4xZ). Identity 1/1/0 applied 2026-10-09T05:39:17Z (dell2_ssm v8; dell1_ssm attachment created); transcripts key 0/1/0
    targeted applied 05:40:13Z. Issuer live read: both Dell users AWS-RunShellScript allowed on i-0167fd745ad906a66 and i-02448edb624a7a7cf,
    AWS-RunPowerShellScript explicitDeny on both; live key policy DellAgentUsersGenerateDataKey for both users with exactly ViaService s3 + the
    bucket ARN context. Re-plans 0/0/0 (applier). Ledger closed (@97439f0662). CTO and both Dells told, with the three CTO conditions.
  </closure>


<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>The apply leg of AMENDMENTS 25-28 (merged @dc5032abde): dell1 = dell2 identical permissions (Andrew-direct ~03:5xZ), both Dells standing shell on mdpf-daily-runner (dell2 IB-pr-383, due 2026-10-12), and kms:GenerateDataKey on the transcripts key for both Dells scoped to S3 via this bucket (NFRA_TRNSPT a17/b17).</decomp_context>
</decomp_ref>

  <objective>
    Two roots, two applies, in this order:
    (1) `infra/aws/terraform/nfra-ctlpln-identity/`, untargeted: `aws_iam_user_policy_attachment.dell1_ssm` created and `aws_iam_policy.dell2_ssm`
        updated in place -- EXACTLY `1 to add, 1 to change, 0 to destroy`.
    (2) `infra/aws/terraform/transcripts/`, TARGETED `-target=aws_kms_key.transcripts` (row S46: the root holds another cell's pending changes):
        `aws_kms_key.transcripts` updated in place, policy only, statement `DellAgentUsersGenerateDataKey` added -- EXACTLY `0 to add, 1 to change, 0 to destroy`.
  </objective>

  <context>
    Trunk containing the merge @dc5032abde. Measured by the issuer ~05:3xZ (read-only, default variables): identity `Plan: 1 to add, 1 to change,
    0 to destroy`; transcripts targeted `Plan: 0 to add, 1 to change, 0 to destroy`, the new statement carrying `kms:ViaService =
    s3.us-east-1.amazonaws.com` and `kms:EncryptionContext:aws:s3:arn = arn:aws:s3:::opal-data-transcripts`. Halves:
    - parity: CTO `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261009_035xZ_DELL1_DELL2_IDENTICAL_PERMISSIONS_AND_LAYOUT.md` @910951a1e0;
      COO `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL1_DELL2_IDENTICAL_20261009.md`;
    - the key: CTO addendum @8fc644a586 (msg 107696); COO addendum 1 of `NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL2_SHELL_PARITY_20261009.md`;
    - mdpf-daily-runner: dell2's pair (COO @8323d3fb19, CTO @f0a2f049f7) and the laptop CTO's YES (msg 107749 reply; addendum to the parity
      record @cc4ef8a7ed), given knowing row S48 (a shell there runs as mdpf-daily-runner-ec2-role, which assumes the 49 Financial source principal).
    THE CONDITIONS THAT RIDE WITH THIS GRANT (the CTO's addendum, restated; each Dell seat is told them with the applied time):
      (1) a send that writes a firm data bucket, or assumes the 49F principal outside the runner's own documented job, tells the laptop FIRST;
      (2) every send to mdpf-daily-runner is reported after the fact, with command id and purpose;
      (3) 49 Financial data is never written into another firm's tree.
    The step-C before-rule also stands for the state bucket.
    YOU SEND NO SSM COMMAND AND READ NO SECRET OR OBJECT VALUE. Use the shared TF_PLUGIN_CACHE_DIR; delete your scratch dirs at close.
  </context>

  <the_act>
    1. Load /cloud-ops. Save `aws_iam_policy.dell2_ssm`'s default version id and the transcripts key policy (get-key-policy, saved to your deliverables).
    2. Read BEFORE, for both Dell users: ssm:SendCommand AWS-RunShellScript on `i-0167fd745ad906a66` and on `i-02448edb624a7a7cf`; AWS-RunPowerShellScript
       on each; the transcripts key GenerateDataKey (from the saved key policy: dell users absent from any GenerateDataKey statement).
    3. One NEVER-2 entry naming both roots (rollback: re-apply each root at the merge's first parent; the key policy also restorable from the saved file).
    4. Identity: plan untargeted; EXACTLY 1/1/0 on the two addresses above, or apply nothing and report. ONE safe-apply.
    5. Transcripts: plan `-target=aws_kms_key.transcripts`; EXACTLY 0/1/0 on that address, policy only, or apply nothing and report. ONE safe-apply.
    6. Read AFTER, both users: AWS-RunShellScript allowed on both hosts; PowerShell explicitDeny on both; the live key policy carries
       `DellAgentUsersGenerateDataKey` for both users with exactly the two conditions (compare principals as a SET, row S47).
       Identity re-plan `No changes`; transcripts targeted re-plan `No changes`. Close the entry. Report the applied times to me and to dell1
       and dell2 via 0.0.0_AB_MSTR at once, with the three conditions above.
  </the_act>

  <bounds>
    - These two roots, these three addresses. No edit to any file. `safe-apply` only. No SSM command sent. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat.
comp-iam: RUN -- denominator 3 addresses in 2 roots, 2 Dell users, 2 hosts x 2 documents + 1 key action per user; BLIND to the hosts' own role reach (row S48) and to key grants outside the key policy.
comp-adversary: RUN -- a wider plan (exact counts per root; transcripts targeted so another cell's pending changes do not ride); a key-policy principal-order false diff (set compare, S47); dell2 access gap (attachment create, policy in place, nothing destroyed); BLIND: Dell sends (reported after the fact; step-C before-rule).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C (and the applied time to dell2 V2 via 0.0.0_AB_MSTR at once): the plan count and the one ARN; the saved
    version id; the live arms; THE APPLIED TIME in UTC in the subject; the ledger entry; the proof instance (full id) and its check; commit
    hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
