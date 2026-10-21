#!/usr/bin/env bash
# OPLGTW OG-cs-5 AC1 (cli-shim workstream, wave 1): the access POST accepts an optional boolean widening_confirm. app/admin_people_access.shape_refusal, in one fresh process:
#  (a) a body {change, expect_revision, widening_confirm: true} is well formed ('' returned) and so is widening_confirm false;
#  (b) a body with widening_confirm "yes", 1 or null is REFUSED with a reason that names widening_confirm (a bool is the only accepted type; the bool 1 is not an int here);
#  (c) CONTROL: a body without widening_confirm is as well formed as before ('' for a valid body) and the old refusals are unchanged (an unknown change key, a missing expect_revision).
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
    from app import admin_people_access as pa
except Exception as exc:  # noqa: BLE001
    print("import failed: %s" % type(exc).__name__)
    print("NO")
    sys.exit(0)
base = {"change": {"channels_allow": ["native"]}, "expect_revision": None}
t = pa.shape_refusal(dict(base, widening_confirm=True))
f = pa.shape_refusal(dict(base, widening_confirm=False))
say("widening_confirm true and false are well formed (reasons %r, %r)" % (t, f), t == "" and f == "")
bad = {}
for label, v in (("a string", "yes"), ("the int 1", 1), ("null", None)):
    bad[label] = pa.shape_refusal(dict(base, widening_confirm=v))
say("a non-bool widening_confirm is refused naming widening_confirm (%s)" % ", ".join("%s: %s" % (k, "named" if "widening_confirm" in r else "NOT named" if r else "ACCEPTED") for k, r in bad.items()),
    all(r and "widening_confirm" in r for r in bad.values()))
none_ok = pa.shape_refusal(base) == ""
old1 = pa.shape_refusal({"change": {"bogus": ["x"]}, "expect_revision": None})
old2 = pa.shape_refusal({"change": {"channels_allow": ["native"]}})
say("control: a body without widening_confirm is well formed; unknown key and missing expect_revision still refused", none_ok and bool(old1) and bool(old2))
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
