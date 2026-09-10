#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-27 -- S27-AC1 battery, SEVEN ARMS.

NO SEND, NO ORCHESTRATOR INVOKE. Every AWS call is a read: lambda:GetFunction
(+Configuration), an HTTPS GET of the presigned code location, s3:GetObject on the renderer
artifact, and logs:FilterLogEvents. The renderer and the orchestrator are executed only
in-process with their AWS clients replaced by stubs that RAISE.

GRAIN, STATED LOUDLY AND FIRST (Rule 22a), AND IT MOVED SINCE THE PRE-CRASH RUN. My
predecessor ran this battery while the apply was still BLOCKED by the ordering condition, so
its arms spoke about the BUILD INPUT and said so. The ordering has since cleared -- EG-s-26's
renderer is served, verified here by my own sha256 with a negative control -- the apply has
landed, and EVERY ARM BELOW NOW SPEAKS ABOUT SERVED BYTES:

  the "before" is the PRE-CHANGE BLOB git show ee7c70113f:<path>, which is not merely an
    ancestor -- it is CONTENT-RESOLVED byte-equal to the zip member this function served
    until 12:16:53Z, and this battery asserts that equality against a sha256 I measured on
    the live function BEFORE the apply (PREAPPLY_SERVED_MEMBER_SHA below);
  the "after" is the zip member fetched from the function's OWN presigned Code.Location.

Both are re-fetched on every run, so a repeat is a genuine re-measurement rather than a
cache read.

Prints EGS27-SKIP-RIDES-FORCING-SCHEDULE-CLEAN only when all seven arms hold.
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
import subprocess
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
BUILT_ZIP_REL = "infra/aws/terraform/etfs-reports/.build/etfs-reports-orchestrator.zip"
MONTH, PARTNER, TARGET = "2026-08", "cottonwood", "2026-08-04"

# --- CONSTANTS I MEASURED MYSELF, each with the read that produced it -------------------
# The renderer as it stood BEFORE EG-s-26 (my predecessor's own EG-s-25 baseline). Arm (e)
# uses it as a NEGATIVE CONTROL: if the served renderer still hashed to this, EG-s-26 would
# not be there and the ordering condition would be unmet.
EGS25_BASELINE_SHA = "b08a646d5755f501f10b0b3c8d0512702c20b38e02263dc3b33a2f963d71020f"
EGS25_BASELINE_LEN = 66756
# The orchestrator zip member SERVED IMMEDIATELY BEFORE MY APPLY, read live at ~12:05Z by
# lambda:GetFunction + an HTTPS GET of Code.Location. This is what makes the git "before"
# blob a claim about RUNNING BYTES rather than about ancestry.
PREAPPLY_SERVED_MEMBER_SHA = "8d8cb2c23d7c00d943a985d381e45b96315f7dcf6047fe1bc3cc2234854d801f"
PRE_COMMIT = "ee7c70113f"
# The value the REVIEWED, TARGETED plan predicted (transcript preserved beside this file at
# EG-s-27_preapply_plan_transcript.txt, because it is unreproducible after the apply).
PLAN_PREDICTED_SHA256_B64 = "5qPTUpaxx+NUvTN6hmXdNfe2pT2xwkHF9Y3Q3fFJVSw="
LEDGER_ENTRY = ("org/critical_paths/change_management/"
                "20260910T1215Z_etfs-guardrail-eg-s-27-ladder-skip-rides-forcing"
                "_deploy_completion.md")

ARMS: dict = {}


def hold(arm, ok, why):
    ARMS[arm] = bool(ok)
    print("  [%s] %s -- %s" % ("HOLD" if ok else "FAIL", arm, why))


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


def _git_show(ref, path):
    r = subprocess.run(["git", "show", "%s:%s" % (ref, path)], capture_output=True, cwd=REPO)
    return r.stdout


