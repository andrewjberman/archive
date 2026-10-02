"""HVST-ak-4 AC3 (issuer, read-only, NO WRITE): the ft quarantine reaches the daily table (CTO msg 28715 ruling 3:
"excluded from gold serving and every downstream use").

Runs the REAL `publication_gold.build_daily` over the first 5 round-33-universe securities that carry ft rows in the
SERVED mention snapshot, through the issuer's capturing client (no put is sent). The served snapshot still carries ft
until rebuild #6, so this proves the builder's own exclusion. PASS requires:
- no captured daily row names ft in `publishers_covered_codes` or in `publishers_found_codes`;
- `publishers_enabled` equals the count of enabled publishers less the quarantined ones, on every row;
- at least 1 row was built, and PUTS SENT is 0.
"""
import datetime
import importlib.util
import io
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
R32 = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round32/checks")
UNIVERSE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round33/securities.universe.r33.json")

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)


def main():
    failures = []
    q = getattr(pg, "QUARANTINED_PUBLISHERS", None)
    if not (isinstance(q, dict) and "ft" in q):
        print("QUARANTINED_PUBLISHERS %r" % (q,))
        print("AC3 RESULT: FAIL (1 failure(s))")
        print("  FAIL: QUARANTINED_PUBLISHERS does not name ft")
        return 1
    universe = json.load(open(UNIVERSE, encoding="utf-8"))
    by_key = {s["security_key"]: s for s in universe}
    ft_keys = []
    for r in pg._latest_gold_snapshot_rows(pg.GOLD_TABLE):
        k = r.get("security_key")
        if r.get("publisher") == "ft" and k in by_key and k not in ft_keys:
            ft_keys.append(k)
        if len(ft_keys) == 5:
            break
    securities = [by_key[k] for k in ft_keys]
    cm = sg.CapturingClient(store._default_client())
    pg.build_daily(securities, datetime.datetime.now(datetime.timezone.utc).date(), client=cm)
    (_k, body), = cm.puts.items()
    rows = pq.read_table(io.BytesIO(body)).to_pylist()
    enabled = [p for p in pg.ENABLED_PUBLISHERS if p not in q] if hasattr(pg, "ENABLED_PUBLISHERS") else None
    names_ft = sum(1 for r in rows if "ft" in (r.get("publishers_covered_codes") or [])
                   or "ft" in (r.get("publishers_found_codes") or []))
    bad_enabled = sum(1 for r in rows if enabled is not None and r.get("publishers_enabled") != len(enabled))
    sent = getattr(cm, "sent", 0)
    print("DAILY rows %d over %s; rows naming ft %d; publishers_enabled expected %s, rows off %d; PUTS SENT %s" % (
        len(rows), ft_keys, names_ft, None if enabled is None else len(enabled), bad_enabled, sent))
    if not rows:
        failures.append("no rows built")
    if names_ft:
        failures.append("%d daily rows name ft as a covering or found publisher" % names_ft)
    if enabled is None:
        failures.append("publication_gold has no ENABLED_PUBLISHERS")
    elif bad_enabled:
        failures.append("%d rows whose publishers_enabled != %d" % (bad_enabled, len(enabled)))
    if sent:
        failures.append("puts sent %s" % sent)
    print("AC3 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
