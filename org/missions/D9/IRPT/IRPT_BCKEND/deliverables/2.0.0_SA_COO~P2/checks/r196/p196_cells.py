"""IRPT_BCKEND round 196 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of four orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB196-1  IB-pr-540  the bundle closure fixed into a NEW pin (BUILD): one member added, proven by `python -I` imports and by closure == trace both ways
    AC1  the pin: ancestor of nothing but the old pin's line, the closure gains exactly opal_unidentified.py, nothing else is deleted
    AC2  every .py closure member imported in a clean interpreter from each firm's BUILT bundle tree, no ImportError
    AC3  closure against the traced import set both ways (missing none; each extra with an import site the check reads), and the bundle delta
  IB196-2  IB-pr-541  the differential on BUILT bundles (live bundle bytes against the new pin's bundle bytes), same-state gate (READ ONLY)
    AC1  rows, accounts, values, the gate at one served state; 32 and 841 reproduce; Cottonwood's signed 249; the rest named for IB-pr-542
    AC2  provenance (the new pin, the live versions) and determinism: two runs one digest per firm, a mutant flagged
    AC3  the record's honesty: notes, the six bound counters 0, no long digit run
  IB196-3  IB-pr-542  Cottonwood's beyond-rule changes attributed by TOGGLING one named commit at a time (READ ONLY)
    AC1  four reverts, each applied; every beyond-rule node lands on a commit whose revert removes it or is UNATTRIBUTED (a STOP); per-commit counts
    AC2  determinism (two runs one digest) and a planted mutant that no revert removes, flagged as one UNATTRIBUTED node
    AC3  notes, the six bound counters 0, no long digit run
  IB196-4  IB-pr-543  packet v3: the new pin, the built-bundle differential and the attribution; both halves UNSIGNED
    AC1  v3 is v2 plus at least 3,000 characters and carries the new pin, the closure fix and the phrases
    AC2  every number of the two records appears in v3 (the per-commit counts, the totals) and both halves read UNSIGNED
    AC3  no long digit run, the six bound counters 0
"""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
R1 = D + "0.9.0_WK_IRPT_BCKEND~385/IB196-1_closure_record.json"
R2 = D + "0.9.0_WK_IRPT_BCKEND~386/IB196-2_built_differential.json"
R3 = D + "0.9.0_WK_IRPT_BCKEND~387/IB196-3_toggle_attribution.json"
R4 = D + "0.9.0_WK_IRPT_BCKEND~388/IB196-4_packet_v3_record.json"
V2 = D + "0.9.0_WK_IRPT_BCKEND~383/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V2.md"
V3 = D + "0.9.0_WK_IRPT_BCKEND~388/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V3.md"
CORE = ".tools/safe_deploy_core.py"
ORDER540 = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-540"
PIN = "49467335d288d5c0012fe339c4cafcb74bd43fb5"
MISSING = "data/assets/scripts/silver/opal_unidentified.py"
FIRMS = ["49financial", "cottonwood", "inflection"]
SIGNED = {"49financial": 32, "cottonwood": 249, "inflection": 841}
PINS = {"49financial": "2026-10-12", "cottonwood": "2026-10-12", "inflection": "2026-10-13"}
LIVE_VERSIONS = {"49financial": "UHOCIkWj3QiIzNucG1VjNnk_AufIg6oD", "cottonwood": "oyIYMVdh_l2zCg5ZWvn3ISPPS6_9Q82_", "inflection": "PzhCs97qVBXkZcIjaOklHmzWiFsOFafM"}
COMMIT_NAMES = {"account_id": r"account_id", "keyed_gate": r"keyed", "cusip_fallback": r"SC-e-56|CUSIP|\be56\b", "multi_asset": r"multi_asset"}
BOUND = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB196"))
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


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def is_hex(x, n):
    return isinstance(x, str) and re.fullmatch(r"[0-9a-f]{%d}" % n, x) is not None


