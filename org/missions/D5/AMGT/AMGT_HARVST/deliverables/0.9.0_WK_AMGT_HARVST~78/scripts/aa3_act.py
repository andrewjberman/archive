"""HVST-aa-3 act (0.9.0_WK_AMGT_HARVST~78): ONE silver_append of the issuer's rebuilt bbg rows. No retry, no other writer."""
import datetime
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round28/checks"))

import aa3_common  # noqa: E402
from lib.research.harvest import store  # noqa: E402

cl = aa3_common.client()
rebuilt = aa3_common.rebuilt_rows(cl)
rows = [row for _key, row in rebuilt]
latest, _hashes = aa3_common.latest_hashes(cl)
exp = aa3_common.expected_write(rebuilt, latest)
kinds = {}
for e in exp:
    kinds[e[0]] = kinds.get(e[0], 0) + 1
print("rebuilt rows: %d; EXPECTED WRITE: %d rows -- %s" % (len(rows), len(exp), kinds), flush=True)
if kinds != {"NEW": 11}:
    print("STOP: expected write is not exactly 11 NEW; no put made")
    sys.exit(2)

run_stamp = store.stamp(datetime.datetime.now(datetime.timezone.utc))
print("run_stamp:", run_stamp, flush=True)
receipt = store.silver_append("bloomberg", "article", rows, ("article_key",), run_stamp)
print("RECEIPT:", receipt, flush=True)
