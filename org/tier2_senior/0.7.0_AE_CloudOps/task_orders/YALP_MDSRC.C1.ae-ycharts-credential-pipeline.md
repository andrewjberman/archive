<task_order>
  <metadata>
    <id>YALP_MDSRC.C1</id>
    <slug>ae-ycharts-credential-pipeline</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-20</date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_unblock_condition>STAGED — Phase 2C. GATED on the Andrew Q1 (official YCharts Data API vs session-scrape) + Q7 (ToS) business calls (PRD v0.3 §8). The TO's scope BRANCHES on Q1 — see &lt;scope&gt;. COO finalizes the scope to the chosen branch + flips status->pending + fires the GO once Andrew rules Q1 (and Q7 if Q1=scrape). Also requires PRD v0.3 on origin/CLOUD. CTO recommendation (PRD §6.3): official API.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — Phase 2C. The YCharts credential/auth pipeline the market-data pull (TO-C2) depends on.</priority>
    <sla>~2-3 days (Q1=official API) or ~5-8 days (Q1=session-scrape, + the dedicated-seat dependency) — PRD §7.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3. This TO = §7 Phase 2C TO-C1. Read §6.1 (the WS-4 operational pattern), §6.3 (official-API recommendation), §8 (Q1/Q7).</prd>
    <ws4_brief>docs/briefs/mdsrc-ws4-ycharts-operational-pattern-20260520.md — the full WS-4 §4 scrape-pattern design + §7 official-API footprint.</ws4_brief>
    <probe>YALP_MDSRC.A1 — the capture probe; its Branch-A/B verdict + cookie-TTL finding feed the scrape branch of this TO.</probe>
  </references>

  <context>
    YALP_MDSRC PRD v0.3 §6 — the YCharts integration needs a credential/auth pipeline before the market-data pull (TO-C2) can run. The shape depends entirely on the Andrew Q1 decision (official API vs session-scrape), so this TO is GATED on Q1 and its scope branches. CTO recommendation (§6.3): the official API — it eliminates the single-session eviction risk, the WAF, the capture EC2, the freshness gate, the refresh Lambda, and the dedicated-seat procurement.
  </context>

  <scope>
    <in_scope>
      BRANCH A — if Q1 = OFFICIAL YCHARTS DATA API (CTO-recommended): the key-auth path. A `ycharts/api/key` Secrets Manager secret + the resource-scoped GetSecretValue grant + a thin call-failure CloudWatch alarm (WS-4 §7 — the collapsed footprint). No capture EC2, no freshness gate, no refresh Lambda. ~2-3 days.
      BRANCH B — if Q1 = SESSION-SCRAPE (the designed fallback; requires Q7 ToS cleared + a dedicated YCharts seat provisioned): the full WS-4 §4 pattern — the capture mechanism (Branch A/B per the YALP_MDSRC.A1 probe), the `ycharts/session/current` secret, `cookie_freshness.py` (the active authenticated-probe freshness gate), the `ycharts-session-trigger` refresh Lambda, the `YCharts/SessionResilience` CloudWatch namespace + the `ycharts-session-evicted` alarm, the daily pre-emptive cron. ~5-8 days.
      COO finalizes this TO to the chosen branch at dispatch (post-Q1). Until then both branches are documented; the agent does NOT pre-build.
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
    <ac id="AC3">Branch A: the `ycharts/api/key` secret + call-failure alarm live. Branch B: the full WS-4 §4 pattern live (capture / session secret / freshness gate / refresh Lambda / CW + evicted alarm / cron) — and the dedicated-seat dependency confirmed satisfied.</ac>
    <ac id="AC4">Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The Q1-branch YCharts credential pipeline, Terraform-deployed.
    - Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT start before Andrew rules Q1 (and Q7 if Q1=scrape) — the scope branches on it; pre-building the wrong branch is wasted work.</rule>
    <rule>Do NOT handle a YCharts credential value in chat/MCP/git/tfstate/logs — secret values via put-secret-value, out of Terraform state.</rule>
    <rule>Terraform-only deploy. No emojis in code, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
