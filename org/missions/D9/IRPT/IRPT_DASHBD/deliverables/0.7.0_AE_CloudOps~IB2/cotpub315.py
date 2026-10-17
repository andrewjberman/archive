"""IRPT_DASHBD TO-DB-b-315 (applier 0.7.0_AE_CloudOps~IB2): the reads and the three invokes of the Cottonwood reporting-publish 0.4.0 apply and republish.

  python cotpub315.py gates                 packet bytes, halves, ancestry, one-change-at-a-time census, live state vs the packet (read only)
  python cotpub315.py before                the BEFORE state -> state315/before.json
  python cotpub315.py after_apply <UTC>     the function and schedule after the apply -> state315/after.json
  python cotpub315.py prewrite              the pre-write counts from the read tool's output file -> state315/pre_write.json (STOP lines checked)
  python cotpub315.py invoke dry|canary|full   ONE synchronous invoke (never retried here) -> state315/<name>_invoke.json, with its after-read
  python cotpub315.py compile               assemble COT_PUBLISH_HOP2_RECORD.json from state315/

Counts, dates, keys, hashes and words only: no account id is printed or written (only account_hash12).
"""
import base64
import datetime as dt
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
from botocore.config import Config

ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True, cwd=str(Path(__file__).resolve().parent)).strip())
HERE = Path(__file__).resolve().parent
STATE = HERE / "state315"
CHK_PATH = ROOT / "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~D2/checks/r149/p182_cot_publish_apply.py"
spec = importlib.util.spec_from_file_location("p182_for_cotpub315", str(CHK_PATH))
chk = importlib.util.module_from_spec(spec)
sys.modules["p182_for_cotpub315"] = chk
spec.loader.exec_module(chk)

REGION = "us-east-1"
FUNCTION, SCHEDULE = chk.FUNCTION, chk.SCHEDULE
ART_BUCKET, ART_KEY = chk.ARTIFACT_BUCKET, chk.ARTIFACT_KEY
SURFACE = re.compile(r"reporting-publish-iso|irpt-cot-reporting-publish|cottonwood/platinum/reporting", re.I)
OWN_SLUG = chk.LEDGER_SLUG
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


def schedule():
    sc = sch.get_schedule(Name=SCHEDULE)
    return {"state": sc["State"], "cron": sc["ScheduleExpression"], "zone": sc.get("ScheduleExpressionTimezone")}


def artifact_current():
    vs = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=ART_BUCKET, Prefix=ART_KEY):
        vs += [v for v in pg.get("Versions", []) if v["Key"] == ART_KEY]
    return [v for v in vs if v["IsLatest"]][0]["VersionId"], len(vs)


def handler_mod():
    sys.path[:0] = [str(ROOT / "infra/aws/lambda/investor-reporting"), str(ROOT / "infra/aws/lambda/investor-reporting/reporting-publish"), str(ROOT)]
    for m in ("handler", "publisher"):
        sys.modules.pop(m, None)
    import handler as h  # noqa: E402
    return h


def prefix_counts():
    """series / manifest / other object counts under irpt/cottonwood/platinum/reporting/ by key name (client-side, auto-paginated), plus the denominator."""
    h = handler_mod()
    bucket, key = h._split(h.opal_naming.address("irpt", "cottonwood", h.TIER_PLATINUM, h.TABLE_PLATINUM, "account=x", "series.json.gz"))
    prefix = key.split("account=")[0]
    ser = man = oth = tot = 0
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        for o in pg.get("Contents", []):
            tot += 1
            k = o["Key"]
            if k.endswith("series.json.gz"):
                ser += 1
            elif k.endswith("manifest.json"):
                man += 1
            else:
                oth += 1
    return {"series": ser, "manifest": man, "other": oth}, tot


def published_docs(h):
    _b, mp, _u = h._published_map(s3, "cottonwood")
    raws = sorted(mp.values())

    def one(raw):
        doc = h._read_published(s3, "cottonwood", raw)
        return raw, doc["series"].get("history_scope"), doc["series"].get("history_scope_claim"), doc["manifest"].get("publisher_version")
    with ThreadPoolExecutor(16) as pool:
        return list(pool.map(one, raws))


