#!/usr/bin/env bash
# MP-b-1 AC3 (R-1, the package is an artifact of the source): every member of the built zip other than
# lambda_function.py sits at its REPO-RELATIVE path (the package mirrors the repository layout, so a module that climbs
# parents[N] to the repo root finds the package's own mirror) and is byte-equal to that path at HEAD -- including
# infra/aws/ec2/opal-gateway/app/access_state.py, infra/aws/ec2/opal-gateway/ops/schwab_entitlement_admin.py and any
# data file they load; a zero-byte __init__.py absent at HEAD counts as a package marker, printed. lambda_function.py at
# HEAD climbs no parents[N]. Amended @ issuer (row NFRA_MCPORTAL-Z-W1-S3): the mirrored layout replaces gateway-relative.
. "$(dirname "$0")/_root.sh"
[ -f "$MPW_DIR/build_package.py" ] || { echo "$MPW_DIR/build_package.py absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_b1_ac3_$$"; mkdir -p "$T"; Z="$T/mcpw.zip"
timeout 120 python "$MPW_DIR/build_package.py" --out "$(native "$Z")" >/dev/null 2>&1; brc=$?
cat > "$T/probe.py" <<'EOF'
import subprocess, sys, zipfile
z = zipfile.ZipFile(sys.argv[1])
members = [n for n in z.namelist() if not n.endswith('/') and n != 'lambda_function.py']
eq = 0; diff = []; markers = 0
for n in members:
    head = subprocess.run(['git', 'show', 'HEAD:' + n], capture_output=True)
    if head.returncode == 0 and head.stdout == z.read(n):
        eq += 1
    elif head.returncode != 0 and n.endswith('__init__.py') and z.read(n) == b'':
        eq += 1; markers += 1
    else:
        diff.append(n)
G = 'infra/aws/ec2/opal-gateway/'
need = sum(1 for n in (G + 'app/access_state.py', G + 'ops/schwab_entitlement_admin.py') if n in members)
print('synthetic empty package markers: %d' % markers)
print('members %d equal %d need %d' % (len(members), eq, need))
for n in diff[:5]:
    print('not byte-equal to HEAD: ' + n)
EOF
out=$(timeout 60 python "$(native "$T/probe.py")" "$(native "$Z")" 2>&1 | tr -d '\r') || true
rm -rf "$T"
m=$(printf '%s\n' "$out" | sed -n 's/^members \([0-9]*\) .*/\1/p'); e=$(printf '%s\n' "$out" | sed -n 's/.* equal \([0-9]*\) .*/\1/p'); nd=$(printf '%s\n' "$out" | sed -n 's/.* need \([0-9]*\)$/\1/p')
pn=$(git show "HEAD:$MPW_DIR/lambda_function.py" 2>/dev/null | grep -c 'parents\[')
printf '%s\n' "$out" | grep 'not byte-equal' || true
printf '%s\n' "$out" | grep 'synthetic empty package markers' || true
echo "build rc=$brc; zip members byte-equal to their repo path at HEAD ${e:-0} of ${m:-0} (required members present ${nd:-0} of 2); parents[ in lambda_function.py=$pn"
if [ "$brc" = 0 ] && [ -n "$m" ] && [ "$m" -ge 2 ] && [ "$e" = "$m" ] && [ "$nd" = 2 ] && [ "$pn" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
