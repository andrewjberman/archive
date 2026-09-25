#!/usr/bin/env bash
# MP-b-1 AC2 (R-3, the in-package refusal run, as Lambda does it): lambda_handler, imported from the zip EXTRACTED at
# Lambda's /var/task depth (C:\lt\<pid>) by a SCRIPT FILE (the gateway tree off the path, no AWS credentials in the
# environment), answers a narrow with no owner header with verdict REFUSED and reason NO-OWNER-HEADER -- the refusal arm
# that must work before any grant is written. Amended @ issuer (rows NFRA_MCPORTAL-Z-W1-S3, -Z-W1-S4), as AC1.
. "$(dirname "$0")/_root.sh"
[ -f "$MPW_DIR/build_package.py" ] || { echo "$MPW_DIR/build_package.py absent"; echo "RESULT: FAIL"; exit 1; }
T="${TMPDIR:-/tmp}/mp_b1_ac2_$$"; mkdir -p "$T"; Z="$T/mcpw.zip"; X="/c/lt/$$"
timeout 120 python "$MPW_DIR/build_package.py" --out "$(native "$Z")" >/dev/null 2>&1; brc=$?
rm -rf "$X"; mkdir -p "$X" && python -c "import sys,zipfile;zipfile.ZipFile(sys.argv[1]).extractall(sys.argv[2])" "$(native "$Z")" "$(native "$X")"
cat > "$T/probe.py" <<'EOF'
import sys
sys.path = [sys.argv[1]] + [p for p in sys.path[1:] if p and 'opal-gateway' not in p.replace('\\', '/')]
try:
    import lambda_function as lf
    r = lf.lambda_handler({"action": "narrow", "tid": "00000000-0000-4000-8000-0000000000e5",
                           "oid": "00000000-0000-4000-8000-0000000000f6", "candidate": {}, "owner_header": ""}, None)
    print('VERDICT %s %s' % (r.get('verdict'), r.get('reason')))
except Exception as e:
    print('RUN-FAILED %s: %s' % (type(e).__name__, e))
EOF
out=$(cd "$T" && env -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN AWS_PROFILE=mp-b1-no-such-profile \
  MCPORTAL_OWNER_OID=00000000-0000-4000-8000-00000000a0a0 MCPORTAL_OWNER_KEY_CLAIM=oid MCPORTAL_OWNER_KEY=00000000-0000-4000-8000-00000000a0a0 \
  timeout 60 python "$(native "$T/probe.py")" "$(native "$X")" 2>&1 | tr -d '\r')
rm -rf "$T" "$X"; rmdir /c/lt 2>/dev/null
v=$(printf '%s\n' "$out" | sed -n 's/^VERDICT //p' | tail -1)
printf '%s\n' "$out" | grep -m1 'RUN-FAILED' || true
echo "build rc=$brc; in-package lambda_handler (Lambda depth) with no owner header -> verdict=${v:-NONE}"
if [ "$brc" = 0 ] && [ "$v" = "REFUSED NO-OWNER-HEADER" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
