#!/usr/bin/env python3
"""IRPT_BCKEND IB-pr-545 (round 197, workstream ~P, worker 0.9.0_WK_IRPT_BCKEND~390), pin 2 -- the BUILT-bundle differential
with a same-state publish gate. READ ONLY.

Two code sides, each a BUNDLE tree (CLAUDE.md 22a: for a release the bundle is the build input):
  LIVE   the live investor-reporting bundle, downloaded by version id and untarred (scratch).
  BUILT  core.build_bundle_payload(b) at the new pin, untarred (scratch).
Each tree's producer is imported from that tree, in its own subprocess under python -I (both trees export a module
named holdings_snapshot); the import is refused unless the imported file lies under its tree. The S3 client is wrapped:
any operation whose name does not begin with get_, list_ or head_ is refused and counted. Source objects are read through
the producer's own VersionedInputs; both sides of a pair are built on the same pre-seeded source receipts.

The publication index is captured ONCE per firm (publisher.begin(), subcommand served) and kept in scratch. Each code's
served_publication reads the exact versions that one capture names, and each code's own evaluate_publish_gate runs on its
own served read; the two readers must name the same served revision, index date and version (the same-state attestation,
a STOP otherwise). Scratch lives outside the repository. Nothing is written to S3, nothing is
signed, minted, uploaded or sent.

Subcommands:
  served    read the firm's served publication once (begin + served_publication) into a scratch pickle.
  build     one tree, one firm: build the candidate; optionally evaluate the gate against the scratch served state; write
            the per-node signature, the receipts, and (for the built tree) the identity-patch signature.
  run       the whole per-firm sequence: served read (once), built pair 1, live pair 1, built pair 2, live pair 2,
            the comparison run twice, and the planted mutant.
  assemble  the record JSON from the three per-firm results, the served metadata and the notes file.
"""
import argparse
import gzip
import hashlib
import json
import os
import pickle
import re
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

BUILT_ROOT = Path("C:/dev/_scratch390/built")
LIVE_ROOT = Path("C:/dev/_scratch390/live")
WORK_ROOT = Path("C:/dev/_scratch390/run")
PIN = "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f"
BASE_COMMIT = "52dea9de8a32c39db3b2cdf146a8d35962e976f8"
FIRMS = ("49financial", "cottonwood", "inflection")
AS_OF = {"49financial": "2026-10-12", "cottonwood": "2026-10-12", "inflection": "2026-10-13"}
SIGNED = {"49financial": 32, "cottonwood": 249, "inflection": 841}
LIVE_VERSIONS = {"49financial": "UHOCIkWj3QiIzNucG1VjNnk_AufIg6oD", "cottonwood": "oyIYMVdh_l2zCg5ZWvn3ISPPS6_9Q82_",
                 "inflection": "PzhCs97qVBXkZcIjaOklHmzWiFsOFafM"}
CLASS_FIELDS = ("asset_class", "asset_class_basis", "sub_asset_class", "class_source")
TOL = 0.01
READ_OPS = ("get_", "list_", "head_")
PRODUCER = ("data", "assets", "scripts", "gold", "investor_reporting")
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
    """The read client. get_object is logged; get_, list_ and head_ operations pass through; everything else is refused."""

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
    """One record per node: id, kind, the raw classification fields, every numeric leaf by field path, and a short hash of
    the non-numeric residue of EVERY top-level field."""
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
    """Put the tree's producer and lib first, import holdings_snapshot, and refuse a module imported from outside the tree."""
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


def fingerprint(served):
    """Identity of a served read, comparable across the two code versions: the revision, the index date and version,
    the account count and the node count. The two readers return different shapes (the built reader a keyed summary,
    the live reader a node list), so only these fields are compared."""
    if served is None:
        return None
    node_count = served["node_count"] if "node_count" in served else len(served.get("nodes") or [])
    return {"revision": served.get("revision"), "index_date": served.get("index_date"),
            "index_version": served.get("index_version"), "account_count": len(served.get("account_ids") or []),
            "node_count": node_count}


