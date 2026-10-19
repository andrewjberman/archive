"""IRPT_BCKEND workstream ~PO round 12 (issuer 2.0.0_SA_COO~N2) -- the checks of the WORLD apply order IB-pn-7 (the Scope feed script that
writes the raw replies once per run, ORION pair (b) ADDENDUM 5; no dispatch change).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL: <reason>" last, exit 0 or 1.
Grades the apply record the seat writes at deliverables/0.7.0_AE_CloudOps~IB2/IBN7-1_apply_record.json (counts, hashes, flags only).

  IBN7-AC1  the gates read before any write: ADDENDUM 5 at its blob with both halves, the writer cell IB-pn-5 complete, the repository
            script at HEAD hashing to the addendum's sha256 (read by this check, not the record), no other act of the seat open on the
            chain, the feed's row still in the live dispatch object, the bound equal to the household count, the live sidecar equal to
            the builder-generated address and the calendar present, the notification filter not matching the feed's keys, and the
            apply timed outside the CTO's band and not on the Inflection transaction day
  IBN7-AC2  the apply: the replaced script object hashed and saved (it must be the pn-4 object), the uploaded sha256 equal to the new
            script's, the THREE-PART smoke clean over the live code prefixes, the run object's address printed from address() or the
            sidecar with its partition, object name and bucket-and-prefix equal to the builder's, the dispatch object unchanged, no rollback
  IBN7-AC3  the first scheduled run, read from the STEP LOG: exit 0, not tolerated, no skipped day, coverage returned plus absent equals
            the denominator, no zero, the daily factor stored, requests within the bound, calcGrossOfFees false, nothing outside the
            Inflection scope, exactly ONE run object under run=<pull_date>, and every day's envelope v2 without responses that names it
"""
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/"
ADDENDUM = D + "2.0.0_SA_COO~N2/ORION_PAIR_B_ADDENDUM_5_SCOPE_FEED_RAW_ONCE_AND_BACKFILL.md"
COO_HALF = D + "2.0.0_SA_COO~N2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_5_SCOPE_FEED_RAW_ONCE_AND_BACKFILL_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_5_SCOPE_FEED_RAW_ONCE_AND_BACKFILL_CTO_HALF.md"
RECORD = D + "0.7.0_AE_CloudOps~IB2/IBN7-1_apply_record.json"
WRITER_ORDER = "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pn-5.scope-feed-raw-replies-once-per-run.md"
SCRIPT = "data/inf/manual_api/pull_inflection_scope_account_returns.py"
ADDENDUM_BLOB = "619dbf431bc578cf22bb59114f5e289d7f9c4c94"
SCRIPT_SHA = "acfe390bda5af03e3c38330ece8f18d32a87f122594f593f855fc6d802eb21a3"
REPLACED_EXPECT = "a92589d697bac504d5338b434d49c5cb1ccb09926c6fe8720fc6a72c5de8dfae"   # the pn-4 object
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
    cid = "IBN7-AC1"
    rec = load(root, cid)
    add = root / ADDENDUM
    need(cid, add.is_file() and blob(add) == ADDENDUM_BLOB, "the addendum is not at blob " + ADDENDUM_BLOB)
    for half in (COO_HALF, CTO_HALF):
        p = root / half
        need(cid, p.is_file() and ADDENDUM_BLOB[:10] in p.read_text(encoding="utf-8"), "half absent or not bound to the blob: " + half)
    need(cid, "<status>complete</status>" in (root / WRITER_ORDER).read_text(encoding="utf-8"), "IB-pn-5 is not complete")
    script = root / SCRIPT
    need(cid, script.is_file() and hashlib.sha256(script.read_bytes()).hexdigest() == SCRIPT_SHA, "the repository script does not hash to " + SCRIPT_SHA)
    g = rec.get("gates", {})
    need(cid, g.get("addendum_blob") == ADDENDUM_BLOB and g.get("both_halves_signed") is True, "record: addendum blob or halves")
    need(cid, g.get("other_act_open_on_chain") is False, "record: another act of the seat or another ledger is open on the chain")
    need(cid, g.get("dispatch_object", {}).get("feed_row_present") is True and HEX64.match(str(g.get("dispatch_object", {}).get("live_sha256", ""))),
         "record: the feed's catalog row is not in the live dispatch object")
    rr = g.get("runner_role", {})
    need(cid, rr.get("secret_read_allowed") is True and rr.get("feed_prefix_write_allowed") is True, "record: runner role grants")
    hc, bound = g.get("household_count"), g.get("request_bound")
    need(cid, type(hc) is int and 0 < hc <= 294 and bound == hc, "record: request_bound must equal the household count (at most 294)")
    sc = g.get("sidecar", {})
    need(cid, HEX64.match(str(sc.get("live_sha256", ""))) and sc.get("equals_generated_address") is True
         and g.get("calendar_object_present") is True, "record: the live sidecar must equal the builder-generated address and the calendar object be present")
    need(cid, g.get("notification_filter_matches_feed_keys") is False, "record: the live notification filter matches a feed key shape (day or run object)")
    need(cid, schedule_ok(rec.get("apply", {}).get("applied_at_utc")), "record: the apply is inside the weekday 11:30Z-14:15Z band or on 2026-10-20")
    need(cid, str(rec.get("ledger_entry", "")).startswith("org/critical_paths/change_management/"), "record: ledger entry not named")


