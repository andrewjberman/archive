#!/usr/bin/env python3
"""MDPF_CANON cell CN-i-2 -- the repair of the AUA Trend candidate after the CVO's NOT MET (rows D1-C-S73, D1-C-S74; PRD v2.18).

Issuer's check (2.0.0_SA_COO~D1). Read-only for every worker: never edit this file.

  python r8_cn_i_2.py build     the three repairs on the portal source: colour (4), tooltip (5), the per-model-detail note and no band (4) = 13 arms
  python r8_cn_i_2.py data      the stack against the Total on the REAL served Global object, classified so it CAN fail (3 arms; reads S3, read-only)
  python r8_cn_i_2.py regress   the CN-i-1 module (9) and page (8) arms of r7_cn_i_1.py stay green: 2 aggregate arms
  python r8_cn_i_2.py selftest  the arms fail on the unpatched base, pass on a reference patch, six mutants RED, the classifier planted; issuer only

Targets: a portal `src` directory: `<git toplevel>/portal/src`, or the directory in env R8_SRC (selftest and the base dry-run use it).
Files read: lib/trendGrouping.ts, pages/ModelPortfolios.tsx, components/CategoryViewTree.tsx, api/portal-proxy.ts, lib/chartColors.ts, lib/modelPortfolioColors.ts.

THE COLOUR RULE (the CVO's instrument, D1-C-S73): CIEDE2000 between the Client Unsupervised colour and EVERY other colour the Trend draws is at least 10;
the implementation below is cross-checked against the five pairs the CVO published before any verdict is trusted (arm C1).

THE DATA CLASSIFIER (arm D1) replaces the CN-i-1 data arm D1, whose second branch allowed a gap up to 0.02 + |model_aua - sum(lines)| and so accepted every
date (the Total is built as model + non-model + SMA + tax, so that allowance IS the gap). Per valued date:
  IDENTITY-BREAK  the Total is not model_aua + non_model_aua + sma_additive_aua + tax_additive_aua (to 0.02)           -> FAIL
  EXACT           |Total - stack| <= 0.01
  BEFORE-DETAIL   date < meta.by_model_fold.per_model_detail_begins, NO model line holds a value, and the gap equals model_aua (to 0.02)
  FOLD-OR-OTHER   date >= the boundary and the stack is BELOW the Total by more than 0.01: counted, min and max printed, NOT claimed as fold-suppressed
                  (the served object carries no per-date fold record)
  FAIL            anything else (a model line before the boundary; the stack ABOVE the Total; a pre-boundary gap that is not the model AUA)

Output: `ROUND 8 CN-I-2 <NAME>: k of n arms`, exit 0 only when k == n. ASCII only.
"""
import importlib.util
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

BUCKET = "opal-data-assets"
HERE = os.path.dirname(os.path.abspath(__file__))
PREFIX = "portal/gold/mdpf/global/aggregate-aua-timeseries/"
CARVE = ("opal_div_sma", "opal_growth_sma")
LOCKED_MODEL = {"Ultra Short-Term": "#f97316", "Short-Term": "#f59e0b", "Intermediate-Term": "#10b981",
                "Long-Term": "#3b82f6", "Ultra Long-Term": "#ef4444"}
LOCKED_TOKENS = {"Custom": "fuchsia500", "ETF Strategies": "cyan400", "Client - Opal Supervised": "amber400"}
ALT_TOKEN = "vermilion500"
ORANGE_LOCKED = "#f97316"
MIN_DE = 10.0
CVO_PAIRS = (("#f97316", "#f97316", 0.0), ("#fbbf24", "#f59e0b", 10.6), ("#ff4f1f", "#ef4444", 10.5),
             ("#ff4f1f", "#f97316", 10.3), ("#d946ef", "#ef4444", 34.8))
N_BUILD = 13


