"""IRPT_DASHBD round 149, workstream PUB49F (issuer 2.0.0_SA_COO~D2) -- DB-b-292, the 49 FINANCIAL series publisher states its unreported trading days (CTO ruling msg 9224): the handler passes the gold's
partition dates and the trading calendar to publisher.build_series and the calendar's name to publisher.build_manifest, so a 49 Financial series carries `unreported_trading_days` (an EXPLICIT EMPTY LIST where the gold holds
no absent trading day) with its basis text, and its manifest carries `calendar_source`. The bundle's source-map entry gains the trading calendar as a pinned staged member and any stale pin is re-pinned. LOCAL:
python files and one JSON file; nothing is built for upload, uploaded or invoked.

  DB-b-292 (~235)   infra/aws/lambda/investor-reporting/reporting-publish/handler.py + tests/test_handler_unreported.py + infra/aws/lambda/ci/lambda-source-map.json (the one entry) + a facts record
                    DB160-1-AC1 (BEHAVIOUR on a fake S3 holding synthetic 49 Financial gold: complete gold gives an empty list, a missing partition is listed, the list is the GOLD's not the account's, the manifest names the calendar),
                    DB160-1-AC2 (the entry: the calendar added and pinned, stale pins moved, nothing else; the build-only package equals its sources; the UNPACKED handler passes AC1's behaviour),
                    DB160-1-AC3 (the worker's tests, the grant, the facts record)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure clauses on synthetic arms (and, when the handler already carries the change, fault arms on it)
       python <this file> --unpacked <dir>                 the behaviour clause on an unpacked package (used by AC2)
"""
import copy
import gzip
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
AUTHOR = "0.9.0_WK_IRPT_DASHBD~235"
REC_REL = D + AUTHOR + "/RD_PUB49F_UNREPORTED_FACTS_R149.json"
ORDER_REL = "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/IRPT_DASHBD.TO-DB-b-292.publish-49f-states-unreported-days.md"
SOURCE_DIR = "infra/aws/lambda/investor-reporting/reporting-publish"
HANDLER_REL = SOURCE_DIR + "/handler.py"
TEST_REL = SOURCE_DIR + "/tests/test_handler_unreported.py"
SOURCE_MAP_REL = "infra/aws/lambda/ci/lambda-source-map.json"
CONTRACT_REL = "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json"
ENTRY_KEY = "irpt-49f-reporting-publish-lambda"
CAL_MEMBER = "lib/trading_calendar.py"
FIXED = "trading calendar minus present partitions"
CAL_VALUES = ("pandas_market_calendars", "fallback_2010_2027")
PUBLISHER_VERSION = "0.3.0"
HEX40, HEX64 = re.compile(r"[0-9a-f]{40}$"), re.compile(r"[0-9a-f]{64}$")
LONG_DIGITS = re.compile(r"\d{8,}")
UNION_TEST_REL = SOURCE_DIR + "/tests/test_publisher_account_union.py"
TESTS_DIR = SOURCE_DIR + "/tests"
GRANT_FILES = {HANDLER_REL, TEST_REL, SOURCE_MAP_REL, UNION_TEST_REL}
GRANT_PREFIXES = (D + AUTHOR + "/", "org/missions/D9/IRPT/IRPT_DASHBD/surprise-channel/investigations/", "org/missions/D9/IRPT/IRPT_DASHBD/task-orders/")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(root, *a):
    r = subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True)
    return r.stdout, r.returncode


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def p148():
    return helper("r147/p148_cothandler.py", "p148_helper")


def p149():
    return helper("r147/p149_pubroot.py", "p149_helper")


def base_commit(root):
    out, _ = git(root, "log", "--diff-filter=A", "--format=%H", "--", ORDER_REL)
    need(out.split(), "the order's first commit is not in this history")
    return out.decode().split()[-1]


