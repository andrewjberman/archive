"""HVST-av-1 census: stored silver ft/wsj link sources. S3 GET/LIST only; no publisher contact."""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import lib.research.harvest.publication_gold as gold  # noqa: E402
from lib.research.harvest import store  # noqa: E402
from lib.opal_data_harvest.harvest_grammar import SOURCE_FOR_PUBLISHER  # noqa: E402


def first(v):
    if isinstance(v, (list, tuple)):
        v = next((i for i in v if isinstance(i, str) and i.strip()), None)
    return v.strip() if isinstance(v, str) and v.strip() else None


def main():
    for pub in ("ft", "wsj"):
        latest = store.silver_latest(SOURCE_FOR_PUBLISHER[pub], "article", ("article_key",))
        pref = gold._FT_WSJ_HOST[pub]
        src = {"top-level url": 0, "og:url": 0, "sourceUrl": 0, "none": 0}
        refused = 0
        both = same = 0
        for row in latest.values():
            meta = row.get("html_meta")
            og = first(meta.get("og:url")) if isinstance(meta, dict) else None
            ad = row.get("articleData")
            if isinstance(ad, str):
                try:
                    ad = json.loads(ad)
                except ValueError:
                    ad = None
            su = first(ad.get("sourceUrl")) if isinstance(ad, dict) and pub == "wsj" else None
            top = first(row.get("url"))
            for v in (top, og, su):
                if v and not v.startswith(pref):
                    refused += 1
            got = gold.article_url(row)
            if got is None:
                src["none"] += 1
            elif got == top:
                src["top-level url"] += 1
            elif got == og:
                src["og:url"] += 1
            else:
                src["sourceUrl"] += 1
            if pub == "wsj" and og and su:
                both += 1
                same += og == su
        n = len(latest)
        print("%s: articles %d; with link %d" % (pub, n, n - src["none"]))
        for k, v in src.items():
            print("  by source %s: %d" % (k, v))
        if pub == "wsj":
            print("  og:url == sourceUrl on %d of %d" % (same, both))
        print("  values refused for a foreign host: %d" % refused)


main()
