"""AC3 -- publisher_coverage run PURE over the post-run listing_hit rows."""
import json
import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), ".scratch", "s1"))
from _common import client
from lib.research.harvest.publication_gold import publisher_coverage, _iter_all_listing_hits

securities_path = os.path.join(
    "org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
    "0.9.0_WK_AMGT_HARVST~4", "securities.json",
)
with open(securities_path, "r", encoding="utf-8") as f:
    securities = json.load(f)

c = client()
listing_hits = list(_iter_all_listing_hits(client=c))
coverage = publisher_coverage(listing_hits, securities)

denominator = len(securities)
sa_spans = 0
print("AC3 publisher_coverage (PURE), post-run listing_hit rows")
print("securities tested (denominator): %d" % denominator)
for security in securities:
    key = security.get("security_key")
    spans = coverage.get(key) or {}
    sa_span = spans.get("sa")
    if sa_span is not None:
        sa_spans += 1
        print("  %-16s sa span: (%s, %s)" % (key, sa_span[0].isoformat(), sa_span[1].isoformat()))
    else:
        print("  %-16s sa span: None" % key)

if sa_spans == 0:
    print("sa spans 0 of %d" % denominator)
else:
    print("sa spans %d of %d" % (sa_spans, denominator))
