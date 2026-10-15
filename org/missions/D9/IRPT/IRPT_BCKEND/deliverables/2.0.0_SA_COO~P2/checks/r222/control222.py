"""Positive control and negatives for p222_cells.py (run by the issuer at the cut). Usage: python control222.py <real_repo_root>"""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r222/p222_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent.parent / "r218"))
import p222_cells as P  # noqa: E402

PY = "# BEGIN ABSENT-AT-SOURCE-A\na = 1\n# END ABSENT-AT-SOURCE-A\n# BEGIN ABSENT-AT-SOURCE-B\nb = 2\n# END ABSENT-AT-SOURCE-B\n# BEGIN ABSENT-AT-SOURCE-C\nc = 3\n# END ABSENT-AT-SOURCE-C\n"
OTHER = "x = 1\n"
OTHER_PATH = "data/assets/scripts/gold/investor_reporting/holdings_publication.py"


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(mut=None, hs_text=PY):
    root = Path(tempfile.mkdtemp(prefix="c222_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel, txt in ((P.HS, hs_text), (OTHER_PATH, OTHER)):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(txt, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "members")
    pin = git(root, "rev-parse", "HEAD")
    firm = {"live_bundle_sha256": "a" * 64, "candidate_bundle_sha256": "b" * 64, "members_total": 30,
            "changed_members": [{"repo_path": P.HS, "sha256_at_pin": hashlib.sha256(hs_text.encode()).hexdigest()}], "extra_changed_reasons": {}}
    rec = {"base_commit": pin, "read_date": "2026-10-15", "claim": "measured", "pin": pin, "holdings_snapshot_blob": git(root, "rev-parse", "%s:%s" % (pin, P.HS)),
           "method": "Built each firm's bundle from the pin with the bundle builder BUILD ONLY and compared it member by member with the live bundle downloaded read-only; nothing uploaded.",
           "firms": {f: copy.deepcopy(firm) for f in P.FIRMS},
           "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
           "notes": ["the candidate bundles sit in scratch outside the repository and were not uploaded", "the live bundles were downloaded read-only and hashed",
                     "the pin is the merged commit that carries IB-pr-576, 577 and 582"]}
    if mut:
        mut(rec, root, pin)
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
    print("%s %-12s %-24s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


def extra_member(rec, root, pin):
    rec["firms"]["cottonwood"]["changed_members"].append({"repo_path": OTHER_PATH, "sha256_at_pin": hashlib.sha256(OTHER.encode()).hexdigest()})


NEGS = [
    ("two_firms", "AC1", lambda r, *a: r["firms"].pop("inflection")),
    ("bad_blob", "AC1", lambda r, *a: r.update(holdings_snapshot_blob="0" * 40)),
    ("same_bundle", "AC2", lambda r, *a: r["firms"]["inflection"].update(candidate_bundle_sha256="a" * 64)),
    ("wrong_member_sha", "AC2", lambda r, *a: r["firms"]["49financial"]["changed_members"][0].update(sha256_at_pin="0" * 64)),
    ("no_holdings_member", "AC2", lambda r, *a: r["firms"]["cottonwood"].update(changed_members=[{"repo_path": OTHER_PATH, "sha256_at_pin": hashlib.sha256(OTHER.encode()).hexdigest()}])),
    ("extra_unexplained", "AC2", extra_member),
    ("counter_nonzero", "AC3", lambda r, *a: r.update(aws_writes_made=1)),
]
root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB222-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn)
    expect(label, "IB222-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(hs_text="x = 1\n")
expect("pin_lacks_blocks", "IB222-1-AC1", root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
