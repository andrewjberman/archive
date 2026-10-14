"""IRPT_DASHBD round 98 (issuer 2.0.0_SA_COO~D2) -- the FDRXX -> CASH pair is SIGNED on both halves at packet sha256 cfc1dd8d... (CTO half @d3b576bb67, msg 7383).

  DB-b-183 (WORLD, applier 0.7.0_AE_CloudOps~IB2)  the apply: ONE S3 object, under the pair, ledger first.                              DB98-1-AC1
  DB-b-184 (LOCAL, worker ~149)                     read where the Inflection client's Investor Reporting holdings get FDRXX's class.    DB98-2-AC1

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.
"""
import json
import re
import sys
from pathlib import Path

PACKET_SHA = "cfc1dd8d01206badc657bbf17c46653482149c1904b708bd002ba1ff172b1fe6"
PRE_SHA = "d2e6aa88086ce9741feb3bf4df22b84996d37906730710c9d1fc79029b874250"
NEW_SHA = "e7385264668e9bf746aeab809c8ff0a869f9091685f86751b1679dfc6ddd81ba"
KEY = "s3://opal-data-bd/code/gold/lib/etf_classifier.py"
APPLY_RECORD = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/bd_gold_classifier_cash/APPLY_RECORD.json"
READ_RECORD = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~149/IR_HOLDINGS_CLASS_SOURCE.json"
RUN = re.compile(r"\d{8,}")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 0


