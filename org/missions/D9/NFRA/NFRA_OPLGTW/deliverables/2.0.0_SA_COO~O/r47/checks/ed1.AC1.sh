#!/usr/bin/env bash
# OPLGTW OG-ed-1 AC1 (round 47; the CTO half of OG-gv-1, email_deny option 2, msg 36207): the legacy /callback consent branch exempts the MASTER-ADMIN tier from the email deny record, and nobody else.
# One fresh process, MOCK_GRAPH=1, the in-memory fake table of tests/test_email_deny.py. Arms (ADMIN is the one master admin the roster names, NON_ADMIN has a deny record too):
#  (a) email_denial(ADMIN, route_class="consent") is None with an active deny record, and the fake store records ZERO reads;  (b) email_denial(NON_ADMIN, route_class="consent") == 403 and the record was read;
#  (c) the same non-admin on an unreadable store == 503;  (d) email_denial(ADMIN) with no class == 403 (today's verdict kept);  (e) a lookalike of the admin on class "consent" == 403;
#  (f) token_broker.redeem_consent for ADMIN with a deny record returns the principal (no EmailDenied) and for NON_ADMIN raises EmailDenied(403)  [_exchange_code, verify_upstream_id_token, oidc_nonce, _consent_scope_list, _write_cache, _principal_owner, _email_owner stubbed].
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
G=infra/aws/ec2/opal-gateway
res=$(MOCK_GRAPH=1 python3 -I - "$(native "$G")" <<'PYEOF'
import importlib, os, sys, types
G = sys.argv[1]
sys.path.insert(0, G); sys.path.insert(0, os.path.join(G, "tests"))
os.environ["MOCK_GRAPH"] = "1"
from botocore.exceptions import EndpointConnectionError
from test_email_deny import _FakeTable, _seed_deny
de = importlib.import_module("app.data_entitlement"); acs = importlib.import_module("app.access_state")
tb = importlib.import_module("app.token_broker"); cfg = importlib.import_module("app.config").get_config()
cfg.MOCK_GRAPH = True
ADMIN, NON_ADMIN, LOOK = "andrew@opalinvest.com", "alyssa@opalinvest.com", "xandrew@opalinvest.com"
cfg.MASTER_ADMIN_EMAILS = (ADMIN,)


def store(deny=None, error=None):
    t = _FakeTable(error=error); s = acs.AccessState(client=t)
    if deny is not None:
        _seed_deny(s, deny); t.calls.clear()
    return s, t


def reads(t):
    return sum(1 for n, _ in t.calls if n == "get_item")


ok = True


def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NOT OK", (" (%s)" % extra) if extra else ""))


def verdict(*a, **k):
    try:
        return de.email_denial(*a, **k)
    except Exception as e:
        return "raised %s" % type(e).__name__


s, t = store(ADMIN)
say("a master admin with an active deny record, class consent: not denied, store reads 0", verdict(ADMIN, store=s, route_class="consent") is None and reads(t) == 0, "got %r reads %d" % (verdict(ADMIN, store=s, route_class="consent"), reads(t)))
s, t = store(NON_ADMIN)
say("a non-admin with a deny record, class consent: 403 and the record was read", verdict(NON_ADMIN, store=s, route_class="consent") == 403 and reads(t) >= 1)
bad, _ = store(error=EndpointConnectionError(endpoint_url="https://dynamodb.us-east-1.amazonaws.com/"))
say("a non-admin on an unreadable store, class consent: 503", verdict(NON_ADMIN, store=bad, route_class="consent") == 503)
s, t = store(ADMIN)
say("the master admin with NO class keeps today's verdict: 403", verdict(ADMIN, store=s) == 403)
s, t = store(LOOK)
say("a lookalike of the admin, class consent: 403", verdict(LOOK, store=s, route_class="consent") == 403)

# (f) redeem_consent: the SECOND check on the validated principal
caches = []
tb.oidc_nonce = lambda state: "n"
tb._consent_scope_list = lambda email: []
tb._exchange_code = lambda code, scopes, nonce: ({"id_token": "x"}, types.SimpleNamespace(serialize=lambda: "c"))
tb._write_cache = lambda owner, blob: caches.append(owner)
tb._principal_owner = lambda p: "p:" + p.email
tb._email_owner = lambda e: "e:" + e
for who, want in ((ADMIN, "returns"), (NON_ADMIN, "denied")):
    s, t = store(who)
    acs._default = s
    tb.verify_upstream_id_token = lambda tok, nonce, w=who: types.SimpleNamespace(email=w, key="k")
    try:
        p = tb.redeem_consent(who, "code", "state"); got = "returns" if p.email == who else "wrong"
    except tb.EmailDenied as e:
        got = "denied" if getattr(e, "status", None) == 403 else "denied-other"
    except Exception as e:
        got = "raised %s" % type(e).__name__
    say("redeem_consent for the %s with a deny record %s" % ("master admin" if who == ADMIN else "non-admin", want), got == want, "got %s" % got)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
