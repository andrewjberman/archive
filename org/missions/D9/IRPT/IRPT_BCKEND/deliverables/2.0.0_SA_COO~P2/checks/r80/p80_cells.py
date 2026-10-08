"""IRPT_BCKEND round 80 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-367 (E7 of the CTO analysis ADDENDUM 4
@eba8fde8bb: repin irpt-export-render's reports/repository.py, plus any reporting-policy row the read path checks, past b13bab7495;
the never-widen packet for the release; nothing built for upload, nothing applied).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB80-1-AC1  the census file C names a pin P (an ancestor of HEAD) and its changed members; `release-census.py irpt-export-render
              --pin P`, re-run here, prints exactly those members, every one carries a named owner commit in C, and
              repository.py is among them. Base: FAIL (no census file).
  IB80-1-AC2  at P, the source map's staged rows for repository.py and entry.py point at blobs where repository.KINDS names
              CUSTODY_REPORT and entry.py routes custody-report-read; C records a BUILD_ONLY run from a clean worktree at P (rc 0,
              tree_clean true, built_sha256). Base: FAIL (no census file; at HEAD the repository row is pinned at 83e8b9577a,
              whose KINDS lacks CUSTODY_REPORT).
  IB80-1-AC3  the packet K names P, the rollback CodeSha256 03p2eIEK... (live after IB-pr-364), Branch A and Branch B, and the two
              after-reads: an Opal custody-report-read of a real CUSTODY_REPORT by ref, and OBJECT_NOT_COVERED for another firm.
              Base: FAIL (no packet).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~175/"
C = D + "IB80-1_repository_repin_census.json"
K = D + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-367.md"
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-export-render"
ROLLBACK = "03p2eIEKU9iSIOe5GYDbkbisapqAjULUyAPA/Wcxrfc="


def git(root, *a):
    p = subprocess.run(["git", *a], cwd=str(root), capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB80-1"))
        sys.exit(1)

    if cid not in ("IB80-1-AC1", "IB80-1-AC2", "IB80-1-AC3"):
        fail("unknown criterion %r" % cid)
    if cid == "IB80-1-AC3":
        k = root / K
        if not k.is_file():
            fail("no packet %s" % K)
        txt = k.read_text(encoding="utf-8")
        c = json.loads((root / C).read_text(encoding="utf-8")) if (root / C).is_file() else {}
        need = [str(c.get("pin", "<no census pin>"))[:10], ROLLBACK, "Branch A", "Branch B", "CUSTODY_REPORT",
                "custody-report-read", "OBJECT_NOT_COVERED"]
        miss = [n for n in need if n not in txt]
        if miss:
            fail("packet lacks %s" % miss)
        print("OK: packet names the pin, the rollback sha, both branches and both after-reads")
        print("%s PASS" % cid)
        return

    cf = root / C
    if not cf.is_file():
        fail("no census file %s" % C)
    c = json.loads(cf.read_text(encoding="utf-8"))
    pin = str(c.get("pin", ""))
    if not re.fullmatch(r"[0-9a-f]{10,40}", pin):
        fail("census pin %r" % pin)
    if git(root, "merge-base", "--is-ancestor", pin, "HEAD")[0] != 0:
        fail("pin %s is not an ancestor of HEAD" % pin)

    if cid == "IB80-1-AC1":
        members = c.get("changed_members") or []
        names = {m.get("member") for m in members}
        if not names or "repository.py" not in names:
            fail("census members %r lack repository.py" % sorted(n for n in names if n))
        unowned = [m.get("member") for m in members if not re.fullmatch(r"[0-9a-f]{10,40}", str(m.get("owner_commit", "")))]
        if unowned:
            fail("members without an owner commit: %s" % unowned)
        p = subprocess.run([sys.executable, str(root / "infra/aws/lambda/ci/release-census.py"), FN, "--pin", pin],
                           cwd=str(root), capture_output=True, timeout=280)
        out = p.stdout.decode("utf-8", "replace")
        live = set(re.findall(r"^(?:changed|added|removed)\s+(\S+)", out, re.M))
        if live != names:
            fail("census re-run members %s != census file %s" % (sorted(live), sorted(names)))
        print("OK: pin %s, %d changed members re-read, each owned: %s" % (pin[:10], len(live), sorted(live)))
    else:
        rc, raw = git(root, "show", "%s:%s" % (pin, MAP))
        if rc:
            fail("source map unreadable at %s" % pin)
        rows = json.loads(raw)
        rows = rows.get("functions", rows)[FN]["staged_from"]
        got = {}
        for want in ("repository.py", "entry.py"):
            r = [x for x in rows if x.get("packaged_as") == want]
            if want == "entry.py" and not r:
                got[want] = None
                continue
            if len(r) != 1:
                fail("%d staged rows packaged as %s at %s" % (len(r), want, pin))
            rc, blob = git(root, "show", "%s:%s" % (r[0]["pin"], r[0]["repo_path"]))
            if rc:
                fail("cannot read %s at %s" % (r[0]["repo_path"], r[0]["pin"]))
            got[want] = blob
        kinds = re.search(r"^KINDS\s*=\s*(.+)$", got["repository.py"], re.M)
        if not kinds or "CUSTODY_REPORT" not in kinds.group(1):
            fail("repository.KINDS at the pinned row lacks CUSTODY_REPORT: %r" % (kinds.group(1) if kinds else None))
        entry = got["entry.py"]
        if entry is None:
            rc, entry = git(root, "show", "%s:infra/aws/lambda/investor-reporting/export/entry.py" % pin)
        if "custody-report-read" not in (entry or ""):
            fail("entry.py packaged at the pin does not route custody-report-read")
        b = c.get("build_only") or {}
        if b.get("rc") != 0 or b.get("tree_clean") is not True or not b.get("built_sha256"):
            fail("build_only record %r" % b)
        print("OK: at %s KINDS %s; entry.py routes custody-report-read; BUILD_ONLY rc 0 from a clean tree, built %s"
              % (pin[:10], kinds.group(1).strip(), b["built_sha256"][:12]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
