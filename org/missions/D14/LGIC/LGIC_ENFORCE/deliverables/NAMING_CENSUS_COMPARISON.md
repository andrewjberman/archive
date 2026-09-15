# NAMING_CENSUS_COMPARISON -- census mode, the comparison (LGIC_ENFORCE EN-s-2, DEC-7)

**Worker:** `0.9.0_WK_LGIC_ENFORCE~7` | **TO:** `LGIC_ENFORCE.TO-EN-s-2` | **Branch:** `wk-lgic-enforce-1-7-s2`, cut from
CLOUD @`652d3a2204`.

This file sets the census report's totals beside three hand products and compares the verdicts on every name that
both the census and a hand product graded. It does not grade any name itself.

## What this comparison can say, and what it cannot

The census report it reads **stopped on its first RAISE** (row `LGIC_ENFORCE-W7-S1`). It judged **3 of 1805**
nameable live names and **0 of 1869** repo names. All 3 are of one type, API_GW. They are the first three API_GW
names the census reached, so they are not a sample of anything. So:

- the comparison covers **3 names** and says nothing about the rest of the estate;
- the names graded both by the census and by a hand product number **1** (N2) and **2** (N6);
- IV7 grades no name, so on IV7 no verdict can be compared;
- the name the census stopped on, API_GW `sentiment-query-api`, is in none of the three hand products.

Every denominator below is printed as it is. No name the census did not judge is graded here to fill one. Row
`LGIC_ENFORCE-W7-S4` records what the order says beside what the census holds.

## Inputs, each at the commit that last changed it (all read at base `652d3a2204`)

| product | file | commit | its own vintage |
|---|---|---|---|
| census | `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/NAMING_CENSUS_REPORT.md` | `f64b6f35cb` | live pull "Built from the estate as of 2026-09-15 00:57:50 UTC", registry@50e4fabd1cb6a150 |
| N2 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`, section 9 json | `51b0952d71` | `LIVE_NAMES.json` "Built from the estate as of 2026-09-14 12:13:53 UTC" |
| N6 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv` | `388b07f486` | `# base 3d671ff59c...` |
| N6 agreement | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-compare.md` | `f829fdb1fc` | 85 of 85 discriminating names agree; the two answer files are byte-identical (0 of 88 rows disagree) |
| IV7 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md` | `3497a41c31` | the brief @`1b42dbe758` Part IV.7 and `infra/logic/09_NAMING_CENSUS.md` (2,531 live nodes, 2026-09-13) |

The census and the hand products use different instruments. The census calls `grade()` in `lib/opal_naming.py`
against the registry. N2 and N6 apply `GRADING_RULE.md` by hand. They also read live names at different vintages.

## 1. The totals, side by side

Each row counts its own population. The populations differ, so the shares are not comparable.

| product | population (denominator) | CONFORMANT | ALIAS | OUT-OF-PATTERN | RAISE | NOT-GRADED |
|---|---|---|---|---|---|---|
| census (live, judged) | 3 of 1805 live_nameable; repo 0 of 1869 | 2 | 0 | 1 | stopped on 1 (never filed under a verdict) | 0 |
| N2 worked cases | 43 | 18 | 3 | 18 | 3 | 1 |
| N6 grader A | 88 (85 discriminating + 3 overlap with N2) | 13 | 1 | 37 | 18 | 19 |
| IV7 ranking | 10 ranked surfaces, no per-name verdicts | -- | -- | -- | -- | -- |

The census's totals by type are one row: API_GW, live, CONFORMANT 2, OUT-OF-PATTERN 1. Among the hand products,
API_GW appears once in N2 (`opal-portal-data-proxy-api`, CONFORMANT) and three times in N6
(`inf-otp-relay-api` OUT-OF-PATTERN, `opal-session-analytics-api` CONFORMANT, `trade-submission-api` CONFORMANT).

## 2. Name by name: every name graded by both

The match is on (name, type). A pair agrees when the verdict and the canonical form are both equal.

**Against N2: 1 name graded by both, 1 agrees.**

| name | type | census | N2 | result |
|---|---|---|---|---|
| `opal-portal-data-proxy-api` | API_GW | CONFORMANT `opal-portal-data-proxy-api` | CONFORMANT `opal-portal-data-proxy-api` | AGREE |

N2 does not hold `inf-otp-relay-api` or `opal-session-analytics-api`.

**Against N6: 2 names graded by both, 2 agree.**

| name | type | census | N6 grader A | result |
|---|---|---|---|---|
| `inf-otp-relay-api` | API_GW | OUT-OF-PATTERN `{system}-inf-otp-relay-api` | OUT-OF-PATTERN `{system}-inf-otp-relay-api` | AGREE |
| `opal-session-analytics-api` | API_GW | CONFORMANT `opal-session-analytics-api` | CONFORMANT `opal-session-analytics-api` | AGREE |

