"""RIV-cu-1 AC1 (PRD v0.18 FWD-22; analysis round 22 ADDENDUM 1 and 2, Andrew-direct 2026-10-07): the dialog chart's x-axis is
dated -- a pure `rfChart.ticks(pl)` and one svg `text[data-tick]` per tick.

Interface (prescribed, interface item 1 of the cell), in `render.CHART_SCRIPT`:
  - `window.rfChart.ticks(pl)` takes what `rfChart.plan(s, from, to)` returns (`pl.a`, `pl.b` the range's first and last day
    numbers) and returns an array of 4 to 7 objects `{x, label}`: `x` a day number with `pl.a <= x <= pl.b`, strictly
    increasing; `label` a date a reader can place: day and month ("8 Sep") for a range of 100 days or fewer, month and two-digit
    year ("Oct 25") for a longer one; no two labels equal;
  - the script's own draw writes one svg `text` per tick carrying the attribute `data-tick`, that label as its text, under the plot.
Runs the script under node in a vm context with a stub document and window, as pm-1.AC2 does; the stub keeps parent/children
order, attributes, classes, text and event listeners, the script's two document listeners (toggle, click) are fired as a browser
would, a stub fetch hands the script one chart object, and the check reads what the script's own draw built.

Fixture: one USD security K, a priced point every day from 2025-09-29 to 2026-09-29, two markers, chart object asof 2026-09-29
with R30 from 2026-08-30, R90 from 2026-07-01 and R365 from 2025-09-29 (so the plans span 30, 90 and 365 days).
  - (a) `rfChart.ticks` is a function and, for each of the three plans, returns an array of 4 to 7 objects with a finite number
    `x` and a non-empty string `label`;
  - (b) for each plan every `x` lies in `[pl.a, pl.b]` and the x values are strictly increasing;
  - (c) label form by range length: the 30-day and the 90-day plans give "<day> <Mon>" ("8 Sep"), the 365-day plan gives
    "<Mon> <two digits>" ("Oct 25");
  - (d) within one plan no two labels are equal;
  - (e) each label names the date its own `x` falls on (the day and month, or the month and the two-digit year, of the UTC date
    of day number x -- floor, round or ceil of x);
  - (f) the script's own draw (opened on the dialog, then the 90-day and 365-day buttons clicked) writes, inside its svg, one
    `text` carrying `data-tick` per tick of `ticks(plan)` with the same labels as its text (as a multiset), each placed at a
    numeric x inside the 600-wide viewBox and a numeric y greater than every vertex y of the curve (under the plot);
  - (g) control: node runs, the script loads without error and exposes plan, words and curve, plan finds priced points in all three
    ranges, and the script's own draw creates exactly one svg for each of the three ranges (so the stub reaches the draw).
FAIL at base bcf0b16c75: (a), (b), (c), (d), (e), (f) FAIL (no rfChart.ticks -- 'r.ticks is not a function' -- and no text[data-tick] in the
drawn svg); (g) PASSES (node runs the script, one svg per range). The simulated conforming build passes (a) to (g)."""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, timedelta

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
RANGES = ("R30", "R90", "R365")
JS = r"""
const vm = require("vm");
const src = require("fs").readFileSync(process.argv[2], "utf8");
const ERRS = [];
let timers = [];
function flush() {
  for (let n = 0; n < 20 && timers.length; n++) {
    const t = timers; timers = [];
    t.forEach(f => { try { f(); } catch (e) { ERRS.push("timer: " + e); } });
  }
}
const tokens = s => String(s || "").split(/\s+/).filter(Boolean);
function parseCompound(s) {
  const c = {tag: null, cls: [], attrs: []};
  const m = /^[a-zA-Z][\w-]*/.exec(s);
  if (m) { c.tag = m[0].toLowerCase(); s = s.slice(m[0].length); }
  const re = /\.([\w-]+)|\[([\w-]+)(?:=(?:"([^"]*)"|'([^']*)'|([^\]]*)))?\]/g;
  let r;
  while ((r = re.exec(s))) {
    if (r[1]) c.cls.push(r[1]);
    else c.attrs.push([r[2], r[3] !== undefined ? r[3] : r[4] !== undefined ? r[4] : r[5]]);
  }
  return c;
}
function matchOne(e, c) {
  if (!e || !e.attrs) return false;
  if (c.tag && String(e.tagName).toLowerCase() !== c.tag) return false;
  const have = tokens(e.className);
  if (!c.cls.every(x => have.includes(x))) return false;
  return c.attrs.every(([k, v]) => k in e.attrs && (v === undefined || e.attrs[k] === v));
}
function matchChain(e, chain) {
  const parts = chain.split(/\s*>\s*|\s+/).filter(Boolean).map(parseCompound);
  if (!parts.length || !matchOne(e, parts[parts.length - 1])) return false;
  let i = parts.length - 2;
  for (let n = e.parentNode; n && i >= 0; n = n.parentNode) if (matchOne(n, parts[i])) i--;
  return i < 0;
}
function walk(n, fn) { fn(n); n.children.forEach(k => walk(k, fn)); }
class El {
  constructor(tag, ns) {
    this.tagName = ns ? String(tag) : String(tag).toUpperCase();
    this.attrs = {}; this.children = []; this.parentNode = null; this._text = ""; this._l = {}; this.nodeType = 1;
    const self = this;
    this.style = {setProperty(k, v) { this[k] = v; }, removeProperty(k) { delete this[k]; }, getPropertyValue(k) { return this[k] || ""; }};
    this.classList = {
      add(...c) { const t = tokens(self.className); c.forEach(x => { if (!t.includes(x)) t.push(x); }); self.className = t.join(" "); },
      remove(...c) { self.className = tokens(self.className).filter(x => !c.includes(x)).join(" "); },
      contains(c) { return tokens(self.className).includes(c); },
      toggle(c, f) { const want = f === undefined ? !tokens(self.className).includes(c) : !!f; if (want) this.add(c); else this.remove(c); return want; },
    };
    this.dataset = new Proxy({}, {
      get(_, k) { const a = "data-" + String(k).replace(/[A-Z]/g, m => "-" + m.toLowerCase()); return a in self.attrs ? self.attrs[a] : undefined; },
      set(_, k, v) { self.attrs["data-" + String(k).replace(/[A-Z]/g, m => "-" + m.toLowerCase())] = String(v); return true; },
    });
  }
  get className() { return "class" in this.attrs ? this.attrs["class"] : ""; }
  set className(v) { this.attrs["class"] = String(v); }
  get hidden() { return "hidden" in this.attrs; }
  set hidden(v) { if (v) this.attrs.hidden = ""; else delete this.attrs.hidden; }
  get tabIndex() { return "tabindex" in this.attrs ? Number(this.attrs.tabindex) : -1; }
  set tabIndex(v) { this.attrs.tabindex = String(v); }
  get id() { return this.attrs.id || ""; }
  set id(v) { this.attrs.id = String(v); }
  get textContent() { return this._text + this.children.map(k => k.textContent).join(""); }
  set textContent(v) { this.children.forEach(k => { k.parentNode = null; }); this.children = []; this._text = String(v); }
  get firstChild() { return this.children[0] || null; }
  get lastChild() { return this.children[this.children.length - 1] || null; }
  get childNodes() { return this.children; }
  get firstElementChild() { return this.children[0] || null; }
  get nextSibling() { if (!this.parentNode) return null; const s = this.parentNode.children; return s[s.indexOf(this) + 1] || null; }
  get previousSibling() { if (!this.parentNode) return null; const s = this.parentNode.children; return s[s.indexOf(this) - 1] || null; }
  get nextElementSibling() { return this.nextSibling; }
  get previousElementSibling() { return this.previousSibling; }
  get ownerDocument() { return DOC; }
  get parentElement() { return this.parentNode && this.parentNode.attrs ? this.parentNode : null; }
  get offsetWidth() { return 220; } get offsetHeight() { return 60; } get clientWidth() { return 600; } get clientHeight() { return 300; }
  get offsetLeft() { return 0; } get offsetTop() { return 0; } get scrollWidth() { return 600; } get scrollHeight() { return 300; }
  setAttribute(a, b) { this.attrs[a] = String(b); }
  setAttributeNS(ns, a, b) { this.attrs[a] = String(b); }
  getAttribute(a) { return a in this.attrs ? this.attrs[a] : null; }
  hasAttribute(a) { return a in this.attrs; }
  removeAttribute(a) { delete this.attrs[a]; }
  appendChild(k) { if (k.parentNode) k.parentNode.removeChild(k); this.children.push(k); k.parentNode = this; return k; }
  insertBefore(k, ref) {
    if (k.parentNode) k.parentNode.removeChild(k);
    const i = ref ? this.children.indexOf(ref) : -1;
    if (i < 0) this.children.push(k); else this.children.splice(i, 0, k);
    k.parentNode = this; return k;
  }
  removeChild(k) { const i = this.children.indexOf(k); if (i >= 0) this.children.splice(i, 1); k.parentNode = null; return k; }
  remove() { if (this.parentNode) this.parentNode.removeChild(this); }
  append(...ns) { ns.forEach(n => this.appendChild(typeof n === "string" ? tnode(n) : n)); }
  prepend(...ns) { ns.slice().reverse().forEach(n => this.insertBefore(typeof n === "string" ? tnode(n) : n, this.children[0] || null)); }
  before(n) { this.parentNode.insertBefore(n, this); }
  after(n) { this.parentNode.insertBefore(n, this.nextSibling); }
  replaceChildren(...ns) { this.textContent = ""; this.append(...ns); }
  insertAdjacentElement(pos, e) {
    if (pos === "beforebegin") this.before(e); else if (pos === "afterend") this.after(e);
    else if (pos === "afterbegin") this.insertBefore(e, this.children[0] || null); else this.appendChild(e);
    return e;
  }
  contains(k) { for (let n = k; n; n = n.parentNode) if (n === this) return true; return false; }
  matches(sel) { return String(sel).split(",").some(p => matchChain(this, p.trim())); }
  closest(sel) { for (let n = this; n && n.attrs; n = n.parentNode) if (n.matches(sel)) return n; return null; }
  querySelectorAll(sel) { const o = []; walk(this, n => { if (n !== this && n.matches(sel)) o.push(n); }); return o; }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  addEventListener(t, f) { (this._l[t] = this._l[t] || []).push(f); }
  removeEventListener(t, f) { this._l[t] = (this._l[t] || []).filter(x => x !== f); }
  dispatchEvent(ev) {
    ev.target = this; ev.preventDefault = ev.preventDefault || function () {}; ev.stopPropagation = function () { ev._stop = true; };
    const path = [];
    if (ev.bubbles) { for (let n = this; n; n = n.parentNode) path.push(n); } else path.push(this);
    for (const n of path) {
      ev.currentTarget = n;
      (n._l[ev.type] || []).slice().forEach(f => { try { f.call(n, ev); } catch (e) { ERRS.push(ev.type + ": " + e); } });
      if (ev._stop) break;
    }
    flush();
    return true;
  }
  focus() { this.dispatchEvent({type: "focus", bubbles: false}); }
  blur() { this.dispatchEvent({type: "blur", bubbles: false}); }
  getBBox() { return {x: 0, y: 0, width: 100, height: 20}; }
  getBoundingClientRect() {
    const vb = String(this.attrs.viewBox || "").split(/\s+/).map(Number);
    const h = vb.length === 4 && vb[2] ? 600 * vb[3] / vb[2] : 300;
    return {left: 0, top: 0, x: 0, y: 0, width: 600, height: h, right: 600, bottom: h};
  }
}
function tnode(s) { const t = new El("#text"); t.tagName = "#text"; t.nodeType = 3; t._text = String(s); return t; }
const DOC = {
  _l: {}, parentNode: null, children: [], attrs: null,
  addEventListener(t, f) { (this._l[t] = this._l[t] || []).push(f); },
  removeEventListener() {},
  createElement: t => new El(t, false), createElementNS: (ns, t) => new El(t, true), createTextNode: tnode,
  querySelector() { return null; }, querySelectorAll() { return []; },
};
DOC.body = new El("body"); DOC.body.parentNode = DOC; DOC.documentElement = DOC.body;
const WIN = {addEventListener() {}, removeEventListener() {}, innerWidth: 1200, innerHeight: 800, matchMedia() { return {matches: false}; }};
const OBJS = {};
const ctx = {
  document: DOC, window: WIN, console: {log() {}, warn() {}, error() {}},
  setTimeout(f) { timers.push(f); return timers.length; }, clearTimeout() {}, requestAnimationFrame(f) { timers.push(f); return 1; },
  getComputedStyle() { return {}; },
  fetch(u) { const f = decodeURIComponent(String(u).split("/").pop()); return Promise.resolve({ok: true, status: 200, json() { return Promise.resolve(OBJS[f]); }}); },
};
let loaded = null;
try { vm.runInNewContext(src, ctx); } catch (e) { loaded = String(e); }
const r = WIN.rfChart || {};
const TO = "2026-09-29";
const FROM = {R30: "2026-08-30", R90: "2026-07-01", R365: "2025-09-29"};
const iso = n => new Date(n * 864e5).toISOString().slice(0, 10);
const PTS = [];
for (let n = Date.parse("2025-09-29T00:00:00Z") / 864e5, i = 0; n <= Date.parse(TO + "T00:00:00Z") / 864e5; n++, i++) {
  PTS.push([iso(n), Math.round((100 + 0.011 * i + 4 * Math.sin(i / 13)) * 100) / 100, "m"]);
}
const MARKERS = [
  {side: "buy", start: "2026-09-10", end: "2026-09-10", span: false, usd: 1234567, bps: 12.3, r: 7, n_trades: 1},
  {side: "sell", start: "2026-09-02", end: "2026-09-12", span: true, usd: 250000, bps: null, r: 5, n_trades: 3},
];
const SEC = {name: "n", currency: "USD", source_words: "x", points: PTS, gaps: [], markers: MARKERS};
OBJS.F = {fund: "F", asof: TO, generated_at: "g", ranges: FROM, securities: {K: SEC}};
const safe = f => { try { const x = f(); return x === undefined ? "<undefined>" : x; } catch (e) { return "<error " + e + ">"; } };
const tag = n => String(n.tagName || "").toLowerCase();
const hasCls = (n, c) => tokens(n.className).includes(c);
const all = (root, pred) => { const o = []; walk(root, n => { if (pred(n)) o.push(n); }); return o; };
function mount() {
  const dialog = new El("div"); dialog.setAttribute("data-sec-dialog", "K");
  const f = new El("div"); f.className = "rf-chart"; f.setAttribute("data-chart-fund", "F"); f.setAttribute("data-chart-key", "K");
  const st = new El("p"); st.setAttribute("data-chart-status", "");
  const tr = new El("ul"); tr.setAttribute("data-chart-trades", "");
  f.appendChild(st); f.appendChild(tr);
  ["R30", "R90", "R365"].forEach(rg => { const b = new El("button"); b.setAttribute("data-chart-range", rg); b.textContent = rg; f.appendChild(b); });
  dialog.appendChild(f); DOC.body.appendChild(dialog);
  return {dialog, f, st};
}
const settle = async () => { for (let i = 0; i < 30; i++) await new Promise(res => setImmediate(res)); flush(); };
async function openDialog(m) {
  (DOC._l.toggle || []).forEach(fn => { try { fn({type: "toggle", target: m.dialog, newState: "open"}); } catch (e) { ERRS.push("toggle: " + e); } });
  await settle();
}
async function clickRange(m, rg) {
  const b = all(m.f, n => n.attrs["data-chart-range"] === rg)[0];
  b.dispatchEvent({type: "click", bubbles: true});
  await settle();
}
const firstSvg = m => all(m.f, n => tag(n) === "svg")[0] || null;
const nearestFrame = (m, n) => { for (let x = n && n.parentNode; x && x !== m.f; x = x.parentNode) if (hasCls(x, "rf-ch-frame")) return x; return null; };
const lstn = (n, t) => { let c = 0; for (let x = n; x; x = x.parentNode) c += (x._l[t] || []).length; return c; };
(async () => {
  const out = {loaded: loaded, errs: ERRS, has: {plan: typeof r.plan === "function", words: typeof r.words === "function",
                                                 curve: typeof r.curve === "function", ticks: typeof r.ticks === "function"}};
  out.ticks = {}; out.npts = {};
  for (const rg of ["R30", "R90", "R365"]) {
    const pl = safe(() => r.plan(SEC, FROM[rg], TO));
    out.npts[rg] = pl && pl.pts ? pl.pts.length : null;
    out.ticks[rg] = pl && pl.pts ? {a: pl.a, b: pl.b, ticks: safe(() => r.ticks(pl))} : null;
  }
  out.draw = {};
  const m = mount();
  await openDialog(m);
  for (const rg of ["R30", "R90", "R365"]) {
    if (rg !== "R30") await clickRange(m, rg);
    const svgs = all(m.f, n => tag(n) === "svg"), svg = svgs[0] || null;
    const tk = svg ? all(svg, n => tag(n) === "text" && "data-tick" in n.attrs) : [];
    let maxY = null;
    if (svg) {
      all(svg, n => tag(n) === "polyline").forEach(p => String(p.attrs.points || "").split(/\s+/).forEach(pt => {
        const y = Number(pt.split(",")[1]); if (isFinite(y) && (maxY === null || y > maxY)) maxY = y;
      }));
    }
    out.draw[rg] = {svgs: svgs.length, maxY: maxY, status: m.st.textContent,
                    ticks: tk.map(e => ({text: e.textContent, x: Number(e.attrs.x), y: Number(e.attrs.y)}))};
  }
  console.log(JSON.stringify(out));
})();
"""


