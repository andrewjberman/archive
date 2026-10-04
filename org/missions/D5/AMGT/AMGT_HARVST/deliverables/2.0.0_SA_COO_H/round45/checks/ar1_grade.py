"""Round 45 HVST-ar-1 grader (FWD-2), shared by AC2 and AC3.

Reads one field-census JSON in the round-44 aq-1 shape (`publishers.<pub>.named_kinds`,
`article_paths_missing`, `no_silver_row_for_sampled_bronze`) and prints one verdict line.

A path is LOST when the census found it MISSING (not typed, not elsewhere, not in page_config_json)
in at least one sampled object. Site chrome is not an article field and is excluded by the declared
CHROME rule below, never by judgment at grading time.

PASS iff, for every one of the five publishers:
  1. no named-kind path (language, paywall, ticker_tags, sentiment, themes, summary) is LOST outside CHROME;
  2. no article-subtree path is LOST (barrons excepted: its whole page is the article subtree, so its
     article fields are graded through rule 1 only);
  3. every sampled original has a silver row.
"""

import json
import sys

PUBLISHERS = ("sa", "barrons", "bbg", "ft", "wsj")

# Declared site chrome: navigation, translation strings, ad config, the reader's own session state,
# follow-button config, author bios, and live market quotes. None is a field of the article.
CHROME_SUBSTRINGS = (
    ".menuItems.", ".translatedMessages.", ".adsConfig.",
    "instrumentResult", "tradingInfo", "marketdataContent",
)
CHROME_PREFIXES = (
    "barronsHeaderProps", "followTopicProps", "articleBylineProps", "availableDrawerInstruments",
    "quoteApiTickerNews", "isSubscriber",
)


def is_chrome(path):
    return path.startswith(CHROME_PREFIXES) or any(s in path for s in CHROME_SUBSTRINGS)


def grade(census):
    pubs = census.get("publishers") or {}
    failures = []
    for pub in PUBLISHERS:
        p = pubs.get(pub)
        if p is None:
            failures.append("%s: absent from the census" % pub)
            continue
        if not p.get("compared"):
            failures.append("%s: 0 objects compared" % pub)
        for kind, v in (p.get("named_kinds") or {}).items():
            for path, info in (v.get("paths_not_typed") or {}).items():
                if (info.get("missing") or 0) > 0 and not is_chrome(path):
                    failures.append("%s %s LOST %s (missing %s of %s)" % (pub, kind, path, info.get("missing"), info.get("carried")))
        if pub != "barrons":
            for path in (p.get("article_paths_missing") or {}):
                failures.append("%s article LOST %s" % (pub, path))
        nosilver = p.get("no_silver_row_for_sampled_bronze") or []
        if nosilver:
            failures.append("%s: %d sampled originals have no silver row" % (pub, len(nosilver)))
    return failures


def main(path, label):
    with open(path, encoding="utf-8") as fh:
        census = json.load(fh)
    failures = grade(census)
    per_pub = {pub: sum(1 for f in failures if f.startswith(pub + " ") or f.startswith(pub + ":")) for pub in PUBLISHERS}
    print("%s census: %s" % (label, path))
    print("%s lost per publisher: %s" % (label, json.dumps(per_pub, sort_keys=True)))
    for f in failures[:60]:
        print("  " + f)
    if len(failures) > 60:
        print("  ... %d more" % (len(failures) - 60))
    print("%s RESULT: %s" % (label, "PASS" if not failures else "FAIL"))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "GRADE"))
