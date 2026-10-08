# AMGT_CORPUS round 40 -- CRPS-ap-8, the DEV drive: what was read and walked (in part)

**By:** `2.0.0_SA_COO~X`, 2026-10-08 18:55. **On:** portal DEV `1cbc56a75eee` (the round's page cells ap-2 to ap-5 landed by Andrew's word,
msg 31915; CI "Build & Validate" success 17:22Z), served locally from `C:/tmp/wk-crps-r40-4/portal`, port 5174 held in two
windows the CTO granted (msgs 31935, 31957): 17:55Z-18:10Z and 18:42Z-18:48Z. Each walk ended with DISARM REFUSED (HTTP 401)
and the server stopped. Screenshots in `tmp/ui-walk/20261008T180129Z` and `tmp/ui-walk/20261008T184323Z`, not committed (rule).

## FWD-21 -- a name without forecast years (ruling 4)

`evidence/r40_ap8_no_forecast_census_20261008.txt`, through `scoped_amgt.read_model` (the Model tab's payload): **95 of 95
read; 1 serves no forecast period: `UNVGY_US_Equity`.** Its served reason: "raw stamp 20261008T131353Z carries no
bestdata.json (pulled before C-MODEL-FORECASTS)". **That reason is wrong for this case:** the stamp is the 2026-10-08 13:00Z
fire, after C-MODEL-FORECASTS; UNVGY returned no forecast (it is one of the five names with no value for any of the four
dispersion fields in the unit-map preview). The page would tell a reader the data is old when it is today's and simply has
no forecast. Not walked on the page.

## FWD-11 -- the team's management passage beside the FILING roster (ruling 5)

**Census first** (`evidence/r40_ap8_fwd11_both_census_20261008.txt`, 95 of 95, through `read_management` and the served
dossier): roster source BLOOMBERG_FALLBACK 86, FILING 7, none 2. Team passage and filing roster: neither 45; filing only 5;
passage only 43; **BOTH 2: BABA US and SAP GY.** BA US and VLO US, which ruling 5 names, are among the "filing only" five:
the walk of 17:55Z shows each says "neither the research team's pack nor an earnings update is on file for this name"
beside a filing roster (BA 12 officers from the 10-K, VLO 5). ASML is "passage only" (the Bloomberg fallback list).

**Walk on the two names that can show it (18:42Z):**

| name | the team passage | the roster under it |
|---|---|---|
| SAP GY | drawn whole, from "SAP Research Pack 2026 06 12_v1", beginning "Management/Board: Christian Klein is the CEO..." | 6 officers from Item 6 of the 20-F filed February 26th, 2026, each "confirmed from the filing", role starts and tenure stated |
| BABA US | drawn, from "Alibaba BABA Research Pack 2026 03 09_v1", beginning **"Management/Board 80 Eddie Wu..."** | 7 officers from Item 6 of the 20-F filed May 20th, 2026, each "confirmed from the filing", role start "not stated" |

Both draw the passage and the filing roster together, labelled apart ("THE RESEARCH TEAM ON MANAGEMENT" and "7 OFFICER(S)
FROM ITEM 6..."). **Finding:** BABA's passage begins with a scorecard heading and its score ("Management/Board 80"), the same
kind of text row `Z-S89` was about on 8306 JP and 8316 JP, here glued to the front of real prose rather than standing alone.
**Not done:** the officer names were not compared one by one against the 20-F text; the page's own "confirmed from the
filing" mark is what was read.

## FWD-10, FWD-15, FWD-18 on real names (17:55Z walk)

Seen on BA, VLO and ASML at DEV: the header's dossier section and its "Where this comes from" opener (IMB was captured this
morning on the candidate); the term filter and pillar openers on ASML as captured this morning. Nothing different from the
candidate captures was seen; the term filter still has no real name with a matching headline (owed to the CTO, msg 31656).

## FWD-20 -- the rendered-rows census (ruling 2)

`checks/round40/ap8_rows_capture.py` read the /thesis payload the page reads (`read_thesis_bundle`) for all 95 names at
19:27Z and applied the PAGE's own refusal join (`figureIdentity.ts` figureId "<scope>:<mnemonic>:<fiscal_year>" against the
served check face, verdict REFUSE, as `ModelTab.tsx` rowRefusal does). `checks/round40/ap8_rows_census.py` counts it against
DEV's own row specs (`modelSheet.ts` at `1cbc56a75eee`: 13 summary rows, 4 margin-history rows, 45 V3 rows). Evidence
`evidence/r40_ap8_rows_census_20261008.txt`. The capture file itself is not committed (Andrew-direct, this folder's
`ANDREW_DIRECT_20261008_200xZ_OPEN_CALLS_RECS_APPROVED_ON_THIS_BOX.md`); it re-generates from the capture script.

