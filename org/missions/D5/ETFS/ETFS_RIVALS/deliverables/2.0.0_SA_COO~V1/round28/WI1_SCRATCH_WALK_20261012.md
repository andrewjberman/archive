# RIV-wi-1 J1 -- the scratch-sink full run_dag walk (CVO ADDENDUM 12, row D1-C-S13)

Author 2.0.0_SA_COO~V1, 2026-10-12 14:1xZ-14:4xZ, dell1. Nothing here grades; the grade is the CVO's. Driver:
`round28/wi1_scratch_walk.py` (real `sweep.run_dag`, real `dramatic_move.run_for_day`, real Bright Data SERP search; stage runners
stubbed, markers in memory; sink = a LocalSink holding a READ-ONLY copy of the stored G4 closes and corporate actions for the 30
days to 2026-10-12: 11 `security_market` objects, 9 `corporate_actions` objects). **Nothing was written to S3**: the key
`.../corporate_actions/date=2026-10-12/` holds 0 objects and a HeadObject on the walk's object reads 404 (read 14:3xZ).

## Measured

| # | walk | what it ran | result |
|---|---|---|---|
| A | stored data as is | `run_dag` for 2026-10-12: stages ran in order build-peer-group-map, fetch-holdings, build-silver, build-canonical-shape, build-coverage, build-trade-schedule, publish-page; the lookup ran once, inside `run_one("publish-page")` | `dramatic_move: cap 8; candidates 0; searched 0; calls 0; written 0; failed 0; capped 0` (`run_dag` returned `dramatic_move: {status RAN, ...}`). Wiring and the 0-calls clause: PASS. The Bloomberg TKOMY row (split 15.0 ex 2026-10-07, claim MEASURED) explains the one move, so no name has an unexplained discontinuity |
| B | TKOMY's 10 stored action rows withheld FROM THE COPY (a CONSTRUCTED condition) | same walk, `--cap 3` | candidate 1: `TKOMY_US_Equity` 2026-10-07, close 50.50 -> 3.33; query `Tokio Marine Holdings Inc stock split October 2026`. Attempts: b1 FAILED (`SERP FAILED: VENDOR`, calls 1, failed 1, written 0, run continued); b2 FAILED the same way; **b3 written 1**: one INFERRED row, split 15.0 ex 2026-10-07, source web_search, `source_url` https://www.tokiomarinehd.com/en/ir/stock/return.html (the company's IR page) |
| C | rendered series (`price_series.load`, the function the chart reads, over the scratch sinks, window 2026-10-01..2026-10-12) | control b2 (no split on file) vs b3 (the walk's INFERRED row) | b2: points 49.59, 50.50, then None for 10-07..10-09, gap reason "the price moved more than threefold in one day and no corporate action". b3: 3.31, 3.37, 3.33, 3.35, 3.40 (continuous), `adjustment` split 15.0 ex 2026-10-07 claim INFERRED with the source_url. This is the series, NOT the published HTML page |
| D | Bright Data reliability on this account's zone `serp_opal` | 9 searches in all (4 inside walks, 5 direct) | 4 OK (9 records each), 5 FAILED: 4 `VENDOR` (HTTP 200, brd_status 502, `expect_element` "waiting for selector #main failed: timeout 30000ms exceeded"), 1 `TRANSPORT`. The same query failed once and succeeded once. The key read from Secrets Manager worked every time (length 36, never printed) |

## What it settles for RIV-wi-1 J1, and what it does not

- The lookup clauses (wiring before publish; a non-candidate makes 0 calls; a candidate is searched; an explicit ratio becomes one row
  with a source_url; a failed search is counted and the run goes on, nothing written): observed on the real code path with real data and
  the real vendor.
- A find was observed only after two failures. `run_for_day` has no retry: a failed search leaves the candidate for the next day's walk
  (the cap counts it again). At this account's failure rate (5 of 9) a candidate may wait several sweep days. Left for the round-29
  analysis, not changed here.
- The face's "Tokio Marine adjusted on the served page" clause: the served page IS adjusted (MEASURED, from the Bloomberg row, L2_READ_20261012
  facts 6-7), but that is not wi-1's work (row D1-C-S13). The only observation of an inferred row on a page-level object is row C above,
  at the series. No published page carries an INFERRED adjustment and none can be produced without a served write.

## Not measured

- A served or rendered HTML page adjusted from an actions-inferred row.
- That the lookup finds a split for a name the stored data does not already explain (no such name exists in the 30-day window: walk A).
