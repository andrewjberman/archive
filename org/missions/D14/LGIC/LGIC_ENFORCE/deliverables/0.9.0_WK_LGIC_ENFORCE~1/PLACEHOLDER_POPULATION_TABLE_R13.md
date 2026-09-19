# PLACEHOLDER_POPULATION_TABLE_R13 -- one markdown table row per JUDGED census item (EN-p-37)

Derived, at this cell's own write time, from `NAMING_CENSUS_REPORT.r13.md`'s fenced json `rows` list
(the live+repo census run by this cell: `python lib/opal_naming.py census --live --repo --budget 600 --not-judged .../NOT_JUDGED_R13.json --report .../NAMING_CENSUS_REPORT.r13.md`, rc=0, CENSUS: COMPLETE,
registry@9f4a569d7a54b53c over all 6 registry file(s)).

**This is the report the round-13 arm RE-COUNTS.** Each data line below carries exactly one judged
row's `canonical` value verbatim (the field R-38's population is defined over); `current` and `where`
have their own `{`/`}` bytes rendered as `(`/`)` SO THAT a pre-existing literal template brace in the
OBSERVED name (e.g. `{snap}`) is never double-counted by appearing twice on the same line -- the
`canonical` cell is the ONLY column left with real `{` `}` bytes. The header and separator lines below
do not start with `|` alone matching the arm's row filter incorrectly (they satisfy `startswith('|')`
is false for none of these, see note) -- verified: header/separator EXCLUDED from the arm's own
recount, confirmed by direct call (see result.md).

