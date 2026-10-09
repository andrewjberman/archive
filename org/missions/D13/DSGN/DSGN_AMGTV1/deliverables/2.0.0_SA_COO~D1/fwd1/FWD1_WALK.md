# DSGN_AMGTV1 FWD-1 -- the seat walk (2.0.0_SA_COO~D1, dell1, 2026-10-09 ~14:1xZ)

**Ruling:** `org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_FOLD_UNBLOCK_DSGN_1152_FWD1_IS_SEAT_PROVABLE_20261009.md` @a544e646ea
(UB-20261009T132805Z-1152, SIGNED). FWD-1 is graded on a seat walk: `/ui-walk` on the local dev build at `2726bbe7`, signed in as the
walker service account against the real backend and real data, through ACCEPT's steps to Valero's Recommendation card open. The
`2726bbe7` SA tree is byte-equal to PROD `18364342` (portal-v2.1.210), so the walk reads the code PROD serves; the build host is the one
difference. `3.0.0_SA_CVO` grades it at L9.

**FWD-1 text** (`prd/DSGN_AMGTV1_PRD.md:80-93`):
- DONE WHEN: "EXERCISED -- one live walk, signed in with a real account, on real data, ending in Valero's Recommendation card open".
- ACCEPT: "The PM picks Valero out of the list by its company name, reads its header's key figures (v0.15: the SAUX-03 row), opens the
  Thesis and reads it as three cards under the main chart, then opens the Recommendation and can say whose view it is and which document
  each citation comes from. Any step fed by sample data instead of the real thing fails the outcome."

## The walk -- `tmp/ui-walk/20261009T140741Z` (dell1), 14:07Z-14:09Z

`node .claude/skills/ui-walk/walk.mjs --base http://localhost:5174 --route /security-analysis --thread "Valero Energy Corp"`, a
`dev:live` build of portal `2726bbe7` with no scratch edit (`git status` clean). The walk had 0 API issues and 0 guard aborts. The walker
disarmed, and its login is refused (401).

| ACCEPT step | shot | what it shows |
|---|---|---|
| Picks Valero out of the list by its company name | 004 `thread-1-list` | The Trending x Price list, "Change over the last 30 days to October 8th, 2026", ranked from Bloomberg prices (94 names). "Valero Energy Corp +15.9%" is among the Gainers, and the walker picks the row by that name. |
| Reads its header's key figures (SAUX-03) | 005 `thread-2-header-cards` | "Valero Energy Corp", VLO US, Energy -- US. Price USD 443.80, Market cap USD 128B, Enterprise value USD 135B, Net debt USD 5.93B, Beta 0.71, Average volume 3.46M, Short interest 3.4%. "October 9th, 2026, 9:11a ET, Source: Bloomberg". Breakout #5, +12.00% over 30 days. |
| Opens the Thesis and reads it as three cards under the main chart | 005 / 006 `thread-4-thesis-cards` | THESIS, "the 10-K filed February 25th, 2026", has the three cards Investment thesis, Risks and Recommendation. Above them, in the main chart's place, the thesis-driver panel says the series "is not in the model data yet. No chart is drawn until its numbers are there". |
| Opens the Recommendation: whose view, and which document each citation comes from | 007 `thread-5-recommendation-window` | "Recommendation -- Whose view this is, and what each line rests on". It reads "The research team's Base case is not in this pack" and "This is a machine's draft from the company's filing, not the research team's recommendation". Each line cites its passage and document: "VLO US's 10-K, filed February 25th, 2026 -- Item 7. Management's discussion and analysis > Paragraph 72" (and 74, 75). |
| No step fed by sample data | all | Every figure and passage is served: Bloomberg prices, the 10-K. No sample-content finding was recorded. |

## For the grader

- **The main chart:** the three cards sit under the thesis-driver panel. That panel states that the driver's series is absent and draws
  no chart ("none is worked out from the drafted text"). Whether that satisfies "under the main chart" is the CVO's judgment.
- **Latency:** the header's figures arrived 18.6 s after the pick (a 3.0 s settle plus `waitForLoaded` 15.6 s, `load-states.json`). An
  earlier walk at 14:04Z shot the header still as a skeleton at about 6 s. This is a finding, not a pass or fail of FWD-1's text.
- **Instrument repairs, made to run this walk** (`.claude/skills/ui-walk/walk.mjs` `walkThread`, issuer direct act):
  - it matches the price-bar element when the row is not an `<li>` (the redesigned list), as `readPriceBars` already does;
  - it waits for the price bars before matching;
  - it waits for the loaded state before the header shot.

  The earlier thread walks (`...T135850Z`, `...T140158Z`, `...T140358Z`) failed or shot skeletons for these reasons, and are superseded.
