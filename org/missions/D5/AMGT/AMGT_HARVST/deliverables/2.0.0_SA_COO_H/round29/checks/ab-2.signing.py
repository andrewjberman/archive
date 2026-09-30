"""HVST-ab-2 signing measurement (issuer, read-only): the expected write of `build-mention`, produced by the producer's
own `build_mention` -> `write_gold` against a pass-through client that CAPTURES the put, so the parquet really
serializes (the aa-3 lesson). Compared with the served snapshot: pairs KEPT / CHANGED / NEW / GONE, the 11 story ids'
pairs, and the pairs on the 11 hash-keyed empty bbg rows. `--signing` writes round29/ab2_signing_expected.json;
without it, re-measures, compares, and writes the act-start BEFORE (STOP on drift).
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ab2_common as c  # noqa: E402


def measure():
    summary, key, rows, nbytes = c.dry_build()
    served = c.served_rows()
    exp, cur = c.norm_rows(rows), c.norm_rows(served)
    new = sorted(k for k in exp if k not in cur)
    empty = set(c.empty_bbg_keys())
    return {
        "parts": c.list_parts(),
        "served_rows": len(served),
        "expected_key_shape": key.rsplit("/", 2)[0],
        "expected_rows": exp,
        "expected_bytes": nbytes,
        "summary": {k: v for k, v in summary.items() if k != "key"},
        "diff": {
            "kept": sorted(k for k in exp if k in cur and exp[k] == cur[k]),
            "changed": sorted(k for k in exp if k in cur and exp[k] != cur[k]),
            "new": new,
            "gone": sorted(k for k in cur if k not in exp),
        },
        "mention_count_null": sum(1 for r in rows if r.get("mention_count") is None),
        "story_id_pairs": {s: sorted(k for k in exp if k.split("|", 1)[0] == s) for s in c.STORY_IDS},
        "new_outside_story_ids": sorted(k for k in new if k.split("|", 1)[0] not in c.STORY_IDS),
        "empty_bbg_rows": sorted(empty),
        "pairs_on_empty_rows": sorted(k for k in exp if k.split("|", 1)[0] in empty),
        "new_by_publisher": dict(collections.Counter(k.split(":", 1)[0] for k in new)),
    }


def main():
    m = measure()
    d = m["diff"]
    print("gold %s parts: %d; served snapshot rows: %d" % (c.gold_prefix(), len(m["parts"]), m["served_rows"]))
    print("dry build: %s" % m["summary"])
    print("SERIALIZE (the real write_gold, put-captured): 1 put, %d rows, %d bytes"
          % (len(m["expected_rows"]), m["expected_bytes"]))
    print("EXPECTED WRITE: 1 part under %s/ with %d rows -- KEPT %d, CHANGED %d, NEW %d, GONE %d"
          % (m["expected_key_shape"], len(m["expected_rows"]), len(d["kept"]), len(d["changed"]), len(d["new"]),
             len(d["gone"])))
    print("NEW pairs by publisher: %s; NEW pairs outside the 11 story ids: %d; mention_count null in the write: %d"
          % (m["new_by_publisher"], len(m["new_outside_story_ids"]), m["mention_count_null"]))
    with_pairs = sum(1 for v in m["story_id_pairs"].values() if v)
    print("story ids with >= 1 pair: %d of %d" % (with_pairs, len(c.STORY_IDS)))
    for s, v in m["story_id_pairs"].items():
        print("  %s -> %s" % (s, [k.split("|", 1)[1] for k in v]))
    print("empty bbg rows served: %d; pairs on them in the write: %d"
          % (len(m["empty_bbg_rows"]), len(m["pairs_on_empty_rows"])))
    for label in ("changed", "gone"):
        for k in d[label][:20]:
            print("  %-7s %s" % (label.upper(), k))
    for k in m["new_outside_story_ids"][:20]:
        print("  NEW-OUTSIDE %s" % k)
    if "--signing" in sys.argv:
        c.dump(c.SIGNING, m)
        print("wrote " + c.SIGNING)
        return 0
    s = c.load(c.SIGNING)
    drift = [k for k in ("parts", "expected_rows", "expected_bytes") if s[k] != m[k]]
    c.dump(os.path.join(c.WK, "ab2_before.json"), m)
    if drift:
        print("BEFORE DIFFERS FROM SIGNING on %s -> STOP" % drift)
        return 1
    print("BEFORE == signing (gold parts, expected rows, expected bytes): OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
