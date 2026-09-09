# CG-s-24 -- THE FOLD IS BUILT; THE JOIN IS BLOCKED ON A FROZEN TAXONOMY

**TO:** `NFRA_CLDGRPH.TO-CG-F-4` · **cell:** CG-s-24 · **worker:** `0.9.0_WK_NFRA_CLDGRPH~2`,
branch `wk-cldgrph-6-2` · **status: OPEN** -- F4-AC1 PASSES; F4-AC2, F4-AC3 and F4-AC4 are
BLOCKING on `NFRA_CLDGRPH-W2-S45`. **Push state: LOCAL.**

```json
{
  "cell": "CG-s-24",
  "to_id": "NFRA_CLDGRPH.TO-CG-F-4",
  "outcome": "OPEN -- deliverable step 1 delivered and proven; steps 2-4 NOT taken, by the blocking row",
  "worker": "0.9.0_WK_NFRA_CLDGRPH~2",
  "branch": "wk-cldgrph-6-2",
  "push_state": "LOCAL",

  "the_fold": {
    "function": "infra/aws/globgrph/derive_runner.py fold_stitch_document (pure) + ingest_stitch_artifact (the S3 half)",
    "called_from": "main(), last of the folds, immediately BEFORE drop_node_types/relabel_layers_by_node_type",
    "contract": "additive, best-effort -- WARN: STITCH_INGEST_FAIL and the derive continues",
    "guards": [
      "sha256 of the artifact vs the marker's artifact_sha256 -- mismatch is a LOUD skip and the graph is left byte-identical",
      "NODE_TYPE_LAYER membership -- an unmapped node_type is skipped, counted and named; folding one would make relabel_layers_by_node_type FAIL THE DERIVE CLOSED",
      "both-ends resolution -- an edge is folded only if both endpoints resolve in THIS graph; a dangling edge is never created"
    ],
    "edge_types_folded": ["ROUTES_TO", "WRITES", "READS", "DERIVES_FROM", "STORED_IN"],
    "fixture_counts": {"nodes": 3, "edges": 2, "skipped_dup": 1, "tests": "15 passed of 15"}
  },

  "the_vintage_carrier": {
    "reader": "kuzu_nessie_load.read_stitch_vintage (ONE implementation, both engines)",
    "into_pin": ["kuzu_incremental_refresh._read_head_tables", "kuzu_nessie_load's write_manifest call"],
    "keys": ["stitch_built_at", "stitch_producer", "stitch_git_sha", "stitch_artifact_sha256",
             "stitch_marker_last_modified"],
    "onto_the_served_line": "projection_worker._age_line(vintage, manifest) appends 'Stitch source: <producer> built <built_at>.'",
    "why_the_age_line": "no serve path calls _provenance.format_provenance_header; the served VINTAGE line is kuzu_cli._disclosure over four fields projection_server returns, and age_line is the only one reachable from this order's <paths> (row W2-S46)",
    "delta_when_absent": "ZERO -- byte-identical to the pre-CG-s-24 sentence, asserted in the fixture test",
    "prefix_preserved": "APPENDED not prefixed, so TO-CG-D-7's D7-AC3/D7-AC4 ('VINTAGE: Built from the estate as of') stay green"
  },

  "the_blocking_measurement": {
    "row": "NFRA_CLDGRPH-W2-S45",
    "stitch_artifact": {
      "key": "s3://opal-313476888478-globgrph/stitch/stitch_graph.json",
      "bytes": 38845013,
      "sha256_verified_against_marker": true,
      "distinct_node_types": 63,
      "nodes": 29131
    },
    "node_types_absent_from_NODE_TYPE_LAYER": {
      "GOLD_SCRIPT": 1380, "S3_DATA_KEY": 294, "REACT_QUERY_KEY": 94,
      "PORTAL_COMPONENT": 22, "PORTAL_BUNDLE": 1
    },
    "consequence_unguarded": "relabel_layers_by_node_type raises NodeTypeLayerGap -> the nightly derive FAILS CLOSED, no commit, no marker",
    "consequence_guarded": {
      "nodes_dropped": 1791,
      "edges_left_unresolvable": 2170,
      "DERIVES_FROM": "216 of 216 lost",
      "STORED_IN": "955 of 955 lost",
      "WRITES": "309 of 949 lost",
      "READS": "381 of 1191 lost",
      "ROUTES_TO": "0 of 106 lost"
    },
    "ruling_needed_from": "1.0.0_SA_CTO (the map's own governance: every prior addition names a CTO arch-gate GO and a CVO re-sign)"
  },

  "what_was_NOT_done_and_why": {
    "image_act": "NOT TAKEN -- no build, no push, no tag moved",
    "safe_apply": "NOT RUN -- no Terraform touched, no .tf file edited",
    "never_2_entry": "NOT OPENED -- there was no image act to ledger",
    "ad_hoc_derive": "NOT STARTED",
    "reason": "the fold that could ship today carries NONE of the node types the accept names and loses 100% of the DERIVES_FROM and STORED_IN boundary edges; a seven-family NEVER-2 image act spent on that would have to be repeated after the ruling"
  },

  "the_seven_families_UNTOUCHED": {
    "read_at_utc": "2026-09-09T19:3xZ",
    "families_by_digest": "7 of 7",
    "families_on_latest": "0 of 7",
    "distinct_digests": ["sha256:1b89853fe44133f10a60dc2b3e7b463c0d3b68b827a2ddff249bf427ecde2778"],
    "revisions": {"globgrph-derive-runner": 7, "globgrph-projection-worker": 4,
                  "globgrph-serving": 2, "globgrph-comp-learns-producer": 2,
                  "globgrph-cse-producer": 2, "globgrph-fedobs-producer": 2,
                  "globgrph-resource-summaries-producer": 2},
    "note": "the ORDER's seven names resolve 3 of 7 -- row W2-S49"
  },

  "the_pre_fold_served_read": {
    "invocation": "bash .tools/comp-kuzu --json \"MATCH (n:CloudNode) WHERE n.node_type IN ['GOLD_SCRIPT','S3_DATA_KEY','API_ROUTE'] RETURN n.node_type AS t, count(*) AS c ORDER BY t\"",
    "answer": [{"t": "API_ROUTE", "c": 86}],
    "served_stitch_types": "1 of 3 non-zero BEFORE any fold (row W2-S47: the order calls this control 0 of 3)",
    "vintage_line": "VINTAGE: Built from the estate as of 2026-09-09 14:59:48 UTC.  [vintage=2026-09-09T14:59:48.778469+00:00 manifest=86ea84674078 prefix=projection/2026-09-09T14:59:48.778469+00:00/]",
    "pointer": "projection/2026-09-09T14:59:48.778469+00:00/ -- UNCHANGED by this order"
  },

  "surprise_rows_filed": ["NFRA_CLDGRPH-W2-S45", "NFRA_CLDGRPH-W2-S46", "NFRA_CLDGRPH-W2-S47",
                          "NFRA_CLDGRPH-W2-S48", "NFRA_CLDGRPH-W2-S49"],
  "commits": ["<the acts commit>", "<the instance commit>"]
}
```

