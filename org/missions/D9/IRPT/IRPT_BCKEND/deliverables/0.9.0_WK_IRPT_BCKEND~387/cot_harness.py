#!/usr/bin/env python3
"""IB-pr-542 (round 196, worker 0.9.0_WK_IRPT_BCKEND~387) -- Cottonwood node-signature harness. READ ONLY.

Derived from the IB-pr-541 harness (built_bundle_differential.py, worker ~386): the same signature, the same field
classes, the same identity-patch attribution of the signed cash rule, the same beyond-rule rule. Cottonwood only; no
publication gate (not needed for node attribution).

Subcommands:
  build    one tree: build the Cottonwood candidate (holdings_snapshot.build_snapshot), write the per-node signature,
           optionally the identity-patch signature (apply_cash_rule replaced by identity) and the receipts.
  compare  live signature vs base signature vs base identity signature -> the beyond-rule node set and its groups.

The S3 client is wrapped: any operation not beginning get_, list_ or head_ is refused and counted.
"""
import argparse
import gzip
import hashlib
import json
import re
import subprocess  # noqa: F401  (kept for parity with the 386 harness)
import sys
import time
from collections import Counter
from pathlib import Path

CLASS_FIELDS = ("asset_class", "asset_class_basis", "sub_asset_class", "class_source")
TOL = 0.01
READ_OPS = ("get_", "list_", "head_")
PRODUCER = ("data", "assets", "scripts", "gold", "investor_reporting")
AS_OF = "2026-10-12"
SIGNED_TOTAL = 249
BETA_NOTE = "identity-patch: apply_cash_rule replaced by identity in-process"
HERE = Path(__file__).resolve()


def log(msg):
    sys.stdout.write(time.strftime("%H:%M:%S ") + msg + "\n")
    sys.stdout.flush()


def digest_of(obj):
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def short(obj):
    text = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, default=str)
    return hashlib.sha256(text.encode("ascii")).hexdigest()[:16]


class ReadOnlyS3:
    def __init__(self, client):
        self._client = client
        self.reads = []
        self.refused = []

    def get_object(self, **kwargs):
        self.reads.append((kwargs.get("Bucket"), kwargs.get("Key")))
        return self._client.get_object(**kwargs)

    def __getattr__(self, name):
        if name.startswith(READ_OPS):
            return getattr(self._client, name)
        self.refused.append(name)
        raise PermissionError("read-only harness refuses the %s operation" % name)


def strip_numbers(o):
    if isinstance(o, bool):
        return o
    if isinstance(o, (int, float)):
        return None
    if isinstance(o, dict):
        return {k: strip_numbers(v) for k, v in o.items()}
    if isinstance(o, list):
        return [strip_numbers(v) for v in o]
    return o


def flatten_numbers(o, prefix, out):
    if isinstance(o, bool):
        return
    if isinstance(o, (int, float)):
        out[prefix] = float(o)
    elif isinstance(o, dict):
        for k in sorted(o, key=str):
            flatten_numbers(o[k], "%s.%s" % (prefix, k), out)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            flatten_numbers(v, "%s[%d]" % (prefix, i), out)


def signature(nodes):
    rows = []
    for n in nodes:
        cls = {f: n[f] for f in CLASS_FIELDS if f in n}
        num, res = {}, {}
        for k in sorted(n, key=str):
            if k in CLASS_FIELDS:
                continue
            flatten_numbers(n[k], str(k), num)
            res[str(k)] = short(strip_numbers(n[k]))
        rows.append({"id": n.get("node_id"), "kind": n.get("node_kind"), "cls": cls, "num": num, "res": res})
    return rows


