# AUA Scoped Price Overrides -- Deploy Briefing

<task_order>
  <metadata>
    <id>0.4.0_DS_ClientPlatform-2026-03-17-aua-scoped-overrides</id>
    <issued_by>0.4.0_DS_ClientPlatform</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-17</date>
    <status>pending</status>
  </metadata>

  <objective>
    Deploy scoped price overrides into canonical_prices.parquet and regenerate
    the gold pipeline to fix $51M of AUA valuation errors across 7 accounts.
    Two-step deployment: (1) inject corrected prices into canonical_prices,
    (2) rebuild gold client_performance with ghost account exclusions.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/silver/inject_scoped_overrides.py</file>
      <file action="modify">data/black_diamond/scripts/gold/05_build_client_performance.py</file>
      <file action="modify">data/black_diamond/scripts/gold/aua_overrides.json</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Run inject_scoped_overrides.py --upload on EC2 to inject 5 corrected prices
      into canonical_prices.parquet. This replaces wrong prices (BNPQF equity at $97,
      Destinations model sleeves at $546/$384, etc.) with silver-derived flat prices.
      The script is idempotent -- safe to re-run.
    </requirement>
    <requirement id="2">
      Run 05_build_client_performance.py --upload to rebuild gold/client_performance.parquet.
      This picks up the corrected canonical prices AND applies RC6 ghost account
      exclusions from aua_overrides.json.
    </requirement>
    <requirement id="3">
      Run 05c_validate_aua_vs_silver.py to confirm gap reduction.
      Expected: aggregate gap drops from ~3.5% to less than 1.5%.
    </requirement>
    <requirement id="4">
      Run downstream gold scripts (07, 08, 09, 10) to propagate corrected AUA
      into timeseries_chart.json, partner_analytics.json, and leaderboard outputs.
    </requirement>
    <requirement id="5">
      Run the bd-portal-publisher Lambda (or trigger the pipeline) to regenerate
      portal JSON outputs with corrected GRO decomposition values.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">inject_scoped_overrides.py --dry-run shows 1,721 override rows injected, 5,799 wrong rows removed, zero duplicates</criterion>
    <criterion id="2">After --upload, canonical_prices.parquet contains source='scoped_override' rows for all 5 assets</criterion>
    <criterion id="3">05c_validate_aua_vs_silver.py shows gap less than 1.5% on latest date</criterion>
    <criterion id="4">timeseries_chart.json growth_decomposition values reflect corrected AUA (no $20M+ market swings for a $1.5B book)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Run inject_scoped_overrides.py BEFORE 05_build_client_performance.py -- canonical prices must be updated first</constraint>
    <constraint>Do not modify canonical_prices.parquet by hand -- always use the script</constraint>
    <constraint>The script removes ALL existing rows for the 5 overridden asset names (not just scoped_override rows) to prevent the wrong price from being picked up via carry_forward</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">Updated canonical_prices.parquet on S3 with scoped_override source rows</deliverable>
    <deliverable type="commit">Updated gold/client_performance.parquet with corrected AUA</deliverable>
    <deliverable type="commit">Updated portal JSON outputs (timeseries_chart.json, partner_analytics.json)</deliverable>
  </deliverables>
</task_order>

## Deployment Sequence

```
Step 1: Upload scripts to EC2
         safe-ec2-deploy.sh (or S3 artifact upload)

Step 2: Inject scoped overrides into canonical_prices
         python data/black_diamond/scripts/silver/inject_scoped_overrides.py --upload

Step 3: Rebuild client performance (picks up corrected prices + ghost exclusions)
         python data/black_diamond/scripts/gold/05_build_client_performance.py --upload

Step 4: Validate
         python data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py --date 2026-03-13

Step 5: Rebuild downstream gold outputs
         python data/black_diamond/scripts/gold/07_build_nna_aua_by_geography.py --upload
         python data/black_diamond/scripts/gold/08_build_nna_aua_by_advisor.py --upload
         python data/black_diamond/scripts/gold/09_generate_partner_analytics.py --upload
         python data/black_diamond/scripts/gold/10_generate_advisor_rolling_flows.py --upload

Step 6: Trigger portal publisher Lambda (or wait for next pipeline run)

Step 7: Verify GRO values in portal
```

## What the scoped overrides fix

| Asset | Was Priced At | Now Priced At | Source | Impact |
|---|---|---|---|---|
| Waldrop Donor Advised Fund | $1.00 (par) | $1.95 (silver-derived NAV) | scoped_override | Corrects -$2.8M underval |
| BNP PARIBAS SA | $97.16 (BNPQF equity) | $0.75 (75c on dollar) | scoped_override | Corrects +$20.7M overval |
| DESTINATIONS LARGE CAP EQUITY I | $546.00 (fund NAV) | $13.30 (silver-derived) | scoped_override | Corrects +$14.3M overval |
| DESTINATIONS INTERNATIONAL EQUITY I | $384.00 (fund NAV) | $13.30 (silver-derived) | scoped_override | Corrects +$6.0M overval |
| JPMORGAN CHASE FINL CO LLC 0% 2029 | $1.00 (par) | $2.55 (silver-derived) | scoped_override | Corrects -$1.9M underval |

Ghost account exclusions (aua_overrides.json): 4 accounts totaling +$7.4M of stale AUA removed.

## Risk

- **Low**: Scoped overrides use flat prices. Real prices may drift +-5% over time. Acceptable for these illiquid/structured instruments.
- **Low**: inject_scoped_overrides.py is idempotent. Running it twice produces the same result.
- **None**: NNA flows are unaffected (computed from transactions, not positions x prices).
