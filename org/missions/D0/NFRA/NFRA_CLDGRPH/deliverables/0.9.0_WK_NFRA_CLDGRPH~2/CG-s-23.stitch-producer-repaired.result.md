# CG-s-23 -- THE CLOUD STITCH PRODUCER IS REPAIRED AND PRODUCING

**TO:** `NFRA_CLDGRPH.TO-CG-F-3` · **cell:** CG-s-23 (decomp v0.6 @`c6b16d8f04`) · **PRD:** v0.6 row S23
@`50f0e219ba` · **worker:** `0.9.0_WK_NFRA_CLDGRPH~2`, branch `wk-cldgrph-6-2`, worktree
`C:/tmp/wk-cldgrph-6-2` · **push state:** LOCAL, never pushed, never merged, never rebased.

```json
{
  "cell": "CG-s-23",
  "to_id": "NFRA_CLDGRPH.TO-CG-F-3",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~2",
  "branch": "wk-cldgrph-6-2",
  "push_state": "LOCAL",

  "step_1_reproduction_on_the_snapshot_as_pulled": {
    "object": "s3://opal-313476888478-globgrph/stitch-source/source.zip",
    "pulled_at_utc": "2026-09-09T18:2xZ (before the re-push at 18:47:04Z)",
    "last_modified": "Tue, 07 Jul 2026 13:46:19 GMT",
    "content_length": 156995002,
    "etag": "\"5e8011947ede9e0e253dc3a64d36d479-19\"",
    "zip_entries": 7905,
    "portal_src_files": 0,
    "zip_stitch_source_sha": "81064fbcae6dbf440d516eee067554f6a192becd",
    "cloud_log_read": "opal-stitch-produce:3a5b2473-f46a-490a-ae5e-874a96c90b16, 72 events, 2026-09-09T03:00:17Z..03:01:07Z, initiator rule/opal-stitch-produce-nightly",
    "cloud_log_verdict": "exit status 2 / COMMAND_EXECUTION_ERROR, last derive line 'ERROR: GRAIN_SENTINEL_FAIL -- refusing to emit grain-violating stitch graph'",
    "local_run_of_the_snapshot_bytes": "rc 2, same 8 AC-GRAIN.2 groups, same UNIONED 28918 nodes / 60834 edges",
    "ASIS_RC": 2,
    "ASIS_CAUSE": "GRAIN_SENTINEL",
    "ASIS_PORTAL_SRC_FILES": 0
  },

  "the_cause_in_two_layers": {
    "layer_1_the_zip": "the July zip packs 0 portal/src files AND carries the PRE-2026-07-25 grain_baseline.json (1 recertification block; HEAD carries 8). 3 of the 8 violation groups are the missing portal layer, 5 are the stale baseline.",
    "layer_2_the_code": "a HEAD-built zip clears the sentinel and then returns 1 on 5 phantom dangling edges -- 2 that the AWS layer's producer already marked wildcard=True and whose flag derive_stitch's _wild() discarded, 3 EventBridge TRIGGERS onto AWS-PUBLIC accountless SSM documents that comp_aws_cli excludes by an Owner=Self filter. CodeBuild fails on any non-zero exit, so the re-push alone would have moved a 67-build exit-2 streak to an exit-1 streak.",
    "row": "NFRA_CLDGRPH-W2-S43"
  },

  "the_fix": {
    "commit": "de590a7d0227fb9c14ce35b96dcec86deb68df60",
    "file": "infra/aws/globgrph/derive_stitch.py",
    "shape": "+20 / -1: the dangling filter honours the edge's own `wildcard` flag, and a new _aws_public_ssm() exempts accountless ssm ARNs. NARROWED to service 'ssm' so an accountless S3 ARN stays a genuine finding.",
    "commit_gate": "bash .tools/commit-gate.sh infra/aws/globgrph/derive_stitch.py -> rc 0, 'pre-commit gate clean for 1 of 1 file(s)'",
    "paired_control": "same tree, same inputs: rc 1 / dangling 5 -> rc 0 / dangling 0, with UNIONED 29267 nodes / 61275 edges UNCHANGED",
    "terraform_changed": false
  },

  "step_3_the_re_push": {
    "route": "SECOND (local build + aws s3 cp). The FIRST route, .github/workflows/stitch-source-push.yml, fires only on a push to CLOUD -- 0.0.0_AB_MSTR's act -- and its portal checkout needs secrets.PORTAL_REPO_PAT.",
    "ledger_entry": "org/critical_paths/change_management/20260909T184608Z_stitch-source-repush_deploy_completion.md",
    "ledger_opened_utc": "2026-09-09T18:46:08Z",
    "ledger_closed_utc": "2026-09-09T18:47:30Z",
    "ledger_status": "CLOSED",
    "task_families_touched": "NONE -- a CodeBuild source zip; no image, no tag, no task definition",
    "head_object_after": {
      "last_modified_utc": "2026-09-09T18:47:04Z",
      "content_length": 181338655,
      "etag": "\"b20d2d25b4a0851881d55e19af575367-22\""
    },
    "zip_entries": 8224,
    "portal_src_files": 435,
    "portal_checkout_head": "18c0c5cb6a26c2c8e9fbfa168dadf04de4344705",
    "stitch_source_sha_txt": "de590a7d0227fb9c14ce35b96dcec86deb68df60",
    "local_sha256": "06413e9a1ae5b46dde8f745bc9804a8c19243832dd0e4ac00212510e719ab913",
    "s3_objects_written_by_this_seat": 1
  },

  "step_4_the_ad_hoc_build": {
    "build_id": "opal-stitch-produce:daaedf78-3ea7-4dd4-828b-be1c843f5d4c",
    "status": "SUCCEEDED",
    "initiator": "Andrew_Berman",
    "started_utc": "2026-09-09T18:48:15Z",
    "ended_utc": "2026-09-09T18:49:37Z",
    "phases": "SUBMITTED, QUEUED, PROVISIONING, DOWNLOAD_SOURCE, INSTALL, PRE_BUILD, BUILD, POST_BUILD, UPLOAD_ARTIFACTS, FINALIZING -- all SUCCEEDED",
    "log_lines": 92,
    "derive_lines": "UNIONED nodes = 29267, edges = 61275 / 'OK: genuine (non-wildcard) dangling edges = 0' / 'GRAIN-SENTINEL: PASS (0 identity-format + 0 magnitude violations)' / 'OK: stitch published (artifact-first, marker-last)'",
    "marker": {
      "built_at": "2026-09-09T18:49:23Z",
      "aws_snapshot": "snapshots/20260909/graph-20260909.tar.gz",
      "git_sha": "de590a7d0227fb9c14ce35b96dcec86deb68df60",
      "producer": "stitch-codebuild",
      "total_nodes": 29267,
      "total_edges": 61275,
      "artifact_sha256": "a7c1d5898bac1d8c8dc771f9dd63ea747d7d4248ae2408130b0e8b9a9cf1c6cc"
    },
    "artifact": {
      "key": "stitch/stitch_graph.json",
      "bytes": 38845013,
      "last_modified_utc": "2026-09-09T18:49:36Z",
      "sha256_measured_from_s3": "a7c1d5898bac1d8c8dc771f9dd63ea747d7d4248ae2408130b0e8b9a9cf1c6cc",
      "matches_marker": true
    },
    "marker_read_pinned_utc": "2026-09-09T18:52:13Z..18:52:20Z",
    "marker_read_confirmed_utc": "2026-09-09T19:00:59Z (still producer=stitch-codebuild)"
  },

  "step_5_the_no_run_discrimination": {
    "reader": "org/missions/D0/NFRA/NFRA_CLDGRPH/deliverables/0.9.0_WK_NFRA_CLDGRPH~2/f3_marker_verdict.py",
    "age_bar_hours": 26.0,
    "age_bar_source": "IMPORTED from infra/aws/globgrph/_provenance.py:41 DEFAULT_AGE_WARN_HOURS, never re-typed",
    "live": "FRESH",
    "planted_80h": "STALE",
    "missing_key": "NO-RUN (a real NoSuchKey from the same bucket and client)",
    "distinct_verdicts": "3 of 3",
    "rule_disabled": false
  },

  "the_nightly_to_read_tomorrow": {
    "criterion": "F3-AC6 (judgment; graded by 3.0.0_SA_CVO at L9)",
    "expected_fire_utc": "2026-09-10T03:00Z +/- 15 min",
    "rule": "opal-stitch-produce-nightly, cron(0 3 * * ? *), State ENABLED (describe-rule, this seat, 2026-09-09T18:2xZ)",
    "read": "aws codebuild list-builds-for-project --project-name opal-stitch-produce, then batch-get-builds on the build whose initiator is rule/opal-stitch-produce-nightly and whose startTime is 2026-09-10T03:00Z +/- 15 min; then s3api get-object stitch/stitch_marker.json"
  },

  "surprise_rows_filed": [
    "NFRA_CLDGRPH-W2-S40", "NFRA_CLDGRPH-W2-S41", "NFRA_CLDGRPH-W2-S42",
    "NFRA_CLDGRPH-W2-S43", "NFRA_CLDGRPH-W2-S44"
  ],
  "commits": [
    "de590a7d02 -- the derive_stitch repair (before the re-push, so the zip's stitch_source_sha.txt names bytes that exist)",
    "<the acts commit>",
    "<the instance + status flip commit>"
  ]
}
```

