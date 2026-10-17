"""IRPT_DASHBD round 138, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the Inflection launcher's BOUNDED DEFAULT (cell DB-f-2602).

  Ruling (CTO msg 10145, item 4 B): without --since the launcher writes only the trading (business) days AFTER the newest day already written at the target prefix, at most the 25
  newest of them; it never writes the whole history; it writes nothing when the target is up to date; an EMPTY target takes the cap of 25, not the whole history. An explicit --since
  is the applier's bounded range and keeps its meaning (every business day from it, no cap).

  The checker drives data/inf/scripts/gold/INF_G_01.account_transaction_gold.py offline, with the launcher test file's FakeS3 and synthetic frames (made-up accounts and symbols).
  Expected day lists are derived from the launcher's own plan() (its business dates), so the checker grades only the WINDOW logic.

  DBF138-2-AC1  an EMPTY target, no --since: run() and main() write exactly the 25 newest business days (and nothing earlier)
  DBF138-2-AC2  a target with a newest written day W: run() writes only the days after W, at most 25 (the 25 newest when more are pending), and nothing at all when W is the newest day
  DBF138-2-AC3  an explicit --since still writes every business day from it with no cap, and a dry run with no --since makes no put_object call yet reports the same bounded days

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import datetime as dt
import sys
from pathlib import Path

CAP = 25
TESTS_REL = "data/inf/scripts/gold/tests"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def weekdays(start, count):
    """`count` weekday ISO dates from `start` (inclusive)."""
    d = dt.date.fromisoformat(start)
    out = []
    while len(out) < count:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out


def expected_window(keys, newest_written, cap=CAP):
    """The days the bounded default writes: the business days after newest_written (all when None), the `cap` newest of them."""
    pend = [k for k in sorted(keys) if newest_written is None or k > newest_written]
    return pend[-cap:]


def load(root):
    sys.path.insert(0, str(Path(root, TESTS_REL)))
    import test_INF_G_01_account_transaction_gold as T  # noqa: E402
    return T


def snapshot_rows(T, days, first_id=1):
    return [T.line(first_id + i, d) for i, d in enumerate(days)]


def build_store(T, snaps):
    """FakeS3 holding cumulative silver snapshots {partition_day: [weekday dates it holds]}."""
    s3 = T.FakeS3()
    for part, days in snaps.items():
        T.put_partition(s3, part, snapshot_rows(T, days))
    return s3


def written_days(T, s3):
    return sorted({d for d, _r in T.emitted(s3)})


def plan_keys(T, days):
    by_day, _ex, _re = T.L.plan(T.frame_of(*snapshot_rows(T, days)))
    return sorted(by_day)


def gold_puts(T, s3):
    return [k for (_b, k) in s3.puts if T.GOLD_KEY in k]


def scenario_days():
    all_days = weekdays("2026-01-05", 45)
    return all_days


def ac1(root):
    T = load(root)
    days = scenario_days()
    keys = plan_keys(T, days)
    need(len(keys) > CAP + 5, "the synthetic snapshot must hold more than %d business days (got %d)" % (CAP, len(keys)))
    want = expected_window(keys, None)
    s3 = build_store(T, {"2026-03-09": days})
    summ = T.L.run(s3, "2026-03-09", upload=True)
    got = written_days(T, s3)
    need(got == want, "run(): an empty target wrote %d day(s) from %s to %s; expected the %d newest, %s to %s"
         % (len(got), got[:1], got[-1:], len(want), want[:1], want[-1:]))
    need(summ["days"] == want, "run() summary days differ from the written days")
    s3b = build_store(T, {"2026-03-09": days})
    rc = T.L.main(["--date", "2026-03-09", "--upload"], s3=s3b)
    need(rc == 0, "main() returned %r" % (rc,))
    need(written_days(T, s3b) == want, "main(): an empty target did not write exactly the 25 newest days (wrote %d)" % len(written_days(T, s3b)))


def ac2(root):
    T = load(root)
    days = scenario_days()
    keys = plan_keys(T, days)
    # (a) W mid-history: an earlier snapshot written in full by an explicit --since, then a later cumulative snapshot, default run
    early = [d for d in days if d <= "2026-02-06"]
    late_part = "2026-03-09"
    s3 = build_store(T, {"2026-02-06": early, late_part: days})
    T.L.run(s3, "2026-02-06", upload=True, since=days[0])
    day_set_before = written_days(T, s3)
    w = day_set_before[-1]
    T.L.run(s3, late_part, upload=True)
    now = written_days(T, s3)
    new = [d for d in now if d > w]
    want = expected_window(keys, w)
    need(want and len(want) <= CAP, "scenario (a) must have 1..%d pending days (got %d)" % (CAP, len(want)))
    need(new == want, "after W=%s the default wrote %s, expected %s" % (w, new[:3], want[:3]))
    need([d for d in now if d <= w] == day_set_before, "days at or before W changed")
    # (b) up to date: the same default run again writes nothing
    puts_before = len(s3.puts)
    summ = T.L.run(s3, late_part, upload=True)
    need(len(s3.puts) == puts_before, "an up-to-date target was written to again (%d new put calls)" % (len(s3.puts) - puts_before))
    need(summ["days"] == [], "an up-to-date run reports days %r" % (summ["days"][:3],))
    # (c) more than 25 pending: W very early, the 25 newest are written, no more
    very_early = days[:3]
    s3c = build_store(T, {"2026-01-07": very_early, late_part: days})
    T.L.run(s3c, "2026-01-07", upload=True, since=days[0])
    wc = written_days(T, s3c)[-1]
    T.L.run(s3c, late_part, upload=True)
    newc = [d for d in written_days(T, s3c) if d > wc]
    wantc = expected_window(keys, wc)
    need(len(wantc) == CAP, "scenario (c) must have more than %d pending days" % CAP)
    need(newc == wantc, "with more than %d pending the default wrote %d day(s), expected the %d newest" % (CAP, len(newc), CAP))


def ac3(root):
    T = load(root)
    days = scenario_days()
    keys = plan_keys(T, days)
    # explicit --since: every business day from it, no cap
    since = keys[3]
    s3 = build_store(T, {"2026-03-09": days})
    T.L.run(s3, "2026-03-09", upload=True, since=since)
    got = written_days(T, s3)
    want = [k for k in keys if k >= since]
    need(len(want) > CAP, "scenario must put more than %d days after --since" % CAP)
    need(got == want, "an explicit --since wrote %d day(s), expected all %d from %s" % (len(got), len(want), since))
    # dry run, no --since: no put_object, the same bounded days reported
    s3d = build_store(T, {"2026-03-09": days})
    summ = T.L.run(s3d, "2026-03-09", upload=False)
    need(not s3d.puts, "a dry run made %d put_object call(s)" % len(s3d.puts))
    need(summ["days"] == expected_window(keys, None), "a dry run with no --since reports %d day(s), expected the %d newest" % (len(summ["days"]), CAP))


def selftest():
    arms = []
    wd = weekdays("2026-01-05", 10)
    arms.append(("weekdays skips weekends", wd[4] == "2026-01-09" and wd[5] == "2026-01-12" and len(wd) == 10))
    keys = weekdays("2026-01-05", 40)
    arms.append(("empty target takes the 25 newest", expected_window(keys, None) == keys[-25:]))
    arms.append(("days after W only", expected_window(keys, keys[34]) == keys[35:]))
    arms.append(("more than the cap takes the newest 25 after W", expected_window(keys, keys[2]) == keys[-25:] and len(expected_window(keys, keys[2])) == 25))
    arms.append(("up to date -> nothing", expected_window(keys, keys[-1]) == []))
    arms.append(("W beyond the data -> nothing", expected_window(keys, "2099-01-01") == []))
    arms.append(("fewer pending than the cap are all taken", len(expected_window(keys, keys[29])) == 10))
    ok = True
    for name, res in arms:
        print(("  ok   " if res else "  FAIL ") + name)
        ok = ok and res
    print("selftest %s (%d arms)" % ("PASS" if ok else "FAIL", len(arms)))
    return 0 if ok else 1


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3 or argv[2] not in ("DBF138-2-AC1", "DBF138-2-AC2", "DBF138-2-AC3"):
        print("usage: p138_bounded.py <repo_root> DBF138-2-AC1|AC2|AC3 | --selftest")
        return 2
    fn = {"DBF138-2-AC1": ac1, "DBF138-2-AC2": ac2, "DBF138-2-AC3": ac3}[argv[2]]
    try:
        fn(argv[1])
    except Fail as e:
        print("reason: " + str(e))
        print(argv[2] + " FAIL")
        return 1
    except SystemExit as e:  # a launcher REFUSED is a FAIL with its words
        print("reason: the launcher refused: %s" % (e,))
        print(argv[2] + " FAIL")
        return 1
    except Exception as e:  # an unreadable or broken input is a FAIL with its cause, never a PASS
        print("reason: %s: %s" % (type(e).__name__, e))
        print(argv[2] + " FAIL")
        return 1
    print(argv[2] + " PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
