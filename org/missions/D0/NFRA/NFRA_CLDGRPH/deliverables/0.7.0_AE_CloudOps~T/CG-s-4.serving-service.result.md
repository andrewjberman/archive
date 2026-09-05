# CG-s-4 -- current projection serving service

```json
{
  "service_name": "globgrph-serving",
  "in_vpc_address": "http://projection.opal-globgrph.local:8181",
  "port": 8181,
  "auth_kind": "NONE",
  "watch_interval_seconds": 60,
  "task": {
    "task_definition": "globgrph-serving:1",
    "task_arn_before_swap": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/c18ee8b40e4a4bf3993f8f78cc2f98a6",
    "task_arn_after_swap": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/c18ee8b40e4a4bf3993f8f78cc2f98a6",
    "started_at_before_swap_epoch": 1788460967.358,
    "started_at_after_swap_epoch": 1788460967.358,
    "cpu_units": 512,
    "vcpu": 0.5,
    "memory_mib": 1024,
    "image_digest": "sha256:68c822ff9cc4784f6fa8eb83fcde513f6ef1a1659f0220f44a2b78c9fcbd12b5"
  },
  "read_only_open_measurement": {
    "vintage": "2026-09-03T17:01:08.128628+00:00",
    "artifact_bytes": 47964160,
    "baseline_rss_bytes": 52957184,
    "after_download_rss_bytes": 72552448,
    "after_read_only_open_rss_bytes": 138268672,
    "after_query_rss_bytes": 143536128,
    "peak_rss_bytes": 143536128,
    "measurement_query": "MATCH (n) RETURN count(n) AS nodes",
    "measurement_answer": 27225
  },
  "query_exercise": {
    "caller": "gateway i-07dccb1615503ac99 / ip-172-31-89-135.ec2.internal",
    "query": "MATCH (n) RETURN count(n) AS nodes",
    "before": {
      "ssm_command_id": "2e708112-9eec-44ef-9e65-4eeded137343",
      "at": "2026-09-03T18:46:14.328859983Z",
      "rows": [{"nodes": 27225}],
      "vintage": "2026-09-03T17:01:08.128628+00:00",
      "age_line": "Built from the estate as of 2026-09-03 17:01:08 UTC.",
      "manifest_sha256": "28ed81e28144fa3db6dc880adf55ff1076c1b376d36b4b8b1d8597d1cc4a8f1c",
      "artifact_prefix": "projection/2026-09-03T17:01:08.128628+00:00/",
      "http_code": 200,
      "rtt_seconds": 0.026205
    },
    "after": {
      "ssm_command_id": "62213ecc-b319-4d23-b91b-37e765b0f2fc",
      "at": "2026-09-03T19:03:54.159027527Z",
      "rows": [{"nodes": 27225}],
      "vintage": "2026-09-03T19:02:18.412096+00:00",
      "age_line": "Built from the estate as of 2026-09-03 19:02:18 UTC.",
      "manifest_sha256": "751b870534c474298e0e968390f143e325b4741a4a4fc471c3bf341cd39c0b58",
      "artifact_prefix": "projection/2026-09-03T19:02:18.412096+00:00/",
      "http_code": 200,
      "rtt_seconds": 0.003664,
      "health_http_code": 200,
      "health_rtt_seconds": 0.002624
    }
  },
  "swap": {
    "pointer_before": "2026-09-03T17:01:08.128628+00:00",
    "pointer_after": "2026-09-03T19:02:18.412096+00:00",
    "service_last_swap_before": "2026-09-03T18:42:39.874114+00:00",
    "service_last_swap_after": "2026-09-03T19:03:42.191303+00:00",
    "pointer_read_at_after": "2026-09-03T19:03:42.178959+00:00",
    "restart_observed": false
  },
  "backward_refusal": {
    "test_seam": "PointerWatcher.consider_pointer with a planted local body; no S3 write",
    "quoted": "backward pointer refused: candidate=2026-09-03T17:01:08.000000+00:00 current=2026-09-03T18:01:08.000000+00:00",
    "loader_calls": 0,
    "served_vintage_after": "2026-09-03T18:01:08.000000+00:00"
  },
  "terraform": {
    "version": "1.9.8",
    "targeted_plan": "7 to add, 0 to change, 0 to destroy",
    "safe_apply": "Apply complete! Resources: 7 added, 0 changed, 0 destroyed.",
    "unscoped_replan": {
      "actions": [
        "aws_glue_partition.tool_activity[\"rolling_log\"] update",
        "aws_glue_partition.tool_activity[\"rolling_log_summary\"] update",
        "aws_glue_partition.tool_activity[\"routing\"] create",
        "aws_sns_topic_subscription.critical_surface_alerts_email create"
      ],
      "assert_exact_four": "PASS",
      "assert_no_c1": "PASS"
    },
    "security_group": "sg-0e85dd853fbe5584e: tcp/8181 from 172.31.0.0/16 only",
    "iam": "one inline GlobgrphServingReadOnly policy, zero attached policies; S3 GetObject/ListBucket/GetBucketLocation on the bucket and projection/* plus log writes on /ecs/globgrph-serving:*; no PutObject, DeleteObject, or DynamoDB"
  },
  "cost_line": {
    "basis": "us-east-1 Linux Fargate: $0.04048 per vCPU-hour + $0.004445 per GB-hour",
    "arithmetic": "(0.5 * 0.04048 + 1 * 0.004445) * 24",
    "usd_per_24_hours": 0.59244,
    "usd_per_30_days": 17.7732
  }
}
```

