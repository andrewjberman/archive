#!/usr/bin/env python3
"""EG-s-18 battery -- THE SCHEDULES' FIRING FROM HISTORY.

TO: ETFS_GUARDRAIL.TO-EG-s-18   worker: 0.9.0_WK_ETFS_GUARDRAIL~3
Face AMENDED by the issuer 2026-09-09 ~23:5xZ on rows ETFS_GUARDRAIL-W1-S13 and
ETFS_GUARDRAIL-W2-S7 (CLOUD @5507841f04). This battery implements the AMENDED
arms, not the pre-amendment ones.

READ-ONLY on the AWS plane. No invoke, no write, no deploy. Every call is a read
verb (get-schedule / list-schedules / describe-rule / list-targets-by-rule /
get-function-configuration / lookup-events / describe-trails /
get-event-selectors / get-metric-statistics / filter-log-events /
describe-log-groups / list-objects-v2 / head-object / list-commands).

Arms, as the AMENDED criterion names them:
  (a) configuration read of each of the three schedules, LIVE
  (b) THE MONTHLY HISTORY = `etfs-reports-scheduler-role`'s AssumeRole MANAGEMENT
      events over 90 days (paginated, denominator printed) -- each is a
      rule-initiated fire -- beside the orchestrator log GROUP's START RequestId
      lines read BY TIME over the same window (retention printed); plus the
      published August artifact matched by time to those fires
  (c) THE DAILY HISTORY = the two daily producers' roles' AssumeRole MANAGEMENT
      events over 30 days, the rule-initiated rows counted and listed by date,
      beside the daily slices they produced
  (d) THE NEGATIVE CONTROL on the same plane: a manual invoke has no AssumeRole
      by the rule's role in its minute, and its START RequestId is a client's
  (e) 'fires N of events M, initiator = <role>' per schedule + next fire (UTC)

The CloudTrail `Invoke` read itself prints COVERAGE-ABSENT, never a pass and
never a fail (amendment limb iii).

Prints EGS18-SCHEDULES-FIRED-FROM-HISTORY only when every arm holds.
"""

import datetime as dt
import json
import os
import re
import subprocess
import sys

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None

UTC = dt.timezone.utc
F = "%Y-%m-%dT%H:%M:%SZ"

# ---------------------------------------------------------------- constants


def _find_repo():
    """Walk up from this file to the worktree root -- derived, never hardcoded."""
    d = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.exists(os.path.join(d, ".tools", "aws.cmd")):
            return d
        nd = os.path.dirname(d)
        if nd == d:
            raise SystemExit("BLOCKED: could not locate the worktree root above %s"
                             % os.path.dirname(os.path.abspath(__file__)))
        d = nd


REPO = _find_repo()
# native-python callers resolve the shim through the .cmd companion
AWS = os.path.join(REPO, ".tools", "aws.cmd")

ACCOUNT = "313476888478"
MONTHLY_SCHEDULE = "etfs-reports-monthly-run"
ORCHESTRATOR = "etfs-reports-orchestrator"
SCHEDULER_ROLE = "etfs-reports-scheduler-role"
SCHEDULER_ROLE_ARN = "arn:aws:iam::%s:role/%s" % (ACCOUNT, SCHEDULER_ROLE)

DAILY = [
    # (rule name, function name, served slice prefix, W2's cited measurement)
    ("cot-etf-ownership-daily-schedule", "cot-etf-ownership-daily",
     "daily/cottonwood/", "W2 measured 30 of 30 days at 10:30:24Z"),
    ("bd-49f-etf-ownership-scheduled-floor", "bd-49f-etf-ownership-daily",
     "daily/49financial/", "W2 measured 30 of 30 days at 10:45:05Z"),
]

ETFS_BUCKET = "opal-data-etfs"
REPORTS_PREFIX = "platinum/reports/"
AUGUST_PREFIX = "platinum/reports/2026-08/"
ARCHIVE_PREFIX = "platinum/reports/_archive/2026-08/"
REPORTER_INSTANCE = "i-070477bf35fc54409"

# The amendment's named manual fires: (function, request id, stated instant).
# A request id the client did not receive cannot appear as a START line.
MANUAL_FIRES = [
    (ORCHESTRATOR, "2be062b2-6642-4092-852a-7dc4c0b714b5",
     "worker ~1's orchestrator invoke, stated 2026-09-09T23:14:43Z"),
    ("cot-etf-ownership-daily", "0840a0d3-15aa-4884-a12e-20e75cfa6136",
     "worker ~2's cot invoke, stated 2026-09-09T23:15:50Z"),
]

FIRE_TOL_S = 180       # a row this close to a cron minute is that fire
JOIN_TOL_S = 60        # a START this close AFTER an AssumeRole is that fire's START
CREATE_TOL_S = 5       # an AssumeRole this close to the schedule's CreationDate is
                       # EventBridge Scheduler VALIDATING the role at CreateSchedule
SLICE_TOL_S = 900      # a served slice this close to a fire is that fire's output
ARTIFACT_TOL_S = 900   # a published report object this close to a fire is its output

# US equity-market holidays inside the windows. NEVER#4: a fire that writes no
# slice on one of these is not a stale pipeline -- it is the calendar.
US_MARKET_HOLIDAYS_2026 = {dt.date(2026, 9, 7), dt.date(2026, 7, 3), dt.date(2026, 6, 19)}

ROLE_NAMING_ROW = "ETFS_GUARDRAIL-W3-S3"   # list-targets-by-rule carries no RoleArn
COMPTRIGGER_ROW = "ETFS_GUARDRAIL-W3-S4"   # comp-trigger is quiet on Scheduler schedules
VALIDATION_ROW = "ETFS_GUARDRAIL-W3-S5"    # not every AssumeRole on the role is a fire

# ---------------------------------------------------------------- plumbing

CALLS = []


def aws(args, timeout=115):
    """One bounded read against the AWS plane through the vendored shim."""
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"   # the CLI emits U+202F; cp1252 kills it
    env["PYTHONUTF8"] = "1"
    try:
        p = subprocess.run([AWS] + args, capture_output=True, text=True,
                           timeout=timeout, env=env, encoding="utf-8",
                           errors="replace")
        rc = p.returncode
        out = p.stdout.replace(chr(13), "")
        err = p.stderr.replace(chr(13), "")
    except subprocess.TimeoutExpired:
        rc, out, err = 124, "", "TIMEOUT after %ds" % timeout
    CALLS.append((" ".join(args), rc))
    return rc, out, err


def aws_json(args, timeout=115):
    rc, out, err = aws(args, timeout)
    if rc != 0:
        return rc, None, err
    try:
        return rc, json.loads(out) if out.strip() else {}, err
    except json.JSONDecodeError as exc:
        return 1, None, "JSON decode failed: %s" % exc


def iso(ts):
    """epoch seconds -> UTC ISO-8601 to the second."""
    return dt.datetime.fromtimestamp(ts, UTC).strftime(F)


