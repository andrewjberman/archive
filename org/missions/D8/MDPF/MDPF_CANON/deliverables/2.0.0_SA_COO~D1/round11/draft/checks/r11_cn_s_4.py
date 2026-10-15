#!/usr/bin/env python3
"""MDPF_CANON round 11 cell CN-s-4 (part 1: the Variant 2 repair) -- DRAFT check, 2.0.0_SA_COO~D1, 2026-10-15. Not issued.

PRD v2.23 FWD-9 head (a): a non-internal Global session (Variant 2) must never draw the Models band together with the model stack. In
buildGlobalTrendRows the band is set only before per_model_detail_begins, but the carry-forward loop rolls the last known band onto a
carried date AFTER the boundary (row MDPF_CANON-D1-S29). The repair: the Models band is never carried on or after the boundary.

  python r11_cn_s_4.py pure       six arms on the exported pure function, run under bun on fixtures (S0 and S3 and S5 are controls)
  python r11_cn_s_4.py selftest   issuer only: the base reads red on S1 S2, a scratch reference reads green, one planted mutant reddens its arm

Target: <git toplevel>/portal/src, or the directory in env R11_SRC. Output: `ROUND 11 CN-S-4 PURE: k of n arms`, exit 0 only when k == n.
The demo-tenant wiring arms (trendModeFor call site) and the real-object arm (0 of 497 rows draw both) are NOT here: they wait on reading the
page at HEAD at the cut.  ASCII only.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

PRIMARY = ["Ultra-Short Term", "Short Term", "Intermediate Term", "Long Term", "Ultra-Long Term"]
BEGINS = "2026-05-15"
N_ARMS = 6

BUN_TS = r"""
import { pathToFileURL } from 'node:url'
import { readFileSync } from 'node:fs'
const mod: any = await import(pathToFileURL(process.env.R11_MODULE as string).href)
const fx: any = JSON.parse(readFileSync(process.env.R11_FIX as string, 'utf8'))
const out: any = {}
out.missing = ['buildGlobalTrendRows'].filter((n) => typeof mod[n] !== 'function')
const safe = (f: () => any) => { try { return { v: f() } } catch (e: any) { return { err: String(e && e.message || e).slice(0, 120) } } }
if (out.missing.length === 0) {
  const run = (mode: string) => {
    const before = JSON.stringify(fx.served)
    const rows = mod.buildGlobalTrendRows(fx.served, fx.stitch, mode, fx.begins)
    return { rows, unchanged: before === JSON.stringify(fx.served) }
  }
  out.v1 = safe(() => run('variant1'))
  out.v2 = safe(() => run('variant2'))
}
console.log(JSON.stringify(out))
"""


def fixture():
    # 05-13 and 05-14 are before the boundary; 05-15 is the boundary date, measured; 05-16 and 05-17 are carried dates (no total, no legs).
    dates = ["2026-05-13", "2026-05-14", "2026-05-15", "2026-05-16", "2026-05-17"]
    n = [None] * 5
    primary = {k: list(n) for k in PRIMARY}
    for i, v in ((2, 10.0),):
        for k in PRIMARY:
            primary[k][i] = v
    total = [100.0, 101.0, 150.0, None, None]
    model_aua = [40.0, 41.0, 50.0, None, None]
    served = {
        "dates": dates, "total": total, "modelAua": model_aua, "primary": primary,
        "otherModels": [None, None, 5.0, None, None],
        "clientSupervised": [30.0, 30.0, 30.0, None, None], "etfStrategies": [20.0, 20.0, 20.0, None, None],
        "altStrategies": [None, None, 50.0, None, None], "carriedDates": ["2026-05-16", "2026-05-17"],
    }
    # the stitch is OFF for variant 2 (non-internal): a null stitch, as the page passes it
    return {"served": served, "stitch": None, "begins": BEGINS}


def run_bun(module):
    if not os.path.isfile(module):
        return None, "module not found: " + module
    d = tempfile.mkdtemp(prefix="r11cns4_")
    try:
        ex, fx = os.path.join(d, "exercise.ts"), os.path.join(d, "fixture.json")
        with open(ex, "w", newline="\n", encoding="utf-8") as fh:
            fh.write(BUN_TS)
        with open(fx, "w", newline="\n", encoding="utf-8") as fh:
            json.dump(fixture(), fh)
        env = dict(os.environ, R11_MODULE=module, R11_FIX=fx)
        try:
            r = subprocess.run(["bun", ex], capture_output=True, text=True, timeout=100, env=env, cwd=d)
        except subprocess.TimeoutExpired:
            return None, "bun exercise timed out"
        line = (r.stdout.strip().splitlines() or [""])[-1]
        try:
            return json.loads(line), ""
        except ValueError:
            tail = (r.stderr or r.stdout).strip().splitlines()[-1:] or [""]
            return None, "exercise rc=%d, no JSON: %s" % (r.returncode, tail[0][:160])
    finally:
        shutil.rmtree(d, ignore_errors=True)


def src_root():
    if os.environ.get("R11_SRC"):
        return os.environ["R11_SRC"]
    top = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    return os.path.join(top, "portal", "src")


def grade(got, err):
    """Returns a list of (name, ok, detail)."""
    if got is None:
        return [("exercise", False, err)]
    if got.get("missing"):
        return [("exports", False, "missing " + ",".join(got["missing"]))]
    v1 = (got.get("v1") or {}).get("v") or {}
    v2 = (got.get("v2") or {}).get("v") or {}
    r1, r2 = v1.get("rows"), v2.get("rows")
    if not r1 or not r2:
        return [("rows", False, "no rows: %s %s" % ((got.get("v1") or {}).get("err"), (got.get("v2") or {}).get("err")))]
    p2 ={r["period"]: r for r in r2}
    arms = []
    # S0 control: before the boundary Variant 2 still draws the band (the model assets it cannot break out)
    arms.append(("S0 control: before the boundary the band is drawn",
                 p2["2026-05-13"]["modelsBand"] == 40.0 and p2["2026-05-14"]["modelsBand"] == 41.0, "%s %s" % (p2["2026-05-13"]["modelsBand"], p2["2026-05-14"]["modelsBand"])))
    # S1: on a carried date AFTER the boundary the band is null and is not listed as carried
    c = [p2[d] for d in ("2026-05-16", "2026-05-17")]
    arms.append(("S1 the band is not carried after the boundary",
                 all(r["modelsBand"] is None and "Models" not in r["carried"] for r in c),
                 "band %s carried %s" % ([r["modelsBand"] for r in c], [r["carried"] for r in c])))
    # S2: no row draws the band together with any model line
    both = [r["period"] for r in r2 if r["modelsBand"] is not None and any(v is not None for v in r["models"].values())]
    arms.append(("S2 no row draws the band and the stack", not both, "rows with both: %s" % both))
    # S3 control: Variant 1 never draws the band
    arms.append(("S3 control: variant 1 draws no band", all(r["modelsBand"] is None for r in r1), "%s" % [r["modelsBand"] for r in r1]))
    # S4: the repair removes only the band: the five primary lines still carry on the carried dates (Variant 2)
    ok4 = all(p2[d]["models"][k] == 10.0 and k in p2[d]["carried"] for d in ("2026-05-16", "2026-05-17") for k in PRIMARY)
    arms.append(("S4 the primary lines still carry", ok4, "%s" % [p2[d]["models"] for d in ("2026-05-16",)]))
    # S5 control: the served input is not mutated
    arms.append(("S5 control: input not mutated", v1.get("unchanged") is True and v2.get("unchanged") is True, ""))
    return arms


def pure():
    src = src_root()
    got, err = run_bun(os.path.join(src, "lib", "trendGrouping.ts"))
    arms = grade(got, err)
    k = 0
    for name, ok, detail in arms:
        k += 1 if ok else 0
        print("  %s %s%s" % ("PASS" if ok else "FAIL", name, "" if ok else "  -- " + str(detail)[:200]))
    print("ROUND 11 CN-S-4 PURE: %d of %d arms" % (k, N_ARMS))
    return 0 if k == N_ARMS else 1


def selftest():
    src = src_root()
    mod = os.path.join(src, "lib", "trendGrouping.ts")
    text = open(mod, "rb").read().decode("utf-8")
    needle = "      if (v[key] === null && rolls && lastKnown[key] !== undefined && lastKnown[key] !== null) {"
    needle = needle.replace("\n", "\r\n") if "\r\n" in text and "\r\n" in needle else needle
    if needle not in text:
        print("SELFTEST: cannot find the roll-forward condition at the base; the reference patch needs the issuer's eyes")
        return 2
    patched = text.replace(needle, "      if (v[key] === null && rolls && !(key === MODELS_BAND_LABEL) && lastKnown[key] !== undefined && lastKnown[key] !== null) {")
    mutant_carry_all = text  # a planted defect: the base itself (band carried)
    mutant_drop_primaries = patched.replace("if (v[key] === null && rolls && !(key === MODELS_BAND_LABEL)", "if (false && v[key] === null && rolls && !(key === MODELS_BAND_LABEL)")  # no carry at all
    results = {}
    for name, body in (("base", mutant_carry_all), ("reference", patched), ("mutant-no-carry-at-all", mutant_drop_primaries)):
        d = tempfile.mkdtemp(prefix="r11self_")
        try:
            os.makedirs(os.path.join(d, "lib"))
            with open(os.path.join(d, "lib", "trendGrouping.ts"), "wb") as fh:
                fh.write(body.encode("utf-8"))
            sib = os.path.join(src, "lib")
            for f in os.listdir(sib):
                if f != "trendGrouping.ts" and f.endswith(".ts") and not f.endswith(".test.ts"):
                    shutil.copy(os.path.join(sib, f), os.path.join(d, "lib", f))
            got, err = run_bun(os.path.join(d, "lib", "trendGrouping.ts"))
            results[name] = grade(got, err)
        finally:
            shutil.rmtree(d, ignore_errors=True)
    for name, arms in results.items():
        print("%s: %s" % (name, " ".join("%s=%s" % (a[0].split()[0], "ok" if a[1] else "RED") for a in arms)))
    base_red = {a[0].split()[0] for a in results["base"] if not a[1]}
    ref_ok = all(a[1] for a in results["reference"])
    mut_red = {a[0].split()[0] for a in results["mutant-no-carry-at-all"] if not a[1]}
    good = base_red == {"S1", "S2"} and ref_ok and "S4" in mut_red
    print("CN-S-4 SELFTEST: %s (base red %s; reference green %s; mutant red %s)" % ("OK" if good else "NOT OK", sorted(base_red), ref_ok, sorted(mut_red)))
    return 0 if good else 1


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit({"pure": pure, "selftest": selftest}.get(cmd, lambda: print(__doc__) or 2)())
