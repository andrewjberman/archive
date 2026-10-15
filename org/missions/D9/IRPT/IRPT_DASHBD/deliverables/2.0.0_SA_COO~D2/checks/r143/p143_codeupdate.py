"""IRPT_DASHBD round 143, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-276, the APPLY of the signed CODE-UPDATE pair for the chain cap (row IRPT_DASHBD-D2-S95): ACT 1 the build, the MEMBER DIFF against
LIVE (exactly handler.py) and ONE new version of the existing artifact key; ACT 2 ONE safe-apply at plan 0 add / 1 change / 0 destroy on the one function; ACT 3 three synchronous events that write nothing;
the r139 ledger closed after the after-read; the schedule left DISABLED.

  DB-b-276 (0.7.0_AE_CloudOps~DB2)  DBC143-1-AC1 (the record: gates, ledger, before, build and member diff, plan),
                                    DBC143-2-AC1 (FRESH live reads: the function, the artifact versions, the schedule),
                                    DBC143-3-AC1 (FRESH reads: the three events, the filled prefix still 65 and untouched, the REPORT lines, the ledger closed)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the record clauses on synthetic arms
"""
import base64
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.7.0_AE_CloudOps~DB2/COT_CODE_UPDATE_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_CODE_UPDATE_CHAIN_CAP.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_REPORTING_GOLD_CODE_UPDATE_CHAIN_CAP_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_REPORTING_GOLD_CODE_UPDATE_CHAIN_CAP_CTO_HALF.md"
PACKET_SHA = "0ba134ff507a525437ea18ca93d05f58963505cb8bc0b2454cbff789b044f6ae"
BUILD_B64 = "7FYx8sPkt0I25tZ8POS3HIueH0lJ99aGjppTky9E7DE="
LIVE_B64 = "8pQOR3TN3iicEFV53N7Cs0yeensgZhPDd7zEwTZO3Z4="
LEDGER_SLUG = "irpt-dashbd-cottonwood-reporting-gold-20261015"
PIN_COMMIT = "24b4b16305"
FUNCTION = "irpt-cot-reporting-gold-lambda"
ROLE = "irpt-cot-reporting-gold-execution-role"
SCHEDULE = "irpt-cot-reporting-gold-daily"
LOG_GROUP = "/aws/lambda/" + FUNCTION
LAYER = "irpt-performance-native-layer"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "investor-reporting/irpt-cot-reporting-gold-lambda.zip"
GOLD_BUCKET = "opal-data-cottonwood"
FILLED_PREFIX = "irpt/cottonwood/gold/filled_report_values/"
CRON, ZONE = "cron(15 9 ? * MON-FRI *)", "America/New_York"
ADDRESS = "aws_lambda_function.this"
ATTRS = ["s3_object_version", "source_code_hash"]
FILLED = 65
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "packet_blob", "landed_version_id", "version_id", "artifact_version_id", "members", "code_sha256", "addresses", "ledger_entry", "apply_finished_utc",
                 "invoked_utc", "layer_arn", "packet_sha256", "zip_sha256", "zip_sha256_b64", "content_sha256", "request_id", "differing", "gate_footprint")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def git(root, *a):
    return subprocess.run(["git", "-C", str(root)] + list(a), capture_output=True, text=True).stdout


