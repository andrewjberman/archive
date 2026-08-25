"""PRF-a-1 COLUMN AUDIT -- ADVI_PERFRP TO-R1-DS / PRFR1DS-AC1.

Maps every column of the plan's ratified daily account fact
(ADVI_PERFORMANCE_E2E_STANDARDIZATION_PLAN_20260806.md s.3.2, 8 column groups)
to a LIVE source on the 49F canonical plane, or DECLARES IT ABSENT.

Per Q-p1 (CTO): `fact_account_return_daily` IS NOT BUILT and is NOT being built
here. The plan is reused as an ARTIFACT -- its column set is this audit's
DENOMINATOR, never a build target.

Classification (M = DIRECT + DERIVED + CONSTANT ; K = ABSENT ; N = M + K):
  DIRECT   a live column on a live table, read as-is
  DERIVED  deterministic from live columns / an IMPORTED pure core, no upstream work
  CONSTANT the projection assigns it (method identity, versions, run id)
  ABSENT   no live source -- requires upstream production. Goes in the contract's
           declared-absent list against contract_version. NEVER silently filled.

One sub-state is tracked separately and is NOT a fourth bucket: VALUE-REFUSED.
The column is sourced (so it counts in M) but its live values are null at the
current frontier. Measured 2026-08-24: twr_daily r_net/r_gross are dtype null,
status REFUSED-NO-BMV, for all 7,335 rows at date=2026-08-21. Reported separately
so M is never read as "N columns of live values".

Evidence vintage: live plane read 2026-08-24 (schemas + censuses below).
"""
from __future__ import annotations

