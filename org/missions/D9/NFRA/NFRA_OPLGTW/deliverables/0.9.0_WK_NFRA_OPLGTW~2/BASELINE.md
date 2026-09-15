# NFRA_OPLGTW OG-p-1 -- deployed parity and pre-change baseline

Rendered from `BASELINE.json` by `probes/og_p1.py render-md`. Each section is one criterion: the probe's own printed measurement (instrument, UTC vintage, denominator) and its verdict line, verbatim. READ ONLY: every value below came from a read; nothing in AWS or on the host was changed.

## OGP1-AC1

- measured: 2026-09-15T10:53:56Z
- instrument: SSM AWS-RunShellScript sha256sum on i-07dccb1615503ac99 (/opt/opal-gateway) vs git blob sha256 at 7bd89b5d71b8d488d9e8c4168513193c9d6a9ec2 (infra/aws/ec2/opal-gateway); ssm dff40742-2145-45c5-8fbf-f3b560b7d4dd Success at 2026-09-15T10:53:51.245Z
- denominator: 50
- verdict: `VERDICT: PASS-OGP1-AC1`

```
instrument: SSM AWS-RunShellScript sha256sum on i-07dccb1615503ac99 (/opt/opal-gateway) vs git blob sha256 at 7bd89b5d71b8d488d9e8c4168513193c9d6a9ec2 (infra/aws/ec2/opal-gateway); ssm dff40742-2145-45c5-8fbf-f3b560b7d4dd Success at 2026-09-15T10:53:51.245Z
vintage: 2026-09-15T10:53:56Z  deployed_commit(manifest)=7bd89b5d71b8d488d9e8c4168513193c9d6a9ec2 compared_commit=7bd89b5d71b8d488d9e8c4168513193c9d6a9ec2
denominator: 50 files (tree 50, host 50)
match=50 digest_mismatch=0 host_only=0 tree_only=0
running process start (epoch, /proc/<MainPID> ctime)=1788980885; files modified after it: 0
VERDICT: PASS-OGP1-AC1
```

## OGP1-AC2

- measured: 2026-09-15T10:54:14Z
- instrument: SSM AWS-RunShellScript on i-07dccb1615503ac99 (ssm 19c2fe66-894d-4bd2-9b34-0e43101a2be7 at 2026-09-15T10:54:04.707Z); cross-check ec2 DescribeInstances
- denominator: 51
- verdict: `VERDICT: PASS-OGP1-AC2`

```
instrument: SSM AWS-RunShellScript on i-07dccb1615503ac99 (ssm 19c2fe66-894d-4bd2-9b34-0e43101a2be7 at 2026-09-15T10:54:04.707Z); cross-check ec2 DescribeInstances
vintage: 2026-09-15T10:54:14Z
instance_type host DMI product_name='t4g.nano' cloud-init cache='t4g.nano' | EC2 API='t4g.nano'
architecture host uname -m='aarch64' | EC2 API='arm64'
kernel=6.1.175-219.357.amzn2023.aarch64 nproc=2 MemTotal:         428644 kB
unit: ActiveState=active SubState=running MainPID=757114 ActiveEnterTimestamp=Wed 2026-09-09 19:08:05 UTC NRestarts=0
process tree under MainPID: 1 process(es): pid=757114 ppid=1 comm=uvicorn rss_kb=128132 etimes=488760
worker count: running argv --workers=1, unit ExecStart --workers=1, child processes of MainPID=0
main argv: /opt/opal-gateway/.venv/bin/python3.11 /opt/opal-gateway/.venv/bin/uvicorn app.server:app --host 0.0.0.0 --port 8080 --workers 1
python: Python 3.11.15; pyvenv.cfg version=3.11.15
installed packages (dist-info dirs in the service venv): denominator 51
  annotated_types==0.8.0
  anyio==4.14.2
  attrs==26.1.0
  boto3==1.43.72
  botocore==1.43.72
  certifi==2026.7.22
  cffi==2.1.1
  charset_normalizer==3.5.0
  click==8.4.2
  cryptography==50.0.0
  h11==0.16.0
  httpcore2==2.10.0
  httpcore==1.0.9
  httptools==0.8.0
  httpx2==2.10.0
  httpx==0.28.1
  httpx_sse==0.4.3
  idna==3.18
  jmespath==1.1.0
  jsonschema==4.26.0
  jsonschema_specifications==2025.9.1
  mcp==1.28.0
  mcp_types==2.0.0
  msal==1.37.0
  opentelemetry_api==1.44.0
  pip==26.2.1
  pycparser==3.0
  pydantic==2.13.4
  pydantic_core==2.46.4
  pydantic_settings==2.15.0
  pyjwt==2.13.0
  python_dateutil==2.9.0.post0
  python_dotenv==1.2.2
  python_multipart==0.0.32
  pyyaml==6.0.3
  referencing==0.37.0
  requests==2.34.2
  rpds_py==2026.6.3
  s3transfer==0.19.2
  setuptools==65.5.1
  six==1.17.0
  sse_starlette==3.4.8
  starlette==1.6.0
  truststore==0.10.4
  typing_extensions==4.16.0
  typing_inspection==0.4.4
  urllib3==2.7.0
  uvicorn==0.52.3
  uvloop==0.22.1
  watchfiles==1.2.0
  websockets==17.0.1
VERDICT: PASS-OGP1-AC2
```

