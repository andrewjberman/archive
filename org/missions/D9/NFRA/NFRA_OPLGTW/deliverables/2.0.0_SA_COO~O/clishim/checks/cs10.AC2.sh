#!/usr/bin/env bash
# OPLGTW OG-cs-10 AC2 (cli-shim workstream, wave 4): the registry hookup and the classification of the three folder tools. One fresh process, no AWS, no network.
#  (a) registry.available_ids() holds "folders" and its factory builds an Integration whose spec passes registry.validate_integration_spec with no violation;
#  (b) data_entitlement.FOLDER_TOOLS is exactly the three names; each is classified "legacy" (classify() is not None), none is a Schwab tool, none is in DATA_GRANT_TOOLS or TIER_ADMITTED_TOOLS (the folder strings in the person's record are the gate, not the tool name);
#  (c) DORMANT: register_enabled(fake_mcp, []) registers nothing, "folders" is not in get_config().ENABLED_INTEGRATIONS by default, and register_enabled(fake_mcp, ["folders"]) reports exactly the three tools with no error, violations, unclassified or composed_path_refused key.
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
    from app import data_entitlement as de
    from app.config import get_config
    from app.integrations import base, registry
except Exception as exc:  # noqa: BLE001
    print("import failed: %s: %s" % (type(exc).__name__, str(exc)[:80]))
    print("NO")
    sys.exit(0)

NAMES = ("folder_list", "folder_describe", "folder_query")
ids = registry.available_ids()
fac = registry._FACTORIES.get("folders")
errs = None
try:
    integ = fac()
    errs = registry.validate_integration_spec(integ.spec)
except Exception as exc:  # noqa: BLE001
    errs = ["%s: %s" % (type(exc).__name__, str(exc)[:60])]
say("the registry holds folders and its spec validates (violations %s)" % errs, "folders" in ids and fac is not None and errs == [])
ft = getattr(de, "FOLDER_TOOLS", None)
cl = [de.classify(t) for t in NAMES]
say("FOLDER_TOOLS is exactly the three names, each classified %s, none a Schwab, data-grant or tier-admitted tool" % cl,
    ft == frozenset(NAMES) and all(c == de.CLASS_LEGACY for c in cl) and not (set(NAMES) & set(de.SCHWAB_TOOLS)) and not (set(NAMES) & set(de.DATA_GRANT_TOOLS)) and not (set(NAMES) & set(de.TIER_ADMITTED_TOOLS)))


class FakeMCP:
    def __init__(self):
        self.names = []

    def tool(self, name=None, **kw):
        def deco(fn):
            self.names.append(name or fn.__name__)
            return fn
        return deco


m0 = FakeMCP()
r0 = registry.register_enabled(m0, [])
say("register_enabled with no ids registers nothing and folders is not enabled by default (%s)" % list(get_config().ENABLED_INTEGRATIONS), r0 == {} and m0.names == [] and "folders" not in get_config().ENABLED_INTEGRATIONS)
m1 = FakeMCP()
r1 = registry.register_enabled(m1, ["folders"])
rep = r1.get("folders", {})
extra = [k for k in ("error", "violations", "unclassified", "composed_path_refused") if k in rep]
say("enabling folders reports exactly the three tools and nothing refused (%s, extra keys %s)" % (rep.get("tools"), extra), rep.get("tools") == list(NAMES) and m1.names == list(NAMES) and not extra)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
