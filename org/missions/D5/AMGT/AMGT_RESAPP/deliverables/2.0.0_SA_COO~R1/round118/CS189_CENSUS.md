# AMGT_RESAPP round 118 -- `AMGT-by-3`: the C-S189 census across every covered name (the issuer, `2.0.0_SA_COO~R1`, 2026-10-18 ~09:5xZ)

**The CTO's grade (round-117 analysis, item 3):** every covered name with a served recommendation prints it in the pack's Summary, with the denominator printed; each name that does not is listed with its cause.

**Instrument:** `round118_prep/checks/r118_cs189_census.py` (read-only: an S3 listing of `s3://opal-data-harvest/derived/model_block/` and, per name, a Lambda invoke of `GET /thesis` and of `GET /print?format=pdf` on `opal-amgt-scoped-api`, the LIVE function at CodeSha256 `Rycs0LVaL8jbdI1bL1+M5o+KSy+HOGehQucN2ysFstE=`). Raw output on this box: `C:/dev/ui-walk-evidence/r118-cs189-census.txt` and `.json` (the name list below is research coverage, not account data).

**Denominator: 102 folders, 101 distinct names.** The folder `BP` is the slash-encoded form of `BP LN Equity` (addressed as `BP-SLASH-_LN_Equity`: the first run read the folder name `BP`, got a 404 and counted it as an ERROR; read under the right key it is PRINTED, below), and the folders `NG` and `NG-SLASH-_LN_Equity` both address `NG LN Equity` (both read ABSENT: one name).

| result | distinct names | note |
|---|---|---|
| position SERVED and printed in the Summary | **73** | the 72 of the first run plus `BP LN`; each Summary contains the served `last_stated_position` text |
| position SERVED and NOT printed | **0** | the defect class of C-S189 |
| position not served (ABSENT) | **28** | the Summary reads the no-recommendation sentence; two causes below |
| request error | **0** | the one first-run error was the folder name `BP`, not a route key |

**The 28 names with no served position, with the cause the served field names (`dossier_fields.last_stated_position.reason`):**
- `no report carries a non-empty RECOMMENDATION line` (**23** names): 1299 HK, 2317 TT, 8306 JP, 8316 JP, 8766 JP, 9433 JP, 992 HK, AI FP, AMD US, BA US, COST US, GPN US, HAL US, HD US, KMB US, NG LN, PWR US, ROG SW, RWE GR, SLB US, SSE LN, VLO US, ZURN SW.
- `no research dossier exists for this name` (**5** names): 6501 JP, 6861 JP, CAT US, CSL AU, NVDA US.

**Reading:** the grade holds. Of the 73 names whose position is served, every one prints it in the Summary; none is served and unprinted. The 28 unserved names are an INPUT gap (no report carries a recommendation line, or no dossier exists), not a pack defect: whether a recommendation should exist for them is the research team's, not a renderer's. **Not checked:** that the served position is the CURRENT recommendation (the instrument reads what the route serves); that a Summary which prints the text prints it in the right order for every name (the three graded names were read in round 117).

**Instrument note:** the census treats a folder name as a route key, which is wrong for a slash-encoded folder (`BP`); the count above is corrected by hand for that one folder, and the instrument is left as run (its raw output is the record).
