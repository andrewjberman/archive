"""IRPT_DASHBD round 147, workstream B-49F + contract (issuer 2.0.0_SA_COO~D2) -- DB-b-283, the APPLY of the signed never-widen pair for the first Cottonwood series publish (packet sha256 0c9b495ce2f7,
COO half signed @6c8e76f0e0, CTO half signed @474f33174c): the gates, the build, the plan (exactly 4 add / 0 change / 0 destroy), ONE safe-apply, the DRY-RUN event, the ONE-ACCOUNT upload and the FULL upload.
WORLD. The record is the applier's; the checker re-reads the world.

  DBC151-1-AC1  the record's head: packet and halves, gates, ledger and applier, before, build, plan
  DBC151-2-AC1  FRESH live reads of the function, the role policy, the artifact and the absence of any schedule
  DBC151-3-AC1  the dry run, the canary and the full upload in the record, and FRESH reads of the prefix: object counts, sampled series and manifests, the REPORT lines, the open ledger

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import base64
import copy
import gzip
import hashlib
import json
import re
import subprocess
import sys
import datetime as dt
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
APPLIER = "0.7.0_AE_CloudOps~DB2"
REC_REL = D + APPLIER + "/COT_PUBLISH_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_REPORTING_PUBLISH_LAMBDA.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_REPORTING_PUBLISH_LAMBDA_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_REPORTING_PUBLISH_LAMBDA_CTO_HALF.md"
PACKET_SHA = "0c9b495ce2f7e347738ad53a643d1f7b19bf48b226258136e84753371cdae463"
BUILD_B64 = "HDgIzQoXMyUNBxeyqgLXcplD1c01QwVsASRoMJbd4hk="
LEDGER_SLUG = "irpt-dashbd-cottonwood-reporting-publish-20261016"
FUNCTION = "irpt-cot-reporting-publish-lambda"
ROLE = "irpt-cot-reporting-publish-execution-role"
POLICY = "irpt-cot-reporting-publish-execution-policy"
LOG_GROUP = "/aws/lambda/" + FUNCTION
LAYER = "irpt-performance-native-layer"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
ARTIFACT_KEY = "investor-reporting/irpt-cot-reporting-publish-lambda.zip"
BUCKET = "opal-data-cottonwood"
PREFIX = "irpt/cottonwood/platinum/reporting/"
GOLD_PREFIX = "irpt/cottonwood/gold/account_return_daily/"
FLOOR = "2026-07-10"
ABSENT = ["2026-08-19", "2026-09-24", "2026-09-25"]
FIXED = "trading calendar minus present partitions"
SIDS = sorted(["ListGoldReturnsAndPlatinumReportingOnly", "ReadGoldReturnsOnly", "WriteThePlatinumReportingPrefixOnly", "ReadBackThePlatinumReportingPrefixOnly", "OwnLogStreamOnly"])
PLAN_ADDRESSES = sorted(["aws_cloudwatch_log_group.lambda", "aws_iam_role.irpt_reporting_publish_iso_execution", "aws_iam_role_policy.irpt_reporting_publish_iso_execution", "aws_lambda_function.this"])
SUMMARY_KEYS = {"ok", "uploaded", "floor", "partitions", "first", "last", "accounts_seen", "accounts_named", "published", "refused", "refusals", "skipped_null_account", "unreported_trading_days", "seconds"}
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ISO_DAY = re.compile(r"\d{4}-\d{2}-\d{2}$")
HEX12 = re.compile(r"[0-9a-f]{12}$")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "packet_blob", "landed_version_id", "version_id", "code_sha256", "addresses", "ledger_entry", "apply_finished_utc", "zip_sha256", "zip_sha256_b64", "content_sha256",
                 "request_id", "request_ids", "account_hash12", "invoked_utc", "sampled_hash12", "layer_arn", "members", "applier")


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
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and is_int(oc["worktrees_read"]) and oc["worktrees_read"] >= 1 and oc["open_markers_naming_this_surface"] == 0,
         "one_change_at_a_time: the denominator (worktrees read) and zero markers naming this surface")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists, "the ledger entry %s must exist" % LEDGER_SLUG)
    need(rec["applier"] == APPLIER, "the applier must be named (the CTO's condition 2): %s" % APPLIER)
    b = rec["before"]
    need(isinstance(b, dict) and set(b) == {"function_exists", "role_exists", "artifact_exists", "artifact_version_id", "platinum_reporting_objects"}, "before keys")
    need(b["function_exists"] is False and b["role_exists"] is False and b["artifact_exists"] is False and b["artifact_version_id"] is None and b["platinum_reporting_objects"] == 0,
         "before: function, role and artifact absent and the target prefix at 0 objects, as the packet's section 3")
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == b64_of_hex(bd["zip_sha256"]), "build.zip_sha256 and its base64 form must agree")
    need(bd["zip_sha256_b64"] == BUILD_B64, "the build's sha256 must equal the packet's section 2 value %s, got %s" % (BUILD_B64, bd["zip_sha256_b64"]))
    need(isinstance(bd["members"], list) and len(bd["members"]) >= 13 and "handler.py" in bd["members"], "the zip must hold the handler and its 12 staged members")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "the import smoke, the landed version or the built-equals-landed record")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "addresses", "replan_no_changes"}, "plan keys")
    need(p["add"] == 4 and p["change"] == 0 and p["destroy"] == 0 and sorted(re.sub(r"^module\.[^.]+\.", "", str(a)) for a in p["addresses"]) == PLAN_ADDRESSES and p["replan_no_changes"] is True,
         "the plan must read 4 add / 0 change / 0 destroy on the four addresses, and a post-apply plan with no changes")
    return True


def check_report(rp, label):
    need(isinstance(rp, dict) and set(rp) == {"max_memory_used_mb", "duration_ms", "memory_size_mb"} and is_int(rp["max_memory_used_mb"]) and 0 < rp["max_memory_used_mb"] <= 717 and rp["memory_size_mb"] == 1024
         and isinstance(rp["duration_ms"], (int, float)) and 0 < rp["duration_ms"] < 900000, "%s.report: Max Memory Used at most 717 MB, duration under 900 s, memory size 1024" % label)


def check_summary(s, label, uploaded, named=None):
    need(isinstance(s, dict) and set(s) == SUMMARY_KEYS, "%s summary keys differ: %s" % (label, sorted(set(s) ^ SUMMARY_KEYS) if isinstance(s, dict) else "?"))
    need(s["ok"] is True and s["uploaded"] is uploaded and s["floor"] == FLOOR and s["first"] == FLOOR and ISO_DAY.match(str(s["last"])), "%s: ok, uploaded %s, floor and first %s, last an ISO day" % (label, uploaded, FLOOR))
    need(all(is_int(s[k]) and s[k] >= 0 for k in ("partitions", "accounts_seen", "accounts_named", "published", "refused", "skipped_null_account")) and s["partitions"] >= 65, "%s: whole-number counts, at least 65 partitions" % label)
    need(s["published"] + s["refused"] == s["accounts_named"] and s["accounts_named"] <= s["accounts_seen"], "%s: published + refused must equal accounts_named" % label)
    need(isinstance(s["refusals"], dict) and all(nes(k) and is_int(v) and v > 0 for k, v in s["refusals"].items()) and sum(s["refusals"].values()) == s["refused"], "%s: refusals are reason -> count and sum to refused" % label)
    need(s["refused"] * 10 <= s["accounts_named"], "%s: refusals above 10 percent of accounts_named are a STOP" % label)
    ul = s["unreported_trading_days"]
    need(isinstance(ul, list) and ul[:3] == ABSENT and ul == sorted(set(ul)) and all(ISO_DAY.match(str(d)) for d in ul) and all(d > "2026-10-14" for d in ul[3:]), "%s: unreported days begin with the three absent days, strictly increasing, any more after 2026-10-14: %s" % (label, ul))
    need(isinstance(s["seconds"], (int, float)) and 0 <= s["seconds"] < 900, "%s: seconds under 900" % label)
    if named is not None:
        need(s["accounts_named"] == named, "%s: accounts_named %s, expected %s" % (label, s["accounts_named"], named))


def check_tail(rec):
    need(UTC.match(str(rec["apply_finished_utc"])), "apply_finished_utc must be an ISO UTC instant")
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy_sids"}, "after keys")
    f = a["function"]
    need(isinstance(f, dict) and f.get("memory") == 1024 and f.get("timeout") == 900 and f.get("reserved_concurrency") is None and f.get("code_sha256") == rec["build"]["zip_sha256_b64"]
         and nes(f.get("layer_arn")) and (":layer:%s:" % LAYER) in f["layer_arn"], "after.function: memory 1024, timeout 900, NO reserved concurrency, code hash equal to the landed zip's, the native layer's ARN")
    need(sorted(a["policy_sids"]) == SIDS, "after.policy_sids must be the five statements")
    e = rec["dry_run"]
    ek = {"payload", "invoked_utc", "invocation_type", "status_code", "function_error", "returned", "report", "objects_after", "request_id"}
    need(isinstance(e, dict) and set(e) == ek, "dry_run keys differ")
    need(e["payload"] == {} and e["invocation_type"] == "RequestResponse" and e["status_code"] == 200 and e["function_error"] is None, "the dry run must be {}, synchronous, 200, no function error")
    need(UTC.match(str(e["invoked_utc"])) and e["invoked_utc"] >= rec["apply_finished_utc"], "dry_run.invoked_utc not before the apply finished")
    check_summary(e["returned"], "dry_run", False)
    check_report(e["report"], "dry_run")
    need(e["objects_after"] == 0 and nes(e["request_id"]), "the dry run must leave 0 objects in the target prefix")
    dr = e["returned"]
    c = rec["canary"]
    ck = {"payload_shape", "account_hash12", "invoked_utc", "status_code", "function_error", "returned", "report", "objects_after", "checks", "request_id"}
    need(isinstance(c, dict) and set(c) == ck, "canary keys differ")
    need(c["payload_shape"] == {"upload": True, "accounts": 1} and HEX12.match(str(c["account_hash12"])) and c["status_code"] == 200 and c["function_error"] is None, "canary: payload {upload true, one account} (the id stays private, only a hash prefix)")
    need(UTC.match(str(c["invoked_utc"])) and c["invoked_utc"] >= e["invoked_utc"], "canary.invoked_utc after the dry run")
    check_summary(c["returned"], "canary", True, named=1)
    need(c["returned"]["published"] == 1 and c["returned"]["refused"] == 0 and c["objects_after"] == 2, "canary: one account published, none refused, 2 objects in the prefix")
    check_report(c["report"], "canary")
    cks = {"series_size_equals_manifest", "validates_contract", "pair_present", "unreported_equals_dry_run", "income_all_null", "manifest_firm_ok", "publisher_version"}
    need(isinstance(c["checks"], dict) and set(c["checks"]) == cks and all(c["checks"][k] is True for k in cks - {"publisher_version"}) and c["checks"]["publisher_version"] == "0.2.0", "canary checks: all true and publisher_version 0.2.0")
    need(nes(c["request_id"]), "canary.request_id")
    fu = rec["full"]
    fk = {"payload", "invoked_utc", "status_code", "function_error", "returned", "report", "objects_after", "sampled_hash12", "sample_checks_pass", "request_id"}
    need(isinstance(fu, dict) and set(fu) == fk, "full keys differ")
    need(fu["payload"] == {"upload": True} and fu["status_code"] == 200 and fu["function_error"] is None, "full: payload {upload: true}, 200, no function error")
    need(UTC.match(str(fu["invoked_utc"])) and fu["invoked_utc"] >= c["invoked_utc"], "full.invoked_utc after the canary")
    check_summary(fu["returned"], "full", True, named=dr["accounts_named"])
    need(fu["returned"]["published"] == dr["published"] and fu["returned"]["refused"] == dr["refused"] and fu["returned"]["unreported_trading_days"] == dr["unreported_trading_days"], "full: published, refused and the unreported list must equal the dry run's")
    need(fu["objects_after"] == 2 * fu["returned"]["published"], "full: objects_after must be 2 x published")
    need(isinstance(fu["sampled_hash12"], list) and len(fu["sampled_hash12"]) == 10 and all(HEX12.match(str(h)) for h in fu["sampled_hash12"]) and fu["sample_checks_pass"] is True and nes(fu["request_id"]), "full: ten sampled hash prefixes and the sample checks passing")
    check_report(fu["report"], "full")
    need(rec["ledger_closed"] is False, "the ledger must stay OPEN")
    need(rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def list_all(s3, bucket, prefix):
    out, tok = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        out += [(o["Key"], o["LastModified"], o["Size"]) for o in r.get("Contents", [])]
        if not r.get("IsTruncated"):
            return out
        tok = r.get("NextContinuationToken")


def live(root, rec):
    import boto3
    lam, iam, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam"), boto3.client("s3")
    logs, sch = boto3.client("logs", region_name="us-east-1"), boto3.client("scheduler", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    try:
        conc = lam.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    except Exception:  # noqa: BLE001
        conc = None
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    put = [s for s in sts if "s3:PutObject" in (s["Action"] if isinstance(s["Action"], list) else [s["Action"]])]
    names = [s["Name"] for pg in sch.get_paginator("list_schedules").paginate(NamePrefix="irpt-cot-reporting-publish") for s in pg.get("Schedules", [])]
    ver = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=ARTIFACT_KEY)
    objs = list_all(s3, BUCKET, PREFIX)
    gold_days = sorted({k[len(GOLD_PREFIX) + 5:len(GOLD_PREFIX) + 15] for k, _, _ in list_all(s3, BUCKET, GOLD_PREFIX) if k.endswith(".parquet")})
    reports = []
    tok = None
    for _ in range(100):
        kw = {"logGroupName": LOG_GROUP, "filterPattern": "REPORT"}
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
    layers = [x["Arn"] for x in cfg.get("Layers", [])]
    samples = []
    accts = sorted({k[len(PREFIX):].split("/")[0] for k, _, _ in objs})
    pick = [accts[i] for i in range(0, len(accts), max(1, len(accts) // 10))][:10] if accts else []
    for a in pick:
        sb = s3.get_object(Bucket=BUCKET, Key="%s%s/series.json.gz" % (PREFIX, a))["Body"].read()
        mb = s3.get_object(Bucket=BUCKET, Key="%s%s/manifest.json" % (PREFIX, a))["Body"].read()
        samples.append((a, sb, mb))
    return {"layers": layers, "memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "handler": cfg["Handler"], "runtime": cfg["Runtime"], "role": cfg["Role"],
            "env": cfg.get("Environment"), "concurrency": conc, "sids": sorted(s.get("Sid", "") for s in sts), "n_put": len(put), "put_resources": put[0]["Resource"] if len(put) == 1 else None,
            "schedules": names, "artifact_version": ver.get("VersionId"), "objects": objs, "gold_days": gold_days, "reports": reports, "samples": samples}


def check_sample(root, a, sb, mb, rec):
    sys.path.insert(0, str(Path(root) / "infra/aws/lambda/investor-reporting/reporting-publish"))
    import publisher
    contract = json.loads((Path(root) / "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json").read_bytes().decode("utf-8"))
    s = json.loads(gzip.decompress(sb).decode("utf-8"))
    m = json.loads(mb.decode("utf-8"))
    h = hashlib.sha256(a.encode()).hexdigest()[:12]
    bad = publisher.validate_against_contract(s, m, contract)
    need(not bad, "sample %s: the document does not validate: %s" % (h, bad[:2]))
    need(m["byte_sizes"]["series.json.gz"] == len(sb) and m["publisher_version"] == "0.2.0" and m["account_id"] == a, "sample %s: manifest size, version or account" % h)
    need(all(x is None for x in s["income"]), "sample %s: income must be all null" % h)
    need(s["unreported_trading_days_basis"] == FIXED, "sample %s: the basis" % h)
    want = [d for d in rec["dry_run"]["returned"]["unreported_trading_days"] if s["first_data_date"] < d <= s["as_of"] and d not in s["date"]]
    need(s["unreported_trading_days"] == want, "sample %s: unreported days differ from the dry run's list inside its window" % h)
    return h


def run(root, cid):
    root = Path(root)
    rec = load(root, REC_REL)
    packet_blob = git(root, "hash-object", PACKET_REL).strip()
    need(hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest() == PACKET_SHA, "the packet's bytes differ from the signed sha256")
    need((root / CTO_HALF_REL).is_file(), "no CTO half")
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8")
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8")
    ledger_exists = bool(list((root / "org/critical_paths/change_management").glob("*%s*" % LEDGER_SLUG)))
    check_head(rec, packet_blob, coo, cto, ledger_exists)
    if cid == "DBC151-1-AC1":
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time, function, role and artifact absent and the target prefix empty before), ledger %s, applier named, build %s equals the packet's, plan 4/0/0 on the four addresses" % (LEDGER_SLUG, rec["build"]["zip_sha256"][:12]))
        return True
    check_tail(rec)
    lv = live(root, rec)
    if cid == "DBC151-2-AC1":
        need(lv["memory"] == 1024 and lv["timeout"] == 900 and lv["handler"] == "handler.lambda_handler" and lv["runtime"] == "python3.12" and lv["role"].endswith("role/" + ROLE), "live function: memory/timeout/handler/runtime/role")
        need(lv["concurrency"] is None and not (lv["env"] or {}).get("Variables"), "live function: no reserved concurrency, no environment")
        need(lv["code_sha256"] == rec["build"]["zip_sha256_b64"], "live CodeSha256 differs from the landed zip's")
        need(len(lv["layers"]) == 1 and lv["layers"][0] == rec["after"]["function"]["layer_arn"], "live layers differ from the record")
        need(lv["sids"] == SIDS, "live policy sids differ: %s" % lv["sids"])
        want = "arn:aws:s3:::%s/%s*" % (BUCKET, PREFIX)
        need(lv["n_put"] == 1 and lv["put_resources"] in (want, [want]), "the one PutObject statement must name only the platinum reporting prefix: %s" % lv["put_resources"])
        need(lv["schedules"] == [], "a schedule named irpt-cot-reporting-publish* exists: %s" % lv["schedules"])
        need(nes(lv["artifact_version"]) and lv["artifact_version"] == rec["build"]["landed_version_id"], "the artifact's current version differs from the recorded landed version")
        print("OK: live: memory 1024, timeout 900, no reserved concurrency, no environment, CodeSha256 equals the landed zip's, five policy statements with one PutObject on the platinum reporting prefix, no schedule, one native layer")
        return True
    if cid == "DBC151-3-AC1":
        keys = [k for k, _, _ in lv["objects"]]
        n = rec["full"]["returned"]["published"]
        need(len(keys) == 2 * n == rec["full"]["objects_after"], "the prefix holds %d objects, the record says 2 x %d" % (len(keys), n))
        need(sum(1 for k in keys if k.endswith("/series.json.gz")) == n and sum(1 for k in keys if k.endswith("/manifest.json")) == n, "series and manifest counts must each equal published")
        need(not [k for k in keys if not (k.endswith("/series.json.gz") or k.endswith("/manifest.json"))], "an object other than a series or manifest sits in the prefix")
        first_put = min(t for _, t, _ in lv["objects"]).strftime("%Y-%m-%dT%H:%M:%SZ")
        need(first_put >= rec["canary"]["invoked_utc"], "an object is older than the canary: the dry run (or something else) wrote")
        last = rec["dry_run"]["returned"]["last"]
        sys.path.insert(0, str(root / "lib"))
        import trading_calendar as tc
        cal = [d.isoformat() for d in tc.trading_days_between(dt.date.fromisoformat(FLOOR), dt.date.fromisoformat(last))]
        want_un = [d for d in cal if d not in set(lv["gold_days"])]
        got = rec["dry_run"]["returned"]["unreported_trading_days"]
        need(got == want_un, "the dry run's unreported list differs from the calendar minus the live gold partitions: %s vs %s" % (got, want_un))
        hs = [check_sample(root, a, sb, mb, rec) for a, sb, mb in lv["samples"]]
        need(len(hs) == 10 and hs == rec["full"]["sampled_hash12"], "the ten sampled accounts (by position) must equal the record's hash prefixes")
        rp = rec["dry_run"]["report"]
        need([r for r in lv["reports"] if r[2] == rp["max_memory_used_mb"] and abs(r[0] - rp["duration_ms"]) < 1.0 and r[1] == 1024], "no REPORT line in the log group equals the dry run's")
        need(not [r for r in lv["reports"] if r[2] > 717], "a REPORT line reads Max Memory Used above 717 MB")
        need((root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file(), "the ledger's open marker is missing: the ledger must stay OPEN")
        print("OK: the dry run left no object; %d objects (%d series, %d manifests) all in the target prefix; ten sampled series validate against the series contract, carry the pair equal to the dry run's list inside their windows, all-null income and a matching manifest; a REPORT line equals the dry run's, none above 717 MB; ledger open" % (len(keys), n, n))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    def red(fn, label):
        try:
            fn()
        except Fail:
            return
        raise AssertionError("red arm passed: " + label)
    zh = "ab" * 32
    global BUILD_B64, PACKET_SHA
    saved = (BUILD_B64, PACKET_SHA)
    BUILD_B64, PACKET_SHA = b64_of_hex(zh), "cc" * 32
    try:
        rp = {"max_memory_used_mb": 300, "duration_ms": 5000.0, "memory_size_mb": 1024}

        def summ(up, named, pub, ref, reasons):
            return {"ok": True, "uploaded": up, "floor": FLOOR, "partitions": 65, "first": FLOOR, "last": "2026-10-14", "accounts_seen": 979, "accounts_named": named, "published": pub, "refused": ref,
                    "refusals": reasons, "skipped_null_account": 1, "unreported_trading_days": list(ABSENT), "seconds": 12.5}
        good = {"claim": "measured", "gates": {"packet_blob": "b" * 40, "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
                                               "one_change_at_a_time": {"worktrees_read": 5, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
                "ledger_entry": LEDGER_SLUG, "applier": APPLIER, "before": {"function_exists": False, "role_exists": False, "artifact_exists": False, "artifact_version_id": None, "platinum_reporting_objects": 0},
                "build": {"zip_sha256": zh, "zip_sha256_b64": b64_of_hex(zh), "members": ["handler.py"] + ["m%d" % i for i in range(12)], "import_smoke_rc": 0, "landed_version_id": "v1", "content_sha256": zh, "built_equals_landed": True},
                "plan": {"add": 4, "change": 0, "destroy": 0, "addresses": ["module.x." + a for a in PLAN_ADDRESSES], "replan_no_changes": True}, "apply_finished_utc": "2026-10-16T05:00:00Z",
                "after": {"function": {"memory": 1024, "timeout": 900, "reserved_concurrency": None, "code_sha256": b64_of_hex(zh), "layer_arn": "arn:aws:lambda:us-east-1:1:layer:%s:1" % LAYER}, "policy_sids": list(SIDS)},
                "dry_run": {"payload": {}, "invoked_utc": "2026-10-16T05:01:00Z", "invocation_type": "RequestResponse", "status_code": 200, "function_error": None, "returned": summ(False, 978, 970, 8, {"no positive value": 8}),
                            "report": rp, "objects_after": 0, "request_id": "r1"},
                "canary": {"payload_shape": {"upload": True, "accounts": 1}, "account_hash12": "abcdef012345", "invoked_utc": "2026-10-16T05:02:00Z", "status_code": 200, "function_error": None,
                           "returned": summ(True, 1, 1, 0, {}), "report": rp, "objects_after": 2, "request_id": "r2",
                           "checks": {"series_size_equals_manifest": True, "validates_contract": True, "pair_present": True, "unreported_equals_dry_run": True, "income_all_null": True, "manifest_firm_ok": True, "publisher_version": "0.2.0"}},
                "full": {"payload": {"upload": True}, "invoked_utc": "2026-10-16T05:03:00Z", "status_code": 200, "function_error": None, "returned": summ(True, 978, 970, 8, {"no positive value": 8}), "report": rp,
                         "objects_after": 1940, "sampled_hash12": ["%012x" % i for i in range(10)], "sample_checks_pass": True, "request_id": "r3"},
                "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
        assert check_head(good, "b" * 40, "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12], True) and check_tail(good)
        arms = (("claim", lambda r: r.update(claim="inferred")), ("blob", lambda r: r["gates"].update(packet_blob="c" * 40)), ("cto", lambda r: r["gates"].update(cto_half_signed=False)),
                ("markers", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1)), ("applier", lambda r: r.update(applier="x")), ("before", lambda r: r["before"].update(function_exists=True)),
                ("prefix", lambda r: r["before"].update(platinum_reporting_objects=3)), ("build", lambda r: r["build"].update(zip_sha256_b64="x")), ("smoke", lambda r: r["build"].update(import_smoke_rc=1)),
                ("plan", lambda r: r["plan"].update(add=5)), ("replan", lambda r: r["plan"].update(replan_no_changes=False)), ("memory", lambda r: r["after"]["function"].update(memory=512)),
                ("concurrency", lambda r: r["after"]["function"].update(reserved_concurrency=1)), ("sids", lambda r: r["after"].update(policy_sids=["x"])), ("dry payload", lambda r: r["dry_run"].update(payload={"upload": True})),
                ("dry uploaded", lambda r: r["dry_run"]["returned"].update(uploaded=True)), ("dry objects", lambda r: r["dry_run"].update(objects_after=1)), ("absent days", lambda r: r["dry_run"]["returned"].update(unreported_trading_days=["2026-08-19"])),
                ("memory717", lambda r: r["dry_run"]["report"].update(max_memory_used_mb=800)), ("refusals 10pct", lambda r: r["dry_run"]["returned"].update(accounts_named=978, published=800, refused=178, refusals={"x": 178})),
                ("canary two", lambda r: r["canary"]["returned"].update(published=2)), ("canary objects", lambda r: r["canary"].update(objects_after=1)), ("canary check", lambda r: r["canary"]["checks"].update(income_all_null=False)),
                ("canary hash", lambda r: r["canary"].update(account_hash12="zz")), ("full published", lambda r: r["full"]["returned"].update(published=969)), ("full objects", lambda r: r["full"].update(objects_after=1939)),
                ("full sample", lambda r: r["full"].update(sample_checks_pass=False)), ("full order", lambda r: r["full"].update(invoked_utc="2026-10-16T05:00:30Z")), ("ledger", lambda r: r.update(ledger_closed=True)),
                ("digits", lambda r: r["dry_run"].update(request_id="r1", payload={})), ("extra", lambda r: r.update(z=1)))
        for label, fn in arms:
            r2 = copy.deepcopy(good)
            fn(r2)
            if label == "digits":
                r2["canary"]["checks"]["note"] = "12345678"
                r2["canary"]["checks"].pop("note")
                r2["after"]["note"] = "12345678"
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
