# CG-s-24 -- THE PROJECTION CARRIES THE STITCH SOURCE

**TO:** `NFRA_CLDGRPH.TO-CG-F-4` · **cell:** CG-s-24 · **worker:** `0.9.0_WK_NFRA_CLDGRPH~2`,
branch `wk-cldgrph-6-2` · **push state: LOCAL.**
The served graph answers `GOLD_SCRIPT=1380` where it answered 0, and its VINTAGE line names the
stitch that put it there.

```json
{
  "cell": "CG-s-24",
  "to_id": "NFRA_CLDGRPH.TO-CG-F-4",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~2",
  "branch": "wk-cldgrph-6-2",
  "push_state": "LOCAL",

  "the_gate_this_order_waited_for": {
    "row": "NFRA_CLDGRPH-W2-S45",
    "cto_go": "20260909T2015Z (PRD v0.10 @4fc1bcb3e4 merged @04d9942aff; rule R17)",
    "cvo_re_sign": "C-S40 @e7db04572e",
    "entries_added": {"GOLD_SCRIPT": "pipeline", "REACT_QUERY_KEY": "portal",
                      "PORTAL_COMPONENT": "portal", "PORTAL_BUNDLE": "portal",
                      "S3_DATA_KEY": "aws"},
    "node_type_layer_keys": 65,
    "node_type_layer_by_layer": {"aws": 34, "portal": 18, "pipeline": 4, "ms": 7, "semctl": 2},
    "cvo_census_agrees": "C-S40: 60 -> 65 keys; aws 33 -> 34; portal 15 -> 18; pipeline 3 -> 4; COND-A resource-type count 32 UNMOVED. Every number checked against the map committed here, not asserted.",
    "go_line_provenance": "extracted programmatically from the CTO record's own backtick block (4 physical lines), never retyped -- row W2-S50 records that the face's inline quotation differs from it"
  },

  "the_fold": {
    "function": "derive_runner.fold_stitch_document (pure) + ingest_stitch_artifact (S3)",
    "guards": ["sha256 vs the marker", "NODE_TYPE_LAYER membership", "both-ends edge resolution"],
    "stamp": "every node admitted under one of the five carries vocabulary=stitch-v1",
    "fixture": "F4_TESTS=21 passed of 21, 11 named arms, 4 of them controls"
  },

  "the_image_act": {
    "ledger": "org/critical_paths/change_management/20260909T203713Z_cldgrph-cgs24-stitch-fold-image-and-sevenfamily-repin_deploy_completion.md",
    "ledger_opened_utc": "2026-09-09T20:37:13Z",
    "ledger_closed_utc": "2026-09-09T20:58:00Z",
    "ledger_families_named": 7,
    "codebuild": "globgrph-derive-build:f8abbe55-c611-4317-8df7-2edf15908de3 SUCCEEDED",
    "source_commit": "27e4ac36de776c8da06df4179b8343f62c63392b",
    "digest_before": "sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778",
    "digest_after": "sha256:478d0a43742b2ed5a44631c6352b5713c5ba22f015d82a673cfb93428a9dae20",
    "image_pushed_at": "2026-09-09T20:39:50Z",
    "ecr_tags": ["20260909-203936", "latest"],
    "latest_moved": true,
    "families_pulling_latest": "0 of 7 -- all seven are pinned BY DIGEST, which is why the tag move is safe"
  },

  "the_seven_families": {
    "globgrph-derive-runner": {"revision_before": 7, "revision_after": 8},
    "globgrph-projection-worker": {"revision_before": 4, "revision_after": 5},
    "globgrph-serving": {"revision_before": 2, "revision_after": 3},
    "globgrph-comp-learns-producer": {"revision_before": 2, "revision_after": 3},
    "globgrph-cse-producer": {"revision_before": 2, "revision_after": 3},
    "globgrph-fedobs-producer": {"revision_before": 2, "revision_after": 3},
    "globgrph-resource-summaries-producer": {"revision_before": 2, "revision_after": 3},
    "on_new_digest": "7 of 7", "on_latest": "0 of 7",
    "name_note": "the TRUE ACTIVE names; the order's cut named four of them without the globgrph- prefix and those four do not resolve (row W2-S49)"
  },

  "the_apply": {
    "binary": ".tools/terraform.exe (91,104,424 B), never the PATH terraform",
    "addresses": 18,
    "addresses_note": "censused from a plan, not carried over; the order's 'ten' was E-2's, for a four-family act (row W2-S52)",
    "unscoped_plan_pre": "Plan: 9 to add, 13 to change, 7 to destroy.  (22 addresses; NEVER applied)",
    "foreign_left_as_found": ["aws_glue_partition.tool_activity[\"rolling_log\"]",
                              "aws_glue_partition.tool_activity[\"rolling_log_summary\"]",
                              "aws_glue_partition.tool_activity[\"routing\"]",
                              "aws_sns_topic_subscription.critical_surface_alerts_email"],
    "targeted_plan_pre": "Plan: 7 to add, 11 to change, 7 to destroy.  (18 addresses, 0 foreign)",
    "apply": "Apply complete! Resources: 7 added, 11 changed, 7 destroyed.  rc 0",
    "targeted_plan_post": "No changes. Your infrastructure matches the configuration.",
    "halt_gate": "blocked the first attempt on IDENTITY UNRESOLVED; satisfied as it instructs by naming this worker in the gitignored org/mcp/sessions/<session>.serial, never overridden (row W2-S53)"
  },

  "the_derive": {
    "task": "arn:aws:ecs:us-east-1:313476888478:task/opal-globgrph/deee298ca1bd422fa3fcc124cf42a86f",
    "task_definition": "globgrph-derive-runner:8",
    "image_is_the_new_digest": true,
    "started_utc": "2026-09-09T20:51:45Z",
    "last_status": "STOPPED", "exit_code": 0,
    "stitch_ingest_line": "INFO: STITCH_INGEST nodes=1844 edges=723 skipped_dup=27423 stamped=1771 skipped_unmapped_type=0 skipped_edge_unresolved=2694 producer=stitch-codebuild vintage=2026-09-09T19:55:00Z",
    "stitch_producer_at_fold": "stitch-codebuild",
    "stitch_ingest_fail_lines": 0,
    "relabel": "OK: NODE_TYPE_LAYER relabel applied -- 63 node_types all mapped (aws/portal/ms partition clean)",
    "node_type_layer_gap_lines": 0,
    "stitch_unmapped_type_lines": 0,
    "control": "the two previous derives in the same log group carry 0 STITCH_INGEST lines -- an image without the fold cannot print it"
  },

  "the_projection": {
    "worker_task_definition": "globgrph-projection-worker:5 (the new revision), started by EventBridge Pipes 21:05:19Z",
    "pointer_before": "projection/2026-09-09T20:04:09.034708+00:00/",
    "pointer_after": "projection/2026-09-09T21:05:17.968166+00:00/",
    "manifest_sha256": "09be45b5ff92acc4c05e83357877020f710ce8d57e7eef5a83f27876ea4d9504",
    "pointer_advanced": true
  },

  "the_served_read": {
    "invocation": "bash .tools/comp-kuzu --json \"MATCH (n:CloudNode) WHERE n.node_type IN ['GOLD_SCRIPT','S3_DATA_KEY','API_ROUTE'] RETURN n.node_type AS t, count(*) AS c ORDER BY t\"",
    "served_stitch_types": "3 of 3 non-zero",
    "GOLD_SCRIPT": 1380, "S3_DATA_KEY": 294, "API_ROUTE": 151,
    "pre_fold_control": {"GOLD_SCRIPT": 0, "S3_DATA_KEY": 0, "API_ROUTE": 86,
                         "served_stitch_types": "1 of 3 -- NOT the 0 of 3 the criterion states (row W2-S47)"},
    "stitch_v1_stamped": 1771,
    "stitch_v1_query": "n.props CONTAINS 'stitch-v1' -- `vocabulary` is not a CloudNode column and the column form is a Binder exception, not a zero (row W2-S51)",
    "vintage_line": "VINTAGE: Built from the estate as of 2026-09-09 21:05:17 UTC. Stitch source: stitch-codebuild built 2026-09-09T19:55:00Z.  [vintage=2026-09-09T21:05:17.968166+00:00 manifest=09be45b5ff92 prefix=projection/2026-09-09T21:05:17.968166+00:00/]",
    "vintage_has_stitch": true,
    "stitch_built_at": "2026-09-09T19:55:00Z"
  },

  "cross_plane_agreements": [
    "the derive's own log says stamped=1771 and the served graph answers 1771 for the stamp -- two planes, one number",
    "the CVO's C-S40 census counted the five types at 1,791 nodes in the artifact; 1,791 - 1,771 = 20 = C-S40's own 'PORTAL_COMPONENT 20 of 22 ids identical to Component', which the fold's co-key skips as duplicates",
    "the map committed here reads 65 keys with aws 34 / portal 18 / pipeline 4 / ms 7 / semctl 2 -- every figure in C-S40"
  ],

  "surprise_rows_filed": ["NFRA_CLDGRPH-W2-S45", "NFRA_CLDGRPH-W2-S46", "NFRA_CLDGRPH-W2-S47",
                          "NFRA_CLDGRPH-W2-S48", "NFRA_CLDGRPH-W2-S49", "NFRA_CLDGRPH-W2-S50",
                          "NFRA_CLDGRPH-W2-S51", "NFRA_CLDGRPH-W2-S52", "NFRA_CLDGRPH-W2-S53",
                          "NFRA_CLDGRPH-W2-S54"],
  "commits": ["5d3c589f25 the fold + carrier (pre-gate)", "9c98dd1e63 the OPEN instance (pre-gate)",
              "27e4ac36de the gate taken: +5 NODE_TYPE_LAYER entries + the stamp",
              "<the acts commit>", "<the instance + flip commit>"]
}
```