def own_commits(root):
    out, _ = git(root, "log", "--reverse", "--format=%H", "--author=" + AUTHOR, base_commit(root) + "..HEAD")
    need(out.split(), "no commit by %s since the order was issued" % AUTHOR)
    return out.decode().split()


# ------------------------------------------------------------------------------------------------ the behaviour clause
COLS = ["account_id", "business_date", "market_value_eod", "total_return_daily", "return_basis", "day_quality", "external_flow", "income_received", "holdings_price_return", "method_version", "history_scope"]


def fixture(h, tc, naming, firm, drop_day=None):
    """-> (FakeS3, expectations). Gold for the 49 Financial firm: every trading day 2026-07-06 .. 2026-07-24 (less drop_day when given), accounts A (all days), B (07-13 .. 07-22) and C (B's window, with NO ROW on
    2026-07-16 although that day's partition exists); income is a number on every day."""
    probe = str(naming.address("irpt", firm, "gold", "account_return_daily", "date=2026-07-06", "data.parquet"))
    prefix = probe[len("s3://"):].partition("/")[2].rsplit("/date=", 1)[0] + "/"
    days = h.trading(tc, "2026-07-06", "2026-07-24")
    present = [d for d in days if d != drop_day]

    def row(acct, d, i, value=100.0):
        first = i == 0
        return {"account_id": acct, "business_date": d, "market_value_eod": value + i, "total_return_daily": None if first else 0.001, "return_basis": "NOT_MEASURABLE" if first else "TWR",
                "day_quality": "NOT_MEASURABLE" if first else "MEASURED", "external_flow": 0.0, "income_received": 0.0, "holdings_price_return": None, "method_version": 3, "history_scope": "PARTIAL_HISTORY"}
    b_days = [d for d in days if "2026-07-13" <= d <= "2026-07-22"]
    objs = {}
    for d in present:
        rows = [row("A0000000001", d, present.index(d))]
        if d in b_days:
            rows.append(row("B0000000002", d, b_days.index(d), 200.0))
            if d != "2026-07-16":
                rows.append(row("C0000000003", d, b_days.index(d), 300.0))
        objs["%sdate=%s/data.parquet" % (prefix, d)] = h.parquet_bytes(rows, COLS)
    return h.FakeS3(objs), {"present": present, "firm": firm, "days": days}


def load_handler(h, root, handler_path, name="f49_handler"):
    return h.load_module(handler_path, name)


def check_behaviour(h, root, handler_path, patch=None, contract_root=None):
    """The behaviour clause. `patch(publisher_module)` injects a fault for the self-test and returns an undo callable. The series contract is read from
    `contract_root` (default root): the bundle does not package it, so the unpacked run grades against the repo's."""
    root = Path(root)
    naming = h.load_module(root / "lib" / "opal_naming.py", "opal_naming")
    tc = h.load_module(root / "lib" / "trading_calendar.py", "trading_calendar")
    mod = load_handler(h, root, handler_path)
    for name in ("run", "resolve_firm", "_publish_one"):
        need(hasattr(mod, name), "the handler must define %s" % name)
    firm = mod.resolve_firm(None)[1]
    contract = json.loads((Path(contract_root or root) / CONTRACT_REL).read_bytes().decode("utf-8"))
    pub = sys.modules["publisher"]
    undo = patch(pub) if patch else None
    try:
        for drop, label in ((None, "complete gold"), ("2026-07-15", "gold missing 2026-07-15")):
            s3, ex = fixture(h, tc, naming, firm, drop)
            res = mod.run(accounts=None, upload=True, s3=s3, contract=contract)
            need(len(res) == 3 and all(r["ok"] for r in res), "%s: three accounts must build and validate against the series contract: %s" % (label, [r.get("error") for r in res if not r["ok"]][:2]))
            want = [] if drop is None else [drop]
            for acct in ("A0000000001", "B0000000002", "C0000000003"):
                gz = s3.puts[h.series_key(naming, firm, acct, "series.json.gz")]
                s = json.loads(gzip.decompress(gz).decode("utf-8"))
                need("unreported_trading_days" in s and "unreported_trading_days_basis" in s, "%s: %s's series must carry the unreported-days pair (an absent field would read as not measured)" % (label, acct[:1]))
                if drop is None:
                    need(s["unreported_trading_days"] == [], "%s: %s's list must be the EXPLICIT empty list, got %s" % (label, acct[:1], s["unreported_trading_days"]))
                need(s["unreported_trading_days"] == want, "%s: %s's unreported days must be the gold's missing trading days %s, got %s" % (label, acct[:1], want, s["unreported_trading_days"]))
                need(s["unreported_trading_days_basis"] == FIXED, "%s: the basis text" % label)
                need("income_claim" not in s and all(x == 0.0 for x in s["income"]), "%s: numeric income writes no claim" % label)
                m = json.loads(s3.puts[h.series_key(naming, firm, acct, "manifest.json")].decode("utf-8"))
                src = "pandas_market_calendars" if tc.calendar_source().startswith("NYSE/pandas_market_calendars") else "fallback_%d_%d" % (tc.FALLBACK_FIRST_YEAR, tc.FALLBACK_LAST_YEAR)
                need(m.get("calendar_source") == src and m["calendar_source"] in CAL_VALUES, "%s: the manifest's calendar_source must be %s, got %r" % (label, src, m.get("calendar_source")))
                need(m["publisher_version"] == PUBLISHER_VERSION and m["firm"] == firm and m["account_id"] == acct and m["byte_sizes"]["series.json.gz"] == len(gz), "%s: manifest firm, account, size or publisher version" % label)
    finally:
        if undo:
            undo()
    return True


