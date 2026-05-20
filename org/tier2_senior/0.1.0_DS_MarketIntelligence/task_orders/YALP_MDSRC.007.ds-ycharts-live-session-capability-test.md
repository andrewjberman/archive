<task_order>
  <metadata>
    <id>YALP_MDSRC.007</id>
    <slug>ds-ycharts-live-session-capability-test</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.1.0_DS_MarketIntelligence</issued_to>
    <date>2026-05-20</date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO NOW — Andrew-direct via CTO, urgent (YCharts seat currently free; Alyssa signed out). Phase 0 (runner prep) starts immediately, in parallel with YALP_MDSRC.006. Phase 1 (the live test) has ONE in-TO gate: the `ycharts/credentials` secret must be populated by Andrew out-of-band — proceed to Phase 1 the moment that is confirmed.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 urgent — time-boxed to the YCharts seat-free window. Run the live test promptly once the credential lands; the seat may not stay free.</priority>
    <sla>~1-2h once the credential is populated. Phase 0 prep can run now.</sla>
  </metadata>

  <references>
    <prd>docs/architecture/YALP_MDSRC.md — PRD v0.2. This TO = a Phase-0 capability-test follow-on (CTO dispatch ask 2026-05-20, Andrew-direct). WS-1 lane — you already did the HAR/live-probe capture.</prd>
    <ws1_brief>docs/briefs/mdsrc-ws1-external-market-data-audit-20260520.md — your WS-1 audit; the endpoint inventory this test exercises.</ws1_brief>
    <pairs_with>YALP_MDSRC.006 (AE 0.7.0) — creates the `ycharts/credentials` Secrets Manager secret + the GetSecretValue IAM grant this test consumes.</pairs_with>
    <recon_doc>docs/briefs/ycharts-bloomberg-portal-data-sourcing-audit-20260520.md (3987616d8) — the recon doc-of-record.</recon_doc>
  </references>

  <context>
    Andrew freed the YCharts seat (the single-concurrent-session constraint — WS-1 Finding F1 — is clear for a one-off live test) and wants a real authenticated-session test against YCharts now, while the seat is free. This TO runs that test: authenticate with the real account credentials (read from Secrets Manager — never handled in chat/git), capture the session cookie bundle, and pull the key portal-relevant endpoints to confirm real data returns end-to-end.

    SCOPE CAVEAT — DO NOT OVER-READ THE RESULT (carry into the brief verbatim): this test validates the scrape path TECHNICALLY (can an authenticated session pull the data). It does NOT make a shared-seat scrape the production answer. WS-4's single-concurrent-session finding stands — production still requires a dedicated automation seat or the official YCharts API (Q1, an Andrew call). A PASS here means "the scrape path technically works," NOT "shared-seat scrape is production-viable."
  </context>

  <scope>
    <in_scope>
      Phase 0 (runner prep — start NOW, parallel with YALP_MDSRC.006):
      - Prepare the live-test runner: the auth + cookie-capture + endpoint-pull script, reading the credential from Secrets Manager `ycharts/credentials` at runtime (NOT hardcoded, NOT from any file in git).
      - MCP AE 0.7.0 (YALP_MDSRC.006) the exact runner IAM principal so AE scopes the GetSecretValue grant to it.
      Phase 1 (the live test — gated on the secret being populated by Andrew):
      - Authenticate to YCharts with the account credentials; capture the session cookie bundle (ycsessionid + csrftoken + aws-waf-token + any required headers).
      - Pull the key portal-relevant endpoints and confirm real data returns: `/indices/table_data`, `/charts/fund_data.json`, `/model_portfolios/*`, and the `static.ycharts.com/calculations/all_calc_menu.json` catalog. Record HTTP status, response shape, row/record counts, a data sanity check.
      - Time-box to the seat-free window. If the seat is reclaimed mid-test (403 "signed out due to concurrent sign in"), record how far the test got and stop — partial is fine, surface it.
    </in_scope>
    <out_of_scope>
      - NO production capture mechanism build — that is the WS-4 design, a v0.3 implementation TO.
      - NO code/Terraform/portal change beyond the throwaway test runner.
      - Do NOT decide Q1 (official API vs scrape) — this test is one input.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <phase id="0" when="runner prep / before the test">
      <step>
        <run>(none) — YCharts is an external system, not in the comp-graph; the test runner is throwaff test code, not a pipeline script.</run>
        <expect>Documented-none per PRD §5 honest-scope note. Evidence base is the live HTTP capture.</expect>
        <if_mismatch>N/A.</if_mismatch>
      </step>
    </phase>
    <phase id="1" when="the live test">
      <step>
        <run>Live authenticated pull of /indices/table_data, /charts/fund_data.json, /model_portfolios/*, all_calc_menu.json</run>
        <expect>HTTP 200 with real data on each; record status + shape + counts. A 403 mid-run = the seat was reclaimed — record + stop, partial is acceptable.</expect>
        <if_mismatch>Auth fails / WAF blocks / 403 throughout -> record the exact failure mode (it is itself a finding for Q1/Q3) and surface to COO.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    MCP AE 0.7.0 (YALP_MDSRC.006) with the exact test-runner IAM principal so the GetSecretValue grant is scoped to it. The credential VALUE is placed by Andrew out-of-band — you read it from Secrets Manager at runtime; you never receive it via MCP/chat and never write it to git or a log. No shared files.
  </cross_domain_coordination>

  <acceptance_criteria>
    <ac id="AC1">Test runner reads the YCharts credential from Secrets Manager `ycharts/credentials` at runtime — credential never appears in source, git, logs, or any MCP message.</ac>
    <ac id="AC2">Live authenticated session established; the cookie bundle (ycsessionid + csrftoken + aws-waf-token + headers) captured and characterized.</ac>
    <ac id="AC3">The 4 endpoint classes pulled (/indices/table_data, /charts/fund_data.json, /model_portfolios/*, all_calc_menu.json) with HTTP status + response shape + record counts + a data sanity check recorded. Partial result acceptable if the seat is reclaimed mid-test — document how far it got.</ac>
    <ac id="AC4">Result brief committed (e.g. docs/briefs/mdsrc-ycharts-live-session-test-20260520.md) — the technical PASS/PARTIAL/FAIL verdict, WITH the scope caveat verbatim (technical validation only; not a production-architecture verdict; WS-4 single-session finding + Q1 stand). Session log + RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.</ac>
  </acceptance_criteria>

  <deliverables>
    - The live-session test result brief (technical verdict + the scope caveat verbatim).
    - Session log with Compiler Tools section. RAVC2 to 2.0.0_SA_COO + CC 1.0.0_SA_CTO.
  </deliverables>

  <do_not>
    <rule>NEVER handle the YCharts credential in chat, MCP, git, or logs — read it from Secrets Manager at runtime only. The credential VALUE is Andrew's out-of-band placement.</rule>
    <rule>Do NOT over-read a PASS — a technical PASS is NOT a production-viability verdict. WS-4's single-session finding stands; Q1 is unresolved. State this in the brief.</rule>
    <rule>Do NOT build the production capture mechanism — throwaway test runner only.</rule>
    <rule>No emojis in the brief, the test runner, the session log, or CLI transcripts (ASCII-only).</rule>
  </do_not>
</task_order>
