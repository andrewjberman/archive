"""IRPT_BCKEND round 189 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB189-1  IB-pr-527  the IR holdings class rule BUILT: on the canonical-row branch of classify_security a row whose sub_asset_class (trimmed, lower-cased) is cash serves the cash class; the fallback layer is unchanged (BUILD ONLY, offline)
    AC1  the classification test set passes (the baseline 101 and at least 5 new in tests/test_holdings_cash_rule.py), the tests folder holds the baseline files plus that one, and holdings_snapshot.py differs from its base blob only in classify_security and its neighbour
    AC2  the behaviour: a canonical fixed_income row with sub Cash serves cash (sub, basis and class_source kept), a lower-case cash sub too, via a CUSIP key too; an equity row, an already-cash row and a Money Market row are untouched; the fallback layer is untouched
    AC3  one definition: exactly one function named like cash_rule, called exactly once in classify_security and only on the canonical-row branch; the admitted class enum and the CASH-line rule are unchanged
  IB189-2  IB-pr-528  the IR holdings class rule's count split by layer, the FDRXX-on-Inflection check, and the never-widen packet (READ ONLY)
    AC1  the FDRXX check: the canonical table's row for FDRXX read, Inflection's FDRXX nodes counted, the rule scope stated and consistent with them
    AC2  the split: per firm the would-move nodes split into the canonical branch and the fallback branch, summing to the total, public symbols only, the IB-pr-526 upper bounds compared
    AC3  the packet and the counters: the never-widen packet for the rule's later release (counts, blast radius, rollback, both halves unsigned), no client identifier, no long digit run, the six bound counters 0
"""
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HS_DIR = "data/assets/scripts/gold/investor_reporting"
HS = HS_DIR + "/holdings_snapshot.py"
PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
BASE_BLOB = "71d6b50322cd08c9492e962f90ad693e11526c3e"
BASE_ENUM = ("equity", "fixed_income", "alternatives", "cash", "other", "structured", "commodities", "unclassified")
SET8 = ["test_holdings_classification.py", "test_holdings_cusip_fallback.py", "test_holdings_narrowed.py", "test_holdings_unclassified.py",
        "test_holdings_snapshot.py", "test_holdings_publish_gate.py", "test_holdings_multi_asset_v1_enum.py", "test_holdings_display.py"]
BASE_TESTS = ["test_build_refuses_planted_member.py", "test_bundle_manifest_stamp.py", "test_cot_account_mapping.py", "test_directory_account_masks.py",
              "test_directory_runner.py", "test_directory_runner_refuse_drop.py", "test_directory_runner_source_principal.py",
              "test_directory_runner_terminated.py", "test_economic_regressions.py", "test_holdings_49f.py", "test_holdings_49f_account_id.py",
              "test_holdings_classification.py", "test_holdings_cusip_fallback.py", "test_holdings_display.py", "test_holdings_inf.py",
              "test_holdings_membership.py", "test_holdings_multi_asset_v1_enum.py", "test_holdings_narrowed.py", "test_holdings_publish_gate.py",
              "test_holdings_rearm_trigger.py", "test_holdings_snapshot.py", "test_holdings_unclassified.py", "test_holdouts.py", "test_inf_positions.py",
              "test_l0_categories.py", "test_retained_capture_cleanup.py", "test_runner_jsonschema_tolerance.py", "test_schwab_codes.py",
              "test_smartx_valuation.py", "test_source_inputs.py", "test_tax_membership_once.py", "test_vendor_keys.py"]
NEWT = "test_holdings_cash_rule.py"
REC2 = D + "0.9.0_WK_IRPT_BCKEND~375/IB189-2_cash_rule_by_layer.json"
PACKET = D + "0.9.0_WK_IRPT_BCKEND~375/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-528.md"
BOUND2 = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
BOUNDS_526 = {"49financial": 32, "cottonwood": 253, "inflection": 841}
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB189"))
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


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT)] + list(args), capture_output=True, text=True)


def no_long_digits(txt):
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", txt):
        fail("a long digit run (an identifier or a figure) is present")


def hs_text():
    f = ROOT / HS
    if not f.is_file():
        fail("no %s" % HS)
    return f.read_text(encoding="utf-8")


