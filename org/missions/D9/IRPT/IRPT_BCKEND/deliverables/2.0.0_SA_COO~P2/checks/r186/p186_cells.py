"""IRPT_BCKEND round 186 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB186-1  IB-pr-521  the APPLY of the signed pair IB-pr-519: irpt-export-render moved to the signed built digest by its Terraform path, then a health proof
    AC1  the gates: both halves signed at the packet sha256, the receipt store re-read with no receipt lacking the field, no open marker or ledger naming the function, the start read equal to the signed live digest, the ledger entry naming the Branch B version
    AC2  the apply: the rebuilt digest equals the signed one, plan 1 change 0 destroy by safe-apply, the live function afterwards equals the built digest, re-plan 0, exactly the one schema member changed, the source-map row committed with the release
    AC3  the health proof: the deployed member equals the built one, the stored receipt validates against the DEPLOYED schema member (offline), a metric and log read with zero errors, no invoke, the bound counters
  IB186-2  IB-pr-522  the account_activity_daily backfill CENSUS: read-only measure of the table, its writers, its sources and the days a 2012-floor backfill would fill, and a plan packet (a draft for the pair)
    AC1  the writers and the table: the writers of account_activity_daily counted and named, the existing partitions per firm, the upstream returns table's range per firm
    AC2  the demand: the earliest record per firm with the 2012 floor applied, the days to fill per firm, the per-invocation chunk bound, the observed seconds per day or its stated absence
    AC3  the plan and the packet: the run mechanism and its event keys, idempotence, overwrite rule, rollback possibility, the write set, batches, the red list, the bound counters
"""
import json
import re
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
REC1 = D + "0.7.0_AE_CloudOps~IB2/IB186-1_apply_record.json"
COO_HALF = D + "2.0.0_SA_COO~P2/NEVER_WIDEN_IB_pr_519_EXPORT_RECEIPT_REPIN_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_IB_pr_519_EXPORT_RECEIPT_REPIN_CTO_HALF.md"
PACKET1_SHA = "7d78889847312b5517d1d85172a93c5f1f993de30760c8f83d60c92079a7b53b"
LIVE1_B64 = "K74JEIjw0NKmy4YfEo7Sb7LcRxEII+/yaYtaKJ3qnD8="
BUILT1_B64 = "5/9LZBbTEWOfrnNZufc6Mqz5pbDxTxYAxpWcZVURGs4="
MEMBER1 = "ExportReceipt.schema.json"
MEMBER1_SHA = "118a3575eaf20ff6ffb37d387b0cb3d4bd5e1a4d42ce68c86c07919bc968b4c7"
PIN1 = "e8005582a1"
REC2 = D + "0.9.0_WK_IRPT_BCKEND~369/IB186-2_activity_backfill_census.json"
PACKET2 = D + "0.9.0_WK_IRPT_BCKEND~369/BACKFILL_PLAN_PACKET_IB-pr-522.md"
BOUND2 = ("functions_invoked", "sign_ins_made", "aws_writes_made", "rows_written", "figures_written", "vendor_requests_sent")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB186"))
    sys.exit(1)


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def text(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    return f.read_text(encoding="utf-8", errors="replace")


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_date(x):
    return isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) is not None


