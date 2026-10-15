"""AR345-y-AC1 checker (0.9.0_WK_IRPT_ANLREQ~149): the driver and the mint helper compile, and the driver self-test passes.

Runs: node --check fwd1_driver.mjs; python -m py_compile fwd1_mint.py; node fwd1_driver.mjs --selftest.
Prints DRIVER-OK <n> selftest cases only when all three succeed and the self-test printed SELFTEST-OK <n> cases with n >= 12;
otherwise DRIVER-BAD <why> and exit 1. Offline: no browser, no AWS, no boto3 import, no password.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DRV = HERE / "fwd1_driver"


def bad(why):
    print("DRIVER-BAD " + why)
    return 1


def main():
    r = subprocess.run(["node", "--check", "fwd1_driver.mjs"], cwd=str(DRV), capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        return bad("node --check rc=%d" % r.returncode)
    r = subprocess.run([sys.executable, "-m", "py_compile", "fwd1_mint.py"], cwd=str(DRV), capture_output=True, text=True,
                       timeout=120)
    if r.returncode != 0:
        return bad("py_compile rc=%d" % r.returncode)
    r = subprocess.run(["node", "fwd1_driver.mjs", "--selftest"], cwd=str(DRV), capture_output=True, text=True, timeout=300)
    m = re.search(r"^SELFTEST-OK (\d+) cases$", r.stdout, re.M)
    if r.returncode != 0 or m is None:
        return bad("selftest rc=%d, no SELFTEST-OK line" % r.returncode)
    n = int(m.group(1))
    if n < 12:
        return bad("selftest has %d cases, below 12" % n)
    print("DRIVER-OK %d selftest cases" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
