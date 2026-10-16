#!/usr/bin/env bash
# OPLGTW OG-rr-3 AC2 (round-37, the bound of the apply cell): against name_rulings.json at the pinned commit ecd2aad5d0 (OG-rr-1 merged) the cell changed NOTHING except ADDING ruling_ref to rows that had none:
# same row count and order, same (name, type) in every position, every other field equal, every ruling_ref that was present is unchanged, no key added other than ruling_ref, _about equal.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
PIN=ecd2aad5d0
res=$(python - "$PIN" <<'PYEOF'
import json, subprocess, sys
pin = sys.argv[1]
base = json.loads(subprocess.check_output(["git", "show", "%s:infra/logic/registry/name_rulings.json" % pin]).decode("utf-8"))
now = json.load(open("infra/logic/registry/name_rulings.json", encoding="utf-8"))
b = base["name_rulings"]; n = now["name_rulings"]
same_about = base.get("_about") == now.get("_about"); same_len = len(b) == len(n)
moved = changed = refchanged = extra = added = 0
if same_len:
    for x, y in zip(b, n):
        if (x.get("name"), x.get("type")) != (y.get("name"), y.get("type")): moved += 1
        if {k: v for k, v in y.items() if k != "ruling_ref"} != {k: v for k, v in x.items() if k != "ruling_ref"}: changed += 1
        if "ruling_ref" in x and x["ruling_ref"] != y.get("ruling_ref"): refchanged += 1
        if "ruling_ref" not in x and y.get("ruling_ref"): added += 1
        extra += len(set(y) - set(x) - {"ruling_ref"})
print("name_rulings vs %s: rows %d to %d; rows moved %d (want 0); rows with another field changed %d (want 0); existing ruling_ref changed %d (want 0); keys added other than ruling_ref %d (want 0); _about equal %s; ruling_ref newly added on %d rows" % (pin, len(b), len(n), moved, changed, refchanged, extra, same_about, added))
print("OK" if same_len and moved == 0 and changed == 0 and refchanged == 0 and extra == 0 and same_about else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
