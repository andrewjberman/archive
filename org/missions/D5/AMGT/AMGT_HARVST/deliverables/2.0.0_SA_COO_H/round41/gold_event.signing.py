"""HARVST round 41 HVST-an-3 -- the serializing dry run the event-rebuild never-widen pair signs (issuer, NO WRITE).

Andrew-direct ~20:3xZ card 2: the served `chatter_event` snapshot is rebuilt over the NEWEST served mention snapshot.
`publication_gold.build_event` (its own code: newest mention + silver headlines -> `event_rows`) runs through the
issuer's capturing client (PUTS SENT 0) and the result is checked against the mention snapshot it read.

THE RULE (event rebuild):
- built events > 0, and every `event_id` is unique;
- every event's `security_key` is in the universe file, and every `article_keys` entry is a mention row of that security
  in the newest served mention snapshot (ORPHAN 0);
- `lead_article_key` is the first NON-GUARDED entry of `article_keys` (the builder's own rule: `event_rows` skips a
  member with `co_mention_count >= 4` when it picks the lead), and `articles_total` equals `len(article_keys)`;
- every event's `lead_headline` equals the silver headline of its lead article (HEADLINE MISMATCH 0).
The served events are REPLACED by the rebuild (the newest part is the snapshot): the 8 served rows are reported, with how
many of their event_ids the rebuild reproduces. That count is reported, not graded.

Writes `round41/gold_event_signing.json` (or the path in GOLD_EVENT_SIGNING_OUT). Prints `RULE (event rebuild): HOLDS`
only when all of it holds.
"""
import datetime
import hashlib
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

import pyarrow.parquet as pq  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

OUT = os.environ.get("GOLD_EVENT_SIGNING_OUT") or os.path.join(HERE, "gold_event_signing.json")


def check(events, mention, headlines, universe_keys):
    by_sec, row_of = {}, {}
    for r in mention:
        by_sec.setdefault(r.get("security_key"), set()).add(r.get("article_key"))
        row_of[(r.get("security_key"), r.get("article_key"))] = r
    ids = [e.get("event_id") for e in events]
    out_of_universe = sum(1 for e in events if e.get("security_key") not in universe_keys)
    orphan = sum(1 for e in events for k in (e.get("article_keys") or [])
                 if k not in by_sec.get(e.get("security_key"), set()))

    def first_unguarded(e):
        # The builder's own rule (publication_gold.event_rows): the lead is the first NON-GUARDED member in
        # `_event_sort_key` order, and `article_keys` is that order (`_is_guarded`: co_mention_count >= 4).
        for k in e.get("article_keys") or []:
            r = row_of.get((e.get("security_key"), k))
            if r is not None and not pg._is_guarded(r):
                return k
        return None
    lead_bad = sum(1 for e in events if e.get("lead_article_key") != first_unguarded(e))
    total_bad = sum(1 for e in events if e.get("articles_total") != len(e.get("article_keys") or []))
    headline_bad = sum(1 for e in events if e.get("lead_headline") != headlines.get(e.get("lead_article_key")))
    headline_null = sum(1 for e in events if not e.get("lead_headline"))
    return {"events": len(events), "duplicate_ids": len(ids) - len(set(ids)), "out_of_universe": out_of_universe,
            "orphan_article_keys": orphan, "lead_not_first": lead_bad, "articles_total_mismatch": total_bad,
            "headline_mismatch": headline_bad, "headline_null": headline_null,
            "securities_with_events": len({e.get("security_key") for e in events}),
            "holds": bool(events) and len(ids) == len(set(ids)) and not out_of_universe and not orphan
            and not lead_bad and not total_bad and not headline_bad}


def digest(rows):
    return hashlib.sha256(json.dumps(sorted(json.dumps(r, sort_keys=True, default=str) for r in rows)).encode()).hexdigest()


def main():
    universe = os.environ["HVST_GOLD_UNIVERSE"]
    securities = json.load(open(universe, encoding="utf-8"))
    universe_keys = {s.get("security_key") for s in securities}
    print("UNIVERSE FILE: %s (%d securities)" % (universe, len(securities)))
    as_of = datetime.datetime.now(datetime.timezone.utc).date()
    real = store._default_client()
    served_e = pg._latest_gold_snapshot_rows(pg.GOLD_EVENT_TABLE)
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE)
    headlines = pg._headline_by_article_key(client=real)
    ce = sg.CapturingClient(real)
    summary = pg.build_event(securities, as_of, client=ce)
    (ekey, ebody), = ce.puts.items()
    events = pq.read_table(io.BytesIO(ebody)).to_pylist()
    verdict = check(events, mention, headlines, universe_keys)
    served_ids = {e.get("event_id") for e in served_e}
    built_ids = {e.get("event_id") for e in events}
    out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "as_of": str(as_of),
           "universe_file": universe, "mention_rows_read": len(mention),
           "served": {"events": len(served_e), "securities": len({e.get("security_key") for e in served_e})},
           "built": verdict, "served_ids_reproduced": len(served_ids & built_ids), "key": ekey, "bytes": len(ebody),
           "built_digest": digest(events), "builder_summary_events": summary.get("events"), "puts_sent": ce.sent}
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    print("MENTION ROWS READ: %d" % len(mention))
    print("SERVED: %d events on %d securities" % (out["served"]["events"], out["served"]["securities"]))
    print("BUILT: %s" % json.dumps({k: v for k, v in verdict.items() if k != "holds"}))
    print("SERVED IDS REPRODUCED: %d of %d" % (out["served_ids_reproduced"], len(served_ids)))
    holds = verdict["holds"] and out["puts_sent"] == 0
    print("RULE (event rebuild): %s" % ("HOLDS" if holds else "BROKEN"))
    print("PUTS SENT: %d" % out["puts_sent"])
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
