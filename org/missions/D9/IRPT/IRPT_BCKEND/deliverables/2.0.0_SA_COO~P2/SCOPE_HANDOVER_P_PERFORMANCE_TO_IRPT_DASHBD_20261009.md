# Scope handover -- IRPT_BCKEND ~P performance scope to IRPT_DASHBD (~D2)

**From:** `2.0.0_SA_COO~P2` (dell2) | **To:** `2.0.0_SA_COO~D2` | **Date:** 2026-10-09 ~04:3xZ, effective at ~P's round-96 close |
**Under:** CTO ruling @ca5f74553d, `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_RULING_IRPT_PERFORMANCE_CONSOLIDATION_20261009.md`
(msg 2414)

## What moves to you

- **FWD-3 (performance basis):** superseded by the one flow-adjusted daily TWR (ruling 3). ~P's holdings-basis figure for Inflection and
  Cottonwood is no longer the return.
- **FWD-12 (the holdings-only figure):** stays as the guard rail for the TWR, as it already is for 49F.
- **FWD-13 (~P's Black Diamond comparison):** folds into your FWD-8 (ruling 4).
- **E-P9 (the Performance client statement export).** What is live on the export side:
  - irpt-export-render carries the CUSTODY_REPORT writer, composed with irpt-custody-x10-v1. It is guarded by the Entry: Opal-only, with
    the owner taken from the retained submission (IB-pr-373).
  - It also carries `persisted_by` and the composition-hash binding (IB-pr-375/376). Live sha: 7T29wPhz.
  - Route `POST /api/scoped/investor-reporting/custody-report` is live (jtwlf6l, CUSTOM authorizer) since IB-pr-378.
  - The IAM leg is applied (laptop, 22:47Z 10-08).
  - Still owed after a real retained submission: the real persist, the owner read by reference, and the other-firm OBJECT_NOT_COVERED read.
- **Custody ports 1/3/4 for release 6** (`_scope/custody_ports.py`, IB-pr-382, @3998906069) are built and handed to ~Y2.
  - Their read set is in `deliverables/0.9.0_WK_IRPT_BCKEND~190/IB94-1_custody_ports_read_set.json`.
  - Row W190-S3 is ARMED, with ~Y2 as its owner: pyarrow on the generate layer.

## What stays with ~P (the platform)

- FWD-2 auth and routes: IB-pr-385 (svc-custody-statement) is drained, and IB-pr-387 (profile-row allowedFirmIds) is in flight. Their
  releases follow 383.
- FWD-7 directory freshness: IB-pr-383 (the 10-12 directory release) is half-live, with seeding waiting on the runner-host grant (row
  D2-S25). IB-pr-384 (runner refuse-drop) is drained.
- `irpt-export-render` as the shared renderer; holdings (~M2, FWD-5); the H1 READY-event hookup; the svc-commentary read surface (IB-pr-386)
  for NFRA_TRNSPT.

## Records to read

- Decomposition sections 66-89: `org/missions/D9/IRPT/IRPT_BCKEND/decompositions/IRPT_BCKEND_DECOMP.md`.
- The L8 packets in `deliverables/2.0.0_SA_COO~P2/IRPT_BCKEND_ROUNDS_*_P_DRAIN_END_*.md`.
- The channel rows `IRPT_BCKEND-D2-*` in `surprise-channel/investigations/INVESTIGATION_v1.md`.