def build_ac1():
    gold = ROOT / HS_DIR
    newt = gold / "tests" / NEWT
    if not newt.is_file() or newt.read_text(encoding="utf-8").count("def test_") < 5:
        fail("tests/%s must exist with at least 5 test functions" % NEWT)
    files = ["tests/" + n for n in SET8] + ["tests/" + NEWT]
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + files, cwd=str(gold), capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), timeout=150)
    m = re.search(r"(\d+) passed", r.stdout)
    if r.returncode != 0 or not m or int(m.group(1)) < 106 or " failed" in r.stdout:
        fail("pytest of the classification set must pass with at least 106 tests (101 baseline + 5 new): rc %s %s" % (r.returncode, (r.stdout + r.stderr)[-200:]))
    tests = sorted(p.name for p in (gold / "tests").glob("test_*.py"))
    if tests != sorted(BASE_TESTS + [NEWT]):
        fail("tests/ must hold exactly the baseline files plus %s; found %s" % (NEWT, tests))
    if git("cat-file", "-e", BASE_BLOB).returncode == 0:
        fd, tmp = tempfile.mkstemp(prefix="p189base_", suffix=".py")
        try:
            os.write(fd, subprocess.run(["git", "-C", str(ROOT), "cat-file", "-p", BASE_BLOB], capture_output=True).stdout)
            os.close(fd)
            d = subprocess.run(["git", "diff", "--no-index", "-U0", tmp, str(ROOT / HS)], capture_output=True, text=True, cwd=str(ROOT)).stdout
        finally:
            os.remove(tmp)
        if not d.strip():
            fail("holdings_snapshot.py equals its base blob: the rule is absent")
        labels = set()
        for ln in d.splitlines():
            mm = re.match(r"@@ [^@]+ @@\s*(.*)$", ln)
            if mm:
                lab = mm.group(1).strip()
                labels.add(re.sub(r"^def\s+(\w+).*", r"\1", lab) if lab.startswith("def ") else lab)
        allowed = {"cusip_key", "classify_security", ""}
        if not labels <= allowed:
            fail("holdings_snapshot.py hunks may sit only at %s; found %s" % (sorted(allowed), sorted(labels)))
    print("OK: %s tests pass; the change is confined" % m.group(1))


def _hs():
    d = str(ROOT / HS_DIR)
    if d not in sys.path:
        sys.path.insert(0, d)
    for name in [m for m in sys.modules if m in ("holdings_snapshot", "bd_securities_fallback")]:
        del sys.modules[name]
    import holdings_snapshot as hs
    import bd_securities_fallback as ec
    return hs, ec


class _Clf:
    """A _NarrowedClassifier stand-in: a canonical table in memory over a real fallback class with its own in-memory table."""

    def __init__(self, ec, canonical, fallback_rows):
        fb = ec.ETFClassifier.__new__(ec.ETFClassifier)
        fb._ticker_map, fb._name_map = {}, {}
        for row in fallback_rows:
            fb._ticker_map[row["ticker"]] = row
            for alias in row.get("name_aliases", ()):
                fb._name_map[fb.normalize_name(alias)] = row["ticker"]
        self._fb, self._canon = fb, canonical

    @property
    def _ticker_map(self):
        return self._fb._ticker_map

    @property
    def _name_map(self):
        return self._fb._name_map

    def canonical_lookup(self, key):
        return self._canon.get(key)

    def classify(self, ticker, name):
        return self._fb.classify(ticker, name)

    def get_sub_asset_class(self, ticker, name=None):
        return self._fb.get_sub_asset_class(ticker, name)

    @staticmethod
    def normalize_name(s):
        import bd_securities_fallback as ec2
        return ec2.ETFClassifier.normalize_name(s)


