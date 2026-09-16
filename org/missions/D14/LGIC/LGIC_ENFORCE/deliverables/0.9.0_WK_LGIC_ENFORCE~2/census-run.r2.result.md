# EN-s-1 re-run (round 2) -- result

**Order:** `org/missions/D14/LGIC/LGIC_ENFORCE/task-orders/LGIC_ENFORCE.TO-EN-s-1-r2.census-run.md` @`4f9a9eb3f3`
**Worker:** `0.9.0_WK_LGIC_ENFORCE~2`, worktree `/c/Users/AndrewBerman/Desktop/ajb_workspace/.worktrees/wk-lgic-enforce-2d-2`, branch `wk-lgic-enforce-2d-2`, base `CLOUD` @`c8e9d02213`
**Verdict:** the order STAYS PENDING. 3 of 5 mechanical criteria PASS; S1R-AC1 and S1R-AC2 FAIL BY MEASUREMENT, which the cell names in advance as a result rather than a defect.

## What was run

```
python lib/opal_naming.py census --live --repo --report org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/NAMING_CENSUS_REPORT.md
```

Verbatim, unchanged, on round 1's code (`lib/opal_naming.py` @`39cbad4214`, untouched -- the cell says "The code is round 1's; do not change it"). rc=3.

```
CENSUS LIVE: 2176 node(s) at VINTAGE Built from the estate as of 2026-09-16 05:57:28 UTC. Stitch source: stitch-codebuild built 2026-09-16T03:01:17Z.  manifest: b2849dcf2cac; 339 of NOT GRADED types, 16 aws_fixed; 1821 to judge
CENSUS REPO: 1878 name(s) from 472 .tf file(s) and 468 source file(s); 2864 vendored file(s) excluded; 121 Terraform name expression(s) and 0 template(s) not names; 0 file(s) unparsed
CENSUS RAISE live API_GW sentiment-query-api -- R1.f: 'sentiment' is in no vocabulary; no registry row resolves it
CENSUS OUT-OF-PATTERN live API_GW inf-otp-relay-api -> {system}-inf-otp-relay-api
CENSUS CONFORMANT live API_GW opal-portal-data-proxy-api -> opal-portal-data-proxy-api
CENSUS CONFORMANT live API_GW opal-session-analytics-api -> opal-session-analytics-api
CENSUS REPORT org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/NAMING_CENSUS_REPORT.md
CENSUS: STOPPED on the first RAISE after 3 judged: live API_GW 'sentiment-query-api'
```

## Criteria

| id | status | deciding line | denominator |
|---|---|---|---|
| S1R-AC1 | **FAIL** | `VERDICT: FAIL-PLANES` (rc=1) | 1 of 2 planes carry judged rows; repo 0 of 1878 names reached |
| S1R-AC2 | **FAIL** | `VERDICT: FAIL-NOT-ALL-JUDGED` (rc=1) | 3 of 1821 nameable live names judged |
| S1R-AC3 | PASS | `VERDICT: PASS-ROW-SHAPE` (rc=0) | 3 of 3 rows, 0 malformed |
| S1R-AC4 | PASS | `VERDICT: PASS-RAISE-STOPS` (rc=0) | boolean on 1 of 1 fixture line; corroborated on the real run (rc=3 + the RAISE string) |
| S1R-AC5 | PASS | `REPORT registry@254d4e9ece847acb  HEAD registry@254d4e9ece847acb` / `VERDICT: PASS-REPORT-AT-HEAD-REGISTRY` (rc=0) | 1 of 1 comparison, 16 of 16 hex characters equal |

## Why the two FAILs are the anticipated branch, not a defect

The cell states it in terms: *"If a class (d) or undecided group remains, the run stops on it: S1R-AC1 and S1R-AC2 then FAIL by measurement, and the order stays pending. That is a result, not a defect (decomposition v2 s.0b)."*

