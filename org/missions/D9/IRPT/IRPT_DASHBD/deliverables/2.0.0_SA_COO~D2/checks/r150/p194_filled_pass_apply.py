"""IRPT_DASHBD round 150 (issuer 2.0.0_SA_COO~D2) -- the APPLY of the signed filled-report switch-on pair (packet NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md, sha256 3248f3c4; COO half a1e2575ac6, CTO half a824aebb24):
the bundle, a code-only safe-apply (0/1/0) with the OFF no-op probe, ONE safe-apply of the one environment variable (0/1/0), a dry run in 28 shards, ONE canary client, the mint leg and S2's V leg, the full pass in
28 shards, the after-read. WORLD, client-facing documents. The record is the applier's (`0.7.0_AE_CloudOps~IB2`); the checker re-reads the world and VALIDATES a sample of the written documents itself.

  DBC194-1-AC1  the record: both halves signed at the packet's sha256, the ledger, the build hash, the two plans, the OFF no-op, the dry run and the full pass by shard reconciling, the canary, the V leg, no id
  DBC194-2-AC1  FRESH live reads: the function runs the bundle with exactly the one environment variable; the role policy and the three schedules are as in the packet; the schedules' inputs carry no filled_report event
  DBC194-3-AC1  FRESH live reads of the data prefix: the filled objects equal the full pass's written total, the series and summary counts are unchanged, and a sample of the written documents validates against the contract

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                       the pure record clauses on synthetic arms
"""
import copy
import hashlib
import importlib.util
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


H = helper("r147/p151_pubapply.py", "p151_helper_194")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/FILLED_PASS_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS_CTO_HALF.md"
LEDGER_SLUG = "irpt-dashbd-49f-filled-report-switch-on-first-pass-20261017"
FUNCTION, ROLE, POLICY = "irpt-49f-reporting-publish-lambda", "irpt-49f-reporting-publish-role", "irpt-49f-reporting-publish-policy"
POLICY_HASH16, POLICY_STATEMENTS = "e6a7e585f3021a05", 8
BUILD_B64, MEMBERS = "4SF81dqnVu8rqP3xT0dWtQ8br1w9hvjQft/0knAtaic=", 17
CODE_BEFORE, VERSION_BEFORE = "s/OKOv98j53aFJCLrBpYP8xh3oUcuWagn0vSHVBjhIM=", "oXM0wQg8revg3asMHOhpbz1gPDnXaatK"
SCHEDULES = sorted(["irpt-49f-reporting-publish-daily", "irpt-49f-reporting-publish-summaries-daily", "irpt-49f-reporting-gold-daily"])
BUCKET, REPORTING_PREFIX = "opal-data-49financial", "irpt/49financial/platinum/reporting/"
OFF = {"enabled": False, "clients": 0, "written": 0, "not_available": [], "refused": []}
LABELS = ["code", "switch"]
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("packet_sha256", "email_digest12", "client_digest12", "request_id", "invoked_utc", "code_sha256", "zip_sha256_b64", "artifact_version_id", "version_id", "landed_version_id")


def count(x, lo=0):
    return is_int(x) and x >= lo


ZERO2 = ["000000000000", "000000000000"]


def check_shards(shards, label, expect_sum=None, mem_line=921):
    need(isinstance(shards, list) and len(shards) == 28 and [s.get("shard") for s in shards] == list(range(28)), "%s: 28 shards 0..27 in order (Addendum 1)" % label)
    for s in shards:
        need(set(s) == {"shard", "clients", "written", "not_available", "refused", "max_memory_mb", "duration_s"} and all(count(s[k]) for k in ("clients", "written", "not_available", "refused", "max_memory_mb"))
             and isinstance(s["duration_s"], (int, float)) and 0 <= s["duration_s"] <= 240 and s["max_memory_mb"] <= mem_line, "%s shard %s: counts, at most %d MB and 240 s (Addendum 1)" % (label, s.get("shard"), mem_line))
        need(s["written"] + s["not_available"] + s["refused"] == s["clients"], "%s shard %s: written + not_available + refused must equal the clients" % (label, s["shard"]))
    tot = {k: sum(s[k] for s in shards) for k in ("clients", "written", "not_available", "refused")}
    need(tot["refused"] * 10 <= tot["clients"], "%s: refused above 10 percent of the clients (Branch D)" % label)
    if expect_sum is not None:
        need(tot == expect_sum, "%s: the 28 shards must reconcile with the dry run: %s vs %s" % (label, tot, expect_sum))
    return tot


