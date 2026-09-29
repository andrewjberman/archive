#!/usr/bin/env bash
# MX-x-3 AC1 (row Z-W13-S2): validate_catalog_v02.py has an offline mode that makes ZERO AWS calls. Proven by running
# its main() under `--offline` with the module's aws() replaced by a trap that aborts on any call: exit 0, 0 calls, and
# the local schema pass still printed.
. "$(dirname "$0")/_root.sh"
cd workflows/atom_decomposition || { echo "workflows/atom_decomposition absent"; echo "RESULT: FAIL"; exit 1; }
out=$(timeout 300 python - <<'PY' 2>&1 | tr -d '\r'
import sys
import validate_catalog_v02 as v
calls = []
def trap(*a):
    calls.append(a)
    raise SystemExit("AWS CALLED: %r" % (a[:3],))
v.aws = trap
sys.argv = ["validate_catalog_v02.py", "--offline"]
try:
    rc = v.main()
except SystemExit as e:
    print("EXIT %s" % e)
    rc = 99
print("offline rc=%s aws calls=%d" % (rc, len(calls)))
PY
); rc=$?
printf '%s\n' "$out" | tail -4
schema=$(printf '%s\n' "$out" | grep -c 'SILVER ENTRY SCHEMA VALIDATION')
line=$(printf '%s\n' "$out" | grep -E '^offline rc=0 aws calls=0$' | head -1)
if [ -n "$line" ] && [ "$schema" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
