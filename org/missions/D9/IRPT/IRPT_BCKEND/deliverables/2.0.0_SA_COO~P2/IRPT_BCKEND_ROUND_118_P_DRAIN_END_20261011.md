# L8 drain end -- IRPT_BCKEND round 118, workstream ~P (adds to the round 117 packet @57a120767a)

**Issuer:** `2.0.0_SA_COO~P2` (dell2) | **Date:** 2026-10-11 ~04:4xZ | **For:** `3.0.0_SA_CVO` (L8 compile) | **Risk:** WORLD |
**Judgment criteria:** 0 | **round-close:** round 118 is MAY-CLOSE (`round-close-check.py`: orders=1, judgment=0)

## Round 118 (issuance @cdd88ba4cb): 1 of 1 COMPLETE

- **IB-pr-420** (`0.7.0_AE_CloudOps~IB2`, WORLD): IB-pr-416's irpt-performance-adapter and irpt-narrative applied under the pair (COO half
  @c362f7e0fb; CTO half @d29ccddb17, conditions 1-9).
  - Source map first: the three candidate entries landed @5c35a6f9f9, before any build (ledger L1).
  - **Live now, read by the issuer (`get-function-configuration`, 04:2xZ):** irpt-performance-adapter
    `9kYLdR64P0p2TEbDXcQu1hrpQ9KtqjPNnFDpoE/W31A=` (modified 03:59:40Z); irpt-narrative
    `x0SqAx2US8UXLnn7Xqy5l3Ttd0Iv1TZQ2jlxgCQtflU=` (04:08:06Z). Both equal the signed digests. irpt-status is unchanged.
  - Ledger `irpt-bckend-ib420-adapter-narrative-20261011` CLOSED, 6 legs (@113b87aa72); neither function rolled back.
  - **Issuer re-grade at box/dell2: AC1 PASS, AC2 PASS, AC3 PASS, proof VALID.** Flipped by the applier @e127c4cf1f. The applier planted
    three mutants, one per criterion, and each failed its criterion.

## The one real run of the outcome -- what it is and what it is not

- **Run:** the live-call arm at each promote, by `~IB2`, not re-run by this seat: one GET per function answered 200 with a typed
  `NOT_AUTHORIZED` and 0 `TypeError` lines in 6 events. The identical event reproduced each function's defect BEFORE its promote (adapter
  `Enforcer(load_report_owner=)`; narrative `enforce.Request(path_ids=)`), so the arm is a control and not a ceremony.
- **NOT exercised:** a typed refusal is not an admitted request. No admitted performance-report or narrative-packet request has run on
  the new bytes (CTO msg 4046). The first organic admitted request is the first exercise of that path. ABSENT, not exercised-against.
- **Widenings (CTO half condition 9):** on irpt-performance-adapter, `svc-commentary` on retention reserve, `svc-irpt-packager` reading
  ANALYSIS_COMMENTARY and `analysis-request-read` for svc-custody-statement are each APPLIED, UNEXERCISED. Stated in full in a note
  appended to the closed completion record @12ac2a4241, because the record's own L6 close line is cut at 154 characters. Condition 8's
  reach read: 0 reaching sites on the adapter (`checks/r118/REACH_READ_IB416_BUILT_ZIPS_20261011.txt`; CTO half A4).

## Rows for the compile

- **D2-S68** (`~IB2`, BLOCKING): IB118-1-AC1 could not pass after a correct apply, because the apply rewrites `artifact_sha256`. An issuer
  check defect; TO-IB-pr-420 AMENDMENT 1 @8d0d9976ed; resolved by D2-S69.
- **D2-S64 / D2-S65** and **D2-W278-S2 / D2-S66**: as the round 117 packet; both resolved @1a4d947901.
- Pattern for the round-N analysis: two issuer check defects in one day (D2-S64, D2-S68), each found by the applier at grading time
  after a correct act. One is a re-point that did not re-point its check; the other a check that compared an output of the act.

## Carried, not closed by this round

- **irpt-status** (IB-pr-416's third function): `2.0.0_SA_COO~Y2` applies it under IRPT_ANLREQ release 1 revision 6, pin 5c35a6f9f9.
  CTO half condition 5 (both arms of `analysis-request-read` as svc-custody-statement) is exercised in its after-reads, or recorded
  APPLIED, UNEXERCISED.
- **IB-pr-413** (round 114) L4 and **IB-pr-404** (round 105) L6: both read the Monday 2026-10-12 14:15Z 49F fire. SECCLASS e56
  acceptance 1 closes on that read; this seat sends it to dell1 through `0.0.0_AB_MSTR~DELL2`.
- Row **D2-S60** (the three-function split) closes when irpt-status lands.

**Push state:** LOCAL on box/dell2 (MSTR box-sync pushes); re-measured in the send.
