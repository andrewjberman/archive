#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-24 -- S24-AC1 battery (face HARDENED @e618f3f88d).

EVERY CODE ARM READS THE DEPLOYED BYTES. The function's own code zip is fetched from
`lambda:GetFunction`'s presigned `Code.Location`, its member hashed, and the module
imported from THAT text with every boto3 client replaced by a stub that RAISES -- so no
AWS call is reachable through the module under test.

Six arms (a)-(f), plus the four hardened conditions, each measured and each printing its
denominator. Prints EGS24-FORCING-THREADED-SCHEDULE-CLEAN only when all of them hold.

NO SEND AND NO ORCHESTRATOR INVOCATION. Every AWS call is a read.
"""
from __future__ import annotations

import ast
import base64
import datetime
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import urllib.request
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
FUNCTION = "etfs-reports-orchestrator"
REGION = "us-east-1"
SOURCE_REL = "infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py"
PRE_CHANGE_PIN = "0228b9c456"
PRE_CHANGE_SHA256 = "ac0484b73a26865eab649917cec7d1bf9c5d604ccd293cc72f17cb83e9e17000"
ENTRY = os.path.join(REPO_ROOT, "org", "critical_paths", "change_management",
                     "20260910T0538Z_etfs-guardrail-eg-s-24-forcing-seam-hardened"
                     "_deploy_completion.md")
PLAN_TRANSCRIPT = os.path.join(HERE, "EG-s-24_preapply_plan_transcript.txt")
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "ec2/etfs-reports/render_month_end.py"

ARMS, FAILS = {}, []


def hold(arm, ok, why):
    ARMS[arm] = bool(ok)
    if not ok:
        FAILS.append(arm)
    print("  [%s] %s -- %s" % ("HOLD" if ok else "FAIL", arm, why))


def head(t):
    print("")
    print("=" * 78)
    print(t)
    print("=" * 78)


_lam = boto3.client("lambda", region_name=REGION)
_s3 = boto3.client("s3", region_name=REGION)
_logs = boto3.client("logs", region_name=REGION)
_sched = boto3.client("scheduler", region_name=REGION)

# =====================================================================================
head("0. THE SUBJECT: the DEPLOYED orchestrator")
# =====================================================================================
fn = _lam.get_function(FunctionName=FUNCTION)
CONF = fn["Configuration"]
zip_bytes = urllib.request.urlopen(fn["Code"]["Location"]).read()
SRC = zipfile.ZipFile(io.BytesIO(zip_bytes)).read("lambda_function.py")
TEXT = SRC.decode("utf-8")
SHA = hashlib.sha256(SRC).hexdigest()
ZIP_B64 = base64.b64encode(hashlib.sha256(zip_bytes).digest()).decode()
print("served CodeSha256   : %s" % CONF["CodeSha256"])
print("served LastModified : %s" % CONF["LastModified"])
print("served CodeSize     : %d" % CONF["CodeSize"])
print("zip member          : lambda_function.py, %d B, sha256 %s" % (len(SRC), SHA))
APPLY_UTC = datetime.datetime.strptime(CONF["LastModified"], "%Y-%m-%dT%H:%M:%S.%f%z")


class _Stub:
    def __init__(self, svc):
        self._svc = svc

    def __getattr__(self, name):
        def _c(**kw):
            raise AssertionError("STUB REFUSAL: %s.%s -- this battery invokes nothing"
                                 % (self._svc, name))
        return _c


def _load(src_bytes, tag):
    p = os.path.join(REPO_ROOT, ".scratch", "egs24_%s.py" % tag)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, "wb") as fh:
        fh.write(src_bytes)
    real = boto3.client
    boto3.client = lambda service, **kw: _Stub(service)
    os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
    os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub")
    spec = importlib.util.spec_from_file_location("egs24_%s" % tag, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    boto3.client = real
    return m


DEP = _load(SRC, "deployed")
pre = subprocess.run(["git", "show", "%s:%s" % (PRE_CHANGE_PIN, SOURCE_REL)],
                     cwd=REPO_ROOT, capture_output=True)
assert pre.returncode == 0 and pre.stdout, "git show positive control failed"
PRE_SHA = hashlib.sha256(pre.stdout).hexdigest()
PRE = _load(pre.stdout, "prechange")
print("pre-change blob     : %s:%s -> %d B, sha256 %s"
      % (PRE_CHANGE_PIN, SOURCE_REL.rsplit("/", 1)[-1], len(pre.stdout), PRE_SHA))
print("  content-verified against the sha256 measured on the PREVIOUSLY deployed member: %s"
      % (PRE_SHA == PRE_CHANGE_SHA256))

SCHEDULED_SHAPES = [{"mode": "run"}, {}, None, {"mode": "run", "month": "2026-08"},
                    {"version": "0", "id": "abc", "detail-type": "Scheduled Event",
                     "source": "aws.events", "detail": {}, "mode": "run"}]

# =====================================================================================
head("(a) THE SEAM REPRODUCES ITS OWN ABSENCE FIRST -- against the PRE-CHANGE code")
# =====================================================================================
pre_tree = ast.parse(pre.stdout.decode("utf-8"))
pre_keys = set()
for n in ast.walk(pre_tree):
    if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get"
            and n.args and isinstance(n.args[0], ast.Constant)
            and isinstance(n.args[0].value, str)):
        seg = ast.get_source_segment(pre.stdout.decode("utf-8"), n.func.value) or ""
        if "event" in seg:
            pre_keys.add(n.args[0].value)
print("PRE-CHANGE handler event keys (denominator %d): %s" % (len(pre_keys), sorted(pre_keys)))
absent = 0
for ev in SCHEDULED_SHAPES:
    month = (ev or {}).get("month") or PRE._last_month()
    cmd = PRE._render_command(month)[0]
    if "--fixture-remove" not in cmd:
        absent += 1
print("  pre-change commands containing --fixture-remove: %d of %d"
      % (len(SCHEDULED_SHAPES) - absent, len(SCHEDULED_SHAPES)))
hold("a-absence-reproduced", absent == len(SCHEDULED_SHAPES) and "--fixture-remove" not in
     pre.stdout.decode("utf-8"),
     "the pre-change code produces NO --fixture-remove for %d of %d shapes and the token appears "
     "nowhere in its source -- the seam genuinely did not exist" % (absent, len(SCHEDULED_SHAPES)))

# =====================================================================================
head("(b) THE SCHEDULED PATH IS BIT-FOR-BIT UNCHANGED")
# =====================================================================================
same = 0
for ev in SCHEDULED_SHAPES:
    month = (ev or {}).get("month") or DEP._last_month()
    before = PRE._render_command(month)[0]
    after = DEP._render_command(month, DEP._forcing_spec(ev))[0]
    ok = before == after
    same += ok
    print("  %-56s identical=%s len=%d" % (json.dumps(ev)[:56], ok, len(after)))
hold("b-scheduled-bit-for-bit", same == len(SCHEDULED_SHAPES),
     "%d of %d marker-free payload shapes build a command byte-identical to the pre-change one"
     % (same, len(SCHEDULED_SHAPES)))

# =====================================================================================
head("(c) THE SCHEDULED PATH CANNOT REACH THE FORCING -- code AND deployed payload")
# =====================================================================================
SMUGGLE = [
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04"},
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04", "test_run": False},
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04", "test_run": None},
    {"mode": "run", "force_fixture_remove": "cottonwood:2026-08-04", "test_run": 0},
    {"mode": "run", "detail": {"force_fixture_remove": "cottonwood:2026-08-04",
                               "test_run": True}},
    {"mode": "run", "test_run": True, "FORCE_FIXTURE_REMOVE": "cottonwood:2026-08-04"},
    {"mode": "run", "test_run": True, "fixture_remove": "cottonwood:2026-08-04"},
    {"mode": "run", "test_run": True, "--fixture-remove": "cottonwood:2026-08-04"},
    {"mode": "run", "test_run": True, "force_fixture_remove": None},
    {"mode": "run", "test_run": True, "force_fixture_remove": ""},
    {"mode": "run", "test_run": True, "force_fixture_remove": []},
    {"mode": "run", "test_run": True, "force_fixture_remove": 1},
    {"mode": "run", "test_run": True, "force_fixture_remove": ["cottonwood:2026-08-04"]},
    {"mode": "run", "test_run": True, "force_fixture_remove": "cottonwood:2026-08-04'; id; echo '"},
    {"mode": "run", "test_run": True, "force_fixture_remove": "cottonwood:2026-8-4"},
]
reached = 0
for ev in SCHEDULED_SHAPES + SMUGGLE:
    month = (ev or {}).get("month") or DEP._last_month()
    if "--fixture-remove" in DEP._render_command(month, DEP._forcing_spec(ev))[0]:
        reached += 1
n_code = len(SCHEDULED_SHAPES) + len(SMUGGLE)
print("  CODE GRAIN: payloads reaching --fixture-remove: %d of %d" % (reached, n_code))

# THE SECOND WRITER, which a handler-scoped census cannot see
month_inj = ["2026-08 --fixture-remove cottonwood:2026-08-04", "2026-08 --s3-out s3://x/",
             "2026-08 --no-ladder", "2026-08'; id; echo '", "2026-13", "current", "", None]
month_refused = 0
for bad in month_inj:
    try:
        DEP._render_command(bad, "")
    except ValueError:
        month_refused += 1
print("  SECOND WRITER (`month`): refused %d of %d injection shapes"
      % (month_refused, len(month_inj)))

sc = _sched.get_schedule(Name="etfs-reports-monthly-run")
raw_input_ = sc["Target"]["Input"]
payload = json.loads(raw_input_)
print("  DEPLOYED PAYLOAD GRAIN -- the live rule's own Input, read now:")
print("    State=%s  Schedule=%s  Input(VERBATIM)=%r"
      % (sc["State"], sc["ScheduleExpression"], raw_input_))
print("    keys (denominator %d): %s" % (len(payload), sorted(payload)))
for k in ("mode", "test_run", "force_fixture_remove", "month"):
    print("      %-22s present=%-5s value=%r"
          % (k, k in payload, payload.get(k, "<ABSENT>")))
pos_ctrl = payload.get("mode") == "run"
forcing_in_payload = sum(1 for k in ("test_run", "force_fixture_remove", "month") if k in payload)
hold("c-code-grain", reached == 0,
     "0 of %d payload shapes reach --fixture-remove in the DEPLOYED code" % n_code)
hold("c-second-writer-fenced", month_refused == len(month_inj),
     "the `month` writer refuses %d of %d injections (it accepted them before this cell -- row "
     "W4-S5)" % (month_refused, len(month_inj)))
hold("c-deployed-payload", pos_ctrl and forcing_in_payload == 0,
     "the LIVE rule sends %d key(s) %s; 0 of 3 forcing-capable keys present, and the POSITIVE "
     "CONTROL mode='run' reads present so the absences are real"
     % (len(payload), sorted(payload)))

# =====================================================================================
head("(d) THE FORCING WORKS WHEN EXPLICITLY ASKED -- and cannot persist")
# =====================================================================================
spec = "cottonwood:2026-08-04,2026-08-05"
ev = {"mode": "run", "month": "2026-08", "test_run": True, "force_fixture_remove": spec}
got = DEP._forcing_spec(ev)
cmd = DEP._render_command("2026-08", got)[0]
tail = cmd[cmd.index("render_month_end.py --month"):]
print("  resolved spec : %r" % got)
print("  command tail  : %s" % tail[:160])
presentation = os.path.join(REPO_ROOT, "data", "etfs", "scripts", "presentation")
if presentation not in sys.path:
    sys.path.insert(0, presentation)
import render_month_end  # noqa: E402 -- the PRODUCER's own parser, imported after sys.path setup

parsed = render_month_end._parse_fixture_remove(got)
print("  renderer's own _parse_fixture_remove(spec) -> %r" % parsed)
hold("d-forcing-works", got == spec and (" --fixture-remove %s" % spec) in cmd
     and parsed == {"cottonwood": ["2026-08-04", "2026-08-05"]},
     "the spec reaches --fixture-remove verbatim and parses under the renderer's own parser")

print("  PERSISTENCE (hardened condition d), on the DEPLOYED module object:")
src_tree = ast.parse(TEXT)
n_global = sum(1 for n in ast.walk(src_tree) if isinstance(n, ast.Global))
env_writes = len([n for n in ast.walk(src_tree)
                  if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Subscript)
                          and "environ" in (ast.get_source_segment(TEXT, t.value) or "")
                          for t in n.targets)])
persisters = sum(TEXT.count(t) for t in ("put_parameter", "put_object"))
c_forced = DEP._render_command("2026-08", DEP._forcing_spec(ev))[0]
c_after = DEP._render_command("2026-08", DEP._forcing_spec({"mode": "run"}))[0]
c_never = DEP._render_command("2026-08", "")[0]
print("    `global` stmts %d | os.environ WRITES %d | put_parameter/put_object %d"
      % (n_global, env_writes, persisters))
print("    warm container: forced->flag=%s, next scheduled call->flag=%s, == never-forced build:%s"
      % ("--fixture-remove" in c_forced, "--fixture-remove" in c_after, c_after == c_never))
hold("d-cannot-persist",
     n_global == 0 and env_writes == 0 and persisters == 0
     and "--fixture-remove" in c_forced and "--fixture-remove" not in c_after
     and c_after == c_never,
     "no global, no env write, no SSM/S3 persistence, and a warm container that just forced "
     "builds a byte-identical never-forced command on the next call")

# =====================================================================================
head("(e) THE DEPLOY IS REAL AND MATCHES WHAT WAS REVIEWED")
# =====================================================================================
committed = subprocess.run(["git", "show", "HEAD:%s" % SOURCE_REL],
                           cwd=REPO_ROOT, capture_output=True).stdout
COMMITTED_SHA = hashlib.sha256(committed).hexdigest()
plan_text = io.open(PLAN_TRANSCRIPT, "r", encoding="utf-8").read()
predicted = re.search(r'source_code_hash\s+=\s+"[^"]+"\s+->\s+"([^"]+)"', plan_text)
plan_res = re.findall(r"^  # (\S+) will be", plan_text, re.M)
print("  served CodeSha256      : %s" % CONF["CodeSha256"])
print("  fetched zip sha256 b64 : %s" % ZIP_B64)
print("  plan PREDICTED         : %s" % (predicted.group(1) if predicted else "<none>"))
print("  zip member sha256      : %s" % SHA)
print("  committed HEAD blob    : %s (%d B)" % (COMMITTED_SHA, len(committed)))
print("  NEGATIVE CONTROL, pre-change blob: %s -- equal to deployed: %s"
     % (PRE_SHA, PRE_SHA == SHA))
print("  plan resources (denominator %d): %s" % (len(plan_res), plan_res))
entry_text = io.open(ENTRY, "r", encoding="utf-8").read()
opened_at = datetime.datetime.fromisoformat(
    re.search(r"\*\*Date opened:\*\*\s*(\S+)", entry_text).group(1)).astimezone(
        datetime.timezone.utc)
status = re.search(r"\*\*Status:\*\*\s*(.+)", entry_text).group(1).strip()
rc_log, log_out = subprocess.run(
    ["git", "log", "--full-history", "--format=%H", "--",
     os.path.relpath(ENTRY, REPO_ROOT).replace("\\", "/")],
    cwd=REPO_ROOT, capture_output=True).returncode, subprocess.run(
    ["git", "log", "--full-history", "--format=%H", "--",
     os.path.relpath(ENTRY, REPO_ROOT).replace("\\", "/")],
    cwd=REPO_ROOT, capture_output=True).stdout.decode()
entry_commits = [x for x in log_out.split() if x]
print("  entry opened %s < apply %s : %s"
      % (opened_at.isoformat(), APPLY_UTC.isoformat(), opened_at < APPLY_UTC))
print("  entry status: %s | commits on the entry: %d" % (status[:60], len(entry_commits)))
for tok in ("NEW REACHABLE STATE", "deliberately dropped input data", "DENOMINATOR = 6",
            "b08a646d5755f501"):
    print("    sign-off names %-34s : %s" % (tok, tok in entry_text))
hold("e-deployed-equals-built-equals-reviewed",
     CONF["CodeSha256"] == ZIP_B64 and predicted and predicted.group(1) == CONF["CodeSha256"]
     and COMMITTED_SHA == SHA and PRE_SHA != SHA
     and plan_res == ["aws_lambda_function.orchestrator"],
     "served == fetched zip == the hash the plan predicted; the member equals the committed blob; "
     "the pre-change blob does NOT match; the plan carried 1 of 1 resource")
hold("e-entry-ordering-and-signoff",
     opened_at < APPLY_UTC and status.startswith("CLOSED") and len(entry_commits) >= 2
     and "deliberately dropped input data" in entry_text and "DENOMINATOR = 6" in entry_text
     and "b08a646d5755f501" in entry_text,
     "the entry opened before the apply, is CLOSED across %d commits, names the new reachable "
     "state in its own words, PRINTS the writer count, and carries my own sha256 of the served "
     "EG-s-25 renderer" % len(entry_commits))

# =====================================================================================
head("(f) NO SEND, NO INVOKE")
# =====================================================================================
served_renderer = _s3.get_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)["Body"].read()
print("  ORDERING RE-CHECK: served renderer %d B sha256 %s (EG-s-25 present: forced=%d run_id=%d)"
      % (len(served_renderer), hashlib.sha256(served_renderer).hexdigest(),
         served_renderer.decode("utf-8").count("forced"),
         served_renderer.decode("utf-8").count("run_id")))
start = int((APPLY_UTC - datetime.timedelta(hours=2)).timestamp() * 1000)
ev_resp = _logs.filter_log_events(logGroupName="/aws/lambda/%s" % FUNCTION,
                                  startTime=start, limit=200)
events = ev_resp.get("events", [])
starts = [e for e in events if e.get("message", "").startswith("START RequestId")]
print("  CloudWatch /aws/lambda/%s since %s: %d event(s) scanned, %d of them START RequestId"
      % (FUNCTION, datetime.datetime.fromtimestamp(start / 1000, datetime.timezone.utc)
         .isoformat(), len(events), len(starts)))
for e in starts[:5]:
    print("    %s" % e["message"].strip()[:110])
# POSITIVE CONTROL -- a 0-of-0 read cannot tell "not invoked" from "log group unreadable",
# and a gate on an empty set passes vacuously. Widen to a window that CONTAINS a known
# invocation (EG-s-15's driven run, 2026-09-10T01:19:02Z) and require it to be non-zero.
ctrl_start = int(datetime.datetime(2026, 9, 10, 1, 0, tzinfo=datetime.timezone.utc)
                 .timestamp() * 1000)
ctrl_end = int(datetime.datetime(2026, 9, 10, 1, 30, tzinfo=datetime.timezone.utc)
               .timestamp() * 1000)
ctrl = _logs.filter_log_events(logGroupName="/aws/lambda/%s" % FUNCTION,
                               startTime=ctrl_start, endTime=ctrl_end, limit=200)
ctrl_events = ctrl.get("events", [])
ctrl_starts = [e for e in ctrl_events if e.get("message", "").startswith("START RequestId")]
print("  POSITIVE CONTROL 01:00-01:30Z (contains EG-s-15's known driven run): %d event(s), "
      "%d START RequestId -- a non-zero here is what makes the zero above a real absence"
      % (len(ctrl_events), len(ctrl_starts)))
print("  this battery's own AWS calls, all READS: lambda:GetFunction, HTTPS GET of "
      "Code.Location, s3:GetObject x1, scheduler:GetSchedule, logs:FilterLogEvents (5 kinds)")
print("  the module under test was imported with EVERY boto3 client replaced by a stub that "
      "RAISES on any call, so no SES/EC2/SSM call is reachable through it")
hold("f-no-send-no-invoke", len(starts) == 0 and len(ctrl_starts) > 0,
     "%d START RequestId in my 2 h window (of %d events), against %d in the control window "
     "(of %d) -- the control is NON-ZERO, so my zero is a measured absence and not an empty-set "
     "vacuous pass; and the battery makes 5 kinds of AWS call, all reads"
     % (len(starts), len(events), len(ctrl_starts), len(ctrl_events)))

# =====================================================================================
head("VERDICT")
# =====================================================================================
print("arms: %d of %d HOLD" % (sum(1 for v in ARMS.values() if v), len(ARMS)))
for k, v in ARMS.items():
    print("  %-42s %s" % (k, "HOLD" if v else "FAIL"))
if FAILS:
    print("")
    print("FAILED: %s" % ", ".join(FAILS))
    print("NOT-PROVEN.")
    sys.exit(1)
print("")
print("EGS24-FORCING-THREADED-SCHEDULE-CLEAN")
sys.exit(0)
