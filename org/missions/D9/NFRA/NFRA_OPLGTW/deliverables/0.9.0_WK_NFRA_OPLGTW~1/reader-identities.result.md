# NFRA_OPLGTW.TO-OG-i-2 -- result (0.9.0_WK_NFRA_OPLGTW~1)

**Outcome: APPLIED. The data role, the catalog role, the Gateway's one assume statement and both secrets are live.
The ledger is CLOSED. 16 of 16 mechanical criteria PASS by output.** Branch `wk-nfra_oplgtw-1-1c`, worktree
`/c/tmp/wk-oplgtw-1-1c`, base `5503d92f88`.

## What happened, in order (UTC, 2026-09-16)

1. `TREE-OK` on `wk-nfra_oplgtw-1-1c` @5503d92f88. `.tools/terraform.exe` and the halt-gate session file were
   provisioned by the issuer; this worker neither wrote nor committed either one. `.venv-og` was built with the
   order's command, rc 0.
2. Pre-reads 18:0xZ. `opal-data-assets` default encryption is `AES256` with SSE-C blocked, so no KMS grant is
   needed. The bucket policy has 2 statements (`DenyParquetUnderBronze17a`, `AllowMdpfPortalCloudFrontOACRead`),
   neither of which touches these roles. Both role names read `NoSuchEntity`. `opal-gateway-role` held 9 inline
   policies plus `AmazonSSMManagedInstanceCore`. Every silver and completion prefix lists objects.
3. `schwab_reader_iam.tf` written. `terraform fmt -check` rc 0, `init` rc 0, `validate` rc 0. Plan
   18:03:35Z..18:03:49Z rc 0: `Plan: 10 to add, 0 to change, 0 to destroy.` The plan was redacted into
   `og_i2.plan.json` (81 resource_changes: create 10, no-op 71; sensitive values masked).
4. Halt gate, bounded, without `HALT_ACK`: **rc 1**. It found 18 routine pending messages to the issuer
   `2.0.0_SA_COO~O`. This worker reviewed all 18 subjects: none is STOP class, and none concerns this apply. The
   gate did not return rc 2.
5. The ledger `nfra-oplgtw-og-i-2-reader-identities` was opened with legs L1-L4 and **committed @9efbe7a275
   (18:19:45Z)** together with the .tf, the probes, the plan and rows W1-S9/S10. All of this happened BEFORE the
   apply.
6. **The ONE guarded safe-apply run**, `probes/og_i2_act.py apply` under `HALT_ACK=1`, ran
   18:22:50.350290Z..18:25:35.796609Z. The bucket policy was read before at 18:22:49.351537Z. The in-run guard
   judged the plan printed in this run at 18:25:32.274376Z: exactly the ten creates, `other_headers []`,
   `Plan: 10 to add, 0 to change, 0 to destroy.` It answered **yes**. Result: **rc 0**,
   `Apply complete! Resources: 10 added, 0 changed, 0 destroyed.` The bucket policy was read again after, at
   18:25:36.032414Z. No `-target`, no saved planfile, no retry.
7. The alias-key secret received its FIRST value (`og_i2_act.py put-alias-key`): VersionId
   `8a580052-fd2d-480b-801c-355de8c08b4a`, `AWSCURRENT`. The read-back shape is
   `{current_version: v1, keys: [v1]}`, and the key decodes to 32 bytes. The value was not recorded. Supplementary
   check: OG-z-3's `app/account_ref.py parse_keyring` accepted it, and a synthetic account id minted a reference of
   the form `acr_v1_...` (33 characters).
8. Ledger legs L1-L4 were closed with proofs and the entry CLOSED, then **committed @6b7e7b17c1 (18:32:01Z)**
   before every read that grades the act. The committed files: evidence/og_i2/apply.json, apply.log,
   bucket_policy_pre/post.json, alias_key_put.json and row W1-S11.
9. The sixteen criteria ran 18:33:13Z..18:4xZ, each under `timeout 120`: **16 of 16 PASS**. AC10 took two runs;
   see "Probe defect" below.

## Identities (read back live; names only, no values) -- also in SCHWAB_IDENTITIES.json