def build_ac2():
    hs, ec = _hs()
    canon = {"FDRXX": {"asset_class": "fixed_income", "sub_asset_class": "Cash"},
             "LOWCS": {"asset_class": "fixed_income", "sub_asset_class": "cash"},
             "PADCS": {"asset_class": "fixed_income", "sub_asset_class": " Cash "},
             "CUSIP:912828XX0": {"asset_class": "fixed_income", "sub_asset_class": "Cash"},
             "SPY": {"asset_class": "equity", "sub_asset_class": "US Large Cap"},
             "ALRCS": {"asset_class": "cash", "sub_asset_class": "Cash"},
             "MMKT": {"asset_class": "fixed_income", "sub_asset_class": "Money Market"},
             "NOSUB": {"asset_class": "fixed_income", "sub_asset_class": None}}
    fb = [{"ticker": "FBCSH", "asset_class": "fixed_income", "sub_asset_class": "Cash", "name_aliases": {"FALLBACK CASH FUND"}}]
    clf = _Clf(ec, canon, fb)
    ccs = hs.CANONICAL_CLASS_SOURCE

    def one(ticker, name, **kw):
        return hs.classify_security(ec, clf, ticker, name, **kw)

    g = one("FDRXX", "FIDELITY GOVERNMENT CASH RESERVES")
    if g["asset_class"] != "cash" or g["sub_asset_class"] != "Cash" or g["asset_class_basis"] != "TABLE" or g["class_source"] != ccs:
        fail("a canonical fixed_income row with sub Cash must serve cash with its sub, basis TABLE and canonical class_source: %r" % g)
    for t in ("LOWCS", "PADCS"):
        if one(t, "X")["asset_class"] != "cash":
            fail("a canonical row whose sub, trimmed and lower-cased, is cash must serve cash (%s)" % t)
    g = one("", "US TREASURY MONEY", security_id={"namespace": "CUSIP", "value": "912828xx0"})
    if g["asset_class"] != "cash" or g["class_source"] != ccs:
        fail("a CUSIP-key canonical hit with sub Cash must serve cash too: %r" % g)
    for t, want in (("SPY", "equity"), ("ALRCS", "cash"), ("MMKT", "fixed_income"), ("NOSUB", "fixed_income")):
        g = one(t, "X")
        if g["asset_class"] != want or g["class_source"] != ccs:
            fail("%s must stay %s (the rule acts only on a Cash sub): %r" % (t, want, g))
    g = one("FBCSH", "FALLBACK CASH FUND")
    if g["asset_class"] != "fixed_income" or g["class_source"] == ccs:
        fail("the fallback layer must be unchanged (a fallback row with sub Cash stays fixed_income): %r" % g)
    g = one("CASH", "CASH", description="CASH")
    if g["asset_class"] != "cash" or g["asset_class_basis"] != "NAME_PATTERN":
        fail("the Pathward CASH-line rule must be unchanged: %r" % g)
    print("OK: the rule acts on the canonical branch only, on a Cash sub only")


def build_ac3():
    txt = hs_text()
    try:
        tree = ast.parse(txt)
    except SyntaxError as e:
        fail("holdings_snapshot.py does not parse: %s" % e)
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef) and "cash_rule" in n.name]
    if len(fns) != 1:
        fail("exactly one top-level function named like cash_rule must exist; found %d" % len(fns))
    name = fns[0].name
    cs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "classify_security"]
    if len(cs) != 1:
        fail("classify_security must exist once")
    calls = [n for n in ast.walk(cs[0]) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name]
    if len(calls) != 1:
        fail("classify_security must call %s exactly once; found %d" % (name, len(calls)))
    fb_line = None
    for n in ast.walk(cs[0]):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "answer" for t in n.targets):
            fb_line = n.lineno
    if fb_line is None or calls[0].lineno >= fb_line:
        fail("the call must sit on the canonical-row branch, before the fallback answer line")
    other = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name and n not in calls]
    if other:
        fail("%s must not be called anywhere else" % name)
    hs, _ec = _hs()
    if tuple(hs.ASSET_CLASS_VALUES) != BASE_ENUM:
        fail("ASSET_CLASS_VALUES must be unchanged")
    print("OK: one definition, one call, canonical branch only")


def fdrxx(arm):
    r = load(REC2)
    f = r.get("fdrxx_inflection") or {}
    ct = r.get("canonical_table") or {}
    if arm == "AC1":
        for k in ("canonical_row_found", "resolves_on_canonical_branch"):
            if not isinstance(f.get(k), bool):
                fail("fdrxx_inflection.%s must be true or false" % k)
        if f.get("ticker") != "FDRXX":
            fail("fdrxx_inflection.ticker must be FDRXX")
        if not (is_int(ct.get("rows")) and ct["rows"] > 0 and is_int(ct.get("cash_subclass_rows")) and ct["cash_subclass_rows"] > 0):
            fail("canonical_table needs integer rows and cash_subclass_rows, both above 0 (a table that could not be scanned cannot answer the check)")
        n = f.get("inflection_nodes_with_ticker")
        if not (is_int(n) and n >= 0):
            fail("inflection_nodes_with_ticker must be an integer >= 0")
        if f["canonical_row_found"]:
            if not (str(f.get("canonical_asset_class", "")).strip() and str(f.get("canonical_sub_asset_class", "")).strip()):
                fail("a found canonical row needs its asset_class and sub_asset_class")
        sub = str(f.get("canonical_sub_asset_class", "")).strip().lower()
        want = bool(f["canonical_row_found"] and sub == "cash" and n > 0)
        if f["resolves_on_canonical_branch"] != want:
            fail("resolves_on_canonical_branch must equal (row found and its sub is cash and Inflection holds the ticker)")
        scope = r.get("rule_scope")
        if scope != ("canonical_only" if want else "canonical_and_fallback"):
            fail("rule_scope must be canonical_only when FDRXX resolves canonically, else canonical_and_fallback")
        if not str(f.get("reading", "")).strip():
            fail("fdrxx_inflection.reading is required")
    print("OK: FDRXX check")