columns: current(escaped) | canonical | verdict | type | plane | where
-------|-------|-------|-------|-------|-------
| inf-otp-relay-api | advi-inf-otp-relay-api | OUT-OF-PATTERN | API_GW | live |  |
| opal-portal-data-proxy-api | opal-portal-data-proxy-api | CONFORMANT | API_GW | live |  |
| opal-session-analytics-api | opal-session-analytics-api | CONFORMANT | API_GW | live |  |
| estate-report-seam-freshness-publisher | estate-report-seam-freshness-publisher-build | OUT-OF-PATTERN | CODEBUILD_PROJECT | live |  |
| globgrph-derive-build | globgrph-derive-build | CONFORMANT | CODEBUILD_PROJECT | live |  |
| opal-drift-producer | opal-drift-producer-build | OUT-OF-PATTERN | CODEBUILD_PROJECT | live |  |
| opal-stitch-produce | opal-stitch-produce-build | OUT-OF-PATTERN | CODEBUILD_PROJECT | live |  |
| semantic-clustering-lambda-build | {system}-semantic-clustering-lambda-build | OUT-OF-PATTERN | CODEBUILD_PROJECT | live |  |
| ExecIncrParityFailure | {system}-exec-incrparity-failure-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| FIRMSEP-auth-advisor-scoping-denied | firmsep-auth-advisor-scoping-denied-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| FIRMSEP-auth-ownership-map-fetch-failed | firmsep-auth-ownership-map-fetch-failed-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| FIRMSEP-auth-ownership-map-schema-mismatch | firmsep-auth-ownership-map-schema-mismatch-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| FIRMSEP-auth-tier-denied | firmsep-auth-tier-denied-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| FIRMSEP-shared-advisor-router-denied | firmsep-shared-advisor-router-denied-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| Inflection-HistBackfill-FailureSpike | advi-inf-hist-backfill-failure-spike-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| Inflection-JwtResilience-NearExpirySpike | advi-inf-jwt-resilience-near-expiry-spike-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| Inflection-SilverChain-DimConversionFailure | advi-inf-silver-chain-dim-conversion-failure-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| OPSEC-auth-login-rate-limit-blocked | {system}-opsec-auth-login-rate-limit-blocked-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| OPSEC-auth-throttled | {system}-opsec-auth-throttled-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| PortfolioExcelGenerator-Errors | {system}-portfolio-excel-generator-errors-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| YChartsSessionEviction | ycharts-session-eviction-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| bd-gold-qa-runner-forgotten | {system}-49f-gold-qa-runner-forgotten-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| bd-gold-runner-overrun | {system}-49f-gold-runner-overrun-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| cloudfront-high-error-rate | {system}-cloudfront-high-error-rate-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| cloudfront-high-origin-latency | {system}-cloudfront-high-origin-latency-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| cloudfront-low-cache-hit-rate | {system}-cloudfront-low-cache-hit-rate-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| cmtque-commit-latency-high | cmtque-commit-latency-high-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| cmtque-dlq-depth | cmtque-dlq-depth-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| cmtque-queue-backlog | cmtque-queue-backlog-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| cmtque-worker-down | cmtque-worker-down-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| etfs-netassets-daily-errors | etfs-netassets-daily-errors-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| etfs-reports-orchestrator-errors | etfs-reports-orchestrator-errors-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| exec-summary-advisors-processed-ceiling | {system}-exec-summary-advisors-processed-ceiling-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| exec-summary-tokens-in-anomaly | {system}-exec-summary-tokens-in-anomaly-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| gldinc-ss4c-canary-break | {system}-gldinc-ss4c-canary-break-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| gldinc-ss4c-weekly-divergence | {system}-gldinc-ss4c-weekly-divergence-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| globgrph-s3-requests-daily-high | globgrph-s3-requests-daily-high-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| globgrph-s3-requests-daily-warning | globgrph-s3-requests-daily-warning-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| inf-bronze-trigger-missed-start | advi-inf-bronze-trigger-missed-start-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| inf-gold-chain-failed | advi-inf-gold-chain-failed-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| inf-gold-runner-overrun | advi-inf-gold-runner-overrun-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| inf-gold-trigger-dlq-depth | advi-inf-gold-trigger-dlq-depth-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| inf-nna-partition-completeness-breach | advi-inf-nna-partition-completeness-breach-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| mdpf-daily-trigger-dlq-not-empty | mdpf-daily-trigger-dlq-not-empty-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| opal-partners-data-duration-high | opal-partners-data-duration-high-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| opal-partners-data-errors | opal-partners-data-errors-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| opal-partners-data-throttles | opal-partners-data-throttles-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| opal-session-analytics-errors | opal-session-analytics-errors-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| opal-session-analytics-estimated-monthly-cost | opal-session-analytics-estimated-monthly-cost-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| opal-session-analytics-high-invocations | opal-session-analytics-high-invocations-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| opal-session-analytics-throttles | opal-session-analytics-throttles-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| orion-otp-timeout-alert | orion-otp-timeout-alert-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| semantic-layer2.5-clustering-failures | {system}-semantic-layer2-5-clustering-failures-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| semantic-layer2.5-duration-warning | {system}-semantic-layer2-5-duration-warning-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| semantic-layer3-gpt-curation-failures | {system}-semantic-layer3-gpt-curation-failures-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| semantic-layer4-portal-publisher-failures | {system}-semantic-layer4-portal-publisher-failures-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| wsb-49f-model-aua-daily-errors | {system}-49f-wsb-model-aua-daily-errors-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| wsd-49f-partner-held-etf-daily-errors | {system}-49f-wsd-partner-held-etf-daily-errors-alarm | OUT-OF-PATTERN | CW_ALARM | live |  |
| bd-securities | {system}-49f-securities-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| etf-classifications | {system}-etf-classifications-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| find-insure-cost-state | {system}-find-insure-cost-state-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| gateway-access-state-table | gateway-access-state-table | CONFORMANT | DYNAMODB_TABLE | live |  |
| irpt-checkpoints | irpt-checkpoints-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| irpt-jobs | irpt-jobs-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| irpt-outbox | irpt-outbox-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| irpt-requests | irpt-requests-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| market-updates | {system}-market-updates-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-data-refresh-executions | opal-data-refresh-executions-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-data-smartx | opal-data-smartx-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-firms | opal-firms-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-gateway-access-state | gateway-access-state-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-globgrph-nessie-_objs | globgrph-nessie-objs-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-globgrph-nessie-_refs | globgrph-nessie-refs-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-harvest-articles | harvest-articles-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-harvest-security-metrics | harvest-security-metrics-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-inf-launch-locks | opal-inf-launch-locks-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-invitations | opal-invitations-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-keyword-intelligence | opal-keyword-intelligence-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-offices | opal-offices-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-partner-49financial | opal-49f-partner-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-partner-cottonwood | opal-cot-partner-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-partner-demo | opal-demo-partner-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-partner-inflection | opal-inf-partner-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-pii-lookup | opal-pii-lookup-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-pm-snapshots | opal-pm-snapshots-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-portal-auth-mfa | opal-portal-auth-mfa-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-portal-auth-throttle | opal-portal-auth-throttle-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-portal-content | opal-portal-content-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-portal-market-data | opal-portal-market-data-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-portfolio-exports | opal-portfolio-exports-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-portfolio-sessions | opal-portfolio-sessions-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-sessions | opal-sessions-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-suspicious-addresses | opal-suspicious-addresses-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-tickets | opal-tickets-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| opal-users-v2 | opal-users-v2-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| seeking-alpha-article-urls | seeking-alpha-article-urls-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| user-permissions | {system}-user-permissions-table | OUT-OF-PATTERN | DYNAMODB_TABLE | live |  |
| bd-49f-auto-login | blackdiamond-49f-auto-login-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| bd-allocations | {system}-49f-allocations-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| bd-assets | {system}-49f-assets-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| bd-fees | {system}-49f-fees-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| bd-gold-detail-generator | {system}-49f-gold-detail-generator-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| bd-gold-layer-runner | {system}-49f-gold-layer-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| bd-gold-qa-runner | {system}-49f-gold-qa-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| bd-transactions | {system}-49f-transactions-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| canonical-schwab-si2 | schwab-canonical-si2-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| consolidation-gold-runner | {system}-consolidation-gold-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| cot-exporter | advi-cot-exporter-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| estate-report-runner | estate-report-runner | CONFORMANT | EC2_INSTANCE | live |  |
| estate-report-runner | estate-report-runner | CONFORMANT | EC2_INSTANCE | live |  |
| etfs-reports-reporter | etfs-reports-reporter-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| historical-prices-fetcher | {system}-historical-prices-fetcher-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| historical-prices-fetcher | {system}-historical-prices-fetcher-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| historical-prices-fetcher | {system}-historical-prices-fetcher-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| historical-prices-fetcher | {system}-historical-prices-fetcher-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| historical-prices-fetcher | {system}-historical-prices-fetcher-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| historical-prices-fetcher | {system}-historical-prices-fetcher-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| historical-prices-fetcher | {system}-historical-prices-fetcher-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| historical-prices-fetcher | {system}-historical-prices-fetcher-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| inf-bronze-runner | advi-inf-bronze-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| inf-exporter | advi-inf-exporter-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| inf-gold-layer-runner | {system}-inf-gold-layer-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| inf-gold-qa-runner | {system}-inf-gold-qa-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| irpt-ycharts-runner | irpt-ycharts-runner | CONFORMANT | EC2_INSTANCE | live |  |
| mdpf-daily-runner | mdpf-daily-runner | CONFORMANT | EC2_INSTANCE | live |  |
| opal-gateway | gateway-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| opal-website-wp | opal-website-wp-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| seeking-alpha-scraper | seeking-alpha-scraper-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| seeking-alpha-scraper | seeking-alpha-scraper-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| smartx-exporter | smartx-exporter-runner | OUT-OF-PATTERN | EC2_INSTANCE | live |  |
| opal-globgrph | globgrph-cluster | OUT-OF-PATTERN | ECS_CLUSTER | live |  |
| globgrph-comp-learns-producer | globgrph-comp-learns-producer-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| globgrph-cse-producer | globgrph-cse-producer-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| globgrph-derive-runner | globgrph-derive-runner-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| globgrph-fedobs-producer | globgrph-fedobs-producer-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| globgrph-nessie | globgrph-nessie-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| globgrph-projection-worker | globgrph-projection-worker-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| globgrph-resource-summaries-producer | globgrph-resource-summaries-producer-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| globgrph-serving | globgrph-serving-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| globgrph-trino | globgrph-trino-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | live |  |
| FIRMSEP-s3-direct-access-bypass | firmsep-s3-direct-access-bypass-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| access-anomaly-scanner-schedule | {system}-access-anomaly-scanner-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-49f-etf-ownership-scheduled-floor | blackdiamond-49f-etf-ownership-scheduled-floor-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-49f-fees-runner-daily | blackdiamond-49f-fees-runner-daily | ALIAS | EVENT_RULE | live |  |
| bd-49f-fees-session-daily | blackdiamond-49f-fees-session-daily | ALIAS | EVENT_RULE | live |  |
| bd-49f-insurance-session-daily | blackdiamond-49f-insurance-session-daily | ALIAS | EVENT_RULE | live |  |
| bd-49f-keepalive-sched | blackdiamond-49f-keepalive-sched-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-49f-runner-daily | blackdiamond-49f-runner-daily | ALIAS | EVENT_RULE | live |  |
| bd-49f-session-complete | blackdiamond-49f-session-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-49f-session-daily | blackdiamond-49f-session-daily | ALIAS | EVENT_RULE | live |  |
| bd-allocation-file-check-daily | {system}-49f-allocation-file-check-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-allocation-pipeline-trigger | {system}-49f-allocation-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-asset-dim-pipeline-trigger | {system}-49f-asset-dim-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-canonical-prices-daily | {system}-49f-canonical-prices-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-cot-keepalive-sched | blackdiamond-cot-keepalive-sched-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-fees-pipeline-trigger | {system}-49f-fees-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-gold-layer-monthly-trigger | {system}-49f-gold-layer-trigger-monthly | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-gold-nightly-fallback | {system}-49f-gold-nightly-fallback-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-realized-pipeline-trigger | {system}-49f-realized-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-transaction-pipeline-trigger | {system}-49f-transaction-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| bd-unrealized-pipeline-trigger | {system}-49f-unrealized-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| canonical-schwab-si2-08242234-daily-pull | schwab-08242234-canonical-si2-pull-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| canonical-schwab-si2-08335338-daily-pull | schwab-08335338-canonical-si2-pull-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| consolidation-gold-runner-scheduled-start | {system}-consolidation-gold-runner-scheduled-start-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| cost-anomaly-scanner-schedule | {system}-cost-anomaly-scanner-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| cot-bronze-complete | {system}-cot-bronze-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| cot-etf-ownership-daily-schedule | {system}-cot-etf-ownership-schedule-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| cot-rebalancer-runner-daily | {system}-cot-rebalancer-runner-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| cot-satellites-characteristics-producer-daily | {system}-cot-satellites-characteristics-producer-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| cot-satellites-registry-producer-daily | {system}-cot-satellites-registry-producer-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| cot-session-complete | {system}-cot-session-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| cot-silver-complete | {system}-cot-silver-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| daily-agenda-generator | {system}-agenda-generator-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| daily-sprint-generator-schedule | {system}-sprint-generator-schedule-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| ec2-auto-shutdown-enforcer-schedule | {system}-ec2-auto-shutdown-enforcer-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| ec2-runtime-monitor-15min | {system}-ec2-runtime-monitor-15min-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| etf-ownership-dashboard-daily | {system}-etf-ownership-dashboard-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| etf-positioning-producer-daily | {system}-etf-positioning-producer-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| etfs-canon-fanin-daily | etfs-canon-fanin-daily | CONFORMANT | EVENT_RULE | live |  |
| etfs-netassets-daily | etfs-netassets-daily | CONFORMANT | EVENT_RULE | live |  |
| exec-summary-trigger | {system}-exec-summary-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| fear-greed-daily-update | {system}-fear-greed-update-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| finbert-scoring-post-ingestion | {system}-finbert-scoring-post-ingestion-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| finbert-scoring-post-ingestion-45min | {system}-finbert-scoring-post-ingestion-45min-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| fred-ingestion-daily | fred-ingestion-daily | CONFORMANT | EVENT_RULE | live |  |
| fred-ingestion-monthly-early | fred-ingestion-early-monthly | OUT-OF-PATTERN | EVENT_RULE | live |  |
| fred-ingestion-monthly-late | fred-ingestion-late-monthly | OUT-OF-PATTERN | EVENT_RULE | live |  |
| fred-ingestion-monthly-mid | fred-ingestion-mid-monthly | OUT-OF-PATTERN | EVENT_RULE | live |  |
| fred-ingestion-weekly | fred-ingestion-weekly | CONFORMANT | EVENT_RULE | live |  |
| fred-macro-ingestion-daily | fred-macro-ingestion-daily | CONFORMANT | EVENT_RULE | live |  |
| gldinc-ss4c-canary-daily | {system}-gldinc-ss4c-canary-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| historical-prices-daily | {system}-historical-prices-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| incrparity-weekly | {system}-incrparity-weekly | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-accounts-v2-daily | advi-inf-accounts-v2-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-api-assets-v2-daily | {system}-inf-api-assets-v2-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-api-eclipse-daily | eclipse-inf-api-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-api-positions-daily | {system}-inf-api-positions-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-api-reps-daily | {system}-inf-api-reps-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-api-txn-daily | {system}-inf-api-txn-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-assets-trigger-bronze-complete | {system}-inf-assets-trigger-bronze-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-billing-daily | advi-inf-billing-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-bronze-complete-emitter-daily | {system}-inf-bronze-complete-emitter-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-canonical-prices-daily | {system}-inf-canonical-prices-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-etf-ownership-daily-schedule | {system}-inf-etf-ownership-schedule-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-gold-dispatch-release-changed | {system}-inf-gold-dispatch-release-changed-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-gold-full-on-bronze-complete | {system}-inf-gold-full-on-bronze-complete | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-gold-incremental-daily | {system}-inf-gold-incremental-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-nna-partition-check-trigger | {system}-inf-nna-partition-check-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-otp-state-change | {system}-inf-otp-state-change-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-performance-daily | advi-inf-performance-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-silver-chain-bronze-complete | {system}-inf-silver-chain-bronze-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-tax-daily | advi-inf-tax-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| inf-unified-account-dim-daily | advi-inf-unified-account-dim-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| infrastructure-monitor-daily | {system}-infrastructure-monitor-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| infrastructure-snapshot-daily | {system}-infrastructure-snapshot-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| keyword-drilldown-generator-daily | {system}-keyword-drilldown-generator-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| keyword-intelligence-generator-daily | {system}-keyword-intelligence-generator-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| layer3-gpt-curation-daily | {system}-layer3-gpt-curation-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| market-rsi-tiered-daily | {system}-market-rsi-tiered-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| mdpf-feeder-accelerator | mdpf-feeder-accelerator-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| moltbot-ssm-sendcommand-alert | {system}-moltbot-ssm-sendcommand-alert-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-49f-served-guard-on-write | opal-49f-served-guard-on-write | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-bd49f-daily-pull-pull-daily | opal-assets-bd49f-daily-pull-pull-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-bd49f-daily-pull-reattempt-daily | opal-assets-bd49f-daily-pull-reattempt-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-daily-emitter-daily | opal-assets-daily-emitter-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-ingest-mirror-inf-daily | opal-inf-assets-ingest-mirror-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-assets-silver-blackdiamond-sweep-daily | opal-assets-silver-blackdiamond-sweep-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-silver-eclipse-sweep-daily | opal-assets-silver-eclipse-sweep-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-silver-etf-sweep-daily | opal-assets-silver-etf-sweep-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-silver-orion-sweep-daily | opal-assets-silver-orion-sweep-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-silver-schwab-sweep-daily | opal-assets-silver-schwab-sweep-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-assets-silver-smartx-sweep-daily | opal-assets-silver-smartx-sweep-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-cot-served-guard-on-write | opal-cot-served-guard-on-write | CONFORMANT | EVENT_RULE | live |  |
| opal-cot-value-parity-hourly | opal-cot-value-parity-hourly | CONFORMANT | EVENT_RULE | live |  |
| opal-drift-producer-nightly | opal-drift-producer-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-globgrph-cloudtrail-mgmt | globgrph-cloudtrail-mgmt-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-globgrph-comp-learns-producer-nightly | globgrph-comp-learns-producer-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-globgrph-derive-runner-nightly | globgrph-derive-runner-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-globgrph-fedobs-producer-nightly | globgrph-fedobs-producer-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-inf-bronze-runner-cron | opal-inf-bronze-runner-cron-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-inf-ec2-state-change-monitor | opal-inf-ec2-state-change-monitor-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-inf-export-schedule | opal-inf-export-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-inf-jwt-fetch | opal-inf-jwt-fetch-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-inf-served-guard-on-write | opal-inf-served-guard-on-write | CONFORMANT | EVENT_RULE | live |  |
| opal-inf-value-parity-hourly | opal-inf-value-parity-hourly | CONFORMANT | EVENT_RULE | live |  |
| opal-ipset-reconciler-daily | opal-ipset-reconciler-daily | CONFORMANT | EVENT_RULE | live |  |
| opal-ms-ingest-liveness-6h | opal-ms-ingest-liveness-6h-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-otp-liveness-6h | opal-otp-liveness-6h-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-sentinel-daily-digest | opal-sentinel-digest-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| opal-stitch-produce-nightly | opal-stitch-produce-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| seeking-alpha-analysis-daily | seeking-alpha-analysis-daily | CONFORMANT | EVENT_RULE | live |  |
| seeking-alpha-news-daily | seeking-alpha-news-daily | CONFORMANT | EVENT_RULE | live |  |
| trending-image-selector-daily | {system}-trending-image-selector-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| trending-topics-portal-publisher-afternoon | {system}-trending-topics-portal-publisher-afternoon-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| trending-topics-portal-publisher-daily | {system}-trending-topics-portal-publisher-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| trending-topics-portal-publisher-morning | {system}-trending-topics-portal-publisher-morning-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| volatility-daily-update | {system}-volatility-update-daily | OUT-OF-PATTERN | EVENT_RULE | live |  |
| yang-refresh-fred-cache-weekly | yang-refresh-fred-cache-weekly | CONFORMANT | EVENT_RULE | live |  |
| ycharts-session-capture-schedule | ycharts-session-capture-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| ycharts-session-probe-schedule | ycharts-session-probe-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | live |  |
| AccessAnomalyScannerPolicy | {system}-access-anomaly-scanner-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| AdditionalPermissions | {system}-additional-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| BDPipelinePermissions | {system}-49f-pipeline-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| BDPipelineTaskPolicy | {system}-49f-pipeline-task-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| BoundedDeriveReadOnly | {system}-bounded-derive-read-only-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CodeBuildSemanticClusteringPolicy | {system}-codebuild-semantic-clustering-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CompLearnsProducerLogs | {system}-comp-learns-producer-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CompLearnsProducerRunTask | {system}-comp-learns-producer-run-task-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CompLearnsServedWrite | {system}-comp-learns-served-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CostAnomalyScannerPolicy | {system}-cost-anomaly-scanner-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CotServedAndSourceRead | {system}-cot-served-and-source-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CseProducerCWLogs | {system}-cse-producer-cw-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CseProducerRunTask | {system}-cse-producer-run-task-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| CseProducerS3 | {system}-cse-producer-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DeriveRunnerAccountDescribe | {system}-derive-runner-account-describe-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DeriveRunnerBucketNotificationRead | {system}-derive-runner-bucket-notification-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DeriveRunnerCWLogs | {system}-derive-runner-cw-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DeriveRunnerMsIngestSecret | {system}-derive-runner-ms-ingest-secret-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DeriveRunnerS3 | {system}-derive-runner-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DeriveRunnerSNS | {system}-derive-runner-sns-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DriftProducerCompPutAndSourceZip | {system}-drift-producer-comp-put-and-source-zip-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DriftProducerWritesAndDataDeny | {system}-drift-producer-writes-and-data-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DynamoDBAccess | {system}-dynamo-db-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| DynamoDBAccessPolicy | {system}-dynamo-db-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| EC2RuntimeMonitorPolicy | {system}-ec2-runtime-monitor-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| EventsRunECSTask | {system}-events-run-ecs-task-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| FargateTriggerPermissions | {system}-fargate-trigger-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| FedobsEmitterLogs | {system}-fedobs-emitter-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| FedobsProducerRunTask | {system}-fedobs-producer-run-task-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| FedobsWriteScoped | {system}-fedobs-write-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| GlobgrphServingReadOnly | globgrph-serving-read-only-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| IncrementalUpdaterSNS | {system}-incremental-updater-sns-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| InfServedAndSourceRead | {system}-inf-served-and-source-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| InfrastructureSnapshotPolicy | {system}-infrastructure-snapshot-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| LambdaSelfInvoke | {system}-lambda-self-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| Layer3EC2Policy | {system}-layer3-ec2-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| MarketRSITieredPolicy | {system}-market-rsi-tiered-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| MonitorAnthropicSecretRead | {system}-monitor-anthropic-secret-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| MonitorDataFreshnessRead | {system}-monitor-data-freshness-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| MonitorGraphHeadContractRead | {system}-monitor-graph-head-contract-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| MonitorLogsRead | {system}-monitor-logs-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| MonitorSnsEgressRead | {system}-monitor-sns-egress-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| NessieDynamoAccess | {system}-nessie-dynamo-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| NessieS3WarehouseAccess | {system}-nessie-s3-warehouse-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| OpalAuthSecretsAccess | opal-auth-secrets-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| OpalDataPMAccess | opal-data-pm-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| OpalDataPMCacheBustAccess | opal-data-pm-cache-bust-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| OpalDataPMUploadAccess | opal-data-pm-upload-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| OpalPMDynamoDBAccess | opal-pm-dynamo-db-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| PartnerEtlOpsConsumerPolicy | {system}-partner-etl-ops-consumer-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| PartnerIdentityReadPermissions | {system}-partner-identity-read-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| PortfolioExportPolicy | {system}-portfolio-export-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ProjectionPipeInvoke | {system}-projection-pipe-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ProjectionRuntime | {system}-projection-runtime-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| RecheckQueue | {system}-recheck-queue-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| RecheckQueue | {system}-recheck-queue-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| RecheckQueue | {system}-recheck-queue-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ResourceSummariesProducerCWLogs | {system}-resource-summaries-producer-cw-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ResourceSummariesProducerS3 | {system}-resource-summaries-producer-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| S3Access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| S3Access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| S3WarehouseWrite | {system}-s3-warehouse-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SQSConsume | {system}-sqs-consume-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SQSConsume | {system}-sqs-consume-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SchwabAnonymizerPolicy | schwab-anonymizer-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SecretsManagerAccess | {system}-secretsmanager-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SecretsManagerAccess | {system}-secretsmanager-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SecretsManagerAccess | {system}-secretsmanager-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SeekingAlpha-S3-Access | seeking-alpha-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SeekingAlpha-SecretsAccess | seeking-alpha-secrets-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SeekingAlphaNewsPolicy | seeking-alpha-news-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SeekingAlphaScraperPolicy | seeking-alpha-scraper-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SemanticLayer3CurationAccess | {system}-semantic-layer3-curation-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SemanticTrendingPublisherS3Access | {system}-semantic-trending-publisher-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ServedKeyGuardS3 | {system}-served-key-guard-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ServedKeyGuardS3 | {system}-served-key-guard-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ServedKeyGuardS3 | {system}-served-key-guard-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| StartDriftProducerBuild | {system}-start-drift-producer-build-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| StartStitchProduceBuild | {system}-start-stitch-produce-build-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| StitchProducePerms | {system}-stitch-produce-perms-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| StitchSourceZipPut | {system}-stitch-source-zip-put-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| SurfaceCheckArtifactPut | {system}-surface-check-artifact-put-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| TrinoCWLogs | {system}-trino-cw-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| TrinoCodeHeatGlueRead | {system}-trino-code-heat-glue-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| TrinoSSMExecChannel | {system}-trino-ssm-exec-channel-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| TrinoWarehouseReadOnly | {system}-trino-warehouse-read-only-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| advi-49f-chain-access | advi-49f-chain-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| advi-49f-gold-dispatch-scoped | advi-49f-gold-dispatch-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| advi-49f-publisher-platinum-put | advi-49f-publisher-platinum-put-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| agentbus-alyssa01-fleet-andrew-role-partition | agentbus-alyssa01-fleet-andrew-role-partition-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| agentbus-sim01-fleet-alpha-role-partition | agentbus-sim01-fleet-alpha-role-partition-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| agentbus-sim01-fleet-beta-role-partition | agentbus-sim01-fleet-beta-role-partition-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| amgt-resapp-chatter-axis-lambda-policy | amgt-resapp-chatter-axis-lambda-policy | CONFORMANT | IAM_POLICY | live |  |
| amgt-resapp-chatter-axis-scheduler-invoke | amgt-resapp-chatter-axis-scheduler-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-49f-auto-login | blackdiamond-49f-auto-login-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-49f-fees-runner-policy | blackdiamond-49f-fees-runner-policy | ALIAS | IAM_POLICY | live |  |
| bd-49f-keepalive-policy | blackdiamond-49f-keepalive-policy | ALIAS | IAM_POLICY | live |  |
| bd-49f-runner-policy | blackdiamond-49f-runner-policy | ALIAS | IAM_POLICY | live |  |
| bd-49f-session-trigger-policy | blackdiamond-49f-session-trigger-policy | ALIAS | IAM_POLICY | live |  |
| bd-allocation-checker-permissions | {system}-49f-allocation-checker-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-cot-keepalive-policy | blackdiamond-cot-keepalive-policy | ALIAS | IAM_POLICY | live |  |
| bd-daily-trigger-policy | {system}-49f-daily-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-gold-detail-cloudwatch-logs | {system}-49f-gold-detail-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-gold-detail-s3-access | {system}-49f-gold-detail-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-gold-eventbridge-start-execution-policy | {system}-49f-gold-eventbridge-start-execution-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-gold-step-functions-lambda-policy | {system}-49f-gold-step-functions-lambda-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-merge-daily-policy | {system}-49f-merge-daily-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-s3-access | {system}-49f-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-s3-readwrite | {system}-49f-s3-readwrite-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-s3-scoped | {system}-49f-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-securities-access | {system}-49f-securities-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bd-silver-merge-policy | {system}-49f-silver-merge-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| bronze-modemarker-rw | {system}-bronze-modemarker-rw-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudfront-invalidate | {system}-cloudfront-invalidate-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudfront-invalidate | {system}-cloudfront-invalidate-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudfront-invalidate | {system}-cloudfront-invalidate-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-histbf-namespace | {system}-cloudwatch-histbf-namespace-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-jwtres-namespace | {system}-cloudwatch-jwtres-namespace-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-logs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-logs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-logs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-put-metric | {system}-cloudwatch-put-metric-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-put-metric | {system}-cloudwatch-put-metric-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cloudwatch-put-metric | {system}-cloudwatch-put-metric-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| consolidation-gold-runner-inline | {system}-consolidation-gold-runner-inline-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cot-bd-session-trigger-policy | blackdiamond-cot-session-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cot-exporter-policy | {system}-cot-exporter-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cot-rebalancer-runner-invoke-silver-blackdiamond | blackdiamond-cot-rebalancer-runner-invoke-silver-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cot-rebalancer-runner-session-read | {system}-cot-rebalancer-runner-session-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cot-rebalancer-runner-write-cot | {system}-cot-rebalancer-runner-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-read-deny | {system}-cross-firm-bucket-read-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-bucket-write-deny | {system}-cross-firm-bucket-write-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| daily-sprint-generator-policy | {system}-daily-sprint-generator-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| data-refresh-cloudfront-read | {system}-data-refresh-cloudfront-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| data-refresh-qa-scratch-access-20260803 | {system}-data-refresh-qa-scratch-access-20260803-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| data-refresh-sscn-s3-access | {system}-data-refresh-sscn-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| data-refresh-time-machine-invoke | {system}-data-refresh-time-machine-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ddb-write-ownership-daily | {system}-ddb-write-ownership-daily-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| deck-generation-lambda-policy | {system}-deck-generation-lambda-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| demo-transform-runner-s3-scoped | {system}-demo-transform-runner-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| describe-tags-self | {system}-describe-tags-self-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| describe-tags-self | {system}-describe-tags-self-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| describe-tags-self | {system}-describe-tags-self-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ec2-auto-shutdown-enforcer-policy | {system}-ec2-auto-shutdown-enforcer-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ec2-ssm-deploy | {system}-ec2-ssm-deploy-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ecr-access | {system}-ecr-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| estate-capture-writer-text-input | estate-capture-writer-text-input-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| estate-report-orchestrator | estate-report-orchestrator-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| estate-report-runner | estate-report-runner-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| estate-report-runner-selfstop | estate-report-runner-selfstop-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| estate-report-scheduler-invoke | estate-report-scheduler-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| estate-report-seam-freshness-publisher | estate-report-seam-freshness-publisher-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| estate-report-seam-freshness-scheduler | estate-report-seam-freshness-scheduler-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| etfs-reports-orchestrator | etfs-reports-orchestrator-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| etfs-reports-reporter | etfs-reports-reporter-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| etfs-reports-scheduler-invoke | etfs-reports-scheduler-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| events-emit | {system}-events-emit-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| exec-summary-generator-policy | {system}-exec-summary-generator-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| find-insure-dynamodb | {system}-find-insure-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| find-insure-events | {system}-find-insure-events-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| find-insure-kms | {system}-find-insure-kms-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| find-insure-logs | {system}-find-insure-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| find-insure-s3 | {system}-find-insure-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| find-insure-secrets-read | {system}-find-insure-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| find-insure-sns | {system}-find-insure-sns-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| fred-ingestion-secrets-read | fred-ingestion-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| fred-macro-artifact-write | fred-macro-artifact-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| fred-macro-secrets-read | fred-macro-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| gateway-access-admin-ssm-readonly-policy | gateway-access-admin-ssm-readonly-policy | CONFORMANT | IAM_POLICY | live |  |
| gateway-assume-schwab-readers-policy | gateway-assume-schwab-readers-policy | CONFORMANT | IAM_POLICY | live |  |
| gateway-schwab-catalog-read-role-policy | gateway-schwab-catalog-read-role-policy | CONFORMANT | IAM_POLICY | live |  |
| gateway-schwab-read-role-policy | gateway-schwab-read-role-policy | CONFORMANT | IAM_POLICY | live |  |
| gldinc-ss4c-canary-policy | {system}-gldinc-ss4c-canary-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| globgrph-derive-build-perms | globgrph-derive-build-perms-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| gold-layer-trigger | {system}-gold-layer-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| historical-prices-policy | {system}-historical-prices-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-api-eclipse-scoped | eclipse-inf-api-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-assets-trigger-kms | {system}-inf-assets-trigger-kms-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-assets-trigger-policy | {system}-inf-assets-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-bronze-complete-emitter-scoped | {system}-inf-bronze-complete-emitter-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-bronze-trigger-policy | {system}-inf-bronze-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-ec2-launch-monitor-policy | {system}-inf-ec2-launch-monitor-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-ec2-retry-launch-kms | {system}-inf-ec2-retry-launch-kms-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-ec2-retry-launch-policy | {system}-inf-ec2-retry-launch-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-gold-trigger-policy | {system}-inf-gold-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-jwt-trigger-dynamo | {system}-inf-jwt-trigger-dynamo-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-jwt-trigger-kms | {system}-inf-jwt-trigger-kms-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-jwt-trigger-policy | {system}-inf-jwt-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-nna-partition-checker-scoped | {system}-inf-nna-partition-checker-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-s3-scoped | {system}-inf-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-silver-aggregator-policy | {system}-inf-silver-aggregator-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| inf-silver-chain-s3 | {system}-inf-silver-chain-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| infrastructure-ops-permissions | {system}-infrastructure-ops-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-price-update | {system}-invoke-price-update-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-publisher-fanout | {system}-invoke-publisher-fanout-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-smartx-assets-daily-pull | smartx-invoke-assets-daily-pull-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-smartx-rest-lambdas | smartx-invoke-rest-lambdas-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-start-automation | {system}-invoke-start-automation-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-the-accrual-trigger | {system}-invoke-the-accrual-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-the-daily-trigger-plus-dlq | {system}-invoke-the-daily-trigger-plus-dlq-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-the-dispatcher-plus-dlq | {system}-invoke-the-dispatcher-plus-dlq-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-the-feeder-trigger-plus-dlq | {system}-invoke-the-feeder-trigger-plus-dlq-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-the-mirror | {system}-invoke-the-mirror-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-the-publisher | {system}-invoke-the-publisher-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-the-session-trigger | {system}-invoke-the-session-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-the-two-feeders | {system}-invoke-the-two-feeders-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| invoke-trending-publisher | {system}-invoke-trending-publisher-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-49f-directory-read-policy | irpt-49f-directory-read-policy | CONFORMANT | IAM_POLICY | live |  |
| irpt-core-firm-49financial-prefix | irpt-49f-core-firm-prefix-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-core-firm-cottonwood-prefix | irpt-cot-core-firm-prefix-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-core-firm-inflection-prefix | irpt-inf-core-firm-prefix-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-core-quarantine-prefix | irpt-core-quarantine-prefix-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-directory-policy | irpt-directory-policy | CONFORMANT | IAM_POLICY | live |  |
| irpt-directory-refresh-policy | irpt-directory-refresh-policy | CONFORMANT | IAM_POLICY | live |  |
| irpt-directory-refresh-scheduler-policy | irpt-directory-refresh-scheduler-policy | CONFORMANT | IAM_POLICY | live |  |
| irpt-export-render-dispatch | irpt-export-render-dispatch-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-export-render-evidence | irpt-export-render-evidence-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-export-render-host-evidence | irpt-export-render-host-evidence-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-export-render-logs | irpt-export-render-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-holdings-firm-read | irpt-holdings-firm-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-holdings-logs | irpt-holdings-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-holdings-snapshot-scheduler-policy | irpt-holdings-snapshot-scheduler-policy | CONFORMANT | IAM_POLICY | live |  |
| irpt-intake-poll-invoke | irpt-intake-poll-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-intake-poller | irpt-intake-poller-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-narrative-logs | irpt-narrative-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-narrative-news-read | irpt-narrative-news-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-performance-adapter-logs | irpt-performance-adapter-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-status-policy | irpt-status-policy | CONFORMANT | IAM_POLICY | live |  |
| irpt-ycharts-generate | irpt-ycharts-generate-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| irpt-ycharts-runner | irpt-ycharts-runner-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| jwt-public-key-secret | {system}-jwt-public-key-secret-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| jwt-trigger-invoke | {system}-jwt-trigger-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| keyword-intelligence-dynamodb-and-invoke | {system}-keyword-intelligence-dynamodb-and-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| kms-ebs-decrypt | {system}-kms-ebs-decrypt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| kms-ebs-decrypt | {system}-kms-ebs-decrypt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| kms-ebs-decrypt | {system}-kms-ebs-decrypt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| kms-ebs-decrypt | {system}-kms-ebs-decrypt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| lambda-deploy | {system}-lambda-deploy-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| lambda-edge-ownership-map-read | {system}-lambda-edge-ownership-map-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| lambda-edge-secrets-logs | {system}-lambda-edge-secrets-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| lambda-edge-sns-alert | {system}-lambda-edge-sns-alert-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| lambda-invoke | {system}-lambda-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| lambda-invoke-finbert | {system}-lambda-invoke-finbert-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| layer3-bd-securities-read | {system}-49f-layer3-securities-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| market-data-generator-permissions | {system}-market-data-generator-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| market-update-dynamodb-scoped | {system}-market-update-dynamodb-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| market-update-lambda-policy | {system}-market-update-lambda-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| market-update-secrets-read | {system}-market-update-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| mdpf-accrual-trigger-scoped | mdpf-accrual-trigger-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| mdpf-feeder-trigger | mdpf-feeder-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| mdpf-gold-scoped | mdpf-gold-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| mdpf-runner-scoped | mdpf-runner-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| monolith-bd49f-xref-silver-read | {system}-monolith-bd49f-xref-silver-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| monolith-schwab-08242234-silver-read | schwab-08242234-monolith-silver-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| monolith-schwab-08335338-silver-read | schwab-08335338-monolith-silver-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-313476888478-lambda-artifacts#policy | opal-313476888478-lambda-artifacts#policy | CONFORMANT | IAM_POLICY | live |  |
| opal-advi-stitch-landing-scoped | advi-stitch-landing-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-amgt-scoped-api-grants | amgt-scoped-api-grants-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-bd49f-daily-pull-session-read | opal-assets-bd49f-daily-pull-session-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-bd49f-daily-pull-write-49f | opal-49f-assets-bd49f-daily-pull-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-bd49f-dim-convert-scheduler-invoke | opal-assets-bd49f-dim-convert-scheduler-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-bd49f-dim-convert-scoped | opal-assets-bd49f-dim-convert-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-bd49f-reporting-pull-io | opal-assets-bd49f-reporting-pull-io-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-bd49f-reporting-pull-session-read | opal-assets-bd49f-reporting-pull-session-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-daily-emitter-scoped | opal-assets-daily-emitter-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-ingest-router-read-sources | opal-assets-ingest-router-read-sources-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-mdpf-egress-publisher-live-serve | opal-assets-mdpf-egress-publisher-live-serve-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-mdpf-egress-publisher-scoped | opal-assets-mdpf-egress-publisher-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-mdpf-portal-publisher-scoped | opal-assets-mdpf-portal-publisher-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-one-way-fan-in-fence | opal-assets-one-way-fan-in-fence-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-bd49finsurance-read-bronze | opal-assets-silver-bd49finsurance-read-bronze-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-blackdiamond-read-bronze | opal-assets-silver-blackdiamond-read-bronze-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-dlq-access | opal-assets-silver-dlq-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-eclipse-read-bronze | opal-assets-silver-eclipse-read-bronze-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-etf-read-bronze | opal-assets-silver-etf-read-bronze-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-orion-read-bronze | opal-assets-silver-orion-read-bronze-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-schwab-read-bronze | opal-assets-silver-schwab-read-bronze-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-smartx-read-bronze | opal-assets-silver-smartx-read-bronze-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-bd49finsurance-blackdiamond | opal-assets-silver-write-bd49finsurance-blackdiamond-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-blackdiamond | opal-assets-silver-write-blackdiamond-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-eclipse | opal-assets-silver-write-eclipse-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-msn | opal-assets-silver-write-msn-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-orion | opal-assets-silver-write-orion-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-pathfinder | opal-assets-silver-write-pathfinder-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-schwab | opal-assets-silver-write-schwab-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-smartx | opal-assets-silver-write-smartx-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-silver-write-trueshares | opal-assets-silver-write-trueshares-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-write-blackdiamond | opal-assets-write-blackdiamond-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-write-eclipse | opal-assets-write-eclipse-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-assets-write-orion | opal-assets-write-orion-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-bedrock-invoke | opal-bedrock-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-cloudfront-invalidation | opal-cloudfront-invalidation-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-data-49financial#policy | opal-data-49financial#policy | CONFORMANT | IAM_POLICY | live |  |
| opal-data-assets#policy | opal-data-assets#policy | CONFORMANT | IAM_POLICY | live |  |
| opal-data-bd#policy | opal-data-49financial#policy | ALIAS | IAM_POLICY | live |  |
| opal-data-cot#policy | opal-data-cottonwood#policy | ALIAS | IAM_POLICY | live |  |
| opal-data-demo#policy | opal-data-demo#policy | CONFORMANT | IAM_POLICY | live |  |
| opal-data-inf#policy | opal-data-inflection#policy | ALIAS | IAM_POLICY | live |  |
| opal-data-portal-v2#policy | opal-data-portal-v2#policy | CONFORMANT | IAM_POLICY | live |  |
| opal-data-refresh-lambda-policy | opal-data-refresh-lambda-policy | CONFORMANT | IAM_POLICY | live |  |
| opal-gateway-access-admin-policy | gateway-access-admin-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-access-state-runtime | gateway-access-state-runtime-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-assume-emp-roles | gateway-assume-emp-roles-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-assume-schwab-readers | gateway-assume-schwab-readers-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-audit-lake-write | gateway-audit-lake-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-daily-reports-read | gateway-daily-reports-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-golive | gateway-golive-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-graph-read-secret-read | gateway-graph-read-secret-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-opal-portal-secret-read | gateway-opal-portal-secret-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-queryv0-portal-read | gateway-queryv0-portal-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-gateway-ycharts-secret-read | gateway-ycharts-secret-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-infrastructure-monitor | opal-infrastructure-monitor-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-ipblock-cli-row-only | opal-ipblock-cli-row-only-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-ipset-reconciler-table-stream-and-sets | opal-ipset-reconciler-table-stream-and-sets-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-mcp-emp-alyssa-onboard-policy | opal-mcp-emp-alyssa-onboard-policy | CONFORMANT | IAM_POLICY | live |  |
| opal-mcp-emp-alyssa-read-policy | opal-mcp-emp-alyssa-read-policy | CONFORMANT | IAM_POLICY | live |  |
| opal-mcp-emp-menachem-schwab-read-policy | opal-mcp-emp-menachem-schwab-read-policy | CONFORMANT | IAM_POLICY | live |  |
| opal-mcp-schwab-catalog-read-policy | opal-mcp-schwab-catalog-read-policy | CONFORMANT | IAM_POLICY | live |  |
| opal-ms-ingest-liveness | opal-ms-ingest-liveness-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-otp-liveness | opal-otp-liveness-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-portal-content-table-rw | opal-portal-content-table-rw-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-portal-dynamodb | opal-portal-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-portal-logs | opal-portal-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-portal-s3-read | opal-portal-s3-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-portal-secrets | opal-portal-secrets-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-research-pull-enqueue-grants | opal-research-pull-enqueue-grants-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-schwab-monolith-remap-inline | schwab-monolith-remap-inline-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-security-admin-evidence-and-key | opal-security-admin-evidence-and-key-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-sentinel-table-evidence-and-notify | opal-sentinel-table-evidence-and-notify-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-sessions-dynamodb | opal-sessions-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-sessions-secrets | opal-sessions-secrets-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-smartx-logs | smartx-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-smartx-s3-access | smartx-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-smartx-secrets | smartx-secrets-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-ticket-api-ses-send | opal-ticket-api-ses-send-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-tickets-table-rw | opal-tickets-table-rw-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-users-v2-access | opal-users-v2-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-website-s3-backup | opal-website-s3-backup-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opal-website-ses-send | opal-website-ses-send-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| opalinvest-auth-permissions | {system}-opalinvest-auth-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| outset-drift-publisher-laptop | {system}-outset-drift-publisher-laptop-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| partners-lambda-permissions | {system}-partners-lambda-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| pipeline-chain | {system}-pipeline-chain-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| pipeline-chain | {system}-pipeline-chain-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| portfolio-export-dynamodb | {system}-portfolio-export-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| portfolio-export-s3 | {system}-portfolio-export-s3-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| portfolio-s3-dynamodb | {system}-portfolio-s3-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| quartz-si2-monolith-write | {system}-quartz-si2-monolith-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| quartz-si2-spike-inline | {system}-quartz-si2-spike-inline-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| runner-shared-read | {system}-runner-shared-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| runner-shared-read | {system}-runner-shared-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-accounts-v2 | {system}-s3-accounts-v2-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-assets-v2 | {system}-s3-assets-v2-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-billing | {system}-s3-billing-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-etf-ownership | {system}-s3-etf-ownership-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-etf-ownership | {system}-s3-etf-ownership-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-etf-ownership | {system}-s3-etf-ownership-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-etfs-presentation | etfs-s3-presentation-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-etfs-read | etfs-s3-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-otp-rw | {system}-s3-otp-rw-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-performance | {system}-s3-performance-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-portal-write | {system}-s3-portal-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-positions | {system}-s3-positions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-qa-scoped | {system}-s3-qa-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-rate-limit-state | {system}-s3-rate-limit-state-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-read-cot-bronze-write-cot-platinum | {system}-cot-s3-read-bronze-write-platinum-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-read-etfs-daily | etfs-s3-read-daily-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-read-three-inputs-write-satellites-characteristics | {system}-s3-read-three-inputs-write-satellites-characteristics-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-reps | {system}-s3-reps-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-rw-etfs-bronze-silver | etfs-s3-rw-bronze-silver-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-rw-etfs-gold-platinum | etfs-s3-rw-gold-platinum-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-scoped-cot | {system}-cot-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-scoped-inf | {system}-inf-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-scoped-inf | {system}-inf-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-scoped-inf-exporter | {system}-inf-s3-scoped-exporter-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-tax | {system}-s3-tax-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-txn | {system}-s3-txn-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| s3-unified-account-dim | {system}-s3-unified-account-dim-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| schwab-bucket-access | schwab-bucket-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secrets-access | {system}-secrets-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secrets-manager-orion | orion-secrets-manager-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secrets-manager-orion-jwt | orion-secrets-manager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secrets-manager-orion-jwt-read | orion-secrets-manager-jwt-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secrets-read-otp-token | {system}-secrets-read-otp-token-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| self-shutdown | {system}-self-shutdown-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| self-stop | {system}-self-stop-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| self-stop | {system}-self-stop-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| send-daily-pull-command | {system}-send-daily-pull-command-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ses-send-email | {system}-ses-send-email-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ses-send-noreply | {system}-ses-send-noreply-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| smartx-assets-pull-access | smartx-assets-pull-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| smartx-assets-pull-invoke-silver-converter | smartx-assets-pull-invoke-silver-converter-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| smartx-dynamodb-access | smartx-dynamodb-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| smartx-jwt-refresher-access | smartx-jwt-refresher-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| smartx-rest-pull-access | smartx-rest-pull-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| smartx-s3-access | smartx-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| sms-send-text-message | {system}-sms-send-text-message-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| sns-otp-alert | {system}-sns-otp-alert-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| sns-otp-alert | {system}-sns-otp-alert-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| sns-publish-chainfatal | {system}-sns-publish-chainfatal-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| sscn-cloudwatch-logs | {system}-sscn-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| sscn-s3-access | {system}-sscn-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ssm-access | {system}-ssm-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ssm-access | {system}-ssm-access-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ssm-send-command-inf-jwt-fetch | {system}-inf-ssm-send-command-jwt-fetch-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| start-consolidation-gold-runner | {system}-start-consolidation-gold-runner-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| workspace-sync-permissions | {system}-workspace-sync-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| wsb-49f-model-aua-daily | mdpf-49f-wsb-model-aua-daily-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| wsd-49f-partner-held-etf-daily | mdpf-49f-wsd-partner-held-etf-daily-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| yang-pipeline-lambda-permissions | yang-pipeline-lambda-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| yang-pipeline-sfn-permissions | yang-pipeline-sfn-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| yang-qa-scratch-access-20260803 | yang-qa-scratch-access-20260803-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| yang-varflag-check-scoped | yang-varflag-check-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ycharts-capture-secrets | ycharts-capture-secrets-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ycharts-market-data-pull-secrets-read | ycharts-market-data-pull-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ycharts-probe-invoke-capture | ycharts-probe-invoke-capture-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ycharts-session-metric-write | ycharts-session-metric-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| ycharts-session-read | ycharts-session-read-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| yield-curve-artifact-write | {system}-yield-curve-artifact-write-policy | OUT-OF-PATTERN | IAM_POLICY | live |  |
| FredIngestionLambdaRole | fred-ingestion-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| FredMacroIngestionLambdaRole | fred-macro-ingestion-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| YChartsMarketDataPullLambdaRole | ycharts-market-data-pull-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| YChartsSessionCaptureLambdaRole | ycharts-session-capture-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| YChartsSessionProbeLambdaRole | ycharts-session-probe-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| advi-49f-floor-scheduler-role | advi-49f-floor-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| advi-49f-gold-dispatch-role | advi-49f-gold-dispatch-role | CONFORMANT | IAM_ROLE | live |  |
| agentbus-alyssa01-fleet-andrew-role | agentbus-alyssa01-fleet-andrew-role | CONFORMANT | IAM_ROLE | live |  |
| agentbus-sim01-fleet-alpha-role | agentbus-sim01-fleet-alpha-role | CONFORMANT | IAM_ROLE | live |  |
| agentbus-sim01-fleet-beta-role | agentbus-sim01-fleet-beta-role | CONFORMANT | IAM_ROLE | live |  |
| amgt-resapp-chatter-axis-lambda-role | amgt-resapp-chatter-axis-lambda-role | CONFORMANT | IAM_ROLE | live |  |
| amgt-resapp-chatter-axis-scheduler-role | amgt-resapp-chatter-axis-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| bd-49f-auto-login-role | blackdiamond-49f-auto-login-role | ALIAS | IAM_ROLE | live |  |
| bd-49f-etf-ownership-daily-role | blackdiamond-49f-etf-ownership-daily-role | ALIAS | IAM_ROLE | live |  |
| bd-49f-fees-runner-role | blackdiamond-49f-fees-runner-role | ALIAS | IAM_ROLE | live |  |
| bd-49f-keepalive-role | blackdiamond-49f-keepalive-role | ALIAS | IAM_ROLE | live |  |
| bd-49f-runner-role | blackdiamond-49f-runner-role | ALIAS | IAM_ROLE | live |  |
| bd-49f-session-trigger-role | blackdiamond-49f-session-trigger-role | ALIAS | IAM_ROLE | live |  |
| bd-allocation-checker-lambda-role | {system}-49f-allocation-checker-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-allocation-processor-role | {system}-49f-allocation-processor-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-cot-keepalive-role | blackdiamond-cot-keepalive-role | ALIAS | IAM_ROLE | live |  |
| bd-daily-trigger-lambda-role | {system}-49f-daily-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-exporter-ec2-role | {system}-49f-exporter-ec2-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-gold-detail-generator-role | {system}-49f-gold-detail-generator-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-gold-eventbridge-step-functions-role | {system}-49f-gold-eventbridge-step-functions-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-gold-layer-lambda-role | {system}-49f-gold-layer-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-gold-step-functions-role | {system}-49f-gold-step-functions-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-merge-daily-lambda-role | {system}-49f-merge-daily-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-pipeline-task-role | {system}-49f-pipeline-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-processor-lambda-role | {system}-49f-processor-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| bd-silver-merge-role | advi-49f-silver-merge-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| canonical-schwab-si2-daily-events-ssm-role | schwab-canonical-si2-daily-events-ssm-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| codebuild-semantic-clustering-role | {system}-codebuild-semantic-clustering-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| consolidation-gold-runner-automation-start-role | {system}-consolidation-gold-runner-automation-start-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| consolidation-gold-runner-events-invoke-ssm-role | {system}-consolidation-gold-runner-events-invoke-ssm-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| consolidation-gold-runner-role | {system}-consolidation-gold-runner-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| cot-bd-session-trigger-lambda-role | blackdiamond-cot-session-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| cot-etf-ownership-daily-role | etfs-cot-etf-ownership-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| cot-exporter-ec2-role | advi-cot-exporter-ec2-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| cot-gold-layer-ec2-role | advi-cot-gold-layer-ec2-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| cot-rebalancer-runner-role | mdpf-cot-rebalancer-runner-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| cot-satellites-characteristics-producer-role | etfs-cot-satellites-characteristics-producer-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| cot-satellites-registry-producer-role | etfs-cot-satellites-registry-producer-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| cot-session-scheduler-role | {system}-cot-session-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| daily-sprint-generator-role | {system}-daily-sprint-generator-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| deck-generation-lambda-role | {system}-deck-generation-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| demo-transform-runner-ec2-role | advi-demo-transform-runner-ec2-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| ec2-auto-shutdown-enforcer-role | {system}-ec2-auto-shutdown-enforcer-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| ec2-ssm-role | {system}-ec2-ssm-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| ecsTaskExecutionRole | {system}-ecs-task-execution-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| estate-capture-writer | estate-capture-writer-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| estate-report-orchestrator-role | estate-report-orchestrator-role | CONFORMANT | IAM_ROLE | live |  |
| estate-report-runner-role | estate-report-runner-role | CONFORMANT | IAM_ROLE | live |  |
| estate-report-scheduler-role | estate-report-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| estate-report-seam-freshness-publisher | estate-report-seam-freshness-publisher-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| estate-report-seam-freshness-scheduler | estate-report-seam-freshness-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| etf-ownership-dashboard-role | etfs-etf-ownership-dashboard-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| etf-positioning-producer-role | etfs-etf-positioning-producer-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| etfs-avgcap-reader-role | etfs-avgcap-reader-role | CONFORMANT | IAM_ROLE | live |  |
| etfs-canon-fanin-role | etfs-canon-fanin-role | CONFORMANT | IAM_ROLE | live |  |
| etfs-netassets-daily-role | etfs-netassets-daily-role | CONFORMANT | IAM_ROLE | live |  |
| etfs-reports-orchestrator-role | etfs-reports-orchestrator-role | CONFORMANT | IAM_ROLE | live |  |
| etfs-reports-reporter-role | etfs-reports-reporter-role | CONFORMANT | IAM_ROLE | live |  |
| etfs-reports-scheduler-role | etfs-reports-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| exec-summary-generator-role | {system}-exec-summary-generator-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| finbert-ec2-backfill-role | {system}-finbert-ec2-backfill-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| find-insure-lambda-role | {system}-find-insure-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| gateway-schwab-catalog-read-role | gateway-schwab-catalog-read-role | CONFORMANT | IAM_ROLE | live |  |
| gateway-schwab-read-role | gateway-schwab-read-role | CONFORMANT | IAM_ROLE | live |  |
| github-actions-opal-deploy | {system}-github-actions-opal-deploy-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| gldinc-ss4c-canary-role | {system}-gldinc-ss4c-canary-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| globgrph-derive-build-role | globgrph-derive-build-role | CONFORMANT | IAM_ROLE | live |  |
| historical-prices-lambda-role | {system}-historical-prices-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-accounts-v2-daily-role | advi-inf-accounts-v2-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-api-assets-v2-lambda-role | advi-inf-api-assets-v2-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-api-eclipse-role | eclipse-inf-api-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-api-positions-role | advi-inf-api-positions-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-api-reps-role | advi-inf-api-reps-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-api-txn-role | advi-inf-api-txn-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-assets-trigger-lambda-role | advi-inf-assets-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-billing-daily-role | advi-inf-billing-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-bronze-complete-emitter-role | advi-inf-bronze-complete-emitter-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-bronze-runner-ec2-role | advi-inf-bronze-runner-ec2-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-bronze-trigger-lambda-role | advi-inf-bronze-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-ec2-launch-monitor-lambda-role | advi-inf-ec2-launch-monitor-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-ec2-retry-launch-lambda-role | advi-inf-ec2-retry-launch-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-etf-ownership-daily-role | etfs-inf-etf-ownership-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-eventbridge-ssm-role | advi-inf-eventbridge-ssm-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-exporter-ec2-role | advi-inf-exporter-ec2-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-gold-layer-ec2-role | advi-inf-gold-layer-ec2-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-gold-layer-lambda-role | advi-inf-gold-layer-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-gold-qa-runner-ec2-role | advi-inf-gold-qa-runner-ec2-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-gold-trigger-lambda-role | advi-inf-gold-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-jwt-trigger-lambda-role | advi-inf-jwt-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-nna-partition-checker-lambda-role | advi-inf-nna-partition-checker-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-otp-relay-lambda-role | advi-inf-otp-relay-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-performance-daily-role | advi-inf-performance-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-silver-aggregator-lambda-role | advi-inf-silver-aggregator-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-silver-chain-lambda-role | advi-inf-silver-chain-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-tax-daily-role | advi-inf-tax-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| inf-unified-account-dim-daily-role | advi-inf-unified-account-dim-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| infrastructure-ops-lambda-role | {system}-infrastructure-ops-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| infrastructure-snapshot-role | {system}-infrastructure-snapshot-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| irpt-49f-directory-read-role | irpt-49f-directory-read-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-core-firm-49financial | irpt-49f-core-firm-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| irpt-core-firm-cottonwood | irpt-cot-core-firm-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| irpt-core-firm-inflection | irpt-inf-core-firm-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| irpt-core-quarantine | irpt-core-quarantine-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| irpt-directory-refresh-role | irpt-directory-refresh-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-directory-refresh-scheduler-role | irpt-directory-refresh-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-directory-role | irpt-directory-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-export-render-role | irpt-export-render-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-holdings-role | irpt-holdings-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-holdings-snapshot-scheduler-role | irpt-holdings-snapshot-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-intake-poll-role | irpt-intake-poll-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-intake-poller-role | irpt-intake-poller-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-narrative-role | irpt-narrative-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-performance-adapter-role | irpt-performance-adapter-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-status-role | irpt-status-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-ycharts-generate-role | irpt-ycharts-generate-role | CONFORMANT | IAM_ROLE | live |  |
| irpt-ycharts-runner-role | irpt-ycharts-runner-role | CONFORMANT | IAM_ROLE | live |  |
| lambda-access-anomaly-scanner-role | {system}-lambda-access-anomaly-scanner-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| lambda-cost-anomaly-scanner-role | {system}-lambda-cost-anomaly-scanner-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| lambda-ec2-runtime-monitor-role | {system}-lambda-ec2-runtime-monitor-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| lambda-edge-execution-role | {system}-lambda-edge-execution-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| lambda-execution-role | {system}-lambda-execution-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| lambda-test-role | {system}-lambda-test-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| market-data-generator-lambda-role | {system}-market-data-generator-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| market-update-lambda-role | {system}-market-update-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| mdpf-accrual-scheduler-role | mdpf-accrual-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| mdpf-accrual-trigger-role | mdpf-accrual-trigger-role | CONFORMANT | IAM_ROLE | live |  |
| mdpf-daily-runner-ec2-role | mdpf-daily-runner-ec2-role | CONFORMANT | IAM_ROLE | live |  |
| mdpf-feeder-scheduler-role | mdpf-feeder-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| mdpf-feeder-trigger-role | mdpf-feeder-trigger-role | CONFORMANT | IAM_ROLE | live |  |
| mdpf-floor-scheduler-role | mdpf-floor-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| mdpf-gold-lambda-role | mdpf-gold-lambda-role | CONFORMANT | IAM_ROLE | live |  |
| opal-49f-served-guard | opal-49f-served-guard-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-advi-stitch-landing-role | advi-stitch-landing-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-amgt-scoped-api-role | amgt-scoped-api-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-assets-bd49f-daily-pull-role | opal-assets-bd49f-daily-pull-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-bd49f-dim-convert-role | opal-assets-bd49f-dim-convert-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-bd49f-dim-convert-scheduler-role | opal-assets-bd49f-dim-convert-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-bd49f-reporting-pull-role | opal-assets-bd49f-reporting-pull-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-daily-emitter-role | opal-assets-daily-emitter-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-ingest-router-role | opal-assets-ingest-router-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-mdpf-egress-publisher-role | opal-assets-mdpf-egress-publisher-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-mdpf-portal-publisher-role | opal-assets-mdpf-portal-publisher-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-mdpf-portal-publisher-scheduler-role | opal-assets-mdpf-portal-publisher-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-mirror-cot-scheduler-role | opal-cot-assets-mirror-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-assets-silver-bd49finsurance-role | opal-assets-silver-bd49finsurance-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-silver-blackdiamond-role | opal-assets-silver-blackdiamond-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-silver-eclipse-role | opal-assets-silver-eclipse-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-silver-etf-role | opal-assets-silver-etf-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-silver-orion-role | opal-assets-silver-orion-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-silver-schwab-role | opal-assets-silver-schwab-role | CONFORMANT | IAM_ROLE | live |  |
| opal-assets-silver-smartx-role | opal-assets-silver-smartx-role | CONFORMANT | IAM_ROLE | live |  |
| opal-bloomberg-tunnel-instance-role | bloomberg-tunnel-instance-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-cot-served-guard | opal-cot-served-guard-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-cot-value-parity | opal-cot-value-parity-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-data-refresh-lambda-role | opal-data-refresh-lambda-role | CONFORMANT | IAM_ROLE | live |  |
| opal-drift-producer-codebuild-role | opal-drift-producer-codebuild-role | CONFORMANT | IAM_ROLE | live |  |
| opal-drift-producer-events-role | opal-drift-producer-events-role | CONFORMANT | IAM_ROLE | live |  |
| opal-drift-producer-gha-role | opal-drift-producer-gha-role | CONFORMANT | IAM_ROLE | live |  |
| opal-gateway-access-admin | gateway-access-admin-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-gateway-role | gateway-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-comp-learns-producer-events | globgrph-comp-learns-producer-events-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-comp-learns-producer-task | globgrph-comp-learns-producer-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-cse-producer-scheduler | globgrph-cse-producer-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-cse-producer-task | globgrph-cse-producer-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-derive-runner-events | globgrph-derive-runner-events-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-derive-runner-execution | globgrph-derive-runner-execution-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-derive-runner-task | globgrph-derive-runner-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-fedobs-emitter-task | globgrph-fedobs-emitter-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-fedobs-producer-events | globgrph-fedobs-producer-events-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-incremental-updater | globgrph-incremental-updater-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-nessie-execution | globgrph-nessie-execution-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-nessie-task | globgrph-nessie-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-projection-pipe | globgrph-projection-pipe-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-projection-worker | globgrph-projection-worker-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-projection-worker-execution | globgrph-projection-worker-execution-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-resource-summaries-producer-task | globgrph-resource-summaries-producer-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-serving-task | globgrph-serving-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-trino-execution | globgrph-trino-execution-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-globgrph-trino-task | globgrph-trino-task-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-inf-served-guard | opal-inf-served-guard-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-inf-value-parity | opal-inf-value-parity-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-ipblock-cli | opal-ipblock-cli-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-ipset-reconciler | opal-ipset-reconciler-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-lambda-market-rsi-role | opal-lambda-market-rsi-role | CONFORMANT | IAM_ROLE | live |  |
| opal-layer3-ec2-role | opal-layer3-ec2-role | CONFORMANT | IAM_ROLE | live |  |
| opal-mcp-emp-alyssa-onboard | opal-mcp-emp-alyssa-onboard-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-mcp-emp-alyssa-read | opal-mcp-emp-alyssa-read-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-mcp-emp-menachem-schwab-read | opal-mcp-emp-menachem-schwab-read-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-mcp-schwab-catalog-read | opal-mcp-schwab-catalog-read-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-ms-ingest-liveness-role | opal-ms-ingest-liveness-role | CONFORMANT | IAM_ROLE | live |  |
| opal-otp-liveness-role | opal-otp-liveness-role | CONFORMANT | IAM_ROLE | live |  |
| opal-portal-content-api-role | opal-portal-content-api-role | CONFORMANT | IAM_ROLE | live |  |
| opal-portal-lambda-role | opal-portal-lambda-role | CONFORMANT | IAM_ROLE | live |  |
| opal-research-pull-enqueue-role | opal-research-pull-enqueue-role | CONFORMANT | IAM_ROLE | live |  |
| opal-schwab-monolith-remap-role | schwab-monolith-remap-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-security-admin | opal-security-admin-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-security-scanner-processor-role | opal-security-scanner-processor-role | CONFORMANT | IAM_ROLE | live |  |
| opal-sentinel | opal-sentinel-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-smartx-lambda-role | smartx-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| opal-stitch-produce-codebuild-role | opal-stitch-produce-codebuild-role | CONFORMANT | IAM_ROLE | live |  |
| opal-stitch-produce-events-role | opal-stitch-produce-events-role | CONFORMANT | IAM_ROLE | live |  |
| opal-stitch-source-gha-role | opal-stitch-source-gha-role | CONFORMANT | IAM_ROLE | live |  |
| opal-surface-check-publish-gha-role | opal-surface-check-publish-gha-role | CONFORMANT | IAM_ROLE | live |  |
| opal-ticket-api-role | opal-ticket-api-role | CONFORMANT | IAM_ROLE | live |  |
| opal-website-dlm-role | opal-website-dlm-role | CONFORMANT | IAM_ROLE | live |  |
| opal-website-wp-role | opal-website-wp-role | CONFORMANT | IAM_ROLE | live |  |
| opalinvest-auth-lambda-role | {system}-opalinvest-auth-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| outset-drift-publisher-laptop | {system}-outset-drift-publisher-laptop-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| partner-etl-ops-sqs-consumer-role | {system}-partner-etl-ops-sqs-consumer-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| partners-lambda-role | {system}-partners-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| portfolio-export-lambda-role | {system}-portfolio-export-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| portfolio-management-lambda-role | {system}-portfolio-management-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| quartz-si2-spike-role | {system}-quartz-si2-spike-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| rds-monitoring-role | {system}-rds-monitoring-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| schwab-anonymizer-lambda-role | schwab-anonymizer-lambda-role | CONFORMANT | IAM_ROLE | live |  |
| seeking-alpha-scraper-role | seeking-alpha-scraper-role | CONFORMANT | IAM_ROLE | live |  |
| smartx-assets-pull-role | smartx-assets-pull-role | CONFORMANT | IAM_ROLE | live |  |
| smartx-assets-pull-scheduler-role | smartx-assets-pull-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| smartx-exporter-role-20251218220948293500000001 | smartx-exporter-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| smartx-ingestion-lambda-role | smartx-ingestion-lambda-role | CONFORMANT | IAM_ROLE | live |  |
| smartx-jwt-refresher-role | smartx-jwt-refresher-role | CONFORMANT | IAM_ROLE | live |  |
| smartx-rest-pull-role | smartx-rest-pull-role | CONFORMANT | IAM_ROLE | live |  |
| smartx-rest-scheduler-role | smartx-rest-scheduler-role | CONFORMANT | IAM_ROLE | live |  |
| workspace-sync-lambda-role | {system}-workspace-sync-lambda-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| wp5-49f-feeder-scheduler-role | mdpf-49f-wp5-feeder-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| wsb-49f-model-aua-daily-role | mdpf-49f-wsb-model-aua-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| wsd-49f-partner-held-etf-daily-role | mdpf-49f-wsd-partner-held-etf-daily-role | OUT-OF-PATTERN | IAM_ROLE | live |  |
| yang-pipeline-lambda-role | yang-pipeline-lambda-role | CONFORMANT | IAM_ROLE | live |  |
| yang-pipeline-sfn-role | yang-pipeline-sfn-role | CONFORMANT | IAM_ROLE | live |  |
| yang-varflag-check-role | yang-varflag-check-role | CONFORMANT | IAM_ROLE | live |  |
| bd-49f-auto-login-profile | blackdiamond-49f-auto-login-profile | ALIAS | INSTANCE_PROFILE | live |  |
| bd-exporter-profile | {system}-49f-exporter-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| bd-gold-detail-generator-profile | {system}-49f-gold-detail-generator-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| consolidation-gold-runner-profile | {system}-consolidation-gold-runner-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| cot-exporter-profile | {system}-cot-exporter-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| estate-report-runner-profile | estate-report-runner-profile | CONFORMANT | INSTANCE_PROFILE | live |  |
| etfs-reports-reporter-profile | etfs-reports-reporter-profile | CONFORMANT | INSTANCE_PROFILE | live |  |
| inf-bronze-runner-profile | {system}-inf-bronze-runner-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| inf-exporter-profile | {system}-inf-exporter-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| inf-gold-layer-profile | {system}-inf-gold-layer-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| inf-gold-qa-runner-profile | {system}-inf-gold-qa-runner-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| irpt-ycharts-runner-profile | irpt-ycharts-runner-profile | CONFORMANT | INSTANCE_PROFILE | live |  |
| mdpf-daily-runner-profile | mdpf-daily-runner-profile | CONFORMANT | INSTANCE_PROFILE | live |  |
| opal-gateway-profile | gateway-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| opal-website-wp-profile | opal-website-wp-profile | CONFORMANT | INSTANCE_PROFILE | live |  |
| quartz-si2-spike-profile | {system}-quartz-si2-spike-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| seeking-alpha-scraper-role | seeking-alpha-scraper-role-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| smartx-exporter-profile-20251218220948955300000004 | smartx-exporter-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | live |  |
| access-anomaly-scanner | {system}-access-anomaly-scanner-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| advi-49f-gold-dispatch | advi-49f-gold-dispatch-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| amgt-resapp-chatter-axis | amgt-resapp-chatter-axis-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| auth-validator-edge | {system}-auth-validator-edge-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-49f-etf-ownership-daily | blackdiamond-49f-etf-ownership-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-49f-fees-runner | blackdiamond-49f-fees-runner-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-49f-keepalive | blackdiamond-49f-keepalive-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-49f-runner | blackdiamond-49f-runner-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-49f-session-trigger | blackdiamond-49f-session-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-allocation-file-checker | {system}-49f-allocation-file-checker-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-allocation-processor | {system}-49f-allocation-processor-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-allocation-trigger | {system}-49f-allocation-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-asset-dim-trigger | {system}-49f-asset-dim-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-cot-keepalive | blackdiamond-cot-keepalive-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-fees-trigger | {system}-49f-fees-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-gold-trigger | {system}-49f-gold-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-incrparity-trigger | {system}-49f-incrparity-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-price-update | {system}-49f-price-update-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-realized-trigger | {system}-49f-realized-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-silver-merge | advi-49f-silver-merge-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-transactions-trigger | {system}-49f-transactions-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| bd-unrealized-trigger | {system}-49f-unrealized-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| cost-anomaly-scanner | {system}-cost-anomaly-scanner-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| cot-bd-session-trigger | blackdiamond-cot-session-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| cot-etf-ownership-daily | etfs-cot-etf-ownership-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| cot-rebalancer-runner | mdpf-cot-rebalancer-runner-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| cot-satellites-characteristics-producer | etfs-cot-satellites-characteristics-producer-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| cot-satellites-registry-producer | etfs-cot-satellites-registry-producer-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| daily-agenda-generator | {system}-daily-agenda-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| daily-sprint-generator | {system}-daily-sprint-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| deck-generation | {system}-deck-generation-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| ec2-auto-shutdown-enforcer | {system}-ec2-auto-shutdown-enforcer-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| ec2-runtime-monitor | {system}-ec2-runtime-monitor-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| estate-report-orchestrator | estate-report-orchestrator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| etf-ownership-dashboard | etfs-etf-ownership-dashboard-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| etf-positioning-producer | etfs-etf-positioning-producer-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| etfs-canon-fanin | etfs-canon-fanin-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| etfs-netassets-daily | etfs-netassets-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| etfs-reports-orchestrator | etfs-reports-orchestrator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| exec-summary-generator | {system}-exec-summary-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| finbert-batch-processor | {system}-finbert-batch-processor-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| find-insure-crawl-web | {system}-find-insure-crawl-web-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| find-insure-crawl-web-scraping-browser | {system}-find-insure-crawl-web-scraping-browser-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| find-insure-parse-web | {system}-find-insure-parse-web-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| find-insure-score-web | {system}-find-insure-score-web-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| fred-data-ingestion | fred-data-ingestion-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| fred-macro-ingestion | fred-macro-ingestion-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| gldinc-ss4c-canary | {system}-gldinc-ss4c-canary-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| historical-prices-scheduler | {system}-historical-prices-scheduler-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-accounts-v2-daily | advi-inf-accounts-v2-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-api-assets-v2 | advi-inf-api-assets-v2-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-api-eclipse | eclipse-inf-api-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-api-positions | advi-inf-api-positions-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-api-reps | advi-inf-api-reps-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-api-txn | advi-inf-api-txn-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-assets-trigger | advi-inf-assets-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-billing-daily | advi-inf-billing-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-bronze-complete-emitter | advi-inf-bronze-complete-emitter-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-bronze-trigger | advi-inf-bronze-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-client-detail | advi-inf-client-detail-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-ec2-launch-monitor | advi-inf-ec2-launch-monitor-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-ec2-retry-launch | advi-inf-ec2-retry-launch-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-etf-ownership-daily | etfs-inf-etf-ownership-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-gold-trigger | advi-inf-gold-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-jwt-trigger | advi-inf-jwt-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-nna-partition-checker | advi-inf-nna-partition-checker-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-otp-relay | advi-inf-otp-relay-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-performance-daily | advi-inf-performance-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-portal-advisor-publisher | advi-inf-portal-advisor-publisher-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-portal-publisher | {system}-inf-portal-publisher-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-silver-aggregator | advi-inf-silver-aggregator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-silver-chain | advi-inf-silver-chain-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-tax-daily | advi-inf-tax-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| inf-unified-account-dim-daily | advi-inf-unified-account-dim-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| infrastructure-daily-snapshot | {system}-infrastructure-daily-snapshot-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-directory-refresh | irpt-directory-refresh-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-directory-search | irpt-directory-search-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-export-render | irpt-export-render-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-holdings | irpt-holdings-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-intake-poller | irpt-intake-poller-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-narrative | irpt-narrative-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-performance-adapter | irpt-performance-adapter-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-status | irpt-status-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| irpt-ycharts-generate | irpt-ycharts-generate-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| keyword-intelligence-generator | {system}-keyword-intelligence-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| market-update-data-aggregator | {system}-market-update-data-aggregator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| market-update-exporter | {system}-market-update-exporter-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| market-update-generator | {system}-market-update-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| mdpf-accrual-trigger | mdpf-accrual-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| mdpf-feeder-trigger | mdpf-feeder-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| mdpf-gold-lambda | mdpf-gold-lambda | CONFORMANT | LAMBDA | live |  |
| opal-49f-served-guard | opal-49f-served-guard-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-amgt-scoped-api | amgt-scoped-api-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-bd49f-daily-pull | opal-assets-bd49f-daily-pull-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-bd49f-dim-convert | opal-assets-bd49f-dim-convert-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-bd49f-reporting-pull | opal-assets-bd49f-reporting-pull-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-daily-emitter | opal-assets-daily-emitter-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-ingest-mirror | opal-assets-ingest-mirror-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-mdpf-portal-publisher | opal-assets-mdpf-portal-publisher-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-silver-bd49finsurance | opal-assets-silver-bd49finsurance-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-silver-blackdiamond | opal-assets-silver-blackdiamond-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-silver-eclipse | opal-assets-silver-eclipse-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-silver-etf | opal-assets-silver-etf-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-silver-orion | opal-assets-silver-orion-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-silver-schwab | opal-assets-silver-schwab-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-assets-silver-smartx | opal-assets-silver-smartx-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-bd-transaction-consolidator | opal-49f-transaction-consolidator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-cot-served-guard | opal-cot-served-guard-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-cot-value-parity | opal-cot-value-parity-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-data-refresh-api | opal-data-refresh-api-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-data-refresh-api-qa-scratch | opal-data-refresh-api-qa-scratch-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-globgrph-incremental-updater | globgrph-incremental-updater-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-inf-served-guard | opal-inf-served-guard-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-inf-value-parity | opal-inf-value-parity-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-infrastructure-monitor | opal-infrastructure-monitor-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-ipset-reconciler | opal-ipset-reconciler-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-keyword-drilldown-generator | opal-keyword-drilldown-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-market-overview-tiered-generator | opal-market-overview-tiered-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-market-regime-classifier | opal-market-regime-classifier-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-market-rsi-tiered-generator | opal-market-rsi-tiered-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-ms-ingest-liveness | opal-ms-ingest-liveness-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-otp-liveness | opal-otp-liveness-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-partners-data | opal-partners-data-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-pm-optimization-autosave-put | opal-pm-optimization-autosave-put-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-pm-optimization-loader | opal-pm-optimization-loader-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-pm-snapshot-handler | opal-pm-snapshot-handler-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-pm-upload-urls | opal-pm-upload-urls-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portal-authorizer | opal-portal-authorizer-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portal-content-api | opal-portal-content-api-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portal-data-proxy | opal-portal-data-proxy-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portal-fear-greed-fetcher | opal-portal-fear-greed-fetcher-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portal-rest-authorizer | opal-portal-rest-authorizer-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portal-volatility-fetcher | opal-portal-volatility-fetcher-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portfolio-autosave-get | opal-portfolio-autosave-get-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portfolio-autosave-put | opal-portfolio-autosave-put-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portfolio-excel-generator | opal-portfolio-excel-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portfolio-export-download | opal-portfolio-export-download-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portfolio-funds-list | opal-portfolio-funds-list-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portfolio-pickle-parser | opal-portfolio-pickle-parser-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portfolio-version-get | opal-portfolio-version-get-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-portfolio-versions-list | opal-portfolio-versions-list-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-research-pull-enqueue | opal-research-pull-enqueue-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-security-scanner-processor | opal-security-scanner-processor-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-sentinel | opal-sentinel-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-session-analytics | opal-session-analytics-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-smartx-ingestion-pipeline | smartx-ingestion-pipeline-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-ticket-api | opal-ticket-api-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-trending-image-generator | opal-trending-image-generator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opal-trending-topics-portal-publisher | opal-trending-topics-portal-publisher-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| opalinvest-auth-handler | {system}-opalinvest-auth-handler-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| partner-etl-ops-sqs-consumer | {system}-partner-etl-ops-sqs-consumer-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| public-data-router | {system}-public-data-router-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| schwab-anonymizer | schwab-anonymizer-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| seeking-alpha-analysis-coordinator | seeking-alpha-analysis-coordinator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| seeking-alpha-analysis-dedup | seeking-alpha-analysis-dedup-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| seeking-alpha-analysis-listing-parser | seeking-alpha-analysis-listing-parser-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| seeking-alpha-analysis-scraper | seeking-alpha-analysis-scraper-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| seeking-alpha-news-coordinator | seeking-alpha-news-coordinator-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| seeking-alpha-news-dedup | seeking-alpha-news-dedup-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| seeking-alpha-news-scraper | seeking-alpha-news-scraper-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| semantic-trending-topics-portal-publisher | {system}-semantic-trending-topics-portal-publisher-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| shared-advisor-router | {system}-shared-advisor-router-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| shared-advisor-router-response | {system}-shared-advisor-router-response-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| smartx-assets-daily-pull | smartx-assets-daily-pull-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| smartx-jwt-refresher | smartx-jwt-refresher-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| smartx-rest-pull | smartx-rest-pull-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| wsb-49f-model-aua-daily | mdpf-49f-wsb-model-aua-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| wsd-49f-partner-held-etf-daily | mdpf-49f-wsd-partner-held-etf-daily-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-canon-interlock | yang-canon-interlock-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-capture-output-versions | yang-capture-output-versions-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-cleanup-uploads | yang-cleanup-uploads-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-allocation-summary | yang-generate-allocation-summary-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-cma | yang-generate-cma-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-correlation | yang-generate-correlation-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-etf-returns | yang-generate-etf-returns-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-factor-tilts | yang-generate-factor-tilts-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-holdings-attribution | yang-generate-holdings-attribution-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-latest | yang-generate-latest-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-macro | yang-generate-macro-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-macro-timeseries | yang-generate-macro-timeseries-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-manifest | yang-generate-manifest-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-peer-performance | yang-generate-peer-performance-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-positioning | yang-generate-positioning-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-risk-premium | yang-generate-risk-premium-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-valuation | yang-generate-valuation-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-generate-volatility | yang-generate-volatility-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-get-prior-metadata | yang-get-prior-metadata-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-ingest-dynamodb | yang-ingest-dynamodb-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-invalidate-cloudfront | yang-invalidate-cloudfront-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-model-portfolio-benchmarks | yang-model-portfolio-benchmarks-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-move-to-processed | yang-move-to-processed-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-pipeline-trigger | yang-pipeline-trigger-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-refresh-fred-cache | yang-refresh-fred-cache-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-time-machine | yang-time-machine-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-validate-files | yang-validate-files-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| yang-varflag-check | yang-varflag-check-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| ycharts-market-data-pull | ycharts-market-data-pull-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| ycharts-session-capture | ycharts-session-capture-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| ycharts-session-probe | ycharts-session-probe-lambda | OUT-OF-PATTERN | LAMBDA | live |  |
| anthropic-sdk-deps | {system}-anthropic-sdk-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| bd-gold-common | {system}-49f-gold-common-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| deck-generation-deps | {system}-deck-generation-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| find-insure-browser-deps | {system}-find-insure-browser-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| find-insure-deps | {system}-find-insure-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| find-insure-parse-deps | {system}-find-insure-parse-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| irpt-common | irpt-common-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| mdpf-gold-calendar-deps | mdpf-gold-calendar-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| opal-amgt-print-deps | amgt-print-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| opal-trading-calendar-layer | opal-trading-calendar-layer | CONFORMANT | LAMBDA_LAYER | live |  |
| openpyxl-layer | {system}-openpyxl-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| pandas-pyarrow-layer | {system}-pandas-pyarrow-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| pandas-pyarrow-requests-layer | {system}-pandas-pyarrow-requests-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| pyiceberg-nessie-deps | {system}-pyiceberg-nessie-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| security-scanner-deps | {system}-security-scanner-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| yfinance-dependencies | {system}-yfinance-dependencies-layer | OUT-OF-PATTERN | LAMBDA_LAYER | live |  |
| opal-gateway | gateway-lb | OUT-OF-PATTERN | LOAD_BALANCER | live |  |
| /aws/codebuild/estate-report-seam-freshness-publisher | /aws/codebuild/estate-report-seam-freshness-publisher-build | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/codebuild/globgrph-derive-build | /aws/codebuild/globgrph-derive-build | CONFORMANT | LOG_GROUP | live |  |
| /aws/codebuild/opal-c3materialize-b4-sbm | /aws/codebuild/opal-c3materialize-b4-sbm-build | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/codebuild/opal-drift-producer | /aws/codebuild/opal-drift-producer-build | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/codebuild/opal-stitch-produce | /aws/codebuild/opal-stitch-produce-build | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/codebuild/semantic-clustering-lambda-build | /aws/codebuild/{system}-semantic-clustering-lambda-build | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/ecs/opal-globgrph-projection-worker | /aws/ecs/globgrph-projection-worker-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/events/inf-gold-dispatch-release-audit | /aws/events/{system}-inf-gold-dispatch-release-audit-{cadence} | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/access-anomaly-scanner | /aws/lambda/{system}-access-anomaly-scanner-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/advi-49f-gold-dispatch | /aws/lambda/advi-49f-gold-dispatch-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/amgt-resapp-chatter-axis | /aws/lambda/amgt-resapp-chatter-axis-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/auth-validator-edge | /aws/lambda/{system}-auth-validator-edge-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-49f-etf-ownership-daily | /aws/lambda/blackdiamond-49f-etf-ownership-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-49f-fees-runner | /aws/lambda/blackdiamond-49f-fees-runner-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-49f-keepalive | /aws/lambda/blackdiamond-49f-keepalive-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-49f-runner | /aws/lambda/blackdiamond-49f-runner-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-49f-session-trigger | /aws/lambda/blackdiamond-49f-session-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-allocation-file-checker | /aws/lambda/{system}-49f-allocation-file-checker-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-allocation-processor | /aws/lambda/{system}-49f-allocation-processor-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-allocation-trigger | /aws/lambda/{system}-49f-allocation-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-asset-dim-trigger | /aws/lambda/{system}-49f-asset-dim-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-bronze-trigger | /aws/lambda/{system}-49f-bronze-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-cot-keepalive | /aws/lambda/blackdiamond-cot-keepalive-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-daily-trigger | /aws/lambda/{system}-49f-daily-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-fargate-trigger | /aws/lambda/{system}-49f-fargate-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-fees-trigger | /aws/lambda/{system}-49f-fees-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-gold-trigger | /aws/lambda/{system}-49f-gold-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-incrparity-trigger | /aws/lambda/{system}-49f-incrparity-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-merge-daily | /aws/lambda/{system}-49f-merge-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-pipeline-trigger | /aws/lambda/{system}-49f-pipeline-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-price-update | /aws/lambda/{system}-49f-price-update-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-realized-trigger | /aws/lambda/{system}-49f-realized-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-silver-consolidator | /aws/lambda/{system}-49f-silver-consolidator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-silver-merge | /aws/lambda/advi-49f-silver-merge-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-transaction-trigger | /aws/lambda/{system}-49f-transaction-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-transactions-trigger | /aws/lambda/{system}-49f-transactions-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/bd-unrealized-trigger | /aws/lambda/{system}-49f-unrealized-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/cost-anomaly-scanner | /aws/lambda/{system}-cost-anomaly-scanner-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/cot-bd-session-trigger | /aws/lambda/blackdiamond-cot-session-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/cot-etf-ownership-daily | /aws/lambda/etfs-cot-etf-ownership-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/cot-rebalancer-runner | /aws/lambda/mdpf-cot-rebalancer-runner-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/cot-satellites-characteristics-producer | /aws/lambda/etfs-cot-satellites-characteristics-producer-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/cot-satellites-registry-producer | /aws/lambda/etfs-cot-satellites-registry-producer-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/daily-agenda-generator | /aws/lambda/{system}-daily-agenda-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/daily-sprint-generator | /aws/lambda/{system}-daily-sprint-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/deck-generation | /aws/lambda/{system}-deck-generation-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/ec2-auto-shutdown-enforcer | /aws/lambda/{system}-ec2-auto-shutdown-enforcer-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/ec2-runtime-monitor | /aws/lambda/{system}-ec2-runtime-monitor-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/estate-report-orchestrator | /aws/lambda/estate-report-orchestrator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/etf-ownership-dashboard | /aws/lambda/etfs-etf-ownership-dashboard-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/etf-positioning-producer | /aws/lambda/etfs-etf-positioning-producer-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/etfs-canon-fanin | /aws/lambda/etfs-canon-fanin-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/etfs-netassets-daily | /aws/lambda/etfs-netassets-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/etfs-reports-orchestrator | /aws/lambda/etfs-reports-orchestrator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/exec-summary-generator | /aws/lambda/{system}-exec-summary-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/finbert-batch-processor | /aws/lambda/{system}-finbert-batch-processor-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/find-insure-crawl-web | /aws/lambda/{system}-find-insure-crawl-web-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/find-insure-crawl-web-scraping-browser | /aws/lambda/{system}-find-insure-crawl-web-scraping-browser-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/find-insure-parse-web | /aws/lambda/{system}-find-insure-parse-web-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/find-insure-score-web | /aws/lambda/{system}-find-insure-score-web-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/fred-data-ingestion | /aws/lambda/fred-data-ingestion-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/fred-macro-ingestion | /aws/lambda/fred-macro-ingestion-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/gldinc-ss4c-canary | /aws/lambda/{system}-gldinc-ss4c-canary-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/historical-prices-scheduler | /aws/lambda/{system}-historical-prices-scheduler-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/historical-prices-yfinance | /aws/lambda/{system}-historical-prices-yfinance-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-accounts-v2-daily | /aws/lambda/advi-inf-accounts-v2-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-api-assets-v2 | /aws/lambda/advi-inf-api-assets-v2-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-api-eclipse | /aws/lambda/eclipse-inf-api-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-api-positions | /aws/lambda/advi-inf-api-positions-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-api-reps | /aws/lambda/advi-inf-api-reps-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-api-txn | /aws/lambda/advi-inf-api-txn-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-assets-trigger | /aws/lambda/advi-inf-assets-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-billing-daily | /aws/lambda/advi-inf-billing-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-bronze-complete-emitter | /aws/lambda/advi-inf-bronze-complete-emitter-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-bronze-trigger | /aws/lambda/advi-inf-bronze-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-client-detail | /aws/lambda/advi-inf-client-detail-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-ec2-launch-monitor | /aws/lambda/advi-inf-ec2-launch-monitor-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-ec2-retry-launch | /aws/lambda/advi-inf-ec2-retry-launch-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-etf-ownership-daily | /aws/lambda/etfs-inf-etf-ownership-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-gold-trigger | /aws/lambda/advi-inf-gold-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-jwt-trigger | /aws/lambda/advi-inf-jwt-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-nna-partition-checker | /aws/lambda/advi-inf-nna-partition-checker-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-otp-relay | /aws/lambda/advi-inf-otp-relay-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-performance-daily | /aws/lambda/advi-inf-performance-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-portal-advisor-publisher | /aws/lambda/advi-inf-portal-advisor-publisher-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-portal-publisher | /aws/lambda/{system}-inf-portal-publisher-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-silver-aggregator | /aws/lambda/advi-inf-silver-aggregator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-silver-chain | /aws/lambda/advi-inf-silver-chain-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-tax-daily | /aws/lambda/advi-inf-tax-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/inf-unified-account-dim-daily | /aws/lambda/advi-inf-unified-account-dim-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/infrastructure-daily-snapshot | /aws/lambda/{system}-infrastructure-daily-snapshot-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-directory-refresh | /aws/lambda/irpt-directory-refresh-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-directory-search | /aws/lambda/irpt-directory-search-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-export-render | /aws/lambda/irpt-export-render-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-holdings | /aws/lambda/irpt-holdings-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-intake-poller | /aws/lambda/irpt-intake-poller-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-narrative | /aws/lambda/irpt-narrative-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-performance-adapter | /aws/lambda/irpt-performance-adapter-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-status | /aws/lambda/irpt-status-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-ycharts-generate | /aws/lambda/irpt-ycharts-generate-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/irpt-ycharts-research-20260911 | /aws/lambda/irpt-ycharts-research-20260911-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/keyword-intelligence-generator | /aws/lambda/{system}-keyword-intelligence-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/mdpf-accrual-trigger | /aws/lambda/mdpf-accrual-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/mdpf-feeder-trigger | /aws/lambda/mdpf-feeder-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/mdpf-gold-lambda | /aws/lambda/mdpf-gold-lambda | CONFORMANT | LOG_GROUP | live |  |
| /aws/lambda/opal-49f-served-guard | /aws/lambda/opal-49f-served-guard-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-amgt-scoped-api | /aws/lambda/amgt-scoped-api-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-absence-check | /aws/lambda/opal-assets-absence-check-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-bd49f-daily-pull | /aws/lambda/opal-assets-bd49f-daily-pull-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-bd49f-dim-convert | /aws/lambda/opal-assets-bd49f-dim-convert-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-bd49f-reporting-pull | /aws/lambda/opal-assets-bd49f-reporting-pull-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-daily-emitter | /aws/lambda/opal-assets-daily-emitter-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-ingest-mirror | /aws/lambda/opal-assets-ingest-mirror-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-mdpf-portal-publisher | /aws/lambda/opal-assets-mdpf-portal-publisher-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-silver-bd49finsurance | /aws/lambda/opal-assets-silver-bd49finsurance-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-silver-blackdiamond | /aws/lambda/opal-assets-silver-blackdiamond-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-silver-eclipse | /aws/lambda/opal-assets-silver-eclipse-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-silver-etf | /aws/lambda/opal-assets-silver-etf-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-silver-orion | /aws/lambda/opal-assets-silver-orion-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-silver-schwab | /aws/lambda/opal-assets-silver-schwab-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-assets-silver-smartx | /aws/lambda/opal-assets-silver-smartx-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-bd-transaction-consolidator | /aws/lambda/opal-49f-transaction-consolidator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-cot-served-guard | /aws/lambda/opal-cot-served-guard-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-cot-value-parity | /aws/lambda/opal-cot-value-parity-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-data-refresh-api | /aws/lambda/opal-data-refresh-api-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-data-refresh-api-qa-scratch | /aws/lambda/opal-data-refresh-api-qa-scratch-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-generate-benchmark-returns | /aws/lambda/opal-generate-benchmark-returns-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-globgrph-freeze-monitor | /aws/lambda/globgrph-freeze-monitor-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-globgrph-freshness-alarm | /aws/lambda/globgrph-freshness-alarm-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-globgrph-incremental-updater | /aws/lambda/globgrph-incremental-updater-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-globgrph-tool-activity-freshness | /aws/lambda/globgrph-tool-activity-freshness-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-inf-served-guard | /aws/lambda/opal-inf-served-guard-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-inf-value-parity | /aws/lambda/opal-inf-value-parity-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-infrastructure-monitor | /aws/lambda/opal-infrastructure-monitor-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-ipset-reconciler | /aws/lambda/opal-ipset-reconciler-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-keyword-drilldown-generator | /aws/lambda/opal-keyword-drilldown-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-market-overview-tiered-generator | /aws/lambda/opal-market-overview-tiered-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-market-regime-classifier | /aws/lambda/opal-market-regime-classifier-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-market-rsi-tiered-generator | /aws/lambda/opal-market-rsi-tiered-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-ms-ingest-liveness | /aws/lambda/opal-ms-ingest-liveness-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-otp-liveness | /aws/lambda/opal-otp-liveness-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-partners-data | /aws/lambda/opal-partners-data-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-pm-optimization-autosave-put | /aws/lambda/opal-pm-optimization-autosave-put-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-pm-optimization-loader | /aws/lambda/opal-pm-optimization-loader-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-pm-snapshot-handler | /aws/lambda/opal-pm-snapshot-handler-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-pm-upload-urls | /aws/lambda/opal-pm-upload-urls-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portal-authorizer | /aws/lambda/opal-portal-authorizer-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portal-content-api | /aws/lambda/opal-portal-content-api-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portal-data-proxy | /aws/lambda/opal-portal-data-proxy-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portal-fear-greed-fetcher | /aws/lambda/opal-portal-fear-greed-fetcher-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portal-rest-authorizer | /aws/lambda/opal-portal-rest-authorizer-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portal-volatility-fetcher | /aws/lambda/opal-portal-volatility-fetcher-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portfolio-autosave-get | /aws/lambda/opal-portfolio-autosave-get-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portfolio-autosave-put | /aws/lambda/opal-portfolio-autosave-put-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portfolio-excel-generator | /aws/lambda/opal-portfolio-excel-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portfolio-export-download | /aws/lambda/opal-portfolio-export-download-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portfolio-funds-list | /aws/lambda/opal-portfolio-funds-list-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portfolio-pickle-parser | /aws/lambda/opal-portfolio-pickle-parser-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portfolio-version-get | /aws/lambda/opal-portfolio-version-get-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-portfolio-versions-list | /aws/lambda/opal-portfolio-versions-list-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-research-pull-enqueue | /aws/lambda/opal-research-pull-enqueue-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-security-scanner-processor | /aws/lambda/opal-security-scanner-processor-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-sentinel | /aws/lambda/opal-sentinel-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-session-analytics | /aws/lambda/opal-session-analytics-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-smartx-ingestion-pipeline | /aws/lambda/smartx-ingestion-pipeline-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-ticket-api | /aws/lambda/opal-ticket-api-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-trending-image-generator | /aws/lambda/opal-trending-image-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-trending-topics-portal-publisher | /aws/lambda/opal-trending-topics-portal-publisher-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opal-valuation-tiered-generator | /aws/lambda/opal-valuation-tiered-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/opalinvest-auth-handler | /aws/lambda/{system}-opalinvest-auth-handler-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/partner-etl-ops-sqs-consumer | /aws/lambda/{system}-partner-etl-ops-sqs-consumer-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/public-data-router | /aws/lambda/{system}-public-data-router-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-analysis-coordinator | /aws/lambda/seeking-alpha-analysis-coordinator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-analysis-dedup | /aws/lambda/seeking-alpha-analysis-dedup-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-analysis-listing-parser | /aws/lambda/seeking-alpha-analysis-listing-parser-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-analysis-scraper | /aws/lambda/seeking-alpha-analysis-scraper-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-article-scraper | /aws/lambda/seeking-alpha-article-scraper-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-listing-parser | /aws/lambda/seeking-alpha-listing-parser-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-news-coordinator | /aws/lambda/seeking-alpha-news-coordinator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-news-dedup | /aws/lambda/seeking-alpha-news-dedup-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-news-scraper | /aws/lambda/seeking-alpha-news-scraper-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/seeking-alpha-url-coordinator | /aws/lambda/seeking-alpha-url-coordinator-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/semantic-trending-topics-portal-publisher | /aws/lambda/{system}-semantic-trending-topics-portal-publisher-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/shared-advisor-router | /aws/lambda/{system}-shared-advisor-router-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/shared-advisor-router-response | /aws/lambda/{system}-shared-advisor-router-response-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/smartx-assets-daily-pull | /aws/lambda/smartx-assets-daily-pull-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/smartx-jwt-refresher | /aws/lambda/smartx-jwt-refresher-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/smartx-rest-pull | /aws/lambda/smartx-rest-pull-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/test-seeking-alpha-unauth-simple | /aws/lambda/seeking-alpha-test-unauth-simple-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/test-yfinance-simple | /aws/lambda/{system}-test-yfinance-simple-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/us-east-1.auth-validator-edge | /aws/lambda/us-east-1.{system}-auth-validator-edge-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/us-east-1.public-data-router | /aws/lambda/us-east-1.{system}-public-data-router-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/us-east-1.shared-advisor-router | /aws/lambda/us-east-1.{system}-shared-advisor-router-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/us-east-1.shared-advisor-router-response | /aws/lambda/us-east-1.{system}-shared-advisor-router-response-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/us-east-1.tier-router-edge | /aws/lambda/us-east-1.{system}-tier-router-edge-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/wsb-49f-model-aua-daily | /aws/lambda/mdpf-49f-wsb-model-aua-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/wsd-49f-partner-held-etf-daily | /aws/lambda/mdpf-49f-wsd-partner-held-etf-daily-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-canon-interlock | /aws/lambda/yang-canon-interlock-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-capture-output-versions | /aws/lambda/yang-capture-output-versions-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-cleanup-uploads | /aws/lambda/yang-cleanup-uploads-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-allocation-summary | /aws/lambda/yang-generate-allocation-summary-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-allocation-summary-attribution-tab | /aws/lambda/yang-generate-allocation-summary-attribution-tab-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-cma | /aws/lambda/yang-generate-cma-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-correlation | /aws/lambda/yang-generate-correlation-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-etf-returns | /aws/lambda/yang-generate-etf-returns-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-factor-tilts | /aws/lambda/yang-generate-factor-tilts-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-holdings-attribution | /aws/lambda/yang-generate-holdings-attribution-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-latest | /aws/lambda/yang-generate-latest-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-macro | /aws/lambda/yang-generate-macro-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-macro-timeseries | /aws/lambda/yang-generate-macro-timeseries-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-manifest | /aws/lambda/yang-generate-manifest-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-peer-performance | /aws/lambda/yang-generate-peer-performance-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-positioning | /aws/lambda/yang-generate-positioning-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-risk-premium | /aws/lambda/yang-generate-risk-premium-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-valuation | /aws/lambda/yang-generate-valuation-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-generate-volatility | /aws/lambda/yang-generate-volatility-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-get-prior-metadata | /aws/lambda/yang-get-prior-metadata-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-ingest-dynamodb | /aws/lambda/yang-ingest-dynamodb-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-invalidate-cloudfront | /aws/lambda/yang-invalidate-cloudfront-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-model-portfolio-benchmarks | /aws/lambda/yang-model-portfolio-benchmarks-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-move-to-processed | /aws/lambda/yang-move-to-processed-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-pipeline-trigger | /aws/lambda/yang-pipeline-trigger-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-refresh-fred-cache | /aws/lambda/yang-refresh-fred-cache-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-time-machine | /aws/lambda/yang-time-machine-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-validate-files | /aws/lambda/yang-validate-files-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yang-varflag-check | /aws/lambda/yang-varflag-check-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/ycharts-market-data-pull | /aws/lambda/ycharts-market-data-pull-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/ycharts-session-capture | /aws/lambda/ycharts-session-capture-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/ycharts-session-probe | /aws/lambda/ycharts-session-probe-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/lambda/yfinance-aapl-test | /aws/lambda/{system}-yfinance-aapl-test-lambda | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/stepfunctions/YangDataPipeline | /aws/stepfunctions/yang-data-pipeline-sfn | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /aws/vendedlogs/states/bd-gold-pipeline | /aws/vendedlogs/states/{system}-49f-gold-pipeline-sfn | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/bd-pipeline | /aws/ecs/{system}-49f-pipeline-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/globgrph-cse-producer | /aws/ecs/globgrph-cse-producer-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/globgrph-fedobs-emitter | /aws/ecs/globgrph-fedobs-emitter-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/globgrph-resource-summaries-producer | /aws/ecs/globgrph-resource-summaries-producer-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/globgrph-serving | /aws/ecs/globgrph-serving-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/globgrph/comp-learns-producer | /aws/ecs/globgrph-comp-learns-producer-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/globgrph/derive-runner | /aws/ecs/globgrph-derive-runner-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/globgrph/nessie | /aws/ecs/globgrph-nessie-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| /ecs/globgrph/trino | /aws/ecs/globgrph-trino-task | OUT-OF-PATTERN | LOG_GROUP | live |  |
| opal-313476888478-globgrph | opal-313476888478-globgrph | CONFORMANT | S3_BUCKET | live |  |
| opal-313476888478-lambda-artifacts | opal-313476888478-lambda-artifacts | CONFORMANT | S3_BUCKET | live |  |
| opal-313476888478-lambda-layers | opal-313476888478-lambda-layers | CONFORMANT | S3_BUCKET | live |  |
| opal-313476888478-terraform-state | opal-313476888478-terraform-state | CONFORMANT | S3_BUCKET | live |  |
| opal-313476888478-yang-qa-scratch | opal-313476888478-yang-qa-scratch | CONFORMANT | S3_BUCKET | live |  |
| opal-cloudtrail-logs-313476888478 | opal-313476888478-cloudtrail-logs | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-cur-313476888478 | opal-313476888478-cur | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-data-49financial | opal-data-49financial | CONFORMANT | S3_BUCKET | live |  |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | live |  |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | live |  |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET | live |  |
| opal-data-cottonwood | opal-data-cottonwood | CONFORMANT | S3_BUCKET | live |  |
| opal-data-demo | opal-data-demo | CONFORMANT | S3_BUCKET | live |  |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | live |  |
| opal-data-harvest | opal-data-harvest | CONFORMANT | S3_BUCKET | live |  |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | live |  |
| opal-data-inflection | opal-data-inflection | CONFORMANT | S3_BUCKET | live |  |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | live |  |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | live |  |
| opal-data-ycharts | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-estate-report | opal-313476888478-estate-report | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-infrastructure-snapshots | opal-313476888478-infrastructure-snapshots | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-mcp-athena-results | opal-313476888478-mcp-athena-results | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-mcp-audit | opal-313476888478-mcp-audit | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-runner-shared | opal-313476888478-runner-shared | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-security-evidence | opal-313476888478-security-evidence | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-served-key-write-trail-logs | opal-313476888478-served-key-write-trail-logs | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-website-backups | opal-313476888478-website-backups | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opalinvest-portal | opal-313476888478-opalinvest-portal | OUT-OF-PATTERN | S3_BUCKET | live |  |
| opal-313476888478-lambda-artifacts | opal-313476888478-lambda-artifacts | CONFORMANT | S3_BUCKET_POLICY | live |  |
| opal-cloudtrail-logs-313476888478 | opal-313476888478-cloudtrail-logs | OUT-OF-PATTERN | S3_BUCKET_POLICY | live |  |
| opal-cur-313476888478 | opal-313476888478-cur | OUT-OF-PATTERN | S3_BUCKET_POLICY | live |  |
| opal-data-49financial | opal-data-49financial | CONFORMANT | S3_BUCKET_POLICY | live |  |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET_POLICY | live |  |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET_POLICY | live |  |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET_POLICY | live |  |
| opal-data-demo | opal-data-demo | CONFORMANT | S3_BUCKET_POLICY | live |  |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET_POLICY | live |  |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET_POLICY | live |  |
| opal-security-evidence | opal-313476888478-security-evidence | OUT-OF-PATTERN | S3_BUCKET_POLICY | live |  |
| opal-served-key-write-trail-logs | opal-313476888478-served-key-write-trail-logs | OUT-OF-PATTERN | S3_BUCKET_POLICY | live |  |
| opalinvest-portal | opal-313476888478-opalinvest-portal | OUT-OF-PATTERN | S3_BUCKET_POLICY | live |  |
| advi-49f-gold-floor | advi-49f-gold-floor-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| advi-49f-publisher | advi-49f-publisher-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| amgt-resapp-chatter-axis-daily | amgt-resapp-chatter-axis-daily | CONFORMANT | SCHEDULE | live |  |
| cot-bd-session-daily-et | blackdiamond-cot-session-et-daily | OUT-OF-PATTERN | SCHEDULE | live |  |
| estate-report-0900et | estate-report-0900et-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| estate-report-seam-freshness-0830et | estate-report-seam-freshness-0830et-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| etfs-reports-monthly-run | etfs-reports-run-monthly | OUT-OF-PATTERN | SCHEDULE | live |  |
| globgrph-cse-producer-nightly | globgrph-cse-producer-nightly-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| irpt-directory-refresh | irpt-directory-refresh-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| irpt-holdings-snapshot | irpt-holdings-snapshot-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| irpt-intake-poll | irpt-intake-poll-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| mdpf-accrual-bridge-daily | mdpf-accrual-bridge-daily | CONFORMANT | SCHEDULE | live |  |
| mdpf-feeder-backstop-daily | mdpf-feeder-backstop-daily | CONFORMANT | SCHEDULE | live |  |
| mdpf-scheduled-floor | mdpf-scheduled-floor-{cadence} | OUT-OF-PATTERN | SCHEDULE | live |  |
| opal-assets-bd49f-dim-convert-daily | opal-assets-bd49f-dim-convert-daily | CONFORMANT | SCHEDULE | live |  |
| opal-assets-ingest-mirror-cot-daily-et | opal-cot-assets-ingest-mirror-et-daily | OUT-OF-PATTERN | SCHEDULE | live |  |
| opal-assets-mdpf-portal-publisher-daily | opal-assets-mdpf-portal-publisher-daily | CONFORMANT | SCHEDULE | live |  |
| smartx-assets-daily-pull-daily | smartx-assets-daily-pull-daily | CONFORMANT | SCHEDULE | live |  |
| smartx-jwt-refresher-daily | smartx-jwt-refresher-daily | CONFORMANT | SCHEDULE | live |  |
| smartx-rest-pull-daily | smartx-rest-pull-daily | CONFORMANT | SCHEDULE | live |  |
| wsb-49f-model-aua-pull-daily | {system}-49f-wsb-model-aua-pull-daily | OUT-OF-PATTERN | SCHEDULE | live |  |
| wsd-49f-partner-held-etf-pull-daily | {system}-49f-wsd-partner-held-etf-pull-daily | OUT-OF-PATTERN | SCHEDULE | live |  |
| FredApiKey | fred/api-key | OUT-OF-PATTERN | SECRET | live |  |
| aaii/credentials | {system}/aaii/credentials | OUT-OF-PATTERN | SECRET | live |  |
| ai/claude-api-key | {system}/ai/claude-api-key | OUT-OF-PATTERN | SECRET | live |  |
| anthropic-api-key | {system}/anthropic-api-key | OUT-OF-PATTERN | SECRET | live |  |
| blackdiamond/49f/credentials | blackdiamond/49f/credentials | CONFORMANT | SECRET | live |  |
| blackdiamond/49f/otp-gateway-token | blackdiamond/49f/otp-gateway-token | CONFORMANT | SECRET | live |  |
| blackdiamond/49f/otp-relay | blackdiamond/49f/otp-relay | CONFORMANT | SECRET | live |  |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | live |  |
| blackdiamond/cot/credentials | blackdiamond/cot/credentials | CONFORMANT | SECRET | live |  |
| blackdiamond/cot/otp-gateway-token | blackdiamond/cot/otp-gateway-token | CONFORMANT | SECRET | live |  |
| blackdiamond/cot/otp-relay | blackdiamond/cot/otp-relay | CONFORMANT | SECRET | live |  |
| blackdiamond/cot/session | blackdiamond/cot/session | CONFORMANT | SECRET | live |  |
| bloomberg/session | bloomberg/session | CONFORMANT | SECRET | live |  |
| bloomberg/terminal/login | bloomberg/terminal/login | CONFORMANT | SECRET | live |  |
| brightdata-api-key | {system}/brightdata-api-key | OUT-OF-PATTERN | SECRET | live |  |
| conferenceboard/credentials | {system}/conferenceboard/credentials | OUT-OF-PATTERN | SECRET | live |  |
| estate-report/github-token | estate/report/github-token | OUT-OF-PATTERN | SECRET | live |  |
| find-dualbiz/bright-data/serp | {system}/find-dualbiz/bright-data/serp | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/bright-data/api-key | {system}/find-insure/bright-data/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/bright-data/scraping-browser-creds | {system}/find-insure/bright-data/scraping-browser-creds | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/builtin/api-key | {system}/find-insure/job-board/builtin/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/efinancialcareers/api-key | {system}/find-insure/job-board/efinancialcareers/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/glassdoor/api-key | {system}/find-insure/job-board/glassdoor/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/indeed/api-key | {system}/find-insure/job-board/indeed/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/insurancejobs/api-key | {system}/find-insure/job-board/insurancejobs/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/linkedin-jobs/api-key | {system}/find-insure/job-board/linkedin-jobs/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/placeholder | {system}/find-insure/job-board/placeholder | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/wellfound/api-key | {system}/find-insure/job-board/wellfound/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/job-board/ziprecruiter/api-key | {system}/find-insure/job-board/ziprecruiter/api-key | OUT-OF-PATTERN | SECRET | live |  |
| find-insure/lusha-ai/api-key | {system}/find-insure/lusha-ai/api-key | OUT-OF-PATTERN | SECRET | live |  |
| github-token | {system}/github-token | OUT-OF-PATTERN | SECRET | live |  |
| google-cse-config | {system}/google-cse-config | OUT-OF-PATTERN | SECRET | live |  |
| google/andrew-goldengate/credentials | {system}/google/andrew-goldengate/credentials | OUT-OF-PATTERN | SECRET | live |  |
| google/officialmadeaux/credentials | {system}/google/officialmadeaux/credentials | OUT-OF-PATTERN | SECRET | live |  |
| inf/otp-relay/token | {system}/inf/otp-relay/token | OUT-OF-PATTERN | SECRET | live |  |
| massive-api-key | {system}/massive-api-key | OUT-OF-PATTERN | SECRET | live |  |
| msci-api-credentials | msci/api-credentials | OUT-OF-PATTERN | SECRET | live |  |
| multi-threadv2 | {system}/multi-threadv2 | OUT-OF-PATTERN | SECRET | live |  |
| nopecha/api-key | {system}/nopecha/api-key | OUT-OF-PATTERN | SECRET | live |  |
| opal/auth/jwt-private-key | opal/auth/jwt-private-key | CONFORMANT | SECRET | live |  |
| opal/auth/jwt-public-key | opal/auth/jwt-public-key | CONFORMANT | SECRET | live |  |
| opal/auth/origin-verify | opal/auth/origin-verify | CONFORMANT | SECRET | live |  |
| opal/bd/cottonwood/credentials | blackdiamond/cot/credentials | OUT-OF-PATTERN | SECRET | live |  |
| opal/bd/credentials | opal/49f/credentials | ALIAS | SECRET | live |  |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | live |  |
| opal/finbert/config | opal/finbert/config | CONFORMANT | SECRET | live |  |
| opal/mcp/graph-read-token | opal/mcp/graph-read-token | CONFORMANT | SECRET | live |  |
| opal/mcp/ms-ingest-token | opal/mcp/ms-ingest-token | CONFORMANT | SECRET | live |  |
| opal/mcp/opal-gateway-fernet | opal/mcp/opal-gateway-fernet | CONFORMANT | SECRET | live |  |
| opal/mcp/opal-gateway-graph | opal/mcp/opal-gateway-graph | CONFORMANT | SECRET | live |  |
| opal/mcp/opal-gateway-jwt | opal/mcp/opal-gateway-jwt | CONFORMANT | SECRET | live |  |
| opal/mcp/opal-gateway-login | opal/mcp/opal-gateway-login | CONFORMANT | SECRET | live |  |
| opal/mcp/opal-gateway-schwab-account-ref-key | opal/mcp/opal-gateway-schwab-account-ref-key | CONFORMANT | SECRET | live |  |
| opal/mcp/opal-gateway-schwab-reader-external-ids | opal/mcp/opal-gateway-schwab-reader-external-ids | CONFORMANT | SECRET | live |  |
| opal/mcp/opalbloomberg-login | opal/mcp/opalbloomberg-login | CONFORMANT | SECRET | live |  |
| opal/openai/andrew-fideles | opal/openai/andrew-fideles | CONFORMANT | SECRET | live |  |
| opal/openai/aws-lambda-ki | opal/openai/aws-lambda-ki | CONFORMANT | SECRET | live |  |
| opal/openai/layer3-curation | opal/openai/layer3-curation | CONFORMANT | SECRET | live |  |
| opal/openai/market-update | opal/openai/market-update | CONFORMANT | SECRET | live |  |
| opal/openai/news-trending | opal/openai/news-trending | CONFORMANT | SECRET | live |  |
| opal/portal/config | opal/portal/config | CONFORMANT | SECRET | live |  |
| opal/portal/svc-data-refresh | opal/portal/svc-data-refresh | CONFORMANT | SECRET | live |  |
| opal/pseudonym/49financial | opal/49f/pseudonym | OUT-OF-PATTERN | SECRET | live |  |
| opal/pseudonym/opal-capital | opal/pseudonym/opal-capital | CONFORMANT | SECRET | live |  |
| opal/smartx/config | smartx/config | OUT-OF-PATTERN | SECRET | live |  |
| opal/smartx/qa-models | smartx/qa-models | OUT-OF-PATTERN | SECRET | live |  |
| opal/ticketing/svc-analyst-intake | opal/ticketing/svc-analyst-intake | CONFORMANT | SECRET | live |  |
| opalinvest/admin-seed | {system}/opalinvest/admin-seed | OUT-OF-PATTERN | SECRET | live |  |
| opalinvest/jwt-secret | {system}/opalinvest/jwt-secret | OUT-OF-PATTERN | SECRET | live |  |
| openai-api-key | {system}/openai-api-key | OUT-OF-PATTERN | SECRET | live |  |
| orion/credentials | orion/credentials | CONFORMANT | SECRET | live |  |
| orion/eclipse_jwt/current | orion/eclipse-jwt/current | OUT-OF-PATTERN | SECRET | live |  |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | live |  |
| price_discovery | {system}/price-discovery | OUT-OF-PATTERN | SECRET | live |  |
| quo/api-key | {system}/quo/api-key | OUT-OF-PATTERN | SECRET | live |  |
| schwab/anonymization-key | schwab/anonymization-key | CONFORMANT | SECRET | live |  |
| schwab/ec2-credentials | schwab/ec2-credentials | CONFORMANT | SECRET | live |  |
| schwab/sdd-credentials | schwab/sdd-credentials | CONFORMANT | SECRET | live |  |
| schwab/sdd/session | schwab/sdd/session | CONFORMANT | SECRET | live |  |
| seeking-alpha/bright-data-api-key | seeking-alpha/bright-data-api-key | CONFORMANT | SECRET | live |  |
| seeking-alpha/credentials | seeking-alpha/credentials | CONFORMANT | SECRET | live |  |
| seeking-alpha/session | seeking-alpha/session | CONFORMANT | SECRET | live |  |
| smartx/cookie/current | smartx/cookie/current | CONFORMANT | SECRET | live |  |
| smartx/credentials/password | smartx/credentials/password | CONFORMANT | SECRET | live |  |
| smartx/credentials/username | smartx/credentials/username | CONFORMANT | SECRET | live |  |
| smartx/credentials/yaliu-bundle | smartx/credentials/yaliu-bundle | CONFORMANT | SECRET | live |  |
| smartx/credentials/yang-shared | smartx/credentials/yang-shared | CONFORMANT | SECRET | live |  |
| smartx/jwt/current | smartx/jwt/current | CONFORMANT | SECRET | live |  |
| twilio/credentials | {system}/twilio/credentials | OUT-OF-PATTERN | SECRET | live |  |
| twilio/recovery-code | {system}/twilio/recovery-code | OUT-OF-PATTERN | SECRET | live |  |
| ycharts/credentials | ycharts/credentials | CONFORMANT | SECRET | live |  |
| ycharts/login/credentials | ycharts/login/credentials | CONFORMANT | SECRET | live |  |
| ycharts/session/current | ycharts/session/current | CONFORMANT | SECRET | live |  |
| ycharts/session/research-20260911 | ycharts/session/research-20260911 | CONFORMANT | SECRET | live |  |
| bd-49f-auto-login-sg | blackdiamond-49f-auto-login-sg | ALIAS | SECURITY_GROUP | live |  |
| bd-exporter-sg | {system}-49f-exporter-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| cot-exporter-sg | {system}-cot-exporter-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| estate-report-runner-sg | estate-report-runner-sg | CONFORMANT | SECURITY_GROUP | live |  |
| etfs-reports-reporter-sg | etfs-reports-reporter-sg | CONFORMANT | SECURITY_GROUP | live |  |
| inf-bronze-runner-sg | {system}-inf-bronze-runner-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| inf-exporter-sg | {system}-inf-exporter-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| inf-gold-qa-runner-sg | {system}-inf-gold-qa-runner-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| inf-gold-runner-sg | {system}-inf-gold-runner-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| irpt-ycharts-runner-sg | irpt-ycharts-runner-sg | CONFORMANT | SECURITY_GROUP | live |  |
| mdpf-daily-runner-sg | mdpf-daily-runner-sg | CONFORMANT | SECURITY_GROUP | live |  |
| opal-gateway-alb-sg | gateway-alb-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| opal-gateway-sg | gateway-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| opal-globgrph-derive-runner-sg | globgrph-derive-runner-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| opal-globgrph-incremental-updater-sg | globgrph-incremental-updater-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| opal-globgrph-nessie-sg | globgrph-nessie-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| opal-globgrph-projection-worker-sg | globgrph-projection-worker-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| opal-globgrph-serving-sg | globgrph-serving-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| opal-globgrph-trino-sg | globgrph-trino-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| opal-vpc-endpoints-sg | opal-vpc-endpoints-sg | CONFORMANT | SECURITY_GROUP | live |  |
| opal-website-wp-sg | opal-website-wp-sg | CONFORMANT | SECURITY_GROUP | live |  |
| quartz-si2-spike-sg | {system}-quartz-si2-spike-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| seeking-alpha-scraper-proxy | seeking-alpha-scraper-proxy-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| smartx-exporter-20251218220948304800000002 | smartx-exporter-sg | OUT-OF-PATTERN | SECURITY_GROUP | live |  |
| bd-allocation-file-missing | {system}-49f-allocation-file-missing-topic | OUT-OF-PATTERN | SNS_TOPIC | live |  |
| ec2-auto-shutdown-alerts | {system}-ec2-auto-shutdown-alerts | OUT-OF-PATTERN | SNS_TOPIC | live |  |
| ec2-long-running-alerts | {system}-ec2-long-running-alerts | OUT-OF-PATTERN | SNS_TOPIC | live |  |
| etfs-reports-alerts | etfs-reports-alerts | CONFORMANT | SNS_TOPIC | live |  |
| find-insure-budget-alerts | {system}-find-insure-budget-alerts | OUT-OF-PATTERN | SNS_TOPIC | live |  |
| inf-gold-dispatch-release-alarm | {system}-inf-gold-dispatch-release-alarm-topic | OUT-OF-PATTERN | SNS_TOPIC | live |  |
| inf-otp-alert | {system}-inf-otp-alert-topic | OUT-OF-PATTERN | SNS_TOPIC | live |  |
| opal-bd-49f-cookie-alerts | blackdiamond-49f-cookie-alerts | OUT-OF-PATTERN | SNS_TOPIC | live |  |
| opal-bd-cot-cookie-alerts | blackdiamond-cot-cookie-alerts | OUT-OF-PATTERN | SNS_TOPIC | live |  |
| opal-critical-surface-alerts | opal-critical-surface-alerts | CONFORMANT | SNS_TOPIC | live |  |
| opal-infrastructure-alerts | opal-infrastructure-alerts | CONFORMANT | SNS_TOPIC | live |  |
| opal-login-abuse-alerts | opal-login-abuse-alerts | CONFORMANT | SNS_TOPIC | live |  |
| opal-partner-etl-ops-alerts | opal-partner-etl-ops-alerts | CONFORMANT | SNS_TOPIC | live |  |
| advi-49f-floor-dlq | advi-49f-floor-dlq | CONFORMANT | SQS_QUEUE | live |  |
| agentbus-ajbdev-laptop-to-sitez.fifo | agentbus-ajbdev-laptop-to-sitez-queue.fifo | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| agentbus-ajbdev-sitez-to-laptop.fifo | agentbus-ajbdev-sitez-to-laptop-queue.fifo | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| agentbus-alyssa01-alyssa-to-andrew.fifo | agentbus-alyssa01-alyssa-to-andrew-queue.fifo | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| agentbus-alyssa01-andrew-to-alyssa.fifo | agentbus-alyssa01-andrew-to-alyssa-queue.fifo | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| agentbus-sim01-alpha-to-beta.fifo | agentbus-sim01-alpha-to-beta-queue.fifo | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| agentbus-sim01-beta-to-alpha.fifo | agentbus-sim01-beta-to-alpha-queue.fifo | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| inf-gold-trigger-dlq | {system}-inf-gold-trigger-dlq | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| irpt-export | irpt-export-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| irpt-export-dlq | irpt-export-dlq | CONFORMANT | SQS_QUEUE | live |  |
| irpt-generation | irpt-generation-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| irpt-generation-dlq | irpt-generation-dlq | CONFORMANT | SQS_QUEUE | live |  |
| irpt-intake | irpt-intake-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| irpt-intake-dlq | irpt-intake-dlq | CONFORMANT | SQS_QUEUE | live |  |
| mdpf-daily-trigger-dlq | mdpf-daily-trigger-dlq | CONFORMANT | SQS_QUEUE | live |  |
| opal-49f-served-guard-recheck | opal-49f-served-guard-recheck-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| opal-assets-silver-dlq | opal-assets-silver-dlq | CONFORMANT | SQS_QUEUE | live |  |
| opal-cot-served-guard-recheck | opal-cot-served-guard-recheck-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| opal-critical-surface-alerts-coo | opal-critical-surface-alerts-coo-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| opal-globgrph-incremental-events | globgrph-incremental-events-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| opal-globgrph-incremental-events-dlq | globgrph-incremental-events-dlq | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| opal-globgrph-projection-events | globgrph-projection-events-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| opal-globgrph-projection-events-dlq | globgrph-projection-events-dlq | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| opal-inf-served-guard-recheck | opal-inf-served-guard-recheck-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| opal-research-pull-requests | opal-research-pull-requests-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| partner-etl-ops-queue | {system}-partner-etl-ops-queue | OUT-OF-PATTERN | SQS_QUEUE | live |  |
| advi-49f-chain-dispatch | advi-49f-chain-dispatch-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| gateway-readonly-host-document | gateway-readonly-host-document | CONFORMANT | SSM_DOCUMENT | live |  |
| irpt-export-render-run | irpt-export-render-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| irpt-ycharts-deploy | irpt-ycharts-deploy-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| irpt-ycharts-run | irpt-ycharts-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-bd-49f-session-fetch | blackdiamond-49f-session-fetch-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-bd-allocation-download | opal-49f-allocation-download-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-bd-asset-dim-download | opal-49f-asset-dim-download-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-bd-fees-download | opal-49f-fees-download-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-bd-realized-download | opal-49f-realized-download-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-bd-transaction-download | opal-49f-transaction-download-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-bd-unrealized-download | opal-49f-unrealized-download-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-cot-bd-session-fetch | opal-cot-blackdiamond-session-fetch-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-cot-bronze-run | opal-cot-bronze-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-cot-gold-run | opal-cot-gold-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-cot-silver-run | opal-cot-silver-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-inf-export-run | opal-inf-export-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-inf-jwt-fetch | opal-inf-jwt-fetch-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-inf-jwt-setup | opal-inf-jwt-setup-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-inf-test-login-stage1 | opal-inf-test-login-stage1-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-inf-test-login-stage2 | opal-inf-test-login-stage2-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-inf-test-login-stage3 | opal-inf-test-login-stage3-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-schwab-archive-01raw | schwab-archive-01raw-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| opal-schwab-rps-convert | schwab-rps-convert-document | OUT-OF-PATTERN | SSM_DOCUMENT | live |  |
| YangDataPipeline | yang-data-pipeline-sfn | OUT-OF-PATTERN | STATE_MACHINE | live |  |
| opal-49f-value-parity | opal-49f-value-parity-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/49f-value-parity/49f_value_parity.tf:46 |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/49f-value-parity/49f_value_parity.tf:51 |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/49f-value-parity/49f_value_parity.tf:85 |
| opal-49f-value-parity | opal-49f-value-parity-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/49f-value-parity/49f_value_parity.tf:98 |
| opal-49f-value-parity-hourly | opal-49f-value-parity-hourly | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/49f-value-parity/49f_value_parity.tf:135 |
| brightdata-api-key | {system}/brightdata-api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/astn-pipeline/secrets-shared.tf:15 |
| bd-49f-auto-login-role | blackdiamond-49f-auto-login-role | ALIAS | IAM_ROLE | repo | infra/aws/terraform/bd-49f-auto-login/iam.tf:17 |
| bd-49f-auto-login | blackdiamond-49f-auto-login-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-49f-auto-login/iam.tf:32 |
| bd-49f-auto-login-profile | blackdiamond-49f-auto-login-profile | ALIAS | INSTANCE_PROFILE | repo | infra/aws/terraform/bd-49f-auto-login/iam.tf:103 |
| bd-49f-auto-login-sg | blackdiamond-49f-auto-login-sg | ALIAS | SECURITY_GROUP | repo | infra/aws/terraform/bd-49f-auto-login/instance.tf:29 |
| bd-49f-auto-login | blackdiamond-49f-auto-login-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/bd-49f-auto-login/instance.tf:51 |
| ExecIncrParityFailure | {system}-exec-incrparity-failure-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/bd-pipeline/alarms.tf:15 |
| bd-gold-runner-overrun | {system}-49f-gold-runner-overrun-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/bd-pipeline/alarms.tf:55 |
| bd-gold-qa-runner-forgotten | {system}-49f-gold-qa-runner-forgotten-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/bd-pipeline/alarms.tf:77 |
| bd-49f-etf-ownership-daily-role | blackdiamond-49f-etf-ownership-daily-role | ALIAS | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/bd-49f-etf-ownership-daily.tf:41 |
| s3-etf-ownership | {system}-s3-etf-ownership-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/bd-49f-etf-ownership-daily.tf:63 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/bd-49f-etf-ownership-daily.tf:136 |
| bd-49f-etf-ownership-scheduled-floor | blackdiamond-49f-etf-ownership-scheduled-floor-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/bd-49f-etf-ownership-daily.tf:198 |
| opal-bd-49f-cookie-alerts | blackdiamond-49f-cookie-alerts | OUT-OF-PATTERN | SNS_TOPIC | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:49 |
| bd-49f-keepalive-role | blackdiamond-49f-keepalive-role | ALIAS | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:66 |
| bd-49f-keepalive-policy | blackdiamond-49f-keepalive-policy | ALIAS | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:84 |
| bd-49f-keepalive-sched | blackdiamond-49f-keepalive-sched-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:148 |
| bd-49f-runner-role | blackdiamond-49f-runner-role | ALIAS | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:194 |
| bd-49f-runner-policy | blackdiamond-49f-runner-policy | ALIAS | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:212 |
| bd-49f-runner-daily | blackdiamond-49f-runner-daily | ALIAS | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:338 |
| bd-49f-fees-runner-role | blackdiamond-49f-fees-runner-role | ALIAS | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:378 |
| bd-49f-fees-runner-policy | blackdiamond-49f-fees-runner-policy | ALIAS | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:396 |
| bd-49f-fees-runner-daily | blackdiamond-49f-fees-runner-daily | ALIAS | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/bd-49f-interim.tf:479 |
| opal-bd-49f-session-fetch | blackdiamond-49f-session-fetch-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf:67 |
| bd-49f-session-trigger-role | blackdiamond-49f-session-trigger-role | ALIAS | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf:93 |
| bd-49f-session-trigger-policy | blackdiamond-49f-session-trigger-policy | ALIAS | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf:109 |
| bd-49f-session-daily | blackdiamond-49f-session-daily | ALIAS | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf:219 |
| bd-49f-session-complete | blackdiamond-49f-session-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf:243 |
| bd-49f-fees-session-daily | blackdiamond-49f-fees-session-daily | ALIAS | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf:278 |
| bd-49f-insurance-session-daily | blackdiamond-49f-insurance-session-daily | ALIAS | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/bd-49f-session-chain.tf:317 |
| bd-exporter-sg | {system}-49f-exporter-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/bd-pipeline/bd-exporter-sg.tf:12 |
| bd-silver-merge-role | advi-49f-silver-merge-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/bd-silver-merge.tf:14 |
| bd-silver-merge-policy | {system}-49f-silver-merge-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/bd-silver-merge.tf:32 |
| bd-allocations | {system}-49f-allocations-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/bd-pipeline/ec2.tf:10 |
| bd-transactions | {system}-49f-transactions-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/bd-pipeline/ec2.tf:46 |
| bd-fees | {system}-49f-fees-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/bd-pipeline/ec2.tf:86 |
| bd-assets | {system}-49f-assets-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/bd-pipeline/ec2.tf:128 |
| bd-gold-detail-generator | {system}-49f-gold-detail-generator-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/bd-pipeline/ec2.tf:167 |
| bd-gold-layer-runner | {system}-49f-gold-layer-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/bd-pipeline/ec2.tf:207 |
| bd-gold-qa-runner | {system}-49f-gold-qa-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/bd-pipeline/ec2.tf:268 |
| bd-allocation-pipeline-trigger | {system}-49f-allocation-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:40 |
| bd-unrealized-pipeline-trigger | {system}-49f-unrealized-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:71 |
| bd-realized-pipeline-trigger | {system}-49f-realized-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:103 |
| bd-fees-pipeline-trigger | {system}-49f-fees-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:136 |
| bd-asset-dim-pipeline-trigger | {system}-49f-asset-dim-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:169 |
| bd-transaction-pipeline-trigger | {system}-49f-transaction-pipeline-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:199 |
| bd-gold-layer-monthly-trigger | {system}-49f-gold-layer-trigger-monthly | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:228 |
| bd-allocation-file-check-daily | {system}-49f-allocation-file-check-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:259 |
| bd-gold-nightly-fallback | {system}-49f-gold-nightly-fallback-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:292 |
| historical-prices-daily | {system}-historical-prices-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:322 |
| bd-canonical-prices-daily | {system}-49f-canonical-prices-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:364 |
| incrparity-weekly | {system}-incrparity-weekly | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/eventbridge.tf:399 |
| gldinc-ss4c-canary-role | {system}-gldinc-ss4c-canary-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/gldinc-ss4c.tf:27 |
| gldinc-ss4c-canary-policy | {system}-gldinc-ss4c-canary-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/gldinc-ss4c.tf:50 |
| gldinc-ss4c-canary-daily | {system}-gldinc-ss4c-canary-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/bd-pipeline/gldinc-ss4c.tf:106 |
| gldinc-ss4c-canary-break | {system}-gldinc-ss4c-canary-break-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/bd-pipeline/gldinc-ss4c.tf:139 |
| gldinc-ss4c-weekly-divergence | {system}-gldinc-ss4c-weekly-divergence-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/bd-pipeline/gldinc-ss4c.tf:161 |
| bd-daily-trigger-lambda-role | {system}-49f-daily-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:26 |
| bd-daily-trigger-policy | {system}-49f-daily-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:44 |
| bd-s3-access | {system}-49f-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:131 |
| bd-allocation-checker-lambda-role | {system}-49f-allocation-checker-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:157 |
| bd-allocation-checker-permissions | {system}-49f-allocation-checker-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:175 |
| bd-processor-lambda-role | {system}-49f-processor-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:215 |
| bd-s3-readwrite | {system}-49f-s3-readwrite-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:233 |
| pipeline-chain | {system}-pipeline-chain-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:256 |
| bd-gold-layer-lambda-role | {system}-49f-gold-layer-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:280 |
| bd-s3-scoped | {system}-49f-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:298 |
| bd-exporter-ec2-role | {system}-49f-exporter-ec2-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:340 |
| bd-exporter-profile | {system}-49f-exporter-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/bd-pipeline/iam.tf:358 |
| s3-access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:363 |
| monolith-schwab-08242234-silver-read | schwab-08242234-monolith-silver-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:399 |
| monolith-schwab-08335338-silver-read | schwab-08335338-monolith-silver-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:434 |
| monolith-bd49f-xref-silver-read | {system}-monolith-bd49f-xref-silver-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:470 |
| runner-shared-read | {system}-runner-shared-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:496 |
| AdditionalPermissions | {system}-additional-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:523 |
| gold-layer-trigger | {system}-gold-layer-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:578 |
| pipeline-chain | {system}-pipeline-chain-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:596 |
| describe-tags-self | {system}-describe-tags-self-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:618 |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:640 |
| events-emit | {system}-events-emit-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:665 |
| cloudfront-invalidate | {system}-cloudfront-invalidate-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:695 |
| bd-gold-detail-generator-role | {system}-49f-gold-detail-generator-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:715 |
| bd-gold-detail-generator-profile | {system}-49f-gold-detail-generator-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/bd-pipeline/iam.tf:733 |
| bd-gold-detail-s3-access | {system}-49f-gold-detail-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:738 |
| bd-gold-detail-cloudwatch-logs | {system}-49f-gold-detail-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:755 |
| bd-allocation-processor-role | {system}-49f-allocation-processor-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:774 |
| s3-access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:792 |
| invoke-price-update | {system}-invoke-price-update-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:809 |
| bd-gold-step-functions-role | {system}-49f-gold-step-functions-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:833 |
| bd-gold-step-functions-lambda-policy | {system}-49f-gold-step-functions-lambda-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:851 |
| bd-gold-eventbridge-step-functions-role | {system}-49f-gold-eventbridge-step-functions-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:893 |
| bd-gold-eventbridge-start-execution-policy | {system}-49f-gold-eventbridge-start-execution-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:911 |
| historical-prices-lambda-role | {system}-historical-prices-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bd-pipeline/iam.tf:946 |
| historical-prices-policy | {system}-historical-prices-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:969 |
| advi-49f-chain-access | advi-49f-chain-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:1042 |
| advi-49f-publisher-platinum-put | advi-49f-publisher-platinum-put-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bd-pipeline/iam.tf:1196 |
| bd-allocation-file-checker | {system}-49f-allocation-file-checker-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/bd-pipeline/lambdas.tf:167 |
| /aws/lambda/bd-allocation-file-checker | /aws/lambda/{system}-49f-allocation-file-checker-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/bd-pipeline/lambdas.tf:186 |
| openpyxl-layer | {system}-openpyxl-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/bd-pipeline/layers.tf:8 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/terraform/bd-pipeline/opal-data-bd.tf:8 |
| opal/bd/credentials | opal/49f/credentials | ALIAS | SECRET | repo | infra/aws/terraform/bd-pipeline/secrets-opal-bd.tf:18 |
| price_discovery | {system}/price-discovery | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/bd-pipeline/secrets-opal-bd.tf:29 |
| opal-bloomberg-tunnel-instance-role | bloomberg-tunnel-instance-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/bloomberg-tunnel/main.tf:124 |
| opal-bloomberg-tunnel-caller | bloomberg-tunnel-caller-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/bloomberg-tunnel/main.tf:178 |
| quartz-si2-spike-role | {system}-quartz-si2-spike-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/canonical-schwab-ec2/iam.tf:8 |
| quartz-si2-spike-inline | {system}-quartz-si2-spike-inline-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/canonical-schwab-ec2/iam.tf:28 |
| quartz-si2-spike-profile | {system}-quartz-si2-spike-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/canonical-schwab-ec2/iam.tf:128 |
| canonical-schwab-si2-daily-events-ssm-role | schwab-canonical-si2-daily-events-ssm-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/canonical-schwab-ec2/monolith-daily-schedule.tf:154 |
| send-daily-pull-command | {system}-send-daily-pull-command-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/canonical-schwab-ec2/monolith-daily-schedule.tf:162 |
| quartz-si2-monolith-write | {system}-quartz-si2-monolith-write-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/canonical-schwab-ec2/monolith-iam.tf:36 |
| opal-schwab-monolith-remap-role | schwab-monolith-remap-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/canonical-schwab-ec2/monolith-iam.tf:122 |
| opal-schwab-monolith-remap-inline | schwab-monolith-remap-inline-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/canonical-schwab-ec2/monolith-iam.tf:137 |
| schwab/anonymization-key | schwab/anonymization-key | CONFORMANT | SECRET | repo | infra/aws/terraform/canonical-schwab-ec2/secrets.tf:16 |
| schwab/ec2-credentials | schwab/ec2-credentials | CONFORMANT | SECRET | repo | infra/aws/terraform/canonical-schwab-ec2/secrets.tf:28 |
| schwab/sdd-credentials | schwab/sdd-credentials | CONFORMANT | SECRET | repo | infra/aws/terraform/canonical-schwab-ec2/secrets.tf:43 |
| schwab/sdd/session | schwab/sdd/session | CONFORMANT | SECRET | repo | infra/aws/terraform/canonical-schwab-ec2/secrets.tf:60 |
| consolidation-gold-runner-role | {system}-consolidation-gold-runner-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/consolidation-gold-runner/runner-iam.tf:25 |
| consolidation-gold-runner-inline | {system}-consolidation-gold-runner-inline-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/consolidation-gold-runner/runner-iam.tf:46 |
| consolidation-gold-runner-profile | {system}-consolidation-gold-runner-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/consolidation-gold-runner/runner-iam.tf:137 |
| consolidation-gold-runner-scheduled-start | {system}-consolidation-gold-runner-scheduled-start-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/consolidation-gold-runner/runner-trigger.tf:9 |
| consolidation-gold-runner-automation-start-role | {system}-consolidation-gold-runner-automation-start-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/consolidation-gold-runner/runner-trigger.tf:34 |
| start-consolidation-gold-runner | {system}-start-consolidation-gold-runner-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/consolidation-gold-runner/runner-trigger.tf:42 |
| consolidation-gold-runner-events-invoke-ssm-role | {system}-consolidation-gold-runner-events-invoke-ssm-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/consolidation-gold-runner/runner-trigger.tf:59 |
| invoke-start-automation | {system}-invoke-start-automation-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/consolidation-gold-runner/runner-trigger.tf:67 |
| consolidation-gold-runner | {system}-consolidation-gold-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/consolidation-gold-runner/runner.tf:13 |
| opal-bd-cot-cookie-alerts | blackdiamond-cot-cookie-alerts | OUT-OF-PATTERN | SNS_TOPIC | repo | infra/aws/terraform/cot-pipeline/cot-detection-layer.tf:39 |
| bd-cot-keepalive-role | blackdiamond-cot-keepalive-role | ALIAS | IAM_ROLE | repo | infra/aws/terraform/cot-pipeline/cot-detection-layer.tf:70 |
| bd-cot-keepalive-policy | blackdiamond-cot-keepalive-policy | ALIAS | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/cot-detection-layer.tf:88 |
| bd-cot-keepalive-sched | blackdiamond-cot-keepalive-sched-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/cot-pipeline/cot-detection-layer.tf:151 |
| cot-etf-ownership-daily-role | etfs-cot-etf-ownership-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/cot-pipeline/cot-etf-ownership-daily.tf:48 |
| s3-etf-ownership | {system}-s3-etf-ownership-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/cot-etf-ownership-daily.tf:70 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/cot-etf-ownership-daily.tf:161 |
| cot-etf-ownership-daily-schedule | {system}-cot-etf-ownership-schedule-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/cot-pipeline/cot-etf-ownership-daily.tf:222 |
| cot-exporter-sg | {system}-cot-exporter-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/cot-pipeline/ec2.tf:14 |
| cot-exporter | advi-cot-exporter-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/cot-pipeline/ec2.tf:44 |
| cot-session-complete | {system}-cot-session-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/cot-pipeline/eventbridge.tf:121 |
| cot-bronze-complete | {system}-cot-bronze-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/cot-pipeline/eventbridge.tf:172 |
| cot-silver-complete | {system}-cot-silver-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/cot-pipeline/eventbridge.tf:219 |
| cot-bd-session-trigger-lambda-role | blackdiamond-cot-session-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/cot-pipeline/iam.tf:17 |
| cot-bd-session-trigger-policy | blackdiamond-cot-session-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/iam.tf:35 |
| cot-gold-layer-ec2-role | advi-cot-gold-layer-ec2-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/cot-pipeline/iam.tf:122 |
| cot-gold-layer-profile | {system}-cot-gold-layer-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/cot-pipeline/iam.tf:140 |
| s3-scoped-cot | {system}-cot-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/iam.tf:145 |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/iam.tf:192 |
| cot-exporter-ec2-role | advi-cot-exporter-ec2-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/cot-pipeline/iam.tf:218 |
| cot-exporter-profile | {system}-cot-exporter-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/cot-pipeline/iam.tf:236 |
| cot-exporter-policy | {system}-cot-exporter-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/iam.tf:241 |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/iam.tf:370 |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET | repo | infra/aws/terraform/cot-pipeline/s3.tf:10 |
| cot-satellites-characteristics-producer-role | etfs-cot-satellites-characteristics-producer-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/cot-pipeline/satellites-characteristics-producer.tf:43 |
| s3-read-three-inputs-write-satellites-characteristics | {system}-s3-read-three-inputs-write-satellites-characteristics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/satellites-characteristics-producer.tf:106 |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/satellites-characteristics-producer.tf:223 |
| cot-satellites-characteristics-producer-daily | {system}-cot-satellites-characteristics-producer-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/cot-pipeline/satellites-characteristics-producer.tf:355 |
| cot-satellites-registry-producer-role | etfs-cot-satellites-registry-producer-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/cot-pipeline/satellites-registry-producer.tf:44 |
| s3-read-cot-bronze-write-cot-platinum | {system}-cot-s3-read-bronze-write-platinum-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/satellites-registry-producer.tf:90 |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/satellites-registry-producer.tf:170 |
| cot-satellites-registry-producer-daily | {system}-cot-satellites-registry-producer-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/cot-pipeline/satellites-registry-producer.tf:284 |
| cot-session-scheduler-role | {system}-cot-session-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/cot-pipeline/schedule-et.tf:46 |
| invoke-the-session-trigger | {system}-invoke-the-session-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-pipeline/schedule-et.tf:64 |
| cot-bd-session-daily-et | blackdiamond-cot-session-et-daily | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/cot-pipeline/schedule-et.tf:78 |
| blackdiamond/cot/credentials | blackdiamond/cot/credentials | CONFORMANT | SECRET | repo | infra/aws/terraform/cot-pipeline/secrets.tf:13 |
| blackdiamond/cot/session | blackdiamond/cot/session | CONFORMANT | SECRET | repo | infra/aws/terraform/cot-pipeline/secrets.tf:26 |
| blackdiamond/cot/otp-relay | blackdiamond/cot/otp-relay | CONFORMANT | SECRET | repo | infra/aws/terraform/cot-pipeline/secrets.tf:73 |
| blackdiamond/cot/otp-gateway-token | blackdiamond/cot/otp-gateway-token | CONFORMANT | SECRET | repo | infra/aws/terraform/cot-pipeline/secrets.tf:92 |
| opal-cot-bd-session-fetch | opal-cot-blackdiamond-session-fetch-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/cot-pipeline/ssm.tf:23 |
| opal-cot-bronze-run | opal-cot-bronze-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/cot-pipeline/ssm.tf:83 |
| opal-cot-silver-run | opal-cot-silver-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/cot-pipeline/ssm.tf:195 |
| opal-cot-gold-run | opal-cot-gold-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/cot-pipeline/ssm.tf:294 |
| opal-cot-value-parity | opal-cot-value-parity-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/cot-value-parity/cot_value_parity.tf:47 |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-value-parity/cot_value_parity.tf:52 |
| CotServedAndSourceRead | {system}-cot-served-and-source-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-value-parity/cot_value_parity.tf:66 |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/cot-value-parity/cot_value_parity.tf:83 |
| opal-cot-value-parity | opal-cot-value-parity-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/cot-value-parity/cot_value_parity.tf:96 |
| opal-cot-value-parity-hourly | opal-cot-value-parity-hourly | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/cot-value-parity/cot_value_parity.tf:126 |
| daily-sprint-generator-role | {system}-daily-sprint-generator-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/daily-sprint-generator/main.tf:110 |
| daily-sprint-generator-policy | {system}-daily-sprint-generator-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/daily-sprint-generator/main.tf:130 |
| daily-sprint-generator | {system}-daily-sprint-generator-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/daily-sprint-generator/main.tf:173 |
| daily-sprint-generator-schedule | {system}-sprint-generator-schedule-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/daily-sprint-generator/main.tf:212 |
| data-refresh-sscn-s3-access | {system}-data-refresh-sscn-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/data-refresh/main.tf:58 |
| data-refresh-cloudfront-read | {system}-data-refresh-cloudfront-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/data-refresh/main.tf:80 |
| data-refresh-time-machine-invoke | {system}-data-refresh-time-machine-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/data-refresh/main.tf:99 |
| data-refresh-qa-scratch-access-20260803 | {system}-data-refresh-qa-scratch-access-20260803-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/data-refresh/qa-scratch-instance.tf:36 |
| deck-generation-lambda-role | {system}-deck-generation-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/deck-generation-pipeline/iam.tf:8 |
| deck-generation-lambda-policy | {system}-deck-generation-lambda-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/deck-generation-pipeline/iam.tf:21 |
| deck-generation-deps | {system}-deck-generation-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/deck-generation-pipeline/lambdas.tf:16 |
| deck-generation | {system}-deck-generation-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/deck-generation-pipeline/lambdas.tf:37 |
| /aws/lambda/deck-generation | /aws/lambda/{system}-deck-generation-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/deck-generation-pipeline/lambdas.tf:74 |
| estate-report-scheduler-role | estate-report-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/estate-report/iam.tf:35 |
| estate-report-scheduler-invoke | estate-report-scheduler-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/estate-report/iam.tf:44 |
| estate-report-orchestrator-role | estate-report-orchestrator-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/estate-report/iam.tf:60 |
| estate-report-orchestrator | estate-report-orchestrator-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/estate-report/iam.tf:69 |
| estate-report-runner-role | estate-report-runner-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/estate-report/iam.tf:111 |
| estate-report-runner-profile | estate-report-runner-profile | CONFORMANT | INSTANCE_PROFILE | repo | infra/aws/terraform/estate-report/iam.tf:120 |
| estate-report-runner | estate-report-runner-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/estate-report/iam.tf:131 |
| estate-report-runner-selfstop | estate-report-runner-selfstop-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/estate-report/iam.tf:334 |
| estate-capture-writer | estate-capture-writer-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/estate-report/iam.tf:443 |
| estate-capture-writer-text-input | estate-capture-writer-text-input-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/estate-report/iam.tf:540 |
| outset-drift-publisher-laptop | {system}-outset-drift-publisher-laptop-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/estate-report/iam.tf:585 |
| outset-drift-publisher-laptop | {system}-outset-drift-publisher-laptop-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/estate-report/iam.tf:613 |
| estate-report-runner-sg | estate-report-runner-sg | CONFORMANT | SECURITY_GROUP | repo | infra/aws/terraform/estate-report/instance.tf:42 |
| estate-report-runner | estate-report-runner | CONFORMANT | EC2_INSTANCE | repo | infra/aws/terraform/estate-report/instance.tf:55 |
| estate-report-orchestrator | estate-report-orchestrator-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/estate-report/orchestrator.tf:15 |
| estate-report-0900et | estate-report-0900et-{cadence} | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/estate-report/orchestrator.tf:56 |
| estate-report-seam-freshness-publisher | estate-report-seam-freshness-publisher-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/estate-report/seam-freshness-publisher.tf:79 |
| estate-report-seam-freshness-publisher | estate-report-seam-freshness-publisher-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/estate-report/seam-freshness-publisher.tf:92 |
| estate-report-seam-freshness-publisher | estate-report-seam-freshness-publisher-build | OUT-OF-PATTERN | CODEBUILD_PROJECT | repo | infra/aws/terraform/estate-report/seam-freshness-publisher.tf:147 |
| estate-report-seam-freshness-0830et | estate-report-seam-freshness-0830et-{cadence} | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/estate-report/seam-freshness-publisher.tf:214 |
| estate-report-seam-freshness-scheduler | estate-report-seam-freshness-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/estate-report/seam-freshness-publisher.tf:227 |
| estate-report-seam-freshness-scheduler | estate-report-seam-freshness-scheduler-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/estate-report/seam-freshness-publisher.tf:240 |
| estate-report/github-token | estate/report/github-token | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/estate-report/secrets.tf:11 |
| opal-etfs-ownership-daily | etfs-ownership-daily-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/etfs-canon/dynamo.tf:19 |
| etfs-canon-fanin-role | etfs-canon-fanin-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/etfs-canon/fanin-lambda.tf:17 |
| s3-read-etfs-daily | etfs-s3-read-daily-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/etfs-canon/fanin-lambda.tf:37 |
| ddb-write-ownership-daily | {system}-ddb-write-ownership-daily-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/etfs-canon/fanin-lambda.tf:63 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/etfs-canon/fanin-lambda.tf:85 |
| etfs-canon-fanin-daily | etfs-canon-fanin-daily | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/etfs-canon/fanin-lambda.tf:129 |
| etfs-netassets-daily-role | etfs-netassets-daily-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/etfs-netassets/netassets-lambda.tf:5 |
| s3-rw-etfs-bronze-silver | etfs-s3-rw-bronze-silver-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/etfs-netassets/netassets-lambda.tf:31 |
| etfs-netassets-daily | etfs-netassets-daily | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/etfs-netassets/netassets-lambda.tf:208 |
| etfs-netassets-daily-errors | etfs-netassets-daily-errors-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/etfs-netassets/netassets-lambda.tf:248 |
| etf-positioning-producer-role | etfs-etf-positioning-producer-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/etfs-positioning/producer-lambda.tf:5 |
| s3-rw-etfs-gold-platinum | etfs-s3-rw-gold-platinum-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/etfs-positioning/producer-lambda.tf:40 |
| opal-trading-calendar-layer | opal-trading-calendar-layer | CONFORMANT | LAMBDA_LAYER | repo | infra/aws/terraform/etfs-positioning/producer-lambda.tf:186 |
| etf-positioning-producer-daily | {system}-etf-positioning-producer-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/etfs-positioning/producer-lambda.tf:278 |
| etfs-reports-reporter-role | etfs-reports-reporter-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/etfs-reports/iam.tf:9 |
| etfs-reports-reporter | etfs-reports-reporter-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/etfs-reports/iam.tf:24 |
| etfs-reports-reporter-profile | etfs-reports-reporter-profile | CONFORMANT | INSTANCE_PROFILE | repo | infra/aws/terraform/etfs-reports/iam.tf:89 |
| etfs-reports-reporter-sg | etfs-reports-reporter-sg | CONFORMANT | SECURITY_GROUP | repo | infra/aws/terraform/etfs-reports/instance.tf:24 |
| etfs-reports-reporter | etfs-reports-reporter-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/etfs-reports/instance.tf:37 |
| etfs-reports-alerts | etfs-reports-alerts | CONFORMANT | SNS_TOPIC | repo | infra/aws/terraform/etfs-reports/orchestrator.tf:14 |
| etfs-reports-orchestrator-role | etfs-reports-orchestrator-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/etfs-reports/orchestrator.tf:26 |
| etfs-reports-orchestrator | etfs-reports-orchestrator-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/etfs-reports/orchestrator.tf:35 |
| etfs-reports-orchestrator | etfs-reports-orchestrator-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/etfs-reports/orchestrator.tf:117 |
| etfs-reports-orchestrator-errors | etfs-reports-orchestrator-errors-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/etfs-reports/orchestrator.tf:142 |
| etfs-reports-scheduler-role | etfs-reports-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/etfs-reports/orchestrator.tf:157 |
| etfs-reports-scheduler-invoke | etfs-reports-scheduler-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/etfs-reports/orchestrator.tf:166 |
| etfs-reports-monthly-run | etfs-reports-run-monthly | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/etfs-reports/orchestrator.tf:178 |
| exec-summary-generator-role | {system}-exec-summary-generator-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/exec-summary/iam.tf:11 |
| exec-summary-generator-policy | {system}-exec-summary-generator-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/exec-summary/iam.tf:33 |
| anthropic-sdk-deps | {system}-anthropic-sdk-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/exec-summary/main.tf:82 |
| exec-summary-advisors-processed-ceiling | {system}-exec-summary-advisors-processed-ceiling-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/exec-summary/main.tf:156 |
| exec-summary-tokens-in-anomaly | {system}-exec-summary-tokens-in-anomaly-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/exec-summary/main.tf:176 |
| exec-summary-trigger-placeholder | {system}-exec-summary-trigger-placeholder-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/exec-summary/main.tf:220 |
| fred-ingestion-daily | fred-ingestion-daily | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/fred-pipeline/eventbridge.tf:14 |
| fred-ingestion-weekly | fred-ingestion-weekly | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/fred-pipeline/eventbridge.tf:42 |
| fred-ingestion-monthly-early | fred-ingestion-early-monthly | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/fred-pipeline/eventbridge.tf:70 |
| fred-ingestion-monthly-mid | fred-ingestion-mid-monthly | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/fred-pipeline/eventbridge.tf:98 |
| fred-ingestion-monthly-late | fred-ingestion-late-monthly | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/fred-pipeline/eventbridge.tf:126 |
| fred-macro-ingestion-daily | fred-macro-ingestion-daily | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/fred-pipeline/eventbridge.tf:163 |
| yield-curve-artifact-write | {system}-yield-curve-artifact-write-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/fred-pipeline/iam.tf:23 |
| fred-ingestion-secrets-read | fred-ingestion-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/fred-pipeline/iam.tf:45 |
| FredMacroIngestionLambdaRole | fred-macro-ingestion-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/fred-pipeline/iam.tf:73 |
| fred-macro-secrets-read | fred-macro-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/fred-pipeline/iam.tf:98 |
| fred-macro-artifact-write | fred-macro-artifact-write-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/fred-pipeline/iam.tf:114 |
| fred-data-ingestion | fred-data-ingestion-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/fred-pipeline/lambdas.tf:21 |
| /aws/lambda/fred-data-ingestion | /aws/lambda/fred-data-ingestion-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/fred-pipeline/lambdas.tf:49 |
| fred-macro-ingestion | fred-macro-ingestion-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/fred-pipeline/lambdas.tf:92 |
| /aws/lambda/fred-macro-ingestion | /aws/lambda/fred-macro-ingestion-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/fred-pipeline/lambdas.tf:119 |
| github-actions-runner-role | {system}-github-actions-runner-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/github-actions-runner/runner-iam.tf:40 |
| github-actions-runner-logs | {system}-github-actions-runner-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/github-actions-runner/runner-iam.tf:81 |
| github-actions-runner-profile | {system}-github-actions-runner-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/github-actions-runner/runner-iam.tf:98 |
| github-actions-runner | {system}-github-actions-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/github-actions-runner/runner.tf:22 |
| /ecs/globgrph/comp-learns-producer | /aws/ecs/globgrph-comp-learns-producer-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/comp_learns_producer.tf:28 |
| opal-globgrph-comp-learns-producer-task | globgrph-comp-learns-producer-task-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/comp_learns_producer.tf:34 |
| CompLearnsServedWrite | {system}-comp-learns-served-write-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/comp_learns_producer.tf:39 |
| CompLearnsProducerLogs | {system}-comp-learns-producer-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/comp_learns_producer.tf:56 |
| globgrph-comp-learns-producer | globgrph-comp-learns-producer-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/comp_learns_producer.tf:72 |
| opal-globgrph-comp-learns-producer-events | globgrph-comp-learns-producer-events-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/comp_learns_producer.tf:116 |
| CompLearnsProducerRunTask | {system}-comp-learns-producer-run-task-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/comp_learns_producer.tf:121 |
| opal-globgrph-comp-learns-producer-nightly | globgrph-comp-learns-producer-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/globgrph/comp_learns_producer.tf:147 |
| /ecs/globgrph-cse-producer | /aws/ecs/globgrph-cse-producer-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/cse_producer.tf:45 |
| opal-globgrph-cse-producer-task | globgrph-cse-producer-task-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/cse_producer.tf:51 |
| CseProducerS3 | {system}-cse-producer-s3-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/cse_producer.tf:56 |
| CseProducerCWLogs | {system}-cse-producer-cw-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/cse_producer.tf:105 |
| globgrph-cse-producer | globgrph-cse-producer-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/cse_producer.tf:121 |
| opal-globgrph-cse-producer-scheduler | globgrph-cse-producer-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/cse_producer.tf:179 |
| CseProducerRunTask | {system}-cse-producer-run-task-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/cse_producer.tf:187 |
| globgrph-cse-producer-nightly | globgrph-cse-producer-nightly-{cadence} | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/globgrph/cse_producer.tf:215 |
| globgrph-s3-requests-daily-warning | globgrph-s3-requests-daily-warning-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/globgrph/d4f1_request_alarm.tf:31 |
| globgrph-s3-requests-daily-high | globgrph-s3-requests-daily-high-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/globgrph/d4f1_request_alarm.tf:58 |
| globgrph-derive-build-role | globgrph-derive-build-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/globgrph/derive-build.tf:16 |
| globgrph-derive-build-perms | globgrph-derive-build-perms-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/derive-build.tf:29 |
| globgrph-derive-build | globgrph-derive-build | CONFORMANT | CODEBUILD_PROJECT | repo | infra/aws/terraform/globgrph/derive-build.tf:66 |
| opal-globgrph-fedobs-emitter-task | globgrph-fedobs-emitter-task-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/fedobs.tf:37 |
| FedobsWriteScoped | {system}-fedobs-write-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/fedobs.tf:53 |
| FedobsEmitterLogs | {system}-fedobs-emitter-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/fedobs.tf:94 |
| /ecs/globgrph-fedobs-emitter | /aws/ecs/globgrph-fedobs-emitter-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/fedobs_producer.tf:50 |
| globgrph-fedobs-producer | globgrph-fedobs-producer-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/fedobs_producer.tf:56 |
| opal-globgrph-fedobs-producer-events | globgrph-fedobs-producer-events-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/fedobs_producer.tf:102 |
| FedobsProducerRunTask | {system}-fedobs-producer-run-task-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/fedobs_producer.tf:107 |
| opal-globgrph-fedobs-producer-nightly | globgrph-fedobs-producer-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/globgrph/fedobs_producer.tf:133 |
| opal-globgrph-nessie-task | globgrph-nessie-task-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/iam.tf:30 |
| NessieDynamoAccess | {system}-nessie-dynamo-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/iam.tf:35 |
| NessieS3WarehouseAccess | {system}-nessie-s3-warehouse-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/iam.tf:69 |
| opal-globgrph-nessie-execution | globgrph-nessie-execution-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/iam.tf:99 |
| opal-globgrph-incremental-updater | globgrph-incremental-updater-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/iam.tf:113 |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/iam.tf:118 |
| SQSConsume | {system}-sqs-consume-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/iam.tf:138 |
| S3WarehouseWrite | {system}-s3-warehouse-write-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/iam.tf:159 |
| BoundedDeriveReadOnly | {system}-bounded-derive-read-only-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/iam.tf:185 |
| DeriveRunnerBucketNotificationRead | {system}-derive-runner-bucket-notification-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/iam.tf:260 |
| /ecs/globgrph/derive-runner | /aws/ecs/globgrph-derive-runner-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/item2a.tf:45 |
| opal-globgrph-derive-runner-task | globgrph-derive-runner-task-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/item2a.tf:55 |
| DeriveRunnerS3 | {system}-derive-runner-s3-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/item2a.tf:60 |
| DeriveRunnerAccountDescribe | {system}-derive-runner-account-describe-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/item2a.tf:121 |
| DeriveRunnerCWLogs | {system}-derive-runner-cw-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/item2a.tf:223 |
| opal-globgrph-derive-runner-execution | globgrph-derive-runner-execution-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/item2a.tf:244 |
| DeriveRunnerMsIngestSecret | {system}-derive-runner-ms-ingest-secret-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/item2a.tf:261 |
| opal-globgrph-derive-runner-events | globgrph-derive-runner-events-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/item2a.tf:286 |
| EventsRunECSTask | {system}-events-run-ecs-task-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/item2a.tf:291 |
| opal-globgrph-derive-runner-sg | globgrph-derive-runner-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/globgrph/item2a.tf:323 |
| globgrph-derive-runner | globgrph-derive-runner-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/item2a.tf:346 |
| opal-globgrph-derive-runner-nightly | globgrph-derive-runner-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/globgrph/item2a.tf:438 |
| /aws/lambda/opal-globgrph-incremental-updater | /aws/lambda/globgrph-incremental-updater-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/item2b.tf:8 |
| opal-globgrph-incremental-events | globgrph-incremental-events-queue | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/globgrph/item2b.tf:15 |
| opal-globgrph-incremental-events-dlq | globgrph-incremental-events-dlq | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/globgrph/item2b.tf:28 |
| opal-globgrph-cloudtrail-mgmt | globgrph-cloudtrail-mgmt-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/globgrph/item2b.tf:70 |
| opal-globgrph-incremental-updater-sg | globgrph-incremental-updater-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/globgrph/item2b.tf:93 |
| pyiceberg-nessie-deps | {system}-pyiceberg-nessie-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/globgrph/item2b.tf:124 |
| opal-globgrph-incremental-updater | globgrph-incremental-updater-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/globgrph/item2b.tf:134 |
| opal-critical-surface-alerts | opal-critical-surface-alerts | CONFORMANT | SNS_TOPIC | repo | infra/aws/terraform/globgrph/item2c_surface_alarm.tf:15 |
| DeriveRunnerSNS | {system}-derive-runner-sns-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/item2c_surface_alarm.tf:60 |
| IncrementalUpdaterSNS | {system}-incremental-updater-sns-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/item2c_surface_alarm.tf:82 |
| opal-served-key-write-trail-logs | opal-313476888478-served-key-write-trail-logs | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/globgrph/item2e_served_write_trail.tf:35 |
| /ecs/globgrph/nessie | /aws/ecs/globgrph-nessie-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/nessie.tf:8 |
| opal-globgrph | globgrph-cluster | OUT-OF-PATTERN | ECS_CLUSTER | repo | infra/aws/terraform/globgrph/nessie.tf:14 |
| opal-globgrph-nessie-sg | globgrph-nessie-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/globgrph/nessie.tf:34 |
| globgrph-nessie | globgrph-nessie-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/nessie.tf:87 |
| opal-globgrph-projection-events | globgrph-projection-events-queue | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/globgrph/projection.tf:16 |
| opal-globgrph-projection-events-dlq | globgrph-projection-events-dlq | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/globgrph/projection.tf:34 |
| opal-globgrph-projection-worker | globgrph-projection-worker-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/projection.tf:111 |
| SQSConsume | {system}-sqs-consume-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/projection.tf:120 |
| ProjectionRuntime | {system}-projection-runtime-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/projection.tf:148 |
| /aws/ecs/opal-globgrph-projection-worker | /aws/ecs/globgrph-projection-worker-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/projection.tf:182 |
| opal-globgrph-projection-worker-execution | globgrph-projection-worker-execution-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/projection.tf:187 |
| opal-globgrph-projection-worker-sg | globgrph-projection-worker-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/globgrph/projection.tf:197 |
| globgrph-projection-worker | globgrph-projection-worker-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/projection.tf:212 |
| opal-globgrph-projection-pipe | globgrph-projection-pipe-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/projection.tf:268 |
| ProjectionPipeInvoke | {system}-projection-pipe-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/projection.tf:278 |
| /ecs/globgrph-resource-summaries-producer | /aws/ecs/globgrph-resource-summaries-producer-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/resource_summaries_producer.tf:48 |
| opal-globgrph-resource-summaries-producer-task | globgrph-resource-summaries-producer-task-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/resource_summaries_producer.tf:54 |
| ResourceSummariesProducerS3 | {system}-resource-summaries-producer-s3-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/resource_summaries_producer.tf:59 |
| ResourceSummariesProducerCWLogs | {system}-resource-summaries-producer-cw-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/resource_summaries_producer.tf:126 |
| globgrph-resource-summaries-producer | globgrph-resource-summaries-producer-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/resource_summaries_producer.tf:142 |
| /ecs/globgrph-serving | /aws/ecs/globgrph-serving-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/serving.tf:42 |
| opal-globgrph-serving-task | globgrph-serving-task-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/serving.tf:66 |
| GlobgrphServingReadOnly | globgrph-serving-read-only-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/serving.tf:71 |
| opal-globgrph-serving-sg | globgrph-serving-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/globgrph/serving.tf:77 |
| globgrph-serving | globgrph-serving-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/serving.tf:121 |
| opal-stitch-source-gha-role | opal-stitch-source-gha-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/globgrph/stitch-produce.tf:43 |
| StitchSourceZipPut | {system}-stitch-source-zip-put-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/stitch-produce.tf:61 |
| opal-stitch-produce-codebuild-role | opal-stitch-produce-codebuild-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/globgrph/stitch-produce.tf:79 |
| StitchProducePerms | {system}-stitch-produce-perms-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/stitch-produce.tf:91 |
| opal-stitch-produce | opal-stitch-produce-build | OUT-OF-PATTERN | CODEBUILD_PROJECT | repo | infra/aws/terraform/globgrph/stitch-produce.tf:130 |
| opal-stitch-produce-events-role | opal-stitch-produce-events-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/globgrph/stitch-produce.tf:213 |
| StartStitchProduceBuild | {system}-start-stitch-produce-build-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/stitch-produce.tf:225 |
| opal-stitch-produce-nightly | opal-stitch-produce-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/globgrph/stitch-produce.tf:238 |
| /ecs/globgrph/trino | /aws/ecs/globgrph-trino-task | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/globgrph/trino.tf:22 |
| opal-globgrph-trino-task | globgrph-trino-task-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/trino.tf:33 |
| TrinoWarehouseReadOnly | {system}-trino-warehouse-read-only-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/trino.tf:38 |
| TrinoCodeHeatGlueRead | {system}-trino-code-heat-glue-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/trino.tf:65 |
| TrinoSSMExecChannel | {system}-trino-ssm-exec-channel-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/trino.tf:96 |
| TrinoCWLogs | {system}-trino-cw-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/globgrph/trino.tf:121 |
| opal-globgrph-trino-execution | globgrph-trino-execution-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/globgrph/trino.tf:141 |
| opal-globgrph-trino-sg | globgrph-trino-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/globgrph/trino.tf:156 |
| globgrph-trino | globgrph-trino-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/terraform/globgrph/trino.tf:209 |
| opal-vpc-endpoints-sg | opal-vpc-endpoints-sg | CONFORMANT | SECURITY_GROUP | repo | infra/aws/terraform/globgrph/vpc_endpoints.tf:50 |
| opal-research-pull-enqueue-role | opal-research-pull-enqueue-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/harvest/api-gateway.tf:25 |
| opal-research-pull-enqueue-grants | opal-research-pull-enqueue-grants-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/harvest/api-gateway.tf:42 |
| amgt-resapp-chatter-axis-lambda-role | amgt-resapp-chatter-axis-lambda-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/harvest/chatter-axis-schedule.tf:67 |
| amgt-resapp-chatter-axis-lambda-policy | amgt-resapp-chatter-axis-lambda-policy | CONFORMANT | IAM_POLICY | repo | infra/aws/terraform/harvest/chatter-axis-schedule.tf:79 |
| amgt-resapp-chatter-axis | amgt-resapp-chatter-axis-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/harvest/chatter-axis-schedule.tf:118 |
| amgt-resapp-chatter-axis-scheduler-role | amgt-resapp-chatter-axis-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/harvest/chatter-axis-schedule.tf:146 |
| amgt-resapp-chatter-axis-scheduler-invoke | amgt-resapp-chatter-axis-scheduler-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/harvest/chatter-axis-schedule.tf:158 |
| amgt-resapp-chatter-axis-daily | amgt-resapp-chatter-axis-daily | CONFORMANT | SCHEDULE | repo | infra/aws/terraform/harvest/chatter-axis-schedule.tf:172 |
| opal-harvest-articles | harvest-articles-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/harvest/dynamodb.tf:46 |
| opal-harvest-security-metrics | harvest-security-metrics-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/harvest/dynamodb.tf:111 |
| opal-amgt-print-deps | amgt-print-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/harvest/print-deps-layer.tf:48 |
| opal-data-harvest | opal-data-harvest | CONFORMANT | S3_BUCKET | repo | infra/aws/terraform/harvest/s3.tf:23 |
| opal-amgt-scoped-api-role | amgt-scoped-api-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/harvest/scoped-amgt-api.tf:77 |
| opal-amgt-scoped-api-grants | amgt-scoped-api-grants-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/harvest/scoped-amgt-api.tf:165 |
| opal-research-pull-requests | opal-research-pull-requests-queue | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/harvest/sqs.tf:19 |
| find-insure-cost-state | {system}-find-insure-cost-state-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/imo-pipeline/dynamodb.tf:37 |
| find-insure-dynamodb | {system}-find-insure-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/imo-pipeline/dynamodb.tf:79 |
| find-insure-lambda-role | {system}-find-insure-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/imo-pipeline/iam.tf:17 |
| find-insure-s3 | {system}-find-insure-s3-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/imo-pipeline/iam.tf:38 |
| find-insure-secrets-read | {system}-find-insure-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/imo-pipeline/iam.tf:105 |
| find-insure-logs | {system}-find-insure-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/imo-pipeline/iam.tf:130 |
| find-insure-events | {system}-find-insure-events-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/imo-pipeline/iam.tf:152 |
| find-insure-kms | {system}-find-insure-kms-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/imo-pipeline/kms.tf:139 |
| find-insure-deps | {system}-find-insure-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/imo-pipeline/layers.tf:24 |
| find-insure-parse-deps | {system}-find-insure-parse-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/imo-pipeline/layers.tf:59 |
| find-insure-browser-deps | {system}-find-insure-browser-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/imo-pipeline/layers.tf:110 |
| find-insure/job-board/linkedin-jobs/api-key | {system}/find-insure/job-board/linkedin-jobs/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/phase2b-secrets.tf:28 |
| find-insure/job-board/indeed/api-key | {system}/find-insure/job-board/indeed/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/phase2b-secrets.tf:44 |
| find-insure/job-board/glassdoor/api-key | {system}/find-insure/job-board/glassdoor/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/phase2b-secrets.tf:60 |
| find-insure/job-board/ziprecruiter/api-key | {system}/find-insure/job-board/ziprecruiter/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/phase2b-secrets.tf:76 |
| find-insure/job-board/wellfound/api-key | {system}/find-insure/job-board/wellfound/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/phase2b-secrets.tf:92 |
| find-insure/job-board/builtin/api-key | {system}/find-insure/job-board/builtin/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/phase2b-secrets.tf:108 |
| find-insure/job-board/efinancialcareers/api-key | {system}/find-insure/job-board/efinancialcareers/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/phase2b-secrets.tf:129 |
| find-insure/job-board/insurancejobs/api-key | {system}/find-insure/job-board/insurancejobs/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/phase2b-secrets.tf:145 |
| find-insure/lusha-ai/api-key | {system}/find-insure/lusha-ai/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/secrets.tf:23 |
| find-insure/bright-data/api-key | {system}/find-insure/bright-data/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/secrets.tf:39 |
| find-insure/bright-data/scraping-browser-creds | {system}/find-insure/bright-data/scraping-browser-creds | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/secrets.tf:64 |
| find-insure/job-board/placeholder | {system}/find-insure/job-board/placeholder | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/imo-pipeline/secrets.tf:84 |
| find-insure-budget-alerts | {system}-find-insure-budget-alerts | OUT-OF-PATTERN | SNS_TOPIC | repo | infra/aws/terraform/imo-pipeline/sns.tf:43 |
| find-insure-sns | {system}-find-insure-sns-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/imo-pipeline/sns.tf:96 |
| orion-otp-timeout-alert | orion-otp-timeout-alert-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/alarms.tf:10 |
| Inflection-JwtResilience-NearExpirySpike | advi-inf-jwt-resilience-near-expiry-spike-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/alarms.tf:35 |
| Inflection-HistBackfill-FailureSpike | advi-inf-hist-backfill-failure-spike-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/alarms.tf:60 |
| inf-gold-chain-failed | advi-inf-gold-chain-failed-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/alarms.tf:93 |
| inf-gold-runner-overrun | advi-inf-gold-runner-overrun-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/alarms.tf:146 |
| inf-gold-trigger-dlq-depth | advi-inf-gold-trigger-dlq-depth-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/alarms.tf:181 |
| inf-otp-relay-api | advi-inf-otp-relay-api | OUT-OF-PATTERN | API_GW | repo | infra/aws/terraform/inf-pipeline/api-gateway.tf:24 |
| inf-api-eclipse-role | eclipse-inf-api-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf:32 |
| inf-api-eclipse-scoped | eclipse-inf-api-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf:56 |
| inf-api-eclipse-daily | eclipse-inf-api-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf:119 |
| inf-bronze-complete-emitter-role | advi-inf-bronze-complete-emitter-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf:149 |
| inf-bronze-complete-emitter-scoped | {system}-inf-bronze-complete-emitter-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf:171 |
| inf-bronze-complete-emitter-daily | {system}-inf-bronze-complete-emitter-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/br1-eclipse-rehome.tf:222 |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/cross-firm-deny.tf:72 |
| opal-inf-launch-locks | opal-inf-launch-locks-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/inf-pipeline/dynamo.tf:13 |
| inf-gold-runner-sg | {system}-inf-gold-runner-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/inf-pipeline/ec2.tf:12 |
| inf-gold-layer-runner | {system}-inf-gold-layer-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/inf-pipeline/ec2.tf:31 |
| inf-exporter-sg | {system}-inf-exporter-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/inf-pipeline/ec2.tf:81 |
| inf-exporter | advi-inf-exporter-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/inf-pipeline/ec2.tf:100 |
| opal-inf-jwt-fetch | opal-inf-jwt-fetch-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/eventbridge.tf:31 |
| opal-inf-bronze-runner-cron | opal-inf-bronze-runner-cron-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/eventbridge.tf:66 |
| opal-inf-export-schedule | opal-inf-export-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/eventbridge.tf:97 |
| inf-canonical-prices-daily | {system}-inf-canonical-prices-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/eventbridge.tf:132 |
| inf-gold-trigger-dlq | {system}-inf-gold-trigger-dlq | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/inf-pipeline/eventbridge.tf:164 |
| inf-gold-full-on-bronze-complete | {system}-inf-gold-full-on-bronze-complete | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/eventbridge.tf:271 |
| inf-gold-incremental-daily | {system}-inf-gold-incremental-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/eventbridge.tf:367 |
| inf-andrew-otp-write | {system}-inf-andrew-otp-write-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:15 |
| ycharts-credentials-read | ycharts-credentials-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:49 |
| inf-gold-layer-ec2-role | advi-inf-gold-layer-ec2-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:74 |
| inf-gold-layer-profile | {system}-inf-gold-layer-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/inf-pipeline/iam.tf:92 |
| s3-scoped-inf | {system}-inf-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:97 |
| runner-shared-read | {system}-runner-shared-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:123 |
| ssm-access | {system}-ssm-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:149 |
| cloudwatch-logs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:177 |
| cloudwatch-put-metric | {system}-cloudwatch-put-metric-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:201 |
| sns-publish-chainfatal | {system}-sns-publish-chainfatal-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:228 |
| kms-ebs-decrypt | {system}-kms-ebs-decrypt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:246 |
| self-stop | {system}-self-stop-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:264 |
| describe-tags-self | {system}-describe-tags-self-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:290 |
| cloudfront-invalidate | {system}-cloudfront-invalidate-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:318 |
| inf-gold-layer-lambda-role | advi-inf-gold-layer-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:338 |
| inf-s3-scoped | {system}-inf-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:356 |
| inf-gold-trigger-lambda-role | advi-inf-gold-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:391 |
| inf-gold-trigger-policy | {system}-inf-gold-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:409 |
| inf-exporter-ec2-role | advi-inf-exporter-ec2-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:495 |
| inf-exporter-profile | {system}-inf-exporter-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/inf-pipeline/iam.tf:513 |
| s3-scoped-inf-exporter | {system}-inf-s3-scoped-exporter-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:518 |
| secrets-manager-orion | orion-secrets-manager-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:547 |
| secrets-manager-orion-jwt | orion-secrets-manager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:574 |
| sns-otp-alert | {system}-sns-otp-alert-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:596 |
| kms-ebs-decrypt | {system}-kms-ebs-decrypt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:611 |
| cloudfront-invalidate | {system}-cloudfront-invalidate-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:625 |
| invoke-publisher-fanout | {system}-invoke-publisher-fanout-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:640 |
| inf-jwt-trigger-lambda-role | advi-inf-jwt-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:661 |
| inf-jwt-trigger-policy | {system}-inf-jwt-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:679 |
| inf-jwt-trigger-dynamo | {system}-inf-jwt-trigger-dynamo-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:749 |
| inf-jwt-trigger-kms | {system}-inf-jwt-trigger-kms-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:772 |
| inf-bronze-trigger-lambda-role | advi-inf-bronze-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:810 |
| inf-bronze-trigger-policy | {system}-inf-bronze-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:828 |
| inf-assets-trigger-lambda-role | advi-inf-assets-trigger-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:886 |
| inf-assets-trigger-policy | {system}-inf-assets-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:904 |
| inf-assets-trigger-kms | {system}-inf-assets-trigger-kms-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:946 |
| inf-silver-aggregator-lambda-role | advi-inf-silver-aggregator-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:989 |
| inf-silver-aggregator-policy | {system}-inf-silver-aggregator-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:1007 |
| inf-eventbridge-ssm-role | advi-inf-eventbridge-ssm-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/iam.tf:1063 |
| ssm-send-command-inf-jwt-fetch | {system}-inf-ssm-send-command-jwt-fetch-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:1081 |
| cloudwatch-put-metric | {system}-cloudwatch-put-metric-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/iam.tf:1100 |
| inf-accounts-v2-daily-role | advi-inf-accounts-v2-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-accounts-v2-daily.tf:37 |
| s3-accounts-v2 | {system}-s3-accounts-v2-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-accounts-v2-daily.tf:55 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-accounts-v2-daily.tf:131 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-accounts-v2-daily.tf:146 |
| inf-accounts-v2-daily | advi-inf-accounts-v2-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-accounts-v2-daily.tf:196 |
| inf-api-assets-v2-lambda-role | advi-inf-api-assets-v2-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf:29 |
| s3-assets-v2 | {system}-s3-assets-v2-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf:47 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf:119 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf:134 |
| inf-api-assets-v2-daily | {system}-inf-api-assets-v2-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-api-assets-v2.tf:185 |
| inf-api-positions-role | advi-inf-api-positions-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-api-positions.tf:27 |
| s3-positions | {system}-s3-positions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-positions.tf:45 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-positions.tf:118 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-positions.tf:133 |
| inf-api-positions-daily | {system}-inf-api-positions-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-api-positions.tf:179 |
| inf-api-reps-role | advi-inf-api-reps-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-api-reps.tf:32 |
| s3-reps | {system}-s3-reps-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-reps.tf:50 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-reps.tf:122 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-reps.tf:137 |
| inf-api-reps-daily | {system}-inf-api-reps-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-api-reps.tf:184 |
| inf-api-txn-role | advi-inf-api-txn-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-api-txn.tf:27 |
| s3-txn | {system}-s3-txn-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-txn.tf:45 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-txn.tf:101 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-api-txn.tf:116 |
| inf-api-txn-daily | {system}-inf-api-txn-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-api-txn.tf:166 |
| inf-assets-trigger-bronze-complete | {system}-inf-assets-trigger-bronze-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-assets-trigger.tf:17 |
| inf-billing-daily-role | advi-inf-billing-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-billing-daily.tf:26 |
| s3-billing | {system}-s3-billing-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-billing-daily.tf:44 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-billing-daily.tf:88 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-billing-daily.tf:103 |
| inf-billing-daily | advi-inf-billing-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-billing-daily.tf:139 |
| inf-bronze-runner-sg | {system}-inf-bronze-runner-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:23 |
| inf-bronze-runner-ec2-role | advi-inf-bronze-runner-ec2-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:42 |
| inf-bronze-runner-profile | {system}-inf-bronze-runner-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:60 |
| s3-scoped-inf | {system}-inf-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:65 |
| cloudwatch-logs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:136 |
| cloudwatch-put-metric | {system}-cloudwatch-put-metric-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:154 |
| sns-otp-alert | {system}-sns-otp-alert-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:174 |
| kms-ebs-decrypt | {system}-kms-ebs-decrypt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:189 |
| inf-bronze-runner | advi-inf-bronze-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:219 |
| cloudwatch-histbf-namespace | {system}-cloudwatch-histbf-namespace-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:265 |
| cloudwatch-jwtres-namespace | {system}-cloudwatch-jwtres-namespace-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:286 |
| secrets-manager-orion-jwt-read | orion-secrets-manager-jwt-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:309 |
| s3-rate-limit-state | {system}-s3-rate-limit-state-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:331 |
| bronze-modemarker-rw | {system}-bronze-modemarker-rw-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:353 |
| jwt-trigger-invoke | {system}-jwt-trigger-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-bronze-runner.tf:375 |
| inf-ec2-launch-monitor-lambda-role | advi-inf-ec2-launch-monitor-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-ec2-launch-monitor.tf:22 |
| inf-ec2-launch-monitor-policy | {system}-inf-ec2-launch-monitor-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-ec2-launch-monitor.tf:40 |
| opal-inf-ec2-state-change-monitor | opal-inf-ec2-state-change-monitor-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-ec2-launch-monitor.tf:93 |
| inf-ec2-retry-launch-lambda-role | advi-inf-ec2-retry-launch-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-ec2-retry-launch.tf:21 |
| inf-ec2-retry-launch-policy | {system}-inf-ec2-retry-launch-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-ec2-retry-launch.tf:39 |
| inf-ec2-retry-launch-kms | {system}-inf-ec2-retry-launch-kms-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-ec2-retry-launch.tf:90 |
| inf-etf-ownership-daily-role | etfs-inf-etf-ownership-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf:89 |
| s3-etf-ownership | {system}-s3-etf-ownership-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf:110 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf:200 |
| inf-etf-ownership-daily-schedule | {system}-inf-etf-ownership-schedule-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-etf-ownership-daily.tf:260 |
| /aws/events/inf-gold-dispatch-release-audit | /aws/events/{system}-inf-gold-dispatch-release-audit-{cadence} | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/inf-pipeline/inf-gold-dispatch-release-alarm.tf:40 |
| inf-gold-dispatch-release-alarm | {system}-inf-gold-dispatch-release-alarm-topic | OUT-OF-PATTERN | SNS_TOPIC | repo | infra/aws/terraform/inf-pipeline/inf-gold-dispatch-release-alarm.tf:78 |
| inf-gold-dispatch-release-changed | {system}-inf-gold-dispatch-release-changed-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-gold-dispatch-release-alarm.tf:102 |
| inf-gold-qa-runner-sg | {system}-inf-gold-qa-runner-sg | OUT-OF-PATTERN | SECURITY_GROUP | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:29 |
| inf-gold-qa-runner-ec2-role | advi-inf-gold-qa-runner-ec2-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:52 |
| inf-gold-qa-runner-profile | {system}-inf-gold-qa-runner-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:70 |
| s3-qa-scoped | {system}-s3-qa-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:75 |
| ssm-access | {system}-ssm-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:145 |
| cloudwatch-logs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:173 |
| kms-ebs-decrypt | {system}-kms-ebs-decrypt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:192 |
| self-stop | {system}-self-stop-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:210 |
| describe-tags-self | {system}-describe-tags-self-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:235 |
| inf-gold-qa-runner | {system}-inf-gold-qa-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/inf-pipeline/inf-gold-qa-runner.tf:259 |
| inf-nna-partition-checker-lambda-role | advi-inf-nna-partition-checker-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-nna-partition-checker.tf:37 |
| inf-nna-partition-checker-scoped | {system}-inf-nna-partition-checker-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-nna-partition-checker.tf:60 |
| inf-nna-partition-check-trigger | {system}-inf-nna-partition-check-trigger-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-nna-partition-checker.tf:97 |
| inf-nna-partition-completeness-breach | advi-inf-nna-partition-completeness-breach-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/inf-nna-partition-checker.tf:131 |
| inf-performance-daily-role | advi-inf-performance-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-performance-daily.tf:28 |
| s3-performance | {system}-s3-performance-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-performance-daily.tf:46 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-performance-daily.tf:97 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-performance-daily.tf:112 |
| inf-performance-daily | advi-inf-performance-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-performance-daily.tf:148 |
| inf-silver-chain-lambda-role | advi-inf-silver-chain-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-silver-chain.tf:20 |
| inf-silver-chain-s3 | {system}-inf-silver-chain-s3-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-silver-chain.tf:38 |
| inf-silver-chain-bronze-complete | {system}-inf-silver-chain-bronze-complete-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-silver-chain.tf:135 |
| Inflection-SilverChain-DimConversionFailure | advi-inf-silver-chain-dim-conversion-failure-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/inf-silver-chain.tf:181 |
| inf-tax-daily-role | advi-inf-tax-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-tax-daily.tf:32 |
| s3-tax | {system}-s3-tax-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-tax-daily.tf:50 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-tax-daily.tf:101 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-tax-daily.tf:116 |
| inf-tax-daily | advi-inf-tax-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-tax-daily.tf:158 |
| inf-unified-account-dim-daily-role | advi-inf-unified-account-dim-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf:36 |
| s3-unified-account-dim | {system}-s3-unified-account-dim-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf:54 |
| secretsmanager-jwt | {system}-secretsmanager-jwt-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf:102 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf:117 |
| inf-unified-account-dim-daily | advi-inf-unified-account-dim-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/inf-unified-account-dim-daily.tf:163 |
| inf-otp-relay-lambda-role | advi-inf-otp-relay-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-pipeline/lambda-otp-relay.tf:10 |
| s3-otp-rw | {system}-s3-otp-rw-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/lambda-otp-relay.tf:25 |
| secrets-read-otp-token | {system}-secrets-read-otp-token-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-pipeline/lambda-otp-relay.tf:46 |
| inf-otp-state-change | {system}-inf-otp-state-change-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/inf-pipeline/lambda-otp-relay.tf:99 |
| inf-bronze-trigger-missed-start | advi-inf-bronze-trigger-missed-start-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/inf-pipeline/lambdas.tf:364 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/terraform/inf-pipeline/s3.tf:7 |
| inf/otp-relay/token | {system}/inf/otp-relay/token | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/inf-pipeline/secrets-otp.tf:15 |
| orion/credentials | orion/credentials | CONFORMANT | SECRET | repo | infra/aws/terraform/inf-pipeline/secrets.tf:10 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/terraform/inf-pipeline/secrets.tf:22 |
| orion/eclipse_jwt/current | orion/eclipse-jwt/current | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/inf-pipeline/secrets.tf:33 |
| ycharts/credentials | ycharts/credentials | CONFORMANT | SECRET | repo | infra/aws/terraform/inf-pipeline/secrets.tf:66 |
| inf-otp-alert | {system}-inf-otp-alert-topic | OUT-OF-PATTERN | SNS_TOPIC | repo | infra/aws/terraform/inf-pipeline/sns.tf:9 |
| opal-inf-export-run | opal-inf-export-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/inf-pipeline/ssm-inf-exporter.tf:8 |
| opal-inf-test-login-stage1 | opal-inf-test-login-stage1-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/inf-pipeline/ssm-inf-exporter.tf:63 |
| opal-inf-test-login-stage2 | opal-inf-test-login-stage2-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/inf-pipeline/ssm-inf-exporter.tf:95 |
| opal-inf-test-login-stage3 | opal-inf-test-login-stage3-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/inf-pipeline/ssm-inf-exporter.tf:128 |
| opal-inf-jwt-fetch | opal-inf-jwt-fetch-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/inf-pipeline/ssm-inf-jwt-fetch.tf:8 |
| opal-inf-jwt-setup | opal-inf-jwt-setup-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/inf-pipeline/ssm-inf-jwt-setup.tf:9 |
| opal-inf-value-parity | opal-inf-value-parity-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/inf-value-parity/inf_value_parity.tf:75 |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-value-parity/inf_value_parity.tf:80 |
| InfServedAndSourceRead | {system}-inf-served-and-source-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-value-parity/inf_value_parity.tf:95 |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-value-parity/inf_value_parity.tf:112 |
| opal-inf-value-parity | opal-inf-value-parity-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/inf-value-parity/inf_value_parity.tf:125 |
| opal-inf-value-parity-hourly | opal-inf-value-parity-hourly | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/inf-value-parity/inf_value_parity.tf:155 |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/inf-value-parity/inf_value_parity.tf:200 |
| irpt-requests | irpt-requests-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/investor-reporting/core/dynamodb.tf:28 |
| irpt-jobs | irpt-jobs-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/investor-reporting/core/dynamodb.tf:55 |
| irpt-outbox | irpt-outbox-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/investor-reporting/core/dynamodb.tf:83 |
| irpt-checkpoints | irpt-checkpoints-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/investor-reporting/core/dynamodb.tf:113 |
| irpt-core-quarantine-prefix | irpt-core-quarantine-prefix-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/core/iam_firm_conditions.tf:81 |
| opal-data-ycharts | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/investor-reporting/core/s3.tf:20 |
| irpt-directory-role | irpt-directory-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/directory/iam.tf:56 |
| irpt-directory-policy | irpt-directory-policy | CONFORMANT | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/directory/iam.tf:81 |
| irpt-holdings-snapshot-scheduler-role | irpt-holdings-snapshot-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/directory/schedule.tf:46 |
| irpt-holdings-snapshot-scheduler-policy | irpt-holdings-snapshot-scheduler-policy | CONFORMANT | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/directory/schedule.tf:61 |
| irpt-holdings-snapshot | irpt-holdings-snapshot-{cadence} | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/investor-reporting/directory/schedule.tf:67 |
| irpt-directory-refresh-role | irpt-directory-refresh-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/directory/schedule.tf:198 |
| irpt-directory-refresh-policy | irpt-directory-refresh-policy | CONFORMANT | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/directory/schedule.tf:325 |
| irpt-directory-refresh-scheduler-role | irpt-directory-refresh-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/directory/schedule.tf:343 |
| irpt-directory-refresh-scheduler-policy | irpt-directory-refresh-scheduler-policy | CONFORMANT | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/directory/schedule.tf:358 |
| irpt-directory-refresh | irpt-directory-refresh-{cadence} | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/investor-reporting/directory/schedule.tf:377 |
| irpt-export-render-role | irpt-export-render-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/export/iam.tf:42 |
| irpt-export-render-logs | irpt-export-render-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/export/iam.tf:58 |
| irpt-export-render-evidence | irpt-export-render-evidence-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/export/iam.tf:85 |
| irpt-export-render-dispatch | irpt-export-render-dispatch-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/export/iam.tf:130 |
| irpt-export-render-host-evidence | irpt-export-render-host-evidence-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/export/iam.tf:194 |
| irpt-export-render-run | irpt-export-render-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/investor-reporting/export/ssm.tf:19 |
| irpt-holdings-role | irpt-holdings-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/holdings/iam.tf:28 |
| irpt-holdings-logs | irpt-holdings-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/holdings/iam.tf:44 |
| irpt-holdings-firm-read | irpt-holdings-firm-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/holdings/iam.tf:68 |
| irpt-narrative-role | irpt-narrative-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/narrative/iam.tf:32 |
| irpt-narrative-logs | irpt-narrative-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/narrative/iam.tf:48 |
| irpt-narrative-news-read | irpt-narrative-news-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/narrative/iam.tf:72 |
| irpt-status-role | irpt-status-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/ops/iam.tf:33 |
| irpt-status-policy | irpt-status-policy | CONFORMANT | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/ops/iam.tf:81 |
| irpt-performance-adapter-role | irpt-performance-adapter-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/performance/iam.tf:23 |
| irpt-performance-adapter-logs | irpt-performance-adapter-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/performance/iam.tf:39 |
| irpt-common | irpt-common-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/investor-reporting/performance/layers.tf:41 |
| irpt-ycharts-runner-role | irpt-ycharts-runner-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/investor-reporting/ycharts/iam.tf:68 |
| irpt-ycharts-runner | irpt-ycharts-runner-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/investor-reporting/ycharts/iam.tf:86 |
| irpt-ycharts-runner-profile | irpt-ycharts-runner-profile | CONFORMANT | INSTANCE_PROFILE | repo | infra/aws/terraform/investor-reporting/ycharts/iam.tf:151 |
| irpt-ycharts-runner-sg | irpt-ycharts-runner-sg | CONFORMANT | SECURITY_GROUP | repo | infra/aws/terraform/investor-reporting/ycharts/instance.tf:45 |
| irpt-ycharts-runner | irpt-ycharts-runner | CONFORMANT | EC2_INSTANCE | repo | infra/aws/terraform/investor-reporting/ycharts/instance.tf:61 |
| ycharts/session/research-20260911 | ycharts/session/research-20260911 | CONFORMANT | SECRET | repo | infra/aws/terraform/investor-reporting/ycharts/research_absorbed.tf:46 |
| /aws/lambda/irpt-ycharts-research-20260911 | /aws/lambda/irpt-ycharts-research-20260911-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/investor-reporting/ycharts/research_absorbed.tf:57 |
| irpt-ycharts-deploy | irpt-ycharts-deploy-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/investor-reporting/ycharts/ssm.tf:19 |
| irpt-ycharts-run | irpt-ycharts-run-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/investor-reporting/ycharts/ssm.tf:56 |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/market-overview/cross-firm-secret-deny.tf:30 |
| market-updates | {system}-market-updates-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/market-overview/dynamo.tf:7 |
| fear-greed-daily-update | {system}-fear-greed-update-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/market-overview/eventbridge.tf:20 |
| market-rsi-tiered-daily | {system}-market-rsi-tiered-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/market-overview/eventbridge.tf:44 |
| trending-topics-portal-publisher-morning | {system}-trending-topics-portal-publisher-morning-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/market-overview/eventbridge.tf:68 |
| trending-topics-portal-publisher-afternoon | {system}-trending-topics-portal-publisher-afternoon-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/market-overview/eventbridge.tf:82 |
| trending-topics-portal-publisher-daily | {system}-trending-topics-portal-publisher-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/market-overview/eventbridge.tf:105 |
| opal-lambda-market-rsi-role | opal-lambda-market-rsi-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/market-overview/iam.tf:18 |
| MarketRSITieredPolicy | {system}-market-rsi-tiered-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/market-overview/iam.tf:32 |
| market-data-generator-lambda-role | {system}-market-data-generator-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/market-overview/iam_legacy.tf:15 |
| market-data-generator-permissions | {system}-market-data-generator-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/market-overview/iam_legacy.tf:34 |
| market-update-lambda-role | {system}-market-update-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/market-overview/iam_legacy.tf:101 |
| opal-portal-data-proxy | opal-portal-data-proxy-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/market-overview/lambdas.tf:89 |
| /aws/lambda/opal-portal-data-proxy | /aws/lambda/opal-portal-data-proxy-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/market-overview/lambdas.tf:108 |
| opal-portal-volatility-fetcher | opal-portal-volatility-fetcher-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/market-overview/lambdas.tf:126 |
| /aws/lambda/opal-portal-volatility-fetcher | /aws/lambda/opal-portal-volatility-fetcher-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/market-overview/lambdas.tf:145 |
| volatility-daily-update | {system}-volatility-update-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/market-overview/lambdas.tf:155 |
| market-update-dynamodb-scoped | {system}-market-update-dynamodb-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/market-overview/least-privilege-dataplane.tf:26 |
| market-update-secrets-read | {system}-market-update-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/market-overview/least-privilege-secrets.tf:46 |
| opal-market-data-v2 | opal-313476888478-market-data-v2 | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/market-overview/s3.tf:5 |
| mdpf-accrual-trigger-role | mdpf-accrual-trigger-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/accrual-bridge.tf:29 |
| mdpf-accrual-trigger-scoped | mdpf-accrual-trigger-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/accrual-bridge.tf:48 |
| mdpf-accrual-scheduler-role | mdpf-accrual-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/accrual-bridge.tf:132 |
| invoke-the-accrual-trigger | {system}-invoke-the-accrual-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/accrual-bridge.tf:151 |
| mdpf-accrual-bridge-daily | mdpf-accrual-bridge-daily | CONFORMANT | SCHEDULE | repo | infra/aws/terraform/mdpf-pipeline/accrual-bridge.tf:165 |
| mdpf-daily-trigger-dlq-not-empty | mdpf-daily-trigger-dlq-not-empty-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/mdpf-pipeline/alarms.tf:13 |
| mdpf-daily-runner-sg | mdpf-daily-runner-sg | CONFORMANT | SECURITY_GROUP | repo | infra/aws/terraform/mdpf-pipeline/ec2.tf:11 |
| mdpf-daily-runner | mdpf-daily-runner | CONFORMANT | EC2_INSTANCE | repo | infra/aws/terraform/mdpf-pipeline/ec2.tf:30 |
| mdpf-daily-trigger-dlq | mdpf-daily-trigger-dlq | CONFORMANT | SQS_QUEUE | repo | infra/aws/terraform/mdpf-pipeline/eventbridge.tf:23 |
| mdpf-feeder-trigger-role | mdpf-feeder-trigger-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/feeder-trigger.tf:62 |
| mdpf-feeder-trigger | mdpf-feeder-trigger-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/feeder-trigger.tf:80 |
| mdpf-feeder-scheduler-role | mdpf-feeder-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/feeder-trigger.tf:194 |
| invoke-the-feeder-trigger-plus-dlq | {system}-invoke-the-feeder-trigger-plus-dlq-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/feeder-trigger.tf:212 |
| mdpf-feeder-backstop-daily | mdpf-feeder-backstop-daily | CONFORMANT | SCHEDULE | repo | infra/aws/terraform/mdpf-pipeline/feeder-trigger.tf:233 |
| mdpf-feeder-accelerator | mdpf-feeder-accelerator-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/mdpf-pipeline/feeder-trigger.tf:259 |
| mdpf-gold-calendar-deps | mdpf-gold-calendar-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/mdpf-pipeline/gold-lambda.tf:81 |
| mdpf-gold-lambda | mdpf-gold-lambda | CONFORMANT | LAMBDA | repo | infra/aws/terraform/mdpf-pipeline/gold-lambda.tf:96 |
| mdpf-daily-runner-ec2-role | mdpf-daily-runner-ec2-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/iam.tf:12 |
| mdpf-daily-runner-profile | mdpf-daily-runner-profile | CONFORMANT | INSTANCE_PROFILE | repo | infra/aws/terraform/mdpf-pipeline/iam.tf:30 |
| mdpf-runner-scoped | mdpf-runner-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/iam.tf:41 |
| mdpf-gold-lambda-role | mdpf-gold-lambda-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/iam.tf:733 |
| mdpf-gold-scoped | mdpf-gold-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/iam.tf:756 |
| mdpf-floor-scheduler-role | mdpf-floor-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/scheduled-floor.tf:61 |
| invoke-the-daily-trigger-plus-dlq | {system}-invoke-the-daily-trigger-plus-dlq-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/scheduled-floor.tf:80 |
| mdpf-scheduled-floor | mdpf-scheduled-floor-{cadence} | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/mdpf-pipeline/scheduled-floor.tf:110 |
| wsb-49f-model-aua-daily-role | mdpf-49f-wsb-model-aua-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:29 |
| wsb-49f-model-aua-daily | mdpf-49f-wsb-model-aua-daily-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:48 |
| wsd-49f-partner-held-etf-daily-role | mdpf-49f-wsd-partner-held-etf-daily-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:120 |
| wsd-49f-partner-held-etf-daily | mdpf-49f-wsd-partner-held-etf-daily-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:139 |
| wp5-49f-feeder-scheduler-role | mdpf-49f-wp5-feeder-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:215 |
| invoke-the-two-feeders | {system}-invoke-the-two-feeders-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:234 |
| wsb-49f-model-aua-pull-daily | {system}-49f-wsb-model-aua-pull-daily | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:251 |
| wsd-49f-partner-held-etf-pull-daily | {system}-49f-wsd-partner-held-etf-pull-daily | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:270 |
| wsb-49f-model-aua-daily-errors | {system}-49f-wsb-model-aua-daily-errors-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:305 |
| wsd-49f-partner-held-etf-daily-errors | {system}-49f-wsd-partner-held-etf-daily-errors-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/mdpf-pipeline/wp5-feeder-schedules.tf:325 |
| CloudWatchLogs | {system}-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/modules/served-guard/main.tf:65 |
| ServedKeyGuardS3 | {system}-served-key-guard-s3-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/modules/served-guard/main.tf:80 |
| RecheckQueue | {system}-recheck-queue-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/modules/served-guard/main.tf:111 |
| PublishSurfaceAlerts | {system}-publish-surface-alerts-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/modules/served-guard/main.tf:129 |
| cross-firm-bucket-read-deny | {system}-cross-firm-bucket-read-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/cross-firm-bucket-read-deny.tf:72 |
| cross-firm-bucket-write-deny | {system}-cross-firm-bucket-write-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/cross-firm-bucket-write-deny.tf:42 |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/cross-firm-secret-deny.tf:45 |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/cross-firm-secret-deny.tf:92 |
| layer3-gpt-curation-daily | {system}-layer3-gpt-curation-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/news-pipeline/eventbridge.tf:167 |
| keyword-intelligence-generator-daily | {system}-keyword-intelligence-generator-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/news-pipeline/eventbridge.tf:175 |
| keyword-drilldown-generator-daily | {system}-keyword-drilldown-generator-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/news-pipeline/eventbridge.tf:631 |
| finbert-batch-processor | {system}-finbert-batch-processor-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/news-pipeline/finbert-batch.tf:21 |
| /aws/lambda/finbert-batch-processor | /aws/lambda/{system}-finbert-batch-processor-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/news-pipeline/finbert-batch.tf:41 |
| finbert-scoring-post-ingestion | {system}-finbert-scoring-post-ingestion-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/news-pipeline/finbert-batch.tf:47 |
| finbert-scoring-post-ingestion-45min | {system}-finbert-scoring-post-ingestion-45min-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/news-pipeline/finbert-batch.tf:71 |
| keyword-intelligence-dynamodb-and-invoke | {system}-keyword-intelligence-dynamodb-and-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/iam.tf:85 |
| s3-portal-write | {system}-s3-portal-write-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/iam.tf:112 |
| SecretsManagerAccess | {system}-secretsmanager-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/iam.tf:130 |
| invoke-trending-publisher | {system}-invoke-trending-publisher-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/iam.tf:187 |
| layer3-bd-securities-read | {system}-49f-layer3-securities-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/iam.tf:368 |
| opal-layer3-ec2-role | opal-layer3-ec2-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/news-pipeline/iam.tf:389 |
| Layer3EC2Policy | {system}-layer3-ec2-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/news-pipeline/iam.tf:403 |
| semantic-trending-topics-portal-publisher | {system}-semantic-trending-topics-portal-publisher-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/news-pipeline/lambdas.tf:230 |
| /aws/lambda/semantic-trending-topics-portal-publisher | /aws/lambda/{system}-semantic-trending-topics-portal-publisher-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/news-pipeline/lambdas.tf:306 |
| keyword-intelligence-generator | {system}-keyword-intelligence-generator-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/news-pipeline/lambdas.tf:329 |
| /aws/lambda/keyword-intelligence-generator | /aws/lambda/{system}-keyword-intelligence-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/news-pipeline/lambdas.tf:355 |
| opal-keyword-drilldown-generator | opal-keyword-drilldown-generator-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/news-pipeline/lambdas.tf:372 |
| /aws/lambda/opal-keyword-drilldown-generator | /aws/lambda/opal-keyword-drilldown-generator-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/news-pipeline/lambdas.tf:396 |
| opal-keyword-intelligence | opal-keyword-intelligence-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/news-pipeline/main.tf:48 |
| opal/openai/layer3-curation | opal/openai/layer3-curation | CONFORMANT | SECRET | repo | infra/aws/terraform/news-pipeline/secrets.tf:15 |
| opal/openai/news-trending | opal/openai/news-trending | CONFORMANT | SECRET | repo | infra/aws/terraform/news-pipeline/secrets.tf:25 |
| agentbus-ajbdev-sitez-to-laptop.fifo | agentbus-ajbdev-sitez-to-laptop-queue.fifo | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/nfra-agentbus-port2/sqs.tf:23 |
| agentbus-ajbdev-laptop-to-sitez.fifo | agentbus-ajbdev-laptop-to-sitez-queue.fifo | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/nfra-agentbus-port2/sqs.tf:38 |
| advi-49f-floor-dlq | advi-49f-floor-dlq | CONFORMANT | SQS_QUEUE | repo | infra/aws/terraform/opal-assets/advi_49f_floor.tf:57 |
| advi-49f-floor-scheduler-role | advi-49f-floor-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/opal-assets/advi_49f_floor.tf:64 |
| invoke-the-dispatcher-plus-dlq | {system}-invoke-the-dispatcher-plus-dlq-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-assets/advi_49f_floor.tf:79 |
| advi-49f-chain-dispatch | advi-49f-chain-dispatch-document | OUT-OF-PATTERN | SSM_DOCUMENT | repo | infra/aws/terraform/opal-assets/advi_49f_floor.tf:223 |
| advi-49f-gold-floor | advi-49f-gold-floor-{cadence} | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/opal-assets/advi_49f_floor.tf:302 |
| advi-49f-publisher | advi-49f-publisher-{cadence} | OUT-OF-PATTERN | SCHEDULE | repo | infra/aws/terraform/opal-assets/advi_49f_publisher.tf:75 |
| opal-advi-stitch-landing-role | advi-stitch-landing-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/opal-assets/advi_stitch_landing.tf:25 |
| opal-advi-stitch-landing-scoped | advi-stitch-landing-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-assets/advi_stitch_landing.tf:46 |
| invoke-the-publisher | {system}-invoke-the-publisher-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-assets/mdpf_portal_publisher.tf:198 |
| opal-assets-mirror-cot-scheduler-role | opal-cot-assets-mirror-scheduler-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/opal-assets/mirror.tf:116 |
| invoke-the-mirror | {system}-invoke-the-mirror-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-assets/mirror.tf:131 |
| opal-assets-one-way-fan-in-fence | opal-assets-one-way-fan-in-fence-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-assets/router_iam.tf:139 |
| opal-assets-read | opal-assets-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-assets/router_iam.tf:256 |
| opal-assets-silver-dlq | opal-assets-silver-dlq | CONFORMANT | SQS_QUEUE | repo | infra/aws/terraform/opal-assets/silver.tf:260 |
| opal-assets-silver-dlq-access | opal-assets-silver-dlq-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-assets/silver.tf:277 |
| opal-mcp-audit | opal-313476888478-mcp-audit | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/opal-gateway/audit-lake.tf:17 |
| opal-mcp-athena-results | opal-313476888478-mcp-athena-results | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/opal-gateway/audit-lake.tf:51 |
| opal-ms-ingest-liveness-role | opal-ms-ingest-liveness-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/opal-gateway/ms-ingest.tf:27 |
| opal-ms-ingest-liveness | opal-ms-ingest-liveness-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-gateway/ms-ingest.tf:37 |
| opal-ms-ingest-liveness | opal-ms-ingest-liveness-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/opal-gateway/ms-ingest.tf:74 |
| opal-ms-ingest-liveness-6h | opal-ms-ingest-liveness-6h-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/opal-gateway/ms-ingest.tf:101 |
| opal-critical-surface-alerts-coo | opal-critical-surface-alerts-coo-queue | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/opal-gateway/otp-alert-sqs.tf:35 |
| opal-otp-liveness-role | opal-otp-liveness-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/opal-gateway/otp-liveness.tf:22 |
| opal-otp-liveness | opal-otp-liveness-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opal-gateway/otp-liveness.tf:32 |
| opal-otp-liveness | opal-otp-liveness-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/opal-gateway/otp-liveness.tf:71 |
| opal-otp-liveness-6h | opal-otp-liveness-6h-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/opal-gateway/otp-liveness.tf:100 |
| opal/mcp/opal-gateway-fernet | opal/mcp/opal-gateway-fernet | CONFORMANT | SECRET | repo | infra/aws/terraform/opal-gateway/secrets.tf:16 |
| opal/mcp/opal-gateway-jwt | opal/mcp/opal-gateway-jwt | CONFORMANT | SECRET | repo | infra/aws/terraform/opal-gateway/secrets.tf:27 |
| opal/mcp/opal-gateway-graph | opal/mcp/opal-gateway-graph | CONFORMANT | SECRET | repo | infra/aws/terraform/opal-gateway/secrets.tf:38 |
| opal/mcp/opal-gateway-login | opal/mcp/opal-gateway-login | CONFORMANT | SECRET | repo | infra/aws/terraform/opal-gateway/secrets.tf:49 |
| opal-mcp-emp-alyssa-read | opal-mcp-emp-alyssa-read-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/opal-gateway/taxsma_gateway_iam.tf:65 |
| opal-mcp-emp-alyssa-read-policy | opal-mcp-emp-alyssa-read-policy | CONFORMANT | IAM_POLICY | repo | infra/aws/terraform/opal-gateway/taxsma_gateway_iam.tf:71 |
| opal-mcp-emp-alyssa-onboard | opal-mcp-emp-alyssa-onboard-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/opal-gateway/taxsma_gateway_iam.tf:98 |
| opal-mcp-emp-alyssa-onboard-policy | opal-mcp-emp-alyssa-onboard-policy | CONFORMANT | IAM_POLICY | repo | infra/aws/terraform/opal-gateway/taxsma_gateway_iam.tf:104 |
| opal-suspicious-addresses | opal-suspicious-addresses-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/opsec/dynamodb.tf:57 |
| opal-security-admin | opal-security-admin-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/opsec/iam.tf:19 |
| opal-security-admin-evidence-and-key | opal-security-admin-evidence-and-key-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opsec/iam.tf:54 |
| opal-ipset-reconciler | opal-ipset-reconciler-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/opsec/iam_reconciler_and_cli.tf:97 |
| opal-ipset-reconciler-table-stream-and-sets | opal-ipset-reconciler-table-stream-and-sets-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opsec/iam_reconciler_and_cli.tf:120 |
| opal-ipblock-cli | opal-ipblock-cli-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/opsec/iam_reconciler_and_cli.tf:232 |
| opal-ipblock-cli-row-only | opal-ipblock-cli-row-only-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opsec/iam_reconciler_and_cli.tf:261 |
| opal-sentinel | opal-sentinel-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/opsec/iam_sentinel.tf:60 |
| opal-sentinel-table-evidence-and-notify | opal-sentinel-table-evidence-and-notify-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/opsec/iam_sentinel.tf:83 |
| opal-ipset-reconciler | opal-ipset-reconciler-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/opsec/reconciler-lambda.tf:31 |
| /aws/lambda/opal-ipset-reconciler | /aws/lambda/opal-ipset-reconciler-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/opsec/reconciler-lambda.tf:75 |
| opal-ipset-reconciler-daily | opal-ipset-reconciler-daily | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/opsec/reconciler-lambda.tf:122 |
| opal-security-evidence | opal-313476888478-security-evidence | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/opsec/s3_evidence.tf:47 |
| opal-sentinel-daily-digest | opal-sentinel-digest-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/opsec/sentinel.tf:157 |
| opal-partner-etl-ops-alerts | opal-partner-etl-ops-alerts | CONFORMANT | SNS_TOPIC | repo | infra/aws/terraform/partner-etl-ops-alerts/ops-alerts.tf:10 |
| partner-etl-ops-queue | {system}-partner-etl-ops-queue | OUT-OF-PATTERN | SQS_QUEUE | repo | infra/aws/terraform/partner-etl-ops-alerts/ops-alerts.tf:15 |
| partners-lambda-role | {system}-partners-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/partners-api/iam.tf:9 |
| partners-lambda-permissions | {system}-partners-lambda-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/partners-api/iam.tf:36 |
| FIRMSEP-auth-advisor-scoping-denied | firmsep-auth-advisor-scoping-denied-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:40 |
| FIRMSEP-auth-tier-denied | firmsep-auth-tier-denied-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:74 |
| FIRMSEP-auth-ownership-map-fetch-failed | firmsep-auth-ownership-map-fetch-failed-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:108 |
| FIRMSEP-auth-ownership-map-schema-mismatch | firmsep-auth-ownership-map-schema-mismatch-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:142 |
| FIRMSEP-shared-advisor-router-denied | firmsep-shared-advisor-router-denied-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:184 |
| FIRMSEP-s3-direct-access-bypass | firmsep-s3-direct-access-bypass-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:225 |
| OPSEC-auth-login-rate-limit-blocked | {system}-opsec-auth-login-rate-limit-blocked-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:334 |
| OPSEC-auth-throttled | {system}-opsec-auth-throttled-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/portal-auth/cloudwatch-alarms.tf:377 |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portal-auth/cross-firm-secret-deny.tf:86 |
| opal-firms | opal-firms-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/portal-auth/dynamodb.tf:18 |
| opal-sessions | opal-sessions-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/portal-auth/dynamodb.tf:46 |
| user-permissions | {system}-user-permissions-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/portal-auth/dynamodb.tf:88 |
| opal-offices | opal-offices-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/portal-auth/dynamodb.tf:120 |
| opal-portal-auth-throttle | opal-portal-auth-throttle-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/portal-auth/dynamodb.tf:195 |
| opal-portal-auth-mfa | opal-portal-auth-mfa-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/portal-auth/dynamodb.tf:230 |
| opalinvest.dev |  | NOT-GRADED | ROUTE53_RECORD | repo | infra/aws/terraform/portal-auth/email-auth-dns.tf:46 |
| _dmarc.opalinvest.dev |  | NOT-GRADED | ROUTE53_RECORD | repo | infra/aws/terraform/portal-auth/email-auth-dns.tf:73 |
| opalinvest-auth-lambda-role | {system}-opalinvest-auth-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/portal-auth/iam.tf:15 |
| opalinvest-auth-permissions | {system}-opalinvest-auth-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portal-auth/iam.tf:33 |
| ses-send-email | {system}-ses-send-email-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portal-auth/iam.tf:176 |
| lambda-edge-execution-role | {system}-lambda-edge-execution-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/portal-auth/iam.tf:258 |
| lambda-edge-secrets-logs | {system}-lambda-edge-secrets-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portal-auth/iam.tf:287 |
| lambda-edge-ownership-map-read | {system}-lambda-edge-ownership-map-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portal-auth/iam.tf:323 |
| lambda-edge-sns-alert | {system}-lambda-edge-sns-alert-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portal-auth/iam.tf:354 |
| auth-validator-edge | {system}-auth-validator-edge-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/portal-auth/lambda-edge.tf:84 |
| /aws/lambda/auth-validator-edge | /aws/lambda/{system}-auth-validator-edge-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/portal-auth/lambda-edge.tf:129 |
| public-data-router | {system}-public-data-router-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/portal-auth/lambda-edge.tf:204 |
| /aws/lambda/public-data-router | /aws/lambda/{system}-public-data-router-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/portal-auth/lambda-edge.tf:248 |
| shared-advisor-router | {system}-shared-advisor-router-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/portal-auth/lambda-edge.tf:268 |
| /aws/lambda/shared-advisor-router | /aws/lambda/{system}-shared-advisor-router-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/portal-auth/lambda-edge.tf:295 |
| shared-advisor-router-response | {system}-shared-advisor-router-response-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/portal-auth/lambda-edge.tf:318 |
| /aws/lambda/shared-advisor-router-response | /aws/lambda/{system}-shared-advisor-router-response-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/portal-auth/lambda-edge.tf:345 |
| opalinvest-auth-handler | {system}-opalinvest-auth-handler-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/portal-auth/lambdas.tf:12 |
| /aws/lambda/opalinvest-auth-handler | /aws/lambda/{system}-opalinvest-auth-handler-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/portal-auth/lambdas.tf:50 |
| opal-portal-authorizer | opal-portal-authorizer-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/portal-auth/lambdas.tf:71 |
| /aws/lambda/opal-portal-authorizer | /aws/lambda/opal-portal-authorizer-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/portal-auth/lambdas.tf:90 |
| opalinvest/admin-seed | {system}/opalinvest/admin-seed | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/portal-auth/secrets-opalinvest.tf:14 |
| opalinvest/jwt-secret | {system}/opalinvest/jwt-secret | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/portal-auth/secrets-opalinvest.tf:26 |
| opal/auth/jwt-private-key | opal/auth/jwt-private-key | CONFORMANT | SECRET | repo | infra/aws/terraform/portal-auth/secrets.tf:14 |
| opal/auth/jwt-public-key | opal/auth/jwt-public-key | CONFORMANT | SECRET | repo | infra/aws/terraform/portal-auth/secrets.tf:24 |
| opal/auth/origin-verify | opal/auth/origin-verify | CONFORMANT | SECRET | repo | infra/aws/terraform/portal-auth/secrets.tf:77 |
| opal-session-analytics | opal-session-analytics-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/portal-auth/session-analytics.tf:65 |
| sms-send-text-message | {system}-sms-send-text-message-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portal-auth/sms-iam.tf:50 |
| aws-waf-logs-opal-cloudfront |  | NOT-GRADED | LOG_GROUP | repo | infra/aws/terraform/portal-auth/waf-cloudfront.tf:279 |
| opal-portal-content | opal-portal-content-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/portal-content/main.tf:54 |
| opal-portal-content-api-role | opal-portal-content-api-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/portal-content/main.tf:74 |
| opal-portal-content-table-rw | opal-portal-content-table-rw-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portal-content/main.tf:91 |
| portfolio-export-lambda-role | {system}-portfolio-export-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/portfolio-management/main.tf:226 |
| portfolio-export-dynamodb | {system}-portfolio-export-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portfolio-management/main.tf:249 |
| portfolio-export-s3 | {system}-portfolio-export-s3-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portfolio-management/main.tf:290 |
| OpalDataPMCacheBustAccess | opal-data-pm-cache-bust-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/portfolio-management/main.tf:322 |
| opal-pm-snapshots | opal-pm-snapshots-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/portfolio-management/main.tf:341 |
| opal-portal-api | opal-portal-api | CONFORMANT | API_GW | repo | infra/aws/terraform/portfolio-management/rest-api.tf:44 |
| opal-portal-rest-authorizer | opal-portal-rest-authorizer-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/portfolio-management/rest-authorizer.tf:49 |
| /aws/lambda/opal-portal-rest-authorizer | /aws/lambda/opal-portal-rest-authorizer-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/portfolio-management/rest-authorizer.tf:68 |
| access-anomaly-scanner-schedule | {system}-access-anomaly-scanner-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/security-ops/events.tf:7 |
| cost-anomaly-scanner-schedule | {system}-cost-anomaly-scanner-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/security-ops/events.tf:31 |
| lambda-access-anomaly-scanner-role | {system}-lambda-access-anomaly-scanner-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/security-ops/iam.tf:19 |
| AccessAnomalyScannerPolicy | {system}-access-anomaly-scanner-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/security-ops/iam.tf:29 |
| lambda-cost-anomaly-scanner-role | {system}-lambda-cost-anomaly-scanner-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/security-ops/iam.tf:64 |
| CostAnomalyScannerPolicy | {system}-cost-anomaly-scanner-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/security-ops/iam.tf:74 |
| access-anomaly-scanner | {system}-access-anomaly-scanner-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/security-ops/lambdas.tf:10 |
| /aws/lambda/access-anomaly-scanner | /aws/lambda/{system}-access-anomaly-scanner-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/security-ops/lambdas.tf:28 |
| cost-anomaly-scanner | {system}-cost-anomaly-scanner-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/security-ops/lambdas.tf:36 |
| /aws/lambda/cost-anomaly-scanner | /aws/lambda/{system}-cost-anomaly-scanner-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/security-ops/lambdas.tf:53 |
| schwab-anonymizer | schwab-anonymizer-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/security-ops/schwab-anonymizer.tf:19 |
| schwab-anonymizer-lambda-role | schwab-anonymizer-lambda-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/security-ops/schwab-anonymizer.tf:36 |
| SchwabAnonymizerPolicy | schwab-anonymizer-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/security-ops/schwab-anonymizer.tf:42 |
| sscn-s3-access | {system}-sscn-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/security-scanner-pipeline/iam.tf:27 |
| sscn-cloudwatch-logs | {system}-sscn-cloudwatch-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/security-scanner-pipeline/iam.tf:62 |
| security-scanner-deps | {system}-security-scanner-deps-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/security-scanner-pipeline/lambdas.tf:20 |
| opal-security-scanner-processor | opal-security-scanner-processor-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/security-scanner-pipeline/lambdas.tf:47 |
| /aws/lambda/opal-security-scanner-processor | /aws/lambda/opal-security-scanner-processor-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/security-scanner-pipeline/lambdas.tf:70 |
| seeking-alpha-analysis-daily | seeking-alpha-analysis-daily | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/seeking-alpha/main.tf:115 |
| seeking-alpha-news-daily | seeking-alpha-news-daily | CONFORMANT | EVENT_RULE | repo | infra/aws/terraform/seeking-alpha/main.tf:210 |
| seeking-alpha-scraper-role | seeking-alpha-scraper-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/seeking-alpha/main.tf:240 |
| SeekingAlphaScraperPolicy | seeking-alpha-scraper-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/seeking-alpha/main.tf:260 |
| /aws/lambda/seeking-alpha-analysis-coordinator | /aws/lambda/seeking-alpha-analysis-coordinator-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/seeking-alpha/main.tf:312 |
| /aws/lambda/seeking-alpha-analysis-listing-parser | /aws/lambda/seeking-alpha-analysis-listing-parser-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/seeking-alpha/main.tf:318 |
| /aws/lambda/seeking-alpha-analysis-dedup | /aws/lambda/seeking-alpha-analysis-dedup-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/seeking-alpha/main.tf:324 |
| /aws/lambda/seeking-alpha-analysis-scraper | /aws/lambda/seeking-alpha-analysis-scraper-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/seeking-alpha/main.tf:330 |
| /aws/lambda/seeking-alpha-news-coordinator | /aws/lambda/seeking-alpha-news-coordinator-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/seeking-alpha/main.tf:336 |
| /aws/lambda/seeking-alpha-news-dedup | /aws/lambda/seeking-alpha-news-dedup-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/seeking-alpha/main.tf:342 |
| /aws/lambda/seeking-alpha-news-scraper | /aws/lambda/seeking-alpha-news-scraper-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/seeking-alpha/main.tf:348 |
| cross-firm-bucket-deny | {system}-cross-firm-bucket-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/served-guard-inf/_root.tf:79 |
| opal-portal-data-proxy-api | opal-portal-data-proxy-api | CONFORMANT | API_GW | repo | infra/aws/terraform/shared-infra/apigateway-portal/main.tf:19 |
| cmtque-worker-down | cmtque-worker-down-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/shared-infra/cmtque-alarms.tf:33 |
| cmtque-dlq-depth | cmtque-dlq-depth-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/shared-infra/cmtque-alarms.tf:60 |
| cmtque-queue-backlog | cmtque-queue-backlog-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/shared-infra/cmtque-alarms.tf:86 |
| cmtque-commit-latency-high | cmtque-commit-latency-high-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/shared-infra/cmtque-alarms.tf:112 |
| cross-firm-secret-deny | {system}-cross-firm-secret-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/cross-firm-secret-deny.tf:45 |
| opal-cur-313476888478 | opal-313476888478-cur | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/shared-infra/cur.tf:17 |
| demo-transform-runner-ec2-role | advi-demo-transform-runner-ec2-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/shared-infra/demo-transform.tf:33 |
| demo-transform-runner-s3-scoped | {system}-demo-transform-runner-s3-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/demo-transform.tf:76 |
| demo-transform-runner-ec2-profile | {system}-demo-transform-runner-ec2-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/terraform/shared-infra/demo-transform.tf:185 |
| opal-drift-producer-codebuild-role | opal-drift-producer-codebuild-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/shared-infra/drift-producer.tf:35 |
| DriftProducerWritesAndDataDeny | {system}-drift-producer-writes-and-data-deny-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/drift-producer.tf:57 |
| opal-drift-producer-gha-role | opal-drift-producer-gha-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/shared-infra/drift-producer.tf:129 |
| DriftProducerCompPutAndSourceZip | {system}-drift-producer-comp-put-and-source-zip-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/drift-producer.tf:147 |
| opal-drift-producer | opal-drift-producer-build | OUT-OF-PATTERN | CODEBUILD_PROJECT | repo | infra/aws/terraform/shared-infra/drift-producer.tf:173 |
| opal-drift-producer-events-role | opal-drift-producer-events-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/shared-infra/drift-producer.tf:219 |
| StartDriftProducerBuild | {system}-start-drift-producer-build-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/drift-producer.tf:231 |
| opal-drift-producer-nightly | opal-drift-producer-nightly-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/shared-infra/drift-producer.tf:244 |
| opal-portal-market-data | opal-portal-market-data-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/shared-infra/dynamo-market-data-import.tf:22 |
| opal-users-v2 | opal-users-v2-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/shared-infra/dynamo.tf:27 |
| opal-pii-lookup | opal-pii-lookup-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/shared-infra/dynamo.tf:121 |
| etfs-avgcap-reader-role | etfs-avgcap-reader-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/shared-infra/etfs-aggregation-iam.tf:20 |
| s3-etfs-read | etfs-s3-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/etfs-aggregation-iam.tf:41 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/etfs-aggregation-iam.tf:75 |
| etf-ownership-dashboard-role | etfs-etf-ownership-dashboard-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/shared-infra/etfs-presentation.tf:27 |
| s3-etfs-presentation | etfs-s3-presentation-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/etfs-presentation.tf:47 |
| ses-send-noreply | {system}-ses-send-noreply-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/etfs-presentation.tf:110 |
| cloudwatch-metrics | {system}-cloudwatch-metrics-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/etfs-presentation.tf:130 |
| etf-ownership-dashboard-daily | {system}-etf-ownership-dashboard-daily | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/shared-infra/etfs-presentation.tf:178 |
| github-actions-opal-deploy | {system}-github-actions-opal-deploy-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/shared-infra/github-actions-opal-deploy.tf:22 |
| ec2-ssm-deploy | {system}-ec2-ssm-deploy-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/github-actions-opal-deploy.tf:51 |
| lambda-deploy | {system}-lambda-deploy-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/github-actions-opal-deploy.tf:78 |
| ec2-ssm-role | {system}-ec2-ssm-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/shared-infra/iam_legacy.tf:17 |
| infrastructure-ops-lambda-role | {system}-infrastructure-ops-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/shared-infra/iam_legacy.tf:42 |
| infrastructure-ops-permissions | {system}-infrastructure-ops-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/iam_legacy.tf:62 |
| infrastructure-snapshot-role | {system}-infrastructure-snapshot-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/shared-infra/iam_legacy.tf:91 |
| InfrastructureSnapshotPolicy | {system}-infrastructure-snapshot-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/iam_legacy.tf:106 |
| opal-infrastructure-monitor | opal-infrastructure-monitor-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/shared-infra/infra-monitor.tf:39 |
| MonitorAnthropicSecretRead | {system}-monitor-anthropic-secret-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/infra-monitor.tf:64 |
| MonitorLogsRead | {system}-monitor-logs-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/infra-monitor.tf:87 |
| MonitorDataFreshnessRead | {system}-monitor-data-freshness-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/infra-monitor.tf:135 |
| MonitorSnsEgressRead | {system}-monitor-sns-egress-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/infra-monitor.tf:208 |
| MonitorGraphHeadContractRead | {system}-monitor-graph-head-contract-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/infra-monitor.tf:241 |
| infrastructure-daily-snapshot | {system}-infrastructure-daily-snapshot-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/shared-infra/infra-snapshot.tf:30 |
| lambda-execution-role | {system}-lambda-execution-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:47 |
| BDPipelinePermissions | {system}-49f-pipeline-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:86 |
| FargateTriggerPermissions | {system}-fargate-trigger-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:124 |
| LambdaSelfInvoke | {system}-lambda-self-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:147 |
| OpalAuthSecretsAccess | opal-auth-secrets-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:204 |
| OpalDataPMAccess | opal-data-pm-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:226 |
| OpalDataPMUploadAccess | opal-data-pm-upload-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:250 |
| OpalPMDynamoDBAccess | opal-pm-dynamo-db-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:273 |
| PortfolioExportPolicy | {system}-portfolio-export-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:300 |
| S3Access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:356 |
| SeekingAlpha-S3-Access | seeking-alpha-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:381 |
| SeekingAlpha-SecretsAccess | seeking-alpha-secrets-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:406 |
| SemanticLayer3CurationAccess | {system}-semantic-layer3-curation-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:426 |
| SemanticTrendingPublisherS3Access | {system}-semantic-trending-publisher-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/lambda-execution-role.tf:462 |
| pandas-pyarrow-requests-layer | {system}-pandas-pyarrow-requests-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/terraform/shared-infra/layers.tf:24 |
| opal-runner-shared | opal-313476888478-runner-shared | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/shared-infra/main.tf:158 |
| PartnerIdentityReadPermissions | {system}-partner-identity-read-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/main.tf:262 |
| bd-securities | {system}-49f-securities-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/shared-infra/main.tf:362 |
| bd-securities-access | {system}-49f-securities-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/main.tf:395 |
| opal-portal-lambda-role | opal-portal-lambda-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:36 |
| SecretsManagerAccess | {system}-secretsmanager-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:55 |
| lambda-invoke-finbert | {system}-lambda-invoke-finbert-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:89 |
| opal-bedrock-invoke | opal-bedrock-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:107 |
| opal-cloudfront-invalidation | opal-cloudfront-invalidation-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:130 |
| opal-infrastructure-monitor | opal-infrastructure-monitor-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:149 |
| opal-portal-dynamodb | opal-portal-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:229 |
| opal-portal-logs | opal-portal-logs-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:272 |
| opal-portal-secrets | opal-portal-secrets-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:294 |
| opal-sessions-dynamodb | opal-sessions-dynamodb-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:317 |
| opal-sessions-secrets | opal-sessions-secrets-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:348 |
| opal-portal-s3-read | opal-portal-s3-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/opal-portal-lambda-role.tf:387 |
| partner-etl-ops-sqs-consumer-role | {system}-partner-etl-ops-sqs-consumer-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/shared-infra/partner-etl-ops-sqs-consumer.tf:57 |
| PartnerEtlOpsConsumerPolicy | {system}-partner-etl-ops-consumer-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/partner-etl-ops-sqs-consumer.tf:71 |
| partner-etl-ops-sqs-consumer | {system}-partner-etl-ops-sqs-consumer-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/shared-infra/partner-etl-ops-sqs-consumer.tf:108 |
| opal-data-49financial | opal-data-49financial | CONFORMANT | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3-49financial.tf:26 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3-portal-v2-import.tf:22 |
| opalinvest-portal | opal-313476888478-opalinvest-portal | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3.tf:11 |
| opal-cloudtrail-logs-313476888478 | opal-313476888478-cloudtrail-logs | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3.tf:47 |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3.tf:101 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3.tf:135 |
| opal-data-demo | opal-data-demo | CONFORMANT | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3.tf:221 |
| opal-313476888478-globgrph | opal-313476888478-globgrph | CONFORMANT | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3.tf:313 |
| opal-infrastructure-snapshots | opal-313476888478-infrastructure-snapshots | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/terraform/shared-infra/s3.tf:396 |
| FredApiKey | fred/api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:15 |
| aaii/credentials | {system}/aaii/credentials | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:25 |
| ai/claude-api-key | {system}/ai/claude-api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:36 |
| anthropic-api-key | {system}/anthropic-api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:47 |
| conferenceboard/credentials | {system}/conferenceboard/credentials | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:57 |
| find-dualbiz/bright-data/serp | {system}/find-dualbiz/bright-data/serp | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:68 |
| github-token | {system}/github-token | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:79 |
| google-cse-config | {system}/google-cse-config | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:89 |
| massive-api-key | {system}/massive-api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:99 |
| msci-api-credentials | msci/api-credentials | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:110 |
| multi-threadv2 | {system}/multi-threadv2 | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:121 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:133 |
| opal/finbert/config | opal/finbert/config | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:143 |
| opal/mcp/ms-ingest-token | opal/mcp/ms-ingest-token | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:153 |
| opal/openai/andrew-fideles | opal/openai/andrew-fideles | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:164 |
| opal/openai/aws-lambda-ki | opal/openai/aws-lambda-ki | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:174 |
| opal/openai/market-update | opal/openai/market-update | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:184 |
| opal/portal/config | opal/portal/config | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:194 |
| opal/pseudonym/49financial | opal/49f/pseudonym | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:206 |
| opal/pseudonym/opal-capital | opal/pseudonym/opal-capital | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:217 |
| opal/smartx/config | smartx/config | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:228 |
| opal/smartx/qa-models | smartx/qa-models | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:238 |
| openai-api-key | {system}/openai-api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:248 |
| seeking-alpha/bright-data-api-key | seeking-alpha/bright-data-api-key | CONFORMANT | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:261 |
| twilio/credentials | {system}/twilio/credentials | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:274 |
| twilio/recovery-code | {system}/twilio/recovery-code | OUT-OF-PATTERN | SECRET | repo | infra/aws/terraform/shared-infra/secrets-unowned.tf:286 |
| opal-surface-check-publish-gha-role | opal-surface-check-publish-gha-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/shared-infra/surface-check-gate.tf:27 |
| SurfaceCheckArtifactPut | {system}-surface-check-artifact-put-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/shared-infra/surface-check-gate.tf:47 |
| smartx/cookie/current | smartx/cookie/current | CONFORMANT | SECRET | repo | infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf:34 |
| smartx/credentials/yaliu-bundle | smartx/credentials/yaliu-bundle | CONFORMANT | SECRET | repo | infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf:52 |
| smartx-assets-pull-role | smartx-assets-pull-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf:67 |
| smartx-assets-pull-access | smartx-assets-pull-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/assets-pull-iam.tf:84 |
| smartx-assets-daily-pull | smartx-assets-daily-pull-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/smartx-pipeline/assets-pull-lambda.tf:35 |
| /aws/lambda/smartx-assets-daily-pull | /aws/lambda/smartx-assets-daily-pull-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/smartx-pipeline/assets-pull-lambda.tf:72 |
| smartx-assets-pull-scheduler-role | smartx-assets-pull-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/smartx-pipeline/assets-pull-lambda.tf:85 |
| invoke-smartx-assets-daily-pull | smartx-invoke-assets-daily-pull-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/assets-pull-lambda.tf:106 |
| smartx-assets-daily-pull-daily | smartx-assets-daily-pull-daily | CONFORMANT | SCHEDULE | repo | infra/aws/terraform/smartx-pipeline/assets-pull-lambda.tf:125 |
| smartx-assets-pull-invoke-silver-converter | smartx-assets-pull-invoke-silver-converter-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/assets-pull-onsuccess.tf:54 |
| smartx-exporter | smartx-exporter-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/smartx-pipeline/ec2.tf:6 |
| smartx-ingestion-lambda-role | smartx-ingestion-lambda-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/smartx-pipeline/iam.tf:20 |
| smartx-s3-access | smartx-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/iam.tf:36 |
| smartx-dynamodb-access | smartx-dynamodb-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/iam.tf:78 |
| s3-access | {system}-s3-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/iam.tf:135 |
| ecr-access | {system}-ecr-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/iam.tf:186 |
| secrets-access | {system}-secrets-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/iam.tf:213 |
| self-shutdown | {system}-self-shutdown-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/iam.tf:248 |
| lambda-invoke | {system}-lambda-invoke-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/iam.tf:270 |
| opal-smartx-ingestion-pipeline | smartx-ingestion-pipeline-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/smartx-pipeline/lambdas.tf:19 |
| /aws/lambda/opal-smartx-ingestion-pipeline | /aws/lambda/smartx-ingestion-pipeline-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/smartx-pipeline/lambdas.tf:64 |
| smartx-jwt-refresher-role | smartx-jwt-refresher-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/smartx-pipeline/rest-pull-iam.tf:15 |
| smartx-jwt-refresher-access | smartx-jwt-refresher-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/rest-pull-iam.tf:31 |
| smartx-rest-pull-role | smartx-rest-pull-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/smartx-pipeline/rest-pull-iam.tf:71 |
| smartx-rest-pull-access | smartx-rest-pull-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/rest-pull-iam.tf:87 |
| smartx-rest-scheduler-role | smartx-rest-scheduler-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/smartx-pipeline/rest-pull-schedule.tf:18 |
| invoke-smartx-rest-lambdas | smartx-invoke-rest-lambdas-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/smartx-pipeline/rest-pull-schedule.tf:38 |
| smartx-jwt-refresher-daily | smartx-jwt-refresher-daily | CONFORMANT | SCHEDULE | repo | infra/aws/terraform/smartx-pipeline/rest-pull-schedule.tf:59 |
| smartx-rest-pull-daily | smartx-rest-pull-daily | CONFORMANT | SCHEDULE | repo | infra/aws/terraform/smartx-pipeline/rest-pull-schedule.tf:77 |
| smartx/jwt/current | smartx/jwt/current | CONFORMANT | SECRET | repo | infra/aws/terraform/smartx-pipeline/rest-pull.tf:19 |
| smartx-jwt-refresher | smartx-jwt-refresher-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/smartx-pipeline/rest-pull.tf:41 |
| /aws/lambda/smartx-jwt-refresher | /aws/lambda/smartx-jwt-refresher-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/smartx-pipeline/rest-pull.tf:65 |
| smartx-rest-pull | smartx-rest-pull-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/smartx-pipeline/rest-pull.tf:89 |
| /aws/lambda/smartx-rest-pull | /aws/lambda/smartx-rest-pull-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/smartx-pipeline/rest-pull.tf:113 |
| smartx/credentials/username | smartx/credentials/username | CONFORMANT | SECRET | repo | infra/aws/terraform/smartx-pipeline/secrets-credentials.tf:14 |
| smartx/credentials/password | smartx/credentials/password | CONFORMANT | SECRET | repo | infra/aws/terraform/smartx-pipeline/secrets-credentials.tf:27 |
| opal-tickets | opal-tickets-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/ticket-center/main.tf:47 |
| opal-ticket-api-role | opal-ticket-api-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/ticket-center/main.tf:81 |
| opal-tickets-table-rw | opal-tickets-table-rw-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/ticket-center/main.tf:107 |
| opal-ticket-api-ses-send | opal-ticket-api-ses-send-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/ticket-center/main.tf:215 |
| opal-users-v2-access | opal-users-v2-access-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/trade-pipeline/iam.tf:125 |
| opal-website-dlm-role | opal-website-dlm-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/website/dlm.tf:20 |
| opal-website-wp-role | opal-website-wp-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/website/iam.tf:15 |
| opal-website-s3-backup | opal-website-s3-backup-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/website/iam.tf:42 |
| opal-website-wp-profile | opal-website-wp-profile | CONFORMANT | INSTANCE_PROFILE | repo | infra/aws/terraform/website/iam.tf:48 |
| opal-website-ses-send | opal-website-ses-send-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/website/iam.tf:89 |
| patricia@thewhitelabelcreative.com |  | NOT-GRADED | IAM_USER | repo | infra/aws/terraform/website/iam_patricia.tf:20 |
| website-estate-admin | estate-website-admin-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/website/iam_patricia.tf:151 |
| opal-website-wp-sg | opal-website-wp-sg | CONFORMANT | SECURITY_GROUP | repo | infra/aws/terraform/website/main.tf:36 |
| opal-website-wp | opal-website-wp-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/terraform/website/main.tf:70 |
| etf-classifications | {system}-etf-classifications-table | OUT-OF-PATTERN | DYNAMODB_TABLE | repo | infra/aws/terraform/yang-pipeline/etf-classifications.tf:22 |
| yang-pipeline-lambda-role | yang-pipeline-lambda-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/yang-pipeline/iam.tf:5 |
| yang-pipeline-lambda-permissions | yang-pipeline-lambda-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/yang-pipeline/iam.tf:27 |
| yang-pipeline-sfn-role | yang-pipeline-sfn-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/yang-pipeline/iam.tf:180 |
| yang-pipeline-sfn-permissions | yang-pipeline-sfn-permissions-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/yang-pipeline/iam.tf:201 |
| opal-313476888478-yang-qa-scratch | opal-313476888478-yang-qa-scratch | CONFORMANT | S3_BUCKET | repo | infra/aws/terraform/yang-pipeline/qa-scratch.tf:10 |
| yang-qa-scratch-access-20260803 | yang-qa-scratch-access-20260803-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/yang-pipeline/qa-scratch.tf:45 |
| YangDataPipeline | yang-data-pipeline-sfn | OUT-OF-PATTERN | STATE_MACHINE | repo | infra/aws/terraform/yang-pipeline/stepfunctions.tf:9 |
| yang-varflag-check-role | yang-varflag-check-role | CONFORMANT | IAM_ROLE | repo | infra/aws/terraform/yang-pipeline/varflag.tf:17 |
| yang-varflag-check-scoped | yang-varflag-check-scoped-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/yang-pipeline/varflag.tf:38 |
| YChartsSessionEviction | ycharts-session-eviction-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/terraform/ycharts-pipeline/cloudwatch.tf:8 |
| ycharts-session-probe-schedule | ycharts-session-probe-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/ycharts-pipeline/eventbridge.tf:9 |
| ycharts-session-capture-schedule | ycharts-session-capture-schedule-{cadence} | OUT-OF-PATTERN | EVENT_RULE | repo | infra/aws/terraform/ycharts-pipeline/eventbridge.tf:45 |
| YChartsSessionProbeLambdaRole | ycharts-session-probe-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/ycharts-pipeline/iam.tf:8 |
| ycharts-session-read | ycharts-session-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/ycharts-pipeline/iam.tf:33 |
| ycharts-session-metric-write | ycharts-session-metric-write-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/ycharts-pipeline/iam.tf:50 |
| ycharts-probe-invoke-capture | ycharts-probe-invoke-capture-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/ycharts-pipeline/iam.tf:71 |
| YChartsSessionCaptureLambdaRole | ycharts-session-capture-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/ycharts-pipeline/iam.tf:99 |
| ycharts-capture-secrets | ycharts-capture-secrets-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/ycharts-pipeline/iam.tf:123 |
| ycharts-session-probe | ycharts-session-probe-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/ycharts-pipeline/lambdas.tf:21 |
| /aws/lambda/ycharts-session-probe | /aws/lambda/ycharts-session-probe-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/ycharts-pipeline/lambdas.tf:49 |
| ycharts-session-capture | ycharts-session-capture-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/ycharts-pipeline/lambdas.tf:72 |
| /aws/lambda/ycharts-session-capture | /aws/lambda/ycharts-session-capture-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/ycharts-pipeline/lambdas.tf:102 |
| ycharts-market-data-pull | ycharts-market-data-pull-lambda | OUT-OF-PATTERN | LAMBDA | repo | infra/aws/terraform/ycharts-pipeline/market-data-pull.tf:24 |
| /aws/lambda/ycharts-market-data-pull | /aws/lambda/ycharts-market-data-pull-lambda | OUT-OF-PATTERN | LOG_GROUP | repo | infra/aws/terraform/ycharts-pipeline/market-data-pull.tf:48 |
| YChartsMarketDataPullLambdaRole | ycharts-market-data-pull-lambda-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/terraform/ycharts-pipeline/market-data-pull.tf:70 |
| ycharts-market-data-pull-secrets-read | ycharts-market-data-pull-secrets-read-policy | OUT-OF-PATTERN | IAM_POLICY | repo | infra/aws/terraform/ycharts-pipeline/market-data-pull.tf:93 |
| ycharts/session/current | ycharts/session/current | CONFORMANT | SECRET | repo | infra/aws/terraform/ycharts-pipeline/secrets.tf:20 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | data/black_diamond/scripts/gold/lib/config.py:14 |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET | repo | data/cot/scripts/gold/lib/config.py:16 |
| opal/smartx/config | smartx/config | OUT-OF-PATTERN | SECRET | repo | data/smartx/scripts/config.py:19 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | data/smartx/scripts/config.py:20 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | data/smartx/scripts/config.py:208 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | data/smartx/scripts/config.py:112 |
| opal-code-smartx | opal-313476888478-code-smartx | OUT-OF-PATTERN | S3_BUCKET | repo | data/smartx/scripts/config.py:114 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/ec2/opal-gateway/app/config.py:101 |
| ycharts/credentials | ycharts/credentials | CONFORMANT | SECRET | repo | infra/aws/ec2/opal-gateway/app/config.py:231 |
| opal/smartx/config | smartx/config | OUT-OF-PATTERN | SECRET | repo | infra/aws/ec2/smartx-exporter/smartx-workspace/scripts/config.py:19 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/ec2/smartx-exporter/smartx-workspace/scripts/config.py:20 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/ec2/smartx-exporter/smartx-workspace/scripts/config.py:188 |
| opal-313476888478-lambda-artifacts | opal-313476888478-lambda-artifacts | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/astn-wsjft-orchestrator/lambda_function.py:61 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/backfill_49f_daily_from_monolith_rps.py:61 |
| schwab/08242234/silver/fact_rps | schwab/08242234/silver/fact_rps | CONFORMANT | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/backfill_49f_daily_from_monolith_rps.py:62 |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-49f-etf-ownership-daily/backfill_49f_daily_from_monolith_rps.py:64 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-49f-fees-runner/lambda_function.py:38 |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | repo | infra/aws/lambda/bd-pipeline/bd-49f-fees-runner/lambda_function.py:40 |
| code/bronze/cot_bronze_ingest.py | {source}/{scope}/code/bronze/cot_bronze_ingest.py | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-49f-fees-runner/lambda_function.py:43 |
| code/silver/convert_fees_to_silver.py | {source}/{scope}/code/silver/convert_fees_to_silver.py | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-49f-fees-runner/lambda_function.py:44 |
| silver/%s/ | {source}/{scope}/silver/%s/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-49f-freshness-probe/lambda_function.py:69 |
| bronze/ | {source}/{scope}/bronze/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-49f-freshness-probe/lambda_function.py:74 |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | repo | infra/aws/lambda/bd-pipeline/bd-49f-freshness-probe/lambda_function.py:55 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-49f-freshness-probe/lambda_function.py:57 |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | repo | infra/aws/lambda/bd-pipeline/bd-49f-keepalive/lambda_function.py:45 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-49f-runner/lambda_function.py:54 |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | repo | infra/aws/lambda/bd-pipeline/bd-49f-runner/lambda_function.py:56 |
| code/bronze/cot_bronze_ingest.py | {source}/{scope}/code/bronze/cot_bronze_ingest.py | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-49f-runner/lambda_function.py:59 |
| bd-49f-runner | blackdiamond-49f-runner | ALIAS | EC2_INSTANCE | repo | infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py:51 |
| bd-49f-fees-runner | blackdiamond-49f-fees-runner | ALIAS | EC2_INSTANCE | repo | infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py:52 |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | repo | infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py:76 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-49f-session-trigger/lambda_function.py:77 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-client-detail/lambda_function.py:25 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-gold-trigger/lambda_function.py:30 |
| gold/trigger-pending.json | {source}/{scope}/gold/trigger-pending.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-gold-trigger/lambda_function.py:31 |
| gold/trigger-mode.json | {source}/{scope}/gold/trigger-mode.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-gold-trigger/lambda_function.py:32 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-incrparity-trigger/incrparity_core.py:18 |
| gold/_parity | {source}/{scope}/gold/_parity | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-incrparity-trigger/incrparity_core.py:19 |
| gold/_parity_reports | {source}/{scope}/gold/_parity_reports | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-incrparity-trigger/incrparity_core.py:20 |
| gold/meta/incremental_promoted.json | {source}/{scope}/gold/meta/incremental_promoted.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-incrparity-trigger/incrparity_core.py:21 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:54 |
| silver/prices/canonical_prices.parquet | {source}/{scope}/silver/prices/canonical_prices.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:441 |
| silver/interpolated_prices.parquet | {source}/{scope}/silver/interpolated_prices.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:748 |
| silver/transactions/ | {source}/{scope}/silver/transactions/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:92 |
| silver/transactions/ | {source}/{scope}/silver/transactions/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function.py:713 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-price-update/lambda_function_v2.py:39 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/bd-silver-merge/lambda_function.py:40 |
| code/silver/merge-daily-incremental.py | {source}/{scope}/code/silver/merge-daily-incremental.py | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/bd-silver-merge/lambda_function.py:41 |
| gold/_state/load_flows/ | {source}/{scope}/gold/_state/load_flows/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd-pipeline/gldinc-ss4c-canary/lambda_function.py:42 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd-pipeline/gldinc-ss4c-canary/lambda_function.py:41 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/bd_transaction_consolidator/lambda_function.py:28 |
| silver/ | {source}/{scope}/silver/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/bd_transaction_consolidator/lambda_function.py:29 |
| opal-313476888478-terraform-state | opal-313476888478-terraform-state | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/ci/trigger-census.py:49 |
| ecs-task | {system}-ecs-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/lambda/ci/trigger-census.py:108 |
| ecs-task | {system}-ecs-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/lambda/ci/trigger-census.py:271 |
| ecs-task | {system}-ecs-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/lambda/ci/trigger-census.py:352 |
| ecs-task | {system}-ecs-task | OUT-OF-PATTERN | ECS_TASK_DEFINITION | repo | infra/aws/lambda/ci/trigger-census.py:222 |
| bd-gold-layer-runner | {system}-49f-gold-layer-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/lambda/cost-anomaly-scanner/lambda_function.py:25 |
| silver/%s/ | {source}/{scope}/silver/%s/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/cot-pipeline/bd-cot-freshness-probe/lambda_function.py:67 |
| blackdiamond/cot/session | blackdiamond/cot/session | CONFORMANT | SECRET | repo | infra/aws/lambda/cot-pipeline/bd-cot-freshness-probe/lambda_function.py:44 |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET | repo | infra/aws/lambda/cot-pipeline/bd-cot-freshness-probe/lambda_function.py:46 |
| platinum/firm/timeseries_overview.json | advi/{scope}/platinum/firm/timeseries_overview.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/cot-pipeline/bd-cot-freshness-probe/lambda_function.py:56 |
| blackdiamond/cot/session | blackdiamond/cot/session | CONFORMANT | SECRET | repo | infra/aws/lambda/cot-pipeline/bd-cot-keepalive/lambda_function.py:44 |
| blackdiamond/cot/session | blackdiamond/cot/session | CONFORMANT | SECRET | repo | infra/aws/lambda/cot-pipeline/cot-bd-session-trigger/lambda_function.py:35 |
| blackdiamond/cot/credentials | blackdiamond/cot/credentials | CONFORMANT | SECRET | repo | infra/aws/lambda/cot-pipeline/cot-bd-session-trigger/lambda_function.py:36 |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET | repo | infra/aws/lambda/cot-pipeline/cot-bd-session-trigger/lambda_function.py:37 |
| cot-rebalancer-runner | {system}-cot-rebalancer-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:59 |
| blackdiamond/cottonwood/ | blackdiamond/cottonwood/ | CONFORMANT | S3Key | repo | infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:68 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:62 |
| blackdiamond/cot/session | blackdiamond/cot/session | CONFORMANT | SECRET | repo | infra/aws/lambda/cot-pipeline/cot-rebalancer-runner/lambda_function.py:64 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/daily_agenda_generator/lambda_function.py:25 |
| github-token | {system}/github-token | OUT-OF-PATTERN | SECRET | repo | infra/aws/lambda/daily_agenda_generator/lambda_function.py:27 |
| github-token | {system}/github-token | OUT-OF-PATTERN | SECRET | repo | infra/aws/lambda/daily_agenda_generator/package/lambda_function.py:27 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/daily_sprint_generator/lambda_function.py:68 |
| estate-report/github-token | estate/report/github-token | OUT-OF-PATTERN | SECRET | repo | infra/aws/lambda/daily_sprint_generator/lambda_function.py:74 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/data_refresh/lambda_function.py:46 |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/etfs-pipeline/etf-ownership-dashboard/dashboard_compute.py:53 |
| platinum/etf_ownership_dashboard.json | {source}/{scope}/platinum/etf-ownership-dashboard.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/etfs-pipeline/etf-ownership-dashboard/dashboard_compute.py:56 |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/etfs-pipeline/etf-ownership-dashboard/lambda_function.py:36 |
| platinum/etf_ownership_dashboard.json | {source}/{scope}/platinum/etf-ownership-dashboard.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/etfs-pipeline/etf-ownership-dashboard/lambda_function.py:37 |
| pandas-pyarrow-requests-layer | {system}-pandas-pyarrow-requests-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/lambda/etfs-pipeline/etf-positioning-producer/build_package.py:188 |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/etfs-pipeline/etfs-canon-fanin/lambda_function.py:40 |
| silver/netassets | {source}/{scope}/silver/netassets | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py:133 |
| silver/netassets_daily.parquet | {source}/{scope}/silver/netassets_daily.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py:134 |
| silver/holdings | {source}/{scope}/silver/holdings | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py:135 |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/etfs-pipeline/etfs-netassets-daily/lambda_function.py:117 |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:49 |
| platinum/reports | {source}/{scope}/platinum/reports | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:50 |
| opal-313476888478-lambda-artifacts | opal-313476888478-lambda-artifacts | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py:53 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/exec-summary-generator/config.py:29 |
| platinum/advisors/ | advi/{scope}/platinum/advisors/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/exec-summary-generator/config.py:30 |
| platinum/leaderboards/ | {source}/{scope}/platinum/leaderboards/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/exec-summary-generator/config.py:31 |
| platinum/firm/leaderboard.json | advi/{scope}/platinum/firm/leaderboard.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/exec-summary-generator/exec_summary/template_library.py:63 |
| platinum/firm/leaderboard.prior_week.json | {source}/{scope}/platinum/firm/leaderboard.prior-week.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/exec-summary-generator/exec_summary/template_library.py:64 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/fred-data-ingestion/ingest_yield_curve_fred.py:56 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/fred-data-ingestion/lambda_fred_ingestion.py:33 |
| opal-market-update | opal-313476888478-market-update | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/fred-data-ingestion/lambda_fred_ingestion.py:257 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/fred-macro-ingestion/ingest_fred_macro.py:45 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/fred-macro-ingestion/ingest_fred_macro.py:47 |
| bd-exporter-profile | {system}-49f-exporter-profile | OUT-OF-PATTERN | INSTANCE_PROFILE | repo | infra/aws/lambda/historical-prices-scheduler/lambda_function.py:27 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-client-detail/lambda_function.py:9 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-gold-trigger/lambda_function.py:22 |
| gold/trigger-pending.json | {source}/{scope}/gold/trigger-pending.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-gold-trigger/lambda_function.py:23 |
| gold/meta/pipeline-complete.json | {source}/{scope}/gold/meta/pipeline-complete.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-gold-trigger/lambda_function.py:24 |
| gold/trigger-mode.json | {source}/{scope}/gold/trigger-mode.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-gold-trigger/lambda_function.py:25 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-otp-relay/lambda_function.py:48 |
| inf/otp-relay/token | {system}/inf/otp-relay/token | OUT-OF-PATTERN | SECRET | repo | infra/aws/lambda/inf-otp-relay/lambda_function.py:54 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/ci/verify_bronze_key_agreement.py:63 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/_orion_api_silver_lib.py:26 |
| silver/api_dims/ | {source}/{scope}/silver/api_dims/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/_orion_api_silver_lib.py:27 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/_orion_api_silver_lib.py:25 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/_orion_api_silver_lib.py:228 |
| silver/transactions/ | {source}/{scope}/silver/transactions/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/convert_orion_api_to_silver.py:87 |
| bronze/positions/(snap).parquet | {source}/{scope}/bronze/positions/{snap}.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/convert_orion_api_to_silver.py:729 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/convert_orion_api_to_silver.py:83 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/convert_orion_api_to_silver.py:446 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/convert_orion_api_to_silver.py:647 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/convert_orion_api_to_silver.py:706 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/convert_orion_api_to_silver.py:812 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/lambda_function.py:38 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/pull_inflection_new_portfolio.py:42 |
| bronze/orion-api/latest/accounts_roster.json | {source}/{scope}/bronze/orion-api/latest/accounts_roster.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/pull_inflection_new_portfolio.py:150 |
| bronze/orion-api/latest/accounts_roster_marker.json | {source}/{scope}/bronze/orion-api/latest/accounts_roster_marker.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/pull_inflection_new_portfolio.py:151 |
| bronze/orion-api/latest/accounts_roster.json | {source}/{scope}/bronze/orion-api/latest/accounts_roster.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/pull_inflection_new_portfolio.py:123 |
| bronze/orion-api/latest/accounts_roster_marker.json | {source}/{scope}/bronze/orion-api/latest/accounts_roster_marker.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/pull_inflection_new_portfolio.py:125 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/rate_limiter.py:36 |
| orion/rate_limit_state_(dim_name).json | orion/rate_limit_state_{dim_name}.json | CONFORMANT | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-accounts-v2-daily/rate_limiter.py:37 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/convert_assets_v2_to_silver.py:42 |
| bronze/assets/(snap).parquet | {source}/{scope}/bronze/assets/{snap}.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/convert_assets_v2_to_silver.py:43 |
| silver/assets_v2/(snap).parquet | {source}/{scope}/silver/assets_v2/{snap}.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/convert_assets_v2_to_silver.py:44 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/lambda_function.py:33 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/pull_inflection_assets_v2.py:71 |
| silver/api_dims/household_rep_mapping/ | {source}/{scope}/silver/api_dims/household_rep_mapping/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/pull_inflection_assets_v2.py:77 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/rate_limiter.py:36 |
| orion/rate_limit_state_(dim_name).json | orion/rate_limit_state_{dim_name}.json | CONFORMANT | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-assets-v2/rate_limiter.py:37 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-eclipse/lambda_function.py:53 |
| bronze/eclipse_qa | {source}/{scope}/bronze/eclipse_qa | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-eclipse/lambda_function.py:56 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/_orion_api_silver_lib.py:55 |
| silver/api_dims/ | {source}/{scope}/silver/api_dims/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/_orion_api_silver_lib.py:56 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/_orion_api_silver_lib.py:54 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/_orion_api_silver_lib.py:163 |
| silver/transactions/ | {source}/{scope}/silver/transactions/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/convert_orion_api_to_silver.py:80 |
| bronze/positions/(snap).parquet | {source}/{scope}/bronze/positions/{snap}.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/convert_orion_api_to_silver.py:651 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/convert_orion_api_to_silver.py:76 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/convert_orion_api_to_silver.py:434 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/convert_orion_api_to_silver.py:571 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/convert_orion_api_to_silver.py:629 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/convert_orion_api_to_silver.py:733 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/lambda_function.py:32 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/pull_inflection_positions_daily.py:65 |
| silver/api_dims/household_rep_mapping/ | {source}/{scope}/silver/api_dims/household_rep_mapping/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/pull_inflection_positions_daily.py:71 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/rate_limiter.py:36 |
| orion/rate_limit_state_(dim_name).json | orion/rate_limit_state_{dim_name}.json | CONFORMANT | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-positions/rate_limiter.py:37 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/_orion_api_silver_lib.py:55 |
| silver/api_dims/ | {source}/{scope}/silver/api_dims/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/_orion_api_silver_lib.py:56 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/_orion_api_silver_lib.py:54 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/_orion_api_silver_lib.py:163 |
| silver/transactions/ | {source}/{scope}/silver/transactions/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/convert_orion_api_to_silver.py:80 |
| bronze/positions/(snap).parquet | {source}/{scope}/bronze/positions/{snap}.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/convert_orion_api_to_silver.py:651 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/convert_orion_api_to_silver.py:76 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/convert_orion_api_to_silver.py:434 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/convert_orion_api_to_silver.py:571 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/convert_orion_api_to_silver.py:629 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/convert_orion_api_to_silver.py:733 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/lambda_function.py:35 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/pull_inflection_representatives.py:52 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/rate_limiter.py:36 |
| orion/rate_limit_state_(dim_name).json | orion/rate_limit_state_{dim_name}.json | CONFORMANT | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-reps/rate_limiter.py:37 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/_orion_api_silver_lib.py:25 |
| silver/api_dims/ | {source}/{scope}/silver/api_dims/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/_orion_api_silver_lib.py:26 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/_orion_api_silver_lib.py:24 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/_orion_api_silver_lib.py:133 |
| silver/transactions/ | {source}/{scope}/silver/transactions/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/convert_orion_api_to_silver.py:80 |
| bronze/positions/(snap).parquet | {source}/{scope}/bronze/positions/{snap}.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/convert_orion_api_to_silver.py:627 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/convert_orion_api_to_silver.py:76 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/convert_orion_api_to_silver.py:428 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/convert_orion_api_to_silver.py:547 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/convert_orion_api_to_silver.py:605 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/convert_orion_api_to_silver.py:709 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/lambda_function.py:77 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/pull_inflection_transactions_v2.py:69 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/pull_inflection_transactions_v2.py:75 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/rate_limiter.py:36 |
| orion/rate_limit_state_(dim_name).json | orion/rate_limit_state_{dim_name}.json | CONFORMANT | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-api-txn/rate_limiter.py:37 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-assets-trigger/lambda_function.py:23 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-billing-daily/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-billing-daily/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-billing-daily/lambda_function.py:36 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-billing-daily/orion_billing_dim.py:57 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-billing-daily/orion_billing_dim.py:67 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-bronze-complete-emitter/lambda_function.py:55 |
| bronze/orion-api | {source}/{scope}/bronze/orion-api | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-bronze-complete-emitter/lambda_function.py:56 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-bronze-trigger/lambda_function.py:27 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-gold-freshness-guard/lambda_function.py:41 |
| gold/meta/pipeline-complete.json | {source}/{scope}/gold/meta/pipeline-complete.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-gold-freshness-guard/lambda_function.py:42 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py:23 |
| gold/dispatch-lock.json | {source}/{scope}/gold/dispatch-lock.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-gold-trigger/lambda_function.py:24 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-jwt-trigger/lambda_function.py:30 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-jwt-trigger/lambda_function.py:36 |
| orion/eclipse_jwt/current | orion/eclipse-jwt/current | OUT-OF-PATTERN | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-jwt-trigger/lambda_function.py:37 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-nna-partition-checker/lambda_function.py:38 |
| platinum/firm/advisor_nna_canonical.json | advi/{scope}/platinum/firm/advisor_nna_canonical.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-nna-partition-checker/lambda_function.py:40 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-performance-daily/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-performance-daily/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-performance-daily/lambda_function.py:40 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-performance-daily/pull_inflection_performance_dim.py:56 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-performance-daily/pull_inflection_performance_dim.py:72 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/_orion_api_silver_lib.py:26 |
| silver/api_dims/ | {source}/{scope}/silver/api_dims/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/_orion_api_silver_lib.py:27 |
| inf-gold-layer-runner | {system}-inf-gold-layer-runner | OUT-OF-PATTERN | EC2_INSTANCE | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/_orion_api_silver_lib.py:528 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/_orion_api_silver_lib.py:25 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/_orion_api_silver_lib.py:256 |
| silver/transactions/ | {source}/{scope}/silver/transactions/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/convert_orion_api_to_silver.py:93 |
| bronze/positions/(snap).jsonl.gz | {source}/{scope}/bronze/positions/{snap}.jsonl.gz | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/convert_orion_api_to_silver.py:785 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/convert_orion_api_to_silver.py:89 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/convert_orion_api_to_silver.py:501 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/convert_orion_api_to_silver.py:702 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/convert_orion_api_to_silver.py:761 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/convert_orion_api_to_silver.py:907 |
| bronze/orion-api | {source}/{scope}/bronze/orion-api | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/lambda_function.py:54 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/lambda_function.py:53 |
| orion-api | orion-api | CONFORMANT | API_GW | repo | infra/aws/lambda/inf-pipeline/inf-silver-chain/lambda_function.py:124 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-tax-daily/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-tax-daily/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-tax-daily/lambda_function.py:36 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-tax-daily/orion_tax_dim.py:61 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-tax-daily/orion_tax_dim.py:76 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily/jwt_freshness.py:43 |
| orion/jwt/current | orion/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily/jwt_freshness.py:45 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily/lambda_function.py:33 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily/pull_unified_account_dim.py:65 |
| bronze/orion-api/ | {source}/{scope}/bronze/orion-api/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-pipeline/inf-unified-account-dim-daily/pull_unified_account_dim.py:76 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-portal-advisor-publisher/lambda_function.py:61 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-portal-advisor-publisher/lambda_function.py:62 |
| gold/canonical/ | {source}/{scope}/gold/canonical/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-portal-publisher/lambda_function.py:60 |
| gold/canonical/ | {source}/{scope}/gold/canonical/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-portal-publisher/lambda_function.py:61 |
| gold/timeseries/client_performance.parquet | {source}/{scope}/gold/timeseries/client_performance.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-portal-publisher/lambda_function.py:62 |
| gold/views/account_team.parquet | {source}/{scope}/gold/views/account_team.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-portal-publisher/lambda_function.py:64 |
| silver/aum_snapshot/ | {source}/{scope}/silver/aum_snapshot/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-portal-publisher/lambda_function.py:65 |
| silver/api_dims/household/ | {source}/{scope}/silver/api_dims/household/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-portal-publisher/lambda_function.py:66 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-portal-publisher/lambda_function.py:49 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-portal-publisher/lambda_function.py:50 |
| silver/_silver_complete/ | {source}/{scope}/silver/_silver_complete/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/inf-silver-aggregator/lambda_function.py:32 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/inf-silver-aggregator/lambda_function.py:30 |
| opal-infrastructure-snapshots | opal-313476888478-infrastructure-snapshots | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/infrastructure-daily-snapshot/lambda_function.py:34 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:96 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:107 |
| opal-313476888478-globgrph | opal-313476888478-globgrph | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:123 |
| anthropic-api-key | {system}/anthropic-api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:134 |
| opal-313476888478-lambda-artifacts | opal-313476888478-lambda-artifacts | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:791 |
| opal-login-abuse-alerts | opal-login-abuse-alerts | CONFORMANT | SNS_TOPIC | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:2055 |
| etfs-reports-alerts | etfs-reports-alerts | CONFORMANT | SNS_TOPIC | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:2063 |
| opal-critical-surface-alerts | opal-critical-surface-alerts | CONFORMANT | SNS_TOPIC | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:2073 |
| opal-infrastructure-alerts | opal-infrastructure-alerts | CONFORMANT | SNS_TOPIC | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:2078 |
| opal-partner-etl-ops-alerts | opal-partner-etl-ops-alerts | CONFORMANT | SNS_TOPIC | repo | infra/aws/lambda/infrastructure_monitor/lambda_function.py:2084 |
| platinum/(firm)/ownership_map.json | {source}/{scope}/platinum/{firm}/ownership-map.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/investor-reporting/_authz/loaders.py:32 |
| x-user-role | {system}-x-user-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/investor-reporting/_scope/resolve.py:92 |
| x-advisor-role | {system}-x-advisor-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/investor-reporting/_scope/resolve.py:96 |
| x-user-role | {system}-x-user-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/investor-reporting/_scope/resolve.py:171 |
| x-advisor-role | {system}-x-advisor-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/investor-reporting/_scope/resolve.py:172 |
| irpt-ycharts-runner | irpt-ycharts-runner | CONFORMANT | EC2_INSTANCE | repo | infra/aws/lambda/investor-reporting/export/dispatch.py:49 |
| opal-data-ycharts | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/investor-reporting/export/handler.py:62 |
| x-user-role | {system}-x-user-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/investor-reporting/holdings/resolve.py:92 |
| x-advisor-role | {system}-x-advisor-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/investor-reporting/holdings/resolve.py:96 |
| x-user-role | {system}-x-user-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/investor-reporting/holdings/resolve.py:171 |
| x-advisor-role | {system}-x-advisor-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/investor-reporting/holdings/resolve.py:172 |
| irpt/graph/app-registration | irpt/graph/app-registration | CONFORMANT | SECRET | repo | infra/aws/lambda/investor-reporting/intake/graph_client.py:54 |
| opal-data-ycharts | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/investor-reporting/intake/poller.py:62 |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | repo | infra/aws/lambda/investor-reporting/performance/tenants.py:88 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/investor-reporting/performance/tenants.py:89 |
| blackdiamond/49f/ | blackdiamond/49financial/ | ALIAS | S3Key | repo | infra/aws/lambda/investor-reporting/performance/tenants.py:89 |
| blackdiamond/cot/session | blackdiamond/cot/session | CONFORMANT | SECRET | repo | infra/aws/lambda/investor-reporting/performance/tenants.py:98 |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET | repo | infra/aws/lambda/investor-reporting/performance/tenants.py:99 |
| orion/credentials | orion/credentials | CONFORMANT | SECRET | repo | infra/aws/lambda/investor-reporting/performance/tenants.py:105 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/investor-reporting/performance/tenants.py:106 |
| orion/inflection/ | orion/inflection/ | CONFORMANT | S3Key | repo | infra/aws/lambda/investor-reporting/performance/tenants.py:106 |
| ycharts/session/current | ycharts/session/current | CONFORMANT | SECRET | repo | infra/aws/lambda/investor-reporting/ycharts/session/broker.py:62 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/keyword_drilldown_generator/lambda_function.py:38 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/keyword_intelligence_generator/lambda_function.py:43 |
| opal/openai/news-trending | opal/openai/news-trending | CONFORMANT | SECRET | repo | infra/aws/lambda/keyword_intelligence_generator/lambda_function.py:46 |
| opal/auth/jwt-public-key | opal/auth/jwt-public-key | CONFORMANT | SECRET | repo | infra/aws/lambda/lib/authkeys/jwtPublicKeys.mjs:57 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-accrual-trigger/lambda_function.py:39 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:47 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:52 |
| gold/meta/pipeline-complete.json | {source}/{scope}/gold/meta/pipeline-complete.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:53 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:54 |
| gold/canonical | {source}/{scope}/gold/canonical | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:102 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:163 |
| schwab/08242234/silver/fact_rps_s2 | schwab/08242234/silver/fact_rps_s2 | CONFORMANT | S3Key | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:165 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:172 |
| platinum/mdpf/aggregate_aua | mdpf/{scope}/platinum/aggregate_aua | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/mdpf-pipeline/mdpf-daily-trigger/lambda_function.py:173 |
| gold/eclipse/(d)/_meta/gold_complete.json | eclipse/{scope}/gold/{d}/_meta/gold_complete.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/mdpf-pipeline/mdpf-feeder-trigger/lambda_function.py:93 |
| schwab/silver/rps/date=(dc)/data.parquet | schwab/{scope}/silver/rps/date={dc}/data.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/mdpf-pipeline/mdpf-feeder-trigger/lambda_function.py:100 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-feeder-trigger/lambda_function.py:84 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-feeder-trigger/lambda_function.py:86 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-feeder-trigger/lambda_function.py:87 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/mdpf-freshness-checker/lambda_function.py:45 |
| platinum/mdpf/aggregate_aua_timeseries.json | mdpf/{scope}/platinum/aggregate-aua-timeseries.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/mdpf-pipeline/mdpf-freshness-checker/lambda_function.py:47 |
| mdpf-daily-runner | mdpf-daily-runner | CONFORMANT | EC2_INSTANCE | repo | infra/aws/lambda/mdpf-pipeline/mdpf-freshness-checker/lambda_function.py:51 |
| platinum/mdpf/aggregate_aua/ | mdpf/{scope}/platinum/aggregate_aua/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/mdpf-pipeline/mdpf-freshness-checker/lambda_function.py:59 |
| mdpf-gold-lambda | mdpf-gold-lambda | CONFORMANT | LAMBDA | repo | infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py:430 |
| pandas-pyarrow-requests-layer | {system}-pandas-pyarrow-requests-layer | OUT-OF-PATTERN | LAMBDA_LAYER | repo | infra/aws/lambda/mdpf-pipeline/mdpf-gold-lambda/build_package.py:438 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/wsb-49f-model-aua-daily/wsb_49f_smartx_model_aua.py:65 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/wsd-49f-partner-held-etf-daily/wsd_partner_held_etf.py:72 |
| schwab/silver/rps | schwab/{scope}/silver/rps | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/mdpf-pipeline/wsd-49f-partner-held-etf-daily/wsd_partner_held_etf.py:73 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/mdpf-pipeline/wsd-49f-partner-held-etf-daily/wsd_partner_held_etf.py:75 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/news_ingestion_scheduler/lambda_function.py:52 |
| openai-api-key | {system}/openai-api-key | OUT-OF-PATTERN | SECRET | repo | infra/aws/lambda/news_layer3_curation/lambda_function.py:57 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/news_trending_analysis/lambda_function.py:76 |
| opal/openai/news-trending | opal/openai/news-trending | CONFORMANT | SECRET | repo | infra/aws/lambda/news_trending_analysis/lambda_function.py:70 |
| blackdiamond/49f/bronze/ | blackdiamond/49financial/bronze/ | ALIAS | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py:73 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py:68 |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-daily-pull/lambda_function.py:70 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-dim-convert/bd49f_dim_conversion.py:63 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-dim-convert/bd49f_dim_conversion.py:77 |
| schwab/silver/account_xref | schwab/{scope}/silver/account_xref | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-dim-convert/bd49f_dim_conversion.py:78 |
| blackdiamond/49financial/bronze/ | blackdiamond/49financial/bronze/ | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/insurance_leg.py:56 |
| blackdiamond/49f/bronze/ | blackdiamond/49financial/bronze/ | ALIAS | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py:46 |
| blackdiamond/49f/silver/dim_account_xref/ | blackdiamond/49financial/silver/dim_account_xref/ | ALIAS | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py:47 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py:44 |
| blackdiamond/49f/session | blackdiamond/49f/session | CONFORMANT | SECRET | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/lambda_function.py:45 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/taxsma_registry.py:26 |
| blackdiamond/49f/silver/dim_account_xref/ | blackdiamond/49financial/silver/dim_account_xref/ | ALIAS | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/taxsma_resolver.py:35 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull/taxsma_resolver.py:36 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:56 |
| schwab/08242234/silver/fact_rps_s2 | schwab/08242234/silver/fact_rps_s2 | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:57 |
| orion/inflection/silver/fact_assets | orion/inflection/silver/fact_assets | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:61 |
| eclipse/inflection/silver/fact_portfolios_full | eclipse/inflection/silver/fact_portfolios_full | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:63 |
| blackdiamond/cottonwood/silver/fact_holdings | blackdiamond/cottonwood/silver/fact_holdings | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:64 |
| gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json | {source}/{scope}/gold/mdpf_revamp/cottonwood/aggregate_aua_timeseries.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/channel_sources.py:69 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py:66 |
| platinum/mdpf/aggregate_aua/ | mdpf/{scope}/platinum/aggregate_aua/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py:67 |
| opal-data-etfs | opal-data-etfs | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-daily-emitter/lambda_function.py:706 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:69 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:96 |
| bronze/ | {source}/{scope}/bronze/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:112 |
| orion/inflection/bronze/ | orion/inflection/bronze/ | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:113 |
| opal-data-inf | opal-data-inflection | ALIAS | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:117 |
| bronze/eclipse/ | eclipse/{scope}/bronze/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:119 |
| eclipse/inflection/bronze/ | eclipse/inflection/bronze/ | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:120 |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:124 |
| blackdiamond/cottonwood/bronze/ | blackdiamond/cottonwood/bronze/ | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:138 |
| opal-data-cot | opal-data-cottonwood | ALIAS | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:155 |
| code/bronze/templates/ | {source}/{scope}/code/bronze/templates/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-ingest-mirror/lambda_function.py:157 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py:77 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher/lambda_function.py:79 |
| blackdiamond/49financial/silver/fact_x/date=2026-08-25/data.parquet | blackdiamond/49financial/silver/fact_x/date=2026-08-25/data.parquet | CONFORMANT | S3Key | repo | infra/aws/lambda/opal-assets/opal-assets-silver-bd49finsurance/bd49f_insurance_conversion.py:896 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-bd49finsurance/silver_registry.py:46 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/mirror_conversion.py:71 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/rebalancer_conversion.py:45 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-blackdiamond/silver_registry.py:46 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/mirror_conversion.py:69 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-eclipse/silver_registry.py:35 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-etf/etf_conversion.py:69 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-etf/mirror_conversion.py:71 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-etf/silver_registry.py:35 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-orion/mirror_conversion.py:71 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-orion/silver_registry.py:35 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-schwab/schwab_runtime.py:35 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-schwab/silver_registry.py:46 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal-assets/opal-assets-silver-smartx/smartx_runtime.py:34 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/opal_security_scanner_processor/lambda_function.py:86 |
| unknown-topic | {system}-unknown-topic | OUT-OF-PATTERN | SNS_TOPIC | repo | infra/aws/lambda/partner-etl-ops-sqs-consumer/lambda_function.py:60 |
| unknown-alarm | {system}-unknown-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/lambda/partner-etl-ops-sqs-consumer/lambda_function.py:75 |
| test-alarm | {system}-test-alarm | OUT-OF-PATTERN | CW_ALARM | repo | infra/aws/lambda/partner-etl-ops-sqs-consumer/lambda_function.py:160 |
| opal/openai/news-trending | opal/openai/news-trending | CONFORMANT | SECRET | repo | infra/aws/lambda/portal_data_proxy/lambda_function.py:1360 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/portal_data_proxy/lambda_function.py:92 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/portfolio_autosave_get/lambda_function.py:36 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/portfolio_autosave_put/lambda_function.py:50 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/portfolio_excel_generator/lambda_function.py:52 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/portfolio_export_download/lambda_function.py:36 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/portfolio_optimization_autosave_put/lambda_function.py:50 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/portfolio_pickle_parser/lambda_function.py:47 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/portfolio_version_get/lambda_function.py:36 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/precompute_market_metrics/index.js:22 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/precompute_market_metrics/index.js:774 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/precompute_market_metrics/index.js:827 |
| opal-data-harvest | opal-data-harvest | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/research/pull_enqueue/lambda_function.py:32 |
| opal-data-schwab | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/schwab-anonymizer/schwab_anonymizer.py:323 |
| schwab/anonymization-key | schwab/anonymization-key | CONFORMANT | SECRET | repo | infra/aws/lambda/schwab-anonymizer/schwab_anonymizer.py:84 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/security-sweep-comprehensive/lambda_function.py:1525 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/security-sweep-comprehensive/lambda_function.py:1421 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/seeking-alpha-analysis-coordinator/lambda_function.py:179 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/seeking-alpha-analysis-listing-parser/lambda_function.py:141 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/seeking-alpha-analysis-scraper/lambda_function.py:125 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/seeking-alpha-news-coordinator/lambda_function.py:154 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/seeking-alpha-news-scraper/lambda_function.py:127 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/semantic-news-layer3-curation/lambda_function.py:49 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/semantic-trending-topics-portal-publisher/lambda_function.py:26 |
| opal-portal-api | opal-portal-api | CONFORMANT | API_GW | repo | infra/aws/lambda/shared/opal_auth/__init__.py:32 |
| opal/auth/jwt-public-key | opal/auth/jwt-public-key | CONFORMANT | SECRET | repo | infra/aws/lambda/shared/opal_auth/__init__.py:33 |
| smartx/credentials/username | smartx/credentials/username | CONFORMANT | SECRET | repo | infra/aws/lambda/smartx_assets_pull/auth_bundle.py:62 |
| smartx/credentials/password | smartx/credentials/password | CONFORMANT | SECRET | repo | infra/aws/lambda/smartx_assets_pull/auth_bundle.py:64 |
| smartx/jwt/current | smartx/jwt/current | CONFORMANT | SECRET | repo | infra/aws/lambda/smartx_assets_pull/auth_bundle.py:65 |
| smartx/cookie/current | smartx/cookie/current | CONFORMANT | SECRET | repo | infra/aws/lambda/smartx_assets_pull/auth_bundle.py:67 |
| opal-data-assets | opal-data-assets | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_assets_pull/lambda_function.py:44 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/aggregate_smartx_by_transaction_dates.py:43 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/aggregate_smartx_to_timeseries.py:45 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/append_new_dates_only.py:32 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/append_today_to_dynamodb.py:25 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/compute_account_distribution.py:66 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/compute_account_distribution.py:80 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/compute_account_distribution.py:85 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/compute_per_firm_account_distribution.py:56 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/compute_per_firm_account_distribution.py:58 |
| opal/smartx/config | smartx/config | OUT-OF-PATTERN | SECRET | repo | infra/aws/lambda/smartx_ingestion_pipeline/config.py:19 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/smartx_ingestion_pipeline/config.py:20 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/config.py:208 |
| opal-data-smartx | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/config.py:112 |
| opal-code-smartx | opal-313476888478-code-smartx | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/config.py:114 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/consolidate_smartx_to_parquet.py:40 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/forward_fill_missing_dates.py:36 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/generate_smartx_timeseries_and_metrics.py:51 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/generate_smartx_timeseries_and_metrics.py:55 |
| opal-data-mdpf | opal-data-mdpf | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/generate_smartx_timeseries_and_metrics.py:86 |
| platinum/mdpf/global/aggregate-aua-timeseries.json | mdpf/global/platinum/aggregate-aua-timeseries.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/smartx_ingestion_pipeline/generate_smartx_timeseries_and_metrics.py:487 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:32 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:123 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:57 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:65 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:77 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:186 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:238 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:262 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:287 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:314 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/lambda_function.py:315 |
| opal-data-smartx-v2 | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/precompute_views.py:38 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/smartx_ingestion_pipeline/precompute_views.py:43 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/smartx_jwt_refresher/lambda_function.py:40 |
| opal-data-smartx | opal-data-{scope} | OUT-OF-PATTERN | S3_BUCKET | repo | infra/aws/lambda/smartx_query/lambda_function.py:25 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/smartx_rest_pull/pull_smartx_models_rest.py:43 |
| smartx/bronze | smartx/{scope}/bronze | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/smartx_rest_pull/pull_smartx_models_rest.py:45 |
| opal-data-bd | opal-data-49financial | ALIAS | S3_BUCKET | repo | infra/aws/lambda/smartx_rest_pull/smartx_jwt_reader.py:38 |
| by-role | {system}-by-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/trade-pipeline/trade-dashboard-api/src/dashboard_api.py:353 |
| by-role | {system}-by-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/trade-pipeline/trade-submission-handler/src/submission_handler.py:28 |
| by-role | {system}-by-role | OUT-OF-PATTERN | IAM_ROLE | repo | infra/aws/lambda/trade-pipeline/trade-workflow-handler/src/workflow_handler.py:41 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/trending_image_generator/lambda_function.py:21 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/trending_image_selector/lambda_function.py:21 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/01_market_overview/lambdas/fear-greed-fetcher/lambda_function.py:34 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/01_market_overview/lambdas/market-overview-tiered-generator/lambda_function.py:55 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/01_market_overview/lambdas/market-regime-classifier/lambda_function.py:48 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/01_market_overview/lambdas/market-rsi-tiered-generator/lambda_function.py:40 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/01_market_overview/lambdas/trending-topics-portal-publisher/lambda_function.py:28 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/07_macroeconomics/lambdas/opal-portal-volatility-fetcher/lambda_function.py:39 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/v2_portal/07_macroeconomics/lambdas/opal-portal-volatility-fetcher/lambda_function.py:43 |
| platinum/firm/cumulative_chart.json | advi/{scope}/platinum/firm/cumulative_chart.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py:879 |
| gold/timeseries/holdings_lots/ | {source}/{scope}/gold/timeseries/holdings_lots/ | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py:1064 |
| gold/timeseries/nna_total.json | {source}/{scope}/gold/timeseries/nna_total.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py:628 |
| gold/timeseries/client_performance.parquet | {source}/{scope}/gold/timeseries/client_performance.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py:1142 |
| gold/timeseries/account_performance.parquet | {source}/{scope}/gold/timeseries/account_performance.parquet | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py:1149 |
| gold/artifacts/summary/header_metrics.json | {source}/{scope}/gold/artifacts/summary/header_metrics.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/v2_portal/partners/lambdas/opal-partners-data/lambda_function.py:983 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/canon/yang-canon-interlock/lambda_function.py:42 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/cma/yang-generate-cma/lambda_function.py:177 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/correlation/yang-generate-correlation/lambda_function.py:21 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/factor_tilts/yang-generate-factor-tilts/lambda_function.py:24 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/macroeconomics/yang-generate-macro-timeseries/lambda_function.py:20 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/macroeconomics/yang-generate-macro/lambda_function.py:22 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/orchestration/cleanup-uploads/lambda_function.py:16 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/orchestration/generate-manifest/lambda_function.py:30 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/orchestration/get-prior-metadata/lambda_function.py:17 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/orchestration/move-to-processed/lambda_function.py:17 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/orchestration/trigger/lambda_function.py:37 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/orchestration/validate-files/lambda_function.py:17 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/outputs/capture-output-versions/lambda_function.py:21 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/outputs/generate-latest/lambda_function.py:17 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/outputs/generate-volatility/lambda_function.py:22 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/v2_portal/yang_pipeline/outputs/generate-volatility/lambda_function.py:82 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/outputs/ingest-dynamodb/lambda_function.py:28 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/outputs/refresh-fred-cache/lambda_function.py:30 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/outputs/varflag-check/varflag_check.py:47 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/outputs/yang-time-machine/lambda_function.py:39 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-generate-etf-returns/lambda_function.py:23 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-generate-peer-performance/lambda_function.py:35 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/portfolios/yang-model-portfolio-benchmarks/lambda_function.py:46 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-allocation-summary/lambda_function.py:33 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-holdings-attribution/lambda_function.py:41 |
| platinum/mdpf/global/aum-metrics.json | mdpf/global/platinum/aum-metrics.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning/lambda_function.py:1440 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning/lambda_function.py:2674 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/positioning/yang-generate-positioning/lambda_function.py:1491 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py:49 |
| platinum/etfs/positioning_data.json | etfs/{scope}/platinum/positioning_data.json | OUT-OF-PATTERN | S3Key | repo | infra/aws/lambda/v2_portal/yang_pipeline/seed-etf-constituents.py:50 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/valuation/yang-generate-risk-premium/lambda_function.py:31 |
| opal-data-portal-v2 | opal-data-portal-v2 | CONFORMANT | S3_BUCKET | repo | infra/aws/lambda/v2_portal/yang_pipeline/valuation/yang-generate-valuation/lambda_function.py:22 |
| opal/external-apis | opal/external-apis | CONFORMANT | SECRET | repo | infra/aws/lambda/ycharts-market-data-pull/ws2_mp_benchmark_pull.py:89 |
| ycharts/credentials | ycharts/credentials | CONFORMANT | SECRET | repo | infra/aws/lambda/ycharts-market-data-pull/ycharts_client.py:39 |
| ycharts/session/current | ycharts/session/current | CONFORMANT | SECRET | repo | infra/aws/lambda/ycharts-session-probe/lambda_function.py:77 |
