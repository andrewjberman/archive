"""IRPT_BCKEND workstream ~PO round 9 (issuer 2.0.0_SA_COO~N2) -- the checks of the WORLD apply order IB-pn-2.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL: <reason>" last, exit 0 or 1.
Grades the apply record the seat writes at deliverables/0.7.0_AE_CloudOps~IB2/IBN2-1_apply_record.json (counts, hashes, flags only).

  IBN2-AC1  the gates read before any write: the addendum at its blob, both halves present and bound to it, the builder cell
            complete, the live dispatch object equal to the repository copy, no other open ledger on the chain, the bound
            equal to the household count
  IBN2-AC2  the apply: the uploaded script's sha256 equals the corrected script's, the replaced object hashed and saved, the
            in-runner import smoke ran over the LIVE code prefixes with exit 0 and no Orion request, the dispatch object
            changed by exactly one row and its chain entries, no rollback
  IBN2-AC3  the first scheduled run, read from the STEP LOG: exit 0, not a tolerated failure, no skipped day, coverage
            returned plus absent equals the denominator, no zero, the daily factor stored, requests within the bound,
            calcGrossOfFees false on every request, nothing outside the Inflection scope
"""
import hashlib
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
ADDENDUM = D + "2.0.0_SA_COO~N2/ORION_PAIR_B_ADDENDUM_3_SCOPE_FEED_RUNNER_LAYOUT.md"
COO_HALF = D + "2.0.0_SA_COO~N2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_3_SCOPE_FEED_RUNNER_LAYOUT_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_3_SCOPE_FEED_RUNNER_LAYOUT_CTO_HALF.md"
RECORD = D + "0.7.0_AE_CloudOps~IB2/IBN2-1_apply_record.json"
BUILDER_ORDER = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pn-1.scope-feed-runner-layout.md"
ADDENDUM_BLOB = "d4b8c52eeeccbd176e22d7acbc072033d5ccbefc"
SCRIPT_SHA = "4527c57f6eed54ac62d732468419a83adce08fec80916f333800db5d2d0a8d32"
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def fail(cid, why):
    print("%s FAIL: %s" % (cid, why))
    sys.exit(1)


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def load(root, cid):
    path = root / RECORD
    if not path.is_file():
        fail(cid, "apply record absent: " + RECORD)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        fail(cid, "apply record is not JSON: %s" % exc)


def need(cid, cond, why):
    if not cond:
        fail(cid, why)


def ac1(root):
    cid = "IBN2-AC1"
    rec = load(root, cid)
    add = root / ADDENDUM
    need(cid, add.is_file() and blob(add) == ADDENDUM_BLOB, "the addendum is not at blob " + ADDENDUM_BLOB)
    for half in (COO_HALF, CTO_HALF):
        p = root / half
        need(cid, p.is_file() and ADDENDUM_BLOB[:10] in p.read_text(encoding="utf-8"), "half absent or not bound to the blob: " + half)
    need(cid, "<status>complete</status>" in (root / BUILDER_ORDER).read_text(encoding="utf-8"), "IB-pn-1 is not complete")
    g = rec.get("gates", {})
    need(cid, g.get("addendum_blob") == ADDENDUM_BLOB and g.get("both_halves_signed") is True, "record: addendum blob or halves")
    disp = g.get("dispatch_object", {})
    need(cid, HEX64.match(str(disp.get("live_sha256", ""))) and disp.get("live_sha256") == disp.get("repository_sha256")
         and disp.get("equal") is True, "record: the live dispatch object is not equal to the repository copy")
    need(cid, g.get("other_open_ledger_on_chain") is False, "record: another ledger or window is open on the chain")
    rr = g.get("runner_role", {})
    need(cid, rr.get("secret_read_allowed") is True and rr.get("feed_prefix_write_allowed") is True, "record: runner role grants")
    hc, bound = g.get("household_count"), g.get("request_bound")
    need(cid, type(hc) is int and hc > 0 and bound == hc, "record: request_bound must equal the household count read at the apply")
    need(cid, str(rec.get("ledger_entry", "")).startswith("org/critical_paths/change_management/"), "record: ledger entry not named")


def ac2(root):
    cid = "IBN2-AC2"
    rec = load(root, cid)
    ap = rec.get("apply", {})
    rep = ap.get("replaced_script", {})
    need(cid, HEX64.match(str(rep.get("sha256", ""))) and HEX64.match(str(rep.get("saved_copy_sha256", "")))
         and rep.get("sha256") == rep.get("saved_copy_sha256"), "record: the replaced script object is not hashed and saved")
    need(cid, ap.get("script", {}).get("uploaded_sha256") == SCRIPT_SHA, "record: the uploaded script's sha256 is not " + SCRIPT_SHA)
    sm = ap.get("import_smoke", {})
    need(cid, sm.get("ran_on_runner") is True and sm.get("built_from_live_prefixes") is True and sm.get("exit_code") == 0
         and sm.get("orion_requests") == 0, "record: the in-runner import smoke over the live code prefixes did not run clean")
    de = ap.get("dispatch_edit", {})
    n = de.get("chain_entries_added")
    need(cid, de.get("rows_added") == 1 and type(n) is int and n > 0 and n == de.get("chains_carrying_perf")
         and de.get("other_lines_changed") == 0 and HEX64.match(str(de.get("saved_copy_sha256", ""))),
         "record: the dispatch object must change by exactly one row and its entries on every chain, nothing else")
    need(cid, ap.get("rollback_performed") is False, "record: a rollback was performed")


def ac3(root):
    cid = "IBN2-AC3"
    rec = load(root, cid)
    fr = rec.get("first_run", {})
    need(cid, fr.get("read_from_step_log") is True and fr.get("exit_code") == 0 and fr.get("tolerated_failure") is False,
         "record: the step did not exit 0 clean in its own log")
    need(cid, fr.get("skipped_days") == 0 and fr.get("zero_returns") == 0 and fr.get("keys_outside_inflection_scope") == 0,
         "record: skipped days, zero returns or keys outside the scope")
    cov = fr.get("coverage", {})
    den, ret, ab = cov.get("denominator"), cov.get("returned"), cov.get("absent")
    need(cid, all(type(v) is int for v in (den, ret, ab)) and den > 0 and ret + ab == den, "record: returned plus absent must equal the denominator")
    bound = rec.get("gates", {}).get("request_bound")
    need(cid, type(fr.get("requests_made")) is int and type(bound) is int and 0 < fr["requests_made"] <= bound, "record: requests exceed the bound")
    need(cid, fr.get("calc_gross_of_fees_false_on_every_request") is True and fr.get("stored_value") == "daily_factor",
         "record: fee basis or the stored value")


CHECKS = {"IBN2-AC1": ac1, "IBN2-AC2": ac2, "IBN2-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: pn2_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    CHECKS[sys.argv[2]](Path(sys.argv[1]).resolve())
    print("%s PASS" % sys.argv[2])
