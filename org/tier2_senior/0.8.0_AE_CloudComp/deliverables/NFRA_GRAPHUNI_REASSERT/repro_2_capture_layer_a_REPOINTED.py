#!/usr/bin/env python
"""
NFRA_GRAPHUNI P0-CVO no-regression fixture -- layer (a) RE-ASSERT, REPOINTED onto the
marker-head graph (comp_marker_read.py) per CVO~Z dispatch 20260725T055641Z.

Method: monkeypatch cli._get_graph() to return comp_marker_read.py's as_tracegraph()
projection instead of the local .comp-graph/graph.json cache, then drive the REAL
cli.main() / cmd_blast / cmd_trace / cmd_xref code paths in-process (sys.argv simulated,
stdout captured) -- so the answer-formatting logic is byte-identical to production, only
the graph SOURCE changes. comp-platinum is NOT re-pointed here: it does not consume
TraceGraph at all (separate routing/DAG/dataflow cache via graph_cache.py), so a clean
TraceGraph swap does not apply to it -- out of scope for this pass, flagged not silently
skipped.

Firm-aware S3 canonicalization per FIXTURE_ATTESTATION.md S7: each OLD (bucketless) s3 id
is expanded to its firm-qualified set via NFRA_GRAPHUNI.P1-D.bucketless_to_qualified.json
BEFORE the set-compare (a pre-canonicalization id-diff is noise, not a regression).

Reads the CVO fixture directory (org/tier1_exec/3.0.0_SA_CVO/NFRA_GRAPHUNI_P0-CVO_fixture/)
read-only -- never writes there (CVO-owned lane). All output lands in this script's own dir.

Author: 0.8.0_AE_CloudComp~D, per CVO~Z ruling (Andrew-direct "reopen it, have CVO deal
with it"). Read-only against the estate: only imports + in-process calls, zero writes
outside this script's own output file.
"""
from __future__ import annotations
import contextlib
import hashlib
import io
import json
import os
import re
import sys

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, WS)

from org.modules.graph import cli as cli_mod  # noqa: E402
from org.modules.graph import comp_marker_read as cmr  # noqa: E402

SP = os.path.dirname(__file__)
FIXTURE_DIR = os.path.join(WS, "org", "tier1_exec", "3.0.0_SA_CVO", "NFRA_GRAPHUNI_P0-CVO_fixture")

sample_doc = json.load(open(os.path.join(FIXTURE_DIR, "sample.deterministic.json")))
S = sample_doc["sample"]

bucketless_map = json.load(open(os.path.join(
    WS, "org", "projects", "NFRA_GRAPHUNI", "NFRA_GRAPHUNI.P1-D.bucketless_to_qualified.json")))

# ---------------------------------------------------------------------------
# 1. Load the marker-head graph, monkeypatch cli._get_graph to return it.
# ---------------------------------------------------------------------------
mh = cmr.load_marker_head_graph()
G = mh.as_tracegraph()
print(f"MARKER-HEAD GRAPH: marker_head={mh.provenance.get('marker_head')} "
      f"built_at={mh.provenance.get('built_at')} nodes={len(G.nodes)} edges={len(G.edges)}",
      file=sys.stderr)

_orig_get_graph = cli_mod._get_graph
cli_mod._get_graph = lambda force_rebuild=False, check_freshness=True: G


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]


def canon_s3(old_id: str) -> set:
    """Expand a fixture (bucketless, pre-delta) s3 id to its firm-qualified candidate set.
    A non-s3 id passes through unchanged. Per S7: this MUST run before the set-compare."""
    if not old_id.startswith("s3:"):
        return {old_id}
    quals = bucketless_map.get(old_id)
    if not quals:
        return {old_id}  # not in the map -- leave as-is, will show as a real miss if genuinely gone
    return {"s3:" + q for q in quals}


def canon_id_set(ids) -> set:
    out = set()
    for i in ids:
        out |= canon_s3(i)
    return out


def run_cli(argv) -> tuple[str, int]:
    """Call cli.main() in-process with argv simulated; capture stdout; catch SystemExit."""
    old_argv = sys.argv
    sys.argv = ["cli.py"] + argv
    buf = io.StringIO()
    rc = 0
    try:
        with contextlib.redirect_stdout(buf):
            cli_mod.main()
    except SystemExit as e:
        rc = e.code if isinstance(e.code, int) else (1 if e.code else 0)
    finally:
        sys.argv = old_argv
    return buf.getvalue(), rc


fixture = json.load(open(os.path.join(FIXTURE_DIR, "fixture_layer_a.tool_answers.json")))
old = fixture["tool"]
report = {"comp-blast": {}, "comp-trace": {}, "comp-xref": {}}
match_count = {"comp-blast": 0, "comp-trace": 0, "comp-xref": 0}
total_count = {"comp-blast": 0, "comp-trace": 0, "comp-xref": 0}

