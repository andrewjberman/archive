"""WS2-c AC1 -- the security dialog's trade list follows the selected window and sits behind a closed disclosure.

Server side: render._trade_list() wraps the list in a <details> with no `open` attribute, and no static heading says 365 days.
Page script (run in node, as test_r17nc1 runs it): window.rfChart.tradehead(rg) names the window, and
window.rfChart.tradelines(markers, from) keeps only markers whose end is on or after `from`.

Run from the repository root:  python org/missions/D5/ETFS/ETFS_RIVALS/deliverables/2.0.0_SA_COO~V1/ws2/checks/ws2-c.AC1.py
Last line: `AC1 RESULT: PASS 0 failures` or `AC1 RESULT: FAIL <n> (<arms>)`.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 9))
sys.path[:0] = [ROOT, os.path.join(ROOT, "data", "etfs", "scripts")]

from rivalfunds import render  # noqa: E402

fails = []


def check(arm, ok, detail):
    print(("OK   " if ok else "FAIL ") + f"({arm}) {detail}", flush=True)
    if not ok:
        fails.append(arm)


# (a) the server-rendered list is behind a closed disclosure and claims no fixed window
html = render._trade_list([])
check("a", "<details" in html and "<details open" not in html and " open>" not in html.split("<summary")[0]
      and "365 days" not in html, f"_trade_list([]) -> {html[:200]!r}")

# (b) the page script names the window and filters the markers to it
JS = r"""
const vm = require("vm");
const src = require("fs").readFileSync(process.argv[2], "utf8");
const ctx = {document: {addEventListener() {}}, window: {}};
vm.runInNewContext(src, ctx);
const c = ctx.window.rfChart || {};
const M = [{side: "buy", start: "2026-06-01", end: "2026-06-02", usd: 1000, bps: 30, n_trades: 1},
           {side: "sell", start: "2026-10-05", end: "2026-10-06", usd: 2000, bps: 40, n_trades: 1}];
const out = {
  head: ["R30", "R90", "R365"].map(r => typeof c.tradehead === "function" ? c.tradehead(r) : null),
  n30: typeof c.tradelines === "function" ? c.tradelines(M, "2026-09-07").length : null,
  n365: typeof c.tradelines === "function" ? c.tradelines(M, "2025-10-07").length : null};
console.log(JSON.stringify(out));
"""
node = shutil.which("node")
if not node:
    check("b", False, "node is not on PATH")
else:
    with tempfile.TemporaryDirectory() as td:
        js, page = os.path.join(td, "t.js"), os.path.join(td, "page.js")
        open(js, "w", encoding="utf-8").write(JS)
        open(page, "w", encoding="utf-8").write(render.CHART_SCRIPT)
        r = subprocess.run([node, js, page], capture_output=True, text=True, timeout=60)
        try:
            o = json.loads(r.stdout.strip().splitlines()[-1])
        except Exception:  # noqa: BLE001
            o = {"error": (r.stderr or r.stdout)[-300:]}
        check("b", o.get("head") == ["Trades in the last 30 days", "Trades in the last 90 days", "Trades in the last 365 days"]
              and o.get("n30") == 1 and o.get("n365") == 2, f"node -> {o}")

print("AC1 RESULT: PASS 0 failures" if not fails else f"AC1 RESULT: FAIL {len(fails)} ({', '.join(fails)})")
