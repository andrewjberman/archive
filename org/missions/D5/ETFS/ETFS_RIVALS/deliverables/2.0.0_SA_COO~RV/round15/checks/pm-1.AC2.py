"""RIV-pm-1 AC2 (PRD v0.18 FWD-22): the page's one script draws no curve where there is no curve, and says so.

Interface (prescribed, from the cell), all in `render.CHART_SCRIPT`:
  - `nohist(s)` returns the no-history sentence NH ("No price history is stored for this holding yet.", held ONCE in the
    script text) not only when `s.currency == null` (where the object's `source_words` still wins) but ALSO when the security
    has a stored currency and NOT ONE point with a non-null price (`s.points` empty or every price null); in that second case
    the plain sentence is returned and the object's `source_words` is not used;
  - a new pure function `window.rfChart.curve(pl)` takes what `plan(s, from, to)` returns and answers `true` only when the
    range holds TWO OR MORE priced points; for a range where it is false the script draws no svg and prints exactly FEW
    ("Fewer than two prices on file in this range.", held ONCE in the script text). A range with two or more draws as today.
Runs the script under node, as tl-1.AC1 does (vm context with a stub document and window; "@DAY@" and "@FAIL@" substituted).
Arm (g) goes one step further than the text: the stub document keeps the script's two listeners, a stub fetch hands the
script a chart object, and the check counts the `svg` elements the script's own draw creates and reads every text it writes.

Fixture: security objects typed in the node snippet; chart object asof 2026-09-29, R30 from 2026-08-30. ONE has one priced
point in R30 (and one in June, outside it), TWO has two in R30, ZERO has none in R30 (one in June), NULLS is a USD listing
whose points are all null.
  - (a) nohist({currency "USD", points all null, source_words "x"}) and nohist({currency "JPY", points []}) both return NH;
  - (b) nohist({currency null, source_words "from the object"}) still returns "from the object", and nohist of a USD
    security with one priced point returns null;
  - (c) `curve` is a function: curve(plan(ONE)) is false, curve(plan(TWO)) is true, curve(plan(ZERO)) is false (strict
    booleans; plan called with the R30 bounds);
  - (d) NH appears exactly once in the script text, and FEW appears exactly once;
  - (e) nc-1.AC1, tl-1.AC1 and md-1.AC2 still end `PASS 0 failures` (each run as its own process from the worktree root;
    md-1.AC2 is where `render.validate` admits the page carrying the script);
  - (f) control: node is on the PATH, the script exposes plan, nohist and words, plan finds 1 / 2 / 0 priced points in the
    three ranges, and the script's own draw, run through the stub document, creates one svg for TWO. (Measured and printed,
    not asserted, because the build changes it: nohist of NULLS is null at the base.)
  - (g) through the script's own draw: ONE creates no svg and one text written is exactly FEW; ZERO creates no svg; NULLS
    creates no svg and the status line reads NH; TWO still creates one svg.
FAIL at base b1a4837abe: (a), (c), (d), (g) FAIL (nohist null for a priced-less dollar listing; no curve; no FEW sentence; one
point draws an svg); (b), (e), (f) PASS."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

NH = "No price history is stored for this holding yet."
FEW = "Fewer than two prices on file in this range."
EARLIER = ("nc-1.AC1", "tl-1.AC1", "md-1.AC2")
JS = r"""
const vm = require("vm");
const src = require("fs").readFileSync(process.argv[1], "utf8");
const listeners = {};
let made = [];
function el(tag) {
  const e = {tagName: String(tag).toUpperCase(), children: [], attrs: {}, textContent: "", className: "", style: {}, parentNode: null,
    nextSibling: null, classList: {add() {}, remove() {}},
    appendChild(k) { this.children.push(k); k.parentNode = this; return k; },
    insertBefore(k) { this.children.push(k); k.parentNode = this; return k; },
    removeChild(k) { this.children = this.children.filter(x => x !== k); return k; },
    setAttribute(a, b) { this.attrs[a] = b; }, getAttribute(a) { return a in this.attrs ? this.attrs[a] : null; },
    removeAttribute(a) { delete this.attrs[a]; }, addEventListener() {}, querySelector() { return null; },
    querySelectorAll() { return []; }, getBoundingClientRect() { return {left: 0, top: 0, width: 600, height: 200}; }};
  Object.defineProperty(e, "firstChild", {get() { return this.children[0] || null; }});
  made.push(e);
  return e;
}
const objs = {};
const ctx = {
  document: {addEventListener(t, f) { (listeners[t] = listeners[t] || []).push(f); }, createElement: el, createElementNS: (ns, t) => el(t)},
  window: {},
  fetch(u) { const f = decodeURIComponent(String(u).split("/").pop()); return Promise.resolve({ok: true, status: 200, json() { return Promise.resolve(objs[f]); }}); },
};
let loaded = null;
try { vm.runInNewContext(src, ctx); } catch (e) { loaded = String(e); }
const r = ctx.window.rfChart || {};
const FROM = "2026-08-30", TO = "2026-09-29";
const sec = (pts, ccy) => ({name: "n", currency: ccy === undefined ? "USD" : ccy, source_words: "x", points: pts, gaps: [], markers: []});
const JUNE = ["2026-06-01", 11.0, "m"];
const S = {
  ONE: sec([JUNE, ["2026-09-01", 10.0, "m"], ["2026-09-02", null, null]]),
  TWO: sec([JUNE, ["2026-09-01", 10.0, "m"], ["2026-09-02", 10.5, "m"]]),
  ZERO: sec([JUNE, ["2026-09-01", null, null], ["2026-09-02", null, null]]),
  NULLS: sec([["2026-09-01", null, null], ["2026-09-02", null, null]]),
};
const safe = f => { try { const x = f(); return x === undefined ? "<undefined>" : x; } catch (e) { return "<error " + e + ">"; } };
const out = {loaded: loaded, has: {plan: typeof r.plan === "function", nohist: typeof r.nohist === "function",
                                   words: typeof r.words === "function", curve: typeof r.curve === "function"}};