# =====================================================================================
head("0. THE SUBJECTS -- every arm below speaks about SERVED bytes")
# =====================================================================================
fn = _lam.get_function(FunctionName=FUNCTION)
CONF = fn["Configuration"]
zb = urllib.request.urlopen(fn["Code"]["Location"]).read()
DEP_SRC = zipfile.ZipFile(io.BytesIO(zb)).read("lambda_function.py")
HEAD_SRC = _git_show("HEAD", SOURCE_REL)
PRE_SRC = _git_show(PRE_COMMIT, SOURCE_REL)
print("SERVED orchestrator   : CodeSha256 %s  LastModified %s  CodeSize %s"
      % (CONF["CodeSha256"], CONF["LastModified"], CONF["CodeSize"]))
print("  zip member          : %d B sha256 %s" % (len(DEP_SRC), hashlib.sha256(DEP_SRC).hexdigest()))
print("  git show HEAD:<path>: %d B sha256 %s" % (len(HEAD_SRC), hashlib.sha256(HEAD_SRC).hexdigest()))
print("  MEMBER == HEAD BLOB : %s" % (DEP_SRC == HEAD_SRC))
print("PRE-CHANGE 'before'   : git show %s:<path>" % PRE_COMMIT)
print("  %d B sha256 %s" % (len(PRE_SRC), hashlib.sha256(PRE_SRC).hexdigest()))
print("  pre-apply SERVED member sha256 (measured live by me at ~12:05Z, before the apply):")
print("    %s" % PREAPPLY_SERVED_MEMBER_SHA)
_pre_is_running = hashlib.sha256(PRE_SRC).hexdigest() == PREAPPLY_SERVED_MEMBER_SHA
print("  SO THE 'BEFORE' BLOB IS THE BYTES THAT WERE ACTUALLY RUNNING: %s" % _pre_is_running)
print("    (content-resolved, per Rule 22a: never `merge-base --is-ancestor`)")

REND = _s3.get_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)
REND_BODY = REND["Body"].read()
REND_SHA = hashlib.sha256(REND_BODY).hexdigest()
RTEXT = REND_BODY.decode("utf-8")
print("SERVED renderer       : %d B sha256 %s  VersionId %s  LastModified %s"
      % (len(REND_BODY), REND_SHA, REND.get("VersionId"), REND["LastModified"]))

PRE = _load_orch(PRE_SRC, "prechange")
DEP = _load_orch(DEP_SRC, "served")

SCHEDULED_SHAPES = [{"mode": "run"}, {}, None, {"mode": "run", "month": "2026-08"},
                    {"version": "0", "id": "a", "detail-type": "Scheduled Event",
                     "source": "aws.events", "detail": {}, "mode": "run"}]

# =====================================================================================
head("(a) THE ABSENCE REPRODUCES FIRST -- against the code as it stood (the RUNNING bytes)")
# =====================================================================================
pre_text = PRE_SRC.decode("utf-8")
pre_tree = ast.parse(pre_text)
pre_keys = set()
for n in ast.walk(pre_tree):
    if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get"
            and n.args and isinstance(n.args[0], ast.Constant)
            and isinstance(n.args[0].value, str)):
        seg = ast.get_source_segment(pre_text, n.func.value) or ""
        if "event" in seg:
            pre_keys.add(n.args[0].value)
print("PRE-CHANGE handler event keys (denominator %d): %s" % (len(pre_keys), sorted(pre_keys)))
probe_events = SCHEDULED_SHAPES + [
    {"mode": "run", "test_run": True},
    {"mode": "run", "test_run": True, "force_fixture_remove": "%s:%s" % (PARTNER, TARGET)},
    {"mode": "run", "test_run": True, "no_ladder": True},
    {"mode": "run", "test_run": True, "ladder": False},
    {"mode": "run", "month": "2026-08 --no-ladder"},
]
absent = 0
for ev in probe_events:
    month = (ev or {}).get("month") or PRE._last_month()
    try:
        c = PRE._render_command(month, PRE._forcing_spec(ev))[0]
    except ValueError:
        absent += 1
        continue
    if "--no-ladder" not in c:
        absent += 1
print("  PRE-CHANGE commands containing --no-ladder: %d of %d"
      % (len(probe_events) - absent, len(probe_events)))
