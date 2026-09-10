#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-21 -- S21-AC1 battery, second attempt (dependencies now served).

IT DOES NOT INVOKE THE ORCHESTRATOR AND FIRES NO SEND. Every AWS call is a READ:
lambda:GetFunction(+Configuration), an HTTPS GET of the presigned code location, and
s3:GetObject on the renderer artifact and two served verdicts. The renderer is executed
only in-process with `remediate` and `s3` replaced by stubs.

ARM (a), THE PRECONDITION, is re-taken AT THIS RUN'S TIME on the bytes deployed now --
which are NOT the bytes my earlier read covered, because EG-s-24 redeployed the function
at 05:42:07Z. It HOLDS.

ARMS (c)-(g) CANNOT BE REACHED, and this battery measures WHY: the forcing EG-s-24
threaded is DEFEATED BY THE LADDER. `--fixture-remove` mutates the in-memory series that
`coverage_gate` uses for its FIRST classify; with `ladder=True` -- the only path the
orchestrator's fixed `--gate` command takes -- the gate then RE-CLASSIFIES FROM REAL S3
(render_month_end.py:999), where the slice was never removed. Same fixture, same month:
ladder=False -> REFUSE, ladder=True -> PUBLISH.

Prints EGS21-BLOCKED-FORCING-DEFEATED-BY-LADDER. It can never print the success token.
"""
from __future__ import annotations

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
ETFS_BUCKET = "opal-data-etfs"
MONTH, PARTNER, TARGET = "2026-08", "cottonwood", "2026-08-04"

FINDINGS = []


def head(t):
    print("")
    print("=" * 78)
    print(t)
    print("=" * 78)


def line(tag, msg):
    print("  [%s] %s" % (tag, msg))


_lam = boto3.client("lambda", region_name=REGION)
_s3 = boto3.client("s3", region_name=REGION)

# =====================================================================================
head("(a) THE PRECONDITION, re-taken at THIS run's time on the CURRENT deployed bytes")
# =====================================================================================
fn = _lam.get_function(FunctionName=FUNCTION)
CONF = fn["Configuration"]
zb = urllib.request.urlopen(fn["Code"]["Location"]).read()
ORCH = zipfile.ZipFile(io.BytesIO(zb)).read("lambda_function.py")
print("served CodeSha256   : %s" % CONF["CodeSha256"])
print("served LastModified : %s" % CONF["LastModified"])
print("zip member          : %d B sha256 %s" % (len(ORCH), hashlib.sha256(ORCH).hexdigest()))
print("zip sha256 (b64)    : %s" % base64.b64encode(hashlib.sha256(zb).digest()).decode())
print("live EMAIL_RECIPIENT: %s" % CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"])


class _Stub:
    def __init__(self, svc):
        self._svc = svc

    def __getattr__(self, n):
        def _c(**kw):
            raise AssertionError("STUB REFUSAL: %s.%s -- this battery invokes nothing"
                                 % (self._svc, n))
        return _c


op = os.path.join(REPO, ".scratch", "egs21b_orch.py")
os.makedirs(os.path.dirname(op), exist_ok=True)
io.open(op, "wb").write(ORCH)
_real = boto3.client
boto3.client = lambda service, **kw: _Stub(service)
os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub")
os.environ["EMAIL_RECIPIENT"] = CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"]
_sp = importlib.util.spec_from_file_location("egs21b_orch", op)
ORCHM = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(ORCHM)
boto3.client = _real

EVENTS = [
    {"mode": "run", "month": MONTH, "test_run": True},
    {"mode": "run", "month": MONTH, "test_run": True,
     "force_fixture_remove": "%s:%s" % (PARTNER, TARGET)},
    {"mode": "run", "test_run": True, "test_recipients": ["aj@opalinvest.com"]},
    {"mode": "run", "test_run": True, "test_recipients": "aj@opalinvest.com,andrew@opalinvest.com"},
    {"mode": "run", "test_run": True, "test_recipients": ["AJ@OpalInvest.COM"]},
    {"mode": "run", "test_run": True, "test_recipients": ["  aj@opalinvest.com  "]},
    {"mode": "run", "test_run": True, "test_recipients": []},
    {"mode": "run", "test_run": True, "test_recipients": None},
    {"mode": "run", "test_run": 1, "month": MONTH},
]
leak, n = 0, 0
for ev in EVENTS:
    for base in (ORCHM.EMAIL_RECIPIENT, ORCHM.TERMINAL_RECIPIENT):
        h, env = ORCHM._resolve_recipients(ev, base)
        n += 1
        if any(a.lower() == "aj@opalinvest.com" for a in env) or "aj@" in h.lower():
            leak += 1
_, sched_env = ORCHM._resolve_recipients({"mode": "run"}, ORCHM.EMAIL_RECIPIENT)
print("scheduled envelope (must stay BOTH): %s" % sched_env)
PRE_OK = leak == 0 and sched_env == ["aj@opalinvest.com", "andrew@opalinvest.com"]
line("HOLD" if PRE_OK else "FAIL",
     "aj@opalinvest.com in %d of %d resolved test-invocation recipient lists, on the bytes "
     "deployed at %s -- and the scheduled path is unchanged" % (leak, n, CONF["LastModified"]))

# =====================================================================================
head("(c) THE FORCING IS DEFEATED BY THE LADDER -- measured on the SERVED renderer")
# =====================================================================================
REND = _s3.get_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)["Body"].read()
RTEXT = REND.decode("utf-8")
RL = RTEXT.split("\n")
print("SERVED renderer: %d B sha256 %s" % (len(REND), hashlib.sha256(REND).hexdigest()))
gi = [i for i, x in enumerate(RL) if x.startswith("def coverage_gate")][0]
print("  coverage_gate at :%d" % (gi + 1))
for i, x in enumerate(RL, 1):
    if "classify_month(" in x and ("series=series" in x or "s3=s3" in x):
        print("    :%-5d %s" % (i, x.strip()))
apply_sites = [i for i, x in enumerate(RL, 1) if "_apply_fixture_remove(" in x]
print("  _apply_fixture_remove call sites (denominator %d): %s -- NONE inside coverage_gate "
      "(:%d-%d)" % (len(apply_sites), apply_sites, gi + 1, gi + 71))

# load the served renderer WITHOUT letting its S3 self-bootstrap fallback run
sys.path.insert(0, os.path.join(REPO, "data", "etfs", "scripts"))
sys.path.insert(0, os.path.join(REPO, "data", "inf", "scripts", "silver"))
import _orion_vendor_asof  # noqa: F401,E402
import coverage  # noqa: F401,E402

series = {}
d = datetime.date(2026, 8, 1)
while d <= datetime.date(2026, 8, 31):
    series[d.isoformat()] = True
    d += datetime.timedelta(days=1)


class _StubS3:
    """Reports the slice STILL PRESENT -- which is the truth, because --fixture-remove
    never touches S3. This is exactly what the re-classify at :999 reads."""
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


rp = os.path.join(REPO, ".scratch", "egs21b_rend.py")
io.open(rp, "wb").write(REND)
_real2 = boto3.client
boto3.client = lambda service, **kw: _StubS3() if service == "s3" else mock.Mock()
RM = types.ModuleType("egs21b_rend")
RM.__file__ = rp
sys.modules["egs21b_rend"] = RM
exec(compile(REND, rp, "exec"), RM.__dict__)
boto3.client = _real2
RM.s3 = _StubS3()

asked = []


def _fake_remediate(p, month, classes, invoke=None, s3=None, dry_run=False):
    cs = sorted(k for k, v in classes.items() if v["class"] == "C")
    asked.append((p, cs))
    return {"resolved": cs, "expected_empty": [], "unresolved": [],
            "rungs": {"probe": 0, "rerun": len(cs), "recheck": 0}}


RM.remediate = types.SimpleNamespace(remediate_month=_fake_remediate)
RM._make_invoke = lambda *a, **k: (lambda f, p: {"ok": True})
results = {}
for ladder in (False, True):
    daily = {PARTNER: dict(series)}
    fixture = {PARTNER: [TARGET]}
    RM._apply_fixture_remove(daily, fixture)
    asked.clear()
    v = RM.coverage_gate(MONTH, [PARTNER], daily, ["DIVZ"], ladder=ladder,
                         probe=lambda p, ds: {"partition": True, "priced": 12},
                         fixture_remove=fixture,
                         fixture_remove_spec="%s:%s" % (PARTNER, TARGET),
                         run_id="BATTERY-PROBE", run_id_source="battery")
    s = v["per_partner"][PARTNER]["summary"]
    results[ladder] = (v["verdict"], s["C"], v["per_partner"][PARTNER]["holes"], list(asked))
    print("  ladder=%-5s -> VERDICT=%-8s C=%d holes=%s | ladder asked to fix: %s"
          % (ladder, v["verdict"], s["C"], v["per_partner"][PARTNER]["holes"],
             asked or "<skipped>"))
print("  the DISCRIMINATING PAIR: identical fixture, identical month, identical probe; the only")
print("  difference is the ladder, and it flips the verdict.")
DEFEATED = results[False][0] == "REFUSE" and results[True][0] == "PUBLISH"
line("BLOCKED" if DEFEATED else "HOLD",
     "with ladder=True -- the ONLY path the orchestrator's fixed --gate command takes -- the "
     "forcing yields %s, not REFUSE; and rung 1 would invoke the producer for %s, rewriting a "
     "SERVED daily slice" % (results[True][0], results[True][3]))
if DEFEATED:
    FINDINGS.append("the forcing does not change the verdict on the ladder path")

cmd = ORCHM._render_command(MONTH, "%s:%s" % (PARTNER, TARGET))[0]
tail = cmd[cmd.index("render_month_end.py --month"):]
print("  the DEPLOYED command a forced invoke would send:")
print("    %s" % tail[:170])
print("  contains --fixture-remove: %s | contains --no-ladder: %s"
      % ("--fixture-remove" in cmd, "--no-ladder" in cmd))
NO_LADDER_ABSENT = "--no-ladder" not in cmd
line("BLOCKED" if NO_LADDER_ABSENT else "HOLD",
     "--no-ladder is not threaded, so no invocation can select the only mode in which the "
     "forcing works")
if NO_LADDER_ABSENT:
    FINDINGS.append("--no-ladder is not reachable from any event")

# =====================================================================================
head("AND THERE IS NO ORGANIC CLASS C TO FALL BACK ON")
# =====================================================================================
for m in ("2026-08", "2026-09"):
    v = json.loads(_s3.get_object(Bucket=ETFS_BUCKET,
                                  Key="platinum/reports/%s/coverage_verdict.json" % m)
                   ["Body"].read())
    tot = sum(pp["summary"]["C"] for pp in v["per_partner"].values())
    print("  %s served verdict: %s holes=%d | class C = %d of %d partners"
          % (m, v["verdict"], v["holes"], tot, len(v["per_partner"])))

# =====================================================================================
head("VERDICT")
# =====================================================================================
print("ARM (a) PRECONDITION : %s" % ("HOLDS -- 0 of %d reach aj@" % n if PRE_OK else "FAILS"))
print("ARMS (c)-(g)         : NOT REACHABLE -- no refusal can be produced.")
for f in FINDINGS:
    print("    BLOCKING: %s" % f)
print("")
print("NOTHING WAS INVOKED. NO SEND. NO S3 WRITE OR DELETE. EG-s-21's ONE RUN IS UNSPENT.")
print("")
if PRE_OK and len(FINDINGS) == 2:
    print("EGS21-BLOCKED-FORCING-DEFEATED-BY-LADDER")
    sys.exit(2)
print("EGS21-INDETERMINATE -- the expected blocking shape did not hold; re-read the output")
sys.exit(1)
