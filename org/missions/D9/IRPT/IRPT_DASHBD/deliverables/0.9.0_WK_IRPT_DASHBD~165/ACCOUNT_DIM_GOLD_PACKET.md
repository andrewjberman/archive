# ACCOUNT_DIM_GOLD_PACKET -- Cottonwood account_dim into its address() gold (never-widen packet)

TO IRPT_DASHBD.TO-DB-b-200 | round 104, workstream B | decomp cell DB-b-200 (section 106) | worker 0.9.0_WK_IRPT_DASHBD~165
This packet is a never-widen packet for ONE write. It writes nothing. The COO half and the CTO half of the pair are signed by their owners, not by this cell.

Read basis: the worktree at a1d871ec33 (branch wk-IRPT_DASHBD-165). Live reads: 2026-10-14, 11:13 to 11:15 UTC, under the box identity cloudops-dell2-agent-user.

## 1. The act

ONE apply, not yet run. It writes ONE date partition of account_dim for Cottonwood:

- Partition: date=2026-10-12. This is the newest silver date the round-103 dry run used (dry-run record target_address, org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~161/COTTONWOOD_ACCOUNT_DIM.json). The adapter does NOT compute this date: emit_account_dim(table, as_of) and gold_address(as_of) take it as an argument (data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_account_dim.py, lines 165-175). It is recorded as a surprise row (IRPT_DASHBD-D2-W165-S1).
- Keys: s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/date=2026-10-12/data.parquet and .../manifest.json. Bucket and prefix come from lib/opal_naming.py address("irpt", "cottonwood", "gold", "account_dim", "date=2026-10-12"), which returns s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/date=2026-10-12 (read in this cell).
- Writer: an AE applier (the AE seat class, cloud-ops). No applier exists at HEAD.
- Upload path: the adapter HAS NO UPLOAD PATH. emit_account_dim(upload=True) raises NotImplementedError by round-103 design (adapter lines 173-174; test test_emit_defaults_to_no_write_and_upload_is_refused passes). The order's "exact invocation shape of the adapter's upload path" therefore names nothing that exists. The applier's order must add: (a) an upload function that builds the 16-column table with the adapter's ARROW_SCHEMA, writes data.parquet through the same stream writer the 49F producer uses (data/assets/scripts/lib/stream_parquet.py, stream_to_parquet), then writes manifest.json with one put_object after the parquet finalises, the same two-step shape as account_return_daily.py emit_day (lines 1876-1908); (b) an entry point with an explicit --upload flag, default off, mirroring account_return_daily.py main() (--upload, --dry-run); (c) a refusal when the prefix is not empty at the moment of the write. This is not a rider on this packet: an upload path is code, it needs its own review and tests, and this cell may not edit the adapter (grant).
- No live run. The apply is not executed in this cell and not scheduled.

## 2. What moves