The run stopped on live `API_GW sentiment-query-api`. `token:sentiment` is class (d) by `EN-r-2`'s own ruling -- `REGISTRY_TOKEN_CLASSES.md` @`72d636db4f`, `why` entry: *"token:sentiment: K1 rule gap (mixed with R1.f): 'sentiment/keyword-sentiments.json' fails K1 the same way as cache; mixed group stays class (d)."* That document classes **46** groups as (d) and leaves **6** undecided out of a printed **152**-group union, so a stop before exhaustion was the expected branch when the cell was cut. `EN-r-5`'s `gateway` row did its part: the three names that WERE judged are all `API_GW` and none raises.

`census()` judges the live plane before the repo plane (`lib/opal_naming.py` @`39cbad4214`, docstring: *"The live plane is judged first, then the repo plane"*), which is why the repo plane's 1878 collected names never reached the judge and S1R-AC1's `PLANES: ['live']` follows mechanically from the same single stop.

No remedy is available inside this order: clearing a class (d) group means editing `infra/logic/registry/`, which this order's `<paths>` does not grant, and altering the census to skip a RAISE is expressly forbidden by the cell.

## Controls

- **Mutant (S1R-AC5):** the same limb, run against round 1's report bytes from `f64b6f35cb` (registry@`50e4fabd1cb6a150`), by loading `check_en_r2.py` as a module and redirecting only its in-memory `REPORT` constant -- the file's bytes were not touched. Positive control first: the round-1 bytes read clean, 4045 chars, carrying `at registry@50e4fabd1cb6a150`. The limb then printed `REPORT registry@50e4fabd1cb6a150  HEAD registry@254d4e9ece847acb` / `VERDICT: FAIL-REPORT-STALE`, rc=1. **FIRED-AS-EXPECTED.**
- **Determinism:** all five criterion invocations re-run against the same committed report; 5 of 5 VERDICT lines identical. The census run itself is deliberately NOT claimed deterministic -- its live plane is a fresh `comp-find --corpus aws` pull (2148 nodes at 2026-09-15 00:57:50 UTC in round 1 against 2176 at 2026-09-16 05:57:28 UTC here).
- **Not claimed:** `check_en_r2.py selftest-negative` was attempted as a supplementary control and hit rc=124 at its `timeout 120` bound with zero output. It is the whole project's negative suite, not this cell's, and is recorded rather than retried.

## Vintage

The issuance pinned this run to a registry that would not move under it. Re-grounded rather than assumed: `git log -1 -- lib/opal_naming.py` returns `39cbad4214` (EN-r-6's drain), contained in this worktree's base `c8e9d02213`. S1R-AC5's PASS is the measured confirmation that the report was written at exactly HEAD's registry, `254d4e9ece847acb`.

## Rows filed

- `LGIC_ENFORCE-W2-S10` -- OBSERVATION, INERT. The only OUT-OF-PATTERN row the run produced carries a LITERAL unfilled `{system}`: `grade('inf-otp-relay-api','API_GW')` returns `{system}-inf-otp-relay-api` while its registered sibling `grade('inf-otp-relay-lambda-role','IAM_ROLE')` returns `advi-inf-otp-relay-lambda-role`. `resources.json` @`b15ed01ee6` is keyed by (name, type) and 18 of `RESOURCE_GAPS.json`'s 48 gaps have no (name, type) row. Filed, not chased -- the registry is outside this order's grant, and whether that gap count is itself a defect is `EN-r-4`'s own criterion.

## Proof

`org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/LGIC_ENFORCE.TO-EN-s-1-r2.census-run.proof_of_spec.json` -- `proof-of-spec-check.py` **rc=0, VALID**. The first run was rc=1 INVALID and is recorded in the instance's own `compiler_tools`: an `introduces` token round 1's report already carried, refused correctly by the content limb, replaced with one absent at the pin's parent.

**A VALID instance is not a met order.** `<status>` is NOT flipped and stays `pending`.
