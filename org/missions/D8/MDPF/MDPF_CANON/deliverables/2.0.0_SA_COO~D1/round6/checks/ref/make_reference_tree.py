#!/usr/bin/env python3
"""Build a REFERENCE TREE for the CN-f-1 issuer checks (the dry-run that proves the arms CAN pass).

  python make_reference_tree.py <dest-dir>

Copies, read-only from the repo at the current checkout, data/mdpf/scripts, lib/ and the second home of the model crosswalk
into <dest-dir>, applies the cell's change as the ISSUER'S REFERENCE (never a worker's code, never committed to the repo),
and drops a small test file. Then:   R6_ROOT=<dest-dir> python r6_cn_f_1.py contract|seams ; ... r6_cn_f_1_comparator.py

Every patch asserts it applied exactly once; a drift in a target file fails loud instead of silently skipping.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys

REF_FUNCS = '''
GLOBAL_FOLD_KEY = "other_models"


def _fold_refuse(msg: str) -> None:
    raise SystemExit("GLOBAL MIN-FIRMS FOLD REFUSED: " + msg)


def apply_global_min_firms_fold(arts: dict, firm_scopes=FIRM_SCOPES, min_firms: int = 2):
    """CN-f-1 REFERENCE (issuer dry-run). Per-date min-firms fold of the model-class global lines. Returns (arts_out, report)."""
    g = arts.get("global")
    if g is None or not g.get("dates"):
        return arts, {"applied": False}
    dates = list(g["dates"])
    n = len(dates)
    bm = g.get("by_model") or {}
    model_keys = []
    for k, e in bm.items():
        cc = (e or {}).get("cohort_class")
        if cc not in ("model", "sma"):
            _fold_refuse("by_model line %r carries no usable cohort_class" % k)
        for fld in ("model_value", "account_count"):
            arr = e.get(fld)
            if not isinstance(arr, list) or len(arr) != n:
                _fold_refuse("by_model line %r %s has %s element(s) over %d date(s)"
                             % (k, fld, len(arr) if isinstance(arr, list) else "no", n))
        if cc == "model":
            model_keys.append(k)
    pos = {}
    for f in firm_scopes:
        a = arts.get(f)
        if a is not None:
            pos[f] = {d: j for j, d in enumerate(a.get("dates") or [])}

    def held(k, i):
        out = set()
        for f, ix in pos.items():
            e = (arts[f].get("by_model") or {}).get(k)
            if not e:
                continue
            j = ix.get(dates[i])
            arr = e.get("model_value") or []
            v = arr[j] if j is not None and j < len(arr) else None
            if v is not None and v > 0:
                out.add(f)
        return out

    H = {k: [held(k, i) for i in range(n)] for k in model_keys}
    fold_keys = sorted(k for k in model_keys if len(H[k][n - 1]) < min_firms)
    fk = set(fold_keys)
    pool_v = [None] * n
    pool_c = [None] * n
    pool_h = [set() for _ in range(n)]
    new_bm = {}
    for k, e in bm.items():
        if k not in H:
            new_bm[k] = e
            continue
        v, c = list(e["model_value"]), list(e["account_count"])
        ov, oc = [None] * n, [None] * n
        for i in range(n):
            if k in fk or len(H[k][i]) < min_firms:
                if v[i] is not None:
                    pool_v[i] = (pool_v[i] or 0.0) + v[i]
                    pool_h[i] |= H[k][i]
                if c[i] is not None:
                    pool_c[i] = (pool_c[i] or 0) + c[i]
            else:
                ov[i], oc[i] = v[i], c[i]
        if k in fk:
            continue
        ne = dict(e)
        ne["model_value"], ne["account_count"] = ov, oc
        new_bm[k] = ne
    suppressed = [0.0] * n
    supp_dates, emitted_dates = [], []
    om_v, om_c = [None] * n, [None] * n
    for i in range(n):
        if pool_v[i] is None and pool_c[i] is None:
            continue
        if len(pool_h[i]) >= min_firms:
            om_v[i] = None if pool_v[i] is None else round(pool_v[i], 2)
            om_c[i] = pool_c[i]
            emitted_dates.append(dates[i])
        elif pool_v[i] is not None:
            suppressed[i] = pool_v[i]
            supp_dates.append(dates[i])
    chans = set()
    if emitted_dates:
        new_bm[GLOBAL_FOLD_KEY] = {"display_name": "Other Models", "cohort_class": "model",
                                   "model_value": om_v, "account_count": om_c}
        for k in fk:
            chans.update(((g.get("meta") or {}).get("by_model_channels") or {}).get(k) or [])
    if list(bm) == sorted(bm):
        new_bm = dict(sorted(new_bm.items()))
    # the differential identity, to the cent, on every valued date (a pre-existing rounding gap is carried, not refused)
    valued = [i for i in range(n) if g.get("model_aua") and g["model_aua"][i] is not None]
    bad = []
    for i in valued:
        before = sum(bm[k]["model_value"][i] for k in model_keys if bm[k]["model_value"][i] is not None)
        after = sum(e["model_value"][i] for e in new_bm.values()
                    if e.get("cohort_class") == "model" and e["model_value"][i] is not None)
        if round(before - after, 2) != round(suppressed[i], 2):
            bad.append((dates[i], round(before - after - suppressed[i], 2)))
    if bad:
        _fold_refuse("%d date(s) where the gap to model_aua moved by more than the suppressed amount; first (date, difference to the cent): %s"
                     % (len(bad), ", ".join("(%s, %.2f)" % x for x in bad[:5])))
    first = None
    for i in range(n):
        if any(new_bm[k]["model_value"][i] is not None for k in new_bm
               if k != GLOBAL_FOLD_KEY and new_bm[k].get("cohort_class") == "model"):
            first = dates[i]
            break
    if first is None and emitted_dates:
        first = emitted_dates[0]
    meta = dict(g.get("meta") or {})
    if "by_model_channels" in meta:
        ch = {k: v for k, v in (meta["by_model_channels"] or {}).items() if k not in fk}
        if emitted_dates:
            ch[GLOBAL_FOLD_KEY] = sorted(chans)
        meta["by_model_channels"] = ch
    meta["by_model_fold"] = {
        "min_firms": min_firms, "per_model_detail_begins": first,
        "statement": ("Per-model lines are shown on a date only where at least %d firms hold the model; per-model detail "
                      "begins %s, the first date Global combined %d firms. Lines held by fewer firms are folded into one "
                      "Other Models line, itself shown only where at least %d firms hold it." % (min_firms, first, min_firms, min_firms))}
    nulls = {}
    for k in fold_keys:
        arr = bm[k]["model_value"]
        if arr[n - 1] is None:
            last = [(i, v) for i, v in enumerate(arr) if v is not None]
            if last:
                nulls[k] = {"last_value": last[-1][1], "last_value_date": dates[last[-1][0]]}
    flips = {}
    for k in model_keys:
        if len(H[k][n - 1]) >= min_firms:
            c = sum(1 for i in range(n - 1) if len(H[k][i]) < min_firms)
            if c:
                flips[k] = c
    g2 = dict(g)
    g2["by_model"], g2["meta"] = new_bm, meta
    out = dict(arts)
    out["global"] = g2
    report = {"applied": True, "as_of": dates[-1], "fold_keys": fold_keys, "null_lines": nulls,
              "suppressed_dates": supp_dates, "other_models_emitted_dates": len(emitted_dates),
              "other_models_emitted_as_of": bool(emitted_dates and emitted_dates[-1] == dates[-1]),
              "identity_dates_checked": len(valued), "identity_gap_dates": 0,
              "first_per_model_date": first, "flip_dates": flips}
    return out, report


def guard_global_min_firms_fold(arts: dict, isolated):
    """CN-f-1 REFERENCE: the fold runs through the build's scope isolation; a refusal refuses Global alone."""
    if arts.get("global") is None:
        return arts, None
    box = {}

    def _run():
        box["out"] = apply_global_min_firms_fold(arts)
        return True

    if isolated("global", _run) is None:
        out = dict(arts)
        out["global"] = None
        return out, None
    return box["out"]

