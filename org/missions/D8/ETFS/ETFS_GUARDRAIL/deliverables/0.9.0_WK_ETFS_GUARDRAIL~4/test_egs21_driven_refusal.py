#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-21 -- S21-AC1 battery.

IT DOES NOT INVOKE ANYTHING. Every call it makes is a READ:
lambda:GetFunction(+Configuration), an HTTPS GET of the presigned code location,
and s3:GetObject on the box's renderer artifact and the served coverage documents.

ARM (a), THE PRECONDITION, is measured and HOLDS.

ARMS (b)..(g) CANNOT BE MEASURED, because the cell's forcing premise fails against
the world as deployed. This script measures WHY, so the finding is re-derivable in
one command rather than argued:

  (1) THE ONLY EVENT-DERIVED INPUT to the box's render command is `month`. The
      deployed orchestrator builds a FIXED command --
        python3 render_month_end.py --month {month} --pdf --gate --s3-out {out}
      -- so no forcing spec can reach the classifier through an orchestrator
      invocation, and arm (e) needs the ORCHESTRATOR's refusal branch (the terminal
      send lives in _run, not in the renderer), so a renderer-only SSM run cannot
      substitute.
  (2) THE PRODUCED VERDICT DOCUMENT HAS NO DISCLOSURE FIELD. The renderer the box
      actually pulls carries ZERO occurrences of a forced-condition or run-id token,
      beside positive controls that are non-zero. Adding one is a code change to
      data/etfs/scripts/presentation/render_month_end.py plus a re-upload of the
      artifact -- a file outside this order's <paths> and forbidden by its own
      "NO CODE CHANGE" bound.

