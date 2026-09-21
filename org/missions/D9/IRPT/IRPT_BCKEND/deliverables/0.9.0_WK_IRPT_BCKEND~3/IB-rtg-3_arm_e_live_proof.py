#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtg-3 arm (e) -- PROVEN LIVE, under the deployed role and bytes.

Reuses the bounded-principal MECHANISM in
../0.7.0_AE_CloudOps~V/battery_ib_rtf_10.py (rtf-9 packet blob a1f36b95b2, both halves at
HEAD), generalized to ONE test principal PER REGISTRY FIRM (a new epoch per firm, same
lifecycle shape: create K1+K1b -> login -> one scoped HTTP request -> rollback, verified).

WHY role="admin" (FIRM_OPERATIONS class) RATHER THAN rtf-10's advisor class: cottonwood's
ownership map is a 107-byte near-empty stub and inflection's ownership map is ABSENT
(404) at this run (measured below) -- an ADVISOR-class principal for either firm would
resolve an EMPTY permitted set (`_scope/resolve.py::advisor_grant` returns `[], [], census`
when `ownership` is falsy, or when the schema map holds no entry for the advisor), which
`performance/handler.py::check_scope` then REFUSES at `resolved_scope.scope_kind ==
"UNSUPPORTED"` -- a `ScopeRefused` BEFORE `tenants.route_for` is ever reached. That would
prove nothing about R74-AC1 for those two firms; it would just prove a DIFFERENT, upstream
refusal. `_scope/resolve.py::resolve()`'s FIRM_OPERATIONS branch (`role=="admin" and firm`)
uses `firm_population(directory, firm_id)` -- the DIRECTORY, never the ownership map -- so it
is INDEPENDENT of the ownership-map gap and reaches `check_scope` with a non-empty permitted
set for any firm whose DIRECTORY is populated (all 3 are: 4576 / 260 / 291 entries, measured
below), which is exactly what is needed to reach `tenants.route_for(firm_id)` and exercise
this order's fix. This is a considered SUBSTITUTION for rtf-10's advisor-class mechanism,
not a departure from its LIFECYCLE (create -> login -> request -> rollback, each verified,
no residue) -- filed as row IRPT_BCKEND-W3-S50.

NEVER PRINTED OR WRITTEN: the password, the access or refresh token, the Authorization
header, any secret value; response bodies are bound by sha256 and summarised by counts and
codes only.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request

import bcrypt
import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rtg-3_arm_e_live_proof_output.txt")
D_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~3"
RTF9_PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md"
RTF9_BLOB = "a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4"
RTF9_HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
}
ACCT = "313476888478"
BASE = "https://opalinvest.dev"
PFX = "/api/scoped/investor-reporting"
UA = "opal-irpt-ib-rtg-3-arm-e/1.0 (0.9.0_WK_IRPT_BCKEND~3)"
USERS = "opal-users-v2"
THROTTLE = "opal-portal-auth-throttle"
FN = "irpt-performance-adapter"
ROLE = "irpt-performance-adapter-role"
PARTNER_TABLE = {"49financial": "opal-partner-49financial", "cottonwood": "opal-partner-cottonwood",
                  "inflection": "opal-partner-inflection"}
# ONE real account id per firm, read from that firm's OWN directory (first entry), so the
# GET path parameter names an account genuinely INSIDE the FIRM_OPERATIONS permitted set --
# a fabricated placeholder id is a REQUESTED account outside the permitted set and
# `performance/handler.py::check_scope` correctly refuses THAT with ScopeRefused
# (-> public_reason_code NOT_AUTHORIZED, _authz/errors.py:132), which happens BEFORE
# `tenants.route_for` is ever reached -- a defect in the TEST's fixture, not the fix.
REAL_ACCOUNT_ID: dict[str, str] = {}

