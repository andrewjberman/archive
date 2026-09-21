#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtg-2 battery -- the status loader reads the real job store. Cell IB-rtg-2
(round 7, the recut on the round-6 analysis @fa2ff4f0dd). SECOND PASS: arms (d) (apply, already
performed by this worker) and (e) (proven live) -- this script re-verifies (d)'s served state and
then performs (e), the live proof under the deployed role and bytes.

  (a) PACKET at HEAD: blob == the signed blob, both never-widen halves at HEAD naming it.
  (b) K-CODE, POST-APPLY: the built artifact still latest at rest == the built sha; the function
      NOW serves that sha; a fresh plan on the ops root reads 0-diff.
  (c) PRECONDITION for the live proof: the rtf-9 two-key-test-principal packet (blob a1f36b95b2),
      both halves at HEAD, reused per this order's arm (e) instruction; this order's OWN
      live-principal ledger committed OPEN at HEAD.
  (d) THE LIVE PROOF, under the deployed role irpt-status-role: create the bounded test principal
      (K1/K1b, a NEW epoch), log in, then exercise the three routes `irpt-status` serves through
      real HTTP requests -- printing route, function and execution role per request -- and confirm
      NEVER `UNSUPPORTED_OPERATION`/`NoSuchOperation` (the round-6 defect): a job naming no job id
      (status-summary) and a job naming one that was never claimed (status-job, the negative
      control; also analysis-report for coverage of the third route) each resolve to the
      DECLARED `NOT_FOUND` code (KeyError -> NOT_FOUND, `_authz/errors.py:136`), never the
      residual. Then the full rollback: K1b and K1 deleted and verified, the refresh cookie
      refused, the access token refused 401 after exp, no residue (prefix scan before/after).

NEVER PRINTED OR WRITTEN: the password, the access or refresh token, the Authorization header, any
secret value; response bodies are bound by sha256 and summarised by counts and codes only. The
token prints only when every arm holds.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import os
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
OUTPUT_PATH = os.path.join(HERE, "IB-rtg-2_R73-AC1_battery_output.txt")
TOKEN = "IBR73-STATUS-LOADER-SERVES-ENVELOPE"
D_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~2"
PACKET_REL = D_REL + "/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-2.md"
PACKET_BLOB = "26360553eb7a66af4ea7c68d93f14e206e03ef60"
COO_HALF_REL = "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtg-2_STATUS_LOADER.md"
CTO_HALF_REL = "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtg-2_20260920.md"
BUILT_SHA = "B0AmyfRKxd4uMhcfoklf3cCpPtnDQUBpLsUBADeDcQ0="
PRIOR_LIVE_SHA = "O3TyGqfqjiwZP9OSXmryonnAst+SbYMLzyuSGphOyCE="
KCODE_FN = "irpt-status"
ARTIFACT_BUCKET = "opal-313476888478-lambda-artifacts"
TF = os.path.join(WS, ".tools", "terraform.exe")
OPS_ROOT = os.path.join(WS, "infra", "aws", "terraform", "investor-reporting", "ops")
PLAN_DIR = os.path.join(WS, ".scratch", "plans_battery_rtg2")

# rtf-9's bounded test principal packet, REUSED per this order's arm (e) instruction verbatim.
RTF9_PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md"
RTF9_BLOB = "a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4"
RTF9_HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
}
PRINCIPAL_SENTINEL_REL = "org/critical_paths/.open_deploys/irpt-status-ib-rtg-2-live-principal.json"

ACCT = "313476888478"
USERS, PARTNER, THROTTLE = "opal-users-v2", "opal-partner-49financial", "opal-portal-auth-throttle"
FIRM, ADVISOR = "49financial", "abby_horton"
OM_BUCKET, OM_KEY = "opal-data-bd", "platinum/49financial/ownership_map.json"
BASE = "https://opalinvest.dev"
PFX = "/api/scoped/investor-reporting"
UA = "opal-irpt-ib-rtg-2-battery/1.0 (0.9.0_WK_IRPT_BCKEND~2)"

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


def identity_line(arm: str, served: bool = False) -> None:
    if not IDENTITY:
        IDENTITY.append(boto3.client("sts").get_caller_identity()["Arn"])
    if served:
        emit("  identity: %s -- the HTTP requests run as the bounded test principal; the served compute runs as each "
             "function's OWN execution role (printed per request); the operator identity %s only creates/deletes the "
             "principal's keys and reads configuration" % (arm, IDENTITY[0]))
    else:
        emit("  identity: %s ran as %s -- a configuration/document claim, NOT a served behaviour" % (arm, IDENTITY[0]))


