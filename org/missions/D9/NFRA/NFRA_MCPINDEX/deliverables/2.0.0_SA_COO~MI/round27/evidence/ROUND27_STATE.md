# NFRA_MCPINDEX round 27 - state (2.0.0_SA_COO~MI, 2026-10-21 ~09:0xZ)

Orders MX-u-1..3 complete, merged (0a7940eb881), proofs valid; round-close-check REFUSED only for reviewer=ABSENT (broker down), as in rounds 25 and 26.

Done:
- Platform labels read from source (MX-u-1, 35 of 35 (tool, adapter) pairs): the `platform` argument is a custodian label from the data (orion: fact_positions / fact_transactions; bdcottonwood: fact_allocations / fact_transactions; eclipse resolve: the Orion fact_positions custodian), a constant (smartx, commonwealth, bd49f: blackdiamond / black diamond), or nothing (schwab accepts no value). The round-26 platform_not_source_label refusals were input errors of that run.
- Re-run with valid labels (runner 8; SCHWAB_ECLIPSE_VALID_LABELS_20261021.json, counts and codes only): Eclipse resolve answers with a custodian label (2 candidates, lag 0 trading days); Eclipse holdings, allocation, fees and transactions refuse on source (vendor_no_holdings, account_not_resolved, no_fee_source, vendor_no_transactions): ruling item 5 for COO~O. Schwab with platform omitted: both masters resolve to non-Schwab candidates and carry no_resolve_source for vendor schwab (ruling item 6 for COO~O); no Schwab account_ref exists to run the chain.
- Commonwealth feed (MX-u-2): manual landing (commonwealth_landing.py --apply) and hand-run silver builders, no schedule, owner ADVI_COTBKF; newest partition 2026-06-23, 83 trading days behind; surprise row Z-W95-S1.
- Sheets labels section (MX-u-3) merged; the 17 sheets regenerated locally (fork), NOT uploaded: the site is HELD for Andrew.

Open (event-gated): routing and battery on candidate e once served (rides OPLGTW batch17, not before 2026-10-22 06:00Z; the trunk catalog stays untouched until then); the per-vendor re-run after OPLGTW round 48. 42 tools with no second client PARKED under this seat.
