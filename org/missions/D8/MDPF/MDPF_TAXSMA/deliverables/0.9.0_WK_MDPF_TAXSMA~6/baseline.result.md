# TX-p-1 -- the pre-change baseline, read only -- RESULT

**Worker:** `0.9.0_WK_MDPF_TAXSMA~6` | **Order:** `MDPF_TAXSMA.TO-TX-p-1` | **Branch:** `wk-mdpf_taxsma-1-6` |
**Worktree HEAD for every run:** `91b11ff0c957cb3470d0ae4a1513488b228e12b7` | **Date:** 2026-09-15 (all times UTC)

**Instruments.** One probe, `probes/tx_p_1.py`, one criterion per invocation. Each criterion's full output is in
`runs/AC<n>.txt` (the run the table cites). Every AWS call goes through the workspace `.tools/aws` shim and is
appended to `command_log.jsonl` before it runs. Each AWS criterion starts with `sts get-caller-identity`, and every
run returned Account `313476888478`, region `us-east-1`. No object body is kept in the repository: served JSON and
deployed zips live in `<worktree>/.scratch/tx_p_1/` only. Numeric values of the served `tax` node are printed
masked (zero / nonzero / null), never as amounts.

**Verdicts:** AC1-AC9 `PASS`; AC10 `FAIL` (1 non-read call, `ssm send-command`, which AC7 requires; row
`MDPF_TAXSMA-W6-S1`). The order stays open.

---

## AC1 -- the two served documents at their historical keys

Instrument: `s3api get-object` (bucket `opal-data-portal-v2`), SHA-256 over the downloaded bytes, JSON walk for
the `tax` node. Run 2026-09-15T21:28:54Z. Denominator: 2 of 2 keys read; 1 `tax` node in each (55 JSON nodes
walked per document).

| field | `platinum/mdpf/49financial/category-views.json` | `platinum/mdpf/global/category-views.json` |
|---|---|---|
| read at | 21:29:04Z | 21:29:09Z |
| VersionId | `I3.leHi_SZFkikM9W6754oFuR6vxsEmG` | `SImWn5XJ5opzUoQraNunob2Iy1gGbVQW` |
| LastModified (UTC) | Tue, 15 Sep 2026 13:50:50 GMT | Tue, 15 Sep 2026 13:50:51 GMT |
| ETag | `166473e3e56f04b3ef989b54c4c72caa` | `7af9411960a9549c0a72770adfc0f2fe` |
| bytes | 4,346 | 4,330 |
| SHA-256 | `c907a9fac921c96c620a38e4920fbe08495813ede6de36db7e70b4f32db9b0d9` | `da8e8e2cdc7266e60426d3fe3fbefafae65538037151f5c0062483dafc8d2d15` |
| top-level keys (10) | `_provenance, as_of, firm_id, nodes, schema_version, scope, scope_note, scope_set, sums, view_plane` | same 10 |
| `tax` node path | `$.nodes.SMA.children.ALT Strategies.members[1]` | same |
| `tax` node fields (5) | `aum` null; `display_name` 'Tax-Managed SMA'; `member_id` 'tax'; `served` true; `strategy_id` 'tax' | identical 5 fields and values |
| contract `wire_extension` document fields `taxsma_contract_version`, `taxsma_coverage` | ABSENT, ABSENT | ABSENT, ABSENT |
| contract `node_field` `coverage` on the tax node | ABSENT | ABSENT |

## AC2 -- deployed code SHA-256 vs each builder's package from HEAD

Instrument: `lambda get-function` (CodeSha256 plus the code download from its presigned location; the downloaded zip
hashes equal to CodeSha256, 2 of 2), each builder run at `--pin 91b11ff0c957cb3470d0ae4a1513488b228e12b7`, and
member-by-member SHA-256. Discrimination arm: the same comparator against a rebuild at the pin string each
deployed zip's own `BUILD_MANIFEST.json` records. Run 2026-09-15T21:47:26Z (a first run at 21:34:57Z gave identical
live and HEAD hashes; its control passed the 40-character commit instead of the recorded pin string, so it differed in
the single field `source_vintage` and nothing else, and was corrected). Denominator: 2 of 2 functions.

