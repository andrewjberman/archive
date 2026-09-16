# LN-h-2 -- hand-grader B, result

**Worker:** `0.9.0_WK_LGIC_NAMING~8` | **TO:** `LGIC_NAMING.TO-LN-h-2` | **Branch:** `wk-lgic-naming-1-8`
**Base:** `3d671ff59cfba948d00af61d2d7145ea254f63b7` (git rev-parse HEAD before the first commit)
**Output:** `org/missions/D14/LGIC/LGIC_NAMING/deliverables/exercises/n6-grader-b.tsv` (blob `91566d3d7a`)

**Read:** GRADING_RULE.md, LEGACY_SERVED_PATHS.json, org/standards/NAMING_SCHEMA.json v1.4,
infra/logic/05_IDENTITY_SPINE.md v0.1, N6_SAMPLE.json. Nothing else was read to grade. I did not open
any other exercise file, `N3_*`, `N5_*`, the decomposition, the rule author's other files, or the source
of `check_ln.py`.

## Tally (88 of 88)

| verdict | count |
|---|---|
| OUT-OF-PATTERN | 37 |
| NOT-GRADED | 19 |
| RAISE | 18 |
| CONFORMANT | 13 |
| ALIAS | 1 |

The 19 NOT-GRADED names come from all 8 G1.2 types: API_ROUTE 3, CLOUDFRONT_DISTRIBUTION 1,
EVENT_SOURCE 3, IAM_USER 3, KMS_KEY 3, ROUTE53_RECORD 1, SERVICE_PRINCIPAL 3 and VPC_ENDPOINT 2.

## The step that raised each RAISE (18)

| step | names |
|---|---|
| R1.c, t1 in V2 | CODEBUILD_PROJECT `estate-report-seam-freshness-publisher`, `semantic-clustering-lambda-build`; EC2_INSTANCE `estate-report-runner`; ECS_TASK_DEFINITION `globgrph-comp-learns-producer`, `globgrph-nessie`, `globgrph-trino`; EVENT_RULE `FIRMSEP-s3-direct-access-bypass` (N2 gives `firmsep`) |
| R2, t2 in V2 | ECS_CLUSTER `opal-globgrph` |
| L3 -> R1.c / R2 | LOG_GROUP `/aws/codebuild/estate-report-seam-freshness-publisher` (rest raises at R1.c), `/aws/lambda/opal-globgrph-freeze-monitor` (rest raises at R2) |
| R1.f, t1 in no vocabulary | DYNAMODB_TABLE `user-permissions`; IAM_POLICY `yield-curve-artifact-write`; LAMBDA `access-anomaly-scanner`; SQS_QUEUE `partner-etl-ops-queue` |
| G2.2, AWS prefix | IAM_POLICY `AWSDataLifecycleManagerServiceRole` |
| G2.3, no leading `/` | LOG_GROUP `aws-waf-logs-opal-gateway` |
| K1, segment 1 neither source nor tier | S3Key `%s/date=%s/data.parquet` (a variable segment), `warehouse/_branch_head.main.json` |

## Where the rule had to be read, stated so a second grader can dispute it

Each of these names was placed by a clause of the rule. None was guessed, so none is a RAISE and none is
a surprise row. They are the grades whose clause is least direct.

1. **SECRET `opal/bd/credentials` -> ALIAS `opal/49f/credentials`.** S3 names only V4 tokens as a secret's
   scope, and `bd` is not V4. R3 says `bd` is refused in *every* slot, reads as the firm when no firm
   token is next to it, and is spelled in "the firm's form for the slot". V-4 lists `bd` to the firm's
   form as an alias replacement. The SHORT form of a secret scope is `49f`. On the system slot, R2 reads
   t2. Segment 1 has only one token, so t2 is either nothing or `bd` read as the firm. Neither is in V1
   or V2, so the system is `opal` on both readings.
2. **SSM_DOCUMENT `opal-cot-bd-session-fetch` -> OUT-OF-PATTERN `opal-cot-blackdiamond-session-fetch-document`.**
   R2 reads t2, which is `cot`, a firm. So the system is `opal`, as in the worked case `opal-cot-silver-run`.
   `bd` sits next to the firm token `cot`, so R3 reads it as the vendor `blackdiamond`. It stays in the
   function, because R1/R2 already fixed the system. The scope is `cot` alone, so R4 does not raise for
   two firms. `fetch` is not a kind, so R6 appends `document`.
3. **LAMBDA `opal-assets-silver-schwab` -> OUT-OF-PATTERN `opal-assets-silver-schwab-lambda`.** R2 reads t2
   only, and t2 is `assets`, which is in neither V1 nor V2. So the system is `opal`, and the later `schwab`
   is a function token. Compare SSM_DOCUMENT `opal-schwab-rps-convert`, where t2 is `schwab`: there `opal`
   is a null prefix and the canonical form is `schwab-rps-convert-document`.

## Criteria

- `H2-AC1` -- `check_ln.py h2-graded`: `SAMPLE: 88 (85 discriminating + 3 overlap)  GRADED WITH A VERDICT: 88  MISSING: []`, `VERDICT: PASS-ALL-GRADED`, rc 0.
- `H2-AC2` -- `check_ln.py h2-base`: `BASE: 3d671ff59cfba948d00af61d2d7145ea254f63b7`, `VERDICT: PASS-BASE-RECORDED`, rc 0.

Surprise rows filed: none.