| object | ARN / name |
|---|---|
| data role | `arn:aws:iam::313476888478:role/opal-mcp-emp-menachem-schwab-read` (created 2026-09-16T18:25:35Z), inline `opal-mcp-emp-menachem-schwab-read-policy`, 0 attached |
| catalog role | `arn:aws:iam::313476888478:role/opal-mcp-schwab-catalog-read` (created 2026-09-16T18:25:35Z), inline `opal-mcp-schwab-catalog-read-policy`, 0 attached |
| Gateway statement | inline `opal-gateway-assume-schwab-readers` on `opal-gateway-role`, one statement, **Sid `AssumeSchwabReaderRoles`** |
| ExternalIds | secret `opal/mcp/opal-gateway-schwab-reader-external-ids` (fields `data_read`, `catalog_read`); resource-policy Sid `GatewayReadsSchwabReaderExternalIds` |
| alias key | secret `opal/mcp/opal-gateway-schwab-account-ref-key` (the name for `SCHWAB_ACCOUNT_REF_SECRET_ID`); resource-policy Sid `GatewayReadsSchwabAccountRefKey` |

The mechanisms the order does not name are recorded as row `NFRA_OPLGTW-W1-S10`: Terraform-generated ExternalIds, an
out-of-band key value, and read grants carried as secret resource policies. Supplementary on-host read of the
alias-key secret: the instance role got the VersionId (rc 0), and no value was printed.

## Ledger legs (entry `org/critical_paths/change_management/20260916T1818Z_nfra-oplgtw-og-i-2-reader-identities_deploy_completion.md`)

| leg | what | proof |
|---|---|---|
| L1 | declaration committed before the apply | `9efbe7a275` 18:19:45Z < apply start 18:22:50.350290Z |
| L2 | the apply | safe-apply rc 0, `Apply complete! Resources: 10 added, 0 changed, 0 destroyed.`, guard yes |
| L3 | bucket policy unchanged | PRE and POST sha256 `9846f8dbffdf7ed02c3e4c3aa9825d39423d97209221c05b1b5c7ae642177528`, identical |
| L4 | alias-key first value | VersionId, AWSCURRENT, shape v1 / 32 bytes |

## Criteria (all under `timeout 120`)

| id | verdict line | deciding measurement |
|---|---|---|
| OGI2-AC1 | `PASS-OGI2-AC1` | plan 9 of 9: creates == the ten, 0 non-create changes of 81, two roles, the assume policy on `opal-gateway-role`, alias-key secret and its Gateway-only GetSecretValue policy. Applied readback 7 of 7: one statement, Sid `AssumeSchwabReaderRoles`, Resource == the two ARNs, ExternalIds == the two dedicated ones, Tax SMA ExternalId absent |
| OGI2-AC2 | `PASS-OGI2-AC2` | 10 of 10: all 5 resource blocks of `taxsma_gateway_iam.tf` no-op (including `gw_assume_emp` = `opal-gateway-assume-emp-roles` and both alyssa roles), 4 of 4 alyssa addresses no-op, 0 changes outside the ten creates |
| OGI2-AC3 | `PASS-OGI2-AC3` | document 11 of 11 (2 Allow + 4 Deny; reads on the 6 object ARNs; ListBucket StringLike on the 6 forms; Deny NotAction, Deny reads NotResource, Deny other buckets, Deny StringNotLike; no write) + simulation 9 of 9 |
| OGI2-AC4 | `PASS-OGI2-AC4` | document 11 of 11 over the 2 completion prefixes + simulation 8 of 8 |
| OGI2-AC5 | `PASS-OGI2-AC5` | 15 of 15: each trust has one statement, Principal only `opal-gateway-role`, one StringEquals sts:ExternalId equal to its own secret field, not the Tax SMA one; the two ExternalIds differ |
| OGI2-AC6 | `PASS-OGI2-AC6` | 7 of 7 on host: Tax SMA ExternalId -> AccessDenied for both roles; dedicated -> assumed-role ARN for both |
| OGI2-AC7 | `PASS-OGI2-AC7` | 7 of 7: data role GetObject rc 0 (content_length 875257, body to /dev/null); control under the bare instance role AccessDenied |
| OGI2-AC8 | `PASS-OGI2-AC8` | 7 of 7: data role GetObject on `meta/complete/` AccessDenied; same session silver GetObject rc 0 |
| OGI2-AC9 | `PASS-OGI2-AC9` | 7 of 7: data role GetObject on a `bronze/` key (exists, HeadObject 200) AccessDenied; same-session control rc 0 |
| OGI2-AC10 | `PASS-OGI2-AC10` | 7 of 7: PutObject (0-byte body) under `silver/dim_position/` AccessDenied; key absent before and after (HeadObject 404) |
| OGI2-AC11 | `PASS-OGI2-AC11` | 7 of 7: ListBucket prefix `schwab/08242234/meta/` AccessDenied, empty prefix AccessDenied, control `silver/dim_position/` rc 0 |
| OGI2-AC12 | `PASS-OGI2-AC12` | 7 of 7: from a data-role session, AssumeRole on the catalog role, on itself and on `opal-mcp-emp-alyssa-read` all AccessDenied |
| OGI2-AC13 | `PASS-OGI2-AC13` | 6 of 6: catalog role GetObject on the `meta/complete/` key rc 0 (content_length 853) |
| OGI2-AC14 | `PASS-OGI2-AC14` | 7 of 7: catalog role GetObject on the silver key AccessDenied; same-session completion GetObject rc 0 |
| OGI2-AC15 | `PASS-OGI2-AC15` | 5 of 5: pre 18:22:49.351537Z <= start, post 18:25:36.032414Z >= end, apply completed, sha256 before == after; live now also equal |
| OGI2-AC16 | `PASS-OGI2-AC16` | 7 of 7: the two labelled sections below exist once each and are distinct; simulation section carries simulate-principal-policy decisions and no SSM command id; live section cites AC6..AC14 and 11 distinct SSM command ids. The first AC16 run (18:48:34Z) FAILED 6 of 7, because the simulation body named its instrument only in its header. The body now names it; the probe was not changed |

