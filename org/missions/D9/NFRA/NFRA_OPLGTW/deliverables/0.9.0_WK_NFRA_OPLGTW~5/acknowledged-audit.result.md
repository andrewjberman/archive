# NFRA_OPLGTW.TO-OG-o-1 -- result (0.9.0_WK_NFRA_OPLGTW~5)

**Order:** `org/missions/D9/NFRA/NFRA_OPLGTW/task-orders/NFRA_OPLGTW.TO-OG-o-1.acknowledged-audit.md`
**Branch:** `wk-nfra_oplgtw-1-5`, cut from `CLOUD` @1bcc827bda. **Build commit:** `21c047b3ea` (LOCAL, never pushed).
**Instance:** `NFRA_OPLGTW.TO-OG-o-1.acknowledged-audit.proof_of_spec.json` (beside this file).

## What was built

`infra/aws/ec2/opal-gateway/app/schwab_audit.py` (new):

- `release(produce, **fields)` builds the sanitized `release_authorized` record, awaits `put_acknowledged` off the event
  loop (`asyncio.to_thread`), and calls `produce` only after S3 has answered HTTP 200 with an ETag. With no receipt it
  returns `ReleaseOutcome(released=False, data=None, error_code="DEPENDENCY_UNAVAILABLE")` and never calls `produce`.
- `record_event(event_type, **fields)` writes the other events (`delivery_finished`, `denied`, `cancelled`, `failed`,
  `operator_revision`) through the same acknowledged write; it raises `AuditUnavailable` when there is no receipt.
- Sink: the existing `AUDIT_S3_BUCKET` (`opal-mcp-audit`), under `SCHWAB_AUDIT_PREFIX = "audit/schwab/"`. That is inside
  the existing `s3:PutObject` grant on `<audit bucket>/audit/*` (`audit-lake.tf:186-187`), and outside the `mcp_audit`
  table's projected `audit/dt=<day>/` location. With `AUDIT_S3_BUCKET` unset the write fails closed (`sink_unconfigured`).
- Record: a closed key set (`RECORD_FIELDS`) with no free-text slot. Operation, master, dataset, error code and
  classification are enums taken from the contract. The date is a validated `YYYY-MM-DD`, and counts, bytes, duration
  and grant revision are non-negative ints. The principal and the operator actor are stored only as sha256 digests,
  the snapshot/version reference only as an opaque fingerprint, and the operator reference is a change-id or git-hash
  shape. A value that fails its check is dropped and named in `redacted_fields`; an unknown keyword is a `TypeError`.
- `release_authorized` records the planned counts and refuses delivered counts (authorization does not prove
  delivery). `delivery_finished` requires both, and its outcome is `complete` or `partial`.
- Sink errors are never copied into the record: `AuditUnavailable` carries a bounded classification plus, at most, the
  AWS error-code token, and it is raised `from None`.
- Importing the module makes no network call and does not import boto3. No authentication module imports it.
- `app/audit.py` is unchanged.

`infra/aws/ec2/opal-gateway/tests/test_schwab_audit.py` (new): `test_ogo1_ac01` .. `test_ogo1_ac07`, offline against moto
with fake credentials.

## Criteria (each invocation verbatim from the order, `<WS>` = `/c/tmp/wk-oplgtw-1-5`)

| id | invocation (test) | rc | deciding line |
|---|---|---|---|
| OGO1-AC1 | `::test_ogo1_ac01` | 0 | `1 passed in 0.61s` |
| OGO1-AC2 | `::test_ogo1_ac02` | 0 | `1 passed in 0.64s` |
| OGO1-AC3 | `::test_ogo1_ac03` | 0 | `1 passed in 0.35s` |
| OGO1-AC4 | `::test_ogo1_ac04` | 0 | `1 passed in 0.65s` |
| OGO1-AC5 | `::test_ogo1_ac05` | 0 | `1 passed in 0.62s` |
| OGO1-AC6 | `::test_ogo1_ac06` | 0 | `1 passed in 0.66s` |
| OGO1-AC7 | `::test_ogo1_ac07` | 0 | `1 passed in 0.28s` |

Denominator: 7 of 7 criteria PASS by output, and none is marked `judgment`.

## Controls

- **Mutant** (call order): I inserted `_early = produce()` ahead of the acknowledged write in `release()`. Running AC1
  and AC2 against it gave rc=1, `2 failed in 1.28s`. AC1 failed with
  `[('data_released', None), ('put_object_acked', 200), ('data_released', None)]` and AC2 at `test_schwab_audit.py:122`.
  After restoring the file, the sha256 read `911b682e8f84dba5148c2b0bf59eca5d9cd01b5be1b6efe68cd29ca75b37dcd5` both
  before and after, with 0 MUTANT lines left.
- **Determinism:** the whole file gave `7 passed in 2.23s`, then the seven single-test runs each gave `1 passed`.
- **Regression (not a criterion):** the existing suite, run from `infra/aws/ec2/opal-gateway` with
  `-k "not test_scoped_deny_by_default and not test_schwab_audit"`, gave rc=0 and
  `76 passed, 8 deselected, 34 subtests passed`. This matches row NFRA_OPLGTW-S1's base count of 76 passed; the 8
  deselected are the 7 new tests plus the known red test.
- **Commit gate:** `bash .tools/commit-gate.sh <both .py files>` gave rc=0 and
  `OK: pre-commit gate clean for 2 of 2 file(s)` (ruff and py_compile included).

## Surprise rows

- `NFRA_OPLGTW-W5-S1` (OBSERVATION, INERT): the PRD's audit fields name `master` in the same sentence that excludes
  raw account IDs, and the contract's masters are 8-digit codes. I record master as given, bounded to the contract's
  two keys. Committed @21c047b3ea, and the surprise-row gate graded it: `1 new row(s) of 2 total checked`.

## Disclosure

`infra/aws/ec2/opal-gateway/audit.jsonl` shows as modified in this worktree and is **not committed**. The cause is the
regression run above: `test_ratelimit` appended 3 `_ratelimit_control` lines at 10:38:12Z through `audit.log_call` to
the cwd-relative `./audit.jsonl`. The file is outside this order's grant, so it is left as it is. The seven criteria
run from the workspace root and write nothing there.

## Venv (`py -3.12 -m venv --system-site-packages .venv-og`, then the order's pip install; rc=0)

Python 3.12.10. The `pip freeze` output follows, 318 lines, written in by a python writer from `.scratch/pip-freeze.txt`:

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
