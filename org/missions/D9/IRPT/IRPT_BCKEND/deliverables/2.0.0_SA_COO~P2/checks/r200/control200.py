"""Positive control and negatives for p200_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control200.py <real_repo_root>
Builds a temp git root with stub packages at the real relative paths (a base commit; a worker commit by each cell's worker serial adding marker blocks, new
tests and records), a synthetic Orion design record and packet, runs every criterion expecting PASS, then applies each mutation expecting the NAMED
criterion to FAIL. The naming builder is read from the REAL root (P200_NAMING_ROOT). The temp roots are removed.
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
CHECK = REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r200/p200_cells.py"
sys.path.insert(0, str(CHECK.parent.parent / "r196"))
sys.path.insert(0, str(CHECK.parent))
import p200_cells as P  # noqa: E402
import p200_orion as PO  # noqa: E402

P6 = P.P6
os.environ["P200_NAMING_ROOT"] = str(REAL)
BS = chr(92)


def git(root, *a, env=None):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True, env=env).stdout.strip()


def wt(root, rel, txt):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt if isinstance(txt, str) else json.dumps(txt), encoding="utf-8")


def commit(root, msg, author=None):
    git(root, "add", "-A")
    args = ["commit", "-qm", msg] + (["--author", "%s <w@x>" % author] if author else [])
    git(root, *args)
    return git(root, "rev-parse", "HEAD")


def block(marker, fn="feature"):
    return "def %s(x):\n    # BEGIN %s\n    x = x * 2\n    # END %s\n    return x\n" % (fn, marker, marker)


def tests(name, n, loader_file, fn="feature", extra_names=()):
    head = ("import importlib.util\n"
            "spec = importlib.util.spec_from_file_location('m_%s', r'%s')\n"
            "m = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(m)\n" % (name, loader_file))
    body = "".join("def test_case_%d():\n    assert m.%s(%d) == %d\n" % (i, fn, i, 2 * i) for i in range(n))
    body += "".join("def test_%s():\n    assert m.%s(1) == 2\n" % (x, fn) for x in extra_names)
    return head + body


def build(cell, variant=None):
    """variant: a string naming one defect to plant (None for the clean positive)."""
    c = P.CELLS[cell]
    root = Path(tempfile.mkdtemp(prefix="c200_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    for rel in c["regress"]:
        wt(root, rel, "def test_ok():\n    assert True\n")
    for rel in c["mutants"]:
        wt(root, rel, "def other():\n    return 1\n")
    wt(root, "infra/logic/registry/reporting_policies.json", {"families": ["summary"]})
    wt(root, P.TF + "api.tf", 'resource "aws_apigatewayv2_route" "summary" {}\n')
    wt(root, P.TF + "locals.tf", "locals {}\n")
    wt(root, P.LAMBDA + "reporting-publish/handler.py", "def h():\n    return 1\n")
    base = commit(root, "base")
    ser = "0.9.0_WK_IRPT_BCKEND~%d" % c["slot"]
    changed = []
    for i, rel in enumerate(c["mutants"]):
        fn = "feature" if i == 0 else "feature_b"
        if variant == "no_block":
            src = "def other():\n    return 1\n\ndef %s(x):\n    x = x * 2\n    return x\n" % fn
        elif variant == "import_error":
            src = "def other():\n    return 1\n\n# BEGIN %s\nHELPER = 3\n# END %s\nVALUE = HELPER\n\ndef %s(x):\n    return x * 2\n" % (c["marker"], c["marker"], fn)
        else:
            src = "def other():\n    return 1\n\n" + block(c["marker"], fn)
        if variant == "typed_address" and i == 0 and cell == "1":
            src += "\nADDR = 's3://opal-data-49financial/x'\n"
        wt(root, rel, src)
        changed.append(rel)
    neg = list(P.NEG_B) if cell == "2" else []
    if variant == "missing_neg_test":
        neg_defs = neg[:-1]
    else:
        neg_defs = neg
    n = c["min_tests"] if variant != "few_tests" else 2
    t = tests("t", n, str(root / c["mutants"][0]), "feature", neg_defs)
    if variant == "failing_test":
        t += "def test_bad():\n    assert False\n"
    if variant == "weak_tests":
        t = "import importlib.util\n" + "".join("def test_w%d():\n    assert True\n" % i for i in range(c["min_tests"]))
    wt(root, c["test"], t)
    changed.append(c["test"])
    if cell == "1":
        wt(root, "infra/logic/registry/reporting_policies.json", {"families": ["summary", "filled_report"]})
        changed.append("infra/logic/registry/reporting_policies.json")
    if cell == "2":
        route = 'resource "aws_apigatewayv2_route" "summary" {}\nresource "aws_apigatewayv2_route" "report" {\n  route_key = "GET /x/client/{client_id}/report"\n}\n'
        if variant == "two_routes":
            route += 'resource "aws_apigatewayv2_route" "extra" {}\n'
        wt(root, P.TF + "api.tf", route)
        changed.append(P.TF + "api.tf")
        if variant != "no_route_template":
            src = (root / c["mutants"][0]).read_text(encoding="utf-8") + "\nROUTE = '/x/client/{client_id}/report'\n"
            wt(root, c["mutants"][0], src)
    if variant == "stray_path":
        wt(root, "infra/aws/terraform/x.tf", "x")
        changed.append("infra/aws/terraform/x.tf")
    rec = {"base_commit": base, "changed_paths": sorted(changed), "tests_total": n + len(neg_defs) + (1 if variant == "failing_test" else 0), "mutant_tests_failed": 2,
           "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    rec["tests_passed"] = rec["tests_total"] - (1 if variant == "failing_test" else 0)
    if cell == "1":
        rec["default_off"] = variant != "not_off"
        p = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, sys.argv[1]); from lib import opal_naming as n; print(n.address('irpt','49financial','platinum','reporting','client=PLACEHOLDER','filled_report.json'))", str(REAL)],
                           capture_output=True, text=True)
        rec["address_example"] = "s3://wrong/x" if variant == "bad_address" else p.stdout.strip()
    if cell == "2":
        rec["negative_tests"] = neg
    if cell == "3":
        rec["existing_kinds_untouched"] = True
        rec["removed_lines"] = 3 if variant == "bad_removed" else 0
    wt(root, P.record_path(c), rec)
    if variant == "record_mismatch":
        rec["changed_paths"] = rec["changed_paths"][:-1]
        wt(root, P.record_path(c), rec)
    commit(root, "work", ser)
    return root


ORION = {
    "base_commit": "a" * 40,
    "live_writer": {"claim": "inferred", "statement": "the live daily flat writer is not in the repository; a runner on a host writes the flat key each morning",
                    "evidence": ["the newest flat positions key is dated the morning of the last run", "no scheduled rule in the repository fires at that time"]},
    "pair_b": {"files": [{"path": "cli/pull_positions.py", "line": 4, "identifier": "pull_positions"}], "port": "port the flat-key writer of the manual CLI into the scheduled inf-api-positions function so production writes the flat key",
               "cli_disposition": "the manual CLI is retired in the same pair and its docstring repointed to the scheduled function", "no_second_producer": True,
               "schedule_builder_output": "the schedule name is the output of lib/opal_naming.py name() for the SCHEDULE kind, never typed",
               "trading_day_frontier": "the producer stamps the previous trading day by lib/trading_calendar.py and holds by name on a non-trading day"},
    "pair_a": {"days": [{"date": d, "trading_day": d not in ("2026-07-03", "2026-07-04", "2026-07-05")} for d in PO.DAYS],
               "keys": [PO.KEYPFX + d + ".jsonl.gz" for d in PO.DAYS], "absent_beforehand_read_at_act": True, "through_b_code_path": True, "requests": 2240,
               "pacing": "the shared limiter at its two requests per second floor", "read_back": "list each written key and compare its size and ETag with the response held in scratch",
               "rollback_per_key": "delete each created key by the version id its put returned after a HEAD showed it absent",
               "non_trading_policy": "a non-trading day is pulled once and an empty vendor answer is recorded as such, never filled"},
    "blast_radius": {"writes": ["seven flat positions keys in opal-data-inf bronze"], "reads": ["the vendor"], "new_iam": False, "served_values_changed": False, "other_dates_touched": False},
    "build_slices": [{"cell": "port the writer", "risk": "LOCAL", "files": ["cli/pull_positions.py"]}, {"cell": "the schedule declaration", "risk": "LOCAL", "files": ["infra/x.tf"]}],
    "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
ORION_PKT = "# never-widen packet\n" + "pair (a), pair (b); blast radius; rollback; stop rule; opal_naming; trading-day frontier; no shadow pipeline; COO half UNSIGNED. CTO half UNSIGNED.\n" + ("padding line\n" * 600)


def orion_root(rec=None, pkt=None):
    root = Path(tempfile.mkdtemp(prefix="c200o_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    wt(root, "cli/pull_positions.py", "import x\n\n\ndef other():\n    return 0\n\n\ndef pull_positions():\n    return 1\n")
    commit(root, "base")
    r = copy.deepcopy(rec or ORION)
    r["pair_b"]["files"][0]["line"] = 8
    wt(root, PO.REC, r)
    wt(root, PO.PKT, pkt if pkt is not None else ORION_PKT)
    commit(root, "work")
    return root


def run(root, cid):
    p = subprocess.run([sys.executable, str(CHECK), str(root), cid], capture_output=True, text=True, timeout=200, env=dict(os.environ))
    return p.stdout.strip().splitlines()[-1] if p.stdout.strip() else "NOOUT " + p.stderr[-200:]


bad = 0


def expect(label, cid, root, want):
    global bad
    r = run(root, cid)
    ok = r == cid + (" PASS" if want else " FAIL")
    bad += 0 if ok else 1
    print("%s %-12s %-50s -> %s %s" % ("POSITIVE" if want else "NEGATIVE", cid, label, r, "" if ok else "<-- UNEXPECTED"))


for cell in ("1", "2", "3"):
    root = build(cell)
    for ac in ("AC1", "AC2", "AC3"):
        expect("clean", "IB200-%s-%s" % (cell, ac), root, True)
    shutil.rmtree(root, ignore_errors=True)
    for variant, ac in (("failing_test", "AC1"), ("few_tests", "AC1"), ("no_block", "AC2"), ("import_error", "AC2"), ("weak_tests", "AC2"),
                        ("stray_path", "AC3"), ("record_mismatch", "AC3")):
        root = build(cell, variant)
        expect(variant, "IB200-%s-%s" % (cell, ac), root, False)
        shutil.rmtree(root, ignore_errors=True)
for cell, variant, ac in (("1", "typed_address", "AC3"), ("1", "bad_address", "AC3"), ("1", "not_off", "AC3"), ("2", "missing_neg_test", "AC3"), ("2", "two_routes", "AC3"),
                          ("2", "no_route_template", "AC3"), ("3", "bad_removed", "AC3")):
    root = build(cell, variant)
    expect(variant, "IB200-%s-%s" % (cell, ac), root, False)
    shutil.rmtree(root, ignore_errors=True)

root = orion_root()
for ac in ("AC1", "AC2", "AC3"):
    expect("clean", "IB200-4-" + ac, root, True)
shutil.rmtree(root, ignore_errors=True)


def mo(fn):
    o = copy.deepcopy(ORION)
    fn(o)
    return o


for label, ac, rec, pkt in (
        ("a CLI not retired", "AC1", mo(lambda o: o["pair_b"].update({"cli_disposition": "the manual CLI stays as it is beside the function"})), None),
        ("a second producer", "AC1", mo(lambda o: o["pair_b"].update({"no_second_producer": False})), None),
        ("schedule names typed", "AC1", mo(lambda o: o["pair_b"].update({"schedule_builder_output": "the schedule is called orion-6am, typed here"})), None),
        ("a wrong file identifier", "AC1", mo(lambda o: o["pair_b"]["files"][0].update({"identifier": "nope_function"})), None),
        ("no live-writer evidence", "AC1", mo(lambda o: o["live_writer"].update({"evidence": ["one line of evidence only here"]})), None),
        ("six days only", "AC2", mo(lambda o: o["pair_a"].update({"days": o["pair_a"]["days"][:-1]})), None),
        ("a key for another date", "AC2", mo(lambda o: o["pair_a"]["keys"].__setitem__(0, PO.KEYPFX + "2026-07-02.jsonl.gz")), None),
        ("not through (b)'s path", "AC2", mo(lambda o: o["pair_a"].update({"through_b_code_path": False})), None),
        ("other dates touched", "AC2", mo(lambda o: o["blast_radius"].update({"other_dates_touched": True})), None),
        ("a packet too short", "AC3", None, "# never-widen packet\nshort. COO half UNSIGNED. CTO half UNSIGNED.\n"),
        ("one half signed", "AC3", None, ORION_PKT.replace("CTO half UNSIGNED.", "CTO half signed.")),
        ("one build slice", "AC3", mo(lambda o: o["build_slices"].pop()), None),
        ("a vendor request already sent", "AC3", mo(lambda o: o.update({"vendor_requests_sent": 1})), None)):
    root = orion_root(rec, pkt)
    expect(label, "IB200-4-" + ac, root, False)
    shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
