"""IRPT_DASHBD TO-DB-b-328 (applier 0.7.0_AE_CloudOps~IB2): the filled-report switch-on pair, the reads, the events and the record.

  python fill328.py gates | before | probe_off | sched | pass dry|full | canary_pick | canary_write | after | compile

Every event is ONE synchronous invoke (never retried here). Client ids live in memory and in a scratch file OUTSIDE the repo (the canary id, $TEMP/f328_canary_id.txt);
only counts, digests, hashes and words are printed or written. Writes (the canary, the full pass) go through the function only, never from this script.
"""
import base64
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import boto3
from botocore.config import Config

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cotc0_318 as c0  # noqa: E402  (ROOT, now_utc, directory(), git)

HERE = Path(__file__).resolve().parent
STATE = HERE / "state328"
ROOT = c0.ROOT
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PACKET = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS.md"
COO_HALF = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_49F_FILLED_REPORT_SWITCH_ON_FIRST_PASS_CTO_HALF.md"
PACKET_SHA = "3248f3c488fff06b00a165ee5a98da0bd0f509a013d23238dd8590af04290573"
SLUG = "irpt-dashbd-49f-filled-report-switch-on-first-pass-20261017"
FN, ROLE, POLICY = "irpt-49f-reporting-publish-lambda", "irpt-49f-reporting-publish-role", "irpt-49f-reporting-publish-policy"
BUCKET, PREFIX = "opal-data-49financial", "irpt/49financial/platinum/reporting/"
CODE_BEFORE, VERSION_BEFORE = "s/OKOv98j53aFJCLrBpYP8xh3oUcuWagn0vSHVBjhIM=", "oXM0wQg8revg3asMHOhpbz1gPDnXaatK"
POLICY_HASH16 = "e6a7e585f3021a05"
SCHEDULES = ["irpt-49f-reporting-gold-daily", "irpt-49f-reporting-publish-daily", "irpt-49f-reporting-publish-summaries-daily"]
ART_BUCKET, ART_KEY = "opal-313476888478-lambda-artifacts", "investor-reporting/irpt-reporting-publish-lambda.zip"
OFF = {"enabled": False, "clients": 0, "written": 0, "not_available": [], "refused": []}
SURFACE = ("irpt-49f-reporting-publish-lambda", "reporting-publish", "irpt/49financial/platinum/reporting")
CANARY_FILE = Path(os.environ.get("TEMP", "/tmp")) / "f328_canary_id.txt"
s3 = boto3.client("s3", region_name="us-east-1")
iam = boto3.client("iam", region_name="us-east-1")
sch = boto3.client("scheduler", region_name="us-east-1")
lam_cfg = boto3.client("lambda", region_name="us-east-1")
LAM = boto3.client("lambda", region_name="us-east-1", config=Config(read_timeout=900, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"}))


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def digest12(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def git(*a):
    import subprocess
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT)).stdout


def counts():
    series = 0
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
        series += sum(1 for c in pg.get("CommonPrefixes", []) if c["Prefix"][len(PREFIX):].startswith("account="))
    summ = fill = other = 0
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for o in pg.get("Contents", []):
            k = o["Key"][len(PREFIX):]
            if re.fullmatch(r"client=[^/]+/summary\.json", k):
                summ += 1
            elif re.fullmatch(r"client=[^/]+/filled_report\.json", k):
                fill += 1
            else:
                other += 1
    return {"series_prefixes": series, "summary_objects": summ, "filled_objects": fill, "other_objects": other}


def prefix_total():
    n = 0
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        n += len(pg.get("Contents", []))
    return n


def role_hash():
    doc = iam.get_role_policy(RoleName=ROLE, PolicyName=POLICY)["PolicyDocument"]
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16], len(doc.get("Statement", []))


def art_current():
    vs = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=ART_BUCKET, Prefix=ART_KEY):
        vs += [v for v in pg.get("Versions", []) if v["Key"] == ART_KEY]
    return [v for v in vs if v["IsLatest"]][0]["VersionId"]


def open_legs_on_surface():
    wts = [ln[9:] for ln in git("worktree", "list", "--porcelain").splitlines() if ln.startswith("worktree ")]
    files, found = 0, []
    seen = set()
    for wt in wts:
        for n in [x for x in git("-C", wt, "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/.open_deploys/").split("\n") if x.strip()]:
            files += 1
            slug = Path(n).stem
            if slug in seen or slug == SLUG:
                continue
            seen.add(slug)
            led = list((ROOT / "org/critical_paths/change_management").glob("*_%s_deploy_completion.md" % slug))
            if not led:
                continue
            text = led[0].read_text(encoding="utf-8", errors="replace")
            head = text[:1500]
            if "**Status:** CLOSED" in head or "**Status:** ROLLED-BACK" in head:
                continue
            for ln in text.splitlines():
                if re.match(r"\|\s*[A-Za-z]\w*\s*\|", ln) and ln.rstrip().endswith("OPEN |") and any(s in ln for s in SURFACE):
                    found.append(slug)
    return len(wts), files, sorted(set(found))


