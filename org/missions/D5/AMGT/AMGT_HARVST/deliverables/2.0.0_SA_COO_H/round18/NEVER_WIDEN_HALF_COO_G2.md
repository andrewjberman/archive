# NEVER-WIDEN -- COO HALF: rebuild `article_security_mention`, `chatter_daily`, `chatter_event` on the round-18 alias rule (`HVST-g-2`)

**Signer:** `2.0.0_SA_COO~H`. **Date:** 2026-09-29 ~19:0xZ (15:0x ET). **Pairs with:** `1.0.0_SA_CTO~Z`'s half (owed).
**Rule at signing:** `lib/research/harvest/publication_gold.py` and `universe_securities.py` at CLOUD `a802677065` (the
`HVST-g-1` drain). The harvest suite passes 194 of 194 on the merged trunk. **Securities input:**
`org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~45/securities.universe.json` (written by `g-1`; 191
securities; `ticker_aliases` on 191 of 191). **Measured by:** a fresh run of `g-1`'s AC2 script at signing, saved beside
this file as `g2_signing_ac2_rerun.txt`. It is BYTE-IDENTICAL to `g-1`'s committed `ac2_output.txt`, so silver has not
moved since the cell ran (120 articles, 60 listing rows). **That file IS the expected diff.**

## VERDICT: SIGNED -- blast radius THREE new S3 objects, USER-VISIBLE; rollback forward-only

## 1. THE ACT

`python -m lib.research.harvest.publication_gold build-mention`, then `build-daily`, then `build-event`, each with
`--securities-json <the file above> --as-of <run date UTC>`. Each runs ONCE, in that order, by
`0.9.0_WK_AMGT_HARVST~45`, from CLOUD code at or after `a802677065`. Code from before `g-1` silently ignores
`ticker_aliases` (row `Z-W45-S3`). No code change, no delete, no vendor call. A failed read-back on any table stops the
sequence before the next one.

## 2. WRITERS -- N = 3, TWO READERS (measured at signing)

- **Writers:** `build_mention` (article_security_mention), `build_daily` (chatter_daily) and `build_event`
  (chatter_event), all in `publication_gold.py`. No scheduled producer writes any of the three prefixes.
- **Reader 1, the deployed scoped API** `opal-amgt-scoped-api`: CodeSha256
  `CtIvirvMTG47vvgBGmouk3GrTNKPjPIPx/6ovB+EAOM=`, LastModified 2026-09-29T09:56:25Z. That is unchanged since round 16's
  half. It serves the newest daily part as the `/timeline` `series` and the newest event part as `events`.
- **Reader 2, LATENT:** `amgt-resapp-chatter-axis`, with `CHATTER_AXIS_SOURCE=legacy` (LastModified
  2026-09-24T05:09:00Z). It does not read chatter_daily today.

## 3. BLAST RADIUS -- measured at signing (S3 list plus a read of the newest part)

| table | parts | newest (served) | ETag | rows | this act |
|---|---|---|---|---|---|
| article_security_mention | 5 | `date=2026-09-29/part-20260929T112204Z` | `b8118b05d3160c7c31b4955c22732afe` | 275 | ONE put |
| chatter_daily | 6 | `date=2026-09-29/part-20260929T112222Z` | `06025a62eb771b336f33fe097d50c61c` | 51,952 | ONE put |
| chatter_event | 7 | `date=2026-09-29/part-20260929T092439Z` | `c146a325c98963f965b8b1bd69ca3393` | 8 | ONE put |

Each put is conditional (`IfNoneMatch="*"`) at `amgt/harvest/gold/<table>/date=<as-of>/part-<run_stamp>.parquet`.
Every prior part (18 in all) stays, and its ETag is unchanged.

## 4. EXPECTED OUTCOME, READ FROM THE MERGED RULE AT SIGNING -- both branches

### 4.1 article_security_mention: 275 -> 304 rows; DRIFT 0; every move ALIAS

- **Moved mention rows: 186**, each attributed ALIAS, with 0 DRIFT.
  - 244 added spans over 132 (article, security) pairs, 29 of them NEW pairs. 0 spans lost.
  - The per-security list is in the rerun file, section (a): 51 securities, 51 forms. The largest are Dell 40, BA 31,
    COST 19, NVDA 13 and AAPL 12.
- **Existing rows:**
  - Title flips 7 and lead flips 10.
  - Tier changes on 45 rows. Tiers can move in both directions (D->C appears, e.g. UPS on the Miami cargo-plane
    report).
- **Tier-A/B securities: 29 -> 36.** The new ones include ASML_NA and ASML_US.
- **Pair uniqueness:** 304 of 304 (article, security) pairs are unique.

