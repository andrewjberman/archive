"""IRPT_BCKEND workstream ~PO round 10 (issuer 2.0.0_SA_COO~N2) -- the checks of the WORLD apply order IB-pn-4 (the Scope feed script with its region named).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL: <reason>" last, exit 0 or 1.
Grades the apply record the seat writes at deliverables/0.7.0_AE_CloudOps~IB2/IBN4-1_apply_record.json (counts, hashes, flags only).

  IBN4-AC1  the gates read before any write: ADDENDUM 4 at its blob with both halves, the builder cell IB-pn-3 complete, the live
            dispatch object equal to the repository copy before the feed's row, no other open ledger on the chain, the bound
            equal to the household count, the live sidecar equal to the builder-generated address and the calendar object
            present, and the apply timed outside the CTO's band and not on the Inflection transaction day
  IBN4-AC2  the apply: the replaced script object hashed and saved (it is the Branch B restore of the first apply, or ADDENDUM 3's
            bytes; any other hash is a STOP), the uploaded sha256 equal to the new script's, the THREE-PART smoke clean over the
            live code prefixes, the dispatch object changed by exactly one row and its chain entries, no rollback
  IBN4-AC3  the first scheduled run, read from the STEP LOG: exit 0, not tolerated, no skipped day, coverage returned plus absent
            equals the denominator, no zero, the daily factor stored, requests within the bound, calcGrossOfFees false, nothing
            outside the Inflection scope
"""
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
ADDENDUM = D + "2.0.0_SA_COO~N2/ORION_PAIR_B_ADDENDUM_4_SCOPE_FEED_REGION.md"
COO_HALF = D + "2.0.0_SA_COO~N2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_4_SCOPE_FEED_REGION_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_4_SCOPE_FEED_REGION_CTO_HALF.md"
RECORD = D + "0.7.0_AE_CloudOps~IB2/IBN4-1_apply_record.json"
BUILDER_ORDER = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pn-3.scope-feed-region.md"
ADDENDUM_BLOB = "22172a052e8de14c97c5eed0846fa78239964ea3"
SCRIPT_SHA = "a92589d697bac504d5338b434d49c5cb1ccb09926c6fe8720fc6a72c5de8dfae"
REPLACED_OK = ("ab5905d71d397a3bfb2bd594b91ff15d23ed29ebde0c3e6a98ee88fd14bf6db2",   # the first apply's bytes (Branch B restored them)
               "4527c57f6eed54ac62d732468419a83adce08fec80916f333800db5d2d0a8d32")   # ADDENDUM 3's bytes
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def fail(cid, why):
    print("%s FAIL: %s" % (cid, why))
    sys.exit(1)


def need(cid, cond, why):
    if not cond:
        fail(cid, why)


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


def schedule_ok(stamp):
    """Outside the weekday 11:30Z to 14:15Z band and not Tuesday 2026-10-20 (the Inflection transaction day)."""
    try:
        when = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return False
    if when.date() == dt.date(2026, 10, 20):
        return False
    minutes = when.hour * 60 + when.minute
    return not (when.weekday() < 5 and 11 * 60 + 30 <= minutes < 14 * 60 + 15)


def ac1(root):
    cid = "IBN4-AC1"
    rec = load(root, cid)
    add = root / ADDENDUM
    need(cid, add.is_file() and blob(add) == ADDENDUM_BLOB, "the addendum is not at blob " + ADDENDUM_BLOB)
    for half in (COO_HALF, CTO_HALF):
        p = root / half
        need(cid, p.is_file() and ADDENDUM_BLOB[:8] in p.read_text(encoding="utf-8"), "half absent or not bound to the blob: " + half)
    need(cid, "<status>complete</status>" in (root / BUILDER_ORDER).read_text(encoding="utf-8"), "IB-pn-3 is not complete")
    g = rec.get("gates", {})
    need(cid, g.get("addendum_blob") == ADDENDUM_BLOB and g.get("both_halves_signed") is True, "record: addendum blob or halves")
    disp = g.get("dispatch_object", {})
    need(cid, HEX64.match(str(disp.get("live_sha256", ""))) and disp.get("live_sha256") == disp.get("repository_sha256")
         and disp.get("equal") is True, "record: the live dispatch object is not equal to the repository copy")
    need(cid, g.get("other_open_ledger_on_chain") is False, "record: another ledger or window is open on the chain")
    rr = g.get("runner_role", {})
    need(cid, rr.get("secret_read_allowed") is True and rr.get("feed_prefix_write_allowed") is True, "record: runner role grants")
    hc, bound = g.get("household_count"), g.get("request_bound")
    need(cid, type(hc) is int and 0 < hc <= 294 and bound == hc, "record: request_bound must equal the household count (at most 294)")
    sc = g.get("sidecar", {})
    need(cid, HEX64.match(str(sc.get("live_sha256", ""))) and sc.get("equals_generated_address") is True
         and g.get("calendar_object_present") is True, "record: the live sidecar must equal the builder-generated address and the calendar object be present")
    need(cid, schedule_ok(rec.get("apply", {}).get("applied_at_utc")), "record: the apply is inside the weekday 11:30Z-14:15Z band or on 2026-10-20")
    need(cid, str(rec.get("ledger_entry", "")).startswith("org/critical_paths/change_management/"), "record: ledger entry not named")


def ac2(root):
    cid = "IBN4-AC2"
    rec = load(root, cid)
    ap = rec.get("apply", {})
    rep = ap.get("replaced_script", {})
    need(cid, rep.get("sha256") in REPLACED_OK and rep.get("saved_copy_sha256") == rep.get("sha256"),
         "record: the replaced script object must be hashed and saved and be one of the two expected objects")
    need(cid, ap.get("script", {}).get("uploaded_sha256") == SCRIPT_SHA, "record: the uploaded script's sha256 is not " + SCRIPT_SHA)
    sm = ap.get("import_smoke", {})
    where_ok = sm.get("ran_on_runner") is True or (sm.get("ran_on_runner") is False and sm.get("fallback_host") is True
                                                    and bool(str(sm.get("python_version", "")).strip()))
    parts = all(sm.get(k) is True for k in ("part_i_import_and_prefixes", "part_ii_session_token_client_under_scrubbed_env", "part_iii_plan_only_run"))
    need(cid, where_ok and parts and sm.get("built_from_live_prefixes") is True and sm.get("exit_code") == 0
         and sm.get("orion_requests") == 0, "record: the three-part smoke over the live code prefixes did not run clean")
    de = ap.get("dispatch_edit", {})
    n = de.get("chain_entries_added")
    need(cid, de.get("rows_added") == 1 and type(n) is int and n > 0 and n == de.get("chains_carrying_perf")
         and de.get("other_lines_changed") == 0 and HEX64.match(str(de.get("saved_copy_sha256", ""))),
         "record: the dispatch object must change by exactly one row and its entries on every chain, nothing else")
    need(cid, ap.get("rollback_performed") is False, "record: a rollback was performed")


def ac3(root):
    cid = "IBN4-AC3"
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


CHECKS = {"IBN4-AC1": ac1, "IBN4-AC2": ac2, "IBN4-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: pn4_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    CHECKS[sys.argv[2]](Path(sys.argv[1]).resolve())
    print("%s PASS" % sys.argv[2])