def split(arm):
    r = load(REC2)
    firms = r.get("firms") or {}
    if sorted(firms) != ["49financial", "cottonwood", "inflection"]:
        fail("firms must hold exactly 49financial, cottonwood and inflection")
    for k, v in firms.items():
        s = v.get("snapshot_read") or {}
        if not isinstance(s.get("found"), bool):
            fail("%s: snapshot_read.found must be true or false" % k)
        if s["found"] and not (is_date(s.get("business_date")) and is_int(s.get("nodes")) and s["nodes"] >= 0):
            fail("%s: a found snapshot needs a business_date and an integer node count" % k)
        if not s["found"] and not str(s.get("reason", "")).strip():
            fail("%s: a snapshot not found needs its stated reason" % k)
        if not s["found"]:
            for key in ("would_move_total", "canonical_branch", "fallback_branch"):
                if v.get(key) is not None:
                    fail("%s: no snapshot was found, so %s must be null" % (k, key))
            continue
        t, c, fbk = v.get("would_move_total"), v.get("canonical_branch"), v.get("fallback_branch")
        if not all(is_int(x) and x >= 0 for x in (t, c, fbk)):
            fail("%s: would_move_total, canonical_branch and fallback_branch must be integers >= 0" % k)
        if c + fbk != t or t > s["nodes"]:
            fail("%s: canonical_branch + fallback_branch must equal would_move_total, not above the node count" % k)
        for key in ("canonical_tickers", "fallback_tickers"):
            tk = v.get(key)
            if not isinstance(tk, list) or len(tk) != len(set(tk)) or any(not re.fullmatch(r"[A-Z0-9.\-]{1,12}", str(x)) for x in tk):
                fail("%s: %s must be distinct public symbols (A-Z, 0-9, dot, dash, up to 12 characters)" % (k, key))
        if len(v["canonical_tickers"]) > c or len(v["fallback_tickers"]) > fbk:
            fail("%s: more distinct tickers than nodes on a branch" % k)
        if (c == 0) and v["canonical_tickers"]:
            fail("%s: canonical_tickers must be empty when no node moves on the canonical branch" % k)
        vs = v.get("vs_ib526") or {}
        if vs.get("upper_bound") != BOUNDS_526[k] or vs.get("delta") != t - BOUNDS_526[k]:
            fail("%s: vs_ib526 must state upper_bound %d and delta = would_move_total - upper_bound" % (k, BOUNDS_526[k]))
    print("OK: split consistent for 3 firms")


def packet_counters():
    r = load(REC2)
    f = ROOT / PACKET
    if not f.is_file():
        fail("no %s" % PACKET)
    txt = f.read_text(encoding="utf-8")
    if len(txt) < 3000:
        fail("the packet must be at least 3,000 characters")
    low = txt.lower()
    for w in ("branch a", "branch b", "blast radius", "rollback", "version", "coo half", "cto half", "fallback", "cash", "unsigned", "publish gate"):
        if w not in low:
            fail("the packet must state %r" % w)
    no_long_digits(txt)
    no_long_digits(json.dumps(r))
    for k in BOUND2:
        if r.get(k) != 0:
            fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
    for k, v in (r.get("firms") or {}).items():
        if not str(v.get("note", "")).strip():
            fail("%s: a note stating what the counts rest on and what was not read is required" % k)
    print("OK: packet and counters")


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    if cell == "IB189-1":
        {"AC1": build_ac1, "AC2": build_ac2, "AC3": build_ac3}[arm]()
    elif cell == "IB189-2":
        {"AC1": lambda: fdrxx("AC1"), "AC2": lambda: split("AC2"), "AC3": packet_counters}[arm]()
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
