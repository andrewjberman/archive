#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-27 -- S27-AC1 battery.

NO SEND, NO ORCHESTRATOR INVOKE. Every AWS call is a read: lambda:GetFunction
(+Configuration), an HTTPS GET of the presigned code location, s3:GetObject/HeadObject on
the renderer artifact, and logs:FilterLogEvents. The renderer and the orchestrator are
executed only in-process with their AWS clients replaced by stubs that RAISE.

GRAIN, STATED LOUDLY AND FIRST (Rule 22a): the ordering condition BLOCKS THE APPLY until
EG-s-26's renderer is served, so at this run's time the seam under test is the BUILD INPUT
and NOT served bytes. Arms (a)-(d) and (g) are therefore claims about the build input and
say so; arm (f) is the deploy and is BLOCKED; arm (e) needs EG-s-26's skip record and is
BLOCKED. The DEPLOYED orchestrator is still read, and is used as arm (a)'s "before".

Prints EGS27-SKIP-RIDES-FORCING-SCHEDULE-CLEAN only when all seven arms hold. Until the
ordering clears it prints EGS27-BLOCKED-ORDERING-EG-S-26-NOT-SERVED.
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
import sys
import types
import urllib.request
import zipfile
from unittest import mock

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
FUNCTION = "etfs-reports-orchestrator"
REGION = "us-east-1"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "ec2/etfs-reports/render_month_end.py"
SOURCE_REL = "infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py"
MONTH, PARTNER, TARGET = "2026-08", "cottonwood", "2026-08-04"
EGS25_BASELINE_SHA = "b08a646d5755f501f10b0b3c8d0512702c20b38e02263dc3b33a2f963d71020f"

ARMS, BLOCKED = {}, []


def hold(arm, ok, why, blocking=False):
    ARMS[arm] = bool(ok)
    if not ok and blocking:
        BLOCKED.append(arm)
    print("  [%s] %s -- %s" % ("HOLD" if ok else ("BLOCKED" if blocking else "FAIL"), arm, why))


def head(t):
    print("")
    print("=" * 78)
    print(t)
    print("=" * 78)


_lam = boto3.client("lambda", region_name=REGION)
_s3 = boto3.client("s3", region_name=REGION)
_logs = boto3.client("logs", region_name=REGION)


class _Stub:
    def __init__(self, svc):
        self._svc = svc

    def __getattr__(self, n):
        def _c(**kw):
            raise AssertionError("STUB REFUSAL: %s.%s -- this battery invokes nothing"
                                 % (self._svc, n))
        return _c


def _load_orch(src_bytes, tag):
    p = os.path.join(REPO, ".scratch", "egs27_%s.py" % tag)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    io.open(p, "wb").write(src_bytes)
    real = boto3.client
    boto3.client = lambda service, **kw: _Stub(service)
    os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
    os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub")
    spec = importlib.util.spec_from_file_location("egs27_%s" % tag, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    boto3.client = real
    return m


# =====================================================================================
head("0. THE SUBJECTS, and which grain each arm speaks about")
# =====================================================================================
fn = _lam.get_function(FunctionName=FUNCTION)
CONF = fn["Configuration"]
zb = urllib.request.urlopen(fn["Code"]["Location"]).read()
DEP_SRC = zipfile.ZipFile(io.BytesIO(zb)).read("lambda_function.py")
NEW_SRC = io.open(os.path.join(REPO, SOURCE_REL), "rb").read()
print("DEPLOYED orchestrator : CodeSha256 %s  LastModified %s"
      % (CONF["CodeSha256"], CONF["LastModified"]))
print("  zip member          : %d B sha256 %s" % (len(DEP_SRC), hashlib.sha256(DEP_SRC).hexdigest()))
print("  zip sha256 (b64)    : %s" % base64.b64encode(hashlib.sha256(zb).digest()).decode())
print("BUILD INPUT (this cell's change, NOT yet served -- the apply is blocked):")
print("  %s : %d B sha256 %s" % (SOURCE_REL, len(NEW_SRC), hashlib.sha256(NEW_SRC).hexdigest()))
DEP = _load_orch(DEP_SRC, "deployed")
NEW = _load_orch(NEW_SRC, "buildinput")

REND = _s3.get_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)["Body"].read()
REND_SHA = hashlib.sha256(REND).hexdigest()
RTEXT = REND.decode("utf-8")
print("SERVED renderer       : %d B sha256 %s" % (len(REND), REND_SHA))

