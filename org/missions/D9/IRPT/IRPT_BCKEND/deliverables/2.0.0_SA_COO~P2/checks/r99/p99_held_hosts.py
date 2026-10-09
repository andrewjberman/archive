"""IRPT_BCKEND round 99 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of the held-hosts cell (CTO msg 2690 via ~V2 msg 2691): the two
served.py hosts IB-pr-390 held out -- irpt-narrative (TypeError on the new served.py against its staged errors.py; row W201-S6) and
irpt-holdings (ADHC_DRIFTD.002 parity gate: holdings_publication_port.py not in files[]; row W201-S5) -- are fixed, restaged, built and
packeted, so every IRPT route reads ONE in the SA route census.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB99-1-AC1  BUILD_ONLY of irpt-narrative AND irpt-holdings at the pin both exit 0 from a clean tree, recorded in the census file C with
              both artifacts' built_sha256 and live_before; and the narrative tests `-k served_error_path` pass (>= 2: the new served.py's
              error path returns the staged errors.py shape for an internal and a service caller). Base: FAIL.
  IB99-1-AC2  the packet P names the pin, both built sha256s and live_befores, Branch A/B, the replay arms, and lists each of the two
              hosts' routes with admitted-firm and other-firm-refused. Base: FAIL.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

WK = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~262/"
C = WK + "IB99-1_release_census.json"
P = WK + "NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-394.md"
NARR = "infra/aws/lambda/investor-reporting/narrative"
HOSTS = ("irpt-narrative", "irpt-holdings")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB99-1"))
        sys.exit(1)

    f = root / C
    if not f.is_file():
        fail("no %s" % C)
    c = json.loads(f.read_text(encoding="utf-8"))
    arts = {a.get("name"): a for a in c.get("artifacts") or []}
    if cid == "IB99-1-AC1":
        bo = c.get("build_only") or {}
        if bo.get("rc") != 0 or bo.get("tree_clean") is not True:
            fail("build_only %r" % bo)
        for h in HOSTS:
            a = arts.get(h) or {}
            if len(str(a.get("built_sha256", ""))) < 40 or not a.get("live_before"):
                fail("%s %r" % (h, a))
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests", "-k", "served_error_path"],
                           cwd=str(root / NARR), capture_output=True, timeout=280)
        out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace")).strip().splitlines()
        last = out[-1] if out else ""
        m = re.search(r"\b(\d+) passed", last)
        if p.returncode != 0 or not m or int(m.group(1)) < 2:
            fail("narrative -k served_error_path rc %d: %s" % (p.returncode, last))
        print("OK: both hosts built; narrative %s" % last)
    elif cid == "IB99-1-AC2":
        if not (root / P).is_file():
            fail("no %s" % P)
        pk = (root / P).read_text(encoding="utf-8")
        need = [str(c.get("pin", "")), "Branch A", "Branch B", "replay"] + list(HOSTS)
        for h in HOSTS:
            need += [str(arts.get(h, {}).get("built_sha256", "")), str(arts.get(h, {}).get("live_before", ""))]
        for s in need:
            if not s or s not in pk:
                fail("packet lacks %r" % s)
        if "refused" not in pk.lower():
            fail("packet lists no other-firm refusal per route")
        print("OK: packet names pin, both hosts, both branches, route table")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