Keys named (no bytes kept): the silver key read in AC7 and denied in AC14 is
`schwab/08242234/silver/dim_position/date=2024-05-24/data.parquet`. The completion key is
`schwab/08242234/meta/complete/date=2026-08-31.json`. The outside key is
`schwab/08242234/bronze/acc/20240116/CRS20240116.ACC`. The write-denial key is
`schwab/08242234/silver/dim_position/og-i2-denial-probe-<utc>.txt`, and it never existed.

## POLICY SIMULATION RESULTS (iam simulate-principal-policy -- modelled, NOT exercised)

Instrument: `iam simulate-principal-policy` (PolicySourceArn = the role ARN, one action and one resource per call,
`s3:prefix` supplied as a context entry for ListBucket). These are the APPLIED-plane model: IAM's policy simulator
evaluated against the live role policies. Nothing here
was called. Files `evidence/og_i2/simulation_AC3.json` and `evidence/og_i2/simulation_AC4.json`.

OGI2-AC3, data role `opal-mcp-emp-menachem-schwab-read`, read 2026-09-16T18:33:31.946721Z, 9 of 9 as expected:

| action | resource | s3:prefix | decision |
|---|---|---|---|
| s3:GetObject | silver `dim_position/date=2024-05-24/data.parquet` | - | allowed |
| s3:GetObjectVersion | same | - | allowed |
| s3:GetObject | `meta/complete/date=2026-08-31.json` | - | explicitDeny |
| s3:GetObject | `bronze/acc/20240116/CRS20240116.ACC` | - | explicitDeny |
| s3:PutObject | silver key | - | explicitDeny |
| s3:DeleteObject | silver key | - | explicitDeny |
| s3:ListBucket | `opal-data-assets` | `schwab/08242234/silver/dim_position/` | allowed |
| s3:ListBucket | `opal-data-assets` | `schwab/08242234/meta/` | explicitDeny |
| sts:AssumeRole | catalog role | - | explicitDeny |

OGI2-AC4, catalog role `opal-mcp-schwab-catalog-read`, read 2026-09-16T18:33:38.327687Z, 8 of 8 as expected:

| action | resource | s3:prefix | decision |
|---|---|---|---|
| s3:GetObject | `meta/complete/date=2026-08-31.json` | - | allowed |
| s3:GetObjectVersion | same | - | allowed |
| s3:GetObject | silver `dim_position/date=2024-05-24/data.parquet` | - | explicitDeny |
| s3:GetObject | `meta/backfill-status.json` | - | explicitDeny |
| s3:PutObject | completion key | - | explicitDeny |
| s3:ListBucket | `opal-data-assets` | `schwab/08242234/meta/complete/` | allowed |
| s3:ListBucket | `opal-data-assets` | `schwab/08242234/silver/dim_position/` | explicitDeny |
| sts:AssumeRole | data role | - | explicitDeny |

A simulation is not proof of the live boundary; the section below is.

## LIVE EXERCISED RESULTS (Gateway host i-07dccb1615503ac99 via SSM, instance role -- exercised)

Each arm ran `AWS-RunShellScript` on the Gateway host under `assumed-role/opal-gateway-role/i-07dccb1615503ac99`.
The ExternalIds were read ON the host from their secret; nothing but rc and error class was printed. Files
`evidence/og_i2/live_AC<n>.json`.

| criterion | SSM command id | start (UTC) | host lines that decide |
|---|---|---|---|
| OGI2-AC6 | `7df971d0-8137-49e9-94cc-12efc89c4677` | 18:34:57.796795Z | `ASSUME_TAXSMA_data rc=254 err=(AccessDenied)`; `ASSUME_DEDICATED_data rc=0 ... assumed-role/opal-mcp-emp-menachem-schwab-read/...`; `ASSUME_TAXSMA_catalog rc=254 err=(AccessDenied)`; `ASSUME_DEDICATED_catalog rc=0 ... assumed-role/opal-mcp-schwab-catalog-read/...` |
| OGI2-AC7 | `5b0f4595-3a5d-4551-b44d-605ea0f6044e` | 18:35:09.170080Z | `GET_SILVER_AS_DATA_ROLE rc=0 content_length=875257 bytes_kept=0`; `GET_SILVER_AS_INSTANCE_ROLE_CONTROL rc=254 err=(AccessDenied)` |
| OGI2-AC8 | `08e07a31-d5ec-4172-bb7c-1ca557d22cb2` | 18:35:18.870672Z | `GET_TARGET rc=254 err=(AccessDenied)`; `GET_CONTROL rc=0 content_length=875257` |
| OGI2-AC9 | `f1722ea0-081d-4ba0-8c74-b0c57ad0b8dc` | 18:36:13.351450Z | `GET_TARGET rc=254 err=(AccessDenied)`; `GET_CONTROL rc=0 content_length=875257` |
| OGI2-AC10 | `6357fd26-440b-4f53-8c02-83b7107f38db` | 18:38:52.682838Z | `EMPTY_BODY bytes=0`; `PUT rc=254 err=(AccessDenied)`; key HeadObject 404 before and after |
| OGI2-AC11 | `da0d0626-4b73-473c-a726-cb68a4450726` | 18:36:31.031612Z | `LIST_OUTSIDE rc=254 err=(AccessDenied)`; `LIST_NO_PREFIX rc=254 err=(AccessDenied)`; `LIST_CONTROL rc=0 key_count=1` |
| OGI2-AC12 | `354063f6-aeb2-41e6-862d-5ade0d37b055` | 18:36:39.834730Z | `CHAIN_CATALOG rc=254 err=(AccessDenied)`; `CHAIN_SELF rc=254 err=(AccessDenied)`; `CHAIN_ALYSSA_READ rc=254 err=(AccessDenied)` |
| OGI2-AC13 | `f505f83f-329e-41f3-abbc-7934ce712619` | 18:36:50.529070Z | `GET_COMPLETE rc=0 content_length=853 bytes_kept=0` |
| OGI2-AC14 | `14418e92-50e0-44e0-90f3-7d285e04cc29` | 18:37:00.406254Z | `GET_TARGET rc=254 err=(AccessDenied)`; `GET_CONTROL rc=0 content_length=853` |
| supplementary | `c58bb0b2-cea9-4556-8ef0-270e8091c61d` | 18:40:34Z | `ALIAS_KEY_SECRET_READ rc=0 version_id=8a580052-...` (the Gateway reads the alias-key secret through its resource policy) |
| AC10 first run (probe defect) | `bdd0b476-eab0-48d5-8200-1a331890d76c` | 18:36:23.347769Z | `PUT rc=252 err=` -- see below |

## Probe defect in AC10, recorded rather than hidden

