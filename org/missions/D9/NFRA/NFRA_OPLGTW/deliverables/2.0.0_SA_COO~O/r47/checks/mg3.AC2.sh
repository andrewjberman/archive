#!/usr/bin/env bash
# OPLGTW OG-mg-3 AC2 (round 47): the guard is hooked into the ONE dispatch chokepoint of every tool, app/tools.py _PolicyGuardedMCP.call_tool, AFTER the entitlement
# denial (a denied call takes no slot) and around the tool run. Probe: the entitlement denial is patched to "allowed", the parent FastMCP.call_tool is patched to a fake that
# sleeps 0.4 s and records the concurrency it saw, and `app.inflight_guard.guard` is replaced by InflightGuard(2, 0.1). Six concurrent calls ->
#   at most 2 ran at once; the 4 refused calls return a CallToolResult with isError true whose structuredContent has error and code "gateway_busy" and an integer
#   retry_after_s; the refusal is audited (audit.log_call with outcome "denied" and the reason "gateway_busy") once per refused call;
#   a denied call (entitlement denial returns a dict) returns the denial exactly as before and takes NO slot (snapshot peak stays 0 for a run of denied calls);
#   a follow-up single call after the burst runs normally (slot released).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 110 python3 -I - <<'EOF'
import sys, asyncio, json
sys.path.insert(0, ".")
ok = True
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app import tools, inflight_guard as ig, data_entitlement as de, audit
    from mcp.server.fastmcp import FastMCP
    from mcp.types import CallToolResult
except Exception as exc:
    print("import failed: %s %s" % (type(exc).__name__, str(exc)[:100])); print("NO"); sys.exit(0)
state = {"now": 0, "max": 0, "ran": 0}
async def fake_call(self, name, arguments):
    state["now"] += 1
    state["max"] = max(state["max"], state["now"])
    try:
        await asyncio.sleep(0.4)
        state["ran"] += 1
        return {"ok": True}
    finally:
        state["now"] -= 1
FastMCP.call_tool = fake_call
logged = []
audit.log_call = lambda *a, **k: logged.append((a, k))
de.tool_denial = lambda name, principal=None: None
de.remember_allowed = lambda name, principal=None: None
de.forget = lambda token: None
ig.guard = ig.InflightGuard(2, 0.1)
async def burst(n):
    return await asyncio.gather(*[tools.mcp.call_tool("whoami", {}) for _ in range(n)], return_exceptions=True)
res = asyncio.run(burst(6))
errs = [r for r in res if isinstance(r, Exception)]
busy = [r for r in res if isinstance(r, CallToolResult)]
okr = [r for r in res if isinstance(r, dict)]
say("six concurrent calls: 2 ran, 4 refused, no exception", len(okr) == 2 and len(busy) == 4 and not errs, "ran %d refused %d raised %s" % (len(okr), len(busy), [type(e).__name__ for e in errs]))
say("at most 2 ran at once", state["max"] <= 2, "max %d" % state["max"])
sc = [(r.isError, (r.structuredContent or {}).get("code"), (r.structuredContent or {}).get("error"), isinstance((r.structuredContent or {}).get("retry_after_s"), int)) for r in busy]
say("refusals: isError true, code and error gateway_busy, integer retry_after_s", sc and all(x == (True, "gateway_busy", "gateway_busy", True) for x in sc), "first %r" % ((sc[0] if sc else None),))
refused_logs = [1 for a, k in logged if "gateway_busy" in repr(a) + repr(k)]
say("each refusal audited once", len(refused_logs) == 4, "audit rows naming gateway_busy %d" % len(refused_logs))
say("slots all released after the burst", ig.guard.snapshot()["inflight"] == 0, "snapshot %s" % ig.guard.snapshot())
# denied calls take no slot
denial = {"error": "entitlement_denied", "code": "entitlement_denied"}
de.tool_denial = lambda name, principal=None: denial
ig.guard = ig.InflightGuard(1, 0.1)
res2 = asyncio.run(burst(5))
dres = [r for r in res2 if isinstance(r, CallToolResult) and (r.structuredContent or {}).get("code") == "entitlement_denied"]
say("denied calls: five denials as before, no slot taken", len(dres) == 5 and ig.guard.snapshot()["peak"] == 0, "denials %d snapshot %s" % (len(dres), ig.guard.snapshot()))
de.tool_denial = lambda name, principal=None: None
ig.guard = ig.InflightGuard(2, 0.1)
res3 = asyncio.run(burst(1))
say("a single call after the burst runs", res3 == [{"ok": True}], "got %r" % (res3,))
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
