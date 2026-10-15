"""HVST-cb-2 R5 support: sample the visible/minimised Chrome windows not in the baseline every 3 s. Read only.
Usage: python cb2_windows_sample.py <baseline.json> <samples>
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time

PROBE = r"org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_W1/round87/cb5_window_probe.py"

spec = importlib.util.spec_from_file_location("cb5_window_probe", PROBE)
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)
before = set(json.load(open(sys.argv[1])))
for _ in range(int(sys.argv[2])):
    wins = [(h, ic) for h, ic in probe.chrome_windows() if h not in before]
    procs = subprocess.run(
        ["powershell", "-NoProfile", "-Command", "@(Get-Process chrome -ErrorAction SilentlyContinue).Count"],
        capture_output=True, text=True).stdout.strip()
    print("%s new_windows=%d minimised=%d not_minimised=%d chrome_procs=%s" % (
        time.strftime("%H:%M:%SZ", time.gmtime()), len(wins), sum(1 for _, ic in wins if ic),
        sum(1 for _, ic in wins if not ic), procs), flush=True)
    time.sleep(3)
