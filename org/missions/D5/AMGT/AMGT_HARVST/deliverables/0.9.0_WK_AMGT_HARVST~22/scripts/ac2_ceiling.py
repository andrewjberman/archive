"""AC2's CEILING, MEASURED -- run BEFORE the capture and again read after it.

ZERO NETWORK: `universe(config)` reads two local JSON files and the CRO's bulk-pass module
(__main__.py:13-36). Nothing here contacts a vendor or AWS.

It prints, each with its denominator:
  - how many securities `--all-securities` resolves,
  - how many of those carry a usable `sa_symbol` / only a `ticker` / NEITHER,
  - the JOB CAP the invocation's own `--max-jobs` imposes, and which securities that cap selects
    (jobs = securities x publishers, executed from a persistent per-plan cursor: worker.py:332-348),
  - the publisher cooldown rows that could suppress a job.
"""
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.getcwd())

from lib.opal_data_harvest.__main__ import universe
from lib.opal_data_harvest.storage import content_hash

RUNTIME_ROOT = "C:/Users/Opal Bloomberg/Desktop/ajb_workspace/.runtime/opal-data-harvest"
MAX_JOBS = 8
PUBLISHERS = ["sa"]

config = json.loads(open(os.path.join("lib", "opal_data_harvest", "config.json"),
                        encoding="utf-8").read())
securities = universe(config)

n = len(securities)


def usable(value):
    return isinstance(value, str) and value.strip() != ""


with_sa = [s for s in securities if usable(s.get("sa_symbol"))]
without_sa_with_ticker = [s for s in securities
                          if not usable(s.get("sa_symbol")) and usable(s.get("ticker"))]
neither = [s for s in securities
           if not usable(s.get("sa_symbol")) and not usable(s.get("ticker"))]

print("AC2 CEILING, MEASURED (zero network)")
print("--all-securities resolves: %d securities (denominator = universe_source denominator_folders)" % n)
print("  carry a usable sa_symbol : %d of %d" % (len(with_sa), n))
print("  no sa_symbol, has ticker : %d of %d" % (len(without_sa_with_ticker), n))
print("  carry NEITHER            : %d of %d" % (len(neither), n))
print("  SUBTRACTION CHECK: %d + %d + %d = %d (must equal %d)"
      % (len(with_sa), len(without_sa_with_ticker), len(neither),
         len(with_sa) + len(without_sa_with_ticker) + len(neither), n))
# The amendment's "32 carry a ticker" is the WHOLE-POPULATION ticker count, not the disjoint slice
# above; both are printed so the two numbers are not read as a discrepancy.
any_ticker = [s for s in securities if usable(s.get("ticker"))]
both = [s for s in securities if usable(s.get("ticker")) and usable(s.get("sa_symbol"))]
print("  carry a usable ticker, WHOLE POPULATION (the amendment's 32): %d of %d" % (len(any_ticker), n))
print("  of which also carry an sa_symbol: %d -- so ticker-only = %d" % (len(both), len(any_ticker) - len(both)))
print("")

jobs = [(s, p) for s in securities for p in PUBLISHERS]
plan_key = "cursor:" + content_hash(json.dumps([(s["key"], p) for s, p in jobs]))
con = sqlite3.connect("file:%s/progress.sqlite3?mode=ro" % RUNTIME_ROOT, uri=True)
try:
    row = con.execute("SELECT value FROM state WHERE key=?", (plan_key,)).fetchone()
    cursor = int(row[0]) if row else 0
    cooldowns = con.execute("SELECT * FROM cooldown").fetchall()
finally:
    con.close()

print("JOB CAP: jobs = %d securities x %d publisher(s) = %d; --max-jobs %d executes %d of them"
      % (n, len(PUBLISHERS), len(jobs), MAX_JOBS, MAX_JOBS))
print("plan cursor for THIS plan (%s): %d" % (plan_key, cursor))
print("so the invocation ATTEMPTS these %d of %d securities (job order, from the cursor):" % (MAX_JOBS, n))
attempted = []
for i in range(MAX_JOBS):
    security, publisher = jobs[(cursor + i) % len(jobs)]
    attempted.append(security)
    print("  %d. %-22s key=%-24s sa_symbol=%-10r ticker=%-10r identity_status=%r"
          % (i + 1, security.get("company"), security.get("key"), security.get("sa_symbol"),
             security.get("ticker"), security.get("identity_status")))
att_with = [s for s in attempted if usable(s.get("sa_symbol"))]
print("of the %d attempted: %d carry a usable sa_symbol, %d do not"
      % (len(attempted), len(att_with), len(attempted) - len(att_with)))
print("cooldown rows (publisher-level suppressors) in progress.sqlite3: %r" % (cooldowns,))

out = {
    "resolved_denominator": n,
    "with_sa_symbol": len(with_sa),
    "no_sa_symbol_has_ticker": len(without_sa_with_ticker),
    "neither": len(neither),
    "max_jobs": MAX_JOBS,
    "jobs_total": len(jobs),
    "plan_cursor": cursor,
    "attempted_keys": [s["key"] for s in attempted],
    "attempted": [{"key": s["key"], "company": s.get("company"), "sa_symbol": s.get("sa_symbol"),
                   "ticker": s.get("ticker"), "identity_status": s.get("identity_status")}
                  for s in attempted],
    "attempted_with_sa_symbol": [s["key"] for s in att_with],
    "cooldown_rows": cooldowns,
}
path = os.path.join("org", "missions", "D5", "AMGT", "AMGT_HARVST", "deliverables",
                    "0.9.0_WK_AMGT_HARVST~22", "ac2_ceiling.json")
with open(path, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(out, fh, indent=2, sort_keys=True)
print("wrote %s" % path)
