<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-18-mvp318-001-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-18</date>
    <status>complete</status>
    <project_code>ADVI_MVP318</project_code>
  </metadata>

  <objective>
    Commit all pending DS deliverables for the ADVI_MVP318 sprint:
    (1) bd-portal-publisher uncommitted fix (WS1),
    (2) D4 architect consolidation (WS2) + WS3a advisor timeseries logic in a single commit to bd-portal-advisor-publisher,
    (3) WS3c new route handlers in opal-partners-data,
    (4) WS5 script 10 confirmation and commit if not yet committed.
    All DT deploys and the AE gold run gate on DS completing these commits.
  </objective>

  <context>
    Reference: docs/architecture/ADVI_MVP318_PRD.md (WS1-WS3, WS5).
    Architecture background: docs/architecture/ADVI_architect_methodology_bifurcation.md,
    docs/architecture/ADVI_data_lineage.md.

    State of working tree:
    - `infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py` has uncommitted changes (+17 lines per git diff).
      These may be the WS1 Prescription A fix (date anchor alignment). Read the diff before committing.
      If the changes are correct per WS1-B in the PRD, commit them. If not, do not commit broken code.
    - `infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py` has uncommitted D4 changes (+32 lines).
      These implement the architect override (load_sources + lambda_handler join). Correct per PRD WS2.
      WS3a logic must be added to this file BEFORE committing — DT batches WS2 and WS3b into one deploy.
  </context>

  <scope>
    <files>
      <file action="verify-then-commit">infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py</file>
      <file action="modify-then-commit">infra/aws/lambda/bd-pipeline/bd-portal-advisor-publisher/lambda_function.py</file>
      <file action="modify-then-commit">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="verify-then-commit">data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1" workstream="WS1">
      Read the uncommitted diff in bd-portal-publisher/lambda_function.py:
        git diff infra/aws/lambda/bd-pipeline/bd-portal-publisher/lambda_function.py
      Verify it matches Prescription A from the PRD (geo_us_for_snap date anchor alignment).
      If it is correct, commit it separately under DS author attribution:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "fix(bd-portal-publisher): align snapshot date anchor to US-only max date (WS1 Prescription A)"
      If the diff does NOT match Prescription A, document what it contains and flag to COO before committing.
      Note: DT runs the WS1-A diagnostic independently to determine whether WS1 fix is even needed.
      Commit this regardless — if Root Cause B, DT simply won't deploy it.
    </requirement>

    <requirement id="2" workstream="WS3a">
      Add two new output functions to bd-portal-advisor-publisher/lambda_function.py.
      These are batched with D4 (WS2) into a single commit to avoid double DT deploys.

      Function 1 — build_advisor_timeseries(acct: DataFrame, cdim: DataFrame) -> dict:
      - After architect override in lambda_handler(), group acct by (date, architect)
      - Aggregate: sum total_aua, cum_inflows, cum_outflows, nna; count unique relationship_ids per group
      - For each architect, write gold/advisors/{advisor_id}/timeseries.json to S3
      - Shape matches AdvisorTimeseriesResponse from PRD WS3 endpoint contract
      - Runs after build_advisor_books(), uses the same post-override acct DataFrame

      Function 2 — build_advisor_mix_timeseries(acct: DataFrame, relationship_ids_by_advisor: dict) -> None:
      - For each advisor, collect their relationship_ids (from the architect groupby already done in build_advisor_books)
      - For each relationship, load gold/client_timeseries/{rel_id}.json from S3 (skip if missing — 06b AP gate may exclude some)
      - On each date, compute AUA-weighted average of equity/fixed_income/structured_notes/cash/other
      - All pct fields are 0-1 convention (not 0-100)
      - Write gold/advisors/{advisor_id}/mix_timeseries.json
      - Load one advisor at a time to manage memory; clear per-relationship data after writing each advisor

      Call both functions from lambda_handler() after build_advisor_books().
      Pass relationship_ids_by_advisor as a dict collected during the architect groupby in build_advisor_books
      (or refactor build_advisor_books to return it).
    </requirement>

    <requirement id="3" workstream="WS2+WS3a-commit">
      Commit the combined D4 + WS3a changes to CLOUD in a single commit:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "feat(bd-portal-advisor-publisher): D4 architect override + WS3a advisor timeseries artifacts (ADVI_MVP318)"
      This is the gate for DT's bd-portal-advisor-publisher deploy. Confirm commit SHA to COO.
    </requirement>

    <requirement id="4" workstream="WS3c">
      Read infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py.
      Identify how existing routes are dispatched (look for /books/relationship/ handler pattern).
      Add two new handlers:

        def handle_advisor_timeseries(advisor_id: str, firm_id: str) -> dict:
            """Serve gold/advisors/{advisor_id}/timeseries.json from S3."""
            key = f"gold/advisors/{advisor_id}/timeseries.json"
            return serve_s3_json(key, firm_id)

        def handle_advisor_mix_timeseries(advisor_id: str, firm_id: str,
                                           window: str | None) -> dict:
            """Serve gold/advisors/{advisor_id}/mix_timeseries.json from S3."""
            key = f"gold/advisors/{advisor_id}/mix_timeseries.json"
            data = serve_s3_json(key, firm_id)
            if window and data.get('data'):
                data['data'] = _filter_window(data['data'], window)
            return data

      Add routing in lambda_handler() to dispatch:
      - GET /api/scoped/partners/books/advisor/{advisor_id}/timeseries
      - GET /api/scoped/partners/books/advisor/{advisor_id}/mix-timeseries (optional ?window= param)

      Path discriminator: /books/advisor/ (not /books/relationship/) — confirm it does not conflict.
      Use the same _filter_window helper used for relationship mix-timeseries if it exists, or implement
      a minimal equivalent (filter data list to dates >= window_start).

      Commit to CLOUD:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "feat(opal-partners-data): advisor timeseries + mix-timeseries route handlers (ADVI_MVP318 WS3c)"
      Confirm commit SHA to COO. This is the gate for DT's partners-api deploy.
    </requirement>

    <requirement id="5" workstream="WS5">
      Run: git log --oneline -- data/black_diamond/scripts/gold/generate_advisor_rolling_flows.py
      If the MTD/QTD/YTD changes from ADVI_MVPLVL.006 are in the log, WS5 is confirmed committed. Report it.
      If NOT committed: commit the script now under DS author attribution.

      Also confirm whether generate_partner_analytics.py (script 09, architect_leaderboard.json) requires
      corresponding MTD/QTD/YTD window additions. Check the leaderboard response shape — if it only has
      trailing windows (3M/6M/1Y/2Y/3Y), it needs the same treatment per ADVI_MVPLVL.006 requirements.
      If script 09 needs changes, add them in the same commit.

      The AE gold run will upload whichever scripts are confirmed committed. Scripts not committed to CLOUD
      will not be picked up.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">bd-portal-publisher WS1 fix committed to CLOUD (or flagged to COO if incorrect)</criterion>
    <criterion id="2">bd-portal-advisor-publisher: D4 + WS3a (both functions + handler calls) committed in single commit</criterion>
    <criterion id="3">opal-partners-data: two new advisor route handlers committed to CLOUD</criterion>
    <criterion id="4">generate_advisor_rolling_flows.py MTD/QTD/YTD changes confirmed committed; script 09 status reported</criterion>
    <criterion id="5">All commit SHAs reported to COO for DT gate clearance</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT commit bd-portal-advisor-publisher without WS3a — DT deploys both in one build</constraint>
    <constraint>No emojis in any code, log lines, or print statements (CLAUDE.md rule 13)</constraint>
    <constraint>Use 0.4.0_DS_ClientPlatform as git author on all commits</constraint>
    <constraint>All commits go to CLOUD branch (parent repo), not portal DEV</constraint>
    <constraint>Do not modify any Lambda file already confirmed correct by CTO review</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="clear">No upstream DS gates — this task order is the first mover</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">bd-portal-publisher WS1 fix on CLOUD</deliverable>
    <deliverable type="commit">bd-portal-advisor-publisher D4+WS3a on CLOUD</deliverable>
    <deliverable type="commit">opal-partners-data WS3c handlers on CLOUD</deliverable>
    <deliverable type="report">WS5 script 10 commit confirmation + script 09 status brief</deliverable>
  </deliverables>
</task_order>
