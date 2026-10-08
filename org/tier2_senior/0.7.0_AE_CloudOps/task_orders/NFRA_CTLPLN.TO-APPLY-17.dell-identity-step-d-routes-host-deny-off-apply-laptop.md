<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-17.dell-identity-step-d-routes-host-deny-off-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc> (workstream ACCESS, cell `CT-a-1`), the apply leg of cell 1 (AMENDMENTS 15 and 18 built it).
<owned_cells>CT-a-1</owned_cells>
</decomp_ref>

  <closure>
    COMPLETE (issuer, 2026-10-08 ~19:0xZ). APPLIED 2026-10-08T18:55:14Z by 0.7.0_AE_CloudOps, exactly 0/0/2, re-plan exit 0,
    ledger closed; report org/tier2_senior/0.7.0_AE_CloudOps/deliverables/NFRA_CTLPLN.TO-APPLY-17.step-d-report.md (commits
    148d5e171f, ee51cd6229). Issuer read-back, live, ~19:0xZ: six managed policies on the Dell group, routes-host absent;
    s3:PutObject on opal-data-cot/code/gold/x.py = allowed for dell1 and dell2. APPLIED, not EXERCISED until a Dell's own use.
  </closure>

  <objective>
    Apply STEP D on the Dell identity root: destroy the routes-host Deny policy and its group attachment (Andrew-direct
    ~13:2xZ "LIFT ITEM 5"). Steps A, B, C, E are applied.
  </objective>

  <context>
    Root `infra/aws/terraform/nfra-ctlpln-identity/`. The commit is the CLOUD trunk containing the merge 09b723ac96; the GO
    names the HEAD. The issuer planned it read-only at ~18:4xZ, untargeted, default variables (exit 2):
    `Plan: 0 to add, 0 to change, 2 to destroy.` 57 removed lines, 0 added. YOU MAKE NO S3 WRITE AND NO SSM DOCUMENT CHANGE
    YOURSELF: read-back by simulation only.
  </context>

  <the_act>
    The apply runs only when BOTH never-widen halves are SIGNED. ONE go; the issuer's GO names the CTO half and the HEAD.
    - COO half: org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_D_ROUTES_HOST_DENY_OFF_20261008.md
    - CTO half: org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_NFRA_CTLPLN_DELL_IDENTITY_STEP_D_ROUTES_HOST_DENY_OFF_20261008.md (@297921e56a, SIGNED)
    Read both in full first and carry every condition of both.

    1. Load /cloud-ops. Show `git status --porcelain -- infra/aws/terraform/nfra-ctlpln-identity/` is empty. Run and record the
       last line of `python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py` (expect
       `routes_freed=90/138 routes_still_refused=48 vendor_ok=245/245 all_ok=True` at its end). A failing line is a STOP.
    2. BEFORE: save the group's attached-policy list and `cloudops-dell-agent-routes-host-policy`'s current default version
       document (get-policy-version).
    3. Plan (no -target, no -var): EXACTLY `0 to add, 0 to change, 2 to destroy`, the addresses
       `aws_iam_policy.dell_agent_routes_host[0]` and `aws_iam_group_policy_attachment.dell_agent_routes_host[0]`, zero added
       lines -> go to 4. Anything else -> apply NOTHING; report the plan as read and stop.
    4. Open ONE NEVER-2 ledger entry naming the laptop, the saved list and document, both halves, and the rollback (re-apply the
       root at the merge's first parent 049d81ffa6, which re-creates the same policy and attachment).
    5. ONE apply through `.tools/safe-apply.sh`, the same plan shape.
    6. Read-back LIVE with `aws iam simulate-principal-policy` on EACH Dell user, matched statement named. ALLOWED:
       `s3:PutObject` on `arn:aws:s3:::opal-data-cot/code/gold/x.py`; `ssm:UpdateDocument` on one document named in the saved
       routes-host document. REFUSED: `ssm:SendCommand` on that document (implicitDeny); `lambda:UpdateFunctionCode` on one
       function named in `cloudops-dell-agent-routes-fn-policy` (explicitDeny by it); `iam:CreateRole` (explicitDeny). The
       group's attached-policy list read live (six expected). A re-plan reads no changes. Close the entry. APPLIED, not
       EXERCISED, until a Dell's own first use.
    7. The applied-time report to dell2 (via 0.0.0_AB_MSTR) says, in these words: "ssm:SendCommand on the 12 documents stays
       refused until cell D2 applies" (CTO msg 107113).
  </the_act>

  <bounds>
    - This root only, one apply. No edit to any `.tf`, policy document or test file.
    - `safe-apply` only. No push of a shared branch. No S3 write, no SSM document change, no other root.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE this order schedules nothing; it is one apply by a seat.
comp-iam: RUN at the cut by the cell's simulation (routes_freed 90 of 138, 48 still refused, every earlier field as at the base) and by the applier before the plan; step 6 repeats named arms against the LIVE policies.
comp-adversary: RUN -- a wider change than two destroys (exact plan shape, zero added lines); the routes-fn Deny removed by mistake (its live refused arm at step 6); SendCommand granted by mistake (refused arm); no way back (first-parent re-apply recreates the same document); BLIND: bucket policies and SCPs on the code buckets (row S25), and a Dell's own first use.
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the apply itself writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>python infra/aws/terraform/nfra-ctlpln-identity/tests/simulate_policy.py</invocation><expect>routes_freed=90/138 routes_still_refused=48</expect></criterion>
  <criterion id="AC2" cell_refs="CT-a-1"><invocation>terraform -chdir=infra/aws/terraform/nfra-ctlpln-identity plan -input=false -no-color -lock=false -detailed-exitcode; echo "exit=$?"</invocation><expect>exit=0</expect></criterion>
</proof_of_spec>

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the pre-plan line; the plan's count;
    the saved list; every live simulator arm per user with decision and matched statement; the live attached-policy list; the
    re-plan's exit; THE APPLIED TIME in UTC, in the subject line; the wrapper's WARN lines; the ledger entry's path and close;
    the proof-of-spec instance at org/tier2_senior/0.7.0_AE_CloudOps/deliverables/ named with this order's FULL id, and its
    check result; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
