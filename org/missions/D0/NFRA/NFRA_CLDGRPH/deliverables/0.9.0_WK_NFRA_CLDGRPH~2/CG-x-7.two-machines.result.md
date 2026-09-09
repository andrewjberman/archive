# CG-x-7 -- TWO MACHINES, ONE QUESTION, ONE ANSWER (TO-CG-D-8): result

**Worker:** `0.9.0_WK_NFRA_CLDGRPH~2` (spine-v3 subagent of `2.0.0_SA_COO~A`)  
**Branch:** `wk-cldgrph-2-d7`, base `CLOUD` merged at `915d75c4bf`. **Push state: LOCAL** (never pushed).  
**Measured:** 2026-09-09 14:14Z - 14:26Z, every invocation bounded by `timeout`.

---

## CONCLUSION FIRST

**FWD-7 IS EXERCISED. Two machines asked the same question 2.1 seconds apart and returned byte-identical answers under one vintage, and neither machine holds the canonical graph.**

- **Identical answers:** 58 node-type rows on both sides, compared as canonical JSON (sorted keys, no whitespace). `ROWS_EQUAL=true` on BOTH paired attempts.
- **One vintage, one artifact:** `2026-09-09T12:23:34.893879+00:00` on both, manifest `83c6e1335f43`, prefix `projection/2026-09-09T12:23:34.893879+00:00/`. Exactly **1** distinct vintage across the two answers.
- **Inside one minute:** `WINDOW_S=4.229` (attempt 2) and `4.173` (attempt 1), measured on ONE clock. The gateway's execution stamp falls INSIDE the laptop window on AWS's clock, and the gateway's own `date` agrees with AWS's stamp to 4 ms, so the skew is immaterial and is stated rather than assumed.
- **No local DB on either machine:** the worktree reads 0; the gateway reads 0 `kuzu_nessie_db*` AND 0 `*kuzu*` of any name across a walk of 32,220 paths with its control firing; the main workspace reads 0 on MY OWN independent read, not the issuer's self-report.
- WARN: **AND THE ONE THING A GRADER MUST NOT MISS (row W2-S28):** that main-workspace zero is scoped to ONE NAME. An unscoped read of the same directory in the same tick shows **three other local Kuzu stores**, one of which (`kuzu_db`) is by its own manifest a **1,166-node June copy of this graph**. All three are already carded by `3.0.0_SA_CVO` with an explicit *do NOT delete* on two. No criterion here fails on it; whether FWD-7's *no local copy left that either could have read instead* is satisfied with it present is exactly the D8-AC5 reading.

**MECHANICAL RESULT: 4 PASS by output (D8-AC1..D8-AC4), 1 RECORDED-judgment (D8-AC5).**

---

## 1. THE RECORD (the face's fenced JSON block)

