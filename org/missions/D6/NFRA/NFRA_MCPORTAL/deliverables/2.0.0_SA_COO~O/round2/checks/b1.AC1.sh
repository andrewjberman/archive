#!/usr/bin/env bash
# MP-b-1 AC1 (R-1, the in-package import, as Lambda does it): build_package.py builds the grant writer's zip; the zip is
# EXTRACTED to a directory exactly as shallow as Lambda's /var/task (C:\lt\<pid>: the same 4 parent levels above a
# file one directory down), and a fresh interpreter running a SCRIPT FILE (not stdin: python-dotenv's find_dotenv asserts
# on a stdin caller) with the extraction directory first on its path and the gateway tree NOT on it imports
# lambda_function.lambda_handler, with app.access_state and ops.schwab_entitlement_admin resolved from INSIDE the
# extraction (their __file__ lies under it). Amended @ issuer after the resume run of 0.9.0_WK_NFRA_MCPORTAL~1 (rows
# NFRA_MCPORTAL-Z-W1-S3, -Z-W1-S4): a deep temp path hid ops' parents[5], and `python -` tripped dotenv.
. "$(dirname "$0")/_root.sh"
[ -f "$MPW_DIR/build_package.py" ] || { echo "$MPW_DIR/build_package.py absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_b1_ac1_$$"; mkdir -p "$T"; Z="$T/mcpw.zip"; X="/c/lt/$$"
b=$(timeout 120 python "$MPW_DIR/build_package.py" --out "$(native "$Z")" 2>&1 | tr -d '\r'); brc=$?
built=no; [ "$brc" = 0 ] && [ -s "$Z" ] && built=yes
rm -rf "$X"; mkdir -p "$X" && python -c "import sys,zipfile;zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$(native "$Z")" "$(native "$X")"
cat > "$T/probe.py" <<'EOF'
import os, sys
x = os.path.normcase(os.path.abspath(sys.argv[1]))
sys.path = [sys.argv[1]] + [p for p in sys.path[1:] if p and 'opal-gateway' not in p.replace('\\', '/')]
try:
    import lambda_function as lf
    import app.access_state as a
    import ops.schwab_entitlement_admin as o
except Exception as e:
    print('IMPORT-FAILED %s: %s' % (type(e).__name__, e)); raise SystemExit(0)
inside = sum(1 for m in (a, o) if os.path.normcase(os.path.abspath(m.__file__)).startswith(x))
print('handler=%s inside=%d' % ('yes' if callable(getattr(lf, 'lambda_handler', None)) else 'no', inside))
EOF
out=$(cd "$T" && timeout 60 python "$(native "$T/probe.py")" "$(native "$X")" 2>&1 | tr -d '\r')
rm -rf "$T" "$X"; rmdir /c/lt 2>/dev/null
h=$(printf '%s\n' "$out" | sed -n 's/^handler=\([a-z]*\) .*/\1/p'); n=$(printf '%s\n' "$out" | sed -n 's/.* inside=\([0-9]*\)$/\1/p')
printf '%s\n' "$out" | grep -m1 'IMPORT-FAILED' || true
echo "build rc=$brc built zip=$built; extracted at Lambda depth; lambda_handler callable=${h:-no}; app and ops resolved inside the package ${n:-0} of 2"
if [ "$built" = yes ] && [ "$h" = yes ] && [ "$n" = 2 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