# ---------------------------------------------------------------------------
# comp-blast
# ---------------------------------------------------------------------------
blast_targets = S["blast_fn_bd"] + S["blast_fn_inf"] + S["blast_script"] + S["s3_top"]
for tgt in blast_targets:
    out, rc = run_cli(["blast", tgt, "--json", "--direction", "both"])
    total_count["comp-blast"] += 1
    old_entry = old["comp-blast"].get(tgt, {})
    old_ids = set(old_entry.get("radius_ids", []))
    old_ids_canon = canon_id_set(old_ids)
    try:
        d = json.loads(out)
        new_ids = set()
        for bucket in ("consumers", "producers"):
            for cls, lst in (d.get(bucket) or {}).items():
                for it in lst:
                    new_ids.add(it["id"])
    except Exception as e:
        report["comp-blast"][tgt] = {"status": "PARSE-ERROR", "rc": rc, "err": str(e), "raw_tail": out[-300:]}
        continue
    new_ids_canon = canon_id_set(new_ids)
    match = (old_ids_canon == new_ids_canon)
    if match:
        match_count["comp-blast"] += 1
    report["comp-blast"][tgt] = {
        "status": "MATCH" if match else "MISMATCH",
        "old_n": len(old_ids), "new_n": len(new_ids),
        "old_n_canon": len(old_ids_canon), "new_n_canon": len(new_ids_canon),
        "missing_from_new": sorted(old_ids_canon - new_ids_canon)[:20],
        "extra_in_new": sorted(new_ids_canon - old_ids_canon)[:20],
    }

# ---------------------------------------------------------------------------
# comp-trace
# ---------------------------------------------------------------------------
def trace_ids(out):
    try:
        d = json.loads(out)
    except Exception:
        return None
    res = d.get("results", [])
    return sorted({(r["id"] if isinstance(r, dict) and "id" in r else
                    (r if isinstance(r, str) else json.dumps(r, sort_keys=True))) for r in res})

for node in S["trace_nodes"]:
    total_count["comp-trace"] += 1
    up_out, _ = run_cli(["trace", node, "--json", "--direction", "up", "--all"])
    down_out, _ = run_cli(["trace", node, "--json", "--direction", "down", "--all"])
    up_new = trace_ids(up_out)
    down_new = trace_ids(down_out)
    old_entry = old["comp-trace"].get(node, {})
    up_old = set(old_entry.get("up", {}).get("ids", []) or [])
    down_old = set(old_entry.get("down", {}).get("ids", []) or [])
    up_new_c = canon_id_set(up_new or [])
    down_new_c = canon_id_set(down_new or [])
    up_old_c = canon_id_set(up_old)
    down_old_c = canon_id_set(down_old)
    match = (up_old_c == up_new_c) and (down_old_c == down_new_c)
    if match:
        match_count["comp-trace"] += 1
    report["comp-trace"][node] = {
        "status": "MATCH" if match else "MISMATCH",
        "up_old_n": len(up_old), "up_new_n": len(up_new or []),
        "down_old_n": len(down_old), "down_new_n": len(down_new or []),
        "up_missing": sorted(up_old_c - up_new_c)[:15], "up_extra": sorted(up_new_c - up_old_c)[:15],
        "down_missing": sorted(down_old_c - down_new_c)[:15], "down_extra": sorted(down_new_c - down_old_c)[:15],
    }

# ---------------------------------------------------------------------------
# comp-xref
# ---------------------------------------------------------------------------
xref_syms = []
for s in S["xref_symbols"]:
    if s not in xref_syms:
        xref_syms.append(s)
for sym in xref_syms:
    total_count["comp-xref"] += 1
    out, rc = run_cli(["xref", sym])
    m = re.search(r"\((\d+)\s+node\(s\),\s*(\d+)\s+edge\(s\)\s+matched\)", out)
    ncount = int(m.group(1)) if m else None
    node_ids = sorted(set(re.findall(r"\b((?:gold|s3|lambda|endpoint|eventbridge|component):[^\s]+)", out)))
    old_entry = old["comp-xref"].get(sym, {})
    old_ids = set(old_entry.get("matched_node_ids", []))
    old_ids_canon = canon_id_set(old_ids)
    new_ids_canon = canon_id_set(node_ids)
    match = (old_ids_canon == new_ids_canon)
    if match:
        match_count["comp-xref"] += 1
    report["comp-xref"][sym] = {
        "status": "MATCH" if match else "MISMATCH",
        "old_node_count": old_entry.get("node_count"), "new_node_count": ncount,
        "missing_from_new": sorted(old_ids_canon - new_ids_canon)[:15],
        "extra_in_new": sorted(new_ids_canon - old_ids_canon)[:15],
    }

cli_mod._get_graph = _orig_get_graph  # restore

# ---------------------------------------------------------------------------
# Summary + the specifically-requested sharp case
# ---------------------------------------------------------------------------
summary = {
    "marker_head": mh.provenance.get("marker_head"),
    "marker_head_built_at": mh.provenance.get("built_at"),
    "per_tool": {t: f"{match_count[t]}/{total_count[t]}" for t in match_count},
    "total": f"{sum(match_count.values())}/{sum(total_count.values())}",
    "comp_platinum": "NOT RE-POINTED THIS PASS -- separate routing/DAG/dataflow cache (graph_cache.py), does not consume TraceGraph, a clean swap does not apply; see script docstring.",
}
sharp_case_script = report["comp-blast"].get("gold:D_01.partner_analytics", {})
sharp_case_fn = report["comp-blast"].get("gold:D_01.partner_analytics:generate_header_metrics", {})

out_path = os.path.join(SP, "REASSERT_20260725_result.json")
json.dump({"summary": summary, "per_target": report,
           "sharp_case_script_gold:D_01.partner_analytics": sharp_case_script,
           "sharp_case_fn_gold:D_01.partner_analytics:generate_header_metrics": sharp_case_fn},
          open(out_path, "w"), indent=2)

print("=" * 70)
print("SUMMARY:", json.dumps(summary, indent=2))
print("=" * 70)
print("SHARP CASE gold:D_01.partner_analytics (script, expected 216):", json.dumps(sharp_case_script, indent=2)[:2000])
print("SHARP CASE gold:D_01.partner_analytics:generate_header_metrics (fn, expected 39):", json.dumps(sharp_case_fn, indent=2)[:1500])
print("WROTE", out_path)
