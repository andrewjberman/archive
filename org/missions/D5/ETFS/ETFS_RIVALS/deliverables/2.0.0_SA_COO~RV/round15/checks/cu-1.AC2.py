"""RIV-cu-1 AC2 (PRD v0.18 FWD-22; analysis round 22 ADDENDUM 1 and 2, Andrew-direct 2026-10-07): the dialog chart is framed and
roomy, and its hover read-out is bold and focal.

Interface (prescribed, interface items 2 and 3 of the cell), in `render.CHART_SCRIPT` and `render.CHART_CSS`:
  - the chart's svg sits inside an element of class `rf-ch-frame`; `CHART_CSS` gives `.rf-ch-frame` a border of at least 1px
    solid, a border-radius, a padding of at least 10px and a background; the svg's viewBox is `0 0 600 H` with H at least 280;
  - the read-out (class `rf-ch-read`) is BEFORE the svg inside the frame; `CHART_CSS` gives `.rf-ch-read` a font-size of at least
    20px and a font-weight of at least 700, as plain numbers in px; on a pointer move over the curve it shows the price with its
    currency and the date, each in its own child element (`data-read="price"`, `data-read="date"`).
Runs the script under node in a vm context with a stub document and window, as pm-1.AC2 does; the stub keeps parent/children order,
attributes, classes, text and event listeners; the toggle and click listeners are fired as a browser would, a stub fetch hands the
script a chart object, and a `pointermove` then a `mousemove` is dispatched on the script's own svg at client x 300.
CSS is read from `render.CHART_CSS` by a small parser (shorthand or longhand; `bold` is 700; spaces optional; at-rule blocks skipped).

Fixture: one USD security K, a priced point every day from 2025-09-29 to 2026-09-29, two markers, chart object asof 2026-09-29
with R30 from 2026-08-30, R90 from 2026-07-01 and R365 from 2025-09-29; the dialog is opened (30 days) and the 90- and 365-day
buttons clicked, and arms (a) to (d) are read for all three ranges.
  - (a) the drawn svg has an ancestor of class `rf-ch-frame` inside the chart, and the chart holds exactly one such frame;
  - (b) exactly one `rf-ch-read` element is inside that frame and comes before the svg in document order;
  - (c) after the pointer move the read-out holds a child `data-read="price"` whose text has a number equal to the price of a
    stored point and the currency "USD", and a child `data-read="date"` that names that same point's date (ISO, or day and
    month);
  - (d) the svg's viewBox is `0 0 600 H` with H >= 280;
  - (e) `CHART_CSS` `.rf-ch-frame`: a border of at least 1px solid, a border-radius above 0, a padding of at least 10px on every
    side, a background;
  - (f) `CHART_CSS` `.rf-ch-read`: font-size >= 20px and font-weight >= 700 (or bold);
  - (g) control: node runs the script, it exposes plan, the script's own draw creates one svg and one `rf-ch-read` element for each
    range, the pointer move reaches the script's listener and leaves a non-empty read-out text, and the CSS parser reads a fixed
    sample stylesheet (border 1px solid, radius, padding 1px, a background, display:block, a `font` shorthand, an at-rule skipped).
FAIL at base bcf0b16c75: (a), (b), (c), (d), (e), (f) FAIL (no rf-ch-frame, the read-out sits after the svg in the out div and is one
flat <p> with no data-read children, viewBox 0 0 600 200, no .rf-ch-frame or .rf-ch-read rule in CHART_CSS); (g) PASSES (node runs the
script, one svg and one rf-ch-read per range, the move reaches the listener, the parser reads the sample stylesheet). The simulated
conforming build passes (a) to (g)."""
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
  const out = {loaded: loaded, errs: ERRS, has: {plan: typeof r.plan === "function"}, pts: PTS.map(p => [p[0], p[1]])};
  out.draw = {};
  const m = mount();
  await openDialog(m);
  for (const rg of ["R30", "R90", "R365"]) {
    if (rg !== "R30") await clickRange(m, rg);
    const svgs = all(m.f, n => tag(n) === "svg"), svg = svgs[0] || null;
    const frames = all(m.f, n => hasCls(n, "rf-ch-frame")), reads = all(m.f, n => hasCls(n, "rf-ch-read"));
    const frame = nearestFrame(m, svg);
    const d = {svgs: svgs.length, frames: frames.length, reads: reads.length, inFrame: !!frame, viewBox: svg ? svg.attrs.viewBox || null : null};
    if (frame) {
      const pre = []; walk(frame, n => pre.push(n));
      const rd = reads.filter(x => frame.contains(x))[0] || null;
      d.readsInFrame = reads.filter(x => frame.contains(x)).length;
      d.readBeforeSvg = !!rd && pre.indexOf(rd) >= 0 && pre.indexOf(rd) < pre.indexOf(svg);
    }
    if (svg) {
      d.moveListeners = lstn(svg, "mousemove") + lstn(svg, "pointermove");
      svg.dispatchEvent({type: "pointermove", bubbles: true, clientX: 300, clientY: 120});
      svg.dispatchEvent({type: "mousemove", bubbles: true, clientX: 300, clientY: 120});
      const rd = reads[0] || null;
      d.readText = rd ? rd.textContent : null;
      d.kids = rd ? all(rd, n => n !== rd && "data-read" in n.attrs).map(n => ({k: n.attrs["data-read"], text: n.textContent})) : [];
    }
    out.draw[rg] = d;
  }
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


