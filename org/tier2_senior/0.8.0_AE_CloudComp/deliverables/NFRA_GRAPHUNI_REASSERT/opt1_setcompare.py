#!/usr/bin/env python
"""
NFRA_GRAPHUNI OPT1-BUILD step 3 -- member-level SET-COMPARE of the fresh
--full producer artifact against the P0-CVO fixture.

Reconstructs a real TraceGraph object from gold_compute_producer_FULL_20260725.json
(inverting the producer's own id-canonicalization and flipping READS_S3 polarity --
the producer emits script->s3 with pipeline:<firm>:gold:* ids; the fixture/build_graph
convention is s3->script with gold:* ids, per extract_s3.py:453-455), then drives the
SAME real cli.main() blast/trace/xref code (monkeypatched _get_graph, argv simulated,
stdout captured) used for the marker-head re-assert -- so this is a genuine per-target
SHA/set-equality test against fixture_layer_a.tool_answers.json, not a count comparison.

Author: 0.8.0_AE_CloudComp~D, per CTO~Z dispatch NFRA_GRAPHUNI OPT1-BUILD (20260725T064248Z)
+ supplement (20260725T064432Z: per-target SHA equality, not aggregate totals; verdict
line states PROVEN/REFUTED explicitly).
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
from org.modules.graph.trace_graph import Edge, Node, TraceGraph  # noqa: E402

SP = os.path.dirname(__file__)
FIXTURE_DIR = os.path.join(WS, "org", "tier1_exec", "3.0.0_SA_CVO", "NFRA_GRAPHUNI_P0-CVO_fixture")
PRODUCER_JSON = os.path.join(SP, "gold_compute_producer_FULL_20260725.json")

sample_doc = json.load(open(os.path.join(FIXTURE_DIR, "sample.deterministic.json")))
S = sample_doc["sample"]
fixture = json.load(open(os.path.join(FIXTURE_DIR, "fixture_layer_a.tool_answers.json")))
old = fixture["tool"]

# ---------------------------------------------------------------------------
# 1. Reconstruct a TraceGraph from the producer's own output, inverting its own
#    _pipeline_id() transform (source-grounded: extract_gold_compute.py:47-51) and
#    flipping READS_S3 polarity to match build_graph's own convention.
# ---------------------------------------------------------------------------
doc = json.load(open(PRODUCER_JSON))
PIPELINE_RE = re.compile(r"^pipeline:[a-z_]+:gold:(.+)$")


def un_pipeline_id(pid: str) -> str | None:
    m = PIPELINE_RE.match(pid)
    return ("gold:" + m.group(1)) if m else None


def un_s3_id(target: str) -> str | None:
    # "opal-data-<firm>/<key>" -> "s3:<key>" (strip the bucket-qualification the producer
    # adds at extract_gold_compute.py:140: `"opal-data-%s/%s" % (owner_firm, key)`)
    m = re.match(r"^opal-data-[a-z]+/(.+)$", target)
    return ("s3:" + m.group(1)) if m else None


g = TraceGraph(built_at=0.0)
node_ids_added = set()


def ensure_node(nid: str, ntype: str):
    if nid in node_ids_added:
        return
    node_ids_added.add(nid)
    g.add_node(Node(id=nid, node_type=ntype, label=nid))


skipped_edges = {"CONTAINS": 0, "unmapped_node": 0}
for e in doc["edges"]:
    et = e["edge_type"]
    if et == "CONTAINS":
        skipped_edges["CONTAINS"] += 1  # not a TraceGraph/fixture edge type -- GRAPHDEPTH-only
        continue
    src_raw, tgt_raw = e["source"], e["target"]
    if et in ("CALLS",):
        s = un_pipeline_id(src_raw)
        t = un_pipeline_id(tgt_raw)
        if not (s and t):
            skipped_edges["unmapped_node"] += 1
            continue
        ensure_node(s, "GOLD_SCRIPT")
        ensure_node(t, "GOLD_SCRIPT")
        g.add_edge(Edge(source=s, target=t, edge_type="CALLS"))
    elif et == "WRITES_S3":
        s = un_pipeline_id(src_raw)          # script/fn
        t = un_s3_id(tgt_raw)                # s3 key
        if not (s and t):
            skipped_edges["unmapped_node"] += 1
            continue
        ensure_node(s, "GOLD_SCRIPT")
        ensure_node(t, "S3_ARTIFACT")
        g.add_edge(Edge(source=s, target=t, edge_type="WRITES_S3"))
    elif et == "READS_S3":
        s = un_pipeline_id(src_raw)          # script/fn (producer polarity: script->s3)
        t = un_s3_id(tgt_raw)                # s3 key
        if not (s and t):
            skipped_edges["unmapped_node"] += 1
            continue
        ensure_node(s, "GOLD_SCRIPT")
        ensure_node(t, "S3_ARTIFACT")
        # POLARITY FLIP (CTO~Z 20260725T064248Z): fixture/build_graph convention is
        # s3 -> script (extract_s3.py:453-455), producer emits script -> s3. Flip here.
        g.add_edge(Edge(source=t, target=s, edge_type="READS_S3"))

print(f"RECONSTRUCTED TraceGraph: nodes={len(g.nodes)} edges={len(g.edges)} "
      f"skipped={skipped_edges}", file=sys.stderr)

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


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# 2. Per-target SET-COMPARE, comp-blast only (the dimension this dispatch is scoped to --
#    CALLS/READS_S3/WRITES_S3 are what the producer emits; comp-trace/xref would need the
#    same reconstruction and are not re-derived here -- named as a boundary, not skipped
#    silently).
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
    match = (old_ids == new_ids)  # NOTE: no S3 bucket-qualification issue here -- both sides
    # are already in the SAME bucketless "s3:<key>" form (fixture is bucketless natively;
    # this reconstruction deliberately un-qualifies back to bucketless, so no expand-before-
    # compare step is needed on THIS axis -- different from the marker-head re-assert, which
    # compared against BUCKET-QUALIFIED kuzu ids and needed the firm-aware expansion).
    if match:
        match_n += 1
    report[tgt] = {
        "status": "MATCH" if match else "MISMATCH",
        "old_n": len(old_ids), "new_n": len(new_ids),
        "missing_from_new": sorted(old_ids - new_ids)[:25],
        "extra_in_new": sorted(new_ids - old_ids)[:25],
    }

cli_mod._get_graph = _orig_get_graph

sharp_script = report.get("gold:D_01.partner_analytics", {})
sharp_fn = report.get("gold:D_01.partner_analytics:generate_header_metrics", {})
verdict = "SET-IDENTITY PROVEN" if match_n == len(blast_targets) else "SET-IDENTITY REFUTED"

summary = {
    "verdict": verdict,
    "match": f"{match_n}/{len(blast_targets)}",
    "reconstructed_graph": {"nodes": len(g.nodes), "edges": len(g.edges), "skipped": skipped_edges},
    "scope_note": "comp-blast only this pass (the producer emits CALLS/READS_S3/WRITES_S3, the edges comp-blast consumes); comp-trace/comp-xref would need the same reconstruction, not re-derived here -- named boundary, not silent gap.",
    "sharp_case_script_gold:D_01.partner_analytics": sharp_script,
    "sharp_case_fn": sharp_fn,
}

out_path = os.path.join(SP, "OPT1_SETCOMPARE_20260725_result.json")
json.dump({"summary": summary, "per_target": report}, open(out_path, "w"), indent=2)
print("=" * 70)
print("VERDICT:", verdict, "--", summary["match"])
print(json.dumps(summary, indent=2)[:3000])
print("WROTE", out_path)
