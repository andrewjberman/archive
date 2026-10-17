"""IRPT_DASHBD TO-DB-b-331 (round 150): mint and remove the two synthetic V-leg principals in opal-users-v2.

Subcommands (the two fixed addresses are the ONLY addresses this file will touch; anything else is refused):
  state                 read both rows (consistent get + email-index count); prints ABSENT/PRESENT lines.
  pair                  generate two passwords IN MEMORY (never printed, never written, never in argv/env), mint COVERING then
                        NON_COVERING once each (attribute_not_exists(PK), read-back), poll the email index up to 120 s until
                        each reads 1, sign both in (POST /auth/login on the base), and print the two bearer tokens ONCE as
                        "SESSION <ROLE> <token>" lines for the broker hand-over. On any failure it removes whatever it minted.
  remove [ROLE ...]     delete the row(s) (attribute_exists), poll ABSENT on the index and a consistent get.

Row shapes (read from fwd1_mint.py / fwd5_mint.py, not imported):
  COVERING      firmId opal-capital (the verified internal-subject predicate), allowedFirmIds [49financial]
  NON_COVERING  firmId cottonwood, allowedFirmIds [cottonwood]   (a non-empty Cottonwood scope; no 49 Financial account)
Both: role user, userType test-filer, status active, no MFA attribute, bcrypt cost 12, exp = now + 3 h.
Facts only go to state331/*.json: UTC times, statuses in words, counts. Never an address, a hash, a password or a token.
"""
from __future__ import annotations

import hashlib
import json
import secrets
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REGION = "us-east-1"
TABLE = "opal-users-v2"
INDEX = "email-index"
SK = "PROFILE"
TTL_HOURS = 3
COST = 12
BASE = "http://localhost:5174"
ROLES = ("COVERING", "NON_COVERING")
EMAILS = {"COVERING": "v328-cover-r150@opal.invalid", "NON_COVERING": "v328-ctrl-r150@opal.invalid"}
SPEC = {
    "COVERING": {"firm": "opal-capital", "ids": ["49financial"], "klass": "OPAL_GLOBAL",
                 "name": "IRPT_DASHBD TO-DB-b-331 synthetic covering staff viewer"},
    "NON_COVERING": {"firm": "cottonwood", "ids": ["cottonwood"], "klass": "COTTONWOOD_SCOPED",
                     "name": "IRPT_DASHBD TO-DB-b-331 synthetic non-covering Cottonwood viewer"},
}
HERE = Path(__file__).resolve().parent
STATE = HERE / "state331"


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def digest12(email):
    return hashlib.sha256(email.encode("utf-8")).hexdigest()[:12]


def save(name, obj):
    STATE.mkdir(exist_ok=True)
    (STATE / (name + ".json")).write_text(json.dumps(obj, indent=1, sort_keys=True) + "\n", encoding="ascii")


def client():
    import boto3
    return boto3.client("dynamodb", region_name=REGION)


def key(role):
    return {"PK": {"S": "USER#" + EMAILS[role]}, "SK": {"S": SK}}


def read_state(ddb, role):
    cons = ddb.get_item(TableName=TABLE, Key=key(role), ConsistentRead=True).get("Item") is not None
    gsi = ddb.query(TableName=TABLE, IndexName=INDEX, KeyConditionExpression="email = :e",
                    ExpressionAttributeValues={":e": {"S": EMAILS[role]}}, Select="COUNT")["Count"]
    return cons, gsi


def item_for(role, hashed):
    s = SPEC[role]
    return {
        "PK": {"S": "USER#" + EMAILS[role]}, "SK": {"S": SK}, "email": {"S": EMAILS[role]},
        "passwordHash": {"S": hashed}, "status": {"S": "active"}, "firmId": {"S": s["firm"]},
        "allowedFirmIds": {"L": [{"S": i} for i in s["ids"]]}, "role": {"S": "user"},
        "userType": {"S": "test-filer"}, "name": {"S": s["name"]},
        "exp": {"N": str(int(time.time()) + TTL_HOURS * 3600)},
    }


def ids_of(attr):
    if not isinstance(attr, dict) or set(attr) != {"L"}:
        return None
    return [e.get("S") for e in attr["L"]]


def word(e):
    resp = getattr(e, "response", None)
    return str((resp.get("Error") or {}).get("Code", "?")) if isinstance(resp, dict) else type(e).__name__


def mint_one(ddb, role, password):
    import bcrypt
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(COST)).decode("ascii")
    item = item_for(role, hashed)
    try:
        ddb.put_item(TableName=TABLE, Item=item, ConditionExpression="attribute_not_exists(PK)")
    except Exception as e:  # noqa: BLE001
        print("MINT-REFUSED %s %s" % (role, word(e)))
        return None
    row = ddb.get_item(TableName=TABLE, Key=key(role), ConsistentRead=True).get("Item") or {}
    ok = (row.get("status", {}).get("S") == "active" and row.get("firmId", {}).get("S") == SPEC[role]["firm"]
          and "passwordHash" in row and not any(k in row for k in ("mfaEnabled", "mfaChannel"))
          and ids_of(row.get("allowedFirmIds")) == SPEC[role]["ids"])
    q = ddb.query(TableName=TABLE, KeyConditionExpression="PK = :p", ExpressionAttributeValues={":p": {"S": "USER#" + EMAILS[role]}},
                  ConsistentRead=True, ProjectionExpression="SK")
    rows = sum(1 for it in (q.get("Items") or []) if (it.get("SK") or {}).get("S") != SK)
    got = ids_of(row.get("allowedFirmIds")) or []
    print("MINT-OK %s %s" % (role, "READBACK-OK" if ok and rows == 0 else "READBACK-BAD"))
    print("MINT-SCOPE %s allowedFirmIds=%s entitlement_rows=%d" % (role, ",".join(got), rows))
    return {"readback_ok": bool(ok and rows == 0), "scope_nonempty": bool(got), "covers_49f": "49financial" in got}


