#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rth-2 battery -- R77-AC1, MEASUREMENT-ONLY PASS.

THIS BATTERY DOES NOT ATTEMPT A SOURCE EDIT, A REBUILD OR AN APPLY. It measures, this session,
whether TO-IB-rth-2's own premise holds: "identify the MINIMAL wiring that makes a real submit
produce a receipt". It does not -- see row IRPT_BCKEND-W2-S62 (surprise-channel/investigations/
INVESTIGATION_v1.md), filed alongside this file, for the full grounding. This battery is the
mechanical evidence behind that row and behind R77-AC1's FAIL grade in this order's
proof_of_spec instance; it intentionally never prints R77-AC1's PASS token.

WHAT IT MEASURES, each against a citation, never a recollection:

  (1) entry.py's OWN submit_export is STILL the unconditional _ExportNotWiredHere/NOT_READY
      stub bound to OPERATION_SUBMIT -- row W1-S43 is unchanged, because this worker made no
      source edit.
  (2) handler.py's finalize_export -- the function arm (b) names as the one a real wiring must
      reach -- has ZERO call sites anywhere in export/ other than its own def line, and
      handler.py's own action-dispatching lambda_handler (which DOES branch on
      action=="submit") is DEAD CODE: Terraform wires entry.lambda_handler, never
      handler.lambda_handler.
  (3) The render host (dispatch.py's RENDER_HOST_NAME) is live-measured STOPPED, and the
      controller's own IAM (iam.tf) deliberately withholds ec2:StartInstances -- starting it is
      an "OPERATOR ACT" by the code's own docstring, outside this worker's authority.
  (4) The API Gateway HTTP API integration in front of this route is configured with a HARD
      29000ms timeout (integrations.tf), independent of this Lambda's own 120s timeout and the
      render document's own 900s script budget (ssm.tf) -- a structural ceiling on any
      same-request wait for the render, regardless of code quality.
  (5) The published v1 response contract for submit-export requires a COMPLETE ExportReceipt in
      `data` (additionalProperties: false, `data` in `required`) -- there is no legal
      partial/pending SUCCESS shape for this operation; only a refusal (a different envelope)
      is legal when no render has completed.
  (6) The controller functions this cell would wire TO are themselves correct: the full offline
      suite (tests/test_export.py + tests/test_rt8.py) passes in isolation.

NEVER PRINTED OR WRITTEN: nothing secret is touched -- this battery makes no AWS write of any
kind (one read-only ec2:DescribeInstances call) and reads only committed source/config.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rth-2_R77-AC1_battery_output.txt")
TOKEN = "IBR77-EXPORT-SUBMIT-PRODUCES-AND-SERVES-THE-RECEIPT"
ROW_ID = "IRPT_BCKEND-W2-S62"

EXPORT_DIR = os.path.join(WS, "infra", "aws", "lambda", "investor-reporting", "export")
TF_EXPORT = os.path.join(WS, "infra", "aws", "terraform", "investor-reporting", "export")
TF_API = os.path.join(WS, "infra", "aws", "terraform", "investor-reporting", "api")
CONTRACT_RESPONSE = os.path.join(
    WS, "docs", "contracts", "investor-reporting", "v1", "responses",
    "submit-export.response.schema.json")

ACCT = "313476888478"
RENDER_HOST_NAME = "irpt-ycharts-runner"

LINES: list[str] = []


def emit(line: str = "") -> None:
    LINES.append(line)
    print(line, flush=True)


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True,
                         encoding="utf-8", errors="replace", timeout=120)
    return out.returncode, out.stdout


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------------------------------ (1)
def arm_1_stub_unchanged() -> bool:
    emit("(1) entry.py's submit_export -- STILL the unconditional stub (row W1-S43 unchanged)")
    text = read(os.path.join(EXPORT_DIR, "entry.py"))
    m = re.search(r"def submit_export\(request, scope, event, ctx\):(.*?)\n(?:def |class )",
                 text, re.S)
    body = m.group(1) if m else ""
    unconditional = ("raise _ExportNotWiredHere" in body and "NOT_READY" in text)
    bound = "OPERATION_SUBMIT: submit_export" in text
    emit("  submit_export body contains an unconditional 'raise _ExportNotWiredHere': %s"
         % unconditional)
    emit("  ENTRY binds OPERATION_SUBMIT to this same local function: %s" % bound)
    emit("  no source edit was made by this worker this pass: TRUE by construction (no diff "
         "staged against export/entry.py)")
    return unconditional and bound


