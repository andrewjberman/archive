"""IRPT_DASHBD round 136, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- DB-f-2204, the APPLY of the signed never-widen pair for the 49 Financial TRANSACTION TABLE
(packet sha256 b67bd4ad57f23b13b6e89361a551a0e6e026a831ecc495cdfb66e13ac5e7313c, COO half signed, CTO half signed @6b6c16b492): the new bundle, ONE safe-apply (plan exactly 0 add /
2 change / 0 destroy: the write statement's one new resource and the function's code), a transaction-only dry run, the first one-day write and a bounded 25-day range. WORLD.
The record is the applier's; the checker re-reads the world.

  DBF136-4-AC1  the record's head: packet and halves, gates, ledger and applier, before, build, plan, the policy change, the apply window
  DBF136-4-AC2  FRESH live reads: the function's code and settings, the role policy (eleven statements, the write statement gaining exactly the new resource), the schedule, the artifact version
  DBF136-4-AC3  the dry run, the time trigger, the first write and the range in the record, and FRESH reads of the new prefix, the five other tables and the open ledger

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import copy
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

APPLIER = "0.7.0_AE_CloudOps~IB2"
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.7.0_AE_CloudOps~IB2/TRANSACTION_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_49F_TRANSACTION_WIRING.md"
COO_REL = D + "2.0.0_SA_COO~F2/NEVER_WIDEN_49F_TRANSACTION_WIRING_COO_HALF.md"
CTO_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_TRANSACTION_WIRING_CTO_HALF.md"
PACKET_SHA = "b67bd4ad57f23b13b6e89361a551a0e6e026a831ecc495cdfb66e13ac5e7313c"
BUILD_B64 = "SCt7IgN3A+SXxfn8cv0QHVnhjVMmHXePihA6MnPm2nQ="
OLD_CODE_B64 = "JNTOivgNaJ8spRxoXSkXAYWhf1cLqXr350sTpH5ADg4="
OLD_ARTIFACT_VERSION = "00dm6f4.vFnWIiIuxVafNVtxIh0zAEeh"
FUNCTION = "irpt-49f-reporting-gold-lambda"
ROLE = "irpt-49f-reporting-gold-role"
POLICY = "irpt-49f-reporting-gold-policy"
SCHEDULE = "irpt-49f-reporting-gold-daily"
WRITE_SID = "WriteTheFiveGoldPrefixesOnly"
SIDS = ["ListExactlyTheDeclaredSilverPrefixes", "ReadDeclaredSilverPartitionsOnly", "ListExactlyTheSixGoldPrefixes", "ReadTheSixGoldPrefixesOnly", WRITE_SID,
        "ReadTheServedModelSeriesObjectOnly", "ListExactlyTheHouseholdCrosswalkPrefix", "ReadTheHouseholdCrosswalkOnly", "ReadTheClassTableByKeyOnly", "OwnLogStreamOnly",
        "InvokeOwnFunctionOnly"]
OTHER_TABLES = ("account_return_daily", "account_class_daily", "account_activity_daily", "account_lot_realized", "account_lot_unrealized_daily", "filled_report_values")
SCHEMA_HASH = "ac652e2f71b18427b52f321858163768158f850ec173d1e592c7c3abe815bb6a"
FIRM = "49financial"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def parse_utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)


def in_fire_window(t):
    """11:35Z to 12:00Z on a trading weekday (Mon-Fri; the calendar's holidays only widen the safe side)."""
    return t.weekday() < 5 and dt.time(11, 35) <= t.time() <= dt.time(12, 0)


def statement_hash(st):
    return hashlib.sha256(json.dumps(st, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- the record's clauses (pure)
def head_problems(rec, new_resource):
    pr = []
    keys = ["claim", "gates", "ledger_entry", "applier", "before", "build", "plan", "apply_finished_utc", "after", "dry_run", "time_trigger", "first_write", "range",
            "ledger_closed", "reads"]
    if not isinstance(rec, dict) or any(k not in rec for k in keys):
        return ["the record must carry %s" % keys]
    if rec["claim"] != "measured" or rec["applier"] != APPLIER:
        pr.append("claim must be measured and applier %s" % APPLIER)
    g = rec["gates"]
    if not (isinstance(g, dict) and g.get("packet_sha256") == PACKET_SHA and g.get("coo_half_signed") is True and g.get("cto_half_signed") is True
            and g.get("pins_ok") is True and isinstance(g.get("one_change_at_a_time"), dict)
            and is_int(g["one_change_at_a_time"].get("worktrees_read")) and g["one_change_at_a_time"]["worktrees_read"] > 0
            and g["one_change_at_a_time"].get("open_markers_naming_this_surface") == 0):
        pr.append("gates must record the packet sha256, both halves signed, the pins, and the worktree denominator with 0 open markers naming this surface")
    if not (isinstance(rec["ledger_entry"], str) and rec["ledger_entry"].strip()):
        pr.append("ledger_entry must name the ledger")
    b = rec["before"]
    if not (isinstance(b, dict) and b.get("function_code_sha256") == OLD_CODE_B64 and b.get("artifact_version_id") == OLD_ARTIFACT_VERSION
            and isinstance(b.get("policy"), dict) and sorted(b["policy"]) == sorted(SIDS) and isinstance(b.get("write_resources"), list) and len(b["write_resources"]) == 6
            and b.get("new_prefix_objects") == 0 and isinstance(b.get("schedule"), dict) and b["schedule"].get("state") == "ENABLED"
            and is_int((b.get("last_fire") or {}).get("duration_ms")) and isinstance(b.get("other_tables"), dict) and sorted(b["other_tables"]) == sorted(OTHER_TABLES)):
        pr.append("before must be the packet's section 3: the old code hash and artifact version, eleven statements, six write resources, an empty new prefix, an ENABLED schedule, the last fire's duration, the six other tables' counts")
    bd = rec["build"]
    if not (isinstance(bd, dict) and bd.get("zip_sha256_b64") == BUILD_B64 and bd.get("import_smoke_rc") == 0 and isinstance(bd.get("landed_version_id"), str)
            and bd["landed_version_id"] and bd["landed_version_id"] != OLD_ARTIFACT_VERSION and bd.get("built_equals_landed") is True):
        pr.append("build must equal the packet's base64 sha256, import smoke rc 0, a NEW landed version, built equals landed")
    pl = rec["plan"]
    if not (isinstance(pl, dict) and pl.get("add") == 0 and pl.get("change") == 2 and pl.get("destroy") == 0
            and sorted(pl.get("change_addresses") or []) == ["aws_iam_role_policy.irpt_reporting_gold", "module.irpt_reporting_gold.aws_lambda_function.this"]
            and pl.get("policy_added_resources") == [new_resource] and pl.get("policy_other_changes") == 0 and pl.get("replan_no_changes") is True):
        pr.append("plan must read exactly 0/2/0 on the two addresses, the policy change the ONE new write resource and nothing else, and a re-plan with no changes")
    fin = rec["apply_finished_utc"]
    try:
        if in_fire_window(parse_utc(fin)):
            pr.append("the apply finished inside the fire window 11:35Z to 12:00Z")
    except (ValueError, TypeError):
        pr.append("apply_finished_utc must be a UTC time")
    a = rec["after"]
    if not (isinstance(a, dict) and isinstance(a.get("function"), dict) and a["function"].get("memory") == 8192 and a["function"].get("timeout") == 900
            and a["function"].get("code_sha256") == BUILD_B64 and isinstance(a.get("write_resources"), list) and len(a["write_resources"]) == 7
            and a["write_resources"][-1] == new_resource and a["write_resources"][:6] == b.get("write_resources")
            and isinstance(a.get("policy"), dict) and sorted(a["policy"]) == sorted(SIDS)
            and all(a["policy"][s] == b["policy"][s] for s in SIDS if s != WRITE_SID) and a["policy"][WRITE_SID] != b["policy"][WRITE_SID]):
        pr.append("after must show the new code hash, memory 8192, timeout 900, seven write resources (the six, then the new one), every statement but the write statement byte-identical")
    return pr


def events_problems(rec, new_prefix_uri):
    pr = []
    dr = rec["dry_run"]
    if not (isinstance(dr, dict) and dr.get("status_code") == 200 and dr.get("function_error") is None and isinstance(dr.get("payload"), dict)
            and dr["payload"].get("stages") == ["transaction"] and dr["payload"].get("dry_run") is True
            and isinstance(dr.get("returned"), dict) and dr["returned"].get("stages") == ["transaction"] and dr["returned"].get("transaction_failed") == {}
            and isinstance(dr["returned"].get("transaction_rows"), dict) and len(dr["returned"]["transaction_rows"]) == 1
            and all(is_int(v) and v > 0 for v in dr["returned"]["transaction_rows"].values()) and dr.get("prefix_objects_after") == 0
            and is_int((dr.get("report") or {}).get("duration_ms")) and (dr["report"].get("max_memory_used_mb") or 0) <= 6553):
        pr.append("dry_run must be a 200 with no function error, stages [transaction], dry_run true, one day with a positive count, none failed, memory within 6,553 MB, and 0 objects at the new prefix after")
    tt = rec["time_trigger"]
    if not (isinstance(tt, dict) and is_int(tt.get("act3_stage_duration_ms")) and is_int(tt.get("last_pre_apply_fire_duration_ms"))
            and tt.get("sum_ms") == tt["act3_stage_duration_ms"] + tt["last_pre_apply_fire_duration_ms"] and tt.get("over_720s") == (tt["sum_ms"] > 720000)
            and tt.get("rollback_taken") in (False, True)):
        pr.append("time_trigger must carry the dry run's duration, the last pre-apply fire's duration, their sum, over_720s computed from it, and whether the rollback was taken (the CTO's trigger)")
    elif tt.get("over_720s") and not tt.get("rollback_taken"):
        pr.append("the sum exceeds 720 s: the rollback must have been taken before the next 11:41Z fire (the CTO's word)")
    fw = rec["first_write"]
    if not (isinstance(fw, dict) and fw.get("status_code") == 200 and fw.get("function_error") is None and isinstance(fw.get("payload"), dict)
            and fw["payload"].get("stages") == ["transaction"] and not fw["payload"].get("dry_run")
            and isinstance(fw.get("returned"), dict) and fw["returned"].get("transaction_failed") == {}
            and fw["returned"].get("transaction_rows") == (dr.get("returned") or {}).get("transaction_rows")
            and len(fw.get("partitions_after") or []) == 1 and fw.get("schema_hash") == SCHEMA_HASH and fw.get("claims_ok") is True and fw.get("flow_class_ok") is True
            and fw.get("columns") == 19):
        pr.append("first_write must be a 200, stages [transaction], the same one day with the SAME count as the dry run, none failed, exactly one partition after, 19 columns, the contract's schema hash, claims and flow classes valid")
    rg = rec["range"]
    if not (isinstance(rg, dict) and rg.get("status_code") == 200 and rg.get("function_error") is None and isinstance(rg.get("payload"), dict)
            and rg["payload"].get("stages") == ["transaction"] and isinstance(rg.get("returned"), dict) and rg["returned"].get("transaction_failed") == {}
            and is_int(rg.get("days_written")) and 1 <= rg["days_written"] <= 25 and rg["days_written"] == len(rg["returned"].get("transaction_rows") or {})
            and rg.get("partitions_after") == rg["days_written"] and rg.get("other_tables_unchanged") is True):
        pr.append("range must be a 200, stages [transaction], at most 25 days all written and none failed, the partition count equal to the days written, the other tables unchanged")
    if rec.get("ledger_closed") is not False:
        pr.append("ledger_closed must be false (the issuer verifies and closes it, after the first scheduled fire is read)")
    if rec.get("reads") != {"vendor_calls": 0, "secret_reads": 0}:
        pr.append("reads must be {vendor_calls 0, secret_reads 0}")
    del new_prefix_uri
    return pr


# ---------------------------------------------------------------- fresh reads (injectable)
def aws_json(args):
    shim = str(Path(__file__).resolve().parents[9] / ".tools" / "aws.cmd")  # the Windows shim; the extensionless one is for MSYS shells
    run = subprocess.run([shim] + args + ["--output", "json"], capture_output=True, text=True, timeout=300)
    if run.returncode != 0:
        raise Fail("aws %s failed: %s" % (" ".join(args[:3]), (run.stderr or run.stdout)[-200:]))
    return json.loads(run.stdout or "null")


class LiveReads(object):
    def function(self):
        c = aws_json(["lambda", "get-function-configuration", "--function-name", FUNCTION])
        return {"code_sha256": c["CodeSha256"], "memory": c["MemorySize"], "timeout": c["Timeout"], "layers": [x["Arn"] for x in c.get("Layers", [])],
                "environment": c.get("Environment"), "handler": c["Handler"], "runtime": c["Runtime"]}

    def policy(self):
        p = aws_json(["iam", "get-role-policy", "--role-name", ROLE, "--policy-name", POLICY])["PolicyDocument"]["Statement"]
        return {s["Sid"]: s for s in p}

    def schedule(self):
        s = aws_json(["scheduler", "get-schedule", "--name", SCHEDULE])
        return {"state": s["State"], "cron": s["ScheduleExpression"]}

    def artifact_versions(self, bucket, key):
        v = aws_json(["s3api", "list-object-versions", "--bucket", bucket, "--prefix", key, "--max-items", "3"])
        return [x["VersionId"] for x in v.get("Versions", []) if x["Key"] == key and x.get("IsLatest")]

    def partitions(self, bucket, prefix):
        """The day partitions under a prefix (the CLI auto-paginates; CommonPrefixes are counted client-side)."""
        r = aws_json(["s3api", "list-objects-v2", "--bucket", bucket, "--prefix", prefix, "--delimiter", "/"]) or {}
        return sorted(c["Prefix"] for c in r.get("CommonPrefixes", []))


def split_uri(uri):
    rest = uri[len("s3://"):]
    b, _, k = rest.partition("/")
    return b, k


def addresses(root):
    sys.path.insert(0, str(Path(root, "lib")))
    import opal_naming
    tx = opal_naming.address("irpt", FIRM, "gold", "account_transaction", "date=2000-01-03")
    bucket, key = split_uri(tx)
    tx_prefix = key.rsplit("/date=", 1)[0] + "/"
    res = "arn:aws:s3:::%s/%s*" % (bucket, tx_prefix)
    others = {t: split_uri(opal_naming.address("irpt", FIRM, "gold", t, "date=2000-01-03"))[1].rsplit("/date=", 1)[0] + "/" for t in OTHER_TABLES}
    return bucket, tx_prefix, res, others


def live_problems(rec, reads, new_resource):
    pr = []
    f = reads.function()
    af = rec["after"]["function"]
    if not (f["code_sha256"] == BUILD_B64 == rec["build"]["zip_sha256_b64"] and f["memory"] == 8192 and f["timeout"] == 900 and f["environment"] is None
            and len(f["layers"]) == 1 and f["handler"] == "handler.lambda_handler" and f["runtime"] == "python3.12"):
        pr.append("the function must run the NEW code (CodeSha256 equal to the build) with memory 8192, timeout 900, no environment, the one layer, the same handler and runtime: %r" % ({k: f[k] for k in ("code_sha256", "memory", "timeout")},))
    del af
    st = reads.policy()
    if sorted(st) != sorted(SIDS):
        pr.append("the role policy must hold the eleven statements by id")
    else:
        for sid in SIDS:
            h = statement_hash(st[sid])
            want = rec["after"]["policy"][sid]
            if h != want:
                pr.append("statement %s differs from the record's after-state" % sid)
            if sid != WRITE_SID and h != rec["before"]["policy"][sid]:
                pr.append("statement %s changed from the before-state (only the write statement may)" % sid)
        res = st[WRITE_SID].get("Resource")
        res = [res] if isinstance(res, str) else list(res or [])
        if sorted(res) != sorted(rec["before"]["write_resources"] + [new_resource]) or st[WRITE_SID].get("Action") not in ("s3:PutObject", ["s3:PutObject"]):
            pr.append("the write statement must be s3:PutObject over the six old resources plus exactly the new one")
    sc = reads.schedule()
    if sc != rec["before"]["schedule"] or sc["state"] != "ENABLED":
        pr.append("the schedule must be ENABLED and untouched: %r" % (sc,))
    return pr


def prefix_problems(rec, reads, bucket, tx_prefix, others):
    pr = []
    parts = reads.partitions(bucket, tx_prefix)
    if len(parts) != rec["range"]["partitions_after"]:
        pr.append("the new prefix must hold exactly %d day partitions (the range's), found %d" % (rec["range"]["partitions_after"], len(parts)))
    fw_day = (rec["first_write"].get("partitions_after") or [None])[0]
    if fw_day and not any(p.endswith("date=%s/" % str(fw_day).replace("date=", "").strip("/")) for p in parts):
        pr.append("the first write's day is not among the prefix's partitions")
    for t, pref in others.items():
        now = len(reads.partitions(bucket, pref))
        if now != rec["before"]["other_tables"][t].get("partitions"):
            pr.append("table %s now holds %d day partitions, the record's before-state said %r" % (t, now, rec["before"]["other_tables"][t].get("partitions")))
    return pr


def load_record(root):
    p = Path(root, REC_REL)
    need(p.is_file(), "missing the applier's record " + REC_REL)
    return json.loads(p.read_text(encoding="utf-8"))


def packet_problems(root):
    p = Path(root, PACKET_REL)
    need(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == PACKET_SHA, "the packet's bytes are not the signed ones (sha256)")
    for rel, who in ((COO_REL, "COO"), (CTO_REL, "CTO")):
        t = Path(root, rel)
        need(t.is_file() and PACKET_SHA in t.read_text(encoding="utf-8") and "SIGNED" in t.read_text(encoding="utf-8"), "the %s half is missing or is not SIGNED on the packet's sha256" % who)


def ac1(root):
    packet_problems(root)
    rec = load_record(root)
    _b, _p, res, _o = addresses(root)
    pr = head_problems(rec, res)
    need(not pr, "; ".join(pr))


def ac2(root):
    rec = load_record(root)
    _b, _p, res, _o = addresses(root)
    pr = live_problems(rec, LiveReads(), res)
    r = LiveReads()
    ver = r.artifact_versions("opal-313476888478-lambda-artifacts", "investor-reporting/irpt-reporting-gold-lambda.zip")
    if ver != [rec["build"]["landed_version_id"]]:
        pr.append("the artifact key's current version must be the recorded landed one: %r" % (ver,))
    need(not pr, "; ".join(pr))


def ac3(root):
    rec = load_record(root)
    bucket, tx_prefix, res, others = addresses(root)
    pr = events_problems(rec, tx_prefix)
    pr += prefix_problems(rec, LiveReads(), bucket, tx_prefix, others)
    if not Path(root, "org/critical_paths/.open_deploys", rec["ledger_entry"] + ".json").is_file():
        pr.append("the ledger's open marker org/critical_paths/.open_deploys/%s.json must exist (the ledger stays open until the first scheduled fire is read)" % rec["ledger_entry"])
    need(not pr, "; ".join(pr))


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    new = "arn:aws:s3:::b/irpt/x/gold/account_transaction/*"
    old6 = ["r%d" % i for i in range(6)]
    pol = {s: "h_" + s for s in SIDS}
    pol_after = dict(pol, **{WRITE_SID: "h_new"})
    rec = {"claim": "measured", "applier": APPLIER, "ledger_entry": "irpt-dashbd-49f-transaction-wiring-20261016", "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0},
           "gates": {"packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pins_ok": True,
                     "one_change_at_a_time": {"worktrees_read": 91, "open_markers_naming_this_surface": 0}},
           "before": {"function_code_sha256": OLD_CODE_B64, "artifact_version_id": OLD_ARTIFACT_VERSION, "policy": pol, "write_resources": old6, "new_prefix_objects": 0,
                      "schedule": {"state": "ENABLED", "cron": "c"}, "last_fire": {"duration_ms": 300000}, "other_tables": {t: {"partitions": 7} for t in OTHER_TABLES}},
           "build": {"zip_sha256_b64": BUILD_B64, "import_smoke_rc": 0, "landed_version_id": "NEWV", "built_equals_landed": True},
           "plan": {"add": 0, "change": 2, "destroy": 0, "change_addresses": ["aws_iam_role_policy.irpt_reporting_gold", "module.irpt_reporting_gold.aws_lambda_function.this"],
                    "policy_added_resources": [new], "policy_other_changes": 0, "replan_no_changes": True},
           "apply_finished_utc": "2026-10-16T23:10:00Z",
           "after": {"function": {"memory": 8192, "timeout": 900, "code_sha256": BUILD_B64}, "write_resources": old6 + [new], "policy": pol_after},
           "dry_run": {"status_code": 200, "function_error": None, "payload": {"stages": ["transaction"], "dry_run": True},
                       "returned": {"stages": ["transaction"], "transaction_failed": {}, "transaction_rows": {"2026-10-15": 100}}, "prefix_objects_after": 0,
                       "report": {"duration_ms": 90000, "max_memory_used_mb": 900}},
           "time_trigger": {"act3_stage_duration_ms": 90000, "last_pre_apply_fire_duration_ms": 300000, "sum_ms": 390000, "over_720s": False, "rollback_taken": False},
           "first_write": {"status_code": 200, "function_error": None, "payload": {"stages": ["transaction"]},
                           "returned": {"transaction_failed": {}, "transaction_rows": {"2026-10-15": 100}}, "partitions_after": ["2026-10-15"], "schema_hash": SCHEMA_HASH,
                           "claims_ok": True, "flow_class_ok": True, "columns": 19},
           "range": {"status_code": 200, "function_error": None, "payload": {"stages": ["transaction"]},
                     "returned": {"transaction_failed": {}, "transaction_rows": {"d%d" % i: 5 for i in range(25)}}, "days_written": 25, "partitions_after": 25,
                     "other_tables_unchanged": True}}
    arm("head-green", head_problems(rec, new), [])
    arm("events-green", events_problems(rec, "p/"), [])
    r2 = copy.deepcopy(rec)
    r2["plan"]["change"] = 3
    arm("plan-red", len(head_problems(r2, new)), 1)
    r3 = copy.deepcopy(rec)
    r3["apply_finished_utc"] = "2026-10-19T11:50:00Z"
    arm("window-red", len(head_problems(r3, new)), 1)
    r4 = copy.deepcopy(rec)
    r4["after"]["policy"]["OwnLogStreamOnly"] = "x"
    arm("other-statement-changed-red", len(head_problems(r4, new)), 1)
    r5 = copy.deepcopy(rec)
    r5["time_trigger"].update({"sum_ms": 800000, "act3_stage_duration_ms": 500000, "over_720s": True})
    arm("trigger-without-rollback-red", len(events_problems(r5, "p/")), 1)
    r6 = copy.deepcopy(rec)
    r6["first_write"]["returned"]["transaction_rows"] = {"2026-10-15": 99}
    arm("first-write-count-differs-red", len(events_problems(r6, "p/")), 1)
    r7 = copy.deepcopy(rec)
    r7["range"]["days_written"] = 26
    arm("range-too-long-red", len(events_problems(r7, "p/")), 1)
    arm("window-function", (in_fire_window(parse_utc("2026-10-19T11:41:00Z")), in_fire_window(parse_utc("2026-10-17T11:41:00Z")), in_fire_window(parse_utc("2026-10-19T13:00:00Z"))), (True, False, False))
    arm("statement-hash-stable", statement_hash({"a": 1, "b": [2]}) == statement_hash({"b": [2], "a": 1}), True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF136-4-AC1": ac1, "DBF136-4-AC2": ac2, "DBF136-4-AC3": ac3}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
