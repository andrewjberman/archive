"""IRPT_BCKEND workstream ~PS round 2 and workstream ~PO round 2 (issuer 2.0.0_SA_COO~P2) -- the checks of the build cells and the Orion packet cell.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196 helpers (checks/r196/p196_cells.py, committed beside r200).

  IB200-1  IB-pr-553  hop 2 PLUMBING of the filled-report publisher: the object name, report_address(), the registry family row, a validating put, a default-OFF pass (BUILD)
  IB200-2  IB-pr-554  hop 3: the /report route, a NEW named-account reader, the scope refusal, the route declaration (BUILD)
  IB200-3  IB-pr-555  hop 4: the filled_report export source kind, additive (BUILD)
    AC1  the new tests and the existing tests of the package pass
    AC2  the difference control: with the cell's BEGIN/END block(s) removed from the product file(s) in memory, the new tests FAIL (assertion failures, not import errors)
    AC3  the record, the diff bounded to the cell's files, and the cell's own facts (the builder's address; the negative tests; additive-only)
  IB200-4  IB-pr-556  the Orion pairs (a) the 7-day positions re-pull and (b) the scheduled producer in the 6 AM ET fold: design record and packet, both halves UNSIGNED (READ ONLY)
    (see p200_orion.py)
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE))
import p196_cells as P6  # noqa: E402

D = P6.D
LAMBDA = "infra/aws/lambda/investor-reporting/"
TF = "infra/aws/terraform/investor-reporting/reporting-read/"
fail, load, is_int, counters, no_long_digits, git = P6.fail, P6.load, P6.is_int, P6.counters, P6.no_long_digits, P6.git

CELLS = {
    "1": dict(
        slot=397, test=LAMBDA + "reporting-publish/tests/test_filled_report_publish.py", min_tests=8,
        regress=[LAMBDA + "reporting-publish/tests/test_publisher.py", LAMBDA + "reporting-publish/tests/test_client_summary.py"],
        mutants=[LAMBDA + "reporting-publish/publisher.py"], marker="FILLED-REPORT-A",
        allowed={LAMBDA + "reporting-publish/publisher.py", LAMBDA + "reporting-publish/handler.py", "infra/logic/registry/reporting_policies.json",
                 LAMBDA + "reporting-publish/tests/test_filled_report_publish.py"},
        required={LAMBDA + "reporting-publish/publisher.py", "infra/logic/registry/reporting_policies.json", LAMBDA + "reporting-publish/tests/test_filled_report_publish.py"}),
    "2": dict(
        slot=398, test=LAMBDA + "reporting/tests/test_reporting_filled_report.py", min_tests=10,
        regress=[LAMBDA + "reporting/tests/test_reporting_entry.py", LAMBDA + "reporting/tests/test_reporting_summary.py"],
        mutants=[LAMBDA + "reporting/entry.py"], marker="FILLED-REPORT-B",
        allowed={LAMBDA + "reporting/entry.py", TF + "api.tf", TF + "locals.tf", LAMBDA + "reporting/tests/test_reporting_filled_report.py"},
        required={LAMBDA + "reporting/entry.py", TF + "api.tf", LAMBDA + "reporting/tests/test_reporting_filled_report.py"}),
    "3": dict(
        slot=399, test=LAMBDA + "export/tests/test_filled_report_source.py", min_tests=8,
        regress=[LAMBDA + "export/tests/test_export_path_b.py", LAMBDA + "export/tests/test_retained_export.py", LAMBDA + "export/tests/test_bundle_report_ref.py"],
        mutants=[LAMBDA + "export/bundle.py", LAMBDA + "export/retained_export.py"], marker="FILLED-REPORT-C",
        allowed={LAMBDA + "export/bundle.py", LAMBDA + "export/retained_export.py", LAMBDA + "export/tests/test_filled_report_source.py"},
        required={LAMBDA + "export/bundle.py", LAMBDA + "export/retained_export.py", LAMBDA + "export/tests/test_filled_report_source.py"}),
}
NEG_B = ("uncovered_viewer", "client_id_is_claim", "nested_accounts_named", "other_firm")
ALLOWED_PREFIX = (D, "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md")


def cfg(cid):
    return CELLS[cid.split("-")[0][-1]]


def record_path(c):
    n = {397: "IB200-1_record.json", 398: "IB200-2_record.json", 399: "IB200-3_record.json"}[c["slot"]]
    return D + "0.9.0_WK_IRPT_BCKEND~%d/%s" % (c["slot"], n)


def run_pytest(files, extra_env=None, runner=None):
    env = dict(os.environ, **(extra_env or {}))
    cmd = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *files] if runner is None else [sys.executable, runner, *files]
    p = subprocess.run(cmd, cwd=str(P6.ROOT), capture_output=True, text=True, timeout=110, env=env)
    return p.returncode, p.stdout + p.stderr


def build_ac1(c):
    for rel in [c["test"], *c["regress"], *c["mutants"]]:
        if not (P6.ROOT / rel).is_file():
            fail("no %s" % rel)
    rc, out = run_pytest([c["test"], *c["regress"]])
    m = re.search(r"(\d+) passed", out)
    if rc != 0 or not m:
        fail("the tests do not all pass:\n" + out[-600:])
    if (P6.ROOT / c["test"]).read_text(encoding="utf-8").count("def test_") < c["min_tests"]:
        fail("the new test file must hold at least %d tests" % c["min_tests"])
    print("OK: %s passed" % m.group(1))


RUNNER = (
    "import importlib.machinery as M, os, sys, json, pytest\n"
    "targets = json.loads(open(sys.argv[1], encoding='utf-8').read())\n"
    "targets = {os.path.normcase(os.path.abspath(k)): v for k, v in targets.items()}\n"
    "orig = M.SourceFileLoader.get_data\n"
    "def get_data(self, path):\n"
    "    p = os.path.normcase(os.path.abspath(path))\n"
    "    if p in targets:\n"
    "        return targets[p].encode('utf-8')\n"
    "    return orig(self, path)\n"
    "M.SourceFileLoader.get_data = get_data\n"
    "sys.dont_write_bytecode = True\n"
    "sys.exit(pytest.main(['-q', '-p', 'no:cacheprovider', sys.argv[2]]))\n")


def build_ac2(c):
    blocks_total, targets = 0, {}
    pat = re.compile(r"^[ \t]*# BEGIN %s\b.*?^[ \t]*# END %s\b[^\n]*\n" % (re.escape(c["marker"]), re.escape(c["marker"])), re.S | re.M)
    for rel in c["mutants"]:
        src = (P6.ROOT / rel).read_text(encoding="utf-8")
        found = pat.findall(src)
        blocks_total += len(found)
        targets[str((P6.ROOT / rel).resolve())] = pat.sub("", src)
    if blocks_total < 1:
        fail("the product file(s) must hold at least one BEGIN/END %s block" % c["marker"])
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "targets.json").write_text(json.dumps(targets), encoding="utf-8")
        (Path(td) / "run_mutant.py").write_text(RUNNER, encoding="utf-8")
        rc, out = run_pytest([str(Path(td) / "targets.json"), str((P6.ROOT / c["test"]).resolve())], {"PYTHONPYCACHEPREFIX": str(Path(td) / "pyc")},
                             runner=str(Path(td) / "run_mutant.py"))
    if rc == 0:
        fail("the new tests still pass with the %s block(s) removed: the tests cannot discriminate" % c["marker"])
    if not re.search(r"\d+ failed", out) or re.search(r"\d+ error", out):
        fail("the mutant run must fail on assertions, not on import or collection errors (rc %s):\n%s" % (rc, out[-500:]))
    print("OK: removing the block fails the new tests (%d block(s))" % blocks_total)


def own_changes(c, base):
    ser = "0.9.0_WK_IRPT_BCKEND~%d" % c["slot"]
    log = subprocess.run(["git", "-C", str(P6.ROOT), "log", "--no-merges", "--format=%H", "--author=" + ser, base + "..HEAD"], capture_output=True, text=True, timeout=60)
    if log.returncode != 0:
        fail("git log failed: " + log.stderr.strip()[:200])
    names = set()
    for sha in log.stdout.split():
        dt = subprocess.run(["git", "-C", str(P6.ROOT), "diff-tree", "--no-commit-id", "--name-only", "-r", sha], capture_output=True, text=True, timeout=60)
        if dt.returncode != 0:
            fail("git diff-tree failed: " + dt.stderr.strip()[:200])
        names.update(x for x in dt.stdout.splitlines() if x)
    return sorted(x for x in names if not x.startswith(ALLOWED_PREFIX))


def added_removed(base, paths):
    out = subprocess.run(["git", "-C", str(P6.ROOT), "diff", "-U0", base, "HEAD", "--", *paths], capture_output=True, text=True, timeout=60).stdout
    add = [x[1:] for x in out.splitlines() if x.startswith("+") and not x.startswith("+++")]
    rem = [x[1:] for x in out.splitlines() if x.startswith("-") and not x.startswith("---")]
    return add, rem


def build_ac3(c, which):
    r = load(record_path(c))
    base = r.get("base_commit", "")
    if not re.fullmatch(r"[0-9a-f]{40}", base):
        fail("base_commit must be 40 hex")
    changed = own_changes(c, base)
    if sorted(r.get("changed_paths", [])) != changed:
        fail("changed_paths differs from the worker's own commits since base (deliverables and the channel aside)")
    stray = [x for x in changed if x not in c["allowed"]]
    if stray:
        fail("paths outside the grant: %r" % stray[:4])
    missing = sorted(c["required"] - set(changed))
    if missing:
        fail("these files must change: %r" % missing[:4])
    if not is_int(r.get("tests_total")) or r.get("tests_passed") != r.get("tests_total") or not is_int(r.get("mutant_tests_failed")) or r["mutant_tests_failed"] < 1:
        fail("tests_total equal to tests_passed and mutant_tests_failed >= 1 must be recorded")
    prod_py = [x for x in changed if x.endswith(".py") and "/tests/" not in x]
    add, rem = added_removed(base, prod_py)
    if any(re.search(r"s3://|opal-data-|irpt/(49financial|cottonwood|inflection)/", x) for x in add):
        fail("a typed object address in a product file: addresses are the builder's output (rule 30)")
    if which == "1":
        if r.get("default_off") is not True:
            fail("default_off must be true: the scheduled pass stays off until activation")
        ex = r.get("address_example")
        root = os.environ.get("P200_NAMING_ROOT") or str(P6.ROOT)
        p = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); from lib import opal_naming as n; print(n.address('irpt','49financial','platinum','reporting','client=PLACEHOLDER','filled_report.json'))", root],
                           capture_output=True, text=True, timeout=60)
        if p.returncode != 0 or ex != p.stdout.strip():
            fail("address_example must equal the naming builder's output for client=PLACEHOLDER: %r" % p.stdout.strip()[:160])
        reg = (P6.ROOT / "infra/logic/registry/reporting_policies.json").read_text(encoding="utf-8")
        if "filled_report" not in reg:
            fail("the registry family row for the filled report must be in reporting_policies.json")
    elif which == "2":
        neg = r.get("negative_tests")
        txt = (P6.ROOT / c["test"]).read_text(encoding="utf-8")
        if not isinstance(neg, list) or not set(NEG_B) <= set(neg):
            fail("negative_tests must list %r" % (NEG_B,))
        for n in NEG_B:
            if not re.search(r"def test_\w*%s\w*\(" % n, txt):
                fail("the new test file has no test named for %s" % n)
        ent = (P6.ROOT / (LAMBDA + "reporting/entry.py")).read_text(encoding="utf-8")
        tf = (P6.ROOT / (TF + "api.tf")).read_text(encoding="utf-8")
        if "client/{client_id}/report" not in ent or "client/{client_id}/report" not in tf:
            fail("the route template must be in entry.py and declared in api.tf")
        was = subprocess.run(["git", "-C", str(P6.ROOT), "show", "%s:%s" % (base, TF + "api.tf")], capture_output=True, text=True, timeout=60).stdout
        if tf.count('resource "aws_apigatewayv2_route"') != was.count('resource "aws_apigatewayv2_route"') + 1:
            fail("exactly one new aws_apigatewayv2_route resource is declared")
    else:
        if r.get("existing_kinds_untouched") is not True or not is_int(r.get("removed_lines")) or r["removed_lines"] != len(rem) or len(rem) > 6:
            fail("existing_kinds_untouched true; removed_lines equal to the diff's removed lines (%d) and at most 6" % len(rem))
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: record, diff bounded, the cell's facts")


import p200_orion as PO  # noqa: E402

CHECKS = {}
for _n in ("1", "2", "3"):
    CHECKS["IB200-%s-AC1" % _n] = (lambda n=_n: build_ac1(CELLS[n]))
    CHECKS["IB200-%s-AC2" % _n] = (lambda n=_n: build_ac2(CELLS[n]))
    CHECKS["IB200-%s-AC3" % _n] = (lambda n=_n: build_ac3(CELLS[n], n))
CHECKS.update(PO.CHECKS)

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p200_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
