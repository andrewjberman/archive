#!/usr/bin/env python
"""MDPF_CANON round 7, cell CN-l-1 -- the Other Models dated carry (rows D1-W16-S2, D1-W16-S4).

The Global aum-metrics `Other Models` row must not serve carried dollars as current. A carried value carries its date, or it is blank:
  (a) the pool is present on the as-of date -> the value is current and the row has NO `as_of` key;
  (b) no pool on the as-of date, a pooled date within 4 calendar days -> the row carries that date's value and `as_of` = that date;
  (c) no pooled date within 4 calendar days (or never) -> the row is absent.
The rule is the fold line's alone: every other model key keeps its existing last-real-value fallback (control arm).

  python r7_cn_l_1.py unit    [--root DIR]   synthetic fixtures through build_aum_metrics (offline)
  python r7_cn_l_1.py seams   [--root DIR]   the module's existing callers still pass; the served shape and the constant
  python r7_cn_l_1.py real    [--root DIR]   the REAL served Global object and the real staged firm artifacts, with the pool withheld
                                             on the last 1, 2 and 5 dates (read-only S3 GetObject/ListObjects)

--root defaults to the repo root (git rev-parse --show-toplevel). A reference tree (ref/make_reference_tree_l1.py) is passed here.
Each arm prints `  <ARM> PASS|FAIL <detail>`; the last line is `ROUND 7 CN-L-1 <MODE>: k of n arms`; exit 0 only when k == n.
Read-only. ASCII only. Every mode terminates well inside 120 s.
"""
import copy
import datetime as dt
import importlib
import json
import os
import subprocess
import sys

CARRY_DAYS = 4
OM = "other_models"
CORE = "opal_intermediate"
BUCKET = "opal-data-assets"
SERVED_PREFIX = "portal/gold/mdpf/global/aggregate-aua-timeseries/"
BASE_ROW_KEYS = ["account_count", "aum", "model_name", "q0", "q1", "q2", "q3"]


def _root(argv):
    if "--root" in argv:
        return os.path.abspath(argv[argv.index("--root") + 1])
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, timeout=30)
    if out.returncode != 0:
        print("ERROR: git rev-parse failed: %s" % out.stderr.strip())
        sys.exit(2)
    return out.stdout.strip()


def _load(root):
    gold = os.path.join(root, "data", "mdpf", "scripts", "gold")
    if gold not in sys.path:
        sys.path.insert(0, gold)
    for name in ("dim_mdpf_aum_metrics", "dim_mdpf_aggregate_aua_timeseries"):
        sys.modules.pop(name, None)
    mod = importlib.import_module("dim_mdpf_aum_metrics")
    mod._log = lambda msg: None          # the producer's progress lines are not part of any verdict here
    return mod


class Arms:
    def __init__(self, mode):
        self.mode, self.rows = mode, []

    def check(self, arm, ok, detail):
        self.rows.append(bool(ok))
        print("  %s %s %s" % (arm, "PASS" if ok else "FAIL", detail))

    def finish(self):
        k, n = sum(self.rows), len(self.rows)
        print("ROUND 7 CN-L-1 %s: %d of %d arms" % (self.mode.upper(), k, n))
        return 0 if k == n else 1


def _row(out, name):
    for r in out["by_model"]:
        if r["model_name"] == name:
            return r
    return None


# ---------------------------------------------------------------------------------------------------- synthetic fixture
def fixture(dates, om_values, om_counts=None, core_values=None):
    """A minimal Global aggregate that build_aum_metrics accepts, with its three firm artifacts (arts_override)."""
    n = len(dates)
    m49, nm49, minf = 1000.0, 200.0, 300.0
    ent = m49 + nm49 + minf
    core = core_values if core_values is not None else [500.0] * n
    agg = {
        "dates": list(dates), "as_of_last": dates[-1], "point_class": None, "cohort_provenance": [],
        "opal_aggregate_aua": [ent] * n, "model_aua": [m49 + minf] * n, "non_model_aua": [nm49] * n,
        "account_count_total": [100] * n,
        "by_model": {
            CORE: {"cohort_class": "model", "model_value": list(core), "account_count": [10] * n},
            OM: {"cohort_class": "model", "model_value": list(om_values),
                 "account_count": list(om_counts) if om_counts is not None else [7] * n},
        },
    }
    def art(m, nm):
        return {"dates": list(dates), "model_aua": [m] * n, "non_model_aua": [nm] * n}
    arts = {"49financial": art(m49, nm49), "inflection": art(minf, 0.0), "cottonwood": art(0.0, 0.0)}
    return agg, arts


def _dates(n, end="2026-10-13"):
    e = dt.date.fromisoformat(end)
    return [(e - dt.timedelta(days=n - 1 - i)).isoformat() for i in range(n)]


