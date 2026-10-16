#!/usr/bin/env bash
# OPLGTW OG-rr-3 AC1 (round-37, CRO backfill msg 34909, CTO msg 34907): the CRO's ruling_refs are applied to name_rulings.json EXACTLY.
# Source of truth: org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/NAME_RULINGS_BACKFILL_RULING_REFS_20261016.json (rows with name, type, ruling_ref or null).
# Every CRO row with a non-null ruling_ref equals the registry row's ruling_ref for the same (name, type); every registry ruling_ref resolves by `git cat-file -e <commit>:<path>`;
# the only registry rows without a ruling_ref are the CRO's null rows; no registry row carries a ruling_ref where the CRO file has none.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
res=$(python - <<'PYEOF'
import json, subprocess
reg = json.load(open("infra/logic/registry/name_rulings.json", encoding="utf-8"))["name_rulings"]
cro = json.load(open("org/tier1_exec/4.0.0_SA_CRO~Z/deliverables/NAME_RULINGS_BACKFILL_RULING_REFS_20261016.json", encoding="utf-8"))["rows"]
cmap = {(r["name"], r["type"]): r.get("ruling_ref") for r in cro}
applied = 0; differ = 0; unresolved = 0; carrying = 0; nullrows_ok = 0; ref_where_none = 0; missing = 0
for r in reg:
    key = (r.get("name"), r.get("type")); ref = r.get("ruling_ref")
    if ref:
        carrying += 1
        path, _, c = ref.rpartition("@")
        if subprocess.run(["git", "cat-file", "-e", "%s:%s" % (c, path)], capture_output=True).returncode != 0:
            unresolved += 1
    if key in cmap:
        want = cmap[key]
        if want:
            if ref == want: applied += 1
            else: differ += 1
        else:
            if ref: ref_where_none += 1
            else: nullrows_ok += 1
    else:
        # a registry row the CRO file does not name must already have carried its ref at OG-rr-1
        if not ref: missing += 1
cro_nonnull = sum(1 for v in cmap.values() if v)
no_ref = sum(1 for r in reg if not r.get("ruling_ref"))
print("name_rulings: rows %d; carrying a ruling_ref %d, unresolved %d (want 0); CRO refs applied equal %d of %d, differing %d (want 0); rows without a ref %d (CRO null rows %d); ref where the CRO file has none %d (want 0); rows neither in the CRO file nor carrying a ref %d (want 0)" % (len(reg), carrying, unresolved, applied, cro_nonnull, differ, no_ref, nullrows_ok, ref_where_none, missing))
print("OK" if unresolved == 0 and differ == 0 and applied == cro_nonnull and no_ref == nullrows_ok and ref_where_none == 0 and missing == 0 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r'); printf '%s\n' "$res" | sed '$d'
restore_audit
[ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