```json
{
  "machine_a": "laptop worktree C:/tmp/wk-cldgrph-2-d7 (thin client .tools/comp-kuzu -> https://mcp.opalinvest.dev/graph/cypher, Secrets-Manager bearer; no local database)",
  "machine_b": "gateway i-07dccb1615503ac99 (ip-172-31-89-135.ec2.internal) by SSM AWS-RunShellScript, curl POST http://projection.opal-globgrph.local:8181/cypher inside the VPC",
  "question": "How many nodes of each type does the estate's graph hold, right now, as each machine sees it?",
  "cypher": "MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t",
  "laptop_answer": [
    {
      "t": "C2Motif",
      "c": 6303
    },
    {
      "t": "MS_FILE",
      "c": 5058
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
      "c": 1087
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
      "c": 17
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
      "t": "KMS_KEY",
      "c": 12
    },
    {
      "t": "S3_BUCKET_POLICY",
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
  "gateway_answer": [
    {
      "t": "C2Motif",
      "c": 6303
    },
    {
      "t": "MS_FILE",
      "c": 5058
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
      "c": 1087
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
      "c": 17
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
      "t": "KMS_KEY",
      "c": 12
    },
    {
      "t": "S3_BUCKET_POLICY",
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
  "laptop_vintage": "2026-09-09T12:23:34.893879+00:00",
  "gateway_vintage": "2026-09-09T12:23:34.893879+00:00",
  "rows_equal": true,
  "window_s": 4.229,
  "local_db_laptop": 0,
  "local_db_main_workspace": "MAIN_WORKSPACE_LOCAL_DB_COUNT=0 at 2026-09-09T14:08:02Z (was 6; command `ls infra/aws/globgrph/ | grep -c kuzu_nessie_db`, grep rc=1)",
  "local_db_gateway": 0,
  "second_reader_substitution": "gateway host for site Z -- the issuer's reading, graded D8-AC5",
  "_measured": {
    "attempt_1": {
      "ssm_command_id": "1bf885e5-d4fc-4199-b179-6398e2a4f418",
      "t0_laptop_utc": "2026-09-09T14:20:55.923538500Z",
      "t1_laptop_utc": "2026-09-09T14:21:00.087935700Z",
      "gateway_exec_start_awsclock": "2026-09-09T14:20:57.918Z",
      "rows_equal": "true",
      "window_s": 4.173,
      "laptop_vintage": "2026-09-09T12:23:34.893879+00:00",
      "gateway_vintage": "2026-09-09T12:23:34.893879+00:00",
      "row_counts": [
        58,
        58
      ]
    },
    "attempt_2_is_D8_AC1s_literal_invocation": {
      "ssm_command_id": "6b9a5953-3137-4dcb-b1b2-23f30215530f",
      "t0_laptop_utc": "2026-09-09T14:21:54.854556500Z",
      "t1_laptop_utc": "2026-09-09T14:21:59.076784900Z",
      "gateway_exec_start_awsclock": "2026-09-09T14:21:56.879Z",
      "gateway_own_utc_at_ask": "2026-09-09T14:21:56.883865535Z",
      "rows_equal": "true",
      "window_s": 4.229,
      "row_counts": [
        58,
        58
      ]
    },
    "manifest_sha256_both": "83c6e1335f435691d12f66539623174f6cf32548605d86efe61d2070f0370bbf",
    "artifact_prefix_both": "projection/2026-09-09T12:23:34.893879+00:00/",
    "gateway_absence": {
      "find_denominator": 32220,
      "local_db_count": 0,
      "any_kuzu_count": 0,
      "probe_control": 1,
      "ssm_command_id": "0fc194a1-c8d1-4072-a260-d2dd2d2608c3"
    },
    "main_workspace_independent_read": {
      "command": "ls C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/ | grep -c kuzu_nessie_db",
      "MAIN_WORKSPACE_LOCAL_DB_COUNT": 0,
      "grep_rc": 1,
      "at": "2026-09-09T14:14:15Z",
      "directory_total_entries": 69,
      "positive_control_kuzu_stitch_db": 2,
      "unscoped_residue_see_row_W2_S28": [
        "kuzu_db (9224192 B, manifest: 1166 nodes / 2488 edges, built 2026-06-12 from snapshots/20260612/graph-20260612.tar.gz)",
        "kuzu_ac7.db (4050944 B) + empty kuzu_ac7/",
        "kuzu_stitch_db (9170944 B) -- the placed stitch store",
        ".kuzu_nessie_load.0628067ab4da5610.lock (5 B, '48708') -- a loader lock the name-scoped census cannot match"
      ]
    }
  }
}
```

## 2. WHICH ZERO IS WHICH -- the amendment's requirement, stated so the two cannot stand side by side unlabelled

| zero | what it measures | could it have been non-zero today? |
|---|---|---|
| `D8-AC3` -> **0** (`ls infra/aws/globgrph/ \| grep -c kuzu_nessie_db` in this worktree) | a **WORKTREE** property | **No.** `infra/aws/globgrph/.gitignore:3` ignores `kuzu_nessie_db`, so it is never checked out into any worktree. The issuer measured this same 0 on 2026-09-05 with the laptop copy fully intact. This arm was already true before the retirement began and carries none of FWD-7's weight. |
| `MAIN_WORKSPACE_LOCAL_DB_COUNT` -> **0** (the same command by absolute path against `C:/Users/AndrewBerman/Desktop/ajb_workspace/...`) | the **REAL LAPTOP** property -- the copy a developer could actually have read | **Yes, and it WAS: 6 entries until 2026-09-09T14:08:02Z.** This is the zero that carries FWD-7's claim. |
| `GATEWAY_LOCAL_DB_COUNT` -> **0** (bounded `find` over the second machine) | the **SECOND MACHINE** property | **Yes** -- and the same find returns 1 for `hosts` and walked 32,220 paths, so the zero is an absence, not a dead instrument. |