def sign_in(password, role):
    body = json.dumps({"email": EMAILS[role], "password": password}).encode("utf-8")
    req = urllib.request.Request(BASE + "/auth/login", data=body, method="POST",
                                 headers={"Content-Type": "application/json", "Accept": "application/json"})
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(req, timeout=30) as r:
            status, data = r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, None, []
    except OSError:
        return 0, None, []
    try:
        obj = json.loads(data.decode("utf-8"))
    except ValueError:
        return status, None, []
    tok = obj.get("accessToken") if isinstance(obj, dict) and obj.get("mfaRequired") is not True else None
    return status, tok if isinstance(tok, str) and tok else None, sorted(obj) if isinstance(obj, dict) else []


def remove_roles(ddb, roles):
    out = {}
    for role in roles:
        try:
            ddb.delete_item(TableName=TABLE, Key=key(role), ConditionExpression="attribute_exists(PK)")
            print("REMOVE-OK %s deleted" % role)
        except Exception as e:  # noqa: BLE001
            print("REMOVE-NOOP %s %s" % (role, word(e)))
    deadline = time.time() + 300
    while True:
        st = {r: read_state(ddb, r) for r in roles}
        if all(c is False and g == 0 for c, g in st.values()) or time.time() >= deadline:
            break
        time.sleep(10)
    for r, (c, g) in st.items():
        out[r] = {"gsi": "ABSENT" if g == 0 else "PRESENT", "consistent": "ABSENT" if not c else "PRESENT"}
        print("%s GSI %s" % (out[r]["gsi"], r))
        print("%s CONSISTENT %s" % (out[r]["consistent"], r))
    return out


def cmd_state():
    ddb = client()
    res = {}
    for r in ROLES:
        c, g = read_state(ddb, r)
        res[r] = {"gsi": "ABSENT" if g == 0 else "PRESENT", "consistent": "ABSENT" if not c else "PRESENT"}
        print("%s GSI %s" % (res[r]["gsi"], r))
        print("%s CONSISTENT %s" % (res[r]["consistent"], r))
    return 0 if all(v["gsi"] == v["consistent"] == "ABSENT" for v in res.values()) else 1


def cmd_pair():
    ddb = client()
    for r in ROLES:  # the gate is re-read here: a PRESENT row refuses the whole mint
        c, g = read_state(ddb, r)
        if c or g:
            print("PAIR-REFUSED %s not ABSENT" % r)
            return 1
    pw = {r: secrets.token_urlsafe(32) for r in ROLES}
    facts = {"principals": [], "mint": {}}
    minted = []
    for r in ROLES:
        got = mint_one(ddb, r, pw[r])
        if got is None:
            remove_roles(ddb, minted)
            return 1
        minted.append(r)
        facts["principals"].append({"role": r, "email_digest12": digest12(EMAILS[r]), "user_type": "test-filer",
                                    "firm": SPEC[r]["firm"], "class": SPEC[r]["klass"], **{k: got[k] for k in ("scope_nonempty", "covers_49f")}})
        facts["mint"][r] = got["readback_ok"]
    facts["mint_utc"] = utc()
    counts = [0, 0]
    deadline = time.time() + 120
    while time.time() < deadline:
        counts = [read_state(ddb, r)[1] for r in ROLES]
        if counts == [1, 1]:
            break
        time.sleep(10)
    facts["index_counts_after_mint"] = counts
    print("INDEX-COUNTS %s" % counts)
    if counts != [1, 1] or not all(facts["mint"].values()):
        save("pair_failed", facts)
        remove_roles(ddb, minted)
        return 1
    sess = {}
    facts["signin"] = {}
    for r in ROLES:
        status, tok, keys = sign_in(pw[r], r)
        facts["signin"][r] = {"http_status": status, "token_present": tok is not None, "response_keys": keys}
        print("SIGNIN %s status=%d token=%s" % (r, status, "yes" if tok else "no"))
        if tok:
            sess[r] = tok
    save("pair", facts)
    if len(sess) != 2:
        remove_roles(ddb, minted)
        return 1
    for r in ROLES:
        print("SESSION %s %s" % (r, sess[r]))
    return 0


def cmd_remove(args):
    roles = [a for a in args if a in ROLES] or list(ROLES)
    if any(a not in ROLES for a in args):
        print("REMOVE-REFUSED args")
        return 1
    res = remove_roles(client(), roles)
    return 0 if all(v["gsi"] == v["consistent"] == "ABSENT" for v in res.values()) else 1


def main(argv):
    if len(argv) >= 2 and argv[1] == "state":
        return cmd_state()
    if len(argv) >= 2 and argv[1] == "pair":
        return cmd_pair()
    if len(argv) >= 2 and argv[1] == "remove":
        return cmd_remove(argv[2:])
    print("USAGE vleg_pair_mint.py state | pair | remove [COVERING] [NON_COVERING]")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
