"""IRPT_DASHBD round 150 (issuer 2.0.0_SA_COO~D2) -- C4 of the Cottonwood Performance read path: the APPLY of the signed never-widen pair (packet NEVER_WIDEN_PACKET_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD.md): the bundle build of
BOTH function-map entries, ONE safe-apply of the new root `reporting-read-iso` (exactly 5 add / 0 change / 0 destroy), the direct probes of the new function, ONE safe-apply of `reporting-read` (exactly 1 add / 1 change / 0 destroy),
the probes through the live 49 Financial function, and the receipt. WORLD. The record is the applier's (`0.7.0_AE_CloudOps~IB2`); the checker re-reads the world.

  DBC189-1-AC1  the record: both halves signed at the packet's sha256, the ledger, the build hash from the C3 record, the two plans, the eight probes by label (status, reason token, size), the simulations, the counts before and after
  DBC189-2-AC1  FRESH live reads: both functions run the bundle's code hash with the recorded environment keys, the new role is `-cot-`, the 49 Financial role gained exactly the forward policy and its other three policies are byte-identical to the packet
  DBC189-3-AC1  FRESH live reads: the Cottonwood bucket policy, the 939 prefixes and the API routes are as the record says and nothing routes to the new function

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


H = helper("r147/p151_pubapply.py", "p151_helper_189")
need, nes, is_int, Fail = H.need, H.nes, H.is_int, H.Fail
D = H.D
APPLIER = "0.7.0_AE_CloudOps~IB2"
REC_REL = D + APPLIER + "/COT_READ_APPLY_RECORD.json"
PACKET_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_PACKET_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD.md"
COO_HALF_REL = D + "2.0.0_SA_COO~D2/NEVER_WIDEN_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD_COO_HALF.md"
CTO_HALF_REL = D + "1.0.0_SA_CTO~DELL2/NEVER_WIDEN_COTTONWOOD_PERFORMANCE_READ_PATH_FORWARD_CTO_HALF.md"
C3_RECORD_REL = D + "0.9.0_WK_IRPT_DASHBD~255/RD_COT_READ_FUNCTION_MAP_FACTS_R150.json"
LEDGER_SLUG = "irpt-dashbd-cottonwood-read-path-forward-20261017"
COT_FN, READ_FN = "irpt-cot-reporting-read-lambda", "irpt-49f-reporting-read-lambda"
COT_ROLE, READ_ROLE = "irpt-cot-reporting-read-role", "irpt-49f-reporting-read-role"
FORWARD_POLICY = "irpt-49f-reporting-read-forward-policy"
COT_POLICIES = sorted(["irpt-cot-reporting-read-policy", "irpt-cot-reporting-read-service-profile-policy"])
OLD_POLICIES = {"irpt-49f-reporting-read-policy": "fb3891535e540a7d", "irpt-49f-reporting-read-service-profile-policy": "3f23ca0ec834c691", "irpt-reporting-read-render-grant-read-policy": "7e5c7c3fffef8c78"}
READ_ENV_BEFORE = ["IRPT_DIRECTORY_BUCKET_MAP", "IRPT_EVIDENCE_BUCKET", "IRPT_FIRM_REGISTRY"]
READ_ENV_AFTER = sorted(READ_ENV_BEFORE + ["IRPT_FORWARD_COTTONWOOD_FUNCTION"])
COT_ENV = ["IRPT_DIRECTORY_BUCKET_MAP", "IRPT_FIRM_REGISTRY"]
READ_CODE_BEFORE = "z634S2QsrfCpY4c3cD2UGwicdmLDo6/Rmng8SrEskCQ="
ROLLBACK_VERSION = "J9krUD0Qw3fz5QdcfYM4CRg7bYlHNigW"
BUCKET, PREFIX = "opal-data-cottonwood", "irpt/cottonwood/platinum/reporting/"
PREFIXES, BUCKET_STATEMENTS = 939, 7
API_ID = "7k3ed8px20"
LABELS = ["cot-direct-manifest", "cot-direct-series", "cot-direct-forged", "control-49f-manifest", "cot-via-49f-manifest", "cot-via-49f-series", "inflection-via-49f", "noninternal-cot-via-49f"]
OK_LABELS = {"cot-direct-manifest", "cot-direct-series", "control-49f-manifest", "cot-via-49f-manifest", "cot-via-49f-series"}
REFUSED_LABELS = {"cot-direct-forged", "inflection-via-49f", "noninternal-cot-via-49f"}
REASON = re.compile(r"^[A-Z][A-Z0-9_]{2,40}$")
B64 = re.compile(r"[A-Za-z0-9+/]{43}=$")
H.DIGIT_OK_KEYS = tuple(H.DIGIT_OK_KEYS) + ("request_id", "invoked_utc", "sha256_before", "sha256_after", "version_id", "artifact_version_id", "cot_entry_sha256_b64", "read_entry_sha256_b64", "code_sha256", "read_code_sha256",
                                           "bucket_policy_sha256", "new_version_id", "packet_sha256")


def canon(doc):
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def check_head(rec, packet_sha, coo_text, cto_text, ledger_exists, c3_hash):
    exp = {"claim", "gates", "ledger_entry", "applier", "before", "build", "plans", "probes", "probe_identity_class", "simulate", "after", "ledger_closed", "reads", "notes"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["claim"] == "measured", "claim must be measured")
    need(rec["probe_identity_class"] == "OPAL_GLOBAL", "the staff probes must use an OPAL_GLOBAL internal identity, the class used at Global (CTO msg 10262), and the receipt names it")
    g = rec["gates"]
    need(isinstance(g, dict) and set(g) == {"packet_sha256", "coo_half_signed", "cto_half_signed", "one_change_at_a_time", "live_matches_packet"}, "gates keys")
    need(g["packet_sha256"] == packet_sha, "the packet's sha256 differs from the file at HEAD")
    need(g["coo_half_signed"] is True and "SIGNED" in coo_text and packet_sha in coo_text, "the COO half does not read SIGNED at the packet's sha256")
    need(g["cto_half_signed"] is True and "SIGNED" in cto_text and packet_sha[:12] in cto_text, "the CTO half does not read SIGNED at the packet's sha256")
    oc = g["one_change_at_a_time"]
    need(isinstance(oc, dict) and set(oc) == {"worktrees_read", "open_markers_naming_this_surface"} and is_int(oc["worktrees_read"]) and oc["worktrees_read"] >= 1 and oc["open_markers_naming_this_surface"] == 0, "one_change_at_a_time: the denominator and zero markers")
    need(g["live_matches_packet"] is True, "the live state must be recorded as matching the packet's section 2")
    need(rec["ledger_entry"] == LEDGER_SLUG and ledger_exists, "the ledger entry %s must exist" % LEDGER_SLUG)
    need(rec["applier"] == APPLIER, "the applier must be %s" % APPLIER)
    b = rec["before"]
    keys = {"cot_function_exists", "cot_role_exists", "cot_artifact_exists", "read_artifact_version_id", "read_code_sha256", "prefixes", "objects", "versions", "bucket_policy_sha256", "bucket_policy_statements"}
    need(isinstance(b, dict) and set(b) == keys, "before keys")
    need(b["cot_function_exists"] is False and b["cot_role_exists"] is False and b["cot_artifact_exists"] is False, "before: the new function, role and artifact absent")
    need(b["read_artifact_version_id"] == ROLLBACK_VERSION and b["read_code_sha256"] == READ_CODE_BEFORE, "before: the 49 Financial function runs the packet's rollback version")
    need(b["prefixes"] == PREFIXES and is_int(b["objects"]) and b["objects"] >= PREFIXES and is_int(b["versions"]) and b["versions"] >= b["objects"] and b["bucket_policy_statements"] == BUCKET_STATEMENTS and nes(b["bucket_policy_sha256"]),
         "before: %d prefixes, object and version counts, the bucket policy at %d statements" % (PREFIXES, BUCKET_STATEMENTS))
    bd = rec["build"]
    need(isinstance(bd, dict) and set(bd) == {"cot_entry_sha256_b64", "read_entry_sha256_b64", "members"}, "build keys")
    need(B64.match(str(bd["cot_entry_sha256_b64"])) and bd["cot_entry_sha256_b64"] == bd["read_entry_sha256_b64"] == c3_hash and bd["members"] == 32, "both entries must build the C3 record's hash %s (32 members)" % c3_hash)
    pl = rec["plans"]
    need(isinstance(pl, dict) and set(pl) == {"iso", "read"}, "plans keys")
    for name, (a, c, d) in (("iso", (5, 0, 0)), ("read", (1, 1, 0))):
        p = pl[name]
        need(isinstance(p, dict) and set(p) == {"add", "change", "destroy", "replan_no_changes"} and (p["add"], p["change"], p["destroy"]) == (a, c, d) and p["replan_no_changes"] is True,
             "plan %s must read %d add / %d change / %d destroy with a clean re-plan after the apply" % (name, a, c, d))
    return True


def check_probes(rec):
    pr = rec["probes"]
    need(isinstance(pr, list) and [p.get("label") for p in pr] == LABELS, "probes must be exactly these labels in order: %s" % LABELS)
    by = {}
    for p in pr:
        need(set(p) == {"label", "method", "status", "reason_code", "content_encoding", "size_bytes", "invoked_utc", "request_id"}, "probe keys: %s" % p.get("label"))
        need(p["method"] == "lambda-invoke" and is_int(p["status"]) and 100 <= p["status"] <= 599 and H.UTC.match(str(p["invoked_utc"])) and nes(p["request_id"]) and is_int(p["size_bytes"]) and p["size_bytes"] >= 0,
             "probe %s: lambda-invoke, a status, a UTC time, a request id, a size" % p["label"])
        need(p["reason_code"] is None or REASON.match(str(p["reason_code"])), "probe %s: reason_code a token or null, never a sentence" % p["label"])
        by[p["label"]] = p
    for lab in OK_LABELS:
        need(by[lab]["status"] == 200 and by[lab]["reason_code"] is None and by[lab]["size_bytes"] > 0, "probe %s must be served (200, no refusal token, a body)" % lab)
    for lab in REFUSED_LABELS:
        need(by[lab]["reason_code"] is not None, "probe %s must carry a refusal reason token" % lab)
    need(by["inflection-via-49f"]["reason_code"] == "FIRM_BINDING", "a firm the literal map does not name must be refused FIRM_BINDING")
    for a, b in (("cot-direct-manifest", "cot-via-49f-manifest"), ("cot-direct-series", "cot-via-49f-series")):
        need(by[a]["size_bytes"] == by[b]["size_bytes"] and by[a]["content_encoding"] == by[b]["content_encoding"], "the forward must return the reply untouched: %s vs %s differ in size or encoding" % (a, b))
    need(by["cot-direct-series"]["content_encoding"] == "gzip", "the series reply must be gzip")
    need(by["cot-direct-forged"]["size_bytes"] < by["cot-direct-manifest"]["size_bytes"], "a forged-forward refusal must carry less than the served manifest")
    sim = rec["simulate"]
    need(isinstance(sim, dict) and sim == {"invoke_new_function": "allowed", "invoke_other_function": "implicitDeny", "s3_get_cottonwood_platinum": "implicitDeny"}, "simulations: invoke of the new function allowed, of another function denied, S3 GetObject on a Cottonwood platinum key denied")
    return True


def check_after(rec, c3_hash):
    a = rec["after"]
    keys = {"cot_function", "read_function", "read_role_policies", "bucket_policy_sha256", "prefixes", "objects", "versions"}
    need(isinstance(a, dict) and set(a) == keys, "after keys")
    cf, rf = a["cot_function"], a["read_function"]
    need(isinstance(cf, dict) and set(cf) == {"code_sha256", "memory_mb", "timeout_s", "env_keys", "role"} and cf["code_sha256"] == c3_hash and cf["memory_mb"] == 512 and cf["timeout_s"] == 29
         and sorted(cf["env_keys"]) == COT_ENV and cf["role"] == COT_ROLE, "the new function: the bundle's hash, 512 MB, 29 s, exactly the two environment keys and the -cot- role")
    need(isinstance(rf, dict) and set(rf) == {"code_sha256", "env_keys", "forward_value"} and rf["code_sha256"] == c3_hash and sorted(rf["env_keys"]) == READ_ENV_AFTER and rf["forward_value"] == COT_FN,
         "the 49 Financial function: the bundle's hash, the three environment keys plus the forward variable naming the new function")
    need(sorted(a["read_role_policies"]) == sorted(list(OLD_POLICIES) + [FORWARD_POLICY]), "the 49 Financial role must hold its three policies plus the forward policy")
    b = rec["before"]
    need(a["bucket_policy_sha256"] == b["bucket_policy_sha256"], "the Cottonwood bucket policy changed")
    need(a["prefixes"] == b["prefixes"] and a["objects"] == b["objects"] and a["versions"] == b["versions"], "the 939 series prefix counts differ before and after: this pair writes nothing")
    need(rec["ledger_closed"] is False and rec["reads"] == {"vendor_calls": 0, "secret_reads": 0}, "the ledger left OPEN for the issuer (the order: the issuer closes it after verification) and the reads block")
    need(isinstance(rec["notes"], str) and 20 <= len(rec["notes"]) <= 2400, "notes: words")
    return True


def check_record(rec, packet_sha, coo_text, cto_text, ledger_exists, c3_hash):
    check_head(rec, packet_sha, coo_text, cto_text, ledger_exists, c3_hash)
    check_probes(rec)
    check_after(rec, c3_hash)
    return True


def check_live_functions(cot_cfg, read_cfg, read_policies, forward_doc, cot_policy_names, c3_hash):
    need(cot_cfg["CodeSha256"] == c3_hash and cot_cfg["MemorySize"] == 512 and cot_cfg["Timeout"] == 29 and cot_cfg["Handler"] == "entry.lambda_handler", "the new function: code hash, 512 MB, 29 s and handler differ from the bundle")
    need(sorted((cot_cfg.get("Environment") or {}).get("Variables", {})) == COT_ENV, "the new function's environment keys must be exactly %s" % COT_ENV)
    need(cot_cfg["Role"].endswith("/" + COT_ROLE) and "-cot-" in cot_cfg["Role"], "the new function's role must be %s (the -cot- token the bucket fence admits)" % COT_ROLE)
    need(read_cfg["CodeSha256"] == c3_hash, "the 49 Financial function does not run the bundle")
    env = (read_cfg.get("Environment") or {}).get("Variables", {})
    need(sorted(env) == READ_ENV_AFTER and env.get("IRPT_FORWARD_COTTONWOOD_FUNCTION") == COT_FN, "the 49 Financial function's environment keys must be %s with the forward variable naming %s" % (READ_ENV_AFTER, COT_FN))
    need(read_cfg["MemorySize"] == 512 and read_cfg["Timeout"] == 29, "the 49 Financial function's memory and timeout must not move")
    need(sorted(read_policies) == sorted(list(OLD_POLICIES) + [FORWARD_POLICY]), "the 49 Financial role must hold exactly its three policies plus %s" % FORWARD_POLICY)
    for name, h in OLD_POLICIES.items():
        need(canon(read_policies[name])[:16] == h, "the policy %s differs from the packet's pre-state" % name)
    st = forward_doc.get("Statement")
    need(isinstance(st, list) and len(st) == 1 and st[0].get("Sid") == "InvokeTheCottonwoodReadFunctionOnly" and st[0].get("Effect") == "Allow", "the forward policy must hold exactly the one statement")
    act, res = st[0].get("Action"), st[0].get("Resource")
    act = [act] if isinstance(act, str) else act
    res = [res] if isinstance(res, str) else res
    need(act == ["lambda:InvokeFunction"] and isinstance(res, list) and len(res) == 1 and res[0].endswith(":function:" + COT_FN), "the one statement is lambda:InvokeFunction on the one new function")
    need(sorted(cot_policy_names) == COT_POLICIES, "the new role must hold exactly %s" % COT_POLICIES)
    return True


def check_live_world(rec, bucket_doc, prefixes, routes, integrations):
    need(len(bucket_doc.get("Statement", [])) == BUCKET_STATEMENTS and canon(bucket_doc) == rec["after"]["bucket_policy_sha256"], "the Cottonwood bucket policy differs from the record (statement count or hash)")
    need(prefixes == rec["after"]["prefixes"] == PREFIXES, "the live platinum reporting prefix count is %s, the record says %s" % (prefixes, rec["after"]["prefixes"]))
    perf = [r for r in routes if "/investor-reporting/reporting/" in r.get("RouteKey", "")]
    need(len(perf) == 3, "the three Performance routes must still exist (read %d)" % len(perf))
    targets = {r.get("Target") for r in perf}
    need(len(targets) == 1, "the three routes must still share ONE integration")
    iid = next(iter(targets)).split("/")[-1]
    uri = integrations[iid]
    need(READ_FN in uri and COT_FN not in uri, "the routes' one integration must still invoke the 49 Financial function")
    need(not [u for u in integrations.values() if COT_FN in u], "no integration may invoke the new function: it is reached only by the forward")
    return True


# ------------------------------------------------------------------------------------------------ the live run
def run(root, cid):
    root = Path(root)
    rec = H.load(root, REC_REL)
    packet = (root / PACKET_REL).read_bytes()
    packet_sha = hashlib.sha256(packet).hexdigest()
    coo = (root / COO_HALF_REL).read_text(encoding="utf-8") if (root / COO_HALF_REL).is_file() else ""
    cto = (root / CTO_HALF_REL).read_text(encoding="utf-8") if (root / CTO_HALF_REL).is_file() else ""
    c3 = H.load(root, C3_RECORD_REL)["build_only_sha256"]
    ledger_exists = bool(list((root / "org/critical_paths/.open_deploys").glob(LEDGER_SLUG + "*.json"))) or bool(list((root / "org/critical_paths/change_management").glob("*" + LEDGER_SLUG + "*")))
    check_record(rec, packet_sha, coo, cto, ledger_exists, c3)
    scrub = dict(rec, notes=re.sub(r"[a-z][a-z0-9-]*-\d{8}", "ledger", str(rec["notes"])))  # a ledger slug ends in a date; any other 8-digit run is a leak
    need(not H.digit_runs(scrub), "a run of 8 or more digits outside the exempt fields: %s" % H.digit_runs(scrub)[:2])
    if cid == "DBC189-1-AC1":
        print("OK: both halves read SIGNED at the packet's sha256, the ledger exists, both entries built the C3 hash, the plans read 5/0/0 and 1/1/0 with clean re-plans, eight probes by label, the forward returned the reply untouched, the simulations, the counts equal before and after, no id")
        return True
    import boto3
    lam, iam = boto3.client("lambda", region_name="us-east-1"), boto3.client("iam")
    if cid == "DBC189-2-AC1":
        cot_cfg = lam.get_function_configuration(FunctionName=COT_FN)
        read_cfg = lam.get_function_configuration(FunctionName=READ_FN)
        names = iam.list_role_policies(RoleName=READ_ROLE)["PolicyNames"]
        docs = {n: iam.get_role_policy(RoleName=READ_ROLE, PolicyName=n)["PolicyDocument"] for n in names}
        fwd = docs.get(FORWARD_POLICY, {})
        check_live_functions(cot_cfg, read_cfg, docs, fwd, iam.list_role_policies(RoleName=COT_ROLE)["PolicyNames"], c3)
        print("OK: live: the new function and the 49 Financial function run the bundle's code hash with the recorded environment keys, the new role is -cot-, the 49 Financial role holds its three old policies byte-identical plus the one forward statement")
        return True
    if cid == "DBC189-3-AC1":
        s3, apigw = boto3.client("s3"), boto3.client("apigatewayv2", region_name="us-east-1")
        bucket_doc = json.loads(s3.get_bucket_policy(Bucket=BUCKET)["Policy"])
        n = 0
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX, Delimiter="/"):
            n += len(page.get("CommonPrefixes", []))
        routes, token = [], None
        while True:
            r = apigw.get_routes(ApiId=API_ID, **({"NextToken": token} if token else {}))
            routes += r["Items"]
            token = r.get("NextToken")
            if not token:
                break
        integ = {i["IntegrationId"]: i.get("IntegrationUri", "") for i in apigw.get_integrations(ApiId=API_ID, MaxResults="500")["Items"]}
        check_live_world(rec, bucket_doc, n, routes, integ)
        print("OK: live: the Cottonwood bucket policy equals the record's, the platinum prefix count is %d, the three Performance routes still share one integration that invokes the 49 Financial function, and nothing routes to the new function" % n)
        return True
    raise Fail("unknown criterion %s" % cid)


def synthetic():
    h = "A" * 43 + "="
    pr = lambda lab, st, rc, size, enc=None: {"label": lab, "method": "lambda-invoke", "status": st, "reason_code": rc, "content_encoding": enc, "size_bytes": size, "invoked_utc": "2026-10-17T06:00:00Z", "request_id": "r-" + lab}  # noqa: E731
    probes = [pr("cot-direct-manifest", 200, None, 900), pr("cot-direct-series", 200, None, 150000, "gzip"), pr("cot-direct-forged", 200, "NOT_AUTHORIZED", 120), pr("control-49f-manifest", 200, None, 800),
              pr("cot-via-49f-manifest", 200, None, 900), pr("cot-via-49f-series", 200, None, 150000, "gzip"), pr("inflection-via-49f", 200, "FIRM_BINDING", 120), pr("noninternal-cot-via-49f", 200, "FIRM_BINDING", 120)]
    pol = sorted(list(OLD_POLICIES) + [FORWARD_POLICY])
    rec = {"claim": "measured", "gates": {"packet_sha256": "p" * 64, "coo_half_signed": True, "cto_half_signed": True, "one_change_at_a_time": {"worktrees_read": 9, "open_markers_naming_this_surface": 0}, "live_matches_packet": True},
           "ledger_entry": LEDGER_SLUG, "applier": APPLIER,
           "before": {"cot_function_exists": False, "cot_role_exists": False, "cot_artifact_exists": False, "read_artifact_version_id": ROLLBACK_VERSION, "read_code_sha256": READ_CODE_BEFORE, "prefixes": PREFIXES, "objects": 1900, "versions": 1950,
                      "bucket_policy_sha256": "b" * 64, "bucket_policy_statements": BUCKET_STATEMENTS},
           "build": {"cot_entry_sha256_b64": h, "read_entry_sha256_b64": h, "members": 32},
           "plans": {"iso": {"add": 5, "change": 0, "destroy": 0, "replan_no_changes": True}, "read": {"add": 1, "change": 1, "destroy": 0, "replan_no_changes": True}},
           "probes": probes, "probe_identity_class": "OPAL_GLOBAL", "simulate": {"invoke_new_function": "allowed", "invoke_other_function": "implicitDeny", "s3_get_cottonwood_platinum": "implicitDeny"},
           "after": {"cot_function": {"code_sha256": h, "memory_mb": 512, "timeout_s": 29, "env_keys": COT_ENV, "role": COT_ROLE}, "read_function": {"code_sha256": h, "env_keys": READ_ENV_AFTER, "forward_value": COT_FN},
                     "read_role_policies": pol, "bucket_policy_sha256": "b" * 64, "prefixes": PREFIXES, "objects": 1900, "versions": 1950},
           "ledger_closed": False, "reads": {"vendor_calls": 0, "secret_reads": 0}, "notes": "Counts, hashes and statuses only; no body, id or name was written."}
    return rec, h


def selftest():
    rec, h = synthetic()
    coo, cto = "SIGNED " + "p" * 64, "SIGNED " + "p" * 12

    def go(r, **kw):
        return check_record(r, kw.get("sha", "p" * 64), kw.get("coo", coo), kw.get("cto", cto), kw.get("led", True), kw.get("h", h))
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

    def mut(label, fn, **kw):
        r = copy.deepcopy(rec)
        fn(r)
        red(lambda: go(r, **kw), label)
    red(lambda: go(rec, sha="q" * 64), "packet sha differs")
    red(lambda: go(rec, coo="DRAFT"), "coo unsigned")
    red(lambda: go(rec, cto="SIGNED"), "cto not bound")
    red(lambda: go(rec, led=False), "ledger missing")
    red(lambda: go(rec, h="B" * 43 + "="), "build hash differs from C3")
    mut("claim", lambda r: r.update(claim="inferred"))
    mut("identity class", lambda r: r.update(probe_identity_class="FIRM_ADVISOR"))
    mut("applier", lambda r: r.update(applier="x"))
    mut("function pre-exists", lambda r: r["before"].update(cot_function_exists=True))
    mut("rollback version", lambda r: r["before"].update(read_artifact_version_id="x"))
    mut("prefixes before", lambda r: r["before"].update(prefixes=938))
    mut("build entries differ", lambda r: r["build"].update(read_entry_sha256_b64="C" * 43 + "="))
    mut("iso plan", lambda r: r["plans"]["iso"].update(add=4))
    mut("read plan change", lambda r: r["plans"]["read"].update(change=0))
    mut("destroy", lambda r: r["plans"]["read"].update(destroy=1))
    mut("replan", lambda r: r["plans"]["iso"].update(replan_no_changes=False))
    mut("label order", lambda r: r["probes"].reverse())
    mut("control refused", lambda r: r["probes"][3].update(reason_code="FIRM_BINDING"))
    mut("direct not served", lambda r: r["probes"][0].update(status=500))
    mut("forged served", lambda r: r["probes"][2].update(reason_code=None))
    mut("inflection token", lambda r: r["probes"][6].update(reason_code="NOT_READY"))
    mut("forward altered the reply", lambda r: r["probes"][4].update(size_bytes=901))
    mut("series not gzip", lambda r: (r["probes"][1].update(content_encoding=None), r["probes"][5].update(content_encoding=None)))
    mut("reason sentence", lambda r: r["probes"][6].update(reason_code="the firm is refused"))
    mut("forged as big as manifest", lambda r: r["probes"][2].update(size_bytes=900))
    mut("simulate", lambda r: r["simulate"].update(s3_get_cottonwood_platinum="allowed"))
    mut("cot env", lambda r: r["after"]["cot_function"].update(env_keys=COT_ENV + ["IRPT_FORWARD_COTTONWOOD_FUNCTION"]))
    mut("cot role", lambda r: r["after"]["cot_function"].update(role="irpt-49f-reporting-read-role"))
    mut("read env", lambda r: r["after"]["read_function"].update(env_keys=READ_ENV_BEFORE))
    mut("policies", lambda r: r["after"].update(read_role_policies=sorted(OLD_POLICIES)))
    mut("bucket policy moved", lambda r: r["after"].update(bucket_policy_sha256="c" * 64))
    mut("objects moved", lambda r: r["after"].update(objects=1901))
    mut("ledger closed by the applier", lambda r: r.update(ledger_closed=True))
    mut("reads", lambda r: r.update(reads={"vendor_calls": 1, "secret_reads": 0}))
    mut("extra key", lambda r: r.update(z=1))
    cot_cfg = {"CodeSha256": h, "MemorySize": 512, "Timeout": 29, "Handler": "entry.lambda_handler", "Role": "arn:aws:iam::1:role/" + COT_ROLE, "Environment": {"Variables": {k: "x" for k in COT_ENV}}}
    read_cfg = {"CodeSha256": h, "MemorySize": 512, "Timeout": 29, "Environment": {"Variables": dict({k: "x" for k in READ_ENV_BEFORE}, IRPT_FORWARD_COTTONWOOD_FUNCTION=COT_FN)}}
    fwd = {"Statement": [{"Sid": "InvokeTheCottonwoodReadFunctionOnly", "Effect": "Allow", "Action": ["lambda:InvokeFunction"], "Resource": ["arn:aws:lambda:us-east-1:1:function:" + COT_FN]}]}
    docs = {name: {"fixture": name} for name in OLD_POLICIES}
    saved = dict(OLD_POLICIES)
    OLD_POLICIES.update({name: canon(docs[name])[:16] for name in docs})
    try:
        docs[FORWARD_POLICY] = fwd

        def live(**kw):
            return check_live_functions(kw.get("cot", cot_cfg), kw.get("read", read_cfg), kw.get("docs", docs), kw.get("fwd", fwd), kw.get("names", COT_POLICIES), h)
        assert live()
        red(lambda: live(cot=dict(cot_cfg, MemorySize=1024)), "live memory")
        red(lambda: live(cot=dict(cot_cfg, Role="arn:aws:iam::1:role/other-role")), "live role")
        red(lambda: live(cot=dict(cot_cfg, Environment={"Variables": {k: "x" for k in COT_ENV + ["IRPT_FORWARD_COTTONWOOD_FUNCTION"]}})), "live forward on target")
        red(lambda: live(read=dict(read_cfg, CodeSha256="z=")), "live read code")
        red(lambda: live(read=dict(read_cfg, Environment={"Variables": {k: "x" for k in READ_ENV_BEFORE}})), "live read env")
        red(lambda: live(docs=dict(docs, **{next(iter(OLD_POLICIES)): {"fixture": "changed"}})), "live old policy moved")
        red(lambda: live(fwd={"Statement": fwd["Statement"] + fwd["Statement"]}), "two forward statements")
        red(lambda: live(fwd={"Statement": [dict(fwd["Statement"][0], Action=["lambda:*"])]}), "forward action")
        red(lambda: live(fwd={"Statement": [dict(fwd["Statement"][0], Resource=["*"])]}), "forward resource")
        red(lambda: live(names=COT_POLICIES[:1]), "cot policies")
    finally:
        OLD_POLICIES.clear()
        OLD_POLICIES.update(saved)
    bucket = {"Statement": [{"i": i} for i in range(BUCKET_STATEMENTS)]}
    r2 = copy.deepcopy(rec)
    r2["after"]["bucket_policy_sha256"] = canon(bucket)
    routes = [{"RouteKey": "GET /api/scoped/investor-reporting/reporting/{a}/{b}", "Target": "integrations/i1"}] * 3
    integ = {"i1": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:1:function:%s/invocations" % READ_FN}
    assert check_live_world(r2, bucket, PREFIXES, routes, integ)
    red(lambda: check_live_world(r2, {"Statement": bucket["Statement"][:-1]}, PREFIXES, routes, integ), "bucket policy statements")
    red(lambda: check_live_world(r2, bucket, PREFIXES - 1, routes, integ), "prefix count")
    red(lambda: check_live_world(r2, bucket, PREFIXES, routes[:2], integ), "route lost")
    red(lambda: check_live_world(r2, bucket, PREFIXES, routes[:2] + [dict(routes[0], Target="integrations/i2")], dict(integ, i2=integ["i1"])), "two integrations")
    red(lambda: check_live_world(r2, bucket, PREFIXES, routes, {"i1": integ["i1"].replace(READ_FN, COT_FN)}), "routes to the new function")
    red(lambda: check_live_world(r2, bucket, PREFIXES, routes, dict(integ, i9=integ["i1"].replace(READ_FN, COT_FN))), "a new integration to the new function")
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