def check_head(rec, packet_sha, coo_text, cto_text, ledger_exists):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "build", "plans", "probe_off", "schedule_inputs", "dry_run", "canary", "v_leg", "full", "after", "ledger_closed", "reads", "notes"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    g = rec["gates"]
    need(isinstance(g, dict) and set(g) == {"packet_sha256", "coo_half_signed", "cto_half_signed", "one_change_at_a_time", "live_matches_packet"}, "gates keys")
    need(g["packet_sha256"] == packet_sha, "the packet's sha256 differs from the file at HEAD")
    need(g["coo_half_signed"] is True and "SIGNED" in coo_text and packet_sha in coo_text, "the COO half does not read SIGNED at the packet's sha256")
    need(g["cto_half_signed"] is True and "SIGNED" in cto_text and packet_sha[:8] in cto_text, "the CTO half does not read SIGNED at the packet's sha256")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and count(oc["worktrees_read"], 1) and oc["open_markers_naming_this_surface"] == 0, "one_change_at_a_time: the denominator and zero open legs on this surface")
    need(g["live_matches_packet"] is True and rec["ledger_entry"] == LEDGER_SLUG and ledger_exists and rec["applier"] == APPLIER, "live state matches the packet; the ledger %s exists; the applier is %s" % (LEDGER_SLUG, APPLIER))
    b = rec["before"]
    keys = {"code_sha256", "artifact_version_id", "env_keys", "schedules", "series_prefixes", "summary_objects", "filled_objects", "other_objects", "role_policy_hash16"}
    need(isinstance(b, dict) and set(b) == keys, "before keys")
    need(b["code_sha256"] == CODE_BEFORE and b["artifact_version_id"] == VERSION_BEFORE and b["env_keys"] == [] and sorted(b["schedules"]) == SCHEDULES and b["filled_objects"] == 0 and b["role_policy_hash16"] == POLICY_HASH16
         and all(count(b[k], 1) for k in ("series_prefixes", "summary_objects")) and count(b["other_objects"]), "before: the packet's section 2 (code hash, rollback version, no environment, three schedules, no filled object, the role policy)")
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"zip_sha256_b64", "members", "landed_version_id"} and bd["zip_sha256_b64"] == BUILD_B64 and bd["members"] == MEMBERS and nes(bd["landed_version_id"]) and bd["landed_version_id"] != VERSION_BEFORE,
         "build: the packet's hash %s (%d members) and a NEW landed version" % (BUILD_B64, MEMBERS))
    pl = rec["plans"]
    need(isinstance(pl, dict) and set(pl) == set(LABELS), "plans keys")
    for k in LABELS:
        p = pl[k]
        need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "replan_no_changes"} and (p["add"], p["change"], p["destroy"]) == (0, 1, 0) and p["replan_no_changes"] is True, "plan %s must read 0 add / 1 change / 0 destroy with a clean re-plan" % k)
    need(rec["probe_off"] == {"response": OFF, "payload_shape": "clients+shard+shards"}, "probe_off: the exact OFF no-op for an event that carries options")
    si = rec["schedule_inputs"]
    need(isinstance(si, dict) and si.get("checked") == 3 and si.get("none_contains_filled_report") is True and set(si) == {"checked", "none_contains_filled_report"}, "schedule_inputs: three schedules read, none sends a filled_report event")
    return True


