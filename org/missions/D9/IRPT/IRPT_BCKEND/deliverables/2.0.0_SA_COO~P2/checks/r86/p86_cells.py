"""IRPT_BCKEND round 86 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-373 (E10 recut, replacing IB-pr-372 per CTO msg 1651; E10 of CTO ADDENDUM 10: a production
composition site for persist_custody_report in irpt-export-render, the function that runs IRPT_CUSTDY's render (PRD S07), composed
with irpt-custody-x10-v1 through the registry-gated probe; its release packet carries the ACTIVE registry row b4d98a4fe3).

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB86-1-AC1  the census file C names a pin P (an ancestor of HEAD); `release-census.py irpt-export-render --pin P`, re-run here,
              prints exactly C's changed members, each with an owner commit; the writer (custody_write.py) and the registry row are
              among them, and the registry packaged at P carries irpt-custody-x10-v1 ACTIVE. Base: FAIL (no census file).
  IB86-1-AC2  in T, three groups each pass (>= 1 test): `custody_writer_composed` (a CUSTODY_REPORT retained under
              irpt-custody-x10-v1 and read back; an unregistered kind refuses), `derived_owner` (owner and account set derived
              server-side; a caller-supplied principal, owner or account field cannot change what is stored), and
              `guarded_or_scheduled` (the persist is reachable only through the guarded Entry or an in-function scheduled run;
              an unauthenticated / non-Opal / other-firm caller refuses); and export/entry.py carries no irpt_custody_persist
              direct-invoke path (CTO msg 1651). Base: FAIL (no file).
  IB86-1-AC3  the packet K names P, the rollback CodeSha256 PbyqmHBQ... (live after IB-pr-371), the host function and its entry
              point ("irpt-export-render"), Branch A and Branch B, the two after-reads, and C records a clean-tree BUILD_ONLY (rc 0).
              Base: FAIL (no packet).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~181/"
C = D + "IB86-1_e10_census.json"
K = D + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-373.md"
T = "infra/aws/lambda/investor-reporting/export/tests/test_custody_writer_composed.py"
MAP = "infra/aws/lambda/ci/lambda-source-map.json"
FN = "irpt-export-render"
ROLLBACK = "PbyqmHBQpr4DC76qt0noBfoqKVleydNaJ7s2qsx5mT0="


def git(root, *a):
    p = subprocess.run(["git", *a], cwd=str(root), capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB86-1"))
        sys.exit(1)

    if cid == "IB86-1-AC2":
        t = root / T
        if not t.is_file():
            fail("no %s" % T)
        res = []
        for k in ("custody_writer_composed", "derived_owner", "guarded_or_scheduled"):
            p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", t.name, "-k", k],
                               cwd=str(t.parent), capture_output=True, timeout=280)
            out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
            last = [ln for ln in out.splitlines() if ln.strip()]
            last = last[-1] if last else ""
            if p.returncode != 0 or not re.search(r"\b[1-9]\d* passed", last):
                fail("-k %s rc %d: %s" % (k, p.returncode, last))
            res.append("%s: %s" % (k, last))
        entry_src = (root / "infra/aws/lambda/investor-reporting/export/entry.py").read_text(encoding="utf-8")
        if "irpt_custody_persist" in entry_src:
            fail("entry.py still carries the caller-asserted irpt_custody_persist direct-invoke path (CTO msg 1651)")
        print("OK: " + "; ".join(res))
        print("%s PASS" % cid)
        return
    if cid not in ("IB86-1-AC1", "IB86-1-AC3"):
        fail("unknown criterion %r" % cid)
    cf = root / C
    if not cf.is_file():
        fail("no census file %s" % C)
    c = json.loads(cf.read_text(encoding="utf-8"))
    pin = str(c.get("pin", ""))
    if not re.fullmatch(r"[0-9a-f]{10,40}", pin) or git(root, "merge-base", "--is-ancestor", pin, "HEAD")[0] != 0:
        fail("census pin %r is not an ancestor of HEAD" % pin)
    if cid == "IB86-1-AC3":
        k = root / K
        if not k.is_file():
            fail("no packet %s" % K)
        txt = k.read_text(encoding="utf-8")
        miss = [n for n in (pin[:10], ROLLBACK, FN, "Branch A", "Branch B", "custody-report-read", "OBJECT_NOT_COVERED") if n not in txt]
        if miss:
            fail("packet lacks %s" % miss)
        b = c.get("build_only") or {}
        if b.get("rc") != 0 or b.get("tree_clean") is not True or not b.get("built_sha256"):
            fail("build_only record %r" % b)
        print("OK: packet complete; BUILD_ONLY rc 0 from a clean tree, built %s" % b["built_sha256"][:12])
        print("%s PASS" % cid)
        return
    members = c.get("changed_members") or []
    names = {m.get("member") for m in members}
    if not any("custody_write" in str(n) for n in names) or not any("reporting_policies.json" in str(n) for n in names):
        fail("census members %r lack the writer or the registry row" % sorted(n for n in names if n))
    unowned = [m.get("member") for m in members if not re.fullmatch(r"[0-9a-f]{10,40}", str(m.get("owner_commit", "")))]
    if unowned:
        fail("members without an owner commit: %s" % unowned)
    p = subprocess.run([sys.executable, str(root / "infra/aws/lambda/ci/release-census.py"), FN, "--pin", pin],
                       cwd=str(root), capture_output=True, timeout=280)
    live = set(re.findall(r"^(?:changed|added|removed)\s+(\S+)", p.stdout.decode("utf-8", "replace"), re.M))
    if live != names:
        fail("census re-run members %s != census file %s" % (sorted(live), sorted(names)))
    rc, raw = git(root, "show", "%s:%s" % (pin, MAP))
    rows = json.loads(raw).get("functions", json.loads(raw))[FN]["staged_from"]
    reg = [x for x in rows if x.get("packaged_as", "").endswith("reporting_policies.json")]
    rc, regblob = git(root, "show", "%s:%s" % (reg[0]["pin"], reg[0]["repo_path"])) if len(reg) == 1 else (1, "")
    pol = None
    try:
        doc = json.loads(regblob)
        for r in json.dumps(doc) and (doc.get("policies") if isinstance(doc, dict) and "policies" in doc else doc if isinstance(doc, list) else list(doc.values()) if isinstance(doc, dict) else []):
            if isinstance(r, dict) and "irpt-custody-x10-v1" in json.dumps(r):
                pol = r
    except ValueError:
        pass
    if not pol or "ACTIVE" not in json.dumps(pol) or "PENDING_ENFORCEMENT" in json.dumps(pol):
        fail("the registry packaged at P does not carry irpt-custody-x10-v1 ACTIVE")
    print("OK: pin %s, %d owned members incl. the writer and the registry; packaged irpt-custody-x10-v1 is ACTIVE" % (pin[:10], len(names)))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