'''

REF_TEST = '''"""CN-f-1 reference tests (issuer dry-run only)."""
import importlib.util
import os
import sys

import pytest

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, "..", "..", "scripts", "gold"), os.path.join(_HERE, "..", "..", "scripts", "silver")):
    _p = os.path.normpath(_p)
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mdpf_gold_consolidator as gc  # noqa: E402

_spec = importlib.util.spec_from_file_location("r6chk", os.environ["R6_CHECK_PATH"])
_chk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_chk)


def test_present():
    assert callable(gc.apply_global_min_firms_fold) and callable(gc.guard_global_min_firms_fold)


def test_fold_set_is_computed():
    _, rep = gc.apply_global_min_firms_fold(_chk._synthetic())
    assert rep["fold_keys"] == ["opal_blend_5050_st_int", "opal_fixed_income", "opal_income"]


def test_other_models_sum_and_absent_is_not_zero():
    out, _ = gc.apply_global_min_firms_fold(_chk._synthetic())
    om = out["global"]["by_model"]["other_models"]
    assert om["model_value"] == [None, None, None, None, None, 27.0]


def test_suppressed_dates_named():
    _, rep = gc.apply_global_min_firms_fold(_chk._synthetic())
    assert rep["suppressed_dates"][0] == "2026-10-01" and rep["identity_gap_dates"] == 0


def test_malformed_array_refused():
    a = _chk._synthetic()
    a["global"]["by_model"]["opal_income"]["model_value"] = [None]
    with pytest.raises(SystemExit) as e:
        gc.apply_global_min_firms_fold(a)
    assert str(e.value).startswith("GLOBAL MIN-FIRMS FOLD REFUSED:")


