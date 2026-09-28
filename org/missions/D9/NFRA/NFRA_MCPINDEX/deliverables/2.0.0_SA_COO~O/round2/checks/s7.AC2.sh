#!/usr/bin/env bash
# MX-s-7 AC2: the recorder's OWN update block, run on a temp source map holding one U+2014,
# writes that character back unchanged (no cp1252 mojibake). Exercises the real bytes of the script.
f=${RTD_FILE:-infra/aws/lambda/ci/record-terraform-deploy.sh}
PY=$(command -v python3 || command -v python)
T=$(mktemp -d); W=$(cygpath -m "$T" 2>/dev/null || echo "$T"); R=$(cygpath -m "$PWD" 2>/dev/null || echo "$PWD")
awk "/<<'PYEOF'/{n++; if(n==1){on=1;next}} /^PYEOF\$/{on=0} on" "$f" > "$T/block.py"
"$PY" -c "import json; open(r'$W/sm.json','w',encoding='utf-8').write(json.dumps({'functions':{'x':{'tf_file':'zz/x.tf','source_dir':'EXTERNAL','files':[],'note':'a — b'}}}, ensure_ascii=False))"
"$PY" "$T/block.py" "$W/sm.json" zz 0000000 2026-01-01T00:00:00Z "$R" > "$T/out.txt" 2>&1; rc=$?
got=$("$PY" -c "import json; n=json.load(open(r'$W/sm.json',encoding='utf-8'))['functions']['x']['note']; print('intact' if n=='a — b' else 'mojibake chars=%d' % sum(1 for c in n if ord(c)>127))" 2>&1)
rm -rf "$T"
echo "block rc=$rc em-dash round-trip=$got"
if [ "$rc" -eq 0 ] && [ "$got" = "intact" ]; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
