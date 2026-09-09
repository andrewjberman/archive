#!/usr/bin/env python3
"""F4-AC1 -- the CG-s-24 stitch fold, exercised on a fixture. TO-CG-F-4, deliverable step 1.

No network, no AWS, no Kuzu, no local store: every arm drives derive_runner.fold_stitch_document
directly, which is why the IO half (ingest_stitch_artifact) is a separate function.

WHAT EACH ARM IS FOR -- an arm that cannot fail is not a test:
  1  the happy fold          3 new nodes land, 1 duplicate ARN is skipped AND counted
  2  the duplicate is REAL   the surviving node is the ORIGINAL, not the stitch's copy
  3  sha256 mismatch         the artifact its marker does not describe is refused LOUD
                             and the graph is left BYTE-IDENTICAL (not partially folded)
  4  unmapped node_type      skipped, counted, named -- and the graph still survives
                             relabel_layers_by_node_type, which FAILS THE DERIVE CLOSED
  5  both-ends resolution    an edge to a node nobody has is not folded as a dangling edge
  6  non-stitch edge types   the artifact's own AWS-layer edges are NOT re-folded
  7  unparseable artifact    a LOUD skip, never a traceback out of the fold
  8  age_line, no stitch     BYTE-IDENTICAL to the pre-CG-s-24 sentence (delta 0)
  9  age_line, with stitch   carries the stitch clause
 10  age_line prefix         still starts "Built from the estate as of" -- TO-CG-D-7's
                             D7-AC3 and D7-AC4 both expect that prefix and are COMPLETE
"""
import hashlib
import json
import os
import sys


