"""IRPT_BCKEND round 76 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of the CTO's rounds 69-74 analysis enrichment
(@b35c7d8c73, msg 1214; the CTO's "round 75" is numbered 76 here because round 75 already holds IB-pr-361):
  E1 = IB-pr-362: the four ARMED rows (S334, W140-S1, W145-S2, W165-S2) disarmed or re-justified;
  E2 = IB-pr-363: the custody release packet (P-c1..c3 plus the custody-report-read route) as ONE release pair.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line. Every check finishes inside 120 s.

  IB76-1-AC1  deliverables/0.9.0_WK_IRPT_BCKEND~170/IB76-1_armed_rows.json names each of the 4 rows exactly once, each either
              {"state": "DISARMED", "resolving_row": "<id present in the channel>", "evidence": "..."} or
              {"state": "ARMED", "disarm_act": "...", "owner": "<serial>"}; and it prints "armed_after": N equal to the ARMED count.
              Base: FAIL (no file).
  IB76-2-AC1  deliverables/0.9.0_WK_IRPT_BCKEND~171/IB76-2_custody_release_census.json carries one "pin", and for every function it
              lists: "changed_members" (each with "member" and a non-empty "owner" naming an IB order), "rollback_object_version"
              and "live_code_sha256"; every function's census at the pin is reproduced by release-census.py with the same member set.
              Base: FAIL (no file).
  IB76-2-AC2  deliverables/0.9.0_WK_IRPT_BCKEND~171/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-363.md exists and names both branches
              (released / rolled back), the pin, and the two after-reads (a refused other-firm read; an Opal read of one custody
              report by ref). Base: FAIL (no file).
  IB76-G-<n>  A GUARD for slot ~<n> (170, 171): that worker's commits touch only its grant. Base: PASS.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "b7e16c7230"
P = "org/missions/D9/IRPT/IRPT_BCKEND"
CH = P + "/surprise-channel/investigations/INVESTIGATION_v1.md"
ROWS = ("IRPT_BCKEND-S334", "IRPT_BCKEND-W140-S1", "IRPT_BCKEND-W145-S2", "IRPT_BCKEND-W165-S2")
TO = P + "/task-orders/IRPT_BCKEND.TO-IB-pr-"
GRANTS = {
    "170": (CH, TO + "362.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~170/"),
    "171": (CH, TO + "363.", P + "/deliverables/0.9.0_WK_IRPT_BCKEND~171/", "infra/aws/lambda/ci/lambda-source-map.json"),
}


def _run(cmd, cwd, timeout=110):
    r = subprocess.run(cmd, cwd=str(cwd), capture_output=True, timeout=timeout)
    out = (r.stdout or b"").decode("utf-8", "replace") + (r.stderr or b"").decode("utf-8", "replace")
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", out)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB76"))
        sys.exit(1)

    if cid == "IB76-1-AC1":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~170/IB76-1_armed_rows.json"
        if not f.is_file():
            fail("no IB76-1_armed_rows.json")
        d = json.loads(f.read_text(encoding="utf-8"))
        rows = d.get("rows") or {}
        if sorted(rows) != sorted(ROWS):
            fail("rows named %s, expected exactly %s" % (sorted(rows), list(ROWS)))
        channel = (root / CH).read_text(encoding="utf-8")
        armed = 0
        for rid, r in rows.items():
            st = r.get("state")
            if st == "DISARMED":
                rr = r.get("resolving_row", "")
                if not rr or ('"id": "%s"' % rr) not in channel or not r.get("evidence"):
                    fail("%s DISARMED without a resolving row present in the channel and evidence" % rid)
            elif st == "ARMED":
                armed += 1
                if not r.get("disarm_act") or not r.get("owner"):
                    fail("%s ARMED without its disarm act and owner" % rid)
            else:
                fail("%s state %r" % (rid, st))
        if d.get("armed_after") != armed:
            fail("armed_after %r != %d ARMED rows" % (d.get("armed_after"), armed))
        print("OK: 4 of 4 rows ruled; %d disarmed, armed_after=%d" % (4 - armed, armed))
    elif cid == "IB76-2-AC1":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~171/IB76-2_custody_release_census.json"
        if not f.is_file():
            fail("no IB76-2_custody_release_census.json")
        d = json.loads(f.read_text(encoding="utf-8"))
        pin = d.get("pin")
        fns = d.get("functions") or {}
        if not pin or not fns:
            fail("no pin or no functions")
        for fn, v in fns.items():
            mem = v.get("changed_members") or []
            if not mem or any(not m.get("member") or not re.search(r"IB-[a-z0-9-]+", str(m.get("owner", ""))) for m in mem):
                fail("%s: a changed member lacks its member name or an IB-order owner" % fn)
            if not v.get("rollback_object_version") or not v.get("live_code_sha256"):
                fail("%s: no rollback_object_version or live_code_sha256" % fn)
            rc, out = _run([sys.executable, "infra/aws/lambda/ci/release-census.py", fn, "--pin", pin], root)
            got = sorted(set(re.findall(r"^(?:changed|added|removed) (\S+)", out, re.M)))
            want = sorted(set(m["member"] for m in mem))
            if rc or got != want:
                fail("%s census at %s gives %s, the file lists %s" % (fn, pin, got, want))
        print("OK: %d function(s) at pin %s, every changed member owned, census reproduced" % (len(fns), pin))
    elif cid == "IB76-2-AC2":
        f = root / P / "deliverables/0.9.0_WK_IRPT_BCKEND~171/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-363.md"
        if not f.is_file():
            fail("no NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-363.md")
        t = f.read_text(encoding="utf-8").lower()
        for need in ("branch a", "branch b", "pin", "rollback", "other firm", "custody-report-read"):
            if need not in t:
                fail("the packet never names %r" % need)
        print("OK: the packet names both branches, the pin, rollback and both after-reads")
    elif cid.startswith("IB76-G-"):
        slot = cid.rsplit("-", 1)[1]
        grant = GRANTS.get(slot)
        if not grant:
            fail("unknown slot %r" % slot)
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~%s" % slot, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if not c.startswith(grant)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside slot ~%s's grant" % (len(changed), slot))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
