"""IRPT_BCKEND round 190 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of three orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB190-1  IB-pr-529  the IR cash rule on the FALLBACK layer too: the one apply_cash_rule is also called at the bd-securities fallback return of classify_security (BUILD ONLY, offline)
    AC1  the classification set passes (the 107 at base, one rewritten, and at least 3 new in tests/test_holdings_cash_rule.py: 109 or more), the tests folder is unchanged in its file list, and holdings_snapshot.py differs from its base blob only in classify_security and the rule's docstring
    AC2  the behaviour: a fallback-only fund whose sub is Cash (table basis, name-alias basis) serves cash with its sub, basis and fallback class_source; a canonical Cash row still serves cash; equity, Money Market and null-sub rows on both layers are untouched; the CASH-line rule is unchanged
    AC3  one definition, exactly two calls inside classify_security (one before the fallback answer line, one after), none elsewhere; the admitted class enum unchanged
  IB190-2  IB-pr-530  the directory exemption repair: the all-UNKNOWN test reads source-marked statuses only and ignores the entries the directory builder carries forward (BUILD ONLY, offline)
    AC1  the classification set passes (the 107 at base and at least 4 new in tests/test_directory_exemption_source_marks.py), the tests folder holds the baseline plus that file, and holdings_snapshot.py differs from its base blob only in the directory-reading functions
    AC2  the function arms: all UNKNOWN true; UNKNOWN plus carried TERMINATED true; UNKNOWN plus a source-marked TERMINATED false; an ACTIVE entry false; no directory or an empty one false; only carried entries false
    AC3  the replay through the real gate: a Cottonwood-shaped directory (many UNKNOWN entries and two carried TERMINATED ones) lets a candidate with one lost account PUBLISH, listing the account; the same candidate is still refused when another worse condition holds or when the directory marks a closure at the source
  IB190-3  IB-pr-531  the producer census (READ ONLY): how the holdings producer is deployed and scheduled, its code hash, and its rollback by manifest version per firm
    AC1  the producer: the runner, its dispatch, the schedule (name, state, expression, target) and, per firm, the served standalone bundle (key shape, version id, sha256, last modified, member count, whether it carries apply_cash_rule)
    AC2  the release path and the rollback: the deploy tool and its ledger rule named, and per firm the current manifest key's version id and last-modified date
    AC3  the S71 reconciliation, the notes and the counters: the missing-member finding against the fact that scheduled fires wrote records, no client identifier, no long digit run, the six bound counters 0
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
BASE_BLOB = "e3d733821efe43856018259e0d2747f43bb4357d"
BASE_ENUM = ("equity", "fixed_income", "alternatives", "cash", "other", "structured", "commodities", "unclassified")
SET9 = ["test_holdings_classification.py", "test_holdings_cusip_fallback.py", "test_holdings_narrowed.py", "test_holdings_unclassified.py",
        "test_holdings_snapshot.py", "test_holdings_publish_gate.py", "test_holdings_multi_asset_v1_enum.py", "test_holdings_display.py",
        "test_holdings_cash_rule.py"]
BASE_TESTS = ["test_build_refuses_planted_member.py", "test_bundle_manifest_stamp.py", "test_cot_account_mapping.py", "test_directory_account_masks.py",
              "test_directory_runner.py", "test_directory_runner_refuse_drop.py", "test_directory_runner_source_principal.py",
              "test_directory_runner_terminated.py", "test_economic_regressions.py", "test_holdings_49f.py", "test_holdings_49f_account_id.py",
              "test_holdings_cash_rule.py", "test_holdings_classification.py", "test_holdings_cusip_fallback.py", "test_holdings_display.py",
              "test_holdings_inf.py", "test_holdings_membership.py", "test_holdings_multi_asset_v1_enum.py", "test_holdings_narrowed.py",
              "test_holdings_publish_gate.py", "test_holdings_rearm_trigger.py", "test_holdings_snapshot.py", "test_holdings_unclassified.py",
              "test_holdouts.py", "test_inf_positions.py", "test_l0_categories.py", "test_retained_capture_cleanup.py",
              "test_runner_jsonschema_tolerance.py", "test_schwab_codes.py", "test_smartx_valuation.py", "test_source_inputs.py",
              "test_tax_membership_once.py", "test_vendor_keys.py"]
NEWT2 = "test_directory_exemption_source_marks.py"
REC3 = D + "0.9.0_WK_IRPT_BCKEND~378/IB190-3_producer_census.json"
BOUND = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
FIRMS = ["49financial", "cottonwood", "inflection"]
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB190"))
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


def hunk_labels():
    if git("cat-file", "-e", BASE_BLOB).returncode != 0:
        return None
    fd, tmp = tempfile.mkstemp(prefix="p190base_", suffix=".py")
    try:
        os.write(fd, subprocess.run(["git", "-C", str(ROOT), "cat-file", "-p", BASE_BLOB], capture_output=True).stdout)
        os.close(fd)
        d = subprocess.run(["git", "diff", "--no-index", "-U0", tmp, str(ROOT / HS)], capture_output=True, text=True, cwd=str(ROOT)).stdout
    finally:
        os.remove(tmp)
    if not d.strip():
        fail("holdings_snapshot.py equals its base blob: the change is absent")
    labels = set()
    for ln in d.splitlines():
        mm = re.match(r"@@ [^@]+ @@\s*(.*)$", ln)
        if mm:
            lab = mm.group(1).strip()
            labels.add(re.sub(r"^def\s+(\w+).*", r"\1", lab) if lab.startswith("def ") else lab)
    return labels


def tests_ac1(newfile, minimum, allowed_labels, label):
    gold = ROOT / HS_DIR
    want_tests = sorted(BASE_TESTS + ([newfile] if newfile else []))
    if newfile:
        nt = gold / "tests" / newfile
        if not nt.is_file() or nt.read_text(encoding="utf-8").count("def test_") < 4:
            fail("tests/%s must exist with at least 4 test functions" % newfile)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + ["tests/" + n for n in SET9 + ([newfile] if newfile else [])],
                       cwd=str(gold), capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), timeout=170)
    m = re.search(r"(\d+) passed", r.stdout)
    if r.returncode != 0 or not m or int(m.group(1)) < minimum or " failed" in r.stdout:
        fail("pytest of the classification set must pass with at least %d tests: rc %s %s" % (minimum, r.returncode, (r.stdout + r.stderr)[-200:]))
    tests = sorted(p.name for p in (gold / "tests").glob("test_*.py"))
    if tests != want_tests:
        fail("tests/ must hold exactly the baseline files%s; found %s" % (" plus " + newfile if newfile else "", tests))
    labels = hunk_labels()
    if labels is not None and not labels <= allowed_labels:
        fail("holdings_snapshot.py hunks may sit only at %s; found %s" % (sorted(allowed_labels), sorted(labels)))
    print("OK: %s tests pass; the change is confined (%s)" % (m.group(1), label))


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


def b1_ac2():
    hs, ec = _hs()
    canon = {"FDRXX": {"asset_class": "fixed_income", "sub_asset_class": "Cash"},
             "SPY": {"asset_class": "equity", "sub_asset_class": "US Large Cap"},
             "MMKT": {"asset_class": "fixed_income", "sub_asset_class": "Money Market"}}
    fb = [{"ticker": "FBCSH", "asset_class": "fixed_income", "sub_asset_class": "Cash", "name_aliases": {"FALLBACK CASH FUND"}},
          {"ticker": "FBMM", "asset_class": "fixed_income", "sub_asset_class": "Money Market"},
          {"ticker": "FBEQ", "asset_class": "equity", "sub_asset_class": "US Large Cap"},
          {"ticker": "FBNS", "asset_class": "fixed_income", "sub_asset_class": None},
          {"ticker": "FBLOW", "asset_class": "fixed_income", "sub_asset_class": " cash "}]
    clf = _Clf(ec, canon, fb)
    ccs, fcs = hs.CANONICAL_CLASS_SOURCE, hs.FALLBACK_CLASS_SOURCE

    def one(ticker, name, **kw):
        return hs.classify_security(ec, clf, ticker, name, **kw)

    g = one("FBCSH", "ANY NAME")
    if g["asset_class"] != "cash" or g["sub_asset_class"] != "Cash" or g["asset_class_basis"] != "TABLE" or g["class_source"] != fcs:
        fail("a fallback table row with sub Cash must serve cash with its sub, basis TABLE and the fallback class_source: %r" % g)
    g = one(None, "FALLBACK CASH FUND")
    if g["asset_class"] != "cash" or g["asset_class_basis"] != "NAME_ALIAS" or g["class_source"] != fcs:
        fail("a fallback name-alias row with sub Cash must serve cash with basis NAME_ALIAS: %r" % g)
    if one("FBLOW", "X")["asset_class"] != "cash":
        fail("a padded lower-case cash sub on the fallback layer must serve cash")
    for t, want in (("FBMM", "fixed_income"), ("FBEQ", "equity"), ("FBNS", "fixed_income")):
        g = one(t, "X")
        if g["asset_class"] != want or g["class_source"] != fcs:
            fail("fallback %s must stay %s: %r" % (t, want, g))
    g = one("FDRXX", "X")
    if g["asset_class"] != "cash" or g["class_source"] != ccs:
        fail("a canonical Cash row must still serve cash: %r" % g)
    for t, want in (("SPY", "equity"), ("MMKT", "fixed_income")):
        if one(t, "X")["asset_class"] != want:
            fail("canonical %s must stay %s" % (t, want))
    g = one("CASH", "CASH", description="CASH")
    if g["asset_class"] != "cash" or g["asset_class_basis"] != "NAME_PATTERN":
        fail("the Pathward CASH-line rule must be unchanged: %r" % g)
    print("OK: the rule acts on both layers, on a Cash sub only")


def b1_ac3():
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
    if len(calls) != 2:
        fail("classify_security must call %s exactly twice (canonical and fallback returns); found %d" % (name, len(calls)))
    fb_line = None
    for n in ast.walk(cs[0]):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "answer" for t in n.targets):
            fb_line = n.lineno
    lines = sorted(c.lineno for c in calls)
    if fb_line is None or not (lines[0] < fb_line < lines[1]):
        fail("one call must sit before the fallback answer line (canonical) and one after it (fallback)")
    other = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name and n not in calls]
    if other:
        fail("%s must not be called anywhere else" % name)
    hs, _ec = _hs()
    if tuple(hs.ASSET_CLASS_VALUES) != BASE_ENUM:
        fail("ASSET_CLASS_VALUES must be unchanged")
    print("OK: one definition, two calls, none elsewhere")


def _entry(ind, carried=False, acc="a"):
    e = {"ids": {"account_ids": [acc]}, "termination": {"indicator": ind}}
    if carried:
        e["termination"]["effective_date"] = "2026-10-08"
        e["cohort"] = {"capability_facts": ["cot:relationship-grain ships on every custody row", "source_removed_on=2026-10-08 carried against the previous directory"]}
    else:
        e["cohort"] = {"capability_facts": ["termination: cottonwood fact_allocations carries no account status column at this vintage -> UNKNOWN, never defaulted to ACTIVE"]}
    return e


def b2_ac2():
    hs, _ec = _hs()
    orig = hs._directory_entries

    def run(entries):
        hs._directory_entries = lambda s3, bucket: entries
        try:
            return hs.directory_marks_no_closures(None, "b", "cottonwood")
        finally:
            hs._directory_entries = orig

    unk = [_entry("UNKNOWN", acc="u%d" % i) for i in range(5)]
    arms = [("all UNKNOWN", unk, True),
            ("UNKNOWN plus carried TERMINATED", unk + [_entry("TERMINATED", True, "c1"), _entry("TERMINATED", True, "c2")], True),
            ("UNKNOWN plus a source-marked TERMINATED", unk + [_entry("TERMINATED", False, "s1")], False),
            ("UNKNOWN plus carried plus a source-marked TERMINATED", unk + [_entry("TERMINATED", True, "c1"), _entry("TERMINATED", False, "s1")], False),
            ("UNKNOWN plus an ACTIVE entry", unk + [_entry("ACTIVE", False, "x1")], False),
            ("no directory", None, False), ("an empty directory", [], False),
            ("only carried TERMINATED entries", [_entry("TERMINATED", True, "c1"), _entry("TERMINATED", True, "c2")], False)]
    for label, ents, want in arms:
        got = run(ents)
        if got is not want:
            fail("directory_marks_no_closures(%s) must be %s, was %s" % (label, want, got))
    print("OK: the exemption reads source-marked statuses only")


def b2_ac3():
    tdir = str(ROOT / HS_DIR / "tests")
    hsd = str(ROOT / HS_DIR)
    for p in (hsd, tdir):
        if p not in sys.path:
            sys.path.insert(0, p)
    for name in [m for m in sys.modules if m in ("holdings_snapshot", "bd_securities_fallback", "test_holdings_publish_gate")]:
        del sys.modules[name]
    import test_holdings_publish_gate as pg
    from _pytest.monkeypatch import MonkeyPatch
    hs = pg.hs

    def write_dir(s3, entries):
        bucket = hs.firm_bucket_map()[pg.FIRM]
        prefix = hs.PROD_PREFIX.replace("holdings", "directory")
        s3.put_object(Bucket=bucket, Key=prefix + "/latest.json", Body=json.dumps({"key": prefix + "/d.json"}).encode())
        s3.put_object(Bucket=bucket, Key=prefix + "/d.json", Body=json.dumps({"entries": entries}).encode())

    unk = [_entry("UNKNOWN", acc="acc1")] + [_entry("UNKNOWN", acc="u%d" % i) for i in range(20)]
    carried = [_entry("TERMINATED", True, "cx1"), _entry("TERMINATED", True, "cx2")]
    book = {"acc1": [("AAA", "equity", 60.0), ("BBB", "fixed_income", 40.0)]}
    with MonkeyPatch.context() as mp:
        s3 = pg.seeded(mp)
        write_dir(s3, unk + [_entry("UNKNOWN", acc="acc2")] + carried)
        before = pg.index_ref(s3)
        result = pg.fire(mp, s3, pg.make_snapshot(book, date=pg.DATE1, stamp="2026-10-09T10:15:00Z"))
        gate = result["publish_gate"]
        if gate["outcome"] != "PUBLISHED" or gate["conditions"] != [] or gate["listed"].get("account_lost_not_refused", {}).get("ids") != ["acc2"] \
                or pg.index_ref(s3) == before:
            fail("a directory of UNKNOWN entries plus carried TERMINATED ones must let the candidate PUBLISH, listing the lost account: %r" % (gate,))
    with MonkeyPatch.context() as mp:
        s3 = pg.seeded(mp, date=pg.DATE1)
        write_dir(s3, unk + [_entry("UNKNOWN", acc="acc2")] + carried)
        g = pg.refused(mp, s3, pg.make_snapshot(book, date=pg.DATE0, stamp="2026-10-09T10:15:00Z"), "source_frontier_older")
        if g["listed"].get("account_lost_not_refused", {}).get("ids") != ["acc2"]:
            fail("another worse condition must still refuse while the lost account is listed")
    with MonkeyPatch.context() as mp:
        s3 = pg.seeded(mp, book={"acc1": [("AAA", "equity", 100.0)], "acc2": [("CCC", "cash", 50.0)], "acc3": [("EEE", "equity", 25.0)]})
        write_dir(s3, unk + [_entry("UNKNOWN", acc="acc3"), _entry("TERMINATED", False, "acc2")] + carried)
        g = pg.refused(mp, s3, pg.make_snapshot({"acc1": [("AAA", "equity", 100.0)]}, date=pg.DATE1), "account_lost")
        if g["conditions"][0]["ids"] != ["acc3"] or "account_lost_not_refused" in g["listed"]:
            fail("where the source marks a closure the lost unmarked account must still be refused")
    print("OK: the replay publishes, listing the lost account; the refusals hold")


def census(arm):
    r = load(REC3)
    p = r.get("producer") or {}
    if arm == "AC1":
        for k in ("runner", "dispatch"):
            if not str(p.get(k, "")).strip():
                fail("producer.%s is required" % k)
        s = p.get("schedule") or {}
        if not str(s.get("name", "")).strip() or s.get("state") not in ("ENABLED", "DISABLED") or not str(s.get("expression", "")).strip() or not str(s.get("target", "")).strip():
            fail("producer.schedule needs name, state (ENABLED or DISABLED), expression and target")
        b = p.get("bundles") or {}
        if sorted(b) != FIRMS:
            fail("producer.bundles must hold exactly the three firms")
        for k, v in b.items():
            if not (str(v.get("key_shape", "")).strip() and str(v.get("version_id", "")).strip() and re.fullmatch(r"[0-9a-f]{64}", str(v.get("sha256", "")))
                    and str(v.get("last_modified", "")).strip() and is_int(v.get("members")) and v["members"] > 0 and isinstance(v.get("has_apply_cash_rule"), bool)):
                fail("%s: a bundle needs key_shape, version_id, a 64-hex sha256, last_modified, members above 0 and has_apply_cash_rule true or false" % k)
    elif arm == "AC2":
        rp = r.get("release_path") or {}
        if not (str(rp.get("deploy_tool", "")).strip() and isinstance(rp.get("ledger_required"), bool) and str(rp.get("rollback", "")).strip()):
            fail("release_path needs deploy_tool, ledger_required (true or false) and rollback")
        rb = r.get("rollback_by_manifest_version") or {}
        if sorted(rb) != FIRMS:
            fail("rollback_by_manifest_version must hold exactly the three firms")
        for k, v in rb.items():
            if not (str(v.get("manifest_key", "")).endswith("current/manifest.json") and str(v.get("version_id", "")).strip() and is_date(str(v.get("last_modified", ""))[:10])):
                fail("%s: a manifest key ending current/manifest.json, its version_id and a last_modified date are required" % k)
    else:
        s71 = r.get("s71_reconciliation") or {}
        if not (is_int(s71.get("missing_member_count")) and s71["missing_member_count"] >= 0 and isinstance(s71.get("scheduled_fires_wrote_records"), bool)
                and str(s71.get("reading", "")).strip()):
            fail("s71_reconciliation needs missing_member_count, scheduled_fires_wrote_records (true or false) and a reading")
        no_long_digits(json.dumps(r))
        for k in BOUND:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        if not (isinstance(r.get("notes"), list) and r["notes"] and all(str(n).strip() for n in r["notes"])):
            fail("notes (what each fact rests on and what was not read) are required")
    print("OK: census %s" % arm)


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    if cell == "IB190-1":
        {"AC1": lambda: tests_ac1(None, 109, {"classify_security", "apply_cash_rule", "cusip_key", ""}, "classify_security"), "AC2": b1_ac2, "AC3": b1_ac3}[arm]()
    elif cell == "IB190-2":
        {"AC1": lambda: tests_ac1(NEWT2, 111, {"_directory_entries", "closed_account_ids", "directory_marks_no_closures", ""}, "directory reading"),
         "AC2": b2_ac2, "AC3": b2_ac3}[arm]()
    elif cell == "IB190-3":
        census(arm)
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