def gate_eval(hs, client, firm, snap, served):
    """evaluate_publish_gate of THIS code against the served read of the one index capture (begin, read once per firm).
    Each code reads through its own served_publication, so the gate and its served shape are the same code's. The
    closed-account and no-closures lookups are read calls on the firm's directory."""
    bucket = hs.firm_bucket_map().get(firm, "")
    gate = hs.evaluate_publish_gate(
        snap, served,
        lambda: hs.closed_account_ids(client, bucket, firm),
        lambda: hs.directory_marks_no_closures(client, bucket, firm))
    return {"outcome": gate["outcome"], "conditions": [c["condition"] for c in gate.get("conditions", [])]}


# ----------------------------------------------------------------------------------------------- subcommands

def cmd_served(a):
    """The ONE index read per firm: begin() captures the publication index and its version ids. The index capture is
    pickled; every code's served_publication reads the exact versions that capture names. The built reader's served read
    is taken here for the attestation fingerprint only."""
    hs, mod = import_producer(a.tree)
    client = make_client()
    publisher = hs.HoldingsPublication(client, a.firm, qa=False)
    expected = publisher.begin()
    with open(a.out, "wb") as fh:
        pickle.dump(expected, fh)
    served = hs.served_publication(publisher, expected)
    doc = expected.get("document") or {}
    ref = expected.get("reference") or {}
    state = {"latest_date": doc.get("latest_date"), "manifest_version": ref.get("version_id"),
             "index_sha256": ref.get("sha256"), "served": served}
    meta = {"firm": a.firm, "latest_date": state["latest_date"], "manifest_version": state["manifest_version"],
            "index_sha256": state["index_sha256"], "served_is_none": served is None,
            "fingerprint_built_reader": fingerprint(served), "index_reads": len(client.reads),
            "refused_calls": len(client.refused), "producer_module": str(mod)}
    Path(a.meta_out).write_text(json.dumps(meta, sort_keys=True, indent=1), encoding="utf-8")
    log("OK: served %s latest_date=%s manifest_version=%s none=%s reads=%d refused=%d"
        % (a.firm, meta["latest_date"], meta["manifest_version"], meta["served_is_none"], len(client.reads),
           len(client.refused)))
    return 0


def cmd_build(a):
    hs, mod = import_producer(a.tree)
    client = make_client()
    inputs = hs.VersionedInputs(client)
    seed = json.loads(Path(a.seed).read_text(encoding="utf-8")) if a.seed else []
    for ref in seed:
        inputs._refs[(ref["bucket"], ref["key"])] = dict(ref)
    seeded = {(ref["bucket"], ref["key"]) for ref in seed}
    meta = {"label": a.label, "firm": a.firm, "as_of": a.as_of, "tree": str(Path(a.tree).resolve()),
            "producer_module": str(mod), "seeded_objects": len(seeded)}
    t0 = time.time()
    n0 = len(client.reads)
    snap = hs.build_snapshot(a.firm, inputs, a.as_of)
    hs.recompute_weights(snap["nodes"])
    meta["business_date_built"] = (snap.get("clocks") or {}).get("business_date")
    meta["node_count"] = len(snap["nodes"])
    meta["kinds"] = dict(Counter(n.get("node_kind") for n in snap["nodes"]))
    write_gz(a.out, signature(snap["nodes"]))
    src_reads = set(client.reads[n0:])
    meta["source_objects_read"] = len(src_reads)
    meta["source_reads_outside_seed"] = len(src_reads - seeded)
    if a.gate_out:
        with open(a.served, "rb") as fh:
            expected = pickle.load(fh)
        publisher = hs.HoldingsPublication(client, a.firm, qa=False)
        served = hs.served_publication(publisher, expected)
        gate = gate_eval(hs, client, a.firm, snap, served)
        gate["served_fingerprint"] = fingerprint(served)
        Path(a.gate_out).write_text(json.dumps(gate, sort_keys=True, indent=1), encoding="utf-8")
        meta["gate"] = gate["outcome"]
        meta["served_fingerprint"] = gate["served_fingerprint"]
    if a.identity_out:
        if not hasattr(hs, "apply_cash_rule"):
            raise SystemExit("REFUSED: this tree has no apply_cash_rule to replace")
        real = hs.apply_cash_rule
        hs.apply_cash_rule = lambda result: result
        try:
            n1 = len(client.reads)
            ident = hs.build_snapshot(a.firm, inputs, a.as_of)
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
    log("OK: build %s %s as_of=%s nodes=%d reads=%d outside_seed=%d refused=%d seconds=%d"
        % (a.label, a.firm, a.as_of, meta["node_count"], meta["source_objects_read"],
           meta["source_reads_outside_seed"], meta["refused_calls"], meta["seconds"]))
    return 0


