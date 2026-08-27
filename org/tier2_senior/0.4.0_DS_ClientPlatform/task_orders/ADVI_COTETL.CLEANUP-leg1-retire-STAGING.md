# ADVI_COTETL.CLEANUP Leg-1 — RETIRE dead account_gains->C_00->C_02 path — STAGED (HELD, not applied)

**Status:** complete -- EXECUTED 2026-06-22 ~1758Z (AE-first coordinated landing). AE de-chain DONE (7240a8933, live-verified -- SPRING-CLEAN 2026-08-25: closed WITH project ADVI_COTETL (no directive attachment). Record act, not a work verdict.
C_00/C_02 gone from opal-cot-gold-run); DS landed AFTER: D_00/D_00b fallback->fail-loud-raise (1703ac61d, deployed
[cot], structurally proven no-silent-return) + C_00/C_02 source DELETED (bba478b66). Functional retire COMPLETE.
RESIDUAL: 2 inert S3 code-orphans (code/gold/C_00.py,C_02.py -- safe-deploy doesn't S3-delete; de-chained-harmless)
pending sanctioned-delete decision (RAVC AE+COO 175855Z). Nightly-verify (served $395.30M unchanged) rides tomorrow.
Original ruling+plan retained below.

**[ORIG] Status:** STAGED-READY, HELD. CTO ruled RETIRE (173237Z) + ENDORSED coordinated-queue (173738Z).
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
**CTO fail-loud guardrail (174605Z):** removal must FAIL LOUD, NOT silent-empty — replace the `except` body
with an EXPLICIT raise (`except Exception as e: raise RuntimeError("cot snapshot-first: account_performance
required, no client_performance fallback") from e`), NOT a bare except-deletion (which could let a raw error
propagate or return empty). Verify it ERRORS VISIBLY (don't trade one silent failure for another).
1. **D_00.portal_aggregates.py `_load_perf` (lines 286-292):** replace the `except Exception:` CLIENT_PERFORMANCE
   fallback (print WARN -> _load_parquet(CLIENT_PERFORMANCE) -> return df,None,False) with the explicit RuntimeError
   raise above. account_performance (C_03 snapshot) is required for cot; the silent-stale C_02 fallback IS the
   freeze-bug class the CTO named -> fail loud instead.
2. **D_00b.portal_timeseries.py `_load_perf` (lines 1294-1300):** same — replace the CLIENT_PERFORMANCE fallback with the explicit RuntimeError raise -> fail-loud.
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

---
**RECONCILE-NOTE 2026-06-23 (KEEP-OPEN)** (COO /drive 132528Z): the C_02 multi-leg rewire -- Leg-1 retire DONE (bba478b66 + AE de-chain 7240a8933) + Leg-2 ruff DONE (5d43b4304) + Leg-3 C_03-cross-val-retire DONE today (ec5831836). STILL-OPEN: Leg-3 C_01-cross-val (deferred-careful, woven into worker, CTO-approved) + Leg-4 re-census + C_02-artifact-removal. KEEP.
