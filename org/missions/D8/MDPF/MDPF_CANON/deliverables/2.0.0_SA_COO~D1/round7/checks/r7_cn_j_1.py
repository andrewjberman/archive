"""Issuer check for MDPF_CANON CN-j-1: the read-only HISTORY LEAF over the dated category-views (FWD-9 Client chips).  2.0.0_SA_COO~D1, round 7.

    python r7_cn_j_1.py unit     [--root R]   the assembly function: order, absent-not-zero, omission, determinism, exact key set
    python r7_cn_j_1.py seam     [--root R]   the handler end to end on a stubbed S3 + the publisher's own tests
    python r7_cn_j_1.py real     [--root R]   offline on the REAL dated category-views of all four scopes (read-only S3 gets)
    python r7_cn_j_1.py selftest [--root R]   the arms pass on a scratch reference and two planted mutants turn RED

Every arm prints `  <ARM> PASS|FAIL <detail>`, then `ROUND 7 CN-J-1 <NAME>: k of n arms`.  Exit 0 only when all arms pass.
R = a repo root holding infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher (default: this repository).  The publisher package is COPIED
to a temp dir before anything runs, so the product tree is never written (the publisher's own tests write adjacent roster/axis copies).
A control arm (marked) passes at the base so the instrument is shown able to read.  Client data: no account id is read or printed.
"""
from __future__ import annotations

import ast
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

REL = "infra/aws/lambda/opal-assets/opal-assets-mdpf-portal-publisher"
HERE = os.path.dirname(os.path.abspath(__file__))
SCOPES = ("49financial", "inflection", "cottonwood", "global")
TYPES = ("aggregate-aua-timeseries", "aum-metrics", "account-distribution", "category-views")
SUP, UNS = "Client - Opal Supervised", "Client - Opal Unsupervised"
LEAF = "category-views-history"
LEAF_KEYS = {"schema", "leaf", "scope", "n_dates", "dates", "client_supervised", "client_unsupervised", "omitted", "_provenance"}
ROSTER = {"partners": [{"firm_id": f, "legs": {"model": {"quantities": {"value": {"effective_from": "2026-05-01", "effective_to": None}}}}}
                       for f in ("49financial", "inflection", "cottonwood")]}
AXIS = {"schema": "mdpf-publisher-artifact-type-axis/v1",
        "derived_from": {"repo_path": "data/mdpf/scripts/gold/mdpf_gold_consolidator.py", "commit": "0" * 40, "source_sha256": "0" * 64,
                         "symbol": "ARTIFACT_TYPE_SCOPE_SET"},
        "declared_scopes": sorted(SCOPES), "types": {t: {"scope_set": "all-scope", "scopes_excluded": []} for t in TYPES}}


