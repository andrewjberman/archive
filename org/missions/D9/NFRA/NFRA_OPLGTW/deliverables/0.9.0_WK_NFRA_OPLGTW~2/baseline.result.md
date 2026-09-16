# NFRA_OPLGTW.TO-OG-p-1 -- baseline result (0.9.0_WK_NFRA_OPLGTW~2)

Original run: worktree `/c/tmp/wk-oplgtw-1-2`, branch `wk-nfra_oplgtw-1-2`, cut from CLOUD at 417631ae6f, 2026-09-15.
AC1-AC10 below are that run's rows, carried unchanged per the RE-HAND SCOPE.

**COLD RE-HAND, 2026-09-16:** worktree `/c/tmp/wk-oplgtw-1-2d`, branch `wk-nfra_oplgtw-1-2d`, cut from CLOUD at
bec64dea66 (contains the OG-p-1/OG-c-2 amendment @246231edd6, executing `1.0.0_SA_CTO` rulings R-OG-1/R-OG-2, msg
97499 @d6583eab37, `org/tier1_exec/1.0.0_SA_CTO/deliverables/RULINGS_NFRA_OPLGTW_20260916.md`). AC11, AC12 and AC13
were rebuilt to the amended criteria and re-run; AC1-AC10 were NOT re-run. READ ONLY throughout both runs: no apply,
deploy, restart or write in AWS or on the Gateway host.

## Outcome

**13 of 13 mechanical criteria PASS by output.** AC1-AC10 PASS from the 2026-09-15 run (unchanged). AC11, AC12 and
AC13 were rebuilt per ruling R-OG-2 and now PASS:
- AC11 reads p95 from the ALB's own CloudWatch `TargetResponseTime` (overall + per target group), not the audit
  record; the audit record's missing latency field is the finding row `NFRA_OPLGTW-W2-S1`, carried to L10, not fixed.
- AC12 reads the OAuth client inventory from the Gateway's persisted access-state table (`opal-gateway-access-state`,
  created by `OG-i-1` since the first run), not the audit record; the audit record's missing `client_id` is the
  finding row `NFRA_OPLGTW-W2-S2`, carried to L10 against FWD-8, not fixed.
