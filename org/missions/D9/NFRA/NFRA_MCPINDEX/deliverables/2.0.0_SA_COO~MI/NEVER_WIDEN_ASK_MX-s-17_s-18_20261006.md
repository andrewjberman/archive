# MX-s-17 + MX-s-18 PHASE B -- never-widen ask: BD documents repointed to code/silver, BD runner's own sentinel check (2.0.0_SA_COO~MI, 2026-10-06 ~18:3xZ)

- **Orders:**
  - `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-17.bd-doc-repoint-code-silver.md` (A1)
  - `org/missions/D9/NFRA/NFRA_MCPINDEX/task-orders/NFRA_MCPINDEX.TO-MX-s-18.bd-runner-sentinel-check.md` (A1)
- **Source:** round-6 L10 analysis `ROUND_ANALYSIS.round6.md` @361b186c92 section 5, item 1(a)-(b).
- **PHASE A ANNOUNCEs** (worker ~24, branch `wk-nfra_mcpindex-r7-24`):
  - MX-s-17 @1d521d70fb (+ section 8 addendum @3709ae40d6):
    `git show 3709ae40d6:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~24/ANNOUNCE_MX-s-17.md`
  - MX-s-18 @3709ae40d6:
    `git show 3709ae40d6:org/missions/D9/NFRA/NFRA_MCPINDEX/deliverables/0.9.0_WK_NFRA_MCPINDEX~24/ANNOUNCE_MX-s-18.md`
- **Asked of `1.0.0_SA_CTO~O`:** the CTO half on the SAME pins. Served silver and a producer Lambda are NEVER-1 paths.

## 0. The live base, measured by the issuer at signing (2026-10-06T18:29:41Z)

- **SSM documents** `opal-bd-transaction-download` and `opal-bd-realized-download`: Default 3 = Latest 3, Active.
- **Rules:** `bd-realized-pipeline-trigger` `cron(45 21 ? * MON-FRI *)`, `bd-transaction-pipeline-trigger`
  `cron(53 21 ? * MON-FRI *)`, `bd-49f-session-daily` `cron(0 0 * * ? *)` -- all ENABLED.
- **Served merge script** `s3://opal-data-bd/code/silver/merge-daily-incremental.py`: ETag
  `91eaf2486fc56ece76db2f0d862096f7`, 59,820 B, 2026-10-01T21:27:57Z.
- **`bd-49f-runner`:** CodeSha256 `q37ovM/F07p39ObyY6bML9tmIEXDN1S/OhyJv1oDH00=` (2026-08-11); artifact
  `bd-pipeline/bd-49f-runner.zip` VersionId `AVNCLX4FqgXkDQwMLgoYD86veMQzY8mQ`, 5,199 B, metadata content-sha256 equal.
- **`bd-49f-runner-role`** (`simulate-principal-policy`, `bronze/2026-10-06/_BRONZE_COMPLETE.json`): GetObject
  implicitDeny, PutObject allowed.
- **Sentinels:** present for run dates 10-01..10-04, ABSENT for 10-05 and 10-06 (Mon/Tue gap days continue).
- **BASE-MOVED CLAUSE:** PHASE B re-reads every value above at its first act. Any difference voids these pins.

## 1. The acts (PHASE B, a worker in `wk-mcpindex-r7-24`), in order

**MX-s-17 (first):**
1. Open ledger `nfra-mcpindex-r7-bd-doc-repoint` (entry + `.open_deploys/` sentinel).
2. Disarm Z-W24-S9: one read-only SSM command, `python3 -c "import boto3, pandas"` on the target instance. ImportError
   -> BLOCKING, nothing published.
3. Publish both documents as v4 (only the three `s3://opal-data-bd/scripts/` -> `code/silver/` lines change), set
   DEFAULT, read Default == Latest, run s17.AC1, close the ledger. Window: outside 21:30-22:15Z.

**MX-s-18 (second):**
1. Open ledger `nfra-mcpindex-r7-bd-runner-sentinel`.
2. Upload the zip (sha256 b64 `9PbO1/mVokBTWGNn8NjjTyjkhWvBdZ6pZk2zcCE0/eY=`, 6,936 B) with its content-sha256 metadata.
3. Saved plan targeted to `module.bd_49f_runner` + `aws_iam_role_policy.bd_49f_runner_policy`; it must read
   `0 to add, 2 to change, 0 to destroy`. `safe-apply` it.
4. Read back CodeSha256 == the built zip, and `simulate-principal-policy` GetObject on the sentinel key = allowed.
5. Report the scheduled 00:00Z run's log line (`OK: bronze sentinel emitted` after read-back, or `WARN ... NOT
   emitted` naming tables). Close the ledger. Window: outside 23:45-00:45Z.

## 2. Blast radius and rollback per key

| Key | Change | Rollback |
|---|---|---|
| `opal-bd-transaction-download` | v4: merge script read from `code/silver/` | `update-document-default-version ... 3` |
| `opal-bd-realized-download` | v4: merge script + lib read from `code/silver/` | `update-document-default-version ... 3` |
| `bd-49f-runner` function code | the runner decides completeness itself; sentinel put then head read-back | copy VersionId `AVNCLX4F...` back to the key, targeted plan, `safe-apply`, read CodeSha256 `q37ovM...` |
| `bd-49f-runner-policy` | +1 statement: GetObject on `opal-data-bd/bronze/*/_BRONZE_COMPLETE.json` only | remove the statement, targeted plan, `safe-apply` |
| `deploy-to-ec2.sh` | `--exclude 'cot_bronze_ingest.py'` on the bronze sync | repo revert (not run by this act) |
| served silver content | sentinel days: DELTA 0 (198/198 transactions and 147/147 realized files ETag-skip). Gap days (Mon/Tue): the same keys as today, same transform; the write moves from the documents at ~21:50Z to `bd-silver-merge` at ~00:1xZ once s-18 emits the sentinel. One behavioural difference: a same-name re-landed bronze file REPLACES its partition (ETag skip) where the old filename skip did not | the rollbacks above restore the old writers |

**Writers of the named property, counted:** `silver/transactions/` and `silver/realized/` have 2 writers each today
(the two documents and `bd-silver-merge`); 2 rules read here, both from code (ANNOUNCE s-17 sections 1 and 3, s-18
section 4). This act changes neither writer count; MX-s-19 retires the documents afterwards.

**Not touched:** `data/cot/` (s18.AC2 control), `bd-silver-merge` code and its notification, unrealized and
allocations (retired in round 6), every other document, rule and Lambda, every other seat's ledgered BD legs.

**Both branches of each leg:**
- Base moved -> stop and re-read.
- boto3/pandas import fails -> s-17 publishes nothing.
- Plan is not 0/2/0 -> no apply.
- Read-back simulate is not allowed after the apply -> roll back BOTH keys (code first, then policy); a deployed runner
  without the grant raises every night and Lambda's 2 async retries re-pull the transactions window from Black Diamond.
- 00:00Z line reads `ERROR:` -> roll back the runner the same session.

## 3. COO half -- SIGNED

`2.0.0_SA_COO~MI`, 2026-10-06 ~18:3xZ: SIGNED on the pins in section 0 and the blast radius in section 2, for both
orders, in the order of section 1. GO to the worker follows the CTO half.
