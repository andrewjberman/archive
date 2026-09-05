# CG-s-15 -- the shared image rebuilt, THIS PROJECT'S THREE families pinned by digest, and the whole chain exercised in the cloud

**TO:** `NFRA_CLDGRPH.TO-CG-D-1` (REOPENED pass) · **Cell:** `CG-s-15` (decomposition v0.3) · **Seat:** `0.9.0_WK_NFRA_CLDGRPH~1`
**Branch:** `wk-NFRA_CLDGRPH-1` · **Push state: LOCAL** · **Written:** 2026-09-04 ~17:1xZ

> THIS PASS closed what the FIRST pass could not: the terraform apply (leg L4), the projection
> family's launch on the pinned digest (L6), the serving family's rollout (L7), and a SECOND
> ad-hoc derive -- this one on the PINNED revision `globgrph-derive-runner:7` and AFTER the
> `s3:GetBucketNotification` grant of TO-CG-D-12 -- whose own log reads
> `buckets read=34 / buckets unreadable=0` against the first pass's `read=0 / unreadable=34`.
> The live served graph answers **TRIGGERS = 171**. Rows `S20` and `S28` have their cloud proof.

```json
{
  "record_kind": "CG-s-15 shared-image rebuild + digest pins + live cloud exercise",
  "claim": "measured",
  "seat": "0.9.0_WK_NFRA_CLDGRPH~1",
  "branch": "wk-NFRA_CLDGRPH-1",
  "push_state": "LOCAL (no push attempted; this seat never pushes)",
  "region": "us-east-1",
  "account": "313476888478",

  "image": {
    "repository": "opal-globgrph-derive-runner",
    "build_id": "globgrph-derive-build:442305e5-9d54-4e89-96de-b22a6ed9f776",
    "build_status": "SUCCEEDED (codebuild batch-get-builds, re-read this pass 2026-09-04 17:0xZ)",
    "digest": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
    "tags": ["latest", "20260904-080337"],
    "pushed_at": "2026-09-04T08:03:52Z",
    "built_from_commit": "5644fee152600506259a8869f7067e89c8e6c0f2",
    "pre_cut_digest_replaced": "sha256:68bd8b932689a331928c1c3a6cc00fe124d24e04e7a9b64ba008f1a2d3de10e8",
    "note": "BUILT ON THE FIRST PASS, NOT REBUILT HERE. build_id.txt and digest.txt at HEAD agree with ECR, so step 2 was not repeated."
  },

  "copy_source_diff": {
    "instrument": "my own Dockerfile COPY parse over `git show HEAD:infra/aws/globgrph/Dockerfile`, a SECOND instrument beside build-derive-image.sh's grep+awk which leg L3 used",
    "denominator": "37 zip sources = 35 distinct COPY sources + Dockerfile + buildspec.yml (35 COPY directives, 35 distinct -- no duplicate source)",
    "from_last_built_commit": "649164d75bc96b7c9f3001a9342108a5852ad0a2 (the commit behind the image being replaced, C-2's build)",
    "to": "5644fee152600506259a8869f7067e89c8e6c0f2 (the built commit) and to this branch's HEAD",
    "changed_files": [
      {
        "path": "org/modules/graph/comp_aws_cli.py",
        "numstat": "168 insertions / 18 deletions",
        "commits": "1 -- b5bc1c8b27 (NFRA_CLDGRPH: preserve S3 notification read state, the C-3 deriver fix)",
        "families_depending_on_it": "family (1) globgrph-derive-runner ONLY -- imported by exactly one file in the image, infra/aws/globgrph/derive_runner.py:40 `import comp_aws_cli`; every other reference in infra/aws/globgrph is a comment or a shape note"
      }
    ],
    "dockerfile_changed": false,
    "buildspec_changed": false,
    "anything_beyond_the_deriver_fix": "NO. Over the 37-path set the diff is exactly one file and one commit. Dockerfile and buildspec.yml are byte-identical to the last build, so there is no new pip dependency and no resolution risk for families (2)-(7).",
    "built_commit_vs_this_HEAD": "EMPTY DIFF over all 37 paths -- the running image is current with this branch's HEAD on every byte the image carries."
  },

  "pins_applied": {
    "edit_surface": "one local + three image lines; the Pipe target already referenced aws_ecs_task_definition.projection_worker.arn and needed no edit",
    "local": "infra/aws/terraform/globgrph/serving.tf:22  globgrph_image_digest = \"sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778\"",
    "image_lines": [
      "infra/aws/terraform/globgrph/item2a.tf:361  aws_ecs_task_definition.derive_runner",
      "infra/aws/terraform/globgrph/projection.tf:231  aws_ecs_task_definition.projection_worker",
      "infra/aws/terraform/globgrph/serving.tf:125  aws_ecs_task_definition.globgrph_serving"
    ],
    "terraform_fmt_check": "rc 0 on all three files",
    "apply": {
      "command": "bash .tools/safe-apply.sh -chdir=infra/aws/terraform/globgrph apply -input=false -no-color -auto-approve -target=<eight addresses>",
      "addresses": [
        "aws_ecs_task_definition.derive_runner",
        "aws_ecs_task_definition.projection_worker",
        "aws_ecs_task_definition.globgrph_serving",
        "aws_pipes_pipe.projection_worker",
        "aws_iam_role_policy.derive_runner_events_ecs",
        "aws_iam_role_policy.projection_pipe",
        "aws_cloudwatch_event_target.derive_runner_nightly",
        "aws_ecs_service.globgrph_serving"
      ],
      "targeted_plan": "Plan: 3 to add, 5 to change, 3 to destroy. -- exactly those eight, no foreign address (targeted_plan.txt)",
      "apply_result": "Apply complete! Resources: 3 added, 5 changed, 3 destroyed. rc 0 (targeted_apply.txt)",
      "unscoped_plan_control": {
        "file": "unscoped_plan_pre.txt (run BEFORE the apply, against the live S3 backend)",
        "summary": "Plan: 5 to add, 8 to change, 3 to destroy. over 13 addresses",
        "foreign_addresses_not_applied": [
          "aws_codebuild_project.stitch_produce",
          "aws_glue_partition.tool_activity[\"rolling_log\"]",
          "aws_glue_partition.tool_activity[\"rolling_log_summary\"]",
          "aws_glue_partition.tool_activity[\"routing\"]",
          "aws_sns_topic_subscription.critical_surface_alerts_email"
        ],
        "d12_second_carrier": "the TO-CG-D-12 s3:GetBucketNotification inline policy in iam.tf shows NO diff in the unscoped plan -- config and state agree. LEFT EXACTLY AS FOUND, not folded into item2a.tf (row W1-S9 stands)."
      }
    },
    "task_definitions_after": [
      {"family": "globgrph-derive-runner", "arn": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-derive-runner:7", "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"},
      {"family": "globgrph-projection-worker", "arn": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4", "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"},
      {"family": "globgrph-serving", "arn": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-serving:2", "image": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner@sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"}
    ],
    "digest_equals_digest_txt": true,
    "latest_tag_present_in_any_of_the_three": false,
    "pipe_target_live": {
      "pipe": "opal-globgrph-projection-worker",
      "current_state": "RUNNING",
      "target_cluster": "arn:aws:ecs:us-east-1:313476888478:cluster/opal-globgrph",
      "task_definition_arn": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-projection-worker:4"
    },
    "nightly_rule_target_live": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-derive-runner:7 (events list-targets-by-rule opal-globgrph-derive-runner-nightly) -- the revision-scoped ecs:RunTask grants moved WITH the task definitions, so the W1-S2 hazard did not occur"
  },

  "derive_family_launch": {
    "kind": "ONE ad-hoc QA run-task (CLAUDE.md s.5) on the PINNED revision -- the 02:00Z scheduled fire stays the acceptance",
    "task_arn": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/4a1baae562c8496983eb068146ae33d5",
    "task_definition": "globgrph-derive-runner:7",
    "network": "FARGATE, subnet-023db8cbfd99ffff2, sg-0f6cedf53107c6f8c, assignPublicIp ENABLED -- the nightly rule's own live parameters, mirrored",
    "started_at": "1788539432.975 = 2026-09-04T16:30:32Z",
    "stopped_at": "1788540008.657 = 2026-09-04T16:40:08Z (576 s)",
    "exit_code": 0,
    "stopped_reason": "Essential container in task exited",
    "image_digest": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778 (= the pin)",
    "log_group": "/ecs/globgrph/derive-runner",
    "log_stream": "derive-runner/derive-runner/4a1baae562c8496983eb068146ae33d5",
    "denominator_line": "s3 notifications buckets read=34 / buckets unreadable=0; unreadable=none",
    "contrast": "the FIRST pass's derive (task 7286e56c..., ledger leg L5) read 0 of 34 -- the IAM gap row W1-S7 named. TO-CG-D-12's grant moved it to 34 of 34."
  },

  "projection_family_launch": {
    "launched_by": "the derive's OWN marker stamp through the EventBridge Pipe -- no hand",
    "marker_before": "warehouse/_branch_head.main.json LastModified Fri 04 Sep 2026 14:45:22 GMT ETag 2b7aeb6f97cb974ed533a0d4b4d8ed10",
    "marker_after": "Fri 04 Sep 2026 16:38:40 GMT ETag 6ac588a987d7e00500ad9c0b248636ce",
    "task_arn": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/7b2d3bbefb2a4573bc5af5c8459f6e8a",
    "task_definition": "globgrph-projection-worker:4 (the pinned revision)",
    "image_digest": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778 (= the pin)",
    "started_at": "1788539938.255 = 2026-09-04T16:38:58Z",
    "stopped_at": "1788540696.908 = 2026-09-04T16:51:36Z (759 s)",
    "exit_code": 0,
    "pointer_put_ok": "POINTER_PUT_OK key=projection/current.json vintage=2026-09-04T16:38:39.485910+00:00 manifest_sha256=c3ba0330e3065984b247a1733f4d62387eff8ad507aad90b7bb7fc27ad337e48",
    "log_group": "/aws/ecs/opal-globgrph-projection-worker",
    "log_stream": "projection-worker/projection-worker/7b2d3bbefb2a4573bc5af5c8459f6e8a"
  },

  "pointer": {
    "before": "2026-09-04T14:45:21.329463+00:00 (manifest_sha256 84eb18f1abc29f55c8d7bfe6e9223f0d9bcfb36bf3d51c35a690181c0fe911a9)",
    "after": "2026-09-04T16:38:39.485910+00:00 (manifest_sha256 c3ba0330e3065984b247a1733f4d62387eff8ad507aad90b7bb7fc27ad337e48)",
    "written_by_this_seat": false
  },

  "serving_family_launch": {
    "deployment_id": "ecs-svc/5051693120450624574",
    "rollout_state": "COMPLETED",
    "task_definition": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-serving:2",
    "running_desired": "1 / 1, and the PRIMARY is the only deployment",
    "new_task_arn": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/8889156e83ad4e3e95931e9d505169a9",
    "new_task_started_at": "1788539216.079 = 2026-09-04T16:26:56Z",
    "new_task_image_digest": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778 (= the pin)",
    "replaced_task": "c18ee8b40e4a4bf3993f8f78cc2f98a6 (by the service's own rolling deployment; no stop-task)",
    "health": "{\"status\":\"ok\",\"vintage\":\"2026-09-04T16:38:39.485910+00:00\",\"pointer_read_at\":\"2026-09-04T16:51:51.910784+00:00\",\"last_swap\":\"2026-09-04T16:51:51.953750+00:00\"}"
  },

  "triggers": {
    "count": 171,
    "served_vintage": "2026-09-04T16:38:39.485910+00:00",
    "derive_started_at": "2026-09-04T16:30:32Z",
    "vintage_is_later_than_derive_start": true,
    "shape_control": "MATCH (n) RETURN count(n) AS nodes -> {\"nodes\":27295} at the same vintage",
    "query_1_as_the_server_received_it": "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type = 'TRIGGERS' RETURN count(e) AS triggers",
    "query_2_as_the_server_received_it": "MATCH (a:CloudNode)-[e:CloudEdge]->(b:CloudNode) WHERE e.edge_type = 'TRIGGERS' AND a.node_id CONTAINS 'opal-data-bd' RETURN b.node_id AS target ORDER BY target",
    "bd_pipeline_targets": [
      "arn:aws:lambda:us-east-1:313476888478:function:bd-allocation-processor",
      "arn:aws:lambda:us-east-1:313476888478:function:bd-gold-trigger",
      "arn:aws:lambda:us-east-1:313476888478:function:bd-silver-merge"
    ],
    "inf_pipeline_targets_additional_evidence": [
      "arn:aws:lambda:us-east-1:313476888478:function:inf-portal-publisher",
      "arn:aws:lambda:us-east-1:313476888478:function:inf-silver-aggregator"
    ],
    "cot_pipeline": "contributes none -- EventBridge-only (S27, corrected at decomposition v0.3; S32 the disarm ack)",
    "instrument": "the REPAIRED triggers_query.sh (row W1-S10): each cypher travels base64 and the script echoes it as the server received it, so the FALSE ZERO class that made the previous pass read triggers:0 cannot hide"
  },

  "the_four_nfra_globgrph_families": {
    "policy": "named per the S31 discipline line, NOT edited and NOT run; they stay on :latest and pick the new image up on their next scheduled fire",
    "next_fire_utc_from_2026_09_04T17_0xZ": [
      {"family": "globgrph-comp-learns-producer", "trigger": "EventBridge Rule opal-globgrph-comp-learns-producer-nightly cron(0 4 * * ? *) ENABLED", "next_fire": "2026-09-05T04:00Z", "claim": "inferred from the cron expression, ENABLED state measured"},
      {"family": "globgrph-cse-producer", "trigger": "EventBridge SCHEDULER globgrph-cse-producer-nightly cron(30 3 * * ? *) ENABLED -- a Rules-only census misses it (W1-S8)", "next_fire": "2026-09-05T03:30Z", "claim": "inferred from the cron expression, ENABLED state measured"},
      {"family": "globgrph-fedobs-producer", "trigger": "EventBridge Rule opal-globgrph-fedobs-producer-nightly cron(30 4 * * ? *) ENABLED", "next_fire": "2026-09-05T04:30Z", "claim": "inferred from the cron expression, ENABLED state measured"},
      {"family": "globgrph-resource-summaries-producer", "trigger": "NONE -- no EventBridge Rule (describe-rule: ResourceNotFoundException) and no Scheduler schedule", "next_fire": "NONE", "claim": "measured; row W1-S8"}
    ]
  },

  "deploy_ledger": {
    "slug": "cldgrph-cgs15-shared-image-digest-pins",
    "entry": "org/critical_paths/change_management/20260904T0756Z_cldgrph-cgs15-shared-image-digest-pins_deploy_completion.md",
    "legs_closed": "7 of 7",
    "status_line": "**Status:** CLOSED -- nothing stranded -- closed 20260904T170545Z",
    "sentinel": "org/critical_paths/.open_deploys/cldgrph-cgs15-shared-image-digest-pins.json -- COMMITTED first (f497b7d71b) so the OPEN state could survive a worktree drain (S34), then UNLINKED by `deploy_ledger.py close` (W2-S5); both states are on this branch."
  },

  "bounds_respected": {
    "marker_or_pointer_written_by_this_seat": false,
    "s3_object_deleted": false,
    "four_nfra_globgrph_families_touched_or_run": false,
    "ad_hoc_derives_this_pass": 1,
    "stop_task_used": false,
    "terraform_files_edited_this_pass": "none -- the local and the three image lines were already at HEAD and re-read, not re-edited",
    "alarm_sns_monitor_built": false
  },

  "rows_filed_this_pass": ["NFRA_CLDGRPH-W1-S11", "NFRA_CLDGRPH-W1-S12"]
}
```

