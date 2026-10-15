"""Positive control and negatives for p221_cells.py (run by the issuer at the cut). Usage: python control221.py <real_repo_root>
Builds temp git roots holding the two members at a commit, a synthetic record, runs every criterion expecting PASS, then each mutation expecting FAIL."""
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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r221/p221_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent.parent / "r218"))
import p221_cells as P  # noqa: E402

PY = "# BEGIN SPLIT-ADJUST-A\nx = 1\n# END SPLIT-ADJUST-A\n# BEGIN SPLIT-ADJUST-B\ny = 2\n# END SPLIT-ADJUST-B\n"
JS = '{"split_adjust": {}}\n'


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(mut=None, files=None):
    root = Path(tempfile.mkdtemp(prefix="c221_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel, txt in (files or {P.MEMBERS["holdings_performance.py"]: PY, P.MEMBERS["sources.json"]: JS}).items():
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(txt, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "members")
    pin = git(root, "rev-parse", "HEAD")
    rec = {"base_commit": pin, "read_date": "2026-10-15", "claim": "measured", "method": "Built the candidate with BUILD_ONLY and a candidate source map that re-pins the two members of this function only, then compared the zip members with the live zip's, nothing uploaded.",
           "function": P.FN, "live_codesha256": P.LIVE_DIGEST, "override_map_used": True,
           "candidate": {"codesha256": "A" * 43 + "=", "moved_count": 2, "total_members": 40, "moved_members": ["holdings_performance.py", "sources.json"]},
           "members": {"holdings_performance.py": {"repo_path": P.MEMBERS["holdings_performance.py"], "pin": pin, "sha256_now": hashlib.sha256(PY.encode()).hexdigest(), "split_blocks_a": 1, "split_blocks_b": 1},
                       "sources.json": {"repo_path": P.MEMBERS["sources.json"], "pin": pin, "sha256_now": hashlib.sha256(JS.encode()).hexdigest(), "split_adjust_declared": True}},
           "siblings_unmoved": list(P.SIBLINGS), "extra_moved_reasons": {},
           "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
           "notes": ["the candidate zip sits in scratch outside the repository and was not uploaded", "the live zip was downloaded by get-function and its sha256 equals the live CodeSha256", "sibling functions were not built"]}
    if mut:
        rec = copy.deepcopy(rec)
        mut(rec)
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


NEGS = [
    ("stale_live", "AC1", lambda r: r.update(live_codesha256="B" * 43 + "=")),
    ("candidate_equals_live", "AC1", lambda r: r["candidate"].update(codesha256=P.LIVE_DIGEST)),
    ("no_override_map", "AC1", lambda r: r.update(override_map_used=False)),
    ("member_not_moved", "AC1", lambda r: r["candidate"].update(moved_members=["sources.json", "other.py"])),
    ("wrong_sha", "AC2", lambda r: r["members"]["sources.json"].update(sha256_now="0" * 64)),
    ("wrong_block_count", "AC2", lambda r: r["members"]["holdings_performance.py"].update(split_blocks_a=3)),
    ("sibling_released", "AC2", lambda r: r.update(siblings_unmoved=[P.SIBLINGS[0]])),
    ("extra_unexplained", "AC2", lambda r: r["candidate"].update(moved_count=3, moved_members=["holdings_performance.py", "sources.json", "lib/x.py"])),
    ("counter_nonzero", "AC3", lambda r: r.update(aws_writes_made=1)),
]
root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB221-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn)
    expect(label, "IB221-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(files={P.MEMBERS["holdings_performance.py"]: "x = 1\n", P.MEMBERS["sources.json"]: JS})
expect("no_split_blocks_at_pin", "IB221-1-AC2", root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