## OGP1-AC3

- measured: 2026-09-15T10:49:27Z
- instrument: elbv2 DescribeLoadBalancers/DescribeLoadBalancerAttributes/DescribeListeners/DescribeRules, wafv2 GetWebACLForResource via .tools/aws
- denominator: 10
- verdict: `VERDICT: PASS-OGP1-AC3`

```
instrument: elbv2 DescribeLoadBalancers/DescribeLoadBalancerAttributes/DescribeListeners/DescribeRules, wafv2 GetWebACLForResource via .tools/aws
vintage: 2026-09-15T10:49:27Z
load balancer arn:aws:elasticloadbalancing:us-east-1:313476888478:loadbalancer/app/opal-gateway/89166a68f337e5a4 (read 2026-09-15T10:49:06Z) scheme=internet-facing state=active | recorded ARN MATCH
idle_timeout.timeout_seconds=60 (read 2026-09-15T10:49:11Z, resource arn:aws:elasticloadbalancing:us-east-1:313476888478:loadbalancer/app/opal-gateway/89166a68f337e5a4) | recorded 60 MATCH
denominator: 2 listener(s), 8 rule(s)
listener arn:aws:elasticloadbalancing:us-east-1:313476888478:listener/app/opal-gateway/89166a68f337e5a4/2904a0140214f982 HTTPS:443 (read 2026-09-15T10:49:15Z) default actions: forward, authenticate-oidc
  rule prio=10 arn:aws:elasticloadbalancing:us-east-1:313476888478:listener-rule/app/opal-gateway/89166a68f337e5a4/2904a0140214f982/4ea29ffe7abbebf4 (read 2026-09-15T10:49:18Z) if [path-pattern=['/mcp/*', '/mcp', '/authorize', '/register', '/token']] -> forward
  rule prio=20 arn:aws:elasticloadbalancing:us-east-1:313476888478:listener-rule/app/opal-gateway/89166a68f337e5a4/2904a0140214f982/6f65117747bef7d2 (read 2026-09-15T10:49:18Z) if [path-pattern=['/.well-known/oauth-authorization-server', '/callback', '/.well-known/oauth-protected-resource', '/.well-known/jwks.json']] -> forward
  rule prio=30 arn:aws:elasticloadbalancing:us-east-1:313476888478:listener-rule/app/opal-gateway/89166a68f337e5a4/2904a0140214f982/43a3ad4399df52d7 (read 2026-09-15T10:49:18Z) if [path-pattern=['/otp/fetch', '/otp/health', '/otp/token']] -> forward
  rule prio=31 arn:aws:elasticloadbalancing:us-east-1:313476888478:listener-rule/app/opal-gateway/89166a68f337e5a4/2904a0140214f982/d2acd598fe9d729b (read 2026-09-15T10:49:18Z) if [path-pattern=['/ms/site_children', '/ms/onedrive_children', '/ms/health', '/ms/sites', '/ms/search']] -> forward
  rule prio=32 arn:aws:elasticloadbalancing:us-east-1:313476888478:listener-rule/app/opal-gateway/89166a68f337e5a4/2904a0140214f982/ec87188ebb2935a7 (read 2026-09-15T10:49:18Z) if [path-pattern=['/graph/cypher', '/graph/health']] -> forward
  rule prio=33 arn:aws:elasticloadbalancing:us-east-1:313476888478:listener-rule/app/opal-gateway/89166a68f337e5a4/2904a0140214f982/99e7defdf8f5a7d6 (read 2026-09-15T10:49:18Z) if [path-pattern=['/ms/token']] -> forward
  rule prio=default arn:aws:elasticloadbalancing:us-east-1:313476888478:listener-rule/app/opal-gateway/89166a68f337e5a4/2904a0140214f982/7742954dae1efc37 (read 2026-09-15T10:49:18Z) if [] -> forward, authenticate-oidc
listener arn:aws:elasticloadbalancing:us-east-1:313476888478:listener/app/opal-gateway/89166a68f337e5a4/a72b21be9d935e5c HTTP:80 (read 2026-09-15T10:49:15Z) default actions: redirect
  rule prio=default arn:aws:elasticloadbalancing:us-east-1:313476888478:listener-rule/app/opal-gateway/89166a68f337e5a4/a72b21be9d935e5c/e3f2f38934d2225d (read 2026-09-15T10:49:23Z) if [] -> redirect
default browser OIDC action on arn:aws:elasticloadbalancing:us-east-1:313476888478:listener/app/opal-gateway/89166a68f337e5a4/2904a0140214f982: issuer=https://login.microsoftonline.com/6810043e-d171-4adc-9975-068b35e179da/v2.0 client_id=sha256:707f59440e6d435d on_unauthenticated=authenticate scope=openid profile email session_timeout=604800
WAF association (read 2026-09-15T10:49:27Z, resource arn:aws:elasticloadbalancing:us-east-1:313476888478:loadbalancer/app/opal-gateway/89166a68f337e5a4): opal-gateway-waf arn:aws:wafv2:us-east-1:313476888478:regional/webacl/opal-gateway-waf/181df35e-e886-40c6-a8dc-9d0b60346a44 rules=5
VERDICT: PASS-OGP1-AC3
```

