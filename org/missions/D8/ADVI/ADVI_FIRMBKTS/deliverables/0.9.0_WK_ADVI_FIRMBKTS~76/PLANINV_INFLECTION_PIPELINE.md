# FB-k-1 -- Inflection: what runs against the legacy home (PLANINV, read-only)

Record: `PLANINV_INFLECTION_PIPELINE.json` (same folder). Sweeps 2026-10-13 21:31Z to 22:10Z, read-only. Firm: inflection. Legacy home: `opal-data-inf`. Destination named in PRD v1.5: `opal-data-inflection`.

## Totals

- 54 functions by kind: 33 lambda (incl. 2 bd notification Lambdas), 9 rule, 7 script, 2 edge (Lambda@Edge router, CloudFront distribution), 2 other (gold-runner EC2, Step Functions machine), 1 service (ECS cluster).
- `legacy_touch` true: 34 of 54. Measured claims: 50 rows. Held: 2 (L02, L03 bucket resolution not evaluated). Absent: 2 (L37, L38 notification Lambdas whose source was not read).
- Premise gap, filed as surprise `ADVI_FIRMBKTS-D1-W76-S1` (OBSERVATION, INERT): `opal-data-bd` holds no Inflection-scope object (census 0 tokens; mapping 0 of 247 bd rows).

## Denominators

| sweep | denominator |
|---|---|
| EventBridge rules listed | 156 (two pages, counted client-side) |
| rules with targets read (name, pattern or description names an Inflection token) | 52 of 156 |
| rules whose EventPattern names opal-data-inf (graph band) | 7 of 157 EVENT_RULE nodes |
| Scheduler schedules (default group; 1 group) | 34 read, 34 targets read |
| Lambda configurations read | 51 |
| S3 notification configs (opal-data-inf 2 Lambda, opal-data-bd 2, opal-data-cot 0) | 3 buckets |
| Step Functions state machines | 1 (definition byte-scanned) |
| ECS cluster / services / active task definitions | 1 / 3 / 9 (all described) |
| CloudFront distributions / origins / behaviors+default | 1 / 7 / 30 |
| Lambda@Edge source files read | 2 |
| Repository files matching opal-data-inf (data/) | 169 (complete) |
| Repository files matching opal-data-inf (infra/) | 200 (capped; lower bound) |
| data/inf/scripts/gold, data/inf/manual_api, data/inf/scripts/silver | 72, 44, 14 |
| infra/aws/lambda/inf-pipeline tree | 54 (19 lambda_function.py with an S3 call) |
| census buckets / Inflection tokens in opal-data-bd | 3 / 0 |
| mapping_v4 rows (inf 3,127; bd 247; cot 77; total 3,451) | 0 bd rows in Inflection scope |

## Rows (id, kind, legacy, claim, access in brief)

