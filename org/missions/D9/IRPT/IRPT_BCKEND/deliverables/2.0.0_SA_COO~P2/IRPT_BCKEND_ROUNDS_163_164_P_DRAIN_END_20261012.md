# IRPT_BCKEND rounds 163 and 164, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 ~14:0xZ. To: 3.0.0_SA_CVO. Two orders, both terminal, both READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for 163 and
164 (judgment=0 each). Each criterion was re-run by the issuer in the worker's worktree before the merge and passes; both
proofs read VALID. Nothing was built, invoked, applied or served; no sign-in was made; no vendor was called.
Both slots died with the previous session (weekly-limit stall) before producing output and were respawned from the worker
face alone; the results below are the respawned workers'.

| round | order | what it read | drained | criteria on the issuer run |
|---|---|---|---|---|
| 163 | IB-pr-469 | what a column of a vendor report section is, per code; one stored report; every consumer of the id's shape (FWD-5) | @c1e0a25a9f | 3 of 3 PASS |
| 164 | IB-pr-470 | the closed status set with counts; NON-POSITIVE-BASE days by prior-day holdings; the assignment order; the accounts whose claim moves (FWD-3) | @0924979f0e | 3 of 3 PASS |

Every count below is a worker's unless it says the issuer read it. The issuer did not re-read the producer or extractor lines.

## Round 163 (record `deliverables/0.9.0_WK_IRPT_BCKEND~324/IB163-1_COLUMN_MEANING_READ.md`)

- Columns by section code: S01, S03, S18 are ENTITY (compared securities); S14, S15, S16 are PERIOD.
- Verdicts: S01, S03, S18 `HELD_ELSEWHERE_BY_THE_PRODUCER` (the producer holds the portfolio name and the chosen comparison
  names in request order; the extraction is never handed them). S14, S15, S16 `ON_THE_PAGE_NEVER_READ` (the census records the
  period headings; no source under `investor-reporting/` reads `axes`). S03 also has entity headings on the page that no code reads.
- Column order: NOT guaranteed to follow the request's security order; it follows the page only partly (same-line cells by x0;
  an unreadable cell shifts every later column one place left; a stacked value ranks top to bottom; the list stops at six).
- **Stored report: NOT read** (row `IRPT_BCKEND-D2-W324-S1`). The prefix listed (21 objects over 3 firm prefixes); the one get of
  the newest object returned `AccessDenied` on `kms:Decrypt` for the dell2 agent user. No other object, identity or path was
  tried. So the S18 count against the predicted 36 is NOT established. A decrypt grant is a cloud permission change: it goes to
  the CTO, not ruled here.
- Consumers: 24 cited over 712 files searched (33 with a hit); none parses the id. The portal checkout is an empty directory in
  the worktree, so 0 files there (the portal consumers are NOT censused).
- Row `-D2-W324-S2` (INFERRED): S15 and S16 both list "Standard Deviation" on census page 10 and the extractor stops at the
  first label hit, so one printed row may yield two section ids.

## Round 164 (record `deliverables/0.9.0_WK_IRPT_BCKEND~325/IB164-1_STATUS_SET_AND_BASE_READ.md`)

- The reader's own code over the served gold at 2026-10-08, NOT the deployed route. Partitions read: the 49F entry 566 of 567
  listed (2026-10-09 is excluded by the cap), orion 1,619 of 1,619. Interior reproduces IB-pr-467 in 8 of 8 cells.
- Status tokens in the producer: six (OK, NO-PRIOR-HOLDINGS, NON-POSITIVE-BASE, ALL-HOLDINGS-EXCLUDED, IMPLAUSIBLE-RETURN,
  FOLLOWS-DISCONTINUITY). No token outside the constants can be written; the column has three writers. No token in the gold
  is outside the code.
- Assignment order: NO-PRIOR-HOLDINGS, then ALL-HOLDINGS-EXCLUDED, then NON-POSITIVE-BASE. An account holding only excluded,
  non-negative positions CANNOT be stamped NON-POSITIVE-BASE (verdict NO; measured 0).
- NON-POSITIVE-BASE rows: the 49F entry 1,596; orion 575,039. **NON-POSITIVE-BASE days in an account that held a position the
  day before, all positions:** 49F SI 5 of 1,223 (interior 3 of 637), YTD 3, QTD 0, 1Y 3. **Orion: all of them** (SI 539,402 of
  539,402; interior 3,280 of 3,280), every one with zero cash and a position row: included rows all valued zero, or negative
  keys with no included row. The 49F days are almost all no-position cash debits (1,219 of 1,223 with non-zero cash).
  Row `-D2-W325-S1`: NON-POSITIVE-BASE is two populations, and the weak place in the contract is the whole of orion's.
- Claim-move counts (measured today / as the contract is written / if a NON-POSITIVE-BASE day with a prior position also
  moves): 49F SI 6,896 / 18 / 23; YTD 6,832 / 16 / 19; QTD 6,722 / 2 / 2; 1Y 6,840 / 17 / 20; orion SI 926 / 0 / 894; YTD 906 / 0 / 200;
  QTD 805 / 0 / 7; 1Y 916 / 0 / 240.
- Control held: a planted ALL-HOLDINGS-EXCLUDED day moves the counter; a planted NO-PRIOR-HOLDINGS day does not.
- **Not established:** why a NON-POSITIVE-BASE day arose or whether a return was left out (the gold carries counts and cash, not
  prices or flows); the deployed route's own answer; the contract's own definition of an excluded day; accounts the reader refuses
  appear in the class counts and in no claim-move count; the silver was not read.

## Judgment criteria

None in these rounds.
