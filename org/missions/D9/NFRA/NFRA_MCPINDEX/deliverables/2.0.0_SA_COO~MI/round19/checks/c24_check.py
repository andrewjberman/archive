"""c24_check.py -- grades MX-c-24 (the opal_discover answer echoes `bucket` on every catalog row that has one, and `vendor` and `firm` on every row that has them), from the repo root.

  python c24_check.py ac1   the echo: every silver row answered to opal-internal carries `bucket` equal to the row's, and `vendor` / `firm` where the row has them;
                            and the deployed opal_discover (discover_buckets.py, in-process on this tree) shows the bucket echoed on every bucket and the vendor and firm
                            on the matches of opal-data-assets and opal-data-bd
  python c24_check.py ac2   the difference control: the BASE tree (git ref BASE_REF) against the NEW tree, every silver row x {opal-internal, two known firms, an unknown firm}:
                            the same rows are visible to the same principals (no newly visible, no hidden), every key the base answer had is byte-equal in the new answer,
                            and the only keys added are `bucket`, `vendor`, `firm`
  python c24_check.py ac3   gateway tests: tests/test_discover_echo.py (new, at least 6 tests) with tests/test_opal_discover.py and tests/test_firm_catalog_visibility.py pass

The NEW tree is infra/aws/ec2/opal-gateway of the worktree, or C24_GW (a planted tree). Exit 0 PASS, 1 FAIL, 9 no run.
"""
import json
import os
import subprocess
import sys
import tempfile

import yaml

BASE_REF = "38fe44d5cb"
GW = "infra/aws/ec2/opal-gateway"
NEWGW = os.environ.get("C24_GW") or GW
HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.join("org", "missions", "D9", "NFRA", "NFRA_MCPINDEX", "deliverables", "2.0.0_SA_COO~MI", "round18", "discover_buckets.py")
ADDED = {"bucket", "vendor", "firm"}


def answers(root):
    r = subprocess.run([sys.executable, os.path.join(HERE, "c24_answers.py"), root], capture_output=True, text=True, timeout=200)
    line = (r.stdout or "").strip().splitlines()[-1:] or [""]
    try:
        return json.loads(line[0])
    except ValueError:
        print("ERROR: c24_answers under %s rc %d: %s" % (root, r.returncode, (r.stderr or r.stdout)[-300:]))
        sys.exit(9)


def base_tree():
    d = tempfile.mkdtemp(prefix="c24_base_")
    p = subprocess.run("git archive %s %s | tar -x -C %s" % (BASE_REF, GW, d.replace("\\", "/")), shell=True, capture_output=True)
    if p.returncode != 0:
        print("ERROR: git archive %s failed: %s" % (BASE_REF, p.stderr[-200:]))
        sys.exit(9)
    return os.path.join(d, GW)


