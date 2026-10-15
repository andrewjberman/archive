"""Positive control and negatives for p228_cells.py (run by the issuer at the cut). Usage: python control228.py <real_repo_root>"""
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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r228/p228_cells.py"
sys.path.insert(0, str(CHECK.parent))
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent.parent / "r218"))
import p228_cells as P  # noqa: E402

HS_TXT = "# BEGIN ABSENT-AT-SOURCE-A\na = 1\n# END ABSENT-AT-SOURCE-A\n# BEGIN ABSENT-AT-SOURCE-B\nb = 2\n# END ABSENT-AT-SOURCE-B\n# BEGIN ABSENT-AT-SOURCE-C\nc = 3\n# END ABSENT-AT-SOURCE-C\n"
PUB_TXT = "p = 1\n"
OTHER_PATH = "lib/opal_naming.py"


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build(mut=None, hs_text=HS_TXT):
    root = Path(tempfile.mkdtemp(prefix="c228_"))
    (root / "lib").mkdir()
    shutil.copy(REAL / "lib/trading_calendar.py", root / "lib/trading_calendar.py")
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel, txt in ((P.HS, hs_text), (P.PUB, PUB_TXT), (OTHER_PATH, "x = 1\n")):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(txt, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "members")
    pin = git(root, "rev-parse", "HEAD")
    art_dir = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~434/transplant/"
    for rel, txt in ((art_dir + "hs.py", hs_text), (art_dir + "pub.py", PUB_TXT)):
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(txt.encode("utf-8"))
    firm = {"live_bundle_sha256": "a" * 64, "candidate_bundle_sha256": "b" * 64, "members_total": 46, "members_equal_to_live": 44,
            "changed_members": [{"repo_path": P.HS, "artifact": art_dir + "hs.py", "sha256_transplanted": hashlib.sha256(hs_text.encode()).hexdigest()},
                                {"repo_path": P.PUB, "artifact": art_dir + "pub.py", "sha256_transplanted": hashlib.sha256(PUB_TXT.encode()).hexdigest()}],
            "transplant": {"one_date_bypass_absent": True, "cusip_port_present": False, "foreign_diff_lines": 12,
                           "foreign_diff_reading": "The only lines outside the exemption blocks that differ from the minting pin are the gate's new keyword argument and its plumbing lines."},
            "overlay_tests": {"passed": 120, "failed": 0}}
    rec = {"base_commit": pin, "read_date": "2026-10-15", "claim": "measured", "overlay_pin": pin,
           "method": "Built each firm's bundle from its minting pin with only holdings_snapshot.py and publication.py overlaid from the overlay pin, BUILD ONLY, ran the offline tests on that tree, and compared members with the live bundle; nothing uploaded.",
           "firms": {f: dict(copy.deepcopy(firm), minting_pin=P.MINTING[f]) for f in P.FIRMS},
           "functions_invoked": 0, "sign_ins_made": 0, "aws_writes_made": 0, "rows_written": 0, "figures_written": 0, "vendor_requests_sent": 0,
           "notes": ["the candidate bundles sit in scratch outside the repository and were not uploaded", "the live bundles were downloaded read-only and compared member by member",
                     "the offline tests ran on the overlay tree of each firm"]}
    rec["firms"]["49financial"]["transplant"]["cusip_port_present"] = True
    if mut:
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


def third_member(r):
    r["firms"]["cottonwood"]["changed_members"].append({"repo_path": OTHER_PATH, "sha256_at_pin": hashlib.sha256(b"x = 1\n").hexdigest()})


NEGS = [
    ("wrong_minting_pin", "AC1", lambda r: r["firms"]["cottonwood"].update(minting_pin="0" * 40)),
    ("two_firms", "AC1", lambda r: r["firms"].pop("inflection")),
    ("same_bundle", "AC2", lambda r: r["firms"]["inflection"].update(candidate_bundle_sha256="a" * 64)),
    ("third_member_moved", "AC2", third_member),
    ("wrong_member_sha", "AC2", lambda r: r["firms"]["49financial"]["changed_members"][0].update(sha256_transplanted="0" * 64)),
    ("bypass_present", "AC2", lambda r: r["firms"]["cottonwood"]["transplant"].update(one_date_bypass_absent=False)),
    ("cusip_port_dropped_for_49f", "AC2", lambda r: r["firms"]["49financial"]["transplant"].update(cusip_port_present=False)),
    ("cusip_port_added_for_cot", "AC2", lambda r: r["firms"]["cottonwood"]["transplant"].update(cusip_port_present=True)),
    ("foreign_diff_too_big", "AC2", lambda r: r["firms"]["inflection"]["transplant"].update(foreign_diff_lines=300)),
    ("equal_count_wrong", "AC2", lambda r: r["firms"]["49financial"].update(members_equal_to_live=40)),
    ("tests_failed", "AC3", lambda r: r["firms"]["cottonwood"]["overlay_tests"].update(failed=2)),
    ("no_tests_run", "AC3", lambda r: r["firms"]["inflection"].pop("overlay_tests")),
    ("counter_nonzero", "AC3", lambda r: r.update(aws_writes_made=1)),
]
root = build()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB228-1-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)
for label, ac, fn in NEGS:
    root = build(fn)
    expect(label, "IB228-1-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
root = build(hs_text="x = 1\n")
expect("pin_lacks_blocks", "IB228-1-AC1", root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