# (column, group, class, source)
COLS = [
    # --- Identity (7) ---
    ("firm_id", "Identity", "CONSTANT",
     "runner --firm argument (PRF-inv-5, required, no default); pins the bucket"),
    ("account_id", "Identity", "DIRECT", "canonical_valuation.account_id"),
    ("date", "Identity", "DIRECT", "canonical_valuation.business_date"),
    ("prior_valuation_date", "Identity", "DERIVED",
     "dim_calendar prior trading day (NEVER#1: calendar-resolved, never wall-clock)"),
    ("method_id", "Identity", "CONSTANT",
     "projection declares; twr_daily.flow_convention='EOD' is the convention half"),
    ("method_version", "Identity", "CONSTANT", "projection declares; tied to contract_version"),
    ("schema_version", "Identity", "DIRECT", "schema_version present on every canonical table"),
    # --- Source/provenance (7) ---
    ("source_system", "Source/provenance", "DIRECT", "source_pipeline on every canonical table"),
    ("source_grain", "Source/provenance", "CONSTANT", "declared per source table by the projection"),
    ("source_vintage", "Source/provenance", "DIRECT", "_ingested_at on every canonical table"),
    ("source_object", "Source/provenance", "DERIVED", "the S3 key the projection read, recorded at read time"),
    ("source_row_hash", "Source/provenance", "ABSENT",
     "no row hash on ANY of the 8 canonical tables (all schemas read 2026-08-24)"),
    ("calculation_version", "Source/provenance", "CONSTANT",
     "the projection's own version, tied to contract_version"),
    ("run_id", "Source/provenance", "DERIVED",
     "run id minted per run (the publisher already mints one for _manifests)"),
    # --- Valuation (10) ---
    ("bmv", "Valuation", "DERIVED",
     "canonical_valuation.net_mv_plus_cash @ prior trading day "
     "(530 partitions; 100% non-null measured at 08-20 and 08-21)"),
    ("emv", "Valuation", "DIRECT", "canonical_valuation.net_mv_plus_cash @ date"),
    ("bmv_cash", "Valuation", "DERIVED", "prior-day cash components, declared composition rule"),
    ("emv_cash", "Valuation", "DERIVED",
     "cash_balance_settled_only + money_mkt_funds + bank_sweep_ibf + bank_cash + margin_balance "
     "(composition DECLARED in the contract, not assumed)"),
    ("bmv_accrual", "Valuation", "DERIVED", "canonical_valuation.accrued_income @ prior trading day"),
    ("emv_accrual", "Valuation", "DIRECT", "canonical_valuation.accrued_income"),
    ("performing_bmv", "Valuation", "ABSENT",
     "requires a return-eligibility (performing) classification; no live source"),
    ("performing_emv", "Valuation", "ABSENT", "same"),
    ("position_only_bmv", "Valuation", "ABSENT",
     "position-only (known-not-held) accounts have NO canonical_valuation row; "
     "a-6 is an EXISTENCE join (Q-p3), not a valuation"),
    ("position_only_emv", "Valuation", "ABSENT", "same"),
    # --- External flow (8) ---
    ("external_flow_in_cash", "External flow", "DERIVED",
     "flow_ledger final_class=EXTERNAL, is_in_kind=false, signed_amount>0"),
    ("external_flow_out_cash", "External flow", "DERIVED", "same, signed_amount<0"),
    ("external_flow_in_kind", "External flow", "DERIVED", "flow_ledger is_in_kind=true, in_kind_value>0"),
    ("external_flow_out_kind", "External flow", "DERIVED", "same, in_kind_value<0"),
    ("external_flow_net", "External flow", "DERIVED", "sum of the four above"),
    ("flow_weighted_net", "External flow", "DERIVED",
     "under the declared EOD convention (twr_daily.flow_convention)"),
    ("flow_count", "External flow", "DERIVED", "count of flow_ledger rows in the interval"),
    ("flow_timing_basis", "External flow", "DIRECT", "twr_daily.flow_convention (='EOD' measured)"),
    # --- Fee/tax/income evidence (6) ---
    ("income_total", "Fee/tax/income", "DERIVED",
     "IMPORT c00_account_gains.SB_INCOME (Build Ladder rung 2; imported, never copied)"),
    ("advisory_fee_billed", "Fee/tax/income", "DERIVED",
     "flow_ledger final_class=FEE-MANAGEMENT -- 121,564 rows in 125 of 530 partitions: "
     "PERIODIC, not daily. A single-day census reads a FALSE ABSENT here."),
    ("advisory_fee_accrued", "Fee/tax/income", "ABSENT",
     "canonical_valuation.accrued_income is INVESTMENT INCOME accrual, not fee accrual; "
     "no fee-accrual source on the plane"),
    ("transaction_fee", "Fee/tax/income", "DERIVED",
     "flow_ledger final_class=FEE-ADMIN (2,650 rows estate-wide)"),
    ("tax_withholding", "Fee/tax/income", "ABSENT",
     "no withholding class in flow_ledger; full census = 5 values "
     "{INTERNAL, FEE-MANAGEMENT, EXTERNAL, FEE-ADMIN, UNRESOLVED}"),
    ("fee_timing_adjustment", "Fee/tax/income", "ABSENT", "no live source"),
    # --- Return (7) ---
    ("return_denominator", "Return", "DERIVED", "bmv + flow_weighted_net under the declared convention"),
    ("gross_return_dollars", "Return", "DERIVED",
     "identity-consistent with a-2; residual market gain via the imported core"),
    ("net_return_dollars", "Return", "DERIVED", "same, net of FEE-MANAGEMENT"),
    ("daily_return_gross", "Return", "DIRECT",
     "twr_daily.r_gross -- VALUE-REFUSED at frontier (dtype null; REFUSED-NO-BMV 7335/7335 @2026-08-21)"),
    ("daily_return_net", "Return", "DIRECT",
     "twr_daily.r_net -- VALUE-REFUSED at frontier (same)"),
    ("daily_factor_gross", "Return", "DERIVED", "1 + r_gross -- inherits VALUE-REFUSED"),
    ("daily_factor_net", "Return", "DERIVED", "1 + r_net -- inherits VALUE-REFUSED"),
    # --- Reconciliation (4) ---
    ("observed_after_posted_activity", "Reconciliation", "ABSENT", "no live source"),
    ("known_component_total", "Reconciliation", "DERIVED",
     "valuation_integrity.position_recon_mv + cash_components"),
    ("recon_residual", "Reconciliation", "DIRECT", "valuation_integrity.recon_variance"),
    ("recon_residual_pct_bmv", "Reconciliation", "DERIVED", "recon_variance / bmv"),
    # --- Quality (7) ---
    ("valuation_complete", "Quality", "DERIVED", "valuation_integrity.recon_status vs tolerance_bp"),
    ("flow_classification_complete", "Quality", "DERIVED",
     "nna_canonical.row_quality + flow_ledger.resolution_provenance + in_kind_unvalued"),
    ("method_match", "Quality", "DERIVED", "twr_daily.schema_version vs declared method_version"),
    ("return_eligible", "Quality", "DIRECT", "twr_daily.status"),
    ("quality_code", "Quality", "DERIVED",
     "twr_daily.status + nna_canonical.row_quality + valuation_integrity.recon_status"),
    ("quality_details", "Quality", "DERIVED",
     "the composing statuses carried, not flattened (PRF-d-7: never a 0 where unknown)"),
    ("attribution_coverage_pct", "Quality", "ABSENT",
     "fact_performance_attribution_daily (plan s.3.3) IS NOT BUILT -- a separate table, "
     "not on the canonical plane"),
]

