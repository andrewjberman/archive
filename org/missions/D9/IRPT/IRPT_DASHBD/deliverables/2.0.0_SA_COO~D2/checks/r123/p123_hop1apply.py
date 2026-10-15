"""IRPT_DASHBD round 123, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-253, the APPLY of the signed hop-1 pair (packet sha256 2f25b84dc85c..., COO half @2959d224ad, CTO half
@c07129fed1, CTO msg 8235): one Terraform apply of the reporting-gold root by the AE applier, plan exactly 0 add / 2 change / 0 destroy on the function and the role policy.

  DB-b-253 (0.7.0_AE_CloudOps~DB2) the gates, the ledger, the bundle build and upload, the plan, ONE safe-apply, the read-backs, no invoke, the ledger left OPEN.
                                                                                           DBB123-1-AC1 (gates, ledger, build, plan; the record),
                                                                                           DBB123-2-AC1 (FRESH live reads: function, policy, schedule),
                                                                                           DBB123-3-AC1 (FRESH reads: the new prefix, no invoke, the ledger open)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the record clauses on synthetic arms
"""
import base64
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.7.0_AE_CloudOps~DB2/HOP1_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_HOP1_FILLED_REPORT_VALUES_STAGE.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_HOP1_FILLED_REPORT_VALUES_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_HOP1_FILLED_REPORT_VALUES_CTO_HALF.md"
PACKET_SHA = "2f25b84dc85c1592801783ae23113e13c2686bad54b9fa6460ea6d353ac2635e"
LEDGER_SLUG = "irpt-dashbd-hop1-filled-report-values-20261015"
FUNCTION = "irpt-49f-reporting-gold-lambda"
ROLE = "irpt-49f-reporting-gold-role"
POLICY = "irpt-49f-reporting-gold-policy"
SCHEDULE_PREFIX = "irpt-49f-reporting-gold"
CRON = "cron(41 7 ? * MON-FRI *)"
ZONE = "America/New_York"
SIDS_BEFORE = ["ListExactlyTheDeclaredSilverPrefixes", "ReadDeclaredSilverPartitionsOnly", "ListExactlyTheSixGoldPrefixes", "ReadTheSixGoldPrefixesOnly", "WriteTheFiveGoldPrefixesOnly",
               "ReadTheClassTableByKeyOnly", "OwnLogStreamOnly"]
