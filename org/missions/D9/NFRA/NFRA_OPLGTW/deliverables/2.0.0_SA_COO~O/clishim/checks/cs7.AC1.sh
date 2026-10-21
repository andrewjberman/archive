#!/usr/bin/env bash
# OPLGTW OG-cs-7 AC1 (cli-shim workstream, wave 3): app/client_grant.py, the per-firm client grant decision (a pure function). One fresh process, no AWS, no network.
#   CLIENT_NAMESPACE == "opal-clients"; client_entry(vendor, firm="") -> "opal-clients/<vendor>/<firm>" | "opal-clients/<vendor>" | "opal-clients";
#   client_pair_decision(is_master_admin, is_opal, rec, vendor, firm) -> (allowed: bool, reason: str).
#  Rules, in order: vendor and firm are each ^[a-z0-9]{2,32}$ (else refused, reason names the field); an Opal principal; a LIVE record's channels_deny entry that covers the pair (deny wins, the master admin included); the master admin; a LIVE record's channels_allow entry that covers the pair.
#  An entry covers a pair when it is the namespace alone (every pair), the namespace and the vendor (every firm of that vendor) or the namespace, vendor and firm (that pair only). Folder entries of the three served buckets cover nothing here, and a client entry covers nothing in folder_grant.folder_decision (the namespace is not a served bucket).
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import os, sys
G = sys.argv[1]
sys.path.insert(0, G)
os.environ["MOCK_GRAPH"] = "1"
import warnings
warnings.simplefilter("ignore")
ok = True


def say(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%s: %s" % (label, "ok" if cond else "NOT OK"))


try:
    from app import data_entitlement as de, folder_grant as fg, client_grant as cg
except Exception as exc:  # noqa: BLE001
    print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
    print("NO")
    sys.exit(0)


def rec(allow=(), deny=(), status="active", stopped=False):
    return de.PersonAccess(status, 3, stopped, frozenset(), frozenset(), frozenset(allow), frozenset(deny))


def dec(admin, opal, r, v, f):
    try:
        a, why = cg.client_pair_decision(admin, opal, r, v, f)
        return bool(a), why
    except Exception as exc:  # noqa: BLE001
        return None, "%s: %s" % (type(exc).__name__, str(exc)[:60])


say("the namespace and the entry builder (%s | %s | %s)" % (cg.client_entry("orion", "49financial"), cg.client_entry("orion"), cg.client_entry("")) if hasattr(cg, "client_entry") else "client_entry absent",
    getattr(cg, "CLIENT_NAMESPACE", None) == "opal-clients" and cg.client_entry("orion", "49financial") == "opal-clients/orion/49financial" and cg.client_entry("orion") == "opal-clients/orion")
ents = [cg.client_entry("orion", "49financial"), cg.client_entry("orion"), "opal-clients"]
say("every client entry is accepted by the person-access entry parser", all(de._CHANNEL_OR_FOLDER.match(e) for e in ents))
pair = rec(allow=[cg.client_entry("orion", "49financial")])
say("a pair entry admits that (vendor, firm) only", dec(False, True, pair, "orion", "49financial")[0] is True and dec(False, True, pair, "orion", "cottonwood")[0] is False and dec(False, True, pair, "schwab", "49financial")[0] is False)
ven = rec(allow=[cg.client_entry("orion")])
say("a vendor entry admits every firm of that vendor and no other vendor", dec(False, True, ven, "orion", "cottonwood")[0] is True and dec(False, True, ven, "schwab", "cottonwood")[0] is False)
say("the namespace alone admits every pair", dec(False, True, rec(allow=["opal-clients"]), "smartx", "eclipse")[0] is True)
dn = rec(allow=[cg.client_entry("orion")], deny=[cg.client_entry("orion", "cottonwood")])
say("deny wins: a denied pair is refused under a vendor grant, a sibling firm is not", dec(False, True, dn, "orion", "cottonwood")[0] is False and dec(False, True, dn, "orion", "49financial")[0] is True)
say("the master admin is admitted with no record and refused only by a live deny", dec(True, True, None, "orion", "49financial")[0] is True and dec(True, True, rec(deny=[cg.client_entry("orion")]), "orion", "49financial")[0] is False)
say("no record, a stopped record, a revoked record and a non-Opal caller are refused", dec(False, True, None, "orion", "49financial")[0] is False and dec(False, True, rec(allow=["opal-clients"], stopped=True), "orion", "49financial")[0] is False and dec(False, True, rec(allow=["opal-clients"], status="revoked"), "orion", "49financial")[0] is False and dec(False, False, rec(allow=["opal-clients"]), "orion", "49financial")[0] is False and dec(True, False, None, "orion", "49financial")[0] is False)
bad = [("", "49financial"), ("orion", ""), ("Orion", "49financial"), ("or/ion", "x1"), ("orion", ".."), ("o", "49financial"), (None, "49financial"), ("orion", 7)]
res_bad = [dec(True, True, None, v, f) for v, f in bad]
say("a malformed vendor or firm is refused even for the master admin (%d of %d)" % (sum(1 for a, _ in res_bad if a is False), len(bad)), all(a is False and isinstance(w, str) and w for a, w in res_bad))
g = rec(allow=["opal-data-assets", "opal-data-etfs/x"])
say("served-bucket folder entries cover no client pair, and a client entry covers no folder read", dec(False, True, g, "orion", "49financial")[0] is False and fg.folder_decision(False, True, rec(allow=["opal-clients"]), "opal-clients", "orion/49financial")[0] is False)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