# ------------------------------------------------------------------------------------------------ faults for the self-test
def fault_drop_present(pub):
    orig = pub.build_series
    pub.build_series = lambda rows, present_dates=None, calendar=None: orig(rows)
    return lambda: setattr(pub, "build_series", orig)


def fault_empty_present(pub):
    orig = pub.build_series
    pub.build_series = lambda rows, present_dates=None, calendar=None: orig(rows, present_dates=[], calendar=calendar)
    return lambda: setattr(pub, "build_series", orig)


def fault_account_dates(pub):
    orig = pub.build_series
    pub.build_series = lambda rows, present_dates=None, calendar=None: orig(rows, present_dates=[r["business_date"] for r in rows], calendar=calendar)
    return lambda: setattr(pub, "build_series", orig)


def fault_drop_calendar_source(pub):
    orig = pub.build_manifest
    pub.build_manifest = lambda account_id, firm, series, gz_len, built_at=None, calendar_source=None: orig(account_id, firm, series, gz_len, built_at=built_at)
    return lambda: setattr(pub, "build_manifest", orig)


def fault_wrong_calendar_source(pub):
    orig = pub.build_manifest
    pub.build_manifest = lambda account_id, firm, series, gz_len, built_at=None, calendar_source=None: orig(account_id, firm, series, gz_len, built_at=built_at, calendar_source="pandas_market_calendars" if calendar_source != "pandas_market_calendars" else "fallback_2010_2027")
    return lambda: setattr(pub, "build_manifest", orig)


FAULTS = (("pair dropped", fault_drop_present), ("empty present dates", fault_empty_present), ("the account's own dates", fault_account_dates), ("calendar_source dropped", fault_drop_calendar_source), ("calendar_source wrong", fault_wrong_calendar_source))


