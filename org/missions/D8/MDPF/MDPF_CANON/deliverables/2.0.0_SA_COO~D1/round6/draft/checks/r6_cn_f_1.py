#!/usr/bin/env python3
"""MDPF_CANON round 6, cell CN-f-1 -- the Global min-firms fold (fe9b, RULED A; ADDENDA 1-4). Issuer checks, offline.

Two subcommands, each prints one `  <ARM> PASS|FAIL <detail>` line per arm and then `ROUND 6 <NAME>: k of n arms`;
exit 0 only when every arm passes. ASCII only. No network. Terminates well under 120 s.

  contract   10 arms on SYNTHETIC arts (6 dates, 3 firm scopes, 1 SMA-class line): the fold unit contract of
             apply_global_min_firms_fold / guard_global_min_firms_fold in data/mdpf/scripts/gold/mdpf_gold_consolidator.py
             (fold set computed from the objects; sum rule; absent is not zero; per-date suppression incl. the fold
             line; the DIFFERENTIAL identity; every emitted line held by >= 2 firms; nothing else moves; fail closed;
             isolation; null lines printed with dollars; the worker's own test file passes).
  seams      6 arms, static (ast) over the files the cell edits: build_all wiring, the distribution's fold_keys/fold_emit,
             MODEL_ORDER / SERVED_MODEL_NAME, the fold line's crosswalk row in both homes (id-less, not served, in no leg tuple), and the
             three firm scopes riding through the guard as the SAME objects.

Root = $R6_ROOT, else `git rev-parse --show-toplevel`. The issuer's dry-run points R6_ROOT at a reference tree.

The function contract the arms read (the order's section 1 states it; a worker never needs this file):
  apply_global_min_firms_fold(arts, firm_scopes=FIRM_SCOPES, min_firms=2) -> (arts_out, report)
  guard_global_min_firms_fold(arts, isolated) -> (arts_out, report_or_None)
  report keys: applied, as_of, fold_keys, null_lines{key:{last_value, last_value_date}}, suppressed_dates,
               other_models_emitted_dates, identity_dates_checked, identity_gap_dates, first_per_model_date
  refusal: SystemExit whose message starts `GLOBAL MIN-FIRMS FOLD REFUSED:` (dates and differences only, no level).
"""
from __future__ import annotations

import ast
import copy
import importlib
import os
import subprocess
import sys

FOLD_KEY = "other_models"
REFUSE_PREFIX = "GLOBAL MIN-FIRMS FOLD REFUSED:"
TEST_FILE = os.path.join("data", "mdpf", "tests", "canon", "test_global_min_firms_fold.py")


def _root() -> str:
    r = os.environ.get("R6_ROOT")
    if r:
        return r
    return subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()


def _load_consolidator(root: str):
    for sub in ("scripts/silver", "scripts/gold"):
        p = os.path.normpath(os.path.join(root, "data", "mdpf", sub))
        if p not in sys.path:
            sys.path.insert(0, p)
    if root not in sys.path:
        sys.path.insert(0, root)
    return importlib.import_module("mdpf_gold_consolidator")


# ---------------------------------------------------------------- synthetic arts
D = ["2026-10-01", "2026-10-02", "2026-10-05", "2026-10-06", "2026-10-07", "2026-10-08"]
N = None


def _firm(dates, bm):
    return {"dates": list(dates), "by_model": {k: {"model_value": list(v[0]), "account_count": list(v[1]),
                                                    "cohort_class": v[2]} for k, v in bm.items()}}


