"""IRPT_ANLREQ TO-APPLY-t55 LEG A (0.7.0_AE_CloudOps~AQ2): ONE direct invoke of outlook-global-commentary-draft-lambda with a WRONG_KIND body naming the synthetic job row.

  python t55_leg_a.py --selftest
  python t55_leg_a.py --go

Guards (STOP, nothing invoked): the commentary function CodeSha256 is I/6mirBT..., the row irpt-jobs 49financial REQ-d47252fe74634d0c5cdd8067 exists
with state READY and no hop_failure, and its item sha256 equals the PRE recorded in C:/dev/aq2-t54/t55_pre.json. Then ONE RequestResponse invoke, no
retry on any outcome. Prints: the UTC moment, the parsed answer (results, failed reasons, batchItemFailures ids), the function's log line count after
the invoke, the row after (hop_failure keys, hop, code, at, state, the sha256 of the item without hop_failure against PRE). Writes nothing else; no
put-item, no delete-item, no queue message.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
import datetime as dt

REGION = "us-east-1"
FN = "outlook-global-commentary-draft-lambda"
ROW = {"tenant": {"S": "49financial"}, "job": {"S": "REQ-d47252fe74634d0c5cdd8067"}}
LOGGROUP = "/aws/lambda/" + FN
WANT_SHA = "I/6mirBTU5+JPCUUx6Xrmd1bn1vGAjvZTL75LhOm3HY="
PAYLOAD = {"Records": [{"eventSource": "aws:sqs", "messageId": "t55-1",
                        "body": json.dumps({"kind": "t55_forced_refusal", "tenant": "49financial", "request_id": "REQ-d47252fe74634d0c5cdd8067"}, separators=(",", ":"))}]}


def digest(item, drop=()):
    return hashlib.sha256(json.dumps({k: v for k, v in item.items() if k not in drop}, sort_keys=True).encode()).hexdigest()


def selftest():
    a = {"tenant": {"S": "t"}, "state": {"S": "READY"}}
    b = dict(a, hop_failure={"M": {"code": {"S": "X"}}})
    assert digest(b, drop=("hop_failure",)) == digest(a) != digest(b)
    body = json.loads(PAYLOAD["Records"][0]["body"])
    assert body["kind"] != "analysis_ready" and body["request_id"].startswith("REQ-") and body["tenant"] == "49financial"
    assert PAYLOAD["Records"][0]["messageId"] == "t55-1"
    print("SELFTEST OK digest (with and without hop_failure), the payload body is not the canonical kind and names the one row")
    return 0


def go():
    import boto3
    lam = boto3.client("lambda", region_name=REGION)
    ddb = boto3.client("dynamodb", region_name=REGION)
    logs = boto3.client("logs", region_name=REGION)
    pre = json.load(open("C:/dev/aq2-t54/t55_pre.json"))["pre"]
    got = lam.get_function_configuration(FunctionName=FN)["CodeSha256"]
    if got != WANT_SHA:
        print("STOP: the commentary function digest is not the expected one; nothing invoked")
        return 2
    r = ddb.get_item(TableName="irpt-jobs", Key=ROW, ConsistentRead=True).get("Item")
    if r is None or r["state"]["S"] != "READY" or "hop_failure" in r or digest(r) != pre:
        print("STOP: the row is absent, not READY, already carries hop_failure, or its sha256 differs from PRE; nothing invoked")
        return 2
    print("GUARDS GREEN: digest equal, row READY, hop_failure ABSENT, item sha256 equals PRE %s" % pre)
    t0 = time.time()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    resp = lam.invoke(FunctionName=FN, InvocationType="RequestResponse", Payload=json.dumps(PAYLOAD).encode())
    raw = resp["Payload"].read().decode()
    print("INVOKE at %s UTC: StatusCode %s FunctionError %s ExecutedVersion %s" % (stamp, resp["StatusCode"], resp.get("FunctionError"), resp.get("ExecutedVersion")))
    try:
        body = json.loads(raw)
    except ValueError:
        body = None
    if isinstance(body, dict):
        results = body.get("results")
        failed = body.get("failed")
        bif = (body.get("batchItemFailures") or [])
        print("ANSWER results=%s failed=%s batchItemFailures=%s" % (len(results) if isinstance(results, list) else results,
              [(f.get("reason") if isinstance(f, dict) else f) for f in (failed or [])], [x.get("itemIdentifier") for x in bif if isinstance(x, dict)]))
    else:
        print("ANSWER unparsed, %d bytes, sha256 %s" % (len(raw), hashlib.sha256(raw.encode()).hexdigest()))
    print("NOTE direct invoke: no SQS message exists, nothing is redelivered and no dead-letter entry is made")
    time.sleep(8)
    ev = logs.filter_log_events(logGroupName=LOGGROUP, startTime=int(t0 * 1000) - 2000, filterPattern='"HOP-FAILURE-REPORTED"').get("events", [])
    want = "HOP-FAILURE-REPORTED request_id=REQ-d47252fe74634d0c5cdd8067 hop=COMMENTARY code=COMMENTARY_DRAFT_REFUSED written=True"
    print("LOG events with the HOP-FAILURE-REPORTED line since the invoke: %d; exact line present: %s" % (len(ev), any(want in (e.get("message") or "") for e in ev)))
    r2 = ddb.get_item(TableName="irpt-jobs", Key=ROW, ConsistentRead=True).get("Item")
    hf = (r2 or {}).get("hop_failure", {}).get("M", {})
    print("ROW after: hop_failure keys %s hop %s code %s at %s; state %s; item sha256 without hop_failure %s (PRE %s) equal=%s"
          % (sorted(hf), hf.get("hop", {}).get("S"), hf.get("code", {}).get("S"), hf.get("at", {}).get("S"), (r2 or {}).get("state", {}).get("S"),
             digest(r2, drop=("hop_failure",)), pre, digest(r2, drop=("hop_failure",)) == pre))
    json.dump({"pre": pre, "recorded_hop_failure": {k: v.get("S") for k, v in hf.items()}, "invoke_utc": stamp}, open("C:/dev/aq2-t54/t55_after_a.json", "w"))
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--go" in sys.argv:
        sys.exit(go())
    print(__doc__)
    sys.exit(2)
