# NAMING_CENSUS_COMPARISON -- census mode, the comparison (LGIC_ENFORCE EN-s-2, DEC-7), round 2

**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **TO:** `LGIC_ENFORCE.TO-EN-s-2-r2` | **Branch:** `wk-lgic-enforce-2e-2b`,
cut from CLOUD @`2a2b853f79`. Every file below was read at that base.

This file sets the round-2 census report's totals beside three hand products and compares the verdicts on every name
that both the census and a hand product graded. It grades no name itself. It replaces round 1's comparison
(@`e6ffd3a2a0`), which read a different census report at a different registry vintage.

## What this comparison can say, and what it cannot

The report it reads, rewritten by `EN-s-1` in round 2 (@`db7eac8f1d`), **stopped on its first RAISE** -- live plane,
API_GW `sentiment-query-api`, `R1.f: 'sentiment' is in no vocabulary; no registry row resolves it`. A RAISE is never
filed under a verdict, so it is not a fourth verdict in any table below.

The census therefore judged **3 of 1821** nameable live names and **0 of 1878** repo names. All 3 are of one type,
API_GW, and they are the first three API_GW names the run reached, in the order the live pull returned them. They are
not a sample of anything. So:

- the comparison covers **3 names** and says nothing about the other 1818 nameable live names or any repo name;
- the names graded both by the census and by a hand product number **1** (N2) and **2** (N6); none is in both;
- IV7 gives no per-name verdict, so on IV7 there is no verdict to compare -- **0** names graded by both;
- the name the census stopped on, `sentiment-query-api`, appears in none of the three hand products (checked as
  `(type, name)` against all 45 N2 cases and all 88 N6 rows).

