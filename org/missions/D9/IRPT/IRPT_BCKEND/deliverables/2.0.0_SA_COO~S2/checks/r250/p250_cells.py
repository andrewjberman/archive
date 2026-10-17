"""IRPT_BCKEND workstream ~PS round 10 (issuer 2.0.0_SA_COO~S2) -- the check of one APPLY order: the NEW irpt-export-render bundle that reads the CURRENT filled-report object and
refuses on a sha256 or size mismatch (IB-pr-551 ADDENDUM 3; built by TO-IB-pr-617 and TO-IB-pr-619, merged at 1dab1295ef).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB250-1  IB-pr-618  APPLY the new export bundle, code attributes only, BEFORE the IAM statement
    AC1  the gates: ADDENDUM 3's blob with its CTO half SIGNED, IB-pr-616's ledger in its by-design state (L1 to L6 closed, L7 open), one change at a time, the BEFORE sha equal to the order's
    AC2  the build: the bundle was built from a commit that is an ancestor of HEAD; the retained_export.py inside the zip is the blob of that commit; and that file's read_pinned_filled reads the current object (no version_id passed)
    AC3  the apply: the plan exactly 0 add / 1 change / 0 destroy on the function, the live CodeSha256 equal to the built zip and different from before, a clean re-plan, the environment untouched, the counters, no rollback
"""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
REC = D + "0.7.0_AE_CloudOps~IB2/IB250-1_bundle_record.json"
A3_COO = D + "2.0.0_SA_COO~S2/NEVER_WIDEN_IB_pr_551_ADDENDUM_3_GETOBJECT_ONLY_SHA256_REFUSAL_COO_HALF.md"
PAIR_CTO = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_551_SERVE_PATH_HOPS_2_4_CTO_HALF.md"
A3_COO_BLOB = "87a46d9cf370c293dae46a413cba213db721b5ef"
EXPORT_BEFORE = "5bIgn/MLNgtNtDnRpmE3OejAMw2IpoJBmzzRfHvFLXI="
READ_LIVE = "z634S2QsrfCpY4c3cD2UGwicdmLDo6/Rmng8SrEskCQ="
FN = "irpt-export-render"
TARGET = "infra/aws/lambda/investor-reporting/export/retained_export.py"
ROOT = Path(".")
CID = ""


def fail(msg):
    print("%s FAIL: %s" % (CID, msg))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no record at %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def git(*args):
    return subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True, text=True, timeout=60)


def hex40(v):
    return isinstance(v, str) and re.fullmatch(r"[0-9a-f]{40}", v) is not None


def ac1(r):
    f = ROOT / A3_COO
    if not f.is_file():
        fail("no %s" % A3_COO)
    blob = subprocess.run(["git", "hash-object", "--stdin"], input=f.read_bytes(), capture_output=True, timeout=60).stdout.decode().strip()
    if blob != A3_COO_BLOB:
        fail("ADDENDUM 3's COO half must hold its signed blob %s" % A3_COO_BLOB)
    cto = (ROOT / PAIR_CTO).read_text(encoding="utf-8") if (ROOT / PAIR_CTO).is_file() else ""
    if A3_COO_BLOB[:10] not in cto or len(re.findall(r"(?<![A-Za-z])SIGNED", cto)) < 4:
        fail("the CTO half must name ADDENDUM 3's blob and read SIGNED for the pair and ADDENDUM 1, 2 and 3")
    g = r.get("gates") or {}
    if g.get("addendum_3_blob") != A3_COO_BLOB or g.get("all_halves_signed") is not True:
        fail("gates must carry ADDENDUM 3's blob and all_halves_signed true")
    led = g.get("ledger_616") or {}
    if led.get("l1_to_l6_closed") is not True or led.get("l7_open_by_design") is not True:
        fail("gates.ledger_616 must read l1_to_l6_closed true and l7_open_by_design true: the only open ledger naming the function is IB-pr-616's, with its IAM leg owed")
    if g.get("one_change_at_a_time") is not True or not isinstance(g.get("open_deploys_worktrees_read"), int) or g["open_deploys_worktrees_read"] < 1:
        fail("gates.one_change_at_a_time must be true and the worktree union of .open_deploys printed with a denominator of 1 or more")
    if (g.get("before") or {}).get("export_function_sha256") != EXPORT_BEFORE:
        fail("gates.before.export_function_sha256 must equal the order's BEFORE %s; a different value is a STOP and a re-cut" % EXPORT_BEFORE)
    print("OK: the gates: ADDENDUM 3 signed at its blob, IB-pr-616's ledger in its by-design state, one change at a time, the BEFORE equal")


