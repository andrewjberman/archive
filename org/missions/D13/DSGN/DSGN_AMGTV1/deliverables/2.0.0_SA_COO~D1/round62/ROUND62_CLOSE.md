# DSGN_AMGTV1 round 62 -- CLOSE (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~10:4xZ)

| item | value |
|---|---|
| list | `ledger/ROUND_ANALYSIS.round61.md` @3e33baad5b section 3, items 1-4: one batched repair cell (decomposition v62) |
| issuance | @c2b0e84932; fan-out 1 of 1; the order is LF only (ruling R2) and stayed LF through the flip |
| order | `TO-AV-zzn-1` -> ~134 (worker-light), drained @0fb5305656 (`git show --stat HEAD`: the proof instance and the order, 2 of 2 paths); instance VALID |
| checks | r62 6/6 (re-run by the issuer on the worker's tree and on both candidates); battery29 ALL PASS on both candidates |
| DEV | candidate `ce3b0cc4` = origin DEV `9b06f6ed` + 1 (`cand/dsgn-amgtv1-r62-dev`) |
| PROD | candidate `2e41c008` = PROD `90db1e84` + the same commit (`cand/prod-dsgn-r62`); 0 files outside `src/pages/SecurityAnalysis/`; the SA tree equals the DEV candidate's |
| rows | none from the worker |
| round-close-check | `verdict=REFUSED` until the CVO grades `TO-AV-zzn-1` AC3 (L9) |

## The real run -- 10:35Z-10:38Z, `tmp/ui-walk/20261009T103538Z`

A signed-in `dev:live` build of `ce3b0cc4`. The News tab was opened through the scratch default-tab edit, then reverted (`git status`
reads clean). AMD, NVDA and ASML were walked: 56 screenshots, 0 guard aborts. The walker disarmed and its login is refused (401).

| item | what the screenshots show |
|---|---|
| `TO-AV-zzn-1` AC3, joined line | AMD (`004-AMD-overlay`): the price line runs unbroken from January to October over the article bars. The right axis reads "Closing price" (150-750), and the legend reads "Closing price, joined across days with no close". |
| `TO-AV-zzn-1` AC3, no-price name | NVDA US (`032-NVDA-overlay`), with no stored prices: no line is drawn, and one line under the chart reads "No price line: none of the 5 stored price history objects holds a series for NVDA US." This is the round-61 `TO-AV-zzm-2` carry (CVO, `ADJUDICATION_v34`), now seen on the page. |
| Z-W87-S1 | `types.ts` `CoverageItem.url: string \| null`; `HEADER_FEED_VISIBLE_COUNT` is gone; tsc rc=0. |
| Z-W97-S1, re-measured by source | Every bubble-label path in `ChatterBubbles.tsx` at `ce3b0cc4` floors at `MIN_FS = 11` (`outsideVariants`, the in-bubble loop `fs >= MIN_FS`, the last-resort grid), so the 8-10 px label clause is answered in the code. The radii clause is not re-measured: the ramp legend still draws `borderRadius: 2`. It is carried as a measured question for round 63. |

**The ASML read for round 63 did not happen.** The walker's search selected the key `ASML`, and `/thesis` and `/overlay` answered 404 for
it (7 API issues, all on that key). A `--probe-get` of `ASML_NA_Equity/thesis` answered 200 (1.1 MB, 401 without the page's headers), but
a probe keeps no 2xx body. The served `description_verdict_state` for ASML is still to be read; see `round63/PREP.md`.

## Seen on the walk, not of this round (for the round-62 analysis)

- NVDA's spine: the event-marker titles overlap one another, at late February to March and at late August (two titles drawn over
  each other, unreadable).
- NVDA's header tiles read "5.26T currency not stated" three times, in three tiles.
- Selecting "ASML" in the search lands on the key `ASML` (404) and not `ASML_NA_Equity`, so the page shows nothing for a covered name.
  This is a walker artifact or a page defect; to read in round 63.

## Carried

- **Round 63:** `round63/PREP.md` (the three AMGT_RESAPP R1 page items, CTO msg 2266), the ASML read, and the radii question.
- **FWD-1:** Andrew's own signed-in walk on PROD (open-calls 2caa).
