"""IRPT_DASHBD round 150, workstream LATEWIN (issuer 2.0.0_SA_COO~D2) -- DB-b-333, the Cottonwood LATE-POSTING READER (CTO rulings after dell1's finding, msg 7612, and the late-posting window ruling): the account-return
derivation summed fact_transactions rows from EVERY partition on or after the day, and the silver partitions are rolling pulls that repeat each trade, so the landed gold external flows are inflated 8 to 13 times.
The fix, in the adapter and the handler of irpt-cot-account-return-daily-lambda: read the partitions from the window's first day through the 14th trading day after its last day, count each TransactionID ONCE (the later
partition's copy replaces an earlier one), treat a day whose own partition is absent as present when rows dated that day exist in that window, and make each scheduled fire ALSO rewrite, through the existing rewrite
path, the landed day 14 trading days before each day it owes. The code is a worker's, in a workspace worktree; nothing is deployed by this cell (the release is a later signed pair, folded with ~F2's stage).

  DBC199-1-AC1  the diff and the source: only the adapter, the handler and test files changed since the worker's branch point, within the line caps; the adapter reads TransactionID and the handler has a settle
  DBC199-2-AC1  the behaviour: the worker's own test file passes and the issuer's probe (copied into the tests directory by the checker, run, deleted) passes against the worker's code
  DBC199-3-AC1  the proof: the existing adapter, rewrite and handler suites pass, ruff is clean, and a LIVE read-only derivation of 2026-07-24 against today's silver equals an independent deduplicated sum while the raw sum differs

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <repo_root_of_the_reference>
"""
import difflib
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ADAPTER = "data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py"
HANDLER = "infra/aws/lambda/investor-reporting/account-return-daily/handler.py"
TESTS_A = "data/assets/scripts/gold/irpt_reporting/tests/"
TESTS_H = "infra/aws/lambda/investor-reporting/account-return-daily/tests/"
EXISTING_TESTS = (TESTS_A + "test_cottonwood_bd_account_return_daily.py", TESTS_A + "test_cottonwood_rewrite.py", TESTS_H + "test_handler.py", TESTS_H + "test_transaction_emission.py")
NEW_TEST_PREFIX = "test_cottonwood_late_window"
PROBE_SRC = HERE / "p199_probe_late_window.py"
PROBE_DST = TESTS_A + "test_p199_probe.py"
OWN = ("org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.7.0_AE_CloudOps~", "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~",
       "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-333")
CAP_ADAPTER, CAP_HANDLER = 150, 120
LIVE_DAY, LIVE_DISTINCT_IDS = "2026-07-24", 277


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def run(cmd, cwd, timeout=900):
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)


def git(root, *a):
    r = run(["git", "-C", str(root)] + list(a), root)
    return r.stdout, r.returncode


def lines_changed(root, base, rel):
    old, rc = git(root, "show", "%s:%s" % (base, rel))
    need(rc == 0, "cannot read %s at %s" % (rel, base[:10]))
    new = (Path(root) / rel).read_bytes().decode("utf-8")
    need("\r" not in new, "%s must keep LF line endings" % rel)
    d = list(difflib.unified_diff(old.splitlines(), new.splitlines(), lineterm="", n=0))
    return sum(1 for x in d if x.startswith(("+", "-")) and not x.startswith(("+++", "---")))