- AC13 admits the 8 `ssm:SendCommand` calls (AC1/AC2/AC10's unchanged host reads, and the two retired AC11/AC12
  audit-census calls from the first run) by regenerating and printing each one's script text and certifying it
  read-only, per ruling R-OG-2; every other call is graded Describe/Get/List/Head/Scan/Query as before (Scan/Query
  added for AC12's DynamoDB read, per the hand-off facts).

The `complete` flip is made in the commit that carries this result.

| criterion | verdict (verbatim) | probe rc | recorded (UTC) | denominator |
|---|---|---|---|---|
| OGP1-AC1 | `VERDICT: PASS-OGP1-AC1` | 0 | 2026-09-15T10:53:56Z | 50 files (tree 50, host 50) |
| OGP1-AC2 | `VERDICT: PASS-OGP1-AC2` | 0 | 2026-09-15T10:54:14Z | 51 |
| OGP1-AC3 | `VERDICT: PASS-OGP1-AC3` | 0 | 2026-09-15T10:49:27Z | 2 listener(s), 8 rule(s) |
| OGP1-AC4 | `VERDICT: PASS-OGP1-AC4` | 0 | 2026-09-15T10:47:40Z | 4 reads, 7 values (versioning, encryption, 4 public-access-block flags, policy status) |
| OGP1-AC5 | `VERDICT: PASS-OGP1-AC5` | 0 | 2026-09-15T10:50:46Z | 1 trust document + 8 inline + 1 attached policies |
| OGP1-AC6 | `VERDICT: PASS-OGP1-AC6` | 0 | 2026-09-15T10:51:14Z | 2 role names |
| OGP1-AC7 | `VERDICT: PASS-OGP1-AC7` | 0 | 2026-09-15T10:51:39Z | 1 table name |
| OGP1-AC8 | `VERDICT: PASS-OGP1-AC8` | 0 | 2026-09-15T10:52:25Z | 2 master prefix(es) under schwab/, 2 with meta/complete/ objects |
| OGP1-AC9 | `VERDICT: PASS-OGP1-AC9` | 0 | 2026-09-15T10:53:02Z | 11 notification configuration(s) (11 ObjectCreated); EventBridge enabled=False |
| OGP1-AC10 | `VERDICT: PASS-OGP1-AC10` | 0 | 2026-09-15T10:54:26Z | 1 process(es) in the service (MainPID + children) |
| OGP1-AC11 (2026-09-15, superseded) | `VERDICT: FAIL-OGP1-AC11 p95 latency not computable from the audit record: 0 of 78049 records in the window carry a latency/duration field` | 1 | 2026-09-15T10:57:49Z | 78049 audit records in window; per-tool sample counts: {'create_draft': 3, 'find_sharepoint_site': 14, 'get_item': 5, 'get_site_item': 1, 'graph_cypher': 35, 'graph_status': 5, 'list_calendar': 4, 'list_channels': 16, 'list_chats': 33, 'list_email_attachments': 26, 'list_onedrive': 2, 'list_recent_email': 25, 'list_site_files': 8, 'list_teams': 12, 'ms_site_children': 42055, 'ms_sites': 1, 'otp_fetch': 32, 'poll_addressed_teams_messages': 19370, 'profile_site_file': 2, 'query_v0': 40, 'read_channel_messages': 3526, 'read_chat_messages': 81, 'read_document': 5, 'read_email': 82, 'read_site_file': 4, 'read_site_workbook': 8, 'save_email_attachment_to_site': 15, 'search_email': 164, 'search_files': 17, 'search_site_files': 8, 'send_channel_message': 3, 'send_chat_message': 29, 'send_email': 4, 'sprint_view': 4, 'whoami': 163, 'ycharts_freshness': 3, 'ycharts_fund_series': 7, 'ycharts_search': 55, 'ycharts_snapshot_metrics': 20, 'ycharts_time_series': 9} |
| OGP1-AC12 (2026-09-15, superseded) | `VERDICT: FAIL-OGP1-AC12 no client inventory derivable: 0 of 79091 audit records carry a client_id field (audit.py log_call does not write one), so an inventory from it is empty by construction` | 1 | 2026-09-15T10:58:01Z | 78049 audit records in window (79091 in file) |
| OGP1-AC13 (2026-09-15, superseded) | `VERDICT: FAIL-OGP1-AC13 8 of 57 calls are not Describe/Get/List/Head: {'ssm:SendCommand': 8}` | 1 | 2026-09-15T11:01:03Z | 57 AWS call(s) in the command log |
| **OGP1-AC11 (2026-09-16, rebuilt)** | `VERDICT: PASS-OGP1-AC11` | 0 | 2026-09-16T19:15:11Z | 1 overall + 1 target group metric read(s) |
| **OGP1-AC12 (2026-09-16, rebuilt)** | `VERDICT: PASS-OGP1-AC12` | 0 | 2026-09-16T19:01:01Z | 7 item(s) scanned, 0 matching record_type='oauth_client' |
| **OGP1-AC13 (2026-09-16, rebuilt)** | `VERDICT: PASS-OGP1-AC13` | 0 | 2026-09-16T19:15:53Z | 77 AWS call(s) in the command log |

Invocation of every criterion: the order's own, `cd /c/tmp/wk-oplgtw-1-2d && timeout 120 .venv-og/Scripts/python org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/probes/og_p1.py AC<n>` (the 2026-09-15 rows used `/c/tmp/wk-oplgtw-1-2`, that run's own worktree); the recorded runs appended `--record`, which only persists the printed lines into BASELINE.json. Full printed output per criterion: BASELINE.md / BASELINE.json.

### AC11 rebuilt output (2026-09-16T19:15:11Z, verbatim)