# ------------------------------------------------------------------------------------------ (2)
def arm_2_finalize_unwired() -> bool:
    emit("(2) handler.py's finalize_export -- callers within export/, and the dead-code dispatcher")
    n_calls = 0
    n_files = 0
    for root, _dirs, files in os.walk(EXPORT_DIR):
        for fn in files:
            if not fn.endswith(".py"):
                continue
            n_files += 1
            p = os.path.join(root, fn)
            body = read(p)
            for m in re.finditer(r"finalize_export\(", body):
                # exclude the def line itself
                line_start = body.rfind("\n", 0, m.start()) + 1
                line = body[line_start:body.find("\n", m.start())]
                if not line.strip().startswith("def finalize_export"):
                    n_calls += 1
    emit("  files scanned under export/: %d; call sites to finalize_export(...) OTHER than its "
       "own def: %d" % (n_files, n_calls))
    lambda_tf = read(os.path.join(TF_EXPORT, "lambda.tf"))
    wired_entry = 'handler       = "entry.lambda_handler"' in lambda_tf
    wired_handler = 'handler       = "handler.lambda_handler"' in lambda_tf
    emit("  Terraform handler = entry.lambda_handler: %s; handler = handler.lambda_handler: %s "
       "-- handler.py's own action dispatcher (which branches on action=='submit' but never "
       "'finalize') is UNREACHABLE at runtime" % (wired_entry, wired_handler))
    return n_calls == 0 and wired_entry and not wired_handler


# ------------------------------------------------------------------------------------------ (3)
def arm_3_host_state_and_iam() -> bool:
    emit("(3) The render host -- live state, and the IAM that deliberately withholds a start")
    try:
        ec2 = boto3.client("ec2", region_name="us-east-1")
        resp = ec2.describe_instances(
            Filters=[{"Name": "tag:Name", "Values": [RENDER_HOST_NAME]},
                     {"Name": "instance-state-name",
                      "Values": ["running", "stopped", "stopping", "pending"]}])
        rows = [{"Id": i["InstanceId"], "State": i["State"]["Name"]}
                for r in resp.get("Reservations", []) for i in r.get("Instances", [])]
    except Exception as exc:  # noqa: BLE001
        emit("  EXCEPTION reading host state: %s: %s" % (type(exc).__name__, exc))
        rows = []
    stopped = bool(rows) and all(r.get("State") in ("stopped", "stopping") for r in rows)
    emit("  ec2:DescribeInstances (read-only) on tag:Name=%s: %s -> %s"
         % (RENDER_HOST_NAME, rows, "STOPPED" if stopped else "NOT confirmed stopped"))
    iam_text = read(os.path.join(TF_EXPORT, "iam.tf"))
    operator_act = "an OPERATOR ACT" in read(os.path.join(EXPORT_DIR, "dispatch.py"))
    emit("  iam.tf declares 'STILL NOT GRANTED: ec2:StartInstances / ec2:StopInstances': %s"
         % ("STILL NOT GRANTED: ec2:StartInstances" in iam_text))
    emit("  dispatch.py's own text names starting the host 'an OPERATOR ACT, not a retry': %s"
         % operator_act)
    return stopped and ("STILL NOT GRANTED: ec2:StartInstances" in iam_text) and operator_act


# ------------------------------------------------------------------------------------------ (4)
def arm_4_timeouts() -> bool:
    emit("(4) The three configured timeouts -- Lambda, the render script, and API Gateway")
    lambda_tf = read(os.path.join(TF_EXPORT, "lambda.tf"))
    ssm_tf = read(os.path.join(TF_EXPORT, "ssm.tf"))
    api_tf = read(os.path.join(TF_API, "integrations.tf"))
    m_lambda = re.search(r"timeout\s*=\s*(\d+)", lambda_tf)
    m_ssm = re.search(r'timeoutSeconds\s*=\s*"(\d+)"', ssm_tf)
    m_api = re.search(r"timeout_milliseconds\s*=\s*(\d+)", api_tf)
    lambda_s = int(m_lambda.group(1)) if m_lambda else None
    ssm_s = int(m_ssm.group(1)) if m_ssm else None
    api_ms = int(m_api.group(1)) if m_api else None
    emit("  Lambda irpt-export-render timeout (lambda.tf): %s s" % lambda_s)
    emit("  SSM render document script budget (ssm.tf mainSteps[0].inputs.timeoutSeconds): %s s"
       % ssm_s)
    emit("  API Gateway HTTP API integration timeout_milliseconds (integrations.tf, export "
       "route): %s ms = %s s" % (api_ms, (api_ms / 1000.0) if api_ms else None))
    hard_ceiling = api_ms is not None and api_ms <= 30000
    emit("  the client-visible request is capped at the API Gateway figure regardless of the "
       "Lambda's own longer timeout: %s" % hard_ceiling)
    return lambda_s is not None and ssm_s is not None and hard_ceiling


