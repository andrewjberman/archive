"""IRPT_DASHBD round 93 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 7081, round-93 analysis section 3 item 2.

Cell DB-b-173 (~139, LOCAL, DIRECT ACT, read-only on stored local files, zero S3 access, zero vendor calls, no served byte moves): ONE figure. Account 5 of the round-90 plan order
(7 differing days: 4 taken by BD_EXCLUDES_SERVED_INCOME, 3 UNEXPLAINED each under 0.07 pp): the window return after its 4 reasoned days are corrected, against 0.35 pp, by the window method of
round 92's RULE_EXCL.md section 5 (unchanged, bound by hash); the 3 UNEXPLAINED days stay as served.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB93-1-AC1  ~139/ACCOUNT5_CORRECTED_WINDOW.json: tolerance_pp 0.35; rule {file = round 92's RULE_EXCL.md, sha256 equal to its bytes, reused_unchanged true}; code {file under
              org/missions/D9/IRPT/IRPT_DASHBD/, sha256 equal to its bytes, tracked true}; account_index_plan_order 5; reasoned_days and unexplained_days equal to round 92's committed record for the fifth
              account (4 and 3); uncorrected_gap_pp a number above 0.35 (the negative arm, equal in verdict to round 92's uncorrected_window_misses true); corrected_gap_pp a number >= 0;
              corrected_differs_from_uncorrected true and consistent (the two gaps are not equal); inside_tolerance a bool equal to (corrected_gap_pp <= 0.35); reads {vendor_calls 0, secret_reads 0,
              s3_writes 0, s3_reads 0}; served_values_changed false; no run of 8 or more digits (sha256 and commit members excepted).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~139"
R92 = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~138/EXCLUDES_INCOME_23_DAYS.json"
RULE = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~138/RULE_EXCL.md"
RUN = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) != "commit":
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    try:
        need(cid == "DB93-1-AC1", "unknown criterion %r" % cid)
        p = root / FOLDER / "ACCOUNT5_CORRECTED_WINDOW.json"
        need(p.is_file(), "no %s/ACCOUNT5_CORRECTED_WINDOW.json" % FOLDER)
        r = json.loads(p.read_bytes().decode("utf-8"))
        need(r.get("tolerance_pp") == 0.35, "tolerance_pp %r" % r.get("tolerance_pp"))
        ru = r.get("rule") or {}
        rf = root / RULE
        need(rf.is_file() and ru.get("file") == RULE and ru.get("reused_unchanged") is True and hashlib.sha256(rf.read_bytes()).hexdigest() == ru.get("sha256"),
             "rule must be round 92's RULE_EXCL.md, reused unchanged, with its sha256")
        code = r.get("code") or {}
        f = str(code.get("file") or "")
        need(f.startswith(PROJ) and code.get("tracked") is True and re.fullmatch(r"[0-9a-f]{64}", str(code.get("sha256") or "")), "code %r" % code)
        need((root / f).is_file() and hashlib.sha256((root / f).read_bytes()).hexdigest() == code["sha256"], "code file missing or its sha256 differs from the record")
        r92p = root / R92
        need(r92p.is_file(), "round 92's record %s is missing" % R92)
        a5 = json.loads(r92p.read_bytes().decode("utf-8"))["per_account"][4]
        want_r, want_u = a5["by_reason"]["BD_EXCLUDES_SERVED_INCOME"], a5["by_reason"]["UNEXPLAINED"]
        need(a5["days_differing"] == 7 and want_r == 4 and want_u == 3, "round 92's fifth account does not read 7 differing days, 4 reasoned, 3 unexplained")
        need(r.get("account_index_plan_order") == 5, "account_index_plan_order must be 5")
        need(r.get("reasoned_days") == want_r and r.get("unexplained_days") == want_u, "reasoned_days and unexplained_days must equal round 92's record (%d and %d)" % (want_r, want_u))
        ug, cg = r.get("uncorrected_gap_pp"), r.get("corrected_gap_pp")
        need(num(ug) and ug > 0.35 and a5["uncorrected_window_misses"] is True, "uncorrected_gap_pp %r: the negative arm needs a gap above 0.35 pp" % ug)
        need(num(cg) and cg >= 0 and cg != ug, "corrected_gap_pp %r must be a number of 0 or more that differs from the uncorrected gap" % cg)
        need(isinstance(r.get("inside_tolerance"), bool) and r["inside_tolerance"] == (cg <= 0.35), "inside_tolerance must equal (corrected_gap_pp <= 0.35)")
        rd = r.get("reads") or {}
        need(rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0 and rd.get("s3_writes") == 0 and rd.get("s3_reads") == 0, "reads %r" % rd)
        need(r.get("served_values_changed") is False, "served_values_changed must be false")
        hits = long_digit_runs(r)
        need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: account 5 (plan order), %d reasoned days corrected, %d UNEXPLAINED days as served: uncorrected gap %.4f pp, corrected gap %.4f pp, inside 0.35 pp: %s"
              % (want_r, want_u, ug, cg, str(r["inside_tolerance"]).lower()))
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB93"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
