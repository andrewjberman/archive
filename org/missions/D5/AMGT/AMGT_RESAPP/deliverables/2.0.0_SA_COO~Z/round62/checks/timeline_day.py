"""AMGT_RESAPP round 62 -- the demo-path timeline day route answers inside the gateway ceiling (CTO round-61 addendum ruling 5
@f1d5dac151; CVO~Z row DSGN_AMGTV1-Z-C-S29).

  --what pre --out <json>        record the function's MemorySize/LastModified, ONE invoke of the control day (body sha256 and
                                 status), and ONE BA day invoke (duration and status) -- read-only
  --what post --pre <json> [--target-ms 20000]
                                 C0 MemorySize moved off the pre value
                                 C1 3 of 3 CONCURRENT invokes of BA_US_Equity /timeline/day/2026-09-08, each COLD (REPORT carries
                                    "Init Duration") and each status 200 with Duration under --target-ms
                                 C2 the control day's body sha256 equals the pre value (the memory change moves no output)
Verdict: THE BA DAY ROUTE ANSWERS COLD UNDER TARGET: YES|NO. Read-only (lambda:Invoke with LogType=Tail, GetFunctionConfiguration).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import boto3

FUNCTION = "opal-amgt-scoped-api"
REGION = "us-east-1"
BA_PATH = "/api/scoped/amgt/security/BA_US_Equity/timeline/day/2026-09-08"
CONTROL_PATH = "/api/scoped/amgt/security/AMD_US_Equity/timeline"


def _event(path):
    return {"rawPath": path, "headers": {"x-firm-id": "opal"},
            "requestContext": {"http": {"method": "GET", "path": path}}, "queryStringParameters": None}


def _invoke(lam, path):
    r = lam.invoke(FunctionName=FUNCTION, Payload=json.dumps(_event(path)).encode("utf-8"), LogType="Tail")
    raw = r["Payload"].read()
    log = base64.b64decode(r.get("LogResult") or b"").decode("utf-8", "replace")
    rep = next((ln for ln in log.splitlines() if ln.startswith("REPORT")), "")
    dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
    init = re.search(r"Init Duration: ([\d.]+) ms", rep)
    mem = re.search(r"Max Memory Used: (\d+) MB", rep)
    status, body = None, b""
    if not r.get("FunctionError"):
        try:
            parsed = json.loads(raw)
            status = parsed.get("statusCode")
            body = (parsed.get("body") or "").encode("utf-8")
        except ValueError:
            pass
    return {"function_error": r.get("FunctionError"), "status": status,
            "duration_ms": float(dur.group(1)) if dur else None, "init_ms": float(init.group(1)) if init else None,
            "max_mem_mb": int(mem.group(1)) if mem else None, "body_sha256": hashlib.sha256(body).hexdigest(),
            "report": rep[:300]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("pre", "post"), required=True)
    ap.add_argument("--out")
    ap.add_argument("--pre")
    ap.add_argument("--target-ms", type=float, default=20000.0)
    a = ap.parse_args()
    lam = boto3.client("lambda", region_name=REGION)
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    if a.what == "pre":
        control = _invoke(lam, CONTROL_PATH)
        ba = _invoke(lam, BA_PATH)
        doc = {"MemorySize": cfg["MemorySize"], "LastModified": cfg["LastModified"], "CodeSha256": cfg["CodeSha256"],
               "control": control, "ba": ba}
        json.dump(doc, open(a.out, "w", encoding="utf-8"), indent=1)
        print(f"pre MemorySize {cfg['MemorySize']} CodeSha256 {cfg['CodeSha256']}")
        print(f"pre control {CONTROL_PATH}: status {control['status']} sha {control['body_sha256'][:16]} dur {control['duration_ms']}")
        print(f"pre BA {BA_PATH}: status {ba['status']} err {ba['function_error']} dur {ba['duration_ms']} init {ba['init_ms']} mem {ba['max_mem_mb']}")
        return 0
    pre = json.load(open(a.pre, encoding="utf-8"))
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    clause("C0 MemorySize moved", cfg["MemorySize"] != pre["MemorySize"], f"{pre['MemorySize']} -> {cfg['MemorySize']}")
    with ThreadPoolExecutor(max_workers=3) as pool:
        runs = list(pool.map(lambda _: _invoke(lam, BA_PATH), range(3)))
    good = [r for r in runs if r["status"] == 200 and not r["function_error"] and r["init_ms"] is not None
            and r["duration_ms"] is not None and r["duration_ms"] < a.target_ms]
    for i, r in enumerate(runs):
        print(f"   BA run {i + 1}: status {r['status']} err {r['function_error']} duration_ms {r['duration_ms']} init_ms {r['init_ms']} max_mem {r['max_mem_mb']}")
    clause(f"C1 3 of 3 cold BA day invokes 200 under {a.target_ms:.0f} ms", len(good) == 3, f"{len(good)} of 3")
    control = _invoke(lam, CONTROL_PATH)
    clause("C2 the control's body equals its pre value", control["status"] == 200 and control["body_sha256"] == pre["control"]["body_sha256"],
           f"status {control['status']} sha {control['body_sha256'][:16]} vs pre {pre['control']['body_sha256'][:16]}")
    print(f"THE BA DAY ROUTE ANSWERS COLD UNDER TARGET: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
