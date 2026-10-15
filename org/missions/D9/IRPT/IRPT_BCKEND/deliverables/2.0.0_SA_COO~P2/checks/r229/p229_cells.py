"""IRPT_BCKEND workstream ~PO round 6 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the Orion Scope account feed (pair (b) ADDENDUM 1).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB229-1  IB-pr-596  the feed script, its two beside-files and its catalog row land on the Inflection gold chain; the first scheduled run is read
    AC1  the gates: both halves signed at the addendum blob, the builds merged, the live dispatch object equal to the repository copy, the roster column present, the runner grants, the live notification filter printed and not matching, the household bound stated
    AC2  the apply: the script and the two beside-files uploaded equal to the repository, the sidecar generated from address() output and hashed, the dispatch object edited by exactly the one row and its chain entries, the saved copy kept
    AC3  the first scheduled run: every account carries a daily factor or an ABSENT row with a reason class, no zero, the stored value is the daily factor, the request count within the stated bound, the keys inside the Inflection scope, the counters
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB229-1_apply_record.json"
ADD = D + "2.0.0_SA_COO~P2/ORION_PAIR_B_ADDENDUM_1_SCOPE_ACCOUNT_FEED.md"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_1_SCOPE_FEED_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_ORION_PAIR_B_ADDENDUM_1_SCOPE_FEED_CTO_HALF.md"
BLOB = "1e138cbeeaa12d4bf972cf579851546a7e3b3b37"
REASONS = ("NO_GROUP", "GROUP_NO_SERIES", "NO_START_DATE_AT_SOURCE", "SERIES_ENDED_AT_SOURCE")
fail, load, is_int = P6.fail, P6.load, P6.is_int
ROOT = Path(".")


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def hex64(x, what):
    if not re.fullmatch(r"[0-9a-f]{64}", str(x)):
        fail("%s must be a 64-hex sha256" % what)


def ac1(r):
    if BLOB[:10] not in text(COO_HALF) or "SIGNED" not in text(COO_HALF) or BLOB[:10] not in text(CTO_HALF) or "SIGNED" not in text(CTO_HALF):
        fail("both halves must read SIGNED at the addendum blob %s" % BLOB[:10])
    g = r.get("gates") or {}
    if g.get("addendum_blob") != BLOB or g.get("both_halves_signed") is not True:
        fail("gates.addendum_blob must be %s and both_halves_signed true" % BLOB)
    b = g.get("builds_merged") or {}
    if not (b.get("IB-pr-586") is True and b.get("IB-pr-594") is True):
        fail("gates.builds_merged must read true for IB-pr-586 and IB-pr-594 (the CTO's addendum-2 condition 1: 594 gates both applies)")
    d = g.get("dispatch_object") or {}
    hex64(d.get("live_sha256"), "dispatch_object.live_sha256")
    if d.get("live_sha256") != d.get("repository_sha256") or d.get("equal") is not True:
        fail("the live dispatch object must equal the repository copy (COO half condition 2): a difference is a STOP and a row")
    if g.get("roster_column_present") not in ("accountStartDate", "account_start_date"):
        fail("gates.roster_column_present must name the roster column found in a live accounts_v2 snapshot (row W429-S2)")
    ru = g.get("runner_role") or {}
    if not (ru.get("secret_read_allowed") is True and ru.get("feed_prefix_write_allowed") is True and ru.get("cross_bucket_write_checked") is True):
        fail("gates.runner_role must read secret_read_allowed, feed_prefix_write_allowed and cross_bucket_write_checked true (rows W429-S3; COO half condition 3)")
    n = g.get("notification_filter") or {}
    if n.get("printed") is not True or n.get("matches_feed_key") is not False:
        fail("gates.notification_filter must be printed from the LIVE configuration and must not match the feed's bronze key (CTO half condition 2)")
    if not (is_int(g.get("household_count")) and g["household_count"] >= 1 and g.get("request_bound") == g["household_count"]):
        fail("gates.request_bound must equal the household count read from the roster at the apply, one call per household (CTO half condition 3)")
    if g.get("write_set_inflection_only") is not True:
        fail("gates.write_set_inflection_only must be true (any key outside orion/inflection/ is a STOP)")
    print("OK: gates met; bound %d" % g["household_count"])


def ac2(r):
    a = r.get("apply") or {}
    for k in ("script", "trading_calendar"):
        u = a.get(k) or {}
        hex64(u.get("uploaded_sha256"), k + ".uploaded_sha256")
        if u.get("uploaded_sha256") != u.get("repository_sha256"):
            fail("%s: the uploaded object must equal the repository file" % k)
    s = a.get("sidecar") or {}
    hex64(s.get("sha256"), "sidecar.sha256")
    if s.get("generated_from") != "address()" or sorted(s.get("keys") or []) != ["bronze_key_prefix", "bucket", "silver_key_prefix"]:
        fail("the sidecar must be generated from address() output with the keys bucket, bronze_key_prefix and silver_key_prefix")
    d = a.get("dispatch_edit") or {}
    hex64(d.get("saved_copy_sha256"), "dispatch_edit.saved_copy_sha256")
    if d.get("rows_added") != 1 or not (is_int(d.get("chain_entries_added")) and d["chain_entries_added"] >= 1) or d.get("other_lines_changed") != 0:
        fail("the dispatch object must change by exactly one catalog row, its chain entries and no other line")
    if d.get("chain_entries_added") != d.get("chains_carrying_perf"):
        fail("chain_entries_added must equal chains_carrying_perf (every chain that carries the performance pull gets the entry)")
    if a.get("rollback_performed") is not False:
        fail("rollback_performed must be false for a landed apply (Branch B is reported, not graded as a pass)")
    print("OK: uploads equal the repository; sidecar from address(); dispatch edited by one row")


def ac3(r):
    f = r.get("first_run") or {}
    if f.get("exit_code") != 0 or f.get("tolerated_failure") is not False:
        fail("first_run must read exit_code 0 and tolerated_failure false (a tolerated failure of the new step is a row, not a pass)")
    cov = f.get("coverage") or {}
    den, ret, ab = cov.get("denominator"), cov.get("returned"), cov.get("absent")
    if not (is_int(den) and den >= 1 and is_int(ret) and is_int(ab) and ret + ab == den):
        fail("coverage: returned plus absent must equal the printed denominator (every account carries a factor or an ABSENT row)")
    rs = cov.get("absent_by_reason") or {}
    if sum(rs.values()) != ab or not all(k in REASONS for k in rs):
        fail("coverage.absent_by_reason must sum to absent and use only %s" % (REASONS,))
    if cov.get("zero_returns_written") != 0 or cov.get("value_stored") != "daily_factor":
        fail("zero_returns_written must be 0 and value_stored must read daily_factor (CTO addendum-2 condition 1)")
    g = r.get("gates") or {}
    if not (is_int(f.get("requests_made")) and 0 < f["requests_made"] <= g.get("request_bound", 0)):
        fail("first_run.requests_made must be within the stated bound (a higher count is a STOP and a row)")
    if f.get("calc_gross_of_fees_false_on_every_request") is not True:
        fail("every request must have carried calcGrossOfFees false")
    if f.get("keys_outside_inflection_scope") != 0:
        fail("keys_outside_inflection_scope must be 0")
    c = r.get("counters") or {}
    want = {"function_updates": 0, "lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "terraform_changes": 0, "existing_keys_changed": 0, "secrets_printed": 0}
    for k, v in want.items():
        if c.get(k) != v:
            fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the first run covers %d accounts; %d returned, %d absent" % (den, ret, ab))


CHECKS = {"IB229-1-AC1": ac1, "IB229-1-AC2": ac2, "IB229-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p229_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
