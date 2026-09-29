# AMGT_HARVST ROUND 16 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~11:5xZ

**Issuance:** `b8c8214ce5` (two orders over `ROUND_ANALYSIS.round15.md` @`ce26d1244b`; decomp section 28).
**L8-L10 route:** `3.0.0_SA_CVO~Z`. **Close run:** `round16/close_run_round16.py`, output `close_run_round16.out.txt`
(the deployed API, invoked; CLOSE RUN: OK).

## 1. TWO ORDERS, TERMINAL, VALID

| order | risk | drained | audit (landed = branch) | instance |
|---|---|---|---|---|
| `HVST-e-1` one text span, one count (in memory) | LOCAL | `5f25e64267` | 10 = 10 | VALID rc=0 on the trunk |
| `HVST-e-2` served rebuild, mention + daily | SERVED | `7b1027e99f` | 12 = 12 | VALID rc=0 on the trunk |

Never-widen pair for `e-2`: COO half `604165a591`, CTO half `73fce69599`. No delete, no event put, no vendor call.
**Two implementations agree:** `e-1`'s matcher and the issuer's prototype move the same 14 rows and the same 8 tiers.

## 2. WHAT IS SERVED NOW -- read by this seat from S3 and from the deployed Lambda

| table | parts | newest part | ETag | rows |
|---|---|---|---|---|
| article_security_mention | 5 | `date=2026-09-29/part-20260929T112204Z` | `b8118b05d3160c7c31b4955c22732afe` | 275 |
| chatter_daily | 6 | `date=2026-09-29/part-20260929T112222Z` | `06025a62eb771b336f33fe097d50c61c` | 51,952 |
| chatter_event | 7 (unchanged) | `date=2026-09-29/part-20260929T092439Z` | `c146a325c98963f965b8b1bd69ca3393` | 8 |

- **Inside the pair:**
  - mention: 14 rows moved over 6 securities (AMZN 8, UPS 2, DAL, FDX, GOOGL, GOOG 1 each), including 8 moves from tier C
    to D;
  - daily: 212 cells moved, over the same 6 securities;
  - 0 rows outside the pair, 0 DRIFT;
  - `e-2` AC2: served equals rebuildable on all three tables. The served event part equals `event_rows` over the new
    mention part, 8 of 8.
- **The AMZN 09-06 crash report** now reads `mention_count` **8** (was 10), still tier A, credited to `Amazon` and
  `Amazon.com Inc`.
- **Served tier distribution:** A 72, B 63, C 39, D 101.
- **The ONE REAL RUN.** The deployed `opal-amgt-scoped-api` (CodeSha256 `CtIvirv...`) returns HTTP 200 for each
  security below:
  - AMZN: 1 event (09-07, unchanged). The daily `series` for 09-07 now reads `mention_count_total` **15** (was 17),
    equal to the landed row, with articles 3, tier A 2, tier B 1, score 2.6.
  - BA and 992_HK: events unchanged.

## 3. WHAT THE ROUND DID NOT REACH -- stated plainly

- **Leftmost-first scanning:** a shorter alias that starts before an overlapping longer one would take the position.
  None of today's 14 moved rows has a half-overlap, so the case is a declared exclusion in `e-1`, unmeasured beyond
  today's silver.
- **The larger burst shape** stays UNEXERCISED (no new captures).

## 4. JUDGMENT FOR L9 (presented, not graded) -- `e-2` AC4, `e2_ac4_output.txt`

Nine rows are presented: the AMZN 09-06 crash report and the 8 rows whose tier moved C -> D. Each shows its served
`mention_count` and `match_forms` beside every matched span in the text (block, offset, the words around it).
**Does each served count equal one per actual mention of that company?**

## 5. ROWS -- the gate's own fold: 99 ids, GRADUATED 56, DISMISSED_WITH_REASON 25, UNDER_INVESTIGATION 18 (28 files)

- **New, INERT:**
  - `Z-W42-S1`: the `e-2` act ran when the worker meant a dry run, and its stdout was cut at 60 lines by `head`. The act
    was the sanctioned one, at the as-of both halves allow. Its own pre-put checks passed, and the post-act re-read
    (`ac1_post_act_verify.py`) shows it inside the pair; this seat's S3 read agrees (section 2). It is a care defect,
    not a radius defect.
  - `Z-W42-S2`: AC1 is write-once, so a verifier re-running it now reads its STOP branch; grade with
    `ac1_post_act_verify.py`.
- **`Z-W41-S2` (the double count) is REMEDIED by this round,** and the served count is one per span. The remediation
  record is the CVO's.
- **Carried:**
  - ARMED `Z-S37` (the tool's authoring lane) and `Z-W39-S1` (disarmed by condition).
  - ARMED `Z-W40-S1`, disarmed by specification in round 14. It is not in any analysis's list since.
  - ARMED `Z-W41-S1`, disarmed by acceptance in round 15.
  - `Z-W37-S4` (the account holder).
- **Armed rows with an owner this seat could not seat: NONE.**

## 6. FOR THE ROUND-17 CUT (the CTO decides)

1. `Z-W40-S1` (cross-story name detection) is still open from round 14.
2. Held-out reads and the larger burst shape both wait on new captures; the Seeking Alpha 402 is the account holder's.
3. Unchanged: the portal push (Andrew's hold).

## 7. RETAINED, NOT REMOVED

- The worktrees `wk-hvst-r15-41` and `wk-hvst-r16-42` hold untracked worker scratch. Removing them is a recursive delete,
  left for the account holder's word, as with `wk-hvst-r12-37`.
- Branches `wk-AMGT_HARVST-41` and `-42` are fully merged.

## 8. WHAT THIS PACKET DOES NOT DO

It grades no judgment, claims no FWD REALIZED, pushes nothing, and cuts no round-17 cell.
