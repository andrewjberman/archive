# DSGN_AMGTV1 -- ROUND 39 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-05 ~14:5xZ) -- THE CTO'S THREE-ITEM LIST

**Input:** decomposition v39 and the issuance @22ef916e2c; the CTO's list @222ecd916c (msg 29564): (1) the CardFooter unknown-source
fallback; (2) row S3, the end line with no invented clock, touching the fewest shared files; (3) reads37's What-changed selector.

## 1. THE CELL -- `AV-zq-1`, one order, item 1 first

| item | change | worker | portal | proof (issuer re-run where noted) | outer drain |
|---|---|---|---|---|---|
| 1 | `CardFooter.tsx:95` returns `UNNAMED_SOURCE_WORDS` (1 line) | ~101 | 72c60f2b | repairs38 6/6 (AMENDMENT 2, unknown-source arm); battery29 ALL PASS | 90bbb5e8f1 |
| 2 (AMENDMENT 1 @7377677834) | `PageEnd.tsx` optional `asOfText` (default unchanged); `SecurityAnalysis.tsx` passes the served day via longDate/longStamp | ~101 | 066fb196 | repairs38 6/6 (AMENDMENT 3: arm 3 renders the REAL PageEnd); battery29 ALL PASS 14/14 | f37ce06676 |
| 3 | reads37's What-changed scope selector follows `section[data-what-changed-failed]` | issuer | -- | node --check; committed @7377677834 | -- |

The item-2 design touches ONE shared file (PageEnd.tsx, one optional prop). Without the prop the old formatting runs, so every other page
prints what it printed before; repairs38 arm 3 asserts the Market end line unchanged.

## 2. WHAT LANDED ALREADY -- item 1 with rounds 37 and 38

Push candidate 481b3bcc (= DEV cab2b039 + r37 + r38 + item 1). The issuer's run read repairs38 6/6, repairs37 5/5 and battery ALL PASS.
CTO CONFIRMED it (msg 29590). MSTR~Z pushed portal DEV cab2b039 -> 481b3bcc on Andrew's record 121b7b016e; CI 37321896188 success
(msg 29591; fetch read: DEV = 481b3bcc). PROD is untouched at c69b4747.

## 3. THE ITEM-2 CANDIDATE -- portal `71097b53` = DEV 481b3bcc + dsgn-r39-zq1 (2 files, +9/-3), LOCAL

- battery29 ALL PASS (0 skipped). Nine checks, rounds 34-38, at full marks; repairs38 arm 3: "End of Security Analysis. Data as of
  October 2nd, 2026." on MSFT/AMD, no clock; Market default unchanged.
- FWD-20 instrument (C:/tmp/r39-scratch-close): 4 of 4 arms. The built page's PNG (`candidate/thesis.png`, a fixture with no served
  page date) ends "End of Security Analysis." with no date and no clock. Every card ends in its served footer, for example
  "September 30th, 2026, 9:00a ET | Source: company filings and Form 10-K."
- **Not run:** a live walk of the dated end line. The walker is held by the laptop's Y-6 runs. The dated line is graded on the real
  PageEnd render over served MSFT/AMD fixtures (arm 3). A live read can follow in the next walker slot if the CTO wants one.

## 4. OPEN

- The CTO's review of 71097b53. It touches one shared file (PageEnd.tsx), so its DEV push needs Andrew's word.
- **Next list:** none named by this round.
