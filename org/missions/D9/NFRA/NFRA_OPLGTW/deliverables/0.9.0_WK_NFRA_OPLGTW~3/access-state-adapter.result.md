# NFRA_OPLGTW.TO-OG-d-1 -- the access-state adapter: result

**Worker:** `0.9.0_WK_NFRA_OPLGTW~3` | **Branch:** `wk-nfra_oplgtw-1-3` (worktree `/c/tmp/wk-oplgtw-1-3`), cut from
`CLOUD` @2fdc84e250 | **Commits (LOCAL, never pushed):** `0c4a5edcd0` (code + tests + conftest), `e13bbe2b95` (surprise
rows W3-S1, W3-S2), and the commit carrying this file, the proof instance and the status flip.

## Emulator

**moto 5.2.3** (`mock_aws`, DynamoDB in-process), boto3 1.42.54, botocore 1.42.97, Python 3.12.10. moto implements
ConditionExpression and TransactWriteItems semantics: OGD1-AC7 shows a failed condition raising
`ConditionalCheckFailedException` for a single item, and `TransactionCanceledException` with
`CancellationReasons=['None', 'ConditionalCheckFailed']` for a transaction whose other item was not written. A positive
control (the same transaction with a satisfiable condition) commits. moto cannot evaluate IAM conditions, so the
`dynamodb:LeadingKeys` arm belongs to `OG-i-1`.

## Criteria (each invocation run from `/c/tmp/wk-oplgtw-1-3` under `timeout 120`; output verbatim)

| id | output (deciding lines) | rc |
|---|---|---|
| OGD1-AC1 | `READ CALLS: 8 of 8 client read calls passed ConsistentRead=True (get_item 3, query pages 5)` / `READ CALL SITES: 2 of 2 in app/access_state.py pass ConsistentRead=True (get_item:319, query:349)` / `1 passed in 0.68s` | 0 |
| OGD1-AC2 | `WRITE ITEMS: 6 of 6 written items carried a ConditionExpression (3 write calls: transact_write_items)` / `UNCONDITIONAL WRITES REFUSED: 15 of 15 attempts (5 write APIs x 3 empty conditions), 0 AWS calls` / `TRANSACTIONS: failed condition wrote 0 of 2 items; satisfied condition wrote 2 of 2 in 1 call` / `WRITE CALL SITES: 3 single-item sites all pass ConditionExpression; batch_write_item sites: 0` / `1 passed in 0.69s` | 0 |
| OGD1-AC3 | `KEYS: 9 of 9 contract record types map to one namespace (POLICY 3, RUNTIME 6)` / `MALFORMED KEYS REFUSED: 7 of 7` / `STORED PARTITION KEYS: POLICY#tid-a#oid-b, POLICY#tid-a#oid-b, RUNTIME#ticket#hash-1` / `1 passed in 0.88s` | 0 |
| OGD1-AC4 | `POLICY# REFUSED: 4 of 4 runtime write APIs, 0 AWS calls (client that fails on any touch)` / `RUNTIME# ACCEPTED: 4 of 4, the same calls, 1 AWS call each` / `LOOKALIKE KEYS REFUSED: 7 of 7 (x3 write APIs each), 0 AWS calls` / `1 passed in 0.74s` | 0 |
| OGD1-AC5 | `EXPIRED-BUT-PRESENT: raw get_item present; adapter get -> None, query -> 0 records (expiry now-1 and now)` / `UNEXPIRED: same record, expiry now+60 -> present; clock moved past expiry -> absent again` / `LIVE CONDITION: consume on the expired record -> ConditionFailed; on the unexpired record -> applied` / `1 passed in 0.72s` | 0 |
| OGD1-AC6 | `UNAVAILABLE: 22 of 22 arms raised DEPENDENCY_UNAVAILABLE; 0 returned a value or a default` / `ARMS: no-table 5, unreachable 5, malformed records 10, malformed responses 2` / `ALARMS: 22 of 22 fail-closed alarms emitted` / `1 passed in 5.99s` | 0 |
| OGD1-AC7 | `EMULATOR: moto 5.2.3 (boto3 1.42.54, botocore 1.42.97), DynamoDB mocked in-process via mock_aws` / `SINGLE-ITEM: failed ConditionExpression -> ConditionalCheckFailedException` / `TRANSACTION: failed ConditionCheck -> TransactionCanceledException, CancellationReasons=['None', 'ConditionalCheckFailed']; its Put wrote 0 of 1` / `POSITIVE CONTROL: ...committed` / `ADAPTER: both surface as ConditionFailed, ...` / `1 passed in 0.66s` | 0 |