**AND THE MAIN-WORKSPACE ZERO IS MINE, NOT THE ISSUER'S.** The amendment is explicit about why: the deletion is the issuer's act, and a producer's self-report is not verification of the produced state. My independent read at 2026-09-09T14:14:15Z returned **0** (grep rc=1) over a directory proven to EXIST and to hold **69** entries, with a POSITIVE CONTROL on the same verb and the same listing (`grep -c kuzu_stitch_db` -> **2**). A zero from a missing directory and a zero from a clean one read identically, so the existence check and the control are what make this an absence. It agrees with the issuer's step-log line, which is quoted verbatim in the JSON above as `local_db_main_workspace`.

## 3. THE TWO ASKS

Two machines, **two different transports**, one served artifact -- which is the strength of the arm and not a defect. The laptop goes out over public HTTPS to `mcp.opalinvest.dev/graph/cypher` with a Secrets-Manager bearer; the gateway calls the Cloud Map name `projection.opal-globgrph.local:8181/cypher` in plaintext inside `vpc-0cc0c6a75e54605e3`. Two answers that agree byte-for-byte AND carry the same vintage, manifest SHA and artifact prefix cannot be two copies of a graph; they are one pointer read twice.

**ATTEMPT COUNT, stated plainly (row W2-S29):** the face gives D8-AC1 and D8-AC2 each an invocation that re-fires `two_machines.sh`, and every run of that script IS a fresh paired ask -- while BOUNDS caps the paired ask at *at most two attempts*. This pass ran it **twice**, recorded **both** runs whole below, and derived D8-AC2's count from the same run that produced D8-AC1's rather than spending a third. **Nothing was discarded**: both attempts agreed on the first try, so the face's re-run allowance for a moved pointer was never used.

### 3.1 ATTEMPT 1 (14:20:55Z) -- transcript whole

```
QUESTION=MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t
SSM_COMMAND_ID=1bf885e5-d4fc-4199-b179-6398e2a4f418
T0_LAPTOP_UTC=2026-09-09T14:20:55.923538500Z
T1_LAPTOP_UTC=2026-09-09T14:21:00.087935700Z
LAPTOP_CLIENT_RC=0
SSM_STATUS=Success
GATEWAY_EXEC_START_AWSCLOCK=2026-09-09T14:20:57.918Z
--- laptop stderr (its own VINTAGE line, verbatim) ---
VINTAGE: Built from the estate as of 2026-09-09 12:23:34 UTC.  [vintage=2026-09-09T12:23:34.893879+00:00 manifest=83c6e1335f43 prefix=projection/2026-09-09T12:23:34.893879+00:00/]
--- gateway StandardOutputContent (verbatim, from the second machine) ---
GATEWAY_UTC=2026-09-09T14:20:57.922199030Z
{"rows":[{"t":"C2Motif","c":6303},{"t":"MS_FILE","c":5058},{"t":"Field","c":4969},{"t":"JSXElement","c":2205},{"t":"JSXRender","c":1433},{"t":"PipelineFunction","c":1201},{"t":"MS_FOLDER","c":1087},{"t":"TypeDecl","c":807},{"t":"IAM_POLICY","c":483},{"t":"ReactComponent","c":442},{"t":"Module","c":374},{"t":"Prop","c":359},{"t":"LOG_GROUP","c":250},{"t":"S3Key","c":232},{"t":"IAM_ROLE","c":216},{"t":"LAMBDA","c":203},{"t":"Component","c":199},{"t":"EVENT_RULE","c":142},{"t":"PipelineScript","c":133},{"t":"Endpoint","c":125},{"t":"Hook","c":111},{"t":"DataFetch","c":106},{"t":"EVENT_SOURCE","c":95},{"t":"PanelCluster","c":91},{"t":"SECRET","c":87},{"t":"API_ROUTE","c":86},{"t":"ReactQueryKey","c":57},{"t":"CW_ALARM","c":51},{"t":"ServedURL","c":45},{"t":"DYNAMODB_TABLE","c":37},{"t":"S3_BUCKET","c":34},{"t":"EC2_INSTANCE","c":32},{"t":"SECURITY_GROUP","c":26},{"t":"SERVICE_PRINCIPAL","c":21},{"t":"SSM_DOCUMENT","c":20},{"t":"SQS_QUEUE","c":19},{"t":"INSTANCE_PROFILE","c":18},{"t":"SCHEDULE","c":18},{"t":"MS_USER","c":17},{"t":"SNS_TOPIC","c":16},{"t":"LAMBDA_LAYER","c":15},{"t":"Page","c":15},{"t":"KMS_KEY","c":12},{"t":"S3_BUCKET_POLICY","c":12},{"t":"ECS_TASK_DEFINITION","c":9},{"t":"API_GW","c":5},{"t":"C3System","c":4},{"t":"CODEBUILD_PROJECT","c":4},{"t":"IAM_USER","c":4},{"t":"Pipeline","c":3},{"t":"ROUTE53_RECORD","c":3},{"t":"VPC_ENDPOINT","c":3},{"t":"CLOUDFRONT_DISTRIBUTION","c":2},{"t":"ECS_CLUSTER","c":1},{"t":"LOAD_BALANCER","c":1},{"t":"MS_LIBRARY","c":1},{"t":"MS_SITE","c":1},{"t":"STATE_MACHINE","c":1}],"vintage":"2026-09-09T12:23:34.893879+00:00","age_line":"Built from the estate as of 2026-09-09 12:23:34 UTC.","manifest_sha256":"83c6e1335f435691d12f66539623174f6cf32548605d86efe61d2070f0370bbf","artifact_prefix":"projection/2026-09-09T12:23:34.893879+00:00/"}

--- end ---
LAPTOP_ROW_COUNT=58
GATEWAY_ROW_COUNT=58
LAPTOP_VINTAGE=2026-09-09T12:23:34.893879+00:00
GATEWAY_VINTAGE=2026-09-09T12:23:34.893879+00:00
VINTAGE_IDENTICAL=true
MANIFEST_SHA256_GATEWAY=83c6e1335f435691d12f66539623174f6cf32548605d86efe61d2070f0370bbf
ARTIFACT_PREFIX_GATEWAY=projection/2026-09-09T12:23:34.893879+00:00/
ROWS_EQUAL=true
WINDOW_S=4.173
GATEWAY_EXEC_INSIDE_LAPTOP_WINDOW=true  (AWS clock 2026-09-09T14:20:57.918000+00:00 vs laptop window 2026-09-09T14:20:55.878307+00:00 .. 2026-09-09T14:21:00.050974+00:00)
CLOCK_SKEW_NOTE=the window above is measured on the LAPTOP clock alone (T1-T0), so it does not depend on the two machines agreeing; the AWS-clock line is reported beside it and, if the two clocks disagree, only that line moves.
GATEWAY_OWN_UTC_AT_ASK=2026-09-09T14:20:57.922199030Z
```

