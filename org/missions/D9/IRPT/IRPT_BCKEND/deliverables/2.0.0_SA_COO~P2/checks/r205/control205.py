"""Positive control and negatives for p205_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control205.py <real_repo_root>
Builds temp git roots holding stub members at the real repo paths (a commit that carries commentary_requested, one that does not), runs every
criterion expecting PASS on the clean record, then applies each mutation expecting the NAMED criterion to FAIL. The temp roots are removed.
"""
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
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r205/p205_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p205_cells as P  # noqa: E402

LIVE = P.LIVE_DIGEST


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def build():
    root = Path(tempfile.mkdtemp(prefix="c205_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for k, (path, _signed) in P.ENDPOINT.items():
        f = root / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("# member %s\nFLAG = 'commentary_requested'\n" % k, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "with")
    with_pin = git(root, "rev-parse", "HEAD")
    for k, (path, _signed) in P.ENDPOINT.items():
        (root / path).write_text("# member %s\nFLAG = 'older'\n" % k, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "without")
    without_pin = git(root, "rev-parse", "HEAD")
    return root, with_pin, without_pin


def record(root, with_pin):
    em = {}
    for k, (path, signed) in P.ENDPOINT.items():
        data = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (with_pin, path)], capture_output=True, check=True).stdout
        now = hashlib.sha256(data).hexdigest()
        em[k] = {"repo_path": path, "pin": with_pin, "sha256_at_signing": signed, "sha256_now": now,
                 "commentary_requested_count": data.count(b"commentary_requested"), "changed": now != signed}
    return {"base_commit": with_pin, "function": "irpt-ycharts-generate", "live_codesha256": LIVE,
            "candidate": {"codesha256": "Zq3" + "A" * 40 + "=", "moved_count": 4, "total_members": 106,
                          "moved_members": ["submission.py", "acceptance.py", "contracts/AnalysisSubmissionRequest.schema.json", "composition_admission.py"]},
            "override_map_used": True, "r29c_members_preserved": True, "endpoint_members": em, "endpoint_bytes_moved": True, "resign_needed": True,
            "composition_admission_moved": True, "pre_apply_digest_restated": LIVE,
            "notes": ["built with BAU_SOURCE_MAP_OVERRIDE from make_candidate_map.py at the signed pin", "not read: the live event source mappings and routes",
                      "the candidate zip sits in scratch outside the repository, never uploaded"],
            **{k: 0 for k in P.P6.BOUND}}


def write(root, rec):
    p = root / P.REC
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, indent=1), encoding="utf-8")


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=120, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


def mut(name, fn):
    def go(rec, without_pin):
        r = copy.deepcopy(rec)
        fn(r, without_pin)
        return r
    return name, go


MUTS = [
    ("AC1", mut("candidate_is_wrong_MfxpvRhV", lambda r, w: r["candidate"].__setitem__("codesha256", "MfxpvRhV" + "A" * 35 + "="))),
    ("AC1", mut("candidate_is_live", lambda r, w: r["candidate"].__setitem__("codesha256", LIVE))),
    ("AC1", mut("no_override", lambda r, w: r.__setitem__("override_map_used", False))),
    ("AC1", mut("endpoint_not_moved", lambda r, w: r["candidate"].update(moved_members=["composition_admission.py", "a.py", "b.py", "c.py"]))),
    ("AC1", mut("count_mismatch", lambda r, w: r["candidate"].__setitem__("moved_count", 3))),
    ("AC2", mut("r29c_member_moved", lambda r, w: r["candidate"].update(moved_members=r["candidate"]["moved_members"][:3] + ["uploads.py"]))),
    ("AC2", mut("r29c_flag_false", lambda r, w: r.__setitem__("r29c_members_preserved", False))),
    ("AC2", mut("pin_without_feature", lambda r, w: [r["endpoint_members"]["acceptance.py"].__setitem__("pin", w)])),
    ("AC2", mut("wrong_now_hash", lambda r, w: r["endpoint_members"]["submission.py"].__setitem__("sha256_now", "e" * 64))),
    ("AC2", mut("wrong_signed_hash", lambda r, w: r["endpoint_members"]["submission.py"].__setitem__("sha256_at_signing", "d" * 64))),
    ("AC2", mut("resign_false_while_changed", lambda r, w: r.__setitem__("resign_needed", False))),
    ("AC3", mut("digest_not_restated", lambda r, w: r.__setitem__("pre_apply_digest_restated", "x" * 44))),
    ("AC3", mut("composition_flag_wrong", lambda r, w: r.__setitem__("composition_admission_moved", False))),
    ("AC3", mut("short_notes", lambda r, w: r.__setitem__("notes", ["short"]))),
    ("AC3", mut("counter_nonzero", lambda r, w: r.__setitem__("vendor_requests_sent", 1))),
]

bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-30s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


root, with_pin, without_pin = build()
rec = record(root, with_pin)
write(root, rec)
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB205-1-" + ac, root, True)
for ac, (name, fn) in MUTS:
    write(root, fn(rec, without_pin))
    expect(name, "IB205-1-" + ac, root, False)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
