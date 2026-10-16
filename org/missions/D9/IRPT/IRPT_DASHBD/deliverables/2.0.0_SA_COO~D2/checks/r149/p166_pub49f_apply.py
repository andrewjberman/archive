"""IRPT_DASHBD round 149, workstream PUB49FAPPLY (issuer 2.0.0_SA_COO~D2) -- DB-b-298, the APPLY of the signed never-widen pair for the 49 Financial series publish (packet sha256 29b7df738efc, COO half signed
@023604d076, CTO half signed @582155d0b7): a NEW artifact version, ONE safe-apply (plan exactly 0 add / 1 change / 0 destroy: the function's CODE), the CTO's absent-days check, a one-shard DRY RUN, a ONE-ACCOUNT
republish and the FULL republish of the 6,949 series (7 shard invocations). WORLD. The record is the applier's; the checker re-reads the world.

  DBC166-1-AC1  the record's head: packet and halves, gates, ledger and applier, before, build, plan, the time rule
  DBC166-2-AC1  FRESH live reads: the function's code, the execution policy, the schedule (ENABLED, untouched), the artifact version
  DBC166-3-AC1  the absent-days check, the dry run, the canary and the full republish in the record, and FRESH reads of the prefix: every series and manifest, samples, prior versions, the REPORT lines, the open ledger

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import base64
import copy
import datetime as dt
import gzip
import hashlib
import importlib.util
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def p151():
    spec = importlib.util.spec_from_file_location("p151_helper_166", str(HERE.parent / "r147" / "p151_pubapply.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["p151_helper_166"] = mod
    spec.loader.exec_module(mod)
    return mod


H = p151()
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D, APPLIER = H.D, H.APPLIER
REC_REL = D + APPLIER + "/PUB49F_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_REPORTING_PUBLISH_CODE_UPDATE_REPUBLISH_CTO_HALF.md"
PACKET_SHA = "29b7df738efcc7b070fde732fc34f88c77a75ea034e1d107545fc789292b5449"
BUILD_B64 = "SX0xYFZsxH4q6psJM56yAee9wRb6vrVUN4VrTV1ouU8="
BEFORE_CODE = "AH5r60vpxR/Gt4RlpsSkhAw5HDths5P2Ht+Ix1CHlQ8="
BEFORE_VERSION = "4kEV9O.UMGs.NSGSYi_N4ZZjNm45rso4"
LEDGER_SLUG = "irpt-dashbd-49f-reporting-publish-codeupdate-20261016"
FUNCTION, ROLE, POLICY = "irpt-49f-reporting-publish-lambda", "irpt-49f-reporting-publish-role", "irpt-49f-reporting-publish-policy"
SCHEDULE, CRON, ZONE = "irpt-49f-reporting-publish-daily", "cron(15 8 ? * MON-FRI *)", "America/New_York"
EXEC_SIDS = sorted(["ListExactlyTheDeclaredGoldPrefixes", "ReadDeclaredGoldPartitionsOnly", "WriteThePlatinumReportingPrefixOnly", "ReadBackThePlatinumReportingPrefixOnly", "ListThePlatinumReportingPrefixForSummaries",
                    "ReadTheFirmDirectoryObjectsOnly", "InvokeOwnFunctionForShardFanOut", "OwnLogStreamOnly"])
ARTIFACT_BUCKET, ARTIFACT_KEY = "opal-313476888478-lambda-artifacts", "investor-reporting/irpt-reporting-publish-lambda.zip"
BUCKET, PREFIX, GOLD_PREFIX = "opal-data-49financial", "irpt/49financial/platinum/reporting/", "irpt/49financial/gold/account_return_daily/"
LOG_GROUP = "/aws/lambda/" + FUNCTION
LAYER = "irpt-performance-native-layer"
CAL_VALUES = ["pandas_market_calendars", "fallback_2010_2027"]
BASIS = "trading calendar minus present partitions"
CHECKS = ["series_size_equals_manifest", "validates_contract", "pair_present", "basis_const", "unreported_equals_absent_dates_in_window", "no_income_claim", "calendar_source_in_values", "manifest_firm_ok", "prior_versions_kept"]
MEM_LINE, DUR_LINE = 819, 240000
SHARDS = 7
HEX12 = H.HEX12
digit_runs = H.digit_runs
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("before", "dates", "range", "request_ids")


def b64_of_hex(h):
    return base64.b64encode(bytes.fromhex(h)).decode("ascii")


def in_fire_window(utc):
    """True when the instant is inside 12:05Z to 13:00Z (the daily fire and its summaries pass) on a Monday to Friday."""
    t = dt.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
    return t.weekday() < 5 and "12:05" <= t.strftime("%H:%M") < "13:00"


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_head(rec, packet_blob, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "build", "plan", "apply_finished_utc", "after", "absent_days", "dry_run", "canary", "full", "ledger_closed", "reads"}
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
    need(isinstance(b, dict) and set(b) == {"function_code_sha256", "artifact_version_id", "schedule", "objects"}, "before keys")
    need(b["function_code_sha256"] == BEFORE_CODE and b["artifact_version_id"] == BEFORE_VERSION, "before: the live code hash and artifact version of the packet's section 3")
    need(b["schedule"] == {"state": "ENABLED", "cron": CRON}, "before: the schedule ENABLED at %s" % CRON)
    ob = b["objects"]
    need(isinstance(ob, dict) and set(ob) == {"series", "manifest", "other"} and all(is_int(ob[k]) for k in ob) and ob["series"] >= 6949 and ob["manifest"] >= 6949 and ob["other"] >= 4344, "before.objects: at least the packet's 6,949 / 6,949 / 4,344")
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == b64_of_hex(bd["zip_sha256"]) == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s" % BUILD_B64)
    need(isinstance(bd["members"], list) and len(bd["members"]) >= 17 and "handler.py" in bd["members"] and "lib/trading_calendar.py" in bd["members"], "the zip must hold the handler, the calendar and the entry's other members (17)")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["landed_version_id"] != BEFORE_VERSION and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "import smoke, a NEW landed version or built-equals-landed")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "change_addresses", "function_change_attributes", "replan_no_changes"}, "plan keys")
    strip = lambda a: re.sub(r"^module\.[^.]+\.", "", str(a))  # noqa: E731
    need(p["add"] == 0 and p["change"] == 1 and p["destroy"] == 0 and [strip(a) for a in p["change_addresses"]] == ["aws_lambda_function.this"] and p["replan_no_changes"] is True, "the plan must read 0 add / 1 change / 0 destroy on aws_lambda_function.this and a post-apply plan of No changes")
    fa = p["function_change_attributes"]
    need(isinstance(fa, list) and fa and set(fa) <= {"source_code_hash", "s3_object_version", "s3_key", "s3_bucket", "last_modified", "qualified_arn", "qualified_invoke_arn", "version", "source_code_size"}, "the function change must be by CODE attributes only: %s" % fa)
    need(H.UTC.match(str(rec["apply_finished_utc"])) and rec["apply_finished_utc"] >= "2026-10-16T13:00:00Z" and not in_fire_window(rec["apply_finished_utc"]),
         "apply_finished_utc must be at or after 2026-10-16T13:00:00Z (the CTO's condition 3) and outside 12:05Z to 13:00Z on a weekday (the packet's condition 3)")
    return True


def check_report(rp, label, many=False):
    need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"}, "%s: report keys" % label)
    need(is_int(rp["max_memory_used_mb"]) and rp["max_memory_used_mb"] <= MEM_LINE and rp["memory_size_mb"] == 1024 and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] <= DUR_LINE,
         "%s: Max Memory Used at most %d MB and duration at most %d ms (the packet's line)" % (label, MEM_LINE, DUR_LINE))


def check_absent(a, rec_first, rec_last):
    need(isinstance(a, dict) and set(a) == {"range", "count", "dates", "accounts_touched", "all_nyse_trading_days"}, "absent_days keys")
    need(a["range"] == [rec_first, rec_last] and is_int(a["count"]) and a["count"] == len(a["dates"]) and a["dates"] == sorted(set(a["dates"])) and all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(x)) for x in a["dates"]), "absent_days: range, count equal to the sorted dates")
    need(is_int(a["accounts_touched"]) and a["accounts_touched"] >= 0 and a["all_nyse_trading_days"] is True and (a["count"] > 0 or a["accounts_touched"] == 0), "absent_days: accounts_touched, and every listed date a NYSE trading day (the CTO's condition 1)")
    return True


def check_tail(rec):
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy_sids", "schedule"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 300 and f.get("reserved_concurrency") is None and f.get("code_sha256") == rec["build"]["zip_sha256_b64"] and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"],
         "after.function: memory 1024, timeout 300, NO reserved concurrency, the landed zip's code hash, the native layer")
    need(sorted(a["policy_sids"]) == EXEC_SIDS, "after: the execution policy's eight statements, unchanged")
    need(a["schedule"] == {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "after.schedule must be ENABLED at the packet's cron, untouched")
    check_absent(rec["absent_days"], rec["absent_days"]["range"][0] if isinstance(rec["absent_days"], dict) else None, rec["absent_days"]["range"][1] if isinstance(rec["absent_days"], dict) else None)
    ob = rec["before"]["objects"]
    e = rec["dry_run"]
    need(isinstance(e, dict) and set(e) == {"payload", "invoked_utc", "invocation_type", "status_code", "function_error", "returned", "report", "objects_after", "request_id"}, "dry_run keys")
    need(e["payload"] == {"dry_run": True, "shard": 0, "shards": SHARDS} and e["invocation_type"] == "RequestResponse" and e["status_code"] == 200 and e["function_error"] is None, "the dry run: shard 0 of 7, synchronous, 200, no function error")
    need(H.UTC.match(str(e["invoked_utc"])) and e["invoked_utc"] >= rec["apply_finished_utc"], "dry_run.invoked_utc not before the apply finished")
    r = e["returned"]
    need(isinstance(r, dict) and set(r) == {"ok", "accounts", "refused_count"} and r["ok"] is True and is_int(r["accounts"]) and r["accounts"] > 0 and r["refused_count"] == 0, "the dry run returned ok, a positive shard count and 0 refusals (counts only, never an id)")
    check_report(e["report"], "dry_run")
    need(e["objects_after"] == ob and nes(e["request_id"]), "the dry run must leave the prefix's object counts unchanged")
    c = rec["canary"]
    ck = {"payload_shape", "account_hash12", "invoked_utc", "status_code", "function_error", "returned", "report", "objects_after", "checks", "request_id"}
    need(isinstance(c, dict) and set(c) == ck, "canary keys differ")
    need(c["payload_shape"] == {"accounts": 1} and HEX12.match(str(c["account_hash12"])) and c["status_code"] == 200 and c["function_error"] is None and H.UTC.match(str(c["invoked_utc"])) and c["invoked_utc"] >= e["invoked_utc"], "canary: payload {accounts: one}, a hash prefix, 200, no error, after the dry run")
    need(c["returned"] == {"ok": True, "accounts": 1, "refused_count": 0} and c["objects_after"] == ob, "canary: one account published, none refused, the prefix's object counts unchanged (same keys)")
    check_report(c["report"], "canary")
    need(isinstance(c["checks"], dict) and set(c["checks"]) == set(CHECKS) | {"publisher_version"} and all(c["checks"][k] is True for k in CHECKS) and c["checks"]["publisher_version"] == "0.4.0" and nes(c["request_id"]), "canary checks: all true and publisher_version 0.4.0")
    fu = rec["full"]
    fk = {"payload", "invoked_utc", "status_code", "function_error", "returned", "shard_reports", "published", "refused", "objects_after", "sampled_hash12", "sample_checks_pass", "pair_count", "manifest_calendar_count", "calendar_sources_answered",
          "manifest_v040_count", "nonempty_unreported_series_count", "request_ids"}
    need(isinstance(fu, dict) and set(fu) == fk, "full keys differ: %s" % (sorted(set(fu) ^ fk) if isinstance(fu, dict) else "?"))
    need(fu["payload"] == {} and fu["status_code"] == 200 and fu["function_error"] is None and H.UTC.match(str(fu["invoked_utc"])) and fu["invoked_utc"] >= c["invoked_utc"], "full: payload {}, 200, no error, after the canary")
    need(isinstance(fu["returned"], dict) and fu["returned"].get("ok") is True and fu["returned"].get("fanned_out") == SHARDS and is_int(fu["returned"].get("accounts")), "full: the fan-out answer (ok, 7 shards, the account count)")
    need(isinstance(fu["shard_reports"], list) and len(fu["shard_reports"]) == SHARDS, "full: exactly %d shard REPORT lines" % SHARDS)
    for i, rp in enumerate(fu["shard_reports"]):
        check_report(rp, "full shard %d" % i)
    n = fu["published"]
    need(is_int(n) and n >= 6949 and fu["refused"] == 0 and n == fu["returned"]["accounts"], "full: published (the sum of the shards' log lines) equals the fan-out's account count, at least 6,949, 0 refused")
    oa = fu["objects_after"]
    need(isinstance(oa, dict) and oa == {"series": n, "manifest": n, "other": ob["other"]}, "full: series and manifests equal published and the other objects are unchanged")
    need(fu["pair_count"] == n and fu["manifest_calendar_count"] == n and fu["manifest_v040_count"] == n, "full: the pair, calendar_source and publisher 0.4.0 counts must each equal published")
    cs = fu["calendar_sources_answered"]
    need(isinstance(cs, list) and cs and cs == sorted(set(cs)) and set(cs) <= set(CAL_VALUES), "full: calendar_sources_answered")
    need(fu["nonempty_unreported_series_count"] == rec["absent_days"]["accounts_touched"], "full: the count of series with a non-empty list must equal the absent-days check's accounts touched")
    need(isinstance(fu["sampled_hash12"], list) and len(fu["sampled_hash12"]) == 10 and all(HEX12.match(str(x)) for x in fu["sampled_hash12"]) and fu["sample_checks_pass"] is True and isinstance(fu["request_ids"], list) and fu["request_ids"], "full: ten sampled hash prefixes, the sample checks, request ids")
    need(rec["ledger_closed"] is False and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "the ledger must stay OPEN; reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def absent_dates(root, first, last, gold_days):
    sys.path.insert(0, str(Path(root) / "lib"))
    import trading_calendar as tc
    cal = [d.isoformat() for d in tc.trading_days_between(dt.date.fromisoformat(first), dt.date.fromisoformat(last))]
    have = set(gold_days)
    return [d for d in cal if d not in have], [d for d in gold_days if d not in set(cal) and first <= d <= last]


def live(root, rec):
    import boto3
    lam, iam, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam"), boto3.client("s3")
    sch, logs = boto3.client("scheduler", region_name="us-east-1"), boto3.client("logs", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    try:
        conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    except Exception:  # noqa: BLE001
        conc = None
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    sc = sch.get_schedule(Name=SCHEDULE)
    ver = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)
    return {"layers": [x["Arn"] for x in cfg.get("Layers", [])], "memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "handler": cfg["Handler"], "runtime": cfg["Runtime"], "role": cfg["Role"],
            "env": cfg.get("Environment"), "concurrency": conc, "sids": sorted(x.get("Sid", "") for x in sts), "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")},
            "schedule_target": sc["Target"]["Arn"], "artifact_version": ver.get("VersionId"), "s3": s3, "logs": logs}


def check_sample(root, a, sb, mb, nver, absent, rec):
    sys.path.insert(0, str(Path(root) / "infra/aws/lambda/investor-reporting/reporting-publish"))
    sys.modules.pop("publisher", None)
    import publisher
    contract = json.loads((Path(root) / "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json").read_bytes().decode("utf-8"))
    s = json.loads(gzip.decompress(sb).decode("utf-8"))
    m = json.loads(mb.decode("utf-8"))
    h = hashlib.sha256(a.encode()).hexdigest()[:12]
    bad = publisher.validate_against_contract(s, m, contract)
    need(not bad, "sample %s: the document does not validate against series contract %s: %s" % (h, contract["contract_version"], bad[:2]))
    need(contract["contract_version"] == "0.3.3", "the repo series contract is not 0.3.3")
    need(m["byte_sizes"]["series.json.gz"] == len(sb) and m["publisher_version"] == "0.4.0" and m["account_id"] == a, "sample %s: manifest size, version or account" % h)
    need(m.get("calendar_source") in CAL_VALUES, "sample %s: manifest calendar_source %r" % (h, m.get("calendar_source")))
    need("unreported_trading_days" in s and s["unreported_trading_days_basis"] == BASIS and isinstance(s["unreported_trading_days"], list), "sample %s: the unreported pair, an explicit list and the fixed basis" % h)
    want = [d for d in absent if s["first_data_date"] < d <= s["as_of"] and d not in s["date"]]
    need(s["unreported_trading_days"] == want, "sample %s: the list must equal the absent days inside its window" % h)
    need("income_claim" not in s and any(x is not None for x in s["income"]), "sample %s: numeric income, no income claim" % h)
    need(nver >= 2, "sample %s: the prior version of the series key must still be present (versions read: %d)" % (h, nver))
    return h


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
    if cid == "DBC166-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time, the live code hash, artifact version and ENABLED schedule before), ledger %s, applier named, build %s equals the packet's and landed as a NEW version, plan 0 add / 1 change / 0 destroy on the function by code attributes only, and the apply at or after 13:00Z outside the fire window" % (LEDGER_SLUG, rec["build"]["zip_sha256"][:12]))
        return True
    check_tail(rec)
    lv = live(root, rec)
    if cid == "DBC166-2-AC1":
        need(lv["memory"] == 1024 and lv["timeout"] == 300 and lv["handler"] == "handler.lambda_handler" and lv["runtime"] == "python3.12" and lv["role"].endswith("role/" + ROLE), "live function: memory/timeout/handler/runtime/role")
        need(lv["concurrency"] is None and not (lv["env"] or {}).get("Variables"), "live function: no reserved concurrency, no environment")
        need(lv["code_sha256"] == rec["build"]["zip_sha256_b64"] != BEFORE_CODE and len(lv["layers"]) == 1 and lv["layers"][0] == rec["after"]["function"]["layer_arn"], "live CodeSha256 must equal the landed zip's, differ from the old, and the one layer unchanged")
        need(lv["sids"] == EXEC_SIDS, "live execution policy: the eight statements, unchanged")
        need(lv["schedule"] == {"state": "ENABLED", "cron": CRON, "zone": ZONE} and lv["schedule_target"].endswith(":function:" + FUNCTION), "the schedule must be ENABLED, untouched, on the one function: %s" % lv["schedule"])
        need(nes(lv["artifact_version"]) and lv["artifact_version"] == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
        print("OK: live: the function runs the NEW code (CodeSha256 equals the landed zip's, not the old); memory 1024, timeout 300, no reserved concurrency, no environment, one layer; the execution policy is unchanged (eight statements); the daily schedule is ENABLED at %s %s, untouched; the artifact's current version is the recorded one" % (CRON, ZONE))
        return True
    if cid == "DBC166-3-AC1":
        s3, logs = lv["s3"], lv["logs"]
        objs = H.list_all(s3, BUCKET, PREFIX)
        keys = [k for k, _, _ in objs]
        n = rec["full"]["published"]
        ser = sorted(k for k in keys if k.endswith("/series.json.gz"))
        man = sorted(k for k in keys if k.endswith("/manifest.json"))
        other = len(keys) - len(ser) - len(man)
        need(len(ser) == len(man) == n and other == rec["before"]["objects"]["other"], "the prefix holds %d series, %d manifests and %d others; the record says %d, %d and %d" % (len(ser), len(man), other, n, n, rec["before"]["objects"]["other"]))
        newest = max(t for k, t, _ in objs if k.endswith("/series.json.gz"))
        need(newest.strftime("%Y-%m-%dT%H:%M:%SZ") >= rec["canary"]["invoked_utc"], "no series is newer than the canary: nothing was republished")
        gold = sorted({k[len(GOLD_PREFIX) + 5:len(GOLD_PREFIX) + 15] for k, _, _ in H.list_all(s3, BUCKET, GOLD_PREFIX) if k.endswith(".parquet")})
        lo, hi = rec["absent_days"]["range"]
        absent, odd = absent_dates(root, lo, hi, [d for d in gold if lo <= d <= hi])
        need(absent == rec["absent_days"]["dates"] and not odd, "the absent days (the trading calendar minus the gold partitions in the range) differ from the record: live %s" % absent[:3])

        def read(k):
            return gzip.decompress(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()), s3.get_object(Bucket=BUCKET, Key=k.replace("series.json.gz", "manifest.json"))["Body"].read()

        pair = cal = v40 = nonempty = 0
        sources = set()
        by_acct = {}
        with ThreadPoolExecutor(max_workers=12) as pool:
            for k, (sb, mb) in zip(ser, pool.map(read, ser)):
                s, m = json.loads(sb.decode("utf-8")), json.loads(mb.decode("utf-8"))
                by_acct[k] = (s, m)
                ok = "unreported_trading_days" in s and s.get("unreported_trading_days_basis") == BASIS and isinstance(s["unreported_trading_days"], list)
                pair += 1 if ok else 0
                cal += 1 if m.get("calendar_source") in CAL_VALUES else 0
                v40 += 1 if m.get("publisher_version") == "0.4.0" else 0
                if m.get("calendar_source") in CAL_VALUES:
                    sources.add(m["calendar_source"])
                if ok and s["unreported_trading_days"]:
                    nonempty += 1
                    need(set(s["unreported_trading_days"]) <= set(absent), "a series lists a day that is not in the absent-days set")
        need(pair == cal == v40 == n, "series with the pair %d, manifests with calendar_source %d, manifests at 0.4.0 %d; published %d" % (pair, cal, v40, n))
        need(nonempty == rec["full"]["nonempty_unreported_series_count"] == rec["absent_days"]["accounts_touched"], "series with a non-empty list: live %d, record %d, absent-days check %d" % (nonempty, rec["full"]["nonempty_unreported_series_count"], rec["absent_days"]["accounts_touched"]))
        need(sorted(sources) == rec["full"]["calendar_sources_answered"], "the calendar sources answered differ from the record")
        pick = [ser[i] for i in range(0, len(ser), max(1, len(ser) // 10))][:10]
        hs = []
        for k in pick:
            a = k[len(PREFIX):].split("/")[0][len("account="):]
            vs = s3.list_object_versions(Bucket=BUCKET, Prefix=k).get("Versions", [])
            sb = s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()
            mb = s3.get_object(Bucket=BUCKET, Key=k.replace("series.json.gz", "manifest.json"))["Body"].read()
            hs.append(check_sample(root, a, sb, mb, len(vs), absent, rec))
        need(len(hs) == 10 and hs == rec["full"]["sampled_hash12"], "the ten sampled accounts (by position) must equal the record's hash prefixes")
        rp = rec["dry_run"]["report"]
        reps, tok = [], None
        for _ in range(100):
            kw = {"logGroupName": LOG_GROUP, "filterPattern": "REPORT"}
            if tok:
                kw["nextToken"] = tok
            r = logs.filter_log_events(**kw)
            for ev in r.get("events", []):
                m2 = re.search(r"Duration: ([\d.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ev["message"], re.S)
                if m2:
                    reps.append((float(m2.group(1)), int(m2.group(2)), int(m2.group(3))))
            tok = r.get("nextToken")
            if not tok:
                break
        need([x for x in reps if x[2] == rp["max_memory_used_mb"] and abs(x[0] - rp["duration_ms"]) < 1.0 and x[1] == 1024], "no REPORT line in the log group equals the dry run's")
        need((root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file(), "the ledger's open marker is missing: the ledger must stay OPEN")
        print("OK: %d series and %d manifests (the %d others untouched), every one carries the unreported-days pair as an explicit list with the fixed basis (%d non-empty, each inside the absent-days set of %d day(s)), calendar_source and publisher 0.4.0; ten sampled series validate against series contract 0.3.3 with the prior version of each key present; a REPORT line equals the dry run's; ledger open" % (len(ser), len(man), other, nonempty, len(absent)))
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
        rp = {"max_memory_used_mb": 400, "duration_ms": 9000.0, "memory_size_mb": 1024}
        ob = {"series": 6949, "manifest": 6949, "other": 4344}
        good = {"claim": "measured", "gates": {"packet_blob": "b" * 40, "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
                                               "one_change_at_a_time": {"worktrees_read": 5, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
                "ledger_entry": LEDGER_SLUG, "applier": APPLIER, "before": {"function_code_sha256": BEFORE_CODE, "artifact_version_id": BEFORE_VERSION, "schedule": {"state": "ENABLED", "cron": CRON}, "objects": dict(ob)},
                "build": {"zip_sha256": zh, "zip_sha256_b64": b64_of_hex(zh), "members": ["handler.py", "lib/trading_calendar.py"] + ["m%d" % i for i in range(15)], "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": zh, "built_equals_landed": True},
                "plan": {"add": 0, "change": 1, "destroy": 0, "change_addresses": ["module.x.aws_lambda_function.this"], "function_change_attributes": ["source_code_hash", "s3_object_version"], "replan_no_changes": True},
                "apply_finished_utc": "2026-10-16T13:10:00Z",
                "after": {"function": {"memory": 1024, "timeout": 300, "reserved_concurrency": None, "code_sha256": b64_of_hex(zh), "layer_arn": "arn:aws:lambda:us-east-1:1:layer:%s:1" % LAYER}, "policy_sids": list(EXEC_SIDS),
                          "schedule": {"state": "ENABLED", "cron": CRON, "zone": ZONE}},
                "absent_days": {"range": ["2024-07-08", "2026-10-14"], "count": 0, "dates": [], "accounts_touched": 0, "all_nyse_trading_days": True},
                "dry_run": {"payload": {"dry_run": True, "shard": 0, "shards": SHARDS}, "invoked_utc": "2026-10-16T13:15:00Z", "invocation_type": "RequestResponse", "status_code": 200, "function_error": None,
                            "returned": {"ok": True, "accounts": 990, "refused_count": 0}, "report": rp, "objects_after": dict(ob), "request_id": "r1"},
                "canary": {"payload_shape": {"accounts": 1}, "account_hash12": "abcdef012345", "invoked_utc": "2026-10-16T13:16:00Z", "status_code": 200, "function_error": None, "returned": {"ok": True, "accounts": 1, "refused_count": 0},
                           "report": rp, "objects_after": dict(ob), "request_id": "r2", "checks": dict({k: True for k in CHECKS}, publisher_version="0.4.0")},
                "full": {"payload": {}, "invoked_utc": "2026-10-16T13:17:00Z", "status_code": 200, "function_error": None, "returned": {"ok": True, "accounts": 6949, "fanned_out": SHARDS}, "shard_reports": [dict(rp) for _ in range(SHARDS)],
                         "published": 6949, "refused": 0, "objects_after": {"series": 6949, "manifest": 6949, "other": 4344}, "sampled_hash12": ["%012x" % i for i in range(10)], "sample_checks_pass": True, "pair_count": 6949,
                         "manifest_calendar_count": 6949, "calendar_sources_answered": ["fallback_2010_2027"], "manifest_v040_count": 6949, "nonempty_unreported_series_count": 0, "request_ids": ["r3"]},
                "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
        blob, ok_text = "b" * 40, ("SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12])
        assert check_head(good, blob, ok_text[0], ok_text[1], True) and check_tail(good)
        arms = (("claim", lambda r: r.update(claim="inferred")), ("blob", lambda r: r["gates"].update(packet_blob="c" * 40)), ("cto", lambda r: r["gates"].update(cto_half_signed=False)), ("applier", lambda r: r.update(applier="x")),
                ("before code", lambda r: r["before"].update(function_code_sha256="z")), ("before schedule", lambda r: r["before"].update(schedule={"state": "DISABLED", "cron": CRON})), ("before objects", lambda r: r["before"]["objects"].update(series=10)),
                ("build hash", lambda r: r["build"].update(zip_sha256_b64="x")), ("same version", lambda r: r["build"].update(landed_version_id=BEFORE_VERSION)), ("plan add", lambda r: r["plan"].update(add=1)),
                ("plan change", lambda r: r["plan"].update(change=2)), ("plan destroy", lambda r: r["plan"].update(destroy=1)), ("plan addr", lambda r: r["plan"].update(change_addresses=["x.aws_iam_role.y"])),
                ("plan attrs", lambda r: r["plan"].update(function_change_attributes=["memory_size"])), ("replan", lambda r: r["plan"].update(replan_no_changes=False)),
                ("apply before 13Z", lambda r: r.update(apply_finished_utc="2026-10-16T12:50:00Z")), ("memory", lambda r: r["after"]["function"].update(memory=512)), ("timeout", lambda r: r["after"]["function"].update(timeout=900)),
                ("code stale", lambda r: r["after"]["function"].update(code_sha256="x")), ("policy", lambda r: r["after"].update(policy_sids=["x"])), ("schedule disabled", lambda r: r["after"]["schedule"].update(state="DISABLED")),
                ("absent count", lambda r: r["absent_days"].update(count=3)), ("absent not nyse", lambda r: r["absent_days"].update(all_nyse_trading_days=False)), ("dry payload", lambda r: r["dry_run"].update(payload={})),
                ("dry shard", lambda r: r["dry_run"]["payload"].update(shard=1)), ("dry refused", lambda r: r["dry_run"]["returned"].update(refused_count=1)), ("dry objects", lambda r: r["dry_run"].update(objects_after={"series": 1, "manifest": 1, "other": 1})),
                ("memory line", lambda r: r["dry_run"]["report"].update(max_memory_used_mb=900)), ("canary two", lambda r: r["canary"]["returned"].update(accounts=2)), ("canary check", lambda r: r["canary"]["checks"].update(pair_present=False)),
                ("canary version", lambda r: r["canary"]["checks"].update(publisher_version="0.3.0")), ("full shards", lambda r: r["full"]["shard_reports"].pop()), ("full fanned", lambda r: r["full"]["returned"].update(fanned_out=6)),
                ("full published", lambda r: r["full"].update(published=6948)), ("full refused", lambda r: r["full"].update(refused=1)), ("full objects", lambda r: r["full"]["objects_after"].update(other=1)),
                ("full pair", lambda r: r["full"].update(pair_count=6948)), ("full v040", lambda r: r["full"].update(manifest_v040_count=1)), ("full nonempty", lambda r: r["full"].update(nonempty_unreported_series_count=5)),
                ("full calendar", lambda r: r["full"].update(calendar_sources_answered=["x"])), ("ledger", lambda r: r.update(ledger_closed=True)), ("extra", lambda r: r.update(z=1)))
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
        assert in_fire_window("2026-10-16T12:30:00Z") and not in_fire_window("2026-10-16T13:00:00Z") and not in_fire_window("2026-10-17T12:30:00Z")
    finally:
        BUILD_B64, PACKET_SHA = saved
    print("selftest: record clauses behave on a green arm and %d red arms (plus two head arms and the fire-window rule)" % len(arms))
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
