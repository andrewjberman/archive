"""AMGT_RESAPP round-101 PREP -- the /freshness snapshot is current by the TRADING CALENDAR, not by a 24-hour clock (CTO round-100 analysis ADDENDUM 1, msg 4292).

  PYTHONPATH=<repo root> python r101_snapshot_rule_check.py

The writer is `cron(30 12 ? * MON-FRI *)` (infra/aws/terraform/harvest/freshness-snapshot-schedule.tf); the reader (`lib/research/freshness/snapshot.py::read_freshness_snapshot`) refused a
snapshot older than 24 hours, so from Saturday 12:30Z to Monday 12:30Z every request after the 60-second hold recomputed the whole view live. The rule asked for: a snapshot is current
when it was written at or after the latest trading day's scheduled write (12:30 UTC of the latest trading day, `lib/trading_calendar`, whose 12:30 has passed at `now`): Friday's covers the
weekend and a holiday Monday; a weekday past its write with no new snapshot is NOT current (the caller recomputes). A calendar that cannot answer falls back to the old 24-hour rule and
never raises. Each arm calls the real `read_freshness_snapshot` with a stub client and an injected `now`; read-only, no S3, no network.
    A1 Sunday 15:00Z, snapshot Friday 12:30Z                         -> served
    A2 Monday 11:00Z (before its write), snapshot Friday 12:30Z      -> served
    A3 Monday 13:00Z (past its write), snapshot Friday 12:30Z        -> NOT served, the reason names the scheduled write
    A4 Monday 15:00Z, snapshot Monday 12:30Z                         -> served
    A5 Tuesday 12:00Z, snapshot Monday 12:30Z                        -> served
    A6 Tuesday 13:00Z, snapshot Monday 12:30Z                        -> NOT served
    A7 Tuesday 2026-09-08 11:00Z, snapshot Friday 2026-09-04 12:30Z (Monday the 7th a holiday) -> served; at 13:00Z -> NOT served
    A8 a date far outside the calendar's table (2099): no exception, whichever source answers: served at 4 hours, NOT served at 52 hours
    A9 a snapshot with no readable `generated_at` -> NOT served, as before
Prints one line per arm and `R101 SNAPSHOT RULE: YES|NO` (exit 0|1). At the base: A1, A2 and A7 (the first half) FAIL; the rest PASS.
"""
import datetime
import json
import sys

from lib.research.freshness import snapshot


class _Body:
    def __init__(self, raw):
        self._raw = raw

    def read(self):
        return self._raw


class _Client:
    def __init__(self, generated_at):
        self._doc = {"rows": [], "generated_at": generated_at}

    def get_object(self, Bucket, Key):  # noqa: N803 -- the boto3 signature
        return {"Body": _Body(json.dumps(self._doc).encode("utf-8"))}


def served(generated_at, now):
    document, record = snapshot.read_freshness_snapshot(_Client(generated_at), now=datetime.datetime.fromisoformat(now))
    return document is not None, record


def main():
    results = []

    def arm(label, generated_at, now, want_served, reason_has=None):
        try:
            got, record = served(generated_at, now)
            ok = got == want_served and (reason_has is None or reason_has in str(record.get("reason")))
            detail = "served=%s age=%s reason=%s" % (got, record.get("age_hours"), str(record.get("reason"))[:70])
        except Exception as exc:  # the reader never raises
            ok, detail = False, "RAISED %s: %s" % (type(exc).__name__, exc)
        print("%s %-4s %-58s %s" % ("PASS" if ok else "FAIL", label, "snapshot %s, now %s" % (generated_at, now), detail))
        results.append(ok)

    arm("A1", "2026-10-09T12:30Z", "2026-10-11T15:00:00", True)
    arm("A2", "2026-10-09T12:30Z", "2026-10-12T11:00:00", True)
    arm("A3", "2026-10-09T12:30Z", "2026-10-12T13:00:00", False, "scheduled write")
    arm("A4", "2026-10-12T12:30Z", "2026-10-12T15:00:00", True)
    arm("A5", "2026-10-12T12:30Z", "2026-10-13T12:00:00", True)
    arm("A6", "2026-10-12T12:30Z", "2026-10-13T13:00:00", False)
    arm("A7a", "2026-09-04T12:30Z", "2026-09-08T11:00:00", True)
    arm("A7b", "2026-09-04T12:30Z", "2026-09-08T13:00:00", False)
    arm("A8a", "2099-01-01T01:00Z", "2099-01-01T05:00:00", True)
    arm("A8b", "2098-12-30T01:00Z", "2099-01-01T05:00:00", False)
    arm("A9", "not a time", "2026-10-12T13:00:00", False)
    print("   arms passed %d of %d" % (sum(1 for r in results if r), len(results)))
    ok = all(results)
    print("R101 SNAPSHOT RULE: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