def half_names_blob(path: str, blob: str) -> bool:
    rc, text = git("show", "HEAD:" + path)
    return rc == 0 and blob in text


def arm_a() -> bool:
    emit("(a) THE IB-rtg-2 PACKET at HEAD, and both never-widen halves naming it")
    identity_line("(a)")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    head = head.strip() if rc == 0 else ""
    _, wt = git("hash-object", PACKET_REL)
    ok = bool(head) and head == wt.strip() == PACKET_BLOB
    emit("  packet %s: blob at HEAD %s, worktree %s, signed %s -> %s" % (
        PACKET_REL, head or "ABSENT", wt.strip(), PACKET_BLOB, "COMMITTED, UNCHANGED" if ok else "NOT THE SIGNED BLOB"))
    coo_ok = half_names_blob(COO_HALF_REL, PACKET_BLOB)
    cto_ok = half_names_blob(CTO_HALF_REL, PACKET_BLOB)
    emit("  COO half %s naming blob %s: %s" % (COO_HALF_REL, PACKET_BLOB, coo_ok))
    emit("  CTO half %s naming blob %s: %s" % (CTO_HALF_REL, PACKET_BLOB, cto_ok))
    return ok and coo_ok and cto_ok


def arm_b() -> bool:
    emit("(b) K-CODE, POST-APPLY -- the built artifact still latest at rest, the served CodeSha256, a fresh 0-diff plan")
    identity_line("(b)")
    key = "investor-reporting/%s.zip" % KCODE_FN
    head = s3.head_object(Bucket=ARTIFACT_BUCKET, Key=key)
    meta = (head.get("Metadata") or {}).get("content-sha256")
    emit("  S3 head-object %s Metadata.content-sha256 = %s -> %s" % (key, meta, "EQUAL to built" if meta == BUILT_SHA else "DIFFERS"))
    live = lam.get_function_configuration(FunctionName=KCODE_FN)["CodeSha256"]
    role = lam.get_function_configuration(FunctionName=KCODE_FN)["Role"]
    emit("  function %s CodeSha256 NOW %s -> %s (Role %s)" % (KCODE_FN, live, "EQUAL to built" if live == BUILT_SHA else "DIFFERS", role))
    os.makedirs(PLAN_DIR, exist_ok=True)
    env = dict(os.environ, TF_IN_AUTOMATION="1", AWS_REGION="us-east-1",
               TF_PLUGIN_CACHE_DIR=os.environ.get("TF_PLUGIN_CACHE_DIR") or os.path.join(WS, ".scratch", "tf-plugin-cache"))
    os.makedirs(env["TF_PLUGIN_CACHE_DIR"], exist_ok=True)
    pf = os.path.join(PLAN_DIR, "ops.tfplan")
    p = subprocess.run([TF, "-chdir=" + OPS_ROOT, "plan", "-input=false", "-no-color", "-out=" + pf],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=600)
    line = next((ln.strip() for ln in p.stdout.splitlines() if ln.startswith("Plan:") or "No changes." in ln), "?")
    zero_diff = p.returncode == 0 and "No changes." in p.stdout
    emit("  fresh ops-root plan (rc %d): %s -> %s" % (p.returncode, line, "0-DIFF" if zero_diff else "NOT 0-DIFF"))
    return meta == BUILT_SHA and live == BUILT_SHA and zero_diff


def arm_c() -> bool:
    emit("(c) PRECONDITION for the live proof -- the rtf-9 packet, its 2 halves, and this order's OWN principal ledger")
    identity_line("(c)")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + RTF9_PACKET_REL)
    head = head.strip() if rc == 0 else ""
    pk = bool(head) and head == RTF9_BLOB
    n = sum(half_names_blob(p, RTF9_BLOB) for p in RTF9_HALVES.values())
    rc3, _ = git("rev-parse", "--verify", "--quiet", "HEAD:" + PRINCIPAL_SENTINEL_REL)
    emit("  rtf-9 packet blob at HEAD %s (== %s: %s); halves naming it %d of 2; this order's principal ledger sentinel at HEAD: %s"
         % (head or "ABSENT", RTF9_BLOB, pk, n, rc3 == 0))
    return pk and n == 2 and rc3 == 0


def get_item(table: str, key: dict) -> dict | None:
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def item_digest(item: dict) -> str:
    return sha(json.dumps({k: v for k, v in item.items() if k != "passwordHash"}, sort_keys=True).encode("utf-8"))


