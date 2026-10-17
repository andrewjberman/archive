"""IRPT_DASHBD TO-DB-f-2204 (applier 0.7.0_AE_CloudOps~IB2): the reads and the three invokes of the 49 Financial transaction-table apply.

  python tx2204.py gates                  AMENDMENT 2 R0: packet bytes, halves, ADDENDUM 1, re-pin checks, one-change-at-a-time census, live state vs the state after the first apply (read only)
  python tx2204.py first_apply            the first apply as it was -> state2204_r2/first_apply.json (copied from state2204/)
  python tx2204.py before                 the BEFORE state -> state2204/before.json
  python tx2204.py after_apply <UTC>      the function, policy and schedule after the apply -> state2204/after.json
  python tx2204.py invoke dry|write|range ONE synchronous invoke (never retried here) -> state2204/<name>_invoke.json, with its after-read
  python tx2204.py trigger                the time trigger from the dry run and the last pre-apply fire -> state2204/time_trigger.json
  python tx2204.py compile                assemble TRANSACTION_APPLY_RECORD.json from state2204/

Counts, dates, keys, hashes and words only: no account id is printed or written.
"""
import base64
import datetime as dt
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import boto3
from botocore.config import Config

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, cwd=str(Path(__file__).resolve().parent)).strip())
HERE = Path(__file__).resolve().parent
STATE = HERE / "state2204_r2"  # AMENDMENT 2 (the re-stage): a fresh state folder; the first apply and its stopped dry run stay in state2204/
FIRST = HERE / "state2204"
CHK_PATH = ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/p136_apply.py"
spec = importlib.util.spec_from_file_location("p136_for_tx2204", str(CHK_PATH))
chk = importlib.util.module_from_spec(spec)
sys.modules["p136_for_tx2204"] = chk
spec.loader.exec_module(chk)

REGION = "us-east-1"
FUNCTION, ROLE, POLICY, SCHEDULE = chk.FUNCTION, chk.ROLE, chk.POLICY, chk.SCHEDULE
SIDS, WRITE_SID, OTHER = chk.SIDS, chk.WRITE_SID, chk.OTHER_TABLES
ART_BUCKET, ART_KEY = "opal-313476888478-lambda-artifacts", "investor-reporting/irpt-reporting-gold-lambda.zip"
BUCKET, TX_PREFIX, NEW_RESOURCE, OTHER_PREFIX = chk.addresses(str(ROOT))
SURFACE = re.compile(r"reporting-gold|reporting_gold|gold/account_transaction", re.I)
OWN_SLUG = "irpt-dashbd-49f-transaction-wiring-20261016"
PINS = {"infra/aws/lambda/investor-reporting/reporting-gold/handler.py": "29099416ca56",
        "data/assets/scripts/gold/irpt_reporting/account_transaction.py": "3b859c6d7440",
        "data/assets/scripts/gold/irpt_reporting/transaction_words.json": "996d7c304fdb",
        "infra/aws/terraform/investor-reporting/reporting-gold/locals.tf": "eb629c95b43d",
        "infra/aws/terraform/investor-reporting/reporting-gold/iam.tf": "a9b82429beeb",
        "infra/aws/terraform/investor-reporting/reporting-gold/lambda.tf": "a20ea4a0a21c",
        "infra/aws/terraform/investor-reporting/reporting-gold/main.tf": "782bb1348099",
        "infra/aws/terraform/investor-reporting/reporting-gold/schedule.tf": "6f92147a2a18"}
iam = boto3.client("iam", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)
sch = boto3.client("scheduler", region_name=REGION)
lam_read = boto3.client("lambda", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)


def now_utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def load_first(name):
    return json.loads((FIRST / name).read_text(encoding="ascii"))


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT)).stdout


def policy_doc():
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    return doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]


def policy_hashes():
    return {x["Sid"]: chk.statement_hash(x) for x in policy_doc()}


