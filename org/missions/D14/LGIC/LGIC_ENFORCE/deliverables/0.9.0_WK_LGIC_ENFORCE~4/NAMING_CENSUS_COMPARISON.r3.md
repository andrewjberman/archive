# NAMING_CENSUS_COMPARISON -- census mode, the comparison, round 3 (AMENDMENT 1 re-run)

**Worker:** `0.9.0_WK_LGIC_ENFORCE~4` | **TO:** `LGIC_ENFORCE.TO-EN-s-6-r3` | **Branch:** `wk-lgic-enforce-3-4`,
cut from CLOUD @`b54636545d`. This supersedes this worker's PRE-AMENDMENT `NAMING_CENSUS_COMPARISON.r3.md`
(3 judged, stopped on `sentiment-query-api`), which read the cell BEFORE AMENDMENT 1 landed.

This file sets round 3's (post-amendment) census report's totals beside the two hand products the order
names -- LGIC_NAMING's N2 worked cases and N6 grader rows -- over the REAL hand populations (N2 45, N6 88).
It grades no name itself.

## What changed under AMENDMENT 1

AMENDMENT 1 (`LGIC_ENFORCE.TO-EN-s-6-r3` THE CELL item 4) added `--not-judged` to
`lib/opal_naming.py census` (R-29): a name in that file is CARDED, not graded, and does not stop the run.
This worker minted ONE registry row the first RAISE named (`infra/logic/registry/resources.json`
`inf-otp-relay-api`, API_GW, system `advi`, citing `infra/aws/terraform/inf-pipeline/api-gateway.tf:24-38
@422a3c724c`), then carded two further RAISEs whose owner could not be measured from any declared source
(`sentiment-query-api`, `trade-submission-api` -- `OWNER_CARDS_S6.r3.md` Cards 1-2), then re-ran.

The re-run reaches a THIRD RAISE, `astn-wsjft-orchestrator-errors` (CW_ALARM), on the token `astn` --
already MEASURED unresolved by `EN-r-5-r3` (same registry commit as the two carded API_GW names). A
direct-library sweep (this worker, not a sequential CLI loop -- `RAISE_POPULATION_S6.r3.md`) measures
**462 RAISE occurrences, 351 distinct (plane, type, name) triples** still ahead of this point, dominated by
the SAME three already-unresolved tokens (`news` 114, `trade` 50, `astn` 35 -- `astn`/`trade` overlapping
the two already carded/stopped-on) plus `json`/`jwt`/`security`/etc. (S3 key path segments, not system
tokens at all). **This crosses THE CELL's own timebox** ("if more than 25 distinct RAISEs appear, stop
minting, file the full list as one row, and FWD-5 goes to round 4 on that list") by more than an order of
magnitude. Per that clause this worker STOPS minting/carding here: row
`LGIC_ENFORCE-W4-S<next>` files the full list; `RAISE_POPULATION_S6.r3.md` is its evidence.

## What this comparison can say, and what it cannot

