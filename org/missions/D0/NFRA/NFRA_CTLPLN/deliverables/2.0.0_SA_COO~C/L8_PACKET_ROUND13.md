# NFRA_CTLPLN round 13 -- drain end and L8 packet, for 3.0.0_SA_CVO~L and 1.0.0_SA_CTO (issuer 2.0.0_SA_COO~C, 2026-10-14 ~21:2xZ)

All seven round-13 orders are terminal: six `complete`, one `parked` (`TO-CT-ac-5`, held on Andrew's word ~20:49Z, CTO ruling msg 109252, record `CT-ac-5_RESTART_HELD_20261014.md` in this folder). `python .tools/round-close-check.py --project NFRA_CTLPLN --round 13` reads `verdict=MAY-CLOSE` with `judgment=2 graded=2 ungraded=0 self_graded=0` (both judgment criteria are the earlier `TO-APPLY-9` and `TO-APPLY-31` AC2, graded MET by you). Pins are commits on `box/laptop`; the issuer's own re-run of each cell is in the order's `<status_reason>`.

## 1. Judgment criteria owed to the CVO

None new. `CTac5-AC2` belongs to the parked order and is not graded this round; it returns when the restart is cut fresh.

## 2. Cells, their orders and the issuer's own re-run

| cell | order status | merge or commit | issuer re-run |
|---|---|---|---|
| `CT-ac-1` | complete | `2bf798e271` | `CROSSBOX-TEST cases=71/71`; `ROUND13-BATCH arms=15/15`; `APPLY-GATES-TEST cases=100/100`; `simulate_policy.py` deleted |
| `CT-ac-2` | complete | `e7d28c398b` | `STOP-AT-DESCENDANT cases=27/27`; `SEAT-BOUNDARY-TEST cases=39/39 wired=both` |
| `CT-ac-3` | complete | `e581a6975c` | `FENCE-SCOPED ... sim_ok=31/31 refusals_ok=5/5 ... ok=True`; relocation attributed `057cfa8a1c` |
| `CT-ac-4` | complete (seat `~U7`) | listing `76bd3d4dcf`, proof row `e0dcb80218` | `CENSUS saved_before=233 live=238 added=5 removed=0`, `census_in_sync=True` |
| `CT-ac-5` | parked | `4e9f71fe08` (status), `53c8d3cc7c` (amendment 3) | none; no restart happened; S0 at 20:15:08Z (`403fbe344e`) is superseded when a window is set |
| `CT-ac-6` | complete | `2d35ab062c` | `UNBLOCK-OWED-FOREIGN cases=6/6`; `UNBLOCK-SELFTEST cases=32/32` |
| `CT-ac-7` | complete | `1f86074dba` (on CLOUD) | `PROOF-JUDGMENT-EXPECTED cases=4/4`; checker self-test 63 of 63 (base 59) |

## 3. Outcomes

`FWD-11` (a box restarts mid-round and nothing is lost) is NOT exercised: the one approved restart was held by Andrew. The CTO qualifies it in the round-13 analysis as a wait on Andrew's word (open call `laptop-20261014T205216Z-7841`). `FWD-9` is PARKED (CTO ruling, no account held). `FWD-27` read back 3 of 3 on 2026-10-13. No UI is touched, so no screenshot.

## 4. Rows this round minted or routed

`W87-S1`, `W87-S2` (CT-ac-1; `routes.tf` comments at about :23 and :30 still name `simulate_policy.py`), `W88-S1` (ruled), `W89-S1..S3` (CT-ac-3; the pre-rows scopes lack `restricted_prefix_hosts`, the lgic fence files never append `fence_scoped_allow_statements`), `W90-S1` (accepted), `W91-S1`, `W91-S2` (`coverage-frame` prints as `VIOLATION:`), `S9123` (fixed by CT-ac-6), `D2-S5` (fixed by CT-ac-7). Carried and unchanged: `S9118`, `S9119`, `S9120`, `W8-S7`, `Z-S3`, `W12-S1`, `S9103`, `NFRA_MCPINDEX-Z-W34-S8`. The full round-14 input list is `ROUND13_INPUTS_FOR_ROUND_ANALYSIS.md` in this folder.

## 5. Not measured here

The reached-roles census freshness against the five new protected functions (`derive_reached_roles.py --check-fresh` did not finish offline); the open-ARMED count (the CVO's pass-2 figure stands); the PRD FWD grade table, which the CTO's coverage read governs.
