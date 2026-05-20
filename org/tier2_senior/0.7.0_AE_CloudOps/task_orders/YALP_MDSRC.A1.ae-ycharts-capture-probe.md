<task_order>
  <metadata>
    <id>YALP_MDSRC.A1</id>
    <slug>ae-ycharts-capture-probe</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <date>2026-05-20</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO FIRED 2026-05-20 — PRD v0.3 confirmed on origin/CLOUD (de7facf93 + c3c04bc9d); COO flipped pending + dispatched. Original: STAGED — Phase 2A. Q1-INDEPENDENT (dispatchable on COO decomposition per PRD v0.3 §7/§12 — runs regardless of the Q1 official-API-vs-scrape decision; its result feeds the scrape branch if Q1 picks scrape). COO flips status->pending + fires the GO once PRD v0.3 (commit de7facf93) is confirmed on origin/CLOUD — so the runner pulls a v0.3 PRD, not v0.2. No Andrew gate.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P2 — Phase 2A unblock. Cheap, fast; de-risks the Q1=scrape branch by answering empirically whether headless capture is viable.</priority>
    <sla>~1 day. External-system probe.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.3 (the implementation charter). This TO = §7 Phase 2A TO-A1. Read §3.1 (YCharts cookie-session + WAF), §6.1 (the WS-4 operational pattern), §6.3 (the official-API recommendation).</prd>
    <ws4_brief>docs/briefs/mdsrc-ws4-ycharts-operational-pattern-20260520.md — WS-4 design; Branch A (headless Playwright) vs Branch B (attended fallback) capture mechanism.</ws4_brief>
  </references>

  <context>
    YALP_MDSRC PRD v0.3 charters the portal market-data sourcing migration. The YCharts integration's capture mechanism has two designed branches (WS-4): Branch A = headless Playwright solving the AWS WAF JS-challenge; Branch B = attended capture fallback. This probe answers empirically WHICH branch is viable, so the Phase 2C build (TO-C1) is scoped against fact, not assumption. Q1-independent: if Andrew picks the official YCharts Data API, the capture mechanism is moot — but the probe is cheap and runs regardless so the scrape fallback is fully de-risked.
  </context>

  <scope>
    <in_scope>
      - Run Playwright headless against the YCharts login flow once. Determine empirically: does the AWS WAF JS-challenge clear under headless automation (Branch A viable) or is an attended/real-browser capture required (Branch B)?
      - Measure the `ycsessionid` `Set-Cookie` `Max-Age` (and any other session-cookie TTLs) on a successful login — this sizes the WS-4 refresh-cron cadence.
      - Record the WAF challenge behavior observed (challenge type, whether the awswaf token solve is scriptable).
      - Deliverable: a short probe-result brief — Branch A vs Branch B verdict + the cookie TTL finding + cron-cadence implication.
    </in_scope>
    <out_of_scope>
      - NO integration build — that is TO-C1 (Phase 2C). This is a probe only.
      - NO code/Terraform/Lambda deploy — throwaway probe script only.
      - The official-API path (Q1) — not this TO; the probe informs the scrape branch only.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="1" when="before the probe">
      <step>
        <run>(none) — YCharts is an external system, not in the comp-graph; the probe is throwaway test code, not a pipeline script.</run>
        <expect>Documented-none per PRD §10 honest-scope note. Evidence base is the live Playwright probe.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="2" when="before commit">
      <step>
        <run>(none) — probe-result brief, no production code.</run>
        <expect>No py_compile / ruff gate applies.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="3" when="after commit">
      <step>
        <run>(none) — the Branch-A/B verdict IS the deliverable's self-validation.</run>
        <expect>Checked by AC1/AC2.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    The Branch-A/B verdict + cookie-TTL finding feed TO-C1 (YALP_MDSRC.C1, YCharts credential pipeline — your own lane) if Q1 resolves to session-scrape. No shared files. No other coordination.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Empirical verdict: does headless Playwright clear the AWS WAF challenge (Branch A viable) or is attended capture required (Branch B)? Answered yes/no with evidence (the observed WAF behavior).</ac>
    <ac id="AC2">The `ycsessionid` (and other session-cookie) `Set-Cookie Max-Age` measured on a live login; the implied WS-4 refresh-cron cadence stated.</ac>
    <ac id="AC3">Deliverable is a committed probe-result brief (e.g. docs/briefs/mdsrc-ycharts-capture-probe-20260520.md). Session log with a Compiler Tools section (documented-none rationale). RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The capture-probe result brief (Branch A/B verdict + cookie TTL + cron implication).
    - Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>Do NOT build the integration — probe only; the build is TO-C1.</rule>
    <rule>Do NOT handle any YCharts credential in chat/MCP/git/logs — if the probe needs a login, read from Secrets Manager `ycharts/credentials` at runtime (the secret YALP_MDSRC.006 stood up).</rule>
    <rule>No emojis in the brief, the probe script, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
