"""AMGT_RESAPP round-102 PREP -- the FIRST request after the apply, driven ALONE and recorded with its request id (`AMGT-bi-2`'s act 2).

  python r102_first_cold_request.py <out file> [--subject ASML_NA_Equity]

ONE GET-shaped direct invoke of `opal-amgt-scoped-api` for `/api/scoped/amgt/security/<subject>/overlay` with `LogType=Tail`, made BEFORE any capture, replay or other reader: the first
request on a function version whose package was just replaced runs in a new execution environment, so it is COLD by construction (the REPORT line carries an Init Duration). Writes
`<out file>` (ASCII): a line `REQUEST_ID <id>` (the id `r102_phase_table.py --id-file` reads), the invoke time in UTC, the status, the REPORT line, and every `AMGT_PHASE` line the log tail
returned. Prints the same and a verdict line:
    R102 FIRST COLD REQUEST: RECORDED   status 200, a request id, and a REPORT line with an Init Duration (a cold container)
    R102 FIRST COLD REQUEST: NOT COLD   status 200 and a request id but no Init Duration: the file is written, the request is NOT the cold one, and the caller says so
    R102 FIRST COLD REQUEST: NO         anything else
Exit 0 on RECORDED. Reads only the function; writes only `<out file>`.
"""
import base64
import datetime
import json
import re
import sys

import boto3

FN = "opal-amgt-scoped-api"


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    out_path = argv[0]
    subject = argv[argv.index("--subject") + 1] if "--subject" in argv else "ASML_NA_Equity"
    lam = boto3.client("lambda", region_name="us-east-1")
    ev = {"rawPath": "/api/scoped/amgt/security/%s/overlay" % subject, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}},
          "headers": {"x-firm-id": "opal"}}
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    resp = lam.invoke(FunctionName=FN, Payload=json.dumps(ev).encode(), LogType="Tail")
    request_id = resp.get("ResponseMetadata", {}).get("RequestId") or resp.get("ResponseMetadata", {}).get("HTTPHeaders", {}).get("x-amzn-requestid")
    body = json.loads(resp["Payload"].read())
    status = body.get("statusCode")
    tail = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
    report = next((x for x in tail.splitlines() if x.startswith("REPORT ")), "")
    phases = [x for x in tail.splitlines() if x.startswith("AMGT_PHASE ")]
    cold = re.search(r"Init Duration: ([0-9.]+) ms", report) is not None
    lines = ["REQUEST_ID %s" % request_id, "INVOKED_AT %s" % at, "SUBJECT %s" % subject, "STATUS %s" % status,
             "FUNCTION_VERSION_LOG_TAIL_LINES %d" % len(tail.splitlines()), report or "REPORT ABSENT"] + phases
    text = "\n".join(row.encode("ascii", "replace").decode("ascii") for row in lines) + "\n"
    with open(out_path, "w", encoding="ascii", newline="\n") as fh:
        fh.write(text)
    sys.stdout.write(text)
    if status == 200 and request_id and cold:
        verdict = "RECORDED"
    elif status == 200 and request_id:
        verdict = "NOT COLD"
    else:
        verdict = "NO"
    print("R102 FIRST COLD REQUEST: %s" % verdict)
    return 0 if verdict == "RECORDED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
