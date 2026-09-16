# NFRA_OPLGTW.TO-OG-c-2 -- result: refused at the plan; no deploy and no replay

**Worker:** `0.9.0_WK_NFRA_OPLGTW~4` | **Branch:** `wk-nfra_oplgtw-1-4b` (worktree `/c/tmp/wk-oplgtw-1-4b`, cut from `CLOUD`
@3f94e0a024) | **Spec:** PRD v0.2 C3/C6 @f0aa50dbc0 | **Decomposition:** v1 @8768f46770, cell `OG-c-2` |
**Status:** order left OPEN -- 3 of 11 criteria PASS, 8 FAIL.

## 1. Outcome

Vendoring and the pin move are done and committed (@271bab18dc). The deploy was **refused at the plan**:

- The only permitted apply route is `.tools/safe-apply.sh`, with no `-target`.
- That route applies the whole `opal-assets` root.
- The root's plan carries two rows outside `opal-assets-silver-schwab`, one of them an IAM policy change.
- The order's blast-radius bound makes that a BLOCKING row and no apply: row `NFRA_OPLGTW-W4-S5`.

So nothing was built, uploaded, applied or replayed. **No date was replayed for either master, and no record key or
VersionId exists to name.**

**Nothing is armed.** Read at ~12:50Z and unchanged by this worker:

- no ledger entry `nfra-oplgtw-og-c-2-producer` was opened;
- the artifact's latest S3 version is still `RigDVPxrZlvI49kyJJrOMk4vXnxEACzs` (2026-08-30T03:31:43Z);
- the function still runs `CodeSha256 /Uog2LDpLg42FrCU5MfTrEBaTFJTlVRY97tONxmjhVM=`, LastModified 2026-08-30T03:37:41Z,
  with `OPAL_BUILD_COMMIT 5c7b2a9a6b`;
- no marker was written.

## 2. The plan that stopped it

Command: `.tools/terraform.exe -chdir=infra/aws/terraform/opal-assets plan -out`, at 271bab18dc. The init was offline,
using `-plugin-dir` from the main workspace's `.terraform/providers` (hashicorp/aws 5.100.0, matching the lock file).
Result: `Plan: 0 to add, 3 to change, 0 to destroy.` (plan timestamp 2026-09-15T13:03:39Z; 210 resource_changes).

| row | change | source |
|---|---|---|
| `module.silver_converter["schwab"].aws_lambda_function.this` | env `OPAL_BUILD_COMMIT` `5c7b2a9a6b` -> `1f03a3f209` | this order's pin move |
| `aws_iam_role_policy.emitter` | Resource and the `s3:prefix` condition gain `portal/gold/mdpf/_staging/aggregate_aua/*` | @2740e4de8f, 0.7.0_AE_CloudOps, "STAGED-NOT-APPLIED ... apply held for the act's own window" |
| `module.emitter.aws_lambda_function.this` | env `AGGREGATE_PREFIX` `gold/mdpf_revamp/_aggregate_aua/` -> `portal/gold/mdpf/_staging/aggregate_aua/` | same commit |

The committed plan evidence is `plans/plan_pre_upload.json`. It carries the address and actions of every resource_change,
210 of 210. Attribute values were dropped, because the full `terraform show -json` carries every attribute of the root in
plain text.

## 3. What was done

1. **Vendoring:** `conversion_manifest.py` and `schwab_runtime.py` were written from `git show 1f03a3f209:data/assets/scripts/silver/<f>`.
   They are byte-equal (cmp) and LF in the index and the worktree. The other 9 modules `BUILD_MANIFEST.json` names were
   already equal, so 11 of 11 are equal (AC1).
2. **Pin:** `silver.tf` `silver_build_commit.schwab` moved `5c7b2a9a6b` -> `1f03a3f209`, with the rollback pin named in the
   comment (AC2).
3. **Pre-build gates:**
   - `import-closure-check.py`: `OK: import-closure -- 12 packaged .py file(s)`, rc 0.
   - `commit-gate.sh` on the two vendored files: `clean for 2 of 2`.
   - Commit 271bab18dc.
4. **The pre-upload plan** (section 2). It was run BEFORE any upload, so that a plan carrying foreign rows would stop the
   order with nothing armed. It did stop the order.

### Measured for the sign-off's conditions before the stop (none of them was reached as an act)

- **Condition 3 (botocore, before A1):**
  - The function runs `python3.11` runtime `python:3.11.mainlinev2.v31` (the CloudWatch `INIT_START` line, last 2 days; runtime
    ARN `...runtime:393e50a9...`).
  - Its only layer, `pandas-pyarrow-layer:1` (67,631,690 bytes, 3,000 members), carries **0** boto3 or botocore members.
  - So the runtime's own botocore is the client. Its version is not readable without executing code in the function.
  - The branch (a) or (b) would be decided by the record's `write_guard`, as W4-S2 states.
