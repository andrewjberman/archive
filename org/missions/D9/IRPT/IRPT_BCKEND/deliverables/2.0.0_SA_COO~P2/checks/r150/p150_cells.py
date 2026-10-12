"""IRPT_BCKEND round 150 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one BUILD order, nothing served:
  IB150-1  IB-pr-454  the date-basis grading instrument's PRODUCT FORM (PRD v0.35 to v0.43, all signed): one pure module with its
                      tests, and one read-only run of it that returns the three things the CTO writes into the contract: a FIXED
                      window for the repeated-share rule, the count of securities by share of repeated days in tenths, and the
                      seven-security cost (CTO msg 5800).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last. All three FAIL at base (no module).
  IB150-1-AC1  the module's own tests pass, and the issuer's cases run here against it: the repeated-share rule over a FIXED
               trailing window gives the SAME grade for the same security-day whatever the length of the run it is asked in.
  IB150-1-AC2  the seam: the module, run over the real data with the repeated-share rule switched off, reproduces IB-pr-452's
               nine-pair sizing member for member.
  IB150-1-AC3  the three returns are printed and add up, a window is proposed with its reason and its short-history rule, the
               bounds held, and no file outside the module's own tests imports it.
"""
import datetime as dt
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

MOD = "data/assets/scripts/gold/irpt_reporting/date_basis_grading.py"
TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_date_basis_grading.py"
D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~310/"
OUT, READ = D + "IB150-1_product_form_run.json", D + "IB150-1_PRODUCT_FORM_RUN_READ.md"
PRIOR = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~308/IB148-1_nine_pair_sizing.json"
CLAIMS = ("UNGRADEABLE", "ACCT_PRIOR_DATE", "ACCT_OWN_DATE", "NOTHING_TO_GRADE")
TENTHS = ["0.0-0.1", "0.1-0.2", "0.2-0.3", "0.3-0.4", "0.4-0.5", "0.5-0.6", "0.6-0.7", "0.7-0.8", "0.8-0.9", "0.9-1.0"]


