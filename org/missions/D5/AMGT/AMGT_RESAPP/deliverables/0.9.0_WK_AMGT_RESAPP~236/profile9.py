"""Profile: per-route cold and warm, with boto call counts per (service, operation) and cProfile top by cumulative."""

import sys
import time
import cProfile
import pstats
import io
import collections
import botocore.client

calls = collections.Counter()
caltime = collections.Counter()
_orig = botocore.client.BaseClient._make_api_call


def _wrap(self, op, params):
    t = time.time()
    try:
        return _orig(self, op, params)
    finally:
        k = (self.meta.service_model.service_name, op)
        calls[k] += 1
        caltime[k] += time.time() - t


botocore.client.BaseClient._make_api_call = _wrap
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import capture9  # noqa: E402

which = sys.argv[1:]  # indexes
for i in (int(x) for x in which):
    path, q = capture9.READS[i]
    for phase in ("cold", "warm"):
        calls.clear()
        caltime.clear()
        pr = cProfile.Profile()
        t = time.time()
        pr.enable()
        capture9.get(path, q)
        pr.disable()
        el = time.time() - t
        print(f"== {capture9.name(path, q)} {phase} {el * 1000:.0f} ms")
        for k, n in sorted(calls.items(), key=lambda kv: -caltime[kv[0]]):
            print(f"   boto {k[0]}.{k[1]}: {n} calls {caltime[k] * 1000:.0f} ms")
        s = io.StringIO()
        pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats(14)
        print("\n".join(ln for ln in s.getvalue().splitlines() if ln.strip())[:3500])
