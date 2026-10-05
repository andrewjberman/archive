"""Round 47 (IRPT_BCKEND ~P, CTO ROUND ANALYSIS rounds 42-46 item E1) -- reconcile ~P's 42 not-closed remediation rows against live.

Usage: python <this file> <repo_root> <criterion_id>
  IB47-1-AC1  the reconciliation file (RECON below) holds exactly the 42 row ids of the census (CENSUS below), each with a
              verdict HOLDS or LIVE, a non-empty close_condition and a non-empty read (the live evidence). Base: FAIL (no file).
  IB47-1-AC2  every HOLDS row has a closing row in the investigation channel added since base 2fd59da001: a row whose JSON names
              the remediation row id and reads disposition DISMISSED_WITH_REASON. Base: FAIL (no file).
  IB47-1-AC3  a GUARD: against base 2fd59da001, the worker's own commits touch no file under surprise-channel/remediations/
              (REMEDIATION rows stay the CVO's) and no path outside org/missions/D9/IRPT/IRPT_BCKEND/. Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "2fd59da001"
RECON = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~116/E1_RECONCILE_ROUNDS_42_46.json"
CHANNEL = "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md"
CENSUS = ["IRPT_BCKEND-S147", "IRPT_BCKEND-S175", "IRPT_BCKEND-S178", "IRPT_BCKEND-S180", "IRPT_BCKEND-W62-S1", "IRPT_BCKEND-W69-S1", "IRPT_BCKEND-S204", "IRPT_BCKEND-S214", "IRPT_BCKEND-S216", "IRPT_BCKEND-S218", "IRPT_BCKEND-W80-S1", "IRPT_BCKEND-S220", "IRPT_BCKEND-W86-S1", "IRPT_BCKEND-W86-S2", "IRPT_BCKEND-S238", "IRPT_BCKEND-S241", "IRPT_BCKEND-S245", "IRPT_BCKEND-S252", "IRPT_BCKEND-S257", "IRPT_BCKEND-W100-S2", "IRPT_BCKEND-W99-S3", "IRPT_BCKEND-S260", "IRPT_BCKEND-S272", "IRPT_BCKEND-S278", "IRPT_BCKEND-S282", "IRPT_BCKEND-S297", "IRPT_BCKEND-S298", "IRPT_BCKEND-W101-S1", "IRPT_BCKEND-W101-S11", "IRPT_BCKEND-W101-S14", "IRPT_BCKEND-W101-S15", "IRPT_BCKEND-W101-S16", "IRPT_BCKEND-W101-S2", "IRPT_BCKEND-W101-S4", "IRPT_BCKEND-W101-S5", "IRPT_BCKEND-W101-S6", "IRPT_BCKEND-W104-S1", "IRPT_BCKEND-W104-S2", "IRPT_BCKEND-W104-S3", "IRPT_BCKEND-W104-S4", "IRPT_BCKEND-W105-S1", "IRPT_BCKEND-W105-S2"]


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB47-1"))
        sys.exit(1)

    def recon():
        p = root / RECON
        if not p.is_file():
            fail("no %s" % RECON)
        rows = json.loads(p.read_bytes().decode("utf-8"))
        return {r.get("id"): r for r in (rows if isinstance(rows, list) else rows.get("rows", []))}

    if cid == "IB47-1-AC1":
        rows = recon()
        if set(rows) != set(CENSUS):
            fail("ids differ: missing %s, extra %s" % (sorted(set(CENSUS) - set(rows))[:5], sorted(set(rows) - set(CENSUS))[:5]))
        for rid, r in rows.items():
            if r.get("verdict") not in ("HOLDS", "LIVE"):
                fail("%s verdict %r" % (rid, r.get("verdict")))
            if not str(r.get("close_condition") or "").strip() or not str(r.get("read") or "").strip():
                fail("%s lacks close_condition or read" % rid)
        n = sum(1 for r in rows.values() if r["verdict"] == "HOLDS")
        print("OK: %d of %d rows reconciled (%d HOLDS, %d LIVE)" % (len(rows), len(CENSUS), n, len(rows) - n))
    elif cid == "IB47-1-AC2":
        rows = recon()
        holds = [rid for rid, r in rows.items() if r.get("verdict") == "HOLDS"]
        base = subprocess.run(["git", "show", "%s:%s" % (BASE, CHANNEL)], cwd=str(root), capture_output=True).stdout.decode("utf-8")
        now = (root / CHANNEL).read_bytes().decode("utf-8")
        if not base or not now.startswith(base[:2000]):
            fail("cannot read the channel at base, or it was rewritten")
        added = now[len(base):] if now.startswith(base) else now
        blocks = re.findall(r"```json\s*(.*?)```", added, re.S)
        closing = set()
        for b in blocks:
            if '"DISMISSED_WITH_REASON"' in b:
                for rid in holds:
                    if '"%s"' % rid in b or rid + " " in b or rid + ":" in b or rid + "," in b:
                        closing.add(rid)
        missing = [rid for rid in holds if rid not in closing]
        if missing:
            fail("%d HOLDS row(s) with no closing row: %s" % (len(missing), missing[:8]))
        print("OK: %d HOLDS rows, each closed by a DISMISSED_WITH_REASON row added since base" % len(holds))
    elif cid == "IB47-1-AC3":
        # only the worker's own commits since BASE: other seats' commits and the shared tree's dirt are not this cell's
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=0.9.0_WK_IRPT_BCKEND~116", "--name-only",
                            "--format="], cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if "/surprise-channel/remediations/" in c or not c.startswith("org/missions/D9/IRPT/IRPT_BCKEND/")]
        if bad:
            fail("out-of-bounds changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside IRPT_BCKEND and none in remediations/" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
