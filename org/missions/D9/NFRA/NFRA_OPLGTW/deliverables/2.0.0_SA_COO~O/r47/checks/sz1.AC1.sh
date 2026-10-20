#!/usr/bin/env bash
# OPLGTW OG-sz-1 AC1 (round 47, Z-S413 P4 and P5): harvest_typed.project() measures the size the way the server SERVES the reply (json indent=2, UTF-8 bytes)
# and never nulls a whole field.
#  P4: a 3000-row list answer projects to <= 51200 indented bytes, truncated true, projected_to_bytes equal to the indented size of the result.
#  P5: a non-list field (a dict of long lists; a long string) is shrunk INSIDE, never set to None: the answer fits, the dict keeps every key with its lists shortened,
#      the string stays a non-empty string; the envelope keys are never dropped.
#  Controls: a small answer is returned equal to its input, with no truncated key.
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 100 python3 -I - <<'EOF'
import sys, json
sys.path.insert(0, ".")
from app import harvest_typed as ht
ok = True
def size(o):
    return len(json.dumps(o, indent=2, default=str).encode("utf-8"))
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
env = {"as_of": "2026-10-16", "source_keys": ["k"], "denominator": 1, "absent_reason": None}
big = dict(env, rows=[{"k": i, "v": "x" * 40} for i in range(3000)])
r = ht.project(big, 51200)
say("P4 3000-row list: indented size <= 51200", size(r) <= 51200, "size %d" % size(r))
say("P4 truncated true, rows kept a non-empty prefix, envelope keys intact", r.get("truncated") is True and 0 < len(r["rows"]) < 3000 and all(k in r for k in env))
say("P4 projected_to_bytes equals the indented size", r.get("projected_to_bytes") == size(r), "field %r size %d" % (r.get("projected_to_bytes"), size(r)))
macro = {"series": {"a": [float(i) for i in range(6000)], "b": [float(i) for i in range(6000)]}, "note": "n"}
r2 = ht.project(dict(env, macro=macro), 51200)
m = r2.get("macro")
say("P5 dict-of-lists field: not None, a dict, every key kept", isinstance(m, dict) and set(m) == {"series", "note"} and isinstance(m["series"], dict) and set(m["series"]) == {"a", "b"}, "macro %s" % type(m).__name__)
say("P5 dict-of-lists field: fits and says truncated", size(r2) <= 51200 and r2.get("truncated") is True, "size %d" % size(r2))
say("P5 the lists inside kept a non-empty prefix or suffix", isinstance(m, dict) and 0 < len(m["series"]["a"]) < 6000 and 0 < len(m["series"]["b"]) < 6000)
r3 = ht.project(dict(env, blob="x" * 200000), 51200)
say("P5 long string field: a non-empty shorter string, fits", isinstance(r3.get("blob"), str) and 0 < len(r3["blob"]) < 200000 and size(r3) <= 51200, "len %s size %d" % (len(r3.get("blob") or ""), size(r3)))
small = dict(env, rows=[1, 2, 3])
r4 = ht.project(small, 51200)
say("control: a small answer is equal to its input, no truncated key", r4 == small and "truncated" not in r4)
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
