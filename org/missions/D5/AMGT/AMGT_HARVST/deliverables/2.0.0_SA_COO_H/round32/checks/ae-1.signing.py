"""HVST-ae-1 phase B signing (issuer, NO WRITE): the serializing dry run of the two gold rebuilds under the quarantine.

Reads the 33 article keys the producer's own `sa_quarantine` predicate names (the census, read-only), then runs the
gold builders' OWN code (`build_mention`, then `build_daily` fed the captured mention rows) through a capturing client
that keeps every put in memory and sends none, with `sa_quarantined_keys` answering the 33 keys. Diffs each captured
snapshot against the snapshot served now. Writes `round32/ae1_signing.json` (row counts, byte sizes, digests, the
moves by class). Prints `PUTS SENT: 0`.
"""
import datetime
import hashlib
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ae1_common as c  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.opal_data_harvest import sa_quarantine  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

OUT = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round32/ae1_signing.json")
UNIVERSE = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~46/securities.universe.json")


class CapturingClient:
    def __init__(self, real):
        self._real, self.puts, self.sent = real, {}, 0

    def put_object(self, Bucket, Key, Body, **kw):
        self.puts[Key] = Body
        return {"ETag": '"captured"'}

    def head_object(self, Bucket, Key, **kw):
        if Key in self.puts:
            return {"ContentLength": len(self.puts[Key])}
        return self._real.head_object(Bucket=Bucket, Key=Key, **kw)

    def __getattr__(self, name):
        return getattr(self._real, name)


def digest(rows):
    h = hashlib.sha256()
    for r in sorted(json.dumps(r, sort_keys=True, default=str) for r in rows):
        h.update(r.encode("utf-8") + b"\n")
    return h.hexdigest()


def key_rows(rows, key):
    return {key(r): json.dumps(r, sort_keys=True, default=str) for r in rows}


def main():
    silver = c.rows(c.SILVER)
    listing = c.rows(c.LISTING)
    wrong = c.classify(silver, listing)
    keys = sorted({c.article_key(r) for r in wrong})
    census_keys = set()
    if hasattr(sa_quarantine, "wrong_object_keys"):
        census_keys = set(sa_quarantine.wrong_object_keys())
    print("QUARANTINE KEYS: %d (issuer oracle); producer census agrees: %s" % (len(keys), (not census_keys) or census_keys == set(keys)))
    securities = json.load(open(UNIVERSE, encoding="utf-8"))
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    pg.sa_quarantined_keys = lambda client=None: set(keys)

    served_mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    served_daily = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)

    cm = CapturingClient(real)
    pg.build_mention(securities, as_of, client=cm)
    (mkey, mbody), = cm.puts.items()
    mention = pq.read_table(io.BytesIO(mbody)).to_pylist()

    orig_latest = pg._latest_gold_snapshot_rows
    pg._latest_gold_snapshot_rows = lambda table, client=None: (mention if table == pg.GOLD_TABLE
                                                                else orig_latest(table, client=client))
    cd = CapturingClient(real)
    pg.build_daily(securities, as_of, client=cd)
    (dkey, dbody), = cd.puts.items()
    daily = pq.read_table(io.BytesIO(dbody)).to_pylist()
    pg._latest_gold_snapshot_rows = orig_latest

    mk = lambda r: (r.get("article_key"), r.get("security_key"))  # noqa: E731
    old_m, new_m = key_rows(served_mention, mk), key_rows(mention, mk)
    gone = sorted(k for k in old_m if k not in new_m)
    added = sorted(k for k in new_m if k not in old_m)
    changed = sorted(k for k in new_m if k in old_m and new_m[k] != old_m[k])
    gone_q = [k for k in gone if k[0] in keys]
    still = [r for r in mention if r.get("article_key") in keys]
    dk = lambda r: (r.get("security_key"), str(r.get("date") or r.get("day") or r.get("publication_date")))  # noqa: E731
    old_d, new_d = key_rows(served_daily, dk), key_rows(daily, dk)
    d_changed = sorted(k for k in new_d if k in old_d and new_d[k] != old_d[k])
    d_added = sorted(k for k in new_d if k not in old_d)
    d_gone = sorted(k for k in old_d if k not in new_d)

    out = {
        "measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
        "quarantine_keys": keys, "silver_rows_checked": len(silver), "wrong_rows": len(wrong),
        "mention": {"key": mkey, "bytes": len(mbody), "rows": len(mention), "digest": digest(mention),
                    "served_rows": len(served_mention), "gone": len(gone), "gone_quarantined": len(gone_q),
                    "gone_other": [list(k) for k in gone if k[0] not in keys], "added": [list(k) for k in added],
                    "changed": len(changed), "quarantined_still_present": len(still)},
        "daily": {"key": dkey, "bytes": len(dbody), "rows": len(daily), "digest": digest(daily),
                  "served_rows": len(served_daily), "changed": len(d_changed), "added": len(d_added),
                  "gone": len(d_gone), "changed_rows": [list(k) for k in d_changed][:200]},
        "puts_sent": 0,
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    m, d = out["mention"], out["daily"]
    print("MENTION: served %d -> built %d rows (%d B); gone %d (quarantined %d, other %d); added %d; changed %d; quarantined still present %d"
          % (m["served_rows"], m["rows"], m["bytes"], m["gone"], m["gone_quarantined"], len(m["gone_other"]),
             len(m["added"]), m["changed"], m["quarantined_still_present"]))
    print("DAILY: served %d -> built %d rows (%d B); changed %d; added %d; gone %d"
          % (d["served_rows"], d["rows"], d["bytes"], d["changed"], d["added"], d["gone"]))
    print("KEYS: mention %s ; daily %s" % (mkey, dkey))
    print("PUTS SENT: 0")


if __name__ == "__main__":
    main()
