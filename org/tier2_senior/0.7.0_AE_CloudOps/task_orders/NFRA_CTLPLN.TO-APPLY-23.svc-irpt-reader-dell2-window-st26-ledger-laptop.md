<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-23.svc-irpt-reader-dell2-window-st26-ledger-laptop</id>
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
<decomp_context>A second use of the svc-irpt secret-reader window (TO-APPLY-15/16's form) for dell2's ledger irpt-ycdgen-f1-st26-20261008. dell2 2.0.0_SA_COO~G2 msg 2025 (relay 107563): V1 closed 01:08Z. CTO consent for this ledger: named in the GO.</decomp_context>
</decomp_ref>

  <objective>
    LEG ADD: set the resource policy of `arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l` to
    the signed ADD file. LEG REMOVE: put the BEFORE file back at dell2's X1, OR at 2026-10-09T06:00Z WITHOUT waiting for any answer.
  </objective>

  <context>
    The same signed documents as TO-APPLY-15/16:
    `org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_ADD_dell2_window_20261008.json` (ADD) and
    `org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_BEFORE_restore_20261008.json` (BEFORE). The live policy equals BEFORE
    under the SET RULE (measured by the issuer ~01:1xZ). SET RULE: compare the Principal.AWS list and the ArnNotEquals value list as
    unordered sets; every other part of the parsed JSON must be equal. Halves: the window pair of TO-APPLY-15/16 (COO
    `NEVER_WIDEN_HALF_SVC_IRPT_READER_DELL2_WINDOW_20261008.md`, CTO @7aab22d727) with the CTO's consent for THIS ledger, named in the GO.
    YOU READ NO SECRET VALUE.
  </context>

  <the_act>
    LEG ADD (GO from the issuer after the CTO's consent):
    1. Read the live policy: must equal BEFORE (set rule), else STOP.
    2. NEVER-2 entry. `put-resource-policy --resource-policy file://<ADD file> --block-public-policy`.
    3. Read back: equals ADD (set rule). Simulate GetSecretValue with the live policy: dell2 allowed, dell1 explicitDeny, Andrew_Berman allowed.
       Any other result -> put BEFORE back at once, read back, report.
    4. Report the put time to me and to dell2 via 0.0.0_AB_MSTR at once (dell2 runs F1 on it).
    LEG REMOVE (GO when dell2 calls X1; OR at 2026-10-09T06:00Z WITHOUT waiting):
    5. Live equals ADD (set rule) as the expected start. Put BEFORE; read back equal (set rule); simulate dell2 explicitDeny, dell1
       explicitDeny, walker allowed. Close the entry; report the time.
  </the_act>

  <bounds>
    - This one secret's resource policy only. No GetSecretValue. No other secret, key or principal. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE two legs on GOs; the REMOVE leg carries the 06:00Z clock deadline.
comp-iam: RUN by the applier per leg -- denominator 1 secret policy, 3 principals simulated (dell2, dell1, the walker); BLIND to the secret's value (never read) and to every other principal.
comp-adversary: RUN -- a stale start (set-rule equality to BEFORE or STOP); a wider document (the signed file, set-rule read-back); a value read (forbidden); the window left open (REMOVE at X1 or 06:00Z without waiting; backstops: the issuer's 05:55Z reminder and the handoff); BLIND: dell2's use of the value (its ledger).
lane: the <paths> block names the ledger, the sentinel and the seat's own deliverables and logs.
</preflight>

<proof_of_spec>
  <criterion id="AC1" cell_refs="CT-a-1"><invocation>aws secretsmanager get-resource-policy --secret-id irpt/svc-irpt-analysis/password --query ResourcePolicy --output text</invocation><expect>WalkerReadsByExplicitArn</expect></criterion>
</proof_of_spec>
  AC1 is read after the REMOVE leg; its row states the live policy equals BEFORE under the set rule.

  <report>
    Report per leg to 2.0.0_SA_COO~C (and the times to dell2 via 0.0.0_AB_MSTR): the start read; the put time in UTC in the subject; the
    read-back; every simulated decision; the ledger entry; commit hashes and the measured push state. Leave the status flip to the issuer.
  </report>
</task_order>
