#!/usr/bin/env bash
# OPLGTW OG-rr-1 AC1 (round-37, CTO ruling @8b9adcbd8d section 3 cell 1, CVO verdict 6495): every name_rulings.json row carries a ruling_ref (path@commit) that RESOLVES by `git cat-file -e <commit>:<path>`;
# a row whose ruling cannot be found is LISTED by name in W/RULING_REF_UNRESOLVED.json and is NOT given an invented ref. The check counts: rows with a ref that resolves + rows listed unresolved = all rows, and no row is in both.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~115"
[ -f "$W/RULING_REF_UNRESOLVED.json" ] || { echo "RULING_REF_UNRESOLVED.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/RULING_REF_UNRESOLVED.json")" <<'PYEOF'
import json, subprocess, sys
d = json.load(open("infra/logic/registry/name_rulings.json", encoding="utf-8"))
rows = [r for r in d.get("name_rulings", []) if isinstance(r, dict)]
unres = json.load(open(sys.argv[1], encoding="utf-8")).get("unresolved", [])
listed = {(u.get("name"), u.get("type")) for u in unres if isinstance(u, dict)}
resolved = 0; bad = []; both = 0
for r in rows:
    key = (r.get("name"), r.get("type"))
    ref = r.get("ruling_ref")
    ok = False
    if isinstance(ref, str) and "@" in ref:
        path, _, commit = ref.rpartition("@")
        ok = subprocess.run(["git", "cat-file", "-e", "%s:%s" % (commit, path)], capture_output=True).returncode == 0
    if ok:
        resolved += 1
        if key in listed:
            both += 1
    elif key not in listed:
        bad.append(key)
print("name_rulings: rows %d; ruling_ref resolves %d; listed unresolved %d; neither (defect) %d (want 0); in both %d (want 0)" % (len(rows), resolved, len(listed), len(bad), both))
print("OK" if not bad and both == 0 and resolved + len(listed) == len(rows) else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
