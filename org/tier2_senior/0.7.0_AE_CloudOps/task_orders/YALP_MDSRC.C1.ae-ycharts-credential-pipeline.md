<task_order>
  <metadata>
    <id>YALP_MDSRC.C1</id>
    <slug>ae-ycharts-credential-pipeline</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <completed>2026-05-22</completed>
    <!-- CLOSE 2026-05-22 (0.7.0_AE_CloudOps): the internal-API session/credential pipeline is deployed. ycharts-session-capture container-image Lambda built (Lambda-compatible single-manifest) + pushed to ECR; terraform apply 9-add/1-change, 0-diff replan PASS; tag ycharts-pipeline-v1.1.0. Deployed DORMANT -- EventBridge schedule DISABLED, 0 invocations, no live YCharts call (freeze respected). Probe wired to invoke capture on 403. ycharts/session/current created (capture output); ycharts/credentials = login input. Go-live gated on the dedicated-seat creds (Andrew procurement). RAVC2 sent. Session log: logs/2026-05-22/c1_ycharts_capture_pipeline_deploy.md. -->

    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — Andrew ruled Q1 (2026-05-20): integrate YCharts by reverse-engineering its internal JSON API, authenticated with the YCharts web session — NOT an official API key. Branch A (official-API key-auth) is RETIRED. Q7 (ToS) folded into the Q1 ruling per Andrew's directive. The build spec is committed: A3 P2 (the auth/session model) in docs/briefs/mdsrc-ycharts-internal-api-20260520.md (af5102dd3, origin/CLOUD). COO has finalized the scope to the chosen branch (see &lt;scope&gt;). 0.7.0_AE_CloudOps owns it — sequence behind F2-P1 / F5; GO on pickup.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — Phase 2C. The YCharts credential/auth pipeline the market-data pull (TO-C2) depends on.</priority>
    <sla>~2-3 days (Q1=official API) or ~5-8 days (Q1=session-scrape, + the dedicated-seat dependency) — PRD §7.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3. This TO = §7 Phase 2C TO-C1. Read §6.1 (the WS-4 operational pattern), §6.3 (official-API recommendation), §8 (Q1/Q7).</prd>
    <ws4_brief>docs/briefs/mdsrc-ws4-ycharts-operational-pattern-20260520.md — the full WS-4 §4 scrape-pattern design + §7 official-API footprint.</ws4_brief>
    <probe>YALP_MDSRC.A1 — the capture probe; its headless-WAF verdict + cookie-TTL findings + the bun/Playwright runtime-gap feed C1's capture/refresh design.</probe>
    <a3_p2_build_spec>docs/briefs/mdsrc-ycharts-internal-api-20260520.md (A3 P1+P2, af5102dd3, origin/CLOUD) — THE C1 BUILD SPEC. P2 is the empirically-reverse-engineered auth/session model: the credential bundle, the headers, the WAF behavior, the cookie TTLs, the active-probe freshness gate, the rate-limit status. Build C1 against A3 P2 — it supersedes the generic WS-4 §4 design where they differ.</a3_p2_build_spec>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED) — C1 is the credential pipeline for an INTEGRATION against YCharts' internal API. Terminology: "reverse engineer" / "integrate", never "scrape". §3 step 2 — the YCharts session credential binds to AWS Secrets Manager.</standard>
  </references>

  <context>
    YALP_MDSRC PRD v0.3 §6 — the YCharts integration needs a credential/auth pipeline before the market-data pull (TO-C2) can run. The shape depends entirely on the Andrew Q1 decision (official API vs session-scrape), so this TO is GATED on Q1 and its scope branches. CTO recommendation (§6.3): the official API — it eliminates the single-session eviction risk, the WAF, the capture EC2, the freshness gate, the refresh Lambda, and the dedicated-seat procurement.
  </context>

  <scope>
    <in_scope>
      FINALIZED (COO, post-Q1, 2026-05-20) — the internal-API session/credential pipeline. Andrew ruled Q1 = reverse-engineer the YCharts internal JSON API, which the web app authenticates with a YCharts session (cookie bundle), NOT an official API key. Branch A (official-API key-auth) is RETIRED — not chosen. Build the session/credential pipeline that lets the TO-C2 internal-API pull authenticate, per the A3 P2 auth/session model (af5102dd3) — A3 P2 is the canonical, empirically-reverse-engineered build spec; it supersedes the generic WS-4 §4 design where they differ. Scope:
      - SESSION CREDENTIAL SECRET: the YCharts session cookie bundle in AWS Secrets Manager. NOTE: `ycharts/credentials` already holds an Alyssa cookie-bundle capture (per A1 / A3 P2) — Phase 0: confirm whether C1 reuses/renames that secret or stands up `ycharts/session/current`; do NOT duplicate the secret.
      - FRESHNESS GATE: per A3 P2's documented freshness check — an ACTIVE authenticated probe, not a stored-timestamp check (A1 measured aws-waf-token ~96h TTL, ycsessionid a server-side session cookie).
      - CAPTURE / REFRESH MECHANISM: a headless capture (A1 confirmed headless Chromium clears the AWS WAF JS-challenge) that refreshes the session secret on a pre-emptive cadence. CRITICAL per A1's runtime-gap finding: Playwright launch()/connectOverCDP() HANG under bun on this host — C1's production capture MUST run on a real Node runtime (a Lambda Node image, or Node on a capture EC2) or the raw-CDP approach. Do not assume a bun runtime works.
      - WAF HANDLING per A3 P2 — the awswaf SDK engages on app pages (not the login page); the capture must navigate to an app page to acquire the aws-waf-token.
      - CLOUDWATCH: a session-eviction / call-failure alarm so a dead session surfaces fast.
      - IAM: the resource-scoped GetSecretValue grant on the session secret, least-privilege.
      SEAT COORDINATION: YCharts is single-concurrent-session. While A3 (0.1.0_DS) is still running, it holds the YCharts seat — C1's automated capture/refresh must NOT evict A3's live session. By the time C1 dispatches (behind F2-P1/F5) A3 may be complete; confirm the seat is free, or coordinate the capture window with 0.1.0_DS before running a live refresh.
    </in_scope>
    <out_of_scope>
      - The market-data pull itself — TO-C2.
      - The Q1/Q7 decisions — Andrew's calls; this TO consumes the outcome.
      - The yang cutover — TO-D1.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the build">
      <step>
        <run>comp-iam service &lt;the new YCharts credential lambda/role&gt;</run>
        <expect>The new boto3 surface enumerated (Secrets Manager always; + Lambda/EC2-role/CloudWatch/S3 on Branch B per WS-4 §6) — confirm the grants needed before authoring iam.tf.</expect>
        <if_mismatch>If a node is not yet in the graph, fall back to a direct WS-4 §6 enumeration + document.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="after the iam.tf change">
      <step>
        <run>comp-iam gaps</run>
        <expect>0 new IAM gaps from the YCharts credential pipeline.</expect>
        <if_mismatch>Resolve the flagged gap in iam.tf before apply.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after deploy">
      <step>
        <run>comp-routes behaviors  (only if a serving path changed)</run>
        <expect>No unintended serving-path / CF behavior change. (Branch A/B credential pipeline normally touches no serving path — confirm.)</expect>
        <if_mismatch>If a serving path moved, RAVC2 COO before declaring done.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Consumes the YALP_MDSRC.A1 capture-probe verdict (scrape branch only). Feeds TO-C2 (the market-data pull authenticates via this pipeline). Terraform-only deploy (CLAUDE.md Rule 1). If Q1=scrape, the dedicated-seat provisioning is an Andrew/procurement dependency — confirm it is in place before the capture mechanism is built.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">The credential pipeline for the Q1-chosen branch is built + Terraform-deployed (plan -> apply -> 0-diff replan -> tag -> push --follow-tags -> record-terraform-deploy).</ac>
    <ac id="AC2">comp-iam gaps shows 0 new gaps after the iam.tf change; the credential secret's GetSecretValue grant is resource-scoped + least-privilege.</ac>
    <ac id="AC3">The internal-API session/credential pipeline live, built per A3 P2: the session-credential secret (reuse-or-rename decision documented), the active-probe freshness gate, the headless capture/refresh on a confirmed-working Node runtime (not bun), the WAF handling, the session-eviction CloudWatch alarm. The single-session seat coordination with A3/0.1.0_DS confirmed before any live refresh.</ac>
    <ac id="AC4">Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The Q1-branch YCharts credential pipeline, Terraform-deployed.
    - Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Q1 is RULED — build the internal-API session branch only; do NOT build Branch A (official-API key-auth) — it is retired.</rule>
    <rule>Do NOT run a live YCharts capture/refresh that evicts A3/0.1.0_DS's session — YCharts is single-concurrent-session; confirm the seat is free or coordinate the window first.</rule>
    <rule>Do NOT assume a bun runtime for the capture — A1 proved Playwright hangs under bun; use a real Node runtime or raw-CDP.</rule>
    <rule>Do NOT handle a YCharts credential value in chat/MCP/git/tfstate/logs — secret values via put-secret-value, out of Terraform state.</rule>
    <rule>Terminology: "reverse engineer" / "integrate", never "scrape" (Third-Party Data Integration Standard). Terraform-only deploy. No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
