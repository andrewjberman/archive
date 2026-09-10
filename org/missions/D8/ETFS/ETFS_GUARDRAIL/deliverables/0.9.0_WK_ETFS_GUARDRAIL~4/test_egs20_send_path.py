#!/usr/bin/env python3
"""ETFS_GUARDRAIL.TO-EG-s-20 -- S20-AC2 battery.

EVERY ARM READS THE DEPLOYED BYTES OR LIVE STATE. The worktree copy is never the
subject (Rule 22a: diff deployed bytes against the BUILD INPUT, never by filename).
The function's own code zip is fetched from `lambda:GetFunction`'s presigned
`Code.Location`, its `lambda_function.py` member is hashed, and every code arm is
taken against THAT text -- parsed, imported and executed.

Prints EGS20-SEND-PATH-CORRECT-AND-TEST-SAFE only when every arm holds.

NO SEND AND NO INVOCATION OF etfs-reports-orchestrator IS FIRED BY THIS SCRIPT.
Every AWS call it makes is a READ: lambda:GetFunction(Configuration), an HTTPS GET
of the presigned code location, s3:GetObject on three served coverage artifacts.
The imported module's boto3 clients are STUBS installed before import, so no code
path inside it can reach AWS even if one were taken.
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

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, *([".."] * 7)))
FUNCTION = "etfs-reports-orchestrator"
REGION = "us-east-1"
ETFS_BUCKET = "opal-data-etfs"
MONTH = "2026-09"
TF_DIR = os.path.join(REPO_ROOT, "infra", "aws", "terraform", "etfs-reports")
TF_BIN = os.path.join(REPO_ROOT, ".tools", "terraform.exe")
ENTRY = os.path.join(REPO_ROOT, "org", "critical_paths", "change_management",
                     "20260910T0347Z_etfs-guardrail-eg-s-20-send-path_deploy_completion.md")
PLAN_TRANSCRIPT = os.path.join(HERE, "EG-s-20_preapply_plan_transcript.txt")
SOURCE_PATH_IN_REPO = "infra/aws/lambda/etfs-reports-orchestrator/lambda_function.py"

FAILURES = []
ARMS = {}


def hold(arm, ok, why):
    ARMS[arm] = bool(ok)
    if not ok:
        FAILURES.append("%s: %s" % (arm, why))
    print("  [%s] %s -- %s" % ("HOLD" if ok else "FAIL", arm, why))


def head(title):
    print("")
    print("=" * 78)
    print(title)
    print("=" * 78)


def run(cmd, cwd=None, timeout=300):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=timeout)
    out = (p.stdout or b"").decode("utf-8", "replace") + (p.stderr or b"").decode("utf-8", "replace")
    return p.returncode, out


# =====================================================================================
head("0. THE SUBJECT: the DEPLOYED bytes, fetched now")
# =====================================================================================
import boto3  # noqa: E402

_lam = boto3.client("lambda", region_name=REGION)
_s3_real = boto3.client("s3", region_name=REGION)

fn = _lam.get_function(FunctionName=FUNCTION)
CONF = fn["Configuration"]
zip_bytes = urllib.request.urlopen(fn["Code"]["Location"]).read()
zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
DEPLOYED_SRC_BYTES = zf.read("lambda_function.py")
DEPLOYED_SRC = DEPLOYED_SRC_BYTES.decode("utf-8")
DEPLOYED_LINES = DEPLOYED_SRC.split("\n")
DEPLOYED_MEMBER_SHA = hashlib.sha256(DEPLOYED_SRC_BYTES).hexdigest()
SERVED_CODE_SHA256_B64 = CONF["CodeSha256"]
ZIP_SHA256_B64 = base64.b64encode(hashlib.sha256(zip_bytes).digest()).decode()

print("FunctionName            : %s" % CONF["FunctionName"])
print("served CodeSha256       : %s" % SERVED_CODE_SHA256_B64)
print("served LastModified     : %s" % CONF["LastModified"])
print("served CodeSize         : %d" % CONF["CodeSize"])
print("zip members             : %s (denominator: %d of %d)"
      % (zf.namelist(), len(zf.namelist()), len(zf.namelist())))
print("deployed lambda_function.py : %d B  sha256 %s" % (len(DEPLOYED_SRC_BYTES), DEPLOYED_MEMBER_SHA))
print("deployed source lines       : %d" % len(DEPLOYED_LINES))
print("EMAIL_RECIPIENT (live env)  : %s" % CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"])
APPLY_UTC = datetime.datetime.strptime(
    CONF["LastModified"], "%Y-%m-%dT%H:%M:%S.%f%z").astimezone(datetime.timezone.utc)
print("APPLY UTC (LastModified)    : %s" % APPLY_UTC.isoformat())


# =====================================================================================
head("(a) BOTH SITES FIXED, quoted from the DEPLOYED source with line numbers")
# =====================================================================================
def find_line(pred):
    for i, line in enumerate(DEPLOYED_LINES, start=1):
        if pred(line):
            return i, line
    return None, None


guard_ln, guard_line = find_line(
    lambda ln: ln.strip() == "unresolved_days = _normalize_unresolved(unresolved_doc)")
qa_ln, qa_line = find_line(
    lambda ln: ln.strip() == 'unresolved_days = _normalize_unresolved(artifacts["unresolved"])')

print("SITE ONE  -- the live guard in _run's refusal branch")
print("  :%d  %s" % (guard_ln or -1, (guard_line or "<ABSENT>").rstrip()))
print("SITE TWO  -- the terminal_qa send-free rehearsal")
print("  :%d  %s" % (qa_ln or -1, (qa_line or "<ABSENT>").rstrip()))
print("  (pre-fix, from the blob deployed until 2026-09-10T01:16:14Z, sha256 dc05ea90c94dc41e...:")
print('   :435  unresolved_days = (unresolved_doc or {}).get("unresolved") or []')
print('   :516  msg = _build_terminal_email(month, unresolved_doc.get("unresolved") or [], artifacts["ask"]))')
hold("a1-site-one-fixed", guard_ln is not None,
     "the live guard calls _normalize_unresolved at :%s" % guard_ln)
hold("a2-site-two-fixed", qa_ln is not None,
     "the terminal_qa rehearsal calls _normalize_unresolved at :%s" % qa_ln)

print("")
print("CENSUS over the DEPLOYED source for reads of the absent key.")
print("  INSTRUMENT 1 -- RAW TEXT (comments and docstrings included):")
raw_get_hits = [(i, ln.strip()) for i, ln in enumerate(DEPLOYED_LINES, start=1)
                if '.get("unresolved")' in ln]
raw_sub_hits = [(i, ln.strip()) for i, ln in enumerate(DEPLOYED_LINES, start=1)
                if '["unresolved"]' in ln]
print("    '.get(\"unresolved\")'  : %d hit(s) / %d lines scanned"
      % (len(raw_get_hits), len(DEPLOYED_LINES)))
for i, t in raw_get_hits:
    print("      :%d  %s" % (i, t[:110]))
print("    '[\"unresolved\"]'      : %d hit(s) / %d lines scanned"
      % (len(raw_sub_hits), len(DEPLOYED_LINES)))
for i, t in raw_sub_hits:
    print("      :%d  %s" % (i, t[:110]))

print("  INSTRUMENT 2 -- AST (a DIFFERENT instrument: comments and docstrings do not exist in it):")
tree = ast.parse(DEPLOYED_SRC)
ast_get_hits, ast_sub_hits = [], []
for node in ast.walk(tree):
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get" and node.args
            and isinstance(node.args[0], ast.Constant) and node.args[0].value == "unresolved"):
        ast_get_hits.append(node)
    if (isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant)
            and node.slice.value == "unresolved"):
        recv = node.value.id if isinstance(node.value, ast.Name) else ast.dump(node.value)[:40]
        ast_sub_hits.append((node.lineno, recv))
total_nodes = sum(1 for _ in ast.walk(tree))
print("    EXECUTABLE `.get(\"unresolved\")` calls : %d  (denominator: %d AST nodes walked)"
      % (len(ast_get_hits), total_nodes))
print("    EXECUTABLE `[\"unresolved\"]` subscripts: %d" % len(ast_sub_hits))
ARTIFACT_MAP_RECEIVERS = {"artifacts", "out"}
bad_sub = [(ln, r) for ln, r in ast_sub_hits if r not in ARTIFACT_MAP_RECEIVERS]
for ln, r in ast_sub_hits:
    kind = ("the ARTIFACTS MAP built by _read_coverage_artifacts (keys verdict/unresolved/ask) "
            "-- NOT a read of the coverage document" if r in ARTIFACT_MAP_RECEIVERS
            else "*** a read of the COVERAGE DOCUMENT's absent key ***")
    print("      :%d  receiver=%s -- %s" % (ln, r, kind))
hold("a3-zero-executable-reads-of-the-absent-key",
     len(ast_get_hits) == 0 and len(bad_sub) == 0,
     "0 executable .get(\"unresolved\") calls and 0 coverage-document [\"unresolved\"] "
     "subscripts; the %d raw-text hits are %d DOCSTRING/COMMENT quotations of the historical "
     "defect and %d artifacts-map reads" % (len(raw_get_hits) + len(raw_sub_hits),
                                            len(raw_get_hits), len(ast_sub_hits)))

print("")
print("UNSCOPED RE-READ of the population (CVO row S11 named it and nobody had measured it):")
print("  _read_coverage_artifacts loads THREE documents; a check scoped to the member that")
print("  was found cannot see the same defect in its siblings. All THREE readers against all")
print("  THREE served writers:")
served_docs = {}
for name in ("coverage_verdict.json", "coverage_unresolved.json", "coverage_egress_ask.json"):
    key = "platinum/reports/%s/%s" % (MONTH, name)
    body = _s3_real.get_object(Bucket=ETFS_BUCKET, Key=key)["Body"].read()
    served_docs[name] = json.loads(body)
    print("    s3://%s/%s -- %d B, top-level keys %s"
          % (ETFS_BUCKET, key, len(body), sorted(served_docs[name])))
reader_census = [
    ("coverage_verdict.json", "verdict", "no key read at all -- the whole document is json.dumps'd "
     "into the alert text", True),
    ("coverage_unresolved.json", "unresolved", "_normalize_unresolved -- partner-keyed, WAS THE "
     "DEFECT, fixed by this order", "unresolved" not in served_docs["coverage_unresolved.json"]),
    ("coverage_egress_ask.json", "ask", "ask.get('asks') + per-row date/partner/provider/class/"
     "reason + ask.get('authorization')",
     "asks" in served_docs["coverage_egress_ask.json"]
     and "authorization" in served_docs["coverage_egress_ask.json"]
     and set(served_docs["coverage_egress_ask.json"]["asks"][0])
     >= {"date", "partner", "provider", "class", "reason"}),
]
for fname, slot, how, ok in reader_census:
    print("    %-28s reader=%-10s %s -- reader/writer AGREE: %s" % (fname, slot, how, ok))
hold("a4-all-three-readers-censused", all(x[3] for x in reader_census),
     "3 of 3 coverage readers checked against the served writers; 1 of 3 was defective "
     "(coverage_unresolved.json) and is the one this order fixes; 2 of 3 were already correct")


# =====================================================================================
head("(b) THE GUARD IS NOW TRUTHY AGAINST REAL SERVED BYTES -- the discriminating pair")
# =====================================================================================
served_unresolved = served_docs["coverage_unresolved.json"]
print("SERVED coverage_unresolved.json (s3://%s/platinum/reports/%s/coverage_unresolved.json):"
      % (ETFS_BUCKET, MONTH))
print("  top-level keys : %s  (denominator: %d of %d)"
      % (sorted(served_unresolved), len(served_unresolved), len(served_unresolved)))
print("  'unresolved' in doc : %s" % ("unresolved" in served_unresolved))

# import the DEPLOYED module (never the worktree), with every boto3 client stubbed
_scratch = os.path.join(REPO_ROOT, ".scratch")
os.makedirs(_scratch, exist_ok=True)
DEPLOYED_COPY = os.path.join(_scratch, "egs20_deployed_lambda_function.py")
with io.open(DEPLOYED_COPY, "wb") as fh:
    fh.write(DEPLOYED_SRC_BYTES)


class _StubClient:
    def __init__(self, service):
        self._service = service

    def __getattr__(self, name):
        def _call(**kwargs):
            raise AssertionError(
                "STUB REFUSAL: the imported deployed module tried %s.%s -- this battery makes "
                "no AWS call through it" % (self._service, name))
        return _call


_real_boto_client = boto3.client
boto3.client = lambda service, **kw: _StubClient(service)
os.environ.setdefault("REPORTER_INSTANCE_ID", "i-0000000000000stub")
os.environ.setdefault("REPORTS_SNS_TOPIC", "arn:aws:sns:us-east-1:000000000000:stub-topic")
os.environ["EMAIL_RECIPIENT"] = CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"]
_spec = importlib.util.spec_from_file_location("egs20_deployed", DEPLOYED_COPY)
DEP = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(DEP)
boto3.client = _real_boto_client
print("  imported the DEPLOYED source as a module (sha256 %s), boto3 clients STUBBED"
      % DEPLOYED_MEMBER_SHA[:16])

pre_fix = (served_unresolved or {}).get("unresolved") or []
post_fix = DEP._normalize_unresolved(served_unresolved)
print("")
print("  PRE-FIX  expression  (unresolved_doc or {}).get(\"unresolved\") or []")
print("      -> %r   len=%d   guard truthy: %s" % (pre_fix, len(pre_fix), bool(pre_fix)))
print("  POST-FIX expression  _normalize_unresolved(unresolved_doc)")
print("      -> len=%d   guard truthy: %s" % (len(post_fix), bool(post_fix)))
for row in post_fix:
    print("         %s | %s | %s | %s" % (row.get("date"), row.get("partner"),
                                          row.get("class"), (row.get("reason") or "")[:60]))
hold("b1-pre-fix-guard-falsy-on-real-bytes", not pre_fix,
     "the pre-fix expression evaluates to [] against the real served document -- the defect")
hold("b2-post-fix-guard-truthy-on-real-bytes", bool(post_fix) and len(post_fix) == 2,
     "the post-fix guard evaluates TRUTHY with %d row(s), each carrying its partner" % len(post_fix))

qa = DEP.handler({"mode": "terminal_qa", "month": MONTH}, None) if False else None
DEP._read_coverage_artifacts = lambda month: {
    "verdict": served_docs["coverage_verdict.json"],
    "unresolved": served_unresolved,
    "ask": served_docs["coverage_egress_ask.json"]}
qa = DEP.handler({"mode": "terminal_qa", "month": MONTH}, None)
print("")
print("  THE REHEARSAL, run on the DEPLOYED code over the SAME served bytes (send-free):")
print("    %s" % json.dumps({k: v for k, v in qa.items() if k != "body_head"}))
hold("b3-rehearsal-reports-the-real-count", qa.get("unresolved_count") == 2,
     "terminal_qa now reports unresolved_count=%s over the real month -- pre-fix this same input "
     "returned a clean ok:true over an EMPTY table" % qa.get("unresolved_count"))


# =====================================================================================
head("(c) THE RECIPIENT PROPERTY, BOTH DIRECTIONS, resolved from the DEPLOYED bytes")
# =====================================================================================
print("Andrew-direct 2026-09-10 ~02:5xZ, verbatim: \"make sure no test run hits aj's email,")
print("that is not appropriate.\"")
print("")
print("PRODUCER'S SET (the Lambda's live environment): EMAIL_RECIPIENT = %s"
      % CONF["Environment"]["Variables"]["EMAIL_RECIPIENT"])
print("DEPLOYED constants: TEST_MARKER=%r TEST_FORBIDDEN_RECIPIENTS=%s TEST_DEFAULT_RECIPIENTS=%s"
      % (DEP.TEST_MARKER, sorted(DEP.TEST_FORBIDDEN_RECIPIENTS), list(DEP.TEST_DEFAULT_RECIPIENTS)))

TEST_EVENTS = [
    {"mode": "run", "test_run": True},
    {"mode": "run", "test_run": True, "test_recipients": ["aj@opalinvest.com"]},
    {"mode": "run", "test_run": True, "test_recipients": "aj@opalinvest.com"},
    {"mode": "run", "test_run": True, "test_recipients": "aj@opalinvest.com,andrew@opalinvest.com"},
    {"mode": "run", "test_run": True, "test_recipients": ["AJ@OpalInvest.COM"]},
    {"mode": "run", "test_run": True, "test_recipients": ["  aj@opalinvest.com  "]},
    {"mode": "run", "test_run": True, "test_recipients": ["aj@opalinvest.com", "aj@opalinvest.com"]},
    {"mode": "run", "test_run": True, "test_recipients": []},
    {"mode": "run", "test_run": True, "test_recipients": None},
    {"mode": "run", "test_run": True, "test_recipients": ["qa@opalinvest.dev"]},
    {"mode": "run", "test_run": 1, "month": "2026-09"},
    {"mode": "terminal_qa", "test_run": True, "test_recipients": ["aj@opalinvest.com"]},
]
BASES = [("report  (EMAIL_RECIPIENT)", DEP.EMAIL_RECIPIENT),
         ("terminal (TERMINAL_RECIPIENT)", DEP.TERMINAL_RECIPIENT)]
print("")
print("TEST-INVOCATION RESOLUTION -- every branch, adversarial (denominator: %d event(s) x %d "
      "recipient carrier(s) = %d resolution(s)):"
      % (len(TEST_EVENTS), len(BASES), len(TEST_EVENTS) * len(BASES)))
leaks = []
checked = 0
for ev in TEST_EVENTS:
    for label, base in BASES:
        header, envelope = DEP._resolve_recipients(ev, base)
        checked += 1
        if any(a.lower() == "aj@opalinvest.com" for a in envelope) or "aj@" in header.lower():
            leaks.append((ev, label, envelope))
        print("  %-30s %-72s -> %s" % (label, json.dumps(ev)[:72], envelope))
hold("c1-test-invocation-cannot-reach-aj", not leaks and checked == len(TEST_EVENTS) * len(BASES),
     "aj@opalinvest.com appears in 0 of %d resolved test-invocation recipient lists" % checked)

print("")
print("SCHEDULED-INVOCATION RESOLUTION -- UNCHANGED (the EventBridge schedule's own input is")
print("jsonencode({mode = \"run\"}), which carries no marker):")
sched_ok = True
SCHED_EVENTS = [{"mode": "run"}, {}, None, {"mode": "run", "month": "2026-09"},
                {"mode": "absence_check"}]
for ev in SCHED_EVENTS:
    header, envelope = DEP._resolve_recipients(ev, DEP.EMAIL_RECIPIENT)
    print("  report   %-40s -> header=%r envelope=%s" % (json.dumps(ev), header, envelope))
    if envelope != ["aj@opalinvest.com", "andrew@opalinvest.com"] or header != DEP.EMAIL_RECIPIENT:
        sched_ok = False
t_header, t_env = DEP._resolve_recipients({"mode": "run"}, DEP.TERMINAL_RECIPIENT)
print("  terminal %-40s -> header=%r envelope=%s" % ('{"mode": "run"}', t_header, t_env))
print("  EMAIL_RECIPIENTS (the module's own derivation, unchanged): %s" % DEP.EMAIL_RECIPIENTS)
hold("c2-scheduled-invocation-unchanged-and-joint",
     sched_ok and t_env == ["andrew@opalinvest.com"]
     and DEP.EMAIL_RECIPIENTS == ["aj@opalinvest.com", "andrew@opalinvest.com"],
     "the scheduled payload still resolves to BOTH recipients in order across %d payload shape(s), "
     "and the terminal path stays andrew@-only" % len(SCHED_EVENTS))

print("")
print("AND A TEST INVOCATION THAT FILTERS TO EMPTY SENDS NOTHING (no silent substitution):")
sent = []
DEP._ses = type("S", (), {"send_raw_email": staticmethod(
    lambda **kw: sent.append(kw) or {"MessageId": "unreachable"})})()
DEP._send_terminal_unresolved(MONTH, post_fix, served_docs["coverage_egress_ask.json"],
                              {"test_run": True, "test_recipients": ["aj@opalinvest.com"]})
print("  send_raw_email calls after a test invocation whose only recipient is forbidden: %d" % len(sent))
hold("c3-empty-test-envelope-sends-nothing", len(sent) == 0,
     "0 SES calls when the test branch filters every recipient away")
sent2 = []
DEP._ses = type("S", (), {"send_raw_email": staticmethod(
    lambda **kw: sent2.append(kw) or {"MessageId": "0100-battery-stub"})})()
DEP._send_terminal_unresolved(MONTH, post_fix, served_docs["coverage_egress_ask.json"],
                              {"test_run": True})
print("  a DEFAULT test invocation's terminal send -> %d call(s), Destinations=%s"
      % (len(sent2), sent2[0]["Destinations"] if sent2 else None))
hold("c4-default-test-invocation-reaches-andrew-only",
     len(sent2) == 1 and sent2[0]["Destinations"] == ["andrew@opalinvest.com"],
     "a default test invocation's terminal send carries exactly ['andrew@opalinvest.com'] "
     "-- which is what EG-s-21's driven refusal needs")


# =====================================================================================
head("(d) DEPLOYED == BUILT")
# =====================================================================================
rc, committed = run(["git", "show", "HEAD:%s" % SOURCE_PATH_IN_REPO], cwd=REPO_ROOT)
committed_bytes = subprocess.run(["git", "show", "HEAD:%s" % SOURCE_PATH_IN_REPO],
                                 cwd=REPO_ROOT, capture_output=True).stdout
COMMITTED_SHA = hashlib.sha256(committed_bytes).hexdigest()
rc_h, head_hash = run(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT)
print("committed blob HEAD:%s" % SOURCE_PATH_IN_REPO)
print("  %d B  sha256 %s   (git show rc=%d, HEAD %s)"
      % (len(committed_bytes), COMMITTED_SHA, rc, head_hash.strip()))
print("deployed zip member lambda_function.py")
print("  %d B  sha256 %s" % (len(DEPLOYED_SRC_BYTES), DEPLOYED_MEMBER_SHA))
print("served CodeSha256 (whole zip, base64) : %s" % SERVED_CODE_SHA256_B64)
print("fetched zip sha256 (base64)           : %s" % ZIP_SHA256_B64)
print("NEGATIVE CONTROL -- the PRE-FIX blob at ea47e92a72 must NOT match:")
prefix_bytes = subprocess.run(["git", "show", "ea47e92a72:%s" % SOURCE_PATH_IN_REPO],
                              cwd=REPO_ROOT, capture_output=True)
PREFIX_SHA = hashlib.sha256(prefix_bytes.stdout).hexdigest()
print("  %d B  sha256 %s   (rc=%d)  equal to deployed: %s"
      % (len(prefix_bytes.stdout), PREFIX_SHA, prefix_bytes.returncode,
         PREFIX_SHA == DEPLOYED_MEMBER_SHA))
hold("d1-deployed-equals-committed",
     len(committed_bytes) > 0 and COMMITTED_SHA == DEPLOYED_MEMBER_SHA,
     "the deployed zip member's sha256 equals the committed blob's")
hold("d2-served-equals-fetched-zip", SERVED_CODE_SHA256_B64 == ZIP_SHA256_B64,
     "the served CodeSha256 equals the base64 sha256 of the zip actually fetched")
hold("d3-negative-control-prefix-differs",
     prefix_bytes.returncode == 0 and len(prefix_bytes.stdout) > 0
     and PREFIX_SHA != DEPLOYED_MEMBER_SHA,
     "the pre-fix blob is retrievable (%d B) and does NOT match -- the equality above "
     "discriminates" % len(prefix_bytes.stdout))


# =====================================================================================
head("(e) THE NEVER-2 ENTRY: OPEN before the apply, CLOSED AND COMMITTED before these reads")
# =====================================================================================
entry_text = io.open(ENTRY, "r", encoding="utf-8").read()
m_open = re.search(r"\*\*Date opened:\*\*\s*(\S+)", entry_text)
opened_at = datetime.datetime.fromisoformat(m_open.group(1)).astimezone(datetime.timezone.utc)
status_line = re.search(r"\*\*Status:\*\*\s*(.+)", entry_text).group(1).strip()
print("entry   : %s" % os.path.relpath(ENTRY, REPO_ROOT).replace("\\", "/"))
print("opened  : %s" % opened_at.isoformat())
print("apply   : %s   (the served function's own LastModified)" % APPLY_UTC.isoformat())
print("status  : %s" % status_line[:150])
rc_l, log_out = run(["git", "log", "--full-history", "--format=%H %cI %s",
                     "--", os.path.relpath(ENTRY, REPO_ROOT).replace("\\", "/")], cwd=REPO_ROOT)
entry_commits = [ln for ln in log_out.strip().split("\n") if ln.strip()]
print("commits touching the entry (denominator: %d):" % len(entry_commits))
for ln in entry_commits:
    print("  %s" % ln[:150])
close_commit = entry_commits[0].split()[0] if entry_commits else ""
open_commit = entry_commits[-1].split()[0] if entry_commits else ""
rc_anc, _ = run(["git", "merge-base", "--is-ancestor", close_commit, "HEAD"], cwd=REPO_ROOT)
print("CLOSE commit %s is an ancestor of HEAD: rc=%d" % (close_commit[:10], rc_anc))
print("OPEN  commit %s" % open_commit[:10])
for token in ("ROLLBACK", "NEVER-WIDEN HALVES", "CodeSha256 M5Dopbky3W1f1j97cqAB403Kh7IofIv"):
    print("  entry names %-46s : %s" % (token, token in entry_text))
hold("e1-entry-opened-before-the-apply", opened_at < APPLY_UTC,
     "opened %s < apply %s" % (opened_at.isoformat(), APPLY_UTC.isoformat()))
hold("e2-entry-closed-and-committed", status_line.startswith("CLOSED")
     and len(entry_commits) >= 2 and rc_anc == 0,
     "status CLOSED, %d commit(s) on the entry, the CLOSE commit an ancestor of HEAD"
     % len(entry_commits))
hold("e3-entry-names-rollback-and-both-halves",
     "ROLLBACK" in entry_text and "NEVER-WIDEN HALVES" in entry_text
     and "M5Dopbky3W1f1j97cqAB403Kh7IofIv" in entry_text,
     "the entry names the rollback, both never-widen halves and the pre-state CodeSha256")


# =====================================================================================
head("(f) THE PLAN: exactly one resource pre-apply, and No changes after")
# =====================================================================================
plan_text = io.open(PLAN_TRANSCRIPT, "r", encoding="utf-8").read()
print("PRE-APPLY PLAN TRANSCRIPT (PRESERVED -- unreproducible after the apply):")
print("  %s  (%d B)" % (os.path.relpath(PLAN_TRANSCRIPT, REPO_ROOT).replace("\\", "/"),
                        len(plan_text)))
for ln in plan_text.split("\n"):
    s = ln.strip()
    if (s.startswith("Plan:") or "will be updated in-place" in s
            or "source_code_hash" in s or s.startswith("PLAN ")):
        print("    | %s" % s)
plan_resources = re.findall(r"^  # (\S+) will be", plan_text, re.M)
print("  resources in the plan (denominator: %d): %s" % (len(plan_resources), plan_resources))
predicted = re.search(r'source_code_hash\s+=\s+"[^"]+"\s+->\s+"([^"]+)"', plan_text)
print("  the hash the plan PREDICTED : %s" % (predicted.group(1) if predicted else "<none>"))
print("  the hash the world SERVES   : %s" % SERVED_CODE_SHA256_B64)
hold("f1-plan-read-exactly-one-resource",
     plan_resources == ["aws_lambda_function.orchestrator"]
     and "Plan: 0 to add, 1 to change, 0 to destroy." in plan_text,
     "the targeted plan carried exactly 1 resource and read "
     "'Plan: 0 to add, 1 to change, 0 to destroy.'")
hold("f2-served-is-what-the-plan-predicted",
     bool(predicted) and predicted.group(1) == SERVED_CODE_SHA256_B64,
     "the served CodeSha256 is exactly the value the reviewed plan said it would become")

print("")
print("POST-APPLY RE-PLAN, run now:")
rc_plan, plan_out = run([TF_BIN, "plan", "-no-color", "-input=false", "-detailed-exitcode",
                         "-target=aws_lambda_function.orchestrator"], cwd=TF_DIR, timeout=420)
no_changes = [ln.strip() for ln in plan_out.split("\n") if "No changes" in ln]
print("  %s plan -detailed-exitcode -target=aws_lambda_function.orchestrator -> rc=%d"
      % (os.path.relpath(TF_BIN, REPO_ROOT).replace("\\", "/"), rc_plan))
for ln in no_changes:
    print("    | %s" % ln)
hold("f3-post-apply-replan-no-changes", rc_plan == 0 and bool(no_changes),
     "rc=%d and 'No changes. Your infrastructure matches the configuration.'" % rc_plan)


# =====================================================================================
head("VERDICT")
# =====================================================================================
print("arms: %d of %d HOLD" % (sum(1 for v in ARMS.values() if v), len(ARMS)))
for name, ok in ARMS.items():
    print("  %-42s %s" % (name, "HOLD" if ok else "FAIL"))
if FAILURES:
    print("")
    for f in FAILURES:
        print("FAILED ARM: %s" % f)
    print("NOT-PROVEN -- one or more arms failed.")
    sys.exit(1)
print("")
print("EGS20-SEND-PATH-CORRECT-AND-TEST-SAFE")
sys.exit(0)
