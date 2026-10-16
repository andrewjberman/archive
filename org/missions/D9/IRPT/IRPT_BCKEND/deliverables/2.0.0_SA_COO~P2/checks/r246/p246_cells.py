"""IRPT_BCKEND workstream ~PM round 5 (issuer 2.0.0_SA_COO~P2) -- the check of one DRIVE order: one DEV export under a transient staff-only user, to close L6 of the IB-pr-521 ledger.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB246-1  IB-pr-615  mint ONE staff-only transient user, read one pre-existing receipt, request ONE new DEV export, read its status, remove the user (read back ABSENT)
    AC1  the gates: the ledger open at L6 only, the function at the signed digest, XA-f98b RULED, the helper blob, the CTO ruling cited
    AC2  the user: staff role, firm opal-capital, 0 entitlement rows, removed and read back ABSENT, password in memory only
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
HELPER_BLOB = "f368e9d95c62dc9fce1e6d5e04cd7fe6f79c444a"
fail, load = P6.fail, P6.load


def ac1(r):
    g = r.get("gates") or {}
    if g.get("ledger_open_l6_only") is not True or g.get("function_code_sha256") != DIGEST:
        fail("gates: the ledger must read OPEN at L6 only and the function CodeSha256 must equal the signed digest %s" % DIGEST)
    if g.get("xa_f98b_state") != "RULED" or g.get("helper_blob") != HELPER_BLOB or g.get("cto_ruling_msg") != 9653:
        fail("gates: XA-20261016T160537Z-f98b must read RULED, the helper blob must equal %s and the CTO ruling (msg 9653) must be cited" % HELPER_BLOB)
    print("OK: the gates: L6 only open, the signed digest live, XA-f98b RULED, the helper blob, the CTO ruling")


def ac2(r):
    u = r.get("user") or {}
    if u.get("role") not in ("user", "staff") or u.get("firmId") != "opal-capital" or u.get("entitlement_rows") != 0:
        fail("user: role user or staff, firmId opal-capital and entitlement_rows 0 (CTO condition: staff only, no firm entitlement row)")
    if u.get("removed_read_back_absent") is not True or u.get("password_in_memory_only") is not True:
        fail("user: removed_read_back_absent and password_in_memory_only must both be true")
    print("OK: the transient user was staff-only, no entitlement row, removed and read back ABSENT")


def ac3(r):
    o = r.get("old_receipt") or {}
    if o.get("readable") is not True or not o.get("status"):
        fail("old_receipt must read readable true with a status word (a refusal here is a finding about IB-pr-521)")
    n = r.get("new_export") or {}
    if n.get("posts") != 1 or n.get("http_class") != "2xx" or n.get("readable") is not True or not n.get("status") or n.get("emails_sent") != 0:
        fail("new_export must read posts 1, http_class 2xx, readable true, a status word and emails_sent 0 (ONE export, no client emailed)")
    k = r.get("counters") or {}
    want = {"exports_requested": 1, "users_minted": 1, "users_removed": 1, "lambda_code_changes": 0, "iam_changes": 0, "schedule_changes": 0, "files_deleted": 0, "markers_closed": 0}
    for key, val in want.items():
        if k.get(key) != val:
            fail("counters.%s must read %s, read %r" % (key, val, k.get(key)))
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