- **Condition 4 (the day's floor):**
  - `gold/advi/_logs/chain_20260915T124542Z.log` (VersionId `3eNJFWhmCUu_orz4If4TQ83BMOdrVHkq`) reads
    `CHAIN START date=2026-09-14` ... `CHAIN OK date=2026-09-14 wall=132.0s`.
  - This read is in the 49F bucket; the order's cross-firm bound reads otherwise (row W4-S8).
- **Replay candidate:**
  - Date 2026-09-14, 11 bronze objects per master (listed read-only).
  - The current markers are v1 (9 keys, no `closure`): `08242234` VersionId `Tsx9ccaDlBPOk_NxcXTLNw4EbQudxl_H`,
    `08335338` VersionId `TMi_xXeNS6OS606E7kW5nmr.ZZwdh9J6`, both `written_tables [dim_asset, fact_sec]`.

## 4. Criteria -- run exactly as the order writes them, `<WS>` = `/c/tmp/wk-oplgtw-1-4b`

| id | deciding output | rc | denominator |
|---|---|---|---|
| OGC2-AC1 | `VERDICT: PASS-OGC2-AC1` | 0 | 11 of 11 vendored modules equal to 1f03a3f209, CR 0 |
| OGC2-AC2 | `VERDICT: PASS-OGC2-AC2` (pin `1f03a3f209` names `1f03a3f20915c4ece1b7b09654b4d7a316e2bae6`) | 0 | 1 pin |
| OGC2-AC3 | `VERDICT: FAIL-OGC2-AC3 2 of 3 changed row(s) are outside opal-assets-silver-schwab: aws_iam_role_policy.emitter, module.emitter.aws_lambda_function.this` | 1 | 210 resource_changes, 3 changed, 7 families (0 rows for the 6 others) |
| OGC2-AC4 | `VERDICT: FAIL-OGC2-AC4 no ledger entry nfra-oplgtw-og-c-2-producer at HEAD and no sentinel commit -- no deploy was opened` | 1 | 1 entry sought, 0 found |
| OGC2-AC5 | `VERDICT: FAIL-OGC2-AC5 no build ran -- deploy/build.log absent; the live code is the pre-deploy artifact` | 1 | 1 function, 0 builds |
| OGC2-AC6 | `VERDICT: FAIL-OGC2-AC6 no deploy or replay occurred, so no deploy commit exists for the sign-off to precede` (both halves SIGNED at HEAD, cited @65e254cafe) | 1 | 2 of 2 halves present; 0 deploy commits |
| OGC2-AC7 | `VERDICT: FAIL-OGC2-AC7 no controlled replay ran (blocked before the deploy) -- 0 of 2 masters carry a replayed record` | 1 | 0 of 2 masters |
| OGC2-AC8 | `VERDICT: FAIL-OGC2-AC8 no controlled replay ran -- nothing to validate` | 1 | 0 records |
| OGC2-AC9 | `VERDICT: FAIL-OGC2-AC9 no controlled replay ran -- no VersionId to match` | 1 | 0 VersionIds |
| OGC2-AC10 | `VERDICT: FAIL-OGC2-AC10 no controlled replay ran -- there is no before/after to compare` | 1 | 0 silver objects |
| OGC2-AC11 | `VERDICT: PASS-OGC2-AC11` | 0 | 7 bucket values + 11 notification configurations + the EventBridge flag, all MATCH |

**A probe correction, stated.** The first AC6 run printed `half 1.0.0_SA_CTO: ABSENT or incomplete`. The probe had required
the literal token `ObjectCreated` inside each half, which the criterion does not ask for, and Half 2 names the consumer
by its target instead. The probe now grades the SIGNED heading and prints each half's content as context only. The verdict
did not change (FAIL, no deploy commit); only the reason is now accurate.

## 5. Rows filed (channel `INVESTIGATION_v1.md`)

| row | class | hazard | what |
|---|---|---|---|
| `NFRA_OPLGTW-W4-S5` | BLOCKING | INERT | the plan carries another seat's staged IAM and env change; no apply is permitted |
| `NFRA_OPLGTW-W4-S6` | OBSERVATION | INERT | Rule 13's `safe-deploy.sh` maps no `assets` tree and cannot grade a Lambda zip |
| `NFRA_OPLGTW-W4-S7` | OBSERVATION | INERT | the build rewrites `lambda-source-map.json`, which is outside the grant |
| `NFRA_OPLGTW-W4-S8` | OBSERVATION | INERT | sign-off conditions 4/5/7 need reads in `opal-data-49financial`, against the cross-firm bound; read once |
| `NFRA_OPLGTW-W4-S9` | OBSERVATION | INERT | the event replay also writes 2 run manifests, and would write a missing dim |

## 6. What un-blocks it

One of these:

- `0.7.0_AE_CloudOps` applies, or withdraws, the staged emitter change (@2740e4de8f) in its own window;
- the issuer amends the apply route.

Then, in order:

1. A fresh plan, read before any upload.
2. Build: `TMPDIR=<ws>/.scratch bash infra/aws/lambda/ci/build-and-upload.sh opal-assets opal-assets-silver-schwab`.
3. A second plan, then `safe-apply`. All under the ledger entry, committed first.
4. A read-only dry run of `convert_object` for the chosen date, to rule out a dim write.
5. The two event replays (`08242234` first; `08335338` after 13:00Z and after the day's `CHAIN OK`, while no lock is live).
   Use RequestResponse, `AWS_MAX_ATTEMPTS=1` and a long read timeout, so the CLI cannot re-invoke.

The probe already reads the evidence those acts leave (`deploy/`, `replay/`, `plans/plan_apply.json`).
