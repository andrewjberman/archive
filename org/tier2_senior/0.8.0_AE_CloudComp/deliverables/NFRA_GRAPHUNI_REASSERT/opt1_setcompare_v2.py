#!/usr/bin/env python
"""
NFRA_GRAPHUNI SET-DIFF dispatch -- v2 reconstruction (fixes a node-insertion-order bug
found in v1/opt1_setcompare.py): v1 built nodes lazily off EDGE iteration order, which
scrambled node insertion order relative to the original build_graph (which inserts each
script's own node BEFORE its function children, extract_s3.py:347-377). That let
find_node()'s [0]-index pick (cli.py:568 `node = matches[0]`) land on a FUNCTION node for
a SCRIPT-level query in the reconstruction, while the fixture's original build always
resolves matches[0] to the intended SCRIPT node -- an apples-to-a-different-node
comparison, not a real coverage gap, for however much of the mismatch that bug caused.

v2 pre-populates ALL nodes from the producer's own `nodes` list (which preserves the
correct script-before-function order, inherited transitively from build_graph's own
insertion order) BEFORE processing any edges, so matches[0] resolves identically to how
the original fixture capture resolves it.

Author: 0.8.0_AE_CloudComp~D, per CTO~Z dispatch NFRA_GRAPHUNI SET-DIFF (20260725T065418Z).
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, WS)

from org.modules.graph import cli as cli_mod  # noqa: E402
from org.modules.graph.trace_graph import Edge, Node, TraceGraph  # noqa: E402

SP = os.path.dirname(__file__)
FIXTURE_DIR = os.path.join(WS, "org", "tier1_exec", "3.0.0_SA_CVO", "NFRA_GRAPHUNI_P0-CVO_fixture")
PRODUCER_JSON = os.path.join(SP, "gold_compute_producer_FULL_20260725.json")

sample_doc = json.load(open(os.path.join(FIXTURE_DIR, "sample.deterministic.json")))
S = sample_doc["sample"]
fixture = json.load(open(os.path.join(FIXTURE_DIR, "fixture_layer_a.tool_answers.json")))
old = fixture["tool"]

doc = json.load(open(PRODUCER_JSON))
PIPELINE_RE = re.compile(r"^pipeline:[a-z_]+:gold:(.+)$")


def un_pipeline_id(pid: str) -> str | None:
    m = PIPELINE_RE.match(pid)
    return ("gold:" + m.group(1)) if m else None


def un_s3_id(target: str) -> str | None:
    m = re.match(r"^opal-data-[a-z]+/(.+)$", target)
    return ("s3:" + m.group(1)) if m else None


g = TraceGraph(built_at=0.0)

# --- FIX: pre-populate nodes in the producer's own order, script-before-function preserved ---
node_type_by_id = {}
for n in doc["nodes"]:
    canon = un_pipeline_id(n["id"])
    if not canon:
        continue
    if canon in node_type_by_id:
        continue
    node_type_by_id[canon] = "GOLD_SCRIPT"
    g.add_node(Node(id=canon, node_type="GOLD_SCRIPT", label=canon))

skipped_edges = {"CONTAINS": 0, "unmapped_node": 0}
for e in doc["edges"]:
    et = e["edge_type"]
    if et == "CONTAINS":
        skipped_edges["CONTAINS"] += 1
        continue
    src_raw, tgt_raw = e["source"], e["target"]
    if et == "CALLS":
        s, t = un_pipeline_id(src_raw), un_pipeline_id(tgt_raw)
        if not (s and t):
            skipped_edges["unmapped_node"] += 1
            continue
        g.add_edge(Edge(source=s, target=t, edge_type="CALLS"))
    elif et == "WRITES_S3":
        s, t = un_pipeline_id(src_raw), un_s3_id(tgt_raw)
        if not (s and t):
            skipped_edges["unmapped_node"] += 1
            continue
        if t not in g.nodes:
            g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
        g.add_edge(Edge(source=s, target=t, edge_type="WRITES_S3"))
    elif et == "READS_S3":
        s, t = un_pipeline_id(src_raw), un_s3_id(tgt_raw)
        if not (s and t):
            skipped_edges["unmapped_node"] += 1
            continue
        if t not in g.nodes:
            g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
        g.add_edge(Edge(source=t, target=s, edge_type="READS_S3"))  # polarity flip, as v1

print(f"RECONSTRUCTED (v2, node-order-fixed): nodes={len(g.nodes)} edges={len(g.edges)} "
      f"skipped={skipped_edges}", file=sys.stderr)

# --- verify the fix: matches[0] for the sharp case must now be the SCRIPT node itself ---
m0 = g.find_node("gold:D_01.partner_analytics")
print(f"VERIFY: find_node('gold:D_01.partner_analytics') -> {len(m0)} matches, "
      f"matches[0]={m0[0].id if m0 else None}", file=sys.stderr)
assert m0 and m0[0].id == "gold:D_01.partner_analytics", (
    "node-order fix did not work -- matches[0] is not the script node")

_orig_get_graph = cli_mod._get_graph
cli_mod._get_graph = lambda force_rebuild=False, check_freshness=True: g


def run_cli(argv) -> tuple[str, int]:
    old_argv = sys.argv
    sys.argv = ["cli.py"] + argv
    buf = io.StringIO()
    rc = 0
    try:
        with contextlib.redirect_stdout(buf):
            cli_mod.main()
    except SystemExit as ex:
        rc = ex.code if isinstance(ex.code, int) else (1 if ex.code else 0)
    finally:
        sys.argv = old_argv
    return buf.getvalue(), rc


# ---------------------------------------------------------------------------
# Full 28-target re-run (corrected v2 numbers, supersedes v1's OPT1_RUN.md figures
# for the sharp case specifically -- see GRAPHUNI_SETDIFF.md for the delta).
# ---------------------------------------------------------------------------
blast_targets = S["blast_fn_bd"] + S["blast_fn_inf"] + S["blast_script"] + S["s3_top"]
report = {}
match_n = 0
for tgt in blast_targets:
    out, rc = run_cli(["blast", tgt, "--json", "--direction", "both"])
    old_ids = set(old["comp-blast"].get(tgt, {}).get("radius_ids", []))
    try:
        d = json.loads(out)
        new_ids = set()
        for bucket in ("consumers", "producers"):
            for cls, lst in (d.get(bucket) or {}).items():
                for it in lst:
                    new_ids.add(it["id"])
    except Exception as ex:
        report[tgt] = {"status": "PARSE-ERROR", "rc": rc, "err": str(ex)}
        continue
    match = (old_ids == new_ids)
    if match:
        match_n += 1
    report[tgt] = {
        "status": "MATCH" if match else "MISMATCH",
        "old_n": len(old_ids), "new_n": len(new_ids),
        "missing_from_new": sorted(old_ids - new_ids),
        "extra_in_new": sorted(new_ids - old_ids),
    }

cli_mod._get_graph = _orig_get_graph
verdict = "SET-IDENTITY PROVEN" if match_n == len(blast_targets) else "SET-IDENTITY REFUTED"
print("=" * 70)
print("v2 VERDICT:", verdict, f"{match_n}/{len(blast_targets)}")

out_path = os.path.join(SP, "OPT1_SETCOMPARE_v2_result.json")
json.dump({"verdict": verdict, "match": f"{match_n}/{len(blast_targets)}", "per_target": report},
          open(out_path, "w"), indent=2)
print("WROTE", out_path)

# ---------------------------------------------------------------------------
# SET-DIFF + EDGE-CLASS PARTITION on the sharp case (script grain), plus the
# function-level CONTROL, per the SET-DIFF dispatch.
# ---------------------------------------------------------------------------
if not g._indexed:
    g._build_index()

# ---------------------------------------------------------------------------
# Load the FIXTURE's own pinned pre-delta graph (real TraceGraph, the same one the
# fixture capture ran against) so a missing member's edge class is read from the graph
# that actually produced the fixture's expected answer, not guessed or left unclassified.
# ---------------------------------------------------------------------------
PINNED = os.path.join(FIXTURE_DIR, "graph.json.pinned_predelta")
from pathlib import Path as _Path  # noqa: E402
fixture_graph = TraceGraph.load(_Path(PINNED))
if not fixture_graph._indexed:
    fixture_graph._build_index()


def edge_classes_into(node_id: str, tg: TraceGraph) -> list[str]:
    """Every edge type on an edge that has node_id as its TARGET in tg (i.e. an edge that
    would place node_id one hop closer to a seed doing forward/downstream traversal, or
    the reverse-direction equivalent for upstream) -- the direct connecting edge class(es)
    for this node in this specific graph."""
    return sorted({e.edge_type for e in tg._reverse.get(node_id, [])} |
                  {e.edge_type for e in tg._forward.get(node_id, [])})


def blast_ids_and_report(target: str):
    out, _ = run_cli(["blast", target, "--json", "--direction", "both"])
    d = json.loads(out)
    new_ids = set()
    for bucket in ("consumers", "producers"):
        for cls, lst in (d.get(bucket) or {}).items():
            for it in lst:
                new_ids.add(it["id"])
    return new_ids


cli_mod._get_graph = lambda force_rebuild=False, check_freshness=True: g
script_new = blast_ids_and_report("gold:D_01.partner_analytics")
fn_new = blast_ids_and_report("gold:D_01.partner_analytics:generate_header_metrics")
cli_mod._get_graph = _orig_get_graph

script_old = set(old["comp-blast"].get("gold:D_01.partner_analytics", {}).get("radius_ids", []))
fn_old = set(old["comp-blast"].get("gold:D_01.partner_analytics:generate_header_metrics", {}).get("radius_ids", []))

script_missing = sorted(script_old - script_new)
script_extra = sorted(script_new - script_old)
fn_missing = sorted(fn_old - fn_new)
fn_extra = sorted(fn_new - fn_old)

from collections import Counter  # noqa: E402

script_missing_classes = {nid: edge_classes_into(nid, fixture_graph) for nid in script_missing}
fn_missing_classes = {nid: edge_classes_into(nid, fixture_graph) for nid in fn_missing}


def distribution(classes_map):
    c = Counter()
    for nid, classes in classes_map.items():
        key = ",".join(classes) if classes else "NO-EDGE-IN-FIXTURE-GRAPH(unexpected)"
        c[key] += 1
    return dict(c)


setdiff = {
    "script_case": {
        "target": "gold:D_01.partner_analytics",
        "old_n": len(script_old), "new_n": len(script_new),
        "missing_n": len(script_missing), "extra_n": len(script_extra),
        "missing_members_with_edge_class": script_missing_classes,
        "edge_class_distribution": distribution(script_missing_classes),
        "extra_members": script_extra,
    },
    "function_control": {
        "target": "gold:D_01.partner_analytics:generate_header_metrics",
        "old_n": len(fn_old), "new_n": len(fn_new),
        "missing_n": len(fn_missing), "extra_n": len(fn_extra),
        "missing_members_with_edge_class": fn_missing_classes,
        "edge_class_distribution": distribution(fn_missing_classes),
        "extra_members": fn_extra,
    },
}
out_path2 = os.path.join(SP, "SETDIFF_20260725_result.json")
json.dump(setdiff, open(out_path2, "w"), indent=2)
print("=" * 70)
print("SET-DIFF script case:", len(script_missing), "missing /", len(script_old), "expected;",
      len(script_extra), "extra")
print("  edge-class distribution:", distribution(script_missing_classes))
print("SET-DIFF function control:", len(fn_missing), "missing /", len(fn_old), "expected;",
      len(fn_extra), "extra")
print("  edge-class distribution:", distribution(fn_missing_classes))
print("WROTE", out_path2)
