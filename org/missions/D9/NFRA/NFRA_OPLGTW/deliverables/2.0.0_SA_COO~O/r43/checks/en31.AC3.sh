#!/usr/bin/env bash
# OPLGTW OG-en-31 AC3 (round 43): the discrimination of test_ogpr1_ac13. A mutant of app/probe_listener.py that answers an unarmed probe BEFORE the body is read must make test_ogpr1_ac13 FAIL,
# and the unmutated file must make it PASS. The product file is copied aside, mutated in place for the two seconds of the run, and restored from the copy; the restore is verified byte-equal (and a trap restores it on any exit).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
F="$GW/app/probe_listener.py"
T="tests/test_og_pr1.py"
[ -f "$F" ] || { echo "probe_listener.py absent"; echo "RESULT: FAIL"; exit 1; }
BAK="$(mktemp)"; cp -p "$F" "$BAK"
restore() { cp -p "$BAK" "$F"; }
trap restore EXIT
python -I - "$(native "$F")" <<'PYEOF'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in t else "\n"
needle = "    body_bytes = await _read_body_bounded(request)" + nl
if t.count(needle) != 1:
    print("MUTATION-NEEDLE-NOT-UNIQUE"); sys.exit(3)
mut = ("    _l0 = await current_lease()" + nl + "    if _l0 is None:" + nl +
       "        return await _refuse(tool, 403, UNARMED_LABEL, \"probe_not_armed\", \"the probe is not armed; no data is served\")" + nl)
open(p, "w", encoding="utf-8", newline="").write(t.replace(needle, mut + needle))
PYEOF
mrc=$?
if [ "$mrc" != 0 ]; then restore; echo "the mutation could not be applied (rc=$mrc)"; echo "RESULT: FAIL"; exit 1; fi
mout=$(cd "$GW" && timeout 110 python -m pytest "$T" -k test_ogpr1_ac13 -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
mfail=$(printf '%s\n' "$mout" | grep -cE '::test_ogpr1_ac13(\[.*\])? FAILED')
restore
cmp -s "$BAK" "$F" && same=yes || same=no
uout=$(cd "$GW" && timeout 110 python -m pytest "$T" -k test_ogpr1_ac13 -v -p no:cacheprovider --color=no 2>&1 | tr -d '\r')
upass=$(printf '%s\n' "$uout" | grep -cE '::test_ogpr1_ac13(\[.*\])? PASSED')
restore_audit
echo "mutant (a refusal before the body read): test_ogpr1_ac13 $([ "$mfail" -ge 1 ] && echo FAILED || echo NOT-FAILED) (want failed)"
echo "unmutated: test_ogpr1_ac13 $([ "$upass" -ge 1 ] && echo PASSED || echo NOT-PASSED) (want passed)"
echo "probe_listener.py restored byte-equal: $same"
[ "$mfail" -ge 1 ] && [ "$upass" -ge 1 ] && [ "$same" = yes ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
