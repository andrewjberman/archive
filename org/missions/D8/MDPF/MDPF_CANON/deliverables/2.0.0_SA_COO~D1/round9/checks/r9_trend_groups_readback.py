#!/usr/bin/env python3
"""MDPF_CANON CN-p-1 -- the acceptance READ-BACK of the Variant 1 Trend groups on the served gold objects (issuer's instrument, read-only).

  python r9_trend_groups_readback.py read                    newest served objects from S3 (+ the prior dated object per scope), 11 arms
  python r9_trend_groups_readback.py read --dir D            the same arms over local files in D (names below)
  python r9_trend_groups_readback.py read --expect absent    the PRE-FIRE state: the four keys must be ABSENT on every scope (exit 0 = absent)
  python r9_trend_groups_readback.py fixture --served D --out O   build a PASS fixture from served files with the merged CN-p-1 code (repo import)
  python r9_trend_groups_readback.py selftest                absent check on the served files + fixture PASS + planted defects each red

Local file names in a --dir (one per scope in global, 49financial, inflection, cottonwood):
  <scope>__aggregate-aua-timeseries.json   the NEWEST served object
  <scope>__aggregate-aua-timeseries.prior.json   the PRIOR dated object (optional; arm R6 is skipped-and-said without it, never passed)
  <scope>__category-views.json              the newest category-views object
S3 mode reads s3://opal-data-assets/portal/gold/mdpf/<scope>/<type>/<date>.json (newest and the one before it) and the newest
_manifests object. Output: `R9 TREND-GROUPS READBACK: k of n arms`, one line per arm. ASCII only. Exit 0 only when k == n.
"""
import json
import os
import re
import subprocess
import sys

SCOPES = ("global", "49financial", "inflection", "cottonwood")
KEYS = ("client_supervised_aua", "etf_strategies_aua", "alt_strategies_aua")
CARRIED = "carried_dates"
RESTATE_MAX = 5
NEW = KEYS + (CARRIED,)
BUCKET = "opal-data-assets"
PREFIX = "portal/gold/mdpf"
# The CRO spec's AMENDED period-end oracle, $M (Client Sup., ETF, ALT, Total); spec @686f769e63, "Amended oracle".
ORACLE = {
    "2024-12-31": (356.8, 5.8, 0.0, 874.6),
    "2025-03-31": (275.8, 13.1, 0.0, 977.0),
    "2025-06-30": (234.3, 17.2, 0.0, 1069.1),
    "2025-09-30": (239.4, 19.9, 0.0, 1184.0),
    "2025-12-31": (268.8, 22.2, 0.0, 1380.8),
    "2026-03-31": (250.7, 23.7, 0.0, 1477.9),
    "2026-06-30": (228.6, 23.1, 0.0, 1770.6),
    "2026-09-30": (266.6, 21.2, 24.8, 2109.9),
    "2026-10-13": (292.3, 21.5, 29.2, 2177.1),
}
GAETR_END = "2025-03-27"          # the Global All Equity Total Return leg exists only before this date (SMArtX), <= about $0.06M
IDENTITY_TOL = 0.011
GAETR_MAX = 60000.0


class Arms:
    def __init__(self, name):
        self.name, self.rows = name, []

    def arm(self, aid, ok, detail):
        self.rows.append((aid, bool(ok), detail))
        print("  %-3s %-4s %s" % (aid, "PASS" if ok else "FAIL", detail))

    def done(self):
        k = sum(1 for _, ok, _ in self.rows if ok)
        print("%s: %d of %d arms" % (self.name, k, len(self.rows)))
        return 0 if k == len(self.rows) else 1


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ---------------------------------------------------------------- loading
def load_dir(d):
    out = {}
    for s in SCOPES:
        def rd(t, suffix=""):
            p = os.path.join(d, "%s__%s%s.json" % (s, t, suffix))
            return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
        out[s] = {"ts": rd("aggregate-aua-timeseries"), "prior": rd("aggregate-aua-timeseries", ".prior"), "cv": rd("category-views")}
    return out, None