---

## What was broken, in the order it had to be taken apart

The producer had **two** failures stacked, and only the first was visible.

**The first is the one the PRD names.** `opal-stitch-produce` reads a source zip that was written
once, on 2026-07-07, by a GitHub Action whose portal checkout needs a secret. That zip packs **0
files from `portal/src`** -- the Action's own comment at
`.github/workflows/stitch-source-push.yml:53-61` records exactly this class and even the numbers
(`REACT_QUERY_KEY 0/32, PORTAL_COMPONENT 0/27`). It also carries the **pre-2026-07-25**
`grain_baseline.json`. So the grain sentinel refuses on eight groups: three because the portal layer
is absent, five because the baseline inside the zip predates the CTO-gated recalibration that moved
SQS_QUEUE 4 -> 12, ECS_TASK_DEFINITION 2 -> 7, SCHEDULE 3 -> 10, IAM_USER 1 -> 4 and
EXTERNAL_ENDPOINT 3 -> 0. `derive_stitch.main()` returns 2 on that one branch, CodeBuild reports
`exit status 2`, and the marker is never written. Sixty-seven times.

That was reproduced **on the snapshot as pulled**, not on HEAD: the July object was fetched by
`s3api get-object` (ETag recorded), unzipped whole (7905 of 7905 entries, 0 errors), and **its own**
`derive_stitch.py` -- 255 lines, not HEAD's 267 -- was run from that tree. rc 2, the same eight
groups, the same `UNIONED nodes = 28918, edges = 60834` line the cloud printed. Two instruments on
two planes agreeing on every digit is what makes this a reproduction rather than a re-enactment.

