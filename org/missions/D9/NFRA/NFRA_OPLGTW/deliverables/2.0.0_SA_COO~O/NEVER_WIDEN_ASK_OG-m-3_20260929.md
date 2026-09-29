# Never-widen ask -- OG-m-3 (= OG-m-2b), the 49F gold dispatcher's chain-log classifier (NFRA_OPLGTW E11, part 2)

By: `2.0.0_SA_COO~O` (issuer), 2026-09-29. Order: `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-m-3.chain-log-classifier.md`.
Rulings: `1.0.0_SA_CTO~O` msgs 26305 (option (a)), 26360 (split: 2a now, 2b held on row Z-W15-S3), 26381 (2b unblocked:
gate `tf_local` @7610be987f, authority @a5aa8e92c8, entry `OPLGTW-LEGACY-READ-01` @e4ec197609). Read it rests on: OG-m-1
(`deliverables/0.9.0_WK_NFRA_OPLGTW~13/MARKER_STORM_READ.md`, merged @70f45e7675), rows Z-W13-S1, Z-W15-S3.
The bytes: the frozen candidate `deliverables/0.9.0_WK_NFRA_OPLGTW~15/og-m-2b_candidate_frozen.patch` (sha256
`600a4b6da9e75c65472dfdf10532cd85218f291c2b0b14b79d232275ca5ffbfe`, vs `8340c65376`) = the CTO pin
`deliverables/1.0.0_SA_CTO~O/OG-m-2b_candidate_vs_8340c65376.patch` @5b44ba518d, re-applied UNMODIFIED.

**Halves owed:** `1.0.0_SA_CTO~O` (CTO half) and `3.0.0_SA_CVO~O` (second, non-acting half), both against THIS file.
PHASE A (re-apply, tests, targeted PLAN) changes nothing in AWS and runs before them; PHASE B waits for both.

## 1. Blast radius -- the DELTA over OG-m-2a (deployed 2026-09-29T02:05:33Z, merged 40fcde8bf7)

**Repository write set (the order's `<paths>`):** `lambda_function.py` (the dispatcher), its test file (six tests; 2a's
three are among them), `advi_49f_floor.tf`, `lambda-source-map.json` (the build rewrites the artifact sha), the NEVER-2
entry + sentinel `nfra-oplgtw-chain-log-classifier`, the worker's deliverables, one channel file.

**The delta, measured** (8340c65376 + the frozen patch, diffed against CLOUD HEAD's 2a bytes, CR-insensitive):
- `lambda_function.py`: the stdout `_classify(stdout)` is REPLACED by `_classify(inv)`, which reads the chain log
  (`_chain_log_keys`, `_classify_log`); `CHAIN_LOG_BUCKET` / `CHAIN_LOG_PREFIX` read from the environment;
  `from datetime import datetime, timedelta`; the call site `_classify(inv)` plus a stdout-length context print; the
  docstring's two bullets. The 2a marker gate (`_marker_closure_status`, the SKIP branch) is byte-unchanged.
- `advi_49f_floor.tf`: the local `advi_49f_chain_log_prefix = "gold/advi/_logs/chain_"`; the `ReadTheChainLog` statement
  (`s3:GetObject` on `arn:aws:s3:::${local.advi_49f_bucket}/${local.advi_49f_chain_log_prefix}*`, rendered
  `arn:aws:s3:::opal-data-49financial/gold/advi/_logs/chain_*`); the env vars `CHAIN_LOG_BUCKET` and `CHAIN_LOG_PREFIX`
  on `module.advi_49f_gold_dispatch`; the SSM document's `aws s3 cp` line reads the local instead of the literal (a
  SOURCE refactor whose rendered command string is identical: `s3://${local.advi_49f_bucket}/gold/advi/_logs/chain_$${SUFFIX}.log`
  both before and after), and the marker statement's comment text.

**AWS write set (four keys, all on the dispatcher; the SSM document is NOT an apply target):**

| key | before (read 2026-09-29 ~02:2xZ) | after | rollback |
|---|---|---|---|
| `s3://opal-313476888478-lambda-artifacts/opal-assets/advi-49f-gold-dispatch.zip` | VersionId `3qOKR75Bkc4pDjaQxsSqy0h1.dYuTjqp` (IsLatest, 2026-09-29T01:54:50Z, 4,695 bytes), content-sha256 `KqlIoAJs98dXE1RoL9g0xBG0yQw9Mo3JiSFUaJO17qg=` (OG-m-2a) | a new version built from the committed source | `s3api copy-object` of VersionId `3qOKR75B...` back over the key WITH its `content-sha256` metadata |
| Lambda `advi-49f-gold-dispatch` code | `CodeSha256` `KqlIoAJs...`, LastModified 2026-09-29T02:05:33Z | the new artifact's sha | after the artifact rollback, the targeted `safe-apply`; verify `CodeSha256` reads `KqlIoAJs...` |
| Lambda `advi-49f-gold-dispatch` environment | `HOST_INSTANCE_ID`, `SSM_DOCUMENT_NAME`, `POLL_BUDGET_S` (no `CHAIN_LOG_*`) | + `CHAIN_LOG_BUCKET=opal-data-49financial`, `CHAIN_LOG_PREFIX=gold/advi/_logs/chain_` | revert the `.tf` commit on the worker branch; the same targeted `safe-apply` removes both |
| IAM inline policy `advi-49f-gold-dispatch-role` / `advi-49f-gold-dispatch-scoped` | 2a: ONE s3 statement, `s3:GetObject` + `s3:GetObjectVersion` on `arn:aws:s3:::opal-data-assets/schwab/08335338/meta/complete/*` (`dc.AC2.sh` at HEAD: exact 1 of 2, extra 0) | + `ReadTheChainLog`: `s3:GetObject` on `arn:aws:s3:::opal-data-49financial/gold/advi/_logs/chain_*`; no ListBucket | revert the `.tf` commit, `safe-apply -target=aws_iam_role_policy.advi_49f_gold_dispatch` back to 2a's single statement |

