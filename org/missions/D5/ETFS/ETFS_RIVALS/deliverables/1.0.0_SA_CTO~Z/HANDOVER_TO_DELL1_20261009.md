# ETFS_RIVALS -- HAND-OVER to DELL1 (`1.0.0_SA_CTO~Z` to `1.0.0_SA_CTO~DELL1`), 2026-10-09 ~02:0xZ, MID-ROUND on Andrew's word

**Orders:** Andrew-direct ~22:5xZ 2026-10-08 (record @b7361ceb2a), then ~01:5xZ 2026-10-09 at this terminal, VERBATIM: "i just
canceled your spawns, those agents are on DELL1 now, thats where they can work" (record
`org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261009_014xZ_RESAPP_BBG_ASKS_VIA_BACKFILL_QUEUE_NO_UNBLOCK_NEEDED.md`).
His second word moves this project with round 28 in flight, which overrides `1.0.0_SA_CTO~DELL1`'s term 4 for this project.
**Census:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_DELL1_MOVE_BBG_AND_LOCAL_DEPENDENCY_CENSUS_20261008.md` @6a308cd424.

## State at hand-over

| item | value |
|---|---|
| tree row | `org/missions/D5/ETFS/ETFS_RIVALS/project.json`: `active`, `EXECUTING`, `fabric: site-z`, `coo_lane: 2.0.0_SA_COO~RV` (no live process since ~01:04Z). DELL1 re-places it and seats a COO and a CVO |
| PRD | `prd/ETFS_RIVALS_PRD.md` v0.21 @92d5e920c3: ADMITTED; ratified-text half SIGNED by `3.0.0_SA_CVO~RV` (@a44d9bcd47) |
| round 28 | both orders terminal (aw-1 merged; tc-1 on its branch); L8/L9 slug 32017 (`ADJUDICATION_v39.Z.md` @bed765812d); aw-1 J1 and tc-1 J1 NOT MEASURED by design; analysis `ledger/ROUND_ANALYSIS.round22.md` ADDENDUM 7 @0820f6b0b7. Round 29 cuts nothing; round 28 closes on three paired acts |

## Acts owed, in order (each under its own pair; the first is signed)

1. **aw-1 Lambda deploy at pin 39889dd4d7, both halves SIGNED.** COO half @d3d6c3e73f; CTO half
   `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_HALF_ETFS_RIVALS_R28_AW1_DEPLOY_20261008.md` @a0ee589cc2. **Window: 2026-10-09
   after the 11:00Z chain's REPORT lines and before 12:55Z**, never inside 10:55-11:15Z or 12:55-13:15Z. The plan must read
   0/5/0, package only. A NEVER-2 entry is opened before and closed after. **The applier is site Z's `0.7.0_AE_CloudOps~Z`**, on
   the order of DELL1's COO (Andrew ~22:0xZ, record `ANDREW_DIRECT_20261008_220xZ_ONE_LAPTOP_APPLIER_EXCEPTION_YES.md`). aw-1 J1
   reads the 13:00Z sweep.
2. **tc-1 merge** of `wk-ETFS_RIVALS-22` @b0b65368fb (on origin as a branch), after tw-1's J1 reads the 2026-10-09 11:00Z vehicle
   run. Its own pair. This is a site-Z producer path, so the CTO half is `1.0.0_SA_CTO~Z`'s, signed before the merge.
3. **The switch-on** (`RIVALFUNDS_HISTORY_OWED`), per R24: cap 20,000 returned records a run (Andrew's card 5), after both. Its own pair.

## Open deploy ledger

`org/critical_paths/.open_deploys/etfs-rivalfunds-r27.json`: OPEN, author `2.0.0_SA_COO~RV`. L1 closed. **L2 owed:** the first
scheduled run on the round-27 package, at the 2026-10-09 11:00Z chain and 13:00Z sweep. **It needs a DELL1 owner** to read L2 and
close it. A dead owner on an open ledger is a NEVER-2 exposure.

## Site-Z producers (census; they stay on site Z)

The holdings collector and the enrichment (`security_market`, corporate actions, names) are legs of the 11:00Z daily Bloomberg pull.
So is the close-price backfill / history-owed step. The budget ledger sits beside the Terminal, and graders read the pull log
`%USERPROFILE%\opal_bbg_logs`. The five Lambdas and both cloud schedules run in AWS, so DELL1 reads their outputs as they are. A DELL1
change to a producer path is a site-Z deploy under a pair.

## Acts only Andrew can do (cited)

None owed in this round. FWD-24 stands NOT REALIZED until the switch-on (item 3).

-- 1.0.0_SA_CTO~Z
