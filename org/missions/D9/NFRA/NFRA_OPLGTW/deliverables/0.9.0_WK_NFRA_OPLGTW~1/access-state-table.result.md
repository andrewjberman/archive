# NFRA_OPLGTW.TO-OG-i-1 -- result (0.9.0_WK_NFRA_OPLGTW~1), re-run on the order as amended @fd2f1e4b31

**Outcome: BLOCKED AT SAFE-APPLY'S HALT GATE, BEFORE TERRAFORM RAN. Nothing was applied in AWS. The ledger entry is
OPEN (committed before the act, @4b9671ec09). The order stays `pending`.**
Branch `wk-nfra_oplgtw-1-1b`, worktree `/c/tmp/wk-oplgtw-1-1b`, base `09668e3207`.

## What happened, in order (UTC, 2026-09-15)

1. Tree check `TREE-OK` on `wk-nfra_oplgtw-1-1b` @09668e3207. `.tools/terraform.exe` v1.9.8 present.
2. Disk on C: -- 5.0G free at hand-off, 4.9G immediately before `terraform init` (21:31:55Z), 4.2G after it, 5.6G
   immediately before the apply (21:56:41Z; the driver's own read 5.53 GiB at 21:56:43Z). Never under the 2 GB floor.
3. `schwab_access_state.tf` restored from `59b567eed0`, byte-identical (sha256 68397bd897e6c2e9...).
4. `terraform init` rc 0 (lock file unchanged). `terraform plan` 21:35:26Z..21:35:48Z rc 0:
   **`Plan: 4 to add, 2 to change, 0 to destroy.`** -- this cell's 4 creates, and the 2 admitted in-place
   `+ description` updates on `aws_wafv2_ip_set.opal_blocked_ips_regional_v4` / `_v6`, with `addresses` absent from the
   diff. OGI1-AC1 and OGI1-AC10 PASS on the redacted plan `og_i1.plan.json`.
5. A live WAF read at 21:49:30Z found both regional blocked-IP sets holding **0 addresses**, the same count the plan's
   prior state carries. So the description update cannot drop a live list, and AC11 compares two empty lists
   (row `NFRA_OPLGTW-W1-S5`).
6. The ledger was opened at 21:52Z with 5 legs: L1 git, L2 activation, and L3-L5 verify, which carry the ruling's four
   conditions, one line each. Its sentinel and entry were committed @4b9671ec09 at 21:54:38Z, together with the
   declaration, the probes, the plan JSON and rows W1-S4/W1-S5.
7. The ONE guarded safe-apply run, `probes/og_i1_act.py apply`, 21:56:44.893672Z..21:56:47.841644Z: WAF pre-read,
   then `bash .tools/safe-apply.sh -chdir=infra/aws/terraform/opal-gateway apply -no-color`, which exited **3** with
   `HALT-GATE: IDENTITY UNRESOLVED -- BLOCKED (fail-closed)`. That is safe-apply's first stage, so the run stopped before
   the naming, tag-authz and tombstone limbs and before any plan: no approval prompt, no answer, terraform never
   invoked. The WAF post-read (21:56:48.609510Z) reads 0 and 0 with **the same lock tokens** as the pre-read
   (a2f2440b0dcf, 133af1a2f3f2), which confirms that no UpdateIPSet ran.

## Why it stopped -- row `NFRA_OPLGTW-W1-S6` (BLOCKING, ARMED, disarm_owner `2.0.0_SA_COO~O`)

`.tools/halt-gate-check.sh` @09668e3207 resolves the acting serial only from
`<worktree>/org/mcp/sessions/${CLAUDE_CODE_SESSION_ID}.serial` or a `${CLAUDE_CODE_SESSION_ID}.*.orphan-cleaned` marker
(`:52-120`). It never reads `OPAL_AGENT_SERIAL`: 0 occurrences in the file. `org/mcp/sessions/` is gitignored
(`.gitignore:423`), absent in this fresh worktree, and not named in the order's `<paths>`. The gate's remedy is to write
that file, and the gate says not to override it. The order's Grant bound makes an unnamed path a BLOCKING row, never an
override. So no apply was attempted past the gate.

**ARMED, for the issuer:** (1) do not drain `schwab_access_state.tf` from this branch to CLOUD before an order-bound
apply, or any later apply of the root creates the table and grants outside this ledger; (2) the OPEN sentinel will blare
RED past its 2 h window once it is on CLOUD, although nothing deployed. A re-run needs one of three things: the session
serial file admitted by a re-cut `<paths>` (worktree-local, gitignored, never committed); a serial file the issuer
provisions at spawn, as it does `.tools/terraform.exe`; or an apply by a seat whose identity the gate resolves. The re-run
can reuse the open ledger, because `open` refuses a second open of the same slug.

## The two ARNs (DECLARED, NOT CREATED)

| object | ARN | state |
|---|---|---|
| table | `arn:aws:dynamodb:us-east-1:313476888478:table/opal-gateway-access-state` | declared (`pk` HASH S, `sk` RANGE S, TTL `expires_at`, PAY_PER_REQUEST, SSE, PITR, deletion protection); `describe-table` -> ResourceNotFoundException at 22:08:14Z |
| operator role | `arn:aws:iam::313476888478:role/opal-gateway-access-admin` | declared (trust: the account root, refusing `aws:PrincipalArn` = `opal-gateway-role`; policy GetItem + PutItem/UpdateItem under LeadingKeys `POLICY#*`); `get-role` -> NoSuchEntity at 22:08:20Z |

The runtime grant `opal-gateway-access-state-runtime` on `opal-gateway-role` (GetItem; PutItem/UpdateItem under
LeadingKeys `RUNTIME#*`): `get-role-policy` -> NoSuchEntity at 22:08:17Z.

## Ledger

`org/critical_paths/change_management/20260915T2152Z_nfra-oplgtw-og-i-1-access-state_deploy_completion.md` and
`org/critical_paths/.open_deploys/nfra-oplgtw-og-i-1-access-state.json`: **OPEN, L1-L5 unproven**, committed @4b9671ec09.
L1's fact holds: the declaration was committed before any apply. It was not close-legged, because the act it precedes has
not happened.

## Criteria (all under `timeout 120`, 2026-09-15T22:08:05Z..22:08:49Z)

| id | verdict line | why |
|---|---|---|
| OGI1-AC1 | `PASS-OGI1-AC1` | 4 of 4 creates; 2 of 71 change existing resources, both admitted; 0 destroys |
| OGI1-AC2 | `FAIL-OGI1-AC2 probe error ResourceNotFoundException` | sentinel committed 21:54:38Z before the run (21:56:44Z), but the run exited 3 and created nothing (W1-S6) |
| OGI1-AC3 | `FAIL-OGI1-AC3 no commit deletes the ledger sentinel` | no act, so no close |
| OGI1-AC4 | `FAIL-OGI1-AC4 table absent: ResourceNotFoundException` | not applied |
| OGI1-AC5 | `FAIL-OGI1-AC5 runtime grant absent: NoSuchEntity` | not applied |
| OGI1-AC6 | `FAIL-OGI1-AC6 operator role absent: NoSuchEntity` | not applied |
| OGI1-AC7 | `FAIL-OGI1-AC7 precondition: table absent` | not applied; no SSM command sent |
| OGI1-AC8 | `FAIL-OGI1-AC8 precondition: table absent` | not applied; no race |
| OGI1-AC9 | `FAIL-OGI1-AC9 precondition: table absent` | not applied; no record written |
| OGI1-AC10 | `PASS-OGI1-AC10` | 11 of 11 checks: exactly the two admitted `description` updates, `addresses` count 0 -> 0, not in the diff |
| OGI1-AC11 | `FAIL-OGI1-AC11 the before/after address lists or their record did not hold` | lists identical (0/0), but the bracketed apply exited 3 and the entry has no close commit (0 of 6 tokens) |
| OGI1-AC12 | `FAIL-OGI1-AC12 a graded resource is not no-op in the fresh plan` | fresh plan 22:08:37Z still `Plan: 4 to add, 2 to change, 0 to destroy.`; 0 changes elsewhere |

Controls: the approval guard said yes on the real plan and no on 3 of 3 mutants (an extra `- addresses` line, a
`must be replaced` header, an unadmitted WAF address). AC11 refuses a record whose bracketed apply did not complete.
AC1 and AC10 are stable across two runs.

## comp-iam re-run

No apply happened, so there is no after-the-apply re-run. The lens was re-run over the root with the declaration present,
2026-09-15T22:11:48Z, `.tools/comp-iam service opal-gateway`, rc 0: **PLANE DESIRED** (Terraform; does not read live
AWS). It scanned 3 trees (473 .tf files): 393 policy blocks attached, 27 NOT ATTACHED, 13 standalone; 2 deny statements
unparsed. For service `opal-gateway` and role `opal-gateway-role` it lists **27 operations: 14 UNGRANTED,
11 UNRESOLVABLE-RESOURCE, 2 GRANTED-ACTION/UNGRANTED-RESOURCE**, and 8 UNMAPPED-METHOD calls (among them
`raw.transact_write_items`). It now lists DynamoDB operations, because the merged adapter's tests call DynamoDB:
`dynamodb:GetItem`/`PutItem` UNRESOLVABLE-RESOURCE at `tests/test_access_state.py:110`, `:118`; `dynamodb:Scan` and
`DeleteItem` UNGRANTED at `:312`, `:470`. Those are test calls against moto, and this cell grants neither of those two
by design. The APPLIED and EXERCISED planes are AC5-AC8's, and they did not run.

## Interpreter

`.venv-og` = `py -3.12 -m venv --system-site-packages`, then
`pip install -r infra/aws/ec2/opal-gateway/requirements.txt msal moto pytest`: rc 0. pip warned that the system awscli
1.44.44 pins botocore 1.42.54 while the venv resolved 1.42.97, and that mitmproxy 12.2.3 wants typing-extensions
<=4.14. Python 3.12.10, boto3 1.42.54, botocore 1.42.97. The freeze has 318 lines. It differs from the first run's by
one line: `duckdb==1.5.0` then, `duckdb==1.2.2` now.

## pip freeze (.venv-og)

318 lines, captured 2026-09-15 ~22:11Z from .venv-og/Scripts/python -m pip freeze.

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
