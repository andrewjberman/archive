"""HVST-ak-4 AC2 (issuer, read-only, NO WRITE): the ft quarantine removes exactly the ft rows from the gold mention build
(CTO msg 28715 ruling 3; ROUND_ANALYSIS.round37.md addendum 2).

Picks the first 5 round-33-universe securities that carry ft rows in the SERVED mention snapshot. It then runs the REAL
`publication_gold.build_mention` twice through the issuer's capturing client (no put is sent): once as shipped, and
once with `QUARANTINED_PUBLISHERS` emptied (the control). PASS requires:
- `publication_gold.QUARANTINED_PUBLISHERS` names "ft" with a non-empty reason;
- the shipped build has 0 rows whose publisher is ft;
- the control build has more than 0 ft rows, so the control can see what the quarantine removes;
- every non-ft row is identical on every field across the two builds, and the same non-ft keys appear in both;
- PUTS SENT is 0.
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


def build(securities):
    cm = sg.CapturingClient(store._default_client())
    pg.build_mention(securities, datetime.datetime.now(datetime.timezone.utc).date(), client=cm)
    (_k, body), = cm.puts.items()
    return pq.read_table(io.BytesIO(body)).to_pylist(), getattr(cm, "sent", 0)


def done(failures):
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures[:30]:
        print("  FAIL: " + f)
    return 0 if not failures else 1


def main():
    q = getattr(pg, "QUARANTINED_PUBLISHERS", None)
    print("QUARANTINED_PUBLISHERS %r" % (q,))
    if not (isinstance(q, dict) and isinstance(q.get("ft"), str) and q["ft"].strip()):
        return done(["QUARANTINED_PUBLISHERS does not name ft with a reason"])
    universe = json.load(open(UNIVERSE, encoding="utf-8"))
    by_key = {s["security_key"]: s for s in universe}
    served = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    ft_keys = []
    for r in served:
        k = r.get("security_key")
        if r.get("publisher") == "ft" and k in by_key and k not in ft_keys:
            ft_keys.append(k)
        if len(ft_keys) == 5:
            break
    securities = [by_key[k] for k in ft_keys]
    print("SECURITIES with served ft rows: %s" % ft_keys)
    shipped, sent1 = build(securities)
    saved = dict(q)
    try:
        q.clear()
        control, sent2 = build(securities)
    finally:
        q.update(saved)
    def key(r):
        return (r["article_key"], r["security_key"])
    ft_shipped = [r for r in shipped if r.get("publisher") == "ft"]
    ft_control = [r for r in control if r.get("publisher") == "ft"]
    non_ship = {key(r): r for r in shipped if r.get("publisher") != "ft"}
    non_ctrl = {key(r): r for r in control if r.get("publisher") != "ft"}
    differ = sum(1 for k in non_ship if k in non_ctrl and non_ship[k] != non_ctrl[k])
    print("SHIPPED rows %d (ft %d); CONTROL rows %d (ft %d); non-ft keys shipped %d control %d; non-ft rows differing %d;"
          " PUTS SENT %s/%s" % (len(shipped), len(ft_shipped), len(control), len(ft_control), len(non_ship),
                                len(non_ctrl), differ, sent1, sent2))
    failures = []
    if ft_shipped:
        failures.append("%d ft rows in the shipped build" % len(ft_shipped))
    if not ft_control:
        failures.append("the control build has 0 ft rows (the control cannot see the quarantine)")
    if set(non_ship) != set(non_ctrl):
        failures.append("non-ft keys differ: %d only shipped, %d only control" % (
            len(set(non_ship) - set(non_ctrl)), len(set(non_ctrl) - set(non_ship))))
    if differ:
        failures.append("%d non-ft rows differ between the builds" % differ)
    if sent1 or sent2:
        failures.append("puts sent %s/%s" % (sent1, sent2))
    return done(failures)


if __name__ == "__main__":
    sys.exit(main())
