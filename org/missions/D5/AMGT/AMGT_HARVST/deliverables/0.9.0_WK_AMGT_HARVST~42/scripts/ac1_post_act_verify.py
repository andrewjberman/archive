"""HVST-e-2 AC1 (c)(d)(e), re-run from S3 AFTER the act. `ac1_rebuild_two_tables.py` is write-once (a second run stops at
its own step (a), the BEFORE state having changed); this script reads only. It takes the two parts the act wrote
(named below, from the act's own stdout) and the BEFORE parts (named by the COO half s.3, still on S3, ETags
checked), and prints the same (c) AFTER, (d) moved-rows-against-the-pair and (e) prior-parts checks. S3 GET/LIST only."""
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")
import _common as C  # noqa: E402
import _e2 as E  # noqa: E402

NEW = C.NEW
T_M, T_D, T_E = NEW.GOLD_TABLE, NEW.GOLD_DAILY_TABLE, NEW.GOLD_EVENT_TABLE
# the act's own stdout: the keys build-mention / build-daily reported
WRITTEN = {T_M: "date=2026-09-29/part-20260929T112204Z.parquet", T_D: "date=2026-09-29/part-20260929T112222Z.parquet"}
AS_OF = E.AS_OF_ALLOWED[0]


def main():
    client = C.store._default_client()
    now = E.snapshot(client)
    fails = []
    print("== (c) AFTER, from S3 ==")
    for t in C.TABLES:
        key, etag, size = now[t][-1]
        rows = NEW._latest_gold_snapshot_rows(t, client=client)
        print("%-26s parts=%d newest=%s ETag=%s size=%d rows=%d" % (t, len(now[t]), C.short(key), etag, size, len(rows)))
    for t, want in WRITTEN.items():
        ok = C.short(now[t][-1][0]) == want
        print("newest %s is the part the act wrote (%s): %s" % (t, want, ok))
        if not ok:
            fails.append("newest %s is not the written part" % t)
    be = E.BEFORE_EXPECT[T_E]
    ev_ok = (len(now[T_E]), C.short(now[T_E][-1][0]), now[T_E][-1][1], len(NEW._latest_gold_snapshot_rows(T_E, client=client))) == be
    print("newest event part unchanged = the COO half s.3 newest (%s): %s" % (be, ev_ok))
    if not ev_ok:
        fails.append("event part changed")

    def part(table, short_key):
        return next(p for p in now[table] if C.short(p[0]) == short_key)

    before_parts = {t: [p for p in now[t] if C.short(p[0]) != WRITTEN.get(t)] for t in C.TABLES}
    for t in (T_M, T_D):
        newest_before = before_parts[t][-1]
        want = E.BEFORE_EXPECT[t]
        ok = (len(before_parts[t]), C.short(newest_before[0]), newest_before[1]) == want[:3]
        print("BEFORE %s reconstructed: parts=%d newest=%s ETag=%s == COO half s.3 %s : %s" % (
            t, len(before_parts[t]), C.short(newest_before[0]), newest_before[1], want[:3], ok))
        if not ok:
            fails.append("BEFORE part of %s not as the half states" % t)

    print("\n== (d) MOVED ROWS against the pair (BEFORE newest part vs the part the act wrote) ==")
    titles = {r.get("article_key"): r.get("title") for r in NEW._iter_latest_articles(client=client)}
    b_m = E.rows_of(before_parts[T_M][-1][0], client)
    a_m = E.rows_of(part(T_M, WRITTEN[T_M])[0], client)
    b_d = E.rows_of(before_parts[T_D][-1][0], client)
    a_d = E.rows_of(part(T_D, WRITTEN[T_D])[0], client)
    o_m, l_m = E.check_mention(b_m, a_m, titles)
    o_d, l_d = E.check_daily(b_d, a_d, AS_OF)
    print("-- article_security_mention (COO half s.4.1) --")
    for s in l_m:
        print(s)
    print("-- chatter_daily (COO half s.4.2) --")
    for s in l_d:
        print(s)
    for s in o_m + o_d:
        print("OUTSIDE THE PAIR: %s" % s)
    print("OUTSIDE THE PAIR rows/counts: %d" % (len(o_m) + len(o_d)))
    fails += o_m + o_d

    print("\n== (e) every prior part still exists with its ETag unchanged ==")
    print("(the act's own BEFORE listing is not on S3; the prior parts are every part but the two written, and each is present now; "
          "their ETags are the ones printed here -- the newest-before ETags equal the COO half s.3 values checked above)")
    for t in C.TABLES:
        print("%-26s prior parts present=%d (parts now=%d, written by the act=%d)" % (
            t, len(before_parts[t]), len(now[t]), len(now[t]) - len(before_parts[t])))
        for k, etag, size in before_parts[t]:
            print("   %s ETag=%s size=%d" % (C.short(k), etag, size))
    print("\nS3 KEYS WRITTEN BY THE ACT:")
    for t in (T_M, T_D):
        k, etag, size = part(t, WRITTEN[t])
        print("  %s ETag=%s size=%d" % (k, etag, size))
    for f in fails:
        print("FAIL: %s" % f)
    print("AC1-POST-ACT %s" % ("PASS" if not fails else "FAIL"))
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
