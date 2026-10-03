"""Ledger irpt-authorizer-series-render-20261003, leg P2 (CTO batch 227): a render token minted for account X, asking the
49F reporting SERIES route for account Y, is refused.

The render private key is read BY NAME from Secrets Manager (opal/auth/irpt-render-jwt-private-key, slot `current`) and is
never printed or written. The token is never printed or written: only its jti and the sha256 of the token string are.
X and Y are two distinct 49F accounts' opaque ids, minted by the ONE normalizer (_ids/ids.py opaque_account); only their last
4 characters are printed. The request goes through the public origin (CloudFront -> edge V3 -> API Gateway authorizer V2).

Usage: python auth_p2_foreign_token_probe.py <raw account X> <raw account Y>
Prints the HTTP status and the body's first 200 characters. PASS when the status is 403 (V2 refuses the id mismatch).
"""
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

import boto3

ROOT = Path(__file__).resolve().parents[8]
sys.path[:0] = [str(ROOT / "infra/aws/lambda/investor-reporting/_render_identity"),
                str(ROOT / "infra/aws/lambda/investor-reporting/_ids")]
import ids  # noqa: E402
import mint  # noqa: E402

FIRM = "49financial"
ORIGIN = "https://opalinvest.dev"


def main():
    raw_x, raw_y = sys.argv[1], sys.argv[2]
    x, y = ids.opaque_account(FIRM, raw_x), ids.opaque_account(FIRM, raw_y)
    if x == y:
        sys.exit("X and Y must differ")
    sec = boto3.client("secretsmanager").get_secret_value(SecretId="opal/auth/irpt-render-jwt-private-key")["SecretString"]
    try:
        pem = json.loads(sec)["current"]
    except (ValueError, KeyError, TypeError):
        pem = sec
    bundle = {"firm_id": FIRM, "bundle_id": "p2-foreign-probe", "revision": "p2", "account_set_id": x, "job_id": "p2",
              "report_id": "p2", "delegator_subject": "2.0.0_SA_COO~P"}
    res = mint.mint_render_token(bundle, private_key_pem=pem)
    del pem, sec
    print("minted jti=%s token_sha256=%s accountSetId=...%s exp-iat=%ds"
          % (res.jti, hashlib.sha256(res.token.encode()).hexdigest()[:16], x[-4:], res.exp - res.iat))
    url = ORIGIN + "/api/scoped/investor-reporting/reporting/%s/series" % y
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + res.token})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            status, body = r.status, r.read()[:200]
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read()[:200]
    print("GET .../reporting/...%s/series with the X token -> HTTP %d %s" % (y[-4:], status, body.decode("utf-8", "replace")))
    print("P2 %s" % ("PASS" if status == 403 else "FAIL"))


if __name__ == "__main__":
    main()
