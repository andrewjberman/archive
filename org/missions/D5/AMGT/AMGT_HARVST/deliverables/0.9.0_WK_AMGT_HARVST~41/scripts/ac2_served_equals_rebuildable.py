"""HVST-d-2 AC2: C-HV-GOLD-REBUILDABLE ON THE SERVED PLANE. For each table, the rows built IN MEMORY from the
same inputs (securities.universe.json + the landed silver + the landed listing hits, day range ending at the
served part's own as-of) equal the SERVED newest snapshot row by row. S3 GET only; writes nothing."""
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _rebuild as R  # noqa: E402

from lib.research.harvest import publication_gold as pg  # noqa: E402
from lib.research.harvest import store  # noqa: E402

KEYS = {pg.GOLD_TABLE: lambda r: (r["article_key"], r["security_key"]),
        pg.GOLD_DAILY_TABLE: lambda r: (r["security_key"], r["day"]),
        pg.GOLD_EVENT_TABLE: lambda r: (r["event_id"],)}


def main():
    client = store._default_client()
    newest = {t: R.parts(t, client)[-1] for t in R.TABLES}
    as_of = R.date_of(newest[pg.GOLD_DAILY_TABLE][0])
    print("== INPUTS ==")
    for t in R.TABLES:
        print("served newest %-26s %s ETag=%s" % (t, R.short(newest[t][0]), newest[t][1]))
    print("in-memory day range ends at the served daily part's as-of = %s ; securities file = 191 securities" % as_of)
    served = {t: pg._latest_gold_snapshot_rows(t, client=client) for t in R.TABLES}
    mem, n_art, _titles = R.memory(R.load_securities(), as_of, client)
    print("silver articles read = %d" % n_art)

    all_equal = True
    print("\n== ROW BY ROW: in-memory rebuild vs the SERVED newest snapshot ==")
    for t in R.TABLES:
        kf = KEYS[t]
        s = {kf(r): R.canon_row(r) for r in served[t]}
        n = {kf(r): R.canon_row(r) for r in mem[t]}
        dup = (len(s) != len(served[t])) or (len(n) != len(mem[t]))
        only_s = sorted(set(s) - set(n))
        only_n = sorted(set(n) - set(s))
        diffs = []
        for k in sorted(set(s) & set(n)):
            fields = [f for f in sorted(set(s[k]) | set(n[k])) if s[k].get(f) != n[k].get(f)]
            if fields:
                diffs.append((k, fields))
        equal = not dup and not only_s and not only_n and not diffs
        all_equal = all_equal and equal
        cols = len(R.SCHEMAS[t].names)
        print("%-26s served rows=%d in-memory rows=%d keys equal=%s duplicate keys=%s columns compared=%d fields compared=%d  rows differing=%d  only-served=%d only-in-memory=%d  => %s" % (
            t, len(s), len(n), not only_s and not only_n, dup, cols, cols * len(s), len(diffs), len(only_s), len(only_n),
            "EQUAL" if equal else "DIFFERENT"))
        for k in only_s:
            print("  ONLY IN SERVED: %s -> %s" % (k, s[k]))
        for k in only_n:
            print("  ONLY IN MEMORY: %s -> %s" % (k, n[k]))
        for k, fields in diffs:
            for f in fields:
                print("  DIFF %s field %s: served=%r in-memory=%r" % (k, f, s[k].get(f), n[k].get(f)))
    print("\nAC2 %s" % ("PASS" if all_equal else "FAIL"))
    return 0 if all_equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