# ------------------------------------------------------------------------------------------------ the entry clause
def check_entry(base_map, new_map, head_blob, pin_blob, pin_ok):
    for k in set(base_map) | set(new_map):
        if k != "functions":
            need(base_map.get(k) == new_map.get(k), "a top-level key changed: %s" % k)
    bf, nf = base_map["functions"], new_map["functions"]
    need(set(bf) == set(nf), "the set of entries changed")
    for k in bf:
        if k != ENTRY_KEY:
            need(bf[k] == nf[k], "another entry changed: %s" % k)
    be, ne = bf[ENTRY_KEY], nf[ENTRY_KEY]
    need({k: v for k, v in be.items() if k not in ("files", "staged_from")} == {k: v for k, v in ne.items() if k not in ("files", "staged_from")},
         "the entry changed beyond files and staged_from (the deployed artifact_sha256, last_deployed_commit, recorded_by and the notes must be untouched)")
    need(CAL_MEMBER not in be["files"] and ne["files"].count(CAL_MEMBER) == 1, "files must list %s exactly once" % CAL_MEMBER)
    need([f for f in ne["files"] if f != CAL_MEMBER] == be["files"], "files must be the base list plus %s and nothing else, in the base order" % CAL_MEMBER)
    bs, ns = be["staged_from"], ne["staged_from"]
    need([s["repo_path"] for s in ns if s["repo_path"] != CAL_MEMBER] == [s["repo_path"] for s in bs], "staged_from must be the base members in the base order plus %s" % CAL_MEMBER)
    need(sum(1 for s in ns if s["repo_path"] == CAL_MEMBER) == 1, "staged_from must hold %s exactly once" % CAL_MEMBER)
    bmap = {s["repo_path"]: s for s in bs}
    moved = []
    for n in ns:
        need(set(n) == {"repo_path", "pin", "packaged_as", "sha256"} and n["packaged_as"] == n["repo_path"] or n["repo_path"] in bmap and n["packaged_as"] == bmap[n["repo_path"]]["packaged_as"] and set(n) == {"repo_path", "pin", "packaged_as", "sha256"},
             "member form: %s" % n.get("repo_path"))
        need(isinstance(n["pin"], str) and HEX40.match(n["pin"]) and isinstance(n["sha256"], str) and HEX64.match(n["sha256"]), "pin or sha256 form: %s" % n["repo_path"])
        need(pin_ok(n["pin"]), "pin of %s is not an ancestor commit" % n["repo_path"])
        need(sha(pin_blob(n["pin"], n["repo_path"])) == n["sha256"] == sha(head_blob(n["repo_path"])), "sha256 of %s differs from git show pin:path or from the file at HEAD" % n["repo_path"])
        if n["repo_path"] == CAL_MEMBER:
            need(n["packaged_as"] == CAL_MEMBER, "the calendar is packaged as %s" % CAL_MEMBER)
            continue
        b = bmap[n["repo_path"]]
        if b["sha256"] == sha(head_blob(b["repo_path"])):
            need(n == b, "member %s is not stale and must stay byte-identical" % b["repo_path"])
        else:
            need(n["pin"] != b["pin"] and n["sha256"] != b["sha256"] and n["packaged_as"] == b["packaged_as"], "stale member %s must get a new pin and sha256 and keep its packaged_as" % b["repo_path"])
            moved.append(b["repo_path"])
    return moved


def check_facts(rec, moved, n_tests):
    exp = {"entry", "added_member", "repinned", "tests", "words"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["entry"] == ENTRY_KEY and rec["added_member"] == CAL_MEMBER and sorted(rec["repinned"]) == sorted(moved), "entry, added_member or repinned differ from the recount")
    need(isinstance(rec["tests"], int) and not isinstance(rec["tests"], bool) and rec["tests"] == n_tests >= 8, "tests must equal the recount and be at least 8")
    need(nes(rec["words"]) and 80 <= len(rec["words"]) <= 1800 and not LONG_DIGITS.findall(rec["words"]), "words must be one paragraph of 80 to 1800 characters with no long digit run")
    return True


def check_grant(changed):
    bad = [f for f in changed if f not in GRANT_FILES and not f.startswith(GRANT_PREFIXES)]
    need(not bad, "the worker's commits touch files outside its grant: %s" % bad[:3])
    need(HANDLER_REL in changed and TEST_REL in changed and SOURCE_MAP_REL in changed, "the handler, its test file and the source map must all change")
    return True


