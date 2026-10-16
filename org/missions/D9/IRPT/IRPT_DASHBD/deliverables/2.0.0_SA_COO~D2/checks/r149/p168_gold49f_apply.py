"""IRPT_DASHBD round 149, workstream GOLD49FAPPLY (issuer 2.0.0_SA_COO~D2) -- DB-b-300, the APPLY of the signed never-widen pair for the 49 Financial reporting-gold function (packet sha256 d2c27ac2bdc5,
COO half signed @c17e5d10b9, CTO half signed @89ca7c661c): the new bundle, ONE safe-apply (plan exactly 0 add / 2 change / 0 destroy: the role policy's one list pattern and the function's code), hop 1's FIRST WRITE
by a hand event, a ONE-DAY backfill of 2026-10-15, the CTO's flip count, and the republish of the series. WORLD. The record is the applier's; the checker re-reads the world.

  DBC168-1-AC1  the record's head: packet and halves, gates, ledger and applier, before, build, plan, the policy change, the timing rules
  DBC168-2-AC1  FRESH live reads: the function's code, the role policy (eleven statements, the one added pattern), the schedule, the artifact version, the first write's partition
  DBC168-3-AC1  the backfill, the flips and the republish in the record, and FRESH reads of the newest returns partition, the other tables' row counts, the series and the open ledger

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import base64
import copy
import datetime as dt
import hashlib
import importlib.util
import io
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


H = helper("r147/p151_pubapply.py", "p151_helper_168")
P166 = helper("r149/p166_pub49f_apply.py", "p166_helper_168")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D, APPLIER = H.D, H.APPLIER
REC_REL = D + APPLIER + "/GOLD49F_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_GOLD_LISTING_GRANT_CODE_UPDATE_FIRST_WRITE.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_49F_REPORTING_GOLD_LISTING_GRANT_CODE_UPDATE_FIRST_WRITE_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_REPORTING_GOLD_LISTING_GRANT_CODE_UPDATE_FIRST_WRITE_CTO_HALF.md"
PACKET_SHA = "d2c27ac2bdc591f38e8b59b4c5d6fd6039a95e4e1906e2b124881be8365d7b16"
BUILD_B64 = "JNTOivgNaJ8spRxoXSkXAYWhf1cLqXr350sTpH5ADg4="
BEFORE_CODE = "jz6fRzL52EaI+3ZBI5cWHuDuGwiBDM/S5DPX/CmjeaM="
BEFORE_VERSION = "My0rI3fwtMCZYPDLqRhPgJ7QH9HrE8L3"
LEDGER_SLUG = "irpt-dashbd-49f-reporting-gold-listing-codeupdate-20261016"
PUBLISH_LEDGER = "irpt-dashbd-49f-reporting-publish-codeupdate-20261016"
FUNCTION, ROLE, POLICY = "irpt-49f-reporting-gold-lambda", "irpt-49f-reporting-gold-role", "irpt-49f-reporting-gold-policy"
SCHEDULE, CRON, ZONE = "irpt-49f-reporting-gold-daily", "cron(41 7 ? * MON-FRI *)", "America/New_York"
SIDS = sorted(["ListExactlyTheDeclaredSilverPrefixes", "ReadDeclaredSilverPartitionsOnly", "ListExactlyTheSixGoldPrefixes", "ReadTheSixGoldPrefixesOnly", "WriteTheFiveGoldPrefixesOnly", "ReadTheServedModelSeriesObjectOnly",
               "ListExactlyTheHouseholdCrosswalkPrefix", "ReadTheHouseholdCrosswalkOnly", "ReadTheClassTableByKeyOnly", "OwnLogStreamOnly", "InvokeOwnFunctionOnly"])
LIST_SID = "ListExactlyTheSixGoldPrefixes"
FILLED_PATTERN = "irpt/49financial/gold/filled_report_values/*"
ARTIFACT_BUCKET, ARTIFACT_KEY = "opal-313476888478-lambda-artifacts", "investor-reporting/irpt-reporting-gold-lambda.zip"
BUCKET = "opal-data-49financial"
DAY = "2026-10-15"
EARLIEST = "2024-07-08"
MEM_LINE, DUR_LINE = 6553, 720000
LAYER = "irpt-performance-native-layer"
MAX_SILVER_ONLY = 20  # PARTIAL accounts whose first GOLD row is after the floor but whose first SILVER row is on it (the producer labels from silver first_seen)
LATE_COLS = ("total_return_daily", "return_basis", "day_quality", "holdings_price_return", "holdings_price_return_reason", "guard_state")  # the columns that depend on inputs arriving after the first fire (CTO addendum 1)
OTHER_TABLES = ["account_class_daily", "account_activity_daily", "account_lot_realized", "account_lot_unrealized_daily"]
HEX12 = H.HEX12
digit_runs = H.digit_runs
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("request_ids", "flow_columns_sha256")


def b64_of_hex(h):
    return base64.b64encode(bytes.fromhex(h)).decode("ascii")


def in_window(utc, lo, hi):
    t = dt.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
    return t.weekday() < 5 and lo <= t.strftime("%H:%M") < hi


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_head(rec, packet_blob, coo_text, cto_text, ledger_exists, publish_ledger_closed=True):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "build", "plan", "apply_finished_utc", "after", "first_write", "backfill", "flips", "republish", "ledger_closed", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    g = rec["gates"]
    keys = {"packet_blob", "packet_sha256", "coo_half_signed", "cto_half_signed", "pin_is_ancestor", "one_change_at_a_time", "live_matches_packet"}
    need(isinstance(g, dict) and set(g) == keys, "gates keys")
    need(g["packet_blob"] == packet_blob and g["packet_sha256"] == PACKET_SHA, "the packet's blob or sha256 differs from the signed one")
    need(g["coo_half_signed"] is True and "SIGNED" in coo_text and PACKET_SHA in coo_text, "the COO half does not read SIGNED at the packet's sha256")
    need(g["cto_half_signed"] is True and "SIGNED" in cto_text and PACKET_SHA[:12] in cto_text, "the CTO half does not read SIGNED at the packet's sha256")
    need(g["pin_is_ancestor"] is True and g["live_matches_packet"] is True, "pin ancestry and live-state gates must be recorded true")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and is_int(oc["worktrees_read"]) and oc["worktrees_read"] >= 1 and oc["open_markers_naming_this_surface"] == 0, "one_change_at_a_time: the denominator and zero markers")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists, "the ledger entry %s must exist" % LEDGER_SLUG)
    need(rec["applier"] == APPLIER, "the applier must be named: %s" % APPLIER)
    b = rec["before"]
    need(isinstance(b, dict) and set(b) == {"function_code_sha256", "artifact_version_id", "policy", "list_prefixes", "schedule", "filled_partitions", "newest_returns_day"}, "before keys")
    need(b["function_code_sha256"] == BEFORE_CODE and b["artifact_version_id"] == BEFORE_VERSION, "before: the live code hash and artifact version of the packet's section 3")
    need(isinstance(b["policy"], dict) and sorted(b["policy"]) == SIDS and all(re.fullmatch(r"[0-9a-f]{64}", str(v)) for v in b["policy"].values()), "before.policy: sha256 of each of the eleven statements")
    need(isinstance(b["list_prefixes"], list) and b["list_prefixes"] and FILLED_PATTERN not in b["list_prefixes"], "before.list_prefixes: the list statement's patterns, without the filled one")
    need(b["schedule"] == {"state": "ENABLED", "cron": CRON} and b["filled_partitions"] == [] and b["newest_returns_day"] == DAY, "before: schedule ENABLED, 0 filled partitions, newest returns day %s" % DAY)
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == b64_of_hex(bd["zip_sha256"]) == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s" % BUILD_B64)
    need(isinstance(bd["members"], list) and "handler.py" in bd["members"] and len(bd["members"]) >= 10, "the zip must hold the handler and its staged members")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["landed_version_id"] != BEFORE_VERSION and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "import smoke, a NEW landed version or built-equals-landed")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "change_addresses", "function_change_attributes", "policy_added_values", "policy_other_changes", "replan_no_changes"}, "plan keys")
    strip = lambda a: re.sub(r"^module\.[^.]+\.", "", str(a))  # noqa: E731
    need(p["add"] == 0 and p["change"] == 2 and p["destroy"] == 0 and sorted(strip(a) for a in p["change_addresses"]) == sorted(["aws_iam_role_policy.irpt_reporting_gold", "aws_lambda_function.this"]) and p["replan_no_changes"] is True,
         "the plan must read 0 add / 2 change / 0 destroy on the policy and the function and a post-apply plan of No changes")
    need(p["policy_added_values"] == [FILLED_PATTERN] and p["policy_other_changes"] == 0, "the policy change must be the ONE s3:prefix value %s and nothing else (the CTO's condition 4)" % FILLED_PATTERN)
    fa = p["function_change_attributes"]
    need(isinstance(fa, list) and fa and set(fa) <= {"source_code_hash", "s3_object_version", "s3_key", "s3_bucket", "last_modified", "qualified_arn", "qualified_invoke_arn", "version", "source_code_size"}, "the function change must be by CODE attributes only: %s" % fa)
    t = rec["apply_finished_utc"]
    need(H.UTC.match(str(t)) and not in_window(t, "11:35", "12:00"), "the apply must be outside 11:35Z to 12:00Z on a trading weekday (the CTO's condition 5)")
    return True


def check_report(rp, label):
    need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"}, "%s: report keys" % label)
    need(is_int(rp["max_memory_used_mb"]) and rp["max_memory_used_mb"] <= MEM_LINE and rp["memory_size_mb"] == 8192 and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] <= DUR_LINE,
         "%s: Max Memory Used at most %d MB and duration at most %d ms (the CTO's branch-C line)" % (label, MEM_LINE, DUR_LINE))


def check_tail(rec):
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy", "list_prefixes", "schedule"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 8192 and f.get("timeout") == 900 and f.get("reserved_concurrency") is None and f.get("code_sha256") == rec["build"]["zip_sha256_b64"] and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"],
         "after.function: memory 8192, timeout 900, NO reserved concurrency, the landed zip's code hash, the native layer")
    b = rec["before"]
    need(isinstance(a["policy"], dict) and sorted(a["policy"]) == SIDS, "after.policy: the eleven statements")
    need(all(a["policy"][s] == b["policy"][s] for s in SIDS if s != LIST_SID) and a["policy"][LIST_SID] != b["policy"][LIST_SID], "after.policy: every statement but the list statement byte-identical to before, the list statement changed")
    need(sorted(a["list_prefixes"]) == sorted(b["list_prefixes"] + [FILLED_PATTERN]), "after.list_prefixes must be before's patterns plus the filled one, nothing else")
    need(a["schedule"] == {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "after.schedule untouched")
    fw = rec["first_write"]
    need(isinstance(fw, dict) and set(fw) == {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "filled_partitions_after", "request_id"}, "first_write keys")
    need(fw["payload"] == {"day": DAY} and fw["status_code"] == 200 and fw["function_error"] is None and H.UTC.match(str(fw["invoked_utc"])) and fw["invoked_utc"] >= rec["apply_finished_utc"] and not in_window(fw["invoked_utc"], "11:35", "12:00"), "first write: {day: %s}, 200, no error, after the apply, outside the fire window" % DAY)
    r = fw["returned"]
    need(isinstance(r, dict) and r.get("day") == DAY and isinstance(r.get("result"), dict) and is_int(r["result"].get("rows")) and r["result"]["rows"] > 0 and r.get("next") is None and "failed" not in r["result"], "first write returned a positive row count for the day and no next day")
    check_report(fw["report"], "first_write")
    need(fw["filled_partitions_after"] == [DAY] and nes(fw["request_id"]), "first write: exactly the one filled partition %s afterwards" % DAY)
    bf = rec["backfill"]
    need(isinstance(bf, dict) and set(bf) == {"payload", "invoked_utc", "status_code", "function_error", "report", "before", "after", "previous_version_id", "request_id"}, "backfill keys")
    need(bf["payload"] == {"backfill": {"start": DAY, "end": DAY}, "accounts": "population"} and bf["status_code"] == 200 and bf["function_error"] is None and H.UTC.match(str(bf["invoked_utc"])) and bf["invoked_utc"] >= fw["invoked_utc"] and not in_window(bf["invoked_utc"], "11:35", "12:00"),
         "backfill: the one-day event on %s, 200, no error, after the first write, outside the fire window" % DAY)
    check_report(bf["report"], "backfill")
    bb, ba = bf["before"], bf["after"]
    need(isinstance(bb, dict) and set(bb) == {"rows", "floor_start_with_row", "flow_columns_sha256", "other_tables_rows"} and is_int(bb["rows"]) and bb["rows"] > 0 and is_int(bb["floor_start_with_row"]) and 0 < bb["floor_start_with_row"] <= bb["rows"], "backfill.before: rows and the accounts with a row whose first row is on the floor day")
    need(isinstance(ba, dict) and set(ba) == {"rows", "partial", "full", "claim_inferred", "flow_columns_sha256", "changed_columns", "other_tables_rows"}, "backfill.after keys")
    need(ba["rows"] == bb["rows"] and ba["claim_inferred"] == ba["rows"] and bb["floor_start_with_row"] <= ba["partial"] <= bb["floor_start_with_row"] + MAX_SILVER_ONLY and ba["partial"] + ba["full"] == ba["rows"], "backfill.after: same rows, the claim on every row, PARTIAL_HISTORY on the floor-start accounts (by first gold row) plus at most %d silver-first-seen accounts, the rest FULL" % MAX_SILVER_ONLY)
    need(ba["flow_columns_sha256"] == bb["flow_columns_sha256"] and re.fullmatch(r"[0-9a-f]{64}", str(ba["flow_columns_sha256"])), "backfill: market_value_eod and external_flow identical before and after (one hash; the CTO addendum 1)")
    cc = ba["changed_columns"]
    need(isinstance(cc, dict) and set(cc) <= set(LATE_COLS) and all(is_int(v) and 0 < v <= ba["rows"] for v in cc.values()), "backfill.after.changed_columns: only the late-input columns, each with a row count: %s" % (sorted(cc) if isinstance(cc, dict) else cc))
    need(nes(bf.get("previous_version_id")), "backfill.previous_version_id: the version the day held before the event")
    need(isinstance(bb["other_tables_rows"], dict) and sorted(bb["other_tables_rows"]) == sorted(OTHER_TABLES) and ba["other_tables_rows"] == bb["other_tables_rows"], "backfill: the other tables' row counts for the day unchanged")
    need(nes(bf["request_id"]), "backfill.request_id")
    fl = rec["flips"]
    need(isinstance(fl, dict) and set(fl) == {"full_to_partial", "partial_to_full", "unchanged", "floor_account_flips", "served_before_full"} and all(is_int(fl[k]) for k in fl), "flips keys: counts only")
    need(fl["served_before_full"] == 0 and fl["full_to_partial"] == 0 and fl["floor_account_flips"] == 0, "Act 5 stops only on a FULL to PARTIAL flip or a PARTIAL to FULL flip of an account whose first row is on or before the floor; the served series read PARTIAL_HISTORY before (the CTO addendum 1)")
    need(fl["partial_to_full"] == ba["full"] and fl["unchanged"] == ba["partial"], "flips: PARTIAL to FULL equals the FULL rows and unchanged equals the PARTIAL rows of the day")
    rp = rec["republish"]
    ck = {"payload", "invoked_utc", "status_code", "function_error", "returned", "shard_reports", "published", "refused", "objects_after", "pair_count", "partial_with_pair", "no_claim_count", "request_ids"}
    need(isinstance(rp, dict) and set(rp) == ck, "republish keys differ")
    need(rp["payload"] == {} and rp["status_code"] == 200 and rp["function_error"] is None and H.UTC.match(str(rp["invoked_utc"])) and rp["invoked_utc"] >= bf["invoked_utc"] and not in_window(rp["invoked_utc"], "12:05", "13:00"), "republish: payload {}, 200, no error, after the backfill, outside 12:05Z to 13:00Z")
    need(isinstance(rp["returned"], dict) and rp["returned"].get("ok") is True and rp["returned"].get("fanned_out") == 7, "republish: the 7-shard fan-out answer")
    need(isinstance(rp["shard_reports"], list) and len(rp["shard_reports"]) == 7, "republish: exactly 7 shard REPORT lines")
    for i, x in enumerate(rp["shard_reports"]):
        P166.check_report(x, "republish shard %d" % i)
    n = rp["published"]
    need(is_int(n) and n >= 6949 and rp["refused"] == 0 and n == rp["returned"].get("accounts"), "republish: published equals the fan-out's account count, at least 6,949, 0 refused")
    need(rp["objects_after"] == {"series": n, "manifest": n}, "republish: series and manifests equal published")
    need(rp["pair_count"] == bb["rows"] and rp["partial_with_pair"] == ba["partial"] and rp["no_claim_count"] == n - bb["rows"], "republish: the series with the pair equal the accounts with a row on the day, the PARTIAL_HISTORY ones equal Act 4's PARTIAL count, the rest carry no claim")
    need(isinstance(rp["request_ids"], list) and rp["request_ids"], "republish: request ids")
    need(rec["ledger_closed"] is False and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "the ledger must stay OPEN; reads block")
    scan = copy.deepcopy(rec)
    scan["before"].pop("policy", None)  # statement hashes: hex by construction
    scan["after"].pop("policy", None)
    need(not digit_runs(scan), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(scan)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def stmt_hash(st):
    return hashlib.sha256(json.dumps(st, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def read_day(s3, table_prefix, day, columns=None):
    import pyarrow.parquet as pq
    keys = [o["Key"] for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="%sdate=%s/" % (table_prefix, day)) for o in p.get("Contents", []) if o["Key"].endswith(".parquet")]
    need(keys, "no parquet under %sdate=%s/" % (table_prefix, day))
    tabs = [pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()), columns=columns) for k in keys]
    return tabs


def table_prefix(root, table):
    sys.path.insert(0, str(Path(root) / "lib"))
    import opal_naming
    probe = opal_naming.address("irpt", "49financial", "gold", table, "date=0000-00-00", "data.parquet")
    return probe[len("s3://"):].partition("/")[2].rsplit("/date=", 1)[0] + "/"


def live(root):
    import boto3
    lam, iam, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam"), boto3.client("s3")
    sch = boto3.client("scheduler", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    try:
        conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    except Exception:  # noqa: BLE001
        conc = None
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    pol = {x["Sid"]: stmt_hash(x) for x in sts}
    lst = next(x for x in sts if x["Sid"] == LIST_SID)
    vals = lst["Condition"]["StringLike"]["s3:prefix"]
    vals = vals if isinstance(vals, list) else [vals]
    sc = sch.get_schedule(Name=SCHEDULE)
    ver = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)
    return {"cfg": cfg, "conc": conc, "policy": pol, "list_prefixes": sorted(vals), "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")},
            "artifact_version": ver.get("VersionId"), "s3": s3}


def flow_hash(tab):
    cols = ["account_id", "market_value_eod", "external_flow"]
    rows = sorted(zip(*[tab[c].to_pylist() for c in cols]), key=lambda r: str(r[0]))
    return hashlib.sha256(json.dumps(rows, default=str, separators=(",", ":")).encode("utf-8")).hexdigest()


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    packet_blob = H.git(root, "hash-object", PACKET_REL).strip()
    need(hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest() == PACKET_SHA, "the packet's bytes differ from the signed sha256")
    need((root / CTO_HALF_REL).is_file(), "no CTO half")
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8")
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8")
    ledger_exists = bool(list((root / "org/critical_paths/change_management").glob("*%s*" % LEDGER_SLUG)))
    check_head(rec, packet_blob, coo, cto, ledger_exists)
    if cid == "DBC168-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time), ledger %s, applier named, build %s equals the packet's and landed as a NEW version, plan 0 add / 2 change / 0 destroy on the policy and the function, the policy change the ONE s3:prefix value, the apply outside the fire window" % (LEDGER_SLUG, rec["build"]["zip_sha256"][:12]))
        return True
    check_tail(rec)
    lv = live(root)
    s3 = lv["s3"]
    cfg = lv["cfg"]
    if cid == "DBC168-2-AC1":
        need(cfg["MemorySize"] == 8192 and cfg["Timeout"] == 900 and cfg["Handler"] == "handler.lambda_handler" and cfg["Runtime"] == "python3.12" and cfg["Role"].endswith("role/" + ROLE) and lv["conc"] is None and not (cfg.get("Environment") or {}).get("Variables"), "live function: memory/timeout/handler/runtime/role, no concurrency, no environment")
        need(cfg["CodeSha256"] == rec["build"]["zip_sha256_b64"] != BEFORE_CODE and [x["Arn"] for x in cfg.get("Layers", [])] == [rec["after"]["function"]["layer_arn"]], "live CodeSha256 must equal the landed zip's, differ from the old, and the one layer unchanged")
        need(lv["policy"] == rec["after"]["policy"] and sorted(lv["list_prefixes"]) == sorted(rec["after"]["list_prefixes"]), "live role policy: the eleven statements and the list patterns must equal the record's after-read (the one added pattern)")
        need(lv["schedule"] == {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "the schedule must be ENABLED, untouched")
        need(nes(lv["artifact_version"]) and lv["artifact_version"] == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
        fp = table_prefix(root, "filled_report_values")
        parts = sorted(c["Prefix"][len(fp):].strip("/") for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=fp, Delimiter="/") for c in p.get("CommonPrefixes", []))
        need(DAY in [x[len("date="):] for x in parts if x.startswith("date=")] and rec["first_write"]["filled_partitions_after"] == [DAY], "the filled prefix must hold the %s partition (hop 1's first write)" % DAY)
        tabs = read_day(s3, fp, DAY)
        need(sum(t.num_rows for t in tabs) == rec["first_write"]["returned"]["result"]["rows"] > 0, "the filled partition's rows differ from the event's answer")
        print("OK: live: the function runs the NEW code; the role policy holds the eleven statements with the list statement gaining exactly %s; the schedule is untouched; the artifact's current version is the recorded one; the filled prefix holds the %s partition with the rows the event answered (hop 1's first write)" % (FILLED_PATTERN, DAY))
        return True
    if cid == "DBC168-3-AC1":
        rp = table_prefix(root, "account_return_daily")
        tabs = read_day(s3, rp, DAY)
        import pyarrow as pa
        tab = pa.concat_tables(tabs) if len(tabs) > 1 else tabs[0]
        bf = rec["backfill"]
        need(tab.num_rows == bf["after"]["rows"] and "history_scope_claim" in tab.column_names, "the day's returns partition: %d rows (record %d), claim column %s" % (tab.num_rows, bf["after"]["rows"], "history_scope_claim" in tab.column_names))
        cl, hs = tab["history_scope_claim"].to_pylist(), tab["history_scope"].to_pylist()
        need(all(x == "inferred" for x in cl), "every row of the rewritten day must carry history_scope_claim = inferred")
        need(hs.count("PARTIAL_HISTORY") == bf["after"]["partial"] and hs.count("FULL") == bf["after"]["full"], "PARTIAL_HISTORY and FULL counts differ from the record")
        key = [k for k in [o["Key"] for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="%sdate=%s/" % (rp, DAY)) for o in p.get("Contents", [])] if k.endswith(".parquet")][0]
        vers = sorted([v for p in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=key) for v in p.get("Versions", []) if v["Key"] == key], key=lambda v: v["LastModified"])
        need(len(vers) >= 2 and vers[0]["VersionId"] == bf["previous_version_id"], "the day's data.parquet must hold its previous version (the recorded one) beside the new one")
        import io as _io
        import pyarrow.parquet as pq
        old = pq.read_table(_io.BytesIO(s3.get_object(Bucket=BUCKET, Key=key, VersionId=vers[0]["VersionId"])["Body"].read()))
        need(flow_hash(tab) == flow_hash(old) == bf["after"]["flow_columns_sha256"], "market_value_eod and external_flow of the rewritten day differ from the previous version or the record")
        oi = {a: i for i, a in enumerate(old["account_id"].to_pylist())}
        need(set(oi) == set(tab["account_id"].to_pylist()), "the rewritten day holds a different account set than its previous version")
        chg = {}
        for c in old.column_names:
            if c in ("history_scope", "history_scope_claim"):
                continue
            ov, nv = old[c].to_pylist(), tab[c].to_pylist()
            n_chg = sum(1 for j, a in enumerate(tab["account_id"].to_pylist()) if ov[oi[a]] != nv[j])
            if n_chg:
                chg[c] = n_chg
        need(chg == bf["after"]["changed_columns"] and set(chg) <= set(LATE_COLS), "columns changed against the previous version: live %s, record %s (allowed: %s)" % (chg, bf["after"]["changed_columns"], list(LATE_COLS)))
        first = {}
        days = sorted({k.split("date=")[1][:10] for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=rp) for k in [o["Key"] for o in p.get("Contents", [])] if "date=" in k})

        def one(d):
            return d, [t.select(["account_id"]).to_pylist() for t in read_day(s3, rp, d)]
        with ThreadPoolExecutor(max_workers=12) as pool:
            for d, tl in pool.map(one, days):
                for rows in tl:
                    for r in rows:
                        a = str(r["account_id"])
                        if a not in first:
                            first[a] = d
        accts = [str(x) for x in tab["account_id"].to_pylist()]
        floor_with_row = sum(1 for a in set(accts) if first.get(a) == days[0])
        silver_only = bf["after"]["partial"] - floor_with_row
        need(days[0] == EARLIEST and floor_with_row == bf["before"]["floor_start_with_row"] and 0 <= silver_only <= MAX_SILVER_ONLY, "the accounts with a row on %s whose first gold row is on the floor day: live %d, record %d; PARTIAL rows %d, so %d account(s) are PARTIAL by silver first_seen only (at most %d)" % (DAY, floor_with_row, bf["before"]["floor_start_with_row"], bf["after"]["partial"], silver_only, MAX_SILVER_ONLY))
        partial_accts = {str(a) for a, s in zip(tab["account_id"].to_pylist(), hs) if s == "PARTIAL_HISTORY"}
        need(len([a for a in partial_accts if first.get(a) != days[0]]) == silver_only, "the PARTIAL accounts outside the first-gold-row set must number exactly the difference")
        need(all((first.get(a) != days[0]) or (a in partial_accts) for a in set(accts)), "an account whose first gold row is on the floor day reads FULL")
        for t in OTHER_TABLES:
            tb = pa.concat_tables(read_day(s3, table_prefix(root, t), DAY)) if len(read_day(s3, table_prefix(root, t), DAY)) > 1 else read_day(s3, table_prefix(root, t), DAY)[0]
            need(tb.num_rows == bf["after"]["other_tables_rows"][t], "the %s day partition holds %d rows; the record says %d" % (t, tb.num_rows, bf["after"]["other_tables_rows"][t]))
        # the series
        import gzip as gz
        pre = "irpt/49financial/platinum/reporting/"
        keys = sorted(o["Key"] for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=pre) for o in p.get("Contents", []) if o["Key"].endswith("/series.json.gz"))
        n = rec["republish"]["published"]
        need(len(keys) == n, "the prefix holds %d series; published %d" % (len(keys), n))

        def readseries(k):
            return json.loads(gz.decompress(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()).decode("utf-8"))
        pair = partial = 0
        with ThreadPoolExecutor(max_workers=12) as pool:
            for s in pool.map(readseries, keys):
                if s.get("history_scope_claim") == "inferred" and s.get("history_scope_basis") == "first value day vs source floor":
                    pair += 1
                    partial += 1 if s["history_scope"] == "PARTIAL_HISTORY" else 0
                else:
                    need("history_scope_claim" not in s and "history_scope_basis" not in s, "a series carries one of the history-scope pair without the other or with another word")
        need(pair == rec["republish"]["pair_count"] == bf["after"]["rows"] and partial == rec["republish"]["partial_with_pair"] == bf["after"]["partial"] and n - pair == rec["republish"]["no_claim_count"], "series with the pair %d (record %d), PARTIAL among them %d (record %d)" % (pair, rec["republish"]["pair_count"], partial, rec["republish"]["partial_with_pair"]))
        need((root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file(), "the ledger's open marker is missing: the ledger must stay OPEN")
        need(not (root / "org/critical_paths/.open_deploys" / (PUBLISH_LEDGER + ".json")).is_file(), "the publish pair's ledger %s must read CLOSED before Act 5 (the CTO's condition 2)" % PUBLISH_LEDGER)
        print("OK: the day's returns partition holds %d rows with the claim on every row, %d PARTIAL_HISTORY (every account whose first gold row is on the floor day, plus the silver first-seen accounts the gold cannot show, at most 20, recomputed from the gold) and %d FULL, market_value_eod and external_flow identical to the previous version and only the late-input columns changed (counts equal the record's), the other four tables' day row counts unchanged; %d of %d series carry the pair (%d PARTIAL), the rest none; the publish ledger is closed and this ledger stays open" % (tab.num_rows, hs.count("PARTIAL_HISTORY"), hs.count("FULL"), pair, n, partial))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    zh = "cd" * 32
    global BUILD_B64, PACKET_SHA
    saved = (BUILD_B64, PACKET_SHA)
    BUILD_B64, PACKET_SHA = b64_of_hex(zh), "ee" * 32
    try:
        rp = {"max_memory_used_mb": 3000, "duration_ms": 300000.0, "memory_size_mb": 8192}
        shard = {"max_memory_used_mb": 400, "duration_ms": 9000.0, "memory_size_mb": 1024}
        pol_b = {s: ("%02x" % i) * 32 for i, s in enumerate(SIDS)}
        pol_a = dict(pol_b)
        pol_a[LIST_SID] = "ff" * 32
        lp = ["irpt/49financial/gold/a/*", "irpt/49financial/gold/b/*"]
        good = {"claim": "measured", "gates": {"packet_blob": "b" * 40, "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
                                               "one_change_at_a_time": {"worktrees_read": 5, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
                "ledger_entry": LEDGER_SLUG, "applier": APPLIER,
                "before": {"function_code_sha256": BEFORE_CODE, "artifact_version_id": BEFORE_VERSION, "policy": pol_b, "list_prefixes": lp, "schedule": {"state": "ENABLED", "cron": CRON}, "filled_partitions": [], "newest_returns_day": DAY},
                "build": {"zip_sha256": zh, "zip_sha256_b64": b64_of_hex(zh), "members": ["handler.py"] + ["m%d" % i for i in range(12)], "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": zh, "built_equals_landed": True},
                "plan": {"add": 0, "change": 2, "destroy": 0, "change_addresses": ["aws_iam_role_policy.irpt_reporting_gold", "module.x.aws_lambda_function.this"], "function_change_attributes": ["source_code_hash", "s3_object_version"],
                         "policy_added_values": [FILLED_PATTERN], "policy_other_changes": 0, "replan_no_changes": True},
                "apply_finished_utc": "2026-10-16T14:10:00Z",
                "after": {"function": {"memory": 8192, "timeout": 900, "reserved_concurrency": None, "code_sha256": b64_of_hex(zh), "layer_arn": "arn:aws:lambda:us-east-1:1:layer:%s:1" % LAYER}, "policy": pol_a,
                          "list_prefixes": lp + [FILLED_PATTERN], "schedule": {"state": "ENABLED", "cron": CRON, "zone": ZONE}},
                "first_write": {"payload": {"day": DAY}, "invoked_utc": "2026-10-16T14:15:00Z", "status_code": 200, "function_error": None, "returned": {"day": DAY, "result": {"day": DAY, "rows": 6900}, "next": None},
                                "report": rp, "filled_partitions_after": [DAY], "request_id": "r1"},
                "backfill": {"payload": {"backfill": {"start": DAY, "end": DAY}, "accounts": "population"}, "invoked_utc": "2026-10-16T14:25:00Z", "status_code": 200, "function_error": None, "report": rp,
                             "before": {"rows": 6946, "floor_start_with_row": 2849, "flow_columns_sha256": "ab" * 32, "other_tables_rows": {t: 100 for t in OTHER_TABLES}},
                             "after": {"rows": 6946, "partial": 2849, "full": 4097, "claim_inferred": 6946, "flow_columns_sha256": "ab" * 32, "changed_columns": {"guard_state": 6700, "holdings_price_return": 6700}, "other_tables_rows": {t: 100 for t in OTHER_TABLES}}, "previous_version_id": "pv1", "request_id": "r2"},
                "flips": {"full_to_partial": 0, "partial_to_full": 4097, "unchanged": 2849, "floor_account_flips": 0, "served_before_full": 0},
                "republish": {"payload": {}, "invoked_utc": "2026-10-16T14:35:00Z", "status_code": 200, "function_error": None, "returned": {"ok": True, "accounts": 6949, "fanned_out": 7}, "shard_reports": [dict(shard) for _ in range(7)],
                              "published": 6949, "refused": 0, "objects_after": {"series": 6949, "manifest": 6949}, "pair_count": 6946, "partial_with_pair": 2849, "no_claim_count": 3, "request_ids": ["r3"]},
                "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
        blob, ok_text = "b" * 40, ("SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12])
        assert check_head(good, blob, ok_text[0], ok_text[1], True) and check_tail(good)
        arms = (("claim", lambda r: r.update(claim="inferred")), ("cto", lambda r: r["gates"].update(cto_half_signed=False)), ("applier", lambda r: r.update(applier="x")), ("before code", lambda r: r["before"].update(function_code_sha256="z")),
                ("before filled", lambda r: r["before"].update(filled_partitions=[DAY])), ("before list has filled", lambda r: r["before"].update(list_prefixes=lp + [FILLED_PATTERN])), ("build hash", lambda r: r["build"].update(zip_sha256_b64="x")),
                ("same version", lambda r: r["build"].update(landed_version_id=BEFORE_VERSION)), ("plan add", lambda r: r["plan"].update(add=1)), ("plan change", lambda r: r["plan"].update(change=1)), ("plan destroy", lambda r: r["plan"].update(destroy=1)),
                ("plan addr", lambda r: r["plan"].update(change_addresses=["x.aws_iam_role.y", "module.x.aws_lambda_function.this"])), ("plan values", lambda r: r["plan"].update(policy_added_values=["other/*"])),
                ("plan other policy", lambda r: r["plan"].update(policy_other_changes=1)), ("plan attrs", lambda r: r["plan"].update(function_change_attributes=["memory_size"])), ("replan", lambda r: r["plan"].update(replan_no_changes=False)),
                ("apply in window", lambda r: r.update(apply_finished_utc="2026-10-16T11:50:00Z")), ("memory", lambda r: r["after"]["function"].update(memory=3008)), ("policy other changed", lambda r: r["after"]["policy"].update({SIDS[0]: "11" * 32})),
                ("policy list unchanged", lambda r: r["after"]["policy"].update({LIST_SID: pol_b[LIST_SID]})), ("list values", lambda r: r["after"].update(list_prefixes=lp)), ("schedule", lambda r: r["after"]["schedule"].update(state="DISABLED")),
                ("fw payload", lambda r: r["first_write"].update(payload={"day": "2026-10-14"})), ("fw rows", lambda r: r["first_write"]["returned"]["result"].update(rows=0)), ("fw next", lambda r: r["first_write"]["returned"].update(next="2026-10-16")),
                ("fw memory line", lambda r: r["first_write"]["report"].update(max_memory_used_mb=7000)), ("fw partitions", lambda r: r["first_write"].update(filled_partitions_after=[DAY, "2026-10-14"])),
                ("bf payload", lambda r: r["backfill"].update(payload={"backfill": {"start": "2026-10-14", "end": DAY}, "accounts": "population"})), ("bf rows", lambda r: r["backfill"]["after"].update(rows=6900)),
                ("bf claim", lambda r: r["backfill"]["after"].update(claim_inferred=6000)), ("bf partial", lambda r: r["backfill"]["after"].update(partial=2000, full=4946)), ("bf flows", lambda r: r["backfill"]["after"].update(flow_columns_sha256="cd" * 32)), ("bf changed col", lambda r: r["backfill"]["after"]["changed_columns"].update(market_value_eod=5)), ("bf changed empty count", lambda r: r["backfill"]["after"]["changed_columns"].update(guard_state=0)), ("bf prev", lambda r: r["backfill"].update(previous_version_id="")),
                ("bf other tables", lambda r: r["backfill"]["after"]["other_tables_rows"].update({OTHER_TABLES[0]: 5})), ("flip f2p", lambda r: r["flips"].update(full_to_partial=1)), ("flip floor account", lambda r: r["flips"].update(floor_account_flips=1)), ("flip served full", lambda r: r["flips"].update(served_before_full=2)), ("flip p2f sum", lambda r: r["flips"].update(partial_to_full=4000)), ("flip unchanged", lambda r: r["flips"].update(unchanged=2000)), ("rp payload", lambda r: r["republish"].update(payload={"summaries": True})),
                ("rp shards", lambda r: r["republish"]["shard_reports"].pop()), ("rp refused", lambda r: r["republish"].update(refused=1)), ("rp pair", lambda r: r["republish"].update(pair_count=6000)), ("rp partial", lambda r: r["republish"].update(partial_with_pair=1)),
                ("rp in window", lambda r: r["republish"].update(invoked_utc="2026-10-16T12:30:00Z")), ("ledger", lambda r: r.update(ledger_closed=True)), ("extra", lambda r: r.update(z=1)))
        for label, fn in arms:
            r2 = copy.deepcopy(good)
            fn(r2)
            try:
                check_head(r2, blob, ok_text[0], ok_text[1], True)
                check_tail(r2)
            except Fail:
                continue
            raise AssertionError("red arm passed: " + label)
        red(lambda: check_head(good, blob, ok_text[0], ok_text[1], False), "no ledger")
        red(lambda: check_head(good, blob, "UNSIGNED", ok_text[1], True), "coo half")
        assert in_window("2026-10-16T11:50:00Z", "11:35", "12:00") and not in_window("2026-10-17T11:50:00Z", "11:35", "12:00")
    finally:
        BUILD_B64, PACKET_SHA = saved
    print("selftest: record clauses behave on a green arm and %d red arms (plus two head arms and the window rule)" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
