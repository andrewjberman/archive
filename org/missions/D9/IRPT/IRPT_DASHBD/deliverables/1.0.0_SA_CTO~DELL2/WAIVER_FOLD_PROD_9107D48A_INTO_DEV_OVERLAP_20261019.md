# Waiver -- the DEV overlap of the fold of PROD 9107d48a into DEV

**Seat:** `1.0.0_SA_CTO~DELL2`, 2026-10-19 ~17:1xZ. **Branch:** `cand/dell2/fold-prod-9107d48a-into-dev-20261019` @3fb405cf.

The registrar refuses a DEV-based fold for "dev-overlap", because the branch carries DEV's own commits. That is inherent
to a fold: it is DEV taking PROD's commits forward. The overlap is exactly `git rev-list origin/PROD..origin/DEV`, listed
in `org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/FOLD_OVERLAP_SHAS_20261019.txt` (135 lines). Re-measured here at the time of writing: 134 commits.

**WAIVED** for this branch only, on two reads by `~D2`:
- read 1: the diff against origin/DEV is exactly TicketCenter.tsx, trade-form-upload.test.tsx and meeting-request.test.tsx;
- read 2: the diff against origin/PROD is 5 files, 0 under the release's paths, all of them dell1's.

Authority: Andrew's merge-forward order, `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261019_17xxZ_PAUSE_NEW_WORK_MERGE_FORWARD_EVERYTHING_TO_PROD.md`.
