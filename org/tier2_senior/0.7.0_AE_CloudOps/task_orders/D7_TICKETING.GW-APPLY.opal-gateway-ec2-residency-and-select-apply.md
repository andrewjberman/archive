<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-21-d7-gw-apply</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps (EC2 lane; safe-ec2-deploy mechanism)</issued_to>
    <date>2026-08-21</date>
    <status>staged -- ACTIVATES when the SITEZ build commits 2b7258f31c + 90d526c199 are REACHABLE FROM CLOUD HEAD (0.0.0_AB_MSTR's /integrate merge). ZERO URGENCY, no clock (site Z's own word: nobody is asking for an apply tonight; MSTR 63943). TARGET 2 of the D7 pending-apply surface -- a SEPARATE TO on a SEPARATE MECHANISM from D7_TICKETING.WA-APPLY (Lambda/Terraform): "TWO TARGETS ON TWO MECHANISMS ... anyone treating 'the pending apply' as a single act will do half of it." COO GO on activation.</status>
    <project_code>OPAL_TICKET</project_code>
  </metadata>

  <objective>
    APPLY LEG (laptop, EC2) for the opal-gateway app changes built on SITEZ: 2b7258f31c (Item A:
    5 NEW `_meta` anthropic/alwaysLoad residency marks -- 4 in app/tools.py + 1 in
    app/integrations/opal_portal/integration.py; a 6th, ack_messages, is already live in the
    broker @83e6a786d7 and needs NO apply) and 90d526c199 (Item B: lastModifiedDateTime on the
    $select of read_channel_messages + read_chat_messages). Mechanism: `safe-ec2-deploy.sh` per
    the EC2 code standard (local -> S3 -> EC2 pulls -> execute; NEVER write code on the VM) +
    the on-box boot test. Deployment Rules 7-12 bind.
  </objective>

  <context>
    PREREQUISITE, and it is also YOUR standing LD-0428 item (MSTR 63943): the ON-BOX READ of the
    gateway's actual deploy directory at your next legitimate touch of that instance -- TWO
    site-Z records CONFLICT: (A) the 2026-07-31 rename record says /opt/m365-mcp-gateway/app/
    verified serving; (B) org/critical_paths/change_management/20260815T0230Z_opal-gwrename-s3-cutover_deploy_completion.md
    (CLOSED 0336Z) says S4-14 deployed to /opt/opal-gateway with on-box verification and S6-15
    REMOVED /opt/m365-mcp-gateway (142M). Neither seat misread -- two renames 15 days apart, the
    older record carries no superseded marker; site Z marked it CONTESTED rather than flipping it
    record-vs-record. ONLY THE BOX SETTLES IT, and safe-ec2-deploy needs the right destination --
    resolve BEFORE the deploy, annotate the contested record with what the box says. (The
    "decoy source tree infra/aws/ec2/m365-mcp-gateway/ UNTRACKED" trap is site-Z-local: measured
    ABSENT on the laptop, 0 files -- no laptop action.)

    SPEC CORRECTION THAT BINDS ACCEPTANCE (MSTR 63943, site-Z self-correction): the item was
    WRITTEN as "five marks in tools.py"; the truth is 4 (tools.py) + 1 (integrations/opal_portal/
    integration.py) + 1 already-live (broker). The gateway registers tools from THREE homes
    (tools.py 34, integrations/ycharts 6, integrations/opal_portal 1) -- a census finding 5 in
    tools.py would read COMPLETE on a build missing integration.py: right count, right file,
    WRONG DENOMINATOR.

    THE mcp==1.28.0 HAZARD, stated so it travels to the boot test: the gateway PINS mcp==1.28.0
    (requirements.txt:4); every measurement site Z has is on 1.28.1. NOTHING establishes 1.28.0's
    behavior with the `meta` kwarg, and PyPI is EGRESS -- not pre-authorized; do not hunt a local
    shortcut, there is not one. TWO branches: LOUD -- 1.28.0 rejects the kwarg -> TypeError at
    DECORATION = import time = the gateway FAILS TO START; the boot test catches it
    deterministically and THE FIX IS REVERT, NOT DEBUG. SILENT -- 1.28.0 accepts and ignores
    `meta` -> the gateway BOOTS GREEN and ALL SIX MARKS ARE INERT while every check passes. NO
    BOOT TEST REACHES THE SILENT BRANCH -- it is not ruled out, and the proof SAYS SO.

    THE RULE-22a LADDER FOR THIS ITEM, so nobody closes on the wrong rung: DESIRED = 6/6 marks in
    source (AST census, sound at this layer only). APPLIED = the gateway starts with the new
    package (the boot test). EXERCISED = the six tools arrive RESIDENT at a session start with no
    ToolSearch hop -- THE ITEM'S ACTUAL CRITERION, and it is SITE Z'S READ at BG's next launch
    (they run it and report). 6/6 at the AST layer certifies the MARKS, NOT the residency. This
    TO does NOT close the exercised rung and declares it.
  </context>

  <compiler_tools_mandate>
    Phase 1: activation ancestry (`git merge-base --is-ancestor` both commits) + the on-box
    deploy-dir read (SSM, read-only) -> contested record annotated; `./infra/aws/ec2/verify-ec2.sh`
    parity before work (Rule 11); EC2_MANIFEST.json entry confirmed (Rule 8).
    Phase 2: safe-ec2-deploy per the standard; deploy-completion ledger opened at start, closed
    in-session; boot test on the box (systemd active, /health, /mcp auth response) -- on the LOUD
    branch: REVERT, not debug, and surface.
    Phase 3: the mark census at the RIGHT denominator (4+1 in the deployed tree via the S3-pulled
    artifact, three registration homes named); the SILENT branch declared UNREACHED; the
    exercised rung declared SITE Z'S (their report lands via the ferry).
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - 0.0.0_AB_MSTR / ~Z: activation = the /integrate merge; the exercised-rung report comes back
      from site Z at BG's next launch -- your close cites it as PENDING-THEIRS, never claims it.
    - The broker (server.py @83e6a786d7) needs NO apply (per-session stdio, self-deploying,
      already exercised at three seats) -- Target 3 is nobody's act; do not "deploy" it.
    - 1.0.0_SA_CTO: mechanics per the EC2 standard; nothing here is a new gate or alarm.
  </cross_domain_coordination>

  <acceptance_criteria>
    (Rule-24 layer declaration: the layer is the EC2 APPLY LEG as cut -- G1 activation +
    deploy-dir, G2 denominator census, G3 deploy + ledger, G4 boot test + hazard honesty, G5
    ladder honesty, G6 proof; exhaustive over the leg; the exercised rung and the Lambda target
    are OUTSIDE.)
    G1  Activation evidenced (both commits' ancestry, rc printed); the on-box deploy-dir read
        RESOLVES the contested pair (A)/(B) and the losing record is ANNOTATED with the box's
        answer (superseded marker), never flipped record-vs-record.
    G2  Mark census at the RIGHT denominator: 4 (tools.py) + 1 (integration.py) in the DEPLOYED
        artifact, three registration homes named (34/6/1); a tools.py-only count is a FAIL.
    G3  Deploy via safe-ec2-deploy (local -> S3 -> pull), EC2_MANIFEST current, parity verified
        before work, ledger opened + closed in-session.
    G4  Boot test run and printed; the 1.28.0 two-branch hazard stated in the proof: LOUD ->
        REVERT-not-debug (exercised only if it fires); SILENT -> declared NOT REACHABLE by the
        boot test, NOT ruled out, NOT closed on. No PyPI egress; the pin is not changed.
    G5  The 22a ladder stated on the proof: DESIRED (AST 6/6) + APPLIED (boot) closed here;
        EXERCISED (resident-at-session-start, no ToolSearch hop) = SITE Z's read at BG's next
        launch, declared PENDING-THEIRS.
    G6  Proof instance VALID rc=0 positional G1-G6; RAVC close to COO, cc 0.0.0_AB_MSTR (ferry to
        ~Z) + 1.0.0_SA_CTO.
  </acceptance_criteria>

  <proof_of_spec>
    <expected_criteria>G1,G2,G3,G4,G5,G6</expected_criteria>
    <instance_path>org/tier2_senior/0.7.0_AE_CloudOps/deliverables/D7_TICKETING.GW-APPLY_PROOF_OF_SPEC.json</instance_path>
  </proof_of_spec>

  <requirements>
    <requirement id="1">Do not start before COO's GO (activation = the merge). Zero urgency; normal cadence; never open an apply at the day boundary just because the files arrived. SSM reads are read-only until the deploy act; S3 is the artifact store for ALL EC2 code (Rule 12). Surprise channel: one line to COO.</requirement>
  </requirements>
</task_order>
