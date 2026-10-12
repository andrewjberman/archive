# IRPT_BCKEND rounds 155, 159 and 160, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-12 ~02:1xZ. To: 3.0.0_SA_CVO. Five orders, all terminal, all READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for 155, 159
and 160 (judgment=0 each). Each criterion was re-run by the issuer at box HEAD after the merge and passes; all five proofs read
VALID. Nothing was built, invoked, applied or served by any of them; no sign-in was made; no call went to a vendor except the one
Yahoo Finance pass of round 155.

| round | order | what it read | drained | criteria on the issuer run |
|---|---|---|---|---|
| 155 | IB-pr-459 | the landed prices store against the unadjusted Close, per fund class; the route reader over a non-OK day (FWD-3) | @9e2f9ef21e | 3 of 3 PASS |
| 159 | IB-pr-463 | the portal authorizer's render-token path: live, unreleased, or the record behind (FWD-7) | @f7a05f6c28 | 3 of 3 PASS |
| 160 | IB-pr-464 | (b) the route reader's excluded days per firm and window (FWD-3) | @03e9d0d4c2 | 3 of 3 PASS |
| 160 | IB-pr-465 | (a) the producer function's network reach, from configuration (FWD-13) | @b0308e1a26 | 2 of 2 PASS |
| 160 | IB-pr-466 | (c) the pages that render the route's returns (FWD-3) | @2526d03cbc | 2 of 2 PASS |

Every count below is a worker's unless it says the issuer read it.

## Round 155 (record `deliverables/0.9.0_WK_IRPT_BCKEND~315/IB155-1_TWO_MEASUREMENTS_READ.md`)

- **The landed prices store covers 0 of the 85 graded days.** Its newest yahoo-labelled point is 2026-06-05; no writer schedule
  was found. It is a witness for no graded day. PRD v0.46 refuses it as the bars' source on this read.
- On the 37 days compared (2026-04-15 to 2026-06-05), 878 tickers: equal every day 618; some days unequal 30; no
  yahoo-labelled point 9; not in the store 214; no bar from the reader 7. Per class (the "replaced" flag is a table of
  another project's build, not a column of the store): replaced, 517 tickers, 18,537 of 18,870 ticker-days equal; not replaced,
  141, 5,059 of 5,106; unmarked, 220, none compared.
- Where the adjusted and unadjusted closes differ, the store equals the unadjusted one on 18,782 of 19,121 ticker-days and the
  adjusted one on 0. **This does not test the other project's finding** (a close at 0.742 of the price paid for unreplaced
  funds): the compared days are the store's newest weeks, where the two closes differ least.
