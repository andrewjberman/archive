"""HARVST served gold rebuild #5 -- the serializing dry run the NEW never-widen pair signs (issuer, NO WRITE).

Track C step 1 (CTO msg 28509; cells aj-7 + aj-8): `title` (VERBATIM) and `published_precision` JOIN every gold mention
row. The gold builders' own code runs through the issuer's capturing client (round32/checks/ae-1.signing.py
CapturingClient; PUTS SENT 0), and the result is diffed against the served snapshot.

THE RULE (rebuild #5):
- mention: 0 served rows GONE; 0 CHANGED on the PRE-EXISTING field set (the two added fields alone never count);
  every built row carries `title` and `published_precision`, the title verbatim against silver (null where silver
  has none) and the precision equal to silver's.
- daily: 0 rows GONE; every CHANGED row is EXPLAINED, either (a) its security gained an added mention (the round-32
  class: rolling sums and counts move), or (b) COVERAGE-ONLY: it is the as-of day and its changed fields are a subset
  of {data_status, publishers_covered, publishers_covered_codes} (a publisher's job covered the security after the
  prior rebuild; measured on 6 rows at 15:1xZ, `round37/gold_rebuild5_other6_diff.json`). OTHER must be 0.

Writes `round37/gold_rebuild5_signing.json`. Prints `RULE (rebuild #5): HOLDS` only when all of it holds.
"""
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

from lib.opal_data_harvest import harvest_grammar as hg  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

ADDED_FIELDS = ("title", "published_precision")
OUT = os.path.join(HERE, "gold_rebuild5_signing.json")


STATUS_RANK = {"DENIED": 0, "PARTIAL": 1, "COMPLETE": 2}


def coverage_bounds(before, after, as_of, gained_mention):
    """CTO half @b69262724d: class (b) COVERAGE-ONLY is IN only when all four bounds hold. Returns (in_b, bounds)."""
    diff = {f for f in set(before) | set(after)
            if json.dumps(before.get(f), default=str) != json.dumps(after.get(f), default=str)}
    b1 = str(after.get("day"))[:10] == str(as_of)
    b2 = bool(diff) and diff <= {"data_status", "publishers_covered", "publishers_covered_codes"}
    b3 = ((after.get("publishers_covered") or 0) >= (before.get("publishers_covered") or 0)
          and set(after.get("publishers_covered_codes") or []) >= set(before.get("publishers_covered_codes") or [])
          and STATUS_RANK.get(after.get("data_status"), -1) >= STATUS_RANK.get(before.get("data_status"), -1))
    b4 = not gained_mention
    bounds = {"as_of_day": b1, "coverage_fields_only": b2, "coverage_grows": b3, "no_mention_gained": b4,
              "changed": sorted(diff), "status": [before.get("data_status"), after.get("data_status")],
              "covered": [before.get("publishers_covered"), after.get("publishers_covered")],
              "codes": [list(before.get("publishers_covered_codes") or []), list(after.get("publishers_covered_codes") or [])]}
    return b1 and b2 and b3 and b4, bounds


def pre(r):
    return {k: v for k, v in r.items() if k not in ADDED_FIELDS}


def dumps(r):
    return json.dumps(r, sort_keys=True, default=str)


def changed_fields(a, b):
    return {f for f in set(a) | set(b) if json.dumps(a.get(f), default=str) != json.dumps(b.get(f), default=str)}


