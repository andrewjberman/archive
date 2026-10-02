"""HVST-al-2 AC3 (issuer, read-only, NO WRITE): the window builder joins tone by the CONTENT key carried on each mention row (PRD v0.17 FWD-16 key; FWD-17).

Builds the gold mention rows for the first 5 round-33-universe securities through the capturing client (no put; the
served snapshot predates the content key), plants a
deterministic tone per CONTENT KEY (`sentiment_content_key`; the first security is planted ALL-NEUTRAL), and calls
`window_tone.build_window_rows(mention_rows, sentiment_by_key, window_end)` with window_end = the last trading day
(`trading_calendar.prev_trading_day(today UTC)`). It then recomputes every row independently. PASS requires:
- 3 rows (windows 30, 90, 365) per security that has served mention rows, each with window_end equal to the T-1
  date;
- window_start_requested = window_end - (N - 1) days; window_start_served = max(requested, 2026-01-01);
- articles_total, scored, voters and tone equal this check's own recompute over the mention rows whose UTC
  publication day is in [window_start_served, window_end]. A voter is a non-neutral label with NO confidence
  threshold. tone is the mean signed score over the voters, compared within 1e-9;
- the all-neutral security reads voters 0 and tone null (None, never 0.0) in every window where it has articles.
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
sys.path.insert(0, ROOT)
UNIVERSE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round33/securities.universe.r33.json")
STORE_START = datetime.date(2026, 1, 1)
WINDOWS = (30, 90, 365)

from lib import trading_calendar  # noqa: E402
from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402
import importlib.util  # noqa: E402
import io  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402
_R32 = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round32/checks")
_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(_R32, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)


def pub_day(row):
    v = row.get("published_utc")
    if v is None:
        return None
    if isinstance(v, datetime.datetime):
        return (v if v.tzinfo is None else v.astimezone(datetime.timezone.utc)).date()
    return datetime.datetime.fromisoformat(str(v).replace("Z", "+00:00")).astimezone(datetime.timezone.utc).date()


def plant(h, all_neutral):
    if all_neutral:
        return {"label": "neutral", "score": 0.0}
    k = int(hashlib.sha256(h.encode()).hexdigest()[:8], 16) % 4
    return [{"label": "positive", "score": 0.8}, {"label": "negative", "score": -0.7},
            {"label": "neutral", "score": 0.0}, None][k]


def main():
    failures = []
    try:
        from lib.research.harvest import window_tone as wt
    except Exception as exc:
        print("IMPORT FAILED: %s: %s" % (type(exc).__name__, exc))
        print("AC3 RESULT: FAIL (1 failure(s))")
        return 1
    securities = json.load(open(UNIVERSE, encoding="utf-8"))[:5]
    wanted = [s["security_key"] for s in securities]
    cm = sg.CapturingClient(store._default_client())
    pg.build_mention(securities, datetime.datetime.now(datetime.timezone.utc).date(), client=cm, sentiment_by_key={})
    (_k, body), = cm.puts.items()
    mention = [r for r in pq.read_table(io.BytesIO(body)).to_pylist() if r.get("security_key") in wanted]
    keys = [k for k in wanted if any(r["security_key"] == k for r in mention)]  # securities with served articles
    neutral_key = keys[0]
    sentiment = {}
    for r in mention:
        h = r.get("sentiment_content_key")
        if h and h not in sentiment:
            p = plant(h, r["security_key"] == neutral_key)
            if p is not None:
                sentiment[h] = dict(p, scorer="opal-news-ai-sentiment")
    window_end = trading_calendar.prev_trading_day(datetime.datetime.now(datetime.timezone.utc).date())
    rows = wt.build_window_rows(mention, sentiment, window_end)
    print("MENTION rows %d over %d securities; planted %d hashes; window_end %s; window rows %d" % (
        len(mention), len(keys), len(sentiment), window_end, len(rows)))
    if len(rows) != len(keys) * len(WINDOWS):
        failures.append("%d window rows, expected %d" % (len(rows), len(keys) * len(WINDOWS)))
    by = {(r["security_key"], r["window_days"]): r for r in rows}
    for key in keys:
        own = [r for r in mention if r["security_key"] == key]
        for n in WINDOWS:
            r = by.get((key, n))
            if r is None:
                failures.append("no row for %s %dd" % (key, n))
                continue
            req = window_end - datetime.timedelta(days=n - 1)
            served = max(req, STORE_START)
            arts = {}
            for m in own:
                d = pub_day(m)
                if d is not None and served <= d <= window_end:
                    arts[m["article_key"]] = sentiment.get(m.get("sentiment_content_key"))
            scored = [s for s in arts.values() if s is not None]
            voters = [s for s in scored if s["label"] != "neutral"]
            tone = (sum(v["score"] for v in voters) / len(voters)) if voters else None
            exp = {"window_end": window_end, "window_start_requested": req, "window_start_served": served,
                   "articles_total": len(arts), "scored": len(scored), "voters": len(voters)}
            for f, v in exp.items():
                got = r.get(f)
                if isinstance(got, datetime.datetime):
                    got = got.date()
                if isinstance(got, str):
                    got = datetime.date.fromisoformat(got[:10]) if f.startswith("window_") else got
                if got != v:
                    failures.append("%s %dd %s=%r expected %r" % (key, n, f, got, v))
            got_tone = r.get("tone")
            if tone is None:
                if got_tone is not None:
                    failures.append("%s %dd tone=%r expected null" % (key, n, got_tone))
            elif got_tone is None or abs(got_tone - tone) > 1e-9:
                failures.append("%s %dd tone=%r expected %r" % (key, n, got_tone, tone))
            if key == neutral_key:
                print("ALL-NEUTRAL %s %dd: articles %d voters %s tone %r" % (key, n, len(arts), r.get("voters"), got_tone))
    print("AC3 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures[:40]:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
