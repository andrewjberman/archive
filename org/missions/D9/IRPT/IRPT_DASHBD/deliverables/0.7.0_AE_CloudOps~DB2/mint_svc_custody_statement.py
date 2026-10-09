"""Leg M of IRPT_DASHBD.TO-DB-b-84: mint the svc-custody-statement service token.

Under the signed never-widen pair (COO half AMENDMENT 2 @a319fc74b8, CTO half msg 2440).

The signing key is read from Secrets Manager into memory only. It is never printed, never
written and never passed through argv. The minted token is handed straight to CreateSecret
in-process for the same reason: a --secret-string on a command line would put a live bearer
credential into process arguments. Nothing this script prints contains key material, the
token, or its signature.

Usage:
    python mint_svc_custody_statement.py            # dry run: mint + validate claims, no AWS write
    python mint_svc_custody_statement.py --go       # also CreateSecret (the one irreversible act)
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys

import boto3
import jwt
from botocore.exceptions import ClientError

REGION = "us-east-1"
SIGNING_SECRET = "opal/auth/jwt-private-key"
TARGET_SECRET = "opal/investor-reporting/svc-custody-statement"
MINTED_BY = "0.7.0_AE_CloudOps~DB2"
TTL_DAYS = 90
ROTATE_LEAD_DAYS = 14

# Pair section 1, exactly. Anything not here is ABSENT by construction.
REQUIRED_CLAIMS = {
    "sub": "svc-custody-statement",
    "name": "svc-custody-statement",
    "userType": "service",
    "tier": "service",
    "firmId": "cottonwood",
    "iss": "opal-portal-auth",
    "aud": "opal-portal-api",
}
FORBIDDEN_CLAIMS = ("role", "advisorId", "allowedPages", "allowedTabs", "firmRole")


def build_claims(now):
    iat = int(now.timestamp())
    exp = int((now + dt.timedelta(days=TTL_DAYS)).timestamp())
    claims = dict(REQUIRED_CLAIMS)
    claims["iat"] = iat
    claims["exp"] = exp
    return claims


def verify_claims(token):
    """Decode WITHOUT verifying (pair section 3 step 3) and refuse any drift."""
    decoded = jwt.decode(
        token,
        options={"verify_signature": False, "verify_aud": False, "verify_exp": False},
        algorithms=["RS256"],
    )
    for key, want in REQUIRED_CLAIMS.items():
        got = decoded.get(key)
        if got != want:
            raise SystemExit("CLAIM MISMATCH: %s is %r, pair says %r" % (key, got, want))
    present = [c for c in FORBIDDEN_CLAIMS if c in decoded]
    if present:
        raise SystemExit("FORBIDDEN CLAIM PRESENT: %s" % ", ".join(present))
    ttl = decoded["exp"] - decoded["iat"]
    if ttl <= 0 or ttl > TTL_DAYS * 86400:
        raise SystemExit("TTL OUT OF BOUND: exp-iat is %s s, cap is %s s" % (ttl, TTL_DAYS * 86400))
    extra = sorted(set(decoded) - set(REQUIRED_CLAIMS) - {"iat", "exp"})
    if extra:
        raise SystemExit("UNEXPECTED CLAIM(S): %s" % ", ".join(extra))
    header = jwt.get_unverified_header(token)
    if header.get("alg") != "RS256":
        raise SystemExit("ALG IS NOT RS256: %r" % header.get("alg"))
    return decoded, ttl, header


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--go", action="store_true", help="also create the secret")
    args = ap.parse_args()

    sm = boto3.client("secretsmanager", region_name=REGION)

    # Fail closed if the target already exists, re-read at the apply itself.
    try:
        sm.describe_secret(SecretId=TARGET_SECRET)
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ResourceNotFoundException":
            raise
    else:
        raise SystemExit("REFUSED: %s already exists -- this order mints once." % TARGET_SECRET)

    key_read = sm.get_secret_value(SecretId=SIGNING_SECRET)
    private_key = key_read["SecretString"]  # memory only
    now = dt.datetime.now(dt.timezone.utc)
    claims = build_claims(now)
    token = jwt.encode(claims, private_key, algorithm="RS256")
    del private_key
    if isinstance(token, bytes):  # PyJWT < 2 returns bytes
        token = token.decode("ascii")

    decoded, ttl, header = verify_claims(token)
    exp_at = dt.datetime.fromtimestamp(decoded["exp"], dt.timezone.utc)
    rotate_by = exp_at - dt.timedelta(days=ROTATE_LEAD_DAYS)

    out = {
        "signing_key_read": {
            "secret_name": SIGNING_SECRET,
            "version_id": key_read["VersionId"],
            "version_stages": key_read.get("VersionStages"),
            "run": "leg M of IRPT_DASHBD.TO-DB-b-84",
            "claim": "measured",
        },
        "header": header,
        "claims": decoded,
        "ttl_days": ttl / 86400.0,
        "exp_utc": exp_at.isoformat(),
        "rotate_by_utc": rotate_by.isoformat(),
        "forbidden_claims_absent": list(FORBIDDEN_CLAIMS),
        "token_written_anywhere": False,
    }

    if not args.go:
        out["mode"] = "DRY-RUN -- claims validated, nothing created, token discarded"
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0

    description = (
        "svc-custody-statement service token. ONE use: the IRPT Performance client statement "
        "submission and persist routes (POST /api/scoped/investor-reporting/custody-report, "
        "POST /analysis, POST /export). Firm cottonwood ONLY -- the firm comes from the verified "
        "claim and never from a request field. TTL %d days, exp %s, ROTATE BY %s (14 days before "
        "exp; rotation owner 2.0.0_SA_COO~D2). Minted by %s under the signed never-widen pair "
        "(COO half AMENDMENT 2 @a319fc74b8, CTO half msg 2440) for TO-DB-b-84. The real control is "
        "the code admission IB-pr-385: rolling it back disarms this token everywhere."
        % (TTL_DAYS, exp_at.isoformat(), rotate_by.isoformat(), MINTED_BY)
    )
    payload = json.dumps(
        {
            "token": token,
            "sub": decoded["sub"],
            "exp": decoded["exp"],
            "minted_by": MINTED_BY,
        }
    )
    created = sm.create_secret(
        Name=TARGET_SECRET,
        Description=description,
        SecretString=payload,
    )
    del token, payload

    out["mode"] = "CREATED"
    out["secret"] = {
        "name": created["Name"],
        "arn": created["ARN"],
        "version_id": created["VersionId"],
    }
    out["description_set"] = description
    out["secret_value_fields"] = ["token", "sub", "exp", "minted_by"]
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
