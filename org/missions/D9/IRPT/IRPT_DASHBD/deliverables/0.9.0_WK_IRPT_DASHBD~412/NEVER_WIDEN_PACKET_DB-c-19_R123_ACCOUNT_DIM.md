# NEVER-WIDEN PACKET -- DB-c-19 (round 124, workstream B-CW): the Cottonwood account_dim, one key, both branches (UNSIGNED)

Status: UNSIGNED. This packet is an unsigned draft. It carries no signature, no approval and no sign-off from either half. It applies nothing: no resource is created, no function is built or packaged, no artifact is uploaded, no key is written, no schedule is enabled, and no Terraform is planned or applied. The CTO's half and the issuer's half both sign over the blob of this file (its git hash-object is printed by the checker DBC124-2-AC1) before any act below starts. Any edit after that blob is signed re-opens the packet.

Measured on 2026-10-15 from the worktree at HEAD cd0675ff9c (the checker's base is f02b7e9545). The reads are in ACCOUNT_DIM_PACKET_READS_R123.json in this folder, made 08:55:25Z to 08:55:26Z by boto3 read calls only. Every name below is output of lib/opal_naming.py name() or address(); none is typed by hand. Counts, dates, hashes and words only.

## Change set

Names (builder output, confirmed by calling name() and address() in this worktree):
- function: irpt-cot-account-dim-lambda (name(..., "lambda"))
- execution role: irpt-cot-account-dim-role (name(..., "role"))
- execution role inline policy: irpt-cot-account-dim-policy (name(..., "policy"))
- scheduler role: irpt-cot-account-dim-scheduler-role (name(..., "role", "scheduler"))
- scheduler role inline policy: irpt-cot-account-dim-scheduler-policy (name(..., "policy", "scheduler"))
- schedule: irpt-cot-account-dim-daily (name(..., "daily"))
- function log group: /aws/lambda/irpt-cot-account-dim-lambda (created by the module, retention 14 days)
- gold table root: s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/ (address() with the partition tail cut)
- artifact object: investor-reporting/irpt-cot-account-dim-lambda.zip (lambda-source-map.json artifact_s3_key)

Resources the Terraform root creates, derived from the five files of infra/aws/terraform/investor-reporting/account-dim/ (not from the order):
1. aws_iam_role.irpt_account_dim -- irpt-cot-account-dim-role, trust lambda.amazonaws.com (iam.tf).
2. aws_iam_role_policy.irpt_account_dim -- irpt-cot-account-dim-policy, the closed statement set below (iam.tf).
3. module.irpt_account_dim.aws_lambda_function.this -- the function (lambda.tf, module yang-lambda): handler lambda_function.lambda_handler, runtime python3.12, timeout 300, memory 1536, the existing layer irpt-performance-native-layer, tags Cell DB-c-18.
4. module.irpt_account_dim.aws_cloudwatch_log_group.lambda -- /aws/lambda/irpt-cot-account-dim-lambda, retention 14 days (yang-lambda main.tf).
5. aws_iam_role.irpt_account_dim_scheduler -- irpt-cot-account-dim-scheduler-role, trust scheduler.amazonaws.com (schedule.tf).
6. aws_iam_role_policy.irpt_account_dim_scheduler -- irpt-cot-account-dim-scheduler-policy, lambda:InvokeFunction on the one function ARN (schedule.tf).
7. aws_scheduler_schedule.irpt_account_dim -- irpt-cot-account-dim-daily (schedule.tf).

Read-only data sources, which create nothing: data.aws_lambda_layer_version.irpt_performance_native (reads the existing layer irpt-performance-native-layer; no layer version is published); data.aws_s3_object.artifact inside the module (reads the artifact, so the artifact must exist before any plan); data.aws_caller_identity.current; four aws_iam_policy_document data sources. The modules/opal_name module holds data and outputs only, no resource.

Execution role closed set (iam.tf; the silver prefixes are the two locals.tf derives from data/assets/scripts/gold/irpt_holdings_performance/sources.json; silver_locations() resolves the same prefixes):
- s3:ListBucket on the silver bucket opal-data-assets, condition s3:prefix StringLike blackdiamond/cottonwood/silver/fact_holdings/* and blackdiamond/cottonwood/silver/fact_allocations/*.
- s3:GetObject on the objects under those two prefixes of opal-data-assets, nothing else on the silver.
- s3:ListBucket on the gold bucket opal-data-cottonwood, condition s3:prefix StringLike irpt/cottonwood/gold/account_dim/*.
- s3:PutObject on arn:aws:s3:::opal-data-cottonwood/irpt/cottonwood/gold/account_dim/* only.
- logs:CreateLogStream and logs:PutLogEvents on the function's own log group and its streams only.
No delete action, no GetObject on the gold table, no ACL, no wildcard action and no wildcard resource.

Schedule (schedule.tf): group default, expression cron(45 8 ? * MON-FRI *), time zone America/New_York, flexible time window OFF, state DISABLED at creation. The target input carries no date (kind irpt_account_dim_daily and a note), so the handler resolves the T-1 trading day itself. The schedule is enabled only after the after-read, by a one-line change of state in schedule.tf from DISABLED to ENABLED, applied by safe-apply (Catch-up first, step 8).

Package step, in the order the applier runs it (none of it is run by this packet):
1. BUILD_ONLY=1 bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-account-dim-lambda. The script runs every gate, builds the zip, prints its sha256, keeps the zip, and skips the upload, the head-object verify and the source-map update (build-and-upload.sh lines 691-692).
2. ADCOT_ZIP_PATH=<the zip of step 1> python -m pytest -q infra/aws/lambda/investor-reporting/account-dim-cot/tests/test_package_resolves.py. This runs the package test on the real artifact with no AWS call.
3. Only if step 2 passes: the real bash infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-cot-account-dim-lambda. This writes ONE new object, investor-reporting/irpt-cot-account-dim-lambda.zip, in the lambda artifacts bucket named by ARTIFACT_BUCKET (build-and-upload.sh line 54), with content-sha256 metadata, verifies it by head-object, and sets artifact_sha256 in lambda-source-map.json. That object is a WRITE of the act. The source-map change is committed by the applier, not by this packet.

## Function

Mode: BUILD. The record reads all four named resources ABSENT: lambda get_function returns ResourceNotFoundException, iam get_role returns NoSuchEntity for both roles, scheduler get_schedule returns ResourceNotFoundException, and describe_log_groups finds 0 groups under the function's log-group prefix. Nothing is adopted and no import is made; the apply creates all seven resources.

Handler: infra/aws/lambda/investor-reporting/account-dim-cot/lambda_function.py, lambda_handler (lines 122-138).
- Event: {"date": "<D>"} names the day as an ISO date. With no date the handler computes target_day(now) = prev_trading_day(expected_last_trading_day(now)), the T-1 trading day of its own clock.
- A dry_run event reads the silver, builds the table and returns without a write. The act does not use it.
- Otherwise the handler first runs gold_partition_exists (one LIST with prefix date=<day>/ and MaxKeys 1). If any object sits there it returns TARGET_ALREADY_LANDED and reads nothing.
- Otherwise it reads the two silver inputs with GetObject. An absent input raises RuntimeError ("silver partition absent") before any write.
- It builds the table with the adapter's pure build_account_dim(), then emit_account_dim(upload=True). That refuses a non-empty partition (FileExistsError) and writes through stream_parquet: the parquet is written locally, then ONE put_object of the key, then the response ETag is compared with the local md5.
- Refusals: absent silver raises and writes nothing; a non-empty partition returns TARGET_ALREADY_LANDED; an ETag mismatch raises StreamWriteUnverified after the put, which leaves the object at the key (Both branches, third branch); a custodian declaration that does not select exactly one source raises at silver_locations().
- Success returns {"date", "ok": true, "landed": true, "rows", "keys"}.

## Catch-up first

The ordered acts. Each starts only after the one before is complete and read.
1. Both halves sign over the blob of this file. Nothing below starts before both signatures are on that blob.
2. Open the change-management ledger entry with .tools/deploy_ledger.py open before the first write (CLAUDE.md NEVER-2). The entry declares every leg in advance: the artifact upload, the safe-apply of the root, the single invoke, the after-read, and the schedule enable.
3. Build and package test: the three steps of the Change set package step, in that order.
4. A LIST before the invoke of the account_dim gold prefix (the record reads 0 objects), and of the other gold prefixes under irpt/cottonwood/gold/, so that the after-read has a before-state for every prefix it compares.
5. .tools/safe-apply.sh of infra/aws/terraform/investor-reporting/account-dim/ creates the seven resources. The schedule is created DISABLED. The applier reads the plan and the state of the schedule before applying.
6. ONE invoke of the function with the event {"date": "2026-10-13"}, the pinned date of Keys written. This packet grants no second invoke. A failed invoke goes to Both branches, and any retry is a new decision for the CTO's half.
7. The AFTER-READ. A fresh LIST of the account_dim gold prefix must show exactly one key, the pinned date's data.parquet, and nothing else. The object's size and ETag are recorded from a head-object. The parquet is read back for its row count and its schema hash, computed by the method named in org/standards/IRPT_DASHBD_ACCOUNT_DIM_CONTRACT.json (schema_hash_basis) and compared with that file's schema_hash field. The silver counts and newest dates are read again and must equal the record. The other gold prefixes must show no new key against step 4.
8. ONLY IF the after-read passes: the schedule is enabled by the one-line change of state from DISABLED to ENABLED in schedule.tf, and applied by safe-apply.
9. The ledger stays OPEN for the first scheduled fire, which is 08:45 New York on the next trading weekday. The ledger closes only after that fire's own read.

## Keys written

The pinned date is the common_newest of the record: 2026-10-13, present in both silver tables in a fresh LIST at 08:55:25Z (fact_holdings newest 2026-10-13, fact_allocations newest 2026-10-13, common count 91).

The ONE key, as address() output with /data.parquet appended:

s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/date=2026-10-13/data.parquet

Pre-run state: ABSENT. The fresh LIST of the whole prefix irpt/cottonwood/gold/account_dim/ at 08:55:25Z returned 0 objects (record gold_account_dim.object_count = 0). The key is written by one put_object of the local parquet, and the response ETag must equal the local md5 before the act is read as landed.

The scheduled fires after enabling write one new key per trading day. Each is a new key under the same rule: the T-1 trading day of the fire's own clock, under the address() of that day. A re-fire on a day already landed writes nothing and returns TARGET_ALREADY_LANDED. The first scheduled fire writes its own T-1 day and does not backfill the days between the pinned date and that day (Questions, item 3).

No other prefix is read or written beyond these: the two silver inputs (GetObject of the one partition each, in opal-data-assets); the function's own gold prefix (one LIST per invoke and the one put above); the artifact object (one put by build-and-upload.sh); and the root's own Terraform state.

## Both branches

Success (the invoke returns landed true). The gold gains one partition, date=2026-10-13. Who reads it, as established from the repo:
- infra/aws/lambda/investor-reporting/reporting-gold/handler.py line 722 calls ad.households(reader, None).
- data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_report_reader.py households() (lines 141-158) takes the NEWEST account_dim partition, reads its account_id and household_id columns, and REFUSES when the prefix holds none.
- Those households feed filled_report_values.py main() (line 1032), the build that the reporting-gold stage runs.
So the first landed partition changes the household source of the next reporting-gold run. Whether that stage runs on a schedule, and whether its output is served, is NOT ESTABLISHED: the reporting-publish handler and the portal path were not read. No other reader of account_dim was found under data/, under infra/aws/lambda/investor-reporting/ or in this worktree's portal folder (a Grep of each folder).

The invoke fails, or the silver of 2026-10-13 is absent. The handler raises RuntimeError before any write, because the silver reads precede emit. The key is not written. The function and the roles stay, the schedule stays DISABLED, and the applier does not enable it. A second invoke is not in this packet.

The unverified write (an ETag mismatch after the put). The writer raises StreamWriteUnverified, and the unverified object is left at the key. Every later invoke for the same day then returns TARGET_ALREADY_LANDED from the guard, before any silver read, so the same-key overwrite that the writer's comment describes cannot run through this handler. The object must be read and judged by the CTO's half. Its removal is an S3 delete, which needs Andrew's word. Filed as channel row IRPT_DASHBD-D2-W412-S1 (BLOCKING, INERT; the function is not deployed, so the hazard is latent).

A failure inside the build before any put (an adapter or schema error). The stream writer aborts its local temp, and nothing lands. The handler raises.

Partial states of the ACT. The table itself cannot be partial, since it is one key. The act can be:
- (a) Resources created, no key. The schedule is DISABLED and the function exists with no object. The applier stops at step 6 and does not invoke again. The rollback is the reviewed plan of the Rollback section.
- (b) Key written, schedule not enabled. The after-read has passed and the enable is pending. The state stays DISABLED until the one-line change and safe-apply succeed. If safe-apply fails mid-apply, the applier finishes in session or rolls back and escalates loud, and the ledger stays open (NEVER-2).
- (c) Key written, after-read fails (more than one key under the prefix, or a key outside the pinned date moved). The applier does not enable the schedule. Removing the key is an S3 delete, which needs Andrew's word.
- (d) Artifact uploaded, no Terraform apply. The object exists. Its only consumer is the module's data.aws_s3_object read at plan. The applier records it; its deletion needs Andrew's word.

## Rollback

- The one key: an S3 delete of date=2026-10-13/data.parquet restores the pre-run state ABSENT. It is a delete and needs Andrew's word under CLAUDE.md section 5 and the agent autonomy rule. This packet does not authorise it.
- The schedule: set state back to DISABLED by a one-line change and safe-apply, or remove the resource in a reviewed plan. Either stops every scheduled fire.
- The function, the two roles, their two inline policies and the log group: remove them in one reviewed plan through safe-apply, in the root's own state. Removing the log group also removes its logs; if those logs are to go, that is a delete and needs Andrew's word.
- The artifact object: an S3 delete of investor-reporting/irpt-cot-account-dim-lambda.zip, which needs Andrew's word. The artifact_sha256 entry in the source map is reverted by a commit.
- The Terraform state: the root's own state only. No other root's state is read or written.
No rollback step reads or writes the silver inputs.

## Questions for the CTO's half

1. The applying seat and its AE lane. This packet does not name them.
2. The pinned date against the history question. The default of this packet is ONE partition, 2026-10-13, and no earlier partition. The repo's household reader takes only the newest partition (cottonwood_report_reader.py households()), so no reader in the repo needs history. Confirm, or name the earlier dates a consumer needs.
3. The first scheduled fire writes its own T-1 trading day and does not backfill. If the schedule is enabled on the day of a fire that computes a later day, the days between 2026-10-13 and that day stay absent. Confirm that gap, or name a backfill, which would be a separate packet.
4. The bucket policy of opal-data-cottonwood was NOT read. The gold bucket's deny fence admits role names carrying the firm token (iam.tf header), and the new role name carries it. Confirm the live policy admits the role before any apply.
5. The schedule time. 08:45 New York is 12:45 UTC under EDT and 13:45 UTC under EST, against the measured landing of about 11:46 UTC. The holdings-performance trigger fires at 08:15 New York (schedule.tf comment, lines 7-8). Confirm the time against both.
6. Retries. The schedule sets no retry policy, so the scheduler's defaults apply to a fire that raises on absent silver. The default retry count of the scheduler is NOT ESTABLISHED in this packet. A re-fire of a landed day is a no-op (TARGET_ALREADY_LANDED). Confirm that this is acceptable.
7. The unverified-write branch (channel row IRPT_DASHBD-D2-W412-S1). The writer's comment assumes a same-key reconvert overwrites the unverified object, but the handler refuses any non-empty partition. Rule which path a future unverified write takes: a handler change, a delete with Andrew's word, or the stop as written.
8. The artifact upload is a write: one new object in the artifact bucket and an artifact_sha256 record in the source map. Confirm it is inside the blast radius of this act.
9. The rollback deletes need Andrew's word before they run. Confirm the wording of the Rollback section.
10. The layer irpt-performance-native-layer is read by the data source at plan. Its existence was NOT read in this packet, so a plan fails if it is absent. Confirm before the plan.
11. Both halves sign the same blob. The checker DBC124-2-AC1 prints that blob's git hash-object.

## Not in this packet

- Not read: the bucket policies of opal-data-cottonwood, opal-data-assets and the artifact bucket; the live IAM state beyond the get_role results (no attached policy, no trust policy); the existence of the layer irpt-performance-native-layer; the scheduler's default retry behaviour; the consumers beyond the repo (the reporting-publish handler and the portal path); the content of any silver partition (only partition presence was read).
- Not run: whether the invoke would succeed; any build, package test, plan, apply, upload, invoke or write; the schema hash of the object that the invoke would write.
- NOT ESTABLISHED: whether the reporting-gold stage runs on a schedule and when; whether any served output reads account_dim through the portal path.
- The fire time against the holdings-performance trigger and the other schedules is read from the schedule.tf comments only; no schedule was read live.
