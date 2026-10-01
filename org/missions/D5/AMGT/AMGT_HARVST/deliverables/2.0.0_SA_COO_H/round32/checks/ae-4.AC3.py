"""HVST-ae-4 AC3 (issuer, read-only): the per-name depth table after the driver's WORLD run (toward FWD-14).

KEY SPACE (row AMGT_HARVST-Z-S51): the collector universe keys (`BA`, `security-<hash>`) do not appear in the gold
mention table (`BA_US_Equity`, ...): 0 of 89 at the cut, and only 32 of 89 names carry a ticker. So this census reads the
collector's OWN silver article rows, keyed by `discovered_for` (the universe key the job ran for), per publisher, and
counts DISTINCT articles published since 2026-01-01. Wrong-object rows (ae1_common.classify) are excluded.

PASS requires:
- the driver's run summary `~92/ae4_run_summary.json` exists, with `started_at`;
- distinct sa articles since 2026-01-01 over universe keys exceed the cut baseline below.
Securities at 50+ and 100+ (Andrew's bar, never re-based) are REPORTED with the denominator, not graded here.
"""
import collections
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ae1_common as c  # noqa: E402

PREFIX = {"sa": "seeking-alpha", "bbg": "bloomberg", "wsj": "wsj", "ft": "ft", "barrons": "barrons"}
# Measured at the cut (2026-10-01 ~05:2xZ) by running this file at the base; see the issuance commit.
BASELINE_SA_DISTINCT_SINCE_JAN = 20
SUMMARY = os.path.join(c.ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/ae4_run_summary.json")


def universe():
    p = subprocess.run([sys.executable, "-m", "lib.opal_data_harvest", "universe"], cwd=c.ROOT, capture_output=True,
                       text=True, timeout=120)
    return [s["key"] for s in json.loads(p.stdout)["securities"]]


def for_keys(value):
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value]
    text = str(value or "").strip()
    if text.startswith("["):
        try:
            return [str(v) for v in json.loads(text.replace("'", '"'))]
        except ValueError:
            return []
    return [text] if text and text != "None" else []


def main():
    failures = []
    uni = universe()
    uset = set(uni)
    cl = c.client()
    seen = collections.defaultdict(set)
    read = {}
    for pub, root in PREFIX.items():
        silver = c.rows(root + "/harvest/silver/article/", cl)
        listing = c.rows(root + "/harvest/silver/listing_hit/", cl) if pub == "sa" else []
        bad = {id(r) for r in c.classify(silver, listing)} if pub == "sa" else set()
        read[pub] = len(silver)
        for r in silver:
            if id(r) in bad or str(r.get("published_utc") or "")[:10] < c.FLOOR:
                continue
            for k in for_keys(r.get("discovered_for")):
                if k in uset:
                    seen[(k, pub)].add(str(r.get("article_id") or r.get("article_key") or r.get("record_hash")))
    print("UNIVERSE: %d; silver rows read %s" % (len(uni), " ".join("%s=%d" % kv for kv in read.items())))
    at50 = at100 = anyn = 0
    for k in uni:
        per = {p: len(seen.get((k, p), ())) for p in PREFIX}
        total = sum(per.values())
        anyn += total > 0
        at50 += total >= 50
        at100 += total >= 100
        if total:
            print("  %-28s total %4d  %s" % (k, total, " ".join("%s=%d" % (p, per[p]) for p in PREFIX)))
    sa_distinct = len(set().union(*[v for (k, p), v in seen.items() if p == "sa"] or [set()]))
    print("SECURITIES WITH ANY: %d of %d; AT 50+: %d of %d; AT 100+: %d of %d" % (anyn, len(uni), at50, len(uni),
                                                                               at100, len(uni)))
    print("SA DISTINCT SINCE 2026-01-01 (universe keys): %d (cut baseline %d)" % (sa_distinct, BASELINE_SA_DISTINCT_SINCE_JAN))
    if not os.path.exists(SUMMARY):
        failures.append("no driver run summary at ~92/ae4_run_summary.json")
    else:
        print("DRIVER RUN started_at %s" % json.load(open(SUMMARY, encoding="utf-8")).get("started_at"))
    if sa_distinct <= BASELINE_SA_DISTINCT_SINCE_JAN:
        failures.append("sa distinct articles since January did not rise above the cut baseline")
    print("AC3 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