| | `mdpf-gold-lambda` | `opal-assets-mdpf-portal-publisher` |
|---|---|---|
| live CodeSha256 (read 21:47:35Z / 21:47:53Z) | `evIYCXURor4V++Ci4HsgwE8zIPZva/BAL+ICaLJIiAE=` | `7X50uR1HrGyeEHZ4FWyHBNwTxt/XXJq5GNmR/eFfWE0=` |
| LastModified / CodeSize / runtime | 2026-09-15T06:09:14Z / 835,383 / python3.11 | 2026-08-29T01:01:04Z / 53,286 / python3.12 |
| deployed in-zip `source_vintage` | pin `48b8671569`, commit `48b8671569b72efb4eca64ef41ded4de9c54e84c` | pin and commit `dc14d649bb3e8e7853ed9f648b08f7ca7017b7c8` |
| live env stamp | `MDPF_GOLD_COMMIT=48b8671569...` (equals the zip) | `MDPF_PUBLISHER_COMMIT=c0902245b0...` (NOT the zip's pin; row `MDPF_TAXSMA-W6-S3`) |
| HEAD build | rc 0, 849,624 bytes, b64 `0CcOB6JXsX6uQiseyu0GDJ4MKpEUXD9bI6dgMNUFxfU=` | rc 0, b64 `xif2dx9dH9hdPpV3Qo3/76Iyh2jYv/VY0rPok/9vLiI=` |
| **RESULT** | **MISMATCH** | **MISMATCH** |
| members (union) | 23: 20 identical, 3 differ (`BUILD_MANIFEST.json`, `mdpf_category_registry.py`, `mdpf_gold_consolidator.py`), 0 one-sided | 4: 2 identical (`lambda_function.py`, `partner_roster.json`), 2 differ (`BUILD_MANIFEST.json`, `artifact_types.json`), 0 one-sided |
| CONTROL rebuild at deployed pin | `48b8671569` -> **MATCH** | `dc14d649bb` -> **MATCH** |

Reading: both functions run exactly the bytes their recorded pins produce. HEAD's source is ahead of the gold Lambda in
two modules, and of the publisher in the derived artifact-type axis (`artifact_types.json`). `lambda_function.py`
is identical.

## AC3 -- the Gold floor schedule and the publisher's 13:50 UTC trigger

Instrument: `scheduler list-schedules --name-prefix <name>` (1 match each), then `scheduler get-schedule`.
Run 2026-09-15T21:29:11Z. Denominator: 2 of 2 schedules; 1 of 1 listed per prefix.

| | `mdpf-scheduled-floor` (read 21:29:27Z) | `opal-assets-mdpf-portal-publisher-daily` (read 21:29:38Z) |
|---|---|---|
| group | default | default |
| State | ENABLED | ENABLED |
| expression / timezone | `cron(30 13 * * ? *)` / UTC | `cron(50 13 * * ? *)` / UTC (encodes 13:50 UTC: YES) |
| flexible window | OFF | OFF |
| Target.Arn | `arn:aws:lambda:us-east-1:313476888478:function:mdpf-gold-lambda` | `arn:aws:lambda:us-east-1:313476888478:function:opal-assets-mdpf-portal-publisher` |
| Target.RoleArn | `arn:aws:iam::313476888478:role/mdpf-floor-scheduler-role` | `arn:aws:iam::313476888478:role/opal-assets-mdpf-portal-publisher-scheduler-role` |
| Target.Input | `{"floor":"mdpf-scheduled-floor","run_class":"production","source":"aws.events"}` | `{}` |

## AC4 -- the two roles' trust and every inline and attached policy

Instrument: `iam get-role`, `list-role-policies`, `get-role-policy`, `list-attached-role-policies`, `get-policy`,
`get-policy-version`. Run 2026-09-15T21:29:40Z. Denominator: 2 of 2 roles, trust 2 of 2, policy documents 5 of 5.
Full documents are printed verbatim in `runs/AC4.txt`; the hashes are SHA-256 over sorted-key compact JSON, first 16 hex.

| role | trust | inline | attached | boundary |
|---|---|---|---|---|
| `mdpf-gold-lambda-role` (read 21:29:50Z; created 2026-08-07) | lambda.amazonaws.com AssumeRole (`f3502e8666443cac`) | `mdpf-gold-scoped`, 10 statements (`5aa4e8929e3508f8`): 9 on `opal-data-assets` prefixes, 1 GetObject pair on `opal-data-portal-v2/json/...`, 1 on `opal-data-mdpf/mdpf/feeds/*`; **no statement names `opal-data-49financial`** | `AWSLambdaBasicExecutionRole` v1 (`8992968b3dd4b989`) | none |
| `opal-assets-mdpf-egress-publisher-role` (read 21:30:25Z; created 2026-07-28) | same (`f3502e8666443cac`) | `...-live-serve`, 2 statements (`8f9b763985c86228`): PutObject `opal-data-portal-v2/platinum/mdpf/*`, conditioned ListBucket; `...-scoped`, 4 statements (`5c9f4a164b17030f`): GetObject `opal-data-assets/portal/gold/mdpf/*`, PutObject `platinum/_staging/mdpf/*`, 2 conditioned ListBucket | `AWSLambdaBasicExecutionRole` v1 (`8992968b3dd4b989`) | none |

## AC5 -- `opal-data-49financial` controls

Instrument: `s3api get-bucket-versioning`, `get-bucket-encryption`, `get-public-access-block`, `get-bucket-policy`.
Run 2026-09-15T21:31:05Z. Denominator: 4 of 4 reads; 4 of 4 flags; Deny 1 of 1 statements (Allow 0 of 1).

- Versioning: `Enabled` (MFADelete not returned).
- Default encryption: 1 rule, SSE `AES256`, SSE-C blocked, BucketKey false.
- Public-access block: BlockPublicAcls true, IgnorePublicAcls true, BlockPublicPolicy true, RestrictPublicBuckets true.
- Bucket policy (`86fa75c33b785495`), 1 statement: **Deny `DenyForeignFirmPrincipals`**, Principal `*`, Action `s3:*`,
  Resource the bucket and `/*`, Condition `ArnNotLike aws:PrincipalArn` over 17 exempted ARNs: the pattern
  `role/*-49f-*`, 3 AWS service roles, 10 named roles and 3 IAM users (full list in `runs/AC5.txt`). Neither
  `mdpf-gold-lambda-role` nor `opal-assets-mdpf-egress-publisher-role` is among them. A role named
  `mdpf-49f-taxsma-role` would match `role/*-49f-*`.

## AC6 -- `mdpf-49f-taxsma-role` does not exist

Instrument: `iam get-role`. Run 2026-09-15T21:24:54Z (read 21:25:06Z). Denominator: 1 of 1 target, 1 of 1 control.
Result: rc 255, `An error occurred (NoSuchEntity) when calling the GetRole operation: The role with name
mdpf-49f-taxsma-role cannot be found.` Positive control: the same call on `mdpf-gold-lambda-role` returns rc 0, so
NoSuchEntity is an absence, not an access denial.

## AC7 -- the Gateway host's app source, `taxsma-workbook` route census

Instrument: host `i-07dccb1615503ac99` and root `/opt/opal-gateway`, read from `infra/aws/ec2/EC2_MANIFEST.json`
at HEAD; `ssm describe-instance-information` (Online, Amazon Linux, agent 3.3.4624.0); `ssm send-command`
`AWS-RunShellScript` with a 20-line read-only script (find, grep, wc, md5sum, stat); `ssm get-command-invocation`.
CommandId `686530ff-12ce-46ab-b5b2-d07ef6985eaa`, sent 21:36:04Z, Success, ended 21:36:06.903Z.

| measurement | value |
|---|---|
| file denominator (pruned: venv, .venv, `__pycache__`, node_modules, .git, site-packages) | **57 files, 43 of them `.py`** |
| files containing the string `taxsma-workbook` | **0 of 57** (grep errors 0) |
| `Route(` lines carrying `taxsma-workbook` | **0: not registered** |
| files containing `taxsma` in any case | 5 of 57 (context only) |
| positive control: `Route(` declaration lines found by the same census | 26; `Route("/health"` in `app/server.py`: 1 |
| `app/server.py` on the host | md5 `370d55689b57c33221317271f10d7bd3`, mtime 2026-09-09 18:43:58 +0000 |

The host's `server.py` equals the git blob at the manifest's `deployed_commit` 7bd89b5d71, but not the manifest's
recorded checksum (row `MDPF_TAXSMA-W6-S2`). `ssm send-command` is a Send verb (row `MDPF_TAXSMA-W6-S1`).

## AC8 -- the b00 `canonical_valuation` home and newest partition

Instrument: AST read of `b00_canonical_valuation.py` (`TABLE='canonical/canonical_valuation'`) and of its imported
`runner_common.py` (`GOLD_BUCKET='opal-data-49financial'`, `OUT_ROOT='gold/advi'`, emit key
`{OUT_ROOT}/{table}/date={asof}/data.parquet`; `_bucket_for()` sends OUT_ROOT-rooted keys to GOLD_BUCKET); then
`s3api list-objects-v2 --delimiter /` (read 21:31:47Z) and `s3api head-object` twice. Run 2026-09-15T21:31:35Z.

- Home: `s3://opal-data-49financial/gold/advi/canonical/canonical_valuation/`
- Partitions: **550** `date=` prefixes, oldest `2024-07-08`, **newest `2026-09-14`**, 0 non-date prefixes.
- Newest, confirmed by 2 of 2 heads: `date=2026-09-14/data.parquet` LastModified Tue, 15 Sep 2026 12:47:38 GMT,
  392,485 bytes, VersionId `iWFEZY7BJioBYcBbfqnUPtkrtkbxsl4_`; `manifest.json` same LastModified, 527 bytes.
  (2026-09-14 is the Monday before this Tuesday's read.)

## AC9 -- the MDPF Gold suite at the cell's HEAD

Instrument: `python -m pytest data/mdpf/scripts/gold/tests -q -rf` (Python 3.12.10, `-p no:cacheprovider`, no
bytecode written) plus `--co` for the collected count. Run 2026-09-15T21:26:29Z at HEAD 91b11ff0c9.

- 92 collected; **89 passed, 3 failed**, 0 errors, 0 skipped (`3 failed, 89 passed in 2.34s`).
- Failing ids (3 of 3):
  `test_global_fold_flag2.py::test_carry_beyond_window_absent_for_real`,
  `::test_carry_source_is_measured_never_interpolated`, `::test_carry_within_window_carries_and_labels`.
- Agrees with the cut measurement (92 / 89 / 3, all in `test_global_fold_flag2.py`) and with row `MDPF_TAXSMA-S1`.

## AC10 -- every AWS call in the command log is a read verb

Instrument: `command_log.jsonl`, the verb taken from each operation name; classifier self-test get-object READ,
put-object NON-READ, send-command NON-READ. Run 2026-09-15T21:47:59Z, over the log as it stood then.

- Denominator: **48 AWS calls** logged, 21:24:54Z to 21:47:53Z. Verbs: get 37, list 7, head 2, describe 1, **send 1**.
- Read-verb calls 47 of 48. **Non-read: 1 of 48**, `ssm send-command` at 21:35:56Z (criterion TXP1-AC7).
- **FAIL.** AC7's census cannot run without SendCommand, so AC7 and AC10 cannot both pass as written (row
  `MDPF_TAXSMA-W6-S1`). No mutating S3, IAM, Lambda, Scheduler or Terraform call appears in the log.
- Not covered by the log: the Gold test suite's own imports (the test folder has 0 `boto3`/`botocore` references);
  the builders call only `git`.

---

## Rows filed

| id | class / hazard | one line |
|---|---|---|
| `MDPF_TAXSMA-W6-S1` | BLOCKING / INERT | AC7 needs `ssm:SendCommand`, so AC10 cannot pass in the same cell as written |
| `MDPF_TAXSMA-W6-S2` | OBSERVATION / INERT | EC2_MANIFEST.json's opal-gateway checksums for server.py, config.py and audit.py match neither the host nor the blobs at its own deployed_commit |
| `MDPF_TAXSMA-W6-S3` | OBSERVATION / INERT | the live publisher's `MDPF_PUBLISHER_COMMIT` (c0902245b0) is not the pin its deployed zip was built from (dc14d649bb) |
