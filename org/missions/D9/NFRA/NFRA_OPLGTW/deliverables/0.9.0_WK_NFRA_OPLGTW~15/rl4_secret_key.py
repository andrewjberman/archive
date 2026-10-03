"""OG-rl-4 PHASE B step 13: add taxsma_workbook_identity to gateway/principals/rosters. Never prints a value or a hash of one.

usage: python rl4_secret_key.py read     # in-memory read: key names, value types, whether the new key exists; no write
       python rl4_secret_key.py apply    # read, add the key, put-secret-value, re-read AWSCURRENT, prove every pre-existing key unchanged

The value is the step-9 identity export (rl4_identity.py's identity(): part_d_20260930.json), whose sha256 rl4_identity.py check
proves equal, host-side, to the host's current TAXSMA_WORKBOOK_IDENTITY. The secret string never touches disk or argv (boto3)."""
import hashlib
import json
import os
import re
import sys

import boto3

SECRET = "gateway/principals/rosters"
NEW = "taxsma_workbook_identity"
PAIR = re.compile(r"[0-9a-fA-F-]{36}/[0-9a-fA-F-]{36}")
PARTD = os.path.join(os.environ["LOCALAPPDATA"], "opal", "og-principals", "part_d_20260930.json")


def h(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def identity():
    v = json.load(open(PARTD, encoding="utf-8"))["values"]
    return v["tenant_id"] + "/" + v["opalbloomberg@opalinvest.com"]


def main():
    mode = sys.argv[1]
    sm = boto3.session.Session(region_name="us-east-1").client("secretsmanager")
    cur = sm.get_secret_value(SecretId=SECRET, VersionStage="AWSCURRENT")
    before_vid = cur["VersionId"]
    d = json.loads(cur["SecretString"])
    before = {k: h(json.dumps(v, sort_keys=True)) for k, v in d.items()}
    print("READ version %s... keys %d %s" % (before_vid[:8], len(d), sorted(d)))
    print("TYPES %s" % {k: type(v).__name__ for k, v in d.items()})
    print("NEW KEY %s present before: %s" % (NEW, NEW in d))
    ident = identity()
    print("IDENTITY pair-regex match: %s" % bool(PAIR.fullmatch(ident)))
    if mode == "read":
        return 0
    if NEW in d:
        print("REFUSED: %s already present; not overwriting" % NEW)
        return 3
    if not PAIR.fullmatch(ident):
        print("REFUSED: identity export is not one <tid>/<oid> pair")
        return 3
    d[NEW] = ident
    r = sm.put_secret_value(SecretId=SECRET, SecretString=json.dumps(d))
    print("PUT new version %s... stages %s" % (r["VersionId"][:8], r.get("VersionStages")))
    after = sm.get_secret_value(SecretId=SECRET, VersionStage="AWSCURRENT")
    a = json.loads(after["SecretString"])
    prev = sm.get_secret_value(SecretId=SECRET, VersionStage="AWSPREVIOUS")
    print("AWSCURRENT %s... == put: %s; AWSPREVIOUS %s... == before: %s" % (
        after["VersionId"][:8], after["VersionId"] == r["VersionId"], prev["VersionId"][:8], prev["VersionId"] == before_vid))
    unchanged = [k for k in before if k in a and h(json.dumps(a[k], sort_keys=True)) == before[k]]
    print("PRE-EXISTING KEYS value hash unchanged %d of %d; missing after %d" % (len(unchanged), len(before), len([k for k in before if k not in a])))
    print("KEYS after %d %s" % (len(a), sorted(a)))
    ok_new = isinstance(a.get(NEW), str) and h(a[NEW]) == h(ident) and bool(PAIR.fullmatch(a[NEW]))
    print("NEW KEY sha256 == identity export sha256 (rl4_identity.py check proves == host): %s" % ("MATCH" if ok_new else "DIFFER"))
    ok = ok_new and len(unchanged) == len(before) and len(a) == len(before) + 1
    print("STEP13 RESULT: %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


sys.exit(main())