The first AC10 run, at 18:36:21Z, printed `VERDICT: FAIL-OGI2-AC10`. `aws s3api put-object --body /dev/null` exited
**252**, which is the AWS CLI's own argument-handling exit, not an AWS answer, and no error class was printed. The
key was HeadObject 404 before and after, so nothing was written. The defect was in this worker's harness, not in the
role. The probe now passes a 0-byte `mktemp` file and prints that file's size. The re-run at 18:38:51Z printed
`PUT rc=254 err=(AccessDenied)` with the key absent before and after, and PASS. The probe change rides the
evidence commit. No other arm was re-run.

## comp-iam re-run after the apply

`.tools/comp-iam service opal-gateway`, 2026-09-16T18:4xZ, rc 0, **PLANE DESIRED** (Terraform; it does not read live
AWS, and says so). It scanned 3 trees (474 `.tf` files): 396 policy blocks attached, 29 NOT ATTACHED, 13 standalone,
and 6 deny statements unparsed. For `opal-gateway-role` it lists **29 operations**: 14 UNGRANTED,
13 UNRESOLVABLE-RESOURCE and 2 GRANTED-ACTION/UNGRANTED-RESOURCE. **None is `sts:AssumeRole`.** No Gateway source
calls the reader roles yet (that is a later cell), so comp-iam has no operation to match this cell's grant against.
Its `secretsmanager:GetSecretValue` row is UNRESOLVABLE-RESOURCE, and it does not model secret resource policies.
The APPLIED and EXERCISED planes for this cell are AC3-AC5 (live documents and 17 simulations) and AC6-AC14 (nine
on-host exercises).

## Rows filed this run

- `NFRA_OPLGTW-W1-S9` (OBSERVATION, INERT) -- in WARN mode, safe-apply's naming limb prints REFUSE for the C6 role
  names. ENFORCE would stop this apply.
- `NFRA_OPLGTW-W1-S10` (OBSERVATION, INERT) -- the three mechanisms the order does not name: Terraform-generated
  ExternalIds in a secret, the alias-key value written out-of-band, and the read grants as secret resource policies.
- `NFRA_OPLGTW-W1-S11` (OBSERVATION, INERT) -- W1-S9 undercounted; there are three REFUSE verdicts, the third on the
  Gateway policy name.

## Interpreter

`.venv-og` was built this run with `py -3.12 -m venv --system-site-packages .venv-og` and
`pip install -r infra/aws/ec2/opal-gateway/requirements.txt msal moto pytest`, rc 0. Python 3.12.10, boto3 1.42.54,
botocore 1.42.97. botocore/boto3/urllib3 loggers are held at INFO in both probes (row W3-S26).

## pip freeze (.venv-og)

318 lines, captured 2026-09-16T18:4xZ.

