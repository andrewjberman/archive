#!/usr/bin/env bash
# MS-t-1 AC3 (row NFRA_OPALAI-Z-W2-S2, the audit gap the PRD sends to L5): app.audit._ARGS_ALLOWLIST declares
# opal_asker_query with asker_oid, key, verdict AND bytes, and declares the refusal entry's tool name
# "asker_sender_refusal" with tid, oid, display_name, chat_id and reason -- and neither carries a text/message field.
. "$(dirname "$0")/_root.sh"
res=$(cd "$G" && AUDIT_PATH="${TMPDIR:-/tmp}/ms_t1_ac3_audit.jsonl" timeout 60 python -c "
import app.audit as a
al = a._ARGS_ALLOWLIST
q = set(al.get('opal_asker_query', set())); r = set(al.get('asker_sender_refusal', set()))
need_q = {'asker_oid','key','verdict','bytes'}; need_r = {'tid','oid','display_name','chat_id','reason'}
bad = {f for f in q | r if f in ('text','message','body','content')}
ok = need_q <= q and need_r <= r and not bad
print('opal_asker_query=%s asker_sender_refusal=%s text_fields=%s verdict=%s' % (sorted(q), sorted(r), sorted(bad), 'OK' if ok else 'NO'))
" 2>&1 | tr -d '\r' | tail -1)
echo "$res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
