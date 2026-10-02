"""HVST-aj-4 AC2 (issuer, read-only): the ft keep-alive run holds a session for 120 min with one keep-alive event per
page load (round-36 analysis ruling 5; CTO 28235).

Reads `org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/aj4_ft_keepalive.json`
= {"run_records": [<each ft job's run record, verbatim>]}. PASS requires:
- the jobs span >= 120 min (first started_at to last finished_at);
- no job status in {sign_in_refused, auth_failed_after_refresh, auth_expired} and auth_refreshes == 0 on every job;
- every run record carries `events` with event == "keepalive_page_load", and the gap between consecutive keep-alive
  events inside one job never exceeds 2 x the contract cadence (session_keepalive_seconds, default 300 s).
"""
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
F = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/aj4_ft_keepalive.json")
BAD = {"sign_in_refused", "auth_failed_after_refresh", "auth_expired"}


def ts(s):
    t = dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    return t if t.tzinfo else t.replace(tzinfo=dt.timezone.utc)


def cadence():
    try:
        with open(os.path.join(ROOT, "lib/opal_data_harvest/contracts.json"), encoding="utf-8") as fh:
            c = json.load(fh)
        return int(((c.get("publishers") or c).get("ft") or {}).get("session_keepalive_seconds") or 300)
    except Exception:
        return 300


def main():
    failures = []
    if not os.path.exists(F):
        print("RECORD: absent (%s)" % F)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no aj-4 run record file")
        return 1
    with open(F, encoding="utf-8") as fh:
        recs = json.load(fh).get("run_records") or []
    limit = 2 * cadence()
    starts, ends, kas = [], [], 0
    for r in recs:
        starts.append(ts(r.get("started_at")))
        ends.append(ts(r.get("finished_at")))
        for j in r.get("jobs") or []:
            if j.get("status") in BAD:
                failures.append("job %s status %s" % (r.get("run_id"), j.get("status")))
            if (j.get("auth_refreshes") or 0) != 0:
                failures.append("job %s auth_refreshes %s" % (r.get("run_id"), j.get("auth_refreshes")))
        times = sorted(ts(e.get("at")) for e in (r.get("events") or []) if e.get("event") == "keepalive_page_load")
        kas += len(times)
        if not times:
            failures.append("run %s carries no keepalive_page_load event" % r.get("run_id"))
        for a, b in zip(times, times[1:]):
            if (b - a).total_seconds() > limit:
                failures.append("run %s keep-alive gap %d s > %d s" % (r.get("run_id"), (b - a).total_seconds(), limit))
                break
    span = ((max(ends) - min(starts)).total_seconds() / 60.0) if recs else 0.0
    print("JOBS %d span %.0f min keepalive_events %d cadence %d s" % (len(recs), span, kas, cadence()))
    if span < 120:
        failures.append("span %.0f min < 120" % span)
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
