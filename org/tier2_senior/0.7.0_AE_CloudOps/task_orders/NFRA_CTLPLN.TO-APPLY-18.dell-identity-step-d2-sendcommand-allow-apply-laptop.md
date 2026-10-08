<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-18.dell-identity-step-d2-sendcommand-allow-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>pending</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc> (workstream ACCESS, cell `CT-a-1`), the apply legs of cell D2 (AMENDMENT 19).
<owned_cells>CT-a-1</owned_cells>
</decomp_ref>

  <objective>
    LEG A: apply the group SendCommand Allow (window CLOSED). LEG B and LEG C: open and close dell2's F1 shell window on dell2's
    svc-irpt ledger legs (with TO-APPLY-15 / TO-APPLY-16).
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`, trunk containing merge 52ca9d65b1. Measured by the issuer ~19:3xZ: default
    `2 to add, 0 to change, 0 to destroy`; with the window `2 to add, 1 to change, 0 to destroy`. Halves: COO
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_D2_SENDCOMMAND_AND_F1_SHELL_WINDOW_20261008.md`;
    CTO `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_D2_SENDCOMMAND_AND_F1_SHELL_WINDOW_20261008.md`
    (@ac2c6e852d, SIGNED). YOU SEND NO COMMAND: read-back by simulation only. The applied-time note to dell2 and dell1 (via
    0.0.0_AB_MSTR) carries the CTO's rule verbatim: "a Dell reports EVERY send to one of the 6 hosts after the fact, by bus
    (document, host, purpose); a send that writes a firm data bucket or the state bucket stays under the step-C before-rule."
  </context>

  <the_act>
    LEG A (GO after both halves):
    1. Load /cloud-ops; `git status --porcelain -- infra/aws/terraform/nfra-ctlpln-identity/` empty; the simulation's last line
       ends `sendcmd_ok=34/34 shellwin_ok=18/18 routes_freed=114/138 routes_still_refused=24 vendor_ok=245/245 all_ok=True`.
    2. Save the group's attached-policy list.
    3. Plan, default variables: EXACTLY `2 to add, 0 to change, 0 to destroy`, `aws_iam_policy.dell_agent_ssm_send[0]` and
       `aws_iam_group_policy_attachment.dell_agent_ssm_send[0]`; anything else -> apply nothing, report.
    4. NEVER-2 entry (rollback: re-apply at the merge's first parent, or detach and delete the one policy).
    5. ONE `.tools/safe-apply.sh`.
    6. Read-back per the COO half's condition 2; the group list (seven); re-plan no changes. Close the entry.

    LEG B -- WINDOW OPEN (GO from the issuer when dell2 ASKS FOR SEND (1) -- `pre_read.sh` to `i-0167fd745ad906a66` -- NOT at V1;
    CTO msg 107187; the svc-irpt secret window TO-APPLY-15/16 stays V1 to X1): plan and apply with
    `-var open_dell2_f1_shell_window=true`: EXACTLY `0 to add, 1 to change, 0 to destroy` on `aws_iam_policy.dell2_ssm`. Read back:
    dell2 `AWS-RunShellScript` + `i-0167fd745ad906a66` allowed; dell2 + `i-0643a5bee8a8feabf` explicitDeny. NEVER-2 entry.

    LEG C -- WINDOW CLOSE (GO when dell2 calls X1; or at 2026-10-09T06:00Z WITHOUT waiting, as TO-APPLY-16): a plain plan and
    apply: EXACTLY `0 to add, 1 to change, 0 to destroy` on `aws_iam_policy.dell2_ssm`. Read back: dell2 `AWS-RunShellScript` +
    `i-0167fd745ad906a66` explicitDeny (`DenyShellDocuments`). Close the entry. Report.
  </the_act>

  <bounds>
    - This root only. No edit to any file. `safe-apply` only. No SSM command sent. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE applies by a seat on GOs; leg C carries a clock deadline.
comp-iam: RUN at the cut by the cell's simulation (sendcmd 34/34, shellwin 18/18) and by the applier before each plan; read-back live per leg.
comp-adversary: RUN -- the window opened by leg A (default closed; exact 2/0/0); a wider send (19 exact ARNs, no wildcard; refused arms live); the window left open (leg C on X1 or 06:00Z without waiting); BLIND: free-text document parameters as a shell route (row S28), a Dell's own sends.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>sendcmd_ok=34/34 shellwin_ok=18/18</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report per leg to 2.0.0_SA_COO~C (and the applied time to dell2 via 0.0.0_AB_MSTR): the plan count; every live arm with
    decision and matched statement; THE APPLIED TIME in UTC in the subject; the ledger path and close; the proof instance named
    with this order's full id and its check (after leg A); commit hashes and the measured push state. Leave the status flip to the
    issuer.
  </report>
</task_order>
