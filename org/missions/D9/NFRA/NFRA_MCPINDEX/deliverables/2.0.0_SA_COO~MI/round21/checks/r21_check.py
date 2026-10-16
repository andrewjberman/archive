"""r21_check.py -- the round 21 release candidate against the LIVE catalog (the host's blob b81c48aa3c at git ref LIVE_REF), from the repo root.

  python r21_check.py ac1   the difference control: candidate catalog C21_CATALOG (default infra/aws/ec2/opal-gateway/app/refs/DATA_CATALOG.yaml) against the live one
                            - every row of the three row sections (silver_datasets, portal_datasets, harvest_datasets) is byte-equal (no row moves, none added or removed);
                            - the tool index lists the same tools in the same order; for every entry, with `depth_kind` and `measured_at` removed from its history_depth claims the entry is
                              byte-equal to the live one;
                            - every `measured` history_depth claim (and every measured element of a per-link claim) of the candidate carries depth_kind latest or series_start (never floor) and measured_at == read_at, exactly the 6 series-start fields (total.series_start, as_of_first) are series_start,
                              and no other claim carries either key; the count of such claims is printed (39 at the live blob)
  python r21_check.py ac2   the consumers: the gateway tests that read the tool index and the catalog (tests/test_portal_index.py, test_opal_discover.py, test_discover_echo.py,
                            test_firm_catalog_visibility.py, and every tests/test_*tool_index*.py) pass with the candidate PLACED as the tree's catalog (it is restored afterwards)

Exit 0 PASS, 1 FAIL, 9 no run."""
import glob
import os
import shutil
import subprocess
import sys

import yaml

LIVE_REF = "bf9d23b518"
GW = "infra/aws/ec2/opal-gateway"
CAT = os.environ.get("C21_CATALOG") or GW + "/app/refs/DATA_CATALOG.yaml"
SECS = ("silver_datasets", "portal_datasets", "harvest_datasets")
KEYS = ("depth_kind", "measured_at")
SERIES_FIELDS = ("total.series_start", "as_of_first")
READ = ("read_at",)   # a fresh measure moves only the read stamps; every value must still equal the live one


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok  " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def live_doc():
    r = subprocess.run(["git", "show", "%s:%s/app/refs/DATA_CATALOG.yaml" % (LIVE_REF, GW)], capture_output=True)
    if r.returncode != 0:
        print("ERROR: git show %s catalog rc %d" % (LIVE_REF, r.returncode))
        sys.exit(9)
    return yaml.safe_load(r.stdout.decode("utf-8"))


def claims(h):
    if not isinstance(h, dict):
        return []
    return list(h.get("links") or []) if h.get("claim") == "per-link" else [h]


def strip(h):
    if not isinstance(h, dict):
        return h
    h = {k: v for k, v in h.items() if k not in KEYS + READ}
    if h.get("claim") == "per-link":
        h["links"] = [strip(x) for x in h.get("links") or []]
    return h


def ac1():
    lv, cd = live_doc(), yaml.safe_load(open(CAT, encoding="utf-8"))
    res = []
    for s in SECS:
        a, b = lv.get(s) or [], cd.get(s) or []
        res.append(("%s: %d rows, byte-equal to the live section" % (s, len(b)), a == b))
    lt, ct = lv.get("tool_index") or [], cd.get("tool_index") or []
    res.append(("the tool index lists the same %d tools in the same order" % len(lt), [e["tool"] for e in lt] == [e["tool"] for e in ct]))
    diff = []
    for a, b in zip(lt, ct):
        b2 = dict(b)
        if "history_depth" in b2:
            b2["history_depth"] = strip(b2["history_depth"])
        if "freshness" in b2:
            b2["freshness"] = strip(b2["freshness"])
        a = dict(a)
        for hk in ("history_depth", "freshness"):
            if hk in a:
                a[hk] = strip(a[hk])
        if a != b2:
            diff.append(a["tool"])
    res.append(("with the two keys and the read stamps removed every tool_index entry equals the live one (%d differ: %s)" % (len(diff), ",".join(diff[:3])), not diff))
    n = bad = other = nser = 0
    for e in ct:
        for c in claims(e.get("history_depth")):
            if c.get("claim") == "measured":
                n += 1
                want = "series_start" if c.get("field") in SERIES_FIELDS else "latest"
                nser += 1 if c.get("depth_kind") == "series_start" else 0
                bad += 0 if (c.get("depth_kind") == want and c.get("measured_at") and c.get("measured_at") == c.get("read_at")) else 1
            elif any(k in c for k in KEYS):
                other += 1
        for c in claims(e.get("freshness")):
            if any(k in c for k in KEYS):
                other += 1
    print("DENOMINATOR measured history_depth claims %d; with a wrong or missing kind or measured_at %d; series_start claims %d; other claims carrying the keys %d" % (n, bad, nser, other))
    res.append(("every measured history_depth claim carries the kind its field implies (latest, or series_start on the 6 series-start fields) and measured_at == read_at; no other claim does", n > 0 and not bad and not other and nser == 6))
    return report(res)


def ac2():
    tests = ["tests/test_portal_index.py", "tests/test_opal_discover.py", "tests/test_discover_echo.py", "tests/test_firm_catalog_visibility.py"] \
        + sorted(os.path.relpath(p, GW).replace(os.sep, "/") for p in glob.glob(os.path.join(GW, "tests", "test_*tool_index*.py")))
    tests = [t for t in tests if os.path.exists(os.path.join(GW, t))]
    tracked = os.path.join(GW, "app", "refs", "DATA_CATALOG.yaml")
    backup = tracked + ".c21bak"
    placed = os.path.abspath(CAT) != os.path.abspath(tracked)
    if placed:
        shutil.copyfile(tracked, backup)
        shutil.copyfile(CAT, tracked)
    try:
        env = dict(os.environ, PYTHONPATH=os.path.abspath(GW))
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header"] + tests, cwd=GW, env=env, capture_output=True, text=True, timeout=280)
    finally:
        if placed:
            shutil.copyfile(backup, tracked)
            os.remove(backup)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("DENOMINATOR test files %d; pytest rc=%d: %s" % (len(tests), r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    return report([("the gateway tests that read the catalog pass with the candidate placed", r.returncode == 0)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