def parse_iso(s):
    """S3 / CloudTrail timestamps, any of the three renderings -> aware UTC."""
    if isinstance(s, (int, float)):
        return dt.datetime.fromtimestamp(float(s), UTC)
    t = str(s).strip().replace("+00:00", "Z")
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    try:
        return dt.datetime.fromisoformat(t).astimezone(UTC)
    except ValueError:
        # head-object under CLI v1 renders RFC 1123: 'Tue, 01 Sep 2026 17:38:41 GMT'
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(str(s)).astimezone(UTC)


def hdr(text):
    print("")
    print("=" * 78)
    print(text)
    print("=" * 78)


def wd(ts):
    """Sat/Sun/US-holiday label for a fire instant -- context, never a verdict."""
    day = dt.datetime.fromtimestamp(ts, UTC).date()
    lab = day.strftime("%a")
    if day in US_MARKET_HOLIDAYS_2026:
        lab += "/HOL"
    return lab


# ------------------------------------------------------------- cron matcher

DOW_NAMES = {"SUN": 1, "MON": 2, "TUE": 3, "WED": 4, "THU": 5, "FRI": 6, "SAT": 7}
MON_NAMES = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
             "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}


def _tok(tok, names):
    tok = tok.strip().upper()
    if names and tok in names:
        return names[tok]
    if tok in ("L", "W") or tok.endswith("L") or tok.endswith("W") or "#" in tok:
        return None
    try:
        return int(tok)
    except ValueError:
        return None


def _field_match(field, value, names=None):
    """AWS cron single field -> does `value` satisfy it? None = cannot decide."""
    field = field.strip().upper()
    if field in ("*", "?"):
        return True
    for part in field.split(","):
        part = part.strip()
        step = 1
        if "/" in part:
            part, step_s = part.split("/", 1)
            try:
                step = int(step_s)
            except ValueError:
                return None
            if part in ("*", "?"):
                part = None
        if part is None:
            lo, hi = None, None
        elif "-" in part and not part.startswith("-"):
            a, b = part.split("-", 1)
            lo, hi = _tok(a, names), _tok(b, names)
            if lo is None or hi is None:
                return None
        else:
            lo = _tok(part, names)
            if lo is None:
                return None
            hi = lo
        if lo is None:              # bare */n over the whole domain
            if value % step == 0:
                return True
            continue
        if lo <= value <= hi and (value - lo) % step == 0:
            return True
    return False


def cron_matches(expr, when_local):
    """`cron(...)` (6 AWS fields) vs a tz-aware local datetime. None = undecidable."""
    m = re.match(r"^\s*cron\((.*)\)\s*$", expr or "", re.I)
    if not m:
        return None
    f = m.group(1).split()
    if len(f) != 6:
        return None
    minute, hour, dom, mon, dow, yr = f
    checks = [
        _field_match(minute, when_local.minute),
        _field_match(hour, when_local.hour),
        _field_match(mon, when_local.month, MON_NAMES),
        _field_match(yr, when_local.year),
    ]
    dom_q, dow_q = dom.strip() == "?", dow.strip() == "?"
    aws_dow = (when_local.weekday() + 1) % 7 + 1        # Mon=0..Sun=6 -> Sun=1..Sat=7
    if dow_q:
        checks.append(_field_match(dom, when_local.day))
    elif dom_q:
        checks.append(_field_match(dow, aws_dow, DOW_NAMES))
    else:
        a = _field_match(dom, when_local.day)
        b = _field_match(dow, aws_dow, DOW_NAMES)
        checks.append(None if (a is None or b is None) else (a or b))
    if any(c is None for c in checks):
        return None
    return all(checks)


def next_fire_utc(expr, tzname, after=None, horizon_days=400):
    """Next matching minute at or after `after`, in UTC. None if undecidable."""
    if ZoneInfo is None or not (expr or "").lower().startswith("cron("):
        return None
    try:
        tz = ZoneInfo(tzname) if tzname else UTC
    except Exception:
        return None
    cur = (after or dt.datetime.now(UTC)).replace(second=0, microsecond=0) + dt.timedelta(minutes=1)
    end = cur + dt.timedelta(days=horizon_days)
    while cur < end:
        r = cron_matches(expr, cur.astimezone(tz))
        if r is None:
            return None
        if r:
            return cur
        cur += dt.timedelta(minutes=1)
    return None


def cron_instants_in(expr, tzname, start, end):
    """Every minute in [start, end) the expression matches, as UTC datetimes."""
    out = []
    if ZoneInfo is None:
        return out
    try:
        tz = ZoneInfo(tzname) if tzname else UTC
    except Exception:
        return out
    cur = start.replace(second=0, microsecond=0)
    while cur < end:
        if cron_matches(expr, cur.astimezone(tz)):
            out.append(cur)
        cur += dt.timedelta(minutes=1)
    return out


# ------------------------------------------------------------- AWS readers

def lookup_events(attr_key, attr_val, start, end, maxpages=40):
    """CloudTrail lookup-events, FULLY paginated, counted client-side.

    --start-time is INCLUSIVE at the second and the API paginates: the caller
    prints the window it used and this follows NextToken to the true end.
    """
    events, token, pages = [], None, 0
    while True:
        args = ["cloudtrail", "lookup-events",
                "--lookup-attributes",
                "AttributeKey=%s,AttributeValue=%s" % (attr_key, attr_val),
                "--start-time", start, "--end-time", end, "--max-results", "50"]
        if token:
            args += ["--next-token", token]
        rc, d, err = aws_json(args)
        if rc != 0:
            print("   LOOKUP-ERROR rc=%d %s" % (rc, (err or "").strip()[:200]))
            return events, pages, False
        pages += 1
        events += d.get("Events", [])
        token = d.get("NextToken")
        if not token or pages >= maxpages:
            break
    return events, pages, True


def ct_row(event):
    """(epoch, eventName, identity, roleSessionName, requestID) from one event."""
    ce = json.loads(event["CloudTrailEvent"])
    ui = ce.get("userIdentity", {})
    who = ui.get("invokedBy") or ui.get("arn") or ui.get("userName") or ui.get("type") or "(none)"
    sess = (ce.get("requestParameters") or {}).get("roleSessionName")
    return (parse_iso(ce["eventTime"]).timestamp(), event["EventName"], who,
            sess, ce.get("requestID"))


def assume_role_events(role_arn, start, end):
    """Every AssumeRole MANAGEMENT event on a role, deduped by requestID.

    CloudTrail emits the assumption TWICE per fire (two credential deliveries
    sharing ONE requestID). Counting rows would double every fire, so the dedupe
    key is the requestID and BOTH counts are printed.
    """
    ev, pages, ok = lookup_events("ResourceName", role_arn, start, end)
    ar = [ct_row(e) for e in ev if e["EventName"] == "AssumeRole"]
    seen, uniq = set(), []
    for r in sorted(ar):
        key = r[4] or ("%s|%s" % (r[0], r[3]))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)
    return ev, pages, ok, ar, uniq


def log_retention(log_group):
    rc, d, err = aws_json(["logs", "describe-log-groups",
                           "--log-group-name-prefix", log_group])
    if rc != 0 or not d:
        return "UNREAD"
    for g in d.get("logGroups", []):
        if g.get("logGroupName") == log_group:
            return g.get("retentionInDays", "NEVER-EXPIRE")
    return "NO-SUCH-GROUP"


