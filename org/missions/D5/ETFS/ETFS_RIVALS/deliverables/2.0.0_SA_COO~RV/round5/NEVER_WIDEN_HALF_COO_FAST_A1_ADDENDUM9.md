# NEVER-WIDEN -- COO HALF, ADDENDUM 9: a G5 row whose shares go 0 -> 0 is not shown as a trade (CVO G8-2), at pin CLOUD 2d511b9058

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~12:0xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-9 half (asked).
**Extends:** the half @4df699fa92 and addenda 1-8. Every gate, key and condition stands.

**Why:** CVO~RV grade 8 G8-2 (P1): 27 of 968 Sep-Oct G5 rows are "exits" with shares 0 -> 0 and no notional (lines
carried at zero shares, then dropped). Two show as trades on the served 2026-10-02 page (TXUE ATD_CN, INEQ JAR_LN). The AI
facts already exclude them (a fact needs a notional). Grade 9 (@33f6db4880) PASS keeps G8-2 open for this act. Code
@0dc03ae8e8, drained 2d511b9058.

## VERDICT: SIGNED (at pin CLOUD 2d511b9058)

## THE PLAN, MEASURED

**Plan: 0 to add, 5 to change, 0 to destroy** (`/c/tmp/rv_apply10.tfplan`, from `/c/tmp/rv-fast` with HEAD = CLOUD HEAD
2d511b9058): the five Lambdas' `source_code_hash` + `last_modified` only; no policy change. Package diff vs the deployed
b973c9fdb9: `publish_page.py` (`no_shares_moved` + the trade-log skip and count), `render.py` (the per-window note). The
G5 producer is unchanged; the served G5 table keeps its rows.

## THE SERVED DELTA, MEASURED (page day 2026-10-02)

Overlay publish at 2d511b9058 over the served inputs vs the served fast-a1-publish-1002c, trace-panel ids normalised (a
removed row renumbers the later trace ids within its fund): **8 hunks**.
- KPI trades 238 -> 236.
- TXUE's and INEQ's window 2026-09-30 to 2026-10-01 goes 1 -> 0 trades; the one 0 -> 0 row's table is replaced by "1
  line(s) carried at zero shares and then dropped (0 -> 0) moved no shares: not trades, not shown."
- Their render_readback reasons (4 -> 3 and 67 -> 66 trace panels) and the page rollup reason.
Status OK, 13 of 13; 1,625,040 -> 1,620,532 bytes; no AI-account, A1 or check-verdict change.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| K1 | the five stage Lambdas' code | b973c9fdb9 (daily 2eP47qLH.., fetch el5nqCzh.., canonical v+HyBuB+.., silver l9poKhq+.., publish SeTRK1+n..) | in place to 2d511b9058 | re-apply from a tree at b973c9fdb9 |
| K2 | platinum page 2026-10-02 | batch fast-a1-publish-1002c | republished ONCE, batch fast-a1-publish-1002d, no `refresh_a1` | prior page kept under `revisions/<ts>/` |
| K3 | the 13:00Z sweep and every later scheduled run | would run b973c9fdb9 | run 2d511b9058 | K1's rollback |

No gold object is written.

## ACT-START GATES

1. Plan exactly 0/5/0. 2. Live base equals K1's CodeSha256. 3. NEVER-2 entry `etfs-rivalfunds-fast-a1-r10` opened AND
committed before the apply (`&&`). 4. Nothing in flight, and outside 12:50-13:15Z; else after the sweep.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 12:50Z:** the served 10-02 page shows 236 trades; TXUE's and INEQ's newest window reads 0 trades with
  the note; no 0 -> 0 row anywhere in the trade log; 13 of 13; AI accounts unchanged (22 PASS / 2 FAIL).
- **Not applied by 12:50Z:** the sweep republishes 10-02 at b973c9fdb9 with the two 0 -> 0 rows. The act follows the
  sweep, and K2 republishes whatever page the sweep left. The keys and rollbacks are the same.
