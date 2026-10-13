# ADVI_COTBKF -- ROUND 81 drain-end packet (L8), issuer 2.0.0_SA_COO~C2 on dell2, 2026-10-13T18:00Z

**To:** `3.0.0_SA_CVO`. **Round:** 81, cut on the CTO's round-81 analysis @ab1112493b (msg 7078) over PRD v0.10 @4d488ab2f0 (ADMITTED at the cut; no addendum).
**Issuance:** @873fe28f00 (3 cells, `fanout: 3 of 3 chains, cap 8`); item 4 (`closes_when`) @5092d778a6 under the audited TREE_DELIVERABLES override, its own commit, because the lane refuses the issuer
on a file directly under `deliverables/` (the refusal printed first). **All 3 orders terminal.** Nothing was built, applied, served, corrected, re-minted or fetched from a vendor.

## What each cell found (each check re-run by the issuer at the base after its merge)

| cell | worker | merge | record | check line (head) |
|---|---|---|---|---|
| CB-cc-1 | ~158 | a4de227548 | `deliverables/0.9.0_WK_ADVI_COTBKF~158/CONSUMER_READ.json` | `CONSUMER-READ tables=3 prefixes=3 graph_calls=13 control_found=True consumers=2 with_a_page=0 searches=20 disarm_fact_a=consumers_found build_after_feeds_served=True` |
| CB-cc-2 | ~159 | 938efa86c5 | `deliverables/0.9.0_WK_ADVI_COTBKF~159/STAGE_READ.json` | `STAGE-READ securities=5 with_six_stage_keys=5 with_a_first_stage=5 served_prefixes=3 store_bytes_match=True` |
| CB-cc-3 | ~160 | 93297eaab7 | `deliverables/0.9.0_WK_ADVI_COTBKF~160/DATE_BOUNDS.json` | `DATE-BOUNDS windows=4 total=4 moving=1 with_a_rule=1 built_before_bound=1 earliest=2013-04-03 floor=2012-01-01` |

1. **The consumers (cb-cc-1).** Each of the three minted prefixes holds ONE object (written 2026-10-09T12:41Z; listing limit 5, complete). Two direct code readers: the ARD adapter
   `commonwealth_account_return_daily.py:221-226` (all three tables) and `commonwealth_price_basis_census.py:292-295` (`account_day_value`); neither serves a page. A second hop is in code:
   ARD output, gold `account_return_daily`, `reporting-publish/handler.py`, the InvestorReporting dashboard; the read route is recorded "Planned, not applied" (`lambda-source-map.json:6485`), so liveness is NOT established.
   The graph shows no portal-page reader (its positive control had to be changed: the order's named control, the cot price store, returned nothing; `platinum/firm/client_directory.json` found known consumers; the graph's zero is for the portal-platinum domain only).
   `disarm_fact_a = consumers_found`: per the CTO's ruling 1, row `D2-W155-S1` stays ARMED and the correction is the next cell, under a never-widen pair.
   **My disarm row `D2-S134` is contradicted by this read:** it said no consumer on the minted table and "0 objects" (the never-widen record's wording); there are two code readers and one object per prefix. Row `D2-W158-S2` (owner the CTO) says so.
2. **Where the five leave 1.0 (cb-cc-2).** For APH, CTVA and HON the first stage off 1.0 is store row against the cached vendor Close (store/vendor 1.9859, 6.65, 0.9488). On the chosen day the build and the minted copy EQUAL the vendor Close, and
   the STORE row is the side nearer the price paid (store/price paid 0.9672, 0.9898, 0.9986; build/price paid 0.487, 0.1488, 1.0525). So the served error enters where the build takes the vendor Close in place of the store's row; the worker names the writer to read next
   (`build_canonical_prices_v2.py:705-707`, `:822`, `:571`) and did not run it: the builder shape, not proven as the writer of the live bytes. KLAC and SCCO: no build or store row on their held day, `not_established`. No chosen day falls in the served window, so `served_row` is absent for all five;
   a supplementary read of HON's 47 partitions: 9 days, 2 accounts (count), served/store 1.0, served/minted 0.9535 on 7 days.
3. **The bounds (cb-cc-3).** Earliest client record 2013-04-03 (1,533 accounts: 0 before 2012, 1,026 in 2012-2019, 97 in 2020, 410 after); the 2012 floor moves no client history. Of 4 determinate windows 1 moves: the canonical price store (2006-01-02, 2,190 days before the floor).
   8 windows `not_established` (the dell1 request window, the minted table's range, the 47 partitions' contents among them). The law was quoted from `origin/box/dell1` @82c7c92449.
4. **`closes_when`** now quotes v0.10 lines 416-419 (commit above); no gate limb graded the edit.

## Rows, and what is owed at L9

- ARMED: `D2-W155-S1` (CTO), `D2-W158-S2` (CTO), `D2-W159-S1` (disarm_owner this seat: the store holds two `asset_name` values under one ticker, SCCO on 1,027 dates and APH on 70; I did NOT disarm it, because "whether any consumer keys by ticker alone" is
  unread and no cell this round reads it).
- Worker rows that read wrongly: `D2-W160-S2` (BLOCKING/INERT) and `D2-W158-S4` say the status flip is outside the worker's `<paths>`; worker ~159 flipped its own order under the identical block, so the issuer flipped ~158 and ~160 (commits 5224f3b6f5, 37f0d13706). Grade them.
- Other worker rows: W158-S1, S3, S5; W159-S2; W160-S1 (`Cost_Date` 1901-01-01 on 2 rows and before 2000 on 389; the bound uses `Trade_Date`).
- **Owed at L9 (3.0.0_SA_CVO):** `CB81cc1-AC2`, `CB81cc2-AC2`, `CB81cc3-AC2`. `round-close-check --project ADVI_COTBKF --round 81`: REFUSED, 3 ungraded, 0 self-graded (expected before L9).
- Worker ~159 wrote no short `.md` (its stated reason: an operator rule against report `.md` files); the JSON carries the headline, the absent list and `not_established`.
- Remote reads: ~158 three `list-objects-v2 --max-items 5`; ~159 one price-store `get-object` (97,443,387 bytes, matched), 48 gold holdings gets, three listings; ~160 none. No write, delete or vendor call. Account-id scans: 821, 820, 821 files, 0 hits.

## Not established (carried)

Whether the read route to the InvestorReporting dashboard is live; the writer of the live store bytes (the census writer is not in the tree); KLAC and SCCO on any held day; the 8 windows above; whether any consumer keys the store by ticker alone.
