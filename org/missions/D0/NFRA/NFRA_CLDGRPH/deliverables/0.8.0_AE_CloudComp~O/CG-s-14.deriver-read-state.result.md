# CG-s-14 — honest S3 notification read state and declared trigger edges

The canonical graph engine now keeps a failed S3 notification read as data: the bucket is `UNREADABLE`, its notification counts are unknown rather than zero, and every full build prints the read/unreadable denominator and unreadable bucket names. The same engine merges live notification targets with Terraform-declared `aws_s3_bucket_notification` targets and records `live`, `declared`, or `both` provenance plus an explicit disagreement state on each `TRIGGERS` edge.

Implementation is LOCAL at `b5bc1c8b27e89a477e17a5d9b789fdc010173af5`. The real-account exercise was read-only: no bucket configuration, Terraform, graph marker, resource, image, or deployment was written. The live runtime still requires a separately routed rebuild of the shared globgrph image; that fact is recorded as `NFRA_CLDGRPH-S28` at `6e5af8cdc7610e7a6efbba98a4e4d919607988ec`.

```json
{
  "task_order": "NFRA_CLDGRPH.TO-CG-C-3",
  "cell": "CG-s-14",
  "implementation_commit": "b5bc1c8b27e89a477e17a5d9b789fdc010173af5",
  "pre_change_commit": "57500ca0fb5332aee91cefa9889e4f539402c940",
  "swallowed_read_census": {
    "instrument": "python .tools/comp-read org/modules/graph/comp_aws_cli.py --enumerate 'except:\\s*$|except Exception|pass$'; revision comparison counted executable statements at the pinned commits",
    "whole_file": {
      "bare_except_before": 0,
      "bare_except_after": 0,
      "except_exception_handlers_before": 81,
      "except_exception_handlers_after": 79,
      "pass_statements_before": 25,
      "pass_statements_after": 24
    },
    "notification_reads_that_swallowed_failure_before": {
      "count": 3,
      "sites": [
        "org/modules/graph/comp_aws_cli.py:273-281 @ 57500ca0fb5332aee91cefa9889e4f539402c940 — node-property read caught Exception and assigned three genuine-zero values",
        "org/modules/graph/comp_aws_cli.py:1442-1447 @ 57500ca0fb5332aee91cefa9889e4f539402c940 — Lambda TRIGGERS read caught Exception and passed",
        "org/modules/graph/comp_aws_cli.py:1679-1683 @ 57500ca0fb5332aee91cefa9889e4f539402c940 — SNS/SQS sibling read caught Exception and continued"
      ]
    },
    "notification_reads_that_swallow_failure_after": {
      "count": 0,
      "sites": [
        "org/modules/graph/comp_aws_cli.py:202-222 @ b5bc1c8b27e89a477e17a5d9b789fdc010173af5 — one cached helper returns READ/configuration or UNREADABLE/error",
        "org/modules/graph/comp_aws_cli.py:418-419 @ b5bc1c8b27e89a477e17a5d9b789fdc010173af5 — node twin records notification_read_state and notification_read_error",
        "org/modules/graph/comp_aws_cli.py:1587-1591 @ b5bc1c8b27e89a477e17a5d9b789fdc010173af5 — canonical derive_edges extends the merged live/declared result"
      ]
    }
  },
  "build_denominator": {
    "real_build_line": "s3 notifications buckets read=34 / buckets unreadable=0; unreadable=none",
    "build_result": "exit 0; edges total=3934; TRIGGERS=188; NOT PERSISTED",
    "implementation": "org/modules/graph/comp_aws_cli.py:225-239,2808 @ b5bc1c8b27e89a477e17a5d9b789fdc010173af5"
  },
  "live_declared_edges": [
    {
      "source": "arn:aws:s3:::opal-data-bd",
      "target": "arn:aws:lambda:us-east-1:313476888478:function:bd-allocation-processor",
      "edge_type": "TRIGGERS",
      "provenance": "both",
      "live_read_state": "READ",
      "source_disagreement": "NONE",
      "declared_provenance": "bd-pipeline/aws_s3_bucket_notification.bd_data_bucket"
    },
    {
      "source": "arn:aws:s3:::opal-data-bd",
      "target": "arn:aws:lambda:us-east-1:313476888478:function:bd-gold-trigger",
      "edge_type": "TRIGGERS",
      "provenance": "both",
      "live_read_state": "READ",
      "source_disagreement": "NONE",
      "declared_provenance": "bd-pipeline/aws_s3_bucket_notification.bd_data_bucket"
    },
    {
      "source": "arn:aws:s3:::opal-data-bd",
      "target": "arn:aws:lambda:us-east-1:313476888478:function:bd-silver-merge",
      "edge_type": "TRIGGERS",
      "provenance": "both",
      "live_read_state": "READ",
      "source_disagreement": "NONE",
      "declared_provenance": "bd-pipeline/aws_s3_bucket_notification.bd_data_bucket"
    }
  ],
  "planted_denial": {
    "test": "org/modules/graph/tests/test_comp_aws_s3_notification_state.py:65-105 @ b5bc1c8b27e89a477e17a5d9b789fdc010173af5",
    "aws_write_count": 0,
    "before": {
      "legacy_result": 0,
      "meaning": "the caught PermissionError manufactured an empty/genuine-zero value"
    },
    "after": {
      "state": "UNREADABLE",
      "configuration": null,
      "buckets_read": 1,
      "buckets_unreadable": 1,
      "unreadable_buckets": [
        "denied"
      ],
      "meaning": "the denominator moves by one and no zero edge/count is fabricated"
    }
  },
  "source_merge_control": {
    "test": "org/modules/graph/tests/test_comp_aws_s3_notification_state.py:109-135 @ b5bc1c8b27e89a477e17a5d9b789fdc010173af5",
    "declared_edge_survives_denied_live_read": true,
    "provenance": "declared",
    "live_read_state": "UNREADABLE",
    "source_disagreement": "UNKNOWN_LIVE_UNREADABLE"
  },
  "validation": {
    "tests": "27 passed in 1.47s",
    "commit_gate": "clean for 2 of 2 touched Python files",
    "push_state": "LOCAL",
    "origin_cloud": "351f309e0a6ded1a5a5bdf3aacec18a5f9f8dbee",
    "implementation_is_ancestor_of_origin_rc": 1,
    "push_performed": false
  }
}
```

The pre-fix live graph observation remains the before-control: S20 at `72c0022be817096f95248f927778bd687e924b7b` measured zero S3-to-Lambda `TRIGGERS` rows and zero outgoing edges for `opal-data-bd`. The repaired read-only build derives the three quoted bd targets (and eleven additional S3-to-Lambda targets) without persisting output.

Read-dependency release from CG-s-2: `0.7.0_AE_CloudOps~S` reports CG-s-2 COMPLETE at `1c0d13904e7cbb5d563293de6f6beb13c027f382` with proof VALID. Its authentic revision-3 worker task advanced the existing marker-to-projection path to vintage `2026-09-03T19:02:18.412096+00:00` after direct-count and exact hash/size verification, and C1 served that vintage with HTTP 200 and `nodes=27225`. The sender's follow-up ACK expressly confirms these are read-dependency/existing-path evidence only, C2 makes no CG-s-14 claim, and C3 retains exclusive ownership of the deriver-read-state surface. C-3 does not deploy its new engine image.

HANDOFF NFRA_COMPEFFICACY `comp-trigger`: consume `TRIGGERS` edge provenance and `live_read_state`; treat `UNKNOWN_LIVE_UNREADABLE` as declared evidence with an unreadable live plane, never as fixture-covered zero or a silently reconciled match.
