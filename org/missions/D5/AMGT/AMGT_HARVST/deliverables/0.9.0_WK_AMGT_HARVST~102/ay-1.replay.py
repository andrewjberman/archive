"""HVST-ay-1 offline replay. Real _matches/slug_query from the worktree; OLD substring rule inline. No network.
Usage: python ay-1.replay.py <worktree> <workspace_root>"""

import glob
import json
import os
import re
import sys

WT, ROOT = sys.argv[1], sys.argv[2]
sys.path.insert(0, WT)
from lib.opal_data_harvest.discovery import _matches  # noqa: E402
from lib.opal_data_harvest.publishers import slug_query  # noqa: E402


def words(q):
    return re.findall(r"[a-z0-9]+", (q or "").lower())


def old(url, q):
    slug = url.rsplit("/", 1)[-1].lower()
    w = words(q)
    return bool(w) and all(x in slug for x in w)


def old_query(c):  # round-51 slug_query: `com` kept
    ws = re.findall(r"[A-Za-z0-9]+", c or "")
    suf = {
        "inc",
        "corp",
        "corporation",
        "co",
        "company",
        "ltd",
        "limited",
        "plc",
        "llc",
        "holdings",
        "holding",
        "group",
        "sa",
        "ag",
        "nv",
    }
    k = list(ws)
    while len(k) > 1 and k[-1].lower() in suf:
        k.pop()
    return " ".join(k)


def company(key):
    try:
        return json.load(
            open(
                os.path.join(
                    ROOT, ".runtime/harvest-backfill/securities", key + ".json"
                ),
                encoding="utf-8",
            )
        ).get("company")
    except Exception:
        return None


fails = []
lost_all = []
for rootd, pub in (("opal-data-harvest-bbg", "bbg"), ("opal-data-harvest-wsj", "wsj")):
    acc = []
    for f in glob.glob(os.path.join(ROOT, ".runtime", rootd, "runs/*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("publisher") != pub or not d.get("accepted"):
            continue
        c = company(d.get("security_key") or "")
        if not c:
            continue
        for a in d["accepted"]:
            try:
                u = json.load(open(a["path"], encoding="utf-8")).get("url")
            except Exception:
                u = None
            if u:
                acc.append((c, u))
    base = [(c, u) for c, u in acc if old(u, old_query(c))]
    kept = 0
    for c, u in base:
        if _matches(u, slug_query(c)):
            kept += 1
        else:
            toks = [t for t in u.rsplit("/", 1)[-1].lower().split("-") if t]
            q = old_query(c)
            miss = [w for w in words(q) if w not in toks and w + "s" not in toks]
            # substring_accident: every query word is present only inside longer tokens or whole; alias: some word is
            # a whole token while another is absent as a whole token (the slug carries part of the name).
            sub = not any(w in toks or w + "s" in toks for w in words(q)) and all(
                any(w in t for t in toks) for w in miss
            )
            cls = "substring_accident" if sub else "alias"
            print("LOST %s %s %s" % (cls, q, u.rsplit("/", 1)[-1]))
            lost_all.append((pub, cls, c))
    print("%s: kept %d of %d" % (pub, kept, len(base)))
    if pub == "wsj" and kept != len(base):
        fails.append("wsj kept %d != n %d" % (kept, len(base)))
    if pub == "bbg":
        lost = len(base) - kept
        if lost > 6:
            fails.append("bbg lost %d > 6" % lost)
        for p, cls, c in lost_all:
            if (
                p == "bbg"
                and cls != "substring_accident"
                and slug_query(c) != "Eli Lilly"
            ):
                fails.append("bbg lost non-accident non-Lilly: " + c)

urls = set()
for f in glob.glob(
    os.path.join(ROOT, ".runtime/opal-data-harvest-wsj/harvest_listing/*.xml")
):
    urls.update(
        re.findall(
            r"<loc>([^<]+)</loc>", open(f, encoding="utf-8", errors="replace").read()
        )
    )
print("wsj stored sitemap unique URLs: %d" % len(urls))
for c in [
    "AT&T Inc",
    "SSE PLC",
    "Bank of America Corp",
    "Amazon.com Inc",
    "Meta Platforms Inc",
]:
    n = sum(1 for u in urls if old(u, old_query(c)))
    m = sum(1 for u in urls if _matches(u, slug_query(c)))
    print("%s: old %d new %d" % (c, n, m))
    if c in ("AT&T Inc", "SSE PLC", "Bank of America Corp") and m > 100:
        fails.append("%s new %d > 100" % (c, m))
print("REPLAY FAIL: " + "; ".join(fails) if fails else "REPLAY OK")