def check_run(rec):
    dr = rec["dry_run"]
    need(isinstance(dr, dict) and set(dr) == {"directory_clients", "shards", "objects_before", "objects_after"} and count(dr["directory_clients"], 1) and dr["objects_before"] == dr["objects_after"] and count(dr["objects_before"]), "dry_run keys; the prefix object count must be EQUAL before and after (a dry run writes nothing)")
    tot = check_shards(dr["shards"], "dry run", mem_line=900)
    need(tot["clients"] == dr["directory_clients"], "dry run: the 28 shards' clients must sum to the directory's client count")
    need(tot["written"] >= 1, "dry run: at least one client would be written")
    c = rec["canary"]
    need(isinstance(c, dict) and set(c) == {"client_digest12", "dry_run_written", "clients", "written", "object_exists", "validates", "prefix_gain"}, "canary keys")
    need(re.fullmatch(r"[0-9a-f]{12}", str(c["client_digest12"])) and c["dry_run_written"] == 1 and c["clients"] == 1 and c["written"] == 1 and c["object_exists"] is True and c["validates"] is True and c["prefix_gain"] == 1,
         "canary: one client by digest, dry-run written 1, then written 1, the object exists, it validates, the prefix gained exactly 1")
    v = rec["v_leg"]
    need(isinstance(v, dict) and set(v) == {"principals", "signins_ok", "s2_step1", "s2_step2", "s2_step3", "leak", "removed", "absent_reads"}, "v_leg keys")
    need(isinstance(v["principals"], list) and len(v["principals"]) == 2 and all(re.fullmatch(r"[0-9a-f]{12}", str(x)) for x in v["principals"]) and v["signins_ok"] is (v["principals"] != ZERO2), "v_leg: two principals by digest, both signed in; or two zero digests and nothing signed in (nothing minted)")
    need(v["s2_step1"] == "PASS" and v["s2_step2"] in ("PASS", "OWED") and v["leak"] is False
         and (v["s2_step3"] == "PASS") == (v["principals"] != ZERO2) and (v["principals"] != ZERO2 or (v["s2_step2"] == "OWED" and v["s2_step3"] == "OWED")),
         "v_leg: step (1) PASS, no leak; minted: step (3) PASS; nothing minted: steps (2) and (3) both OWED (CTO msg 10467)")
    need(v["removed"] is True and isinstance(v["absent_reads"], list) and len(v["absent_reads"]) == 2 and all(isinstance(x, dict) and set(x) == {"gsi", "consistent"} and x["gsi"] == "ABSENT" and x["consistent"] == "ABSENT" for x in v["absent_reads"]),
         "v_leg: both rows removed and read ABSENT twice")
    f = rec["full"]
    need(isinstance(f, dict) and set(f) == {"shards", "written_total", "objects_before", "objects_after"}, "full keys")
    ft = check_shards(f["shards"], "full pass", expect_sum=tot, mem_line=900)
    need(f["written_total"] == ft["written"] and f["objects_after"] - f["objects_before"] == tot["written"] - 1, "full: written_total = the shards' sum; the prefix gained exactly (would-be total - 1), the canary already existed")
    return tot, ft


def check_after(rec, ft):
    a = rec["after"]
    keys = {"function", "role_policy_hash16", "schedules", "series_prefixes", "summary_objects", "filled_objects", "other_objects"}
    need(isinstance(a, dict) and set(a) == keys, "after keys")
    fn = a["function"]
    need(isinstance(fn, dict) and set(fn) == {"code_sha256", "memory_mb", "timeout_s", "env_keys", "layer", "reserved_concurrency"} and fn["code_sha256"] == BUILD_B64 and fn["memory_mb"] == 1024 and fn["timeout_s"] == 300
         and fn["env_keys"] == ["FILLED_REPORT_PASS"] and nes(fn["layer"]) and fn["reserved_concurrency"] is None, "after.function: the bundle's hash, 1,024 MB, 300 s, exactly FILLED_REPORT_PASS, the layer, no reserved concurrency")
    b = rec["before"]
    need(a["role_policy_hash16"] == POLICY_HASH16 and sorted(a["schedules"]) == SCHEDULES, "after: the role policy byte-identical and the three schedules ENABLED")
    need(a["series_prefixes"] == b["series_prefixes"] and a["summary_objects"] == b["summary_objects"] and a["other_objects"] == b["other_objects"], "after: series, summary and every other key count EQUAL to before")
    need(a["filled_objects"] == ft["written"], "after: the filled objects equal the full pass's written total")
    need(rec["ledger_closed"] is False and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "the ledger left OPEN for the issuer; the reads block")
    need(isinstance(rec["notes"], str) and 30 <= len(rec["notes"]) <= 3000, "notes: words")
    need(rec["v_leg"]["principals"] != ZERO2 or "no viewer session pair" in rec["notes"], "notes: when nothing was minted they say V-leg steps 2 and 3 are OWED: no viewer session pair (CTO msg 10467)")
    return True


