# VERIFY #07 -- target: INF_B_03.account_gains.py

- is_real: **True**
- confidence: **confirmed**
- corrected_severity: high

## Reasoning
CONFIRMED. The two operands of B_03's unrealized_gain (INF_B_03 lines 124-126) come from structurally different unit universes, and both fillna(0.0) phantom paths are reachable and feed a served artifact.

Mechanism, source-confirmed end to end:
- market_value: B_03 reads gold/holdings/ (line 55) = INF_B_01 output. B_01 line 120 computes market_value = units * price where `units` is gold/positions_cube/ (INF_A_03). INF_A_03 is "derived entirely from silver/transactions via cumulative unit reconstruction" (cumsum at A_03 lines 147-150; forward-fill expand) with NO canonical clamp. So MV's unit basis = raw-txn cumsum.
- cost_basis: B_03 reads gold/lots/lots_latest.parquet = INF_B_02. B_02 build_lots (lines 286-304) CLAMPS lot current_units to gold/canonical/holdings (INF_B_00 = silver/api_dims/positions_mv, the Orion positions API). B_02's own docstring (269-285) documents raw-txn FIFO "over-retains ... ~3.15x on the Peter Lee book" vs the positions API — the exact reason the clamp exists. So CB's unit basis = positions-API-clamped units.

Thus line 124-126 subtracts a clamped-CB from an un-clamped-MV — different unit counts on divergent books, directionally overstating gains (big_units*price - small_units*cost).

Both fillna phantom paths fire:
(1) cost_basis NaN -> phantom full-MV gain: a position in positions_cube but dropped from lots by B_02's "absent from canonical / H<=0 -> drop all lots" rule -> merge(how='left') at B_03:115-119 leaves cost_basis NaN -> fillna(0) -> unrealized_gain = full market_value; oldest_buy_date NaN -> holding_period_days NaN -> term defaults short_term (132-134). These are exactly the over-retained/phantom positions B_02's docstring enumerates (cash-sweep with no sell-out, disposed/transferred with no captured close), so the trigger data is the documented normal state, not hypothetical.
(2) market_value NaN -> phantom full loss: B_01 line 114 warns the price left-join yields null MV when a ticker has no canonical price for the date -> B_03 gives 0 - cost_basis = -cost_basis.

Served reach: INF_C_05 reads gold/account_gains/, splits by term, and computes estimated_liability = st_gain.clip(lower=0)*0.37 + lt_gain.clip(lower=0)*0.20 -> gold/artifacts/client_tax_liability.json. Phantom gains are always positive and default to short_term, so they are taxed at the top 0.37 rate. INF_C_03 sums unrealized_gain/cost_basis to account level and feeds I_C07 advisor attribution. Both are client-facing.

Adversarial refutations all fail: there is no guard at 124-126 (no NaN preservation, no unit reconciliation) and not even a targeted WARN (main's except only catches a whole-date crash, so the corruption is fully silent — worse than the flag states). The divergence is not "maybe absent"; B_02's clamp exists precisely because it is real and measured (3.15x). The fix was applied to the CB side (B_02 clamp) but never to the MV side (positions_cube/B_01), an incomplete-fix inconsistency rather than intended design.

Severity high (not critical): the corrupted number lands in a SERVED, client-facing tax-liability/unrealized-gain artifact with material overstatement on every divergent-unit account, but it is explicitly labeled advisory/indicative ("not a tax filing artifact", "Advisory only"), it does not crash or abort the chain, and it is not a regulatory filing. Residual: exact live dollar magnitude on the current partition was not quantified (no S3 read performed here); the mechanism is fully source-grounded. Relevant files: data/inf/scripts/gold/INF_B_03.account_gains.py (115-134), INF_B_01.holdings_lots.py (120), INF_A_03.positions_cube.py (docstring + 147-150), INF_B_02.canonical_lots.py (269-304), INF_B_00.canonical_holdings.py, INF_C_05.client_tax_liability.py (127,166-187), INF_C_03.account_performance.py (106-111).
