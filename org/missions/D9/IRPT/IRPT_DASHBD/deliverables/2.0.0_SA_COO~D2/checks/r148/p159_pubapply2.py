"""IRPT_DASHBD round 149, workstream PUBLISH (issuer 2.0.0_SA_COO~D2) -- DB-b-291, the APPLY of the second signed never-widen pair for the Cottonwood series publish (packet sha256 77f0af99d2bb, COO half signed
@d20bc88608, CTO half to be signed): a NEW artifact version, ONE safe-apply (plan exactly 3 add / 1 change / 0 destroy: the schedule's role, policy and schedule DISABLED, and the function's CODE), a DRY-RUN event, a
ONE-ACCOUNT republish and the FULL republish of the 939 series (branch E of the first pair), and the read for row S104. WORLD. The record is the applier's; the checker re-reads the world.

  DBC159-1-AC1  the record's head: packet and halves, gates, ledger and applier, before, build, plan
  DBC159-2-AC1  FRESH live reads: the function's code, the schedule (DISABLED), the scheduler role's policy, the artifact version
  DBC159-3-AC1  the dry run, the canary and the full republish in the record, and FRESH reads of the prefix: objects, sampled series and manifests, prior versions kept, the REPORT lines, the open ledger

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import base64
import copy
import gzip
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def p151():
    spec = importlib.util.spec_from_file_location("p151_helper", str(HERE.parent / "r147" / "p151_pubapply.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["p151_helper"] = mod
    spec.loader.exec_module(mod)
    return mod


H = p151()
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = H.APPLIER
REC_REL = D + APPLIER + "/COT_PUBLISH_CODE_UPDATE_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_CODE_UPDATE_SCHEDULE_REPUBLISH.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_REPORTING_PUBLISH_CODE_UPDATE_SCHEDULE_REPUBLISH_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_REPORTING_PUBLISH_CODE_UPDATE_SCHEDULE_REPUBLISH_CTO_HALF.md"
PACKET_SHA = "77f0af99d2bb28cd49344df6cf63494e8185f04d6cc8fff65bf9c4f1f2d501b0"
BUILD_B64 = "GagDGBNGmPsmYaJR1B7qG/TvaPdQU3LiVAh6c+wt6jo="
BEFORE_CODE = "HDgIzQoXMyUNBxeyqgLXcplD1c01QwVsASRoMJbd4hk="
BEFORE_VERSION = "9s6sk2dVtf6Ygi2JOGUxtwuiSNXCfKDa"
LEDGER_SLUG = "irpt-dashbd-cottonwood-reporting-publish-codeupdate-20261016"
FUNCTION, ROLE, POLICY = H.FUNCTION, H.ROLE, H.POLICY
SCHED_ROLE, SCHED_POLICY = "irpt-cot-reporting-publish-scheduler-role", "irpt-cot-reporting-publish-scheduler-policy"
SCHEDULE = "irpt-cot-reporting-publish-daily"
CRON, ZONE = "cron(30 9 ? * MON-FRI *)", "America/New_York"
PLAN_ADDS = sorted(["aws_iam_role.irpt_reporting_publish_iso_scheduler", "aws_iam_role_policy.irpt_reporting_publish_iso_scheduler", "aws_scheduler_schedule.irpt_reporting_publish_iso"])
PLAN_CHANGE = "aws_lambda_function.this"
CAL_VALUES = ["pandas_market_calendars", "fallback_2010_2027"]
CHECKS = ["series_size_equals_manifest", "validates_contract", "pair_present", "unreported_equals_dry_run", "income_all_null", "income_claim_absent", "calendar_source_in_values", "manifest_firm_ok", "prior_versions_kept"]
HEX12 = H.HEX12
digit_runs = H.digit_runs
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("before",)


def b64_of_hex(h):
    return base64.b64encode(bytes.fromhex(h)).decode("ascii")


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_head(rec, packet_blob, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "build", "plan", "apply_finished_utc", "after", "dry_run", "canary", "full", "ledger_closed", "reads"}
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
    need(isinstance(b, dict) and set(b) == {"function_code_sha256", "artifact_version_id", "schedules", "platinum_reporting_objects"}, "before keys")
    need(b["function_code_sha256"] == BEFORE_CODE and b["artifact_version_id"] == BEFORE_VERSION and b["schedules"] == [] and is_int(b["platinum_reporting_objects"]) and b["platinum_reporting_objects"] >= 1878, "before: the first pair's code hash and artifact version, no schedule, at least 1,878 objects (the packet's section 3)")
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == b64_of_hex(bd["zip_sha256"]), "build.zip_sha256 and its base64 form must agree")
    need(bd["zip_sha256_b64"] == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s, got %s" % (BUILD_B64, bd["zip_sha256_b64"]))
    need(isinstance(bd["members"], list) and len(bd["members"]) >= 13 and "handler.py" in bd["members"], "the zip must hold the handler and its 12 staged members")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["landed_version_id"] != BEFORE_VERSION and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "the import smoke, a NEW landed version (not the old one) or the built-equals-landed record")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "addresses", "change_addresses", "function_change_attributes", "replan_no_changes"}, "plan keys")
    strip = lambda a: re.sub(r"^module\.[^.]+\.", "", str(a))  # noqa: E731
    need(p["add"] == 3 and p["change"] == 1 and p["destroy"] == 0 and sorted(strip(a) for a in p["addresses"]) == PLAN_ADDS and [strip(a) for a in p["change_addresses"]] == [PLAN_CHANGE] and p["replan_no_changes"] is True,
         "the plan must read 3 add / 1 change / 0 destroy: the three schedule resources added and aws_lambda_function.this changed, and a post-apply plan with no changes")
    fa = p["function_change_attributes"]
    need(isinstance(fa, list) and fa and all(isinstance(x, str) for x in fa) and set(fa) <= {"source_code_hash", "s3_object_version", "s3_key", "s3_bucket", "last_modified", "qualified_arn", "qualified_invoke_arn", "version", "source_code_size"}, "the function change must be by CODE attributes only: %s" % fa)
    return True


def check_tail(rec):
    need(H.UTC.match(str(rec["apply_finished_utc"])), "apply_finished_utc must be an ISO UTC instant")
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy_sids", "schedule", "scheduler_policy_sids"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 900 and f.get("reserved_concurrency") is None and f.get("code_sha256") == rec["build"]["zip_sha256_b64"] and nes(f.get("layer_arn")) and (":layer:%s:" % H.LAYER) in f["layer_arn"],
         "after.function: memory 1024, timeout 900, NO reserved concurrency, code hash equal to the landed zip's, the native layer")
    need(sorted(a["policy_sids"]) == H.SIDS and a["scheduler_policy_sids"] == ["InvokeThePublishFunctionOnly"], "after: the execution policy's five statements and the scheduler policy's one")
    need(a["schedule"] == {"state": "DISABLED", "cron": CRON, "zone": ZONE, "input": {"upload": True}}, "after.schedule must be DISABLED at the packet's cron with input {upload: true}")
    e = rec["dry_run"]
    ek = {"payload", "invoked_utc", "invocation_type", "status_code", "function_error", "returned", "report", "objects_after", "request_id"}
    need(isinstance(e, dict) and set(e) == ek, "dry_run keys differ")
    need(e["payload"] == {} and e["invocation_type"] == "RequestResponse" and e["status_code"] == 200 and e["function_error"] is None, "the dry run must be {}, synchronous, 200, no function error")
    need(H.UTC.match(str(e["invoked_utc"])) and e["invoked_utc"] >= rec["apply_finished_utc"], "dry_run.invoked_utc not before the apply finished")
    H.check_summary(e["returned"], "dry_run", False)
    H.check_report(e["report"], "dry_run")
    need(e["objects_after"] == rec["before"]["platinum_reporting_objects"] and nes(e["request_id"]), "the dry run must leave the prefix's object count unchanged")
    dr = e["returned"]
    c = rec["canary"]
    ck = {"payload_shape", "account_hash12", "invoked_utc", "status_code", "function_error", "returned", "report", "objects_after", "checks", "request_id"}
    need(isinstance(c, dict) and set(c) == ck, "canary keys differ")
    need(c["payload_shape"] == {"upload": True, "accounts": 1} and HEX12.match(str(c["account_hash12"])) and c["status_code"] == 200 and c["function_error"] is None, "canary: payload {upload true, one account}; only a hash prefix of the id")
    need(H.UTC.match(str(c["invoked_utc"])) and c["invoked_utc"] >= e["invoked_utc"], "canary.invoked_utc after the dry run")
    H.check_summary(c["returned"], "canary", True, named=1)
    need(c["returned"]["published"] == 1 and c["returned"]["refused"] == 0 and c["objects_after"] == rec["before"]["platinum_reporting_objects"], "canary: one account published, none refused, the prefix's object count unchanged (same keys)")
    H.check_report(c["report"], "canary")
    need(isinstance(c["checks"], dict) and set(c["checks"]) == set(CHECKS) | {"publisher_version"} and all(c["checks"][k] is True for k in CHECKS) and c["checks"]["publisher_version"] == "0.3.0", "canary checks: all true and publisher_version 0.3.0")
    need(nes(c["request_id"]), "canary.request_id")
    fu = rec["full"]
    fk = {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "objects_after", "sampled_hash12", "sample_checks_pass", "claim_count", "request_id"}
    need(isinstance(fu, dict) and set(fu) == fk, "full keys differ")
    need(fu["payload"] == {"upload": True} and fu["status_code"] == 200 and fu["function_error"] is None, "full: payload {upload: true}, 200, no function error")
    need(H.UTC.match(str(fu["invoked_utc"])) and fu["invoked_utc"] >= c["invoked_utc"], "full.invoked_utc after the canary")
    H.check_summary(fu["returned"], "full", True, named=dr["accounts_named"])
    need(fu["returned"]["published"] == dr["published"] and fu["returned"]["refused"] == dr["refused"] and fu["returned"]["unreported_trading_days"] == dr["unreported_trading_days"], "full: published, refused and the unreported list must equal the dry run's")
    need(fu["objects_after"] == 2 * fu["returned"]["published"], "full: objects_after must be 2 x published (a republish adds no key)")
    need(fu["claim_count"] == fu["returned"]["published"], "full: the count of series carrying the claim must equal published (the S104 read)")
    need(isinstance(fu["sampled_hash12"], list) and len(fu["sampled_hash12"]) == 10 and all(HEX12.match(str(h)) for h in fu["sampled_hash12"]) and fu["sample_checks_pass"] is True and nes(fu["request_id"]), "full: ten sampled hash prefixes and the sample checks passing")
    H.check_report(fu["report"], "full")
    need(rec["ledger_closed"] is False, "the ledger must stay OPEN")
    need(rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def live(root, rec):
    import boto3
    lam, iam, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam"), boto3.client("s3")
    sch, logs = boto3.client("scheduler", region_name="us-east-1"), boto3.client("logs", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    try:
        conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    except Exception:  # noqa: BLE001
        conc = None

    def sids_of(role, pol):
        doc = iam.get_role_policy(RoleName=role, PolicyName=pol)["PolicyDocument"]
        sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
        return sts
    ex, sp = sids_of(ROLE, POLICY), sids_of(SCHED_ROLE, SCHED_POLICY)
    put = [s for s in ex if "s3:PutObject" in (s["Action"] if isinstance(s["Action"], list) else [s["Action"]])]
    sc = sch.get_schedule(Name=SCHEDULE)
    ver = s3.head_object(Bucket=H.ARTIFACT_BUCKET, Key=H.ARTIFACT_KEY)
    objs = H.list_all(s3, H.BUCKET, H.PREFIX)
    gold_days = sorted({k[len(H.GOLD_PREFIX) + 5:len(H.GOLD_PREFIX) + 15] for k, _, _ in H.list_all(s3, H.BUCKET, H.GOLD_PREFIX) if k.endswith(".parquet")})
    reports, tok = [], None
    for _ in range(100):
        kw = {"logGroupName": H.LOG_GROUP, "filterPattern": "REPORT"}
        if tok:
            kw["nextToken"] = tok
        r = logs.filter_log_events(**kw)
        for ev in r.get("events", []):
            m = re.search(r"Duration: ([\d.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ev["message"], re.S)
            if m:
                reports.append((float(m.group(1)), int(m.group(2)), int(m.group(3))))
        tok = r.get("nextToken")
        if not tok:
            break
    accts = sorted({k[len(H.PREFIX):].split("/")[0][len("account="):] for k, _, _ in objs})
    pick = [accts[i] for i in range(0, len(accts), max(1, len(accts) // 10))][:10] if accts else []
    samples = []
    for a in pick:
        sb = s3.get_object(Bucket=H.BUCKET, Key="%saccount=%s/series.json.gz" % (H.PREFIX, a))["Body"].read()
        mb = s3.get_object(Bucket=H.BUCKET, Key="%saccount=%s/manifest.json" % (H.PREFIX, a))["Body"].read()
        vs = s3.list_object_versions(Bucket=H.BUCKET, Prefix="%saccount=%s/series.json.gz" % (H.PREFIX, a)).get("Versions", [])
        samples.append((a, sb, mb, len(vs)))
    claims = 0
    for a in accts:
        pass
    return {"layers": [x["Arn"] for x in cfg.get("Layers", [])], "memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "handler": cfg["Handler"], "runtime": cfg["Runtime"], "role": cfg["Role"],
            "env": cfg.get("Environment"), "concurrency": conc, "sids": sorted(s.get("Sid", "") for s in ex), "sched_sids": sorted(s.get("Sid", "") for s in sp), "n_put": len(put), "put_resources": put[0]["Resource"] if len(put) == 1 else None,
            "sched_actions": [s["Action"] for s in sp], "sched_resources": [s["Resource"] for s in sp], "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone"), "input": json.loads(sc["Target"].get("Input", "null"))},
            "schedule_target": sc["Target"]["Arn"], "artifact_version": ver.get("VersionId"), "objects": objs, "gold_days": gold_days, "reports": reports, "samples": samples, "claims": claims}


def check_sample(root, a, sb, mb, nver, rec):
    sys.path.insert(0, str(Path(root) / "infra/aws/lambda/investor-reporting/reporting-publish"))
    import publisher
    contract = json.loads((Path(root) / "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json").read_bytes().decode("utf-8"))
    s = json.loads(gzip.decompress(sb).decode("utf-8"))
    m = json.loads(mb.decode("utf-8"))
    h = hashlib.sha256(a.encode()).hexdigest()[:12]
    bad = publisher.validate_against_contract(s, m, contract)
    need(not bad, "sample %s: the document does not validate against series contract %s: %s" % (h, contract["contract_version"], bad[:2]))
    need(contract["contract_version"] == "0.3.2", "the repo series contract is not 0.3.2")
    need(m["byte_sizes"]["series.json.gz"] == len(sb) and m["publisher_version"] == "0.3.0" and m["account_id"] == a, "sample %s: manifest size, version or account" % h)
    need(m.get("calendar_source") in CAL_VALUES, "sample %s: manifest calendar_source %r outside its values" % (h, m.get("calendar_source")))
    need(s.get("income_claim") == "absent" and all(x is None for x in s["income"]), "sample %s: the series must carry income_claim absent beside all-null income" % h)
    need(s["unreported_trading_days_basis"] == H.FIXED, "sample %s: the basis" % h)
    want = [d for d in rec["dry_run"]["returned"]["unreported_trading_days"] if s["first_data_date"] < d <= s["as_of"] and d not in s["date"]]
    need(s["unreported_trading_days"] == want, "sample %s: unreported days differ from the dry run's list inside its window" % h)
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
    if cid == "DBC159-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time, the first pair's code hash and artifact version before, no schedule), ledger %s, applier named, build %s equals the packet's and landed as a NEW version, plan 3 add / 1 change / 0 destroy on the named addresses by code attributes only" % (LEDGER_SLUG, rec["build"]["zip_sha256"][:12]))
        return True
    check_tail(rec)
    lv = live(root, rec)
    if cid == "DBC159-2-AC1":
        need(lv["memory"] == 1024 and lv["timeout"] == 900 and lv["handler"] == "handler.lambda_handler" and lv["runtime"] == "python3.12" and lv["role"].endswith("role/" + ROLE), "live function: memory/timeout/handler/runtime/role")
        need(lv["concurrency"] is None and not (lv["env"] or {}).get("Variables"), "live function: no reserved concurrency, no environment")
        need(lv["code_sha256"] == rec["build"]["zip_sha256_b64"] != BEFORE_CODE, "live CodeSha256 must equal the landed zip's and differ from the first pair's")
        need(len(lv["layers"]) == 1 and lv["layers"][0] == rec["after"]["function"]["layer_arn"], "live layers differ from the record")
        need(lv["sids"] == H.SIDS and lv["n_put"] == 1, "live execution policy: the five statements and one PutObject")
        want = "arn:aws:s3:::%s/%s*" % (H.BUCKET, H.PREFIX)
        need(lv["put_resources"] in (want, [want]), "the one PutObject statement must name only the platinum reporting prefix: %s" % lv["put_resources"])
        need(lv["schedule"] == {"state": "DISABLED", "cron": CRON, "zone": ZONE, "input": {"upload": True}}, "live schedule differs: %s" % lv["schedule"])
        need(lv["schedule_target"].endswith(":function:" + FUNCTION), "the schedule's target must be the one function: %s" % lv["schedule_target"])
        need(lv["sched_sids"] == ["InvokeThePublishFunctionOnly"] and lv["sched_actions"] == [["lambda:InvokeFunction"]] or lv["sched_actions"] == ["lambda:InvokeFunction"], "the scheduler policy: one statement, lambda:InvokeFunction only: %s" % lv["sched_actions"])
        need(all(str(r).endswith(":function:" + FUNCTION) or r == [("arn:aws:lambda:us-east-1:%s" % "")] or FUNCTION in str(r) for r in lv["sched_resources"]), "the scheduler policy must name the one function ARN: %s" % lv["sched_resources"])
        need(nes(lv["artifact_version"]) and lv["artifact_version"] == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
        print("OK: live: the function runs the NEW code (CodeSha256 equals the landed zip's, not the first pair's); memory 1024, timeout 900, no reserved concurrency, no environment, one layer; the execution policy is unchanged (five statements, one PutObject on the platinum reporting prefix); the schedule is DISABLED at %s %s with input {upload: true} on the one function; the scheduler policy holds only lambda:InvokeFunction" % (CRON, ZONE))
        return True
    if cid == "DBC159-3-AC1":
        keys = [k for k, _, _ in lv["objects"]]
        n = rec["full"]["returned"]["published"]
        need(len(keys) == 2 * n == rec["full"]["objects_after"], "the prefix holds %d objects, the record says 2 x %d" % (len(keys), n))
        need(sum(1 for k in keys if k.endswith("/series.json.gz")) == n and sum(1 for k in keys if k.endswith("/manifest.json")) == n, "series and manifest counts must each equal published")
        need(not [k for k in keys if not (k.endswith("/series.json.gz") or k.endswith("/manifest.json"))], "an object other than a series or manifest sits in the prefix")
        need(max(t for _, t, _ in lv["objects"]).strftime("%Y-%m-%dT%H:%M:%SZ") >= rec["canary"]["invoked_utc"], "no object is newer than the canary: nothing was republished")
        sys.path.insert(0, str(root / "lib"))
        import datetime as dt
        import trading_calendar as tc
        last = rec["dry_run"]["returned"]["last"]
        cal = [d.isoformat() for d in tc.trading_days_between(dt.date.fromisoformat(H.FLOOR), dt.date.fromisoformat(last))]
        need(rec["dry_run"]["returned"]["unreported_trading_days"] == [d for d in cal if d not in set(lv["gold_days"])], "the dry run's unreported list differs from the calendar minus the live gold partitions")
        hs = [check_sample(root, a, sb, mb, nv, rec) for a, sb, mb, nv in lv["samples"]]
        need(len(hs) == 10 and hs == rec["full"]["sampled_hash12"], "the ten sampled accounts (by position) must equal the record's hash prefixes")
        rp = rec["dry_run"]["report"]
        need([r for r in lv["reports"] if r[2] == rp["max_memory_used_mb"] and abs(r[0] - rp["duration_ms"]) < 1.0 and r[1] == 1024], "no REPORT line in the log group equals the dry run's")
        need(not [r for r in lv["reports"] if r[2] > 717], "a REPORT line reads Max Memory Used above 717 MB")
        need((root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file(), "the ledger's open marker is missing: the ledger must stay OPEN")
        print("OK: the dry run left the prefix as it was; %d objects (%d series, %d manifests), no key added; ten sampled series validate against series contract 0.3.2, carry income_claim absent beside all-null income and the pair equal to the dry run's list, with a manifest at publisher 0.3.0 naming its calendar source and the prior version of each series key still present; a REPORT line equals the dry run's, none above 717 MB; ledger open" % (len(keys), n, n))
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
        rp = {"max_memory_used_mb": 300, "duration_ms": 5000.0, "memory_size_mb": 1024}

        def summ(up, named, pub, ref, reasons):
            return {"ok": True, "uploaded": up, "floor": H.FLOOR, "partitions": 65, "first": H.FLOOR, "last": "2026-10-14", "accounts_seen": 979, "accounts_named": named, "published": pub, "refused": ref,
                    "refusals": reasons, "skipped_null_account": 1, "unreported_trading_days": list(H.ABSENT), "seconds": 12.5}
        good = {"claim": "measured", "gates": {"packet_blob": "b" * 40, "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
                                               "one_change_at_a_time": {"worktrees_read": 5, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
                "ledger_entry": LEDGER_SLUG, "applier": APPLIER, "before": {"function_code_sha256": BEFORE_CODE, "artifact_version_id": BEFORE_VERSION, "schedules": [], "platinum_reporting_objects": 1878},
                "build": {"zip_sha256": zh, "zip_sha256_b64": b64_of_hex(zh), "members": ["handler.py"] + ["m%d" % i for i in range(12)], "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": zh, "built_equals_landed": True},
                "plan": {"add": 3, "change": 1, "destroy": 0, "addresses": list(PLAN_ADDS), "change_addresses": ["module.x." + PLAN_CHANGE], "function_change_attributes": ["source_code_hash", "s3_object_version"], "replan_no_changes": True},
                "apply_finished_utc": "2026-10-16T10:00:00Z",
                "after": {"function": {"memory": 1024, "timeout": 900, "reserved_concurrency": None, "code_sha256": b64_of_hex(zh), "layer_arn": "arn:aws:lambda:us-east-1:1:layer:%s:1" % H.LAYER}, "policy_sids": list(H.SIDS),
                          "schedule": {"state": "DISABLED", "cron": CRON, "zone": ZONE, "input": {"upload": True}}, "scheduler_policy_sids": ["InvokeThePublishFunctionOnly"]},
                "dry_run": {"payload": {}, "invoked_utc": "2026-10-16T10:01:00Z", "invocation_type": "RequestResponse", "status_code": 200, "function_error": None, "returned": summ(False, 979, 939, 40, {"no positive value": 40}),
                            "report": rp, "objects_after": 1878, "request_id": "r1"},
                "canary": {"payload_shape": {"upload": True, "accounts": 1}, "account_hash12": "abcdef012345", "invoked_utc": "2026-10-16T10:02:00Z", "status_code": 200, "function_error": None,
                           "returned": summ(True, 1, 1, 0, {}), "report": rp, "objects_after": 1878, "request_id": "r2", "checks": dict({k: True for k in CHECKS}, publisher_version="0.3.0")},
                "full": {"payload": {"upload": True}, "invoked_utc": "2026-10-16T10:03:00Z", "status_code": 200, "function_error": None, "returned": summ(True, 979, 939, 40, {"no positive value": 40}), "report": rp,
                         "objects_after": 1878, "sampled_hash12": ["%012x" % i for i in range(10)], "sample_checks_pass": True, "claim_count": 939, "request_id": "r3"},
                "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
        assert check_head(good, "b" * 40, "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12], True) and check_tail(good)
        arms = (("claim", lambda r: r.update(claim="inferred")), ("blob", lambda r: r["gates"].update(packet_blob="c" * 40)), ("cto", lambda r: r["gates"].update(cto_half_signed=False)), ("applier", lambda r: r.update(applier="x")),
                ("before code", lambda r: r["before"].update(function_code_sha256="z")), ("before schedule", lambda r: r["before"].update(schedules=["x"])), ("before objects", lambda r: r["before"].update(platinum_reporting_objects=10)),
                ("build hash", lambda r: r["build"].update(zip_sha256_b64="x")), ("same version", lambda r: r["build"].update(landed_version_id=BEFORE_VERSION)), ("plan add", lambda r: r["plan"].update(add=4)),
                ("plan change", lambda r: r["plan"].update(change=0)), ("plan destroy", lambda r: r["plan"].update(destroy=1)), ("plan change addr", lambda r: r["plan"].update(change_addresses=["x.aws_iam_role.y"])),
                ("plan attrs", lambda r: r["plan"].update(function_change_attributes=["memory_size"])), ("replan", lambda r: r["plan"].update(replan_no_changes=False)), ("memory", lambda r: r["after"]["function"].update(memory=512)),
                ("code stale", lambda r: r["after"]["function"].update(code_sha256="x")), ("schedule enabled", lambda r: r["after"]["schedule"].update(state="ENABLED")), ("schedule input", lambda r: r["after"]["schedule"].update(input={"upload": False})),
                ("sched sids", lambda r: r["after"].update(scheduler_policy_sids=["x"])), ("dry payload", lambda r: r["dry_run"].update(payload={"upload": True})), ("dry uploaded", lambda r: r["dry_run"]["returned"].update(uploaded=True)),
                ("dry objects", lambda r: r["dry_run"].update(objects_after=1879)), ("memory717", lambda r: r["dry_run"]["report"].update(max_memory_used_mb=800)), ("canary two", lambda r: r["canary"]["returned"].update(published=2)),
                ("canary objects", lambda r: r["canary"].update(objects_after=1880)), ("canary check", lambda r: r["canary"]["checks"].update(income_claim_absent=False)), ("canary version", lambda r: r["canary"]["checks"].update(publisher_version="0.2.0")),
                ("full published", lambda r: r["full"]["returned"].update(published=938)), ("full objects", lambda r: r["full"].update(objects_after=1877)), ("claim count", lambda r: r["full"].update(claim_count=900)),
                ("sample", lambda r: r["full"].update(sample_checks_pass=False)), ("order", lambda r: r["full"].update(invoked_utc="2026-10-16T10:00:30Z")), ("ledger", lambda r: r.update(ledger_closed=True)), ("extra", lambda r: r.update(z=1)))
        for label, fn in arms:
            r2 = copy.deepcopy(good)
            fn(r2)
            try:
                check_head(r2, "b" * 40, "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12], True)
                check_tail(r2)
            except Fail:
                continue
            raise AssertionError("red arm passed: " + label)
        red(lambda: check_head(good, "b" * 40, "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12], False), "no ledger")
        red(lambda: check_head(good, "b" * 40, "UNSIGNED", "SIGNED " + PACKET_SHA[:12], True), "coo half")
    finally:
        BUILD_B64, PACKET_SHA = saved
    print("selftest: record clauses behave on a green arm and %d red arms (plus two head arms)" % len(arms))
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
