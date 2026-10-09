<task_order>
  <metadata>
    <id>NFRA_CTLPLN.TO-APPLY-30.svc-irpt-reader-dell2-window-served-read-laptop</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.7.0_AE_CloudOps~CTL</issued_to>
    <date>2026-10-09</date>
    <status>staged</status>
    <project_code>NFRA_CTLPLN</project_code>
  </metadata>

  <closure>
    COMPLETE (issuer, ~14:0xZ). CTO yes msg 107976. ADD put 13:37:33-13:37:36Z by 0.7.0_AE_CloudOps~CTL -- AFTER dell2 G2's own window
    13:05:57-13:35:57Z had already closed with NO read (msg 107978), so the access was never used. REMOVE put 13:45:37-13:45:41Z on G2's
    "remove at once"; read back SET-EQUAL to BEFORE, dell2/dell1 explicitDeny. Issuer live poll: dell2 on the policy first seen 13:38:02Z,
    gone 13:46:07Z. Ledger closed (@d7e3566b1d). A retry is a new GO, ADD first, the 30 minutes run from W1.
    RETRY (AMENDMENT 1) COMPLETE (issuer, ~14:5xZ): ADD 14:19:47Z, G2 read once ~14:26:12Z and called R DONE 14:26:19Z, REMOVE 14:35:05Z,
    read back SET-EQUAL to BEFORE, dell2/dell1 explicitDeny. Issuer live poll: first seen 14:20:12Z, gone 14:35:36Z. Ledgers closed
    (@045091bab0).
  </closure>

<risk>WORLD</risk>
<proof_genre>DEPLOY</proof_genre>
<decomp_ref>
<decomp_doc>org/missions/D0/NFRA/NFRA_CTLPLN/decompositions/NFRA_CTLPLN_DECOMP.access1.md</decomp_doc>
<owned_cells>CT-a-1</owned_cells>
<decomp_context>A further use of the svc-irpt secret-reader window (TO-APPLY-28 form) for dell2's ledger irpt-ycdgen-served-read-20261009, with a 30-minute hard close. dell2 crossbox ORDER (relay 0.0.0_AB_MSTR msg 107968, bus 4854909d); dell2 CTO half org/missions/D9/IRPT/IRPT_YCDGEN/deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_SERVED_READ_WINDOW_CTO_HALF.md @da885deef2. Laptop CTO consent for this ledger (a service-secret window is asked per ledger): named in the GO.</decomp_context>
</decomp_ref>



  <amendment>
    AMENDMENT 1 (issuer, 2026-10-09 ~14:1xZ) -- REOPENED for ONE RETRY of the same ledger irpt-ycdgen-served-read-20261009, under the same
    CTO consent (msg 107976) and the dell2 CTO half @da885deef2. dell2 2.0.0_SA_COO~G2 (relay 0.0.0_AB_MSTR msg 107988): a served read of
    REQ-5e4149d2. ADD FIRST, on the GO: start from live == BEFORE (set rule), put the signed ADD, read back, simulate; send the put time to
    me and to dell2 via 0.0.0_AB_MSTR at once (G2 takes W1 on it). REMOVE at G2's "R done", OR 30 minutes after the ADD put WITHOUT waiting
    -- this lane holds the clock itself. The first pair (13:37Z / 13:45Z) stays closed as recorded. A new NEVER-2 entry for the retry.
  </amendment>

  <amendment>
    AMENDMENT 2 (issuer, 2026-10-09 ~15:3xZ) -- STAGED for a THIRD use of the same ledger irpt-ycdgen-served-read-20261009, same CTO consent
    (msg 107976) and dell2 CTO half @da885deef2 (dell2 2.0.0_SA_COO~G2, relay 0.0.0_AB_MSTR msg 108023). DO NOT ADD on this text: the ADD waits
    for the issuer's GO, which follows G2's "ADD now" (sent when dell2 0.7.0_AE_CloudOps~DELL2 reports R2 PASS on IRPT_ANLREQ.TO-APPLY-Y1 rev 4).
    On the GO: start from live == BEFORE, put the signed ADD, read back, simulate, send the put time to me and to dell2 via 0.0.0_AB_MSTR at
    once. REMOVE at G2's "R done" or ADD+30m WITHOUT waiting, this lane's own clock. A new NEVER-2 entry for this use.
  </amendment>

  <objective>
    LEG ADD: set the resource policy of `arn:aws:secretsmanager:us-east-1:313476888478:secret:irpt/svc-irpt-analysis/password-rfHf9l` to
    the signed ADD file. LEG REMOVE: put the BEFORE file back at G2's "R done", OR 30 minutes after the ADD put time WITHOUT waiting for any answer.
  </objective>

  <context>
    The same signed documents as TO-APPLY-15/16:
    `org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_ADD_dell2_window_20261008.json` (ADD) and
    `org/tier1_exec/2.0.0_SA_COO/deliverables/SVC_IRPT_READER_POLICY_BEFORE_restore_20261008.json` (BEFORE). The live policy must equal BEFORE under
    the SET RULE at the start of LEG ADD (step 1 reads it). SET RULE: compare the Principal.AWS list and the ArnNotEquals value list as
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
    4. Report the put time to me and to dell2 via 0.0.0_AB_MSTR at once (G2 reads once on it). Run LEG REMOVE yourself at ADD+30m if no "R done" has come -- no GO is needed for the REMOVE.
    LEG REMOVE (GO when G2 calls "R done"; OR 30 minutes after the ADD put time WITHOUT waiting):
    5. Live equals ADD (set rule) as the expected start. Put BEFORE; read back equal (set rule); simulate dell2 explicitDeny, dell1
       explicitDeny, walker allowed. Close the entry; report the time.
  </the_act>

  <bounds>
    - This one secret's resource policy only. No GetSecretValue. No other secret, key or principal. No push of a shared branch.
  </bounds>

  <paths>
    org/critical_paths/change_management/
    org/critical_paths/.open_deploys/
    org/tier2_senior/0.7.0_AE_CloudOps~CTL/deliverables/
    org/tier2_senior/0.7.0_AE_CloudOps~CTL/logs/
  </paths>

<preflight>
comp-schedule: DECLARED-NOT-APPLICABLE two legs on GOs; the REMOVE leg carries a 30-minute clock deadline from the ADD.
comp-iam: RUN by the applier per leg -- denominator 1 secret policy, 3 principals simulated (dell2, dell1, the walker); BLIND to the secret's value (never read) and to every other principal.
comp-adversary: RUN -- a stale start (set-rule equality to BEFORE or STOP); a wider document (the signed file, set-rule read-back); a value read (forbidden); the window left open (REMOVE at "R done" or ADD+30m without waiting; the applier holds the clock itself (it does not wait for a GO)); BLIND: dell2's use of the value (its ledger).
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