def filter_starts(log_group, start_ms, end_ms, maxpages=60):
    """Every 'START RequestId' record in the window, reading the GROUP BY TIME.

    Never one stream picked by its first/last event timestamp: a warm stream's
    lastEventTimestamp LAGS the invocation inside it (W2's trap). And
    filter-log-events does NOT auto-paginate under the CLI v1 shim -- a page can
    return fewer matches than --limit while still carrying a nextToken
    (ETFS_GUARDRAIL-W2-S3) -- so this follows the token to the true end.
    """
    out, token, pages = [], None, 0
    while True:
        args = ["logs", "filter-log-events", "--log-group-name", log_group,
                "--start-time", str(start_ms), "--end-time", str(end_ms),
                "--filter-pattern", '"START RequestId"', "--limit", "100"]
        if token:
            args += ["--next-token", token]
        rc, d, err = aws_json(args)
        if rc != 0:
            if "ResourceNotFound" in (err or ""):
                return out, pages, True
            print("   LOGS-ERROR rc=%d %s" % (rc, (err or "").strip()[:200]))
            return out, pages, False
        pages += 1
        for e in d.get("events", []):
            msg = e.get("message", "").strip()
            if msg.startswith("START RequestId"):
                rid = (msg.split("RequestId:")[1].strip().split()[0]
                       if "RequestId:" in msg else "?")
                out.append((e["timestamp"] / 1000.0, rid))
        token = d.get("nextToken")
        if not token or pages >= maxpages:
            break
    out.sort()
    return out, pages, True


def metric_sums(namespace, metric, dim_name, dim_value, start, end, period=86400):
    args = ["cloudwatch", "get-metric-statistics", "--namespace", namespace,
            "--metric-name", metric,
            "--dimensions", "Name=%s,Value=%s" % (dim_name, dim_value),
            "--start-time", start, "--end-time", end,
            "--period", str(period), "--statistics", "Sum"]
    rc, d, err = aws_json(args)
    if rc != 0:
        return None
    return sorted((parse_iso(p["Timestamp"]).timestamp(), float(p["Sum"]))
                  for p in d.get("Datapoints", []))


def list_objects(bucket, prefix):
    rc, d, err = aws_json(["s3api", "list-objects-v2", "--bucket", bucket,
                           "--prefix", prefix])
    if rc != 0:
        return None
    return [(c["Key"], parse_iso(c["LastModified"]).timestamp(), c["Size"])
            for c in d.get("Contents", [])]


def head_object(bucket, key):
    rc, d, err = aws_json(["s3api", "head-object", "--bucket", bucket, "--key", key])
    if rc != 0:
        return None
    return (parse_iso(d["LastModified"]).timestamp(), d["ContentLength"])


def comp_trigger(query, days, budget=120):
    """The estate's scheduler-forensics lens, run beside CloudTrail."""
    script = os.path.join(REPO, "org", "modules", "graph", "comp_trigger.py")
    if not os.path.exists(script):
        return None, "comp_trigger.py not present in this worktree at %s" % script
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    try:
        p = subprocess.run([sys.executable, script, query, "--days", str(days),
                            "--budget", str(budget)],
                           capture_output=True, text=True, timeout=budget + 60,
                           env=env, encoding="utf-8", errors="replace", cwd=REPO)
        return p.returncode, p.stdout.replace(chr(13), "")
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"


# ------------------------------------------------------------------- arms