def long_digit_runs(obj, name=""):
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not str(k).endswith("sha256") and str(k) not in ("commit", "path", "version_id", "request_id", "slug", "ledger_entry"):
                hits += long_digit_runs(v, name + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += long_digit_runs(v, "%s/%d" % (name, i))
    elif isinstance(obj, str) and RUN.search(obj):
        hits.append(name)
    return hits


def load(root, rel):
    p = root / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def check_apply(root):
    r = load(root, APPLY_RECORD)
    need(r.get("packet_sha256") == PACKET_SHA, "packet_sha256 %r must equal the signed packet's %s..." % (r.get("packet_sha256"), PACKET_SHA[:12]))
    need(r.get("object") == KEY and r.get("objects_uploaded") == 1, "exactly the one object %s must be uploaded" % KEY)
    b, a = r.get("before") or {}, r.get("after") or {}
    need(b.get("sha256") == PRE_SHA and a.get("sha256") == NEW_SHA, "before.sha256 must equal %s... and after.sha256 %s..." % (PRE_SHA[:12], NEW_SHA[:12]))
    need(re.fullmatch(r"[A-Za-z0-9._-]{16,}", str(b.get("version_id") or "")) and re.fullmatch(r"[A-Za-z0-9._-]{16,}", str(a.get("version_id") or "")) and b["version_id"] != a["version_id"], "before and after version ids must be recorded and differ")
    need(r.get("rollback_version_id") == b["version_id"], "rollback_version_id must be the version read BEFORE the upload")
    need(r.get("bucket_versioning") == "Enabled", "bucket_versioning must read Enabled")
    up = r.get("upload") or {}
    need(up.get("command") == "safe-deploy.sh data/black_diamond/scripts/gold/lib/etf_classifier.py" and up.get("rc") == 0 and up.get("readback_ok") is True and up.get("pipescript_deployed_match") is True, "upload %r: the explicit-files safe-deploy call, rc 0, read-back ok, deployed MATCH" % up)
    tb = r.get("tests_before_upload") or {}
    need(is_int(tb.get("passed")) and tb["passed"] >= 37 and tb.get("failed") == 0 and tb.get("import_smoke") is True, "tests_before_upload %r: 37 or more passed, none failed, import smoke" % tb)
    pre = r.get("preconditions") or {}
    need(pre.get("chain_in_flight") is False and str(pre.get("chain_in_flight_instrument") or "").strip() != "" and is_int(pre.get("worktrees_read")) and pre["worktrees_read"] >= 1 and pre.get("open_entries_on_bd_gold_tree") == 0 and pre.get("packet_rehashed") is True and pre.get("new_bytes_pin_commit") == "e340e07f4e",
         "preconditions %r" % pre)
    lg = r.get("ledger") or {}
    need(str(lg.get("slug") or "") == "bd-gold-etf-classifier-cash-type-20261014" and sorted(lg.get("legs_closed") or []) == ["L1", "L2"] and lg.get("legs_open") == ["L3"], "ledger %r: slug bd-gold-etf-classifier-cash-type-20261014, L1 and L2 closed, L3 (the first D_04 run read) open for the issuer" % lg)
    need(r.get("rollback") in (None, False), "a rollback was recorded: this criterion describes the applied state")
    z = r.get("not_done") or {}
    need(z.get("jobs_run") == 0 and z.get("dynamodb_writes") == 0 and z.get("deletes") == 0 and z.get("other_keys_uploaded") == 0 and z.get("terraform_applied") is False and z.get("full_rebuild") is False, "not_done %r must read zero everywhere" % z)
    need(r.get("served_values_changed_by_the_upload") is False, "served_values_changed_by_the_upload must be false: nothing served moves until the next run")
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: the one object replaced (%s... to %s...), versioning Enabled, rollback version recorded, 37+ tests before, ledger L1 and L2 closed with L3 open, nothing else moved" % (PRE_SHA[:8], NEW_SHA[:8]))


def check_read(root):
    r = load(root, READ_RECORD)
    hops = r.get("hops")
    need(isinstance(hops, list) and len(hops) >= 3 and all(isinstance(h, dict) and str(h.get("layer") or "").strip() and str(h.get("file") or "").strip() and is_int(h.get("line")) and str(h.get("what") or "").strip() for h in hops),
         "hops must be 3 or more {layer, file, line, what}: from the portal holdings tab to the place the class is read or assigned")
    ca = r.get("class_assigned_at") or {}
    need(str(ca.get("file") or "").strip() and is_int(ca.get("line")) and str(ca.get("rule") or "").strip() and ca.get("keyed_on") in ("canonical_row_asset_class", "ticker_list", "name", "sub_asset_class", "other"), "class_assigned_at %r needs file, line, rule and keyed_on" % ca)
    need(isinstance(r.get("shares_code_with_bd_gold_classifier"), bool) and isinstance(r.get("reads_same_canonical_table"), bool) and isinstance(r.get("needs_its_own_rule"), bool), "shares_code_with_bd_gold_classifier, reads_same_canonical_table and needs_its_own_rule must be bools")
    if r["needs_its_own_rule"]:
        pr = r.get("proposed_rule") or {}
        need(str(pr.get("words") or "").strip() != "" and pr.get("keyed_on") == "sub_asset_class" and pr.get("ticker_list_used") is False and str(pr.get("where") or "").strip() != "", "proposed_rule %r: words, keyed_on sub_asset_class, no ticker list, where" % pr)
    else:
        need(str(r.get("why_no_rule_needed") or "").strip() != "", "why_no_rule_needed must say why")
    need(isinstance(r.get("served_class_of_a_money_market_fund_today"), str) and r["served_class_of_a_money_market_fund_today"].strip() != "" and isinstance(r.get("served_class_read_from"), str) and r["served_class_read_from"].strip() != "",
         "served_class_of_a_money_market_fund_today and served_class_read_from must be stated (a stored served object or a fixture; NOT_ESTABLISHED with its reason is allowed)")
    need(isinstance(r.get("other_readers_of_that_assignment"), list), "other_readers_of_that_assignment must be a list (possibly empty)")
    rd = r.get("reads") or {}
    need(rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0 and rd.get("writes") == 0 and r.get("served_values_changed") is False and r.get("pushed") is False, "reads %r" % rd)
    hits = long_digit_runs(r)
    need(not hits, "the record holds a run of 8 or more digits at %s" % hits[:3])
    print("OK: the IR holdings' class is read through %d hop(s) and assigned at one site keyed on %s; own rule needed: %s" % (len(hops), ca["keyed_on"], str(r["needs_its_own_rule"]).lower()))


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""
    fns = {"DB98-1-AC1": check_apply, "DB98-2-AC1": check_read}
    try:
        need(cid in fns, "unknown criterion %r" % cid)
        fns[cid](root)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (cid or "DB98"))
        sys.exit(1)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