```
instrument: cloudwatch GetMetricStatistics AWS/ApplicationELB TargetResponseTime (Statistics SampleCount, ExtendedStatistics p95), one CloudWatch period spanning the whole window, via .tools/aws; elbv2 DescribeLoadBalancers/DescribeTargetGroups resolve the dimensions
vintage: 2026-09-16T19:15:11Z  load_balancer=arn:aws:elasticloadbalancing:us-east-1:313476888478:loadbalancer/app/opal-gateway/89166a68f337e5a4  target_groups=1
window: 2026-09-02T19:15:00Z .. 2026-09-16T19:15:00Z (14 days, period=1209600s)
the ALB does not know the MCP tool: this is per target group and overall, and claims no per-tool figure (the audit record's missing latency field, row NFRA_OPLGTW-W2-S1, is a separate finding, not fixed here)
denominator: 1 overall + 1 target group metric read(s)
overall: sample_count=43745.0 p95_seconds=0.5535024102704742 (553.5 ms) (read 2026-09-16T19:15:05Z)
  target group opal-gateway-tg (arn:aws:elasticloadbalancing:us-east-1:313476888478:targetgroup/opal-gateway-tg/00997fc81f087cb8): sample_count=43745.0 p95_seconds=0.5535024102704742 (553.5 ms) (read 2026-09-16T19:15:11Z)
VERDICT: PASS-OGP1-AC11
```

### AC12 rebuilt output (2026-09-16T19:01:01Z, verbatim)

```
instrument: dynamodb Scan (FilterExpression record_type='oauth_client', ConsistentRead) on opal-gateway-access-state via .tools/aws; deployed-commit source read (git show, no AWS call) for process-locality
vintage: 2026-09-16T19:01:01Z
denominator: 7 item(s) scanned, 0 matching record_type='oauth_client' (read 2026-09-16T19:01:01Z)
registered clients (persisted store): 0
process-locality AS MEASURED: deployed_commit=7bd89b5d71 -- app/access_state.py ABSENT at that commit; app/oauth_as.py there still defines an in-memory '_clients' store. So the RUNNING gateway's OAuth client store is process-local (in-memory; workers pinned to 1); the persisted table read above is the durable store OG-a-1/OG-d-1 built at HEAD but not yet released to this host, so today it is independent of process locality either way -- a finding carried to L10 (row NFRA_OPLGTW-W2-S2) is that the audit record still cannot name which client made a given call.
VERDICT: PASS-OGP1-AC12
```

### AC13 rebuilt output (2026-09-16T19:15:53Z, verbatim; full script-text listing in BASELINE.md/BASELINE.json)

```
instrument: this probe reads org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/command_log.jsonl (one row per AWS call, written by aws()); ssm:SendCommand rows are graded against this file's own script-building functions -- this criterion makes no AWS call itself
vintage: 2026-09-16T19:15:53Z
denominator: 77 AWS call(s) in the command log
Describe/Get/List/Head/Scan/Query calls: 69 of 77
ssm:SendCommand calls: 8 of 77; admitted (read-only script) 8, refused 0
  ADMITTED AC1 label='AC1 digests' logged_digest=54a7f4892ab06aa3 digest_check=EXACT MATCH (54a7f4892ab06aa3)
  ADMITTED AC2 label='AC2 host shape' logged_digest=575bae85b00568aa digest_check=EXACT MATCH (575bae85b00568aa)
  ADMITTED AC10 label='AC10 peak RSS' logged_digest=a509ac92d2db6b24 digest_check=EXACT MATCH (a509ac92d2db6b24)
  ADMITTED AC11 label='AC11 audit latency census' logged_digest=57277991a613ee60 digest_check=template-match (per-call timestamp, not a command, cannot be recomputed)
  ADMITTED AC12 label='AC12 audit client census' logged_digest=3310fedad277dd7f digest_check=template-match (per-call timestamp, not a command, cannot be recomputed)
  ADMITTED AC11 label='AC11 audit latency census' logged_digest=5599443ef08849d6 digest_check=template-match (per-call timestamp, not a command, cannot be recomputed)
  ADMITTED AC12 label='AC12 audit client census' logged_digest=d664b3cab82e044a digest_check=template-match (per-call timestamp, not a command, cannot be recomputed)
  ADMITTED AC1 label='AC1 digests' logged_digest=54a7f4892ab06aa3 digest_check=EXACT MATCH (54a7f4892ab06aa3)
VERDICT: PASS-OGP1-AC13
```

## Surprise rows filed

- `NFRA_OPLGTW-W2-S1` OBSERVATION, INERT -- AC11: the audit record has no timing field; still true, no longer
  blocking (AC11 now reads CloudWatch instead), carried to L10 as a finding (FWD-7's later proof needs a
  per-request measure the Gateway itself emits).
