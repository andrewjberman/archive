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

- measured: 2026-09-16T19:15:11Z
- instrument: cloudwatch GetMetricStatistics AWS/ApplicationELB TargetResponseTime (Statistics SampleCount, ExtendedStatistics p95), one CloudWatch period spanning the whole window, via .tools/aws; elbv2 DescribeLoadBalancers/DescribeTargetGroups resolve the dimensions
- denominator: 2
- verdict: `VERDICT: PASS-OGP1-AC11`

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

## OGP1-AC12

- measured: 2026-09-16T19:01:01Z
- instrument: dynamodb Scan (FilterExpression record_type='oauth_client', ConsistentRead) on opal-gateway-access-state via .tools/aws; deployed-commit source read (git show, no AWS call) for process-locality
- denominator: 7
- verdict: `VERDICT: PASS-OGP1-AC12`

```
instrument: dynamodb Scan (FilterExpression record_type='oauth_client', ConsistentRead) on opal-gateway-access-state via .tools/aws; deployed-commit source read (git show, no AWS call) for process-locality
vintage: 2026-09-16T19:01:01Z
denominator: 7 item(s) scanned, 0 matching record_type='oauth_client' (read 2026-09-16T19:01:01Z)
registered clients (persisted store): 0
process-locality AS MEASURED: deployed_commit=7bd89b5d71 -- app/access_state.py ABSENT at that commit; app/oauth_as.py there still defines an in-memory '_clients' store. So the RUNNING gateway's OAuth client store is process-local (in-memory; workers pinned to 1); the persisted table read above is the durable store OG-a-1/OG-d-1 built at HEAD but not yet released to this host, so today it is independent of process locality either way -- a finding carried to L10 (row NFRA_OPLGTW-W2-S2) is that the audit record still cannot name which client made a given call.
VERDICT: PASS-OGP1-AC12
```

## OGP1-AC13

- measured: 2026-09-16T19:15:53Z
- instrument: this probe reads org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/command_log.jsonl (one row per AWS call, written by aws()); ssm:SendCommand rows are graded against this file's own script-building functions -- this criterion makes no AWS call itself
- denominator: 77
- verdict: `VERDICT: PASS-OGP1-AC13`

