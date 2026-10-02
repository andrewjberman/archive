"""AMGT_RESAPP round 62 track B -- the silver read's deadline (CTO round-61 addendum ruling 5a @e041af6102).

  --what pre --out <json>        record CodeSha256 and the two control days' bodies (sha256 of the SECOND, warm call of each)
  --what post --pre <json>       C0 CodeSha256 moved off the pre value
                                 C1 3 of 3 CONCURRENT cold invokes of BA_US_Equity /timeline/day/2026-09-08 answer 200 (each REPORT
                                    carries Init Duration); each run prints its Duration and whether headline_reason was served
                                 C2 each control day's body (its second, warm call) is byte-equal to its pre value
Verdict: TRACK B SERVES THE DAY ROUTE INSIDE THE CEILING: YES|NO. The planted-slow-read criterion is the unit test
lib/research/api/tests/test_timeline_silver_deadline.py (a deployed read cannot be planted). Read-only.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor

import boto3

sys.path.insert(0, "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/2.0.0_SA_COO~Z/round62/checks")
import timeline_day as td  # noqa: E402

BA = "/api/scoped/amgt/security/BA_US_Equity/timeline/day/2026-09-08"
CONTROLS = ("/api/scoped/amgt/security/BA_US_Equity/timeline/day/2026-09-30",
            "/api/scoped/amgt/security/BA_US_Equity/timeline/day/2026-10-01")


def _warm_sha(lam, path):
    td._invoke(lam, path)
    second = td._invoke(lam, path)
    return second


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--what", choices=("pre", "post"), required=True)
    ap.add_argument("--out")
    ap.add_argument("--pre")
    a = ap.parse_args()
    lam = boto3.client("lambda", region_name=td.REGION)
    cfg = lam.get_function_configuration(FunctionName=td.FUNCTION)
    if a.what == "pre":
        controls = {p: _warm_sha(lam, p) for p in CONTROLS}
        json.dump({"CodeSha256": cfg["CodeSha256"], "MemorySize": cfg["MemorySize"], "controls": controls},
                  open(a.out, "w", encoding="utf-8"), indent=1)
        print(f"pre CodeSha256 {cfg['CodeSha256']} MemorySize {cfg['MemorySize']}")
        for p, c in controls.items():
            print(f"pre control {p}: status {c['status']} sha {c['body_sha256'][:16]} dur {c['duration_ms']}")
        return 0
    pre = json.load(open(a.pre, encoding="utf-8"))
    ok = []

    def clause(name, cond, detail=""):
        ok.append(bool(cond))
        print(f"{'PASS' if cond else 'FAIL'} {name} {detail}")

    clause("C0 the deployed code moved", cfg["CodeSha256"] != pre["CodeSha256"], f"{pre['CodeSha256']} -> {cfg['CodeSha256']}")

    def one(_):
        r = lam.invoke(FunctionName=td.FUNCTION, Payload=json.dumps(td._event(BA)).encode("utf-8"), LogType="Tail")
        raw = json.loads(r["Payload"].read())
        import base64
        import re
        log = base64.b64decode(r.get("LogResult") or b"").decode("utf-8", "replace")
        rep = next((ln for ln in log.splitlines() if ln.startswith("REPORT")), "")
        dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
        init = re.search(r"Init Duration: ([\d.]+) ms", rep)
        body = json.loads(raw.get("body") or "{}") if isinstance(raw, dict) else {}
        return {"status": raw.get("statusCode") if isinstance(raw, dict) else None, "error": r.get("FunctionError"),
                "duration_ms": float(dur.group(1)) if dur else None, "init_ms": float(init.group(1)) if init else None,
                "headline_reason": bool(body.get("headline_reason")), "articles": len(body.get("articles") or [])}

    with ThreadPoolExecutor(max_workers=3) as pool:
        runs = list(pool.map(one, range(3)))
    for i, r in enumerate(runs):
        print(f"   BA run {i + 1}: status {r['status']} err {r['error']} duration_ms {r['duration_ms']} init_ms {r['init_ms']} "
              f"articles {r['articles']} headline_reason {r['headline_reason']}")
    clause("C1 3 of 3 cold BA day invokes answer 200", all(r["status"] == 200 and not r["error"] and r["init_ms"] is not None for r in runs),
           f"{sum(1 for r in runs if r['status'] == 200)} of 3 status 200; cold {sum(1 for r in runs if r['init_ms'] is not None)} of 3")
    eq = []
    for p in CONTROLS:
        c = _warm_sha(lam, p)
        same = c["status"] == 200 and c["body_sha256"] == pre["controls"][p]["body_sha256"]
        eq.append(same)
        print(f"   control {p}: status {c['status']} sha {c['body_sha256'][:16]} vs pre {pre['controls'][p]['body_sha256'][:16]} equal {same}")
    clause("C2 both control days' bodies are byte-equal to their pre values", all(eq), f"{sum(eq)} of {len(CONTROLS)}")
    print(f"TRACK B SERVES THE DAY ROUTE INSIDE THE CEILING: {'YES' if all(ok) else 'NO'}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
