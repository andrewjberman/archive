"""HVST-ae-1 daily attribution (issuer, NO WRITE; the CTO's condition, msg 27574): build `chatter_daily` twice with the
gold builder's own code through a capturing client -- once WITH the 33 quarantined sa keys and once WITHOUT -- and
compare the two captured snapshots. Equal means the quarantine moves no daily row (DELTA=0 holds for daily too); the
8 changed / 191 added rows against the served snapshot are then the as-of advance and the run records, not the
quarantine. Unequal is a STOP (then a pair). Both builds read the same served mention snapshot, minus the quarantine
in the WITH arm (the build_daily filter). Writes `round32/ae1_daily_attribution.json`; prints `PUTS SENT: 0`.
"""
import datetime
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ae1_common as c  # noqa: E402

import importlib.util  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

OUT = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round32/ae1_daily_attribution.json")


def build(keys, securities, as_of, real):
    pg.sa_quarantined_keys = lambda client=None: set(keys)
    cl = sg.CapturingClient(real)
    pg.build_daily(securities, as_of, client=cl)
    (key, body), = cl.puts.items()
    return key, body, pq.read_table(io.BytesIO(body)).to_pylist()


def main():
    keys = sorted({c.article_key(r) for r in c.classify(c.rows(c.SILVER), c.rows(c.LISTING))})
    securities = json.load(open(sg.UNIVERSE, encoding="utf-8"))
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    k_with, b_with, with_rows = build(keys, securities, as_of, real)
    k_without, b_without, without_rows = build([], securities, as_of, real)
    d_with, d_without = sg.digest(with_rows), sg.digest(without_rows)
    equal = d_with == d_without
    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "quarantine_keys": len(keys), "with": {"rows": len(with_rows), "bytes": len(b_with), "digest": d_with},
           "without": {"rows": len(without_rows), "bytes": len(b_without), "digest": d_without},
           "equal": equal, "puts_sent": 0}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1)
    print("DAILY WITH %d keys: %d rows, digest %s" % (len(keys), len(with_rows), d_with))
    print("DAILY WITHOUT:      %d rows, digest %s" % (len(without_rows), d_without))
    print("ATTRIBUTION: %s" % ("EQUAL -- the quarantine moves no daily row" if equal else "UNEQUAL -- STOP, then a pair"))
    print("PUTS SENT: 0")
    return 0 if equal else 1


if __name__ == "__main__":
    sys.exit(main())