def cmd_gates():
    packet = chk.PACKET_REL
    blob = git("hash-object", packet).strip()
    sha = hashlib.sha256((ROOT / packet).read_bytes()).hexdigest()
    coo = (ROOT / chk.COO_HALF_REL).read_text(encoding="utf-8")
    cto = (ROOT / chk.CTO_HALF_REL).read_text(encoding="utf-8")
    coo_ok = "SIGNED" in coo and chk.PACKET_SHA in coo
    cto_ok = "SIGNED" in cto and chk.PACKET_SHA[:12] in cto
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", "cbf7ead020", "HEAD"], cwd=str(ROOT)).returncode == 0
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
    live_ok = (cfg["CodeSha256"] == chk.BEFORE_CODE and cfg["MemorySize"] == 1024 and cfg["Timeout"] == 900 and conc is None and not (cfg.get("Environment") or {}).get("Variables")
               and cur == chk.BEFORE_VERSION and scs["state"] == "DISABLED" and scs["cron"] == chk.CRON)
    gates = {"packet_blob": blob, "packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok, "pin_is_ancestor": anc,
             "one_change_at_a_time": {"worktrees_read": len(wts), "open_markers_naming_this_surface": len(live)}, "live_matches_packet": bool(live_ok)}
    print("GATES blob_ok=%s sha_ok=%s coo=%s cto=%s ancestor=%s" % (blob == chk.PACKET_BLOB, sha == chk.PACKET_SHA, coo_ok, cto_ok, anc))
    print("GATES worktrees_read=%d stale_closed_slugs=%d live_markers_naming_surface=%d %s" % (len(wts), stale, len(live), live[:3]))
    print("GATES live: code_ok=%s mem=%s timeout=%s conc=%s env=%s artifact_current_ok=%s (artifact versions %d) schedule=%s -> live_matches_packet=%s" % (
        cfg["CodeSha256"] == chk.BEFORE_CODE, cfg["MemorySize"], cfg["Timeout"], conc, bool((cfg.get("Environment") or {}).get("Variables")), cur == chk.BEFORE_VERSION, nvers, scs, live_ok))
    save("gates.json", gates)
    return 0 if (blob == chk.PACKET_BLOB and sha == chk.PACKET_SHA and coo_ok and cto_ok and anc and not live and live_ok) else 3


def cmd_before():
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    cur, _n = artifact_current()
    objs, tot = prefix_counts()
    h = handler_mod()
    docs = published_docs(h)
    scopes = {}
    for _r, sc, _cl, _pv in docs:
        scopes[str(sc)] = scopes.get(str(sc), 0) + 1
    out = {"function_code_sha256": cfg["CodeSha256"], "artifact_version_id": cur, "schedule": {k: v for k, v in schedule().items() if k != "zone"}, "objects": objs, "history_scope_counts": scopes}
    save("before.json", out)
    print("BEFORE code=%s artifact_current=%s schedule=%s" % (out["function_code_sha256"], cur, out["schedule"]))
    print("BEFORE objects=%s (denominator: %d keys listed) history_scope_counts=%s" % (objs, tot, scopes))
    ok = out["function_code_sha256"] == chk.BEFORE_CODE and cur == chk.BEFORE_VERSION and objs["series"] == 939 and objs["manifest"] == 939 and scopes == {"PARTIAL_HISTORY": 939}
    return 0 if ok else 3


