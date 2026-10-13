# PLANINV FB-k-2 -- Inflection: what serves and notifies (read-only)

Read at 2026-10-13T22:13:25Z against HEAD 5760dbcc38db497aa878acf35ea4bf695b8c4f34. Full rows and evidence are in PLANINV_INFLECTION_SERVING.json.

Totals: 97 rows, 80 legacy_touch true, 17 legacy_touch false.

## Rows (id, kind, name, legacy_touch)

| id | kind | name | legacy_touch | claim |
|---|---|---|---|---|
| INF-FN-01 | lambda | inf-portal-publisher | true | measured |
| INF-FN-02 | lambda | inf-portal-advisor-publisher | true | measured |
| INF-FN-03 | lambda | inf-silver-aggregator | true | measured |
| INF-FN-04 | lambda | inf-gold-trigger | true | measured |
| INF-FN-05 | lambda | inf-silver-chain | true | measured |
| INF-FN-06 | lambda | inf-bronze-complete-emitter | true | measured |
| INF-FN-07 | lambda | inf-nna-partition-checker | true | measured |
| INF-FN-08 | lambda | inf-client-detail | false | measured |
| INF-FN-09 | lambda | inf-otp-relay | true | measured |
| INF-FN-10 | lambda | inf-api-eclipse | true | measured |
| INF-FN-11 | lambda | inf-api-positions | true | measured |
| INF-FN-12 | lambda | inf-api-reps | true | measured |
| INF-FN-13 | lambda | inf-api-txn | true | measured |
| INF-FN-14 | lambda | inf-api-assets-v2 | true | measured |
| INF-FN-15 | lambda | inf-accounts-v2-daily | true | measured |
| INF-FN-16 | lambda | inf-billing-daily | true | measured |
| INF-FN-17 | lambda | inf-performance-daily | true | measured |
| INF-FN-18 | lambda | inf-tax-daily | true | measured |
| INF-FN-19 | lambda | inf-unified-account-dim-daily | true | measured |
| INF-FN-20 | lambda | inf-etf-ownership-daily | true | measured |
| INF-FN-21 | lambda | inf-assets-trigger | false | measured |
| INF-FN-22 | lambda | inf-jwt-trigger | true | measured |
| INF-FN-23 | lambda | inf-bronze-trigger | true | measured |
| INF-FN-24 | lambda | mdpf-feeder-trigger | true | measured |
| INF-FN-25 | lambda | opal-inf-served-guard | true | measured |
| INF-FN-26 | lambda | opal-inf-value-parity | true | measured |
| INF-FN-27 | lambda | opal-assets-ingest-mirror | true | measured |
| INF-FN-28 | lambda | exec-summary-generator | false | measured |
| INF-FN-29 | lambda | irpt-directory-search | true | measured |
| INF-FN-30 | lambda | irpt-status | true | measured |
| INF-FN-31 | lambda | irpt-holdings | true | measured |
| INF-FN-32 | lambda | irpt-narrative | true | measured |
| INF-FN-33 | lambda | irpt-export-render | true | measured |
| INF-FN-34 | lambda | irpt-directory-refresh | true | measured |
| INF-FN-35 | lambda | irpt-performance-adapter | true | measured |
| INF-FN-36 | lambda | irpt-ycharts-generate | true | measured |
| INF-FN-37 | lambda | irpt-49f-reporting-read-lambda | false | measured |
| INF-FN-38 | lambda | irpt-holdings-refresh-lambda | false | measured |
| INF-FN-39 | lambda | irpt-inf-holdings-performance-lambda | false | measured |
| INF-EDGE-01 | edge | shared-advisor-router (Lambda@Edge, origin-request) | true | measured |
| INF-EDGE-02 | edge | shared-advisor-router-response (Lambda@Edge, origin-response) | true | measured |
| INF-EDGE-03 | edge | CloudFront distribution EVTSA9VEHNZVH (origin S3-opal-data-inf) | true | measured |
| INF-EDGE-04 | other | bucket policy of opal-data-inf | true | measured |
| INF-EDGE-05 | other | opal-data-inf bucket notification configuration (S3 to Lambda) | true | measured |
| INF-READER-01 | reader | portal/src/api/endpoints/advisor-intelligence.ts (nested portal worktree) | true | measured |
| INF-REPO-01 | other | infra/aws/lambda-edge/_shared/firm-config.mjs | false | measured |
| INF-RULE-01 | rule | mdpf-feeder-accelerator | true | measured |
| INF-RULE-02 | rule | exec-summary-trigger | false | measured |
| INF-RULE-03 | rule | inf-gold-dispatch-release-changed | false | measured |
| INF-RULE-04 | rule | inf-canonical-prices-daily, inf-gold-full-on-bronze-complete, inf-gold-incremental-daily | false | measured |
| INF-SNS-01 | topic | inf-otp-alert | false | measured |
| INF-SNS-02 | topic | inf-gold-dispatch-release-alarm | false | measured |
| INF-EMAIL-01 | email | SES identities naming the Inflection firm domain (2 individual addresses; addresses withheld) | false | measured |
| INF-ROLE-01 | role | bd-exporter-ec2-role | true | measured |
| INF-ROLE-02 | role | inf-accounts-v2-daily-role | true | measured |
| INF-ROLE-03 | role | inf-api-assets-v2-lambda-role | true | measured |
| INF-ROLE-04 | role | inf-api-eclipse-role | true | measured |
| INF-ROLE-05 | role | inf-api-positions-role | true | measured |
| INF-ROLE-06 | role | inf-api-reps-role | true | measured |
| INF-ROLE-07 | role | inf-api-txn-role | true | measured |
| INF-ROLE-08 | role | inf-billing-daily-role | true | measured |
| INF-ROLE-09 | role | inf-bronze-complete-emitter-role | true | measured |
| INF-ROLE-10 | role | inf-bronze-runner-ec2-role | true | measured |
| INF-ROLE-11 | role | inf-bronze-trigger-lambda-role | true | measured |
| INF-ROLE-12 | role | inf-etf-ownership-daily-role | true | measured |
| INF-ROLE-13 | role | inf-exporter-ec2-role | true | measured |
| INF-ROLE-14 | role | inf-gold-layer-ec2-role | true | measured |
| INF-ROLE-15 | role | inf-gold-layer-lambda-role | true | measured |
| INF-ROLE-16 | role | inf-gold-qa-runner-ec2-role | true | measured |
| INF-ROLE-17 | role | inf-gold-trigger-lambda-role | true | measured |
| INF-ROLE-18 | role | inf-jwt-trigger-lambda-role | true | measured |
| INF-ROLE-19 | role | inf-nna-partition-checker-lambda-role | true | measured |
| INF-ROLE-20 | role | inf-otp-relay-lambda-role | true | measured |
| INF-ROLE-21 | role | inf-performance-daily-role | true | measured |
| INF-ROLE-22 | role | inf-silver-aggregator-lambda-role | true | measured |
| INF-ROLE-23 | role | inf-silver-chain-lambda-role | true | measured |
| INF-ROLE-24 | role | inf-tax-daily-role | true | measured |
| INF-ROLE-25 | role | inf-unified-account-dim-daily-role | true | measured |
| INF-ROLE-26 | role | irpt-directory-refresh-role | true | measured |
| INF-ROLE-27 | role | irpt-directory-role | true | measured |
| INF-ROLE-28 | role | irpt-export-render-role | true | measured |
| INF-ROLE-29 | role | irpt-holdings-role | true | measured |
| INF-ROLE-30 | role | irpt-inf-holdings-role | true | measured |
| INF-ROLE-31 | role | irpt-narrative-role | true | measured |
| INF-ROLE-32 | role | irpt-performance-adapter-role | true | measured |
| INF-ROLE-33 | role | irpt-status-role | true | measured |
| INF-ROLE-34 | role | irpt-ycharts-generate-role | true | measured |
| INF-ROLE-35 | role | mdpf-daily-runner-ec2-role | true | measured |
| INF-ROLE-36 | role | mdpf-feeder-trigger-role | true | measured |
| INF-ROLE-37 | role | opal-assets-ingest-router-role | true | measured |
| INF-ROLE-38 | role | opal-inf-served-guard | true | measured |
| INF-ROLE-39 | role | opal-inf-value-parity | true | measured |
| INF-ROLE-40 | role | opal-portal-lambda-role | true | measured |
| INF-ROLE-41 | role | firmsep-inf-bucket-recovery-role | false | measured |
| INF-ROLE-42 | role | irpt-inf-holdings-performance-role | false | measured |
| INF-ROLE-43 | role | irpt-inf-ycharts-research-role | false | measured |
| INF-ROLE-44 | role | mdpf-inf-gold-writer-role | false | measured |

