<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-26.dell2-shell-parity-standing-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>

  <closure>
    COMPLETE (issuer, ~04:0xZ). Applied 2026-10-09T03:52:21Z (dell2_ssm v7, plan 0/1/0). Issuer live read: dell2 ssm:SendCommand
    AWS-RunShellScript allowed, i-0167fd745ad906a66 allowed, AWS-RunPowerShellScript explicitDeny; dell1 unchanged (shell doc allowed
    via the group Allow, resident host implicitDeny -- the gap AMENDMENT 26 closes). Ledgers closed (@8d42d8967a); TO-APPLY-25 C2 SUPERSEDED.
  </closure>

<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>The apply leg of AMENDMENT 24 (merged @7dfcfb686a): dell2 shell parity with dell1, standing, on Andrew-direct ~02:5xZ ("the DELLS should not be waiting on us for this function, let's adjust their permissions accordingly"). Replaces the open F1 window of TO-APPLY-25 (never re-closed).</decomp_context>
</decomp_ref>

  <objective>
    `aws_iam_policy.dell2_ssm` takes the policy file as built at the merge: `AWS-RunShellScript` joins
    `SendResidentDocumentsToResidentHost` (resident host `i-0167fd745ad906a66`), leaves `DenyShellDocuments`, and
    `DenyStartSessionOnShellScriptDocument` is added; the two window statements leave. `0 to add, 1 to change, 0 to destroy`.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`, trunk containing the AMENDMENT 24 merge @7dfcfb686a. Measured by the issuer ~03:4xZ
    (read-only, untargeted, default variables -- the window variable no longer exists): `Plan: 0 to add, 1 to change, 0 to destroy`, only
    `aws_iam_policy.dell2_ssm`. Halves: CTO `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261009_025xZ_DELLS_RUN_THEIR_OWN_SCRIPTS_NO_LAPTOP_WAIT.md`
    @de8b26aa1f (SIGNED); COO `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL2_SHELL_PARITY_20261009.md` @afef73dacf.
    The TO-APPLY-25 ledger's C2 line closes SUPERSEDED by this apply. YOU SEND NO SSM COMMAND. Use the shared TF_PLUGIN_CACHE_DIR and delete
    your Terraform scratch dir at close.
  </context>

  <the_act>
    1. Load /cloud-ops. Save the policy's default version id.
    2. Plan (default variables, untargeted): EXACTLY `0 to add, 1 to change, 0 to destroy` at `aws_iam_policy.dell2_ssm`, the shell
       document added to the resident Allow and removed from the Deny, the two window statements removed. Anything else -> apply nothing, report.
    3. One NEVER-2 entry (rollback: re-apply at the merge's first parent, which re-opens the window state that is live now).
    4. ONE `.tools/safe-apply.sh`.
    5. Read-back live (simulation only), cloudops-dell2-agent-user `ssm:SendCommand`: `AWS-RunShellScript` allowed and
       `i-0167fd745ad906a66` allowed; `AWS-RunPowerShellScript` explicitDeny; `irpt-export-render-run` explicitDeny. `ssm:StartSession` on
       `AWS-RunShellScript` explicitDeny. cloudops-dell1-agent-user's same four arms unchanged from before the apply (read them first).
       Re-plan reads no changes. Close the entry, and close the TO-APPLY-25 ledger's C2 line SUPERSEDED. Report the applied time to me
       and to dell2 via 0.0.0_AB_MSTR at once.
  </the_act>

  <bounds>
    - This root, this one address. No edit to any file. `safe-apply` only. No SSM command sent. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one apply by a seat.
comp-iam: RUN -- denominator 1 policy address, 2 Dell users, 5 arms each (shell doc, resident host, PowerShell doc, export render doc, StartSession); BLIND to the hosts' own role reach.
comp-adversary: RUN -- a wider grant (exact 0/1/0; other shell documents and StartSession explicitDeny); dell1 moved (its arms read before and after); BLIND: dell2's sends (reported after the fact, step D2 condition 2).
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
