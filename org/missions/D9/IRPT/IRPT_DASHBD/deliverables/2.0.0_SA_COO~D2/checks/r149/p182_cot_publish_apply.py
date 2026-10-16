"""IRPT_DASHBD round 149, workstream COTPUBHOP2 (issuer 2.0.0_SA_COO~D2) -- DB-b-315, the APPLY of the signed never-widen pair for the Cottonwood reporting-publish function (packet sha256 584a774339a1, COO half and
CTO half signed; applier IB2): a NEW artifact version (publisher 0.4.0), ONE safe-apply (plan exactly 0 add / 1 change / 0 destroy: the function's CODE), the pre-write read with its STOP lines, one dry run, a ONE-account canary
and the FULL republish of the 939 series at the same keys. WORLD, and SERVED output moves. The record is the applier's; the checker re-reads the world.

  DBC182-1-AC1  the record's head: packet and halves, gates, ledger and applier, before, build, plan, the time rule
  DBC182-2-AC1  the pre-write read, the dry run, the canary and the full republish in the record, each inside its STOP lines
  DBC182-3-AC1  FRESH live reads: the function's code, the schedule (DISABLED), the artifact version, the 1,878 keys, and EVERY series and manifest (claim, publisher 0.4.0, the FULL count)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import base64
import copy
import hashlib
import importlib.util
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


H = helper("r147/p151_pubapply.py", "p151_helper_182")
G = helper("r149/p168_gold49f_apply.py", "p168_helper_182")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/COT_PUBLISH_HOP2_RECORD.json"
PD = D + "2.0.0_SA_COO~D2/"
PACKET_REL = PD + "NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_HOP2_HISTORY_SCOPE_REPUBLISH.md"
COO_HALF_REL = PD + "NEVER_WIDEN_COTTONWOOD_REPORTING_PUBLISH_HOP2_HISTORY_SCOPE_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_PUBLISH_040_REPUBLISH_CTO_HALF.md"
PACKET_SHA = "584a774339a15acac39defbab5919cb9a8400eeef98dd63aa10be46aeb0c9c36"
PACKET_BLOB = "008efedd5f08e7861d77ae3ea60b0d51d4782378"
BUILD_B64 = "vYNB1EBTU2qEIINxTnhYQBBBEHBYFId7lllrIJM3YRE="
BEFORE_CODE = "GagDGBNGmPsmYaJR1B7qG/TvaPdQU3LiVAh6c+wt6jo="
BEFORE_VERSION = "4wX9zhqX6x4x73i1vX1ADsXfv1LyDzRA"
LEDGER_SLUG = "irpt-dashbd-cottonwood-publish-hop2-scope-republish-20261016"
FUNCTION = "irpt-cot-reporting-publish-lambda"
SCHEDULE, CRON, ZONE = "irpt-cot-reporting-publish-daily", "cron(30 9 ? * MON-FRI *)", "America/New_York"
ARTIFACT_BUCKET, ARTIFACT_KEY = "opal-313476888478-lambda-artifacts", "investor-reporting/irpt-cot-reporting-publish-lambda.zip"
LAYER = "irpt-performance-native-layer"
PUBLISHED = 939
OBJECTS = {"series": 939, "manifest": 939}
MEM_LINE, DUR_LINE = 819, 720000
CANARY_CHECKS = ["validates_contract", "scope_full", "claim_inferred", "basis_present", "manifest_publisher_040", "prior_versions_kept", "series_size_equals_manifest"]
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("request_ids", "layer_arn")
in_window = G.in_window


def check_report(rp, label):
    need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"}, "%s: report keys" % label)
    need(is_int(rp["max_memory_used_mb"]) and rp["max_memory_used_mb"] <= MEM_LINE and rp["memory_size_mb"] == 1024 and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] <= DUR_LINE,
         "%s: Max Memory Used at most %d MB and duration at most %d ms (no resize inside this pair)" % (label, MEM_LINE, DUR_LINE))


def check_head(rec, packet_blob, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "build", "plan", "apply_finished_utc", "after", "pre_write", "dry_run", "canary", "full", "ledger_closed", "reads"}
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
    need(isinstance(b, dict) and set(b) == {"function_code_sha256", "artifact_version_id", "schedule", "objects", "history_scope_counts"}, "before keys")
    need(b["function_code_sha256"] == BEFORE_CODE and b["artifact_version_id"] == BEFORE_VERSION, "before: the live code hash and artifact version of the packet's section 3")
    need(b["schedule"] == {"state": "DISABLED", "cron": CRON}, "before.schedule: DISABLED at the cron")
    need(isinstance(b["objects"], dict) and set(b["objects"]) == {"series", "manifest", "other"} and b["objects"]["series"] == PUBLISHED and b["objects"]["manifest"] == PUBLISHED and is_int(b["objects"]["other"]), "before.objects: 939 series and 939 manifests")
    need(b["history_scope_counts"] == {"PARTIAL_HISTORY": PUBLISHED}, "before.history_scope_counts: all 939 PARTIAL_HISTORY")
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == G.b64_of_hex(bd["zip_sha256"]) == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s" % BUILD_B64)
    need(isinstance(bd["members"], list) and "handler.py" in bd["members"] and any(m.endswith("publisher.py") for m in bd["members"]), "the zip must hold the handler and the publisher")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["landed_version_id"] != BEFORE_VERSION and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "import smoke, a NEW landed version or built-equals-landed")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "change_addresses", "function_change_attributes", "replan_no_changes"}, "plan keys")
    strip = lambda a: re.sub(r"^module\.[^.]+\.", "", str(a))  # noqa: E731
    need(p["add"] == 0 and p["change"] == 1 and p["destroy"] == 0 and [strip(a) for a in p["change_addresses"]] == ["aws_lambda_function.this"] and p["replan_no_changes"] is True,
         "the plan must read 0 add / 1 change / 0 destroy on the function and a post-apply plan of No changes")
    fa = p["function_change_attributes"]
    need(isinstance(fa, list) and fa and set(fa) <= {"source_code_hash", "s3_object_version", "s3_key", "s3_bucket", "last_modified", "qualified_arn", "qualified_invoke_arn", "version", "source_code_size"}, "the function change must be by CODE attributes only: %s" % fa)
    t = rec["apply_finished_utc"]
    need(H.UTC.match(str(t)) and not in_window(t, "12:05", "12:45"), "the apply must be outside 12:05Z to 12:45Z on a trading weekday (the packet's condition 3)")
    return True


def check_body(rec):
    b, a = rec["before"], rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "schedule"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 900 and f.get("reserved_concurrency") is None and f.get("code_sha256") == rec["build"]["zip_sha256_b64"] and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"],
         "after.function: memory 1024, timeout 900, no reserved concurrency, the landed zip's code hash, the native layer")
    need(a["schedule"] == {"state": "DISABLED", "cron": CRON}, "after.schedule must stay DISABLED, untouched")
    pw = rec["pre_write"]
    keys = {"partial_to_full", "full_to_partial", "series_gaining_day", "changed_total_return_common", "changed_external_flow_common", "changed_value_common", "changed_income_common", "changed_price_return_common", "refused", "published_series"}
    need(isinstance(pw, dict) and set(pw) == keys and all(is_int(v) for v in pw.values()), "pre_write keys and integer counts")
    need(pw["published_series"] == PUBLISHED, "pre_write: the 939 published series")
    need(pw["full_to_partial"] == 0 and pw["partial_to_full"] <= 150, "pre_write STOP lines: no FULL to PARTIAL flip and at most 150 flips to FULL (got %s / %s)" % (pw["full_to_partial"], pw["partial_to_full"]))
    need(pw["changed_value_common"] == 0 and pw["changed_income_common"] == 0 and pw["changed_price_return_common"] == 0, "pre_write STOP lines: value, income and holdings_price_return unchanged on every common day")
    need(pw["changed_total_return_common"] <= 800 and pw["changed_external_flow_common"] <= 800 and pw["refused"] == 0, "pre_write STOP lines: at most 800 series with a changed daily return or flow, and 0 refused")
    d = rec["dry_run"]
    need(isinstance(d, dict) and set(d) == {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "request_id"}, "dry_run keys")
    need(d["payload"] == {} and d["status_code"] == 200 and d["function_error"] is None and H.UTC.match(str(d["invoked_utc"])) and d["invoked_utc"] >= rec["apply_finished_utc"] and not in_window(d["invoked_utc"], "12:05", "12:45"),
         "dry run: payload {}, 200, no error, after the apply, outside the landing fire window")
    r = d["returned"]
    need(isinstance(r, dict) and set(r) == {"uploaded", "published", "refused"} and r["uploaded"] is False and r["published"] == PUBLISHED and is_int(r["refused"]) and 0 <= r["refused"] <= (PUBLISHED + r["refused"]) // 10,
         "dry run: uploaded false, 939 published and refused inside the 10 percent line")
    check_report(d["report"], "dry_run")
    need(nes(d["request_id"]), "dry run: request id")
    c = rec["canary"]
    ck = {"payload_shape", "account_hash12", "invoked_utc", "status_code", "function_error", "returned", "report", "objects_after", "checks", "request_id"}
    need(isinstance(c, dict) and set(c) == ck, "canary keys differ")
    need(c["payload_shape"] == {"upload": True, "accounts": 1} and H.HEX12.match(str(c["account_hash12"])) and c["status_code"] == 200 and c["function_error"] is None and H.UTC.match(str(c["invoked_utc"])) and c["invoked_utc"] >= d["invoked_utc"],
         "canary: payload {upload, one account}, a hash prefix, 200, no error, after the dry run")
    need(c["returned"] == {"published": 1, "refused": 0} and c["objects_after"] == {"series": PUBLISHED, "manifest": PUBLISHED, "other": b["objects"]["other"]}, "canary: one account published, none refused, the prefix's object counts unchanged (same keys)")
    check_report(c["report"], "canary")
    need(isinstance(c["checks"], dict) and set(c["checks"]) == set(CANARY_CHECKS) and all(c["checks"][k] is True for k in CANARY_CHECKS) and nes(c["request_id"]), "canary checks: all true")
    fu = rec["full"]
    fk = {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "objects_after", "claim_count", "full_count", "partial_count", "changed_value_common_count", "prior_versions_kept", "sampled_hash12", "sample_checks_pass", "request_ids"}
    need(isinstance(fu, dict) and set(fu) == fk, "full keys differ: %s" % (sorted(set(fu) ^ fk) if isinstance(fu, dict) else "?"))
    need(fu["payload"] == {"upload": True} and fu["status_code"] == 200 and fu["function_error"] is None and H.UTC.match(str(fu["invoked_utc"])) and fu["invoked_utc"] >= c["invoked_utc"] and not in_window(fu["invoked_utc"], "12:05", "12:45"),
         "full: payload {upload: true}, 200, no error, after the canary, outside the landing fire window")
    need(fu["returned"] == {"published": PUBLISHED, "refused": r["refused"]}, "full: published equals the dry run's, refused equals the dry run's")
    check_report(fu["report"], "full")
    need(fu["objects_after"] == {"series": PUBLISHED, "manifest": PUBLISHED, "other": b["objects"]["other"]}, "full: series and manifests equal published and the other objects are unchanged")
    need(fu["claim_count"] == PUBLISHED and fu["full_count"] == pw["partial_to_full"] and fu["partial_count"] == PUBLISHED - pw["partial_to_full"], "full: every series carries the claim, and the FULL count equals the pre-write flips")
    need(fu["changed_value_common_count"] == 0 and fu["prior_versions_kept"] is True, "full: no series changed value on a common day against its prior version, and every prior version is present")
    need(isinstance(fu["sampled_hash12"], list) and len(fu["sampled_hash12"]) == 10 and all(H.HEX12.match(str(x)) for x in fu["sampled_hash12"]) and fu["sample_checks_pass"] is True and isinstance(fu["request_ids"], list) and fu["request_ids"], "full: ten sampled hash prefixes, the sample checks, request ids")
    need(isinstance(rec["ledger_closed"], bool) and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "ledger_closed boolean; reads block")
    return True


def digit_runs(rec):
    skip = {"zip_sha256", "zip_sha256_b64", "content_sha256", "landed_version_id", "request_id", "request_ids", "function_code_sha256", "code_sha256", "artifact_version_id", "invoked_utc", "apply_finished_utc",
            "packet_blob", "packet_sha256", "ledger_entry", "layer_arn", "sampled_hash12", "account_hash12"}
    out = []

    def walk(x, key=""):
        if isinstance(x, dict):
            for k, v in x.items():
                walk(v, k)
        elif isinstance(x, list):
            for v in x:
                walk(v, key)
        elif isinstance(x, str) and key not in skip and re.search(r"\d{8,}", x):
            out.append((key, x[:20]))
    walk(rec)
    return out


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
    if cid == "DBC182-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time), ledger %s, applier named, build %s equals the packet's and landed as a NEW version, plan 0 add / 1 change / 0 destroy on the function by code attributes only, the apply outside the landing fire window" % (LEDGER_SLUG, BUILD_B64[:8]))
        return True
    check_body(rec)
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    if cid == "DBC182-2-AC1":
        print("OK: the pre-write read sat inside its STOP lines, the dry run published 939 with refusals inside 10 percent, the canary showed the flip and passed seven checks, and the full republish kept 1,878 keys, put the claim on all 939 and a FULL count equal to the pre-write flips, with no value changed on a common day")
        return True
    import boto3
    lam, s3, sch = boto3.client("lambda", region_name="us-east-1"), boto3.client("s3"), boto3.client("scheduler", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    need(cfg["MemorySize"] == 1024 and cfg["Timeout"] == 900 and cfg["Handler"] == "handler.lambda_handler" and conc is None and not (cfg.get("Environment") or {}).get("Variables"), "live function: memory 1024, timeout 900, handler, no reserved concurrency, no environment variable")
    need(cfg["CodeSha256"] == rec["build"]["zip_sha256_b64"] != BEFORE_CODE and [x["Arn"] for x in cfg.get("Layers", [])] == [rec["after"]["function"]["layer_arn"]], "live CodeSha256 must equal the landed zip's, differ from the old, and the one layer unchanged")
    sc = sch.get_schedule(Name=SCHEDULE)
    need({"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")} == {"state": "DISABLED", "cron": CRON, "zone": ZONE}, "the schedule must stay DISABLED, untouched")
    need(s3.head_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY).get("VersionId") == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
    sys.path[:0] = [str(root / "infra/aws/lambda/investor-reporting"), str(root / "infra/aws/lambda/investor-reporting/reporting-publish"), str(root)]
    for m in ("handler", "publisher"):
        sys.modules.pop(m, None)
    import handler as h  # noqa: E402
    _b, mp, _u = h._published_map(s3, "cottonwood")
    raws = sorted(mp.values())
    need(len(raws) == PUBLISHED, "the published prefix must hold 939 accounts, it holds %d" % len(raws))

    def one(raw):
        doc = h._read_published(s3, "cottonwood", raw)
        return doc["series"].get("history_scope"), doc["series"].get("history_scope_claim"), doc["manifest"].get("publisher_version")
    with ThreadPoolExecutor(16) as pool:
        got = list(pool.map(one, raws))
    need(all(g[2] == "0.4.0" for g in got), "every manifest must read publisher_version 0.4.0 (found %s)" % sorted({str(g[2]) for g in got}))
    need(all(g[1] == "inferred" for g in got), "every series must carry history_scope_claim inferred (found %s)" % sorted({str(g[1]) for g in got}))
    full = sum(1 for g in got if g[0] == "FULL")
    need(full == rec["full"]["full_count"] and sum(1 for g in got if g[0] == "PARTIAL_HISTORY") == PUBLISHED - full, "the live FULL count %d differs from the record's %d" % (full, rec["full"]["full_count"]))
    print("OK: live: the function runs the NEW code with no environment variable; the schedule is DISABLED and untouched; the artifact's current version is the recorded one; all 939 series carry the claim, all 939 manifests read publisher 0.4.0, and the FULL count equals the record's")
    return True


# ------------------------------------------------------------------------------------------------ selftest
def synthetic():
    rp = {"max_memory_used_mb": 500, "duration_ms": 90000, "memory_size_mb": 1024}
    hx = base64.b64decode(BUILD_B64).hex()
    other = 0
    return {"claim": "measured",
            "gates": {"packet_blob": PACKET_BLOB, "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True, "one_change_at_a_time": {"worktrees_read": 4, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
            "ledger_entry": LEDGER_SLUG, "applier": APPLIER,
            "before": {"function_code_sha256": BEFORE_CODE, "artifact_version_id": BEFORE_VERSION, "schedule": {"state": "DISABLED", "cron": CRON}, "objects": {"series": 939, "manifest": 939, "other": other}, "history_scope_counts": {"PARTIAL_HISTORY": 939}},
            "build": {"zip_sha256": hx, "zip_sha256_b64": BUILD_B64, "members": ["handler.py", "infra/aws/lambda/investor-reporting/reporting-publish/publisher.py"], "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": hx, "built_equals_landed": True},
            "plan": {"add": 0, "change": 1, "destroy": 0, "change_addresses": ["module.x.aws_lambda_function.this"], "function_change_attributes": ["source_code_hash", "s3_object_version"], "replan_no_changes": True},
            "apply_finished_utc": "2026-10-16T23:10:00Z",
            "after": {"function": {"memory": 1024, "timeout": 900, "reserved_concurrency": None, "code_sha256": BUILD_B64, "layer_arn": "arn:aws:lambda:us-east-1:1:layer:%s:1" % LAYER}, "schedule": {"state": "DISABLED", "cron": CRON}},
            "pre_write": {"partial_to_full": 102, "full_to_partial": 0, "series_gaining_day": 826, "changed_total_return_common": 657, "changed_external_flow_common": 659, "changed_value_common": 0, "changed_income_common": 0,
                          "changed_price_return_common": 0, "refused": 0, "published_series": 939},
            "dry_run": {"payload": {}, "invoked_utc": "2026-10-16T23:20:00Z", "status_code": 200, "function_error": None, "returned": {"uploaded": False, "published": 939, "refused": 40}, "report": dict(rp), "request_id": "r1"},
            "canary": {"payload_shape": {"upload": True, "accounts": 1}, "account_hash12": "ab12cd34ef56", "invoked_utc": "2026-10-16T23:25:00Z", "status_code": 200, "function_error": None, "returned": {"published": 1, "refused": 0}, "report": dict(rp),
                       "objects_after": {"series": 939, "manifest": 939, "other": other}, "checks": {k: True for k in CANARY_CHECKS}, "request_id": "r2"},
            "full": {"payload": {"upload": True}, "invoked_utc": "2026-10-16T23:30:00Z", "status_code": 200, "function_error": None, "returned": {"published": 939, "refused": 40}, "report": dict(rp), "objects_after": {"series": 939, "manifest": 939, "other": other},
                     "claim_count": 939, "full_count": 102, "partial_count": 837, "changed_value_common_count": 0, "prior_versions_kept": True, "sampled_hash12": ["ab12cd34ef56"] * 10, "sample_checks_pass": True, "request_ids": ["r3"]},
            "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}


def selftest():
    rec = synthetic()
    ok = lambda r: (check_head(r, PACKET_BLOB, "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12], True), check_body(r))  # noqa: E731
    ok(rec)
    arms = {
        "claim": lambda r: r.update(claim="inferred"),
        "build hash": lambda r: r["build"].update(zip_sha256_b64="x" * 44),
        "plan change 2": lambda r: r["plan"].update(change=2),
        "plan address": lambda r: r["plan"].update(change_addresses=["module.x.aws_scheduler_schedule.y"]),
        "replan": lambda r: r["plan"].update(replan_no_changes=False),
        "apply window": lambda r: r.update(apply_finished_utc="2026-10-16T12:30:00Z"),
        "schedule enabled": lambda r: r["after"]["schedule"].update(state="ENABLED"),
        "memory": lambda r: r["after"]["function"].update(memory=3008),
        "before scope": lambda r: r["before"].update(history_scope_counts={"PARTIAL_HISTORY": 900, "FULL": 39}),
        "pre full_to_partial": lambda r: r["pre_write"].update(full_to_partial=1),
        "pre flips high": lambda r: r["pre_write"].update(partial_to_full=151),
        "pre value changed": lambda r: r["pre_write"].update(changed_value_common=1),
        "pre income changed": lambda r: r["pre_write"].update(changed_income_common=3),
        "pre returns high": lambda r: r["pre_write"].update(changed_total_return_common=801),
        "pre refused": lambda r: r["pre_write"].update(refused=1),
        "dry uploaded": lambda r: r["dry_run"]["returned"].update(uploaded=True),
        "dry published": lambda r: r["dry_run"]["returned"].update(published=938),
        "dry refused high": lambda r: r["dry_run"]["returned"].update(refused=200),
        "dry memory": lambda r: r["dry_run"]["report"].update(max_memory_used_mb=900),
        "dry duration": lambda r: r["dry_run"]["report"].update(duration_ms=800000),
        "dry payload": lambda r: r["dry_run"].update(payload={"upload": True}),
        "canary check false": lambda r: r["canary"]["checks"].update(scope_full=False),
        "canary two accounts": lambda r: r["canary"].update(returned={"published": 2, "refused": 0}),
        "canary order": lambda r: r["canary"].update(invoked_utc="2026-10-16T23:10:00Z"),
        "full payload": lambda r: r["full"].update(payload={}),
        "full objects": lambda r: r["full"]["objects_after"].update(series=938),
        "full claim": lambda r: r["full"].update(claim_count=938),
        "full count": lambda r: r["full"].update(full_count=101, partial_count=838),
        "full value changed": lambda r: r["full"].update(changed_value_common_count=2),
        "full versions": lambda r: r["full"].update(prior_versions_kept=False),
        "full sample": lambda r: r["full"].update(sampled_hash12=["ab12cd34ef56"] * 9),
        "reads": lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}),
        "ledger name": lambda r: r.update(ledger_entry="other"),
        "applier": lambda r: r.update(applier="0.7.0_AE_CloudOps~DB2"),
    }
    n = 0
    for label, mut in arms.items():
        r = copy.deepcopy(rec)
        mut(r)
        try:
            ok(r)
        except (Fail, KeyError, AssertionError):
            n += 1
            continue
        raise AssertionError("arm passed: " + label)
    print("selftest: record clauses behave on a green arm and %d red arms" % n)
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
