"""IRPT_DASHBD round 139, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-272, the APPLY of the signed Cottonwood report-build pair (packet revision 2): ACT 1 the bundle build and upload and
ONE safe-apply of the new root reporting-gold-iso (7 add / 0 change / 0 destroy, the schedule DISABLED), ACT 2 ONE synchronous DRY-RUN event, ACTS 3 and 4 the backfill of the filled report values;
the ledger left OPEN for the issuer.

  DB-b-272 (0.7.0_AE_CloudOps~DB2)  DBC139-1-AC1 (the record: gates, ledger, before, build, plan),
                                    DBC139-2-AC1 (FRESH live reads: function, role policy, schedule, artifact, the layer's pyarrow),
                                    DBC139-3-AC1 (FRESH reads: the dry run left no object, the filled prefix holds the recorded days with the claim in each object, the REPORT lines, the ledger open)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the record clauses on synthetic arms
"""
import base64
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.7.0_AE_CloudOps~DB2/COT_REPORT_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_GOLD_LAMBDA.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_REPORTING_GOLD_LAMBDA_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_REPORTING_GOLD_LAMBDA_R2_CTO_HALF.md"
PACKET_SHA = "a9cdd5b207fe2f856570ec2a5899da50202caa3d71555e979a2f5fc609438d3d"
BUILD_B64 = "8pQOR3TN3iicEFV53N7Cs0yeensgZhPDd7zEwTZO3Z4="
LEDGER_SLUG = "irpt-dashbd-cottonwood-reporting-gold-20261015"
FUNCTION = "irpt-cot-reporting-gold-lambda"
ROLE = "irpt-cot-reporting-gold-execution-role"
POLICY = "irpt-cot-reporting-gold-execution-policy"
SCHEDULER_ROLE = "irpt-cot-reporting-gold-scheduler-role"
SCHEDULE = "irpt-cot-reporting-gold-daily"
LOG_GROUP = "/aws/lambda/" + FUNCTION
LAYER = "irpt-performance-native-layer"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "investor-reporting/irpt-cot-reporting-gold-lambda.zip"
GOLD_BUCKET = "opal-data-cottonwood"
FILLED_PREFIX = "irpt/cottonwood/gold/filled_report_values/"
CRON, ZONE = "cron(15 9 ? * MON-FRI *)", "America/New_York"
DRY_DAY = "2026-10-14"
ABSENT = ["2026-08-19", "2026-09-24", "2026-09-25"]
MAX_FILLED = 65
SIDS = sorted(["ListCottonwoodGoldInputsAndFilledOnly", "ReadCottonwoodGoldInputsOnly", "WriteTheFilledReportValuesPrefixOnly", "ReadBackTheFilledPrefixOnly",
               "ReadTheServedModelSeriesObjectOnly", "InvokeOwnFunctionOnly", "OwnLogStreamOnly"])