SCHEDULED_SHAPES = [{"mode": "run"}, {}, None, {"mode": "run", "month": "2026-08"},
                    {"version": "0", "id": "a", "detail-type": "Scheduled Event",
                     "source": "aws.events", "detail": {}, "mode": "run"}]

# =====================================================================================
head("(a) THE ABSENCE REPRODUCES FIRST -- against the code as it stands (DEPLOYED)")
# =====================================================================================
dep_tree = ast.parse(DEP_SRC.decode("utf-8"))
dep_keys = set()
for n in ast.walk(dep_tree):
    if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get"
            and n.args and isinstance(n.args[0], ast.Constant)
            and isinstance(n.args[0].value, str)):
        seg = ast.get_source_segment(DEP_SRC.decode("utf-8"), n.func.value) or ""
        if "event" in seg:
            dep_keys.add(n.args[0].value)
print("DEPLOYED handler event keys (denominator %d): %s" % (len(dep_keys), sorted(dep_keys)))
probe_events = SCHEDULED_SHAPES + [
    {"mode": "run", "test_run": True},
    {"mode": "run", "test_run": True, "force_fixture_remove": "%s:%s" % (PARTNER, TARGET)},
    {"mode": "run", "test_run": True, "no_ladder": True},
    {"mode": "run", "test_run": True, "ladder": False},
    {"mode": "run", "month": "2026-08 --no-ladder"},
]
absent = 0
for ev in probe_events:
    month = (ev or {}).get("month") or DEP._last_month()
    try:
        c = DEP._render_command(month, DEP._forcing_spec(ev))[0]
    except ValueError:
        absent += 1
        continue
    if "--no-ladder" not in c:
        absent += 1
print("  DEPLOYED commands containing --no-ladder: %d of %d"
      % (len(probe_events) - absent, len(probe_events)))
# EXECUTABLE occurrences only, via the AST, where comments do not exist. A raw-text
# count over the deployed source returns 1 and it is a COMMENT -- my own W4-S5 note at
# :145 naming `--no-ladder` as one of the flags the `month` injection could reach. A
# text probe that cannot tell a comment from a string literal is the same error I made
# counting `ses` and `.get("unresolved")`, so this one is banded.
_dep_text = DEP_SRC.decode("utf-8")
_dep_str_hits = [n for n in ast.walk(dep_tree)
                 if isinstance(n, ast.Constant) and isinstance(n.value, str)
                 and "--no-ladder" in n.value]
_raw = _dep_text.count("--no-ladder")
_comment_hits = [ln.strip() for ln in _dep_text.split("\n")
                 if "--no-ladder" in ln and ln.strip().startswith("#")]
print("  --no-ladder in the DEPLOYED source: raw text %d | in a STRING LITERAL (AST) %d | "
      "in a COMMENT %d" % (_raw, len(_dep_str_hits), len(_comment_hits)))
for c in _comment_hits:
    print("      COMMENT: %s" % c[:110])
hold("a-absence-reproduced",
     absent == len(probe_events) and len(_dep_str_hits) == 0,
     "no event shape produces --no-ladder on the deployed code (%d of %d absent) and the token "
     "appears in 0 executable string literals there -- its %d raw-text hit(s) are all comments. "
     "The premise holds." % (absent, len(probe_events), _raw))

# =====================================================================================
head("(b) THE SCHEDULED PATH IS BIT-FOR-BIT UNCHANGED")
# =====================================================================================
same = 0
for ev in SCHEDULED_SHAPES:
    month = (ev or {}).get("month") or NEW._last_month()
    before = DEP._render_command(month, DEP._forcing_spec(ev))[0]
    after = NEW._render_command(month, NEW._forcing_spec(ev))[0]
    same += before == after
    print("  %-52s identical=%s" % (json.dumps(ev)[:52], before == after))
hold("b-scheduled-bit-for-bit", same == len(SCHEDULED_SHAPES),
     "%d of %d marker-free shapes build a command byte-identical to the deployed one"
     % (same, len(SCHEDULED_SHAPES)))

