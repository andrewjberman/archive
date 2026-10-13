# PLANINV -- COTTONWOOD: WHAT SERVES AND NOTIFIES, AND EVERY CONSUMER OF THE CROSSWALK (FB-k-4)

Record: PLANINV_COTTONWOOD_SERVING_CROSSWALK.json (same rows, full text). Read at 2026-10-13T22:06:36Z; live reads span 21:33Z to 22:06Z. Read-only: no write, no producer run, no deploy, no terraform. Scope: the Cottonwood serving and notifying surface and every consumer of the Cottonwood crosswalk input.

## Headline

- The Cottonwood crosswalk input is NOT in a legacy home. It lives at s3://opal-data-assets/commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/ (crosswalk.parquet, crosswalk.csv). The 20 crosswalk rows are the input object, the builder, 7 crosswalk consumers (6 read the parquet; rule-change-diff runs the builder locally) and 11 module importers; all are legacy_touch false.
- Cottonwood serving is split: the Lambda@Edge router resolves cottonwood to opal-data-cot (16 legacy rows), but IRPT holdings read opal-data-cottonwood (surprise ADVI_FIRMBKTS-D1-W79-S2). No Cottonwood scope inside opal-data-bd was found (surprise S1).
- bd-cot-freshness-probe exists in the repository only (surprise S3).

## Table (56 rows; legacy_touch true on 16)

