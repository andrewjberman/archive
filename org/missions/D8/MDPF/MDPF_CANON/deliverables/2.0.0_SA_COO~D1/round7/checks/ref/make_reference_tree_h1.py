#!/usr/bin/env python3
"""Build a REFERENCE TREE for the CN-h-1 issuer checks (the dry-run that proves the arms CAN pass).

  python make_reference_tree_h1.py <dest-dir>

Copies, read-only from the repo at the current checkout (CN-f-1 already merged there), data/mdpf/scripts, lib/ and the naming
registry into <dest-dir>, applies the cell's change as the ISSUER'S REFERENCE (never a worker's code, never committed to the
repo), and drops a small test file. Then:   R6_ROOT=<dest-dir> python r6_cn_h_1.py reader|seams|comparator

Every patch asserts it applied exactly once; a drift in a target file fails loud instead of silently skipping.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

NEW_SELECT = '''    s3 = _s3()
    if not axis_date:
        log(f"  WARN frontier-count: no axis date for {firm_id} -> frontier honest-None (never the staged object)")
        return {}
    # CN-h-1 (S5 disarm, CTO ADDENDUM 5): the newest A4 distribution AT OR BEFORE the axis date; never the staged runner object.
    prefix = f"portal/gold/mdpf/{firm_id}/account-distribution/"
    best = None
    try:
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=ASSETS_BUCKET, Prefix=prefix):
            for o in page.get("Contents", []):
                nm = o["Key"].rsplit("/", 1)[-1]
                if nm.endswith(".json") and len(nm) == 15 and nm[:-5] <= axis_date:
                    if best is None or nm[:-5] > best[0]:
                        best = (nm[:-5], o["Key"])
    except Exception as e:   # noqa: BLE001 -- deliberate breadth BECAUSE it re-raises
        raise RuntimeError(
            f"C2-SIBLING FAIL-LOUD: frontier-count A4 listing FAILED (NOT absent) for "
            f"s3://{ASSETS_BUCKET}/{prefix} ({type(e).__name__}: {e})") from e
    if best is None:
        log(f"  WARN frontier-count: no A4 account-distribution at or before {axis_date} for {firm_id} "
            "-> frontier honest-None (never the staged object)")
        return {}
    key = best[1]
'''

NEW_TAIL = '''    out = dict((obj.get("meta") or {}).get("account_count_by_model_key") or {})
    period = obj.get("period")
    if period and period > axis_date:
        log(f"  WARN frontier-count: A4 {key} period {period} is AFTER the axis {axis_date} -> refused (honest-None)")
        return {}
    if out:
        out["__as_of__"] = period
    return out
'''

REF_TEST = '''"""CN-h-1 REFERENCE test (issuer dry-run only; the worker writes its own)."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
for sub in ("scripts/silver", "scripts/gold"):
    sys.path.insert(0, os.path.join(ROOT, "data", "mdpf", sub))
sys.path.insert(0, ROOT)
import dim_mdpf_aggregate_aua_timeseries as m  # noqa: E402


class _B:
    def __init__(self, b):
        self.b = b

    def read(self):
        return self.b


class _NSK(Exception):
    pass


class Fake:
    class exceptions:
        NoSuchKey = _NSK

    def __init__(self, objs, boom=False):
        self.objs, self.boom, self.gets = objs, boom, []

    def get_object(self, Bucket, Key):
        self.gets.append(Key)
        if Key not in self.objs:
            raise _NSK(Key)
        return {"Body": _B(json.dumps(self.objs[Key]).encode())}

    def get_paginator(self, n):
        o = self

        class P:
            def paginate(self, Bucket, Prefix):
                if o.boom:
                    raise PermissionError("AccessDenied")
                yield {"Contents": [{"Key": k} for k in sorted(o.objs) if k.startswith(Prefix)]}
        return P()


def _o(d, mp, period=None):
    return ("portal/gold/mdpf/global/account-distribution/%s.json" % d,
            {"period": period or d, "meta": {"account_count_by_model_key": mp}})


def _run(objs, axis, boom=False):
    f = Fake(objs, boom)
    m._s3 = lambda: f
    return m.load_account_dist_frontier_counts("global", axis), f


def test_selects_newest_at_or_before():
    k1, o1 = _o("2026-10-09", {"a": 1})
    k2, o2 = _o("2026-10-12", {"a": 2})
    out, _ = _run({k1: o1, k2: o2}, "2026-10-10")
    assert out["a"] == 1 and out["__as_of__"] == "2026-10-09"


