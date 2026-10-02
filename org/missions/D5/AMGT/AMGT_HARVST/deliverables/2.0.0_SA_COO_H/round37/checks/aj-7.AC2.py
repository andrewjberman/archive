"""HVST-aj-7 AC2 (issuer, read-only, NO WRITE): `title` (VERBATIM, rule 17b) and `published_precision` join the gold mention
rows (CTO track-C ruling msg 28509; RESAPP r62 addendum @40e1d622aa).

Runs the REAL builder `publication_gold.build_mention` over the first 5 securities of the round-33 universe through the
issuer's capturing client (round32/checks/ae-1.signing.py CapturingClient: every put is kept in memory, none is sent).
Reads live silver. PASS requires:
- `title` and `published_precision` are fields of `GOLD_MENTION_SCHEMA` and of the captured parquet;
- every captured row's `title` is byte-identical to its silver article's `title` (null where silver has none, never
  ""), and `published_precision` equals silver's;
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
sys.path.insert(0, R32)
UNIVERSE = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/2.0.0_SA_COO_H/round33/securities.universe.r33.json")

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

_spec = importlib.util.spec_from_file_location("ae1_signing", os.path.join(R32, "ae-1.signing.py"))
sg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sg)


def silver_articles(source_keys):
    """{article_key: silver row} for the article keys the captured gold rows name, from each source's silver."""
    out = {}
    for source in source_keys:
        latest = store.silver_latest(source, "article", ("article_key",))
        for (k,), row in latest.items():
            out[k] = row
    return out


def main():
    failures = []
    names = [f.name for f in pg.GOLD_MENTION_SCHEMA]
    print("SCHEMA has title=%s published_precision=%s" % ("title" in names, "published_precision" in names))
    for f in ("title", "published_precision"):
        if f not in names:
            failures.append("GOLD_MENTION_SCHEMA lacks %s" % f)
    if failures:
        print("AC2 RESULT: FAIL (%d failure(s))" % len(failures))
        for f in failures:
            print("  FAIL: " + f)
        return 1
    securities = json.load(open(UNIVERSE, encoding="utf-8"))[:5]
    cm = sg.CapturingClient(store._default_client())
    pg.build_mention(securities, datetime.datetime.now(datetime.timezone.utc).date(), client=cm)
    puts_sent = getattr(cm, "sent", 0)
    (_k, body), = cm.puts.items()
    rows = pq.read_table(io.BytesIO(body)).to_pylist()
    print("BUILT %d rows over %d securities; PUTS SENT %s" % (len(rows), len(securities), puts_sent))
    if not rows:
        failures.append("no rows built")
    sources = sorted({pg.SOURCE_FOR_PUBLISHER[r["publisher"]] for r in rows} if hasattr(pg, "SOURCE_FOR_PUBLISHER")
                     else {r["article_key"].split(":")[0] for r in rows})
    silver = silver_articles([s for s in sources if s])
    mism_t, mism_p, missing = 0, 0, 0
    for r in rows:
        s = silver.get(r["article_key"])
        if s is None:
            missing += 1
            continue
        expected_title = s.get("title") or None  # verbatim; null where silver has none, never ""
        if r.get("title") != expected_title:
            mism_t += 1
        if r.get("published_precision") != s.get("published_precision"):
            mism_p += 1
    print("TITLE mismatches %d; PRECISION mismatches %d; rows without a silver article %d (of %d)" % (
        mism_t, mism_p, missing, len(rows)))
    if mism_t:
        failures.append("%d rows whose title is not the silver title verbatim" % mism_t)
    if mism_p:
        failures.append("%d rows whose published_precision differs from silver" % mism_p)
    if puts_sent:
        failures.append("puts sent %s" % puts_sent)
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
