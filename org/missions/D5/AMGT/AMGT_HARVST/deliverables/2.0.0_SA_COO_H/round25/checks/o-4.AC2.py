"""HVST-o-4 AC2 (issuer check, read-only): the readers now SERVE the rebuilt rows -- the reason the tie-break exists.

PASS requires, read through the merged `store.silver_latest` (HVST-o-3's rule): served record keys = before + the
expected NEW keys; each MOVED key's served record_hash is the rebuilt hash (a tied fetched_at resolved to the later
part) and its row carries non-null `links`, `type` and `meta`; each NEW key is served with its rebuilt hash; every
OTHER key's served record_hash is unchanged. A re-run of the rebuild against the served state expects to write 0
rows (idempotence: silver_append's own filter would skip everything).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import o4_common as c  # noqa: E402


def main():
    failures = []
    before = c.load(os.path.join(c.WK, "o4_before.json"))
    cl = c.client()
    latest, hashes = c.latest_hashes(cl)
    exp = before["expected_write"]
    moved = {t[1]: t[3] for t in exp if t[0] == "MOVED"}
    new = {t[1]: t[3] for t in exp if t[0] == "NEW"}
    want_keys = set(before["latest_record_hash"]) | set(new)
    print("served record keys: before %d, after %d, expected %d" % (len(before["latest_record_hash"]), len(hashes), len(want_keys)))
    if set(hashes) != want_keys:
        failures.append("served keys differ from expected: +%d / -%d"
                        % (len(set(hashes) - want_keys), len(want_keys - set(hashes))))
    ok_moved = 0
    for k, h in sorted(moved.items()):
        row = latest.get((k,)) or {}
        fields_ok = all(row.get(f) is not None for f in ("links", "type", "meta"))
        good = hashes.get(k) == h and fields_ok
        ok_moved += good
        print("  MOVED %s served_hash==rebuilt: %s links/type/meta present: %s" % (k, hashes.get(k) == h, fields_ok))
        if not good:
            failures.append("MOVED %s not served as rebuilt" % k)
    ok_new = sum(1 for k, h in new.items() if hashes.get(k) == h)
    if ok_new != len(new):
        failures.append("NEW keys served with rebuilt hash: %d of %d" % (ok_new, len(new)))
    others = [k for k in before["latest_record_hash"] if k not in moved]
    changed = [k for k in others if hashes.get(k) != before["latest_record_hash"][k]]
    print("MOVED served as rebuilt: %d of %d; NEW served: %d of %d; other keys unchanged: %d of %d"
          % (ok_moved, len(moved), ok_new, len(new), len(others) - len(changed), len(others)))
    if changed:
        failures.append("%d other served key(s) changed (first: %s)" % (len(changed), changed[0]))
    again = c.expected_write(c.rebuilt_rows(cl), latest)
    print("idempotence: a re-run would write %d row(s)" % len(again))
    if again:
        failures.append("a re-run would still write %d row(s) (first: %s)" % (len(again), again[0][:3]))

    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
