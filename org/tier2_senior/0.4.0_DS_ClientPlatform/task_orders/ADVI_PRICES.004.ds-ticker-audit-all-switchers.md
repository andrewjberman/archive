<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-24-prices-004-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-24</date>
    <status>complete</status>
    <project_code>ADVI_PRICES</project_code>
  </metadata>

  <objective>
    GATE CHECK before any further deployment. DS already corrected 13 ticker
    mismatches and flagged 2 more for investigation (CRBL, FM). But the COO
    needs certainty that EVERY ticker that will switch to yahoo under the new
    hierarchy is actually correct — not just the ones that were obviously broken.

    The full pool is ~145 T1 assets with tickers that have yahoo data.
    DS must audit ALL of them, not just the outliers.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/diagnostics/diag_ticker_accuracy_audit.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Build diag_ticker_accuracy_audit.py that for each T1 asset with a ticker:

      1. Loads canonical_prices.parquet (latest date) — get asset_name, ticker, price
      2. Loads historical_prices.parquet — get yahoo close for that ticker
      3. For each asset, performs a SANITY CHECK:
         a. Does the yahoo security name (from yfinance .info if available, or
            inferred from the ticker) match the BD asset_name?
         b. Is the yahoo price in the right MAGNITUDE for this asset?
            (e.g., mutual fund NAVs are typically $10-$500, ETFs $20-$600,
            equities vary. A $26,500 yahoo price for a $1 canonical asset is
            a red flag — BMC was exactly this.)
         c. For Vanguard/Fidelity/Schwab mutual funds: does the ticker resolve
            to the correct SHARE CLASS? Admiral vs Investor vs Institutional
            vs ETF have different NAVs for the same fund.
         d. For any asset where the ticker appears in _TICKER_CORRECTIONS:
            confirm the correction is right.

      4. Classify each into:
         - VERIFIED: ticker matches asset name, price is in expected range
         - CORRECTED: already in _TICKER_CORRECTIONS, correction verified
         - SUSPECT: name mismatch, magnitude mismatch, or share class mismatch
         - NO_DATA: ticker not in historical_prices (the 12 missing ones)

      5. For SUSPECT items: provide the BD asset_name, current mapped ticker,
         what the ticker actually resolves to, and the correct ticker if identifiable.
    </requirement>

    <requirement id="2">
      Resolve the 2 deferred items from .003:
      - CRBL (Ceribell): is the ticker correct and the company just crashed, or
        is it a mismatch?
      - FM: is BD holding the iShares Frontier EM ETF (FM on US exchanges) or
        First Quantum Minerals (FM.TO on TSX)?
    </requirement>

    <requirement id="3">
      Resolve the Vanguard share-class problems COO flagged:
      - VXUS maps to 3 different asset names. One is the ETF (correct), one is
        "Admiral" (should be VTIAX?), one is "Institutional" (should be VITSX?).
      - VEIPX (Vanguard Equity-Income Inv) — not in historical_prices. Is the
        ticker correct?
      - Any other Vanguard/Fidelity/Schwab share class issues found in the audit.
    </requirement>

    <requirement id="4">
      Deliver a complete audit table in the session log:

      | asset_name | ticker | status | yahoo_name | price_check | notes |

      Plus a FINAL list of tickers that are VERIFIED or CORRECTED — this becomes
      the definitive "yahoo-safe" list that AE uses for historical_prices backfill.
      Any SUSPECT tickers get either corrected (add to _TICKER_CORRECTIONS) or
      removed (set to None) before the list is finalized.
    </requirement>

    <requirement id="5">
      Commit any new ticker corrections found during the audit.
      Do NOT commit the audit script until the full results are in the session log.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Every T1+ticker asset audited and classified (VERIFIED/CORRECTED/SUSPECT/NO_DATA)</criterion>
    <criterion id="2">CRBL and FM resolved</criterion>
    <criterion id="3">All Vanguard/Fidelity/Schwab share-class issues identified and corrected</criterion>
    <criterion id="4">Final "yahoo-safe" ticker list delivered for AE backfill</criterion>
    <criterion id="5">Any new corrections committed to CLOUD</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>This is a READ-ONLY audit + targeted corrections. Do NOT rebuild canonical prices.</constraint>
    <constraint>Commit with --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="none" status="clear">No blockers. Uses existing parquet files.</dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">Any new ticker corrections + audit script</deliverable>
    <deliverable type="document">Full audit table + final yahoo-safe ticker list in session log</deliverable>
  </deliverables>
</task_order>