def no_long_digits(txt):
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", txt):
        fail("a long digit run (an identifier or a figure) is present")


def counters(r):
    for k in BOUND:
        if r.get(k) != 0:
            fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
    if not isinstance(r.get("notes"), list) or not r["notes"]:
        fail("notes are required")


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=60)


def git_show(commit, path):
    p = subprocess.run(["git", "-C", str(ROOT), "show", "%s:%s" % (commit, path)], capture_output=True, timeout=60)
    return p.stdout if p.returncode == 0 else None


def subject(c):
    p = git("show", "-s", "--format=%s", c)
    return p.stdout.strip() if p.returncode == 0 else None


def closure(src):
    tree = ast.parse(src.decode("utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "_IRPT_HOLDINGS_CLOSURE" for t in node.targets):
            return [e.value for e in node.value.elts if isinstance(e, ast.Constant)]
    fail("no _IRPT_HOLDINGS_CLOSURE in the file")


# ----------------------------------------------------------------------------- IB196-1
def c1_ac1():
    r = load(R1)
    pin = r.get("new_pin")
    if r.get("base_pin") != PIN or not is_hex(pin, 40):
        fail("base_pin must be %s and new_pin 40 hex" % PIN)
    if git("merge-base", "--is-ancestor", PIN, pin).returncode != 0:
        fail("the new pin does not descend from the old pin")
    names = [x for x in git("diff", "--name-only", PIN, pin).stdout.splitlines() if x]
    stray = [x for x in names if x != CORE and not x.startswith(ORDER540)]
    if CORE not in names or stray:
        fail("the new pin may change only %s (and the order file): %r" % (CORE, stray[:4]))
    old_src, new_src = git_show(PIN, CORE), git_show(pin, CORE)
    if old_src is None or new_src is None:
        fail("the core file is absent at a pin")
    old, new = closure(old_src), closure(new_src)
    if len(new) != len(old) + 1 or set(new) != set(old) | {MISSING}:
        fail("the closure must gain exactly %s" % MISSING)
    num = git("diff", "--numstat", PIN, pin, "--", CORE).stdout.split()
    if len(num) < 2 or num[1] != "0":
        fail("the core file may not delete a line (it deletes %s)" % (num[1] if len(num) > 1 else "?"))
    print("OK: the closure gains exactly one member on a pin that descends from the old pin")


def c1_ac2():
    r = load(R1)
    new = closure(git_show(r["new_pin"], CORE) or fail("no core at the new pin"))
    expected = sorted(m for m in new if m.endswith(".py"))
    ip = r.get("import_proof") or {}
    for firm in FIRMS:
        f = ip.get(firm) or fail("no import proof for %s" % firm)
        if f.get("python_flags") != "-I":
            fail("%s: the imports must run under python -I" % firm)
        if sorted(f.get("members_imported", [])) != expected:
            fail("%s: members_imported must be every .py closure member (%d)" % (firm, len(expected)))
        if f.get("import_errors") != []:
            fail("%s: an ImportError is a FAIL: %r" % (firm, f.get("import_errors")))
        if f.get("bundle_tree_members") != len(new) + 1:
            fail("%s: the built bundle tree must hold the closure plus SHA256SUMS (%d)" % (firm, len(new) + 1))
    print("OK: every .py member imported from each firm's built bundle")


def c1_ac3():
    r = load(R1)
    pin = r["new_pin"]
    new = closure(git_show(pin, CORE) or fail("no core at the new pin"))
    t = r.get("closure_vs_trace") or {}
    traced = set(t.get("traced_files", []))
    if not traced:
        fail("traced_files is empty")
    missing = sorted(traced - set(new) - {"SHA256SUMS"})
    if missing or t.get("missing") != []:
        fail("traced but not in the closure: %r" % missing[:4])
    extra = sorted(set(new) - traced)
    rec_extra = {e.get("path"): e.get("import_site") for e in t.get("extra", [])}
    if set(rec_extra) != set(extra):
        fail("extra must list exactly the closure members the trace did not touch: %r" % extra[:4])
    for path, site in rec_extra.items():
        m = re.fullmatch(r"(.+):(\d+)", site or "")
        src = git_show(pin, m.group(1)) if m else None
        if not m or src is None or m.group(1) not in new:
            fail("extra %s: the import site must be path:line of a closure member" % path)
        lines = src.decode("utf-8", "replace").splitlines()
        stem = Path(path).stem
        if int(m.group(2)) > len(lines) or stem not in lines[int(m.group(2)) - 1]:
            fail("extra %s: line %s of %s does not name it" % (path, m.group(2), m.group(1)))
    bd = r.get("bundle_delta") or {}
    if bd.get("members_added") != [MISSING] or bd.get("members_changed") != [] or bd.get("members_removed") != []:
        fail("the built bundle may differ from the old pin's by exactly +%s" % MISSING)
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: closure equals the trace both ways, the bundle delta is one member")


# ----------------------------------------------------------------------------- IB196-2
def c2_ac1():
    r = load(R2)
    for firm in FIRMS:
        f = (r.get("firms") or {}).get(firm) or fail("no differential for %s" % firm)
        for side in ("live", "built"):
            rows = (f.get("rows") or {}).get(side)
            if not isinstance(rows, dict) or not rows or not all(is_int(v) and v >= 0 for v in rows.values()):
                fail("%s: rows.%s must be a mapping of node kinds to counts" % (firm, side))
        a = f.get("account_set") or {}
        if not all(is_int(a.get(k)) and a[k] >= 0 for k in ("only_live", "only_built", "both")):
            fail("%s: account_set needs only_live, only_built, both" % firm)
        cv = f.get("changed_values") or {}
        if not (is_num(cv.get("tolerance")) and cv["tolerance"] > 0 and is_int(cv.get("nodes_with_changed_numeric_value")) and is_num(cv.get("largest_abs_delta"))):
            fail("%s: changed_values needs a tolerance, a count and the largest delta" % firm)
        g = f.get("gate") or {}
        sv = g.get("served_state") or {}
        if not isinstance(sv.get("latest_date"), str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sv["latest_date"]):
            fail("%s: the gate comparison needs the served state (latest_date)" % firm)
        for side in ("live", "built"):
            if (g.get(side) or {}).get("outcome") not in ("PUBLISHED", "REFUSED") or not isinstance((g.get(side) or {}).get("conditions"), list):
                fail("%s: gate.%s needs an outcome and conditions" % (firm, side))
        same = g["live"]["outcome"] == g["built"]["outcome"] and sorted(map(str, g["live"]["conditions"])) == sorted(map(str, g["built"]["conditions"]))
        ga = g.get("attribution")
        if same and ga != "same":
            fail("%s: equal gates read 'same'" % firm)
        if not same and not (ga == "signed_exemption_repair" and firm == "cottonwood"):
            fail("%s: a gate difference that is not the signed exemption repair on Cottonwood is a STOP" % firm)
        total = f.get("total_changed_nodes")
        diffs = f.get("differences")
        if not is_int(total) or not isinstance(diffs, list):
            fail("%s: total_changed_nodes and differences are required" % firm)
        signed = sum(d.get("nodes", 0) for d in diffs if d.get("attribution") == "signed_cash_rule")
        if signed != SIGNED[firm]:
            fail("%s: the signed cash rule explains %d nodes, the signed count is %d" % (firm, signed, SIGNED[firm]))
        other = [d for d in diffs if d.get("attribution") != "signed_cash_rule"]
        if firm != "cottonwood" and (other or total != SIGNED[firm]):
            fail("%s: 32 and 841 must reproduce exactly; any other number is a STOP (total %r)" % (firm, total))
        if firm == "cottonwood":
            if any(d.get("attribution") != "TO_IB-pr-542" for d in other) or f.get("beyond_rule_nodes") is None:
                fail("cottonwood: the beyond-rule groups are named for IB-pr-542 and counted (beyond_rule_nodes)")
            if not is_int(f["beyond_rule_nodes"]) or f["beyond_rule_nodes"] + SIGNED[firm] < total:
                fail("cottonwood: beyond_rule_nodes does not cover the total changed nodes")
    print("OK: the built-bundle differential, 32 and 841 reproduced, the same-state gate")


def c2_ac2():
    r = load(R2)
    r1 = load(R1)
    if r.get("new_pin") != r1.get("new_pin") or not is_hex(r.get("new_pin"), 40):
        fail("new_pin must equal IB-pr-540's new pin")
    if r.get("custody_pins") != PINS or r.get("live_versions") != LIVE_VERSIONS:
        fail("custody_pins and live_versions must be the signed ones")
    for firm in FIRMS:
        f = r["firms"][firm]
        if f.get("built_from") != "core.build_bundle_payload at the new pin" or not is_int(f.get("built_bundle_members")) or f["built_bundle_members"] < 46:
            fail("%s: the build input is the BUILT bundle (core.build_bundle_payload at the new pin)" % firm)
        d1, d2 = f.get("run1_digest"), f.get("run2_digest")
        if not (is_hex(d1, 64) and is_hex(d2, 64)) or d1 != d2:
            fail("%s: two runs must give ONE digest" % firm)
        m = f.get("mutant") or {}
        if m.get("flagged") is not True or m.get("changed_nodes_with_mutant") != f["total_changed_nodes"] + 1:
            fail("%s: the planted mutant must be flagged as exactly one more changed node" % firm)
    print("OK: provenance and one digest per firm, the mutant flagged")


def c2_ac3():
    r = load(R2)
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: notes and counters")


# ----------------------------------------------------------------------------- IB196-3
def c3_ac1():
    r = load(R3)
    r2 = load(R2)
    cw = r2["firms"]["cottonwood"]
    if r.get("beyond_rule_total") != cw["beyond_rule_nodes"]:
        fail("beyond_rule_total must equal IB-pr-541's beyond_rule_nodes (%r)" % cw["beyond_rule_nodes"])
    pc = r.get("per_commit")
    if not isinstance(pc, list) or {x.get("name") for x in pc} != set(COMMIT_NAMES):
        fail("per_commit must hold the four named commits: %r" % sorted(COMMIT_NAMES))
    attributed_sum = 0
    for x in pc:
        c = x.get("commit")
        s = subject(c) if is_hex(c, 40) else None
        if s is None or not re.search(COMMIT_NAMES[x["name"]], s, re.I):
            fail("%s: commit %r does not exist or its subject does not name it" % (x["name"], c))
        if x.get("revert_applied") is not True or not is_int(x.get("removed_nodes")) or x["removed_nodes"] < 0 or not is_num(x.get("largest_abs_delta")):
            fail("%s: the revert must be applied, with a removed-node count and the largest delta" % x["name"])
        if not isinstance(x.get("groups"), list) or sum(g.get("nodes", 0) for g in x["groups"]) < x["removed_nodes"] and x["removed_nodes"] > 0:
            fail("%s: groups must account for the removed nodes" % x["name"])
        attributed_sum += x["removed_nodes"]
    overlap, joint, un = r.get("overlap_nodes"), r.get("joint_nodes"), r.get("unattributed_nodes")
    if not (is_int(overlap) and overlap >= 0 and is_int(joint) and joint >= 0 and is_int(un) and un >= 0):
        fail("overlap_nodes, joint_nodes and unattributed_nodes are required")
    if attributed_sum - overlap + joint + un != r["beyond_rule_total"]:
        fail("attributed (minus overlap) plus joint plus unattributed must equal the beyond-rule total")
    if un != 0:
        fail("%d UNATTRIBUTED node(s): the release STOPS (CTO round-196 ruling)" % un)
    print("OK: every beyond-rule node attributed by a single revert")


def c3_ac2():
    r = load(R3)
    if not (is_hex(r.get("run1_digest"), 64) and r.get("run1_digest") == r.get("run2_digest")):
        fail("two runs must give ONE digest")
    m = r.get("mutant") or {}
    if m.get("flagged") is not True or m.get("unattributed_nodes_with_mutant") != r["unattributed_nodes"] + 1:
        fail("the planted mutant (a change no revert removes) must be flagged as exactly one more UNATTRIBUTED node")
    print("OK: one digest, the mutant flagged")


def c3_ac3():
    r = load(R3)
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: notes and counters")


# ----------------------------------------------------------------------------- IB196-4
def v3_text():
    f3, f2 = ROOT / V3, ROOT / V2
    if not f3.is_file() or not f2.is_file():
        fail("packet v3 and v2 are both required")
    return f3.read_text(encoding="utf-8"), f2.read_text(encoding="utf-8")


def c4_ac1():
    t3, t2 = v3_text()
    r1 = load(R1)
    low = t3.lower()
    if len(t3) < len(t2) + 3000:
        fail("v3 must be v2 plus at least 3,000 characters")
    if r1["new_pin"] not in t3:
        fail("v3 must name the new pin %s" % r1["new_pin"])
    for need in ("opal_unidentified", "built bundle", "toggling", "closure", "same served state", "live-against-pin", "branch a", "branch b",
                 "manifest anchor", "business date", "moved member", "signed scope"):
        if need not in low:
            fail("packet v3 does not carry %r" % need)
    print("OK: v3 carries the new pin and the phrases")


def c4_ac2():
    t3, _ = v3_text()
    low = t3.lower()
    r2, r3 = load(R2), load(R3)
    for x in r3["per_commit"]:
        if x["commit"][:10] not in t3 or str(x["removed_nodes"]) not in t3:
            fail("v3 must name commit %s and its count %s" % (x["commit"][:10], x["removed_nodes"]))
    for firm in FIRMS:
        if str(r2["firms"][firm]["total_changed_nodes"]) not in t3:
            fail("v3 must carry the %s total changed nodes" % firm)
    if str(r3["beyond_rule_total"]) not in t3 or "unattributed" not in low:
        fail("v3 must carry the beyond-rule total and the unattributed statement")
    if len(re.findall(r"unsigned", low)) < 2 or "coo half" not in low or "cto half" not in low:
        fail("both halves must read UNSIGNED at the packet bytes")
    print("OK: the records' numbers are in v3, both halves unsigned")


def c4_ac3():
    t3, _ = v3_text()
    r = load(R4)
    known = [load(R1)["new_pin"]] + [x["commit"] for x in load(R3)["per_commit"]]
    for h in known:  # a commit id the packet must name can be a run of digits; it is an id, not a figure
        t3 = t3.replace(h, "").replace(h[:10], "")
    no_long_digits(t3)
    counters(r)
    print("OK: no long digit run, counters 0")


CHECKS = {"IB196-1-AC1": c1_ac1, "IB196-1-AC2": c1_ac2, "IB196-1-AC3": c1_ac3, "IB196-2-AC1": c2_ac1, "IB196-2-AC2": c2_ac2, "IB196-2-AC3": c2_ac3,
          "IB196-3-AC1": c3_ac1, "IB196-3-AC2": c3_ac2, "IB196-3-AC3": c3_ac3, "IB196-4-AC1": c4_ac1, "IB196-4-AC2": c4_ac2, "IB196-4-AC3": c4_ac3}


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p196_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT = Path(sys.argv[1])
    CID = sys.argv[2]
    CHECKS[CID]()
    print("%s PASS" % CID)