## Denominators

- lambda_functions_graph_LAMBDA_nodes: 238
- lambda_functions_live_list_functions_auto_paginated: 237
- lambda_functions_name_pattern_read_in_live_list: 63
- lambda_functions_env_naming_inflection_or_legacy_inf_bucket: 23
- lambda_functions_env_naming_any_legacy_bucket_opal_data_bd_inf_cot: 32
- iam_roles_scanned_get_account_authorization_details: 303
- iam_customer_managed_policies_scanned: 56
- iam_roles_with_allow_on_opal-data-inf: 40
- iam_roles_with_deny_only_on_opal-data-inf: 20
- iam_roles_with_allow_on_opal-data-inflection: 8
- iam_roles_with_allow_on_opal-data-bd_inflection_scope: 0
- s3_bucket_notification_lambda_configurations_opal-data-inf: 2
- s3_bucket_policy_statements_opal-data-inf: 2
- cloudfront_distributions_listed: 2
- cloudfront_distribution_EVTSA9VEHNZVH_origins: 7
- cloudfront_distribution_EVTSA9VEHNZVH_behaviours: 30
- cloudfront_behaviours_targeting_S3-opal-data-inf_origin: 0
- cloudfront_lambda_edge_associations_on_EVTSA9VEHNZVH: 40
- eventbridge_rules_inflection_pattern_graph: 30
- eventbridge_rules_read_live_describe_and_targets: 30
- sns_topics_listed_live: 17
- sns_topics_inflection_pattern_matched: 3
- sns_subscriptions_read_on_inflection_topics: 2
- ses_identities_listed_live: 26
- ses_identities_naming_inflection: 2
- ses_templates_listed_live: 0
- repo_tracked_files_worktree_outer: 80104
- repo_tracked_files_portal_nested_repo: 2127
- repo_tracked_files_naming_opal-data-inf_outer_repo: 2576
- repo_portal_files_naming_opal-data-inf: 2
- repo_edge_router_bundle_members_read: 2
- mapping_v4_rows_opal-data-inf: 3127
- mapping_v4_rows_opal-data-bd_with_inflection_scope_prefix: 0

