#!/usr/bin/env bash
# OPLGTW OG-cs-8 AC1 (cli-shim workstream, wave 2; PRD v3.19 FWD-24 DONE WHEN: the contract's per-account, per-column and masked-reference clauses are revised to say they are superseded). One fresh process:
#  (a) both copies (infra/aws/ec2/opal-gateway/deploy/NFRA_OPLGTW_CONTRACT.json and org/standards/NFRA_OPLGTW_CONTRACT.json) parse and are BYTE-EQUAL;
#  (b) contract_version reads "1.5" (the pin read "1.4") and a top-level key fwd24_supersession holds the keys authority, applies_to, superseded_clauses, meaning, unchanged, with superseded_clauses exactly ["per_account_grant", "per_column_grant", "masked_account_reference"];
#  (c) NOTHING ELSE MOVED: deleting fwd24_supersession and setting contract_version back to "1.4" makes the parsed document equal the pinned blob e24c1fcc85's, and the text diff against the pin has at most two hunks, one removed line (the version line) and at most 12 added lines.
. "$(dirname "$0")/../../r47/checks/_gwtests.sh"
res=$(python3 -I - "$(native "$GW")" "$(native "$_R")" <<'PYEOF'
import difflib, json, subprocess, sys
G, ROOT = sys.argv[1], sys.argv[2]
ok = True


def say(label, cond):
    global ok
    ok = ok and bool(cond)
    print("%s: %s" % (label, "ok" if cond else "NOT OK"))


try:
    a = open(G + "/deploy/NFRA_OPLGTW_CONTRACT.json", "rb").read()
    b = open(ROOT + "/org/standards/NFRA_OPLGTW_CONTRACT.json", "rb").read()
    d = json.loads(a.decode("utf-8"))
except Exception as exc:  # noqa: BLE001
    print("read failed: %s" % type(exc).__name__)
    print("NO")
    sys.exit(0)
say("both copies parse and are byte-equal", a == b)
sup = d.get("fwd24_supersession") or {}
say("contract_version is 1.5 and fwd24_supersession holds its five keys with the three superseded clauses", d.get("contract_version") == "1.5" and sorted(sup) == sorted(["authority", "applies_to", "superseded_clauses", "meaning", "unchanged"])
    and sup.get("superseded_clauses") == ["per_account_grant", "per_column_grant", "masked_account_reference"] and all(isinstance(sup.get(k), str) and len(sup[k]) >= 20 for k in ("authority", "applies_to", "meaning", "unchanged")))
pin_raw = subprocess.run(["git", "show", "e24c1fcc85340624874b2d7f2c16d9f30bb174e0"], capture_output=True).stdout.decode("utf-8")
pin = json.loads(pin_raw) if pin_raw else {}
back = dict(d)
back.pop("fwd24_supersession", None)
back["contract_version"] = "1.4"
dd = list(difflib.unified_diff(pin_raw.splitlines(), a.decode("utf-8").splitlines(), lineterm="", n=0))
hunks = [x for x in dd if x.startswith("@@")]
rem = [x for x in dd if x.startswith("-") and not x.startswith("---")]
add = [x for x in dd if x.startswith("+") and not x.startswith("+++")]
say("nothing else moved: the document minus the new key equals the pin (hunks %d, removed %d, added %d)" % (len(hunks), len(rem), len(add)), bool(pin) and back == pin and len(hunks) <= 2 and len(rem) == 1 and "contract_version" in rem[0] and 1 <= len(add) <= 13)
print("OK" if ok else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
