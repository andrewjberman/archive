"""IRPT_BCKEND round 193 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of three orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB193-1  IB-pr-535  the holdings-producer release APPLIED under the signed pair IB-pr-532 (three bundle mints), per-firm rules
    AC1  the gates: the packet's sha256, both halves signed, the blob at the pin, the per-firm re-measure equal to the packet (Inflection on its own pin), Branch B re-read, the digest gate
    AC2  the act: the window, the releasing seat's ledger, the three mints, the per-firm business date stated before the fire
    AC3  the after-read per firm at the first fire (T-1 stamp, or a named hold with the frontier unchanged), the gap and the bound counters
  IB193-2  IB-pr-536  the one-date bypass of the publish gate for 49financial, with the landed-date-equals-as_of assertion (offline build)
    AC1  the new tests and the existing gate tests pass
    AC2  the difference control: with the assertion block removed from a COPY the new tests FAIL
    AC3  the record, the diff bounded to the producer file and its test, the scheduled path unchanged
  IB193-3  IB-pr-537  the cause of the 2026-10-09 kill read from the host's own record (OOM, not, or unreadable)
    AC1  the verdict, its basis and reads; the release memory-read flag follows the verdict
    AC2  the host commands: at most two, each read-only by an allowlist
    AC3  no identifier, notes, and the bound counters 0
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
APPLY_REC = D + "0.7.0_AE_CloudOps~IB2/IB193-1_apply_record.json"
KILL_REC = D + "0.7.0_AE_CloudOps~IB2/IB193-3_kill_cause.json"
BUILD_REC = D + "0.9.0_WK_IRPT_BCKEND~382/IB193-2_record.json"
PKG = "data/assets/scripts/gold/investor_reporting/"
SNAP = PKG + "holdings_snapshot.py"
TEST_NEW = PKG + "tests/test_holdings_bypass_one_date.py"
TEST_OLD = PKG + "tests/test_holdings_publish_gate.py"
PACKET_SHA = "4129abf31f3d402d72de9778c0cc32d7114fd414105cc24ac169893696e28504"
BLOB = "3a19dcf5912798f7d94e9756ae04f64dd2ce7ea0"
PACKET_NUMBERS = {"49financial": (32, 0, "PUBLISHED", "PUBLISHED", 0), "cottonwood": (38, 211, "REFUSED", "PUBLISHED", 1), "inflection": (774, 67, "PUBLISHED", "PUBLISHED", 0)}
PINS = {"49financial": "2026-10-12", "cottonwood": "2026-10-12", "inflection": "2026-10-13"}
BUNDLES = {"49financial": "irpt_holdings_49f", "cottonwood": "irpt_holdings_cot", "inflection": "irpt_holdings_inf"}
BRANCH_B_BUNDLE = {"49financial": "UHOCIkWj3QiIzNucG1VjNnk_AufIg6oD", "cottonwood": "oyIYMVdh_l2zCg5ZWvn3ISPPS6_9Q82_", "inflection": "PzhCs97qVBXkZcIjaOklHmzWiFsOFafM"}
BRANCH_B_MANIFEST = {"49financial": "daFZJt6f7G9.CXj3MJftFYV.DNUOVFQh", "cottonwood": "lQMhNnImgj0ikICMdhFeasBGJKSbl55s", "inflection": "MLSPlfHHsZa7mSnXEzorRkR9zgs2Q68u"}
FIRMS = list(PACKET_NUMBERS)
APPLY_COUNTERS = {"bundles_minted": 3, "other_bucket_writes": 0, "lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "backfills": 0, "files_deleted": 0, "markers_closed": 0}
KILL_COUNTERS = ("functions_invoked", "aws_writes_made", "files_deleted", "service_restarts", "host_state_changes")
READ_ONLY = re.compile(r"^\s*(journalctl|dmesg|grep|cat|free|uptime|ps|ls|zgrep|zcat)\b")
HOST_DANGER = re.compile(r"[;&`>]|\$\(|\b(rm|kill|pkill|systemctl|service|reboot|shutdown|tee|dd|mv|cp|chmod|chown|sudo|curl|wget|pip|apt|yum)\b|\|\s*(sh|bash)\b")
ALLOWED_BUILD_PREFIX = (D + "0.9.0_WK_IRPT_BCKEND~382/", "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md")
ALLOWED_BUILD_FILES = {SNAP, TEST_NEW}
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB193"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_date(x):
    return isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) is not None


def is_ts(x):
    return isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", x) is not None


def no_long_digits(txt):
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", txt):
        fail("a long digit run (an identifier or a figure) is present")


def ts(x):
    import datetime as dt
    return dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")


def prev_trading_day(date):
    sys.path.insert(0, str(ROOT / "lib"))
    import importlib
    tc = importlib.import_module("trading_calendar")
    import datetime as dt
    d = tc.prev_trading_day(dt.date.fromisoformat(date))
    return d.isoformat() if hasattr(d, "isoformat") else str(d)


# ----------------------------------------------------------------------------- IB193-1
def apply_ac1():
    r = load(APPLY_REC)
    g = r.get("gates") or {}
    if g.get("packet_sha256") != PACKET_SHA:
        fail("gates.packet_sha256 is not the signed packet's")
    if g.get("coo_half_signed") is not True or g.get("cto_half_signed") is not True:
        fail("both halves must read signed at the packet bytes")
    if g.get("holdings_snapshot_blob") != BLOB:
        fail("the blob of holdings_snapshot.py at the release is not the pin's %s" % BLOB)
    rm = r.get("remeasure") or {}
    if rm.get("pins") != PINS:
        fail("the re-measure pins must be %r (each firm on the custody partition its packet row used)" % PINS)
    for firm, (can, fb, gb, ga, listed) in PACKET_NUMBERS.items():
        v = (rm.get("firms") or {}).get(firm) or fail("no re-measure for %s" % firm)
        got = (v.get("movers_canonical"), v.get("movers_fallback"), v.get("gate_before"), v.get("gate_after"), v.get("lost_accounts_listed_after"))
        if got != (can, fb, gb, ga, listed):
            fail("%s re-measure %r differs from the packet %r: the release stops" % (firm, got, (can, fb, gb, ga, listed)))
        if v.get("matches_packet") is not True:
            fail("%s matches_packet must be true" % firm)
    bb = r.get("branch_b_reread") or {}
    for firm in FIRMS:
        v = bb.get(firm) or fail("no branch_b_reread for %s" % firm)
        if v.get("bundle_version_id") != BRANCH_B_BUNDLE[firm] or v.get("manifest_version_id") != BRANCH_B_MANIFEST[firm]:
            fail("%s Branch B versions differ from the packet's: the release stops" % firm)
        # AMENDMENT 1 (CTO ruling msg 7650): the manifest version at mint is the recorded page anchor. A version newer than
        # the packet's is admitted only if it is the only newer one, was written by that firm's scheduled fire, and its
        # published date is T-1 of that fire by the trading calendar.
        a = v.get("manifest_anchor_at_mint") or fail("%s: no manifest_anchor_at_mint" % firm)
        if not a.get("version_id"):
            fail("%s: the anchor needs a version id" % firm)
        if a["version_id"] == BRANCH_B_MANIFEST[firm]:
            if a.get("newer_versions") != 0:
                fail("%s: the anchor equals the packet's but newer versions are claimed" % firm)
        else:
            if a.get("newer_versions") != 1 or a.get("written_by_scheduled_fire") is not True:
                fail("%s: a newer manifest version must be the only one and written by the scheduled fire: a STOP" % firm)
            fd = a.get("fire_date")
            if not is_date(fd) or a.get("published_date") != prev_trading_day(fd):
                fail("%s: the newer manifest's published date must be T-1 of its fire by the calendar: a STOP" % firm)
    dg = r.get("digest_gate") or {}
    for firm in FIRMS:
        ch = (dg.get(firm) or fail("no digest_gate for %s" % firm)).get("changed_members")
        if not isinstance(ch, list) or "holdings_snapshot.py" not in ch or not set(ch) <= {"holdings_snapshot.py", "SHA256SUMS"}:
            fail("%s changed members %r must be holdings_snapshot.py (and SHA256SUMS) only" % (firm, ch))
    if r.get("stop") is not None:
        fail("a STOP is recorded: the criteria are not run on a stopped release")
    print("OK: gates, re-measure on per-firm pins, Branch B, digest gate")


def apply_ac2():
    r = load(APPLY_REC)
    w = r.get("window") or {}
    for k in ("last_fire_all_success_utc", "mint_start_utc", "mint_end_utc", "next_fire_utc"):
        if not is_ts(w.get(k)):
            fail("window.%s must be a UTC timestamp" % k)
    a, b, c, n = (ts(w[k]) for k in ("last_fire_all_success_utc", "mint_start_utc", "mint_end_utc", "next_fire_utc"))
    if not (a < b <= c < n):
        fail("the mints must start after the day's fires read Success and end before the next fire")
    if (n - c).total_seconds() < 1800:
        fail("nothing is minted within 30 minutes before a fire")
    if (c - b).total_seconds() > 3600:
        fail("the three mints must be made inside one session (one hour)")
    if not re.fullmatch(r"\d\d:15:00Z", w["next_fire_utc"][11:]) or w["next_fire_utc"][11:13] not in ("14", "15"):
        fail("next_fire_utc must be a 10:15 ET fire (14:15Z or 15:15Z)")
    led = r.get("ledger") or {}
    ent = led.get("entry", "")
    if not ent.startswith("org/critical_paths/change_management/") or not (ROOT / ent).is_file():
        fail("the ledger entry must exist under org/critical_paths/change_management/")
    if led.get("legs") != 4 or led.get("opened_before_first_mint") is not True:
        fail("the ledger must name the four legs and be opened before the first mint")
    mints = r.get("mints") or {}
    for firm in FIRMS:
        m = mints.get(firm) or fail("no mint for %s" % firm)
        if m.get("bundle") != BUNDLES[firm]:
            fail("%s mint is not %s" % (firm, BUNDLES[firm]))
        if not m.get("after_version_id") or m.get("after_version_id") == m.get("before_version_id") or m.get("before_version_id") != BRANCH_B_BUNDLE[firm]:
            fail("%s mint must move the bundle off the packet's Branch B version" % firm)
        if m.get("after_sha256_equals_built") is not True:
            fail("%s landed bytes must equal the built bundle" % firm)
    bd = r.get("business_date_statement") or {}
    if not (is_ts(bd.get("stated_at_utc")) and ts(bd["stated_at_utc"]) < n):
        fail("the per-firm business date must be stated before the fire")
    fd = bd.get("fire_date")
    if not is_date(fd) or bd.get("t_minus_1") != prev_trading_day(fd):
        fail("t_minus_1 must be the calendar's previous trading day of the fire date")
    if set((bd.get("per_firm_expected") or {})) != set(FIRMS):
        fail("a business date is stated for each of the three firms")
    print("OK: window, ledger, three mints, business date stated")


def apply_ac3():
    r = load(APPLY_REC)
    bd = r.get("business_date_statement") or {}
    t1 = bd.get("t_minus_1")
    ar = r.get("after_read") or {}
    for firm in FIRMS:
        v = ar.get(firm) or fail("no after_read for %s" % firm)
        o = v.get("outcome")
        if o == "STAMPED_T_MINUS_1":
            if v.get("stamp") != t1 or v.get("t1_partition_under_it") is not True:
                fail("%s stamped %r, not T-1 %r, or no T-1 partition under it: a STOP" % (firm, v.get("stamp"), t1))
        elif o == "HELD_NO_NEW_PUBLICATION":
            if not v.get("absent_partition_named") or v.get("frontier_unchanged") is not True or v.get("served_latest_date_after") != v.get("served_latest_date_before"):
                fail("%s hold needs the absent T-1 partition named and the served frontier unchanged" % firm)
        else:
            fail("%s outcome %r is neither a T-1 stamp nor a named hold" % (firm, o))
    cw = ar["cottonwood"]
    if cw["outcome"] == "STAMPED_T_MINUS_1" and cw.get("lost_accounts_listed") != 1:
        fail("a stamped Cottonwood must list its one lost account")
    if r.get("rule_after_read", {}).get("cash_sub_read_cash") is not True and any(ar[f]["outcome"] == "STAMPED_T_MINUS_1" for f in FIRMS):
        fail("a published firm must read its Cash-sub holdings as Cash")
    if (r.get("gap_2026_10_08") or {}).get("unchanged") is not True:
        fail("the 49financial 2026-10-08 gap must read unchanged")
    kr = r.get("kill_cause_memory_read") or {}
    if kr.get("required_by_verdict") is True and kr.get("memory_read_done") is not True:
        fail("an OOM verdict requires the fire's memory read")
    if r.get("rollback_performed") is not False:
        fail("rollback_performed must be false (a rollback is a STOP)")
    c = r.get("counters") or {}
    for k, want in APPLY_COUNTERS.items():
        if c.get(k) != want:
            fail("counter %s must read %r, reads %r" % (k, want, c.get(k)))
    no_long_digits(json.dumps(r))
    print("OK: per-firm after-read, gap, counters")


# ----------------------------------------------------------------------------- IB193-2
def run_pytest(cwd, files, extra=()):
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", *extra, *files], cwd=str(cwd),
                       capture_output=True, text=True, timeout=110)
    return p.returncode, p.stdout + p.stderr


def build_ac1():
    for rel in (SNAP, TEST_NEW, TEST_OLD):
        if not (ROOT / rel).is_file():
            fail("no %s" % rel)
    rc, out = run_pytest(ROOT, [TEST_NEW, TEST_OLD])
    m = re.search(r"(\d+) passed", out)
    if rc != 0 or not m:
        fail("the tests do not all pass:\n" + out[-600:])
    if (ROOT / TEST_NEW).read_text(encoding="utf-8").count("def test_") < 8:
        fail("the new test file must hold at least eight tests")
    print("OK: %s passed" % m.group(1))


def build_ac2():
    src = (ROOT / SNAP).read_text(encoding="utf-8")
    blocks = re.findall(r"^[ \t]*# BEGIN ONE-DATE-ASSERT.*?^[ \t]*# END ONE-DATE-ASSERT[^\n]*\n", src, re.S | re.M)
    if len(blocks) != 1:
        fail("holdings_snapshot.py must hold exactly one BEGIN/END ONE-DATE-ASSERT block, holds %d" % len(blocks))
    with tempfile.TemporaryDirectory() as td:
        cp = Path(td) / "investor_reporting"
        shutil.copytree(ROOT / PKG, cp, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        mutated = src.replace(blocks[0], "")
        (cp / "holdings_snapshot.py").write_text(mutated, encoding="utf-8")
        rc, out = run_pytest(cp, ["tests/test_holdings_bypass_one_date.py"])
    if rc == 0:
        fail("the new tests still pass with the assertion removed: the tests cannot discriminate")
    if not re.search(r"\d+ failed", out):
        fail("the mutant run did not fail on a test (rc %s):\n%s" % (rc, out[-500:]))
    print("OK: removing the assertion block fails the new tests")


def build_ac3():
    r = load(BUILD_REC)
    base = r.get("base_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("base_commit must be 40 hex")
    p = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", base, "HEAD"], capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        fail("git diff failed: " + p.stderr.strip()[:200])
    changed = sorted(x for x in p.stdout.split("\n") if x and not x.startswith(ALLOWED_BUILD_PREFIX))
    if sorted(r.get("changed_paths", [])) != changed:
        fail("changed_paths (the product paths) differs from the git diff since base, deliverables and the channel aside")
    stray = [c for c in changed if c not in ALLOWED_BUILD_FILES]
    if stray:
        fail("paths outside the grant: %r" % stray[:4])
    if SNAP not in changed or TEST_NEW not in changed:
        fail("the producer file and the new test must both change")
    if r.get("default_path_unchanged") is not True or not is_int(r.get("tests_total")) or r.get("tests_passed") != r.get("tests_total"):
        fail("default_path_unchanged true and all tests passed must be recorded")
    if not is_int(r.get("mutant_tests_failed")) or r["mutant_tests_failed"] < 1:
        fail("mutant_tests_failed must be at least 1")
    need = {"no_upload", "wrong_firm", "no_as_of", "as_of_differs_from_allowed_date", "landed_date_differs", "qa"}
    if not need <= set(r.get("refusals_tested", [])):
        fail("refusals_tested must cover %r" % sorted(need))
    notes = r.get("notes")
    if not isinstance(notes, list) or not notes:
        fail("notes are required")
    no_long_digits(json.dumps(r))
    print("OK: record, diff bounded, default path unchanged")


# ----------------------------------------------------------------------------- IB193-3
def kill_ac1():
    r = load(KILL_REC)
    f = r.get("fire") or {}
    if f.get("fire_date") != "2026-10-09" or f.get("response_code") != 137:
        fail("fire must be the 2026-10-09 fire with response code 137")
    v = r.get("verdict")
    if v not in ("OOM", "NOT_OOM", "UNREADABLE"):
        fail("verdict must be OOM, NOT_OOM or UNREADABLE")
    if not isinstance(r.get("verdict_basis"), str) or len(r["verdict_basis"]) < 40:
        fail("a verdict basis of one real line is required")
    rd = r.get("reads")
    if not isinstance(rd, list) or not rd or not all(isinstance(x, dict) and x.get("source") and x.get("result") for x in rd):
        fail("reads: each needs a source and a result")
    if r.get("memory_read_for_release_fire") is not (v == "OOM"):
        fail("memory_read_for_release_fire must be true exactly when the verdict is OOM")
    print("OK: verdict %s" % v)


def kill_ac2():
    r = load(KILL_REC)
    hc = r.get("host_commands")
    if not isinstance(hc, list) or len(hc) > 2 or r.get("host_commands_sent") != len(hc):
        fail("at most two host commands, and host_commands_sent must equal the list")
    for c in hc:
        cmd = c.get("command", "") if isinstance(c, dict) else ""
        if not READ_ONLY.match(cmd) or HOST_DANGER.search(cmd) or c.get("read_only") is not True:
            fail("host command not read-only by the allowlist: %r" % cmd[:80])
    print("OK: %d host command(s), all read-only" % len(hc))


def kill_ac3():
    r = load(KILL_REC)
    no_long_digits(json.dumps(r))
    if not isinstance(r.get("notes"), list) or not r["notes"]:
        fail("notes are required")
    for k in KILL_COUNTERS:
        if r.get(k) != 0:
            fail("counter %s must read 0, reads %r" % (k, r.get(k)))
    print("OK: notes and counters")


CHECKS = {
    "IB193-1-AC1": apply_ac1, "IB193-1-AC2": apply_ac2, "IB193-1-AC3": apply_ac3,
    "IB193-2-AC1": build_ac1, "IB193-2-AC2": build_ac2, "IB193-2-AC3": build_ac3,
    "IB193-3-AC1": kill_ac1, "IB193-3-AC2": kill_ac2, "IB193-3-AC3": kill_ac3,
}


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p193_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT = Path(sys.argv[1])
    CID = sys.argv[2]
    CHECKS[CID]()
    print("%s PASS" % CID)
