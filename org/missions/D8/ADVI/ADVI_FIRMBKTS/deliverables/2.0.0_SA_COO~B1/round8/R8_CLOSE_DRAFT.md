# ADVI_FIRMBKTS round 8 -- L8 PACKET (DRAFT, written 2026-10-14 ~14:5xZ while the guard's first organic run and act 3 are dated waits) -- 2.0.0_SA_COO~B1

**SUPERSEDED 2026-10-16 by `R8_L8_PACKET.md` (the final packet); this draft is stale (7 orders, two of them then pending) and is kept only as the 10-14 record.**

STATUS: DRAFT. Not sent. The round is NOT counted finished: `FB-m-2` (arm (a) due 2026-10-15 about 13:00Z, read by 14:00Z) and `FB-l-5` (act 3, then the first-day reads 2026-10-16 by 18:00Z) are open.
This file carries what is measured so far; the CVO packet is cut from it when both orders are terminal (or when the CTO carries act 3 to round 9).

## 1. The orders (read from the task-order faces and the commits)

| cell | status | workstream | assignee | handle | merged / closed |
|---|---|---|---|---|---|
| `FB-l-1` | complete | MOVEPLAN | `0.9.0_WK_ADVI_FIRMBKTS~81` | the Inflection move plan (44 moves, 13 retire, 30 open questions) | 5118743acd / a470e794b2 |
| `FB-l-2` | complete | MOVEPLAN | `0.9.0_WK_ADVI_FIRMBKTS~82` | the Cottonwood move plan (30 moves, 6 retire, 14 open questions; canonical home `opal-data-cottonwood`, CTO Q1 ratified) | f90ecab714 / 2b0d526d5b |
| `FB-l-3` | complete | RETIREMENT | `0.9.0_WK_ADVI_FIRMBKTS~83` | the consumer census of 17 retirement candidates (zero-consumer: C2, C3) | 9977d91265 / 7440f2ec7e |
| `FB-l-4` | complete | RETIREMENT | `0.7.0_AE_CloudOps~FB1` | the one real retirement: rule `inf-gold-full-on-bronze-complete` (plan 0/1/3 at 12:44:50Z; read absent live by the issuer) | 4618ae2254 |
| `FB-l-5` | pending | FIRSTMOVE | `0.7.0_AE_CloudOps~FB1` | the first moved trigger: acts 1-2 done (restore 085bdb2f22; floor `advi-inf-publish-daily` created DISABLED; one exercise rolled back on an advisor-publisher defect, D1-S58, ruled `Input` `{}`); act 3 a conditional standing GO | c588c745e6 (acts 1-2) |
| `FB-m-1` | complete | READYHALT | `0.9.0_WK_ADVI_FIRMBKTS~84` | the publisher's readiness guard (data frontier; NNA within 4 days; 6 tests; purely additive, 105 lines) | 987e2ca3f9 / b0d0896665 |
| `FB-m-2` | pending | READYHALT | `0.7.0_AE_CloudOps~FB1` | deploy the guard and read its arms: deployed (code hash qZ90srrn..., verified live by the issuer), arm (b) halt read (0 keys written), arm (a) owed | 4f5ef9102f (apply, arm b) |

Terminal 5 of 7. Not terminal: `FB-l-5`, `FB-m-2`.

## 2. FWD inputs measured this round

- FWD-9 (the move plan and the retirement of legacy operations): (a) the ONE plan document `ledger/FWD9_MOVE_PLAN.md` @2b0d526d5b indexes both per-firm records (74 moves); the CTO read the plan's first moves (msg 5530) and left the FWD-9(a) grade to L9. (b) the first real retirement is DONE and read (`FB-l-4`).
- FWD-5 (the owner sees nothing aimed at the old home): the first moved trigger is half done. The exec-summary trigger is under Terraform again (restore 085bdb2f22 after the CRO's registry row 9edbf38575); the portal publisher's new trigger (the floor) exists and is exercised once, but the switch (act 3) waits on the guard's publish arm. No grade offered.
- FWD-4, FWD-6, FWD-7, FWD-8: unchanged this round.

## 3. Rows to disposition at the packet

- ARMED / BLOCKING: `D1-S57` (the exec-summary `main.tf` stray revert: disarmed by the restore commit 085bdb2f22, per the CTO); `D1-W84-S1`, `S4`, `S8` (the readiness signal, disarmed by the CTO's rulings 5552 and 5571); `D1-W75-S2` (B_01 silver-noncash cap, the CRO's pricing brief; unchanged); `D1-W80-S1` (Door 6 second consumer: the plan names its successor M03; the CTO disarms when M04 lands); the carried round-7 ARMED rows owned elsewhere.
- Round-8 observations to list: `D1-W81-S1..S11`, `D1-W82-S1..S6`, `D1-W83-S1..S5`, `D1-W84-S5..S10`, `D1-S58`.
- Carried: `FB-h-5` (the live FWD-4 half; owner the CTO), `D1-S43` (NFRA_CTLPLN, laptop).

## 4. Not yet known (named)

- Whether the guard publishes on a normal day through the live path (arm (a)): 2026-10-15 about 13:00Z.
- Whether the floor, with `Input` `{}`, publishes the advisor artifacts through the advisor publisher without error, and whether the 16:30Z catch-up halts with zero writes: the first-day reads, 2026-10-16.
- The Cottonwood and Inflection moves beyond the first (the plan's rows M05 onward) are not started; Inflection Q2 (the cutover date for the 45-day window) gates M05.
