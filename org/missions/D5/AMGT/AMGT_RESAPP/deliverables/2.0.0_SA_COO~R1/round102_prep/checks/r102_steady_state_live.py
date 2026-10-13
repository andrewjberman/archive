"""AMGT_RESAPP round-102 PREP -- bh-2's STEADY STATE, DRIVEN on the live function (`AMGT-bi-3`): a warm request AFTER the 60 s hold is served from the stored snapshot, fast, and says so.

  PYTHONPATH=<repo root> python r102_steady_state_live.py [--hold-seconds 65] [--limit-seconds 3.0]

READ-ONLY: GET-shaped direct invokes of `opal-amgt-scoped-api` with `LogType=Tail` (so each REPORT line comes back), one function-configuration read, one S3 GET of the stored freshness
snapshot (through the checkout's own `snapshot.read_freshness_snapshot`, the rule `AMGT-bh-1` built). Sequence, each request more than the 60 s hold (`FRESHNESS_TTL`) after the last:
  q0  overlay ASML_NA_Equity          (warms a container; may be cold; not graded)
  q1  /freshness                       the served view must carry `snapshot` (served from the stored object) and NOT `snapshot_fallback` (computed live)
  q2  overlay ASML_NA_Equity
  q3  overlay ADBE_US_Equity
Arms: S1 the reader's rule counts the stored snapshot current NOW; S2 q1 is 200 and served from the snapshot (its `snapshot.generated_at` equals the stored object's); S3 q1, q2, q3 each
200; S4 q1, q2, q3 each a WARM container (no Init Duration on its REPORT line); S5 q1, q2, q3 each under `--limit-seconds` of handler time (default 3.0, the CTO's 'about 1.3 s' with
margin; every number is printed, a request over the limit is a NO and is read, not argued). The handler times are the REPORT lines' Duration, the number the 29 s limit applies to.
Verdict `R102 STEADY STATE LIVE: YES`, `NOT WARM` (S1 to S3 and S5 hold but a container was cold: the request is not the steady state, retry), else `NO`. Exit 0 on YES. Writes nothing.
On a weekday the OLD 24-hour rule also served the snapshot: this run shows the served path's latency and bytes on Lambda, NOT the calendar rule's weekend arm (that is Saturday's).
"""
import base64
import json
import re
import sys
import time

import boto3

FN = "opal-amgt-scoped-api"


def event(path):
    return {"rawPath": path, "queryStringParameters": None, "requestContext": {"http": {"method": "GET"}}, "headers": {"x-firm-id": "opal"}}


def main(argv):
    def opt(name, default):
        return argv[argv.index(name) + 1] if name in argv else default

    hold = float(opt("--hold-seconds", "65"))
    limit = float(opt("--limit-seconds", "3.0"))
    lam = boto3.client("lambda", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FN)
    print("function %s | CodeSha256 %s | LastModified %s | %s/%s" % (FN, cfg.get("CodeSha256"), cfg.get("LastModified"), cfg.get("State"), cfg.get("LastUpdateStatus")))
    from lib.research.freshness import snapshot

    s3 = boto3.client("s3", region_name="us-east-1")
    doc, rec = snapshot.read_freshness_snapshot(s3)
    current = doc is not None
    print("snapshot: generated_at %s age %s h required_since %s current %s | %s" % (rec.get("generated_at"), rec.get("age_hours"), rec.get("required_since"), current, rec.get("reason")))

    def invoke(label, path):
        t0 = time.monotonic()
        resp = lam.invoke(FunctionName=FN, Payload=json.dumps(event(path)).encode(), LogType="Tail")
        wall = time.monotonic() - t0
        out = json.loads(resp["Payload"].read())
        tail = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
        dur = re.search(r"Duration: ([0-9.]+) ms", tail)
        init = re.search(r"Init Duration: ([0-9.]+) ms", tail)
        body = {}
        try:
            body = json.loads(out.get("body") or "{}")
        except Exception:  # noqa: BLE001
            pass
        handler_s = float(dur.group(1)) / 1000.0 if dur else None
        print("%-4s %-46s status %s handler %s s (wall %.2f s) %s" % (label, path.replace("/api/scoped/amgt", ""), out.get("statusCode"),
              ("%.2f" % handler_s) if handler_s is not None else "?", wall, ("COLD init %s ms" % init.group(1)) if init else "warm"))
        return {"status": out.get("statusCode"), "handler_s": handler_s, "cold": init is not None, "body": body}

    invoke("q0", "/api/scoped/amgt/security/ASML_NA_Equity/overlay")  # warms a container; printed, not graded
    time.sleep(hold)
    q1 = invoke("q1", "/api/scoped/amgt/freshness")
    time.sleep(hold)
    q2 = invoke("q2", "/api/scoped/amgt/security/ASML_NA_Equity/overlay")
    time.sleep(hold)
    q3 = invoke("q3", "/api/scoped/amgt/security/ADBE_US_Equity/overlay")
    served = isinstance(q1["body"].get("snapshot"), dict) and "snapshot_fallback" not in q1["body"]
    stamp = (q1["body"].get("snapshot") or {}).get("generated_at")
    print("q1 served from the snapshot: %s | snapshot.generated_at %s | stored generated_at %s | snapshot_fallback %s" % (served, stamp, rec.get("generated_at"),
          "snapshot_fallback" in q1["body"]))
    qs = [q1, q2, q3]
    arms = [
        ("S1 the rule counts the stored snapshot current NOW", current),
        ("S2 q1 served from the snapshot, generated_at equal to the stored object's", served and stamp == rec.get("generated_at")),
        ("S3 q1, q2, q3 each 200", all(q["status"] == 200 for q in qs)),
        ("S4 q1, q2, q3 each a warm container", all(not q["cold"] for q in qs)),
        ("S5 q1, q2, q3 each under %.1f s of handler time" % limit, all(q["handler_s"] is not None and q["handler_s"] < limit for q in qs)),
    ]
    for name, ok in arms:
        print("   %s %s" % ("PASS" if ok else "FAIL", name))
    times = sorted(q["handler_s"] for q in qs if q["handler_s"] is not None)
    if times:
        print("handler times s: %s | median %.2f s" % (", ".join("%.2f" % t for t in times), times[len(times) // 2]))
    held = {n.split()[0]: ok for n, ok in arms}
    if all(ok for _, ok in arms):
        verdict = "YES"
    elif held["S1"] and held["S2"] and held["S3"] and held["S5"] and not held["S4"]:
        verdict = "NOT WARM"
    else:
        verdict = "NO"
    print("R102 STEADY STATE LIVE: %s" % verdict)
    return 0 if verdict == "YES" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
