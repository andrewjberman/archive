"""HVST-cb-2 R5: visible Chrome windows that were not open before the start, and whether each is minimised.

Imports chrome_windows() from the issuer's cb5_window_probe.py BY PATH (its main is never run). Read only.
  baseline <file>              record the hwnds of the Chrome windows open now
  read <file> <label>          two listings 10 s apart; one NOT_MINIMISED=<n> line per listing
  control <file>               print the listing as if no baseline exists (a plain window must read not minimised)
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from pathlib import Path

PROBE = Path("org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_W1/round87/cb5_window_probe.py")


def _load():
    spec = importlib.util.spec_from_file_location("cb5_window_probe", str(PROBE))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _stamp():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def main(argv):
    probe = _load()
    cmd, path = argv[1], Path(argv[2])
    if cmd == "baseline":
        wins = probe.chrome_windows()
        path.write_text(json.dumps(sorted(h for h, _ in wins)), encoding="ascii")
        print("BASELINE %s windows_open_before=%d iconic=%d" % (_stamp(), len(wins), sum(1 for _, m in wins if m)))
        return 0
    before = set(json.loads(path.read_text(encoding="ascii"))) if cmd == "read" else set()
    label = argv[3] if len(argv) > 3 else cmd
    for i in (1, 2):
        wins = [(h, m) for h, m in probe.chrome_windows() if h not in before]
        n = sum(1 for _, m in wins if not m)
        prefix = "CONTROL_" if cmd == "control" else ""
        print("%s %s listing=%d new_windows=%d minimised=%d %sNOT_MINIMISED=%d" % (
            label, _stamp(), i, len(wins), len(wins) - n, prefix, n))
        if i == 1:
            time.sleep(10)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
