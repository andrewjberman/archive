#!/usr/bin/env python3
"""IRPT_BCKEND IB-pr-539 (round 195, workstream ~P) -- the LIVE-against-PIN differential of the holdings producer.

READ ONLY. Each tree's producer is imported from that tree, in its own subprocess (both trees export a module named
holdings_snapshot). The S3 client is wrapped: any operation whose name does not begin with get_, list_ or head_ is
refused and counted, so the harness cannot mutate state or send anything. Source objects are read through the
producer's own VersionedInputs; the candidate of each tree is built from the same pinned source receipts.

Subcommands:
  build   one tree, one firm: build the candidate as the tree stands (and, for the pin, once more with apply_cash_rule
          replaced by identity, inside this process only), write the per-node signature, the receipts, the publish-gate
          evaluation of the candidate (when asked) and the metadata. Writes nothing to S3.
  run     the whole per-firm sequence: pin builds, live build, one hybrid build per behaviour or data member of the
          firm's packet v2 table (the live tree with that one member replaced by the pin bytes), the second pair of
          builds on the same receipts, the comparison step run twice, and the planted mutant.
  assemble  the record JSON from the three per-firm results and the notes file.

Every output goes outside the repository (scratch). The comparison compares per-node signatures: rows by kind, the
account set, numeric leaves with an absolute tolerance, the classification fields, the non-numeric residue of each
top-level field, and the publish gate on each code's own candidate.
"""
import argparse
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

PIN_TREE = Path("C:/dev/wk-ib539-pin")
PIN = "49467335d288d5c0012fe339c4cafcb74bd43fb5"
FIRMS = ("49financial", "cottonwood", "inflection")
AS_OF = {"49financial": "2026-10-12", "cottonwood": "2026-10-12", "inflection": "2026-10-13"}
SIGNED = {"49financial": 32, "cottonwood": 249, "inflection": 841}
CLASS_FIELDS = ("asset_class", "asset_class_basis", "sub_asset_class", "class_source")
TOL = 0.01
NAMED = re.compile(r"account_id|keyed|CUSIP|SC-e-56|multi_asset", re.I)
READ_OPS = ("get_", "list_", "head_")
PRODUCER = ("data", "assets", "scripts", "gold", "investor_reporting")
DEFAULT_WORK = "C:/dev/_scratch384/run"
DEFAULT_HYB = "C:/dev/_scratch384/hyb"
DEFAULT_LIVE = "C:/dev/_scratch384/live"
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
    """One record per node: id, kind, the raw classification fields, every numeric leaf by field path, and a short
    hash of the non-numeric residue of EVERY top-level field."""
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


def gate_eval(hs, client, firm, snap):
    """The publish gate as the tree's own orchestration calls it (read calls only): begin, served_publication,
    evaluate_publish_gate with closed_account_ids and directory_marks_no_closures bound to the firm's bucket."""
    publisher = hs.HoldingsPublication(client, firm, qa=False)
    expected = publisher.begin()
    served = hs.served_publication(publisher, expected)
    gate = hs.evaluate_publish_gate(
        snap, served,
        lambda: hs.closed_account_ids(client, hs.firm_bucket_map().get(firm, ""), firm),
        lambda: hs.directory_marks_no_closures(client, hs.firm_bucket_map().get(firm, ""), firm))
    return {"outcome": gate["outcome"], "conditions": [c["condition"] for c in gate.get("conditions", [])]}


def cmd_build(a):
    tree = Path(a.tree).resolve()
    sys.path[:0] = [str(tree.joinpath(*PRODUCER)), str(tree / "lib")]
    import holdings_snapshot as hs
    mod = Path(hs.__file__).resolve()
    if not str(mod).lower().startswith(str(tree).lower()):
        raise SystemExit("REFUSED: the producer imported from outside its tree: %s" % mod)
    import boto3
    client = ReadOnlyS3(boto3.client("s3", region_name="us-east-1"))
    inputs = hs.VersionedInputs(client)
    seed = json.loads(Path(a.seed).read_text(encoding="utf-8")) if a.seed else []
    for ref in seed:
        inputs._refs[(ref["bucket"], ref["key"])] = dict(ref)
    seeded = {(ref["bucket"], ref["key"]) for ref in seed}
    meta = {"label": a.label, "firm": a.firm, "as_of": a.as_of, "producer_module_under_tree": True,
            "seeded_objects": len(seeded)}
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
        gate = gate_eval(hs, client, a.firm, snap)
        Path(a.gate_out).write_text(json.dumps(gate, sort_keys=True, indent=1), encoding="utf-8")
        meta["gate"] = gate["outcome"]
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

