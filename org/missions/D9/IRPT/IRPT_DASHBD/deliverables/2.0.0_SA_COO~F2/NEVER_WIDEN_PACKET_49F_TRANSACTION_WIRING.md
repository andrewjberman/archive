# NEVER-WIDEN PACKET -- the 49 Financial reporting-gold function: the TRANSACTION TABLE (the write prefix, the new bundle, a transaction-only dry run, the first one-day write and a bounded range backfill) (IRPT_DASHBD round 136, cells DB-f-2201, DB-f-2202, DB-f-2203)

**Author:** 2.0.0_SA_COO~F2. **Date:** 2026-10-16 ~22:1xZ. **STATUS: REVISION 0, DRAFT.** Section 2's handler pin, the build-only hash and the final test counts are filled when `DB-f-2201` is on the trunk; nothing below is a request to sign until the header reads REVISION 1.
**Ordered by:** 1.0.0_SA_CTO~DELL2, the round-135 analysis (`org/tier1_exec/1.0.0_SA_CTO/deliverables/CTO_ROUND_ANALYSIS_IRPT_DASHBD_F-SHIP_ROUND_135_20261016.md` @8d48df1751, msg 9837) and msg 9486 (the release order: 49 Financial first; the object kind is NEW, no reader exists): ruling 2 (the applier is `0.7.0_AE_CloudOps~IB2`), ruling 3 (the sid `WriteTheFiveGoldPrefixesOnly` stays and this packet states that the plan changes the statement's prefix list only; the sid is not a count).
**Two halves, one packet:** the COO half is `NEVER_WIDEN_49F_TRANSACTION_WIRING_COO_HALF.md` (this seat); the CTO half is `1.0.0_SA_CTO~DELL2`'s. Both bind to THIS FILE's sha256. A packet whose bytes differ is not covered. **Nothing is built, uploaded, applied or invoked until both halves are SIGNED on one sha256.**

## 1. The acts (six, in order; each has its own stop)

**Act 1 -- build and upload the new bundle.** The applier builds `irpt-49f-reporting-gold-lambda` with `infra/aws/lambda/ci/build-and-upload.sh investor-reporting irpt-49f-reporting-gold-lambda` (the entry key; the artifact key is read from the map, never typed). The build-only hash is in section 2; the real build must print the same base64 sha256 or STOP. The upload writes a NEW VERSION of the key in `opal-313476888478-lambda-artifacts` (versioned) and updates the entry's `artifact_sha256` only. **Rollback target: the current version `00dm6f4.vFnWIiIuxVafNVtxIh0zAEeh` (280,526 bytes, 2026-10-16T13:44:54Z).** The bundle gains two members and no other: `account_transaction.py` and `transaction_words.json` (the source-map entry, `DB-f-2203`); the handler changes (`DB-f-2201`).

**Act 2 -- ONE `safe-apply` of `infra/aws/terraform/investor-reporting/reporting-gold/`** (never a bare `terraform apply`, never `aws lambda update-function-code`). **The plan gate is exactly 0 to add, 2 to change, 0 to destroy:**

| address | what changes |
|---|---|
| `aws_iam_role_policy.irpt_reporting_gold` (change) | in the ONE statement `WriteTheFiveGoldPrefixesOnly` (sid kept; "Five" is a name, not a count: it already lists six prefixes) the `Resource` list gains exactly ONE entry, `arn:aws:s3:::opal-data-49financial/irpt/49financial/gold/account_transaction/*`, last. The action stays `s3:PutObject`. No read grant, no list grant, no other statement, no other value. |
| `module.irpt_reporting_gold.aws_lambda_function.this` (change) | the CODE only (the artifact version and its hash); memory 8,192, timeout 900, ephemeral storage 512, handler, runtime, role, the one layer and no environment stay exactly as they are |

Any other line, any other attribute, any destroy, STOPS the act. The schedule, its role and policy and the log group do not appear in the plan. `iam.tf` is byte-identical (a comment and an output description there still say "six gold tables": wording only, outside this plan).

**Act 3 -- a transaction-only DRY RUN, writing nothing.** ONE synchronous event `{"backfill": {"start": "<D>", "end": "<D>"}, "accounts": "population", "stages": ["transaction"], "dry_run": true}` for `<D>` = the newest landed returns day at the apply (2026-10-15 at packet time), `RequestResponse`, `--cli-read-timeout 0`. It reads the day's `fact_trn` partition, runs the producer and writes nothing. **Expected:** `stages` is `["transaction"]`; `transaction_rows` carries the day with a positive count; `transaction_failed` is `{}`; no object appears at the new prefix (it holds 0 objects before and after); Max Memory Used and duration inside 80 percent of the function's limits (6,553 MB, 720 s).

**Act 4 -- the first one-day WRITE** of the same event without `dry_run`. **Expected:** the prefix `irpt/49financial/gold/account_transaction/` holds exactly one `date=<D>/` partition (a `data.parquet` and a `manifest.json`) where it held 0 objects; the row count equals Act 3's; the file carries the 19 columns of contract 0.5.1 with the schema hash `ac652e2f71b18427b52f321858163768158f850ec173d1e592c7c3abe815bb6a`; every `business_date_claim` is `measured` or `inferred` and equals `inferred` exactly where `business_date` differs from `trade_date`; `flow_class` has no value outside the seven classes. The applier reads counts and word values only, never an account id or a figure.

**Act 5 -- the bounded RANGE backfill, transaction-only.** One event `{"backfill": {"start": "<D-24 trading days>", "end": "<D>"}, "accounts": "population", "stages": ["transaction"]}` (at most the handler's 25 trading days per invocation). **Expected:** one `date=` partition per trading day of the range at the new prefix, each with its own manifest, the same 19 columns; the returns, class, activity, lot and filled prefixes' object counts and newest days are unchanged before and after (counts compared). This is the CTO's question 2 below: the range is a proposal, not an assumption.

**Act 6 -- the receipt** with the counts, memory and duration of Acts 3 to 5, the checks, the first scheduled fire's reading (condition 6) and the words "new gold table account_transaction, no reader yet: nothing served moves".

**NOT in this packet:** any day earlier than the range of Act 5 (a later range, on the CTO's word); the Cottonwood and Inflection sides; the schedule; any reader; any change to a read or list grant; any delete of any object or version; the wording of `iam.tf`.

## 2. Pins (filled at the merge of DB-f-2201)

Code at the tree named in the applier's ledger on `box/dell2` (LOCAL). sha256 (first 12 hex) and bytes at packet time; the applier re-reads each and STOPS on a difference unless a later commit is named in its ledger entry. **Terraform root** `infra/aws/terraform/investor-reporting/reporting-gold/`: `locals.tf` `eb629c95b43d` (12,173; was `1063ebb77489`), `iam.tf` `a9b82429beeb` (8,002; unchanged), `lambda.tf` `a20ea4a0a21c` (4,557; unchanged), `main.tf` `782bb1348099` (1,616; unchanged), `schedule.tf` `6f92147a2a18` (5,573; unchanged; not in the plan). **Producer and words:** `account_transaction.py` `3b859c6d7440` (22,330) and `transaction_words.json` `996d7c304fdb` (85,309), pinned in the source-map entry at commits `acffc76bee...` and `ab96608480...` (full hashes in the entry). **Source map** `infra/aws/lambda/ci/lambda-source-map.json` `83b1eeacf73e` at packet time (a shared file; the entry `irpt-49f-reporting-gold-lambda` holds 24 files and 23 pins). **Handler** `reporting-gold/handler.py`: TBD at the merge of `DB-f-2201` (sha256 and bytes). **The build-only package** (`BUILD_ONLY=1`, nothing uploaded): base64 sha256 TBD, built by this seat at the final tree. The Inflection bundle pin is NOT this packet's: it is re-cut at the Inflection release (CTO ruling 4).

## 3. Live state, measured by this seat at packet time (read-only; the applier re-reads at the apply)

- **Function** `irpt-49f-reporting-gold-lambda`: PRESENT; CodeSha256 `JNTOivgNaJ8spRxoXSkXAYWhf1cLqXr350sTpH5ADg4=`; 280,526 bytes; 8,192 MB; timeout 900 s; ephemeral storage 512 MB; one layer (`irpt-performance-native-layer:1`); no environment; handler `handler.lambda_handler`, python3.12; last modified 2026-10-16T13:50:44Z. **Artifact key** `investor-reporting/irpt-reporting-gold-lambda.zip`: current VersionId `00dm6f4.vFnWIiIuxVafNVtxIh0zAEeh` (280,526 bytes, 2026-10-16T13:44:54Z), the prior `My0rI3fwtMCZYPDLqRhPgJ7QH9HrE8L3`; bucket versioning Enabled.
- **Role policy** `irpt-49f-reporting-gold-policy` on `irpt-49f-reporting-gold-role`: eleven statements by id (`ListExactlyTheDeclaredSilverPrefixes`, `ReadDeclaredSilverPartitionsOnly`, `ListExactlyTheSixGoldPrefixes`, `ReadTheSixGoldPrefixesOnly`, `WriteTheFiveGoldPrefixesOnly`, `ReadTheServedModelSeriesObjectOnly`, `ListExactlyTheHouseholdCrosswalkPrefix`, `ReadTheHouseholdCrosswalkOnly`, `ReadTheClassTableByKeyOnly`, `OwnLogStreamOnly`, `InvokeOwnFunctionOnly`). The write statement lists SIX resources today (filled report values, returns, class, activity, realized lots, unrealized lots), each under `opal-data-49financial/irpt/49financial/gold/`.
- **Schedule** `irpt-49f-reporting-gold-daily`: ENABLED, `cron(41 7 ? * MON-FRI *)` America/New_York (11:41Z in October). It keeps firing and is untouched.
- **The new prefix** `irpt/49financial/gold/account_transaction/`: 0 objects (to be re-read by count at the apply).
- **Open ledgers** read in every live worktree (91 trees) at the round-136 cut: none names this root. The applier re-reads at the apply and prints its denominator.

## 4. What each act changes in the world

- **Act 1:** a new version of one artifact key. **Act 2:** the role policy gains one write resource and the function's code is replaced; the next invocation, including the scheduled fire, runs the new code (see condition 6). **Act 3:** nothing is written. **Act 4:** ONE new partition at an EMPTY prefix. **Act 5:** up to 25 more NEW partitions at the same prefix; no existing key is overwritten. **Act 6:** reads only. Nothing served moves: no reader of the new table exists; the existing five tables, the filled report and the published series are not written by any act.

## 5. Writers of the changed properties, counted

The new prefix: ONE rule writes it (`emit_transactions`, calling the producer's `emit_transaction_day`, one PutObject statement of the role), entered by the scheduled fire's last stage, the full backfill's last stage and the transaction-only backfill. N = 1 per property. The write statement: ONE (`WriteTheFiveGoldPrefixesOnly`).

## 6. Both branches

- **Branch A:** as the acts state it. **Branch B (the write is denied):** Act 4 returns a failed day with an AccessDenied; nothing is written; the policy read-back is the first thing to read; STOP. **Branch C (the producer refuses the day):** Act 3 or 4 returns the day in `transaction_failed` with the producer's refusal text; nothing is written for that day; STOP and report the text (a refusal is the producer's own check of a mapping or a date, never to be worked around). **Branch D (the stage runs out of memory or time):** the function fails at the line; nothing is written; STOP and report the measured peak. **Branch E (the first scheduled fire after the apply overlaps or is slowed):** see condition 6. **Branch F (a repeated Act 4 or 5):** same keys, same bytes except the manifest's build time; acceptable.

## 7. Rollback, per key

- **The code:** the previous artifact version `00dm6f4.vFnWIiIuxVafNVtxIh0zAEeh` is the target: a new upload of those bytes as the current version (a copy of the old version over the key, no delete) and a `safe-apply`, by the applier with the CTO's word. The write grant reverts with the same apply (the one resource leaves).
- **The new partitions:** the prefix is NEW, so there is no prior version to restore: the rollback is the prefix's removal from the write list (the apply above) and, if Andrew rules the objects out, their deletion, which is Andrew's act and is never done here.

## 8. Conditions

1. **Ledger entry first,** bound to this packet's sha256: `deploy_ledger.py open --slug irpt-dashbd-49f-transaction-wiring-20261016`, the applier `0.7.0_AE_CloudOps~IB2`, legs git, build, terraform, dry run, first write, range backfill and receipt. Read every live worktree's `.open_deploys/` first and print the denominator.
2. **Naming gate:** the plan passes `.tools/naming-apply-gate.py` in plan mode with 0 REFUSE. **Live state re-read at the moment of the apply** and equal to section 3, else STOP. The plan's policy change must be the one resource; its function change must name `source_code_hash` and the artifact version only.
3. **Keep Acts 2 to 5 out of the daily fire window** (11:35Z to 12:00Z on a trading weekday: the gold fire runs about five minutes from 11:41Z, with its chained filled days after it).
4. **Each event only after the previous leg's after-read is recorded;** counts and words only, never an account id or a figure. **Stop at once** on a `Task timed out`, an `AccessDenied`, a Max Memory Used above 80 percent of the limit, or a count that differs from the act's expectation.
5. **No `update-function-code`, no bare `terraform apply`, no delete of any object or version, no change to the schedule.**
6. **The first scheduled fire after the apply is READ,** not assumed: its log must show the returns, class, lots and filled stages unchanged in their outputs and the new stage's line (`transaction rows=` or `TRANSACTION_SKIPPED`), with duration and Max Memory Used inside 80 percent of the limits. The transaction stage is the LAST stage and never raises, so a failure there cannot stop the earlier stages; a TIMEOUT could still cut it, which is why the fire is read. If the fire times out or exceeds 80 percent, the rollback of section 7 is taken with the CTO's word.
7. **The receipt** after Act 6 carries the phrase of Act 6.

## 9. Questions for the CTO's half

1. **One packet for the write prefix, the code update, the dry run, the first write and the bounded range?** Each act has its own stop; accept, or split.
2. **The range of Act 5:** the 25 most recent trading days through the newest landed day, one invocation, as proposed? A longer history (the gold holds 572 returns partitions; the producer's 14-day business-date window and the calendar are the only per-day limits) would be several invocations of 25 and is a later act on your word.
3. **Condition 6** reads the first scheduled fire as the acceptance of the scheduled path: accept, or ask for a hand fire.

## 10. Not established, and so not covered

Whether the stage's time and memory on a busy fire stay inside the limits (no run has reached it; Acts 3 and 4 measure one day, condition 6 measures a fire); the per-day row count of the 49 Financial transactions silver (read by the applier at Act 3, not asserted here); the lines whose trade date is not a trading day (296 of 3,354,885 in the round-132 census of the silver partition then read; the producer rolls them to the next trading day and stamps `inferred`, graded by the CVO's J2); any reader or page for the new table; the Cottonwood and Inflection sides.

-- 2.0.0_SA_COO~F2
