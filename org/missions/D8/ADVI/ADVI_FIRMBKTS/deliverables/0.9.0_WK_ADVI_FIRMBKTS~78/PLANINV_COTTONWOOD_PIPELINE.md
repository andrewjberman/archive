# FB-k-3 -- Cottonwood: what runs (read-only inventory)

Record: `PLANINV_COTTONWOOD_PIPELINE.json` (read_at 2026-10-13T22:18:52Z). Scope: rules, schedules, Lambda functions, SSM documents, exporter scripts and repository pipeline scripts that start or run the Cottonwood pipeline and touch `opal-data-cot`, the Cottonwood scope of `opal-data-bd`, or the Cottonwood monolith copy in `opal-data-assets`.

## Rows (42; legacy_touch true on 23)

| id | kind | trigger | legacy | reads / writes on the legacy home (opal-data-cot) |
|---|---|---|---|---|
| rule.cot-bronze-complete | rule | S3 event, *_BRONZE_COMPLETE.json | yes | event subscription |
| rule.cot-silver-complete | rule | S3 event, silver_complete.json | yes | event subscription |
| rule.cot-session-complete | rule | SSM status Success, opal-cot-bd-session-fetch | no | -- |
| rule.opal-cot-served-guard-on-write | rule | S3 event, platinum/firm/header_metrics.json | yes | event subscription |
| rule.cot-etf-ownership-daily-schedule | rule | cron 10:30 UTC | no | -- |
| rule.cot-rebalancer-runner-daily | rule | cron 12:45 UTC | no | -- |
| rule.cot-satellites-characteristics-producer-daily | rule | cron 13:25 UTC | no | -- |
| rule.etfs-cot-satellites-registry-producer-stamp-gated-daily | rule | cron 13:15 UTC | no | -- |
| rule.etfs-cot-satellites-characteristics-producer-reattempt-hourly | rule | cron :55 hourly | no | -- |
| rule.bd-cot-keepalive-sched | rule | rate 15 min | no | -- |
| rule.opal-cot-value-parity-hourly | rule | rate 1 hour | no | -- |
| rule.FIRMSEP-s3-direct-access-bypass | rule | CloudTrail GetObject on bd/inf | no | watch only (named for retirement, FB-k-5) |
| rule.cot-satellites-registry-producer-daily | rule | none live | no | ABSENT (graph only; surprise S3) |
| schedule.cot-bd-session-daily-et | schedule | 07:30 ET | no | -- |
| schedule.opal-assets-ingest-mirror-cot-daily-et | schedule | 07:45 ET, firm cot | no | -- |
| lambda.cot-bd-session-trigger | lambda | rules + schedule; SSM dispatch | yes | writes mode marker (inferred) |
| lambda.cot-rebalancer-runner | lambda | rule daily; reattempt | no | assets monolith only |
| lambda.cot-etf-ownership-daily | lambda | rule daily | no | assets read; etfs write (env SRC_BUCKET stale; surprise S4) |
| lambda.cot-satellites-characteristics-producer | lambda | rule daily; reattempt | yes | reads platinum/satellites/holdings.json; writes characteristics.json |
| lambda.cot-satellites-registry-producer | lambda | rule stamp-gated | yes | writes registry.json, holdings.json |
| lambda.bd-cot-keepalive | lambda | rate 15 min | no | secret and metrics only |
| lambda.opal-cot-served-guard | lambda | S3 event on served header | yes | reads and restores header_metrics.json; quarantine write |
| lambda.opal-cot-value-parity | lambda | rate 1 hour | yes | reads served header and silver/holdings anchor |
| lambda.opal-assets-ingest-mirror | lambda | schedule, firm cot | yes | reads forwardfill_v2/ and code/bronze/templates/ |
| lambda.bd-silver-merge | lambda | S3 event on opal-data-bd bronze | no | opal-data-bd only |
| lambda.bd-gold-trigger | lambda | S3 event, BD price parquet; rules | no | opal-data-bd pending marker |
| lambda.exec-summary-generator | lambda | chain-complete event | no | opal-data-bd (inferred) |
| lambda.mdpf-gold-lambda | lambda | not read | yes | writes investor-reporting/directory/ (measured prefix) |
| task.opal-cot-bd-session-fetch | task | SSM | yes | log copy to legacy home; session secret |
| task.opal-cot-bronze-run | task | SSM | yes | writes bronze/ and _BRONZE_COMPLETE.json |
| task.opal-cot-silver-run | task | SSM | yes | writes silver/ |
| task.opal-cot-gold-run | task | SSM | yes | writes gold/ and gold/.checkpoints/ |
| script.cot-exporter-user-data | script | EC2 boot | yes | reads code/bronze/ scripts |
| script.data/cot/scripts/bronze/cot_bronze_ingest.py | script | opal-cot-bronze-run | yes | writes bronze/ |
| script.data/cot/scripts/silver/cot_silver_merge.py | script | opal-cot-silver-run | yes | reads forwardfill_v2/; writes silver/ |
| script.data/cot/scripts/gold/gold_dispatch.sh | script | opal-cot-gold-run | yes | reads code/gold/, silver/, gold/artifacts; writes checkpoints, logs |
| script.data/cot/scripts/gold/runners_cot/d01_cot_firm_header_metrics.py | script | gold chain | yes | reads served header (compare) |
| script.data/cot/scripts/gold/build_canonical_prices_v2.py | script | manual or chain | yes | reads silver/historical_prices, ticker lookup |
| script.data/mdpf/scripts/demque/land_cot.py | script | manual | yes | writes historical prices and ticker lookup |
| script.data/assets/scripts/gold/investor_reporting/directory_runner.py | script | hosted by mdpf-gold-lambda | yes | writes investor-reporting/directory/ |
| script.data/assets/scripts/gold/build_cottonwood_mdpf_pair.py | script | manual | no | assets monolith; names opal-data-cot only as a prohibition |
| other.s3-notifications-cot-pipeline | other | config | yes | EventBridge enabled on opal-data-cot |