**The second only appears once the first is gone.** A zip built from HEAD carries the portal layer
and the current baseline, so the sentinel passes -- and then `derive_stitch` returns **1**, because
its 0-dangling check counts five edges that are not findings:

* two `IN_SUBNET` edges from the gateway load balancer to subnets, which the AWS layer's own
  producer emits **carrying `wildcard=True`** (`org/modules/graph/comp_aws_cli.py:1890`). The flag
  was discarded: `_wild()` inspects only the endpoint *string* and never reads the edge's own field.
  There is no subnet node class in the snapshot at all.
* three `TRIGGERS` edges onto **AWS-public** SSM documents -- `arn:aws:ssm:us-east-1::document/
  AWS-RunPowerShellScript` and `::automation-definition/AWS-StartEC2Instance`. The empty account
  field is what AWS-owned means, and `comp_aws_cli.live_ssm_documents` (`:1092-1094`) derives
  SSM_DOCUMENT nodes **"Self-owned only (exclude AWS-public docs)"** through an explicit
  `Owner=Self` filter. Those edges terminate outside the modelled estate *by design*, which is the
  same structural situation `_known_transient` already covers for the pre-WAVE-4 ECS case.

CodeBuild fails a phase on any non-zero exit, so the re-push on its own would have converted a
67-build exit-2 streak into an exit-1 streak and nobody would have been better off.

**This is a guard being repaired, not relaxed**, and the distinction is the whole of it. The
`wildcard` limb honours a flag the *producer* sets; it does not invent one. `_aws_public_ssm` is
narrowed to service `ssm` on purpose -- an accountless S3 ARN (`arn:aws:s3:::bucket`) is a modelled
node class, so a dangling S3 endpoint stays a genuine finding. `derive_stitch`'s own docstring
already claims this check *is* comp-aws's ("a wildcard-exempt 0-dangling check (AC5 == comp-aws
0-dangling, CTO ruling)"); the commit makes the claim true. And the paired run is the control: same
tree, same inputs, `UNIONED nodes = 29267, edges = 61275` **identical** before and after, with only
the dangling count moving 5 -> 0. A change that moved anything else would have shown there.

## The re-push, and what it cost

One S3 object, under a NEVER-2 ledger entry opened before the `cp` and closed after it with the
served object's own `head-object` reading. The entry states the task-family answer rather than
omitting it: **none** -- this is a CodeBuild source zip, no image is built, no tag moves, no task
definition pulls it. The July bytes are retained locally as the rollback material and the entry says
where.

The zip was built with the Action's own recipe (`portal/src`, `org/modules`, `infra/aws`, `.tools`,
`stitch_source_sha.txt`, every `data/*/scripts/**/*.py`, the same four exclusions). `portal/` is a
bare gitlink here, so `portal/src` came from the main workspace's portal checkout by absolute path.
**That checkout is not at the gitlink**, and the gitlink object is not even present in it -- three
different portal shas name this layer and no two agree. Row `NFRA_CLDGRPH-W2-S40`.

