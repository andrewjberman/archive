"""Positive control and negatives for p197_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control197.py <real_repo_root>
Builds a temp git repo (a base pin b1 holding a closure file and holdings_snapshot.py, and a pin 2 whose diff of holdings_snapshot.py is saved as the
round-196 cusip toggle diff), synthetic records and packets in the shapes the orders ask for, runs every criterion in-process expecting PASS, then
applies each mutation expecting the NAMED criterion to FAIL. The temp root is removed.
"""
import contextlib
import copy
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REAL = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r197"))
import p197_cells as P  # noqa: E402

P6 = P.P6
HS = P.HS
CLOS = ["data/a.py", "data/b.py", HS]
MISSING = P6.MISSING


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def wt(root, rel, txt):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")


def core(items):
    return "_IRPT_HOLDINGS_CLOSURE = (\n" + "".join('    "%s",\n' % i for i in items) + ")\n"


def commit(root, msg):
    git(root, "add", "-A")
    git(root, "commit", "-qm", msg)
    return git(root, "rev-parse", "HEAD")


def build(stray=False, core_edit=False):
    root = Path(tempfile.mkdtemp(prefix="c197_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    wt(root, P6.CORE, core(CLOS))
    wt(root, "data/a.py", "import b\n")
    wt(root, "data/b.py", "X = 1\n")
    wt(root, HS, "def classify(x):\n    return table(x)  # CUSIP fallback\n\n\ndef cash(x):\n    return x\n")
    b1 = commit(root, "pin 1")
    wt(root, HS, "def classify(x):\n    return prior(x)\n\n\ndef cash(x):\n    return x\n")
    if stray:
        wt(root, "data/b.py", "X = 2\n")
    if core_edit:
        wt(root, P6.CORE, core(CLOS + ["data/extra.py"]))
    p2 = commit(root, "revert(IRPT_BCKEND pin 2): undo the CUSIP port 01e843ce2e in holdings_snapshot.py")
    wt(root, P.TOGGLE_DIFF, git(root, "diff", b1, p2, "--", HS) + "\n")
    wt(root, "line_site.py", "def f():\n    return 1\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "toggle diff and a site file")
    return root, b1, p2


def recs(b1, p2):
    members = sorted(m for m in CLOS if m.endswith(".py"))
    r1 = {"base_pin": b1, "new_pin": p2, "import_proof": {f: {"python_flags": "-I", "members_imported": members, "import_errors": [], "bundle_tree_members": len(CLOS) + 1} for f in P6.FIRMS},
          "closure_vs_trace": {"traced_files": list(CLOS), "missing": [], "extra": []},
          "bundle_delta": {"members_added": [], "members_changed": [HS], "members_removed": []}, "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    firms = {}
    for f in P6.FIRMS:
        total = {"49financial": 32, "inflection": 841, "cottonwood": 253}[f]
        firms[f] = {"rows": {"live": {"SECURITY": 100}, "built": {"SECURITY": 100}}, "account_set": {"only_live": 0, "only_built": 0, "both": 5},
                    "changed_values": {"tolerance": 0.01, "nodes_with_changed_numeric_value": 0, "largest_abs_delta": 0.0},
                    "gate": {"served_state": {"latest_date": "2026-10-13"},
                             "live": {"outcome": "REFUSED" if f == "cottonwood" else "PUBLISHED", "conditions": ["account_lost"] if f == "cottonwood" else []},
                             "built": {"outcome": "PUBLISHED", "conditions": []}, "attribution": "signed_exemption_repair" if f == "cottonwood" else "same"},
                    "total_changed_nodes": total, "differences": [{"group": "asset_class: fixed_income -> cash", "nodes": total, "attribution": "signed_cash_rule"}],
                    "built_from": "core.build_bundle_payload at pin 2", "built_bundle_members": 47, "run1_digest": "ab" * 32, "run2_digest": "ab" * 32,
                    "mutant": {"flagged": True, "changed_nodes_with_mutant": total + 1}}
    r2 = {"new_pin": p2, "custody_pins": dict(P6.PINS), "live_versions": dict(P6.LIVE_VERSIONS), "firms": firms, "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    r3 = {"notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    r4 = {"pin": b1, "sub_class_blanked_nodes": 45,
          "causes": [{"nodes": 30, "securities_public_symbols": ["AGG"], "rule": "the table path sets the sub-class to None when the symbol is not in the table", "rule_site": HS + ":2",
                      "rule_identifier": "table", "prior_path": "the live name-alias path kept the sub-class label for these symbols"},
                     {"nodes": 15, "securities_public_symbols": ["MUB"], "rule": "the municipal branch of the table path returns no sub-class for these symbols", "rule_site": HS + ":2",
                      "rule_identifier": "table", "prior_path": "the live name-pattern path kept the sub-class label for these symbols"}],
          "options": [{"kind": "keep_prior_sub_class", "consequence": "the port keeps the sub-class where the prior path held it; 45 labels stay", "nodes_affected": 45},
                      {"kind": "documented_correction", "consequence": "the absence is documented as a correction and Andrew is told before it ships", "nodes_affected": 45}],
          "recommendation": "keep_prior_sub_class", "notes": ["synthetic"], **{k: 0 for k in P6.BOUND}}
    v2 = "# v2\n" + ("v2 line\n" * 100)
    v3 = v2 + ("\n## v3\npin 2 %s reverts the CUSIP port %s; the closure fix opal_unidentified stays; the built bundle, the cash rule alone explains Cottonwood, the CUSIP port is its own release, "
               "same served state, Branch A, Branch B, manifest anchor, business date, moved member, signed scope.\ntotals 49financial 32, cottonwood 253, inflection 841.\n"
               "COO half UNSIGNED. CTO half UNSIGNED.\n" % (p2, P.CUSIP_PORT)) + ("padding line\n" * 400)
    return r1, r2, r3, r4, v2, v3


def put(root, r1, r2, r3, r4, v2, v3):
    for rel, obj in ((P.R1, r1), (P.R2, r2), (P.R3, r3), (P.R4, r4)):
        wt(root, rel, json.dumps(obj))
    wt(root, P6.V2, v2)
    wt(root, P.V3, v3)


def run(root, cid, b1):
    P6.ROOT, P6.CID, P.PIN1 = root, cid, b1
    P.PIN2 = PIN2_BY_ROOT.get(str(root), P.PIN2)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            P.CHECKS[cid]()
        return cid + " PASS"
    except SystemExit:
        return cid + " FAIL"
    except Exception as e:  # noqa: BLE001 -- a crash is not a verdict
        return cid + " CRASH " + type(e).__name__ + ": " + str(e)[:120]


PIN2_BY_ROOT = {}
bad = 0
root, b1, p2 = build()
PIN2_BY_ROOT[str(root)] = p2
base = recs(b1, p2)
put(root, *base)
for cid in P.CHECKS:
    r = run(root, cid, b1)
    ok = r == cid + " PASS"
    bad += 0 if ok else 1
    print("POSITIVE %s -> %s %s" % (cid, r, "" if ok else "<-- UNEXPECTED"))


def neg(label, cid, edit=None, v3=None, r2fix=None):
    global bad
    rr = list(copy.deepcopy(base))
    if edit:
        edit(rr)
    if v3 is not None:
        rr[5] = v3
    put(root, *rr)
    r = run(root, cid, b1)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-50s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))


neg("a closure member left unimported", "IB197-1-AC2", lambda r: r[0]["import_proof"]["cottonwood"].update({"members_imported": [HS]}))
neg("an ImportError recorded", "IB197-1-AC2", lambda r: r[0]["import_proof"]["inflection"].update({"import_errors": ["ModuleNotFoundError"]}))
neg("a traced file outside the closure", "IB197-1-AC3", lambda r: r[0]["closure_vs_trace"]["traced_files"].append("data/zzz.py"))
neg("a bundle delta of two changed members", "IB197-1-AC3", lambda r: r[0]["bundle_delta"].update({"members_changed": [HS, "data/a.py"]}))
neg("a bundle delta that adds a member", "IB197-1-AC3", lambda r: r[0]["bundle_delta"].update({"members_added": [MISSING]}))
neg("Cottonwood has a beyond-rule group", "IB197-2-AC1", lambda r: r[1]["firms"]["cottonwood"]["differences"].append({"group": "x", "nodes": 1, "attribution": "UNATTRIBUTED"}))
neg("49financial not exactly 32", "IB197-2-AC1", lambda r: (r[1]["firms"]["49financial"]["differences"][0].update({"nodes": 31}), r[1]["firms"]["49financial"].update({"total_changed_nodes": 31})))
neg("Cottonwood still at 485", "IB197-2-AC1", lambda r: (r[1]["firms"]["cottonwood"]["differences"][0].update({"nodes": 485}), r[1]["firms"]["cottonwood"].update({"total_changed_nodes": 485})))
neg("a gate difference called nothing", "IB197-2-AC1", lambda r: r[1]["firms"]["cottonwood"]["gate"].update({"attribution": "same"}))
neg("a pin that is not 544's", "IB197-2-AC2", lambda r: r[1].update({"new_pin": "e" * 40}))
neg("built from the repository tree", "IB197-2-AC2", lambda r: r[1]["firms"]["inflection"].update({"built_from": "the pin worktree"}))
neg("two digests", "IB197-2-AC2", lambda r: r[1]["firms"]["cottonwood"].update({"run2_digest": "ef" * 32}))
neg("a counter above 0", "IB197-2-AC3", lambda r: r[1].update({"aws_writes_made": 1}))
neg("v3 is v2 plus little", "IB197-3-AC1", v3="# v2\n" + ("v2 line\n" * 100) + "x\n")
neg("v3 without pin 2", "IB197-3-AC1", v3=base[5].replace(p2, "0" * 6))
neg("v3 without the reverted port", "IB197-3-AC1", v3=base[5].replace(P.CUSIP_PORT, "abc"))
neg("v3 without a firm total", "IB197-3-AC2", v3=base[5].replace("cottonwood 253", "cottonwood x"))
neg("v3 with one half signed", "IB197-3-AC2", v3=base[5].replace("CTO half UNSIGNED.", "CTO half signed."))
neg("v3 with a long digit run", "IB197-3-AC3", v3=base[5] + "\nacct 123456789012\n")
neg("causes covering 44 nodes", "IB197-4-AC1", lambda r: r[3]["causes"][1].update({"nodes": 14}))
neg("a rule site that does not hold its identifier", "IB197-4-AC1", lambda r: r[3]["causes"][0].update({"rule_identifier": "nonexistent_function"}))
neg("a cause with no prior path", "IB197-4-AC1", lambda r: r[3]["causes"][0].update({"prior_path": "x"}))
neg("one option only", "IB197-4-AC2", lambda r: r[3]["options"].pop())
neg("a recommendation outside the options", "IB197-4-AC2", lambda r: r[3].update({"recommendation": "ship_it"}))
neg("a long digit run in the read", "IB197-4-AC3", lambda r: r[3].update({"notes": ["account 123456789012"]}))
for label, cid, kw in (("a stray file in pin 2", "IB197-1-AC1", {"stray": True}), ("a closure change in pin 2", "IB197-1-AC1", {"core_edit": True})):
    root2, c1, c2 = build(**kw)
    PIN2_BY_ROOT[str(root2)] = c2
    put(root2, *recs(c1, c2))
    r = run(root2, cid, c1)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-50s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))
    shutil.rmtree(root2, ignore_errors=True)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
