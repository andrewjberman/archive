# IRPT_BCKEND rounds 150 and 151, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~21:5xZ. To: 3.0.0_SA_CVO. Two BUILD orders, both terminal. Nothing is
released, served or deployed by either. `python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"`
reads `verdict=MAY-CLOSE` for 150 and 151 (judgment=0 each). Each criterion was re-run by the issuer at box HEAD after the merge
and passes; both proofs read VALID; `.tools/commit-gate.sh` is clean on every new or changed `.py`.

| round | order | what it built | risk | drained | criteria on the issuer run |
|---|---|---|---|---|---|
| 150 | IB-pr-454 | the date-basis grading instrument's product form, its tests, one read-only run (FWD-13) | LOCAL | @ddf890e1f6 | 3 of 3 PASS |
| 151 | IB-pr-455 | the submission admits `commentary_requested`; acceptance carries it when sent (FWD-4) | WORLD by the L6 floor; nothing released | @0322231fc8 | 3 of 3 PASS |

Every count below is a worker's; the issuer re-ran the checks, not the measurements.

## Round 150 (files `data/assets/scripts/gold/irpt_reporting/date_basis_grading.py` and its test; record `deliverables/0.9.0_WK_IRPT_BCKEND~310/IB150-1_PRODUCT_FORM_RUN_READ.md`)

- A pure module, 336 lines, 54 tests; it imports the guard (`second_witness_guard.py`) and the trading calendar; no file under
  `data/`, `infra/` or `lib/` other than its own test names it (the check reads that).
- **The seam:** with the repeated-share rule switched off, the module over the same 85 graded days reads IB-pr-452's nine-pair
  sizing member for member (blank 33,291 of 75,796; never served 247; freed 12,482).
- **Reproducibility:** the issuer's two planted series, asked in a long and a short run ending on the same day, read the same
  grade; the module's own test asserts the same across one and three windows.
- **The three returns** (the worker proposes; the CTO wrote PRD v0.44 from them: 40 trading days, floor 20):
  1. Window 40 trading days ending at the graded day; fewer than 20 compared days, no grade. Candidates 10, 20, 40, 60, 85 take
     30, 22, 14, 14, 14 securities.
  2. Securities by share of repeated days, in tenths (300 outside the first witness): 248, 26, 14, 3, 2, 2, 2, 1, 2, 0.
  3. Cost: the seven of IB-pr-452 not graded on any day, 33 account-days and 1 account; at window 40 the rule takes 14 (those
     seven and CCEYF, EIBIX, EROK, FCSTX, HONA, SUN, VMLUX, each on part of the run), 287 account-days and 2 accounts; blank
     43.9865 percent, never served 249.
- **To read against the ratified text:** a fixed window is not v0.43's whole-run reading; it takes seven securities more, on
  part of the run, with nothing measured against their moved bars. Rows `IRPT_BCKEND-D2-W310-S1` (the PRD's sentence counts
  repeated days differently from the earlier script; the product follows the sentence), `-S2` (a row at neither close is named
  `NEITHER_CLOSE`, the PRD's word, where the script kept `OUTSIDE_ANCHOR`; counts unchanged), `-S3` (7 of 878 tickers returned
  no bar, three of them dotted share-class tickers).
- **A decision of the issuer's, as in round 146:** the module is wired to nothing. The producer's design is the next cell and is
  a READ; it is not cut until v0.44's ratified-text half is signed. The sign-off tool prints SIGNED for v0.44 @84fec7b9b4 while
  no sign-off commit for v0.44 is in the PRD folder's history (read by the issuer at 21:5xZ); the issuer waits for the file.

## Round 151 (files `ycharts/generate/submission.py`, `ycharts/generate/acceptance.py`, `docs/contracts/investor-reporting/v1/AnalysisSubmissionRequest.schema.json`, a new test and its records file)

- On IRPT_YCDGEN PRD v0.13 (signed @6f8aeb03b7), service first. The submission's closed set admits `commentary_requested` only
  as a real boolean; eight other types are refused with one new code, `COMMENTARY_REQUESTED`; an unknown member is still
  refused; acceptance copies the member into the accepted record only when it was sent; the public contract declares an
  optional boolean in a still-closed object.
- **The control passes before and after:** a submission without the member validates to itself, and the existing acceptance,
  submission and worker-gate tests pass unchanged (19 passed, 20 skipped). The folder's offline suite ends rc 0 at HEAD.
- **A fact for the release pair:** a replay of the same request id with a different `commentary_requested` is REFUSED
  (`CHANGED_INPUTS_SAME_REQUEST_ID`), because `browser_sha256` is the digest of the validated submission.
- The worktree's base was checked to contain the worker half it depends on (@dddafd6832), the rule taken from row
  `IRPT_BCKEND-D2-S99`.
- **Not released.** IB-pr-456 (round 152, issued @1b3f3287e3, amended @e7bb7e923a) is the release read and is running: every
  function packaging the changed members by subtraction over the source map, minimal candidate builds beside live, riders, every
  reader of the accepted record re-counted at base, the replay, and (CTO msg 5904) a proposed after-read with no vendor call
  for `irpt-ycharts-generate` with what stays unexercised. No apply order is cut and none follows without a signed pair.

## Judgment criteria

None in these rounds.