def _synthetic(cottonwood_blend: bool = False) -> dict:
    """The six-date world. Values by firm (49F, INF, COT):
      opal_intermediate   49F 100 all; INF 0.0,0.0,40,40,40,40; COT N,N,N,N,30,30   -> held by 1 firm on d0,d1; by 2+ from d2
      opal_blend_5050_st_int  INF N,N,N,20,20,20                                     -> one firm (inflection) from d3
      opal_fixed_income   COT N,N,N,N,N,7                                            -> one firm (cottonwood) at the as-of only
      opal_income         COT N,N,4,N,N,N                                            -> NULL line: no value at the as-of
      opal_div_sma        49F 10 all (SMA class: outside model_aua, never folded)
    Global lines are the sums of the legs; model_aua is the sum of the model-class lines, +0.01 on d3 (a pre-existing
    rounding gap the DIFFERENTIAL identity must tolerate)."""
    f49 = _firm(D, {
        "opal_intermediate": ([100.0] * 6, [10, 10, 12, 12, 15, 15], "model"),
        "opal_div_sma": ([10.0] * 6, [3] * 6, "sma"),
    })
    inf = _firm(D, {
        "opal_intermediate": ([0.0, 0.0, 40.0, 40.0, 40.0, 40.0], [N, N, N, N, N, N], "model"),
        "opal_blend_5050_st_int": ([N, N, N, 20.0, 20.0, 20.0], [N, N, N, 2, 2, 2], "model"),
    })
    cot = _firm(D, {
        "opal_intermediate": ([N, N, N, N, 30.0, 30.0], [N, N, N, N, 2, 2], "model"),
        "opal_fixed_income": ([N, N, N, N, N, 7.0], [N, N, N, N, N, 3], "model"),
        "opal_income": ([N, N, 4.0, N, N, N], [N, N, 1, N, N, N], "model"),
    })
    if cottonwood_blend:       # cottonwood also holds the blend at the as-of: it is a two-firm line and must be KEPT
        cot["by_model"]["opal_blend_5050_st_int"] = {"model_value": [N, N, N, N, N, 5.0],
                                                     "account_count": [N, N, N, N, N, 1], "cohort_class": "model"}
    inter = [100.0, 100.0, 140.0, 140.0, 170.0, 170.0]
    blend = [N, N, N, 20.0, 20.0, 20.0]
    fixed = [N, N, N, N, N, 7.0]
    income = [N, N, 4.0, N, N, N]
    if cottonwood_blend:
        blend = [N, N, N, 20.0, 20.0, 25.0]
        fixed = list(fixed)
    model_aua = []
    for i in range(6):
        model_aua.append(round(sum(x[i] for x in (inter, blend, fixed, income) if x[i] is not None), 2))
    model_aua[3] = round(model_aua[3] + 0.01, 2)          # the rounding gap
    g = {
        "dates": list(D),
        "model_aua": model_aua,
        "non_model_aua": [50.0] * 6,
        "tax_additive_aua": [N] * 6,
        "sma_additive_aua": [10.0] * 6,
        "opal_aggregate_aua": [round(m + 50.0 + 10.0, 2) for m in model_aua],
        "account_count_total": [20, 20, 22, 24, 30, 32],
        "point_class": ["measured"] * 6,
        "firm_id": "global",
        "by_model": {
            "opal_intermediate": {"display_name": "Intermediate", "cohort_class": "model", "model_value": inter,
                                  "account_count": [10, 10, 12, 12, 17, 17]},
            "opal_blend_5050_st_int": {"display_name": "50/50 ST/INT", "cohort_class": "model", "model_value": blend,
                                       "account_count": [N, N, N, 2, 2, 2 + (1 if cottonwood_blend else 0)]},
            "opal_fixed_income": {"display_name": "Opal Fixed Income", "cohort_class": "model", "model_value": fixed,
                                  "account_count": [N, N, N, N, N, 3]},
            "opal_income": {"display_name": "Opal Income", "cohort_class": "model", "model_value": income,
                            "account_count": [N, N, 1, N, N, N]},
            "opal_div_sma": {"display_name": "Dividend SMA", "cohort_class": "sma", "model_value": [10.0] * 6,
                             "account_count": [3] * 6, "count_as_of": "2026-10-01"},
        },
        "meta": {"basis": "synthetic", "by_model_channels": {
            "opal_intermediate": ["49financial", "cottonwood", "inflection"],
            "opal_blend_5050_st_int": ["inflection"], "opal_fixed_income": ["cottonwood"],
            "opal_income": ["cottonwood"], "opal_div_sma": ["49financial"]}},
    }
    return {"global": g, "49financial": f49, "inflection": inf, "cottonwood": cot}


