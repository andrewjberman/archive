# Round 103, workstream V1 -- the per-name section census, as read by the issuer (FWD-40 (a), PRD v0.44)

**Issuer:** `2.0.0_SA_COO~R1`, 2026-10-13 ~19:4xZ. **Order:** `AMGT-bj-7` (worker `0.9.0_WK_AMGT_RESAPP~408`, merged @a1d12f5201). **Evidence files, beside this one:**
[census_v2.txt](census_v2.txt) and `census_v2.json` (the issuer's run of `round103_prep/checks/r103_section_census_v2.py`, 2026-10-13 19:29Z, 95 of 95 names, 0 read failures, the live function
`AaACnKtr..`); the worker's run of the v1 instrument is in `deliverables/0.9.0_WK_AMGT_RESAPP~408/census_sections.{txt,json}`.

This is a READING, not a grade: FWD-40 (a) is graded by `3.0.0_SA_CVO`, and a broken value counts only when a screenshot read CONFIRMS it (`AMGT-bj-11`).

## 1. What the instrument got wrong first, and the correction

The v1 instrument (the one `bj-7` ran, 7 of 7 arms) read **UNEXPLAINED 575**. Most of that was the instrument's own error, which the issuer found by reading live bodies:

| v1 reading | cause | v2 |
|---|---|---|
| `thesis.{as_of_date, drafted_sections, thesis_driver}` UNEXPLAINED on 83 names each | the route's reason is the sibling `drafting_reason`, not `<key>_reason` | REASONED |
| `peers.members` UNEXPLAINED on 6 names | the route's own top-level `reason` | REASONED |
| `coverage.reason`, `thesis.drafting_reason`, `*_reason` keys | a null `reason` key is a companion field, not a section | not a section |
| `thesis.model_cases` UNEXPLAINED on 26 names | the reason is nested inside `base` / `upside` / `downside` | 23 REASONED, 3 still read UNEXPLAINED (below) |

v2 (new file, 11 of 11 arms, so v1's recorded proof stays reproducible) reads: **FILLED / REASONED over 114 route-sections; STATE_ONLY 187 (coverage); UNEXPLAINED 3.**

## 2. The three that still read UNEXPLAINED are not gaps

`thesis.model_cases` for `BABA_US_Equity`, `BA_US_Equity` and `PBR_US_Equity` serves `status: ABSENT` and a stated reason INSIDE each case (`base.reason`: "quote currency 'USD' and
reporting currency 'CNY' differ ..."; "forward EPS (FY1 BEST_EPS) is -0.969, not positive ..."; "no adjusted P/E history ..."). The instrument looks for a reason one level up and does not look
inside; the reason exists. Read as: **0 sections empty with no stated reason in the served payloads**, with the instrument's limit named.

## 3. The finding the census did surface: the `/coverage` route

`coverage.items` and `coverage.key_forms` read STATE_ONLY on all 95 names: `coverage_status: NEVER_HELD`, `items: []`, `store_item_count: 0`, `key_forms: []` (probed forms
`ASML_NA`, `ASML_NA_Equity`, `security-81a74ed057551e58`). For `ASML_NA_Equity` the overlay's own feed reads `coverage_status: SERVED`, `item_count: 9`, `store_item_count: 584`. So two routes
of one name contradict each other. **It is not rendered:** `useCoverageSet` has no caller outside the harnesses' stubs on `origin/DEV` (c1d367231c) or on PROD (15c9754975), so the Security
Analysis page does not show it. A route-level inconsistency to be named to the CTO, not a page defect.

## 4. The population (every difference named)

| set | count |
|---|---|
| resolved names (the dossier's resolved keys) | 95 |
| `packs/` prefixes | 105 |
| resolved names whose pack sits under the EXACT key | **93** |
| resolved names whose pack sits under the slash-safe encoding (`BP-SLASH-_LN_Equity` = `BP/_LN_Equity`; `NG-SLASH-_LN_Equity` = `NG/_LN_Equity`) | 2 |
| pack prefixes that are a bare-ticker form of a resolved name (`BABA_US`, `BA_US`, `COST_US`) | 3 |
| pack prefixes with no resolved name (`6501_JP_Equity`, `6861_JP_Equity`, `CAT_US_Equity`, `CSL_AU_Equity`, `NVDA_US_Equity`, `BP`, `NG`) | 7 |

93 + 2 = 95 resolved; 93 + 2 + 3 + 7 = 105 prefixes. "The 93" of the CTO's text reads here as the resolved names with an exact-key pack; the other two are the same companies under the
slash-safe key. The five full-form prefixes with no resolved name are `execFixture`/`tabsFixture` names of the portal's harnesses (6861_JP, CAT_US, CSL_AU) and two more; none is
served by any route. Stated, not graded.

## 5. Broken-value candidates (a candidate is not a verdict)

9,607 hits in 896 patterns, every one `raw-code` (an underscore-joined identifier inside a rendered key); no placeholder word and no money format at the payload level. The patterns that
matter by reach (names on which each appears):

| pattern | names | what it is |
|---|---|---|
| `.peers.rungs[].name`, `.denominators.per_rung[].name` = `size_band`, `industry_group` | 95 | a rung's internal name; whether the Peers tab prints it or a mapped word is the walk's read |
| `.peers.members[].horizon_label` ("... (market_cap_musd, price); ...") | 89 | prose carrying a column code |
| `.thesis_driver_chart.reason` ("no thesis_driver on a served D-1 document") | 83 | a reason sentence naming a field |
| `.peers.members[].rung_name` = `size_band` | 58 | as above |
| `.drafting_reason` ("filing_identity.source is 'none' ...") | 41 | a reason sentence naming a field |
| `.peers.reason` ("derived over N candidate(s) ...") | 46 | a reason sentence; the match is `_` inside it |
| `.provenance.inputs[].reason`, `.ledger classes.news.run_reason` | 22 | a reason sentence naming a field |
| `.posture.generation.usage.stop_reason` = `end_turn` | 9 | a model API field |
| `.posture.fit.<key>.presets.*.absent[].reason` ("no value for dy_ntm") | 2 each | a reason naming a field code |

The portal's `reasonWords.ts` and `refusalPresentation.ts` exist to turn reason sentences into words; which of these reach the screen as written is exactly what `AMGT-bj-11` (ten
names, screenshots read) confirms or clears. The minor-unit census, run by the worker (`bj-7` AC3), reads `R92 MINOR-UNIT CENSUS: YES`.

## 6. What this reading does not say

- It does not say FWD-40 (a) is met: the grade is the CVO's, and it needs the screenshot read for the candidates.
- It covers six routes per name (overlay, thesis, peers, coverage, versions, ledger), not the on-demand routes (`compare`, `print`).
- A section classed FILLED is non-empty, not correct: `FWD-40`'s "correct" is read by the walk and by the CVO's reading of five names.
