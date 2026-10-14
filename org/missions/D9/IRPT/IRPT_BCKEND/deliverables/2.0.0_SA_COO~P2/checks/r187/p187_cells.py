"""IRPT_BCKEND round 187 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB187-1  IB-pr-523  Design (B) of the 49F activity backfill: the reporting-gold backfill event can select its stages, so an activity-and-lots-only run never touches the returns or class partitions (BUILD ONLY)
    AC1  the folder's offline tests pass (the pre-existing 90 and at least 5 new in tests/test_backfill_stages.py), and the change is confined: only handler.py and the new test file changed under reporting-gold, in the functions the design names
    AC2  the lots-only arm: a backfill event with stages ["lots"] calls neither compute, nor the returns emit, nor the class emit, and calls the lots emit once for the declared days and accounts; the result names its stages
    AC3  the default and refusal arms: an event without stages runs exactly the calls it ran before (compute, returns emit, class emit, lots emit); an unknown stage, an empty list, a returns-only list and a stages key on a non-backfill event are refused by name
  IB187-2  IB-pr-524  the landed transaction sources of Cottonwood and Inflection and their mapping to the account_activity_daily shape (READ ONLY)
    AC1  the shape: the table's columns read from the producer's own schema, and per firm the landed transaction source (vendor, tables, partitions, earliest and latest day)
    AC2  the mapping: every shape column of the table accounted for per firm as MAPPED, DERIVED or ABSENT with its source column or its stated reason; the unmapped list consistent with the statuses
    AC3  the note and the counters: the per-firm reading of whether the shape can be produced, no estimate presented as a measure, no long digit run, the six bound counters 0
"""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

RG = "infra/aws/lambda/investor-reporting/reporting-gold"
D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
REC2 = D + "0.9.0_WK_IRPT_BCKEND~371/IB187-2_transaction_source_mapping.json"
BOUND2 = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
NEWEST = "2026-10-01"
BASE_BLOB = "fe08ad501aa9503cc56a2ef65249283dcc696ead"
BASE_TESTS = ["test_activity_lot_emission.py", "test_backfill_mode.py", "test_class_catch_up.py", "test_class_table_emission.py", "test_day_selection.py", "test_handler_passes_src.py", "test_lots_status.py", "test_population_account_set.py"]
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB187"))
    sys.exit(1)


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_date(x):
    return isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) is not None


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT)] + list(args), capture_output=True, text=True)


def build_ac1():
    gold = ROOT / RG
    if not (gold / "handler.py").is_file():
        fail("no %s/handler.py" % RG)
    newt = gold / "tests" / "test_backfill_stages.py"
    if not newt.is_file() or newt.read_text(encoding="utf-8").count("def test_") < 5:
        fail("tests/test_backfill_stages.py must exist with at least 5 tests")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests"], cwd=str(gold), capture_output=True, text=True,
                       env=dict(__import__("os").environ, PYTHONDONTWRITEBYTECODE="1"), timeout=110)
    m = re.search(r"(\d+) passed", r.stdout)
    if r.returncode != 0 or not m or int(m.group(1)) < 95:
        fail("pytest of the folder must pass with at least 95 tests (90 pre-existing + 5 new): rc %s %s" % (r.returncode, (r.stdout + r.stderr)[-200:]))
    # the change is confined: the test files are the baseline eight plus the new one, and handler.py differs from its base blob
    # (content-addressed, so this holds on any branch) only inside the functions the design names
    tests = sorted(p.name for p in (gold / "tests").glob("test_*.py"))
    want_tests = sorted(BASE_TESTS + ["test_backfill_stages.py"])
    if tests != want_tests:
        fail("tests/ must hold exactly the baseline files plus test_backfill_stages.py; found %s" % tests)
    if git("cat-file", "-e", BASE_BLOB).returncode == 0:
        import os
        import tempfile
        fd, tmp = tempfile.mkstemp(prefix="p187base_", suffix=".py")
        try:
            os.write(fd, subprocess.run(["git", "-C", str(ROOT), "cat-file", "-p", BASE_BLOB], capture_output=True).stdout)
            os.close(fd)
            d = subprocess.run(["git", "diff", "--no-index", "-U0", tmp, str(gold / "handler.py")], capture_output=True, text=True, cwd=str(ROOT)).stdout
        finally:
            os.remove(tmp)
        labels = set()
        for ln in d.splitlines():
            mm = re.match(r"@@ [^@]+ @@\s*(.*)$", ln)
            if mm:
                lab = mm.group(1).strip()
                labels.add(re.sub(r"^def\s+(\w+).*", r"\1", lab) if lab.startswith("def ") else lab)
        allowed = {"backfill_days", "run_backfill", "run", ""}
        if not d.strip():
            fail("handler.py equals its base blob: the design's change is absent")
        if not labels <= allowed:
            fail("handler.py hunks may sit only in %s; found %s" % (sorted(allowed), sorted(labels)))
    print("OK: %s tests pass; the change is confined" % m.group(1))


