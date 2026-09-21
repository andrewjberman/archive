#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtg-1 battery -- the export receipt aligns to the writer and the taxonomy
tests the code. R72-AC1.

DISCLOSED-PARTIAL (row IRPT_BCKEND-W1-S43, disarm_owner 2.0.0_SA_COO~B): the DEPLOYED
`entry.py`'s own wired `submit_export` unconditionally raises `_ExportNotWiredHere` /
`NOT_READY` and never calls `handler.py` -- so a served submit->receipt round trip through
POST /export cannot be exercised on the deployed path, today. This battery grades the
EXERCISABLE SUBSTANCE the code edit actually fixes instead:

  PART 1 -- KEY ALIGNMENT (S105). The reader's key (export/entry.py's RECEIPT_KEY_TEMPLATE,
  imported and evaluated as REAL production code, never re-typed as a string literal) is
  compared against the writer's key (export/handler.py's receipt_key(), same treatment) for
  a REAL export_id minted by export/identity.py's real identity_for() over a real sha256
  input. Then a receipt is PERSISTED at that exact address using handler.py's own real
  persist_receipt() (this worker's own S3 credentials write it -- the deployed function's own
  submit path cannot, per the disclosure above) and READ BACK over the REAL deployed HTTP
  route, under the REAL deployed execution role (irpt-export-render-role), through a real
  bounded test principal's real JWT. A SERVED response (not NOT_FOUND) whose content equals
  what was persisted is the round trip the order asks for, exercised as far as the disclosed
  gap allows.

  PART 2 -- TAXONOMY BY CODE (S106), on REAL WIRE ERRORS, never a constructed ClientError
  stub. (a) an export_id that does NOT match the new IAM grant's `EXP-*` resource pattern
  produces a REAL 403 AccessDenied from S3 when the deployed function (under its own role)
  attempts the GetObject -- the route must answer NOT_FOUND, not UNEXPECTED (this is exactly
  the bug S106 fixes: the OLD code matched exception CLASS NAMES and let a modeled
  AccessDenied propagate). (b) a real EXP-* id that was never written produces a REAL 404
  NoSuchKey -- the route must still answer NOT_FOUND (the case the old code already handled,
  proven still correct after the rewrite).