def run_unit(root):
    M = _load(root)
    arms = Arms("unit")
    D = _dates(12)                       # 2026-10-02 .. 2026-10-13, every calendar day

    def build(om, **kw):
        agg, arts = fixture(D, om, **kw)
        return M.build_aum_metrics(agg, arts)

    # U1 (a) pool present today: current value, no stamp, the base key set  [control: holds at the base]
    om = [100.0 + i for i in range(12)]
    r = _row(build(om), "Other Models")
    arms.check("U1", r is not None and r["aum"] == om[-1] and sorted(r.keys()) == BASE_ROW_KEYS,
               "(a) pool today: aum=%s keys=%s" % (r and r["aum"], r and sorted(r.keys())))

    # U2 (b) no pool today, pooled yesterday: yesterday's value, stamped
    om = [100.0 + i for i in range(11)] + [None]
    r = _row(build(om), "Other Models")
    arms.check("U2", r is not None and r["aum"] == 110.0 and r.get("as_of") == D[-2],
               "(b) carried 1 day: aum=%s as_of=%s want 110.0 / %s" % (r and r["aum"], r and r.get("as_of"), D[-2]))

    # U3 (b) the boundary: 4 calendar days carries (inclusive)
    om = [100.0 + i for i in range(8)] + [None] * 4
    r = _row(build(om), "Other Models")
    arms.check("U3", r is not None and r["aum"] == 107.0 and r.get("as_of") == D[7],
               "(b) carried 4 days: aum=%s as_of=%s want 107.0 / %s" % (r and r["aum"], r and r.get("as_of"), D[7]))

    # U4 (c) 5 calendar days: blank (the row is absent, never a zero)
    om = [100.0 + i for i in range(7)] + [None] * 5
    r = _row(build(om), "Other Models")
    arms.check("U4", r is None, "(c) 5 days since the last pool: row absent (found %s)" % (r and r["aum"]))

    # U5 (c) never pooled: absent
    r = _row(build([None] * 12), "Other Models")
    arms.check("U5", r is None, "(c) never pooled: row absent (found %s)" % (r and r["aum"]))

    # U6 control: a core model None on the as-of keeps the existing last-real-value fallback, with NO stamp
    agg_core = [500.0 + i for i in range(11)] + [None]
    r = _row(build([100.0 + i for i in range(12)], core_values=agg_core), "Intermediate")
    arms.check("U6", r is not None and r["aum"] == 510.0 and "as_of" not in r,
               "control: core model fallback unchanged, aum=%s keys=%s" % (r and r["aum"], r and sorted(r.keys())))

    # U7 the carried row's count is the count AT the carried date, never the frontier of a later date
    om = [100.0 + i for i in range(11)] + [None]
    cnt = [7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 9, 50]      # the as-of itself holds a count (50) while its value is None
    r = _row(build(om, om_counts=cnt), "Other Models")
    arms.check("U7", r is not None and r.get("as_of") == D[-2] and r["account_count"] == 9,
               "carried row count at its own date: %s want 9" % (r and r["account_count"]))

    # U8 the carried row keeps the same q-cell keys and the whole output stays JSON-clean
    om = [100.0 + i for i in range(11)] + [None]
    out = build(om)
    r = _row(out, "Other Models")
    try:
        json.dumps(out, allow_nan=False)
        clean = True
    except ValueError:
        clean = False
    arms.check("U8", r is not None and sorted(r.keys()) == sorted(BASE_ROW_KEYS + ["as_of"]) and clean,
               "carried row keys = base + as_of only; json clean=%s keys=%s" % (clean, r and sorted(r.keys())))
    return arms.finish()


# ---------------------------------------------------------------------------------------------------- seams
def run_seams(root):
    M = _load(root)
    arms = Arms("seams")

    def pytest(paths):
        p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"] + paths, cwd=root,
                           capture_output=True, text=True, timeout=50)
        tail = [ln for ln in (p.stdout + p.stderr).splitlines() if ln.strip()][-1:] or ["(no output)"]
        return p.returncode == 0, tail[0]

    ok, tail = pytest(["data/mdpf/tests/stratid/test_stratid_global_fold.py", "data/mdpf/tests/taxsma/test_taxsma_served_fold.py"])
    arms.check("S1", ok, "the stratid and taxsma callers of build_aum_metrics pass: %s" % tail)
    ok, tail = pytest(["data/mdpf/scripts/gold/tests/test_canplat_p1_1.py"])
    arms.check("S2", ok, "the canplat caller of build_aum_metrics passes: %s" % tail)

    # S3 the window is one named constant, 4, so the rule is legible and testable (absent at the base)
    got = getattr(M, "OTHER_MODELS_CARRY_MAX_DAYS", None)
    arms.check("S3", got == CARRY_DAYS, "OTHER_MODELS_CARRY_MAX_DAYS=%r want %d" % (got, CARRY_DAYS))

    # S4 the stamp is an ISO date that is one of the object's own dates
    D = _dates(12)
    agg, arts = fixture(D, [100.0 + i for i in range(11)] + [None])
    r = _row(M.build_aum_metrics(agg, arts), "Other Models")
    stamp = r.get("as_of") if r else None
    try:
        dt.date.fromisoformat(stamp)
        iso = True
    except (TypeError, ValueError):
        iso = False
    arms.check("S4", iso and stamp in D, "as_of=%r is ISO and one of the object's dates" % stamp)

    # S5 top-level and total key sets are identical on a carried day and on a current day (the readback's R3 arm)
    a1, r1 = fixture(D, [100.0 + i for i in range(12)])
    a2, r2 = fixture(D, [100.0 + i for i in range(11)] + [None])
    o1, o2 = M.build_aum_metrics(a1, r1), M.build_aum_metrics(a2, r2)
    same = sorted(o1.keys()) == sorted(o2.keys()) and sorted(o1["total"].keys()) == sorted(o2["total"].keys()) \
        and sorted(o1["meta"].keys()) == sorted(o2["meta"].keys())
    arms.check("S5", same, "top-level, total and meta key sets equal between a current day and a carried day")
    return arms.finish()


