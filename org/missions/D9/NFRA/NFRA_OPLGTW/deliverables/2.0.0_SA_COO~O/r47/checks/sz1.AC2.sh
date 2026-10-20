#!/usr/bin/env bash
# OPLGTW OG-sz-1 AC2 (round 47, Z-S413 P6 and P7): the two oversize tools are projected, probed through their registered tools with fakes (no network, no S3).
#  P6: mdpf_get_aggregate_aua (the portal_index integration): the projection is applied in PortalIndexIntegration._run, AFTER answer() returns, so answer() itself is unchanged.
#      A 6000-row ascending daily series inside `data` is served <= 51200 indented bytes with the NEWEST rows kept (the last row equals the source's last row),
#      `status`, `tool`, `bucket`, `key`, `as_of`, `as_of_field` intact, `data` a dict, `truncated` true, `projected_to_bytes` equal to the indented size, and
#      `trimmed["data.series"] == {"total": 6000, "returned": <n>, "kept": "newest"}`.
#  P7: opal_discover (the opal_discover integration): 137 matches are served <= 51200 indented bytes, the FIRST matches kept in rank order, `matches` still a list,
#      `truncated` true, `matches_total` 137 and `matches_returned` equal to the length served.
#  Controls: a small answer of each tool is returned equal to what the function produced, with no `truncated` key.
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
class Mcp:
    def __init__(self): self.fns = {}
    def tool(self, *a, **k):
        def deco(fn):
            self.fns[fn.__name__] = fn
            return fn
        return deco
try:
    from app.integrations.portal_index import integration as pi
    from app.integrations.opal_discover import integration as od
except Exception as exc:
    print("import failed: %s" % type(exc).__name__); print("NO"); sys.exit(0)

# ---- P6
rows = [{"date": "%04d-%02d-%02d" % (2000 + i // 372, (i // 31) % 12 + 1, i % 31 + 1), "aua": 1000.0 + i, "flows": 3.5 * i} for i in range(6000)]
def make(rows_):
    return {"status": "ok", "tool": "mdpf_get_aggregate_aua", "bucket": "b", "key": "k", "as_of": "2026-10-16", "as_of_field": "asOf",
            "data": {"asOf": "2026-10-16", "series": rows_}}
def run_p6(payload):
    inst = pi.PortalIndexIntegration(getter=lambda b, k: None)
    m = Mcp()
    o_ans, o_run = pi.answer, pi.run_integration_tool
    pi.answer = lambda tool, getter, principal, as_of="", **kw: json.loads(json.dumps(payload))
    pi._principal = lambda: ("t", "o")
    pi.run_integration_tool = lambda spec, name, args, fn, credential_provider=None: fn(None)
    try:
        inst.register(m)
        return m.fns["mdpf_get_aggregate_aua"]("global", "")
    finally:
        pi.answer, pi.run_integration_tool = o_ans, o_run
try:
    r = run_p6(make(rows))
    s = (r.get("data") or {}).get("series") or []
    say("P6 6000-row series: indented size <= 51200", size(r) <= 51200, "size %d" % size(r))
    say("P6 envelope fields intact, data a dict", all(r.get(k) == make(rows)[k] for k in ("status", "tool", "bucket", "key", "as_of", "as_of_field")) and isinstance(r.get("data"), dict) and (r["data"].get("asOf") == "2026-10-16"))
    say("P6 newest rows kept, a shorter non-empty series", 0 < len(s) < 6000 and s[-1] == rows[-1], "returned %d" % len(s))
    say("P6 truncated true, projected_to_bytes equals the indented size", r.get("truncated") is True and r.get("projected_to_bytes") == size(r), "field %r size %d" % (r.get("projected_to_bytes"), size(r)))
    say("P6 trimmed note names the path, total and kept side", (r.get("trimmed") or {}).get("data.series") == {"total": 6000, "returned": len(s), "kept": "newest"}, "trimmed %r" % (r.get("trimmed"),))
    small = make(rows[:5])
    r2 = run_p6(small)
    say("P6 control: a 5-row answer equals the function's output, no truncated key", r2 == small and "truncated" not in r2)
except Exception as exc:
    print("P6 probe raised %s: %s" % (type(exc).__name__, str(exc)[:140])); ok = False

# ---- P7
def match(i):
    return {"dataset": "ds_%03d" % i, "servable": i % 3 == 0, "freshness": {"field": "asOf", "latest": "2026-10-16", "claim": "measured"},
            "caveats": ["c" * 120] * 6, "next_tool": "gateway_query_catalog", "description": "d" * 2200}
def run_p7(n):
    inst = od.OpalDiscoverIntegration()
    m = Mcp()
    payload = {"subject": "client account holdings", "catalog": {"version": "v", "home": "app/refs/DATA_CATALOG.yaml"}, "catalogued": True,
               "matches": [match(i) for i in range(n)], "answer": "'client account holdings' is catalogued: %d dataset(s)." % n}
    o_disc, o_run, o_pr = od.discover, od.run_integration_tool, od._principal
    od.discover = lambda subject, *a, **k: json.loads(json.dumps(payload))
    od._principal = lambda: ("t", "o")
    od.run_integration_tool = lambda spec, name, args, fn, credential_provider=None: fn(None)
    try:
        inst.register(m)
        return m.fns["opal_discover"]("client account holdings"), payload
    finally:
        od.discover, od.run_integration_tool, od._principal = o_disc, o_run, o_pr
try:
    r, src = run_p7(137)
    ms = r.get("matches")
    say("P7 137 matches: indented size <= 51200", size(r) <= 51200, "size %d" % size(r))
    say("P7 the first matches kept in rank order, matches a list", isinstance(ms, list) and 0 < len(ms) < 137 and ms == src["matches"][:len(ms)], "returned %s" % (len(ms) if isinstance(ms, list) else None))
    say("P7 truncated true, matches_total 137, matches_returned equals the length", r.get("truncated") is True and r.get("matches_total") == 137 and r.get("matches_returned") == (len(ms) if isinstance(ms, list) else -1), "total %r returned %r" % (r.get("matches_total"), r.get("matches_returned")))
    r2, src2 = run_p7(3)
    say("P7 control: a 3-match answer equals the function's output, no truncated key", r2 == src2 and "truncated" not in r2)
except Exception as exc:
    print("P7 probe raised %s: %s" % (type(exc).__name__, str(exc)[:140])); ok = False
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