## Not read

- IRPT Lambda source (infra/aws/lambda/investor-reporting/*): live env maps and IAM grants read; per-key use not traced line by line.
- Inf pipeline pull Lambdas INF-FN-11 to INF-FN-19 (api pulls, accounts, billing, performance, tax, unified dim): legacy access stated from the IAM grant (measured), not from line-level code reads.
- shared-advisor-router rewrite template (the target key shape after the firm lookup) not traced beyond the firm map; the live package was read by zipfile and regex only.
- auth-validator-edge (viewer-request on 26 behaviours), cache-control-injector and public-data-router (origin-request, 2 behaviours) packages not read; no legacy env reference observed.
- orion/jwt/current.json (credential object): referenced by readers; contents NOT read or printed by design.
- opal-data-inf/gold/meta/pipeline-complete.json: existence not probed (no head on the key); its watchers are the rule and the notification.
- SNS subscription endpoints of inf-otp-alert (email and sms): protocol counts only; endpoints withheld.
- SES identities: the two individual addresses at the firm domain counted, not printed; SES templates 0.
- EventBridge Scheduler schedules: not read (FB-k-1 scope); the graph holds one Scheduler node for the firm (irpt-inf-holdings-performance-daily).
- Graph LAMBDA nodes 238 against live list-functions 237: the one-node difference is not identified.
- EC2 instance-profile roles (inf-exporter, inf-gold-layer-ec2, inf-bronze-runner, inf-gold-qa-runner, mdpf-daily-runner): which instances assume them was not read.
- Portal: only portal/src/api/endpoints/advisor-intelligence.ts names the legacy bucket among 2127 tracked portal files; other portal readers of inflection keys route through the router and were not enumerated.
- Mapping table (mapping_v4.json, 3451 rows) used only as a denominator cross-check; no row of this record is sourced from it.
- CloudFront distribution list: 2 distributions; the 30 behaviours of EVTSA9VEHNZVH enumerated; the second distribution (origin opalinvest.com) not inspected.
- Lambda env values of functions with no env (inf-accounts-v2-daily and the other pull Lambdas): bucket literals in source not grepped line by line.
- Deny-only roles (20 roles with a Deny on opal-data-inf and no Allow) are fences, not grants, and are counted, not listed.
