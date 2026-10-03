"""HVST-ak-1 AC3 (issuer, read-only, NO WRITE): the gold mention rows carry the FinBERT tone joined by `record_hash`
(FWD-16).

Runs the REAL builder `publication_gold.build_mention` twice over the first 5 securities of the round-33 universe,
through the issuer's capturing client (round32/checks/ae-1.signing.py CapturingClient: every put is kept in memory,
none is sent), and reads live silver.
- Build 1 passes `sentiment_by_hash={}` to learn the rows' record_hash values.
- Build 2 passes a planted map covering every other record_hash.
PASS requires:
- `sentiment_finbert_label`, `sentiment_finbert_score` and `sentiment_scorer` are fields of `GOLD_MENTION_SCHEMA` and
  of the captured parquet;
- every planted row carries exactly its planted label, score and scorer;
- every unplanted row carries a null label and a null score;
- at least 1 row was built, and PUTS SENT is 0.
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
FIELDS = ("sentiment_finbert_label", "sentiment_finbert_score", "sentiment_scorer")

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)


def build(securities, sentiment_by_hash):
    cm = sg.CapturingClient(store._default_client())
    pg.build_mention(securities, datetime.datetime.now(datetime.timezone.utc).date(), client=cm,
                     sentiment_by_hash=sentiment_by_hash)
    (_k, body), = cm.puts.items()
    table = pq.read_table(io.BytesIO(body))
    return table.schema.names, table.to_pylist(), getattr(cm, "sent", 0)


def fail(failures):
    print("AC3 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


def main():
    failures = []
    names = [f.name for f in pg.GOLD_MENTION_SCHEMA]
    missing = [f for f in FIELDS if f not in names]
    print("SCHEMA missing %s" % missing)
    if missing:
        return fail(["GOLD_MENTION_SCHEMA lacks %s" % ", ".join(missing)])
    securities = json.load(open(UNIVERSE, encoding="utf-8"))[:5]
    try:
        _n, rows1, sent1 = build(securities, {})
    except TypeError as exc:
        return fail(["build_mention does not take sentiment_by_hash: %s" % exc])
    hashes = sorted({r["record_hash"] for r in rows1 if r.get("record_hash")})
    planted = {}
    for i, h in enumerate(hashes):
        if i % 2 == 0:
            label = ("positive", "negative", "neutral")[i % 3]
            planted[h] = {"label": label, "score": {"positive": 0.81, "negative": -0.72, "neutral": 0.0}[label],
                          "scorer": "opal-news-ai-sentiment"}
    names2, rows2, sent2 = build(securities, planted)
    print("BUILT %d rows over %d securities; record_hashes %d, planted %d; PUTS SENT %s/%s" % (
        len(rows2), len(securities), len(hashes), len(planted), sent1, sent2))
    for f in FIELDS:
        if f not in names2:
            failures.append("captured parquet lacks %s" % f)
    if not rows2:
        failures.append("no rows built")
    bad_planted, bad_unplanted = 0, 0
    for r in rows2:
        p = planted.get(r.get("record_hash"))
        if p is not None:
            if (r.get("sentiment_finbert_label"), r.get("sentiment_finbert_score"), r.get("sentiment_scorer")) != (
                    p["label"], p["score"], p["scorer"]):
                bad_planted += 1
        elif r.get("sentiment_finbert_label") is not None or r.get("sentiment_finbert_score") is not None:
            bad_unplanted += 1
    print("PLANTED rows wrong %d; UNPLANTED rows carrying a tone %d" % (bad_planted, bad_unplanted))
    if bad_planted:
        failures.append("%d planted rows do not carry their planted tone" % bad_planted)
    if bad_unplanted:
        failures.append("%d unplanted rows carry a tone" % bad_unplanted)
    if sent1 or sent2:
        failures.append("puts sent %s/%s" % (sent1, sent2))
    return fail(failures)


if __name__ == "__main__":
    sys.exit(main())