# ---------------------------------------------------------------------------------------------------- real
def _s3():
    import boto3
    from botocore.config import Config
    return boto3.client("s3", region_name="us-east-1", config=Config(read_timeout=30, connect_timeout=10,
                                                                      retries={"max_attempts": 2}))


def _expect(dates, vals, asof_idx):
    """The spec rule, stated independently of the producer: (value, date) or None."""
    asof = dt.date.fromisoformat(dates[asof_idx])
    for j in range(asof_idx, -1, -1):
        if vals[j] is not None:
            d = dt.date.fromisoformat(dates[j])
            if j == asof_idx:
                return (vals[j], None)
            return (vals[j], dates[j]) if (asof - d).days <= CARRY_DAYS else None
    return None


def run_real(root):
    M = _load(root)
    arms = Arms("real")
    s3 = _s3()
    ks = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=SERVED_PREFIX).get("Contents", [])
                if o["Key"].endswith(".json"))
    agg = json.loads(s3.get_object(Bucket=BUCKET, Key=ks[-1])["Body"].read())
    arts = {f: json.loads(s3.get_object(Bucket=BUCKET, Key="gold/mdpf_revamp/%s/aggregate_aua_timeseries.json" % f)["Body"].read())
            for f in ("49financial", "inflection", "cottonwood")}
    d = agg["dates"]
    gi = d.index(agg["as_of_last"])
    om0 = agg["by_model"][OM]["model_value"]
    print("  instrument: served key %s, as_of_last %s, %d dates; %d of %d dates carry an %s value" %
          (ks[-1], d[gi], len(d), sum(v is not None for v in om0), len(om0), OM))

    def variant(k):
        a = copy.deepcopy(agg)
        mv = a["by_model"][OM]["model_value"]
        ct = a["by_model"][OM].get("account_count") or []
        for i in range(gi - k + 1, gi + 1):
            mv[i] = None
            if i < len(ct):
                ct[i] = None
        return a, mv

    base_out = M.build_aum_metrics(copy.deepcopy(agg), copy.deepcopy(arts))
    base_core = {r["model_name"]: r for r in base_out["by_model"] if r["model_name"] != "Other Models"}

    # R1 the real object as served: the pool is present on the as-of -> current, no stamp  [control: holds at the base]
    r = _row(base_out, "Other Models")
    want = om0[gi]
    arms.check("R1", (want is None and r is None) or (r is not None and r["aum"] == round(float(want), 2) and "as_of" not in r),
               "as served: Other Models aum=%s stamp=%s want %s" % (r and r["aum"], r and r.get("as_of"), want))

    outs = {}
    for tag, k in (("R2", 1), ("R3", 2), ("R4", 5)):
        a, mv = variant(k)
        out = M.build_aum_metrics(a, copy.deepcopy(arts))
        outs[tag] = out
        r = _row(out, "Other Models")
        exp = _expect(d, mv, gi)
        if exp is None:
            ok = r is None
            detail = "pool withheld on the last %d date(s): expect blank; row %s" % (k, "absent" if r is None else r["aum"])
        else:
            ok = r is not None and r["aum"] == round(float(exp[0]), 2) and r.get("as_of") == exp[1]
            detail = "pool withheld on the last %d date(s): expect %.2f stamp %s; got aum=%s stamp=%s" % (
                k, exp[0], exp[1], r and r["aum"], r and r.get("as_of"))
        arms.check(tag, ok, detail)

    # R5 the five core rows and every other row are identical in all three withheld builds  [control: holds at the base]
    same = True
    for tag, out in outs.items():
        for r in out["by_model"]:
            if r["model_name"] == "Other Models":
                continue
            if base_core.get(r["model_name"]) != r:
                same = False
    arms.check("R5", same, "every non-fold row equals the as-served build in all three withheld builds (%d rows)" % len(base_core))

    # R6 the headline is untouched by the carry  [control: holds at the base]
    arms.check("R6", all(o["total"] == base_out["total"] for o in outs.values()),
               "total{} equal across the as-served and the three withheld builds")
    return arms.finish()


def main(argv):
    if len(argv) < 2 or argv[1] not in ("unit", "seams", "real"):
        print(__doc__)
        return 2
    root = _root(argv)
    return {"unit": run_unit, "seams": run_seams, "real": run_real}[argv[1]](root)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
