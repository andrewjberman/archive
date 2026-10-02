"""DB-7-AC3 -- the reporting-gold root's saved plan creates the function and its schedule at the RECORDED time, 0 destroy.

Reads deliverables/0.9.0_WK_IRPT_DASHBD~1/reporting-gold.plan.txt and REPORTING_GOLD_FIRE_TIME_R3.json. Grades: a
'Plan: N to add, 0 to change, 0 to destroy.' line; an aws_lambda_function named irpt-49f-reporting-gold-lambda is created;
an aws_scheduler_schedule is created whose schedule_expression equals the record's chosen_cron and whose
schedule_expression_timezone is America/New_York. Usage: python <this file> <repo_root>
"""
import json
import re
import sys
from pathlib import Path


def fail(msg):
    print("FAIL: " + msg)
    print("DB-7-AC3 FAIL")
    sys.exit(1)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    d = root / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~1"
    plan, rec = d / "reporting-gold.plan.txt", d / "REPORTING_GOLD_FIRE_TIME_R3.json"
    if not plan.is_file():
        fail("no saved plan at %s" % plan)
    if not rec.is_file():
        fail("no fire-time record at %s" % rec)
    t = plan.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy\.", t)
    if not m:
        fail("no Plan: line")
    if m.group(2) != "0" or m.group(3) != "0":
        fail("plan changes or destroys: %s" % m.group(0))
    if not re.search(r'aws_lambda_function\.this will be created', t) or '"irpt-49f-reporting-gold-lambda"' not in t:
        fail("no creation of irpt-49f-reporting-gold-lambda")
    if "aws_scheduler_schedule" not in t:
        fail("no aws_scheduler_schedule in the plan")
    cron = json.loads(rec.read_text(encoding="utf-8")).get("chosen_cron")
    if not re.search(r'schedule_expression\s+=\s+"%s"' % re.escape(str(cron)), t):
        fail("the plan's schedule_expression is not the record's %r" % cron)
    if not re.search(r'schedule_expression_timezone\s+=\s+"America/New_York"', t):
        fail("the schedule's timezone is not America/New_York")
    print("OK: %s; schedule %s America/New_York" % (m.group(0), cron))
    print("DB-7-AC3 PASS")


if __name__ == "__main__":
    main()
