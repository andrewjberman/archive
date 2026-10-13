"""ADVI_FIRMBKTS round 6 shape grader for FB-i-2 (the runner-side emit read), issuer 2.0.0_SA_COO~B1.

  runner --file F   RUNNER_EMIT_READ.json: every call a read verb except at most ONE `aws events put-events` of a NON-MATCHING
                    probe (the CTO's word covers exactly one event, ROUND_ANALYSIS.round5.md section 2), sent only when the read
                    alone left the verdict indeterminate. Proves SHAPE and discipline, never that the findings are true.
Prints one result line; exit 0 on a pass. Plain ASCII.
"""
import argparse
import json
import re
import sys

CLAIMS = ("measured", "inferred", "held", "absent")
READ = re.compile(r"^(aws|\.tools/aws)\s+[a-z0-9-]+\s+(get|describe|list|lookup|head|filter)[a-z0-9-]*\b")
PROBE = re.compile(r"^(aws|\.tools/aws)\s+(events\s+put-events|ssm\s+send-command)\b")
VERDICTS = ("REGION_UNSET", "CREDENTIALS", "CLI_OR_OUTPUT_FORMAT", "EXCEPTION_NAMED", "STILL_INDETERMINATE")


def _get(d, path):
    cur = d
    for k in path.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return None, "missing %s" % path
        cur = cur[k]
    return cur, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("runner",))
    ap.add_argument("--file", required=True)
    a = ap.parse_args()
    try:
        d = json.load(open(a.file, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print("FAIL ABSENT or unreadable: %s: %s" % (type(e).__name__, str(e)[:100]))
        return 1
    p = []
    calls = d.get("calls")
    if not isinstance(calls, list) or not calls:
        p.append("calls: a non-empty list")
        calls = []
    probes = [c for c in calls if isinstance(c, str) and PROBE.match(c.strip())]
    bad = [c for c in calls if not (isinstance(c, str) and (READ.match(c.strip()) or PROBE.match(c.strip())))]
    for c in bad[:3]:
        p.append("call is neither a read verb nor the one probe: %s" % str(c)[:90])
    for path in ("warn_context.chains_read", "warn_context.warn_lines", "emit_path.client", "emit_path.region_source",
                 "emit_path.credential_source", "positive_control.note", "verdict", "verdict_reason",
                 "test_event.sent", "test_event.count"):
        v, e = _get(d, path)
        if e:
            p.append(e)
    for path in ("warn_context", "emit_path", "positive_control"):
        v, e = _get(d, path + ".claim")
        if e or v not in CLAIMS:
            p.append("claim at %s.claim not one of %s" % (path, "/".join(CLAIMS)))
    if not p:
        if d["verdict"] not in VERDICTS:
            p.append("verdict not in the closed set")
        te = d["test_event"]
        if te["count"] not in (0, 1) or len(probes) != te["count"] or bool(te["sent"]) != (te["count"] == 1):
            p.append("test_event.count must equal the probe calls listed (0 or 1) and agree with sent")
        if te["sent"]:
            if d.get("indeterminate_before_test") is not True:
                p.append("a test event was sent without indeterminate_before_test true")
            if te.get("matches_any_rule") is not False or not str(te.get("detail_type", "")).strip():
                p.append("the test event must name a detail_type and matches_any_rule false")
    if p:
        for x in p:
            print("FAIL %s" % x)
        print("RUNNER: %d problem(s)" % len(p))
        return 1
    print("RUNNER record ok calls=%d verdict=%s test_event_sent=%s" % (len(calls), d["verdict"], d["test_event"]["sent"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
