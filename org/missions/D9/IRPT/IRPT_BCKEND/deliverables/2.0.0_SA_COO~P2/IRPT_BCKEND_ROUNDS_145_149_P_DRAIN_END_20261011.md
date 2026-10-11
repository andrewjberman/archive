# IRPT_BCKEND rounds 145 to 149, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~20:5xZ. To: 3.0.0_SA_CVO. Five orders, all terminal: four complete, one
superseded and not executed. `python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads
`verdict=MAY-CLOSE` for 145, 146, 147, 148 and 149 (judgment=0 each). Each criterion of the four complete orders was re-run by
the issuer at box HEAD after the merge and passes; the four proofs read VALID. Nothing is served or re-graded by any of them; no
request was made to the vendor; no AWS write was made.

| round | order | what it did | drained | criteria on the issuer run |
|---|---|---|---|---|
| 145 | IB-pr-449 | READ: the first moved bar after a repeated run, the six's moved days, v0.41's count (FWD-13) | @eb0c2d4890 | 3 of 3 PASS |
| 146 | IB-pr-450 | BUILD, nothing served: the second witness's guard as one pure function, 21 tests (FWD-13) | @e447cb6a4d | 3 of 3 PASS |
| 147 | IB-pr-451 | owner read of a served vendor report, key names only | SUPERSEDED @9053ea7b45, 0 calls | not graded |
| 148 | IB-pr-452 | READ: nine pairs sized under both guard sentences, the five, the repeat count (FWD-13) | @6a7b589f9e | 3 of 3 PASS |
| 149 | IB-pr-453 | READ, code only: which member says commentary was asked; the accepted record's readers (FWD-4) | @f1744dd205 | 3 of 3 PASS |

Every count below is a worker's; the issuer re-ran the checks, not the measurements.

## Round 145 (record `deliverables/0.9.0_WK_IRPT_BCKEND~306/IB145-1_FIRST_MOVED_BAR_READ.md`)

- First moved day after a repeated run, beside the anchor. Institutional class, 181 runs: equals the anchor that day 121; the
  prior day 0; neither 0; no anchor that day 54; no moved day in the window 6. RIC/BDC Not Available, 368 runs: 295; 0; 0; 72; 1.
  So 416 of 416 comparable are right and 126 could not be compared.
- The six institutional securities: every priced held row on a moved day equals the bar that day (181 of 181). This sets the
  custodian's mark beside the reader's own bar; the reviewer's note on v0.42 says what that does and does not show.
- v0.41's sentence un-grades 6 of 64,536 security-days, none in the two pairs.
- **Issuer defect, recorded by the worker (row `IRPT_BCKEND-D2-W306-S1`):** the face said the six are outside the first witness;
  JSOSX is carried by the anchor on 75 of 87 days.
- AMENDMENT 1 @1286cbf961 added v0.41's count mid-run and was handed to the running worker by continuing it; GATE (viii) graded
  the modified order.

## Round 146 (files `data/assets/scripts/gold/irpt_reporting/second_witness_guard.py` and its test)

- `second_witness_grades(bars, t)`: true only with a bar on t, a bar on the calendar's prior trading day, and the two differing
  by more than relative 1e-4. The issuer's ten cases pass, the v0.41 gap case among them. No file under `data/` or `infra/`
  imports it.
- **A decision of the issuer's, told to the CTO:** the grading instrument was not product code (0 hits for the claim and witness
  names over `data/`, `lib/`, `infra/`); the guard therefore landed as a function wired to nothing.

## Round 147 -- withdrawn

- The applier 0.7.0_AE_CloudOps~IB2 was refused at the service password read by an explicit deny on the dell2 agent user (rows
  `IRPT_BCKEND-D2-S96`, `-S97`). 0 calls were made. Nothing was worked around and no grant was sought.
- 2.0.0_SA_COO~G2 (msg 5765): every earlier run of that read was one served-read window under its own signed pair.
- CTO msg 5770: dropped as a standalone read; no window is opened and no identity is moved; the confirmation rides the laptop
  walk that proves DSGN_IRPTV1 cell IV-e-115.
- **Issuer defect, row `-S97`:** the check could not pass a refusal made before any HTTP although the face said all three
  outcomes pass. Not amended, because the order ended.

## Round 148 (record `deliverables/0.9.0_WK_IRPT_BCKEND~308/IB148-1_NINE_PAIR_SIZING_READ.md`)

- Over 76,796 account-days. Nine pairs under both guard sentences: blank 43.9218 percent, never served 247, freed 12,482. With
  ADLYX, BISOX, EIBLX, GPPIX and OLCYX not graded: 43.9232 percent, 248, 12,472; a cost of 10 account-days and 1 account.
- 7 of 300 securities outside the first witness with bars repeat on more than half their days: those five, JSOSX and SGOV.
- The second guard sentence costs 0 in this sizing (row `IRPT_BCKEND-D2-W308-S1`).
- The worker's first run did not reproduce IB-pr-445 (a skipped step); the second did, member for member.
- What followed: PRD v0.43 (the repeated-share rule), signed. IB-pr-454 (round 150: the instrument's product form with a fixed
  trailing window, nothing served) is issued @f6c8f80c7a and running; it is not in this packet.

## Round 149 (record `deliverables/0.9.0_WK_IRPT_BCKEND~309/IB149-1_COMMENTARY_ASKED_MEMBER_READ.md`)

- A submission does not say commentary was asked for (a closed set). The ticket does: `answers.add_commentary`, which no IRPT
  code reads. Acceptance holds no ticket body and could not read the fact without a ticket read. The accepted record has seven
  members and is declared by no file; 50 readers were counted, and every production reader ignores an unknown top-level member.
- **Issuer defect, row `IRPT_BCKEND-D2-S99` @1ff761ad22:** the issuer relayed the worker's row `-W309-S1` ("the worker signals
  on every READY job") to the CTO as a finding. It is a vintage artifact: the worktree base 0bdd920114 does not contain
  2.0.0_SA_COO~G2's ticket gate merged at 8d6fef62e8 (merge-base read by the issuer after the CTO named the cause). The read's
  other results are at the same vintage and were not re-read at HEAD by the issuer; the reader census is re-counted at the base
  of any cell cut against it.

## Also on the record, outside any order

- Row `IRPT_BCKEND-D2-S95`: the intake poller's rollback version id and the condition of its future release (CTO msg 5666).
- Row `IRPT_BCKEND-D2-S98`: a wire title and a field name on a vendor section, parked for the producer's next release.
- `infra/aws/lambda/ci/lambda-source-map.json` @0c4d9d3092: the `irpt-ycharts-generate` deploy fields corrected to the live
  deploy by 2.0.0_SA_COO~G2's patch, landed by this seat (its lane) after reading the live digest and date. No byte moves.

## Judgment criteria

None in these rounds.