def read_ok(kids, pts):
    """True when the price child's number is a stored point's price, carries USD, and the date child names that point's date."""
    price = next((k["text"] for k in kids if k.get("k") == "price"), None)
    when = next((k["text"] for k in kids if k.get("k") == "date"), None)
    if price is None or when is None or "USD" not in price:
        return False
    nums = [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*\.\d+|\d+", price)]
    return any(abs(p - n) < 0.005 and names_date(when, d) for d, p in pts for n in nums)


def run(v):
    c.setup_path()
    c.offline_guards()
    from rivalfunds import render

    script = (getattr(render, "CHART_SCRIPT", "") or "").replace("@DAY@", "2026-09-30").replace("@FAIL@", getattr(render, "CHART_FAIL", "x"))
    out, err = node_run(script)
    out = out or {}
    draw, pts = out.get("draw") or {}, out.get("pts") or []
    print("node:", err or "ran", "| script load error:", out.get("loaded"), "| exposes:", out.get("has"), "| stub errors:", (out.get("errs") or [])[:3])
    for rg in RANGES:
        d = draw.get(rg) or {}
        print(f"  draw {rg}: svgs {d.get('svgs')} | frames {d.get('frames')} | reads {d.get('reads')} | read in frame, before svg: "
              f"{d.get('readsInFrame')}, {d.get('readBeforeSvg')} | viewBox {d.get('viewBox')!r}")
        print(f"    read-out after the move: {str(d.get('readText'))[:90]!r} | data-read children {d.get('kids')}")

    v.check(all((draw.get(rg) or {}).get("svgs") == 1 and (draw.get(rg) or {}).get("inFrame") and (draw.get(rg) or {}).get("frames") == 1
                for rg in RANGES), "(a) the svg sits inside one rf-ch-frame in each range")
    v.check(all((draw.get(rg) or {}).get("readsInFrame") == 1 and (draw.get(rg) or {}).get("readBeforeSvg") is True for rg in RANGES),
            "(b) exactly one rf-ch-read is inside the frame and comes before the svg")
    v.check(all(read_ok((draw.get(rg) or {}).get("kids") or [], pts) for rg in RANGES),
            "(c) after the pointer move the read-out has a data-read price child (a stored price, USD) and a data-read date child (that point's date)")

    def height_ok(vb):
        m = re.fullmatch(r"\s*0\s+0\s+600\s+(\d+(?:\.\d+)?)\s*", vb or "")
        return bool(m) and float(m.group(1)) >= 280

    v.check(all(height_ok((draw.get(rg) or {}).get("viewBox")) for rg in RANGES), "(d) the svg viewBox is 0 0 600 H with H >= 280")

    rules = css_rules(getattr(render, "CHART_CSS", ""))
    fr = merged(rules, ends_with_class("rf-ch-frame"))
    bw, bs = border_of(fr)
    pad = padding_min(fr)
    print("CSS .rf-ch-frame:", fr)
    v.check(bw is not None and bw >= 1 and bs == "solid" and radius_of(fr) > 0 and pad is not None and pad >= 10 and has_background(fr),
            f"(e) CHART_CSS .rf-ch-frame has a border >= 1px solid, a border-radius, padding >= 10px, a background (read: border {bw} {bs}, radius {radius_of(fr)}, padding {pad})")

    ro = merged(rules, ends_with_class("rf-ch-read"))
    fs, fw = font_size(ro), font_weight(ro)
    print("CSS .rf-ch-read:", ro)
    v.check(fs is not None and fs >= 20 and fw is not None and fw >= 700,
            f"(f) CHART_CSS .rf-ch-read has font-size >= 20px and font-weight >= 700 (read: {fs}, {fw})")

    sample = css_rules("/* c */.rf-chart button{padding:1px 8px;border:1px solid #c5ccd8;background:#fff;border-radius:3px}"
                       "@media (max-width:9px){.x{y:z}}.rf-chart svg{display:block;width:100%}.q,.rf-ch-tip{font:700 20px/1.2 serif}")
    btn = merged(sample, lambda s: s.strip() == ".rf-chart button")
    svgr = merged(sample, lambda s: s.strip() == ".rf-chart svg")
    qq = merged(sample, ends_with_class("rf-ch-tip"))
    bbw, bbs = border_of(btn)
    css_reads = (bbw == 1 and bbs == "solid" and radius_of(btn) > 0 and padding_min(btn) == 1 and has_background(btn)
                 and svgr.get("display") == "block" and len(sample) == 3 and font_size(qq) == 20 and font_weight(qq) == 700)
    ones = [(rg, (draw.get(rg) or {})) for rg in RANGES]
    print("control: node", shutil.which("node") is not None, "| svgs / reads / move text:",
          [(rg, d.get("svgs"), d.get("reads"), bool(d.get("readText"))) for rg, d in ones], "| CSS parser on a sample stylesheet:", css_reads)
    v.check(shutil.which("node") is not None and out.get("loaded") is None and (out.get("has") or {}).get("plan") is True
            and all(d.get("svgs") == 1 and (d.get("reads") or 0) >= 1 and (d.get("moveListeners") or 0) >= 1 and bool(d.get("readText"))
                    for _, d in ones) and css_reads,
            "(g) control: node runs the script, the draw creates one svg and a rf-ch-read per range, the pointer move reaches a listener and leaves read-out text, the CSS parser reads a sample stylesheet")


v = c.Verdict("AC2")
try:
    run(v)
except SystemExit:
    raise
except Exception as e:  # noqa: BLE001 -- an import error at the base is the expected FAIL of a build check
    v.check(False, f"(x) exception: {type(e).__name__}: {e}")
labels = ", ".join(m.split(")")[0] + ")" for m in v.fails)
print("AC2 RESULT: PASS 0 failures" if not v.fails else f"AC2 RESULT: FAIL {len(v.fails)}: {labels}")
sys.exit(0 if not v.fails else 1)
