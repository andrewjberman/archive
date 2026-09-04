# NFRA_CLDGRPH CG-s-15 -- shared image rebuild, digest pins, live derive

**TO:** `NFRA_CLDGRPH.TO-CG-D-1` · **assignee:** `0.9.0_WK_NFRA_CLDGRPH~1` · **branch:** `wk-NFRA_CLDGRPH-1` · **HEAD:** `5644fee152` (LOCAL)

The image half of CG-s-15 landed and is EXERCISED. The pin half never started: `safe-apply`'s halt gate
refuses the spine-v3 worker serial grammar itself and offers no reachable override, so this seat cannot run
any `terraform apply` (`NFRA_CLDGRPH-W1-S1`). The live derive nevertheless answered the question the cell was
cut to ask -- and the answer is not the one the cell expected: the C-3 denominator line printed
`buckets read=0 / buckets unreadable=34`, which means the silent-zero TRIGGERS defect (S20) is an **IAM gap on
the cloud derive role**, not an image-currency defect. TRIGGERS is still 0, now for a named and measured
reason (`NFRA_CLDGRPH-W1-S7`). The rebuild was necessary and is not sufficient.

```json
{
  "to_id": "NFRA_CLDGRPH.TO-CG-D-1",
  "cell": "CG-s-15",
  "assignee": "0.9.0_WK_NFRA_CLDGRPH~1",
  "source_commit": "5644fee152600506259a8869f7067e89c8e6c0f2",
  "push_state": "LOCAL (no push attempted; worker branch)",

  "build": {
    "build_id": "globgrph-derive-build:442305e5-9d54-4e89-96de-b22a6ed9f776",
    "build_status": "SUCCEEDED",
    "start_time_epoch": 1788508908.293,
    "end_time_epoch": 1788509033.546,
    "env_override": "PROJECTION_SOURCE_COMMIT=5644fee152600506259a8869f7067e89c8e6c0f2",
    "source_zip": {
      "key": "s3://opal-313476888478-globgrph/build-source/derive-runner-source.zip",
      "entries": 37,
      "bytes_local": 449396,
      "bytes_read_back_from_s3": 449396,
      "etag_read_back": "a4cbe63234f0a3e3ad22e12113f91daa",
      "md5_local": "a4cbe63234f0a3e3ad22e12113f91daa",
      "last_modified": "2026-09-04T08:00:09Z",
      "pre_state_bytes": 447665,
      "pre_state_etag": "db6386e955e58a1bb9a4c1a6c0d1007e",
      "verified_by": "s3api head-object read-back, NOT the cp exit code",
      "baked_artifact_control": {
        "c2_instances.json": 0,
        "c3_structures.json": 0,
        "positive_control_same_grep": {"c2_individuate.py": 1, "c3_cover.py": 1, "comp_aws_cli.py": 1}
      }
    },
    "image": {
      "repository": "313476888478.dkr.ecr.us-east-1.amazonaws.com/opal-globgrph-derive-runner",
      "digest": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
      "tags": ["latest", "20260904-080337"],
      "pushed_at_epoch": 1788509032.393,
      "previous_digest": "sha256:68bd8b932689a331928c1c3a6cc00fe124d24e04e7a9b64ba008f1a2d3de10e8",
      "previous_build": "globgrph-derive-build:efc258e6-713c-47ae-ba79-fa2e691e0d0e"
    }
  },

  "copy_source_diff": {
    "from_commit": "649164d75bc96b7c9f3001a9342108a5852ad0a2",
    "from_commit_provenance": "TO-CG-C-2 result, image.build_source_head -- the commit behind the image being replaced",
    "to_commit": "5644fee152600506259a8869f7067e89c8e6c0f2",
    "denominator": 37,
    "denominator_derivation": "35 Dockerfile COPY sources + Dockerfile + buildspec.yml, agreed by TWO independent instruments (a python COPY parse and build-derive-image.sh's own grep+awk)",
    "missing": 0,
    "dirty": 0,
    "changed": 1,
    "table": [
      {
        "file": "org/modules/graph/comp_aws_cli.py",
        "commits": 1,
        "commit": "b5bc1c8b27 NFRA_CLDGRPH: preserve S3 notification read state",
        "blob_before": "57788c66dc18e244ede9d9cd841f4a333cdddada",
        "blob_after": "327c35cfcb105b999220c66f8801860a864acf0c",
        "diffstat": "168 insertions, 18 deletions",
        "families_depending_on_it": ["globgrph-derive-runner"],
        "why_only_that_family": "the ONLY import in the image is infra/aws/globgrph/derive_runner.py:40 `import comp_aws_cli`; the other 20 references across infra/aws/globgrph are comments or shape notes (e.g. resource_summaries_store.py:300)"
      }
    ],
    "anything_beyond_the_deriver_fix": "NO",
    "dockerfile_and_buildspec": "byte-identical to the last build (empty diffstat) -- therefore NO new pip dependency and no resolution risk for any of the seven families",
    "contrast_with_precedent": "the 2026-08-26 rebuild shipped 10 changed files over 58 commits plus a new pip dep (kuzu==0.11.3); this one ships 1 file over 1 commit"
  },

  "seven_families_blast_radius": {
    "pinned_by_this_order": "NONE -- the apply never ran (NFRA_CLDGRPH-W1-S1)",
    "families": [
      {"n": 1, "family": "globgrph-derive-runner", "project": "NFRA_CLDGRPH", "task_def": "globgrph-derive-runner:6", "image_ref": ":latest", "next_fire": "cron(0 2 * * ? *) EventBridge Rule opal-globgrph-derive-runner-nightly", "exercised_on_new_image": true},
      {"n": 2, "family": "globgrph-projection-worker", "project": "NFRA_CLDGRPH", "task_def": "globgrph-projection-worker:3", "image_ref": ":latest", "next_fire": "on the next marker stamp via Pipe opal-globgrph-projection-worker", "exercised_on_new_image": true},
      {"n": 3, "family": "globgrph-serving", "project": "NFRA_CLDGRPH", "task_def": "globgrph-serving:1", "image_ref": ":latest", "next_fire": "only on a service deployment; the running task is NOT replaced by a tag move", "exercised_on_new_image": false},
      {"n": 4, "family": "globgrph-comp-learns-producer", "project": "NFRA_GLOBGRPH", "task_def": "globgrph-comp-learns-producer:1", "image_ref": ":latest", "next_fire": "cron(0 4 * * ? *) EventBridge Rule opal-globgrph-comp-learns-producer-nightly", "exercised_on_new_image": false},
      {"n": 5, "family": "globgrph-cse-producer", "project": "NFRA_GLOBGRPH", "task_def": "globgrph-cse-producer:1", "image_ref": ":latest", "next_fire": "cron(30 3 * * ? *) EventBridge SCHEDULER globgrph-cse-producer-nightly -- a DIFFERENT service from Rules; a Rules-only census reports this family unscheduled", "exercised_on_new_image": false},
      {"n": 6, "family": "globgrph-fedobs-producer", "project": "NFRA_GLOBGRPH", "task_def": "globgrph-fedobs-producer:1", "image_ref": ":latest", "next_fire": "cron(30 4 * * ? *) EventBridge Rule opal-globgrph-fedobs-producer-nightly", "exercised_on_new_image": false},
      {"n": 7, "family": "globgrph-resource-summaries-producer", "project": "NFRA_GLOBGRPH", "task_def": "globgrph-resource-summaries-producer:1", "image_ref": ":latest", "next_fire": "NONE -- no EventBridge Rule, no Scheduler, and the only reference to its task definition in infra/aws/terraform is an `output` (row NFRA_CLDGRPH-W1-S8)", "exercised_on_new_image": false}
    ],
    "note": "families 4-7 were NAMED, never edited and never run, per the order's bound"
  },

  "terraform": {
    "edits_made": "one local + three image lines; NOTHING else",
    "diffstat": "item2a.tf +6-2, projection.tf +6-2, serving.tf +15-1 (3 files, 22 insertions, 5 deletions)",
    "local": {"file": "infra/aws/terraform/globgrph/serving.tf", "name": "globgrph_image_digest", "value": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778", "placement_reason": "locals.tf does not exist and the module's other locals live in main.tf, which is OUTSIDE this order's PATHS block -- the order's own stated fallback"},
    "image_lines": [
      "item2a.tf:361 aws_ecs_task_definition.derive_runner -> ...amazonaws.com/opal-globgrph-derive-runner@${local.globgrph_image_digest}",
      "projection.tf:231 aws_ecs_task_definition.projection_worker -> ${aws_ecr_repository.derive_runner.repository_url}@${local.globgrph_image_digest}",
      "serving.tf:125 aws_ecs_task_definition.globgrph_serving -> ${aws_ecr_repository.derive_runner.repository_url}@${local.globgrph_image_digest}"
    ],
    "pipe_target": "aws_pipes_pipe.projection_worker target_parameters.ecs_task_parameters.task_definition_arn ALREADY reads aws_ecs_task_definition.projection_worker.arn -- a symbolic reference that follows the new revision, so NO text edit was needed or made",
    "fmt_check": "terraform fmt -check -diff item2a.tf projection.tf serving.tf -> rc 0, no diff",
    "unscoped_plan_control": {
      "file": "unscoped_plan_pre.txt",
      "summary": "Plan: 5 to add, 8 to change, 3 to destroy",
      "address_count": 13,
      "mine": ["aws_ecs_task_definition.derive_runner", "aws_ecs_task_definition.projection_worker", "aws_ecs_task_definition.globgrph_serving", "aws_pipes_pipe.projection_worker", "aws_iam_role_policy.derive_runner_events_ecs", "aws_iam_role_policy.projection_pipe", "aws_cloudwatch_event_target.derive_runner_nightly", "aws_ecs_service.globgrph_serving"],
      "foreign": ["aws_sns_topic_subscription.critical_surface_alerts_email", "aws_glue_partition.tool_activity[\"routing\"]", "aws_glue_partition.tool_activity[\"rolling_log\"]", "aws_glue_partition.tool_activity[\"rolling_log_summary\"]", "aws_codebuild_project.stitch_produce"],
      "foreign_known_from_C1_C2": 4,
      "foreign_new_since_C2": ["aws_codebuild_project.stitch_produce -- a buildspec re-render diff, pre-existing, not adjudicated here"],
      "stale_outputs_found": "7 root outputs planned for removal with no accompanying resource change -- residue of the authorized 858554332d freshness teardown (row NFRA_CLDGRPH-W1-S3); the TARGETED plan does not touch them"
    },
    "targeted_plan": {
      "file": "targeted_plan.txt",
      "summary": "Plan: 3 to add, 5 to change, 3 to destroy",
      "addresses": 8,
      "address_set_correction": "the order named FOUR; the measured dependent closure is EIGHT. The two IAM role policies scope `ecs:RunTask` to the task definition AT ITS REVISION, and -target pulls a resource's dependencies but never its DEPENDENTS -- a four-address apply would have left the nightly rule and the Pipe authorized only for the revisions the same apply superseded (row NFRA_CLDGRPH-W1-S2)",
      "output_changes": "exactly one, derive_runner_task_definition_arn"
    },
    "targeted_apply": {
      "status": "NEVER RAN",
      "blocker": "NFRA_CLDGRPH-W1-S1 -- .tools/safe-apply.sh fires .tools/halt-gate-check.sh, whose halt_gate_validate_serial rejects 0.9.0_WK_NFRA_CLDGRPH~1 on BOTH limbs (lane suffix must be [A-Z], base must match an agent home folder; 105 folders censused, 0 match, positive control 2.0.0_SA_COO -> 3). rc 3, terraform never invoked, with HALT_OVERRIDE and HALT_ACK both set.",
      "bare_terraform_apply": "NOT RUN -- forbidden, and not attempted"
    }
  },

  "derive_family_launch": {
    "kind": "ONE ad-hoc run-task, QA (CLAUDE.md s.5); the 02:00Z scheduled fire remains the acceptance",
    "task_arn": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/7286e56c80614ab49fa2fba791bb8b43",
    "task_definition": "globgrph-derive-runner:6 (UNPINNED -- references :latest, which now resolves to the new digest)",
    "params_source": "events list-targets-by-rule opal-globgrph-derive-runner-nightly, mirrored exactly: subnet-023db8cbfd99ffff2, sg-0f6cedf53107c6f8c, assignPublicIp ENABLED, FARGATE",
    "image_digest_actually_run": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
    "exit_code": 0,
    "started_at_epoch": 1788511057.509,
    "stopped_at_epoch": 1788511860.622,
    "duration_seconds": 803,
    "log_group": "/ecs/globgrph/derive-runner",
    "log_stream": "derive-runner/derive-runner/7286e56c80614ab49fa2fba791bb8b43",
    "denominator_line": "s3 notifications buckets read=0 / buckets unreadable=34; unreadable=opal-313476888478-globgrph,opal-313476888478-lambda-artifacts,opal-313476888478-lambda-layers,opal-313476888478-terraform-state,opal-313476888478-yang-qa-scratch,opal-cloudtrail-logs-313476888478,opal-cur-313476888478,opal-data-49financial,opal-data-assets,opal-data-astn,opal-data-bd,opal-data-cot,opal-data-demo,opal-data-etfs,opal-data-imo,opal-data-inf,opal-data-mdpf,opal-data-news-av,opal-data-news-v2,opal-data-pm,opal-data-portal-v2,opal-data-portfolio,opal-data-security,opal-data-security-access-logs,opal-data-trade-submissions,opal-estate-report,opal-infrastructure-snapshots,opal-mcp-athena-results,opal-mcp-audit,opal-runner-shared,opal-security-evidence,opal-served-key-write-trail-logs,opal-website-backups,opalinvest-portal"
  },

  "projection_family_launch": {
    "task_arn": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/08459e7d5608493bb149fb991b16fe1b",
    "started_by": "Started by Eventbridge Pipes -- the REAL launch the derive's marker stamp caused, not a driven run",
    "task_definition": "globgrph-projection-worker:3 (UNPINNED, :latest)",
    "image_digest_actually_run": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
    "digest_equals_the_intended_pin": true,
    "reference_is_pinned": false,
    "exit_code": 0,
    "started_at_epoch": 1788511779.664,
    "stopped_at_epoch": 1788512664.603,
    "duration_seconds": 885,
    "mode": "INCR_RESULT status=fallback -- delta 27296 >= 4000 and >= 25% of head, bulk reload cheaper",
    "pointer_log_order": ["POINTER_VERIFY_OK", "POINTER_PUT_OK"],
    "node_count": 27278,
    "edge_count": 58727
  },

  "marker_and_pointer": {
    "marker_pre": {"last_modified": "2026-09-04T05:53:38Z", "etag": "ee38c260c3d7eb67149113474497289e"},
    "marker_post": {"last_modified": "2026-09-04T08:49:21Z", "etag": "bfe5c18640c822ca1f476f7c22b9adf1"},
    "pointer_pre_vintage": "2026-09-04T05:53:37.689093+00:00",
    "pointer_post_vintage": "2026-09-04T08:49:20.217966+00:00",
    "pointer_post_manifest_sha256": "6f6fa5fe50b4730d75652012575b13a150e9dde86a55dc027bd2b266918d0a94",
    "written_by": "the derive runner and the projection worker themselves; this seat wrote NO marker, NO pointer and NO object under projection/"
  },

  "serving_family_launch": {
    "status": "DID NOT HAPPEN -- no new task, no new revision",
    "primary_deployment_rollout_state": "COMPLETED",
    "primary_deployment_task_definition": "arn:aws:ecs:us-east-1:313476888478:task-definition/globgrph-serving:1",
    "reason": "a service only redeploys on a task-definition change, and the apply is blocked (NFRA_CLDGRPH-W1-S1). No force-new-deployment and no stop-task were used -- the order forbids replacing the task by hand.",
    "artifact_swap_did_happen": "the RUNNING serving process picked the new vintage up in place via its 60 s pointer watch: /health last_swap 2026-09-04T09:04:50.007848+00:00, vintage 2026-09-04T08:49:20.217966+00:00 -- an ARTIFACT swap, which is NOT the task replacement D1-AC6 asks for"
  },

  "triggers_query": {
    "instrument": "triggers_query.sh -- SSM AWS-RunShellScript on i-07dccb1615503ac99 -> curl http://projection.opal-globgrph.local:8181/cypher",
    "post_derive": {
      "vintage": "2026-09-04T08:49:20.217966+00:00",
      "vintage_is_later_than_derive_start": true,
      "shape_control_nodes": 27278,
      "triggers": 0,
      "bd_targets": []
    },
    "pre_derive_baseline": {
      "vintage": "2026-09-04T05:53:37.689093+00:00",
      "shape_control_nodes": 27244,
      "triggers": 0,
      "bd_targets": []
    },
    "why_the_shape_control_matters": "nodes answers 27278 on the same transport in the same call, so triggers=0 is the GRAPH's answer and not a dead query path -- the discrimination the silent-zero class needs",
    "cause": "NFRA_CLDGRPH-W1-S7 -- the derive task role opal-globgrph-derive-runner-task has no s3:GetBucketNotification, so 0 of 34 buckets' notification configurations were readable and no S3_BUCKET-[TRIGGERS]->LAMBDA edge can be derived in the cloud at all"
  },

  "deploy_ledger": {
    "entry": "org/critical_paths/change_management/20260904T0756Z_cldgrph-cgs15-shared-image-digest-pins_deploy_completion.md",
    "slug": "cldgrph-cgs15-shared-image-digest-pins",
    "state": "OPEN (RED)",
    "closed_legs": ["L1", "L2", "L3", "L5"],
    "stranded_legs": ["L4", "L6", "L7"],
    "hold_attempted_and_REFUSED": "deploy_ledger.py hold -> 'REFUSED: cannot HELD -- open APPLY/DEPLOY leg(s) [L4] -- a half-landed deploy cannot be HELD (stays RED)'. The entry therefore stays OPEN and BLARES, which IS the loud escalation NEVER-2 asks for; it was not silenced.",
    "leg_kind_substitution": "the order declares L5/L6/L7 as kind `exercise`, which deploy_ledger.py refuses (LEG_KINDS has no such member); opened as `verify` with the order's ids and proof text verbatim (row NFRA_CLDGRPH-W1-S4)"
  },

  "rollback_considered": {
    "decision": "NOT rolled back",
    "reasoning": "the world is CONSISTENT, not half-landed: the pin never started, so no family sits in an intermediate state -- every family is exactly where :latest semantics put it, which is where it was before this act. The new image is MEASURED GOOD end to end (derive exit 0, projection exit 0, pointer advanced, serving swapped, 27278 nodes / 58727 edges) and differs from its predecessor by one file and one commit with no dependency change. Re-pointing :latest backwards would delete the only instrument that has ever named S20's cause and would itself be an unexercised mutation.",
    "contrast": "the 2026-08-26 precedent rolled back because its verification run FAILED at import; this one has a measured clean run on both consumers"
  },

  "surprise_rows_filed": [
    "NFRA_CLDGRPH-W1-S1 BLOCKING/ARMED -- halt gate refuses every spine-v3 worker serial; no terraform apply is possible for this seat",
    "NFRA_CLDGRPH-W1-S2 OBSERVATION/ARMED -- the apply address set is 8, not the 4 the order names",
    "NFRA_CLDGRPH-W1-S3 OBSERVATION/ARMED -- 7 stale root outputs in the module's state",
    "NFRA_CLDGRPH-W1-S4 OBSERVATION/INERT -- no `exercise` leg kind; safe-apply is .tools/safe-apply.sh",
    "NFRA_CLDGRPH-W1-S5 OBSERVATION/INERT -- non-ASCII in 8 of 22 module .tf files",
    "NFRA_CLDGRPH-W1-S6 OBSERVATION/ARMED -- sibling workers share one scratchpad directory; same-named files overwrite silently",
    "NFRA_CLDGRPH-W1-S7 BLOCKING/ARMED -- s3:GetBucketNotification missing from the derive role: the ROOT CAUSE of S20",
    "NFRA_CLDGRPH-W1-S8 OBSERVATION/ARMED -- globgrph-resource-summaries-producer has no trigger at all"
  ]
}
```

