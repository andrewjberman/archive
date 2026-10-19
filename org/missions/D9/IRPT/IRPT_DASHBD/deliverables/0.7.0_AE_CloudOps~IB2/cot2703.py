"""IRPT_DASHBD TO-DB-f-2703 (applier 0.7.0_AE_CloudOps~IB2): the reads, the build record, the plan record and the events of the Cottonwood transaction pair.

  python cot2703.py gates                       R0: packet bytes, halves, the ledgers, the one-change-at-a-time census, the six pin checks, the release commit, the live state (read only)
  python cot2703.py before [<fire date>]        Act 2: the before state, the first fire's owed and settle days, the rollback targets -> state2703/before.json
  python cot2703.py build_record <b64_1> <b64_2> <smoke_rc> <atc_import_error|None> <landed_version_id>
  python cot2703.py plan_record <plan.json> <gate_output.txt> <replan_no_changes yes|no>
  python cot2703.py after_apply <UTC>           the function, policy and schedule after the apply -> state2703/after.json
  python cot2703.py event scheduled_dry|settle_dry|tx_dry|tx_write|tx_range     ONE synchronous invoke each (never retried here) with its after-read
  python cot2703.py compile                     assemble COTTONWOOD_TRANSACTION_APPLY_RECORD.json from state2703/

Counts, dates, keys, hashes, words only: no account id and no figure is printed or written.
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

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, cwd=str(HERE)).strip())
STATE = HERE / "state2703"
CHK_PATH = ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks/r139/p139_cotapply.py"
spec = importlib.util.spec_from_file_location("p139_cotapply_for_2703", str(CHK_PATH))
chk = importlib.util.module_from_spec(spec)
sys.modules["p139_cotapply_for_2703"] = chk
spec.loader.exec_module(chk)

REGION = "us-east-1"
FUNCTION, ROLE, POLICY, SCHEDULE = chk.FUNCTION, chk.ROLE, chk.POLICY, chk.SCHEDULE
ART_BUCKET, ART_KEY, BUCKET, TX_PREFIX, RET_PREFIX = chk.ARTIFACT_BUCKET, chk.ARTIFACT_KEY, chk.BUCKET, chk.TX_PREFIX, chk.RETURNS_PREFIX
OWN_SLUG = "irpt-dashbd-cottonwood-transaction-wiring-20261017"
SURFACE = re.compile(r"account-return-daily|irpt-cot-account-return|gold/account_return_daily|gold/account_transaction", re.I)
OTHER_SCHEDULES = {"irpt-cot-reporting-gold-daily": "irpt-cot-reporting-gold-daily", "irpt-cot-reporting-publish-daily": "irpt-cot-reporting-publish-daily"}
CL = "org/critical_paths/change_management/"
iam = boto3.client("iam", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)
sch = boto3.client("scheduler", region_name=REGION)
lam_read = boto3.client("lambda", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)
LAM = boto3.client("lambda", region_name=REGION, config=Config(read_timeout=960, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"}))


def now_utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT)).stdout


def in_band():
    t = dt.datetime.now(dt.timezone.utc)
    return t.weekday() < 5 and dt.time(11, 30) <= t.time() <= dt.time(14, 15)


def policy_statements():
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    return doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]


def policy_hashes():
    return {x["Sid"]: chk.statement_hash(x) for x in policy_statements()}


def schedule_of(name):
    sc = sch.get_schedule(Name=name)
    return {"state": sc["State"], "cron": sc["ScheduleExpression"]}


def artifact_latest():
    vs = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=ART_BUCKET, Prefix=ART_KEY):
        vs += [v for v in pg.get("Versions", []) if v["Key"] == ART_KEY]
    return [v for v in vs if v["IsLatest"]][0]["VersionId"], len(vs)


def partitions(prefix):
    out = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix, Delimiter="/"):
        out += [c["Prefix"].rstrip("/").rsplit("date=", 1)[-1] for c in pg.get("CommonPrefixes", [])]
    return sorted(out)


def objects(prefix):
    return sum(len(pg.get("Contents", [])) for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix))


def ledger_head(slug):
    led = sorted((ROOT / CL).glob("*_%s_deploy_completion.md" % slug))
    return led[-1].read_text(encoding="utf-8", errors="replace")[:1500] if led else ""


def cmd_gates():
    sha = hashlib.sha256((ROOT / chk.PACKET_REL).read_bytes()).hexdigest()
    coo, cto = (ROOT / chk.COO_REL).read_text(encoding="utf-8"), (ROOT / chk.CTO_REL).read_text(encoding="utf-8")
    coo_ok = "SIGNED" in coo and (chk.PACKET_SHA in coo or chk.PACKET_SHA[:12] in coo)
    cto_ok = "SIGNED" in cto and (chk.PACKET_SHA in cto or chk.PACKET_SHA[:12] in cto)
    pins = {}
    for cid, script in (("DBF138-6-AC1", "r138/p138_cotbundle.py"), ("DBF138-6-AC2", "r138/p138_cotbundle.py"), ("DBF138-6-AC3", "r138/p138_cotbundle.py"),
                        ("DBF139-6-AC1", "r139/p139_cotwindow.py"), ("DBF139-6-AC2", "r139/p139_cotwindow.py"), ("DBF139-6-AC3", "r139/p139_cotwindow.py")):
        r = subprocess.run([sys.executable, "-I", str(ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/checks" / script), str(ROOT), cid], capture_output=True, text=True, cwd=str(ROOT), timeout=600)
        pins[cid] = (r.returncode == 0 and (cid + " PASS") in r.stdout)
    release = subprocess.run(["git", "merge-base", "--is-ancestor", "36da4e101f", "HEAD"], cwd=str(ROOT)).returncode == 0
    led49 = ledger_head("irpt-dashbd-49f-transaction-wiring-20261016")
    m49 = "**Status:** CLOSED" in led49
    b332 = "**Status:** CLOSED" in ledger_head("irpt-dashbd-cottonwood-reland-pair-20261017")
    wts = [ln[9:] for ln in git("worktree", "list", "--porcelain").splitlines() if ln.startswith("worktree ")]
    stale, live = 0, []
    for wt in wts:
        for n in [x for x in git("-C", wt, "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/.open_deploys/").split("\n") if x.strip()]:
            if SURFACE.search(git("-C", wt, "show", "HEAD:" + n)):
                slug = Path(n).stem
                if slug == OWN_SLUG:
                    continue
                head = ledger_head(slug)
                if "**Status:** CLOSED" in head or "**Status:** ROLLED-BACK" in head:
                    stale += 1
                else:
                    live.append((wt, n))
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    cur, nvers = artifact_latest()
    sc = schedule_of(SCHEDULE)
    sids_ok = sorted(policy_hashes()) == sorted(chk.OLD_SIDS)
    newobj = objects(TX_PREFIX)
    live_ok = (cfg["CodeSha256"] == "+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=" and cfg["MemorySize"] == 1024 and cfg["Timeout"] == 900 and cfg["Runtime"] == "python3.12"
               and cfg["Handler"] == "handler.lambda_handler" and len(cfg.get("Layers", [])) == 1 and not (cfg.get("Environment") or {}).get("Variables")
               and cur == "6tFJSAqDjN0GqFkYj.DgT6.TkSmlwAuh" and sc["state"] == "ENABLED" and sc["cron"] == "cron(15 8 ? * MON-FRI *)" and sids_ok and newobj == 0)
    gates = {"packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok, "pins_ok": bool(all(pins.values())), "monday_49f_read_passed": m49, "sequence_waiver": chk.SEQUENCE_WAIVER,
             "b332_closed_superseded": b332, "release_commit_in_head": "36da4e101f" if release else None, "open_rewrite_ledgers_on_root": len(live),
             "one_change_at_a_time": {"worktrees_read": len(wts), "open_markers_naming_this_surface": len(live)}}
    print("GATES sha_ok=%s coo=%s cto=%s pin_checks=%s release_in_head=%s" % (sha == chk.PACKET_SHA, coo_ok, cto_ok, pins, release))
    print("GATES monday_49f_ledger_closed=%s b332_ledger_closed=%s" % (m49, b332))
    print("GATES worktrees_read=%d stale_closed_slugs=%d live_markers_naming_surface=%d %s" % (len(wts), stale, len(live), live[:3]))
    print("GATES live: code=%s mem=%s timeout=%s runtime=%s handler=%s layers=%d env=%s artifact_current_ok=%s (artifact versions %d) schedule=%s sids_ok=%s new_prefix_objects=%d -> live_ok=%s" % (
        cfg["CodeSha256"] == "+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=", cfg["MemorySize"], cfg["Timeout"], cfg["Runtime"], cfg["Handler"], len(cfg.get("Layers", [])),
        bool((cfg.get("Environment") or {}).get("Variables")), cur == "6tFJSAqDjN0GqFkYj.DgT6.TkSmlwAuh", nvers, sc, sids_ok, newobj, live_ok))
    save("gates.json", gates)
    ok = sha == chk.PACKET_SHA and coo_ok and cto_ok and gates["pins_ok"] and m49 and b332 and release and not live and live_ok and not in_band()
    print("GATES outside_band_now=%s -> %s" % (not in_band(), "GREEN" if ok else "NOT GREEN"))
    return 0 if ok else 3


def fires():
    group = "/aws/lambda/" + FUNCTION
    t0 = int((dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=6)).timestamp() * 1000)
    out = []
    for pg in logs.get_paginator("filter_log_events").paginate(logGroupName=group, startTime=t0, filterPattern="REPORT"):
        for e in pg["events"]:
            m = re.search(r"REPORT RequestId: (\S+)\s+Duration: ([0-9.]+) ms.*?Max Memory Used: (\d+) MB", e["message"], re.S)
            if m:
                out.append((e["timestamp"], float(m.group(2)), int(m.group(3))))
    return sorted(out)


def cmd_before(fire_date="2026-10-20"):
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    cur, _n = artifact_latest()
    fr = fires()
    ret = partitions(RET_PREFIX)
    sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/account-return-daily"))
    import handler as h
    bk, pf = h.cbd.gold_prefix()
    newest = h.newest_landed_day(s3, bk, pf)
    owed = h.owed_days(newest, dt.date.fromisoformat(fire_date))
    settle = h.settle_days(s3, owed)
    targets = {}
    for day in settle:
        t = {}
        for fname in ("data.parquet", "manifest.json"):
            key = "%sdate=%s/%s" % (RET_PREFIX, day, fname)
            vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=key) for v in pg.get("Versions", []) if v["Key"] == key]
            t[fname] = [v["VersionId"] for v in vs if v["IsLatest"]][0]
        targets[day] = t
    last = fr[-1] if fr else None
    out = {"function_code_sha256": cfg["CodeSha256"], "artifact_version_id": cur, "policy": policy_hashes(), "new_prefix_objects": objects(TX_PREFIX), "schedule": schedule_of(SCHEDULE),
           "other_schedules": {k: schedule_of(v)["state"] for k, v in OTHER_SCHEDULES.items()},
           "fires": {"count": len(fr), "last_duration_ms": int(last[1]) if last else None, "last_max_memory_mb": last[2] if last else None},
           "returns_partitions": len(ret), "newest_returns_day": ret[-1] if ret else None,
           "first_fire_date": fire_date, "newest_landed_returns_day": newest, "first_fire_owed_days": owed, "first_fire_settle_days": settle, "rollback_targets": targets}
    save("before.json", out)
    save("before_fires.json", [{"utc": dt.datetime.fromtimestamp(r[0] / 1000, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "duration_ms": r[1], "max_memory_mb": r[2]} for r in fr])
    print("BEFORE code=%s artifact=%s sids=%d new_prefix_objects=%d schedule=%s other_schedules=%s" % (out["function_code_sha256"], cur, len(out["policy"]), out["new_prefix_objects"], out["schedule"], out["other_schedules"]))
    print("BEFORE fires: REPORT lines in 6 days (denominator) %d, last %s ms / %s MB" % (len(fr), out["fires"]["last_duration_ms"], out["fires"]["last_max_memory_mb"]))
    print("BEFORE returns_partitions=%d newest=%s | first fire %s: owed=%s settle=%s rollback_targets_for=%s" % (len(ret), out["newest_returns_day"], fire_date, owed, settle, sorted(targets)))
    ok = (out["function_code_sha256"] == "+iYXakKx7zhK33lv6W0jDAY1QsLYUNqNCuHHIA7owD0=" and cur == "6tFJSAqDjN0GqFkYj.DgT6.TkSmlwAuh" and sorted(out["policy"]) == sorted(chk.OLD_SIDS)
          and out["new_prefix_objects"] == 0 and len(settle) <= 5 and sorted(targets) == sorted(settle))
    return 0 if ok else 3


def cmd_build_record(b1, b2, smoke_rc, atc_err, landed):
    before = load("before.json")
    out = {"zip_sha256_b64": b1, "second_run_equal": b1 == b2, "import_smoke_rc": int(smoke_rc), "atc_import_error": None if atc_err in ("None", "null", "") else atc_err,
           "landed_version_id": landed, "built_equals_landed": False}
    # the landed object must be the current version, different from the before-state's, and its sha256 (base64) equal to the build
    cur, _n = artifact_latest()
    body = s3.get_object(Bucket=ART_BUCKET, Key=ART_KEY, VersionId=landed)["Body"].read()
    got = base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")
    out["built_equals_landed"] = (got == b1 and cur == landed and landed != before["artifact_version_id"])
    save("build.json", out)
    print("BUILD %s | landed object b64 sha256 equals build=%s current==landed=%s differs_from_before=%s" % (out, got == b1, cur == landed, landed != before["artifact_version_id"]))
    return 0 if (b1 == chk.BUILD_B64 and out["second_run_equal"] and out["import_smoke_rc"] == 0 and out["atc_import_error"] is None and out["built_equals_landed"]) else 3


def cmd_plan_record(plan_json, gate_txt, replan_ok):
    p = json.loads(Path(plan_json).read_text(encoding="utf-8"))
    rc = [r for r in p.get("resource_changes", []) if r["change"]["actions"] != ["no-op"]]
    add = sum(1 for r in rc if r["change"]["actions"] == ["create"])
    chg = sum(1 for r in rc if r["change"]["actions"] == ["update"])
    dst = sum(1 for r in rc if "delete" in r["change"]["actions"])
    addrs = sorted(r["address"] for r in rc)
    fn = [r for r in rc if r["type"] == "aws_lambda_function"]
    pol = [r for r in rc if r["type"] == "aws_iam_role_policy"]
    code_only = False
    if len(fn) == 1:
        b, a = fn[0]["change"]["before"], fn[0]["change"]["after"]
        diff = sorted(k for k in set(b) | set(a) if b.get(k) != a.get(k) and k not in ("last_modified", "source_code_hash", "s3_object_version", "version", "qualified_arn", "qualified_invoke_arn", "invoke_arn", "source_code_size"))
        code_only = (diff == [])
        print("PLAN function attribute diff beyond the code attributes: %s" % diff)
    sids = []
    if len(pol) == 1:
        bdoc = json.loads(pol[0]["change"]["before"]["policy"])
        adoc = json.loads(pol[0]["change"]["after"]["policy"])
        bs = {s["Sid"]: chk.statement_hash(s) for s in (bdoc["Statement"] if isinstance(bdoc["Statement"], list) else [bdoc["Statement"]])}
        as_ = {s["Sid"]: s for s in (adoc["Statement"] if isinstance(adoc["Statement"], list) else [adoc["Statement"]])}
        sids = sorted(set(as_) - set(bs))
        unchanged = all(chk.statement_hash(as_[k]) == v for k, v in bs.items() if k in as_)
        new = as_.get(chk.NEW_SID, {})
        res = [new.get("Resource")] if isinstance(new.get("Resource"), str) else list(new.get("Resource") or [])
        act = [new.get("Action")] if isinstance(new.get("Action"), str) else list(new.get("Action") or [])
        print("PLAN policy: added sids %s | the five old statements unchanged=%s | new: effect=%s actions=%s resources_equal=%s condition=%s" % (sids, unchanged, new.get("Effect"), act, res == [chk.NEW_RESOURCE], "Condition" in new))
        if not (unchanged and res == [chk.NEW_RESOURCE] and act == ["s3:PutObject"] and new.get("Effect") == "Allow" and "Condition" not in new):
            sids = ["MISMATCH"] + sids
    gate = Path(gate_txt).read_text(encoding="utf-8", errors="replace")
    refuse = len(re.findall(r"\bREFUSE\b", gate))
    out = {"add": add, "change": chg, "destroy": dst, "change_addresses": addrs, "policy_added_sids": sids, "function_change_attributes_code_only": bool(code_only), "naming_gate_refuse": refuse,
           "replan_no_changes": replan_ok == "yes"}
    save("plan.json", out)
    print("PLAN %s" % out)
    return 0 if (add, chg, dst) == (0, 2, 0) and len(addrs) == 2 and sids == [chk.NEW_SID] and code_only and refuse == 0 else 3


def cmd_after_apply(utc):
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    layers = [x["Arn"] for x in cfg.get("Layers", [])]
    out = {"function": {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "code_sha256": cfg["CodeSha256"], "layer_arn": layers[0] if layers else None}, "policy": policy_hashes(),
           "schedule": schedule_of(SCHEDULE)}
    save("after.json", out)
    save("apply_finished.json", {"apply_finished_utc": utc})
    b, bld = load("before.json"), load("build.json")
    differ = sorted(s for s in chk.OLD_SIDS if out["policy"].get(s) != b["policy"].get(s))
    print("AFTER code=%s equals_build=%s memory=%s timeout=%s layers=%d handler=%s runtime=%s env=%s" % (cfg["CodeSha256"], cfg["CodeSha256"] == bld["zip_sha256_b64"], cfg["MemorySize"], cfg["Timeout"], len(layers), cfg["Handler"], cfg["Runtime"],
                                                                                                     bool((cfg.get("Environment") or {}).get("Variables"))))
    print("AFTER policy sids=%d old statements differing from before=%s new sid present=%s schedule_equal_before=%s" % (len(out["policy"]), differ, chk.NEW_SID in out["policy"], out["schedule"] == b["schedule"]))
    ok = (cfg["CodeSha256"] == bld["zip_sha256_b64"] and cfg["MemorySize"] == 1024 and cfg["Timeout"] == 900 and len(layers) == 1 and not (cfg.get("Environment") or {}).get("Variables")
          and sorted(out["policy"]) == sorted(chk.OLD_SIDS + [chk.NEW_SID]) and not differ and out["schedule"] == b["schedule"])
    return 0 if ok else 3


def invoke(payload):
    t = now_utc()
    resp = LAM.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse", LogType="Tail", Payload=json.dumps(payload).encode("ascii"))
    raw = resp["Payload"].read().decode("utf-8")
    try:
        body = json.loads(raw)
    except ValueError:
        body = {"_unparsed": True}
    log = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
    m = re.search(r"REPORT RequestId: (\S+)\s+Duration: ([0-9.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", log, re.S)
    rep = {"max_memory_mb": int(m.group(4)), "duration_ms": int(float(m.group(2)))} if m else None
    flags = {"timed_out": "Task timed out" in log, "access_denied": "AccessDenied" in log, "function_error": resp.get("FunctionError")}
    return body, rep, flags, (m.group(1) if m else None), log, t, resp["StatusCode"]


def problems_common(rep, flags):
    pr = []
    if flags["timed_out"] or flags["access_denied"] or flags["function_error"] or rep is None:
        pr.append("timeout, AccessDenied, function error or no REPORT line: %s" % flags)
    elif rep["max_memory_mb"] > 819 or rep["duration_ms"] > 720000:
        pr.append("memory %s MB or duration %s ms above the 80 percent line (819 MB / 720000 ms)" % (rep["max_memory_mb"], rep["duration_ms"]))
    return pr


def range_start(w):
    sys.path.insert(0, str(ROOT / "lib"))
    import trading_calendar as tc
    days, cur = [w], dt.date.fromisoformat(w)
    while len(days) < 25:
        cur = tc.prev_trading_day(cur)
        days.append(cur.isoformat())
    return days[-1]


def schema_hash(table):
    lines = sorted("%s:%s" % (f.name, f.type) for f in table.schema)
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest(), len(table.schema)


def read_tx_day(day):
    import pyarrow.parquet as pq
    keys = [o["Key"] for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="%sdate=%s/" % (TX_PREFIX, day)) for o in pg.get("Contents", [])]
    data = [k for k in keys if k.endswith("data.parquet")]
    return sorted(k.rsplit("/", 1)[-1] for k in keys), (pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=data[0])["Body"].read())) if data else None)


def cmd_event(name):
    f = "%s_event.json" % name
    if (STATE / f).exists():
        print("REFUSED: %s was already invoked (state file present)" % name)
        return 2
    if in_band():
        print("STOP: inside the weekday band 11:30Z to 14:15Z")
        return 3
    b = load("before.json")
    ret_before = (objects(RET_PREFIX), objects(TX_PREFIX))
    order = ["scheduled_dry", "settle_dry", "tx_dry", "tx_write", "tx_range"]
    for prev in order[:order.index(name)]:
        if not (STATE / ("%s_check.json" % prev)).exists():
            print("REFUSED: the previous leg's after-read (%s) is not recorded" % prev)
            return 2
    problems, rec = [], {}
    if name == "scheduled_dry":
        payload = {"dry_run": True}
        body, rep, flags, rid, log, t, status = invoke(payload)
        m = re.search(r"OWED: newest landed (\S+), today (\S+), days (\[.*?\])", log)
        owed = json.loads(m.group(3).replace("'", '"')) if m else None
        win = (body.get("transaction_window") or {}) if isinstance(body, dict) else {}
        settled = {d: {"rows": (v or {}).get("rows")} for d, v in ((body.get("settled") or {}).items() if isinstance(body, dict) else [])}
        after = (objects(RET_PREFIX), objects(TX_PREFIX))
        rec = {"payload": payload, "status_code": status, "owed_days": owed, "newest_writable_day": win.get("newest_writable_day"), "settled": settled, "wrote_nothing": after == ret_before,
               "max_memory_mb": rep["max_memory_mb"] if rep else None, "duration_ms": rep["duration_ms"] if rep else None, "request_id": rid, "invoked_utc": t,
               "settle_failed": body.get("settle_failed") if isinstance(body, dict) else None, "transaction_rows": body.get("transaction_rows") if isinstance(body, dict) else None,
               "transaction_failed": body.get("transaction_failed") if isinstance(body, dict) else None, "held": body.get("held") if isinstance(body, dict) else None}
        problems += problems_common(rep, flags)
        if status != 200 or not rec["newest_writable_day"] or not rec["wrote_nothing"] or rec["owed_days"] is None:
            problems.append("status %s newest_writable_day %s wrote_nothing %s owed_days %s" % (status, rec["newest_writable_day"], rec["wrote_nothing"], rec["owed_days"]))
        save("scheduled_dry_check.json", {"object_counts_before": ret_before, "object_counts_after": after})
    elif name == "settle_dry":
        rec = {}
        for day in b["first_fire_settle_days"]:
            payload = {"rewrite": {"start": day, "end": day}, "dry_run": True}
            body, rep, flags, rid, log, t, status = invoke(payload)
            res = ((body.get("results") or {}).get(day) or {}) if isinstance(body, dict) else {}
            tool = subprocess.run([sys.executable, "-I", str(ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/tools/settle_day_figures.py"), day], capture_output=True, text=True, cwd=str(ROOT), timeout=900)
            mm = re.search(r"derived rows (\d+), NOT_MEASURABLE (\d+) \(([0-9.]+) percent\), flow accounts (\d+)", tool.stdout)
            n, nm, flow = (int(mm.group(1)), int(mm.group(2)), int(mm.group(4))) if mm else (None, None, None)
            after = (objects(RET_PREFIX), objects(TX_PREFIX))
            rec[day] = {"payload": payload, "status_code": status, "wrote_nothing": after == ret_before, "rows": res.get("rows"), "rows_tool": n,
                        "not_measurable_share": (float(nm) / n) if n else None, "flow_accounts": flow, "max_memory_mb": rep["max_memory_mb"] if rep else None,
                        "duration_ms": rep["duration_ms"] if rep else None, "request_id": rid, "invoked_utc": t}
            print("SETTLE_DRY %s rows=%s rows_tool=%s nm_share=%s flow_accounts=%s mem=%s dur=%s wrote_nothing=%s" % (day, rec[day]["rows"], n, rec[day]["not_measurable_share"], flow, rec[day]["max_memory_mb"], rec[day]["duration_ms"], rec[day]["wrote_nothing"]))
            problems += problems_common(rep, flags)
            if status != 200 or not rec[day]["wrote_nothing"] or not isinstance(rec[day]["rows"], int) or rec[day]["rows"] != n or n is None or rec[day]["not_measurable_share"] > 0.15:
                problems.append("%s: rows %s vs tool %s, share %s, wrote_nothing %s, status %s" % (day, rec[day]["rows"], n, rec[day]["not_measurable_share"], rec[day]["wrote_nothing"], status))
                break
        save("settle_dry_check.json", {"days": sorted(rec)})
    elif name == "tx_dry":
        w = load("scheduled_dry_event.json")["newest_writable_day"]
        payload = {"transaction": {"start": w, "end": w}, "dry_run": True}
        body, rep, flags, rid, log, t, status = invoke(payload)
        rows, failed = (body.get("transaction_rows"), body.get("transaction_failed")) if isinstance(body, dict) else (None, None)
        objs = objects(TX_PREFIX)
        rec = {"payload": payload, "status_code": status, "transaction_rows": rows, "transaction_failed": failed, "max_memory_mb": rep["max_memory_mb"] if rep else None, "duration_ms": rep["duration_ms"] if rep else None,
               "prefix_objects_after": objs, "request_id": rid, "invoked_utc": t}
        problems += problems_common(rep, flags)
        if status != 200 or failed != {} or not isinstance(rows, dict) or list(rows) != [w] or not all(isinstance(v, int) and v > 0 for v in rows.values()) or objs != 0:
            problems.append("status %s failed %s rows %s objects_after %s" % (status, failed, rows, objs))
        save("tx_dry_check.json", {"prefix_objects_after": objs})
    elif name == "tx_write":
        w = load("scheduled_dry_event.json")["newest_writable_day"]
        dry = load("tx_dry_event.json")
        payload = {"transaction": {"start": w, "end": w}}
        body, rep, flags, rid, log, t, status = invoke(payload)
        rows, failed = (body.get("transaction_rows"), body.get("transaction_failed")) if isinstance(body, dict) else (None, None)
        parts = partitions(TX_PREFIX)
        names, tbl = read_tx_day(w)
        sh, ncols = schema_hash(tbl) if tbl is not None else (None, None)
        claims = tbl["business_date_claim"].to_pylist() if tbl is not None else []
        bd, td = (tbl["business_date"].to_pylist(), tbl["trade_date"].to_pylist()) if tbl is not None else ([], [])
        claims_ok = bool(claims) and all(c in ("measured", "inferred") for c in claims) and all((c == "inferred") == (str(x) != str(y)) for c, x, y in zip(claims, bd, td))
        enum = ("EXTERNAL_IN", "EXTERNAL_OUT", "INCOME", "FEE", "INTERNAL", "CORPORATE_ACTION", "UNRESOLVED")
        flow_ok = tbl is not None and all(v in enum for v in tbl["flow_class"].to_pylist())
        rec = {"payload": payload, "status_code": status, "transaction_rows": rows, "transaction_failed": failed, "partitions_after": parts, "columns": ncols, "schema_hash": sh, "claims_ok": bool(claims_ok),
               "flow_class_ok": bool(flow_ok), "partition_objects": names, "request_id": rid, "invoked_utc": t, "max_memory_mb": rep["max_memory_mb"] if rep else None, "duration_ms": rep["duration_ms"] if rep else None}
        problems += problems_common(rep, flags)
        print("WRITE check partitions=%s columns=%s schema_hash_equals_packet=%s claims_ok=%s flow_class_ok=%s objects=%s same_count_as_dry=%s" % (parts, ncols, sh == chk.SCHEMA_HASH, claims_ok, flow_ok, names, rows == dry["transaction_rows"]))
        if status != 200 or failed != {} or rows != dry["transaction_rows"] or parts != [w] or ncols != 19 or sh != chk.SCHEMA_HASH or not claims_ok or not flow_ok or names != ["data.parquet", "manifest.json"]:
            problems.append("first write check failed")
        save("tx_write_check.json", {"partitions_after": parts})
    else:
        w = load("scheduled_dry_event.json")["newest_writable_day"]
        start = range_start(w)
        payload = {"transaction": {"start": start, "end": w}}
        body, rep, flags, rid, log, t, status = invoke(payload)
        rows, failed = (body.get("transaction_rows"), body.get("transaction_failed")) if isinstance(body, dict) else (None, None)
        days = sorted((rows or {}).keys())
        parts = partitions(TX_PREFIX)
        ret_now = partitions(RET_PREFIX)
        unchanged = (len(ret_now) == b["returns_partitions"] and (ret_now[-1] if ret_now else None) == b["newest_returns_day"])
        rec = {"payload": payload, "status_code": status, "days": days, "days_written": len(days), "partitions_after": len(parts), "transaction_failed": failed, "returns_prefix_unchanged": bool(unchanged),
               "max_memory_mb": rep["max_memory_mb"] if rep else None, "duration_ms": rep["duration_ms"] if rep else None, "request_id": rid, "invoked_utc": t}
        problems += problems_common(rep, flags)
        print("RANGE days_written=%d partitions_after=%d failed=%s returns_unchanged=%s" % (len(days), len(parts), failed, unchanged))
        if status != 200 or not (1 <= len(days) <= 24) or len(parts) != len(days) + 1 or not isinstance(failed, dict) or list(failed) != [w] or "already" not in str(failed.get(w)).lower() or w in days or not unchanged:
            problems.append("range check failed")
        save("tx_range_check.json", {"partitions_after": len(parts)})
    rec["problems"] = problems
    save(f, rec)
    shown = {k: v for k, v in rec.items() if k not in ("settled",)} if name != "settle_dry" else {}
    print("EVENT %s %s" % (name, json.dumps(shown, sort_keys=True)[:900]))
    print("EVENT %s PROBLEMS: %s" % (name, problems or "none"))
    return 0 if not problems else 3


def cmd_compile():
    sd, st, dr, fw, rg = load("scheduled_dry_event_run1.json"), load("settle_dry_event.json"), load("tx_dry_event.json"), load("tx_write_event.json"), load("tx_range_event.json")
    sd2, ap, ap_plan = load("scheduled_dry_event.json"), load("addendum_apply.json"), load("addendum_plan.json")
    keep = ("payload", "status_code", "max_memory_mb", "duration_ms", "request_id")
    addendum1 = {"plan": ap_plan, "iam_tf_commit": ap_plan["iam_tf_commit"], "apply_finished_utc": ap["apply_finished_utc"], "policy_sids": ap["policy_sids"], "six_before_statements_identical": ap["six_identical"],
                 "step6_first_run_transaction_failed": "AccessDenied s3:ListBucket on opal-data-cottonwood (the transaction prefix, no grant yet), 2026-09-29",
                 "step6_rerun": {**{k: sd2[k] for k in keep}, "invoked_utc": sd2["invoked_utc"], "owed_days": sd2["owed_days"], "newest_writable_day": sd2["newest_writable_day"], "settled": sd2["settled"],
                                 "wrote_nothing": sd2["wrote_nothing"], "transaction_failed": sd2["transaction_failed"], "transaction_rows": sd2["transaction_rows"]}}
    rec = {"claim": "measured", "gates": load("gates.json"), "ledger_entry": CL + [p.name for p in sorted((ROOT / CL).glob("*_%s_deploy_completion.md" % OWN_SLUG))][-1], "applier": chk.APPLIER,
           "before": load("before.json"), "build": load("build.json"), "plan": load("plan.json"), "apply_finished_utc": load("apply_finished.json")["apply_finished_utc"], "after": load("after.json"),
           "scheduled_dry_run": {**{k: sd[k] for k in keep}, "owed_days": sd["owed_days"], "newest_writable_day": sd["newest_writable_day"], "settled": sd["settled"], "wrote_nothing": sd["wrote_nothing"]},
           "settle_dry_runs": {d: {k: v for k, v in x.items() if k != "invoked_utc"} for d, x in st.items() if d != "problems"},
           "addendum1": addendum1,
           "dry_run": {**{k: dr[k] for k in keep}, "transaction_rows": dr["transaction_rows"], "transaction_failed": dr["transaction_failed"], "prefix_objects_after": dr["prefix_objects_after"]},
           "first_write": {**{k: fw[k] for k in keep}, "transaction_rows": fw["transaction_rows"], "transaction_failed": fw["transaction_failed"], "partitions_after": fw["partitions_after"], "columns": fw["columns"],
                           "schema_hash": fw["schema_hash"], "claims_ok": fw["claims_ok"], "flow_class_ok": fw["flow_class_ok"]},
           "range": {**{k: rg[k] for k in keep}, "days": rg["days"], "days_written": rg["days_written"], "partitions_after": rg["partitions_after"], "transaction_failed": rg["transaction_failed"],
                     "returns_prefix_unchanged": rg["returns_prefix_unchanged"]},
           "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    (HERE / "COTTONWOOD_TRANSACTION_APPLY_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote COTTONWOOD_TRANSACTION_APPLY_RECORD.json keys=%s" % sorted(rec))
    return 0


if __name__ == "__main__":
    c = sys.argv[1]
    a = sys.argv[2:]
    table = {"gates": lambda: cmd_gates(), "before": lambda: cmd_before(*a), "build_record": lambda: cmd_build_record(*a), "plan_record": lambda: cmd_plan_record(*a),
             "after_apply": lambda: cmd_after_apply(*a), "event": lambda: cmd_event(*a), "compile": lambda: cmd_compile()}
    sys.exit(table[c]())