| id | kind | name | legacy | reads | writes | claim |
|---|---|---|---|---|---|---|
| fn-opal-cot-value-parity | lambda | opal-cot-value-parity | Y | opal-data-cot:platinum/firm/header_metrics.json (measured); opal-data-cot:silver/holdings/<date>.parquet (measured) | - | measured |
| fn-opal-cot-served-guard | lambda | opal-cot-served-guard | Y | opal-data-cot:platinum/firm/header_metrics.json (measured); opal-data-cot:version list of the served key (measured) | opal-data-cot:platinum/firm/header_metrics.json (measured); opal-data-cot:_quarantine/served-guard/* (measured) | measured |
| fn-cot-bd-session-trigger | lambda | cot-bd-session-trigger | Y | - | opal-data-cot:blackdiamond/cot/session-trigger-mode.json (measured) | measured |
| fn-cot-rebalancer-runner | lambda | cot-rebalancer-runner | n | - | opal-data-assets:blackdiamond/cottonwood/bronze/* and meta/* (measured) | measured |
| fn-cot-satellites-registry-producer | lambda | cot-satellites-registry-producer | Y | opal-data-assets:blackdiamond/cottonwood/bronze/rebalancer_models/* and rebalancer_mode (measured); opal-data-assets:stamp prefix (measured) | opal-data-cot:platinum/satellites/registry.json (measured); opal-data-cot:platinum/satellites/holdings.json (measured) | measured |
| fn-cot-satellites-characteristics-producer | lambda | cot-satellites-characteristics-producer | Y | opal-data-cot:platinum/satellites/holdings.json (measured); opal-data-portal-v2:json/positioning/positioning_data.json (measured); opal-data-etfs:bbg/*/characteristics.parquet, bbg/*/run_manifest.json | opal-data-cot:platinum/satellites/characteristics.json (measured) | measured |
| fn-cot-etf-ownership-daily | lambda | cot-etf-ownership-daily | Y | opal-data-cot:gold/canonical/holdings/* (measured); opal-data-assets:blackdiamond/cottonwood/silver/fact_holdings/* (measured); opal-data-etfs:config/* and platinum/reports/*/etf_ownership.pdf (measur | opal-data-etfs:daily/cottonwood/* (measured) | measured |
| fn-bd-cot-keepalive | lambda | bd-cot-keepalive | n | - | - | measured |
| fn-bd-cot-freshness-probe | lambda | infra/aws/lambda/cot-pipeline/bd-cot-freshness-probe/lambda_function.py (repository only; no live function of  | Y | opal-data-cot:platinum/firm/timeseries_overview.json (measured) | - | measured |
| fn-irpt-directory-refresh | lambda | irpt-directory-refresh (role irpt-directory-refresh-role) | Y | opal-data-cot:investor-reporting/directory/* (measured) | opal-data-cot:investor-reporting/directory/_refresh/* (measured) | measured |
| fn-irpt-directory-search | lambda | irpt-directory-search (role irpt-directory-role) | Y | opal-data-cot:investor-reporting/directory/* (measured); opal-data-cot:platinum/cottonwood/ownership_map.json (measured) | - | measured |
| fn-irpt-holdings | lambda | irpt-holdings (role irpt-holdings-role) | Y | opal-data-cot:investor-reporting/directory/* and platinum/cottonwood/ownership_map.j (measured); opal-data-cottonwood:irpt/cottonwood/platinum/holdings/current/manifest.json and date=*/ ve (measured) | - | measured |
| fn-irpt-performance-adapter | lambda | irpt-performance-adapter (role irpt-performance-adapter-role) | Y | opal-data-cot:investor-reporting/directory/* (measured); opal-data-cot:platinum/cottonwood/ownership_map.json (measured); opal-data-cot:forwardfill_v2/ (inferred) | - | measured |
| edge-shared-advisor-router | edge | shared-advisor-router (Lambda@Edge, origin-request) | Y | opal-data-cot:platinum/advi/* (measured) | - | measured |
| edge-shared-advisor-router-response | edge | shared-advisor-router-response (Lambda@Edge, origin-response) | n | - | - | measured |
| edge-auth-validator-edge | edge | auth-validator-edge (Lambda@Edge, viewer-request) | n | - | - | measured |
| edge-cf-EVTSA9VEHNZVH-origin-cot | edge | CloudFront EVTSA9VEHNZVH origin S3-opal-data-cot (opal-data-cot.s3.us-east-1.amazonaws.com, no OAC) | Y | opal-data-cot:all keys, via the scoped advisor OAI in the bucket policy (measured) | - | measured |
| grant-opal-data-cot-bucket-policy | other | opal-data-cot bucket policy (resource grants) | Y | opal-data-cot:gold/* (measured) | - | measured |
| role-irpt-core-firm-cottonwood | role | irpt-core-firm-cottonwood (role; attached policy irpt-core-firm-cottonwood-prefix v1) | n | opal-data-ycharts:firms/cottonwood/* (measured) | - | measured |
| role-firmsep-cot-bucket-recovery-role | role | firmsep-cot-bucket-recovery-role (inline cottonwood-recovery-policy) | n | - | opal-data-cottonwood:bucket policy (measured) | measured |
| reader-portal-satelliteRegistry | reader | portal/src/api/endpoints/satelliteRegistry.ts | Y | opal-data-cot:platinum/satellites/registry.json, holdings.json, characteristics.json (measured) | - | measured |
| reader-portal-advisor-intelligence-endpoint | reader | portal/src/api/endpoints/advisor-intelligence.ts (firm bucket suffix map) | Y | opal-data-cot:advisor-intelligence artifacts in the firm bucket (measured) | - | measured |
| reader-portal-cottonwood-layout | reader | portal/src/pages/AdvisorIntelligence/_partners/cottonwood/layout.ts | n | - | - | measured |
| reader-portal-firmAccess | reader | portal/src/lib/firmAccess.ts | n | - | - | measured |
| topic-opal-critical-surface-alerts | topic | SNS opal-critical-surface-alerts | n | - | - | measured |
| topic-opal-bd-cot-cookie-alerts | topic | SNS opal-bd-cot-cookie-alerts | n | - | - | measured |
| email-ses-account-identities | email | SES account identities (us-east-1) | n | - | - | measured |
| rule-opal-cot-served-guard-on-write | rule | opal-cot-served-guard-on-write | n | - | - | measured |
| rule-opal-cot-value-parity-hourly | rule | opal-cot-value-parity-hourly | n | - | - | measured |
| rule-cot-bronze-complete | rule | cot-bronze-complete | n | - | - | measured |
| rule-cot-silver-complete | rule | cot-silver-complete | n | - | - | measured |
| rule-etfs-cot-satellites-registry-producer-stamp-gated-daily | rule | etfs-cot-satellites-registry-producer-stamp-gated-daily | n | - | - | measured |
| rule-cot-satellites-characteristics-producer-daily | rule | cot-satellites-characteristics-producer-daily | n | - | - | measured |
| rule-etfs-cot-satellites-characteristics-producer-reattempt-hourly | rule | etfs-cot-satellites-characteristics-producer-reattempt-hourly | n | - | - | measured |
| rule-cot-etf-ownership-daily-schedule | rule | cot-etf-ownership-daily-schedule | n | - | - | measured |
| notif-opal-data-cot-s3-config | other | S3 notification configuration of opal-data-cot | n | - | - | measured |
| xw-input-commonwealth-crosswalk | other | THE COTTONWOOD CROSSWALK INPUT: s3://opal-data-assets/commonwealth/cottonwood/silver/crosswalk/date=2026-06-23 | n | - | opal-data-assets:commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/ (measured) | measured |
| xw-builder-commonwealth-crosswalk-py | script | data/assets/scripts/silver/commonwealth_crosswalk.py (crosswalk builder) | n | - | opal-data-assets:commonwealth/cottonwood/silver/crosswalk/date=<d>/crosswalk.parquet an (measured) | measured |
| xw-consumer-commonwealth-fwd8-read | script | data/assets/scripts/analysis/commonwealth_fwd8_read.py (crosswalk consumer: FWD-8 read) | n | opal-data-assets:commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.par (measured) | - | measured |
| xw-consumer-commonwealth-coverage-statement | script | data/assets/scripts/analysis/commonwealth_coverage_statement.py (crosswalk consumer: coverage statement) | n | opal-data-assets:commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.par (measured) | - | measured |
| xw-consumer-commonwealth-near-match-page | script | data/assets/scripts/analysis/commonwealth_near_match_page.py (crosswalk consumer: near-match page) | n | opal-data-assets:commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.par (measured) | - | measured |
| xw-consumer-commonwealth-price-need | script | data/assets/scripts/silver/commonwealth_price_need.py (crosswalk consumer: price-need ranking) | n | opal-data-assets:commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.par (measured) | - | measured |
| xw-consumer-mdpf-demque-rank | script | data/mdpf/scripts/demque/rank.py (crosswalk consumer: MDPF demque ranking) | n | opal-data-assets:commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.par (measured) | - | measured |
| xw-consumer-amlp-read-2026-10-09 | reader | AMLP consumer read, ADVI_COTBKF 2026-10-09 (crosswalk consumer: one-off read) | n | opal-data-assets:commonwealth/cottonwood/silver/crosswalk/date=2026-06-23/crosswalk.par (measured) | - | measured |
| xw-consumer-commonwealth-rule-change-diff | script | data/assets/scripts/analysis/commonwealth_rule_change_diff.py (crosswalk consumer: before and after diff) | n | - | - | measured |
| xw-module-import-commonwealth-asf-source | script | data/assets/scripts/silver/commonwealth_asf_source.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-base-close-trace | script | data/assets/scripts/silver/commonwealth_base_close_trace.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-bond-custodian-price | script | data/assets/scripts/silver/commonwealth_bond_custodian_price.py (crosswalk consumer: imports the builder modul | n | - | - | measured |
| xw-module-import-commonwealth-daily-holdings | script | data/assets/scripts/silver/commonwealth_daily_holdings.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-daily-returns | script | data/assets/scripts/silver/commonwealth_daily_returns.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-daily-valuation | script | data/assets/scripts/silver/commonwealth_daily_valuation.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-mover-classes | script | data/assets/scripts/silver/commonwealth_mover_classes.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-mover-causes | script | data/assets/scripts/silver/commonwealth_mover_causes.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-non-positive-base | script | data/assets/scripts/silver/commonwealth_non_positive_base.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-split-level-probe | script | data/assets/scripts/silver/commonwealth_split_level_probe.py (crosswalk consumer: imports the builder module) | n | - | - | measured |
| xw-module-import-commonwealth-residuals-explain | script | data/assets/scripts/analysis/commonwealth_residuals_explain.py (crosswalk consumer: imports the builder module | n | - | - | measured |

## Denominators

- lambda_functions_listed_live: 237
- lambda_function_configs_read_live: 11
- lambda_distinct_roles_listed: 149
- iam_roles_listed: 18
- iam_inline_policy_documents_read: 38
- iam_managed_policy_versions_read: 1
- s3_bucket_policies_read: 1
- s3_bucket_notification_configs_read: 1
- eventbridge_rules_listed: 156
- eventbridge_rules_name_matched_cot_or_cottonwood: 11
- eventbridge_targets_read: 8
- eventbridge_rules_described: 2
- sns_topics_listed: 17
- sns_topics_name_matched: 2
- ses_identities_listed: 26
- ses_templates_listed: 0
- cloudfront_distributions_read: 1
- cloudfront_origins_read: 7
- cloudfront_cache_behaviors_read: 30
- edge_function_configs_read: 3
- repo_files_matched_opal_data_cot_infra: 128
- repo_files_matched_opal_data_cot_portal_src: 4
- repo_files_matched_opal_data_cot_data: 67
- repo_files_matched_crosswalk_key_data: 32
- repo_files_matched_crosswalk_key_infra: 2
- repo_files_matched_crosswalk_key_portal_src: 0
- repo_script_files_non_test_scanned_for_crosswalk_calls: 200
- aws_graph_nodes_scanned: 2926

## Not read

- the environment values of the other 226 live functions: only 11 configurations were read; their source was searched in the repository (infra/aws/lambda, 128 files for opal-data-cot), not their live environments
- invocation triggers of the IRPT functions (irpt-directory-refresh, irpt-directory-search, irpt-holdings, irpt-performance-adapter): the rules and callers were not identified; trigger fields say not determined
- EventBridge state and schedule expressions of opal-cot-value-parity-hourly and the schedule rules other than the two described; targets of cot-rebalancer-runner-daily not read
- SNS subscriptions of opal-critical-surface-alerts and opal-bd-cot-cookie-alerts (subscribers unknown)
- SES sending statistics and the 26 identities' use: only the identity and template listings were read; the addresses were not printed
- the forwardfill_v2 Cottonwood data-plane read in tenants.py: no role grant found among the inline policies of irpt-performance-adapter-role; whether any other role reads it was not checked
- the aws comp-find DEFAULT band enumeration for the crosswalk key timed out at 100 seconds (rc 124) and was not retried; the repository was read with the native Grep tool instead
- dim_identity_crosswalk (data/assets/scripts/gold/investor_reporting/directory_runner.py:339) is a different crosswalk (the investor-reporting identity dimension); its bucket was not traced and it is excluded from the Cottonwood crosswalk consumer list
- commonwealth_sweeps.py and commonwealth_signs.py name the crosswalk module in a docstring only (no import found); commonwealth_sweep_regrade.py reaches the module through dv.cw; neither is listed as a consumer
- consumers of the ADVI_COTBKF deliverables that cite the crosswalk (ACTIVE_SET_RECORD.json, REVERSE_MATCH.csv, RULE_CHANGE_DIFF.md, the signing tables): records, not code; not traced further
- CloudFront access logs, Lambda invocation metrics and any traffic to the origin: not read
- the opal-data-cot managed customer policy named in the graph (opal-data-cot#policy): not read live
- the ajb_workspace household_crosswalk builders (data/assets/scripts/gold/advi_billing/household_crosswalk.py and the 49financial household_crosswalk key): a different firm and a different crosswalk; excluded by scope
- PLANINV egress: none; no portal, Terraform or producer command was run

