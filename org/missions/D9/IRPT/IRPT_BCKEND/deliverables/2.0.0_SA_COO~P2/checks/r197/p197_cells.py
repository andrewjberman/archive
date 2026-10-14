"""IRPT_BCKEND round 197 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of four orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196 helpers (checks/r196/p196_cells.py, committed beside it).

  IB197-1  IB-pr-544  the release pin 2: b1d354cfc9 plus ONE commit reverting the CUSIP port 01e843ce2e in the closure members (BUILD)
    AC1  the pin: descends from b1d354cfc9, changes only holdings_snapshot.py, the closure file is byte-equal, and its diff IS the round-196 cusip toggle diff
    AC2  every .py closure member imported under python -I from each firm's BUILT bundle, no ImportError
    AC3  closure == traced set both ways, the bundle delta against b1d354cfc9's bundles is exactly holdings_snapshot.py changed
  IB197-2  IB-pr-545  the differential on the BUILT bundles at pin 2: Cottonwood's remaining changes are the cash rule alone (READ ONLY)
    AC1  32 and 841 unchanged, Cottonwood totals exactly its signed cash-rule nodes (no beyond-rule group), the gate at one served state
    AC2  provenance (pin 2), the signed custody pins and live versions, one digest from two runs, a mutant flagged
    AC3  notes, the six bound counters 0, no long digit run
  IB197-3  IB-pr-546  packet v3 on pin 2; both halves UNSIGNED
    AC1  v3 is v2 plus 3,000 characters, names pin 2, the reverted port and the closure fix
    AC2  the numbers of the two records are in v3 and both halves read UNSIGNED
    AC3  no long digit run, the six bound counters 0
  IB197-4  IB-pr-547  READ: why the CUSIP port blanks 45 Cottonwood sub-class values (READ ONLY)
    AC1  the 45 nodes split by cause, each cause with a rule site the check reads at the pin and the prior path
    AC2  the options (keep the sub-class where the prior path held it, or a documented correction) with their consequences
    AC3  notes, the six bound counters 0, no long digit run
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
R1 = D + "0.9.0_WK_IRPT_BCKEND~389/IB197-1_pin2_record.json"
R2 = D + "0.9.0_WK_IRPT_BCKEND~390/IB197-2_built_differential.json"
R3 = D + "0.9.0_WK_IRPT_BCKEND~391/IB197-3_packet_v3_record.json"
V3 = D + "0.9.0_WK_IRPT_BCKEND~391/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V3.md"
R4 = D + "0.9.0_WK_IRPT_BCKEND~392/IB197-4_cusip_sub_class_read.json"
TOGGLE_DIFF = D + "0.9.0_WK_IRPT_BCKEND~387/toggle_cusip_fallback.diff"
PIN1 = "b1d354cfc9341168a3b4c316a344876ce0049b97"
PIN2 = "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f"
CUSIP_PORT = "01e843ce2e"
HS = "data/assets/scripts/gold/investor_reporting/holdings_snapshot.py"
CORE = P6.CORE
FIRMS = P6.FIRMS
SIGNED_FIXED = {"49financial": 32, "inflection": 841}
fail, load, is_int, is_num, is_hex = P6.fail, P6.load, P6.is_int, P6.is_num, P6.is_hex
no_long_digits, counters, git, git_show, closure = P6.no_long_digits, P6.counters, P6.git, P6.git_show, P6.closure


def diff_lines(text):
    return sorted(x for x in text.splitlines() if x[:1] in "+-" and not x.startswith(("+++", "---")))


# ----------------------------------------------------------------------------- IB197-1
def c1_ac1():
    r = load(R1)
    pin = r.get("new_pin")
    if r.get("base_pin") != PIN1 or pin != PIN2:
        fail("base_pin must be %s and new_pin the issuer's pin 2 %s" % (PIN1, PIN2))
    if git("merge-base", "--is-ancestor", PIN1, pin).returncode != 0:
        fail("pin 2 does not descend from b1d354cfc9")
    names = [x for x in git("diff", "--name-only", PIN1, pin).stdout.splitlines() if x]
    if names != [HS]:
        fail("pin 2 may change only %s, changes %r" % (HS, names[:4]))
    if git_show(pin, CORE) != git_show(PIN1, CORE):
        fail("the closure file must be byte-equal at pin 2 (the closure fix stays)")
    tfile = P6.ROOT / TOGGLE_DIFF
    if not tfile.is_file():
        fail("no round-196 toggle diff to compare with")
    mine = diff_lines(git("diff", PIN1, pin, "--", HS).stdout)
    theirs = diff_lines(tfile.read_text(encoding="utf-8", errors="replace"))
    if not mine or mine != theirs:
        fail("pin 2's diff of holdings_snapshot.py is not the round-196 cusip toggle diff (%d lines against %d)" % (len(mine), len(theirs)))
    subj = git("show", "-s", "--format=%s", pin).stdout
    if CUSIP_PORT not in subj:
        fail("pin 2's commit subject must name the reverted port %s" % CUSIP_PORT)
    print("OK: pin 2 is b1d354cfc9 plus the reverse of the CUSIP port in holdings_snapshot.py, equal to the round-196 toggle")


def c1_ac2():
    r = load(R1)
    P6.R1 = R1
    new = closure(git_show(r["new_pin"], CORE) or fail("no core at pin 2"))
    expected = sorted(m for m in new if m.endswith(".py"))
    for firm in FIRMS:
        f = (r.get("import_proof") or {}).get(firm) or fail("no import proof for %s" % firm)
        if f.get("python_flags") != "-I" or sorted(f.get("members_imported", [])) != expected or f.get("import_errors") != [] or f.get("bundle_tree_members") != len(new) + 1:
            fail("%s: every .py closure member imported under python -I with no error from a tree of the closure plus SHA256SUMS" % firm)
    print("OK: every .py member imported from each firm's built bundle")


def c1_ac3():
    r = load(R1)
    pin = r["new_pin"]
    new = closure(git_show(pin, CORE) or fail("no core at pin 2"))
    t = r.get("closure_vs_trace") or {}
    traced = set(t.get("traced_files", []))
    if not traced or t.get("missing") != [] or sorted(traced - set(new) - {"SHA256SUMS"}) != []:
        fail("traced files must be in the closure (missing none)")
    extra = sorted(set(new) - traced)
    rec = {e.get("path"): e.get("import_site") for e in t.get("extra", [])}
    if set(rec) != set(extra):
        fail("extra must list exactly the closure members the trace did not touch")
    for path, site in rec.items():
        m = re.fullmatch(r"(.+):(\d+)", site or "")
        src = git_show(pin, m.group(1)) if m else None
        if not m or src is None or m.group(1) not in new:
            fail("extra %s: a verifiable import site is required" % path)
        lines = src.decode("utf-8", "replace").splitlines()
        if int(m.group(2)) > len(lines) or Path(path).stem not in lines[int(m.group(2)) - 1]:
            fail("extra %s: line %s does not name it" % (path, m.group(2)))
    bd = r.get("bundle_delta") or {}
    if bd.get("members_added") != [] or bd.get("members_removed") != [] or bd.get("members_changed") != [HS]:
        fail("the built bundle may differ from b1d354cfc9's by exactly %s changed" % HS)
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: closure equals the trace both ways, the bundle delta is one changed member")


# ----------------------------------------------------------------------------- IB197-2
def c2_ac1():
    r = load(R2)
    for firm in FIRMS:
        f = (r.get("firms") or {}).get(firm) or fail("no differential for %s" % firm)
        for side in ("live", "built"):
            rows = (f.get("rows") or {}).get(side)
            if not isinstance(rows, dict) or not rows or not all(is_int(v) and v >= 0 for v in rows.values()):
                fail("%s: rows.%s must map node kinds to counts" % (firm, side))
        a = f.get("account_set") or {}
        if not all(is_int(a.get(k)) and a[k] >= 0 for k in ("only_live", "only_built", "both")):
            fail("%s: account_set needs only_live, only_built, both" % firm)
        cv = f.get("changed_values") or {}
        if not (is_num(cv.get("tolerance")) and cv["tolerance"] > 0 and is_int(cv.get("nodes_with_changed_numeric_value")) and is_num(cv.get("largest_abs_delta"))):
            fail("%s: changed_values needs a tolerance, a count and the largest delta" % firm)
        g = f.get("gate") or {}
        sv = g.get("served_state") or {}
        if not isinstance(sv.get("latest_date"), str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", sv["latest_date"]):
            fail("%s: the gate comparison needs the served state" % firm)
        for side in ("live", "built"):
            if (g.get(side) or {}).get("outcome") not in ("PUBLISHED", "REFUSED") or not isinstance((g.get(side) or {}).get("conditions"), list):
                fail("%s: gate.%s needs an outcome and conditions" % (firm, side))
        same = g["live"]["outcome"] == g["built"]["outcome"] and sorted(map(str, g["live"]["conditions"])) == sorted(map(str, g["built"]["conditions"]))
        if same and g.get("attribution") != "same":
            fail("%s: equal gates read 'same'" % firm)
        if not same and not (g.get("attribution") == "signed_exemption_repair" and firm == "cottonwood"):
            fail("%s: a gate difference that is not the signed exemption repair on Cottonwood is a STOP" % firm)
        total, diffs = f.get("total_changed_nodes"), f.get("differences")
        if not is_int(total) or not isinstance(diffs, list) or any(d.get("attribution") != "signed_cash_rule" for d in diffs):
            fail("%s: every difference group is the signed cash rule (any other group is UNATTRIBUTED, a STOP)" % firm)
        signed = sum(d.get("nodes", 0) for d in diffs)
        if signed != total:
            fail("%s: the cash-rule groups cover %d nodes, the total is %d" % (firm, signed, total))
        if firm in SIGNED_FIXED and total != SIGNED_FIXED[firm]:
            fail("%s must total exactly %d changed nodes, totals %d: a STOP" % (firm, SIGNED_FIXED[firm], total))
        if firm == "cottonwood" and not (249 <= total <= 260):
            fail("cottonwood's cash-rule nodes should be about 253 (249 signed plus the 4 formerly overdetermined), reads %d" % total)
    print("OK: 32 and 841 unchanged, Cottonwood is the cash rule alone, the same-state gate")


def c2_ac2():
    r = load(R2)
    r1 = load(R1)
    if r.get("new_pin") != r1.get("new_pin") or not is_hex(r.get("new_pin"), 40):
        fail("new_pin must equal IB-pr-544's pin 2")
    if r.get("custody_pins") != P6.PINS or r.get("live_versions") != P6.LIVE_VERSIONS:
        fail("custody_pins and live_versions must be the signed ones")
    for firm in FIRMS:
        f = r["firms"][firm]
        if f.get("built_from") != "core.build_bundle_payload at pin 2" or not is_int(f.get("built_bundle_members")) or f["built_bundle_members"] < 46:
            fail("%s: the build input is the BUILT bundle (core.build_bundle_payload at pin 2)" % firm)
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


# ----------------------------------------------------------------------------- IB197-3
def v3_text():
    f3, f2 = P6.ROOT / V3, P6.ROOT / P6.V2
    if not f3.is_file() or not f2.is_file():
        fail("packet v3 and v2 are both required")
    return f3.read_text(encoding="utf-8"), f2.read_text(encoding="utf-8")


def c3_ac1():
    t3, t2 = v3_text()
    low = t3.lower()
    pin = load(R1)["new_pin"]
    if len(t3) < len(t2) + 3000:
        fail("v3 must be v2 plus at least 3,000 characters")
    if pin not in t3 or CUSIP_PORT not in t3:
        fail("v3 must name pin 2 (%s) and the reverted port (%s)" % (pin, CUSIP_PORT))
    for need in ("opal_unidentified", "built bundle", "closure", "own release", "cash rule", "same served state", "branch a", "branch b", "manifest anchor",
                 "business date", "moved member", "signed scope"):
        if need not in low:
            fail("packet v3 does not carry %r" % need)
    print("OK: v3 names pin 2, the reverted port and the phrases")


def c3_ac2():
    t3, _ = v3_text()
    r2 = load(R2)
    for firm in FIRMS:
        if str(r2["firms"][firm]["total_changed_nodes"]) not in t3:
            fail("v3 must carry the %s total changed nodes" % firm)
    low = t3.lower()
    if len(re.findall(r"unsigned", low)) < 2 or "coo half" not in low or "cto half" not in low:
        fail("both halves must read UNSIGNED at the packet bytes")
    print("OK: the records' totals are in v3, both halves unsigned")


def c3_ac3():
    t3, _ = v3_text()
    for h in (load(R1)["new_pin"], PIN1):
        t3 = t3.replace(h, "").replace(h[:10], "")
    no_long_digits(t3)
    counters(load(R3))
    print("OK: no long digit run, counters 0")


# ----------------------------------------------------------------------------- IB197-4
def c4_ac1():
    r = load(R4)
    pin = r.get("pin")
    if pin != PIN1 or r.get("sub_class_blanked_nodes") != 45:
        fail("the read is at b1d354cfc9 and covers the 45 blanked sub-class values")
    causes = r.get("causes")
    if not isinstance(causes, list) or not causes:
        fail("causes are required")
    total = 0
    for c in causes:
        if not (is_int(c.get("nodes")) and c["nodes"] > 0 and isinstance(c.get("securities_public_symbols"), list) and isinstance(c.get("rule"), str) and len(c["rule"]) >= 30):
            fail("each cause needs a node count, public symbols, and a rule sentence")
        m = re.fullmatch(r"(.+):(\d+)", c.get("rule_site") or "")
        src = git_show(pin, m.group(1)) if m else None
        ident = c.get("rule_identifier")
        if not m or src is None or not isinstance(ident, str) or not ident:
            fail("each cause needs a rule_site path:line at the pin and the identifier on that line")
        lines = src.decode("utf-8", "replace").splitlines()
        if int(m.group(2)) > len(lines) or ident not in lines[int(m.group(2)) - 1]:
            fail("rule site %s does not hold %r" % (c["rule_site"], ident))
        if not isinstance(c.get("prior_path"), str) or len(c["prior_path"]) < 30:
            fail("each cause names the prior path that held the sub-class")
        total += c["nodes"]
    if total != 45:
        fail("the causes cover %d nodes, not 45" % total)
    print("OK: the 45 blanked sub-class values split by cause, each with a verifiable rule site")


def c4_ac2():
    r = load(R4)
    opts = r.get("options")
    if not isinstance(opts, list) or len(opts) < 2:
        fail("at least two options are required")
    kinds = {o.get("kind") for o in opts}
    if not {"keep_prior_sub_class", "documented_correction"} <= kinds:
        fail("options must include keep_prior_sub_class and documented_correction")
    for o in opts:
        if not (isinstance(o.get("consequence"), str) and len(o["consequence"]) >= 40 and is_int(o.get("nodes_affected"))):
            fail("each option states its consequence and the nodes affected")
    rec = r.get("recommendation")
    if rec not in kinds:
        fail("the recommendation must name one of the options")
    print("OK: the options and the recommendation")


def c4_ac3():
    r = load(R4)
    counters(r)
    no_long_digits(json.dumps(r))
    print("OK: notes and counters")


CHECKS = {"IB197-1-AC1": c1_ac1, "IB197-1-AC2": c1_ac2, "IB197-1-AC3": c1_ac3, "IB197-2-AC1": c2_ac1, "IB197-2-AC2": c2_ac2, "IB197-2-AC3": c2_ac3,
          "IB197-3-AC1": c3_ac1, "IB197-3-AC2": c3_ac2, "IB197-3-AC3": c3_ac3, "IB197-4-AC1": c4_ac1, "IB197-4-AC2": c4_ac2, "IB197-4-AC3": c4_ac3}


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p197_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT = Path(sys.argv[1])
    P6.CID = sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