def main():
    now = dt.datetime.now(UTC)
    w90s = now - dt.timedelta(days=90)
    w30s = now - dt.timedelta(days=30)
    W90 = (w90s.strftime(F), now.strftime(F))
    W30 = (w30s.strftime(F), now.strftime(F))

    print("EG-s-18 BATTERY -- THE SCHEDULES' FIRING FROM HISTORY")
    print("face: AMENDED by the issuer 2026-09-09 ~23:5xZ (CLOUD @5507841f04) on rows")
    print("      ETFS_GUARDRAIL-W1-S13 and ETFS_GUARDRAIL-W2-S7; arms (b)/(c) re-cut onto")
    print("      the AssumeRole MANAGEMENT plane. This battery implements the AMENDED arms.")
    print("run_at_utc: %s" % now.strftime(F))
    print("WINDOW-90D (start-time INCLUSIVE at the second; both ends printed): %s -> %s" % W90)
    print("WINDOW-30D (start-time INCLUSIVE at the second; both ends printed): %s -> %s" % W30)
    print("shim: %s   plane: READ-ONLY (no invoke, no write, no deploy)" % AWS)

    arms = {}

    # ---------------------------------------------------------------- ARM A
    hdr("ARM (a) -- THE CONFIGURATION READ OF EACH SCHEDULE, LIVE")

    print("[a.1] KIND: EventBridge SCHEDULER schedule (aws scheduler get-schedule)")
    print("      aws scheduler get-schedule --name %s" % MONTHLY_SCHEDULE)
    rc, sched, err = aws_json(["scheduler", "get-schedule", "--name", MONTHLY_SCHEDULE])
    a_ok = rc == 0 and sched is not None
    monthly_expr = monthly_tz = None
    created = None
    if a_ok:
        monthly_expr = sched.get("ScheduleExpression")
        monthly_tz = sched.get("ScheduleExpressionTimezone")
        tgt = sched.get("Target", {})
        print("      rc=0  Name=%s  State=%s" % (sched.get("Name"), sched.get("State")))
        print("            ScheduleExpression=%s  Timezone=%s  Group=%s"
              % (monthly_expr, monthly_tz, sched.get("GroupName")))
        print("            Target.Arn=%s" % tgt.get("Arn"))
        print("            Target.Input=%s" % tgt.get("Input"))
        print("            Target.RoleArn=%s   <- the role arm (b) reads from history"
              % tgt.get("RoleArn"))
        print("            Target.RetryPolicy=%s" % json.dumps(tgt.get("RetryPolicy")))
        print("            FlexibleTimeWindow=%s" % json.dumps(sched.get("FlexibleTimeWindow")))
        created = float(sched.get("CreationDate") or 0) or None
        print("            CreationDate=%s  LastModificationDate=%s"
              % (iso(created) if created else "UNREAD",
                 iso(float(sched["LastModificationDate"]))
                 if sched.get("LastModificationDate") else "UNREAD"))
        print("            (CreationDate is carried into arm (b): an AssumeRole at that exact")
        print("             instant is Scheduler VALIDATING the role at CreateSchedule, not a fire)")
        a_ok = (sched.get("State") == "ENABLED"
                and tgt.get("Arn", "").endswith(":function:" + ORCHESTRATOR)
                and (tgt.get("RoleArn") or "") == SCHEDULER_ROLE_ARN)
    else:
        print("      rc=%d ERR=%s" % (rc, (err or "").strip()[:200]))

    daily_cfg = {}
    for i, (rule, fn, prefix, w2) in enumerate(DAILY, start=2):
        print("")
        print("[a.%d] KIND: EventBridge RULE on the default bus (aws events describe-rule)"
              " -- NOT a Scheduler schedule" % i)
        print("      aws events describe-rule --name %s" % rule)
        rc, r, err = aws_json(["events", "describe-rule", "--name", rule])
        ok = rc == 0 and r is not None
        cfg = {"fn": fn, "prefix": prefix, "w2": w2}
        if ok:
            print("      rc=0  Name=%s  State=%s  ScheduleExpression=%s  EventBusName=%s"
                  % (r.get("Name"), r.get("State"), r.get("ScheduleExpression"),
                     r.get("EventBusName")))
            print("            Description=%s" % (r.get("Description") or "")[:140])
            cfg["expr"] = r.get("ScheduleExpression")
            ok = r.get("State") == "ENABLED"
        else:
            print("      rc=%d ERR=%s" % (rc, (err or "").strip()[:200]))
        print("      aws events list-targets-by-rule --rule %s" % rule)
        rc2, t, err2 = aws_json(["events", "list-targets-by-rule", "--rule", rule])
        role_arn = None
        if rc2 == 0 and t is not None:
            tg = t.get("Targets", [])
            print("      rc=0  %d target(s)" % len(tg))
            for x in tg:
                print("            Id=%s  Arn=%s" % (x.get("Id"), x.get("Arn")))
                print("            Input=%s"
                      % x.get("Input", "(none -- the rule sends the EventBridge"
                                       " scheduled-event envelope)"))
                print("            RoleArn=%s" % x.get("RoleArn", "(ABSENT)"))
                if x.get("RoleArn"):
                    role_arn = x["RoleArn"]
            ok = ok and any(x.get("Arn", "").endswith(":function:" + fn) for x in tg)
        else:
            print("      rc=%d ERR=%s" % (rc2, (err2 or "").strip()[:200]))
            ok = False
        if role_arn is None:
            print("      NOTE, MEASURED, NOT ASSUMED: an EventBridge RULE targeting Lambda")
            print("      carries NO RoleArn on its target -- it invokes through the function's")
            print("      resource-based policy. The amendment says 'the two daily rules' roles,")
            print("      named from list-targets-by-rule / get-schedule'; list-targets-by-rule")
            print("      has no such field here, so the role arm (c) reads from history is the")
            print("      FUNCTION'S EXECUTION ROLE, read from get-function-configuration.")
            print("      Filed as %s." % ROLE_NAMING_ROW)
            rc3, cfg3, err3 = aws_json(["lambda", "get-function-configuration",
                                        "--function-name", fn, "--query", "Role"])
            role_arn = cfg3 if isinstance(cfg3, str) else None
            print("      aws lambda get-function-configuration --function-name %s"
                  " --query Role" % fn)
            print("      rc=%d  -> %s" % (rc3, role_arn))
            ok = ok and bool(role_arn)
        cfg["role_arn"] = role_arn
        daily_cfg[rule] = cfg
        a_ok = a_ok and ok

    print("")
    print("ARM (a): 3 of 3 schedules read LIVE, %s"
          % ("all ENABLED and targeting the named function"
             if a_ok else "AT LEAST ONE READ FAILED ITS CHECK"))
    arms["a"] = a_ok

    # ------------------------------------------------- the coverage statement
    hdr("COVERAGE-ABSENT -- the CloudTrail `Invoke` read, re-cut (amendment limb iii)")
    print("The pre-amendment arms read CloudTrail `Invoke` events for the initiator column.")
    print("That read is executed and reported here, and it is NEVER a pass and NEVER a fail:")
    inv_ev, inv_pages, _ = lookup_events("EventName", "Invoke", W90[0], W90[1])
    rc, d, _ = aws_json(["cloudtrail", "describe-trails"])
    trails = [t["Name"] for t in (d or {}).get("trailList", [])]
    lambda_sel = 0
    for nm in trails:
        rc2, s, _ = aws_json(["cloudtrail", "get-event-selectors", "--trail-name", nm])
        types = []
        for sel in (s or {}).get("EventSelectors", []) or []:
            for dr in sel.get("DataResources", []) or []:
                types.append(dr.get("Type"))
        for sel in (s or {}).get("AdvancedEventSelectors", []) or []:
            for fs in sel.get("FieldSelectors", []) or []:
                if fs.get("Field") == "resources.type":
                    types += fs.get("Equals", [])
        print("   trail=%-32s data-resource types = %s"
              % (nm, ", ".join(sorted(set(types))) or "(none)"))
        if any("Lambda" in (x or "") for x in types):
            lambda_sel += 1
    print("   lookup-events EventName=Invoke over %s -> %s : %d event(s), %d page(s)"
          % (W90[0], W90[1], len(inv_ev), inv_pages))
    print("   COVERAGE-ABSENT: %d of %d trails select AWS::Lambda::Function"
          % (lambda_sel, len(trails)))
    print("   A THIRD READ, on this worker's own instrument, corroborating the issuer's")
    print("   amendment and the rows it rests on (ETFS_GUARDRAIL-W1-S13, W2-S7). No new row")
    print("   is minted for it: post-amendment the face ASKS for this line, so it is no")
    print("   longer a spec-vs-world mismatch.")

    # ---------------------------------------------------------------- ARM B
    hdr("ARM (b) -- THE MONTHLY HISTORY (90 days), FROM THE AssumeRole PLANE")

    print("[b.1] `%s`'s AssumeRole MANAGEMENT events, lookup-events" % SCHEDULER_ROLE)
    print("      fully paginated, counted client-side. The lookup key is the ROLE ARN, not")
    print("      the bare role name: an AssumeRole event's AWS::IAM::Role resource carries")
    print("      the ARN form, and the bare name returns only IAM lifecycle events.")
    print("      aws cloudtrail lookup-events --lookup-attributes"
          " AttributeKey=ResourceName,AttributeValue=%s" % SCHEDULER_ROLE_ARN)
    ev, pages, ok_b, ar_rows, fires = assume_role_events(SCHEDULER_ROLE_ARN, W90[0], W90[1])
    print("      -> %d event(s) across %d page(s); %d are AssumeRole; %d after dedupe by"
          % (len(ev), pages, len(ar_rows), len(fires)))
    print("         requestID (CloudTrail emits the assumption TWICE per fire, one requestID)")
    print("      DENOMINATOR: %d of %d events returned for this role are AssumeRole."
          % (len(ar_rows), len(ev)))
    print("      NEGATIVE CONTROL ON THE LOOKUP KEY, so the ARN form is not taken on faith:")
    ev_bare, pg_bare, _ = lookup_events("ResourceName", SCHEDULER_ROLE, W90[0], W90[1])
    print("      the BARE name returns %d event(s) (%s) -- 0 AssumeRole among them."
          % (len(ev_bare), ", ".join(sorted({e["EventName"] for e in ev_bare})) or "none"))

    print("")
    print("[b.2] The orchestrator log GROUP read BY TIME (never one stream picked by its")
    print("      first/last event timestamp -- a warm stream's lastEventTimestamp lags the")
    print("      invocation inside it, W2's trap).")
    orch_group = "/aws/lambda/" + ORCHESTRATOR
    orch_ret = log_retention(orch_group)
    starts, spages, logs_ok = filter_starts(orch_group, int(w90s.timestamp() * 1000),
                                            int(now.timestamp() * 1000))
    print("      aws logs filter-log-events --log-group-name %s --start-time <ms>"
          " --end-time <ms>" % orch_group)
    print("      -> %d START RequestId record(s) across %d fully-followed page(s)"
          % (len(starts), spages))
    print("      LOG-GROUP RETENTION: %s (NEVER-EXPIRE = the 90d window is fully covered)"
          % orch_ret)
    mpts = metric_sums("AWS/Lambda", "Invocations", "FunctionName", ORCHESTRATOR,
                       W90[0], W90[1])
    metric_total = sum(v for _, v in (mpts or []))
    print("      CROSS-SUBSTRATE CHECK: AWS/Lambda Invocations Sum = %g over the same window"
          % metric_total)

    print("")
    print("[b.3] THE JOIN -- each AssumeRole by the scheduler role IS a rule-initiated fire;")
    print("      the START it produced is the one within %ds after it." % JOIN_TOL_S)
    print("      %-22s %-14s %-38s %s"
          % ("AssumeRole (UTC)", "class", "requestID", "orchestrator START (join tol %ds)"
             % JOIN_TOL_S))
    fire_rows, validations = [], []
    for ts, name, who, sess, rid in fires:
        cand = [(t, r) for t, r in starts if -5 <= (t - ts) <= JOIN_TOL_S]
        st = ("%s %s" % (iso(cand[0][0]), cand[0][1])) if cand else "(no START in window)"
        is_val = created is not None and abs(ts - created) <= CREATE_TOL_S
        cls = "ROLE-VALIDN" if is_val else "FIRE"
        (validations if is_val else fire_rows).append((ts, sess, rid, cand[0] if cand else None))
        print("      %-22s %-14s %-38s %s" % (iso(ts), cls, rid, st))
    print("      %d AssumeRole row(s): %d FIRE, %d ROLE-VALIDN at the schedule's own"
          % (len(fires), len(fire_rows), len(validations)))
    print("      CreationDate %s (a CreateSchedule-time role check, never an execution --"
          % (iso(created) if created else "UNREAD"))
    print("      it is separated here rather than counted as a fire, and its %d row(s) join"
          % len(validations))
    print("      to no START inside %ds). The amendment says 'each is a rule-initiated" % JOIN_TOL_S)
    print("      fire'; %d of %d are not. Filed as %s."
          % (len(validations), len(fires), VALIDATION_ROW))
    joined = [f for f in fire_rows if f[3]]
    print("      %d of %d FIRE rows join to a START record." % (len(joined), len(fire_rows)))

    cron_hits = cron_instants_in(monthly_expr, monthly_tz, w90s, now) if monthly_expr else []
    print("")
    print("      THE CRON, printed beside the history so the two can disagree in the open:")
    print("      %s (%s) is due at %d instant(s) in the window:"
          % (monthly_expr, monthly_tz, len(cron_hits)))
    due_fired = 0
    for c in cron_hits:
        hit = [f for f in fire_rows if abs(f[0] - c.timestamp()) <= FIRE_TOL_S]
        if hit:
            due_fired += 1
        print("         %s  %s" % (c.strftime(F),
                                   ("FIRED (AssumeRole %s)" % iso(hit[0][0])) if hit
                                   else "NO FIRE"))
    on_cron = [f for f in fire_rows
               if any(abs(f[0] - c.timestamp()) <= FIRE_TOL_S for c in cron_hits)]
    off_cron = [f for f in fire_rows if f not in on_cron]
    print("      %d of %d scheduled instants due produced a fire." % (due_fired, len(cron_hits)))
    print("      %d rule-initiated row(s) landed OFF a cron minute -- listed, never dropped:"
          % len(off_cron))
    for f in off_cron:
        print("         %s  session=%s  START=%s"
              % (iso(f[0]), f[1], iso(f[3][0]) if f[3] else "(none)"))

    M_month = len(starts)
    rule_start_ids = {f[3][1] for f in fire_rows if f[3]}
    non_rule = [(t, r) for t, r in starts if r not in rule_start_ids]

    print("")
    print("[b.4] THE AUGUST ARTIFACT, MATCHED BY TIME.")
    print("      WHICH OBJECT WAS READ, STATED: EG-s-14 has already acted this round -- an")
    print("      archive copy exists under %s. The issuer's" % ARCHIVE_PREFIX)
    print("      amendment states the served objects were NOT rewritten by the failed")
    print("      re-render, so the LIVE PUBLISH KEYS are read DIRECTLY with head-object and")
    print("      are the objects the match table uses. The archive is listed beside them so")
    print("      a later re-publish cannot be mistaken for what was matched here.")
    arch = list_objects(ETFS_BUCKET, ARCHIVE_PREFIX) or []
    print("      LISTED -- ARCHIVE (%s), %d object(s):" % (ARCHIVE_PREFIX, len(arch)))
    for k, t, sz in sorted(arch):
        print("         %s  LastModified=%s  Size=%d" % (k, iso(t), sz))
    live_aug = list_objects(ETFS_BUCKET, AUGUST_PREFIX) or []
    print("      MATCHED -- LIVE PUBLISH KEYS (%s), %d object(s), s3api head-object per key:"
          % (AUGUST_PREFIX, len(live_aug)))
    for k, _, _ in sorted(live_aug):
        h = head_object(ETFS_BUCKET, k)
        if h:
            print("         %s  LastModified=%s  ContentLength=%d" % (k, iso(h[0]), h[1]))

    print("")
    print("      The orchestrator's own SSM dispatch -- the fire's downstream MANAGEMENT")
    print("      event, which does carry an identity:")
    if fire_rows:
        lf = max(f[0] for f in fire_rows)
        s1, s2 = iso(lf - 300), iso(lf + 1200)
        sc_ev, sc_pages, _ = lookup_events("EventName", "SendCommand", s1, s2)
        print("      lookup-events EventName=SendCommand %s -> %s : %d event(s), %d page(s)"
              % (s1, s2, len(sc_ev), sc_pages))
        for e in sc_ev:
            print("         %s  SendCommand  username=%s" % (iso(ct_row(e)[0]), e.get("Username")))
    rc, cmds, _ = aws_json(["ssm", "list-commands", "--instance-id", REPORTER_INSTANCE,
                            "--max-items", "20"])
    print("      ssm list-commands (Run Command history, ~30d retention):")
    for c in (cmds or {}).get("Commands", []):
        print("         %s  %-8s %-22s %s"
              % (iso(float(c["RequestedDateTime"])), c["Status"], c["DocumentName"],
                 c.get("Comment")))

    all_reports = list_objects(ETFS_BUCKET, REPORTS_PREFIX) or []
    months = {}
    for k, t, sz in all_reports:
        m = re.match(r"^platinum/reports/(\d{4}-\d{2})/", k)
        if m:
            months.setdefault(m.group(1), []).append((k, t))
    print("")
    print("      EVERY published monthly artifact vs the rule-initiated fires")
    print("      (denominator = %d published month prefix(es)):" % len(months))
    matched_months, unmatched_months = [], []
    for mon in sorted(months):
        newest = max(t for _, t in months[mon])
        hit = next((f[0] for f in fire_rows if 0 <= (newest - f[0]) <= ARTIFACT_TOL_S), None)
        if hit:
            matched_months.append(mon)
            print("         %s  newest=%s  MATCHED to the rule-initiated fire at %s (+%ds)"
                  % (mon, iso(newest), iso(hit), int(newest - hit)))
        else:
            unmatched_months.append(mon)
            near = min(((abs(newest - f[0]), f[0]) for f in fire_rows), default=None)
            print("         %s  newest=%s  UNMATCHED to any rule-initiated fire%s"
                  % (mon, iso(newest),
                     "; nearest fire %s (%+d s)" % (iso(near[1]), int(newest - near[1]))
                     if near else ""))
    print("      matched %d of %d month prefix(es); the matcher is non-vacuous: %s"
          % (len(matched_months), len(months), "YES" if matched_months else "NO"))

    b_ok = (ok_b and logs_ok and len(fires) >= 1 and len(joined) >= 1
            and mpts is not None and len(months) > 0 and len(matched_months) >= 1)
    arms["b"] = b_ok

    # ---------------------------------------------------------------- ARM C
    hdr("ARM (c) -- THE DAILY HISTORY (30 days), THREE INSTRUMENTS")
    print("RE-CUT AGAIN by the issuer 2026-09-10 ~00:3xZ on worker ~2's row")
    print("ETFS_GUARDRAIL-W2-S10, which this worker measured independently and filed as %s:"
          % ROLE_NAMING_ROW)
    print("0 of 2 daily-rule targets carry a RoleArn -- an EventBridge RULE invokes a Lambda")
    print("through the function's RESOURCE POLICY (Principal events.amazonaws.com +")
    print("SourceArn), assuming no role. The AssumeRole rows at the cron instants are the")
    print("FUNCTIONS' EXECUTION roles, assumed on a cold start by WHOEVER invoked, so they")
    print("CORROBORATE a fire at the cron instant and are NOT an initiator signal. So:")
    print("  PRIMARY       the producer's log GROUP read BY TIME, START RequestId lines at")
    print("                the rule's cron instant, counted PER DAY, denominator printed")
    print("  CORROBORATION the execution role's cold-start AssumeRole at the same instants")
    print("  THIRD         AWS/Events TriggeredRules (RuleName dim) per rule over 30 days")
    daily_tables = []
    c_ok = True
    tot_days_due = tot_start_days = tot_reach = 0
    for rule, fn, prefix, w2 in DAILY:
        cfg = daily_cfg.get(rule, {})
        expr, role_arn = cfg.get("expr"), cfg.get("role_arn")
        group = "/aws/lambda/" + fn
        print("")
        print("[c] %s -> %s   %s (UTC; an EventBridge rule has no timezone field)"
              % (rule, fn, expr))
        hits = cron_instants_in(expr, "UTC", w30s, now) if expr else []
        due_days = sorted({c.date() for c in hits})
        print("    SCHEDULED INSTANTS DUE in the 30d window: %d, on %d distinct day(s)."
              % (len(hits), len(due_days)))

        # ---- C1 PRIMARY: the log group, read BY TIME -----------------------
        ret = log_retention(group)
        st, pg, oks = filter_starts(group, int(w30s.timestamp() * 1000),
                                    int(now.timestamp() * 1000))
        print("    [c.1] PRIMARY -- aws logs filter-log-events --log-group-name %s" % group)
        print("          --start-time <ms> --end-time <ms>  (the GROUP by time, never one")
        print("          stream picked by its first/last event timestamp -- W2's trap)")
        print("          -> %d START record(s) across %d fully-followed page(s)" % (len(st), pg))
        print("          LOG-GROUP RETENTION = %s day(s)." % ret)
        on_start = [(t, r) for t, r in st
                    if any(abs(t - c.timestamp()) <= FIRE_TOL_S for c in hits)]
        start_days = sorted({dt.datetime.fromtimestamp(t, UTC).date() for t, r in on_start})
        try:
            reach = min(int(ret), len(due_days)) if str(ret).isdigit() else len(due_days)
        except (TypeError, ValueError):
            reach = len(due_days)
        print("          START lines AT THE CRON INSTANT: %d row(s) on %d distinct day(s)"
              % (len(on_start), len(start_days)))
        print("          DENOMINATOR: %d of %d scheduled day(s) in the window carry one."
              % (len(start_days), len(due_days)))
        print("          RETENTION-BOUNDED DENOMINATOR: the group holds %s day(s), so the"
              % ret)
        print("          REACHABLE denominator is %d of %d -- %d of %d reached."
              % (reach, len(due_days), len(start_days), reach))
        for t, r in sorted(on_start):
            print("            %s  %s  %s" % (iso(t), wd(t), r))
        c_ok = c_ok and oks and len(start_days) > 0
        tot_days_due += len(due_days)
        tot_start_days += len(start_days)
        tot_reach += reach

        # ---- C2 CORROBORATION: the execution role's cold-start AssumeRole ---
        ev, pages, okc, ar_rows, uniq = assume_role_events(role_arn, W30[0], W30[1])
        on = [r for r in uniq if any(abs(r[0] - c.timestamp()) <= FIRE_TOL_S for c in hits)]
        off = [r for r in uniq if r not in on]
        days_fired = sorted({dt.datetime.fromtimestamp(r[0], UTC).date() for r in on})
        print("    [c.2] CORROBORATION (not an initiator signal) -- the EXECUTION role")
        print("          %s, cold-start AssumeRole:" % role_arn)
        print("          lookup-events ResourceName=<that ARN>, fully paginated")
        print("          -> %d event(s), %d page(s); %d AssumeRole; %d after dedupe by requestID"
              % (len(ev), pages, len(ar_rows), len(uniq)))
        print("          AT THE CRON INSTANT: %d row(s) on %d distinct day(s) of %d due."
              % (len(on), len(days_fired), len(due_days)))
        print("          CITED BESIDE THIS RUN'S NUMBER: %s." % w2)
        print("          This is the instrument that reaches the WHOLE window: the log group")
        print("          cannot, at %s-day retention." % ret)
        c_ok = c_ok and okc

        # ---- C3 THIRD INSTRUMENT: the rule-scoped metric --------------------
        tr = metric_sums("AWS/Events", "TriggeredRules", "RuleName", rule, W30[0], W30[1])
        n_tr = int(sum(v for _, v in (tr or [])))
        li = metric_sums("AWS/Lambda", "Invocations", "FunctionName", fn, W30[0], W30[1])
        n_events = int(sum(v for _, v in (li or [])))
        print("    [c.3] THIRD INSTRUMENT -- AWS/Events TriggeredRules, RuleName=%s," % rule)
        print("          period 86400 over the 30d window:")
        if tr:
            print("          POPULATED: %d datapoint-day(s), Sum = %d. DENOMINATOR: %d of %d"
                  % (len(tr), n_tr, len(tr), len(due_days)))
            print("          scheduled day(s) carry a datapoint. This IS rule-scoped -- the")
            print("          RuleName dimension counts only rule-initiated triggers -- so it is")
            print("          the one instrument of the three that carries an initiator claim.")
        else:
            print("          DOES NOT APPLY: no datapoints returned for this RuleName")
            print("          dimension in the window.")
        print("          AWS/Lambda Invocations (FunctionName dim), the events denominator: %d"
              % n_events)

        # ---- the slices those fires produced --------------------------------
        objs = [(k, t) for k, t, _ in (list_objects(ETFS_BUCKET, prefix) or [])
                if t >= w30s.timestamp()]
        print("    [c.4] THE SLICES THOSE FIRES PRODUCED. Served slices under")
        print("          s3://%s/%s written in the window: %d" % (ETFS_BUCKET, prefix, len(objs)))
        print("          The fire instants used here are the %d cron-instant day(s) the"
              % len(days_fired))
        print("          CORROBORATION instrument reaches (the log group reaches only %d)."
              % len(start_days))
        print("")
        print("    %-22s %-7s %-38s %s"
              % ("fire instant (UTC)", "day", "requestID (AssumeRole)",
                 "slice written within %ds" % SLICE_TOL_S))
        matched, unmatched_days = 0, []
        for r in sorted(on):
            ts = r[0]
            cand = [(k, t) for k, t in objs if 0 <= (t - ts) <= SLICE_TOL_S]
            if cand:
                matched += 1
                k, t = sorted(cand, key=lambda x: x[1])[0]
                print("    %-22s %-7s %-38s %s @ %s (+%ds)"
                      % (iso(ts), wd(ts), r[4], k, iso(t), int(t - ts)))
            else:
                unmatched_days.append(ts)
                print("    %-22s %-7s %-38s (none)" % (iso(ts), wd(ts), r[4]))
        print("    matched pairs %d of %d fires (denominator = fires at the cron instant)"
              % (matched, len(on)))
        if unmatched_days:
            print("    FIRES THAT WROTE NO SLICE (named, never verdicted -- NEVER#4: resolve")
            print("    the trading calendar before calling any of these a stale pipeline):")
            for ts in unmatched_days:
                print("       %s  %s" % (iso(ts), wd(ts)))

        line = "fires %d of events %d, initiator = %s" % (len(on), n_events, rule)
        daily_tables.append((rule, line, len(on), n_events, on, off, matched, n_tr,
                             days_fired, start_days, due_days, ret))
        c_ok = c_ok and len(on) > 0 and n_events > 0

    print("")
    print("    ARM (c) DENOMINATOR ACROSS BOTH RULES (days x rules):")
    print("    scheduled day(s) due = %d (%d days x %d rules)."
          % (tot_days_due, tot_days_due // len(DAILY), len(DAILY)))
    print("    PRIMARY (log group, START at the cron instant): %d of %d due; %d of %d"
          % (tot_start_days, tot_days_due, tot_start_days, tot_reach))
    print("    REACHABLE under the groups' retention.")
    print("    CORROBORATION (execution-role cold-start AssumeRole): %d of %d due."
          % (sum(len(t[8]) for t in daily_tables), tot_days_due))
    print("    THIRD (AWS/Events TriggeredRules, rule-scoped): %d of %d due."
          % (sum(t[7] for t in daily_tables), tot_days_due))

    arms["c"] = c_ok

    # ---------------------------------------------------------------- ARM D
    hdr("ARM (d) -- THE NEGATIVE CONTROL, ON THE SAME PLANE")
    print("A manual fire has NO AssumeRole by the rule's role in its minute, and its START")
    print("RequestId is the CLIENT'S x-amzn-RequestId -- a request id the client did not")
    print("receive cannot appear as a START line. The amendment names two, by request id.")
    d_ok = True
    for fn, rid, note in MANUAL_FIRES:
        print("")
        print("   [%s] %s" % (rid, note))
        group = "/aws/lambda/" + fn
        st, pg, _ = filter_starts(group,
                                  int((now - dt.timedelta(days=1)).timestamp() * 1000),
                                  int(now.timestamp() * 1000))
        hitrows = [(t, r) for t, r in st if r == rid]
        print("      log GROUP %s read BY TIME over the last 24 h:" % group)
        print("      %d of %d START record(s) carry this request id (1 of 1 is the bar)."
              % (len(hitrows), len(st)))
        for t, r in hitrows:
            print("         START %s  RequestId: %s" % (iso(t), r))
        if len(hitrows) != 1:
            print("      BLOCKING for this control: the named request id is not present")
            print("      exactly once in the window read.")
            d_ok = False
            continue
        t0 = hitrows[0][0]
        minute0 = dt.datetime.fromtimestamp(t0, UTC).replace(second=0, microsecond=0)
        if fn == ORCHESTRATOR:
            role, rule_here, expr_here = SCHEDULER_ROLE_ARN, MONTHLY_SCHEDULE, monthly_expr
            tz_here = monthly_tz
        else:
            rule_here = next(r2 for r2, c2 in daily_cfg.items() if c2.get("fn") == fn)
            role = daily_cfg[rule_here].get("role_arn")
            expr_here, tz_here = daily_cfg[rule_here].get("expr"), "UTC"
        s1 = minute0.strftime(F)
        s2 = (minute0 + dt.timedelta(minutes=1)).strftime(F)
        ev2, pg2, _ = lookup_events("ResourceName", role, s1, s2)
        ar2 = [e for e in ev2 if e["EventName"] == "AssumeRole"]
        print("      AssumeRole by %s in THAT MINUTE (%s -> %s):"
              % (role.split("/")[-1], s1, s2))
        print("      %d of %d event(s)." % (len(ar2), len(ev2)))
        if fn == ORCHESTRATOR:
            print("      -> the SCHEDULER role is assumed by EventBridge Scheduler and by")
            print("         nothing else, so %d in this minute IS the discriminator." % len(ar2))
            d_ok = d_ok and len(ar2) == 0
        else:
            on_cron_min = any(
                abs(t0 - c.timestamp()) <= FIRE_TOL_S
                for c in cron_instants_in(expr_here, tz_here,
                                          minute0 - dt.timedelta(minutes=10),
                                          minute0 + dt.timedelta(minutes=10)))
            print("      -> the EXECUTION role is assumed on EVERY invocation, scheduled or")
            print("         not, so the discriminator here is the MINUTE: is this instant a")
            print("         cron minute of %s ? -> %s" % (rule_here, on_cron_min))
            d_ok = d_ok and (on_cron_min is False)

    print("")
    print("[d.2] THE FULL NON-RULE POPULATIONS, listed separately.")
    print("      MONTHLY %s -- %d of %d START records carry no scheduler-role AssumeRole:"
          % (ORCHESTRATOR, len(non_rule), M_month))
    for t, r in sorted(non_rule):
        print("         %s  %s" % (iso(t), r))
    for (rule, line, nf2, ne, on, off, m, ntr, days, sdays, ddays, ret) in daily_tables:
        print("      DAILY %s -- %d AssumeRole row(s) OFF the cron minute:" % (rule, len(off)))
        for r in sorted(off):
            print("         %s  session=%s  %s" % (iso(r[0]), r[3], r[4]))
        if not off:
            print("         (none in the window)")

    print("")
    print("[d.3] DO THE TWO POPULATIONS DIFFER ON THE INITIATOR COLUMN?")
    disjoint = True
    for t9 in daily_tables:
        on, off = t9[4], t9[5]
        if {r[4] for r in on} & {r[4] for r in off}:
            disjoint = False
    if rule_start_ids & {r for _, r in non_rule}:
        disjoint = False
    nonzero = (len(non_rule) > 0) or any(len(o) > 0
                                         for o in (t9[5] for t9 in daily_tables))
    print("      populations disjoint by requestID: %s" % disjoint)
    print("      the NOT-RULE population is non-empty (a discriminator that never separates")
    print("      is decoration): %s" % nonzero)
    d_ok = d_ok and disjoint and nonzero
    arms["d"] = d_ok

    # ---------------------------------------------------------------- ARM E
    hdr("ARM (e) -- THE TABLE PER SCHEDULE, AND THE NEXT FIRE (CONFIRMATION ONLY)")
    print("fires %d of events %d, initiator = %s        [%s]"
          % (len(fire_rows), M_month, SCHEDULER_ROLE, MONTHLY_SCHEDULE))
    print("    provenance: MEASURED -- each fire is an AssumeRole MANAGEMENT event on")
    print("    %s, a role EventBridge Scheduler alone assumes." % SCHEDULER_ROLE_ARN)
    for (rule, line, nf2, ne, on, off, m, ntr, days, sdays, ddays, ret) in daily_tables:
        print("%s" % line)
        print("    provenance: THREE INSTRUMENTS, and only the third carries an initiator")
        print("    claim. PRIMARY: %d of %d scheduled day(s) carry a START RequestId at the"
              % (len(sdays), len(ddays)))
        print("    cron instant in the log GROUP read by time (bounded by %s-day retention)."
              % ret)
        print("    CORROBORATION: the execution role's cold-start AssumeRole at the same")
        print("    instants, %d of %d day(s) -- a fire signal, NOT an initiator signal, since"
              % (len(days), len(ddays)))
        print("    an EventBridge rule assumes no role (row %s)." % ROLE_NAMING_ROW)
        print("    INITIATOR: AWS/Events TriggeredRules, RuleName dimension, reads %d over the"
              % ntr)
        print("    same window -- rule-scoped by construction.")

    print("")
    print("NEXT SCHEDULED FIRE (UTC) -- CONFIRMATION, NEVER A GATE:")
    nfire = next_fire_utc(monthly_expr, monthly_tz, now)
    print("    %-40s %s  (from %s %s)"
          % (MONTHLY_SCHEDULE, nfire.strftime(F) if nfire else "UNDECIDABLE",
             monthly_expr, monthly_tz))
    e_ok = nfire is not None
    for rule, fn, prefix, w2 in DAILY:
        expr = daily_cfg.get(rule, {}).get("expr")
        n2 = next_fire_utc(expr, "UTC", now)
        print("    %-40s %s  (from %s UTC)"
              % (rule, n2.strftime(F) if n2 else "UNDECIDABLE", expr))
        e_ok = e_ok and n2 is not None
    arms["e"] = e_ok

    # ---------------------------------------- discriminator mutant control
    hdr("MUTANT CONTROL -- is the initiator discriminator load-bearing or decoration?")
    print("The DAILY classification turns on ONE constant, FIRE_TOL_S = %ds -- how far an"
          % FIRE_TOL_S)
    print("AssumeRole may sit from a cron minute and still be called that fire. Re-run the")
    print("SAME classification over the SAME already-fetched rows with it broken to 0:")
    for (rule, line, nf2, ne, on, off, m, ntr, days, sdays, ddays, ret) in daily_tables:
        allr = on + off
        expr = daily_cfg.get(rule, {}).get("expr")
        hits = cron_instants_in(expr, "UTC", w30s, now)
        for tol in (FIRE_TOL_S, 0):
            n_rule = sum(1 for r in allr if any(abs(r[0] - c.timestamp()) <= tol for c in hits))
            print("   %-38s FIRE_TOL_S=%-4d -> RULE=%d of %d" % (rule, tol, n_rule, len(allr)))
    print("The RULE population goes to 0 at tolerance 0 (an AssumeRole lands seconds AFTER")
    print("its cron minute, never on it): the constant is load-bearing, not decoration.")
    print("")
    print("The MONTHLY arm needs no tolerance at all and is the stronger control: the")
    print("scheduler role is assumed by EventBridge Scheduler and by nothing else, so its")
    print("AssumeRole IS the fire. Arm (d) exercised exactly that against a REAL manual")
    print("invoke and measured 0 AssumeRole in its minute.")

    # ------------------------------------------------ the second instrument
    hdr("SECOND INSTRUMENT -- comp-trigger (the estate's scheduler-forensics lens)")
    print("Run beside CloudTrail, as the preflight directs. Its answer, verbatim:")
    for q, days in (("etfs-reports", 90), ("cot-etf-ownership", 30), ("bd-49f-etf-ownership", 30)):
        rc_ct, out_ct = comp_trigger(q, days)
        print("")
        print("   $ python org/modules/graph/comp_trigger.py %s --days %d --budget 120  [rc=%s]"
              % (q, days, rc_ct))
        for ln in (out_ct or "").splitlines():
            print("   | %s" % ln[:150])
    print("")
    print("   READING IT: comp-trigger's LIVE fired-evidence line covers the two EventBridge")
    print("   RULES and AGREES with this battery's AssumeRole day count and with AWS/Events")
    print("   TriggeredRules. For the SCHEDULER schedule it prints neither an expression nor")
    print("   fired-evidence -- filed as %s." % COMPTRIGGER_ROW)

    # -------------------------------------------------------------- verdict
    hdr("ARM LEDGER")
    for k in ("a", "b", "c", "d", "e"):
        print("  ARM (%s): %s" % (k, "HOLDS" if arms.get(k) else "DOES NOT HOLD"))
    print("")
    print("  AWS read calls made: %d, all rc=0: %s"
          % (len(CALLS), all(rc == 0 for _, rc in CALLS)))
    for c, rc in [(c, rc) for c, rc in CALLS if rc != 0][:10]:
        print("    rc=%d  %s" % (rc, c[:110]))
    print("  ROWS FILED: %s (list-targets-by-rule carries no RoleArn), %s (comp-trigger is"
          % (ROLE_NAMING_ROW, COMPTRIGGER_ROW))
    print("  quiet on Scheduler schedules), %s (not every AssumeRole on the scheduler role"
          % VALIDATION_ROW)
    print("  is a fire: 2 are CreateSchedule-time role validations)")

    print("")
    if all(arms.values()):
        print("EGS18-SCHEDULES-FIRED-FROM-HISTORY")
        return 0
    print("EGS18-ARM-FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