```
instrument: this probe reads org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~2/command_log.jsonl (one row per AWS call, written by aws()); ssm:SendCommand rows are graded against this file's own script-building functions -- this criterion makes no AWS call itself
vintage: 2026-09-16T19:15:53Z
denominator: 77 AWS call(s) in the command log
per operation: {'cloudwatch:GetMetricStatistics': 8, 'dynamodb:DescribeTable': 1, 'dynamodb:Scan': 4, 'ec2:DescribeInstances': 1, 'elbv2:DescribeListeners': 1, 'elbv2:DescribeLoadBalancerAttributes': 1, 'elbv2:DescribeLoadBalancers': 5, 'elbv2:DescribeRules': 2, 'elbv2:DescribeTargetGroups': 4, 'iam:GetPolicy': 1, 'iam:GetPolicyVersion': 1, 'iam:GetRole': 5, 'iam:GetRolePolicy': 8, 'iam:ListAttachedRolePolicies': 1, 'iam:ListRolePolicies': 1, 's3api:GetBucketEncryption': 2, 's3api:GetBucketNotificationConfiguration': 1, 's3api:GetBucketPolicyStatus': 2, 's3api:GetBucketVersioning': 2, 's3api:GetObject': 2, 's3api:GetPublicAccessBlock': 2, 's3api:ListObjectsV2': 3, 'ssm:GetCommandInvocation': 9, 'ssm:SendCommand': 8, 'sts:GetCallerIdentity': 1, 'wafv2:GetWebAclForResource': 1}
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
the 5 distinct SSM script text(s) this cell's evidence relies on, verbatim (AC1/AC2/AC10 regenerated identically; AC11/AC12's retired template shown with its per-call cutoff timestamp replaced by a placeholder):
--- AC1 digests (read_only=True) ---
    cd /opt/opal-gateway || exit 3
    echo "### unit"
    systemctl show opal-gateway -p MainPID -p ActiveEnterTimestamp --no-pager
    PID=$(systemctl show opal-gateway -p MainPID --value)
    echo "### pidstart"
    stat -c %Y /proc/$PID 2>&1
    echo "### files"
    find app deploy requirements.txt identity_tool_allowlist.txt -type f ! -path '*/__pycache__/*' ! -name '*.pyc' | LC_ALL=C sort | while IFS= read -r f; do printf '%s %s %s\n' "$(sha256sum < "$f" | cut -c1-64)" "$(stat -c %Y "$f")" "$f"; done
--- AC2 host shape (read_only=True) ---
    echo "### dmi"
    cat /sys/devices/virtual/dmi/id/product_name 2>&1
    cat /sys/devices/virtual/dmi/id/sys_vendor 2>&1
    echo "### cloudinit"
    grep -o '"instance[-_]type": *"[^"]*"' /run/cloud-init/instance-data.json 2>&1 | sort -u
    echo "### arch"
    uname -m
    echo "### kernel"
    uname -r
    echo "### nproc"
    nproc
    echo "### memtotal"
    grep MemTotal /proc/meminfo
    echo "### unit"
    systemctl show opal-gateway -p MainPID -p ActiveState -p SubState -p ActiveEnterTimestamp -p NRestarts -p ExecStart --no-pager
    echo "### ps"
    ps -eo pid=,ppid=,etimes=,rss=,comm=
    echo "### mainargs"
    PID=$(systemctl show opal-gateway -p MainPID --value)
    ps -o args= -p $PID
    echo "### children"
    ps -o pid=,args= --ppid $PID
    echo "### pyv"
    PYTHONDONTWRITEBYTECODE=1 /opt/opal-gateway/.venv/bin/python -V 2>&1
    echo "### pyvenv"
    cat /opt/opal-gateway/.venv/pyvenv.cfg
    echo "### distinfo"
    ls -1d /opt/opal-gateway/.venv/lib/python*/site-packages/*.dist-info | sed 's#.*/##'
--- AC10 peak RSS (read_only=True) ---
    PID=$(systemctl show opal-gateway -p MainPID --value)
    echo "### unit"
    systemctl show opal-gateway -p MainPID -p ActiveEnterTimestamp -p ControlGroup -p MemoryCurrent --no-pager
    echo "### now"
    date -u +%Y-%m-%dT%H:%M:%SZ
    echo "### lstart"
    ps -o lstart= -p $PID
    echo "### procs"
    for p in $PID $(ps -o pid= --ppid $PID); do printf 'pid=%s ' "$p"; grep -E '^(VmHWM|VmRSS):' /proc/$p/status | tr -s ' \t' ' ' | tr '\n' ' '; echo; done
    echo "### cgpeak"
    CG=$(systemctl show opal-gateway -p ControlGroup --value)
    cat /sys/fs/cgroup$CG/memory.peak 2>&1
    echo "### cgcurrent"
    cat /sys/fs/cgroup$CG/memory.current 2>&1
--- AC11 audit latency census (read_only=True) ---
    F=/opt/opal-gateway/audit.jsonl
    echo "### stat"
    stat -c '%s %Y' $F 2>&1
    wc -l < $F
    echo "### first"
    head -1 $F | grep -o '"ts":"[^"]*"'
    echo "### last"
    tail -1 $F | grep -o '"ts":"[^"]*"'
    echo "### window"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) n++ } END { print n+0 }' $F
    echo "### firstinwin"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) { print ts; exit } }' $F
    echo "### tools"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -o '"tool":"[^"]*"' | LC_ALL=C sort | uniq -c
    echo "### events"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -o '"event":"[^"]*"' | LC_ALL=C sort | uniq -c
    echo "### outcomes"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -o '"outcome":"[^"]*"' | LC_ALL=C sort | uniq -c
    echo "### durationkeys"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -c -E '"(duration|duration_ms|duration_s|latency|latency_ms|elapsed|elapsed_ms|elapsed_s|took_ms)":'
    echo "### durationkeys_all"
    grep -c -E '"(duration|duration_ms|duration_s|latency|latency_ms|elapsed|elapsed_ms|elapsed_s|took_ms)":' $F
    echo "### clientid"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -c '"client_id"'
    echo "### clientid_all"
    grep -c '"client_id"' $F
    echo "### clientid_values"
    grep -o '"client_id":"[^"]*"' $F | LC_ALL=C sort | uniq -c
    echo "### topkeys"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | sed -e 's/"args":{[^}]*}/"args":{}/' | grep -o '"[a-z_]*":' | LC_ALL=C sort | uniq -c
--- AC12 audit client census (read_only=True) ---
    F=/opt/opal-gateway/audit.jsonl
    echo "### stat"
    stat -c '%s %Y' $F 2>&1
    wc -l < $F
    echo "### first"
    head -1 $F | grep -o '"ts":"[^"]*"'
    echo "### last"
    tail -1 $F | grep -o '"ts":"[^"]*"'
    echo "### window"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) n++ } END { print n+0 }' $F
    echo "### firstinwin"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) { print ts; exit } }' $F
    echo "### tools"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -o '"tool":"[^"]*"' | LC_ALL=C sort | uniq -c
    echo "### events"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -o '"event":"[^"]*"' | LC_ALL=C sort | uniq -c
    echo "### outcomes"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -o '"outcome":"[^"]*"' | LC_ALL=C sort | uniq -c
    echo "### durationkeys"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -c -E '"(duration|duration_ms|duration_s|latency|latency_ms|elapsed|elapsed_ms|elapsed_s|took_ms)":'
    echo "### durationkeys_all"
    grep -c -E '"(duration|duration_ms|duration_s|latency|latency_ms|elapsed|elapsed_ms|elapsed_s|took_ms)":' $F
    echo "### clientid"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | grep -c '"client_id"'
    echo "### clientid_all"
    grep -c '"client_id"' $F
    echo "### clientid_values"
    grep -o '"client_id":"[^"]*"' $F | LC_ALL=C sort | uniq -c
    echo "### topkeys"
    awk -v since='SINCE_PLACEHOLDER_TS' 'match($0, /"ts":"[^"]*"/) { ts=substr($0,RSTART+6,RLENGTH-7); if (ts>=since) print }' $F | sed -e 's/"args":{[^}]*}/"args":{}/' | grep -o '"[a-z_]*":' | LC_ALL=C sort | uniq -c
VERDICT: PASS-OGP1-AC13
```