---

## What the graph does now that it did not do this morning

Ask the served graph for a gold script and it answers. `GOLD_SCRIPT=1380`, `S3_DATA_KEY=294`,
`API_ROUTE` up from 86 to 151 -- and the line the client prints under the answer says where the
second half came from:

    VINTAGE: Built from the estate as of 2026-09-09 21:05:17 UTC. Stitch source: stitch-codebuild
    built 2026-09-09T19:55:00Z.  [vintage=2026-09-09T21:05:17.968166+00:00 manifest=09be45b5ff92 ...]

Two sources, two vintages, one line, one graph. That is the JOIN.

## The block, and what unblocked it

This order was reported OPEN four hours ago on `W2-S45`: four of the five node types the accept
names were absent from `NODE_TYPE_LAYER`, and folding them would have made
`relabel_layers_by_node_type` fail the nightly derive **closed**. The map is a CVO-signed frozen
taxonomy under a CTO arch-gate, and this seat had neither.

The CTO ruled (**GO 20260909T2015Z**, PRD v0.10 R17) and the CVO re-signed (**C-S40 @`e7db04572e`**).
Five additive, **labelled-interim** entries; every node admitted under one of them stamped
`vocabulary=stitch-v1`; four of the five retire under S31 when the vocabulary is unified at the
producer. The map's comment carries the GO line copied out of the CTO record programmatically --
which is how row `W2-S50` got written, because the face's inline quotation of that line and the
record's own text differ by a clause and only the file's bytes are the ruling.

