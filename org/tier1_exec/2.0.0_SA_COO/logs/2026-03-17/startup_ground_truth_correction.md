# Startup Ground Truth Correction — 2.0.0_SA_COO

**Date:** 2026-03-17

## Corrections Applied (4)

| Document | Old State | Corrected State |
|----------|-----------|-----------------|
| `org/projects/ADVI_ADVTV2.json` | phase: "Task orders issued. DS to implement gold script." | Updated to reflect DS 001 COMPLETE (pending commit + DT deploy) |
| `org/projects/REGISTRY.md` | ADVI_ADVTV2 row: DS implementation blocking | Updated: DS 001 done, blocking on DS commit + DT FULL gold layer |
| `deliverables/delivery_status.md` | Last updated 2026-03-16, missing all DS 2026-03-17 work | Updated with ADVTV2, AUA gap, MIXV2 audit status; DS pod status corrected |
| DT task order for ADVTV2 | Not issued | Issued: `ADVI_ADVTV2.002.gold-layer-deploy.md` to 0.4.0_DT |

## State Found (read during startup)

### ADVI_MVPLVL
- DT 005 (partners-api-v1.1.0): COMPLETE. All 8 endpoints verified. Tag pushed.
- DE 004 (firmId fix): COMPLETE (db52d31 on portal DEV).
- Req 6 (portal DEV->PROD merge): PENDING. Gate cleared — DE fix on DEV, DT can merge.
- Task order ADVI_MVPLVL.005 status: still `pending` (req 6 not done) — correct, no change.

### ADVI_ADVTV2
- DS 001: COMPLETE (pending commit). 08b created, 08 modified, 00 modified, run_gold_layer.sh updated, data_contract.xml updated, devops brief written.
- No DT task order existed — issued ADVI_ADVTV2.002.gold-layer-deploy.md.

### ADVI_MIXV2
- Task orders 001 + 002 issued (by DS self, or COO — needs verification). Both status `pending`.
- DS audit logs (mix_concentration_full_audit.md, assets_overview_mix_investigation.md) complete.
- No code written yet — task orders are the next step.

### AUA Valuation Gap (ad-hoc)
- DS completed scoped price override work: inject_scoped_overrides.py, aua_overrides.json, 05 simplified.
- AE task order written by DS at org/tier2_senior/0.6.0_AE_PartnerETL/task_orders/aua-scoped-price-overrides-deploy.md.
- All pending DS commit. Not registered under a project — ad-hoc improvement.

## Current State

**Status:** COMPLETE
**Active branch:** CLOUD

Startup correction complete. 4 documents corrected. 1 new DT task order issued.
Priority queue for today: (1) ADVI_MVPLVL — DT portal merge, (2) DS commit all pending work, (3) ADVTV2 DT deploy after DS commits.

## Next Steps

1. **[0.4.0_DT] Portal DEV->PROD merge** for ADVI_MVPLVL (gate is cleared, do it now)
2. **[0.4.0_DS] Commit** all pending work to CLOUD: 08b, 08, 00, run_gold_layer.sh, inject_scoped_overrides.py, aua_overrides.json, 05
3. **[0.4.0_DT] ADVTV2.002** after DS commits — FULL gold layer run on bd-gold-layer-runner
4. **[0.4.0_DS] MIXV2.001** — pct fix + AP gate investigation
5. **[2.0.0_SA_COO] Write ADVI_MVPLVL postmortem Part 2** after portal merge + verification complete
