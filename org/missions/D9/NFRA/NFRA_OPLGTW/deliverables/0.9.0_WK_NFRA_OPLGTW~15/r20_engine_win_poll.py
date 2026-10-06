"""OG-rl-8: OG-fl-1's two branches, measured on the WINDOWS branch of engine.process_rss_bytes (the branch the change is in), live tree vs release tree, each in its OWN process.
usage: python r20_engine_win_poll.py <gateway dir> <label> [<child pid>]
  The parent starts one sleeping child (a fixed 30 MiB), polls it N times with the engine under test, and prints:
    RESULT_VALUES  distinct poll results across N polls (memory-poll results: equal between the two trees means the same quantity is read), the child's pid
    ALLOC          net allocated blocks/KiB across the N polls with gc DISABLED (what the poll leaves behind for the cyclic collector), tracemalloc
Both trees are measured by the caller with the SAME child workload (a fresh child each run: its working set is read, not compared across runs).
"""
import gc
import json
import os
import subprocess
import sys
import time
import tracemalloc

gw, label = sys.argv[1], sys.argv[2]
sys.path.insert(0, gw)
os.environ["MOCK_GRAPH"] = "1"
from app.integrations.schwab import engine  # noqa: E402

p = subprocess.Popen([sys.executable, "-c", "import time; x = bytearray(30 * 1024 * 1024); time.sleep(40)"])
time.sleep(1.5)
N = 2000
engine.process_rss_bytes(p.pid)   # warm: the release builds its cached objects here, the live code builds and drops its own
gc.collect()
gc.disable()
tracemalloc.start()
s0 = tracemalloc.take_snapshot()
objs0 = len(gc.get_objects())
vals = [engine.process_rss_bytes(p.pid) for _ in range(N)]
objs1 = len(gc.get_objects())
s1 = tracemalloc.take_snapshot()
tracemalloc.stop()
stats = s1.compare_to(s0, "filename")
net_kib = sum(st.size_diff for st in stats) / 1024.0
net_blocks = sum(st.count_diff for st in stats)
alive = engine.pid_alive(p.pid)
p.kill()
p.wait()
d = {"label": label, "polls": N, "distinct_results": len(set(vals)), "all_positive_int": all(isinstance(v, int) and v > 0 for v in vals),
     "result_mib": round(vals[0] / 1048576.0, 1), "gc_objects_left_by_polls": objs1 - objs0, "tracemalloc_net_blocks": net_blocks, "tracemalloc_net_kib": round(net_kib, 1),
     "pid_alive_true_for_live_child": alive, "has_cached_helpers": hasattr(engine, "_kernel32")}
print("WIN_POLL " + json.dumps(d))
