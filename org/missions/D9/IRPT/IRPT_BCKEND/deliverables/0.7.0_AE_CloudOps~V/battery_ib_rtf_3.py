#!/usr/bin/env python3
"""IRPT_BCKEND.TO-IB-rtf-3 (RE-HANDED @0382e96047) -- the bounded test principal on the TWO-KEY packet:
created, exercised on the disclosed-partial path by real signed requests, and deleted.

THE PACKET EXECUTED: NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md, blob a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4
(K1 the opal-users-v2 PROFILE item, K1b the opal-partner-49financial item {email, advisorKey}, K2 the session).
Its EXERCISE PLAN steps 1-9 are this battery's arms, with the halves' binding conditions:
  (a) PRECONDITION: 2 of 2 halves at HEAD naming the blob; the packet re-hashed equal.
  (b) GUARD (iii): the live 49financial ownership map re-read immediately before any write; abby_horton
      PRESENT or STOP; counts + VersionId recorded. Then K1, then K1b immediately before the login (ii);
      each read back by a consistent GetItem and hashed with passwordHash excluded from the digest input;
      one login through the real portal route mints K2 (never recorded; only its exp).
  (d) NEGATIVE CONTROLS BEFORE ANY OUTCOME ARM (iv): the firm swapped refused FIRM_BINDING without echo
      (2 of 2); a route outside api/scoped/ refused; the terminated client's entitlement gap enforced.
      A failed control is a STOP: the outcome arms are skipped and the rollback runs the same turn.
  (c) OUTCOME ARMS: FWD-1, FWD-2, FWD-5 by real signed requests, every response bound by its sha256 at the
      event; vendor calls counted; FWD-11 recorded as not reachable by this principal (v).
  (e) ROLLBACK in a finally block, so it runs on every path: K1b deleted FIRST, then K1, each verified by a
      failing consistent BASE-TABLE read (2 of 2, never the e-mail GSI); then a REFRESH with the issued
      refresh token REQUIRED to be refused (1 of 1; a success is a STOP and an escalation) (i); then one
      request with the access token after its exp REQUIRED to be refused 401. The interval is recorded as
      [K1 create, max(K1 delete verified, K1b delete verified, last access-token exp, refresh refused)].
      A failed-login throttle counter, if one exists, is named (vi).
NEVER PRINTED OR WRITTEN (vii): the password, the access token, the refresh token, the Authorization header,
any secret value. Response BODIES are not written either (real client data): each is bound by its sha256
and summarised by counts and codes only.
"""
from __future__ import annotations

import base64
import collections
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
OUTPUT_PATH = os.path.join(HERE, "IB-rtf-3_R60-AC1_battery_output.txt")
TOKEN = "IBR60-FOUR-OUTCOMES-EXERCISED-AND-PRINCIPAL-DELETED"

PACKET_REL = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.7.0_AE_CloudOps~V/NEVER_WIDEN_SIGNOFF_PACKET_IB-rtf-9.md"
PACKET_BLOB = "a1f36b95b26c8fefd6ff0d47489f9884f87dd2c4"
HALVES = {
    "COO": "org/tier1_exec/2.0.0_SA_COO~B/deliverables/NEVER_WIDEN_SIGNOFF_COO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
    "CTO": "org/tier1_exec/1.0.0_SA_CTO/deliverables/NEVER_WIDEN_SIGNOFF_CTO_HALF_IRPT_BCKEND_IB-rtf-9_TWO_KEY_PRINCIPAL.md",
}
USERS, PARTNER, THROTTLE = "opal-users-v2", "opal-partner-49financial", "opal-portal-auth-throttle"
FIRM, ADVISOR = "49financial", "abby_horton"
OM_BUCKET, OM_KEY = "opal-data-bd", "platinum/49financial/ownership_map.json"
DIR_BUCKET, DIR_POINTER = "opal-data-bd", "investor-reporting/directory/latest.json"
BASE = "https://opalinvest.dev"
PFX = "/api/scoped/investor-reporting"
PERF_FN = "irpt-performance-adapter"
UA = "opal-irpt-ib-rtf-3-battery/1.0 (0.7.0_AE_CloudOps~V)"

