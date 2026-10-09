"""IRPT_BCKEND round 94 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-382: the production custody ports ~P owns for
release 6 (CTO ruling msg 2128; contract deliverables/2.0.0_SA_COO~Y2/release6_custody/CUSTODY_PORT_CONTRACT.md @859ae01405):
port 1 current_selection, port 3 interpret_source, port 4 validate_evidence, for _scope/accepted_custody.py AcceptedCustodyReader.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB94-1-AC1  in _scope/tests, `-k custody_current_selection` passes (>= 2) and `-k custody_interpret_source` passes (>= 3).
              Base: FAIL (no such tests).
  IB94-1-AC2  in _scope/tests, `-k custody_validate_evidence` passes (>= 3) and `-k custody_ports_compose` passes (>= 1); the whole
              _scope/tests suite passes. Base: FAIL.
  IB94-1-AC3  the read-set file R names, per port, the module and function, and every AWS read it makes
              (reads: [{service, resource, action}], may be empty), and `release6_staged` lists the repo paths release 6 must stage.
              Base: FAIL (no file).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SCOPE = "infra/aws/lambda/investor-reporting/_scope"
R = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~190/IB94-1_custody_ports_read_set.json"
PORTS = ("current_selection", "interpret_source", "validate_evidence")


def pytest(cwd, *args):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    last = [ln for ln in out.splitlines() if ln.strip()]
    return p.returncode, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB94-1"))
        sys.exit(1)

    def sel(name, n):
        rc, last = pytest(root / SCOPE, "tests", "-k", name)
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < n:
            fail("-k %s rc %d: %s" % (name, rc, last))
        return last

    if cid == "IB94-1-AC1":
        a = sel("custody_current_selection", 2)
        b = sel("custody_interpret_source", 3)
        print("OK: current_selection %s; interpret_source %s" % (a, b))
    elif cid == "IB94-1-AC2":
        a = sel("custody_validate_evidence", 3)
        b = sel("custody_ports_compose", 1)
        rc, last = pytest(root / SCOPE, "tests")
        if rc != 0:
            fail("_scope suite rc %d: %s" % (rc, last))
        print("OK: validate_evidence %s; compose %s; suite %s" % (a, b, last))
    elif cid == "IB94-1-AC3":
        f = root / R
        if not f.is_file():
            fail("no %s" % R)
        d = json.loads(f.read_text(encoding="utf-8"))
        ports = d.get("ports") or {}
        for p in PORTS:
            x = ports.get(p) or {}
            if not str(x.get("module", "")).strip() or not str(x.get("function", "")).strip() or not isinstance(x.get("reads"), list):
                fail("port %s %r" % (p, x))
            for r in x["reads"]:
                if not all(str(r.get(k, "")).strip() for k in ("service", "resource", "action")):
                    fail("port %s read %r" % (p, r))
        staged = d.get("release6_staged") or []
        if not staged or not all((root / s).is_file() for s in staged):
            fail("release6_staged %r" % staged)
        print("OK: 3 ports named; reads %s; staged %d" % ({p: len(ports[p]["reads"]) for p in PORTS}, len(staged)))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
