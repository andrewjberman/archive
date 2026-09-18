# NAMING_CENSUS_COMPARISON -- census mode, the comparison, round 4 (EN-s-25-r4, "the run to the end")

**Worker:** `0.9.0_WK_LGIC_ENFORCE~2` | **TO:** `LGIC_ENFORCE.TO-EN-s-25-r4` | **Branch:** `wk-lgic-enforce-4-2`,
cut from CLOUD @`a7ae7f5e01`. This reads `NAMING_CENSUS_REPORT.r4.md` (same worker, same worktree, run
`python lib/opal_naming.py census --live --repo --not-judged
org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~1/NOT_JUDGED_R4.json --report
.../NAMING_CENSUS_REPORT.r4.md`, registry@`4f192e91bd64ee70`, live/AWS-corpus vintage `Built from the estate
as of 2026-09-17 18:16:22 UTC. Stitch source: stitch-codebuild built 2026-09-17T03:01:15Z.  manifest:
514495fde115`).

This file sets round 4's census report's totals beside the two hand products the order names -- LGIC_NAMING's
N2 worked cases and N6 grader rows -- over the REAL hand populations (N2 45, N6 88). It grades no name itself.

## 1. The census, this round

Unlike round 3 (stopped on its third RAISE, 21 of 1828 live names judged, 0 of 1878 repo names judged), round
4's run reads **COMPLETE: every item was judged and no name raised.** `judged_live 1690 + carded_live 136 ==
live_nameable 1826`; `judged_repo 1547 + carded_repo 331 == repo 1878`; `stopped: null`. The `--not-judged`
input was slot ~1's `NOT_JUDGED_R4.json` (348 entries; both names round 3 carded under `NOT_JUDGED_S6.r3.json`,
`sentiment-query-api` and `trade-submission-api`, are already members of that 348 -- carried forward, not
dropped, and not re-added).

**AC1 and AC2 (S25R4-AC1, S25R4-AC2)**: PASS by this arithmetic, `stopped` null, and the live plane's
`Built from the estate as of ...` vintage stated -- measured directly against `check_en_r4.py
s25-live-complete` / `s25-repo-complete` (own report below).

**AC3 (S25R4-AC3, "no placeholder reaches a report row", W2-S10's rule)**: **FAILS by measurement.**
**1411 of the 3237 judged rows** carry a literal `{` in `canonical` (`{system}`, `{scope}`, `{cadence}`, etc.),
dominated by `IAM_POLICY` (live 309 + repo 266), `S3Key` repo (106), `LOG_GROUP` live (87), `EVENT_RULE`
(live 84 + repo 76), `LAMBDA` live (71), `IAM_ROLE` (live 56 + repo 57), `SECRET` (live 33 + repo 34),
`EC2_INSTANCE` live (21), `CW_ALARM` (live 20 + repo 18), `S3_BUCKET` repo (20), and 20+ further types at
smaller counts. This is a REAL result, not a run defect: `grade()` synthesizes a `{system}`/`{scope}`/
`{cadence}` placeholder whenever a name's system/scope/cadence token is placeholder-eligible (V3) rather than
unresolved outright (V2, which RAISEs) -- see round 3's own comparison, Section 4, for the same mechanism on
a smaller sample. Round 4's campaign cells (`EN-c-23-r4`, `EN-h-24-r4`) closed the **RAISE population**
(`RAISE_POPULATION_S6.r3.md`'s 351 triples) by carding or minting so the run would not stop -- they did not,
and were not asked to, resolve the much larger **placeholder population**, which never raises and so never
appeared on that list. `EN-h-24-r4` minted/carded exactly the 8 placeholder rows round 3's early-stopped
21-row report exposed; round 3 never judged the other ~3200 rows round 4 now reaches, so the other ~1400
placeholder rows were invisible to round 4's own campaign cells at cut time. **The registry is not this
worker's grant** (BOUNDS), so this criterion is reported FAIL with its measured evidence and surprise row
`LGIC_ENFORCE-W2-S<next>` files it; nothing is minted or carded by this worker.

## 2. Name by name: every name graded by both

The match is on `(name, type)`, exact byte match required for AGREE (round 2/3's rule, unchanged).

**Against N2: 34 of 45 worked cases graded by both, 33 agree, 1 disagrees.**

Compared names (34): `mdpf-gold-lambda`, `inf-silver-chain`, `inf-api-eclipse`, `etfs-canon-fanin-role`,
`bd-49f-runner-role`, `FredMacroIngestionLambdaRole`, `irpt-directory-policy`, `s3-etfs-read`,
`opal-data-49financial#policy`, `mdpf-daily-runner-profile`, `etfs-reports-reporter-sg`,
`opal-portal-data-proxy-api`, `irpt-jobs`, `irpt-export-dlq`, `etfs-reports-alerts`,
`Inflection-SilverChain-DimConversionFailure`, `pandas-pyarrow-layer`, `mdpf-daily-runner`,
`opal-stitch-produce`, `opal-cot-silver-run`, `globgrph-serving`, `YangDataPipeline`, `opal-gateway`,
`opal-globgrph`, `etfs-netassets-daily`, `bd-49f-session-complete`, `wsb-49f-model-aua-pull-daily`,
`mdpf-accrual-bridge-daily`, `/aws/lambda/mdpf-gold-lambda`, `opal-data-bd`,
`opal-cloudtrail-logs-313476888478`, `opal-data-cot`, `blackdiamond/49f/credentials`, `inf/otp-relay/token`.

The one disagreement:

| name | type | census | N2 | axis |
|---|---|---|---|---|
| `Inflection-SilverChain-DimConversionFailure` | CW_ALARM | OUT-OF-PATTERN `advi-inf-silver-chain-dim-conversion-failure-alarm` | OUT-OF-PATTERN `{system}-inf-silver-chain-dim-conversion-failure-alarm` | canonical only (verdict agrees) -- the current registry now resolves `inf` to system `advi` (a mint since N2's vintage); N2's hand answer necessarily used the pre-mint placeholder. |

**Against N6: 57 of 88 grader rows graded by both, 40 agree, 17 disagree.**

17 disagreements (full detail in the fenced json, Section 5):

| name | type | census verdict/canonical | N6 verdict/canonical | axis |
|---|---|---|---|---|
| `inf-otp-relay-api` | API_GW | OUT-OF-PATTERN `advi-inf-otp-relay-api` | OUT-OF-PATTERN `{system}-inf-otp-relay-api` | canonical (registry mint since N6's vintage) |
| `estate-report-seam-freshness-publisher` | CODEBUILD_PROJECT | OUT-OF-PATTERN `...-build` | RAISE | verdict (`estate` now resolves) |
| `ExecIncrParityFailure` | CW_ALARM | OUT-OF-PATTERN `{system}-exec-incrparity-failure-alarm` | OUT-OF-PATTERN `{system}-exec-incr-parity-failure-alarm` | canonical (tokeniser hyphenation) |
| `user-permissions` | DYNAMODB_TABLE | OUT-OF-PATTERN `{system}-user-permissions-table` | RAISE | verdict (now placeholder-eligible, not unresolved) |
| `estate-report-runner` | EC2_INSTANCE | CONFORMANT | RAISE | verdict (`estate` now resolves) |
| `globgrph-comp-learns-producer` | ECS_TASK_DEFINITION | OUT-OF-PATTERN `...-task` | RAISE | verdict |
| `globgrph-nessie` | ECS_TASK_DEFINITION | OUT-OF-PATTERN `...-task` | RAISE | verdict |
| `globgrph-trino` | ECS_TASK_DEFINITION | OUT-OF-PATTERN `...-task` | RAISE | verdict |
| `FIRMSEP-s3-direct-access-bypass` | EVENT_RULE | OUT-OF-PATTERN `...-{cadence}` | RAISE | verdict |
| `yield-curve-artifact-write` | IAM_POLICY | OUT-OF-PATTERN `{system}-...-policy` | RAISE | verdict |
| `access-anomaly-scanner` | LAMBDA | OUT-OF-PATTERN `{system}-...-lambda` | RAISE | verdict |
| `/aws/codebuild/estate-report-seam-freshness-publisher` | LOG_GROUP | OUT-OF-PATTERN `...-build` | RAISE | verdict |
| `/aws/lambda/opal-globgrph-freeze-monitor` | LOG_GROUP | OUT-OF-PATTERN `.../globgrph-freeze-monitor-lambda` | RAISE | verdict |
| `partner-etl-ops-queue` | SQS_QUEUE | OUT-OF-PATTERN `{system}-...` | RAISE | verdict |
| `opal-cot-bd-session-fetch` | SSM_DOCUMENT | OUT-OF-PATTERN `opal-cot-bd-session-fetch-document` | OUT-OF-PATTERN `opal-cot-blackdiamond-session-fetch-document` | canonical (spelling: `bd` vs `blackdiamond`) |
| `opal-globgrph` | ECS_CLUSTER | OUT-OF-PATTERN `globgrph-cluster` | RAISE | verdict |
| `opal-gateway` | LOAD_BALANCER | OUT-OF-PATTERN `gateway-lb` | OUT-OF-PATTERN `opal-gateway-lb` | canonical |

15 of 17 disagreements are the SAME shape: N6's hand answer RAISEd at its own (earlier) vintage on a token
the current registry now resolves or places a `{...}` placeholder for -- a registry-growth effect, not a
rule conflict (the same effect round 3's comparison Section 4 measured on 3 of 4 pairs there). The other 2
(`ExecIncrParityFailure`, `opal-cot-bd-session-fetch`) are tokeniser/spelling artifacts on the canonical form
only, verdict agrees on both.

**Coverage.** 91 of the 133 hand rows (34 N2 + 57 N6, with 0 names shared between the two products in this
comparison) are graded by the census; 42 are not (11 N2 + 31 N6) -- Section 3. **The split of those 42 by
reason: NOT-GRADED-TYPE 20 + AWS_FIXED-EXCLUDED 2 + CARDED 10 + HAND-SPECIMEN-ABSENT 10 = 42**, so the next
reader can check the parts against the total without re-deriving them from the per-row table.

## 3. What the census did not reach, and every uncompared row's reason

Unlike round 3 (stopped early, 124 uncompared for reasons that were uniformly "the run had not reached
this point yet"), round 4's run is COMPLETE on both planes, so every uncompared hand row now has one of
FOUR distinct, individually-verified reasons -- none of them "the run stopped before it got there":

- **NOT-GRADED-TYPE** (20 rows): the hand row's type is in `_vocab().not_graded`
  (`API_ROUTE`, `CLOUDFRONT_DISTRIBUTION`, `EVENT_SOURCE`, `IAM_USER`, `KMS_KEY`, `ROUTE53_RECORD`,
  `SERVICE_PRINCIPAL`, `VPC_ENDPOINT`) -- the census never turns a node of this type into an item, on
  either plane, so it can carry no verdict to compare (matches round 3's report: 346 live nodes of these 8
  types were excluded the same way).
- **AWS_FIXED-EXCLUDED** (2 rows): `NAMING_SCHEMA.json`'s `aws_fixed` rule (`opal_naming._aws_fixed`) puts
  this exact name outside the grade's domain even though its TYPE is graded -- `default` (SECURITY_GROUP,
  by-name) and `aws-waf-logs-opal-gateway` (LOG_GROUP, by-name prefix `aws-waf-logs-`), each confirmed by a
  direct `_aws_fixed()` call against `NAMING_SCHEMA.json` at this commit.
- **CARDED** (10 rows): the name is a member of slot ~1's `NOT_JUDGED_R4.json` (R-29) -- carded rather than
  graded, so it carries no verdict by design, not by gap.
- **HAND-SPECIMEN-ABSENT** (10 rows): the type IS graded and the name is NOT `aws_fixed`-excluded, but the
  literal string is not present among the 2188 live AWS nodes this vintage's pull scanned nor among the
  repo's tracked `.tf`/source literals -- these are worked/exercise names the hand products invented to
  demonstrate a rule (two RAISE specimens explicitly flagged `"specimen": true` in `GRADING_RULE.md`, one
  IAM_POLICY RAISE specimen, and 8 fabricated S3Key paths in N2 alone) rather than names of resources
  currently in the estate.

Full per-row table (11 N2 + 31 N6 = 42 rows, every one individually re-derived against `_vocab().not_graded`,
`opal_naming._aws_fixed()` at this commit, and `NOT_JUDGED_R4.json` -- no row's reason is inferred or assumed):

| hand product | name | type | hand verdict | reason |
|---|---|---|---|---|
| N2 | `mdpf-lambda-lambda` | LAMBDA | RAISE (specimen) | HAND-SPECIMEN-ABSENT |
| N2 | `orion-orion-lambda-lambda` | LAMBDA | RAISE (specimen) | HAND-SPECIMEN-ABSENT |
| N2 | `default` | SECURITY_GROUP | NOT-GRADED | AWS_FIXED-EXCLUDED |
| N2 | `platinum/firm/header_metrics.json` | S3Key | OUT-OF-PATTERN | HAND-SPECIMEN-ABSENT |
| N2 | `code/gold/*` | S3Key | OUT-OF-PATTERN | HAND-SPECIMEN-ABSENT |
| N2 | `schwab/08335338/silver/fact_rps/` | S3Key | CONFORMANT | HAND-SPECIMEN-ABSENT |
| N2 | `mdpf/global/code/gold/mdpf-accrual-bridge.tar.gz` | S3Key | CONFORMANT | HAND-SPECIMEN-ABSENT |
| N2 | `advi/49financial/platinum/advisors/advisor_id=A123/positions.json` | S3Key | CONFORMANT | HAND-SPECIMEN-ABSENT |
| N2 | `advi/49financial/platinum/firm/fee_efficiency.json` | S3Key | CONFORMANT | HAND-SPECIMEN-ABSENT |
| N2 | `advi/49financial/platinum/firm/top_holdings.json` | S3Key | OUT-OF-PATTERN | HAND-SPECIMEN-ABSENT |
| N2 | `4ba4753c-98f4-47c0-9a47-6dacaa1b6370` | KMS_KEY | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `trade-submission-api` | API_GW | CONFORMANT | CARDED |
| N6 | `$default` | API_ROUTE | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `POST /api/scoped/tickets/{ticketId}/complete` | API_ROUTE | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `valueIsUnsafe` | API_ROUTE | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `E1DHJH4Y1W8YC2` | CLOUDFRONT_DISTRIBUTION | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `semantic-clustering-lambda-build` | CODEBUILD_PROJECT | RAISE | CARDED |
| N6 | `astn-wsjft-scraper` | EC2_INSTANCE | OUT-OF-PATTERN | CARDED |
| N6 | `GetObject` | EVENT_SOURCE | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `cron(15 17 * * ? *)` | EVENT_SOURCE | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `{'anything-but': [...]}` | EVENT_SOURCE | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `AWSDataLifecycleManagerServiceRole` | IAM_POLICY | RAISE | HAND-SPECIMEN-ABSENT |
| N6 | `Andrew_Berman` | IAM_USER | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `github-actions-portal` | IAM_USER | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `token.actions.githubusercontent.com` | IAM_USER | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `astn-wsjft-scraper-profile` | INSTANCE_PROFILE | CONFORMANT | CARDED |
| N6 | `0a55c5f0-3096-449b-bc3a-c363f70e2f12` | KMS_KEY | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `86324aae-521d-4b32-849d-d857da2e65a1` | KMS_KEY | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `e56eea8d-db4c-411a-adee-29bf3941435e` | KMS_KEY | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `aws-waf-logs-opal-gateway` | LOG_GROUP | RAISE | AWS_FIXED-EXCLUDED |
| N6 | `mcp.opalinvest.dev` | ROUTE53_RECORD | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `%s/date=%s/data.parquet` | S3Key | RAISE | CARDED |
| N6 | `warehouse/_branch_head.main.json` | S3Key | RAISE | CARDED |
| N6 | `opal-data-news-av` | S3_BUCKET | OUT-OF-PATTERN | CARDED |
| N6 | `astn-wsjft-scraper-sg` | SECURITY_GROUP | CONFORMANT | CARDED |
| N6 | `E139998VWH0PD` | SERVICE_PRINCIPAL | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `edgelambda.amazonaws.com` | SERVICE_PRINCIPAL | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `vpc-flow-logs.amazonaws.com` | SERVICE_PRINCIPAL | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `astn-wsjft-alerts` | SNS_TOPIC | CONFORMANT | CARDED |
| N6 | `trade-pipeline-ses-complaints` | SNS_TOPIC | OUT-OF-PATTERN | CARDED |
| N6 | `com.amazonaws.us-east-1.dynamodb` | VPC_ENDPOINT | NOT-GRADED | NOT-GRADED-TYPE |
| N6 | `com.amazonaws.us-east-1.s3` | VPC_ENDPOINT | NOT-GRADED | NOT-GRADED-TYPE |

## 4. What this record does not claim

- It does not judge whether AC3's FAIL should block FWD-5's closure -- that is `1.0.0_SA_CTO`'s round-4
  analysis, not this worker's; this worker's grant excludes `infra/logic/registry/`.
- It does not re-grade any of the 91 compared names by a different rule; AGREE/DISAGREE is the byte-exact
  match round 2/3 established, unchanged here.
- The `HAND-SPECIMEN-ABSENT` reason states that the literal string is absent from THIS vintage's live pull
  and THIS commit's tracked repo files; it does not claim the name was never real or will never exist.
- `3.0.0_SA_CVO` grades `S25R4-AC4` at L9: whether every hand row this comparison leaves uncompared carries
  a stated reason (Section 3 gives one of four measured reasons, individually re-derived, for each of the
  42 uncompared rows), and whether the live plane's stated vintage is the one the run actually read (Section
  1 and the report's own added paragraph: a fresh `comp-find --corpus aws --name . S3_BUCKET --limit 1` read
  by this worker prints the byte-identical `VINTAGE:` line).

```json
{
 "census": {"report": "org/missions/D14/LGIC/LGIC_ENFORCE/deliverables/0.9.0_WK_LGIC_ENFORCE~2/NAMING_CENSUS_REPORT.r4.md", "vintage": "Built from the estate as of 2026-09-17 18:16:22 UTC. Stitch source: stitch-codebuild built 2026-09-17T03:01:15Z.  manifest: 514495fde115", "registry": "4f192e91bd64ee70", "judged_live": 1690, "carded_live": 136, "live_nameable": 1826, "live": 2188, "judged_repo": 1547, "carded_repo": 331, "repo": 1878, "stopped": null, "not_judged_count": 348, "placeholder_rows": 1411, "placeholder_rows_by_plane_type": {"live/IAM_POLICY": 309, "repo/IAM_POLICY": 266, "repo/S3Key": 106, "live/LOG_GROUP": 87, "live/EVENT_RULE": 84, "repo/EVENT_RULE": 76, "live/LAMBDA": 71, "repo/IAM_ROLE": 57, "live/IAM_ROLE": 56, "repo/SECRET": 34, "live/SECRET": 33, "live/EC2_INSTANCE": 21, "live/CW_ALARM": 20, "repo/S3_BUCKET": 20, "repo/CW_ALARM": 18}},
 "against": {
  "N2": {"hand_population": 45, "compared": 34, "agree": 33, "disagree": 1, "uncompared_hand_rows": 11, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/GRADING_RULE.md@7c1e9ffb26"},
  "N6": {"hand_population": 88, "compared": 57, "agree": 40, "disagree": 17, "uncompared_hand_rows": 31, "source": "org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-a.tsv@388b07f486"}
 },
 "uncompared_reasons": {"NOT-GRADED-TYPE": 20, "AWS_FIXED-EXCLUDED": 2, "CARDED": 10, "HAND-SPECIMEN-ABSENT": 10, "total": 42},
 "disagreements": [
  {"name": "Inflection-SilverChain-DimConversionFailure", "type": "CW_ALARM", "hand_product": "N2", "axis": "canonical", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "advi-inf-silver-chain-dim-conversion-failure-alarm"}, "hand": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-inf-silver-chain-dim-conversion-failure-alarm"}},
  {"name": "inf-otp-relay-api", "type": "API_GW", "hand_product": "N6", "axis": "canonical", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "advi-inf-otp-relay-api"}, "hand": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-inf-otp-relay-api"}},
  {"name": "estate-report-seam-freshness-publisher", "type": "CODEBUILD_PROJECT", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "estate-report-seam-freshness-publisher-build"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "ExecIncrParityFailure", "type": "CW_ALARM", "hand_product": "N6", "axis": "canonical", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-exec-incrparity-failure-alarm"}, "hand": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-exec-incr-parity-failure-alarm"}},
  {"name": "user-permissions", "type": "DYNAMODB_TABLE", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-user-permissions-table"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "estate-report-runner", "type": "EC2_INSTANCE", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "CONFORMANT", "canonical": "estate-report-runner"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "globgrph-comp-learns-producer", "type": "ECS_TASK_DEFINITION", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "globgrph-comp-learns-producer-task"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "globgrph-nessie", "type": "ECS_TASK_DEFINITION", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "globgrph-nessie-task"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "globgrph-trino", "type": "ECS_TASK_DEFINITION", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "globgrph-trino-task"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "FIRMSEP-s3-direct-access-bypass", "type": "EVENT_RULE", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "firmsep-s3-direct-access-bypass-{cadence}"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "yield-curve-artifact-write", "type": "IAM_POLICY", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-yield-curve-artifact-write-policy"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "access-anomaly-scanner", "type": "LAMBDA", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-access-anomaly-scanner-lambda"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "/aws/codebuild/estate-report-seam-freshness-publisher", "type": "LOG_GROUP", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "/aws/codebuild/estate-report-seam-freshness-publisher-build"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "/aws/lambda/opal-globgrph-freeze-monitor", "type": "LOG_GROUP", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "/aws/lambda/globgrph-freeze-monitor-lambda"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "partner-etl-ops-queue", "type": "SQS_QUEUE", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "{system}-partner-etl-ops-queue"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "opal-cot-bd-session-fetch", "type": "SSM_DOCUMENT", "hand_product": "N6", "axis": "canonical", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "opal-cot-bd-session-fetch-document"}, "hand": {"verdict": "OUT-OF-PATTERN", "canonical": "opal-cot-blackdiamond-session-fetch-document"}},
  {"name": "opal-globgrph", "type": "ECS_CLUSTER", "hand_product": "N6", "axis": "verdict", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "globgrph-cluster"}, "hand": {"verdict": "RAISE", "canonical": null}},
  {"name": "opal-gateway", "type": "LOAD_BALANCER", "hand_product": "N6", "axis": "canonical", "census": {"verdict": "OUT-OF-PATTERN", "canonical": "gateway-lb"}, "hand": {"verdict": "OUT-OF-PATTERN", "canonical": "opal-gateway-lb"}}
 ]
}
```
