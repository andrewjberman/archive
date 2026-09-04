# NFRA_CLDGRPH CG-s-16 -- the IAM grant that was the real cause of S20's silent zero

**TO:** `NFRA_CLDGRPH.TO-CG-D-12` · **cell** CG-s-16 (decomposition v0.4) · **seat** `0.9.0_WK_NFRA_CLDGRPH~1`
· **branch** `wk-NFRA_CLDGRPH-1` (LOCAL, never pushed) · **2026-09-04**

```json
{
  "verdict": "the grant is APPLIED, READ LIVE and EXERCISED end to end: 34 of 34 buckets readable, 182 TRIGGERS edges derived, 171 served, the three declared bd-pipeline targets present at a vintage this order's own derive produced. All six mechanical criteria PASS by output. TWO surprise rows, one of them the reason a passing criterion nearly read as a failing one.",

  "the_statement_before": {
    "where_the_order_said_it_was": "infra/aws/terraform/globgrph/iam.tf, the role's `Sid AccountWideReadOnly` statement",
    "where_it_actually_is": "infra/aws/terraform/globgrph/item2a.tf:129, Sid AccountWideReadOnly inside `aws_iam_role_policy.derive_runner_describe` (policy name DeriveRunnerAccountDescribe, role = aws_iam_role.derive_runner_task.id at item2a.tf:123)",
    "iam_tf_actually_carries": "three principals -- aws_iam_role.nessie_task (:30), aws_iam_role.nessie_execution (:99), aws_iam_role.globgrph_incremental_updater (:113) -- and no mention of the derive runner at all",
    "condition_on_the_statement": "NONE. Checked before applying because the order asks: a conditioned grant reads implicitDeny/MissingContext on simulate, a FALSE deny the criterion could not have graded. Neither the existing AccountWideReadOnly statement nor the one this order added carries a Condition, so both simulate calls below are gradeable at face value.",
    "s3_actions_on_the_role_before": ["s3:GetBucketPolicy", "s3:GetBucketVersioning", "s3:GetBucketLocation", "s3:ListAllMyBuckets", "s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:ListBucket"],
    "s3_getbucketnotification_before": "ABSENT -- and re-measured by this seat on the LIVE principal before touching anything: simulate-principal-policy s3:GetBucketNotification on arn:aws:s3:::opal-data-bd -> `implicitDeny 0`",
    "inline_policy_denominator_before": 4,
    "inline_policy_denominator_after": 5
  },

  "the_statement_after": {
    "address": "aws_iam_role_policy.derive_runner_bucket_notification (NEW, in infra/aws/terraform/globgrph/iam.tf)",
    "policy_name": "DeriveRunnerBucketNotificationRead",
    "role": "aws_iam_role.derive_runner_task -> opal-globgrph-derive-runner-task",
    "statement": {"Sid": "BucketNotificationRead", "Effect": "Allow", "Action": ["s3:GetBucketNotification"], "Resource": "*"},
    "why_not_the_statement_the_order_named": "item2a.tf is NOT in this order's <paths> (it appears under SURFACES as READ). Editing it would have been an out-of-grant write, which is a row and never an override. Row NFRA_CLDGRPH-W1-S9.",
    "effect_difference_from_the_order_s_shape": "NONE at the IAM plane -- a role's inline policies are evaluated as a union, so no consumer can tell the two placements apart; the difference is visible only to a human reading the source, which is exactly what the row is filed about.",
    "fmt_check": "terraform fmt -check infra/aws/terraform/globgrph/iam.tf -> rc 0"
  },

  "plan_and_apply": {
    "targeted_plan_address_list": ["aws_iam_role_policy.derive_runner_bucket_notification will be created"],
    "targeted_plan_summary": "Plan: 1 to add, 0 to change, 0 to destroy",
    "the_order_expected": "0 to add, 1 to change, 0 to destroy -- the shape difference IS row W1-S9, not a scope difference",
    "apply_route": ".tools/safe-apply.sh -chdir=infra/aws/terraform/globgrph apply <saved targeted plan>",
    "halt_gate": "PASSED: 'HALT-GATE: worker 0.9.0_WK_NFRA_CLDGRPH~1 has no inbox; scanning its issuer 2.0.0_SA_COO~A (a [STOP] to the issuer halts its workers)'. This is the repair at 68f22f74f5 exercised: row W1-S1 recorded that NO spine-v3 worker could run any terraform apply, and that blocker is now measured GONE on the live gate, not merely declared fixed.",
    "apply_summary": "Apply complete! Resources: 1 added, 0 changed, 0 destroyed",
    "apply_id": "opal-globgrph-derive-runner-task:DeriveRunnerBucketNotificationRead",
    "unscoped_plan_control": {
      "when": "pre-apply, saved at deliverables/0.9.0_WK_NFRA_CLDGRPH~1/unscoped_plan_pre_d12.txt",
      "summary": "Plan: 6 to add, 8 to change, 3 to destroy",
      "addresses": 14,
      "mine": ["aws_iam_role_policy.derive_runner_bucket_notification"],
      "foreign_and_pre_existing_not_applied": ["aws_cloudwatch_event_target.derive_runner_nightly", "aws_codebuild_project.stitch_produce", "aws_ecs_service.globgrph_serving", "aws_ecs_task_definition.derive_runner", "aws_ecs_task_definition.globgrph_serving", "aws_ecs_task_definition.projection_worker", "aws_glue_partition.tool_activity[rolling_log]", "aws_glue_partition.tool_activity[rolling_log_summary]", "aws_glue_partition.tool_activity[routing]", "aws_iam_role_policy.derive_runner_events_ecs", "aws_iam_role_policy.projection_pipe", "aws_pipes_pipe.projection_worker", "aws_sns_topic_subscription.critical_surface_alerts_email"],
      "reading": "13 of 14 pending addresses are foreign and pre-existing (the task-definition replacements are row W1-S2's territory, the stale root outputs row W1-S3's); the targeted apply dragged none of them."
    }
  },

  "the_two_simulate_reads": {
    "D12-AC1_positive": {
      "invocation": ".tools/aws iam simulate-principal-policy --policy-source-arn arn:aws:iam::313476888478:role/opal-globgrph-derive-runner-task --action-names s3:GetBucketNotification --resource-arns arn:aws:s3:::opal-data-bd --query 'EvaluationResults[0].[EvalDecision,length(MatchedStatements)]' --output text",
      "output": "allowed\t1",
      "one_arn_per_call": true
    },
    "D12-AC2_negative_control": {
      "invocation": "same, --action-names s3:PutBucketNotification --query 'EvaluationResults[0].EvalDecision'",
      "output": "implicitDeny",
      "what_it_bounds": "the write twin of the granted action stays denied on the same principal and the same resource -- the grant is one action wide, not a class"
    },
    "pre_state_baseline_on_the_same_instrument": "implicitDeny\t0 before the apply -- so the `allowed` is THIS act's and the instrument is not stuck-allow"
  },

  "the_derive": {
    "kind": "ONE ad-hoc QA run (CLAUDE.md s.5). The 02:00Z scheduled fire stays the acceptance the L9 seat reads.",
    "task_arn": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/aeb8dec6982a43bd80fe49a9ed34b871",
    "task_definition": "globgrph-derive-runner:6 (UNPINNED, :latest -- the pins are TO-CG-D-1's, sequenced AFTER this order)",
    "image_digest_actually_run": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
    "run_params": "subnet-023db8cbfd99ffff2, sg-0f6cedf53107c6f8c, assignPublicIp ENABLED, FARGATE -- mirrored from the nightly rule",
    "exit_code": 0,
    "started_at_epoch": 1788526055.745,
    "stopped_at_epoch": 1788526655.232,
    "duration_seconds": 599.5,
    "log_group": "/ecs/globgrph/derive-runner",
    "log_stream": "derive-runner/derive-runner/aeb8dec6982a43bd80fe49a9ed34b871",
    "denominator_line": "s3 notifications buckets read=34 / buckets unreadable=0; unreadable=none",
    "the_same_line_before_the_grant": "s3 notifications buckets read=0 / buckets unreadable=34; unreadable=<all 34 named>",
    "edge_summary": "edges total=3940 ALIAS_TO=1 ASSUMES=253 CAN_ASSUME=218 DEAD_LETTERS_TO=6 EMITS_TO=145 ENCRYPTS_WITH=45 GRANTS=20 HAS_POLICY=622 HAS_PROFILE=31 HAS_ROUTE=86 INVOKES=43 IN_SUBNET=2 IN_VPC=1 LOGS_TO=212 MONITORS=27 NOTIFIES=41 ORIGIN=5 PUBLISHES_TO=48 READS=810 READS_SECRET=311 ROUTES_TO=86 SENDS_TO=10 SUBSCRIBES=10 TRIGGERS=182 USES_LAYER=78 USES_OAC=1 USES_OAI=4 USES_SG=2 WRITES=640",
    "triggers_derived": 182,
    "completion": "OK: DERIVE_RUNNER_COMPLETE date=20260904 batch_ts=1788526056030"
  },

  "the_chain_and_the_served_read": {
    "marker": "OK: MARKER_STAMPED writer=derive_runner hash=4bb3844b5243976ac128dd97ffda29ca1c6157002ed1a32ba49367661bd560eb nodes_snap=4492677536813842224 edges_snap=1732740251598783067",
    "projection_worker": "task 7b7800b7e4b24353829f167af774cb12, 'Started by Eventbridge Pipes' (NOT a driven run), 12:56:21Z -> 13:09:54Z, exit 0",
    "pointer_advanced_at": "2026-09-04T13:09:29Z (s3api head-object LastModified, UTC)",
    "post_derive_vintage": "2026-09-04T12:55:59.236365+00:00",
    "derive_start": "2026-09-04T12:47:35Z (task startedAt 1788526055.745); run-task issued 12:47:06Z",
    "vintage_is_later_than_derive_start": true,
    "serving_swap": "/health last_swap 2026-09-04T13:10:26.957439+00:00, pointer_read_at 13:10:26.950195+00:00",
    "lineage_proof_not_assumption": "the build manifest at projection/2026-09-04T12:55:59.236365+00:00/_build_manifest.json carries nodes_snapshot_id 4492677536813842224, edges_snapshot_id 1732740251598783067, nessie_commit_hash 4bb3844b... -- byte-identical to this derive's marker line. The served answer is THIS derive's graph. (It matters: three other projections advanced the pointer between 12:17Z and 12:48Z today, so 'the newest vintage' alone would not have identified the right one.)",
    "manifest_counts": {"node_count": 27206, "edge_count": 58589, "edges_skipped_missing_endpoint": 386},
    "triggers_served": 171,
    "triggers_derived_minus_served": "182 - 171 = 11, inside the 386 edges the projection dropped for a missing endpoint. NOT a criterion of this order and NOT investigated further; recorded so the next seat does not read the two numbers as a contradiction.",
    "bd_targets": ["arn:aws:lambda:us-east-1:313476888478:function:bd-allocation-processor", "arn:aws:lambda:us-east-1:313476888478:function:bd-gold-trigger", "arn:aws:lambda:us-east-1:313476888478:function:bd-silver-merge"],
    "bd_targets_source_node": "arn:aws:s3:::opal-data-bd (all three)",
    "cross_plane_check": "served NOTIFIES=41 equals the derive log's NOTIFIES=41 -- two producers, one number"
  },

  "the_instrument_repair_disclosed": {
    "row": "NFRA_CLDGRPH-W1-S10",
    "what_was_broken": "triggers_query.sh built its SSM command with json.dumps(q).replace(\"'\", \"'\\\"'\\\"'\"); the '\\'' idiom is correct only inside a SINGLE-quoted shell word and json.dumps emits a DOUBLE-quoted one, so the server received `WHERE e.edge_type='\"TRIGGERS\"'` -- a valid, unmatchable predicate",
    "the_reading_it_produced": "{\"rows\":[{\"triggers\":0}]} at the correct vintage with no error, beside a shape control that passed because MATCH (n) RETURN count(n) carries no string literal",
    "same_vintage_before_and_after_the_repair": {"pre_repair": "\"triggers\":0", "post_repair": "\"triggers\":171"},
    "the_fix": "the cypher travels as base64, is decoded into a file on the gateway and posted with --data-binary; every query is echoed AS THE SERVER RECEIVED IT beside its answer. The queries are unchanged.",
    "scope_of_the_repair": "the two scripts this order names, both in this seat's own deliverables folder. The defect is a SHAPE and other carriers of it exist (.tools/comp-kuzu, c2c3_liveness_acceptance.py, the gateway's graph_cypher); widening is not this order's grant -- routed to 2.0.0_SA_COO~A in the row.",
    "why_it_is_stated_here_and_not_only_in_the_row": "D12-AC4 passes on a REPAIRED instrument. A criterion that passes because the seat fixed its own measuring device has to say so where the verdict is read, not only where the surprise is filed."
  },

  "the_34_buckets_the_grant_reaches": ["opal-313476888478-globgrph", "opal-313476888478-lambda-artifacts", "opal-313476888478-lambda-layers", "opal-313476888478-terraform-state", "opal-313476888478-yang-qa-scratch", "opal-cloudtrail-logs-313476888478", "opal-cur-313476888478", "opal-data-49financial", "opal-data-assets", "opal-data-astn", "opal-data-bd", "opal-data-cot", "opal-data-demo", "opal-data-etfs", "opal-data-imo", "opal-data-inf", "opal-data-mdpf", "opal-data-news-av", "opal-data-news-v2", "opal-data-pm", "opal-data-portal-v2", "opal-data-portfolio", "opal-data-security", "opal-data-security-access-logs", "opal-data-trade-submissions", "opal-estate-report", "opal-infrastructure-snapshots", "opal-mcp-athena-results", "opal-mcp-audit", "opal-runner-shared", "opal-security-evidence", "opal-served-key-write-trail-logs", "opal-website-backups", "opalinvest-portal"],

  "deploy_ledger": {
    "entry": "org/critical_paths/change_management/20260904T1232Z_cldgrph-cgs16-derive-role-bucket-notification_deploy_completion.md",
    "slug": "cldgrph-cgs16-derive-role-bucket-notification",
    "opened": "12:32:00Z, BEFORE the apply, with the complete 5-leg manifest, the principal named and the 34 buckets enumerated",
    "state": "CLOSED, 5 of 5 legs proven; sentinel org/critical_paths/.open_deploys/cldgrph-cgs16-derive-role-bucket-notification.json removed by the tool at close"
  },

  "bounds_honoured": {
    "one_action_one_statement_one_role": true,
    "no_s3_star_no_managed_policy_no_other_principal_no_bucket_policy": true,
    "one_ad_hoc_derive": true,
    "no_pins_no_serving_restart": "correct -- the pins are TO-CG-D-1's, after this order; no force-new-deployment, no stop-task",
    "no_marker_no_pointer_no_projection_object_written": "the derive and the projection worker wrote their own; this seat wrote none",
    "no_s3_delete_no_firm_bucket_touched_no_alarm_no_monitor": true,
    "reads_only_outside_the_grant": "item2a.tf, the CG-s-15 record, the derive logs and the projection manifest were READ, never written"
  },

  "surprise_rows_filed": [
    "NFRA_CLDGRPH-W1-S9 OBSERVATION/ARMED -- the AccountWideReadOnly statement is in item2a.tf, which this order does not grant; the grant landed at its own address in iam.tf and the role's account-wide S3 reads now have two carriers",
    "NFRA_CLDGRPH-W1-S10 OBSERVATION/ARMED -- the served-graph instrument returned a FALSE ZERO for every WHERE-filtered cypher; repaired in the two scripts this order names, still armed in the others"
  ]
}
```

