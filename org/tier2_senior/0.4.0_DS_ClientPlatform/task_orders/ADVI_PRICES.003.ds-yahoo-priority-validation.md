<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-24-prices-003-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-24</date>
    <status>complete</status>
    <project_code>ADVI_PRICES</project_code>
  </metadata>

  <objective>
    DIAGNOSTIC ONLY — DO NOT DEPLOY.

    COO has written a pricing hierarchy change in bd_price_update.py (unstaged)
    that promotes yahoo_finance to highest priority for tickered assets:

      yahoo_finance (tickered) -> scoped_override (non-tickered) -> transaction_observed -> carry_forward

    Before this goes anywhere near production, DS must build a dry-run comparison
    script that simulates the new hierarchy against current data and produces a
    full impact report. We need to see exactly what changes, how many assets are
    affected, and what happens to the reconciliation numbers — all without
    writing to S3 or touching any production artifacts.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/diagnostics/diag_yahoo_priority_dryrun.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Build diag_yahoo_priority_dryrun.py that:

      1. Loads the current canonical_prices.parquet (the LIVE production prices)
      2. Loads historical_prices.parquet (yahoo closes)
      3. For the most recent date in canonical_prices, simulates the new hierarchy:
         - For each asset with a ticker: look up that ticker in historical_prices
           for the same date (or nearest prior date within 7 days)
         - If yahoo has a price: that's the "new" price
         - If not: keep the current canonical price unchanged
      4. Produces a COMPARISON table (NOT a replacement):

         | asset_name | ticker | current_price | current_source | current_date |
         | yahoo_price | yahoo_date | delta | pct_delta | would_switch |

      5. Summary statistics:
         - Total assets in canonical: N
         - Assets with yahoo match: N (would switch to yahoo)
         - Assets WITHOUT yahoo match: N (unchanged — scoped_override, T1, carry_forward)
         - Of the switching assets: how many currently use transaction_observed vs carry_forward
         - Aggregate MV impact: join against holdings_lots to compute
           sum((yahoo_price - current_price) * total_units) per asset
         - Top 30 assets by ABSOLUTE MV impact (both directions)
         - Net MV impact across entire book
         - What the reconciliation gap would become (current -$57.7M - net MV impact)

      6. Flag any asset where yahoo_price is MORE than 50% different from
         current_price — these need manual review before deployment. Could be
         ticker mismatches (e.g. structured note resolving to wrong public ticker,
         which is exactly why scoped_overrides exist).

      7. Flag any scoped_override asset that ALSO has a yahoo match — these are
         cases where the new hierarchy would switch from the deliberate override
         to yahoo. List them explicitly. If any exist, that's a problem we need
         to solve before deploying (either remove the ticker mapping for those
         assets or keep override priority for them).
    </requirement>

    <requirement id="2">
      Run the script against current data (2026-03-19 or latest available) and
      deliver the full output in your session log. COO will review the numbers
      before deciding whether to commit and deploy the hierarchy change.
    </requirement>

    <requirement id="3">
      DO NOT commit the bd_price_update.py change. It is in the working tree
      for reference only. The diagnostic script is the only deliverable.
      Commit: feat(diagnostics): diag_yahoo_priority_dryrun.py (ADVI_PRICES-003)
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Dry-run script produces the full comparison table and summary statistics</criterion>
    <criterion id="2">Top 30 assets by MV impact listed with current vs yahoo prices</criterion>
    <criterion id="3">Any >50% price delta assets flagged for manual review</criterion>
    <criterion id="4">Scoped override conflicts identified (if any)</criterion>
    <criterion id="5">Session log contains full output for COO review</criterion>
    <criterion id="6">bd_price_update.py NOT committed — only the diagnostic script is committed</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>DO NOT commit bd_price_update.py changes</constraint>
    <constraint>DO NOT write to S3 or modify any production artifacts</constraint>
    <constraint>DO NOT run bd_price_update.py</constraint>
    <constraint>This is a READ-ONLY diagnostic against existing parquet files</constraint>
    <constraint>Commit with --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">
      COO's bd_price_update.py change is in the working tree for reference.
      canonical_prices.parquet and historical_prices.parquet are on S3.
      No blockers.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">diag_yahoo_priority_dryrun.py diagnostic script only</deliverable>
    <deliverable type="document">Full dry-run results in session log for COO review</deliverable>
  </deliverables>
</task_order>
