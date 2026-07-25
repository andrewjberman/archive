import sys
import os

WS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, WS)

import json  # noqa: E402
import re  # noqa: E402

from org.modules.graph.trace_graph import Edge, Node, TraceGraph  # noqa: E402

SP = os.path.dirname(__file__)
doc = json.load(open(os.path.join(SP, "gold_compute_producer_FULL_20260725.json")))

PIPELINE_RE = re.compile(r"^pipeline:[a-z_]+:gold:(.+)$")


def un_pipeline_id(pid):
    m = PIPELINE_RE.match(pid)
    return ("gold:" + m.group(1)) if m else None


def un_s3_id(target):
    m = re.match(r"^opal-data-[a-z]+/(.+)$", target)
    return ("s3:" + m.group(1)) if m else None


g = TraceGraph(built_at=0.0)
seen = set()


def ensure_node(nid, ntype):
    if nid in seen:
        return
    seen.add(nid)
    g.add_node(Node(id=nid, node_type=ntype, label=nid))


for e in doc["edges"]:
    et = e["edge_type"]
    if et == "CONTAINS":
        continue
    src_raw, tgt_raw = e["source"], e["target"]
    if et == "CALLS":
        s, t = un_pipeline_id(src_raw), un_pipeline_id(tgt_raw)
        if not (s and t):
            continue
        ensure_node(s, "GOLD_SCRIPT")
        ensure_node(t, "GOLD_SCRIPT")
        g.add_edge(Edge(source=s, target=t, edge_type="CALLS"))
    elif et == "WRITES_S3":
        s, t = un_pipeline_id(src_raw), un_s3_id(tgt_raw)
        if not (s and t):
            continue
        ensure_node(s, "GOLD_SCRIPT")
        ensure_node(t, "S3_ARTIFACT")
        g.add_edge(Edge(source=s, target=t, edge_type="WRITES_S3"))
    elif et == "READS_S3":
        s, t = un_pipeline_id(src_raw), un_s3_id(tgt_raw)
        if not (s and t):
            continue
        ensure_node(s, "GOLD_SCRIPT")
        ensure_node(t, "S3_ARTIFACT")
        g.add_edge(Edge(source=t, target=s, edge_type="READS_S3"))

matches = g.find_node("gold:D_01.partner_analytics")
print("total matches:", len(matches))
print("matches[0] id:", matches[0].id, "| node_type:", matches[0].node_type)
print("first 5 match ids:", [m.id for m in matches[:5]])
script_id = "gold:D_01.partner_analytics"
idx_in_dict = list(g.nodes.keys()).index(script_id) if script_id in g.nodes else -1
print("exact script node present:", script_id in g.nodes, "| insertion index:", idx_in_dict, "of", len(g.nodes))