def cmd_after_apply(utc):
    cfg = lam_read.get_function_configuration(FunctionName=FUNCTION)
    conc = lam_read.get_function_concurrency(FunctionName=FUNCTION).get("ReservedConcurrentExecutions")
    layers = [x["Arn"] for x in cfg.get("Layers", [])]
    out = {"function": {"memory": cfg["MemorySize"], "timeout": cfg["Timeout"], "reserved_concurrency": conc, "code_sha256": cfg["CodeSha256"], "layer_arn": layers[0] if layers else None},
           "schedule": {k: v for k, v in schedule().items() if k != "zone"}}
    save("after.json", out)
    save("apply_finished.json", {"apply_finished_utc": utc})
    print("AFTER code=%s memory=%s timeout=%s conc=%s layers=%d handler=%s env=%s schedule=%s" % (cfg["CodeSha256"], cfg["MemorySize"], cfg["Timeout"], conc, len(layers), cfg["Handler"], bool((cfg.get("Environment") or {}).get("Variables")), out["schedule"]))
    return 0


def cmd_prewrite(path):
    txt = open(path, encoding="utf-8").read()
    flips = dict(re.findall(r"\('(\w+)', '(\w+)'\): (\d+)", txt)[0:0])
    m = re.search(r"scope flips \(old,new\): (\{.*\})", txt)
    flipd = eval(m.group(1)) if m else {}  # noqa: S307 -- the read tool prints a dict of tuple keys; counts only
    over = eval(re.search(r"changed value on a day present in BOTH \(by field\): (\{.*\})", txt).group(1))  # noqa: S307
    res = eval(re.search(r"RESULT total \d+ (\{.*\})", txt).group(1))  # noqa: S307
    del flips
    p2f = flipd.get(("PARTIAL_HISTORY", "FULL"), 0)
    f2p = flipd.get(("FULL", "PARTIAL_HISTORY"), 0)
    pw = {"partial_to_full": p2f, "full_to_partial": f2p, "series_gaining_day": res.get("new_days_added", 0), "changed_total_return_common": over.get("total_return_daily", 0),
          "changed_external_flow_common": over.get("external_flow", 0), "changed_value_common": over.get("value", 0), "changed_income_common": over.get("income", 0),
          "changed_price_return_common": over.get("holdings_price_return", 0), "refused": res.get("new_refused", 0), "published_series": 939}
    save("pre_write.json", pw)
    print("PREWRITE %s" % pw)
    stops = []
    if pw["full_to_partial"] > 0 or pw["partial_to_full"] > 150:
        stops.append("scope flips")
    if pw["changed_value_common"] or pw["changed_income_common"] or pw["changed_price_return_common"]:
        stops.append("value, income or price return changed on a common day")
    if pw["changed_total_return_common"] > 800 or pw["changed_external_flow_common"] > 800 or pw["refused"] > 0:
        stops.append("daily return or flow above 800, or refused")
    print("PREWRITE STOP lines: %s" % (stops or "none crossed (expected 102 / 826 / 657 / 659 / 0 per the packet)"))
    return 0 if not stops else 3