def check_test_words(text):
    need("unreported_trading_days" in text and "calendar_source" in text and "== []" in text, "the test file must assert the unreported list (including the empty list) and calendar_source")
    return True


# ------------------------------------------------------------------------------------------------ the run
def run_pytest(root, target):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target], cwd=str(root), capture_output=True, text=True, timeout=900)
    m = re.search(r"(\d+) passed", r.stdout)
    need(r.returncode == 0 and m is not None, "tests failed: %s" % r.stdout[-300:].replace("\n", " | "))
    return int(m.group(1))


def build_only(root):
    env = dict(os.environ, BUILD_ONLY="1")
    r = subprocess.run(["bash", "infra/aws/lambda/ci/build-and-upload.sh", "investor-reporting", ENTRY_KEY], cwd=str(root), env=env, capture_output=True, text=True, timeout=300)
    m = re.search(r"BUILD_ONLY:\s*(\S+)\s+sha256=(\S+)", r.stdout + r.stderr)
    need(r.returncode == 0 and m is not None, "the build-only run failed (rc %s): %s" % (r.returncode, (r.stdout + r.stderr)[-300:].replace("\n", " | ")))
    zpath = m.group(1)
    if zpath.startswith("/"):
        cp = subprocess.run(["cygpath", "-w", zpath], capture_output=True, text=True)
        need(cp.returncode == 0, "cygpath could not resolve %s" % zpath)
        zpath = cp.stdout.strip()
    return zpath


def source_of(root, entry, member):
    """The repo file a package member is built from: handler.py and publisher.py from the entry's source_dir, a staged member from its repo_path."""
    if member in ("handler.py", "publisher.py"):
        return Path(root) / entry["source_dir"] / member
    for s in entry["staged_from"]:
        if s["packaged_as"] == member:
            return Path(root) / s["repo_path"]
    return Path(root) / member


