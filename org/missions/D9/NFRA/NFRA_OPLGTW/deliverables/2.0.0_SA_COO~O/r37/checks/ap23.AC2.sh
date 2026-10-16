#!/usr/bin/env bash
# OPLGTW OG-ap-23 AC2 (round-37 CODE-BATCH, PHASE B, landed and served):
#  - ledger nfra-oplgtw-gateway-release-code is CLOSED at HEAD, its sentinel gone;
#  - the release LANDED (row Z-S119, time-anchored via _landed.sh);
#  - W/CODE_SERVED.json, read on the host through the INSTALLED code: the registry grew by exactly the number of tools trunk_sha adds beyond the base,
#    each added tool serves an Opal stand-in principal an enveloped answer and refuses a non-Opal principal with zero reads,
#    CVO condition C1 (one real AssumeRole of a vendor read role by the gateway role) and C2 (SmartX answers the asked firm's rows only: the two-firm negative arm) are true.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
. "$(dirname "$0")/_landed.sh"
W="org/missions/D9/NFRA/NFRA_OPLGTW/deliverables/0.7.0_AE_CloudOps~Z"
slug=nfra-oplgtw-gateway-release-code; closed=0
e=$(git ls-tree -r --name-only HEAD org/critical_paths/change_management/ | grep "_${slug}_deploy_completion\.md$" | tail -1)
[ -n "$e" ] && git show "HEAD:$e" | tr -d '\r' | grep -qE '^\*\*Status:\*\* CLOSED' && closed=1
sent=$(git ls-tree --name-only HEAD "org/critical_paths/.open_deploys/${slug}.json" | grep -c .)
[ -f "$W/ap23_release.json" ] && [ -f "$W/CODE_SERVED.json" ] || { echo "ap23_release.json or CODE_SERVED.json absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$(native "$W/ap23_release.json")" "$(native "$W/CODE_SERVED.json")" <<'PYEOF'
import json, re, subprocess, sys
rec = json.load(open(sys.argv[1], encoding="utf-8"))
base, rel, trunk = rec.get("base_sha", ""), rec.get("release_sha", ""), rec.get("trunk_sha", "")
G = "infra/aws/ec2/opal-gateway/app/tools.py"
def defs(ref):
    s = subprocess.run(["git", "show", "%s:%s" % (ref, G)], capture_output=True).stdout.decode("utf-8", "replace")
    return set(re.findall(r"(?m)^(?:async )?def (\w+)\(", s))
names = sorted(defs(trunk) - defs(base))
try:
    b = json.load(open(sys.argv[2], encoding="utf-8")).get("body", {})
except Exception:
    b = {}
before, after = b.get("registry_before"), b.get("registry_count")
grew = isinstance(before, int) and isinstance(after, int) and after == before + len(names)
pt = b.get("per_tool") or {}
good = sum(1 for n in names if isinstance(pt.get(n), dict) and pt[n].get("opal_served") is True and pt[n].get("non_opal_refused") is True and pt[n].get("reads_on_refusal") == 0)
c1, c2 = b.get("assume_role_real") is True, b.get("smartx_two_firm_arm") is True
env = b.get("reader_env_keys_present")
ca = b.get("client_admission") or {}
adm = ca.get("unprofiled_nonadmin_refused") is True and ca.get("reads_on_refusal") == 0 and ca.get("master_admin_served") is True
cls = isinstance(pt.get("mdpf_get_security_classification"), dict) and pt["mdpf_get_security_classification"].get("via_internal_reader") is True
print("registry %s -> %s (+%d); per-tool %d of %d; reader env keys %s of 6; client admission refused-then-served %s; classification call via the internal reader %s; C1 real AssumeRole %s; C2 smartx two-firm arm %s" % (before, after, len(names), good, len(names), env if isinstance(env, int) else 0, "yes" if adm else "no", "yes" if cls else "no", "yes" if c1 else "no", "yes" if c2 else "no"))
print("OK" if names and grew and good == len(names) and env == 6 and adm and cls and c1 and c2 else "NO")
PYEOF
)
res=$(printf '%s' "$res" | tr -d '\r')
rel=$(python -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8')).get('release_sha','NONE'))" "$(native "$W/ap23_release.json")" | tr -d '\r')
state=$(landed_state "$rel")
echo "ledger CLOSED $closed of 1; sentinel at HEAD $sent"
echo "release_sha=${rel:0:10}; landed=$state"
printf '%s\n' "$res" | sed '$d'
[ "$closed" = 1 ] && [ "$sent" = 0 ] && [ "$rel" != NONE ] && { [ "$state" = current ] || [ "$state" = superseded ]; } && [ "$(printf '%s\n' "$res" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