**S2R-AC3 FAILs by measurement**, and this record is what the order asks for anyway (`TO-EN-s-2-r2`, THE CELL:
"If the census stopped on a RAISE, S2R-AC3 FAILs by measurement and the order stays pending ... Compare what the
report judged anyway, and say what it did not reach."). Section 5 states what it did not reach, with denominators.

## Inputs, each at the commit that last changed it (all read at base `2a2b853f79`)

| product | file | commit | its own vintage |
|---|---|---|---|
| census | `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/NAMING_CENSUS_REPORT.md` | `db7eac8f1d` | live pull "Built from the estate as of 2026-09-16 05:57:28 UTC", registry@`254d4e9ece847acb` |
| N2 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`, section 9 json | `fd6ce8c330` | `LIVE_NAMES.json` "Built from the estate as of 2026-09-14 12:13:53 UTC" |
| N6 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv` | `388b07f486` | `# base 3d671ff59c...` |
| N6 agreement | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-compare.md` | `f829fdb1fc` | 85 of 85 discriminating names agree; the two answer files are byte-identical (0 of 88 rows disagree) |
| IV7 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md` | `3497a41c31` | the brief @`1b42dbe758` Part IV.7 and `infra/logic/09_NAMING_CENSUS.md` (2,531 live nodes, 2026-09-13) |

The census and the hand products use different instruments. The census calls `grade()` in `lib/opal_naming.py`
against the registry at `254d4e9ece847acb`. N2 and N6 apply `GRADING_RULE.md` by hand. They also read live names at
different vintages: the census's pull is 2026-09-16, N2's is 2026-09-14, N6's base is `3d671ff59c`.

**What moved since round 1.** Of the four hand inputs, only N2 changed: `GRADING_RULE.md` was re-cut to
NAMING_SCHEMA v1.9 (@`fd6ce8c330`), so its worked cases went from 43 to 45. Measured by diffing the two section-9
json blocks: two cases added (`LAMBDA mdpf-lambda-lambda`, `LAMBDA orion-orion-lambda-lambda`, both RAISE
specimens), none removed, one verdict changed (`SECURITY_GROUP default`, RAISE -> NOT-GRADED under G2/RULING AW1),
one canonical form changed (`LOAD_BALANCER opal-gateway`, `opal-gateway-lb` -> `gateway-lb`). **None of the four
touches the one name N2 shares with the census**, so round 1's N2 agreement is not disturbed by the re-cut. The N6
files and `TENSION_RANKING.md` are at the same commits round 1 read.

## 1. The totals, side by side

Each row counts its own population. The populations differ, so the shares are not comparable.

| product | population (denominator) | CONFORMANT | ALIAS | OUT-OF-PATTERN | RAISE | NOT-GRADED |
|---|---|---|---|---|---|---|
| census (live, judged) | 3 of 1821 live_nameable; repo 0 of 1878 | 2 | 0 | 1 | stopped on 1 (never filed under a verdict) | 0 |
| N2 worked cases | 45 | 18 | 3 | 18 | 4 | 2 |
| N6 grader A | 88 (85 discriminating + 3 overlap with N2) | 13 | 1 | 37 | 18 | 19 |
| IV7 ranking | 10 ranked surfaces, no per-name verdicts | -- | -- | -- | -- | -- |

The census's totals by type are one row: API_GW, live, CONFORMANT 2, OUT-OF-PATTERN 1, ALIAS 0, NOT-GRADED 0. The
hand products are far wider by type and far narrower by count: N2 covers 26 types in 45 cases, N6 33 types in 88
rows, the census 1 type in 3 rows. API_GW appears once in N2 (`opal-portal-data-proxy-api`, CONFORMANT) and three
times in N6 (`inf-otp-relay-api` OUT-OF-PATTERN, `opal-session-analytics-api` CONFORMANT, `trade-submission-api`
CONFORMANT).

## 2. Name by name: every name graded by both

The match is on `(name, type)`. A pair agrees when the verdict and the canonical form are both equal, byte for byte.

**Against N2: 1 name graded by both, 1 agrees.**

| name | type | census | N2 | result |
|---|---|---|---|---|
| `opal-portal-data-proxy-api` | API_GW | CONFORMANT `opal-portal-data-proxy-api` | CONFORMANT `opal-portal-data-proxy-api` | AGREE |

N2 holds no other API_GW case, so it holds neither `inf-otp-relay-api` nor `opal-session-analytics-api`.

**Against N6: 2 names graded by both, 2 agree.**

| name | type | census | N6 grader A | result |
|---|---|---|---|---|
| `inf-otp-relay-api` | API_GW | OUT-OF-PATTERN `{system}-inf-otp-relay-api` | OUT-OF-PATTERN `{system}-inf-otp-relay-api` | AGREE |
| `opal-session-analytics-api` | API_GW | CONFORMANT `opal-session-analytics-api` | CONFORMANT `opal-session-analytics-api` | AGREE |

N6 does not hold `opal-portal-data-proxy-api`. Grader B's file is byte-identical to grader A's (`n6-compare.md`
section 2, sha256 `41c3de9d...ffde945` on both), so these two agreements hold against both graders. N6 grades one
further API_GW name, `trade-submission-api` (CONFORMANT), which the census never reached; it is not graded here.

**Coverage.** 3 of the 3 census rows fall in N2 or N6, and none in both -- N2 and N6 share no API_GW name. By type
the overlap is 1 of N2's 26 types and 1 of N6's 33.

## 3. Against IV7

`TENSION_RANKING.md` ranks 10 naming surfaces by what each costs today. It gives no verdict for any name and names
none of the 3 census rows, so 0 names are graded by both and there is no verdict to compare. Its figures (for example
`opal-` in 445 names over 18 types, the firm in the system slot in ~210 names, 118 distinct first tokens with no
registry) come from a different census -- `infra/logic/09_NAMING_CENSUS.md`, 2,531 live nodes, 2026-09-13. A run that
judged 3 rows of one type cannot set a count beside any of them, so **no IV7 rank or figure is confirmed or
contradicted by this census**.

What the census's own records do show is where its rows sit among the ranked surfaces, read from the canonical forms
it already computed and from its stop record -- not from any new grade:

- `inf-otp-relay-api` (OUT-OF-PATTERN) carries the firm token `inf` where the system should be, which its canonical
  form `{system}-inf-otp-relay-api` records. That is the shape IV7 rank 1 describes ("firm-as-system").
- `opal-portal-data-proxy-api` and `opal-session-analytics-api` (both CONFORMANT) begin with `opal-`, the prefix IV7
  rank 7 counts. The census, and N2 on the first of them, read `opal` there as the system (`GRADING_RULE.md` R2: t2
  is in neither V1 nor V2), not as a null prefix. A name on a ranked surface can still be CONFORMANT: IV7 measures
  cost, the grade returns a verdict, and they are different questions.
- The name the run stopped on, `sentiment-query-api`, stopped it because `sentiment` is in no vocabulary and no
  registry row resolves it. That is the shape of IV7 rank 6 -- a first token that no registry lists as a system, in
  an estate with 118 distinct first tokens and no such registry. It is a shape, not a figure: one stop cannot size
  rank 6's 28 names, and the RAISE is filed under no verdict, so it enters no table above.

## 4. Disagreements

**None.** 0 disagreements in 3 compared pairs (N2 1, N6 2), and 0 on IV7, which grades no name. The json below
carries an empty `disagreements` list. Round 1 reached the same count on the same 3 names against a census at a
different registry vintage (`254d4e9ece847acb` here, `50e4fabd1cb6a150` there).

## 5. What the census did not reach, with denominators

This is the section the order asks for, and every number is the report's own.

- **The live plane, past the stop.** 1818 of 1821 nameable live names were never judged (judged_live 3). The live
  pull returned 2176 nodes; 339 are of types the schema does not grade by kind and 16 are `aws_fixed` names outside
  the grade's domain, which is how 1821 is reached. The run stopped at the first RAISE and did not resume.
- **The repo plane, entirely.** judged_repo is **0 of 1878** -- 0 of the Terraform names (472 tracked `.tf` files;
  121 name attributes that are expressions are not names) and 0 of the source names (468 tracked files, after 2864
  vendored and test files were excluded). The census judges live first, so the stop came before the repo plane ran.
  Nothing in this comparison touches the repo plane at all.
- **Types.** 1 type (API_GW) carries any judged row. The live command asked for 33 node types; the report puts 8 of
  them outside the grade by kind (API_ROUTE, CLOUDFRONT_DISTRIBUTION, EVENT_SOURCE, IAM_USER, KMS_KEY,
  ROUTE53_RECORD, SERVICE_PRINCIPAL, VPC_ENDPOINT, 339 nodes), which leaves 25 graded types, so **24 graded types
  carry no judged row at all**. No LAMBDA, IAM_ROLE,
  IAM_POLICY, S3_BUCKET, S3Key, SECRET, CW_ALARM, EVENT_RULE, SCHEDULE or any other graded type was reached, and
  those are where N2's 26 types and N6's 33 types hold their mass.
- **Hand rows left uncompared.** 44 of N2's 45 worked cases and 86 of N6's 88 rows have no census verdict to be set
  beside, because the census never judged those names. They are not graded here and no verdict is inferred for them.
- **The stop itself.** `sentiment-query-api` has no verdict in the report (a RAISE is not a verdict) and appears in
  no hand product, so it is compared against nothing.

## 6. What this record does not claim

- It says nothing about the 1818 nameable live names the census did not judge, or about the 1878 repo names.
- It does not grade `sentiment-query-api`, and it does not judge whether the registry row its RAISE calls for is
  owed, or by whom. That is `EN-r-2`'s ruling and the channel's business, not this comparison's.
- The comparison is only as current as the census report it reads. A census re-run after the registry gains a row
  resolving `sentiment` would judge past this stop and produce rows this comparison has never seen; the comparison
  would then have to be made again on them.
- A 3-name agreement is not evidence that `grade()` and the hand rule agree in general. 3 of 1821, one type, taken
  in arrival order, is too small and too narrow to bound disagreement anywhere else.
- `3.0.0_SA_CVO` grades `S2R-J1` at L9: do the totals agree with the hand ranking, or is every difference explained?
  This record gives no verdict on it.

```json
{
 "against": {
  "N2": {"denominator": 1, "agree": 1, "denominator_is": "names graded by both the census and N2's worked cases, matched on (name, type)", "hand_population": 45, "hand_types": 26, "census_judged": 3, "compared": ["opal-portal-data-proxy-api"], "uncompared_hand_rows": 44, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md@fd6ce8c330", "note": "Re-cut to NAMING_SCHEMA v1.9 since round 1 (43 -> 45 cases: 2 added, 1 verdict changed, 1 canonical form changed); none of the four changes touches the compared name."},
  "N6": {"denominator": 2, "agree": 2, "denominator_is": "names graded by both the census and n6-grader-a.tsv, matched on (name, type)", "hand_population": 88, "hand_types": 33, "census_judged": 3, "compared": ["inf-otp-relay-api", "opal-session-analytics-api"], "uncompared_hand_rows": 86, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv@388b07f486; agreement n6-compare.md@f829fdb1fc (85 of 85 discriminating agree, 0 of 88 rows disagree, answer files byte-identical)"},
  "IV7": {"denominator": 10, "denominator_is": "the ranking's 10 surfaces; IV7 carries no per-name verdict", "names_graded_by_both": 0, "notes": "TENSION_RANKING.md@3497a41c31 ranks 10 surfaces by cost, with figures from infra/logic/09_NAMING_CENSUS.md (2,531 live nodes, 2026-09-13). It names none of the 3 census rows, so no verdict can be compared, and a stopped census of 3 API_GW rows cannot set a count beside any rank's figure. Read from the census's own canonical forms and stop record, not from a new grade: inf-otp-relay-api sits on the rank-1 shape (firm token in the system slot, {system}-inf-otp-relay-api); the two opal- rows sit on the rank-7 prefix, where the census and N2 read opal as the system (GRADING_RULE.md R2) and both are CONFORMANT; and the stop, sentiment-query-api, is the rank-6 shape (a first token no registry lists as a system). No rank is confirmed or contradicted.", "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md@3497a41c31"}
 },
 "census": {"report": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/NAMING_CENSUS_REPORT.md@db7eac8f1d", "vintage": "Built from the estate as of 2026-09-16 05:57:28 UTC", "registry": "254d4e9ece847acb", "judged_live": 3, "live_nameable": 1821, "live": 2176, "judged_repo": 0, "repo": 1878, "types_with_judged_rows": 1, "totals": {"API_GW/live": {"CONFORMANT": 2, "ALIAS": 0, "OUT-OF-PATTERN": 1, "NOT-GRADED": 0}}, "stopped": {"plane": "live", "type": "API_GW", "current": "sentiment-query-api", "message": "R1.f: 'sentiment' is in no vocabulary; no registry row resolves it", "in_hand_products": false}},
 "not_reached": {"live_nameable_unjudged": 1818, "repo_unjudged": 1878, "repo_plane_ran": false, "types_requested": 33, "types_not_graded_by_kind": 8, "graded_types": 25, "graded_types_with_no_judged_row": 24, "n2_rows_uncompared": 44, "n6_rows_uncompared": 86, "criterion": "S2R-AC3 FAILS by measurement: check_en_r2.py s2r-real-population prints CENSUS STOPPED: True  LIVE 3 of 1821 judged  REPO 0 of 1878 judged, VERDICT: FAIL-PARTIAL-POPULATION, rc=1"},
 "disagreements": []
}
```