N6 does not hold `opal-portal-data-proxy-api`. Grader B's file is byte-identical to grader A's (`n6-compare.md`
section 2), so these two agreements hold against both graders. N6 grades one more API_GW name,
`trade-submission-api`, which the census never reached. It is not graded here.

**Coverage.** 3 of the 3 census rows fall in N2 or N6. None falls in both, and N2 and N6 share no API_GW name.

## 3. Against IV7

`TENSION_RANKING.md` ranks 10 naming surfaces by what each one costs. It gives no verdict for any name and names none
of the 3 census rows, so 0 names are graded by both and there is no verdict to compare. Its figures (for example
`opal-` in 445 names, a firm in the system slot in ~210) come from a different census, over 2,531 live nodes on
2026-09-13. A stopped run with 3 rows of one type cannot set a count beside any of them, so no IV7 rank or figure can
be confirmed or contradicted from this census.

The most this census's own records show is where its 3 rows sit among the surfaces, read from their canonical forms
and not from a new grade:
- `inf-otp-relay-api` (OUT-OF-PATTERN) carries the firm token `inf` where the system should be. Its canonical form
  `{system}-inf-otp-relay-api` records that. This is the shape IV7 rank 1 describes ("firm-as-system").
- `opal-portal-data-proxy-api` and `opal-session-analytics-api` (both CONFORMANT) begin with `opal-`, the prefix that
  IV7 rank 7 counts. The census, and N2 on the first of them, read `opal` there as the system (`GRADING_RULE.md`
  R2, `:155-158` @`51b0952d71`: t2 is in neither V1 nor V2), not as a null prefix. So a name on a ranked surface
  can still be CONFORMANT. IV7 measures cost and the grade gives a verdict, which are different things.

## 4. Disagreements

**None.** 0 disagreements in 3 compared pairs (N2 1, N6 2) and 0 on IV7, which grades no name. The json below
carries an empty list.

## 5. What this record does not claim

- It says nothing about the 1802 nameable live names the census did not judge, or about the 1869 repo names. The
  census judged none of those names, and none of them is graded here.
- It does not grade `sentiment-query-api`, the name the census stopped on. No hand product holds that name.
- The comparison is only as current as the census report it reads. A census re-run after the registry rows owed under
  row `LGIC_ENFORCE-W7-S1` would produce different rows, and this comparison would need to be run again on them.
- 3.0.0_SA_CVO grades `S2-J1` at L9: do the totals agree with the hand ranking, or is every difference explained? This
  record gives no verdict on it.

```json
{
 "against": {
  "N2": {"denominator": 1, "agree": 1, "denominator_is": "names graded by both the census and N2's worked cases, matched on (name, type)", "hand_population": 43, "census_judged": 3, "compared": ["opal-portal-data-proxy-api"], "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md@51b0952d71"},
  "N6": {"denominator": 2, "agree": 2, "denominator_is": "names graded by both the census and n6-grader-a.tsv, matched on (name, type)", "hand_population": 88, "census_judged": 3, "compared": ["inf-otp-relay-api", "opal-session-analytics-api"], "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv@388b07f486; agreement n6-compare.md@f829fdb1fc (85 of 85 discriminating, 0 of 88 rows disagree)"},
  "IV7": {"denominator": 10, "denominator_is": "the ranking's 10 surfaces; IV7 carries no per-name verdict", "names_graded_by_both": 0, "notes": "TENSION_RANKING.md@3497a41c31 ranks 10 surfaces by cost, with figures from infra/logic/09_NAMING_CENSUS.md (2,531 live nodes, 2026-09-13). It names none of the 3 census rows, so no verdict can be compared, and a stopped census of 3 API_GW rows cannot set a count beside any rank's figure. The census's own canonical forms place inf-otp-relay-api on the rank-1 shape (firm token in the system slot, {system}-inf-otp-relay-api) and the two opal- rows on the rank-7 prefix, where the census and N2 read opal as the system (GRADING_RULE.md R2), not as a null prefix. No rank is confirmed or contradicted.", "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md@3497a41c31"}
 },
 "census": {"report": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/NAMING_CENSUS_REPORT.md@f64b6f35cb", "vintage": "Built from the estate as of 2026-09-15 00:57:50 UTC", "registry": "50e4fabd1cb6a150", "judged_live": 3, "live_nameable": 1805, "judged_repo": 0, "repo": 1869, "totals": {"API_GW/live": {"CONFORMANT": 2, "ALIAS": 0, "OUT-OF-PATTERN": 1, "NOT-GRADED": 0}}, "stopped": {"plane": "live", "type": "API_GW", "current": "sentiment-query-api", "in_hand_products": false}, "row": "LGIC_ENFORCE-W7-S1"},
 "disagreements": []
}
```