---

## What happened

The order's route is sound and the fold is built. It stops one layer short of the served graph,
on something the cut could not have seen from outside the file.

`derive_runner.py` ends every derive with `relabel_layers_by_node_type`, which sets each node's
layer from `NODE_TYPE_LAYER` and **raises `NodeTypeLayerGap` on any observed node_type absent from
that map** -- deliberately, as the COND-2 durability cert, so a new resource type forces a map
update instead of silently falling out of the frozen COND-A count. `main()` turns that into
`ERROR: NODE_TYPE_LAYER_GAP -- failing derive CLOSED (no commit)` and `return 1`.

The live stitch artifact carries **63 distinct node types, five of them absent from that map**:
`GOLD_SCRIPT` (1380), `S3_DATA_KEY` (294), `REACT_QUERY_KEY` (94), `PORTAL_COMPONENT` (22),
`PORTAL_BUNDLE` (1). Four of the five are the very types `CG-s-24` closes on. The map's own
comment records why: the `pipeline` `GOLD_SCRIPT`/`S3_DATA_KEY` placeholder was **dropped from
the taxonomy on 2026-06-26** because it was empty and conceptually muddy.

So the fold as ordered has two possible shapes and both are refused here:

* **fold them unguarded** -- the nightly derive fails closed. Not a risk to run once and see;
  the derive is the estate's single writer.
