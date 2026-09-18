#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtd-3 arm (a): the RECORDED difference between the two HoldingsSnapshot schemas.

    V1  docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json      (what holdings_snapshot.py reads)
    CTR infra/aws/lambda/investor-reporting/_contracts/HoldingsSnapshot.schema.json

Both are read as git BLOBS at a named commit (never the worktree), so the diff is of the committed content.
Three grains, each with its denominator:
  1. every schema OBJECT PATH that declares `properties`: the property-name sets compared
  2. every object path that declares `required`: the required-name sets compared
  3. every LEAF (a JSON pointer to a scalar or a list of scalars): only-in-V1, only-in-CTR, value differs
Which schema is THE contract is L4's call; this module only says what differs.

Usage: py -3.12 schema_diff_ib_rtd_3.py [--ref <commit-ish>]
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

V1 = "docs/contracts/investor-reporting/v1/HoldingsSnapshot.schema.json"
CTR = "infra/aws/lambda/investor-reporting/_contracts/HoldingsSnapshot.schema.json"
WS = pathlib.Path(__file__).resolve().parents[7]


def blob(ref: str, rel: str) -> bytes:
    return subprocess.run(["git", "show", f"{ref}:{rel}"], capture_output=True, check=True, cwd=str(WS)).stdout


def blob_id(ref: str, rel: str) -> str:
    return subprocess.run(["git", "rev-parse", f"{ref}:{rel}"], capture_output=True, text=True, check=True,
                          cwd=str(WS)).stdout.strip()


def _ptr(path) -> str:
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in path)


def walk(node, path, props, reqs, leaves):
    if isinstance(node, dict):
        if isinstance(node.get("properties"), dict):
            props[_ptr(path)] = set(node["properties"])
        if isinstance(node.get("required"), list):
            reqs[_ptr(path)] = set(node["required"])
        for k, v in node.items():
            walk(v, path + [k], props, reqs, leaves)
    elif isinstance(node, list):
        if all(not isinstance(x, (dict, list)) for x in node):
            leaves[_ptr(path)] = json.dumps(node, sort_keys=True)
        else:
            for i, v in enumerate(node):
                walk(v, path + [i], props, reqs, leaves)
    else:
        leaves[_ptr(path)] = json.dumps(node)


def diff(ref: str = "HEAD") -> dict:
    out = {"ref": ref}
    grains = {}
    for tag, rel in (("V1", V1), ("CTR", CTR)):
        raw = blob(ref, rel)
        props, reqs, leaves = {}, {}, {}
        walk(json.loads(raw.decode("utf-8")), [], props, reqs, leaves)
        grains[tag] = (props, reqs, leaves)
        out[tag] = {"path": rel, "blob": blob_id(ref, rel), "bytes": len(raw), "cr": raw.count(b"\r"),
                    "object_paths_with_properties": len(props), "object_paths_with_required": len(reqs),
                    "leaves": len(leaves)}
    (p1, r1, l1), (p2, r2, l2) = grains["V1"], grains["CTR"]
    out["properties"] = {
        "paths_union": len(set(p1) | set(p2)),
        "only_v1_paths": sorted(set(p1) - set(p2)), "only_ctr_paths": sorted(set(p2) - set(p1)),
        "differ": {k: {"only_v1": sorted(p1[k] - p2[k]), "only_ctr": sorted(p2[k] - p1[k])}
                   for k in sorted(set(p1) & set(p2)) if p1[k] != p2[k]}}
    out["required"] = {
        "paths_union": len(set(r1) | set(r2)),
        "only_v1_paths": sorted(set(r1) - set(r2)), "only_ctr_paths": sorted(set(r2) - set(r1)),
        "differ": {k: {"only_v1": sorted(r1[k] - r2[k]), "only_ctr": sorted(r2[k] - r1[k])}
                   for k in sorted(set(r1) & set(r2)) if r1[k] != r2[k]}}
    common = set(l1) & set(l2)
    out["leaves"] = {
        "union": len(set(l1) | set(l2)), "common": len(common),
        "only_v1": sorted(set(l1) - set(l2)), "only_ctr": sorted(set(l2) - set(l1)),
        "value_differs": sorted(k for k in common if l1[k] != l2[k])}
    out["_leaf_values"] = {k: (l1.get(k), l2.get(k)) for k in out["leaves"]["value_differs"]}
    return out


def render(d: dict) -> "list[str]":
    L = [f"TWO HoldingsSnapshot SCHEMAS, as git blobs at {d['ref']}"]
    for tag in ("V1", "CTR"):
        s = d[tag]
        L.append(f"  {tag:<3} {s['path']}  blob {s['blob']}  {s['bytes']} bytes ({s['cr']} CR)  "
                 f"objects-with-properties {s['object_paths_with_properties']}, with-required "
                 f"{s['object_paths_with_required']}, leaves {s['leaves']}")
    pr = d["properties"]
    L.append(f"(1) PROPERTIES over {pr['paths_union']} object path(s) (union): only in V1 {len(pr['only_v1_paths'])}, "
             f"only in CTR {len(pr['only_ctr_paths'])}, name sets differ at {len(pr['differ'])}")
    for p in pr["only_v1_paths"]:
        L.append(f"      only V1  {p}")
    for p in pr["only_ctr_paths"]:
        L.append(f"      only CTR {p}")
    for p, v in pr["differ"].items():
        L.append(f"      differ   {p}: only V1 {v['only_v1']}; only CTR {v['only_ctr']}")
    rq = d["required"]
    L.append(f"(2) REQUIRED over {rq['paths_union']} object path(s) (union): only in V1 {len(rq['only_v1_paths'])}, "
             f"only in CTR {len(rq['only_ctr_paths'])}, sets differ at {len(rq['differ'])}")
    for p in rq["only_v1_paths"]:
        L.append(f"      only V1  {p}")
    for p in rq["only_ctr_paths"]:
        L.append(f"      only CTR {p}")
    for p, v in rq["differ"].items():
        L.append(f"      differ   {p}: only V1 {v['only_v1']}; only CTR {v['only_ctr']}")
    lv = d["leaves"]
    L.append(f"(3) LEAVES over {lv['union']} pointer(s) (union; {lv['common']} common): only in V1 {len(lv['only_v1'])}, "
             f"only in CTR {len(lv['only_ctr'])}, value differs {len(lv['value_differs'])}")
    for p in lv["value_differs"]:
        a, b = d["_leaf_values"][p]
        L.append(f"      differs  {p}: V1 {a[:140]} | CTR {b[:140]}")
    for p in lv["only_v1"]:
        L.append(f"      only V1  {p}")
    for p in lv["only_ctr"]:
        L.append(f"      only CTR {p}")
    return L


if __name__ == "__main__":
    ref = sys.argv[sys.argv.index("--ref") + 1] if "--ref" in sys.argv else "HEAD"
    print("\n".join(render(diff(ref))))
