# NAMING_CENSUS_COMPARISON -- census mode, the comparison, round 3

**Worker:** `0.9.0_WK_LGIC_ENFORCE~4` | **TO:** `LGIC_ENFORCE.TO-EN-s-6-r3` | **Branch:** `wk-lgic-enforce-3-4`,
cut from CLOUD @`b54636545d`. Every file below was read at that base unless a later commit is named.

This file sets round 3's census report's totals beside the two hand products the order names -- LGIC_NAMING's
N2 worked cases and N6 grader rows -- and (matching round 2's shape) IV7's ranking, over the REAL hand
populations (N2 45, N6 88). It grades no name itself.

## What this comparison can say, and what it cannot

The report it reads, `NAMING_CENSUS_REPORT.r3.md` (this worker, this worktree, HEAD `b54636545d`), **STOPPED on
its first RAISE** -- live plane, API_GW `sentiment-query-api`, `R1.f: 'sentiment' is in no vocabulary; no
registry row resolves it` -- exactly as round 1's and round 2's runs did (rows `LGIC_ENFORCE-W7-S1`,
`LGIC_ENFORCE-W4-S5`). A RAISE is never filed under a verdict, so it is not a fourth verdict in any table below.

The census therefore judged **3 of 1829** nameable live names and **0 of 1878** repo names. All 3 are of one
type, API_GW, and they are the first three API_GW names the run reached, in the order the live pull returned
them. They are not a sample of anything. So:

- the comparison covers **3 names** and says nothing about the other 1826 nameable live names or any repo name;
- the names graded both by the census and by a hand product number **1** (N2) and **2** (N6); none is in both;
- IV7 gives no per-name verdict, so on IV7 there is no verdict to compare -- **0** names graded by both;
- the name the census stopped on, `sentiment-query-api`, appears in none of the three hand products (checked
  by string search against all 45 N2 worked cases and all 88 N6 rows).

**S6R3-AC4 FAILS by measurement, exactly as this order's ACCEPTANCE states in advance**: the arithmetic below
closes on both N2 and N6, but the embedded census is `stopped` and incomplete on both planes, and
`check_en_r3.py s6-comparison-arithmetic` requires the embedded census to be complete, not merely for the
compared/uncompared counts to sum to the hand population.

## Inputs, each at the commit that last changed it

| product | file | commit | its own vintage |
|---|---|---|---|
| census | `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~4/NAMING_CENSUS_REPORT.r3.md` | (this commit) | live pull "Built from the estate as of 2026-09-17 13:49:55 UTC. Stitch source: stitch-codebuild built 2026-09-17T03:01:15Z. manifest: 0dd53f50b7da", registry@`4a7c7676da225e7b` |
| N2 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`, section 9 json | `7c1e9ffb26` | "Built from the estate as of 2026-09-14 12:13:53 UTC" |
| N6 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv` | `388b07f486` | `# base 3d671ff59c...` |
| N6 agreement | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-compare.md` | `f829fdb1fc` | 85 of 85 discriminating names agree; the two answer files are byte-identical (0 of 88 rows disagree) |
| IV7 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md` | `3497a41c31` | the brief Part IV.7 and `infra/logic/09_NAMING_CENSUS.md` (2,531 live nodes, 2026-09-13) |

The census and the hand products use different instruments. The census calls `grade()` in `lib/opal_naming.py`
against the registry at `4a7c7676da225e7b`. N2 and N6 apply `GRADING_RULE.md` by hand, at their own,
earlier live-pull vintages.

**What moved since round 2's comparison.** `GRADING_RULE.md` moved from `fd6ce8c330` to `7c1e9ffb26`; its
section 9 json still carries exactly **45** worked cases and the one API_GW case the census can reach
(`opal-portal-data-proxy-api`, CONFORMANT `opal-portal-data-proxy-api`) is unchanged -- EXERCISED by reading the
fence directly (see evidence below). ITS VERDICT MIX DID MOVE, measured by counting the 45 rows' `verdict`
field directly (not carried over from round 2's table): CONFORMANT 18, ALIAS 3, OUT-OF-PATTERN 20, RAISE 2,
NOT-GRADED 2 (round 2 read OUT-OF-PATTERN 18, RAISE 4 on the pre-recut file) -- section 1's N2 row below is
this round's own count. N6's tsv and `n6-compare.md` are at the commits round 2 read; `n6-grader-a.tsv` still
carries exactly 88 data rows and the same verdict mix (CONFORMANT 13, ALIAS 1, OUT-OF-PATTERN 37, RAISE 18,
NOT-GRADED 19), re-measured the same way. The live estate moved (round 2's live pull: 2176 nodes, live_nameable
1821; this round's: 2191 nodes, live_nameable 1829), but the 3 names the census reaches did not change and
neither did their verdicts.

## 1. The totals, side by side

Each row counts its own population. The populations differ, so the shares are not comparable.

| product | population (denominator) | CONFORMANT | ALIAS | OUT-OF-PATTERN | RAISE | NOT-GRADED |
|---|---|---|---|---|---|---|
| census (live, judged) | 3 of 1829 live_nameable; repo 0 of 1878 | 2 | 0 | 1 | stopped on 1 (never filed under a verdict) | 0 |
| N2 worked cases | 45 | 18 | 3 | 20 | 2 | 2 |
| N6 grader A | 88 (85 discriminating + 3 overlap with N2) | 13 | 1 | 37 | 18 | 19 |
| IV7 ranking | 10 ranked surfaces, no per-name verdicts | -- | -- | -- | -- | -- |

The census's totals by type are one row: API_GW, live, CONFORMANT 2, OUT-OF-PATTERN 1, ALIAS 0, NOT-GRADED 0.

## 2. Name by name: every name graded by both

The match is on `(name, type)`. A pair agrees when the verdict and the canonical form are both equal, byte for
byte.

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

N6 does not hold `opal-portal-data-proxy-api`. N6 grades one further API_GW name, `trade-submission-api`
(CONFORMANT), which the census never reached; it is not graded here.

**Coverage.** 3 of the 3 census rows fall in N2 or N6, and none in both -- N2 and N6 share no API_GW name.

## 3. Against IV7

`TENSION_RANKING.md` ranks 10 naming surfaces by what each costs today. It gives no verdict for any name and
names none of the 3 census rows, so 0 names are graded by both and there is no verdict to compare. Its figures
come from a different census -- `infra/logic/09_NAMING_CENSUS.md`, 2,531 live nodes, 2026-09-13. A run that
judged 3 rows of one type cannot set a count beside any of them, so **no IV7 rank or figure is confirmed or
contradicted by this census**.

- `inf-otp-relay-api` (OUT-OF-PATTERN) carries the firm token `inf` where the system should be, recorded in its
  canonical form `{system}-inf-otp-relay-api` -- the shape IV7 rank 1 describes ("firm-as-system").
- `opal-portal-data-proxy-api` and `opal-session-analytics-api` (both CONFORMANT) begin with `opal-`, the prefix
  IV7 rank 7 counts. The census and N2 (on the first of them) read `opal` there as the system, not as a null
  prefix.
- The name the run stopped on, `sentiment-query-api`, stopped it because `sentiment` is in no vocabulary and no
  registry row resolves it -- the shape of IV7 rank 6 (a first token no registry lists as a system). It is a
  shape, not a figure: one stop cannot size rank 6, and the RAISE is filed under no verdict.

## 4. Disagreements

**None.** 0 disagreements in 3 compared pairs (N2 1, N6 2), and 0 on IV7, which grades no name. The json below
carries an empty `disagreements` list. This is the same result as round 1 and round 2, on the same 3 names,
because the run stops at the same point each round.

## 5. What the census did not reach, with denominators

- **The live plane, past the stop.** 1826 of 1829 nameable live names were never judged (judged_live 3). The
  live pull returned 2191 nodes; 346 are of types the schema does not grade by kind and 16 are `aws_fixed`
  names outside the grade's domain, which is how 1829 is reached. The run stopped at the first RAISE and did
  not resume.
- **The repo plane, entirely.** judged_repo is **0 of 1878** -- 0 of the Terraform names (473 tracked `.tf`
  files; 128 name attributes that are expressions are not names) and 0 of the source names (468 tracked files,
  after 2864 vendored and test files were excluded). The census judges live first, so the stop came before the
  repo plane ran.
- **Types.** 1 type (API_GW) carries any judged row. The live command asked for 33 node types; the report puts
  8 of them outside the grade by kind (API_ROUTE, CLOUDFRONT_DISTRIBUTION, EVENT_SOURCE, IAM_USER, KMS_KEY,
  ROUTE53_RECORD, SERVICE_PRINCIPAL, VPC_ENDPOINT, 346 nodes), which leaves 25 graded types, so **24 graded
  types carry no judged row at all**.
- **Hand rows left uncompared.** 44 of N2's 45 worked cases and 86 of N6's 88 rows have no census verdict to be
  set beside, because the census never judged those names. Each is uncompared for the SAME reason: the census
  stopped before reaching it, not because it was checked and found not to match. No further reason is stated
  per row; the reason is uniform across all 44 + 86 = 130 uncompared hand rows.
- **The stop itself.** `sentiment-query-api` has no verdict in the report (a RAISE is not a verdict) and
  appears in no hand product, so it is compared against nothing.

## 6. What this record does not claim

- It says nothing about the 1826 nameable live names the census did not judge, or about the 1878 repo names.
- It does not grade `sentiment-query-api`, and it does not judge whether the registry row its RAISE calls for
  is owed, or by whom -- that is filed as row `LGIC_ENFORCE-W4-S5` and is the channel's business, not this
  comparison's.
- The comparison is only as current as the census report it reads. A census re-run after the registry gains a
  row resolving `sentiment` (and one resolving `inf-otp-relay-api`'s system) would judge past this stop and
  produce rows this comparison has never seen.
- A 3-name agreement is not evidence that `grade()` and the hand rule agree in general.
- `3.0.0_SA_CVO` grades `S6R3-AC5` at L9: whether every hand row this comparison leaves uncompared carries a
  stated reason. Section 5 above states one uniform reason (the run stopped before reaching any of them) for
  all 130 uncompared rows; this record gives no verdict on whether that reason satisfies the criterion.

```json
{
 "census": {"report": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~4/NAMING_CENSUS_REPORT.r3.md", "vintage": "Built from the estate as of 2026-09-17 13:49:55 UTC. Stitch source: stitch-codebuild built 2026-09-17T03:01:15Z.  manifest: 0dd53f50b7da", "registry": "4a7c7676da225e7b", "judged_live": 3, "live_nameable": 1829, "live": 2191, "judged_repo": 0, "repo": 1878, "types_with_judged_rows": 1, "totals": {"API_GW/live": {"CONFORMANT": 2, "ALIAS": 0, "OUT-OF-PATTERN": 1, "NOT-GRADED": 0}}, "stopped": {"plane": "live", "type": "API_GW", "current": "sentiment-query-api", "message": "R1.f: 'sentiment' is in no vocabulary; no registry row resolves it", "in_hand_products": false}},
 "against": {
  "N2": {"hand_population": 45, "hand_types": 26, "census_judged": 3, "compared": ["opal-portal-data-proxy-api"], "agree": 1, "uncompared_hand_rows": 44, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md@7c1e9ffb26"},
  "N6": {"hand_population": 88, "hand_types": 33, "census_judged": 3, "compared": ["inf-otp-relay-api", "opal-session-analytics-api"], "agree": 2, "uncompared_hand_rows": 86, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv@388b07f486; agreement n6-compare.md@f829fdb1fc (85 of 85 discriminating agree, 0 of 88 rows disagree)"},
  "IV7": {"denominator": 10, "denominator_is": "the ranking's 10 surfaces; IV7 carries no per-name verdict", "names_graded_by_both": 0, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md@3497a41c31"}
 },
 "not_reached": {"live_nameable_unjudged": 1826, "repo_unjudged": 1878, "repo_plane_ran": false, "types_requested": 33, "types_not_graded_by_kind": 8, "graded_types": 25, "graded_types_with_no_judged_row": 24, "n2_rows_uncompared": 44, "n6_rows_uncompared": 86, "uncompared_reason_uniform": "the census stopped at the first RAISE (sentiment-query-api, R1.f) before reaching any of the 130 uncompared hand rows"},
 "disagreements": []
}
```