def load_s3():
    import boto3
    s3 = boto3.client("s3")

    def keys(scope, t):
        ks = []
        for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="%s/%s/%s/" % (PREFIX, scope, t)):
            ks += [c["Key"] for c in pg.get("Contents", []) if c["Key"].endswith(".json")]
        return sorted(ks)

    def get(k):
        return json.loads(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read())
    out = {}
    for s in SCOPES:
        ts_keys, cv_keys = keys(s, "aggregate-aua-timeseries"), keys(s, "category-views")
        out[s] = {"ts": get(ts_keys[-1]), "prior": get(ts_keys[-2]) if len(ts_keys) > 1 else None, "cv": get(cv_keys[-1]),
                  "ts_key": ts_keys[-1]}
    mans = []
    for pg in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=PREFIX + "/_manifests/"):
        mans += pg.get("Contents", [])
    mans.sort(key=lambda c: c["LastModified"])
    manifest = json.loads(s3.get_object(Bucket=BUCKET, Key=mans[-1]["Key"])["Body"].read()) if mans else None
    return out, manifest


# ---------------------------------------------------------------- helpers
def last_dated_idx(ts, upto):
    best = None
    tot = ts.get("opal_aggregate_aua") or []
    for i, d in enumerate(ts.get("dates") or []):
        if d <= upto and i < len(tot) and tot[i] is not None:
            best = i
    return best


def walk_members(cv):
    node = ((cv or {}).get("nodes") or {}).get("SMA", {}).get("children", {}).get("ALT Strategies")
    return node


# ---------------------------------------------------------------- arms
def absent_mode(data):
    a = Arms("R9 TREND-GROUPS PRE-FIRE")
    for s in SCOPES:
        ts = data[s]["ts"]
        present = [k for k in NEW if k in ts]
        a.arm("P-" + s[:3], not present, "%s: new keys present %s (expected none before the first fire carrying CN-p-1)" % (s, present))
    return a.done()


