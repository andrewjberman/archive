#!/usr/bin/env python
"""
NFRA_GRAPHUNI P0-CVO no-regression fixture capture (layer a: the 4 structure-tools' pre-delta answers).
Deterministic + reproducible sample (top-K by degree per pipeline/class, id-ascending tie-break) so P2
regenerates the IDENTICAL sample and the comparison is a clean set-equality. Captured BEFORE any P1 mutation.
Author: 3.0.0_SA_CVO~B. Read-only (subprocess invocations of comp-* tools + a read of graph.json).
"""
from __future__ import annotations
import json, subprocess, collections, sys, os, hashlib

GJSON = ".comp-graph/graph.json"   # relative to cwd (workspace root)
g = json.load(open(GJSON))
nodes = g["nodes"]; edges = g["edges"]
built_at = g.get("built_at")

# ---- degree maps ----
calls_deg = collections.Counter()
s3io_deg = collections.Counter()
fetch_deg = collections.Counter()
for e in edges:
    t = e["edge_type"]
    if t == "CALLS":
        calls_deg[e["source"]] += 1; calls_deg[e["target"]] += 1
    elif t in ("READS_S3", "WRITES_S3"):
        s3io_deg[e["source"]] += 1; s3io_deg[e["target"]] += 1
    elif t == "FETCHES":
        fetch_deg[e["source"]] += 1; fetch_deg[e["target"]] += 1

def pipe(n):
    fp = (n.get("file_path","") + n.get("id",""))
    nid = n.get("id","")
    if "INF_" in nid or "/inf/" in fp or "inf/scripts" in fp: return "inf"
    if "black_diamond" in fp: return "bd"
    if "mdpf" in fp.lower(): return "mdpf"
    if "cot" in fp.lower(): return "cot"
    return "?"

gold = [n for n in nodes.values() if n["node_type"] == "GOLD_SCRIPT"]
fn = [n for n in gold if n.get("function_name")]
scr = [n for n in gold if not n.get("function_name")]

def topk(cands, degmap, k):
    # deterministic: sort by (-degree, id) ; id-ascending tie-break
    return [n["id"] for n in sorted(cands, key=lambda n: (-degmap[n["id"]], n["id"]))[:k]]

# ---- SAMPLE (deterministic selection rules) ----
sample = {}
sample["blast_fn_bd"]  = topk([n for n in fn if pipe(n)=="bd"],  calls_deg, 8)
sample["blast_fn_inf"] = topk([n for n in fn if pipe(n)=="inf"], calls_deg, 8)
sample["blast_script"] = topk(scr, s3io_deg, 6)
s3 = [n for n in nodes.values() if n["node_type"]=="S3_ARTIFACT"]
lam = [n for n in nodes.values() if n["node_type"]=="LAMBDA"]
endp = [n for n in nodes.values() if n["node_type"]=="ENDPOINT"]
evb = [n for n in nodes.values() if n["node_type"]=="EVENTBRIDGE"]
sample["s3_top"] = topk(s3, s3io_deg, 6)
sample["lambda_top"] = topk(lam, calls_deg, 3) or [n["id"] for n in sorted(lam, key=lambda n:n["id"])[:3]]
sample["endpoint_top"] = topk(endp, fetch_deg, 3) or [n["id"] for n in sorted(endp, key=lambda n:n["id"])[:3]]
sample["eventbridge_top"] = [n["id"] for n in sorted(evb, key=lambda n:n["id"])[:3]]

# xref symbols span classes: fn label, file_path, s3 key, lambda, endpoint
def label(nid): return nodes[nid]["label"] if nid in nodes else nid
xref_syms = []
for nid in (sample["blast_fn_bd"][:2] + sample["blast_fn_inf"][:2]):
    # use the bare function name (symbol), per xref symbol-lookup
    fnm = nodes[nid].get("function_name") or nodes[nid]["label"]
    xref_syms.append(fnm)
for nid in sample["blast_script"][:2]:
    xref_syms.append(nodes[nid].get("file_path") or nodes[nid]["label"])
for nid in sample["s3_top"][:2]:
    xref_syms.append(nodes[nid]["label"])
for nid in sample["lambda_top"][:1]:
    xref_syms.append(nodes[nid]["label"])
for nid in sample["endpoint_top"][:1]:
    xref_syms.append(nodes[nid]["label"])
sample["xref_symbols"] = xref_syms

# trace walks: top gold scripts + s3 artifacts, both directions
sample["trace_nodes"] = (sample["blast_fn_bd"][:2] + sample["blast_fn_inf"][:2] +
                          sample["blast_script"][:2] + sample["s3_top"][:2])

print("SAMPLE SIZES:", {k: len(v) for k, v in sample.items()})
for k, v in sample.items():
    print(f"\n[{k}] ({len(v)})")
    for x in v: print("   ", x)

# save the sample for the capture step
out = os.path.join(os.path.dirname(__file__), "sample.json")
json.dump({"sample": sample, "built_at": built_at,
           "node_counts": dict(collections.Counter(n["node_type"] for n in nodes.values())),
           "edge_counts": dict(collections.Counter(e["edge_type"] for e in edges))},
          open(out, "w"), indent=2)
print("\nwrote", out)
