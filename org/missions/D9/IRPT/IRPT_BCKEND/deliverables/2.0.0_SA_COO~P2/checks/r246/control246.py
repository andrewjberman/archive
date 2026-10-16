"""Positive control and negatives for p246_cells.py (run by the issuer at the cut). Usage: python control246.py <real_repo_root>"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r246/p246_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
import p246_cells as P  # noqa: E402

GOOD = {
    "gates": {"ledger_open_l6_only": True, "function_code_sha256": P.DIGEST, "xa_f98b_state": "RULED", "helper_blob": P.HELPER_BLOB, "cto_ruling_msg": 9653},
    "user": {"role": "user", "userType": "test-filer", "firmId": "opal-capital", "entitlement_rows": 0, "removed_read_back_absent": True, "password_in_memory_only": True},
    "old_receipt": {"readable": True, "status": "complete"},
    "new_export": {"posts": 1, "http_class": "2xx", "status": "complete", "readable": True, "emails_sent": 0},
    "counters": {"exports_requested": 1, "users_minted": 1, "users_removed": 1, "lambda_code_changes": 0, "iam_changes": 0, "schedule_changes": 0, "files_deleted": 0, "markers_closed": 0},
}


def mut(path, value):
    def f(r):
        r = copy.deepcopy(r)
        cur = r
        for k in path[:-1]:
            cur = cur[k]
        cur[path[-1]] = value
        return r
    return f


NEGS = [
    ("wrong_digest", "AC1", mut(["gates", "function_code_sha256"], "o9UugRAV")),
    ("ledger_not_l6_only", "AC1", mut(["gates", "ledger_open_l6_only"], False)),
    ("xa_not_ruled", "AC1", mut(["gates", "xa_f98b_state"], "PENDING")),
    ("helper_differs", "AC1", mut(["gates", "helper_blob"], "0" * 40)),
    ("ruling_not_cited", "AC1", mut(["gates", "cto_ruling_msg"], 0)),
    ("role_is_admin", "AC2", mut(["user", "role"], "admin")),
    ("firm_not_opal", "AC2", mut(["user", "firmId"], "some-firm")),
    ("entitlement_row", "AC2", mut(["user", "entitlement_rows"], 1)),
    ("user_not_absent", "AC2", mut(["user", "removed_read_back_absent"], False)),
    ("password_written", "AC2", mut(["user", "password_in_memory_only"], False)),
    ("old_receipt_refused", "AC3", mut(["old_receipt", "readable"], False)),
    ("two_exports", "AC3", mut(["new_export", "posts"], 2)),
    ("export_not_2xx", "AC3", mut(["new_export", "http_class"], "5xx")),
    ("export_unreadable", "AC3", mut(["new_export", "readable"], False)),
    ("email_sent", "AC3", mut(["new_export", "emails_sent"], 1)),
    ("code_changed", "AC3", mut(["counters", "lambda_code_changes"], 1)),
    ("iam_changed", "AC3", mut(["counters", "iam_changes"], 1)),
    ("file_deleted", "AC3", mut(["counters", "files_deleted"], 1)),
    ("ledger_closed_by_applier", "AC3", mut(["counters", "markers_closed"], 1)),
]


def build(rec):
    root = Path(tempfile.mkdtemp(prefix="c246_"))
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    f = root / P.REC
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(rec), encoding="utf-8")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-26s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root = build(GOOD)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB246-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn(GOOD))
    expect(label, "IB246-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = Path(tempfile.mkdtemp(prefix="c246_"))
for ac in ("AC1", "AC2", "AC3"):
    expect("no_record", "IB246-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