The report it reads, `NAMING_CENSUS_REPORT.r3.md` (this worker, this worktree, registry@`26623a452ff8583d`),
**STOPPED on its third RAISE** (counting from the amendment's re-run) -- live plane, CW_ALARM
`astn-wsjft-orchestrator-errors`, `R1.c: 'astn' is an unresolved token (V2)`. A RAISE is never filed under a
verdict, so it is not a verdict in any table below. Two names (`sentiment-query-api`,
`trade-submission-api`) are CARDED, not graded -- also not a verdict.

The census therefore judged **21 of 1828** nameable live names (**2 carded**, 23 of 1828 dispositioned) and
**0 of 1878** repo names. All 21 are of three types (API_GW, CODEBUILD_PROJECT, CW_ALARM), the first 21
live names of those types the run reached in pull order. They are not a sample of anything. So:

- the comparison covers **21 judged names** and says nothing about the other 1805 nameable live names, the
  2 carded names, or any repo name;
- **S6R3-AC4 FAILS by measurement**, exactly as this order's ACCEPTANCE states in advance: the arithmetic
  below closes on both N2 and N6, but the embedded census is `stopped` and incomplete on both planes (and
  even judged+carded does not close live_nameable: 23 of 1828), so `check_en_r3.py
  s6-comparison-arithmetic`'s completeness requirement is not met.

## Inputs, each at the commit that last changed it

| product | file | commit | its own vintage |
|---|---|---|---|
| census | `org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~4/NAMING_CENSUS_REPORT.r3.md` | (this commit) | live pull "Built from the estate as of 2026-09-17 14:41:29 UTC. Stitch source: stitch-codebuild built 2026-09-17T03:01:15Z.  manifest: c92a803a1057", registry@`26623a452ff8583d` |
| N2 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md`, section 9 json | `7c1e9ffb26` | "Built from the estate as of 2026-09-14 12:13:53 UTC" |
| N6 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv` | `388b07f486` | `# base 3d671ff59c...` |
| N6 agreement | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-compare.md` | `f829fdb1fc` | 85 of 85 discriminating names agree; the two answer files are byte-identical (0 of 88 rows disagree) |
| IV7 | `org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md` | `3497a41c31` | the brief Part IV.7 and `infra/logic/09_NAMING_CENSUS.md` (2,531 live nodes, 2026-09-13) |

The census and the hand products use different instruments and, for the newly-resolved names, different
REGISTRY VINTAGES: the census calls `grade()` against the registry at `26623a452ff8583d` (which now carries
this cell's `inf-otp-relay-api` row and `EN-r-5-r3`'s `harvest`/`retired`/`find` rows); N2 and N6 applied
`GRADING_RULE.md` by hand, at earlier live-pull vintages, against an OLDER registry state that had none of
those rows -- which is exactly why `inf-otp-relay-api` and `ExecIncrParityFailure` disagree in CANONICAL
FORM below even though both sides call them OUT-OF-PATTERN (Section 4).

## 1. The totals, side by side

Each row counts its own population. The populations differ, so the shares are not comparable.

| product | population (denominator) | CONFORMANT | ALIAS | OUT-OF-PATTERN | RAISE | NOT-GRADED |
|---|---|---|---|---|---|---|
| census (live, judged) | 21 of 1828 live_nameable (+2 carded); repo 0 of 1878 | 3 | 0 | 18 | stopped on 1 (never filed under a verdict) | 0 |
| N2 worked cases | 45 | 18 | 3 | 20 | 2 | 2 |
| N6 grader A | 88 (85 discriminating + 3 overlap with N2) | 13 | 1 | 37 | 18 | 19 |
| IV7 ranking | 10 ranked surfaces, no per-name verdicts | -- | -- | -- | -- | -- |

The census's totals by type: API_GW live CONFORMANT 2 / OUT-OF-PATTERN 1; CODEBUILD_PROJECT live
CONFORMANT 1 / OUT-OF-PATTERN 4; CW_ALARM live OUT-OF-PATTERN 13.

## 2. Name by name: every name graded by both

The match is on `(name, type)`. A pair AGREES when the verdict and the canonical form are both equal, byte
for byte (round 2's rule, unchanged).

**Against N2: 3 names graded by both, 3 agree.**

| name | type | census | N2 | result |
|---|---|---|---|---|
| `opal-portal-data-proxy-api` | API_GW | CONFORMANT `opal-portal-data-proxy-api` | CONFORMANT `opal-portal-data-proxy-api` | AGREE |
| `opal-stitch-produce` | CODEBUILD_PROJECT | OUT-OF-PATTERN `opal-stitch-produce-build` | OUT-OF-PATTERN `opal-stitch-produce-build` | AGREE |
| `Inflection-SilverChain-DimConversionFailure` | CW_ALARM | OUT-OF-PATTERN `{system}-inf-silver-chain-dim-conversion-failure-alarm` | OUT-OF-PATTERN `{system}-inf-silver-chain-dim-conversion-failure-alarm` | AGREE |

N2 holds no other of the 21 judged names.

**Against N6: 6 names graded by both, 2 agree, 4 disagree.**

| name | type | census | N6 grader A | result |
|---|---|---|---|---|
| `inf-otp-relay-api` | API_GW | OUT-OF-PATTERN `advi-inf-otp-relay-api` | OUT-OF-PATTERN `{system}-inf-otp-relay-api` | DISAGREE (canonical -- N6 pre-dates this cell's registry mint) |
| `opal-session-analytics-api` | API_GW | CONFORMANT `opal-session-analytics-api` | CONFORMANT `opal-session-analytics-api` | AGREE |
| `estate-report-seam-freshness-publisher` | CODEBUILD_PROJECT | OUT-OF-PATTERN `estate-report-seam-freshness-publisher-build` | RAISE (no canonical) | DISAGREE (verdict -- `estate` resolves in the current registry, did not at N6's vintage) |
| `opal-drift-producer` | CODEBUILD_PROJECT | OUT-OF-PATTERN `opal-drift-producer-build` | OUT-OF-PATTERN `opal-drift-producer-build` | AGREE |
| `semantic-clustering-lambda-build` | CODEBUILD_PROJECT | OUT-OF-PATTERN `{system}-semantic-clustering-lambda-build` | RAISE (no canonical) | DISAGREE (verdict -- census places a `{system}` placeholder where N6 raised outright) |
| `ExecIncrParityFailure` | CW_ALARM | OUT-OF-PATTERN `{system}-exec-incrparity-failure-alarm` | OUT-OF-PATTERN `{system}-exec-incr-parity-failure-alarm` | DISAGREE (canonical -- tokeniser joins `incr`+`parity` without N6's hyphen; both sides agree on verdict and on the `{system}` placeholder) |

N6 also grades `trade-submission-api` (CONFORMANT), one of the two names THIS cell carded rather than
graded -- not compared here (a carded name carries no census verdict, R-29).

**Coverage.** 9 of the 21 judged names fall in N2 (3) or N6 (6), and none in both (N2 and N6 still share no
name among these types, the same disjointness round 2 measured for API_GW). 12 judged names fall in
neither: `globgrph-derive-build`, `FIRMSEP-auth-advisor-scoping-denied`,
`FIRMSEP-auth-ownership-map-fetch-failed`, `FIRMSEP-auth-ownership-map-schema-mismatch`,
`FIRMSEP-auth-tier-denied`, `FIRMSEP-shared-advisor-router-denied`,
`Inflection-HistBackfill-FailureSpike`, `Inflection-JwtResilience-NearExpirySpike`,
`OPSEC-auth-login-rate-limit-blocked`, `OPSEC-auth-throttled`, `PortfolioExcelGenerator-Errors`,
`YChartsSessionEviction`.

## 3. Against IV7

`TENSION_RANKING.md` ranks 10 naming surfaces by what each costs today. It gives no verdict for any name and
names none of the 21 judged names, so 0 names are graded by both and there is no verdict to compare. Its
figures come from a different census -- `infra/logic/09_NAMING_CENSUS.md`, 2,531 live nodes, 2026-09-13. A
run that judged 21 rows of three types cannot set a count beside any of them, so **no IV7 rank or figure is
confirmed or contradicted by this census**.

- `inf-otp-relay-api`, now OUT-OF-PATTERN with a FIRM token (`advi`) where a system belongs, still carries
  the shape IV7 rank 1 describes ("firm-as-system") -- the mint changed the placeholder, not the pattern.
- The 13 `{system}`-placeholder rows (`ExecIncrParityFailure`, the four `Inflection-*` alarms, the two
  `OPSEC-*` alarms, `PortfolioExcelGenerator-Errors`, `semantic-clustering-lambda-build`) are the shape IV7
  rank 6 names (a first token no registry lists as a system) -- 8 distinct such rows in this run alone, more
  than the 3 the pre-amendment report carried, because the run now reaches past the first stop.
- The name the run stopped on, `astn-wsjft-orchestrator-errors`, is the shape of IV7 rank 6 as well (an
  UNRESOLVED V2 token, not merely a placeholder-eligible one) -- a shape, not a figure: one stop cannot size
  rank 6, and the RAISE is filed under no verdict.

## 4. Disagreements

**4 of 9 compared pairs disagree** (all against N6; N2's 3 pairs all agree):

```json
[
 {"name": "inf-otp-relay-api", "type": "API_GW", "hand_product": "N6",
  "census": {"verdict": "OUT-OF-PATTERN", "canonical": "advi-inf-otp-relay-api"},
  "hand": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-inf-otp-relay-api"},
  "axis": "canonical form only; verdict agrees",
  "why": "N6 graded before this cell's resources.json mint (system advi, citing infra/aws/terraform/inf-pipeline/api-gateway.tf:24-38 @422a3c724c); its hand answer necessarily used the pre-mint placeholder."},
 {"name": "estate-report-seam-freshness-publisher", "type": "CODEBUILD_PROJECT", "hand_product": "N6",
  "census": {"verdict": "OUT-OF-PATTERN", "canonical": "estate-report-seam-freshness-publisher-build"},
  "hand": {"verdict": "RAISE", "canonical": null},
  "axis": "verdict",
  "why": "the current registry resolves 'estate' as a systems.json PLATFORM_SUBSYSTEM row (infra/logic/registry/systems.json:171-177, owner_directive D11, owner_claim inferred, landed before this round); N6's vintage predates that row and raised on the same token the census now places."},
 {"name": "semantic-clustering-lambda-build", "type": "CODEBUILD_PROJECT", "hand_product": "N6",
  "census": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-semantic-clustering-lambda-build"},
  "hand": {"verdict": "RAISE", "canonical": null},
  "axis": "verdict",
  "why": "'semantic' is a V3/placeholder-eligible token in the current registry (R1.d fires, {system} placeholder written); N6's hand answer raised instead -- this pair is evidence the rule's V3 membership moved between the two vintages, not that grade() and the hand rule disagree on a fixed rule."},
 {"name": "ExecIncrParityFailure", "type": "CW_ALARM", "hand_product": "N6",
  "census": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-exec-incrparity-failure-alarm"},
  "hand": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-exec-incr-parity-failure-alarm"},
  "axis": "canonical form only; verdict agrees",
  "why": "the tokeniser (_res_tokens) joins 'incr'+'parity' into one piece without a separating hyphen where N6's hand answer inserted one; both sides agree the system is an unresolved {system} placeholder."}
]
```

None of the 3 N2 pairs disagree (Section 2 above).

## 5. What the census did not reach, with denominators

- **The live plane, past the stop.** 1805 of 1828 nameable live names were never judged or carded
  (judged_live 21 + carded_live 2 = 23 of 1828). The live pull returned 2190 nodes; 346 are of types the
  schema does not grade by kind and 16 are `aws_fixed` names outside the grade's domain, which is how 1828
  is reached. The run stopped at its third RAISE (after the two carded names) and did not resume, per THE
  CELL's own timebox (462 RAISE occurrences measured ahead of this point, `RAISE_POPULATION_S6.r3.md`).
- **The repo plane, entirely.** judged_repo is **0 of 1878** and carded_repo is **0** -- 0 of the Terraform
  names (473 tracked `.tf` files; 128 name attributes that are expressions are not names) and 0 of the
  source names (468 tracked files, after 2864 vendored and test files were excluded). The census judges live
  first, so the stop came before the repo plane ran.
- **Types.** 3 types (API_GW, CODEBUILD_PROJECT, CW_ALARM) carry any judged row. The live command asked for
  33 node types; the report puts 8 of them outside the grade by kind, which leaves 25 graded types, so
  **22 graded types carry no judged row at all**.
- **Hand rows left uncompared.** 42 of N2's 45 worked cases and 82 of N6's 88 rows have no census verdict to
  be set beside, because the census never judged or carded those names. Each is uncompared for the SAME
  reason: the census stopped before reaching it (or, for the 2 carded names, was deliberately not graded
  under R-29) -- not because it was checked and found not to match. No further reason is stated per row; the
  reason is uniform across all 42 + 82 = 124 uncompared hand rows.
- **The carded names.** `sentiment-query-api` and `trade-submission-api` carry no census verdict (R-29, a
  card is not a verdict). `trade-submission-api` appears in N6 (CONFORMANT); it is left uncompared here for
  the same reason every un-graded name is -- the census assigns it no verdict to set beside N6's.
- **The stop itself.** `astn-wsjft-orchestrator-errors` has no verdict in the report (a RAISE is not a
  verdict) and appears in neither N2 nor N6 (checked by string search), so it is compared against nothing.

## 6. What this record does not claim

- It says nothing about the 1805 nameable live names the census did not judge or card, or about the 1878
  repo names.
- It does not grade `astn-wsjft-orchestrator-errors`, `sentiment-query-api` or `trade-submission-api`, and
  it does not judge whether Andrew should resolve their owner questions -- that is filed as rows
  `LGIC_ENFORCE-W4-S5` (the RAISE persisting across rounds) and the new timebox row this commit files, and
  is the channel's business, not this comparison's.
- The comparison is only as current as the census report it reads. A census re-run after `astn`/`news`/
  `trade`/`sentiment` gain measured owners (or Andrew's card) would judge past this stop and produce rows
  this comparison has never seen -- and, per the timebox, that re-run is round 4's, not this cell's.
- A 9-name comparison (5 agree, 4 disagree) is not evidence that `grade()` and the hand rule agree or
  disagree in general; three of the four disagreements trace to the two products being graded at DIFFERENT
  REGISTRY VINTAGES, not to a rule conflict.
- `3.0.0_SA_CVO` grades `S6R3-AC5` at L9: whether every hand row this comparison leaves uncompared carries a
  stated reason. Section 5 above states one uniform reason for all 124 uncompared rows plus the carded
  `trade-submission-api`; this record gives no verdict on whether that reason satisfies the criterion.

```json
{
 "census": {"report": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~4/NAMING_CENSUS_REPORT.r3.md", "vintage": "Built from the estate as of 2026-09-17 14:41:29 UTC. Stitch source: stitch-codebuild built 2026-09-17T03:01:15Z.  manifest: c92a803a1057", "registry": "26623a452ff8583d", "judged_live": 21, "carded_live": 2, "live_nameable": 1828, "live": 2190, "judged_repo": 0, "carded_repo": 0, "repo": 1878, "types_with_judged_rows": 3, "totals": {"API_GW/live": {"CONFORMANT": 2, "ALIAS": 0, "OUT-OF-PATTERN": 1, "NOT-GRADED": 0}, "CODEBUILD_PROJECT/live": {"CONFORMANT": 1, "ALIAS": 0, "OUT-OF-PATTERN": 4, "NOT-GRADED": 0}, "CW_ALARM/live": {"CONFORMANT": 0, "ALIAS": 0, "OUT-OF-PATTERN": 13, "NOT-GRADED": 0}}, "stopped": {"plane": "live", "type": "CW_ALARM", "current": "astn-wsjft-orchestrator-errors", "message": "R1.c: 'astn' is an unresolved token (V2)", "in_hand_products": false}, "not_judged": [{"name": "sentiment-query-api", "plane": "live"}, {"name": "trade-submission-api", "plane": "live"}]},
 "against": {
  "N2": {"hand_population": 45, "hand_types": 26, "census_judged": 21, "compared": ["opal-portal-data-proxy-api", "opal-stitch-produce", "Inflection-SilverChain-DimConversionFailure"], "agree": 3, "uncompared_hand_rows": 42, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md@7c1e9ffb26"},
  "N6": {"hand_population": 88, "hand_types": 33, "census_judged": 21, "compared": ["inf-otp-relay-api", "opal-session-analytics-api", "estate-report-seam-freshness-publisher", "opal-drift-producer", "semantic-clustering-lambda-build", "ExecIncrParityFailure"], "agree": 2, "disagree": 4, "uncompared_hand_rows": 82, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv@388b07f486; agreement n6-compare.md@f829fdb1fc (85 of 85 discriminating agree, 0 of 88 rows disagree)"},
  "IV7": {"denominator": 10, "denominator_is": "the ranking's 10 surfaces; IV7 carries no per-name verdict", "names_graded_by_both": 0, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/TENSION_RANKING.md@3497a41c31"}
 },
 "not_reached": {"live_nameable_unjudged": 1805, "repo_unjudged": 1878, "repo_plane_ran": false, "types_requested": 33, "types_not_graded_by_kind": 8, "graded_types": 25, "graded_types_with_no_judged_row": 22, "n2_rows_uncompared": 42, "n6_rows_uncompared": 82, "uncompared_reason_uniform": "the census stopped at its third RAISE (astn-wsjft-orchestrator-errors, R1.c) before reaching any of the 124 uncompared hand rows; sentiment-query-api and trade-submission-api were carded (R-29) rather than judged", "timebox": "462 further RAISE occurrences measured ahead of this point (RAISE_POPULATION_S6.r3.md), crossing THE CELL's 25-distinct-RAISE timebox; minting/carding stops here for round 4"},
 "disagreements": [
  {"name": "inf-otp-relay-api", "type": "API_GW", "hand_product": "N6", "axis": "canonical"},
  {"name": "estate-report-seam-freshness-publisher", "type": "CODEBUILD_PROJECT", "hand_product": "N6", "axis": "verdict"},
  {"name": "semantic-clustering-lambda-build", "type": "CODEBUILD_PROJECT", "hand_product": "N6", "axis": "verdict"},
  {"name": "ExecIncrParityFailure", "type": "CW_ALARM", "hand_product": "N6", "axis": "canonical"}
 ]
}
```
