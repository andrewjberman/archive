# ruff: noqa
# OG-rl-18 Phase A probe, the python of rt1.AC1.sh VERBATIM (extracted by rl18_probes_extract.py); run by rl18_host.py in a fresh guarded process with the stage as the gateway folder.
import sys
sys.path.insert(0, ".")
ok = True
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app import data_entitlement as de
    from ops import schwab_entitlement_admin as adm
except Exception as exc:
    print("import failed: %s %s" % (type(exc).__name__, str(exc)[:100])); print("NO"); sys.exit(0)
M1, M2 = "08242234", "08335338"
def raw(accts):
    return {"masters": sorted(accts), "datasets": ["dim_position"], "accounts": accts, "dates": {"mode": "rolling_complete_window"},
            "columns": {"dim_position": ["symbol"]}, "operations": ["list", "describe", "query"]}
def parse(accts):
    try:
        return de.parse_scope(raw(accts))
    except de.Malformed as exc:
        return exc
s = parse({M1: ["70412358", "70412359"], M2: ["*"]})
say("accepted: one master explicit, one master-wide", isinstance(s, de.Scope), type(s).__name__)
if isinstance(s, de.Scope):
    say("is_master_wide: true for the wildcard master, false for the explicit one", hasattr(de, "is_master_wide") and de.is_master_wide(s, M2) is True and de.is_master_wide(s, M1) is False)
    say("the sentinel is frozenset({'*'}) in Scope.accounts", s.accounts[M2] == frozenset({"*"}) and s.accounts[M1] == frozenset({"70412358", "70412359"}))
    req = {"operation": "query", "master": M2, "dataset": "dim_position", "account_ids": ["70412358", "99999999"]}
    say("check_scope: any well-formed account ids are in scope for the master-wide master", de.check_scope(s, req) == [], "failures %r" % (de.check_scope(s, req),))
    req1 = dict(req, master=M1, account_ids=["70412358", "99999999"])
    f1 = de.check_scope(s, req1)
    say("check_scope: an id outside an explicit list is still refused", len(f1) == 1 and f1[0][0] == "accounts", "failures %r" % (f1,))
    back = adm._scope_to_raw(s)
    say("_scope_to_raw round-trips the sentinel", back["accounts"][M2] == ["*"] and back["accounts"][M1] == ["70412358", "70412359"], "accounts %r" % (back["accounts"],))
    old = parse({M1: ["70412358"], M2: ["70412358", "70412359", "70412360"]})
    diff = adm.scope_diff(old, s)
    d2 = diff["accounts"][M2]
    say("scope_diff: from a list to '*' reads added ['*'] and the old ids removed", d2["added"] == ["*"] and d2["removed"] == ["70412358", "70412359", "70412360"], "diff %r" % (d2,))
mixed = parse({M1: ["70412358"], M2: ["*", "70412358"]})
say("refused: '*' mixed with an id", isinstance(mixed, de.Malformed), type(mixed).__name__)
empty = parse({M1: ["70412358"], M2: []})
say("refused: an empty list", isinstance(empty, de.Malformed), type(empty).__name__)
ungranted_raw = raw({M1: ["70412358"]})
ungranted_raw["accounts"][M2] = ["*"]
try:
    de.parse_scope(ungranted_raw); u = "accepted"
except de.Malformed:
    u = "refused"
say("refused: a '*' key for a master that is not granted", u == "refused", u)
star_str = parse({M1: ["70412358"], M2: "*"})
say("refused: the bare string '*' (not a one-element list)", isinstance(star_str, de.Malformed), type(star_str).__name__)
print("OK" if ok else "NO")
