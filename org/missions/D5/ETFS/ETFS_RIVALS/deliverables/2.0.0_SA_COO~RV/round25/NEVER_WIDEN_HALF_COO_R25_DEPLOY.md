# NEVER-WIDEN -- COO HALF: ETFS_RIVALS round 25 (RIV-rg-1 the readers' grain; RIV-mr-1 the marker read-out) -- deploy the five rivalfunds Lambdas at CLOUD acf83a5716, republish 2026-10-07 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-07 ~23:3xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** row ETFS_RIVALS-Z-S69 (BLOCKING, ARMED; corrected by Z-S70): every reader of gold security_market keeps one
object per date, and for 2026-09-29 the one kept is an import with no price, so 430 market closes reach no stage. CTO
rulings msgs 31416, 31428 (round 25 today; three terms) and 31432 (a close and its currency from the same object).
RIV-mr-1 rides: the two chart faults of CVO ADJUDICATION_v28. No vendor is called; no wheel is built; nothing is fetched.

## VERDICT: SIGNED, conditional on RIV-rg-1 J1 MET

**THIS ACT MOVES SERVED FIGURES, AND THAT IS ITS PURPOSE.** Conditions: RIV-rg-1 J1 MET is on file from
`3.0.0_SA_CVO~RV` before the apply (RIV-mr-1 J1 not MET does not hold the readers' fix: then mr-1's two faults stay as
served today, since its code is in the pin either way -- the CTO half says whether that is accepted); the pin is CLOUD
acf83a5716; every read below holds; the act stops at the first differing read.

## WHAT THE PIN CARRIES OVER THE LIVE CODE (f9f8334ef6, live since 21:2xZ, ledger `etfs-rivalfunds-r24` CLOSED)

Over every path the packager stages: **8 files of the rivalfunds package and nothing else** (no rider this time: the naming
library, the registry, the identity library, the wrappers and the Terraform root are unchanged): `gold_holding_contribution.py`
(+103 / -5, the shared reader `g4_rows` / `g4_window`), `gold_canonical_shape.py` (+16 / -8), `gold_trade_schedule.py` (+9 /
-14), `gold_input_census.py` (+6 / -5), `gold_buying_trend.py` (+4 / -4), `price_series.py` (+1 / -2), `publish_page.py` (+1 /
-2), `render.py` (+8 / -8, the script 9,348 to 9,502 bytes, still one fetch to this product's chart route).
`gold_canonical_shape` now imports the shared reader, and with it pandas, inside `_g4_for`: all five live functions carry
the layer `pandas-pyarrow-requests-layer:1` (read from `list-functions`, 5 of 5).

## THE THREE TERMS OF MSG 31428

1. **The rule, and what it keeps for 2026-09-29.** Rows of a (security, date) are ordered non-backfill first, live before
   import, later capture time in the name, later `as_of`, the name last. The price group (close, day return, currency,
   `as_of`, `source`, `as_of_source`) travels whole from the first row that has a close; descriptive fields fill column by
   column. Read on the live table through the deployed-to-be function: 589 rows; the live pull's close for all 430
   securities it prices, 0 closes with a null currency, sectors 577 (the live pull's, else the import's); the 17
   securities in both objects take the live pull's close (the import's is null for all 17). The name decides nothing.
2. **Before and after.** `round25/before_after_tables_2026-10-07.json` names every moved row. buying_trend: 0 of 1,406.
   holding_contribution: 2,418 rows of the 30d / 90d / 365d periods move (2,125 security, 293 sector), all 13 funds; 108
   security rows enter or leave a top or bottom ten (IDVZ 0); among security rows the median move is 0.0085 percentage
   points, 36 exceed 0.10, the largest is 0.233 (MediaTek in CGIC, 30 days, +0.062 to +0.295, rank 5 to 2). How many of
   the closes reach today's page: 408 chart points of 2026-09-29 become market closes (101 were valuation-implied, 307
   empty); in the tables the day is priced from the market for the holdings on 2,363 rows.
3. **The control.** Through the new reader 2026-10-02 (three objects) and the three single-object dates are identical to
   the object picked before, in every column; 0 duplicate (security, date) anywhere.

## THE ACT, IN ORDER

1. Read J1 MET on file. **Open the NEVER-2 ledger entry** (slug `etfs-rivalfunds-r25`): apply; republish; served read;
   and the first daily run on the new readers (2026-10-08 11:00Z) as a leg, since `gold_canonical_shape` and
   `gold_trade_schedule` run only there.
