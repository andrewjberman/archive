#!/usr/bin/env python3
"""MDPF_CANON cell CN-h-1 (draft, round 7) -- the frontier account counts read the newest A4 account-distribution at or before
the axis date, never the staged runner object (S5 disarm; CTO round-5 ADDENDUM 5, msg 4782).

  python r6_cn_h_1.py reader       offline, a fake S3 client: the selection rule, the fail-closed branches, no staged read
  python r6_cn_h_1.py seams        static (AST): both call sites pass the axis date; the loader body names no staged key; the
                                   two existing test stubs accept the second argument; the stamp/staleness contract is intact
  python r6_cn_h_1.py comparator   the REAL served 2026-10-09 objects, read-only get/list: the module's own loader on real S3,
                                   the per-scope delta table, and the proof that no staged object key is requested

Each prints `  <ARM> PASS|FAIL <detail>` per arm and `CN-H-1 <NAME>: k of n arms`; exit 0 only when every arm passes.
Prints dates, counts and differences; never an account id. ASCII only. Bounded: a few seconds, <= 20 S3 calls.
R6_ROOT overrides the repo root (the issuer's reference-tree dry-run uses it).

  READER   H0 CONTROL (passes at base): the module imports and exposes load_account_dist_frontier_counts and
              frontier_stamp_staleness, and the staleness verdict set is unchanged.
           H1 the newest key at or before the axis date is read (axis on a key, between keys, after every key).
           H2 no A4 key at or before the axis date -> {} (honest absent) and the staged object is NEVER requested.
           H3 an A4 present but a staged object ALSO present: the staged one is never fetched (no fallback, ever).
           H4 a listing failure that is not absence RAISES (C2-sibling idiom), it never wears honest-None.
           H5 an A4 whose period is AFTER the axis date is refused ({}), never stamped.
           H6 the as-of sentinel carries the A4's own period; staleness reads FRESH on equal dates.
           H7 the worker's test file exists and passes (>= 5 tests).
  SEAMS    S1 every call of the loader passes the axis date (a second positional argument or axis_date=).
           S2 the loader's body names no staged key (no "gold/mdpf_revamp", no "account_distribution.json").
           S3 the two existing test stubs of the loader accept the second argument.
           S4 CONTROL (passes at base): meta.frontier_count carries exactly date, source, staleness (no new key).
  COMPARATOR  K0 CONTROL (passes at base): the served objects read, and the served frontier counts equal the staged roster
              on every mapped key (the freeze, measured).
           K1 the loader on real S3 at the served as_of_last returns the A4 of that date (as-of == axis date).
           K2 the per-scope delta table (printed) has at least one moved frontier count per scope and no count moves outside
              the keys the loader returns.
           K3 the loader on real S3 with an axis before every A4 returns {} (fail closed).
           K4 across K1-K3 no request named a staged gold/mdpf_revamp object.
"""
from __future__ import annotations

import ast
import json
import os
import subprocess
import sys

BUCKET = "opal-data-assets"
A4_FMT = "portal/gold/mdpf/%s/account-distribution/"
TS_FMT = "portal/gold/mdpf/%s/aggregate-aua-timeseries/"
STAGED_FMT = "gold/mdpf_revamp/%s/account_distribution.json"
MODULE = "data/mdpf/scripts/gold/dim_mdpf_aggregate_aua_timeseries.py"
TEST_FILE = "data/mdpf/tests/canon/test_frontier_counts_a4.py"
STUB_TESTS = ("data/mdpf/scripts/gold/tests/test_canplat_p1_1.py", "data/mdpf/scripts/gold/tests/test_global_fold_flag2.py")
SCOPES = ("global", "49financial", "inflection")
N = None


def _root() -> str:
    r = os.environ.get("R6_ROOT")
    if r:
        return r
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def _load_module(root: str):
    for sub in ("scripts/silver", "scripts/gold"):
        p = os.path.normpath(os.path.join(root, "data", "mdpf", sub))
        if p not in sys.path:
            sys.path.insert(0, p)
    if root not in sys.path:
        sys.path.insert(0, root)
    import importlib
    return importlib.import_module("dim_mdpf_aggregate_aua_timeseries")


