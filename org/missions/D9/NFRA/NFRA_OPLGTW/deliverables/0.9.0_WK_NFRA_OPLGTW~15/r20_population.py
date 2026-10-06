"""OG-rl-8 Phase A: build the CURRENT principal population for the /login admit set (LG1_ADMIT_SET.md section 2). READ-ONLY: a consistent scan of
gateway-access-state-table (Scan only; no put/update/delete) and nothing else. Prints COUNTS, record-type names and key NAMES only -- never an email or a tid/oid.
usage: python r20_population.py <out population.json>   (the json carries emails: write it ONLY under .scratch and delete it after the admit-set run)
Sources, merged by (tid, oid):
  1. every RUNTIME#refresh# record (oauth_refresh_family) and every RUNTIME#code# record (oauth_code): tid, oid, email  -- persons who have signed in
  2. every POLICY#<tid>#<oid> principal_profile record (any status) -> profile true (catches profiles with no sign-in)
  3. email_denied: per email, the email_deny key (pk POLICY#EMAILDENY#<sha>) exists (a get_item per email)
  4. blocked: blocklist.enforce(email) raising AccessDenied (read in the gateway code by lg1_admit_set's caller; here recorded False unless the blocklist module is importable)
  5. the two server-held identities (OTP_MAILBOX, MS_INGEST_IDENTITY) with tid/oid null
"""
import collections
import json
import os
import sys

import boto3

sys.path.insert(0, os.environ.get("OG_GW_DIR", os.getcwd()))
os.environ.setdefault("MOCK_GRAPH", "1")
from app import access_state as acs  # noqa: E402  (the gateway's own key builders, never a hand-typed key)

TABLE = "gateway-access-state-table"
out = sys.argv[1]
ddb = boto3.client("dynamodb", region_name="us-east-1")
items = []
pages = 0
for page in ddb.get_paginator("scan").paginate(TableName=TABLE, ConsistentRead=True, ProjectionExpression="#p, #s, tid, oid, email, #st",
                                               ExpressionAttributeNames={"#p": "pk", "#s": "sk", "#st": "status"}):
    pages += 1
    items += page.get("Items", [])
print("SCAN pages %d items %d (table ItemCount is approximate)" % (pages, len(items)))
by = collections.Counter()
for it in items:
    pk, sk = it["pk"]["S"], it["sk"]["S"]
    ns = pk.split("#", 1)[0]
    by[(ns, pk.split("#")[1] if ns == "RUNTIME" else ("EMAILDENY" if pk.startswith("POLICY#EMAILDENY#") else ("TENANT" if pk.startswith("POLICY#TENANT#") else "principal")), sk.split("#")[0])] += 1
for k, v in sorted(by.items()):
    print("RECORD_TYPE", k, v)
ex = [it for it in items if it["sk"]["S"] == "oauth_refresh_family"]
if ex:
    print("ONE refresh-family record KEY NAMES:", sorted(ex[0].keys()))
exc = [it for it in items if it["sk"]["S"] == "oauth_code"]
if exc:
    print("ONE code record KEY NAMES:", sorted(exc[0].keys()))
people = {}   # (tid, oid) -> {email, profile}
src = collections.Counter()
for it in items:
    sk = it["sk"]["S"]
    if sk in ("oauth_refresh_family", "oauth_code") and "tid" in it and "oid" in it:
        key = (it["tid"]["S"], it["oid"]["S"])
        e = people.setdefault(key, {"email": "", "profile": False})
        em = it.get("email", {}).get("S", "")
        if em and not e["email"]:
            e["email"] = em
        src[sk] += 1
    elif sk == "principal_profile" and it["pk"]["S"].startswith("POLICY#") and it["pk"]["S"].count("#") == 2:
        _, tid, oid = it["pk"]["S"].split("#")
        e = people.setdefault((tid, oid), {"email": "", "profile": False})
        e["profile"] = True
        src["principal_profile"] += 1
print("SOURCE_COUNTS", dict(src), "distinct principals", len(people), "with an email", sum(1 for v in people.values() if v["email"]), "profile", sum(1 for v in people.values() if v["profile"]))
# 3. email_denied: the email_deny key per email (and the deny count overall, for the denominator)
emails = sorted(set(v["email"].strip().lower() for v in people.values() if v["email"]))
deny = {}
for em in emails:
    k = acs.email_deny_key(em)
    g = ddb.get_item(TableName=TABLE, Key={"pk": {"S": k.pk}, "sk": {"S": k.sk}}, ConsistentRead=True)
    deny[em] = "Item" in g
print("EMAILS distinct %d; email_deny record present for %d" % (len(emails), sum(deny.values())))
alldeny = sum(1 for it in items if it["pk"]["S"].startswith("POLICY#EMAILDENY#"))
print("EMAILDENY records in the table %d" % alldeny)
pop = []
for (tid, oid), v in sorted(people.items()):
    em = v["email"].strip().lower()
    pop.append({"tid": tid, "oid": oid, "email": em, "profile": v["profile"], "email_denied": bool(deny.get(em)), "blocked": False})
for em in ("andrew@opalinvest.com",):   # the server-held identities (OTP_MAILBOX = MS_INGEST_IDENTITY in the committed template)
    pop.append({"tid": None, "oid": None, "email": em, "profile": False, "email_denied": bool(deny.get(em, False)), "blocked": False})
no_email = [p for p in pop if not p["email"]]
print("POPULATION %d; with no email %d (refused no_identity by the rule; the access layer would not admit them either)" % (len(pop), len(no_email)))
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(pop, fh)
print("written (scratch only; delete after use)")
