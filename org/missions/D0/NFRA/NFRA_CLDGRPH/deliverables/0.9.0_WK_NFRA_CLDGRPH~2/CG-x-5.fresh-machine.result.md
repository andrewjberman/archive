# CG-x-5 -- FWD-5 EXERCISED: a machine that has never held the graph asked and was answered

**Cell:** CG-x-5 | **TO:** NFRA_CLDGRPH.TO-CG-D-6 | **Assignee:** 0.9.0_WK_NFRA_CLDGRPH~2 (spine-v3 worker subagent of 2.0.0_SA_COO~A)
**Branch:** wk-NFRA_CLDGRPH-2 | **Base:** CLOUD @4e30d6b635 | **Date (UTC):** 2026-09-04

## The comparison object

```json
{
  "machine": "worktree C:/Users/AndrewBerman/Desktop/wk-NFRA_CLDGRPH-2 on Andrew",
  "local_db_present_before": false,
  "local_db_present_after": false,
  "question": "How many CloudNodes of each node_type does the estate hold?",
  "cypher": "MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t",
  "first_try_rc": 0,
  "answer_json": [
    {
      "t": "C2Motif",
      "c": 6303
    },
    {
      "t": "MS_FILE",
      "c": 5049
    },
    {
      "t": "Field",
      "c": 4969
    },
    {
      "t": "JSXElement",
      "c": 2205
    },
    {
      "t": "JSXRender",
      "c": 1433
    },
    {
      "t": "PipelineFunction",
      "c": 1201
    },
    {
      "t": "MS_FOLDER",
      "c": 1085
    },
    {
      "t": "TypeDecl",
      "c": 807
    },
    {
      "t": "IAM_POLICY",
      "c": 483
    },
    {
      "t": "ReactComponent",
      "c": 442
    },
    {
      "t": "Module",
      "c": 374
    },
    {
      "t": "Prop",
      "c": 359
    },
    {
      "t": "LOG_GROUP",
      "c": 250
    },
    {
      "t": "S3Key",
      "c": 232
    },
    {
      "t": "IAM_ROLE",
      "c": 216
    },
    {
      "t": "LAMBDA",
      "c": 203
    },
    {
      "t": "Component",
      "c": 199
    },
    {
      "t": "EVENT_RULE",
      "c": 142
    },
    {
      "t": "PipelineScript",
      "c": 133
    },
    {
      "t": "Endpoint",
      "c": 125
    },
    {
      "t": "Hook",
      "c": 111
    },
    {
      "t": "DataFetch",
      "c": 106
    },
    {
      "t": "EVENT_SOURCE",
      "c": 95
    },
    {
      "t": "PanelCluster",
      "c": 91
    },
    {
      "t": "SECRET",
      "c": 87
    },
    {
      "t": "API_ROUTE",
      "c": 86
    },
    {
      "t": "ReactQueryKey",
      "c": 57
    },
    {
      "t": "CW_ALARM",
      "c": 51
    },
    {
      "t": "ServedURL",
      "c": 45
    },
    {
      "t": "DYNAMODB_TABLE",
      "c": 37
    },
    {
      "t": "S3_BUCKET",
      "c": 34
    },
    {
      "t": "EC2_INSTANCE",
      "c": 32
    },
    {
      "t": "SECURITY_GROUP",
      "c": 26
    },
    {
      "t": "SERVICE_PRINCIPAL",
      "c": 21
    },
    {
      "t": "SSM_DOCUMENT",
      "c": 20
    },
    {
      "t": "SQS_QUEUE",
      "c": 19
    },
    {
      "t": "INSTANCE_PROFILE",
      "c": 18
    },
    {
      "t": "SCHEDULE",
      "c": 18
    },
    {
      "t": "MS_USER",
      "c": 16
    },
    {
      "t": "SNS_TOPIC",
      "c": 16
    },
    {
      "t": "LAMBDA_LAYER",
      "c": 15
    },
    {
      "t": "Page",
      "c": 15
    },
    {
      "t": "S3_BUCKET_POLICY",
      "c": 15
    },
    {
      "t": "KMS_KEY",
      "c": 12
    },
    {
      "t": "ECS_TASK_DEFINITION",
      "c": 9
    },
    {
      "t": "API_GW",
      "c": 5
    },
    {
      "t": "C3System",
      "c": 4
    },
    {
      "t": "CODEBUILD_PROJECT",
      "c": 4
    },
    {
      "t": "IAM_USER",
      "c": 4
    },
    {
      "t": "Pipeline",
      "c": 3
    },
    {
      "t": "ROUTE53_RECORD",
      "c": 3
    },
    {
      "t": "VPC_ENDPOINT",
      "c": 3
    },
    {
      "t": "CLOUDFRONT_DISTRIBUTION",
      "c": 2
    },
    {
      "t": "ECS_CLUSTER",
      "c": 1
    },
    {
      "t": "LOAD_BALANCER",
      "c": 1
    },
    {
      "t": "MS_LIBRARY",
      "c": 1
    },
    {
      "t": "MS_SITE",
      "c": 1
    },
    {
      "t": "STATE_MACHINE",
      "c": 1
    }
  ],
  "vintage_line": "VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]",
  "laptop_seat_comparison": "ISSUER'S AT THE DRAIN -- see the round-4 step log"
}
```