# ------------------------------------------------------------------ fake S3 (offline arms)
class _Body:
    def __init__(self, b: bytes):
        self._b = b

    def read(self) -> bytes:
        return self._b


class _NoSuchKey(Exception):
    pass


class FakeS3:
    """Serves {key: dict} for get_object and a flat listing; records every get and list prefix."""

    class exceptions:                                         # noqa: N801 -- mirrors the boto3 client attribute
        NoSuchKey = _NoSuchKey

    def __init__(self, objects: dict, list_error: bool = False):
        self.objects = dict(objects)
        self.gets = []
        self.lists = []
        self.list_error = list_error

    def get_object(self, Bucket, Key):                        # noqa: N803
        self.gets.append(Key)
        if Key not in self.objects:
            raise _NoSuchKey(Key)
        return {"Body": _Body(json.dumps(self.objects[Key]).encode("utf-8"))}

    def get_paginator(self, name):
        outer = self

        class _P:
            def paginate(self, Bucket, Prefix):               # noqa: N803
                outer.lists.append(Prefix)
                if outer.list_error:
                    raise PermissionError("AccessDenied: s3:ListBucket")
                keys = sorted(k for k in outer.objects if k.startswith(Prefix))
                yield {"Contents": [{"Key": k} for k in keys]}
        return _P()


def _a4(scope, date, mapping, period=None):
    return (A4_FMT % scope + date + ".json",
            {"period": period or date, "meta": {"account_count_by_model_key": dict(mapping)}, "total": {"account_count": 1}})


