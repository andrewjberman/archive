# DSGN_AMGTV1 -- ROUND 34 CLOSE (issuer `2.0.0_SA_COO~D`, 2026-10-04 ~02:1xZ) -- THE GAP WALK + THE REPAIR CELL

**Input:** decomposition v34 and the issuance are @c14db45cb0, over PRD v0.15 @237d5d742f (ADMITTED). The rectangle is the CTO's
round-33 analysis, section 3 (@ff31355b93). The base is portal PROD dbd29c6320.

## 1. THE GAP WALK ON THE SERVED BUILD (the issuer's real run; walker ARM/DISARMED notices to MSTR~Z; login REFUSED after each disarm)

| run | build | reads | result |
|---|---|---|---|
| `walk/read-20261004T001928Z` (00:19-00:30Z) | PROD dbd29c6320 | 20 | 16 PASS, 3 FAIL (display names: the Peers subject), 1 ERROR (the FWD-24 control) |
| `walk/read-20261004T012802Z` (01:28-01:34Z) | PROD dbd29c6320, MSFT US | 14 | **FWD-24 control PASS**: MSFT US lacks breakout_price, which renders its designed empty state, no number |
| `sixstate/out-20261004T010236Z` (ui-contract-check.mjs --dist, --states-sweep) | PROD dbd29c6320 | 77 cells | 62 PASS, 14 FAIL, 0 NOT_EXERCISED |

What the PROD reads give the CTO's 13 NOT_EVALUATED (detail: `walk/GAP_READ.md`):
- every tab on BA, VLO and AMD with the day dialog closed (5 of 5 each);
- the non-USD header (ROG SW, CHF);
- the no-officer filing (ASML NA: 7 officers from the Bloomberg fallback, source named);
- the overlay census (0 "not served" on 19 carried fields, ×3) and its control (MSFT US);
- hovers: FWD-2 identity, FWD-21 full names and "no clear tone", the FWD-5 timeline tooltip;
- Escape closing the account menu;
- **FWD-19:** `run.fwd19_designedStates` PASS on 6 panels; fourStates PASS (loading 6, error 6, empty 7, no-permission 1); harnesses
  drafting 8/8, tabs 20/20, posture 32/32.

**FWD-20's instrument is stale against the redesign.** Its 14 FAILs are its own anchors, not the page:
- `darkContainers` and `bandIsIdentityHeader` expect a navy identity band on all six states; the light-family redesign removed it
  (12 FAILs);
- `faces.price` expects every served row visible, but the page shows the top 10 per side by design (round 29);
- `faces.chatter` reads the round-16 monthly fixture, so 0 bubbles draw on the windowed face (round 31).
The instrument is re-anchored in round 35, below.

## 2. THE REPAIR CELL (1 of 1 terminal, drained)

| order | cell | worker | portal | AC1 / AC2 / AC3 | outer drain |
|---|---|---|---|---|---|
| `AV-zl-1` | FWD-21 labels; FWD-27: move window, change precision, axis ink, the Peers subject name | ~93 | 934d86d940 | labels34 4/4; repairs34 4/4 + peername34 4/4; battery29 0 skipped | cecc655e65 |

The proof instance is VALID (worktree checker). Six blobs, all LF, with no 0x08 and no non-ASCII. The issuer re-ran each check and read
4/4. No rows were filed.

## 3. THE CANDIDATE -- portal `055ba370` (worktree 92, branch `dsgn-r34-onto-dev`, LOCAL)

The candidate is PROD dbd29c6320 plus ~93, merged with remote DEV a403f466 (0 SecurityAnalysis files on the DEV side). Issuer run:
- `battery29.sh` with no skip: ALL PASS (14/14 harnesses, tsc 0, eslint 0).
- round 34: labels34 4/4, repairs34 4/4, peername34 4/4. round 32 words32 4/4. round 31: presets 4/4, windowread 4/4, feedrest 4/4.
- round 30: universe, resolutionwords, chrome and served all at full marks. round 29: all 12 at full marks.
- round 27: identity 3/3. round 28: fixture and render 3/3.

**Close walk** `walk/read-20261004T014957Z` (5174 = 055ba370; 01:49-02:00Z; DISARMED 02:00:29Z; login after: REFUSED): 20 reads,
**19 PASS, 0 FAIL, 1 ERROR**. The ERROR is the FWD-24 control again, because BA, VLO and AMD carry every checked field; the MSFT US
run supplies that control. **Display names: 1 per security on every surface** ("The Boeing Co" ×10).
L9 read of the PNGs:
- the 90D collage has no label over a mark, and shortened labels end "..." with the full name on hover;
- the header reads "Breakout (price) #62 | -3.78% over the last 30 days, up 10 places";
- the timeline axis ticks are navy;
- What changed prints each change at its row's precision (-0.01, +1.44, -USD 3B, +1.42M).

**Seen at that read, not in this cell's scope (round 35):**
- What changed on BA, on today's served compare: **33 of 37 changed rows read "a line this page has no name for yet"** (the
  `UNNAMED_CHANGED_LINE` fallback). Rows whose before and after both print 0.0% show "-100.0%".
- FWD-24's designed empty state for a missing sector/country reads "sector/country not carried on this payload". "payload" is
  system wording (FWD-27).

## 4. OPEN -> ROUND 35 (enrichment list)

1. **FWD-20 instrument re-anchor:** the light-family band clauses, the price face's top-10 rest state, and the windowed chatter fixture.
2. **What changed reads in words:** name the changed lines from the served names; no percent move printed against two equal rounded
   values.
3. **Wording:** the "not carried on this payload" empty states.
4. **After RESAPP ap-4 serves FWD-39:** the FWD-5 word cloud.
**Elsewhere:**
- the CTO's product-file review of 055ba370;
- its DEV push on Andrew's word (card at MSTR~Z);
- the 84 of 95 names with no M-1 management object (RESAPP upstream, observation);
- SAUX-25's provenance lines (RESAPP FWD-38(d), COO~Z).

## 5. CTO REVIEW CONDITION 1 (review @720f78e6f6, msg 29124): BUBBLES MINUS LABELS, PER WINDOW, ON THE SERVED WALK

The CTO's point: labels34 counts collisions and never compares labels to bubbles, so a collage that dropped every hard label would
still read 0 collisions. Measured on the candidate's close walk `walk/read-20261004T014957Z` (055ba370, live data). The bubbles are
the face's own count line, "<k> of 95 covered names have collected articles in this window", which counts the bubbles drawn. The
labels are the distinct label keys in `0{2,4,5}-fwd21-labels-<w>.json`:

| window | bubbles | labels (distinct keys) | bubbles minus labels |
|---|---|---|---|
| 30D | 57 | 57 | **0** |
| 90D | 67 | 67 | **0** |
| 365D | 70 | 70 | **0** |

No label is dropped at any window, so condition 1 is met. Condition 2, the DEV push on Andrew's word, is carded at MSTR~Z.