**The count was checked, not assumed.** The committed map reads **65 keys**, `aws` 34, `portal` 18,
`pipeline` 4, `ms` 7, `semctl` 2 -- every figure in C-S40, and the COND-A *resource*-type count
unmoved at 32 because `S3_DATA_KEY` joins the `aws` **layer** at object grain exactly as `S3Key`
already does. The fixture asserts `len(NODE_TYPE_LAYER) == 65` on every run, so the next edit that
moves the count fails a test instead of drifting.

**The guard stayed and still bites.** With the five now mapped, the fixture's unmapped-type arm
would have tested nothing, so it plants `SOME_FUTURE_TYPE` instead -- the case the guard actually
exists for. In the cloud the same guard printed `NODE_TYPE_LAYER relabel applied -- 63 node_types
all mapped` and zero `STITCH_UNMAPPED_TYPE` lines.

## The numbers that agree across planes

Three independent readings landed on the same figure, which is what makes 1,771 a measurement:

* the derive's own log: `stamped=1771`
* the served graph: `n.props CONTAINS 'stitch-v1'` -> **1771**
* the CVO's C-S40 census of the artifact: the five types are **1,791** nodes -- and 1,791 - 1,771 =
  **20**, which is precisely C-S40's own "PORTAL_COMPONENT 20 of 22 ids identical to `Component`".
  Those 20 are the duplicates the fold's co-key skips. The two censuses do not merely resemble each
  other; they reconcile exactly, by a number neither of them was fitted to.

