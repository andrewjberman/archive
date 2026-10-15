"""IRPT_BCKEND workstream ~PL round 2 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: 49 Financial's anatomy and exemption-alone DELTA on the TRANSPLANT tree (pin 1 plus the exemption).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB233-1  IB-pr-602  the CTO's re-measure (ADDENDUM 1 @334382c7f4, msg 8538): the anatomy of 49 Financial's refusal and the exemption-alone DELTA, both on the code of IB-pr-595's tree
    AC1  the identity and method: base commit, read date, days, the tree named by the sha256 of its two transplanted files, equal to IB-pr-595's record; the CUSIP port present, the one-date bypass absent
    AC2  the arithmetic: the anatomy (lost = exempted + remaining, classes sum, classified_security_lost counts, the remaining conditions) and the DELTA (with = without + the exemption alone, no other node, no amount, the gate outcomes and the second fire)
    AC3  notes, the six counters 0, no long digit run (no id)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for sub in ("r196", "r218", "r220"):
    sys.path.insert(0, str(HERE.parent / sub))
import p196_cells as P6  # noqa: E402
import p218_cells as P8  # noqa: E402
import p220_cells as P20  # noqa: E402

REC = P6.D + "0.9.0_WK_IRPT_BCKEND~437/IB233-1_49f_transplant_reread.json"
SRC = P6.D + "0.9.0_WK_IRPT_BCKEND~434/IB228-1_holdings_transplant_candidate.json"
fail, load, count = P6.fail, P6.load, P8.count


def transplant_hashes():
    doc = load(SRC)
    members = (((doc.get("firms") or {}).get("49financial") or {}).get("changed_members")) or []
    return sorted(m.get("sha256_transplanted") for m in members if isinstance(m, dict))


def ac1(r):
    P8.identity(r)
    P8.iso(r.get("candidate_day"), "candidate_day")
    P8.iso(r.get("served_day"), "served_day")
    if r.get("firm_scope") != "49financial":
        fail("firm_scope must read 49financial")
    P8.text(r.get("builder"), 8, "builder")
    t = r.get("tree") or {}
    want = transplant_hashes()
    got = sorted([t.get("holdings_snapshot_sha256"), t.get("publication_sha256")])
    if len(want) != 2 or got != want:
        fail("tree.holdings_snapshot_sha256 and tree.publication_sha256 must equal IB-pr-595's transplanted files for 49financial (%s)" % SRC)
    if t.get("cusip_port_present") is not True or t.get("one_date_bypass_absent") is not True:
        fail("tree must read cusip_port_present true and one_date_bypass_absent true")
    low = r["method"].lower()
    if "without" not in low or "transplant" not in low:
        fail("the method must name the transplant tree and state the WITH and WITHOUT runs")
    print("OK: identity; the tree is IB-pr-595's 49 Financial transplant")


def delta(e):
    wn, wa = P8.side(e.get("without"), "without")
    yn, ya = P8.side(e.get("with"), "with")
    ex = e.get("exemption_alone") or {}
    added_n, added_a = count(ex.get("nodes_added"), "nodes_added"), count(ex.get("accounts_added"), "accounts_added")
    n_ex = count(e["with"].get("exempted_accounts"), "with.exempted_accounts")
    applied = e["with"].get("listing_applied")
    if not isinstance(applied, bool):
        fail("with.listing_applied must be a boolean")
    if yn != wn + added_n or ya != wa + added_a:
        fail("the counts with must equal the counts without plus the exemption alone")
    if ex.get("other_nodes_changed") != 0 or ex.get("amount_added_usd") != 0:
        fail("other_nodes_changed and amount_added_usd must be 0 (the exemption alone)")
    if applied:
        if e["with"]["outcome"] != "PUBLISHED" or added_a != n_ex or added_n != n_ex:
            fail("a listing applied means PUBLISHED and exactly one account node per exempted account")
    else:
        if added_n != 0 or added_a != 0:
            fail("with no listing applied the exemption alone adds no node")
        if n_ex > 0 and e["with"]["outcome"] != "REFUSED":
            fail("exempted accounts without a listing can only be a REFUSED gate")
    if n_ex > 0:
        s2 = e.get("second_fire") or {}
        if s2.get("exempt_again") is not True:
            fail("the second fire must exempt the account again")
        if s2.get("outcome_account_lost") is not ("account_lost" in e["with"]["conditions"]):
            fail("the second fire may refuse as account_lost only where the first run still does")
    elif added_n != 0 or e["with"]["conditions"] != e["without"]["conditions"]:
        fail("with no exempted account the two runs must be identical")


def ac2(r):
    a = r.get("anatomy")
    if not isinstance(a, dict):
        fail("anatomy must be an object")
    P20.ac2(a)
    d = r.get("delta")
    if not isinstance(d, dict):
        fail("delta must be an object")
    delta(d)
    if "account_lost" in d["with"]["conditions"]:
        rem = (a.get("lost_accounts") or {}).get("remaining")
        if not (isinstance(rem, int) and rem > 0):
            fail("the DELTA run still refuses on account_lost, so the anatomy must count remaining lost accounts above 0")
    print("OK: anatomy and DELTA agree")


CHECKS = {"IB233-1-AC1": lambda: ac1(load(REC)), "IB233-1-AC2": lambda: ac2(load(REC)), "IB233-1-AC3": lambda: P8.ac3(load(REC))}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p233_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
