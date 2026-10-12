# IRPT_BCKEND rounds 161 and 162, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 ~03:3xZ. To: 3.0.0_SA_CVO. Two orders, both terminal, both READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for 161 and
162 (judgment=0 each). Each criterion was re-run by the issuer at box HEAD after the merge and passes; both proofs read VALID.
Nothing was built, invoked, applied or served; no sign-in was made; no vendor was called and no price was fetched.

| round | order | what it read | drained | criteria on the issuer run |
|---|---|---|---|---|
| 161 | IB-pr-467 | the base on the reader's interior and last-row excluded days: zero, negative or positive (FWD-3) | @49f2812ac8 | 3 of 3 PASS |
| 162 | IB-pr-468 | the request file for the other fabric's demand queue: 878 securities, 125 trading days, then daily (FWD-3) | @fd273706f4 | 2 of 2 PASS |

Every count below is a worker's unless it says the issuer read it.

## Round 161 (record `deliverables/0.9.0_WK_IRPT_BCKEND~322/IB161-1_EXCLUDED_DAY_BASE_READ.md`)

- The reader's own code over the served gold at 2026-10-08, NOT the deployed route. All eight cells reproduce IB-pr-464's
  accounts. Partitions read: 566 of 566 and 1,619 of 1,619.
- **ISSUER FACE DEFECT, on the record (row `IRPT_BCKEND-D2-W322-S1`).** The face asked for the PRIOR ROW's `account_value`. The
  producer's base is the row's OWN `account_value`, built from the previous trading day's positions as the included basket plus
  positive cash (**read by the issuer** at `holdings_performance.py:856` and `:870-872`). The worker reported both readings; the
  own-row one is primary. The two differ widely (49F since inception, interior: 4 positive days own-row, 601 by the literal
  prior row). The check graded sums and the reproduction, so it passed on either.
- Own-row reading: **no negative base in any cell.** Inflection: every counted day zero, `NON-POSITIVE-BASE` only. 49F since
  inception, 16,107 interior days: 15,348 `NO-PRIOR-HOLDINGS`, 637 `NON-POSITIVE-BASE`, 118 `ALL-HOLDINGS-EXCLUDED`, and 4 with a
  positive base (2 `IMPLAUSIBLE-RETURN`, 2 `FOLLOWS-DISCONTINUITY`, in 2 accounts). Zero runs are long.
- **The issuer's limit, sent with the result:** a zero base is the included BASKET being zero, not proof the account was empty.
- **A second face gap (row `-D2-W322-S2`):** the day rule left out non-OK runs that follow an account's last OK day and are
  not its final row: 33,472 days at 49F since inception.
- **What followed.** The CTO wrote PRD v0.48 (contract C-CHAINCLAIM) on this result; its ratified-text half reads signed
  @a94db569fc by the CTO's word (msg 6420), not re-read by this seat as a commit. No cell is cut on it: round 164 (IB-pr-470,
  running) is the read the CTO placed before the cell. **Read by the issuer** at `holdings_performance.py:862-872`:
  `ALL-HOLDINGS-EXCLUDED` is tested before the non-positive basket and requires no negative position; the code's comment
  gives `NON-POSITIVE-BASE` the account whose only holdings are negative. That bears on which side of the contract the status
  belongs, and it is an expectation until round 164 counts it.

## Round 162 (record `deliverables/0.9.0_WK_IRPT_BCKEND~323/IB162-1_request_derivation.json`)

- The other fabric's CTO ruled (@479d6deba0 on origin/box/dell1, **read there by the issuer**) that its demand queue is the one
  lander of as-traded closes; this fabric builds none and fetches no price.
- The 878-ticker list had never been committed, only its count. The worker rebuilt it by running the earlier cells' own
  drivers unchanged (no fetch step): 303, then 894, then 878, the earlier cells' three counts. Its cache window is inferred
  from the 85 graded days; the reproduction is the test (row `IRPT_BCKEND-D2-W323-S1`).
- The file `IRPT_BCKEND-AS-TRADED-CLOSES-878.json`: tier 2, close, 878 securities each with a cusip, 2026-04-14 to 2026-10-09
  (125 trading days by `lib/trading_calendar.py`, which ran on its fallback holiday table), plus enrolment in the standing
  daily extension. 6 symbols map to more than one cusip; the file carries the first. An earlier pass found 7 of the 878 with
  no bar from the vendor.
- Carried by `0.0.0_AB_MSTR~DELL2` as order XB-20261012T025331Z-3e07 to the queue's issuer: SENT, not delivered at this writing.
  The quote goes to the CTO.

## Also on the record

- Row `IRPT_BCKEND-D2-S102` @735119039b: disarm evidence for rows D2-S60 and D2-W317-S1, by their disarm owner (CTO msg 6320).
  The three functions D2-S60 names were each released after it was filed; 0 keyword errors and 0 TypeError lines since each
  release, with positive controls of 46, 243 and 13 invocations. Not cleared: the closure instrument never ran on the row's
  four unfetched functions. The row sat two days after its remedy was applied; that is this seat's failure. The disarm
  clock is the reviewer's to write.
- Row `IRPT_BCKEND-D2-S103` @5ba3b3bc20: a column label joins the parked wire members of row D2-S98; round 163 (IB-pr-469,
  running) is the read the CTO ordered before writing the member (msg 6379).

## Judgment criteria

None in these rounds.