# =====================================================================================
head("(c) THE SKIP IS NOT INDEPENDENTLY REACHABLE -- the COUPLED shape")
# =====================================================================================
SMUGGLE = [
    {"mode": "run", "no_ladder": True}, {"mode": "run", "test_run": True, "no_ladder": True},
    {"mode": "run", "test_run": True, "NO_LADDER": True},
    {"mode": "run", "test_run": True, "no-ladder": True},
    {"mode": "run", "test_run": True, "ladder": False},
    {"mode": "run", "test_run": True, "skip_ladder": True},
    {"mode": "run", "detail": {"test_run": True, "no_ladder": True}},
    {"mode": "run", "test_run": True, "force_fixture_remove": None, "no_ladder": True},
    {"mode": "run", "test_run": True, "force_fixture_remove": "", "no_ladder": True},
    {"mode": "run", "test_run": True, "force_fixture_remove": "bad-spec", "no_ladder": True},
    {"mode": "run", "force_fixture_remove": "%s:%s" % (PARTNER, TARGET)},
    {"mode": "run", "test_run": False, "force_fixture_remove": "%s:%s" % (PARTNER, TARGET)},
]
MONTH_SMUGGLE = ["2026-08 --no-ladder",
                 "2026-08 --no-ladder --fixture-remove %s:%s" % (PARTNER, TARGET),
                 "2026-08 --fixture-remove %s:%s" % (PARTNER, TARGET)]
reached = []
n_c = 0
for ev in SCHEDULED_SHAPES + SMUGGLE:
    month = (ev or {}).get("month") or NEW._last_month()
    c = NEW._render_command(month, NEW._forcing_spec(ev))[0]
    n_c += 1
    if "--no-ladder" in c:
        reached.append(ev)
for bad in MONTH_SMUGGLE:
    n_c += 1
    try:
        c = NEW._render_command(bad, NEW._forcing_spec({"mode": "run", "month": bad}))[0]
    except ValueError:
        continue
    if "--no-ladder" in c:
        reached.append({"month": bad})
print("  payloads attempting the skip WITHOUT a valid forcing spec: %d, reached: %d"
      % (n_c, len(reached)))
src_txt = NEW_SRC.decode("utf-8")
emitters = [ln.strip() for ln in src_txt.split("\n")
            if "--no-ladder" in ln and not ln.strip().startswith("#")]
print("  EXECUTABLE emitters of --no-ladder in the build input (denominator %d): %s"
      % (len(emitters), emitters))
hold("c-not-independently-reachable",
     len(reached) == 0 and len(emitters) == 1 and "if forcing" in emitters[0],
     "0 of %d payloads reach --no-ladder without a validated forcing spec, and there is exactly "
     "1 executable emitter and it is conditioned on `forcing` -- so the skip ADDS NO NEW WRITER "
     "and inherits every fence the forcing already has" % n_c)

# =====================================================================================
head("(d) THE FORCING NOW REACHES THE VERDICT -- the arm EG-s-24 did not prove")
# =====================================================================================
sys.path.insert(0, os.path.join(REPO, "data", "etfs", "scripts"))
sys.path.insert(0, os.path.join(REPO, "data", "inf", "scripts", "silver"))
import _orion_vendor_asof  # noqa: F401,E402
import coverage  # noqa: F401,E402

series = {}
_d = datetime.date(2026, 8, 1)
while _d <= datetime.date(2026, 8, 31):
    series[_d.isoformat()] = True
    _d += datetime.timedelta(days=1)


class _StubS3:
    """Real S3 state: every slice PRESENT, because --fixture-remove never touches S3."""
    def get_paginator(self, name):
        class _P:
            def paginate(self, Bucket=None, Prefix=None):  # noqa: N803
                p = Prefix.split("/")[1]
                return [{"Contents": [{"Key": "daily/%s/%s.json" % (p, k)} for k in series]}]
        return _P()

    def __getattr__(self, n):
        def _c(**kw):
            raise AssertionError("STUB REFUSAL: s3.%s" % n)
        return _c


rp = os.path.join(REPO, ".scratch", "egs27_rend.py")
io.open(rp, "wb").write(REND)
_real = boto3.client
boto3.client = lambda service, **kw: _StubS3() if service == "s3" else mock.Mock()
RM = types.ModuleType("egs27_rend")
RM.__file__ = rp
sys.modules["egs27_rend"] = RM
exec(compile(REND, rp, "exec"), RM.__dict__)
boto3.client = _real
RM.s3 = _StubS3()
asked = []


