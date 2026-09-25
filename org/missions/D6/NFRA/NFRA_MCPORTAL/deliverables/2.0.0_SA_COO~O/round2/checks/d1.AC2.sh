#!/usr/bin/env bash
# MP-d-1 AC2 (the NARROW release, E4, read from the committed record): EC2_MANIFEST.json at HEAD records an opal-gateway
# deployed_commit that DESCENDS from the previously deployed f1f0fc6780, whose gateway-tree difference from f1f0fc6780
# touches ONLY NFRA_MCPORTAL's files (the files MP-t-1 98ad7e253f and MP-t-4 17b7e01c0f changed, MP-g-1's <paths>, and
# deploy-to-ec2.sh), which carries app/owner_gate.py, app/admin_grants.py and tests/test_admin_round2.py, and a
# mcportal_commit that resolves in the mcportal repo.
. "$(dirname "$0")/_root.sh"
PREV="f1f0fc6780"; G="infra/aws/ec2/opal-gateway"
out=$(git show HEAD:infra/aws/ec2/EC2_MANIFEST.json | python -c "
import json,sys
s=json.loads(sys.stdin.buffer.read().decode('utf-8'))['services']['opal-gateway']
print(s.get('deployed_commit','NONE')); print(s.get('mcportal_commit','NONE'))" 2>&1 | tr -d '\r')
c=$(printf '%s\n' "$out" | sed -n 1p); m=$(printf '%s\n' "$out" | sed -n 2p)
desc=no; git merge-base --is-ancestor "$PREV" "$c" 2>/dev/null && desc=yes
allowed=$( { git show --name-only --format= 98ad7e253f 17b7e01c0f -- "$G"; printf '%s\n' "$G/app/owner_gate.py" "$G/app/admin_api.py" "$G/app/admin_grants.py" "$G/app/config.py" "$G/tests/test_admin_round2.py" "$G/deploy-to-ec2.sh"; } | sort -u)
shipped=$(git diff --name-only "$PREV" "$c" -- "$G" 2>/dev/null | sort -u)
nship=$(printf '%s\n' "$shipped" | grep -c .)
foreign=$(comm -23 <(printf '%s\n' "$shipped" | grep .) <(printf '%s\n' "$allowed" | grep .))
nf=$(printf '%s\n' "$foreign" | grep -c .)
g=0; for f in app/owner_gate.py app/admin_grants.py tests/test_admin_round2.py; do git cat-file -e "$c:$G/$f" 2>/dev/null && g=$((g+1)); done
mc=no; [ "$m" != NONE ] && git -C mcportal cat-file -e "$m^{commit}" 2>/dev/null && mc=yes
[ "$nf" != 0 ] && printf '%s\n' "$foreign" | sed 's/^/  foreign: /'
echo "deployed_commit=$c descends from $PREV=$desc; gateway files shipped $nship, outside NFRA_MCPORTAL's set $nf; carries gate+handlers+round-2 tests $g of 3; mcportal_commit=$m resolves=$mc"
if [ "$desc" = yes ] && [ "$nship" -ge 1 ] && [ "$nf" = 0 ] && [ "$g" = 3 ] && [ "$mc" = yes ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
