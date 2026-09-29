"""HVST-e-1 AC3: C-HV-GOLD-REBUILDABLE for the NEW matcher. Two in-memory builds of mention, daily and event
from the same inputs (the securities file + the landed silver, read once; the second build runs on a deep copy)
equal row by row. S3 GET/LIST only; writes nothing."""
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common as C  # noqa: E402

NEW = C.NEW


def main():
    client = C.store._default_client()
    securities = C.load_securities()
    articles, title_of, hits = C.read_inputs(client)
    served_daily = NEW._latest_gold_snapshot_rows(NEW.GOLD_DAILY_TABLE, client=client)
    as_of = max(r["day"] for r in served_daily)
    print("inputs: securities=%d silver articles=%d listing hits=%d ; daily range %s..%s ; matcher = worktree %s" % (
        len(securities), len(articles), len(hits), NEW.BACKFILL_FLOOR, as_of, C.MODULE_PATH))
    first = C.memory(NEW, securities, articles, title_of, hits, as_of)
    second = C.memory(NEW, securities, articles, title_of, hits, as_of)
    ok = True
    for t in C.TABLES:
        kf = C.KEYS[t]
        x = [C.canon_row(r) for r in first[t]]
        y = [C.canon_row(r) for r in second[t]]
        xi = {kf(r): r for r in x}
        yi = {kf(r): r for r in y}
        only_x, only_y = sorted(set(xi) - set(yi)), sorted(set(yi) - set(xi))
        diffs = [(k, C.diff_fields(xi[k], yi[k])) for k in sorted(set(xi) & set(yi)) if C.diff_fields(xi[k], yi[k])]
        in_order = x == y
        cols = len(C.SCHEMAS[t].names)
        equal = (len(x) == len(y) and not only_x and not only_y and not diffs and in_order
                 and len(xi) == len(x) and len(yi) == len(y))
        ok = ok and equal
        print("%-26s build1 rows=%d build2 rows=%d distinct keys=%d/%d columns=%d fields compared=%d rows differing=%d "
              "only-in-1=%d only-in-2=%d same row order=%s => %s" % (
                  t, len(x), len(y), len(xi), len(yi), cols, cols * len(x), len(diffs), len(only_x), len(only_y),
                  in_order, "EQUAL" if equal else "DIFFERENT"))
        for k in only_x:
            print("  ONLY IN BUILD 1: %s -> %s" % (k, xi[k]))
        for k in only_y:
            print("  ONLY IN BUILD 2: %s -> %s" % (k, yi[k]))
        for k, fields in diffs:
            for f in fields:
                print("  DIFF %s field %s: build1=%r build2=%r" % (k, f, xi[k].get(f), yi[k].get(f)))
    print("AC3 %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