def trading_days(root, start, n):
    sys.path.insert(0, str(root / "lib"))
    import trading_calendar as tc
    out, d = [], start
    while len(out) < n:
        if tc.is_trading_day(d):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB150"))
        sys.exit(1)

    if not (root / MOD).is_file():
        fail("no %s" % MOD)
    if cid == "IB150-1-AC1":
        if not (root / TEST).is_file():
            fail("no %s" % TEST)
        r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", str(root / TEST)], cwd=str(root),
                           capture_output=True, text=True, timeout=110)
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        if r.returncode != 0 or " passed" not in tail or "failed" in tail:
            fail("pytest rc=%d: %s" % (r.returncode, tail[:160]))
        sys.path.insert(0, str(root))
        spec = importlib.util.spec_from_file_location("date_basis_grading", str(root / MOD))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        w = m.REPEATED_SHARE_WINDOW
        if not isinstance(w, int) or w < 5:
            fail("REPEATED_SHARE_WINDOW must be an integer count of trading days, 5 or more")
        days = trading_days(root, dt.date(2026, 1, 5), 3 * w + 12)
        # a security that repeats on every day but one in five: mostly repeating in any window
        sticky = {d: 10.0 + (i // 5) * 0.5 for i, d in enumerate(days)}
        # a security that moves every day: never mostly repeating
        lively = {d: 10.0 + i * 0.07 for i, d in enumerate(days)}
        bad = []
        t = days[2 * w + 5]
        for name, bars, want in (("sticky", sticky, False), ("lively", lively, True)):
            long_run = {d: v for d, v in bars.items() if d <= t}
            short_run = {d: v for d, v in bars.items() if days[w + 3] <= d <= t}
            a, b = m.second_witness_grades_security_day(long_run, t), m.second_witness_grades_security_day(short_run, t)
            if a is not b:
                bad.append("%s: the grade differs between a long and a short run (%r, %r)" % (name, a, b))
            if name == "lively" and a is not want:
                bad.append("lively: a security that moves every day must be graded on a moved day, got %r" % (a,))
            if name == "sticky" and a is not False:
                bad.append("sticky: a security repeating on four days in five must not be graded, got %r" % (a,))
        if bad:
            fail("; ".join(bad)[:600])
        print("OK: %s; window %d trading days; the same security-day reads the same grade in a long and a short run" % (tail[:60], w))
    elif cid == "IB150-1-AC2":
        f = root / OUT
        if not f.is_file():
            fail("no %s" % OUT)
        a = json.loads(f.read_text(encoding="utf-8"))
        prior = json.loads((root / PRIOR).read_text(encoding="utf-8"))["sizings"]["nine_pairs_under_both_guard_sentences"]
        s = a.get("seam_rule_off_reproduces_ib_pr_452") or {}
        rd = s.get("read") or {}
        if s.get("reproduces") is not True or rd.get("account_days") != prior["account_days"] \
                or rd.get("freed_and_holding_no_other_ungradeable_kind") != prior["freed_and_holding_no_other_ungradeable_kind"] \
                or (rd.get("serving_rule") or {}).get("accounts_never_served") != prior["serving_rule"]["accounts_never_served"] \
                or (rd.get("serving_rule") or {}).get("blank") != prior["serving_rule"]["blank"]:
            fail("the module with the repeated-share rule off does not reproduce IB-pr-452's nine-pair sizing")
        if s.get("computed_by") != "the product module":
            fail("seam_rule_off_reproduces_ib_pr_452.computed_by must be 'the product module'")
        print("OK: rule off, the product module reads blank %d, never served %d, freed %d: IB-pr-452's" % (
            rd["serving_rule"]["blank"], rd["serving_rule"]["accounts_never_served"], rd["freed_and_holding_no_other_ungradeable_kind"]))
    elif cid == "IB150-1-AC3":
        f = root / OUT
        if not f.is_file():
            fail("no %s" % OUT)
        text = f.read_text(encoding="utf-8")
        a = json.loads(text)
        p = a.get("window_proposed") or {}
        if not isinstance(p.get("trading_days"), int) or not p.get("reason") or not p.get("when_fewer_bars_than_the_window") \
                or not isinstance(p.get("candidates"), list) or len(p["candidates"]) < 3:
            fail("window_proposed needs trading_days, reason, when_fewer_bars_than_the_window and three or more candidates")
        for c in p["candidates"]:
            if not all(isinstance(c.get(k), int) for k in ("trading_days", "securities_taken", "security_days_not_graded", "account_days_no_longer_freed")):
                fail("each candidate window needs trading_days, securities_taken, security_days_not_graded, account_days_no_longer_freed")
        d = a.get("securities_by_share_of_repeated_days") or {}
        if list((d.get("tenths") or {}).keys()) != TENTHS or sum(d["tenths"].values()) != d.get("securities"):
            fail("securities_by_share_of_repeated_days.tenths must carry the ten bins in order, summing to securities")
        if not d.get("over_what") or not d.get("bin_rule_in_words"):
            fail("the distribution must say over what and how a share on a bin edge is placed")
        sz = a.get("sizing_under_the_rule") or {}
        ad, sr = sz.get("account_days") or {}, sz.get("serving_rule") or {}
        if any(not isinstance(ad.get(c), int) for c in CLAIMS) or sum(ad[c] for c in CLAIMS) != ad.get("present") \
                or not all(isinstance(sr.get(x), int) for x in ("eligible", "served", "blank", "accounts_never_served")) or sr["served"] + sr["blank"] != sr["eligible"]:
            fail("sizing_under_the_rule does not add up")
        c7 = a.get("securities_taken_by_the_rule_cost") or {}
        if not isinstance(c7.get("securities"), list) or not all(isinstance(c7.get(k), int) for k in ("account_days_no_longer_freed", "accounts_no_longer_ever_served", "row_days")) \
                or not isinstance(c7.get("the_seven_of_ib_pr_452_all_taken"), bool):
            fail("securities_taken_by_the_rule_cost needs securities, the three cost counts, and the_seven_of_ib_pr_452_all_taken")
        for k in ("claims_regraded_in_product", "classes_admitted_by_this_cell", "served_changes", "other_sources_asked"):
            if a.get(k) != 0:
                fail("%s must be 0" % k)
        if (a.get("fetch") or {}).get("tickers_asked_more_than_once") != 0 or not isinstance(a.get("not_established"), list):
            fail("fetch.tickers_asked_more_than_once must be 0 and not_established stated")
        rd = root / READ
        if not rd.is_file():
            fail("no %s" % READ)
        if re.search(r"(?<![0-9A-Za-z])[0-9]{8}(?![0-9A-Za-z])", text + rd.read_text(encoding="utf-8")):
            fail("an eight-digit token is in the outputs: an account id may not be written")
        hits = []
        for top in ("data", "infra", "lib"):
            for g in (root / top).rglob("*.py"):
                rel = g.relative_to(root).as_posix()
                if rel in (MOD, TEST) or "__pycache__" in rel:
                    continue
                try:
                    if "date_basis_grading" in g.read_text(encoding="utf-8", errors="replace"):
                        hits.append(rel)
                except OSError:
                    continue
        if hits:
            fail("the module is named outside its own test: %s" % ", ".join(hits[:5]))
        print("OK: window proposed %d trading days; %d securities in ten bins; the rule takes %d securities costing %d account-days; nothing served" % (
            p["trading_days"], d["securities"], len(c7["securities"]), c7["account_days_no_longer_freed"]))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