# ---------------------------------------------------------------- independent recomputation (the check's own arithmetic)
def _held(arts: dict, key: str, i: int, dates: list) -> list:
    out = []
    for f in ("49financial", "inflection", "cottonwood"):
        a = arts.get(f)
        if a is None:
            continue
        e = (a.get("by_model") or {}).get(key)
        if not e:
            continue
        di = {d: j for j, d in enumerate(a["dates"])}
        j = di.get(dates[i])
        v = e["model_value"][j] if j is not None and j < len(e["model_value"]) else None
        if v is not None and v > 0:
            out.append(f)
    return out


def _model_sum(g: dict, i: int) -> float:
    s = 0.0
    for e in (g.get("by_model") or {}).values():
        if e.get("cohort_class") == "model" and e["model_value"][i] is not None:
            s += e["model_value"][i]
    return s


def _suppressed_vector(arts: dict, out_g: dict) -> list:
    """Independent S[i]: dollars of the INPUT model-class lines that left by_model and were not re-emitted in the fold line,
    computed as (input model-class sum) - (output model-class sum). Cents."""
    g = arts["global"]
    return [round(_model_sum(g, i) - _model_sum(out_g, i), 2) for i in range(len(g["dates"]))]


def _run(gc, arts):
    return gc.apply_global_min_firms_fold(arts)