## What was proven, in the order it was proven

1. **ABSENCE FIRST, then the ask.** Before any query left this machine, `infra/aws/globgrph/kuzu_nessie_db`
   was proven absent by two independent reads: a name census over the directory listing
   (`ls infra/aws/globgrph/ | grep -c kuzu_nessie_db` -> `0`) and a direct stat
   (`ls -d infra/aws/globgrph/kuzu_nessie_db` -> `ls: cannot access ...: No such file or directory`, rc=2).
   The whole-directory listing is in the transcript section below: none of its entries is the DB or any of
   its `._refresh_status.json` / `.fallback.jsonl` / `.rebuild.tmp` / `.kuzu_nessie_load.lock` siblings.
   DENOMINATOR: 0 of 60 entries (the `ls infra/aws/globgrph/` name list, wc -l = 60) match `kuzu_nessie_db`.
2. **ONE ask, answered on the FIRST try.** `bash .tools/comp-kuzu --json "<cypher>"` returned rc=0 with a
   58-row JSON array on stdout and the FWD-3 disclosure line on stderr. No retry was made and none was
   needed; had it failed, the rc and the error text would stand here as a FAIL.
3. **The reader did not become a builder.** The same two absence reads re-run after both asks:
   census `0`, state `absent`. Nothing was created under `infra/aws/globgrph/` by the ask.

## The answer (58 node_type rows, deterministic ordering `c DESC, t`)

Total CloudNodes across all types: **27295**. Top of the distribution: C2Motif=6303, MS_FILE=5049, Field=4969, JSXElement=2205, JSXRender=1433.
Anchor value for the issuer's cross-seat comparison: **LAMBDA=203**.

Vintage line, verbatim and unmodified (this client runs no clock):

```
VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]
```

## The laptop-seat comparison is NOT mine

Per the order, `2.0.0_SA_COO~A` runs the identical Cypher from the main workspace (a laptop seat that still
holds the local graph until CG-s-8 retires it) and records both answers in
`org/missions/D0/NFRA/NFRA_CLDGRPH/ledger/STEP_LOG.2.0.0_SA_COO~A.round4.json`; `3.0.0_SA_CVO` grades the
pair at L9 as D6-AC4. My half is recorded above WITH NO VERDICT. The vintage line is what makes the two
comparable: two readers of one served artifact at one vintage must agree row-for-row; readers at different
vintages are compared on the vintage line, not on the rows. My vintage is
`2026-09-04T16:38:39.485910+00:00`, manifest `c3ba0330e306`, prefix
`projection/2026-09-04T16:38:39.485910+00:00/`.

## Instrument note

The absence is a property of THIS worktree, not of the device: `git worktree add -b wk-NFRA_CLDGRPH-2 <path>
CLOUD` checks out tracked content only, and `infra/aws/globgrph/kuzu_nessie_db` is gitignored, so no local
database can arrive with the checkout. That is exactly the cell's stated form -- "site Z, OR a fresh
checkout with the path absent, proven by an `ls`" -- and the ls is the proof, taken before the ask rather
than inferred from the checkout mechanism.
The client itself cannot open a local path even if one existed: `infra/aws/globgrph/kuzu_cli.py` has no
`--db-path`, no `--mode` and no refresh flag, and its only data path is `projection_client.query()` over the
gateway's `/graph/cypher` route (both files read at HEAD 4e30d6b635 this turn).

## Raw transcript -- the deliverable run (bash fresh_ask.sh, stdout+stderr interleaved)