def b64_of_hex(h):
    return base64.b64encode(bytes.fromhex(h)).decode("ascii")


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_head(rec, packet_blob, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "before", "build", "plan", "apply_finished_utc", "after", "events", "filled_after", "r139_ledger_closed", "gate_footprint_in_ledger", "reads"}
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
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and is_int(oc["worktrees_read"]) and oc["worktrees_read"] >= 1 and oc["open_markers_naming_this_surface"] == 0,
         "one_change_at_a_time: the denominator (worktrees read) and zero OTHER markers naming this surface")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists, "the ledger entry %s must exist" % LEDGER_SLUG)
    b = rec["before"]
    need(isinstance(b, dict) and set(b) == {"code_sha256", "artifact_version_id", "artifact_versions", "filled_objects", "schedule_state"}, "before keys")
    need(b["code_sha256"] == LIVE_B64 and nes(b["artifact_version_id"]) and b["artifact_versions"] == 1 and b["filled_objects"] == FILLED and b["schedule_state"] == "DISABLED",
         "before: the live CodeSha256 %s, one artifact version, %d filled objects, the schedule DISABLED" % (LIVE_B64, FILLED))
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "member_diff", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == b64_of_hex(bd["zip_sha256"]), "build.zip_sha256 and its base64 form must agree")
    need(bd["zip_sha256_b64"] == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s, got %s" % (BUILD_B64, bd["zip_sha256_b64"]))
    md = bd["member_diff"]
    need(isinstance(md, dict) and set(md) == {"live_members", "new_members", "differing"} and is_int(md["live_members"]) and md["live_members"] >= 19 and md["new_members"] == md["live_members"]
         and md["differing"] == ["handler.py"], "the member diff against LIVE must read the same member list and EXACTLY one differing member, handler.py: %s" % md)
    need(nes(bd["landed_version_id"]) and bd["landed_version_id"] != b["artifact_version_id"] and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True,
         "the landed version must be a NEW version (not the live one) holding the built bytes")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "addresses", "attributes", "replan_no_changes"}, "plan keys")
    need(p["add"] == 0 and p["change"] == 1 and p["destroy"] == 0 and isinstance(p["addresses"], list) and len(p["addresses"]) == 1 and re.sub(r"^module\.[^.]+\.", "", str(p["addresses"][0])) == ADDRESS
         and sorted(p["attributes"]) == sorted(ATTRS) and p["replan_no_changes"] is True,
         "the plan must read 0 add / 1 change / 0 destroy on the one function, changing exactly %s, and a post-apply plan with no changes" % ATTRS)
    return True


def check_tail(rec):
    need(UTC.match(str(rec["apply_finished_utc"])), "apply_finished_utc must be an ISO UTC instant")
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "schedule"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 900 and f.get("reserved_concurrency") is None and f.get("handler") == "handler.lambda_handler" and f.get("runtime") == "python3.12"
         and f.get("code_sha256") == rec["build"]["zip_sha256_b64"] and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"] and f.get("environment") is None,
         "after.function: memory 1024, timeout 900, handler, runtime, NO reserved concurrency, NO environment, the one layer, code hash equal to the landed zip's")
    need(a["schedule"] == {"state": "DISABLED", "cron": CRON}, "after.schedule must read DISABLED")
    ev = rec["events"]
    need(isinstance(ev, dict) and set(ev) == {"empty", "landed_dry_run", "refused"}, "events must hold exactly empty, landed_dry_run and refused")
    base = {"payload", "invoked_utc", "invocation_type", "status_code", "function_error", "returned", "request_id"}
    for name, pay in (("empty", {}), ("landed_dry_run", {"day": "2026-10-14", "dry_run": True}), ("refused", {"day": "2026-10-14", "chain_left": 10})):
        e = ev[name]
        need(isinstance(e, dict) and set(e) == base | ({"max_memory_used_mb"} if name != "refused" else {"error_text"}), "event %s keys" % name)
        need(e["payload"] == pay and e["invocation_type"] == "RequestResponse" and e["status_code"] == 200 and nes(e["request_id"]), "event %s: the packet's payload, synchronous, status 200" % name)
        need(UTC.match(str(e["invoked_utc"])) and e["invoked_utc"] >= rec["apply_finished_utc"], "event %s: invoked after the apply finished" % name)
    need(ev["empty"]["function_error"] is None and isinstance(ev["empty"]["returned"], dict) and ev["empty"]["returned"].get("result", {}).get("skipped") == "NOTHING_OWED", "the empty event must read skipped NOTHING_OWED")
    d = ev["landed_dry_run"]
    need(d["function_error"] is None and isinstance(d["returned"], dict) and d["returned"].get("result", {}).get("skipped") == "LANDED" and not (d["returned"].get("chain") or {}).get("invoked"),
         "the dry run of the landed day must read skipped LANDED and chain nothing")
    r = ev["refused"]
    need(nes(r["function_error"]) and nes(r["error_text"]) and "chain_left" in r["error_text"] and "REFUSED" in r["error_text"], "the refused event must carry a function error naming chain_left and REFUSED")
    for name in ("empty", "landed_dry_run"):
        m = ev[name]["max_memory_used_mb"]
        need(is_int(m) and 0 < m <= 717, "event %s: Max Memory Used at most 717 MB" % name)
    fa = rec["filled_after"]
    need(isinstance(fa, dict) and set(fa) == {"objects", "newest_after_apply"} and fa["objects"] == FILLED and fa["newest_after_apply"] is False, "filled_after: %d objects and none newer than the apply" % FILLED)
    need(rec["r139_ledger_closed"] is True, "the r139 ledger must be closed after the after-read")
    need(rec["gate_footprint_in_ledger"] is True, "the gate footprint must be copied into the ledger before any worktree is removed")
    need(rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def live(root):
    import boto3
    lam, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("s3")
    sch, logs = boto3.client("scheduler", region_name="us-east-1"), boto3.client("logs", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    try:
        conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    except Exception:  # noqa: BLE001
        conc = None
    sc = sch.get_schedule(Name=SCHEDULE)
    vers = s3.list_object_versions(Bucket=ARTIFACT_BUCKET, Prefix=ARTIFACT_KEY).get("Versions", [])
    versions = [(v["VersionId"], v["IsLatest"]) for v in vers if v["Key"] == ARTIFACT_KEY]
    objs, token = [], None
    while True:
        kw = {"Bucket": GOLD_BUCKET, "Prefix": FILLED_PREFIX}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        objs += [(o["Key"], o["LastModified"]) for o in r.get("Contents", [])]
        if not r.get("IsTruncated"):
            break
        token = r.get("NextContinuationToken")
    reports, tok = [], None
    for _ in range(100):
        kw = {"logGroupName": LOG_GROUP, "filterPattern": "REPORT"}
        if tok:
            kw["nextToken"] = tok
        r = logs.filter_log_events(**kw)
        for ev in r.get("events", []):
            m = re.search(r"Max Memory Used: (\d+) MB", ev["message"])
            if m:
                reports.append(int(m.group(1)))
        tok = r.get("nextToken")
        if not tok:
            break
    return {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "handler": cfg["Handler"], "runtime": cfg["Runtime"], "role": cfg["Role"], "env": cfg.get("Environment"),
            "concurrency": conc, "layers": [x["Arn"] for x in cfg.get("Layers", [])], "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")},
            "versions": versions, "objects": objs, "reports": reports}


