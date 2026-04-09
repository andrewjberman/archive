<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-08</date>
    <status>pending</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>1</wave>
    <phase>P1</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~A" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Write D_04.client_portal_summary.py -- the platinum layer publisher for the Books tab.
    This script reads gold/ outputs and writes pre-sliced JSON to platinum/ in S3 for all
    4 drill levels: N1 firm, L2 advisor, L3 client, L4 account. Plus ClientDetail panel
    feeds (mix_timeseries, concentration). ~5,300 files total.
  </objective>

  <context>
    The platinum layer introduces a hard boundary between analytical outputs (gold/) and
    portal-serving outputs (platinum/). Today the Books tab fires 4-5 fetches per drill level
    pulling full analytical datasets. D_04 consolidates these into pre-sliced JSONs served
    directly via S3/CloudFront.

    PRD: docs/architecture/ADVI_49PUSH_P1_PRD.md (read the FULL PRD -- it contains the
    complete fetch map, target state, input sources, processing logic, and number consistency
    principle).

    CRITICAL DESIGN CONSTRAINT -- Number Consistency Principle:
    All platinum files for a given entity must derive from the same gold source row for any
    shared metric. Firm total_aua = sum of advisor total_aua = sum of client total_aua.
    Compute TOP-DOWN: firm totals first, then advisors as partitions, then clients as
    partitions of advisors.

    Reference docs (read before writing):
    - docs/briefs/data-scientist-D_04-client-portal-summary-spec.md (if exists)
    - docs/briefs/data-scientist-platinum-layer-architecture-strategy.md (if exists)
    - data/black_diamond/scripts/gold/D_03.composition_artifacts.py (pattern for S3 writes)
    - data/black_diamond/scripts/gold/D_00.portal_aggregates.py (source of employee_leaderboard, clients_tab)
  </context>

  <compiler_tools_mandate>
    BEFORE writing any code, you MUST run these comp-* commands to understand the full
    dependency chain. Do NOT skip this step. Do NOT use Explore agents.

    1. comp-trace D_00 --all
       -- lists all D_00 function nodes + their S3 write targets (your input sources)

    2. comp-trace D_03 --all
       -- lists all D_03 function nodes + their S3 write targets

    3. comp-trace employee_leaderboard --direction up --all
       -- traces where employee_leaderboard data originates

    4. comp-trace clients_tab --direction up --all
       -- traces clients_tab origin

    5. comp-trace firm_mix_views --direction up --all
       -- traces mix data origin

    6. comp-trace C_06 --all
       -- lists all C_06 function nodes + their S3 write targets (you read these)

    7. comp-trace C_08 --all
       -- lists all C_08 function nodes + fee efficiency outputs

    8. comp-blast build_employee_leaderboard
       -- blast radius from the specific D_00 builder you consume

    9. comp-blast employee_leaderboard
       -- blast radius from the S3 artifact -- shows all current consumers

    THEN use comp-pipescript for authoritative script-level I/O (AST-parsed, not regex):

    10. comp-pipescript io D_00
        -- every S3 key D_00 reads and writes, with upstream writers and downstream consumers

    11. comp-pipescript io D_02
        -- D_02 I/O manifest (source of advisor books, client details)

    12. comp-pipescript io D_03
        -- D_03 I/O manifest (source of compositions, mix views)

    13. comp-pipescript io C_06
        -- C_06 I/O manifest (source of client mix timeseries)

    14. comp-pipescript io C_08
        -- C_08 I/O manifest (source of fee efficiency)

    15. comp-pipescript overlap D_00 D_03
        -- shared artifacts between D_00 and D_03 that D_04 will consolidate

    16. comp-pipescript consumers D_00
        -- verify which D_00 outputs are terminal (portal-only) vs consumed by other scripts

    comp-pipescript is AUTHORITATIVE for script I/O. comp-trace may show gaps for some
    artifacts (regex-based). If they disagree, trust comp-pipescript.
  </compiler_tools_mandate>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/D_04.client_portal_summary.py</file>
      <file action="reference">data/black_diamond/scripts/gold/D_00.portal_aggregates.py</file>
      <file action="reference">data/black_diamond/scripts/gold/D_02.entity_enrichment.py</file>
      <file action="reference">data/black_diamond/scripts/gold/D_03.composition_artifacts.py</file>
      <file action="reference">data/black_diamond/scripts/gold/C_06.client_mix_timeseries.py</file>
      <file action="reference">data/black_diamond/scripts/gold/C_08.fee_efficiency.py</file>
      <file action="reference">data/black_diamond/scripts/gold/B_01.holdings_lots.py</file>
      <file action="reference">data/black_diamond/scripts/gold/A_02.fee_rate_history.py</file>
      <file action="reference">data/black_diamond/scripts/gold/lib/s3_layout.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Read the existing D_00, D_02, D_03 scripts to understand the gold/ output paths and
      JSON schemas. Use comp-trace to verify each path. Read lib/s3_layout.py for S3 path
      constants.
    </requirement>

    <requirement id="2">
      D_04 must be structured with these builder functions:
      - build_firm_dashboard() -> platinum/firm/dashboard.json
      - build_firm_mix_summary() -> platinum/firm/mix_summary.json
      - build_advisor_summaries() -> platinum/advisors/{id}/summary.json (for each advisor)
      - build_client_summaries() -> platinum/clients/{rel_id}/summary.json (for each client)
      - build_client_timeseries() -> platinum/clients/{rel_id}/mix_timeseries.json + concentration.json
      - build_account_summaries() -> platinum/accounts/{acct_id}/summary.json (for each account)
      - main() orchestrates: firm -> advisors -> clients -> accounts -> upload all
    </requirement>

    <requirement id="3">
      Number consistency: Compute firm totals FIRST from gold sources. Then compute advisor
      totals as partitions of the firm total. Then clients as partitions of advisor totals.
      Never independently aggregate at each level -- always derive from the level above.
    </requirement>

    <requirement id="4">
      Platinum file schemas per PRD section "Target State: Platinum File Map":
      - platinum/firm/dashboard.json: employee leaderboard, clients_tab headline, fee efficiency scatter (all windows)
      - platinum/firm/mix_summary.json: latest 3-class mix, 5 quarterly bars, concentration top-10, composition pie
      - platinum/advisors/{id}/summary.json: book, mix snapshot, quarterly bars, composition, top holdings, fee role breakdown
      - platinum/clients/{rel_id}/summary.json: detail, mix snapshot, quarterly bars, composition, top holdings, 90d AUA decomposition, fee summary
      - platinum/clients/{rel_id}/mix_timeseries.json: daily asset-class allocation for 1Y/3Y/Max
      - platinum/clients/{rel_id}/concentration.json: top-N holdings over time by window
      - platinum/accounts/{acct_id}/summary.json: 3-class mix pie + top holdings
    </requirement>

    <requirement id="5">
      S3 upload: Use ThreadPoolExecutor for writing ~5,300 small JSON files to platinum/.
      Follow the same upload pattern used in D_03 (read D_03 for the exact boto3 upload code).
      Bucket: opal-data-bd. Prefix: platinum/.
    </requirement>

    <requirement id="6">
      Script must be idempotent (safe to re-run, overwrites all platinum/ files).
      Must pass py_compile before upload to gold runner.
      No emojis in print statements -- use plain ASCII prefixes (OK:, WARN:, ERROR:, SKIP:).
    </requirement>

    <requirement id="7">
      Dispatch chain update: D_04 goes after D_03 in CHAIN_DOWNSTREAM.
      Document the chain position in a comment at the top of the script.
      Catalog entry format: D_04|D_04.client_portal_summary.py|--upload
    </requirement>

    <requirement id="8">
      If dashboard.json exceeds 200KB when assembled, split into:
      platinum/firm/leaderboard.json, platinum/firm/clients_tab.json, platinum/firm/fee_efficiency.json.
      Implement as single file first, measure, split only if needed. Document the decision.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>data/black_diamond/scripts/gold/D_04.client_portal_summary.py -- complete, py_compile clean</deliverable>
    <deliverable>Session log documenting: comp-* traces run, input paths verified, schema decisions, number consistency approach</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT use Explore agents for dependency tracing -- use comp-trace and comp-blast</rule>
    <rule>Do NOT independently aggregate at firm/advisor/client levels -- derive top-down</rule>
    <rule>Do NOT write to gold/ paths -- all output goes to platinum/</rule>
    <rule>Do NOT deploy to EC2 or run on gold runner -- that is AE's job in Wave 2</rule>
    <rule>Do NOT use emojis anywhere in the script</rule>
  </do_not>
</task_order>