def label_val(v):
    return "(absent)" if v is None else str(v)


def diff_items(lr, p):
    items = []
    for f in CLASS_FIELDS:
        a, b = lr["cls"].get(f), p["cls"].get(f)
        if a != b:
            items.append({"kind": "cls", "field": f, "label": "%s: %s -> %s" % (f, label_val(a), label_val(b)),
                          "delta": None})
    for path in sorted(set(lr["num"]) | set(p["num"])):
        a, b = lr["num"].get(path), p["num"].get(path)
        if a is None or b is None:
            if a != b:
                items.append({"kind": "presence", "field": path, "label": "%s: presence change" % path, "delta": None})
        elif abs(a - b) > TOL:
            items.append({"kind": "num", "field": path, "label": "%s: numeric change" % path, "delta": abs(a - b)})
    for f in sorted(set(lr["res"]) | set(p["res"])):
        if lr["res"].get(f) != p["res"].get(f):
            items.append({"kind": "res", "field": f, "label": "%s: non-numeric change" % f, "delta": None})
    return items


def val_of(rec, item):
    k = item["kind"]
    if k == "cls":
        return rec["cls"].get(item["field"])
    if k in ("num", "presence"):
        return rec["num"].get(item["field"])
    return rec["res"].get(item["field"])


def close(a, b, kind):
    if kind in ("num", "presence"):
        if a is None or b is None:
            return a is None and b is None
        return abs(a - b) <= TOL
    return a == b


def changed_nodes(L, P):
    out = {}
    for nid in sorted((k for k in L if k in P), key=str):
        items = diff_items(L[nid], P[nid])
        if items:
            out[nid] = items
    return out


def git_commits(member, live_commit):
    rng = ["%s..%s" % (live_commit, PIN)] if live_commit else [PIN]
    cmd = ["git", "-C", str(PIN_TREE), "log", "--format=%H%x09%s"] + rng + ["--", member]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise SystemExit("REFUSED: git log failed for a member")
    out = []
    for line in p.stdout.splitlines():
        h, _, subj = line.partition("\t")
        if re.fullmatch(r"[0-9a-f]{40}", h) and NAMED.search(subj):
            out.append(h)
    return sorted(set(out))


def gate_attr(firm, gl, gp):
    if gl["outcome"] == gp["outcome"] and sorted(gl["conditions"]) == sorted(gp["conditions"]):
        return "same"
    if (firm == "cottonwood" and gl["outcome"] == "REFUSED" and gp["outcome"] == "PUBLISHED"
            and set(gl["conditions"]) - set(gp["conditions"]) == {"account_lost"}
            and set(gp["conditions"]) <= set(gl["conditions"])):
        return "signed_exemption_repair"
    return "UNATTRIBUTED"