## OGP1-AC4

- measured: 2026-09-15T10:47:40Z
- instrument: s3api GetBucketVersioning/GetBucketEncryption/GetPublicAccessBlock/GetBucketPolicyStatus via .tools/aws
- denominator: 7
- verdict: `VERDICT: PASS-OGP1-AC4`

```
instrument: s3api GetBucketVersioning/GetBucketEncryption/GetPublicAccessBlock/GetBucketPolicyStatus via .tools/aws
vintage: 2026-09-15T10:47:40Z  bucket=opal-data-assets
denominator: 4 reads, 7 values (versioning, encryption, 4 public-access-block flags, policy status)
versioning=Enabled (read 2026-09-15T10:47:26Z) | recorded Enabled MATCH
default encryption SSEAlgorithm=['AES256'] KMSMasterKeyID=[None] BucketKeyEnabled=[False] (read 2026-09-15T10:47:30Z) | recorded AES256 MATCH
public access block {'BlockPublicAcls': True, 'IgnorePublicAcls': True, 'BlockPublicPolicy': True, 'RestrictPublicBuckets': True} (read 2026-09-15T10:47:34Z) | recorded all four true MATCH
policy status {'IsPublic': False} (read 2026-09-15T10:47:40Z)
VERDICT: PASS-OGP1-AC4
```

## OGP1-AC5

- measured: 2026-09-15T10:50:46Z
- instrument: iam GetRole/ListRolePolicies/GetRolePolicy/ListAttachedRolePolicies/GetPolicy/GetPolicyVersion via .tools/aws
- denominator: 10
- verdict: `VERDICT: PASS-OGP1-AC5`

