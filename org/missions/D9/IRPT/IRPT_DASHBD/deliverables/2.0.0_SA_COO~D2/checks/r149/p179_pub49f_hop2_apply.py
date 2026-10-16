"""IRPT_DASHBD round 149, workstream PUB49FHOP2 (issuer 2.0.0_SA_COO~D2) -- DB-b-312, the APPLY of the signed never-widen pair for the 49 Financial reporting-publish function: the hop-2 READER code (switch OFF) and the
READ grant on the filled-report gold prefix (packet sha256 e6af7a92148d, COO half and CTO half signed; applier IB2): a NEW artifact version, ONE safe-apply (plan exactly 0 add / 2 change / 0 destroy: the function's CODE and the
role policy's two statements), the switch-OFF probe, one dry-run shard, the after-read. WORLD. The record is the applier's; the checker re-reads the world.

  DBC179-1-AC1  the record's head: packet and halves, gates, ledger and applier, before, build, plan, the time rule
  DBC179-2-AC1  FRESH live reads: the function's code, the policy (eight statements, two widened by the one prefix, six identical), the two schedules, the artifact version
  DBC179-3-AC1  the probe, the dry-run shard and the platinum object counts in the record

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
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


H = helper("r147/p151_pubapply.py", "p151_helper_179")
G = helper("r149/p168_gold49f_apply.py", "p168_helper_179")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/PUB49F_HOP2_READER_RECORD.json"
PD = D + "2.0.0_SA_COO~D2/"
PACKET_REL = PD + "NEVER_WIDEN_PACKET_49F_REPORTING_PUBLISH_HOP2_READER_CODE_AND_READ_GRANT.md"
COO_HALF_REL = PD + "NEVER_WIDEN_49F_REPORTING_PUBLISH_HOP2_READER_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_REPORTING_PUBLISH_HOP2_READER_READ_GRANT_CTO_HALF.md"
PACKET_SHA = "e6af7a92148dcaefcfd8375f7421751636429c1e7a19b1de738db4d712d9d698"
PACKET_BLOB = "c12b711739d8f5f2528ee05265543bc51a3d8ee3"
BUILD_B64 = "s/OKOv98j53aFJCLrBpYP8xh3oUcuWagn0vSHVBjhIM="
BEFORE_CODE = "SX0xYFZsxH4q6psJM56yAee9wRb6vrVUN4VrTV1ouU8="
BEFORE_VERSION = "41lfCmfJWyvHbzqC3VtGeHVm6VJ4gRZb"
LEDGER_SLUG = "irpt-dashbd-49f-publish-hop2-reader-readgrant-20261016"
FUNCTION, ROLE, POLICY = "irpt-49f-reporting-publish-lambda", "irpt-49f-reporting-publish-role", "irpt-49f-reporting-publish-policy"
SCHEDULES = {"irpt-49f-reporting-publish-daily": None, "irpt-49f-reporting-publish-summaries-daily": None}  # name -> cron, read at the record's before
SIDS = sorted(["ListExactlyTheDeclaredGoldPrefixes", "ReadDeclaredGoldPartitionsOnly", "WriteThePlatinumReportingPrefixOnly", "ReadBackThePlatinumReportingPrefixOnly",
               "ListThePlatinumReportingPrefixForSummaries", "ReadTheFirmDirectoryObjectsOnly", "InvokeOwnFunctionForShardFanOut", "OwnLogStreamOnly"])
WIDENED = ["ListExactlyTheDeclaredGoldPrefixes", "ReadDeclaredGoldPartitionsOnly"]
FILLED_PREFIX = "irpt/49financial/gold/filled_report_values/"
ARTIFACT_BUCKET, ARTIFACT_KEY = "opal-313476888478-lambda-artifacts", "investor-reporting/irpt-reporting-publish-lambda.zip"
LAYER = "irpt-performance-native-layer"
MEM_LINE, DUR_LINE = 819, 240000
PROBE_EXPECT = {"enabled": False, "clients": 0, "written": 0, "not_available": [], "refused": []}
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("request_ids",)
in_window = G.in_window
stmt_hash = G.stmt_hash


def check_report(rp, label):
    need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"}, "%s: report keys" % label)
    need(is_int(rp["max_memory_used_mb"]) and rp["max_memory_used_mb"] <= MEM_LINE and rp["memory_size_mb"] == 1024 and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] <= DUR_LINE,
         "%s: Max Memory Used at most %d MB and duration at most %d ms (no resize inside this pair)" % (label, MEM_LINE, DUR_LINE))


def check_head(rec, packet_blob, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "build", "plan", "apply_finished_utc", "after", "probe", "dry_run", "platinum_after", "ledger_closed", "reads"}
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
    need(isinstance(b, dict) and set(b) == {"function_code_sha256", "artifact_version_id", "policy", "schedules", "platinum", "filled_prefix_objects"}, "before keys")
    need(b["function_code_sha256"] == BEFORE_CODE and b["artifact_version_id"] == BEFORE_VERSION, "before: the live code hash and the artifact version of the packet's section 3")
    need(isinstance(b["policy"], dict) and sorted(b["policy"]) == SIDS and all(re.fullmatch(r"[0-9a-f]{64}", str(v)) for v in b["policy"].values()), "before.policy: sha256 of each of the eight statements")
    need(isinstance(b["schedules"], dict) and sorted(b["schedules"]) == sorted(SCHEDULES) and all(isinstance(v, dict) and v.get("state") == "ENABLED" and nes(v.get("cron")) for v in b["schedules"].values()), "before.schedules: both ENABLED with their crons")
    need(isinstance(b["platinum"], dict) and set(b["platinum"]) == {"objects", "versions"} and is_int(b["platinum"]["objects"]) and is_int(b["platinum"]["versions"]) and b["platinum"]["objects"] > 0, "before.platinum: object and version counts")
    need(is_int(b["filled_prefix_objects"]) and b["filled_prefix_objects"] >= 1, "before.filled_prefix_objects: the filled prefix count the CTO asked to see printed before Act 3")
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == G.b64_of_hex(bd["zip_sha256"]) == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s" % BUILD_B64)
    need(isinstance(bd["members"], list) and "handler.py" in bd["members"] and "publisher.py" in bd["members"], "the zip must hold the handler and the publisher")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["landed_version_id"] != BEFORE_VERSION and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "import smoke, a NEW landed version or built-equals-landed")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "change_addresses", "function_change_attributes", "replan_no_changes"}, "plan keys")
    strip = lambda a: re.sub(r"^module\.[^.]+\.", "", str(a))  # noqa: E731
    need(p["add"] == 0 and p["change"] == 2 and p["destroy"] == 0 and sorted(strip(a) for a in p["change_addresses"]) == ["aws_iam_role_policy.irpt_reporting_publish", "aws_lambda_function.this"] and p["replan_no_changes"] is True,
         "the plan must read 0 add / 2 change / 0 destroy on the function and the role policy and a post-apply plan of No changes")
    fa = p["function_change_attributes"]
    need(isinstance(fa, list) and fa and set(fa) <= {"source_code_hash", "s3_object_version", "s3_key", "s3_bucket", "last_modified", "qualified_arn", "qualified_invoke_arn", "version", "source_code_size"}, "the function change must be by CODE attributes only: %s" % fa)
    t = rec["apply_finished_utc"]
    need(H.UTC.match(str(t)) and not in_window(t, "12:05", "13:15"), "the apply must be outside 12:05Z to 13:15Z on a trading weekday (the packet's condition 3)")
    return True


def check_tail(rec):
    b, a = rec["before"], rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy", "schedules"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 300 and f.get("reserved_concurrency") is None and f.get("code_sha256") == rec["build"]["zip_sha256_b64"] and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"],
         "after.function: memory 1024, timeout 300, no reserved concurrency, the landed zip's code hash, the native layer")
    need(isinstance(a["policy"], dict) and sorted(a["policy"]) == SIDS, "after.policy: the eight statements")
    same = [s for s in SIDS if a["policy"][s] == b["policy"][s]]
    need(sorted(set(SIDS) - set(same)) == sorted(WIDENED) and len(same) == 6, "after.policy: exactly the two named statements differ from before and the other six are byte-identical (differing: %s)" % sorted(set(SIDS) - set(same)))
    need(a["schedules"] == b["schedules"], "after.schedules must equal before.schedules (both ENABLED, crons untouched)")
    pr = rec["probe"]
    need(isinstance(pr, dict) and set(pr) == {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "request_id"}, "probe keys")
    need(pr["payload"] == {"filled_report": True} and pr["status_code"] == 200 and pr["function_error"] is None and H.UTC.match(str(pr["invoked_utc"])) and pr["invoked_utc"] >= rec["apply_finished_utc"]
         and not in_window(pr["invoked_utc"], "12:05", "13:15"), "probe: payload {filled_report: true}, 200, no error, after the apply, outside the fire windows")
    need(pr["returned"] == PROBE_EXPECT, "probe: the answer must be exactly the switch-OFF no-op %s, got %s" % (PROBE_EXPECT, pr["returned"]))
    check_report(pr["report"], "probe")
    need(nes(pr["request_id"]), "probe: request id")
    d = rec["dry_run"]
    need(isinstance(d, dict) and set(d) == {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "request_id"}, "dry_run keys")
    need(d["payload"] == {"dry_run": True, "shard": 0, "shards": 7} and d["status_code"] == 200 and d["function_error"] is None and H.UTC.match(str(d["invoked_utc"])) and d["invoked_utc"] >= pr["invoked_utc"]
         and not in_window(d["invoked_utc"], "12:05", "13:15"), "dry run: shard 0 of 7, 200, no error, after the probe, outside the fire windows")
    r = d["returned"]
    need(isinstance(r, dict) and set(r) == {"ok", "accounts", "refused_count"} and r["ok"] is True and is_int(r["accounts"]) and r["accounts"] > 0 and r["refused_count"] == 0, "dry run: ok, a positive shard count and 0 refusals (counts only, never an id)")
    check_report(d["report"], "dry_run")
    need(nes(d["request_id"]), "dry run: request id")
    need(rec["platinum_after"] == b["platinum"], "the platinum reporting prefix's object and version counts must be the same after the probe and the dry run")
    need(rec["ledger_closed"] in (True, False) and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "ledger_closed boolean; reads block")
    return True


def digit_runs(rec):
    skip = {"zip_sha256", "zip_sha256_b64", "content_sha256", "landed_version_id", "request_id", "request_ids", "policy", "function_code_sha256", "code_sha256", "artifact_version_id", "invoked_utc", "apply_finished_utc", "packet_blob", "packet_sha256", "ledger_entry", "layer_arn"} | set(SIDS)  # the ledger slug carries a date; a policy hash sits under its statement id
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
    if cid == "DBC179-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time), ledger %s, applier named, build %s equals the packet's and landed as a NEW version, plan 0 add / 2 change / 0 destroy on the function and the role policy, the apply outside the fire window" % (LEDGER_SLUG, BUILD_B64[:8]))
        return True
    check_tail(rec)
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    if cid == "DBC179-3-AC1":
        print("OK: the probe answered the exact switch-OFF no-op, the dry-run shard returned ok with 0 refusals inside 819 MB / 240 s, and the platinum object and version counts are unchanged")
        return True
    import boto3
    lam, iam, s3, sch = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam"), boto3.client("s3"), boto3.client("scheduler", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    need(cfg["MemorySize"] == 1024 and cfg["Timeout"] == 300 and cfg["Handler"] == "handler.lambda_handler" and cfg["Runtime"] == "python3.12" and cfg["Role"].endswith("role/" + ROLE) and conc is None and not (cfg.get("Environment") or {}).get("Variables"),
         "live function: memory 1024, timeout 300, handler, runtime, role, NO reserved concurrency and NO environment variable (the switch is off)")
    need(cfg["CodeSha256"] == rec["build"]["zip_sha256_b64"] != BEFORE_CODE and [x["Arn"] for x in cfg.get("Layers", [])] == [rec["after"]["function"]["layer_arn"]], "live CodeSha256 must equal the landed zip's, differ from the old, and the one layer unchanged")
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    live = {x["Sid"]: stmt_hash(x) for x in sts}
    need(live == rec["after"]["policy"], "live execution policy: the eight statements must equal the record's")
    by = {x["Sid"]: x for x in sts}
    lst = by["ListExactlyTheDeclaredGoldPrefixes"]["Condition"]["StringLike"]["s3:prefix"]
    need(len(lst) == 3 and (FILLED_PREFIX + "*") in lst, "live List statement: 3 prefixes, the filled prefix among them")
    rd = by["ReadDeclaredGoldPartitionsOnly"]["Resource"]
    need(len(rd) == 3 and any(r.endswith("/" + FILLED_PREFIX + "*") for r in rd), "live Read statement: 3 resources, the filled prefix among them")
    need(by["ReadDeclaredGoldPartitionsOnly"]["Action"] == "s3:GetObject" and by["ReadDeclaredGoldPartitionsOnly"]["Effect"] == "Allow", "the widened read statement stays a GetObject Allow")
    for name, v in rec["after"]["schedules"].items():
        sc = sch.get_schedule(Name=name)
        need({"state": sc["State"], "cron": sc["ScheduleExpression"]} == {"state": v["state"], "cron": v["cron"]} and sc["State"] == "ENABLED", "the schedule %s must be ENABLED, untouched" % name)
    ver = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)
    need(ver.get("VersionId") == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
    print("OK: live: the function runs the NEW code with no environment variable; the policy's List and Read statements carry exactly the one added prefix and the other six are unchanged; both schedules are ENABLED and untouched; the artifact's current version is the recorded one")
    return True


# ------------------------------------------------------------------------------------------------ selftest
def synthetic():
    pol_b = {s: ("%02x" % i) * 32 for i, s in enumerate(SIDS)}
    pol_a = dict(pol_b)
    for s in WIDENED:
        pol_a[s] = "ff" * 32
    sch = {n: {"state": "ENABLED", "cron": "cron(15 8 ? * MON-FRI *)"} for n in SCHEDULES}
    rp = {"max_memory_used_mb": 300, "duration_ms": 12000, "memory_size_mb": 1024}
    rec = {"claim": "measured",
           "gates": {"packet_blob": PACKET_BLOB, "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True, "one_change_at_a_time": {"worktrees_read": 4, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
           "ledger_entry": LEDGER_SLUG, "applier": APPLIER,
           "before": {"function_code_sha256": BEFORE_CODE, "artifact_version_id": BEFORE_VERSION, "policy": pol_b, "schedules": sch, "platinum": {"objects": 18257, "versions": 18300}, "filled_prefix_objects": 1},
           "build": {"zip_sha256": None, "zip_sha256_b64": BUILD_B64, "members": ["handler.py", "publisher.py"], "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": None, "built_equals_landed": True},
           "plan": {"add": 0, "change": 2, "destroy": 0, "change_addresses": ["module.x.aws_lambda_function.this", "module.x.aws_iam_role_policy.irpt_reporting_publish"], "function_change_attributes": ["source_code_hash", "s3_object_version"], "replan_no_changes": True},
           "apply_finished_utc": "2026-10-16T22:10:00Z",
           "after": {"function": {"memory": 1024, "timeout": 300, "reserved_concurrency": None, "code_sha256": BUILD_B64, "layer_arn": "arn:aws:lambda:us-east-1:1:layer:%s:1" % LAYER}, "policy": pol_a, "schedules": sch},
           "probe": {"payload": {"filled_report": True}, "invoked_utc": "2026-10-16T22:20:00Z", "status_code": 200, "function_error": None, "returned": dict(PROBE_EXPECT), "report": dict(rp), "request_id": "r1"},
           "dry_run": {"payload": {"dry_run": True, "shard": 0, "shards": 7}, "invoked_utc": "2026-10-16T22:25:00Z", "status_code": 200, "function_error": None, "returned": {"ok": True, "accounts": 990, "refused_count": 0}, "report": dict(rp), "request_id": "r2"},
           "platinum_after": {"objects": 18257, "versions": 18300}, "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    return rec


def selftest():
    import base64
    rec = synthetic()
    hx = base64.b64decode(BUILD_B64).hex()
    rec["build"]["zip_sha256"] = hx
    rec["build"]["content_sha256"] = hx
    ok = lambda r: (check_head(r, PACKET_BLOB, "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12], True), check_tail(r))  # noqa: E731
    ok(rec)
    arms = {
        "claim": lambda r: r.update(claim="inferred"),
        "build hash": lambda r: r["build"].update(zip_sha256_b64="x" * 44),
        "plan change 1": lambda r: r["plan"].update(change=1),
        "plan destroy": lambda r: r["plan"].update(destroy=1),
        "plan address": lambda r: r["plan"].update(change_addresses=["module.x.aws_lambda_function.this", "module.x.aws_iam_role.y"]),
        "replan": lambda r: r["plan"].update(replan_no_changes=False),
        "apply window": lambda r: r.update(apply_finished_utc="2026-10-16T12:30:00Z"),
        "memory": lambda r: r["after"]["function"].update(memory=3008),
        "concurrency": lambda r: r["after"]["function"].update(reserved_concurrency=1),
        "policy third statement": lambda r: r["after"]["policy"].update({SIDS[3]: "ee" * 32}),
        "policy widened missing": lambda r: r["after"]["policy"].update({WIDENED[0]: r["before"]["policy"][WIDENED[0]]}),
        "schedule": lambda r: r["after"]["schedules"].update({sorted(SCHEDULES)[0]: {"state": "DISABLED", "cron": "x"}}),
        "probe payload": lambda r: r["probe"].update(payload={"filled_report": False}),
        "probe enabled": lambda r: r["probe"]["returned"].update(enabled=True),
        "probe written": lambda r: r["probe"]["returned"].update(written=1),
        "probe error": lambda r: r["probe"].update(function_error="Unhandled"),
        "dry payload": lambda r: r["dry_run"].update(payload={"dry_run": True, "shard": 1, "shards": 7}),
        "dry refused": lambda r: r["dry_run"]["returned"].update(refused_count=1),
        "dry memory": lambda r: r["dry_run"]["report"].update(max_memory_used_mb=900),
        "dry duration": lambda r: r["dry_run"]["report"].update(duration_ms=250000),
        "dry order": lambda r: r["dry_run"].update(invoked_utc="2026-10-16T22:15:00Z"),
        "platinum moved": lambda r: r["platinum_after"].update(objects=18258),
        "reads": lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}),
        "ledger name": lambda r: r.update(ledger_entry="other"),
        "applier": lambda r: r.update(applier="0.7.0_AE_CloudOps~DB2"),
        "digit run": lambda r: r["before"].update(note="1234567890"),
    }
    n = 0
    for label, mut in arms.items():
        r = copy.deepcopy(rec)
        mut(r)
        try:
            ok(r)
            if label == "digit run":
                need(not digit_runs(r), "digit")
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
