# RESIDUE_E2_GROSS -- counts only (TO IRPT_DASHBD.TO-DB-b-28)

Source: the GROSS record of DB-b-27. Zero vendor calls. Closure date 2025-01-09. Surprise rows filed: none.

- Denominator (graded rows): 9,078
- UNEXPLAINED (OUTSIDE, reason UNEXPLAINED): 3,279
- PLUS_ONE_DAY (BD days - Opal days == 1, segment spans 2025-01-09): 3,395
- Overlap: 2,299
- Union (one residue row each): 4,375

Residue per reason (closed set): FLOW_TIMING 107; MISSING_PRICE 0; INCOME_DATE 10; COVERAGE_DAYS 979; UNEXPLAINED 3,279.

Rule: a +1-day segment is residue, never agreement (PRD ruling 23). A +1-day segment inside tolerance is COVERAGE_DAYS;
one outside tolerance keeps the gross record's reason; an UNEXPLAINED segment stays UNEXPLAINED even when +1-day (the
day count alone is not shown to account for the return gap). No reason was added to the closed set.
