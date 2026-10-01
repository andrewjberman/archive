#!/usr/bin/env bash
# MS-sv-1 AC1 (the live refusal, read from the served host's own audit record): in the window the worker recorded at
# deliverables/0.9.0_WK_NFRA_MCPMSP~6/r2_e2v_run.json ({"t0","t1","chat_id"}), the host's audit.jsonl holds >= 1
# asker_sender_refusal entry for that chat with reason asker_pilot_scope and sender_domain opalinvest.com, and NO such
# entry carries a text/message/body field.
. "$(dirname "$0")/_root.sh"
RUN="$R2/0.9.0_WK_NFRA_MCPMSP~6/r2_e2v_run.json"
[ -f "$RUN" ] || { echo "$RUN absent (the live arm has not run)"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_e2v.XXXXXX")"
python - "$RUN" "$T/params.json" <<'EOF'
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
cmd = ("python3 -c \"import json,sys\nfor l in open('/opt/opal-gateway/audit.jsonl'):\n  try: d=json.loads(l)\n  except Exception: continue\n"
       "  if d.get('tool')=='asker_sender_refusal' and '%s'<=str(d.get('ts',''))<='%s': print('E2V='+json.dumps(d))\"") % (r['t0'], r['t1'])
json.dump({"commands": [cmd]}, open(sys.argv[2], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"
printf '%s\n' "$SSM_OUT" | sed -n 's/^E2V=//p' > "$T/e.jsonl"
res=$(python - "$RUN" "$T/e.jsonl" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
chat = json.load(open(sys.argv[1], encoding='utf-8')).get('chat_id')
es = [json.loads(l) for l in open(sys.argv[2], encoding='utf-8') if l.strip()]
hit = [e for e in es if (e.get('args') or {}).get('chat_id') == chat and (e.get('args') or {}).get('reason') == 'asker_pilot_scope' and (e.get('args') or {}).get('sender_domain') == 'opalinvest.com']
txt = [e for e in es if any(f in (e.get('args') or {}) for f in ('text','message','body','content'))]
print('refusal entries in window=%d matching chat+asker_pilot_scope+opalinvest.com=%d with text=%d verdict=%s' % (len(es), len(hit), len(txt), 'OK' if hit and not txt else 'NO'))
EOF
)
rm -rf "$T"
echo "ssm command=$SSM_CID status=$SSM_ST; $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
