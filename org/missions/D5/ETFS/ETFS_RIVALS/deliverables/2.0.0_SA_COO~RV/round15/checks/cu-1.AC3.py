"""RIV-cu-1 AC3 (PRD v0.18 FWD-22; analysis round 22 ADDENDUM 1 and 2, Andrew-direct 2026-10-07): a buy or sell marker has a
dramatic, focusable tooltip, and the page's one script stays one small script.

Interface (prescribed, interface item 4 and the cell's rulings), in `render.CHART_SCRIPT` and `render.CHART_CSS`:
  - the script creates ONE element of class `rf-ch-tip` per chart, inside the frame (`rf-ch-frame`), with the attribute `hidden` by
    default; on `mouseover` (and `focus`) of a marker it is shown (no `hidden`), carries `data-side="buy"` or `"sell"`, and its text
    states the side in a word ("Bought" / "Sold"), the dollars and the date or dates (the content of `rfChart.words(m)` at least);
    on `mouseout` (and `blur`) it is hidden again; each marker is focusable (`tabindex="0"`); the marker's svg `<title>` stays;
  - `CHART_CSS` gives `.rf-ch-tip` a font-size of at least 16px, a font-weight of at least 600, `position:absolute`, a padding and a
    coloured background or border that differs by `data-side`;
  - the cell's rulings: the script grows by at most 3,000 bytes (7,369 at the base), stays ONE script with no `innerHTML`, the page
    stays valid under `render.validate`, and the frame and the tip add no per-dialog markup to the static page.
Runs the script under node in a vm context with a stub document and window, as pm-1.AC2 does; the stub keeps parent/children order,
attributes, classes, text and event listeners (a dispatched event bubbles unless it is `focus` / `blur`; `focusin` / `focusout`
follow them, as in a browser); the toggle listener is fired as a browser would, and a stub fetch hands the script a chart object.

Fixture: one USD security K, a priced point every day from 2025-09-29 to 2026-09-29, chart object asof 2026-09-29 with R30 from
2026-08-30; two markers -- a single-day buy ($1,234,567, 2026-09-10) and a span sell ($250,000, 2026-09-02 to 2026-09-12). The
dialog is opened (30 days); events are fired at each marker circle the draw made (a circle with a `title` child or `data-m`).
  - (a) the chart holds exactly one `rf-ch-tip`, inside a `rf-ch-frame`, carrying the attribute `hidden` before any event, also after
    the 90- and 365-day buttons are clicked (one per chart, not one per draw);
  - (b) `mouseover` on each marker shows the tip (no `hidden`) with `data-side` equal to the marker's side, text holding "Bought" (buy)
    or "Sold" (sell) and not the other word, the dollars ("1,234,567" / "250,000") and the date or dates (ISO, or day and month);
    both markers are matched, one each;
  - (c) `mouseout` on each marker hides the tip again;
  - (d) `focus` on each marker shows the tip with the same side, and `blur` hides it;
  - (e) each marker has `tabindex="0"` and still holds its `<title>` child, whose text is `rfChart.words(m)` of its marker;
  - (f) `CHART_CSS` `.rf-ch-tip`: font-size >= 16px, font-weight >= 600, `position:absolute`, a padding above 0, and the background or
    border declarations differ between `[data-side=buy]` and `[data-side=sell]` (each side carries a colour);
  - (g) regression: the script is at most 7,369 + 3,000 bytes, `render.script_count` of the rendered fc-1 page is 1, `render.validate`
    accepts the page, the script has no `innerHTML`, and the page source holds no `class="rf-ch-frame"` or `class="rf-ch-tip"`
    markup (the CSS rule text is not markup);
  - (h) control: node runs the script, the draw creates one svg with two marker circles each holding a `<title>`, and a `mouseover`
    dispatched at a marker reaches a listener on it or on one of its ancestors.
FAIL at base bcf0b16c75: (a), (b), (c), (d), (e), (f) FAIL (no rf-ch-tip element, so no tip to show or hide; markers carry no tabindex;
no .rf-ch-tip rule in CHART_CSS); (g) PASSES (script 7,369 bytes, one script, validate accepts the page, no innerHTML) and (h) PASSES
(two titled marker circles, the mouseover reaches the script's own listener). The simulated conforming build passes (a) to (h)."""
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
BASE_BYTES, GROW = 7369, 3000
# the two fixture markers: (side, the dollars as the script words them, the dates the tip must name, the word it must hold, the other word)
EXPECT = (("buy", "1,234,567", ("2026-09-10",), "Bought", "Sold"), ("sell", "250,000", ("2026-09-02", "2026-09-12"), "Sold", "Bought"))
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
  const out = {loaded: loaded, errs: ERRS, has: {plan: typeof r.plan === "function", words: typeof r.words === "function"}};
  out.words = MARKERS.map(mm => safe(() => r.words(mm)));
  const m = mount();
  await openDialog(m);
  const tips = () => all(m.f, n => hasCls(n, "rf-ch-tip"));
  const state = () => { const t = tips()[0]; return t ? {hidden: t.hidden, side: "data-side" in t.attrs ? t.attrs["data-side"] : null, text: t.textContent} : null; };
  const tipFacts = () => { const t = tips()[0] || null; return {n: tips().length, inFrame: !!t && !!nearestFrame(m, t), hidden: !!t && t.hidden}; };
  out.tip0 = tipFacts();
  out.svgs = all(m.f, n => tag(n) === "svg").length;
  const svg = firstSvg(m);
  const mks = svg ? all(svg, n => tag(n) === "circle" && (n.children.some(k => tag(k) === "title") || "data-m" in n.attrs)) : [];
  out.markers = mks.map(mk => {
    const title = mk.children.filter(k => tag(k) === "title")[0];
    const rec = {tabindex: "tabindex" in mk.attrs ? mk.attrs.tabindex : null, title: title ? title.textContent : null, over_listeners: lstn(mk, "mouseover")};
    mk.dispatchEvent({type: "mouseover", bubbles: true});
    rec.over = state();
    mk.dispatchEvent({type: "mouseout", bubbles: true});
    rec.out = state();
    mk.dispatchEvent({type: "focus", bubbles: false}); mk.dispatchEvent({type: "focusin", bubbles: true});
    rec.focus = state();
    mk.dispatchEvent({type: "blur", bubbles: false}); mk.dispatchEvent({type: "focusout", bubbles: true});
    rec.blur = state();
    return rec;
  });
  out.tipAfter = {};
  for (const rg of ["R90", "R365"]) { await clickRange(m, rg); out.tipAfter[rg] = tipFacts(); }
  console.log(JSON.stringify(out));
})();
"""

def css_rules(css: str):
    """(selector list, {property: value}) for each top-level rule of a stylesheet, in order; at-rule blocks are skipped."""
    css = re.sub(r"/\*.*?\*/", "", css or "", flags=re.S)
    rules, i = [], 0
    while True:
        j = css.find("{", i)
        if j < 0:
            return rules
        depth, k = 1, j + 1
        while k < len(css) and depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0)
            k += 1
        sel, body = css[i:j].strip(), css[j + 1:k - 1]
        i = k
        if sel.startswith("@"):
            continue
        decls = {}
        for part in body.split(";"):
            if ":" in part:
                key, val = part.split(":", 1)
                decls[key.strip().lower()] = re.sub(r"\s*!important\s*$", "", val.strip(), flags=re.I)
        rules.append(([s.strip() for s in sel.split(",") if s.strip()], decls))


def merged(rules, pred):
    """The declarations of every rule with a selector entry accepted by `pred`, later rules winning."""
    out = {}
    for sels, decls in rules:
        if any(pred(s) for s in sels):
            out.update(decls)
    return out


def ends_with_class(cls: str):
    """A selector entry that ends in exactly `.cls` (no attribute or pseudo suffix), alone or after an ancestor."""
    rx = re.compile(r"(^|[\s>+~])\." + re.escape(cls) + r"$")
    return lambda s: bool(rx.search(s))


def px(val):
    m = re.fullmatch(r"\s*(-?\d*\.?\d+)px\s*", val or "")
    return float(m.group(1)) if m else None


def font_size(p):
    if "font-size" in p:
        return px(p["font-size"])
    m = re.search(r"(\d*\.?\d+)px", p.get("font", ""))
    return float(m.group(1)) if m else None


def font_weight(p):
    raw = p.get("font-weight")
    if raw is None:
        m = re.match(r"\s*(?:italic\s+|oblique\s+)?(bold|bolder|normal|[1-9]00)\b", p.get("font", ""), re.I)
        raw = m.group(1) if m else None
    if raw is None:
        return None
    raw = raw.strip().lower()
    return {"bold": 700, "bolder": 700, "normal": 400}.get(raw, int(raw) if raw.isdigit() else None)


def border_of(p):
    """(width in px, style) from the `border` shorthand and/or `border-width` / `border-style`."""
    width = style = None
    sh = p.get("border", "")
    if sh:
        m = re.search(r"(\d*\.?\d+)px", sh)
        width = float(m.group(1)) if m else ({"thin": 1.0, "medium": 3.0, "thick": 5.0}.get(next((w for w in ("thin", "medium", "thick") if w in sh), ""), 3.0))
        m = re.search(r"\b(solid|dashed|dotted|double|groove|ridge|inset|outset|none|hidden)\b", sh)
        style = m.group(1) if m else None
    if "border-width" in p:
        width = px(p["border-width"].split()[0])
    if "border-style" in p:
        style = p["border-style"].split()[0]
    return width, style


def radius_of(p):
    nums = [float(x) for x in re.findall(r"\d*\.?\d+", p.get("border-radius", ""))]
    return max(nums) if nums else 0.0


def padding_min(p):
    """The smallest of the four padding sides in px, or None when a side is missing or not in px."""
    sides = {}
    if "padding" in p:
        vals = [px(x) for x in p["padding"].split()]
        if vals and None not in vals and len(vals) <= 4:
            n = len(vals)
            top = vals[0]
            right = vals[1] if n > 1 else top
            bottom = vals[2] if n > 2 else top
            left = vals[3] if n > 3 else right
            sides = {"top": top, "right": right, "bottom": bottom, "left": left}
    for side in ("top", "right", "bottom", "left"):
        if "padding-" + side in p:
            sides[side] = px(p["padding-" + side])
    return min(sides.values()) if len(sides) == 4 and None not in sides.values() else None


def has_background(p):
    val = (p.get("background") or p.get("background-color") or "").strip().lower()
    return bool(val) and val not in ("none", "transparent", "initial", "inherit", "unset")


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


def names_date(text: str, iso: str) -> bool:
    """The text names the date: the ISO form, or its day number beside its month name."""
    _, mo, d = (int(x) for x in iso.split("-"))
    return iso in text or (re.search(r"(?<!\d)0?%d(?!\d)" % d, text) is not None and re.search(MON[mo - 1], text, re.I) is not None)


def match_markers(recs, key):
    """Pair each fixture marker with the one marker whose `key` state text holds its dollars; None when the pairing is not 1:1."""
    paired = []
    for side, usd, dates, word, other in EXPECT:
        hit = [r for r in recs if r.get(key) and usd in (r[key].get("text") or "").replace("$", "")]
        if len(hit) != 1:
            return None
        paired.append((hit[0], side, usd, dates, word, other))
    return paired if len({id(p[0]) for p in paired}) == len(paired) else None


def shown_right(state, side, dates, word, other):
    text = (state or {}).get("text") or ""
    return (bool(state) and state.get("hidden") is False and state.get("side") == side and word in text and other not in text
            and all(names_date(text, d) for d in dates))


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    script = (getattr(render, "CHART_SCRIPT", "") or "").replace("@DAY@", "2026-09-30").replace("@FAIL@", getattr(render, "CHART_FAIL", "x"))
    out, err = node_run(script)
    out = out or {}
    recs, words, tip0 = out.get("markers") or [], out.get("words") or [], out.get("tip0") or {}
    print("node:", err or "ran", "| script load error:", out.get("loaded"), "| exposes:", out.get("has"), "| stub errors:", (out.get("errs") or [])[:3])
    print("tip before any event:", tip0, "| after 90 / 365 days:", out.get("tipAfter"), "| marker circles found:", len(recs))
    for i, r in enumerate(recs):
        print(f"  marker {i}: tabindex {r.get('tabindex')!r} | title {str(r.get('title'))[:60]!r} | over {r.get('over')} | out {r.get('out')} "
              f"| focus {r.get('focus')} | blur {r.get('blur')}")

    after = out.get("tipAfter") or {}
    v.check(tip0.get("n") == 1 and tip0.get("inFrame") is True and tip0.get("hidden") is True
            and all((after.get(rg) or {}).get("n") == 1 and (after.get(rg) or {}).get("inFrame") is True
                    and (after.get(rg) or {}).get("hidden") is True for rg in ("R90", "R365")),
            "(a) exactly one rf-ch-tip per chart, inside a rf-ch-frame, hidden by default (also after a range switch)")

    over = match_markers(recs, "over")
    v.check(over is not None and all(shown_right(r["over"], side, dates, word, other) for r, side, _, dates, word, other in over),
            "(b) mouseover on a marker shows the tip with its data-side, the Bought / Sold word, the dollars and the date(s)")

    v.check(over is not None and all((r.get("out") or {}).get("hidden") is True for r, *_ in over),
            "(c) mouseout hides the tip again (after it was shown)")

    foc = match_markers(recs, "focus")
    v.check(foc is not None and all(shown_right(r["focus"], side, dates, word, other) and (r.get("blur") or {}).get("hidden") is True
                                    for r, side, _, dates, word, other in foc),
            "(d) focus shows the tip with the same side and content, and blur hides it")

    v.check(len(recs) == len(EXPECT) and all(r.get("tabindex") == "0" for r in recs)
            and sorted(r.get("title") or "" for r in recs) == sorted(w for w in words if isinstance(w, str)) and len(words) == len(EXPECT),
            "(e) each marker has tabindex 0 and keeps its svg title, which is rfChart.words(m)")

    rules = css_rules(getattr(render, "CHART_CSS", ""))
    base = merged(rules, ends_with_class("rf-ch-tip"))
    sides = {}
    for s in ("buy", "sell"):
        rx = re.compile(r"(\.rf-ch-tip|(^|[\s>+~]))\[data-side\s*=\s*[\"']?" + s + r"[\"']?\]$")
        sides[s] = dict(base, **merged(rules, lambda sel, rx=rx: bool(rx.search(sel))))
    fs, fw, pad = font_size(base), font_weight(base), padding_min(base)
    colour = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|\b(?:green|red|crimson|firebrick|maroon|darkgreen|darkred|seagreen|forestgreen|lime|tomato)\b", re.I)

    def tint(p):
        return {k: val for k, val in p.items() if (k.startswith("background") or k.startswith("border")) and not re.search(r"radius|width|style", k)
                and colour.search(val)}

    tb, ts = tint(sides["buy"]), tint(sides["sell"])
    print("CSS .rf-ch-tip:", base, "| buy tint:", tb, "| sell tint:", ts)
    v.check(fs is not None and fs >= 16 and fw is not None and fw >= 600 and (base.get("position") or "").strip().lower() == "absolute"
            and pad is not None and pad > 0 and bool(tb) and bool(ts) and tb != ts,
            f"(f) CHART_CSS .rf-ch-tip: font-size >= 16px, weight >= 600, position:absolute, padding, a colour that differs by data-side (read: {fs}, {fw}, {base.get('position')}, {pad})")

    nbytes = len(getattr(render, "CHART_SCRIPT", "").encode("utf-8"))
    html = render.render_page(c.load_fc1().fixture())
    ok, why = render.validate(html)
    print("script bytes:", nbytes, "| script_count:", render.script_count(html), "| validate:", ok, "|", why[:90])
    v.check(nbytes <= BASE_BYTES + GROW and render.script_count(html) == 1 and ok is True and "innerHTML" not in script
            and 'class="rf-ch-frame"' not in html and 'class="rf-ch-tip"' not in html and "class=rf-ch-frame" not in html and "class=rf-ch-tip" not in html,
            f"(g) regression: script {nbytes} <= {BASE_BYTES + GROW} bytes, one script, render.validate accepts the page, no innerHTML, no static frame or tip markup")

    print("control: node", shutil.which("node") is not None, "| svgs:", out.get("svgs"), "| markers with a title:", sum(1 for r in recs if r.get("title")),
          "| mouseover listeners on the chain:", [r.get("over_listeners") for r in recs])
    v.check(shutil.which("node") is not None and out.get("loaded") is None and out.get("svgs") == 1 and len(recs) == len(EXPECT)
            and all(r.get("title") and (r.get("over_listeners") or 0) >= 1 for r in recs),
            "(h) control: node runs the script, the draw creates one svg with two titled marker circles, and a mouseover reaches a listener")


v = c.Verdict("AC3")
try:
    run(v)
except SystemExit:
    raise
except Exception as e:  # noqa: BLE001 -- an import error at the base is the expected FAIL of a build check
    v.check(False, f"(x) exception: {type(e).__name__}: {e}")
labels = ", ".join(m.split(")")[0] + ")" for m in v.fails)
print("AC3 RESULT: PASS 0 failures" if not v.fails else f"AC3 RESULT: FAIL {len(v.fails)}: {labels}")
sys.exit(0 if not v.fails else 1)
