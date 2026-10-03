#!/usr/bin/env bash
# OPLGTW OG-gw-2 AC2 (NEVER-2 + NARROW): the ledger entry for nfra-oplgtw-grant-writer-catchup is committed and its
# sentinel gone, and the act left the function's environment unchanged -- key names and per-value sha256 equal the
# before-record GW2_ENV_BEFORE.json ({"env": {name: sha256}}, written at PHASE A). Counts only.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
SLUG="nfra-oplgtw-grant-writer-catchup"
B="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.9.0_WK_NFRA_OPLGTW~26/GW2_ENV_BEFORE.json"
entry=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep -c "_${SLUG}_deploy_completion\.md$")
sent=no; git cat-file -e "HEAD:org/critical_paths/.open_deploys/${SLUG}.json" 2>/dev/null && sent=yes
echo "entry files at HEAD=$entry; sentinel at HEAD=$sent"
[ -f "$B" ] || { echo "$B absent"; echo "RESULT: FAIL"; exit 1; }
aws lambda get-function-configuration --region us-east-1 --function-name mcportal-grant-writer-lambda \
  --query Environment.Variables --output json | tr -d '\r' | python -c '
import hashlib, json, sys
now = json.loads(sys.stdin.read() or "{}")
before = json.load(open(sys.argv[1], encoding="utf-8"))["env"]
hn = {k: hashlib.sha256(str(v).encode("utf-8")).hexdigest() for k, v in now.items()}
same = sum(1 for k in before if hn.get(k) == before[k])
print("env keys before %d now %d; value hashes equal %d" % (len(before), len(hn), same))
sys.exit(0 if (set(before) == set(hn) and same == len(before) and len(before) > 0) else 1)
' "$(native "$B")"; erc=$?
[ "$entry" -ge 1 ] && [ "$sent" = no ] && [ "$erc" = 0 ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