## The ad-hoc build, and the read that is perishable

One build, `daaedf78`, initiator `Andrew_Berman` (not `rule/`), SUCCEEDED in 82 seconds. Its log
carries the three lines that matter: `OK: genuine (non-wildcard) dangling edges = 0`,
`GRAIN-SENTINEL: PASS`, `OK: stitch published (artifact-first, marker-last)`. The marker it wrote
carries `producer: stitch-codebuild` and `git_sha de590a7d02` -- this worker's own commit -- and the
artifact's sha256, read back **from S3**, equals the marker's `artifact_sha256`. Its node and edge
counts, 29267 / 61275, are the same numbers this seat measured locally before the push, which is the
cross-plane agreement that says the cloud ran the bytes that were sent.

**The marker read is perishable and the record says so.** `.git/hooks/post-commit` runs
`.tools/git-hooks/stitch-refresh-post-commit.sh`, which republishes both stitch keys with
`producer=stitch-local` within about a minute of any commit -- at this laptop *or* at site Z --
touching `portal/`, `data/*/scripts/`, `org/modules/graph/` or the two derive scripts. The order's
own `<paths>` grant names both derive scripts, so **this worker's fix commit fired that publisher
inside its own worktree**, two minutes before the CodeBuild. It wrote nothing only because it was
refused: `portal/` is empty in a linked worktree, so the derive read zero portal files and the grain
sentinel refused to publish (`/tmp/stitch-refresh.log`, captured at `f3_hook_refusal_tail.txt`). That
same log is an independent second instrument on the fix: the run under the hook printed
`OK: genuine (non-wildcard) dangling edges = 0` where the block immediately above it, on the same
tree with the same union counts, printed `ERROR: ... = 5`. Row `NFRA_CLDGRPH-W2-S44`. **The hook is
not touched by this order** -- it carries an Andrew-direct of 2026-07-07 and its reconciliation
belongs to `1.0.0_SA_CTO`.

Because of that, `f3_marker_cloud.sh` always prints two readings: the pinned one taken at
18:52:13Z..18:52:20Z, three minutes after the build wrote the marker, and a live one taken on every
run. At 19:00:59Z they were still identical.

## A control that turned out not to be one

`F3-AC4` offers the marker's `git_sha` membership as the discriminator between a cloud marker and a
laptop one, on the premise -- also carried by row `NFRA_CLDGRPH-S70` -- that the 17:53Z laptop
marker's `9b99b4934217c54aea516591a65e1009a5f9bdf6` is not an object in this repository. At this
worktree's vintage it **is**: a commit of `1.0.0_SA_CTO~Z`'s, contained in `CLOUD`, made 57 seconds
before that marker was written. So the laptop publisher is the hook on this estate, not a foreign
clone, and `MARKER_SHA_IN_THIS_REPO` reads `true` for both arms. The limb is reported as a provenance
fact; **`producer` is the only field that discriminates**, and it does. The script prints both
controls, plus a live positive/negative pair on the oracle itself (HEAD resolves, forty zeros do
not), so the `true` is not a constant. Row `NFRA_CLDGRPH-W2-S42`.

## What would make tomorrow's read fail

`F3-AC6` is graded by `3.0.0_SA_CVO` the morning after, and the worker's half was to leave the
producer in a state where that read *can* be SUCCEEDED. It is: the rule is ENABLED and unchanged, the
source at the key is the HEAD-built zip, and the same bytes have already produced a SUCCEEDED build
once. Three things would break it, and they are named rather than left implicit:

1. **The marker gets overwritten by the hook.** Any commit at this laptop or at site Z touching the
   four trigger paths republishes with `producer=stitch-local`. Site Z's publishes pass the sentinel
   (its portal tree is populated), so site Z can and does write. The 03:00Z build would still be
   SUCCEEDED, but the marker read at 03:0xZ could show `stitch-local` with a later `built_at`.
   The discriminator is `producer`, and the grader should read the build's own log tail beside it.
2. **Source drift.** The zip at the key is a point-in-time copy. If the GH Action fires on a CLOUD
   push before 03:00Z it will overwrite `source.zip` with a build whose `portal/src` may again be
   empty (the PAT is still unread by this seat) -- and the exit 2 returns.
3. **A new AWS-side band break.** The sentinel compares live counts against `grain_baseline.json`.
   The baseline is a dated artifact; an estate change between now and 03:00Z that moves a covered
   class past 2.5x re-arms the same refusal. Nothing here weakens that guard, which is the point.