def compare_once(firm, live_rows, pin_rows, ident_rows, gate_live, gate_pin, hyb_files, members, v2_info, mutant=False):
    """The comparison step. Returns the result dict and its digest. With mutant=True it changes one asset_class value
    in the pin signature in memory and returns only the changed-node count."""
    L = {r["id"]: r for r in live_rows}
    P = {r["id"]: r for r in pin_rows}
    if mutant:
        cand = sorted((k for k in L if k in P and L[k]["kind"] == "SECURITY"
                       and L[k]["cls"].get("asset_class") is not None
                       and L[k]["cls"].get("asset_class") == P[k]["cls"].get("asset_class")), key=str)
        pick = cand[0]
        saved = P[pick]["cls"]["asset_class"]
        P[pick]["cls"]["asset_class"] = "__mutant__"
        count = len(changed_nodes(L, P))
        P[pick]["cls"]["asset_class"] = saved
        return {"planted": "one asset_class value changed in the pin signature", "flagged": count == len(changed_nodes(L, P)) + 1,
                "changed_nodes_with_mutant": count}
    rows = {"live": dict(Counter(r["kind"] for r in live_rows)), "pin": dict(Counter(r["kind"] for r in pin_rows))}
    AL = {k for k, r in L.items() if r["kind"] == "ACCOUNT"}
    AP = {k for k, r in P.items() if r["kind"] == "ACCOUNT"}
    account_set = {"only_live": len(AL - AP), "only_pin": len(AP - AL), "both": len(AL & AP)}
    changed = changed_nodes(L, P)
    num_nodes, largest = 0, (0.0, "none")
    for nid, items in changed.items():
        if any(i["kind"] == "num" for i in items):
            num_nodes += 1
        for i in items:
            if i["kind"] == "num" and i["delta"] > largest[0]:
                largest = (i["delta"], i["field"])
    cset = set(changed)
    ident_ac = {}
    for r in ident_rows or []:
        if r["id"] in cset:
            ident_ac[r["id"]] = r["cls"].get("asset_class")
    hyb = {}
    for member, path in hyb_files:
        rows_h = load_gz(path)
        hyb[member] = {r["id"]: r for r in rows_h if r["id"] in cset}
        del rows_h
    commit_cache = {}
    member_info = v2_info

    def commits_for(member):
        if member not in commit_cache:
            commit_cache[member] = git_commits(member, member_info[member]["live_commit"])
        return commit_cache[member]

    groups, node_ok, signed = {}, {}, set()
    for nid, items in changed.items():
        ok = True
        for it in items:
            att, by, mem = "UNATTRIBUTED", "none", []
            l_rec, p_rec = L[nid], P[nid]
            l_ac = l_rec["cls"].get("asset_class")
            p_ac = p_rec["cls"].get("asset_class")
            id_ac = ident_ac.get(nid)
            if (it["kind"] == "cls" and it["field"] == "asset_class" and id_ac is not None
                    and p_ac != id_ac and l_ac == id_ac):
                att, by = "signed_cash_rule", "identity-patch"
                signed.add(nid)
            else:
                reproducers = []
                for m in sorted(hyb):
                    h = hyb[m].get(nid)
                    if h is None:
                        continue
                    hv, pv, lv = val_of(h, it), val_of(p_rec, it), val_of(l_rec, it)
                    if close(hv, pv, it["kind"]) and not close(hv, lv, it["kind"]):
                        reproducers.append(m)
                if reproducers:
                    cs = sorted(set(c for m in reproducers for c in commits_for(m)))
                    if cs:
                        att = "W383-S2:" + "+".join(sorted(os.path.splitext(os.path.basename(m))[0] for m in reproducers))
                        by, mem = "member-swap", sorted(reproducers)
            if att == "UNATTRIBUTED":
                ok = False
            g = groups.setdefault((it["label"], att, by), {"nodes": set(), "members": set()})
            g["nodes"].add(nid)
            g["members"].update(mem)
        node_ok[nid] = ok
    diffs = []
    for (label, att, by), g in sorted(groups.items()):
        mem = sorted(g["members"])
        cs = sorted(set(c for m in mem for c in commits_for(m)))
        diffs.append({"group": label, "nodes": len(g["nodes"]), "attribution": att, "attributed_by": by,
                      "members": mem, "commits": cs})
    total = len(changed)
    unatt = sum(1 for ok in node_ok.values() if not ok)
    gl, gp = gate_live, gate_pin
    res = {
        "firm": firm,
        "rows": rows,
        "account_set": account_set,
        "only_live_nodes": len(set(L) - set(P)),
        "only_pin_nodes": len(set(P) - set(L)),
        "duplicate_node_ids": {"live": len(live_rows) - len(L), "pin": len(pin_rows) - len(P)},
        "changed_values": {"tolerance": TOL, "nodes_with_changed_numeric_value": num_nodes,
                           "largest_abs_delta": round(largest[0], 6), "largest_delta_field": largest[1]},
        "gate": {"live": {"outcome": gl["outcome"], "conditions": sorted(gl["conditions"])},
                 "pin": {"outcome": gp["outcome"], "conditions": sorted(gp["conditions"])}},
        "gate_attribution": gate_attr(firm, gl, gp),
        "total_changed_nodes": total,
        "attributed_nodes": total - unatt,
        "unattributed_nodes": unatt,
        "signed_cash_rule_nodes": len(signed),
        "differences": diffs,
    }
    return res, digest_of(res)