def write_gz(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(str(path), "wt", encoding="utf-8") as fh:
        json.dump(obj, fh, separators=(",", ":"), sort_keys=True)


def load_gz(path):
    with gzip.open(str(path), "rt", encoding="utf-8") as fh:
        return json.load(fh)


def import_producer(tree):
    tree = Path(tree).resolve()
    sys.path[:0] = [str(tree.joinpath(*PRODUCER)), str(tree / "lib")]
    import holdings_snapshot as hs
    mod = Path(hs.__file__).resolve()
    if not str(mod).lower().startswith(str(tree).lower()):
        raise SystemExit("REFUSED: the producer imported from outside its tree: %s" % mod)
    return hs, mod


def make_client():
    import boto3
    return ReadOnlyS3(boto3.client("s3", region_name="us-east-1"))


def cmd_build(a):
    hs, mod = import_producer(a.tree)
    client = make_client()
    inputs = hs.VersionedInputs(client)
    seed = json.loads(Path(a.seed).read_text(encoding="utf-8")) if a.seed else []
    for ref in seed:
        inputs._refs[(ref["bucket"], ref["key"])] = dict(ref)
    seeded = {(ref["bucket"], ref["key"]) for ref in seed}
    meta = {"label": a.label, "as_of": AS_OF, "tree": str(Path(a.tree).resolve()), "producer_module": str(mod),
            "seeded_objects": len(seeded)}
    t0 = time.time()
    n0 = len(client.reads)
    snap = hs.build_snapshot("cottonwood", inputs, AS_OF)
    hs.recompute_weights(snap["nodes"])
    meta["business_date_built"] = (snap.get("clocks") or {}).get("business_date")
    meta["node_count"] = len(snap["nodes"])
    meta["kinds"] = dict(Counter(n.get("node_kind") for n in snap["nodes"]))
    write_gz(a.out, signature(snap["nodes"]))
    src_reads = set(client.reads[n0:])
    meta["source_objects_read"] = len(src_reads)
    meta["source_reads_outside_seed"] = len(src_reads - seeded)
    if a.identity_out:
        if not hasattr(hs, "apply_cash_rule"):
            raise SystemExit("REFUSED: this tree has no apply_cash_rule to replace")
        real = hs.apply_cash_rule
        hs.apply_cash_rule = lambda result: result
        try:
            n1 = len(client.reads)
            ident = hs.build_snapshot("cottonwood", inputs, AS_OF)
        finally:
            hs.apply_cash_rule = real
        hs.recompute_weights(ident["nodes"])
        write_gz(a.identity_out, signature(ident["nodes"]))
        meta["identity_node_count"] = len(ident["nodes"])
        meta["identity_reads_outside_seed"] = len(set(client.reads[n1:]) - seeded)
    if a.receipts_out:
        Path(a.receipts_out).write_text(json.dumps(inputs.receipts(), sort_keys=True), encoding="utf-8")
    meta["receipts_count"] = len(inputs._refs)
    meta["refused_calls"] = len(client.refused)
    meta["seconds"] = round(time.time() - t0)
    Path(a.meta_out).write_text(json.dumps(meta, sort_keys=True, indent=1), encoding="utf-8")
    log("OK: build %s nodes=%d reads=%d outside_seed=%d refused=%d seconds=%d"
        % (a.label, meta["node_count"], meta["source_objects_read"], meta["source_reads_outside_seed"],
           meta["refused_calls"], meta["seconds"]))
    return 0


# ----------------------------------------------------------------------------------------------- comparison

def top_field(path):
    return re.split(r"[.\[]", path, maxsplit=1)[0]


def diff_items(lr, br):
    items = []
    for f in CLASS_FIELDS:
        a, b = lr["cls"].get(f), br["cls"].get(f)
        if a != b:
            items.append({"kind": "cls", "field": f, "label": "%s: %s -> %s" % (
                f, "(absent)" if a is None else str(a), "(absent)" if b is None else str(b)), "delta": None})
    for path in sorted(set(lr["num"]) | set(br["num"])):
        a, b = lr["num"].get(path), br["num"].get(path)
        top = top_field(path)
        if a is None or b is None:
            if a != b:
                items.append({"kind": "presence", "field": top, "label": "%s: presence change" % top, "delta": None})
        elif abs(a - b) > TOL:
            items.append({"kind": "num", "field": top, "label": "%s: numeric change" % top, "delta": abs(a - b)})
    for f in sorted(set(lr["res"]) | set(br["res"])):
        if lr["res"].get(f) != br["res"].get(f):
            items.append({"kind": "res", "field": f, "label": "%s: non-numeric change" % f, "delta": None})
    return items


def changed_nodes(L, B):
    out = {}
    for nid in sorted((k for k in L if k in B), key=str):
        items = diff_items(L[nid], B[nid])
        if items:
            out[nid] = items
    return out


def cmd_compare(a):
    live = load_gz(a.live)
    base = load_gz(a.base)
    ident = load_gz(a.identity)
    L = {r["id"]: r for r in live}
    B = {r["id"]: r for r in base}
    IDN = {r["id"]: r for r in ident}
    changed = changed_nodes(L, B)
    signed, beyond = set(), set()
    for nid, items in changed.items():
        l_ac = L[nid]["cls"].get("asset_class")
        b_ac = B[nid]["cls"].get("asset_class")
        id_ac = IDN[nid]["cls"].get("asset_class") if nid in IDN else None
        for it in items:
            if (it["kind"] == "cls" and it["field"] == "asset_class" and id_ac is not None
                    and b_ac != id_ac and l_ac == id_ac):
                signed.add(nid)
            else:
                beyond.add(nid)
    # per beyond node: its items (all beyond when the node is not signed)
    beyond_items = {nid: [it for it in changed[nid]] for nid in beyond}
    res = {
        "rows": {"live": dict(Counter(r["kind"] for r in live)), "base": dict(Counter(r["kind"] for r in base))},
        "total_changed_nodes": len(changed),
        "signed_cash_rule_nodes": len(signed),
        "beyond_rule_nodes": len(beyond),
        "beyond_rule_total_check": len(changed) - len(signed),
        "signed_and_beyond_overlap": len(signed & beyond),
        "beyond_groups": {},
    }
    groups = Counter()
    for nid in beyond:
        for it in beyond_items[nid]:
            groups[it["label"]] += 1
    res["beyond_groups"] = dict(sorted(groups.items()))
    out = {"result": res, "digest": digest_of(res)}
    if a.out_beyond:
        write_gz(a.out_beyond, {"beyond": {nid: beyond_items[nid] for nid in sorted(beyond, key=str)},
                                "signed": sorted(signed, key=str)})
    Path(a.out).write_text(json.dumps(out, sort_keys=True, indent=1), encoding="utf-8")
    log("OK: compare total=%d signed=%d beyond=%d overlap=%d digest=%s"
        % (res["total_changed_nodes"], res["signed_cash_rule_nodes"], res["beyond_rule_nodes"],
           res["signed_and_beyond_overlap"], out["digest"][:12]))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("build")
    b.add_argument("--tree", required=True)
    b.add_argument("--label", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--meta-out", required=True)
    b.add_argument("--seed")
    b.add_argument("--identity-out")
    b.add_argument("--receipts-out")
    c = sp.add_parser("compare")
    c.add_argument("--live", required=True)
    c.add_argument("--base", required=True)
    c.add_argument("--identity", required=True)
    c.add_argument("--out", required=True)
    c.add_argument("--out-beyond")
    a = ap.parse_args(argv)
    if a.cmd == "build":
        return cmd_build(a)
    return cmd_compare(a)


if __name__ == "__main__":
    sys.exit(main())
