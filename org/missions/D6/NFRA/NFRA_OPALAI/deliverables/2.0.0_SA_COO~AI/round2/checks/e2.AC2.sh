#!/usr/bin/env bash
# OA-e-2 AC2 (built): the Analyst's runbook opal/agent/refs/RELAUNCH.md at opal_ai ${OA_NESTED_REF:-HEAD} no longer
# gives the Analyst the upload. Read as: 0 occurrences of `/terminal-upload`; every line that still names
# `opal_data_refresh_upload` also says it is NOT the Analyst's (the token `never` or `not` on that same line); and the
# operator's daily script `publish_to_portal.py` is named at least once, so the duty has an owner in the text.
. "$(dirname "$0")/_root.sh"
REF="${OA_NESTED_REF:-HEAD}"
[ -e opal_ai/.git ] || { echo "opal_ai nested repo absent"; echo "RESULT: FAIL"; exit 1; }
txt=$(git -C opal_ai show "$REF:opal/agent/refs/RELAUNCH.md" 2>/dev/null | tr -d '\r')
if [ -z "$txt" ]; then echo "RELAUNCH.md absent at opal_ai $REF"; echo "RESULT: FAIL"; exit 1; fi
tu=$(printf '%s\n' "$txt" | grep -c '/terminal-upload')
up=$(printf '%s\n' "$txt" | grep -c 'opal_data_refresh_upload')
upbad=$(printf '%s\n' "$txt" | grep 'opal_data_refresh_upload' | grep -vciE '\b(never|not)\b')
pub=$(printf '%s\n' "$txt" | grep -c 'publish_to_portal\.py')
echo "opal_ai $REF RELAUNCH.md: /terminal-upload=$tu; upload lines=$up, of which without never/not=$upbad; publish_to_portal.py=$pub"
if [ "$tu" = 0 ] && [ "$upbad" = 0 ] && [ "$pub" -ge 1 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
