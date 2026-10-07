"""HARVST served gold rebuild #8 (round 57) -- the signing dry run the never-widen pair reads (issuer, NO WRITE).

Asked by 1.0.0_SA_CTO~Z msg 30924. The served gold was built from `round33/securities.universe.r33.json` (212 names, every
rebuild through #7). The proposed list is `universe_securities.build()` as merged (HVST-bc-1 @0b35eeba2a, HVST-bd-1
@088d226de5): the pool's securities with legal names from the collector's identity record, `Meta` as a gold brand and `Lilly`
anchored. This script builds mention and daily with that list through the capturing client (PUTS SENT 0) and prints, AGAINST
THE SERVED SNAPSHOT:
- the list diff: securities new, securities absent, and every common security whose alias set differs;
- mention pairs gained and LOST per security, both directions;
- pre-existing mention rows changed, by field;
- daily rows gone, added, changed.
It states no rule and prints no verdict: a loss is read and explained by a seat, or it stops the rebuild.

Writes `securities.universe.r57.json`, `securities.universe.r57.summary.json` and `gold_rebuild8.signing.json` beside itself.
"""
import collections
import datetime
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)
R32C = os.path.join(PARENT, "round32", "checks")
sys.path.insert(0, R32C)
import ae1_common as c  # noqa: E402,F401  (puts the repo root on sys.path, as the round-32 dry run does)

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.research.harvest import universe_securities as us  # noqa: E402

R33 = os.path.join(PARENT, "round33", "securities.universe.r33.json")
OUT = os.path.join(HERE, "gold_rebuild8.signing.json")
ALIAS_FIELDS = ("company", "aliases", "ticker_aliases", "anchored_aliases", "ticker")


def dumps(row):
    return json.dumps(row, sort_keys=True, default=str)


def changed_fields(a, b):
    return {f for f in set(a) | set(b) if json.dumps(a.get(f), default=str) != json.dumps(b.get(f), default=str)}


