"""Mint ONE RS256 service token for svc-irpt-packager and store it as ONE secret. ASCII only.
The token lives in memory only: it is never printed, written to disk or logged. Prints claim NAMES, the expiry date,
and the secret's name, ARN and dates. usage: mint_packager.py [--go]   (no --go = checks only, creates nothing)
Method: the sibling's (TCKT_VNEXT F10 leg M): signing key = bare PEM at opal/auth/jwt-private-key (current slot), claims
sub/userType/tier/name/iss/aud/iat/exp and no others. The ticket authorizer sets actor.email from the `sub` claim
(infra/aws/users/lambda/portal-authorizer/index.mjs:387,398), so sub IS the email the door reads."""
import datetime as dt
import json
import sys
import time

import boto3
import jwt as pyjwt
from botocore.exceptions import ClientError

REGION = "us-east-1"
SUBJECT = "svc-irpt-packager"
SECRET = "opal/ticketing/svc-irpt-packager"
KEY_SECRET = "opal/auth/jwt-private-key"
DAYS = 90
ALLOWED = {"sub", "userType", "tier", "name", "iss", "aud", "iat", "exp"}
sm = boto3.client("secretsmanager", region_name=REGION)

try:
    sm.describe_secret(SecretId=SECRET)
    print("STOP: %s already exists" % SECRET)
    sys.exit(2)
except ClientError as e:
    if e.response["Error"]["Code"] != "ResourceNotFoundException":
        print("STOP: describe-secret answered", e.response["Error"]["Code"])
        sys.exit(2)
print("OK: before-read ResourceNotFoundException for", SECRET)

pem = sm.get_secret_value(SecretId=KEY_SECRET)["SecretString"]
if not pem.lstrip().startswith("-----BEGIN"):
    print("STOP: the signing secret is not a bare PEM; the sibling's method does not apply as written")
    sys.exit(3)
iat = int(time.time())
exp = iat + DAYS * 86400
claims = {"sub": SUBJECT, "userType": "service", "tier": "service", "name": SUBJECT,
          "iss": "opal-portal-auth", "aud": "opal-portal-api", "iat": iat, "exp": exp}
token = pyjwt.encode(claims, pem, algorithm="RS256")
del pem

back = pyjwt.decode(token, options={"verify_signature": False})
names = sorted(back)
bad = []
if set(names) != ALLOWED:
    bad.append("claim names %s" % names)
if back.get("sub") != SUBJECT or back.get("userType") != "service":
    bad.append("sub/userType do not read as the door reads them")
if back["exp"] - back["iat"] > DAYS * 86400:
    bad.append("exp - iat over 90d")
for absent in ("firmId", "role", "advisorId", "allowedPages", "allowedTabs", "firmRole", "email"):
    if absent in back:
        bad.append("unexpected claim " + absent)
iso = lambda t: dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")  # noqa: E731
print("claim names:", names)
print("sub/userType as the door reads them: %s / %s" % (back["sub"], back["userType"]))
print("iat %s  exp %s  lifetime days %d" % (iso(back["iat"]), iso(back["exp"]), (back["exp"] - back["iat"]) // 86400))
if bad:
    print("STOP (nothing created):", bad)
    sys.exit(4)
if "--go" not in sys.argv:
    print("CHECK ONLY: nothing created")
    sys.exit(0)

minted, rotate = iso(iat)[:10], iso(exp - 14 * 86400)[:10]
desc = ("svc-irpt-packager service token for the IRPT packager door (ticket_center package route); sub %s, userType "
        "service, NO firm claim. RS256 iss=opal-portal-auth aud=opal-portal-api. TTL 90d minted %s, rotate by %s, "
        "expires %s. Consumer reads .token. Minted 0.7.0_AE_CloudOps~ANL under crossbox XB-20261011T163203Z-3fc2."
        % (SUBJECT, minted, rotate, iso(exp)[:10]))
value = json.dumps({"token": token, "sub": SUBJECT, "exp": iso(exp), "minted_by": "0.7.0_AE_CloudOps~ANL"})
r = sm.create_secret(Name=SECRET, Description=desc, SecretString=value)
del value, token
d = sm.describe_secret(SecretId=SECRET)
print("OK: secret created: name=%s arn=%s" % (d["Name"], d["ARN"]))
print("created=%s last_changed=%s" % (d["CreatedDate"].isoformat(), d["LastChangedDate"].isoformat()))
print("description=%s" % d["Description"])
