"""IRPT_BCKEND workstream ~PQ round 1 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the holdings EXEMPTION pair (three bundles, transplant candidates).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB236-1  IB-pr-605  mint the three holdings bundles from IB-pr-595's transplant candidates, once each, between fires, and read the first fire per firm
    AC1  the gates and the digest gate: both halves signed at the packet blob, the ledger of IB-pr-549 closed, the Branch B versions recorded, each built bundle equal to its digest, exactly two changed members plus SHA256SUMS, the CUSIP and bypass reads, the re-measure per firm
    AC2  the mints: the window, the ledger opened first, each firm's mint moving its bundle off its Branch B version with the landed bytes equal to the built bundle, the business date stated before the fire
    AC3  the first fire per firm (a stamp with a T-1 partition, or a named hold with the frontier unchanged), the exemption's after-read, the counters
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB236-1_apply_record.json"
PACKET = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_SIGNOFF_PACKET_HOLDINGS_EXEMPTION_PAIR.md"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_HOLDINGS_EXEMPTION_PAIR_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_HOLDINGS_EXEMPTION_PAIR_CTO_HALF.md"
BLOB = "b4ad2d79c98618d78350eb06775294960874dd4c"
DIGESTS = {"49financial": "d2eaf3056c1d", "cottonwood": "bc2e8f548556", "inflection": "bc2e8f548556"}
FIRMS = tuple(DIGESTS)
MEMBERS = ("data/assets/scripts/gold/investor_reporting/holdings_snapshot.py", "infra/aws/lambda/investor-reporting/holdings/publication.py", "SHA256SUMS")
fail, load, is_int = P6.fail, P6.load, P6.is_int


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def firms(r, section):
    s = r.get(section)
    if not isinstance(s, dict) or sorted(s) != sorted(FIRMS):
        fail("%s must hold exactly %s" % (section, FIRMS))
    return s


def ac1(r):
    for rel in (COO_HALF, CTO_HALF):
        t = text(rel)
        if BLOB[:10] not in t or "SIGNED" not in t.upper() and "GIVEN" not in t.upper():
            fail("both halves must read SIGNED or GIVEN at the packet blob %s: %s" % (BLOB[:10], rel))
    g = r.get("gates") or {}
    if g.get("packet_blob") != BLOB or g.get("both_halves_signed") is not True:
        fail("gates.packet_blob must be %s and both_halves_signed true" % BLOB)
    if g.get("one_change_at_a_time") is not True or g.get("ib_pr_549_ledger_closed") is not True:
        fail("gates.one_change_at_a_time and gates.ib_pr_549_ledger_closed must be true (IB-pr-549's after-read is the first change; this order follows it)")
    bb = firms(r, "branch_b_reread")
    for f in FIRMS:
        if not (bb[f].get("bundle_version_id") and bb[f].get("manifest_anchor_at_mint")):
            fail("branch_b_reread.%s must record bundle_version_id and manifest_anchor_at_mint" % f)
    dg = firms(r, "digest_gate")
    for f in FIRMS:
        e = dg[f]
        if not str(e.get("built_bundle_sha256", "")).startswith(DIGESTS[f]) or not re.fullmatch(r"[0-9a-f]{64}", str(e.get("built_bundle_sha256"))):
            fail("%s: the built bundle sha256 must be a 64-hex value starting %s (the signed digest)" % (f, DIGESTS[f]))
        if sorted(e.get("changed_members") or []) != sorted(MEMBERS):
            fail("%s: changed_members must be exactly %s" % (f, (MEMBERS,)))
        if e.get("allow_older_date_count") != 0 or e.get("drifted_members_equal_live") is not True:
            fail("%s: allow_older_date_count must be 0 and drifted_members_equal_live true" % f)
    if dg["49financial"].get("cusip_lines") != 12 or dg["49financial"].get("cusip_lines_live") != 12:
        fail("49financial: cusip_lines and cusip_lines_live must both read 12 (row S206: a reversal is a STOP)")
    rm = firms(r, "remeasure")
    fv = rm["49financial"]
    if fv.get("verdict") not in ("REFUSED_NO_NODE_MOVES", "PUBLISHED_ONE_LISTED_ACCOUNT", "PUBLISHED_TWO_LISTED_ACCOUNTS_AMOUNT_ZERO"):
        fail("remeasure.49financial.verdict must read REFUSED_NO_NODE_MOVES, PUBLISHED_ONE_LISTED_ACCOUNT or PUBLISHED_TWO_LISTED_ACCOUNTS_AMOUNT_ZERO (the signed branches and the CTO-accepted count, msg 9538)")
    if fv.get("verdict") == "PUBLISHED_TWO_LISTED_ACCOUNTS_AMOUNT_ZERO" and (fv.get("listed_accounts") != 2 or fv.get("amount_added_usd") != 0 or fv.get("other_nodes_changed") != 0 or fv.get("evidence_values_per_exempted_account") != 2):
        fail("remeasure.49financial at two listed accounts must read listed_accounts 2, amount_added_usd 0, other_nodes_changed 0 and one evidence value per exempted account (2)")
    cv = rm["cottonwood"]
    if cv.get("verdict") not in ("PUBLISHED_FOUR_LISTED_ACCOUNTS", "PUBLISHED_NO_LISTED_ACCOUNTS") or cv.get("nodes_added") != (4 if cv.get("verdict") == "PUBLISHED_FOUR_LISTED_ACCOUNTS" else 0) or cv.get("other_nodes_changed") != 0:
        fail("remeasure.cottonwood must read PUBLISHED_FOUR_LISTED_ACCOUNTS with nodes_added 4, or PUBLISHED_NO_LISTED_ACCOUNTS with nodes_added 0, and other_nodes_changed 0 (any other is a STOP for Cottonwood)")
    iv = rm["inflection"].get("verdict")
    if iv not in ("REFUSED_SOURCE_FRONTIER_OLDER_NO_NODE_MOVES", "PUBLISHED_LISTED_ACCOUNTS_AMOUNT_ZERO", "PUBLISHED_NO_LISTED_ACCOUNTS", "STOP_INFLECTION_ONLY"):
        fail("remeasure.inflection.verdict must be one of the three signed readings (CTO half: any other verdict is a STOP for Inflection only)")
    if iv == "STOP_INFLECTION_ONLY" and (r.get("mints") or {}).get("inflection"):
        fail("an Inflection STOP means Inflection is not minted")
    print("OK: gates, digest gate and the re-measure agree with the signed pair")


def ac2(r):
    w = r.get("window") or {}
    for k in ("last_fire_all_success_utc", "mint_start_utc", "mint_end_utc", "next_fire_utc"):
        if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", str(w.get(k))):
            fail("window.%s must be an ISO UTC time" % k)
    if not (w["last_fire_all_success_utc"] < w["mint_start_utc"] <= w["mint_end_utc"] < w["next_fire_utc"]):
        fail("the mints must lie after the day's fires and before the next fire")
    if w.get("minutes_before_next_fire") is None or not is_int(w["minutes_before_next_fire"]) or w["minutes_before_next_fire"] < 30:
        fail("window.minutes_before_next_fire must be 30 or more")
    lg = r.get("ledger") or {}
    if lg.get("opened_before_first_mint") is not True or not str(lg.get("entry", "")).startswith("org/critical_paths/change_management/"):
        fail("ledger must name an entry under org/critical_paths/change_management/ opened before the first mint")
    mints = r.get("mints") or {}
    done = [f for f in FIRMS if mints.get(f)]
    if not done:
        fail("at least one firm must be minted")
    for f in done:
        m = mints[f]
        if m.get("before_version_id") == m.get("after_version_id") or not m.get("after_version_id"):
            fail("%s: the mint must move the bundle off its Branch B version" % f)
        if m.get("after_sha256_equals_built") is not True:
            fail("%s: the landed bytes must equal the built bundle" % f)
    bd = r.get("business_date_statement") or {}
    if not (bd.get("stated_at_utc") and bd.get("t_minus_1") and bd["stated_at_utc"] < bd.get("fire_utc", "9")):
        fail("business_date_statement must be stated BEFORE the fire (stated_at_utc < fire_utc) with t_minus_1")
    print("OK: window, ledger and mints; the business date stated before the fire")


def ac3(r):
    ar = r.get("after_read") or {}
    mints = r.get("mints") or {}
    for f in [x for x in FIRMS if mints.get(x)]:
        a = ar.get(f) or {}
        if a.get("outcome") == "STAMPED_T_MINUS_1":
            if a.get("t1_partition_under_it") is not True:
                fail("%s: a stamp needs a T-1 partition under it" % f)
        elif a.get("outcome") == "HELD_NO_NEW_PUBLICATION":
            if not a.get("absent_partition_named") or a.get("frontier_unchanged") is not True:
                fail("%s: a hold must name the absent partition and leave the served frontier unchanged" % f)
        else:
            fail("%s.after_read.outcome must be STAMPED_T_MINUS_1 or HELD_NO_NEW_PUBLICATION" % f)
    ex = r.get("exemption_after_read") or {}
    if ex.get("cottonwood_listed_accounts") not in (0, 4) or ex.get("no_closed_name_in_manifest") is not True or ex.get("amount_shown_for_listed") is not False:
        fail("exemption_after_read: cottonwood_listed_accounts 0 or 4, no_closed_name_in_manifest true and amount_shown_for_listed false")
    if r.get("rollback_performed") is not False:
        fail("rollback_performed must be false for a landed release (Branch B is reported, not graded as a pass)")
    c = r.get("counters") or {}
    want = {"lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "backfills": 0, "files_deleted": 0, "markers_closed": 0, "other_bucket_writes": 0}
    for k, v in want.items():
        if c.get(k) != v:
            fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
    if not (is_int(c.get("bundles_minted")) and 1 <= c["bundles_minted"] <= 3 and c["bundles_minted"] == len([f for f in FIRMS if mints.get(f)])):
        fail("counters.bundles_minted must equal the number of minted firms (1 to 3)")
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the first fire per firm; the exemption's after-read; counters")


CHECKS = {"IB236-1-AC1": ac1, "IB236-1-AC2": ac2, "IB236-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p236_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
