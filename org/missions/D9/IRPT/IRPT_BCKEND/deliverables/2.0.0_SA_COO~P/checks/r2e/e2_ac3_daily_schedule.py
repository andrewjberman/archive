"""~E round 2 AC3 -- the production trigger exists: an EventBridge Scheduler schedule named by the builder,
lib/opal_naming.name("irpt", None, "holdings-performance", "daily") (= irpt-holdings-performance-daily), ENABLED, on a
cron expression, with a target (PRD v0.19 ruling 9; CLAUDE.md: production pipelines MUST be scheduled).

Usage: python e2_ac3_daily_schedule.py
Read-only: scheduler.get_schedule.
"""
import sys
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parents[9]
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402

NAME = opal_naming.name("irpt", None, "holdings-performance", "daily")
ok = True
try:
    s = boto3.client("scheduler").get_schedule(Name=NAME)
    expr, state, target = s.get("ScheduleExpression", ""), s.get("State"), (s.get("Target") or {}).get("Arn")
    print("%s | state %s | %s %s | target %s" % (NAME, state, expr, s.get("ScheduleExpressionTimezone", ""), target))
    ok = state == "ENABLED" and expr.startswith("cron(") and bool(target)
except Exception as exc:
    print("%s | not readable: %s" % (NAME, type(exc).__name__))
    ok = False
if ok:
    print("E2-AC3 PASS")
else:
    print("E2-AC3 FAIL")
sys.exit(0 if ok else 1)
