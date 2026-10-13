# Laptop pare-down receipt -- 2026-10-13 (0.0.0_AB_MSTR)

Authority: Andrew-direct ~13:4xZ, record `org/tier1_exec/1.0.0_SA_CTO/deliverables/ANDREW_DIRECT_20261013_134xZ_LAPTOP_PARE_DOWN_UNSEATED_CLOSES_EXCEPT_SPMOVE.md` @4750e84345; CTO msg 108751; ledger `org/tier0/ledger/LD-0645.md`. Nothing deleted.

## The three counts

- **Register closes: 5 of 6.** ADVI_49FSRC, ADVI_BDPLAT_RESTORE, OPAL_ADVIPOINTERS, ADVI_PERFRP, ADVI_ROSTERCOLS (commit 97bfce4846). Each `org/projects/<CODE>.json` reads `status: closed` with `closed_record`; prior status and phase kept. REGISTRY: three Active rows moved to Completed/Archived, two Completed rows added (no row existed). **LGIC_LGCTFM not closed here:** it is a tree project; its index JSON is generated from `org/missions/D14/LGIC/LGIC_LGCTFM/project.json` (lane TREE_PROJECT_ROW, 1.0.0_SA_CTO's), and missions-tree-check refused the index edit as drift. Routed to the CTO. NFRA_SPMOVE untouched.
- **Orders retired: 9** (commit f66afe0d1a), status flipped to `cancelled` with the record as reason and the prior status kept in the tag. **17 more open orders could not be flipped by this author:** they sit in seat-lane folders under `org/tier2_senior/*/task_orders/` and the lane gate refuses them to 0.0.0_AB_MSTR. Not bypassed. Listed below for their issuer or the CTO.
- **Scheduled task OpalOutsetDriftLaptop: DISABLED** at 2026-10-13T14:29:24Z (`schtasks /Change /Disable`, reversible with `/Enable`). Last run before disable: 10/13/2026 10:15:01 AM local (14:15:01Z), Last Result 0, next run was 10:30 local. After: Status Disabled, Next Run N/A. It ran `infra/aws/ec2/outset-drift-device/publish_drift.py --out-prefix s3://opal-estate-report/outset --trigger scheduled`.

## Orders per project (measured, not the report's figure)

The record cites 74 orphan orders from the laptop CRO report. Measured from the order files' `<status>` tags: **26 open** across the 12 projects named. The other faces read complete / superseded / withdrawn / closed-unspent. The report's figure is not reproduced; the measured one stands.

| project | report said | order files | open (measured) | retired | refused by lane |
|---|---|---|---|---|---|
| ADHC_OWNPTH | 1 | 7 | 0 | 0 | 0 |
| ADVI_49F | 3 | 20 | 1 | 0 | 1 |
| ADVI_BDPARITY | 5 | 7 | 3 | 0 | 3 |
| ADVI_INSURE | 3 | 8 | 3 | 0 | 3 |
| ETFS_GUARDRAIL | 4 | 32 | 0 | 0 | 0 |
| IRPT_CUSTDY | 1 | 21 | 1 | 1 | 0 |
| MDPF_TAXSMA | 6 | 27 | 6 | 6 | 0 |
| NFRA_CLDGRPH | 14 | 49 | 0 | 0 | 0 |
| NFRA_COMPEFFICACY | 2 | 28 | 0 | 0 | 0 |
| NFRA_OUTSET | 22 | 28 | 2 | 2 | 0 |
| OPAL_ADVIPOINTERS | 10 | 21 | 7 (one more face, P4-PINS-CERT, reads 'GROUP PIN CLOSED + GROUP CERT CLOSED': already closed in its own words, not counted open) | 0 | 7 |
| ADVI_PERFRP | 3 | 5 | 3 | 0 | 3 |

Denominator: 6,184 order files under `org/**/task_orders/` and `org/**/task-orders/` (git ls-files), 277 matched to the 12 projects.

## Retired (cancelled)

- `org/missions/D9/IRPT/IRPT_CUSTDY/task-orders/IRPT_CUSTDY.TO-CU-g-2a.real-statement-retained-and-persisted.md`
- `org/missions/D8/MDPF/MDPF_TAXSMA/task-orders/MDPF_TAXSMA.TO-TX-c-2.category-tree.md`
- `org/missions/D8/MDPF/MDPF_TAXSMA/task-orders/MDPF_TAXSMA.TO-TX-o-1.recovery-runbook.md`
- `org/missions/D8/MDPF/MDPF_TAXSMA/task-orders/MDPF_TAXSMA.TO-TX-r-2.gateway-release.md`
- `org/missions/D8/MDPF/MDPF_TAXSMA/task-orders/MDPF_TAXSMA.TO-TX-r-3.activation.md`
- `org/missions/D8/MDPF/MDPF_TAXSMA/task-orders/MDPF_TAXSMA.TO-TX-v-2.journey-harness.md`
- `org/missions/D8/MDPF/MDPF_TAXSMA/task-orders/MDPF_TAXSMA.TO-TX-v-3.consumer-journey.md`
- `org/missions/D11/NFRA/NFRA_OUTSET/task-orders/NFRA_OUTSET.TO-OS-s-22.the-per-device-consumer.md`
- `org/missions/D11/NFRA/NFRA_OUTSET/task-orders/NFRA_OUTSET.TO-OS-s-23.the-group-b-publish.md`

## Not flipped -- lane refused (seat-lane folders), for the issuer or 1.0.0_SA_CTO

- `org/tier2_senior/0.7.0_AE_CloudOps~L/task_orders/ADVI_49F.c02-REEMITRETIRE.the-re-emit-capability-object-plus-driver-retired-together-on-andrews-word-once.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_BDPARITY.P3-EXACT.drive-to-exact-loop.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform~B/task_orders/ADVI_BDPARITY.T1-ORACLE.book-tie-out-qt6-group-grain.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform~B/task_orders/ADVI_BDPARITY.T2-DIMS.portfolio-group-and-bridge.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_INSURE.TO-R1-DS.landing-gold-platinum-planes.md`
- `org/tier2_senior/0.7.0_AE_CloudOps~R/task_orders/ADVI_INSURE.TO-H2-AE.runner-import-safety-and-re-arm.md`
- `org/tier2_senior/0.7.0_AE_CloudOps~U/task_orders/ADVI_INSURE.TO-H3-AE.trigger-sequencing.md`
- `org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/OPAL_ADVIPOINTERS.P4-REPOINT-49F.portal-firm-config-repoint-tolerant-read-then-flip.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/OPAL_ADVIPOINTERS.INF-ONEWRITER.inf-silver-chain-one-producer-per-key-plus-billing-consumer.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/OPAL_ADVIPOINTERS.P3-CLOSE-49F.canonical-root-live-and-dims-scheduled~A.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/OPAL_ADVIPOINTERS.R-WATCH.fam-resumption-watch-plus-pb1-proof-read.md`
- `org/tier2_senior/0.4.0_DT_ClientPlatform/task_orders/OPAL_ADVIPOINTERS.P4-PROMOTE-49F.prod-promote-of-the-repoint-plus-rendered-read.md`
- `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/OPAL_ADVIPOINTERS.P4-PUBIAM-49F.publisher-iam-scoped-put-plus-schedule.md`
- `org/tier2_senior/0.7.0_AE_CloudOps/task_orders/OPAL_ADVIPOINTERS.P5-TEARDOWN-49F.legacy-bd-stage-retirement-event-gated.md`
- `org/tier2_senior/0.4.0_DE_ClientPlatform~D/task_orders/ADVI_PERFRP.TO-R1-DE.books-cards-book-view.md`
- `org/tier2_senior/0.4.0_DS_ClientPlatform/task_orders/ADVI_PERFRP.TO-R2-DS.read-gold-defeated-aliasing-producer-fix.md`
- `org/tier2_senior/0.7.0_AE_CloudOps~G/task_orders/ADVI_PERFRP.TO-R1-AE.publisher-keys-route-chain-stage-iam.md`

## Push state

See the final commit and the CLOUD ls-remote read in the commit that carries this receipt.