# ----------------------------------------------------------------------------------------------- comparison

def top_field(path):
    """The top-level field name of a flattened path (never a keyed id under it)."""
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


def gate_attr(firm, gl, gb):
    if gl["outcome"] == gb["outcome"] and sorted(gl["conditions"]) == sorted(gb["conditions"]):
        return "same"
    if (firm == "cottonwood" and gl["outcome"] == "REFUSED" and gb["outcome"] == "PUBLISHED"
            and set(gl["conditions"]) - set(gb["conditions"]) == {"account_lost"}
            and set(gb["conditions"]) <= set(gl["conditions"])):
        return "signed_exemption_repair"
    return "UNATTRIBUTED"


def compare(firm, live_rows, built_rows, ident_rows, gate_live, gate_built):
    """The comparison step: per-node signatures, one attribution per changed item. Returns (result, digest)."""
    L = {r["id"]: r for r in live_rows}
    B = {r["id"]: r for r in built_rows}
    rows = {"live": dict(Counter(r["kind"] for r in live_rows)), "built": dict(Counter(r["kind"] for r in built_rows))}
    AL = {k for k, r in L.items() if r["kind"] == "ACCOUNT"}
    AB = {k for k, r in B.items() if r["kind"] == "ACCOUNT"}
    account_set = {"only_live": len(AL - AB), "only_built": len(AB - AL), "both": len(AL & AB)}
    changed = changed_nodes(L, B)
    num_nodes, largest = 0, (0.0, "none")
    for nid, items in changed.items():
        if any(i["kind"] == "num" for i in items):
            num_nodes += 1
        for i in items:
            if i["kind"] == "num" and i["delta"] > largest[0]:
                largest = (i["delta"], i["field"])
    ident_ac = {r["id"]: r["cls"].get("asset_class") for r in (ident_rows or []) if r["id"] in changed}
    groups, signed, beyond = {}, set(), set()
    for nid, items in changed.items():
        l_ac = L[nid]["cls"].get("asset_class")
        b_ac = B[nid]["cls"].get("asset_class")
        id_ac = ident_ac.get(nid)
        for it in items:
            if (it["kind"] == "cls" and it["field"] == "asset_class" and id_ac is not None
                    and b_ac != id_ac and l_ac == id_ac):
                att, by = "signed_cash_rule", "identity-patch"
                signed.add(nid)
            else:
                att, by = "UNATTRIBUTED", "none"
                beyond.add(nid)
            groups.setdefault((it["label"], att, by), set()).add(nid)
    diffs = [{"group": label, "nodes": len(nodes), "attribution": att, "attributed_by": by}
             for (label, att, by), nodes in sorted(groups.items())]
    res = {
        "firm": firm,
        "rows": rows,
        "account_set": account_set,
        "only_live_nodes": len(set(L) - set(B)),
        "only_built_nodes": len(set(B) - set(L)),
        "duplicate_node_ids": {"live": len(live_rows) - len(L), "built": len(built_rows) - len(B)},
        "changed_values": {"tolerance": TOL, "nodes_with_changed_numeric_value": num_nodes,
                           "largest_abs_delta": round(largest[0], 6), "largest_delta_field": largest[1]},
        "gate": {"live": {"outcome": gate_live["outcome"], "conditions": sorted(gate_live["conditions"])},
                 "built": {"outcome": gate_built["outcome"], "conditions": sorted(gate_built["conditions"])}},
        "gate_attribution": gate_attr(firm, gate_live, gate_built),
        "total_changed_nodes": len(changed),
        "signed_cash_rule_nodes": len(signed),
        "beyond_rule_nodes": len(beyond),
        "differences": diffs,
    }
    return res, digest_of(res)