# ------------------------------------------------------------------ reader arms
def reader(root: str) -> int:
    arms = []

    def arm(name, ok, detail):
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        arms.append(bool(ok))

    try:
        mod = _load_module(root)
    except Exception as exc:                                  # noqa: BLE001
        print("  import FAIL: %s: %s" % (type(exc).__name__, str(exc)[:160]))
        print("CN-H-1 READER: 0 of 8 arms")
        return 1
    fn = getattr(mod, "load_account_dist_frontier_counts", None)
    stale = getattr(mod, "frontier_stamp_staleness", None)

    # H0 control
    v = []
    if stale is not None:
        v = [stale("2026-10-09", "2026-10-09")["verdict"], stale("2026-10-08", "2026-10-09")["verdict"],
             stale("2026-10-12", "2026-10-09")["verdict"], stale(None, "2026-10-09")["verdict"]]
    arm("H0", fn is not None and v == ["FRESH", "STALE", "AHEAD_OF_AXIS", "UNKNOWN"],
        "loader present=%s; staleness verdicts %s" % (fn is not None, v))

    def run(objects, axis, scope="global", list_error=False):
        fake = FakeS3(objects, list_error=list_error)
        mod._s3 = lambda: fake                                # noqa: SLF001 -- the module's own client factory
        try:
            out = fn(scope, axis)
            return out, fake, ""
        except BaseException as exc:                          # noqa: BLE001
            return None, fake, "%s: %s" % (type(exc).__name__, str(exc)[:140])

    k08, o08 = _a4("global", "2026-10-08", {"opal_short_term": 800})
    k09, o09 = _a4("global", "2026-10-09", {"opal_short_term": 841, "opal_intermediate": 2034})
    k12, o12 = _a4("global", "2026-10-12", {"opal_short_term": 899})
    staged = {STAGED_FMT % "global": {"period": "2026-08-17", "meta": {"account_count_by_model_key": {"opal_short_term": 1}}}}
    base_objs = {k08: o08, k09: o09, k12: o12}

    # H1 selection
    ok, detail = False, "no function"
    if fn is not None:
        try:
            a, f1, e1 = run(base_objs, "2026-10-09")
            b, f2, e2 = run(base_objs, "2026-10-10")
            c, f3, e3 = run(base_objs, "2026-10-12")
            d, f4, e4 = run(base_objs, "2026-12-31")
            ok = (a is not None and a.get("opal_short_term") == 841 and a.get("__as_of__") == "2026-10-09"
                  and b is not None and b.get("opal_short_term") == 841
                  and c is not None and c.get("opal_short_term") == 899 and c.get("__as_of__") == "2026-10-12"
                  and d is not None and d.get("__as_of__") == "2026-10-12")
            detail = "axis 10-09 -> %s; 10-10 -> %s; 10-12 -> %s; 12-31 -> %s %s" % (
                (a or {}).get("__as_of__"), (b or {}).get("__as_of__"), (c or {}).get("__as_of__"),
                (d or {}).get("__as_of__"), e1 or e2 or e3 or e4)
        except BaseException as exc:                          # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:140])
    arm("H1", ok, detail)

    # H2 fail closed, staged never requested
    ok, detail = False, "no function"
    if fn is not None:
        out, fake, err = run({k12: o12, **staged}, "2026-10-09")
        ok = out == {} and not any("gold/mdpf_revamp" in g for g in fake.gets) and not err
        detail = "no A4 <= axis -> %r; staged requested=%s %s" % (out, any("gold/mdpf_revamp" in g for g in fake.gets), err)
    arm("H2", ok, detail)

    # H3 no fallback even when only the staged object exists
    ok, detail = False, "no function"
    if fn is not None:
        out, fake, err = run(dict(staged), "2026-10-09")
        ok = out == {} and not any("gold/mdpf_revamp" in g for g in fake.gets) and not err
        detail = "only a staged object present -> %r; staged requested=%s %s" % (
            out, any("gold/mdpf_revamp" in g for g in fake.gets), err)
    arm("H3", ok, detail)

    # H4 a non-absence listing failure raises
    ok, detail = False, "no function"
    if fn is not None:
        out, fake, err = run(base_objs, "2026-10-09", list_error=True)
        ok = out is None and "FAIL-LOUD" in err
        detail = "listing AccessDenied -> %s" % (err or "returned %r" % (out,))
    arm("H4", ok, detail)

    # H5 period after the axis refused
    ok, detail = False, "no function"
    if fn is not None:
        kx, ox = _a4("global", "2026-10-09", {"opal_short_term": 5}, period="2026-10-12")
        out, fake, err = run({kx: ox}, "2026-10-09")
        ok = out == {} and not err
        detail = "key 10-09 with period 10-12 on axis 10-09 -> %r %s" % (out, err)
    arm("H5", ok, detail)

    # H6 sentinel and staleness
    ok, detail = False, "no function"
    if fn is not None and stale is not None:
        out, fake, err = run(base_objs, "2026-10-12")
        asof = (out or {}).get("__as_of__")
        verdict = stale(asof, "2026-10-12")["verdict"] if asof else None
        ok = asof == "2026-10-12" and verdict == "FRESH"
        detail = "as-of %s verdict %s %s" % (asof, verdict, err)
    arm("H6", ok, detail)

    # H7 the worker's own tests
    path = os.path.join(root, *TEST_FILE.split("/"))
    ok, detail = False, "%s absent" % TEST_FILE
    if os.path.isfile(path):
        try:
            import re
            p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider", path],
                               capture_output=True, text=True, timeout=100, cwd=root)
            tail = (p.stdout.strip().splitlines() or [""])[-1]
            m = re.search(r"(\d+) passed", tail)
            n = int(m.group(1)) if m else 0
            ok = p.returncode == 0 and n >= 5 and "failed" not in tail
            detail = "pytest rc=%d: %s" % (p.returncode, tail[:100])
        except subprocess.TimeoutExpired:
            detail = "pytest timed out at 100 s"
    arm("H7", ok, detail)

    k = sum(1 for a in arms if a)
    print("CN-H-1 READER: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) == 8 else 1


# ------------------------------------------------------------------ static arms
def _parse(root: str, rel: str):
    with open(os.path.join(root, *rel.split("/")), encoding="utf-8") as fh:
        src = fh.read()
    return ast.parse(src), src


def seams(root: str) -> int:
    arms = []

    def arm(name, ok, detail):
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        arms.append(bool(ok))

    tree, src = _parse(root, MODULE)
    fdef = next((n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
                 and n.name == "load_account_dist_frontier_counts"), None)

    # S1 every call passes the axis date
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and getattr(n.func, "id", getattr(n.func, "attr", "")) == "load_account_dist_frontier_counts"]
    ok = bool(calls) and all(len(c.args) >= 2 or any(k.arg == "axis_date" for k in c.keywords) for c in calls)
    arm("S1", ok, "%d call site(s); %d pass the axis date" % (
        len(calls), sum(1 for c in calls if len(c.args) >= 2 or any(k.arg == "axis_date" for k in c.keywords))))

    # S2 the loader body names no staged key
    body = ast.get_source_segment(src, fdef) if fdef is not None else ""
    ok = fdef is not None and "gold/mdpf_revamp" not in body and "account_distribution.json" not in body
    arm("S2", ok, "loader body %s a staged key literal" % ("names" if fdef is not None and not ok else "names no"
                                                         if fdef is not None else "ABSENT:"))

    # S3 the two stubs accept the second argument
    good, seen = 0, 0
    for rel in STUB_TESTS:
        try:
            ttree, _ = _parse(root, rel)
        except OSError:
            continue
        for n in ast.walk(ttree):
            tgt = None
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Lambda):
                for t in n.targets:
                    if getattr(t, "attr", getattr(t, "id", "")) == "load_account_dist_frontier_counts":
                        tgt = n.value
            elif isinstance(n, ast.keyword) and n.arg == "load_account_dist_frontier_counts" and isinstance(n.value, ast.Lambda):
                tgt = n.value
            if tgt is not None:
                seen += 1
                a = tgt.args
                if len(a.args) >= 2 or a.vararg is not None:
                    good += 1
    arm("S3", seen == 2 and good == 2, "%d stub(s) found, %d accept the second argument" % (seen, good))

    # S4 control: the stamp keeps its three keys
    keys = None
    for n in ast.walk(tree):
        if isinstance(n, ast.Dict):
            ks = [k.value for k in n.keys if isinstance(k, ast.Constant)]
            if "staleness" in ks and "source" in ks and "date" in ks:
                keys = sorted(ks)
    arm("S4", keys == ["date", "source", "staleness"], "meta.frontier_count keys %s" % keys)

    k = sum(1 for a in arms if a)
    print("CN-H-1 SEAMS: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) == 4 else 1


# ------------------------------------------------------------------ comparator (real objects, read-only)
def comparator(root: str) -> int:
    import boto3
    arms = []

    def arm(name, ok, detail):
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        arms.append(bool(ok))

    s3 = boto3.client("s3", region_name="us-east-1")

    class Rec:
        """Wraps the real client: read-only, records the keys requested."""

        def __init__(self, c):
            self._c = c
            self.gets = []
            self.exceptions = c.exceptions

        def get_object(self, **kw):
            self.gets.append(kw.get("Key"))
            return self._c.get_object(**kw)

        def get_paginator(self, n):
            return self._c.get_paginator(n)

    def J(key):
        return json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())

    def newest(prefix):
        ks = []
        for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
            ks += [o["Key"] for o in p.get("Contents", []) if o["Key"].endswith(".json")]
        return max(ks)

    served, staged = {}, {}
    for sc in SCOPES:
        served[sc] = J(newest(TS_FMT % sc))
        try:
            staged[sc] = J(STAGED_FMT % sc)
        except Exception:                                     # noqa: BLE001
            staged[sc] = None
    axis = served["global"].get("as_of_last")

    # K0 control: the freeze, measured
    frozen = []
    for sc in SCOPES:
        m = ((staged[sc] or {}).get("meta") or {}).get("account_count_by_model_key") or {}
        bm = served[sc].get("by_model") or {}
        for k, v in m.items():
            if k in bm and bm[k].get("account_count"):
                frozen.append(bm[k]["account_count"][-1] == v)
    arm("K0", bool(axis) and bool(frozen) and all(frozen),
        "served objects read, as_of_last %s; served frontier == staged roster on %d of %d mapped keys" % (
            axis, sum(1 for x in frozen if x), len(frozen)))

    try:
        mod = _load_module(root)
    except Exception as exc:                                  # noqa: BLE001
        print("  import FAIL: %s: %s" % (type(exc).__name__, str(exc)[:160]))
        for nm in ("K1", "K2", "K3", "K4"):
            arm(nm, False, "module import failed")
        print("CN-H-1 COMPARATOR: %d of %d arms" % (sum(arms), len(arms)))
        return 1
    rec = Rec(s3)
    mod._s3 = lambda: rec                                     # noqa: SLF001
    fn = mod.load_account_dist_frontier_counts

    out = {}
    err = ""
    try:
        for sc in SCOPES:
            out[sc] = fn(sc, axis)
    except BaseException as exc:                              # noqa: BLE001
        err = "%s: %s" % (type(exc).__name__, str(exc)[:140])

    # K1
    asofs = {sc: (out.get(sc) or {}).get("__as_of__") for sc in SCOPES}
    arm("K1", not err and all(a == axis for a in asofs.values()),
        "loader at axis %s -> as-of %s %s" % (axis, asofs, err))

    # K2 the delta table
    table, ok2 = [], not err
    for sc in SCOPES:
        m = {k: v for k, v in (out.get(sc) or {}).items() if not k.startswith("__")}
        bm = served[sc].get("by_model") or {}
        # the builder overrides only the keys it iterates: GLOBAL_MODEL_KEYS for global, the firm's own by_model for a firm
        allowed = set(getattr(mod, "GLOBAL_MODEL_KEYS", ())) if sc == "global" else set(bm)
        moved = 0
        s_tot = n_tot = 0
        for k, v in m.items():
            if k in allowed and k in bm and bm[k].get("account_count"):
                cur = bm[k]["account_count"][-1]
                if cur is None:
                    continue
                s_tot += cur
                n_tot += v
                if v != cur:
                    moved += 1
        tot_last = (served[sc].get("account_count_total") or [None])[-1]
        table.append((sc, len(m), moved, s_tot, n_tot, n_tot - s_tot, tot_last,
                      None if tot_last is None else tot_last + (n_tot - s_tot)))
        ok2 = ok2 and moved >= 1
    for t in table:
        print("      %-12s map_keys=%2d moved=%2d  served_sum=%6d  fresh_sum=%6d  delta=%+d  "
              "account_count_total[-1] %s -> %s" % t)
    arm("K2", ok2, "per-scope delta table printed; moved >= 1 in every scope: %s" % ok2)

    # K3 fail closed on real S3
    try:
        early = fn("global", "2000-01-01")
    except BaseException as exc:                              # noqa: BLE001
        early = "%s: %s" % (type(exc).__name__, str(exc)[:100])
    arm("K3", early == {}, "axis 2000-01-01 -> %r" % (early,))

    # K4 no staged request
    staged_gets = [g for g in rec.gets if g and "gold/mdpf_revamp" in g]
    arm("K4", not staged_gets and len(rec.gets) >= 1, "%d get(s), %d on a staged key" % (len(rec.gets), len(staged_gets)))

    k = sum(1 for a in arms if a)
    print("CN-H-1 COMPARATOR: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) == 5 else 1


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("reader", "seams", "comparator"):
        print(__doc__)
        return 2
    root = _root()
    return {"reader": reader, "seams": seams, "comparator": comparator}[sys.argv[1]](root)


if __name__ == "__main__":
    sys.exit(main())