def read_mode(data, manifest, pin=None):
    a = Arms("R9 TREND-GROUPS READBACK")
    g = data["global"]["ts"]
    dates = g.get("dates") or []
    n = len(dates)
    # R1
    miss = [k for k in NEW if k not in g]
    badlen = [k for k in KEYS if k in g and len(g[k]) != n]
    cd = g.get(CARRIED)
    cd_ok = isinstance(cd, list) and cd == sorted(cd) and all(isinstance(x, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) for x in cd) and set(cd) <= set(dates)
    a.arm("R1", not miss and not badlen and cd_ok,
          "global: missing %s, wrong length %s (dates %d), carried_dates sorted ISO subset of dates %s" % (miss, badlen, n, cd_ok))
    # R2
    bad = {}
    for s in SCOPES[1:]:
        ts = data[s]["ts"]
        d = len(ts.get("dates") or [])
        ok = all(k in ts and len(ts[k]) == d and all(v is None for v in ts[k]) for k in KEYS) and ts.get(CARRIED) == []
        if not ok:
            bad[s] = [k for k in NEW if k not in ts]
    a.arm("R2", not bad, "49financial, inflection, cottonwood: the three arrays all-None aligned to dates[] and carried_dates []%s" % ("" if not bad else "; offending " + json.dumps(bad)))
    # R3 oracle
    fails, checked = [], 0
    for pe, (cs, etf, alt, tot) in sorted(ORACLE.items()):
        i = last_dated_idx(g, pe)
        if i is None or any(k not in g for k in KEYS):
            fails.append((pe, "no dated row or key absent"))
            continue
        got = [(g[KEYS[0]][i] or 0.0) / 1e6, (g[KEYS[1]][i] or 0.0) / 1e6, (g[KEYS[2]][i] or 0.0) / 1e6, (g["opal_aggregate_aua"][i] or 0.0) / 1e6]
        checked += 1
        for lab, gv, ov in zip(("CS", "ETF", "ALT", "TOTAL"), got, (cs, etf, alt, tot)):
            if abs(gv - ov) > 0.0501:
                fails.append((pe, "%s got %.2f oracle %.1f" % (lab, gv, ov)))
    a.arm("R3", not fails and checked == len(ORACLE), "amended period-end oracle at %d period ends (+-0.05 $M on Client Sup, ETF, ALT and the Total)%s" % (checked, "" if not fails else "; " + "; ".join("%s %s" % f for f in fails[:4])))
    # R4 identity
    worst, count, bad4 = 0.0, 0, []
    ma = g.get("model_aua") or []
    for i, d in enumerate(dates):
        tot = (g.get("opal_aggregate_aua") or [None] * n)[i]
        cs, etf, alt = (g.get(k, [None] * n)[i] for k in KEYS)
        if tot is None or i >= len(ma) or ma[i] is None or cs is None or etf is None:
            continue
        count += 1
        r = tot - ma[i] - cs - etf - (alt or 0.0)      # ALT is null before its first observation (2026-09-30): absent adds nothing
        lim_lo, lim_hi = (-IDENTITY_TOL, GAETR_MAX) if d < GAETR_END else (-IDENTITY_TOL, IDENTITY_TOL)
        worst = max(worst, abs(r) if d >= GAETR_END else 0.0)
        if not (lim_lo <= r <= lim_hi):
            bad4.append((d, round(r, 2)))
    a.arm("R4", count > 0 and not bad4, "partition identity total - model_aua - (Client Sup + ETF + ALT, ALT null = 0 before 2026-09-30) on %d dated rows: residual within [0, 0.06M] before %s (the Global All Equity TR leg) and within 0.01 after; offending %s" % (count, GAETR_END, bad4[:3]))
    # R5 carried
    nototal = [d for i, d in enumerate(dates) if (g.get("opal_aggregate_aua") or [None] * n)[i] is None]
    a.arm("R5", cd == nototal if isinstance(cd, list) else False, "carried_dates equals the dates with no total (%d): %s" % (len(nototal), "equal" if cd == nototal else "got %s want %s" % (cd, nototal)))
    # R6 prior
    r6 = []
    restated = []
    skipped = []
    for s in SCOPES:
        ts, pr = data[s]["ts"], data[s].get("prior")
        if pr is None:
            skipped.append(s)
            continue
        added = sorted(set(ts) - set(pr))
        dropped = sorted(set(pr) - set(ts))
        if dropped:
            r6.append((s, "dropped keys", dropped[:4]))
        if sorted(set(added) - set(NEW)):
            r6.append((s, "unexpected new keys", sorted(set(added) - set(NEW))[:4]))
        sh = min(len(pr.get("dates") or []), len(ts.get("dates") or []))
        for k in ("opal_aggregate_aua", "point_class", "non_model_aua", "model_aua"):
            if k in pr and k in ts:
                # a routine day-over-day restatement of a few cells is data, not a CN-p-1 effect (CloudOps 2026-10-14: 1 cell);
                # more than RESTATE_MAX moved cells in one array is a defect (a splice or a bug moves them by the hundred)
                moved = [i for i in range(sh) if pr[k][i] != ts[k][i]]
                if len(moved) > RESTATE_MAX:
                    r6.append((s, "moved on shared dates", k, len(moved)))
                elif moved:
                    restated.append("%s.%s %d cell(s)" % (s, k, len(moved)))
    a.arm("R6", not r6 and not skipped, "against the prior dated object per scope: only the four new keys added, none dropped, opal_aggregate_aua, point_class, non_model_aua, model_aua equal on the shared dates except at most %d restated cells per array (restated: %s)%s%s" % (
        RESTATE_MAX, restated or "none", "" if not r6 else "; " + json.dumps(r6[:3]), "" if not skipped else "; NO PRIOR OBJECT for %s (not passed)" % skipped))
    # R7 category-views
    bad7 = {}
    for s in SCOPES:
        node = walk_members(data[s]["cv"])
        mem = [m.get("member_id") for m in (node or {}).get("members", [])]
        if node is None or "muni" in mem:
            bad7[s] = mem
    a.arm("R7", not bad7, "category-views SMA > ALT Strategies lists no 'Muni SMA' member on any scope%s" % ("" if not bad7 else "; " + json.dumps(bad7)))
    # R8 meta
    meta = (g.get("meta") or {}).get("trend_groups") or {}
    a.arm("R8", bool(meta.get("smartx_partition")) and (meta.get("smartx_dates") or 0) > 0 and meta.get("smartx_legs_until") == "2026-05-18",
          "global meta.trend_groups names the SMArtX partition read (%s), its date count (%s) and the 2026-05-18 boundary" % (meta.get("smartx_partition"), meta.get("smartx_dates")))
    # R9 manifest
    if manifest is None:
        a.arm("R9", False, "no manifest read (local mode has none: R9 is not passed)")
    else:
        run = manifest.get("run") or {}
        commit = (run.get("code") or {}).get("commit")
        ok = not manifest.get("errors") and (pin is None or commit == pin)
        a.arm("R9", ok, "run manifest errors %s, run.code.commit %s%s" % (sorted(manifest.get("errors") or {}), commit, "" if pin is None else " (pin %s)" % pin))
    # R10 disjoint from the frontier cell: the CN-p-1 keys are not among the keys that CN-h-1/CN-l-1 move
    h1 = {"account_count_total", "account_count_total_raw", "count_provenance", "count_basis", "count_as_of"}
    a.arm("R10", not (set(NEW) & h1), "the CN-p-1 key set %s shares no top-level key with the CN-h-1 count fields %s (the leaf-by-leaf table of the pair, section 4)" % (sorted(NEW), sorted(h1)))
    # R11 leg presence (CTO condition C1, msg 5940): a leg absent on the newest dated row while it held a value the day before is Branch B
    ndr = last_dated_idx(g, "9999-12-31")
    prev = None
    if ndr is not None:
        for j in range(ndr - 1, -1, -1):
            if (g.get("opal_aggregate_aua") or [None] * n)[j] is not None:
                prev = j
                break
    bm = g.get("by_model") or {}

    def _leg(name, i):
        if i is None:
            return None
        if name == "sma_additive_aua":
            arr = g.get(name) or []
        else:
            arr = (bm.get(name) or {}).get("model_value") or []
        return i < len(arr) and arr[i] is not None

    legs = ("opal_div_sma", "opal_growth_sma", "sma_additive_aua")
    now = {nm: _leg(nm, ndr) for nm in legs}
    before = {nm: _leg(nm, prev) for nm in legs}
    lost = [nm for nm in legs if before[nm] and not now[nm]]
    a.arm("R11", ndr is not None and not lost,
          "leg presence on the newest dated row %s vs the previous dated row %s: now %s, before %s; absent now but present before %s (Branch B for CN-p-1)" % (
              dates[ndr] if ndr is not None else None, dates[prev] if prev is not None else None, now, before, lost))
    return a.done()