def load_v2(path, firm):
    v2 = json.loads(Path(path).read_text(encoding="utf-8"))
    info = {}
    for m in v2["members"][firm]:
        if m["class"] in ("behaviour", "data"):
            info[m["path"]] = {"live_commit": m.get("live_commit"), "class": m["class"], "state": m["state"]}
    return info


def make_hybrid(live_dir, member, dest):
    if dest.exists():
        shutil.rmtree(str(dest))
    shutil.copytree(str(live_dir), str(dest))
    target = dest / member
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(str(PIN_TREE / member), str(target))


MISSING = re.compile(r"No module named '([A-Za-z0-9_.]+)'")


def pin_python_files():
    """The .py paths the pin tracks under the producer's script, lib and lambda roots (names only)."""
    cmd = ["git", "-C", str(PIN_TREE), "ls-tree", "-r", "--name-only", PIN, "--", "data/assets/scripts", "lib",
           "infra/aws/lambda/investor-reporting"]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if p.returncode != 0:
        raise SystemExit("REFUSED: git ls-tree failed on the pin")
    return [x.strip() for x in p.stdout.splitlines() if x.strip().endswith(".py")]


def sub_build(*args, **kw):
    ok, err = try_build(*args, **kw)
    if not ok:
        raise SystemExit("REFUSED: build %s failed: %s" % (args[1], err[-600:]))


def try_build(work, label, tree, firm, as_of, out, meta_out, seed=None, gate_out=None, identity_out=None,
              receipts_out=None):
    """Runs one build in its own process. Returns (True, "") or (False, stderr text); a build whose meta file exists
    is skipped (resume)."""
    if Path(meta_out).exists() and Path(out).exists():
        log("SKIP: %s already built (resume)" % label)
        return True, ""
    cmd = [sys.executable, "-I", str(HERE), "build", "--tree", str(tree), "--label", label, "--firm", firm,
           "--as-of", as_of, "--out", str(out), "--meta-out", str(meta_out)]
    for flag, val in (("--seed", seed), ("--gate-out", gate_out), ("--identity-out", identity_out),
                      ("--receipts-out", receipts_out)):
        if val:
            cmd += [flag, str(val)]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=5400)
    if p.returncode != 0:
        return False, (p.stderr or "")
    sys.stdout.write(p.stdout)
    sys.stdout.flush()
    return True, ""


