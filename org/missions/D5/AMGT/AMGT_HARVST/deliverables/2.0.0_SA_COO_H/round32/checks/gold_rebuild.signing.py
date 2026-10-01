"""HARVST served gold rebuild -- the serializing dry run the CTO+COO never-widen halves sign (issuer, NO WRITE).

Runs the gold builders' own code (`build_mention`, then `build_daily` fed the captured mention rows) through a capturing
client: every put is kept in memory and none is sent. Diffs each captured snapshot against the snapshot served now.

The SIGNABLE RULE (the act re-runs this immediately before it writes, and writes only when the rule holds):
- mention: 0 previously served rows gone, 0 changed; only rows ADDED, each for an article in silver;
- daily: 0 rows gone; every changed (security, day) row belongs to a security that gained an added mention (a new
  mention legitimately moves that security's cumulative_ytd and rolling sums on every later day -- measured 2026-10-01:
  the changed field-sets are cumulative_ytd / baseline_30d_sum / trailing_7d_sum / trailing_30d_sum, plus the
  day's own counts where the mention lands); a changed row on any other security is OTHER and must be 0. Added rows are
  the new as-of day.
Prints the counts per class and `PUTS SENT: 0`; writes `round32/gold_rebuild_signing.json`.
"""
import datetime
import importlib.util
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ae1_common as c  # noqa: E402

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                           "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)
OUT = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round32/gold_rebuild_signing.json")


def rows_by(rows, key):
    return {key(r): json.dumps(r, sort_keys=True, default=str) for r in rows}


def main():
    # HVST_GOLD_UNIVERSE: the gold securities file the builders run over (default: ~46's file)
    securities = json.load(open(os.environ.get("HVST_GOLD_UNIVERSE") or sg.UNIVERSE, encoding="utf-8"))
    print("UNIVERSE FILE: %s (%d securities)" % (os.environ.get("HVST_GOLD_UNIVERSE") or sg.UNIVERSE, len(securities)))
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    served_m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    served_d = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)

    cm = sg.CapturingClient(real)
    pg.build_mention(securities, as_of, client=cm)
    (mkey, mbody), = cm.puts.items()
    mention = pq.read_table(io.BytesIO(mbody)).to_pylist()
    orig = pg._latest_gold_snapshot_rows
    pg._latest_gold_snapshot_rows = lambda table, client=None: mention if table == pg.GOLD_TABLE else orig(table, client=client)
    cd = sg.CapturingClient(real)
    pg.build_daily(securities, as_of, client=cd)
    (dkey, dbody), = cd.puts.items()
    daily = pq.read_table(io.BytesIO(dbody)).to_pylist()
    pg._latest_gold_snapshot_rows = orig

    mk = lambda r: (r.get("article_key"), r.get("security_key"))  # noqa: E731
    om, nm = rows_by(served_m, mk), rows_by(mention, mk)
    m_gone = [k for k in om if k not in nm]
    m_changed = [k for k in nm if k in om and nm[k] != om[k]]
    # ADDENDUM 1 (CTO half @e24ca120a2): with a widened universe file, a served row may change ONLY in the co-mention
    # fields and only when what it NEWLY co-mentions is a non-empty subset of the keys the file adds over the base file.
    base_keys = {r["security_key"] for r in json.load(open(sg.UNIVERSE, encoding="utf-8"))}
    added_keys = {r["security_key"] for r in securities} - base_keys
    before_rows = {mk(r): r for r in served_m}
    after_rows = {mk(r): r for r in mention}
    co_fields = {"co_mention_count", "co_mentioned_securities", "is_roundup"}

    def co_mention_only(k):
        a, b = after_rows[k], before_rows[k]
        diff = {f for f in set(a) | set(b) if json.dumps(a.get(f), default=str) != json.dumps(b.get(f), default=str)}
        new_co = set(a.get("co_mentioned_securities") or []) - set(b.get("co_mentioned_securities") or [])
        return diff <= co_fields and bool(new_co) and new_co <= added_keys

    m_co_only = [k for k in m_changed if co_mention_only(k)]
    m_changed = [k for k in m_changed if k not in set(m_co_only)]
    m_added = [k for k in nm if k not in om]
    new_days = {}
    for r in mention:
        if mk(r) in set(m_added):
            new_days.setdefault(r.get("security_key"), set()).add(str(r.get("published_utc"))[:10])

    dk = lambda r: (r.get("security_key"), str(r.get("date") or r.get("day") or r.get("publication_date"))[:10])  # noqa: E731
    od, nd = rows_by(served_d, dk), rows_by(daily, dk)
    d_gone = [k for k in od if k not in nd]
    d_changed = [k for k in nd if k in od and nd[k] != od[k]]
    d_added = [k for k in nd if k not in od]

    def explained(k):
        return k[0] in new_days

    d_other = [k for k in d_changed if not explained(k)]
    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "mention": {"served": len(served_m), "built": len(mention), "gone": len(m_gone), "changed": len(m_changed),
                       "added": len(m_added), "co_mention_only_changes": len(m_co_only), "added_universe_keys": sorted(added_keys),
                       "key": mkey, "bytes": len(mbody)},
           "daily": {"served": len(served_d), "built": len(daily), "gone": len(d_gone), "changed": len(d_changed),
                     "added": len(d_added), "changed_explained": len(d_changed) - len(d_other),
                     "changed_other": len(d_other), "other_sample": [list(k) for k in d_other[:20]],
                     "key": dkey, "bytes": len(dbody)},
           "securities_with_new_mentions": len(new_days), "puts_sent": 0}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    m, d = out["mention"], out["daily"]
    print("MENTION: served %d -> built %d; gone %d, changed %d, added %d; co-mention-only changes %d (added universe keys %d)"
          % (m["served"], m["built"], m["gone"], m["changed"], m["added"], m["co_mention_only_changes"],
             len(m["added_universe_keys"])))
    print("DAILY: served %d -> built %d; gone %d, added %d, changed %d (on securities with new mentions %d, OTHER %d)"
          % (d["served"], d["built"], d["gone"], d["added"], d["changed"], d["changed_explained"], d["changed_other"]))
    print("SECURITIES WITH NEW MENTIONS: %d" % out["securities_with_new_mentions"])
    rule = m["gone"] == 0 and m["changed"] == 0 and d["gone"] == 0 and d["changed_other"] == 0
    print("RULE: %s" % ("HOLDS" if rule else "BROKEN"))
    print("PUTS SENT: 0")
    return 0 if rule else 1


if __name__ == "__main__":
    sys.exit(main())
