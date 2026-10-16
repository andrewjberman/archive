"""IRPT_DASHBD TO-DB-b-312 (applier 0.7.0_AE_CloudOps~IB2): the reads and the two invokes of the 49 Financial reporting-publish apply.

  python pub312.py gates                  packet bytes, halves, ancestry, one-change-at-a-time census, live state vs the packet (read only)
  python pub312.py before                 the BEFORE state -> state312/before.json
  python pub312.py after_apply <UTC>      the function, policy and schedules after the apply -> state312/after.json
  python pub312.py invoke probe|dry       ONE synchronous invoke (never retried here) -> state312/<name>_invoke.json
  python pub312.py platinum_after         the platinum counts again -> state312/platinum_after.json
  python pub312.py compile                assemble PUB49F_HOP2_READER_RECORD.json from state312/

Counts, dates, keys, hashes and words only: no account id is printed or written.
"""
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import boto3
from botocore.config import Config

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, cwd=str(Path(__file__).resolve().parent)).strip())
HERE = Path(__file__).resolve().parent
STATE = HERE / "state312"
CHK_PATH = ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/checks/r149/p179_pub49f_hop2_apply.py"
spec = importlib.util.spec_from_file_location("p179_for_pub312", str(CHK_PATH))
chk = importlib.util.module_from_spec(spec)
sys.modules["p179_for_pub312"] = chk
spec.loader.exec_module(chk)
G = chk.G

REGION = "us-east-1"
FUNCTION, ROLE, POLICY = chk.FUNCTION, chk.ROLE, chk.POLICY
ART_BUCKET, ART_KEY = chk.ARTIFACT_BUCKET, chk.ARTIFACT_KEY
SURFACE = re.compile(r"reporting-publish|reporting_publish|platinum/reporting", re.I)
OWN_SLUG = chk.LEDGER_SLUG
PLAT_PREFIX = "irpt/49financial/platinum/reporting/"
iam = boto3.client("iam", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)
sch = boto3.client("scheduler", region_name=REGION)
lam_read = boto3.client("lambda", region_name=REGION)


def now_utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT)).stdout


def policy_doc():
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    return doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]


def policy_hashes():
    return {x["Sid"]: G.stmt_hash(x) for x in policy_doc()}


def plat_bucket():
    arns = [x for x in policy_doc() if x["Sid"] == "WriteThePlatinumReportingPrefixOnly"][0]["Resource"]
    arn = arns[0] if isinstance(arns, list) else arns
    return arn.split(":::")[1].split("/")[0]


def schedules():
    out = {}
    for name in sorted(chk.SCHEDULES):
        sc = sch.get_schedule(Name=name)
        out[name] = {"state": sc["State"], "cron": sc["ScheduleExpression"]}
    return out


def counts(bucket, prefix):
    objs = sum(len(pg.get("Contents", [])) for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix))
    vers = 0
    markers = 0
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=prefix):
        vers += len(pg.get("Versions", []))
        markers += len(pg.get("DeleteMarkers", []))
    return objs, vers, markers


def artifact_current():
    vs = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=ART_BUCKET, Prefix=ART_KEY):
        vs += [v for v in pg.get("Versions", []) if v["Key"] == ART_KEY]
    return [v for v in vs if v["IsLatest"]][0]["VersionId"], len(vs)


