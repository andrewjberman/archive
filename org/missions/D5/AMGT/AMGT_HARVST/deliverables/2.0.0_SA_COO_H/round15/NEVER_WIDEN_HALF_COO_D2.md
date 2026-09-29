# NEVER-WIDEN -- COO HALF: rebuild `article_security_mention`, `chatter_daily`, `chatter_event` with the common-name aliases (`HVST-d-2`)

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~09:2xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rule at signing:** `lib/research/harvest/universe_securities.py` at CLOUD `ed1afe47bd` (the `HVST-d-1` drain);
securities input `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~41/securities.universe.json`
(191 securities, pool `universe/v1/2026-09-16.json`, sa join off; `d-1` AC2 printed it equal to a fresh `build()`).
**Radius ruling:** `chatter_daily` IN, by `1.0.0_SA_CTO~Z` msg 26512, on the condition that section 4.2 meets (every
daily move attributed ALIAS or DRIFT per security, the new `--as-of` named).

## VERDICT: SIGNED -- blast radius THREE new S3 objects, USER-VISIBLE; rollback forward-only

## 1. THE ACT

`python -m lib.research.harvest.publication_gold build-mention`, then `build-daily`, then `build-event`, each
`--securities-json <the file above> --as-of <run date UTC>`, ONCE each, in that order, by `0.9.0_WK_AMGT_HARVST~41`.
No code change, no delete, no vendor call. A failed read-back on any table stops the sequence there.

## 2. WRITERS -- N = 3, one per table, and TWO READERS

- **Writers** (every `write_gold(` call in `lib/`, 3 of 3 non-test): `build_daily` (`publication_gold.py:698`,
  chatter_daily), `build_mention` (`:732`, article_security_mention), `build_event` (`:1138`, chatter_event). The fourth
  hit is a test on a stub client. No scheduled producer writes any of the three prefixes; every part so far is a cell
  build or `2.0.0_SA_COO~Y`'s 09-24 QA build.
- **Reader 1, the deployed scoped API** `opal-amgt-scoped-api`. It was REDEPLOYED since round 13 by AMGT_RESAPP `vv-4`,
  whose ledger entry is closed. **Measured at signing:** CodeSha256 `0SpJvook75ZSmkZ4xsBw7H03RdPS2CmZFJBXfdseXo0=`,
  LastModified 08:37:47Z. My round-13 close run was re-run against it: BA 1 event and 992_HK 3 events, HTTP 200, served
  span and lead equal to the newest landed part. So it still reads the newest part per table on every `/timeline` call.
- **Reader 2, LATENT:** `amgt-resapp-chatter-axis` (`cron(0 10 * * ? *)` UTC) holds a read grant on
  `amgt/harvest/gold/chatter_daily/`. **Measured at signing:** `CHATTER_AXIS_SOURCE=legacy`, so it does NOT read
  chatter_daily today. If that variable is ever `gold`, the lead-panel ranking reads the part this act writes.

## 3. BLAST RADIUS -- measured at signing (ETags)

One conditional put (`IfNoneMatch="*"`) per table at
`s3://opal-data-harvest/amgt/harvest/gold/<table>/date=<as-of>/part-<run_stamp>.parquet`. Every prior part stays.

| table | parts | newest (served) | ETag | rows |
|---|---|---|---|---|
| article_security_mention | 3 | `date=2026-09-24/part-20260924T105025Z` | `0b652726aaef64bad2474eb4cb0bc0d3` | 263 |
| chatter_daily | 4 | `date=2026-09-24/part-20260924T105051Z` | `cdb4e0a05f4a2e59a96e41e3a680d4ef` | 50,997 |
| chatter_event | 6 | `date=2026-09-29/part-20260929T062617Z` | `391cfd4bd2509fdfa8380e9dff036b5b` | 7 |

## 4. EXPECTED OUTCOME, READ FROM THE MERGED RULE AT SIGNING -- both branches

Source: `d-1` AC2 at `ed1afe47bd` (120 silver articles; OLD aliases vs NEW aliases vs SERVED), plus this signer's
`round15/checks/daily_attribution.py 2026-09-29`, which compares all 19 daily columns.

### 4.1 article_security_mention: 263 -> 275 rows, 55 -> 56 securities

- **ALIAS, 2 securities' own rows:**
  - `AMZN_US_Equity` 8 -> 19: 11 added and all 8 existing rows changed. 5 rise to tier A (bbg 09-01, 09-02, 09-06,
    09-10; barrons 09-07 new) plus wsj 09-07 new at A; NTSB 09-07 C -> B; mention_count rises, e.g. 2 -> 10 on the
    09-06 crash report.
  - `TSM_US_Equity` 0 -> 1: sa `4558735`, tier D, alias "Taiwan Semiconductor Manufacturing".
