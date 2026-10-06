# DSGN_AMGTV1 -- ROUND 44 CLOSE (2.0.0_SA_COO~D, 2026-10-06 ~06:4xZ; issued by hand, no loop)

**Rectangle:** AMGT_RESAPP `ledger/ROUND_ANALYSIS.round73.md` @cf0d03deb2 item 1 (msg 29921):
- (a) FWD-18: a driver-chart click opens the served `passage_text` with its cite;
- (b) FWD-1: the served `segment_breakdown` is drawn with its cites, or with its reason.

| step | evidence |
|---|---|
| issue | @3d87120c03 (decomposition v44; `round44/checks/r44/r44.cjs` 1 of 5 at base DEV b0051830 on deployed-satkY3HX fixtures, 5 of 5 on scratch reference edits) |
| worker ~105 | portal c6a3f8d2: ThesisDriverChart served passage + "From the filing: <location>"; NEW SegmentBreakdown.tsx; ThesisTab mount; types |
| AMENDMENT 1 | @342094450e: drafting.harness.cjs stubs the new ThesisTab import (row Z-W105-S1, resolved). Portal 8544e133 |
| issuer walk 1 | candidate fdf63a4b: BA passage + BA segments PASS; **MSFT FAIL, no card**. The mount sat under ThesisTab's `served` (drafted-thesis) branch, which was the issuer's spec gap |
| AMENDMENT 2 | @a4f6202597: the mount moved outside the `served` branch; r44 arm 4 tightened (4 of 5 on fdf63a4b, 5 of 5 moved). Portal 66204076 |
| drains | @91552921bb, @f5ba7b927b |
| candidate | portal **1d6d2573** = DEV 75ff922c + rounds 43 and 44 (5 commits re-applied; a fast-forward of DEV). r43 5/5, r44 5/5, battery29 ALL PASS (14 of 14 harnesses, tsc 0, eslint 0), run in worktree 105 with the current outer |

## The one real run (localhost:5174 = 1d6d2573 on the live API; walker 06:39-06:43:04Z, DISARMED)

`round44/walk/reads44.mjs` -> `round44/walk/read-20261006T063906Z/` (3 of 3 PASS). The 06:34Z attempt hit a port 5174 held by another
process, so the server never started. It is recorded in read-20261006T063453Z (3 ERROR, not reached) and re-run here.

- **FWD-18:** BA's first driver point opens its SERVED passage (`data-driver-chart-passage-source="served"`) with the cite line "From the
  filing: ITEM 7. MANAGEMENT'S DISCUSSION AND ANALYSIS / TABLE 2023". No "not shown on this page".
- **FWD-1, SERVED:** BA's Thesis tab shows "Business segments -- from the filing" with 11 rows, each cite folded (11 closed
  `details`).
- **FWD-1, REASON:** MSFT (drafting ABSENT) shows the card with the served reason ("No filing analysis is stored for this name yet, ...")
  and 0 rows.
- **Census at the cut:** all 12 names serving segment rows also have a drafted thesis, so no segment table was hidden before
  AMENDMENT 2. The amendment makes the reason visible on the other names.

## Grades this round moves (for RESAPP's walk and the countersign)

FWD-18 (DSGN) and RESAPP FWD-18 / FWD-1 (the page halves) are read on the page. RESAPP's walk grades its own FWD-18 and FWD-1 once this
is on DEV. **Round 44: 1 of 1 orders terminal.** Rounds 43 and 44 go to Andrew as ONE DEV push (candidate 1d6d2573); PROD is his
separate word.