SIDS_NEW = ["ReadTheServedModelSeriesObjectOnly", "ListExactlyTheHouseholdCrosswalkPrefix", "ReadTheHouseholdCrosswalkOnly", "InvokeOwnFunctionOnly"]
SIDS_AFTER = sorted(SIDS_BEFORE + SIDS_NEW)
BEFORE_CODE_SHA = "J6M/92MhjYM/0kKoYRQwR0ah68DizcvnkVSE6o24udg="
PLAN_ADDRESSES = ["aws_iam_role_policy.irpt_reporting_gold", "module.irpt_reporting_gold.aws_lambda_function.this"]
NEW_MEMBERS = ("filled_report_values.py", "model_series_windows.py", "IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json")
UTC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
CLAIMS = ("measured", "inferred", "held", "absent")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "packet_blob", "landed_version_id", "version_id", "members", "code_sha256", "addresses", "ledger_entry", "apply_finished_utc", "packet_sha256", "zip_sha256", "zip_sha256_b64", "content_sha256")


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
def check_gates_build_plan(rec, packet_blob, coo_text, cto_text, ledger_exists, sha_hex_ok=True):
    exp = {"claim", "gates", "ledger_entry", "before", "build", "plan", "apply_finished_utc", "after", "invoke", "ledger_closed", "reads"}
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
         "one_change_at_a_time: the denominator (worktrees read) and zero markers")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists, "the ledger entry %s must exist" % LEDGER_SLUG)
    b = rec["before"]
    need(isinstance(b, dict) and set(b) == {"function", "policy_sids", "schedule", "filled_prefix_objects", "artifact_previous"}, "before keys")
    need(b["function"] == {"memory": 3008, "timeout": 900, "code_sha256": BEFORE_CODE_SHA}, "before.function differs from the packet's live state: %s" % b["function"])
    need(sorted(b["policy_sids"]) == sorted(SIDS_BEFORE), "before.policy_sids differ from the packet's seven")
    need(b["schedule"] == {"state": "ENABLED", "cron": CRON}, "before.schedule differs")
    need(is_int(b["filled_prefix_objects"]) and b["filled_prefix_objects"] >= 0 and isinstance(b["artifact_previous"], dict) and nes(b["artifact_previous"].get("version_id")), "before.filled_prefix_objects or artifact_previous")
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256", "zip_sha256_b64", "members", "import_smoke_rc", "landed_version_id", "content_sha256", "built_equals_landed"}, "build keys")
    need(re.fullmatch(r"[0-9a-f]{64}", str(bd["zip_sha256"])) and bd["zip_sha256_b64"] == b64_of_hex(bd["zip_sha256"]), "build.zip_sha256 and its base64 form must agree")
    need(isinstance(bd["members"], list) and "handler.py" in bd["members"] and all(any(m.endswith(n) for m in bd["members"]) for n in NEW_MEMBERS), "the zip must hold handler.py and the three new members")
    need(bd["import_smoke_rc"] == 0 and nes(bd["landed_version_id"]) and bd["content_sha256"] == bd["zip_sha256"] and bd["built_equals_landed"] is True, "the import smoke, the landed version or the built-equals-landed record")
    p = rec["plan"]
    need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "addresses", "memory_line", "policy_words", "replan_no_changes"}, "plan keys")
    need(p["add"] == 0 and p["change"] == 2 and p["destroy"] == 0 and sorted(p["addresses"]) == PLAN_ADDRESSES and p["replan_no_changes"] is True, "the plan must read 0 add / 2 change / 0 destroy on the two addresses, and a post-apply plan with no changes")
    need(nes(p["memory_line"]) and "8192" in p["memory_line"] and "3008" in p["memory_line"] and nes(p["policy_words"]), "plan.memory_line must show 3008 to 8192; policy_words required")
    return True


def check_after_record(rec):
    need(UTC.match(str(rec["apply_finished_utc"])), "apply_finished_utc must be an ISO UTC instant")
    a = rec["after"]
    need(isinstance(a, dict) and set(a) == {"function", "policy_sids", "schedule", "filled_prefix_objects"}, "after keys")
    f = a["function"]
    need(f["memory"] == 8192 and f["timeout"] == 900 and f["code_sha256"] == rec["build"]["zip_sha256_b64"], "after.function: memory 8192, timeout 900, code hash equal to the landed zip's")
    need(sorted(a["policy_sids"]) == SIDS_AFTER and a["schedule"] == {"state": "ENABLED", "cron": CRON}, "after.policy_sids or after.schedule")
    need(rec["invoke"] == {"count": 0}, "no invoke is permitted by this order")
    need(rec["ledger_closed"] is False, "the ledger must stay OPEN")
    need(rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "reads block")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    return True


