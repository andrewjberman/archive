"""IRPT_BCKEND round 195 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB195-1  IB-pr-539  the LIVE-against-PIN differential of the holdings-producer release, per firm, and packet v3 (READ ONLY)
    AC1  the differential and its attribution: rows, account set, changed values and the largest delta, the gate on both codes; every
         difference attributed to a signed change or to a commit named in W383-S2; UNATTRIBUTED is a STOP (the check fails on it)
    AC2  determinism and discrimination: two runs, one digest, per firm; a planted mutant that the comparison flags; the pins and the live versions
    AC3  packet v3 = v2 plus the differential as the signed scope, both halves UNSIGNED, no long digit run, the six bound counters 0
"""
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
REC = D + "0.9.0_WK_IRPT_BCKEND~384/IB195-1_differential_record.json"
V3 = D + "0.9.0_WK_IRPT_BCKEND~384/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V3.md"
V2REC = D + "0.9.0_WK_IRPT_BCKEND~383/IB194-1_packet_v2_record.json"
V2 = D + "0.9.0_WK_IRPT_BCKEND~383/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V2.md"
PIN = "49467335d288d5c0012fe339c4cafcb74bd43fb5"
FIRMS = ["49financial", "cottonwood", "inflection"]
SIGNED = {"49financial": 32, "cottonwood": 249, "inflection": 841}
PINS = {"49financial": "2026-10-12", "cottonwood": "2026-10-12", "inflection": "2026-10-13"}
LIVE_VERSIONS = {"49financial": "UHOCIkWj3QiIzNucG1VjNnk_AufIg6oD", "cottonwood": "oyIYMVdh_l2zCg5ZWvn3ISPPS6_9Q82_", "inflection": "PzhCs97qVBXkZcIjaOklHmzWiFsOFafM"}
NAMED = re.compile(r"account_id|keyed|CUSIP|SC-e-56|multi_asset", re.I)
BOUND = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
SIGNED_ATTR = {"signed_cash_rule": "identity-patch", "signed_exemption_repair": "gate"}
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB195"))
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


def commit_subject(c):
    p = subprocess.run(["git", "-C", str(ROOT), "show", "-s", "--format=%s", c], capture_output=True, text=True, timeout=60)
    return p.stdout.strip() if p.returncode == 0 else None


def v2_members(firm):
    r = load(V2REC)
    return {x["path"] for x in r["members"][firm] if x["class"] in ("behaviour", "data")}


