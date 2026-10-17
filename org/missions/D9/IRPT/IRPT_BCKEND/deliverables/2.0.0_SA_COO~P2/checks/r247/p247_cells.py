"""IRPT_BCKEND workstream ~PM round 6 (issuer 2.0.0_SA_COO~P2) -- the check of one READ order: the facts the served account-id HMAC list producer is built on (CTO ruling B, msg 10161).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IBHM1  IB-hm-1  seven repository questions answered with evidence that resolves
    AC1  q1 to q7 present, each with at least one evidence entry `path:line` whose file exists and whose line exists
    AC2  no id-like token in the record (no run of 8 or more digits, no acc_-shaped token) and the id kind named
    AC3  the registry rows to add listed, the two IAM statements named exactly, the hook regex and the equality flag stated
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.9.0_WK_IRPT_BCKEND~447/IBhm1_facts.json"
QS = ("q1", "q2", "q3", "q4", "q5", "q6", "q7")
fail, load = P6.fail, P6.load


def ac1(r):
    if not isinstance(r, dict):
        fail("the record must be a JSON object")
    for q in QS:
        e = r.get(q)
        if not isinstance(e, dict) or not str(e.get("answer", "")).strip():
            fail("%s must carry a non-empty answer" % q)
        ev = e.get("evidence")
        if not isinstance(ev, list) or not ev:
            fail("%s must carry at least one evidence entry path:line" % q)
        for c in ev:
            m = re.fullmatch(r"(.+):(\d+)", str(c))
            if not m:
                fail("%s evidence %r is not path:line" % (q, c))
            f = P6.ROOT / m.group(1)
            if not f.is_file():
                fail("%s evidence names a file that does not exist: %s" % (q, m.group(1)))
            n = sum(1 for _ in f.open("rb"))
            if int(m.group(2)) < 1 or int(m.group(2)) > n:
                fail("%s evidence line %s is past the end of %s (%d lines)" % (q, m.group(2), m.group(1), n))
    print("OK: seven answers, every evidence cite resolves to an existing file and line")


def ac2(r):
    s = json.dumps(r)
    if re.search(r"(?<![0-9a-fA-F-])\d{8,}(?![0-9a-fA-F])", s) or re.search(r"\bacc_[0-9a-f]{6,}", s):
        fail("the record carries an id-like token (a run of 8 or more digits or an acc_-shaped token)")
    if (r.get("q2") or {}).get("id_kind") not in ("account", "client") or not (r["q2"].get("field_names") or []):
        fail("q2 must name id_kind (account or client) and at least one field name")
    print("OK: no id-like token, the id kind and field names named")


def ac3(r):
    q4 = r.get("q4") or {}
    if not isinstance(q4.get("registry_rows_to_add"), list) or not q4["registry_rows_to_add"]:
        fail("q4.registry_rows_to_add must be a non-empty list (names only)")
    q5 = r.get("q5") or {}
    if sorted(q5.get("statements_to_add") or []) != ["s3:PutObject", "secretsmanager:GetSecretValue"]:
        fail("q5.statements_to_add must be exactly [secretsmanager:GetSecretValue, s3:PutObject] (CTO condition 3)")
    if not q5.get("existing_sids") or not q5.get("env_file") or not isinstance(q5.get("new_env_var"), bool):
        fail("q5 must list the existing Sids, name the env file and state new_env_var true or false")
    q3 = r.get("q3") or {}
    if not q3.get("hook_token_regex") or not isinstance(q3.get("upper_equal"), bool):
        fail("q3 must state the hook token regex and upper_equal true or false")
    if not isinstance((r.get("q6") or {}).get("flagged"), bool) or not (r.get("q7") or {}).get("model_test"):
        fail("q6.flagged must be true or false and q7.model_test must be named")
    print("OK: registry rows, the two IAM statements, the hook regex and equality, the gate and the model test")


CHECKS = {"IBHM1-AC1": ac1, "IBHM1-AC2": ac2, "IBHM1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p247_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