# ------------------------------------------------------------------------------------------------ the live reads
def live(root):
    sys.path.insert(0, str(root))
    import boto3
    from lib import opal_naming
    lam, iam, s3 = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam"), boto3.client("s3")
    sch = boto3.client("scheduler", region_name="us-east-1")
    cfg = lam.get_function_configuration(FunctionName=FUNCTION)
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    names = [s["Name"] for s in sch.list_schedules(NamePrefix=SCHEDULE_PREFIX)["Schedules"]]
    need(len(names) == 1, "expected one schedule with the prefix %s, found %s" % (SCHEDULE_PREFIX, names))
    sc = sch.get_schedule(Name=names[0])
    addr = opal_naming.address("irpt", "49financial", "gold", "filled_report_values", "date=2000-01-03", "data.parquet")
    bucket, key = addr[len("s3://"):].split("/", 1)
    prefix = key.split("date=", 1)[0]
    objs, token = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        objs += [(o["Key"], o["LastModified"]) for o in r.get("Contents", [])]
        if not r.get("IsTruncated"):
            break
        token = r.get("NextContinuationToken")
    put = [s for s in sts if "s3:PutObject" in (s["Action"] if isinstance(s["Action"], list) else [s["Action"]])]
    put_res = sorted(put[0]["Resource"]) if len(put) == 1 and isinstance(put[0]["Resource"], list) else None
    return {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "handler": cfg["Handler"], "runtime": cfg["Runtime"], "role": cfg["Role"],
            "sids": sorted(s.get("Sid", "") for s in sts), "put_resources": put_res, "schedule": {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")},
            "filled_objects": objs, "filled_prefix": prefix, "bucket": bucket}


def run(root, cid):
    root = Path(root)
    rec = load(root, REC_REL)
    packet_blob = git(root, "hash-object", PACKET_REL).strip()
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8")
    need((root / CTO_HALF_REL).is_file(), "no CTO half")
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8")
    need(hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest() == PACKET_SHA, "the packet's bytes differ from the signed sha256")
    ledger_exists = bool(list((root / "org/critical_paths/change_management").glob("*%s*" % LEDGER_SLUG)))
    if cid == "DBB123-1-AC1":
        check_gates_build_plan(rec, packet_blob, coo, cto, ledger_exists)
        print("OK: gates (packet, both halves SIGNED, ancestry, one change at a time, live equals the packet), ledger %s, bundle built and landed equal (%s...), plan 0/2/0 on the two addresses with 3008 to 8192" %
              (LEDGER_SLUG, rec["build"]["zip_sha256"][:12]))
        return True
    check_gates_build_plan(rec, packet_blob, coo, cto, ledger_exists)
    check_after_record(rec)
    lv = live(root)
    if cid == "DBB123-2-AC1":
        need(lv["memory"] == 8192 and lv["timeout"] == 900 and lv["handler"] == "handler.lambda_handler" and lv["runtime"] == "python3.12" and lv["role"].endswith("role/" + ROLE),
             "live function: memory %s timeout %s handler %s runtime %s" % (lv["memory"], lv["timeout"], lv["handler"], lv["runtime"]))
        need(lv["code_sha256"] == rec["build"]["zip_sha256_b64"] == rec["after"]["function"]["code_sha256"], "live CodeSha256 %s differs from the landed zip's %s" % (lv["code_sha256"], rec["build"]["zip_sha256_b64"]))
        need(lv["sids"] == SIDS_AFTER, "live policy sids differ: %s" % lv["sids"])
        need(lv["put_resources"] is not None and len(lv["put_resources"]) == 6 and any("filled_report_values" in r for r in lv["put_resources"]), "the one PutObject statement must list six prefixes incl. filled_report_values")
        need(lv["schedule"] == {"state": "ENABLED", "cron": CRON, "zone": ZONE}, "live schedule changed: %s" % lv["schedule"])
        print("OK: live: memory 8192, timeout 900, CodeSha256 equals the landed zip's, %d policy statements incl. the four new, one PutObject statement of six prefixes, schedule unchanged" % len(lv["sids"]))
        return True
    if cid == "DBB123-3-AC1":
        finished = rec["apply_finished_utc"]
        old = [k for k, t in lv["filled_objects"] if t.strftime("%Y-%m-%dT%H:%M:%SZ") < finished]
        need(not old, "keys under the new prefix were written BEFORE the apply finished: %d" % len(old))
        need(rec["after"]["filled_prefix_objects"] == 0, "after.filled_prefix_objects at the apply must be 0")
        need((root / "org/critical_paths/.open_deploys" / (LEDGER_SLUG + ".json")).is_file(), "the ledger's open marker is missing: the ledger must stay OPEN")
        print("OK: the new prefix holds %d key(s), none written before the apply finished; no invoke; the ledger %s is open" % (len(lv["filled_objects"]), LEDGER_SLUG))
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    zh = "ab" * 32
    good = {"claim": "measured", "gates": {"packet_blob": "blob1", "packet_sha256": PACKET_SHA, "coo_half_signed": True, "cto_half_signed": True, "pin_is_ancestor": True,
            "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True}, "ledger_entry": LEDGER_SLUG,
            "before": {"function": {"memory": 3008, "timeout": 900, "code_sha256": BEFORE_CODE_SHA}, "policy_sids": list(SIDS_BEFORE), "schedule": {"state": "ENABLED", "cron": CRON},
                       "filled_prefix_objects": 0, "artifact_previous": {"version_id": "v1"}},
            "build": {"zip_sha256": zh, "zip_sha256_b64": b64_of_hex(zh), "members": ["handler.py", "data/x/filled_report_values.py", "data/y/model_series_windows.py", "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"],
                      "import_smoke_rc": 0, "landed_version_id": "v2", "content_sha256": zh, "built_equals_landed": True},
            "plan": {"add": 0, "change": 2, "destroy": 0, "addresses": list(PLAN_ADDRESSES), "memory_line": "memory_size: 3008 -> 8192", "policy_words": "w", "replan_no_changes": True},
            "apply_finished_utc": "2026-10-16T01:00:00Z",
            "after": {"function": {"memory": 8192, "timeout": 900, "code_sha256": b64_of_hex(zh)}, "policy_sids": list(SIDS_AFTER), "schedule": {"state": "ENABLED", "cron": CRON}, "filled_prefix_objects": 0},
            "invoke": {"count": 0}, "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    coo, cto = "SIGNED " + PACKET_SHA, "SIGNED " + PACKET_SHA[:12]

    def grade(r, blob="blob1", ledger=True, c=coo, t=cto):
        try:
            check_gates_build_plan(r, blob, c, t, ledger)
            check_after_record(r)
            return True
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    for name, f in (("plan add", lambda r: r["plan"].update(add=1)), ("plan change", lambda r: r["plan"].update(change=3)), ("address", lambda r: r["plan"]["addresses"].pop()),
                    ("memory after", lambda r: r["after"]["function"].update(memory=3008)), ("code hash", lambda r: r["after"]["function"].update(code_sha256="x")),
                    ("invoke", lambda r: r["invoke"].update(count=1)), ("ledger closed", lambda r: r.update(ledger_closed=True)), ("sids", lambda r: r["after"]["policy_sids"].pop()),
                    ("before drift", lambda r: r["before"]["function"].update(memory=4096)), ("zip b64", lambda r: r["build"].update(zip_sha256_b64="x")),
                    ("members", lambda r: r["build"].update(members=["handler.py"])), ("not equal", lambda r: r["build"].update(built_equals_landed=False)),
                    ("denominator", lambda r: r["gates"]["one_change_at_a_time"].update(worktrees_read=0)), ("marker", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1)),
                    ("extra key", lambda r: r.update(z=1)), ("digits", lambda r: r["plan"].update(policy_words="id 1234567890")), ("utc", lambda r: r.update(apply_finished_utc="soon"))):
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False, "red arm %s passed" % name
    assert grade(copy.deepcopy(good), blob="other") is False and grade(copy.deepcopy(good), ledger=False) is False
    assert grade(copy.deepcopy(good), c="DRAFT " + PACKET_SHA) is False and grade(copy.deepcopy(good), t="SIGNED deadbeef0000") is False
    assert b64_of_hex("00" * 32) == "A" * 43 + "="
    print("selftest: one green and %d red record arms behave" % 22)


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
