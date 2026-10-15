# NEVER-WIDEN PACKET -- hop 1 to the cloud: the 49 Financial reporting-gold function gains the `filled_report_values` stage (IRPT_DASHBD rounds 118 to 123, workstream B-49F): ONE Terraform apply, TWO in-place changes, ONE new gold prefix

**Author:** 2.0.0_SA_COO~D2. **Date:** 2026-10-15 ~11:0xZ. **Ordered by:** 1.0.0_SA_CTO~DELL2, CTO round-120 analysis @5e358b0a8f ruling 1 (hop 1 goes to the cloud under a never-widen pair), round-121 @9d4bd6adf3 ruling 1 (the three grants ride the pair), round-122 @e690365741 ruling 1 (one invocation per owed day, `InvokeOwnFunctionOnly`) and round-123 @1ffd4f5afb ruling 1 (`memory_size = 8192`, plan 0/2/0, the after-read records `Max Memory Used`).
**Two halves, one packet:** the COO half is `NEVER_WIDEN_HOP1_FILLED_REPORT_VALUES_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is applied until both halves are SIGNED on one sha256.**

## 1. The act

ONE Terraform apply of the root `infra/aws/terraform/investor-reporting/reporting-gold/`, by `.tools/safe-apply.sh` (never a bare `terraform apply`, never `aws lambda update-function-code`), by the AE applier `0.7.0_AE_CloudOps~DB2`, after the bundle of the function `irpt-49f-reporting-gold-lambda` is built and uploaded by `infra/aws/lambda/ci/build-and-upload.sh` from the source-map entry `irpt-49f-reporting-gold-lambda`. **The plan gate is exactly 0 to add, 2 to change, 0 to destroy, on exactly these two addresses; any other line STOPS the act:**

| address | changes |
|---|---|
| `module.irpt_reporting_gold.aws_lambda_function.this` | `memory_size` 3008 to **8192**; the code hash (`s3_object_version` / `source_code_hash`) to the new bundle; nothing else (`timeout` stays 900, handler, runtime, role, layers, environment unchanged) |
| `aws_iam_role_policy.irpt_reporting_gold` | the policy document gains **four statements** and one existing statement's list gains a sixth prefix (below) |

**The four new statements and the one extended list (explicit actions, no wildcard, every ARN derived and recounted from the naming builder; recorded in `deliverables/0.9.0_WK_IRPT_DASHBD~197/RD_GRANTS_FACTS_R121.json` and `~201/RD_SPLIT_FACTS_R122.json`):**
1. `WriteTheFiveGoldPrefixesOnly` (sid unchanged, now six prefixes): `s3:PutObject` on `arn:aws:s3:::opal-data-49financial/irpt/49financial/gold/filled_report_values/*` added to the five existing gold write prefixes. It stays the ONLY PutObject statement.
2. `ReadTheServedModelSeriesObjectOnly`: `s3:GetObject` on the ONE object `arn:aws:s3:::opal-data-portal-v2/json/benchmarks/model_portfolio_timeseries.json`.
3. `ListExactlyTheHouseholdCrosswalkPrefix`: `s3:ListBucket` on `arn:aws:s3:::opal-data-49financial`, only under `s3:prefix` `advi/49financial/gold/household_crosswalk/*`.
4. `ReadTheHouseholdCrosswalkOnly`: `s3:GetObject` on `arn:aws:s3:::opal-data-49financial/advi/49financial/gold/household_crosswalk/*`.
5. `InvokeOwnFunctionOnly`: `lambda:InvokeFunction` on the function's OWN ARN only (built from the builder module's function name), the only `lambda:` action in the policy.

**What the code does (merged; read line by line by this seat):** the scheduled 07:41 America/New_York fire runs the earlier stages exactly as today, then computes the filled days owed and runs the OLDEST one (`run_filled_day`: build with the round-118 module from the day's gold tables, write ONE partition `data.parquet` at the builder address of `filled_report_values`), then invokes ITSELF asynchronously (`InvocationType` Event, payload `{"day": <next owed>}`) if another day is owed. An invocation carrying a `day` runs only that day, no earlier stage, and chains the next. A day whose `data.parquet` exists is a no-op. A failed day is logged `FILLED_SKIPPED`, left unlanded, and the chain moves past it. The stage never raises into the earlier tables.

**Pins.** Code at or after trunk `00e325c0bb` (`box/dell2`, LOCAL; the pieces landed as `3e1230abec` (the stage), `ac0b90b6f3` (the grants), `091ad4ded1` (the split), `00e325c0bb` (the memory)). sha256 of the files at the time of this packet (the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry): `handler.py` `ad1a382500cb...` (59,221 bytes), `iam.tf` `a9b82429beeb...` (8,002), `locals.tf` `b7a293c0578c...` (11,319), `lambda.tf` `a20ea4a0a21c...` (4,557), `filled_report_values.py` `e34bffa95e0f...` (54,508), `adapters/model_series_windows.py` `84105b78d74a...` (7,413), the performance contract `abb005cac25a...` (187,938). **The three new source-map members (`filled_report_values.py`, `model_series_windows.py`, the performance contract) carry `pin` and `sha256` null in the repo: the applier writes them in the same change, as for the earlier members.**

## 2. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-49f-reporting-gold-lambda`: `MemorySize` 3008, `Timeout` 900, `Runtime` python3.12, `Handler` handler.lambda_handler, role `irpt-49f-reporting-gold-role`, `CodeSha256` `J6M/92MhjYM/0kKoYRQwR0ah68DizcvnkVSE6o24udg=`, `LastModified` 2026-10-13T12:39:43Z (equal to the source map's recorded `deployed_code_sha256`).
- **Role policy** `irpt-49f-reporting-gold-policy`: seven statements (`ListExactlyTheDeclaredSilverPrefixes`, `ReadDeclaredSilverPartitionsOnly`, `ListExactlyTheSixGoldPrefixes`, `ReadTheSixGoldPrefixesOnly`, `WriteTheFiveGoldPrefixesOnly`, `ReadTheClassTableByKeyOnly`, `OwnLogStreamOnly`); none of the new ones. After the apply it has eleven.
- **Schedule** `cron(41 7 ? * MON-FRI *)` America/New_York, ENABLED (unchanged by this act).
- **Not read:** the gold prefix `filled_report_values` (this seat did not LIST it; a first write into an empty prefix is the expectation, to be confirmed by the applier's pre-read).

## 3. What the apply changes in the world, and what the first fires do

- **At the apply:** nothing served moves. The function's code and memory change and its role gains the five grants above; no gold object is written by the apply itself.
- **At the first scheduled fire after the apply:** the earlier tables are written as on any day. The filled stage owes ONLY the days this fire wrote (`class_owed_days` with no filled partition landed returns the fire's own days: the first fire never pulls history), so it writes ONE new partition, `irpt/49financial/gold/filled_report_values/date=<the newest returns day>/data.parquet`, built from the firm's full gold history, the served model series and the household crosswalk. It is a NEW prefix: no existing key is overwritten. From the second fire on, each fire writes the days after the newest landed filled day, oldest first, one invocation each.
- **History is NOT backfilled by this act.** A filled partition for an earlier day needs an explicit `{"day": "<YYYY-MM-DD>"}` event, one invocation per day (about 160 s each at the local measurement). That is a later cell.
- **Readers.** Whether any served code reads `filled_report_values` is NOT ESTABLISHED by this seat; the table is new and its portal reader is a later hop.

## 4. Writers of the changed property, counted

The property is the content of the gold prefix `filled_report_values`. **ONE rule writes it, `run_filled_day` (through `filled_write` and `emit_filled`), entered by TWO paths:** the scheduled fire (the oldest owed day) and a `day` event (a chain link or an explicit event). N = 1 rule, 2 entry paths; the IAM write grant admits no other principal's path to the prefix. No other function writes it. The earlier five gold prefixes keep their one writer each; this act changes none of their rules.

## 5. Both branches

- **Branch A (the stage runs):** the section 3 behaviour; the after-read (condition 4) records the first fire's `Max Memory Used` and duration from its REPORT line against 8,192 MB and 900 s, the partition's existence and row count, and that the chain stopped.
- **Branch B (the stage fails):** (i) a read denied or an input absent: the day is logged `FILLED_SKIPPED`, nothing is written for it, and the earlier tables are unaffected (the stage runs after them and never raises into them); (ii) a memory kill or a timeout of the invocation: the earlier tables of that fire are already written; **the schedule sets no explicit retry policy and the function is invoked asynchronously, so Lambda's own async retry (two retries by default) re-runs a failed invocation, and with it the earlier stages, which are idempotent by design (a day is rewritten with the same content), and the filled day again;** (iii) the self-invoke is refused: the day is logged, the chain stops, and the next scheduled fire owes the remaining days again.
- **The plan is not the world.** `terraform plan` has NEVER been run for this change (the box this seat works on has no terraform binary; the files were checked by their checkers, not by Terraform). The applier's plan is the first reading; the gate above is the check.

## 6. Rollback, per key

- **Function code and memory:** a `terraform apply` through `safe-apply` of the reverted files (`git revert` of the four merges), which restores `memory_size` 3008 and the previous bundle (`CodeSha256` `J6M/92Mh...`; the artifact bucket `opal-313476888478-lambda-artifacts` has versioning `Enabled` (read by this seat): the applier records the previous object's version id in its ledger entry before the apply). Never `update-function-code`.
- **Policy:** the same revert removes the five statements and returns the policy to its seven.
- **Gold objects the stage wrote:** a partition under `irpt/49financial/gold/filled_report_values/date=...` is removed ONLY by an explicit listed-key delete with Andrew's word (a first write into an empty prefix is Andrew's delete); never a wildcard prefix delete. Nothing else is written by this act.

## 7. Conditions, and the questions for the CTO's half

**Conditions.**
1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-hop1-filled-report-values-20261015` with legs L1 git (the commit pin of the applier's tree and the sha256 of each file in section 1), L2 terraform (the plan 0/2/0 on the two addresses, then the apply, recorded by `infra/aws/lambda/ci/record-terraform-deploy.sh`), L3 verify (the first scheduled fire after the apply: the REPORT line's `Max Memory Used` and duration, the new partition's row count, no `FILLED_SKIPPED`). The ledger stays OPEN to L3 and is recorded known-held if the fire has not happened inside its window. Read every live worktree's `.open_deploys/` first and print the denominator.
2. **The live state is re-read at the moment of the apply** and equal to section 2 (memory 3008, `CodeSha256` `J6M/92Mh...`, seven policy statements), else STOP.
3. **The bundle is built from the pinned files;** the applier writes the three new members' `pin` and `sha256` into the source map in the same change and verifies the artifact's recorded hash after upload; the plan is read BEFORE the apply and anything but 0/2/0 on the two addresses STOPS.
4. **The after-read** is the first real scheduled fire (07:41 New York on a trading day) or, if the applier wants it sooner, ONE `{"day": "<the newest returns day>", "dry_run": true}` event is NOT a proof (nothing is written); the proof is the real fire. A real manual event for one day is a write and needs the CTO's word.
5. **Not during another seat's open ledger entry on the reporting-gold root,** and not within an hour before a scheduled fire.
6. **No `update-function-code`, no bare `terraform apply`, no schedule change, no other root.** The Cottonwood root (`account-return-daily`) is a different pair.

**Questions (the CTO's half decides them):**
1. **The unqualified function ARN.** `InvokeOwnFunctionOnly` grants `lambda:InvokeFunction` on the unqualified ARN; the handler invokes `context.invoked_function_arn`. If a scheduled invocation reports a qualified ARN (an alias or version), the self-invoke is refused and the chain stops after the first day (Branch B iii; the earlier tables and the first day are unaffected). Accept that the first fire is the first reading, with the fix (a qualified-ARN grant or an unqualified invoke target) a later cell?
2. **History.** Accept that this act lands ONE new partition per fire and no backfill, with the backfill a later cell (explicit day events or an orchestrator)?
3. **Async retry on a failed invocation** (Branch B ii) re-runs the earlier stages. Accept, given their idempotence, or require `MaximumRetryAttempts` 0 on the schedule's target in this pair (a third change; the plan would then read 0/3/0)?

## 8. Not established, and so not covered

A `terraform plan` of the change; the Lambda's actual memory and time at 8,192 MB (the 4,025 MB peak and the 154 s day were measured on a workstation, not in the Lambda); the real input sizes at the first fire (the local day was 2026-10-13); whether the unqualified ARN matches; which served code reads `filled_report_values`; the prefix's current emptiness.

-- 2.0.0_SA_COO~D2