def cmd_gates():
    packet = chk.PACKET_REL
    blob = git("hash-object", packet).strip()
    sha = hashlib.sha256((ROOT / packet).read_bytes()).hexdigest()
    coo = (ROOT / chk.COO_HALF_REL).read_text(encoding="utf-8")
    cto = (ROOT / chk.CTO_HALF_REL).read_text(encoding="utf-8")
    coo_ok = "SIGNED" in coo and chk.PACKET_SHA in coo
    cto_ok = "SIGNED" in cto and chk.PACKET_SHA[:12] in cto
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", "4aca09a82d", "HEAD"], cwd=str(ROOT)).returncode == 0
    wts = [ln[9:] for ln in git("worktree", "list", "--porcelain").splitlines() if ln.startswith("worktree ")]
    stale, live = {}, []
    for wt in wts:
        for n in [x for x in git("-C", wt, "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/.open_deploys/").split("\n") if x.strip()]:
            if SURFACE.search(git("-C", wt, "show", "HEAD:" + n)):
                slug = Path(n).stem
                if slug == OWN_SLUG:
                    continue
                led = list((ROOT / "org/critical_paths/change_management").glob("*_%s_deploy_completion.md" % slug))
                head = led[0].read_text(encoding="utf-8", errors="replace")[:1500] if led else ""
                if "**Status:** CLOSED" in head or "**Status:** ROLLED-BACK" in head:
                    stale[slug] = stale.get(slug, 0) + 1
                else:
                    live.append((wt, n))
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    conc = lam_read.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    cur, nvers = artifact_current()
    scs = schedules()
    live_ok = (cfg["CodeSha256"] == chk.BEFORE_CODE and cfg["MemorySize"] == 1024 and cfg["Timeout"] == 300 and conc is None and not (cfg.get("Environment") or {}).get("Variables")
               and cur == chk.BEFORE_VERSION and all(v["state"] == "ENABLED" for v in scs.values()) and sorted(policy_hashes()) == chk.SIDS)
    gates = {"packet_blob": blob, "packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok, "pin_is_ancestor": anc,
             "one_change_at_a_time": {"worktrees_read": len(wts), "open_markers_naming_this_surface": len(live)}, "live_matches_packet": bool(live_ok)}
    print("GATES blob_ok=%s sha_ok=%s coo=%s cto=%s ancestor=%s" % (blob == chk.PACKET_BLOB, sha == chk.PACKET_SHA, coo_ok, cto_ok, anc))
    print("GATES worktrees_read=%d stale_closed_slugs=%d live_markers_naming_surface=%d %s" % (len(wts), len(stale), len(live), live[:3]))
    print("GATES live: code_ok=%s mem=%s timeout=%s conc=%s env=%s artifact_current_ok=%s (artifact versions %d) schedules=%s policy_sids_ok=%s -> live_matches_packet=%s" % (
        cfg["CodeSha256"] == chk.BEFORE_CODE, cfg["MemorySize"], cfg["Timeout"], conc, bool((cfg.get("Environment") or {}).get("Variables")), cur == chk.BEFORE_VERSION, nvers, scs,
        sorted(policy_hashes()) == chk.SIDS, live_ok))
    save("gates.json", gates)
    return 0 if (blob == chk.PACKET_BLOB and sha == chk.PACKET_SHA and coo_ok and cto_ok and anc and not live and live_ok) else 3


def cmd_before():
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    cur, _n = artifact_current()
    bucket = plat_bucket()
    po, pv, pm = counts(bucket, PLAT_PREFIX)
    fo, fv, fm = counts(bucket, chk.FILLED_PREFIX)
    out = {"function_code_sha256": cfg["CodeSha256"], "artifact_version_id": cur, "policy": policy_hashes(), "schedules": schedules(), "platinum": {"objects": po, "versions": pv}, "filled_prefix_objects": fo}
    save("before.json", out)
    print("BEFORE code=%s artifact_current=%s policy_sids=%d schedules=%s" % (out["function_code_sha256"], cur, len(out["policy"]), out["schedules"]))
    print("BEFORE platinum objects=%d versions=%d delete_markers=%d | filled prefix objects=%d versions=%d delete_markers=%d (denominator: client-side counts, auto-paginated)" % (po, pv, pm, fo, fv, fm))
    ok = out["function_code_sha256"] == chk.BEFORE_CODE and cur == chk.BEFORE_VERSION and sorted(out["policy"]) == chk.SIDS and fo >= 1 and po > 0
    return 0 if ok else 3


def cmd_after_apply(utc):
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    conc = lam_read.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    layers = [x["Arn"] for x in cfg.get("Layers", [])]
    out = {"function": {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "reserved_concurrency": conc, "code_sha256": cfg["CodeSha256"], "layer_arn": layers[0] if layers else None},
           "policy": policy_hashes(), "schedules": schedules()}
    save("after.json", out)
    save("apply_finished.json", {"apply_finished_utc": utc})
    b = load("before.json")
    differ = sorted(s for s in out["policy"] if out["policy"][s] != b["policy"].get(s))
    print("AFTER code=%s memory=%s timeout=%s conc=%s layers=%d handler=%s runtime=%s env=%s" % (cfg["CodeSha256"], cfg["MemorySize"], cfg["Timeout"], conc, len(layers), cfg["Handler"], cfg["Runtime"], bool((cfg.get("Environment") or {}).get("Variables"))))
    print("AFTER policy statements differing from before: %s ; schedules_equal_before=%s" % (differ, out["schedules"] == b["schedules"]))
    return 0