# ---------------------------------------------------------------------------------------------- CIEDE2000
def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_lab(h):
    h = h.lstrip("#")
    r, g, b = (_lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    x = (0.4124564 * r + 0.3575761 * g + 0.1804375 * b) / 0.95047
    y = (0.2126729 * r + 0.7151522 * g + 0.0721750 * b) / 1.0
    z = (0.0193339 * r + 0.1191920 * g + 0.9503041 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def de00(h1, h2):
    L1, a1, b1 = hex_to_lab(h1)
    L2, a2, b2 = hex_to_lab(h2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if C1p else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if C2p else 0.0
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbp = (h1p + h2p) / 2
    else:
        hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dth = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc, Sh = 1 + 0.045 * Cbp, 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


# ---------------------------------------------------------------------------------------------- source reading
def root():
    r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR: not in a git worktree")
        sys.exit(2)
    return r.stdout.strip()


def src_root():
    return os.environ.get("R8_SRC") or os.path.join(root(), "portal", "src")


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read().replace("\r\n", "\n")


def parse_palette(chart):
    i = chart.index("export const PALETTE")
    j = chart.index("\n} as const", i) if "\n} as const" in chart[i:] else chart.index("\n}", i)
    return dict(re.findall(r"^\s*([A-Za-z0-9]+):\s*'(#[0-9a-fA-F]{6})'", chart[i:j], re.M))


def parse_l1(cvt):
    i = cvt.index("export const L1_COLOR")
    j = cvt.index("\n}", i)
    out = {}
    for m in re.finditer(r"^\s*(?:'([^']+)'|([A-Za-z]+)):\s*PALETTE\.([A-Za-z0-9]+)", cvt[i:j], re.M):
        out[m.group(1) or m.group(2)] = m.group(3)
    return out


def parse_model_primary(mpc, key):
    m = re.search(r"'%s':\s*\{[^}]*?primary:\s*'(#[0-9a-fA-F]{6})'" % re.escape(key), mpc)
    return m.group(1).lower() if m else None


def trend_colours(src):
    """The colours the Trend draws, resolved from the page's own sources. Returns (map, unsupervised_hex, problems)."""
    pal = parse_palette(read(os.path.join(src, "lib", "chartColors.ts")))
    l1 = parse_l1(read(os.path.join(src, "components", "CategoryViewTree.tsx")))
    mpc = read(os.path.join(src, "lib", "modelPortfolioColors.ts"))
    problems, cols = [], {}
    for name in LOCKED_MODEL:
        h = parse_model_primary(mpc, name)
        if h is None:
            problems.append("model colour %s unreadable" % name)
        else:
            cols["model:" + name] = h
    for key, tok in (("Custom", None), ("ETF Strategies", None), ("Client - Opal Supervised", None)):
        t = l1.get(key)
        if t is None or t not in pal:
            problems.append("L1_COLOR[%s] unreadable" % key)
        else:
            cols["l1:" + key] = pal[t].lower()
    m = re.search(r"'tax managed sma':\s*\{[^}]*?primary:\s*PALETTE\.([A-Za-z0-9]+)", mpc)
    if m and m.group(1) in pal:
        cols["alt"] = pal[m.group(1)].lower()
    else:
        problems.append("ALT colour unreadable")
    other = parse_model_primary(mpc, "Non-Model")
    if other:
        cols["other_aua"] = other
    else:
        problems.append("Other AUA colour unreadable")
    ut = l1.get("Client - Opal Unsupervised")
    unsup = pal[ut].lower() if ut in pal else None
    if unsup is None:
        problems.append("L1_COLOR[Client - Opal Unsupervised] unreadable")
    return cols, unsup, problems, l1


def colour_arms(src):
    arms = []
    worst = max(abs(de00(a, b) - want) for a, b, want in CVO_PAIRS)
    arms.append(("C1", worst <= 0.06, "CIEDE2000 reproduces the CVO's five published pairs (worst difference %.3f of 0.06 allowed)" % worst))
    try:
        cols, unsup, problems, l1 = trend_colours(src)
    except (OSError, ValueError) as exc:
        why = "colour sources unreadable: %s" % exc
        return arms + [("C2", False, why), ("C3", False, why), ("C4", False, why)]
    arms.append(("C2", unsup is not None and unsup != ORANGE_LOCKED and not problems,
                 "Client Unsupervised resolves to %s (the locked Ultra-Short Term hex is %s)%s" % (unsup, ORANGE_LOCKED, "; " + "; ".join(problems) if problems else "")))
    if unsup is None:
        arms.append(("C3", False, "no Client Unsupervised colour to measure"))
    else:
        dists = sorted((de00(unsup, h), k) for k, h in cols.items())
        lo = dists[0] if dists else (0.0, "none")
        arms.append(("C3", len(dists) == 10 and lo[0] >= MIN_DE,
                     "minimum CIEDE2000 from Client Unsupervised %s to the %d other Trend colours: %.2f vs %s (rule: at least %.0f)" % (unsup, len(dists), lo[0], lo[1], MIN_DE)))
    expect_ok = all(cols.get("model:" + k) == v for k, v in LOCKED_MODEL.items())
    pal = parse_palette(read(os.path.join(src, "lib", "chartColors.ts")))
    tok_ok = all(l1.get(k) == t for k, t in LOCKED_TOKENS.items()) and cols.get("alt") == pal.get(ALT_TOKEN, "").lower()
    arms.append(("C4", expect_ok and tok_ok,
                 "CONTROL: the five locked model hexes and the Custom, ETF, Client Supervised and ALT colours are untouched (models %s, tokens %s)" % (expect_ok, tok_ok)))
    return arms


# ---------------------------------------------------------------------------------------------- bun exercise
BUN_TS = r"""
import { pathToFileURL } from 'node:url'
const mod: any = await import(pathToFileURL(process.env.R8_MODULE as string).href)
const pres = mod.presentTrendEntries as (e: any[]) => any[]
const note = mod.trendDetailNote as (b: any, f: any) => string | null
const out: string[] = []
const arm = (id: string, ok: boolean, why: string) => out.push(`ARM ${id} ${ok ? 'PASS' : 'FAIL'} ${why}`)
const has = typeof pres === 'function'
const names = (a: any[]) => a.map((x) => x.name).join(',')
const mixed = [
  { name: 'Short Term', value: 5 }, { name: 'Client Supervised', value: null }, { name: 'Client Unsupervised', value: undefined },
  { name: 'Long Term', value: 7.5 }, { name: 'Blank', value: '' }, { name: 'Nan', value: Number.NaN }, { name: 'Inf', value: Infinity },
]
const snap = JSON.stringify(mixed)
const r1 = has ? pres(mixed) : []
arm('T1', has && names(r1) === 'Short Term,Long Term', `null, undefined, '', NaN and Infinity drop; order kept (got ${has ? names(r1) : 'no function'})`)
const z = has ? pres([{ name: 'Zero', value: 0 }, { name: 'ZeroStr', value: '0' }, { name: 'Neg', value: -3.25 }, { name: 'NumStr', value: '12.5' }]) : []
arm('T2', has && names(z) === 'Zero,ZeroStr,Neg,NumStr', `a measured zero (number or string), a negative and a numeric string stay (got ${has ? names(z) : 'no function'})`)
const inCopy = has ? pres(mixed) : []
arm('T3', has && JSON.stringify(mixed) === snap && inCopy !== (mixed as any) && Array.isArray(pres([])) && pres([]).length === 0,
  'the input is not mutated, a new array comes back, an empty payload gives an empty array')
const dateC = has ? pres([{ name: 'Short Term', value: 5 }, { name: 'Client Supervised', value: null }, { name: 'Client Unsupervised', value: null }]) : []
arm('T4', has && dateC.length === 1 && dateC[0].name === 'Short Term', 'a date with null Client chips lists no Client row (no $0 row for an absent series)')
const hasNote = typeof note === 'function'
const n1 = hasNote ? note('2026-05-15', '2024-11-01') : undefined
const okText = typeof n1 === 'string' && /per-model detail begins May 15, 2026/i.test(n1) && /earlier model assets are in the Total and are not broken out/.test(n1)
arm('N2', hasNote && okText && note('2026-05-15', '2026-05-15') === null && note('2026-05-15', '2026-05-16') === null
  && note(undefined, '2024-11-01') === null && note(null, '2024-11-01') === null && note('2026-05-15', undefined) === null
  && note('May 15', '2024-11-01') === null && note('2026-05-15', '2026-05-14') !== null,
  `the note names the boundary date and says earlier model assets are in the Total; null on equal or later first period, a missing date or a non-ISO date (got ${JSON.stringify(n1)})`)
console.log(out.join('\n'))
"""


def run_bun(module):
    if not os.path.isfile(module):
        return {}, "module not found: " + module
    d = tempfile.mkdtemp(prefix="r8cni2_")
    try:
        ex = os.path.join(d, "exercise.ts")
        with open(ex, "w", newline="\n", encoding="utf-8") as fh:
            fh.write(BUN_TS)
        env = dict(os.environ)
        env["R8_MODULE"] = module
        try:
            r = subprocess.run(["bun", ex], capture_output=True, text=True, timeout=100, env=env, cwd=d)
        except subprocess.TimeoutExpired:
            return {}, "bun exercise timed out"
        got = {}
        for line in r.stdout.splitlines():
            m = re.match(r"ARM (\w+) (PASS|FAIL) (.*)", line)
            if m:
                got[m.group(1)] = (m.group(2) == "PASS", m.group(3))
        if r.returncode != 0 or len(got) != 5:
            tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
            return got, "exercise rc=%d arms=%d %s" % (r.returncode, len(got), tail[0][:160])
        return got, ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


def tooltip_note_arms(src):
    module = os.path.join(src, "lib", "trendGrouping.ts")
    page = read(os.path.join(src, "pages", "ModelPortfolios.tsx"))
    proxy = read(os.path.join(src, "api", "portal-proxy.ts"))
    got, err = run_bun(module)
    arms = []

    def bun_arm(aid):
        if aid in got:
            return got[aid][0], got[aid][1]
        return False, err or "no result"
    for aid in ("T1", "T2", "T3", "T4"):
        ok, why = bun_arm(aid)
        arms.append((aid, ok, why))
    # T5 the page: renderTrendTooltip filters its buckets through the pure helper before it formats a row.
    i = page.find("const renderTrendTooltip")
    seg = page[i:i + 6000] if i >= 0 else ""
    imp = re.search(r"import \{[^}]*\bpresentTrendEntries\b[^}]*\} from '[^']*trendGrouping'", page) is not None
    wired = re.search(r"const buckets = presentTrendEntries\(", seg) is not None
    raw = re.search(r"const buckets = payload\.filter", seg) is not None
    arms.append(("T5", imp and wired and not raw, "page imports presentTrendEntries (%s); renderTrendTooltip buckets go through it (%s); the raw filter is gone (%s)" % (imp, wired, not raw)))
    # N1 the served meta is typed: the proxy's per-firm series carries meta.by_model_fold.per_model_detail_begins.
    m = re.search(r"export interface MdpfPerFirmTimeSeries \{(.*?)\n\}\n", proxy, re.S)
    body = m.group(1) if m else ""
    typed = "by_model_fold" in body and "per_model_detail_begins" in body
    arms.append(("N1", typed, "MdpfPerFirmTimeSeries.meta carries by_model_fold.per_model_detail_begins (%s)" % typed))
    ok, why = bun_arm("N2")
    arms.append(("N2", ok, why))
    # N3 the page prints the note from the served boundary, Global only, in its own element.
    imp_n = re.search(r"import \{[^}]*\btrendDetailNote\b[^}]*\} from '[^']*trendGrouping'", page) is not None
    call = re.search(r"trendDetailNote\([^)]*by_model_fold\??\.per_model_detail_begins", page) is not None
    gated = re.search(r"isGlobalSI\s*\?\s*trendDetailNote\(", page) is not None
    el = 'data-trend-detail-note' in page and re.search(r"\{detailNote\s*&&", page) is not None
    arms.append(("N3", imp_n and call and gated and el,
                 "imports trendDetailNote (%s), reads meta.by_model_fold.per_model_detail_begins (%s), Global only (%s), own element data-trend-detail-note (%s)" % (imp_n, call, gated, el)))
    # N4 NO band (PRD v2.18: a band of suppressed model dollars would draw what FWD-3 forbids): the mount spine is the thirteen CN-i-1 series.
    m = re.search(r"const STACK_SERIES[^=]*=\s*\[(.*?)\n\]", page, re.S)
    blk = m.group(1) if m else ""
    labels = re.findall(r"label:\s*'([^']+)'", blk)
    bad = [x for x in labels if re.search(r"withheld|detail|unattributed|suppress|Models \(", x, re.I)]
    arms.append(("N4", len(labels) == 13 and not bad and "Custom Models" in labels,
                 "STACK_SERIES holds %d series (must be the thirteen CN-i-1 series), band-like labels: %s" % (len(labels), bad)))
    return arms


def build_arms(src):
    arms = colour_arms(src) + tooltip_note_arms(src)
    order = ["C1", "C2", "C3", "C4", "T1", "T2", "T3", "T4", "T5", "N1", "N2", "N3", "N4"]
    arms.sort(key=lambda a: order.index(a[0]) if a[0] in order else 99)
    return arms


# ---------------------------------------------------------------------------------------------- the data classifier
def _num(x):
    return 0.0 if x is None else float(x)


def classify(ts):
    """Classify every valued date of a served Global aggregate-aua-timeseries object. Pure: used by `data` and by the planted selftest."""
    dates = ts["dates"]
    bm = ts["by_model"]
    sma = {k for k, v in bm.items() if v.get("cohort_class") == "sma"}
    model = {k: v for k, v in bm.items() if k not in sma}
    fold = (ts.get("meta") or {}).get("by_model_fold") or {}
    begins = fold.get("per_model_detail_begins")

    def at(k, i):
        arr = (bm.get(k) or {}).get("model_value") or []
        return arr[i] if i < len(arr) else None
    res = {"begins": begins, "dates": len(dates), "valued": 0, "EXACT": [], "BEFORE-DETAIL": [], "FOLD-OR-OTHER": [], "IDENTITY-BREAK": [], "FAIL": [],
           "first_line_date": None, "pre_boundary_with_line": []}
    for i, d in enumerate(dates):
        tot, nm, ma = ts["opal_aggregate_aua"][i], ts["non_model_aua"][i], ts["model_aua"][i]
        if tot is None or nm is None or ma is None:
            continue
        res["valued"] += 1
        smaA, tax = _num(ts["sma_additive_aua"][i]), _num(ts["tax_additive_aua"][i])
        any_line = any(at(k, i) is not None for k in model)
        if any_line and res["first_line_date"] is None:
            res["first_line_date"] = d
        if abs(tot - (ma + nm + smaA + tax)) > 0.02:
            res["IDENTITY-BREAK"].append((d, round(tot - (ma + nm + smaA + tax), 2)))
            continue
        lines = sum(_num(at(k, i)) for k in model)
        carve = sum(_num(at(k, i)) for k in CARVE)
        stack = lines + smaA + carve + tax + (nm - carve)
        gap = round(tot - stack, 2)
        if abs(gap) <= 0.01:
            res["EXACT"].append((d, gap))
        elif begins is not None and d < begins:
            if any_line:
                res["pre_boundary_with_line"].append(d)
                res["FAIL"].append((d, gap))
            elif abs(gap - round(ma, 2)) <= 0.02:
                res["BEFORE-DETAIL"].append((d, gap))
            else:
                res["FAIL"].append((d, gap))
        elif begins is not None and gap > 0.01:
            res["FOLD-OR-OTHER"].append((d, gap))
        else:
            res["FAIL"].append((d, gap))
    return res


def _mm(rows):
    vals = [g for _, g in rows]
    return "n/a" if not vals else "%.2f to %.2f" % (min(vals), max(vals))


def data_arms_from(ts):
    r = classify(ts)
    arms = []
    bad = len(r["FAIL"]) + len(r["IDENTITY-BREAK"])
    arms.append(("D1", r["valued"] > 0 and r["begins"] is not None and bad == 0,
                 "valued %d of %d dates: EXACT %d; BEFORE-DETAIL %d (gap = the whole model AUA, %s); FOLD-OR-OTHER %d (stack below the Total, %s; NOT claimed as fold-suppressed); "
                 "FAIL %d %s; boundary %s"
                 % (r["valued"], r["dates"], len(r["EXACT"]), len(r["BEFORE-DETAIL"]), _mm(r["BEFORE-DETAIL"]), len(r["FOLD-OR-OTHER"]), _mm(r["FOLD-OR-OTHER"]),
                    len(r["FAIL"]), r["FAIL"][:2], r["begins"])))
    arms.append(("D2", r["begins"] is not None and r["first_line_date"] == r["begins"] and not r["pre_boundary_with_line"],
                 "the boundary is real: per_model_detail_begins %s, first date with any model line %s, dates before the boundary carrying a model line: %d"
                 % (r["begins"], r["first_line_date"], len(r["pre_boundary_with_line"]))))
    arms.append(("D3", r["valued"] > 0 and not r["IDENTITY-BREAK"],
                 "the served Total is model + non-model + SMA + tax on every valued date (%d identity breaks of %d; tolerance 0.02)" % (len(r["IDENTITY-BREAK"]), r["valued"])))
    return arms


def run_data():
    import boto3
    s3 = boto3.client("s3", region_name="us-east-1")
    ks = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX):
        ks += [o["Key"] for o in p.get("Contents", []) if o["Key"].endswith(".json")]
    if not ks:
        return [("D1", False, "no served object under " + PREFIX)]
    key = sorted(ks)[-1]
    ts = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read())
    print("  object %s (%d dates)" % (key.split("/")[-1], len(ts["dates"])))
    return data_arms_from(ts)


# ---------------------------------------------------------------------------------------------- regress (CN-i-1 arms)
def regress_arms(src):
    here = [os.path.join(HERE, "r7_cn_i_1.py"), os.path.join(HERE, "..", "checks", "r7_cn_i_1.py"), os.path.join(HERE, "..", "..", "checks", "r7_cn_i_1.py")]
    script = next((p for p in here if os.path.isfile(p)), None)
    if script is None:
        return [("R0", False, "r7_cn_i_1.py not found beside this check")]
    env = dict(os.environ)
    env["R7_MODULE"] = os.path.join(src, "lib", "trendGrouping.ts")
    env["R7_PAGE"] = os.path.join(src, "pages", "ModelPortfolios.tsx")
    env["R7_CVT"] = os.path.join(src, "components", "CategoryViewTree.tsx")
    arms = []
    for mode, want in (("module", 9), ("page", 8)):
        r = subprocess.run([sys.executable, script, mode], capture_output=True, text=True, timeout=110, env=env)
        m = re.search(r"ROUND 7 [A-Z-]+: (\d+) of (\d+) arms", r.stdout)
        k, n = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        arms.append(("R-" + mode, k == want and n == want, "CN-i-1 %s arms: %d of %d" % (mode, k, n)))
    return arms


def report(name, arms):
    for a in arms:
        print("  %s %s %s" % (a[0], "PASS" if a[1] else "FAIL", a[2]))
    k = sum(1 for a in arms if a[1])
    print("ROUND 8 CN-I-2 %s: %d of %d arms" % (name, k, len(arms)))
    return k, len(arms)


# ---------------------------------------------------------------------------------------------- selftest (issuer only)
def _synthetic(n_pre=3, n_post=3, partial_pre=False, above=False, ident_break=False):
    begins = "2026-05-15"
    dates = ["2026-05-%02d" % d for d in range(10, 10 + n_pre)] + ["2026-05-%02d" % d for d in range(15, 15 + n_post)]
    n = len(dates)
    ma = [100.0] * n
    nm = [50.0] * n
    sma = [10.0] * n
    tax = [5.0] * n
    tot = [165.0] * n
    line = [None] * n_pre + [100.0, 60.0, 100.0][:n_post]
    if partial_pre:
        line[0] = 40.0
    if above:
        line[-1] = 130.0
        ma[-1] = 130.0
        tot[-1] = 165.0 + 30.0 - 30.0
    if ident_break:
        tot[1] = 999.0
    ts = {"dates": dates, "opal_aggregate_aua": tot, "non_model_aua": nm, "model_aua": ma, "sma_additive_aua": sma, "tax_additive_aua": tax,
          "by_model": {"opal_x": {"cohort_class": "model", "model_value": line}},
          "meta": {"by_model_fold": {"min_firms": 2, "per_model_detail_begins": begins}}}
    return ts


def selftest():
    ref_mod = importlib.util.spec_from_file_location("mk", os.path.join(HERE, "ref", "make_reference_tree_i2.py"))
    mk = importlib.util.module_from_spec(ref_mod)
    ref_mod.loader.exec_module(mk)
    portal = os.path.join(root(), "portal")
    d = tempfile.mkdtemp(prefix="r8cni2_self_")
    ok_all = True
    try:
        def tree(name, mutant=None):
            p = os.path.join(d, name)
            mk.build(p, mutant, portal)
            return p
        ref = build_arms(tree("ref"))
        print("selftest reference tree:", sum(a[1] for a in ref), "of", len(ref))
        ok_all &= len(ref) == N_BUILD and all(a[1] for a in ref)
        base = os.path.join(d, "base")
        for rel in mk.FILES:
            out = os.path.join(base, *rel.split("/"))
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(mk.show(portal, rel))
        b = build_arms(base)
        failing = sorted(a[0] for a in b if not a[1])
        print("selftest unpatched base: red arms", failing)
        ok_all &= failing == ["C2", "C3", "N1", "N2", "N3", "T1", "T4", "T5"] or set(["C2", "C3", "T5", "N1", "N3"]) <= set(failing)
        for mut, expect in (("colour", ("C2", "C3")), ("dropzero", ("T2",)), ("equalnote", ("N2",)), ("band", ("N4",)), ("nonote", ("N3",)), ("nometa", ("N1",))):
            arms = build_arms(tree("m_" + mut, mut))
            red = sorted(a[0] for a in arms if not a[1])
            hit = all(e in red for e in expect)
            print("selftest mutant %-9s red arms %s -> %s" % (mut, red, "OK" if hit else "NOT CAUGHT"))
            ok_all &= hit
        for label, kw, want_fail in (("clean", {}, False), ("partial model line before the boundary", {"partial_pre": True}, True),
                                     ("stack above the Total", {"above": True}, True), ("identity break", {"ident_break": True}, True)):
            ts = _synthetic(**kw)
            r = classify(ts)
            fails = len(r["FAIL"]) + len(r["IDENTITY-BREAK"])
            res = fails > 0
            print("selftest data classifier %-40s FAIL+BREAK %d -> %s" % (label, fails, "OK" if res == want_fail else "WRONG"))
            ok_all &= res == want_fail
        # the OLD CN-i-1 rule, run on the same planted partial-line date, accepts it: the reason the arm is replaced
        ts = _synthetic(partial_pre=True)
        accepted = True
        for i in range(len(ts["dates"])):
            tot, ma = ts["opal_aggregate_aua"][i], ts["model_aua"][i]
            lines = _num(ts["by_model"]["opal_x"]["model_value"][i])
            stack = lines + 10.0 + 5.0 + 50.0
            gap = round(tot - stack, 2)
            if not (abs(gap) < 0.005 or abs(gap) <= 0.02 + abs(round(ma - lines, 2))):
                accepted = False
        print("selftest old CN-i-1 D1 rule accepts every planted date: %s (the vacuous branch)" % accepted)
        ok_all &= accepted
    finally:
        shutil.rmtree(d, ignore_errors=True)
    print("ROUND 8 CN-I-2 SELFTEST: %s" % ("OK" if ok_all else "NOT OK"))
    return 0 if ok_all else 1


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("build", "data", "regress", "selftest"):
        print(__doc__)
        return 2
    mode = sys.argv[1]
    if mode == "selftest":
        return selftest()
    if mode == "data":
        k, n = report("DATA", run_data())
    elif mode == "regress":
        k, n = report("REGRESS", regress_arms(src_root()))
    else:
        k, n = report("BUILD", build_arms(src_root()))
    return 0 if k == n else 1


if __name__ == "__main__":
    sys.exit(main())
