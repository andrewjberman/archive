<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-09-49push-020-de</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-04-09</date>
    <status>pending -- unblocked (auth confirmed fixed, gold re-run in progress)</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>5</wave>
    <phase>P3+P4</phase>
  </metadata>

  <objective>
    After Terraform deploys Lambdas (.019) and portal deploys to DEV:
    1. Run test_platinum_auth.py with all 4 test accounts
    2. Verify all ADVI tabs render correctly from platinum data
  </objective>

  <context>
    Gold rebuild complete -- platinum/ files are in S3.
    Lambdas deploying via .019 (DT).
    Portal changes committed on DEV branch (4 commits).

    Auth smoke test: scripts/test_platinum_auth.py (24 assertions, 4 tiers)
    PRD test matrix: docs/architecture/ADVI_49PUSH_P4_PRD.md (T1-T6)
  </context>

  <requirements>
    <requirement id="1">
      BLOCKED: Wait for DT (.019) to confirm Lambda deploy complete before running auth tests.
      Check inbox or agent status for DT's confirmation.
    </requirement>

    <requirement id="2">
      Deploy portal DEV branch to opalinvest.dev:
      - cd portal && bun install && bun run build
      - Deploy to DEV environment
    </requirement>

    <requirement id="3">
      Run auth smoke test with internal admin account:
      python scripts/test_platinum_auth.py --token <JWT> --tier internal --role admin --firm bd
      All 24 tests should pass.
    </requirement>

    <requirement id="4">
      Browser QA on opalinvest.dev:
      - Distribution tab: donut + stacked area render from platinum
      - Advisors tab: leaderboard renders from platinum (~15KB vs 681KB)
      - Books tab: N1 -> L2 -> L3 -> L4 drill, each level renders from platinum
      - ClientDetail: mix timeseries + concentration panels render
      - Verify: no console errors, no missing data, numbers look reasonable
    </requirement>

    <requirement id="5">
      Report results: which tests passed/failed, any rendering issues, screenshots if problems found.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>Auth smoke test results (pass/fail per test case)</deliverable>
    <deliverable>Browser QA confirmation or issue list</deliverable>
    <deliverable>Message to COO with results</deliverable>
  </deliverables>
</task_order>
