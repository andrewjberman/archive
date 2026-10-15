"""IRPT_BCKEND round 199 (workstream ~P) -- the apply check IB199-2 (IB-pr-549), imported by p199_cells.py.

  IB199-2  IB-pr-549  the holdings-producer release APPLIED under the signed pair IB-pr-532 packet v3: three bundle mints, each from its firm's pin
    AC1  the gates: the packet's sha256, both halves signed, the pins and blobs, the per-firm re-measure (32, 255, 841, all the signed cash rule),
         Branch B re-read with the manifest anchor rule, the digest gate against the packet's moved members
    AC2  the act: the window, the releasing seat's ledger (five legs), the three mints each from its pin, the per-firm business date stated before the fire
    AC3  the after-read per firm at the first fire (T-1 stamp, or a named hold with the frontier unchanged), the Cash rows, the gap, the kernel-log count, the counters
"""
import json
import re

import p193_cells as P3  # noqa: E402
import p196_cells as P6  # noqa: E402

D = P6.D
APPLY_REC = D + "0.7.0_AE_CloudOps~IB2/IB199-2_apply_record.json"
V3 = D + "0.9.0_WK_IRPT_BCKEND~393/NEVER_WIDEN_SIGNOFF_PACKET_IB-pr-532_V3.md"
V3_SHA = "94eca88e90711b793f43ef1288d0c61aa7a420d0057bd3816942c650153fc853"
PIN1 = "b1d354cfc9341168a3b4c316a344876ce0049b97"
PIN2 = "5fad7eaaa8fb4c512190fa406b78c683c4b6ad1f"
FIRM_PIN = {"49financial": PIN1, "cottonwood": PIN2, "inflection": PIN2}
FIRM_BLOB = {"49financial": "3a19dcf5912798f7d94e9756ae04f64dd2ce7ea0", "cottonwood": "ed3cf609a7e7f345a033da42e4da3f83670cfe89",
             "inflection": "ed3cf609a7e7f345a033da42e4da3f83670cfe89"}
FIRM_TOTAL = {"49financial": 32, "cottonwood": 255, "inflection": 841}
OPAL_UNID = "data/assets/scripts/silver/opal_unidentified.py"
APPLY_COUNTERS = {"bundles_minted": 3, "other_bucket_writes": 0, "lambda_invokes": 0, "iam_changes": 0, "schedule_changes": 0, "backfills": 0,
                  "files_deleted": 0, "markers_closed": 0}
FIRMS = P6.FIRMS


def sync():
    P3.ROOT, P3.CID = P6.ROOT, P6.CID


def a_fail(msg):
    sync()
    P3.fail(msg)


def a_load(rel):
    sync()
    return P3.load(rel)


def packet_members(firm):
    """The moved member paths the packet's section 2 table lists for the firm, plus the v3 closure member."""
    f = P6.ROOT / V3
    if not f.is_file():
        a_fail("packet v3 is not at %s" % V3)
    out, on = set(), False
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            on = line.startswith("### " + firm)
            continue
        if line.startswith("## "):
            on = False
        if on and line.startswith("| data/"):
            out.add(line.split("|")[1].strip())
    if not out:
        a_fail("no moved-member rows for %s in packet v3 section 2" % firm)
    return out | {OPAL_UNID}


