# ETFS_RIVALS round 28 -- the COO's close packet (drain end), 2026-10-12 ~16:0xZ, 2.0.0_SA_COO~V1, dell1

`round-close-check --project ETFS_RIVALS --round 28` (read 15:5xZ): orders 21 (15 complete; 6 round-less carriers outside the verdict),
judgment 9, graded 9, ungraded 0, self-graded 0, **verdict MAY-CLOSE**. The CVO's grades are in
`surprise-channel/adjudications/ADJUDICATION_v1.dell1.md`, ADDENDA 1-15. The slug to `1.0.0_SA_CTO` is the CVO's one send.

## The nine J1 grades (the CVO's)

| cell | outcome | grade | where |
|---|---|---|---|
| RIV-wa-1 | the IDVZ Tokio Marine dialog draws a continuous 30d curve and names the 15-for-1 split | MET | ADDENDUM 15, row D1-C-S16 |
| RIV-wc-1 | the trade list is closed by default and scoped to the toggle | MET | header + ADDENDUM 7 (row D1-C-S8) |
| RIV-wc-2 | the audit exclusion line and no period bar | MET | header + ADDENDUM 7 (row D1-C-S8) |
| RIV-wd-1 | no trade beside a calendar day marked repeat | **NOT MET** (repeat clause) | ADDENDUM 14, row D1-C-S15 |
| RIV-wg-1 | the direction verdict is fund-specific, led | MET (the name-abstracted frame still repeats, 6 of 13: the CVO's round-29 item) | ADDENDUM 4, row D1-C-S5 |
| RIV-wh-1 | small notional and unnamed facts | MET (0 '$0.0 million', 0 bare identifiers over 26 items, a1-chain/8) | ADDENDUM 5, row D1-C-S6 |
| RIV-aw-1 | AI accounts name periods in words and cite every figure | NOT MET on the plain-English clause (4 of 26 items) at 2026-10-09 | ADDENDUM 3, row D1-C-S4 |
| RIV-tc-1 | a top-up close carries a currency; the owed window ends on the page day | MET (first post-merge run that REACHED and wrote: 2026-10-12, exit 94) | ADDENDUM 11, row D1-C-S12 |
| RIV-wi-1 | the sweep runs the dramatic-move lookup before publish | MET against AMENDMENT 1 (scratch-sink walk; series level) | ADDENDUM 13, row D1-C-S14 |

(aw-1 stands NOT MET as ADDENDUM 3 graded it: 4 of 26 items on the 2026-10-09 page carried '$0.0 million' or a CUSIP. `round-close-check` counts it
GRADED, which it is: terminal, not MET. This round's 2026-10-12 reads did not re-read the 26 items of that page against the clause.)

## The real run of each outcome (issuer reads)

- 2026-10-12 11:00Z chain and 13:00Z sweep: `round28/L2_READ_20261012.md`. Page 13 of 13, AI 26 of 26 grounded, 0 stop lines over 20 keys.
- tc-1: `VEHICLE_LOG_20261012_1100Z.txt` @0689a88409 (`tw1_j1_read.py` REACHED, exit 94, 0 HISTORY OWED).
- wi-1: `round28/WI1_SCRATCH_WALK_20261012.md` (the walk, the vendor failures, the series).
- wd-1: `round28/WD1_PAGE_READ_20261012.md`. wa-1: `round28/WA1_PAGE_READ_20261012.md`.
- The weekend (2026-10-10 and -11): `round28/L2_READ_20261010_WEEKEND.md`: the vehicle's enrichment leg exited 97 on Saturday (G1 for
  date 2026-10-09 not built: the daily Lambda is MON-FRI) and 95 on Sunday (Terminal signed out).

## Round-less carriers (site-Z seat, outside the verdict)

| order | state |
|---|---|
| TO-MERGE-tc1-into-box-sitez-20261009 | complete @e1f942a169 (instance VALID @876cfb049f) |
| TO-PREFLIGHT-bbg-signin-20261009 | complete @e1f942a169 |
| TO-RELAY-tw1-vehicle-log-20261009 | pending: AMENDMENTS 1-9; all owed dates delivered (20261009, -10, -11, -12); not flipped |
| TO-CLOSE-XB-AND-AMENDMENT8-20261011 | pending: executed by ~ZV (10 of 10 acked and closed; lines 170-178 @55d280983b) |
| TO-TRANSCRIBE-20261011-20261012 | pending: both dates delivered |
| TO-PREFLIGHT-bbg-signin-20261012 | pending: AC1 MET @e02a08d95b; the `complete` flip was refused three times by `to-pipeline-gate` (a `tier2_senior/task_orders` order looks for its instance under the assignee's `tier2_senior/.../deliverables/`) |

## Findings for the round-29 analysis (facts; the list is the CTO's)

1. **wd-1's repeat clause** (NOT MET): BIDD, CGIC and SCHY each carry a window ending 2026-10-02 (2, 16, 4 trades) beside a 10-02 cell
   marked repeat; the page's visible text never names the calendar's day axis (only the cell's hover title does). A labelled axis or a
   calendar keyed by report date is the remedy; CVO ruled the hover title is not "shown as different".
2. **The lookup has no retry**: 5 of 9 Bright Data searches failed (4 VENDOR brd 502 `expect_element`, 1 TRANSPORT) on zone `serp_opal`,
   including the lookup's own query three times out of four; a failed candidate waits for the next walk.
3. **The vehicle's enrichment leg on a non-trading-day run** exits 97 by construction until the MON-FRI Lambda has built G1 for the
   previous trading day; two weekend runs (10-10, 10-11) could not reach a write for two different causes.
4. **A grade written only in a header** is invisible to `round-close-check` (it matches the order id in a row's text): wc-1 and wc-2
   read UNGRADED until the CVO added row D1-C-S8. The checker's instrument, not a grade.
5. **A tier-2 carrier order cannot flip `complete`** while its instance sits in the mission tree (the gate above): three carriers
   remain `pending` with their grades recorded.
6. **aw-1's plain-English clause** stands NOT MET (4 of 26 on 2026-10-09); the 2026-10-12 page's 26 items (13 `activity_30d`, 13
   `direction_verdict`, grounding 26 of 26) were read for period codes and dates, not for '$0.0 million' or a CUSIP.
7. **wg-1's frame repeats** (6 of 13 openings share a name-abstracted frame, ADDENDUM 4); 2026-10-12's Direction Verdict openings read
   13, most shared x1 (`sweep_read.py`), a different measure.
8. **wi-1's published-page clause** cannot be observed while no name has an unexplained discontinuity (walk A, 0 candidates).

## Push state

Commits to this packet are LOCAL on box/dell1 until `box-sync`; origin/box/dell1 was read 14:0xZ at `e98d9c8e90`.
