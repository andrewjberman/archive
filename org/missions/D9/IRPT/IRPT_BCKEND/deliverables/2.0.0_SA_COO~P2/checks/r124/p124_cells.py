"""IRPT_BCKEND round 124 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one BUILD-ONLY order:
  IB124-1  IB-pr-426  irpt-ycharts-generate rebuilt from ONE merged commit (CTO msgs 4621, 4657): the whole entry re-pinned
                      in a candidate map, a census of every member that moves against live, a never-widen packet.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB124-1-AC1  census: built twice identical from one pin that contains the performance/ restoration (c267b71edb); 0 name /
               attribute / method mismatches; live_before == tdpterTM...; every moved member carries its owning commits, a
               class served|inert and a one-line reason; acceptance.py and submission_service.py move together.
               Base: FAIL (no census).
  IB124-1-AC2  replay: every arm identical / expected-diff, at least one negative control, and every member classed
               `served` is named by at least one arm. Base: FAIL (no replay).
  IB124-1-AC3  packet names Branch A, Branch B, the built sha256, the rollback digest and S3 version, and every moved
               member. Base: FAIL (no packet).
"""
import json
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~285/"
LIVE_BEFORE = "tdpterTMfJlWXjnoAQCwil+wN/Jf8Q/yLjGxTk7yUkk="
RESTORED = "c267b71edb"
PAIR = ("acceptance.py", "submission_service.py")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB124"))
        sys.exit(1)

    def load(rel):
        f = root / rel
        if not f.is_file():
            fail("no %s" % rel)
        return json.loads(f.read_text(encoding="utf-8"))

    c = load(D + "IB124-1_generate_census.json")
    moved = c.get("moved_members") or []

    if cid == "IB124-1-AC1":
        if c.get("function") != "irpt-ycharts-generate" or not c.get("pin") or not c.get("built_sha256"):
            fail("census header %r" % {k: c.get(k) for k in ("function", "pin", "built_sha256")})
        p = subprocess.run(["git", "merge-base", "--is-ancestor", RESTORED, str(c["pin"])], cwd=str(root), capture_output=True, timeout=60)
        if p.returncode != 0:
            fail("pin %s does not contain the performance/ restoration %s" % (str(c["pin"])[:10], RESTORED))
        if c.get("built_twice_identical") is not True or c.get("live_before") != LIVE_BEFORE:
            fail("twice %r / live_before %r" % (c.get("built_twice_identical"), c.get("live_before")))
        for k in ("built_signature_mismatched", "built_attribute_mismatched", "built_method_mismatched"):
            if c.get(k) != 0:
                fail("%s = %r" % (k, c.get(k)))
        if not moved:
            fail("no moved_members")
        for m in moved:
            if not m.get("member") or not m.get("owning_commits") or m.get("class") not in ("served", "inert") or not m.get("one_line"):
                fail("moved member row %r" % {k: m.get(k) for k in ("member", "owning_commits", "class")})
        names = {m["member"] for m in moved}
        if len(names) != len(moved):
            fail("a member appears twice")
        if len(names & set(PAIR)) == 1:
            fail("acceptance.py and submission_service.py must move together; only one does")
        if c.get("members_built") != c.get("members_live") and not c.get("member_count_note"):
            fail("member counts differ (%r built, %r live) with no note" % (c.get("members_built"), c.get("members_live")))
        print("OK: built twice identical at %s; 0/0/0; %d moved members, %d served, %d inert" % (
            str(c["pin"])[:10], len(moved), sum(m["class"] == "served" for m in moved), sum(m["class"] == "inert" for m in moved)))
    elif cid == "IB124-1-AC2":
        arms = load(D + "IB124-1_replay.json").get("arms") or []
        if not arms or not all(a.get("verdict") in ("identical", "expected-diff") for a in arms):
            fail("%d arm(s) or a bad verdict" % len(arms))
        if not any(a.get("negative_control") for a in arms):
            fail("no negative control arm")
        covered = set()
        for a in arms:
            covered |= set(a.get("members") or [])
        missing = sorted(m["member"] for m in moved if m.get("class") == "served" and m["member"] not in covered)
        if missing:
            fail("served members no arm names: %s" % missing[:6])
        print("OK: %d arms, all identical / expected-diff; every served member is named by an arm" % len(arms))
    elif cid == "IB124-1-AC3":
        pp = root / (D + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-426.md")
        if not pp.is_file():
            fail("no packet")
        pk = pp.read_text(encoding="utf-8")
        for s in ["Branch A", "Branch B", str(c.get("built_sha256") or ""), LIVE_BEFORE, str(c.get("rollback_version") or "")] + [
                m["member"] for m in moved]:
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        print("OK: packet names both branches, built and rollback, and %d of %d moved members" % (len(moved), len(moved)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
