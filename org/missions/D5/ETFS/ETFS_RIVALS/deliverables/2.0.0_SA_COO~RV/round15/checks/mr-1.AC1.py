"""RIV-mr-1 AC1 (PRD v0.18 FWD-22; CVO ADJUDICATION_v28; CTO round-24 analysis msg 31413): while a marker is pointed at, the
read-out names THAT marker's day and price, and the tooltip never covers the read-out.

Interface (prescribed, interface items 1 and 2 of the cell), in `render.CHART_SCRIPT` / `render.CHART_CSS` only:
  - on `mouseover` or `focus` of a marker the read-out (`.rf-ch-read`) shows the marker's END date in its `data-read="date"` child and,
    in its `data-read="price"` child, the price of the priced point the marker is drawn on (the nearest priced point to the marker's
    end date) with the stored currency code; a marker with no priced point in the range shows the date and no price; on `mouseout`
    or `blur` the read-out returns to its idle prompt until the pointer next moves over the curve; a `mousemove` whose target is a
    marker does not overwrite it;
  - the tooltip (`.rf-ch-tip`) is placed only over the svg's own box: its top edge is never above the svg's top edge inside the
    frame (so it cannot overlap the read-out, which sits before the svg); it still flips below a marker when there is no room above
    and stays inside the frame horizontally; the script grows by at most 600 bytes (9,348 at the base).
Runs the script under node in a vm context with a stub document and window, as cu-1.AC3 does (same stub: parent/children order,
attributes, classes, text, event listeners, bubbling, a stub fetch). The stub is extended with a LAYOUT: the frame starts at
(0,0), the read-out box is 12 to 62 high, the svg box starts at 70 (600 wide, viewBox-high), and the tip's rect follows its own
`style.left` / `style.top` in px relative to the frame (220 x 60). ASSUMED: the script positions the tip only through
`tip.style.left` / `tip.style.top` in px relative to the frame, as the base does.

Fixture: security K (USD), a priced point every day from 2025-09-29 to 2026-09-29 with a sharp peak (the highest price of the
series) on 2026-09-15 and a sharp trough (the lowest) on 2026-09-05; chart object asof 2026-09-29, R30 from 2026-08-30; two markers
-- a single-day buy ($900,000, end 2026-09-15, at the top of the plot) and a span sell ($250,000, 2026-09-01 to 2026-09-05, at the
bottom). A second security K2 (own fund object) has priced points only to 2026-09-20 and one buy marker ending 2026-09-27, seven
days after its last priced point. Before every marker event the pointer first crosses the curve (pointermove then mousemove on the
svg at client x 100, an early-September day), so the read-out holds a curve day that is NOT the marker's end date.
  - (a) `mouseover` on each K marker: the date child names the marker's end date (ISO, or day and month) and the price child holds the
    stored price of the point on that end date with "USD" (and not the curve day's price);
  - (b) `focus` then `focusin` on each K marker: the same;
  - (c) `mouseout` (and `blur` then `focusout`) afterwards: the read-out no longer names the marker's end date or its price;
  - (d) a `mousemove` and a `pointermove` whose target is the marker leave the marker's read-out as it was;
  - (e) K2's marker (no priced point on its end date): the date child names the marker's end date 2026-09-27; the price child is
    either empty of digits OR holds the price of the nearest priced point (2026-09-20) with "USD" -- both are accepted, a curve-day
    price is not;
  - (f) tooltip geometry on `mouseover`: for the top marker (its point is the range's highest price) the tip is shown and its top
    edge (`style.top`) is not above the svg's top edge, so its box does not meet the read-out's box, and it is inside the frame
    horizontally; for the lower marker the tip is shown (not hidden), has a finite top, is not above the svg's top and is inside
    the frame horizontally;
  - (g) regression: cu-1.AC1.py, cu-1.AC2.py and cu-1.AC3.py each, run as their own process from the worktree root, end
    `PASS 0 failures`; the script is at most 9,348 + 600 = 9,948 bytes (inside cu-1.AC3's own 7,369 + 3,000 bound);
  - (h) control: node runs the script, the draw makes one svg with a read-out, a tip and at least two markers, the curve crossing
    sets a read-out day that differs from both markers' end dates, a `mouseover` on a marker shows the tip, and the tip gets a
    `style.top` (the script reads the stub's rects).
FAIL at base 4611085187: (a), (b), (e), (f) FAIL (a marker hover or focus leaves the read-out on the last curve day, 2026-09-01, 103.37
USD; the top marker's tip sits at top 16 px, above the svg's top edge of 70, over the read-out); (c) and (d) PASS vacuously (the
read-out never shows a marker at base, so there is nothing to keep or to clear); (g) PASSES (script 9,348 bytes; cu-1.AC1, AC2 and AC3
end PASS 0 failures) and (h) PASSES (one svg, a read-out, a tip, two markers; the tip gets a style.top). The simulated conforming
build (script +252 bytes) passes (a) to (h)."""
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _common as c  # noqa: E402

MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
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
    const mk = (l, t, w, h) => ({left: l, top: t, x: l, y: t, width: w, height: h, right: l + w, bottom: t + h});
    const cl = tokens(this.className);
    const svgH = n => { const s = n.children.filter(k => String(k.tagName).toLowerCase() === "svg")[0]; const vb = s ? String(s.attrs.viewBox || "").split(/\s+/).map(Number) : []; return vb.length === 4 && vb[2] ? 600 * vb[3] / vb[2] : 300; };
    if (String(this.tagName).toLowerCase() === "svg") { const vb = String(this.attrs.viewBox || "").split(/\s+/).map(Number); return mk(0, 70, 600, vb.length === 4 && vb[2] ? 600 * vb[3] / vb[2] : 300); }
    if (cl.includes("rf-ch-frame")) return mk(0, 0, 600, 70 + svgH(this) + 12);
    if (cl.includes("rf-ch-read")) return mk(0, 12, 600, 50);
    if (cl.includes("rf-ch-tip")) return mk(parseFloat(this.style.left) || 0, parseFloat(this.style.top) || 0, 220, 60);
    return mk(0, 0, 600, 300);
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
const dn = s => Date.parse(s + "T00:00:00Z") / 864e5;
function series(last) {
  const o = [], pk = dn("2026-09-15"), tr = dn("2026-09-05");
  for (let n = dn("2025-09-29"), i = 0; n <= dn(last); n++, i++) {
    const v = 100 + 0.01 * i + 30 * Math.max(0, 1 - Math.abs(n - pk) / 3) - 20 * Math.max(0, 1 - Math.abs(n - tr) / 3);
    o.push([iso(n), Math.round(v * 100) / 100, "m"]);
  }
  return o;
}
const PTS = series(TO), PTS2 = series("2026-09-20");
const price = (pts, d) => (pts.filter(p => p[0] === d)[0] || [])[1];
const MARKERS = [
  {side: "buy", start: "2026-09-15", end: "2026-09-15", span: false, usd: 900000, bps: 12.3, r: 7, n_trades: 1},
  {side: "sell", start: "2026-09-01", end: "2026-09-05", span: true, usd: 250000, bps: null, r: 5, n_trades: 3},
];
const MARKERS2 = [{side: "buy", start: "2026-09-27", end: "2026-09-27", span: false, usd: 777000, bps: 1.5, r: 6, n_trades: 1}];
OBJS.F = {fund: "F", asof: TO, generated_at: "g", ranges: FROM, securities: {K: {name: "n", currency: "USD", source_words: "x", points: PTS, gaps: [], markers: MARKERS}}};
OBJS.F2 = {fund: "F2", asof: TO, generated_at: "g", ranges: FROM, securities: {K2: {name: "n2", currency: "USD", source_words: "x", points: PTS2, gaps: [], markers: MARKERS2}}};
const tag = n => String(n.tagName || "").toLowerCase();
const hasCls = (n, c) => tokens(n.className).includes(c);
const all = (root, pred) => { const o = []; walk(root, n => { if (pred(n)) o.push(n); }); return o; };
function mount(fund, key) {
  const dialog = new El("div"); dialog.setAttribute("data-sec-dialog", key);
  const f = new El("div"); f.className = "rf-chart"; f.setAttribute("data-chart-fund", fund); f.setAttribute("data-chart-key", key);
  const st = new El("p"); st.setAttribute("data-chart-status", "");
  const tr = new El("ul"); tr.setAttribute("data-chart-trades", "");
  f.appendChild(st); f.appendChild(tr);
  ["R30", "R90", "R365"].forEach(rg => { const b = new El("button"); b.setAttribute("data-chart-range", rg); b.textContent = rg; f.appendChild(b); });
  dialog.appendChild(f); DOC.body.appendChild(dialog);
  return {dialog, f};
}
const settle = async () => { for (let i = 0; i < 30; i++) await new Promise(res => setImmediate(res)); flush(); };
async function openDialog(m) {
  (DOC._l.toggle || []).forEach(fn => { try { fn({type: "toggle", target: m.dialog, newState: "open"}); } catch (e) { ERRS.push("toggle: " + e); } });
  await settle();
}
const rect = n => { const b = n.getBoundingClientRect(); return {top: b.top, bottom: b.bottom, left: b.left, right: b.right, width: b.width, height: b.height}; };
function parts(m) {
  const svg = all(m.f, n => tag(n) === "svg")[0] || null;
  return {svg, rd: all(m.f, n => hasCls(n, "rf-ch-read"))[0] || null, tip: all(m.f, n => hasCls(n, "rf-ch-tip"))[0] || null, frame: all(m.f, n => hasCls(n, "rf-ch-frame"))[0] || null};
}
const snap = m => { const p = parts(m); return p.rd ? {kids: p.rd.children.map(k => ({k: k.attrs["data-read"] || null, text: k.textContent})), text: p.rd.textContent} : null; };
function tipState(m) {
  const p = parts(m), t = p.tip;
  if (!t || !p.svg || !p.rd || !p.frame) return null;
  const s = rect(p.svg), rd = rect(p.rd), fr = rect(p.frame);
  return {hidden: t.hidden, top: parseFloat(t.style.top), left: parseFloat(t.style.left), topRaw: t.style.top === undefined ? null : String(t.style.top),
    w: t.offsetWidth, h: t.offsetHeight, svgTop: s.top, readTop: rd.top, readBottom: rd.bottom, frameW: fr.width, text: t.textContent};
}
const cross = m => { const s = parts(m).svg; ["pointermove", "mousemove"].forEach(t => s.dispatchEvent({type: t, bubbles: true, clientX: 100, clientY: 150})); };
function probe(m, mk, mode) {
  cross(m);
  const rec = {before: snap(m)};
  if (mode === "mouse") mk.dispatchEvent({type: "mouseover", bubbles: true});
  else { mk.dispatchEvent({type: "focus", bubbles: false}); mk.dispatchEvent({type: "focusin", bubbles: true}); }
  rec.during = snap(m); rec.tip = tipState(m);
  if (mode === "mouse") {
    ["mousemove", "pointermove"].forEach(t => mk.dispatchEvent({type: t, bubbles: true, clientX: 300, clientY: 150}));
    rec.moved = snap(m);
    mk.dispatchEvent({type: "mouseout", bubbles: true});
  } else { mk.dispatchEvent({type: "blur", bubbles: false}); mk.dispatchEvent({type: "focusout", bubbles: true}); }
  rec.after = snap(m);
  return rec;
}
const circlesOf = (m, usd) => {
  const svg = parts(m).svg;
  if (!svg) return [];
  return all(svg, n => tag(n) === "circle" && "data-m" in n.attrs).filter(n => {
    const t = n.children.filter(k => tag(k) === "title")[0];
    return t && t.textContent.replace(/\$/g, "").includes(usd.toLocaleString("en-US"));
  });
};
(async () => {
  const out = {loaded: loaded, errs: ERRS, has: {plan: typeof r.plan === "function"}};
  const m = mount("F", "K");
  await openDialog(m);
  const p = parts(m);
  out.draw = {svgs: all(m.f, n => tag(n) === "svg").length, read: !!p.rd, tip: !!p.tip, markers: all(m.f, n => tag(n) === "circle" && "data-m" in n.attrs).length};
  out.idle = snap(m);
  cross(m);
  out.cross = snap(m);
  out.markers = [];
  for (const mm of MARKERS) {
    const cs = circlesOf(m, mm.usd), rec = {side: mm.side, found: cs.length, end: mm.end, price: price(PTS, mm.end)};
    if (cs.length === 1) { rec.mouse = probe(m, cs[0], "mouse"); rec.focus = probe(m, cs[0], "focus"); }
    out.markers.push(rec);
  }
  const m2 = mount("F2", "K2");
  await openDialog(m2);
  const c2 = circlesOf(m2, MARKERS2[0].usd), rec2 = {found: c2.length, end: MARKERS2[0].end, near: "2026-09-20", price: price(PTS2, "2026-09-20")};
  if (c2.length === 1) rec2.mouse = probe(m2, c2[0], "mouse");
  out.k2 = rec2;
  console.log(JSON.stringify(out));
})();
"""

def node_run(script_text: str):
    node = shutil.which("node")
    if node is None:
        return None, "node is not on the PATH"
    with tempfile.TemporaryDirectory(prefix="rv_mr1_") as d:
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


def names_date(text: str, iso: str) -> bool:
    """The text names the date: the ISO form, or its day number beside its month name."""
    _, mo, d = (int(x) for x in iso.split("-"))
    return iso in (text or "") or (re.search(r"(?<!\d)0?%d(?!\d)" % d, text or "") is not None and re.search(MON[mo - 1], text or "", re.I) is not None)


def child(snap, kind):
    return next((k["text"] for k in (snap or {}).get("kids", []) if k.get("k") == kind), None)


def numbers(text):
    return [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*\.\d+|\d+", text or "")]


def shows(snap, end, price):
    """The read-out names the end date in its date child and the stored price with USD in its price child."""
    pr, wh = child(snap, "price"), child(snap, "date")
    return (pr is not None and wh is not None and "USD" in pr and names_date(wh, end)
            and any(abs(n - price) < 0.005 for n in numbers(pr)))


def gone(snap, end, price):
    """The read-out no longer names the marker's end date or its price."""
    pr, wh = child(snap, "price"), child(snap, "date")
    return snap is not None and not names_date(wh, end) and not any(abs(n - price) < 0.005 for n in numbers(pr))


