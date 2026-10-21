#!/usr/bin/env bash
# OPLGTW OG-cs-1 AC2 (cli-shim workstream, wave 1; row NFRA_OPLGTW-Z-S447): the gateway reads a folder string in channels_allow and channels_deny without making the record Malformed, and nothing else about the parser loosens.
# app/data_entitlement.parse_person_access, in one fresh process:
#  (a) a record with channels_allow ["opal-data-etfs", "opal-data-assets/schwab/08335338/", "native", "ycharts"] and channels_deny ["opal-data-harvest"] PARSES (the old channel ids and the new folder strings together);
#  (b) CONTROL: entries of the wrong shape still raise Malformed: "Bad Case", "", " x", "UPPER-bucket", "a b", an entry of 129 characters, "opal-data-assets/../x", "/opal-data-assets", and a non-string;
#  (c) the existing channel logic is unchanged: channel_of("whoami") is "native" and person_denial("whoami", a record with channels_deny ["native"]) still denies, while a record whose channels_deny holds only a folder string denies no tool by channel;
#  (d) a BOUND: app/data_entitlement.py against the pinned blob 881da34cda: at most 40 lines added and 10 removed.
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" <<'PYEOF'
import difflib, os, subprocess, sys
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
    from app import data_entitlement as de
except Exception as exc:  # noqa: BLE001
    print("import failed: %s" % type(exc).__name__)
    print("NO")
    sys.exit(0)
T, O = "11111111-1111-1111-1111-111111111111", "22222222-2222-2222-2222-222222222222"


def base(allow=(), deny=()):
    return {"status": "active", "revision": 2, "tid": T, "oid": O, "tools_allow": [], "tools_deny": [], "channels_allow": list(allow), "channels_deny": list(deny)}


def parses(r):
    try:
        return de.parse_person_access(r, T, O)
    except de.Malformed:
        return None
    except Exception as exc:  # noqa: BLE001
        return type(exc).__name__


p = parses(base(["opal-data-etfs", "opal-data-assets/schwab/08335338/", "native", "ycharts"], ["opal-data-harvest"]))
say("old channel ids and folder strings together parse", p is not None and not isinstance(p, str) and "opal-data-assets/schwab/08335338/" in p.channels_allow and "native" in p.channels_allow and "opal-data-harvest" in p.channels_deny)
bads = ["Bad Case", "", " x", "UPPER-bucket", "a b", "x" * 129, "opal-data-assets/../x", "/opal-data-assets"]
res = [(b[:12], parses(base([b]))) for b in bads] + [("non-string", parses(base([7])))]
say("wrong shapes still raise Malformed (%s)" % ", ".join("%s:%s" % (k, "M" if v is None else "ACCEPTED") for k, v in res), all(v is None for _, v in res))
try:
    ch = de.channel_of("whoami")
    deny = de.person_denial("whoami", de.parse_person_access(base([], ["native"]), T, O))
    pf = de.person_denial("whoami", de.parse_person_access(base([], ["opal-data-assets/schwab/"]), T, O))
    say("channel logic unchanged: whoami is native, a native deny denies, a folder-only deny denies nothing by channel", ch == "native" and deny is not None and pf is None)
except Exception as exc:  # noqa: BLE001
    say("channel logic unchanged (%s)" % type(exc).__name__, False)
old = subprocess.run(["git", "show", "881da34cda892e22d588c184505de624a96b36d2"], capture_output=True).stdout.decode("utf-8").splitlines()
new = open(G + "/app/data_entitlement.py", encoding="utf-8").read().splitlines()
dd = list(difflib.unified_diff(old, new, lineterm="", n=0))
r = [x for x in dd if x.startswith("-") and not x.startswith("---")]
a = [x for x in dd if x.startswith("+") and not x.startswith("+++")]
say("app/data_entitlement.py against the pin: %d added, %d removed (want at most 40 and 10, and at least 3 added)" % (len(a), len(r)), 3 <= len(a) <= 40 and len(r) <= 10)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
