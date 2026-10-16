"""IRPT_BCKEND workstream ~PM round 2 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the 49 Financial split-adjusted price return pair, ACT 1 (AMENDED for ADDENDUM 2: the release of the THREE holdings-performance functions, which share one artifact key, to candidate LiDXhN74).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB243-1  IB-pr-612  release the three holdings-performance functions from live o9UugRAV to the signed candidate LiDXhN74 (2 of 14 members), once, by one Terraform plan of 3 changes; read each first scheduled run
    AC1  the gates: all halves signed at the pair's bytes and the two addendum blobs, one change at a time, the manifest-reader census read with no reader refusing an unknown key, each of the three live CodeSha256 equal to the signed one, the Branch B version named
    AC2  the apply: the source-map rows landed (2, siblings 0), the build from the REAL map equal to the signed digest, the ledger opened first, the saved plan 0/3/0, safe-apply rc 0, the after-state (each function's digest, re-plan 0, exactly two members)
    AC3  the health proof (10 minutes or more, 0 errors), the deployed handler's date line, the first scheduled run's manifest (split_adjust declared, counts), the per-sibling DELTA = 0, no rollback, the counters, Act 2 not started
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB243-1_apply_record.json"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_COO_HALF.md"
COO_ADD = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_1_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_CTO_HALF.md"
CTO_ADD = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_1_CTO_HALF.md"
PAIR_SHA256 = "8f645588ab1079c35d22002f786c49d2b78dea27ae4e453ac2afb44bf6b9d6e5"
ADD_BLOB = "f0cec424f485aa3fc34a1670a3cf9eab558e42f0"
ADD2_BLOB = "47e819dd938e0d295e6658057a5be7e165836b47"
COO_ADD2 = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_2_COO_HALF.md"
CTO_ADD2 = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_SPLIT_ADJUST_ADDENDUM_2_CTO_HALF.md"
LIVE = "o9UugRAVhYmF3Q2ULtU6eaaNiLFRAFWW4tjjQPyj2Ok="
CAND = "LiDXhN74TsATYhoQKzs+Oy1qtNn3hDJxxjkLa0ZlfLg="
MEMBERS = ("holdings_performance.py", "sources.json")
SIBLINGS = ("irpt-inf-holdings-performance-lambda", "irpt-cot-holdings-performance-lambda")
FN = "irpt-holdings-performance-lambda"
THREE = (FN,) + SIBLINGS
fail, load, is_int = P6.fail, P6.load, P6.is_int


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def ac1(r):
    if hashlib.sha256((P6.ROOT / COO_HALF).read_bytes()).hexdigest() != PAIR_SHA256:
        fail("the COO half of the pair must hash to the signed sha256 %s (different bytes void the CTO half)" % PAIR_SHA256)
    import subprocess

    def blob(rel):
        return subprocess.run(["git", "hash-object", "--stdin"], input=(P6.ROOT / rel).read_bytes(), capture_output=True, timeout=60).stdout.decode().strip()
    for rel, want, name in ((COO_ADD, ADD_BLOB, "ADDENDUM 1"), (COO_ADD2, ADD2_BLOB, "ADDENDUM 2")):
        if blob(rel) != want:
            fail("the COO %s must have the signed blob %s, reads %s" % (name, want, blob(rel)))
    if PAIR_SHA256[:12] not in text(CTO_HALF) or ADD_BLOB[:12] not in text(CTO_ADD) or ADD2_BLOB[:10] not in text(CTO_ADD2):
        fail("the CTO halves must name the pair's sha256, the addendum blob and the addendum-2 blob")
    for rel in (CTO_HALF, CTO_ADD, CTO_ADD2):
        if not re.search(r"(?<![A-Za-z])SIGNED", text(rel).upper()):
            fail("all three CTO halves must read SIGNED: %s" % rel)
    g = r.get("gates") or {}
    if g.get("pair_sha256") != PAIR_SHA256 or g.get("addendum_blob") != ADD_BLOB or g.get("addendum_2_blob") != ADD2_BLOB or g.get("both_halves_signed") is not True:
        fail("gates.pair_sha256, addendum_blob, addendum_2_blob and both_halves_signed must match the signed pair and its two addenda")
    if g.get("one_change_at_a_time") is not True:
        fail("gates.one_change_at_a_time must be true (no open ledger or marker naming a function or the root)")
    if g.get("manifest_reader_census_read") is not True or g.get("reader_refusing_unknown_key") != 0:
        fail("gates.manifest_reader_census_read must be true and gates.reader_refusing_unknown_key 0 (CTO ADDENDUM 2 condition 1: a reader that refuses an unknown key is a STOP)")
    if (r.get("start_read") or {}).get("code_sha256") != LIVE:
        fail("start_read.code_sha256 must equal the signed live CodeSha256 %s (another release landed first: STOP)" % LIVE)
    fn = r.get("functions") or {}
    if sorted(fn) != sorted(THREE):
        fail("functions must hold exactly the three functions %s" % (THREE,))
    for f in THREE:
        if fn[f].get("code_sha256_before") != LIVE:
            fail("functions.%s.code_sha256_before must equal %s (the three run one zip today; any other value is a STOP)" % (f, LIVE))
    if not r.get("branch_b_version_id"):
        fail("branch_b_version_id must name the S3 version whose content equals the live CodeSha256, BEFORE any upload (one version for all three)")
    print("OK: the gates, the reader census, the live identity of the three functions and Branch B agree with the signed pair and its addenda")


def ac2(r):
    sm = r.get("source_map_rows") or {}
    if sm.get("committed") is not True or sm.get("function") != FN or sm.get("rows_changed") != 2 or sm.get("siblings_changed") != 0:
        fail("source_map_rows must read committed true, function %s, rows_changed 2 (the two members), siblings_changed 0" % FN)
    ap = r.get("apply") or {}
    if ap.get("build_real_map_code_sha256") != CAND or ap.get("built_code_sha256") != CAND:
        fail("the build from the REAL map and the built artifact must both print the signed digest %s (any other: ABORT)" % CAND)
    if ap.get("plan") != {"add": 0, "change": 3, "destroy": 0} or ap.get("safe_apply_rc") != 0 or ap.get("path") != "terraform-safe-apply":
        fail("apply.plan must read 0 add, 3 change, 0 destroy (the three functions); safe_apply_rc 0; path terraform-safe-apply")
    lg = r.get("ledger") or {}
    if lg.get("opened_before_the_apply") is not True or not str(lg.get("entry", "")).startswith("org/critical_paths/change_management/"):
        fail("ledger must name an entry under org/critical_paths/change_management/ opened before the apply")
    af = r.get("after") or {}
    if af.get("replan_changes") != 0:
        fail("after.replan_changes must be 0")
    if sorted(af.get("changed_members") or []) != sorted(MEMBERS):
        fail("after.changed_members must be exactly %s (2 of 14)" % (MEMBERS,))
    fn = r.get("functions") or {}
    for f in THREE:
        if (fn.get(f) or {}).get("code_sha256_after") != CAND:
            fail("functions.%s.code_sha256_after must equal the signed candidate %s (all three move together; any other: Branch B)" % (f, CAND))
    print("OK: the source-map rows, the build, the 3-change plan, the apply and the after-state of the three functions agree with the signed pair")


def ac3(r):
    hp = r.get("health_proof") or {}
    if not (is_int(hp.get("window_minutes")) and hp["window_minutes"] >= 10 and is_int(hp.get("invocations")) and hp["invocations"] >= 0 and hp.get("errors") == 0 and hp.get("throttles_429") == 0):
        fail("health_proof must read a window of 10 minutes or more, invocations an integer, errors 0 and throttles_429 0")
    if r.get("deployed_handler_date_line_present") is not True:
        fail("deployed_handler_date_line_present must be true (Act 2 needs the handler's event date path in the DEPLOYED zip)")
    fr = r.get("first_scheduled_run") or {}
    if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", str(fr.get("fire_utc_stated_before_apply"))):
        fail("first_scheduled_run.fire_utc_stated_before_apply must be an ISO UTC time stated before the apply")
    if fr.get("manifest_split_adjust_declared") is not True:
        fail("first_scheduled_run.manifest_split_adjust_declared must be true (the run after the apply carries the declaration)")
    for k in ("securities_ratio_absent", "days_ratio_absent", "unkeyed_split_rows"):
        if not (is_int(fr.get(k)) and fr[k] >= 0):
            fail("first_scheduled_run.%s must be a non-negative integer (counts only)" % k)
    if fr.get("run_ok") is not True:
        fail("first_scheduled_run.run_ok must be true (the scheduled run completed without error)")
    sd = r.get("sibling_delta") or {}
    if sorted(sd) != sorted(SIBLINGS):
        fail("sibling_delta must hold exactly the two siblings %s" % (SIBLINGS,))
    for f in SIBLINGS:
        e = sd[f]
        if e.get("rows_delta_zero") is not True or e.get("manifest_only_added_key") != "split_adjust" or e.get("replay_non_writing") is not True:
            fail("sibling_delta.%s must read rows_delta_zero true, manifest_only_added_key split_adjust and replay_non_writing true (CTO ADDENDUM 2: DELTA = 0, or Branch B)" % f)
    if r.get("rollback_performed") is not False:
        fail("rollback_performed must be false for a landed release")
    if r.get("act2_started") is not False:
        fail("act2_started must be false: Act 2 (the 47 days) is a separate order after this read")
    c = r.get("counters") or {}
    want = {"artifact_uploads": 1, "lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "backfills": 0, "served_keys_written_by_me": 0, "files_deleted": 0, "markers_closed": 0}
    for k, v in want.items():
        if c.get(k) != v:
            fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the health proof, the handler line, the first scheduled run, no rollback, the counters, Act 2 not started")


CHECKS = {"IB243-1-AC1": ac1, "IB243-1-AC2": ac2, "IB243-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p243_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
