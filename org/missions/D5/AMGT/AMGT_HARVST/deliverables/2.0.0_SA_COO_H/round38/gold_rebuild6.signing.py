"""HARVST served gold rebuild #6: the serializing dry run that the NEW never-widen pair signs (issuer, NO WRITE).

Scope: the ft QUARANTINE ALONE (CTO msg 28715 ruling 3; 28731; cell HVST-ak-4). The served event rebuild, and any tone
or window serving, are HELD on Andrew's card (CARD_HARVST_PUBLISHER_TERMS_20261002.md @8d20bc24c8).

The gold builders' own code (with ak-4's quarantine merged) runs through the issuer's capturing client
(round32/checks/ae-1.signing.py CapturingClient; PUTS SENT 0). The result is diffed against the served snapshots.

THE RULE (rebuild #6):
- mention:
  - every served ft row is GONE;
  - 0 non-ft served rows are GONE;
  - 0 non-ft rows CHANGED on the pre-existing field set (the 3 tone fields alone never count);
  - 0 ft rows are built;
  - every built row carries the 3 tone fields, and every value is NULL (FWD-16 is held: no score was run);
  - ADDED rows are counted and named by publisher. They are new non-ft collection since rebuild #5, under the standing
    collection, and the CTO half decides whether #6 carries them.
- daily: 0 rows GONE. Every CHANGED row is EXPLAINED by exactly one class:
  - (q) QUARANTINE. publishers_enabled moves 5 -> len(GRADED_PUBLISHERS). ft leaves publishers_covered_codes and
    publishers_found_codes, and no other code leaves. publishers_covered equals len(publishers_covered_codes). Any
    other changed field is a count or status field of a security that had served ft rows, or (status only) the
    re-grading under the new denominator.
  - (a) the security gained an added mention (as rebuild #5).
  - (b) COVERAGE-ONLY on the as-of day (rebuild #5's four bounds, read after the quarantine).
  OTHER must be 0. data_status transitions are counted and printed for the signer.

Writes `round38/gold_rebuild6_signing.json`. Prints `RULE (rebuild #6): HOLDS` only when all of it holds.
"""
import collections
import datetime
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R32C = os.path.join(os.path.dirname(HERE), "round32", "checks")
sys.path.insert(0, R32C)
import ae1_common as c  # noqa: E402,F401  (puts the repo root on sys.path, as the round-32 dry run does)

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

TONE = ("sentiment_finbert_label", "sentiment_finbert_score", "sentiment_scorer")
QFIELDS = {"publishers_enabled", "publishers_covered", "publishers_covered_codes", "publishers_found_codes"}
OUT = os.path.join(HERE, "gold_rebuild6_signing.json")
STATUS_RANK = {"DENIED": 0, "PARTIAL": 1, "COMPLETE": 2}


def dumps(r):
    return json.dumps(r, sort_keys=True, default=str)


def changed_fields(a, b):
    return {f for f in set(a) | set(b) if json.dumps(a.get(f), default=str) != json.dumps(b.get(f), default=str)}


def pre(r):
    return {k: v for k, v in r.items() if k not in TONE}


def quarantine_bounds(before, after, graded, ft_secs, quarantined):
    diff = changed_fields(before, after)
    bc, ac = set(before.get("publishers_covered_codes") or []), set(after.get("publishers_covered_codes") or [])
    bf, af = set(before.get("publishers_found_codes") or []), set(after.get("publishers_found_codes") or [])
    q1 = after.get("publishers_enabled") == len(graded)
    q2 = ac == bc - quarantined
    q3 = af == bf - quarantined
    q4 = after.get("publishers_covered") == len(ac)
    rest = diff - QFIELDS - {"data_status"}
    q5 = not rest or before.get("security_key") in ft_secs
    return (q1 and q2 and q3 and q4 and q5), {"enabled": q1, "covered_codes": q2, "found_codes": q3,
                                             "covered_len": q4, "rest_on_ft_security": q5, "rest": sorted(rest)}


