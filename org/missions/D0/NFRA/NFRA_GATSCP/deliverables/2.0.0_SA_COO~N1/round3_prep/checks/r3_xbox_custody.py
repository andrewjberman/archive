"""GS-f-4 AC1 and AC2 (rows D1-S10, Z-S1; ruling R5): who commits a crossbox record, and the integrate's resolver.

Usage: r3_xbox_custody.py lane | resolver

lane -- `python .tools/owned-paths-validate.py --check-path <agent> <path>` (fixed at the cut) reads the STAGED record:
  Arm 1: the record's to_serial (the receiving lane, 0.7.0_AE_CloudOps~ZG) -> PERMIT, rc 0.
  Arm 2: another Codex lane (0.7.0_AE_CloudOps~ZQ) on the same record -> REFUSE, rc 1 ("its own record only").
  Arm 3: a COO lane not named in the lane (2.0.0_SA_COO~W1) -> REFUSE, rc 1 (the lane is otherwise unchanged).
resolver -- `.tools/merge-resolve-known.py` on a crossbox record written on both ends (plumbing commits, unreferenced):
  Arm 1: one side sets ack.at/ack.by, the other sent.bus_message_id -> RESOLVED, the result carries both fields.
  Arm 2: both sides set ack.by to different values -> not resolved, rc != 0 (never a line union).
"""
import json
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "round1_prep", "checks"))
from r1_common import ROOT, git, index_text, plant, run, tail, temp_index  # noqa: E402

XB = "org/devices/crossbox/XB-20261009T105156Z-1c53.json"
mode = sys.argv[1] if len(sys.argv) > 1 else ""
base = json.loads(index_text(XB))
dirs = []


def commit_with(parent, doc, tag):
    d, env = temp_index()
    dirs.append(d)
    git(["read-tree", parent], env=env)
    plant(env, XB, json.dumps(doc, indent=1) + "\n")
    tree = git(["write-tree"], env=env).stdout.strip()
    return git(["commit-tree", tree, "-p", parent, "-m", "probe " + tag]).stdout.strip()


try:
    if mode == "lane":
        d, env = temp_index()
        dirs.append(d)
        doc = dict(base)
        doc["ack"] = {"at": "2026-10-09T11:11:38Z", "by": "0.7.0_AE_CloudOps~ZG", "bus_message_id": None}
        plant(env, XB, json.dumps(doc, indent=1) + "\n")
        v = [sys.executable, ".tools/owned-paths-validate.py", "--check-path"]
        rc1, out1 = run(v + ["0.7.0_AE_CloudOps~ZG", XB], env)
        rc2, out2 = run(v + ["0.7.0_AE_CloudOps~ZQ", XB], env)
        rc3, out3 = run(v + ["2.0.0_SA_COO~W1", XB], env)
        arms = [("receiver-own-record-permitted", rc1 == 0, "rc=%s :: %s" % (rc1, tail(out1, 1))),
                ("other-lane-refused", rc2 == 1, "rc=%s :: %s" % (rc2, tail(out2, 1))),
                ("unnamed-coo-refused", rc3 == 1, "rc=%s :: %s" % (rc3, tail(out3, 1)))]
        for _n, _ok, _d in arms:
            print("  %s %s: %s" % ("PASS" if _ok else "FAIL", _n, _d))
        _bad = sum(1 for a in arms if not a[1])
        print("GS-F4-LANE ok=%s arms=%d failed=%d" % (_bad == 0, len(arms), _bad))
        sys.exit(0 if _bad == 0 else 1)
    if mode == "resolver":
        head = git(["rev-parse", "HEAD"]).stdout.strip()
        a = dict(base)
        a["ack"] = {"at": "2026-10-09T11:11:38Z", "by": "0.7.0_AE_CloudOps~ZG", "bus_message_id": None}
        b = dict(base)
        b["sent"] = {"at": "2026-10-09T10:53:35Z", "bus_message_id": "77379c81-probe"}
        b["ack"] = base.get("ack")
        x, y = commit_with(head, a, "X"), commit_with(head, b, "Y")
        a2 = dict(a)
        a2["ack"] = {"at": "2026-10-09T11:11:38Z", "by": "0.7.0_AE_CloudOps~ZQ", "bus_message_id": None}
        x2 = commit_with(head, a2, "X2")

        def resolve(p1, p2):
            mt = git(["merge-tree", "--write-tree", "--no-messages", p1, p2]).stdout.splitlines()
            t0 = mt[0] if mt else ""
            return run([sys.executable, ".tools/merge-resolve-known.py", "--base", head, "--ours", p1, "--theirs", p2,
                        "--tree", t0, "--cloud", "ours", XB], None)

        rc1, out1 = resolve(x, y)
        merged_ok = False
        for ln in out1.splitlines():
            parts = ln.split()
            if len(parts) >= 3 and parts[0] == "RESOLVED" and parts[1] == XB:
                doc = json.loads(git(["cat-file", "-p", parts[2]]).stdout)
                merged_ok = (doc.get("ack") or {}).get("by") == "0.7.0_AE_CloudOps~ZG" and \
                    (doc.get("sent") or {}).get("bus_message_id") == "77379c81-probe"
        rc2, out2 = resolve(x2, x)
        arms = [("fields-folded", rc1 == 0 and merged_ok, "rc=%s folded=%s :: %s" % (rc1, merged_ok, tail(out1, 2))),
                ("same-field-clash-refused", rc2 != 0, "rc=%s :: %s" % (rc2, tail(out2, 2)))]
        for _n, _ok, _d in arms:
            print("  %s %s: %s" % ("PASS" if _ok else "FAIL", _n, _d))
        _bad = sum(1 for a in arms if not a[1])
        print("GS-F4-RESOLVER ok=%s arms=%d failed=%d" % (_bad == 0, len(arms), _bad))
        sys.exit(0 if _bad == 0 else 1)
    print("usage: r3_xbox_custody.py lane|resolver")
    sys.exit(2)
finally:
    for d in dirs:
        shutil.rmtree(d, ignore_errors=True)
    _ = ROOT