The fold took 1,844 nodes and 723 edges and skipped 27,423 duplicates -- the AWS layer the derive
already had. It is additive, not a second copy.

## The image act

One build, one push, one targeted apply, all inside a NEVER-2 entry that names all seven families
by their **true** names and states the four the cut got wrong. The `:latest` tag moved with the push
and **nothing pulls it** -- 0 of 7 families reference a tag, which is R13 working.

**The apply set is eighteen, not ten.** The order carried E-2's ten over; that ten was correct for
an act moving four families. This one moves seven, because all seven read
`local.globgrph_image_digest`. The set was read off a plan rather than copied: an unscoped plan
(never applied) censused 22 addresses -- the 18 plus four foreign, one of them
`aws_sns_topic_subscription.critical_surface_alerts_email`, an alert destination the C3 moratorium
forbids this order to land. An unscoped apply would have created a notifier nobody asked for. Row
`W2-S52`.

`safe-apply` refused the first attempt outright: **IDENTITY UNRESOLVED**, because the halt-gate
resolves the acting principal from a `.serial` file that does not exist in a fresh linked worktree
and will not guess. Its remedy writes a path this order's `<paths>` does not name. It was taken as
the gate instructs -- this worker's own serial, into a gitignored runtime file that reaches no
record and could clobber no sibling, since the directory was absent -- and never overridden. Row
`W2-S53`, so the next order that applies Terraform can carry the grant or the provisioning.

## One false zero, caught by its own shape

The F4-AC4 reader printed `SERVED_STITCH_TYPES=0 of 3`, `GOLD_SCRIPT=0`, `(no VINTAGE line)` --
twice -- over a graph that answered 1,380 to the same query typed by hand seconds later. The cause
was a bare `bash` in a Python subprocess resolving to the WSL stub rather than the Git Bash running
the script. The tell was in the same output: `POINTER_ADVANCED=true`, read through boto3, stayed
correct while every shelled-out field went to zero. **A whole-output zero is a graph; a zero only in
the shelled-out fields is the shell.** Fixed by exporting the executing interpreter, which the
script now prints. Row `W2-S54`.

## What this does not claim

The fold carries the stitch's vintage; it does not make the stitch fresh -- that is the CodeBuild
nightly's job (CG-s-23) and F-3's `F4`-morning read. On a night the stitch producer fails and the
derive runs, the S3 objects are last night's and still verify against each other, so the fold
succeeds on a **stale** stitch and the served line shows a day-old `stitch_built_at` beside a fresh
Nessie vintage. That is correct and is the reason the vintage is carried rather than collapsed into
one number. If the marker is unreadable the carrier returns nothing and the line simply has no
stitch clause -- an absence, never a default.

Both clones' post-commit hook pairs are gone (this laptop 19:46Z, site Z 19:58Z, row S81), so the
cloud producer is the one writer of `stitch/`; the marker read at the fold was `stitch-codebuild`,
and the record says so because the fold **carries** the producer rather than refusing on it.
