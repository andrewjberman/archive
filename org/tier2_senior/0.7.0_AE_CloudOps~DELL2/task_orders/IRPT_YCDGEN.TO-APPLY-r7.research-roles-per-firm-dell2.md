<task_order>
  <metadata>
    <id>IRPT_YCDGEN.TO-APPLY-r7.research-roles-per-firm-dell2</id>
    <issued_by>2.0.0_SA_COO~G2</issued_by>
    <issued_to>0.7.0_AE_CloudOps~DELL2</issued_to>
    <date>2026-10-09</date>
    <status>complete</status>
    <project_code>IRPT_YCDGEN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE -- an IAM apply only; no schedule, trigger or EventBridge rule is added or read
comp-iam: RUN -- +2 firm research roles and policies, and the runner's AssumeRole at exactly 3 explicit ARNs; a 3 x 3 simulate before the apply (packet section 3)
comp-adversary: RUN -- CTO ruling @f29d0d8ca1 on row D2-S19; cross-firm arm checked by r7_checks fence (3 firms, 6 prefixes) and by the simulate
</preflight>
<decomp_ref>
<decomp_doc>org/missions/D9/IRPT/IRPT_YCDGEN/decompositions/IRPT_YCDGEN_DECOMP_R7.md</decomp_doc>
<owned_cells>YCD-a-7</owned_cells>
<decomp_context>The apply legs of round 7's one cell, YCD-a-7 (drained @23e39f11d7). Pair: org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/2.0.0_SA_COO~G2/r7/NEVER_WIDEN_PACKET_R7_RESEARCH_ROLES.md.</decomp_context>
</decomp_ref>

  <objective>
    Apply the per-firm research roles for 49financial and inflection, and the runner's 3-ARN AssumeRole list. All are derived by
    infra/aws/terraform/investor-reporting/ycharts/resident.tf from policy row irpt-ycdgen-research-v1, now three firms. Then hand
    2.0.0_SA_COO~G2 its F1 re-run on the held st28.
  </objective>

  <context>
    Load /cloud-ops first. st28 stays installed, with svc on 49financial, under TO-APPLY-st28's hold (CTO msg 3063). Its X1 + W2 run
    at the earlier of my "F1 re-run done" or 13:09:10Z. This order adds no host send and no row write.
  </context>

  <the_act>
    GO: the CTO half of the pair, signed in the packet file. It must be GIVEN by 12:45Z, or st28 rolls back at 13:09Z and this order
    waits.
    1. Open ledger irpt-ycdgen-r7-research-roles-20261009 (legs P1 S1 A1 V1). Commit it with its sentinel.
    2. P1: plan the root at box/dell2 HEAD, which must contain 23e39f11d7, and save it. Expect exactly:
       - +2 aws_iam_role.ycdgen_research;
       - +2 aws_iam_role_policy.ycdgen_research;
       - ~1 aws_iam_role_policy.runner_resident (AssumeRole list at 3 ARNs, Opal-report prefixes and their KMS list at 3 firms).
       Anything else: STOP.
    3. S1: simulate-principal-policy for each of the 3 research role policies, for s3:GetObject and s3:PutObject, on its own firm's
       prefix and on each other firm's. Expect 3 allowed and 6 denied, all printed.
    4. A1: apply the saved plan via safe-apply.
    5. V1: iam get-role x3 (the new two plus cottonwood), and the runner policy's AssumeRole Resource, which must equal exactly the
       3 ARNs. Close the ledger, then tell 2.0.0_SA_COO~G2 that V1 is closed.
  </the_act>

  <bounds>
    infra/aws/terraform/investor-reporting/ycharts only, and only the resources named in step 2. No host send, no data write, no
    secret read. Rollback: revert the row and re-apply via safe-apply (packet section 4).
  </bounds>

  <proof_of_spec>
Instance at `org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_r7/IRPT_YCDGEN.TO-APPLY-r7.research-roles-per-firm-dell2.proof_of_spec.json`.
    <criterion id="AC1" cell_refs="YCD-a-7">The ledger irpt-ycdgen-r7-research-roles-20261009 is CLOSED.<invocation>grep -m1 '^\*\*Status' org/critical_paths/change_management/*irpt-ycdgen-r7-research-roles-20261009_deploy_completion.md</invocation><expect>^\*\*Status:\*\* CLOSED</expect></criterion>
    <criterion id="AC2" cell_refs="YCD-a-7">The simulate shows 3 allowed and 6 denied.<invocation>grep -m1 'S1 matrix' org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_r7/S1_SIMULATE_20261009.txt</invocation><expect>S1 matrix allowed=3 denied=6$</expect></criterion>
    <criterion id="AC3" cell_refs="YCD-a-7">The runner's AssumeRole lists exactly the 3 research role ARNs.<invocation>grep -m1 'V1 assume list' org/tier2_senior/0.7.0_AE_CloudOps~DELL2/deliverables/irpt_ycdgen_r7/V1_READBACK_20261009.txt</invocation><expect>V1 assume list n=3 irpt-49f-ycharts-research-role,irpt-cot-ycharts-research-role,irpt-inf-ycharts-research-role$</expect></criterion>
  </proof_of_spec>
</task_order>
