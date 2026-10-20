#!/usr/bin/env bash
# OPLGTW OG-tp-1 AC2 (round 47, Z-S423 T1): poll_addressed_impl (the shared poll behind the MCP tool poll_addressed_teams_messages and the REST /teams/poll) honours `top`.
# Probe: graph.call returns six chats whose last messages are 10:01..10:06; the sender helpers are faked. With since 09:00 and top=2:
#   the answer holds the two OLDEST new messages (oldest-first), count 2, cursor equal to the second one's timestamp, truncated true;
#   three polls in a row (each passing the previous cursor) return all six messages exactly once, in order, and the third poll is not truncated;
#   top=50 (the default) returns all six, cursor 10:06, and no truncated key;
#   a poll with no new message keeps the cursor it was given and count 0.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 110 python3 -I - <<'EOF'
import sys, json
sys.path.insert(0, ".")
ok = True
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app import tools
except Exception as exc:
    print("import failed: %s %s" % (type(exc).__name__, str(exc)[:100])); print("NO"); sys.exit(0)
chats = [{"id": "chat%d" % i, "chatType": "oneOnOne",
          "lastMessagePreview": {"createdDateTime": "2026-10-20T10:%02d:00Z" % i, "from": {"user": {"displayName": "User %d" % i}}, "body": {"content": "<p>hello %d</p>" % i}}}
         for i in range(6, 0, -1)]
tools.graph.call = lambda t, method, path, params=None, **k: {"value": json.loads(json.dumps(chats))}
tools._SenderIds = lambda token: None
tools._sender_fields = lambda usr, ids, chat_id: ("sender-%s" % chat_id, "tenant")
tools.get_current_email = lambda: "tester"
tools.identity_scope.is_opal_users_only = lambda email: False
try:
    r = tools.poll_addressed_impl("tok", "2026-10-20T09:00:00Z", 2)
    ts = [m["timestamp_utc"] for m in r["new_messages"]]
    say("top=2: the two oldest new messages, oldest first, count 2", ts == ["2026-10-20T10:01:00Z", "2026-10-20T10:02:00Z"] and r["count"] == 2, "timestamps %s count %s" % (ts, r.get("count")))
    say("top=2: cursor is the second message, truncated true", r["cursor"] == "2026-10-20T10:02:00Z" and r.get("truncated") is True, "cursor %s truncated %r" % (r.get("cursor"), r.get("truncated")))
    seen, cursor, last = [], "2026-10-20T09:00:00Z", None
    for _ in range(3):
        last = tools.poll_addressed_impl("tok", cursor, 2)
        seen += [m["chat_id"] for m in last["new_messages"]]
        cursor = last["cursor"]
    say("three polls of 2 return all six once, in order", seen == ["chat%d" % i for i in range(1, 7)], "seen %s" % seen)
    say("the third poll is not truncated", not last.get("truncated") and last["cursor"] == "2026-10-20T10:06:00Z", "truncated %r cursor %s" % (last.get("truncated"), last.get("cursor")))
    r = tools.poll_addressed_impl("tok", "2026-10-20T09:00:00Z")
    say("default top: all six, cursor 10:06, no truncated key", r["count"] == 6 and r["cursor"] == "2026-10-20T10:06:00Z" and "truncated" not in r, "count %s" % r.get("count"))
    r = tools.poll_addressed_impl("tok", "2026-10-20T10:06:00Z", 2)
    say("nothing new: count 0, the given cursor kept", r["count"] == 0 and r["cursor"] == "2026-10-20T10:06:00Z" and not r.get("truncated"))
except Exception as exc:
    print("probe raised %s: %s" % (type(exc).__name__, str(exc)[:160])); ok = False
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