def _find_ws(start):
    d = os.path.dirname(os.path.abspath(start))
    for _ in range(12):
        if os.path.isfile(os.path.join(d, "infra", "aws", "globgrph", "derive_runner.py")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    raise SystemExit("BLOCKED: could not locate the workspace root from " + start)


WS = _find_ws(__file__)
sys.path.insert(0, os.path.join(WS, "org", "modules", "graph"))
sys.path.insert(0, os.path.join(WS, "infra", "aws", "globgrph"))

import derive_runner as D          # noqa: E402
import projection_worker as PW     # noqa: E402

BUCKET_ARN = "arn:aws:s3:::opal-data-bd"
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print("  %-34s %s %s" % (name, "PASS" if ok else "FAIL", detail))


def base_graph():
    """A derive graph that already carries ONE node -- the duplicate the stitch also has."""
    return {
        "classes_data": {
            "s3": {"nodes": [{"id": BUCKET_ARN, "type": "S3_BUCKET", "name": "opal-data-bd",
                              "layer": "aws", "source": "derive"}]},
        },
        "edges": [],
    }


def stitch_doc(node_types=("LAMBDA", "API_ROUTE", "S3Key")):
    """Three NEW nodes of MAPPED types + the duplicate + the stitch's own edges."""
    nodes = [{"id": "stitch-node-%d" % i, "type": t, "name": "n%d" % i}
             for i, t in enumerate(node_types)]
    nodes.append({"id": BUCKET_ARN, "type": "S3_BUCKET", "name": "opal-data-bd-FROM-STITCH"})
    return {
        "classes_data": {"mixed": {"nodes": nodes}},
        "edges": [
            # both ends resolve -> folded
            {"source": "stitch-node-2", "target": BUCKET_ARN, "edge_type": "STORED_IN"},
            {"source": "stitch-node-1", "target": "stitch-node-0", "edge_type": "ROUTES_TO"},
            # target is nobody -> NOT folded (both-ends rule)
            {"source": "stitch-node-0", "target": "arn:aws:s3:::nobody", "edge_type": "WRITES"},
            # not a stitch edge type -> NOT folded (the AWS layer is already this derive's)
            {"source": "stitch-node-0", "target": BUCKET_ARN, "edge_type": "HAS_POLICY"},
        ],
    }


def marker_for(body, **over):
    m = {"built_at": "2026-09-09T18:49:23Z", "producer": "stitch-codebuild",
         "git_sha": "de590a7d0227fb9c14ce35b96dcec86deb68df60",
         "aws_snapshot": "snapshots/20260909/graph-20260909.tar.gz",
         "artifact_sha256": hashlib.sha256(body).hexdigest()}
    m.update(over)
    return m


def main():
    print("F4-AC1 -- THE CG-s-24 STITCH FOLD, EXERCISED ON A FIXTURE")
    print("  module under test: %s" % os.path.join(WS, "infra/aws/globgrph/derive_runner.py"))
    print()

    # ---- arms 1, 2, 5, 6: the happy fold -------------------------------------
    g = base_graph()
    body = json.dumps(stitch_doc()).encode()
    v = D.fold_stitch_document(g, body, marker_for(body))
    folded = g["classes_data"].get(D.STITCH_CLASS, {}).get("nodes", [])
    print()
    print("FOLD_OK nodes=%d edges=%d skipped_dup=%d stamped=%d" % (
        v["stitch_nodes_folded"], v["stitch_edges_folded"], v["stitch_nodes_skipped_dup"],
        v["stitch_v1_stamped"]))
    print()
    check("happy_fold_nodes", v["stitch_nodes_folded"] == 3 and len(folded) == 3,
          "folded=%d" % v["stitch_nodes_folded"])
    check("duplicate_skipped_and_counted", v["stitch_nodes_skipped_dup"] == 1,
          "skipped_dup=%d" % v["stitch_nodes_skipped_dup"])
    survivor = g["classes_data"]["s3"]["nodes"][0]["name"]
    check("duplicate_keeps_the_ORIGINAL", survivor == "opal-data-bd",
          "survivor name=%r (the stitch copy would read ...-FROM-STITCH)" % survivor)
    check("both_ends_rule_folds_2_of_3", v["stitch_edges_folded"] == 2,
          "edges=%d of 3 stitch-typed (one targets a node nobody has)" % v["stitch_edges_folded"])
    kinds = sorted({e["edge_type"] for e in g["edges"]})
    check("non_stitch_edge_types_not_folded", "HAS_POLICY" not in kinds, "folded kinds=%s" % kinds)
    check("vintage_carries_the_marker",
          v["stitch_built_at"] == "2026-09-09T18:49:23Z"
          and v["stitch_producer"] == "stitch-codebuild"
          and v["stitch_git_sha"].startswith("de590a7d"),
          "producer=%s built_at=%s" % (v["stitch_producer"], v["stitch_built_at"]))

    # ---- arm 3: the sha256 mismatch ------------------------------------------
    g2 = base_graph()
    before = json.dumps(g2, sort_keys=True)
    bad = marker_for(body, artifact_sha256="0" * 64)
    v2 = D.fold_stitch_document(g2, body, bad)
    after = json.dumps(g2, sort_keys=True)
    arm = "SKIPPED_LOUD" if (v2 is None and after == before) else "NOT_SKIPPED"
    print()
    print("SHA_MISMATCH_ARM=%s" % arm)
    print()
    check("sha_mismatch_returns_None", v2 is None)
    check("sha_mismatch_leaves_graph_UNTOUCHED", after == before,
          "a partial fold under a wrong vintage is the failure this arm exists for")

    # ---- arm 4: an unmapped node_type must never reach the relabel ------------
    # The five stitch-v1 types are MAPPED now (CTO GO 20260909T2015Z), so this arm uses a
    # type nobody has mapped -- which is the case the guard actually exists for: the NEXT
    # node_type a producer invents. Using a now-gated type here would test nothing.
    g3 = base_graph()
    doc3 = stitch_doc()
    doc3["classes_data"]["mixed"].setdefault("nodes", []).append(
        {"id": "future:thing", "type": "SOME_FUTURE_TYPE", "name": "not in the map"})
    body3 = json.dumps(doc3).encode()
    v3 = D.fold_stitch_document(g3, body3, marker_for(body3))
    check("unmapped_type_skipped_and_counted", v3["stitch_nodes_skipped_unmapped_type"] == 1,
          "skipped_unmapped_type=%d (SOME_FUTURE_TYPE)" % v3["stitch_nodes_skipped_unmapped_type"])
    ids = {str(n.get("id")) for c in g3["classes_data"].values() for n in c["nodes"]}
    check("unmapped_type_not_in_the_graph", "future:thing" not in ids)
    relabel_ok, err = True, ""
    try:
        D.drop_node_types(g3)
        D.relabel_layers_by_node_type(g3)
    except Exception as exc:  # noqa: BLE001
        relabel_ok, err = False, "%s: %s" % (type(exc).__name__, exc)
    check("folded_graph_SURVIVES_the_relabel", relabel_ok,
          err or "no NodeTypeLayerGap: the guard kept the unmapped type out, so the derive "
                 "that would have FAILED CLOSED commits")

    # ---- arm 6b (R17): the stitch-v1 stamp, and ONLY on the admitted five ------
    g5 = base_graph()
    doc5 = stitch_doc()
    doc5["classes_data"]["mixed"].setdefault("nodes", []).extend([
        {"id": "gold:some_script.py", "type": "GOLD_SCRIPT", "name": "some_script.py"},
        {"id": "s3key:gold/x.parquet", "type": "S3_DATA_KEY", "name": "gold/x.parquet"},
    ])
    body5 = json.dumps(doc5).encode()
    v5 = D.fold_stitch_document(g5, body5, marker_for(body5))
    folded5 = {str(n["id"]): n for n in g5["classes_data"][D.STITCH_CLASS]["nodes"]}
    stamped_ids = sorted(i for i, n in folded5.items() if n.get("vocabulary") == "stitch-v1")
    check("stitch_v1_stamped_count", v5["stitch_v1_stamped"] == 2,
          "stamped=%d of %d folded" % (v5["stitch_v1_stamped"], v5["stitch_nodes_folded"]))
    check("stitch_v1_stamp_on_the_admitted_five",
          stamped_ids == ["gold:some_script.py", "s3key:gold/x.parquet"],
          "stamped ids=%s" % stamped_ids)
    check("stitch_v1_stamp_NOT_on_a_pre_existing_type",
          folded5["stitch-node-0"].get("vocabulary") is None,
          "the LAMBDA node carries no vocabulary -- the stamp labels the INTERIM population, "
          "not the fold")
    check("gated_five_now_ADMITTED",
          v5["stitch_nodes_skipped_unmapped_type"] == 0 and v5["stitch_nodes_folded"] == 5,
          "folded=%d skipped_unmapped_type=%d (GOLD_SCRIPT and S3_DATA_KEY are in the map now)"
          % (v5["stitch_nodes_folded"], v5["stitch_nodes_skipped_unmapped_type"]))
    relabel5_ok, err5 = True, ""
    try:
        D.drop_node_types(g5)
        D.relabel_layers_by_node_type(g5)
    except Exception as exc:  # noqa: BLE001
        relabel5_ok, err5 = False, "%s: %s" % (type(exc).__name__, exc)
    check("gated_five_SURVIVE_the_relabel", relabel5_ok,
          err5 or "the five are mapped, so the derive that would have failed closed commits")
    check("NODE_TYPE_LAYER_is_65_keys", len(D.NODE_TYPE_LAYER) == 65,
          "keys=%d (CVO C-S40 @e7db04572e: 60 -> 65)" % len(D.NODE_TYPE_LAYER))

    # ---- arm 7: an unparseable artifact --------------------------------------
    g4 = base_graph()
    junk = b"this is not json"
    v4 = D.fold_stitch_document(g4, junk, marker_for(junk))
    check("unparseable_artifact_skips_LOUD", v4 is None and not g4["classes_data"].get(
        D.STITCH_CLASS, {}).get("nodes"))

    # ---- arms 8, 9, 10: the served age line -----------------------------------
    vintage = "2026-09-09T14:59:48.778469+00:00"
    legacy = "Built from the estate as of 2026-09-09 14:59:48 UTC."
    plain = PW._age_line(vintage)
    plain_empty_manifest = PW._age_line(vintage, {"source_vintage": {}})
    with_stitch = PW._age_line(vintage, {"source_vintage": {
        "stitch_built_at": "2026-09-09T18:49:23Z", "stitch_producer": "stitch-codebuild"}})
    print()
    print("AGE_LINE_NO_STITCH=%r" % plain)
    print("AGE_LINE_WITH_STITCH=%r" % with_stitch)
    print()
    check("age_line_delta_ZERO_without_a_stitch",
          plain == legacy and plain_empty_manifest == legacy,
          "byte-identical to the pre-CG-s-24 sentence")
    check("age_line_carries_the_stitch_when_present",
          "Stitch source: stitch-codebuild built 2026-09-09T18:49:23Z." in with_stitch)
    check("age_line_keeps_D7_AC3_AC4_prefix",
          with_stitch.startswith("Built from the estate as of"),
          "TO-CG-D-7's two COMPLETE criteria expect this prefix; the clause is APPENDED")

    passed = sum(1 for _n, ok, _d in RESULTS if ok)
    total = len(RESULTS)
    print()
    print("F4_TESTS=%d passed of %d" % (passed, total))
    print("  DENOMINATOR: %d of %d assertions passed across 11 named arms, 4 of them controls"
          " that must be able to fail (the sha mismatch, the now-synthetic unmapped type, the"
          " both-ends rule, and the pre-existing type that must NOT carry the stitch-v1 stamp)."
          % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
