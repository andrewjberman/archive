"""IRPT_BCKEND round 126 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one read-only DIRECT-ACT order:
  IB126-1  IB-pr-428  for the five routes whose producer fixtures the portal's readers refuse (CTO msg 4801): does the
                      handler's own answer have the fixture's shape, read from code and the handlers' own tests, no live call.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IB126-1-AC1  exactly the five routes are answered, each with the file:line that builds its answer, a verdict and the
               kind of evidence; a verdict other than NOT_ESTABLISHED rests on a run, not on reading alone. Base: FAIL.
  IB126-1-AC2  every route with a DIFFERS verdict names the differing members; every route records whether the handler's
               answer validated against the v1 response schema. Base: FAIL.
  IB126-1-AC3  the control route (comparison-catalogue, one the portal does read) went through the same method and reads
               SAME_AS_FIXTURE. Base: FAIL.
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~287/"
OUT = D + "IB126-1_handler_shape_vs_fixture.json"
ROUTES = ("directory-browse", "analysis-request-history", "analysis-input-upload", "custody-report-read", "custody-report-persist")
VERDICTS = ("SAME_AS_FIXTURE", "DIFFERS", "NOT_ESTABLISHED")
EVIDENCE = ("existing_test_run", "in_process_call", "code_read_only")
SCHEMA = ("VALID", "INVALID", "NOT_RUN")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB126"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    rows = {r.get("operation"): r for r in a.get("routes") or []}

    if cid == "IB126-1-AC1":
        if sorted(rows) != sorted(ROUTES) or len(a.get("routes") or []) != len(ROUTES):
            fail("routes answered %r" % sorted(rows))
        for op, r in rows.items():
            if r.get("verdict") not in VERDICTS or r.get("evidence") not in EVIDENCE:
                fail("%s verdict %r evidence %r" % (op, r.get("verdict"), r.get("evidence")))
            if not r.get("answer_built_at") or ":" not in str(r.get("answer_built_at")) or not r.get("function"):
                fail("%s names no file:line or function" % op)
            if r["verdict"] != "NOT_ESTABLISHED" and r["evidence"] == "code_read_only":
                fail("%s reads %s on code reading alone" % (op, r["verdict"]))
            if r["verdict"] == "NOT_ESTABLISHED" and not r.get("why_not"):
                fail("%s is NOT_ESTABLISHED with no reason" % op)
            if r["evidence"] != "code_read_only" and not r.get("invocation"):
                fail("%s names no invocation for its run" % op)
        print("OK: 5 of 5 routes answered: %s" % {op: rows[op]["verdict"] for op in ROUTES})
    elif cid == "IB126-1-AC2":
        for op in ROUTES:
            r = rows.get(op) or {}
            if r.get("handler_answer_vs_response_schema") not in SCHEMA:
                fail("%s handler_answer_vs_response_schema %r" % (op, r.get("handler_answer_vs_response_schema")))
            if r.get("verdict") == "DIFFERS" and not r.get("differing_members"):
                fail("%s DIFFERS with no differing_members" % op)
            if r.get("verdict") == "SAME_AS_FIXTURE" and r.get("differing_members"):
                fail("%s SAME_AS_FIXTURE yet lists differing members" % op)
            if not isinstance(r.get("envelope_keys"), list):
                fail("%s lists no envelope_keys" % op)
        print("OK: every route records the schema result and its envelope keys; every DIFFERS names its members")
    elif cid == "IB126-1-AC3":
        # AMENDMENT 1 (row D2-W287-S1): the control's whole answer DIFFERS, on one envelope member its closed response schema
        # omits (`unprojected_grant`, which response_envelope always adds by CTO ruling @61627f39f9). That is a finding about
        # the schema, not a method failure. The control passes when its DATA member has the fixture's shape and every envelope
        # difference is that one named member; any other difference still fails.
        c = a.get("control") or {}
        if c.get("operation") != "comparison-catalogue" or c.get("evidence") not in ("existing_test_run", "in_process_call") \
                or not c.get("invocation"):
            fail("control %r" % c)
        if c.get("data_verdict") != "SAME_AS_FIXTURE":
            fail("control data_verdict %r" % c.get("data_verdict"))
        gap = c.get("envelope_schema_gap")
        if not isinstance(gap, list) or [g for g in gap if g != "unprojected_grant"]:
            fail("control envelope_schema_gap %r names a member other than unprojected_grant" % gap)
        for op in ROUTES:
            r = rows.get(op) or {}
            if r.get("data_verdict") not in VERDICTS or not isinstance(r.get("envelope_schema_gap"), list):
                fail("%s lacks data_verdict or envelope_schema_gap" % op)
        print("OK: the control's data member has the fixture's shape; its envelope gap is %s; every route carries both fields" % gap)
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
