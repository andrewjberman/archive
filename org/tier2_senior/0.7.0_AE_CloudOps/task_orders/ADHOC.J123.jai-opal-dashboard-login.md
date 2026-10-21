<task_order>
# pipeline-override: remote job J123 (LDO-001) is an operations act outside the L1-L10 pipeline -- no project, no PRD, no decomposition; the order exists only because a Tier-2 seat acts on an order in its home (LD-0529); Andrew-direct 16:32Z; CTO ruling 9150.
  <metadata>
    <id>1.0.0_SA_CTO~DELL1-2026-10-21-J123-jai-opal-dashboard-login</id>
    <issued_by>1.0.0_SA_CTO~DELL1</issued_by>
    <issued_to>0.7.0_AE_CloudOps~ADVI1</issued_to>
    <date>2026-10-21</date>
    <status>pending -- AMENDED 2026-10-21 ~16:5xZ by 1.0.0_SA_CTO~DELL1 on Andrew-direct 16:46Z (MSTR 9157): the run (J2) and the draft (J3) are 4.0.0_SA_CRO~JAI1's; the reads, the proof instance and the receipt (J1, J4) stay with 0.7.0_AE_CloudOps~ADVI1; no gate limb graded this modification</status>
    <project_code>ADHOC (remote job J123 / LDO-001; Andrew-direct 2026-10-21 16:32Z at the laptop terminal, record org/tier0_exec/0.0.0_AB_MSTR/deliverables/ANDREW_DIRECT_20261021_163xZ_DELL1_HANDLES_JAI_ACCOUNT_CREATION_AS_AN_OPAL_USER.md; CTO ruling msg 9150; seating MSTR 9153)</project_code>
    <risk>SERVED</risk>
  </metadata>

  <objective>
    Create the Opal dashboard login for Jai (an Opal intern) as an opal-capital internal-tier user, on Andrew's word
    "make sure the dell1 box is handling the JAI account creation as an opal user". ONE act, three steps: the user
    insert by the sanctioned path, a DRAFT notice to Yang Liu, the receipt.
  </objective>

  <context>
    Measured by the holder (msg 9156): the route is users/scripts/create_user_v2.py --firm opal-capital (internal tier);
    jai@opalinvest.com is ABSENT from opal-users-v2 (email-index, Count 0); the gateway has no directory tool and the
    mailbox gives no surname. THE NAME IS NEVER GUESSED: it comes from Andrew's word (or Yang Liu's, relayed by him),
    listed on the box's open calls as act row dell1-20261021T164621Z-5956. No seat messages Yang Liu or anyone outside the
    fabric without Andrew's explicit confirmation; the notice is produced as a DRAFT through the gateway (create_draft)
    and SENT by nobody. Secrets and credentials are never printed, logged or committed; a generated temporary password
    (if the path makes one) is delivered only through the path's own channel.
  </context>

  <preflight>
    comp-schedule: DECLARED-NOT-APPLICABLE -- no schedule, rule, cron or pipeline is created or changed; one on-demand user insert.
    comp-iam: DECLARED-NOT-APPLICABLE -- no IAM grant, role or policy changes; the sanctioned script runs under the holder's existing
      credentials against the users table it already writes.
    comp-adversary: DECLARED-NOT-APPLICABLE -- no served surface, bucket, Lambda or route changes; the blast radius is one row in
      opal-users-v2 for one named internal user, reversible by the same path.
  </preflight>

  <paths>
    users/scripts/create_user_v2.py (read; run as the sanctioned path, never edited by this order)
    org/tier2_senior/0.7.0_AE_CloudOps~ADVI1/deliverables/ (the receipt and the proof instance)
  </paths>

  <acceptance_criteria>
    J1  HELD until the name lands: the holder's record names the open-calls row (5956) and the time Andrew's word
        arrived, quoting it; a run before that word fails this order.
    J2  The insert: create_user_v2.py --firm opal-capital run ONCE for the confirmed username BY 4.0.0_SA_CRO~JAI1
        (Andrew-direct 16:46Z: "spawn a new CRO to analyze this and run it"; the CRO analyzes and runs, the CloudOps lane
        never writes the table alongside it); 0.7.0_AE_CloudOps~ADVI1 takes the email-index read BEFORE (Count 0) and
        AFTER (Count 1) with the denominator (the table name) and records the full name as given and no credential.
    J3  The draft: one create_draft to Yang Liu through the gateway by 4.0.0_SA_CRO~JAI1 holding the username and what
        Jai can open (the CRO's analysis names the pages and the firm tier); the proof prints the draft id and the sentence
        "nothing was sent"; a send of any kind fails this order.
    J4  The receipt: one message to 0.0.0_AB_MSTR~DELL1 and 1.0.0_SA_CTO~DELL1 citing this order's path, the proof
        instance, and the status flip to complete in this file.
  </acceptance_criteria>

  <proof_of_spec>
    Criterion ids: J123-J1, J123-J2, J123-J3, J123-J4. Instance at
    org/tier2_senior/0.7.0_AE_CloudOps~ADVI1/deliverables/ADHOC.J123.jai-opal-dashboard-login.proof_of_spec.json, validated with
    python .tools/proof-of-spec-check.py <instance> J123-J1,J123-J2,J123-J3,J123-J4 BEFORE the status flip. No credential in the
    instance.
  </proof_of_spec>
</task_order>