def cmd_run(a):
    firm = a.firm
    as_of = AS_OF[firm]
    work = Path(a.work) / firm
    work.mkdir(parents=True, exist_ok=True)
    live_dir = Path(a.live) / firm
    hyb_root = Path(a.hyb) / firm
    v2_info = load_v2(a.v2_record, firm)
    members = sorted(v2_info)
    w = lambda name: work / name  # noqa: E731
    t_start = time.time()
    # Run 1 builds: pin (rule, identity, gate) then live (rule, gate) on the pin's receipts.
    sub_build(work, "pin_r1", PIN_TREE, firm, as_of, w("pin_r1.json.gz"), w("meta_pin_r1.json"),
              gate_out=w("gate_pin_r1.json"), identity_out=w("pin_id_r1.json.gz"), receipts_out=w("rec_r1.json"))
    sub_build(work, "live_r1", live_dir, firm, as_of, w("live_r1.json.gz"), w("meta_live_r1.json"),
              seed=w("rec_r1.json"), gate_out=w("gate_live_r1.json"))
    # Hybrids: the live tree with ONE member replaced by the pin bytes, on the run-1 receipts.
    hyb_index = []
    pin_files = pin_python_files()
    for i, m in enumerate(members):
        dest = hyb_root / ("h%02d" % i)
        deps_file = w("hyb_deps_%02d.json" % i)
        if w("meta_hyb_%02d.json" % i).exists() and w("hyb_%02d.json.gz" % i).exists():
            deps = json.loads(deps_file.read_text(encoding="utf-8")) if deps_file.exists() else []
            log("SKIP: hybrid %02d already built (resume), extra pin files %d" % (i, len(deps)))
            hyb_index.append({"i": i, "member": m, "extra_pin_files": deps})
            continue
        make_hybrid(live_dir, m, dest)
        deps = []
        # A missing module is a pin-only import the packet's table does not name: copy that ONE pin file into this
        # hybrid, record it, and retry (at most four). Any other failure, or an ambiguous name, stops the run.
        for _attempt in range(5):
            ok, err = try_build(work, "hyb_%02d" % i, dest, firm, as_of, w("hyb_%02d.json.gz" % i),
                                w("meta_hyb_%02d.json" % i), seed=w("rec_r1.json"))
            if ok:
                break
            found = MISSING.search(err)
            name = found.group(1).split(".")[-1] + ".py" if found else None
            cands = [p for p in pin_files if name and os.path.basename(p) == name and p not in deps]
            if len(cands) != 1:
                raise SystemExit("REFUSED: hybrid %s did not build: %s" % (m, err[-400:]))
            target = dest / cands[0]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(PIN_TREE / cands[0]), str(target))
            deps.append(cands[0])
            log("NOTE: hybrid %02d needs pin-only module %s; copied into this hybrid only" % (i, cands[0]))
        else:
            raise SystemExit("REFUSED: hybrid %s still missing modules after four copies" % m)
        deps_file.write_text(json.dumps(deps), encoding="utf-8")
        hyb_index.append({"i": i, "member": m, "extra_pin_files": deps})
    Path(w("hyb_index.json")).write_text(json.dumps(hyb_index, indent=1), encoding="utf-8")
    # Run 2: fresh pairs of builds on the same receipts.
    sub_build(work, "pin_r2", PIN_TREE, firm, as_of, w("pin_r2.json.gz"), w("meta_pin_r2.json"),
              seed=w("rec_r1.json"), gate_out=w("gate_pin_r2.json"), identity_out=w("pin_id_r2.json.gz"),
              receipts_out=w("rec_r2.json"))
    sub_build(work, "live_r2", live_dir, firm, as_of, w("live_r2.json.gz"), w("meta_live_r2.json"),
              seed=w("rec_r1.json"), gate_out=w("gate_live_r2.json"))
    hyb_files = [(h["member"], w("hyb_%02d.json.gz" % h["i"])) for h in hyb_index]
    gl1 = json.loads(w("gate_live_r1.json").read_text(encoding="utf-8"))
    gp1 = json.loads(w("gate_pin_r1.json").read_text(encoding="utf-8"))
    gl2 = json.loads(w("gate_live_r2.json").read_text(encoding="utf-8"))
    gp2 = json.loads(w("gate_pin_r2.json").read_text(encoding="utf-8"))
    rec1 = json.loads(w("rec_r1.json").read_text(encoding="utf-8"))
    rec2 = json.loads(w("rec_r2.json").read_text(encoding="utf-8"))
    rec_same = digest_of(rec1) == digest_of(rec2)
    log("STEP: comparison run 1")
    live_r1, pin_r1 = load_gz(w("live_r1.json.gz")), load_gz(w("pin_r1.json.gz"))
    id_r1 = load_gz(w("pin_id_r1.json.gz"))
    res1, dig1 = compare_once(firm, live_r1, pin_r1, id_r1, gl1, gp1, hyb_files, members, v2_info)
    mutant_pin = pin_r1
    mutant = compare_once(firm, live_r1, mutant_pin, None, gl1, gp1, [], members, v2_info, mutant=True)
    mutant["flagged"] = mutant["changed_nodes_with_mutant"] == res1["total_changed_nodes"] + 1
    del live_r1, pin_r1, id_r1
    log("STEP: comparison run 2")
    live_r2, pin_r2 = load_gz(w("live_r2.json.gz")), load_gz(w("pin_r2.json.gz"))
    id_r2 = load_gz(w("pin_id_r2.json.gz"))
    res2, dig2 = compare_once(firm, live_r2, pin_r2, id_r2, gl2, gp2, hyb_files, members, v2_info)
    del live_r2, pin_r2, id_r2
    out = {"firm": firm, "as_of": as_of, "members_swapped": members, "result": res1, "run1_digest": dig1,
           "hybrid_extra_pin_files": {h["member"]: h["extra_pin_files"] for h in hyb_index if h["extra_pin_files"]},
           "run2_digest": dig2, "run2_result_equal": res1 == res2, "receipts_run2_equal_run1": rec_same,
           "mutant": mutant, "gate_run2_equal_run1": (gl1 == gl2 and gp1 == gp2),
           "meta": {k: json.loads(w(f).read_text(encoding="utf-8")) for k, f in
                    (("pin_r1", "meta_pin_r1.json"), ("live_r1", "meta_live_r1.json"),
                     ("pin_r2", "meta_pin_r2.json"), ("live_r2", "meta_live_r2.json"))},
           "seconds": round(time.time() - t_start)}
    Path(w("result.json")).write_text(json.dumps(out, sort_keys=True, indent=1), encoding="utf-8")
    log("OK: %s total=%d attributed=%d unattributed=%d run1=%s run2=%s equal=%s mutant_flagged=%s"
        % (firm, res1["total_changed_nodes"], res1["attributed_nodes"], res1["unattributed_nodes"], dig1[:12],
           dig2[:12], res1 == res2, mutant["flagged"]))
    return 0


