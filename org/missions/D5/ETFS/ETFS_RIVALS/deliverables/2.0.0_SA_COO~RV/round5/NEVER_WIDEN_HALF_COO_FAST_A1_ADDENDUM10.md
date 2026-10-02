# NEVER-WIDEN -- COO HALF, ADDENDUM 10: money-market trades off the trade log and the AI facts (CVO G8-3) + CALL 12 notional condition (G10-1), at pin CLOUD f122e4476b

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-02 ~12:1xZ, FAST lease. **Pairs with:** `1.0.0_SA_CTO~Z`'s addendum-10 half (asked).
**Extends:** the half @4df699fa92 and addenda 1-9. Every gate, key and condition stands.

**Why:** CVO~RV grade 8 G8-3 (P2): money-market lines stay out of the rankings and trend (grade 2 F2) but show as trades
(IJGXX for ETFT; DGCXX for PCLG, TSEL, WCMG) and as AI facts (CGIC's account leads with CMQXX flows). Grade 10
(@c3050c9b94) G10-1 (P2, latent): `no_shares_moved` tests shares only, while CRO~RV CALL 12 keeps a 0->0 row with a
notional visible. Code @3a937fbbe3, drained f122e4476b.

## VERDICT: SIGNED (at pin CLOUD f122e4476b)

## THE PLAN, MEASURED

**Plan: 0 to add, 5 to change, 0 to destroy** (`/c/tmp/rv_apply11.tfplan`, from `/c/tmp/rv-fast` with HEAD = CLOUD HEAD
f122e4476b): the five Lambdas' `source_code_hash` + `last_modified` only; no policy change. Package diff vs the deployed
2d511b9058: `publish_page.py`, `render.py`, `ai_accounts.py` (no producer or gold-table code).

## THE SERVED DELTA, MEASURED (page day 2026-10-02)

Overlay publish at f122e4476b over the served inputs vs the served fast-a1-publish-1002d: status OK, 13 of 13.
- KPI trades 236 -> 213: 23 money-market lines leave the trade log, each counted in its window's note. IDVZ 4 (its State
  Street government MMKT sweep was every IDVZ trade in those four windows, so they read 0 trades with the note), CGIC 5
  (CMQXX), SCHY 5, WCMG 4, TSEL 2, PCLG 2, ETFT 1 (IJGXX).
- The affected funds' render_readback reasons and window headers change. 214 tag-only hunks are the weight bars
  rescaling: a fund's bars scale to its largest trade weight, which in CGIC was the MMF line.
- No AI-account, A1, rankings, trend or check-verdict change. The AI-facts change moves only future runs; no stored row is
  re-graded or re-rolled.
- G10-1: today no 0->0 row carries a notional, so the CALL 12 condition changes nothing served.

## THE BLAST RADIUS, PER KEY

| # | key | before | after | rollback |
|---|---|---|---|---|
| L1 | the five stage Lambdas' code | 2d511b9058 (daily cg1v2E5W.., fetch +7kl/NY1.., canonical k2GnyeV5.., silver WoUmyWAV.., publish /VPbdQMH..) | in place to f122e4476b | re-apply from a tree at 2d511b9058 |
| L2 | platinum page 2026-10-02 | batch fast-a1-publish-1002d | republished ONCE, batch fast-a1-publish-1002e, no `refresh_a1` | prior page kept under `revisions/<ts>/` |
| L3 | the 13:00Z sweep and every later scheduled run, incl. the next AI run's facts | would run 2d511b9058 | run f122e4476b | L1's rollback |

No gold object is written.

## ACT-START GATES

1. Plan exactly 0/5/0. 2. Live base equals L1's CodeSha256. 3. NEVER-2 entry `etfs-rivalfunds-fast-a1-r11` opened AND
committed before the apply (`&&`). 4. Nothing in flight, and outside 12:50-13:15Z; else after the sweep.

## EXPECTED OUTCOME, BOTH BRANCHES

- **Applied before 12:50Z:** the served 10-02 page shows 213 trades, 23 money-market notes, 0 money-market rows in any
  trade table, AI accounts unchanged (22/2), 13 of 13.
- **Not applied by 12:50Z:** the sweep republishes 10-02 at 2d511b9058 with the money-market rows. The act follows the
  sweep, and L2 republishes whatever page the sweep left. The keys and rollbacks are the same.
