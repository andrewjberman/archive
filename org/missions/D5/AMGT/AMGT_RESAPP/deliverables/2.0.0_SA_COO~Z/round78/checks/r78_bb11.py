"""AMGT_RESAPP round 78 -- AMGT-bb-11: a plain served news-source name (round-77 enrichment item 7; DSGN_AMGTV1 round-47
close, "The news source is served with storage words").

  --crit AC1|AC2|AC3 --where local

AC1 (build): `lib.research.api.source_names`:
    C1 `source_name(raw)` gives a plain name for each of the eight source strings the function serves today (the three
       news strings read "Articles we collect"), known True, and no name carries a system word;
    C2 a string it does not know reads name None and known False: the raw text is never passed off as a name;
    C3 `publisher_name(code)` names the five publisher codes the feed serves today (sa, barrons, bbg, wsj, ft), and an
       unknown code reads None;
    C4 `with_publisher_names(items)` returns copies, each carrying `publisher_name` beside the unchanged `publisher`,
       and does not change the list it was handed.
AC2 (seam, the real neighbour): the real feed of BA_US_Equity, read by `scoped_amgt.read_feed`: its `source` string is
    known and named, and every item gets a non-empty `publisher_name` (N of N printed).
AC3 (bound): each of the eight raw strings AC1 names is still written in lib/research/api/scoped_amgt.py or
    lib/research/ledger/ledger.py, so the map names text the function really serves (8 of 8).
Verdict: R78 BB11 <CRIT> SERVED: YES|NO.
"""
from __future__ import annotations

import argparse
import copy
import io
import sys

BANNED = ("identity", "unresolved", "security key", "crosswalk", "dossier", "landed", "model block", "estate", "stage",
          "input ledger", "bronze", "gold", "harvested", "overlay", "ledger", "fetched_at", "market_data")
NEWS = "Articles we collect"
RAW = {
    "harvested news (the overlay feed, gold article_security_mention)": NEWS,
    "gold article_security_mention (the day view's own source)": NEWS,
    "the overlay feed's newest harvested article (fetched_at)": NEWS,
    "input ledger, class filings": "Company filings",
    "input ledger, class filings (a filings stage run recorded for this name)": "Company filings",
    "the input ledger's newest market_data run": "Bloomberg",
    "the Bloomberg pull the model block was computed from (raw_stamp_used)": "Bloomberg",
    "model block and input ledger": "Bloomberg",
}
CODES = {"sa": "Seeking Alpha", "barrons": "Barron's", "bbg": "Bloomberg", "wsj": "Wall Street Journal",
         "ft": "Financial Times"}
HOMES = ("lib/research/api/scoped_amgt.py", "lib/research/ledger/ledger.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crit", choices=("AC1", "AC2", "AC3"), required=True)
    ap.add_argument("--where", choices=("local",), default="local")
    a = ap.parse_args()
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    if a.crit == "AC3":
        text = ""
        for path in HOMES:
            with io.open(path, "r", encoding="utf-8") as handle:
                text += handle.read()
        gone = [raw for raw in RAW if raw not in text]
        clause("C1 every raw string the map names is still written in the producer", not gone,
               f"{len(RAW) - len(gone)} of {len(RAW)}; gone {gone}")
        return verdict(a, ok)

    try:
        from lib.research.api import source_names
    except ImportError as err:
        clause("C0 lib.research.api.source_names imports", False, str(err))
        return verdict(a, ok)
    named = getattr(source_names, "source_name", None)
    pub = getattr(source_names, "publisher_name", None)
    wrap = getattr(source_names, "with_publisher_names", None)
    if not (callable(named) and callable(pub) and callable(wrap)):
        clause("C0 source_name, publisher_name and with_publisher_names exist", False, "absent")
        return verdict(a, ok)

    if a.crit == "AC1":
        wrong = []
        for raw, want in RAW.items():
            got = named(raw)
            name = got.get("name")
            if name != want or got.get("known") is not True or [w for w in BANNED if w in str(name).lower()]:
                wrong.append((raw[:40], name))
        clause("C1 each source string served today has a plain name", not wrong, f"{len(RAW) - len(wrong)} of {len(RAW)}; wrong {wrong[:3]}")
        odd = named("some store nobody named (v9)")
        clause("C2 an unknown string is not passed off as a name",
               odd.get("name") is None and odd.get("known") is False and named(None).get("known") is False, repr(odd))
        miss = [(c, pub(c)) for c, v in CODES.items() if pub(c) != v]
        clause("C3 the five publisher codes are named and an unknown code is not", not miss and pub("zz9") is None and pub(None) is None,
               f"{len(CODES) - len(miss)} of {len(CODES)}; wrong {miss}")
        items = [{"publisher": "barrons", "title": "t1"}, {"publisher": "zz9", "title": "t2"}, {"publisher": None, "title": "t3"}]
        before = copy.deepcopy(items)
        out = wrap(items)
        clause("C4 items are copied, the name sits beside the unchanged code",
               items == before and out is not items and [i.get("publisher") for i in out] == ["barrons", "zz9", None]
               and out[0].get("publisher_name") == "Barron's" and "publisher_name" in out[1] and out[1]["publisher_name"] is None
               and out[0] is not items[0], repr([i.get("publisher_name") for i in out]))
        return verdict(a, ok)

    from lib.research.api import scoped_amgt

    feed = scoped_amgt.read_feed("BA_US_Equity")
    items = feed.get("items") or []
    got = named(feed.get("source"))
    out = wrap(items)
    with_name = [i for i in out if isinstance(i.get("publisher_name"), str) and i["publisher_name"].strip()]
    print(f"   BA US feed: status {feed.get('coverage_status')!r}; source {feed.get('source')!r} -> {got!r}; "
          f"items {len(items)}; with a publisher name {len(with_name)}; codes {sorted({str(i.get('publisher')) for i in items})}")
    clause("C1 the real feed's source string is known and named", got.get("known") is True and got.get("name") == NEWS)
    clause("C2 every real feed item gets a publisher name", len(items) >= 1 and len(with_name) == len(items),
           f"{len(with_name)} of {len(items)}")
    return verdict(a, ok)


def verdict(a, ok):
    yes = bool(ok) and all(ok)
    print(f"R78 BB11 {a.crit} SERVED: {'YES' if yes else 'NO'}")
    return 0 if yes else 1


if __name__ == "__main__":
    sys.exit(main())
