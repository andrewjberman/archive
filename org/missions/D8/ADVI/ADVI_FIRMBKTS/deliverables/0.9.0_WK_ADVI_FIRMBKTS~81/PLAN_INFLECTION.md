# PLAN_INFLECTION -- ADVI_FIRMBKTS FB-l-1 (FWD-9a, read-only)

Order FB-l-1, firm inflection, record PLAN_INFLECTION.json (same folder). Read at 2026-10-14T12:25:30Z. Claim: measured (from-states read live; to-states are the plan's proposals). Nothing in this plan was executed: no AWS write, no producer run, no deploy, no terraform command.

## 1. Ordered move table

Order is the sequence of execution. A move runs only after its depends_on have landed and been proven. Each row carries rollback and proof in the JSON record; this table gives the short form and the decision owner.

| # | id | function | kind | depends_on | covers | claim | decision |
|---|---|---|---|---|---|---|---|
| 1 | M01 | exec-summary-trigger (rule) and exec-summary-generator (target) | rule | - | INF-RULE-02, INF-FN-28 | measured | CTO: confirm the rule is 49 Financial-only and that the Inflection exec summary is out of scope (open question Q14) |
| 2 | M02 | opal-data-inflection (bucket policy, EventBridge delivery) | role | - | - | measured | CTO: admitting 35 more roles to an identity-plane Deny is a fence change (open question Q4) |
| 3 | M03 | inf-portal-publisher (trigger leg) | schedule | M01 | INF-FN-01 | measured | CTO: the 49 Financial publisher stage is itself DISABLED (advi-49f-publisher); the shape is a design, not a proven live path (surprise S3) |
| 4 | M04 | Door 6: gold/meta/pipeline-complete.json, its notification, rule mdpf-feeder-accelerator, router deny | notification | M03 | R01-mdpf-feeder-accelerator, INF-RULE-01, L27-inf-gold-freshness-guard | held | Andrew's word is required for the marker delete (DEC-17); Q7, Q8 and Q9 must close first |
| 5 | M05 | Inflection bulk data copy (all layers, copy-only) | other | M02 | - | held | Andrew's word is not required for a copy; the layout and the F2 key map are the CTO's call (Q5) |
| 6 | M06 | inf-bronze-complete-emitter | lambda | M05, M02 | L12-inf-bronze-complete-emitter, INF-FN-06, INF-ROLE-09 | measured | - |
| 7 | M07 | inf-api-positions | lambda | M05, M02 | L08-inf-api-positions, INF-FN-11, INF-ROLE-05 | measured | - |
| 8 | M08 | inf-api-reps | lambda | M05, M02 | L09-inf-api-reps, INF-FN-12, INF-ROLE-06 | measured | - |
| 9 | M09 | inf-api-txn | lambda | M05, M02 | L10-inf-api-txn, INF-FN-13, INF-ROLE-07 | measured | - |
| 10 | M10 | inf-api-assets-v2 | lambda | M05, M02 | L06-inf-api-assets-v2, INF-FN-14, INF-ROLE-03 | measured | - |
| 11 | M11 | inf-accounts-v2-daily | lambda | M05, M02 | L05-inf-accounts-v2-daily, INF-FN-15, INF-ROLE-02 | measured | - |
| 12 | M12 | inf-billing-daily | lambda | M05, M02 | L11-inf-billing-daily, INF-FN-16, INF-ROLE-08 | measured | - |
| 13 | M13 | inf-performance-daily | lambda | M05, M02 | L20-inf-performance-daily, INF-FN-17, INF-ROLE-21 | measured | - |
| 14 | M14 | inf-tax-daily | lambda | M05, M02 | L21-inf-tax-daily, INF-FN-18, INF-ROLE-24 | measured | - |
| 15 | M15 | inf-unified-account-dim-daily | lambda | M05, M02 | L22-inf-unified-account-dim-daily, INF-FN-19, INF-ROLE-25 | measured | - |
| 16 | M16 | inf-api-eclipse | lambda | M05, M02 | L07-inf-api-eclipse, INF-FN-10, INF-ROLE-04 | measured | - |
| 17 | M17 | inf-bronze-trigger and rule opal-inf-bronze-runner-cron | lambda | M05, M02 | L13-inf-bronze-trigger, INF-FN-23, INF-ROLE-11 | measured | - |
| 18 | M18 | inf-jwt-trigger and rules opal-inf-jwt-fetch, opal-inf-export-schedule | lambda | M05, M02 | L23-inf-jwt-trigger, INF-FN-22, INF-ROLE-18 | measured | CTO: whether the mode marker should stay in the B2 prefix (Q6) |
| 19 | M19 | bronze runner (S06 bronze-orchestrator) and exporter EC2 roles | script | M05, M02, M17 | S06-bronze-orchestrator, INF-ROLE-01, INF-ROLE-10, INF-ROLE-13 | measured | CTO: the bronze runner is EC2; a runner dispatch needs the same hold check as the gold chain (Q11) |
| 20 | M20 | inf-assets-trigger and rule inf-assets-trigger-bronze-complete (R02) | rule | M06, M02 | R02-inf-assets-trigger-bronze-complete, INF-FN-21, L14-inf-assets-trigger | measured | - |
| 21 | M21 | inf-silver-chain and rule inf-silver-chain-bronze-complete (R03) | lambda | M06, M05, M02 | R03-inf-silver-chain-bronze-complete, L15-inf-silver-chain, INF-FN-05, INF-ROLE-23 | measured | - |
| 22 | M22 | opal-assets-ingest-mirror and rules opal-assets-ingest-mirror-inf-daily, opal-inf-assets-ingest-mirror-late-daily | lambda | M05, M02, M06 | L04-opal-assets-ingest-mirror, INF-FN-27, INF-ROLE-37 | measured | - |
| 23 | M23 | inf-silver-aggregator and its S3 notification (silver/_silver_complete/ + .json) | lambda | M07, M08, M09, M10, M11, M12, M13, M14, M15, M21, M02 | L17-inf-silver-aggregator, INF-FN-03, INF-EDGE-05 | measured | - |
| 24 | M24 | inf-gold-trigger (and gold dispatch lock) | lambda | M23, M05 | L16-inf-gold-trigger, INF-FN-04, INF-ROLE-17 | measured | - |
| 25 | M25 | inf-gold-runner-ec2 and in-instance scripts S01 to S05 (orion-gold-dispatch.sh and the INF_D and INF_C chain) | script | M24, M23, M05, M02 | L32-inf-gold-runner-ec2, S01-orion-gold-dispatch-sh, S02-INF_D_00-portal_aggregates, S03-INF_C_01-canonical_nna, S04-INF_build_canonical_prices, S05-INF_run_c_chain, INF-ROLE-14, INF-ROLE-16 | measured | CTO and COO: a gold dispatch needs the standing release and a signatory halt check before any run (the hold text in the function's environment) |
| 26 | M26 | inf-nna-partition-checker | lambda | M25 | L18-inf-nna-partition-checker, INF-FN-07, INF-ROLE-19 | measured | - |
| 27 | M27 | inf-otp-relay and rule inf-otp-state-change (R05), and the user policy inf-andrew-otp-write | lambda | M05, M02 | L19-inf-otp-relay, INF-FN-09, R05-inf-otp-state-change, INF-ROLE-20, INF-SNS-01 | measured | - |
| 28 | M28 | inf-etf-ownership-daily | lambda | M25 | L24-inf-etf-ownership-daily, INF-FN-20, INF-ROLE-12 | measured | - |
| 29 | M29 | inf-client-detail (on-demand API) | lambda | M25 | INF-FN-08 | measured | - |
| 30 | M30 | inf-portal-advisor-publisher (invoked by the publisher) | lambda | M25, M03 | L26-inf-portal-advisor-publisher, INF-FN-02 | measured | CTO and COO: never-widen sign-off for the served keys is required before this move (Q10) |
| 31 | M31 | inf-portal-publisher (bucket leg, cutover) with CloudFront invalidation | lambda | M03, M04, M30, M25 | L25-inf-portal-publisher, INF-ROLE-15 | measured | CTO and COO: never-widen sign-off (served output, Q10) |
| 32 | M32 | opal-inf-served-guard and rule opal-inf-served-guard-on-write (R06) | lambda | M31 | L30-opal-inf-served-guard, INF-FN-25, R06-opal-inf-served-guard-on-write, INF-ROLE-38 | measured | - |
| 33 | M33 | opal-inf-value-parity and rule opal-inf-value-parity-hourly | lambda | M32, M27 | L31-opal-inf-value-parity, INF-FN-26, INF-ROLE-39 | measured | - |
| 34 | M34 | shared-advisor-router and shared-advisor-router-response (Lambda@Edge) and firm-config.mjs | edge | M31, M32 | L33-shared-advisor-router, INF-EDGE-01, INF-EDGE-02, INF-REPO-01, INF-READER-01 | measured | CTO and COO: never-widen sign-off (served output route; blast radius per key) |
| 35 | M35 | IRPT family 1: irpt-directory-search, irpt-status, irpt-holdings, irpt-narrative, irpt-export-render, irpt-directory-refresh | lambda | M05, M02 | INF-FN-29, INF-FN-30, INF-FN-31, INF-FN-32, INF-FN-33, INF-FN-34, INF-ROLE-26, INF-ROLE-27, INF-ROLE-28, INF-ROLE-29, INF-ROLE-31, INF-ROLE-33 | measured | the IRPT lane (IRPT_BCKEND) owns the bucket: its ownership of the cutover needs a decision (Q12) |
| 36 | M36 | IRPT family 2: irpt-performance-adapter, irpt-ycharts-generate | lambda | M35 | INF-FN-35, INF-FN-36, INF-ROLE-32, INF-ROLE-34 | measured | - |
| 37 | M37 | irpt-inf-holdings-performance-lambda (read leg) and rule irpt-inf-holdings-performance-daily | lambda | M05 | INF-FN-39, INF-ROLE-30, L03-irpt-inf-holdings-performance-lambda | measured | - |
| 38 | M38 | mdpf-feeder-trigger (WSC gate read) | lambda | M04, M25 | L01-mdpf-feeder-trigger, INF-FN-24, INF-ROLE-36 | measured | - |
| 39 | M39 | S07 build_mdpf_wsc_inflection_feeder (MDPF feeder dispatch, run through SSM on the runner) and instance role mdpf-daily-runner-ec2-role | script | M38, M25 | S07-build_mdpf_wsc_inflection_feeder, INF-ROLE-35 | measured | - |
| 40 | M40 | leading-slash namespace on opal-data-inf ('/' prefix, 339 objects) | other | M05 | - | measured | CTO: migrate or retire (Q5); Andrew's word for any delete (DEC-17) |
| 41 | M41 | CloudFront origin S3-opal-data-inf and bucket-policy statements AllowScopedAdvisorOAI and AllowCFDistributionGold | edge | M34, M35, M36, M31 | INF-EDGE-03, INF-EDGE-04 | measured | CTO: a distribution change on the portal (not a portal code change) (Q13) |
| 42 | M42 | opal-portal-lambda-role: wildcard Allow on opal-data-inf | role | M41 | INF-ROLE-40 | measured | the portal lane owner and the CTO decide (Q15) |
| 43 | M43 | inf-jwt-trigger and B2 readers (orion/jwt/current.json) - kept on purpose | other | M16, M10, M09, M08, M07, M11, M12, M13, M14, M15, M19 | - | held | Andrew's ruling DEC-13 applies; out of the 45-day set |
| 44 | M44 | opal-data-inf decommission (reduction to the B2 credential) | other | M04, M23, M25, M31, M34, M35, M36, M37, M38, M39, M40, M41, M42, M43 | - | held | Andrew's word for every delete (DEC-17); the window start is set by the CTO (Q2) |

## 2. Decommission of opal-data-inf and its 45-day window

- Legacy bucket: opal-data-inf. The bucket is reduced, not deleted: it stays open for B2 alone (orion/jwt/current.json, out of the 45-day set by Andrew's ruling DEC-13).
- Window: 45 days, starting at Inflection's cutover (the CTO sets the date, Q2). It counts reads and writes on every other key.
- Instrument: opal-organization-trail, logging true, with ReadOnly and WriteOnly data events on opal-data-inf/ (read live). Proof reader: the CTO (FWD-6). Delete: Andrew's word only (DEC-17).
- Live state of the bucket now: 20 top-level prefixes (including a leading-slash namespace of 339 keys), 2 bucket-policy statements, 2 notification entries, 1 CloudFront origin (0 behaviours), 60 IAM roles with a statement on it (40 Allow, 20 deny-only), 21 Lambda environments naming it, 7 EventBridge rules naming it.

## 3. Legacy operations to retire

| id | operation | consumers | decision |
|---|---|---|---|
| R1 | inf-canonical-prices-daily (EventBridge rule, DISABLED and held; target inf-gold-trigger) | 0 | RECOMMEND delete with M24 (the gold cutover), keep DISABLED and held until then. Deciding: Andrew (a delete, DEC-17), on the CTO's recommendation. |
| R2 | inf-gold-full-on-bronze-complete (EventBridge rule R04, DISABLED; bronze-complete pattern to inf-gold-trigger mode=full) | 0 | RECOMMEND delete with M24. Deciding: Andrew, on the CTO's recommendation. |
| R3 | inf-gold-incremental-daily (EventBridge rule, DISABLED, cron(0 18 * * ? *) to inf-gold-trigger) | 0 | RECOMMEND delete with M24. Deciding: Andrew, on the CTO's recommendation. |
| R4 | mdpf-feeder-accelerator (EventBridge rule R01: S3 Object Created on the Door 6 key, target mdpf-feeder-trigger) | 1 | RETIRE in M04 (Andrew ruled Door 6 RETIRE with no successor marker, DEC-13). L01 continues from mdpf-feeder-backstop-daily. Deciding: Andrew, plus the CTO on Q9 (the latency of days whose input lands after the backstop). |
| R5 | Door 6 marker object gold/meta/pipeline-complete.json and its S3 notification entry (to inf-portal-publisher) | 1 | RETIRE in M04, after M03's proof. The one consumer (the publisher) moves to inf-portal-publisher-floor. Deciding: Andrew (Door 6 ruling and the delete), with the CTO on the successor proof. This row disarms D1-W80-S1 only if the CTO accepts the named successor and its proof (see the surprise channel). |
| R6 | DenyInfGoldSentinelAbsolutely (identity Deny on the marker ARN inside opal-assets-one-way-fan-in-fence, attached to 13 roles) | 13 | RETIRE in M04, step 5, only after the marker is gone. Deciding: CTO (identity-plane fence), with Andrew's Door 6 word. The resource-plane twin named in router_iam.tf is absent from the tree (surprise S6). |
| R7 | FIRMSEP-s3-direct-access-bypass (EventBridge rule, ENABLED; GetObject on opal-data-bd and opal-data-inf where the user agent is not CloudFront; target SNS opal-infrastructure-alerts) | 1 | RECOMMEND keep through the 45-day window (it is a read signal for the window record), then delete at M44. It is not a new alert (the moratorium does not reach a retirement). Deciding: Andrew (delete), CTO recommends. Subscribers of the SNS topic are not read. |
| R8 | opal-portal-lambda-role wildcard on opal-data-inf (12 non-Inflection functions assume the role) | 12 | RETIRE the statement in M42 after a zero-read record. Deciding: the portal lane owner and the CTO; the functions are not Inflection's. |
| R9 | CloudFront origin S3-opal-data-inf (defined, reached by 0 of 30 behaviours) | 0 | RETIRE in M41. Deciding: CTO (distribution change). The 0-of-30 count is inherited from FB-k-2 and was not re-read. |
| R10 | Bucket-policy statements AllowScopedAdvisorOAI (GetObject on the whole bucket) and AllowCFDistributionGold (GetObject on gold/*) on opal-data-inf | 0 | RETIRE in M44 after M41. consumers counts the distribution readers measured (0 origin behaviours); the OAI principal's other readers were not read (not_read). Deciding: CTO, with Andrew's word for the reduction. |
| R11 | inf-gold-freshness-guard (repo source, ABSENT live; reads the Door 6 key as SENTINEL_KEY; inventory row L27 says measured) | 0 | RETIRE the repo source in M04 (absent live: lambda get-function-configuration ResourceNotFound). Deciding: CTO. The inventory row L27 should be corrected (surprise S5). |
| R12 | mdpf-daily-trigger (repo source, ABSENT live; reads the Door 6 key as INF_SENTINEL_KEY) | 0 | RETIRE the repo source in M04 (absent live). Deciding: CTO. |
| R13 | Legacy code/ prefix on opal-data-inf (code/gold, code/silver, code/bronze, code/manual_api, code/exporter), used by the gold runner copy step and S01 | 2 | RETIRE in M44 after M25 repoints the copy step. Deciding: CTO. |

## 4. Open questions

- Q1 (before M03): does inf-portal-publisher parse the S3 event body? Its fixed-key constants (lines 62-68) suggest not, but the handler was not read in full. The one-time at() exercise must use the same payload the floor will send.
- Q2 (window start, M44): the 45-day window counts after each firm's cutover (PRD CONTRACTS). The CTO sets the cutover date; the org trail's ReadOnly and WriteOnly data events on opal-data-inf/ are the instrument (trail logging true, read live 2026-10-14). Its query surface and retention were not read.
- Q3 (M03 cron): the publisher floor must fire after the gold chain completes. Only one marker LastModified was read (2026-10-13T12:59:59Z). The distribution of marker times over the last 30 days decides the cron. The 49 Financial floor (advi-49f-gold-floor at 12:45Z) is a gold clock with no Inflection equivalent.
- Q4 (M02): admitting the 35 non-matching Allow roles to the Inflection bucket is an identity-plane change to a Deny. The CTO decides between explicit ARNs (this plan's proposal) and a pattern change to role/inf-*.
- Q5 (M05, M40): the F2 key map (3,127 opal-data-inf rows in the mapping table) was not read; the CTO decides the layout for bronze and silver keys and whether the 339 leading-slash keys are migrated or retired.
- Q6 (M18, M43): does the mode marker orion/jwt/trigger-mode.json stay in the B2 prefix or move? B2 itself does not move.
- Q7 (M04): who writes gold/meta/pipeline-complete.json? No inventory row names a writer (S01 and L32 list only dispatch lock, telemetry and artifacts). Until the writer is named, step (4) of M04 cannot be proven safe.
- Q8 (M04): inf-gold-freshness-guard (L27) and mdpf-daily-trigger are ABSENT live. Confirm they are not invoked by any other path (no rule, schedule or resource policy; checked: no rule targets, no resource policy) before the marker delete.
- Q9 (M04, R4): the accelerator covered days whose input lands after the 13:30Z floor. Retiring it changes the latency of those days unless the backstop fires after the marker. The count of such days over 30 days decides whether R4 retires.
- Q10 (M30, M31, M34, M36): the served keys platinum/firm/* and platinum/advisors/* move; a served-key move needs never-widen sign-off from the CTO and COO with a blast radius and a per-key rollback.
- Q11 (M19, M25, M39): EC2 instance-profile bindings for the bronze runner, the gold runner, the exporters and the MDPF runner were not resolved; each runner move needs its profile named.
- Q12 (M35, M36): the IRPT lane (IRPT_BCKEND) owns opal-data-inflection and the IRPT Lambdas. Who executes the IRPT repoint, and under which order?
- Q13 (M41): the CloudFront origin removal is a change to the portal distribution. Confirm the second distribution (not read) does not reference opal-data-inf.
- Q14 (M01): the exec-summary generator writes 49financial destinations only (INF-FN-28). Whether Inflection needs an exec summary at all is a product question, not a move.
- Q15 (M42): the 12 functions assuming opal-portal-lambda-role are outside Inflection. The owner of that role must confirm they do not read opal-data-inf before the statement is removed.
- NO-MOVE L02 mdpf-gold-lambda (legacy_touch False in FB-k-1, held; its schedule mdpf-scheduled-floor is ENABLED cron(30 13 * * ? *), read live): no Inflection move; its held state is the MDPF lane's.
- NO-MOVE L28 and L29 (EC2 launch monitor and retry launch, legacy_touch False): retained; not bucket operations.
- NO-MOVE L34 (CloudFront distribution as a whole): the distribution stays; its origin change is M41.
- NO-MOVE L35 (YangDataPipeline state machine) and L36 (globgrph ECS): not read (trigger not determined); not Inflection-legacy by the inventories.
- NO-MOVE L37 and L38 (opal-data-bd notification rows, claim absent): an opal-data-bd fact, not an Inflection move; the bucket notification of opal-data-bd was not read in this plan.
- NO-MOVE R07 (inf-gold-dispatch-release-changed, CloudTrail UpdateFunctionConfiguration on inf-gold-trigger to an SNS alarm): retained as the release audit; it names no bucket.
- NO-MOVE R09 (opal-inf-ec2-state-change-monitor): retained; it names instance ids, not a bucket.
- NO-MOVE INF-FN-37 and INF-FN-38 (irpt-49f-reporting-read-lambda, irpt-holdings-refresh-lambda; legacy_touch False): the first reads 49financial, the second's bundle map is 49financial and cottonwood and inflection to opal-data-inflection (already on the new home).
- NO-MOVE INF-RULE-03 (inf-gold-dispatch-release-changed) and INF-SNS-02 (release alarm): retained with R07.
- NO-MOVE INF-SNS-01 (inf-otp-alert topic): retained; the publisher of the topic was not identified (not_read).
- NO-MOVE INF-EMAIL-01 (SES identities for the Inflection domain): not a bucket operation; addresses withheld.
- NO-MOVE INF-ROLE-41, INF-ROLE-42, INF-ROLE-43, INF-ROLE-44 (roles already on opal-data-inflection or on the mdpf/irpt inflection prefixes): not legacy homes; no move.
- NO-MOVE INF-FN-08 is now a move (M29): listed here only because the serving inventory says legacy_touch False and the live env says the opposite.
- NO-MOVE INF-READER-01 (portal endpoint advisor-intelligence.ts): no change, because the public path is kept (M34).
- NO-MOVE INF-REPO-01 is now a move (M34).

## 5. Not read

- EC2 instance-profile bindings for the bronze runner, the gold runner, the exporters, the MDPF runner and the QA runner (roles ROLE-01, 10, 13, 14, 16, 35); the instance profile to role map was not read.
- IRPT routes: the API route to function map (INF-FN-29 to 36 are 'not traced per route' in FB-k-2; not traced here).
- The second CloudFront distribution (listed in FB-k-2, not inspected) and the Lambda@Edge code beyond the firm map.
- SNS subscriptions on the three inflection-matched topics (names withheld) and the publisher of inf-otp-alert.
- The 2 SES identities that name Inflection (addresses withheld, not printed).
- The F2 mapping table (3,127 opal-data-inf rows; FB-k-1 denominator, not re-read).
- The handler body of inf-portal-publisher beyond the key constants and the first S3 read (event parsing; CloudFront invalidation permission).
- The object contents of orion/jwt/current.json (never read, by rule) and the B2 reader set beyond the 11 functions in the inventories.
- Object-level listings under opal-data-inf beyond the depth-one prefix listing and the 339 leading-slash keys.
- L35 YangDataPipeline trigger and L36 globgrph ECS services (FB-k-1 not_read items remain unread).
- The opal-data-bd bucket notification configuration (L37 and L38 absent claims, not re-read).
- CloudTrail trail query surface and retention for the 45-day record (the trail's selectors and logging status were read; the query tool was not).
- IAM simulation: the fence's effect on each Inflection role was inferred from the ArnNotLike condition semantics; no simulate-custom-policy call was made in this plan.
- The 30 CloudFront behaviours and 7 origins and the 13 fan-in attachments are inherited (FB-k-2) except the fence attachment count, which was read live.
- The 26 SES identities and 17 SNS topics (FB-k-2 denominators; not re-read).
- The gold dispatch script bodies for S04 and S05 (dynamic keys; held in FB-k-1).
- The 169 repository files under data/ and the 200 under infra naming opal-data-inf (FB-k-1 denominators; not re-read; the code-level bucket evidence cited here is from 40 inf-pipeline files returned by the native grep, a capped set).

## 6. Denominators

- eventbridge_rules_listed_live: 156
- eventbridge_rules_naming_opal-data-inf_in_pattern_live: 7
- eventbridge_rules_naming_opal-data-inflection_live: 0
- scheduler_default_group_schedules_live: 33
- scheduler_default_group_schedules_recorded_FB-k-1: 34
- scheduler_schedules_read_by_name_live: 6
- lambda_functions_listed_live: 237
- lambda_functions_with_opal-data-inf_in_env_live: 21
- lambda_functions_named_absent_live: 2
- iam_roles_scanned_live: 303
- iam_customer_managed_policies_scanned_live: 56
- iam_roles_with_allow_on_opal-data-inf_live: 40
- iam_roles_with_deny_only_on_opal-data-inf_live: 20
- iam_allow_roles_admitted_by_inflection_fence_live: 5
- iam_fan-in_fence_attached_roles_live: 13
- s3_notification_entries_opal-data-inf_live: 2
- s3_notification_entries_opal-data-49financial_live: 0
- s3_notification_entries_opal-data-inflection_live: 0
- s3_bucket_policy_statements_opal-data-inf_live: 2
- s3_bucket_policy_statements_opal-data-inflection_live: 4
- s3_top_level_prefixes_opal-data-inf_live: 20
- s3_top_level_prefixes_opal-data-49financial_live: 6
- s3_advi_subprefixes_opal-data-49financial_live: 2
- s3_top_level_prefixes_opal-data-inflection_live: 2
- s3_leading-slash_keys_opal-data-inf_live: 339
- cloudtrail_trails_live: 2
- cloudtrail_org_trail_classic_data_selectors_on_opal-data-inf_live: 2
- inflection_lambda_env_bucket_irpt_map_functions_live: 8
- marker_head_object_samples_live: 1
- legacy_inventory_pipeline_rows_FB-k-1: 54
- legacy_inventory_serving_rows_FB-k-2: 97
- moves_in_this_plan: 44
- retire_rows_in_this_plan: 13
