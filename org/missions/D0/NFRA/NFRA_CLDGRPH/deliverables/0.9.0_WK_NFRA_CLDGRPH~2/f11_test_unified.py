#!/usr/bin/env python3
"""F11 fixture -- the identity merge, the grain split, the carry and the retired stamp.

No network, no AWS. Every arm drives the producer's own functions on hand-built graphs, which is
the only way to exercise the cases the LIVE artifact does not currently contain (an ambiguous
pipeline id, an edge whose endpoint must follow its node).

WHAT EACH ARM IS FOR -- an arm that cannot fail is not a test:
  1  grain split            gold:x -> PipelineScript, gold:x:fn -> PipelineFunction
  2  merge by identity      a stitch id that resolves takes the CANONICAL id
  3  carry, never drop      an unresolvable member keeps its own id and gains origin=stitch
  4  ambiguity is a carry   an id matching TWO canonical ids is carried, not assigned to one
  5  quote normalisation    "rqk:'k'" resolves to rqk:k; rqk:QUERY_KEY does not
  6  EDGES FOLLOW NODES     an edge built on a stitch id is rewritten to the canonical id --
                            the arm that would have left DERIVES_FROM/STORED_IN dangling
  7  the merged node        collapses onto the canonical node; the canonical one survives
  8  reconciliation         admitted = merged + carried, lost = 0, on the fixture's own numbers
  9  the map                0 of the 4 provisional entries, PORTAL_BUNDLE kept, 61 keys
 10  the stamp              the fold writes no vocabulary property on any node
"""
import json
import os
import sys

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("  %-34s %s %s" % (name, "PASS" if ok else "FAIL", detail))


def _find_ws(start):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(12):
        if os.path.isfile(os.path.join(d, "infra", "aws", "globgrph", "derive_stitch.py")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise SystemExit("BLOCKED: could not locate the workspace root from " + start)


WS = _find_ws(__file__)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))
sys.path.insert(0, os.path.join(WS, "infra", "aws", "globgrph"))

import derive_runner as DR              # noqa: E402
import derive_stitch as DS              # noqa: E402
import extract_portal_stitch as EPS     # noqa: E402

CANON = [
    {"id": "pipeline:bd:gold:A_00.x", "type": "PipelineScript", "source": "graphuni"},
    {"id": "pipeline:bd:gold:A_00.x:load", "type": "PipelineFunction", "source": "graphuni"},
    {"id": "opal-data-bd/gold/only_one.parquet", "type": "S3Key", "source": "graphuni"},
    {"id": "opal-data-bd/gold/two_firms.json", "type": "S3Key", "source": "graphuni"},
    {"id": "opal-data-inf/gold/two_firms.json", "type": "S3Key", "source": "graphuni"},
    {"id": "component:portal/src/App.tsx", "type": "Component", "source": "ts_semantic"},
    {"id": "rqk:known-key", "type": "ReactQueryKey", "source": "ts_semantic"},
]
STITCH = [
    {"id": "gold:A_00.x", "type": "PipelineScript", "source": DS.STITCH_SOURCE},
    {"id": "gold:A_00.x:load", "type": "PipelineFunction", "source": DS.STITCH_SOURCE},
    {"id": "gold:nowhere.script", "type": "PipelineScript", "source": DS.STITCH_SOURCE},
    {"id": "s3:gold/only_one.parquet", "type": "S3Key", "source": DS.STITCH_SOURCE},
    {"id": "s3:gold/two_firms.json", "type": "S3Key", "source": DS.STITCH_SOURCE},
    {"id": "component:portal/src/App.tsx", "type": "Component", "source": DS.STITCH_SOURCE},
    {"id": "rqk:'known-key'", "type": "ReactQueryKey", "source": DS.STITCH_SOURCE},
    {"id": "rqk:QUERY_KEY", "type": "ReactQueryKey", "source": DS.STITCH_SOURCE},
    {"id": "portal", "type": "PORTAL_BUNDLE", "source": DS.STITCH_SOURCE},
]