# ---------------------------------------------------------------- fixture + selftest
def build_fixture(served, out, root=None):
    root = root or subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    for sub in ("", "data/mdpf/scripts/silver", "data/mdpf/scripts/gold"):
        sys.path.insert(0, os.path.join(root, sub) if sub else root)
    import boto3
    import mdpf_gold_consolidator as c
    arts = {s: json.load(open(os.path.join(served, "%s__aggregate-aua-timeseries.json" % s), encoding="utf-8")) for s in SCOPES}
    legs, part = c.load_smartx_sma_legs(boto3.client("s3"), "2026-10-14")
    new = c.apply_global_trend_groups(arts, legs, part)
    os.makedirs(out, exist_ok=True)
    for s in SCOPES:
        shaped = c._shape_timeseries(new[s], s, None, None)
        json.dump(shaped, open(os.path.join(out, "%s__aggregate-aua-timeseries.json" % s), "w"), sort_keys=True)
        json.dump(arts[s], open(os.path.join(out, "%s__aggregate-aua-timeseries.prior.json" % s), "w"), sort_keys=True)
        cv = json.load(open(os.path.join(served, "%s__category-views.json" % s), encoding="utf-8"))
        node = walk_members(cv)
        node["members"] = [m for m in node["members"] if m.get("member_id") != "muni"]
        json.dump(cv, open(os.path.join(out, "%s__category-views.json" % s), "w"), sort_keys=True)
    return out


