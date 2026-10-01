"""HVST-ai-2 AC2 (issuer, read-only): the ft session survives a 2-hour collector run with no logout (CTO r35 ruling 4).

Reads `~92/ai2_ft_longevity.json` = {"run_records": [<each ft job's collector run record, verbatim>]}. PASS requires:
- the jobs span at least 120 minutes (earliest started_at to latest finished_at);
- no job status is auth_failed_after_refresh / auth_expired / session_expired, and the jobs' auth_refreshes total 0
  (a renewal means the session was found logged out);
- at least 1 article stored.
"""
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True).stdout.strip()
RECORD = os.path.join(ROOT, "org/missions/D5/AMGT/AMGT_HARVST/deliverables/0.9.0_WK_AMGT_HARVST~92/ai2_ft_longevity.json")
BAD = {"auth_failed_after_refresh", "auth_expired", "session_expired"}


def ts(x):
    return dt.datetime.fromisoformat(str(x).replace("Z", "+00:00"))


def main():
    failures = []
    if not os.path.exists(RECORD):
        print("RECORD: absent (%s)" % RECORD)
        print("AC2 RESULT: FAIL (1 failure(s))")
        print("  FAIL: no ft longevity record")
        return 1
    recs = json.load(open(RECORD, encoding="utf-8")).get("run_records") or []
    starts = [ts(r["started_at"]) for r in recs if r.get("started_at")]
    ends = [ts(r["finished_at"]) for r in recs if r.get("finished_at")]
    span = (max(ends) - min(starts)).total_seconds() / 60 if starts and ends else 0
    refreshes = sum(len(r.get("auth_refreshes") or []) if isinstance(r.get("auth_refreshes"), list)
                    else int(r.get("auth_refreshes") or 0) for r in recs)
    stored = sum(1 for r in recs for o in (r.get("fetch_outcomes") or {}).values() if o.get("outcome") == "stored")
    statuses = [r.get("status") for r in recs]
    print("JOBS %d span %.0f min statuses %s auth_refreshes %d stored %d" % (len(recs), span, statuses, refreshes, stored))
    if span < 120:
        failures.append("span %.0f min < 120" % span)
    if BAD & set(statuses):
        failures.append("an auth-failure status: %s" % sorted(BAD & set(statuses)))
    if refreshes:
        failures.append("%d renewal(s) -- the session was found logged out" % refreshes)
    if stored < 1:
        failures.append("no article stored")
    print("AC2 RESULT: %s (%d failure(s))" % ("PASS" if not failures else "FAIL", len(failures)))
    for f in failures:
        print("  FAIL: " + f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
