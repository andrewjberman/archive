#!/usr/bin/env python
"""
NFRA_GRAPHUNI CANON-WALK -- re-run reachability with INTERMEDIATE-node canonicalization,
not just terminal ids. Per CVO~Z's ruling: v1/v2 canonicalized terminal blast-radius
targets correctly, but the BFS itself walks intermediate nodes that were never
normalized -- a path crossing a glob-form node (fixture uses `{*}`, producer emits none)
or the unqualified cross-firm bridge key cannot resolve regardless of producer
completeness.

TWO NORMALIZATIONS, bidirectional, applied to every node touched during traversal:
1. glob<->prefix: a fixture node `s3:<dir>/{*}<ext>` is bridged to every producer S3 node
   sharing the same directory stem + extension (a real object key the glob would match).
   Implemented as ALIAS EDGES added to the producer edge set before BFS: for every
   producer S3 edge whose key matches a fixture glob's stem, an identical edge is added
   using the glob-form id as well -- so the existing (unmodified) BFS can traverse through
   the glob id transparently.
2. unqualified<->firm-qualified: VERIFIED, not newly built -- this reconstruction's
   un_s3_id() already strips the firm-prefix on every S3 edge uniformly (terminal AND
   intermediate, since it's applied at edge-construction time, not query time), so a key
   written by one firm and read by another already collapses onto ONE canonical node.
   Confirmed empirically below rather than assumed.

PREDICTION (CVO~Z's, stated so it can falsify, carried into this script per the two-commit
provenance standard -- this file states the prediction; the result file is written by a
SEPARATE run after this file is committed): the gap shrinks again and class A (glob-form
key identity) largely dissolves. If it does not shrink, the producer has a real
structural deficit.

Author: 0.8.0_AE_CloudComp~D, per CTO~Z dispatch NFRA_GRAPHUNI CANON-WALK (20260725T072855Z).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

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


def un_pipeline_id(pid):
    m = PIPELINE_RE.match(pid)
    return ("gold:" + m.group(1)) if m else None


def un_s3_id(target):
    m = re.match(r"^opal-data-[a-z]+/(.+)$", target)
    return ("s3:" + m.group(1)) if m else None


def glob_stem(glob_id: str):
    """s3:silver/allocations/{*}.parquet -> ('silver/allocations/', '.parquet')"""
    body = glob_id[len("s3:"):]
    if "{*}" not in body:
        return None
    prefix, _, suffix = body.partition("{*}")
    return prefix, suffix


# ---------------------------------------------------------------------------
# Fixture glob nodes (the identity gap CVO~Z sized at 76).
# ---------------------------------------------------------------------------
fixture_graph = TraceGraph.load(Path(os.path.join(FIXTURE_DIR, "graph.json.pinned_predelta")))
if not fixture_graph._indexed:
    fixture_graph._build_index()
glob_nodes = [nid for nid in fixture_graph.nodes if "{*}" in nid]
print(f"fixture glob nodes: {len(glob_nodes)}", file=sys.stderr)

# ---------------------------------------------------------------------------
# Reconstruct v2 graph (node-order-fixed), THEN add glob-bridge alias edges.
# ---------------------------------------------------------------------------
g = TraceGraph(built_at=0.0)
for n in doc["nodes"]:
    canon = un_pipeline_id(n["id"])
    if canon and canon not in g.nodes:
        g.add_node(Node(id=canon, node_type="GOLD_SCRIPT", label=canon))

s3_nodes_seen = set()
for e in doc["edges"]:
    et = e["edge_type"]
    if et == "CONTAINS":
        continue
    s_raw, t_raw = e["source"], e["target"]
    if et == "CALLS":
        s, t = un_pipeline_id(s_raw), un_pipeline_id(t_raw)
        if s and t:
            g.add_edge(Edge(source=s, target=t, edge_type="CALLS"))
    elif et == "WRITES_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if s and t:
            if t not in g.nodes:
                g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
            s3_nodes_seen.add(t)
            g.add_edge(Edge(source=s, target=t, edge_type="WRITES_S3"))
    elif et == "READS_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if s and t:
            if t not in g.nodes:
                g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
            s3_nodes_seen.add(t)
            g.add_edge(Edge(source=t, target=s, edge_type="READS_S3"))

m0 = g.find_node("gold:D_01.partner_analytics")
assert m0 and m0[0].id == "gold:D_01.partner_analytics", "node-order fix regressed"

# --- VERIFY normalization 2 (unqualified<->firm-qualified) is already native ---
# The canonical_prices.parquet convergence key: does ONE node carry writer edges from
# BOTH firms already (proving un_s3_id's uniform stripping already bridges firms)?
target_key = "s3:silver/prices/canonical_prices.parquet"
writers_into_target = [e.source for e in g._reverse.get(target_key, [])] if g._indexed or True else []
if not g._indexed:
    g._build_index()
writers_into_target = [e.source for e in g._reverse.get(target_key, [])]
firms_seen = set()
for w in writers_into_target:
    if w.startswith("gold:INF_"):
        firms_seen.add("inf")
    elif w.startswith("gold:"):
        firms_seen.add("bd-or-other")
print(f"NORMALIZATION-2 CHECK: {target_key} has {len(writers_into_target)} writer(s) in ONE node; "
      f"firms represented: {firms_seen} -- {'ALREADY BRIDGED (native)' if len(firms_seen) > 1 else 'not multi-firm here'}",
      file=sys.stderr)

# --- normalization 1: glob-stem alias edges ---
alias_edges_added = 0
for glob_id in glob_nodes:
    stem = glob_stem(glob_id)
    if not stem:
        continue
    prefix, suffix = stem
    matched_literal_key = f"s3:{prefix}"  # match by directory prefix, extension optional-strict below
    for s3_node in list(s3_nodes_seen):
        body = s3_node[len("s3:"):]
        if body.startswith(prefix) and (not suffix or body.endswith(suffix)):
            # alias: copy every edge touching s3_node onto glob_id too
            if glob_id not in g.nodes:
                g.add_node(Node(id=glob_id, node_type="S3_ARTIFACT", label=glob_id))
            for e in list(g._forward.get(s3_node, [])):
                g.add_edge(Edge(source=glob_id, target=e.target, edge_type=e.edge_type))
                alias_edges_added += 1
            for e in list(g._reverse.get(s3_node, [])):
                g.add_edge(Edge(source=e.source, target=glob_id, edge_type=e.edge_type))
                alias_edges_added += 1

g._indexed = False
if not g._indexed:
    g._build_index()
print(f"GLOB-BRIDGE: {alias_edges_added} alias edges added across {len(glob_nodes)} glob node targets",
      file=sys.stderr)

_orig_get_graph = cli_mod._get_graph
cli_mod._get_graph = lambda force_rebuild=False, check_freshness=True: g


import contextlib  # noqa: E402
import io  # noqa: E402


def run_cli(argv):
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


def blast_ids(target):
    out, _ = run_cli(["blast", target, "--json", "--direction", "both"])
    d = json.loads(out)
    ids = set()
    for bucket in ("consumers", "producers"):
        for cls, lst in (d.get(bucket) or {}).items():
            for it in lst:
                ids.add(it["id"])
    return ids


# ---------------------------------------------------------------------------
# Full 28-target re-assert with the canonicalized (glob-bridged) walk.
# ---------------------------------------------------------------------------
blast_targets = S["blast_fn_bd"] + S["blast_fn_inf"] + S["blast_script"] + S["s3_top"]
per_target = {}
match_n = 0
for tgt in blast_targets:
    new_ids = blast_ids(tgt)
    old_ids = set(old["comp-blast"].get(tgt, {}).get("radius_ids", []))
    # strip glob-alias artifacts from the comparison id set: a glob id appearing in new_ids
    # that also appears in old_ids is a legitimate match; glob ids are real fixture ids so
    # no special handling needed beyond normal set comparison.
    match = (old_ids == new_ids)
    if match:
        match_n += 1
    per_target[tgt] = {
        "old_n": len(old_ids), "new_n": len(new_ids),
        "missing_n": len(old_ids - new_ids), "extra_n": len(new_ids - old_ids),
        "status": "MATCH" if match else "MISMATCH",
    }

verdict = "SET-IDENTITY PROVEN" if match_n == len(blast_targets) else "SET-IDENTITY REFUTED"
print("=" * 70)
print(f"CANON-WALK v3 VERDICT: {verdict} {match_n}/{len(blast_targets)}")

# --- sharp case + control, full missing-member detail ---
def full_report(target):
    new_ids = blast_ids(target)
    old_ids = set(old["comp-blast"].get(target, {}).get("radius_ids", []))
    return {"old_n": len(old_ids), "new_n": len(new_ids),
            "missing": sorted(old_ids - new_ids), "extra": sorted(new_ids - old_ids)}


sharp = full_report("gold:D_01.partner_analytics")
control = full_report("s3:gold/timeseries/client_performance.parquet")
cli_mod._get_graph = _orig_get_graph

print(f"SHARP CASE: old_n={sharp['old_n']} new_n={sharp['new_n']} missing={len(sharp['missing'])}")
print(f"CONTROL TARGET: old_n={control['old_n']} new_n={control['new_n']} missing={len(control['missing'])}")

out_path = os.path.join(SP, "CANON_WALK_result.json")
json.dump({
    "verdict": verdict, "match": f"{match_n}/{len(blast_targets)}",
    "glob_nodes_in_fixture": len(glob_nodes), "alias_edges_added": alias_edges_added,
    "normalization_2_native_check": {"target_key": target_key,
                                      "writer_count": len(writers_into_target),
                                      "firms": sorted(firms_seen)},
    "per_target": per_target,
    "sharp_case": sharp, "control_target": control,
}, open(out_path, "w"), indent=2)
print("WROTE", out_path)
