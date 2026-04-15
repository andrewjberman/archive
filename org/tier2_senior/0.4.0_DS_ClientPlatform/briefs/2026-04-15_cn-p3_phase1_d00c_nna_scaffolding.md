# CN-P3 Phase 1 — D_00c NNA Cutover Scaffolding (pre-flight)

**Date:** 2026-04-15
**Agent:** 0.4.0_DS_ClientPlatform~B
**TO:** ADVI_ROLLUP.CN-P3 (staged behind CN-P1 + CN-P2)
**Status:** pre-flight scaffolding only; no code

## <run>comp-pipescript io D_00c</run>

Current reads (8): account_performance, account_team, advisor_assignments, advisor_fee_detail,
canonical_nna, client_dimension, fee_rate_history, rel_architect_lookup.

**`canonical_nna` prefix** (`gold/canonical/nna/ [PREFIX]`) — the current NNA read surface.
Post CN-P1+P2 shadow landing, CN-P3 cutover swaps this read to `gold/canonical/nna_atomic/`.

## D_00c NNA aggregation file:line inventory

Source: `data/black_diamond/scripts/gold/D_00c.portal_leaderboard.py`

| Line | Site | Action (CN-P3) |
|------|------|---------------|
| 112-135 | `_load_canonical_nna_account_level()` returns `DataFrame[date, account_id, daily_inflow, daily_outflow, nna_txn]` from `canonical_nna/` | Switch source to `canonical_nna_atomic/` with equivalent schema (verify column parity post CN-P1) |
| 183 | `.agg(nna=('nna_txn', 'sum'))` account-level rollup | No change — column name `nna_txn` preserved |
| 242 | `.agg(nna=('nna_txn', 'sum'))` second rollup path | No change |
| 292 | `.agg(nna=('nna_daily', 'sum'))` 08c-derived leaderboard build | 08c = advisor_fee_detail (upstream), NOT canonical_nna — leave unchanged |
| 328 | `.agg(nna=('nna_daily', 'sum'))` secondary 08c path | Leave unchanged |
| 1023 | `fut_nna = pool.submit(_load_canonical_nna_account_level)` loader entry point | One-line swap lands here |

## CN-P0 consumer memo cross-check

Memo `docs/data/nna_atomic_consumer_enumeration.md` confirms P3 scope = D_00c, entry point
`_load_canonical_nna_account_level`. Matches inventory above. Line 1023 is the single
runtime swap; the function body (112-148) is the schema swap surface.

## Expected <expect> checks (Phase 1)

1. `<expect>` Reads include nna_atomic canonical post CN-P1+P2 — **PRE-RERUN**, TBD. Currently reads `canonical_nna/` only.
2. `<expect>` File:line inventory of D_00c NNA sites — **PASS** (table above).

## Ready-to-execute checklist (when CN-P2 lands)

- [ ] Flip CN-P3 status `staged` -> `pending`
- [ ] Edit `_load_canonical_nna_account_level()` prefix + column read list
- [ ] Verify zero-byte diff on non-NNA fields of `platinum/firm/leaderboard.json`
- [ ] Travis NNA leaderboard ↔ D_02 summary parity within $0.01
- [ ] Co-ship with RA-P3 (paired cutover)
