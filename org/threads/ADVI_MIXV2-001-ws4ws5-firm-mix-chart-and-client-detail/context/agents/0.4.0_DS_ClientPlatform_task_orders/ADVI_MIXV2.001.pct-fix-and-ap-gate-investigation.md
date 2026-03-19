<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-001-pct-fix-ap-gate</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
    <thread_serial>none</thread_serial>
    <project_code>ADVI_MIXV2</project_code>
  </metadata>

  <objective>
    Fix the pct scale bug in opal-partners-data Lambda (WS1) and investigate + fix the $60M
    structured_notes AP gate volatility in 06b (WS2). Both are prerequisite to shipping
    firm-level pre-computed mix views (WS3).
  </objective>

  <scope>
    <files>
      <file action="modify">infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py</file>
      <file action="create">.tmp_insurance_ap_gate.py</file>
      <file action="modify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
      <file action="create">data/black_diamond/scripts/gold/insurance_accounts.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      WS1 — pct fix in handle_books_composition (Lambda).
      Change BOTH the mix_items loop AND the top_items loop AND the other bucket to use:
        'pct': round(float(mv) / total_mv, 6)
      instead of:
        'pct': round(float(mv) / total_mv * 100, 2)
      The 0-1 convention matches every other pct field in the portal data contracts.
      No frontend changes are needed — all consumers already multiply by 100 to display.
      Add a comment in the Lambda confirming the 0-1 convention for future maintainers.
    </requirement>

    <requirement id="2">
      WS2 — Write diagnostic script .tmp_insurance_ap_gate.py that:
        a) Lists all account_ids in positions_cube whose holdings classified as structured_notes
           have total market_value > $1M across any date in the past 18 months
        b) For each such account: shows max(account_performance.date), min/max dates it appears
           in positions_cube snapshots, and the distinct asset_name strings used for structured_notes
           holdings on that account across all dates
        c) Computes for each account: how many snapshot dates had it excluded by the 45-day AP gate
           (last_seen > 45 days from snapshot date)
        d) Prints a summary: total structured_notes market_value when included vs excluded, showing
           the source of the ~$60M oscillation

      Run the diagnostic and document findings in a session log entry.
    </requirement>

    <requirement id="3">
      WS2 — Based on diagnostic findings, implement the AP gate fix in 06b.
      Expected fix: create data/black_diamond/scripts/gold/insurance_accounts.json:
        {"insurance_account_ids": ["acc_xxx", "acc_yyy", ...], "ap_gate_days_override": 180}
      In 06b process_date(), after loading the config, apply the extended gate ONLY to
      account_ids listed in insurance_accounts.json. All other accounts retain the 45-day gate.
      This is a surgical override, not a global gate increase.

      If the diagnostic reveals classification instability (not just AP gate) as a co-cause:
      also add the specific asset_name strings to ASSET_NAME_TO_TICKER or a new
      INSURANCE_NAME_OVERRIDES dict with their correct classification.
    </requirement>

    <requirement id="4">
      Commit all changes to CLOUD with proper --author attribution:
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"
      Separate commits:
        (a) Lambda pct fix — "0.4.0_DS_ClientPlatform: fix pct scale in handle_books_composition (0-1 not 0-100)"
        (b) 06b AP gate fix — "0.4.0_DS_ClientPlatform: 06b targeted AP gate override for insurance accounts"
      Write a DevOps brief at docs/briefs/devops-brief-mixv2-001.md covering both deploys:
        - Lambda: which function, build-and-upload sequence, Terraform plan/apply expected
        - 06b: S3 upload path, how to run incremental to pick up the gate fix
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Lambda pct fix: equity showing 62.5% on firm composition panel, not 6250%</criterion>
    <criterion id="2">Diagnostic identifies the specific account_ids driving $60M structured_notes oscillation</criterion>
    <criterion id="3">After 06b fix, insurance accounts remain in snapshots across their full statement cycle gaps</criterion>
    <criterion id="4">Both commits are on CLOUD with correct --author attribution</criterion>
    <criterion id="5">DevOps brief at docs/briefs/devops-brief-mixv2-001.md is complete and actionable</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT increase AP_GATE_DAYS globally — only override for identified insurance accounts</constraint>
    <constraint>Do NOT deploy — DT deploys Lambda (task order 004), AE deploys 06b (task order 003)</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
    <constraint>Document the insurance_accounts.json format clearly — operations will need to add new accounts when new insurance products are onboarded</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" task="none" status="complete">
      Investigation complete — root cause documented in logs/2026-03-17/mix_concentration_full_audit.md
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Lambda pct fix committed to CLOUD</deliverable>
    <deliverable type="commit">06b AP gate fix + insurance_accounts.json committed to CLOUD</deliverable>
    <deliverable type="document">docs/briefs/devops-brief-mixv2-001.md</deliverable>
    <deliverable type="document">Session log in logs/2026-03-17/ documenting diagnostic findings</deliverable>
  </deliverables>
</task_order>