def apply_ac1():
    r = a_load(APPLY_REC)
    g = r.get("gates") or {}
    if g.get("packet_sha256") != V3_SHA:
        a_fail("gates.packet_sha256 is not packet v3's")
    if g.get("coo_half_signed") is not True or g.get("cto_half_signed") is not True:
        a_fail("both halves must read signed at the packet bytes")
    if g.get("pins") != FIRM_PIN or g.get("holdings_snapshot_blob") != FIRM_BLOB:
        a_fail("the per-firm pins and the holdings_snapshot.py blob at each pin must be the packet's")
    rm = r.get("remeasure") or {}
    if rm.get("pins") != P6.PINS:
        a_fail("the re-measure custody pins must be %r" % P6.PINS)
    for firm in FIRMS:
        v = (rm.get("firms") or {}).get(firm) or a_fail("no re-measure for %s" % firm)
        if v.get("total_changed_nodes") != FIRM_TOTAL[firm] or v.get("unattributed") != 0 or v.get("all_signed_cash_rule") is not True:
            a_fail("%s re-measure must read %d changed nodes, all the signed cash rule, 0 unattributed: a STOP" % (firm, FIRM_TOTAL[firm]))
        att = v.get("gate_attribution")
        if att != "same" and not (att == "signed_exemption_repair" and firm == "cottonwood"):
            a_fail("%s gate attribution %r is a STOP" % (firm, att))
        if not P3.is_date((v.get("served_state") or {}).get("latest_date")) or v.get("matches_packet") is not True:
            a_fail("%s: the served state and matches_packet are required" % firm)
    bb = r.get("branch_b_reread") or {}
    for firm in FIRMS:
        v = bb.get(firm) or a_fail("no branch_b_reread for %s" % firm)
        if v.get("bundle_version_id") != P3.BRANCH_B_BUNDLE[firm]:
            a_fail("%s bundle version differs from the packet's Branch B: the release stops" % firm)
        a = v.get("manifest_anchor_at_mint") or a_fail("%s: no manifest_anchor_at_mint" % firm)
        if not a.get("version_id"):
            a_fail("%s: the anchor needs a version id" % firm)
        if a["version_id"] == P3.BRANCH_B_MANIFEST[firm]:
            if a.get("newer_versions") != 0:
                a_fail("%s: the anchor equals the packet's but newer versions are claimed" % firm)
        else:
            if a.get("newer_versions") != 1 or a.get("written_by_scheduled_fire") is not True:
                a_fail("%s: a newer manifest version must be the only one and written by the scheduled fire: a STOP" % firm)
            fd = a.get("fire_date")
            if not P3.is_date(fd) or a.get("published_date") != P3.prev_trading_day(fd):
                a_fail("%s: the newer manifest's published date must be T-1 of its fire by the calendar: a STOP" % firm)
    dg = r.get("digest_gate") or {}
    for firm in FIRMS:
        v = dg.get(firm) or a_fail("no digest_gate for %s" % firm)
        ch = v.get("changed_members")
        if not isinstance(ch, list) or set(ch) - {"SHA256SUMS"} != packet_members(firm):
            a_fail("%s changed members must equal the packet's moved members (and SHA256SUMS)" % firm)
        if v.get("holdings_snapshot_blob") != FIRM_BLOB[firm]:
            a_fail("%s built holdings_snapshot.py must be the pin's blob" % firm)
    if r.get("stop") is not None:
        a_fail("a STOP is recorded: the criteria are not run on a stopped release")
    print("OK: gates, per-firm re-measure, Branch B, digest gate against the packet's moved members")


def apply_ac2():
    r = a_load(APPLY_REC)
    w = r.get("window") or {}
    for k in ("last_fire_all_success_utc", "mint_start_utc", "mint_end_utc", "next_fire_utc"):
        if not P3.is_ts(w.get(k)):
            a_fail("window.%s must be a UTC timestamp" % k)
    a, b, c, n = (P3.ts(w[k]) for k in ("last_fire_all_success_utc", "mint_start_utc", "mint_end_utc", "next_fire_utc"))
    if not (a < b <= c < n):
        a_fail("the mints must start after the day's fires read Success and end before the next fire")
    if (n - c).total_seconds() < 1800:
        a_fail("nothing is minted within 30 minutes before a fire")
    if (c - b).total_seconds() > 3600:
        a_fail("the mints must be made inside one session (one hour)")
    if not re.fullmatch(r"\d\d:15:00Z", w["next_fire_utc"][11:]) or w["next_fire_utc"][11:13] not in ("14", "15"):
        a_fail("next_fire_utc must be a 10:15 ET fire (14:15Z or 15:15Z)")
    led = r.get("ledger") or {}
    ent = led.get("entry", "")
    if not ent.startswith("org/critical_paths/change_management/") or not (P6.ROOT / ent).is_file():
        a_fail("the ledger entry must exist under org/critical_paths/change_management/")
    if led.get("legs") != 5 or led.get("opened_before_first_mint") is not True:
        a_fail("the ledger must name the five legs and be opened before the first mint")
    mints = r.get("mints") or {}
    for firm in FIRMS:
        m = mints.get(firm) or a_fail("no mint for %s" % firm)
        if m.get("bundle") != P3.BUNDLES[firm]:
            a_fail("%s mint is not %s" % (firm, P3.BUNDLES[firm]))
        if m.get("minted_from_pin") != FIRM_PIN[firm]:
            a_fail("%s must be minted from its own pin %s" % (firm, FIRM_PIN[firm]))
        if not m.get("after_version_id") or m.get("after_version_id") == m.get("before_version_id") or m.get("before_version_id") != P3.BRANCH_B_BUNDLE[firm]:
            a_fail("%s mint must move the bundle off the packet's Branch B version" % firm)
        if m.get("after_sha256_equals_built") is not True:
            a_fail("%s landed bytes must equal the built bundle" % firm)
    bd = r.get("business_date_statement") or {}
    if not (P3.is_ts(bd.get("stated_at_utc")) and P3.ts(bd["stated_at_utc"]) < n):
        a_fail("the per-firm business date must be stated before the fire")
    fd = bd.get("fire_date")
    if not P3.is_date(fd) or bd.get("t_minus_1") != P3.prev_trading_day(fd):
        a_fail("t_minus_1 must be the calendar's previous trading day of the fire date")
    if set((bd.get("per_firm_expected") or {})) != set(FIRMS):
        a_fail("a business date is stated for each of the three firms")
    print("OK: window, ledger, three mints each from its pin, business date stated")