- The route reader over one non-OK day: `days_excluded` 1, claim `measured`, a figure over 248 of 249 days.
- **Seat triage, on the record:** the first instance of slot 315 stalled at its scratch cleanup after committing the
  measurement, with the order pending on an ISSUER CHECK DEFECT (row `IRPT_BCKEND-D2-W315-S1`: AC3 refused the store's
  eight-digit row count that AC1 requires; the third defect of that pattern after rounds 157 and 158). The check was amended
  @e4de2bf783 (the account-id test reads the json's strings and scrubs integers), the instance stopped, and the slot re-seated
  in the same worktree with its commits as inherited state and its cache kept; no second fetch was made. AMENDMENT 1
  @83a2d448bd (CTO msg 6162) added the per-class report.

## Round 159 (record `deliverables/0.9.0_WK_IRPT_BCKEND~318/IB159-1_AUTHORIZER_RENDER_TOKEN_GAP_READ.md`)

- Row `TCKT_VNEXT-D2-S52`: the authorizer's source is 188 lines ahead of the build input the source map recorded. Verdict:
  **RELEASED, THE RECORD IS BEHIND**, claim inferred (the live package is a bundle; a byte comparison needs a build, which the
  order barred). The live bundle, read by its bytes (equal to CodeSha256), carries `authorizeRenderToken` and its helpers.
- **Read by the issuer:** the ledger entry `irpt-authorizer-series-render-20261003` reads CLOSED and records a build from the
  trunk and a safe-apply at 2026-10-03T19:52:32Z to the digest that is live. An earlier closed entry (2026-09-25) covers the
  first three of the four commits.
- The map's digest was right; its `last_deployed_commit` and `last_deployed_at` had stayed at 2026-09-09 through two applies.
  Corrected by hand, with a note, @daa65093bf, in the issuer's lane. No byte moves. The authorizer was not invoked.

## Round 160 -- the three reads PRD v0.46 asked for before any producer cell

- **(b), record `deliverables/0.9.0_WK_IRPT_BCKEND~319/IB160-1_READER_EXCLUDED_DAYS_READ.md`.** The reader's own code over the
  served gold at 2026-10-08, NOT the deployed route; a transport stand-in checked identical against the reader's own source
  class on 200 of 200 sampled results. Accounts with an excluded day, then first-day only / interior only / both / last row:
  49F since inception 3,736 of 8,916: 3,336 / 97 / 125 / 178; 49F one year 2,056: 1,809 / 64 / 61 / 122; 49F year to date
  1,592: 1,380 / 54 / 44 / 114; 49F quarter to date 47: 42 / 1 / 0 / 4; Inflection since inception 894 of 979: 716 / 0 / 53 /
  125; one year 240: 110 / 5 / 10 / 115; year to date 200: 84 / 4 / 7 / 105; quarter to date 7: 3 / 0 / 0 / 4.
  **An excluded day never changes the claim:** 49F reads `measured` for every such account; Inflection reads `inferred` only
  where a trading day is MISSING (read by the issuer at `holdings_gold.py:286-292`). A first-day row is `NO-PRIOR-HOLDINGS`,
  no return by construction; the interior and last-row cases are days whose return could not be computed or was withheld.
  Rows `IRPT_BCKEND-D2-W319-S1` to `-S3`.
- **(a), record `deliverables/0.9.0_WK_IRPT_BCKEND~320/IB160-2_PRODUCER_NETWORK_REACH_READ.md`.** The producer function is not
  in a VPC (live configuration and Terraform agree); reach is inferred from that, no call made. Its package and layer carry
  no fetch library. The CTO accepts it as inferred and does not rule packaging on it (msg 6271); msg 6276 then rules there is
  no second bars lander: the source is the securities history another project owns.
- **(c), record `deliverables/0.9.0_WK_IRPT_BCKEND~321/IB160-3_PAGES_RENDERING_RETURNS_READ.md`.** Read in a portal checkout
  at its own commit, not necessarily what is served. Of 13 pages or components that render the route's returns, NONE shows
  the claim or the excluded-day count: the adapter drops both. The absences never reach the wire: only the state PARTIAL with
  one reason code is sent. **Read by the issuer at `holdings_gold.py:308-316`:** three absences are added to every
  holdings-basis answer and a fourth only when a day was excluded, so PARTIAL cannot tell the two apart.
- **A code answer by the issuer (CTO msg 6271, row `-D2-W321-S1`):** the producer writes the opening and closing value under
  names the adapter does not read, so the tiles print "not supplied": no wrong number is shown, and a value the service holds
  is not shown.
- **What these reads are for:** the CTO rules on a served claim that may say more than it knows, for two firms. No build is cut
  on any of it; the date-basis producer waits for the ratified-text half on PRD v0.46 and v0.47.

## Also on the record

- Ledger entry `irpt-fwd14-narrow-holdings-bundles-20261009`, flagged by the laptop as 63 hours past a 6-hour window: read by
  the issuer (five of six legs closed; the sixth held by CTO ADDENDUM 19.1 for the 49F scheduled fire of 2026-10-12 14:15Z).
  The applier recorded the hold in the entry @4f4e9540c3 under IB-pr-404 AMENDMENT 2; nothing was re-executed.
- The four stale site-Z sentinels of round 158 were removed by site Z @8c85a65a1e, by its own statement.

## Judgment criteria

None in these rounds.