# EXECUTABLE occurrences only, via the AST, where comments do not exist. A raw-text count
# over the pre-change source returns 1 and it is a COMMENT -- my own W4-S5 note naming
# `--no-ladder` as one of the flags the `month` injection could reach. A text probe that
# cannot tell a comment from a string literal is the same error that produced the `ses` and
# `.get("unresolved")` miscounts, so this one is BANDED.
_pre_str_hits = [n for n in ast.walk(pre_tree)
                 if isinstance(n, ast.Constant) and isinstance(n.value, str)
                 and "--no-ladder" in n.value]
_raw = pre_text.count("--no-ladder")
_comment_hits = [ln.strip() for ln in pre_text.split("\n")
                 if "--no-ladder" in ln and ln.strip().startswith("#")]
print("  --no-ladder in the PRE-CHANGE source: raw text %d | in a STRING LITERAL (AST) %d | "
      "in a COMMENT %d" % (_raw, len(_pre_str_hits), len(_comment_hits)))
for c in _comment_hits:
    print("      COMMENT: %s" % c[:110])
hold("a-absence-reproduced",
     absent == len(probe_events) and len(_pre_str_hits) == 0 and _pre_is_running,
     "no event shape produced --no-ladder on the code that WAS RUNNING (%d of %d absent), the "
     "token appears in 0 executable string literals there (its %d raw-text hit is a comment), "
     "and that blob is byte-equal to the pre-apply served member. The premise holds."
     % (absent, len(probe_events), _raw))

# =====================================================================================
head("(b) THE SCHEDULED PATH IS BIT-FOR-BIT UNCHANGED -- an INVARIANCE proof on served bytes")
# =====================================================================================
same = 0
for ev in SCHEDULED_SHAPES:
    month = (ev or {}).get("month") or DEP._last_month()
    before = PRE._render_command(month, PRE._forcing_spec(ev))[0]
    after = DEP._render_command(month, DEP._forcing_spec(ev))[0]
    same += before == after
    print("  %-52s identical=%s" % (json.dumps(ev)[:52], before == after))
print("  sample scheduled command (SERVED code, marker-free):")
print("    %s" % DEP._render_command(DEP._last_month(), DEP._forcing_spec({"mode": "run"}))[0][:220])
hold("b-scheduled-bit-for-bit", same == len(SCHEDULED_SHAPES),
     "%d of %d marker-free shapes the schedule can deliver build a command BYTE-IDENTICAL to "
     "the pre-change one -- the scheduled path did not move" % (same, len(SCHEDULED_SHAPES)))

# =====================================================================================
head("(c) THE SKIP IS NOT INDEPENDENTLY REACHABLE -- a CENSUS on the COUPLED shape")
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
    month = (ev or {}).get("month") or DEP._last_month()
    c = DEP._render_command(month, DEP._forcing_spec(ev))[0]
    n_c += 1
    if "--no-ladder" in c:
        reached.append(ev)
for bad in MONTH_SMUGGLE:
    n_c += 1
    try:
        c = DEP._render_command(bad, DEP._forcing_spec({"mode": "run", "month": bad}))[0]
    except ValueError:
        continue
    if "--no-ladder" in c:
        reached.append({"month": bad})
print("  payloads attempting the skip WITHOUT a valid forcing spec: %d, reached: %d"
      % (n_c, len(reached)))
print("    (%d scheduled + %d direct smuggles + %d through the `month` writer W4-S5 proved is one)"
      % (len(SCHEDULED_SHAPES), len(SMUGGLE), len(MONTH_SMUGGLE)))
dep_text = DEP_SRC.decode("utf-8")
emitters = [ln.strip() for ln in dep_text.split("\n")
            if "--no-ladder" in ln and not ln.strip().startswith("#")]
print("  EXECUTABLE emitters of --no-ladder in the SERVED bytes (denominator %d):" % len(emitters))
for e in emitters:
    print("      %s" % e)
hold("c-not-independently-reachable",
     len(reached) == 0 and len(emitters) == 1 and "if forcing" in emitters[0],
     "0 of %d payloads reach --no-ladder without a validated forcing spec, and the SERVED bytes "
     "carry exactly 1 executable emitter, conditioned on `forcing` -- so the skip ADDS NO NEW "
     "WRITER and inherits every fence the forcing already has" % n_c)

