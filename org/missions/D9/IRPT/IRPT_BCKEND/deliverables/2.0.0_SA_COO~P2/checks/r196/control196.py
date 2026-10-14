"""Positive control and negatives for p196_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control196.py <real_repo_root>
Builds a temp git repo (an old pin whose core file holds a closure tuple, a new pin that adds one member, four named commits and an unrelated one),
synthetic records in the shapes the orders ask for, runs every criterion in-process expecting PASS, then applies each mutation expecting the NAMED
criterion to FAIL. The temp root is removed.
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
sys.path.insert(0, str(REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r196"))
import p196_cells as P  # noqa: E402

NAMES4 = ("account_id", "keyed_gate", "cusip_fallback", "multi_asset")
CLOS = ["data/a.py", "data/b.py", "data/data.json"] + ["data/m_%s.py" % n for n in NAMES4]
ORDER540 = P.ORDER540 + ".verify-closure.md"


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


def build(extra_closure_edit=None, stray=False):
    root = Path(tempfile.mkdtemp(prefix="c196_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    wt(root, P.CORE, core(CLOS))
    wt(root, "data/a.py", "import b\n")
    wt(root, "data/b.py", "X = 1\n")
    for n in NAMES4:
        wt(root, "data/m_%s.py" % n, "V = 0")
    old = commit(root, "old pin")
    wt(root, P.CORE, core(CLOS + [P.MISSING]))
    if extra_closure_edit:
        wt(root, P.CORE, extra_closure_edit)
    if stray:
        wt(root, "data/stray.txt", "x")
    new = commit(root, "closure fix")
    cm = {}
    for name, subj in (("account_id", "build: account_id on every account node"), ("keyed_gate", "feat: keyed sets publish gate"),
                       ("cusip_fallback", "port: e62 + SC-e-56 classifier"), ("multi_asset", "release: multi_asset readers"), ("other", "refactor: rename")):
        wt(root, "data/m_%s.py" % name if name != "other" else "f_other.txt", "V = 1")
        cm[name] = commit(root, subj)
    return root, old, new, cm


def recs(new, cm, old):
    members = sorted(m for m in CLOS + [P.MISSING] if m.endswith(".py"))
    traced = list(CLOS) + [P.MISSING]
    r1 = {"base_pin": old, "new_pin": new, "import_proof": {f: {"python_flags": "-I", "members_imported": members, "import_errors": [], "bundle_tree_members": len(CLOS) + 2} for f in P.FIRMS},
          "closure_vs_trace": {"traced_files": traced, "missing": [], "extra": []},
          "bundle_delta": {"members_added": [P.MISSING], "members_changed": [], "members_removed": []}, "notes": ["synthetic"], **{k: 0 for k in P.BOUND}}
    firms = {}
    for f in P.FIRMS:
        total = P.SIGNED[f] + (236 if f == "cottonwood" else 0)
        diffs = [{"group": "asset_class: fixed_income -> cash", "nodes": P.SIGNED[f], "attribution": "signed_cash_rule", "attributed_by": "identity-patch"}]
        if f == "cottonwood":
            diffs.append({"group": "asset_class_basis: NAME_ALIAS -> TABLE", "nodes": 236, "attribution": "TO_IB-pr-542"})
        firms[f] = {"rows": {"live": {"SECURITY": 100}, "built": {"SECURITY": 100}}, "account_set": {"only_live": 0, "only_built": 0, "both": 5},
                    "changed_values": {"tolerance": 0.01, "nodes_with_changed_numeric_value": 0, "largest_abs_delta": 0.0},
                    "gate": {"served_state": {"latest_date": "2026-10-13"},
                             "live": {"outcome": "REFUSED" if f == "cottonwood" else "PUBLISHED", "conditions": ["account_lost"] if f == "cottonwood" else []},
                             "built": {"outcome": "PUBLISHED", "conditions": []}, "attribution": "signed_exemption_repair" if f == "cottonwood" else "same"},
                    "total_changed_nodes": total, "differences": diffs, "built_from": "core.build_bundle_payload at the new pin", "built_bundle_members": 47,
                    "run1_digest": "ab" * 32, "run2_digest": "ab" * 32, "mutant": {"flagged": True, "changed_nodes_with_mutant": total + 1}}
        if f == "cottonwood":
            firms[f]["beyond_rule_nodes"] = 236
    r2 = {"new_pin": new, "custody_pins": dict(P.PINS), "live_versions": dict(P.LIVE_VERSIONS), "firms": firms, "notes": ["synthetic"], **{k: 0 for k in P.BOUND}}
    pc = [{"name": n, "commit": cm[n], "revert_applied": True, "resolution": "hand_resolved_closure_member", "toggled_files": ["data/m_%s.py" % n], "removed_nodes": c, "largest_abs_delta": 0.0, "groups": [{"group": "g", "nodes": c}]}
          for n, c in (("account_id", 0), ("keyed_gate", 0), ("cusip_fallback", 236), ("multi_asset", 0))]
    r3 = {"beyond_rule_total": 236, "per_commit": pc, "overlap_nodes": 0, "joint_nodes": 0, "unattributed_nodes": 0, "run1_digest": "cd" * 32, "run2_digest": "cd" * 32,
          "mutant": {"flagged": True, "unattributed_nodes_with_mutant": 1}, "notes": ["synthetic"], **{k: 0 for k in P.BOUND}}
    r4 = {"notes": ["synthetic"], **{k: 0 for k in P.BOUND}}
    v2 = "# v2\n" + ("v2 line\n" * 100)
    v3 = v2 + "\n## v3\nnew pin %s. opal_unidentified closure fix. The built bundle, toggling, same served state, live-against-pin, Branch A, Branch B, manifest anchor, business date, moved member, signed scope.\n" % new
    v3 += "".join("commit %s removes %d nodes.\n" % (cm[n][:10], c) for n, c in (("account_id", 0), ("keyed_gate", 0), ("cusip_fallback", 236), ("multi_asset", 0)))
    v3 += "totals 49financial 32, cottonwood 485, inflection 841; beyond-rule 236; unattributed 0.\nCOO half UNSIGNED. CTO half UNSIGNED.\n" + ("padding line\n" * 400)
    return r1, r2, r3, r4, v2, v3


def put(root, r1, r2, r3, r4, v2, v3):
    for rel, obj in ((P.R1, r1), (P.R2, r2), (P.R3, r3), (P.R4, r4)):
        wt(root, rel, json.dumps(obj))
    wt(root, P.V2, v2)
    wt(root, P.V3, v3)


def run(root, cid, old):
    P.ROOT, P.CID, P.PIN = root, cid, old
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            P.CHECKS[cid]()
        return cid + " PASS"
    except SystemExit:
        return cid + " FAIL"
    except Exception as e:  # noqa: BLE001 -- a crash is not a verdict
        return cid + " CRASH " + type(e).__name__ + ": " + str(e)[:120]


bad = 0
root, old, new, cm = build()
base = recs(new, cm, old)
put(root, *base)
for cid in P.CHECKS:
    r = run(root, cid, old)
    ok = r == cid + " PASS"
    bad += 0 if ok else 1
    print("POSITIVE %s -> %s %s" % (cid, r, "" if ok else "<-- UNEXPECTED"))


def neg(label, cid, edit=None, v3=None):
    global bad
    rr = list(copy.deepcopy(base))
    if edit:
        edit(rr)
    if v3 is not None:
        rr[5] = v3
    put(root, *rr)
    r = run(root, cid, old)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-50s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))


neg("a missing member not in the closure was traced", "IB196-1-AC3", lambda r: r[0]["closure_vs_trace"]["traced_files"].append("data/zzz.py"))
neg("an extra with no import site", "IB196-1-AC3", lambda r: r[0]["closure_vs_trace"].update({"traced_files": ["data/a.py", "data/b.py", P.MISSING], "extra": [{"path": "data/data.json", "import_site": "data/a.py:1"}]}))
neg("a bundle delta that changes a member", "IB196-1-AC3", lambda r: r[0]["bundle_delta"].update({"members_changed": ["data/a.py"]}))
neg("an ImportError recorded", "IB196-1-AC2", lambda r: r[0]["import_proof"]["cottonwood"].update({"import_errors": ["ModuleNotFoundError"]}))
neg("imports not under -I", "IB196-1-AC2", lambda r: r[0]["import_proof"]["inflection"].update({"python_flags": ""}))
neg("a member left unimported", "IB196-1-AC2", lambda r: r[0]["import_proof"]["49financial"].update({"members_imported": ["data/a.py"]}))
neg("49financial does not reproduce 32", "IB196-2-AC1", lambda r: (r[1]["firms"]["49financial"]["differences"][0].update({"nodes": 31}), r[1]["firms"]["49financial"].update({"total_changed_nodes": 31})))
neg("inflection has an extra group", "IB196-2-AC1", lambda r: r[1]["firms"]["inflection"]["differences"].append({"group": "x", "nodes": 1, "attribution": "TO_IB-pr-542"}))
neg("a gate difference called nothing", "IB196-2-AC1", lambda r: r[1]["firms"]["cottonwood"]["gate"].update({"attribution": "same"}))
neg("no served state on the gate", "IB196-2-AC1", lambda r: r[1]["firms"]["inflection"]["gate"].update({"served_state": {}}))
neg("a new pin that is not 540's", "IB196-2-AC2", lambda r: r[1].update({"new_pin": "e" * 40}))
neg("built from the repository tree", "IB196-2-AC2", lambda r: r[1]["firms"]["inflection"].update({"built_from": "the pin worktree"}))
neg("two digests", "IB196-2-AC2", lambda r: r[1]["firms"]["cottonwood"].update({"run2_digest": "ef" * 32}))
neg("mutant not flagged", "IB196-2-AC2", lambda r: r[1]["firms"]["49financial"]["mutant"].update({"flagged": False}))
neg("a counter above 0", "IB196-2-AC3", lambda r: r[1].update({"aws_writes_made": 1}))
neg("an UNATTRIBUTED node", "IB196-3-AC1", lambda r: r[2].update({"unattributed_nodes": 1}))
neg("a revert not applied", "IB196-3-AC1", lambda r: r[2]["per_commit"][0].update({"revert_applied": False}))
neg("a commit whose subject does not name it", "IB196-3-AC1", lambda r: r[2]["per_commit"][3].update({"commit": cm["other"]}))
neg("a joint node not counted", "IB196-3-AC1", lambda r: r[2].update({"joint_nodes": 1}))
neg("a toggled file outside the closure", "IB196-3-AC1", lambda r: r[2]["per_commit"][0].update({"toggled_files": ["f_account_id.txt"]}))
neg("a toggled file the commit did not change", "IB196-3-AC1", lambda r: r[2]["per_commit"][0].update({"toggled_files": ["data/m_keyed_gate.py"]}))
neg("no resolution word", "IB196-3-AC1", lambda r: r[2]["per_commit"][1].pop("resolution"))
neg("only three commits", "IB196-3-AC1", lambda r: r[2]["per_commit"].pop())
neg("beyond-rule total not 541's", "IB196-3-AC1", lambda r: r[2].update({"beyond_rule_total": 235}))
neg("two digests (toggling)", "IB196-3-AC2", lambda r: r[2].update({"run2_digest": "ef" * 32}))
neg("mutant not flagged (toggling)", "IB196-3-AC2", lambda r: r[2]["mutant"].update({"flagged": False}))
neg("a long digit run", "IB196-3-AC3", lambda r: r[2].update({"notes": ["account 123456789012"]}))
neg("v3 is v2 plus little", "IB196-4-AC1", v3="# v2\n" + ("v2 line\n" * 100) + "x\n")
neg("v3 without the new pin", "IB196-4-AC1", v3=base[5].replace(new, "0" * 6))
neg("v3 without a commit count", "IB196-4-AC2", v3=base[5].replace(cm["cusip_fallback"][:10], "abcdef0123"))
neg("v3 with one half signed", "IB196-4-AC2", v3=base[5].replace("CTO half UNSIGNED.", "CTO half signed."))
neg("v3 with a long digit run", "IB196-4-AC3", v3=base[5] + "\nacct 123456789012\n")
# negatives that need a different git history
for label, cid, kw in (("a closure change beyond the one member", "IB196-1-AC1", {"extra_closure_edit": core(CLOS + [P.MISSING, "data/extra.py"])}),
                       ("a stray file in the new pin", "IB196-1-AC1", {"stray": True})):
    root2, old2, new2, cm2 = build(**kw)
    rec2 = recs(new2, cm2, old2)
    put(root2, *rec2)
    r = run(root2, cid, old2)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-50s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))
    shutil.rmtree(root2, ignore_errors=True)
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
