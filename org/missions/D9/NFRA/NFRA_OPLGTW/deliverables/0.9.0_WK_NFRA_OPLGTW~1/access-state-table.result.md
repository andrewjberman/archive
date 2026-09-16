# NFRA_OPLGTW.TO-OG-i-1 -- result (0.9.0_WK_NFRA_OPLGTW~1), re-run on the order as amended @fd2f1e4b31

**Outcome: APPLIED. The table and both grants are live, the ledger is CLOSED, and 12 of 12 mechanical criteria
PASS by output.** Branch `wk-nfra_oplgtw-1-1b`, worktree `/c/tmp/wk-oplgtw-1-1b`, base for this run `a0bcaa6bae`.

This is the SECOND run of the order on this branch. The first (21:31Z..22:11Z, recorded below under "The first
run") reached safe-apply and was refused by the halt gate before terraform was invoked; nothing was applied and
the ledger `nfra-oplgtw-og-i-1-access-state` stayed OPEN, committed @4b9671ec09. That same OPEN entry was reused
here, as `deploy_ledger.py open` refuses a second open of one slug.

## What happened, in order (UTC, 2026-09-15 / 2026-09-16)

1. Tree check `TREE-OK` on `wk-nfra_oplgtw-1-1b` @a0bcaa6bae; `.tools/terraform.exe` present (91,104,424 bytes);
   `.venv-og` reused, not rebuilt.
2. The identity fix, provisioned by the issuer and never touched here:
   `org/mcp/sessions/e09b6e12-6f85-4732-b702-3307d4a68532.serial` reads `0.9.0_WK_NFRA_OPLGTW~1` and is gitignored
   (`.gitignore:423`). This worker did not write it and did not commit it.
3. `.tools/halt-gate-check.sh` re-grounded twice under bound, in this worktree, with
   `HALT_GATE_INBOX_ROOT=/c/Users/AndrewBerman/Desktop/ajb_workspace/org/mcp/inbox`:
   - without `HALT_ACK`: **rc 1** after 120 s -- `HALT-GATE: worker 0.9.0_WK_NFRA_OPLGTW~1 has no inbox; scanning
     its issuer 2.0.0_SA_COO~O`, then `HALT-GATE: 14 pending message(s) -- review before proceeding
     (unspecified)`. **Not rc 2**, so no STOP-class message;
   - with `HALT_ACK=1`: **rc 0** after 120 s -- `HALT-GATE: HALT_ACK set -- messages acknowledged. Proceeding.`
   Row `NFRA_OPLGTW-W1-S7` records that neither variable is named by the order.
4. Disk on C: 15 GiB free, never near the driver's 2 GiB floor (`og_i1_act.py apply` prints its own read).
5. **The ONE guarded safe-apply run**, `probes/og_i1_act.py apply`, 2026-09-15T23:27:50.539654Z..23:32:28.811293Z:
   WAF pre-read at 23:27:50.422672Z, then
   `bash .tools/safe-apply.sh -chdir=infra/aws/terraform/opal-gateway apply -no-color` with stdin a pipe. The
   in-run approval guard judged the plan terraform printed in THIS run at 23:32:13.259168Z --
   `ok=true, reasons []`, creates exactly this cell's four, updates exactly the two admitted WAF sets with
   `+ description` as the only attribute line, `other_headers []`,
   `Plan: 4 to add, 2 to change, 0 to destroy.` -- and answered **yes**. Result: **rc 0**,
   `Apply complete! Resources: 4 added, 2 changed, 0 destroyed.` WAF post-read at 23:32:30.068485Z.
   `saved_planfile_consumed=false`, `waf_optimistic_lock_exception=false`: plan and apply in one run, no retry,
   no force, no `-target`.
6. The ledger's five legs were closed with their proofs and the entry CLOSED, then **committed @b17f9b05cb
   (2026-09-15T23:56:26Z) BEFORE any read that grades the act** -- open, commit, act, close, commit, read.
7. The twelve criteria were then re-run, each under `timeout 120`, 2026-09-16T00:00:32Z..00:08:59Z:
   **12 of 12 PASS by output.**

## The four conditions of ruling 97237, as closed legs

| leg | condition | proof |
|---|---|---|
| L1 | the declaration committed before the apply | `4b9671ec09` at 2026-09-15T21:54:38Z, apply start 23:27:50.539654Z |
| L2 | the apply itself | safe-apply rc 0, `Apply complete! Resources: 4 added, 2 changed, 0 destroyed.` |
| L3 | COND-1: out-of-cell changes are EXACTLY the two `~ description` updates, `addresses` absent | saved-plan census 11 of 11 OK, and the in-run guard's own verdict `ok=true` |
| L4 | COND-2: `get-ip-set` before and after reads identical lists | PRE 23:27:50.422672Z and POST 23:32:30.068485Z, v4 and v6 both `count=0 sha256=e3b0c44298fc1c14`, IDENTICAL; lock tokens rotated v4 `a2f2440b0dcf`->`32f45c30512d`, v6 `133af1a2f3f2`->`d0c5e12d46ed` |
| L5 | COND-3 one run, fresh lock token; COND-4 declared for the post-close plan | `saved_planfile_consumed=false`, no `WAFOptimisticLockException`; COND-4 graded by AC12 after the close commit |

**The lock tokens rotated on both sets while the address lists did not move.** That is the discriminator the
condition exists for: the reads bracket a real `UpdateIPSet`, not a no-op. Row `NFRA_OPLGTW-W1-S5` still stands --
both lists were EMPTY (0 addresses) at this apply, so the comparison could not fail on a non-empty list.

## The two ARNs (CREATED and read back live)

| object | ARN | live state |
|---|---|---|
| table | `arn:aws:dynamodb:us-east-1:313476888478:table/opal-gateway-access-state` | ACTIVE. SSE ENABLED (KMS, `arn:aws:kms:us-east-1:313476888478:key/86cc6c40-2387-4446-b7e1-de79392e06b3`), PITR ENABLED, PAY_PER_REQUEST, TTL `expires_at` ENABLED, KeySchema `pk:HASH,sk:RANGE`, AttributeDefinitions `pk:S,sk:S`. CreationDateTime 2026-09-15T23:32:16.103000Z |
| operator role | `arn:aws:iam::313476888478:role/opal-gateway-access-admin` | created 2026-09-15T23:32:16Z; trust = the account root with `ArnNotEquals aws:PrincipalArn = arn:aws:iam::313476888478:role/opal-gateway-role`; inline policy `opal-gateway-access-admin-policy` |

The runtime grant is the inline policy `opal-gateway-access-state-runtime` on `opal-gateway-role`: `GetItem` on the
exact table ARN, and `PutItem`/`UpdateItem` on that ARN only under
`ForAllValues:StringLike dynamodb:LeadingKeys = ["RUNTIME#*"]` with `Null dynamodb:LeadingKeys = false`. No
DeleteItem, no BatchWriteItem, no PartiQL, no table-admin action, no wildcard. Nine other inline policies and one
attached policy on that role were read: none mentions DynamoDB.

## Criteria (all under `timeout 120`, 2026-09-16T00:00:32Z..00:08:59Z)

| id | verdict line | deciding measurement |
|---|---|---|
| OGI1-AC1 | `PASS-OGI1-AC1` | 71 resource_changes: 4 of 4 creates, 0 extra, 2 changes to existing resources both admitted, 0 destroys |
| OGI1-AC2 | `PASS-OGI1-AC2` | 4 of 4: safe-apply, rc 0, sentinel commit 21:54:38Z < apply start 23:27:50.539654Z < table 23:32:16.103000Z and role 23:32:16Z |
| OGI1-AC3 | `PASS-OGI1-AC3` | 2 of 2: the entry reads CLOSED at the close commit `b17f9b05cb` (23:56:26Z), which precedes the first readback 2026-09-16T00:00:34.415276Z |
| OGI1-AC4 | `PASS-OGI1-AC4` | 6 of 6 table properties: SSE ENABLED, PITR ENABLED, PAY_PER_REQUEST, TTL `expires_at` ENABLED, `pk:HASH,sk:RANGE`, `pk:S,sk:S` |
| OGI1-AC5 | `PASS-OGI1-AC5` | 15 of 15: document shape + 8 live `simulate-principal-policy` calls (PutItem/UpdateItem allowed under `RUNTIME#`, implicitDeny under `POLICY#`; DeleteItem, DeleteTable, UpdateTable implicitDeny) |
| OGI1-AC6 | `PASS-OGI1-AC6` | 18 of 18: separate ARN, trust refuses the Gateway role, `sts:AssumeRole` implicitDeny for the Gateway role, POLICY-only writes, and an EXERCISED transaction (conditional `POLICY#` update + `operator_audit` append, DeleteItem AccessDeniedException, strong read-back revision 2 with 2 of 2 audit items) |
| OGI1-AC7 | `PASS-OGI1-AC7` | 3 of 3 deciding, on `i-07dccb1615503ac99` under its own role via SSM `cc2eaf68-8ce4-4c2a-a6c6-d221a91fb9ed`: caller is `assumed-role/opal-gateway-role/i-07dccb1615503ac99`; `POLICY#` put-item AccessDeniedException (rc 254); `RUNTIME#` put-item rc 0 in the same harness. 5 of 5 supplementary also held, including the MIXED transaction denied |
| OGI1-AC8 | `PASS-OGI1-AC8` | 2 concurrent operator `UpdateItem`s on one record: exactly 1 SUCCESS (racer-0) and 1 ConditionalCheckFailedException, read-back revision 2 `rev_by racer-0` |
| OGI1-AC9 | `PASS-OGI1-AC9` | 2 of 2 probe `POLICY#` items carry no `expires_at` against the live TTL attribute name `expires_at` |
| OGI1-AC10 | `PASS-OGI1-AC10` | 11 of 11: exactly two out-of-cell changes, both admitted sets, `[update]`, `description` only, addresses count 0 -> 0 and absent from the diff, no replace_paths, 0 destroys. The guard's own in-run verdict prints beside it |
| OGI1-AC11 | `PASS-OGI1-AC11` | 6 of 6 deciding: both lists identical, the bracketed apply completed (rc 0 + Apply complete), pre 0.1 s before / post 1.3 s after, and 6 of 6 evidence tokens found in the entry at close commit `b17f9b05cb` |
| OGI1-AC12 | `PASS-OGI1-AC12` | fresh plan 00:08:48Z..00:08:59Z, `-detailed-exitcode` rc **0**, `No changes. Your infrastructure matches the configuration.`; 71 of 71 resource_changes no-op; 6 of 6 graded resources no-op; 0 changes elsewhere |

Controls: the approval guard is the instrument that could have gone either way, and did -- yes on the real plan,
no on 3 of 3 mutants (an extra `- addresses` line, a `must be replaced` header, an unadmitted WAF set); AC11
refuses a record whose bracketed apply did not complete, and DID refuse on the first run's record. AC1 and AC10
are byte-stable across three runs of the same saved plan.

## The first run (2026-09-15 21:31Z..22:11Z), kept for the record

Restored `schwab_access_state.tf` from `59b567eed0` byte-identical (sha256 68397bd897e6c2e9...), `terraform init`
rc 0, plan 21:35:26Z..21:35:48Z rc 0 `Plan: 4 to add, 2 to change, 0 to destroy.`, ledger opened 21:52Z and
committed @4b9671ec09 at 21:54:38Z, then one safe-apply invocation at 21:56:44.893672Z that exited **3** with
`HALT-GATE: IDENTITY UNRESOLVED -- BLOCKED (fail-closed)` before terraform was invoked. It is carried in
`evidence/apply.json` as `prior_attempts[0]`. Row `NFRA_OPLGTW-W1-S6` (BLOCKING, ARMED) is that block; the issuer
disarmed it with rows S18 and S19 on CLOUD by provisioning the session serial file and naming the inbox root.

## comp-iam re-run over the root, AFTER the apply

`.tools/comp-iam service opal-gateway`, 2026-09-16T00:1xZ, rc 0: **PLANE DESIRED** (Terraform; it does not read
live AWS, and it says so). 3 trees scanned (473 `.tf` files); 393 policy blocks attached, 27 NOT ATTACHED, 13
standalone; 2 deny statements unparsed. For service `opal-gateway` / role `opal-gateway-role` it lists **27
operations**: 14 UNGRANTED, 11 UNRESOLVABLE-RESOURCE, 2 GRANTED-ACTION/UNGRANTED-RESOURCE, and UNMAPPED-METHOD
rows among them. Its DynamoDB rows come from the merged adapter's tests against moto
(`tests/test_access_state.py`): `dynamodb:GetItem`/`PutItem`/`UpdateItem` UNRESOLVABLE-RESOURCE (comp-iam models
no DynamoDB resource), `dynamodb:Scan` and `DeleteItem` UNGRANTED -- and this cell grants neither of those two by
design. `raw.transact_write_items` renders UNMAPPED-METHOD, which is the same fact row `NFRA_OPLGTW-W1-S3` states:
there is no `dynamodb:TransactWriteItems` IAM action. **The APPLIED and EXERCISED planes for these grants are
AC5-AC9, and they ran: 8 live `simulate-principal-policy` calls on the runtime role, 5 on the operator role, one
exercised operator transaction, one on-host SSM difference and one concurrency race.**

## Probe records written (isolated, this run)

Six isolated keys, all `probe=og-i1`: `POLICY#probe-og-i1-20260916T000402023004Z` (AC6, PROFILE + AUDIT#0001 +
AUDIT#0002), `POLICY#probe-og-i1-20260916T000658709747Z-race` (AC8), `POLICY#probe-og-i1-20260916T000705463912Z-ttl`
(AC9), and `POLICY#`/`RUNTIME#probe-og-i1-20260916T000511712632Z` (AC7, on-host; only the `RUNTIME#` writes landed).
No profile, grant, client or record of any real person. The `RUNTIME#` probe items carry `expires_at` at now+3600 s
and will be cleaned up by TTL; the `POLICY#` probe items carry no TTL attribute by design (that IS AC9) and are
left in place as the evidence AC9 read.

## Rows filed this run

- `NFRA_OPLGTW-W1-S7` (OBSERVATION, INERT) -- the apply ran only under `HALT_ACK=1` and `HALT_GATE_INBOX_ROOT`,
  neither named by the order, and a worker's halt gate scans its ISSUER's inbox, so the acknowledgement covered 14
  routine messages addressed to `2.0.0_SA_COO~O`. The gate returned rc 1, never rc 2.
- `NFRA_OPLGTW-W1-S8` (OBSERVATION, INERT) -- `proof-of-spec-check` refuses a `PENDING-THIS-COMMIT` row for a file
  the RUN created and never committed, so `evidence/first_readback.json` was committed alone at `8acd1d3459` and
  pinned by hash; the instance, the deliverables and the `<status>` flip then ride one commit.

Rows W1-S1..W1-S6 stand as filed; none is re-graded here.

## Interpreter

`.venv-og` was reused, not rebuilt: `py -3.12 -m venv --system-site-packages` with
`pip install -r infra/aws/ec2/opal-gateway/requirements.txt msal moto pytest` from the first run. Python 3.12.10,
boto3 1.42.54, botocore 1.42.97. `pip freeze` re-captured this run: 318 lines, unchanged from the first run's
318.

## pip freeze (.venv-og), 318 lines, captured 2026-09-16 ~00:1xZ

```
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