def check_diff(root, git_scope=True):
    root = Path(root)
    if git_scope:
        base, rc = git(root, "merge-base", "HEAD", "box/dell2")
        need(rc == 0 and base.strip(), "no merge-base of HEAD and box/dell2")
        base = base.strip()
        out, rc = git(root, "diff", "--name-only", base)
        need(rc == 0, "cannot diff against the branch point %s" % base[:10])
        untracked, _ = git(root, "ls-files", "--others", "--exclude-standard")
        # the portal gitlink of a provisioned worktree is not the worker's edit (the provisioner points it at the portal worktree)
        changed = {x for x in (out + untracked).splitlines() if x.strip() and x.strip() != "portal"}
        allowed = lambda f: f in (ADAPTER, HANDLER) or f in EXISTING_TESTS or f.startswith(OWN) or (  # noqa: E731
            (f.startswith(TESTS_A) or f.startswith(TESTS_H)) and f.rsplit("/", 1)[-1].startswith(NEW_TEST_PREFIX))
        extra = [f for f in changed if not allowed(f)]
        need(not extra, "files outside the agreed set changed: %s" % extra[:4])
        need(ADAPTER in changed and HANDLER in changed, "the adapter and the handler must both be in the diff")
        need(any(f.rsplit("/", 1)[-1].startswith(NEW_TEST_PREFIX) for f in changed), "a test file named %s* must be in the diff" % NEW_TEST_PREFIX)
        need(lines_changed(root, base, ADAPTER) <= CAP_ADAPTER, "the adapter may change by at most %d lines" % CAP_ADAPTER)
        need(lines_changed(root, base, HANDLER) <= CAP_HANDLER, "the handler may change by at most %d lines" % CAP_HANDLER)
    a = (root / ADAPTER).read_bytes().decode("utf-8")
    h = (root / HANDLER).read_bytes().decode("utf-8")
    need("TransactionID" in a, "the adapter must read the TransactionID column (the dedup key)")
    need(re.search(r"\bsettle", h) is not None and "rewrite=True" in h, "the handler must settle a day through the existing rewrite path (rewrite=True)")
    need(not re.search(r"\bprint\([^)]*(AccountID|account_id)\b", a + h), "no account id may be printed")
    return True


def pytest_run(root, files, label, timeout=1200):
    r = run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + files, root, timeout)
    out = re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)
    need(r.returncode == 0, "%s failed: %s" % (label, out[-700:].replace("\n", " | ")))
    need(re.search(r"\b[1-9]\d* passed", out) is not None, "%s printed no pass count" % label)
    return out


def check_behaviour(root, require_own_tests=True):
    root = Path(root)
    own = sorted(f for d in (TESTS_A, TESTS_H) for f in (root / d).glob(NEW_TEST_PREFIX + "*.py"))
    if require_own_tests:
        need(own, "no test file named %s* under the tests directories" % NEW_TEST_PREFIX)
        low = " ".join(f.read_text(encoding="utf-8") for f in own).lower()
        for word in ("transactionid", "dedup", "settle"):
            need(word in low, "the cell's tests do not speak of %s" % word)
        pytest_run(root, [str(f.relative_to(root)).replace("\\", "/") for f in own], "the cell's tests")
    dst = root / PROBE_DST
    shutil.copyfile(PROBE_SRC, dst)
    try:
        pytest_run(root, [PROBE_DST], "the issuer's probe", 600)
    finally:
        if dst.exists():
            dst.unlink()
    return True