- `NFRA_OPLGTW-W2-S2` OBSERVATION, INERT -- AC12: the audit record has no client_id field; still true, no longer
  blocking (AC12 now reads the persisted access-state table instead), carried to L10 against FWD-8.
- `NFRA_OPLGTW-W2-S3` OBSERVATION, INERT -- AC13: the named host-read route is ssm:SendCommand, not a read verb;
  resolved by admitting it per ruling R-OG-2 (script text printed and certified read-only), not by widening the
  read-verb list.
- `NFRA_OPLGTW-W2-S4` OBSERVATION, INERT -- new this re-hand: a CloudWatch `GetMetricStatistics` percentile query
  whose one Period spans the 15-day 1-minute-resolution retention boundary silently returns TWO datapoints
  (measured [10, 79222] samples for a 30-day window), not a clean partition of the window; the first build of
  AC11 (30-day window, `Datapoints[0]`) would have reported p95=31 ms from the 10-sample sliver where the true
  figure is ~553 ms. Caught by a day-by-day bisection (0..16 days) before recording; fixed by narrowing
  `AC11_WINDOW_DAYS` to 14 (under the boundary) and adding `_cw_datapoint`, which refuses outright rather than
  picking a datapoint if CloudWatch ever returns more than one.

## Controls

AC6 mutant (an existing role in place of an absent one):

```
MUTANT CONTROL: first role name replaced by 'opal-gateway-role' (OGP1_MUTANT_ROLE)
instrument: iam GetRole via .tools/aws
vintage: 2026-09-15T10:58:48Z
denominator: 2 role names
GetRole opal-gateway-role: EXISTS arn:aws:iam::313476888478:role/opal-gateway-role (rc=0, read 2026-09-15T10:58:44Z)
GetRole opal-mcp-schwab-catalog-read: NoSuchEntity (rc=255, read 2026-09-15T10:58:48Z)
VERDICT: FAIL-OGP1-AC6 not NoSuchEntity: opal-gateway-role
rc=1
```

AC1 discrimination (host compared against HEAD 417631ae6f instead of the deployed commit):

```
instrument: SSM AWS-RunShellScript sha256sum on i-07dccb1615503ac99 (/opt/opal-gateway) vs git blob sha256 at 417631ae6fea14297c772bcb0e4f8387631ecabe (infra/aws/ec2/opal-gateway); ssm bdd26faf-120f-4290-84ef-387274da9fb0 Success at 2026-09-15T10:58:13.861Z
vintage: 2026-09-15T10:58:17Z  deployed_commit(manifest)=7bd89b5d71b8d488d9e8c4168513193c9d6a9ec2 compared_commit=417631ae6fea14297c772bcb0e4f8387631ecabe
denominator: 50 files (tree 50, host 50)
match=48 digest_mismatch=2 host_only=0 tree_only=0
  MISMATCH app/sprint_view.py host=5fec947749e04928 tree=e87e983e4633ed88
  MISMATCH app/tools.py host=9a95dd96a7a37257 tree=fa30b2722bc2d30f
running process start (epoch, /proc/<MainPID> ctime)=1788980885; files modified after it: 0
VERDICT: PASS-OGP1-AC1
```

AC4 determinism: two runs, printed lines identical after removing per-read timestamps (8 of 8 lines).

**AC11 discrimination (2026-09-16, CloudWatch retention-boundary bisection -- row `NFRA_OPLGTW-W2-S4`):** the same
`cloudwatch get-metric-statistics` call (AWS/ApplicationELB TargetResponseTime, ExtendedStatistics p95, this ALB),
StartTime/Period walked day-by-day with EndTime fixed:

```
width= 1h .. 14d : exactly 1 Datapoint every time (e.g. 14d -> SampleCount 43642, p95 ~0.55s)
width=15d        : 2 Datapoints, SampleCount [10.0, 45233.0]
width=16d        : 2 Datapoints, SampleCount [46676.0, 10.0]
width=30d (first build's window) : 2 Datapoints, SampleCount [10.0, 79222.0], p95 of the [0] one = 0.031s
```
The rebuilt AC11 (AC11_WINDOW_DAYS=14, under the boundary) reads exactly 1 datapoint, sample_count=43745,
p95=0.5535s (553.5 ms) -- consistent with the dominant bucket every 15d/16d/30d probe above also showed
(~0.55s), confirming 31 ms (the unfixed build's figure) was the defect, not the baseline.

## AWS command log census (AC13's own read)

**2026-09-15 (superseded; the order's first run, before the amendment):**

```
instrument: this probe reads org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/command_log.jsonl (one row per AWS call, written by aws())
vintage: 2026-09-15T11:01:03Z
denominator: 57 AWS call(s) in the command log
read-verb calls (Describe/Get/List/Head): 49 of 57
per operation: {'dynamodb:DescribeTable': 1, 'ec2:DescribeInstances': 1, 'elbv2:DescribeListeners': 1, 'elbv2:DescribeLoadBalancerAttributes': 1, 'elbv2:DescribeLoadBalancers': 1, 'elbv2:DescribeRules': 2, 'iam:GetPolicy': 1, 'iam:GetPolicyVersion': 1, 'iam:GetRole': 5, 'iam:GetRolePolicy': 8, 'iam:ListAttachedRolePolicies': 1, 'iam:ListRolePolicies': 1, 's3api:GetBucketEncryption': 2, 's3api:GetBucketNotificationConfiguration': 1, 's3api:GetBucketPolicyStatus': 2, 's3api:GetBucketVersioning': 2, 's3api:GetObject': 2, 's3api:GetPublicAccessBlock': 2, 's3api:ListObjectsV2': 3, 'ssm:GetCommandInvocation': 9, 'ssm:SendCommand': 8, 'sts:GetCallerIdentity': 1, 'wafv2:GetWebAclForResource': 1}
non-read-verb calls: 8 {'ssm:SendCommand': 8}
VERDICT: FAIL-OGP1-AC13 8 of 57 calls are not Describe/Get/List/Head: {'ssm:SendCommand': 8}
```

**2026-09-16 (current, rebuilt AC13):** full printed output is under "AC13 rebuilt output" above; denominator grew
from 57 to 77 as this re-hand's own AC11 (CloudWatch) and AC12 (DynamoDB) calls were logged (all Describe/Get/Scan,
zero new SendCommand); the 8 historical SendCommand rows are unchanged and are the ones AC13 now admits by
regenerating and printing their script text.

Rows in command_log.jsonl: 77 total (1 hand-made sts GetCallerIdentity row + 56 from the 2026-09-15 run + 20 from
this re-hand's AC11/AC12/AC13 dry-run and recorded invocations, all read verbs).

## Interpreter

**2026-09-15 run** (worktree `/c/tmp/wk-oplgtw-1-2`): built once, `py -3.12 -m venv --system-site-packages .venv-og
&& .venv-og/Scripts/python -m pip install -r infra/aws/ec2/opal-gateway/requirements.txt msal moto pytest` (rc=0).
`.venv-og/Scripts/python -m pip freeze` (318 lines; --system-site-packages, so the host Python's packages are
included):

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

**2026-09-16 re-hand** (worktree `/c/tmp/wk-oplgtw-1-2d`, `.venv-og` did not exist here): built once, same command
(rc=0). `.venv-og/Scripts/python -m pip freeze` (318 lines) is byte-identical to the 2026-09-15 freeze above except
`duckdb==1.2.2` (was `1.5.0`) -- not re-embedded; `diff <(tr -d '\r' < old) <(tr -d '\r' < new)` shows exactly that
one line.

## Proof-of-spec check

**2026-09-15:** `py -3.12 .tools/proof-of-spec-check.py <instance> OGP1-AC1,...,OGP1-AC13` -> `INVALID (rc=1)`
(AC11/AC12/AC13 FAIL by design, order stayed `pending`); violations=0 mechanical, acceptance rows=13,
invocation-alignment 13/13, surprises 3 of 3 resolve to a channel row.

**2026-09-16 (this re-hand, final):** same command against the rebuilt instance -> result recorded at commit time
below (13 of 13 PASS by output is the mechanical precondition for `complete`; the checker's own exit code is the
verdict, per Rule 22's evidence law -- never re-derived by prose here).