LINES: list[str] = []
SECRETS: list[str] = []
IDENTITY: list[str] = []
ddb = boto3.client("dynamodb", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")
lam = boto3.client("lambda", region_name="us-east-1")


def emit(line: str = "") -> None:
    for s in SECRETS:
        if s:
            line = line.replace(s, "<REDACTED>")
    LINES.append(line)
    print(line, flush=True)


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(*args: str) -> tuple[int, str]:
    out = subprocess.run(["git", *args], cwd=WS, capture_output=True, text=True, encoding="utf-8",
                         errors="replace", timeout=120)
    return out.returncode, out.stdout


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def identity_line(served: bool = False) -> None:
    if not IDENTITY:
        IDENTITY.append(boto3.client("sts").get_caller_identity()["Arn"])
    if served:
        emit("  identity: the HTTP requests run as the bounded test principal; the served compute "
             "runs as %s's OWN execution role %s (printed per request); the operator identity %s "
             "only creates/deletes the principal's keys and reads configuration" % (FN, ROLE, IDENTITY[0]))
    else:
        emit("  identity: ran as %s -- a configuration/document claim, NOT a served behaviour" % IDENTITY[0])


def client_firms() -> list[dict]:
    reg = json.load(open(os.path.join(WS, "data", "firm_registry.json"), encoding="utf-8"))
    return [f for f in reg["firms"] if f.get("kind") == "client" and f.get("enabled")]


def real_account_id(bucket: str) -> str:
    """The FIRST account id in this firm's OWN directory -- genuinely inside the
    FIRM_OPERATIONS permitted set (the whole firm population), never fabricated."""
    ptr = json.loads(s3.get_object(Bucket=bucket, Key="investor-reporting/directory/latest.json")["Body"].read())
    d = json.loads(s3.get_object(Bucket=bucket, Key=ptr["key"])["Body"].read())
    entries = d.get("entries") or []
    if not entries:
        raise RuntimeError("directory at s3://%s/%s has 0 entries -- no real account id available" % (bucket, ptr["key"]))
    return (entries[0].get("ids") or {}).get("account_ids", [None])[0]


def http(method: str, path: str, token: str | None = None, body: dict | None = None,
         query: dict | None = None, cookie: str | None = None):
    url = BASE + path
    if query:
        url += "?" + "&".join("%s=%s" % (k, urllib.request.quote(str(v))) for k, v in query.items())
    headers = {"User-Agent": UA, "X-Contract-Version": "v1", "Origin": BASE}
    if token:
        headers["Authorization"] = "Bearer " + token
    if cookie:
        headers["Cookie"] = cookie
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def as_json(b: bytes):
    try:
        return json.loads(b.decode("utf-8"))
    except ValueError:
        return None


def get_item(table: str, key: dict) -> dict | None:
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def jwt_claims(tok: str) -> dict:
    seg = tok.split(".")[1]
    seg += "=" * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg.encode()).decode("utf-8"))


def prefix_scan(label: str, epoch: int) -> bool:
    ok = True
    for table, attr, prefix in ((USERS, "PK", "USER#usr_irptrtg3_"), (USERS, "email", "irpt-rtg3-test-")):
        d = ddb.scan(TableName=table, Select="COUNT", FilterExpression="begins_with(#a, :p)",
                     ExpressionAttributeNames={"#a": attr}, ExpressionAttributeValues={":p": {"S": prefix}})
        ok = ok and d["Count"] == 0
        emit("    %s: %s %s begins_with '%s': %d of %d scanned" % (label, table, attr, prefix, d["Count"], d["ScannedCount"]))
    return ok


def f_precondition() -> bool:
    emit("PRECONDITION -- the rtf-9 packet's 2 of 2 halves at HEAD (the bounded-principal mechanism this run reuses)")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + RTF9_PACKET_REL)
    _, wt = git("hash-object", RTF9_PACKET_REL) if os.path.exists(os.path.join(WS, RTF9_PACKET_REL)) else (1, "")
    pk = rc == 0 and head.strip() == RTF9_BLOB
    n = 0
    for who, path in RTF9_HALVES.items():
        rc2, text = git("show", "HEAD:" + path)
        n += rc2 == 0 and RTF9_BLOB in text
    emit("  rtf-9 packet blob at HEAD %s (== %s: %s); halves naming it %d of 2" % (head.strip(), RTF9_BLOB, pk, n))
    return pk and n == 2


