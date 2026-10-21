# ruff: noqa
# OG-rl-18 Phase A probe, the python of ed1.AC1.sh VERBATIM (extracted by rl18_probes_extract.py); run by rl18_host.py in a fresh guarded process with the stage as the gateway folder.
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
