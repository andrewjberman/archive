"""Offline: for every finished bbg job with an accepted article, would the NEW slug matcher still admit each accepted URL?
Reads run records and stored publication files only; no request."""

import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, sys.argv[1])
from lib.opal_data_harvest.discovery import _matches as new_match
from lib.opal_data_harvest.publishers import slug_query


def company_of(key):
    try:
        return json.load(
            open(
                os.path.join(
                    sys.argv[1], ".runtime/harvest-backfill/securities", key + ".json"
                ),
                encoding="utf-8",
            )
        ).get("company")
    except Exception:
        return None


def old_match(url, query):
    slug = url.rsplit("/", 1)[-1].lower()
    return all(w in slug for w in re.findall(r"[a-z0-9]+", (query or "").lower()))


jobs = arts = nourl = notsitemap = 0
kept = lost = oldmiss = 0
per = collections.defaultdict(lambda: [0, 0])
examples = []
for f in glob.glob(
    os.path.join(sys.argv[1], ".runtime/opal-data-harvest-bbg/runs/*.json")
):
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    if d.get("publisher") != "bbg" or not d.get("accepted"):
        continue
    jobs += 1
    for a in d["accepted"]:
        arts += 1
        try:
            p = json.load(open(a["path"], encoding="utf-8"))
        except Exception:
            nourl += 1
            continue
        company = company_of(d.get("security_key") or "")
        url, query = p.get("url"), (slug_query(company) if company else None)
        if not url or not query:
            nourl += 1
            continue
        if not old_match(url, query):
            oldmiss += 1
            continue
        if new_match(url, query):
            kept += 1
            per[str(d.get("ticker"))][0] += 1
        else:
            lost += 1
            per[str(d.get("ticker"))][1] += 1
            if len(examples) < 14:
                examples.append((query, url.rsplit("/", 1)[-1][:90]))
print("bbg jobs with an accept: %d; accepted articles: %d" % (jobs, arts))
print(
    "no url/query on the stored record: %d; not sitemap-discovered: %d; old rule itself would not admit: %d"
    % (nourl, notsitemap, oldmiss)
)
print(
    "sitemap-discovered, admitted by OLD rule: %d -> NEW rule keeps %d, loses %d"
    % (kept + lost, kept, lost)
)
worst = sorted(((v[1], v[0], k) for k, v in per.items() if v[1]), reverse=True)[:10]
print("names losing accepted URLs (lost, kept, ticker):", worst)
for e in examples:
    print("  LOST", e)