PLAN_ADDRESSES = sorted(["aws_cloudwatch_log_group.lambda", "aws_iam_role.irpt_reporting_gold_iso_execution", "aws_iam_role.irpt_reporting_gold_iso_scheduler",
                         "aws_iam_role_policy.irpt_reporting_gold_iso_execution", "aws_iam_role_policy.irpt_reporting_gold_iso_scheduler",
                         "aws_lambda_function.this", "aws_scheduler_schedule.irpt_reporting_gold_iso"])
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ISO_DAY = re.compile(r"\d{4}-\d{2}-\d{2}$")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "packet_blob", "landed_version_id", "version_id", "members", "code_sha256", "addresses", "ledger_entry", "apply_finished_utc",
                 "invoked_utc", "layer_arn", "packet_sha256", "zip_sha256", "zip_sha256_b64", "content_sha256", "request_id", "request_ids", "receipt_message_id")


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
    exp = {"claim", "gates", "ledger_entry", "before", "build", "plan", "apply_finished_utc", "after", "dry_run", "backfill", "receipt", "ledger_closed", "reads"}
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
    need(isinstance(b, dict) and set(b) == {"function_exists", "role_exists", "schedule_exists", "artifact_exists", "artifact_version_id", "filled_objects"}, "before keys")
    need(b["function_exists"] is False and b["role_exists"] is False and b["schedule_exists"] is False and isinstance(b["artifact_exists"], bool), "before: the function, both roles and the schedule must be recorded absent, as the packet's section 3")
    need((b["artifact_exists"] is False and b["artifact_version_id"] is None) or (b["artifact_exists"] is True and nes(b["artifact_version_id"])), "before: artifact_version_id must be null when the artifact is absent and a version id when it exists")
    need(b["filled_objects"] == 0, "before: the filled prefix must read 0 objects")
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == b64_of_hex(bd["zip_sha256"]), "build.zip_sha256 and its base64 form must agree")
    need(bd["zip_sha256_b64"] == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s, got %s" % (BUILD_B64, bd["zip_sha256_b64"]))
    need(isinstance(bd["members"], list) and len(bd["members"]) >= 19 and "handler.py" in bd["members"], "the zip must hold the handler and its 18 staged members")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "the import smoke, the landed version or the built-equals-landed record")
    need(b["artifact_exists"] is False or bd["landed_version_id"] == b["artifact_version_id"], "a pre-existing artifact must be reused, never uploaded again (landed version differs from before.artifact_version_id)")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "addresses", "replan_no_changes"}, "plan keys")
    need(p["add"] == 7 and p["change"] == 0 and p["destroy"] == 0 and sorted(re.sub(r"^module\.[^.]+\.", "", str(a)) for a in p["addresses"]) == PLAN_ADDRESSES and p["replan_no_changes"] is True,
         "the plan must read 7 add / 0 change / 0 destroy on the seven addresses, and a post-apply plan with no changes")
    return True


def check_claims(c, day):
    need(isinstance(c, dict) and set(c) == {"households_as_of", "households_claim", "accounts_dropped", "households_no_rows"}, "claim keys for %s" % day)
    need(ISO_DAY.match(str(c["households_as_of"])) and c["households_claim"] == "held" and is_int(c["accounts_dropped"]) and c["accounts_dropped"] >= 0
         and is_int(c["households_no_rows"]) and c["households_no_rows"] >= 0, "claim values for %s: as_of an ISO day, claim held, two non-negative counts" % day)


