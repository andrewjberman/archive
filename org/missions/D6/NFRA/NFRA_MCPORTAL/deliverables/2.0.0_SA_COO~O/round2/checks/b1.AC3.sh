#!/usr/bin/env bash
# MP-b-1 AC3 (R-1, the package is an artifact of the source): every .py member of the built zip other than
# lambda_function.py is byte-equal to the file at the same relative path under infra/aws/ec2/opal-gateway/ at HEAD
# (at least app/access_state.py and ops/schwab_entitlement_admin.py among them), and lambda_function.py at HEAD
# climbs no parents[N].
. "$(dirname "$0")/_root.sh"
[ -f "$MPW_DIR/build_package.py" ] || { echo "$MPW_DIR/build_package.py absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_b1_ac3_$$"; mkdir -p "$T"; Z="$T/mcpw.zip"
timeout 120 python "$MPW_DIR/build_package.py" --out "$(native "$Z")" >/dev/null 2>&1; brc=$?
out=$(timeout 60 python - "$(native "$Z")" <<'EOF' 2>&1 | tr -d '\r'
import subprocess, sys, zipfile
z = zipfile.ZipFile(sys.argv[1])
py = [n for n in z.namelist() if n.endswith('.py') and n != 'lambda_function.py']
eq = 0; diff = []; markers = 0
for n in py:
    head = subprocess.run(['git', 'show', 'HEAD:infra/aws/ec2/opal-gateway/' + n], capture_output=True)
    if head.returncode == 0 and head.stdout == z.read(n):
        eq += 1
    elif head.returncode != 0 and n.endswith('__init__.py') and z.read(n) == b'':
        # A zero-byte package marker the source tree lacks (the gateway's ops/ has no __init__.py) is not a copy of
        # source; it counts as equal and is printed.
        eq += 1; markers += 1
    else:
        diff.append(n)
need = sum(1 for n in ('app/access_state.py', 'ops/schwab_entitlement_admin.py') if n in py)
print('synthetic empty package markers: %d' % markers)
print('members %d equal %d need %d' % (len(py), eq, need))
for n in diff[:5]:
    print('not byte-equal to HEAD: ' + n)
EOF
) || true
rm -rf "$T"
m=$(printf '%s\n' "$out" | sed -n 's/^members \([0-9]*\) .*/\1/p'); e=$(printf '%s\n' "$out" | sed -n 's/.* equal \([0-9]*\) .*/\1/p'); nd=$(printf '%s\n' "$out" | sed -n 's/.* need \([0-9]*\)$/\1/p')
pn=$(git show "HEAD:$MPW_DIR/lambda_function.py" 2>/dev/null | grep -c 'parents\[')
printf '%s\n' "$out" | grep 'not byte-equal' || true
printf '%s\n' "$out" | grep 'synthetic empty package markers' || true
echo "build rc=$brc; zip members byte-equal to the gateway tree at HEAD ${e:-0} of ${m:-0} (required members present ${nd:-0} of 2); parents[ in lambda_function.py=$pn"
if [ "$brc" = 0 ] && [ -n "$m" ] && [ "$m" -ge 2 ] && [ "$e" = "$m" ] && [ "$nd" = 2 ] && [ "$pn" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
