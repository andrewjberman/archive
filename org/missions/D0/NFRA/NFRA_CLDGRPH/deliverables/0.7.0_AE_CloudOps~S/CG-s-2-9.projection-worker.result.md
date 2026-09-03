# CG-s-2 + CG-s-9 - projection worker port result

**Task:** `NFRA_CLDGRPH.TO-CG-B-2` | **Seat:** `0.7.0_AE_CloudOps~S` | **State:** COMPLETE under issuer Msg 93848

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-B-2",
  "cells": ["CG-s-2", "CG-s-9"],
  "state": "COMPLETE_ISSUER_ADJUDICATED",
  "runtime_decision": {
    "runtime": "one ECS Fargate RunTask path for incremental and full fallback",
    "trigger": "EventBridge Pipe consuming the projection SQS queue; exact SQS-body source filter launches ECS only for a real marker Records envelope",
    "consumer_of_record": "EventBridge Pipe",
    "retry": "marker idempotency plus the nightly 02:00Z derive guarantee; not SQS redrive after RunTask acceptance",
    "ceiling_rule": "the full fallback never runs under a 900 s ceiling",
    "task_cpu": 2048,
    "task_memory_mib": 16384,
    "engine_deadline_seconds": 3600,
    "queue_visibility_seconds": 30,
    "visibility_basis": "Pipe RunTask API hold measured at 0.734-0.766 s on 2 of 2 early real messages; ECS does not hold the SQS message",
    "laptop_full_seconds": [1001.172, 935.5],
    "laptop_fallback_range_seconds": [940.594, 1006.266],
    "laptop_peak_mib": 6752.0,
    "cloud_full_peak_mib": 5795.848,
    "cloud_fallback_peak_mib": 5789.156,
    "ce_g_5": "local-only; cloud equivalent is artifact-first, manifest-last, pointer-last in the shared CG-s-3 writer"
  },
  "deployment": {
    "engine_fix_commit": "117e539280d678e946f5c74a1f2593e07d41e01a",
    "deployed_writer_source_commit": "5bb91c894d591ce51987e6fa98f27a4b0f936e22",
    "conditional_create_commit": "59aeb265cca69506ec8c02f76d11a2b615dbe195",
    "compaction_commit_not_deployed": "052a58999a8ba83db4d02279ad0d6765a1e4998a",
    "task_definition_arn": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:2",
    "pipe_arn": "arn:aws:pipes:us-east-1:313476888478:pipe/opal-globgrph-projection-worker",
    "worker_role_arn": "arn:aws:iam::313476888478:role/opal-globgrph-projection-worker",
    "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner:latest",
    "image_digest": "sha256:1e1aaa14df31da756001f3a42b1f5b6c671e4d75586aeb72c96586534a50f01c",
    "image_build": "globgrph-derive-build:330c2689-3d7b-4551-a29e-7c3ff76320f0",
    "initial_apply": "10 add, 0 change, 0 destroy",
    "filter_repair_apply": "0 add, 1 change, 0 destroy",
    "target_replan": "no changes, detailed exit 0",
    "unscoped_replan_addresses": [
      "aws_glue_partition.tool_activity[\"rolling_log\"]",
      "aws_glue_partition.tool_activity[\"rolling_log_summary\"]",
      "aws_glue_partition.tool_activity[\"routing\"]",
      "aws_sns_topic_subscription.critical_surface_alerts_email"
    ],
    "own_addresses_in_unscoped_replan": 0,
    "ledger_close_commit": "668a2a269404d9dd08c6a5789ff1a11f8f27fef2"
  },
  "fixes": {
    "S9": "one graph_key rule for node ids and edge endpoints; pre-port mutant false, port true",
    "S2": "GLOBGRPH_KUZU_INCREMENTAL_REFRESH semantics stated once and consistently: default 1 runs incremental",
    "S3": "singleton is keyed per target database path; different targets do not serialize",
    "S8": "both engines stamp stored COUNT(*) as edge_count; full loader guards untyped nodes and TSGRAPH fold and records the absence of an incremental-style source-vs-landed comparison"
  },
  "controls": {
    "focused_tests": "initial cross-engine suite 6 passed; current worker/compaction suite 9 passed",
    "test_event_after_filter": {
      "attempts": 2,
      "main_queue_after": 0,
      "new_ecs_tasks": 0,
      "dlq_baseline": 3,
      "dlq_after": 3,
      "projection_objects_after": 0
    },
    "local_compaction": {
      "marker_committed_at": "2026-09-03T17:32:43.452059+00:00",
      "engine_node_upsert": 2,
      "engine_nodes": 27226,
      "engine_edges": 58606,
      "checkpointed_bytes": 83615744,
      "compacted_bytes": 34824192,
      "reclaimed_bytes": 48791552,
      "manifest_bytes": 1639,
      "publish_set_bytes": 34825831,
      "contract_band": [42294879, 51693741],
      "within_band": false,
      "outcome": "PublicationRefused locally before any S3 call"
    }
  },
  "cloud_runs": {
    "interrupted_attempt": {
      "marker_committed_at": "2026-09-03T16:21:26.406073+00:00",
      "projection_task": "6aa88972790949a5bbe9b315381ec895",
      "cold_start_seconds": 18.942,
      "engine_runtime_before_stop_seconds": 288.286,
      "stop_code": "UserInitiated",
      "stop_reason": "CG-s-3 prevent pre-contract image collision at released vintage",
      "exit_code": 137,
      "artifact_count": 0,
      "surprise": "NFRA_CLDGRPH-S21 @ ee51681c458e313092d45621d3001bb160b4602c"
    },
    "full_cold": {
      "state": "ACCEPTED_PUBLISHED",
      "marker_committed_at": "2026-09-03T16:27:39.471730+00:00",
      "marker_writer_id": "incremental_updater",
      "projection_task": "fa5df7737afc48fdbda6a9106d5676b6",
      "cold_start_seconds": 21.139,
      "engine_seconds": 833.25,
      "worker_seconds": 834.825,
      "peak_rss_mib": 5795.848,
      "node_count": 27206,
      "edge_count": 58550,
      "edges_skipped_missing_endpoint": 383,
      "artifact_key": "projection/2026-09-03T16:27:39.471730+00:00/kuzu_nessie_db",
      "artifact_bytes": 48046080,
      "artifact_sha256": "5a449cb4384c5933491d431546136b0053f3d0cc37e6c681d361611a7ba0a12a",
      "manifest_bytes": 1632,
      "manifest_sha256": "0c2c0052c43ca06ce92bb37fe822a733c4999a0405e2a8b456b015f14d40f101",
      "direct_count_agreement": true
    },
    "forced_fallback": {
      "state": "ACCEPTED_PUBLISHED",
      "authorized_producer_task": "126daf3f1e9f423ab5456f5ccacbf00f",
      "marker_committed_at": "2026-09-03T17:01:08.128628+00:00",
      "marker_writer_id": "derive_runner",
      "projection_task": "0a53e160f6b0420ba7056e4bd1a098cf",
      "delta_gate": "27225 of 27225 nodes, 100%, forced full fallback",
      "incremental_gate_seconds": 3.001,
      "full_seconds": 801.226,
      "worker_seconds": 806.373,
      "peak_rss_mib": 5789.156,
      "node_count": 27225,
      "edge_count": 58606,
      "edges_skipped_missing_endpoint": 383,
      "artifact_key": "projection/2026-09-03T17:01:08.128628+00:00/kuzu_nessie_db",
      "artifact_bytes": 47964160,
      "artifact_sha256": "68fa26ec8581c37ed66446c6ab5117647235a0b06892d9e555312a1725829e91",
      "manifest_bytes": 1626,
      "manifest_sha256": "28ed81e28144fa3db6dc880adf55ff1076c1b376d36b4b8b1d8597d1cc4a8f1c",
      "direct_count_agreement": true
    },
    "incremental_authentic_1": {
      "state": "ENGINE_ACCEPTED_PUBLICATION_REFUSED",
      "qa_trigger": "one byte-identical re-PUT of the bucket's existing six-tag array",
      "cloudtrail_event_id": "2ef5326a-ad76-4071-8307-d9b8ff5c8bcc",
      "updater_request_id": "70d9ca80-4548-51f8-865c-a993ebf9cd25",
      "marker_committed_at": "2026-09-03T17:23:22.339410+00:00",
      "pipe_execution_id": "09f97531-1a2c-4b5f-91ce-8ead27b74dbc",
      "projection_task": "32d8608dbe8f42f482a5e4114b3e0ace",
      "cold_start_seconds": 18.853,
      "task_started_to_stopped_seconds": 28.682,
      "node_upsert": 1,
      "node_delete": 0,
      "edge_upsert": 0,
      "edge_delete": 0,
      "node_count": 27225,
      "edge_count": 58606,
      "edges_skipped_missing_endpoint": 383,
      "publish_set_bytes": 83617383,
      "outcome": "PublicationRefused above band; zero prefix objects; pointer unchanged"
    },
    "incremental_authentic_2": {
      "state": "ENGINE_ACCEPTED_PUBLICATION_REFUSED",
      "trigger": "natural incremental_updater stamp",
      "marker_committed_at": "2026-09-03T17:32:43.452059+00:00",
      "projection_task": "03a14222ff914416af24193a4f9f61e7",
      "cold_start_seconds": 19.238,
      "task_started_to_stopped_seconds": 28.788,
      "node_upsert": 2,
      "node_delete": 0,
      "edge_upsert": 0,
      "edge_delete": 0,
      "node_count": 27226,
      "edge_count": 58606,
      "edges_skipped_missing_endpoint": 383,
      "publish_set_bytes": 83617383,
      "outcome": "PublicationRefused above band; zero prefix objects; pointer unchanged"
    }
  },
  "pointer_and_handoff": {
    "prefix_grammar": "s3://opal-313476888478-globgrph/projection/<marker committed_at_iso>/",
    "artifact_name": "kuzu_nessie_db",
    "manifest_name": "_build_manifest.json",
    "manifest_fields": ["schema_version", "vintage", "committed_at", "age_line", "built_at", "nessie_commit_hash", "nodes_snapshot_id", "edges_snapshot_id", "writer_id", "producer", "node_count", "edge_count", "edges_skipped_missing_endpoint", "artifact"],
    "vintage_key": "marker committed_at_iso",
    "current_pointer_vintage": "2026-09-03T17:01:08.128628+00:00",
    "current_pointer_manifest_sha256": "28ed81e28144fa3db6dc880adf55ff1076c1b376d36b4b8b1d8597d1cc4a8f1c",
    "pointer_bound_crossing": "NFRA_CLDGRPH-S23 @ 952fae0cc41c6e3f517c4b9fae5113340b159893; issuer ordered no undo",
    "deliberate_absences": ["deletion", "serving"]
  },
  "local_canonical_db_control": {
    "post_preflight_baseline_bytes": 518856704,
    "post_preflight_baseline_mtime_utc": "2026-09-03T13:52:09.3355738Z",
    "post_preflight_listing_md5": "3792f7f8186c238bdacc855c2d73938c",
    "later_state": "externally changed by observed comp-blast rebuild activity, not by the cloud worker or its temp-path runs",
    "carrier": "NFRA_CLDGRPH-S12 @ d60817d742"
  },
  "push_control": {
    "one_pre_ruling_push_disclosed": true,
    "push_after_issuer_msg_93712": false,
    "final_push_state": "measured read-only after the face co-commit; this seat does not push"
  }
}
```

## Decision and deployed shape

The runtime decision is inherited from the exact pre-build record at `18503387b5` and its Pipe-consumer restatement at `799e2dad0a`, against the fit table at `a9aea6f3ce`. A single Fargate task owns both engine paths because every measured laptop full/fallback run exceeded Lambda's 900-second ceiling. The deployed task's 16 GiB memory is 2.43 times the 6,752 MiB laptop peak; accepted cloud peaks were below 5.8 GiB.

The applied revision is `globgrph-projection-worker:2`, using image digest `sha256:1e1aaa14...` built from source commit `5bb91c894d`. The current shared writer includes CG-s-3's verified pointer-last and conditional same-vintage publication. B2's original no-pointer bound was crossed; S23 at `952fae0cc4` records the exact pointer and Msg 93807 forbids an undo.

## Apply, IAM, and ledger

The initial saved target apply was 10 add / 0 change / 0 destroy; the source-filter repair was 0 add / 1 change / 0 destroy. The target replan returned no changes. The one unscoped replan listed only the three ruled Glue partitions and the email subscription, with zero owned addresses. The refreshed IAM census counted 220 roles; the worker's two inline policies contain the four desired statements and no attached policy, and the worker added no gap row. The deployment ledger is CLOSED at `668a2a2694`.

## Cloud exercise

The accepted full-cold and forced-fallback artifacts were independently downloaded, hashed, and queried. Their direct Kuzu counts exactly match their manifests. The full-cold worker completed in 834.825 seconds versus the 935.5-1001.2-second laptop range; the forced fallback completed in 806.373 seconds after a 3.001-second 100% delta gate, below its 940.594-1006.266-second laptop range. Neither approached the 3,600-second engine deadline.

The authentic incremental engine passed twice: one node at 17:23:22 and two nodes at 17:32:43. Both resulting 83,617,383-byte publish sets were refused by the full-load-derived band before any artifact, manifest, or pointer write. Issuer Msg 93834 rules the engine arm PASS and the refusal the required can-fail completeness control firing. The local checkpoint/export/import disarm at `052a58999a` preserved the graph and reclaimed the file to 34,824,192 bytes, but the 34,825,831-byte publish set then fell below the same band. Final Msg 93848 therefore selects option (d): no revision 3, no cloud retry, no marker override, and round-3 deployment only with the fixed publisher.

## Handoff and open downstream route

CG-s-3 receives the exact prefix grammar and manifest fields above. The live pointer remains on the accepted 17:01 fallback artifact; both failed incremental prefixes are empty. S24 at `5acb5d7d7a` routes the byte-band defect to round 3, where integrity is counts, hashes, and declared sizes, with no byte band or a mode-specific one. This task deletes nothing, serves nothing, writes no marker, and performs no post-ruling push.