## The reader and service

The deployed reader is the contract reader at
`infra/aws/globgrph/projection_server.py:97-237 @8f0dff109f`.  It accepts only
canonical `projection/current.json`; derives the manifest and artifact keys
from that pointer; requires pointer prefix, manifest key, vintage, manifest
SHA-256, artifact byte count and downloaded SHA-256 agreement; and repeats
from P2 whenever P1 and P2 differ.  The manifest's publication byte band is
explicitly ignored at `:193-195`: S24 made it telemetry, not integrity.

Kuzu is opened with `read_only=True` at `:242-245`.  The generation swap and
lease are at `:294-353`: publication of the new generation under one lock makes
the next query see it, while an already-leased old generation is retained
until its query exits.  The 60-second watcher refuses/logs backward and
equal-vintage-different pointers at `:382-410`.  `POST /cypher` and
`GET /health` are at `:477-500`; every successful query response carries
`rows`, `vintage`, `age_line`, `manifest_sha256`, and `artifact_prefix`.

Seven focused controls pass at
`infra/aws/globgrph/tests/test_projection_server.py:90-188 @8f0dff109f`:
manifest/artifact verification without the byte band, P1/P2 straddle repeat,
corrupt byte-count refusal, an old-query/new-query atomic swap, backward
refusal before loader invocation, and the single-statement request grammar.
The backward arm was rerun after the real forward advance.  Its planted body
never touched S3 (`LOADER_CALLS=0`) and the served vintage stayed
`2026-09-03T18:01:08.000000+00:00`.

## Resources and measured size

`infra/aws/terraform/globgrph/serving.tf @8f0dff109f` mirrors the existing
Nessie Cloud Map pattern: `projection.opal-globgrph.local` remains stable while
ECS replaces task IPs.  The task definition is 0.5 vCPU / 1 GiB, selected from
the JSON measurement above.  Its 143,536,128-byte peak includes service
imports, the download, a real read-only Kuzu open and a count query.  One GiB
is more than seven times that peak and also accommodates the short overlap of
two generations during a swap.  The measured 24-hour compute line is
`(0.5 * $0.04048 + 1 * $0.004445) * 24 = $0.59244` (about `$17.7732` per
30-day month), before incidental logs/data transfer.

The NEVER-2 ledger `cldgrph-cgs4-serving-plane` opened before the first plan
and closed only after all five activation and exercise legs carried proof.
The targeted plan and saved-plan safe-apply both named only the seven C1
resources.  The one explicit unscoped re-plan's saved JSON was asserted in
both directions: exactly the four listed foreign changes and no C1 resource.
The four were not applied.  The refreshed 18:43:46Z applied IAM census and a
direct role read show exactly the V-2(ii) statements, one inline policy, and
zero attached policies.  The live SG has one ingress rule: TCP 8181 from
`172.31.0.0/16`.

## Live exercise

SSM command `2e708112-9eec-44ef-9e65-4eeded137343` ran from the gateway EC2
host, not the service, and resolved the Cloud Map name to `172.31.9.108`.  Its
query returned HTTP 200, 27,225 nodes, the exact then-current pointer vintage,
the age line and both integrity identifiers in 0.026205 seconds.  Health
returned HTTP 200 in 0.002202 seconds.

C2's authentic revision-3 writer task `f8b288ad95ec42dab2d17ef5a33cbd29`
published the strictly-later `2026-09-03T19:02:18.412096+00:00` pointer only
after verifying 27,225 nodes and 58,606 edges.  Without replacing or restarting
the C1 task, its watcher recorded `last_swap=2026-09-03T19:03:42.191303+00:00`.
Gateway SSM command `62213ecc-b319-4d23-b91b-37e765b0f2fc` then issued the same
count query and received HTTP 200, 27,225, the new vintage, age line, manifest
SHA and prefix in 0.003664 seconds; health returned HTTP 200 in 0.002624
seconds.  The task ARN and `startedAt` remained exactly unchanged, so the
advance was a live in-process swap.  This seat did not write the marker or
pointer and did not touch C2/B2 runtime resources.

## Downstream handoffs

**CG-s-5 handoff:** call `http://projection.opal-globgrph.local:8181` inside
`vpc-0cc0c6a75e54605e3`, `AuthKind.NONE`.  Send one UTF-8 Cypher statement as
the `POST /cypher` body with `Content-Type: text/plain` (JSON
`{"statement":"..."}` is also accepted).  A successful JSON response is
`{"rows":[...],"vintage":"...","age_line":"...","manifest_sha256":"...","artifact_prefix":"..."}`.
The gateway remains a thin HTTP proxy and needs no globgrph IAM grant.

**CG-s-6 handoff:** render the answer's `age_line` as the plain-words age
disclosure.  Preserve `vintage`, `manifest_sha256`, and `artifact_prefix` as
the machine fields underneath it; do not infer age from client time and do not
read S3 or name a vintage directly.