def main():
    served_list = json.load(open(R33, encoding="utf-8"))
    new_list, summary = us.build()
    json.dump(new_list, open(os.path.join(HERE, "securities.universe.r57.json"), "w", encoding="utf-8"), indent=1)
    json.dump(summary, open(os.path.join(HERE, "securities.universe.r57.summary.json"), "w", encoding="utf-8"),
              indent=1, default=str)
    old = {s["security_key"]: s for s in served_list}
    new = {s["security_key"]: s for s in new_list}
    added_keys = sorted(set(new) - set(old))
    absent_keys = sorted(set(old) - set(new))
    differ = []
    for key in sorted(set(old) & set(new)):
        diff = [f for f in ALIAS_FIELDS if json.dumps(old[key].get(f)) != json.dumps(new[key].get(f))]
        if diff:
            differ.append((key, diff))
    print("LIST: served file %d securities (%s); proposed %d (universe_securities.build(), source %s)"
          % (len(old), os.path.relpath(R33, c.ROOT).replace(os.sep, "/"), len(new), (summary.get("universe") or {}).get("source")))
    print("LIST NEW (%d): %s" % (len(added_keys), ", ".join("%s [%s]" % (k, new[k].get("company")) for k in added_keys)))
    print("LIST ABSENT FROM THE PROPOSED (%d): %s"
          % (len(absent_keys), ", ".join("%s [%s]" % (k, old[k].get("company")) for k in absent_keys)))
    print("LIST COMMON %d; alias set or name differs on %d" % (len(set(old) & set(new)), len(differ)))
    for key, diff in differ:
        print("  DIFF %s: %s" % (key, "; ".join(
            "%s %s -> %s" % (f, json.dumps(old[key].get(f)), json.dumps(new[key].get(f))) for f in diff)))
    sys.stdout.flush()

    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    served_m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    served_d = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)
    cm = sg.CapturingClient(real)
    pg.build_mention(new_list, as_of, client=cm)
    (mkey, mbody), = cm.puts.items()
    mention = pq.read_table(io.BytesIO(mbody)).to_pylist()
    orig = pg._latest_gold_snapshot_rows
    pg._latest_gold_snapshot_rows = lambda table, client=None: mention if table == pg.GOLD_TABLE else orig(table, client=client)
    cd = sg.CapturingClient(real)
    pg.build_daily(new_list, as_of, client=cd)
    (dkey, dbody), = cd.puts.items()
    daily = pq.read_table(io.BytesIO(dbody)).to_pylist()
    pg._latest_gold_snapshot_rows = orig

    def mk(row):
        return (row.get("article_key"), row.get("security_key"))

    om = {mk(r): r for r in served_m}
    nm = {mk(r): r for r in mention}
    gone = [k for k in om if k not in nm]
    added = [k for k in nm if k not in om]
    changed = [k for k in nm if k in om and dumps(nm[k]) != dumps(om[k])]
    field_counter = collections.Counter(f for k in changed for f in changed_fields(om[k], nm[k]))
    served_by_sec = collections.Counter(k[1] for k in om)
    built_by_sec = collections.Counter(k[1] for k in nm)
    gained_by_sec = collections.Counter(k[1] for k in added)
    lost_by_sec = collections.Counter(k[1] for k in gone)
    print("MENTION: served %d -> built %d; gone %d, added %d, changed %d" % (len(om), len(nm), len(gone), len(added), len(changed)))
    print("MENTION CHANGED FIELDS: %s" % dict(field_counter.most_common()))
    print("MENTION LOST: %d pairs over %d securities" % (len(gone), len(lost_by_sec)))
    for key, n in lost_by_sec.most_common():
        where = "ABSENT FROM THE PROPOSED LIST" if key not in new else "in both lists"
        print("  LOST %s: %d of %d served pairs (%s); aliases served %s -> proposed %s" % (
            key, n, served_by_sec[key], where, json.dumps((old.get(key) or {}).get("aliases")),
            json.dumps((new.get(key) or {}).get("aliases"))))
    print("MENTION GAINED: %d pairs over %d securities" % (len(added), len(gained_by_sec)))
    for key, n in gained_by_sec.most_common():
        tag = "NEW IN LIST" if key not in old else ("alias set differs" if any(k == key for k, _d in differ) else "same alias set")
        print("  GAINED %s: +%d (served %d -> built %d) [%s]" % (key, n, served_by_sec[key], built_by_sec[key], tag))
    same_set_gain = sum(n for key, n in gained_by_sec.items() if key in old and not any(k == key for k, _d in differ))
    print("GAINED ON AN UNCHANGED ALIAS SET (silver grown since the served build): %d pairs" % same_set_gain)

    def dk(row):
        return (row.get("security_key"), str(row.get("day"))[:10])

    od = {dk(r): r for r in served_d}
    nd = {dk(r): r for r in daily}
    d_gone = [k for k in od if k not in nd]
    d_added = [k for k in nd if k not in od]
    d_changed = [k for k in nd if k in od and dumps(nd[k]) != dumps(od[k])]
    moved_secs = set(gained_by_sec) | set(lost_by_sec)
    d_other = [k for k in d_changed if k[0] not in moved_secs]
    d_gone_by_sec = collections.Counter(k[0] for k in d_gone)
    print("DAILY: served %d -> built %d; gone %d, added %d, changed %d (on a security whose mentions moved %d, OTHER %d)"
          % (len(od), len(nd), len(d_gone), len(d_added), len(d_changed), len(d_changed) - len(d_other), len(d_other)))
    print("DAILY GONE BY SECURITY: %s" % dict(d_gone_by_sec.most_common()))
    print("DAILY OTHER FIELDS: %s" % dict(collections.Counter(
        f for k in d_other for f in changed_fields(od[k], nd[k])).most_common()))
    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "list": {"served": len(old), "proposed": len(new), "new": added_keys, "absent": absent_keys,
                    "differ": {k: d for k, d in differ}},
           "mention": {"served": len(om), "built": len(nm), "gone": len(gone), "added": len(added), "changed": len(changed),
                       "changed_fields": dict(field_counter), "lost_by_security": dict(lost_by_sec),
                       "gained_by_security": dict(gained_by_sec), "gone_keys": [list(k) for k in gone],
                       "key": mkey, "bytes": len(mbody)},
           "daily": {"served": len(od), "built": len(nd), "gone": len(d_gone), "added": len(d_added),
                     "changed": len(d_changed), "other": len(d_other), "gone_by_security": dict(d_gone_by_sec),
                     "key": dkey, "bytes": len(dbody)},
           "puts_sent": cm.sent + cd.sent}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("PUTS SENT: %d" % out["puts_sent"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