| id | kind | legacy | claim | access |
|---|---|---|---|---|
| R01-R09 | rule | no | measured | watches on gold/meta, bronze complete, otp, served header, release, direct GetObject, EC2 stop; targets carry the access |
| L01 mdpf-feeder-trigger | lambda | yes | measured | head gate gold/eclipse/<date>/_meta/gold_complete.json |
| L02 mdpf-gold-lambda | lambda | no | held | writer role named, bucket not read |
| L03 irpt-inf-holdings-performance | lambda | no | held | registry-resolved bucket, not evaluated |
| L04 opal-assets-ingest-mirror (firm=inf) | lambda | yes | measured | reads bronze/{assets,positions,transactions,performance,eclipse}/ flat; writes assets monolith |
| L05-L13 inf-accounts, api-assets, api-eclipse, api-positions, api-reps, api-txn, billing, bronze-complete-emitter, bronze-trigger | lambda | yes | measured | silver _silver_complete sentinels; bronze orion-api; eclipse_qa; _BRONZE_COMPLETE marker; orion/bronze-trigger-mode |
| L14 inf-assets-trigger | lambda | no | measured | starts gold runner; no S3 call of its own |
| L15 inf-silver-chain | lambda | yes | measured | silver/api_dims chain; _chain_summary |
| L16 inf-gold-trigger | lambda | yes | measured | gold/dispatch-lock.json r/w; starts runner; daily path (rules DISABLED) |
| L17 inf-silver-aggregator | lambda | yes | measured | silver sentinels; writes _AGGREGATOR_FIRED.json; fires L16 |
| L18 inf-nna-partition-checker | lambda | yes | measured | platinum/firm/advisor_nna_canonical.json read; metric |
| L19 inf-otp-relay | lambda | yes | measured | otp/state.json r/w |
| L20-L22 inf-performance, inf-tax, inf-unified-account-dim | lambda | yes | measured | bronze head checks; silver sentinels |
| L23 inf-jwt-trigger | lambda | yes | measured | writes orion/jwt/trigger-mode.json only; starts exporter |
| L24 inf-etf-ownership-daily | lambda | no | measured | opal-data-assets and opal-data-etfs only; INF_BUCKET unused |
| L25 inf-portal-publisher | lambda | yes | measured | reads gold and silver; writes platinum/firm/*; CDN invalidation |
| L26 inf-portal-advisor-publisher | lambda | yes | measured | reads gold/views; writes OUTPUT_BUCKET keys (template held) |
| L27 inf-gold-freshness-guard | lambda | yes | measured | reads prohibited key gold/meta/pipeline-complete.json; invoker not identified |
| L28-L29 inf-ec2-launch-monitor, inf-ec2-retry-launch | lambda | no | measured | no S3 call; EC2 restart |
| L30 opal-inf-served-guard | lambda | yes | measured | reads platinum/firm/header_metrics.json; quarantine |
| L31 opal-inf-value-parity | lambda | yes | measured | reads served header and silver anchor; SNS |
| L32 inf gold-layer runner (EC2) | other | yes | measured | code/* sync; dispatch lock; telemetry; gold artifacts |
| L33 shared-advisor-router (Lambda@Edge) | edge | yes | measured | inflection firm maps to opal-data-inf |
| L34 portal CloudFront distribution | edge | no | measured | S3-opal-data-inf origin configured, no behavior routes to it |
| L35 YangDataPipeline | other | no | measured | definition byte scan: zero hits |
| L36 opal-globgrph ECS | service | no | measured | 9 task definitions byte scan: zero hits |
| L37 bd-silver-merge, L38 bd-gold-trigger | lambda | no | absent | opal-data-bd notifications; source not read |
| S01 orion-gold-dispatch.sh | script | yes | measured | code/* sync; lock; telemetry; artifact markers |
| S02 INF_D_00.portal_aggregates.py | script | yes | measured | reads gold and silver; writes platinum/firm clients_tab, dimensions |
| S03 INF_C_01.canonical_nna.py | script | yes | measured | reads silver transactions and gap manifest; no writes detected |
| S04 INF_build_canonical_prices.py | script | yes | measured | get and upload to opal-data-inf; keys dynamic (held) |
| S05 INF_run_c_chain.py | script | yes | measured | head and get on opal-data-inf (AST); writes local only |
| S06 bronze/orchestrator.py | script | yes | measured | reads orion/jwt/current.json (key only), writes bronze/orion-api |
| S07 build_mdpf_wsc_inflection_feeder.py | script | yes | inferred | reads gold client_performance; dynamic gold/eclipse prefix |

## Not read

- 104 of 156 rules: targets not read; none of their EventPatterns names opal-data-inf.
- 31 of 34 schedules: non-Inflection units, source not read.
- Source of mdpf-gold-lambda, irpt-inf-holdings-performance-lambda, bd-silver-merge and bd-gold-trigger.
- Invoker of inf-gold-freshness-guard (not among 52 rule or 34 schedule targets).
- In-instance content of the gold runner, bronze runner and JWT exporter beyond S01 and S06.
- Deployed Lambda@Edge version (repository HEAD 3fc68796 read instead); CloudFront custom error rules and response policies.
- Secrets Manager values, the credential object orion/jwt/current.json, the OTP secret: named only, never read.
- IAM roles and policies; SNS topics, SQS queues and subscriptions (FB-k-2's).
- Object-level listing of opal-data-inf prefixes (no bucket enumeration run).
- Repository scripts beyond the 7 rows: gold (72 files), manual_api (44), silver (14), inf-pipeline tree (54); infra/ match capped at 200.
- comp-find repository sweep with --files timed out (rc 124 at 120 s); repository counts are native Grep.