def write_resources():
    res = [x for x in policy_doc() if x["Sid"] == WRITE_SID][0]["Resource"]
    return [res] if isinstance(res, str) else list(res)


def schedule():
    sc = sch.get_schedule(Name=SCHEDULE)
    return {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")}


def artifact_current():
    vs = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=ART_BUCKET, Prefix=ART_KEY):
        vs += [v for v in pg.get("Versions", []) if v["Key"] == ART_KEY]
    return [v for v in vs if v["IsLatest"]][0]["VersionId"], len(vs)


def day_partitions(prefix):
    out = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix, Delimiter="/"):
        out += [c["Prefix"].rstrip("/").rsplit("date=", 1)[-1] for c in pg.get("CommonPrefixes", [])]
    return sorted(out)


def prefix_objects(prefix):
    return sum(len(pg.get("Contents", [])) for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix))


def other_tables():
    out = {}
    for t, pref in OTHER_PREFIX.items():
        days = day_partitions(pref)
        out[t] = {"partitions": len(days), "newest": days[-1] if days else None}
    return out


def last_fire():
    """The latest REPORT line of the function's log group before the apply: the last scheduled fire's duration (the schedule is the only invoker)."""
    group = "/aws/lambda/" + FUNCTION
    t0 = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=4)).timestamp() * 1000)
    reports = []
    for pg in logs.get_paginator("filter_log_events").paginate(logGroupName=group, startTime=t0, filterPattern="REPORT"):
        for e in pg["events"]:
            m = re.search(r"REPORT RequestId: (\S+)\s+Duration: ([0-9.]+) ms.*?Max Memory Used: (\d+) MB", e["message"], re.S)
            if m:
                reports.append((e["timestamp"], float(m.group(2)), int(m.group(3))))
    reports.sort()
    return reports


