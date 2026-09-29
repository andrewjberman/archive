# AMGT_HARVST ROUND 20 -- DRAIN-END PACKET, `2.0.0_SA_COO~H`, 2026-09-29 ~22:5xZ

**Issuance:** `58fbe48402` (two independent chains over `ROUND_ANALYSIS.round19.md` @`a251f02116`, corrected @`b9554a89d7`;
decomp section 32). **L8-L10 route:** `3.0.0_SA_CVO~Z`. **Class:** LOCAL. Nothing served moved and nothing was
deployed. The event route stays unmounted on the CTO's HOLD ruling (msg 26760).

## 1. TWO ORDERS, TERMINAL, VALID

| order | risk | deliver | drained | instance |
|---|---|---|---|---|
| `HVST-j-1` the event route serves the stored event by its stored id (`Z-W39-S1`) | LOCAL | `d92bcc0158` | `36e8b79f0e` | VALID rc=0 |
| `HVST-j-2` the story-span census (`Z-W41-S1`), measurement only | LOCAL | `774aa8cc48` | `23347e9833` | VALID rc=0 |

- **The `j-2` drain** met the append-only channel conflict (`W47-S1` against `W48-S1`). It was resolved by row-id union
  onto HEAD: 112 rows, all unique, and 0 same-id rows differed. It finished through `safe-merge --continue` with "0
  foreign staged path(s)". That is the first live run of the fixed `--continue` path (`ccf2a27c6b`; row `Z-S43` said
  it was not yet exercised).

## 2. THE CLOSE RUN (`round20/close_run_round20.out.txt`, trunk `5f0f55c034`)

The outcomes are unserved code plus a census, so the real entry points are the function over the SERVED rows and the
census script. Both were re-run on the merged trunk.
- **Suite:** 221 passed (the harvest suite 205, net +3; the api route file 16). The unwired-route test passes unchanged.
- **`j-1` over the 8 served events:**
  - The stored id differs from the old recompute on 8 of 8.
  - The new id-keyed call returns that very row, with articles, on 8 of 8.
  - The old and new article sets are equal on 8 of 8.
- **`j-2`:** the re-run census is BYTE-IDENTICAL to the worker's output, and the baseline equals the served part on 8 of 8.

## 3. THE CENSUS, FOR THE CTO'S RULING (no verdict recorded here)

**Candidate rule:**
- The served story test (`_security_stories`) is unchanged.
- Consecutive story-days, with at most 1 empty day between them, join one story-run.
- The run is tested against the served thresholds: at least 2 tier A/B articles, at least 2 tier-A publishers.

**Delta over 8 served events:** KEPT 5, CHANGED 3, MERGED 0, GONE 0, NEW 0. All 8 ids are unique, and no article is
shared between two events of one security.

| security | served event | candidate event |
|---|---|---|
| AMZN | 09-07 only, 3 articles, led by barrons | 09-06..09-08, 5 articles, led by bbg's first report "Amazon Cargo Plane Overshoots Runway in Miami, Killing Five" |
| 992_HK | 08-13 | 08-13..08-14, 3 articles |
| HD | 08-18 | 08-17..08-20, 4 articles |

**Row `Z-W48-S1` (INERT):** the span rule alone cannot produce the 6-article AMZN burst (09-06..09-10) that `Z-W41-S1`
pictures. bbg's 09-10 NTSB piece is its own 1-article story under the served story test, because of that test's 2-day
link window between tier-A articles. Reaching the pictured burst needs the link window ruled as well.

## 4. FOR L9

- **This round carries NO judgment criterion.** Every criterion is mechanical, so nothing here tests plausibility.
- One read is offered, and it is not graded here: are the 3 CHANGED candidate events each still one story about their
  own company? The member headlines are in `0.9.0_WK_AMGT_HARVST~48/j2_ac1_output.txt`, section (d).

**Rows this round, all INERT:**
- `Z-W47-S1`: a stale path comment at `scoped_amgt.py:4101`, outside `j-1`'s paths.
- `Z-W48-S1`.
- `Z-S42`: the analysis premise, now corrected by the CTO.
- `Z-S43`: the disarm of `Z-S37`.

**Worktrees `wk-hvst-r19-46`, `wk-hvst-r20-47` and `wk-hvst-r20-48` are now DISPOSABLE** (branches kept; removal on
Andrew's go).
