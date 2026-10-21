# ruff: noqa
# OG-rl-18 Phase A probe, the python of rt1.AC2.sh VERBATIM (extracted by rl18_probes_extract.py); run by rl18_host.py in a fresh guarded process with the stage as the gateway folder.
import sys, re, inspect
sys.path.insert(0, ".")
ok = True
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app import data_entitlement as de, account_ref as ar
    from app.integrations.schwab import integration as si
except Exception as exc:
    print("import failed: %s %s" % (type(exc).__name__, str(exc)[:100])); print("NO"); sys.exit(0)
M1, M2 = "08242234", "08335338"
raw = {"masters": [M1, M2], "datasets": ["dim_position"], "accounts": {M1: ["70412358", "70412359"], M2: ["*"]},
       "dates": {"mode": "rolling_complete_window"}, "columns": {"dim_position": ["symbol"]}, "operations": ["list", "describe", "query"]}
try:
    scope = de.parse_scope(raw)
except Exception as exc:
    print("the master-wide scope does not parse (%s): run AC1 first" % type(exc).__name__); print("NO"); sys.exit(0)
f = getattr(si, "account_filter_for", None)
say("account_filter_for exists", callable(f))
if callable(f):
    say("account_filter_for: None for the master-wide master", f(scope, M2) is None, "got %r" % (f(scope, M2),))
    say("account_filter_for: the sorted tuple for the explicit master", f(scope, M1) == ("70412358", "70412359"), "got %r" % (f(scope, M1),))
cnt = si.scope_summary(scope).get("account_count", {})
say("scope_summary account_count: 'all' for the master-wide master, 2 for the explicit one", cnt.get(M2) == "all" and cnt.get(M1) == 2, "got %r" % (cnt,))
src = inspect.getsource(si)
raw_uses = len(re.findall(r"scope\.accounts\.get\(", src))
say("raw scope.accounts.get( uses left in the schwab integration: at most 2", raw_uses <= 2, "%d" % raw_uses)
ca = getattr(ar, "candidate_accounts", None)
say("account_ref.candidate_accounts and AccountsUnavailable exist", callable(ca) and hasattr(ar, "AccountsUnavailable"))
if callable(ca) and hasattr(ar, "AccountsUnavailable"):
    calls = []
    def provider(master):
        calls.append(master)
        return ["70412360", "70412358", "70412358"]
    say("explicit master: the explicit set, provider not called", ca(scope, M1, provider) == ["70412358", "70412359"] and calls == [], "calls %r" % (calls,))
    say("master-wide master: the provider's ids, sorted and de-duplicated", ca(scope, M2, provider) == ["70412358", "70412360"] and calls == [M2], "calls %r" % (calls,))
    try:
        ca(scope, M2, None); n = "returned"
    except ar.AccountsUnavailable:
        n = "AccountsUnavailable"
    say("master-wide master without a provider: AccountsUnavailable", n == "AccountsUnavailable", n)
    def boom(master):
        raise OSError("down")
    try:
        ca(scope, M2, boom); b = "returned"
    except ar.AccountsUnavailable:
        b = "AccountsUnavailable"
    say("a provider that raises: AccountsUnavailable", b == "AccountsUnavailable", b)
    sig = inspect.signature(ar.resolve_refs)
    say("resolve_refs takes accounts_of=None", "accounts_of" in sig.parameters and sig.parameters["accounts_of"].default is None)
print("OK" if ok else "NO")
