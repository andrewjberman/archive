"""HVST-ae-4 AC2 (issuer, LOCAL): the backfill driver's dry run over the REAL collector universe makes no request.

Runs `python -m lib.opal_data_harvest.backfill_driver --dry-run --checkpoint <temp>` with every socket to a non-local host
refused (and counted) in the child, then grades its printed plan.

PASS requires, in the driver's own output:
- `UNIVERSE: 89` (the collector's resolved universe, measured at the cut);
- one `BUDGET <publisher>:` line per publisher, ALL printed before the first `PLAN` line;
- the first `PLAN` line is a sa job;
- `NETWORK CALLS: 0`, and the child's refused-socket counter reads 0.
"""
import os
import re
import subprocess
import sys
import tempfile

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()

GUARD = r'''
import socket, sys, runpy
REFUSED = [0]
_orig = socket.socket.connect
def _connect(self, addr):
    host = addr[0] if isinstance(addr, tuple) else str(addr)
    if host not in ("127.0.0.1", "localhost", "::1"):
        REFUSED[0] += 1
        raise OSError("ae-4 AC2 guard: non-local connect refused to %s" % host)
    return _orig(self, addr)
socket.socket.connect = _connect
sys.argv = ["backfill_driver"] + sys.argv[1:]
try:
    runpy.run_module("lib.opal_data_harvest.backfill_driver", run_name="__main__")
finally:
    print("GUARD REFUSED SOCKETS: %d" % REFUSED[0])
'''


def main():
    failures = []
    ck = os.path.join(tempfile.mkdtemp(prefix="hvst-ae4-"), "checkpoint.json")
    p = subprocess.run([sys.executable, "-c", GUARD, "--dry-run", "--checkpoint", ck], cwd=ROOT, capture_output=True,
                       timeout=300)
    out = (p.stdout + p.stderr).decode("utf-8", errors="replace")
    lines = out.splitlines()
    for ln in lines[:40]:
        print("  | " + ln)
    if len(lines) > 40:
        print("  | ... (%d lines)" % len(lines))
    print("rc=%d" % p.returncode)
    budgets = [i for i, ln in enumerate(lines) if ln.startswith("BUDGET ")]
    plans = [i for i, ln in enumerate(lines) if ln.startswith("PLAN ")]
    universe = [ln for ln in lines if ln.startswith("UNIVERSE:")]
    refused = re.findall(r"GUARD REFUSED SOCKETS: (\d+)", out)
    if p.returncode != 0:
        failures.append("driver dry run rc=%d" % p.returncode)
    if not universe or universe[0].split(":", 1)[1].strip() != "89":
        failures.append("UNIVERSE line is %r, expected 89" % (universe[:1],))
    if len(budgets) < 5:
        failures.append("%d BUDGET lines, expected one per publisher (5)" % len(budgets))
    if not plans:
        failures.append("no PLAN line")
    elif budgets and max(budgets) > min(plans):
        failures.append("a BUDGET line follows the first PLAN line")
    if plans and " sa " not in (" " + lines[plans[0]] + " "):
        failures.append("the first PLAN line is not a sa job: %r" % lines[plans[0]])
    if "NETWORK CALLS: 0" not in out:
        failures.append("no 'NETWORK CALLS: 0' line")
    if not refused or refused[-1] != "0":
        failures.append("the guard refused %s socket(s)" % (refused[-1] if refused else "?"))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