```
TS_START=2026-09-04T17:34:23Z
HOSTNAME=Andrew
MACHINE=worktree C:/Users/AndrewBerman/Desktop/wk-NFRA_CLDGRPH-2
QUESTION=How many CloudNodes of each node_type does the estate hold?
CYPHER=MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t
DB_NAME_CENSUS_BEFORE=0
LOCAL_DB_BEFORE=absent
--- ASK 1: comp-kuzu --json (THE FIRST TRY) ---
FIRST_TRY_RC=0
--- ASK 1 stdout (the comparison object) ---
[
  {
    "t": "C2Motif",
    "c": 6303
  },
  {
    "t": "MS_FILE",
    "c": 5049
  },
  {
    "t": "Field",
    "c": 4969
  },
  {
    "t": "JSXElement",
    "c": 2205
  },
  {
    "t": "JSXRender",
    "c": 1433
  },
  {
    "t": "PipelineFunction",
    "c": 1201
  },
  {
    "t": "MS_FOLDER",
    "c": 1085
  },
  {
    "t": "TypeDecl",
    "c": 807
  },
  {
    "t": "IAM_POLICY",
    "c": 483
  },
  {
    "t": "ReactComponent",
    "c": 442
  },
  {
    "t": "Module",
    "c": 374
  },
  {
    "t": "Prop",
    "c": 359
  },
  {
    "t": "LOG_GROUP",
    "c": 250
  },
  {
    "t": "S3Key",
    "c": 232
  },
  {
    "t": "IAM_ROLE",
    "c": 216
  },
  {
    "t": "LAMBDA",
    "c": 203
  },
  {
    "t": "Component",
    "c": 199
  },
  {
    "t": "EVENT_RULE",
    "c": 142
  },
  {
    "t": "PipelineScript",
    "c": 133
  },
  {
    "t": "Endpoint",
    "c": 125
  },
  {
    "t": "Hook",
    "c": 111
  },
  {
    "t": "DataFetch",
    "c": 106
  },
  {
    "t": "EVENT_SOURCE",
    "c": 95
  },
  {
    "t": "PanelCluster",
    "c": 91
  },
  {
    "t": "SECRET",
    "c": 87
  },
  {
    "t": "API_ROUTE",
    "c": 86
  },
  {
    "t": "ReactQueryKey",
    "c": 57
  },
  {
    "t": "CW_ALARM",
    "c": 51
  },
  {
    "t": "ServedURL",
    "c": 45
  },
  {
    "t": "DYNAMODB_TABLE",
    "c": 37
  },
  {
    "t": "S3_BUCKET",
    "c": 34
  },
  {
    "t": "EC2_INSTANCE",
    "c": 32
  },
  {
    "t": "SECURITY_GROUP",
    "c": 26
  },
  {
    "t": "SERVICE_PRINCIPAL",
    "c": 21
  },
  {
    "t": "SSM_DOCUMENT",
    "c": 20
  },
  {
    "t": "SQS_QUEUE",
    "c": 19
  },
  {
    "t": "INSTANCE_PROFILE",
    "c": 18
  },
  {
    "t": "SCHEDULE",
    "c": 18
  },
  {
    "t": "MS_USER",
    "c": 16
  },
  {
    "t": "SNS_TOPIC",
    "c": 16
  },
  {
    "t": "LAMBDA_LAYER",
    "c": 15
  },
  {
    "t": "Page",
    "c": 15
  },
  {
    "t": "S3_BUCKET_POLICY",
    "c": 15
  },
  {
    "t": "KMS_KEY",
    "c": 12
  },
  {
    "t": "ECS_TASK_DEFINITION",
    "c": 9
  },
  {
    "t": "API_GW",
    "c": 5
  },
  {
    "t": "C3System",
    "c": 4
  },
  {
    "t": "CODEBUILD_PROJECT",
    "c": 4
  },
  {
    "t": "IAM_USER",
    "c": 4
  },
  {
    "t": "Pipeline",
    "c": 3
  },
  {
    "t": "ROUTE53_RECORD",
    "c": 3
  },
  {
    "t": "VPC_ENDPOINT",
    "c": 3
  },
  {
    "t": "CLOUDFRONT_DISTRIBUTION",
    "c": 2
  },
  {
    "t": "ECS_CLUSTER",
    "c": 1
  },
  {
    "t": "LOAD_BALANCER",
    "c": 1
  },
  {
    "t": "MS_LIBRARY",
    "c": 1
  },
  {
    "t": "MS_SITE",
    "c": 1
  },
  {
    "t": "STATE_MACHINE",
    "c": 1
  }
]
--- ASK 1 stderr (the disclosure) ---
VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]
--- ASK 2: comp-kuzu table mode (same statement) ---
TABLE_RC=0
t                        c   
-----------------------  ----
C2Motif                  6303
MS_FILE                  5049
Field                    4969
JSXElement               2205
JSXRender                1433
PipelineFunction         1201
MS_FOLDER                1085
TypeDecl                 807 
IAM_POLICY               483 
ReactComponent           442 
Module                   374 
Prop                     359 
LOG_GROUP                250 
S3Key                    232 
IAM_ROLE                 216 
LAMBDA                   203 
Component                199 
EVENT_RULE               142 
PipelineScript           133 
Endpoint                 125 
Hook                     111 
DataFetch                106 
EVENT_SOURCE             95  
PanelCluster             91  
SECRET                   87  
API_ROUTE                86  
ReactQueryKey            57  
CW_ALARM                 51  
ServedURL                45  
DYNAMODB_TABLE           37  
S3_BUCKET                34  
EC2_INSTANCE             32  
SECURITY_GROUP           26  
SERVICE_PRINCIPAL        21  
SSM_DOCUMENT             20  
SQS_QUEUE                19  
INSTANCE_PROFILE         18  
SCHEDULE                 18  
MS_USER                  16  
SNS_TOPIC                16  
LAMBDA_LAYER             15  
Page                     15  
S3_BUCKET_POLICY         15  
KMS_KEY                  12  
ECS_TASK_DEFINITION      9   
API_GW                   5   
C3System                 4   
CODEBUILD_PROJECT        4   
IAM_USER                 4   
Pipeline                 3   
ROUTE53_RECORD           3   
VPC_ENDPOINT             3   
CLOUDFRONT_DISTRIBUTION  2   
ECS_CLUSTER              1   
LOAD_BALANCER            1   
MS_LIBRARY               1   
MS_SITE                  1   
STATE_MACHINE            1   

(58 rows)
--- ASK 2 stderr (the disclosure) ---
VINTAGE: Built from the estate as of 2026-09-04 16:38:39 UTC.  [vintage=2026-09-04T16:38:39.485910+00:00 manifest=c3ba0330e306 prefix=projection/2026-09-04T16:38:39.485910+00:00/]
DB_NAME_CENSUS_AFTER=0
LOCAL_DB_AFTER=absent
TS_END=2026-09-04T17:34:41Z
```

