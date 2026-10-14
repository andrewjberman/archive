#!/usr/bin/env bash
# MP-pd-5 AC2 (U2, the seam: the real invocation the settings will use): run the script exactly as Claude Code would, as a
# subprocess with the payload on stdin, into a TEMP config dir. It must exit 0, print ONE short line, and leave a
# usage_snapshot.json that parses with schema 1, claim measured, five_hour.used_percentage 42 and remaining_percentage 58.
. "$(dirname "$0")/_root.sh"
S=".tools/claude-usage-statusline.py"
[ -f "$S" ] || { echo "$S absent"; echo "RESULT: FAIL"; exit 1; }
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
payload='{"model":{"display_name":"x"},"rate_limits":{"five_hour":{"used_percentage":42,"resets_at":"2026-10-14T23:00:00Z"},"seven_day":{"used_percentage":10,"resets_at":"2026-10-20T00:00:00Z"}}}'
out=$(printf '%s' "$payload" | CLAUDE_CONFIG_DIR="$T" timeout 20 python "$S" 2>&1); rc=$?
lines=$(printf '%s\n' "$out" | grep -c .)
snap=$(python - "$T/usage_snapshot.json" <<'PY'
import json, sys
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception as e:
    print("snapshot=unreadable(%s)" % type(e).__name__); sys.exit()
fh = d.get("five_hour") or {}
ok = d.get("schema") == 1 and d.get("rate_limits_claim") == "measured" and fh.get("used_percentage") == 42 and fh.get("remaining_percentage") == 58
print("snapshot=read schema=%s claim=%s five_hour_used=%s remaining=%s ok=%s" % (d.get("schema"), d.get("rate_limits_claim"), fh.get("used_percentage"), fh.get("remaining_percentage"), "yes" if ok else "no"))
PY
)
echo "rc=$rc stdout_lines=$lines stdout=[$out] $snap"
if [ "$rc" = 0 ] && [ "$lines" = 1 ] && printf '%s' "$snap" | grep -q 'ok=yes'; then echo "RESULT: PASS"; exit 0; fi
echo "RESULT: FAIL"; exit 1
