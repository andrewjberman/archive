# AMGT_RESAPP round 71 -- drain-end packet (L8), `2.0.0_SA_COO~Z` to `3.0.0_SA_CVO~Z`, 2026-10-05 ~20:0xZ

Round 71 is the CTO's round-70 analysis @21e6a2dc1c, section 4, plus ANDREW-DIRECT 15:0xZ (the Lead Panel load). It ran on PRD
v0.38, ADMITTED @f87ca71f42. Issuance @46bc7b252a; decomposition s.79. **7 of 7 orders are terminal.** Deployed:
`wbIT0PHvxKIgJvgVy+u0XhLuSXFK5dUE/wypJPDcf8o=`.

## 1. Orders

| order | outcome | drain / act | mechanical result (on deployed unless named) |
|---|---|---|---|
| au-1 | FWD-34 score unit | @40dcc8b342 | c34 YES: 572 objects, 0 without `score_unit: percent` |
| au-2 | FWD-30 grader (Z-W230-S1) | @9b4e975093 | renders 3 of 3; values equal 3 of 3 (1674 compared, 0 differ); FWD-30 GRADE equal 0 of 3 on product classes |
| au-3 | FWD-4 feed url | @69c017d520 | route + producer column built; c35 NO until HARVST's next gold build (48 ft/wsj items serve `url_reason`; 552 await `url`) |
| au-4 | FWD-7 freshness | @18931420f3 | c36 YES: 95 of 95 covered names have a row |
| au-5 | the signed-in walk | @0a0ba90abc | FWD8 WRONG 0 of 95; walker disarmed |
| au-6 | Lead Panel load (Andrew) | @066bbc25d2 | c38 YES: 9 of 9 warm under 2,000 ms (worst 757 ms) |
| au-7 | the redeploy | @ba5f7871ed | GS//XHnV -> wbIT0PHv; NEVER-2 closed 4/4; AC1/AC3 YES; 13 of 13 regression cells YES |

The issuer's real run is `round71/REAL_RUN_r71_deployed_20261005.txt` (19:57Z, wbIT0PHv).

## 2. JUDGMENT criteria for L9 (yours; no seat graded them)

1. **au-2 AC2: is each FWD-30 difference correctly called PRODUCT or GRADER?** Artifact:
   `deliverables/0.9.0_WK_AMGT_RESAPP~232/FWD30_READ_ROUND71.md`, with `fwd30_r71.tsv`. The worker calls all four remaining classes
   PRODUCT, and none a grader fault:
   - export-only fiscal figures, 195-200 per name;
   - page-only 2026E-2028E figures, 20-21 per name;
   - the export's "fiscal years 2016 to 2025 only" note;
   - export-only cases, 3 per name.
   Row Z-W232-S2: my scratch estimate of 539-629 export-only figures was wrong. The repaired grader reads 195-200.
2. **au-5 AC3: the walk, per FWD (admin role; role-gated differences NOT covered).** Artifact:
   `deliverables/0.9.0_WK_AMGT_RESAPP~235/WALK_ROUND71.md`. Its captures are in `tmp/ui-walk/20261005T161750Z`, `...163146Z` and
   `...165304Z` (gitignored, on this device), and the print PDFs are in `.../~235/print/`. The worker's observations, with no
   verdict:
   - **FWD-1:** print reaches a PDF in 16-21 s; there is no segment breakdown.
   - **FWD-3:** hover shows the value, as-of date and source.
   - **FWD-6:** a "what changed" block shows two versions.
   - **FWD-10:** 0 refused model rows, so the model arm was not exercised; refusals show elsewhere.
   - **FWD-15:** a row click opens the page.
   - **FWD-17:** BA shows 12 officers, ASML 7 (fallback), and AMD absent with a reason.
   - **FWD-18:** the Risks dialog shows filing text and cites; 0 of 6 driver-chart passages show.
   - **FWD-19:** BA HOLD with reasons; there is no accept/decline control.
   - **FWD-31:** ASML passage beside the roster; BA and AMD in the absent arm; the byte-unchanged arm is read on served data
     (12 of 12, 7 of 7).
   - **FWD-5 (v0.38):** the three prints are field-code dumps (107-109 raw tokens each), not branded documents (row Z-W235-S2).
   - **FWD-8 (v0.38):** WRONG 0 of 95, mechanical.

## 3. Rows (all disarm_owner `2.0.0_SA_COO~Z`)

| row | class / standing | gist | disposition |
|---|---|---|---|
| Z-W230-S1 | ARMED -> disarmed | stale page-render grader | disarmed by au-2 |
| Z-W235-S1 | BLOCKING -> resolved | walker held at start | resolved by the 16:06Z re-seat |
| Z-W232-S1, S2 | OBSERVATION, INERT | the grader needed PageEnd as well; my 539-629 estimate wrong | recorded |
| Z-W233-S1 | OBSERVATION, INERT | 29 ft/wsj articles carry a top-level url, served null as ordered | round-72 candidate |
| Z-W233-S2 | OBSERVATION, INERT | the producer universe object (2026-09-16) holds 53 of 95 covered names | round-72 item; COO~H: the owner is build_universe.py's |
| Z-W233-S3 | OBSERVATION, INERT | the test_aj7 byte pin | fixed @a53eaf74c5 |
| Z-W235-S2..S5 | OBSERVATION, INERT | print is a field-code dump; 0 of 6 driver-chart passages; walk-engine gaps; no segment breakdown | round-72 candidates |
| Z-W236-S1 | OBSERVATION, INERT | cold-container lookups remain (cold chatter 5.3-10.0 s) | round-72 producer item |

## 4. Lead Panel (Andrew-direct), before -> after, deployed

| read | before (GS//XHnV) | after (wbIT0PHv) |
|---|---|---|
| chatter, warm | 9.2-12.3 s | 0.47-0.76 s |
| price rankings, warm | 3.9-5.2 s | 0.06-0.26 s |
| chatter, cold first read | 14.4-19.2 s | 5.3-10.0 s |

Sources: `round71/LEADPANEL_BEFORE_au7.txt`, `0.7.0_AE_CloudOps~A/LEADPANEL_AFTER_au7.txt`, and the issuer's real run.
Andrew's note went via MSTR~Z at 19:59Z.
