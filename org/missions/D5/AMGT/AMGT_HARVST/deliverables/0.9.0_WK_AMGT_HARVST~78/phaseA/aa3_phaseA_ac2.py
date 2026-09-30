"""AC-A2: rebuild the held bbg bronze objects with the new builder, serialize in memory (no S3 write)."""
import io
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round28/checks"))
import aa3_common  # noqa: E402
import pyarrow as pa  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

cl = aa3_common.client()
rebuilt = aa3_common.rebuilt_rows(cl)
latest, _ = aa3_common.latest_hashes(cl)
new_keys = {e[2] for e in aa3_common.expected_write(rebuilt, latest) if e[0] == "NEW"}
held = [(k, r) for k, r in rebuilt if k in new_keys]
print("rows built:", len(rebuilt), "; held NEW (to write):", len(held))
by_date = {}
for _k, r in held:
    by_date.setdefault(r["fetched_at"].date(), []).append(r)
ok = 0
for d, rs in sorted(by_date.items()):
    try:
        pq.write_table(pa.Table.from_pylist(rs), io.BytesIO())
        ok += len(rs)
        print("GROUP date=%s: serialized %d rows" % (d, len(rs)))
    except Exception as e:
        print("GROUP FAIL", d, type(e).__name__, str(e)[:160])
print("SERIALIZED: %d of %d" % (ok, len(held)))
