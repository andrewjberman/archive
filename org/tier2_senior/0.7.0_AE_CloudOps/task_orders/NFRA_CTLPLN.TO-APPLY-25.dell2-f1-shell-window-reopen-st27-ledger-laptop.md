<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-25.dell2-f1-shell-window-reopen-st27-ledger-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>

  <closure>
    COMPLETE (issuer, ~04:0xZ). B2 opened 2026-10-09T02:37:46Z; LEG C2 SUPERSEDED by TO-APPLY-26 (standing access applied 03:52:21Z, the
    window variable retired). Ledger closed SUPERSEDED (@8d42d8967a).
  </closure>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>A third use of the dell2 F1 shell window built by AMENDMENT 19 (variable open_dell2_f1_shell_window), for dell2's ledger irpt-ycdgen-st27-20261009 (dell2 0.7.0_AE_CloudOps~DELL2 msg 2194, relay 0.0.0_AB_MSTR): sends P1 read-only, then the st27 install + V1; no secret window (st27 carries no service secret). Terms: those of TO-APPLY-20 (st26). CTO consent for this ledger: named in the GO.</decomp_context>
</decomp_ref>


  <amendment>
    AMENDMENT 1 (issuer, 2026-10-09 ~03:0xZ), on Andrew-direct ~02:5xZ: "the DELLS should not be waiting on us for this function, let's
    adjust their permissions accordingly". LEG C2 IS SUPERSEDED. Do NOT close the window at dell2's V1 or at 06:00Z. Per the CTO record
    `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261009_025xZ_DELLS_RUN_THEIR_OWN_SCRIPTS_NO_LAPTOP_WAIT.md` @de8b26aa1f, the
    window stays open until the CT-a-1 AMENDMENT 24 apply replaces it with standing access; it is never re-closed. AC1 is read after that
    apply (default variables; the variable no longer exists). The issuer closes this order when the replacing apply lands.
  </amendment>

  <objective>
    Open dell2's F1 shell window again when dell2 says "open now" (LEG B2) and close it at dell2's V1 or at 2026-10-09T06:00Z
    WITHOUT waiting (LEG C2) -- exactly the plans of NFRA_CTLPLN.TO-APPLY-18 legs B and C.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`. Halves: the step D2 pair (COO
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_D2_SENDCOMMAND_AND_F1_SHELL_WINDOW_20261008.md`,
    CTO @ac2c6e852d) with the CTO's YES for this ledger (msg 107646 reply) under the STANDING CONSENT addendum to the CTO half (@5c2d9da8b2): one host,
    targeted 0/1/0, one window at a time on a named open ledger, closed at the ledger's close leg or 4 hours after opening, whichever
    is first, without waiting, then read back with an untargeted 0/0/0 plan; sends reported after the fact. Same send-report rule: dell2 reports every send after the fact.
    YOU SEND NO COMMAND. Use TF_PLUGIN_CACHE_DIR=C:/Users/AndrewBerman/.terraform.d/plugin-cache, and delete your Terraform scratch dir
    after leg C2's ledger closes (0.0.0_AB_MSTR msg 107626).
  </context>

  <the_act>
    LEG B2 -- OPEN (GO from the issuer when dell2 says "open now", relayed by 0.0.0_AB_MSTR): plan and apply TARGETED (`-target=aws_iam_policy.dell2_ssm`) with
    `-var open_dell2_f1_shell_window=true`: EXACTLY `0 to add, 1 to change, 0 to destroy` on `aws_iam_policy.dell2_ssm`, or apply
    nothing. Read back: dell2 `AWS-RunShellScript` + `i-0167fd745ad906a66` both resources allowed; + `i-0643a5bee8a8feabf`
    explicitDeny. NEVER-2 entry. Report the open time to me and to dell2 via 0.0.0_AB_MSTR.

    LEG C2 -- CLOSE (GO when dell2 calls V1; OR at 2026-10-09T06:00Z WITHOUT waiting for any answer): a plain plan and apply:
    EXACTLY `0 to add, 1 to change, 0 to destroy` on `aws_iam_policy.dell2_ssm`. Read back: dell2 `AWS-RunShellScript` explicitDeny
    (`DenyShellDocuments`). Then an UNTARGETED plan with default variables reads `No changes` (0/0/0). Close the entry. Report the
    close time.
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
comp-adversary: RUN -- a wider open (0/1/0 on one address; other-host arm explicitDeny); the window left open (C2 on V1 or 06:00Z without waiting; backstops at the CTO and the issuer); BLIND: dell2's sends (reported after the fact).
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