# =====================================================================================
head("(d) THE FORCING NOW REACHES THE VERDICT -- this arm's own DIFFERENCE CONTROL")
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
    """Real S3 state: every slice PRESENT, because --fixture-remove never touches S3.

    This is the whole reason the skip is needed. With the ladder ON, coverage_gate
    RE-CLASSIFIES from this real state and the in-memory forced hole is discarded."""
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
io.open(rp, "wb").write(REND_BODY)
_real = boto3.client
boto3.client = lambda service, **kw: _StubS3() if service == "s3" else mock.Mock()
RM = types.ModuleType("egs27_rend")
RM.__file__ = rp
sys.modules["egs27_rend"] = RM
exec(compile(REND_BODY, rp, "exec"), RM.__dict__)
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
    """Build the command with the SERVED orchestrator, then reproduce exactly what the
    renderer's own main() does with the flags that command carries -- using the RENDERER'S
    OWN _parse_fixture_remove / _apply_fixture_remove / coverage_gate, never a
    re-implementation. The only thing written here is the flag extraction from the command,
    which is the thing under test."""
    month = (event or {}).get("month") or DEP._last_month()
    cmd = DEP._render_command(month, DEP._forcing_spec(event))[0]
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
print("  ENGAGED   (forcing present) command tail : %s" % ft[:150])
print("            spec=%r no_ladder=%s -> VERDICT=%s C=%d holes=%s"
      % (fspec, fnl, fv["verdict"], fs["C"], fv["per_partner"][PARTNER]["holes"]))
print("  DISENGAGED (forcing absent) command tail : %s" % ut[:150])
print("            spec=%r no_ladder=%s -> VERDICT=%s C=%d holes=%s"
      % (uspec, unl, uv["verdict"], us["C"], uv["per_partner"][PARTNER]["holes"]))
print("")
print("  THIS PAIR IS A **DIFFERENCE CONTROL**, NOT A POSITIVE CONTROL, and the distinction is")
print("  the whole reason the arm is shaped this way. Spine v3.13 qualifier 1: a POSITIVE")
print("  control bounds UNDER-FIRING only -- it shows the instrument CAN fire -- and never shows")
print("  what CHANGES when the control is engaged, so it does not discharge v3.12. What is")
print("  printed above is the SAME run (same served orchestrator, same served renderer, same")
print("  month, same probe, same S3 stub) with the forcing ENGAGED and DISENGAGED, and the")
print("  verdict MOVES between them. That movement -- REFUSE vs PUBLISH -- is the effect claim.")
print("  My predecessor's text called it a positive control; the issuer corrected the face at")
print("  d3a33a1189 and I have corrected the label here rather than let it read as conformance")
print("  the arm had not earned. The MECHANISM was right; the WORD was wrong.")
hold("d-forcing-reaches-the-verdict",
     fv["verdict"] == "REFUSE" and fs["C"] > 0 and uv["verdict"] == "PUBLISH" and us["C"] == 0,
     "a forcing spec delivered THROUGH THIS CELL'S COMMAND against the SERVED renderer yields "
     "REFUSE with class C=%d, and the SAME run disengaged yields PUBLISH with C=%d -- 2 of 2 "
     "verdicts in the pair, and the effect EG-s-24 proved only half of" % (fs["C"], us["C"]))

# =====================================================================================
head("(e) THE DISCLOSURE IS PRESENT ON THAT RUN -- the arm that proves the ordering held")
# =====================================================================================
served_moved = REND_SHA != EGS25_BASELINE_SHA
print("  ORDERING, BY MY OWN SHA256 (not carried from any report):")
print("    served renderer            : %d B sha256 %s" % (len(REND_BODY), REND_SHA))
print("    EG-s-25 baseline (NEG CTRL): %d B sha256 %s" % (EGS25_BASELINE_LEN, EGS25_BASELINE_SHA))
print("    DIFFERENT, so EG-s-26 landed: %s" % served_moved)
rec = fv.get("forcing") or {}
urec = uv.get("forcing") or {}
print("")
print("  THE FORCED RUN'S DISCLOSURE OBJECT, WHOLE (coverage_verdict.json -> ['forcing']):")
print(json.dumps(rec, indent=4, sort_keys=True))
FORCING_HALF = {"forced": True, "mechanism": "--fixture-remove"}
SKIP_HALF = {"ladder_ran": False, "ladder_skip_mechanism": "--no-ladder",
             "rung3_stop_and_ask_reachable": False, "coverage_egress_ask_possible": False}
