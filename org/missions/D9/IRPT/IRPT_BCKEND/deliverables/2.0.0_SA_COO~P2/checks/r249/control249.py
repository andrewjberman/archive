"""Positive control and negatives for p249_cells.py (run by the issuer at the cut). Usage: python control249.py <real_repo_root>

Synthetic git repos: a base commit, then ONE worker commit; a stub lib/opal_naming.py so each arm can be made to fail.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r249/p249_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p249_cells as P  # noqa: E402

STUB = '''def address(source, scope, tier, table, partition, object=None):
    if source == "refuse":
        raise ValueError("REFUSED: missing row")
    return "s3://opal-data-assets/globgrph/%s/%s/%s/%s" % (scope, tier, table, partition)


def name(system, scope, function, kind, qualifier=None, fifo=False):
    return "%s-%s-%s-%s" % (system, scope, function, kind)


def key(source, scope, tier, table, partition):
    return "%s/%s/%s/%s" % (scope, tier, table, partition)
'''


def calls_good():
    out = []
    for f in ("alpha", "bravo", "charlie"):
        out.append({"label": "key " + f, "fn": "address", "args": ["globgrph", "acctlist", "product", "hmac", f], "kwargs": {},
                    "result": "s3://opal-data-assets/globgrph/acctlist/product/hmac/%s" % f})
    out.append({"label": "role", "fn": "name", "args": ["irpt", "acct", "hmac-list-stage", "role"], "kwargs": {}, "result": "irpt-acct-hmac-list-stage-role"})
    out.append({"label": "policy", "fn": "name", "args": ["irpt", "acct", "hmac-list-stage", "policy"], "kwargs": {}, "result": "irpt-acct-hmac-list-stage-policy"})
    return out


GOOD = {"calls": calls_good(), "secret": {"name": "irpt/acct/hmac-key", "registry_file": P.RES}, "rows_added": ["resources.json: irpt/acct/hmac-key"],
        "firms": ["alpha", "bravo", "charlie"], "notes": "n"}
RESOURCES_GOOD = [{"name": "irpt/acct/hmac-key", "type": "SECRET", "system": "irpt", "evidence": "CTO msg 10161"}]


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(rec=None, resources=None, stub=STUB, extra=None, tests_ok=True, with_registry=True):
    rec = GOOD if rec is None else rec
    resources = RESOURCES_GOOD if resources is None else resources
    root = Path(tempfile.mkdtemp(prefix="c249_"))
    (root / "lib").mkdir()
    (root / "lib" / "opal_naming.py").write_text(stub, encoding="utf-8")
    (root / "lib" / "tests").mkdir(parents=True, exist_ok=True)
    for old in (root / "lib" / "tests").glob("*"):
        if old.is_file():
            old.unlink()
    (root / "lib" / "tests" / "test_opal_naming_stub.py").write_text("def test_naming():\n    assert %s\n" % ("True" if tests_ok else "False"), encoding="utf-8")
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "base")
    if with_registry:
        f = root / P.RES
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(resources), encoding="utf-8")
    d = root / P.REC
    d.parent.mkdir(parents=True, exist_ok=True)
    d.write_text(json.dumps(rec), encoding="utf-8")
    for e in extra or []:
        (root / e).parent.mkdir(parents=True, exist_ok=True)
        (root / e).write_text("x\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "worker")
    return root


def mut(path, value):
    def f(r):
        r = copy.deepcopy(r)
        cur = r
        for k in path[:-1]:
            cur = cur[k]
        cur[path[-1]] = value
        return r
    return f


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=300, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-30s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IBHM3A-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)

CASES = [
    ("result_differs_from_rerun", "AC1", dict(rec=mut(["calls", 0, "result"], "s3://opal-data-assets/globgrph/other")(GOOD))),
    ("a_call_refuses", "AC1", dict(rec=mut(["calls", 1, "args"], ["refuse", "acctlist", "product", "hmac", "bravo"])(GOOD))),
    ("address_outside_the_bucket", "AC1", dict(stub=STUB.replace("s3://opal-data-assets/globgrph/", "s3://other-bucket/"))),
    ("only_four_calls", "AC1", dict(rec=mut(["calls"], calls_good()[:4])(GOOD))),
    ("two_firms_one_address", "AC1", dict(rec=mut(["firms"], ["alpha", "alpha", "charlie"])(GOOD))),
    ("firm_not_in_an_address", "AC1", dict(rec=mut(["firms"], ["alpha", "bravo", "delta"])(GOOD))),
    ("other_file_touched", "AC2", dict(extra=["lib/opal_naming_other.py"])),
    ("naming_tests_fail", "AC2", dict(tests_ok=False)),
    ("no_registry_file_in_commit", "AC2", dict(with_registry=False)),
    ("secret_row_wrong_type", "AC3", dict(resources=[{"name": "irpt/acct/hmac-key", "type": "IAM_ROLE", "system": "irpt"}])),
    ("secret_row_wrong_system", "AC3", dict(resources=[{"name": "irpt/acct/hmac-key", "type": "SECRET", "system": "portal"}])),
    ("secret_name_not_slash", "AC3", dict(rec=mut(["secret", "name"], "irpt-acct-hmac-key")(GOOD))),
    ("role_name_not_irpt", "AC3", dict(rec=mut(["calls", 3, "result"], "portal-acct-hmac-list-stage-role")(GOOD), stub=STUB.replace('return "%s-%s-%s-%s" % (system, scope, function, kind)', 'return "portal-%s-%s-%s" % (scope, function, kind)'))),
    ("key_material_in_record", "AC3", dict(rec=mut(["notes"], "A" * 50)(GOOD))),
]
for label, ac, kw in CASES:
    root = build(**kw)
    expect(label, "IBHM3A-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c249_"))
git(root, "init", "-q")
for ac in ("AC1", "AC2", "AC3"):
    expect("empty_repo", "IBHM3A-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
