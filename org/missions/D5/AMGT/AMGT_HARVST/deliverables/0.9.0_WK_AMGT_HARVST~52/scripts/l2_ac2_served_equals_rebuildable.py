"""HVST-l-2 AC2 (read-only, S3 LIST/GET only): C-HV-GOLD-REBUILDABLE ON THE SERVED PLANE for chatter_event. The event
rows built IN MEMORY from the same inputs build_event reads (the newest mention part, each row's headline off silver,
event_rows under the merged rule) are compared with the SERVED newest event part ROW BY ROW, every field. Denominator
printed; every difference printed in full."""
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l2_common as G  # noqa: E402

C, pg = G.C, G.pg


def main():
    client = G.store._default_client()
    parts = G.list_parts(client)
    newest = parts[pg.GOLD_EVENT_TABLE][-1]
    print("== HVST-l-2 AC2: C-HV-GOLD-REBUILDABLE ON THE SERVED PLANE (chatter_event) ==")
    print("served newest event part %s (etag %s)" % (newest["key"], newest["etag"]))
    m_newest = parts[pg.GOLD_TABLE][-1]
    mention = pg._latest_gold_snapshot_rows(pg.GOLD_TABLE, client=client)
    titles = pg._headline_by_article_key(client=client)
    print("inputs: newest mention part %s (etag %s) rows=%d; silver headlines=%d; rule EVENT_GUARD_CO_MENTIONS=%s"
          % (m_newest["key"], m_newest["etag"], len(mention), len(titles), pg.EVENT_GUARD_CO_MENTIONS))
    enriched = []
    for row in mention:
        row = dict(row)
        row["title"] = titles.get(row.get("article_key"))
        enriched.append(row)
    built = C.roundtrip(pg.event_rows(enriched), pg.GOLD_EVENT_TABLE)
    served = G.read_rows(client, newest["key"])
    s_by = {r["event_id"]: r for r in served}
    b_by = {r["event_id"]: r for r in built}
    unique = len(s_by) == len(served) and len(b_by) == len(built)
    print("denominator: served rows=%d (distinct event_ids %d); built-in-memory rows=%d (distinct event_ids %d)" % (
        len(served), len(s_by), len(built), len(b_by)))
    only_s = sorted(set(s_by) - set(b_by))
    only_b = sorted(set(b_by) - set(s_by))
    field_diffs = []
    n_fields = 0
    for k in sorted(set(s_by) & set(b_by)):
        n_fields += len(s_by[k])
        fd = C.diff_fields(s_by[k], b_by[k])
        if fd:
            field_diffs.append((k, fd))
    order_equal = [r["event_id"] for r in served] == [r["event_id"] for r in built]
    print("event_ids equal: %s (served-only %d, built-only %d); rows compared=%d, field values compared=%d, rows with a differing field=%d; row order equal: %s" % (
        not only_s and not only_b and unique, len(only_s), len(only_b), len(set(s_by) & set(b_by)), n_fields, len(field_diffs), order_equal))
    for k in only_s:
        print("DIFF served-only event_id %s: %s" % (k, C.a(C.canon_row(s_by[k]))))
    for k in only_b:
        print("DIFF built-only event_id %s: %s" % (k, C.a(C.canon_row(b_by[k]))))
    for k, fd in field_diffs:
        for f in fd:
            print("DIFF event_id %s field %s: served=%s built=%s" % (k, f, C.a(C.canon(s_by[k].get(f))), C.a(C.canon(b_by[k].get(f)))))
    n_diff = len(only_s) + len(only_b) + len(field_diffs) + (0 if unique else 1) + (0 if order_equal else 1)
    print("chatter_event: %s" % ("EQUAL row by row" if n_diff == 0 else "%d DIFFERENCES" % n_diff))
    print("\nAC2 RESULT: %s" % ("PASS" if n_diff == 0 else "FAIL"))
    return 0 if n_diff == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