def cmd_gates():
    packet = chk.PACKET_REL
    blob = git("hash-object", packet).strip()
    sha = hashlib.sha256((ROOT / packet).read_bytes()).hexdigest()
    coo = (ROOT / chk.COO_REL).read_text(encoding="utf-8")
    cto = (ROOT / chk.CTO_REL).read_text(encoding="utf-8")
    coo_ok = "SIGNED" in coo and chk.PACKET_SHA in coo
    cto_ok = "SIGNED" in cto and chk.PACKET_SHA in cto
    pins = {Path(p).name: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:12] == h for p, h in PINS.items()}
    wts = [ln[9:] for ln in git("worktree", "list", "--porcelain").splitlines() if ln.startswith("worktree ")]
    stale, live = 0, []
    for wt in wts:
        for n in [x for x in git("-C", wt, "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/.open_deploys/").split("\n") if x.strip()]:
            if SURFACE.search(git("-C", wt, "show", "HEAD:" + n)):
                slug = Path(n).stem
                if slug == OWN_SLUG:
                    continue
                led = list((ROOT / "org/critical_paths/change_management").glob("*_%s_deploy_completion.md" % slug))
                head = led[0].read_text(encoding="utf-8", errors="replace")[:1500] if led else ""
                if "**Status:** CLOSED" in head or "**Status:** ROLLED-BACK" in head:
                    stale += 1
                else:
                    live.append((wt, n))
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    conc = lam_read.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    cur, nvers = artifact_current()
    scs = schedule()
    wr = write_resources()
    newobj = prefix_objects(TX_PREFIX)
    live_ok = (cfg["CodeSha256"] == chk.FIRST_BUILD_B64 and cfg["MemorySize"] == 8192 and cfg["Timeout"] == 900 and conc is None and not (cfg.get("Environment") or {}).get("Variables")
               and cur == chk.FIRST_ARTIFACT_VERSION and scs["state"] == "ENABLED" and sorted(policy_hashes()) == sorted(SIDS) and len(wr) == 7 and NEW_RESOURCE in wr and newobj == 0)
    p137 = str(ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r136/p137_repin.py")
    repin = {}
    for cid in ("DBF137-1-AC1", "DBF137-1-AC2"):
        r = subprocess.run([sys.executable, "-I", p137, str(ROOT), cid], capture_output=True, text=True, cwd=str(ROOT))
        repin[cid] = (r.returncode == 0 and (cid + " PASS") in r.stdout)
    cto_a1 = ("ADDENDUM 1" in cto) and ("COUNTERSIGN" in coo.upper() or "COUNTERSIGN" in cto.upper())
    gates = {"packet_blob": blob, "packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok, "addendum_1_signed": bool(cto_a1), "pins_ok": bool(all(repin.values())),
             "one_change_at_a_time": {"worktrees_read": len(wts), "open_markers_naming_this_surface": len(live)}}
    print("GATES addendum_1_signed=%s repin_checks=%s original_pins_ok=%s" % (cto_a1, repin, all(pins.values())))
    print("GATES blob=%s sha_ok=%s coo=%s cto=%s" % (blob[:12], sha == chk.PACKET_SHA, coo_ok, cto_ok))
    print("GATES pins %s" % pins)
    print("GATES worktrees_read=%d stale_closed_slugs=%d live_markers_naming_surface=%d %s" % (len(wts), stale, len(live), live[:3]))
    print("GATES live: code_ok=%s mem=%s timeout=%s conc=%s env=%s artifact_current_ok=%s (artifact versions %d) schedule=%s sids_ok=%s write_resources=%d new_prefix_objects=%d -> live_ok=%s" % (
        cfg["CodeSha256"] == chk.FIRST_BUILD_B64, cfg["MemorySize"], cfg["Timeout"], conc, bool((cfg.get("Environment") or {}).get("Variables")), cur == chk.FIRST_ARTIFACT_VERSION, nvers, scs,
        sorted(policy_hashes()) == sorted(SIDS), len(wr), newobj, live_ok))
    save("gates.json", gates)
    save("gates_live_ok.json", {"live_ok": bool(live_ok), "at": now_utc()})
    return 0 if (sha == chk.PACKET_SHA and coo_ok and cto_ok and gates["addendum_1_signed"] and gates["pins_ok"] and not live and live_ok) else 3


def cmd_before():
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    cur, _n = artifact_current()
    ot = other_tables()
    reports = last_fire()
    old = load_first("before.json")["last_fire"]  # the last SCHEDULED fire (patched at the first run); my own dry-run invokes are not scheduled fires
    out = {"function_code_sha256": cfg["CodeSha256"], "artifact_version_id": cur, "policy": policy_hashes(), "write_resources": write_resources(), "new_prefix_objects": prefix_objects(TX_PREFIX),
           "schedule": {k: v for k, v in schedule().items() if k != "zone"},
           "last_fire": old,
           "other_tables": ot, "newest_returns_day": ot["account_return_daily"]["newest"]}
    save("before.json", out)
    save("before_extra.json", {"report_lines_4d": [{"utc": dt.datetime.fromtimestamp(r[0] / 1000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "duration_ms": r[1], "max_memory_mb": r[2]} for r in reports]})
    print("BEFORE code=%s artifact_current=%s sids=%d write_resources=%d new_prefix_objects=%d schedule=%s" % (out["function_code_sha256"], cur, len(out["policy"]), len(out["write_resources"]), out["new_prefix_objects"], out["schedule"]))
    print("BEFORE last_fire=%s (REPORT lines in 4 days: %d)" % (out["last_fire"], len(reports)))
    print("BEFORE other_tables=%s newest_returns_day=%s (packet time: 572, 7, 7, 7, 7, 1 partitions)" % ({t: (v["partitions"], v["newest"]) for t, v in ot.items()}, out["newest_returns_day"]))
    ok = (out["function_code_sha256"] == chk.FIRST_BUILD_B64 and cur == chk.FIRST_ARTIFACT_VERSION and sorted(out["policy"]) == sorted(SIDS) and len(out["write_resources"]) == 7
          and NEW_RESOURCE in out["write_resources"] and out["new_prefix_objects"] == 0 and old.get("duration_ms") is not None)
    return 0 if ok else 3


def cmd_first_apply():
    plan, fin, bld = load_first("plan.json"), load_first("apply_finished.json"), load_first("build.json")
    out = {"code_sha256": chk.FIRST_BUILD_B64, "landed_version_id": bld["landed_version_id"], "plan": {"add": plan["add"], "change": plan["change"], "destroy": plan["destroy"]},
           "policy_added_resources": plan["policy_added_resources"], "apply_finished_utc": fin["apply_finished_utc"]}
    save("first_apply.json", out)
    print("FIRST_APPLY %s" % out)
    return 0 if (out["landed_version_id"] == chk.FIRST_ARTIFACT_VERSION and (plan["add"], plan["change"], plan["destroy"]) == (0, 2, 0)) else 3


def cmd_after_apply(utc):
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    conc = lam_read.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    layers = [x["Arn"] for x in cfg.get("Layers", [])]
    out = {"function": {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "reserved_concurrency": conc, "code_sha256": cfg["CodeSha256"], "layer_arn": layers[0] if layers else None},
           "policy": policy_hashes(), "write_resources": write_resources(), "schedule": schedule()}
    save("after.json", out)
    save("apply_finished.json", {"apply_finished_utc": utc})
    b = load("before.json")
    differ = sorted(s for s in out["policy"] if out["policy"][s] != b["policy"].get(s))
    print("AFTER code=%s memory=%s timeout=%s conc=%s layers=%d handler=%s runtime=%s env=%s" % (cfg["CodeSha256"], cfg["MemorySize"], cfg["Timeout"], conc, len(layers), cfg["Handler"], cfg["Runtime"], bool((cfg.get("Environment") or {}).get("Variables"))))
    print("AFTER policy statements differing from before: %s ; write_resources=%d last_is_new=%s schedule_equal_before=%s" % (differ, len(out["write_resources"]), out["write_resources"][-1] == NEW_RESOURCE,
                                                                                                                      {k: v for k, v in out["schedule"].items() if k != "zone"} == b["schedule"]))
    return 0


def range_start(d):
    sys.path.insert(0, str(ROOT / "lib"))
    import trading_calendar as tc
    days = [d]
    cur = dt.date.fromisoformat(d)
    while len(days) < 25:
        cur = tc.prev_trading_day(cur)
        days.append(cur.isoformat())
    return days[-1]


def schema_hash(table):
    """sha256 over the sorted name:type lines of the parquet's schema (the contract's rule; checked against the packet's value as a control)."""
    lines = sorted("%s:%s" % (f.name, f.type) for f in table.schema)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest(), len(table.schema)


def read_day(day):
    import pyarrow.parquet as pq
    pref = "%sdate=%s/" % (TX_PREFIX, day)
    keys = [o["Key"] for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=pref) for o in pg.get("Contents", [])]
    data = [k for k in keys if k.endswith(".parquet")]
    return keys, pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=data[0])["Body"].read())) if data else None


