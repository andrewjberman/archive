"""IRPT_BCKEND workstream ~PM round 3 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the 49 Financial split-adjusted price return pair, ACT 2 (the restatement of the 47 split days).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB244-1  IB-pr-613  invoke irpt-holdings-performance-lambda with {"date": D} once per each of the 47 named split days, in ascending order, outside the scheduled fire window; per day record the prior
           version of the key, read back the new one and compare row by row; stop at the first disagreement
    AC1  the gates: the pair's bytes and both addenda, all CTO halves signed, ACT 1 landed and its first scheduled run read, the function at the signed candidate, one change at a time, the deployed handler's
         date line, the day list equal to the signed delta record's 47 days
    AC2  the 47 days in ascending order: each with its prior version recorded before the write, a new version, only split-holding accounts changed, the changed count equal to the record's per-day count
         (985 on 2026-04-21), the first disagreement stopping the run
    AC3  the totals (47 days, 1,291 changed account-days, the ratio-absent names), the event keys sent (date only), the window, the siblings never invoked, no rollback, the counters
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB244-1_act2_record.json"
DELTA = D + "0.9.0_WK_IRPT_BCKEND~423/IB218-2_split_delta.json"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_COO_HALF.md"
COO_ADD = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_1_COO_HALF.md"
COO_ADD2 = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_2_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_CTO_HALF.md"
CTO_ADD = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_SPLIT_ADJUST_PAIR_ADDENDUM_1_CTO_HALF.md"
CTO_ADD2 = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_SPLIT_ADJUST_ADDENDUM_2_CTO_HALF.md"
PAIR_SHA256 = "8f645588ab1079c35d22002f786c49d2b78dea27ae4e453ac2afb44bf6b9d6e5"
ADD_BLOB = "f0cec424f485aa3fc34a1670a3cf9eab558e42f0"
ADD2_BLOB = "47e819dd938e0d295e6658057a5be7e165836b47"
ADD3_BLOB = "82d849a97c086fb1cb20e761eafad2e79b5a5843"
SOURCE = "schwab_08335338"
CAND = "LiDXhN74TsATYhoQKzs+Oy1qtNn3hDJxxjkLa0ZlfLg="
FN = "irpt-holdings-performance-lambda"
SIBLINGS = ("irpt-inf-holdings-performance-lambda", "irpt-cot-holdings-performance-lambda")
fail, load, is_int = P6.fail, P6.load, P6.is_int


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def blob(rel):
    return subprocess.run(["git", "hash-object", "--stdin"], input=(P6.ROOT / rel).read_bytes(), capture_output=True, timeout=60).stdout.decode().strip()


def days():
    """The 47 signed days with the delta record's per-day counts: [(day, changed, ratio_absent)]."""
    d = load(DELTA)
    out = [(x["day"], x["account_days_changed"], x["securities_ratio_absent"]) for x in d["per_day"]]
    if len(out) != 47 or sum(c for _, c, _ in out) != 1291 or [x[0] for x in out] != sorted(x[0] for x in out):
        fail("the signed delta record must hold 47 ascending days summing to 1,291 changed account-days")
    return out


def ac1(r):
    if hashlib.sha256((P6.ROOT / COO_HALF).read_bytes()).hexdigest() != PAIR_SHA256:
        fail("the COO half of the pair must hash to the signed sha256 %s" % PAIR_SHA256)
    for rel, want in ((COO_ADD, ADD_BLOB), (COO_ADD2, ADD2_BLOB)):
        if blob(rel) != want:
            fail("%s must have the signed blob %s" % (rel, want))
    for rel, key in ((CTO_HALF, PAIR_SHA256[:12]), (CTO_HALF, ADD3_BLOB[:10]), (CTO_ADD, ADD_BLOB[:12]), (CTO_ADD2, ADD2_BLOB[:10])):
        t = text(rel)
        if key not in t or not re.search(r"(?<![A-Za-z])SIGNED", t.upper()):
            fail("the CTO half must name the signed bytes and read SIGNED: %s" % rel)
    g = r.get("gates") or {}
    if g.get("pair_sha256") != PAIR_SHA256 or g.get("addendum_blob") != ADD_BLOB or g.get("addendum_2_blob") != ADD2_BLOB or g.get("addendum_3_blob") != ADD3_BLOB or g.get("both_halves_signed") is not True:
        fail("gates must carry the signed pair's sha256 and the three addendum blobs (ADDENDUM 3: the invoke names its source) and both_halves_signed true")
    a1 = g.get("act_1") or {}
    if a1.get("order_complete") is not True or a1.get("first_scheduled_run_read") is not True or a1.get("manifest_split_adjust_declared") is not True:
        fail("gates.act_1 must read order_complete true, first_scheduled_run_read true and manifest_split_adjust_declared true (CTO condition 5: Act 2 starts only after that run is read)")
    if g.get("function_code_sha256") != CAND:
        fail("gates.function_code_sha256 must equal the signed candidate %s" % CAND)
    if g.get("one_change_at_a_time") is not True or g.get("act_1_ledger_closed") is not True:
        fail("gates.one_change_at_a_time and gates.act_1_ledger_closed must be true (no other apply on the root; Act 1's ledger closed by the issuer)")
    if g.get("deployed_handler_date_line_present") is not True or g.get("producer_date_parameter_present") is not True:
        fail("the DEPLOYED handler's date line and the producer's --date parameter must be present before the first invoke (CTO condition 1: absence is a STOP)")
    cen = g.get("schema_reader_census") or {}
    if cen.get("done") is not True or cen.get("readers_refusing_1_2") != 0:
        fail("gates.schema_reader_census must read done true and readers_refusing_1_2 0 (CTO rule A, msg 9476: a reader that refuses schema 1.2 stops the run before day 2)")
    want = days()
    if g.get("days_equal_signed_record") is not True or g.get("delta_record_sha256") != hashlib.sha256((P6.ROOT / DELTA).read_bytes()).hexdigest():
        fail("gates.days_equal_signed_record must be true and gates.delta_record_sha256 must equal the sha256 of %s" % DELTA)
    print("OK: the gates: the pair and addenda, Act 1 landed and read, the candidate live, the handler line, the %d signed days" % len(want))