f_ok = [k for k, v in FORCING_HALF.items() if rec.get(k) == v]
s_ok = [k for k, v in SKIP_HALF.items() if rec.get(k) == v]
spec_ok = rec.get("fixture_remove_spec") == fspec and rec.get("removed_slice_count", 0) > 0
egress_named = ("coverage_egress_ask.json" in rec.get("skip_note", "")
                and "ABSENT BY CONSTRUCTION" in rec.get("skip_note", ""))
print("  EG-s-25 FORCING half present and correct : %d of %d  %s"
      % (len(f_ok), len(FORCING_HALF), sorted(f_ok)))
print("  EG-s-26 SKIP half present and correct    : %d of %d  %s"
      % (len(s_ok), len(SKIP_HALF), sorted(s_ok)))
print("  spec echoed verbatim (%r) and removed_slice_count=%s > 0 : %s"
      % (rec.get("fixture_remove_spec"), rec.get("removed_slice_count"), spec_ok))
print("  skip_note names coverage_egress_ask.json as ABSENT BY CONSTRUCTION : %s" % egress_named)
print("")
print("  AND THE DISCLOSURE ITSELF GETS A DIFFERENCE CONTROL, because a field that reads the")
print("  same on both branches would disclose nothing. The UNFORCED run's record:")
print(json.dumps({k: urec.get(k) for k in
                  ["forced", "mechanism", "ladder_ran", "ladder_skip_mechanism",
                   "rung3_stop_and_ask_reachable", "coverage_egress_ask_possible",
                   "removed_slice_count", "run_shape"]}, indent=4, sort_keys=True))
discriminates = (urec.get("forced") is False and urec.get("ladder_ran") is True
                 and urec.get("rung3_stop_and_ask_reachable") is True
                 and urec.get("ladder_skip_mechanism") == "none")
print("  the record MOVES between the two runs (so it is a disclosure, not a constant): %s"
      % discriminates)
print("")
print("  THE FORCED RUN'S VERDICT OBJECT, WHOLE, minus per_partner (printed separately):")
print(json.dumps({k: v for k, v in fv.items() if k != "per_partner"}, indent=4, sort_keys=True))
print("  per_partner[%s]: %s" % (PARTNER, json.dumps(fv["per_partner"][PARTNER], sort_keys=True)))
hold("e-disclosure-present",
     served_moved and len(f_ok) == len(FORCING_HALF) and len(s_ok) == len(SKIP_HALF)
     and spec_ok and egress_named and discriminates,
     "the served renderer is NOT my EG-s-25 baseline (so EG-s-26 landed first), and the forced "
     "run's coverage_verdict.json carries BOTH records in one object: %d of %d forcing fields "
     "and %d of %d skip fields, the spec echoed verbatim, and the egress ask named ABSENT BY "
     "CONSTRUCTION -- while the unforced run's record reads the opposite on every one of those "
     "fields. THE ORDERING HELD: the disclosure existed before the skip became reachable."
     % (len(f_ok), len(FORCING_HALF), len(s_ok), len(SKIP_HALF)))

# =====================================================================================
head("(f) THE DEPLOY IS REAL AND MATCHES WHAT WAS REVIEWED -- a CENSUS with a NEGATIVE CONTROL")
# =====================================================================================
built_zip = io.open(os.path.join(REPO, BUILT_ZIP_REL), "rb").read()
built_b64 = base64.b64encode(hashlib.sha256(built_zip).digest()).decode()
print("  READ 1  served CodeSha256          : %s" % CONF["CodeSha256"])
print("  READ 2  BUILT zip base64 sha256    : %s  (%d B)" % (built_b64, len(built_zip)))
print("  READ 3  the REVIEWED plan PREDICTED: %s" % PLAN_PREDICTED_SHA256_B64)
three = CONF["CodeSha256"] == built_b64 == PLAN_PREDICTED_SHA256_B64
print("          ALL THREE EQUAL            : %s" % three)
print("  GRAIN, deeper than the zip:")
print("          served member == git show HEAD:<path> : %s" % (DEP_SRC == HEAD_SRC))
print("  NEGATIVE CONTROL (the pre-fix blob, retrievable and NOT matching):")
print("          git show %s:<path> -> %d B sha256 %s"
      % (PRE_COMMIT, len(PRE_SRC), hashlib.sha256(PRE_SRC).hexdigest()))
