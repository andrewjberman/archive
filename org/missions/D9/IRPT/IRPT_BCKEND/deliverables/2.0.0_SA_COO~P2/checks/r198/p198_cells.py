"""IRPT_BCKEND round 198 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- the check of one order.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
It reuses the round-196 and round-197 helpers (checks/r196, checks/r197, committed beside it).

  IB198-1  IB-pr-548  packet v3 on PER-FIRM PINS (CTO round-198 ruling, msg 7910); both halves UNSIGNED
    AC1  v3 is v2 plus 3,000 characters, names both pins in full and the CUSIP port, and carries the phrases
    AC2  the per-firm pin table: 49financial on the closure-fix pin with 32, Cottonwood and Inflection on pin 2 with the records' totals; both halves UNSIGNED
    AC3  no long digit run (known commit ids excepted), the six bound counters 0
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE.parent / "r197"))
import p196_cells as P6  # noqa: E402
import p197_cells as P7  # noqa: E402

D = P6.D
R196_2 = P6.R2
R197_2 = P7.R2
R_REC = D + "0.9.0_WK_IRPT_BCKEND~393/IB198-1_packet_v3_record.json"
V3 = D + "0.9.0_WK_IRPT_BCKEND~393/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V3.md"
PIN1 = P7.PIN1
PIN2 = P7.PIN2
CUSIP_PORT = P7.CUSIP_PORT
FIRMS = P6.FIRMS
fail, load, counters, no_long_digits = P6.fail, P6.load, P6.counters, P6.no_long_digits


def v3_text():
    f3, f2 = P6.ROOT / V3, P6.ROOT / P6.V2
    if not f3.is_file() or not f2.is_file():
        fail("packet v3 and v2 are both required")
    return f3.read_text(encoding="utf-8"), f2.read_text(encoding="utf-8")


def totals():
    a = load(R196_2)["firms"]["49financial"]["total_changed_nodes"]
    b = load(R197_2)["firms"]
    return {"49financial": a, "cottonwood": b["cottonwood"]["total_changed_nodes"], "inflection": b["inflection"]["total_changed_nodes"]}


def c1():
    t3, t2 = v3_text()
    low = t3.lower()
    if len(t3) < len(t2) + 3000:
        fail("v3 must be v2 plus at least 3,000 characters")
    for h, what in ((PIN1, "the closure-fix pin"), (PIN2, "pin 2")):
        if h not in t3:
            fail("v3 must name %s in full (%s)" % (what, h))
    if CUSIP_PORT not in t3:
        fail("v3 must name the CUSIP port %s" % CUSIP_PORT)
    for need in ("opal_unidentified", "built bundle", "closure", "own release", "cash rule", "same served state", "branch a", "branch b", "manifest anchor",
                 "business date", "moved member", "signed scope", "per-firm pin", "temporary fork", "reconverg"):
        if need not in low:
            fail("packet v3 does not carry %r" % need)
    print("OK: v3 names both pins, the port and the phrases")


def firm_line(t3, firm):
    rows = [x for x in t3.splitlines() if x.lstrip().startswith("|") and firm in x]
    return rows


def c2():
    t3, _ = v3_text()
    tot = totals()
    if tot["49financial"] != 32 or tot["inflection"] != 841 or not (249 <= tot["cottonwood"] <= 260):
        fail("the records read %r: 49financial 32, inflection 841 and cottonwood about 255 are the signed scope" % tot)
    want = {"49financial": (PIN1, PIN2), "cottonwood": (PIN2, PIN1), "inflection": (PIN2, PIN1)}
    for firm in FIRMS:
        rows = firm_line(t3, firm)
        ok = [r for r in rows if want[firm][0][:10] in r and want[firm][1][:10] not in r and re.search(r"(?<!\d)%d(?!\d)" % tot[firm], r)]
        if not ok:
            fail("the per-firm pin table needs a row for %s naming %s and %d, and not %s" % (firm, want[firm][0][:10], tot[firm], want[firm][1][:10]))
    if not re.search(r"(?<!\d)119(?!\d)", t3):
        fail("v3 must carry the 49financial 119 measured at pin 2 (why 49financial is not on pin 2)")
    low = t3.lower()
    if len(re.findall(r"unsigned", low)) < 2 or "coo half" not in low or "cto half" not in low:
        fail("both halves must read UNSIGNED at the packet bytes")
    print("OK: the per-firm pin table, the records' totals, both halves unsigned")


def c3():
    t3, _ = v3_text()
    for h in (PIN1, PIN2):
        t3 = t3.replace(h, "").replace(h[:10], "")
    no_long_digits(t3)
    counters(load(R_REC))
    print("OK: no long digit run, counters 0")


CHECKS = {"IB198-1-AC1": c1, "IB198-1-AC2": c2, "IB198-1-AC3": c3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p198_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    try:
        CHECKS[sys.argv[2]]()
    except SystemExit:
        raise
    print("%s PASS" % sys.argv[2])
