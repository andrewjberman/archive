"""IRPT_BCKEND round 101 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of cell IB-pr-396: FWD-14 v0.33 (CTO msg 2738, PRD @13ee60595d) on top of IB-pr-393, the holdings publish gate (PRD v0.31 +
v0.32 @97826891e9; Andrew-direct @f8e7d992dd). In holdings_snapshot.py's publish step, before a firm's index moves, a WORSE candidate is
refused, the firm keeps its last good publication, and one refusal record per firm is written at an address() path; an account the source
records as closed/terminated is LISTED, never refused.

Usage: python <this file> <repo_root> <criterion_id>
Prints "<id> PASS" or "<id> FAIL" as the last line.

  IB101-1-AC1  in the runner tests, `-k publish_gate` passes (>= 9: each of the six WORSE conditions refused with the prior kept; a closed or
              terminated account listed not refused; an equal-or-better candidate re-points; the refusal record written at address() output),
              and the whole runner suite passes (only the pre-existing red S71 guard excused, by exact id). Base: FAIL (no such tests).
  IB101-1-AC2  `-k publish_gate_all_unknown` passes (>= 1): a firm whose directory marks no closures (all UNKNOWN) and that loses an
              account PUBLISHES, and its record lists the lost account. Base: FAIL (no such test).
"""
import re
import subprocess
import sys
from pathlib import Path

RUNNER = "data/assets/scripts/gold/investor_reporting"
KNOWN_RED = {"tests/test_holdings_rearm_trigger.py::test_rearm_trigger_live"}
T = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~261/IB101-1_publish_gate_qa_trace.json"


def pytest(cwd, *args, failed=None):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-rf", *args], cwd=str(cwd),
                       capture_output=True, timeout=280)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (p.stdout + p.stderr).decode("utf-8", "replace"))
    if failed is not None:
        failed.update(m.replace("\\", "/") for m in re.findall(r"^FAILED (\S+?)(?: - |$)", out, re.M))
    last = [ln for ln in out.splitlines() if ln.strip()]
    return p.returncode, (last[-1] if last else "")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB101-1"))
        sys.exit(1)

    if cid == "IB101-1-AC1":
        rc, last = pytest(root / RUNNER, "tests", "-k", "publish_gate")
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < 9:
            fail("-k publish_gate rc %d: %s" % (rc, last))
        red = set()
        rc2, last2 = pytest(root / RUNNER, "tests", failed=red)
        if rc2 != 0 and not (red and red <= KNOWN_RED and re.search(r"\b%d failed" % len(red), last2)):
            fail("runner suite rc %d: %s; failed %s" % (rc2, last2, sorted(red)))
        print("OK: -k publish_gate %s; suite %s; excused %s" % (last, last2, sorted(red)))
    elif cid == "IB101-1-AC2":
        rc, last = pytest(root / RUNNER, "tests", "-k", "publish_gate_all_unknown")
        m = re.search(r"\b(\d+) passed", last)
        if rc != 0 or not m or int(m.group(1)) < 1:
            fail("-k publish_gate_all_unknown rc %d: %s" % (rc, last))
        print("OK: %s" % last)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