def load_adapter(root):
    sys.path.insert(0, str(Path(root) / "lib"))
    spec = importlib.util.spec_from_file_location("cbd_p199_live", str(Path(root) / ADAPTER))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check_live(root):
    """Read-only against S3: the worker's derive of LIVE_DAY equals an independent TransactionID-deduplicated sum; the raw sum differs (the control)."""
    import datetime as dt
    import boto3
    root = Path(root)
    cbd = load_adapter(root)
    tc = sys.modules["trading_calendar"]
    rd = cbd.CottonwoodBlackDiamondSilverReader(boto3.client("s3", region_name="us-east-1"))
    prev = tc.prev_trading_day(dt.date.fromisoformat(LIVE_DAY)).isoformat()
    rows, _summary = cbd.derive(rd, cbd.accounts_in_partition(rd, LIVE_DAY), prev, LIVE_DAY, floor_day="2026-07-10")
    # an account-day the method could not reconcile (a flow word on an unplaced type or a null value) carries no flow by design: it is left out of the comparison
    derived = {r["account_id"]: (r["external_flow"] or 0.0) for r in rows if r["business_date"] == LIVE_DAY and r["day_quality"] != cbd.DAY_FLOW_UNRECONCILED}
    horizon = tc.trading_days_between(LIVE_DAY, dt.date.fromisoformat(LIVE_DAY) + dt.timedelta(days=60))[14].isoformat()
    by_id, raw = {}, {}
    for p in [x for x in rd.list_partitions("fact_transactions") if LIVE_DAY <= x <= horizon]:
        t = rd.read_parquet("fact_transactions", p).to_pydict()
        for tid, acc, trade, word, ttype, mv in zip(t["TransactionID"], t["AccountID"], t["Trade Date"], t["External Flow"], t["Transaction Type"], t["Market Value"]):
            if cbd.parse_trade_date(trade) != LIVE_DAY:
                continue
            w = "" if word is None else str(word).strip()
            v = cbd._num(mv)
            if w not in cbd.WORD_SIGN or cbd.classify("" if ttype is None else str(ttype)) == cbd.UNRESOLVED or v is None:
                continue
            k = cbd._key(acc)
            by_id[tid] = (k, cbd.WORD_SIGN[w] * abs(v))
            raw[k] = raw.get(k, 0.0) + cbd.WORD_SIGN[w] * abs(v)
    indep = {}
    for k, signed in by_id.values():
        indep[k] = indep.get(k, 0.0) + signed
    need(len(by_id) > 0, "no flow rows were read for %s" % LIVE_DAY)
    # only accounts that have a row on the day are compared (an account with a flow but no value that day has no row by design)
    bad = [k for k in set(derived) if abs(derived[k] - indep.get(k, 0.0)) > 1e-6]
    need(not bad, "the derived flow differs from the independent deduplicated sum for %d account(s) of %d" % (len(bad), len(derived)))
    inflated = [k for k in raw if k in derived and abs(raw[k] - indep.get(k, 0.0)) > 1e-6]
    need(inflated, "the control failed: the raw (undeduplicated) sum equals the deduplicated one, so this check cannot tell the defect")
    return len(by_id), len(inflated), len(derived)


def check_proof(root):
    root = Path(root)
    need(any(f.name.startswith(NEW_TEST_PREFIX) for d in (TESTS_A, TESTS_H) for f in (root / d).glob("*.py")), "the cell's test file %s* is missing" % NEW_TEST_PREFIX)
    new_tests = sorted(str(f.relative_to(root)).replace("\\", "/") for d in (TESTS_A, TESTS_H) for f in (root / d).glob(NEW_TEST_PREFIX + "*.py"))
    pytest_run(root, list(EXISTING_TESTS) + new_tests, "the adapter, rewrite and handler suites and the cell's tests", 1800)
    r = run(["ruff", "check", ADAPTER, HANDLER], root)
    need(r.returncode == 0, "ruff: %s" % (r.stdout + r.stderr)[-300:].replace("\n", " | "))
    ids, inflated, accounts = check_live(root)
    return ids, inflated, accounts


def ac3(root):
    ids, inflated, accounts = check_proof(root)
    print("live: %d distinct TransactionIDs with a flow on %s (CTO measured 277 distinct ids for the whole day), %d account(s) whose raw sum would be inflated, %d accounts equal" % (ids, LIVE_DAY, inflated, accounts))
    return True


CHECKS = {"DBC199-1-AC1": check_diff, "DBC199-2-AC1": check_behaviour, "DBC199-3-AC1": ac3}

