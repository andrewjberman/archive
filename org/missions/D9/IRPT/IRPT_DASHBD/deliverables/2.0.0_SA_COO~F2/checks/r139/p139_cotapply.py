"""IRPT_DASHBD round 139, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- the APPLY of the signed Cottonwood transaction pair by 0.7.0_AE_CloudOps~IB2 (order DB-f-2703).

  Packet NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md REVISION 1 (sha256 below), COO half signed @511122931b, CTO half signed @04175d4e4a. The applier's record is
  deliverables/0.7.0_AE_CloudOps~IB2/COTTONWOOD_TRANSACTION_APPLY_RECORD.json. The criteria grade the record and then re-read the world FRESH (AWS GET, list and describe only).

  DBF139-3-AC1  gates (incl. the CTO's order of firms and the clear rewrite ledger), ledger, the bundle's build, the plan (exactly 0 add / 2 change / 0 destroy, the new statement, code only)
                and the apply outside the fire window
  DBF139-3-AC2  fresh reads: the function runs the NEW code (CodeSha256 equal to the build, memory, timeout, layer and environment unchanged); the role policy holds the six statements, the
                five old ones byte-identical to the before-state and the new one PutObject-only on the one prefix; the schedule untouched; the artifact key's current version is the landed one
  DBF139-3-AC3  the returns-only dry run (rows equal the landed day's), the transaction dry run, the first one-day write and the bounded range (at most 25 days, 19 columns, the schema hash,
                valid claims) and a fresh LIST of the new prefix equal to the range's days, each partition with data.parquet and manifest.json, the returns prefix unchanged

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import datetime as dt
import hashlib
import json
import subprocess
import sys
from pathlib import Path

APPLIER = "0.7.0_AE_CloudOps~IB2"
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.7.0_AE_CloudOps~IB2/COTTONWOOD_TRANSACTION_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~F2/NEVER_WIDEN_PACKET_COTTONWOOD_TRANSACTION_WIRING.md"
COO_REL = D + "2.0.0_SA_COO~F2/NEVER_WIDEN_COTTONWOOD_TRANSACTION_WIRING_COO_HALF.md"
CTO_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_TRANSACTION_WIRING_CTO_HALF.md"
PACKET_SHA = "c5b7d756c11edb2d767a02dcaab86f2eb209fe5714a69044a53d0a49410db156"
BUILD_B64 = "6IrkQGalZOejYzTlB/LAQaYh9aTtbj8JMrzJgLZgUMI="
FUNCTION = "irpt-cot-account-return-daily-lambda"
ROLE = "irpt-cot-account-return-daily-execution-role"
POLICY = "irpt-cot-account-return-daily-execution-policy"
SCHEDULE = "irpt-cot-account-return-daily-daily"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "investor-reporting/irpt-cot-account-return-daily-lambda.zip"
BUCKET = "opal-data-cottonwood"
TX_PREFIX = "irpt/cottonwood/gold/account_transaction/"
RETURNS_PREFIX = "irpt/cottonwood/gold/account_return_daily/"
OLD_SIDS = ["ListSilverTablePrefixesOnly", "ReadTwoBlackDiamondSilverTablesOnly", "WriteTheOneAccountReturnDailyGoldPrefixOnly", "ListTheOneAccountReturnDailyGoldPrefixOnly", "OwnLogStreamOnly"]
NEW_SID = "WriteTheAccountTransactionGoldPrefixOnly"
NEW_RESOURCE = "arn:aws:s3:::%s/%s*" % (BUCKET, TX_PREFIX)
SCHEMA_HASH = "ac652e2f71b18427b52f321858163768158f850ec173d1e592c7c3abe815bb6a"
MAX_DAYS = 25


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
    """12:10Z to 12:30Z on a trading weekday (Mon-Fri; the calendar's holidays only widen the safe side): the packet's condition 3."""
    return t.weekday() < 5 and dt.time(12, 10) <= t.time() <= dt.time(12, 30)


def statement_hash(st):
    return hashlib.sha256(json.dumps(st, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def head_problems(rec):
    pr = []
    keys = ["claim", "gates", "ledger_entry", "applier", "before", "build", "plan", "apply_finished_utc", "after", "returns_dry_run", "dry_run", "first_write", "range", "ledger_closed", "reads"]
    if not isinstance(rec, dict) or any(k not in rec for k in keys):
        return ["the record must carry %s" % keys]
    if rec["claim"] != "measured" or rec["applier"] != APPLIER:
        pr.append("claim must be measured and applier %s" % APPLIER)
    g = rec["gates"]
    ok = isinstance(g, dict) and g.get("packet_sha256") == PACKET_SHA and g.get("coo_half_signed") is True and g.get("cto_half_signed") is True and g.get("pins_ok") is True \
        and g.get("monday_49f_read_passed") is True and g.get("inflection_receipt_closed") is True and g.get("d2_reland_pairs_closed") is True \
        and g.get("open_rewrite_ledgers_on_root") == 0 and isinstance(g.get("one_change_at_a_time"), dict) and is_int(g["one_change_at_a_time"].get("worktrees_read")) \
        and g["one_change_at_a_time"]["worktrees_read"] > 0 and g["one_change_at_a_time"].get("open_markers_naming_this_surface") == 0
    if not ok:
        pr.append("gates must record the packet sha256, both halves signed, the pins, Monday's 49 Financial read PASSED, the Inflection receipt, ~D2's re-land pairs closed, 0 open rewrite ledgers on the root, and the worktree denominator with 0 open markers")
    if not (isinstance(rec["ledger_entry"], str) and rec["ledger_entry"].strip()):
        pr.append("ledger_entry must name the ledger")
    b = rec["build"]
    if not (isinstance(b, dict) and b.get("zip_sha256_b64") == BUILD_B64 and b.get("second_run_equal") is True and b.get("import_smoke_rc") == 0 and b.get("atc_import_error") is None
            and b.get("landed_version_id") and b.get("built_equals_landed") is True):
        pr.append("build must record the packet's base64 sha256 %s, two equal runs, an import smoke rc 0 with ATC_IMPORT_ERROR None, and a landed version equal to the build" % BUILD_B64)
    p = rec["plan"]
    if not (isinstance(p, dict) and p.get("add") == 0 and p.get("change") == 2 and p.get("destroy") == 0 and isinstance(p.get("change_addresses"), list) and len(p["change_addresses"]) == 2
            and p.get("policy_added_sids") == [NEW_SID] and p.get("function_change_attributes_code_only") is True and p.get("naming_gate_refuse") == 0 and p.get("replan_no_changes") is True):
        pr.append("plan must read exactly 0 add / 2 change / 0 destroy, the two addresses, the one added statement %s, the function changing by code attributes only, 0 naming REFUSE, a re-plan of No changes" % NEW_SID)
    try:
        if in_fire_window(parse_utc(rec["apply_finished_utc"])):
            pr.append("the apply finished inside the daily fire window (12:10Z to 12:30Z)")
    except (ValueError, TypeError):
        pr.append("apply_finished_utc must be a UTC timestamp")
    if rec["ledger_closed"] is not False:
        pr.append("the ledger stays open until the first scheduled fire is read")
    return pr


def events_problems(rec):
    pr = []
    rd, dr, fw, rg = rec["returns_dry_run"], rec["dry_run"], rec["first_write"], rec["range"]
    if not (isinstance(rd, dict) and is_int(rd.get("rows_dry")) and rd["rows_dry"] > 0 and rd.get("rows_dry") == rd.get("rows_landed") and rd.get("wrote_nothing") is True):
        pr.append("the returns-only dry run after Act 2 must write nothing and its rows must equal the landed day's rows")
    if not (isinstance(dr, dict) and dr.get("transaction_failed") == {} and isinstance(dr.get("transaction_rows"), dict) and len(dr["transaction_rows"]) == 1
            and all(is_int(v) and v > 0 for v in dr["transaction_rows"].values()) and dr.get("prefix_objects_after") == 0
            and is_int(dr.get("max_memory_mb")) and dr["max_memory_mb"] <= 819 and is_int(dr.get("duration_ms")) and dr["duration_ms"] <= 720000):
        pr.append("the transaction dry run must return one day with a positive count, none failed, 0 objects at the prefix after, peak memory <= 819 MB and duration <= 720 s")
    if not (isinstance(fw, dict) and fw.get("transaction_rows") == dr.get("transaction_rows") and fw.get("transaction_failed") == {} and isinstance(fw.get("partitions_after"), list)
            and len(fw["partitions_after"]) == 1 and fw.get("columns") == 19 and fw.get("schema_hash") == SCHEMA_HASH and fw.get("claims_ok") is True):
        pr.append("the first write must equal the dry run's count, fail nothing, leave exactly one partition, and carry 19 columns, the schema hash and valid claims")
    ds = rg.get("days_written") if isinstance(rg, dict) else None
    if not (is_int(ds) and 1 <= ds <= MAX_DAYS and rg.get("partitions_after") == ds and rg.get("transaction_failed") == {} and rg.get("returns_prefix_unchanged") is True
            and isinstance(rg.get("days"), list) and len(rg["days"]) == ds and is_int(rg.get("max_memory_mb")) and rg["max_memory_mb"] <= 819):
        pr.append("the range must write 1 to %d days with none failed, a partition per day, peak memory <= 819 MB, and leave the returns prefix unchanged" % MAX_DAYS)
    return pr


def aws_json(root, args):
    shim = str(Path(root, ".tools", "aws.cmd"))
    run = subprocess.run([shim] + args + ["--output", "json"], capture_output=True, text=True, timeout=300)
    if run.returncode != 0:
        raise Fail("aws %s failed: %s" % (" ".join(args[:3]), (run.stderr or run.stdout)[-200:]))
    return json.loads(run.stdout or "null")


def load_record(root):
    p = Path(root, REC_REL)
    need(p.is_file(), "missing the applier's record " + REC_REL)
    return json.loads(p.read_text(encoding="utf-8"))


def packet_problems(root):
    p = Path(root, PACKET_REL)
    need(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == PACKET_SHA, "the packet's bytes are not the signed ones (sha256)")
    for rel, who in ((COO_REL, "COO"), (CTO_REL, "CTO")):
        t = Path(root, rel)
        txt = t.read_text(encoding="utf-8") if t.is_file() else ""
        need(PACKET_SHA in txt or PACKET_SHA[:8] in txt, "the %s half is missing or does not name the packet's sha256" % who)
        need("SIGNED" in txt, "the %s half is not SIGNED" % who)


def ac1(root):
    packet_problems(root)
    pr = head_problems(load_record(root))
    need(not pr, "; ".join(pr))


def ac2(root):
    rec = load_record(root)
    pr = []
    c = aws_json(root, ["lambda", "get-function-configuration", "--function-name", FUNCTION])
    if not (c["CodeSha256"] == BUILD_B64 == rec["build"]["zip_sha256_b64"] and c["MemorySize"] == 1024 and c["Timeout"] == 900 and len(c.get("Layers", [])) == 1
            and not (c.get("Environment") or {}).get("Variables") and c["Handler"] == "handler.lambda_handler" and c["Runtime"] == "python3.12"):
        pr.append("the function must run the NEW code (CodeSha256 equal to the build) with memory 1024, timeout 900, the one layer, no environment, the same handler and runtime")
    st = {s["Sid"]: s for s in aws_json(root, ["iam", "get-role-policy", "--role-name", ROLE, "--policy-name", POLICY])["PolicyDocument"]["Statement"]}
    if sorted(st) != sorted(OLD_SIDS + [NEW_SID]):
        pr.append("the role policy must hold the five original statements and the new one")
    else:
        for sid in OLD_SIDS:
            if statement_hash(st[sid]) != rec["before"].get("policy", {}).get(sid):
                pr.append("statement %s differs from the record's before-state (only one statement may be added)" % sid)
        n = st[NEW_SID]
        res = [n["Resource"]] if isinstance(n["Resource"], str) else list(n["Resource"])
        act = [n["Action"]] if isinstance(n["Action"], str) else list(n["Action"])
        if res != [NEW_RESOURCE] or act != ["s3:PutObject"] or n.get("Effect") != "Allow" or "Condition" in n:
            pr.append("the new statement must be Allow, s3:PutObject only, on %s, no condition" % NEW_RESOURCE)
    s = aws_json(root, ["scheduler", "get-schedule", "--name", SCHEDULE])
    if {"state": s["State"], "cron": s["ScheduleExpression"]} != rec["before"].get("schedule") or s["State"] != "ENABLED":
        pr.append("the schedule must be ENABLED and untouched")
    v = aws_json(root, ["s3api", "list-object-versions", "--bucket", ARTIFACT_BUCKET, "--prefix", ARTIFACT_KEY, "--max-items", "3"])
    latest = [x["VersionId"] for x in v.get("Versions", []) if x["Key"] == ARTIFACT_KEY and x.get("IsLatest")]
    if latest != [rec["build"]["landed_version_id"]]:
        pr.append("the artifact key's current version must be the recorded landed one: %r" % (latest,))
    need(not pr, "; ".join(pr[:6]))


def ac3(root):
    rec = load_record(root)
    pr = events_problems(rec)
    if not pr:
        days = sorted(rec["range"]["days"])
        r = aws_json(root, ["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", TX_PREFIX, "--delimiter", "/"]) or {}
        parts = sorted(c["Prefix"][len(TX_PREFIX):].strip("/").replace("date=", "") for c in r.get("CommonPrefixes", []))
        if parts != days:
            pr.append("the new prefix holds %d partitions, the record names %d days (they must be the same days)" % (len(parts), len(days)))
        else:
            for d in parts:
                objs = aws_json(root, ["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", "%sdate=%s/" % (TX_PREFIX, d)]) or {}
                keys = sorted(o["Key"].rsplit("/", 1)[-1] for o in objs.get("Contents", []))
                if keys != ["data.parquet", "manifest.json"]:
                    pr.append("partition %s must hold exactly data.parquet and manifest.json (found %r)" % (d, keys))
                    break
        rp = aws_json(root, ["s3api", "list-objects-v2", "--bucket", BUCKET, "--prefix", RETURNS_PREFIX, "--delimiter", "/"]) or {}
        if len(rp.get("CommonPrefixes", [])) != rec["before"].get("returns_partitions") and not rec["range"].get("returns_prefix_unchanged"):
            pr.append("the returns prefix's partition count differs from the before-state")
    need(not pr, "; ".join(pr[:6]))


def selftest():
    bad = count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    rec = {"claim": "measured", "applier": APPLIER, "ledger_entry": "x", "ledger_closed": False, "reads": {}, "before": {},
           "gates": {"packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pins_ok": True, "monday_49f_read_passed": True, "inflection_receipt_closed": True,
                     "d2_reland_pairs_closed": True, "open_rewrite_ledgers_on_root": 0, "one_change_at_a_time": {"worktrees_read": 90, "open_markers_naming_this_surface": 0}},
           "build": {"zip_sha256_b64": BUILD_B64, "second_run_equal": True, "import_smoke_rc": 0, "atc_import_error": None, "landed_version_id": "v1", "built_equals_landed": True},
           "plan": {"add": 0, "change": 2, "destroy": 0, "change_addresses": ["a", "b"], "policy_added_sids": [NEW_SID], "function_change_attributes_code_only": True, "naming_gate_refuse": 0,
                    "replan_no_changes": True},
           "apply_finished_utc": "2026-10-21T14:00:00Z", "after": {},
           "returns_dry_run": {"rows_dry": 5000, "rows_landed": 5000, "wrote_nothing": True},
           "dry_run": {"transaction_rows": {"2026-10-20": 8500}, "transaction_failed": {}, "prefix_objects_after": 0, "max_memory_mb": 400, "duration_ms": 9000},
           "first_write": {"transaction_rows": {"2026-10-20": 8500}, "transaction_failed": {}, "partitions_after": ["2026-10-20"], "columns": 19, "schema_hash": SCHEMA_HASH, "claims_ok": True},
           "range": {"days_written": 2, "partitions_after": 2, "transaction_failed": {}, "returns_prefix_unchanged": True, "days": ["2026-10-19", "2026-10-20"], "max_memory_mb": 500}}
    arm("head-green", head_problems(rec), [])
    arm("events-green", events_problems(rec), [])
    arm("plan-destroy", len(head_problems(dict(rec, plan=dict(rec["plan"], destroy=1)))), 1)
    arm("build-hash", len(head_problems(dict(rec, build=dict(rec["build"], zip_sha256_b64="x")))), 1)
    arm("apply-in-window", len(head_problems(dict(rec, apply_finished_utc="2026-10-21T12:15:00Z"))), 1)
    arm("reland-open", len(head_problems(dict(rec, gates=dict(rec["gates"], d2_reland_pairs_closed=False)))), 1)
    arm("rewrite-ledger-open", len(head_problems(dict(rec, gates=dict(rec["gates"], open_rewrite_ledgers_on_root=1)))), 1)
    arm("returns-rows-differ", len(events_problems(dict(rec, returns_dry_run={"rows_dry": 5000, "rows_landed": 4999, "wrote_nothing": True}))), 1)
    arm("dry-run-wrote", len(events_problems(dict(rec, dry_run=dict(rec["dry_run"], prefix_objects_after=2)))), 1)
    arm("memory-over-80pct", len(events_problems(dict(rec, dry_run=dict(rec["dry_run"], max_memory_mb=900)))), 1)
    arm("write-count-differs", len(events_problems(dict(rec, first_write=dict(rec["first_write"], transaction_rows={"2026-10-20": 1})))), 1)
    arm("range-too-long", len(events_problems(dict(rec, range=dict(rec["range"], days_written=26, partitions_after=26, days=["d"] * 26)))), 1)
    arm("fire-window", (in_fire_window(parse_utc("2026-10-21T12:15:00Z")), in_fire_window(parse_utc("2026-10-21T13:00:00Z")), in_fire_window(parse_utc("2026-10-24T12:15:00Z"))), (True, False, False))
    arm("statement-hash-stable", statement_hash({"a": 1, "b": 2}) == statement_hash({"b": 2, "a": 1}), True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3 or argv[2] not in ("DBF139-3-AC1", "DBF139-3-AC2", "DBF139-3-AC3"):
        print("usage: p139_cotapply.py <repo_root> DBF139-3-AC1|AC2|AC3 | --selftest")
        return 2
    try:
        {"DBF139-3-AC1": ac1, "DBF139-3-AC2": ac2, "DBF139-3-AC3": ac3}[argv[2]](argv[1])
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % argv[2])
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % argv[2])
        return 1
    print("%s PASS" % argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