def check_tail(rec):
    need(UTC.match(str(rec["apply_finished_utc"])), "apply_finished_utc must be an ISO UTC instant")
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy_sids", "schedule"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 900 and f.get("reserved_concurrency") is None and f.get("code_sha256") == rec["build"]["zip_sha256_b64"]
         and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"],
         "after.function: memory 1024, timeout 900, NO reserved concurrency, code hash equal to the landed zip's, and the layer ARN of %s" % LAYER)
    need(sorted(a["policy_sids"]) == SIDS and a["schedule"] == {"state": "DISABLED", "cron": CRON}, "after.policy_sids or after.schedule (DISABLED)")
    e = rec["dry_run"]
    ek = {"payload", "invoked_utc", "invocation_type", "status_code", "function_error", "returned", "report", "objects_after", "over_717_mb", "request_id", "layer_pyarrow_version"}
    need(isinstance(e, dict) and set(e) == ek, "dry_run keys differ: %s" % sorted(set(e) ^ ek) if isinstance(e, dict) else "dry_run")
    need(e["payload"] == {"day": DRY_DAY, "dry_run": True} and e["invocation_type"] == "RequestResponse" and e["status_code"] == 200 and e["function_error"] is None,
         "the dry run must be {day: %s, dry_run: true}, synchronous, 200, no function error" % DRY_DAY)
    need(UTC.match(str(e["invoked_utc"])) and e["invoked_utc"] >= rec["apply_finished_utc"], "dry_run.invoked_utc must be an ISO UTC instant not before the apply finished")
    r = e["returned"]
    need(isinstance(r, dict) and r.get("day") == DRY_DAY and isinstance(r.get("result"), dict), "dry_run.returned must be the handler's body for %s" % DRY_DAY)
    res = r["result"]
    need(is_int(res.get("rows")) and res["rows"] > 0 and is_int(res.get("households")) and res["households"] > 0 and res.get("dry_run") is True, "dry run: rows and households above 0, dry_run true: %s" % res)
    need(res.get("returns_from") == "2026-07-10" and res.get("contract") == {"contract_version": "0.3.0", "method_version": 2}, "dry run: returns_from 2026-07-10 and the contract 0.3.0 / 2")
    need(res.get("unreported_days") == ABSENT and res.get("statement") == "3 trading days not reported by the source (%s)" % ", ".join(ABSENT), "dry run: the three absent days and the statement, exactly")
    check_claims({k: res.get(k) for k in ("households_as_of", "households_claim", "accounts_dropped", "households_no_rows")}, DRY_DAY)
    need(r.get("next") is None or ISO_DAY.match(str(r["next"])), "dry_run.returned.next")
    rp = e["report"]
    need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"} and is_int(rp["max_memory_used_mb"]) and rp["max_memory_used_mb"] > 0 and rp["memory_size_mb"] == 1024
         and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] < 900000, "dry_run.report: Max Memory Used (int MB), duration under 900 s, memory size 1024")
    need(e["objects_after"] == 0, "the dry run must leave 0 objects in the filled prefix")
    need(e["over_717_mb"] is (rp["max_memory_used_mb"] > 717), "over_717_mb must equal (Max Memory Used > 717)")
    need(rp["max_memory_used_mb"] <= 717, "the dry run read Max Memory Used above 717 MB: Act 3 may not start, and the record cannot carry a backfill")
    need(nes(e["request_id"]), "dry_run.request_id")
    need(isinstance(e["layer_pyarrow_version"], str) and re.fullmatch(r"\d+\.\d+\.\d+", e["layer_pyarrow_version"]), "layer_pyarrow_version must be the layer zip's pyarrow version, e.g. 14.0.2")
    bf = rec["backfill"]
    need(isinstance(bf, dict) and set(bf) == {"events", "final", "skipped", "counts"}, "backfill keys")
    ev = bf["events"]
    need(isinstance(ev, list) and len(ev) >= 1, "backfill.events must list at least the first real event")
    for i, x in enumerate(ev):
        need(isinstance(x, dict) and set(x) == {"payload", "invoked_utc", "status_code", "first_day", "chain_days", "max_memory_used_mb", "max_duration_ms", "request_ids"}, "backfill event %d keys" % i)
        need(x["payload"] == {} and x["status_code"] == 200 and UTC.match(str(x["invoked_utc"])) and x["invoked_utc"] >= e["invoked_utc"], "backfill event %d: payload {}, 200, after the dry run" % i)
        need(ISO_DAY.match(str(x["first_day"])) and is_int(x["chain_days"]) and 1 <= x["chain_days"] <= 10, "backfill event %d: first_day and chain_days (1 to 10)" % i)
        need(is_int(x["max_memory_used_mb"]) and 0 < x["max_memory_used_mb"] <= 717 and isinstance(x["max_duration_ms"], (int, float)) and 0 < x["max_duration_ms"] < 900000, "backfill event %d: memory at most 717 MB and each invocation under 900 s" % i)
        need(isinstance(x["request_ids"], list) and x["request_ids"] and all(nes(q) for q in x["request_ids"]), "backfill event %d: request_ids" % i)
    need(ev[0]["first_day"] == "2026-07-10", "the first real event must build the floor day 2026-07-10 first")
    fin = bf["final"]
    need(isinstance(fin, dict) and set(fin) == {"response", "objects"} and fin["response"] == "NOTHING_OWED" and is_int(fin["objects"]) and 1 <= fin["objects"] <= MAX_FILLED,
         "backfill.final: the last event reads NOTHING_OWED and the filled prefix holds 1 to %d objects" % MAX_FILLED)
    sk = bf["skipped"]
    need(isinstance(sk, list) and all(isinstance(s, dict) and set(s) == {"day", "reason"} and ISO_DAY.match(str(s["day"])) and nes(s["reason"]) for s in sk), "backfill.skipped entries: {day, reason}")
    allowed = set(ABSENT) | {"2026-07-10"}
    need(all(s["day"] in allowed for s in sk), "a day skipped other than the three absent days and 2026-07-10 is a STOP condition: %s" % [s["day"] for s in sk if s["day"] not in allowed])
    cn = bf["counts"]
    need(isinstance(cn, dict) and set(cn) == {"days_built", "accounts_dropped_total", "households_no_rows_max", "days_with_dropped_accounts"} and all(is_int(v) and v >= 0 for v in cn.values()), "backfill.counts: four non-negative integers (ids stay private)")
    need(cn["days_built"] == fin["objects"], "counts.days_built must equal final.objects")
    rc = rec["receipt"]
    need(isinstance(rc, dict) and set(rc) == {"to", "via", "text_has_not_a_page_render", "sent_utc", "receipt_message_id"} and rc["to"] == "1.0.0_SA_CTO~DELL1" and rc["via"] == "0.0.0_AB_MSTR~DELL2"
         and rc["text_has_not_a_page_render"] is True and UTC.match(str(rc["sent_utc"])) and nes(rc["receipt_message_id"]), "receipt: to CTO~DELL1 via the MSTR relay, saying NOT a page render")
    need(rc["sent_utc"] >= e["invoked_utc"], "the receipt follows the dry run")
    need(rec["ledger_closed"] is False, "the ledger must stay OPEN")
    need(rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def filter_events(logs, **kw):
    """All events of filter_log_events: a page may be empty and still carry a nextToken, so the loop follows the token (capped at 100 pages)."""
    out, tok = [], None
    for _ in range(100):
        a = dict(kw)
        if tok:
            a["nextToken"] = tok
        r = logs.filter_log_events(**a)
        out += r.get("events", [])
        tok = r.get("nextToken")
        if not tok:
            break
    return out


def live(root):
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
    metas = {}
    if objs:
        import pyarrow.parquet as pq
        for key, _t in sorted(objs)[:: max(1, len(objs) // 5)]:
            body = s3.get_object(Bucket=GOLD_BUCKET, Key=key)["Body"].read()
            md = pq.read_schema(io.BytesIO(body)).metadata or {}
            metas[key] = {k.decode(): v.decode() for k, v in md.items() if k.decode().startswith("households_")}
    reports = []
    for ev in filter_events(logs, logGroupName=LOG_GROUP, filterPattern="REPORT"):
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
    return {"layers": layers, "pyarrow_version": pyarrow_version, "memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "handler": cfg["Handler"],
            "runtime": cfg["Runtime"], "role": cfg["Role"], "env": cfg.get("Environment"), "concurrency": conc, "sids": sorted(s.get("Sid", "") for s in sts), "put_resources": put_res,
            "n_put": len(put), "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")}, "artifact_version": ver.get("VersionId"),
            "objects": objs, "metas": metas, "reports": reports}


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
    if cid == "DBC139-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time, function, both roles, schedule absent and the filled prefix empty before), ledger %s, build %s equals the packet's, plan 7/0/0 on the seven addresses" %
              (LEDGER_SLUG, rec["build"]["zip_sha256"][:12]))
        return True
    check_tail(rec)
    lv = live(root)
    if cid == "DBC139-2-AC1":
        need(lv["memory"] == 1024 and lv["timeout"] == 900 and lv["handler"] == "handler.lambda_handler" and lv["runtime"] == "python3.12" and lv["role"].endswith("role/" + ROLE),
             "live function: memory %s timeout %s handler %s runtime %s role %s" % (lv["memory"], lv["timeout"], lv["handler"], lv["runtime"], lv["role"]))
        need(lv["concurrency"] is None and not (lv["env"] or {}).get("Variables"), "live function: no reserved concurrency (the chain needs it) and no environment, read %s / %s" % (lv["concurrency"], lv["env"]))
        need(lv["code_sha256"] == rec["build"]["zip_sha256_b64"], "live CodeSha256 %s differs from the landed zip's %s" % (lv["code_sha256"], rec["build"]["zip_sha256_b64"]))
        need(len(lv["layers"]) == 1 and lv["layers"][0] == rec["after"]["function"]["layer_arn"] and (":layer:%s:" % LAYER) in lv["layers"][0], "live layers differ from the record: %s" % lv["layers"])
        need(lv["pyarrow_version"] == rec["dry_run"]["layer_pyarrow_version"], "the layer zip's pyarrow version %s differs from the recorded %s" % (lv["pyarrow_version"], rec["dry_run"]["layer_pyarrow_version"]))
        need(lv["sids"] == SIDS, "live policy sids differ: %s" % lv["sids"])
        want = "arn:aws:s3:::%s/%sfilled_report_values/*" % (GOLD_BUCKET, "irpt/cottonwood/gold/")
        need(lv["n_put"] == 1 and lv["put_resources"] in (want, [want]), "the one PutObject statement must name the one filled prefix: %s" % lv["put_resources"])
        need(lv["schedule"] == {"state": "DISABLED", "cron": CRON, "zone": ZONE}, "live schedule differs: %s" % lv["schedule"])
        need(nes(lv["artifact_version"]) and lv["artifact_version"] == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
        print("OK: live: memory 1024, timeout 900, no reserved concurrency, no environment, CodeSha256 equals the landed zip's, seven policy statements with one PutObject on the one filled prefix, schedule DISABLED, layer pyarrow %s" % lv["pyarrow_version"])
        return True
    if cid == "DBC139-3-AC1":
        days = sorted(k[len(FILLED_PREFIX) + 5:len(FILLED_PREFIX) + 15] for k, _ in lv["objects"] if k.endswith("/data.parquet"))
        need(len(lv["objects"]) == len(days) == rec["backfill"]["final"]["objects"], "the filled prefix holds %d objects (%d data.parquet), the record says %d" % (len(lv["objects"]), len(days), rec["backfill"]["final"]["objects"]))
        need(all(ISO_DAY.match(d) for d in days) and "2026-07-10" <= days[0] and days[-1] <= DRY_DAY, "the filled days must lie in 2026-07-10 to %s: %s to %s" % (DRY_DAY, days[:1], days[-1:]))
        need(not (set(days) & set(ABSENT)), "a source-absent day was filled: %s" % sorted(set(days) & set(ABSENT)))
        first_put = min(t for _, t in lv["objects"]).strftime("%Y-%m-%dT%H:%M:%SZ")
        need(first_put >= rec["backfill"]["events"][0]["invoked_utc"], "an object is older than the first real event: the dry run (or something else) wrote")
        need(lv["metas"] and all(m.get("households_claim") == "held" and ISO_DAY.match(m.get("households_as_of", "")) for m in lv["metas"].values()),
             "every sampled object must carry households_as_of and households_claim held in its schema metadata: %s" % lv["metas"])
        rp = rec["dry_run"]["report"]
        need([r for r in lv["reports"] if r[2] == rp["max_memory_used_mb"] and abs(r[0] - rp["duration_ms"]) < 1.0 and r[1] == 1024], "no REPORT line in the log group equals the dry run's (Max Memory Used %s, duration %s)" % (rp["max_memory_used_mb"], rp["duration_ms"]))
        need(not [r for r in lv["reports"] if r[2] > 717], "a REPORT line reads Max Memory Used above 717 MB")
        need((root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file(), "the ledger's open marker is missing: the ledger must stay OPEN")
        print("OK: the dry run left no object (the oldest object is not older than the first real event); %d filled days from %s to %s, none a source-absent day, %d sampled objects carry the held claim; a REPORT line equals the dry run's (Max Memory Used %s MB), none above 717; ledger open" %
              (len(days), days[0], days[-1], len(lv["metas"]), rp["max_memory_used_mb"]))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    zh = "ab" * 32
    global BUILD_B64, PACKET_SHA
    saved = (BUILD_B64, PACKET_SHA)
    BUILD_B64, PACKET_SHA = b64_of_hex(zh), "cc" * 32
    try:
        claim = {"households_as_of": "2026-10-14", "households_claim": "held", "accounts_dropped": 3, "households_no_rows": 1}
        good = {"claim": "measured", "gates": {"packet_blob": "blob1", "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
                "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True}, "ledger_entry": LEDGER_SLUG,
                "before": {"function_exists": False, "role_exists": False, "schedule_exists": False, "artifact_exists": False, "artifact_version_id": None, "filled_objects": 0},
                "build": {"zip_sha256": zh, "zip_sha256_b64": BUILD_B64, "members": ["handler.py"] + ["m%d" % i for i in range(18)], "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": zh,
                          "built_equals_landed": True},
                "plan": {"add": 7, "change": 0, "destroy": 0, "addresses": list(PLAN_ADDRESSES), "replan_no_changes": True}, "apply_finished_utc": "2026-10-16T01:00:00Z",
                "after": {"function": {"memory": 1024, "timeout": 900, "reserved_concurrency": None, "code_sha256": BUILD_B64, "layer_arn": "arn:aws:lambda:us-east-1:313476888478:layer:%s:1" % LAYER},
                          "policy_sids": list(SIDS), "schedule": {"state": "DISABLED", "cron": CRON}},
                "dry_run": {"payload": {"day": DRY_DAY, "dry_run": True}, "invoked_utc": "2026-10-16T01:05:00Z", "invocation_type": "RequestResponse", "status_code": 200, "function_error": None,
                            "returned": {"day": DRY_DAY, "next": None, "result": dict({"day": DRY_DAY, "rows": 10, "households": 5, "dry_run": True, "returns_from": "2026-07-10",
                                                                                   "contract": {"contract_version": "0.3.0", "method_version": 2}, "unreported_days": list(ABSENT),
                                                                                   "statement": "3 trading days not reported by the source (%s)" % ", ".join(ABSENT)}, **claim)},
                            "report": {"max_memory_used_mb": 640, "duration_ms": 21000.5, "memory_size_mb": 1024}, "objects_after": 0, "over_717_mb": False, "request_id": "abc", "layer_pyarrow_version": "14.0.2"},
                "backfill": {"events": [{"payload": {}, "invoked_utc": "2026-10-16T01:10:00Z", "status_code": 200, "first_day": "2026-07-10", "chain_days": 10, "max_memory_used_mb": 650, "max_duration_ms": 30000,
                                         "request_ids": ["r1", "r2"]}], "final": {"response": "NOTHING_OWED", "objects": 65},
                             "skipped": [{"day": "2026-08-19", "reason": "REFUSED: no rows"}], "counts": {"days_built": 65, "accounts_dropped_total": 12, "households_no_rows_max": 1, "days_with_dropped_accounts": 4}},
                "receipt": {"to": "1.0.0_SA_CTO~DELL1", "via": "0.0.0_AB_MSTR~DELL2", "text_has_not_a_page_render": True, "sent_utc": "2026-10-16T01:20:00Z", "receipt_message_id": "m1"},
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
        arms = (("plan add", lambda r: r["plan"].update(add=6)), ("plan change", lambda r: r["plan"].update(change=1)), ("plan destroy", lambda r: r["plan"].update(destroy=1)),
                ("address", lambda r: r["plan"]["addresses"].pop()), ("replan", lambda r: r["plan"].update(replan_no_changes=False)),
                ("memory after", lambda r: r["after"]["function"].update(memory=8192)), ("reserved concurrency set", lambda r: r["after"]["function"].update(reserved_concurrency=1)),
                ("code hash", lambda r: r["after"]["function"].update(code_sha256="x")), ("sids", lambda r: r["after"]["policy_sids"].pop()),
                ("schedule enabled", lambda r: r["after"]["schedule"].update(state="ENABLED")), ("build sha", lambda r: r["build"].update(zip_sha256_b64=b64_of_hex("00" * 32), zip_sha256="00" * 32, content_sha256="00" * 32)),
                ("members", lambda r: r["build"].update(members=["handler.py"])), ("smoke", lambda r: r["build"].update(import_smoke_rc=1)), ("not equal", lambda r: r["build"].update(built_equals_landed=False)),
                ("before function", lambda r: r["before"].update(function_exists=True)), ("before filled", lambda r: r["before"].update(filled_objects=3)),
                ("artifact version without artifact", lambda r: r["before"].update(artifact_version_id="v9")), ("reuploaded over existing", lambda r: r["before"].update(artifact_exists=True, artifact_version_id="v9")),
                ("denominator", lambda r: r["gates"]["one_change_at_a_time"].update(worktrees_read=0)), ("marker", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1)),
                ("ledger closed", lambda r: r.update(ledger_closed=True)), ("extra key", lambda r: r.update(z=1)), ("utc", lambda r: r.update(apply_finished_utc="soon")),
                ("layer arn", lambda r: r["after"]["function"].update(layer_arn="arn:aws:lambda:us-east-1:313476888478:layer:other:1")), ("pyarrow version", lambda r: r["dry_run"].update(layer_pyarrow_version="14")),
                ("dry payload no flag", lambda r: r["dry_run"].update(payload={"day": DRY_DAY})), ("dry async", lambda r: r["dry_run"].update(invocation_type="Event")),
                ("dry function error", lambda r: r["dry_run"].update(function_error="Unhandled")), ("dry status", lambda r: r["dry_run"].update(status_code=500)),
                ("dry wrote", lambda r: r["dry_run"].update(objects_after=1)), ("dry statement", lambda r: r["dry_run"]["returned"]["result"].update(statement="x")),
                ("dry unreported", lambda r: r["dry_run"]["returned"]["result"].update(unreported_days=ABSENT[:2])), ("dry not dry", lambda r: r["dry_run"]["returned"]["result"].update(dry_run=False)),
                ("dry claim", lambda r: r["dry_run"]["returned"]["result"].update(households_claim="measured")), ("dry claim missing", lambda r: r["dry_run"]["returned"]["result"].pop("accounts_dropped")),
                ("dry contract", lambda r: r["dry_run"]["returned"]["result"].update(contract={"contract_version": "0.4.0", "method_version": 2})),
                ("dry memory over", lambda r: (r["dry_run"]["report"].update(max_memory_used_mb=800), r["dry_run"].update(over_717_mb=True))),
                ("over flag", lambda r: r["dry_run"].update(over_717_mb=True)), ("dry before apply", lambda r: r["dry_run"].update(invoked_utc="2026-10-16T00:00:00Z")),
                ("event payload", lambda r: r["backfill"]["events"][0].update(payload={"day": "2026-10-14"})), ("event first day", lambda r: r["backfill"]["events"][0].update(first_day="2026-07-13")),
                ("event chain", lambda r: r["backfill"]["events"][0].update(chain_days=11)), ("event memory", lambda r: r["backfill"]["events"][0].update(max_memory_used_mb=718)),
                ("event before dry", lambda r: r["backfill"]["events"][0].update(invoked_utc="2026-10-16T01:00:00Z")), ("no events", lambda r: r["backfill"].update(events=[])),
                ("not finished", lambda r: r["backfill"]["final"].update(response="OWED")), ("too many objects", lambda r: r["backfill"]["final"].update(objects=66)),
                ("skipped other day", lambda r: r["backfill"]["skipped"].append({"day": "2026-08-20", "reason": "x"})), ("built mismatch", lambda r: r["backfill"]["counts"].update(days_built=64)),
                ("counts negative", lambda r: r["backfill"]["counts"].update(accounts_dropped_total=-1)), ("receipt to", lambda r: r["receipt"].update(to="1.0.0_SA_CTO~DELL2")),
                ("receipt page render", lambda r: r["receipt"].update(text_has_not_a_page_render=False)), ("receipt before dry", lambda r: r["receipt"].update(sent_utc="2026-10-16T01:00:00Z")),
                ("digits", lambda r: r["dry_run"]["returned"]["result"].update(note="id 1234567890")))
        for name, f in arms:
            r = copy.deepcopy(good)
            f(r)
            assert grade(r) is False, "red arm %s passed" % name
        r = copy.deepcopy(good)
        r["backfill"]["skipped"] = []
        assert grade(r) is True
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
