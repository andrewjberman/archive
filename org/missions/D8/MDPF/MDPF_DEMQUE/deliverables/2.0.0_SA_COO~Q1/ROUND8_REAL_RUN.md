# MDPF_DEMQUE round 8 -- the one real run of each outcome (2.0.0_SA_COO~Q1)

Run 2026-10-11 ~14:5xZ on dell1 at the tree that carries every round-8 merge (t-25+t-26 @5440bfe645, t-28 @c07e5187e6, t-29 @7a5a62a3e2) and
`0.7.0_AE_CloudOps~ZQ`'s t-27 close @6581b1054d (origin/CLOUD read 15:07Z). `round-close-check --round 8`: 5 of 5 orders complete, proof_ok=5,
judgment=0, verdict=MAY-CLOSE. The full demque test folder, run once at this tree as the drain hygiene: 111 passed, 0 failed (it collected with no
INTERNALERROR for the first time since D1-S7).

| outcome | run | result (verbatim, trimmed) |
|---|---|---|
| R1 + D1-S5 tier-keyed history quote (t-25) | `dq_t25_quote.py` | `a: tier=4 finish=2026-10-17 today=0`; `b: tier=1 finish=2026-10-12 today=7322`; `c1: finish=None gap=history allowance per day not positive (ceiling 5858, reserve 7322); history ceiling not measured (claim held)`; `c2: finish=2026-10-24 today=0`; `TQQ-OK`. The SHT8 request that read `allowance_today 0, finish 2026-10-17` at the base now reads 7,322 and 2026-10-12. |
| R2 schedule + re-freeze (t-26) | `dq_t26_real.py` (scratch copy), then the REAL re-freeze @f990583b63 | real file: `REFROZEN finish_date 2026-10-17, superseded_finish_date 2026-10-13`; `quote_vs_actual --request DEMQUE-TR-...` reads ONE ruled quote and prints the superseded one with "rule changed, round 6 R1". `drawer_schedule.py --from 2026-10-12 --days 14` prints `["2026-10-17","2026-10-18","2026-10-24","2026-10-25"]`. |
| R2 standing non-trading-day drawer (t-27, site Z) | `dq_t27_fire.py` on the ledger at origin/CLOUD | `first fire: date=2026-10-11 cells_drawn=5858 outcome=DRAWN drawer=0.7.0_AE_CloudOps~ZQ drawn_before=5858 day_share=5858`; `FIRE-OK`. `quote_vs_actual` at 2026-10-11: `cells_drawn 11716 of 15720, finish 2026-10-17, OPEN`. AC1 `DRW-OK` and AC2 `DRSCH-OK` are `~ZQ`'s (commit ed74597667, task `mdpf-demque-drawer-daily`, daily from 10:00 ET). |
| D1-S8 re-draw of the 32 (t-28 + the issuer's act) | `redraw_stale.py --apply`, then `run_daily_draw.sh` once (2026-10-11 05:26Z-05:35Z); `dq_t28_stale.py` | applied: 32 pacer entries reset, one tier-2 request enqueued. stored: 18 `LOCKED` and written, 14 `REJECTED:LOW_TRADE_AGREEMENT` not written. `STALE-OK n=14 of 141`: **127 of 141 served with seven columns. D1-S8's close condition (141 of 141) is NOT met.** |
| D1-S6 + D1-S7 repairs (t-29) | `dq_t29_tests.py`, `dq_t29_land.py` | `FIX-OK` (upload file 6 passed, land file 7 passed); `COLLECT-OK n=111 land=7`. |

## The 14 names and the lock floor

LCEYX 87.2, FTHSX 40.7, HLMEX 82.3, IWS 83.3, IWP 80.6, IWN 83.2, IWO 79.2, VSEIX 77.2, PFORX 42.9, RPIFX 39.2, VSS 79.3, VWO 87.2, MISIX 82.0,
PIMSX 87.6 (percent of trade dates agreeing, `passed/checked` of the run). Every one is below `lock.py`'s `AGREEMENT_FLOOR_PCT_X10 = 9`, which
locks only at 90 percent, so `price_store.write` left each name's three-column file of 2026-10-09 in place. Whether the floor was in force when
those files were written on 2026-10-09 was not read here. The floor is not this decomposition's to change; the finding is row `MDPF_DEMQUE-D1-S9`.

## What is not read

- FWD-3's Monday 2026-10-12 morning production read (carried; no cell serves it; a trading day quotes 0 for a backfill).
- The remaining 4,004 cells of the TR request: they draw at the drawer's next scheduled fire (Saturday 2026-10-17 per the schedule above).
  The request reads OPEN until then; ON_TIME or LATE is not claimed.
- `dq_t27_sched.py` (AC2) runs at site Z only; it is `~ZQ`'s recorded result, not re-run here.
- `dq_t26_real.py` was hardened after the real re-freeze (it now restores its input from the superseded copy and reads the ledger up to
  2026-10-10), because its original input stopped being true once the real file was re-frozen. Its pre-freeze result was REFRZ-OK at the
  worker's run and at the issuer's run before the act.
