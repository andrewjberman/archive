#!/usr/bin/env bash
# OPLGTW OG-ln-1 AC1 (CTO R16): LINEAGE_R18.json classifies EVERY file that differs between live (the manifest's
# deployed_commit) and HEAD under infra/aws/ec2/opal-gateway/ -- measured here, not trusted -- as a CLOUD_ONLY item with
# an owner (cell or order) and a disposition in {SHIPS_IN_RELEASE, REVERTS_ON_OWNER_WORD}; and no LIVE_ONLY content
# remains: the record's live_only_remaining is 0 and the known live-only marker (integration.py
# environ_with_external_ids) is on CLOUD.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~22/LINEAGE_R18.json"
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
c=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "import json,sys;print(json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']['deployed_commit'])" | tr -d '\r')
D="${TMP:-/tmp}/og_ln1_diff_$$.txt"; git diff --name-only "$c" HEAD -- "$GW" | sort -u > "$D"
m=$(grep -c 'environ_with_external_ids' "$GW/app/integrations/schwab/integration.py")
python - "$(native "$F")" "$(native "$D")" "$m" "${c:0:10}" <<'PY'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
diff = [l.strip() for l in open(sys.argv[2], encoding="utf-8") if l.strip()]
items = {i.get("path"): i for i in d.get("items", [])}
miss = [p for p in diff if p not in items]
bad = [p for p in diff if p in items and not (items[p].get("kind") == "CLOUD_ONLY" and items[p].get("owner")
       and items[p].get("disposition") in ("SHIPS_IN_RELEASE", "REVERTS_ON_OWNER_WORD"))]
lor = d.get("live_only_remaining"); marker = int(sys.argv[3])
print("live %s; files differing live..HEAD %d; classified %d; missing %d %s; malformed %d %s; live_only_remaining %s; environ_with_external_ids on CLOUD %d"
      % (sys.argv[4], len(diff), len(diff) - len(miss), len(miss), miss[:4], len(bad), bad[:4], lor, marker))
ok = not miss and not bad and lor == 0 and marker >= 1
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
PY
r=$?; rm -f "$D"; exit $r
