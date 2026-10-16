"""IRPT_BCKEND workstream ~PM round 5 (issuer 2.0.0_SA_COO~P2) -- the check of one DRIVE order: one export by a direct invoke with synthetic claims (CTO ruling B, msg 9743), to close L6 of the IB-pr-521 ledger.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB246-1  IB-pr-615  ONE direct invoke of irpt-export-render with synthetic claims (admin, firm 49financial) creates ONE export; read it and one pre-existing receipt
    AC1  the gates: the ledger open at L6 only, the function at the signed digest, the CTO ruling (B) cited
    AC2  the claims: role admin, firm 49financial, no user row minted, the authorizer stated not exercised
    AC3  the reads: the old receipt readable, ONE new export readable with no email, the counters
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB246-1_export_drive_record.json"
DIGEST = "5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4="
fail, load = P6.fail, P6.load


def ac1(r):
    g = r.get("gates") or {}
    if g.get("ledger_open_l6_only") is not True or g.get("function_code_sha256") != DIGEST:
        fail("gates: the ledger must read OPEN at L6 only and the function CodeSha256 must equal the signed digest %s" % DIGEST)
    if g.get("cto_ruling_msg") != 9743:
        fail("gates: the CTO ruling (B), msg 9743, must be cited")
    print("OK: the gates: L6 only open, the signed digest live, the CTO ruling (B) cited")


def ac2(r):
    c = r.get("claims") or {}
    if c.get("role") != "admin" or c.get("firm") != "49financial":
        fail("claims: role admin and firm 49financial exactly (CTO ruling B, msg 9743)")
    if c.get("user_row_minted") is not False or c.get("authorizer_exercised") is not False:
        fail("claims: user_row_minted false and authorizer_exercised false (no user row; the receipt says the authorizer was not exercised)")
    print("OK: the claims were admin/49financial, no user row minted, the authorizer stated not exercised")


def ac3(r):
    o = r.get("old_receipt") or {}
    if o.get("readable") is not True or not o.get("status"):
        fail("old_receipt must read readable true with a status word (a refusal here is a finding about IB-pr-521)")
    n = r.get("new_export") or {}
    if n.get("creating_invokes") != 1 or n.get("http_class") != "2xx" or n.get("readable") is not True or not n.get("status") or n.get("emails_sent") != 0:
        fail("new_export must read creating_invokes 1, http_class 2xx, readable true, a status word and emails_sent 0 (ONE creating invoke, no email)")
    k = r.get("counters") or {}
    want = {"creating_invokes": 1, "users_minted": 0, "users_removed": 0, "lambda_code_changes": 0, "iam_changes": 0, "schedule_changes": 0, "files_deleted": 0, "markers_closed": 0}
    for key, val in want.items():
        if k.get(key) != val:
            fail("counters.%s must read %s, read %r" % (key, val, k.get(key)))
    if not (isinstance(k.get("status_reads"), int) and k["status_reads"] >= 1):
        fail("counters.status_reads must be an integer of 1 or more (the old receipt and the new export are each read)")
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the old receipt readable, ONE new export readable, no email, the counters")


CHECKS = {"IB246-1-AC1": ac1, "IB246-1-AC2": ac2, "IB246-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p246_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