# ---------------------------------------------------------------- arms
def contract(root: str) -> int:
    arms = []

    def arm(name: str, ok: bool, detail: str) -> bool:
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        arms.append(bool(ok))
        return bool(ok)

    gc = None
    try:
        gc = _load_consolidator(root)
    except Exception as exc:                                  # noqa: BLE001 -- an import failure is an arm failure
        print("  import FAIL: %s: %s" % (type(exc).__name__, str(exc)[:160]))
    fn = getattr(gc, "apply_global_min_firms_fold", None) if gc is not None else None
    gfn = getattr(gc, "guard_global_min_firms_fold", None) if gc is not None else None

    # C1
    arm("C1", fn is not None and gfn is not None,
        "apply_global_min_firms_fold and guard_global_min_firms_fold %s in mdpf_gold_consolidator"
        % ("present" if fn is not None and gfn is not None else "absent"))

    arts = _synthetic()
    before = copy.deepcopy(arts)
    out = rep = None
    err = ""
    if fn is not None:
        try:
            out, rep = _run(gc, arts)
        except BaseException as exc:                          # noqa: BLE001
            err = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    ok_run = out is not None and isinstance(rep, dict)
    og = out["global"] if ok_run else None

    # C2 fold set, sum rule, absent is not zero
    ok = False
    detail = err or "no function"
    if ok_run:
        bm = og["by_model"]
        want_fold = ["opal_blend_5050_st_int", "opal_fixed_income", "opal_income"]
        gone = all(k not in bm for k in want_fold)
        om = bm.get(FOLD_KEY) or {}
        mv, ac = om.get("model_value"), om.get("account_count")
        inter = bm.get("opal_intermediate", {}).get("model_value")
        ok = (sorted(rep.get("fold_keys") or []) == want_fold and gone
              and mv == [N, N, N, N, N, 27.0] and ac == [N, N, N, N, N, 5]
              and om.get("cohort_class") == "model" and om.get("display_name")
              and inter == [N, N, 140.0, 140.0, 170.0, 170.0])
        detail = ("fold_keys=%s removed=%s other_models.value=%s count=%s kept intermediate=%s"
                  % (rep.get("fold_keys"), gone, mv, ac, inter))
    arm("C2", ok, detail)

    # C3 per-date suppression (incl. the fold line) and the differential identity, recomputed here
    ok = False
    detail = err or "no function"
    if ok_run:
        s = _suppressed_vector(arts, og)
        want = [100.0, 100.0, 4.0, 20.0, 20.0, 0.0]
        valued = [i for i, m in enumerate(arts["global"]["model_aua"]) if m is not None]
        before_res = [round(arts["global"]["model_aua"][i] - _model_sum(arts["global"], i), 2) for i in valued]
        after_res = [round(arts["global"]["model_aua"][i] - _model_sum(og, i), 2) for i in valued]
        diff = [round(a - b, 2) for a, b in zip(after_res, before_res)]
        ok = (s == want and diff == want and rep.get("identity_gap_dates") == 0
              and rep.get("identity_dates_checked") == len(valued)
              and list(rep.get("suppressed_dates") or []) == [D[0], D[1], D[2], D[3], D[4]]
              and rep.get("other_models_emitted_dates") == 1)
        detail = ("suppressed=%s differential=%s gap_dates=%s checked=%s suppressed_dates=%d emitted=%s (pre-fold residual on d3=%.2f tolerated)"
                  % (s, diff, rep.get("identity_gap_dates"), rep.get("identity_dates_checked"),
                     len(rep.get("suppressed_dates") or []), rep.get("other_models_emitted_dates"), before_res[3]))
    arm("C3", ok, detail)

    # C4 every emitted by_model line (fold line included) is held by >= 2 firms on every date it carries a value
    ok = False
    detail = err or "no function"
    if ok_run:
        bad = []
        for k, e in og["by_model"].items():
            if e.get("cohort_class") != "model":
                continue
            for i, v in enumerate(e["model_value"]):
                if v is None:
                    continue
                if k == FOLD_KEY:
                    pooled = [pk for pk in arts["global"]["by_model"]
                              if arts["global"]["by_model"][pk]["cohort_class"] == "model" and pk not in og["by_model"]
                              and arts["global"]["by_model"][pk]["model_value"][i] is not None]
                    pooled += [pk for pk in og["by_model"] if pk != FOLD_KEY and og["by_model"][pk].get("cohort_class") == "model"
                               and og["by_model"][pk]["model_value"][i] is None
                               and arts["global"]["by_model"][pk]["model_value"][i] is not None]
                    h = set()
                    for pk in pooled:
                        h.update(_held(arts, pk, i, D))
                else:
                    h = set(_held(arts, k, i, D))
                if len(h) < 2:
                    bad.append((k, D[i]))
        ok = not bad
        detail = "every emitted model-class value held by >= 2 firms" if ok else "held by < 2 firms: %s" % bad[:3]
    arm("C4", ok, detail)

    # C5 nothing else moves; no mutation; siblings are the same objects
    ok = False
    detail = err or "no function"
    if ok_run:
        same_top = sorted(og.keys()) == sorted(arts["global"].keys())
        heads = ("dates", "model_aua", "non_model_aua", "tax_additive_aua", "sma_additive_aua", "opal_aggregate_aua",
                 "account_count_total", "point_class", "firm_id")
        heads_eq = all(og.get(k) == arts["global"].get(k) for k in heads)
        sma_eq = og["by_model"].get("opal_div_sma") == arts["global"]["by_model"]["opal_div_sma"]
        unmut = arts == before
        sib = all(out.get(k) is arts[k] for k in ("49financial", "inflection", "cottonwood"))
        meta_ok = {k: v for k, v in og["meta"].items() if k not in ("by_model_channels", "by_model_fold")} == \
                  {k: v for k, v in arts["global"]["meta"].items() if k != "by_model_channels"}
        fold_meta = og["meta"].get("by_model_fold") or {}
        stmt = str(fold_meta.get("statement", ""))
        in_band = (str(fold_meta.get("per_model_detail_begins", ""))[:10] == D[2] and D[2] in stmt and len(stmt) > 20
                   and fold_meta.get("min_firms") == 2)
        ok = same_top and heads_eq and sma_eq and unmut and sib and meta_ok and in_band
        detail = ("top-level keys equal=%s headline arrays equal=%s SMA line equal=%s input unmutated=%s siblings same objects=%s "
                  "meta otherwise equal=%s in-band statement carries first per-model date=%s"
                  % (same_top, heads_eq, sma_eq, unmut, sib, meta_ok, in_band))
    arm("C5", ok, detail)

    # C6 the fold set is computed from the objects, never a static list
    ok = False
    detail = err or "no function"
    if fn is not None:
        try:
            a2 = _synthetic(cottonwood_blend=True)
            o2, r2 = _run(gc, a2)
            ok = ("opal_blend_5050_st_int" not in (r2.get("fold_keys") or [])
                  and "opal_blend_5050_st_int" in o2["global"]["by_model"]
                  and o2["global"]["by_model"]["opal_blend_5050_st_int"]["model_value"][5] == 25.0
                  and "opal_fixed_income" in (r2.get("fold_keys") or []))
            detail = "blend held by 2 firms at the as-of -> kept with its value; fold_keys=%s" % r2.get("fold_keys")
        except BaseException as exc:                          # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    arm("C6", ok, detail)

    # C7 fail closed: a malformed array and an unclassified line are refused, naming dates/keys only
    ok = False
    detail = "no function"
    if fn is not None:
        names = []
        try:
            bad1 = _synthetic()
            bad1["global"]["by_model"]["opal_fixed_income"]["model_value"] = [N, N, N]        # short array
            try:
                _run(gc, bad1)
                names.append("short array ACCEPTED")
            except SystemExit as exc:
                names.append("short array refused" if str(exc).startswith(REFUSE_PREFIX) else "wrong prefix: %s" % str(exc)[:60])
            bad2 = _synthetic()
            del bad2["global"]["by_model"]["opal_income"]["cohort_class"]                     # unclassified line
            try:
                _run(gc, bad2)
                names.append("unclassified ACCEPTED")
            except SystemExit as exc:
                names.append("unclassified refused" if str(exc).startswith(REFUSE_PREFIX) else "wrong prefix: %s" % str(exc)[:60])
        except BaseException as exc:                          # noqa: BLE001
            names.append("%s: %s" % (type(exc).__name__, str(exc)[:100]))
        ok = names == ["short array refused", "unclassified refused"]
        detail = "; ".join(names)
    arm("C7", ok, detail)

    # C8 isolation: a refusal refuses Global alone, through the build's isolation, siblings the same objects
    ok = False
    detail = "no function"
    if gfn is not None:
        try:
            errors = {}

            def _isolated(scope, f):
                try:
                    return f()
                except BaseException as e:                    # noqa: BLE001 -- mirrors build_all._isolated
                    if isinstance(e, KeyboardInterrupt):
                        raise
                    errors[scope] = str(e)
                    return None

            control = _synthetic()
            planted = _synthetic()
            planted["global"]["by_model"]["opal_fixed_income"]["model_value"] = [N, N, N]
            oc, rc = gfn(control, _isolated)
            op, rp = gfn(planted, _isolated)
            sib = all(op.get(k) is planted[k] for k in ("49financial", "inflection", "cottonwood"))
            ok = (oc.get("global") is not control["global"] and isinstance(rc, dict) and op.get("global") is None
                  and rp is None and sib and "global" in errors and errors["global"].startswith(REFUSE_PREFIX))
            detail = ("control folded=%s; planted -> global %s, report %s, firm scopes same objects=%s, error recorded=%s"
                      % (oc.get("global") is not control["global"], "None" if op.get("global") is None else "kept",
                         rp, sib, "global" in errors))
        except BaseException as exc:                          # noqa: BLE001
            detail = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    arm("C8", ok, detail)

    # C9 the null lines are reported WITH their dollars (ADDENDUM 1/3): last non-null value and its date
    ok = False
    detail = err or "no function"
    if ok_run:
        nl = rep.get("null_lines") or {}
        e = nl.get("opal_income") or {}
        ok = (sorted(nl) == ["opal_income"] and e.get("last_value") == 4.0 and str(e.get("last_value_date")) == D[2])
        detail = "null_lines=%s" % nl
    arm("C9", ok, detail)

    # C10 the worker's own test file exists and passes (>= 6 tests)
    path = os.path.join(root, TEST_FILE)
    ok = False
    detail = "%s absent" % TEST_FILE
    if os.path.isfile(path):
        try:
            p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider", path],
                               capture_output=True, text=True, timeout=100, cwd=root)
            tail = (p.stdout.strip().splitlines() or [""])[-1]
            import re
            m = re.search(r"(\d+) passed", tail)
            n = int(m.group(1)) if m else 0
            ok = p.returncode == 0 and n >= 6 and "failed" not in tail and "error" not in tail.lower()
            detail = "pytest rc=%d: %s" % (p.returncode, tail[:100])
        except subprocess.TimeoutExpired:
            detail = "pytest timed out at 100 s"
    arm("C10", ok, detail)

    k = sum(1 for a in arms if a)
    print("ROUND 6 CONTRACT: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) and len(arms) == 10 else 1


# ---------------------------------------------------------------- static arms
def _parse(root: str, rel: str):
    p = os.path.join(root, *rel.split("/"))
    return ast.parse(open(p, encoding="utf-8").read()), p


def _find_func(tree, name):
    for n in ast.walk(tree):
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return n
    return None


def _calls(node, attr_or_name):
    out = []
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            f = n.func
            nm = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)
            if nm == attr_or_name:
                out.append(n)
    return out


