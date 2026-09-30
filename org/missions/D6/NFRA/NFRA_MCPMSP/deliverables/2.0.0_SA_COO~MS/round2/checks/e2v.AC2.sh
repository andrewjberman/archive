#!/usr/bin/env bash
# MS-sv-1 AC2 (no reply, from the gateway's own record): in the same window, the host's audit.jsonl holds ZERO
# send_chat_message / send_channel_message calls of ANY target by the MSP calling identity (e2v_run.json
# "msp_identity"), while holding >= 1 opal_asker_query call by it (the control: the session did ask). Any target, not
# "that chat": send_chat_message is absent from audit._ARGS_ALLOWLIST, so its chat_id is never logged (measured at the
# cut) and a chat filter would read zero for every send -- a false pass.
. "$(dirname "$0")/_root.sh"
RUN="$R2/0.9.0_WK_NFRA_MCPMSP~6/r2_e2v_run.json"
[ -f "$RUN" ] || { echo "$RUN absent (the live arm has not run)"; echo "RESULT: FAIL"; exit 1; }
T="$(mktemp -d "${TMPDIR:-/tmp}/ms_e2v2.XXXXXX")"
python - "$RUN" "$T/params.json" <<'EOF'
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8'))
cmd = ("python3 -c \"import json\nfor l in open('/opt/opal-gateway/audit.jsonl'):\n  try: d=json.loads(l)\n  except Exception: continue\n"
       "  if '%s'<=str(d.get('ts',''))<='%s' and d.get('tool') in ('send_chat_message','send_channel_message','opal_asker_query'): print('E2V2='+json.dumps(d))\"") % (r['t0'], r['t1'])
json.dump({"commands": [cmd]}, open(sys.argv[2], "w", encoding="utf-8"))
EOF
ssm_run "$T/params.json"
printf '%s\n' "$SSM_OUT" | sed -n 's/^E2V2=//p' > "$T/e.jsonl"
res=$(python - "$RUN" "$T/e.jsonl" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
r = json.load(open(sys.argv[1], encoding='utf-8')); chat = r.get('chat_id'); who = (r.get('msp_identity') or '').lower()
es = [json.loads(l) for l in open(sys.argv[2], encoding='utf-8') if l.strip()]
mine = [e for e in es if str(e.get('user', '')).lower() == who]
sends = [e for e in mine if e.get('tool') in ('send_chat_message', 'send_channel_message')]
asks = [e for e in mine if e.get('tool') == 'opal_asker_query']
print('msp identity calls=%d asker_queries=%d sends_any_target=%d verdict=%s' % (len(mine), len(asks), len(sends), 'OK' if asks and not sends else 'NO'))
EOF
)
rm -rf "$T"
echo "ssm command=$SSM_CID status=$SSM_ST; $res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