def ac1():
    r = load(REC)
    if r.get("pin") != PIN or not is_hex(r.get("base_commit"), 40):
        fail("pin must be %s and base_commit 40 hex" % PIN)
    for firm in FIRMS:
        f = (r.get("firms") or {}).get(firm) or fail("no differential for %s" % firm)
        for side in ("live", "pin"):
            rows = (f.get("rows") or {}).get(side)
            if not isinstance(rows, dict) or not rows or not all(is_int(v) and v >= 0 for v in rows.values()):
                fail("%s: rows.%s must be a mapping of node kinds to counts" % (firm, side))
        a = f.get("account_set") or {}
        if not all(is_int(a.get(k)) and a[k] >= 0 for k in ("only_live", "only_pin", "both")):
            fail("%s: account_set needs only_live, only_pin, both counts" % firm)
        cv = f.get("changed_values") or {}
        if not (is_num(cv.get("tolerance")) and cv["tolerance"] > 0 and is_int(cv.get("nodes_with_changed_numeric_value")) and is_num(cv.get("largest_abs_delta"))
                and cv["largest_abs_delta"] >= 0 and isinstance(cv.get("largest_delta_field"), str)):
            fail("%s: changed_values needs a tolerance, a count, the largest delta and its field" % firm)
        for side in ("live", "pin"):
            g = (f.get("gate") or {}).get(side) or {}
            if g.get("outcome") not in ("PUBLISHED", "REFUSED") or not isinstance(g.get("conditions"), list):
                fail("%s: gate.%s needs an outcome and a conditions list" % (firm, side))
        gl, gp = f["gate"]["live"], f["gate"]["pin"]
        same_gate = gl["outcome"] == gp["outcome"] and sorted(map(str, gl["conditions"])) == sorted(map(str, gp["conditions"]))
        ga = f.get("gate_attribution")
        if same_gate and ga != "same":
            fail("%s: the gates are equal, so gate_attribution is 'same'" % firm)
        if not same_gate and not (ga == "signed_exemption_repair" and firm == "cottonwood"):
            fail("%s: the gate differs and is not the signed exemption repair on Cottonwood: UNATTRIBUTED, a STOP" % firm)
        total, att, unatt = f.get("total_changed_nodes"), f.get("attributed_nodes"), f.get("unattributed_nodes")
        if not (is_int(total) and is_int(att) and is_int(unatt)) or att + unatt != total:
            fail("%s: attributed + unattributed must equal the total changed nodes" % firm)
        if unatt != 0:
            fail("%s: %d UNATTRIBUTED node(s) -- a STOP, read before anything is signed" % (firm, unatt))
        diffs = f.get("differences")
        if not isinstance(diffs, list) or (total > 0 and not diffs):
            fail("%s: differences must list every group of changed nodes" % firm)
        signed_nodes = 0
        allowed = v2_members(firm)
        for d in diffs:
            attr = d.get("attribution")
            if not isinstance(d.get("group"), str) or not is_int(d.get("nodes")) or d["nodes"] <= 0 or d["nodes"] > max(total, 1):
                fail("%s: a difference group needs a label and a node count within the total" % firm)
            if attr in SIGNED_ATTR:
                if d.get("attributed_by") != SIGNED_ATTR[attr]:
                    fail("%s: %s is attributed by %s" % (firm, attr, SIGNED_ATTR[attr]))
                if attr == "signed_cash_rule":
                    signed_nodes += d["nodes"]
            elif isinstance(attr, str) and attr.startswith("W383-S2:"):
                mem = d.get("members")
                if not isinstance(mem, list) or not mem or not set(mem) <= allowed:
                    fail("%s: %s must name members of the v2 behaviour/data table" % (firm, attr))
                cs = d.get("commits")
                if not isinstance(cs, list) or not cs:
                    fail("%s: %s must name its commits" % (firm, attr))
                for c in cs:
                    s = commit_subject(c) if is_hex(c, 40) else None
                    if s is None:
                        fail("%s: commit %r does not exist" % (firm, c))
                    if not NAMED.search(s):
                        fail("%s: commit %s is outside W383-S2's named set (account_id, keyed gate, CUSIP fallback, multi_asset): UNATTRIBUTED, a STOP" % (firm, c[:10]))
            else:
                fail("%s: attribution %r is not a signed change, a W383-S2 commit or UNATTRIBUTED" % (firm, attr))
        if signed_nodes != SIGNED[firm]:
            fail("%s: the signed cash rule explains %d nodes, the signed count is %d" % (firm, signed_nodes, SIGNED[firm]))
    print("OK: differential arithmetic, the signed counts, every difference attributed")


def ac2():
    r = load(REC)
    if r.get("custody_pins") != PINS or r.get("live_versions") != LIVE_VERSIONS:
        fail("custody_pins must be %r and live_versions the signed packet's" % PINS)
    for firm in FIRMS:
        f = r["firms"][firm]
        d1, d2 = f.get("run1_digest"), f.get("run2_digest")
        if not (is_hex(d1, 64) and is_hex(d2, 64)) or d1 != d2:
            fail("%s: two runs must give ONE digest" % firm)
        m = f.get("mutant") or {}
        if m.get("flagged") is not True or m.get("changed_nodes_with_mutant") != f["total_changed_nodes"] + 1:
            fail("%s: the planted mutant must be flagged as exactly one more changed node" % firm)
    print("OK: one digest per firm, the mutant flagged")


def ac3():
    r = load(REC)
    f3, f2 = ROOT / V3, ROOT / V2
    if not f3.is_file() or not f2.is_file():
        fail("packet v3 and v2 are both required")
    t3, t2 = f3.read_text(encoding="utf-8"), f2.read_text(encoding="utf-8")
    low = t3.lower()
    if len(t3) < len(t2) + 1500:
        fail("v3 must be v2 plus the differential section")
    for need in ("live-against-pin", "differential", "unattributed", "signed scope", "branch a", "branch b", "manifest anchor", "business date", "moved member"):
        if need not in low:
            fail("packet v3 does not carry %r" % need)
    if len(re.findall(r"unsigned", low)) < 2 or "coo half" not in low or "cto half" not in low:
        fail("both halves must read UNSIGNED at the packet bytes")
    for firm in FIRMS:
        for d in r["firms"][firm]["differences"]:
            if d["group"] not in t3:
                fail("packet v3 does not name the %s group %r" % (firm, d["group"]))
    for k in BOUND:
        if r.get(k) != 0:
            fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
    if not isinstance(r.get("notes"), list) or not r["notes"]:
        fail("notes are required")
    no_long_digits(t3)
    no_long_digits(json.dumps(r))
    print("OK: packet v3 carries the differential, both halves unsigned")


CHECKS = {"IB195-1-AC1": ac1, "IB195-1-AC2": ac2, "IB195-1-AC3": ac3}


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p195_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    ROOT = Path(sys.argv[1])
    CID = sys.argv[2]
    CHECKS[CID]()
    print("%s PASS" % CID)
