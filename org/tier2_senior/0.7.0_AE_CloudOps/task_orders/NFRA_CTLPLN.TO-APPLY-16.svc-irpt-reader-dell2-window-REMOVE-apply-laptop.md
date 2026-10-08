<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-16.svc-irpt-reader-dell2-window-REMOVE-apply-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-10-08</date>
    <status>complete</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>
<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc> (workstream ACCESS, cell `CT-a-1`, the Dell identity), an issuer's act on `1.0.0_SA_CTO` msgs 107091 and 107099: the laptop writes the policy a Dell cannot (dell2 ledger `irpt-ycdgen-f1-svc-20261008`).
<owned_cells>CT-a-1</owned_cells>
</decomp_ref>

  <closure>
    COMPLETE (issuer, ~21:3xZ). REMOVE put 2026-10-08T21:27:47Z on dell2's request (msgs 1663, 1665), before X1; read back by
    the issuer live: dell2 explicitDeny. The secret window was open 21:04:07Z-21:27:47Z. Ledger 2126Z closed (commit 2fe5100637).
  </closure>

  <objective>
    Leg REMOVE of a time-boxed window: set the resource policy of ONE secret, `arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l`, to the signed document
    `org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_BEFORE_restore_20261008.json`.
  </objective>

  <context>
    The policy is held by no Terraform root (written by hand; N = 1 writer). Halves: COO
    `org/tier1_exec/2.0.0_SA_COO/deliverables/NEVER_WIDEN_HALF_SVC_IRPT_READER_DELL2_WINDOW_20261008.md`; CTO `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_SVC_IRPT_READER_DELL2_WINDOW_20261008.md` (@7aab22d727, SIGNED). Trigger: dell2 2.0.0_SA_COO~G2 says its ledger leg X1 is reached (relayed by 0.0.0_AB_MSTR); the COO half's deadline 2026-10-09T06:00Z applies. The GO
    comes from the issuer when dell2 calls it; do not act on any other signal. YOU READ NO SECRET VALUE.
    DEADLINE (CTO msg 107105, binding): if no GO for this leg has come by 2026-10-09T06:00Z, at 06:00Z put the BEFORE
    document back WITHOUT waiting for any answer (steps 1-6 as written; at step 1, a live policy equal to the ADD file is the
    expected start), read it back, then report to 2.0.0_SA_COO~C and 1.0.0_SA_CTO. This is the one case where the trigger is
    the clock, not a GO.
    SET RULE (issuer ruling 2026-10-08 ~21:0xZ, after the 21:01:00Z rollback): AWS may store a Principal.AWS list and an
    ArnNotEquals value list in a different order. IAM evaluates both as unordered sets, so every comparison of a live policy
    with a signed file compares THOSE TWO LISTS AS SETS; every other part of the parsed JSON must be equal.
  </context>

  <the_act>
    1. Load /cloud-ops. Read the live policy (`get-resource-policy`). It must equal `org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_ADD_dell2_window_20261008.json` (compare parsed JSON).
       Not equal -> STOP and report both.
    2. Open ONE NEVER-2 ledger entry naming the secret ARN, the start and end files, both halves, and the rollback (put the
       start file back).
    3. `aws secretsmanager put-resource-policy --secret-id arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l --resource-policy file://org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_BEFORE_restore_20261008.json --block-public-policy`.
    4. Read back: the live policy equals the end file (parsed JSON).
    5. Simulate with `aws iam simulate-principal-policy --action-names secretsmanager:GetSecretValue --resource-arns arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l
       --resource-policy file://<the live policy you just read>`: ALLOWED `arn:aws:iam::313476888478:user/Andrew_Berman`; REFUSED (explicitDeny) `arn:aws:iam::313476888478:user/cloudops-dell2-agent-user` and `arn:aws:iam::313476888478:user/cloudops-dell1-agent-user`.
       Any other decision -> put the start file back, read it back, report.
    6. Close the entry. Report the time the put returned, in UTC.
  </the_act>

  <bounds>
    - This one secret's resource policy only. No GetSecretValue. No other secret, key or principal. No Terraform.
    - No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE one hand act by a seat, timed by dell2's ledger.
comp-iam: RUN by the applier: simulate-principal-policy with the secret's policy passed as the resource policy, for dell2, dell1 and the walker.
comp-adversary: RUN -- a wider document than signed (byte comparison to the signed file before and after); a stale before-state (STOP if the live policy differs from the expected start); the applier reading the value (forbidden); the window left open (REMOVE order; deadline in the COO half); BLIND: dell2's use of the value inside the window (dell2's ledger).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs; the act writes no repo file.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>aws secretsmanager get-resource-policy --secret-id arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l --query ResourcePolicy --output text</invocation><expect>WalkerReadsByExplicitArn</expect></criterion>
</proof_of_spec>
  AC1's row states that the parsed policy equals `SVC_IRPT_READER_POLICY_BEFORE_restore_20261008.json`, and lists each simulated decision of step 5.

  <report>
    Report ONCE to 2.0.0_SA_COO~C when the entry closes, or at a STOP (name the step): the start read (equal or not); the
    put's time in UTC, in the subject line; the read-back (equal or not); every simulated decision with its principal; the
    ledger entry's path and close; the proof-of-spec instance path (named with this order's full id) and its check result;
    commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