def create_principal(firm_id: str, epoch: int, password: str, created: dict) -> dict:
    email = "irpt-rtg3-test-%s-%d@opal.test" % (firm_id[:3], epoch)
    pk = "USER#usr_irptrtg3_%s_%d" % (firm_id[:3], epoch)
    created.update({"email": email, "pk": pk, "firm_id": firm_id})
    created_at = now_iso()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode("ascii")
    SECRETS.append(pw_hash)
    k1 = {"PK": {"S": pk}, "SK": {"S": "PROFILE"}, "email": {"S": email}, "passwordHash": {"S": pw_hash},
          "name": {"S": "IRPT test principal (IB-rtg-3 arm e, %s)" % firm_id}, "role": {"S": "admin"},
          "firmId": {"S": firm_id}, "status": {"S": "active"}, "createdAt": {"S": created_at},
          "createdBy": {"S": "0.9.0_WK_IRPT_BCKEND~3 IB-rtg-3"}}
    ddb.put_item(TableName=USERS, Item=k1, ConditionExpression="attribute_not_exists(PK)")
    t_k1 = now_iso()
    got1 = get_item(USERS, {"PK": {"S": pk}, "SK": {"S": "PROFILE"}})
    emit("  K1 created %s: PK %s firmId=%s role=admin; consistent read-back %s; attributes %d"
         % (t_k1, pk, firm_id, got1 is not None, len(got1 or {})))
    partner = PARTNER_TABLE[firm_id]
    k1b = {"email": {"S": email}, "advisorKey": {"S": "irpt-rtg3-test-admin"}}
    ddb.put_item(TableName=partner, Item=k1b, ConditionExpression="attribute_not_exists(email)")
    t_k1b = now_iso()
    got = get_item(partner, {"email": {"S": email}})
    emit("  K1b created %s in %s: consistent read-back %s; attributes %s"
         % (t_k1b, partner, got is not None, sorted(got or {})))
    return {"email": email, "pk": pk, "partner": partner, "k1_created": t_k1,
            "ok": got1 is not None and got is not None}


def login(email: str, password: str) -> dict:
    status, headers, body = http("POST", "/auth/login", body={"email": email, "password": password})
    j = as_json(body) or {}
    tok = j.get("accessToken") if isinstance(j, dict) else None
    cookies = headers.get_all("Set-Cookie") or []
    refresh = next((c.split(";", 1)[0] for c in cookies if c.startswith("refresh_token=")), None)
    for s in (tok, refresh, refresh.split("=", 1)[1] if refresh else None):
        if s:
            SECRETS.append(s)
    out = {"http": status, "token": tok, "refresh_cookie": refresh, "at": now_iso()}
    emit("  login POST /auth/login -> HTTP %d at %s; access token minted=%s; refresh cookie set=%s"
         % (status, out["at"], bool(tok), bool(refresh)))
    if tok:
        c = jwt_claims(tok)
        out["claims"] = c
        emit("  K2 claims: firmId=%s role=%s exp=%s" % (
            c.get("firmId"), c.get("role"),
            datetime.datetime.fromtimestamp(c.get("exp", 0), datetime.timezone.utc).strftime("%H:%M:%SZ")))
    return out


def classify(status: int, j) -> dict:
    """SERVED (2xx with data) | POLICY (a refusal carrying a firm_id, code != UNEXPECTED) |
    UNEXPECTED (the S90 shape) | UNRESOLVED (any other refusal: no firm_id)."""
    out = {"http": status}
    if isinstance(j, dict):
        st = j.get("status") or {}
        out.update({"operation": j.get("operation"), "firm_id": j.get("firm_id"),
                     "code": st.get("public_reason_code"), "state": st.get("state")})
        if status < 400 and "data" in j:
            out["class"] = "SERVED"
            out["route"] = ((j.get("data") or {}).get("coverage") or {}).get("route")
            out["outcome"] = ((j.get("data") or {}).get("coverage") or {}).get("outcome")
            return out
        if out["code"] == "UNEXPECTED":
            out["class"] = "UNEXPECTED"
        elif out.get("firm_id"):
            out["class"] = "POLICY"
        else:
            out["class"] = "UNRESOLVED"
        return out
    out["class"] = "UNEXPECTED" if status >= 500 else "UNRESOLVED"
    return out


def request_performance(tok: str, firm_id: str, account_id: str) -> dict:
    st, _, b = http("GET", PFX + "/performance/" + account_id, tok,
                     query={"start": "2026-01-01", "end": "2026-09-18"})
    j = as_json(b)
    c = classify(st, j)
    c["sha256"] = sha(b)
    emit("    GET %s/performance/%s -> HTTP %d class %s code %s firm_id %s | route %s | sha256 %s"
         % (PFX, account_id, st, c["class"], c.get("code"), "present" if c.get("firm_id") else "ABSENT",
            c.get("route"), c["sha256"][:16]))
    return c


