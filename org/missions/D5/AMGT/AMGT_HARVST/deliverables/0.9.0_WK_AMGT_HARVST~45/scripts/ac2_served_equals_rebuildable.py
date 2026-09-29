"""HVST-g-2 AC2 (read-only, S3 LIST/GET only): C-HV-GOLD-REBUILDABLE ON THE SERVED PLANE. For each of the three
tables the rows built IN MEMORY (this cell's securities file, today's silver, the producers' own functions) are
compared with the SERVED newest snapshot ROW BY ROW: equal keys and every field value. Denominator per table;
every difference printed in full."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import g2_common as G  # noqa: E402

C, pg = G.C, G.pg

KEYS = {
    pg.GOLD_TABLE: lambda r: (r["article_key"], r["security_key"]),
    pg.GOLD_DAILY_TABLE: lambda r: (r["security_key"], r["day"].isoformat() if hasattr(r["day"], "isoformat") else r["day"]),
    pg.GOLD_EVENT_TABLE: lambda r: (r["event_id"],),
}


def main():
    client = G.store._default_client()
    securities = C.load_json(C.NEW_PATH)
    parts = G.list_parts(client)
    served_keys = {t: parts[t][-1]["key"] for t in G.TABLES}
    as_of = G.datetime.date.fromisoformat(G.partition_date(served_keys[pg.GOLD_DAILY_TABLE]))
    print("== HVST-g-2 AC2: C-HV-GOLD-REBUILDABLE ON THE SERVED PLANE ==")
    print("securities input: %s (%d securities); as_of (the served daily part's date= partition)=%s" % (
        os.path.relpath(C.NEW_PATH, C.REPO), len(securities), as_of))
    articles, hits, _served = C.fetch(client)
    print("inputs: silver articles=%d, listing_hit rows=%d" % (len(articles), len(hits)))
    built, _enriched = C.build_memory(securities, articles, hits, as_of)
    total_diff = 0
    for t in G.TABLES:
        served = G.read_rows(client, served_keys[t])
        key = KEYS[t]
        s_by = {key(r): r for r in served}
        b_by = {key(r): r for r in built[t]}
        print("\n-- %s: served newest %s" % (t, served_keys[t]))
        print("   denominator: served rows=%d (distinct keys %d); built-in-memory rows=%d (distinct keys %d)" % (
            len(served), len(s_by), len(built[t]), len(b_by)))
        only_s = sorted(set(s_by) - set(b_by))
        only_b = sorted(set(b_by) - set(s_by))
        field_diffs = []
        n_fields = 0
        for k in sorted(set(s_by) & set(b_by)):
            n_fields += len(s_by[k])
            fd = C.diff_fields(s_by[k], b_by[k])
            if fd:
                field_diffs.append((k, fd))
        in_order = [key(r) for r in served] == [key(r) for r in built[t]]
        print("   keys equal: %s (served-only %d, built-only %d); rows compared=%d, field values compared=%d, rows with a differing field=%d" % (
            not only_s and not only_b and len(s_by) == len(served) and len(b_by) == len(built[t]),
            len(only_s), len(only_b), len(set(s_by) & set(b_by)), n_fields, len(field_diffs)))
        print("   (informational) row ORDER identical: %s -- order is not part of the contract" % in_order)
        for k in only_s:
            print("   DIFF served-only key %s: %s" % (k, C.a(C.canon_row(s_by[k]))))
        for k in only_b:
            print("   DIFF built-only key %s: %s" % (k, C.a(C.canon_row(b_by[k]))))
        for k, fd in field_diffs:
            for f in fd:
                print("   DIFF key %s field %s: served=%s built=%s" % (k, f, C.a(C.canon(s_by[k].get(f))), C.a(C.canon(b_by[k].get(f)))))
        n_diff = len(only_s) + len(only_b) + len(field_diffs) + (0 if len(s_by) == len(served) and len(b_by) == len(built[t]) else 1)
        total_diff += n_diff
        print("   %s: %s" % (t, "EQUAL row by row" if n_diff == 0 else "%d DIFFERENCES" % n_diff))
    print("\nAC2 RESULT: %s" % ("PASS" if total_diff == 0 else "FAIL"))
    return 0 if total_diff == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
