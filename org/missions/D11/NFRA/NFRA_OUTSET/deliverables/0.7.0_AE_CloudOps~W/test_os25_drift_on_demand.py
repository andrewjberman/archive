"""O25-AC1 -- THE DRIFT HALF ON DEMAND, proved by the task's own action.

Prints OS25-DRIFT-ON-DEMAND only when every arm passes.

WHAT THIS BATTERY REFUSES TO DO, stated up front because both are how this order nearly went wrong:

  1. IT DOES NOT COMPARE ROW COUNTS. Arm (c) asks whether the artifact's `n` equals the device's
     porcelain count. On the re-run those counts MATCHED WHILE THE SETS DID NOT -- one path had left
     the set and a different one had joined it in the seconds after the publish. A count check
     passes there and reports clean. So the arm compares SETS and attributes every difference to a
     commit or an mtime later than the artifact; an unattributed difference FAILS.

  2. IT DOES NOT RECORD AN ABSENT CLOUDTRAIL RECORD AS "NOT YET". No trail in this account selects
     object-level writes on opal-estate-report, so a PutObject read there can never land. Recording
     that as lag would leave every later reader waiting for something that is not coming. Arm (d)
     reads the identity on the MANAGEMENT plane (AssumeRole), which does exist, and prints the
     object-level plane as COVERAGE-ABSENT with its denominator. Row NFRA_OUTSET-S29, RULED
     @a6be2b52dd.

Author: 0.7.0_AE_CloudOps~W (NFRA_OUTSET OS-s-25). 2026-09-10.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

TASK = "OpalOutsetDriftLaptop"
BUCKET = "opal-estate-report"
DRIFT_KEY = "outset/laptop/comp_heat_drift.json"
ROLE_ARN = "arn:aws:iam::313476888478:role/outset-drift-publisher-laptop"
SESSION_NAME = "outset-drift-laptop"
EXPECTED_PUBLISHER = ("arn:aws:sts::313476888478:assumed-role/"
                      "outset-drift-publisher-laptop/outset-drift-laptop")

# THE RE-RUN this battery grades. Pinned by VersionId so the arm stays reproducible after the
# 11:30Z scheduled fire replaces the key's latest version.
RERUN_START = "2026-09-09T23:58:07Z"
RERUN_VERSION = "3AE8of7Q44VkfbsNNpwWD0EH8lqPj.Sn"

# ARM (e): OS-s-24's manual served day. Filled from that order's own read, never re-derived here.
OS24_REPORT_KEY = "daily/2026/09/10/estate-report-2026-09-10.json"
OS24_REPORT_VERSION = os.environ.get("OS24_REPORT_VERSION", "")

# ARM (a): THE NEVER-FIRED CONFIGURATION READ. Captured at ~2026-09-09T22:54:2xZ, BEFORE the first
# on-demand run. It is EVIDENCE OF RECORD and is deliberately not re-derived: once a task has fired,
# LastTaskResult 267011 and LastRunTime 11/30/1999 cannot be produced again. Pretending otherwise
# would be a fixture that cannot represent the state it claims to score.
ARM_A_RECORD = {
    "captured_at": "2026-09-09T22:54:2xZ (before the first Start-ScheduledTask at 22:54:33Z)",
    "State": "Ready",
    "Enabled": True,
    "Trigger": "MSFT_TaskDailyTrigger DaysInterval=1 StartBoundary=2026-09-09T07:30:00 Enabled=True",
    "TriggerUTC": "07:30 local == 11:30Z (America/New_York, -04:00 on this date)",
    "NextRunTimeUTC": "2026-09-10T11:30:00Z",
    "LastRunTime": "11/30/1999 00:00:00 (the never-fired sentinel)",
    "LastTaskResult": 267011,
    "LastTaskResultMeaning": "SCHED_S_TASK_HAS_NOT_RUN -- 0 runs before",
    "NumberOfMissedRuns": 0,
    "LogonType": "Interactive",
    "StartWhenAvailable": True,
    "ExecutionTimeLimit": "PT1H",
    "DisallowStartIfOnBatteries": False,
}
ARM_A_ACTION = (r"/c cd /d C:\Users\AndrewBerman\Desktop\ajb_workspace && "
                r"C:\Users\AndrewBerman\AppData\Local\Programs\Python\Python312\python.exe "
                r"infra\aws\ec2\outset-drift-device\publish_drift.py "
                r"--out-prefix s3://opal-estate-report/outset")

FAILS: list = []


def fail(arm, msg):
    FAILS.append("%s: %s" % (arm, msg))
    print("  FAIL [%s] %s" % (arm, msg))


def ok(msg):
    print("  OK: %s" % msg)


def repo_root():
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         cwd=os.path.dirname(os.path.abspath(__file__)),
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        print("BLOCKED: not inside a git working tree")
        sys.exit(1)
    return out.stdout.strip()


ROOT = repo_root()


def git(*args):
    out = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True,
                         timeout=180)
    return out.returncode, out.stdout


def ps(cmd):
    out = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", cmd],
                         capture_output=True, text=True, timeout=180)
    return out.returncode, out.stdout.replace("\r", "")


def iso(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


# --------------------------------------------------------------------------- (a)
def arm_a():
    print("\n(a) THE CONFIGURATION READ, rule (4)'s form for a never-fired schedule")
    print("    EVIDENCE OF RECORD, not re-derived -- a fired task cannot produce a never-fired read:")
    for k, v in ARM_A_RECORD.items():
        print("      %-26s %s" % (k, v))
    if ARM_A_RECORD["LastTaskResult"] != 267011:
        fail("a", "the recorded pre-read is not the never-fired sentinel")
        return
    ok("recorded pre-read is the never-fired form (267011, 0 runs)")

    # What IS re-derivable: the installed action line must still be the one that was read.
    rc, out = ps("$t = Get-ScheduledTask -TaskName '%s'; "
                 "Write-Output $t.Actions[0].Execute; Write-Output $t.Actions[0].Arguments" % TASK)
    if rc != 0:
        fail("a", "could not read the installed task (rc=%d)" % rc)
        return
    lines = [x for x in out.split("\n") if x.strip()]
    if len(lines) < 2:
        fail("a", "task action read returned %d line(s), expected 2" % len(lines))
        return
    execu, args = lines[0].strip(), lines[1].strip()
    print("      installed Execute        : %s" % execu)
    if execu != "cmd":
        fail("a", "action Execute is %r, expected 'cmd'" % execu)
    if args != ARM_A_ACTION:
        fail("a", "the installed action string is NOT byte-equal to the recorded line")
        print("      recorded : %s" % ARM_A_ACTION)
        print("      installed: %s" % args)
    else:
        ok("installed action string is BYTE-EQUAL to the line recorded at the pre-read")


# --------------------------------------------------------------------------- (b)
def arm_b():
    print("\n(b) THE TASK'S OWN ACCOUNTING AFTER THE RUN (not the script's)")
    rc, out = ps("$i = Get-ScheduledTaskInfo -TaskName '%s'; "
                 "Write-Output $i.LastTaskResult; "
                 "Write-Output $i.LastRunTime.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'); "
                 "Write-Output $i.NumberOfMissedRuns" % TASK)
    if rc != 0:
        fail("b", "Get-ScheduledTaskInfo rc=%d" % rc)
        return
    vals = [x.strip() for x in out.split("\n") if x.strip()]
    if len(vals) < 3:
        fail("b", "task info returned %d value(s), expected 3" % len(vals))
        return
    result, last_run, missed = vals[0], vals[1], vals[2]
    print("      LastTaskResult : %s" % result)
    print("      LastRunTime UTC: %s" % last_run)
    print("      MissedRuns     : %s" % missed)
    if result != "0":
        fail("b", "LastTaskResult is %s, expected 0" % result)
    else:
        ok("LastTaskResult == 0")
    try:
        if iso(last_run) >= iso(RERUN_START):
            ok("LastRunTime %s is at/after the re-run start %s" % (last_run, RERUN_START))
        else:
            fail("b", "LastRunTime %s precedes the re-run start %s" % (last_run, RERUN_START))
    except ValueError:
        fail("b", "LastRunTime %r is not parseable UTC" % last_run)


# --------------------------------------------------------------------------- (c)
def arm_c(s3):
    print("\n(c) THE ARTIFACT, and its n against the DEVICE")
    head = s3.head_object(Bucket=BUCKET, Key=DRIFT_KEY, VersionId=RERUN_VERSION)
    lm = head["LastModified"].astimezone(timezone.utc)
    print("      VersionId    : %s" % RERUN_VERSION)
    print("      LastModified : %s" % lm.strftime("%Y-%m-%dT%H:%M:%SZ"))
    if lm >= iso(RERUN_START):
        ok("LastModified is at/after the run start %s" % RERUN_START)
    else:
        fail("c", "LastModified precedes the run start")

    body = s3.get_object(Bucket=BUCKET, Key=DRIFT_KEY, VersionId=RERUN_VERSION)["Body"].read()
    art = json.loads(body.decode("utf-8"))
    ts = (art.get("denominators") or {}).get("tool_scalars") or {}
    rows = art.get("rows") or []

    for field, want in (("device", "laptop"), ("publisher_arn", EXPECTED_PUBLISHER)):
        got = ts.get(field)
        if got == want:
            ok("%s == %s" % (field, want))
        else:
            fail("c", "%s is %r, expected %r" % (field, got, want))

    tracked = ts.get("tracked_total") or 0
    if tracked > 0:
        ok("tracked_total %d is non-zero (n=0 would read QUIET, not OUT-OF-CORPUS)" % tracked)
    else:
        fail("c", "tracked_total is %r" % tracked)

    n, nm, nu = ts.get("n"), ts.get("n_modified"), ts.get("n_untracked")
    print("      n=%s  n_modified=%s  n_untracked=%s  len(rows)=%d" % (n, nm, nu, len(rows)))
    if n == (nm or 0) + (nu or 0) == len(rows):
        ok("three internal fields agree on %s" % n)
    else:
        fail("c", "n / n_modified+n_untracked / len(rows) disagree")

    # The S28 fields: both HEAD reads, and the flag.
    print("      git_head_pre=%s @%s" % (ts.get("git_head_pre"), ts.get("git_head_pre_read_at")))
    print("      git_head    =%s @%s" % (ts.get("git_head"), ts.get("git_head_read_at")))
    print("      git_head_moved=%s" % ts.get("git_head_moved"))
    if ts.get("git_head_moved") is True:
        fail("c", "git_head_moved is true -- the stamped head and the rows may differ (S28)")
    elif ts.get("git_head") != ts.get("git_head_pre"):
        fail("c", "the two HEAD reads differ but git_head_moved is not true")
    else:
        ok("both HEAD reads agree and git_head_moved is false")

    # THE SET COMPARISON. Counts are not enough -- see the module docstring.
    art_head = ts.get("git_head")
    art_at = (art.get("vintage") or {}).get("answer_produced_utc")
    rc, live_out = git("status", "--porcelain")
    if rc != 0:
        fail("c", "git status rc=%d" % rc)
        return
    live_rows = [x for x in live_out.split("\n") if x.strip()]
    live = {x[3:].strip().strip('"') for x in live_rows}
    art_paths = {r["path"] for r in rows}
    rc, head_now = git("rev-parse", "--short=12", "HEAD")
    head_now = head_now.strip()
    print("      DENOMINATOR: artifact %d path(s) | device %d porcelain row(s) now"
          % (len(art_paths), len(live_rows)))
    print("      artifact git_head %s | device HEAD now %s" % (art_head, head_now))

    gone = art_paths - live
    new = live - art_paths
    if not gone and not new:
        ok("SET IDENTICAL -- artifact rows are exactly the device's porcelain set")
        return

    # Attribute every difference. A count check would have stopped before this line.
    rc, since = git("log", "--name-only", "--format=@@%h", "%s..HEAD" % art_head)
    committed = set()
    for ln in since.split("\n"):
        ln = ln.strip()
        if ln and not ln.startswith("@@"):
            committed.add(ln)
            parts = ln.split("/")
            for i in range(1, len(parts)):
                committed.add("/".join(parts[:i]) + "/")

    unattributed = []
    for p in sorted(gone):
        if p in committed:
            print("      LEFT  (committed after the artifact) %s" % p)
        else:
            unattributed.append("LEFT " + p)
    for p in sorted(new):
        fp = os.path.join(ROOT, p)
        why = None
        try:
            if os.path.exists(fp):
                m = datetime.fromtimestamp(os.path.getmtime(fp), timezone.utc)
                if art_at and m > iso(art_at):
                    why = m.strftime("%Y-%m-%dT%H:%M:%SZ")
        except OSError:
            why = None
        if why:
            print("      JOINED (mtime %s, after the artifact's %s) %s" % (why, art_at, p))
        else:
            unattributed.append("JOINED " + p)

    if unattributed:
        fail("c", "%d unattributed set difference(s): %s" % (len(unattributed), unattributed[:5]))
    else:
        ok("every set difference attributed to an act LATER than the artifact (%d left, %d joined)"
           % (len(gone), len(new)))


# --------------------------------------------------------------------------- (d)
def arm_d(ct, s3):
    print("\n(d) THE IDENTITY PLANE -- AssumeRole (management), re-cut on row S29")
    start = iso(RERUN_START)
    head = s3.head_object(Bucket=BUCKET, Key=DRIFT_KEY, VersionId=RERUN_VERSION)
    obj_at = head["LastModified"].astimezone(timezone.utc)
    # timedelta, never minute arithmetic: obj_at sits at minute 58 on this run, and a naive
    # `minute + 5` either overflows or (guarded) collapses the window to zero width, which would
    # exclude the very event the arm is looking for and read as a clean absence.
    w0 = start.replace(second=0) - timedelta(minutes=1)
    w1 = obj_at.replace(second=0) + timedelta(minutes=5)
    print("      WINDOW: %s .. %s (printed; --start-time is INCLUSIVE at the second)"
          % (w0.strftime("%Y-%m-%dT%H:%M:%SZ"), w1.strftime("%Y-%m-%dT%H:%M:%SZ")))

    events, token, pages = [], None, 0
    while True:
        kw = {"LookupAttributes": [{"AttributeKey": "EventName", "AttributeValue": "AssumeRole"}],
              "StartTime": w0, "EndTime": w1}
        if token:
            kw["NextToken"] = token
        resp = ct.lookup_events(**kw)
        events.extend(resp.get("Events", []))
        pages += 1
        token = resp.get("NextToken")
        if not token:
            break
    print("      DENOMINATOR: %d AssumeRole event(s) across %d page(s), counted client-side"
          % (len(events), pages))

    def matches(name):
        out = []
        for e in events:
            ce = json.loads(e.get("CloudTrailEvent") or "{}")
            rp = ce.get("requestParameters") or {}
            if rp.get("roleSessionName") == name:
                out.append((ce.get("eventTime"),
                            (ce.get("responseElements") or {}).get("assumedRoleUser", {}).get("arn"),
                            rp.get("roleArn")))
        return out

    hits = matches(SESSION_NAME)
    print("      matching roleSessionName=%s : %d" % (SESSION_NAME, len(hits)))
    if len(hits) != 1:
        fail("d", "expected exactly 1 matching AssumeRole, got %d" % len(hits))
    else:
        t, arn, role = sorted(hits)[0]
        print("        %s  role=%s" % (t, role))
        print("        assumedRoleUser.arn = %s" % arn)
        if arn != EXPECTED_PUBLISHER:
            fail("d", "assumedRoleUser.arn %r != the artifact's publisher_arn" % arn)
        elif role != ROLE_ARN:
            fail("d", "roleArn %r unexpected" % role)
        elif not (start <= iso(t) <= obj_at):
            fail("d", "AssumeRole %s is not bracketed by run start %s and object %s"
                 % (t, RERUN_START, obj_at.strftime("%Y-%m-%dT%H:%M:%SZ")))
        else:
            ok("bracketed: run start %s < assume %s < object %s"
               % (RERUN_START, t, obj_at.strftime("%Y-%m-%dT%H:%M:%SZ")))
            ok("assumedRoleUser.arn is byte-equal to the artifact's publisher_arn -- an instrument "
               "INDEPENDENT of the artifact's own self-report")

    # NEGATIVE CONTROL: the filter must be able to return zero.
    bogus = matches("outset-drift-laptop-NO-SUCH-SESSION")
    if bogus:
        fail("d", "the session-name filter matched a bogus name -- it does not discriminate")
    else:
        ok("NEGATIVE CONTROL: a bogus roleSessionName matches 0 of %d events" % len(events))


def arm_d_coverage(ctc):
    print("\n(d2) THE OBJECT-LEVEL PLANE -- coverage, read live, never recorded as NOT-YET")
    trails = ctc.describe_trails().get("trailList", [])
    stores = ctc.list_event_data_stores().get("EventDataStores", [])
    print("      DENOMINATOR: %d trail(s), %d CloudTrail Lake event data store(s)"
          % (len(trails), len(stores)))
    covering = []
    for t in trails:
        name = t.get("Name")
        try:
            sel = ctc.get_event_selectors(TrailName=name)
        except Exception as exc:                                             # noqa: BLE001
            print("      %-34s selectors unreadable: %s" % (name, type(exc).__name__))
            continue
        blob = json.dumps(sel)
        hit = BUCKET in blob
        print("      %-34s mentions %s: %s" % (name, BUCKET, hit))
        if hit:
            covering.append(name)
    if covering or stores:
        fail("d2", "a trail/store may cover %s -- re-read before printing COVERAGE-ABSENT: %s"
             % (BUCKET, covering))
    else:
        print("      COVERAGE-ABSENT: no data-event trail on %s" % BUCKET)
        ok("recorded as ABSENT COVERAGE, not as NOT-YET (row S29)")


# --------------------------------------------------------------------------- (e)
def arm_e(s3):
    print("\n(e) THE NEGATIVE ARM, read from OS-s-24's manual served day")
    if not OS24_REPORT_VERSION:
        fail("e", "OS24_REPORT_VERSION is not set -- OS-s-24's report has not been read yet. "
                  "This arm is READ FROM that order, never re-derived here.")
        return
    print("      key       : %s" % OS24_REPORT_KEY)
    print("      VersionId : %s" % OS24_REPORT_VERSION)
    body = s3.get_object(Bucket=BUCKET, Key=OS24_REPORT_KEY,
                         VersionId=OS24_REPORT_VERSION)["Body"].read()
    rep = json.loads(body.decode("utf-8"))
    blob = json.dumps(rep)
    devices = {}
    for stage in rep.get("stages", []):
        for k, v in (stage.items() if isinstance(stage, dict) else []):
            if k == "devices" and isinstance(v, dict):
                devices.update(v)
    if not devices:
        # fall back to a scan: the composition may sit deeper in the bundle
        def walk(node):
            if isinstance(node, dict):
                if "device" in node and ("state" in node or "answer_state" in node):
                    devices[str(node.get("device"))] = node
                for vv in node.values():
                    walk(vv)
            elif isinstance(node, list):
                for vv in node:
                    walk(vv)
        walk(rep)
    print("      DENOMINATOR: %d device row(s) found in the served report" % len(devices))
    for name, row in sorted(devices.items()):
        print("        %-14s %s" % (name, json.dumps(row)[:160]))
    if "laptop" not in devices:
        fail("e", "the served report names no `laptop` device row")
    else:
        ok("laptop is present by name in the served group A composition")
    silent = [n for n, r in devices.items()
              if n != "laptop" and ("SILENT" in json.dumps(r).upper()
                                    or "INSTRUMENT_FAILED" in json.dumps(r).upper())]
    if silent:
        ok("NEGATIVE ARM: %d non-reporting device(s) read SILENT/INSTRUMENT_FAILED: %s"
           % (len(silent), silent))
    else:
        fail("e", "no device reads SILENT/INSTRUMENT_FAILED -- the negative arm did not fire, so a "
                  "green here would not discriminate")
    if "laptop" in blob:
        ok("the served report carries the laptop reading")


def main():
    print("O25-AC1 -- THE DRIFT HALF ON DEMAND")
    print("run at %s" % datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    print("repo   %s" % ROOT)
    try:
        import boto3
    except ImportError as e:
        print("BLOCKED: boto3 unavailable (%s). Every world-facing arm needs it." % e)
        return 1
    s3 = boto3.client("s3", region_name="us-east-1")
    ct = boto3.client("cloudtrail", region_name="us-east-1")

    arm_a()
    arm_b()
    arm_c(s3)
    arm_d(ct, s3)
    arm_d_coverage(ct)
    arm_e(s3)

    print("\n" + "=" * 78)
    if FAILS:
        print("FAILED -- %d arm failure(s):" % len(FAILS))
        for f in FAILS:
            print("   %s" % f)
        return 1
    print("OS25-DRIFT-ON-DEMAND")
    return 0


if __name__ == "__main__":
    sys.exit(main())
