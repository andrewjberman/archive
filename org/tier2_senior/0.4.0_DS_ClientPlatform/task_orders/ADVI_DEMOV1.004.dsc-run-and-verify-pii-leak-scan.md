<task_order>
  <metadata>
    <id>2.0.0_SA_COO~C-2026-05-21-demov1-to4-run-verify</id>
    <issued_by>2.0.0_SA_COO~C</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <!-- GO'd 2026-05-22 by 2.0.0_SA_COO~C, SCOPED. The gating text below
         ("TO-1 + TO-2 + TO-3 all RAVC-closed") predates the 2026-05-22 TO-3
         DS/DE split: TO-3 was split into a DS-scope (DynamoDB FIRM#demo +
         USER#demo) and a DE-laned portal track. The operative gate for TO-4
         is TO-3 DS-scope, which is RAVC2-accepted (COO~C-validated:
         records verified in opal-users-v2; script 2ea34ba81 on origin/CLOUD).
         SCOPED GO: ACs 1,2,3,5,6,7,8 (EC2 one-shot transform + PII-leak scan
         + Sigma-identity reconcile) proceed now. AC4 (visual smoke across
         Advisor Intelligence surfaces AS THE DEMO USER) is DEFERRED to the
         post-DE verification track -- it needs the carved portal items
         (ROUTER_FIRM_SUFFIX, firmAccess.ts, _partners/demo/) live, and the
         ~C team has no DE lane yet. Surface the EC2 write-role need (cross-
         domain block) at Phase 1 -- AE~C is pre-warned. -->

    <project_code>ADVI_DEMOV1</project_code>
  </metadata>

  <objective>
    Phase 4 of ADVI_DEMOV1 — execute the transform and verify the demo tenant.
    Run the TO-2 transform engine as an EC2 one-shot to populate `opal-data-demo`
    from `opal-data-bd/platinum/**`; smoke-test every Advisor Intelligence surface
    as the demo user; and run the mandatory PII-leak scanner over the full demo
    bucket. This is the project's closing phase — it does NOT close until the
    leak scan passes clean.
  </objective>

  <context>
    ADVI_DEMOV1 PRD: docs/architecture/ADVI_DEMOV1.md (v0.1, 2e1321f79). Read §4
    rulings R5/R6, §6 TO-4, §7 risks.

    This TO consumes the outputs of TO-1 (bucket + routing live), TO-2 (transform
    engine built + dry-run reviewed), and TO-3 (FIRM#demo + demo Cognito user +
    portal entry). It is the last phase.

    CTO rulings that bind this TO:
    - R5 — MANDATORY PII-LEAK SCANNER GATES THIS PHASE. A post-run scanner asserts
      that NO real advisor name, NO real client name, and NO source `z`-ID from
      opal-data-bd appears anywhere in opal-data-demo — in content OR in S3 keys.
      Phase 4 does NOT close until the scan passes clean. This is the project's
      single most important gate: one missed field = real PII in the demo bucket.
    - R6 — The transform runs as an EC2 one-shot per the EC2 Code Deployment
      Standard (CLAUDE.md Rule 12: write locally -> upload to S3 -> EC2 pulls ->
      execute). No inline code on the VM. Use safe-ec2-deploy.sh; register the
      service in EC2_MANIFEST.json if it is a new service.
    - R4 (carried) — the real->fake mapping table the run produces is a
      re-identification key: it must NEVER be written to opal-data-demo, git,
      logs, or messages. Handle per TO-2's R4 implementation.

    Reconciliation constraint: the populated demo tree must preserve every
    Σ-identity (leaderboard -> firm headline; the identity_1 decomposition;
    per-window TWR/epsilon balances). Verbatim dollar handling is the default
    (ruling R7); if Andrew's Q1 answer selects a global scalar, the TO-2 config
    switch carries it — no code change here.

    GATING — this TO is staged. COO~C issues the GO only when TO-1, TO-2, and
    TO-3 are all RAVC-closed. The TO-0 PII inventory must be FINAL — the leak
    scanner's real-identifier list derives from it + the TO-2 mapping table.
  </context>

  <compiler_tools_mandate>
    Phase 1 — before the run:
      <run>comp-pii audit</run>
      <expect>Re-baseline the component-layer PII audit before the run — a
      reference point for the post-run leak scan.</expect>
      <if_mismatch>n/a — orientation baseline.</if_mismatch>

      <run>comp-pipescript deployed {transform engine} (or the EC2-runner parity check)</run>
      <expect>The EC2 runner has the committed TO-2 engine code — MATCH. The
      run must execute the committed, reviewed engine, not a stale copy.</expect>
      <if_mismatch>If STALE/MISSING, upload the committed engine to S3 and
      re-verify MATCH before running (the S3-pull dispatcher does not
      auto-propagate from a CLOUD push).</if_mismatch>

    Phase 2 — the PII-leak scanner IS the gate (ruling R5):
      <run>the mandatory PII-leak scanner over the full opal-data-demo bucket</run>
      <expect>ZERO hits — no real advisor name, no real client name, no source
      z-ID, in content or in any S3 key, anywhere in opal-data-demo.</expect>
      <if_mismatch>ANY hit BLOCKS closure. Do not smoke-sign-off, do not mark
      complete. Identify the missed field, fix the TO-2 engine, re-run the
      transform, re-scan. Escalate to COO~C if the miss implies a TO-0 inventory
      gap.</if_mismatch>

    Phase 3 — after the run + scan pass:
      <run>visual smoke across all Advisor Intelligence surfaces (biwndw001_visual_smoke.py harness as template)</run>
      <expect>Every surface renders for the demo user; every Σ-identity
      (leaderboard -> headline; identity_1) reconciles to the cent; no broken
      cross-references (a missed id-remap shows as a broken link).</expect>
      <if_mismatch>A broken link = a missed cross-reference in the transform
      (TO-2 R1 unmapped-id class); a broken Σ-identity = a value-handling defect.
      Fix the engine, re-run, re-verify.</if_mismatch>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - shared_resource: opal-data-demo S3 bucket — this TO is the ONLY writer.
      TO-1 created it empty + read-only-for-serving; this TO's EC2 run gets a
      scoped write role.
    - shared_resource: opal-data-bd/platinum/** — READ-ONLY source. The transform
      must never write to or mutate the real 49F bucket.
    - also_in_to: none — by Phase 4 all other DEMOV1 TOs are closed.
    - required_action: confirm the EC2 one-shot's IAM role has write on
      opal-data-demo + read on opal-data-bd, and NOTHING else. If the write role
      is missing, coordinate with the AE lane (it may need a TO-1 follow-up or a
      small grant) — flag to COO~C.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. The transform engine ran as an EC2 one-shot (ruling R6 / Rule 12 — S3
       artifact model, no inline VM code; safe-ec2-deploy.sh; EC2_MANIFEST.json
       registration if a new service).
    2. `opal-data-demo/platinum/**` is populated — object count matches the
       source platinum tree (per the TO-0 live manifest; ~22,253 objects modulo
       any intentional structural change), same prefix structure, re-keyed paths.
    3. THE PII-LEAK SCANNER PASSES CLEAN (ruling R5) — zero real advisor names,
       zero real client names, zero source z-IDs anywhere in opal-data-demo, in
       content AND in S3 keys. The scan output is attached to the session log.
       THIS GATES CLOSURE.
    4. Visual smoke across every Advisor Intelligence surface as the demo user:
       all surfaces render; no broken cross-reference links.
    5. Every Σ-identity reconciles: leaderboard totals -> firm headline; the
       identity_1 decomposition holds to the cent; per-window TWR/epsilon
       balances hold.
    6. The real->fake mapping table was NOT written to opal-data-demo, git, logs,
       or messages (ruling R4) — confirmed in the session log.
    7. The transform run did NOT write to or mutate opal-data-bd (the real 49F
       source) — confirmed.
    8. Session log with Compiler Tools section committed, including the leak-scan
       output and the Σ-identity reconciliation evidence.
  </acceptance_criteria>

  <scope>
    <files>
      <file action="reference">the TO-2 transform engine (executed, not modified)</file>
      <file action="create | modify">infra/aws/ec2/EC2_MANIFEST.json — register the one-shot transform service if new</file>
      <file action="create">the PII-leak scanner (if not already part of the TO-2 engine deliverable — confirm with TO-2 scope)</file>
      <file action="create">org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-05-21/advi_demov1_to4_run_verify~C.md</file>
      <file action="reference">biwndw001_visual_smoke.py (smoke-test harness template)</file>
      <file action="reference">docs/deployment/EC2_CODE_DEPLOYMENT_STANDARD.md, EC2_DEPLOYMENT_PROTOCOL.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Run the transform as an EC2 one-shot (R6) — S3 artifact
    flow, no inline VM code, safe-ec2-deploy.sh, EC2_MANIFEST.json registration.</requirement>
    <requirement id="2">The PII-leak scanner (R5) is the closure gate — clean
    pass is mandatory and non-negotiable; any hit blocks the project.</requirement>
    <requirement id="3">Verify referential integrity (no broken links) and every
    Σ-identity reconciliation in the populated demo tree.</requirement>
    <requirement id="4">The mapping table never lands in opal-data-demo / git /
    logs / messages (R4).</requirement>
    <requirement id="5">The transform reads opal-data-bd strictly read-only —
    never writes or mutates the real 49F source.</requirement>
    <requirement id="6">RAVC2 completion to COO~C with the leak-scan output, the
    smoke results, and the reconciliation evidence — this RAVC closes Phase 4 and
    triggers project closure review.</requirement>
  </requirements>

  <deliverables>
    <deliverable type="document">opal-data-demo populated + verified; the PII-leak scan output (clean)</deliverable>
    <deliverable type="document">Visual smoke results across all Advisor Intelligence surfaces + Σ-identity reconciliation evidence</deliverable>
    <deliverable type="commit">EC2_MANIFEST.json + the leak scanner committed to CLOUD</deliverable>
    <deliverable type="document">Session log with Compiler Tools section (leak-scan output attached)</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT mark Phase 4 / this TO complete while the PII-leak scanner shows
    ANY hit — a clean scan is the non-negotiable closure gate (ruling R5).</rule>
    <rule>Do NOT write to or mutate opal-data-bd — the real 49F bucket is a
    read-only source.</rule>
    <rule>Do NOT write the mapping table anywhere it could leak — not the demo
    bucket, not git, not logs, not messages (ruling R4).</rule>
    <rule>Do NOT run the transform inline on the VM or inline-Python in an SSM
    command — EC2 one-shot via the S3 artifact model only (Rule 12 / R6).</rule>
    <rule>Do NOT begin before COO~C issues the GO (gated on TO-1 + TO-2 + TO-3
    all RAVC-closed, and the TO-0 PII inventory FINAL). This TO is staged.</rule>
  </do_not>
</task_order>