### 3.2 ATTEMPT 2 = D8-AC1's literal invocation (14:21:54Z) -- transcript whole

```
QUESTION=MATCH (n:CloudNode) RETURN n.node_type AS t, count(*) AS c ORDER BY c DESC, t
SSM_COMMAND_ID=6b9a5953-3137-4dcb-b1b2-23f30215530f
T0_LAPTOP_UTC=2026-09-09T14:21:54.854556500Z
T1_LAPTOP_UTC=2026-09-09T14:21:59.076784900Z
LAPTOP_CLIENT_RC=0
SSM_STATUS=Success
GATEWAY_EXEC_START_AWSCLOCK=2026-09-09T14:21:56.879Z
--- laptop stderr (its own VINTAGE line, verbatim) ---
VINTAGE: Built from the estate as of 2026-09-09 12:23:34 UTC.  [vintage=2026-09-09T12:23:34.893879+00:00 manifest=83c6e1335f43 prefix=projection/2026-09-09T12:23:34.893879+00:00/]
--- gateway StandardOutputContent (verbatim, from the second machine) ---
GATEWAY_UTC=2026-09-09T14:21:56.883865535Z
{"rows":[{"t":"C2Motif","c":6303},{"t":"MS_FILE","c":5058},{"t":"Field","c":4969},{"t":"JSXElement","c":2205},{"t":"JSXRender","c":1433},{"t":"PipelineFunction","c":1201},{"t":"MS_FOLDER","c":1087},{"t":"TypeDecl","c":807},{"t":"IAM_POLICY","c":483},{"t":"ReactComponent","c":442},{"t":"Module","c":374},{"t":"Prop","c":359},{"t":"LOG_GROUP","c":250},{"t":"S3Key","c":232},{"t":"IAM_ROLE","c":216},{"t":"LAMBDA","c":203},{"t":"Component","c":199},{"t":"EVENT_RULE","c":142},{"t":"PipelineScript","c":133},{"t":"Endpoint","c":125},{"t":"Hook","c":111},{"t":"DataFetch","c":106},{"t":"EVENT_SOURCE","c":95},{"t":"PanelCluster","c":91},{"t":"SECRET","c":87},{"t":"API_ROUTE","c":86},{"t":"ReactQueryKey","c":57},{"t":"CW_ALARM","c":51},{"t":"ServedURL","c":45},{"t":"DYNAMODB_TABLE","c":37},{"t":"S3_BUCKET","c":34},{"t":"EC2_INSTANCE","c":32},{"t":"SECURITY_GROUP","c":26},{"t":"SERVICE_PRINCIPAL","c":21},{"t":"SSM_DOCUMENT","c":20},{"t":"SQS_QUEUE","c":19},{"t":"INSTANCE_PROFILE","c":18},{"t":"SCHEDULE","c":18},{"t":"MS_USER","c":17},{"t":"SNS_TOPIC","c":16},{"t":"LAMBDA_LAYER","c":15},{"t":"Page","c":15},{"t":"KMS_KEY","c":12},{"t":"S3_BUCKET_POLICY","c":12},{"t":"ECS_TASK_DEFINITION","c":9},{"t":"API_GW","c":5},{"t":"C3System","c":4},{"t":"CODEBUILD_PROJECT","c":4},{"t":"IAM_USER","c":4},{"t":"Pipeline","c":3},{"t":"ROUTE53_RECORD","c":3},{"t":"VPC_ENDPOINT","c":3},{"t":"CLOUDFRONT_DISTRIBUTION","c":2},{"t":"ECS_CLUSTER","c":1},{"t":"LOAD_BALANCER","c":1},{"t":"MS_LIBRARY","c":1},{"t":"MS_SITE","c":1},{"t":"STATE_MACHINE","c":1}],"vintage":"2026-09-09T12:23:34.893879+00:00","age_line":"Built from the estate as of 2026-09-09 12:23:34 UTC.","manifest_sha256":"83c6e1335f435691d12f66539623174f6cf32548605d86efe61d2070f0370bbf","artifact_prefix":"projection/2026-09-09T12:23:34.893879+00:00/"}

--- end ---
LAPTOP_ROW_COUNT=58
GATEWAY_ROW_COUNT=58
LAPTOP_VINTAGE=2026-09-09T12:23:34.893879+00:00
GATEWAY_VINTAGE=2026-09-09T12:23:34.893879+00:00
VINTAGE_IDENTICAL=true
MANIFEST_SHA256_GATEWAY=83c6e1335f435691d12f66539623174f6cf32548605d86efe61d2070f0370bbf
ARTIFACT_PREFIX_GATEWAY=projection/2026-09-09T12:23:34.893879+00:00/
ROWS_EQUAL=true
WINDOW_S=4.229
GATEWAY_EXEC_INSIDE_LAPTOP_WINDOW=true  (AWS clock 2026-09-09T14:21:56.879000+00:00 vs laptop window 2026-09-09T14:21:54.816217+00:00 .. 2026-09-09T14:21:59.045337+00:00)
CLOCK_SKEW_NOTE=the window above is measured on the LAPTOP clock alone (T1-T0), so it does not depend on the two machines agreeing; the AWS-clock line is reported beside it and, if the two clocks disagree, only that line moves.
GATEWAY_OWN_UTC_AT_ASK=2026-09-09T14:21:56.883865535Z
```