def cmd_gates():
    packet = (ROOT / PACKET).read_bytes()
    sha = hashlib.sha256(packet).hexdigest()
    coo, cto = (ROOT / COO_HALF).read_text(encoding="utf-8"), (ROOT / CTO_HALF).read_text(encoding="utf-8")
    coo_ok, cto_ok = "SIGNED" in coo and PACKET_SHA in coo, "SIGNED" in cto and PACKET_SHA[:8] in cto
    import subprocess
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", "4d4cf3e2c4", "HEAD"], cwd=str(ROOT)).returncode == 0
    nw, nf, found = open_legs_on_surface()
    cfg = lam_cfg.get_function_configuration(FunctionName=FN)
    env = sorted((cfg.get("Environment") or {}).get("Variables", {}))
    rh, nst = role_hash()
    scs = {n: sch.get_schedule(Name=n)["State"] for n in SCHEDULES}
    cur = art_current()
    live_ok = (cfg["CodeSha256"] == CODE_BEFORE and cur == VERSION_BEFORE and env == [] and all(v == "ENABLED" for v in scs.values()) and rh == POLICY_HASH16 and nst == 8)
    print("GATES packet_sha_ok=%s coo=%s cto=%s options_code_ancestor=%s" % (sha == PACKET_SHA, coo_ok, cto_ok, anc))
    print("GATES worktrees_read=%d marker_files_read=%d open_legs_on_this_surface=%d %s" % (nw, nf, len(found), found))
    print("GATES live: code_ok=%s version_ok=%s env=%s schedules=%s policy_hash_ok=%s statements=%d -> live_matches_packet=%s" % (cfg["CodeSha256"] == CODE_BEFORE, cur == VERSION_BEFORE, env, scs, rh == POLICY_HASH16, nst, live_ok))
    save("gates.json", {"packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok, "one_change_at_a_time": {"worktrees_read": nw, "open_markers_naming_this_surface": len(found)}, "live_matches_packet": bool(live_ok)})
    return 0 if (sha == PACKET_SHA and coo_ok and cto_ok and anc and not found and live_ok) else 3


def cmd_before():
    cfg = lam_cfg.get_function_configuration(FunctionName=FN)
    rh, _ = role_hash()
    out = {"code_sha256": cfg["CodeSha256"], "artifact_version_id": art_current(), "env_keys": sorted((cfg.get("Environment") or {}).get("Variables", {})),
           "schedules": sorted(SCHEDULES), "role_policy_hash16": rh}
    out.update(counts())
    save("before.json", out)
    print("BEFORE", json.dumps(out, sort_keys=True))
    return 0


def invoke(payload):
    t = c0.now_utc()
    resp = LAM.invoke(FunctionName=FN, InvocationType="RequestResponse", LogType="Tail", Payload=json.dumps(payload).encode("utf-8"))
    body = json.loads(resp["Payload"].read().decode("utf-8"))
    ltxt = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace") if resp.get("LogResult") else ""
    m = re.search(r"Duration: ([0-9.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ltxt, re.S)
    rep = {"duration_s": round(float(m.group(1)) / 1000.0, 1) if m else None, "max_memory_mb": int(m.group(3)) if m else None}
    flags = {"timed_out": "Task timed out" in ltxt, "access_denied": "AccessDenied" in ltxt, "function_error": resp.get("FunctionError"), "request_id": resp["ResponseMetadata"]["RequestId"], "invoked_utc": t}
    return body, rep, flags


def cmd_probe_off():
    body, rep, fl = invoke({"filled_report": True, "clients": ["cli_PROBE"], "shard": 99, "shards": 7})
    ok = body == OFF
    save("probe_off.json", {"response": body, "payload_shape": "clients+shard+shards", "_flags": fl})
    print("PROBE_OFF exact_off=%s response_keys=%s function_error=%s" % (ok, sorted(body) if isinstance(body, dict) else type(body).__name__, fl["function_error"]))
    return 0 if ok else 3


def cmd_sched():
    inputs, none = {}, True
    for n in SCHEDULES:
        s = sch.get_schedule(Name=n)
        inp = s["Target"].get("Input", "")
        inputs[n] = len(inp)
        if "filled_report" in inp:
            none = False
    save("schedule_inputs.json", {"checked": len(SCHEDULES), "none_contains_filled_report": none})
    print("SCHED checked=%d none_contains_filled_report=%s input_lengths=%s" % (len(SCHEDULES), none, inputs))
    return 0 if none else 3


def shard_event(kind, k):
    payload = {"filled_report": True, "shard": k, "shards": 7}
    if kind == "dry":
        payload["dry_run"] = True
    body, rep, fl = invoke(payload)
    row = {"shard": k, "clients": body.get("clients"), "written": body.get("written"), "not_available": len(body.get("not_available") or []), "refused": len(body.get("refused") or []),
           "max_memory_mb": rep["max_memory_mb"], "duration_s": rep["duration_s"]}
    problems = []
    if fl["timed_out"] or fl["access_denied"] or fl["function_error"]:
        problems.append("timeout, AccessDenied or function error: %s" % {k2: v for k2, v in fl.items() if k2 in ("timed_out", "access_denied", "function_error")})
    if body.get("enabled") is not True:
        problems.append("enabled is not true")
    if rep["max_memory_mb"] is None or rep["max_memory_mb"] > 819 or rep["duration_s"] is None or rep["duration_s"] > 240:
        problems.append("memory above 819 MB or duration above 240 s: %s" % rep)
    if row["refused"] * 10 > (row["clients"] or 0):
        problems.append("refused above 10 percent of the clients")
    return row, problems


def cmd_pass(kind):
    if (STATE / ("%s.json" % kind)).exists():
        print("REFUSED: the %s pass was already run (state file present)" % kind)
        return 2
    if kind == "full" and not (STATE / "canary.json").exists():
        print("REFUSED: the canary is not recorded")
        return 2
    tt = dt.datetime.now(dt.timezone.utc)
    if tt.weekday() < 5 and dt.time(12, 5) <= tt.time() <= dt.time(13, 15):
        print("STOP: inside the weekday fire window")
        return 3
    before = prefix_total()
    rows = []
    for k in range(7):
        row, problems = shard_event(kind, k)
        rows.append(row)
        print("%s shard %d %s %s" % (kind.upper(), k, json.dumps(row, sort_keys=True), "PROBLEMS: %s" % problems if problems else "ok"), flush=True)
        save("%s_partial.json" % kind, rows)
        if problems:
            return 3
    after = prefix_total()
    tot = {key: sum(r[key] for r in rows) for key in ("clients", "written", "not_available", "refused")}
    if kind == "dry":
        # the directory's CLIENT count (distinct client ids), counts only
        rec = {"directory_clients": len(client_ids()), "shards": rows, "objects_before": before, "objects_after": after}
        print("DRY totals %s directory_clients=%s objects %d -> %d (must be equal)" % (tot, rec["directory_clients"], before, after))
        save("dry.json", rec)
        return 0 if (before == after and tot["clients"] == rec["directory_clients"] and tot["written"] >= 1) else 3
    dry = load("dry.json")
    dtot = {key: sum(r[key] for r in dry["shards"]) for key in ("clients", "written", "not_available", "refused")}
    rec = {"shards": rows, "written_total": tot["written"], "objects_before": before, "objects_after": after}
    print("FULL totals %s dry totals %s equal=%s prefix gain %d (want dry written - 1 = %d)" % (tot, dtot, tot == dtot, after - before, dtot["written"] - 1))
    save("full.json", rec)
    return 0 if (tot == dtot and after - before == dtot["written"] - 1) else 3


def client_ids():
    d, _ = c0.directory("49financial")
    return sorted({(e.get("ids") or {}).get("client_id") for e in d["entries"] if (e.get("ids") or {}).get("client_id")})


def cmd_canary_pick():
    if CANARY_FILE.exists():
        print("REFUSED: a canary is already picked (scratch file present)")
        return 2
    for i, cid in enumerate(client_ids()):
        body, rep, fl = invoke({"filled_report": True, "clients": [cid], "dry_run": True})
        ok = body.get("enabled") is True and body.get("written") == 1 and not body.get("not_available") and not body.get("refused") and not (fl["timed_out"] or fl["access_denied"] or fl["function_error"])
        print("CANARY_PICK candidate %d single-client dry run: written=%s not_available=%d refused=%d -> %s" % (i, body.get("written"), len(body.get("not_available") or []), len(body.get("refused") or []), "PICK" if ok else "skip"), flush=True)
        if ok:
            CANARY_FILE.write_text(cid, encoding="ascii")
            save("canary_pick.json", {"client_digest12": digest12(cid), "dry_run_written": 1, "candidate_index": i})
            print("CANARY_PICK digest12=%s (the id is in %s, outside the repo)" % (digest12(cid), CANARY_FILE))
            return 0
        if i >= 60:
            break
    print("STOP: no clean single-client candidate in the first 60")
    return 3


def cmd_canary_write():
    cid = CANARY_FILE.read_text(encoding="ascii").strip()
    pick = load("canary_pick.json")
    before = prefix_total()
    body, rep, fl = invoke({"filled_report": True, "clients": [cid]})
    after = prefix_total()
    key = "%sclient=%s/filled_report.json" % (PREFIX, cid)
    try:
        s3.head_object(Bucket=BUCKET, Key=key)
        exists = True
    except Exception:  # noqa: BLE001
        exists = False
    validates = False
    if exists:
        sys.path.insert(0, str(ROOT))
        sys.path.insert(0, str(ROOT / "infra/aws/lambda/investor-reporting/reporting-publish"))
        import publisher
        try:
            publisher.validate_filled_report(json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8")))
            validates = True
        except Exception as ex:  # noqa: BLE001
            print("validate raised", type(ex).__name__)
    rec = {"client_digest12": pick["client_digest12"], "dry_run_written": 1, "clients": body.get("clients"), "written": body.get("written"), "object_exists": exists, "validates": validates, "prefix_gain": after - before}
    save("canary.json", rec)
    print("CANARY", json.dumps(rec, sort_keys=True), "memory_mb=%s duration_s=%s function_error=%s" % (rep["max_memory_mb"], rep["duration_s"], fl["function_error"]))
    return 0 if (rec["clients"] == 1 and rec["written"] == 1 and exists and validates and rec["prefix_gain"] == 1) else 3


def cmd_timing():
    """D2 msg 10385: two read-only dry runs (the first 5, then the first 25 sorted directory clients); counts, time and memory only; no id recorded."""
    ids = client_ids()
    out = []
    for n in (5, 25):
        before = prefix_total()
        body, rep, fl = invoke({"filled_report": True, "clients": ids[:n], "dry_run": True})
        after = prefix_total()
        row = {"clients_requested": n, "clients": body.get("clients"), "written": body.get("written"), "not_available": len(body.get("not_available") or []), "refused": len(body.get("refused") or []),
               "duration_s": rep["duration_s"], "max_memory_mb": rep["max_memory_mb"], "timed_out": fl["timed_out"], "function_error": fl["function_error"], "prefix_objects_equal": before == after}
        out.append(row)
        print("TIMING", json.dumps(row, sort_keys=True), flush=True)
        if fl["timed_out"] or fl["function_error"]:
            break
    save("timing.json", out)
    return 0


def cmd_after():
    cfg = lam_cfg.get_function_configuration(FunctionName=FN)
    rh, _ = role_hash()
    layers = [x["Arn"] for x in cfg.get("Layers", [])]
    conc = lam_cfg.get_function_concurrency(FunctionName=FN).get("ReservedConcurrentExecutions")
    out = {"function": {"code_sha256": cfg["CodeSha256"], "memory_mb": cfg["MemorySize"], "timeout_s": cfg["Timeout"], "env_keys": sorted((cfg.get("Environment") or {}).get("Variables", {})),
                        "layer": ":".join(layers[0].split(":")[-2:]) if layers else None, "reserved_concurrency": conc},
           "role_policy_hash16": rh, "schedules": sorted(n for n in SCHEDULES if sch.get_schedule(Name=n)["State"] == "ENABLED")}
    out.update(counts())
    save("after.json", out)
    print("AFTER", json.dumps(out, sort_keys=True))
    return 0


def cmd_compile():
    rec = {"claim": "measured", "gates": load("gates.json"), "ledger_entry": SLUG, "applier": c0.APPLIER, "before": load("before.json"), "build": load("build.json"), "plans": load("plans.json"),
           "probe_off": {k: v for k, v in load("probe_off.json").items() if k != "_flags"}, "schedule_inputs": load("schedule_inputs.json"), "dry_run": load("dry.json"), "canary": load("canary.json"),
           "v_leg": load("v_leg.json"), "full": load("full.json"), "after": load("after.json"), "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0},
           "notes": (STATE / "notes.txt").read_text(encoding="ascii").strip()}
    (HERE / "FILLED_PASS_APPLY_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote FILLED_PASS_APPLY_RECORD.json")
    return 0


if __name__ == "__main__":
    c = sys.argv[1]
    fn = {"gates": cmd_gates, "before": cmd_before, "probe_off": cmd_probe_off, "sched": cmd_sched, "canary_pick": cmd_canary_pick, "canary_write": cmd_canary_write, "after": cmd_after, "timing": cmd_timing, "compile": cmd_compile}
    sys.exit(fn[c]() if c in fn else cmd_pass(sys.argv[2]))