def cmd_invoke(name):
    if (STATE / ("%s_invoke.json" % name)).exists():
        print("REFUSED: %s was already invoked (state file present)" % name)
        return 2
    payload = {"filled_report": True} if name == "probe" else {"dry_run": True, "shard": 0, "shards": 7}
    if name == "dry" and not (STATE / "probe_invoke.json").exists():
        print("REFUSED: the probe comes first")
        return 2
    t = now_utc()
    if G.in_window(t, "12:05", "13:15"):
        print("STOP: inside the fire windows")
        return 3
    cfg = Config(read_timeout=960, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"})
    lam = boto3.client("lambda", region_name=REGION, config=cfg)
    save("%s_invoking.json" % name, {"payload": payload, "invoked_utc": t})
    print("INVOKE %s sending at %s payload=%s" % (name, t, json.dumps(payload)), flush=True)
    resp = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse", LogType="Tail", Payload=json.dumps(payload).encode("ascii"))
    body = json.loads(resp["Payload"].read().decode("utf-8"))
    log = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
    m = re.search(r"REPORT RequestId: (\S+)\s+Duration: ([0-9.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", log, re.S)
    if name == "dry" and isinstance(body, dict):
        ret = {"ok": body.get("ok"), "accounts": body.get("accounts", len(body.get("results", {})) if isinstance(body.get("results"), (dict, list)) else None), "refused_count": body.get("refused_count", len(body.get("refused", [])) if isinstance(body.get("refused"), list) else None)}
        raw_keys = sorted(body)
    else:
        ret = body
        raw_keys = sorted(body) if isinstance(body, dict) else None
    rec = {"payload": payload, "invoked_utc": t, "status_code": resp["StatusCode"], "function_error": resp.get("FunctionError"), "returned": ret,
           "report": ({"max_memory_used_mb": int(m.group(4)), "duration_ms": float(m.group(2)), "memory_size_mb": int(m.group(3))} if m else None), "request_id": m.group(1) if m else None, "raw_keys": raw_keys}
    save("%s_invoke.json" % name, rec)
    print("INVOKE %s status=%s function_error=%s returned=%s raw_keys=%s report=%s request_id=%s" % (name, rec["status_code"], rec["function_error"], ret, raw_keys, rec["report"], rec["request_id"]))
    if rec["function_error"] or not m or "Task timed out" in log:
        print("STOP: a function error or no REPORT line: %s" % log[:300].replace("\n", " "))
        return 3
    if name == "probe" and ret != chk.PROBE_EXPECT:
        print("STOP: the probe answer is not the exact switch-OFF no-op %s" % chk.PROBE_EXPECT)
        return 3
    if name == "dry" and not (ret.get("ok") is True and ret.get("refused_count") == 0 and isinstance(ret.get("accounts"), int) and ret["accounts"] > 0):
        print("STOP: the dry run is not ok / 0 refused / a positive count")
        return 3
    if m and (int(m.group(4)) > chk.MEM_LINE or float(m.group(2)) > chk.DUR_LINE):
        print("STOP: memory or duration over the line")
        return 3
    return 0


def cmd_platinum_after():
    po, pv, pm = counts(plat_bucket(), PLAT_PREFIX)
    b = load("before.json")
    save("platinum_after.json", {"objects": po, "versions": pv})
    print("PLATINUM_AFTER objects=%d versions=%d delete_markers=%d equal_before=%s" % (po, pv, pm, {"objects": po, "versions": pv} == b["platinum"]))
    return 0 if {"objects": po, "versions": pv} == b["platinum"] else 3


def cmd_compile():
    rec = {"claim": "measured", "gates": load("gates.json"), "ledger_entry": OWN_SLUG, "applier": chk.APPLIER, "before": load("before.json"), "build": load("build.json"), "plan": load("plan.json"),
           "apply_finished_utc": load("apply_finished.json")["apply_finished_utc"], "after": load("after.json"),
           "probe": {k: load("probe_invoke.json")[k] for k in ("payload", "invoked_utc", "status_code", "function_error", "returned", "report", "request_id")},
           "dry_run": {k: load("dry_invoke.json")[k] for k in ("payload", "invoked_utc", "status_code", "function_error", "returned", "report", "request_id")},
           "platinum_after": load("platinum_after.json"), "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    (HERE / "PUB49F_HOP2_READER_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote PUB49F_HOP2_READER_RECORD.json keys=%s" % sorted(rec))
    return 0


if __name__ == "__main__":
    c = sys.argv[1]
    sys.exit({"gates": cmd_gates, "before": cmd_before, "platinum_after": cmd_platinum_after, "compile": cmd_compile}.get(c, lambda: {"after_apply": cmd_after_apply, "invoke": cmd_invoke}[c](sys.argv[2]))())