## Raw transcript -- the absence proof taken BEFORE the ask (separate, earlier reads)

```
2026-09-04T17:30:42Z
$ ls -la infra/aws/globgrph/ | grep -c kuzu_nessie_db
0
rc=1   (grep -c rc=1 means ZERO matching lines; the printed count 0 is the verdict)
2026-09-04T17:30:44Z
$ ls -d infra/aws/globgrph/kuzu_nessie_db; echo rc=$?
ls: cannot access 'infra/aws/globgrph/kuzu_nessie_db': No such file or directory
rc=2
2026-09-04T17:30:45Z
$ ls infra/aws/globgrph/ | grep -c kuzu_nessie_db
0

POSITIVE CONTROL on the same instrument (it CAN return non-zero):
$ ls .tools/ | grep -c comp-kuzu
1

POSITIVE CONTROL on the same state predicate (it CAN say present):
$ if [ -e infra/aws/globgrph/kuzu_cli.py ]; then echo CONTROL_STATE=present; else echo CONTROL_STATE=absent; fi
CONTROL_STATE=present
```

## Directory listing of infra/aws/globgrph/ at the moment of the absence proof (names only)

```
Dockerfile
__pycache__
_canonical.py
_provenance.py
build-derive-image.sh
buildspec.yml
c2c3_liveness_acceptance.py
canon_motif_scorer.py
code_heat_emit.py
code_heat_parity.py
comp_cluster_cli.py
comp_debt.py
comp_debt_baseline.json
comp_detect.py
comp_learns_produce.py
comp_learns_status.py
comp_learns_views.sql
cse_emit_agent.py
cse_emit_deploy.py
cse_emit_frontend_coevolution.py
cse_emit_graphhead.py
cse_emit_promote.py
cse_producers_nightly.py
cse_seed
cse_store.py
debtscan_canon_scorer.py
debtscan_scorecard_latest.json
derive_runner.py
derive_stitch.py
emit_fedobs_snap.py
extract_gold_compute.py
extract_pipeline_cloud.py
extract_portal_stitch.py
fedobs
freshness_alarm
iceberg_parity.py
kuzu_ac_traversals.py
kuzu_cli.py
kuzu_cost_enrich.py
kuzu_incremental_refresh.py
kuzu_load.py
kuzu_nessie_load.py
kuzu_stitch_load.py
ms_cloud_extract.py
node_health.py
probe_ifmatch_cas.py
projection_client.py
projection_server.py
projection_worker.py
publish_contract_integrity.py
resource_summaries_store.py
snap_store.py
tests
tool_activity_emit.py
tool_activity_emit_local.sh
tool_activity_freshness
tool_activity_parity.py
trino_catalog_parity.py
tsgraph_detect_baseline.json
tsgraph_detectors.yaml
```

## Bounds honoured

No local graph was created, copied, downloaded or rebuilt; no engine was run; no `.py` was edited; nothing
was written to S3. The only writes are this record, `fresh_ask.sh`, the proof instance and the TO status
flip -- all inside this order's `<paths>` plus the assignee's deliverables folder.
