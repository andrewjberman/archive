"""HVST-az-1 offline replay. Real universe/slug_queries/slug_query/_matches from the worktree. No network, .runtime read only.
BEFORE = the company's slug_query alone; AFTER = the alias set (slug_queries).
Usage: python az-1.replay.py <worktree> <workspace_root>"""

import glob
import json
import os
import re
import sys

WT, ROOT = sys.argv[1], sys.argv[2]
sys.path.insert(0, WT)
from lib.opal_data_harvest.__main__ import universe  # noqa: E402
from lib.opal_data_harvest.discovery import _matches  # noqa: E402
from lib.opal_data_harvest.publishers import slug_queries, slug_query  # noqa: E402

config = json.load(open(os.path.join(WT, "lib/opal_data_harvest/config.json"), encoding="utf-8"))
UNI = universe(config)
BY_KEY = {s["key"]: s for s in UNI}


def words(q):
    return re.findall(r"[a-z0-9]+", (q or "").lower())


def old(url, q):
    slug = url.rsplit("/", 1)[-1].lower()
    w = words(q)
    return bool(w) and all(x in slug for x in w)


def old_query(c):  # round-51 slug_query: `com` kept (as ay-1.replay.py)
    ws = re.findall(r"[A-Za-z0-9]+", c or "")
    suf = {"inc", "corp", "corporation", "co", "company", "ltd", "limited", "plc", "llc", "holdings", "holding",
           "group", "sa", "ag", "nv"}
    k = list(ws)
    while len(k) > 1 and k[-1].lower() in suf:
        k.pop()
    return " ".join(k)


def security(key):
    s = BY_KEY.get(key)
    if s:
        return s
    try:
        c = json.load(open(os.path.join(ROOT, ".runtime/harvest-backfill/securities", key + ".json"),
                           encoding="utf-8")).get("company")
    except Exception:
        return None
    return {"company": c, "aliases": []} if c else None


def after_match(sec, u):
    return any(_matches(u, q) for q in slug_queries(sec))


fails = []
results = {}
for rootd, pub in (("opal-data-harvest-bbg", "bbg"), ("opal-data-harvest-wsj", "wsj")):
    acc = []
    for f in glob.glob(os.path.join(ROOT, ".runtime", rootd, "runs/*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("publisher") != pub or not d.get("accepted"):
            continue
        sec = security(d.get("security_key") or "")
        if not sec or not sec.get("company"):
            continue
        for a in d["accepted"]:
            try:
                u = json.load(open(a["path"], encoding="utf-8")).get("url")
            except Exception:
                u = None
            if u:
                acc.append((sec, u))
    base = [(s, u) for s, u in acc if old(u, old_query(s["company"]))]
    kb = sum(1 for s, u in base if _matches(u, slug_query(s["company"])))
    ka, lost = 0, []
    for s, u in base:
        if after_match(s, u):
            ka += 1
            continue
        q = old_query(s["company"])
        toks = [t for t in u.rsplit("/", 1)[-1].lower().split("-") if t]
        miss = [w for w in words(q) if w not in toks and w + "s" not in toks]
        sub = not any(w in toks or w + "s" in toks for w in words(q)) and all(any(w in t for t in toks) for w in miss)
        cls = "substring_accident" if sub else "alias"
        print("LOST %s %s %s" % (cls, q, u.rsplit("/", 1)[-1]))
        lost.append(cls)
    print("%s: kept %d of %d (before)" % (pub, kb, len(base)))
    print("%s: kept %d of %d (after)" % (pub, ka, len(base)))
    results[pub] = (kb, ka, len(base), lost)
if results["wsj"][1] != results["wsj"][2]:
    fails.append("wsj kept after %d != n %d" % (results["wsj"][1], results["wsj"][2]))
if results["bbg"][1] < 3278:
    fails.append("bbg kept after %d < 3278" % results["bbg"][1])
if any(c != "substring_accident" for c in results["bbg"][3]):
    fails.append("bbg lost URL not class substring_accident")

urls = set()
for f in glob.glob(os.path.join(ROOT, ".runtime/opal-data-harvest-wsj/harvest_listing/*.xml")):
    urls.update(re.findall(r"<loc>([^<]+)</loc>", open(f, encoding="utf-8", errors="replace").read()))
urls = sorted(urls)
changed = []
table = {}
for s in UNI:
    n = sum(1 for u in urls if _matches(u, slug_query(s["company"])))
    m = sum(1 for u in urls if after_match(s, u))
    table[s["security_key"]] = (n, m)
    print("%s %s: before %d after %d" % (s["security_key"], s["company"], n, m))
    if n != m:
        changed.append(s["security_key"])
print("DENOMINATOR: %d names, %d urls, changed %d" % (len(UNI), len(urls), len(changed)))


def by_company(prefix):
    return [(k, v) for k, v in table.items() if next(x for x in UNI if x["security_key"] == k)["company"].startswith(prefix)]


for pre in ("Meta Platforms", "Eli Lilly", "Bank of America", "AT&T"):
    for k, (n, m) in by_company(pre):
        print("CHECK %s %s: before %d after %d" % (pre, k, n, m))
meta, bac, att = (table.get(k) for k in ("META_US_Equity", "BAC_US_Equity", "T_US_Equity"))
if not (meta and meta[1] > meta[0]):
    fails.append("Meta Platforms after not > before: %s" % (meta,))
if not (bac and bac[0] == bac[1]):
    fails.append("Bank of America changed: %s" % (bac,))
if not (att and att[0] == att[1]):
    fails.append("AT&T changed: %s" % (att,))
if sorted(changed) != ["LLY_US_Equity", "META_US_Equity"]:
    fails.append("changed is %s, not exactly META and LLY" % changed)
print("REPLAY FAIL: " + "; ".join(fails) if fails else "REPLAY OK")
