<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-08-49push-009-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <date>2026-04-08</date>
    <status>complete -- 0.4.0_DS_ClientPlatform~C, commit 999cfa59. Script: data/black_diamond/scripts/gold/validate_platinum_consistency.py</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>2b</wave>
    <phase>P3</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform~B" (not the base serial). This is your instance ID for this session. Use it for register_agent, heartbeat, and inbox-watch.</mcp_identity>
  </metadata>

  <objective>
    Write validate_platinum_consistency.py -- a standalone validation script that reads
    all platinum/ files from S3 and verifies cross-surface number consistency. This script
    will be run immediately after AE deploys D_04 to confirm data accuracy.
  </objective>

  <context>
    PRD: docs/architecture/ADVI_49PUSH_P3_PRD.md (section: Step 5 Cross-Surface Validation)

    The cross-surface matrix (docs/briefs/ADVI_49PUSH_P2_cross_surface_matrix.md) defines
    exactly which metrics must tie across which files. The validation script automates this.

    The master catalog (docs/briefs/ADVI_49PUSH_P2_platinum_file_catalog.md) lists every
    platinum file with its schema. Use this to know what fields to extract.

    This script runs AFTER deploy -- it validates S3 output, not local files. But write it
    NOW so it's ready the instant platinum lands in S3.
  </context>

  <compiler_tools_mandate>
    1. comp-pipescript io D_04
       -- verify D_04's complete I/O (reads + writes) to understand what platinum files exist

    2. comp-pipescript consumers D_04
       -- confirm D_04 is terminal (no other script reads platinum/)
  </compiler_tools_mandate>

  <requirements>
    <requirement id="1">
      Location: data/black_diamond/scripts/gold/validate_platinum_consistency.py
    </requirement>

    <requirement id="2">
      The script reads platinum/ files from S3 (opal-data-bd bucket) and validates:

      TIER 1 -- Firm-level consistency:
      a) dashboard.json total_aua = sum of ALL advisors/*/summary.json total_aua
      b) dashboard.json total_nna = sum of ALL advisors/*/summary.json nna values
      c) dashboard.json client_count = deduplicated count across all advisors
      d) leaderboard.json advisor entries match advisors/*/summary.json (same AUA, NNA per advisor)
      e) partner_analytics.json firm totals match dashboard.json firm totals

      TIER 2 -- Advisor-to-client consistency:
      f) Each advisors/{id}/summary.json total_aua = sum of their clients' total_aua
      g) Each advisor's client_count = count of their client summary files
      h) Each advisor's NNA = sum of their clients' NNA

      TIER 3 -- Client-to-account consistency:
      i) Each clients/{rel_id}/summary.json total_aua = sum of account AUA in fee_summary
      j) Each client's account list matches accounts/*/summary.json files that exist

      TIER 4 -- Timeseries sanity:
      k) clients/{rel_id}/mix_timeseries.json latest date matches summary.json snapshot date
      l) concentration.json top holdings are a subset of the full holdings in the summary
    </requirement>

    <requirement id="3">
      Output format:
      - Print each check with PASS/FAIL prefix (ASCII only, no emojis)
      - For failures: print expected value, actual value, file paths, field names
      - Summary at end: X/Y checks passed
      - Exit code 0 = all passed, exit code 1 = failures found
      - Support --json flag for machine-readable output
    </requirement>

    <requirement id="4">
      Tolerance: Allow rounding discrepancy < $1 for dollar amounts, < 0.01% for percentages.
      Document the tolerance in the script header.
    </requirement>

    <requirement id="5">
      The script should handle the case where platinum/ files don't exist yet (pre-deploy).
      Print a clear message: "ERROR: platinum/ prefix not found in S3. Run D_04 first."
      Exit code 2 for missing data (distinct from validation failure).
    </requirement>

    <requirement id="6">
      py_compile clean, all ASCII, no emojis. Standalone script (no imports from D_04).
      Uses boto3 for S3 reads. Must work on both gold runner and local machine.
    </requirement>
  </requirements>

  <deliverables>
    <deliverable>data/black_diamond/scripts/gold/validate_platinum_consistency.py -- complete, py_compile clean</deliverable>
    <deliverable>Message to COO (2.0.0_SA_COO) confirming script ready, listing all validation checks</deliverable>
  </deliverables>

  <do_not>
    <rule>Do NOT run the script against S3 -- it won't work until AE deploys. Just write it.</rule>
    <rule>Do NOT import from D_04 -- this is a standalone validator</rule>
    <rule>Do NOT hardcode advisor/client IDs -- discover them by listing the S3 prefix</rule>
  </do_not>
</task_order>
