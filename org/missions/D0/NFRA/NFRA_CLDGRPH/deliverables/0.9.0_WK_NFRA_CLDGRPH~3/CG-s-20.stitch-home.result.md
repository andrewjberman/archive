# CG-s-20 -- THE STITCH GRAPH'S HOME: **JOIN_PROJECTION**

**Cell:** CG-s-20 (decomposition v0.5) · **Task order:** `NFRA_CLDGRPH.TO-CG-E-4` · **Worker:** `0.9.0_WK_NFRA_CLDGRPH~3`
· **Worktree:** `C:/tmp/wk-cldgrph-5-3`, branch `wk-cldgrph-5-3`, HEAD `ab45a3337f` at the cut · **Recorded:** 2026-09-09 ~16:4xZ
· **Lane:** `0.8.0_AE_CloudComp` · **Reuses:** the closed-vocabulary and S53 claim shape of this seat's own CG-s-19 record.

**THE BOUND, first:** nothing was rebuilt, deleted or opened with an engine; no producer, Terraform, cloud engine or
thin client was touched; nothing was written to S3; and **no local rebuild path to the projection was created** --
measured at 0 of 3,216 ast nodes across the two edited files, beside a control that scores 9. The store's bytes and
mtime are unchanged (9,170,944 @ 2026-08-27 02:32 local, before and after every act).

---

## 1. THE FACTS (read-only)

### 1a. The store and its manifest

| | value |
|---|---|
| store | `C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_stitch_db` |
| bytes | 9,170,944 |
| Birth / Modify / Change | 2026-06-11 15:07:32 / **2026-08-27 02:32:00.480** / **2026-08-27 02:32:00.480** (local) |
| manifest | `kuzu_stitch_db._build_manifest.json`, Modify 2026-07-07 11:46:38 |
| manifest, before this order | `built_at 2026-07-07T15:46:38.578615+00:00`, `edge_count 5329`, `node_count 3414`, `schema_version 1`, `source_kind stitch`, `source_vintage.stitch_path C:\...\infra\aws\globgrph\stitch_graph.json`, `source_vintage.stitch_mtime 2026-07-07T15:45:33.789673+00:00` |
| builder | `infra/aws/globgrph/kuzu_stitch_load.py` (tracked), `edge_count=written` -- one increment per MERGE EXECUTED |
| git standing | gitignored (`infra/aws/globgrph/.gitignore:5`), so it exists ONLY in the main workspace |