```
instrument: iam GetRole/ListRolePolicies/GetRolePolicy/ListAttachedRolePolicies/GetPolicy/GetPolicyVersion via .tools/aws
vintage: 2026-09-15T10:50:46Z  role=arn:aws:iam::313476888478:role/opal-gateway-role (read 2026-09-15T10:49:57Z) created=2026-08-15T02:32:07Z permissions_boundary=None max_session=3600
denominator: 1 trust document + 8 inline + 1 attached policies
trust sha256=eb54f2b2232042ba statements=1: Allow sts:AssumeRole principal={'Service': 'ec2.amazonaws.com'} cond=[]
inline opal-gateway-assume-emp-roles sha256=bae600a72486ae65 statements=1
    Allow sts:AssumeRole on arn:aws:iam::313476888478:role/opal-mcp-emp-* cond=['StringEquals:sts:ExternalId']
inline opal-gateway-audit-lake-write sha256=305595efe03e65b2 statements=1
    Allow ['s3:PutObject'] on ['arn:aws:s3:::opal-mcp-audit/audit/*'] cond=[]
inline opal-gateway-daily-reports-read sha256=a2c5f99e61c8ced1 statements=2
    Allow ['s3:GetObject'] on ['arn:aws:s3:::opal-data-portal-v2/daily-reports/*'] cond=[]
    Allow ['s3:ListBucket'] on ['arn:aws:s3:::opal-data-portal-v2'] cond=['StringLike:s3:prefix']
inline opal-gateway-golive sha256=3cb567d6eccb2fb4 statements=2
    Allow ['s3:GetObject'] on ['arn:aws:s3:::opal-313476888478-lambda-artifacts/ec2/opal-gateway/*'] cond=[]
    Allow ['secretsmanager:GetSecretValue'] on ['arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/opal-gateway-login-jaQusM', 'arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/opal-gateway-graph-u9Wg85', 'arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/opal-gateway-fernet-ZqfQle', 'arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/opal-gateway-jwt-m0fXOX', 'arn:aws:secretsmanager:us-east-1:313476888478:secret:blackdiamond/49f/otp-gateway-token-asH4JY', 'arn:aws:secretsmanager:us-east-1:313476888478:secret:blackdiamond/cot/otp-gateway-token-T1HlmV', 'arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/ms-ingest-token-mXFTKk'] cond=[]
inline opal-gateway-graph-read-secret-read sha256=9fc621a96309ed1e statements=1
    Allow ['secretsmanager:GetSecretValue'] on arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/mcp/graph-read-token-MGAqlV cond=[]
inline opal-gateway-opal-portal-secret-read sha256=561e04c3a829795b statements=1
    Allow ['secretsmanager:GetSecretValue'] on arn:aws:secretsmanager:us-east-1:313476888478:secret:opal/portal/svc-data-refresh-4QLOH6 cond=[]
inline opal-gateway-queryv0-portal-read sha256=eda213f47ef489dc statements=1
    Allow ['s3:GetObject'] on ['arn:aws:s3:::opal-data-portal-v2/json/*', 'arn:aws:s3:::opal-data-portal-v2/platinum/*'] cond=[]
inline opal-gateway-ycharts-secret-read sha256=89d95973665a5ecb statements=1
    Allow ['secretsmanager:GetSecretValue'] on arn:aws:secretsmanager:us-east-1:313476888478:secret:ycharts/credentials-2deEMz cond=[]
attached arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore v=v2 sha256=3d765f3ba15024b2 statements=3
    Allow ['ssm:DescribeAssociation', 'ssm:GetDeployablePatchSnapshotForInstance', 'ssm:GetDocument', 'ssm:DescribeDocument', 'ssm:GetManifest', 'ssm:GetParameter', 'ssm:GetParameters', 'ssm:ListAssociations', 'ssm:ListInstanceAssociations', 'ssm:PutInventory', 'ssm:PutComplianceItems', 'ssm:PutConfigurePackageResult', 'ssm:UpdateAssociationStatus', 'ssm:UpdateInstanceAssociationStatus', 'ssm:UpdateInstanceInformation'] on * cond=[]
    Allow ['ssmmessages:CreateControlChannel', 'ssmmessages:CreateDataChannel', 'ssmmessages:OpenControlChannel', 'ssmmessages:OpenDataChannel'] on * cond=[]
    Allow ['ec2messages:AcknowledgeMessage', 'ec2messages:DeleteMessage', 'ec2messages:FailMessage', 'ec2messages:GetEndpoint', 'ec2messages:GetMessages', 'ec2messages:SendReply'] on * cond=[]
VERDICT: PASS-OGP1-AC5
```

