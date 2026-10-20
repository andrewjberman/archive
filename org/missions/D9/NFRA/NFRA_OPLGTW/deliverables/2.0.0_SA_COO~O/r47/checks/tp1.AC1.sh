#!/usr/bin/env bash
# OPLGTW OG-tp-1 AC1 (round 47, Z-S424): search_files and search_site_files take a result cap `top` (default 25, at most 100) and every answer fits 51200 bytes as served
# (json indent=2). Probe: tools._run is replaced by a runner that calls the lambda with a token, graph.call by a fake returning 400 drive items.
#   default: 25 items kept, in the order Graph returned them, `truncated` true, `total` 400 (what Graph returned), `returned` 25;
#   top=100: 100 items kept; top=500: capped to 100; top=0 or negative: capped to 1 (never an empty page by a bad argument);
#   items so large that 100 of them exceed 51200 bytes: the answer still fits (the list is cut further, `returned` says how many);
#   a Graph answer of 5 items: returned equal to what Graph answered, no `truncated` key.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 110 python3 -I - <<'EOF'
import sys, json
sys.path.insert(0, ".")
ok = True
def size(o):
    return len(json.dumps(o, indent=2, default=str).encode("utf-8"))
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app import tools
except Exception as exc:
    print("import failed: %s %s" % (type(exc).__name__, str(exc)[:100])); print("NO"); sys.exit(0)
def item(i, pad=0):
    return {"name": "file_%04d.xlsx" % i, "id": "id%06d" % i, "size": 1000 + i, "lastModifiedDateTime": "2026-10-16T00:00:00Z",
            "webUrl": "https://example.invalid/d/%04d/%s" % (i, "p" * pad)}
state = {"payload": None}
tools._run = lambda tool, args, fn, confirm=False, audit_detail="": fn("token")
tools.graph.call = lambda t, method, path, params=None, **k: json.loads(json.dumps(state["payload"]))
def both(**kw):
    state["payload"] = kw.pop("payload")
    return tools.search_files("q", **kw), tools.search_site_files("site", "q", **kw)
try:
    state_items = [item(i) for i in range(400)]
    for label, fn_args in (("search_files", 0), ("search_site_files", 1)):
        pass
    a, b = both(payload={"value": state_items})
    for name, r in (("search_files", a), ("search_site_files", b)):
        v = r.get("value")
        say("%s default: 25 kept in order, truncated, total 400, returned 25" % name, isinstance(v, list) and v == state_items[:25] and r.get("truncated") is True and r.get("total") == 400 and r.get("returned") == 25, "kept %s" % (len(v) if isinstance(v, list) else None))
    a, b = both(payload={"value": state_items}, top=100)
    say("top=100 keeps 100 (both tools)", len(a.get("value") or []) == 100 and len(b.get("value") or []) == 100 and a.get("returned") == 100)
    a, b = both(payload={"value": state_items}, top=500)
    say("top=500 is capped to 100 (both tools)", len(a.get("value") or []) == 100 and len(b.get("value") or []) == 100)
    a, b = both(payload={"value": state_items}, top=0)
    say("top=0 is capped to 1 (both tools)", len(a.get("value") or []) == 1 and len(b.get("value") or []) == 1)
    big = [item(i, pad=3000) for i in range(400)]
    a, b = both(payload={"value": big}, top=100)
    say("100 large items still fit 51200 bytes indented", size(a) <= 51200 and size(b) <= 51200 and 0 < a.get("returned", 0) < 100 and a.get("truncated") is True, "sizes %d %d returned %s" % (size(a), size(b), a.get("returned")))
    small = {"value": [item(i) for i in range(5)]}
    a, b = both(payload=small)
    say("control: 5 items returned equal to Graph's answer, no truncated key", a == small and b == small and "truncated" not in a)
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
