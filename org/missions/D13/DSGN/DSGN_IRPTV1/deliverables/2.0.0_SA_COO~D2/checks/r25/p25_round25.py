"""DSGN_IRPTV1 round 25 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2's ruling msg 5494.

Cell: IV-e-111 ONE candidate cut off portal PROD holding only what IRPT_ANLREQ release 5's return needs: the history reader, the two
missing irpt-status reads, retained_ref. Every changed file under src/pages/InvestorReporting or the one endpoints file; none in the
print route's import closure, shown from the build's chunk graph.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  IV111-AC1  ~61/PROD_CUT.json: base_commit starting 37aa1247ee; candidate_commit (40 hex); pushed false; files (the changed paths,
             1 or more), every one under src/pages/InvestorReporting/ or equal to src/api/endpoints/investor-reporting.ts;
             carries {history_reader, status_read_pdf, status_read_original, retained_ref}, each {carried true, where, test};
             left_out (a list, each {what, why}).
  IV111-AC2  the same record: print_closure {method, entry, closure_files (int > 0), control (a file known to be in the closure,
             found there: true)}; changed_in_closure is a list; when it is empty verdict is CLEAR; when it is not, verdict is
             WAITS_ON_ANDREW with a row id; lint_errors 0; typecheck_errors 0; suite {fail 0, pass > 0}; build_ok true.
"""
import json
import re
import sys
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")
ENDPOINT = "src/api/endpoints/investor-reporting.ts"


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IV25"))
        sys.exit(1)

    p = root / "org/missions/D13/DSGN/DSGN_IRPTV1/deliverables/0.9.0_WK_DSGN_IRPTV1~61/PROD_CUT.json"
    if not p.is_file():
        fail("no record")
    r = json.loads(p.read_bytes().decode("utf-8"))
    files = r.get("files") or []
    if cid == "IV111-AC1":
        if not str(r.get("base_commit") or "").startswith("37aa1247ee") or not HEX40.match(str(r.get("candidate_commit") or "")) or r.get("pushed") is not False:
            fail("base_commit, candidate_commit or pushed is not as required")
        if not files:
            fail("no files")
        outside = [f for f in files if not (str(f).startswith("src/pages/InvestorReporting/") or f == ENDPOINT)]
        if outside:
            fail("%d of %d changed file(s) are outside the allowed paths: %s" % (len(outside), len(files), outside[:3]))
        c = r.get("carries") or {}
        for k in ("history_reader", "status_read_pdf", "status_read_original", "retained_ref"):
            v = c.get(k) or {}
            if v.get("carried") is not True or not str(v.get("where") or "").strip() or not str(v.get("test") or "").strip():
                fail("carries.%s lacks carried true, where or test" % k)
        lo = r.get("left_out")
        if not isinstance(lo, list) or any(not str(x.get("what") or "").strip() or not str(x.get("why") or "").strip() for x in lo):
            fail("left_out is not a list of {what, why}")
        print("OK: candidate %s over PROD: %d file(s), 0 outside the allowed paths; the history reader, both status reads and retained_ref carried; %d thing(s) left out"
              % (r["candidate_commit"][:10], len(files), len(lo)))
    elif cid == "IV111-AC2":
        pc = r.get("print_closure") or {}
        ctl = pc.get("control") or {}
        if not str(pc.get("method") or "").strip() or not str(pc.get("entry") or "").strip() or not isinstance(pc.get("closure_files"), int) \
                or pc["closure_files"] < 1 or not str(ctl.get("file") or "").strip() or ctl.get("found") is not True:
            fail("print_closure lacks its method, entry, a positive closure_files or a found control")
        cic = r.get("changed_in_closure")
        if not isinstance(cic, list) or any(f not in files for f in cic):
            fail("changed_in_closure is not a list of changed files")
        if cic:
            if r.get("verdict") != "WAITS_ON_ANDREW" or not str(r.get("row") or "").strip():
                fail("%d changed file(s) are in the print closure: the verdict must be WAITS_ON_ANDREW with a row" % len(cic))
        elif r.get("verdict") != "CLEAR":
            fail("verdict %r with an empty changed_in_closure" % r.get("verdict"))
        if r.get("lint_errors") != 0 or r.get("typecheck_errors") != 0:
            fail("lint_errors %r, typecheck_errors %r" % (r.get("lint_errors"), r.get("typecheck_errors")))
        s = r.get("suite") or {}
        if s.get("fail") != 0 or not isinstance(s.get("pass"), int) or s["pass"] < 1 or r.get("build_ok") is not True:
            fail("suite %r, build_ok %r" % (s, r.get("build_ok")))
        print("OK: the print route's closure holds %d file(s) (control found); %d changed file(s) in it; verdict %s; lint, typecheck, suite and build clean"
              % (pc["closure_files"], len(cic), r["verdict"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
