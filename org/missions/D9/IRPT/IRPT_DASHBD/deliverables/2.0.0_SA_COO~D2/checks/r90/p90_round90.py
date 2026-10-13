"""IRPT_DASHBD round 90 (issuer 2.0.0_SA_COO~D2) -- 1.0.0_SA_CTO~DELL2 msg 6986, round-90 analysis section 3 items 2 and 3 (PRD v0.13, decision 11b).

Three LOCAL cells, read-only, no served byte moves, counts and day offsets only in the repo:
  DB-b-168 (~134) BUILD the day-grain read of the 7 UNEXPLAINED segments: one tracked module tieout/tieout_day_read.py with modes plan (offline), pull --go
                  (LIVE, the issuer's, never the worker's; Black Diamond's existing per-account call, daily series, written only to a private folder),
                  analyze (offline) and selftest (offline, synthetic); the worker never calls the vendor.
  DB-b-169 (~136) READ the 7 after the issuer's pull: each day that differs gets a reason from round 89's closed list, the cause is corrected and the window re-closes
                  at 0.35 pp, or its days stay UNEXPLAINED (offset and size); rule file committed before the read.
  DB-b-170 (~135) the 2 no-flow segments by a tracked cell: the same closed list, the accrual correction closes both, the uncorrected control misses both.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
  DB90-1-AC1  ~134/DAY_READ_BUILD.json (see check_build)      DB90-2-AC1  ~136/DAY_READ_7.json (see check_read)      DB90-3-AC1  ~135/NOFLOW_2_REASONS.json (see check_noflow)
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_DASHBD/"
D = PROJ + "deliverables/"
REASONS = ("MISSING_PRICE", "FLOW_ABSENT_ONE_SIDE", "FLOW_ON_NON_TRADING_DAY", "INCOME_OFF_FLOW_DAY", "BD_ACCRUED_INCOME", "UNEXPLAINED")
RUN = re.compile(r"\d{8,}")
HEX64 = re.compile(r"[0-9a-f]{64}")


class Fail(Exception):
    pass


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


def load(root, rel):
    p = root / rel
    if not p.is_file():
        raise Fail("no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def code_ok(root, code, must_be_in=PROJ):
    f = str((code or {}).get("file") or "")
    need(f.startswith(must_be_in) and code.get("tracked") is True and HEX64.fullmatch(str(code.get("sha256") or "")), "code %r" % code)
    need((root / f).is_file() and hashlib.sha256((root / f).read_bytes()).hexdigest() == code["sha256"], "code file missing or its sha256 differs from the record")
    return f


def rule_ok(root, folder, ru, flag):
    rf = root / folder / str(ru.get("file") or "")
    need(str(ru.get("file") or "").strip() and rf.is_file(), "rule.file must name a file in the worker's folder")
    need(hashlib.sha256(rf.read_bytes()).hexdigest() == ru.get("sha256"), "rule.sha256 does not equal the rule file's bytes: the rule changed after it was recorded")
    need(re.fullmatch(r"[0-9a-f]{7,40}", str(ru.get("commit") or "")) and ru.get(flag) is True, "rule.commit and %s true are required" % flag)


def reads_ok(r):
    rd = r.get("reads") or {}
    need(rd.get("secret_reads") == 0 and rd.get("s3_writes") == 0, "reads %r" % rd)
    need(r.get("served_values_changed") is False, "served_values_changed must be false")
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])


def check_build(root):
    folder = D + "0.9.0_WK_IRPT_DASHBD~134"
    r = load(root, folder + "/DAY_READ_BUILD.json")
    need(r.get("tolerance_pp") == 0.35, "tolerance_pp %r" % r.get("tolerance_pp"))
    f = code_ok(root, r.get("code"))
    need(f == PROJ + "tieout/tieout_day_read.py", "code.file must be the tracked tieout/tieout_day_read.py")
    pop = r.get("population") or {}
    need(pop.get("unexplained_segments") == 7 and pop.get("accounts") == 7, "population %r must reproduce the 7 UNEXPLAINED segments in 7 accounts" % pop)
    pl = r.get("plan") or {}
    need(pl.get("requests") == 7 and is_int(pl.get("daily_ranges")) and pl["daily_ranges"] == 7 and pl.get("vendor_calls") == 0 and pl.get("dry_run") == 1, "plan %r" % pl)
    need(HEX64.fullmatch(str(pl.get("plan_sha256") or "")) and pl.get("kept_private") is True, "plan.plan_sha256 and plan.kept_private true are required")
    ru = r.get("runner") or {}
    need(ru.get("modes") == ["plan", "pull", "analyze", "selftest"], "runner.modes %r" % ru.get("modes"))
    for k in ("refuses_without_go", "refuses_second_pull", "writes_only_private", "plan_equals_rebuilt_plan_check"):
        need(ru.get(k) is True, "runner.%s must be true" % k)
    need(ru.get("credential_logged") is False, "runner.credential_logged must be false")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0, "the worker made %r vendor calls" % rd.get("vendor_calls"))
    reads_ok(r)
    mod = root / f
    p = subprocess.run([sys.executable, "-I", str(mod), str(root), "pull"], capture_output=True, text=True, timeout=60)
    need(p.returncode != 0 and "--go" in (p.stdout + p.stderr), "`pull` without --go must refuse (rc %d)" % p.returncode)
    s = subprocess.run([sys.executable, "-I", str(mod), str(root), "selftest"], capture_output=True, text=True, timeout=120)
    need(s.returncode == 0 and "SELFTEST PASS" in s.stdout, "selftest did not print SELFTEST PASS (rc %d)" % s.returncode)
    print("OK: day-read module tracked; plan of %d request(s) over %d daily range(s), 0 vendor calls by the worker; `pull` refuses without --go; selftest passes" % (pl["requests"], pl["daily_ranges"]))


def check_read(root):
    folder = D + "0.9.0_WK_IRPT_DASHBD~136"
    r = load(root, folder + "/DAY_READ_7.json")
    need(r.get("tolerance_pp") == 0.35 and r.get("day_differs_pp") == 0.01, "tolerance_pp 0.35 and day_differs_pp 0.01 are fixed by the order")
    rule_ok(root, folder, r.get("rule") or {}, "written_before_read")
    need(tuple(r.get("reasons_list") or ()) == REASONS, "reasons_list must be the closed list %r" % (REASONS,))
    code_ok(root, r.get("code"))
    pop = r.get("population") or {}
    need(pop.get("accounts") == 7 and pop.get("segments") == 7, "population %r" % pop)
    pr = r.get("pull") or {}
    need(pr.get("requests") == 7 and is_int(pr.get("http_ok")) and pr["http_ok"] <= 7 and is_int(pr.get("http_failed")) and pr["http_ok"] + pr["http_failed"] == 7, "pull %r (the issuer's pull record)" % pr)
    pa = r.get("per_account")
    need(isinstance(pa, list) and len(pa) == 7, "per_account must list the 7 accounts (no ids)")
    closed = unexpl = 0
    for i, a in enumerate(pa):
        need(is_int(a.get("days")) and a["days"] >= 1 and is_int(a.get("days_differing")) and a["days_differing"] <= a["days"], "per_account[%d] days %r" % (i, a))
        br = a.get("by_reason") or {}
        need(all(is_int(br.get(k)) for k in REASONS) and sum(br.values()) == a["days_differing"], "per_account[%d] by_reason %r must be six ints summing to days_differing %d" % (i, br, a["days_differing"]))
        ud = a.get("unexplained_days")
        need(isinstance(ud, list) and len(ud) == br["UNEXPLAINED"] and all(isinstance(x, dict) and is_int(x.get("offset")) and num(x.get("size_pp")) for x in ud),
             "per_account[%d] unexplained_days must be {offset, size_pp} entries equal to the UNEXPLAINED count" % i)
        need(a.get("uncorrected_window_misses") is True, "per_account[%d] negative arm: the uncorrected window must still miss at 0.35 pp" % i)
        need(isinstance(a.get("series_last_equals_stored_window"), bool), "per_account[%d] series_last_equals_stored_window (the control that the daily series reproduces the stored window figure) must be a bool" % i)
        w = a.get("window_closed_after_correction")
        need(isinstance(w, bool), "per_account[%d] window_closed_after_correction" % i)
        need(w == (br["UNEXPLAINED"] == 0), "per_account[%d] a window is closed with reasons exactly when no day is UNEXPLAINED" % i)
        closed += 1 if w else 0
        unexpl += 0 if w else 1
    sm = r.get("summary") or {}
    need(sm.get("accounts_closed_with_reasons") == closed and sm.get("accounts_unexplained") == unexpl, "summary %r, expected closed %d unexplained %d" % (sm, closed, unexpl))
    row = str(r.get("surprise_row") or "").strip()
    need((unexpl > 0) == bool(row), "a surprise_row naming the unexplained is required exactly when an account stays UNEXPLAINED")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls_by_worker") == 0, "the worker made %r vendor calls" % rd.get("vendor_calls_by_worker"))
    reads_ok(r)
    print("OK: 7 accounts read at day grain: %d closed with reasons, %d with UNEXPLAINED days" % (closed, unexpl))


def check_noflow(root):
    folder = D + "0.9.0_WK_IRPT_DASHBD~135"
    r = load(root, folder + "/NOFLOW_2_REASONS.json")
    need(r.get("tolerance_pp") == 0.35, "tolerance_pp %r" % r.get("tolerance_pp"))
    ru = r.get("rule") or {}
    rf = root / (D + "0.9.0_WK_IRPT_DASHBD~133/RULE.md")
    need(ru.get("file") == D + "0.9.0_WK_IRPT_DASHBD~133/RULE.md" and ru.get("reused_unchanged") is True and rf.is_file()
         and hashlib.sha256(rf.read_bytes()).hexdigest() == ru.get("sha256") == "fc50363af10dfad3d0088a4220c68132b8a02c41859941e8ab30c7be53361f55",
         "rule must be round 89's RULE.md, reused unchanged (sha256 fc50363a...)")
    need(tuple(r.get("reasons_list") or ()) == REASONS, "reasons_list must be the closed list")
    f = code_ok(root, r.get("code"))
    need(f == PROJ + "tieout/tieout_noflow_reasons.py", "code.file must be the tracked tieout/tieout_noflow_reasons.py")
    pop = r.get("population") or {}
    need(pop.get("segments") == 90 and pop.get("accounts") == 86 and pop.get("no_flow_segments") == 2 and pop.get("flow_segments") == 88, "population %r must reproduce 90 segments, 86 accounts, 2 without a flow day" % pop)
    br = r.get("by_reason") or {}
    need(all(is_int(br.get(k)) for k in REASONS) and sum(br.values()) == 2, "by_reason %r must be six ints summing to 2" % br)
    ev = r.get("evidence") or {}
    for k in REASONS[:-1]:
        if br[k] > 0:
            e = ev.get(k) or {}
            v = e.get("values")
            need(e.get("kind") in ("count", "day_offsets") and isinstance(v, list) and v and all(isinstance(x, int) and not isinstance(x, bool) for x in v), "evidence for %s must be a count or day offsets, ints" % k)
    co = r.get("corrected") or {}
    reasoned = 2 - br["UNEXPLAINED"]
    need(co.get("reasoned") == reasoned and co.get("closed_within_tolerance") == reasoned, "corrected %r: every reasoned segment must close within 0.35 pp when its cause is corrected" % co)
    need(r.get("uncorrected_closes_among_2") == 0, "uncorrected_closes_among_2 %r: the control must miss both" % r.get("uncorrected_closes_among_2"))
    need(br["BD_ACCRUED_INCOME"] == 2, "by_reason %r: the order's expectation is BD_ACCRUED_INCOME 2; any other result is NOT this criterion's to pass (file a row)" % br)
    reads_ok(r)
    print("OK: 2 no-flow segments of 90 over 86 accounts: BD_ACCRUED_INCOME %d, UNEXPLAINED %d; both uncorrected miss, both re-close at 0.35 pp" % (br["BD_ACCRUED_INCOME"], br["UNEXPLAINED"]))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    fn = {"DB90-1-AC1": check_build, "DB90-2-AC1": check_read, "DB90-3-AC1": check_noflow}.get(cid)
    try:
        need(fn is not None, "unknown criterion %r" % cid)
        fn(root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB90"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
