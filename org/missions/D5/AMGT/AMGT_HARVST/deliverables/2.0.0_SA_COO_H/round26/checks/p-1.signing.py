"""HVST-p-1 signing measurement (issuer, read-only): the expected write of `build-mention`, produced by the producer's
own `build_mention` against a pass-through client that CAPTURES the put (round-25 ruling 1). Compared with the served
snapshot: pairs KEPT / CHANGED / NEW / GONE, and `mention_count` coverage. `--signing` writes
round26/p1_signing_expected.json; without it, re-measures, compares, and writes the act-start BEFORE (STOP on drift).
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p1_common as c  # noqa: E402


def measure():
    summary, key, rows = c.dry_build()
    served = c.served_rows()
    exp, cur = c.norm_rows(rows), c.norm_rows(served)
    return {
        "parts": c.list_parts(),
        "served_rows": len(served),
        "expected_key_shape": key.rsplit("/", 2)[0],
        "expected_rows": exp,
        "summary": {k: v for k, v in summary.items() if k != "key"},
        "diff": {
            "kept": sorted(k for k in exp if k in cur and exp[k] == cur[k]),
            "changed": sorted(k for k in exp if k in cur and exp[k] != cur[k]),
            "new": sorted(k for k in exp if k not in cur),
            "gone": sorted(k for k in cur if k not in exp),
        },
        "mention_count_null": sum(1 for r in rows if r.get("mention_count") is None),
        "lenovo_rows": sum(1 for r in rows if r.get("security_key") == "992_HK_Equity"),
        "lenovo_rows_served": sum(1 for r in served if r.get("security_key") == "992_HK_Equity"),
        "new_by_publisher": dict(collections.Counter(k.split(":", 1)[0] for k in exp if k not in cur)),
    }


def main():
    m = measure()
    d = m["diff"]
    print("gold %s parts: %d; served snapshot rows: %d" % (c.gold_prefix(), len(m["parts"]), m["served_rows"]))
    print("dry build: %s" % m["summary"])
    print("EXPECTED WRITE: 1 part under %s/ with %d rows -- KEPT %d, CHANGED %d, NEW %d, GONE %d"
          % (m["expected_key_shape"], len(m["expected_rows"]), len(d["kept"]), len(d["changed"]), len(d["new"]), len(d["gone"])))
    print("NEW pairs by publisher: %s; mention_count null in the write: %d" % (m["new_by_publisher"], m["mention_count_null"]))
    print("Lenovo (992_HK_Equity) pairs: served %d -> written %d" % (m["lenovo_rows_served"], m["lenovo_rows"]))
    for label in ("changed", "gone"):
        for k in d[label][:20]:
            print("  %-7s %s" % (label.upper(), k))
    if "--signing" in sys.argv:
        c.dump(c.SIGNING, m)
        print("wrote " + c.SIGNING)
        return 0
    s = c.load(c.SIGNING)
    drift = [k for k in ("parts", "expected_rows") if s[k] != m[k]]
    c.dump(os.path.join(c.WK, "p1_before.json"), m)
    if drift:
        print("BEFORE DIFFERS FROM SIGNING on %s -> STOP" % drift)
        return 1
    print("BEFORE == signing (gold parts, expected rows): OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