def mutant_changed_count(L_rows, B_rows, changed_base):
    """Plant ONE asset_class value change in the built side's signature (in memory, on a node that is unchanged in the
    comparison) and return the changed-node count with the mutant."""
    L = {r["id"]: r for r in L_rows}
    B = {r["id"]: r for r in B_rows}
    cand = sorted((k for k in L if k in B and k not in changed_base and L[k]["kind"] == "SECURITY"
                   and L[k]["cls"].get("asset_class") is not None
                   and L[k]["cls"].get("asset_class") == B[k]["cls"].get("asset_class")), key=str)
    if not cand:
        raise SystemExit("REFUSED: no unchanged SECURITY node carries an asset_class to plant the mutant on")
    pick = cand[0]
    B[pick]["cls"]["asset_class"] = "__mutant__"
    return len(changed_nodes(L, B))


def sub_build(work, label, tree, firm, as_of, out, meta_out, seed=None, served=None, gate_out=None, identity_out=None,
              receipts_out=None):
    """One build in its own process (python -I). Resumes when its outputs exist."""
    if Path(meta_out).exists() and Path(out).exists() and (not gate_out or Path(gate_out).exists()):
        log("SKIP: %s already built (resume)" % label)
        return
    cmd = [sys.executable, "-I", str(HERE), "build", "--tree", str(tree), "--label", label, "--firm", firm,
           "--as-of", as_of, "--out", str(out), "--meta-out", str(meta_out)]
    for flag, val in (("--seed", seed), ("--served", served), ("--gate-out", gate_out),
                      ("--identity-out", identity_out), ("--receipts-out", receipts_out)):
        if val:
            cmd += [flag, str(val)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=5400)
    if p.returncode != 0:
        raise SystemExit("REFUSED: build %s failed: %s" % (label, (p.stderr or "")[-800:]))
    sys.stdout.write(p.stdout)
    sys.stdout.flush()


def sub_served(work, tree, firm, out, meta_out):
    if Path(out).exists() and Path(meta_out).exists():
        log("SKIP: served state for %s already read once (resume)" % firm)
        return
    cmd = [sys.executable, "-I", str(HERE), "served", "--tree", str(tree), "--firm", firm, "--out", str(out),
           "--meta-out", str(meta_out)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=5400)
    if p.returncode != 0:
        raise SystemExit("REFUSED: served read %s failed: %s" % (firm, (p.stderr or "")[-800:]))
    sys.stdout.write(p.stdout)
    sys.stdout.flush()