def test_none_at_or_before_is_absent_and_staged_untouched():
    k2, o2 = _o("2026-10-12", {"a": 2})
    out, f = _run({k2: o2, "gold/mdpf_revamp/global/account_distribution.json": {"period": "x"}}, "2026-10-09")
    assert out == {} and not any("gold/mdpf_revamp" in g for g in f.gets)


def test_listing_failure_raises():
    try:
        _run({}, "2026-10-09", boom=True)
    except RuntimeError as e:
        assert "FAIL-LOUD" in str(e)
    else:
        raise AssertionError("did not raise")


def test_period_after_axis_refused():
    k, o = _o("2026-10-09", {"a": 1}, period="2026-10-12")
    out, _ = _run({k: o}, "2026-10-09")
    assert out == {}


def test_asof_is_period():
    k, o = _o("2026-10-12", {"a": 7})
    out, _ = _run({k: o}, "2026-10-12")
    assert out["__as_of__"] == "2026-10-12" and out["a"] == 7
'''


def _sub(path: str, old: str, new: str) -> None:
    with open(path, encoding="utf-8", newline="") as fh:
        s = fh.read()
    nl = "\r\n" if "\r\n" in s else "\n"
    if nl == "\r\n":
        old = old.replace("\n", "\r\n")
        new = new.replace("\n", "\r\n")
    if s.count(old) != 1:
        raise SystemExit("PATCH DRIFT: %r occurs %d times in %s" % (old[:60], s.count(old), path))
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(s.replace(old, new))


def main() -> int:
    dest = os.path.abspath(sys.argv[1])
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    if os.path.exists(dest):
        raise SystemExit("dest exists: " + dest)
    ign = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(os.path.join(root, "data", "mdpf", "scripts"), os.path.join(dest, "data", "mdpf", "scripts"), ignore=ign)
    shutil.copytree(os.path.join(root, "lib"), os.path.join(dest, "lib"), ignore=ign)
    shutil.copytree(os.path.join(root, "infra", "logic", "registry"),
                    os.path.join(dest, "infra", "logic", "registry"), ignore=ign)
    os.makedirs(os.path.join(dest, "org", "standards"), exist_ok=True)
    shutil.copy2(os.path.join(root, "org", "standards", "NAMING_SCHEMA.json"),
                 os.path.join(dest, "org", "standards", "NAMING_SCHEMA.json"))
    g = os.path.join(dest, "data", "mdpf", "scripts", "gold")
    mod = os.path.join(g, "dim_mdpf_aggregate_aua_timeseries.py")
    _sub(mod, "def load_account_dist_frontier_counts(firm_id: str) -> dict:",
         'def load_account_dist_frontier_counts(firm_id: str, axis_date: "str | None" = None) -> dict:')
    _sub(mod, '    s3 = _s3()\n    key = f"gold/mdpf_revamp/{firm_id}/account_distribution.json"\n', NEW_SELECT)
    _sub(mod, '    out = dict((obj.get("meta") or {}).get("account_count_by_model_key") or {})\n'
              '    if out:\n        out["__as_of__"] = obj.get("period")\n    return out\n', NEW_TAIL)
    _sub(mod, "    ad_frontier = load_account_dist_frontier_counts(firm_id)  # CTO (a) coherence",
         "    ad_frontier = load_account_dist_frontier_counts(firm_id, dates[-1] if dates else None)  # CTO (a) coherence")
    _sub(mod, '    ad_frontier = load_account_dist_frontier_counts("global")   # CTO (a) frontier coherence',
         '    ad_frontier = load_account_dist_frontier_counts("global", dates[-1] if dates else None)   # CTO (a) frontier coherence')
    for rel in ("tests/test_canplat_p1_1.py", "tests/test_global_fold_flag2.py"):
        p = os.path.join(g, *rel.split("/"))
        with open(p, encoding="utf-8", newline="") as fh:
            s = fh.read()
        if s.count("lambda firm: {}") != 1:
            raise SystemExit("PATCH DRIFT in " + rel)
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(s.replace("lambda firm: {}", "lambda firm, axis_date=None: {}"))
    td = os.path.join(dest, "data", "mdpf", "tests", "canon")
    os.makedirs(td, exist_ok=True)
    with open(os.path.join(td, "test_frontier_counts_a4.py"), "w", encoding="utf-8") as fh:
        fh.write(REF_TEST)
    print("reference tree at", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
