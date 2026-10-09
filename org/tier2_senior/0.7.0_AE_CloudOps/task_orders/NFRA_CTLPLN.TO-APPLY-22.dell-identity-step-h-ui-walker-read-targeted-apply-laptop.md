<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-22.dell-identity-step-h-ui-walker-read-targeted-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-09</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>The apply leg of AMENDMENT 22 (merged @9e17e06278): the Dells may read exactly /opal/ui-walker/password (CTO msg 107538).</decomp_context>
</decomp_ref>

  <objective>
    Apply STEP H as a TARGETED apply: one statement added to `aws_iam_policy.dell_agent_plan_reads`. `0 to add, 1 to change, 0 to destroy`.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`, trunk containing merge 9e17e06278. **dell2's F1 shell window is OPEN** (TO-APPLY-20 leg
    B2, 01:00:23Z): an UNTARGETED plan also changes `aws_iam_policy.dell2_ssm` and would CLOSE it. So THIS ORDER IS TARGETED ONLY. Measured
    by the issuer ~01:1xZ: `-target=aws_iam_policy.dell_agent_plan_reads` -> `0 to add, 1 to change, 0 to destroy`, one statement
    `ReadUiWalkerPassword` added, zero lines removed. Halves: COO
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_H_UI_WALKER_READ_20261009.md`; CTO
    `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_H_UI_WALKER_READ_20261009.md` (@4d7f665001, SIGNED;
    added conditions: the walker login stays disabled; after TO-APPLY-20 leg C2 closes, read an UNTARGETED plan of the root, expect
    0/0/0, and report it to the CTO). YOU READ NO PARAMETER VALUE. Use the shared TF_PLUGIN_CACHE_DIR.
  </context>

  <the_act>
    1. Load /cloud-ops. Save the policy's default version id.
    2. Plan with `-target=aws_iam_policy.dell_agent_plan_reads` ONLY: EXACTLY `0 to add, 1 to change, 0 to destroy`, one statement
       added, none removed, `aws_iam_policy.dell2_ssm` absent from the plan. Anything else -> apply nothing, report.
    3. One NEVER-2 entry (rollback: a targeted re-apply at the merge's first parent).
    4. ONE `.tools/safe-apply.sh` with that targeted plan.
    5. Read-back live (simulation only): both Dells `ssm:GetParameter` on `arn:aws:ssm:us-east-1:313476888478:parameter/opal/ui-walker/password`
       allowed and `ssm:DeleteParameter` on it not allowed; dell2's window STILL OPEN (AWS-RunShellScript + i-0167fd745ad906a66 allowed).
       A targeted re-plan reads no changes. Close the entry. Report the applied time to me, and to dell1 via 0.0.0_AB_MSTR.
  </the_act>

  <bounds>
    - TARGETED only; never an untargeted plan or apply of this root while TO-APPLY-20 is open. No file edit. No value read. No push.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat.
comp-iam: RUN -- denominator 1 policy address, 2 Dell users, 3 live arms per user (Get allowed, Delete not allowed, the open window still open); BLIND to the parameter's value (never read) and to other principals.
comp-adversary: RUN -- closing dell2's open window by an untargeted apply (TARGETED only; dell2_ssm absent from the plan; window read back open); a wider grant (one statement, one action, one exact ARN); a value read (forbidden); BLIND: re-enabling the walker login (a separate decision).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode -target=aws_iam_policy.dell_agent_plan_reads; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C: the targeted plan count and diff; the saved version id; every live arm (including the window still
    open); THE APPLIED TIME in UTC in the subject; the ledger entry; the proof instance (full id) and its check; commit hashes and the
    measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
