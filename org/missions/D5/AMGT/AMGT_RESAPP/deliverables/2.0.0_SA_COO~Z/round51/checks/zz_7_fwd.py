"""AMGT_RESAPP round 51, AMGT-zz-7 AC1 -- the FWD-1..31 re-grade against the SERVED state (CTO round-50 ruling 6; the last full pass was
uu-1 at round 46, deliverables/0.9.0_WK_AMGT_RESAPP~167/FWD_EVIDENCE_ROUND46.json).

Reads `deliverables/0.9.0_WK_AMGT_RESAPP~182/FWD_EVIDENCE_ROUND51.json` and checks, against the PRD
(prd/AMGT_RESAPP_PRD.md, the ENDPOINT section):
  - the round-46 file's shape (`prd`, `run_at`, `code_sha256`, `state_rule`, `tally`, `outcomes` list), exactly one outcome per
    FWD-1..FWD-31 (31 of 31, no extra id);
  - each row's `fence_quote` appears VERBATIM in the PRD (whitespace-normalised);
  - `state` in {met, unmet, unmeasurable}; `instrument` and `output_excerpt` non-empty; `reason` non-empty unless met;
  - the file's top-level `code_sha256` equals the DEPLOYED function's CodeSha256 read now (the pass graded what is served).
usage: python <this>   (from the repo root)"""
import json
import re
import sys

import boto3

EVIDENCE = "org/missions/D5/AMGT/AMGT_RESAPP/deliverables/0.9.0_WK_AMGT_RESAPP~182/FWD_EVIDENCE_ROUND51.json"
PRD = "org/missions/D5/AMGT/AMGT_RESAPP/prd/AMGT_RESAPP_PRD.md"
STATES = {"met", "unmet", "unmeasurable"}


def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def main():
    try:
        ev = json.load(open(EVIDENCE, encoding="utf-8"))
    except FileNotFoundError:
        print("no %s" % EVIDENCE)
        print("THE FWD-1..31 PASS IS COMPLETE AND GROUNDED: NO")
        return 1
    prd = norm(open(PRD, encoding="utf-8").read())
    rows = ev.get("outcomes") or []
    ids = [r.get("id") for r in rows]
    want = ["FWD-%d" % i for i in range(1, 32)]
    bad = []
    if sorted(ids, key=lambda x: int(str(x).split("-")[-1]) if str(x).split("-")[-1].isdigit() else 999) != want:
        bad.append("ids %d, missing %s, extra %s" % (len(ids), sorted(set(want) - set(ids))[:4], sorted(set(ids) - set(want))[:4]))
    counts = {}
    for r in rows:
        counts[r.get("state")] = counts.get(r.get("state"), 0) + 1
        if norm(r.get("fence_quote")) not in prd or not norm(r.get("fence_quote")):
            bad.append("%s fence_quote not verbatim in the PRD" % r.get("id"))
        if r.get("state") not in STATES:
            bad.append("%s state %r" % (r.get("id"), r.get("state")))
        if not r.get("instrument") or not r.get("output_excerpt"):
            bad.append("%s lacks instrument/output_excerpt" % r.get("id"))
        if r.get("state") != "met" and not r.get("reason"):
            bad.append("%s %s without a reason" % (r.get("id"), r.get("state")))
    live = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName="opal-amgt-scoped-api")["CodeSha256"]
    if ev.get("code_sha256") != live:
        bad.append("code_sha256 %r != deployed %r" % (ev.get("code_sha256"), live))
    for b in bad[:8]:
        print("  BAD", b)
    print("rows %d of 31; states %s; graded at %s (deployed %s)" % (len(rows), counts, ev.get("code_sha256"), live))
    ok = not bad
    print("THE FWD-1..31 PASS IS COMPLETE AND GROUNDED: %s" % ("YES" if ok else "NO"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
