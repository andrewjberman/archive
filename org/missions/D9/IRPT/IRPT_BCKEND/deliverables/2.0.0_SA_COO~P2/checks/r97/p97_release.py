"""IRPT_BCKEND round 97 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of the three release-packet cells (CTO msg 2507 (b)):
IB-pr-389 (runner bundle; IB-pr-384), IB-pr-390 (_authz served.py hosts; IB-pr-385 + IB-pr-387), IB-pr-391 (the new composition-read
Lambda; IB-pr-386). BUILD_ONLY and offline replays only; the pairs are signed after IB-pr-383 closes.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB97-<k>-AC1  the census file C_k: {pin, artifacts: [{name, built_sha256, live_before, changed_members: [{member, owner_commit}]}],
                build_only: {rc: 0, tree_clean: true}} with >= 1 artifact, every artifact built and every changed member owned.
                Base: FAIL (no file).
  IB97-<k>-AC2  the packet P_k names the pin, every artifact's built sha256 and live_before, "Branch A", "Branch B", "replay" and
                "after-read"; the replay file R_k records every arm "identical" or "expected-diff" with a negative control.
                Base: FAIL (no files).
k = 2 (IB-pr-389, worker ~200), 3 (IB-pr-390, worker ~201), 4 (IB-pr-391, worker ~202).
"""
import json
import re
import sys
from pathlib import Path

B = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
CELLS = {
    "2": ("0.9.0_WK_IRPT_BCKEND~200/", "IB-pr-389"),
    "3": ("0.9.0_WK_IRPT_BCKEND~201/", "IB-pr-390"),
    "4": ("0.9.0_WK_IRPT_BCKEND~202/", "IB-pr-391"),
}


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB97"))
        sys.exit(1)

    m = re.fullmatch(r"IB97-([234])-(AC[12])", cid)
    if not m:
        fail("unknown criterion %r" % cid)
    folder, cell = CELLS[m.group(1)]
    k = m.group(1)
    cpath = root / (B + folder + "IB97-%s_release_census.json" % k)
    ppath = root / (B + folder + "NEVER_WIDEN_SIGNOFF_PACKET_%s.md" % cell)
    rpath = root / (B + folder + "IB97-%s_release_replay.json" % k)
    if not cpath.is_file():
        fail("no %s" % cpath.relative_to(root))
    c = json.loads(cpath.read_text(encoding="utf-8"))
    arts = c.get("artifacts") or []
    if m.group(2) == "AC1":
        bo = c.get("build_only") or {}
        if not c.get("pin") or not arts or bo.get("rc") != 0 or bo.get("tree_clean") is not True:
            fail("census pin/artifacts/build_only %r" % {"pin": c.get("pin"), "n": len(arts), "build_only": bo})
        for a in arts:
            if not a.get("name") or len(str(a.get("built_sha256", ""))) < 40 or not a.get("live_before"):
                fail("artifact %r" % a)
            for ch in a.get("changed_members") or []:
                if not ch.get("member") or not ch.get("owner_commit"):
                    fail("unowned member %r in %s" % (ch, a.get("name")))
        print("OK: pin %s; %d artifact(s): %s" % (c["pin"], len(arts), ", ".join(a["name"] for a in arts)))
    else:
        if not ppath.is_file() or not rpath.is_file():
            fail("missing packet or replay file")
        pk = ppath.read_text(encoding="utf-8")
        need = [str(c.get("pin", ""))] + ["Branch A", "Branch B", "replay", "after-read"]
        for a in arts:
            need += [str(a.get("built_sha256", "")), str(a.get("live_before", ""))]
        for s in need:
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        r = json.loads(rpath.read_text(encoding="utf-8"))
        arms = r.get("arms") or []
        if not arms or any(x.get("verdict") not in ("identical", "expected-diff") for x in arms) \
                or not any(x.get("negative_control") for x in arms):
            fail("replay arms %r" % arms)
        print("OK: packet names pin, %d artifact(s), both branches; %d replay arm(s) with a negative control" % (len(arts), len(arms)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
