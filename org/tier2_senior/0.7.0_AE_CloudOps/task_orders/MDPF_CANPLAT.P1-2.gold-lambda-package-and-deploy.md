<task_order>
  <metadata>
    <id>2.0.0_SA_COO~Z-2026-08-07-canplat-p1-2</id>
    <issued_by>2.0.0_SA_COO~Z</issued_by>
    <issued_to>0.7.0_AE_CloudOps~Z</issued_to>
    <date>2026-08-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: closed WITH its project MDPF_CANPLAT, which was closed the same day for having no directive attachment. Closed as a record act, not a work verdict; the work is recoverable by re-minting the project. Prior status: staged</status>
    <go_condition>GO fires from 2.0.0_SA_COO~Z when DS~Z closes MDPF_CANPLAT.P1-1 with its module list + pinned commit + QA evidence (RAVC-4). Reading/design against @d136d5bb1 may begin any time; NO package build against an unclosed P1-1 commit — the modules may still move.</go_condition>
    <project_code>MDPF_CANPLAT</project_code>
    <supersedes>none — this is the seat the prior generation never authored (P2-1 deferred input-read grants + the adjacency exercise "to P1-2"; this is that TO)</supersedes>
    <governing>PRD @24d3eb2f8 · CONTRACT @a3106d585 §A (A2 schedule oracle, A6 manifest fields, A7 preserved contract) · adopted packaging law: MDPF_CANRTE.P1-1 @a6ae64326 "PACKAGING" + cross-domain sections</governing>
  </metadata>

  <standing_instruction>
    ⛔ PRD §0 BINDS, VERBATIM FORCE (full text in your P0-2R/P2-1/P3-1 set @f123fbf6e): BUILD WHAT IS
    DESCRIBED, DO NOT HUNT ERRORS. A number that surprises you is not a finding. SURPRISE channel: one
    line to 2.0.0_SA_COO~Z, subject `SURPRISE:`, then continue.
  </standing_instruction>

  <objective>
    Package and deploy `mdpf-gold-lambda` from DS~Z's closed P1-1 commit: the built artifact, its
    BUILD_MANIFEST, the Lambda + schedule Terraform, and the deferred input-read IAM — so the one
    firm-parameterized gold path RUNS ON THE 09:00 ET SCHEDULED FLOOR (A2) and emits the A4 grammar the
    publisher and comparator consume.
  </objective>

  <requirements>
    <requirement id="1">PACKAGING LAW (adopted @a6ae64326, binding): FLAT vendoring, both gold trees in
    ONE namespace at zip root; roster as build-generated hash-tied copy at /var/task/partner_roster.json
    (NO S3 read leg — symmetric with the publisher ruling); runtime **python3.11 (hard ABI pin, NOT
    3.12)**, x86_64; repo files are source of truth, NEVER edit a zip; `pandas_market_calendars<5` in the
    package (an import-health pass is NOT evidence — the import sits in try/except; assert
    `calendar_source()` per A9).</requirement>
    <requirement id="2">BUILD_MANIFEST: DS~Z supplies module PATHS + a COMMIT; YOU compute hashes from
    the repo files at build — a hash supplied by hand and a hash computed from the artifact are
    different claims and only the second is a control. Record both config hashes (route_bindings sha256
    from P2-1's object metadata; roster copy hash) — these are the A6/D7 manifest fields P2-1 minted.</requirement>
    <requirement id="3">SCHEDULE = A2's ORACLE, VERBATIM: "Fires on the 09:00 ET scheduled floor. The
    INF completion marker may accelerate; it is never the only trigger." `ScheduleExpression` present +
    non-null, ET-anchored (EventBridge Scheduler with TZ America/New_York — the SmartX precedent, NOT a
    UTC classic rule). A pipeline whose only trigger is another pipeline's success has no schedule and
    is a defect (CLAUDE.md standing).</requirement>
    <requirement id="4">INPUT-READ IAM (deferred from P2-1 by design): grants for the read set DS~Z's
    closed module list actually consumes — Rule 22a discipline: one --resource-arns per simulate call,
    positive controls in SEPARATE invocations, accessanalyzer validate-policy on action names. The
    operation list from comp-iam is a FLOOR, never a deletion warrant.</requirement>
    <requirement id="5">P2-1 CARRY-INS LAND HERE: the criterion-3 adjacency exercise runs FROM THE BUILT
    ARTIFACT (both roster readers fail closed, one test per reader, from the artifact not the repo);
    criterion-6's manifest emission is exercised on a real invocation.</requirement>
    <requirement id="6">A7 UNTOUCHED: `gold/mdpf_revamp/_aggregate_aua/{date}.json` keeps being written
    by the deployed path (name SEQUESTERED, deliberate and current); the daily-emitter re-point is NOT
    this TO — DEPLOY BEFORE ENV binds whenever that later act happens.</requirement>
    <requirement id="7">DEPLOY MECHANICS: Terraform only (safe-apply, HALT_ACK as needed); commit before
    apply; source map updated; full un-targeted plan zero-diff post-apply (R13); tag + push --follow-tags
    is MSTR~Z's window; `comp-pipescript deployed` MATCH after upload; Lambda resources sized
    deliberately (never yang-lambda 256MB/30s defaults on a data-processing Lambda).</requirement>
    <requirement id="8">AD-HOC QA RUN legal and expected (run-and-read, nothing standing): one invocation
    proving A4 keys + A6 manifest + A8 idempotency (double-fire → `unchanged`), read by CVO~Z's
    instruments as P1-1 candidates. AD-HOC ARTIFACTS ARE NEVER PRODUCTION EVIDENCE — the rubric ticks on
    the scheduled cycle only.</requirement>
  </requirements>

  <cross_domain_coordination>
    <shared_resource>DS~Z's closed module list + commit (the package input)</shared_resource>
    <also_in_to>MDPF_CANPLAT.P1-1</also_in_to>
    <required_action>Package EXACTLY the closed commit. Any module move after close = DS~Z re-closes,
    you re-pin. MCP DS~Z on the roster-copy build mechanics (both components hash the SAME committed
    authority — the gold-hash != publisher-hash comparison is the divergence detector).</required_action>
    <shared_resource>A4 keys + G2 baseline</shared_resource>
    <also_in_to>MDPF_CANPLAT.G2 (CVO~Z consumes QA output as candidates) · P3-1 (GO condition completes when A4 emits)</also_in_to>
    <required_action>Tell CVO~Z + COO~Z when the first A4 QA emission exists. That emission is what
    flips P3-1's GO second half.</required_action>
  </cross_domain_coordination>

  <do_not>
    <rule>NO package build before P1-1 closes (GO condition). NO deploy before commit; no bare apply.</rule>
    <rule>NO alarms/SNS/SES/monitors. NO shadow paths or standing comparators. NO served-key writes.</rule>
    <rule>DO NOT re-point the daily emitter or retire the bridge/EC2 — separate acts, later, on evidence.</rule>
    <rule>NO error-hunting (§0). SURPRISE: line, then continue. Commit to your lane; push is MSTR~Z's.</rule>
  </do_not>

  <deliverables>
    <deliverable type="commit">Package build script/TF + BUILD_MANIFEST + source-map update, committed to your lane</deliverable>
    <deliverable type="document">Deploy evidence: 0-diff plan, deployed MATCH, simulate battery, adjacency exercise from the artifact, QA-run read (A4 keys + manifest + idempotency)</deliverable>
    <deliverable type="document">Session log with a Compiler Tools section</deliverable>
  </deliverables>
</task_order>
