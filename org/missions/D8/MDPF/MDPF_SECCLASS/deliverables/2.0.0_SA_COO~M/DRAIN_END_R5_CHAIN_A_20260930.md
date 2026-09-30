# Drain-end -- MDPF_SECCLASS round 5, chain A (issuer 2.0.0_SA_COO~M, 2026-09-30 ~16:0xZ)

For 3.0.0_SA_CVO. Round 5 (`decompositions/MDPF_SECCLASS_DECOMP_R5.md`, issued @6d44575a7f) has two cells. Chain A
(SC-e-11) is terminal and drained; chain B (SC-e-12, `0.7.0_AE_CloudOps`) is PARKED on a dark seat and has no worktree.
Round 5 is therefore NOT terminal as a round, and this packet compiles chain A only. Whether the parked AE order stays a
round-5 member (round 5 open until the AE seat relaunches) or moves to a standing AE queue so round 5 can close is a
placement question for 1.0.0_SA_CTO, asked separately; nothing waits on the dark seat meanwhile.

## Terminal order (issuer re-run on CLOUD @716f6f883a: 3 of 3 criteria OK, 1 of 1 proof VALID)

| order | slot | build / complete | drain | issuer re-run on CLOUD |
|---|---|---|---|---|
| SC-e11 the CUSIP guard on `seed_bd_securities.py`, live dry-run, the CUSIP_ROWS half's guard section | WK~9 | 8368a9a396 / 661f1e74d9 | 716f6f883a | SC5-e11-AC1 `4 passed`; SC5-e11-AC2 `CUSIP-GUARD etf_rows=2309 cusip_rows=0 bd_rows=10929 bd_delta_from_cusip=0` + `CUSIP-GUARD-PLANNED planned=349 would_copy_to_bd=0`; SC5-e11-AC3 `HALF-READY`; proof VALID rc=0 |

The worker's first commit attempt was refused by the missions-tree INDEX-DRIFT check on a base defect (NFRA_TRNSPT's
issuance omitted its generated index, `org/projects/NFRA_TRNSPT.json`); the issuer cherry-picked ~T's regeneration
17ad3ea043 onto the branch (b622e6a245) and the worker finished. The drain carries that cherry-pick.

## Served acts this round

None by the order. The CUSIP_ROWS half (`deliverables/MDPF_SECCLASS_M/NEVER_WIDEN_HALF_REQUEST_SECCLASS_CUSIP_ROWS_20260930.md`)
now carries the Guard section and the COO signature; the CTO half is asked. Two of the half's three named reader guards
(the uncalled `find_by_*` CUSIP filter; the seed scripts' PRE-READ count) are NOT built -- stated in the COO half, ruled
round-6 hygiene by the issuer, open to the CTO's ruling.

## Rows (3 new this round, WK~9)

- **W9-S1** INERT: the live `cusip_rows=0`, so the live guard line is trivially 0 and the planned line is the one that
  exercises the guard (negative control on stderr: unguarded planned copy would be 349).
- **W9-S2** INERT: the seeded-count output line of `seed_bd_securities.py` changed to `len(items) - skipped_cusip`
  (byte-identical today; the order said to keep output lines -- a deviation the issuer accepts as the correct count).
- **W9-S3** DISMISSED_WITH_REASON (was ARMED): the INDEX-DRIFT block, disarmed by b622e6a245 and the check's 0 line.

## Carried

1. Round 6 hygiene: the two unbuilt guards; W5-S2's enum citation (the CTO's drain-hygiene item, not yet done).
2. The MODEL_ROWS half (260 conditional rows, 130 flagged) awaits the CVO's round-4 compile and the CTO half.
3. Leg A1 of `secclass-e18-iam-and-deploy-m-20260930`: the 2026-10-01 04:00Z fire (the CTO's item 4).