def _root(argv):
    if "--root" in argv:
        return os.path.abspath(argv[argv.index("--root") + 1])
    d = HERE
    for _ in range(12):
        if os.path.isdir(os.path.join(d, "infra")) and os.path.isdir(os.path.join(d, "org")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("repo root not found")


class Arms:
    def __init__(self, name):
        self.name, self.res = name, []

    def arm(self, aid, ok, detail):
        print("  %s %s: %s" % (aid, "PASS" if ok else "FAIL", detail))
        self.res.append(bool(ok))
        return bool(ok)

    def done(self):
        k = sum(self.res)
        print("ROUND 7 CN-J-1 %s: %d of %d arms" % (self.name, k, len(self.res)))
        return 0 if k == len(self.res) else 1


def _copy_pkg(root):
    src = os.path.join(root, *REL.split("/"))
    tmp = tempfile.mkdtemp(prefix="cnj1_")
    dst = os.path.join(tmp, "pkg")
    os.makedirs(os.path.join(dst, "tests"))
    shutil.copy(os.path.join(src, "lambda_function.py"), dst)
    for n in os.listdir(os.path.join(src, "tests")):
        if n.endswith(".py"):
            shutil.copy(os.path.join(src, "tests", n), os.path.join(dst, "tests", n))
    with open(os.path.join(dst, "partner_roster.json"), "w", encoding="utf-8") as fh:
        json.dump(ROSTER, fh)
    with open(os.path.join(dst, "artifact_types.json"), "w", encoding="utf-8") as fh:
        json.dump(AXIS, fh)
    return dst


_N = [0]


def _load(pkg):
    _N[0] += 1
    spec = importlib.util.spec_from_file_location("lf_cnj1_%d" % _N[0], os.path.join(pkg, "lambda_function.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class StubS3:
    def __init__(self, objects):
        self.objects, self.put_calls, self.get_calls = dict(objects), [], []

    def list_objects_v2(self, Bucket, Prefix, **kw):  # noqa: N803
        c = [{"Key": k, "Size": len(v), "ETag": '"x"'} for k, v in sorted(self.objects.items()) if k.startswith(Prefix)]
        return {"Contents": c, "IsTruncated": False}

    def get_object(self, Bucket, Key):  # noqa: N803
        self.get_calls.append((Bucket, Key))
        if Key not in self.objects:
            raise KeyError("NoSuchKey: %s" % Key)
        return {"Body": io.BytesIO(self.objects[Key])}

    def put_object(self, Bucket, Key, Body, **kw):  # noqa: N803
        self.put_calls.append(Key)
        self.objects[Key] = Body
        return {}


def _cv(date, sup, uns, with_as_of=True):
    d = {"nodes": {"Client": {"children": {}}}}
    if sup is not None:
        d["nodes"]["Client"]["children"][SUP] = {"aum": sup}
    if uns is not None:
        d["nodes"]["Client"]["children"][UNS] = {"aum": uns}
    if with_as_of:
        d["as_of"] = date
    return json.dumps(d).encode()


def _gold(extra=None):
    o = {}
    for s in SCOPES:
        for t in TYPES:
            if t != "category-views":
                o["portal/gold/mdpf/%s/%s/2026-08-05.json" % (s, t)] = json.dumps({"scope": s, "type": t, "v": 1}).encode()
        for i, d in enumerate(("2026-08-03", "2026-08-04", "2026-08-05")):
            o["portal/gold/mdpf/%s/category-views/%s.json" % (s, d)] = _cv(d, 100.0 * (i + 1) + len(s), 0.0 if i == 1 else 7.5 * (i + 1))
    o["portal/gold/mdpf/cottonwood/account-units/2026-08-05.json"] = b'{"v": 1}'
    o["portal/gold/mdpf/global/non-model-assets/2026-08-05.json"] = b'{"v": 1}'
    if extra:
        o.update(extra)
    return o


def _run(mod, s3):
    mod.boto3 = type("B", (), {"client": staticmethod(lambda *a, **k: s3)})
    return mod.lambda_handler({"source": "aws.events"}, None)


def _serve_writes(s3, only_history=None):
    out = [k for k in s3.put_calls if not k.startswith("platinum/mdpf/_manifests/")]
    if only_history is True:
        return [k for k in out if k.endswith(LEAF + ".json")]
    if only_history is False:
        return [k for k in out if not k.endswith(LEAF + ".json")]
    return out


def _manifest(s3, r):
    return json.loads(s3.objects[r["manifest_key"]])


# ----------------------------------------------------------------------------------------------------------------------------- unit
def unit(root):
    A = Arms("UNIT")
    pkg = _copy_pkg(root)
    mod = _load(pkg)
    fn = getattr(mod, "assemble_history_leaf", None)
    A.arm("U1", fn is not None and getattr(mod, "HISTORY_LEAF", None) == LEAF,
          "assemble_history_leaf %s; HISTORY_LEAF=%r" % ("present" if fn else "absent", getattr(mod, "HISTORY_LEAF", None)))
    ok, detail = False, "no function"
    if fn:
        try:
            shuffled = [("2026-08-04", _cv("2026-08-04", 2.0, 0.0)), ("2026-08-03", _cv("2026-08-03", 1.0, 5.0)), ("2026-08-05", _cv("2026-08-05", 3.0, 9.0))]
            c, om = fn("global", shuffled)
            ok = c["dates"] == ["2026-08-03", "2026-08-04", "2026-08-05"] and c["client_supervised"] == [1.0, 2.0, 3.0] and c["client_unsupervised"] == [5.0, 0.0, 9.0]
            detail = "input in shuffled order -> dates %s, sup %s, uns %s" % (c["dates"], c["client_supervised"], c["client_unsupervised"])
        except Exception as e:  # noqa: BLE001
            detail = "%s: %s" % (type(e).__name__, str(e)[:120])
    A.arm("U2", ok, detail)
    ok, detail = False, "no function"
    if fn:
        try:
            c, _ = fn("x", [("2026-08-03", _cv("2026-08-03", None, 4.0)), ("2026-08-04", _cv("2026-08-04", 6.0, None)),
                            ("2026-08-05", json.dumps({"as_of": "2026-08-05", "nodes": {}}).encode()),
                            ("2026-08-06", json.dumps({"as_of": "2026-08-06", "nodes": {"Client": {"children": {SUP: {"aum": None}, UNS: {"aum": 0.0}}}}}).encode())])
            ok = (c["client_supervised"] == [None, 6.0, None, None] and c["client_unsupervised"] == [4.0, None, None, 0.0]
                  and c["dates"] == ["2026-08-03", "2026-08-04", "2026-08-05", "2026-08-06"])
            detail = "missing node/None -> null (not 0.0), a measured 0.0 stays 0.0: sup %s uns %s" % (c["client_supervised"], c["client_unsupervised"])
        except Exception as e:  # noqa: BLE001
            detail = "%s: %s" % (type(e).__name__, str(e)[:120])
    A.arm("U3", ok, detail)
    ok, detail = False, "no function"
    if fn:
        try:
            c, om = fn("x", [("2026-08-03", _cv("2026-08-03", 1.0, 2.0)), ("2026-08-04", b"{not json"), ("2026-08-05", b"[1,2]"),
                             ("2026-08-06", _cv("2026-08-09", 3.0, 4.0))])
            reasons = {o["date"]: o["reason"] for o in om}
            ok = (c["dates"] == ["2026-08-03"] and reasons == {"2026-08-04": "unparseable", "2026-08-05": "not_an_object", "2026-08-06": "as_of_differs_from_key"}
                  and c["omitted"] == om)
            detail = "dates %s; omitted named %s" % (c["dates"], reasons)
        except Exception as e:  # noqa: BLE001
            detail = "%s: %s" % (type(e).__name__, str(e)[:120])
    A.arm("U4", ok, detail)
    ok, detail = False, "no function"
    if fn:
        try:
            ds = [("2026-08-03", _cv("2026-08-03", 1.0, 2.0)), ("2026-08-04", _cv("2026-08-04", 3.0, 4.0))]
            c1, _ = fn("global", ds)
            c2, _ = fn("global", list(reversed(ds)))
            s1, s2 = mod._content_sha(c1), mod._content_sha(c2)
            ok = c1 == c2 and s1 == s2 and len(s1) == 64
            detail = "same dated objects, either order -> equal content and equal content sha (%s...)" % s1[:12]
        except Exception as e:  # noqa: BLE001
            detail = "%s: %s" % (type(e).__name__, str(e)[:120])
    A.arm("U5", ok, detail)
    ok, detail = False, "no function"
    if fn:
        try:
            c, _ = fn("global", [("2026-08-03", _cv("2026-08-03", 1.0, 2.0))])
            extra = sorted(set(c) - (LEAF_KEYS - {"_provenance"}))
            lens = {len(c["dates"]), len(c["client_supervised"]), len(c["client_unsupervised"])}
            vals = all(v is None or isinstance(v, (int, float)) for v in c["client_supervised"] + c["client_unsupervised"])
            ok = not extra and set(c) == LEAF_KEYS - {"_provenance"} and len(lens) == 1 and vals and c["n_dates"] == len(c["dates"])
            detail = "key set %s; extra %s; array lengths %s; values numbers or null" % (sorted(c), extra, sorted(lens))
        except Exception as e:  # noqa: BLE001
            detail = "%s: %s" % (type(e).__name__, str(e)[:120])
    A.arm("U6", ok, detail)
    shutil.rmtree(os.path.dirname(pkg), ignore_errors=True)
    return A.done()


# ----------------------------------------------------------------------------------------------------------------------------- seam
def _ast_facts(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    doc_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)) and node.body and isinstance(node.body[0], ast.Expr) \
                and isinstance(getattr(node.body[0], "value", None), ast.Constant):
            doc_ids.add(id(node.body[0].value))
    root_literals = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and "platinum/mdpf" in node.value and id(node) not in doc_ids:
            root_literals += 1
    return root_literals


def seam(root):
    A = Arms("SEAM")
    pkg = _copy_pkg(root)
    mod = _load(pkg)
    has_fn = hasattr(mod, "assemble_history_leaf")
    s3 = StubS3(_gold())
    try:
        r1 = _run(mod, s3)
        err = ""
    except Exception as e:  # noqa: BLE001
        r1, err = None, "%s: %s" % (type(e).__name__, str(e)[:140])
    ok, detail = False, err or "run did not complete"
    if r1 is not None:
        leaves = {s: s3.objects.get("platinum/mdpf/%s/%s.json" % (s, LEAF)) for s in SCOPES}
        got = all(v is not None for v in leaves.values())
        match = False
        if got:
            match = True
            for i, s in enumerate(SCOPES):
                d = json.loads(leaves[s])
                exp_sup = [100.0 * (j + 1) + len(s) for j in range(3)]
                exp_uns = [7.5, 0.0, 22.5]
                match = match and d["dates"] == ["2026-08-03", "2026-08-04", "2026-08-05"] and d["client_supervised"] == exp_sup and d["client_unsupervised"] == exp_uns \
                    and d["_provenance"]["written_by"] == "opal-assets-mdpf-portal-publisher"
        ok = got and match
        detail = "leaves written for %d of 4 scopes at platinum/mdpf/<scope>/%s.json; values equal the dated nodes: %s" % (sum(v is not None for v in leaves.values()), LEAF, match)
    A.arm("S1", ok, detail)
    ok, detail = False, err or "no run"
    if r1 is not None:
        ok = r1["all_present"] is True and r1["published"] == 18 and r1["missing_pairs"] == [] and r1["unexpected_pairs"] == [] \
            and len(_serve_writes(s3, only_history=False)) == 18
        detail = "pairs unchanged by the leaf: published %s, all_present %s, missing %s, unexpected %s, non-leaf serve writes %d" % (
            r1["published"], r1["all_present"], r1["missing_pairs"], r1["unexpected_pairs"], len(_serve_writes(s3, only_history=False)))
    A.arm("S2", ok, detail)
    ok, detail = False, err or "no run"
    if r1 is not None:
        s3.put_calls.clear()
        r2 = _run(mod, s3)
        m2 = _manifest(s3, r2)
        hr = m2.get("history_rows") or {}
        ptr = json.loads(s3.objects["platinum/mdpf/_manifests/latest.json"])
        ok = _serve_writes(s3) == [] and len(hr) == 4 and all(v.get("status") == "unchanged" for v in hr.values()) \
            and len(ptr.get("history_rows") or {}) == 4 and r2["unchanged"] == 18
        detail = "second run: serve writes %d (must be 0), history_rows %d all unchanged=%s, pointer history_rows %d" % (
            len(_serve_writes(s3)), len(hr), all(v.get("status") == "unchanged" for v in hr.values()) if hr else False, len(ptr.get("history_rows") or {}))
    A.arm("S3", ok, detail)
    ok, detail = False, err or "no run"
    if r1 is not None:
        s3.objects["portal/gold/mdpf/global/category-views/2026-08-06.json"] = _cv("2026-08-06", 999.0, 1.0)
        s3.put_calls.clear()
        _run(mod, s3)
        w = sorted(_serve_writes(s3))
        want = ["platinum/mdpf/global/category-views-history.json", "platinum/mdpf/global/category-views.json"]
        ok = w == want
        detail = "a new dated global object -> exactly %s rewritten (got %s)" % (want, w)
    A.arm("S4", ok, detail)
    ok, detail = False, "no function" if not has_fn else ""
    if has_fn:
        s5 = StubS3(_gold({"portal/gold/mdpf/inflection/category-views/2026-08-04.json": b"{garbage"}))
        try:
            r5 = _run(mod, s5)
            hr = _manifest(s5, r5).get("history_rows") or {}
            inf = json.loads(s5.objects["platinum/mdpf/inflection/%s.json" % LEAF])
            others = all(("platinum/mdpf/%s/%s.json" % (s, LEAF)) in s5.objects for s in SCOPES)
            om = (hr.get("inflection/" + LEAF) or {}).get("omitted")
            ok = inf["dates"] == ["2026-08-03", "2026-08-05"] and om == [{"date": "2026-08-04", "reason": "unparseable"}] and others and r5["all_present"] is True
            detail = "malformed dated object: inflection dates %s, omitted named %s, other scopes still written=%s, all_present %s" % (inf["dates"], om, others, r5["all_present"])
        except Exception as e:  # noqa: BLE001
            detail = "%s: %s" % (type(e).__name__, str(e)[:140])
    A.arm("S5", ok, detail)
    ok, detail = False, "no function" if not has_fn else ""
    if has_fn:
        g6 = {k: v for k, v in _gold().items() if "/cottonwood/category-views/" not in k}
        s6 = StubS3(g6)
        try:
            r6 = _run(mod, s6)
            wrote = [k for k in s6.put_calls if "/cottonwood/" in k and k.endswith(LEAF + ".json")]
            ok = wrote == [] and "cottonwood/category-views" in (r6["missing_pairs"] or []) and r6["all_present"] is False
            detail = "no cottonwood category-views: no cottonwood leaf written (%s), missing_pairs still names it, all_present %s" % (wrote, r6["all_present"])
        except Exception as e:  # noqa: BLE001
            detail = "%s: %s" % (type(e).__name__, str(e)[:140])
    A.arm("S6", ok, detail)
    lits = _ast_facts(os.path.join(pkg, "lambda_function.py"))
    served_reads = []
    ok7 = False
    if r1 is not None:
        s7 = StubS3(_gold())
        _run(mod, s7)
        s7.get_calls.clear()
        _run(mod, s7)
        served_reads = [k for (b, k) in s7.get_calls if b == mod.SERVE_BUCKET]
        ok7 = served_reads == ["platinum/mdpf/_manifests/latest.json"] and lits <= 1
    A.arm("S7", ok7, "CONTROL-SHAPED: on a steady-state run the leaf adds NO read of the served plane -- the only served-plane read is the pointer, %s (measured 2026-10-13: the role has no GetObject on the pointer, manifest 20261013T135047Z-4fca44fb prior_pointer_note AccessDenied) -- and the module carries %d non-docstring 'platinum/mdpf' literal(s) (limit 1: the SERVE_ROOT default)" % (served_reads, lits))
    ok, detail = False, ""
    try:
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider", "tests"], cwd=pkg,
                           capture_output=True, text=True, timeout=110)
        tail = (p.stdout.strip().splitlines() or [""])[-1]
        ok = p.returncode == 0 and "passed" in tail and "failed" not in tail
        detail = "publisher tests dir (copied): rc=%d %s" % (p.returncode, tail[:110])
    except subprocess.TimeoutExpired:
        detail = "pytest timed out at 110 s"
    A.arm("S8", ok, detail)
    shutil.rmtree(os.path.dirname(pkg), ignore_errors=True)
    return A.done()


# ----------------------------------------------------------------------------------------------------------------------------- real
def real(root):
    import boto3
    A = Arms("REAL")
    pkg = _copy_pkg(root)
    mod = _load(pkg)
    fn = getattr(mod, "assemble_history_leaf", None)
    s3 = boto3.client("s3", region_name="us-east-1")
    B = "opal-data-assets"
    listing, bodies = {}, {}
    for s in SCOPES:
        ks = []
        for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=B, Prefix="portal/gold/mdpf/%s/category-views/" % s):
            ks += [o["Key"] for o in pg.get("Contents", []) if o["Key"].endswith(".json")]
        listing[s] = sorted(ks)
        bodies[s] = [(k.split("/")[-1][:-5], s3.get_object(Bucket=B, Key=k)["Body"].read()) for k in listing[s]]
    A.arm("R0", all(len(v) > 0 for v in listing.values()),
          "CONTROL: the dated category-views read for all four scopes: %s" % {s: len(listing[s]) for s in SCOPES})
    leaves = {}
    ok, detail = False, "no function"
    if fn:
        try:
            for s in SCOPES:
                leaves[s], _ = fn(s, bodies[s])
            ok = all(leaves[s]["n_dates"] + len(leaves[s]["omitted"]) == len(bodies[s]) for s in SCOPES) and all(len(leaves[s]["omitted"]) == 0 for s in SCOPES)
            detail = "dates in leaf / dated objects: %s; omitted %s" % ({s: "%d/%d" % (leaves[s]["n_dates"], len(bodies[s])) for s in SCOPES}, {s: len(leaves[s]["omitted"]) for s in SCOPES})
        except Exception as e:  # noqa: BLE001
            detail = "%s: %s" % (type(e).__name__, str(e)[:140])
    A.arm("R1", ok, detail)
    both = {}
    for s in SCOPES:
        n = 0
        for _d, b in bodies[s]:
            ch = (((json.loads(b).get("nodes") or {}).get("Client") or {}).get("children")) or {}
            n += 1 if (SUP in ch and UNS in ch) else 0
        both[s] = "%d/%d" % (n, len(bodies[s]))
    A.arm("R2", all(v.split("/")[0] == v.split("/")[1] for v in both.values()), "CONTROL: both Client nodes present on every dated object (independent read): %s" % both)
    ok, detail = False, "no function"
    if leaves:
        bad, cells = [], 0
        for s in SCOPES:
            for i, (d, b) in enumerate(bodies[s]):
                ch = json.loads(b)["nodes"]["Client"]["children"]
                for name, arr in ((SUP, "client_supervised"), (UNS, "client_unsupervised")):
                    cells += 1
                    if leaves[s]["dates"][i] != d or leaves[s][arr][i] != ch[name]["aum"]:
                        bad.append((s, d, arr))
        ok = not bad
        detail = "leaf value == the node's aum, independently extracted: %d cells compared, %d unequal %s" % (cells, len(bad), bad[:3])
    A.arm("R3", ok, detail)
    ok, detail = False, "no function"
    if leaves:
        asc = all(leaves[s]["dates"] == sorted(set(leaves[s]["dates"])) for s in SCOPES)
        ends = all(leaves[s]["dates"][0] == bodies[s][0][0] and leaves[s]["dates"][-1] == bodies[s][-1][0] for s in SCOPES)
        sizes = {s: len(json.dumps(leaves[s], separators=(",", ":"))) for s in SCOPES}
        ok = asc and ends and max(sizes.values()) < 65536
        detail = "ascending and unique=%s; first/last date = the listing's=%s; size (B) %s (limit 65536)" % (asc, ends, sizes)
    A.arm("R4", ok, detail)
    ok, detail = False, "no function"
    if leaves:
        sh = {s: mod._content_sha(leaves[s]) for s in SCOPES}
        again = {s: mod._content_sha(fn(s, list(reversed(bodies[s])))[0]) for s in SCOPES}
        ok = sh == again
        detail = "content sha equal on a second assembly in reverse input order: %s" % ok
    A.arm("R5", ok, detail)
    shutil.rmtree(os.path.dirname(pkg), ignore_errors=True)
    return A.done()


