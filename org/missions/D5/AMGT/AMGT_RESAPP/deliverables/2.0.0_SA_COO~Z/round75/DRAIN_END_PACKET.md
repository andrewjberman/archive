# AMGT_RESAPP round 75 -- drain-end packet (L8), `2.0.0_SA_COO~Z` to `3.0.0_SA_CVO~Z`, 2026-10-06 ~12:5xZ

Round 75 implements the CTO's round-74 analysis @0967e3d9c5, section 4, with ADDENDUM 1 @82afef1fd8 (ruling 3's writer). It ran on
PRD v0.40, ADMITTED. The issuance is @cecef87d4a and the decomposition is s.83. **6 of 6 orders are terminal.** The function was
redeployed from `0MZWPl7n` to `D29LJCXhOStZ51JD4TTt2Jk0QUVDUbXDouXRTUS1ULI=` (11:28:32Z). Also live: the snapshot grant, the schedule
`amgt-global-freshness-snapshot-daily` (cron 30 12 ? * MON-FRI *), and the first snapshot (11:32:38Z, 302 rows).

## 1. Orders

| order | outcome | drain / act | mechanical result (deployed D29LJCXh unless named) |
|---|---|---|---|
| ay-1 | FWD-5: each figure dated by its own period; the served thesis printed (rulings 1-2) | @f5639411fb | c57 YES: fiscal-year lines with the run date 368/491/396 -> 0; the run date once, on page 1. c58 YES: BA 17 of 17 sentences. Stored figures carry no quote date, so market lines say so in words (row Z-W257-S1). |
| ay-2 | FWD-7: /freshness as one snapshot (ruling 3, ADDENDUM 1) | @ab28d0ba01 (three seats) | c59 YES: served from the snapshot, 302 of 302 rows equal; cold 825-980 ms, post-hold 797 ms (from a 7.5 s miss). Served only within 24 h. The ruled write point did not exist (row Z-W258-S1, ARMED, disarmed by Z-S358 and the scheduled writer). |
| ay-3 | the names-phase cut (ruling 5) | @42fd324fb3 | c60 local YES: the names read runs beside the gold reads (it logs 0 by overlap, row Z-W259-S1); first chatter request locally 4.2-4.5 -> 3.5-4.0 s; bodies EQUAL 3 of 3. |
| ay-4 | segment headings and table labels (ruling 6) | @5c9d2edd3c | c61 YES: bad headings 36 -> 0 over 95 names; BA 10 -> 3 segment names; 3 of 3 table passages labelled. |
| ay-5 | redeploy + grant + schedule + first fire | close @1dbe5f78f9 | Built at EXACTLY ab28d0ba01. Grant on the one key; a sibling key reads implicitDeny. Proof VALID @970d3861c7; NEVER-2 closed. STOP 30010 (row Z-S359) was the issuer's c59 check comparing across environments; re-cut @bf909b6665. |
| ay-6 | the walk | @539b33f1bf | 3 PDFs; walker disarmed; DISARMED relayed to MSTR~Z. |

The issuer's real run is `round75/REAL_RUN_r75_deployed_20261006.txt`: **16 of 16 YES**. That is r75 c57/c58/c59/c61; r74
c53/c55/c56 (c55 the slash-key pin); r73 c48/c49/c50; r72 c39/c42/c43/c45; r71 c38 and c35 (657 of 657 feed items with a url).

## 2. JUDGMENT for L9 (yours)

**ay-6 AC3: the walk, per FWD.** Artifact: `deliverables/0.9.0_WK_AMGT_RESAPP~261/WALK_ROUND75.md` and `print/` (3 PDFs). The walk
used a dev build of portal `6de76f0509` (the /freshness page) with DSGN 43+44 (`1d6d2573`) merged UNCOMMITTED, for the walk only.
**Neither is on DEV (`cf3f10c6`).** The worker's observations, with no verdict:
- **FWD-5 (`:521-525`):** BA 22 pp, AMD 24 pp, ASML_NA 24 pp. Lato only, navy ink, no images. "Printed 2026-10-06" appears once.
  - Dates: fiscal-year 2016-2025 lines carry no date; FY2026-28 consensus lines read "period ending <date>"; market header lines read
    "date not stored with this figure".
  - Thesis: BA prints filing sentences for its thesis, risks and recommendation. AMD prints "not written" for all three. ASML_NA's
    recommendation is one governance-code sentence (row Z-W261-S2).
- **FWD-7 (`:539-542`):** a first visit paints the first row at **2,043 ms** (the read 694 ms; the second visit 1,579 ms; r74 9,135
  ms). 95 of 95 flagged stale and every Last refreshed reads 2026-10-04, so no stale name can be singled out. CTO ruling 4: the flags
  are real (SA unread).
- **FWD-18 and FWD-1 on BA (local merge, not DEV):** the driver chart serves 3 points; the first opens its passage with its cite.
  Segments: 11 rows under 3 labels, the label repeated per row rather than shown once as a heading.

## 3. Rows (disarm_owner `2.0.0_SA_COO~Z`)

| row | standing | gist | disposition |
|---|---|---|---|
| Z-W258-S1 | ARMED -> disarmed | the ruled snapshot write point did not exist | 24 h maximum age (AMENDMENT 1) + the CTO's scheduled writer (ADDENDUM 1); recorded as Z-S358 |
| Z-S359 | ruled | c59's deployed arm compared across environments on `rot` | the check's fault; re-cut @bf909b6665; the deployed value is correct |
| Z-W258-S2, Z-W259-S2, Z-W260-S3 | fixed | the mount test broke on round 74's greedy route (19 vs 18) | fixed in ay-2 AMENDMENT 1 (non-greedy equal, at most one greedy); api 703 passed |
| Z-W257-S1 | INERT | stored figures carry no quote date | market lines say so in words; a producer item if a quote date is wanted |
| Z-W257-S2, Z-W259-S1, Z-W260-S1, Z-W260-S2 | INERT | a test-order flake; names overlap; the table filing read; uneven table rows | recorded; S2 (uneven rows) for your read |
| Z-W261-S1, Z-W261-S2 | INERT | the PDF bytes came from the page's print GET; print content notes | for your read |

## 4. Cold start

- The cold chatter read is still above about 2 s, so provisioned concurrency stays on Andrew's list. AE~A's phase table is in the ay-5
  instance @970d3861c7. Locally the first chatter request fell 4.2-4.5 -> 3.5-4.0 s.
- **c59 C2 needs an idle window** to observe a cold invoke. Run right after other invokes, it read "cold invokes 0" (a vacuous FAIL);
  after 11 minutes idle it read 1,087 ms.

## 5. For Andrew (cited, no new spend taken)

- **The portal DEV push** of DSGN rounds 43+44 (`1d6d2573`) and RESAPP's /freshness page (`6de76f0509`), after the CTO's review from a
  render. The two merge clean together and onto DEV `cf3f10c6`. The page's precondition, ruling 3, is now met: a first visit in 2.0 s.
- **Provisioned concurrency,** only if the cold read stays above about 2 s.
- Carried: the Bloomberg Terminal sign-in; Z-W240-S1; Z-W227-S1; FWD-2; FWD-14's list owners; the walker accounts.