## What this pass proves, and what it does not

**The chain ran end to end on the pinned bytes.** The three families this project owns now reference
`opal-globgrph-derive-runner@sha256:1b89853f...` and no mutable tag; each family's NEXT launch was
observed on that digest -- the derive by this order's own ad-hoc QA run (`globgrph-derive-runner:7`,
exit 0), the projection worker by the real Pipe launch the derive's marker stamp produced
(`globgrph-projection-worker:4`, exit 0, `POINTER_PUT_OK`), and the serving service by its own
rolling deployment reaching `COMPLETED` on `globgrph-serving:2`. Each launch's `imageDigest` was read
from `describe-tasks`, which is the discriminator that separates "ran the new bytes" from "resolved a
tag that happens to point at them".

**The denominator moved for a reason that is not this image.** The first pass's derive, on the same
image bytes, printed `read=0 / unreadable=34`. This pass printed `read=34 / unreadable=0`. The image
did not change between them; the IAM grant of TO-CG-D-12 did. That is worth stating plainly because
it is the exact shape of a false attribution: the rebuild is a NECESSARY condition for the denominator
line to exist at all (C-3 wrote it), and the grant is the condition for its VALUE to be non-zero.
Neither alone produces `TRIGGERS = 171`.

**TRIGGERS = 171 is read through a repaired instrument.** The previous pass read `triggers:0` from
this same script and the reading measured the tool, not the graph (row W1-S10): shell re-quoting made
the server evaluate `e.edge_type='"TRIGGERS"'`, valid and unmatchable, at a correct vintage, beside a
shape control that could not exercise the same hazard because it carries no string literal. The
repaired script transports each cypher as base64 and echoes it as the server received it; that echo is
in the output above, unmangled, beside the answer.

**What this does NOT establish.** `171` is the count at ONE vintage from ONE served projection; it is
not a claim about the completeness of the estate's notification graph, and the `read=34` denominator
certifies the SWEEP (34 buckets the deriver enumerated), not that 34 is every bucket the account has.
The four NFRA_GLOBGRPH families remain on `:latest` by design and their next-fire times above are
INFERRED from cron expressions -- only the ENABLED state and the absence of any trigger for
`globgrph-resource-summaries-producer` are measured. The 02:00Z scheduled derive is the acceptance a
later seat reads; this ad-hoc run is QA, not production evidence.

## Ledger leg L5 -- read it with its date

Leg `L5` was closed on the FIRST pass, against the derive that ran on `globgrph-derive-runner:6`
(unpinned, `read=0/34`). It could not be reopened and the `change_management/*.md` is never hand-edited,
so the leg's text still says "the pin is NOT in force". The derive family's launch ON THE PINNED
REVISION is task `4a1baae562c8496983eb068146ae33d5` recorded above and in row `NFRA_CLDGRPH-W1-S12`,
not the task L5 names. A reader taking L5 as this deploy's pinned-derive proof would be reading a
correct record of a different act.