* **add the five to `NODE_TYPE_LAYER`** -- the map is a CVO-signed frozen baseline whose *every*
  prior addition names a CTO arch-gate GO and a CVO re-sign in the comment beside it. TO-CG-F-4
  does not mention the map and does not carry that gate. The path is granted; the authority is
  not, and a worker adding five members to a frozen taxonomy on its own initiative is the
  widening this seat is told not to do.

**The guarded partial fold is not a third option, and that is measured rather than argued.**
Skipping the five unmapped types drops 1,791 of 29,131 nodes and leaves 2,170 edges unresolvable
-- including **216 of 216 `DERIVES_FROM` and 955 of 955 `STORED_IN`**, which are precisely the two
boundary edge types the PRD calls the JOIN. A fold that keeps 100% of the AWS layer it already
has and loses 100% of the join is not a partial delivery; it is an image act spent for nothing.

That is why steps 2-4 were not taken. Not a narrowing of the order: the seven-family image act
would have to be repeated after the ruling, and a NEVER-2 act that reaches seven task families is
not the thing to spend twice.

## What was delivered, and is proven

`fold_stitch_document` is built, gated and exercised: **15 of 15 fixture arms pass**. It carries
three guards and each one is a class of silent damage that now cannot happen -- the sha256 check
(an artifact its own marker does not describe is refused LOUD, leaving the graph byte-identical),
the `NODE_TYPE_LAYER` guard (the finding above, made into a mechanism so a future stitch type
change cannot take the derive down), and the both-ends rule the file's other folds already use.

The vintage carrier is built end to end and reads **one** stitch marker through **one** function
used by **both** engines. It stops at `_age_line` because that is where the grant stops, and that
turned out to be the only place it could go at all: the order's premise that
`_provenance.format_provenance_header` prints the served header is false -- no serve path calls
it. The served `VINTAGE:` line is assembled by `kuzu_cli._disclosure` from four fields
`projection_server` returns, and `age_line` is the only one this order may touch. It is
**appended, never prefixed**, because `TO-CG-D-7`'s D7-AC3 and D7-AC4 are complete criteria that
expect the line to *start* `VINTAGE: Built from the estate as of`; and it is **zero-delta when no
stitch is present**, asserted byte-for-byte in the fixture.

## For the ruling

Two options, and the second is measured to be worse than it looks:

1. **Add the five to `NODE_TYPE_LAYER` under a CTO arch-gate + CVO re-sign**, naming each one's
   layer. Worth noting for the sign-off: four of the five are not AWS resources, so the frozen
   `aws` COND-A count need not move at all -- `GOLD_SCRIPT` is pipeline-shaped, `S3_DATA_KEY` is
   storage under an S3 bucket (the map already rules `S3Key: aws`), `PORTAL_COMPONENT`,
   `REACT_QUERY_KEY` and `PORTAL_BUNDLE` are portal.
2. **Normalise the stitch's vocabulary onto the ratified types.** The artifact carries *both*
   conventions side by side and the populations differ by up to an order of magnitude --
   `GOLD_SCRIPT` 1380 vs `PipelineScript` 133, `S3_DATA_KEY` 294 vs `S3Key` 232,
   `PORTAL_COMPONENT` 22 vs `Component` 199, `REACT_QUERY_KEY` 94 vs `ReactQueryKey` 57. Two
   counts that far apart are not two names for one set; a rename would merge different grains and
   change what every downstream count means, silently. `grain_baseline.json`'s own
   `_naming_fragility_note` records this exact hazard, and its 2026-07-25 recertification
   enumerates three distinct populations for `REACT_QUERY_KEY` alone. Row `W2-S48`.

Either way the code is ready: option 1 needs five map entries and nothing else -- the fold, the
carrier, the guards and the tests all stand, and the `STITCH_UNMAPPED_TYPE` WARN stays as the
mechanism that catches the *next* type nobody mapped.