# ---- selftest: the reference passes the static and behaviour clauses; every single-fault mutant of it fails them ----------------------------------------------------
MUTANTS = [
    ("no-dedup", ADAPTER, "            by_id[tid if tid is not None else (\"row\", p, i)] = row", "            by_id[(\"row\", p, i)] = row"),
    ("earlier-copy-wins", ADAPTER, "            by_id[tid if tid is not None else (\"row\", p, i)] = row", "            by_id.setdefault(tid if tid is not None else (\"row\", p, i), row)"),
    ("window-fifteen", ADAPTER, "LATE_WINDOW_TRADING_DAYS = 14", "LATE_WINDOW_TRADING_DAYS = 15"),
    ("window-thirteen", ADAPTER, "LATE_WINDOW_TRADING_DAYS = 14", "LATE_WINDOW_TRADING_DAYS = 13"),
    ("window-one", ADAPTER, "LATE_WINDOW_TRADING_DAYS = 14", "LATE_WINDOW_TRADING_DAYS = 1"),
    ("presence-old-rule", ADAPTER, " and not transaction_rows_dated(reader, day):", " and False:"),
    ("presence-any-partition", ADAPTER, "        if any(parse_trade_date(x) == day for x in t[\"Trade Date\"]):", "        if True:"),
    ("presence-never-held", ADAPTER, "        missing.append(\"fact_transactions partition absent and no row dated", "        pass  # missing.append(\"fact_transactions partition absent and no row dated"),
    ("settle-lag-13", HANDLER, "SETTLE_LAG_TRADING_DAYS = 14", "SETTLE_LAG_TRADING_DAYS = 13"),
    ("settle-lag-15", HANDLER, "SETTLE_LAG_TRADING_DAYS = 14", "SETTLE_LAG_TRADING_DAYS = 15"),
    ("settle-ignores-floor", HANDLER, "if back >= FLOOR_DAY and back in landed", "if back in landed"),
    ("settle-needs-no-landing", HANDLER, "and back in landed and back not in owed", "and back not in owed"),
    ("settle-includes-owed", HANDLER, " and back not in owed and back not in out", " and back not in out"),
    ("settle-duplicates", HANDLER, " and back not in out:", ":"),
    ("settle-on-explicit-days", HANDLER, "    if scheduled:\n        # the settle", "    if True:\n        # the settle"),
    ("settle-writes-when-dry", HANDLER, "res, _held = _run(s3, reader, [day], upload, rewrite=True)", "res, _held = _run(s3, reader, [day], True, rewrite=True)"),
    ("settle-not-a-rewrite", HANDLER, "res, _held = _run(s3, reader, [day], upload, rewrite=True)", "res, _held = _run(s3, reader, [day], upload, rewrite=False)"),
    ("settle-raises", HANDLER, "                except (Exception, SystemExit) as exc:  # noqa: BLE001\n                    settle_failed[day]", "                except ZeroDivisionError as exc:  # noqa: BLE001\n                    settle_failed[day]"),
    ("settle-key-renamed", HANDLER, "        out[\"settled\"] = settled", "        out[\"settled_days\"] = settled"),
]


def selftest(ref):
    ref = Path(ref)
    checks = {}
    originals = {ADAPTER: (ref / ADAPTER).read_bytes(), HANDLER: (ref / HANDLER).read_bytes()}
    check_diff(ref, git_scope=False)
    check_behaviour(ref, require_own_tests=False)
    print("reference: static clauses and the probe PASS")
    n = 0
    try:
        for name, rel, old, new in MUTANTS:
            text = originals[rel].decode("utf-8")
            if text.count(old) != 1:
                print("MUTANT %s: anchor matched %d times" % (name, text.count(old)))
                checks[name] = "ANCHOR"
                continue
            (ref / rel).write_bytes(text.replace(old, new).encode("utf-8"))
            try:
                check_diff(ref, git_scope=False)
                check_behaviour(ref, require_own_tests=False)
                checks[name] = "SURVIVED"
            except Exception as ex:  # noqa: BLE001
                checks[name] = "killed"
                print("MUTANT %s killed: %s" % (name, str(ex)[:90].replace("\n", " ")))
            n += 1
            for r, b in originals.items():
                (ref / r).write_bytes(b)
    finally:
        for r, b in originals.items():
            (ref / r).write_bytes(b)
        if (ref / PROBE_DST).exists():
            (ref / PROBE_DST).unlink()
    bad = [(k, v) for k, v in checks.items() if v != "killed"]
    print("selftest: %d mutants, %d not killed %s" % (len(checks), len(bad), bad))
    return not bad


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        ok = selftest(sys.argv[2])
        print("SELFTEST " + ("PASS" if ok else "FAIL"))
        sys.exit(0 if ok else 1)
    try:
        r = CHECKS[sys.argv[2]](sys.argv[1])
        if sys.argv[2] != "DBC199-3-AC1":
            print({"DBC199-1-AC1": "OK: only the adapter, the handler and test files changed since the branch point, within the line caps; the adapter reads TransactionID and the handler settles through the rewrite path",
                   "DBC199-2-AC1": "OK: the cell's tests and the issuer's probe pass against the worker's code (a trade repeated across rolling partitions counts once, the later copy wins, the window ends at the 14th trading day, a day with no partition of its own is present when rows dated it post later, a scheduled fire settles the day 14 trading days back)"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