## OGP1-AC6

- measured: 2026-09-15T10:51:14Z
- instrument: iam GetRole via .tools/aws
- denominator: 2
- verdict: `VERDICT: PASS-OGP1-AC6`

```
instrument: iam GetRole via .tools/aws
vintage: 2026-09-15T10:51:14Z
denominator: 2 role names
GetRole opal-mcp-emp-menachem-schwab-read: NoSuchEntity (rc=255, read 2026-09-15T10:51:11Z)
GetRole opal-mcp-schwab-catalog-read: NoSuchEntity (rc=255, read 2026-09-15T10:51:14Z)
VERDICT: PASS-OGP1-AC6
```

## OGP1-AC7

- measured: 2026-09-15T10:51:39Z
- instrument: dynamodb DescribeTable via .tools/aws
- denominator: 1
- verdict: `VERDICT: PASS-OGP1-AC7`

```
instrument: dynamodb DescribeTable via .tools/aws
vintage: 2026-09-15T10:51:39Z
denominator: 1 table name
DescribeTable opal-gateway-access-state: ResourceNotFound (rc=255)
VERDICT: PASS-OGP1-AC7
```

## OGP1-AC8

- measured: 2026-09-15T10:52:25Z
- instrument: s3api ListObjectsV2 (auto-paginated) + GetObject of the newest marker via .tools/aws
- denominator: 2
- verdict: `VERDICT: PASS-OGP1-AC8`

```
instrument: s3api ListObjectsV2 (auto-paginated) + GetObject of the newest marker via .tools/aws
vintage: 2026-09-15T10:52:25Z  bucket=opal-data-assets
denominator: 2 master prefix(es) under schwab/, 2 with meta/complete/ objects
master 08242234: count=10 (read 2026-09-15T10:52:13Z) newest=schwab/08242234/meta/complete/date=2026-09-14.json last_modified=2026-09-15T10:16:10.000Z newest_by_name=schwab/08242234/meta/complete/date=2026-09-14.json schema_field={'schema': 'opal.silver.complete/v1'} keys=['date', 'declared_source', 'declared_tables', 'disagreement', 'emitted_at', 'master', 'run_id', 'schema', 'written_tables']
master 08335338: count=10 (read 2026-09-15T10:52:21Z) newest=schwab/08335338/meta/complete/date=2026-09-14.json last_modified=2026-09-15T09:46:40.000Z newest_by_name=schwab/08335338/meta/complete/date=2026-09-14.json schema_field={'schema': 'opal.silver.complete/v1'} keys=['date', 'declared_source', 'declared_tables', 'disagreement', 'emitted_at', 'master', 'run_id', 'schema', 'written_tables']
VERDICT: PASS-OGP1-AC8
```

## OGP1-AC9

- measured: 2026-09-15T10:53:02Z
- instrument: s3api GetBucketNotificationConfiguration via .tools/aws
- denominator: 11
- verdict: `VERDICT: PASS-OGP1-AC9`

```
instrument: s3api GetBucketNotificationConfiguration via .tools/aws
vintage: 2026-09-15T10:53:02Z  bucket=opal-data-assets
denominator: 11 notification configuration(s) (11 ObjectCreated); EventBridge enabled=False
ObjectCreated consumers whose filter covers schwab/*/meta/complete/: 1
  COVERS lambda id=advi-49f-silver-complete-accelerator target=arn:aws:lambda:us-east-1:313476888478:function:advi-49f-gold-dispatch events=['s3:ObjectCreated:*'] prefix='schwab/08335338/meta/complete/' suffix='.json'
recorded consumer advi-49f-silver-complete-accelerator: PRESENT prefix='schwab/08335338/meta/complete/'
VERDICT: PASS-OGP1-AC9
```

## OGP1-AC10