## What this run settles, and what it does not

**Settled.** The image is current: `:latest` and `20260904-080337` both resolve to
`sha256:1b89853f...`, built by CodeBuild `442305e5-9d54-4e89-96de-b22a6ed9f776` from a source zip
whose S3 read-back matched local bytes on size AND ETag. Exactly one COPY source moved since the
image it replaces -- `comp_aws_cli.py`, the C-3 deriver fix, one commit -- and the Dockerfile and
buildspec are byte-identical, so no other family inherits anything and there is no new pip
dependency. Two of the seven consumers then ran the new bytes to completion: the derive (exit 0,
803 s) and the projection worker the derive's own marker stamp launched through the Pipe (exit 0,
885 s, `POINTER_VERIFY_OK` then `POINTER_PUT_OK`, pointer advanced 05:53:37 -> 08:49:20). The
serving process picked the new artifact up in place at 09:04:50. Nothing in the chain needed a
manual marker, pointer or S3 write, and none was made.

**Not settled, and the reason is measured.** No family is pinned by digest, because no
`terraform apply` ran: `safe-apply` fires a halt gate whose serial validator admits neither limb of
a spine-v3 worker serial -- the `~1` slot suffix is a digit where it requires `[A-Z]`, and no agent
home folder exists for a `0.9.0_WK_*` seat (105 folders censused, 0 matches, positive control
returns 3). The identity refusal returns before the audited-override branch, and setting
`HALT_OVERRIDE` and `HALT_ACK` together still produced rc 3 with terraform never invoked. That is
`NFRA_CLDGRPH-W1-S1`, and it closes D1-AC3, D1-AC6 and D1-AC7 to this seat. The plan itself is
sound and saved: eight addresses, `3 to add, 5 to change, 3 to destroy`, one output, no foreign
address -- and the address set is **eight, not the four the order names**, because two IAM role
policies scope `ecs:RunTask` to the task definition at its revision and `-target` never pulls a
dependent (`NFRA_CLDGRPH-W1-S2`). A four-address apply would have produced a green result and a
nightly derive that cannot start.