Denominator: 7 of 7 criteria, all mechanical, all `1 passed`, rc=0.

## What the adapter decides that the order did not state

- **Key schema and attribute names** (row `NFRA_OPLGTW-W3-S1`, ARMED): composite key `pk` (HASH, S) + `sk` (RANGE, S);
  `record_type` on every item; `expires_at` (integer epoch seconds) is both the logical expiry and the TTL attribute.
  POLICY sort keys are `<record_type>[#<part>...]` (e.g. `data_entitlement#000003`, `operator_audit#<id>`); RUNTIME
  sort keys are the record type. RUNTIME kinds: client, pending_auth, code, refresh, ticket, catalog. All are module
  constants in `app/access_state.py`; if `OG-i-1`'s table differs, reconciling them is one edit.
- **Approval** has no record type of its own: the contract lists nine types, none of them approval, so approvals are stored on
  the `data_entitlement` record.
- **A failed condition is not a dependency failure**: `ConditionFailed` (including a lost `TransactionConflict`) is
  distinct from `DependencyUnavailable`, so a consumed code or a lost refresh race can answer `invalid_grant`
  while an unreachable store fails closed.
- **The operator path** (`operator_transact`) accepts only one principal's POLICY records, requires the matching
  `operator_audit` put in the same transaction, and refuses deletes and any TTL attribute (PRD C6).
- **Alarms** go to stderr (the host journal), not to `app.audit`, so the module never writes the tracked audit file
  and stays importable without Gateway configuration.

## Controls

- **Mutant:** runtime namespace guard reduced to `if k is None:` -> `test_ogd1_ac04` FAILED
  (`AssertionError: the adapter reached the client (put_item) before refusing`), `test_ogd1_ac02` passed,
  `1 failed, 1 passed`. Restored from the byte copy: sha256 `aea443f3b06dff637253aa3beaed85135470159bb1bc250c3ac83abdbedb8cc3`,
  the same before and after.
- **Determinism:** the 7-test file twice, rc=0 both; the only differing line is the wall-clock time (`6.91s` vs `7.12s`).
- **Whole Gateway suite** (not a criterion of this order; run because `conftest.py` affects every Gateway test):
  from `infra/aws/ec2/opal-gateway`, `.venv-og/Scripts/python -m pytest tests -q -p no:cacheprovider` ->
  `1 failed, 83 passed, 34 subtests passed`, rc=1. The one failure is row `NFRA_OPLGTW-S1`'s
  `test_scoped_deny_by_default`. The run appended 3 lines to the tracked `audit.jsonl` (row `NFRA_OPLGTW-W3-S2`),
  which I left uncommitted.
- **Commit gate:** `OK: pre-commit gate clean for 3 of 3 file(s)`.

## Surprise rows

- `NFRA_OPLGTW-W3-S1` -- OBSERVATION, ARMED, disarm owner `2.0.0_SA_COO~O`: no order or contract names the table's key
  attribute names, sort key or TTL attribute.
- `NFRA_OPLGTW-W3-S2` -- OBSERVATION, INERT: the Gateway suite writes the tracked `audit.jsonl`.

## Interpreter

`py -3.12 -m venv --system-site-packages .venv-og && .venv-og/Scripts/python -m pip install -r
infra/aws/ec2/opal-gateway/requirements.txt msal moto pytest` -> rc=0; newly installed into the venv:
`botocore-1.42.97 httptools-0.8.0 mcp-1.28.0 moto-5.2.3 msal-1.38.0 responses-0.26.3 typing-extensions-4.16.0
watchfiles-1.2.0 xmltodict-1.0.4`. `.venv-og/` and `.scratch/` are not committed.

## pip freeze

`.venv-og/Scripts/python -m pip freeze` (the venv sees the system site-packages, so this is the full resolved set):

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
duckdb==1.5.0
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