2. **`safe-apply` of `C:/tmp/rv_apply25.tfplan`** from `C:/tmp/rv-r8` at the pin (plan text `round25/rv_apply25.plan.txt`):
   **0 to add, 5 to change, 0 to destroy**; `source_code_hash` and `last_modified` only. Before = the live set (daily
   3BFfLeYC, fetch mHg1VZz2, canonical vTjVc2Ym, silver 0hmlWkob, publish 8PjWCoxj); after = daily TTbIYgXA, fetch WL/sCGMO,
   canonical lyTfhuTJ, silver 9WgsN3AG, publish lF0sf7UF.
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-07","mode":"daily","batch_id":"rv-publish-1007r25","sink":"s3","refresh_a1":true}`.
   `refresh_a1` is TRUE: the tables' readers changed and no input is newer, so without it the tables would be skipped.
4. Download the served objects and the three rebuilt tables; grade; run `before_after_tables.py` against the SERVED
   after-tables; close the apply, republish and served legs.

## THE WRITE SET, READ FROM THE CODE PATH, with the rollback per key

Under `s3://opal-data-etfs/rivalfunds/etfs/`:

| key | when | expected | rollback |
|---|---|---|---|
| five Lambda code hashes | the apply | the after-set | re-package at f9f8334ef6, plan, `safe-apply` |
| `gold/holding_contribution`, `gold/buying_trend`, `gold/input_census` at `date=2026-10-07` | `produce_a1` with `refresh_a1` | ONE new write-once object each; the earlier objects stay | after a code rollback, one republish with `refresh_a1` true writes a newer object in the old reading; the stages read the newest |
| `platinum/page/date=2026-10-07/revisions/<stamp>/` | the served objects copied first | index, manifest, 13 charts, and audit.html (its bytes change this time): 16 copies | none; they are the rollback |
| `.../index.html`, `.../audit.html`, 13 `.../charts/*.json`, `.../manifest.json` | the publisher's write block, in the order read for round 22 | index 1,694,876 B; audit 1,255,783 B; charts 5,732,176 B, 5,896 markers; `fund_sections` 0 missing | republish from the rolled-back code, or copy back from `revisions/` |
| `state/publish_page/date=2026-10-07/rv-publish-1007r25.json` | the run's record | one object | none |
| `gold/security_market` | never | **no write, no delete** | -- |
| `gold/canonical_shape`, `gold/trade_schedule` | not by this act | no write: a republish does not run those stages | -- |

Prediction source: `round25/real_run_2026-10-07.after_r25.json`, the real-run tool at code equal to the pin over the
packaged paths. **One known gap in that tool:** it rebuilds holding_contribution and buying_trend locally and NOT
input_census, whose reader also changed. So the served bytes may differ from the prediction where the page shows the
census. A difference is READ and reported before the ledger closes; it is not by itself a rollback.

## BOTH BRANCHES

- **Fits** (round 22's refresh run: 164.5 s, 1,009 MB of 3,008; this one opens 3 more objects of the price table per
  365-day read): status OK, the reads above.
- **Killed or timed out:** tables first, then copies, index, audit, charts, manifest. C1 as before: manifest not older
  than index and 13 chart objects, or one more republish, else roll back.
- **The served after-tables differ from the local after-tables:** the before / after is re-run on the served ones and
  that is the record; a move on a row the local run did not move is named to the CTO before the ledger closes.
- **Tomorrow's 11:00Z run** is the first to run `gold_canonical_shape` and `gold_trade_schedule` on the new readers, on a
  date with one object: the same rows as today's rule would read. It is a leg, read with ledger r22's L4.

## WHAT THIS ACT DOES NOT PROVE, AND WHAT IT LEAVES

- The AI accounts were written on the old tables; after this act their figures and "top contributor" names can disagree
  with the tables beside them until the 2026-10-08 13:00Z sweep. 25 badges already say "Grounded on an earlier build".
- A design limit, not introduced here: a market-priced day between valuation-implied days can count a move twice or
  miss one where a fund's valuation lags. Not measured. MediaTek's 0.233 is the figure to look at first.
- The input census still records a date's newest object as a price's location; for 2026-09-29 that names the import.
  Whether the served page shows that location anywhere was not read.
- Worker row Z-W15-S2: a live row with no close beside a backfill row with one. No such partition exists; round 26.
- Upstream tables of earlier dates (the GICS join in G1, the parsekeys in G5) are not rebuilt.