def report(res):
    for name, ok in res:
        print("CHECK %s: %s" % ("ok " if ok else "FAIL", name))
    ok = bool(res) and all(o for _n, o in res)
    print("RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def ac1():
    cat = yaml.safe_load(open(os.path.join(NEWGW, "app", "refs", "DATA_CATALOG.yaml"), encoding="utf-8"))
    rows = {r["entity"]: r for r in (cat.get("silver_datasets") or []) if isinstance(r, dict) and r.get("entity")}
    new = answers(NEWGW)
    res = []
    for field in ("bucket", "vendor", "firm"):
        want = [e for e, r in rows.items() if r.get(field)]
        bad = [e for e in want if ((new["answers"].get("opal-internal|" + e) or {}).get(field)) != rows[e][field]]
        print("DENOMINATOR rows carrying %s %d of %d silver rows; answers not echoing it %d" % (field, len(want), len(rows), len(bad)))
        res.append(("every silver row with a %s echoes it in the answer (%d of %d)" % (field, len(want) - len(bad), len(want)), bool(want) and not bad))
    res.append(("no crash in the run", not new["errors"]))
    p = subprocess.run([sys.executable, PROBE, NEWGW], capture_output=True, text=True, timeout=250)
    out = (p.stdout or "").replace("\r", "")
    lines = [ln for ln in out.splitlines() if ln.startswith("BUCKET")]
    echoed = sum(1 for ln in lines if "bucket_echo=True" in ln)
    vf = [ln for ln in lines if ("opal-data-assets" in ln.split()[1] or "opal-data-bd" in ln.split()[1])]
    vf_ok = sum(1 for ln in vf if "vendor_firm_echo=True" in ln)
    print("DENOMINATOR buckets probed %d; bucket echoed %d; assets+bd buckets %d, vendor and firm echoed %d" % (len(lines), echoed, len(vf), vf_ok))
    res.append(("the discover probe serves and echoes the bucket on every bucket (%d of %d)" % (echoed, len(lines)), bool(lines) and echoed == len(lines) and p.returncode == 0))
    res.append(("the probe shows vendor and firm on the assets and bd matches (%d of %d)" % (vf_ok, len(vf)), len(vf) == 2 and vf_ok == 2))
    return report(res)


def ac2():
    b, n = answers(base_tree()), answers(NEWGW)
    pairs = len(n["answers"])
    res = [("the row sets and principals are equal (%d answers)" % pairs, set(b["answers"]) == set(n["answers"]) and b["_principals"] == n["_principals"])]
    vis_changed = [k for k in n["answers"] if (n["answers"][k] is None) != (b["answers"].get(k) is None)]
    newly = [k for k in vis_changed if n["answers"][k] is not None]
    res.append(("no row becomes visible or hidden to any principal (changed %d, newly visible %d)" % (len(vis_changed), len(newly)), not vis_changed))
    changed_keys, altered, added_other = 0, [], []
    for k, na in n["answers"].items():
        ba = b["answers"].get(k)
        if na is None or ba is None:
            continue
        for key in ba:
            if na.get(key) != ba[key]:
                altered.append((k, key))
        extra = set(na) - set(ba)
        if extra - ADDED:
            added_other.append((k, sorted(extra - ADDED)))
        if extra:
            changed_keys += 1
    res.append(("every key of every base answer is byte-equal in the new one (altered %d)" % len(altered), not altered))
    res.append(("the only keys added are bucket, vendor, firm (other additions %d)" % len(added_other), not added_other))
    res.append(("some answers gained a key (%d)" % changed_keys, changed_keys > 0))
    res.append(("no error in either run", not n["errors"] and not b["errors"]))
    print("DENOMINATOR answers %d (rows %d x principals %d); newly visible %d; altered base keys %d; answers gaining a key %d"
          % (pairs, n["_rows"], len(n["_principals"]), len(newly), len(altered), changed_keys))
    return report(res)


def ac3():
    root = NEWGW
    f = os.path.join(root, "tests", "test_discover_echo.py")
    if not os.path.exists(f):
        print("ERROR: %s absent" % f)
        return report([("the new test file exists", False)])
    env = dict(os.environ, PYTHONPATH=os.path.abspath(root))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--no-header", "tests/test_discover_echo.py",
                        "tests/test_opal_discover.py", "tests/test_firm_catalog_visibility.py"], cwd=root, env=env, capture_output=True, text=True, timeout=280)
    tail = [ln for ln in (r.stdout or "").replace("\x1b", "").splitlines() if "passed" in ln or "failed" in ln][-1:]
    print("pytest rc=%d: %s" % (r.returncode, tail[0].strip() if tail else (r.stdout or r.stderr)[-200:]))
    new_n = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--co", "tests/test_discover_echo.py"], cwd=root, env=env,
                           capture_output=True, text=True, timeout=120)
    n_new = sum(1 for ln in (new_n.stdout or "").splitlines() if "::" in ln)
    print("new tests collected: %d" % n_new)
    return report([("the three test files pass", r.returncode == 0), ("the new file holds at least 6 tests", n_new >= 6)])


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("ac1", "ac2", "ac3"):
        print(__doc__)
        return 9
    return {"ac1": ac1, "ac2": ac2, "ac3": ac3}[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