def apply_arms(arm):
    r = load(REC1)
    if arm == "AC1":
        coo, cto = text(COO_HALF), text(CTO_HALF)
        if PACKET1_SHA[:12] not in coo or "Signed: `2.0.0_SA_COO~P2` at" not in coo:
            fail("the COO half must carry the packet sha256 and its signed line")
        if PACKET1_SHA[:12] not in cto or "SIGNED** at packet sha256" not in cto:
            fail("the CTO half must read SIGNED at the packet sha256")
        g = r.get("gates") or {}
        if g.get("packet_sha256") != PACKET1_SHA or g.get("both_halves_signed") is not True:
            fail("gates.packet_sha256 must equal the signed packet sha256 (re-hashed at the start) and both_halves_signed true")
        rc = g.get("receipt_store_reread") or {}
        if not (rc.get("mode") == "dry_run_reads_only" and is_int(rc.get("receipts_total")) and rc.get("receipts_lacking_field") == 0 and rc.get("unreadable_or_denied") == 0):
            fail("gates.receipt_store_reread needs mode dry_run_reads_only, an integer receipts_total, receipts_lacking_field 0 and unreadable_or_denied 0 (a receipt lacking the field is a STOP: the backfill runs first under its own pair)")
        m = g.get("open_markers") or {}
        if not (is_int(m.get("worktrees_read")) and m["worktrees_read"] >= 1 and is_int(m.get("marker_files_read")) and m["marker_files_read"] >= 1 and m.get("naming_the_function_with_open_trunk_ledger") == 0 and is_int(m.get("stale_views_naming_the_function")) and m["stale_views_naming_the_function"] >= 0):
            fail("gates.open_markers needs worktrees_read >= 1, marker_files_read >= 1, naming_the_function_with_open_trunk_ledger == 0 and an integer stale_views_naming_the_function")
        lg = g.get("open_ledgers") or {}
        if not (is_int(lg.get("ledger_files_read")) and lg["ledger_files_read"] >= 1 and lg.get("open_naming_the_function") == 0):
            fail("gates.open_ledgers needs ledger_files_read >= 1 and open_naming_the_function == 0")
        if r.get("start_read", {}).get("code_sha256") != LIVE1_B64:
            fail("start_read.code_sha256 must equal the signed live digest %s" % LIVE1_B64)
        led = str(r.get("ledger_entry", ""))
        if not led.startswith("org/critical_paths/change_management/") or not (ROOT / led).is_file():
            fail("ledger_entry must be an existing file under org/critical_paths/change_management/")
        bv = str(r.get("branch_b_version_id", "")).strip()
        if not bv or bv not in (ROOT / led).read_text(encoding="utf-8"):
            fail("branch_b_version_id must be named and written in the ledger entry")
        print("OK: gates read met; ledger %s" % led)
    elif arm == "AC2":
        a = r.get("apply") or {}
        if a.get("built_code_sha256") != BUILT1_B64:
            fail("apply.built_code_sha256 must equal the signed built digest %s" % BUILT1_B64)
        pl = a.get("plan") or {}
        if not (pl.get("change") == 1 and pl.get("destroy") == 0 and pl.get("add") == 0):
            fail("apply.plan must read add 0, change 1, destroy 0: %s" % pl)
        if a.get("safe_apply_rc") != 0 or a.get("path") != "terraform-safe-apply":
            fail("apply.path must be terraform-safe-apply with safe_apply_rc 0")
        af = r.get("after") or {}
        if af.get("code_sha256") != BUILT1_B64 or af.get("replan_changes") != 0:
            fail("after.code_sha256 must equal the built digest and after.replan_changes must be 0")
        if af.get("changed_members") != [MEMBER1]:
            fail("after.changed_members must be exactly [%r]: %s" % (MEMBER1, af.get("changed_members")))
        sm = r.get("source_map_row") or {}
        if not (sm.get("committed") is True and str(sm.get("pin", "")).startswith(PIN1) and sm.get("sha256") == MEMBER1_SHA):
            fail("source_map_row must read committed true, pin %s..., sha256 equal to the built schema member" % PIN1)
        if r.get("rollback_performed") is not False:
            fail("rollback_performed must be false for a landed apply (a Branch B restore is reported, not graded as a pass)")
        print("OK: the function moved to the signed digest; re-plan 0; source-map row committed")
    else:
        h = r.get("health_proof") or {}
        if h.get("deployed_member_sha256") != MEMBER1_SHA:
            fail("health_proof.deployed_member_sha256 must equal the built schema member %s" % MEMBER1_SHA)
        sr = h.get("stored_receipt_on_deployed_schema") or {}
        if not (sr.get("validated_offline") is True and sr.get("receipts_checked") == 1 and sr.get("valid") == 1 and sr.get("scratch_removed") is True):
            fail("health_proof.stored_receipt_on_deployed_schema must read validated_offline true, receipts_checked 1, valid 1, scratch_removed true (the one stored receipt validated against the DEPLOYED schema member; counts only)")
        if not (str(h.get("window_start_utc", "")).strip() and str(h.get("window_end_utc", "")).strip() and str(h["window_end_utc"]) > str(h["window_start_utc"])):
            fail("health_proof needs a window with window_end_utc later than window_start_utc")
        if not (is_int(h.get("invocations_in_window")) and h["invocations_in_window"] >= 0 and h.get("errors_in_window") == 0):
            fail("health_proof.invocations_in_window must be an integer and errors_in_window must be 0")
        c = r.get("counters") or {}
        want = {"function_updates": 1, "lambda_invokes": 0, "iam_changes": 0, "route_changes": 0, "env_changes": 0, "receipts_written": 0,
                "table_writes": 0, "figures_written": 0, "files_deleted": 0, "sibling_functions_moved": 0}
        for k, v in want.items():
            if c.get(k) != v:
                fail("counters.%s must read %s, read %r" % (k, v, c.get(k)))
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
            fail("the record carries a long digit run")
        print("OK: health proof and counters")