def apply_ac3():
    r = a_load(APPLY_REC)
    bd = r.get("business_date_statement") or {}
    t1 = bd.get("t_minus_1")
    ar = r.get("after_read") or {}
    for firm in FIRMS:
        v = ar.get(firm) or a_fail("no after_read for %s" % firm)
        o = v.get("outcome")
        if o == "STAMPED_T_MINUS_1":
            if v.get("stamp") != t1 or v.get("t1_partition_under_it") is not True:
                a_fail("%s stamped %r, not T-1 %r, or no T-1 partition under it: a STOP" % (firm, v.get("stamp"), t1))
        elif o == "HELD_NO_NEW_PUBLICATION":
            if not v.get("absent_partition_named") or v.get("frontier_unchanged") is not True or v.get("served_latest_date_after") != v.get("served_latest_date_before"):
                a_fail("%s hold needs the absent T-1 partition named and the served frontier unchanged" % firm)
        else:
            a_fail("%s outcome %r is neither a T-1 stamp nor a named hold" % (firm, o))
    cw = ar["cottonwood"]
    if cw["outcome"] == "STAMPED_T_MINUS_1" and cw.get("lost_accounts_listed") != 1:
        a_fail("a stamped Cottonwood must list its one lost account")
    if r.get("rule_after_read", {}).get("cash_sub_read_cash") is not True and any(ar[f]["outcome"] == "STAMPED_T_MINUS_1" for f in FIRMS):
        a_fail("a published firm must read its Cash-sub holdings as Cash")
    if (r.get("gap_2026_10_08") or {}).get("unchanged") is not True:
        a_fail("the 49financial 2026-10-08 gap must read unchanged")
    k = r.get("kernel_log_count") or {}
    if k.get("memory_read_done") is True:
        if not P3.is_int(k.get("oom_count")) or k["oom_count"] < 0:
            a_fail("a kernel-log count read needs the count")
    elif k.get("memory_read_done") is False:
        if not isinstance(k.get("reason"), str) or len(k["reason"]) < 10:
            a_fail("a kernel-log count not read needs its reason (the host not Online)")
    else:
        a_fail("kernel_log_count.memory_read_done must be true or false")
    if r.get("rollback_performed") is not False:
        a_fail("rollback_performed must be false (a rollback is a STOP)")
    c = r.get("counters") or {}
    for key, want in APPLY_COUNTERS.items():
        if c.get(key) != want:
            a_fail("counter %s must read %r, reads %r" % (key, want, c.get(key)))
    P3.no_long_digits(json.dumps(r))
    print("OK: per-firm after-read, Cash rows, gap, kernel-log count, counters")


CHECKS = {"IB199-2-AC1": apply_ac1, "IB199-2-AC2": apply_ac2, "IB199-2-AC3": apply_ac3}