BOUNDED-PRINCIPAL MECHANISM reused (per this order's arm (e)) from
org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/battery_ib_rtf_10.py at
HEAD: K1 (opal-users-v2) + K1b (opal-partner-49financial) created, a real login, real HTTP
requests, then K1b and K1 deleted and verified, the refresh REFUSED, 401 after exp -- a FRESH
epoch, the full lifecycle including delete. NEVER PRINTED OR WRITTEN: the password, any
access or refresh token, the Authorization header. The token prints only when every arm holds.

ASCII only. Python 3.12.
"""
from __future__ import annotations

import base64
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

import bcrypt
import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "..", ".."))
OUTPUT_PATH = os.path.join(HERE, "IB-rtg-1_R72-AC1_battery_output.txt")
TOKEN = "IBR72-EXPORT-RECEIPT-ALIGNED-AND-TAXONOMY-BY-CODE"

EXPORT_DIR = os.path.join(WS, "infra", "aws", "lambda", "investor-reporting", "export")
if EXPORT_DIR not in sys.path:
    sys.path.insert(0, EXPORT_DIR)

# MODULE-NAME COLLISION GUARD: `export/handler.py`'s own sys.path.insert(0, .../directory) (for
# its `download_mod` import) SHADOWS `export/entry.py` with `directory/entry.py` for any `import
# entry` that runs AFTER `handler` is first imported (both dirs carry an `entry.py`; `directory`
# does not carry an `identity.py` or `receipt.py`, so those two names are unaffected). Importing
# `entry` (and `identity`) HERE, before `handler`, caches the CORRECT file in sys.modules so every
# later `import entry`/`import identity` in this script -- regardless of what handler.py's own
# import does to sys.path afterward -- returns the already-cached, correctly-resolved module.
import entry as entry_mod        # noqa: E402  export/entry.py -- the DEPLOYED reader, real code
import identity as identity_mod  # noqa: E402  export/identity.py, real code
import handler as handler_mod    # noqa: E402  export/handler.py, real code (mutates sys.path)
import receipt as receipt_mod    # noqa: E402  export/receipt.py, real code
assert entry_mod.__file__ == os.path.join(EXPORT_DIR, "entry.py"), (
    "module collision guard tripped: entry_mod resolved to %s, not export/entry.py" % entry_mod.__file__)
assert handler_mod.__file__ == os.path.join(EXPORT_DIR, "handler.py"), (
    "module collision guard tripped: handler_mod resolved to %s, not export/handler.py" % handler_mod.__file__)

D_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~1"
PACKET_REL = D_REL + "/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtg-1.md"
PACKET_BLOB = "74a1004fde6e649c321f43d62cfbda5b61489b98"
COO_HALF_REL = "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtg-1_EXPORT_RECEIPT.md"
CTO_HALF_REL = "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtg-1_20260920.md"

ACCT = "313476888478"
FUNCTION_NAME = "irpt-export-render"
ROLE_NAME = "irpt-export-render-role"
EVIDENCE_BUCKET = "opal-data-ycharts"

USERS, PARTNER, THROTTLE = "opal-users-v2", "opal-partner-49financial", "opal-portal-auth-throttle"
FIRM, ADVISOR = "49financial", "abby_horton"
BASE = "https://opalinvest.dev"
PFX = "/api/scoped/investor-reporting"
UA = "opal-irpt-ib-rtg-1-battery/1.0 (0.9.0_WK_IRPT_BCKEND~1)"

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


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_b64(b: bytes) -> str:
    return base64.b64encode(hashlib.sha256(b).digest()).decode()


def identity_line(arm: str, served: bool = False) -> None:
    if not IDENTITY:
        IDENTITY.append(boto3.client("sts").get_caller_identity()["Arn"])
    if served:
        emit("  identity: %s -- HTTP requests run as the bounded test principal; the served "
             "compute runs as %s's OWN execution role %s (printed per request); the operator "
             "identity %s only writes the test receipt object, creates/deletes the principal's "
             "keys, and reads configuration" % (arm, FUNCTION_NAME, ROLE_NAME, IDENTITY[0]))
    else:
        emit("  identity: %s ran as %s -- a configuration/code claim, NOT a served behaviour"
             % (arm, IDENTITY[0]))


# ------------------------------------------------------------------------------------------ arm 0
def arm_packet() -> bool:
    emit("(0) THE PACKET AND BOTH HALVES -- at HEAD, naming this blob")
    identity_line("(0)")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    head = head.strip() if rc == 0 else ""
    _, wt = git("hash-object", os.path.join(WS, PACKET_REL))
    ok = bool(head) and head == wt.strip() == PACKET_BLOB
    emit("  packet %s: blob at HEAD %s, worktree %s, signed %s -> %s"
         % (PACKET_REL, head or "ABSENT", wt.strip(), PACKET_BLOB,
            "COMMITTED, UNCHANGED" if ok else "NOT THE SIGNED BLOB"))
    n = 0
    for who, path in (("COO", COO_HALF_REL), ("CTO", CTO_HALF_REL)):
        rc2, text = git("show", "HEAD:" + path)
        naming = rc2 == 0 and PACKET_BLOB in text
        n += naming
        emit("  %s half %s: %s" % (who, path, "PRESENT, naming blob" if naming else "ABSENT or not naming the blob"))
    emit("  halves: %d of 2" % n)
    return ok and n == 2


# ------------------------------------------------------------------------------------------ arm 1
def arm_alignment() -> tuple[bool, str, str]:
    emit("(1) KEY ALIGNMENT -- S105, real production code, both sides")
    identity_line("(1)")
    # identity_mod, handler_mod, entry_mod are the module-level imports above (collision-guarded).

    bundle_sha = sha256_hex(b"IB-rtg-1 battery bundle fixture " + str(time.time()).encode())
    contract_version = "1.0.0"
    ident = identity_mod.identity_for(bundle_sha, contract_version, 1)
    export_id = ident["export_id"]
    emit("  real identity.identity_for(bundle_sha256=%s..., contract_version=%s) -> export_id %s"
         % (bundle_sha[:16], contract_version, export_id))

    writer_key = handler_mod.receipt_key(FIRM, export_id)
    reader_key = entry_mod.RECEIPT_KEY_TEMPLATE.format(firm=FIRM, export_id=export_id)
    emit("  writer key (handler.receipt_key, real function):  %s" % writer_key)
    emit("  reader key (entry.RECEIPT_KEY_TEMPLATE, real deployed default): %s" % reader_key)
    aligned = writer_key == reader_key
    emit("  KEY ALIGNMENT: %s" % ("EQUAL" if aligned else "DIFFERS -- S105 NOT fixed"))
    _, entry_source = git("show", "HEAD:infra/aws/lambda/investor-reporting/export/entry.py")
    no_env_override = "IRPT_EXPORT_RECEIPT_KEY" not in os.environ
    emit("  no local IRPT_EXPORT_RECEIPT_KEY override in this run's environment: %s (the ruling "
         "REFUSES using the Terraform override to mask a wrong default; unset here confirms this "
         "run reads entry.py's own real default, the same one the deployed function reads)"
         % no_env_override)
    return aligned and no_env_override, export_id, bundle_sha


# ------------------------------------------------------------------------------------------ arm 2
def arm_write(export_id: str, bundle_sha: str) -> tuple[bool, dict, str]:
    emit("(2) PERSIST A RECEIPT AT THE ALIGNED ADDRESS -- handler.persist_receipt() + receipt.build(), real functions")
    identity_line("(2)")
    # receipt_mod, handler_mod are the module-level imports above (collision-guarded).

    facts = {"page_count": 1, "validation_status": "PASSED", "validation_failures": 0}
    created = now_iso()
    artifact_key = "firms/%s/generations/%s/attempts/1/exports/1/report.pdf" % (FIRM, export_id)
    built, sidecar = receipt_mod.build(
        bundle={"performance_report_revisions": []}, bundle_sha256=bundle_sha,
        artifact_sha256=sha256_hex(b"IB-rtg-1 battery artifact fixture"),
        storage_bucket=EVIDENCE_BUCKET, storage_key=artifact_key, facts=facts,
        created_at=created, released_at=created, job_state="READY",
        export_id=export_id)
    emit("  receipt.build() real output: export_id %s, job_state %s, vendor_signed_url_exposed %s"
         % (built["export_ref"]["export_id"], built["job_state"], built["vendor_signed_url_exposed"]))
    result = handler_mod.persist_receipt(built, FIRM, export_id, region="us-east-1")
    emit("  handler.persist_receipt() real write+readback: bucket %s key %s bytes %d equal(readback==written) %s"
         % (result["bucket"], result["key"], result["bytes"], result["equal"]))
    emit("  persist_receipt is 1 of 1 corpus writers of this address (the packet's own W=1 census); this run's "
         "write stands in for the deployed submit path per the disclosed partial (row W1-S43)")
    return bool(result["equal"]) and result["key"] == entry_receipt_key(FIRM, export_id), built, result["key"]


def entry_receipt_key(firm: str, export_id: str) -> str:
    return entry_mod.RECEIPT_KEY_TEMPLATE.format(firm=firm, export_id=export_id)


# ------------------------------------------------------------------------------------------ HTTP + principal
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


def classify(status: int, j) -> dict:
    """SERVED (2xx with data) | POLICY (a refusal carrying a firm_id, code not UNEXPECTED) |
    UNEXPECTED | UNRESOLVED (no firm_id -- the scope was never read)."""
    out = {"http": status}
    if isinstance(j, dict):
        st = j.get("status") or {}
        out.update({"operation": j.get("operation"), "firm_id": j.get("firm_id"),
                    "code": st.get("public_reason_code"), "state": st.get("state")})
        if status < 400 and "data" in j and j.get("data") is not None:
            out["class"] = "SERVED"
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


def get_item(table: str, key: dict) -> dict | None:
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def item_digest(item: dict) -> str:
    return sha256_hex(json.dumps({k: v for k, v in item.items() if k != "passwordHash"},
                                 sort_keys=True).encode("utf-8"))


def jwt_claims(tok: str) -> dict:
    seg = tok.split(".")[1]
    seg += "=" * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg.encode()).decode("utf-8"))


def prefix_scan(label: str) -> bool:
    ok = True
    for table, attr, prefix in ((USERS, "PK", "USER#usr_irptrtg1_"),
                                (USERS, "email", "irpt-rtg1-test-"),
                                (PARTNER, "email", "irpt-rtg1-test-")):
        d = ddb.scan(TableName=table, Select="COUNT", FilterExpression="begins_with(#a, :p)",
                     ExpressionAttributeNames={"#a": attr}, ExpressionAttributeValues={":p": {"S": prefix}})
        ok = ok and d["Count"] == 0
        emit("  %s: %s %s begins_with '%s': %d of %d scanned" % (label, table, attr, prefix, d["Count"], d["ScannedCount"]))
    return ok


def create_principal(epoch: int, password: str, created: dict) -> dict:
    email = "irpt-rtg1-test-%d@opal.test" % epoch
    pk = "USER#usr_irptrtg1_%d" % epoch
    created.update({"email": email, "pk": pk})
    created_at = now_iso()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode("ascii")
    SECRETS.append(pw_hash)
    k1 = {"PK": {"S": pk}, "SK": {"S": "PROFILE"}, "email": {"S": email}, "passwordHash": {"S": pw_hash},
          "name": {"S": "IRPT test principal (IB-rtg-1)"}, "role": {"S": "user"}, "firmId": {"S": FIRM},
          "status": {"S": "active"}, "createdAt": {"S": created_at}, "createdBy": {"S": "0.9.0_WK_IRPT_BCKEND~1 IB-rtg-1"}}
    ddb.put_item(TableName=USERS, Item=k1, ConditionExpression="attribute_not_exists(PK)")
    t_k1 = now_iso()
    got1 = get_item(USERS, {"PK": {"S": pk}, "SK": {"S": "PROFILE"}})
    emit("  K1 created %s: PK %s; consistent read-back %s; attributes %d; digest (passwordHash excluded) %s"
         % (t_k1, pk, got1 is not None, len(got1 or {}), item_digest(got1) if got1 else "-"))
    k1b = {"email": {"S": email}, "advisorKey": {"S": ADVISOR}}
    ddb.put_item(TableName=PARTNER, Item=k1b, ConditionExpression="attribute_not_exists(email)")
    t_k1b = now_iso()
    got = get_item(PARTNER, {"email": {"S": email}})
    emit("  K1b created %s in %s: consistent read-back %s; attributes %s"
         % (t_k1b, PARTNER, got is not None, sorted(got or {})))
    return {"email": email, "pk": pk, "k1_created": t_k1,
            "ok": got1 is not None and sorted(got1) == sorted(k1) and got is not None
            and sorted(got) == ["advisorKey", "email"]}


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
        emit("  K2 claims: firmId=%s role=%s advisorKey=%s exp=%s"
             % (c.get("firmId"), c.get("role"), c.get("advisorKey"),
                datetime.datetime.fromtimestamp(c.get("exp", 0), datetime.timezone.utc).strftime("%H:%M:%SZ")))
    return out


def rollback(created: dict, sess: dict, receipt_key: str | None) -> dict:
    emit("  ROLLBACK -- test receipt object, K1b, then K1; each verified")
    out = {"receipt_deleted": None, "k1b_deleted": None, "k1_deleted": None,
           "refresh_refused": None, "expired_refused": None}
    if receipt_key:
        s3.delete_object(Bucket=EVIDENCE_BUCKET, Key=receipt_key)
        gone = False
        try:
            s3.head_object(Bucket=EVIDENCE_BUCKET, Key=receipt_key)
        except s3.exceptions.ClientError as exc:
            gone = exc.response.get("Error", {}).get("Code") in ("404", "NoSuchKey", "NotFound")
        out["receipt_deleted"] = now_iso() if gone else None
        emit("  test receipt DeleteObject %s -> head-object confirms gone: %s at %s" % (receipt_key, gone, now_iso()))
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
    emit("  deletions verified: %d of 3" % sum(1 for k in ("receipt_deleted", "k1b_deleted", "k1_deleted") if out[k]))
    try:
        if sess.get("refresh_cookie"):
            st, _, b = http("POST", "/auth/refresh", cookie=sess["refresh_cookie"])
            j = as_json(b) or {}
            minted = isinstance(j, dict) and bool(j.get("accessToken"))
            refused = st != 200 and not minted
            out["refresh_refused"] = now_iso() if refused else None
            emit("  REFRESH with the issued refresh token after K1's delete: HTTP %d; access token minted=%s -> %s"
                 % (st, minted, "REFUSED (1 of 1)" if refused else "NOT REFUSED -- STOP AND ESCALATE"))
        if sess.get("token"):
            exp = sess["claims"].get("exp", 0)
            wait = exp + 10 - time.time()
            emit("  waiting %.0f s for the access token's exp (%s) + 10 s"
                 % (max(wait, 0), datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%H:%M:%SZ")))
            if wait > 0:
                time.sleep(wait)
            st, _, _b = http("GET", PFX + "/status", sess["token"])
            out["expired_refused"] = now_iso() if st == 401 else None
            emit("  the access token after exp: GET status -> HTTP %d -> %s"
                 % (st, "REFUSED 401 (1 of 1)" if st == 401 else "NOT 401"))
    except Exception as exc:  # noqa: BLE001 -- the deletes above already ran
        emit("  EXCEPTION in the post-delete checks: %s: %s" % (type(exc).__name__, str(exc)[:300]))
    return out


# ------------------------------------------------------------------------------------------ main flow
def main() -> int:
    emit("IB-rtg-1 R72-AC1 battery -- run at %s -- worktree HEAD %s" % (now_iso(), git("rev-parse", "HEAD")[1].strip()))
    emit("route: GET %s/export/{exportId}  |  function: %s  |  role: %s"
         % (PFX, FUNCTION_NAME, ROLE_NAME))
    emit("")
    packet_ok = arm_packet()
    emit("")
    align_ok, export_id, bundle_sha = arm_alignment()
    emit("")

    if not packet_ok or not align_ok:
        emit("STOP: packet/halves not at HEAD, or S105 key alignment fails -- (2)-(6) NOT graded")
        arms = {"(0) packet+halves": packet_ok, "(1) key alignment": align_ok,
                "(2) persist": False, "(3) principal+login": False, "(4) round trip": False,
                "(5) taxonomy": False, "(6) rollback": False}
        for k, v in arms.items():
            emit("ARM %s: %s" % (k, "PASS" if v else "FAIL"))
        emit("RESULT: R72-AC1 FAIL -- %d of %d arms hold" % (sum(arms.values()), len(arms)))
        with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LINES) + "\n")
        return 1

    write_ok, receipt_obj, written_key = arm_write(export_id, bundle_sha)
    emit("")

    emit("(3) BOUNDED PRINCIPAL -- fresh epoch, K1 + K1b, real login")
    identity_line("(3)")
    if not prefix_scan("before"):
        emit("  STOP: a principal key already exists (residue) -- nothing written")
        with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(LINES) + "\n")
        return 1
    password = __import__("secrets").token_urlsafe(24)
    SECRETS.append(password)
    created: dict = {}
    sess: dict = {}
    principal_ok = False
    try:
        k = create_principal(int(time.time()), password, created)
        created["k1_created"] = k["k1_created"]
        sess = login(k["email"], password)
        c = sess.get("claims") or {}
        principal_ok = k["ok"] and sess.get("http") == 200 and c.get("firmId") == FIRM and c.get("advisorKey") == ADVISOR
        emit("  keys read back 2 of 2 and session claims as declared: %s" % principal_ok)
    except Exception as exc:  # noqa: BLE001
        emit("  EXCEPTION creating the principal: %s: %s" % (type(exc).__name__, str(exc)[:300]))
    emit("")

    roundtrip_ok = False
    taxonomy_denied_ok = False
    taxonomy_notfound_ok = False
    unexpected_count = 0
    try:
      if principal_ok:
        emit("(4) ROUND TRIP -- GET %s/export/%s under the deployed route+role" % (PFX, export_id))
        identity_line("(4)", served=True)
        st, _, b = http("GET", PFX + "/export/" + export_id, sess["token"])
        j = as_json(b)
        c = classify(st, j)
        emit("  GET /export/%s -> function %s (role %s): %s http %d code %s firm_id %s"
             % (export_id, FUNCTION_NAME, ROLE_NAME, c["class"], st, c.get("code"),
                "present" if c.get("firm_id") else "ABSENT"))
        data = j.get("data") if isinstance(j, dict) else None
        content_matches = isinstance(data, dict) and data.get("export_ref", {}).get("export_id") == export_id \
            and data.get("artifact", {}).get("sha256") == receipt_obj["artifact"]["sha256"]
        roundtrip_ok = c["class"] == "SERVED" and content_matches
        emit("  SERVED with the just-written receipt (export_id + artifact sha256 match what arm (2) persisted): %s"
             % content_matches)
        emit("  round trip (no NOT_FOUND, content matches the write): %s" % roundtrip_ok)
        if c["class"] == "UNEXPECTED":
            unexpected_count += 1

        emit("")
        emit("(5) TAXONOMY BY CODE -- REAL wire errors, never a constructed ClientError stub")
        identity_line("(5)", served=True)
        # (a) a real 403 AccessDenied: an export_id NOT matching the EXP-* IAM resource pattern.
        denied_id = "plainid-" + hashlib.sha256(b"denied probe " + str(time.time()).encode()).hexdigest()[:16]
        st_a, _, b_a = http("GET", PFX + "/export/" + denied_id, sess["token"])
        j_a = as_json(b_a)
        c_a = classify(st_a, j_a)
        emit("  GET /export/%s (key outside the EXP-* grant -> real S3 403 AccessDenied) -> %s http %d code %s"
             % (denied_id, c_a["class"], st_a, c_a.get("code")))
        taxonomy_denied_ok = c_a.get("code") == "NOT_FOUND" and c_a["class"] != "UNEXPECTED"
        if c_a["class"] == "UNEXPECTED":
            unexpected_count += 1
        emit("  S106 (AccessDenied -> NOT_FOUND, not UNEXPECTED): %s" % taxonomy_denied_ok)

        # (b) a real 404 NoSuchKey: a real EXP-* id that matches the grant but was never written.
        missing_bundle_sha = sha256_hex(b"IB-rtg-1 battery NEVER WRITTEN " + str(time.time()).encode())
        missing_id = identity_mod.identity_for(missing_bundle_sha, "1.0.0", 1)["export_id"]
        st_b, _, b_b = http("GET", PFX + "/export/" + missing_id, sess["token"])
        j_b = as_json(b_b)
        c_b = classify(st_b, j_b)
        emit("  GET /export/%s (real EXP-* id, IAM allows, object absent -> real S3 404 NoSuchKey) -> %s http %d code %s"
             % (missing_id, c_b["class"], st_b, c_b.get("code")))
        taxonomy_notfound_ok = c_b.get("code") == "NOT_FOUND" and c_b["class"] != "UNEXPECTED"
        if c_b["class"] == "UNEXPECTED":
            unexpected_count += 1
        emit("  NoSuchKey -> NOT_FOUND (unchanged correct behaviour): %s" % taxonomy_notfound_ok)

        emit("")
        emit("(disclosed, not graded) POST %s/export -- the submit-wiring gap, W1-S43" % PFX)
        st_s, _, b_s = http("POST", PFX + "/export", sess["token"], body={"probe": "IB-rtg-1 battery"})
        j_s = as_json(b_s)
        c_s = classify(st_s, j_s)
        emit("  POST /export -> %s http %d code %s -- EXPECTED NOT_READY (row W1-S43, the submit "
             "controller is not wired to this entry on the deployed path; NOT counted toward the "
             "0-UNEXPECTED tally below, disclosed per this order's arm (e) note)"
             % (c_s["class"], st_s, c_s.get("code")))
    except Exception as exc:  # noqa: BLE001 -- rollback (6) must still run
      emit("  EXCEPTION during arms (4)/(5): %s: %s -- rollback now" % (type(exc).__name__, str(exc)[:300]))

    emit("")
    emit("(6) ROLLBACK")
    rb = rollback(created, sess, written_key if write_ok else None)
    after_ok = prefix_scan("after")
    rollback_ok = (bool(rb.get("receipt_deleted")) and bool(rb.get("k1b_deleted"))
                  and bool(rb.get("k1_deleted")) and bool(rb.get("refresh_refused"))
                  and bool(rb.get("expired_refused")) and after_ok)
    emit("  lifecycle closed (3 of 3 deleted, refresh refused, 401 after exp, no residue): %s" % rollback_ok)

    emit("")
    arms = {
        "(0) packet+halves": packet_ok,
        "(1) key alignment (S105)": align_ok,
        "(2) persist at the aligned address": write_ok,
        "(3) bounded principal + login": principal_ok,
        "(4) round trip (no NOT_FOUND)": roundtrip_ok,
        "(5a) taxonomy: AccessDenied -> NOT_FOUND (S106)": taxonomy_denied_ok,
        "(5b) taxonomy: NoSuchKey -> NOT_FOUND": taxonomy_notfound_ok,
        "(6) rollback, full lifecycle": rollback_ok,
    }
    for k, v in arms.items():
        emit("ARM %s: %s" % (k, "PASS" if v else "FAIL"))
    emit("UNEXPECTED count on the exercised firm (%s): %d" % (FIRM, unexpected_count))
    if all(arms.values()) and unexpected_count == 0:
        emit("RESULT: R72-AC1 PASS -- %d of %d arms hold, 0 UNEXPECTED" % (len(arms), len(arms)))
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R72-AC1 FAIL -- %d of %d arms hold, %d UNEXPECTED"
             % (sum(arms.values()), len(arms), unexpected_count))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