def cmd_run(a):
    firm = a.firm
    as_of = AS_OF[firm]
    work = Path(a.work) / firm
    work.mkdir(parents=True, exist_ok=True)
    built_dir, live_dir = BUILT_ROOT / firm, LIVE_ROOT / firm
    w = lambda name: work / name  # noqa: E731
    t_start = time.time()
    # The served publication, read ONCE for this firm, from the built tree's own reader.
    sub_served(work, built_dir, firm, w("served.pkl"), w("served_meta.json"))
    served = w("served.pkl")
    # Pair 1: built (rule, identity, gate, receipts), then live (rule, gate) on the built run's receipts.
    sub_build(work, "built_r1", built_dir, firm, as_of, w("built_r1.json.gz"), w("meta_built_r1.json"),
              served=served, gate_out=w("gate_built_r1.json"), identity_out=w("built_id_r1.json.gz"),
              receipts_out=w("rec_r1.json"))
    sub_build(work, "live_r1", live_dir, firm, as_of, w("live_r1.json.gz"), w("meta_live_r1.json"),
              seed=w("rec_r1.json"), served=served, gate_out=w("gate_live_r1.json"))
    # Pair 2: fresh builds on the same receipts.
    sub_build(work, "built_r2", built_dir, firm, as_of, w("built_r2.json.gz"), w("meta_built_r2.json"),
              seed=w("rec_r1.json"), served=served, gate_out=w("gate_built_r2.json"),
              identity_out=w("built_id_r2.json.gz"), receipts_out=w("rec_r2.json"))
    sub_build(work, "live_r2", live_dir, firm, as_of, w("live_r2.json.gz"), w("meta_live_r2.json"),
              seed=w("rec_r1.json"), served=served, gate_out=w("gate_live_r2.json"))
    gl1 = json.loads(w("gate_live_r1.json").read_text(encoding="utf-8"))
    gb1 = json.loads(w("gate_built_r1.json").read_text(encoding="utf-8"))
    gl2 = json.loads(w("gate_live_r2.json").read_text(encoding="utf-8"))
    gb2 = json.loads(w("gate_built_r2.json").read_text(encoding="utf-8"))
    # Same-state attestation: both readers, each on the one index capture, must name the same served revision.
    for tag, gl, gb in (("run1", gl1, gb1), ("run2", gl2, gb2)):
        if gl.get("served_fingerprint") != gb.get("served_fingerprint"):
            raise SystemExit("STOP: the live and built served readers disagree on the one index capture (%s): %r vs %r"
                             % (tag, gl.get("served_fingerprint"), gb.get("served_fingerprint")))
    rec1 = json.loads(w("rec_r1.json").read_text(encoding="utf-8"))
    rec2 = json.loads(w("rec_r2.json").read_text(encoding="utf-8"))
    log("STEP: comparison run 1")
    live_r1, built_r1 = load_gz(w("live_r1.json.gz")), load_gz(w("built_r1.json.gz"))
    id_r1 = load_gz(w("built_id_r1.json.gz"))
    res1, dig1 = compare(firm, live_r1, built_r1, id_r1, gl1, gb1)
    changed1 = set(changed_nodes({r["id"]: r for r in live_r1}, {r["id"]: r for r in built_r1}))
    planted = mutant_changed_count(live_r1, built_r1, changed1)
    mutant = {"planted": "one asset_class value changed in the built side's signature (in memory, unchanged node)",
              "changed_nodes_with_mutant": planted, "flagged": planted == res1["total_changed_nodes"] + 1}
    del live_r1, built_r1, id_r1
    log("STEP: comparison run 2")
    live_r2, built_r2 = load_gz(w("live_r2.json.gz")), load_gz(w("built_r2.json.gz"))
    id_r2 = load_gz(w("built_id_r2.json.gz"))
    res2, dig2 = compare(firm, live_r2, built_r2, id_r2, gl2, gb2)
    del live_r2, built_r2, id_r2
    out = {"firm": firm, "as_of": as_of, "result": res1, "run1_digest": dig1, "run2_digest": dig2,
           "served_readers_agree": True, "served_fingerprint": gb1.get("served_fingerprint"),
           "run2_result_equal": res1 == res2, "receipts_run2_equal_run1": digest_of(rec1) == digest_of(rec2),
           "gate_run2_equal_run1": (gl1 == gl2 and gb1 == gb2), "mutant": mutant,
           "meta": {k: json.loads(w(f).read_text(encoding="utf-8")) for k, f in
                    (("built_r1", "meta_built_r1.json"), ("live_r1", "meta_live_r1.json"),
                     ("built_r2", "meta_built_r2.json"), ("live_r2", "meta_live_r2.json"))},
           "seconds": round(time.time() - t_start)}
    Path(w("result.json")).write_text(json.dumps(out, sort_keys=True, indent=1), encoding="utf-8")
    log("OK: %s total=%d signed=%d beyond=%d run1=%s run2=%s equal=%s mutant_flagged=%s"
        % (firm, res1["total_changed_nodes"], res1["signed_cash_rule_nodes"], res1["beyond_rule_nodes"], dig1[:12],
           dig2[:12], res1 == res2, mutant["flagged"]))
    return 0


