#!/usr/bin/env bash
# OPLGTW OG-cl-7 AC1 (round-37 G2-BUILD): the client suites still pass and the client modules import where lib/opal_naming.py is absent (the host shape).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 115 python -m pytest tests/test_og_cl1.py tests/test_og_cl2.py tests/test_og_cl3.py tests/test_og_cl4.py tests/test_og_cl5.py tests/test_og_cl6.py -q -p no:cacheprovider --color=no 2>&1 | tr -d '\r'); rc=$?
passed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ passed' | head -1 | grep -oE '[0-9]+'); failed=$(printf '%s\n' "$out" | grep -oE '[0-9]+ failed' | head -1 | grep -oE '[0-9]+')
echo "client suites: pytest rc=$rc; passed ${passed:-0} (want at least 49); failed ${failed:-0}"
imp=$(python - <<'PYEOF'
import os, shutil, subprocess, sys, tempfile
root = os.getcwd()
gw = os.path.join(root, "infra", "aws", "ec2", "opal-gateway")
d = tempfile.mkdtemp()
dst = os.path.join(d, "a", "b", "c", "opal-gateway")
shutil.copytree(os.path.join(gw, "app"), os.path.join(dst, "app"))
os.makedirs(os.path.join(d, "a", "b", "lib"))
shutil.copy(os.path.join(root, "lib", "trading_calendar.py"), os.path.join(d, "a", "b", "lib", "trading_calendar.py"))
code = "import sys; sys.path.insert(0, %r); sys.path.insert(0, %r); import importlib; [importlib.import_module('app.client_' + m) for m in ('core','role','adapter_schwab','adapter_bd49f','adapter_orion','adapter_eclipse','adapter_bdcottonwood','adapter_smartx','adapter_commonwealth')]; print('OK')" % (os.path.join(d, "a", "b"), dst)
r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=d, env={**os.environ, "AUDIT_PATH": os.path.join(d, "audit.jsonl")})
print("True" if r.stdout.strip().endswith("OK") else "False")
PYEOF
)
imp=$(printf '%s' "$imp" | tr -d '\r')
echo "host-shaped import: client modules import without lib/opal_naming $imp"
restore_audit
[ "$rc" = 0 ] && [ "${passed:-0}" -ge 49 ] && [ "${failed:-0}" = 0 ] && [ "$imp" = True ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
