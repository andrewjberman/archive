"""IRPT_BCKEND round 161 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one READ-ONLY order (CTO msg 6315):
  IB161-1  IB-pr-467  for the INTERIOR and LAST-ROW excluded days of the performance route's reader, per firm and window: the
                      status token; the prior day's ending value as zero, negative or positive; the length of the zero run.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no file).
  IB161-1-AC1  the same eight entry-window cells as IB-pr-464, and in each the accounts with an interior or a last-row excluded
               day reproduce IB-pr-464's counts (interior only + first and interior + last row involved).
  IB161-1-AC2  every interior and last-row excluded DAY is placed in exactly one cell of status token x prior-value class
               (zero, negative, positive, no prior row), summing to the days counted; the zero-run lengths are distributed
               with no remainder over the days whose prior value is zero.
  IB161-1-AC3  the arm said plainly, a control, and the bounds (no invoke, no sign-in, no account written).
"""
import json
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~322/"
OUT, READ = D + "IB161-1_excluded_day_base.json", D + "IB161-1_EXCLUDED_DAY_BASE_READ.md"
PRIOR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~319/IB160-1_reader_excluded_days.json"
PV = ("zero", "negative", "positive", "no_prior_row")


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB161"))
        sys.exit(1)

    f = root / OUT
    if not f.is_file():
        fail("no %s" % OUT)
    a = json.loads(f.read_text(encoding="utf-8"))
    cells = a.get("per_entry_and_window")
    if not isinstance(cells, list) or not cells:
        fail("per_entry_and_window is empty")
    if cid == "IB161-1-AC1":
        prior = {(c["entry"], c["window"]): c for c in json.loads((root / PRIOR).read_text(encoding="utf-8"))["per_entry_and_window"]}
        if {(c.get("entry"), c.get("window")) for c in cells} != set(prior):
            fail("the cells must be the same entry-window pairs as IB-pr-464's (%d)" % len(prior))
        for c in cells:
            p = prior[(c["entry"], c["window"])]["position_of_the_excluded_days"]
            want = p["interior_only"] + p["first_and_interior"] + p["last_day_involved"]
            if c.get("accounts_with_an_interior_or_last_row_excluded_day") != want:
                fail("%s/%s: %r accounts, IB-pr-464 read %d" % (c["entry"], c["window"], c.get("accounts_with_an_interior_or_last_row_excluded_day"), want))
            if not all(isinstance(c.get(k), int) for k in ("interior_days", "last_row_days", "days_counted")) or c["interior_days"] + c["last_row_days"] != c["days_counted"]:
                fail("%s/%s: interior_days + last_row_days must equal days_counted" % (c["entry"], c["window"]))
        print("OK: %d cells reproduce IB-pr-464's accounts; " % len(cells) + "; ".join("%s %s: %d day(s)" % (c["entry"], c["window"], c["days_counted"]) for c in cells))
    elif cid == "IB161-1-AC2":
        for c in cells:
            for part in ("interior", "last_row"):
                t = c.get(part + "_by_status_and_prior_value")
                if not isinstance(t, dict):
                    fail("%s/%s: %s_by_status_and_prior_value" % (c.get("entry"), c.get("window"), part))
                tot = 0
                for tok, row in t.items():
                    if set(row) != set(PV) or any(not isinstance(v, int) or v < 0 for v in row.values()):
                        fail("%s/%s: status %s must carry exactly %s" % (c["entry"], c["window"], tok, PV))
                    tot += sum(row.values())
                if tot != c.get(part + "_days"):
                    fail("%s/%s: the %s table does not sum to its days" % (c["entry"], c["window"], part))
                z = c.get(part + "_zero_run_lengths")
                zero_days = sum(row["zero"] for row in t.values())
                if not isinstance(z, dict) or sum(z.values()) != zero_days:
                    fail("%s/%s: %s_zero_run_lengths must distribute exactly the days whose prior value is zero" % (c["entry"], c["window"], part))
        if not a.get("prior_value_rule_in_words") or not a.get("zero_run_rule_in_words") or not a.get("zero_rule_tolerance"):
            fail("prior_value_rule_in_words, zero_run_rule_in_words and zero_rule_tolerance")
        print("OK: every interior and last-row excluded day is placed by status and prior value; zero runs distributed")
    elif cid == "IB161-1-AC3":
        if a.get("arm") != "READER_CODE_OVER_SERVED_GOLD" or not a.get("arm_in_words") or not (a.get("control") or {}).get("what"):
            fail("arm, arm_in_words and a control")
        for k in ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "values_written"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if not isinstance(a.get("not_established"), list) or not (root / READ).is_file():
            fail("not_established and the read file")
        print("OK: the reader's own code over the served gold; a control; nothing invoked, no account and no value written")
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