def invoke(payload):
    cfg = Config(read_timeout=960, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"})
    lam = boto3.client("lambda", region_name=REGION, config=cfg)
    resp = lam.invoke(FunctionName=FUNCTION, InvocationType="RequestResponse", LogType="Tail", Payload=json.dumps(payload).encode("ascii"))
    body = json.loads(resp["Payload"].read().decode("utf-8"))
    log = base64.b64decode(resp.get("LogResult", "")).decode("utf-8", "replace")
    m = re.search(r"REPORT RequestId: (\S+)\s+Duration: ([0-9.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", log, re.S)
    return resp, body, log, m


def cmd_invoke(name):
    if (STATE / ("%s_invoke.json" % name)).exists():
        print("REFUSED: %s was already invoked (state file present)" % name)
        return 2
    prev = {"dry": None, "canary": "dry", "full": "canary"}[name]
    if prev and not (STATE / ("%s_check.json" % prev)).exists():
        print("REFUSED: the previous act's check is not recorded")
        return 2
    if name == "dry" and not (STATE / "pre_write.json").exists():
        print("REFUSED: the pre-write read is not recorded")
        return 2
    t = now_utc()
    if chk.G.in_window(t, "12:05", "12:45"):
        print("STOP: inside the landing fire window")
        return 3
    if name == "dry":
        payload = {}
    elif name == "canary":
        acct = open(os.path.join(os.environ["TEMP"], "cot315_canary_id.txt"), encoding="ascii").read().strip()
        payload = {"upload": True, "accounts": [acct]}
    else:
        payload = {"upload": True}
    shown = {"upload": True, "accounts": 1} if name == "canary" else payload
    save("%s_invoking.json" % name, {"payload_shape": shown, "invoked_utc": t})
    print("INVOKE %s sending at %s payload_shape=%s" % (name, t, json.dumps(shown)), flush=True)
    resp, body, log, m = invoke(payload)
    ret = {"uploaded": body.get("uploaded"), "published": body.get("published"), "refused": body.get("refused")} if isinstance(body, dict) else body
    if isinstance(ret.get("refused"), (list, dict)):
        ret["refused"] = len(ret["refused"])
    rec = {"payload": ({} if name == "dry" else shown), "invoked_utc": t, "status_code": resp["StatusCode"], "function_error": resp.get("FunctionError"), "returned": ret,
           "report": ({"max_memory_used_mb": int(m.group(4)), "duration_ms": float(m.group(2)), "memory_size_mb": int(m.group(3))} if m else None), "request_id": m.group(1) if m else None,
           "raw_keys": sorted(body) if isinstance(body, dict) else None}
    save("%s_invoke.json" % name, rec)
    print("INVOKE %s status=%s function_error=%s returned=%s raw_keys=%s report=%s request_id=%s" % (name, rec["status_code"], rec["function_error"], ret, rec["raw_keys"], rec["report"], rec["request_id"]))
    problems = []
    if rec["function_error"] or not m or "Task timed out" in log or "AccessDenied" in log:
        problems.append("function error, no REPORT line, a timeout or an AccessDenied: %s" % log[:300].replace("\n", " "))
    if rec["report"] and (rec["report"]["max_memory_used_mb"] > chk.MEM_LINE or rec["report"]["duration_ms"] > chk.DUR_LINE):
        problems.append("memory above %d MB or duration above %d ms: %s" % (chk.MEM_LINE, chk.DUR_LINE, rec["report"]))
    before = load("before.json")
    objs, tot = prefix_counts()
    check = {"objects_after": objs}
    if name == "dry":
        if not (ret.get("uploaded") is False and ret.get("published") == 939 and isinstance(ret.get("refused"), int) and ret["refused"] <= (939 + ret["refused"]) // 10):
            problems.append("dry run answer: %s" % ret)
        if objs != before["objects"]:
            problems.append("a dry run changed the prefix's object counts: %s" % objs)
    elif name == "canary":
        h = handler_mod()
        import publisher
        acct = open(os.path.join(os.environ["TEMP"], "cot315_canary_id.txt"), encoding="ascii").read().strip()
        doc = h._read_published(s3, "cottonwood", acct)
        ser, man = doc["series"], doc["manifest"]
        b, k = h._split(h.opal_naming.address("irpt", "cottonwood", h.TIER_PLATINUM, h.TABLE_PLATINUM, "account=%s" % acct, "series.json.gz"))
        mb, mk = h._split(h.opal_naming.address("irpt", "cottonwood", h.TIER_PLATINUM, h.TABLE_PLATINUM, "account=%s" % acct, "manifest.json"))

        def nvers(bucket, key):
            return sum(1 for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in pg.get("Versions", []) if v["Key"] == key)
        stored = s3.head_object(Bucket=b, Key=k)["ContentLength"]
        contract = json.loads((ROOT / "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json").read_text(encoding="utf-8"))
        bad = publisher.validate_against_contract(ser, man, contract)
        checks = {"validates_contract": not bad, "scope_full": ser.get("history_scope") == "FULL", "claim_inferred": ser.get("history_scope_claim") == "inferred",
                  "basis_present": bool(ser.get("history_scope_basis")), "manifest_publisher_040": man.get("publisher_version") == "0.4.0",
                  "prior_versions_kept": nvers(b, k) >= 2 and nvers(mb, mk) >= 2,
                  "series_size_equals_manifest": (man.get("byte_sizes") or {}).get("series.json.gz") == stored}
        print("CANARY contract problems=%d stored_series_bytes=%s manifest_byte_sizes=%s versions series=%d manifest=%d" % (len(bad), stored, (man.get("byte_sizes") or {}), nvers(b, k), nvers(mb, mk)))
        check.update({"account_hash12": hashlib.sha256(acct.encode()).hexdigest()[:12], "checks": checks, "manifest_keys": sorted(man)})
        if not all(checks.values()) or ret != {"uploaded": ret.get("uploaded"), "published": 1, "refused": 0} or objs != before["objects"]:
            problems.append("canary checks or answer: %s %s %s" % (checks, ret, objs))
    else:
        h = handler_mod()
        docs = published_docs(h)
        claim = sum(1 for _r, _s, c, _p in docs if c == "inferred")
        full = sum(1 for _r, s, _c, _p in docs if s == "FULL")
        pubs = {p for _r, _s, _c, p in docs}
        pw = load("pre_write.json")
        check.update({"claim_count": claim, "full_count": full, "partial_count": len(docs) - full, "manifest_publisher_versions": sorted(str(x) for x in pubs)})
        if not (ret.get("published") == 939 and ret.get("refused") == load("dry_invoke.json")["returned"]["refused"] and claim == 939 and full == pw["partial_to_full"] and pubs == {"0.4.0"} and objs == before["objects"]):
            problems.append("full republish check: %s %s" % (check, ret))
    save("%s_check.json" % name, check)
    print("INVOKE %s check=%s" % (name, {k: v for k, v in check.items() if k != "checks"}))
    if name == "canary":
        print("CANARY checks=%s" % check.get("checks"))
    print("INVOKE %s PROBLEMS: %s" % (name, problems or "none"))
    return 0 if not problems else 3


def cmd_fullcheck():
    """The deeper after-read of the full republish: every series against its ORIGINAL (oldest) version, every key's versions, ten sampled accounts."""
    import gzip
    h = handler_mod()
    import publisher
    docs = published_docs(h)
    raws = [d[0] for d in docs]
    contract = json.loads((ROOT / "org/standards/IRPT_DASHBD_SERIES_CONTRACT.json").read_text(encoding="utf-8"))

    def keys(acct):
        sb, sk = h._split(h.opal_naming.address("irpt", "cottonwood", h.TIER_PLATINUM, h.TABLE_PLATINUM, "account=%s" % acct, "series.json.gz"))
        mb, mk = h._split(h.opal_naming.address("irpt", "cottonwood", h.TIER_PLATINUM, h.TABLE_PLATINUM, "account=%s" % acct, "manifest.json"))
        return sb, sk, mb, mk

    def versions(bucket, key):
        vs = [v for pg in s3.get_paginator("list_object_versions").paginate(Bucket=bucket, Prefix=key) for v in pg.get("Versions", []) if v["Key"] == key]
        return sorted(vs, key=lambda v: v["LastModified"])

    def one(acct):
        sb, sk, mb, mk = keys(acct)
        sv, mv = versions(sb, sk), versions(mb, mk)
        cur = json.loads(gzip.decompress(s3.get_object(Bucket=sb, Key=sk, VersionId=sv[-1]["VersionId"])["Body"].read()))
        old = json.loads(gzip.decompress(s3.get_object(Bucket=sb, Key=sk, VersionId=sv[0]["VersionId"])["Body"].read()))
        od, nd = old.get("date") or [], cur.get("date") or []
        oi = {d: i for i, d in enumerate(od)}
        ni = {d: i for i, d in enumerate(nd)}
        common = [d for d in od if d in ni]
        ov, nv = old.get("value"), cur.get("value")
        changed = isinstance(ov, list) and isinstance(nv, list) and any(ov[oi[d]] != nv[ni[d]] for d in common)
        return acct, len(sv) >= 2 and len(mv) >= 2, bool(changed)

    with ThreadPoolExecutor(16) as pool:
        res = list(pool.map(one, raws))
    kept = all(r[1] for r in res)
    changed_n = sum(1 for r in res if r[2])
    sample = [raws[min(len(raws) - 1, (i * len(raws)) // 10)] for i in range(10)]
    ok_all = True
    for acct in sample:
        doc = h._read_published(s3, "cottonwood", acct)
        sb, sk, _mb, _mk = keys(acct)
        stored = s3.head_object(Bucket=sb, Key=sk)["ContentLength"]
        bad = publisher.validate_against_contract(doc["series"], doc["manifest"], contract)
        ok = (not bad and doc["series"].get("history_scope_claim") == "inferred" and bool(doc["series"].get("history_scope_basis")) and doc["manifest"].get("publisher_version") == "0.4.0"
              and (doc["manifest"].get("byte_sizes") or {}).get("series.json.gz") == stored)
        ok_all = ok_all and ok
    out = {"changed_value_common_count": changed_n, "prior_versions_kept": bool(kept), "sampled_hash12": [hashlib.sha256(a.encode()).hexdigest()[:12] for a in sample], "sample_checks_pass": bool(ok_all)}
    save("full_deep.json", out)
    print("FULLCHECK series=%d prior_versions_kept=%s changed_value_common_count=%d sample_checks_pass=%s sampled=%d" % (len(raws), kept, changed_n, ok_all, len(sample)))
    return 0 if (kept and changed_n == 0 and ok_all) else 3


def cmd_compile():
    d, c, f = load("dry_invoke.json"), load("canary_invoke.json"), load("full_invoke.json")
    cc, fc, deep = load("canary_check.json"), load("full_check.json"), load("full_deep.json")

    def ev(x):
        return {k: x[k] for k in ("payload", "invoked_utc", "status_code", "function_error", "returned", "report")}
    rec = {"claim": "measured", "gates": load("gates.json"), "ledger_entry": OWN_SLUG, "applier": chk.APPLIER, "before": load("before.json"), "build": load("build.json"), "plan": load("plan.json"),
           "apply_finished_utc": load("apply_finished.json")["apply_finished_utc"], "after": load("after.json"), "pre_write": load("pre_write.json"),
           "dry_run": dict(ev(d), request_id=d["request_id"]),
           "canary": {"payload_shape": c["payload"] if "accounts" in c["payload"] and isinstance(c["payload"]["accounts"], int) else {"upload": True, "accounts": 1}, "account_hash12": cc["account_hash12"], "invoked_utc": c["invoked_utc"],
                      "status_code": c["status_code"], "function_error": c["function_error"], "returned": {"published": c["returned"]["published"], "refused": c["returned"]["refused"]}, "report": c["report"],
                      "objects_after": cc["objects_after"], "checks": cc["checks"], "request_id": c["request_id"]},
           "full": dict(ev(f), objects_after=fc["objects_after"], claim_count=fc["claim_count"], full_count=fc["full_count"], partial_count=fc["partial_count"],
                        changed_value_common_count=deep["changed_value_common_count"], prior_versions_kept=deep["prior_versions_kept"], sampled_hash12=deep["sampled_hash12"],
                        sample_checks_pass=deep["sample_checks_pass"], request_ids=[f["request_id"]]),
           "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}}
    rec["dry_run"]["returned"] = {"uploaded": d["returned"]["uploaded"], "published": d["returned"]["published"], "refused": d["returned"]["refused"]}
    rec["full"]["returned"] = {"published": f["returned"]["published"], "refused": f["returned"]["refused"]}
    (HERE / "COT_PUBLISH_HOP2_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote COT_PUBLISH_HOP2_RECORD.json keys=%s" % sorted(rec))
    return 0


if __name__ == "__main__":
    c = sys.argv[1]
    sys.exit({"gates": cmd_gates, "before": cmd_before, "compile": cmd_compile, "fullcheck": cmd_fullcheck}.get(c, lambda: {"after_apply": cmd_after_apply, "invoke": cmd_invoke, "prewrite": cmd_prewrite}[c](sys.argv[2]))())
