# ADVI_COTETL.CLEANUP Leg-1 — RETIRE dead account_gains->C_00->C_02 path — STAGED (HELD, not applied)

**Status:** STAGED-READY, HELD. CTO ruled RETIRE (173237Z) + ENDORSED coordinated-queue (173738Z).
**Do NOT commit/apply the DS diff ahead of AE's SSM-drop** (deleted-but-chained = half-landed chain failure,
NEVER-rule in spirit). COO schedules the coordinated DS+AE landing on a non-P0-adjacent window, under a
deploy-completion ledger. Leg-2 (C_01 ruff) already DONE+deployed (5d43b4304).

## PRE-GATE (banked, CLEAN — CTO-accepted)
- **comp-blast** C_00.canonical_performance -> C_02.client_performance -> D_00/D_00b (gold). **0 LIVE consumers**:
  C_02 is FALLBACK-ONLY (D_00:291, D_00b:1299 except-branches), never fires since C_03 account_performance
  (snapshot) is primary + always present. Served surfaces all @06-18 confirm C_02@06-09 is never served.
- **Portal-consumer check:** the only 2 portal refs to client_performance (AdvisorIntelligence
  PartnerAnalytics:234, DistributionTab:3073) are COMMENTS describing 49F's $1.70B lineage — NOT cot reads.
  0 direct portal/served reads of cot C_02.
- **Firm-sep:** cot fork only; 49F/bd C_00/C_02 + INF_* are separate forks, untouched.

## DS-LANE STAGED DIFF (author at landing-time; held now)
1. **D_00.portal_aggregates.py `_load_perf` (lines 286-292):** remove the `except Exception:` CLIENT_PERFORMANCE
   fallback -> FAIL-LOUD (account_performance is required for cot snapshot-first; raise a clear error if absent,
   rather than silently serving stale C_02 — the silent-stale fallback IS the freeze-bug class the CTO named).
2. **D_00b.portal_timeseries.py `_load_perf` (lines 1294-1300):** same — remove the CLIENT_PERFORMANCE fallback -> fail-loud.
3. **Delete** `data/cot/scripts/gold/C_00.canonical_performance.py` + `C_02.client_performance.py` (the dead lots-path producers).
4. **D_00c.portal_leaderboard.py = NO CHANGE** — it has NO C_02 fallback (its "falling back" lines are
   role_aua/account_team, unrelated). The CTO "D_00/D_00b/D_00c" list over-included D_00c; verified clean.
   (Also remove now-unused CLIENT_PERFORMANCE imports from D_00/D_00b after the fallback removal — ds-commit-gate F401.)

## AE-LANE (sequenced FIRST / atomic)
- Remove `C_00` + `C_02` from the cot SSM gold chain `infra/aws/terraform/cot-pipeline/ssm.tf:234`
  (currently `canonical: B_00 C_00 C_01 C_02 C_04` -> `B_00 C_01 C_04`). AE/terraform lane.

## HARD ORDER (the sequencing hazard)
AE de-chains C_00/C_02 from ssm.tf:234 **BEFORE or atomically with** the DS script-deletion. Else the next
nightly runs a deleted-but-still-chained script -> gold chain FAILS -> half-landed destructive change.

## VALIDATION (on the coordinated landing's ONE nightly — no ad-hoc run)
Served firm-AUA $395,300,238 + all 7 surfaces (clients_tab, header_metrics, dashboard, mix_summary,
timeseries_overview, leaderboard, dashboard) @ data_as_of=06-18 **UNCHANGED**. Any movement -> rollback + surface.

## NON-URGENT
Benign dead-path, 0 consumers. Zero rush. Stage held; COO sequences the coordinated DS+AE landing.