def ac2(root):
    cid = "IBN7-AC2"
    rec = load(root, cid)
    ap = rec.get("apply", {})
    rep = ap.get("replaced_script", {})
    need(cid, rep.get("sha256") == REPLACED_EXPECT and rep.get("saved_copy_sha256") == rep.get("sha256"),
         "record: the replaced script object must be the pn-4 object, hashed and saved")
    need(cid, ap.get("script", {}).get("uploaded_sha256") == SCRIPT_SHA, "record: the uploaded script's sha256 is not " + SCRIPT_SHA)
    sm = ap.get("import_smoke", {})
    where_ok = sm.get("ran_on_runner") is True or (sm.get("ran_on_runner") is False and sm.get("fallback_host") is True
                                                    and bool(str(sm.get("python_version", "")).strip()))
    parts = all(sm.get(k) is True for k in ("part_i_import_and_prefixes", "part_ii_session_token_client_under_scrubbed_env", "part_iii_plan_only_run"))
    need(cid, where_ok and parts and sm.get("built_from_live_prefixes") is True and sm.get("exit_code") == 0
         and sm.get("orion_requests") == 0, "record: the three-part smoke over the live code prefixes did not run clean")
    ra = ap.get("run_object_address", {})
    need(cid, ra.get("source") in ("builder", "sidecar") and ra.get("partition_equals_builder") is True
         and ra.get("object_name_equals_builder") is True and ra.get("bucket_and_prefix_equal_builder") is True,
         "record: the run object's address must be printed and equal the builder's in partition, object name, bucket and prefix")
    du = ap.get("dispatch_unchanged", {})
    need(cid, HEX64.match(str(du.get("sha256_before", ""))) and du.get("sha256_before") == du.get("sha256_after"),
         "record: the dispatch object must be unchanged by this order")
    need(cid, ap.get("rollback_performed") is False, "record: a rollback was performed")


def ac3(root):
    cid = "IBN7-AC3"
    rec = load(root, cid)
    fr = rec.get("first_run", {})
    need(cid, fr.get("read_from_step_log") is True and fr.get("exit_code") == 0 and fr.get("tolerated_failure") is False,
         "record: the step did not exit 0 clean in its own log")
    n = fr.get("days_complete")
    need(cid, type(n) is int and n >= 1 and fr.get("skipped_days") == 0 and fr.get("zero_returns") == 0
         and fr.get("keys_outside_inflection_scope") == 0, "record: days, skipped days, zero returns or keys outside the scope")
    cov = fr.get("coverage", {})
    den, ret, ab = cov.get("denominator"), cov.get("returned"), cov.get("absent")
    need(cid, all(type(v) is int for v in (den, ret, ab)) and den > 0 and ret + ab == den, "record: returned plus absent must equal the denominator")
    bound = rec.get("gates", {}).get("request_bound")
    need(cid, type(fr.get("requests_made")) is int and type(bound) is int and 0 < fr["requests_made"] <= bound, "record: requests exceed the bound")
    need(cid, fr.get("calc_gross_of_fees_false_on_every_request") is True and fr.get("stored_value") == "daily_factor",
         "record: fee basis or the stored value")
    ro = fr.get("run_object", {})
    need(cid, ro.get("keys") == 1 and ro.get("versions") == 1 and type(ro.get("bytes")) is int and ro["bytes"] > 0
         and HEX64.match(str(ro.get("sha256", ""))) and ro.get("partition_is_run_pull_date") is True,
         "record: exactly one run object (one version, bytes above zero, sha256, under run=<pull_date>) is required")
    env = fr.get("envelopes", {})
    need(cid, env.get("count") == n and env.get("schema_v2") is True and env.get("responses_member_absent") is True
         and env.get("raw_object_names_the_run_object") is True and env.get("raw_object_sha256_equals_stored") is True,
         "record: every day's envelope must be v2, carry no responses and name the one run object by key and sha256")
    need(cid, fr.get("silver", {}).get("count") == n and fr.get("silver", {}).get("columns_equal_first_run") is True,
         "record: silver must be present for every day with the first run's columns")
    need(cid, fr.get("new_keys_total") == 2 * n + 1, "record: new keys must be two per day plus the one run object")


CHECKS = {"IBN7-AC1": ac1, "IBN7-AC2": ac2, "IBN7-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: pn7_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    CHECKS[sys.argv[2]](Path(sys.argv[1]).resolve())
    print("%s PASS" % sys.argv[2])
