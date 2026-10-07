"""Offline evaluation of slug-matcher rules. Recall = accepted article URLs (bbg, wsj) each rule still admits.
Selectivity = candidates each rule admits in the stored wsj sitemaps for chosen names. No request is made."""

import glob
import json
import os
import re
import sys

ROOT = sys.argv[1]
sys.path.insert(0, ROOT)
from lib.opal_data_harvest.publishers import slug_query  # noqa: E402


def words(q):
    return re.findall(r"[a-z0-9]+", (q or "").lower())


def toks(url):
    return [t for t in url.rsplit("/", 1)[-1].lower().split("-") if t]


def r_old(url, q):
    slug = url.rsplit("/", 1)[-1].lower()
    return all(w in slug for w in words(q))


def r_adj(url, q):
    j = "".join(words(q))
    t = toks(url)
    if not j:
        return False
    for i in range(len(t)):
        s = ""
        for x in t[i:]:
            s += x
            if len(s) > len(j) + 1:
                break
            if s == j or s == j + "s":
                return True
    return False


def tok_has(t, w):
    return w in t or (w + "s") in t


def r_tok_all(url, q):
    t = set(toks(url))
    w = words(q)
    return bool(w) and all(tok_has(t, x) for x in w)


def r_union(url, q):
    return r_adj(url, q) or r_tok_all(url, q)


def r_brand(url, q):
    w = words(q)
    if not w:
        return False
    if len(w[0]) < 3:
        return r_adj(url, q)
    return tok_has(set(toks(url)), w[0])


def r_brand_or_adj(url, q):
    return r_adj(url, q) or r_brand(url, q)


RULES = [
    ("old substring", r_old),
    ("adjacent (merged ax-1)", r_adj),
    ("every word a whole token", r_tok_all),
    ("adjacent OR every-word-token", r_union),
    ("first word a whole token (>=3 chars) else adjacent", r_brand),
]


def company_of(key):
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


def accepted(root, pub):
    out = []
    for f in glob.glob(os.path.join(ROOT, ".runtime", root, "runs/*.json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if d.get("publisher") != pub or not d.get("accepted"):
            continue
        c = company_of(d.get("security_key") or "")
        if not c:
            continue
        for a in d["accepted"]:
            try:
                u = json.load(open(a["path"], encoding="utf-8")).get("url")
            except Exception:
                u = None
            if u:
                out.append((slug_query(c), u, str(d.get("ticker"))))
    return out


for root, pub in (("opal-data-harvest-bbg", "bbg"), ("opal-data-harvest-wsj", "wsj")):
    acc = accepted(root, pub)
    base = [a for a in acc if r_old(a[1], a[0])]
    print(
        "%s accepted articles with a url and company: %d; admitted by the old rule: %d"
        % (pub, len(acc), len(base))
    )
    for name, rule in RULES[1:]:
        kept = sum(1 for q, u, _ in base if rule(u, q))
        print(
            "   %-52s keeps %d of %d (loses %d)"
            % (name, kept, len(base), len(base) - kept)
        )

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
NAMES = [
    "AT&T Inc",
    "SSE PLC",
    "Amazon.com Inc",
    "Universal Music Group",
    "ICICI Bank Ltd",
    "Eli Lilly & Co",
    "Bank of America Corp",
    "Visa Inc",
    "Netflix Inc",
    "Apple Inc",
    "Meta Platforms Inc",
    "General Motors Co",
    "Target Corp",
    "Gap Inc",
    "Block Inc",
]
print("candidates in the stored wsj sitemaps, per rule:")
print("   %-24s %s" % ("company (query)", " | ".join(n[:22] for n, _ in RULES)))
for c in NAMES:
    q = slug_query(c)
    print(
        "   %-24s %s"
        % (
            "%s (%s)" % (c[:14], q)[:24],
            " | ".join("%22d" % sum(1 for u in urls if r(u, q)) for _, r in RULES),
        )
    )