def census_arms(arm):
    r = load(REC2)
    firms = r.get("firms") or {}
    if arm in ("AC1", "AC2") and sorted(firms) != ["49financial", "cottonwood", "inflection"]:
        fail("firms must hold exactly 49financial, cottonwood and inflection")
    if arm == "AC1":
        w = r.get("writers") or {}
        lst = w.get("list")
        if not isinstance(lst, list) or not lst or w.get("count") != len(lst):
            fail("writers needs a non-empty list and a count equal to its length (N writers = N rules read)")
        for x in lst:
            if not (x.get("file") and x.get("how") in ("scheduled", "backfill", "scheduled_and_backfill", "other")):
                fail("each writer needs a file and a how of scheduled|backfill|scheduled_and_backfill|other")
        for f, v in firms.items():
            a = v.get("activity_table") or {}
            b = v.get("returns_table") or {}
            if not (is_int(a.get("partitions")) and a["partitions"] >= 0 and is_int(b.get("partitions")) and b["partitions"] >= 0):
                fail("%s: activity_table.partitions and returns_table.partitions must be integers >= 0" % f)
            for t in (a, b):
                if t["partitions"] > 0 and not (is_date(t.get("earliest")) and is_date(t.get("latest")) and t["earliest"] <= t["latest"]):
                    fail("%s: a table with partitions needs earliest and latest dates (earliest <= latest)" % f)
        print("OK: %d writer(s) named; partitions read for 3 firms" % lst.__len__())
    elif arm == "AC2":
        cb = r.get("chunk_bound_days")
        if not (is_int(cb) and cb >= 1):
            fail("chunk_bound_days must be an integer >= 1")
        unsourced = 0
        for f, v in firms.items():
            d = v.get("demand") or {}
            if d.get("floor_applied") != "2012-01-01":
                fail("%s: demand.floor_applied must read 2012-01-01 (Andrew-direct 2026-10-07: nothing earlier than the earliest record, cut at 2012)" % f)
            if d.get("earliest_record") is None:
                # AMENDMENT 1: a firm with no activity producer is recorded null WITH its reason, never estimated
                if not (str(d.get("unsourced_reason", "")).strip() and d.get("start_day") is None and d.get("trading_days_to_fill") is None and d.get("invocations_needed") is None):
                    fail("%s: an unsourced demand needs unsourced_reason (the stated cause) and null start_day, trading_days_to_fill and invocations_needed" % f)
                unsourced += 1
                continue
            if not (is_date(d.get("earliest_record")) and is_int(d.get("trading_days_to_fill")) and d["trading_days_to_fill"] >= 0 and is_int(d.get("invocations_needed")) and d["invocations_needed"] >= 0):
                fail("%s: demand needs earliest_record (a date), trading_days_to_fill and invocations_needed (integers >= 0)" % f)
            if d["earliest_record"] < "2012-01-01" and d.get("start_day") != "2012-01-01":
                fail("%s: an earliest record before 2012 means start_day 2012-01-01" % f)
            if d["trading_days_to_fill"] and d["invocations_needed"] != -(-d["trading_days_to_fill"] // cb):
                fail("%s: invocations_needed must equal ceil(trading_days_to_fill / chunk_bound_days)" % f)
        if unsourced >= len(firms):
            fail("at least one firm's demand must be sourced (a measured earliest_record)")
        o = r.get("observed_seconds_per_day")
        if not ((isinstance(o, (int, float)) and not isinstance(o, bool) and o > 0) or (o is None and str(r.get("observed_seconds_per_day_absence", "")).strip())):
            fail("observed_seconds_per_day must be a positive number from the logs, or null with observed_seconds_per_day_absence stating why")
        print("OK: demand per firm with the 2012 floor; cap %d" % cb)
    else:
        p = r.get("plan") or {}
        if not (p.get("mechanism") and isinstance(p.get("event_keys"), list) and p["event_keys"]):
            fail("plan needs a mechanism and a non-empty list of event_keys (key names only)")
        for k in ("idempotent", "overwrites_existing_partitions", "rollback_possible"):
            if not isinstance(p.get(k), bool):
                fail("plan.%s must be true or false, read from the producer and the bucket" % k)
        if not (is_int(p.get("batches")) and p["batches"] >= 0 and isinstance(p.get("write_set"), list) and p["write_set"]):
            fail("plan needs an integer batches and a non-empty write_set (key SHAPES, no firm or account value)")
        t = text(PACKET2)
        for need, pat in (("Branch A", r"Branch A"), ("Branch B", r"Branch B"), ("the red list", r"(?i)red list"), ("the writers counted", r"(?i)writers?"),
                          ("the 2012 floor", r"2012"), ("the COO half", r"(?i)COO half"), ("the CTO half", r"(?i)CTO half"), ("blast radius", r"(?i)blast radius"),
                          ("rollback", r"(?i)rollback|restore")):
            if not re.search(pat, t):
                fail("the packet lacks: %s" % need)
        if len(t) < 3000:
            fail("the packet is shorter than 3000 characters")
        if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", json.dumps(r)):
            fail("the record carries a long digit run")
        for k in BOUND2:
            if r.get(k) != 0:
                fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
        print("OK: plan recorded (%d batch(es)); packet complete; counters 0" % p["batches"])


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if arm not in ("AC1", "AC2", "AC3"):
        fail("unknown criterion %r" % CID)
    if cell == "IB186-1":
        apply_arms(arm)
    elif cell == "IB186-2":
        census_arms(arm)
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
