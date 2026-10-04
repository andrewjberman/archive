"""HARVST round 41 HVST-an-2 -- the serializing dry run the tone-rebuild never-widen pair signs (issuer, NO WRITE).

Andrew-direct ~20:3xZ card 2 (record ANDREW_DIRECT_20261003_20xxZ_YES_TO_ALL_SEVEN_OPEN_CALL_RECS.md): the FinBERT
scores (HVST-an-1) join every gold mention row (FWD-16). The gold builders' own code runs through the issuer's
capturing client (round32/checks/ae-1.signing.py CapturingClient; PUTS SENT 0) and the result is diffed against the
served snapshot.

THE RULE (tone rebuild):
- mention: 0 served rows GONE; 0 CHANGED on the PRE-EXISTING field set (the 4 `sentiment_*` fields alone never
  count); rows ADDED only from silver collected after the served part; every built row carries the 4 fields; every
  row whose `sentiment_content_key` has a score carries that score's label and signed score (JOIN MISMATCH 0).
- daily: 0 rows GONE; every CHANGED row is EXPLAINED, either (a) its security gained an added mention, or (b)
  COVERAGE-ONLY on the as-of day (the rebuild-#5 bounds). OTHER must be 0.

Writes `round41/gold_tone_signing.json`. Prints `RULE (tone rebuild): HOLDS` only when all of it holds.
"""
import datetime
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DELIV = os.path.dirname(HERE)
os.environ.setdefault("HVST_GOLD_UNIVERSE", os.path.join(DELIV, "round33", "securities.universe.r33.json"))
R32C = os.path.join(DELIV, "round32", "checks")
sys.path.insert(0, R32C)
import ae1_common as c  # noqa: E402,F401  (puts the repo root on sys.path)

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32C, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)
_spec5 = importlib.util.spec_from_file_location("r37_signing", os.path.join(DELIV, "round37", "gold_rebuild5.signing.py"))
s5 = importlib.util.module_from_spec(_spec5)
_spec5.loader.exec_module(s5)

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import finbert_sentiment as fs  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

TONE_FIELDS = ("sentiment_finbert_label", "sentiment_finbert_score", "sentiment_scorer", "sentiment_content_key")
OUT = os.path.join(HERE, "gold_tone_signing.json")


def pre(r):
    return {k: v for k, v in r.items() if k not in TONE_FIELDS}


def dumps(r):
    return json.dumps(r, sort_keys=True, default=str)


def main():
    universe = os.environ["HVST_GOLD_UNIVERSE"]
    securities = json.load(open(universe, encoding="utf-8"))
    print("UNIVERSE FILE: %s (%d securities)" % (universe, len(securities)))
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    served_m = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    served_d = pg._latest_gold_snapshot_rows(pg.GOLD_DAILY_TABLE)
    scores = fs.latest_scores(real)
    cm = sg.CapturingClient(real)
    pg.build_mention(securities, as_of, client=cm, sentiment_by_key=scores)
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
    coverage_only, other = [], []
    for k in d_changed:
        if k[0] in added_secs:
            continue
        in_b, _ = s5.coverage_bounds(od_rows[k], nd_rows[k], as_of, False)
        (coverage_only if in_b else other).append(k)

    missing = sum(1 for r in mention if any(f not in r for f in TONE_FIELDS))
    keyed = [r for r in mention if r.get("sentiment_content_key")]
    scored = [r for r in keyed if r["sentiment_content_key"] in scores]
    mismatch = sum(1 for r in scored
                   if r.get("sentiment_finbert_label") != scores[r["sentiment_content_key"]].get("label")
                   or r.get("sentiment_finbert_score") != scores[r["sentiment_content_key"]].get("score"))
    labels = {}
    for r in mention:
        labels[r.get("sentiment_finbert_label")] = labels.get(r.get("sentiment_finbert_label"), 0) + 1
    by_pub = {}
    for r in mention:
        p = by_pub.setdefault(r.get("publisher"), {"rows": 0, "labelled": 0})
        p["rows"] += 1
        p["labelled"] += 1 if r.get("sentiment_finbert_label") is not None else 0

    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "universe_file": universe, "scores_read": len(scores),
           "mention": {"served": len(served_m), "built": len(mention), "gone": len(m_gone),
                       "changed_pre_existing": len(m_changed), "added": len(m_added), "key": mkey, "bytes": len(mbody)},
           "tone": {"rows": len(mention), "missing_fields": missing, "rows_with_content_key": len(keyed),
                    "rows_whose_key_is_scored": len(scored), "rows_whose_key_is_unscored": len(keyed) - len(scored),
                    "join_mismatch": mismatch, "labels": {str(k): v for k, v in labels.items()},
                    "by_publisher": {str(k): v for k, v in by_pub.items()}},
           "daily": {"served": len(served_d), "built": len(daily), "gone": len(d_gone), "changed": len(d_changed),
                     "added": len(d_added), "changed_by_added_mention": len(by_mention),
                     "changed_coverage_only": len(coverage_only), "changed_other": len(other),
                     "other_sample": [list(k) for k in other[:20]], "key": dkey, "bytes": len(dbody)},
           "securities_with_new_mentions": len(added_secs), "puts_sent": cm.sent + cd.sent}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    m, t, d = out["mention"], out["tone"], out["daily"]
    print("SCORES READ: %d" % out["scores_read"])
    print("MENTION: served %d -> built %d; gone %d, changed (pre-existing fields) %d, added %d"
          % (m["served"], m["built"], m["gone"], m["changed_pre_existing"], m["added"]))
    print("TONE: %d rows; missing a tone field %d; content-keyed %d; scored %d; unscored %d; join mismatch %d; labels %s"
          % (t["rows"], t["missing_fields"], t["rows_with_content_key"], t["rows_whose_key_is_scored"],
             t["rows_whose_key_is_unscored"], t["join_mismatch"], t["labels"]))
    print("TONE BY PUBLISHER: %s" % t["by_publisher"])
    print("DAILY: served %d -> built %d; gone %d, added %d, changed %d (by added mention %d, coverage-only %d, OTHER %d)"
          % (d["served"], d["built"], d["gone"], d["added"], d["changed"], d["changed_by_added_mention"],
             d["changed_coverage_only"], d["changed_other"]))
    holds = (not m_gone and not m_changed and not missing and not mismatch and not d_gone and not other
             and out["puts_sent"] == 0)
    print("RULE (tone rebuild): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % out["puts_sent"])
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
