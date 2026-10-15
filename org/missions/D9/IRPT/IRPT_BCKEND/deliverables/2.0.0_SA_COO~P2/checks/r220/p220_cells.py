"""IRPT_BCKEND workstream ~PL round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one READ cell: the anatomy of 49 Financial's remaining refusal.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB220-1  IB-pr-584  after the exemption, why 49 Financial still refuses: the lost accounts by class (counts only), what classified_security_lost counts, the conditions that remain
    AC1  the identity and method: base commit, read date, candidate and served days, the claim measured
    AC2  the arithmetic: lost = exempted + remaining; the classes of the remaining sum to it; the classified_security_lost counts; the remaining conditions
    AC3  notes, the six counters 0, no long digit run (no id)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
sys.path.insert(0, str(HERE.parent / "r218"))
import p196_cells as P6  # noqa: E402
import p218_cells as P8  # noqa: E402

REC = P6.D + "0.9.0_WK_IRPT_BCKEND~426/IB220-1_49f_refusal_anatomy.json"
CLASSES = ("exempted_absent_at_source", "closed_by_directory", "in_source_with_positions", "evidence_incomplete", "other")
fail, load, count = P6.fail, P6.load, P8.count


def ac1(r):
    P8.identity(r)
    P8.iso(r.get("candidate_day"), "candidate_day")
    P8.iso(r.get("served_day"), "served_day")
    if r.get("firm_scope") != "49financial":
        fail("firm_scope must read 49financial")
    print("OK: identity and method")


def ac2(r):
    la = r.get("lost_accounts") or {}
    total = count(la.get("total"), "lost_accounts.total")
    cls = la.get("classes")
    if not isinstance(cls, dict) or sorted(cls) != sorted(CLASSES):
        fail("lost_accounts.classes must hold exactly %s" % (CLASSES,))
    vals = {k: count(v, "classes." + k) for k, v in cls.items()}
    if sum(vals.values()) != total:
        fail("the classes must sum to the lost accounts (%d vs %d)" % (sum(vals.values()), total))
    if count(la.get("exempted"), "lost_accounts.exempted") != vals["exempted_absent_at_source"]:
        fail("lost_accounts.exempted must equal the exempted class")
    if count(la.get("remaining"), "lost_accounts.remaining") != total - vals["exempted_absent_at_source"]:
        fail("remaining must equal lost minus exempted")
    csl = r.get("classified_security_lost") or {}
    n = count(csl.get("total"), "classified_security_lost.total")
    count(csl.get("served_placed_total"), "classified_security_lost.served_placed_total")
    count(csl.get("candidate_unclassified_total"), "classified_security_lost.candidate_unclassified_total")
    if n > csl["served_placed_total"] or n > csl["candidate_unclassified_total"]:
        fail("classified_security_lost.total cannot exceed the served placed securities nor the candidate unclassified securities")
    P8.text(csl.get("reading"), 60, "classified_security_lost.reading")
    conds = r.get("conditions_remaining")
    if not isinstance(conds, list) or not all(isinstance(c, str) and c for c in conds):
        fail("conditions_remaining must list the gate's condition names with every exemption applied")
    if (total - vals["exempted_absent_at_source"] > 0) != ("account_lost" in conds) or (n > 0) != ("classified_security_lost" in conds):
        fail("conditions_remaining must agree with the remaining lost accounts and the classified_security_lost count")
    print("OK: %d lost accounts, %d exempted, classes sum; %d classified securities lost" % (total, vals["exempted_absent_at_source"], n))


CHECKS = {"IB220-1-AC1": lambda: ac1(load(REC)), "IB220-1-AC2": lambda: ac2(load(REC)), "IB220-1-AC3": lambda: P8.ac3(load(REC))}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p220_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]]()
    print("%s PASS" % sys.argv[2])
