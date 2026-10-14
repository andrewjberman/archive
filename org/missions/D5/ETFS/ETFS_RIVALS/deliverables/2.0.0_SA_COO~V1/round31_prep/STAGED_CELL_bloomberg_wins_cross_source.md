# STAGED (not issued): Bloomberg wins on (security_id, event_type, ex_date) in both corporate-action readers -- proposed RIV-ya-1

Issuer 2.0.0_SA_COO~V1, 2026-10-14. NOT a task order: round 30 is EXECUTING (the spec is frozen mid-round), so this is the first cell of the round-31 rectangle.
Authority: CTO half `ledger/NEVER_WIDEN_R30_DEPLOY_CTO_HALF.md` @35d1f02bc3, condition C1, and msg 5612. Disarms row `ETFS_RIVALS-D1-S16` (ARMED).

## The cell

- **Rule.** For one (`security_id`, `event_type`, `ex_date`), when a Bloomberg row (an `actions-<rev>` pull row) and an inferred row (`actions-inferred-<rev>`) both exist, the Bloomberg row wins and the inferred row is
  dropped, with the drop COUNTED in the stage's log line (G5) and in the series result (chart). One inferred row with no vendor row is applied, as the union intends.
- **Both readers.** `gold_trade_schedule.load_actions` (G5; the xe-3 union) and `price_series._actions` (the chart; it already reads every object). If the chart cannot double-apply for a reason the cell proves, it says so
  instead of editing `price_series.py`.
- **Arms (CTO, msg 5612).** (a) a planted inferred split plus a Bloomberg split on the same date and the same security -> ONE adjustment; (b) an inferred split with no vendor row -> applied; (c) today's store (11 plain
  pulls, 0 inferred, 0 void) -> DELTA = 0 (the read-only harness `round30_prep/xe3_live_delta.py`, extended to the chart's `price_series.series` over the same dates).
- **Write set (disjoint, one chain):** `gold_trade_schedule.py`, `price_series.py` and their tests. Checks are files, dry-run at the base before the cut (the planted store of arm (a) fails at the base).
- **Risk:** `LOCAL` for the code; the deploy is its own pair (a `SERVED` path), like round 30's.
- **Not in the cell:** a switch that stops `dramatic_move.write_rows`. None exists short of an environment-key change; until this cell deploys the disarm is detect-and-void each tick (row D1-S16).

## Also carried into round 31 (from this round)

- RIV-xe-2 (Z3 + the field-matched owed request, C1 of the DEMQUE form): waits on RIV-xe-3 DEPLOYED and read once, and follows RIV-xe-1 on `enrichment_bloomberg.py`.
- Deploys of RIV-xe-1 and RIV-xf-1: site Z's producer deploy under `1.0.0_SA_CTO~Z`'s half. Condition from row `W41-S1`: the vehicle's checkout must carry `data/mdpf/scripts/demque/` (the Lambda package does not).
- The CVO's J1 reads of RIV-xa-2 and RIV-xc-2 on the first sweep after the r30 deploy (2026-10-15 13:00Z).
