#!/usr/bin/env bash
# MP-b-1 AC1 (R-1, the in-zip import): build_package.py builds the grant writer's zip, and a fresh interpreter whose path
# holds the ZIP and NOT the gateway tree imports lambda_function.lambda_handler, with app.access_state and
# ops.schwab_entitlement_admin resolved from INSIDE the zip (their __file__ lies under the zip path).
. "$(dirname "$0")/_root.sh"
[ -f "$MPW_DIR/build_package.py" ] || { echo "$MPW_DIR/build_package.py absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_b1_ac1_$$"; mkdir -p "$T"; Z="$T/mcpw.zip"
b=$(timeout 120 python "$MPW_DIR/build_package.py" --out "$(native "$Z")" 2>&1 | tr -d '\r'); brc=$?
built=no; [ "$brc" = 0 ] && [ -s "$Z" ] && built=yes
out=$(cd "$T" && timeout 60 python - "$(native "$Z")" <<'EOF' 2>&1 | tr -d '\r'
import os, sys
z = os.path.normcase(os.path.abspath(sys.argv[1]))
# The zip first; drop the cwd entry and anything under the gateway tree, so only the zip can supply app/ and ops/.
sys.path = [sys.argv[1]] + [p for p in sys.path[1:] if p and 'opal-gateway' not in p.replace('\\', '/')]
try:
    import lambda_function as lf
    import app.access_state as a
    import ops.schwab_entitlement_admin as o
except Exception as e:
    print('IMPORT-FAILED %s: %s' % (type(e).__name__, e)); raise SystemExit(0)
inside = sum(1 for m in (a, o) if os.path.normcase(os.path.abspath(m.__file__)).startswith(z))
print('handler=%s inside=%d' % ('yes' if callable(getattr(lf, 'lambda_handler', None)) else 'no', inside))
EOF
)
rm -rf "$T"
h=$(printf '%s\n' "$out" | sed -n 's/^handler=\([a-z]*\) .*/\1/p'); n=$(printf '%s\n' "$out" | sed -n 's/.* inside=\([0-9]*\)$/\1/p')
printf '%s\n' "$out" | grep -m1 'IMPORT-FAILED' || true
echo "build rc=$brc built zip=$built; lambda_handler callable=${h:-no}; app and ops resolved inside the zip ${n:-0} of 2"
if [ "$built" = yes ] && [ "$h" = yes ] && [ "$n" = 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
