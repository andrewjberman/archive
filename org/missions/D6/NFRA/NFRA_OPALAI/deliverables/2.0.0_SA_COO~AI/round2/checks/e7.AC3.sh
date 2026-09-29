#!/usr/bin/env bash
# OA-e-7 AC3 (built, row Z-S20): opal_ai's CI workflow at ${OA_NESTED_REF:-HEAD} installs BOTH pytest and ruff in a step
# that runs BEFORE the step that runs opal/checks/run_checks.sh. (The run's green on a real push is G-PUSH's, at the
# cutover; this reads the workflow the push will run.)
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
out=$(git -C opal_ai show "$REF:.github/workflows/ci.yml" 2>/dev/null | python -c '
import sys, yaml
try:
    d = yaml.safe_load(sys.stdin.read()) or {}
except Exception as e:
    print("parse failed: %s" % e); sys.exit(0)
steps = [s for j in (d.get("jobs") or {}).values() for s in (j.get("steps") or [])]
runs = [str(s.get("run", "")) for s in steps]
chk = next((i for i, r in enumerate(runs) if "run_checks.sh" in r), None)
def before(tok):
    return any(tok in r and "install" in r for r in runs[: chk if chk is not None else 0])
pin = "yes" if any("ruff==0.16.9" in r for r in runs[: chk if chk is not None else 0]) else "no"
print("steps=%d; run_checks step=%s; pytest installed before it=%s; ruff installed before it=%s; ruff pinned 0.16.9=%s" % (
    len(steps), "none" if chk is None else chk, "yes" if before("pytest") else "no", "yes" if before("ruff") else "no", pin))
' 2>&1 | tr -d '\r')
echo "opal_ai $REF: ${out:-ci.yml absent}"
if printf '%s' "$out" | grep -q 'pytest installed before it=yes; ruff installed before it=yes; ruff pinned 0.16.9=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
