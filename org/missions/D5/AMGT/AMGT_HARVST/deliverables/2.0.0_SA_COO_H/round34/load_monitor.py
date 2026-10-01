"""HVST round 34 (issuer): the input-source monitor over the backfill driver runs -- FWD-11 limb (2) per CTO ruling 27860.

Holds one InputSourceMonitor window open for as long as the driver runs and rewrites a snapshot every 60 s:
`.runtime/harvest-backfill/load_monitor.json` = {instrument, window_start, snapshot_at, hardware_input_events,
injected_input_events, hardware_event_times[<=50]}. Exits (closing the window) when `.runtime/harvest-backfill/STOP_MONITOR`
exists. It reads input flags only, never key codes or coordinates.
"""
import json
import os
import subprocess
import sys
import time

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)

from lib.opal_data_harvest.input_source import InputSourceMonitor  # noqa: E402

OUT = os.path.join(ROOT, ".runtime/harvest-backfill/load_monitor.json")
STOP = os.path.join(ROOT, ".runtime/harvest-backfill/STOP_MONITOR")


class _TimedMonitor(InputSourceMonitor):
    hardware_times = None

    def _count(self, injected):
        super()._count(injected)
        if not injected:
            self.hardware_times = (self.hardware_times or [])[-49:] + [self.now()]


def write(m, final=False):
    rec = dict(m.record()) if final else {"window_start": m.window_start}
    rec.update({"instrument": rec.get("instrument") or "InputSourceMonitor (lib/opal_data_harvest/input_source.py)",
                "snapshot_at": m.now(), "final": final,
                "hardware_input_events": m.hardware_input_events, "injected_input_events": m.injected_input_events,
                "hardware_event_times": m.hardware_times or []})
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, default=str)
    os.replace(tmp, OUT)


def main():
    with _TimedMonitor() as m:
        while not os.path.exists(STOP):
            write(m)
            time.sleep(60)
    write(m, final=True)
    print("OK: window closed %s .. %s hardware %d injected %d" % (m.window_start, m.window_end,
          m.hardware_input_events, m.injected_input_events))
    return 0


if __name__ == "__main__":
    sys.exit(main())
