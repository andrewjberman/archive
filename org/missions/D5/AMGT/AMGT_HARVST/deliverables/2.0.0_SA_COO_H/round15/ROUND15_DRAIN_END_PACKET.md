# AMGT_HARVST ROUND 15 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~09:5xZ

**Issuance:** `e7e184d8ac` (two orders over `ROUND_ANALYSIS.round14.md` @`f00c9a0c43`; decomp section 27).
**L8-L10 route:** `3.0.0_SA_CVO~Z`. **Close run:** `round15/close_run_round15.py`, output `close_run_round15.out.txt`
(the deployed API, invoked; CLOSE RUN: OK).

## 1. TWO ORDERS, TERMINAL, VALID

| order | risk | drained | audit (landed = branch) | instance |
|---|---|---|---|---|
| `HVST-d-1` common-name aliases, in memory | LOCAL | `ed1afe47bd` | 12 = 12 | VALID rc=0 on the trunk |
| `HVST-d-2` served rebuild, three tables | SERVED | `3cfbfb5147` | 11 = 11 | VALID rc=0 on the trunk |

Never-widen pair for `d-2`: COO half `ba195dc1c6`, CTO half `939395dd8d`. The CTO ruled `chatter_daily` into the radius
(msg 26512). No delete, no vendor call.

## 2. WHAT IS SERVED NOW -- read by this seat from S3 and from the deployed Lambda

| table | parts | newest part | ETag | rows |
|---|---|---|---|---|
| article_security_mention | 4 | `date=2026-09-29/part-20260929T092419Z` | `4a5e91d38405f09d3052343f69a68151` | 275 (was 263) |
| chatter_daily | 5 | `date=2026-09-29/part-20260929T092435Z` | `561a3bd6513eccacd68dab502a5a3a93` | 51,952 (was 50,997) |
| chatter_event | 7 | `date=2026-09-29/part-20260929T092439Z` | `c146a325c98963f965b8b1bd69ca3393` | 8 (was 7) |

- **Inside the pair:** the worker's AC1 (d) printed 0 rows outside it. AC2 found served equal to the in-memory rebuild row
  by row on all three tables: 275, 51,952 and 8 rows.
- **The ONE REAL RUN.** The deployed `opal-amgt-scoped-api` (CodeSha256 `0SpJvook...`, the RESAPP `vv-4` redeploy)
  returns HTTP 200 for each security below, and every served span and lead equals the newest landed rows:
  - `AMZN_US_Equity`: 1 event, **2026-09-07, lead "Scene of Fatal Amazon Plane Crash in Miami Is Devastating"** (barrons),
    3 articles, 2 tier A, 3 publishers.
  - The daily `series` for AMZN on 09-07 reads articles 3, tier A 2, tier B 1, mentions 17, score 2.6, equal to the
    landed chatter_daily row. The series has 272 days, through 2026-09-29.
  - Controls: `BA_US_Equity` 1 event (09-08, unchanged); `992_HK_Equity` 3 events (unchanged).
- **The 7 served events are KEPT** (same id, span, lead and members).

## 3. WHAT THE ROUND DID NOT REACH -- stated plainly

- **The AMZN event is narrower than the ruling pictured** (row `Z-W41-S1`): 3 of the 6 crash-pattern articles, on one
  day. bbg's 09-06 first report falls outside the span (only 1 tier-A publisher that day), and bbg's 09-10 NTSB piece is a
  separate story. **So the >= 5-article multi-day shape stays UNEXERCISED** (ruling 3 of the round-14 analysis).
- **The event is the first one outside the tuning set** (AMZN was never tuned on). That makes it the first HELD-OUT
  event, but a sample of ONE. It is graded at L9 below; it is not a precision rate.

## 4. JUDGMENT FOR L9 (presented, not graded) -- `d-2` AC4, `d2_ac4_output.txt`

1. **All 12 new mention matches:**
   - 11 AMZN (alias "Amazon"): 2 are crash articles; 9 are retail, market and economy pieces -- Costco x2, Walmart, Home
     Depot, Sam's Club, digital store labels, a brands essay, an NIL piece, and a market-risk column.
   - 1 TSM (alias "Taiwan Semiconductor Manufacturing").
   - **Is each a real mention of that company, or a false hit on a common word?** (e.g. the river or the rainforest)
2. **The new AMZN 09-07 event,** with all three headlines. **Is it ONE story about its own company, and does its lead name
   that story?**

## 5. ROWS -- the gate's own fold: 97 ids, GRADUATED 56, DISMISSED_WITH_REASON 25, UNDER_INVESTIGATION 16 (27 files)

**New:** `Z-W41-S1` (ARMED, on this seat), `Z-W41-S2` (ARMED, on this seat), `Z-W41-S3` (INERT).
**Disarmed by this seat, same turn:**
- **`Z-W41-S1` -- DISARMED BY ACCEPTANCE UNDER THE PAIR.** The narrow event is what the rule as written produces. Both
  halves named it before the put (COO half s.4.3; the CTO's own rebuild reproduced it), and it is what is served. The
  wider burst is a question for the rule's burst span, not a defect of this act. It is carried to the CTO in section 6
  and never re-read as a pass for the larger shape.
- **`Z-W41-S2` -- DISARMED BY SPECIFICATION.** The co-mention gain on 27 rows of 14 securities and the `mention_count`
  inflation were both named in the pair before the put, and neither moves a tier or an event. The inflation comes from
  the matcher summing each alias independently (the worker's measurement, row S2), so a nested alias ("Amazon" inside
  "Amazon.com") counts the same text twice. The same shape may already exist wherever suffix forms nest (e.g. BA's
  "Boeing Co" / "Boeing"); that is NOT measured this round. It moves `mention_score` in the daily series users see.
  The remedy (count distinct matched spans, not a sum over aliases) is a round-16 candidate for the CTO. Until it lands,
  any cell that reads `mention_count` or `mention_score` as a magnitude reads this row first.

**`W41-S3` (INERT):** the halves' 161 and 215 daily cells include the 5 extension days of each security; the served
rows moved exactly as the halves name. Carried: `Z-S37` (the tool's authoring lane), `Z-W37-S4` (the account holder),
`Z-W39-S1` (disarmed by condition). **Armed rows with an owner this seat could not seat: NONE.**

## 6. FOR THE ROUND-16 CUT (the CTO decides)

1. **`Z-W41-S2`'s fix:** count distinct matched spans per article, so nested aliases do not double-count; rebuild under
   a pair.
2. **`Z-W40-S1`'s fix** (cross-story name detection), still open from round 14.
3. **The larger burst shape** stays UNEXERCISED. The AMZN crash coverage is the nearest real case (6 articles,
   09-06..09-10, 3 publishers). Whether the rule's day-merge should hold a story across a day with one tier-A publisher
   is the question it poses.
4. **Unchanged:** the portal push (Andrew's hold) and the Seeking Alpha 402 (the account holder).

## 7. RETAINED, NOT REMOVED

- The worktree `wk-hvst-r15-41` holds 16 untracked worker scratch files (run copies and helper scripts; the committed
  outputs cover the deliverables). Removing it is a recursive delete, left for the account holder's word, as with
  `wk-hvst-r12-37`.
- Branch `wk-AMGT_HARVST-41` is fully merged.

## 8. WHAT THIS PACKET DOES NOT DO

It grades no judgment, claims no FWD REALIZED, pushes nothing, and cuts no round-16 cell.
