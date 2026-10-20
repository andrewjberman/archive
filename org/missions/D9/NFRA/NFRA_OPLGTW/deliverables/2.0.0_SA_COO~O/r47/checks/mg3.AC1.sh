#!/usr/bin/env bash
# OPLGTW OG-mg-3 AC1 (round 47, Z-S425 / the CTO's item 3): app/inflight_guard.py bounds the number of MCP tool calls running at once, process-wide.
# API fixed by the order: MAX_INFLIGHT (26), QUEUE_WAIT_S (20.0), class Busy (attribute code == "gateway_busy"), class InflightGuard(limit, wait_s) with
# async context manager slot(tool) and snapshot() -> {"limit", "inflight", "waiting", "refused", "peak"}, and the process-wide instance `guard`.
# Scenarios (limit 2): (a) short wait: five calls hold a slot 0.5 s, wait 0.3 s -> exactly two run, three are refused Busy, peak 2, inflight 0 after;
# (b) long wait: five calls hold 0.2 s, wait 3 s -> all five complete, none refused, peak 2 (queued, not refused);
# (c) a body that raises releases its slot (inflight 0 afterwards and a following call runs).
. "$(dirname "$0")/../../trnspt/checks/_root.sh"
out=$(cd "$GW" && timeout 100 python3 -I - <<'EOF'
import sys, asyncio
sys.path.insert(0, ".")
ok = True
def say(label, cond, extra=""):
    global ok
    ok = ok and bool(cond)
    print("%s: %s%s" % (label, "ok" if cond else "NO", (" (" + extra + ")") if extra else ""))
try:
    from app import inflight_guard as ig
except Exception as exc:
    print("import failed: %s" % type(exc).__name__); print("NO"); sys.exit(0)
say("module constants", ig.MAX_INFLIGHT == 26 and ig.QUEUE_WAIT_S == 20.0 and getattr(ig.Busy, "code", None) == "gateway_busy" and isinstance(ig.guard, ig.InflightGuard) and ig.guard.snapshot()["limit"] == 26, "limit %r" % ig.guard.snapshot().get("limit"))

async def call(g, hold, results):
    try:
        async with g.slot("t"):
            await asyncio.sleep(hold)
        results.append("ran")
    except ig.Busy:
        results.append("busy")

async def scenario(limit, wait_s, hold, n):
    g = ig.InflightGuard(limit, wait_s)
    results = []
    await asyncio.gather(*[call(g, hold, results) for _ in range(n)])
    return results, g.snapshot()

res, snap = asyncio.run(scenario(2, 0.3, 0.5, 5))
say("short wait: two ran, three refused, peak 2, inflight 0", res.count("ran") == 2 and res.count("busy") == 3 and snap["peak"] == 2 and snap["inflight"] == 0 and snap["refused"] == 3, "results %s snapshot %s" % (sorted(res), snap))
res, snap = asyncio.run(scenario(2, 3.0, 0.2, 5))
say("long wait: five ran, none refused, peak 2", res.count("ran") == 5 and snap["refused"] == 0 and snap["peak"] == 2 and snap["inflight"] == 0, "results %s snapshot %s" % (sorted(res), snap))

async def raising():
    g = ig.InflightGuard(1, 0.2)
    try:
        async with g.slot("t"):
            raise ValueError("boom")
    except ValueError:
        pass
    after = g.snapshot()["inflight"]
    got = []
    await call(g, 0.0, got)
    return after, got
after, got = asyncio.run(raising())
say("a raising body releases its slot", after == 0 and got == ["ran"], "inflight %s next %s" % (after, got))
print("OK" if ok else "NO")
EOF
)
rc=$?
out=$(printf '%s' "$out" | tr -d '\r')
printf '%s\n' "$out" | sed '$d'
[ "$rc" = 0 ] && [ "$(printf '%s\n' "$out" | tail -1)" = OK ] && { echo "RESULT: PASS"; exit 0; }
echo "RESULT: FAIL"; exit 1