**Not touched, by name:** the marker writer (all four source copies and `opal-assets-silver-schwab`); `silver.tf` and the
S3 notification; the SSM document's RENDERED body (a plan that lists `aws_ssm_document.advi_49f_chain_dispatch` STOPS the
cell); the floor schedule cron(45 12 * * ? *), still the PRODUCTION trigger; the host `i-01003b035d2988dfb`; the chain
code under `s3://opal-data-49financial/_code/`; 2a's marker gate; every other resource in the `opal-assets` root (the apply
is `-target`ed to the module and the policy).

## 2. Writers and consumers of the chain-log prefix `gold/advi/_logs/chain_` (bucket `opal-data-49financial`)

Counted over the tracked tree (`infra/` and `data/`, 2026-09-29): a search for `gold/advi/_logs` and
`advi_49f_chain_log_prefix`, each hit classed from its code.
- **WRITERS: 1**, the SSM document `advi-49f-chain-dispatch` (`advi_49f_floor.tf:299` at HEAD), whose command uploads
  `/tmp/advi_49f_chain_${TS}.log` to the prefix before it exits. This act changes its SOURCE (literal -> the local) and
  not its rendered bytes.
- **CODE CONSUMERS today: 0.** Other hits are not code: `chain_49f_entrypoint.py:236` is a comment, and the
  `runners_49f/pins/pin_d*.json` files quote one log key as evidence. **After this act: 1**, the dispatcher (the consumer
  this act adds).
- **The local's references: exactly 3** (the SSM target, the `ReadTheChainLog` ARN, `CHAIN_LOG_PREFIX`), the count
  `OPLGTW-LEGACY-READ-01` admits; a fourth is refused by the gate.

N writers = 1, and the act adds a reader only; the writer's rule (one log per SSM invocation, keyed by the invocation's
start second) is what the classifier reads by.

## 3. Both branches, read from the classifier's rule as the frozen bytes build it (never predicted from input shape)

When the SSM invocation is terminal inside the 300 s poll, the dispatcher tries the keys `CHAIN_LOG_PREFIX + TS + ".log"`
for TS = the invocation's `ExecutionStartDateTime` (UTC, `%Y%m%dT%H%M%SZ`), then TS-1 s, then TS+1 s:
- the first readable key whose LAST line beginning `CHAIN ` is `CHAIN OK...` -> `OK`; `CHAIN REFUSED...` -> `REFUSED`;
  `CHAIN ABORT...` -> `ABORT`;
- a readable log with no `CHAIN ` line -> `UNKNOWN(chain_log=no terminal line, key=...)`;
- no readable key (absent, or AccessDenied without ListBucket) -> `UNKNOWN(chain_log=absent, key=<first tried>)`, and each
  failed key is printed with its error class;
- `CHAIN_LOG_BUCKET` or `CHAIN_LOG_PREFIX` unset -> `UNKNOWN(chain_log=unconfigured)`;
- in NO branch is `send_command` called a second time, and none retries; the "running past the poll budget" branch is
  unchanged (it classifies nothing). SSM stdout is printed as length context only, never graded.

**What changes in the SERVED world:** the dispatcher writes no gold output, so no served number moves. The change is the
dispatcher's own verdict: a completed chain whose stdout was cut at 24,000 characters reads `OK` from its log instead of
`UNKNOWN`. OG-m-1 measured 13 of 13 floor runs UNKNOWN with 4 of 5 sampled logs ending `CHAIN OK`. The 2a gate (1
accelerator dispatch per qualified date) and the floor are unchanged.

## 4. Naming authority

`OPLGTW-LEGACY-READ-01` @e4ec197609 in `NAMING_LEGACY_READS` (the laptop 1.0.0_SA_CTO's order, read-APPROVED 102538; the
`tf_local` kind @7610be987f; authority @a5aa8e92c8): local `advi_49f_chain_log_prefix`, occurrences 1, reference_count 3,
**cutoff 2026-10-06**. The prefix sits on ADVI_FIRMBKTS's live-remediation surface; this entry admits the existing key as a
legacy read and moves nothing; its migration stays ADVI_FIRMBKTS's.

## 5. NEVER-2

Slug `nfra-oplgtw-chain-log-classifier`; legs: the `tf-lambda` leg for `advi-49f-gold-dispatch` (`lambda-source-map.json`)
and one IAM leg (kind `verify`) for `aws_iam_role_policy.advi_49f_gold_dispatch`. Opened and committed before the upload;
closed with proofs; `dc.AC3.sh` grades the close. One-deployer census across every worktree before the act. Window: outside
12:15-13:30Z and 09:30-10:15Z.

## 6. Signatures

| half | seat | verdict | at bytes |
|---|---|---|---|
| CTO | `1.0.0_SA_CTO~O` | | |
| second | `3.0.0_SA_CVO~O` | | |