def jwt_claims(tok: str) -> dict:
    seg = tok.split(".")[1]
    seg += "=" * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg.encode()).decode("utf-8"))


def prefix_scan(label: str) -> bool:
    ok = True
    for table, attr, prefix in ((USERS, "PK", "USER#usr_irptrtg2_"), (USERS, "email", "irpt-rtg2-test-"), (PARTNER, "email", "irpt-rtg2-test-")):
        d = ddb.scan(TableName=table, Select="COUNT", FilterExpression="begins_with(#a, :p)",
                     ExpressionAttributeNames={"#a": attr}, ExpressionAttributeValues={":p": {"S": prefix}})
        ok = ok and d["Count"] == 0
        emit("  %s: %s %s begins_with '%s': %d of %d scanned" % (label, table, attr, prefix, d["Count"], d["ScannedCount"]))
    return ok


def create_principal(epoch: int, password: str, created: dict) -> dict:
    email = "irpt-rtg2-test-%d@opal.test" % epoch
    pk = "USER#usr_irptrtg2_%d" % epoch
    created.update({"email": email, "pk": pk})  # BEFORE any write, so the rollback always knows both keys
    created_at = now_iso()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode("ascii")
    SECRETS.append(pw_hash)
    k1 = {"PK": {"S": pk}, "SK": {"S": "PROFILE"}, "email": {"S": email}, "passwordHash": {"S": pw_hash},
          "name": {"S": "IRPT test principal (IB-rtg-2)"}, "role": {"S": "user"}, "firmId": {"S": FIRM},
          "status": {"S": "active"}, "createdAt": {"S": created_at}, "createdBy": {"S": "0.9.0_WK_IRPT_BCKEND~2 IB-rtg-2"}}
    ddb.put_item(TableName=USERS, Item=k1, ConditionExpression="attribute_not_exists(PK)")
    t_k1 = now_iso()
    got1 = get_item(USERS, {"PK": {"S": pk}, "SK": {"S": "PROFILE"}})
    emit("  K1 created %s: PK %s; consistent read-back %s; attributes %d; digest (passwordHash excluded) %s"
         % (t_k1, pk, got1 is not None, len(got1 or {}), item_digest(got1) if got1 else "-"))
    k1b = {"email": {"S": email}, "advisorKey": {"S": ADVISOR}}
    ddb.put_item(TableName=PARTNER, Item=k1b, ConditionExpression="attribute_not_exists(email)")
    t_k1b = now_iso()
    got = get_item(PARTNER, {"email": {"S": email}})
    emit("  K1b created %s in %s: consistent read-back %s; attributes %s; digest %s"
         % (t_k1b, PARTNER, got is not None, sorted(got or {}), item_digest(got) if got else "-"))
    return {"email": email, "pk": pk, "k1_created": t_k1,
            "ok": got1 is not None and sorted(got1) == sorted(k1) and got is not None and sorted(got) == ["advisorKey", "email"]}


