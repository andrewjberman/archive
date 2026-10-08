# NEVER-WIDEN -- COO HALF: ETFS_RIVALS rounds 25 + 26 readers (RIV-rg-1 as narrowed by RIV-rg-2) -- deploy the five rivalfunds Lambdas at CLOUD 0576fb051f, republish 2026-10-07 ONCE

**Signer:** `2.0.0_SA_COO~RV`, 2026-10-08 ~01:0xZ, FULL. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (asked).

**Why:** the shared reader of gold security_market (round 25) with the rule of CTO ruling msg 31480 (round 26): the union
applies to objects whose name carries a capture time; a date's untimed objects are read as before. It brings the
deployed code back onto CLOUD's history and puts the union in place for FWD-24's top-ups, WITHOUT moving a served
figure. Row ETFS_RIVALS-Z-S71. No vendor is called; no wheel is built; nothing is fetched.

## VERDICT: SIGNED, conditional on RIV-rg-2 J1 MET

**THIS ACT MUST MOVE NO SERVED FIGURE.** Conditions: RIV-rg-2 J1 MET is on file from `3.0.0_SA_CVO~RV` before the apply;
the pin is CLOUD 0576fb051f; every read below holds; the act stops at the first differing read; **one moved table row on
the served after-tables is a rollback the same hour** (as the CTO's C2 of the last half).

## WHAT THE PIN CARRIES OVER THE LIVE CODE (content pin fd633ec4d2, live since 00:1xZ)

`git diff fd633ec4d2 0576fb051f` over every path the packager stages: **7 files of the rivalfunds package and nothing else**
-- `gold_holding_contribution.py` (+110 / -5), `gold_canonical_shape.py` (+21 / -8), `gold_trade_schedule.py` (+9 / -14),
`gold_input_census.py` (+6 / -5), `gold_buying_trend.py` (+4 / -4), `price_series.py` (+1 / -2), `publish_page.py` (+1 / -2).
`render.py` is equal (RIV-mr-1 is already live). No rider. The real run ran on the worker branch, which equals the pin
over the packaged paths (`git diff edc990895b 0576fb051f`: empty). All five live functions carry the pandas layer the
canonical-shape stage now imports through the shared reader.

## WHAT WAS READ BEFORE SIGNING (packet `round26/DRAIN_END_PACKET.round26.md`)

- The live table through the narrowed reader, all five dates: identical in every column to the object the live code
  picks. 2026-09-29: the import alone, 0 closes; the mis-dated object is not opened. 2026-10-02: three timed objects,
  601 rows, equal to the newest.
- The real run FROM THE BRANCH, before the merge: 0 of 6,066 rows of holding_contribution move, 0 of 1,406 of
  buying_trend; 13 of 13 chart objects with data identical to the served ones; audit byte-equal; the index differs only
  in the two rebuilt tables' revision stamps.
- This is the read the round-25 half lacked: that half reported 3,259 moved rows as a repair, and they were the effect
  of a mis-dated object. Here the expected number is zero and it is zero.

## THE ACT, IN ORDER

1. Read J1 MET on file. **Open the NEVER-2 ledger entry** (slug `etfs-rivalfunds-r26`): apply; republish; served read;
   and the 2026-10-08 11:00Z daily run as a leg (the first run of `gold_canonical_shape` and `gold_trade_schedule` on the
   shared reader).
2. **`safe-apply` of `C:/tmp/rv_apply26.tfplan`** from `C:/tmp/rv-r8` at the pin (plan text `round26/rv_apply26.plan.txt`):
   **0 to add, 5 to change, 0 to destroy**; hashes and `last_modified` only. Before = the live set (daily UHfCiT80, fetch
   OoXPTjMF, canonical 7KNOgjTc, silver 7SS2kS3b, publish DGtKYZj1); after = daily hwvMccck, fetch n7y+Lj2a, canonical
   uLmr4Ejy, silver 7KmpjwMV, publish 3ug0KrGK. (`C:/tmp/rv_apply25.tfplan` is the WITHDRAWN deploy's plan: not applied.)
3. **ONE real run (the republish):** `AWS_MAX_ATTEMPTS=1`, `etfs-rivalfunds-daily-lambda
   {"only":["publish-page"],"date":"2026-10-07","mode":"daily","batch_id":"rv-publish-1007r26","sink":"s3","refresh_a1":true}`.
   `refresh_a1` is TRUE on purpose: with it false the page would render byte-equal and the publisher would write nothing,
   proving nothing about the new readers in the Lambda. With it true the three A1 tables are rebuilt BY the new readers,
   hours before the 11:00Z run depends on them, and the served after-tables can be compared row for row.
4. Download the served objects and the rebuilt tables; `before_after_tables.py` on the SERVED after-tables against the
   tables served before (kept: the 17:45Z / 17:46Z objects stay in S3): **0 moved rows, or roll back**; chart data
   identical; close the apply, republish and served legs.

## THE WRITE SET, READ FROM THE CODE PATH, with the rollback per key

| key under `s3://opal-data-etfs/rivalfunds/etfs/` | expected | rollback |
|---|---|---|
| five Lambda code hashes | the after-set | re-package at fd633ec4d2 (branch `rv-deploy-r25mr`), plan, `safe-apply` |
| `gold/holding_contribution`, `gold/buying_trend`, `gold/input_census` at `date=2026-10-07` | ONE new write-once object each, rows equal to the object before it (compared for the first two; input_census is compared too, by the same key-and-column read, and reported) | after a code rollback one republish with `refresh_a1` true writes a newer object; the earlier objects are never removed |
| `platinum/page/date=2026-10-07/revisions/<stamp>/` | index, manifest, 13 charts copied first; audit only if its bytes change | none; they are the rollback |
| `.../index.html` | 1,693,709 B, the served size; only the tables' revision stamps differ | republish from the rolled-back code, or copy back |
| `.../audit.html`, 13 `.../charts/*.json`, `.../manifest.json`, one state record | audit byte-equal or stamp-only; chart data identical, 5,894 markers | same |
| `gold/security_market`, `gold/canonical_shape`, `gold/trade_schedule` | **no write** by this act | -- |

Prediction: `round26/real_run_2026-10-07.after_rg2.json`. Its known gap stands: the tool rebuilds two tables, not
input_census; the served input_census is therefore compared after the act, not predicted.

## BOTH BRANCHES

- **Fits** (round 22's refresh run: 164.5 s, 1,009 MB of 3,008): status OK; 0 moved rows.
- **A row moves, or a chart point differs:** rollback to fd633ec4d2 the same hour, then one republish with `refresh_a1`
  true so the newest table objects are again the old readers'; the moved rows are named to the CTO.
- **Killed or timed out:** tables, then copies, index, audit, charts, manifest. Manifest not older than index and 13
  chart objects, or one more republish, else roll back.
- **The 11:00Z daily run** (date 2026-10-08, a new single-object partition with a timed name): the union of one object
  is that object. It is a leg, read with ledger r22's L4 and the vehicle log read of row Z-S72.

## WHAT THIS ACT DOES NOT PROVE

- That no future object is mis-dated: the rule is a name's shape plus one named object. Round 27 carries the per-close
  trading date (CTO term 2, msg 31480).
- Anything about a date with timed objects that disagree: none exists in the live table (2026-10-02's three hold the
  same rows, one of them with no closes).
