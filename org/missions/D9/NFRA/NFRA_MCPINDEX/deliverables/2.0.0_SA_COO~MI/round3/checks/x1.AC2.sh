#!/usr/bin/env bash
# MX-x-1 AC2 (row Z-W7-S2): the temp JavaScript CHANGELOG writer is executed ONLY by a JavaScript runtime. The line that
# runs "$TMPJS_CHANGELOG" must not start it with "$JSON_TOOL" (which resolves to python where no bun path exists -- the
# SyntaxError of Z-W7-S2), and the extracted JS must parse under node --check.
. "$(dirname "$0")/_root.sh"
F=infra/aws/lambda/ci/record-terraform-deploy.sh
[ -f "$F" ] || { echo "$F absent"; echo "RESULT: FAIL"; exit 1; }
runs=$(grep -nE '"\$[A-Z_]+"[[:space:]]+"\$TMPJS_CHANGELOG"' "$F")
total=$(printf '%s\n' "$runs" | grep -c .)
viajson=$(printf '%s\n' "$runs" | grep -c '"\$JSON_TOOL"')
T="${TMPDIR:-/tmp}/x1ac2_$$.js"
awk '/cat > "\$TMPJS_CHANGELOG" << .ENDJS./{f=1;next} /^ENDJS$/{if(f){exit}} f' "$F" > "$T"
js=$(wc -l < "$T" | tr -d ' ')
if command -v node >/dev/null 2>&1; then node --check "$T" >/dev/null 2>&1; nc=$?; else nc=127; fi
rm -f "$T"
echo "CHANGELOG writer invocations=$total; started by \$JSON_TOOL=$viajson; extracted JS lines=$js; node --check rc=$nc"
if [ "$total" -ge 1 ] && [ "$viajson" = 0 ] && [ "$js" -gt 0 ] && [ "$nc" = 0 ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
