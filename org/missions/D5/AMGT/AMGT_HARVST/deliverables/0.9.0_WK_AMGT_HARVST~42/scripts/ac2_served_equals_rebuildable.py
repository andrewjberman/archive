"""HVST-e-2 AC2: C-HV-GOLD-REBUILDABLE ON THE SERVED PLANE. Rows built IN MEMORY (NEW matcher) from the same inputs
equal the SERVED newest mention and daily snapshots row by row, AND `event_rows` over the newly served mention part
(each row enriched with its article headline off silver, as build_event does) equals the SERVED newest chatter_event
part row by row. S3 GET/LIST only; writes nothing."""
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common as C  # noqa: E402

NEW = C.NEW


def compare(name, served, built, table):
    kf = C.KEYS[table]
    s = {kf(r): C.canon_row(r) for r in served}
    n = {kf(r): C.canon_row(r) for r in built}
    dup = (len(s) != len(served)) or (len(n) != len(built))
    only_s, only_n = sorted(set(s) - set(n)), sorted(set(n) - set(s))
    diffs = [(k, C.diff_fields(s[k], n[k])) for k in sorted(set(s) & set(n)) if C.diff_fields(s[k], n[k])]
    equal = not dup and not only_s and not only_n and not diffs
    cols = len(C.SCHEMAS[table].names)
    print("%-26s %s: served rows=%d rebuilt rows=%d keys equal=%s duplicate keys=%s columns compared=%d fields compared=%d "
          "rows differing=%d only-served=%d only-rebuilt=%d  => %s" % (
              table, name, len(s), len(n), not only_s and not only_n, dup, cols, cols * len(s), len(diffs),
              len(only_s), len(only_n), "EQUAL" if equal else "DIFFERENT"))
    for k in only_s:
        print("  ONLY IN SERVED: %s -> %s" % (k, s[k]))
    for k in only_n:
        print("  ONLY IN REBUILD: %s -> %s" % (k, n[k]))
    for k, fields in diffs:
        for f in fields:
            print("  DIFF %s field %s: served=%r rebuilt=%r" % (k, f, s[k].get(f), n[k].get(f)))
    return equal


def main():
    client = C.store._default_client()
    newest = {t: C.parts(t, client)[-1] for t in C.TABLES}
    served = {t: NEW._latest_gold_snapshot_rows(t, client=client) for t in C.TABLES}
    print("== INPUTS ==")
    for t in C.TABLES:
        print("served newest %-26s %s ETag=%s rows=%d" % (t, C.short(newest[t][0]), newest[t][1], len(served[t])))
    as_of = max(r["day"] for r in served[NEW.GOLD_DAILY_TABLE])
    securities = C.load_securities()
    articles, title_of, hits = C.read_inputs(client)
    print("securities=%d silver articles=%d listing hits=%d ; in-memory daily range %s..%s (the served daily last day)" % (
        len(securities), len(articles), len(hits), NEW.BACKFILL_FLOOR, as_of))
    mem = C.memory(NEW, securities, articles, title_of, hits, as_of)

    print("\n== ROW BY ROW ==")
    ok = compare("in-memory rebuild vs SERVED", served[NEW.GOLD_TABLE], mem[NEW.GOLD_TABLE], NEW.GOLD_TABLE)
    ok &= compare("in-memory rebuild vs SERVED", served[NEW.GOLD_DAILY_TABLE], mem[NEW.GOLD_DAILY_TABLE], NEW.GOLD_DAILY_TABLE)
    enriched = []
    for r in served[NEW.GOLD_TABLE]:
        r = dict(r)
        r["title"] = title_of.get(r.get("article_key"))
        enriched.append(r)
    ev = C.roundtrip(NEW.event_rows(enriched), NEW.GOLD_EVENT_TABLE)
    print("event_rows over the newly served mention part (%d rows, the part %s):" % (
        len(served[NEW.GOLD_TABLE]), C.short(newest[NEW.GOLD_TABLE][0])))
    ok &= compare("event_rows(SERVED mention) vs SERVED", served[NEW.GOLD_EVENT_TABLE], ev, NEW.GOLD_EVENT_TABLE)
    ids = [r["event_id"] for r in served[NEW.GOLD_EVENT_TABLE]]
    print("served event_id: %d rows, %d distinct" % (len(ids), len(set(ids))))
    print("\nAC2 %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