def _patches(h, calls, frame_days):
    import pandas as pd

    def compute(s3, days, accounts, thresholds, workers=12):
        calls.append(("compute", list(days)))
        return pd.DataFrame([{"business_date": d, "account_id": a} for d in days for a in accounts]), "49financial", "2020-01-01"

    def emit_day(s3, part, firm, day, upload=True, thresholds=None, first_data_date=None, src=None):
        calls.append(("emit_day", day))
        return {"rows": len(part), "landed": upload}

    def emit_classes(s3, firm, days, upload=True):
        calls.append(("emit_classes", list(days)))
        return {}, {}

    def emit_lots(s3, firm, days, accounts, upload=True, workers=12):
        calls.append(("emit_lots", list(days), list(accounts)))
        return {d: 1 for d in days}, {}

    return [
        mock.patch.object(h.ard, "load_declaration", lambda: {}),
        mock.patch.object(h.ard, "declared_sources", lambda doc: ["src"]),
        mock.patch.object(h.ard, "source_entry", lambda doc, s: {}),
        mock.patch.object(h.ard, "firm_scope", lambda src: "49financial"),
        mock.patch.object(h, "_gold_location", lambda firm: ("b", "p/")),
        mock.patch.object(h, "newest_landed_day", lambda s3, b, p: NEWEST),
        mock.patch.object(h, "population_accounts", lambda s3, firm: (NEWEST, ["P1", "P2"])),
        mock.patch.object(h, "newest_accounts", lambda s3, b, p, d: ["P1"]),
        mock.patch.object(h, "load_thresholds", lambda: {"t": 1}),
        mock.patch.object(h, "compute", compute),
        mock.patch.object(h.ard, "emit_day", emit_day),
        mock.patch.object(h, "emit_classes", emit_classes),
        mock.patch.object(h, "emit_lots", emit_lots),
        mock.patch.object(h, "record_lots_status", lambda *a, **k: None),
    ]


def _run(event):
    gold = str(ROOT / RG)
    if gold not in sys.path:
        sys.path.insert(0, gold)
    for name in [m for m in sys.modules if m == "handler"]:
        del sys.modules[name]
    import handler as h
    calls = []
    stack = _patches(h, calls, None)
    for p in stack:
        p.start()
    try:
        out = h.run(object(), "2026-10-02", event)
        return out, calls, None
    except SystemExit as e:
        return None, calls, str(e)
    finally:
        for p in reversed(stack):
            p.stop()


def build_ac2():
    ev = {"backfill": {"start": "2026-09-28", "end": "2026-09-30"}, "accounts": "population", "stages": ["lots"]}
    out, calls, refused = _run(ev)
    if refused is not None:
        fail("a lots-only backfill event was refused: %s" % refused[:200])
    names = [c[0] for c in calls]
    if "compute" in names or "emit_day" in names or "emit_classes" in names:
        fail("a lots-only run must not call compute, the returns emit or the class emit; calls: %s" % names)
    lots = [c for c in calls if c[0] == "emit_lots"]
    if len(lots) != 1 or lots[0][1] != ["2026-09-28", "2026-09-29", "2026-09-30"] or not lots[0][2]:
        fail("a lots-only run must call the lots emit once for the three declared days and a non-empty account set: %s" % lots)
    if not isinstance(out, dict) or out.get("stages") != ["lots"]:
        fail("the result must name its stages ['lots']: %s" % (out if not isinstance(out, dict) else out.get("stages")))
    print("OK: the lots-only arm touches neither the returns nor the class emit")