VALUE_REFUSED = {"daily_return_gross", "daily_return_net", "daily_factor_gross", "daily_factor_net"}


def main() -> int:
    groups = {}
    for col, grp, cls, src in COLS:
        groups.setdefault(grp, []).append((col, cls, src))

    print("PRF-a-1 COLUMN AUDIT -- ADVI_PERFRP TO-R1-DS (PRFR1DS-AC1)")
    print("plan:  docs/architecture/ADVI_PERFORMANCE_E2E_STANDARDIZATION_PLAN_20260806.md s.3.2")
    print("live:  gold/advi/canonical (8 tables) + gold/advi/dimensions + BD silver dim_account_xref")
    print("read:  2026-08-24")
    print("=" * 112)
    for grp, rows in groups.items():
        print("")
        print("-- %s (%d) --" % (grp, len(rows)))
        for col, cls, src in rows:
            mark = "   [VALUE-REFUSED]" if col in VALUE_REFUSED else ""
            print("   %-32s %-9s %s%s" % (col, cls, src, mark))

    n = len(COLS)
    absent = [c for c, g, k, s in COLS if k == "ABSENT"]
    direct = sum(1 for c, g, k, s in COLS if k == "DIRECT")
    derived = sum(1 for c, g, k, s in COLS if k == "DERIVED")
    const = sum(1 for c, g, k, s in COLS if k == "CONSTANT")
    m = direct + derived + const
    k_absent = len(absent)

    print("")
    print("=" * 112)
    print("DENOMINATOR: plan columns N = %d   (8 groups, sizes %s)"
          % (n, [len(v) for v in groups.values()]))
    print("  MAPPED  M = %d    (DIRECT %d + DERIVED %d + CONSTANT %d)" % (m, direct, derived, const))
    print("  ABSENT  K = %d" % k_absent)
    print("  CHECK   N = M + K  ->  %d = %d + %d  ->  %s"
          % (n, m, k_absent, "PASS" if n == m + k_absent else "FAIL"))
    print("")
    print("  of the %d MAPPED, %d are VALUE-REFUSED at the current frontier (sourced, null live):"
          % (m, len(VALUE_REFUSED)))
    for c in sorted(VALUE_REFUSED):
        print("     - %s" % c)
    print("")
    print("DECLARED-ABSENT LIST (%d) -- carried in the contract against contract_version, never filled:"
          % k_absent)
    for c in absent:
        print("   - %s" % c)
    return 0 if n == m + k_absent else 1


if __name__ == "__main__":
    raise SystemExit(main())