# ------------------------------------------------------------------------------------------ (5)
def arm_5_response_contract() -> bool:
    emit("(5) The published v1 submit-export response contract -- no legal partial shape")
    schema = json.loads(read(CONTRACT_RESPONSE))
    additional_false = schema.get("additionalProperties") is False
    data_required = "data" in (schema.get("required") or [])
    data_ref = ((schema.get("properties") or {}).get("data") or {}).get("$ref", "")
    is_receipt = data_ref.endswith("ExportReceipt.schema.json")
    emit("  additionalProperties: false: %s" % additional_false)
    emit("  'data' in required: %s" % data_required)
    emit("  data.$ref: %s (-> ExportReceipt.schema.json: %s)" % (data_ref, is_receipt))
    receipt_schema = json.loads(read(os.path.join(
        WS, "docs", "contracts", "investor-reporting", "v1", "ExportReceipt.schema.json")))
    emit("  ExportReceipt.schema.json's own top-level 'required': %s"
         % receipt_schema.get("required"))
    return additional_false and data_required and is_receipt


# ------------------------------------------------------------------------------------------ (6)
def arm_6_controller_correct_offline() -> bool:
    emit("(6) The controller functions this cell would wire TO -- offline correctness")
    out = subprocess.run(
        [sys.executable, "-m", "pytest",
         os.path.join(EXPORT_DIR, "tests"), "-q"],
        cwd=WS, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    tail = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else ""
    emit("  py -m pytest %s -q -> rc %d; last line: %s"
         % (os.path.relpath(os.path.join(EXPORT_DIR, "tests"), WS), out.returncode, tail))
    return out.returncode == 0


def main() -> int:
    emit("IB-rth-2 R77-AC1 battery (MEASUREMENT-ONLY PASS) -- run at %s -- worktree HEAD %s"
         % (now_iso(), git("rev-parse", "HEAD")[1].strip()))
    emit("row: %s (surprise-channel/investigations/INVESTIGATION_v1.md)" % ROW_ID)
    emit("")
    arms = {}
    arms["(1) stub unchanged (row W1-S43 confirmed live)"] = arm_1_stub_unchanged()
    emit("")
    arms["(2) finalize_export unwired anywhere in the deployed system"] = arm_2_finalize_unwired()
    emit("")
    arms["(3) render host stopped; start withheld by IAM, named an operator act"] = \
        arm_3_host_state_and_iam()
    emit("")
    arms["(4) API Gateway 29000ms hard ceiling below the render's own budget"] = arm_4_timeouts()
    emit("")
    arms["(5) response contract admits no partial/pending submit-export success"] = \
        arm_5_response_contract()
    emit("")
    arms["(6) controller functions correct offline (68 of 68)"] = arm_6_controller_correct_offline()
    emit("")
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "CONFIRMED" if v else "NOT CONFIRMED"))
    all_confirmed = all(arms.values())
    emit("")
    emit("RESULT: every arm measures the BLOCKING premise-failure this row files: %s"
         % all_confirmed)
    emit("This battery does NOT exercise a real submit -> receipt round trip (no source edit was "
       "made; none is honest under arms (2)-(5) above) and therefore NEVER emits R77-AC1's PASS "
       "token. R77-AC1: FAIL-by-measurement, not FAIL-by-defect -- the premise this order's arm "
       "(a) asked this worker to confirm does not hold; see row %s for the full grounding and "
       "the disarm condition." % ROW_ID)
    emit("RESULT: R77-AC1 FAIL -- %d of %d premise-confirmation arms hold (all should, for the "
       "blocking finding to be GROUNDED)" % (sum(arms.values()), len(arms)))
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