def build_ac3():
    ev = {"backfill": {"start": "2026-09-28", "end": "2026-09-30"}, "accounts": "population"}
    out, calls, refused = _run(ev)
    if refused is not None:
        fail("the default backfill event was refused: %s" % refused[:200])
    names = [c[0] for c in calls]
    want = ["compute", "emit_day", "emit_day", "emit_day", "emit_classes", "emit_lots"]
    if names != want:
        fail("the default backfill must run exactly %s, ran %s" % (want, names))
    for label, extra in (("an unknown stage", {"stages": ["lots", "nonsense"]}), ("an empty list", {"stages": []}), ("a returns-only list", {"stages": ["returns"]}),
                         ("a string", {"stages": "lots"})):
        ev2 = dict(ev, **extra)
        out2, calls2, refused2 = _run(ev2)
        if refused2 is None or "REFUSED" not in refused2 or "stages" not in refused2.lower():
            fail("%s must be refused by name (REFUSED ... stages): %s" % (label, refused2))
        if calls2:
            fail("%s must be refused before any call; calls: %s" % (label, [c[0] for c in calls2]))
    out3, calls3, refused3 = _run({"accounts": ["P1"], "stages": ["lots"]})
    if refused3 is None or "REFUSED" not in refused3:
        fail("a stages key on a non-backfill event must be refused by name: %s" % refused3)
    print("OK: the default path is unchanged; four malformed stage values and a non-backfill stages key are refused by name")


def read_arms(arm):
    f = ROOT / REC2
    if not f.is_file():
        fail("no %s" % REC2)
    try:
        r = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (REC2, e))
    cols = r.get("shape_columns")
    if not isinstance(cols, list) or len(cols) < 3 or not all(isinstance(c, str) and c for c in cols) or len(set(cols)) != len(cols):
        fail("shape_columns must be a list of at least 3 distinct column names read from the producer's own schema")
    firms = r.get("firms") or {}
    if sorted(firms) != ["cottonwood", "inflection"]:
        fail("firms must hold exactly cottonwood and inflection")
    if arm == "AC1":
        if not str(r.get("shape_source", "")).strip():
            fail("shape_source (the file and symbol the columns were read from) is required")
        for k, v in firms.items():
            s = v.get("transaction_source") or {}
            if not (str(s.get("vendor", "")).strip() and isinstance(s.get("tables"), list) and s["tables"] and is_int(s.get("partitions")) and s["partitions"] >= 0):
                fail("%s: transaction_source needs a vendor, a non-empty tables list and an integer partitions" % k)
            if s["partitions"] > 0 and not (is_date(s.get("earliest")) and is_date(s.get("latest")) and s["earliest"] <= s["latest"]):
                fail("%s: a source with partitions needs earliest and latest dates (earliest <= latest)" % k)
        print("OK: %d shape columns; two firms' transaction sources read" % len(cols))
    elif arm == "AC2":
        for k, v in firms.items():
            mp = v.get("mapping")
            if not isinstance(mp, list):
                fail("%s: mapping must be a list" % k)
            seen = {}
            for m in mp:
                col, st = m.get("shape_column"), m.get("status")
                if col not in cols or col in seen:
                    fail("%s: each mapping row must name one shape column once: %r" % (k, col))
                if st not in ("MAPPED", "DERIVED", "ABSENT"):
                    fail("%s: %s status must be MAPPED, DERIVED or ABSENT" % (k, col))
                if st in ("MAPPED", "DERIVED") and not str(m.get("source", "")).strip():
                    fail("%s: %s is %s and needs its source (a column or a rule)" % (k, col, st))
                if st == "ABSENT" and not str(m.get("reason", "")).strip():
                    fail("%s: %s is ABSENT and needs its stated reason" % (k, col))
                seen[col] = st
            if set(seen) != set(cols):
                fail("%s: the mapping must account for every shape column; missing %s" % (k, sorted(set(cols) - set(seen))))
            unm = v.get("unmapped_columns")
            if sorted(unm or []) != sorted(c for c, st in seen.items() if st == "ABSENT"):
                fail("%s: unmapped_columns must equal the ABSENT columns" % k)
        print("OK: every shape column accounted for in both firms")
    else:
        for k, v in firms.items():
            if v.get("can_produce_shape") not in ("YES", "PARTIAL", "NO"):
                fail("%s: can_produce_shape must be YES, PARTIAL or NO" % k)
            if not str(v.get("note", "")).strip():
                fail("%s: a note stating the reading and what was not measured is required" % k)
            if (v["can_produce_shape"] == "YES") != (not v.get("unmapped_columns")):
                fail("%s: YES if and only if no column is ABSENT" % k)
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
            fail("the record carries a long digit run")
        for k in BOUND2:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        print("OK: readings and counters")


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    if cell == "IB187-1":
        {"AC1": build_ac1, "AC2": build_ac2, "AC3": build_ac3}[arm]()
    elif cell == "IB187-2":
        read_arms(arm)
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    unittest.TestCase.maxDiff = None
    main()
