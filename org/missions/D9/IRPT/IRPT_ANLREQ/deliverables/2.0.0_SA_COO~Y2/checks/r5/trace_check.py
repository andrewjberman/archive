"""trace_check.py -- the one mechanical check of IRPT_ANLREQ round 5, workstream Y (cell AR-y-51, the read-only FWD-1 trace).

Usage:  python trace_check.py --root <workspace root>

Prints Y51-TRACE-OK when the trace file exists and every hop row is complete; otherwise one FAIL line per problem and
Y51-TRACE-FAIL. It grades the FORM of the table (every hop has a state, an owner, what it waits on, evidence and a claim word);
whether a hop's state is TRUE is the issuer's and the CTO's reading. It writes nothing.
"""
import json
import sys
from pathlib import Path

TRACE = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~52/trace/FWD1_HOP_TRACE.json"
STATES = ("LIVE", "BUILT_NOT_LIVE", "NO_CODE", "NOT_DETERMINED")
OWNERS = ("IRPT_ANLREQ_Y", "IRPT_ANLREQ_G", "TCKT_VNEXT", "PORTAL", "IRPT_BCKEND", "IRPT_YCDGEN", "OTHER")
CLAIMS = ("measured", "inferred", "inherited")


def main(argv):
    if "--root" not in argv:
        print(__doc__)
        return 2
    root = Path(argv[argv.index("--root") + 1])
    path = root / TRACE
    problems = []
    if not path.is_file():
        print("FAIL: no %s" % TRACE)
        print("Y51-TRACE-FAIL")
        return 1
    doc = json.loads(path.read_text(encoding="utf-8"))
    hops = doc.get("hops") or []
    if len(hops) < 4:
        problems.append("fewer than 4 hops: a journey from a filed ticket to an opened report has more")
    if not (isinstance(doc.get("fwd1_text_source"), str) and doc["fwd1_text_source"]):
        problems.append("fwd1_text_source (the file and line FWD-1 was read from) is missing")
    for i, hop in enumerate(hops, 1):
        tag = "hop %d (%s)" % (i, str(hop.get("hop"))[:40])
        if not (isinstance(hop.get("hop"), str) and len(hop["hop"]) >= 10):
            problems.append("%s: no hop description" % tag)
        if hop.get("state") not in STATES:
            problems.append("%s: state %r is not one of %s" % (tag, hop.get("state"), ", ".join(STATES)))
        if hop.get("owner") not in OWNERS:
            problems.append("%s: owner %r is not one of %s" % (tag, hop.get("owner"), ", ".join(OWNERS)))
        if not (isinstance(hop.get("waits_on"), str) and hop["waits_on"]):
            problems.append("%s: waits_on is empty (write NOTHING if it waits on nothing)" % tag)
        evidence = hop.get("evidence")
        if not (isinstance(evidence, list) and evidence and all(isinstance(e, str) and e for e in evidence)):
            problems.append("%s: no evidence entries" % tag)
        if hop.get("claim") not in CLAIMS:
            problems.append("%s: claim %r is not one of %s" % (tag, hop.get("claim"), ", ".join(CLAIMS)))
        if hop.get("state") == "LIVE" and hop.get("claim") == "inferred":
            problems.append("%s: LIVE cannot rest on an inferred claim; read the live resource or say inherited and from whom" % tag)
    counts = {state: sum(1 for hop in hops if hop.get("state") == state) for state in STATES}
    print("hops %d: %s" % (len(hops), ", ".join("%s %d" % item for item in counts.items())))
    for problem in problems:
        print("FAIL: %s" % problem)
    print("Y51-TRACE-%s" % ("FAIL" if problems else "OK"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