def cmd_invoke(name):
    if (STATE / ("%s_invoke.json" % name)).exists():
        print("REFUSED: %s was already invoked (state file present)" % name)
        return 2
    b = load("before.json")
    d = b["newest_returns_day"]
    if name != "dry" and not (STATE / ("%s_check.json" % ("dry" if name == "write" else "write"))).exists():
        print("REFUSED: the previous act's check is not recorded")
        return 2
    if name == "range" and load("time_trigger.json")["over_720s"]:
        print("REFUSED: the time trigger fired; the rollback comes first")
        return 2
    start = range_start(d) if name == "range" else d
    payload = {"backfill": {"start": start, "end": d}, "accounts": "population", "stages": ["transaction"]}
    if name == "dry":
        payload["dry_run"] = True
    t = now_utc()
    tt = dt.datetime.now(dt.timezone.utc)
    if tt.weekday() < 5 and dt.time(11, 35) <= tt.time() <= dt.time(12, 0):
        print("STOP: inside the fire window")
        return 3
    cfg = Config(read_timeout=960, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"})
    lam = boto3.client("lambda", region_name=REGION, config=cfg)
    save("%s_invoking.json" % name, {"payload": payload, "invoked_utc": t})
    print("INVOKE %s sending at %s payload=%s" % (name, t, json.dumps(payload)), flush=True)
    resp = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse", LogType="Tail", Payload=json.dumps(payload).encode("ascii"))
    body = json.loads(resp["Payload"].read().decode("utf-8"))
    log = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
    m = re.search(r"REPORT RequestId: (\S+)\s+Duration: ([0-9.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", log, re.S)
    ret = {"stages": body.get("stages") if isinstance(body, dict) else None, "transaction_rows": (body or {}).get("transaction_rows") if isinstance(body, dict) else None,
           "transaction_failed": (body or {}).get("transaction_failed") if isinstance(body, dict) else None}
    rec = {"payload": payload, "invoked_utc": t, "status_code": resp["StatusCode"], "function_error": resp.get("FunctionError"), "returned": ret,
           "report": ({"max_memory_used_mb": int(m.group(4)), "duration_ms": float(m.group(2)), "memory_size_mb": int(m.group(3))} if m else None), "request_id": m.group(1) if m else None,
           "raw_keys": sorted(body) if isinstance(body, dict) else None}
    save("%s_invoke.json" % name, rec)
    print("INVOKE %s status=%s function_error=%s returned=%s raw_keys=%s report=%s request_id=%s" % (name, rec["status_code"], rec["function_error"], ret, rec["raw_keys"], rec["report"], rec["request_id"]))
    problems = []
    if rec["function_error"] or not m or "Task timed out" in log or "AccessDenied" in log:
        problems.append("function error, no REPORT line, a timeout or an AccessDenied: %s" % log[:300].replace("\n", " "))
    if rec["report"] and (rec["report"]["max_memory_used_mb"] > 6553 or rec["report"]["duration_ms"] > 720000):
        problems.append("memory above 6553 MB or duration above 720000 ms: %s" % rec["report"])
    if ret["stages"] != ["transaction"] or ret["transaction_failed"] != {} or not isinstance(ret["transaction_rows"], dict):
        problems.append("returned shape: %s" % ret)
    check = {}
    parts = day_partitions(TX_PREFIX)
    objs = prefix_objects(TX_PREFIX)
    if name == "dry":
        check = {"prefix_objects_after": objs}
        if objs != 0 or len(ret["transaction_rows"] or {}) != 1 or not all(isinstance(v, int) and v > 0 for v in (ret["transaction_rows"] or {}).values()):
            problems.append("dry run: objects at the new prefix %d, rows %s" % (objs, ret["transaction_rows"]))
    elif name == "write":
        dry = load("dry_invoke.json")
        keys, tbl = read_day(d)
        sh, ncols = schema_hash(tbl) if tbl is not None else (None, None)
        claims = tbl["business_date_claim"].to_pylist() if tbl is not None else []
        bdates, tdates = (tbl["business_date"].to_pylist(), tbl["trade_date"].to_pylist()) if tbl is not None else ([], [])
        claims_ok = bool(claims) and all(c in ("measured", "inferred") for c in claims) and all((c == "inferred") == (str(bd) != str(td)) for c, bd, td in zip(claims, bdates, tdates))
        enum = ("EXTERNAL_IN", "EXTERNAL_OUT", "INCOME", "FEE", "INTERNAL", "CORPORATE_ACTION", "UNRESOLVED")
        flow_ok = tbl is not None and all(f in enum for f in tbl["flow_class"].to_pylist())
        check = {"partitions_after": ["date=%s" % p for p in parts], "columns": ncols, "schema_hash": sh, "claims_ok": claims_ok, "flow_class_ok": bool(flow_ok), "same_count_as_dry": ret["transaction_rows"] == dry["returned"]["transaction_rows"],
                 "rows_in_object": tbl.num_rows if tbl is not None else None}
        print("WRITE check partitions=%s columns=%s schema_hash=%s (want %s) claims_ok=%s flow_class_ok=%s same_count=%s rows_in_object=%s" % (check["partitions_after"], ncols, sh, chk.SCHEMA_HASH, claims_ok, flow_ok,
                                                                                                                                      check["same_count_as_dry"], check["rows_in_object"]))
        if parts != [d] or ncols != 19 or sh != chk.SCHEMA_HASH or not claims_ok or not flow_ok or not check["same_count_as_dry"]:
            problems.append("first write check failed: %s" % check)
    else:
        ot = other_tables()
        unchanged = all(ot[t] == b["other_tables"][t] for t in OTHER)
        days_written = len(ret["transaction_rows"] or {})
        check = {"days_written": days_written, "partitions_after": len(parts), "other_tables_unchanged": unchanged}
        print("RANGE check days_written=%d partitions_after=%d other_tables_unchanged=%s" % (days_written, len(parts), unchanged))
        if not (1 <= days_written <= 25 and len(parts) == days_written and unchanged):
            problems.append("range check failed: %s" % check)
    save("%s_check.json" % name, check)
    print("INVOKE %s PROBLEMS: %s" % (name, problems or "none"))
    return 0 if not problems else 3


def cmd_trigger():
    b = load("before.json")
    dry = load("dry_invoke.json")
    a, bb = int(dry["report"]["duration_ms"]), int(b["last_fire"]["duration_ms"])
    out = {"act3_stage_duration_ms": a, "last_pre_apply_fire_duration_ms": bb, "sum_ms": a + bb, "over_720s": (a + bb) > 720000, "rollback_taken": False}
    save("time_trigger.json", out)
    print("TRIGGER %s" % out)
    return 0


def cmd_compile():
    d, w, r = load("dry_invoke.json"), load("write_invoke.json"), load("range_invoke.json")
    dc, wc, rc = load("dry_check.json"), load("write_check.json"), load("range_check.json")

    def ev(x):
        return {k: x[k] for k in ("payload", "invoked_utc", "status_code", "function_error", "returned", "report", "request_id")}
    rec = {"claim": "measured", "gates": load("gates.json"), "ledger_entry": OWN_SLUG, "applier": chk.APPLIER, "first_apply": load("first_apply.json"), "before": load("before.json"), "build": load("build.json"), "plan": load("plan.json"),
           "apply_finished_utc": load("apply_finished.json")["apply_finished_utc"], "after": load("after.json"),
           "dry_run": dict(ev(d), prefix_objects_after=dc["prefix_objects_after"]), "time_trigger": load("time_trigger.json"),
           "first_write": dict(ev(w), partitions_after=wc["partitions_after"], columns=wc["columns"], schema_hash=wc["schema_hash"], claims_ok=wc["claims_ok"], flow_class_ok=wc["flow_class_ok"]),
           "range": dict(ev(r), days_written=rc["days_written"], partitions_after=rc["partitions_after"], other_tables_unchanged=rc["other_tables_unchanged"]),
           "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    (HERE / "TRANSACTION_APPLY_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote TRANSACTION_APPLY_RECORD.json keys=%s" % sorted(rec))
    return 0


if __name__ == "__main__":
    c = sys.argv[1]
    sys.exit({"gates": cmd_gates, "first_apply": cmd_first_apply, "before": cmd_before, "trigger": cmd_trigger, "compile": cmd_compile}.get(c, lambda: {"after_apply": cmd_after_apply, "invoke": cmd_invoke}[c](sys.argv[2]))())
