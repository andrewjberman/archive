<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-20.dell2-f1-shell-window-reopen-st26-ledger-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>A second use of the dell2 F1 shell window built by AMENDMENT 19 (variable open_dell2_f1_shell_window), for dell2's new ledger irpt-ycdgen-f1-st26-20261008 (the st26 resident release carrying the brand asset; dell2 2.0.0_SA_COO~G2 msg 1901, relay 107454). 1.0.0_SA_CTO msg 107457: "consented: dell2's F1 shell window REOPEN for its new ledger, same terms, hard close 06:00Z".</decomp_context>
</decomp_ref>

  <closure>
    COMPLETE (issuer, ~01:5xZ). B2 OPEN 2026-10-09T01:00:23Z on dell2's "open now"; C2 CLOSED 01:43:20Z on dell2's X1. Issuer live read
    after C2: dell2 AWS-RunShellScript explicitDeny (combined send refused). Untargeted re-plan 0/0/0 (applier). Ledger closed (@bdc7f6e9b7).
  </closure>

  <objective>
    Open dell2's F1 shell window again when dell2 says "open now" (LEG B2) and close it at dell2's X1 or at 2026-10-09T06:00Z
    WITHOUT waiting (LEG C2) -- exactly the plans of NFRA_CTLPLN.TO-APPLY-18 legs B and C.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`. Halves: the step D2 pair (COO
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_D2_SENDCOMMAND_AND_F1_SHELL_WINDOW_20261008.md`,
    CTO @ac2c6e852d) with the CTO's consent to this reuse (msg 107457). Same send-report rule: dell2 reports every send after the fact.
    NOTE: TO-APPLY-19 (step F) may apply first; it does not touch `aws_iam_policy.dell2_ssm`, so both legs' plans stay 0/1/0 on that one
    address. YOU SEND NO COMMAND.
  </context>

  <the_act>
    LEG B2 -- OPEN (GO from the issuer when dell2 says "open now", relayed by 0.0.0_AB_MSTR): plan and apply with
    `-var open_dell2_f1_shell_window=true`: EXACTLY `0 to add, 1 to change, 0 to destroy` on `aws_iam_policy.dell2_ssm`, or apply
    nothing. Read back: dell2 `AWS-RunShellScript` + `i-0167fd745ad906a66` both resources allowed; + `i-0643a5bee8a8feabf`
    explicitDeny. NEVER-2 entry. Report the open time to me and to dell2 via 0.0.0_AB_MSTR.

    LEG C2 -- CLOSE (GO when dell2 calls X1; OR at 2026-10-09T06:00Z WITHOUT waiting for any answer): a plain plan and apply:
    EXACTLY `0 to add, 1 to change, 0 to destroy` on `aws_iam_policy.dell2_ssm`. Read back: dell2 `AWS-RunShellScript` explicitDeny
    (`DenyShellDocuments`). Close the entry. Report the close time.
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
comp-schedule: DECLARED-NOT-APPLICABLE applies on GOs; leg C2 carries the 06:00Z clock deadline.
comp-iam: RUN by the applier per leg -- denominator 1 policy address (aws_iam_policy.dell2_ssm), 1 user (cloudops-dell2-agent-user), 3 resource arms (the shell document, the F1 instance, one of the 6 privileged hosts); BLIND to every other principal and to the host role's own reach.
comp-adversary: RUN -- a wider open (0/1/0 on one address; other-host arm explicitDeny); the window left open (C2 on X1 or 06:00Z without waiting; backstops at the CTO and the issuer); BLIND: dell2's sends (reported after the fact).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>
  AC1 is read after leg C2 (window closed, default variables).

  <report>
    Report per leg to 2.0.0_SA_COO~C (and the times to dell2 via 0.0.0_AB_MSTR): the plan count; the live arms; the time in UTC in the
    subject; the ledger entry; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