def node_run(script_text: str):
    node = shutil.which("node")
    if node is None:
        return None, "node is not on the PATH"
    with tempfile.TemporaryDirectory(prefix="rv_cu1_") as d:
        f, j = pathlib.Path(d) / "chart.js", pathlib.Path(d) / "run.js"
        f.write_text(script_text, encoding="utf-8")
        j.write_text(JS, encoding="utf-8")
        p = subprocess.run([node, str(j), str(f)], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
        if p.returncode != 0:
            return None, f"node rc {p.returncode}: {(p.stderr or '').strip()[:300]}"
        try:
            return json.loads(p.stdout), None
        except Exception as e:  # noqa: BLE001 -- an unparseable run is a failed arm, not a crash
            return None, f"{type(e).__name__}: {e}"


def day_of(x: float):
    return date(1970, 1, 1) + timedelta(days=int(x))


def good_ticks(t):
    return (isinstance(t, list) and 4 <= len(t) <= 7
            and all(isinstance(k, dict) and isinstance(k.get("x"), (int, float)) and not isinstance(k.get("x"), bool)
                    and isinstance(k.get("label"), str) and k["label"].strip() for k in t))


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    script = (getattr(render, "CHART_SCRIPT", "") or "").replace("@DAY@", "2026-09-30").replace("@FAIL@", getattr(render, "CHART_FAIL", "x"))
    out, err = node_run(script)
    out = out or {}
    has, tk, npts, draw = out.get("has") or {}, out.get("ticks") or {}, out.get("npts") or {}, out.get("draw") or {}
    print("node:", err or "ran", "| script load error:", out.get("loaded"), "| exposes:", has, "| stub errors:", (out.get("errs") or [])[:3])
    for rg in RANGES:
        t = (tk.get(rg) or {}).get("ticks")
        print(f"  ticks {rg}:", json.dumps(t)[:260] if t is not None else None)
        d = draw.get(rg) or {}
        print(f"  draw {rg}: svgs {d.get('svgs')} | data-tick texts {[x.get('text') for x in d.get('ticks') or []]}")

    arrays = {rg: (tk.get(rg) or {}).get("ticks") for rg in RANGES}
    v.check(has.get("ticks") is True and all(good_ticks(arrays[rg]) for rg in RANGES),
            "(a) rfChart.ticks returns, for the 30-, 90- and 365-day plans, an array of 4 to 7 {x, label} objects")

    inside = True
    for rg in RANGES:
        t, a, b = arrays[rg], (tk.get(rg) or {}).get("a"), (tk.get(rg) or {}).get("b")
        if not good_ticks(t) or a is None:
            inside = False
            continue
        xs = [k["x"] for k in t]
        if not (all(a <= x <= b for x in xs) and all(p < q for p, q in zip(xs, xs[1:]))):
            inside = False
    v.check(inside, "(b) each plan's tick x values lie in [pl.a, pl.b] and are strictly increasing")

    day_form, year_form = re.compile(r"^\d{1,2} (" + "|".join(MON) + r")$"), re.compile(r"^(" + "|".join(MON) + r") \d{2}$")
    form_ok = True
    for rg in RANGES:
        t = arrays[rg]
        if not good_ticks(t):
            form_ok = False
            continue
        want = year_form if rg == "R365" else day_form
        form_ok = form_ok and all(want.match(k["label"].strip()) for k in t)
    v.check(form_ok, "(c) labels are day and month ('8 Sep') for the 30- and 90-day ranges, month and two-digit year ('Oct 25') for 365 days")

    v.check(all(good_ticks(arrays[rg]) and len({k["label"] for k in arrays[rg]}) == len(arrays[rg]) for rg in RANGES),
            "(d) no two labels in one plan are equal")

    names = True
    for rg in RANGES:
        t = arrays[rg]
        if not good_ticks(t):
            names = False
            continue
        for k in t:
            ok = False
            for x in {int(k["x"] // 1), int(round(k["x"])), -int(-k["x"] // 1)}:
                dt = day_of(x)
                short = f"{dt.day} {MON[dt.month - 1]}" if rg != "R365" else f"{MON[dt.month - 1]} {dt.year % 100:02d}"
                ok = ok or k["label"].strip() == short
            names = names and ok
    v.check(names, "(e) each label names the date (or month and year) its own x falls on")

    drawn = True
    for rg in RANGES:
        d, t = draw.get(rg) or {}, arrays[rg]
        got = d.get("ticks") or []
        if not (good_ticks(t) and d.get("svgs") == 1 and sorted(x.get("text") for x in got) == sorted(k["label"] for k in t)):
            drawn = False
            continue
        my = d.get("maxY")
        for x in got:
            xv, yv = x.get("x"), x.get("y")
            if not (isinstance(xv, (int, float)) and isinstance(yv, (int, float)) and xv == xv and yv == yv and 0 <= xv <= 600
                    and my is not None and yv > my):
                drawn = False
    v.check(drawn, "(f) the script's own draw writes one svg text[data-tick] per tick, with the tick's label, inside the viewBox and under the curve")

    print("control: node", shutil.which("node") is not None, "| priced points per range:", npts, "| svgs drawn:",
          {rg: (draw.get(rg) or {}).get("svgs") for rg in RANGES})
    v.check(shutil.which("node") is not None and out.get("loaded") is None and has.get("plan") is True and has.get("words") is True
            and has.get("curve") is True and all((npts.get(rg) or 0) >= 2 for rg in RANGES)
            and all((draw.get(rg) or {}).get("svgs") == 1 for rg in RANGES),
            "(g) control: node runs the script, it exposes plan, words and curve, each range holds priced points, and the script's own draw creates one svg per range")


v = c.Verdict("AC1")
try:
    run(v)
except SystemExit:
    raise
except Exception as e:  # noqa: BLE001 -- an import error at the base is the expected FAIL of a build check
    v.check(False, f"(x) exception: {type(e).__name__}: {e}")
labels = ", ".join(m.split(")")[0] + ")" for m in v.fails)
print("AC1 RESULT: PASS 0 failures" if not v.fails else f"AC1 RESULT: FAIL {len(v.fails)}: {labels}")
sys.exit(0 if not v.fails else 1)