def main():
    q = getattr(pg, "QUARANTINED_PUBLISHERS", None)
    if not q or "ft" not in q:
        print("QUARANTINED_PUBLISHERS absent -- ak-4 is not merged; this dry run cannot sign anything")
        print("RULE (rebuild #6): BROKEN")
        return 1
    quarantined = set(q)
    graded = list(pg.GRADED_PUBLISHERS)
    securities = json.load(open(os.environ.get("HVST_GOLD_UNIVERSE") or sg.UNIVERSE, encoding="utf-8"))
    print("UNIVERSE FILE: %s (%d securities); quarantined %s; graded %s" % (
        os.environ.get("HVST_GOLD_UNIVERSE") or sg.UNIVERSE, len(securities), sorted(quarantined), graded))
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

    is_q = lambda r: pg.is_quarantined(r)  # noqa: E731
    mk = lambda r: (r.get("article_key"), r.get("security_key"))  # noqa: E731
    served_ft = [r for r in served_m if is_q(r)]
    ft_secs = {r.get("security_key") for r in served_ft}
    om = {mk(r): dumps(pre(r)) for r in served_m if not is_q(r)}
    nm = {mk(r): dumps(pre(r)) for r in mention}
    ft_gone = sum(1 for r in served_ft if mk(r) not in nm)
    m_gone_nonft = [k for k in om if k not in nm]
    m_changed = [k for k in nm if k in om and nm[k] != om[k]]
    m_added = [k for k in nm if k not in om]
    built_ft = sum(1 for r in mention if is_q(r))
    tone_missing = sum(1 for r in mention if any(f not in r for f in TONE))
    tone_valued = sum(1 for r in mention if any(r.get(f) is not None for f in TONE))
    added_by_pub = collections.Counter(r.get("publisher") for r in mention if mk(r) in set(m_added))
    added_secs = {k[1] for k in m_added}

    dk = lambda r: (r.get("security_key"), str(r.get("day"))[:10])  # noqa: E731
    od, nd = {dk(r): r for r in served_d}, {dk(r): r for r in daily}
    d_gone = [k for k in od if k not in nd]
    d_added = [k for k in nd if k not in od]
    d_changed = [k for k in nd if k in od and dumps(nd[k]) != dumps(od[k])]
    cls = collections.Counter()
    other, other_bounds, transitions = [], {}, collections.Counter()
    for k in d_changed:
        b, a = od[k], nd[k]
        if b.get("data_status") != a.get("data_status"):
            transitions["%s->%s" % (b.get("data_status"), a.get("data_status"))] += 1
        ok_q, qb = quarantine_bounds(b, a, graded, ft_secs, quarantined)
        if ok_q:
            cls["q"] += 1
        elif k[0] in added_secs:
            cls["a"] += 1
        elif str(a.get("day"))[:10] == str(as_of) and changed_fields(b, a) - QFIELDS <= {"data_status"}:
            cls["b"] += 1
        else:
            other.append(k)
            if len(other_bounds) < 20:
                other_bounds["|".join(k)] = qb
    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "quarantined": sorted(quarantined), "graded": graded,
           "mention": {"served": len(served_m), "served_ft": len(served_ft), "ft_gone": ft_gone,
                       "built": len(mention), "built_ft": built_ft, "gone_non_ft": len(m_gone_nonft),
                       "changed_pre_existing": len(m_changed), "added": len(m_added),
                       "added_by_publisher": dict(added_by_pub), "tone_missing": tone_missing,
                       "tone_valued": tone_valued, "key": mkey, "bytes": len(mbody)},
           "daily": {"served": len(served_d), "built": len(daily), "gone": len(d_gone), "added": len(d_added),
                     "changed": len(d_changed), "classes": dict(cls), "other": len(other),
                     "other_sample": [list(k) for k in other[:20]], "other_bounds": other_bounds,
                     "status_transitions": dict(transitions), "key": dkey, "bytes": len(dbody)},
           "securities_with_served_ft": len(ft_secs), "puts_sent": cm.sent + cd.sent}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    m, d = out["mention"], out["daily"]
    print("MENTION: served %d (ft %d) -> built %d (ft %d); ft gone %d; non-ft gone %d; changed (pre-existing) %d;"
          " added %d %s" % (m["served"], m["served_ft"], m["built"], m["built_ft"], m["ft_gone"], m["gone_non_ft"],
                            m["changed_pre_existing"], m["added"], m["added_by_publisher"]))
    print("TONE: rows missing a tone field %d; rows with a tone VALUE %d (must be 0: FWD-16 held)" % (
        m["tone_missing"], m["tone_valued"]))
    print("DAILY: served %d -> built %d; gone %d, added %d, changed %d; classes %s; OTHER %d; status transitions %s" % (
        d["served"], d["built"], d["gone"], d["added"], d["changed"], d["classes"], d["other"], d["status_transitions"]))
    for k, b in other_bounds.items():
        print("  OTHER %s %s" % (k, b))
    holds = (m["ft_gone"] == m["served_ft"] and not m["built_ft"] and not m["gone_non_ft"] and not m["changed_pre_existing"]
             and not m["tone_missing"] and not m["tone_valued"] and not d["gone"] and not d["other"]
             and out["puts_sent"] == 0)
    print("RULE (rebuild #6): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % out["puts_sent"])
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