# ----------------------------------------------------------------------------------------------- record

def count_files(root):
    """The bundle's own files: every file except the bytecode caches that python -I writes into the extracted tree
    (the -I flag ignores PYTHONDONTWRITEBYTECODE)."""
    n = 0
    for dirpath, dirnames, files in os.walk(str(root)):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        n += sum(1 for f in files if not f.endswith(".pyc"))
    return n


def cmd_assemble(a):
    work = Path(a.work)
    notes = json.loads(Path(a.notes).read_text(encoding="utf-8"))
    rec = {"base_commit": BASE_COMMIT, "new_pin": PIN,
           "custody_pins": dict(AS_OF), "live_versions": dict(LIVE_VERSIONS), "firms": {}}
    for f in FIRMS:
        r = json.loads((work / f / "result.json").read_text(encoding="utf-8"))
        smeta = json.loads((work / f / "served_meta.json").read_text(encoding="utf-8"))
        res = r["result"]
        entry = {
            "rows": {"live": res["rows"]["live"], "built": res["rows"]["built"]},
            "account_set": res["account_set"],
            "changed_values": res["changed_values"],
            "gate": {"served_state": {"latest_date": smeta["latest_date"], "manifest_version": smeta["manifest_version"]},
                     "live": res["gate"]["live"], "built": res["gate"]["built"], "attribution": res["gate_attribution"]},
            "total_changed_nodes": res["total_changed_nodes"],
            "differences": res["differences"],
            "built_from": "core.build_bundle_payload at pin 2",
            "built_bundle_members": count_files(BUILT_ROOT / f),
            "run1_digest": r["run1_digest"],
            "run2_digest": r["run2_digest"],
            "mutant": {"planted": r["mutant"]["planted"], "flagged": r["mutant"]["flagged"],
                       "changed_nodes_with_mutant": r["mutant"]["changed_nodes_with_mutant"]},
        }
        if f == "cottonwood":
            entry["beyond_rule_nodes"] = res["beyond_rule_nodes"]
        rec["firms"][f] = entry
    rec["notes"] = notes
    for k in ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written",
              "vendor_requests_sent"):
        rec[k] = 0
    Path(a.out).write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    log("OK: wrote the built-bundle differential record")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("served")
    s.add_argument("--tree", required=True)
    s.add_argument("--firm", required=True, choices=FIRMS)
    s.add_argument("--out", required=True)
    s.add_argument("--meta-out", required=True)
    b = sp.add_parser("build")
    b.add_argument("--tree", required=True)
    b.add_argument("--label", required=True)
    b.add_argument("--firm", required=True, choices=FIRMS)
    b.add_argument("--as-of", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--meta-out", required=True)
    b.add_argument("--seed")
    b.add_argument("--served")
    b.add_argument("--gate-out")
    b.add_argument("--identity-out")
    b.add_argument("--receipts-out")
    r = sp.add_parser("run")
    r.add_argument("--firm", required=True, choices=FIRMS)
    r.add_argument("--work", default=str(WORK_ROOT))
    t = sp.add_parser("assemble")
    t.add_argument("--work", default=str(WORK_ROOT))
    t.add_argument("--notes", required=True)
    t.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "served":
        return cmd_served(a)
    if a.cmd == "build":
        return cmd_build(a)
    if a.cmd == "run":
        return cmd_run(a)
    return cmd_assemble(a)


if __name__ == "__main__":
    sys.exit(main())
