"""IRPT_BCKEND workstream ~PQ round 2 (issuer 2.0.0_SA_COO~P2) -- the check of one APPLY order: the holdings EXEMPTION ADDENDUM 1 (49financial, one bundle).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB242-1  IB-pr-611  mint 49financial's addendum bundle (digest 61537d6d) once, between fires, over the exemption pair's bundle (d2eaf305), and read the first fire
    AC1  the gates and the digest gate: both halves signed at the addendum blob, the exemption pair applied (the live bundle read d2eaf305), the Branch B version recorded, the built bundle equal to the
         signed digest with exactly holdings_snapshot.py and SHA256SUMS changed against the live bundle, the bypass and CUSIP reads, the re-measure (the node set unchanged)
    AC2  the mint: the window, the ledger opened first, the mint moving the bundle off its Branch B version with the landed bytes equal to the built bundle, the business date stated before the fire
    AC3  the first fire (a stamp with a T-1 partition, or a named hold with the frontier unchanged), the node set unchanged, exactly one evidence value per exempted account, the counters
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

D = P6.D
REC = D + "0.7.0_AE_CloudOps~IB2/IB242-1_apply_record.json"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_HOLDINGS_EXEMPTION_PAIR_ADDENDUM_1_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_HOLDINGS_EXEMPTION_PAIR_ADDENDUM_1_R3_CTO_HALF.md"
DIGEST = "61537d6d9fac83e67b4406023c89ab391c23144357c6fe8abbfaaf5c4f0fdb01"
LIVE_BEFORE = "d2eaf3056c1d"
MEMBERS = ("data/assets/scripts/gold/investor_reporting/holdings_snapshot.py", "SHA256SUMS")
VALUES = ("smartx_map_present", "smartx_map_absent", "unread")
fail, load, is_int = P6.fail, P6.load, P6.is_int


def text(rel):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8")


def blob_of(rel):
    p = subprocess.run(["git", "hash-object", "--stdin"], input=(P6.ROOT / rel).read_bytes(), capture_output=True, timeout=60)
    return p.stdout.decode().strip()


def ac1(r):
    for rel in (COO_HALF, CTO_HALF):
        t = text(rel)
        if DIGEST[:8] not in t or ("SIGNED" not in t.upper() and "GIVEN" not in t.upper()):
            fail("both halves must read SIGNED or GIVEN at the candidate digest %s: %s" % (DIGEST[:8], rel))
    blob = blob_of(COO_HALF)
    g = r.get("gates") or {}
    if g.get("addendum_blob") != blob or g.get("both_halves_signed") is not True:
        fail("gates.addendum_blob must equal the COO half's blob %s and both_halves_signed true" % blob)
    if g.get("one_change_at_a_time") is not True or g.get("exemption_pair_applied_and_ledger_closed") is not True:
        fail("gates.one_change_at_a_time and gates.exemption_pair_applied_and_ledger_closed must be true (IB-pr-605 is applied and its ledger closed first)")
    br = r.get("branch_b_reread") or {}
    if not (br.get("bundle_version_id") and br.get("manifest_anchor_at_mint")):
        fail("branch_b_reread must record bundle_version_id and manifest_anchor_at_mint")
    if not str(br.get("live_bundle_sha256", "")).startswith(LIVE_BEFORE):
        fail("branch_b_reread.live_bundle_sha256 must start %s (the exemption pair's bundle is live: otherwise STOP)" % LIVE_BEFORE)
    dg = r.get("digest_gate") or {}
    if dg.get("built_bundle_sha256") != DIGEST:
        fail("digest_gate.built_bundle_sha256 must equal the signed digest %s" % DIGEST)
    if sorted(dg.get("changed_members") or []) != sorted(MEMBERS):
        fail("digest_gate.changed_members must be exactly %s" % (MEMBERS,))
    if dg.get("publication_equal_live") is not True or dg.get("allow_older_date_count") != 0:
        fail("digest_gate.publication_equal_live must be true and allow_older_date_count 0")
    if dg.get("cusip_lines") != 12 or dg.get("cusip_lines_live") != 12:
        fail("digest_gate.cusip_lines and cusip_lines_live must both read 12 (row S206: a reversal is a STOP)")
    rm = r.get("remeasure") or {}
    if rm.get("verdict") not in ("REFUSED_NO_NODE_MOVES", "PUBLISHED_ONE_LISTED_ACCOUNT") or rm.get("node_set_unchanged") is not True:
        fail("remeasure must read REFUSED_NO_NODE_MOVES or PUBLISHED_ONE_LISTED_ACCOUNT with node_set_unchanged true against the signed bundle")
    print("OK: gates, digest gate and the re-measure agree with the signed addendum")


def ac2(r):
    w = r.get("window") or {}
    for k in ("last_fire_all_success_utc", "mint_start_utc", "mint_end_utc", "next_fire_utc"):
        if not re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", str(w.get(k))):
            fail("window.%s must be an ISO UTC time" % k)
    if not (w["last_fire_all_success_utc"] < w["mint_start_utc"] <= w["mint_end_utc"] < w["next_fire_utc"]):
        fail("the mint must lie after the day's fires and before the next fire")
    if not is_int(w.get("minutes_before_next_fire")) or w["minutes_before_next_fire"] < 30:
        fail("window.minutes_before_next_fire must be 30 or more")
    lg = r.get("ledger") or {}
    if lg.get("opened_before_the_mint") is not True or not str(lg.get("entry", "")).startswith("org/critical_paths/change_management/"):
        fail("ledger must name an entry under org/critical_paths/change_management/ opened before the mint")
    m = r.get("mint") or {}
    if not m.get("after_version_id") or m.get("before_version_id") == m.get("after_version_id"):
        fail("the mint must move the bundle off its Branch B version")
    if m.get("after_sha256_equals_built") is not True:
        fail("the landed bytes must equal the built bundle")
    bd = r.get("business_date_statement") or {}
    if not (bd.get("stated_at_utc") and bd.get("t_minus_1") and bd["stated_at_utc"] < bd.get("fire_utc", "9")):
        fail("business_date_statement must be stated BEFORE the fire (stated_at_utc < fire_utc) with t_minus_1")
    print("OK: window, ledger and mint; the business date stated before the fire")


def ac3(r):
    a = r.get("after_read") or {}
    if a.get("outcome") == "STAMPED_T_MINUS_1":
        if a.get("t1_partition_under_it") is not True:
            fail("a stamp needs a T-1 partition under it")
        nd = a.get("node_set_diff") or {}
        if any(nd.get(k) != 0 for k in ("nodes_added_vs_signed_bundle", "nodes_removed", "nodes_changed")):
            fail("after_read.node_set_diff must read 0 added, removed and changed against what the signed bundle would have produced (a changed publish is an UNATTRIBUTED STOP)")
        ev = a.get("evidence") or {}
        counts = ev.get("values") or {}
        if sorted(counts) != sorted(VALUES) or not all(is_int(counts[k]) and counts[k] >= 0 for k in VALUES):
            fail("after_read.evidence.values must count %s" % (VALUES,))
        if ev.get("listed_accounts") != sum(counts.values()) or ev.get("missing_or_second_key") != 0:
            fail("every listed exempted account must carry exactly one evidence value: listed_accounts equal to the sum, missing_or_second_key 0")
    elif a.get("outcome") == "HELD_NO_NEW_PUBLICATION":
        if not a.get("absent_partition_named") or a.get("frontier_unchanged") is not True:
            fail("a hold must name the absent partition and leave the served frontier unchanged")
    else:
        fail("after_read.outcome must be STAMPED_T_MINUS_1 or HELD_NO_NEW_PUBLICATION")
    if a.get("no_closed_name_in_manifest") is not True or a.get("amount_shown_for_listed") is not False:
        fail("after_read.no_closed_name_in_manifest must be true and amount_shown_for_listed false")
    if r.get("rollback_performed") is not False:
        fail("rollback_performed must be false for a landed release (Branch B is reported, not graded as a pass)")
    c = r.get("counters") or {}
    want = {"lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "backfills": 0, "files_deleted": 0, "markers_closed": 0, "other_bucket_writes": 0, "bundles_minted": 1}
    for k, v in want.items():
        if c.get(k) != v:
            fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
    if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
        fail("the record carries a long digit run")
    print("OK: the first fire; the node set unchanged; one evidence value per account; counters")


CHECKS = {"IB242-1-AC1": ac1, "IB242-1-AC2": ac2, "IB242-1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p242_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](load(REC))
    print("%s PASS" % sys.argv[2])
