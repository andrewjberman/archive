#!/usr/bin/env python
"""
NFRA_GRAPHUNI P0-CVO no-regression fixture -- layer (a) CAPTURE.
Runs the 4 structure-tools over the deterministic sample, freezes answers in SET-FORM
(order-independent) so P2's post-re-point set-equality comparison is clean.
Read-only: only subprocess invocations of the comp-* tools + a read of graph.json.
Author: 3.0.0_SA_CVO~B.
"""
from __future__ import annotations
import json, subprocess, collections, os, re, hashlib, sys

SP = os.path.dirname(__file__)
sample_doc = json.load(open(os.path.join(SP, "sample.json")))
S = sample_doc["sample"]
g = json.load(open(".comp-graph/graph.json"))
nodes = g["nodes"]

CLI = ["python", "org/modules/graph/cli.py"]
PLAT = ["python", "org/modules/graph/platinum_cli.py"]
def run(args, timeout=120):
    p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, shell=False)
    return p.stdout, p.stderr, p.returncode

def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()[:16]

fixture = {"tool": {}, "meta": {}}

# ---------- comp-blast (full set) ----------
blast = {}
blast_targets = S["blast_fn_bd"] + S["blast_fn_inf"] + S["blast_script"] + S["s3_top"]
for tgt in blast_targets:
    out, err, rc = run(CLI + ["blast", tgt, "--json", "--direction", "both"])
    try:
        d = json.loads(out)
    except Exception as e:
        blast[tgt] = {"error": f"parse:{e}", "rc": rc, "stderr_tail": err[-200:]}
        continue
    ids = set()
    for bucket in ("consumers", "producers"):
        for cls, lst in (d.get(bucket) or {}).items():
            for it in lst:
                ids.add(it["id"])
    blast[tgt] = {"radius_ids": sorted(ids), "n": len(ids), "sha": sha(sorted(ids))}
fixture["tool"]["comp-blast"] = blast

# ---------- comp-trace (up-set + down-set, separate runs) ----------
trace = {}
def trace_results(node, direction):
    out, err, rc = run(CLI + ["trace", node, "--json", "--direction", direction, "--all"])
    try:
        d = json.loads(out)
    except Exception as e:
        return {"error": f"parse:{e}", "rc": rc}
    res = d.get("results", [])
    ids = sorted({(r.get("id") or r.get("node") or r) if not isinstance(r, str) else r for r in res}) if res else []
    # results may be list of dicts or strings; normalize to id strings
    norm = sorted({(r["id"] if isinstance(r, dict) and "id" in r else (r if isinstance(r, str) else json.dumps(r, sort_keys=True))) for r in res})
    return {"ids": norm, "n": len(norm)}
for node in S["trace_nodes"]:
    up = trace_results(node, "up")
    down = trace_results(node, "down")
    trace[node] = {"up": up, "down": down, "sha": sha([up, down])}
fixture["tool"]["comp-trace"] = trace

# ---------- comp-xref (matched-node set + counts; edge-set rides on comp-blast per gap-list) ----------
xref = {}
xref_syms = []
for s in S["xref_symbols"]:
    if s not in xref_syms:
        xref_syms.append(s)
for sym in xref_syms:
    out, err, rc = run(CLI + ["xref", sym])
    # parse: "XREF LOOKUP: 'sym'  (N node(s), M edge(s) matched)" + the NODES section ids
    m = re.search(r"\((\d+)\s+node\(s\),\s*(\d+)\s+edge\(s\)\s+matched\)", out)
    ncount = int(m.group(1)) if m else None
    ecount = int(m.group(2)) if m else None
    # matched node ids appear as "gold:..." / "s3:..." / "lambda:..." / "endpoint:..." tokens in the NODES block
    node_ids = sorted(set(re.findall(r"\b((?:gold|s3|lambda|endpoint|eventbridge|component):[^\s]+)", out)))
    xref[sym] = {"node_count": ncount, "edge_count": ecount,
                 "matched_node_ids": node_ids, "sha": sha([ncount, ecount, node_ids])}
fixture["tool"]["comp-xref"] = xref

# ---------- comp-platinum (normalized chain text per component + reverse on top s3 keys) ----------
plat = {"components": {}, "reverse": {}, "summary": None}
sout, _, _ = run(PLAT + ["summary"])
# component names = first column of the summary table
comps = []
for line in sout.splitlines():
    m = re.match(r"\s{2}([A-Za-z][A-Za-z0-9_]+)\s{2,}\d", line)
    if m:
        comps.append(m.group(1))
plat["summary_components"] = comps

VOLATILE = re.compile(r"(SyntaxWarning|NOTE:|no --firm given|^\s*$)")
def normalize(text):
    return [ln.rstrip() for ln in text.splitlines() if ln.strip() and not VOLATILE.search(ln)]
for c in comps:
    out, err, rc = run(PLAT + ["page", c])
    norm = normalize(out)
    plat["components"][c] = {"chain": norm, "n_lines": len(norm), "sha": sha(norm)}
# reverse on top s3 keys (strip the s3: prefix -> the key path)
for sid in S["s3_top"][:4]:
    key = sid[len("s3:"):] if sid.startswith("s3:") else sid
    out, err, rc = run(PLAT + ["reverse", key])
    norm = normalize(out)
    plat["reverse"][key] = {"chain": norm, "n_lines": len(norm), "sha": sha(norm)}
fixture["tool"]["comp-platinum"] = plat

# ---------- meta / coverage ----------
fixture["meta"] = {
    "graph_json_built_at": sample_doc["built_at"],
    "node_counts": sample_doc["node_counts"],
    "edge_counts": sample_doc["edge_counts"],
    "sample_sizes": {k: len(v) for k, v in S.items()},
    "blast_targets_n": len(blast_targets),
    "xref_symbols_n": len(xref_syms),
    "platinum_components_n": len(comps),
}
out_path = os.path.join(SP, "fixture_layer_a.json")
json.dump(fixture, open(out_path, "w"), indent=2)
print("WROTE", out_path)
print("blast:", len(blast), "| trace:", len(trace), "| xref:", len(xref),
      "| platinum comps:", len(plat["components"]), "| reverse:", len(plat["reverse"]))
# quick error scan
errs = []
for tool, d in fixture["tool"].items():
    if tool == "comp-platinum":
        for c, v in d["components"].items():
            if any("error" in str(x) for x in [v]): errs.append((tool, c))
    else:
        for k, v in d.items():
            if isinstance(v, dict) and "error" in v: errs.append((tool, k, v.get("error")))
print("ERRORS:", errs if errs else "none")