def sibling(name):
    p = subprocess.run([sys.executable, str(HERE / name)], capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(c.ROOT), timeout=600)
    lines = [ln for ln in (p.stdout or "").strip().splitlines() if ln.strip()]
    return (lines[-1] if lines else "<no output>"), p.returncode


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    script = (getattr(render, "CHART_SCRIPT", "") or "")
    out, err = node_run(script.replace("@DAY@", "2026-09-30").replace("@FAIL@", getattr(render, "CHART_FAIL", "x")))
    out = out or {}
    mks, k2, draw = out.get("markers") or [], out.get("k2") or {}, out.get("draw") or {}
    print("node:", err or "ran", "| script load error:", out.get("loaded"), "| exposes:", out.get("has"), "| stub errors:", (out.get("errs") or [])[:3])
    print("draw:", draw, "| idle read-out:", out.get("idle"), "| after a curve crossing:", out.get("cross"))
    for r in mks:
        for mode in ("mouse", "focus"):
            x = r.get(mode) or {}
            print(f"  K {r['side']} {mode}: end {r['end']} price {r['price']} | before {child(x.get('before'), 'date')} {child(x.get('before'), 'price')!r}"
                  f" | during {child(x.get('during'), 'date')} {child(x.get('during'), 'price')!r} | after {child(x.get('after'), 'date')}"
                  f" {child(x.get('after'), 'price')!r} | tip {x.get('tip')}")
    print("  K2 mouse:", {k: k2.get(k) for k in ("found", "end", "near", "price")}, "| during", (k2.get("mouse") or {}).get("during"), "| tip", (k2.get("mouse") or {}).get("tip"))

    ok_m = len(mks) == 2 and all(r.get("found") == 1 for r in mks)
    v.check(ok_m and all(shows((r.get("mouse") or {}).get("during"), r["end"], r["price"]) for r in mks),
            "(a) mouseover on a marker: the date child names the marker's end date and the price child holds its point's price with USD (a buy and a sell)")
    v.check(ok_m and all(shows((r.get("focus") or {}).get("during"), r["end"], r["price"]) for r in mks),
            "(b) focus on a marker: the same read-out")
    v.check(ok_m and all(gone((r.get(mode) or {}).get("after"), r["end"], r["price"]) for r in mks for mode in ("mouse", "focus")),
            "(c) mouseout / blur: the read-out no longer shows the marker's date and price")
    v.check(ok_m and all(((r.get("mouse") or {}).get("moved") or {}).get("kids") is not None
                         and ((r.get("mouse") or {}).get("moved") or {}).get("kids") == ((r.get("mouse") or {}).get("during") or {}).get("kids")
                         for r in mks),
            "(d) a mousemove / pointermove on the marker does not overwrite its read-out")

    km = k2.get("mouse") or {}
    kp, kw = child(km.get("during"), "price"), child(km.get("during"), "date")
    price_ok = kp is not None and (not re.search(r"\d", kp) or ("USD" in kp and any(abs(n - k2.get("price", -1)) < 0.005 for n in numbers(kp))))
    v.check(k2.get("found") == 1 and kw is not None and names_date(kw, k2.get("end", "")) and price_ok,
            "(e) a marker with no priced point on its end date: the date child names its end date; the price child is empty of digits or the nearest priced point's price")

    def geo_ok(t, top_marker):
        return (bool(t) and t.get("hidden") is False and isinstance(t.get("top"), (int, float)) and t["top"] == t["top"]
                and t["top"] >= t["svgTop"] - 0.5 and t["top"] >= t["readBottom"] - 0.5 and t.get("left", -1) >= -0.5
                and t["left"] + t["w"] <= t["frameW"] + 0.5)

    tt = [(r.get("mouse") or {}).get("tip") for r in mks]
    print("tip geometry (top marker, lower marker):", tt)
    v.check(ok_m and len(tt) == 2 and geo_ok(tt[0], True) and geo_ok(tt[1], False),
            "(f) tooltip geometry: shown, top edge not above the svg's top edge (clear of the read-out), inside the frame horizontally, for the top and the lower marker")

    nbytes = len(script.encode("utf-8"))
    subs = {n: sibling(n) for n in ("cu-1.AC1.py", "cu-1.AC2.py", "cu-1.AC3.py")}
    print("script bytes:", nbytes, "| siblings:", subs)
    v.check(nbytes <= 9348 + 600 and all(rc == 0 and ln.endswith("PASS 0 failures") for ln, rc in subs.values()),
            f"(g) regression: script {nbytes} <= {9348 + 600} bytes; cu-1.AC1, AC2 and AC3 each end PASS 0 failures")

    cr = out.get("cross") or {}
    cd = child(cr, "date")
    v.check(shutil.which("node") is not None and out.get("loaded") is None and draw.get("svgs") == 1 and draw.get("read") is True
            and draw.get("tip") is True and (draw.get("markers") or 0) >= 2 and ok_m and cd is not None
            and not any(names_date(cd, r["end"]) for r in mks)
            and all(((r.get("mouse") or {}).get("tip") or {}).get("hidden") is False for r in mks)
            and all(isinstance(((r.get("mouse") or {}).get("tip") or {}).get("top"), (int, float)) for r in mks),
            "(h) control: node runs the script; one svg, a read-out, a tip, >= 2 markers; the curve crossing sets a different day; mouseover shows the tip and gives it a style.top")


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
