#!/usr/bin/env bash
# OPLGTW OG-rr-1 AC2 (round-37, the bound of the backfill cell): the cell changed NOTHING in name_rulings.json except adding the key ruling_ref.
# Baseline = the file at the pinned commit a9dd9aff6c (the last commit that touched it before this cell); the check compares the committed-or-working file to it:
# same row count, same order, same (name, type) in every position, every other field equal, the only new key on any row is ruling_ref, and _about is equal.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
PIN=a9dd9aff6c2cf0b76b7a62c663a017cc06feb8bd
res=$(python - "$PIN" <<'PYEOF'
import json, subprocess, sys
pin = sys.argv[1]
base = json.loads(subprocess.check_output(["git", "show", "%s:infra/logic/registry/name_rulings.json" % pin]).decode("utf-8"))
now = json.load(open("infra/logic/registry/name_rulings.json", encoding="utf-8"))
b = base["name_rulings"]; n = now["name_rulings"]
same_about = base.get("_about") == now.get("_about")
same_len = len(b) == len(n)
moved = 0; changed = 0; extra = 0; with_ref = 0
if same_len:
    for x, y in zip(b, n):
        if (x.get("name"), x.get("type")) != (y.get("name"), y.get("type")):
            moved += 1
        y2 = {k: v for k, v in y.items() if k != "ruling_ref"}
        if y2 != x:
            changed += 1
        extra += len(set(y) - set(x) - {"ruling_ref"})
        with_ref += 1 if "ruling_ref" in y else 0
print("name_rulings vs %s: rows %d to %d; rows moved %d (want 0); rows with another field changed %d (want 0); keys added other than ruling_ref %d (want 0); _about equal %s; rows carrying ruling_ref %d" % (pin[:10], len(b), len(n), moved, changed, extra, same_about, with_ref))
print("OK" if same_len and moved == 0 and changed == 0 and extra == 0 and same_about else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
