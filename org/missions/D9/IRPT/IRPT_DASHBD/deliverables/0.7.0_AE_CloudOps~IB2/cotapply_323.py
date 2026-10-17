"""IRPT_DASHBD TO-DB-b-323 (applier 0.7.0_AE_CloudOps~IB2): C4 of the Cottonwood Performance read path, the reads, the eight probes and the record.

  python cotapply_323.py gates                 step 0: packet bytes, halves, ancestry, one-change-at-a-time census, live state (read only)
  python cotapply_323.py before                step 2: the BEFORE reads -> state323/before.json
  python cotapply_323.py probe <label>         ONE synthetic invoke by label (never retried here) -> state323/probe_<label>.json
  python cotapply_323.py simulate <which>      the iam simulations -> state323/simulate.json
  python cotapply_323.py after                 step 8: the AFTER reads -> state323/after.json
  python cotapply_323.py compile               assemble COT_READ_APPLY_RECORD.json from state323/

Writes nothing to AWS. The client's ids, display name and the staff identity live in memory only; counts, hashes, statuses and words are printed and written.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import boto3
from botocore.config import Config

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cotc0_318 as c0  # noqa: E402  (the C0 script: ids module, directory, published map, the staff header shape)

HERE = Path(__file__).resolve().parent
STATE = HERE / "state323"
ROOT = c0.ROOT
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
PACKET = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD.md"
COO_HALF = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD_COO_HALF.md"
CTO_HALF = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD_CTO_HALF.md"
PACKET_SHA = "07e9ab116825445bd7414e3963075be518036fe4eb209ceb93a7ede44d97cd87"
LANDING = ("3eb27c60c0", "10dac78f46", "67cc230180")
C3_RECORD = D + "0.9.0_WK_IRPT_DASHBD~255/RD_COT_READ_FUNCTION_MAP_FACTS_R150.json"
SLUG = "irpt-dashbd-cottonwood-read-path-forward-20261017"
COT_FN, READ_FN = "irpt-cot-reporting-read-lambda", "irpt-49f-reporting-read-lambda"
COT_ROLE, READ_ROLE = "irpt-cot-reporting-read-role", "irpt-49f-reporting-read-role"
BUCKET, PREFIX = "opal-data-cottonwood", "irpt/cottonwood/platinum/reporting/"
ART_BUCKET = "opal-313476888478-lambda-artifacts"
READ_KEY, COT_KEY = "investor-reporting/irpt-reporting-read-lambda.zip", "investor-reporting/irpt-cot-reporting-read-lambda.zip"
SURFACE = re.compile(r"irpt-49f-reporting-read-lambda|irpt-cot-reporting-read-lambda|reporting-read-iso|investor-reporting/reporting-read\b|7k3ed8px20", re.I)
LABELS = ["cot-direct-manifest", "cot-direct-series", "cot-direct-forged", "control-49f-manifest", "cot-via-49f-manifest", "cot-via-49f-series", "inflection-via-49f", "noninternal-cot-via-49f"]
s3 = boto3.client("s3", region_name="us-east-1")
iam = boto3.client("iam", region_name="us-east-1")
lam_cfg = boto3.client("lambda", region_name="us-east-1")
LAM = boto3.client("lambda", region_name="us-east-1", config=Config(read_timeout=900, connect_timeout=15, retries={"max_attempts": 0, "mode": "standard"}))


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / name).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def load(name):
    return json.loads((STATE / name).read_text(encoding="ascii"))


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(ROOT)).stdout


def canon(doc):
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def exists_key(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except Exception as ex:  # noqa: BLE001
        code = getattr(ex, "response", {}).get("Error", {}).get("Code", "")
        if code in ("404", "NoSuchKey", "NotFound"):
            return False
        raise


def fn_exists(name):
    try:
        lam_cfg.get_function_configuration(FunctionName=name)
        return True
    except lam_cfg.exceptions.ResourceNotFoundException:
        return False


def role_exists(name):
    try:
        iam.get_role(RoleName=name)
        return True
    except iam.exceptions.NoSuchEntityException:
        return False


def counts():
    prefixes = 0
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
        prefixes += len(pg.get("CommonPrefixes", []))
    keys, versions = set(), 0
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=BUCKET, Prefix=PREFIX):
        for v in pg.get("Versions", []):
            keys.add(v["Key"])
            versions += 1
    return prefixes, len(keys), versions


def bucket_policy():
    doc = json.loads(s3.get_bucket_policy(Bucket=BUCKET)["Policy"])
    return canon(doc), len(doc.get("Statement", []))


def art_current(key):
    vs = []
    for pg in s3.get_paginator("list_object_versions").paginate(Bucket=ART_BUCKET, Prefix=key):
        vs += [v for v in pg.get("Versions", []) if v["Key"] == key]
    cur = [v for v in vs if v["IsLatest"]]
    return (cur[0]["VersionId"] if cur else None), len(vs)


def cmd_gates():
    packet = (ROOT / PACKET).read_bytes()
    sha = hashlib.sha256(packet).hexdigest()
    coo, cto = (ROOT / COO_HALF).read_text(encoding="utf-8"), (ROOT / CTO_HALF).read_text(encoding="utf-8")
    coo_ok = "SIGNED" in coo and PACKET_SHA in coo
    cto_ok = "SIGNED" in cto and PACKET_SHA[:12] in cto
    anc = {c: subprocess.run(["git", "merge-base", "--is-ancestor", c, "HEAD"], cwd=str(ROOT)).returncode == 0 for c in LANDING}
    wts = [ln[9:] for ln in git("worktree", "list", "--porcelain").splitlines() if ln.startswith("worktree ")]
    live, stale, files = [], 0, 0
    for wt in wts:
        for n in [x for x in git("-C", wt, "ls-tree", "-r", "--name-only", "HEAD", "org/critical_paths/.open_deploys/").split("\n") if x.strip()]:
            files += 1
            if SURFACE.search(git("-C", wt, "show", "HEAD:" + n)):
                slug = Path(n).stem
                if slug == SLUG:
                    continue
                led = list((ROOT / "org/critical_paths/change_management").glob("*_%s_deploy_completion.md" % slug))
                head = led[0].read_text(encoding="utf-8", errors="replace")[:1500] if led else ""
                if "**Status:** CLOSED" in head or "**Status:** ROLLED-BACK" in head:
                    stale += 1
                else:
                    live.append((Path(wt).name, slug))
    cfg = lam_cfg.get_function_configuration(FunctionName=READ_FN)
    cur, nv = art_current(READ_KEY)
    live_ok = (not fn_exists(COT_FN) and not role_exists(COT_ROLE) and not exists_key(ART_BUCKET, COT_KEY) and cur == "J9krUD0Qw3fz5QdcfYM4CRg7bYlHNigW"
               and cfg["CodeSha256"] == "z634S2QsrfCpY4c3cD2UGwicdmLDo6/Rmng8SrEskCQ=")
    print("GATES packet_sha_ok=%s coo_signed=%s cto_signed=%s ancestors=%s" % (sha == PACKET_SHA, coo_ok, cto_ok, anc))
    print("GATES worktrees_read=%d marker_files_read=%d stale_closed_slugs_naming_surface=%d live_markers_naming_surface=%d %s" % (len(wts), files, stale, len(live), live[:4]))
    print("GATES live: cot_function_absent=%s cot_role_absent=%s cot_artifact_absent=%s read_artifact_current=%s (versions %d) read_code_ok=%s -> live_matches_packet=%s" % (
        not fn_exists(COT_FN), not role_exists(COT_ROLE), not exists_key(ART_BUCKET, COT_KEY), cur, nv, cfg["CodeSha256"] == "z634S2QsrfCpY4c3cD2UGwicdmLDo6/Rmng8SrEskCQ=", live_ok))
    save("gates.json", {"packet_sha256": sha, "coo_half_signed": coo_ok, "cto_half_signed": cto_ok,
                        "one_change_at_a_time": {"worktrees_read": len(wts), "open_markers_naming_this_surface": len(live)}, "live_matches_packet": bool(live_ok)})
    return 0 if (sha == PACKET_SHA and coo_ok and cto_ok and all(anc.values()) and not live and live_ok) else 3


def cmd_before():
    cfg = lam_cfg.get_function_configuration(FunctionName=READ_FN)
    cur, _ = art_current(READ_KEY)
    p, o, v = counts()
    bp, n = bucket_policy()
    out = {"cot_function_exists": fn_exists(COT_FN), "cot_role_exists": role_exists(COT_ROLE), "cot_artifact_exists": exists_key(ART_BUCKET, COT_KEY), "read_artifact_version_id": cur,
           "read_code_sha256": cfg["CodeSha256"], "prefixes": p, "objects": o, "versions": v, "bucket_policy_sha256": bp, "bucket_policy_statements": n}
    save("before.json", out)
    print("BEFORE", json.dumps({k: (x if k != "bucket_policy_sha256" else x[:12]) for k, x in out.items()}, sort_keys=True))
    return 0


def event(account_id, which, tenant, forged=False, noninternal=False):
    h = c0.staff_headers()
    if noninternal:
        h = dict(h, **{"x-firm-id": "49financial", "x-user-type": "advisor", "x-user-role": "user", "x-user-tier": "advisor"})
    if forged:
        h = dict(h, **{"x-origin-verify": "not-the-edge"})
    ev = {"routeKey": c0.ROUTE_KEY, "headers": h, "pathParameters": {"account_id": account_id, "which": which}, "queryStringParameters": {"selected_tenant": tenant}}
    if forged:
        ev["forwarded_from"] = READ_FN
        ev["forward"] = {"firm": "cottonwood", "internal": True}
    return ev


def clients():
    ids = c0.ids_module()
    cdir, _ = c0.directory("cottonwood")
    ent = [e for e in cdir["entries"] if str(e.get("display_name", "")).strip().lower().startswith("thiessen")]
    assert len(ent) >= 1
    cot_acct = (ent[0].get("ids") or {}).get("account_ids")[0]
    _, fraws = c0.published("49financial", ids)
    return cot_acct, ids.opaque_account("49financial", fraws[0])


SPEC = {  # label -> (function, account, which, tenant, forged, noninternal)
    "cot-direct-manifest": (COT_FN, "cot", "manifest", "cottonwood", False, False),
    "cot-direct-series": (COT_FN, "cot", "series", "cottonwood", False, False),
    "cot-direct-forged": (COT_FN, "cot", "manifest", "cottonwood", True, False),
    "control-49f-manifest": (READ_FN, "ctrl", "manifest", "49financial", False, False),
    "cot-via-49f-manifest": (READ_FN, "cot", "manifest", "cottonwood", False, False),
    "cot-via-49f-series": (READ_FN, "cot", "series", "cottonwood", False, False),
    "inflection-via-49f": (READ_FN, "cot", "manifest", "inflection", False, False),
    "noninternal-cot-via-49f": (READ_FN, "cot", "manifest", "cottonwood", False, True),
}


def cmd_probe(label):
    if (STATE / ("probe_%s.json" % label)).exists():
        print("REFUSED: %s was already probed (state file present)" % label)
        return 2
    fn, acct, which, tenant, forged, noninternal = SPEC[label]
    cot_acct, ctrl_acct = clients()
    ev = event(cot_acct if acct == "cot" else ctrl_acct, which, tenant, forged, noninternal)
    t = c0.now_utc()
    resp = LAM.invoke(FunctionName=fn, InvocationType="RequestResponse", LogType="Tail", Payload=json.dumps(ev).encode("utf-8"))
    raw = resp["Payload"].read()
    out = json.loads(raw.decode("utf-8"))
    hdrs = {str(k).lower(): v for k, v in (out.get("headers") or {}).items()} if isinstance(out, dict) else {}
    status = out.get("statusCode") if isinstance(out, dict) else None
    reason, bare = None, False
    if isinstance(out, dict) and status is None and "operation" in out and isinstance(out.get("status"), dict):
        bare, status = True, 200  # a bare refusal envelope (no statusCode): API Gateway's payload 2.0 default is 200 (INFERRED)
        cand = out["status"].get("public_reason_code")
        reason = cand if isinstance(cand, str) and re.match(r"^[A-Z][A-Z0-9_]{2,40}$", cand) else None
    elif isinstance(out, dict) and isinstance(out.get("body"), str) and status is not None and (status >= 400 or not out.get("isBase64Encoded")):
        try:
            cand = (json.loads(out["body"]).get("status") or {}).get("public_reason_code")
            reason = cand if isinstance(cand, str) and re.match(r"^[A-Z][A-Z0-9_]{2,40}$", cand) else None
        except (ValueError, AttributeError):
            reason = None
    rec = {"label": label, "method": "lambda-invoke", "status": int(status) if status is not None else -1, "reason_code": reason, "content_encoding": hdrs.get("content-encoding"),
           "size_bytes": len(raw), "invoked_utc": t, "request_id": resp["ResponseMetadata"]["RequestId"]}
    log = resp.get("LogResult", "")
    import base64
    ltxt = base64.b64decode(log).decode("utf-8", "replace") if log else ""
    m = re.search(r"Duration: ([0-9.]+) ms.*?Memory Size: (\d+) MB\s+Max Memory Used: (\d+) MB", ltxt, re.S)
    extra = {"duration_ms": float(m.group(1)) if m else None, "max_memory_mb": int(m.group(3)) if m else None, "memory_size_mb": int(m.group(2)) if m else None,
             "timed_out": "Task timed out" in ltxt, "access_denied": "AccessDenied" in ltxt, "function_error": resp.get("FunctionError"), "bare_envelope": bare}
    save("probe_%s.json" % label, dict(rec, _extra=extra))
    print("PROBE %s fn=%s status=%s bare=%s reason=%s enc=%s size=%d function_error=%s duration_ms=%s max_mem=%s/%s timed_out=%s access_denied=%s" % (
        label, fn, rec["status"], bare, reason, rec["content_encoding"], rec["size_bytes"], extra["function_error"], extra["duration_ms"], extra["max_memory_mb"], extra["memory_size_mb"],
        extra["timed_out"], extra["access_denied"]))
    return 0


def simulate_one(arn_policy_source, action, resource):
    r = iam.simulate_principal_policy(PolicySourceArn=arn_policy_source, ActionNames=[action], ResourceArns=[resource])
    return r["EvaluationResults"][0]["EvalDecision"]


def cmd_simulate(which):
    role_arn = iam.get_role(RoleName=READ_ROLE)["Role"]["Arn"]
    acct = role_arn.split(":")[4]
    sim = json.loads((STATE / "simulate.json").read_text(encoding="ascii")) if (STATE / "simulate.json").exists() else {}
    if which == "deny":
        other = [f["FunctionName"] for f in lam_cfg.get_paginator("list_functions").paginate().__iter__().__next__()["Functions"] if f["FunctionName"] not in (COT_FN, READ_FN)][0]
        sim["invoke_other_function"] = simulate_one(role_arn, "lambda:InvokeFunction", "arn:aws:lambda:us-east-1:%s:function:%s" % (acct, other))
        sim["s3_get_cottonwood_platinum"] = simulate_one(role_arn, "s3:GetObject", "arn:aws:s3:::%s/%sx/series.json.gz" % (BUCKET, PREFIX + "account=PLACEHOLDER"))
    else:
        sim["invoke_new_function"] = simulate_one(role_arn, "lambda:InvokeFunction", "arn:aws:lambda:us-east-1:%s:function:%s" % (acct, COT_FN))
    save("simulate.json", sim)
    print("SIMULATE", json.dumps(sim, sort_keys=True))
    return 0


def cmd_after():
    cc = lam_cfg.get_function_configuration(FunctionName=COT_FN)
    rc = lam_cfg.get_function_configuration(FunctionName=READ_FN)
    p, o, v = counts()
    bp, _ = bucket_policy()
    out = {"cot_function": {"code_sha256": cc["CodeSha256"], "memory_mb": cc["MemorySize"], "timeout_s": cc["Timeout"], "env_keys": sorted((cc.get("Environment") or {}).get("Variables", {})), "role": cc["Role"].rsplit("/", 1)[-1]},
           "read_function": {"code_sha256": rc["CodeSha256"], "env_keys": sorted((rc.get("Environment") or {}).get("Variables", {})), "forward_value": (rc.get("Environment") or {}).get("Variables", {}).get("IRPT_FORWARD_COTTONWOOD_FUNCTION")},
           "read_role_policies": sorted(iam.list_role_policies(RoleName=READ_ROLE)["PolicyNames"]), "bucket_policy_sha256": bp, "prefixes": p, "objects": o, "versions": v}
    save("after.json", out)
    print("AFTER", json.dumps(out, sort_keys=True)[:900])
    return 0


def cmd_compile():
    probes = []
    for lab in LABELS:
        p = load("probe_%s.json" % lab)
        p.pop("_extra", None)
        probes.append(p)
    rec = {"claim": "measured", "gates": load("gates.json"), "ledger_entry": SLUG, "applier": c0.APPLIER, "before": load("before.json"), "build": load("build.json"), "plans": load("plans.json"),
           "probes": probes, "probe_identity_class": "OPAL_GLOBAL", "simulate": load("simulate.json"), "after": load("after.json"), "ledger_closed": False,
           "reads": {"vendor_calls": 0, "secret_reads": 0}, "notes": (STATE / "notes.txt").read_text(encoding="ascii").strip()}
    (HERE / "COT_READ_APPLY_RECORD.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="ascii")
    print("COMPILE wrote COT_READ_APPLY_RECORD.json")
    return 0


if __name__ == "__main__":
    c = sys.argv[1]
    sys.exit({"gates": cmd_gates, "before": cmd_before, "after": cmd_after, "compile": cmd_compile}.get(c, lambda: {"probe": cmd_probe, "simulate": cmd_simulate}[c](sys.argv[2]))())
