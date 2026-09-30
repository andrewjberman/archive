"""HVST-aa-3 signing measurement (issuer, read-only): the expected diff read from the MERGED rule (builder at CLOUD,
tie-break from HVST-o-3), plus the BEFORE state of every sa silver and bronze article object. Writes
round25/o4_signing_expected.json; the COO half cites it. Without --signing it re-measures and compares (the act's
BEFORE gate): prints BEFORE == signing: OK, or the drift and STOP.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aa3_common as c  # noqa: E402


def measure():
    cl = c.client()
    latest, hashes = c.latest_hashes(cl)
    rebuilt = c.rebuilt_rows(cl)
    write = c.expected_write(rebuilt, latest)
    return {
        "silver_parts": c.list_objects(c.silver_prefix(), cl),
        "bronze_objects": c.list_objects(c.bronze_prefix(), cl),
        "latest_record_hash": hashes,
        "rebuilt_rows": len(rebuilt),
        "expected_write": [list(t) for t in write],
    }


def main():
    m = measure()
    kinds = collections.Counter(t[0] for t in m["expected_write"])
    dates = collections.Counter(t[4] for t in m["expected_write"])
    print("bbg silver article parts: %d; bbg bronze article objects: %d; served record keys (latest): %d; rebuilt rows: %d"
          % (len(m["silver_parts"]), len(m["bronze_objects"]), len(m["latest_record_hash"]), m["rebuilt_rows"]))
    print("EXPECTED WRITE (silver_append's own filter): %d rows -- %s; fetch-date groups (= new parts): %d %s"
          % (len(m["expected_write"]), dict(kinds), len(dates), dict(sorted(dates.items()))))
    for t in m["expected_write"]:
        print("  %-5s %s | %s | %s" % (t[0], t[1], t[4], t[2]))
    print("served record keys AFTER, if applied: %d" % (len(m["latest_record_hash"]) + kinds.get("NEW", 0)))
    if "--signing" in sys.argv:
        c.dump(c.SIGNING, m)
        print("wrote " + c.SIGNING)
        return 0
    s = c.load(c.SIGNING)
    drift = [k for k in ("silver_parts", "bronze_objects", "latest_record_hash", "expected_write") if s[k] != m[k]]
    c.dump(os.path.join(c.WK, "aa3_before.json"), m)
    if drift:
        print("BEFORE DIFFERS FROM SIGNING on %s -> STOP" % drift)
        return 1
    print("BEFORE == signing (parts, bronze, latest hashes, expected write): OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
