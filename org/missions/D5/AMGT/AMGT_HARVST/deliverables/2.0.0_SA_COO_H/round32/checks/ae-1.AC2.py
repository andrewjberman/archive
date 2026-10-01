"""HVST-ae-1 AC2 (issuer, read-only): the re-check over every stored sa silver article row reads 0 UNQUARANTINED
wrong-object rows (FWD-12 DONE WHEN (a) count printed against rows checked, and (d) 0 mismatches).

Quarantine is read from the worker's local manifest `~90/ae1_quarantine.json` ({"s3_key", "article_keys", ...}) and is
honoured only when the S3 object at `s3_key` exists and lists the SAME article keys.
PASS requires: at least one row checked; the S3 quarantine object matching the local manifest; and 0 wrong-object rows
outside the quarantine.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ae1_common as c  # noqa: E402


def main():
    failures = []
    cl = c.client()
    silver = c.rows(c.SILVER, cl)
    listing = c.rows(c.LISTING, cl)
    wrong = c.classify(silver, listing)
    quarantined = set()
    if os.path.exists(c.MANIFEST):
        m = json.load(open(c.MANIFEST, encoding="utf-8"))
        local = set(m.get("article_keys") or [])
        try:
            remote = json.loads(cl.get_object(Bucket=c.B, Key=m.get("s3_key") or "")["Body"].read().decode("utf-8"))
            remote_keys = set(remote.get("article_keys") or [])
        except Exception as exc:  # noqa: BLE001
            remote_keys = None
            failures.append("S3 quarantine object unreadable at %r (%s)" % (m.get("s3_key"), type(exc).__name__))
        if remote_keys is not None and remote_keys != local:
            failures.append("S3 quarantine keys (%d) differ from the local manifest (%d)" % (len(remote_keys), len(local)))
        elif remote_keys is not None:
            quarantined = local
        print("QUARANTINE: %d article keys at s3://%s/%s" % (len(local), c.B, m.get("s3_key")))
    else:
        print("QUARANTINE: none (no manifest at %s)" % c.MANIFEST)
    remaining = [r for r in wrong if c.article_key(r) not in quarantined]
    parts = len({r["_part"] for r in silver})
    via_listing = sum(1 for r in silver if c.listed(r.get("discovered_for")))
    print("ROWS CHECKED: %d (silver parts %d; listing-discovered %d; listing hits read %d)"
          % (len(silver), parts, via_listing, len(listing)))
    print("WRONG-OBJECT: %d of %d; quarantined %d; outside quarantine %d"
          % (len(wrong), len(silver), len(wrong) - len(remaining), len(remaining)))
    for r in remaining[:5]:
        print("  WRONG: %s %s published %s title %r" % (c.article_key(r), r.get("discovered_for"),
                                                       str(r.get("published_utc"))[:10], str(r.get("title"))[:60]))
    print("RE-CHECK MISMATCHES: %d of %d" % (len(remaining), len(silver)))
    if not silver:
        failures.append("no sa silver rows read")
    if remaining:
        failures.append("%d wrong-object rows outside the quarantine" % len(remaining))
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