def ac2(r):
    want = days()
    rows = r.get("days")
    if not isinstance(rows, list):
        fail("days must be a list")
    stop = r.get("stopped_at")
    if stop is not None:
        fail("the run stopped at %s: the first disagreement stops Act 2 (Branch B for the keys written is the issuer's call); this record does not pass" % stop)
    if [x.get("day") for x in rows] != [d for d, _, _ in want]:
        fail("days must be exactly the 47 signed days in ascending order (a date outside the 47 is a STOP)")
    for x, (d, changed, _) in zip(rows, want):
        if not x.get("prior_version_id") or not x.get("new_version_id") or x["prior_version_id"] == x["new_version_id"]:
            fail("%s: the prior version id must be recorded BEFORE the write and the new version must differ from it" % d)
        if x.get("rows_changed") != changed or x.get("rows_changed_expected") != changed:
            fail("%s: rows_changed must equal the signed per-day count %d (read %r)" % (d, changed, x.get("rows_changed")))
        if x.get("columns_compared") != 19 or x.get("schema_new") != "1.2":
            fail("%s: the comparison runs over the 19 columns of the prior key and the new key reads schema 1.2 (CTO rule A)" % d)
        if x.get("other_rows_changed") != 0 or x.get("comparison_ok") is not True or x.get("changed_only_split_holders") is not True:
            fail("%s: only accounts that held a split security at t-1 may change (other_rows_changed 0, changed_only_split_holders true, comparison_ok true)" % d)
    if next(x for x in rows if x["day"] == "2026-04-21")["rows_changed"] != 985:
        fail("2026-04-21 must read 985 changed account-days (CTO condition 4, not the typed 920)")
    print("OK: the 47 days in ascending order, each with its prior version, only split-holders changed, each count equal to the signed one")


def ac3(r):
    want = days()
    t = r.get("totals") or {}
    if t.get("days_run") != 47 or t.get("account_days_changed") != 1291 or t.get("invokes") != 47 or r.get("refused_invokes") != 1:
        fail("totals must read days_run 47, account_days_changed 1291, invokes 47 (that wrote) and refused_invokes 1 (the day-1 invoke the producer refused before ADDENDUM 3, which wrote nothing)")
    if t.get("ratio_absent_named_total") != sum(x for _, _, x in want):
        fail("totals.ratio_absent_named_total must equal the signed record's ratio-absent security-days (%d): the manifests name them, never silent (CTO condition 3)" % sum(x for _, _, x in want))
    if r.get("event_keys_sent") != ["date", "source"] or r.get("event_source") != SOURCE or r.get("source_read_from_schedule") is not True:
        fail("event_keys_sent must be exactly [date, source] with event_source %s read from the schedule's Target.Input (ADDENDUM 3, CTO condition 1 as amended); no other key" % SOURCE)
    w = r.get("window") or {}
    if not (is_int(w.get("minutes_clear_before_fire_min")) and w["minutes_clear_before_fire_min"] >= 30 and is_int(w.get("minutes_clear_after_fire_min")) and w["minutes_clear_after_fire_min"] >= 30):
        fail("window.minutes_clear_before_fire_min and minutes_clear_after_fire_min must both be 30 or more (one writer per key)")
    if r.get("siblings_invoked") != 0:
        fail("siblings_invoked must be 0: the siblings are never invoked by this pair")
    if r.get("rollback_performed") is not False:
        fail("rollback_performed must be false for a completed Act 2")
    c = r.get("counters") or {}
    wantc = {"lambda_invokes": 48, "version_deletes": 0, "iam_changes": 0, "schedule_changes": 0, "artifact_uploads": 0, "other_keys_written": 0, "markers_closed": 0}
    for k, v in wantc.items():
        if c.get(k) != v:
            fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the totals, the event keys, the window, the siblings never invoked, no rollback, the counters")


CHECKS = {"IB244-1-AC1": ac1, "IB244-1-AC2": ac2, "IB244-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p244_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
