"""IRPT_DASHBD round 92 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 7063, round-92 analysis section 3 item 2.

Cell DB-b-172 (~138, LOCAL, read-only; S3 GET/LIST only, zero vendor calls, zero secret reads, no served byte moves): the BD_EXCLUDES_SERVED_INCOME read of the 23 differing days of the 7 open windows.
Test: on the day, the gap (BD minus served) is minus the served income over the prior value, within 0.01 pp. Correction: remove that income from the served day's return and recompute the window; the reason is taken
only if the window re-closes within 0.35 pp. The other days are re-tested under the full list, round 91's Reading B included, after the new reason's days are corrected.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB92-1-AC1  ~138/EXCLUDES_INCOME_23_DAYS.json: tolerance_pp 0.35; rule {file in the worker's folder, sha256 equal to its bytes, commit 7-40 hex, written_before_read true}; reasons_list equal to the closed list below, in order (the new reason first); code {file under org/missions/D9/IRPT/IRPT_DASHBD/, sha256 equal to its bytes, tracked true}; population {accounts 7, windows 7, differing_days 23} and per-account days_differing equal
              to round 90's committed record (~136/DAY_READ_7.json) in plan order; sources {bd_transactions_rows_read int > 0, served_rows_read int > 0}; per_account (7, no ids): by_reason six ints summing to
              days_differing, evidence for every reason above 0 except UNEXPLAINED ({kind count|multiple|day_offsets, values ints}), unexplained_days [{offset, size_pp}] equal in number to UNEXPLAINED,
              uncorrected_window_misses true (negative arm), window_closed_after_correction a bool that is true exactly when no day is UNEXPLAINED; summary matches; a surprise_row exactly when an account stays
              UNEXPLAINED; reads {vendor_calls 0, secret_reads 0, s3_writes 0}; served_values_changed false; no run of 8 or more digits (sha256 and commit members excepted).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
FOLDER = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~138"
ROUND90 = PROJ + "deliverables/0.9.0_WK_IRPT_DASHBD~136/DAY_READ_7.json"
REASONS = ("BD_EXCLUDES_SERVED_INCOME", "BD_INCOME_PER_LOT", "DUPLICATE_ROW", "BOOKING_DATE_DIFFERS", "MISSING_IN_LEDGER", "UNEXPLAINED")
RUN = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


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
        need(cid == "DB92-1-AC1", "unknown criterion %r" % cid)
        p = root / FOLDER / "EXCLUDES_INCOME_23_DAYS.json"
        need(p.is_file(), "no %s/EXCLUDES_INCOME_23_DAYS.json" % FOLDER)
        r = json.loads(p.read_bytes().decode("utf-8"))
        need(r.get("tolerance_pp") == 0.35, "tolerance_pp %r" % r.get("tolerance_pp"))
        ru = r.get("rule") or {}
        rf = root / FOLDER / str(ru.get("file") or "")
        need(str(ru.get("file") or "").strip() and rf.is_file(), "rule.file must name a file in the worker's folder")
        need(hashlib.sha256(rf.read_bytes()).hexdigest() == ru.get("sha256"), "rule.sha256 does not equal the rule file's bytes: the rule changed after it was recorded")
        need(re.fullmatch(r"[0-9a-f]{7,40}", str(ru.get("commit") or "")) and ru.get("written_before_read") is True, "rule.commit and written_before_read true are required")
        need(tuple(r.get("reasons_list") or ()) == REASONS, "reasons_list must be the closed list %r, in order" % (REASONS,))
        code = r.get("code") or {}
        f = str(code.get("file") or "")
        need(f.startswith(PROJ) and code.get("tracked") is True and re.fullmatch(r"[0-9a-f]{64}", str(code.get("sha256") or "")), "code %r" % code)
        need((root / f).is_file() and hashlib.sha256((root / f).read_bytes()).hexdigest() == code["sha256"], "code file missing or its sha256 differs from the record")
        r90p = root / ROUND90
        need(r90p.is_file(), "round 90's record %s is missing" % ROUND90)
        r90 = json.loads(r90p.read_bytes().decode("utf-8"))
        want = [a["days_differing"] for a in r90["per_account"]]
        need(len(want) == 7 and sum(want) == 23, "round 90's record does not read 7 accounts and 23 differing days")
        pop = r.get("population") or {}
        need(pop.get("accounts") == 7 and pop.get("windows") == 7 and pop.get("differing_days") == 23, "population %r" % pop)
        th = r.get("test_held_days")
        need(is_int(th) and th <= 23, "test_held_days (the days on which BD_EXCLUDES_SERVED_INCOME's test held, before any window test) must be an int of 0 to 23")
        sr = r.get("sources") or {}
        need(is_int(sr.get("bd_transactions_rows_read")) and sr["bd_transactions_rows_read"] > 0 and is_int(sr.get("served_rows_read")) and sr["served_rows_read"] > 0,
             "sources %r must name the rows read on each side" % sr)
        pa = r.get("per_account")
        need(isinstance(pa, list) and len(pa) == 7, "per_account must list the 7 accounts (no ids)")
        closed = unexpl = 0
        for i, a in enumerate(pa):
            need(a.get("days_differing") == want[i], "per_account[%d] days_differing %r, round 90's record says %d" % (i, a.get("days_differing"), want[i]))
            br = a.get("by_reason") or {}
            need(all(is_int(br.get(k)) for k in REASONS) and sum(br[k] for k in REASONS) == want[i], "per_account[%d] by_reason %r must be six ints summing to %d" % (i, br, want[i]))
            ev = a.get("evidence") or {}
            for k in REASONS[:-1]:
                if br[k] > 0:
                    e = ev.get(k) or {}
                    v = e.get("values")
                    need(e.get("kind") in ("count", "multiple", "day_offsets") and isinstance(v, list) and v and all(isinstance(x, int) and not isinstance(x, bool) for x in v),
                         "per_account[%d] evidence for %s must be a count, a multiple or day offsets, as ints" % (i, k))
            ud = a.get("unexplained_days")
            need(isinstance(ud, list) and len(ud) == br["UNEXPLAINED"] and all(isinstance(x, dict) and is_int(x.get("offset")) and num(x.get("size_pp")) for x in ud),
                 "per_account[%d] unexplained_days must be {offset, size_pp} entries equal to the UNEXPLAINED count" % i)
            need(a.get("uncorrected_window_misses") is True, "per_account[%d] negative arm: the uncorrected window must still miss at 0.35 pp" % i)
            w = a.get("window_closed_after_correction")
            need(isinstance(w, bool) and w == (br["UNEXPLAINED"] == 0), "per_account[%d] a window is closed exactly when no day is UNEXPLAINED" % i)
            need(br["BD_EXCLUDES_SERVED_INCOME"] <= th, "per_account[%d] more days taken by BD_EXCLUDES_SERVED_INCOME than its test held on" % i)
            closed += 1 if w else 0
            unexpl += 0 if w else 1
        need(sum(a["by_reason"]["BD_EXCLUDES_SERVED_INCOME"] for a in pa) <= th, "the days taken exceed the days the test held on")
        sm = r.get("summary") or {}
        need(sm.get("accounts_closed_with_reasons") == closed and sm.get("accounts_unexplained") == unexpl, "summary %r, expected closed %d unexplained %d" % (sm, closed, unexpl))
        need(isinstance(r.get("round91_pattern_8_days_confirmed"), bool), "round91_pattern_8_days_confirmed (test_held_days equals the 8 days worker 137 measured) must be a bool")
        row = str(r.get("surprise_row") or "").strip()
        need((unexpl > 0) == bool(row), "a surprise_row naming the unexplained is required exactly when an account stays UNEXPLAINED")
        rd = r.get("reads") or {}
        need(rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0 and rd.get("s3_writes") == 0, "reads %r" % rd)
        need(r.get("served_values_changed") is False, "served_values_changed must be false")
        hits = long_digit_runs(r)
        need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
        print("OK: 23 differing days over 7 accounts read against %d BD rows and %d served rows: %d account(s) closed with reasons, %d with UNEXPLAINED days"
              % (sr["bd_transactions_rows_read"], sr["served_rows_read"], closed, unexpl))
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB92"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
