#!/usr/bin/env python
"""OG-ap-38: THE HARD GUARD for every host run that executes gateway code (the order's top rule, after the 2026-10-17 17:21Z host OOM, row Z-S375).
A child of the SSM agent inherits oom_score_adj -900, so a runaway read makes the kernel kill the SERVICE and the daemons first. This wrapper, run ON THE HOST under
/opt/opal-gateway/.venv/bin/python, sets the three limits and then runs the named script as __main__:
  oom_score_adj 1000        (the kernel kills THIS process first)
  RLIMIT_AS 1400 MB         (a runaway allocation raises MemoryError here instead of killing anything)
  wall limit <seconds>      (SIGALRM; the process ends itself with AP38_GUARD_WALL)
usage on the host: python ap38_guard.py [--cgroup] <wall_seconds> <script.py> [args ...]
Two named guards (order OG-ap-38, amendment A1): oom_score_adj_1000_rlimit_as_1400mb (this wrapper's default) and oom_score_adj_1000_cgroup_memmax_1400mb (--cgroup: NO address-space cap,
because pyarrow cannot start its worker pools under RLIMIT_AS; the memory ceiling is then the transient scope the CALLER wraps this in: systemd-run --scope -p MemoryMax=1400M ...).
Prints AP38_GUARD_MEMORYERROR (rc 4) or AP38_GUARD_WALL (rc 5) when it stops a run."""
from __future__ import annotations

import os
import runpy
import signal
import sys
import traceback

GUARD = "oom_score_adj_1000_rlimit_as_1400mb"
AS_MB = 1400


def main() -> int:
    import resource                                   # Linux only
    argv = sys.argv[1:]
    cgroup = bool(argv and argv[0] == "--cgroup")
    if cgroup:
        argv = argv[1:]
    wall, script, args = int(argv[0]), argv[1], argv[2:]
    with open("/proc/self/oom_score_adj", "w") as fh:
        fh.write("1000")
    if not cgroup:
        resource.setrlimit(resource.RLIMIT_AS, (AS_MB * 1024 * 1024, AS_MB * 1024 * 1024))

    def on_wall(_sig, _frm):
        print("AP38_GUARD_WALL %ds" % wall, flush=True)
        os._exit(5)
    signal.signal(signal.SIGALRM, on_wall)
    signal.alarm(wall)
    sys.argv = [script] + args
    sys.path.insert(0, os.path.dirname(os.path.abspath(script)))
    try:
        runpy.run_path(script, run_name="__main__")
    except MemoryError:
        print("AP38_GUARD_MEMORYERROR", flush=True)
        traceback.print_exc(limit=-6, file=sys.stdout)
        return 4
    except SystemExit as ex:
        return int(ex.code) if isinstance(ex.code, int) else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
