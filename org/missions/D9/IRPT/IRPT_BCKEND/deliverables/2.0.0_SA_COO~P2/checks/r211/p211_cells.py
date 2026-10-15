"""IRPT_BCKEND workstream ~PD round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: the split-adjusted holdings price return (CTO ruling @9913bf3ed4, msg 8251).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB211-1  IB-pr-572  where the producer's price return is computed, where the custodian's STK STOCK SPLIT rows live per firm, the measured split ratios, and the served DELTA the fix would move
    AC1  the producer read in the code (the price contribution line, the pure core, the partition loader, the declaration): every file and line verified at HEAD
    AC2  the custodian split rows per firm: columns, rows, split days (trading days), security-days measurable or SPLIT_RATIO_ABSENT, the ratio against the close-price ratio; the 2026-04-21 day found
    AC3  the design inputs and the served DELTA projection (account-days per firm), the reason codes, notes, the six counters 0, no long digit run (no CUSIP, no id)
"""
import datetime as dt
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~415/IB211-1_split_adjust_read.json"
FIRMS = ("49financial", "cottonwood", "inflection")
CLAIMS = ("measured", "inferred", "absent")
COLS = ("tran_srcde", "tr_cd", "sb_cd")
fail, load, is_int, counters, no_long_digits = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits


def text(x, n, what):
    if not isinstance(x, str) or len(x) < n:
        fail("%s must be stated (%d+ characters)" % (what, n))


def iso(x, what):
    if not isinstance(x, str) or not re.fullmatch(r"\d{4}-\d\d-\d\d", x):
        fail("%s must be an ISO date" % what)
    try:
        return dt.date.fromisoformat(x)
    except ValueError:
        fail("%s is not a real date" % what)


def calendar():
    f = P6.ROOT / "lib" / "trading_calendar.py"
    if not f.is_file():
        fail("no lib/trading_calendar.py in the tree")
    spec = importlib.util.spec_from_file_location("tcal_p211", str(f))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def site(s, what):
    if not isinstance(s, dict) or not isinstance(s.get("file"), str) or not is_int(s.get("line")) or not isinstance(s.get("identifier"), str) or not s["identifier"]:
        fail("%s: needs file, line and the identifier on that line" % what)
    f = P6.ROOT / s["file"]
    if not f.is_file():
        fail("%s: %s is not in the tree" % (what, s["file"]))
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    if not 1 <= s["line"] <= len(lines) or s["identifier"] not in lines[s["line"] - 1]:
        fail("%s: line %s of %s does not hold %r" % (what, s["line"], s["file"], s["identifier"]))


def c1():
    r = load(REC)
    if not re.fullmatch(r"[0-9a-f]{40}", str(r.get("base_commit", ""))):
        fail("base_commit must be a 40-hex commit")
    iso(r.get("read_date"), "read_date")
    pr = r.get("producer") or {}
    for k in ("contribution_site", "pure_core_site", "partition_loader_site", "declaration_site"):
        site(pr.get(k), "producer." + k)
    if "holdings_return" not in pr["pure_core_site"]["identifier"]:
        fail("producer.pure_core_site must be the holdings_return definition")
    text(pr.get("quantity_basis_statement"), 60, "producer.quantity_basis_statement (how the price contribution uses the t-1 and day-t prices today)")
    print("OK: the producer read in the code, every site verified at HEAD")


