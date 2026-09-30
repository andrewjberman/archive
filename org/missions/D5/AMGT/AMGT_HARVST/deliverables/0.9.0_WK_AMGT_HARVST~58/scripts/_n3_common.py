"""_n3_common.py -- shared READ-ONLY helpers for HVST-n-3 (AC1 and AC2).

Reads only: Lambda GetFunctionConfiguration, a read-only Invoke of opal-amgt-scoped-api (GET
lead-panel/rankings), and the producer's own compute path run IN MEMORY with write_fn=None.
Nothing here writes to S3 or DynamoDB, changes an environment variable of any deployed function, or
calls a vendor.
"""
import importlib.util
import json
import os
import sys

import boto3

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), *([".."] * 8)))
OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, REPO)
os.chdir(REPO)

REL_ROUTE = "lib/research/api/scoped_amgt.py"
REL_CHATTER = "lib/research/metrics/chatter_axis.py"
REL_MOVE = "lib/research/metrics/movement_gate.py"
REL_POOL = "lib/research/coverage/pool_reader.py"
REL_LAMBDA = "infra/aws/terraform/harvest/lambda_src/lambda_function.py"
REL_TF = "infra/aws/terraform/harvest/chatter-axis-schedule.tf"

lam = boto3.client("lambda", region_name="us-east-1")


def line_of(relpath, needle, start=1):
    """First line number >= start whose text contains needle, or None."""
    with open(os.path.join(REPO, relpath), "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            if i >= start and needle in line:
                return i
    return None


def loc(relpath, needle, start=1):
    return "%s:%s" % (relpath, line_of(relpath, needle, start))


def producer_config():
    cfg = lam.get_function_configuration(FunctionName="amgt-resapp-chatter-axis")
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    return cfg, env


def load_lambda_module():
    """The producer Lambda's OWN entry module, imported from its source file (select_source lives there)."""
    spec = importlib.util.spec_from_file_location("n3_chatter_axis_lambda", os.path.join(REPO, REL_LAMBDA))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def invoke_rankings(movement, as_of=None):
    """Read-only GET of the served route, as the page reads it. Returns (http_status, body)."""
    path = "/api/scoped/amgt/lead-panel/rankings/%s/chatter" % movement
    event = {"rawPath": path, "headers": {"x-firm-id": "n3-readonly-probe"},
             "requestContext": {"http": {"method": "GET", "path": path}}}
    if as_of:
        event["queryStringParameters"] = {"as_of": as_of}
    resp = lam.invoke(FunctionName="opal-amgt-scoped-api", Payload=json.dumps(event).encode())
    out = json.loads(resp["Payload"].read())
    return out.get("statusCode"), json.loads(out["body"])


def print_served(label, status, body):
    print("%s: http=%s axis=%s ranking_status=%s state=%s as_of_date=%s requested_as_of=%s dated=%s "
          "generation_id=%s row_count=%s coverage_vintage=%s"
          % (label, status, body.get("axis"), body.get("ranking_status"), body.get("state"),
             body.get("as_of_date"), body.get("requested_as_of"), body.get("dated"),
             body.get("generation_id"), body.get("row_count"), body.get("coverage_vintage")))
    for row in body.get("rows", []):
        print("   rank %-3s %-10s key=%-16s score=%s raw_chatter_count(as-of day)=%s window_total_count=%s "
              "movement_raw_score=%s" % (row.get("rank"), row.get("ticker"), row.get("security_key"),
                                         row.get("score"), row.get("raw_chatter_count"),
                                         row.get("window_total_count"), row.get("movement_raw_score")))
    if not body.get("rows"):
        print("   (no rows served; ranking_reason: %s)" % body.get("ranking_reason"))


def served_as_of(default_movement_body):
    return default_movement_body.get("as_of_date")
