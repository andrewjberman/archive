#!/usr/bin/env bash
# MS-sh-1 AC2 (registration): opal_ai/opal/runtime-msp/.claude/settings.json is valid JSON whose PreToolUse hooks
# include a matcher covering the send-message tools that runs a command under hooks/ naming the sender gate, AND still
# register the concierge fence (concierge-gate) -- the round-1 fence is kept.
. "$(dirname "$0")/_root.sh"
S="opal_ai/opal/runtime-msp/.claude/settings.json"
[ -f "$S" ] || { echo "$S absent"; echo "RESULT: FAIL"; exit 1; }
res=$(python - "$S" <<'EOF' 2>&1 | tr -d '\r'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding='utf-8'))
except Exception as e:
    print('not JSON: %s verdict=NO' % e); sys.exit(0)
pre = (d.get('hooks') or {}).get('PreToolUse') or []
cmds = [(e.get('matcher', ''), h.get('command', '')) for e in pre for h in (e.get('hooks') or [])]
gate = any(('send' in m.lower() or m in ('*', '')) and 'sender' in c.lower() and 'gate' in c.lower() for m, c in cmds)
fence = any('concierge-gate' in c for _, c in cmds)
print('pretooluse entries=%d sender_gate=%s concierge_fence=%s verdict=%s' % (len(cmds), gate, fence, 'OK' if gate and fence else 'NO'))
EOF
)
echo "$res"
if printf '%s' "$res" | grep -q 'verdict=OK'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
