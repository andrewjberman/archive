"""IRPT_DASHBD round 128, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-260, the APPLY of the signed Cottonwood landing pair (packet revision 2, sha256 a1b080c5fe06...): ACT 1 the bundle build and upload and ONE safe-apply of the new root account-return-daily (plan exactly 7 add / 0 change / 0 destroy, the schedule
DISABLED), ACT 2 ONE synchronous event {"day": "2026-07-10"}; the ledger left OPEN for the issuer and for Act 3.

  DB-b-260 (0.7.0_AE_CloudOps~DB2)  DBC128-1-AC1 (the record: gates, ledger, before, build, plan),
                                    DBC128-2-AC1 (FRESH live reads: function, concurrency, role policy, schedule, artifact),
                                    DBC128-3-AC1 (FRESH reads: the 2026-07-10 partition, the history untouched, the REPORT line, the ledger open)

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
REC_REL = D + "0.7.0_AE_CloudOps~DB2/COT_LANDING_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_ACCOUNT_RETURN_DAILY_LANDING_R2_CTO_HALF.md"
PACKET_SHA = "a1b080c5fe065f90f4ad356c95301e59437637e95ce40afade93726eeaa392df"
LEDGER_SLUG = "irpt-dashbd-cottonwood-account-return-daily-20261015"
PIN_COMMIT = "54e4a0036a"
FUNCTION = "irpt-cot-account-return-daily-lambda"
ROLE = "irpt-cot-account-return-daily-execution-role"
POLICY = "irpt-cot-account-return-daily-execution-policy"
SCHEDULE = "irpt-cot-account-return-daily-daily"
LOG_GROUP = "/aws/lambda/" + FUNCTION
LAYER = "irpt-performance-native-layer"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "investor-reporting/irpt-cot-account-return-daily-lambda.zip"
GOLD_BUCKET = "opal-data-cottonwood"
GOLD_PREFIX = "irpt/cottonwood/gold/account_return_daily/"
HISTORY_COUNT, HISTORY_LAST, FIRST_DAY = 3325, "2026-06-22", "2026-07-10"
CRON, ZONE = "cron(15 8 ? * MON-FRI *)", "America/New_York"
SIDS = sorted(["ListSilverTablePrefixesOnly", "ReadTwoBlackDiamondSilverTablesOnly", "WriteTheOneAccountReturnDailyGoldPrefixOnly", "ListTheOneAccountReturnDailyGoldPrefixOnly",
               "OwnLogStreamOnly"])
PLAN_ADDRESSES = sorted(["aws_cloudwatch_log_group.lambda", "aws_iam_role.irpt_account_return_daily_execution", "aws_iam_role.irpt_account_return_daily_scheduler",
                         "aws_iam_role_policy.irpt_account_return_daily_execution", "aws_iam_role_policy.irpt_account_return_daily_scheduler",
                         "aws_lambda_function.this", "aws_scheduler_schedule.irpt_account_return_daily"])
BUILD_B64 = "fQFe4moIeMHspIjLxO2C04TobQW6cNZc7mfwstcMWzs="
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "packet_blob", "landed_version_id", "version_id", "members", "code_sha256", "addresses", "ledger_entry", "apply_finished_utc",
                 "invoked_utc", "layer_arn", "packet_sha256", "zip_sha256", "zip_sha256_b64", "content_sha256", "request_id")


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
    exp = {"claim", "gates", "ledger_entry", "before", "build", "plan", "apply_finished_utc", "after", "event", "ledger_closed", "reads"}
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
         "one_change_at_a_time: the denominator (worktrees read) and zero markers naming this surface")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists, "the ledger entry %s must exist" % LEDGER_SLUG)
    b = rec["before"]
    need(isinstance(b, dict) and set(b) == {"function_exists", "role_exists", "schedule_exists", "artifact_exists", "gold_partitions", "gold_last_day"}, "before keys")
    need(b["function_exists"] is False and b["role_exists"] is False and b["schedule_exists"] is False and b["artifact_exists"] is False, "before: all four must be recorded absent, as the packet's section 3")
    need(b["gold_partitions"] == HISTORY_COUNT and b["gold_last_day"] == HISTORY_LAST, "before: the gold prefix must read %d partitions to %s" % (HISTORY_COUNT, HISTORY_LAST))
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == b64_of_hex(bd["zip_sha256"]), "build.zip_sha256 and its base64 form must agree")
    need(bd["zip_sha256_b64"] == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s, got %s" % (BUILD_B64, bd["zip_sha256_b64"]))
    need(isinstance(bd["members"], list) and len(bd["members"]) == 16 and "handler.py" in bd["members"], "the zip must hold 16 members incl. handler.py")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "the import smoke, the landed version or the built-equals-landed record")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "addresses", "replan_no_changes"}, "plan keys")
    need(p["add"] == 7 and p["change"] == 0 and p["destroy"] == 0 and sorted(re.sub(r"^module\.[^.]+\.", "", str(a)) for a in p["addresses"]) == PLAN_ADDRESSES and p["replan_no_changes"] is True,
         "the plan must read 7 add / 0 change / 0 destroy on the seven addresses, and a post-apply plan with no changes")
    return True


def check_tail(rec):
    need(UTC.match(str(rec["apply_finished_utc"])), "apply_finished_utc must be an ISO UTC instant")
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy_sids", "schedule"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 900 and f.get("reserved_concurrency") == 1 and f.get("code_sha256") == rec["build"]["zip_sha256_b64"]
         and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"],
         "after.function: memory 1024, timeout 900, reserved concurrency 1, code hash equal to the landed zip's, and the layer ARN of %s" % LAYER)
    need(sorted(a["policy_sids"]) == SIDS and a["schedule"] == {"state": "DISABLED", "cron": CRON}, "after.policy_sids or after.schedule (DISABLED)")
    e = rec["event"]
    ek = {"payload", "invoked_utc", "invocation_type", "status_code", "function_error", "returned", "report", "partition", "over_717_mb", "request_id", "layer_pyarrow_version"}
    need(isinstance(e, dict) and set(e) == ek, "event keys differ: %s" % sorted(set(e) ^ ek) if isinstance(e, dict) else "event")
    need(e["payload"] == {"day": FIRST_DAY} and e["invocation_type"] == "RequestResponse" and e["status_code"] == 200 and e["function_error"] is None, "the event must be {day: %s}, synchronous, 200, no function error" % FIRST_DAY)
    need(UTC.match(str(e["invoked_utc"])) and e["invoked_utc"] >= rec["apply_finished_utc"], "invoked_utc must be an ISO UTC instant not before the apply finished")
    r = e["returned"]
    need(isinstance(r, dict) and r.get("ok") is True and r.get("days") == [FIRST_DAY] and r.get("held") == [], "the returned body must be ok, days [%s], nothing held: %s" % (FIRST_DAY, r))
    rp = e["report"]
    need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"} and is_int(rp["max_memory_used_mb"]) and rp["max_memory_used_mb"] > 0 and rp["memory_size_mb"] == 1024
         and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] < 900000, "report: Max Memory Used (int MB), duration under 900 s, memory size 1024")
    pa = e["partition"]
    need(isinstance(pa, dict) and set(pa) == {"day", "objects"} and pa["day"] == FIRST_DAY and sorted(pa["objects"]) == ["data.parquet", "manifest.json"], "partition: the two objects of %s" % FIRST_DAY)
    need(e["over_717_mb"] is (rp["max_memory_used_mb"] > 717), "over_717_mb must equal (Max Memory Used > 717)")
    need(nes(e["request_id"]), "request_id")
    need(isinstance(e["layer_pyarrow_version"], str) and re.fullmatch(r"\d+\.\d+\.\d+", e["layer_pyarrow_version"]), "layer_pyarrow_version must be the layer zip's pyarrow version, e.g. 14.0.2")
    need(rec["ledger_closed"] is False, "the ledger must stay OPEN")
    need(rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def live(root):
    import boto3
    lam, iam, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam"), boto3.client("s3")
    sch, logs = boto3.client("scheduler", region_name="us-east-1"), boto3.client("logs", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    sc = sch.get_schedule(Name=SCHEDULE)
    ver = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)
    objs, token = [], None
    while True:
        kw = {"Bucket": GOLD_BUCKET, "Prefix": GOLD_PREFIX}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        objs += [(o["Key"], o["LastModified"]) for o in r.get("Contents", [])]
        if not r.get("IsTruncated"):
            break
        token = r.get("NextContinuationToken")
    reports = []
    for ev in logs.filter_log_events(logGroupName=LOG_GROUP, filterPattern="REPORT").get("events", []):
        m = re.search(r"Duration: ([\d.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ev["message"], re.S)
        if m:
            reports.append((float(m.group(1)), int(m.group(2)), int(m.group(3))))
    put = [s for s in sts if "s3:PutObject" in (s["Action"] if isinstance(s["Action"], list) else [s["Action"]])]
    put_res = put[0]["Resource"] if len(put) == 1 else None
    layers = [x["Arn"] for x in cfg.get("Layers", [])]
    pyarrow_version = None
    if layers:
        lv = int(layers[0].rsplit(":", 1)[1])
        import tempfile
        import urllib.request
        import zipfile
        url = lam.get_layer_version(LayerName=LAYER, VersionNumber=lv)["Content"]["Location"]
        with tempfile.TemporaryDirectory() as td:
            zp = Path(td) / "layer.zip"
            urllib.request.urlretrieve(url, str(zp))
            with zipfile.ZipFile(zp) as z:
                names = [n for n in z.namelist() if re.fullmatch(r"python/pyarrow-[^/]*\.dist-info/METADATA", n)]
        m = re.fullmatch(r"python/pyarrow-(\d+\.\d+\.\d+)\.dist-info/METADATA", names[0]) if names else None
        pyarrow_version = m.group(1) if m else None
    return {"layers": layers, "pyarrow_version": pyarrow_version, "memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "handler": cfg["Handler"], "runtime": cfg["Runtime"], "role": cfg["Role"], "env": cfg.get("Environment"),
            "concurrency": conc, "sids": sorted(s.get("Sid", "") for s in sts), "put_resources": put_res, "n_put": len(put),
            "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")}, "artifact_version": ver.get("VersionId"),
            "objects": objs, "reports": reports}


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
    if cid == "DBC128-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time, all four resources absent before, history %d partitions to %s), ledger %s, build %s equals the packet's, plan 7/0/0 on the seven addresses" %
              (HISTORY_COUNT, HISTORY_LAST, LEDGER_SLUG, rec["build"]["zip_sha256"][:12]))
        return True
    check_tail(rec)
    lv = live(root)
    if cid == "DBC128-2-AC1":
        need(lv["memory"] == 1024 and lv["timeout"] == 900 and lv["handler"] == "handler.lambda_handler" and lv["runtime"] == "python3.12" and lv["role"].endswith("role/" + ROLE),
             "live function: memory %s timeout %s handler %s runtime %s role %s" % (lv["memory"], lv["timeout"], lv["handler"], lv["runtime"], lv["role"]))
        need(lv["concurrency"] == 1 and not (lv["env"] or {}).get("Variables"), "live function: reserved concurrency %s, environment %s" % (lv["concurrency"], lv["env"]))
        need(lv["code_sha256"] == rec["build"]["zip_sha256_b64"], "live CodeSha256 %s differs from the landed zip's %s" % (lv["code_sha256"], rec["build"]["zip_sha256_b64"]))
        need(len(lv["layers"]) == 1 and lv["layers"][0] == rec["after"]["function"]["layer_arn"] and (":layer:%s:" % LAYER) in lv["layers"][0], "live layers differ from the record: %s" % lv["layers"])
        need(lv["pyarrow_version"] == rec["event"]["layer_pyarrow_version"], "the layer zip's pyarrow version %s differs from the recorded %s" % (lv["pyarrow_version"], rec["event"]["layer_pyarrow_version"]))
        need(lv["sids"] == SIDS, "live policy sids differ: %s" % lv["sids"])
        need(lv["n_put"] == 1 and lv["put_resources"] in ("arn:aws:s3:::%s/%s*" % (GOLD_BUCKET, GOLD_PREFIX), ["arn:aws:s3:::%s/%s*" % (GOLD_BUCKET, GOLD_PREFIX)]),
             "the one PutObject statement must name the one gold prefix: %s" % lv["put_resources"])
        need(lv["schedule"] == {"state": "DISABLED", "cron": CRON, "zone": ZONE}, "live schedule differs: %s" % lv["schedule"])
        need(nes(lv["artifact_version"]) and lv["artifact_version"] == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
        print("OK: live: memory 1024, timeout 900, concurrency 1, no environment, CodeSha256 equals the landed zip's, five policy statements with one PutObject on the one gold prefix, schedule DISABLED")
        return True
    if cid == "DBC128-3-AC1":
        day_keys = sorted(k[len(GOLD_PREFIX):] for k, _ in lv["objects"] if k.startswith(GOLD_PREFIX + "date=" + FIRST_DAY + "/"))
        need(day_keys == ["date=%s/data.parquet" % FIRST_DAY, "date=%s/manifest.json" % FIRST_DAY], "the %s partition holds %s" % (FIRST_DAY, day_keys))
        hist = [(k, t) for k, t in lv["objects"] if k[len(GOLD_PREFIX):len(GOLD_PREFIX) + 15] <= "date=" + HISTORY_LAST + "~"]
        days = {k[len(GOLD_PREFIX) + 5:len(GOLD_PREFIX) + 15] for k, _ in hist}
        need(len(days) == HISTORY_COUNT and max(days) == HISTORY_LAST, "history: %d partitions to %s expected, read %d to %s" % (HISTORY_COUNT, HISTORY_LAST, len(days), max(days)))
        touched = [k for k, t in hist if t.strftime("%Y-%m-%dT%H:%M:%SZ") >= rec["apply_finished_utc"]]
        need(not touched, "history keys modified after the apply finished: %d" % len(touched))
        newer = sorted({k[len(GOLD_PREFIX) + 5:len(GOLD_PREFIX) + 15] for k, _ in lv["objects"]} - days)
        need(newer and newer[0] == FIRST_DAY and all(d >= FIRST_DAY for d in newer), "partitions after history must start at %s: %s" % (FIRST_DAY, newer[:3]))
        rp = rec["event"]["report"]
        match = [r for r in lv["reports"] if r[2] == rp["max_memory_used_mb"] and abs(r[0] - rp["duration_ms"]) < 1.0 and r[1] == 1024]
        need(match, "no REPORT line in the log group equals the record (Max Memory Used %s, duration %s)" % (rp["max_memory_used_mb"], rp["duration_ms"]))
        need((root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file(), "the ledger's open marker is missing: the ledger must stay OPEN")
        print("OK: partition %s holds its two objects; history %d partitions to %s untouched since the apply; %d later partition(s) from %s; a REPORT line equals the record (Max Memory Used %s MB); ledger open" %
              (FIRST_DAY, len(days), HISTORY_LAST, len(newer), newer[0], rp["max_memory_used_mb"]))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    zh = base64.b64decode(BUILD_B64).hex()
    good = {"claim": "measured", "gates": {"packet_blob": "blob1", "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
            "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True}, "ledger_entry": LEDGER_SLUG,
            "before": {"function_exists": False, "role_exists": False, "schedule_exists": False, "artifact_exists": False, "gold_partitions": HISTORY_COUNT, "gold_last_day": HISTORY_LAST},
            "build": {"zip_sha256": zh, "zip_sha256_b64": BUILD_B64, "members": ["handler.py"] + ["m%d" % i for i in range(15)], "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": zh,
                      "built_equals_landed": True},
            "plan": {"add": 7, "change": 0, "destroy": 0, "addresses": list(PLAN_ADDRESSES), "replan_no_changes": True}, "apply_finished_utc": "2026-10-16T01:00:00Z",
            "after": {"function": {"memory": 1024, "timeout": 900, "reserved_concurrency": 1, "code_sha256": BUILD_B64, "layer_arn": "arn:aws:lambda:us-east-1:313476888478:layer:%s:1" % LAYER}, "policy_sids": list(SIDS), "schedule": {"state": "DISABLED", "cron": CRON}},
            "event": {"payload": {"day": FIRST_DAY}, "invoked_utc": "2026-10-16T01:05:00Z", "invocation_type": "RequestResponse", "status_code": 200, "function_error": None,
                      "returned": {"ok": True, "days": [FIRST_DAY], "held": []}, "report": {"max_memory_used_mb": 640, "duration_ms": 21000.5, "memory_size_mb": 1024},
                      "partition": {"day": FIRST_DAY, "objects": ["data.parquet", "manifest.json"]}, "over_717_mb": False, "request_id": "abc", "layer_pyarrow_version": "14.0.2"},
            "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    coo, cto = "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12]

    def grade(r, blob="blob1", ledger=True, c=coo, t=cto):
        try:
            check_head(r, blob, c, t, ledger)
            check_tail(r)
            return True
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    full = copy.deepcopy(good)
    full["plan"]["addresses"] = [("module.irpt_account_return_daily." + a) if a.startswith(("aws_lambda_function", "aws_cloudwatch")) else a for a in good["plan"]["addresses"]]
    assert grade(full) is True
    arms = (("plan add", lambda r: r["plan"].update(add=6)), ("plan change", lambda r: r["plan"].update(change=1)), ("plan destroy", lambda r: r["plan"].update(destroy=1)),
            ("address", lambda r: r["plan"]["addresses"].pop()), ("replan", lambda r: r["plan"].update(replan_no_changes=False)),
            ("memory after", lambda r: r["after"]["function"].update(memory=8192)), ("concurrency", lambda r: r["after"]["function"].update(reserved_concurrency=2)),
            ("code hash", lambda r: r["after"]["function"].update(code_sha256="x")), ("sids", lambda r: r["after"]["policy_sids"].pop()),
            ("schedule enabled", lambda r: r["after"]["schedule"].update(state="ENABLED")), ("build sha", lambda r: r["build"].update(zip_sha256_b64=b64_of_hex("00" * 32), zip_sha256="00" * 32, content_sha256="00" * 32)),
            ("members", lambda r: r["build"].update(members=["handler.py"])), ("smoke", lambda r: r["build"].update(import_smoke_rc=1)), ("not equal", lambda r: r["build"].update(built_equals_landed=False)),
            ("before function", lambda r: r["before"].update(function_exists=True)), ("before count", lambda r: r["before"].update(gold_partitions=3324)),
            ("denominator", lambda r: r["gates"]["one_change_at_a_time"].update(worktrees_read=0)), ("marker", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1)),
            ("ledger closed", lambda r: r.update(ledger_closed=True)), ("extra key", lambda r: r.update(z=1)), ("utc", lambda r: r.update(apply_finished_utc="soon")),
            ("layer arn", lambda r: r["after"]["function"].update(layer_arn="arn:aws:lambda:us-east-1:313476888478:layer:other:1")), ("pyarrow version", lambda r: r["event"].update(layer_pyarrow_version="14")),
            ("payload", lambda r: r["event"].update(payload={"day": "2026-06-22"})), ("payload days", lambda r: r["event"].update(payload={"days": [FIRST_DAY]})),
            ("async", lambda r: r["event"].update(invocation_type="Event")), ("function error", lambda r: r["event"].update(function_error="Unhandled")),
            ("held", lambda r: r["event"]["returned"].update(held=[FIRST_DAY])), ("status", lambda r: r["event"].update(status_code=500)),
            ("memory size", lambda r: r["event"]["report"].update(memory_size_mb=8192)), ("over flag", lambda r: r["event"].update(over_717_mb=True)),
            ("objects", lambda r: r["event"]["partition"].update(objects=["data.parquet"])), ("invoked before apply", lambda r: r["event"].update(invoked_utc="2026-10-16T00:00:00Z")),
            ("digits", lambda r: r["event"]["returned"].update(note="id 1234567890")))
    for name, f in arms:
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False, "red arm %s passed" % name
    r = copy.deepcopy(good)
    r["event"]["report"]["max_memory_used_mb"] = 800
    r["event"]["over_717_mb"] = True
    assert grade(r) is True
    assert grade(copy.deepcopy(good), blob="other") is False and grade(copy.deepcopy(good), ledger=False) is False
    assert grade(copy.deepcopy(good), c="DRAFT " + PACKET_SHA) is False and grade(copy.deepcopy(good), t="SIGNED deadbeef0000") is False
    print("selftest: two green and %d red record arms behave" % (len(arms) + 4))


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
