"""IRPT_DASHBD TO-DB-b-308 (applier 0.7.0_AE_CloudOps~IB2): the reads, the invokes and the after-reads of the Cottonwood landing apply.

  python cot308.py gates                   packet bytes, halves, ancestry, pins, worktree census, live state vs the packet (read only)
  python cot308.py before                  the BEFORE state (code, artifact versions, policy hashes, schedule, gold survey) -> state/before.json
  python cot308.py after_apply <UTC>       the function, policy and schedule after the apply -> state/after.json
  python cot308.py invoke dry|1|2|3|4      pre-snapshot, ONE synchronous invoke, state/<name>_invoke.json (never retried here)
  python cot308.py read dry|1|2|3|4        the after-read of that act against the landed originals (raises on any STOP clause)
  python cot308.py act5                    the whole-prefix after-read -> state/act5.json
  python cot308.py compile                 assemble COT_LANDING_REWRITE_R2_RECORD.json from state/

Counts, dates, keys, hashes, addresses and words only: no account id is printed or written.
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
STATE = HERE / "state"
CHK_PATH = ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/checks/r149/p176_cot_landing_r2_apply.py"
spec = importlib.util.spec_from_file_location("p176_for_cot308", str(CHK_PATH))
chk = importlib.util.module_from_spec(spec)
sys.modules["p176_for_cot308"] = chk
spec.loader.exec_module(chk)
G, H = chk.G, chk.H

REGION = "us-east-1"
FUNCTION, ROLE, POLICY, SCHEDULE = chk.FUNCTION, chk.ROLE, chk.POLICY, chk.SCHEDULE
BUCKET, FLOOR, NEWEST, HELD = chk.BUCKET, chk.FLOOR, chk.NEWEST, chk.HELD
ART_BUCKET, ART_KEY = chk.ARTIFACT_BUCKET, chk.ARTIFACT_KEY
EVENTS, ALLOWANCE, ALLOWED_COLS = chk.EVENTS, chk.ALLOWANCE, chk.ALLOWED_COLS
MEM_LINE, DUR_LINE = chk.MEM_LINE, chk.DUR_LINE
PREFIX = "irpt/cottonwood/gold/account_return_daily/"
KEYRE = re.compile(r"^.*/date=([0-9-]{10})/(data\.parquet|manifest\.json)$")
SURFACE = re.compile(r"account-return-daily|account_return_daily", re.I)
OWN_SLUG = chk.LEDGER_SLUG
s3 = boto3.client("s3", region_name=REGION)
iam = boto3.client("iam", region_name=REGION)
sch = boto3.client("scheduler", region_name=REGION)
lam_read = boto3.client("lambda", region_name=REGION)


def now_utc():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def git(*a, cwd=None):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd or str(ROOT)).stdout


def partition_days():
    out = set()
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
        out |= {c["Prefix"][len(PREFIX):].strip("/")[5:] for c in pg.get("CommonPrefixes", [])}
    return sorted(out)


def survey():
    """{(day, key): [versions]} over the whole gold prefix, plus the delete-marker count. A key outside the two files of a day raises."""
    vers, markers = {}, 0
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=PREFIX):
        markers += len(pg.get("DeleteMarkers", []))
        for v in pg.get("Versions", []):
            m = KEYRE.match(v["Key"])
            if not m:
                raise SystemExit("STOP: an object under the gold prefix outside the two keys of a day")
            vers.setdefault((m.group(1), v["Key"]), []).append(v)
    return vers, markers


def history_digest(vers):
    hk = sorted(k for k in vers if k[0] < FLOOR)
    one = all(len(vers[k]) == 1 for k in hk)
    digest = hashlib.sha256("\n".join("%s|%s" % (k[1], vers[k][0]["VersionId"]) for k in hk).encode("utf-8")).hexdigest()
    return hk, one, digest


def policy_hashes():
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    sts = doc["Statement"] if isinstance(doc["Statement"], list) else [doc["Statement"]]
    return {x["Sid"]: G.stmt_hash(x) for x in sts}


def schedule_state():
    sc = sch.get_schedule(Name=SCHEDULE)
    return {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")}


def function_state():
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    conc = lam_read.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    return cfg, conc


def artifact_versions():
    out = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=ART_BUCKET, Prefix=ART_KEY):
        out += [v for v in pg.get("Versions", []) if v["Key"] == ART_KEY]
    return sorted(out, key=lambda v: v["LastModified"])


def b64_sha(body):
    return base64.b64encode(hashlib.sha256(body).digest()).decode("ascii")


# ----------------------------------------------------------------------------------------------------------------------------- gates
def cmd_gates():
    packet = chk.PACKET_REL
    blob = git("hash-object", packet).strip()
    sha = hashlib.sha256((ROOT / packet).read_bytes()).hexdigest()
    coo = (ROOT / chk.COO_HALF_REL).read_text(encoding="utf-8")
    cto = (ROOT / chk.CTO_HALF_REL).read_text(encoding="utf-8")
    coo_ok = "SIGNED" in coo and chk.PACKET_SHA in coo
    cto_ok = "SIGNED" in cto and chk.PACKET_SHA[:12] in cto
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", "d58c1dda9c", "HEAD"], cwd=str(ROOT)).returncode == 0
    wts = [ln[9:] for ln in git("worktree", "list", "--porcelain").splitlines() if ln.startswith("worktree ")]
    stale, live = {}, []
    for wt in wts:
        for n in [x for x in git("-C", wt, "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/.open_deploys/").split("\n") if x.strip()]:
            if SURFACE.search(git("-C", wt, "show", "HEAD:" + n)):
                slug = Path(n).stem
                if slug == OWN_SLUG:
                    continue
                led = list((ROOT / "org/critical_paths/change_management").glob("*_%s_deploy_completion.md" % slug))
                closed = bool(led) and "**Status:** CLOSED" in led[0].read_text(encoding="utf-8", errors="replace")[:1500]
                if closed:
                    stale[slug] = stale.get(slug, 0) + 1
                else:
                    live.append((wt, n))
    pins = {"handler.py": ("infra/aws/lambda/investor-reporting/account-return-daily/handler.py", "b22affd4933c"),
            "adapter": ("data/assets/scripts/gold/irpt_reporting/adapters/cottonwood_bd_account_return_daily.py", "4ef97f84d39a"),
            "iam.tf": ("infra/aws/terraform/investor-reporting/account-return-daily/iam.tf", "be6fe3f38597"),
            "lambda.tf": ("infra/aws/terraform/investor-reporting/account-return-daily/lambda.tf", "736826f6e6d8"),
            "locals.tf": ("infra/aws/terraform/investor-reporting/account-return-daily/locals.tf", "8414bb4980d4"),
            "main.tf": ("infra/aws/terraform/investor-reporting/account-return-daily/main.tf", "72245428da82"),
            "schedule.tf": ("infra/aws/terraform/investor-reporting/account-return-daily/schedule.tf", "8bcf2a5295a5")}
    pin_ok = {n: hashlib.sha256((ROOT / p).read_bytes()).hexdigest()[:12] == h for n, (p, h) in pins.items()}
    cfg, conc = function_state()
    vs = artifact_versions()
    cur = [v for v in vs if v["IsLatest"]][0]["VersionId"]
    sc = schedule_state()
    vers, markers = survey()
    days = [d for d in partition_days() if d <= NEWEST]
    live_ok = (cfg["CodeSha256"] == chk.BEFORE_CODE and cfg["MemorySize"] == 1024 and cfg["Timeout"] == 900 and conc == 1 and not (cfg.get("Environment") or {}).get("Variables")
               and cur == chk.BEFORE_VERSION and sc == {"state": "ENABLED", "cron": chk.CRON, "zone": chk.ZONE} and len(days) == 3391 and markers == 0)
    gates = {"packet_blob": blob, "packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok, "pin_is_ancestor": anc,
             "one_change_at_a_time": {"worktrees_read": len(wts), "open_markers_naming_this_surface": len(live)}, "live_matches_packet": bool(live_ok)}
    print("GATES blob_ok=%s sha_ok=%s coo=%s cto=%s ancestor=%s" % (blob == chk.PACKET_BLOB, sha == chk.PACKET_SHA, coo_ok, cto_ok, anc))
    print("GATES worktrees_read=%d stale_closed_slugs=%d (markers in old pins, ledgers CLOSED) live_markers_naming_surface=%d" % (len(wts), len(stale), len(live)))
    print("GATES pins %s" % pin_ok)
    print("GATES live: code_ok=%s mem=%s timeout=%s conc=%s env=%s artifact_current_ok=%s schedule=%s partitions=%d delete_markers=%d -> live_matches_packet=%s" % (
        cfg["CodeSha256"] == chk.BEFORE_CODE, cfg["MemorySize"], cfg["Timeout"], conc, bool((cfg.get("Environment") or {}).get("Variables")), cur == chk.BEFORE_VERSION, sc, len(days), markers, live_ok))
    save("gates.json", gates)
    return 0 if (blob == chk.PACKET_BLOB and sha == chk.PACKET_SHA and coo_ok and cto_ok and anc and not live and all(pin_ok.values()) and live_ok) else 3


# ----------------------------------------------------------------------------------------------------------------------------- before
def cmd_before():
    cfg, conc = function_state()
    vs = artifact_versions()
    running = None
    for v in vs:
        body = s3.get_object(Bucket=ART_BUCKET, Key=ART_KEY, VersionId=v["VersionId"])["Body"].read()
        if b64_sha(body) == cfg["CodeSha256"]:
            running = v["VersionId"]
    cur = [v for v in vs if v["IsLatest"]][0]["VersionId"]
    vers, markers = survey()
    days_all = partition_days()
    days = [d for d in days_all if d <= NEWEST]
    hk, one, digest = history_digest(vers)
    hist = [d for d in days if d < FLOOR]
    landed = [d for d in days if d >= FLOOR]
    out = {"function_code_sha256": cfg["CodeSha256"], "artifact_version_id": cur, "running_version_id": running, "policy": policy_hashes(),
           "schedule": {k: v for k, v in schedule_state().items() if k != "zone"}, "partitions_total": len(days), "history_days": len(hist), "history_keys": len(hk),
           "history_keys_sha256": digest, "landed_days": len(landed), "newest_day": days[-1]}
    save("before.json", out)
    save("before_extra.json", {"artifact_versions_n": len(vs), "history_one_version_all": one, "delete_markers": markers, "partitions_incl_newer": len(days_all),
                               "landed_keys_one_version_all": all(len(vers[k]) == 1 for k in vers if k[0] >= FLOOR), "reserved_concurrency": conc})
    print("BEFORE code=%s artifact_current=%s running=%s" % (out["function_code_sha256"], cur, running))
    print("BEFORE policy sids=%d schedule=%s partitions_total=%d history_days=%d history_keys=%d one_version_all=%s landed_days=%d newest=%s delete_markers=%d" % (
        len(out["policy"]), out["schedule"], out["partitions_total"], out["history_days"], out["history_keys"], one, out["landed_days"], out["newest_day"], markers))
    print("BEFORE history_keys_sha256=%s" % digest)
    ok = (out["function_code_sha256"] == chk.BEFORE_CODE and cur == chk.BEFORE_VERSION and running == chk.RUNNING_VERSION and out["history_days"] == 3325 and out["landed_days"] == 66
          and out["partitions_total"] == 3391 and out["newest_day"] == NEWEST and one and sorted(out["policy"]) == chk.SIDS)
    return 0 if ok else 3


def cmd_after_apply(utc):
    cfg, conc = function_state()
    layers = [x["Arn"] for x in cfg.get("Layers", [])]
    out = {"function": {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "reserved_concurrency": conc, "code_sha256": cfg["CodeSha256"], "layer_arn": layers[0] if layers else None},
           "policy": policy_hashes(), "schedule": schedule_state()}
    save("after.json", out)
    save("apply_finished.json", {"apply_finished_utc": utc})
    print("AFTER code=%s memory=%s timeout=%s conc=%s layers=%d handler=%s runtime=%s env=%s" % (cfg["CodeSha256"], cfg["MemorySize"], cfg["Timeout"], conc, len(layers), cfg["Handler"], cfg["Runtime"], bool((cfg.get("Environment") or {}).get("Variables"))))
    print("AFTER policy_equal_before=%s schedule=%s" % (out["policy"] == load("before.json")["policy"], out["schedule"]))
    return 0


# ----------------------------------------------------------------------------------------------------------------------------- landed day reads
def latest_pair(vers, day):
    kd = [k for k in vers if k[0] == day and k[1].endswith("data.parquet")][0]
    km = [k for k in vers if k[0] == day and k[1].endswith("manifest.json")][0]
    return kd, km


def get_ver(key, v):
    return s3.get_object(Bucket=BUCKET, Key=key[1], VersionId=v["VersionId"])["Body"].read()


SMALL_DRY = {"dryA": ("2026-07-10", "2026-07-14", 3), "dryB": ("2026-10-08", "2026-10-14", 5)}


def range_of(name):
    if name in SMALL_DRY:
        return SMALL_DRY[name]
    if name == "dry":
        return EVENTS[0][0], EVENTS[0][1], EVENTS[0][2]
    return EVENTS[int(name) - 1]


def landed_in(vers, s, e):
    return sorted({k[0] for k in vers if s <= k[0] <= e and k[0] >= FLOOR})


def cmd_invoke(name):
    import pyarrow.parquet as pq
    s, e, n = range_of(name)
    if (STATE / ("%s_invoke.json" % name)).exists():
        print("REFUSED: %s was already invoked (state file present)" % name)
        return 2
    if not name.startswith("dry") and not (STATE / ("%s_read.json" % ("dry" if name == "1" else str(int(name) - 1)))).exists():
        print("REFUSED: the previous act's after-read is not recorded")
        return 2
    vers, _m = survey()
    ds = landed_in(vers, s, e)
    if len(ds) != n or set(ds) & set(HELD):
        print("STOP: the range names %d landed days, expected %d (or names a held day)" % (len(ds), n))
        return 3
    t = now_utc()
    if G.in_window(t, "12:05", "12:45"):
        print("STOP: inside the daily fire window")
        return 3
    pre = {}
    for d in ds:
        kd, km = latest_pair(vers, d)
        vd = sorted(vers[kd], key=lambda v: v["LastModified"])[-1]
        vm = sorted(vers[km], key=lambda v: v["LastModified"])[-1]
        body = get_ver(kd, vd)
        pre[d] = {"rows": pq.read_metadata(io.BytesIO(body)).num_rows, "data_sha256": hashlib.sha256(body).hexdigest(), "manifest_sha256": hashlib.sha256(get_ver(km, vm)).hexdigest(),
                  "versions": [len(vers[kd]), len(vers[km])], "version_ids": [vd["VersionId"], vm["VersionId"]]}
    save("%s_pre.json" % name, pre)
    print("INVOKE %s pre-snapshot: %d days, rows=%d, versions per key=%s" % (name, len(ds), sum(p["rows"] for p in pre.values()), sorted({tuple(p["versions"]) for p in pre.values()})))
    payload = {"rewrite": {"start": s, "end": e}}
    if name.startswith("dry"):
        payload["dry_run"] = True
    cfg = Config(read_timeout=960, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"})
    lam = boto3.client("lambda", region_name=REGION, config=cfg)
    save("%s_invoking.json" % name, {"payload": payload, "invoked_utc": t})
    print("INVOKE %s sending at %s payload=%s" % (name, t, json.dumps(payload)), flush=True)
    resp = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse", LogType="Tail", Payload=json.dumps(payload).encode("ascii"))
    body = json.loads(resp["Payload"].read().decode("utf-8"))
    log = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
    m = re.search(r"REPORT RequestId: (\S+)\s+Duration: ([0-9.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", log, re.S)
    results = body.get("results") or {}
    rec = {"payload": payload, "invoked_utc": t, "status_code": resp["StatusCode"], "function_error": resp.get("FunctionError"),
           "returned": {"ok": body.get("ok"), "rewrite": body.get("rewrite"), "days": len(body.get("days") or []), "held": body.get("held")},
           "report": ({"max_memory_used_mb": int(m.group(4)), "duration_ms": float(m.group(2)), "memory_size_mb": int(m.group(3))} if m else None),
           "request_id": m.group(1) if m else None, "rows_by_day": {d: (results.get(d) or {}).get("rows") for d in (body.get("days") or [])},
           "held_by_day": [d for d, r in results.items() if r.get("held")], "error_class": (body.get("errorType") if isinstance(body, dict) else None)}
    save("%s_invoke.json" % name, rec)
    print("INVOKE %s status=%s function_error=%s returned=%s report=%s request_id=%s held_days=%s" % (name, rec["status_code"], rec["function_error"], rec["returned"], rec["report"], rec["request_id"], rec["held_by_day"]))
    if rec["function_error"] or not m or "Task timed out" in log:
        print("STOP: a function error or no REPORT line (tail follows, first 300 chars): %s" % log[:300].replace("\n", " "))
        return 3
    return 0


# ----------------------------------------------------------------------------------------------------------------------------- the after-read
def floor_sets():
    sys.path.insert(0, str(ROOT / "lib"))
    sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting/adapters"))
    import cottonwood_bd_account_return_daily as cbd
    reader = cbd.CottonwoodBlackDiamondSilverReader()
    ft = reader.read_parquet("fact_allocations", FLOOR).to_pydict()
    fv, _c, _n = cbd.day_values(list(zip(ft[cbd.ACCOUNT_COLUMN], ft[cbd.VALUE_COLUMN])), None)
    pos = {a for a, v in fv.items() if v > 0}
    posset = {str(k) for k in (cbd._key(a) for a in ft[cbd.ACCOUNT_COLUMN]) if k}
    return posset, pos


def cmd_read(name):
    import pyarrow.parquet as pq
    s, e, n = range_of(name)
    inv = load("%s_invoke.json" % name)
    pre = load("%s_pre.json" % name)
    problems = []
    rp = inv["report"]
    if not rp or rp["max_memory_used_mb"] > MEM_LINE or rp["duration_ms"] > DUR_LINE or rp["memory_size_mb"] != 1024:
        problems.append("memory or duration outside the line: %s" % rp)
    if inv["status_code"] != 200 or inv["function_error"] or inv["returned"]["ok"] is not True or inv["returned"]["held"] != 0 or inv["returned"]["days"] != n:
        problems.append("returned %s status %s error %s" % (inv["returned"], inv["status_code"], inv["function_error"]))
    vers, _m = survey()
    ds = landed_in(vers, s, e)
    if sorted(pre) != ds or len(ds) != n:
        problems.append("the named days differ from the pre-snapshot")
    posset, pos = floor_sets()
    if name.startswith("dry"):
        same = all(len(vers[latest_pair(vers, d)[0]]) == 1 and len(vers[latest_pair(vers, d)[1]]) == 1 for d in ds)
        rows_match = all(inv["rows_by_day"].get(d) == pre[d]["rows"] for d in ds)
        unchanged = all([len(vers[latest_pair(vers, d)[0]]), len(vers[latest_pair(vers, d)[1]])] == pre[d]["versions"] and
                        [sorted(vers[k], key=lambda v: v["LastModified"])[-1]["VersionId"] for k in latest_pair(vers, d)] == pre[d]["version_ids"] for d in ds)
        print("READ dry: days=%d rows_match_landed=%s versions_unchanged=%s one_version_each=%s memory=%s" % (len(ds), rows_match, unchanged, same, rp))
        if not (rows_match and unchanged and same):
            problems.append("dry run rows or versions differ")
        hk, one, dg = history_digest(vers)
        landed_one = all(len(vers[k]) == 1 for k in vers if FLOOR <= k[0] <= NEWEST)
        prefix_ok = dg == load("before.json")["history_keys_sha256"] and one and landed_one and not any(k[0] > NEWEST for k in vers)
        print("READ %s whole prefix: history_keys=%d digest_equal_before=%s landed_keys_one_version=%s -> unchanged=%s" % (name, len(hk), dg == load("before.json")["history_keys_sha256"], landed_one, prefix_ok))
        save("%s_read.json" % name, {"rows_match_landed": bool(rows_match), "versions_unchanged": bool(unchanged and same and prefix_ok)})
        print("READ dry PROBLEMS: %s" % (problems or "none"))
        return 0 if not problems else 3
    rows = part = full = f2p = p2f = 0
    changed_by_day = {}
    for d in ds:
        kd, km = latest_pair(vers, d)
        if len(vers[kd]) != 2 or len(vers[km]) != 2:
            problems.append("%s: versions per key %d and %d, not 2 and 2" % (d, len(vers[kd]), len(vers[km])))
            continue
        newest = {k: sorted(vers[k], key=lambda v: v["LastModified"])[-1] for k in (kd, km)}
        oldest = {k: sorted(vers[k], key=lambda v: v["LastModified"])[0] for k in (kd, km)}
        if not all(newest[k]["IsLatest"] for k in newest):
            problems.append("%s: the newest version is not the latest" % d)
        if oldest[kd]["VersionId"] != pre[d]["version_ids"][0] or hashlib.sha256(get_ver(kd, oldest[kd])).hexdigest() != pre[d]["data_sha256"]:
            problems.append("%s: the oldest version is not the pre-event landed one" % d)
        new_t = pq.read_table(io.BytesIO(get_ver(kd, newest[kd])))
        old_t = pq.read_table(io.BytesIO(get_ver(kd, oldest[kd])))
        if not (new_t.num_rows == old_t.num_rows == pre[d]["rows"] == inv["rows_by_day"].get(d) and "history_scope_claim" in new_t.column_names and "history_scope_claim" not in old_t.column_names):
            problems.append("%s: row counts or the claim column" % d)
        if new_t["account_id"].to_pylist() != old_t["account_id"].to_pylist() or new_t["market_value_eod"].to_pylist() != old_t["market_value_eod"].to_pylist():
            problems.append("%s: account_id or market_value_eod differs" % d)
        changed = {}
        for c in [c for c in old_t.column_names if c != "history_scope"]:
            nc = sum(1 for x, y in zip(new_t[c].to_pylist(), old_t[c].to_pylist()) if x != y)
            if nc:
                changed[c] = nc
        if d in ALLOWANCE:
            if not (set(changed) <= set(ALLOWED_COLS) and all(changed[c] <= ALLOWANCE[d][c] for c in changed)):
                problems.append("%s: columns changed %s against the allowance %s" % (d, changed, ALLOWANCE[d]))
        elif changed:
            problems.append("%s: outside the allowance days but changed %s" % (d, changed))
        if changed:
            changed_by_day[d] = changed
        if not all(x == "inferred" for x in new_t["history_scope_claim"].to_pylist()):
            problems.append("%s: claim not inferred on every row" % d)
        if set(old_t["history_scope"].to_pylist()) != {"PARTIAL_HISTORY"}:
            problems.append("%s: the oldest version is not PARTIAL_HISTORY on every row" % d)
        ids = new_t["account_id"].to_pylist()
        for a, sc_new, sc_old in zip(ids, new_t["history_scope"].to_pylist(), old_t["history_scope"].to_pylist()):
            want = "PARTIAL_HISTORY" if str(a) in posset else "FULL"
            if sc_new != want:
                problems.append("%s: an account's history_scope differs from the first-row rule" % d)
                break
            if sc_old == "FULL" and sc_new == "PARTIAL_HISTORY":
                f2p += 1
            if sc_old == "PARTIAL_HISTORY" and sc_new == "FULL":
                p2f += 1
        nm, om = json.loads(get_ver(km, newest[km])), json.loads(get_ver(km, oldest[km]))
        if not (nm["columns"] == om["columns"] + ["history_scope_claim"] and {k: v for k, v in nm.items() if k != "columns"} == {k: v for k, v in om.items() if k != "columns"}):
            problems.append("%s: the manifest differs beyond columns" % d)
        rows += new_t.num_rows
        part += new_t["history_scope"].to_pylist().count("PARTIAL_HISTORY")
        full += new_t["history_scope"].to_pylist().count("FULL")
    if f2p:
        problems.append("FULL to PARTIAL flips: %d" % f2p)
    rec = {"rows": rows, "before_partial": sum(pre[d]["rows"] for d in ds), "partial": part, "full": full, "full_to_partial": f2p, "partial_to_full": p2f,
           "floor_day_accounts": len(posset), "floor_day_positive": len(pos), "changed_by_day": changed_by_day}
    save("%s_read.json" % name, rec)
    print("READ %s: days=%d rows=%d before_partial=%d PARTIAL=%d FULL=%d full_to_partial=%d partial_to_full=%d floor_day_accounts=%d floor_day_positive=%d" % (
        name, len(ds), rows, rec["before_partial"], part, full, f2p, p2f, len(posset), len(pos)))
    print("READ %s changed_by_day=%s" % (name, {d: c for d, c in changed_by_day.items()}))
    print("READ %s PROBLEMS: %s" % (name, problems or "none"))
    return 0 if not problems else 3


def cmd_act5():
    vers, markers = survey()
    days_all = partition_days()
    days = [d for d in days_all if d <= NEWEST]
    hk, one, digest = history_digest(vers)
    hist = [d for d in days if d < FLOOR]
    landed = [d for d in days if d >= FLOOR]
    b = load("before.json")
    two = all(len(vers[k]) == 2 for k in vers if FLOOR <= k[0] <= NEWEST)
    newer = sorted({k[0] for k in vers if k[0] > NEWEST})
    other_new = sum(1 for k in vers if FLOOR <= k[0] <= NEWEST and not KEYRE.match(k[1]))
    out = {"partitions_total": len(days), "history_days": len(hist), "history_keys": len(hk), "history_keys_sha256": digest, "history_one_version_all": bool(one), "landed_days": len(landed),
           "landed_keys_two_versions_all": bool(two), "held_days_absent": not (set(HELD) & set(days_all)), "other_new_keys": other_new, "schedule_state": schedule_state()["state"]}
    save("act5.json", out)
    print("ACT5 %s" % json.dumps(out, sort_keys=True))
    print("ACT5 equal_before: keys=%s sha=%s days=%s newer_days_after_%s=%s delete_markers=%d" % (out["history_keys"] == b["history_keys"], digest == b["history_keys_sha256"], len(hist) == b["history_days"], NEWEST, newer, markers))
    ok = (digest == b["history_keys_sha256"] and out["history_keys"] == b["history_keys"] and one and two and len(landed) == 66 and out["held_days_absent"] and out["schedule_state"] == "ENABLED" and markers == 0)
    return 0 if ok else 3


def cmd_compile():
    ev = []
    for i, (s, e, n) in enumerate(EVENTS, 1):
        inv, rd = load("%d_invoke.json" % i), load("%d_read.json" % i)
        ev.append({"payload": inv["payload"], "invoked_utc": inv["invoked_utc"], "status_code": inv["status_code"], "function_error": inv["function_error"], "returned": inv["returned"], "report": inv["report"],
                   "rows": rd["rows"], "before_partial": rd["before_partial"], "partial": rd["partial"], "full": rd["full"], "full_to_partial": rd["full_to_partial"], "partial_to_full": rd["partial_to_full"],
                   "floor_day_accounts": rd["floor_day_accounts"], "floor_day_positive": rd["floor_day_positive"], "changed_by_day": rd["changed_by_day"], "request_id": inv["request_id"]})
    di, dr = load("dry_invoke.json"), load("dry_read.json")
    rec = {"claim": "measured", "gates": load("gates.json"), "ledger_entry": OWN_SLUG, "applier": chk.APPLIER, "before": load("before.json"), "build": load("build.json"), "plan": load("plan.json"),
           "apply_finished_utc": load("apply_finished.json")["apply_finished_utc"], "after": load("after.json"),
           "dry_run": {"payload": di["payload"], "invoked_utc": di["invoked_utc"], "status_code": di["status_code"], "function_error": di["function_error"], "returned": di["returned"], "report": di["report"],
                       "rows_match_landed": dr["rows_match_landed"], "versions_unchanged": dr["versions_unchanged"], "request_id": di["request_id"]},
           "events": ev, "act5": load("act5.json"), "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    (HERE / "COT_LANDING_REWRITE_R2_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote COT_LANDING_REWRITE_R2_RECORD.json keys=%s" % sorted(rec))
    return 0


if __name__ == "__main__":
    c = sys.argv[1]
    sys.exit({"gates": cmd_gates, "before": cmd_before, "act5": cmd_act5, "compile": cmd_compile}.get(c, lambda: {"after_apply": cmd_after_apply, "invoke": cmd_invoke, "read": cmd_read}[c](sys.argv[2]))())
