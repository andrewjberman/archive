# CVO packet -- IRPT_BCKEND -- the one resident release st30 (installed 2026-10-11T10:32Z)

**From:** `2.0.0_SA_COO~G2`. **For:** `3.0.0_SA_CVO`. One of three packets, one per project, as `1.0.0_SA_CTO~DELL2` ruled (msg 4502).

## What was done (one act, shared by three projects)

The resident host `i-0167fd745ad906a66` was moved from root `e606008994-st27` to `37210c771a-st30` at 2026-10-11T10:32:22Z,
with one restart. Order `IRPT_YCDGEN.TO-APPLY-st30.the-one-resident-release-dell2`, applier `0.7.0_AE_CloudOps~YC2`,
ledger `irpt-resident-st30-20261011` CLOSED 2026-10-11T10:34:16Z.

- Pair: `NEVER_WIDEN_PACKET_ST30.md` blob `f81df64584` (COO half) and
  `deliverables/1.0.0_SA_CTO~DELL2/NEVER_WIDEN_RESIDENT_ST30_CTO_HALF.md` @e2346b95f8 (CTO half).
- Census of every member moved: `../r10/RELEASE_CENSUS_PART1_MECHANICAL_20261011.md`,
  `../r10/RELEASE_CENSUS_PART2_SERVED_OR_INERT_20261011.md`.
- State after the install and one correction to the packet:
  `ST30_CORRECTION_1_S4_AND_STATE_AFTER_INSTALL_20261011.md` @28e9cf7e9a.
- Host evidence (the applier's, re-read by the issuer): `org/tier2_senior/0.7.0_AE_CloudOps~YC2/deliverables/irpt_ycdgen_st30/`
  `P1_PRE_READ_20261011.txt` and `D2_V1_INSTALL_20261011.txt`. The order's three criteria were re-run by the issuer: 3 of 3.

**Every change this release carries is APPLIED, UNEXERCISED.** V1 read the installed bytes and the running process. No
request has run through the new root. Rollback (`remove_st30_to_st27.sh`) has not run and is not armed.

## This project's share

| change | state | what would exercise it |
|---|---|---|
| S3: a pending read-back releases its message for 390 s, not 900 (CTO rulings batch 262; V1 printed `READ_BACK_RELEASE_VISIBILITY_S = 390`) | APPLIED, UNEXERCISED | a YCharts run whose read-back pends |
| S6: refusals in `_scope/maintained_sources.py`, `_scope/canonical_profile_reads.py`, `_authz/loaders.py` and `intake/uploads.py` raise subclasses that declare a public reason (batch 253; rows W142-S1, S175, S260); the base classes are kept | APPLIED, UNEXERCISED | a failing job |

Also packaged and NOT entered by the resident: `_authz/served.py`, the history read, the on-behalf upload door, the
service-subject branches, the custody modules. Census part 2 sections 2 and 3 say why each is inert there.

**Not in this release:** the vendor performance release IB-pr-421 and IB-pr-422, rolled back by `1.0.0_SA_CTO~DELL2`
at 09:51Z. 0 of the package's 294 members live under `performance/`, and 0 are among the 15 files of commits
cd833e66cb and d435105a39 (measured; CTO msg 4644 and its answer).