# ----------------------------------------------------------------------------------------------------------------------------- selftest
def selftest(root):
    sys.path.insert(0, os.path.join(HERE, "ref"))
    import make_reference_publisher_j1 as ref
    tmp = tempfile.mkdtemp(prefix="cnj1_ref_")
    out = []

    def run(sub, r):
        buf = io.StringIO()
        old, sys.stdout = sys.stdout, buf
        try:
            rc = {"unit": unit, "seam": seam}[sub](r)
        finally:
            sys.stdout = old
        return rc, buf.getvalue()

    ref.build(root, tmp)
    for sub in ("unit", "seam"):
        rc, txt = run(sub, tmp)
        out.append(("reference %s" % sub, rc == 0, txt.strip().splitlines()[-1]))
    for mut, sub, arm in (("m1", "unit", "U3"), ("m2", "seam", "S3")):
        mtmp = tempfile.mkdtemp(prefix="cnj1_mut_")
        ref.build(root, mtmp, mut)
        rc, txt = run(sub, mtmp)
        red = [ln for ln in txt.splitlines() if ln.startswith("  %s FAIL" % arm)]
        out.append(("mutant %s -> %s RED" % (mut, arm), rc != 0 and bool(red), (red[0].strip()[:110] if red else txt.strip().splitlines()[-1])))
        shutil.rmtree(mtmp, ignore_errors=True)
    shutil.rmtree(tmp, ignore_errors=True)
    for name, ok, d in out:
        print("  %s %s: %s" % ("OK " if ok else "BAD", name, d))
    allok = all(o[1] for o in out)
    print("ROUND 7 CN-J-1 SELFTEST: %s" % ("OK" if allok else "NOT OK"))
    return 0 if allok else 1


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("unit", "seam", "real", "selftest"):
        print(__doc__)
        return 2
    root = _root(sys.argv)
    return {"unit": unit, "seam": seam, "real": real, "selftest": selftest}[sys.argv[1]](root)


if __name__ == "__main__":
    sys.exit(main())