def ac2(r):
    b = r.get("build") or {}
    commit, blobid = b.get("commit"), b.get("retained_export_blob")
    if not hex40(commit) or not hex40(blobid) or not b.get("built_sha256"):
        fail("build must carry a 40-hex commit, the 40-hex git blob of retained_export.py inside the zip, and the built zip's base64 sha256")
    if git("merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
        fail("the build commit %s must be an ancestor of HEAD" % commit[:10])
    at = git("rev-parse", "%s:%s" % (commit, TARGET))
    if at.returncode != 0 or at.stdout.strip() != blobid:
        fail("the retained_export.py inside the zip must be the blob the build commit holds (%s vs %s)" % (blobid[:10], at.stdout.strip()[:10]))
    src = git("show", "%s:%s" % (commit, TARGET)).stdout
    fn = next((n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "read_pinned_filled"), None)
    if fn is None:
        fail("no read_pinned_filled in the built file")
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and any(k.arg == "version_id" for k in node.keywords):
            fail("the built read_pinned_filled still passes version_id (the old code would call GetObject with a VersionId the new grant forbids)")
    seg = ast.get_source_segment(src, fn) or ""
    if 'pin["sha256"]' not in seg or "changed" not in seg or "resubmit" not in seg:
        fail("the built read_pinned_filled must keep the sha256 comparison and the worded refusal")
    if b.get("import_smoke_rc") != 0:
        fail("build.import_smoke_rc must be 0 (the bundle imports in a fresh directory)")
    print("OK: the bundle was built from an ancestor of HEAD, the zip holds that commit's retained_export.py, which reads the current object and refuses on a change")


def ac3(r):
    a = r.get("apply") or {}
    p = a.get("plan") or {}
    if not (p.get("add") == 0 and p.get("change") == 1 and p.get("destroy") == 0) or not (isinstance(p.get("resources"), list) and len(p["resources"]) == 1):
        fail("apply.plan must read exactly 0 add / 1 change / 0 destroy on exactly one resource (the function's code attributes)")
    built = (r.get("build") or {}).get("built_sha256")
    if not a.get("after_sha256") or a.get("after_sha256") != built or a.get("after_sha256") == EXPORT_BEFORE:
        fail("apply.after_sha256 must equal the built zip's sha256 and differ from the BEFORE")
    if a.get("replan_changes") != 0:
        fail("apply.replan_changes must read 0")
    if a.get("read_stamp_sha256") != READ_LIVE or a.get("stamp_file") != "function-map":
        fail("apply.read_stamp_sha256 must equal the read function's live sha %s and apply.stamp_file must read function-map (the drain left both stamps at the pre-release shas)" % READ_LIVE)
    if a.get("env_vars_before") != a.get("env_vars_after") or a.get("switch_changes") != 0:
        fail("the environment must be untouched (equal variable counts, switch_changes 0)")
    c = r.get("counters") or {}
    for k in ("rollback_performed", "console_edits", "invokes", "iam_changes"):
        want = False if k == "rollback_performed" else 0
        if c.get(k) != want:
            fail("counters.%s must read %r, read %r" % (k, want, c.get(k)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the plan 0/1/0, the live sha equal to the built zip, a clean re-plan, the environment untouched, no invoke, no rollback")


CHECKS = {"IB250-1-AC1": ac1, "IB250-1-AC2": ac2, "IB250-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p250_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT, CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