Counts (the round-103 dry run, read from its record; NOT re-measured in this cell, because silver reads are outside this cell's grant):

- accounts: 999
- relationship ids (household keys, distinct non-sentinel relationship ids): 223
- partitions written by the apply: 1 (two objects: data.parquet and manifest.json)

Nulls per column in the 999 rows (dry-run record null_counts):

- absent_fields 0, account_id 0, coverage 0, firm 0, method_version 0, schema_version 0, household_relationship_count 0
- household_id 47 (null where the account has no non-sentinel relationship; reason NO_RELATIONSHIP_SENTINEL carried)
- household_id_reason 952 (null where household_id is present; this is the complement, not a defect)
- custodian 130, account_type 130, registration 130 (accounts with no roster row)
- client_id 999, tax_status 999, opened_date 999, first_data_date 999 (not carried by the Cottonwood silver in round 103; always null; listed in absent_fields)

Coverage distribution: NOT ESTABLISHED in this cell (the dry-run record carries no coverage counts).

Nothing served changes. The table is read by no consumer: a grep of data/, infra/, lib/ and portal/src for account_dim finds only the adapter, its test, the INF/Orion unified_account_dim pipeline (a different firm, bucket opal-data-inf) and registry rows. The portal positive control returned hits for InvestorReporting|account_return_daily, so the portal corpus is live and the zero for account_dim is an absence.

## 3. When and where

- The apply, when it is ever run, writes at the moment the applier runs. It is not scheduled and no schedule is touched by it.
- No schedule for account_dim exists at HEAD. The only daily trigger in this area is the 49F reporting-gold trigger for account_return_daily: infra/aws/terraform/investor-reporting/reporting-gold/schedule.tf, fire time read from REPORTING_GOLD_FIRE_TIME_R3.json (chosen_cron cron(41 7 ? * MON-FRI *), America/New_York). That trigger is out of this apply and is not changed by it.
- The table's own schedule (when account_dim would be recomputed daily) is a later packet. This packet covers one partition only.

## 4b. Writers

Writers of the target prefix irpt/cottonwood/gold/account_dim/, counted: N = 0.

- Code: a grep for account_dim over data/, infra/ and lib/ at a1d871ec33 finds, for Cottonwood, only the adapter (which writes nothing; upload refused) and its test. The other hits are the INF/Orion unified_account_dim pipeline (bucket opal-data-inf) and registry or documentation rows. The 49F producer's emit_day writes irpt/cottonwood/gold/account_return_daily/ and emit_method_row writes dim_return_method/; it reads holdings_performance_daily and writes no account_dim key.
- Live: the top level of irpt/cottonwood/gold/ holds 7 common prefixes (account_return_daily, account_return_daily_blank_reasons, dim_return_method, holdings, holdings_performance_daily, holdings_performance_manifest, holdings_qa) and no objects directly. The prefix irpt/cottonwood/gold/account_dim/ returns no objects (no Contents key in the list).
- IAM (read): the reporting-gold role may write only the account_return_daily, account_class_daily and the three activity and lot gold prefixes (infra/aws/terraform/investor-reporting/reporting-gold/iam.tf, line 133). The reporting-publish role writes only the platinum reporting prefix. Neither can write account_dim.
- NOT ESTABLISHED: the holdings-performance role's write set and any human principal's write rights to the prefix (not read in this cell; CloudTrail not read).

## 5. Both branches

- Lands: both keys exist; data.parquet is the 999-row table with the 16 ARROW_SCHEMA columns; manifest.json names the address and the counts. The prefix then holds exactly two objects, and no other key moves.
- Fails before data.parquet finishes: the stream writer aborts and nothing lands, per the contract of stream_to_parquet (data/assets/scripts/lib/stream_parquet.py, docstring of stream_to_parquet, lines 176-187: if the iteration raises, __exit__ aborts and nothing lands). The multipart finalisation itself is not read in this cell.
- Fails after data.parquet and before manifest.json: a PARTIAL PARTITION. It holds data.parquet and no manifest.json. Detection: LIST the partition prefix and find one object and no manifest.json. Whether a consumer refuses a manifest-less partition is NOT ESTABLISHED (no consumer reads account_dim).
- In every failed branch the rollback in section 6 applies to whatever keys exist.

## 6. Rollback

Rollback is per key. The keys this apply writes are the only keys it may touch:

1. s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/date=2026-10-12/data.parquet: delete the version(s) the apply created.
2. s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/date=2026-10-12/manifest.json: delete the version(s) the apply created.

Versioning on opal-data-cottonwood is Enabled (live read, get-bucket-versioning, Status Enabled). A plain DELETE on a versioned bucket adds a delete marker and keeps the noncurrent version, so the rollback must remove the version ids the apply created, not only add a marker. After rollback the prefix should again hold no objects, as read today.

No other key moves. The prefix is empty today (read in this cell). Nothing else in the gold home is written by this apply.

The rollback is an S3 delete. CLAUDE.md requires human confirmation for S3 deletes, so the rollback is an act for the issuer and Andrew to confirm, not for this cell.

## 7. Conditions

Before the apply:

1. Ledger first: an entry in org/critical_paths/change_management/ is opened at the start of the apply and closed at its completion (NEVER-2). This cell opens no entry: nothing is applied here.
2. Live bytes re-read at the moment of the apply: the prefix irpt/cottonwood/gold/account_dim/ must still hold no objects. If it holds any object, STOP and report; do not overwrite.
3. The adapter's tests and an import smoke at the pinned commit come first. Done in this cell at a1d871ec33: 7 passed (pytest, offline, no cache written); the import smoke loads the module, reads FIRM "cottonwood", TABLE "account_dim", 16 schema fields, and addresses s3://opal-data-cottonwood/irpt/cottonwood/gold/account_dim/date=2026-10-12. The adapter's sha256 equals the dry-run record's (a6b9f1fc750bcfa10d86484452877f375bcbb24b6fc4f864ce8580dd58867fcc).
4. No other table is written by the apply.
5. The applier's order adds the upload path described in section 1 and its own tests; it is not built here.

Questions for the CTO's half of the pair:

- Q1. Do the four dimension fields the Cottonwood silver does not carry (client_id, tax_status, opened_date, first_data_date) ship as nulls, with absent_fields as their coverage statement (999 nulls each in the dry run)? Or should the apply wait until the silver carries them?
- Q2. Is the household key (smallest non-sentinel Relationship ID; 223 distinct; 47 accounts with none) accepted as the table's household key for this partition?
- Q3. Is date=2026-10-12 the right partition, given that the adapter takes the date as an argument and computes none?

## 8. Not established

- The live counts: 999 accounts and 223 relationship ids are the round-103 dry-run measurements. Silver was not re-read in this cell.
- The coverage distribution (FULL, UNCLASSIFIED_HOLDINGS, PARTIAL_HISTORY counts) is not in the dry-run record and was not measured.
- Whether any consumer refuses a manifest-less partition (no consumer exists yet).
- The write sets of the holdings-performance role and of any human principal, and CloudTrail history for the prefix.
- The MFA-delete state of opal-data-cottonwood (versioning Enabled was read; MFA delete was not).
- Whether the 49F reporting-gold schedule is enabled in AWS: the cron is read from the fire-time record only, not from the live rule.
- The applier's identity, IAM role and entry point: none exists at HEAD.
- Whether the stream writer's multipart finalisation leaves any partial object on a mid-upload failure: the docstring is the only evidence read.