def _fake_remediate(p, month, classes, invoke=None, s3=None, dry_run=False):
    cs = sorted(k for k, v in classes.items() if v["class"] == "C")
    asked.append((p, cs))
    return {"resolved": cs, "expected_empty": [], "unresolved": [],
            "rungs": {"probe": 0, "rerun": len(cs), "recheck": 0}}


RM.remediate = types.SimpleNamespace(remediate_month=_fake_remediate)
RM._make_invoke = lambda *a, **k: (lambda f, p: {"ok": True})


def _drive(event):
    """Build the command with THIS CELL'S code, then reproduce exactly what the renderer's
    own main() does with the flags that command carries -- using the RENDERER'S OWN
    _parse_fixture_remove / _apply_fixture_remove / coverage_gate, never a re-implementation.
    The only thing written here is the flag extraction from my own command, which is the
    thing under test."""
    month = (event or {}).get("month") or NEW._last_month()
    cmd = NEW._render_command(month, NEW._forcing_spec(event))[0]
    tail = cmd[cmd.index("render_month_end.py --month"):].rstrip("'")
    toks = tail.split()
    spec = toks[toks.index("--fixture-remove") + 1] if "--fixture-remove" in toks else ""
    no_ladder = "--no-ladder" in toks
    fixture = RM._parse_fixture_remove(spec)
    daily = {PARTNER: dict(series)}
    RM._apply_fixture_remove(daily, fixture)
    asked.clear()
    v = RM.coverage_gate(MONTH, [PARTNER], daily, ["DIVZ"], ladder=not no_ladder,
                         probe=lambda p, ds: {"partition": True, "priced": 12},
                         fixture_remove=fixture, fixture_remove_spec=spec,
                         run_id="EGS27-BATTERY", run_id_source="battery")
    return tail, spec, no_ladder, v


forced_ev = {"mode": "run", "month": MONTH, "test_run": True,
             "force_fixture_remove": "%s:%s" % (PARTNER, TARGET)}
unforced_ev = {"mode": "run", "month": MONTH}
ft, fspec, fnl, fv = _drive(forced_ev)
ut, uspec, unl, uv = _drive(unforced_ev)
fs = fv["per_partner"][PARTNER]["summary"]
us = uv["per_partner"][PARTNER]["summary"]
print("  FORCED   command tail : %s" % ft[:150])
print("           spec=%r no_ladder=%s -> VERDICT=%s C=%d holes=%s"
      % (fspec, fnl, fv["verdict"], fs["C"], fv["per_partner"][PARTNER]["holes"]))
print("  UNFORCED command tail : %s" % ut[:150])
print("           spec=%r no_ladder=%s -> VERDICT=%s C=%d holes=%s"
      % (uspec, unl, uv["verdict"], us["C"], uv["per_partner"][PARTNER]["holes"]))
print("  (the UNFORCED arm is this arm's POSITIVE CONTROL: same code, same month, same probe,")
print("   same served renderer -- only the forcing differs, and it flips the verdict.)")
hold("d-forcing-reaches-the-verdict",
     fv["verdict"] == "REFUSE" and fs["C"] > 0 and uv["verdict"] == "PUBLISH" and us["C"] == 0,
     "a forcing spec delivered THROUGH THIS CELL'S COMMAND yields REFUSE with class C=%d, beside "
     "the same run unforced yielding PUBLISH with C=%d -- the effect EG-s-24 did not prove"
     % (fs["C"], us["C"]))

# =====================================================================================
head("(e) THE DISCLOSURE ON THAT RUN -- needs EG-s-26 on the served key")
# =====================================================================================
served_ok = REND_SHA != EGS25_BASELINE_SHA
print("  served renderer sha256      : %s" % REND_SHA)
print("  my own EG-s-25 baseline     : %s" % EGS25_BASELINE_SHA)
print("  DIFFERENT (i.e. EG-s-26 landed): %s" % served_ok)
SKIP_TOKENS = ["ladder_skipped", "egress_ask_absent", "rung3", "rung_3", "skip_record"]
CONTROLS = ["forcing", "forced", "run_id", "fixture_remove"]
for t in SKIP_TOKENS:
    print("    EG-s-26 skip token %-18s : %d" % (t, RTEXT.count(t)))
for t in CONTROLS:
    print("    EG-s-25 CONTROL    %-18s : %d" % (t, RTEXT.count(t)))