def check_record(rec, packet_sha, coo_text, cto_text, ledger_exists):
    check_head(rec, packet_sha, coo_text, cto_text, ledger_exists)
    _, ft = check_run(rec)
    check_after(rec, ft)
    return True


def check_live_function(cfg, policy_doc, schedule_inputs):
    need(cfg["CodeSha256"] == BUILD_B64 and cfg["MemorySize"] == 1024 and cfg["Timeout"] == 300 and cfg["Handler"] == "handler.lambda_handler", "the function: the bundle's hash, 1,024 MB, 300 s, the handler")
    env = (cfg.get("Environment") or {}).get("Variables", {})
    need(env == {"FILLED_REPORT_PASS": "1"}, "the function's environment must be exactly FILLED_REPORT_PASS=1")
    need(len(policy_doc.get("Statement", [])) == POLICY_STATEMENTS and hashlib.sha256(json.dumps(policy_doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16] == POLICY_HASH16, "the role policy differs from the packet's pre-state")
    need(sorted(schedule_inputs) == SCHEDULES and all("filled_report" not in str(v) for v in schedule_inputs.values()), "the three schedules' inputs must not carry a filled_report event")
    return True


def check_live_data(rec, filled_keys, series, summaries, others, sample_ok):
    need(len(filled_keys) == rec["after"]["filled_objects"] == rec["full"]["written_total"], "the live filled objects (%d) differ from the record" % len(filled_keys))
    need(series == rec["after"]["series_prefixes"] and summaries == rec["after"]["summary_objects"] and others == rec["after"]["other_objects"], "the live series, summary or other object counts differ from the record")
    need(sample_ok, "a sampled written document does not validate against the contract")
    return True


def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    packet_sha = hashlib.sha256((root / PACKET_REL).read_bytes()).hexdigest()
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8") if (root / COO_HALF_REL).is_file() else ""
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8") if (root / CTO_HALF_REL).is_file() else ""
    ledger_exists = bool(list((root / "org/critical_paths/.open_deploys").glob(LEDGER_SLUG + "*.json"))) or bool(list((root / "org/critical_paths/change_management").glob("*" + LEDGER_SLUG + "*")))
    check_record(rec, packet_sha, coo, cto, ledger_exists)
    scrub = dict(rec, notes=re.sub(r"[a-z][a-z0-9-]*-\d{8}", "ledger", str(rec["notes"])),
                 v_leg=dict(rec["v_leg"], principals=["zero" if x == "0" * 12 else x for x in rec["v_leg"]["principals"]]))  # the order's zero digest is a placeholder, not an id
    need(not H.digit_runs(scrub), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(scrub)[:2])
    if cid == "DBC194-1-AC1":
        print("OK: both halves signed at the packet's sha256, the ledger, the build hash, the two plans, the exact OFF no-op, the dry run and the full pass reconciling by shard, the canary, the V leg, no id")
        return True
    import boto3
    lam = boto3.client("lambda", region_name="us-east-1")
    if cid == "DBC194-2-AC1":
        iam, sch = boto3.client("iam"), boto3.client("scheduler", region_name="us-east-1")
        inputs = {}
        for name in SCHEDULES:
            try:
                s = sch.get_schedule(Name=name)
                inputs[name] = s["Target"].get("Input", "")
            except Exception as ex:  # noqa: BLE001
                need(False, "schedule %s could not be read (%s)" % (name, type(ex).__name__))
        check_live_function(lam.get_function_configuration(FunctionName=FUNCTION), iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"], inputs)
        print("OK: live: the function runs the bundle with exactly FILLED_REPORT_PASS=1; the role policy is the packet's pre-state; the three schedules' inputs carry no filled_report event")
        return True
    if cid == "DBC194-3-AC1":
        s3 = boto3.client("s3")
        filled, series, summaries, others = [], 0, 0, 0
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=REPORTING_PREFIX):
            for o in page.get("Contents", []):
                rest = o["Key"][len(REPORTING_PREFIX):]
                if rest.startswith("client=") and rest.endswith("/filled_report.json"):
                    filled.append(o["Key"])
                elif rest.startswith("client=") and rest.endswith("/summary.json"):
                    summaries += 1
                elif rest.startswith("account=") and rest.endswith("/series.json.gz"):
                    series += 1
                else:
                    others += 1
        sys.path.insert(0, str(root / "infra/aws/lambda/investor-reporting/reporting-publish"))
        sys.path.insert(0, str(root))
        import publisher
        sample = sorted(filled)[:: max(1, len(filled) // 25)][:25]
        ok = True
        for k in sample:
            try:
                publisher.validate_filled_report(json.loads(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read()))
            except Exception:  # noqa: BLE001 -- the key is never printed
                ok = False
        need(len(filled) == rec["after"]["filled_objects"] == rec["full"]["written_total"], "the live filled objects (%d) differ from the record" % len(filled))
        need(summaries == rec["after"]["summary_objects"] and others == rec["after"]["other_objects"], "the live summary or other object counts differ from the record")
        need(ok, "a sampled written document does not validate against the contract (%d sampled)" % len(sample))
        print("OK: live: %d filled objects as recorded, the summary and other counts unchanged, %d sampled documents validate against the contract" % (len(filled), len(sample)))
        return True
    raise Fail("unknown criterion %s" % cid)


def synthetic():
    sh = lambda i, c, w, na, rf: {"shard": i, "clients": c, "written": w, "not_available": na, "refused": rf, "max_memory_mb": 400, "duration_s": 40.0}  # noqa: E731
    dry = [sh(i, 150 + (i % 3), 145 + (i % 3), 4, 1) for i in range(28)]
    full = copy.deepcopy(dry)
    tw = sum(s["written"] for s in dry)
    rec = {"claim": "measured", "gates": {"packet_sha256": "p" * 64, "coo_half_signed": True, "cto_half_signed": True, "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
           "ledger_entry": LEDGER_SLUG, "applier": APPLIER,
           "before": {"code_sha256": CODE_BEFORE, "artifact_version_id": VERSION_BEFORE, "env_keys": [], "schedules": SCHEDULES, "series_prefixes": 3000, "summary_objects": 2000, "filled_objects": 0, "other_objects": 10, "role_policy_hash16": POLICY_HASH16},
           "build": {"zip_sha256_b64": BUILD_B64, "members": MEMBERS, "landed_version_id": "newversion"},
           "plans": {"code": {"add": 0, "change": 1, "destroy": 0, "replan_no_changes": True}, "switch": {"add": 0, "change": 1, "destroy": 0, "replan_no_changes": True}},
           "probe_off": {"response": OFF, "payload_shape": "clients+shard+shards"}, "schedule_inputs": {"checked": 3, "none_contains_filled_report": True},
           "dry_run": {"directory_clients": sum(s["clients"] for s in dry), "shards": dry, "objects_before": 5010, "objects_after": 5010},
           "canary": {"client_digest12": "a" * 12, "dry_run_written": 1, "clients": 1, "written": 1, "object_exists": True, "validates": True, "prefix_gain": 1},
           "v_leg": {"principals": list(ZERO2), "signins_ok": False, "s2_step1": "PASS", "s2_step2": "OWED", "s2_step3": "OWED", "leak": False, "removed": True, "absent_reads": [{"gsi": "ABSENT", "consistent": "ABSENT"}] * 2},
           "full": {"shards": full, "written_total": tw, "objects_before": 5011, "objects_after": 5011 + tw - 1},
           "after": {"function": {"code_sha256": BUILD_B64, "memory_mb": 1024, "timeout_s": 300, "env_keys": ["FILLED_REPORT_PASS"], "layer": "irpt-performance-native-layer:1", "reserved_concurrency": None},
                     "role_policy_hash16": POLICY_HASH16, "schedules": SCHEDULES, "series_prefixes": 3000, "summary_objects": 2000, "filled_objects": tw, "other_objects": 10},
           "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}, "notes": "Counts, digests and statuses only; the page has not been looked at; V-leg steps 2 and 3 OWED: no viewer session pair; written documents stay on a rollback."}
    return rec


def selftest():
    rec = synthetic()
    coo, cto = "SIGNED " + "p" * 64, "SIGNED " + "p" * 8
    # the synthetic full pass reconciles with the dry run by construction; objects_before for the full pass is after the canary
    rec["full"]["objects_before"] = rec["dry_run"]["objects_after"] + 1

    def go(r, **kw):
        return check_record(r, kw.get("sha", "p" * 64), kw.get("coo", coo), kw.get("cto", cto), kw.get("led", True))
    assert go(rec)
    n = 0

    def red(fn, label):
        nonlocal n
        try:
            fn()
        except Fail:
            n += 1
            return
        raise AssertionError("mutant passed: " + label)

    def mut(label, fn):
        r = copy.deepcopy(rec)
        fn(r)
        red(lambda: go(r), label)
    red(lambda: go(rec, sha="q" * 64), "packet sha")
    red(lambda: go(rec, coo="DRAFT"), "coo unsigned")
    red(lambda: go(rec, cto="SIGNED"), "cto unbound")
    red(lambda: go(rec, led=False), "ledger missing")
    mut("claim", lambda r: r.update(claim="inferred"))
    mut("open legs", lambda r: r["gates"]["one_change_at_a_time"].update(open_markers_naming_this_surface=1))
    mut("before env", lambda r: r["before"].update(env_keys=["FILLED_REPORT_PASS"]))
    mut("before filled", lambda r: r["before"].update(filled_objects=3))
    mut("before code", lambda r: r["before"].update(code_sha256="x="))
    mut("build hash", lambda r: r["build"].update(zip_sha256_b64="B" * 43 + "="))
    mut("landed version", lambda r: r["build"].update(landed_version_id=VERSION_BEFORE))
    mut("code plan", lambda r: r["plans"]["code"].update(add=1))
    mut("switch plan", lambda r: r["plans"]["switch"].update(destroy=1))
    mut("replan", lambda r: r["plans"]["switch"].update(replan_no_changes=False))
    mut("off probe", lambda r: r["probe_off"].update(response=dict(OFF, enabled=True)))
    mut("schedule inputs", lambda r: r["schedule_inputs"].update(none_contains_filled_report=False))
    mut("dry shards", lambda r: r["dry_run"]["shards"].pop())
    mut("dry memory", lambda r: r["dry_run"]["shards"][0].update(max_memory_mb=901))
    mut("full memory", lambda r: r["full"]["shards"][0].update(max_memory_mb=922))
    mut("seven shards", lambda r: (r["dry_run"].update(shards=r["dry_run"]["shards"][:7])))
    mut("dry time", lambda r: r["dry_run"]["shards"][0].update(duration_s=241))
    mut("dry shard sum", lambda r: r["dry_run"]["shards"][1].update(written=1))
    mut("dry refused rate", lambda r: (r["dry_run"]["shards"][0].update(refused=500, written=90), r["full"]["shards"][0].update(refused=500, written=90)))
    mut("dry wrote", lambda r: r["dry_run"].update(objects_after=5020))
    mut("directory sum", lambda r: r["dry_run"].update(directory_clients=1))
    mut("canary written", lambda r: r["canary"].update(written=2))
    mut("canary validates", lambda r: r["canary"].update(validates=False))
    mut("canary digest", lambda r: r["canary"].update(client_digest12="cli_S01"))
    mut("canary gain", lambda r: r["canary"].update(prefix_gain=2))
    mut("v leak", lambda r: r["v_leg"].update(leak=True))
    mut("v step1", lambda r: r["v_leg"].update(s2_step1="FAIL"))
    mut("v step3 PASS with nothing minted", lambda r: r["v_leg"].update(s2_step3="PASS"))
    mut("v step2 PASS with nothing minted", lambda r: r["v_leg"].update(s2_step2="PASS"))
    mut("v signin with nothing minted", lambda r: r["v_leg"].update(signins_ok=True))
    mut("notes without the reason", lambda r: r.update(notes="Counts, digests and statuses only; the page has not been looked at; written documents stay."))
    mut("v removal", lambda r: r["v_leg"].update(removed=False))
    mut("v present", lambda r: r["v_leg"]["absent_reads"][1].update(consistent="PRESENT"))
    mut("v one read", lambda r: r["v_leg"]["absent_reads"].pop())
    mut("full vs dry", lambda r: r["full"]["shards"][2].update(written=1, refused=4))
    mut("full gain", lambda r: r["full"].update(objects_after=r["full"]["objects_after"] + 1))
    mut("full total", lambda r: r["full"].update(written_total=1))
    mut("after env", lambda r: r["after"]["function"].update(env_keys=["FILLED_REPORT_PASS", "X"]))
    mut("after code", lambda r: r["after"]["function"].update(code_sha256="x="))
    mut("after memory", lambda r: r["after"]["function"].update(memory_mb=2048))
    mut("after policy", lambda r: r["after"].update(role_policy_hash16="0" * 16))
    mut("after series", lambda r: r["after"].update(series_prefixes=2999))
    mut("after summaries", lambda r: r["after"].update(summary_objects=1999))
    mut("after filled", lambda r: r["after"].update(filled_objects=1))
    mut("ledger closed", lambda r: r.update(ledger_closed=True))
    mut("reads", lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}))
    mut("extra key", lambda r: r.update(z=1))
    cfg = {"CodeSha256": BUILD_B64, "MemorySize": 1024, "Timeout": 300, "Handler": "handler.lambda_handler", "Environment": {"Variables": {"FILLED_REPORT_PASS": "1"}}}
    pol = {"Statement": [{"i": i} for i in range(POLICY_STATEMENTS)]}
    saved = globals()["POLICY_HASH16"]
    globals()["POLICY_HASH16"] = hashlib.sha256(json.dumps(pol, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]
    try:
        ins = {s: '{"summaries": true}' for s in SCHEDULES}
        assert check_live_function(cfg, pol, ins)
        red(lambda: check_live_function(dict(cfg, Environment={"Variables": {"FILLED_REPORT_PASS": "0"}}), pol, ins), "live switch value")
        red(lambda: check_live_function(dict(cfg, Environment={"Variables": {"FILLED_REPORT_PASS": "1", "X": "1"}}), pol, ins), "live extra variable")
        red(lambda: check_live_function(dict(cfg, CodeSha256="x="), pol, ins), "live code")
        red(lambda: check_live_function(cfg, {"Statement": pol["Statement"][:-1]}, ins), "live policy")
        red(lambda: check_live_function(cfg, pol, dict(ins, **{SCHEDULES[0]: '{"filled_report": true}'})), "a schedule sends the event")
        red(lambda: check_live_function(cfg, pol, {SCHEDULES[0]: "{}"}), "a schedule missing")
    finally:
        globals()["POLICY_HASH16"] = saved
    keys = ["k%d" % i for i in range(rec["after"]["filled_objects"])]
    assert check_live_data(rec, keys, 3000, 2000, 10, True)
    red(lambda: check_live_data(rec, keys[:-1], 3000, 2000, 10, True), "live filled count")
    red(lambda: check_live_data(rec, keys, 2999, 2000, 10, True), "live series")
    red(lambda: check_live_data(rec, keys, 3000, 1999, 10, True), "live summaries")
    red(lambda: check_live_data(rec, keys, 3000, 2000, 11, True), "live others")
    red(lambda: check_live_data(rec, keys, 3000, 2000, 10, False), "a sample does not validate")
    print("selftest: green on the synthetic record and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
        sys.exit(0)
    try:
        run(sys.argv[1], sys.argv[2])
        print(sys.argv[2] + " PASS")
    except Exception as e:  # a failed read is a FAIL, not a traceback
        print("FAIL: " + str(e))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