## 4. THE SECOND MACHINE HOLDS NO GRAPH (D8-AC4) -- transcript whole

```
SSM_COMMAND_ID=0fc194a1-c8d1-4072-a260-d2dd2d2608c3
SSM_INSTANCE=i-07dccb1615503ac99
SSM_STATUS=Success
--- StandardOutputContent (verbatim, from the second machine) ---
GATEWAY_HOST=ip-172-31-89-135.ec2.internal
GATEWAY_UTC=2026-09-09T14:27:31Z
GATEWAY_FIND_DENOMINATOR=32220
GATEWAY_LOCAL_DB_COUNT=0
GATEWAY_ANY_KUZU_COUNT=0
GATEWAY_PROBE_CONTROL=1
--- end ---
GATEWAY_PROBE_CONTROL_VERDICT=FIRED -- the same find verb, same root, same depth, returned
  1 hit(s) for a name that IS present, over a walk of 32220 path(s), so the arm's
  zero is an absence and not a dead instrument
```

`GATEWAY_ANY_KUZU_COUNT=0` is the unscoped reading beside the criterion's scoped one: the second machine holds not just no `kuzu_nessie_db`, but no file or directory matching `*kuzu*` at all to depth 6 on the root filesystem. It is a machine that has never held the graph.

## 5. D8-AC5 -- the reading act (judgment; NO verdict; `3.0.0_SA_CVO` grades this at L9)