def test_guard_isolates():
    err = {}

    def iso(scope, f):
        try:
            return f()
        except SystemExit as x:
            err[scope] = str(x)
            return None
    a = _chk._synthetic()
    a["global"]["by_model"]["opal_income"]["model_value"] = [None]
    out, rep = gc.guard_global_min_firms_fold(a, iso)
    assert out["global"] is None and rep is None and "global" in err
'''


def _sub(path: str, old: str, new: str, count: int = 1) -> None:
    t = open(path, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    if nl == "\r\n":
        old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
    c = t.count(old)
    if c != count:
        raise SystemExit("PATCH DRIFT in %s: expected %d occurrence(s) of %r, found %d" % (path, count, old[:70], c))
    open(path, "w", encoding="utf-8", newline="").write(t.replace(old, new))


def main() -> int:
    dest = os.path.abspath(sys.argv[1])
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    if os.path.exists(dest):
        raise SystemExit("dest exists: " + dest)
    ign = shutil.ignore_patterns("__pycache__", "*.pyc")
    shutil.copytree(os.path.join(root, "data", "mdpf", "scripts"), os.path.join(dest, "data", "mdpf", "scripts"), ignore=ign)
    shutil.copytree(os.path.join(root, "lib"), os.path.join(dest, "lib"), ignore=ign)
    # lib/opal_naming.py reads the naming registry from <root>/infra/logic/registry at import
    shutil.copytree(os.path.join(root, "infra", "logic", "registry"),
                    os.path.join(dest, "infra", "logic", "registry"), ignore=ign)
    h2 = os.path.join("infra", "aws", "lambda", "opal-assets", "opal-assets-daily-emitter")
    os.makedirs(os.path.join(dest, h2))
    shutil.copy2(os.path.join(root, h2, "mdpf_revamp_model_crosswalk.py"), os.path.join(dest, h2, "mdpf_revamp_model_crosswalk.py"))
    g = os.path.join(dest, "data", "mdpf", "scripts", "gold")

    cons = os.path.join(g, "mdpf_gold_consolidator.py")
    _sub(cons, "def write_taxsma_category_gold(s3, scope: str,", REF_FUNCS + "\ndef write_taxsma_category_gold(s3, scope: str,")
    # the fold runs AFTER the identity guard (the trailing CN-d-1 comment of the original line rides on the new line: harmless)
    _sub(cons, "    arts = guard_global_served_identity(arts, _isolated)",
         "    arts = guard_global_served_identity(arts, _isolated)\n"
         "    arts, fold_report = guard_global_min_firms_fold(arts, _isolated)   # CN-f-1 REFERENCE;")
    _sub(cons, 'lambda: acct_dist.build_firm_distribution("global", "Global"))',
         'lambda: acct_dist.build_firm_distribution(\n'
         '                "global", "Global",\n'
         '                fold_keys=tuple((fold_report or {}).get("fold_keys") or ()),\n'
         '                fold_emit=bool((fold_report or {}).get("other_models_emitted_as_of"))))')

    _sub(os.path.join(g, "dim_mdpf_account_distribution.py"),
         "def build_firm_distribution(firm_id: str, firm_name: str) -> dict:",
         "def build_firm_distribution(firm_id: str, firm_name: str, fold_keys=None, fold_emit=True) -> dict:")
    am = os.path.join(g, "dim_mdpf_aum_metrics.py")
    _sub(am, '    "opal_blend_5050_st_int": "Opal Blend 5050 St Int",\n}',
         '    "opal_blend_5050_st_int": "Opal Blend 5050 St Int",\n    "other_models": "Other Models",\n}')
    _sub(am, '    "opal_blend_5050_st_int",\n]', '    "opal_blend_5050_st_int",\n    "other_models",\n]')
    for cw in (os.path.join(g, "mdpf_revamp_model_crosswalk.py"),
               os.path.join(dest, h2, "mdpf_revamp_model_crosswalk.py")):
        _sub(cw, '    ModelEntry("opal_muni_sleeve", None, "Opal Muni Sleeve", "model", False),\n)',
             '    ModelEntry("opal_muni_sleeve", None, "Opal Muni Sleeve", "model", False),\n'
             '    ModelEntry("other_models", None, "Other Models", "model", False),\n)')
        _sub(cw, '    "opal_muni_sleeve": "Opal Muni Sleeve",\n}',
             '    "opal_muni_sleeve": "Opal Muni Sleeve",\n    "other_models": "Other Models",\n}')
    td = os.path.join(dest, "data", "mdpf", "tests", "canon")
    os.makedirs(td)
    open(os.path.join(td, "test_global_min_firms_fold.py"), "w", encoding="utf-8").write(REF_TEST)
    print("reference tree at", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