Kinds: rule 13, lambda 13, script 9, task 4, schedule 2, other 1. Legacy touch: 23 of 42.

## Totals (denominators)

- EventBridge rules listed in us-east-1: 156; targets read for all 156 (168 targets). Rules matching cot, gold or bd in pattern, target or name: 23. Rules whose pattern names opal-data-cot: 3.
- Scheduler schedules listed: 34; cot-scoped read in full: 2.
- ECS: 1 cluster, 3 services, 9 active task definitions, none name-matched. Step Functions: 1 state machine, not name-matched.
- Lambda functions listed: 237; environment read for 27 name-matched; source read at matched lines for 11.
- S3 notification configurations read: 2 (opal-data-cot: EventBridge only; opal-data-bd: 2 Lambda configurations).
- S3 list calls: opal-data-cot 13 (9 top-level prefixes); opal-data-bd 13 (31 top-level prefixes).
- Repository files naming opal-data-cot: 1741 worktree-wide; 117 under infra; 61 under data. Pipeline scripts read by matched line: 9.

## Not read

1. ECS task definition contents and service configs (names only).
2. Step Functions YangDataPipeline definition.
3. 210 of 237 Lambda functions (environment and code).
4. lambda.mdpf-gold-lambda source (repository holds build_package.py only) and its trigger source.
5. Live Lambda bytes against repository source (no deployed-bytes check).
6. EC2 state, crontabs and on-box scripts; SSM documents read from the repository, not the live service.
7. Scripts at matched lines only; gold runners d02, c01, and the A_ to E_ gold scripts listed by name only.
8. Object keys below second-level prefixes; no object body read or downloaded.
9. Consumers of platinum/satellites/* and the investor-reporting directory (headers and names only).
10. The Cottonwood crosswalk input and its consumers (FB-k-4). One comp-find crosswalk call returned no output (rc 143, not retried); Grep used.
11. Secret contents and credential objects (not read, not printed).
12. Call sites of the mode-marker writer in lambda.cot-bd-session-trigger.
13. The other 32 schedules (names only).
14. The Black Diamond gold chain beyond its trigger.

## Surprises filed (INVESTIGATION_v1.md)

S1 the Cottonwood scope of opal-data-bd is empty; S2 characteristics.json header says zero writers, object modified today; S3 graph lists a registry daily rule that is absent live; S4 stale SRC_BUCKET env on cot-etf-ownership-daily. Rows: ADVI_FIRMBKTS-D1-W78-S1 to S4 (OBSERVATION, INERT).