print("  the forced run's verdict object, whole:")
print("    %s" % json.dumps({k: v for k, v in fv.items() if k != "per_partner"}, indent=6)[:900])
have_skip = any(RTEXT.count(t) for t in SKIP_TOKENS)
hold("e-disclosure-present", served_ok and have_skip,
     "the served renderer is BYTE-IDENTICAL to the EG-s-25 build I measured myself and carries "
     "0 of %d EG-s-26 skip tokens against %d non-zero EG-s-25 controls -- so EG-s-26 IS NOT "
     "SERVED and a ladder-skipped run could not yet record that it skipped"
     % (len(SKIP_TOKENS), sum(1 for t in CONTROLS if RTEXT.count(t))),
     blocking=True)

# =====================================================================================
head("(f) THE DEPLOY -- gated on (e) by the BLOCKING ORDERING")
# =====================================================================================
print("  served CodeSha256 : %s (unchanged -- this cell has NOT applied)" % CONF["CodeSha256"])
print("  build input sha256: %s" % hashlib.sha256(NEW_SRC).hexdigest())
print("  deployed member   : %s" % hashlib.sha256(DEP_SRC).hexdigest())
hold("f-deploy-real", False,
     "NOT APPLIED, and deliberately: the face forbids applying until EG-s-26's renderer is "
     "verified on the served key by my own sha256, and arm (e) shows it is not there. STOPPED "
     "rather than waiting in a loop.", blocking=True)

# =====================================================================================
head("(g) NO SEND, NO INVOKE")
# =====================================================================================
start = int((datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=2))
            .timestamp() * 1000)
ev_resp = _logs.filter_log_events(logGroupName="/aws/lambda/%s" % FUNCTION,
                                  startTime=start, limit=200)
events = ev_resp.get("events", [])
starts = [e for e in events if e.get("message", "").startswith("START RequestId")]
ctrl_s = int(datetime.datetime(2026, 9, 10, 1, 0, tzinfo=datetime.timezone.utc).timestamp() * 1000)
ctrl_e = int(datetime.datetime(2026, 9, 10, 1, 30, tzinfo=datetime.timezone.utc).timestamp() * 1000)
ctrl = _logs.filter_log_events(logGroupName="/aws/lambda/%s" % FUNCTION,
                               startTime=ctrl_s, endTime=ctrl_e, limit=200)
ctrl_ev = ctrl.get("events", [])
ctrl_st = [e for e in ctrl_ev if e.get("message", "").startswith("START RequestId")]
print("  my 2 h window : %d event(s), %d START RequestId" % (len(events), len(starts)))
print("  POSITIVE CONTROL 01:00-01:30Z (EG-s-15's known run): %d event(s), %d START RequestId"
      % (len(ctrl_ev), len(ctrl_st)))
print("  AWS calls made by this battery, all READS: lambda:GetFunction, HTTPS GET of "
      "Code.Location, s3:GetObject x1, logs:FilterLogEvents x2 (4 kinds)")
hold("g-no-send-no-invoke", len(starts) == 0 and len(ctrl_st) > 0,
     "%d START RequestId in my window (of %d), against %d in the control window (of %d) -- the "
     "control is NON-ZERO so my zero is a measured absence, not an empty-set vacuous pass"
     % (len(starts), len(events), len(ctrl_st), len(ctrl_ev)))

# =====================================================================================
head("VERDICT")
# =====================================================================================
print("arms: %d of %d HOLD" % (sum(1 for v in ARMS.values() if v), len(ARMS)))
for k, v in ARMS.items():
    print("  %-38s %s" % (k, "HOLD" if v else ("BLOCKED" if k in BLOCKED else "FAIL")))
print("")
print("NOTHING WAS INVOKED. NO SEND. NO APPLY. NO S3 WRITE OR DELETE.")
print("EG-s-21's single permitted run remains UNSPENT.")
print("")
if BLOCKED and all(ARMS[k] for k in ARMS if k not in BLOCKED):
    print("EGS27-BLOCKED-ORDERING-EG-S-26-NOT-SERVED")
    sys.exit(2)
if not BLOCKED and all(ARMS.values()):
    print("EGS27-SKIP-RIDES-FORCING-SCHEDULE-CLEAN")
    sys.exit(0)
print("EGS27-INDETERMINATE -- an arm failed for a reason other than the ordering; re-read above")
sys.exit(1)
