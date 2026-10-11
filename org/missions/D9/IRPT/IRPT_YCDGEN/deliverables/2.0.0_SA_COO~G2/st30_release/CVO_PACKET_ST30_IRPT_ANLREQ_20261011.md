# CVO packet -- IRPT_ANLREQ -- the one resident release st30 (installed 2026-10-11T10:32Z)

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

## This project's share (workstream G holds the resident releases; release 4's schema and receipt)

| change | state | what would exercise it |
|---|---|---|
| S2: a request carrying `ticket_id` is admitted by the resident, and its READY receipt names the ticket (V1: the packaged request schema names `ticket_id`) | APPLIED, UNEXERCISED | TCKT_VNEXT's fourth run, on the YCharts producer path, under that project's own pair; `REL4-READ5` is the criterion on that run. A run ending ATTENTION exercises the admission only |
| S5: each READY logs `WARN: ANALYSIS_READY_QUEUE_UNSET <request id>` and sends nothing (AR-g-21) | APPLIED, UNEXERCISED | that run reaching READY. V1: 0 warnings, 0 send failures, because no READY has happened |
| S7: `AnalysisReport` v1 and v2 gain the optional `retained_ref` | APPLIED, UNEXERCISED | the first report persisted |

INERT on this root, by its bindings (V1 printed both counts 0): the packager poll and the analysis-ready SEND. No
commentary queue binding and no analysis-ready queue binding was added. The pre-read STOP passed: the variable
`IRPT_ANALYSIS_READY_QUEUE_URL` read 0 in the unit Environment, the running process and the unit files.