def run(root, cid):
    root = Path(root)
    need((root / HANDLER_REL).is_file(), "no %s" % HANDLER_REL)
    h = p148()
    if cid == "DB160-1-AC1":
        check_behaviour(h, root, root / HANDLER_REL)
        print("OK: on a fake S3 holding synthetic 49 Financial gold the handler publishes series that validate against the series contract; with every trading day present each carries the EXPLICIT empty unreported list and its basis text, with 2026-07-15 absent each lists exactly that day (the gold's missing days, not the account's own), the manifest names the calendar that answered (publisher 0.3.0), and numeric income writes no claim")
        return True
    bm = json.loads(git(root, "show", "%s:%s" % (base_commit(root), SOURCE_MAP_REL))[0].decode("utf-8"))
    nm = json.loads((root / SOURCE_MAP_REL).read_text(encoding="utf-8"))

    def head_blob(p):
        return (root / p).read_bytes()

    def pin_blob(pin, p):
        out, rc = git(root, "show", "%s:%s" % (pin, p))
        need(rc == 0, "git show %s:%s failed" % (pin[:10], p))
        return out

    def pin_ok(pin):
        return git(root, "merge-base", "--is-ancestor", pin, "HEAD")[1] == 0
    if cid == "DB160-1-AC2":
        moved = check_entry(bm, nm, head_blob, pin_blob, pin_ok)
        entry = nm["functions"][ENTRY_KEY]
        zpath = build_only(root)
        hh = p149()
        sources = {f: source_of(root, entry, f).read_text(encoding="utf-8") for f in entry["files"] if f.endswith(".py")}
        mods = {Path(f).stem for f in sources} | {"lib"}
        hh.check_imports(hh.third_party(sources, mods), lambda n: n in hh.layer_names(hh.latest_layer_version()))
        tmp = Path(tempfile.mkdtemp(prefix="p160_pkg_"))
        try:
            with zipfile.ZipFile(zpath) as z:
                hh.check_package([n for n in z.namelist() if not n.endswith("/")], entry["files"], lambda mem: z.read(mem), lambda mem: source_of(root, entry, mem).read_bytes())
                z.extractall(tmp)
            r = subprocess.run([sys.executable, "-I", str(Path(__file__).resolve()), "--unpacked", str(tmp), str(root)], capture_output=True, text=True, timeout=600, cwd=str(tmp))
            need(r.returncode == 0 and "UNPACKED PASS" in r.stdout, "the unpacked handler failed the behaviour clause: %s" % (r.stdout + r.stderr)[-300:].replace("\n", " | "))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        print("OK: the entry %s gained %s (pinned, sha256 = git show pin:path = the file at HEAD) and %d stale pin(s) moved, nothing else changed; the build-only package of %d members equals its sources byte for byte, its third-party imports are pyarrow plus the runtime's, and the UNPACKED handler passes the behaviour clause" % (ENTRY_KEY, CAL_MEMBER, len(moved), len(entry["files"])))
        return True
    if cid == "DB160-1-AC3":
        need((root / TEST_REL).is_file(), "no %s" % TEST_REL)
        n = run_pytest(root, TEST_REL)
        n_dir = run_pytest(root, TESTS_DIR)
        need(n_dir >= n, "the whole tests directory must pass (it holds %d passing tests)" % n_dir)
        check_test_words((root / TEST_REL).read_text(encoding="utf-8"))
        moved = check_entry(bm, nm, head_blob, pin_blob, pin_ok)
        changed = set()
        for cm in own_commits(root):
            changed |= set(git(root, "show", "--name-only", "--format=", cm)[0].decode().split())
        check_grant(changed)
        check_facts(json.loads((root / REC_REL).read_text(encoding="utf-8")), moved, n)
        print("OK: %d new tests pass and assert the empty list, a listed day and calendar_source, and the whole tests directory passes (%d tests); %d files changed, all in the grant; the facts record equals the recount" % (n, n_dir, len(changed)))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    files = ["handler.py", "publisher.py", "lib/opal_naming.py", "ids.py"]
    blobs = {("pa", "lib/opal_naming.py"): b"n1", ("pb", "ids.py"): b"i1", ("pc", "ids.py"): b"i2", ("pd", CAL_MEMBER): b"c1"}
    head = {"lib/opal_naming.py": b"n1", "ids.py": b"i2", CAL_MEMBER: b"c1"}

    PINS = {"pa": "a" * 40, "pb": "b" * 40, "pc": "c" * 40, "pd": "d" * 40}
    REV = {v: k for k, v in PINS.items()}

    def member(path, pin, packaged=None, content=None):
        return {"repo_path": path, "pin": PINS[pin], "packaged_as": packaged or path, "sha256": sha(content)}
    base_entry = {"source_dir": SOURCE_DIR, "files": list(files), "artifact_sha256": "x", "last_deployed_commit": "y", "_build_note": "n",
                  "staged_from": [member("lib/opal_naming.py", "pa", content=b"n1"), member("x/ids.py", "pb", "ids.py", b"i1")]}
    head["x/ids.py"] = b"i2"
    blobs[("pc", "x/ids.py")] = b"i2"
    blobs[("pb", "x/ids.py")] = b"i1"
    blobs[("pa", "lib/opal_naming.py")] = b"n1"
    base = {"_d": 1, "functions": {ENTRY_KEY: base_entry, "other": {"k": 1}}}
    new_entry = copy.deepcopy(base_entry)
    new_entry["files"] = ["handler.py", "publisher.py", "lib/opal_naming.py", CAL_MEMBER, "ids.py"]
    new_entry["staged_from"] = [member("lib/opal_naming.py", "pa", content=b"n1"), member(CAL_MEMBER, "pd", content=b"c1"), member("x/ids.py", "pc", "ids.py", b"i2")]
    new = {"_d": 1, "functions": {ENTRY_KEY: new_entry, "other": {"k": 1}}}

    def hb(p):
        return head[p]

    def pb(pin, p):
        return blobs[(REV[pin], p)]
    pin_ok = lambda pin: True  # noqa: E731
    moved = check_entry(base, new, hb, pb, pin_ok)
    assert moved == ["x/ids.py"], moved
    arms = (("deployed field", lambda n: n["functions"][ENTRY_KEY].update(artifact_sha256="z")), ("other entry", lambda n: n["functions"]["other"].update(k=2)), ("top key", lambda n: n.update(_d=2)),
            ("files extra", lambda n: n["functions"][ENTRY_KEY]["files"].append("zzz.py")), ("calendar missing from files", lambda n: n["functions"][ENTRY_KEY]["files"].remove(CAL_MEMBER)),
            ("calendar missing from staged", lambda n: n["functions"][ENTRY_KEY]["staged_from"].pop(1)), ("stale kept", lambda n: n["functions"][ENTRY_KEY]["staged_from"].__setitem__(2, member("x/ids.py", "pb", "ids.py", b"i1"))),
            ("bad sha", lambda n: n["functions"][ENTRY_KEY]["staged_from"][1].update(sha256="e" * 64)), ("packaged_as moved", lambda n: n["functions"][ENTRY_KEY]["staged_from"][2].update(packaged_as="q/ids.py")),
            ("member reordered", lambda n: n["functions"][ENTRY_KEY]["staged_from"].reverse()))
    for label, fn in arms:
        n2 = copy.deepcopy(new)
        fn(n2)
        red(lambda: check_entry(base, n2, hb, pb, pin_ok), label)
    red(lambda: check_entry(base, new, hb, pb, lambda pin: False), "pin not an ancestor")
    rec = {"entry": ENTRY_KEY, "added_member": CAL_MEMBER, "repinned": ["x/ids.py"], "tests": 8, "words": "w" * 100}
    assert check_facts(rec, ["x/ids.py"], 8)
    farms = (("entry", lambda r: r.update(entry="z")), ("member", lambda r: r.update(added_member="q")), ("repinned", lambda r: r.update(repinned=[])), ("tests", lambda r: r.update(tests=9)), ("extra", lambda r: r.update(z=1)),
             ("words", lambda r: r.update(words="short")), ("digits", lambda r: r.update(words="w" * 100 + " 123456789")))
    for label, fn in farms:
        r2 = copy.deepcopy(rec)
        fn(r2)
        red(lambda: check_facts(r2, ["x/ids.py"], 8), label)
    assert check_grant({HANDLER_REL, TEST_REL, SOURCE_MAP_REL, UNION_TEST_REL, D + AUTHOR + "/x.json"})
    red(lambda: check_grant({HANDLER_REL, TEST_REL}), "no source map")
    red(lambda: check_grant({HANDLER_REL, TEST_REL, SOURCE_MAP_REL, "lib/x.py"}), "outside grant")
    assert check_test_words("a unreported_trading_days b calendar_source c == []")
    red(lambda: check_test_words("unreported_trading_days calendar_source"), "no empty-list assertion")
    print("selftest: entry (%d red arms + ancestry), facts (%d red arms), grant (2) and test-words (1) clauses behave" % (len(arms), len(farms)))
    root = Path(__file__).resolve().parents[9]
    h = p148()
    try:
        check_behaviour(h, root, root / HANDLER_REL)
    except Fail as e:
        print("selftest: the handler at HEAD does not carry the change yet (%s); fault arms skipped" % str(e)[:90])
    else:
        for label, fault in FAULTS:
            red(lambda: check_behaviour(h, root, root / HANDLER_REL, patch=fault), "fault: " + label)
        print("selftest: the behaviour clause is green on the handler at HEAD and red on %d injected faults" % len(FAULTS))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    if sys.argv[1:2] == ["--unpacked"]:
        tmp = Path(sys.argv[2])
        try:
            check_behaviour(p148(), tmp, tmp / "handler.py", contract_root=sys.argv[3])
            print("UNPACKED PASS")
            sys.exit(0)
        except Exception as e:  # noqa: BLE001
            print("UNPACKED FAIL: " + str(e))
            sys.exit(1)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
