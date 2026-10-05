"""AMGT_RESAPP round 70, cell AMGT-at-6: /security/<key>/peers latency PER SEGMENT on the
deployed function.

Why this exists: at-3 adds one stored model-block read PER PEER MEMBER (in parallel), so the
route's cost is no longer independent of member count. AMENDMENT 1 asks for the latency on 3
names and the CTO half's condition 3 asks for it per segment; a /peers over 5 s is a STOP
(the COO half), not a rollback.

Method: one Lambda invoke per name with LogType='Tail', so Duration and every AMGT_SEGMENT
line come from the function's OWN REPORT line rather than from a client-side stopwatch that
would also time the network. Each name is invoked COLD-then-WARM and both are reported,
because a single number cannot tell an operator which it was -- the lesson of row
AMGT_RESAPP-Z-S349.

Run: PYTHONPATH="$(git rev-parse --show-toplevel)" python <this file>
"""
from __future__ import annotations

import base64
import json
import re
import sys

NAMES = ("BA_US_Equity", "AMD_US_Equity", "VLO_US_Equity")
PREFIX = "/api/scoped/amgt"
BAR_MS = 5000.0


def _invoke(lam, function, key):
    ev = {
        "rawPath": "%s/security/%s/peers" % (PREFIX, key),
        "headers": {"x-firm-id": "opal"},
        "requestContext": {"http": {"method": "GET"}},
        "queryStringParameters": None,
    }
    r = lam.invoke(FunctionName=function, Payload=json.dumps(ev).encode("utf-8"), LogType="Tail")
    raw = json.loads(r["Payload"].read())
    log = base64.b64decode(r.get("LogResult") or b"").decode("utf-8", "replace")
    rep = next((ln for ln in log.splitlines() if ln.startswith("REPORT")), "")
    dur = re.search(r"\tDuration: ([\d.]+) ms", rep)
    init = re.search(r"Init Duration: ([\d.]+) ms", rep)
    body = json.loads(raw.get("body") or "{}") if isinstance(raw, dict) else {}
    members = body.get("members") or body.get("peers") or []
    segs = []
    for ln in log.splitlines():
        if "AMGT_SEGMENT" in ln:
            m = re.search(r"AMGT_SEGMENT\s+(\S+?)=(\d+)", ln)
            if m:
                segs.append((m.group(1), int(m.group(2))))
    return {
        "status": raw.get("statusCode") if isinstance(raw, dict) else None,
        "duration_ms": float(dur.group(1)) if dur else None,
        "cold": init is not None,
        "init_ms": float(init.group(1)) if init else None,
        "members": len(members) if isinstance(members, list) else None,
        "segments": segs,
    }


def main() -> int:
    import boto3

    function = "opal-amgt-scoped-api"
    lam = boto3.client("lambda", region_name="us-east-1")

    worst = 0.0
    rows = []
    for key in NAMES:
        for label in ("read 1", "read 2"):
            r = _invoke(lam, function, key)
            rows.append((key, label, r))
            if r["duration_ms"]:
                worst = max(worst, r["duration_ms"])
            segs = " ".join("%s=%d" % s for s in r["segments"]) or "<none>"
            print(
                "  %-14s %-6s status %s  %-9.2f ms  cold=%-5s init=%-8s members=%-4s | %s"
                % (
                    key,
                    label,
                    r["status"],
                    r["duration_ms"] or -1.0,
                    r["cold"],
                    ("%.2f" % r["init_ms"]) if r["init_ms"] else "-",
                    r["members"],
                    segs,
                )
            )

    bad_status = [(k, lab) for k, lab, r in rows if r["status"] != 200]
    with_segs = sum(1 for _, _, r in rows if r["segments"])
    print()
    print("  DENOMINATOR: %d invokes over %d names; non-200 %d" % (len(rows), len(NAMES), len(bad_status)))
    print("  WORST duration: %.2f ms against the %.0f ms STOP bar" % (worst, BAR_MS))
    print(
        "  PER-SEGMENT COVERAGE: %d of %d invokes emitted any AMGT_SEGMENT line. A zero here is NOT"
        % (with_segs, len(rows))
    )
    print(
        "    'no time was spent' -- it means the /peers route carries no segment instrumentation,"
    )
    print(
        "    so the per-segment breakdown the order asks for cannot be read off the function's own"
    )
    print("    logs and the TOTAL duration above is the whole of what this instrument can say.")
    ok = not bad_status and worst < BAR_MS
    print("R70 AT6 PEERS LATENCY: %s" % ("YES" if ok else "NO -- STOP, report with segment times"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