def http(method: str, path: str, token: str | None = None, query: dict | None = None):
    url = BASE + path
    if query:
        url += "?" + "&".join("%s=%s" % (k, urllib.request.quote(str(v))) for k, v in query.items())
    headers = {"User-Agent": UA, "X-Contract-Version": "v1", "Origin": BASE}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(url, method=method, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read()


def login(email: str, password: str) -> dict:
    body = json.dumps({"email": email, "password": password}).encode("utf-8")
    req = urllib.request.Request(BASE + "/auth/login", data=body, method="POST",
                                 headers={"User-Agent": UA, "Content-Type": "application/json", "Origin": BASE})
    try:
        r = urllib.request.urlopen(req, timeout=60)
        status, headers, respb = r.status, r.headers, r.read()
    except urllib.error.HTTPError as e:
        status, headers, respb = e.code, e.headers, e.read()
    j = json.loads(respb.decode("utf-8")) if respb else {}
    tok = j.get("accessToken") if isinstance(j, dict) else None
    cookies = headers.get_all("Set-Cookie") or []
    refresh = next((c.split(";", 1)[0] for c in cookies if c.startswith("refresh_token=")), None)
    for s in (tok, refresh, refresh.split("=", 1)[1] if refresh else None):
        if s:
            SECRETS.append(s)
    out = {"http": status, "token": tok, "refresh_cookie": refresh, "at": now_iso()}
    emit("  login POST /auth/login -> HTTP %d at %s; access token minted=%s; refresh cookie set=%s" % (status, out["at"], bool(tok), bool(refresh)))
    if tok:
        c = jwt_claims(tok)
        out["claims"] = c
        emit("  K2 claims: firmId=%s role=%s advisorKey=%s exp=%s" % (
            c.get("firmId"), c.get("role"), c.get("advisorKey"),
            datetime.datetime.fromtimestamp(c.get("exp", 0), datetime.timezone.utc).strftime("%H:%M:%SZ")))
    return out


def classify(status: int, j) -> dict:
    out = {"http": status}
    if isinstance(j, dict):
        st = j.get("status") or {}
        code = st.get("public_reason_code") or j.get("public_reason_code")
        out.update({"code": code, "state": st.get("state")})
        if status < 400 and "data" in j:
            out["class"] = "SERVED"
        elif code in ("UNSUPPORTED_OPERATION",):
            out["class"] = "DEFECT-STILL-PRESENT"
        elif code == "NOT_FOUND":
            out["class"] = "NOT_FOUND"
        elif code == "UNEXPECTED":
            out["class"] = "UNEXPECTED"
        else:
            out["class"] = "OTHER(%s)" % code
        return out
    out["class"] = "UNEXPECTED-NO-BODY" if status >= 500 else "OTHER(no-json)"
    return out


def requests_arm(tok: str) -> bool:
    emit("  REQUESTS -- the three routes irpt-status serves; NEVER UNSUPPORTED_OPERATION")
    rnd = secrets.token_hex(12)
    rows = []

    def go(label: str, method: str, path: str, query=None):
        st, _, b = http(method, PFX + path, tok, query=query)
        try:
            j = json.loads(b.decode("utf-8"))
        except ValueError:
            j = None
        c = classify(st, j)
        c["sha256"] = sha(b)
        c["label"] = label
        rows.append(c)
        emit("    %-46s %-6s %s%s -> function irpt-status (role irpt-status-role): %s http %d code %s state %s | sha256 %s"
             % (label, method, PFX, path, c["class"], st, c.get("code"), c.get("state"), c["sha256"][:16]))
        return j, c

    go("status-summary (GET /status, no job id)", "GET", "/status")
    go("status-job (GET /status/{jobId}, never-claimed job -- negative control)", "GET", "/status/irpt-rtg2-nojob-%s" % rnd)
    go("analysis-report (GET /analysis/{jobId}/sections, never-claimed job)", "GET", "/analysis/irpt-rtg2-nojob-%s/sections" % rnd)
    defect = sum(1 for r in rows if r["class"] == "DEFECT-STILL-PRESENT")
    resolved = sum(1 for r in rows if r["class"] in ("SERVED", "NOT_FOUND"))
    emit("  routes exercised %d of 3; DEFECT-STILL-PRESENT (UNSUPPORTED_OPERATION) %d; resolved (SERVED or NOT_FOUND) %d"
         % (len(rows), defect, resolved))
    return defect == 0 and resolved == len(rows)


def rollback(created: dict, sess: dict) -> dict:
    emit("  ROLLBACK -- K1b FIRST, then K1; each verified by a failing consistent base-table read")
    out = {"k1b_deleted": None, "k1_deleted": None, "refresh_refused": None, "expired_refused": None}
    if created.get("email"):
        ddb.delete_item(TableName=PARTNER, Key={"email": {"S": created["email"]}})
        gone = get_item(PARTNER, {"email": {"S": created["email"]}}) is None
        out["k1b_deleted"] = now_iso() if gone else None
        emit("  K1b DeleteItem -> consistent GetItem returns no Item: %s at %s" % (gone, now_iso()))
    if created.get("pk"):
        ddb.delete_item(TableName=USERS, Key={"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}})
        gone = get_item(USERS, {"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}}) is None
        out["k1_deleted"] = now_iso() if gone else None
        emit("  K1  DeleteItem -> consistent GetItem returns no Item: %s at %s" % (gone, now_iso()))
    emit("  deletions verified: %d of 2" % sum(1 for k in ("k1b_deleted", "k1_deleted") if out[k]))
    try:
        if sess.get("refresh_cookie"):
            req = urllib.request.Request(BASE + "/auth/refresh", method="POST",
                                         headers={"User-Agent": UA, "Cookie": sess["refresh_cookie"], "Origin": BASE})
            try:
                r = urllib.request.urlopen(req, timeout=60)
                st, respb = r.status, r.read()
            except urllib.error.HTTPError as e:
                st, respb = e.code, e.read()
            try:
                j = json.loads(respb.decode("utf-8"))
            except ValueError:
                j = {}
            minted = isinstance(j, dict) and bool(j.get("accessToken"))
            refused = st != 200 and not minted
            out["refresh_refused"] = now_iso() if refused else None
            emit("  REFRESH with the issued refresh token after K1's delete: HTTP %d; access token minted=%s -> %s"
                 % (st, minted, "REFUSED (1 of 1)" if refused else "NOT REFUSED -- STOP AND ESCALATE"))
        if sess.get("token"):
            exp = sess["claims"].get("exp", 0)
            wait = exp + 10 - time.time()
            emit("  waiting %.0f s for the access token's exp (%s) + 10 s" % (
                max(wait, 0), datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%H:%M:%SZ")))
            if wait > 0:
                time.sleep(wait)
            st, _, _b = http("GET", PFX + "/status", sess["token"])
            out["expired_refused"] = now_iso() if st == 401 else None
            emit("  the access token after exp: GET status -> HTTP %d -> %s" % (st, "REFUSED 401 (1 of 1)" if st == 401 else "NOT 401"))
    except Exception as exc:  # noqa: BLE001 -- the deletes above already ran
        emit("  EXCEPTION in the post-delete checks: %s: %s" % (type(exc).__name__, str(exc)[:300]))
    return out


def arm_d() -> bool:
    emit("(d) THE LIVE PROOF -- real HTTP requests through the deployed routes, under the deployed role")
    identity_line("(d)", served=True)
    if not prefix_scan("before"):
        emit("  STOP: a principal key already exists (residue) -- nothing written")
        return False
    om = json.loads(s3.get_object(Bucket=OM_BUCKET, Key=OM_KEY)["Body"].read().decode("utf-8"))
    present = ADVISOR in (om.get("advisors") or {})
    emit("  GUARD: %s PRESENT in s3://%s/%s: %s" % (ADVISOR, OM_BUCKET, OM_KEY, present))
    if not present:
        emit("  STOP at the guard: nothing written")
        return False
    password = secrets.token_urlsafe(24)
    SECRETS.append(password)
    created: dict = {}
    sess: dict = {}
    req_ok = keys_ok = False
    try:
        k = create_principal(int(time.time()), password, created)
        created["k1_created"] = k["k1_created"]
        sess = login(k["email"], password)
        c = sess.get("claims") or {}
        keys_ok = k["ok"] and sess.get("http") == 200 and c.get("firmId") == FIRM and c.get("advisorKey") == ADVISOR
        emit("  keys read back 2 of 2 and the session as the rtf-9 packet declares: %s" % keys_ok)
        if keys_ok:
            req_ok = requests_arm(sess["token"])
    except Exception as exc:  # noqa: BLE001 -- recorded, then the rollback runs
        emit("  EXCEPTION during the act: %s: %s -- rollback now" % (type(exc).__name__, str(exc)[:300]))
    finally:
        rb = rollback(created, sess)
    after_ok = prefix_scan("after")
    ends = [x for x in (rb.get("k1_deleted"), rb.get("k1b_deleted"), rb.get("refresh_refused")) if x]
    exp = (sess.get("claims") or {}).get("exp")
    if exp:
        ends.append(datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    emit("  INTERVAL: [%s, %s]" % (created.get("k1_created"), max(ends) if ends else "-"))
    life_ok = bool(rb.get("k1b_deleted")) and bool(rb.get("k1_deleted")) and bool(rb.get("refresh_refused")) and bool(rb.get("expired_refused")) and after_ok
    emit("  (d) keys + login %s; requests resolved with 0 DEFECT-STILL-PRESENT %s; lifecycle closed (2 of 2 deleted, refresh refused, "
         "401 after exp, no residue) %s" % (keys_ok, req_ok, life_ok))
    return keys_ok and req_ok and life_ok


def main() -> int:
    emit("IB-rtg-2 R73-AC1 battery (second pass) -- run at %s -- worktree HEAD %s" % (now_iso(), git("rev-parse", "HEAD")[1].strip()))
    emit("")
    a_ok = arm_a()
    emit("")
    b_ok = arm_b()
    emit("")
    c_ok = arm_c()
    emit("")
    arms = {"(a) packet+halves": a_ok, "(b) K-CODE post-apply": b_ok, "(c) precondition": c_ok}
    if not c_ok:
        emit("STOP at (c): the precondition is not met -- (d) is NOT run")
        arms["(d) live proof"] = False
    else:
        arms["(d) live proof"] = arm_d()
    emit("")
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else "FAIL"))
    if all(arms.values()):
        emit("RESULT: R73-AC1 PASS -- 4 of 4 arms hold")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R73-AC1 FAIL -- %d of %d arms hold" % (sum(arms.values()), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
