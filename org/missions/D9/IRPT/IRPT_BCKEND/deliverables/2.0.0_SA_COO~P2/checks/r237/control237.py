"""Positive control and negatives for p237_cells.py (run by the issuer at the cut). Usage: python control237.py <real_repo_root>"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r237/p237_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent.parent / "r218"))
import p237_cells as P  # noqa: E402

BASE_HS = "a = 1\n# BEGIN ABSENT-AT-SOURCE-A\nb = 2\n# END ABSENT-AT-SOURCE-A\nc = 3\n"
SPANS = ["# BEGIN ABSENT-AT-SOURCE-D\nx = 1\n# END ABSENT-AT-SOURCE-D\n", "    # BEGIN ABSENT-AT-SOURCE-D\n    y = 2\n    # END ABSENT-AT-SOURCE-D\n"]
CAND_HS = "a = 1\n" + SPANS[0] + "# BEGIN ABSENT-AT-SOURCE-A\nb = 2\n" + SPANS[1] + "# END ABSENT-AT-SOURCE-A\nc = 3\n"
PUB_TXT = "p = 1\n"
ART595 = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434/transplant/49financial/"
sha = lambda t: hashlib.sha256(t.encode()).hexdigest()  # noqa: E731


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def put(root, rel, txt):
    f = root / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(txt.encode("utf-8"))


def build(mut=None, cand_hs=CAND_HS, head_hs=CAND_HS, cand_pub=PUB_TXT):
    root = Path(tempfile.mkdtemp(prefix="c237_"))
    shutil.copytree(REAL / "lib", root / "lib", ignore=shutil.ignore_patterns("__pycache__"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    put(root, P.HS, head_hs)
    put(root, ART595 + "holdings_snapshot.py", BASE_HS)
    put(root, ART595 + "publication.py", PUB_TXT)
    rec595 = {"firms": {"49financial": {"minting_pin": P.MINTING, "live_bundle_sha256": "a" * 64, "candidate_bundle_sha256": "b" * 64,
                                        "changed_members": [{"repo_path": P.HS, "artifact": ART595 + "holdings_snapshot.py", "sha256_transplanted": sha(BASE_HS)},
                                                            {"repo_path": P.PUB, "artifact": ART595 + "publication.py", "sha256_transplanted": sha(PUB_TXT)}]}}}
    put(root, P.IB595, json.dumps(rec595))
    put(root, P.ART + "holdings_snapshot.py", cand_hs)
    put(root, P.ART + "publication.py", cand_pub)
    git(root, "add", "-A")
    git(root, "commit", "-qm", "members")
    pin = git(root, "rev-parse", "HEAD")
    rec = {"base_commit": pin, "read_date": "2026-10-15", "claim": "measured", "firm": "49financial", "minting_pin": P.MINTING,
           "method": "Applied the D spans of HEAD onto the signed transplanted file of IB-pr-595, built the bundle twice from the minting pin, compared members with the live bundle, ran the offline tests; nothing uploaded.",
           "transplant_ref": {"candidate_bundle_sha256": "b" * 64}, "live_bundle_sha256": "a" * 64, "candidate_bundle_sha256": "c" * 64,
           "members_total": 46, "members_equal_to_live": 44, "cusip_port_present": True,
           "changed_members": [{"repo_path": P.HS, "artifact": P.ART + "holdings_snapshot.py", "sha256_candidate": sha(cand_hs)},
                               {"repo_path": P.PUB, "artifact": P.ART + "publication.py", "sha256_candidate": sha(cand_pub)}],
           "d_spans": {"count": 2, "equal_to_head": True, "diff_lines_outside_spans": 0}, "tests": {"passed": 90, "failed": 0},
           "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
           "notes": ["the candidate bundle sits in scratch outside the repository and was not uploaded", "the live bundle was downloaded read-only and compared member by member",
                     "the offline tests ran on the candidate tree"]}
    if mut:
        mut(rec)
    put(root, P.REC, json.dumps(rec))
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
    print("%s %-12s %-28s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


NEGS = [
    ("wrong_minting_pin", "AC1", lambda r: r.update(minting_pin="0" * 40), {}),
    ("transplant_ref_wrong", "AC1", lambda r: r["transplant_ref"].update(candidate_bundle_sha256="d" * 64), {}),
    ("live_bundle_wrong", "AC1", lambda r: r.update(live_bundle_sha256="e" * 64), {}),
    ("same_as_signed_digest", "AC2", lambda r: r.update(candidate_bundle_sha256="b" * 64), {}),
    ("same_as_live", "AC2", lambda r: r.update(candidate_bundle_sha256="a" * 64), {}),
    ("third_member", "AC2", lambda r: r["changed_members"].append({"repo_path": "lib/opal_naming.py", "artifact": P.ART + "x.py", "sha256_candidate": "0" * 64}), {}),
    ("publication_changed", "AC2", None, {"cand_pub": "p = 2\n"}),
    ("stray_line_outside_spans", "AC2", None, {"cand_hs": CAND_HS + "z = 9\n"}),
    ("spans_differ_from_head", "AC2", None, {"head_hs": CAND_HS.replace("x = 1", "x = 7")}),
    ("bypass_present", "AC2", None, {"cand_hs": CAND_HS.replace("c = 3\n", "c = 3\nallow_older_date = 1\n"), "head_hs": CAND_HS}),
    ("span_count_wrong", "AC2", lambda r: r["d_spans"].update(count=5), {}),
    ("cusip_port_dropped", "AC2", lambda r: r.update(cusip_port_present=False), {}),
    ("equal_count_wrong", "AC2", lambda r: r.update(members_equal_to_live=40), {}),
    ("tests_failed", "AC3", lambda r: r["tests"].update(failed=2), {}),
    ("no_tests", "AC3", lambda r: r.pop("tests"), {}),
    ("counter_nonzero", "AC3", lambda r: r.update(aws_writes_made=1), {}),
]
root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB237-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn, kw in NEGS:
    root = build(fn, **kw)
    expect(label, "IB237-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
