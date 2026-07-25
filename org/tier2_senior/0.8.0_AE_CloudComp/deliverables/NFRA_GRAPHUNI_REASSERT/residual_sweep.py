#!/usr/bin/env python
"""
NFRA_GRAPHUNI RESIDUAL-SWEEP -- set-diff ALL 17 v2 strict-equality failures (not just the
sharp case), STRICT-predicate edge-class partition (out-of-scope only if a member carries
NO in-scope edge class at all -- CVO~Z's corrected predicate, conceded), plus 2 more
function-level controls beyond generate_header_metrics.

Reuses the v2 (node-order-fixed) reconstruction exactly -- same assert-before-trust gate.

Author: 0.8.0_AE_CloudComp~D, per CTO~Z dispatch NFRA_GRAPHUNI RESIDUAL-SWEEP (20260725T070657Z).
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import re
import sys
from collections import Counter
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


# --- v2 reconstruction: nodes first (preserves script-before-function order), then edges ---
g = TraceGraph(built_at=0.0)
for n in doc["nodes"]:
    canon = un_pipeline_id(n["id"])
    if canon and canon not in g.nodes:
        g.add_node(Node(id=canon, node_type="GOLD_SCRIPT", label=canon))

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
            g.add_edge(Edge(source=s, target=t, edge_type="WRITES_S3"))
    elif et == "READS_S3":
        s, t = un_pipeline_id(s_raw), un_s3_id(t_raw)
        if s and t:
            if t not in g.nodes:
                g.add_node(Node(id=t, node_type="S3_ARTIFACT", label=t))
            g.add_edge(Edge(source=t, target=s, edge_type="READS_S3"))

m0 = g.find_node("gold:D_01.partner_analytics")
assert m0 and m0[0].id == "gold:D_01.partner_analytics", "node-order fix regressed"
print(f"RECONSTRUCTED: nodes={len(g.nodes)} edges={len(g.edges)}; fix-assert PASSED", file=sys.stderr)

if not g._indexed:
    g._build_index()
fixture_graph = TraceGraph.load(Path(os.path.join(FIXTURE_DIR, "graph.json.pinned_predelta")))
if not fixture_graph._indexed:
    fixture_graph._build_index()

_orig_get_graph = cli_mod._get_graph
cli_mod._get_graph = lambda force_rebuild=False, check_freshness=True: g


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


def edge_classes_into(node_id, tg):
    return sorted({e.edge_type for e in tg._reverse.get(node_id, [])} |
                  {e.edge_type for e in tg._forward.get(node_id, [])})


IN_SCOPE = {"CALLS", "READS_S3", "WRITES_S3"}   # this producer's own coverage.slices_scanned

# ---------------------------------------------------------------------------
# ALL 17 v2 failures -- reuse the same enumeration the v2 aggregate pass already proved.
# ---------------------------------------------------------------------------
v2_result = json.load(open(os.path.join(SP, "OPT1_SETCOMPARE_v2_result.json")))
failing_targets = [k for k, v in v2_result["per_target"].items() if v.get("status") == "MISMATCH"]
print(f"failing targets to sweep: {len(failing_targets)}", file=sys.stderr)

per_target = {}
strict_out_of_scope_total = 0
strict_in_scope_total = 0
class_counter = Counter()

for tgt in failing_targets:
    new_ids = blast_ids(tgt)
    old_ids = set(old["comp-blast"].get(tgt, {}).get("radius_ids", []))
    missing = sorted(old_ids - new_ids)
    extra = sorted(new_ids - old_ids)
    missing_classes = {nid: edge_classes_into(nid, fixture_graph) for nid in missing}
    strict_out = [nid for nid, cls in missing_classes.items() if cls and not (set(cls) & IN_SCOPE)]
    strict_in = [nid for nid, cls in missing_classes.items() if (set(cls) & IN_SCOPE) or not cls]
    strict_out_of_scope_total += len(strict_out)
    strict_in_scope_total += len(strict_in)
    for cls in missing_classes.values():
        class_counter[",".join(cls) if cls else "NONE"] += 1
    per_target[tgt] = {
        "old_n": len(old_ids), "new_n": len(new_ids),
        "missing_n": len(missing), "extra_n": len(extra),
        "coverage_pct": round(100 * (len(old_ids) - len(missing)) / len(old_ids), 1) if old_ids else None,
        "missing_members_with_edge_class": missing_classes,
        "strict_out_of_scope_n": len(strict_out), "strict_in_scope_n": len(strict_in),
        "extra_members": extra,
    }

cli_mod._get_graph = _orig_get_graph

# ---------------------------------------------------------------------------
# Function-level controls: generate_header_metrics (already run in prior passes) + 2 more.
# ---------------------------------------------------------------------------
cli_mod._get_graph = lambda force_rebuild=False, check_freshness=True: g
controls = ["gold:D_01.partner_analytics:generate_header_metrics",
            "gold:D_02.advisor_client_detail:main",
            "gold:INF_D_02.advisor_client_detail:build_advisor_books"]
control_results = {}
for c in controls:
    new_ids = blast_ids(c)
    old_ids = set(old["comp-blast"].get(c, {}).get("radius_ids", []))
    missing = sorted(old_ids - new_ids)
    extra = sorted(new_ids - old_ids)
    control_results[c] = {"old_n": len(old_ids), "new_n": len(new_ids),
                          "missing_n": len(missing), "extra_n": len(extra),
                          "missing": missing, "extra": extra}
cli_mod._get_graph = _orig_get_graph

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
coverages = [v["coverage_pct"] for v in per_target.values() if v["coverage_pct"] is not None]
summary = {
    "n_targets_swept": len(failing_targets),
    "coverage_pct_per_target_sorted": sorted(coverages),
    "coverage_min": min(coverages) if coverages else None,
    "coverage_max": max(coverages) if coverages else None,
    "coverage_median": sorted(coverages)[len(coverages) // 2] if coverages else None,
    "strict_predicate_out_of_scope_total": strict_out_of_scope_total,
    "strict_predicate_in_scope_total": strict_in_scope_total,
    "edge_class_distribution_all_missing": dict(class_counter),
    "function_controls_all_clean": all(v["missing_n"] == 0 and v["extra_n"] == 0 for v in control_results.values()),
    "function_controls": control_results,
}

out_path = os.path.join(SP, "RESIDUAL_SWEEP_result.json")
json.dump({"summary": summary, "per_target": per_target}, open(out_path, "w"), indent=2)
print("=" * 70)
print("COVERAGE PER TARGET (sorted):", sorted(coverages))
print("STRICT in-scope total:", strict_in_scope_total, "| out-of-scope total:", strict_out_of_scope_total)
print("FUNCTION CONTROLS all clean:", summary["function_controls_all_clean"])
print("WROTE", out_path)