Prints EGS21-BLOCKED-NO-FORCING-PATH. It can never print the success token, and
that is deliberate: a battery that could pass without a driven refusal would be
the confident-wrong shape this project exists to kill.
"""
from __future__ import annotations

import ast
import base64
import hashlib
import importlib.util
import io
import json
import os
import re
import sys
import urllib.request
import zipfile

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
FUNCTION = "etfs-reports-orchestrator"
REGION = "us-east-1"
ETFS_BUCKET = "opal-data-etfs"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "ec2/etfs-reports/render_month_end.py"
MONTH = "2026-09"

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
head("0. THE SUBJECT: the DEPLOYED orchestrator and the DEPLOYED renderer")
# =====================================================================================
fn = _lam.get_function(FunctionName=FUNCTION)
CONF = fn["Configuration"]
zip_bytes = urllib.request.urlopen(fn["Code"]["Location"]).read()
ORCH_SRC = zipfile.ZipFile(io.BytesIO(zip_bytes)).read("lambda_function.py")
ORCH_TEXT = ORCH_SRC.decode("utf-8")
ORCH_SHA = hashlib.sha256(ORCH_SRC).hexdigest()
print("orchestrator served CodeSha256 : %s" % CONF["CodeSha256"])
print("orchestrator LastModified      : %s" % CONF["LastModified"])
print("orchestrator zip sha256 (b64)  : %s"
      % base64.b64encode(hashlib.sha256(zip_bytes).digest()).decode())
print("orchestrator lambda_function.py: %d B sha256 %s" % (len(ORCH_SRC), ORCH_SHA))
print("EMAIL_RECIPIENT (live env)     : %s" % CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"])

REND_SRC = _s3.get_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)["Body"].read()
REND_TEXT = REND_SRC.decode("utf-8")
REND_SHA = hashlib.sha256(REND_SRC).hexdigest()
repo_rend = os.path.join(REPO_ROOT, "data", "etfs", "scripts", "presentation",
                         "render_month_end.py")
with io.open(repo_rend, "rb") as fh:
    REPO_REND = fh.read()
print("")
print("THE RENDERER THE BOX ACTUALLY PULLS (GRAIN: the orchestrator's own render command")
print("does `aws s3 cp %s/%s`, so THIS is the deployed renderer -- the repo file is the" % (ARTIFACT_BUCKET, ARTIFACT_KEY))
print("BUILD INPUT, not the artifact):")
print("  s3://%s/%s : %d B sha256 %s" % (ARTIFACT_BUCKET, ARTIFACT_KEY, len(REND_SRC), REND_SHA))
print("  repo build input                    : %d B sha256 %s"
      % (len(REPO_REND), hashlib.sha256(REPO_REND).hexdigest()))
print("  DEPLOYED == BUILT: %s" % (REND_SRC == REPO_REND))

# =====================================================================================
head("(a) THE PRECONDITION, re-taken at THIS run's time on THESE deployed bytes")
# =====================================================================================
scratch = os.path.join(REPO_ROOT, ".scratch")
os.makedirs(scratch, exist_ok=True)
dep_copy = os.path.join(scratch, "egs21_battery_deployed_lambda_function.py")
with io.open(dep_copy, "wb") as fh:
    fh.write(ORCH_SRC)


class _Stub:
    def __init__(self, svc):
        self._svc = svc

    def __getattr__(self, name):
        def _c(**kw):
            raise AssertionError("STUB REFUSAL: %s.%s -- this battery invokes nothing"
                                 % (self._svc, name))
        return _c


_real = boto3.client
boto3.client = lambda service, **kw: _Stub(service)
os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub")
os.environ["EMAIL_RECIPIENT"] = CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"]
_spec = importlib.util.spec_from_file_location("egs21_deployed", dep_copy)
DEP = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(DEP)
boto3.client = _real

ADVERSARIAL = [
    {"mode": "run", "month": MONTH, "test_run": True},
    {"mode": "run", "test_run": True, "test_recipients": ["aj@opalinvest.com"]},
    {"mode": "run", "test_run": True, "test_recipients": "aj@opalinvest.com"},
    {"mode": "run", "test_run": True, "test_recipients": "aj@opalinvest.com,andrew@opalinvest.com"},
    {"mode": "run", "test_run": True, "test_recipients": ["AJ@OpalInvest.COM"]},
    {"mode": "run", "test_run": True, "test_recipients": ["  aj@opalinvest.com  "]},
    {"mode": "run", "test_run": True, "test_recipients": []},
    {"mode": "run", "test_run": True, "test_recipients": None},
    {"mode": "run", "test_run": 1, "month": MONTH},
]
BASES = [("report  (EMAIL_RECIPIENT)", DEP.EMAIL_RECIPIENT),
         ("terminal (TERMINAL_RECIPIENT)", DEP.TERMINAL_RECIPIENT)]
print("deployed constants: TEST_MARKER=%r FORBIDDEN=%s DEFAULTS=%s"
      % (DEP.TEST_MARKER, sorted(DEP.TEST_FORBIDDEN_RECIPIENTS),
         list(DEP.TEST_DEFAULT_RECIPIENTS)))
leaks, checked = 0, 0
for ev in ADVERSARIAL:
    for label, base in BASES:
        header, env = DEP._resolve_recipients(ev, base)
        checked += 1
        if any(a.lower() == "aj@opalinvest.com" for a in env) or "aj@" in header.lower():
            leaks += 1
        print("  %-30s %-58s -> %s" % (label, json.dumps(ev)[:58], env))
sched_h, sched_env = DEP._resolve_recipients({"mode": "run"}, DEP.EMAIL_RECIPIENT)
print("  SCHEDULED (no marker)          %-58s -> %s" % ('{"mode": "run"}', sched_env))
PRECONDITION_CLEAN = (leaks == 0 and checked == len(ADVERSARIAL) * len(BASES))
line("HOLD" if PRECONDITION_CLEAN else "FAIL",
     "aj@opalinvest.com appears in %d of %d resolved test-invocation recipient lists, on the "
     "bytes deployed at %s (sha256 %s)" % (leaks, checked, CONF["LastModified"], ORCH_SHA[:16]))
line("NOTE", "the scheduled path is UNCHANGED and still carries BOTH: %s" % sched_env)

# =====================================================================================
head("(b/c) THE FORCING PREMISE -- BLOCKING FINDING 1: no forcing reaches the classifier")
# =====================================================================================
tree = ast.parse(ORCH_TEXT)
event_keys = set()
for node in ast.walk(tree):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get" and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)):
        src_seg = ast.get_source_segment(ORCH_TEXT, node.func.value) or ""
        if "event" in src_seg:
            event_keys.add(node.args[0].value)
for node in ast.walk(tree):
    if (isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant)
            and isinstance(node.slice.value, str)):
        seg = ast.get_source_segment(ORCH_TEXT, node.value) or ""
        if seg.strip() == "event":
            event_keys.add(node.slice.value)
print("EVENT KEYS the DEPLOYED handler reads (AST over %d nodes; denominator = every"
      % sum(1 for _ in ast.walk(tree)))
print("`event.get(<const>)` / `(event or {}).get(<const>)` / `event[<const>]` site):")
for k in sorted(event_keys):
    print("    %s" % k)
print("  count: %d" % len(event_keys))

i = ORCH_TEXT.index("def _render_command")
cmd_block = ORCH_TEXT[i:i + 2600]
render_line = [ln.strip() for ln in cmd_block.split("\n")
               if "render_month_end.py --month" in ln]
print("")
print("THE BOX'S RENDER COMMAND, quoted from the DEPLOYED orchestrator:")
for ln in render_line:
    print("    %s" % ln)
FORCING_FLAGS = ["--fixture-remove", "--no-ladder", "fixture_remove"]
print("  forcing flags present anywhere in that command: %s"
      % {f: (f in cmd_block) for f in FORCING_FLAGS})
FORCING_UNREACHABLE = all(f not in cmd_block for f in FORCING_FLAGS)
line("BLOCKED" if FORCING_UNREACHABLE else "HOLD",
     "the render command is FIXED at `--month {month} --pdf --gate --s3-out {out}`; no "
     "forcing spec can reach the classifier through an orchestrator invocation")
if FORCING_UNREACHABLE:
    FINDINGS.append("no forcing reaches the classifier through the orchestrator")

print("")
print("THE MECHANISM EXISTS, AND IT IS THE ONE THE FACE PREFERS -- it is simply not")
print("reachable from the orchestrator. In the DEPLOYED renderer:")
# WHITESPACE-COLLAPSED haystack for any DOC PHRASE: a docstring sentence wraps across
# lines, so a raw .count() of it returns 0 and reads as an absence in the world rather
# than as a defect in the probe.
_REND_FLAT = " ".join(REND_TEXT.split())
for tok, hay, why in (
        ("--fixture-remove", REND_TEXT, "the CLI flag -- an input fixture, in memory only"),
        ("nothing on S3 is ever touched", _REND_FLAT,
         "the mechanism's own guarantee, matched on the whitespace-collapsed text"),
        ("_apply_fixture_remove", REND_TEXT, "the applier the gate calls")):
    print("    %-32s occurrences: %d   (%s)" % (tok, hay.count(tok), why))
line("NOTE", "`--fixture-remove` is EG-s-6 QA, in-memory, touches nothing on S3 -- exactly "
             "'an input fixture the classifier reads', which the face prefers over editing a "
             "real month. It is unreachable only because the orchestrator does not thread it.")

print("")
print("AND ARM (e) FORBIDS THE OBVIOUS SUBSTITUTE: the terminal send lives in the")
print("ORCHESTRATOR, not the renderer, so a renderer-only SSM run cannot produce it.")
term_sites = [n + 1 for n, ln in enumerate(ORCH_TEXT.split("\n"))
              if "_send_terminal_unresolved(" in ln]
print("  _send_terminal_unresolved sites in the deployed orchestrator: %s" % term_sites)
# WORD-BOUNDARY AND CALL-SITE TOKENS, never a bare substring: `REND_TEXT.count("ses")`
# matches "uses"/"series"/"closes"/"parses" and reported 12 "SES sends" in a renderer
# that has none -- a number that CONTRADICTED the very claim it was printed to support.
_SES_CALL_TOKENS = ["send_raw_email", "send_email", 'client("ses"', "client('ses'"]
_ses_hits = {t: REND_TEXT.count(t) for t in _SES_CALL_TOKENS}
_ses_word = len(re.findall(r"\bses\b", REND_TEXT))
print("  SES CALL SITES in the DEPLOYED renderer -- denominator: %d call-site token(s) "
      "censused over %d B" % (len(_SES_CALL_TOKENS), len(REND_SRC)))
print("    %s" % _ses_hits)
print("    word-boundary `ses` tokens: %d  (a bare substring count returns %d and is an "
      "ARTIFACT: uses/series/closes)" % (_ses_word, REND_TEXT.count("ses")))
print("  -> the renderer has %d SES call site(s); the terminal send is the ORCHESTRATOR's "
      "alone, which is why a renderer-only SSM run cannot satisfy arm (e)."
      % sum(_ses_hits.values()))

# =====================================================================================
head("(b) BLOCKING FINDING 2: the verdict artifact carries NO disclosure field")
# =====================================================================================
print("The face requires the produced verdict document to carry 'a field naming that this")
print("run's condition was FORCED, with the run id'. Census over the DEPLOYED renderer")
print("(%d B, sha256 %s), with POSITIVE CONTROLS so a zero is an absence and not a dead read:"
      % (len(REND_SRC), REND_SHA[:16]))
DISCLOSURE = ["forced", "FORCED", "is_forced", "run_id", "runid", "run-id", "request_id",
              "requestId", "trigger", "driven"]
CONTROLS = ["generated_at", "fixture_remove", "verdict", "unresolved", "per_partner"]
zero = 0
for t in DISCLOSURE:
    c = REND_TEXT.count(t)
    zero += (c == 0)
    print("    DISCLOSURE  %-12s : %d" % (t, c))
for t in CONTROLS:
    print("    CONTROL     %-12s : %d" % (t, REND_TEXT.count(t)))
print("  denominator: %d disclosure tokens censused, %d of them ZERO; %d positive controls, "
      "all non-zero" % (len(DISCLOSURE), zero, len(CONTROLS)))

verdict_doc = json.loads(_s3.get_object(
    Bucket=ETFS_BUCKET, Key="platinum/reports/%s/coverage_verdict.json" % MONTH)["Body"].read())
print("")
print("  and on the SERVED bytes of the last real run:")
print("    s3://%s/platinum/reports/%s/coverage_verdict.json top-level keys: %s"
      % (ETFS_BUCKET, MONTH, sorted(verdict_doc)))
NO_DISCLOSURE = (zero == len(DISCLOSURE)
                 and not any(k in verdict_doc for k in ("forced", "run_id", "trigger")))
line("BLOCKED" if NO_DISCLOSURE else "HOLD",
     "the deployed renderer has ZERO of %d disclosure tokens (positive controls non-zero) and "
     "the served verdict document carries no such key; producing one is a code change to "
     "data/etfs/scripts/presentation/render_month_end.py -- outside this order's <paths> and "
     "forbidden by its own NO CODE CHANGE bound" % len(DISCLOSURE))
if NO_DISCLOSURE:
    FINDINGS.append("the verdict artifact cannot disclose a forced condition or a run id")

# =====================================================================================
head("(c) WHY AN UNFORCED RUN WOULD PUBLISH, NOT REFUSE")
# =====================================================================================
gate_rule = [(n + 1, ln.strip()) for n, ln in enumerate(REND_TEXT.split("\n"))
             if 'verdict = "REFUSE" if any_c else "PUBLISH"' in ln]
print("THE CLASSIFIER'S OWN RULE, quoted from the DEPLOYED renderer:")
for n, ln in gate_rule:
    print("    render_month_end.py:%d  %s" % (n, ln))
print("  -> the gate refuses on class C ONLY. D and UNKNOWN are reported, never refused.")
print("")
print("THE LAST REAL RUN'S CLASS TABLE, from the served verdict (denominator: %d of %d partners):"
      % (len(verdict_doc["per_partner"]), len(verdict_doc["per_partner"])))
c_total = 0
for p, v in sorted(verdict_doc["per_partner"].items()):
    s = v["summary"]
    c_total += s["C"]
    print("    %-12s A=%d COVERED=%d B=%d C=%d D=%d UNKNOWN=%d  holes=%s"
          % (p, s["A"], s["COVERED"], s["B"], s["C"], s["D"], s["UNKNOWN"], v["holes"]))
print("    verdict=%s holes=%d  | class C across all partners: %d"
      % (verdict_doc["verdict"], verdict_doc["holes"], c_total))
line("BLOCKED", "class C = %d of %d partners on the last real run, so an UNFORCED driven run "
                "PUBLISHES -- it writes the served publish keys and fires the ORDINARY monthly "
                "email, which is exactly what round 1 measured (W1-S22/S23) and proves nothing "
                "about FWD-10" % (c_total, len(verdict_doc["per_partner"])))

# =====================================================================================
head("VERDICT")
# =====================================================================================
print("ARM (a) PRECONDITION : %s" % ("HOLDS -- 0 of %d resolutions reach aj@" % checked
                                     if PRECONDITION_CLEAN else "FAILS"))
print("ARMS (b)-(g)         : NOT MEASURABLE -- the cell's forcing premise fails.")
for f in FINDINGS:
    print("    BLOCKING: %s" % f)
print("")
print("NOTHING WAS INVOKED. NO SEND WAS FIRED. NO S3 KEY WAS WRITTEN OR DELETED.")
print("")
if PRECONDITION_CLEAN and len(FINDINGS) == 2:
    print("EGS21-BLOCKED-NO-FORCING-PATH")
    sys.exit(2)
print("EGS21-INDETERMINATE -- re-read this output; the expected blocking shape did not hold")
sys.exit(1)