**THE 51-DAY GAP, EXPLAINED (the order's question).** The store's `Modify` and `Change` are equal to the sub-second
at 2026-08-27 02:32:00.480 -- on NTFS that is a **content write**, not a metadata touch. The discriminator is in the
same directory: `kuzu_db`, `stitch_graph.json` and the stitch manifest all carry `Change 2026-08-25 02:16:36` within
8 ms of each other with `Modify` times months earlier -- a bulk metadata sweep, a visibly different shape. And it was
not a build: `kuzu_stitch_load.py` writes the manifest at the end of every build (`:150-160`), so a build would have
moved the manifest's `Modify`, which is still 2026-07-07. **So the store carries 51 days of mutation that no manifest
describes, and `node_count 3414` / `edge_count 5329` are claims about the July bytes.** The named capable mutator is
`kuzu_cost_enrich.py` -- deleted @`1266d65641`, docstring *"Add cost_mtd_usd attribute to CloudNode in kuzu_nessie_db
and kuzu_stitch_db"*, opening stores read-WRITE at `:127`/`:197` and naming the stitch store at `:229`. Capability
GROUNDED; identification INFERRED, and said so. Filed as **W3-S11**.

### 1b. The producer -- cloud-side, scheduled, and it has NEVER succeeded

| | value |
|---|---|
| TF resource | `infra/aws/terraform/globgrph/stitch-produce.tf:231` `aws_cloudwatch_event_target.stitch_produce_nightly` -> `aws_codebuild_project.stitch_produce` |
| schedule | `cron(0 3 * * ? *)`, rule `opal-stitch-produce-nightly`, live State **ENABLED**, 1 target |
| S3 landing | `s3://opal-313476888478-globgrph/stitch/stitch_graph.json` (+ `stitch/stitch_marker.json`, marker-last) |
| vintage NOW | artifact LastModified **2026-09-04T15:05:22Z**, 39,722,299 B; marker `built_at 2026-09-04T15:05:12Z`, `total_nodes 29219`, `total_edges 61628`, **`"producer": "stitch-local"`** |
| builds | `list-builds-for-project` -> **67 ids**; `batch-get-builds` over all 67 -> **FAILED 67, SUCCEEDED 0** |
| the failure | BUILD phase, ~30 s, `COMMAND_EXECUTION_ERROR`: *"Error while executing command: python3 infra/aws/globgrph/derive_stitch.py --out /tmp/stitch_graph.json. Reason: exit status 2"* |
| why it cannot self-heal | `stitch-source/source.zip` LastModified **2026-07-07** -- LEG-1 (the GH-Action) has not re-pushed since bootstrap, so the nightly runs a 64-day-old source against a moving repo |

The chain is APPLIED and FIRING and has produced nothing. What is in S3 was made by a **local** run and uploaded.
Filed as **W3-S10**.

### 1c. Does the served projection carry the stitch types?

**Not today; and the consumer would need no change if it did.** `projection_worker.py:44` `ARTIFACT_NAME =
"kuzu_nessie_db"` -- the served artifact is the Nessie/Iceberg projection, built by the incremental engine or the full
loader and published with its manifest. It carries the AWS-resource types (`REACH_NESSIE_TYPES`), not `GOLD_SCRIPT` or
`S3_DATA_KEY`. But `comp_debt.py` runs **one** Cypher constant, `_ISOLATED_SWEEP` (`:47-50`), against BOTH surfaces
(`:210-217`), selecting on `n.node_type` and returning `n.node_id` -- both columns exist in the stitch schema
(`kuzu_stitch_load.py:74-80`) and in the served one. So a JOIN is an ADDITIVE SOURCE into the projection build, not a
schema change and not a consumer change: the day the served graph carries the stitch types, `dispatch_reachability`
becomes two client queries and the last local Kuzu open in a user-facing tool disappears.

### 1d. The consumer's three sites

| line | site | text (before this order) |
|---|---|---|
| `comp_debt.py:40` | `STITCH_DB = os.path.join(_HERE, "kuzu_stitch_db")` | the 2nd REACHABILITY surface (gold/S3_DATA_KEY) |
| `comp_debt.py:133-134` | absent-store refusal | `REFUSE: kuzu_stitch_db not found at %s -- the REACHABILITY stitch surface.` |
| `comp_debt.py:143-148` | stale refusal, age from **`os.path.getmtime(STITCH_DB)`** | `REFUSE: kuzu_stitch_db is STALE (age %.0fh > %.0fh; built_at=%s) ... Re-run derive_stitch or pass --allow-stale.` |
| `comp_debt.py:215` (now `:230`) | the open | `conn = kuzu.Connection(kuzu.Database(path, read_only=True))` -- the LAST local Kuzu open in a tool a user works with |

The nessie leg was repointed at D-7 pass 1: `freshness_assert` (`:71-93`) reads `projection_client.health()` and
REFUSES if the served graph is unreachable, with *"There is no local database to fall back to"*.

## 2. THE DECISION

```json
{
  "cell": "CG-s-20",
  "task_order": "NFRA_CLDGRPH.TO-CG-E-4",
  "recorded_by": "0.9.0_WK_NFRA_CLDGRPH~3",
  "recorded_at": "2026-09-09T16:45Z",
  "vintage": "ab45a3337f",
  "home_vocabulary": ["JOIN_PROJECTION", "LOCAL_SCRATCH_DECLARED"],
  "home": "JOIN_PROJECTION",
  "owner": "0.8.0_AE_CloudComp",
  "reason": "The stitch graph is ALREADY a cloud artifact by design and by declaration -- produced by a scheduled CodeBuild from an S3 source and landing at s3://opal-313476888478-globgrph/stitch/stitch_graph.json -- and the only local step left is the Kuzu COMPILE of it, which is exactly the shape CG-s-8 retired for the canonical graph and exactly what this PRD's arc forbids: no machine is in the compile business. Three measured facts decide it against LOCAL_SCRATCH_DECLARED. (1) The consumer needs no change: comp_debt.py runs ONE _ISOLATED_SWEEP constant against both surfaces on n.node_type/n.node_id, columns the served schema already has, so JOIN turns the last local Kuzu open in a user-facing tool into a client query. (2) The local artifact is already un-maintainable and known to be: the CTO's K4 adjudication froze its vintage in graph-call-manifest.yaml:1199 ('NO nightly reload exists; the prior reload-on-the-nightly-cycle claim was fiction'), its bytes were mutated 51 days after its manifest by something that stamped nothing (W3-S11), and comp-debt refuses on it TODAY at 322h > 48h. Declaring that permanent scratch would bless a second compile business on this laptop and freeze a REACHABILITY family that only degrades on this box. (3) LOCAL_SCRATCH_DECLARED would also have to explain why the estate's canonical cross-layer freshness already 'rides kuzu_nessie_db' (same manifest entry) while its cross-layer TYPES live in a hand-built copy. The honest cost is stated beside the answer, not hidden by it: the cloud producer has NEVER succeeded (67 of 67 builds FAILED, W3-S10), so the FIRST later-round cell is repairing it, and until the stitch types are SERVED this leg stays DECLARED-LOCAL and refuses rather than scoring against a surface nobody maintains.",
  "producer": {
    "tf_resource": "infra/aws/terraform/globgrph/stitch-produce.tf:224-235 -- aws_cloudwatch_event_rule.stitch_produce_nightly + aws_cloudwatch_event_target.stitch_produce_nightly -> aws_codebuild_project.stitch_produce (opal-stitch-produce)",
    "schedule": "cron(0 3 * * ? *) -- 03:00 UTC nightly, after the 02:00Z AWS snapshot; live State=ENABLED, 1 target (events describe-rule + list-targets-by-rule, 2026-09-09T16:2xZ)",
    "s3_key": "s3://opal-313476888478-globgrph/stitch/stitch_graph.json (artifact) + stitch/stitch_marker.json (marker-last, the atomic commit point); source zip at stitch-source/source.zip",
    "vintage_now": "artifact LastModified 2026-09-04T15:05:22Z, 39,722,299 B; marker built_at 2026-09-04T15:05:12Z, aws_snapshot snapshots/20260904/graph-20260904.tar.gz, total_nodes 29219, total_edges 61628, producer 'stitch-local' -- i.e. a LOCAL run, not the nightly. Builds: 67 of 67 FAILED, 0 SUCCEEDED; source.zip LastModified 2026-07-07 (LEG-1 never re-pushed). Filed as NFRA_CLDGRPH-W3-S10."
  },
  "consumer": {
    "file": "infra/aws/globgrph/comp_debt.py",
    "lines": "40 (STITCH_DB), 133-142 (absent-store REFUSE, this order's edit), 151-160 (STALE REFUSE, this order's edit), 230 (kuzu.Connection(kuzu.Database(path, read_only=True)) -- the last local Kuzu open in a user-facing tool), 47-50 + 217-232 (the single _ISOLATED_SWEEP constant run against BOTH surfaces)"
  },
  "later_round_cells": [
    {
      "surface": "infra/aws/terraform/globgrph/stitch-produce.tf + .github/workflows/stitch-source-push.yml + infra/aws/globgrph/derive_stitch.py",
      "lane": "0.7.0_AE_CloudOps",
      "verb": "repair",
      "accept": "ONE rule-initiated CodeBuild of opal-stitch-produce reads SUCCEEDED and stitch/stitch_marker.json carries a producer that is NOT 'stitch-local' with a built_at inside 26h, measured by batch-get-builds and head-object with the build id and the marker quoted; the source zip's LastModified is inside the same window, so the nightly is proven to be running current source. Denominator: builds since the fix, printed."
    },
    {
      "surface": "infra/aws/globgrph/projection_worker.py + the derive/engine path that feeds it",
      "lane": "0.8.0_AE_CloudComp",
      "verb": "extend",
      "accept": "the served artifact's published manifest declares a stitch source vintage beside its Nessie one, and a thin-client query for the stitch types returns non-zero -- MATCH (n:CloudNode) WHERE n.node_type IN ['GOLD_SCRIPT','S3_DATA_KEY'] RETURN count(*) -- with a positive control on a type the projection already carries and the artifact's counts verified by _verify_manifest_counts as they are today. DEPENDS ON the repair cell: a join to a producer that has never succeeded serves nothing."
    },
    {
      "surface": "infra/aws/globgrph/comp_debt.py",
      "lane": "0.8.0_AE_CloudComp",
      "verb": "repoint",
      "accept": "dispatch_reachability opens NO local store -- an ast read returns 0 kuzu.Database calls and 0 `import kuzu` in the file -- both surfaces answer through projection_client, and _stitch_freshness with its two refusals is DELETED with its reason recorded, not commented out. The dual-surface dedup and the GOLD_SCRIPT script-level filter must produce the same census on the served graph as the local one did, with both numbers printed."
    },
    {
      "surface": "infra/aws/globgrph/kuzu_stitch_db (main workspace) + infra/aws/globgrph/kuzu_stitch_load.py",
      "lane": "0.8.0_AE_CloudComp",
      "verb": "retire",
      "accept": "a CG-s-19-shaped disposition record with RETIRE_WITH_TOMBSTONE, an owner and a reason, EXECUTED once the repoint cell lands: 0 readers measured by an ast walk over the tool homes beside a positive control, then the store deleted and a tombstone left naming the vintage, the counts and the 2026-08-27 un-described mutation. NOT before: deleting the store while comp-debt still opens it converts a labelled refusal into a crash."
    }
  ],
  "manifest_claim": {
    "path": "C:/Users/AndrewBerman/Desktop/ajb_workspace/infra/aws/globgrph/kuzu_stitch_db._build_manifest.json",
    "edge_count_claim": "merge_attempts",
    "artifact_claim": "interim_local_projection",
    "builder_stamps_it": "infra/aws/globgrph/kuzu_stitch_load.py -- _stamp_claim(mpath, edge_count_claim='merge_attempts', artifact_claim='interim_local_projection') at the manifest-writing call site in main()",
    "pre_existing_keys_unchanged": "6 of 6",
    "what_the_claim_does_NOT_say": "that the counts are STALE. built_at 2026-07-07 does not describe the 2026-08-27 bytes; no field in this schema can express that, which is why it travels as row NFRA_CLDGRPH-W3-S11 and not as a manifest value."
  },
  "rebuild_path_to_projection": 0,
  "surprise_rows": ["NFRA_CLDGRPH-W3-S10", "NFRA_CLDGRPH-W3-S11", "NFRA_CLDGRPH-W3-S12"],
  "prior_rulings_engaged": [
    "CTO K4 ruling 2026-08-04 191057Z (DIAL_RECORD_comp-kuzu_20260804.md:85-92): 'The stitch DB's fate is adjudicated at the C-indexed consolidation PRD ... NO interim rebuild machinery gets built ... K4 moves to DISPOSITIONED-PENDING-PRD.' THIS RECORD IS THAT ADJUDICATION ARRIVING, and it builds no interim machinery: it names cells, it does not cut them.",
    "graph-call-manifest.yaml:1199 (K4 adjudication, CTO): kuzu_stitch_db is FROZEN VINTAGE, 'last built 2026-07-07, NO nightly reload exists; the prior reload-on-the-nightly-cycle claim was fiction ... canonical cross-layer freshness rides kuzu_nessie_db'. JOIN_PROJECTION is the answer that makes that sentence true of the TYPES as well as of the freshness."
  ]
}
```

## 3. THE MECHANICAL HALF (what this order actually changed)

| surface | change | evidence |
|---|---|---|
| `comp_debt.py:133-142` | the absent-store refusal names `HOME: JOIN_PROJECTION`, `CG-s-20` and this record, and says *do not rebuild it to silence this refusal* | E4-AC2, 2 of 2 |
| `comp_debt.py:151-160` | the stale refusal does the same, and adds that the age is measured from the STORE's mtime and not from `built_at`, which have diverged | E4-AC2, 2 of 2 |
| `kuzu_stitch_load.py` | `_stamp_claim()` + its call from the manifest-writing site: every future build stamps `edge_count_claim=merge_attempts`, `artifact_claim=interim_local_projection` | E4-AC3, `BUILDER_STAMPS_CLAIM=true` |
| main workspace manifest | the two fields ADDED in place, 6 of 6 pre-existing keys asserted unchanged, store bytes and mtime unchanged | E4-AC3, `MANIFEST_CLAIM_FIELDS=2 of 2`, `UNCHANGED=True` |

**The bounded real run** (`timeout 120 python infra/aws/globgrph/comp_debt.py`, rc=1, stdout empty): the nessie leg
ANSWERED (`freshness_assert` reached `projection_client.health()` without raising, so the served graph was reachable)
and the stitch leg refused NOT-FOUND -- because `STITCH_DB` is resolved beside the SCRIPT and the store is gitignored,
so no worktree copy can ever see it. Run from the main workspace, where the store IS present, the refusal is STALE
(`age 322h > 48h`). Both are correct; the face's expectation that it *"must not refuse on the stitch leg"* is
unsatisfiable at this vintage by either path, which is filed as **W3-S12** and is not a criterion failure -- E4-AC5
grades the commit gate.

## 4. E4-AC6 -- THE HOME READING (a reading act; no verdict; graded by `3.0.0_SA_CVO` at L9, read by `1.0.0_SA_CTO` at L10)

**Why JOIN and not DECLARE.** The question is not "is this store useful" -- it is "where does this SURFACE live".
The stitch graph is a *derived cross-layer union*: portal/pipeline nodes stitched to AWS-layer nodes. Nothing about
that computation wants a laptop. It already has a cloud producer, an S3 landing key, a marker protocol and a schedule;
what it lacks is a serving path, and the local Kuzu store is standing in for one. `LOCAL_SCRATCH_DECLARED` would take
the one piece of the surface that is accidentally local -- the compile -- and make it the definition. That is the
inversion the PRD's arc exists to prevent, and CG-s-8 already refused it once for the canonical graph.

**The strongest argument the other way, and why it does not win.** The producer has never succeeded: 67 of 67 builds
FAILED and the artifact in S3 was made by hand. One could read that as "the cloud path is a fiction; bless the local
one". I read it the opposite way, and the marker is why: the S3 artifact's own `producer` field says `stitch-local`.
Somebody already runs this locally and pushes the result to the cloud key. The estate is ALREADY treating the cloud
key as the home; only the compute is misplaced. Declaring the local store canonical would ratify the workaround and
retire the destination. So: JOIN, and name the producer repair as the first cell, which is what makes the answer
honest rather than aspirational.

**What JOIN costs, as cells.** Four, named above with lanes, verbs and accepts: repair the producer
(`0.7.0_AE_CloudOps`), extend the projection to carry the stitch source (`0.8.0_AE_CloudComp`), repoint comp-debt's
second leg through the thin client (`0.8.0_AE_CloudComp`), retire the local store (`0.8.0_AE_CloudComp`). Only the
first two are real work; the third is the D-7 repoint again on a second leg, and the fourth is a CG-s-19 disposition
executed. This order builds NONE of them, which is what the CTO's K4 ruling requires -- *no interim rebuild machinery
gets built* -- and the ordering matters: retiring the store before the repoint converts a labelled refusal into a
crash.

**Does DECLARE leave a second compile business?** Yes, and worse: an UNMAINTAINED one. The measured state is a store
that comp-debt refuses today at 322h, whose bytes were last written by something that recorded nothing, whose manifest
describes bytes from 51 days earlier, whose builder reads a `stitch_graph.json` two months old, and whose declared
refresh consumer (`ensure_fresh`, promised in `stitch-produce.tf:22-23`) does not exist. `LOCAL_SCRATCH_DECLARED`
would freeze all of that as the design.

**The mtime gap.** Yes -- the store was mutated by something the manifest does not describe, and that is the
sharpest single fact in this cell. `Modify == Change` at 2026-08-27 02:32:00.480 is a content write; the manifest was
not rewritten, so it was not a build; and the same directory carries a *different* shape (three files sharing a
`Change` at 2026-08-25 02:16:36 with much older `Modify` times) that shows what a mere metadata sweep looks like here.
The consequence is not academic: comp-debt reports "age 322h" against a store whose build is 64 days old, because its
staleness oracle is the mtime and its `built_at` is only printed. A store whose freshness signal is a timestamp that
some other process can move is not a surface anyone should score against -- which is a third, independent reason the
home is not here.

**What this order deliberately did not do.** It did not build, cut or schedule any of the four later-round cells; it
did not touch the producer's Terraform, the GH-Action, the cloud engine, the thin client or `projection_worker.py`; it
did not diagnose the CodeBuild exit-2 (the build runs a 2026-07-07 source snapshot, so the failure is not in the file
I can read at HEAD); it did not rebuild, delete, move or open any store; it did not create the `ensure_fresh` consumer
the Terraform header promises -- that is precisely the local rebuild path the cell forbids; and it did not soften the
two refusals into warnings, because a refusal that names its decision is the only thing keeping this surface honest
until the JOIN lands.

## 5. THE SCRIPTS

| script | criterion | what it can FAIL on |
|---|---|---|
| `stitch_home_recorded.sh` | E4-AC1 | a home outside the two-value vocabulary, a missing owner/reason, a missing producer field, a JOIN with no later-round cell carrying a lane; a planted record without a reason passing the same parser |
| `refusal_names_home.sh` | E4-AC2 | either stitch refusal not naming the home token and the cell; a reader that cannot score a control whose refusals name neither |
| `stitch_manifest_claim.sh` | E4-AC3 | a builder that stops stamping the two keywords; a manifest missing either field; a store whose bytes or mtime moved from the cut |
| `no_projection_rebuild_path.sh` | E4-AC4 | any import, call, name or path string of the canonical loader, its rebuild entrypoint, its path constant or its store in either edited file |
| `commit_gate_all.sh` | E4-AC5 | any `.py` this order touches failing the gate; it also quotes the bounded real run of `comp_debt.py` |