### 4.2 chatter_daily: 51,952 -> 51,952 rows; DRIFT 0 cells

- **ALIAS moved cells: 4,286 across EXACTLY the 50 securities listed in section (b) of the rerun file (lines
  562-611).** Any daily cell outside those 50 securities is OUTSIDE THE PAIR.
- **Columns moved:**

  | column | cells |
  |---|---|
  | `cumulative_ytd` | 4,261 |
  | `trailing_30d_sum` | 1,563 |
  | `baseline_30d_sum` | 1,444 |
  | `trailing_7d_sum` | 441 |
  | `data_status` | 148 |
  | `publishers_covered` | 148 |
  | `mention_count_total` | 114 |
  | `mention_score` | 69 |
  | `tier_d` | 47 |
  | `tier_c` | 42 |
  | `articles_total` | 27 |
  | `first_published_utc` | 27 |
  | `last_published_utc` | 27 |
  | `publishers_distinct` | 27 |
  | `tier_b` | 17 |
  | `tier_a` | 6 |

- **The 148 `data_status` / `publishers_covered` cells are ASML_NA and ASML_US** (row `Z-W45-S2`). The whole-brand alias
  `ASML` joins the publisher-coverage match (`sa` listing rows 2026-07-15..09-26), and each of those days moves from
  DENIED to PARTIAL. It is user-visible on the timeline, and this half covers it by name.
- **FDX_US_Equity is NOT in the pair for daily.** It gains 1 span (mention_count 6 -> 7 on "US Earnings to Watch:
  FedEx, Costco, ..."), yet the rebuild moves 0 FDX daily cells. The cause is unmeasured here, most likely that the
  article's day lies outside the daily series. If an FDX daily cell moves after the put, AC1(b) prints it as OUTSIDE THE
  PAIR and the run FAILS.

**The `--as-of` branch:**
- **At 2026-09-29:** the served daily part already ends on 09-29, so there are 0 extension rows.
- **At 2026-09-30:** exactly 191 extension rows are added (one day x 191 securities). That is a DRIFT move and the
  only permitted one.
- Any other as-of is outside this half.

### 4.3 chatter_event: 8 -> 8; KEPT 8, MOVED 0, GONE 0, NEW 0

The new rebuild's events equal the 8 served events row by row: 992_HK x3, AMZN, BA, COST, HD, NVDA. All 8 event ids
are unique. The event put therefore writes a new newest part whose rows equal today's served rows. Any event row that
differs is OUTSIDE THE PAIR.

### 4.4 The failure branches

- **KEY COLLISION:** `PreconditionFailed`; nothing is written for that table and its prior part stays newest.
- **READ-BACK MISMATCH:** `HarvestStoreError`; the object stays distrusted and no later table is built. Recovery is a
  further rebuild, never a delete.
- **Mention lands, then daily fails:** the timeline keeps serving the section-3 daily and event parts. Mention has no
  served reader, so the served view is unchanged until a later rebuild.
- **BEFORE-STATE differs from section 3, or silver has moved:** STOP before the first put (`g-2` clause 1.5 dry step).
  A silver move surfaces as a DRIFT row, and in AC1(b) as OUTSIDE THE PAIR, which FAILS the run.

## 5. ROLLBACK -- forward-only

Rebuild all three tables from the round-17 securities file
(`deliverables/0.9.0_WK_AMGT_HARVST~41/securities.universe.json`). Under the merged code, a file without
`ticker_aliases` matches exactly as before; the matcher is byte-identical
(`test_the_matcher_is_byte_identical_to_the_old_one_without_exact_forms`). The later parts restore the round-17 values by
addition. The section-3 parts survive by construction and are the reference.

## 6. FOR THE CO-SIGNER

1. **This act is wider than round 16's.** It touches 50 securities' daily series, not 6, and its user-visible effects
   are these:
   - The ASML DENIED->PARTIAL coverage change.
   - Tier-A/B rows appear for 7 more securities.
   - Tier C/D weights move.
2. **Events are unmoved.** No served event is kept, moved or lost differently, and no new event forms, so the timeline's
   `events` do not change. Only its `series` changes.
3. **AC4 of `g-1`** (179 of 244 added hits sampled across 52 form blocks, "is it the company?") is a judgment the CVO
   has not graded yet. Signing does not presume that grade. The CVO grades `g-2`'s AC4 on the served rows at L9.

## 7. WHAT THIS HALF DOES NOT COVER

No S3 delete; no code change; no portal or deploy act; no change to `CHATTER_AXIS_SOURCE`; no as-of other than
2026-09-29 or 2026-09-30; no daily move for FDX or for any security outside the 50.