- measured: 2026-09-15T10:54:26Z
- instrument: /proc/<pid>/status VmHWM (kernel resident-set high-water mark since the process exec'd), read on the host by SSM; cgroup v2 memory.peak shown beside it (includes page cache, so it is NOT RSS)
- denominator: 1
- verdict: `VERDICT: PASS-OGP1-AC10`

```
instrument: /proc/<pid>/status VmHWM (kernel resident-set high-water mark since the process exec'd), read on the host by SSM; cgroup v2 memory.peak shown beside it (includes page cache, so it is NOT RSS)
vintage: 2026-09-15T10:54:22Z (host clock), ssm 109d3c57-3182-4b35-9b76-6eeeb6315384 at 2026-09-15T10:54:22.151Z
window: process start Wed 2026-09-09 19:08:05 UTC (ps lstart 'Wed Sep  9 19:08:04 2026') -> 2026-09-15T10:54:22Z
denominator: 1 process(es) in the service (MainPID + children)
  pid=757114 VmHWM=188700 kB (184.3 MiB) VmRSS=128132 kB
peak RSS (max VmHWM) = 188700 kB (184.3 MiB)
cgroup /system.slice/opal-gateway.service memory.peak=193552384 memory.current=130736128
VERDICT: PASS-OGP1-AC10
```

## OGP1-AC11

- measured: 2026-09-15T10:57:49Z
- instrument: host-side awk/grep census of the audit record, read by SSM; counts only
- denominator: 78049
- verdict: `VERDICT: FAIL-OGP1-AC11 p95 latency not computable from the audit record: 0 of 78049 records in the window carry a latency/duration field`

```
instrument: host-side awk/grep census of the audit record, read by SSM; counts only
vintage: 2026-09-15T10:57:49Z
source: /opt/opal-gateway/audit.jsonl on the host (audit.py:29-33 local JSONL floor), ssm a6a55353-e24d-4c88-86d8-f7799f9f7f58 at 2026-09-15T10:57:48.332Z
file: size/mtime=20685082 1789461155 lines_total=79091 first_ts=2026-08-15T03:08:41.552149+00:00 last_ts=2026-09-15T08:32:35.705013+00:00
window: 2026-08-16T10:57:38Z -> read time (30 days); records in window=78049 (first in window 2026-08-17T02:03:46.499785+00:00)
top-level keys in window (args collapsed; key name: record count): {'args': 65896, 'caller': 12153, 'credential_class': 12153, 'detail': 65896, 'event': 12153, 'outcome': 65896, 'route': 12153, 'tier': 65896, 'tool': 65896, 'ts': 78049, 'user': 65896}
event records in window (records with no tool): {'gw_cred_observe': 12153}; outcomes: {'confirm_required': 5, 'denied': 64, 'error': 12, 'ok': 65815}
denominator: 78049 audit records in window; per-tool sample counts: {'create_draft': 3, 'find_sharepoint_site': 14, 'get_item': 5, 'get_site_item': 1, 'graph_cypher': 35, 'graph_status': 5, 'list_calendar': 4, 'list_channels': 16, 'list_chats': 33, 'list_email_attachments': 26, 'list_onedrive': 2, 'list_recent_email': 25, 'list_site_files': 8, 'list_teams': 12, 'ms_site_children': 42055, 'ms_sites': 1, 'otp_fetch': 32, 'poll_addressed_teams_messages': 19370, 'profile_site_file': 2, 'query_v0': 40, 'read_channel_messages': 3526, 'read_chat_messages': 81, 'read_document': 5, 'read_email': 82, 'read_site_file': 4, 'read_site_workbook': 8, 'save_email_attachment_to_site': 15, 'search_email': 164, 'search_files': 17, 'search_site_files': 8, 'send_channel_message': 3, 'send_chat_message': 29, 'send_email': 4, 'sprint_view': 4, 'whoami': 163, 'ycharts_freshness': 3, 'ycharts_fund_series': 7, 'ycharts_search': 55, 'ycharts_snapshot_metrics': 20, 'ycharts_time_series': 9}
records carrying any latency/duration key ['duration', 'duration_ms', 'duration_s', 'latency', 'latency_ms', 'elapsed', 'elapsed_ms', 'elapsed_s', 'took_ms']: window=0 all=0
audit.py log_call (audit.py:122-132 at the deployed commit, byte-identical to HEAD) writes ts, user, tool, args, outcome, detail, tier -- no duration field
VERDICT: FAIL-OGP1-AC11 p95 latency not computable from the audit record: 0 of 78049 records in the window carry a latency/duration field
```

## OGP1-AC12

- measured: 2026-09-15T10:58:01Z
- instrument: host-side grep census of the audit record for the client_id key, read by SSM; values digested
- denominator: 78049
- verdict: `VERDICT: FAIL-OGP1-AC12 no client inventory derivable: 0 of 79091 audit records carry a client_id field (audit.py log_call does not write one), so an inventory from it is empty by construction`

```
instrument: host-side grep census of the audit record for the client_id key, read by SSM; values digested
vintage: 2026-09-15T10:58:01Z
source: /opt/opal-gateway/audit.jsonl on the host (audit.py:29-33 local JSONL floor), ssm d9bfff7a-be92-4fd3-b45b-759e9048fad7 at 2026-09-15T10:57:59.318Z
file: size/mtime=20685082 1789461155 lines_total=79091 first_ts=2026-08-15T03:08:41.552149+00:00 last_ts=2026-09-15T08:32:35.705013+00:00
window: 2026-08-16T10:57:49Z -> read time (30 days); records in window=78049 (first in window 2026-08-17T02:03:46.499785+00:00)
top-level keys in window (args collapsed; key name: record count): {'args': 65896, 'caller': 12153, 'credential_class': 12153, 'detail': 65896, 'event': 12153, 'outcome': 65896, 'route': 12153, 'tier': 65896, 'tool': 65896, 'ts': 78049, 'user': 65896}
event records in window (records with no tool): {'gw_cred_observe': 12153}; outcomes: {'confirm_required': 5, 'denied': 64, 'error': 12, 'ok': 65815}
denominator: 78049 audit records in window (79091 in file)
records carrying client_id: window=0 all=0; distinct client_id values (digested): {}
clients are process-local: oauth_as.py:336 @7bd89b5d71 defines the DCR client store as a module-level in-memory dict (_clients), so every registered client is lost on a process restart; the unit pins --workers 1 for this reason (deploy/opal-gateway.service:13-16)
VERDICT: FAIL-OGP1-AC12 no client inventory derivable: 0 of 79091 audit records carry a client_id field (audit.py log_call does not write one), so an inventory from it is empty by construction
```

## OGP1-AC13

- measured: 2026-09-15T11:01:03Z
- instrument: this probe reads org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/command_log.jsonl (one row per AWS call, written by aws())
- denominator: 57
- verdict: `VERDICT: FAIL-OGP1-AC13 8 of 57 calls are not Describe/Get/List/Head: {'ssm:SendCommand': 8}`

```
instrument: this probe reads org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/command_log.jsonl (one row per AWS call, written by aws())
vintage: 2026-09-15T11:01:03Z
denominator: 57 AWS call(s) in the command log
read-verb calls (Describe/Get/List/Head): 49 of 57
per operation: {'dynamodb:DescribeTable': 1, 'ec2:DescribeInstances': 1, 'elbv2:DescribeListeners': 1, 'elbv2:DescribeLoadBalancerAttributes': 1, 'elbv2:DescribeLoadBalancers': 1, 'elbv2:DescribeRules': 2, 'iam:GetPolicy': 1, 'iam:GetPolicyVersion': 1, 'iam:GetRole': 5, 'iam:GetRolePolicy': 8, 'iam:ListAttachedRolePolicies': 1, 'iam:ListRolePolicies': 1, 's3api:GetBucketEncryption': 2, 's3api:GetBucketNotificationConfiguration': 1, 's3api:GetBucketPolicyStatus': 2, 's3api:GetBucketVersioning': 2, 's3api:GetObject': 2, 's3api:GetPublicAccessBlock': 2, 's3api:ListObjectsV2': 3, 'ssm:GetCommandInvocation': 9, 'ssm:SendCommand': 8, 'sts:GetCallerIdentity': 1, 'wafv2:GetWebAclForResource': 1}
non-read-verb calls: 8 {'ssm:SendCommand': 8}
VERDICT: FAIL-OGP1-AC13 8 of 57 calls are not Describe/Get/List/Head: {'ssm:SendCommand': 8}
```