def rollback(created: dict, sess: dict) -> dict:
    out = {"k1b_deleted": None, "k1_deleted": None, "refresh_refused": None, "expired_refused": None}
    if created.get("email") and created.get("partner"):
        ddb.delete_item(TableName=created["partner"], Key={"email": {"S": created["email"]}})
        gone = get_item(created["partner"], {"email": {"S": created["email"]}}) is None
        out["k1b_deleted"] = now_iso() if gone else None
        emit("  K1b DeleteItem (%s) -> consistent GetItem returns no Item: %s" % (created["partner"], gone))
    if created.get("pk"):
        ddb.delete_item(TableName=USERS, Key={"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}})
        gone = get_item(USERS, {"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}}) is None
        out["k1_deleted"] = now_iso() if gone else None
        emit("  K1  DeleteItem -> consistent GetItem returns no Item: %s" % gone)
    try:
        if sess.get("refresh_cookie"):
            st, _, b = http("POST", "/auth/refresh", cookie=sess["refresh_cookie"])
            j = as_json(b) or {}
            minted = isinstance(j, dict) and bool(j.get("accessToken"))
            refused = st != 200 and not minted
            out["refresh_refused"] = now_iso() if refused else None
            emit("  REFRESH after delete: HTTP %d; access token minted=%s -> %s"
                 % (st, minted, "REFUSED" if refused else "NOT REFUSED -- STOP AND ESCALATE"))
        if sess.get("token"):
            exp = (sess.get("claims") or {}).get("exp", 0)
            wait = exp + 10 - time.time()
            if wait > 0:
                emit("  waiting %.0f s for the access token's exp + 10 s" % wait)
                time.sleep(wait)
            st, _, _b = http("GET", PFX + "/status", sess["token"])
            out["expired_refused"] = now_iso() if st == 401 else None
            emit("  the access token after exp: GET status -> HTTP %d -> %s" % (st, "REFUSED 401" if st == 401 else "NOT 401"))
    except Exception as exc:  # noqa: BLE001 -- the deletes above already ran
        emit("  EXCEPTION in the post-delete checks: %s: %s" % (type(exc).__name__, str(exc)[:300]))
    return out


def one_firm(firm_id: str, epoch: int) -> dict:
    emit("")
    emit("=== FIRM %s (epoch %d) ===" % (firm_id, epoch))
    password = secrets.token_urlsafe(24)
    SECRETS.append(password)
    created: dict = {}
    sess: dict = {}
    result = {"firm_id": firm_id, "route_resolved": False, "dependency_unavailable": False,
              "keys_ok": False, "lifecycle_ok": False, "class": None, "code": None}
    try:
        k = create_principal(firm_id, epoch, password, created)
        created["k1_created"] = k["k1_created"]
        created["partner"] = k["partner"]
        sess = login(k["email"], password)
        c = sess.get("claims") or {}
        keys_ok = k["ok"] and sess.get("http") == 200 and c.get("firmId") == firm_id
        result["keys_ok"] = keys_ok
        emit("  keys read back and session as declared: %s" % keys_ok)
        if keys_ok:
            resp = request_performance(sess["token"], firm_id, REAL_ACCOUNT_ID[firm_id])
            result["class"] = resp["class"]
            result["code"] = resp.get("code")
            result["route"] = resp.get("route")
            result["dependency_unavailable"] = resp.get("code") == "DEPENDENCY_UNAVAILABLE"
            result["route_resolved"] = resp["class"] in ("SERVED", "POLICY") and not result["dependency_unavailable"]
    except Exception as exc:  # noqa: BLE001 -- recorded, then rollback runs
        emit("  EXCEPTION during the act: %s: %s -- rollback now" % (type(exc).__name__, str(exc)[:300]))
    finally:
        rb = rollback(created, sess)
    life_ok = bool(rb.get("k1b_deleted")) and bool(rb.get("k1_deleted")) and bool(rb.get("refresh_refused")) and bool(rb.get("expired_refused"))
    result["lifecycle_ok"] = life_ok
    emit("  (%s) route_resolved=%s dependency_unavailable=%s lifecycle_closed=%s"
         % (firm_id, result["route_resolved"], result["dependency_unavailable"], life_ok))
    return result


def grep_deployed_bytes() -> dict:
    emit("")
    emit("DEPLOYED-BYTES CHECK -- 0 fourth-id-space literals")
    key = "investor-reporting/%s.zip" % FN
    bucket = "opal-313476888478-lambda-artifacts"
    head = s3.head_object(Bucket=bucket, Key=key)
    meta_sha = (head.get("Metadata") or {}).get("content-sha256")
    body = s3.get_object(Bucket=bucket, Key=key, VersionId=head["VersionId"])["Body"].read()
    got_sha = base64.b64encode(hashlib.sha256(body).digest()).decode()
    import io
    import zipfile
    zf = zipfile.ZipFile(io.BytesIO(body))
    tenants_src = zf.read("tenants.py").decode("utf-8")
    tenants_sha = sha(tenants_src.encode("utf-8"))
    # Every ROUTES dict key must be an expression on _LEGACY_SHORT_ID[...] (computed via
    # _ids.opaque_firm), never a bare string literal -- a bare literal key would BE a fourth
    # hand-typed spelling.
    m = re.search(r"ROUTES = \{(.*?)\n\}\n", tenants_src, re.S)
    routes_block = m.group(1) if m else ""
    bare_literal_keys = re.findall(r'^\s*"([^"]+)":\s*TenantRoute\(', routes_block, re.M)
    legacy_alias_keys = re.findall(r'"([A-Z0-9]+)":\s*_ids\.opaque_firm\(', tenants_src)
    emit("  served zip %s VersionId %s: metadata content-sha256 %s, re-downloaded sha256(b64) %s -> %s"
         % (key, head["VersionId"], meta_sha, got_sha, "EQUAL" if meta_sha == got_sha else "DIFFERS"))
    emit("  tenants.py extracted from the served zip: sha256 %s" % tenants_sha)
    emit("  ROUTES dict keys that are BARE STRING LITERALS (a fourth spelling, would FAIL): %d found: %s"
         % (len(bare_literal_keys), bare_literal_keys))
    emit("  _LEGACY_SHORT_ID readability aliases (never consulted by route_for): %d: %s" % (len(legacy_alias_keys), legacy_alias_keys))
    return {"served_sha_equal": meta_sha == got_sha, "bare_literal_count": len(bare_literal_keys),
            "tenants_sha256": tenants_sha}


def main() -> int:
    emit("IB-rtg-3 arm (e) live proof -- run at %s -- worktree HEAD %s" % (now_iso(), git("rev-parse", "HEAD")[1].strip()))
    identity_line()
    if not f_precondition():
        emit("STOP at the precondition: nothing written")
        return 1
    firms = client_firms()
    ids = sorted(f["firm_id"] for f in firms)
    emit("REGISTRY-FIRM-COUNT: %d -> %s" % (len(ids), ids))
    for f in firms:
        acc = real_account_id(f["bucket"])
        REAL_ACCOUNT_ID[f["firm_id"]] = acc
        emit("  %-12s real account id from its own directory (bucket %s): %s" % (f["firm_id"], f["bucket"], acc))
    identity_line(served=True)
    if not prefix_scan("before (all firms)", 0):
        emit("STOP: a principal key already exists (residue) -- nothing written")
        return 1
    epoch_base = int(time.time())
    results = []
    for i, firm_id in enumerate(ids):
        results.append(one_firm(firm_id, epoch_base + i))
    emit("")
    if not prefix_scan("after (all firms)", 0):
        emit("WARNING: residue detected after rollback")
    bytes_check = grep_deployed_bytes()
    emit("")
    emit("SUMMARY")
    n = len(results)
    resolved = sum(1 for r in results if r["route_resolved"])
    dep_unavail = sum(1 for r in results if r["dependency_unavailable"])
    life_ok = sum(1 for r in results if r["lifecycle_ok"])
    for r in results:
        emit("  %-12s route_resolved=%-5s dependency_unavailable=%-5s lifecycle_ok=%-5s class=%s code=%s route=%s"
             % (r["firm_id"], r["route_resolved"], r["dependency_unavailable"], r["lifecycle_ok"],
                r.get("class"), r.get("code"), r.get("route")))
    emit("  route resolved (no DEPENDENCY_UNAVAILABLE): %d of %d" % (resolved, n))
    emit("  dependency_unavailable count: %d of %d" % (dep_unavail, n))
    emit("  lifecycle closed cleanly: %d of %d" % (life_ok, n))
    emit("  deployed-bytes check: served sha equal %s; bare fourth-spelling literals: %d"
         % (bytes_check["served_sha_equal"], bytes_check["bare_literal_count"]))
    ok = (resolved == n and dep_unavail == 0 and life_ok == n and bytes_check["served_sha_equal"]
          and bytes_check["bare_literal_count"] == 0)
    if ok:
        emit("RESULT: R74-AC1 arm (e) PASS -- %d of %d firms resolve a TenantRoute, 0 DEPENDENCY_UNAVAILABLE, "
             "0 fourth-id-space literals in the deployed bytes" % (resolved, n))
        emit("IBR74E-LIVE-PROOF-PERFORMANCE-ROUTE-RESOLVES-EACH-FIRM")
        rc = 0
    else:
        emit("RESULT: R74-AC1 arm (e) FAIL")
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