def run(root, cid):
    root = Path(root)
    rec = load(root, REC_REL)
    packet_blob = git(root, "hash-object", PACKET_REL).strip()
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8")
    need((root / CTO_HALF_REL).is_file(), "no CTO half")
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8")
    need(hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest() == PACKET_SHA, "the packet's bytes differ from the signed sha256")
    ledger_exists = bool(list((root / "org/critical_paths/change_management").glob("*%s*" % LEDGER_SLUG)))
    check_head(rec, packet_blob, coo, cto, ledger_exists)
    if cid == "DBC143-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time, live equals the packet), ledger %s, build %s equals the packet's, the member diff against LIVE reads handler.py only, plan 0/1/0 on the one function changing %s" %
              (LEDGER_SLUG, rec["build"]["zip_sha256"][:12], ATTRS))
        return True
    check_tail(rec)
    lv = live(root)
    if cid == "DBC143-2-AC1":
        need(lv["memory"] == 1024 and lv["timeout"] == 900 and lv["handler"] == "handler.lambda_handler" and lv["runtime"] == "python3.12" and lv["role"].endswith("role/" + ROLE), "live function: memory %s timeout %s handler %s runtime %s role %s" % (lv["memory"], lv["timeout"], lv["handler"], lv["runtime"], lv["role"]))
        need(lv["concurrency"] is None and not (lv["env"] or {}).get("Variables"), "live function: no reserved concurrency and no environment: %s / %s" % (lv["concurrency"], lv["env"]))
        need(lv["code_sha256"] == rec["build"]["zip_sha256_b64"] == BUILD_B64, "live CodeSha256 %s differs from the landed zip's %s" % (lv["code_sha256"], rec["build"]["zip_sha256_b64"]))
        need(len(lv["layers"]) == 1 and lv["layers"][0] == rec["after"]["function"]["layer_arn"] and (":layer:%s:" % LAYER) in lv["layers"][0], "live layers differ from the record: %s" % lv["layers"])
        need(lv["schedule"] == {"state": "DISABLED", "cron": CRON, "zone": ZONE}, "live schedule differs: %s" % lv["schedule"])
        ids = [v for v, _ in lv["versions"]]
        need(len(ids) >= 2 and rec["before"]["artifact_version_id"] in ids and rec["build"]["landed_version_id"] in ids, "the artifact key must hold both the previous version and the landed one (nothing deleted): %d versions" % len(ids))
        need([v for v, latest in lv["versions"] if latest] == [rec["build"]["landed_version_id"]], "the landed version must be the key's current one")
        print("OK: live: memory 1024, timeout 900, no reserved concurrency, no environment, CodeSha256 equals the landed zip's, the one layer, schedule DISABLED, the artifact key holds %d versions with the landed one current and the previous one kept" % len(ids))
        return True
    if cid == "DBC143-3-AC1":
        need(len(lv["objects"]) == FILLED, "the filled prefix holds %d objects, %d expected" % (len(lv["objects"]), FILLED))
        newer = [k for k, t in lv["objects"] if t.strftime("%Y-%m-%dT%H:%M:%SZ") >= rec["apply_finished_utc"]]
        need(not newer, "%d filled objects are newer than the apply: an event wrote" % len(newer))
        need(not [m for m in lv["reports"] if m > 717], "a REPORT line reads Max Memory Used above 717 MB")
        need(rec["events"]["empty"]["max_memory_used_mb"] in lv["reports"], "no REPORT line equals the empty event's recorded Max Memory Used")
        need(not (root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file(), "the r139 ledger's open marker still exists: the ledger must be closed after the after-read")
        print("OK: the three events read as the packet states (NOTHING_OWED, LANDED with no chain, one refused naming chain_left); the filled prefix still holds %d objects, none newer than the apply; no REPORT line above 717 MB; the r139 ledger is closed" % FILLED)
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    zh = "ab" * 32
    global BUILD_B64, PACKET_SHA
    saved = (BUILD_B64, PACKET_SHA)
    BUILD_B64, PACKET_SHA = b64_of_hex(zh), "cc" * 32
    try:
        ev = lambda pay, **kw: dict({"payload": pay, "invoked_utc": "2026-10-16T02:05:00Z", "invocation_type": "RequestResponse", "status_code": 200, "request_id": "abc"}, **kw)  # noqa: E731
        good = {"claim": "measured", "gates": {"packet_blob": "blob1", "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
                "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True}, "ledger_entry": LEDGER_SLUG,
                "before": {"code_sha256": LIVE_B64, "artifact_version_id": "v1", "artifact_versions": 1, "filled_objects": FILLED, "schedule_state": "DISABLED"},
                "build": {"zip_sha256": zh, "zip_sha256_b64": BUILD_B64, "member_diff": {"live_members": 19, "new_members": 19, "differing": ["handler.py"]}, "landed_version_id": "v2", "content_sha256": zh, "built_equals_landed": True},
                "plan": {"add": 0, "change": 1, "destroy": 0, "addresses": ["module.irpt_reporting_gold_iso." + ADDRESS], "attributes": list(ATTRS), "replan_no_changes": True}, "apply_finished_utc": "2026-10-16T02:00:00Z",
                "after": {"function": {"memory": 1024, "timeout": 900, "reserved_concurrency": None, "handler": "handler.lambda_handler", "runtime": "python3.12", "code_sha256": BUILD_B64,
                                       "layer_arn": "arn:aws:lambda:us-east-1:313476888478:layer:%s:1" % LAYER, "environment": None}, "schedule": {"state": "DISABLED", "cron": CRON}},
                "events": {"empty": ev({}, function_error=None, returned={"day": None, "result": {"day": None, "skipped": "NOTHING_OWED"}, "next": None}, max_memory_used_mb=300),
                           "landed_dry_run": ev({"day": "2026-10-14", "dry_run": True}, function_error=None, returned={"day": "2026-10-14", "result": {"skipped": "LANDED"}, "next": None}, max_memory_used_mb=310),
                           "refused": ev({"day": "2026-10-14", "chain_left": 10}, function_error="Unhandled", returned=None, error_text="SystemExit: REFUSED: chain_left must be an integer from 0 to 9")},
                "filled_after": {"objects": FILLED, "newest_after_apply": False}, "r139_ledger_closed": True, "gate_footprint_in_ledger": True, "reads": {"vendor_calls": 0, "secret_reads": 0}}
        coo, cto = "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12]

        def grade(r, blob="blob1", ledger=True, c=coo, t=cto):
            try:
                check_head(r, blob, c, t, ledger)
                check_tail(r)
                return True
            except Fail:
                return False
        assert grade(copy.deepcopy(good)) is True
        arms = (("plan add", lambda r: r["plan"].update(add=1)), ("plan change", lambda r: r["plan"].update(change=2)), ("plan destroy", lambda r: r["plan"].update(destroy=1)),
                ("address", lambda r: r["plan"].update(addresses=["aws_iam_role.x"])), ("two addresses", lambda r: r["plan"]["addresses"].append("aws_iam_role.x")), ("attributes", lambda r: r["plan"].update(attributes=["memory_size"])),
                ("replan", lambda r: r["plan"].update(replan_no_changes=False)), ("memory after", lambda r: r["after"]["function"].update(memory=2048)), ("reserved concurrency", lambda r: r["after"]["function"].update(reserved_concurrency=1)),
                ("code hash", lambda r: r["after"]["function"].update(code_sha256="x")), ("environment", lambda r: r["after"]["function"].update(environment={"A": "b"})), ("schedule enabled", lambda r: r["after"]["schedule"].update(state="ENABLED")),
                ("build sha", lambda r: r["build"].update(zip_sha256_b64=b64_of_hex("00" * 32), zip_sha256="00" * 32, content_sha256="00" * 32)), ("diff two members", lambda r: r["build"]["member_diff"].update(differing=["handler.py", "lib/x.py"])),
                ("diff other member", lambda r: r["build"]["member_diff"].update(differing=["lib/x.py"])), ("member lists differ", lambda r: r["build"]["member_diff"].update(new_members=20)),
                ("not a new version", lambda r: r["build"].update(landed_version_id="v1")), ("not equal", lambda r: r["build"].update(built_equals_landed=False)),
                ("before hash", lambda r: r["before"].update(code_sha256="x")), ("before versions", lambda r: r["before"].update(artifact_versions=2)), ("before filled", lambda r: r["before"].update(filled_objects=64)),
                ("before schedule", lambda r: r["before"].update(schedule_state="ENABLED")), ("denominator", lambda r: r["gates"]["one_change_at_a_time"].update(worktrees_read=0)),
                ("marker", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1)), ("extra key", lambda r: r.update(z=1)), ("utc", lambda r: r.update(apply_finished_utc="soon")),
                ("empty payload", lambda r: r["events"]["empty"].update(payload={"day": "2026-10-14"})), ("empty not owed", lambda r: r["events"]["empty"]["returned"]["result"].update(skipped="LANDED")),
                ("empty error", lambda r: r["events"]["empty"].update(function_error="Unhandled")), ("dry not landed", lambda r: r["events"]["landed_dry_run"]["returned"]["result"].update(skipped="X")),
                ("dry chains", lambda r: r["events"]["landed_dry_run"]["returned"].update(chain={"invoked": True})), ("refused no error", lambda r: r["events"]["refused"].update(function_error=None)),
                ("refused text", lambda r: r["events"]["refused"].update(error_text="boom")), ("refused payload", lambda r: r["events"]["refused"].update(payload={"day": "2026-10-14", "chain_left": 9})),
                ("event async", lambda r: r["events"]["empty"].update(invocation_type="Event")), ("event status", lambda r: r["events"]["empty"].update(status_code=500)),
                ("event before apply", lambda r: r["events"]["empty"].update(invoked_utc="2026-10-16T01:00:00Z")), ("memory over", lambda r: r["events"]["empty"].update(max_memory_used_mb=800)),
                ("filled count", lambda r: r["filled_after"].update(objects=66)), ("filled newer", lambda r: r["filled_after"].update(newest_after_apply=True)), ("ledger open", lambda r: r.update(r139_ledger_closed=False)),
                ("footprint", lambda r: r.update(gate_footprint_in_ledger=False)), ("digits", lambda r: r["events"]["refused"].update(error_text="REFUSED chain_left 1234567890")))
        for name, f in arms:
            r = copy.deepcopy(good)
            f(r)
            assert grade(r) is False, "red arm %s passed" % name
        assert grade(copy.deepcopy(good), blob="other") is False and grade(copy.deepcopy(good), ledger=False) is False
        assert grade(copy.deepcopy(good), c="DRAFT " + PACKET_SHA) is False and grade(copy.deepcopy(good), t="SIGNED deadbeef0000") is False
        print("selftest: one green and %d red record arms behave" % (len(arms) + 4))
    finally:
        BUILD_B64, PACKET_SHA = saved


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Exception as e:  # a failed live read (botocore ClientError and the like) is a FAIL, not a traceback
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