**The finding that outranks both.** D1-AC5 asked for a non-zero TRIGGERS count and got 0 -- but for
the first time the derive said why. `buckets read=0 / buckets unreadable=34`, all 34 named. The
derive task role `opal-globgrph-derive-runner-task` carries four inline policies and no attached
managed policy, and its complete S3 action set is `GetBucketPolicy, GetBucketVersioning,
GetBucketLocation, ListAllMyBuckets, GetObject, PutObject, DeleteObject, ListBucket`.
`s3:GetBucketNotification` -- the single API that yields an `S3_BUCKET-[TRIGGERS]->LAMBDA` edge --
is absent from the role and, measured with a positive control, from all 495 terraform files in the
estate. The laptop's 34-read / TRIGGERS=188 came from a different principal, not different code:
same image digest, same bytes, opposite result. So S20's silent zero is an IAM gap, S28's disarm
cannot complete on an image rebuild alone, and the correct next act is a grant in
`infra/aws/terraform/globgrph/iam.tf` -- outside this order's PATHS block and behind the same
blocked apply. That is `NFRA_CLDGRPH-W1-S7`, and whoever closes S20 should read it first, because
closing S20 on the rebuild would close it on the wrong cause.

The value the C-3 fix delivered is precisely this: before it, this run would have shown TRIGGERS=0
with nothing to say about why, and the next seat would have rebuilt the image again. The fix did not
make the count non-zero. It made the zero answerable.

## Ledger

`org/critical_paths/change_management/20260904T0756Z_cldgrph-cgs15-shared-image-digest-pins_deploy_completion.md`
is **OPEN and RED**, 4 of 7 legs closed with proof (L1 zip, L2 build, L3 diff, L5 derive), 3 stranded
(L4 apply, L6 projection-on-the-pin, L7 serving). A `hold` was attempted and correctly refused -- the
tool will not let an entry with an open apply leg go quiet. Leaving it RED is the loud escalation,
not an oversight; it names its blocker in every leg's text and in `NFRA_CLDGRPH-W1-S1`.
