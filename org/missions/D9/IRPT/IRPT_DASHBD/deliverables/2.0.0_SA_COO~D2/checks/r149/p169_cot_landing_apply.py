"""IRPT_DASHBD round 149, workstream COTLANDAPPLY (issuer 2.0.0_SA_COO~D2) -- DB-b-301, the APPLY of the signed never-widen pair for the Cottonwood account-return landing function (packet sha256 778009ecda40, COO half
@621ef11955, CTO half @ae495e5ee7): the new bundle, ONE safe-apply (plan exactly 0 add / 1 change / 0 destroy: the function's code), a dry run of the rewrite on the first range, FOUR rewrite events over the 66 landed
gold days (around the three held days), and the whole-prefix after-read. WORLD. The record is the applier's; the checker re-reads the world.

  DBC169-1-AC1  the record's head: packet and halves, gates, ledger and applier, before, build, plan, the timing rule
  DBC169-2-AC1  FRESH live reads: the function's code, the policy (five statements), the schedule, the artifact version; the dry run and the four events in the record
  DBC169-3-AC1  FRESH reads of the gold: each of the 66 days against its oldest version, the history days untouched, the held days absent, the PARTIAL set recomputed from the floor day's silver

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def helper(rel, name):
    spec = importlib.util.spec_from_file_location(name, str(HERE.parent / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


H = helper("r147/p151_pubapply.py", "p151_helper_169")
G = helper("r149/p168_gold49f_apply.py", "p168_helper_169")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D, APPLIER = H.D, H.APPLIER
REC_REL = D + APPLIER + "/COT_LANDING_REWRITE_RECORD.json"
PD = D + "2.0.0_SA_COO~D2/"
PACKET_REL = PD + "NEVER_WIDEN_PACKET_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE.md"
COO_HALF_REL = PD + "NEVER_WIDEN_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_LANDING_CODE_UPDATE_REWRITE_CTO_HALF.md"
PACKET_SHA = "778009ecda403f17f2eb81163507e6ca9f1738dfa3417735bb6cf4b8e4d5aeaf"
PACKET_BLOB = "05b8884c840de0dfcdc3e8a005c2264a29fe0b69"
BUILD_B64 = "FH4+ZDunLNxCc2pb03bx9U10iAcmQQrvYPaBx5xnjew="
BEFORE_CODE = "fQFe4moIeMHspIjLxO2C04TobQW6cNZc7mfwstcMWzs="
BEFORE_VERSION = "UnMNWDhcC3KpERDmGYdKAl83whx1oNFW"
LEDGER_SLUG = "irpt-dashbd-cottonwood-landing-codeupdate-rewrite-20261016"
FUNCTION, ROLE, POLICY = "irpt-cot-account-return-daily-lambda", "irpt-cot-account-return-daily-execution-role", "irpt-cot-account-return-daily-execution-policy"
SCHEDULE, CRON, ZONE = "irpt-cot-account-return-daily-daily", "cron(15 8 ? * MON-FRI *)", "America/New_York"
SIDS = sorted(["ListSilverTablePrefixesOnly", "ReadTwoBlackDiamondSilverTablesOnly", "WriteTheOneAccountReturnDailyGoldPrefixOnly", "ListTheOneAccountReturnDailyGoldPrefixOnly", "OwnLogStreamOnly"])
ARTIFACT_BUCKET, ARTIFACT_KEY = "opal-313476888478-lambda-artifacts", "investor-reporting/irpt-cot-account-return-daily-lambda.zip"
BUCKET = "opal-data-cottonwood"
FLOOR = "2026-07-10"
NEWEST = "2026-10-15"
HELD = ["2026-08-19", "2026-09-24", "2026-09-25"]
HISTORY_DAYS, HISTORY_LAST, HISTORY_FIRST = 3325, "2026-06-22", "2013-04-03"
LANDED = 66
EVENTS = [("2026-07-10", "2026-08-13", 25), ("2026-08-14", "2026-08-18", 3), ("2026-08-20", "2026-09-23", 24), ("2026-09-28", "2026-10-15", 14)]
MEM_LINE, DUR_LINE = 819, 720000
LAYER = "irpt-performance-native-layer"
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("history_keys_sha256", "keys_sha256", "request_ids")
in_window = G.in_window


def check_report(rp, label):
    need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"}, "%s: report keys" % label)
    need(is_int(rp["max_memory_used_mb"]) and rp["max_memory_used_mb"] <= MEM_LINE and rp["memory_size_mb"] == 1024 and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] <= DUR_LINE,
         "%s: Max Memory Used at most %d MB and duration at most %d ms (no resize inside this pair)" % (label, MEM_LINE, DUR_LINE))


def check_head(rec, packet_blob, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "build", "plan", "apply_finished_utc", "after", "dry_run", "events", "act5", "ledger_closed", "reads"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    g = rec["gates"]
    need(isinstance(g, dict) and set(g) == {"packet_blob", "packet_sha256", "coo_half_signed", "cto_half_signed", "pin_is_ancestor", "one_change_at_a_time", "live_matches_packet"}, "gates keys")
    need(g["packet_blob"] == packet_blob == PACKET_BLOB and g["packet_sha256"] == PACKET_SHA, "the packet's blob or sha256 differs from the signed one")
    need(g["coo_half_signed"] is True and "SIGNED" in coo_text and PACKET_SHA in coo_text, "the COO half does not read SIGNED at the packet's sha256")
    need(g["cto_half_signed"] is True and "SIGNED" in cto_text and PACKET_SHA[:12] in cto_text, "the CTO half does not read SIGNED at the packet's sha256")
    need(g["pin_is_ancestor"] is True and g["live_matches_packet"] is True, "pin ancestry and live-state gates must be recorded true")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and is_int(oc["worktrees_read"]) and oc["worktrees_read"] >= 1 and oc["open_markers_naming_this_surface"] == 0, "one_change_at_a_time: the denominator and zero markers")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists, "the ledger entry %s must exist" % LEDGER_SLUG)
    need(rec["applier"] == APPLIER, "the applier must be named: %s" % APPLIER)
    b = rec["before"]
    need(isinstance(b, dict) and set(b) == {"function_code_sha256", "artifact_version_id", "policy", "schedule", "partitions_total", "history_days", "history_keys", "history_keys_sha256", "landed_days", "newest_day"}, "before keys")
    need(b["function_code_sha256"] == BEFORE_CODE and b["artifact_version_id"] == BEFORE_VERSION, "before: the live code hash and artifact version of the packet's section 3")
    need(isinstance(b["policy"], dict) and sorted(b["policy"]) == SIDS and all(re.fullmatch(r"[0-9a-f]{64}", str(v)) for v in b["policy"].values()), "before.policy: sha256 of each of the five statements")
    need(b["schedule"] == {"state": "ENABLED", "cron": CRON}, "before.schedule: ENABLED at the cron")
    need(b["history_days"] == HISTORY_DAYS and is_int(b["history_keys"]) and b["history_keys"] >= HISTORY_DAYS and re.fullmatch(r"[0-9a-f]{64}", str(b["history_keys_sha256"])), "before: the 3,325 history days with their key list hash")
    need(b["landed_days"] == LANDED and b["partitions_total"] == HISTORY_DAYS + LANDED and b["newest_day"] == NEWEST, "before: 66 landed days, 3,391 partitions, newest %s" % NEWEST)
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == G.b64_of_hex(bd["zip_sha256"]) == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s" % BUILD_B64)
    need(isinstance(bd["members"], list) and "handler.py" in bd["members"] and len(bd["members"]) >= 10, "the zip must hold the handler and its staged members")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["landed_version_id"] != BEFORE_VERSION and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "import smoke, a NEW landed version or built-equals-landed")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "change_addresses", "function_change_attributes", "replan_no_changes"}, "plan keys")
    strip = lambda a: re.sub(r"^module\.[^.]+\.", "", str(a))  # noqa: E731
    need(p["add"] == 0 and p["change"] == 1 and p["destroy"] == 0 and [strip(a) for a in p["change_addresses"]] == ["aws_lambda_function.this"] and p["replan_no_changes"] is True,
         "the plan must read 0 add / 1 change / 0 destroy on the function and a post-apply plan of No changes")
    fa = p["function_change_attributes"]
    need(isinstance(fa, list) and fa and set(fa) <= {"source_code_hash", "s3_object_version", "s3_key", "s3_bucket", "last_modified", "qualified_arn", "qualified_invoke_arn", "version", "source_code_size"}, "the function change must be by CODE attributes only: %s" % fa)
    t = rec["apply_finished_utc"]
    need(H.UTC.match(str(t)) and not in_window(t, "12:05", "12:45"), "the apply must be outside 12:05Z to 12:45Z on a trading weekday (the CTO's condition 4)")
    return True


def check_tail(rec):
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy", "schedule"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 900 and f.get("reserved_concurrency") == 1 and f.get("code_sha256") == rec["build"]["zip_sha256_b64"] and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"],
         "after.function: memory 1024, timeout 900, reserved concurrency 1, the landed zip's code hash, the native layer")
    need(a["policy"] == rec["before"]["policy"], "after.policy: all five statements byte-identical to before")
    need(a["schedule"] == {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "after.schedule untouched")
    d = rec["dry_run"]
    need(isinstance(d, dict) and set(d) == {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "rows_match_landed", "versions_unchanged", "request_id"}, "dry_run keys")
    need(d["payload"] == {"rewrite": {"start": EVENTS[0][0], "end": EVENTS[0][1]}, "dry_run": True}, "dry run: the first range with dry_run true")
    need(d["status_code"] == 200 and d["function_error"] is None and H.UTC.match(str(d["invoked_utc"])) and d["invoked_utc"] >= rec["apply_finished_utc"] and not in_window(d["invoked_utc"], "12:05", "12:45"), "dry run: 200, no error, after the apply, outside the fire window")
    r = d["returned"]
    need(isinstance(r, dict) and set(r) == {"ok", "rewrite", "days", "held"} and r["ok"] is True and r["rewrite"] is True and r["held"] == 0 and is_int(r["days"]) and r["days"] == EVENTS[0][2], "dry run: ok, rewrite, 0 held, 25 days")
    check_report(d["report"], "dry_run")
    need(d["rows_match_landed"] is True and d["versions_unchanged"] is True and nes(d["request_id"]), "dry run: every day's rows equal the landed ones and the version lists are unchanged")
    ev = rec["events"]
    need(isinstance(ev, list) and len(ev) == len(EVENTS), "events: exactly %d" % len(EVENTS))
    ek = {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "rows", "before_partial", "partial", "full", "full_to_partial", "partial_to_full", "floor_day_accounts", "floor_day_positive", "request_id"}
    prev = d["invoked_utc"]
    floor_acc = floor_pos = None
    for i, (e, (s, en, n)) in enumerate(zip(ev, EVENTS)):
        lb = "event %d" % (i + 1)
        need(isinstance(e, dict) and set(e) == ek, "%s: keys" % lb)
        need(e["payload"] == {"rewrite": {"start": s, "end": en}}, "%s: payload must be the packet's range %s to %s with no dry_run" % (lb, s, en))
        need(e["status_code"] == 200 and e["function_error"] is None and H.UTC.match(str(e["invoked_utc"])) and e["invoked_utc"] >= prev and not in_window(e["invoked_utc"], "12:05", "12:45"), "%s: 200, no error, in order, outside the fire window" % lb)
        prev = e["invoked_utc"]
        r = e["returned"]
        need(isinstance(r, dict) and set(r) == {"ok", "rewrite", "days", "held"} and r["ok"] is True and r["rewrite"] is True and r["held"] == 0 and r["days"] == n, "%s: ok, rewrite, 0 held, %d days" % (lb, n))
        check_report(e["report"], lb)
        need(is_int(e["rows"]) and e["rows"] > 0 and e["before_partial"] == e["rows"], "%s: rows and every landed row PARTIAL_HISTORY before" % lb)
        need(is_int(e["partial"]) and is_int(e["full"]) and e["partial"] + e["full"] == e["rows"], "%s: PARTIAL plus FULL equals rows" % lb)
        need(e["full_to_partial"] == 0 and e["partial_to_full"] == e["full"], "%s: no FULL to PARTIAL flip (the CTO's condition 1) and the PARTIAL to FULL flips equal the FULL rows" % lb)
        need(is_int(e["floor_day_accounts"]) and is_int(e["floor_day_positive"]) and 0 < e["floor_day_positive"] <= e["floor_day_accounts"], "%s: the floor day's account counts" % lb)
        floor_acc = floor_acc or e["floor_day_accounts"]
        floor_pos = floor_pos or e["floor_day_positive"]
        need(e["floor_day_accounts"] == floor_acc and e["floor_day_positive"] == floor_pos, "%s: the floor-day counts must be one number across events" % lb)
        need(nes(e["request_id"]), "%s: request id" % lb)
    a5 = rec["act5"]
    need(isinstance(a5, dict) and set(a5) == {"partitions_total", "history_days", "history_keys", "history_keys_sha256", "history_one_version_all", "landed_days", "landed_keys_two_versions_all", "held_days_absent", "other_new_keys", "schedule_state"}, "act5 keys")
    b = rec["before"]
    need(a5["partitions_total"] == b["partitions_total"] and a5["history_days"] == HISTORY_DAYS and a5["history_keys"] == b["history_keys"] and a5["history_keys_sha256"] == b["history_keys_sha256"],
         "act5: the 3,325 history days' key list (with version ids) equal before's, all of them read")
    need(a5["history_one_version_all"] is True and a5["landed_days"] == LANDED and a5["landed_keys_two_versions_all"] is True and a5["held_days_absent"] is True and a5["other_new_keys"] == 0 and a5["schedule_state"] == "ENABLED", "act5: one version on every history key, two on the 66 days' keys, the held days absent, no other new key, schedule ENABLED")
    need(rec["ledger_closed"] is False and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "the ledger must stay OPEN; reads block")
    scan = copy.deepcopy(rec)
    scan["before"].pop("policy", None)
    scan["after"].pop("policy", None)
    need(not H.digit_runs(scan), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(scan)[:2])
    return True


def partition_days(s3, prefix):
    out = set()
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix, Delimiter="/"):
        out |= {c["Prefix"][len(prefix):].strip("/")[5:] for c in pg.get("CommonPrefixes", [])}
    return sorted(out)


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
    if cid == "DBC169-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time), ledger %s, applier named, build %s equals the packet's and landed as a NEW version, plan 0 add / 1 change / 0 destroy on the function by code attributes only, the apply outside the fire window" % (LEDGER_SLUG, rec["build"]["zip_sha256"][:12]))
        return True
    check_tail(rec)
    import boto3
    lam, iam, s3, sch = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam"), boto3.client("s3"), boto3.client("scheduler", region_name="us-east-1")
    if cid == "DBC169-2-AC1":
        cfg = lam.get_function_configuration(FunctionName=FUNCTION)
        conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
        need(cfg["MemorySize"] == 1024 and cfg["Timeout"] == 900 and cfg["Handler"] == "handler.lambda_handler" and cfg["Runtime"] == "python3.12" and cfg["Role"].endswith("role/" + ROLE) and conc == 1 and not (cfg.get("Environment") or {}).get("Variables"), "live function: memory/timeout/handler/runtime/role, reserved concurrency 1, no environment")
        need(cfg["CodeSha256"] == rec["build"]["zip_sha256_b64"] != BEFORE_CODE and [x["Arn"] for x in cfg.get("Layers", [])] == [rec["after"]["function"]["layer_arn"]], "live CodeSha256 must equal the landed zip's, differ from the old, and the one layer unchanged")
        doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
        sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
        need({x["Sid"]: G.stmt_hash(x) for x in sts} == rec["after"]["policy"], "live execution policy: the five statements must equal the record's (unchanged from before)")
        sc = sch.get_schedule(Name=SCHEDULE)
        need({"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")} == {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "the schedule must be ENABLED, untouched")
        ver = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)
        need(ver.get("VersionId") == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
        print("OK: live: the function runs the NEW code; the five-statement policy and the schedule are untouched; the artifact's current version is the recorded one; the dry run (25 days, 0 held, inside 819 MB / 720 s) and the four events (0 held, no FULL to PARTIAL flip) hold every clause of the packet and the CTO's half")
        return True
    if cid == "DBC169-3-AC1":
        sys.path.insert(0, str(root / "lib"))
        sys.path.insert(0, str(root / "data/assets/scripts/gold/irpt_reporting/adapters"))
        import cottonwood_bd_account_return_daily as cbd
        import pyarrow.parquet as pq
        bucket, prefix = cbd.gold_prefix()
        need(bucket == BUCKET, "the adapter's gold bucket differs from the packet's")
        days = [d for d in partition_days(s3, prefix) if d <= NEWEST]
        hist = [d for d in days if d < FLOOR]
        landed = [d for d in days if d >= FLOOR]
        need(len(hist) == HISTORY_DAYS and hist[0] == HISTORY_FIRST and hist[-1] == HISTORY_LAST and len(landed) == LANDED and not set(HELD) & set(days), "partitions: %d history, %d landed from the floor, the held days absent" % (len(hist), len(landed)))
        vers = {}
        for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=prefix):
            for v in pg.get("Versions", []):
                m = re.match(r"^.*/date=([0-9-]{10})/(data\.parquet|manifest\.json)$", v["Key"])
                need(m, "an object under the gold prefix outside the two keys of a day: %s" % v["Key"].rsplit("/", 2)[-2:])
                vers.setdefault((m.group(1), v["Key"]), []).append(v)
        hk = sorted(k for k in vers if k[0] < FLOOR)
        need(all(len(vers[k]) == 1 for k in hk), "a history key holds more than one version")
        digest = hashlib.sha256("\n".join("%s|%s" % (k[1], vers[k][0]["VersionId"]) for k in hk).encode("utf-8")).hexdigest()
        need(len(hk) == rec["act5"]["history_keys"] and digest == rec["act5"]["history_keys_sha256"] == rec["before"]["history_keys_sha256"], "the history days' keys and version ids differ from the record (%d keys read)" % len(hk))
        reader = cbd.CottonwoodBlackDiamondSilverReader()
        ft = reader.read_parquet("fact_allocations", FLOOR).to_pydict()
        fv, _c, _n = cbd.day_values(list(zip(ft[cbd.ACCOUNT_COLUMN], ft[cbd.VALUE_COLUMN])), None)
        pos = {a for a, v in fv.items() if v > 0}
        posset = {str(x) for x in pos}
        ev = rec["events"]
        need(all(e["floor_day_accounts"] == len(fv) and e["floor_day_positive"] == len(pos) for e in ev), "the floor day: %d accounts, %d positive (record %s)" % (len(fv), len(pos), [(e["floor_day_accounts"], e["floor_day_positive"]) for e in ev][:1]))
        tot = {}
        for (s, en, n), e in zip(EVENTS, ev):
            ds = [d for d in landed if s <= d <= en]
            need(len(ds) == n, "range %s to %s holds %d landed days, not %d" % (s, en, len(ds), n))
            rows = part = full = 0
            for d in ds:
                kd, km = [k for k in vers if k[0] == d and k[1].endswith("data.parquet")][0], [k for k in vers if k[0] == d and k[1].endswith("manifest.json")][0]
                need(len(vers[kd]) == 2 and len(vers[km]) == 2, "%s: each of the two keys must hold exactly two versions" % d)
                newest = {k: sorted(vers[k], key=lambda v: v["LastModified"])[-1] for k in (kd, km)}
                oldest = {k: sorted(vers[k], key=lambda v: v["LastModified"])[0] for k in (kd, km)}
                need(all(newest[k]["IsLatest"] for k in newest), "%s: the newest version is not the latest" % d)
                rd = lambda k, v: s3.get_object(Bucket=BUCKET, Key=k[1], VersionId=v["VersionId"])["Body"].read()  # noqa: E731
                new_t = pq.read_table(io.BytesIO(rd(kd, newest[kd])))
                old_t = pq.read_table(io.BytesIO(rd(kd, oldest[kd])))
                need(new_t.num_rows == old_t.num_rows and "history_scope_claim" in new_t.column_names and "history_scope_claim" not in old_t.column_names, "%s: same rows, the claim column added" % d)
                cols = [c for c in old_t.column_names if c != "history_scope"]
                need(all(new_t[c].to_pylist() == old_t[c].to_pylist() for c in cols), "%s: a value column differs from the oldest version" % d)
                need(all(x == "inferred" for x in new_t["history_scope_claim"].to_pylist()), "%s: the claim must be inferred on every row" % d)
                need(set(old_t["history_scope"].to_pylist()) == {"PARTIAL_HISTORY"}, "%s: the oldest version must read PARTIAL_HISTORY on every row" % d)
                for a, sc in zip(new_t["account_id"].to_pylist(), new_t["history_scope"].to_pylist()):
                    need(sc == ("PARTIAL_HISTORY" if str(a) in posset else "FULL"), "%s: an account's history_scope differs from the floor-day rule" % d)
                rows += new_t.num_rows
                part += new_t["history_scope"].to_pylist().count("PARTIAL_HISTORY")
                full += new_t["history_scope"].to_pylist().count("FULL")
                nm, om = json.loads(rd(km, newest[km])), json.loads(rd(km, oldest[km]))
                need(nm["columns"] == om["columns"] + ["history_scope_claim"] and {k: v for k, v in nm.items() if k != "columns"} == {k: v for k, v in om.items() if k != "columns"}, "%s: the manifest must differ only in columns" % d)
            need(rows == e["rows"] and part == e["partial"] and full == e["full"], "event range %s to %s: rows %d/%d, PARTIAL %d/%d, FULL %d/%d (live/record)" % (s, en, rows, e["rows"], part, e["partial"], full, e["full"]))
            tot[s] = (rows, part, full)
        print("OK: the 66 landed days (4 ranges) each hold two versions of both keys; against the oldest version every value column is identical, the claim is inferred on every row, history_scope is PARTIAL_HISTORY exactly for the %d positive floor-day accounts (of %d) and FULL otherwise, the manifest differs only in its columns; the %d history days' %d keys and version ids equal the record's, one version each; the three held days are absent; %s" % (len(pos), len(fv), len(hist), len(hk), "totals (rows, PARTIAL, FULL) per event: %s" % list(tot.values())))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    global BUILD_B64, PACKET_SHA, PACKET_BLOB
    saved = (BUILD_B64, PACKET_SHA, PACKET_BLOB)
    zh = "cd" * 32
    BUILD_B64, PACKET_SHA, PACKET_BLOB = G.b64_of_hex(zh), "ee" * 32, "b" * 40
    try:
        rp = {"max_memory_used_mb": 600, "duration_ms": 90000.0, "memory_size_mb": 1024}
        pol = {s: ("%02x" % i) * 32 for i, s in enumerate(SIDS)}
        hk = "ab" * 32

        def ev(i, s, en, n):
            return {"payload": {"rewrite": {"start": s, "end": en}}, "invoked_utc": "2026-10-16T14:%02d:00Z" % (30 + i), "status_code": 200, "function_error": None, "returned": {"ok": True, "rewrite": True, "days": n, "held": 0},
                    "report": dict(rp), "rows": 800 * n, "before_partial": 800 * n, "partial": 700 * n, "full": 100 * n, "full_to_partial": 0, "partial_to_full": 100 * n, "floor_day_accounts": 867, "floor_day_positive": 760, "request_id": "r%d" % i}
        good = {"claim": "measured", "gates": {"packet_blob": PACKET_BLOB, "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
                                               "one_change_at_a_time": {"worktrees_read": 5, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
                "ledger_entry": LEDGER_SLUG, "applier": APPLIER,
                "before": {"function_code_sha256": BEFORE_CODE, "artifact_version_id": BEFORE_VERSION, "policy": pol, "schedule": {"state": "ENABLED", "cron": CRON}, "partitions_total": 3391, "history_days": 3325, "history_keys": 6650,
                           "history_keys_sha256": hk, "landed_days": 66, "newest_day": NEWEST},
                "build": {"zip_sha256": zh, "zip_sha256_b64": G.b64_of_hex(zh), "members": ["handler.py"] + ["m%d" % i for i in range(12)], "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": zh, "built_equals_landed": True},
                "plan": {"add": 0, "change": 1, "destroy": 0, "change_addresses": ["module.x.aws_lambda_function.this"], "function_change_attributes": ["source_code_hash", "s3_object_version"], "replan_no_changes": True},
                "apply_finished_utc": "2026-10-16T14:10:00Z",
                "after": {"function": {"memory": 1024, "timeout": 900, "reserved_concurrency": 1, "code_sha256": G.b64_of_hex(zh), "layer_arn": "arn:aws:lambda:us-east-1:1:layer:%s:1" % LAYER}, "policy": dict(pol), "schedule": {"state": "ENABLED", "cron": CRON, "zone": ZONE}},
                "dry_run": {"payload": {"rewrite": {"start": EVENTS[0][0], "end": EVENTS[0][1]}, "dry_run": True}, "invoked_utc": "2026-10-16T14:20:00Z", "status_code": 200, "function_error": None, "returned": {"ok": True, "rewrite": True, "days": 25, "held": 0},
                            "report": dict(rp), "rows_match_landed": True, "versions_unchanged": True, "request_id": "r0"},
                "events": [ev(i, s, en, n) for i, (s, en, n) in enumerate(EVENTS, 1)],
                "act5": {"partitions_total": 3391, "history_days": 3325, "history_keys": 6650, "history_keys_sha256": hk, "history_one_version_all": True, "landed_days": 66, "landed_keys_two_versions_all": True, "held_days_absent": True, "other_new_keys": 0, "schedule_state": "ENABLED"},
                "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
        ok = ("SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12])
        assert check_head(good, PACKET_BLOB, ok[0], ok[1], True) and check_tail(good)

        def e(i, **kw):
            return lambda r: r["events"][i].update(**kw)
        arms = (("claim", lambda r: r.update(claim="inferred")), ("cto", lambda r: r["gates"].update(cto_half_signed=False)), ("blob", lambda r: r["gates"].update(packet_blob="c" * 40)), ("applier", lambda r: r.update(applier="x")),
                ("before code", lambda r: r["before"].update(function_code_sha256="z")), ("before days", lambda r: r["before"].update(history_days=3000)), ("before landed", lambda r: r["before"].update(landed_days=65)),
                ("build hash", lambda r: r["build"].update(zip_sha256_b64="x")), ("same version", lambda r: r["build"].update(landed_version_id=BEFORE_VERSION)), ("plan add", lambda r: r["plan"].update(add=1)),
                ("plan change", lambda r: r["plan"].update(change=2)), ("plan destroy", lambda r: r["plan"].update(destroy=1)), ("plan addr", lambda r: r["plan"].update(change_addresses=["aws_iam_role.x"])),
                ("plan attrs", lambda r: r["plan"].update(function_change_attributes=["memory_size"])), ("replan", lambda r: r["plan"].update(replan_no_changes=False)), ("apply window", lambda r: r.update(apply_finished_utc="2026-10-16T12:30:00Z")),
                ("memory", lambda r: r["after"]["function"].update(memory=3008)), ("concurrency", lambda r: r["after"]["function"].update(reserved_concurrency=None)), ("policy moved", lambda r: r["after"]["policy"].update({SIDS[0]: "11" * 32})),
                ("schedule", lambda r: r["after"]["schedule"].update(state="DISABLED")), ("dry payload", lambda r: r["dry_run"].update(payload={"rewrite": {"start": EVENTS[0][0], "end": EVENTS[0][1]}})),
                ("dry held", lambda r: r["dry_run"]["returned"].update(held=1)), ("dry days", lambda r: r["dry_run"]["returned"].update(days=24)), ("dry memory", lambda r: r["dry_run"]["report"].update(max_memory_used_mb=900)),
                ("dry versions", lambda r: r["dry_run"].update(versions_unchanged=False)), ("events count", lambda r: r["events"].pop()), ("ev1 range", e(0, payload={"rewrite": {"start": "2026-07-10", "end": "2026-08-18"}})),
                ("ev2 dry_run", e(1, payload={"rewrite": {"start": EVENTS[1][0], "end": EVENTS[1][1]}, "dry_run": True})), ("ev3 held", lambda r: r["events"][2]["returned"].update(held=1)), ("ev3 days", lambda r: r["events"][2]["returned"].update(days=25)),
                ("ev4 order", e(3, invoked_utc="2026-10-16T14:05:00Z")), ("ev1 window", e(0, invoked_utc="2026-10-16T12:20:00Z")), ("ev2 memory", lambda r: r["events"][1]["report"].update(max_memory_used_mb=820)),
                ("ev1 flip", e(0, full_to_partial=1)), ("ev1 p2f", e(0, partial_to_full=5)), ("ev2 sum", e(1, partial=1)), ("ev3 before partial", e(2, before_partial=1)), ("ev4 floor count", e(3, floor_day_accounts=868)),
                ("act5 hash", lambda r: r["act5"].update(history_keys_sha256="cd" * 32)), ("act5 keys", lambda r: r["act5"].update(history_keys=6000)), ("act5 held", lambda r: r["act5"].update(held_days_absent=False)),
                ("act5 other", lambda r: r["act5"].update(other_new_keys=1)), ("act5 onev", lambda r: r["act5"].update(history_one_version_all=False)), ("ledger", lambda r: r.update(ledger_closed=True)), ("extra", lambda r: r.update(z=1)))
        for label, fn in arms:
            r2 = copy.deepcopy(good)
            fn(r2)
            try:
                check_head(r2, PACKET_BLOB, ok[0], ok[1], True)
                check_tail(r2)
            except Fail:
                continue
            raise AssertionError("red arm passed: " + label)
        for fn, label in ((lambda: check_head(good, PACKET_BLOB, ok[0], ok[1], False), "no ledger"), (lambda: check_head(good, PACKET_BLOB, "UNSIGNED", ok[1], True), "coo half")):
            try:
                fn()
            except Fail:
                continue
            raise AssertionError("red arm passed: " + label)
    finally:
        BUILD_B64, PACKET_SHA, PACKET_BLOB = saved
    print("selftest: record clauses behave on a green arm and %d red arms (plus two head arms)" % len(arms))
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
