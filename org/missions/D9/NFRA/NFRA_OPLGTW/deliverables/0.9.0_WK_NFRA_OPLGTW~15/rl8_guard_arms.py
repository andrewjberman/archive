"""OG-rl-6 PHASE C-A2 (A4): the FOUR acceptance arms of /yearinreview driven through the REAL stack of the release tree
(GuardMiddleware -> get_user_email in IDENTITY_PROVIDER=alb_oidc -> yearinreview_view), not only the handler.

usage: python rl8_guard_arms.py <gateway dir> owner|empty|missing
  owner   YEARINREVIEW_VIEW_ALLOWED_EMAILS=andrew@opalinvest.com : owner (ALB-signed) 200 + page bytes; a verified non-owner tenant identity 403 and no page bytes;
          a PLANTED non-ALB-signed identity header 401; no identity 401.
  empty   the key set to the empty string : even the verified owner is 403 (fail closed).
  missing the key absent from the environment : even the verified owner is 403 (fail closed).

The "ALB" here is a locally generated ES256 key pair: identity._fetch_elb_public_key is pointed at the local public key (no network), so a token signed by the
local private key is the ALB-signed identity and a token with a garbage signature (the planted one) fails the SAME signature check the host runs. The
deny-list read (_email_denied) and the audit write are replaced by no-ops: this proves ROUTING, IDENTITY and the ROSTER, nothing else. Runs on the release
tree in a throwaway process; writes nothing.
"""
import base64
import json
import os
import sys

gw = sys.argv[1]
mode = sys.argv[2]
sys.path.insert(0, gw)
os.environ["MOCK_GRAPH"] = "1"
os.environ["IDENTITY_PROVIDER"] = "alb_oidc"
os.environ["RATE_LIMIT_ENABLED"] = "0"
os.environ.pop("YEARINREVIEW_VIEW_ALLOWED_EMAILS", None)
if mode == "owner":
    os.environ["YEARINREVIEW_VIEW_ALLOWED_EMAILS"] = "andrew@opalinvest.com"
elif mode == "empty":
    os.environ["YEARINREVIEW_VIEW_ALLOWED_EMAILS"] = ""
elif mode != "missing":
    raise SystemExit("mode must be owner|empty|missing")

import jwt                                                       # noqa: E402
from cryptography.hazmat.primitives import serialization        # noqa: E402
from cryptography.hazmat.primitives.asymmetric import ec        # noqa: E402
from starlette.testclient import TestClient                      # noqa: E402

from app import identity, server, yearinreview_view              # noqa: E402

key = ec.generate_private_key(ec.SECP256R1())
pub_pem = key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()
priv_pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption())
identity._fetch_elb_public_key = lambda kid: pub_pem            # the "regional ELB key"


async def _no_deny(email):
    return None


server._email_denied = _no_deny
audit_lines = []
yearinreview_view.audit.log_call = lambda *a, **k: audit_lines.append((a, k))


def signed(email):
    return jwt.encode({"email": email, "sub": "local"}, priv_pem, algorithm="ES256", headers={"kid": "local-kid"})


def planted(email):
    def b(d):
        return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return b({"alg": "ES256", "typ": "JWT", "kid": "local-kid"}) + "." + b({"email": email, "sub": "planted"}) + "." + base64.urlsafe_b64encode(bytes(64)).decode().rstrip("=")


client = TestClient(server.app, raise_server_exceptions=False)
PAGE = b"Opal Year One Review"
rows = []


def arm(name, headers, want_code, page_expected):
    r = client.get("/yearinreview", headers=headers, follow_redirects=False)
    has_page = PAGE in r.content
    ok = r.status_code == want_code and has_page == page_expected
    rows.append(ok)
    print("%s %s: code %s (want %s), page bytes %s (want %s)" % ("PASS" if ok else "FAIL", name, r.status_code, want_code, has_page, page_expected))


OWNER, OTHER = "andrew@opalinvest.com", "viewer@opalinvest.com"
if mode == "owner":
    arm("owner, ALB-signed, on the roster", {"x-amzn-oidc-data": signed(OWNER)}, 200, True)
    n = len(audit_lines)
    arm("verified tenant non-owner, not on the roster", {"x-amzn-oidc-data": signed(OTHER)}, 403, False)
    denied = audit_lines[n:] and audit_lines[n][0][-2:] == ("denied", "roster")
    rows.append(bool(denied))
    print("%s non-owner denial is audit-logged DENIED / roster: %s" % ("PASS" if denied else "FAIL", denied))
    arm("planted non-ALB-signed identity naming the owner", {"x-amzn-oidc-data": planted(OWNER), "X-User-Email": OWNER}, 401, False)
    arm("no identity", {}, 401, False)
else:
    arm("verified OWNER with the roster %s" % ("empty" if mode == "empty" else "missing"), {"x-amzn-oidc-data": signed(OWNER)}, 403, False)
    arm("verified non-owner with the roster %s" % mode, {"x-amzn-oidc-data": signed(OTHER)}, 403, False)
    arm("no identity", {}, 401, False)
print("ARMS %s: %d of %d  RESULT: %s" % (mode, sum(rows), len(rows), "PASS" if all(rows) else "FAIL"))
sys.exit(0 if all(rows) else 1)
