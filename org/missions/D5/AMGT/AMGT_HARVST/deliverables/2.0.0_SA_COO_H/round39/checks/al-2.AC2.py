"""HVST-al-2 AC2 (issuer, read-only, NO WRITE, NO FinBERT call): the gold mention rows key their tone to a CONTENT hash of
the exact text scored (PRD v0.17 FWD-16; row Z-S67; round-38 analysis ruling 1).

Runs the REAL `publication_gold.build_mention` twice over the first 5 round-33-universe securities through the issuer's
capturing client (no put is sent), reading live silver.
- Build 1 passes `sentiment_by_key={}`.
- Build 2 passes a planted map covering every other content key.
PASS requires:
- `finbert_sentiment.content_key(text)` is the sha256 hex of the text's UTF-8 bytes, and None for None;
- `sentiment_content_key` is a field of `GOLD_MENTION_SCHEMA` and of the captured parquet;
- every row's `sentiment_content_key` equals `content_key(article_text(<its silver article row>))`;
- planted rows carry exactly the planted label, score and scorer, and unplanted rows carry a null label and score;
- PUTS SENT is 0.
"""
import datetime
import hashlib
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


def done(failures):
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures[:30]:
        print("  FAIL: " + f)
    return 0 if not failures else 1


def build(securities, sentiment_by_key):
    cm = sg.CapturingClient(store._default_client())
    pg.build_mention(securities, datetime.datetime.now(datetime.timezone.utc).date(), client=cm,
                     sentiment_by_key=sentiment_by_key)
    (_k, body), = cm.puts.items()
    t = pq.read_table(io.BytesIO(body))
    return t.schema.names, t.to_pylist(), getattr(cm, "sent", 0)


def main():
    try:
        from lib.research.harvest import finbert_sentiment as fs
    except Exception as exc:
        return done(["import finbert_sentiment: %s" % exc])
    failures = []
    ck = getattr(fs, "content_key", None)
    if ck is None:
        return done(["finbert_sentiment.content_key is absent"])
    if ck("abc") != hashlib.sha256("abc".encode("utf-8")).hexdigest() or ck(None) is not None:
        failures.append("content_key is not sha256(utf-8) / None for None")
    if "sentiment_content_key" not in [f.name for f in pg.GOLD_MENTION_SCHEMA]:
        return done(failures + ["GOLD_MENTION_SCHEMA lacks sentiment_content_key"])
    securities = json.load(open(UNIVERSE, encoding="utf-8"))[:5]
    try:
        _n, rows1, s1 = build(securities, {})
    except TypeError as exc:
        return done(failures + ["build_mention does not take sentiment_by_key: %s" % exc])
    keys = sorted({r.get("sentiment_content_key") for r in rows1 if r.get("sentiment_content_key")})
    planted = {}
    for i, k in enumerate(keys):
        if i % 2 == 0:
            label = ("positive", "negative", "neutral")[i % 3]
            planted[k] = {"label": label, "score": {"positive": 0.81, "negative": -0.72, "neutral": 0.0}[label],
                          "scorer": "opal-news-ai-sentiment"}
    names2, rows2, s2 = build(securities, planted)
    if "sentiment_content_key" not in names2:
        failures.append("captured parquet lacks sentiment_content_key")
    silver = {}
    for pub in sorted({r.get("publisher") for r in rows2 if r.get("publisher")}):
        for (k,), srow in store.silver_latest(pg.SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",)).items():
            silver[k] = srow
    key_bad = sum(1 for r in rows2 if r["article_key"] in silver
                  and r.get("sentiment_content_key") != ck(fs.article_text(silver[r["article_key"]])))
    bad_p = bad_u = 0
    for r in rows2:
        p = planted.get(r.get("sentiment_content_key"))
        got = (r.get("sentiment_finbert_label"), r.get("sentiment_finbert_score"), r.get("sentiment_scorer"))
        if p is not None and got != (p["label"], p["score"], p["scorer"]):
            bad_p += 1
        elif p is None and (got[0] is not None or got[1] is not None):
            bad_u += 1
    print("BUILT %d rows; distinct content keys %d, planted %d; key != content_key(article_text(silver)) %d;"
          " planted wrong %d; unplanted with a tone %d; PUTS SENT %s/%s" % (
              len(rows2), len(keys), len(planted), key_bad, bad_p, bad_u, s1, s2))
    if not rows2:
        failures.append("no rows built")
    if key_bad:
        failures.append("%d rows whose content key is not the hash of their scored text" % key_bad)
    if bad_p or bad_u:
        failures.append("planted wrong %d / unplanted toned %d" % (bad_p, bad_u))
    if s1 or s2:
        failures.append("puts sent %s/%s" % (s1, s2))
    return done(failures)


if __name__ == "__main__":
    sys.exit(main())