def selftest(served):
    import shutil
    import tempfile
    ok_all = True
    print("-- served (pre-fire) must report ABSENT")
    served_data, _ = load_dir(served)
    rc = absent_mode(served_data)
    ok_all &= (rc == 0)
    tmp = tempfile.mkdtemp(prefix="r9tg_")
    fx = build_fixture(served, os.path.join(tmp, "fx"))
    print("-- fixture (served + merged CN-p-1 code) must PASS")
    d, _ = load_dir(fx)
    man = {"run": {"code": {"commit": "PIN"}}, "errors": {}}
    rc = read_mode(d, man, pin="PIN")
    ok_all &= (rc == 0)
    plants = {
        "oracle-off": lambda x: x["global"]["ts"][KEYS[0]].__setitem__(-1, x["global"]["ts"][KEYS[0]][-1] + 5e6),
        "identity-off": lambda x: x["global"]["ts"][KEYS[1]].__setitem__(300, (x["global"]["ts"][KEYS[1]][300] or 0) + 3e5),
        "carried-wrong": lambda x: x["global"]["ts"].__setitem__(CARRIED, x["global"]["ts"][CARRIED][:-1]),
        "key-missing": lambda x: x["global"]["ts"].pop(KEYS[2]),
        "other-scope-filled": lambda x: x["inflection"]["ts"][KEYS[0]].__setitem__(5, 1.0),
        "muni-kept": lambda x: walk_members(x["49financial"]["cv"])["members"].insert(0, {"member_id": "muni"}),
        "headline-moved": lambda x: x["global"]["ts"]["opal_aggregate_aua"].__setitem__(slice(10, 40), [1.0] * 30),
        "error-manifest": None,
    }
    for name, fn in plants.items():
        d2, _ = load_dir(fx)
        m2 = {"run": {"code": {"commit": "PIN"}}, "errors": {}}
        if fn is None:
            m2["errors"] = {"global": {"error": "x"}}
        else:
            fn(d2)
        print("-- planted: %s (must be RED)" % name)
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = read_mode(d2, m2, pin="PIN")
        red = rc != 0
        print("   %s -> %s" % (name, "RED (caught)" if red else "GREEN (MISSED)"))
        ok_all &= red
    shutil.rmtree(tmp, ignore_errors=True)
    print("R9 TREND-GROUPS READBACK SELFTEST: %s" % ("OK" if ok_all else "FAILED"))
    return 0 if ok_all else 1


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    opt = {argv[i]: (argv[i + 1] if i + 1 < len(argv) else None) for i in range(2, len(argv))}
    if cmd == "read":
        if "--dir" in opt:
            data, manifest = load_dir(opt["--dir"])
        else:
            data, manifest = load_s3()
        if opt.get("--expect") == "absent":
            return absent_mode(data)
        return read_mode(data, manifest, pin=opt.get("--pin"))
    if cmd == "fixture":
        print(build_fixture(opt["--served"], opt["--out"]))
        return 0
    if cmd == "selftest":
        return selftest(opt.get("--served") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "served"))
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