def main():
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
    om, nm = {mk(r): dumps(pre(r)) for r in served_m}, {mk(r): dumps(pre(r)) for r in mention}
    m_gone = [k for k in om if k not in nm]
    m_changed = [k for k in nm if k in om and nm[k] != om[k]]
    m_added = [k for k in nm if k not in om]
    added_secs = {k[1] for k in m_added}

    dk = lambda r: (r.get("security_key"), str(r.get("day"))[:10])  # noqa: E731
    od_rows, nd_rows = {dk(r): r for r in served_d}, {dk(r): r for r in daily}
    d_gone = [k for k in od_rows if k not in nd_rows]
    d_changed = [k for k in nd_rows if k in od_rows and dumps(nd_rows[k]) != dumps(od_rows[k])]
    d_added = [k for k in nd_rows if k not in od_rows]
    by_mention = [k for k in d_changed if k[0] in added_secs]
    coverage_only, cov_bounds, other_bounds = [], {}, {}
    for k in d_changed:
        if k[0] in added_secs:
            continue
        in_b, bounds = coverage_bounds(od_rows[k], nd_rows[k], as_of, False)
        (coverage_only.append(k), cov_bounds.__setitem__("|".join(k), bounds)) if in_b else other_bounds.__setitem__("|".join(k), bounds)
    d_other = [k for k in d_changed if k not in set(by_mention) and k not in set(coverage_only)]

    missing = sum(1 for r in mention if any(f not in r for f in ADDED_FIELDS))
    silver = {}
    for pub in sorted({r.get("publisher") for r in mention if r.get("publisher")}):
        for (k,), s in store.silver_latest(hg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            silver[k] = s
    title_bad = sum(1 for r in mention if r.get("article_key") in silver
                    and r.get("title") != (silver[r["article_key"]].get("title") or None))
    prec_bad = sum(1 for r in mention if r.get("article_key") in silver
                   and r.get("published_precision") != silver[r["article_key"]].get("published_precision"))
    titled = sum(1 for r in mention if r.get("title"))

    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "mention": {"served": len(served_m), "built": len(mention), "gone": len(m_gone),
                       "changed_pre_existing": len(m_changed), "added": len(m_added), "key": mkey, "bytes": len(mbody)},
           "added_fields": {"rows": len(mention), "missing": missing, "title_not_verbatim": title_bad,
                            "precision_mismatch": prec_bad, "titled": titled},
           "daily": {"served": len(served_d), "built": len(daily), "gone": len(d_gone), "changed": len(d_changed),
                     "added": len(d_added), "changed_by_added_mention": len(by_mention),
                     "changed_coverage_only": len(coverage_only), "coverage_only_rows": [list(k) for k in coverage_only],
                     "changed_other": len(d_other), "other_sample": [list(k) for k in d_other[:20]],
                     "coverage_bounds": cov_bounds, "other_bounds": dict(list(other_bounds.items())[:20]),
                     "key": dkey, "bytes": len(dbody)},
           "securities_with_new_mentions": len(added_secs), "puts_sent": cm.sent + cd.sent}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    m, d, a = out["mention"], out["daily"], out["added_fields"]
    print("MENTION: served %d -> built %d; gone %d, changed (pre-existing fields) %d, added %d"
          % (m["served"], m["built"], m["gone"], m["changed_pre_existing"], m["added"]))
    print("FIELDS: %d rows; missing a new field %d; title not verbatim %d; precision mismatch %d; titled %d"
          % (a["rows"], a["missing"], a["title_not_verbatim"], a["precision_mismatch"], a["titled"]))
    print("DAILY: served %d -> built %d; gone %d, added %d, changed %d (by added mention %d, coverage-only %d, OTHER %d)"
          % (d["served"], d["built"], d["gone"], d["added"], d["changed"], d["changed_by_added_mention"],
             d["changed_coverage_only"], d["changed_other"]))
    print("SECURITIES WITH NEW MENTIONS: %d" % out["securities_with_new_mentions"])
    print("CLASSES: (a) by added mention %d; (b) coverage-only %d; OTHER %d" % (len(by_mention), len(coverage_only), len(d_other)))
    for k, b in list(cov_bounds.items()) + list(other_bounds.items())[:20]:
        print("  %s %s bounds as_of=%s fields=%s grows=%s no_mention=%s status=%s covered=%s codes=%s" % (
            "(b)" if k in cov_bounds else "OTHER", k, b["as_of_day"], b["coverage_fields_only"], b["coverage_grows"],
            b["no_mention_gained"], b["status"], b["covered"], b["codes"]))
    holds = (not m_gone and not m_changed and not missing and not title_bad and not prec_bad
             and not d_gone and not d_other and out["puts_sent"] == 0)
    print("RULE (rebuild #5): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % out["puts_sent"])
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