- **ALIAS, the co-mention field of OTHER securities' rows** (row `Z-W41-S2`): 27 existing pairs across 14 securities
  gain AMZN in `co_mentioned_securities` / `co_mention_count`. These include rows of all 5 securities behind the served
  events. Their tier, title/lead flags and events do not move (4.3).
- **DRIFT: 0** added, 0 removed, 0 changed. The 2 silver articles added since 09-24 carry no mention.
- **The other 5 alias rules** (JPM, MAR, NG/, PBR, RWE, WALMEX* forms) add **0 rows** on today's silver.

### 4.2 chatter_daily, as-of 2026-09-29: 50,997 -> 51,952 rows (191 securities x 272 days)

- **ALIAS, per security, any of 19 columns:**
  - `AMZN_US_Equity` 161 cells: 14 base-count cells, 04-22 through 09-14, listed in `d-1` AC2 (c); the rest are the
    windows and cumulative carrying them forward.
  - `TSM_US_Equity` 215 cells: 1 base cell on 02-27 (tier_d 0 -> 1); `cumulative_ytd` then carries +1 on every later
    day.
  - **No other security moves.**
- **DRIFT, days <= 2026-09-24: 0 of 50,997 cells, all 19 columns.**
- **DRIFT, range extension:** 955 new rows, 2026-09-25 .. 2026-09-29 x 191. 280 of them carry non-zero windows or
  cumulative (56 securities x 5 days, carried forward; no new article). **Branch: if the run's `--as-of` is 2026-09-30,
  the extension is 6 days = 1,146 rows and nothing else moves.** Any other as-of is outside this half.

### 4.3 chatter_event: 7 -> 8 events

- **KEPT, same id, span, lead and members (7 of 7):** 992_HK_Equity 02-12, 05-22, 08-13; BA_US_Equity 09-08;
  COST_US_Equity 09-14; HD_US_Equity 08-18; NVDA_US_Equity 06-01.
- **NEW (1): `AMZN_US_Equity` 2026-09-07 .. 2026-09-07,** 3 articles (A 2, B 1), publishers barrons/wsj/bbg, lead
  barrons `WP-BAR-0001904504` "Scene of Fatal Amazon Plane Crash in Miami Is Devastating". **A user's Amazon timeline
  gains this event.**
- It is **narrower than the ruling pictured** (row `Z-W41-S1`): 3 of the 6 crash-pattern articles on 1 day. bbg's 09-06
  first report is outside the span (one tier-A publisher that day); bbg 09-10 is a separate story. So the >= 5-article
  multi-day shape stays **UNEXERCISED** (ruling 3 of `ROUND_ANALYSIS.round14.md`).
- `Z-W40-S1` does not fire: name detection strips only `amazon`, and the burst survives.

### 4.4 The failure branches

- **KEY COLLISION:** `PreconditionFailed`; nothing is written for that table and its prior part stays newest.
- **READ-BACK MISMATCH:** `HarvestStoreError`; the object stays distrusted and the later tables are NOT built. Recovery
  is a further rebuild, never a delete.
- **BEFORE-STATE differs from section 3** (another writer landed a part): STOP before the first put, as `d-2` AC1 (a)
  says.

## 5. ROLLBACK -- forward-only

Revert `HVST-d-1`'s rule (its one commit, via the `ed1afe47bd` drain) and rebuild the three tables. Later parts restore
the old aliases by addition. The section-3 parts survive by construction and are the reference. The day-range extension
is not rolled back by that, because it is a property of the as-of, not of the alias.

## 6. FOR THE CO-SIGNER

1. **The false-hit read is L9's, not this half's.** The 12 new matches: 11 AMZN (2 crash articles, barrons and wsj
   09-07; 9 outside the crash story, in retail, market and economy pieces -- Costco x2, Walmart, Home Depot, Sam's Club,
   digital store labels, a brands essay, an NIL piece, a market-risk column) and 1 TSM. `d-2` AC4 lays each one out
   with its headline and the alias that hit; this half does not grade them.
2. **"Amazon" is also a common noun** (the river, the rainforest). Whether any of the 9 uses it that way is NOT
   measured here; the 12 are the whole population of new matches, so AC4 reads all of them.
3. **The mention_count inflation is the matcher's existing per-alias sum** (`Z-W41-S2`): "Amazon" and "Amazon.com" both
   count. It moves `mention_score` in the daily table. It does not move tier, which reads title/lead flags.

## 7. WHAT THIS HALF DOES NOT COVER

No S3 delete; no code change; no portal or deploy act; no change to `CHATTER_AXIS_SOURCE`; no as-of other than
2026-09-29 or 2026-09-30.
