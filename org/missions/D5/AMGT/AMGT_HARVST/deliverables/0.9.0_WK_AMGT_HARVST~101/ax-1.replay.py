"""HVST-ax-1: offline replay. Parses the stored wsj sitemap XML files (NO request, no network, no browser profile) and
counts, per name, the URLs the OLD substring rule and the NEW whole-token rule admit; then checks that three CONTROL
names (the finished wsj jobs with the most accepted articles) keep every accepted URL under the NEW rule.

Run from the worktree root: python org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~101/ax-1.replay.py
"""
import glob
import json
import re
import sqlite3
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[7]
sys.path.insert(0, str(ROOT))
from lib.opal_data_harvest import discovery  # noqa: E402

RUNTIME = Path("C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest-wsj")
K = json.loads((ROOT / "lib/opal_data_harvest/contracts.json").read_text(encoding="utf-8"))["publishers"]["wsj"]["unselective_after"]


def old_matches(url, query):  # the rule HVST-ax-1 replaces (discovery.py before this cell)
    slug = url.rsplit("/", 1)[-1].lower()
    return all(word in slug for word in re.findall(r"[a-z0-9]+", (query or "").lower()))


urls = []
files = sorted(glob.glob(str(RUNTIME / "harvest_listing" / "*.xml")))
for path in files:
    urls.extend(h["url"] for h in discovery._hits(SimpleNamespace(text=Path(path).read_text(encoding="utf-8"))))
unique = sorted(set(urls))
print("sitemap files parsed: %d; <url> items: %d; unique URLs: %d; K (contracts.json wsj unselective_after) = %d"
      % (len(files), len(urls), len(unique), K))

fail = []
for name, query in (("T US Equity", "AT T"), ("SSE LN", "SSE")):
    old = sum(1 for u in unique if old_matches(u, query))
    new = sum(1 for u in unique if discovery._matches(u, query))
    print("%s: old %d new %d" % (name, old, new))
    if new > K:
        fail.append("%s: new %d > K %d" % (name, new, K))

# controls: the three finished wsj jobs with the most accepted articles (ties by job id)
records = []
for path in glob.glob(str(RUNTIME / "runs" / "*.json")):
    rec = json.loads(Path(path).read_text(encoding="utf-8"))
    if rec.get("publisher") == "wsj" and rec.get("finished_at") and rec.get("accepted"):
        records.append(rec)
records.sort(key=lambda r: (-len(r["accepted"]), r["job_id"]))
db = sqlite3.connect(str(RUNTIME / "progress.sqlite3"))
print("finished wsj jobs with an accepted article: %d; controls = the top 3 by accepted count" % len(records))
for rec in records[:3]:
    queries = {q for (q,) in db.execute("select query from harvest_listing_outbox where fetched_at>=? and fetched_at<=?",
                                        (rec["started_at"], rec["finished_at"]))}
    queries = {q.split(":", 1)[1] for q in queries if q.startswith("sitemap:")}
    name = "%s [%s]" % (rec.get("ticker") or rec["security_key"], rec["job_id"])
    if len(queries) != 1:
        fail.append("%s: query not recoverable from the listing outbox (found %s)" % (name, sorted(queries)))
        print("%s: query not recoverable (%s)" % (name, sorted(queries)))
        continue
    query = queries.pop()
    by_article = {(o or {}).get("article_key"): k[len("wsj:"):] for k, o in (rec.get("fetch_outcomes") or {}).items()}
    accepted_urls = [by_article.get(a["article_key"]) for a in rec["accepted"]]
    lost = [u for u in accepted_urls if u is None or not discovery._matches(u, query)]
    b = len(accepted_urls) - len(lost)
    print("%s (query %r): accepted %d, still admitted %d" % (name, query, len(rec["accepted"]), b))
    for u in lost:
        print("  LOST: %s slug=%s" % (u, (u or "").rsplit("/", 1)[-1]))
    if b != len(rec["accepted"]):
        fail.append("%s: accepted %d, still admitted %d" % (name, len(rec["accepted"]), b))
print("REPLAY FAIL: " + "; ".join(fail) if fail else "REPLAY OK")
