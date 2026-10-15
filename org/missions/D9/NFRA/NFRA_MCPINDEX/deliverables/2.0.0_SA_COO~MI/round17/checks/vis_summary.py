"""vis_summary.py <gateway root> -- runs vis_matrix.py against <gateway root> in a subprocess and prints ONE summary line:
the row count, the number of rows each principal sees, the count of rows carrying a firm field, and the sha256 of the whole matrix JSON.
Used locally and on the gateway host (via SSM) so the two summaries can be compared byte for byte."""
import hashlib
import json
import os
import subprocess
import sys

root = os.path.abspath(sys.argv[1])
vm = os.environ.get("VIS_MATRIX") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "vis_matrix.py")
env = dict(os.environ, MOCK_GRAPH="1")
r = subprocess.run([sys.executable, vm, root], capture_output=True, text=True, env=env, timeout=240)
lines = [ln for ln in (r.stdout or "").splitlines() if ln.startswith("{")]
if r.returncode != 0 or not lines:
    print("VIS ERROR rc=%d %s" % (r.returncode, (r.stderr or r.stdout)[-300:].replace("\n", " ")))
    sys.exit(1)
m = json.loads(lines[-1])
seen = dict((k, len(v)) for k, v in m.items() if isinstance(v, list))
print("VIS rows=%d firm_field=%d seen=%s errors=%d sha256=%s" % (m["rows"], len(m["firm_field"]), json.dumps(seen, sort_keys=True), len(m.get("errors", [])),
                                                              hashlib.sha256(lines[-1].encode("utf-8")).hexdigest()))
