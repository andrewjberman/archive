# VERIFY #02 -- target: INF_B_02.canonical_lots.py

- is_real: **True**
- confidence: **confirmed**
- corrected_severity: high

## Reasoning
CONFIRMED, not refuted. I traced a concrete triggering path end-to-end.

STRUCTURE (INF_B_02.canonical_lots.py): build_lots has exactly one loop, `for (acct_id, tkr), buy_group in buy_groups` (line 247), where buy_groups = buys.groupby(['account_id','ticker']) (line 240) — so its domain is ONLY pairs with >=1 in-window BUY_DESCS transaction. There is no independent iteration over canonical_units anywhere in the file. The entire canonical-anchor reconciliation, including the residual-lot emission (lines 298-304), is nested inside that loop. A canonical-held (account_id, ticker) with zero in-window buys is absent from buy_groups and is never visited, so no lot — not even a residual — is emitted.

THE RESIDUAL PATH IS UNREACHABLE FOR ITS OWN STATED TRIGGER. The else at line 298 fires only when remaining_total <= 1e-9 (line 294), i.e. the pair HAD in-window buys that FIFO-consumed to ~0. But the authors' own docstrings name the intended trigger as ZERO buys: line 282-284 ("H>0 but zero traceable lots") and load_canonical_units line 183-184 ("held position has no traceable buy lots AT ALL"). Zero-in-window-buys => pair not in buy_groups => loop body (residual included) never runs. The recovery is one scope too deep. This map-vs-implementation gap is exposed by the code's own comments, and line 276 explicitly cites "buy history predates the silver window" as an observed under-retention cause — dispositive evidence the triggering input exists in production (a client holding a fund whose acquiring Buy/Transfer-In all predate the txn snapshot window).

DOWNSTREAM IMPACT IS REAL AND UNMITIGATED. INF_D_00.compute_firm_cost_basis_by_year_from_lots (lines 623-663) and INF_D_02._cbby_from_canonical_lots (lines 1190-1240) build the served cost-basis-by-year SOLELY by aggregating cost_basis from gold/lots/lots_latest.parquet grouped by buy_date year. INF_D_02 line 1196-1198 documents this "Fix A" deliberately replaced the trans-amount sum with lots-only, making lots the exclusive position universe for CBBY. A held position missing from lots contributes zero => served cost-basis-by-year understates that account by 100% of the position, silently, no error. INF_B_03.account_gains likewise yields null cost_basis for the missing account.

FIRES IN NORMAL OPERATION. With canonical_units populated (normal full-mode run, fresh gold/canonical/holdings), the missing positions are simply never emitted (no residual injects them). With an empty anchor (fail-open, line 286), those pairs never entered `buys` either, so still absent. Missing either way.

REFUTATION ATTEMPTS FAILED: (a) No second loop over canonical_units exists to catch held-no-buy pairs. (b) The residual path cannot cover the case per (2) above. (c) No downstream backfill re-derives these positions from canonical holdings; the CBBY functions are lots-only by design. (d) It is a silent wrong-output (under-count), not a crash — matches exemplar defect class (6) silent row-drop -> under-counted served number.

SEVERITY: high, matching the flag. It is a systematic, silent understatement of a client-facing tax/cost-basis served number (per-client INF_D_02 advisor_client_detail + firm-scope INF_D_00), scaling with the count of positions acquired before the transaction window — a population the authors explicitly assert is real. Not critical (no crash, no cross-firm leak, no total-AUA headline corruption), but a genuine financial-correctness defect in served output.
