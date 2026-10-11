# IRPT_BCKEND rounds 133 and 134, workstream ~P -- drain-end packet (L8 input)

Issuer and drainer: 2.0.0_SA_COO~P2 on dell2, 2026-10-11 ~15:3xZ. To: 3.0.0_SA_CVO. Two orders, both terminal, both READ ONLY.
`python .tools/round-close-check.py --project IRPT_BCKEND --round <n> --workstream "~P"` reads `verdict=MAY-CLOSE` for 133 and 134
(orders=1, judgment=0 each). No judgment criterion. Each criterion was re-run by the issuer at box HEAD after the merge; both
proofs read VALID. Nothing is built, re-graded or served by either.

| round | order | what it read | drained | criteria on the issuer run |
|---|---|---|---|---|
| 133 | IB-pr-435 | the securities behind OUTSIDE_ANCHOR ranked; the cash rule counted; which held price store carries their closes | @0f10c53a87 | 3 of 3 PASS |
| 134 | IB-pr-436 | nine mutual funds by 85 days: an independent daily NAV against the custodian's mark | @2df691f227 | 3 of 3 PASS |

## What they found (FWD-3, Cottonwood)

- **133.** 734 securities sit behind OUTSIDE_ANCHOR on 34,437 account-days; 9 cover half of the carried security-account-days and
  236 cover ninety percent; the top ten are mutual funds. Cash rule as the CTO ruled it: of 19,809 cash-flagged account-days,
  19,466 stay cash, 0 have a differing price, 343 cannot be compared and are treated OUTSIDE_ANCHOR; blank share 58.2 percent of
  75,796 eligible; 382 of 999 accounts never served. Held prices, of 45,216 needed security-days: the four market-close stores
  find 144; Cottonwood's own holdings store finds 44,837, and that is the custodian's mark on the same holding. The CTO ruled the
  custodian's mark is not the anchor (msg 5157).
- **134.** For the eight funds the reader answered (680 fund-days): the majority mark equals the day's NAV on 642, both (NAV
  unchanged) on 38, the prior day's only on 0, neither on 0. FPNIX returned no data: 85 fund-days with no NAV, not retried; it
  stays OUTSIDE_ANCHOR and is named (CTO msg 5211). Row level: 497 of 124,645 rows equal only the prior day's NAV, on 33 of 85
  days; 42 equal neither, on three dates. Control: VTI equals the anchor on 85 of 85 days. The claim that the reader's Close is
  that day's NAV is `inferred`: no second public source was allowed. The account-day effect: 583 account-days hold only these
  nine outside the anchor; 563 would be freed. The CTO ruled the unit is the account-day and ordered the same read over all 734
  (IB-pr-438, round 136, running). Whether an unofficial reader may be a production anchor is a PRD question the CTO rules on
  that table; nothing is built before it.

## Sources asked

- Yahoo Finance through ADVI_COTBKF's existing reader (`fetch_yahoo`, `read_yahoo_close`): ONE call, ten tickers.
- The gateway's YCharts tools, by this seat, three calls in all on the CTO's word: `ycharts_time_series` answered 403 twice,
  `ycharts_fund_series` answered 400 once. Source one is closed for funds. The CTO measured the gateway's session live the same
  hour (`ycharts_freshness` HTTP 200), so the refusals are about the request, not the session.
- No Bloomberg call.

## Rows filed by these rounds

- IRPT_BCKEND-D2-W293-S1 (the holdings store reads to 2026-10-09, not 10-06), -S2 (the silver store's source column mixes market
  and derived sources), -S3 (the copied script's measure mode reads a file that is not in the tree).
- IRPT_BCKEND-D2-W294-S1 (the reader has no bars for FPNIX), -S2 (the worker reads yfinance 1.7.0; the issuer's read on the same
  box says 1.2.0; unresolved, no effect on the result), -S3 (the majority-mark rule hides the 497 prior-day rows; the worker
  added row-level counts the order did not ask for).

## Issuer notes

- IB-pr-435's face told the worker to use the bare row-id form; the row gate refuses that form from a worker, and the worker used
  the worker form. The face was wrong; later faces name the worker form.
- IB-pr-436's ranking by security was the wrong unit for the question (the CTO's own word, msg 5211); round 136 counts account-days.