**62 rows x 95 names = 5,890 cells: shown 4,719, refused 25, absent 1,146, unmapped 0.** Ruling 2's term, unmapped 0, holds.
Two rows are absent on all 95: "Fiscal year of the financial statements" (`EQY_FUND_YEAR`, which no name returns) and "Cash
flow per share (consensus estimate)" (`BEST_CPS`, a forecast line: the capture holds fiscal-year figures only and the page
fills that row's E columns from the forecasts, so this census cannot see it). The rest of the absences are per-name gaps
(dividend and valuation ratios for names with no dividend or no history). ASML's zero-dominated row reads "Minority
(non-controlling) interest (zero in all 10 years)" (seen on the candidate; ap-5).

## FWD-16 -- the 2026-09-29 comparison extended to pillars and management (ruling 6), read ~21:3xZ

`checks/round40/ap8_fwd16_census.py`, evidence `evidence/r40_ap8_fwd16_census_20261008.txt`. For each name, BEFORE is the
dossier stored on 2026-09-29 (gold never overwrites; method 4 on 95 of 95), AFTER is the object the served reader picks today
(method 7 on 95 of 95). Pillars compare on title and text (`terms` came after the base date). Grouped by today's `pack_shape`.
**95 of 95 compared, 0 without a 09-29 object.**

| slot | kept | none both dates | changed | lost |
|---|---|---|---|---|
| pillars | 46 (pdf 32, docx 10, mixed 4) | 49 | 0 | **0** |
| management | 41 | 48 | 4 | **2** |
| cases (the control) | 34 (pdf 32, mixed 2) | 61 | 0 | **0** |

- The cases column matches the 2026-10-06 case census (102 of 285 slots = 34 names x 3). The control holds.
- **The 2 lost:** 8306 JP and 8316 JP (docx). On 09-29 both held only `Management/Board 80` (19 characters). Today both are
  ABSENT with a reason. That is the `Z-S89` remediation working, not a lost passage.
- **The 4 changed, read by content:** AZN LN (11 -> 429 characters) and SHOP CN (10 -> 330) held only the heading on 09-29 and
  carry the passage now. SPOT US and ST SP keep the same opening and lose only a trailing fragment ("Supporting
  documentation:", "Asdsa"), the trim the CTO ruled in msg 31382.
- **Reading:** no PDF-only name lost a pillar, a management passage or a case it recovered on 09-29. The docx control
  recovers everything it recovered before except the two scorecard values the round meant to remove. ACCEPT ("not poorer
  for having been filed as a PDF") holds on this population.
- **Finding, the BABA class (round 41):** **2 of 45** served management passages open with a scorecard heading and its
  score: BABA US and ST SP (`Management/Board 80 ...` glued to real prose). This is the same text `Z-S89` removed when it
  stood alone. It belongs with the round-41 cell "a served passage begins and ends at a word boundary".

## NOT DONE in this drive

- FWD-21 is not walked on the page. 1 of 95 names lacks forecast years, so ruling 4 needs a walk of UNVGY's Model tab and
  its reason (the census-only route needs 0). It needs a port 5174 window.
- The term filter still has no capture on a real name with a matching headline (owed to the CTO, msg 31656).
