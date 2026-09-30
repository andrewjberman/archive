#!/usr/bin/env bash
# MS-sg-1 AC3 (C4 in the audit record): app.audit._ARGS_ALLOWLIST["asker_sender_refusal"] includes sender_email and
# sender_domain (plus round 1's tid, oid, display_name, chat_id, reason) and no text/message/body/content field.
. "$(dirname "$0")/_root.sh"
res=$(cd "$G" && AUDIT_PATH="${TMPDIR:-/tmp}/ms_e2g_ac3_audit.jsonl" timeout 60 python -c "
import app.audit as a
r = set(a._ARGS_ALLOWLIST.get('asker_sender_refusal', set()))
need = {'tid','oid','display_name','chat_id','reason','sender_email','sender_domain'}
bad = {f for f in r if f in ('text','message','body','content')}
print('asker_sender_refusal=%s text_fields=%s verdict=%s' % (sorted(r), sorted(bad), 'OK' if need <= r and not bad else 'NO'))
" 2>&1 | tr -d '\r' | tail -1)
echo "$res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