def c2():
    r = load(REC)
    cal = calendar()
    sp = r.get("split_source")
    if not isinstance(sp, dict) or sorted(sp) != sorted(FIRMS):
        fail("split_source must hold %s" % ", ".join(FIRMS))
    found_apr21 = False
    for firm, s in sp.items():
        if not isinstance(s.get("source_found"), bool):
            fail("%s: source_found must be a boolean" % firm)
        text(s.get("source_description"), 30, firm + ".source_description (where the custodian transaction rows are read from; the declaration entry, never a bucket name)")
        if s["source_found"]:
            if sorted(s.get("columns_present") or []) != sorted(COLS):
                fail("%s: columns_present must be exactly %s" % (firm, ", ".join(COLS)))
            days = s.get("split_days")
            if not isinstance(days, list) or days != sorted(set(days)):
                fail("%s: split_days must be a sorted unique list" % firm)
            for x in days:
                if not cal.is_trading_day(iso(x, firm + " split day")):
                    fail("%s: split day %s is not a trading day" % (firm, x))
            found_apr21 = found_apr21 or "2026-04-21" in days
            for k in ("split_rows", "split_security_days", "measurable", "ratio_absent", "ratio_agrees_with_close", "ratio_disagrees_with_close"):
                if not is_int(s.get(k)) or s[k] < 0:
                    fail("%s.%s must be a count" % (firm, k))
            if s["measurable"] + s["ratio_absent"] != s["split_security_days"]:
                fail("%s: measurable + ratio_absent must equal split_security_days" % firm)
            if s["ratio_agrees_with_close"] + s["ratio_disagrees_with_close"] != s["measurable"]:
                fail("%s: ratio_agrees_with_close + ratio_disagrees_with_close must equal measurable" % firm)
            if s["split_security_days"] < len(days) and len(days) > 0:
                fail("%s: split_security_days cannot be below the number of split days" % firm)
        else:
            if s.get("claim") not in CLAIMS or s["claim"] == "measured":
                fail("%s: a source not found carries claim inferred or absent, not measured" % firm)
    if not found_apr21:
        fail("the 2026-04-21 split day (the VUG row) must appear in at least one firm's split_days")
    k = r.get("known_cusips_found_on_2026_04_21")
    if not is_int(k) or not 0 <= k <= 4:
        fail("known_cusips_found_on_2026_04_21 must be a count from 0 to 4 (the ruling names four CUSIPs; none is listed here)")
    print("OK: the custodian split rows per firm, the 2026-04-21 day found, ratios against the close")


def c3():
    r = load(REC)
    dp = r.get("delta_projection") or {}
    af = dp.get("account_days_affected")
    if not isinstance(af, dict) or sorted(af) != sorted(FIRMS) or not all(is_int(v) and v >= 0 for v in af.values()):
        fail("delta_projection.account_days_affected must hold a count per firm")
    if dp.get("total_account_days_affected") != sum(af.values()):
        fail("total_account_days_affected must equal the sum over the firms")
    if not is_int(dp.get("graded_disagreed_on_2026_04_21")):
        fail("delta_projection.graded_disagreed_on_2026_04_21 must be a count (the ruling states 920)")
    if dp.get("claim") not in CLAIMS:
        fail("delta_projection needs a claim")
    text(dp.get("statement"), 60, "delta_projection.statement (how the count was derived and what moves)")
    ds = r.get("design") or {}
    text(ds.get("adjustment_formula"), 60, "design.adjustment_formula (the ratio from the same-day STK STOCK SPLIT row and how the price contribution uses it)")
    ni = ds.get("new_inputs")
    if not isinstance(ni, list) or not ni or not all(isinstance(x, str) and len(x) >= 20 for x in ni):
        fail("design.new_inputs needs at least one line of 20+ characters")
    rc = ds.get("reason_codes")
    if not isinstance(rc, list) or "SPLIT_RATIO_ABSENT" not in rc or "SPLIT_UNADJUSTED_COMPARISON" not in rc:
        fail("design.reason_codes must hold SPLIT_RATIO_ABSENT and SPLIT_UNADJUSTED_COMPARISON")
    notes = r.get("notes")
    if not isinstance(notes, list) or len(notes) < 3 or not all(isinstance(x, str) and len(x) >= 30 for x in notes):
        fail("notes: at least three lines of 30+ characters (what each fact rests on, the objects read counted, what was not read)")
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: the design inputs and the DELTA projection (%d account-days), notes, counters 0" % dp["total_account_days_affected"])


CHECKS = {"IB211-1-AC1": c1, "IB211-1-AC2": c2, "IB211-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p211_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
