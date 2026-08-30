"""P2-CENSUS item 1 -- unit test for the per-feed selector. NO VENDOR CALL ANYWHERE.

Every arm either calls resolve_feeds() (pure) or drives run() with _request PATCHED AT THE
BOUNDARY, so the question is always "which feeds would this call spend", never "what does BD
return". DRY_RUN is left at its default 1 as a second, independent refusal.
"""
import os
import sys

os.environ.setdefault("AWS_DEFAULT_REGION", "us-east-1")
sys.path.insert(0, "infra/aws/lambda/opal-assets/opal-assets-bd49f-reporting-pull")
import lambda_function as L  # noqa: E402

passed = failed = 0


def arm(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print("  OK:  %-54s %s" % (name, detail))
    else:
        failed += 1
        print("  FAIL:%-54s %s" % (name, detail))


arm("egress/DRY_RUN-still-1-no-socket-permitted", L.DRY_RUN is True, "second independent refusal")
arm("default/unspecified-preserves-ALL-THREE",
    sorted(L.resolve_feeds(None)) == ["allocation", "costbasis", "performance"],
    "protects OPAL_TAXSMA_PT2's silver build, which reads costbasis + allocation bronze")
arm("select/performance-only-is-expressible",
    L.resolve_feeds(["performance"]) == ["performance"], "P2 spends ONE endpoint per account")
for bad in (["perfrmance"], ["performance", "nope"], ["PERFORMANCE"]):
    try:
        L.resolve_feeds(bad)
        arm("refuse/unlisted-feed-REFUSED %r" % (bad,), False, "accepted an unlisted feed")
    except ValueError as e:
        arm("refuse/unlisted-feed-REFUSED %r" % (bad,), "REFUSING" in str(e), "named refusal")
try:
    L.resolve_feeds([])
    arm("refuse/empty-list-REFUSED", False, "accepted an empty pull")
except ValueError as e:
    arm("refuse/empty-list-REFUSED", "not a pull" in str(e), "named refusal")

# THE ARM THAT MATTERS: what does run() actually SPEND? _request is patched at the boundary, so
# no socket is opened even if DRY_RUN were flipped -- the two refusals are independent.
spent = []


def fake_request(method, path, **kw):
    spent.append(path)
    return b'{"combinedLevels": [], "dataDate": "2026-08-28T00:00:00"}'


L._request = fake_request
L.land_bronze = lambda raw, feed, aid, q_end, pull_date: "s3://stub/%s/%s" % (feed, aid)
accts = [{"bd_account_id": 1, "schwab_account": "0000000001", "inception": "2026-03-16"},
         {"bd_account_id": 2, "schwab_account": "0000000002", "inception": "2026-03-16"}]

spent.clear()
m = L.run(accts, "2026-07-01", "2026-08-28", "2026-08-30", cookie="x", token="y",
          feeds=["performance"])
arm("spend/ONE-call-per-account-when-narrowed", len(spent) == 2,
    "%d calls for 2 accounts (was 6 before the selector)" % len(spent))
arm("spend/only-the-performance-path-touched",
    all("performancePeriod" in p for p in spent), "paths=%s" % sorted(set(spent)))
arm("manifest/records-the-feeds-actually-spent",
    m.get("feeds_requested") == ["performance"], "feeds_requested=%r" % (m.get("feeds_requested"),))

spent.clear()
L.run(accts, "2026-07-01", "2026-08-28", "2026-08-30", cookie="x", token="y")
arm("spend/UNSPECIFIED-still-spends-all-three", len(spent) == 6,
    "%d calls for 2 accounts -- the pre-existing behaviour is intact" % len(spent))

print("\nP2-1 feed-selector test: %d of %d arms passed." % (passed, passed + failed))
sys.exit(1 if failed else 0)
