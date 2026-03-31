<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-23-prices-002-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-23</date>
    <status>complete</status>
    <project_code>ADVI_PRICES</project_code>
    <thread_serial>ADVI_PRICES-001</thread_serial>
    <thread_ref>org/threads/ADVI_PRICES-001-lot-valuation-reconciliation-investigati/</thread_ref>
  </metadata>

  <objective>
    Two workstreams building on PRICES.001 findings:

    WS1: Deep-dive on the -$44M net pricing divergence (-$141M undershoot / +$97M
    overshoot across active accounts with real positions). Identify the systematic
    drivers — is it stale carry-forward prices, yahoo vs BD vendor pricing, scoped
    overrides drifting, or something else? Produce a ranked list of securities by
    pricing impact and recommend whether we should invest in price alignment or
    accept the methodology difference.

    WS2: Formalize the structural gap exclusion list. The -$35M in allocation-only
    accounts (bank, insurance, 529, HSA, held-away) is accepted as a known limitation.
    But we need an auditable record of exactly which accounts and account types are
    excluded, why, and a script that produces this list on demand. This is not a fix —
    it is documentation and tooling so future reconciliation runs don't re-investigate
    the same accounts.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/diagnostics/diag_pricing_divergence.py</file>
      <file action="create">data/black_diamond/scripts/diagnostics/structural_gap_exclusions.py</file>
      <file action="create">docs/data/structural_gap_exclusions.md</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      WS1 — Pricing divergence diagnostic.

      Build diag_pricing_divergence.py that, for a given date D:

      1. Loads silver/allocations/D.parquet and gold/holdings_lots/D.parquet
      2. Filters to RC5_NORMAL accounts only (excludes phantoms, alloc-only,
         insurance, non-investment — use the same RC classification from
         recon_lots_vs_allocations.py)
      3. For each account, computes:
         - bd_aua (from allocations)
         - lot_mv (from holdings_lots, open lots only)
         - diff and pct_diff
      4. For OVERSHOOTING accounts (lot_mv > bd_aua by > $1K):
         - Drill into per-security lot MV within the account
         - For each security, load the canonical price from
           silver/prices/canonical_prices.parquet (or the dated file)
         - Compare our price to what BD implicitly prices the position at
           (bd_aua / total_units is the account-level implied price, but
           per-security is harder — may need to compare against the
           positions_cube or use lot-level current_price vs transaction-observed)
         - Flag securities where our canonical price is > 10% above or below
           the last transaction-observed price
      5. For UNDERSHOOTING accounts (lot_mv < bd_aua by > $1K):
         - Same drill. Identify securities where our price is below what BD
           likely uses.
      6. Produce a ranked table:
         - Top 50 securities by ABSOLUTE pricing impact (sum of per-account
           divergence attributable to that security)
         - For each: our canonical price, price source (scoped_override /
           transaction_observed / yahoo_finance / carry_forward), price age
           (days since last update), and the implied BD price if derivable
      7. Summary statistics:
         - What % of the -$44M net is attributable to carry_forward prices
           (stale > 7 days)?
         - What % is attributable to scoped_overrides?
         - What % is attributable to yahoo vs transaction-observed spread?
    </requirement>

    <requirement id="2">
      WS1 — Recommendations.

      Based on the diagnostic output, deliver a brief (markdown, in the session
      log) with:
      - The top 10 securities by pricing impact with proposed action per security
        (update override, switch price source, accept as-is)
      - Whether the -$44M is concentrated (fixable by updating a few overrides)
        or distributed (systemic methodology difference we should accept)
      - If concentrated: specific price corrections to make in
        inject_scoped_overrides.py or bd_price_update.py
    </requirement>

    <requirement id="3">
      WS2 — Structural gap exclusion script.

      Build structural_gap_exclusions.py that, for a given date D:

      1. Loads silver/allocations/D.parquet
      2. Loads gold/holdings_lots/D.parquet
      3. Identifies all accounts that fall into the structural gap category:

         EXCLUSION RULES (each is a named category with a code):

         EX1_BANK: account_type in ('Bank', 'Savings')
           Reason: Cash/deposit accounts with no securities. BD tracks balance
           but no transaction feed for holdings.

         EX2_CREDIT: account_type in ('CreditCard', 'Loans', 'Mortgage')
           Reason: Liability accounts. Negative or zero MV. No securities.

         EX3_INSURANCE: account_type == 'Insurance' AND lot_mv == 0
           Reason: Insurance/annuity wrappers where BD reports policy value but
           sub-account holdings are not in transaction feed. Note: Insurance
           accounts WITH lots (lot_mv > 0) are NOT excluded — those have
           partial visibility and should be reconciled normally.

         EX4_TERM_LIFE: account_type == 'TermLife'
           Reason: Life insurance policies. No securities, no transaction feed.

         EX5_ALLOC_ONLY: account_market_value > $1000 AND lot_mv == 0
           AND account_type NOT IN (Bank, Savings, CreditCard, Loans,
           Mortgage, Insurance, TermLife)
           Reason: Catch-all for accounts with AUA but zero transaction
           history. Likely held-away, 529 plans, HSAs, or accounts at other
           custodians BD tracks for reporting only.

         EX6_MICRO: account_market_value > 0 AND account_market_value < $100
           AND lot_mv == 0
           Reason: De minimis accounts. Dust balances not worth reconciling.

      4. Produces output (stdout + optional --output-dir):
         - Per-exclusion summary: code, rule description, account count, AUA sum
         - Full account list per exclusion (account_id, account_type, bd_aua)
         - Total excluded AUA and % of total BD AUA
         - Remaining "reconcilable universe" after exclusions

      5. Writes the exclusion list to a dated parquet:
         structural_exclusions_{date}.parquet with columns:
         account_id, exclusion_code, account_type, bd_aua, reason
    </requirement>

    <requirement id="4">
      WS2 — Exclusion reference document.

      Create docs/data/structural_gap_exclusions.md documenting:
      - Each exclusion code (EX1-EX6) with the rule and rationale
      - The date this policy was established (2026-03-23)
      - The baseline numbers from the first run (account count, AUA per code)
      - Instructions for running the script and interpreting the output
      - Decision record: "Accepted as known limitation per COO on 2026-03-23.
        These accounts are excluded from lot-vs-allocation reconciliation.
        They are NOT excluded from BD-reported AUA totals — the total AUA
        in silver allocations remains the official number."
    </requirement>

    <requirement id="5">
      Commit WS1 and WS2 separately.
      WS1: feat(diagnostics): diag_pricing_divergence.py
      WS2: feat(diagnostics): structural_gap_exclusions.py + reference doc
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">diag_pricing_divergence.py runs against 2026-03-19 data and produces the top 50 securities ranked by pricing impact</criterion>
    <criterion id="2">Session log contains pricing recommendations brief with top 10 securities and concentration assessment</criterion>
    <criterion id="3">structural_gap_exclusions.py runs against 2026-03-19 data and produces per-code account counts and AUA</criterion>
    <criterion id="4">docs/data/structural_gap_exclusions.md documents all 6 exclusion codes with rationale and baseline numbers</criterion>
    <criterion id="5">Both commits on CLOUD branch</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT modify pricing scripts (bd_price_update.py, inject_scoped_overrides.py) — this task order is investigation and documentation only. Any price corrections come as a follow-up after COO reviews recommendations.</constraint>
    <constraint>Do NOT modify 03_build_holdings_lots.py or 02_build_positions_cube.py — PRICES.001 changes are complete.</constraint>
    <constraint>The structural exclusion list is an AUDIT artifact, not a filter applied to production scripts. The recon diagnostic already classifies these as RC2/RC3/RC4 — this task order formalizes and documents that classification.</constraint>
    <constraint>Commit with --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"</constraint>
    <constraint>No emojis in code (CLAUDE.md rule 13)</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="ADVI_PRICES.001.ae-recon-run-and-gold-rerun" status="pending">
      WS1 (pricing divergence) should ideally run against POST-fix holdings_lots
      (after AE gold rerun) to get clean numbers without phantom noise. However,
      DS can develop and test the script against 2026-03-19 pre-fix data and
      re-run after the gold rerun completes. Do not block on AE.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">WS1: diag_pricing_divergence.py diagnostic script</deliverable>
    <deliverable type="commit">WS2: structural_gap_exclusions.py + docs/data/structural_gap_exclusions.md</deliverable>
    <deliverable type="document">Pricing divergence brief in session log with top 10 securities + concentration assessment</deliverable>
  </deliverables>

  <closure>
    <closed_by>0.4.0_DS_ClientPlatform</closed_by>
    <closed_date>2026-03-25</closed_date>
    <summary>
      Both workstreams delivered. WS1 deep-dive was superseded by PRICES.003
      (yahoo priority dry-run) which answered the same questions more directly.

      WS1 — Pricing Divergence:
      - diag_pricing_divergence.py committed (0c62a3a2)
      - Root cause: ~$41M of -$57.7M gap was transaction-observed (T1) pricing
        lagging BD end-of-day NAV for 5 core ETFs (IEFA, IDVZ, Pathfinder US/Focused,
        iShares EM). Not a bug — methodology difference (trade-execution vs close).
      - PRICES.003 dry-run confirmed: switching 123 assets to yahoo_finance produces
        +$52.1M MV increase, closing gap from -3.6% to ~-0.4% (90% reduction).
      - Conclusion: CONCENTRATED, not systemic. Fixable via price source hierarchy
        change (yahoo_finance priority for tickered assets).

      WS2 — Structural Exclusions:
      - build_structural_exclusion_list.py committed (4d6a0258)
      - docs/data/structural_gap_exclusions.md committed (4d6a0258)
      - Baseline: 394 accounts, ~$15M across EX1-EX6 codes. Accepted as known
        limitation — these accounts lack transaction feeds by design.

      Pricing recommendations brief in:
      - org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-24/advi_prices_post_fix_verification.md
      - org/tier2_senior/0.4.0_DS_ClientPlatform/logs/2026-03-24/advi_prices_003_yahoo_priority_dryrun.md
    </summary>
  </closure>
</task_order>