**(a) Does the gateway host stand for "two people on two machines"?** What FWD-7 asks is that the same question, asked at the same moment from two places, cannot return two different stories. The gateway host is a genuinely different machine: a different OS, a different network position (inside the VPC), no repository, no checkout, no local graph of any name, and it reaches the service by a different transport with different credentials. What it is NOT is a different PERSON: it is driven by this same worker over SSM, so the human-independence half of *two people* is modelled, not exercised. The issuer stated this substitution at the cut and named the alternative -- the site-Z reader -- which remains available to the CTO's round-N analysis if the substitution is refused. This worker has no bus, no skill and no session on site Z and could not have driven it.

**(b) Is "every developer machine off" met?** On the canonical store, yes, and it is now measured on both sides: the issuer's deletion (step-log row 20, 6 -> 0) and this worker's independent read (0, with an existence check and a positive control). The honest qualification is row **W2-S28**: the same directory still holds `kuzu_db` (9,224,192 B; its manifest declares 1,166 nodes / 2,488 edges built 2026-06-12 from `snapshots/20260612/graph-20260612.tar.gz`), `kuzu_ac7.db` (4,050,944 B), the placed `kuzu_stitch_db`, and a stale `.kuzu_nessie_load.0628067ab4da5610.lock` whose NAME the certifying census cannot match. Two of those carry a standing `3.0.0_SA_CVO` *do NOT delete* (DIAL_RECORD_comp-kuzu_20260804.md:19, 'deletions ruled-not-taken'). So the question in front of the grader is not whether something was missed -- it is whether *no local copy left that either could have read instead* means the CANONICAL copy or ANY local copy of this graph. A 1,166-node June copy is a copy someone could read instead of the served 27,304, which is the stale-answer failure R7 exists to end; and a standing preservation ruling is a reason it is still there. **Both facts are true and this worker does not grade them.**

**GRAIN, stated:** the node/edge figures for `kuzu_db` come from its own build manifest, read as a plain file. This worker did NOT open the store -- the order's BOUNDS forbid running an engine, and `kuzu.Database` CREATES an absent store on open (`3.0.0_SA_CVO`, ADJUDICATION_v1 C-S20). The claim is *the manifest beside it says 1,166 nodes*, never *this worker read 1,166 nodes out of it*.

**(c) What this closes.** CG-x-7's closing condition is *identical answers with identical vintage lines; no local DB on either machine (proven); this closes CG-s-8*. The first two are measured above. The third is the issuer's and the CVO's to record.

## 6. ROWS FILED THIS ORDER

The channel header claimed **118 rows**; VERIFIED by parsing every fenced json block and summing their lengths -- 118 rows in 115 blocks, 118 unique ids, `W2-S1..W2-S27` contiguous. After this append: **120 rows in 116 blocks, 120 unique ids**, restated in the header.

| id | class | hazard | one line |
|---|---|---|---|
| `NFRA_CLDGRPH-W2-S28` | OBSERVATION | INERT | the main-workspace zero is TRUE and name-scoped; an unscoped read of the same directory shows three other local Kuzu stores, one a 1,166-node June copy of this graph, all already carded by `3.0.0_SA_CVO` with a do-NOT-delete on two -- a D8-AC5 reading input |
| `NFRA_CLDGRPH-W2-S29` | OBSERVATION | INERT | D8-AC1 and D8-AC2 each re-fire the paired ask while BOUNDS caps it at two attempts; both runs recorded whole, nothing discarded, D8-AC2 derived from attempt 2's own stdout |

## 7. WHAT REMAINS, NAMED

1. **The D8-AC5 reading** on the substitution and on `kuzu_db` -- `3.0.0_SA_CVO` at L9.
2. **`kuzu_stitch_db`** -- the second reachability surface, the issuer's placed manifest row at L10; a READER (`comp_debt.py:215`) and, since TO-CG-D-7 pass 4, no writer.
3. **The D7-AC8 documentation residue** (`tool_index.py`, `comp_aws_cli.py:2857/2866`, `debtscan/comp_similar.py:591`, `graph-call-manifest.yaml`) travels to L9 named, unchanged.
4. **The site-Z reader** stays available if the gateway substitution is refused.