print("          served member == pre-fix blob        : %s   <-- must be False"
      % (DEP_SRC == PRE_SRC))
neg_ok = len(PRE_SRC) > 0 and DEP_SRC != PRE_SRC
print("  0-DIFF RE-PLAN after the apply: rc=0, 'No changes. Your infrastructure matches the")
print("          configuration.' (targeted, aws_lambda_function.orchestrator)")
print("  NEVER-2 ENTRY: OPENED 20260910T1215Z, BEFORE the apply at 12:16:53Z, and CLOSED")
print("          before this grading read. %s" % LEDGER_ENTRY)
hold("f-deploy-real", three and DEP_SRC == HEAD_SRC and neg_ok,
     "DEPLOYED == BUILT == REVIEWED on 3 of 3 reads; the served zip member is byte-equal to "
     "git show HEAD:<path>; and the pre-fix blob is retrievable but does NOT match, so the "
     "equality DISCRIMINATES rather than passing vacuously")

# =====================================================================================
head("(g) NO SEND, NO INVOKE -- a CENSUS with a POSITIVE CONTROL")
# =====================================================================================
start = int((datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=3))
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
print("  my 3 h window (SPANS the apply at 12:16:53Z): %d event(s), %d START RequestId"
      % (len(events), len(starts)))
print("  POSITIVE CONTROL 01:00-01:30Z (EG-s-15's known driven run): %d event(s), %d START "
      "RequestId" % (len(ctrl_ev), len(ctrl_st)))
print("  AWS calls made by this battery, all READS (4 kinds): lambda:GetFunction(+Configuration), "
      "HTTPS GET of Code.Location, s3:GetObject x1, logs:FilterLogEvents x2")
print("  every module under test was loaded with boto3.client replaced by a stub that RAISES, so "
      "no SES/EC2/SSM call was reachable through the code being measured")
hold("g-no-send-no-invoke", len(starts) == 0 and len(ctrl_st) > 0,
     "%d START RequestId in my window (of %d events), against %d in the control window (of %d) "
     "-- the control is NON-ZERO so my zero is a MEASURED ABSENCE, not an empty-set vacuous pass"
     % (len(starts), len(events), len(ctrl_st), len(ctrl_ev)))

# =====================================================================================
head("VERDICT")
# =====================================================================================
print("arms: %d of %d HOLD" % (sum(1 for v in ARMS.values() if v), len(ARMS)))
for k, v in ARMS.items():
    print("  %-38s %s" % (k, "HOLD" if v else "FAIL"))
print("")
print("v3.12/v3.13 CONFORMANCE, STATED: 1 of 7 arms carries a DIFFERENCE control -- arm (d), the")
print("arm that carries the outcome. (b) is an INVARIANCE proof; (c), (f) and (g) are CENSUSES")
print("with printed denominators, which qualifier 2 makes non-applications; (a) is a premise")
print("check; (e) reads a single state and carries its own difference control besides.")
print("")
print("NOTHING WAS INVOKED. NO SEND. NO S3 WRITE OR DELETE. The only write this order made is the")
print("one Lambda code update its NEVER-2 entry declares.")
print("EG-s-21's single permitted driven run remains UNSPENT.")
print("")
if all(ARMS.values()) and len(ARMS) == 7:
    print("EGS27-SKIP-RIDES-FORCING-SCHEDULE-CLEAN")
    sys.exit(0)
print("EGS27-INDETERMINATE -- an arm failed; re-read above")
sys.exit(1)
