<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-08-21-d7-gw-apply</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps (EC2 lane; safe-ec2-deploy mechanism)</issued_to>
    <date>2026-08-21</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: ORPHAN. Its project code "D7_TICKETING" resolves to no registration, and no live project references it. Closed as a record act, not a work verdict; recoverable by re-minting the project. Prior status: ⛔⛔ **WITHDRAWN AS TO PLACEMENT BY THE ISSUING SEAT 2026-08-21T1358Z -- DO NOT EXECUTE AS A SEPARATE DEPLOY.** ⛔ **BUT G1-G6 ARE *NOT* WITHDRAWN: THEY TRAVEL WITH THE WORK.**
    **PLACEMENT MOVED (Rule 26 @95b7eeb458), MEASURED NOT ASSUMED at this seat:** both build commits are authored by `0.5.0_AE_OpalETL~Z` -- a site-Z seat -- and both are ancestors of HEAD on this box (`2b7258f31c` ANCESTOR, `90d526c199` ANCESTOR). Builder and box agree; the deploy leg is site Z's.
    **PAYLOAD SUBSUMED:** `safe-ec2-deploy` ships the tree, the tree already contains both commits, so Andrew's ~1346Z card-3 gateway deploy (*"approved on all three, proceed"*) carries this TO's entire code payload. **There is nothing left for a second deploy to add** -- which is the whole reason this is a withdrawal and not a re-route.
    ⛔ **THE CRITERIA ARE THE PART THAT MUST NOT BE LOST, AND THIS IS WHY THIS TO WAS NOT WITHDRAWN AS ITS SIBLING'S TWIN.** `1.0.0_SA_CTO~Z`'s ACT-3 dispatch originally read *"safe-ec2-deploy then verify-ec2"* and carried **none** of G1-G6. Had this been withdrawn by symmetry with `WA-APPLY`, the gateway would have deployed with **no mark census at the right denominator, no boot-test discipline, no 1.28.0 two-branch hazard statement and no ladder honesty** -- and the withdrawal would have *looked* like the tidy outcome. **A WITHDRAWAL THAT DROPS THE CRITERIA IS WORSE THAN THE DOUBLE-APPLY IT PREVENTS.** G1-G6 now ride ACT 3 at `0.5.0_AE_OpalETL~Z`; the dispatch is amended.
    ⚠ **G1's DISCHARGE IS STALE AND MUST BE RE-RUN BEFORE DEPLOY.** The on-box deploy-directory read that settled `/opt/opal-gateway` was taken ~0240Z; instance `i-07dccb1615503ac99` has LaunchTime **2026-08-21T07:58:44Z**. **A read taken at 0240Z cannot describe a box that launched at 0758Z -- the instance that settled the destination no longer exists**, and `safe-ec2-deploy` needs that destination. Re-run G1 against the CURRENT instance and **annotate the stale record rather than flipping it.** *(Measured by `1.0.0_SA_CTO~Z` on the live primitive; consistent with this seat's 0820Z record of the apply carrying an IP change.)*
    **The `main.tf` line stays untouched** -- this TO excludes it in terms, and exercising `user_data` IS the replacement the criterion exists to prevent. **`0.7.0_AE_CloudOps`: nothing to approve, decline or hand back; the work moved and the issuing seat retracted the dispatch.** Prior status preserved verbatim below.
    **Prior status, superseded, retained verbatim:** staged -- ⛔ ACTIVATION CONDITION MET 2026-08-21 ~0110Z (both commits verified reachable from CLOUD HEAD at my seat: 2b7258f31c rc=0, 90d526c199 rc=0, via MSTR's /integrate merge 8aa7120a09), GO DEFERRED TO THE NEXT WORKING BLOCK for the same reason as its sibling WA-APPLY: site Z's own "nobody is asking for an apply tonight", CTO~Z's word on the hour, and the assignee's board. CADENCE, NOT A GATE. PREREQUISITE DISCHARGED 2026-08-21 ~0240Z: the on-box deploy-directory read is CLOSED by LD-0428 @b3fdc39f55 (0.7.0, executing truth on the box) -- /opt/opal-gateway LIVE, /opt/m365-mcp-gateway ABSENT (unit load=not-found); safe-ec2-deploy's destination is settled and Phase 1's contested-record item is satisfied. See <inherited_defect_on_the_code_page> -- main.tf still names the dead path. ORIGINAL: The prerequisite on-box deploy-directory read (the contested /opt/opal-gateway vs /opt/m365-mcp-gateway pair) still comes FIRST -- safe-ec2-deploy needs the right destination, and that read is the LD-0428 item already on 0.7.0's board with no clock. ORIGINAL: ACTIVATES when the SITEZ build commits 2b7258f31c + 90d526c199 are REACHABLE FROM CLOUD HEAD (0.0.0_AB_MSTR's /integrate merge). ZERO URGENCY, no clock (site Z's own word: nobody is asking for an apply tonight; MSTR 63943). TARGET 2 of the D7 pending-apply surface -- a SEPARATE TO on a SEPARATE MECHANISM from D7_TICKETING.WA-APPLY (Lambda/Terraform): "TWO TARGETS ON TWO MECHANISMS ... anyone treating 'the pending apply' as a single act will do half of it." COO GO on activation.</status>
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

    (2026-08-21, COO) THE SILENT BRANCH IS NO LONGER HYPOTHETICAL -- IT FIRED IN THIS ESTATE
    LAST NIGHT, ON THE NEIGHBOURING ITEM. Specimen, rung for rung (1.0.0_SA_CTO's D4 finding):
    TS_HOLDINGS_ENABLED=1 -- DESIRED true; APPLIED true and verified ON THE DEPLOYED PACKAGE BY
    CodeSha256, so the token is genuinely in the running bytes; the scheduled run GREEN -- and
    the flag is read into a bool THAT IS NEVER BRANCHED ON, gating a function defined and never
    called. Zero rows landed and none ever could have. Every rung except EXERCISED passed,
    EXERCISED was the only one that could discriminate, and nobody ran it.
    WHY THIS IS A PARAGRAPH AND NOT A FOOTNOTE: "not ruled out" invites a reasonable engineer to
    price the silent branch as a TAIL RISK and proceed. "It fired here, on the adjacent item,
    within hours" tells them THE TAIL ALREADY FIRED. Same fact about the world; opposite
    instruction to whoever runs the boot test. Plan the mark-residency read as work you WILL do,
    not as a contingency. Raised by 1.0.0_SA_CTO~Z, ferried by 0.0.0_AB_MSTR (64132); site Z
    correctly declined to edit this TO themselves -- one logical statement, one home.

    THE RULE-22a LADDER FOR THIS ITEM, so nobody closes on the wrong rung: DESIRED = 6/6 marks in
    source (AST census, sound at this layer only). APPLIED = the gateway starts with the new
    package (the boot test). EXERCISED = the six tools arrive RESIDENT at a session start with no
    ToolSearch hop -- THE ITEM'S ACTUAL CRITERION, and it is SITE Z'S READ at BG's next launch
    (they run it and report). 6/6 at the AST layer certifies the MARKS, NOT the residency. This
    TO does NOT close the exercised rung and declares it.
  </context>

  <inherited_defect_on_the_code_page>
    ⛔ DISCHARGED 2026-08-21 ~0810Z -- THIS SECTION IS NOW HISTORY, NOT A LIVE DEFECT. Read it for
    the MECHANISM (which still teaches) and NOT as a thing to fix; the fix is done and applied.
    Andrew ruled it twice: "fix it now, you have my sovereign approval" (the TF fix), then again
    with the outage cost in front of him after 0.7.0 declined to widen the first word into the
    second. Corrected @5b5e99fadb, APPLIED @ad38fded65 through safe-apply, verified on the box,
    deploy-completion ledger closed 4/4, re-plan clean. Instance NOT replaced (0 add / 1 change /
    0 destroy, in-place); ~100s stop/start, returned unattended because the systemd unit is ENABLED.
    ⚠ ONE LIVE CONSEQUENCE FOR WHOEVER RUNS THIS TO: THE GATEWAY'S PUBLIC IP CHANGED,
    3.83.108.63 -> 13.221.151.249 (auto-assigned, no Elastic IP, released by the stop/start).
    ALB routing targets by INSTANCE ID and survived (target healthy; /mcp 401 x3 identical to the
    captured pre-state). MEASURED FOR THIS TO SPECIFICALLY: it carries ZERO references to the old
    address (the single IP-literal at :80 below is `0.0.0.0:8080` inside the quoted defect text,
    a bind address and not a pin; positive control on this file = 3 hits for "residency", so the
    search discriminates). The laptop-side fabric sweep found no operational pins either -- its two
    hits are the deploy record and session log documenting the change, correct-at-vintage. THE
    UNSWEPT HALF IS EXTERNAL (vendor consoles, allowlists, firewall rules), which no repo sweep can
    reach and which is DECLARED rather than closed.
    WHY THE APPLY HAPPENED AT ALL, since the running box was already correct: not applying was NOT
    free. It parked a pending stop/start in the diff, to be fired by whatever apply came next,
    bundled with something unrelated, at a moment nobody chose, against a stack of 15 .tf files.
    A deliberate bounce with pre-state captured was the cheaper one. (Reframe: 1.0.0_SA_CTO.)
    Recorded by 2.0.0_SA_COO, who placed the original finding here -- a TO that still described a
    fixed defect as live would be the same class the defect itself belonged to.

    (2026-08-21, COO -- placed here per 0.0.0_AB_MSTR 64208, Andrew-direct at the MSTR~Z terminal
    ~0255Z: "you should definitely mention this about the main.tf:191 to MSTR on the laptop
    though". Re-derived at the COO seat before placing; both claims confirmed at source.)

    infra/aws/terraform/opal-gateway/main.tf carries TWO stale references inside user_data, and
    they CONTRADICT the on-box truth this TO's own Phase 1 prerequisite just established:
      :191  install -d -o ec2-user -g ec2-user /opt/m365-mcp-gateway     <- CREATES the dead path
      :193  "... and deploy/m365-mcp-gateway.service (binds 0.0.0.0:8080)"  <- DANGLING CITATION
    MEASURED AT THE COO SEAT: infra/aws/ec2/m365-mcp-gateway/deploy -> ABSENT. The real unit is
    infra/aws/ec2/opal-gateway/deploy/opal-gateway.service -> EXISTS (950 B). And LD-0428
    (@b3fdc39f55, 0.7.0's on-box read) settled the contested pair: /opt/opal-gateway is LIVE,
    /opt/m365-mcp-gateway is ABSENT with its unit load=not-found.

    ⛔ WHY IT SURVIVED EVERY CHECK, AND IT IS THE SHARPEST PART (site Z's mechanism, 64208):
    USER_DATA EXECUTES ONLY ON FIRST BOOT, AND THE CUTOVER DELIBERATELY DID NOT REPLACE THE
    INSTANCE (main.tf:60-65 -- "The EC2 INSTANCE is NOT replaced"). So the one block the rename
    left stale is EXACTLY THE ONE BLOCK ITS OWN EXECUTION MODEL COULD NEVER EXERCISE, and the
    single event that WOULD execute it -- an instance replacement -- is precisely the event the
    cutover was designed to avoid. "A rename verified by what it changes cannot see what it left
    behind in code that does not run." Plan, live AWS and the running box all agreed because none
    of them executes user_data on a live instance.

    ⛔ AND THE REMEDY INVERTS THE USUAL ONE: for the other three instances of this class tonight,
    exercise is CHEAP -- run it. HERE, EXERCISE *IS* THE FAILURE EVENT: exercising user_data is
    the instance replacement that resurrects the dead path in production. WHEN THE EXERCISE IS
    THE DISASTER YOU ARE PREVENTING, READING IS THE ONLY AVAILABLE CONTROL. A "verify it on the
    box" reflex is not merely insufficient here, it is structurally impossible. Fix it on the
    page, by inspection.

    SCOPE (two lines, one heredoc): :191 install path -> /opt/opal-gateway; :193 reference ->
    opal-gateway/deploy/opal-gateway.service.
    ⛔ NOT AUTHORIZED BY THIS TO AND NOT A GATE ON THE APPLY. A TF edit is an APPLY ACT and no
    existing GO covers it (0.7.0 correctly did not touch it; site Z correctly did not either).
    It is LATENT -- nothing scheduled replaces that instance -- so it carries NO CLOCK. It is
    recorded here rather than left on the bus because whoever eventually runs GW-APPLY or any
    instance rebuild INHERITS it, and a durable artifact beats a transient correction. Route the
    edit through the normal safe-apply path when an apply window is open; do not fold it into
    this TO's deploy legs.

    OPEN, DELIBERATELY UNCLASSIFIED: site Z surfaced something about infra/aws/ec2/EC2_MANIFEST.json
    (Deployment Rule 8) and their frame truncated before the finding. ASK 1.0.0_SA_CTO~Z DIRECTLY
    -- do not guess it; MSTR explicitly declined to invent it and so do I.
  </inherited_defect_on_the_code_page>

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