def main():
    print("F11 -- THE STITCH VOCABULARY UNIFIED AT THE PRODUCER (fixture)")
    print()

    # ---- arm 1: the grain split, from the producer's own helper -----------------
    check("grain_split_script", EPS._pipeline_grain("gold:A_00.x") == "PipelineScript")
    check("grain_split_function", EPS._pipeline_grain("gold:A_00.x:load") == "PipelineFunction")
    check("producer_emits_canonical_names",
          EPS.NODE_TYPE_MAP == {"COMPONENT": "Component", "ENDPOINT": "API_ROUTE",
                                "S3_ARTIFACT": "S3Key", "GOLD_SCRIPT": "PipelineScript"},
          "NODE_TYPE_MAP carries no provisional name")

    classes = {"canon": {"nodes": [dict(n) for n in CANON]},
               "stitch": {"nodes": [dict(n) for n in STITCH]}}
    edges = [
        {"source": "s3:gold/only_one.parquet", "target": "gold:A_00.x",
         "edge_type": "DERIVES_FROM"},
        {"source": "s3:gold/only_one.parquet", "target": "arn:aws:s3:::opal-data-bd",
         "edge_type": "STORED_IN"},
        {"source": "gold:nowhere.script", "target": "s3:gold/two_firms.json",
         "edge_type": "WRITES"},
    ]
    idx = DS.build_canonical_index(classes)

    # ---- arms 2-5: the resolver, one case at a time ----------------------------
    cid, why = DS.resolve_stitch_id({"id": "gold:A_00.x", "type": "PipelineScript"}, idx)
    check("merge_by_identity", cid == "pipeline:bd:gold:A_00.x" and why is None, "-> %s" % cid)
    cid, why = DS.resolve_stitch_id({"id": "gold:nowhere.script", "type": "PipelineScript"}, idx)
    check("carry_when_absent", cid is None and why == "no-canonical-pipeline-node", why or "")
    cid, why = DS.resolve_stitch_id({"id": "s3:gold/two_firms.json", "type": "S3Key"}, idx)
    check("ambiguity_is_a_CARRY_not_a_pick", cid is None and why == "ambiguous-across-firms",
          "two firms hold this key; picking one would invent a cross-firm claim")
    cid, why = DS.resolve_stitch_id({"id": "rqk:'known-key'", "type": "ReactQueryKey"}, idx)
    check("quote_normalisation_resolves", cid == "rqk:known-key", "-> %s" % cid)
    cid, why = DS.resolve_stitch_id({"id": "rqk:QUERY_KEY", "type": "ReactQueryKey"}, idx)
    check("a_variable_name_does_not_resolve", cid is None and why == "no-canonical-query-key")

    # ---- arms 6-8: the whole pass ----------------------------------------------
    stats = DS.unify_stitch_vocabulary(classes, edges, log=lambda m: None)
    ids_after = {n["id"] for v in classes.values() for n in v["nodes"]}
    stitch_after = {n["id"]: n for v in classes.values() for n in v["nodes"]
                    if n.get("source") == DS.STITCH_SOURCE}

    check("edges_follow_their_nodes",
          edges[0]["source"] == "opal-data-bd/gold/only_one.parquet"
          and edges[0]["target"] == "pipeline:bd:gold:A_00.x",
          "DERIVES_FROM %s -> %s" % (edges[0]["source"][:34], edges[0]["target"][:34]))
    check("stored_in_endpoint_rewritten",
          edges[1]["source"] == "opal-data-bd/gold/only_one.parquet")
    check("carried_edge_endpoints_unchanged",
          edges[2]["source"] == "gold:nowhere.script"
          and edges[2]["target"] == "s3:gold/two_firms.json",
          "a carried node keeps its id, so its edges keep pointing at it")
    check("merged_node_collapsed_onto_canonical",
          "gold:A_00.x" not in ids_after and "pipeline:bd:gold:A_00.x" in ids_after
          and sum(1 for v in classes.values() for n in v["nodes"]
                  if n["id"] == "pipeline:bd:gold:A_00.x") == 1)
    carried = [n for n in stitch_after.values() if n.get("origin") == "stitch"]
    # THREE, not four: PORTAL_BUNDLE is not a unified type, so it is never a census member and
    # never carries an origin. The fixture's own arithmetic says so -- admitted 8 of 9 nodes.
    check("carried_carry_origin_and_reason",
          len(carried) == 3 and all(n.get("origin_reason") for n in carried),
          "carried=%s" % sorted(n["origin_reason"] for n in carried))
    check("reconciles_admitted_eq_merged_plus_created",
          stats["admitted"] == stats["merged"] + stats["created"] and stats["lost"] == 0,
          "admitted=%d merged=%d created=%d lost=%d"
          % (stats["admitted"], stats["merged"], stats["created"], stats["lost"]))
    check("portal_bundle_is_not_unified",
          "portal" in ids_after and stitch_after["portal"].get("origin") is None,
          "PORTAL_BUNDLE is the one genuinely new class and is left alone")

    # ---- arms 9-10: the map and the stamp ---------------------------------------
    gone = [t for t in ("GOLD_SCRIPT", "S3_DATA_KEY", "PORTAL_COMPONENT", "REACT_QUERY_KEY")
            if t in DR.NODE_TYPE_LAYER]
    check("map_retired_the_four", not gone, "still present: %s" % gone)
    check("map_kept_PORTAL_BUNDLE", DR.NODE_TYPE_LAYER.get("PORTAL_BUNDLE") == "portal")
    check("map_is_61_keys", len(DR.NODE_TYPE_LAYER) == 61,
          "keys=%d (65 -> 61; the CVO re-signs at L9)" % len(DR.NODE_TYPE_LAYER))
    check("stamp_constants_gone",
          not hasattr(DR, "STITCH_V1_TYPES") and not hasattr(DR, "STITCH_V1_STAMP"))

    g = {"classes_data": {"s3": {"nodes": [{"id": "arn:aws:s3:::b", "type": "S3_BUCKET"}]}},
         "edges": []}
    doc = {"classes_data": {"m": {"nodes": [
        {"id": "pipeline:bd:gold:A_00.x", "type": "PipelineScript", "name": "x"},
        {"id": "component:portal/src/App.tsx", "type": "Component", "name": "App"}]}},
        "edges": []}
    body = json.dumps(doc).encode()
    import hashlib
    marker = {"built_at": "2026-09-09T22:00:00Z", "producer": "stitch-codebuild",
              "git_sha": "0" * 40, "artifact_sha256": hashlib.sha256(body).hexdigest()}
    v = DR.fold_stitch_document(g, body, marker)
    folded = g["classes_data"][DR.STITCH_CLASS]["nodes"]
    check("fold_writes_no_stamp",
          v["stitch_v1_stamped"] == 0 and all("vocabulary" not in n for n in folded),
          "stamped=%d over %d folded node(s)" % (v["stitch_v1_stamped"], len(folded)))

    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    total = len(RESULTS)
    print()
    print("F11_TESTS=%d passed of %d" % (passed, total))
    print("  DENOMINATOR: %d of %d assertions across 10 named arms, 4 of them controls that must"
          " be able to fail (the absent member, the ambiguous member, the variable-name query key,"
          " and the edge that must follow its node)." % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