def cmd_assemble(a):
    base = a.base_commit
    notes = json.loads(Path(a.notes).read_text(encoding="utf-8"))
    live_versions = json.loads(Path(a.versions).read_text(encoding="utf-8"))
    rec = {"base_commit": base, "pin": PIN,
           "custody_pins": {f: AS_OF[f] for f in FIRMS}, "live_versions": live_versions, "firms": {}}
    for f in FIRMS:
        r = json.loads(Path(a.work, f, "result.json").read_text(encoding="utf-8"))
        res = r["result"]
        rec["firms"][f] = {
            "rows": res["rows"], "account_set": res["account_set"], "changed_values": res["changed_values"],
            "gate": res["gate"], "gate_attribution": res["gate_attribution"],
            "total_changed_nodes": res["total_changed_nodes"], "attributed_nodes": res["attributed_nodes"],
            "unattributed_nodes": res["unattributed_nodes"], "differences": res["differences"],
            "run1_digest": r["run1_digest"], "run2_digest": r["run2_digest"], "mutant": r["mutant"],
        }
    rec["notes"] = notes
    for k in ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written",
              "vendor_requests_sent"):
        rec[k] = 0
    Path(a.out).write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    log("OK: wrote the differential record")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("build")
    b.add_argument("--tree", required=True)
    b.add_argument("--label", required=True)
    b.add_argument("--firm", required=True, choices=FIRMS)
    b.add_argument("--as-of", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--meta-out", required=True)
    b.add_argument("--seed")
    b.add_argument("--gate-out")
    b.add_argument("--identity-out")
    b.add_argument("--receipts-out")
    r = sp.add_parser("run")
    r.add_argument("--firm", required=True, choices=FIRMS)
    r.add_argument("--work", default=DEFAULT_WORK)
    r.add_argument("--live", default=DEFAULT_LIVE)
    r.add_argument("--hyb", default=DEFAULT_HYB)
    r.add_argument("--v2-record", required=True)
    s = sp.add_parser("assemble")
    s.add_argument("--work", default=DEFAULT_WORK)
    s.add_argument("--base-commit", required=True)
    s.add_argument("--versions", required=True)
    s.add_argument("--notes", required=True)
    s.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "build":
        return cmd_build(a)
    if a.cmd == "run":
        return cmd_run(a)
    return cmd_assemble(a)


if __name__ == "__main__":
    sys.exit(main())
