"""IRPT_BCKEND round 88 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-376 (the release packet for IB-pr-375:
irpt-export-render packages persisted_by + the composition-hash binding; nothing uploaded or applied).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB88-1-AC1  the census file C names a pin P (an ancestor of HEAD); release-census.py irpt-export-render --pin P, re-run here,
              prints exactly C's changed members, each with an owner commit, and custody_persist.py is among them; every member
              C lists is changed at P relative to live. Base: FAIL (no census file).
  IB88-1-AC2  C records a clean-tree BUILD_ONLY at P (rc 0, tree_clean true, built_sha256), and the packet K names P, the
              rollback CodeSha256 rNjtTwcm... (live after IB-pr-374), Branch A, Branch B, persisted_by and composition_sha256.
              Base: FAIL (no census file, no packet).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~184/"
C = D + "IB88-1_census.json"
K = D + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-376.md"
FN = "irpt-export-render"
ROLLBACK = "rNjtTwcmhpNdHUV7VcO1cRPcC1wHaANm1oIP+Xvf6Ek="


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB88-1"))
        sys.exit(1)

    if cid not in ("IB88-1-AC1", "IB88-1-AC2"):
        fail("unknown criterion %r" % cid)
    cf = root / C
    if not cf.is_file():
        fail("no census file %s" % C)
    c = json.loads(cf.read_text(encoding="utf-8"))
    pin = str(c.get("pin", ""))
    if not re.fullmatch(r"[0-9a-f]{10,40}", pin):
        fail("census pin %r" % pin)
    if subprocess.run(["git", "merge-base", "--is-ancestor", pin, "HEAD"], cwd=str(root)).returncode != 0:
        fail("pin %s is not an ancestor of HEAD" % pin)
    if cid == "IB88-1-AC1":
        members = c.get("changed_members") or []
        names = {m.get("member") for m in members}
        if "custody_persist.py" not in names:
            fail("census members %r lack custody_persist.py" % sorted(n for n in names if n))
        unowned = [m.get("member") for m in members if not re.fullmatch(r"[0-9a-f]{10,40}", str(m.get("owner_commit", "")))]
        if unowned:
            fail("members without an owner commit: %s" % unowned)
        p = subprocess.run([sys.executable, str(root / "infra/aws/lambda/ci/release-census.py"), FN, "--pin", pin],
                           cwd=str(root), capture_output=True, timeout=280)
        live = set(re.findall(r"^(?:changed|added|removed)\s+(\S+)", p.stdout.decode("utf-8", "replace"), re.M))
        if live != names:
            fail("census re-run members %s != census file %s" % (sorted(live), sorted(names)))
        print("OK: pin %s, %d owned members: %s" % (pin[:10], len(names), sorted(names)))
    else:
        b = c.get("build_only") or {}
        if b.get("rc") != 0 or b.get("tree_clean") is not True or not b.get("built_sha256"):
            fail("build_only record %r" % b)
        k = root / K
        if not k.is_file():
            fail("no packet %s" % K)
        txt = k.read_text(encoding="utf-8")
        miss = [n for n in (pin[:10], ROLLBACK, "Branch A", "Branch B", "persisted_by", "composition_sha256") if n not in txt]
        if miss:
            fail("packet lacks %s" % miss)
        print("OK: BUILD_ONLY rc 0 clean, built %s; packet complete" % b["built_sha256"][:12])
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
