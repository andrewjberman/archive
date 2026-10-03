"""DB5-1-AC1 -- P-2 measured before it is served: the 49 Financial population, the reporting gold producer over it for one day, the
publisher over it, and the backfill plan, against the Lambda limit.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~1/P2_SCALE_R5.json:
  {"population": {"source": "<builder address>", "accounts": n},
   "producer": {"day": "YYYY-MM-DD", "accounts": n, "rows": r, "seconds": s},
   "publisher": {"days_sampled": k, "accounts": n, "seconds": s, "projected_seconds": x, "lambda_timeout_s": 900},
   "backfill": {"days": d, "projected_hours": h, "plan": "<text>"}}
Grades: population.accounts >= 1000; population.source starts with "s3://" and names "/gold/holdings_performance_daily/";
producer.accounts == population.accounts and producer.rows > 0 and producer.seconds > 0; publisher.accounts == population.accounts and
publisher.seconds > 0 and publisher.projected_seconds > 0 and lambda_timeout_s == 900; backfill.days > 0, backfill.projected_hours > 0
and a non-empty plan. Usage: python <this file> <repo_root>
"""
import json
import sys
from pathlib import Path

REC = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1/P2_SCALE_R5.json"


def fail(msg):
    print("FAIL: " + msg)
    print("DB5-1-AC1 FAIL")
    sys.exit(1)


def num(d, k):
    try:
        return float(d[k])
    except (KeyError, TypeError, ValueError):
        fail("%s is not a number" % k)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    p = root / REC
    if not p.is_file():
        fail("no record at %s" % REC)
    r = json.loads(p.read_text(encoding="utf-8"))
    pop, pro, pub, bf = (r.get(k) or {} for k in ("population", "producer", "publisher", "backfill"))
    n = num(pop, "accounts")
    if n < 1000:
        fail("population.accounts %d is below 1000" % n)
    src = str(pop.get("source", ""))
    if not src.startswith("s3://") or "/gold/holdings_performance_daily/" not in src:
        fail("population.source is not the holdings gold builder address: %r" % src)
    if num(pro, "accounts") != n or num(pro, "rows") <= 0 or num(pro, "seconds") <= 0:
        fail("producer does not cover the population with rows and a time")
    if num(pub, "accounts") != n or num(pub, "seconds") <= 0 or num(pub, "projected_seconds") <= 0:
        fail("publisher does not cover the population with a time and a projection")
    if num(pub, "lambda_timeout_s") != 900:
        fail("publisher.lambda_timeout_s is not 900")
    if num(bf, "days") <= 0 or num(bf, "projected_hours") <= 0 or not str(bf.get("plan", "")).strip():
        fail("backfill lacks days, hours or a plan")
    print("OK: population %d; producer %.0f rows in %.1f s; publisher projected %.0f s against 900; backfill %d days ~%.1f h"
          % (n, num(pro, "rows"), num(pro, "seconds"), num(pub, "projected_seconds"), num(bf, "days"), num(bf, "projected_hours")))
    print("DB5-1-AC1 PASS")


if __name__ == "__main__":
    main()