## What this run settles

**The grant is the answer S20 was missing, and it is now exercised, not merely applied.** The same
image that printed `buckets read=0 / buckets unreadable=34` this morning printed
`buckets read=34 / buckets unreadable=0` this afternoon, and the only thing that changed between the
two runs is one IAM action on one role. The derive's own edge summary went from no TRIGGERS at all
to `TRIGGERS=182`, and the served projection -- built from this derive's snapshot ids, not from
whatever was newest -- answers 171 with bd-allocation-processor, bd-gold-trigger and bd-silver-merge
all present and all sourced from `arn:aws:s3:::opal-data-bd`. S20 and S28 have their proof; the
disarm itself is the L9 seat's, not this one's.

**The halt gate's repair is exercised too.** W1-S1 recorded that no spine-v3 worker could run any
`terraform apply`; `safe-apply` today named this seat's issuer and let the apply through. That
blocker is measured gone, on the live gate, by an apply that actually landed.

## What it does not settle, and the reason is measured

**The grant sits at a different terraform address than the estate's record describes** (W1-S9). Two
carriers of one role's account-wide S3 reads is a reading hazard, not a security one: IAM sees the
union and no consumer can tell. The disarm is one apply by the module's IAM lane, and until it runs,
a least-privilege audit that reads `AccountWideReadOnly` alone under-reports this role by one action.

**The false-zero instrument is repaired in two files and armed everywhere else** (W1-S10). This is
the finding that outranks the grant for the fabric, because it nearly inverted this order's verdict:
the world was repaired at 12:57Z and the instrument went on reporting the pre-repair answer at 13:12Z,
with a correct vintage, a passing shape control and no error. The shape control shared the transport
but not the hazard -- it carries no string literal -- so it certified reachability and nothing else.
A control has to exercise the failure mode of the thing it stands behind, and the honest form of that
is what both scripts now do: echo the query AS THE SERVER RECEIVED IT beside its answer, so the bytes
that were evaluated can never again be inferred from the bytes that were intended.

**One number is deliberately not chased.** 182 edges derived, 171 served, 11 inside the projection's
386 `edges_skipped_missing_endpoint`. It is recorded so the next seat does not read it as a
contradiction, and it is not this order's cell.