def seams(root: str) -> int:
    arms = []

    def arm(name: str, ok: bool, detail: str) -> bool:
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        arms.append(bool(ok))
        return bool(ok)

    gold = "data/mdpf/scripts/gold/"
    # S1 build_all: the guard call sits after guard_global_served_identity and before the first global dim build
    ok, detail = False, ""
    try:
        tree, _ = _parse(root, gold + "mdpf_gold_consolidator.py")
        ba = _find_func(tree, "build_all")
        gf = _calls(ba, "guard_global_min_firms_fold") if ba is not None else []
        gi = _calls(ba, "guard_global_served_identity") if ba is not None else []
        am = _calls(ba, "build_aum_metrics") if ba is not None else []
        if gf and gi and am:
            l_fold, l_ident, l_dim = gf[0].lineno, gi[0].lineno, min(c.lineno for c in am)
            unpack = False
            for st in ast.walk(ba):
                if isinstance(st, ast.Assign) and st.value is gf[0] and isinstance(st.targets[0], ast.Tuple):
                    unpack = True
            ok = l_ident < l_fold < l_dim and unpack
            detail = "identity guard @%d, fold guard @%d (tuple-unpacked=%s), first global aum-metrics build @%d" % (l_ident, l_fold, unpack, l_dim)
        else:
            detail = "build_all %s a call to guard_global_min_firms_fold" % ("lacks" if ba is not None else "absent: no")
    except Exception as exc:                                  # noqa: BLE001
        detail = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    arm("S1", ok, detail)

    # S2 build_all passes fold_keys= and fold_emit= to the global distribution build
    ok, detail = False, ""
    try:
        tree, _ = _parse(root, gold + "mdpf_gold_consolidator.py")
        ba = _find_func(tree, "build_all")
        hit = None
        for c in _calls(ba, "build_firm_distribution"):
            if c.args and isinstance(c.args[0], ast.Constant) and c.args[0].value == "global":
                hit = c
        kws = sorted(k.arg for k in hit.keywords) if hit is not None else []
        ok = hit is not None and "fold_keys" in kws and "fold_emit" in kws
        detail = "global build_firm_distribution keywords=%s" % kws if hit is not None else "no global build_firm_distribution call"
    except Exception as exc:                                  # noqa: BLE001
        detail = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    arm("S2", ok, detail)

    # S3 build_firm_distribution declares fold_keys=None and fold_emit=True (every other caller unchanged)
    ok, detail = False, ""
    try:
        tree, _ = _parse(root, gold + "dim_mdpf_account_distribution.py")
        fd = _find_func(tree, "build_firm_distribution")
        names = [a.arg for a in fd.args.args]
        defaults = [ast.literal_eval(d) if isinstance(d, ast.Constant) else "?" for d in fd.args.defaults]
        dmap = dict(zip(names[len(names) - len(defaults):], defaults))
        ok = dmap.get("fold_keys", "absent") is None and dmap.get("fold_emit", "absent") is True
        detail = "params=%s defaults=%s" % (names, dmap)
    except Exception as exc:                                  # noqa: BLE001
        detail = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    arm("S3", ok, detail)

    # S4 aum-metrics names the fold line
    ok, detail = False, ""
    try:
        tree, _ = _parse(root, gold + "dim_mdpf_aum_metrics.py")
        mo = sn = False
        for n in tree.body:
            if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name):
                if n.targets[0].id == "MODEL_ORDER" and isinstance(n.value, (ast.List, ast.Tuple)):
                    mo = any(isinstance(e, ast.Constant) and e.value == FOLD_KEY for e in n.value.elts)
                if n.targets[0].id == "SERVED_MODEL_NAME" and isinstance(n.value, ast.Dict):
                    sn = any(isinstance(k, ast.Constant) and k.value == FOLD_KEY for k in n.value.keys)
        ok = mo and sn
        detail = "MODEL_ORDER has %s=%s; SERVED_MODEL_NAME has it=%s" % (FOLD_KEY, mo, sn)
    except Exception as exc:                                  # noqa: BLE001
        detail = "%s: %s" % (type(exc).__name__, str(exc)[:120])
    arm("S4", ok, detail)

    # S5 the fold line is registered through the crosswalk, in both homes, and named by no leg-composed tuple
    ok, detail = False, ""
    try:
        for sub in ("scripts/silver", "scripts/gold"):
            p = os.path.normpath(os.path.join(root, "data", "mdpf", sub))
            if p not in sys.path:
                sys.path.insert(0, p)
        if root not in sys.path:
            sys.path.insert(0, root)
        reg = importlib.import_module("mdpf_category_registry")
        spine = importlib.import_module("dim_mdpf_aggregate_aua_timeseries")
        # the fold line is a CROSSWALK row: the registry derives its model members from the crosswalk and refuses any other
        # model-class member at import. Id-less and not served, so in no SERVED/CORE/BLEND tuple; NOT in GLOBAL_MODEL_KEYS
        # (that tuple names leg-composed keys; the fold line has no leg); GLOBAL_ACCOUNT_DIST_DISPLAY names it in BOTH homes.
        xw = importlib.import_module("mdpf_revamp_model_crosswalk")
        m = reg.resolve_any(FOLD_KEY)
        e = xw._KEY_TO_ENTRY.get(FOLD_KEY)
        shape = (e is not None and e.model_id is None and e.cohort_class == "model" and e.served is False
                 and e.eclipse_id is None and e.orion_id is None)
        tuples = [FOLD_KEY in tuple(t) for t in (xw.SERVED_MODEL_KEYS, xw.CORE_MODEL_KEYS, xw.BLEND_MODEL_KEYS,
                                                 spine.GLOBAL_MODEL_KEYS)]
        home2 = os.path.join(root, "infra", "aws", "lambda", "opal-assets", "opal-assets-daily-emitter",
                             "mdpf_revamp_model_crosswalk.py")
        txt2 = open(home2, encoding="utf-8").read() if os.path.isfile(home2) else ""
        both = ('"%s"' % FOLD_KEY in txt2) and (FOLD_KEY in xw.GLOBAL_ACCOUNT_DIST_DISPLAY)
        ok = shape and not any(tuples) and both and m.view_path == "Models > Custom" and m.asset_category == "models"
        detail = ("crosswalk row id-less/model/not-served=%s; in SERVED/CORE/BLEND/GLOBAL_MODEL_KEYS=%s; display row in both homes=%s; "
                  "registry view_path=%s" % (shape, tuples, both, m.view_path))
    except BaseException as exc:                              # noqa: BLE001
        detail = "%s: %s" % (type(exc).__name__, str(exc)[:140])
    arm("S5", ok, detail)

    # S6 the three firm scopes ride through the guard as the SAME objects and the global top-level key set is unchanged
    ok, detail = False, "no function"
    try:
        gc = _load_consolidator(root)
        gfn = getattr(gc, "guard_global_min_firms_fold", None)
        if gfn is not None:
            arts = _synthetic()
            keys_before = sorted(arts["global"].keys())
            out, rep = gfn(arts, lambda scope, f: f())
            ok = (all(out[k] is arts[k] for k in ("49financial", "inflection", "cottonwood"))
                  and sorted(out["global"].keys()) == keys_before and isinstance(rep, dict))
            detail = "firm scopes same objects=%s; global key set equal=%s" % (
                all(out[k] is arts[k] for k in ("49financial", "inflection", "cottonwood")),
                sorted(out["global"].keys()) == keys_before)
    except BaseException as exc:                              # noqa: BLE001
        detail = "%s: %s" % (type(exc).__name__, str(exc)[:140])
    arm("S6", ok, detail)

    k = sum(1 for a in arms if a)
    print("ROUND 6 SEAMS: %d of %d arms" % (k, len(arms)))
    return 0 if k == len(arms) and len(arms) == 6 else 1


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("contract", "seams"):
        print("usage: r6_cn_f_1.py contract|seams")
        return 2
    root = _root()
    return contract(root) if sys.argv[1] == "contract" else seams(root)


if __name__ == "__main__":
    sys.exit(main())
