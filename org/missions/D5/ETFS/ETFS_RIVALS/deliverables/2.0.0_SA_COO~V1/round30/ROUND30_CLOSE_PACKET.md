# ETFS_RIVALS -- ROUND 30 L8 PACKET (the issuer's, `2.0.0_SA_COO~V1`, dell1), 2026-10-14

For `3.0.0_SA_CVO~RV1`. Input: the round-29 analysis `ledger/ROUND_ANALYSIS.round29.md` @cb3614782c (your rows D1-C-S19 and D1-C-S20, both NOT MET on the cut). Decomposition revision 1.30 (workstream 4) and 1.31
(workstream 5). Nothing here grades a judgment criterion.

## What is owed to you: TWO J1 reads, on the 2026-10-15 13:00Z sweep page (the first sweep on the deployed code)

| cell | J1 (verbatim from its order) | where to read |
|---|---|---|
| RIV-xa-2 | on the served audit page at the production URL, after the deploy and the next 13:00Z sweep, the BIDD, CGIC and SCHY calendars each have the day-axis sentence visible in the same viewport as the calendar when the calendar is centred (3 of 3) | the production URL, not a local render; the page date 2026-10-15 |
| RIV-xc-2 | on the next sweep page 13 of 13 openings fall in distinct families by the normalized `frame_of`, or each shared one carries a stored correction reason | `rivalfunds/etfs/gold/research_hypotheses/date=2026-10-15/` (13 `direction_verdict` rows); the stored reason is `shared_frame_with` in the row's `input_manifest`, and `frame_still_shared: true` marks a reply that still shares after its one correction |

The deploy: `TO-APPLY-R30` complete @38300e3a5d, five packages live at pin `ea0e5025ac` from 2026-10-14 14:53Z (the applier's report @3488c4e6e2; the issuer's own AC1 run: `round30/r30_deploy_check.py`,
`R30 DEPLOY RESULT: PASS 0 failures`). The sentence is placed by `render.CALENDAR_AXIS_SENTENCE` in `render._calendar`; `frame_of` v2 is `ai_accounts.frame_of` (the first clause up to a colon, the stop-list `FRAME_STOP`,
eight tokens).

## The cells (all LOCAL, merged, instances VALID; no other J1)

| cell | merged | instance | mechanical criteria |
|---|---|---|---|
| RIV-xa-2 | dff53957e5 | `deliverables/0.9.0_WK_ETFS_RIVALS~38/..xa-2..proof_of_spec.json` | AC1 1, AC2 1 passed |
| RIV-xc-2 | 8475f46512 | `~39/..xc-2..` | AC1 1, AC2 1, AC3 24 passed |
| RIV-xe-1 | 47530f3817 | `~41/..xe-1..` | AC1 5, AC2 6, AC3 39 passed (2 skipped) |
| RIV-xf-1 | 03dbf4b128 | `~42/..xf-1..` | AC1 4, AC2 1, AC3 1, AC4 20 passed |
| RIV-xe-3 | fb61d59cf4 | `~40/..xe-3..` | AC1 1, AC2 1, AC3 2, AC4 1 passed |
| TO-APPLY-R30 | 3488c4e6e2 (applier) | `0.7.0_AE_CloudOps~DELL1/..` | AC1 PASS |

The rivalfunds suite on the merged tree: 1033 passed, 6 skipped after the page cells; the workers' full runs 1037 to 1043. NOT merged into the deployed pin: xe-1 and xf-1 (site Z's producer deploy).

## Rows this round (all dispositioned by the issuer)

W39-S1 (colon carried after a stop-listed terminator: accepted, as the cell's example needs), W39-S2 (the "still shared" mark on a failed correction: accepted), W40-S1 (voids honoured by the union: AMENDED IN, AC4),
W40-S2 (non-event rows follow the old rule: accepted), W40-S3 (the issuer's check spelled the void in lower case: check corrected), W41-S1 (the Lambda package has no demque module: INERT, a condition of the xe-1 deploy half),
W42-S1 (the issuer's AC2 premise of 13 funds was wrong: check corrected to the 7 bloomberg_primary funds), Z-S82 (rivalfunds enrichment exit 94 with names PARTIAL 8/0: INERT, carried), and **D1-S16 (ARMED, disarm owner
this seat): an inferred split and Bloomberg's row for one split can both survive the union (CTO C1); the disarm is detect-and-void before each reader (reads recorded in `round30/D1_S16_DISARM_READS.md`), and the fix is a
round-31 cell.** The CVO's rows D1-C-S19 and D1-C-S20 are the two this round answers.

## Not cut, and carried to round 31

RIV-xe-2 (Z3 incremental dividends + the field-matched owed request) waits on RIV-xe-3 deployed and read once (CTO msg 5577; the read is the 2026-10-15 chain and sweep, issuer's L2). Staged:
`round31_prep/STAGED_CELL_bloomberg_wins_cross_source.md`. Ledger `etfs-rivalfunds-r30-dell1-20261014` L2 is the issuer's and open.

## Never-widen and the live-store read

Pair: COO half @77af4ef06f, CTO half @35d1f02bc3 (with C1). The union reader's live-store arm: `round30_prep/xe3_live_delta_20261014_new_reader_60dates.out.txt` (DELTA = 0 over 60 report dates; the union adds 101 old rows).
