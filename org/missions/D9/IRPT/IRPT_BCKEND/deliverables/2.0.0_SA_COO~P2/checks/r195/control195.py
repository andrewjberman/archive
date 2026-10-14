"""Positive control and negatives for p195_cells.py (run by the issuer at the cut, never by a worker).

Usage: python control195.py <real_repo_root>
Builds a temp git repo (three commits: a named account_id commit, a named CUSIP-fallback commit, an unrelated refactor), a synthetic v2 record and
packet, a synthetic differential record and packet v3 shaped like the real artifacts (the flat shapes of the real records), runs every criterion
in-process expecting PASS, then applies each mutation expecting the NAMED criterion to FAIL. The temp root is removed.
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
sys.path.insert(0, str(REAL / "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/2.0.0_SA_COO~P2/checks/r195"))
import p195_cells as P  # noqa: E402

MEMBER = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
MEMBER2 = "data/firm_registry.json"


def git(root, *a):
    return subprocess.run(["git", "-C", str(root), *a], capture_output=True, text=True, check=True).stdout.strip()


def wb(root, rel, data):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data, encoding="utf-8")


def build():
    root = Path(tempfile.mkdtemp(prefix="c195_"))
    git(root, "init", "-q")
    git(root, "config", "user.email", "c@x")
    git(root, "config", "user.name", "c")
    out = []
    for i, subj in enumerate(["build: account_id on every account node (IB-pr-400)", "build: SC-e-56 CUSIP fallback classifier", "refactor: rename a helper"]):
        wb(root, "f%d.txt" % i, "x%d" % i)
        git(root, "add", "-A")
        git(root, "commit", "-qm", subj)
        out.append(git(root, "rev-parse", "HEAD"))
    return root, out


def make(commits):
    c_acct, c_cusip, c_bad = commits
    v2 = {"members": {f: [{"path": MEMBER, "class": "behaviour"}, {"path": MEMBER2, "class": "data"}, {"path": "x.py", "class": "docs"}] for f in P.FIRMS}}
    diffs = {
        "49financial": [{"group": "asset_class: fixed_income -> cash", "nodes": 32, "attribution": "signed_cash_rule", "attributed_by": "identity-patch"}],
        "inflection": [{"group": "asset_class: fixed_income -> cash", "nodes": 841, "attribution": "signed_cash_rule", "attributed_by": "identity-patch"}],
        "cottonwood": [{"group": "asset_class: fixed_income -> cash", "nodes": 249, "attribution": "signed_cash_rule", "attributed_by": "identity-patch"},
                       {"group": "asset_class_basis: NAME_ALIAS -> TABLE", "nodes": 236, "attribution": "W383-S2:SC-e-56 CUSIP fallback", "attributed_by": "member-swap",
                        "members": [MEMBER], "commits": [c_cusip]},
                       {"group": "sub_asset_class: Investment Grade -> None", "nodes": 29, "attribution": "W383-S2:account_id", "attributed_by": "member-swap",
                        "members": [MEMBER2], "commits": [c_acct]}],
    }
    totals = {"49financial": 32, "inflection": 841, "cottonwood": 249 + 236 + 29}
    firms = {}
    for f in P.FIRMS:
        firms[f] = {"rows": {"live": {"SECURITY": 1000, "ACCOUNT": 50}, "pin": {"SECURITY": 1000, "ACCOUNT": 50}}, "account_set": {"only_live": 0, "only_pin": 0, "both": 50},
                    "changed_values": {"tolerance": 0.01, "nodes_with_changed_numeric_value": 0, "largest_abs_delta": 0.0, "largest_delta_field": "amount.value"},
                    "gate": ({"live": {"outcome": "REFUSED", "conditions": ["account_lost"]}, "pin": {"outcome": "PUBLISHED", "conditions": []}} if f == "cottonwood" else
                             {"live": {"outcome": "PUBLISHED", "conditions": []}, "pin": {"outcome": "PUBLISHED", "conditions": []}}),
                    "gate_attribution": "signed_exemption_repair" if f == "cottonwood" else "same",
                    "total_changed_nodes": totals[f], "attributed_nodes": totals[f], "unattributed_nodes": 0, "differences": diffs[f],
                    "run1_digest": "ab" * 32, "run2_digest": "ab" * 32, "mutant": {"planted": "one asset_class changed in the pin output", "flagged": True,
                                                                                  "changed_nodes_with_mutant": totals[f] + 1}}
    rec = {"pin": P.PIN, "base_commit": "c" * 40, "custody_pins": dict(P.PINS), "live_versions": dict(P.LIVE_VERSIONS), "firms": firms,
           "notes": ["synthetic control record"], **{k: 0 for k in P.BOUND}}
    v2txt = "# packet v2 (synthetic)\n" + ("v2 body line\n" * 200) + "COO half UNSIGNED. CTO half UNSIGNED.\n"
    labels = "\n".join("- %s" % d["group"] for f in P.FIRMS for d in diffs[f])
    v3txt = v2txt + "\n## The live-against-pin differential (the signed scope)\nA differential with no UNATTRIBUTED difference. Branch A, Branch B, manifest anchor, business date, moved member.\n" + labels + "\n" + ("v3 added line\n" * 200)
    return v2, rec, v2txt, v3txt


def put(root, v2, rec, v2txt, v3txt):
    wb(root, P.V2REC, json.dumps(v2))
    wb(root, P.REC, json.dumps(rec))
    wb(root, P.V2, v2txt)
    wb(root, P.V3, v3txt)


def run(root, cid):
    P.ROOT, P.CID = root, cid
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            P.CHECKS[cid]()
        return cid + " PASS"
    except SystemExit:
        return cid + " FAIL"
    except Exception as e:  # noqa: BLE001 -- a crash is not a verdict
        return cid + " CRASH " + type(e).__name__ + ": " + str(e)[:120]


bad = 0
root, commits = build()
v2_0, rec_0, v2t_0, v3t_0 = make(commits)
put(root, v2_0, rec_0, v2t_0, v3t_0)
for cid in P.CHECKS:
    r = run(root, cid)
    ok = r == cid + " PASS"
    bad += 0 if ok else 1
    print("POSITIVE %s -> %s %s" % (cid, r, "" if ok else "<-- UNEXPECTED"))


def neg(label, cid, edit=None, v3=None):
    global bad
    rec = copy.deepcopy(rec_0)
    if edit:
        edit(rec)
    put(root, v2_0, rec, v2t_0, v3 if v3 is not None else v3t_0)
    r = run(root, cid)
    ok = r == cid + " FAIL"
    bad += 0 if ok else 1
    print("NEGATIVE %-12s %-52s -> %s %s" % (cid, label, r, "" if ok else "<-- DID NOT FAIL"))


def unattr(r):
    f = r["firms"]["cottonwood"]
    f["attributed_nodes"] -= 29
    f["unattributed_nodes"] = 29
    f["differences"].pop()


neg("an UNATTRIBUTED node", "IB195-1-AC1", unattr)
neg("a commit outside the named set", "IB195-1-AC1", lambda r: r["firms"]["cottonwood"]["differences"][1].update({"commits": [commits[2]]}))
neg("a commit that does not exist", "IB195-1-AC1", lambda r: r["firms"]["cottonwood"]["differences"][1].update({"commits": ["d" * 40]}))
neg("a member outside the v2 table", "IB195-1-AC1", lambda r: r["firms"]["cottonwood"]["differences"][1].update({"members": ["data/other.py"]}))
neg("the signed rule explains the wrong count", "IB195-1-AC1", lambda r: r["firms"]["49financial"]["differences"][0].update({"nodes": 31}))
neg("attributed + unattributed not the total", "IB195-1-AC1", lambda r: r["firms"]["inflection"].update({"attributed_nodes": 840}))
neg("a gate outcome that is no outcome", "IB195-1-AC1", lambda r: r["firms"]["inflection"]["gate"]["live"].update({"outcome": "MAYBE"}))
neg("an unattributed attribution word", "IB195-1-AC1", lambda r: r["firms"]["cottonwood"]["differences"][2].update({"attribution": "UNATTRIBUTED"}))
neg("a gate difference attributed to nothing", "IB195-1-AC1", lambda r: r["firms"]["cottonwood"].update({"gate_attribution": "same"}))
neg("an inflection gate difference called the signed repair", "IB195-1-AC1", lambda r: (r["firms"]["inflection"]["gate"]["live"].update({"outcome": "REFUSED", "conditions": ["account_lost"]}), r["firms"]["inflection"].update({"gate_attribution": "signed_exemption_repair"})))
neg("two runs, two digests", "IB195-1-AC2", lambda r: r["firms"]["cottonwood"].update({"run2_digest": "cd" * 32}))
neg("the mutant not flagged", "IB195-1-AC2", lambda r: r["firms"]["49financial"]["mutant"].update({"flagged": False}))
neg("the mutant miscounted", "IB195-1-AC2", lambda r: r["firms"]["inflection"]["mutant"].update({"changed_nodes_with_mutant": 841}))
neg("a wrong custody pin", "IB195-1-AC2", lambda r: r["custody_pins"].update({"inflection": "2026-10-12"}))
neg("a wrong live version", "IB195-1-AC2", lambda r: r["live_versions"].update({"cottonwood": "OTHER"}))
neg("a v3 that is v2 plus nothing", "IB195-1-AC3", v3=v2t_0 + "x\n")
neg("a v3 that omits a group", "IB195-1-AC3", v3=v3t_0.replace("sub_asset_class: Investment Grade -> None", "something else"))
neg("a v3 with one half signed", "IB195-1-AC3", v3=v3t_0.replace("CTO half UNSIGNED.", "CTO half signed."))
neg("a bound counter above 0", "IB195-1-AC3", lambda r: r.update({"aws_writes_made": 1}))
neg("a long digit run in v3", "IB195-1-AC3", v3=v3t_0 + "\naccount 123456789012\n")
shutil.rmtree(root, ignore_errors=True)
print("CONTROL SUMMARY: %d unexpected" % bad)
sys.exit(1 if bad else 0)
