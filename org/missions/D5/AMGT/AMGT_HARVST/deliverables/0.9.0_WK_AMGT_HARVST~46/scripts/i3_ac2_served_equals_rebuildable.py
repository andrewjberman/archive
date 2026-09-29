"""HVST-i-3 AC2 (read-only, S3 LIST/GET only): C-HV-GOLD-REBUILDABLE ON THE SERVED PLANE for chatter_daily. The rows
built IN MEMORY (this cell's securities file, today's silver and listing hits, the producers' own functions) are compared
with the SERVED newest daily part ROW BY ROW: equal keys and every field value, publishers_covered_codes included.
Denominator printed; every difference printed in full."""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i3_common as G  # noqa: E402

C, pg = G.C, G.pg


def main():
    client = G.store._default_client()
    securities = C.load_json(C.NEW_PATH)
    parts = G.list_parts(client)
    key = parts[pg.GOLD_DAILY_TABLE][-1]["key"]
    as_of = G.datetime.date.fromisoformat(G.partition_date(key))
    print("== HVST-i-3 AC2: C-HV-GOLD-REBUILDABLE ON THE SERVED PLANE (chatter_daily) ==")
    print("securities input: %s (%d securities); served newest daily part %s (etag %s); as_of=%s" % (
        os.path.relpath(C.NEW_PATH, C.REPO), len(securities), key, parts[pg.GOLD_DAILY_TABLE][-1]["etag"], as_of))
    articles, hits, _served = C.fetch(client)
    print("inputs: silver articles=%d, listing_hit rows=%d" % (len(articles), len(hits)))
    built, _enriched = C.build_memory(securities, articles, hits, as_of)
    built_rows = built[pg.GOLD_DAILY_TABLE]
    served = G.read_rows(client, key)
    s_by = {G.dkey(r): r for r in served}
    b_by = {G.dkey(r): r for r in built_rows}
    print("served part carries %s: %s; served columns=%d; built columns=%d" % (
        G.NEW_COL, G.NEW_COL in served[0], len(served[0]), len(built_rows[0])))
    print("denominator: served rows=%d (distinct keys %d); built-in-memory rows=%d (distinct keys %d)" % (
        len(served), len(s_by), len(built_rows), len(b_by)))
    only_s = sorted(set(s_by) - set(b_by))
    only_b = sorted(set(b_by) - set(s_by))
    field_diffs = []
    n_fields = 0
    for k in sorted(set(s_by) & set(b_by)):
        n_fields += len(s_by[k])
        fd = C.diff_fields(s_by[k], b_by[k])
        if fd:
            field_diffs.append((k, fd))
    unique = len(s_by) == len(served) and len(b_by) == len(built_rows)
    print("keys equal: %s (served-only %d, built-only %d); rows compared=%d, field values compared=%d, rows with a differing field=%d" % (
        not only_s and not only_b and unique, len(only_s), len(only_b), len(set(s_by) & set(b_by)), n_fields, len(field_diffs)))
    codes_compared = sum(1 for k in set(s_by) & set(b_by) if C.canon(s_by[k].get(G.NEW_COL)) == C.canon(b_by[k].get(G.NEW_COL)))
    print("publishers_covered_codes equal on %d of %d rows" % (codes_compared, len(set(s_by) & set(b_by))))
    for k in only_s:
        print("DIFF served-only key %s: %s" % (k, C.a(C.canon_row(s_by[k]))))
    for k in only_b:
        print("DIFF built-only key %s: %s" % (k, C.a(C.canon_row(b_by[k]))))
    for k, fd in field_diffs:
        for f in fd:
            print("DIFF key %s field %s: served=%s built=%s" % (k, f, C.a(C.canon(s_by[k].get(f))), C.a(C.canon(b_by[k].get(f)))))
    n_diff = len(only_s) + len(only_b) + len(field_diffs) + (0 if unique else 1)
    print("chatter_daily: %s" % ("EQUAL row by row" if n_diff == 0 else "%d DIFFERENCES" % n_diff))
    print("\nAC2 RESULT: %s" % ("PASS" if n_diff == 0 else "FAIL"))
    return 0 if n_diff == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