```text
aiobotocore==3.7.0
aiohappyeyeballs==2.6.2
aiohttp==3.14.1
aioitertools==0.13.0
aioquic==1.2.0
aiosignal==1.4.0
aiosqlite==0.22.1
alabaster==0.7.16
annotated-doc==0.0.4
annotated-types==0.7.0
anthropic==0.84.0
anyio==4.12.1
argon2-cffi==25.1.0
argon2-cffi-bindings==25.1.0
asgiref==3.11.1
attrs==26.1.0
av==18.0.0
awscli==1.44.44
awscrt==0.31.3
awscurl==0.39
awswrangler==3.11.0
babel==2.18.0
bcrypt==5.0.0
beautifulsoup4==4.14.3
blinker==1.9.0
boto3==1.42.54
botocore==1.42.97
brotli==1.2.0
cachetools==5.5.2
catboost==1.2.10
certifi==2026.1.4
cffi==2.0.0
charset-normalizer==3.4.4
# Editable install with no version control (click==8.3.1)
-e c:\users\andrewberman\desktop\worktrees\comp-learns\task-002\ds-b\click-src
colorama==0.4.6
colorclass==2.2.2
coloredlogs==15.0.1
ConfigArgParse==1.7.5
configparser==7.2.0
confuse==2.0.1
contourpy==1.3.3
coverage==7.13.5
cryptography==48.0.1
ctranslate2==4.8.1
curl_cffi==0.13.0
cycler==0.12.1
Cython==3.2.4
datasketch==1.10.0
defusedxml==0.7.1
desert==2022.9.22
distro==1.9.0
docker==7.1.0
dockerd==1.0.0
docstring_parser==0.17.0
docutils==0.18.1
duckdb==1.2.2
easygui==0.98.3
et_xmlfile==2.0.0
exchange_calendars==4.13.2
fastapi==0.135.1
faster-whisper==1.2.1
feedparser==6.0.12
filelock==3.25.2
finnhub-python==2.4.27
Flask==3.1.3
flatbuffers==25.12.19
fonttools==4.63.0
frozendict==2.4.7
frozenlist==1.8.0
fsspec==2026.6.0
graphifyy==0.8.24
graphviz==0.21
greenlet==3.3.2
griffe==2.0.0
griffecli==2.0.0
griffelib==2.0.0
h11==0.16.0
h2==4.3.0
hdbscan==0.8.41
hf-xet==1.4.0
hpack==4.2.0
html5lib==1.1
httpcore==1.0.9
httptools==0.8.0
httpx==0.28.1
httpx-sse==0.4.3
huggingface_hub==1.6.0
humanfriendly==10.0
hyperframe==6.1.0
idna==3.11
imageio-ffmpeg==0.6.0
imagesize==2.0.0
iniconfig==2.3.0
itsdangerous==2.2.0
Jinja2==3.1.6
jiter==0.13.0
jmespath==1.1.0
joblib==1.5.3
jsonpatch==1.33
jsonpointer==3.0.0
jsonschema==4.26.0
jsonschema-specifications==2025.9.1
kaitaistruct==0.11
kiwisolver==1.5.0
korean_lunar_calendar==0.4.0
kuzu==0.11.3
langchain==1.2.12
langchain-anthropic==1.3.4
langchain-core==1.2.18
langgraph==1.1.2
langgraph-checkpoint==4.0.1
langgraph-checkpoint-sqlite==3.0.3
langgraph-prebuilt==1.0.8
langgraph-sdk==0.3.11
langsmith==0.7.17
ldap3==2.9.1
libclang==18.1.1
libcst==1.8.6
llvmlite==0.47.0
lxml==6.0.2
magika==0.6.3
markdown-it-py==4.0.0
markdownify==1.2.3
markitdown==0.1.7
MarkupSafe==3.0.3
marshmallow==4.3.0
marshmallow-oneofschema==3.2.0
# Editable install with no version control (massive==0.0.0)
-e c:\users\andrewberman\downloads\client-python-master\client-python-master
matplotlib==3.11.1
mcp==1.28.0
mdurl==0.1.2
mitmproxy==12.2.3
mitmproxy-windows==0.12.9
mitmproxy_rs==0.12.9
mmh3==5.2.1
model2vec==0.8.2
more-itertools==11.0.2
moto==5.2.3
mpmath==1.3.0
msal==1.38.0
msgpack==1.1.2
msoffcrypto-tool==6.0.0
multidict==6.7.1
multitasking==0.0.12
mypy_extensions==1.1.0
narwhals==2.24.0
networkx==3.6.1
numba==0.65.1
numpy==2.4.2
olefile==0.47
oletools==0.60.2
onnxruntime==1.20.1
openai==2.24.0
openai-whisper==20250625
openpyxl==3.1.5
orjson==3.11.7
ormsgpack==1.12.2
outcome==1.3.0.post0
packaging==24.2
pandas==2.3.3
pandas_market_calendars==5.4.0
pcodedmp==1.2.6
pdfminer.six==20251230
pdfplumber==0.11.9
peewee==4.0.0
pillow==12.1.1
platformdirs==4.9.2
playwright==1.58.0
plotly==6.9.0
pluggy==1.6.0
propcache==0.5.2
protobuf==6.33.5
psutil==7.2.2
publicsuffix2==2.20191221
pyarrow==18.1.0
pyasn1==0.6.2
pycparser==3.0
pydantic==2.12.5
pydantic-settings==2.13.1
pydantic_core==2.41.5
pydivert==2.1.0
pyee==13.0.1
Pygments==2.19.2
pyiceberg==0.9.1
PyJWT==2.11.0
pylsqpack==0.3.24
pyluach==2.3.0
PyMuPDF==1.27.1
pynessie==0.67.0
pyOpenSSL==26.2.0
pyparsing==3.3.2
pypdf==6.12.2
pypdfium2==5.7.1
pyperclip==1.11.0
pyreadline3==3.5.6
pytest==9.0.2
pytest-asyncio==1.3.0
pytest-cov==7.1.0
python-dateutil==2.9.0.post0
python-docx==1.2.0
python-dotenv==1.2.2
python-multipart==0.0.22
python-pptx==1.0.2
python-whois==0.9.6
pytz==2025.2
pywin32==311
PyYAML==6.0.3
RapidFuzz==3.14.5
referencing==0.37.0
regex==2026.2.28
requests==2.32.5
requests-aws4auth==1.3.2
requests-toolbelt==1.0.0
responses==0.26.3
rfc3986==1.5.0
rich==13.9.4
rpds-py==0.30.0
rsa==4.7.2
ruamel.yaml==0.19.1
ruff==0.15.11
s3fs==2026.6.0
s3transfer==0.16.0
safetensors==0.7.0
scikit-learn==1.8.0
scipy==1.17.1
segno==1.6.6
sentence-transformers==5.2.3
service-identity==26.1.0
setuptools==82.0.1
sgmllib3k==1.0.0
shellingham==1.5.4
simplejson==4.1.1
six==1.17.0
sniffio==1.3.1
snowballstemmer==3.0.1
sortedcontainers==2.4.0
soupsieve==2.8.3
# Editable install with no version control (Sphinx==5.1.0.dev20260422)
-e c:\users\andrewberman\desktop\feature_clb\comp\targets\sphinx\_repo
sphinxcontrib-applehelp==2.0.0
sphinxcontrib-devhelp==2.0.0
sphinxcontrib-htmlhelp==2.1.0
sphinxcontrib-jsmath==1.0.1
sphinxcontrib-qthelp==2.0.0
sphinxcontrib-serializinghtml==2.0.0
SQLAlchemy==2.0.51
sqlglot==30.8.0
sqlite-vec==0.1.6
sse-starlette==3.3.3
starlette==0.52.1
strictyaml==1.7.3
sympy==1.14.0
tabulate==0.9.0
tantivy==0.25.1
tenacity==9.1.4
threadpoolctl==3.6.0
tiktoken==0.12.0
tokenizers==0.22.2
toolz==1.1.0
torch==2.10.0
tornado==6.5.5
tqdm==4.67.3
transformers==5.3.0
tree-sitter==0.25.2
tree-sitter-bash==0.25.1
tree-sitter-c==0.24.2
tree-sitter-c-sharp==0.23.5
tree-sitter-cpp==0.23.4
tree-sitter-dm==0.25.1
tree-sitter-elixir==0.3.5
tree-sitter-fortran==0.6.0
tree-sitter-go==0.25.0
tree-sitter-groovy==0.1.2
tree-sitter-java==0.23.5
tree-sitter-javascript==0.25.0
tree-sitter-json==0.24.8
tree-sitter-julia==0.23.1
tree-sitter-kotlin==1.1.0
tree-sitter-lua==0.5.0
tree-sitter-objc==3.0.2
tree-sitter-php==0.24.1
tree-sitter-powershell==0.26.4
tree-sitter-python==0.25.0
tree-sitter-ruby==0.23.1
tree-sitter-rust==0.24.2
tree-sitter-scala==0.26.0
tree-sitter-swift==0.7.2
tree-sitter-typescript==0.23.2
tree-sitter-verilog==1.0.3
tree-sitter-zig==1.1.2
trio==0.33.0
trustme==1.2.1
typer==0.24.1
typing-inspect==0.9.0
typing-inspection==0.4.2
typing_extensions==4.16.0
tzdata==2025.3
urllib3==2.6.3
urwid==3.0.5
uuid_utils==0.14.1
uvicorn==0.42.0
watchfiles==1.2.0
wcwidth==0.8.1
webencodings==0.5.1
websockets==16.0
Werkzeug==3.1.8
win_unicode_console==0.5
wrapt==2.2.2
wsproto==1.3.2
xlrd==2.0.2
xlsxwriter==3.2.9
xmltodict==1.0.4
xxhash==3.6.0
yarl==1.24.2
yfinance==1.2.0
zstandard==0.25.0
```