out.nohist = {
  nulls: safe(() => r.nohist({currency: "USD", points: [["2026-09-01", null, null]], source_words: "x"})),
  empty: safe(() => r.nohist({currency: "JPY", points: []})),
  object: safe(() => r.nohist({currency: null, source_words: "from the object"})),
  priced: safe(() => r.nohist({currency: "USD", points: [["2026-09-01", 10.0, "m"]]})),
};
out.npts = {}; out.curve = {};
for (const k of ["ONE", "TWO", "ZERO"]) {
  out.npts[k] = safe(() => r.plan(S[k], FROM, TO).pts.length);
  out.curve[k] = safe(() => r.curve(r.plan(S[k], FROM, TO)));
}
async function drawn(k) {
  made = [];
  const status = el("p");
  const frame = el("div");
  frame.attrs = {"data-chart-fund": k, "data-chart-key": "K"};
  frame.querySelector = function (q) {
    if (q.indexOf("data-chart-status") >= 0) return status;
    if (q.indexOf("rf-ch-out") >= 0) return this.children.filter(x => String(x.className).indexOf("rf-ch-out") >= 0)[0] || null;
    return null;
  };
  objs[k] = {fund: k, asof: TO, generated_at: "g", ranges: {R30: FROM, R90: "2026-07-01", R365: "2025-09-29"}, securities: {K: S[k]}};
  const dialog = {getAttribute(a) { return a === "data-sec-dialog" ? "K" : null; }, querySelectorAll() { return [frame]; }};
  let err = null;
  try { (listeners.toggle || []).forEach(f => f({target: dialog, newState: "open"})); } catch (e) { err = String(e); }
  for (let i = 0; i < 20; i++) await new Promise(res => setImmediate(res));
  return {err: err, svg: made.filter(x => x.tagName === "SVG").length, status: status.textContent,
          texts: made.map(x => x.textContent).filter(t => t)};
}
(async () => {
  out.drawn = {};
  for (const k of ["ONE", "TWO", "ZERO", "NULLS"]) {
    try { out.drawn[k] = await drawn(k); } catch (e) { out.drawn[k] = {err: String(e), svg: null, status: "", texts: []}; }
  }
  console.log(JSON.stringify(out));
})();
"""


def node_run(script_text: str):
    node = shutil.which("node")
    if node is None:
        return None, "node is not on the PATH"
    with tempfile.TemporaryDirectory(prefix="rv_pm1_") as d:
        f = pathlib.Path(d) / "chart.js"
        f.write_text(script_text, encoding="utf-8")
        p = subprocess.run([node, "-e", JS, str(f)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        if p.returncode != 0:
            return None, f"node rc {p.returncode}: {(p.stderr or '').strip()[:300]}"
        try:
            return json.loads(p.stdout), None
        except Exception as e:  # noqa: BLE001 -- an unparseable run is a failed arm, not a crash
            return None, f"{type(e).__name__}: {e}"


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    script = (getattr(render, "CHART_SCRIPT", "") or "").replace("@DAY@", "2026-09-30").replace("@FAIL@", getattr(render, "CHART_FAIL", "x"))
    out, err = node_run(script)
    out = out or {}
    has, noh, npts, curve = out.get("has") or {}, out.get("nohist") or {}, out.get("npts") or {}, out.get("curve") or {}
    drawn = {k: (x if isinstance(x, dict) else {}) for k, x in (out.get("drawn") or {}).items()}
    print("node:", err or "ran", "| script load error:", out.get("loaded"), "| exposes:", has)
    print("nohist: USD all null ->", repr(noh.get("nulls")), "| JPY no points ->", repr(noh.get("empty")),
          "| currency null ->", repr(noh.get("object")), "| USD one priced ->", repr(noh.get("priced")))
    print("priced points in R30 by plan:", npts, "| curve(plan):", curve)
    for k in ("ONE", "TWO", "ZERO", "NULLS"):
        d = drawn.get(k) or {}
        print(f"  draw {k}: svg {d.get('svg')} | status {d.get('status')!r} | texts {(d.get('texts') or [])[:6]} | error {d.get('err')}")

    v.check(noh.get("nulls") == NH and noh.get("empty") == NH,
            "(a) nohist returns the no-history sentence for a stored-currency security with no priced point (all null, or no points)")
    v.check(noh.get("object") == "from the object" and noh.get("priced") is None and "priced" in noh,
            "(b) nohist still returns the object's words when the currency is null, and null for a dollar security with a price")
    v.check(has.get("curve") is True and curve.get("ONE") is False and curve.get("TWO") is True and curve.get("ZERO") is False,
            "(c) rfChart.curve is a function: false for one priced point in the range, true for two, false for none")
    print("script text: no-history sentence count", script.count(NH), "| fewer-than-two sentence count", script.count(FEW))
    v.check(script.count(NH) == 1 and script.count(FEW) == 1,
            "(d) the script holds the no-history sentence exactly once and the fewer-than-two sentence exactly once")

    lines = {}
    for name in EARLIER:
        p = subprocess.run([sys.executable, str(HERE / f"{name}.py")], cwd=str(c.ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=1500)
        last = [ln for ln in (p.stdout or "").splitlines() if "RESULT:" in ln]
        lines[name] = last[-1].strip() if last else f"no RESULT line (rc {p.returncode})"
        print(f"  {name}: {lines[name]}")
    v.check(all(ln.endswith("RESULT: PASS 0 failures") for ln in lines.values()),
            "(e) nc-1.AC1, tl-1.AC1 and md-1.AC2 still end PASS 0 failures")

    two = drawn.get("TWO") or {}
    print("control: node", shutil.which("node") is not None, "| base reading of arm (a), nohist(USD all null) is null today:",
          noh.get("nulls") is None and "nulls" in noh)
    v.check(shutil.which("node") is not None and out.get("loaded") is None and has.get("plan") is True and has.get("nohist") is True
            and has.get("words") is True and npts == {"ONE": 1, "TWO": 2, "ZERO": 0} and two.get("svg") == 1 and not two.get("err"),
            "(f) control: node runs the script, it exposes plan, nohist and words, plan finds 1 / 2 / 0 priced points, and the "
            "script's own draw creates one svg for a two-price range")

    one, zero, nulls = drawn.get("ONE") or {}, drawn.get("ZERO") or {}, drawn.get("NULLS") or {}
    said = [one.get("status")] + list(one.get("texts") or [])
    v.check(one.get("svg") == 0 and FEW in said and zero.get("svg") == 0 and nulls.get("svg") == 0 and nulls.get("status") == NH
            and two.get("svg") == 1 and not any(d.get("err") for d in (one, zero, nulls, two)),
            "(g) drawn by the script: one price in the range -> no svg and the fewer-than-two sentence; none -> no svg; a "
            "dollar listing with no price at all -> no svg and the no-history sentence as its status; two prices -> one svg")


failures = c.guarded("AC2", run)
print("AC2 RESULT: PASS 0 failures" if failures == 0 else f"AC2 RESULT: FAIL {failures} failures")
sys.exit(0 if failures == 0 else 1)
