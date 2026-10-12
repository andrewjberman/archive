"""AMGT_RESAPP round-101 PREP -- the cold first overlay request on the LIVE function, with the snapshot's state and the container's state printed beside it.

  PYTHONPATH=<repo root> python r101_cold_live.py [--subjects ASML_NA_Equity,ADBE_US_Equity] [--quiet-minutes 15]

READ-ONLY: GET-shaped direct invokes of `opal-amgt-scoped-api` (one per subject, sequential, `LogType=Tail` so the REPORT line comes back), one S3 GET of the stored freshness snapshot,
one Logs Insights count. Per subject it prints: the overlay's status and the HANDLER time (the REPORT line's Duration, the number the 29 s limit applies to), whether the container was
cold (an Init Duration on the REPORT line), and the number of invocations of the function in the preceding `--quiet-minutes` (0 = the request met a quiet function). Before the invokes it
prints the snapshot's `generated_at`, its age and whether the reader's rule counts it as current NOW (`snapshot.read_freshness_snapshot`). Verdict line:
    R101 COLD LIVE: YES     every subject 200, handler time under 20 s, and the snapshot current
    R101 COLD LIVE: NO      a subject over 20 s or not 200, or the snapshot not current
    R101 COLD LIVE: NOT QUIET  the numbers are printed and graded as above, but an invocation was seen in the quiet window, so a 'cold after quiet' claim is not made
Exit 0 on YES, 1 otherwise. Writes nothing.
"""
import json
import re
import sys
import time

import boto3

FN = "opal-amgt-scoped-api"
LG = "/aws/lambda/" + FN


def main(argv):
    def opt(name, default):
        return argv[argv.index(name) + 1] if name in argv else default

    subjects = opt("--subjects", "ASML_NA_Equity,ADBE_US_Equity").split(",")
    quiet = int(opt("--quiet-minutes", "15"))
    from lib.research.freshness import snapshot

    s3 = boto3.client("s3", region_name="us-east-1")
    doc, rec = snapshot.read_freshness_snapshot(s3)
    current = doc is not None
    print("snapshot: generated_at %s age %s h required_since %s current %s | %s" % (rec.get("generated_at"), rec.get("age_hours"), rec.get("required_since"), current, rec.get("reason")))
    cw = boto3.client("logs", region_name="us-east-1")
    end = int(time.time())
    qid = cw.start_query(logGroupName=LG, startTime=end - quiet * 60, endTime=end, queryString='filter @type = "REPORT" | stats count(*) as n', limit=10)["queryId"]
    n_recent = None
    for _ in range(60):
        time.sleep(2)
        res = cw.get_query_results(queryId=qid)
        if res["status"] in ("Complete", "Failed", "Cancelled", "Timeout"):
            if res["status"] == "Complete":
                n_recent = int(float([c["value"] for c in res["results"][0] if c["field"] == "n"][0])) if res.get("results") else 0
            break
    print("invocations in the preceding %d minutes: %s" % (quiet, n_recent))
    lam = boto3.client("lambda", region_name="us-east-1")
    ok = current
    for sj in subjects:
        ev = {"rawPath": "/api/scoped/amgt/security/%s/overlay" % sj, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}},
              "headers": {"x-firm-id": "opal"}}
        t0 = time.monotonic()
        resp = lam.invoke(FunctionName=FN, Payload=json.dumps(ev).encode(), LogType="Tail")
        wall = time.monotonic() - t0
        body = json.loads(resp["Payload"].read())
        status = body.get("statusCode")
        import base64
        tail = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
        dur = re.search(r"Duration: ([0-9.]+) ms", tail)
        init = re.search(r"Init Duration: ([0-9.]+) ms", tail)
        handler_s = float(dur.group(1)) / 1000.0 if dur else None
        print("%-16s status %s handler %s s (wall %.2f s) cold container %s" % (sj, status, "%.2f" % handler_s if handler_s is not None else "?", wall, "YES init %s ms" % init.group(1) if init else "no"))
        ok = ok and status == 200 and handler_s is not None and handler_s < 20.0
    verdict = "YES" if ok else "NO"
    held = n_recent == 0
    print("QUIET WINDOW: %s (%s invocations in the preceding %d minutes)" % ("HELD" if held else "NOT HELD", n_recent, quiet))
    if ok and not held:
        verdict = "NOT QUIET"
    print("R101 COLD LIVE: %s" % verdict)
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
