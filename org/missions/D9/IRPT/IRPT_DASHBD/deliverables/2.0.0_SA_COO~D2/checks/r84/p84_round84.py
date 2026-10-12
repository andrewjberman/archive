"""IRPT_DASHBD round 84 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 6130: one read, not a ruling.

Cell DB-b-162: on the 234 flow-bearing days behind the 51 segments, a count by when the deposited cash was first invested (same
day, next trading day, later, never in the window), under a rule written BEFORE the count, on a copy.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB84-1-AC1  ~131/FLOW_DAYS_FIRST_INVESTED.json: rule {file (exists in the worker's folder), sha256 (equals the file's bytes),
              commit (7 or more hex), written_before_count true}; flow_bearing_days (int > 0) == deposit_days + withdrawal_days +
              other_days; classes {same_day, next_trading_day, later, never_in_window, not_determinable} ints summing to
              deposit_days; accounts (int > 0); on_a_copy true; s3_writes 0; picks_no_convention true; the_39 {count 39,
              accrual_class 31, unclassed 8, statement}; no string holds a run of 8 or more digits (sha256 members excepted).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

M = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RUN = re.compile(r"\d{8,}")
CLASSES = ("same_day", "next_trading_day", "later", "never_in_window", "not_determinable")


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


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "DB84"))
        sys.exit(1)

    if cid != "DB84-1-AC1":
        fail("unknown criterion %r" % cid)
    folder = root / (M + "0.9.0_WK_IRPT_DASHBD~131")
    p = folder / "FLOW_DAYS_FIRST_INVESTED.json"
    if not p.is_file():
        fail("no record 0.9.0_WK_IRPT_DASHBD~131/FLOW_DAYS_FIRST_INVESTED.json")
    r = json.loads(p.read_bytes().decode("utf-8"))
    ru = r.get("rule") or {}
    rf = folder / str(ru.get("file") or "")
    if not str(ru.get("file") or "").strip() or not rf.is_file():
        fail("rule.file must name a file in the worker's folder")
    if hashlib.sha256(rf.read_bytes()).hexdigest() != ru.get("sha256"):
        fail("rule.sha256 does not equal the rule file's bytes: the rule changed after it was recorded")
    if not re.fullmatch(r"[0-9a-f]{7,40}", str(ru.get("commit") or "")) or ru.get("written_before_count") is not True:
        fail("rule.commit and written_before_count true are required")
    keys = ("flow_bearing_days", "deposit_days", "withdrawal_days", "other_days", "accounts")
    if any(not is_int(r.get(k)) for k in keys) or r["flow_bearing_days"] < 1 or r["accounts"] < 1 \
            or r["deposit_days"] + r["withdrawal_days"] + r["other_days"] != r["flow_bearing_days"]:
        fail("flow_bearing_days must be deposit_days + withdrawal_days + other_days, with accounts")
    c = r.get("classes") or {}
    if any(not is_int(c.get(k)) for k in CLASSES) or sum(c[k] for k in CLASSES) != r["deposit_days"]:
        fail("classes must be five counts summing to deposit_days")
    if r.get("on_a_copy") is not True or r.get("s3_writes") != 0 or r.get("picks_no_convention") is not True:
        fail("on_a_copy true, s3_writes 0 and picks_no_convention true are required")
    t = r.get("the_39") or {}
    if t.get("count") != 39 or t.get("accrual_class") != 31 or t.get("unclassed") != 8 or not str(t.get("statement") or "").strip():
        fail("the_39 must state 39 = 31 accrual-class + 8 unclassed, with its statement")
    hits = long_digit_runs(r)
    if hits:
        fail("the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: %d flow-bearing day(s) over %d account(s); %d deposit day(s): same day %d, next trading day %d, later %d, never in the window %d, not determinable %d"
          % (r["flow_bearing_days"], r["accounts"], r["deposit_days"], c["same_day"], c["next_trading_day"], c["later"], c["never_in_window"], c["not_determinable"]))
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