LINES: list[str] = []
SECRETS: list[str] = []
ddb = boto3.client("dynamodb", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")


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


def http(method: str, path: str, token: str | None = None, body: dict | None = None,
         query: dict | None = None, cookie: str | None = None, base: str = BASE):
    url = base + path
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


def is_refusal(status: int, j) -> tuple[bool, str]:
    """A refusal on this boundary is either a non-2xx at the edge, or a 2xx body carrying a public reason
    code and NO `data` (served.refuse returns a dict; under payload 2.0 that arrives as HTTP 200)."""
    if status >= 400:
        return True, "HTTP %d" % status
    if isinstance(j, dict) and "data" not in j:
        code = ((j.get("status") or {}).get("public_reason_code")) or j.get("error") or "?"
        return True, "HTTP %d, public_reason_code %s" % (status, code)
    return False, "SERVED (HTTP %d with data)" % status


def summarize(status: int, body: bytes) -> dict:
    j = as_json(body)
    out = {"http": status, "sha256": sha(body), "bytes": len(body)}
    if isinstance(j, dict):
        out["operation"] = j.get("operation")
        out["firm_id"] = j.get("firm_id")
        st = j.get("status") or {}
        out["reason"] = st.get("public_reason_code")
        out["state"] = st.get("state")
        out["business_date"] = (st.get("source_dates") or {}).get("business_date") if isinstance(st.get("source_dates"), dict) else st.get("business_date")
        out["unprojected_grant"] = j.get("unprojected_grant")
        d = j.get("data")
        out["data_kind"] = type(d).__name__ if "data" in j else "ABSENT"
        if isinstance(d, list):
            out["data_len"] = len(d)
    return out


def get_item(table: str, key: dict) -> dict | None:
    return ddb.get_item(TableName=table, Key=key, ConsistentRead=True).get("Item")


def item_digest(item: dict) -> str:
    safe = {k: v for k, v in item.items() if k != "passwordHash"}
    return sha(json.dumps(safe, sort_keys=True).encode("utf-8"))


def jwt_claims(tok: str) -> dict:
    seg = tok.split(".")[1]
    seg += "=" * (-len(seg) % 4)
    return json.loads(base64.urlsafe_b64decode(seg.encode()).decode("utf-8"))


def prefix_scan(label: str, pk_prefix: str, email_prefix: str) -> bool:
    ok = True
    for table, attr, prefix in ((USERS, "PK", pk_prefix), (USERS, "email", email_prefix), (PARTNER, "email", email_prefix)):
        d = ddb.scan(TableName=table, Select="COUNT", FilterExpression="begins_with(#a, :p)",
                     ExpressionAttributeNames={"#a": attr}, ExpressionAttributeValues={":p": {"S": prefix}})
        ok = ok and d["Count"] == 0
        emit("  %s: %s %s begins_with '%s': %d of %d scanned" % (label, table, attr, prefix, d["Count"], d["ScannedCount"]))
    return ok


# ------------------------------------------------------------------------------------------ arms
def arm_a() -> bool:
    emit("(a) PRECONDITION -- 2 of 2 halves at HEAD naming the packet blob; the packet re-hashed")
    rc, head = git("rev-parse", "--verify", "--quiet", "HEAD:" + PACKET_REL)
    _, wt = git("hash-object", PACKET_REL)
    pk_ok = rc == 0 and head.strip() == PACKET_BLOB and wt.strip() == PACKET_BLOB
    emit("  packet blob at HEAD %s, worktree %s -> %s" % (head.strip(), wt.strip(), "EQUAL" if pk_ok else "DIFFERS"))
    n = 0
    for who, path in HALVES.items():
        rc, text = git("show", "HEAD:" + path)
        ok = rc == 0 and PACKET_BLOB in text and all(k in text for k in ("K1", "K1b", "K2"))
        n += ok
        emit("  %s half at HEAD: present=%s names blob=%s names K1/K1b/K2=%s -> %s" % (
            who, rc == 0, PACKET_BLOB in text, all(k in text for k in ("K1", "K1b", "K2")), "OK" if ok else "FAIL"))
    emit("  halves: %d of %d" % (n, len(HALVES)))
    return pk_ok and n == len(HALVES)


def guard() -> tuple[bool, dict]:
    emit("(b) GUARD -- the live ownership map, immediately before any write")
    head = s3.head_object(Bucket=OM_BUCKET, Key=OM_KEY)
    obj = s3.get_object(Bucket=OM_BUCKET, Key=OM_KEY, VersionId=head["VersionId"])
    om = json.loads(obj["Body"].read().decode("utf-8"))
    adv = (om.get("advisors") or {}).get(ADVISOR)
    info = {"version": head["VersionId"], "etag": head["ETag"].strip('"'),
            "accounts": len((adv or {}).get("accounts") or []), "relationships": len((adv or {}).get("relationships") or [])}
    emit("  s3://%s/%s VersionId %s ETag %s at %s" % (OM_BUCKET, OM_KEY, info["version"], info["etag"], now_iso()))
    emit("  %s PRESENT=%s; accounts %d, relationships %d (packet's read 33 / 18)" % (
        ADVISOR, adv is not None, info["accounts"], info["relationships"]))
    return adv is not None, info


def directory_facts() -> dict:
    ptr = json.loads(s3.get_object(Bucket=DIR_BUCKET, Key=DIR_POINTER)["Body"].read().decode("utf-8"))
    d = json.loads(s3.get_object(Bucket=DIR_BUCKET, Key=ptr["key"])["Body"].read().decode("utf-8"))
    term = [e for e in d.get("entries") or [] if (e.get("termination") or {}).get("indicator") == "TERMINATED"]
    acc = next((a for e in term for a in (e.get("ids") or {}).get("account_ids") or []), None)
    return {"firm_id_opaque": d.get("firm_id_opaque"), "key": ptr["key"], "terminated": len(term),
            "terminated_account": acc, "as_of": d.get("as_of_business_date")}


def create_keys(epoch: int, password: str) -> dict:
    email = "irpt-rte1-test-%d@opal.test" % epoch
    pk = "USER#usr_irptrte_%d" % epoch
    created_at = now_iso()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode("ascii")
    SECRETS.append(pw_hash)
    k1 = {"PK": {"S": pk}, "SK": {"S": "PROFILE"}, "email": {"S": email}, "passwordHash": {"S": pw_hash},
          "name": {"S": "IRPT test principal (IB-rtf-3)"}, "role": {"S": "user"}, "firmId": {"S": FIRM},
          "status": {"S": "active"}, "createdAt": {"S": created_at}, "createdBy": {"S": "0.7.0_AE_CloudOps~V IB-rtf-3"}}
    ddb.put_item(TableName=USERS, Item=k1, ConditionExpression="attribute_not_exists(PK)")
    t_k1 = now_iso()
    got1 = get_item(USERS, {"PK": {"S": pk}, "SK": {"S": "PROFILE"}})
    emit("  K1 created %s: PK %s; read back (consistent GetItem): %s; attributes %d; digest (passwordHash excluded) %s"
         % (t_k1, pk, got1 is not None, len(got1 or {}), item_digest(got1) if got1 else "-"))
    return {"email": email, "pk": pk, "k1_created": t_k1, "k1_ok": got1 is not None and sorted(got1) == sorted(k1)}


def create_k1b(email: str) -> tuple[bool, str]:
    k1b = {"email": {"S": email}, "advisorKey": {"S": ADVISOR}}
    ddb.put_item(TableName=PARTNER, Item=k1b, ConditionExpression="attribute_not_exists(email)")
    t = now_iso()
    got = get_item(PARTNER, {"email": {"S": email}})
    emit("  K1b created %s: read back (consistent GetItem): %s; attributes %s; digest %s"
         % (t, got is not None, sorted(got or {}), item_digest(got) if got else "-"))
    return got is not None and sorted(got) == ["advisorKey", "email"], t


def login(email: str, password: str) -> dict:
    status, headers, body = http("POST", "/auth/login", body={"email": email, "password": password})
    j = as_json(body) or {}
    tok = j.get("accessToken") if isinstance(j, dict) else None
    cookies = headers.get_all("Set-Cookie") or []
    refresh = next((c.split(";", 1)[0] for c in cookies if c.startswith("refresh_token=")), None)
    if tok:
        SECRETS.append(tok)
    if refresh:
        SECRETS.append(refresh)
        SECRETS.append(refresh.split("=", 1)[1])
    out = {"http": status, "token": tok, "refresh_cookie": refresh, "at": now_iso()}
    emit("  login POST /auth/login -> HTTP %d at %s; access token minted=%s; refresh cookie set=%s; body keys %s"
         % (status, out["at"], bool(tok), bool(refresh), sorted(j) if isinstance(j, dict) else "-"))
    if tok:
        c = jwt_claims(tok)
        out["claims"] = c
        emit("  K2 claims: firmId=%s role=%s tier=%s advisorKey=%s advisorId=%s advisorRole=%r userType present=%s "
             "firmRole present=%s iat=%s exp=%s (exp %s)" % (
                 c.get("firmId"), c.get("role"), c.get("tier"), c.get("advisorKey"), c.get("advisorId"),
                 c.get("advisorRole"), "userType" in c, "firmRole" in c, c.get("iat"), c.get("exp"),
                 datetime.datetime.fromtimestamp(c.get("exp", 0), datetime.timezone.utc).strftime("%H:%M:%SZ")))
    return out


def negative_controls(tok: str, facts: dict) -> tuple[bool, list]:
    emit("(d) NEGATIVE CONTROLS -- before any outcome arm")
    rows = []
    for other in ("inflection", "cottonwood"):
        st, _, b = http("GET", PFX + "/directory/search", tok, query={"firm_id": other})
        refused, why = is_refusal(st, as_json(b))
        j = as_json(b) or {}
        code = (j.get("status") or {}).get("public_reason_code") if isinstance(j, dict) else None
        echo = other.encode() in b.lower()
        ok = refused and code == "FIRM_BINDING" and not echo
        rows.append(("NC1 firm swap -> %s" % other, ok))
        emit("  NC1 search with firm_id=%s: %s; code %s; swapped value echoed=%s; sha256 %s -> %s"
             % (other, why, code, echo, sha(b), "PASS" if ok else "FAIL"))
    st, _, b = http("GET", "/api/investor-reporting/directory/search", tok)
    j = as_json(b)
    served = st == 200 and isinstance(j, dict) and "data" in j and j.get("operation")
    ok = not served
    rows.append(("NC2 route outside api/scoped/", ok))
    emit("  NC2 GET /api/investor-reporting/directory/search (outside api/scoped/): HTTP %d; IRPT envelope served=%s; "
         "sha256 %s -> %s" % (st, bool(served), sha(b), "PASS" if ok else "FAIL"))
    acc = facts.get("terminated_account")
    if acc:
        st, _, b = http("GET", PFX + "/holdings/" + acc, tok)
        refused, why = is_refusal(st, as_json(b))
        echo = acc.encode() in b
        ok = refused and not echo
        rows.append(("NC3 terminated client's account", ok))
        emit("  NC3 holdings for a TERMINATED client's account (one of %d terminated entries; id sha256 %s): %s; "
             "echoed=%s -> %s" % (facts["terminated"], sha(acc.encode())[:16], why, echo, "PASS" if ok else "FAIL"))
    else:
        rows.append(("NC3 terminated client's account", False))
        emit("  NC3: no TERMINATED entry with an account id in the live directory -> FAIL (control not runnable)")
    n = sum(1 for _, ok in rows if ok)
    emit("  negative controls: %d of %d refused" % (n, len(rows)))
    return n == len(rows), rows


def outcome_arms(tok: str, guard_info: dict, facts: dict) -> dict:
    res = {}
    emit("(c) OUTCOME ARMS -- real signed requests; every body bound by sha256 at the event; bodies not written")
    # FWD-1: search -> select -> relationship + permitted accounts + as-of
    st, _, b = http("GET", PFX + "/directory/search", tok, query={"q": "a", "limit": "25"})
    s1 = summarize(st, b)
    j1 = as_json(b) or {}
    data = j1.get("data") if isinstance(j1, dict) and isinstance(j1.get("data"), list) else []
    ug = s1.get("unprojected_grant") or {}
    cnt, den = ug.get("count"), ug.get("denominator")
    k = (den - cnt) if isinstance(cnt, int) and isinstance(den, int) else None
    term_visible = sum(1 for e in data if ((e.get("termination") or {}).get("indicator") == "TERMINATED"))
    emit("  FWD-1 search ?q=a&limit=25: %s" % json.dumps(s1, sort_keys=True))
    emit("    entries %d; unprojected_grant count=%s denominator=%s kinds=%s -> k=%s; k+count=%s vs the map's %d "
         "accounts at the event; TERMINATED visible %d" % (len(data), cnt, den, ug.get("kinds"), k,
                                                          (k + cnt) if k is not None else None,
                                                          guard_info["accounts"], term_visible))
    st, _, b2 = http("GET", PFX + "/directory/search", tok, query={"q": "zzqqxxnomatch", "limit": "25"})
    j2 = as_json(b2) or {}
    n2 = len(j2.get("data") or []) if isinstance(j2, dict) and isinstance(j2.get("data"), list) else None
    emit("    q honoured? a no-match query returned %s entries (HTTP %d, sha256 %s) against %d for q=a"
         % (n2, st, sha(b2), len(data)))
    first = data[0] if data else {}
    ids = first.get("ids") or {}
    sel = {"relationship_id": ids.get("relationship_id")}
    st, _, b3 = http("POST", PFX + "/directory/resolve", tok,
                     body={"selection": sel, "client_id": ids.get("client_id"),
                           "relationship_id": ids.get("relationship_id"), "account_ids": ids.get("account_ids")})
    s3r = summarize(st, b3)
    j3 = as_json(b3) or {}
    d3 = j3.get("data") if isinstance(j3, dict) else None
    resolved = isinstance(d3, dict) and d3.get("ok") is True
    emit("  FWD-1 resolve (selection = the first entry's relationship): %s" % json.dumps(s3r, sort_keys=True))
    if isinstance(d3, dict):
        emit("    resolve data: ok=%s scope_kind=%s account_count=%s partial_reason=%s principal_class=%s"
             % (d3.get("ok"), (d3.get("resolved_scope") or {}).get("scope_kind"), d3.get("account_count"),
                (d3.get("partial_reason") or "")[:90], d3.get("principal_class")))
    binding_ok = s1.get("firm_id") == facts.get("firm_id_opaque")
    emit("    firm binding by the enforcer's own read: envelope firm_id %s == directory firm_id_opaque %s -> %s"
         % (s1.get("firm_id"), facts.get("firm_id_opaque"), binding_ok))
    as_of = bool(s1.get("business_date"))
    fwd1 = (st == 200 and s1.get("operation") == "directory-search" and len(data) > 0 and k is not None
            and k + cnt == den == guard_info["accounts"] and resolved and binding_ok and as_of and term_visible > 0)
    res["FWD-1"] = fwd1
    emit("  FWD-1 %s: search served=%s, k+count==denominator==map=%s, resolve served=%s, binding=%s, as-of=%s, "
         "terminated visible=%s" % ("PASS" if fwd1 else "FAIL", len(data) > 0,
                                     k is not None and k + cnt == den == guard_info["accounts"], resolved,
                                     binding_ok, as_of, term_visible > 0))

    # FWD-5: holdings for a permitted account (an issued account id from a WHOLE entry)
    acc = (ids.get("account_ids") or [None])[0]
    s5 = {}
    if acc:
        st, _, b5 = http("GET", PFX + "/holdings/" + acc, tok)
        s5 = summarize(st, b5)
        j5 = as_json(b5) or {}
        d5 = j5.get("data") if isinstance(j5, dict) else None
        nodes = (d5 or {}).get("nodes") or [] if isinstance(d5, dict) else []
        units = sum(1 for n in nodes if ((n.get("amount") or {}).get("units")))
        pct = sum(1 for n in nodes if (n.get("percentages") or {}).get("of_total") is not None)
        model = sum(1 for n in nodes if n.get("model_id"))
        kinds = collections.Counter(str(n.get("node_kind")) for n in nodes)
        totals = (d5 or {}).get("custody_totals") if isinstance(d5, dict) else None
        emit("  FWD-5 holdings/<permitted account> (id sha256 %s): %s" % (sha(acc.encode())[:16], json.dumps(s5, sort_keys=True)))
        emit("    nodes %d; units on %d of %d; of_total percentages on %d; model nodes %d; node_kind %s; "
             "custody positions %s" % (len(nodes), units, len(nodes), pct, model, dict(kinds),
                                       (totals or {}).get("unique_position_count")))
        fwd5 = (s5.get("http") == 200 and s5.get("operation") == "holdings-snapshot" and len(nodes) > 0
                and units == len(nodes) and pct > 0 and model > 0)
    else:
        fwd5 = False
        emit("  FWD-5: no permitted account id available from the search -> FAIL (not runnable)")
    res["FWD-5"] = fwd5
    emit("  FWD-5 %s" % ("PASS" if fwd5 else "FAIL"))

    # FWD-2: every tab within the permitted set + k of k swaps refused without echo
    served_rows = []
    if acc:
        st, _, bp = http("GET", PFX + "/performance/" + acc, tok, query={"start": "2026-01-01", "end": "2026-09-17"})
        sp = summarize(st, bp)
        served_rows.append(("performance/<permitted>", sp))
    st, _, bs = http("GET", PFX + "/status", tok)
    served_rows.append(("status (summary)", summarize(st, bs)))
    for name, s in served_rows:
        emit("  FWD-2 within the permitted set -- %s: %s" % (name, json.dumps(s, sort_keys=True)))
    rnd = secrets.token_hex(12)
    swaps = [
        ("holdings/<foreign account>", "GET", PFX + "/holdings/acc_" + rnd, None, None, "acc_" + rnd),
        ("performance/<foreign account>", "GET", PFX + "/performance/acc_" + rnd, None, None, "acc_" + rnd),
        ("narrative/<foreign report>", "GET", PFX + "/narrative/rep_" + rnd, None, None, "rep_" + rnd),
        ("status/<foreign job>", "GET", PFX + "/status/REQ-" + rnd, None, None, "REQ-" + rnd),
        ("analysis/<foreign job>/sections", "GET", PFX + "/analysis/REQ-" + rnd + "/sections", None, None, "REQ-" + rnd),
        ("export/<foreign export>", "GET", PFX + "/export/EXP-" + rnd, None, None, "EXP-" + rnd),
        ("export/<foreign export>/download", "GET", PFX + "/export/EXP-" + rnd + "/download", None, None, "EXP-" + rnd),
        ("resolve with firm_id=inflection in the body", "POST", PFX + "/directory/resolve", {"firm_id": "inflection"}, None, "inflection"),
    ]
    n_ref = 0
    for name, m, path, body, q, marker in swaps:
        st, _, bb = http(m, path, tok, body=body, query=q)
        refused, why = is_refusal(st, as_json(bb))
        echo = marker.encode() in bb
        ok = refused and not echo
        n_ref += ok
        emit("  FWD-2 swap %-44s -> %s; echoed=%s; sha256 %s -> %s" % (name, why, echo, sha(bb), "REFUSED" if ok else "NOT REFUSED"))
    within = [s for _, s in served_rows]
    within_served = sum(1 for s in within if s.get("http") == 200 and s.get("data_kind") not in ("ABSENT", None))
    fwd2 = n_ref == len(swaps) and within_served == len(within)
    res["FWD-2"] = fwd2
    emit("  FWD-2 %s: swaps refused without echo %d of %d; within-set tabs served %d of %d; the export within the "
         "set is not exercisable (no export exists for this firm -- row W1-S18 -- and POST /export is excluded)"
         % ("PASS" if fwd2 else "FAIL", n_ref, len(swaps), within_served, len(within)))

    # FWD-11: recorded as not reachable (condition v)
    res["FWD-11"] = "NOT-REACHABLE"
    emit("  FWD-11 NOT REACHABLE by this principal (a FIRM_ADVISOR token carries one firmId; OPAL_GLOBAL is the "
         "SSM roster + an opal-capital login, a separate act) -- recorded, no request made")

    # vendor calls
    cfg = boto3.client("lambda", region_name="us-east-1").get_function_configuration(FunctionName=PERF_FN)
    env = (cfg.get("Environment") or {}).get("Variables") or {}
    mode = env.get("IRPT_PERF_TRANSPORT_MODE", "<unset: default recorded>")
    egress = "IRPT_PERF_VENDOR_EGRESS_AUTHORIZED" in env
    live = 0 if (mode in ("recorded", "<unset: default recorded>") and not egress) else 1
    res["vendor_calls"] = live
    emit("  VENDOR CALLS: %d -- %s transport mode %s, egress authorization variable present=%s; POST /analysis "
         "and POST /export (the two routes that enqueue vendor work) called 0 times; directory/holdings compute "
         "is provider_calls 0 by construction" % (live, PERF_FN, mode, egress))
    return res


def rollback(created: dict, sess: dict) -> dict:
    emit("(e) ROLLBACK -- K1b FIRST, then K1; each verified by a failing consistent base-table read")
    out = {"k1b_deleted": None, "k1_deleted": None, "refresh_refused": None, "expired_refused": None}
    if created.get("k1b"):
        ddb.delete_item(TableName=PARTNER, Key={"email": {"S": created["email"]}})
        gone = get_item(PARTNER, {"email": {"S": created["email"]}}) is None
        out["k1b_deleted"] = now_iso() if gone else None
        emit("  K1b DeleteItem -> consistent GetItem returns no Item: %s at %s" % (gone, now_iso()))
    if created.get("k1"):
        ddb.delete_item(TableName=USERS, Key={"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}})
        gone = get_item(USERS, {"PK": {"S": created["pk"]}, "SK": {"S": "PROFILE"}}) is None
        out["k1_deleted"] = now_iso() if gone else None
        emit("  K1  DeleteItem -> consistent GetItem returns no Item: %s at %s" % (gone, now_iso()))
    n_del = sum(1 for k in ("k1b", "k1") if created.get(k))
    n_ok = sum(1 for k in ("k1b_deleted", "k1_deleted") if out[k])
    emit("  deletions verified: %d of %d" % (n_ok, n_del))
    try:
        _post_delete_checks(sess, out)
    except Exception as exc:  # noqa: BLE001 -- the deletes above already ran
        emit("EXCEPTION in the post-delete checks: %s: %s" % (type(exc).__name__, str(exc)[:300]))
    return out


def _post_delete_checks(sess: dict, out: dict) -> None:
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
        emit("  waiting %.0f s for the access token's exp (%s) + 10 s" % (max(wait, 0), datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%H:%M:%SZ")))
        if wait > 0:
            time.sleep(wait)
        st, _, b = http("GET", PFX + "/status", sess["token"])
        refused = st == 401
        out["expired_refused"] = now_iso() if refused else None
        emit("  the access token after exp: GET status -> HTTP %d -> %s" % (st, "REFUSED 401 (1 of 1)" if refused else "NOT 401"))


def main() -> int:
    emit("IB-rtf-3 R60-AC1 LIVE battery -- run at %s -- worktree HEAD %s" % (now_iso(), git("rev-parse", "HEAD")[1].strip()))
    emit("")
    arms: dict = {}
    if not arm_a():
        emit("STOP at (a): nothing written")
        arms["(a)"] = False
        return finish(arms)
    arms["(a)"] = True
    emit("")
    epoch = int(time.time())
    before_ok = prefix_scan("before", "USER#usr_irptrte_", "irpt-rte1-test-")
    g_ok, g_info = guard()
    facts = directory_facts()
    emit("  directory %s: firm_id_opaque %s, as_of %s, TERMINATED entries %d" % (facts["key"], facts["firm_id_opaque"], facts["as_of"], facts["terminated"]))
    if not (g_ok and before_ok):
        emit("STOP at the guard: nothing written")
        arms["(b) guard"] = False
        return finish(arms)
    arms["(b) guard"] = True
    password = secrets.token_urlsafe(24)
    SECRETS.append(password)
    created: dict = {}
    sess: dict = {}
    rb: dict = {}
    try:
        emit("")
        emit("(b) CREATE -- K1, then K1b immediately before the login")
        k = create_keys(epoch, password)
        created.update({"k1": True, "email": k["email"], "pk": k["pk"], "k1_created": k["k1_created"]})
        k1b_ok, t_k1b = create_k1b(k["email"])
        created["k1b"] = True
        sess = login(k["email"], password)
        c = sess.get("claims") or {}
        claims_ok = (sess.get("http") == 200 and c.get("firmId") == FIRM and c.get("role") == "user"
                     and c.get("advisorId") == ADVISOR and c.get("advisorKey") == ADVISOR and "userType" not in c
                     and "firmRole" not in c and c.get("advisorRole") in (None, ""))
        arms["(b) keys + login"] = k["k1_ok"] and k1b_ok and claims_ok
        emit("  keys created and read back 2 of 2=%s; login + claims as the packet declares=%s"
             % (k["k1_ok"] and k1b_ok, claims_ok))
        if not arms["(b) keys + login"]:
            emit("STOP after create: the keys or the session do not match the packet -- rollback now")
        else:
            emit("")
            nc_ok, _ = negative_controls(sess["token"], facts)
            arms["(d) negative controls"] = nc_ok
            if not nc_ok:
                emit("STOP: a negative control failed -- the outcome arms are skipped; rollback now")
            else:
                emit("")
                res = outcome_arms(sess["token"], g_info, facts)
                arms["(c) FWD-1"] = res["FWD-1"]
                arms["(c) FWD-2"] = res["FWD-2"]
                arms["(c) FWD-5"] = res["FWD-5"]
                arms["(c) vendor calls 0"] = res["vendor_calls"] == 0
    except Exception as exc:  # noqa: BLE001 -- recorded, then the rollback runs
        emit("EXCEPTION during the act: %s: %s -- rollback now" % (type(exc).__name__, str(exc)[:300]))
        arms["(act) no exception"] = False
    finally:
        emit("")
        rb = rollback(created, sess)
    after_ok = prefix_scan("after", "USER#usr_irptrte_", "irpt-rte1-test-")
    thr_pk = "login#acct#" + sha((created.get("email") or "").strip().lower().encode())
    thr = get_item(THROTTLE, {"pk": {"S": thr_pk}}) if created.get("email") else None
    emit("  failed-login throttle counter for the test e-mail: %s" % ("PRESENT (named here, TTL'd)" if thr else "none"))
    n_del = sum(1 for key in ("k1b", "k1") if created.get(key))
    arms["(e) deletes verified"] = n_del == 2 and bool(rb.get("k1b_deleted")) and bool(rb.get("k1_deleted"))
    arms["(e) refresh refused"] = bool(rb.get("refresh_refused"))
    arms["(e) expired token refused"] = bool(rb.get("expired_refused"))
    arms["(e) no residue"] = after_ok
    ends = [x for x in (rb.get("k1_deleted"), rb.get("k1b_deleted"), rb.get("refresh_refused")) if x]
    exp = (sess.get("claims") or {}).get("exp")
    if exp:
        ends.append(datetime.datetime.fromtimestamp(exp, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    emit("  INTERVAL: [%s, %s] (K1 create, max of the deletes verified, the last access-token exp, the refresh refused)"
         % (created.get("k1_created"), max(ends) if ends else "-"))
    return finish(arms)


def finish(arms: dict) -> int:
    emit("")
    for kk, v in arms.items():
        emit("ARM %s: %s" % (kk, "PASS" if v else "FAIL"))
    emit("FWD-11: NOT-REACHABLE by this principal, recorded (re-hand condition (v))")
    if arms and all(arms.values()) and len(arms) == 12:
        emit("RESULT: R60-AC1 PASS -- the outcomes exercised by real signed requests and the principal deleted")
        emit(TOKEN)
        rc = 0
    else:
        emit("RESULT: R60-AC1 FAIL -- %d of %d arms hold" % (sum(1 for v in arms.values() if v), len(arms)))
        rc = 1
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(LINES) + "\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
