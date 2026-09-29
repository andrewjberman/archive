# NEVER-WIDEN -- COO HALF: rebuild `article_security_mention` and `chatter_daily` with one span, one count (`HVST-e-2`)

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~11:1xZ. **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rule at signing:** `lib/research/harvest/publication_gold.py` `_match_counts` / `_span_pattern` at CLOUD `5f25e64267` (the
`HVST-e-1` drain). **Securities input:** `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~41/securities.universe.json`
(unchanged since round 15). **Measured by:** `round16/checks/span_attribution.py 2026-09-29`, which compares every served
column. It reproduces `e-1` AC2 on every count below.

## VERDICT: SIGNED -- blast radius TWO new S3 objects, USER-VISIBLE; no event put; rollback forward-only

## 1. THE ACT

`python -m lib.research.harvest.publication_gold build-mention`, then `build-daily`, each `--securities-json <the file
above> --as-of <run date UTC>`, ONCE each, in that order, by `0.9.0_WK_AMGT_HARVST~42`. No `build-event`, no code change,
no delete, no vendor call. A failed read-back on mention stops the sequence before daily.

## 2. WRITERS -- N = 3 (unchanged since round 15), TWO READERS

- **Writers:** `build_daily` (`publication_gold.py`, chatter_daily), `build_mention` (article_security_mention),
  `build_event` (chatter_event; NOT run by this act). No scheduled producer writes any of the three prefixes.
- **Reader 1, the deployed scoped API** `opal-amgt-scoped-api`. **Measured at signing:** CodeSha256
  `CtIvirvMTG47vvgBGmouk3GrTNKPjPIPx/6ovB+EAOM=` (the round-13 code, after the RESAPP `vv-4` rollback). It serves the
  newest daily part as the `/timeline` `series` and the newest event part as `events`.
- **Reader 2, LATENT:** `amgt-resapp-chatter-axis`. **Measured at signing:** `CHATTER_AXIS_SOURCE=legacy`, so it does
  not read chatter_daily today.

## 3. BLAST RADIUS -- measured at signing (ETags)

| table | parts | newest (served) | ETag | rows | this act |
|---|---|---|---|---|---|
| article_security_mention | 4 | `date=2026-09-29/part-20260929T092419Z` | `4a5e91d38405f09d3052343f69a68151` | 275 | ONE put |
| chatter_daily | 5 | `date=2026-09-29/part-20260929T092435Z` | `561a3bd6513eccacd68dab502a5a3a93` | 51,952 | ONE put |
| chatter_event | 7 | `date=2026-09-29/part-20260929T092439Z` | `c146a325c98963f965b8b1bd69ca3393` | 8 | NONE; stays newest |

Each put is conditional (`IfNoneMatch="*"`), at `amgt/harvest/gold/<table>/date=<as-of>/part-<run_stamp>.parquet`. Every
prior part stays.

## 4. EXPECTED OUTCOME, READ FROM THE MERGED RULE AT SIGNING -- both branches

### 4.1 article_security_mention: 275 -> 275 rows; 0 added, 0 removed; DRIFT 0 of 275 on all 22 columns

**SPAN moves, 6 securities, 14 rows** (columns moved -> rows):

| security | mention_count | match_forms | signal_tier / signal_weight | tier moves |
|---|---|---|---|---|
| `AMZN_US_Equity` | 8 | 7 | 2 | C->D 2 (`barrons:WP-BAR-0001882188`, `sa:4638889`) |
| `UPS_US_Equity` | 2 | 2 | 2 | C->D 2 |
| `DAL_US_Equity` | 1 | 1 | 1 | C->D 1 |
| `FDX_US_Equity` | 1 | 1 | 1 | C->D 1 |
| `GOOGL_US_Equity` | 1 | 1 | 1 | C->D 1 |
| `GOOG_US_Equity` | 1 | 1 | 1 | C->D 1 |

Title, lead and blocks_hit move on **0** rows, so no row moves into or out of tier A or B. Example: the AMZN 09-06 crash
report `bbg:TKYJAAVTTCZL00` goes from `mention_count` 10 to 8, still tier A (`e-1` report).

### 4.2 chatter_daily: 51,952 -> 51,952 rows; DRIFT 0 cells on all 19 columns

**SPAN cells per security (212):** AMZN 41, DAL 65, GOOGL 29, GOOG 29, UPS 24, FDX 24.
- Direct columns are `mention_count_total`, `mention_score`, `tier_c` and `tier_d`: AMZN 7 count cells and 2 tier cells;
  UPS 2 each; DAL, FDX, GOOGL and GOOG 1 each.
- Every other moved cell is a trailing, baseline or cumulative window carrying those forward.
- **No other security moves.**

**The `--as-of` branch:**
- **At 2026-09-29:** the served daily part already ends on 09-29, so there are 0 extension rows.
- **At 2026-09-30:** exactly 191 extension rows are added (one day x 191 securities), a DRIFT move and nothing else.
- Any other as-of is outside this half.

### 4.3 chatter_event: NOT WRITTEN; expected equal

`event_rows` over the NEW mention rows equals the served newest event part **row by row (8 of 8)**, measured at signing.
If `e-2` AC2 finds it unequal after the mention put, that is a finding (BLOCKING row). The remedy is a separate pair,
never an event put under this half.

### 4.4 The failure branches

- **KEY COLLISION:** `PreconditionFailed`; nothing is written for that table and its prior part stays newest.
- **READ-BACK MISMATCH:** `HarvestStoreError`; the object stays distrusted and daily is NOT built. Recovery is a further
  rebuild, never a delete.
- **BEFORE-STATE differs from section 3, or silver has moved:** STOP before the first put (`e-2` AC1 (a)). A silver
  move surfaces as a moved row OUTSIDE THE PAIR in AC1 (d), which FAILS the run.

## 5. ROLLBACK -- forward-only

Revert `HVST-e-1`'s matcher (the `5f25e64267` drain) and rebuild mention and daily. Later parts restore the round-15 counts
by addition. The section-3 parts survive by construction and are the reference.

## 6. FOR THE CO-SIGNER

1. **The ruling's premise ("does not touch tier") holds for A/B and not for C/D.** Tier C is `mention_count >= 2`
   (`assign_tier`). 8 rows fall to D, and their `signal_weight` and the daily `mention_score` fall with them. Carded to
   you at the issuance (my msg of 10:28Z); the counts above are read from the merged code.
2. **Leftmost-first scanning:** a shorter alias that starts before a longer overlapping one would win the position.
   `e-1` records it as a declared exclusion because none of the 14 moved rows has a half-overlap. It is not measured on
   rows outside today's silver.

## 7. WHAT THIS HALF DOES NOT COVER

No S3 delete; no event put; no code change; no portal or deploy act; no change to `CHATTER_AXIS_SOURCE`; no as-of other
than 2026-09-29 or 2026-09-30.
