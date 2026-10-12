#!/usr/bin/env python3
"""MDPF_CANON round 6, cell CN-f-1 -- the never-widen comparator for the Global min-firms fold, on the REAL served objects.

Reads (READ-ONLY get/list) the newest aggregate-aua-timeseries object every scope has, builds `arts` from them exactly as the
build holds them (global + the three firm scopes), runs the cell's `apply_global_min_firms_fold` on them, and grades the
result with this file's OWN arithmetic (it never reuses the cell's report to grade the cell, except K10's report keys).

  python r6_cn_f_1_comparator.py [--date YYYY-MM-DD]       newest date present for all four scopes by default

Prints `  K<n> PASS|FAIL: <detail>` per arm and `ROUND 6 COMPARATOR: k of 11 arms`; exit 0 only on 11 of 11. Prints dates,
counts and differences; never an account id. ASCII only. Bounded: 4 list calls, 4 gets, a few seconds of arithmetic.

  K0  CONTROL (passes at base): the object read, and before the fold model_aua - sum(model-class lines) is within $0.02 on
      every valued date (the pre-existing rounding dates are counted, not hidden).
  K1  the cell's function runs on the real objects and returns (arts_out, report).
  K2  every top-level field other than by_model and meta is EQUAL, the top-level key set is equal, meta is equal except
      by_model_channels and the in-band by_model_fold.
  K3  every kept line equals its input on the dates it is held by >= 2 firms and is None elsewhere; a line the fold
      removed is gone from by_model.
  K4  other_models equals the sum of the dollars that left their lines, on every date it is emitted; where it is None
      the pool really was held by < 2 firms (no over-suppression).
  K5  the DIFFERENTIAL identity: (model_aua - sum(by_model)) after minus before == the suppressed dollars, to the cent,
      on every valued date; a pre-existing rounding gap is carried, never tripped over.
  K6  every emitted model-class line, the fold line included, is held by >= 2 firms on every date it carries a value.
  K7  no removed line's key or display name survives ANYWHERE in the folded global object.
  K8  the three firm scopes are the same objects and deep-equal to their pre-fold copies.
  K9  the SMA-class lines and `tax` are deep-equal.
  K10 every null line (no value at the as-of) is reported with its last dollars and date, equal to the object's own.
"""
from __future__ import annotations

import argparse
import copy
import importlib
import json
import os
import subprocess
import sys

BUCKET = "opal-data-assets"
PREFIX = "portal/gold/mdpf"
TYPE = "aggregate-aua-timeseries"
SCOPES = ("global", "49financial", "inflection", "cottonwood")
FIRMS = ("49financial", "inflection", "cottonwood")
FOLD_KEY = "other_models"


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


def _s3():
    import boto3
    from botocore.config import Config
    return boto3.client("s3", region_name="us-east-1", config=Config(read_timeout=30, connect_timeout=10,
                                                                      retries={"max_attempts": 2}))


def _dates(s3, scope: str) -> list:
    out, tok = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": "%s/%s/%s/" % (PREFIX, scope, TYPE)}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            n = o["Key"].rsplit("/", 1)[-1]
            if n.endswith(".json") and n[:2] == "20":
                out.append(n[:-5])
        if not r.get("IsTruncated"):
            return sorted(out)
        tok = r.get("NextContinuationToken")


def _get(s3, scope: str, date: str) -> dict:
    k = "%s/%s/%s/%s.json" % (PREFIX, scope, TYPE, date)
    return json.loads(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read())


def _held(arts, key, i, dates):
    out = []
    for f in FIRMS:
        a = arts.get(f)
        if a is None:
            continue
        e = (a.get("by_model") or {}).get(key)
        if not e:
            continue
        j = _idx(a).get(dates[i])
        arr = e.get("model_value") or []
        v = arr[j] if j is not None and j < len(arr) else None
        if v is not None and v > 0:
            out.append(f)
    return out


_IDX = {}


def _idx(a):
    k = id(a)
    if k not in _IDX:
        _IDX[k] = {d: j for j, d in enumerate(a.get("dates") or [])}
    return _IDX[k]


def _msum(g, i):
    s = 0.0
    for e in (g.get("by_model") or {}).values():
        if e.get("cohort_class") == "model":
            v = (e.get("model_value") or [None] * (i + 1))[i]
            if v is not None:
                s += v
    return s


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default="")
    args = ap.parse_args()
    root = _root()
    arms = []

    def arm(n: str, ok: bool, detail: str) -> bool:
        print("  %s %s: %s" % (n, "PASS" if ok else "FAIL", detail))
        arms.append(bool(ok))
        return bool(ok)

    s3 = _s3()
    per = {s: _dates(s3, s) for s in SCOPES}
    common = sorted(set(per["global"]).intersection(*[set(per[f]) for f in FIRMS]))
    date = args.date or (common[-1] if common else "")
    if not date or date not in common:
        print("  READ FAIL: no common date across the four scopes (counts %s)" % {s: len(v) for s, v in per.items()})
        print("ROUND 6 COMPARATOR: 0 of 11 arms")
        return 1
    arts = {s: _get(s3, s, date) for s in SCOPES}
    print("  read: %d scopes at %s (dated objects per scope %s)" % (len(arts), date, {s: len(v) for s, v in per.items()}))
    g = arts["global"]
    dates = g["dates"]
    n = len(dates)
    valued = [i for i in range(n) if g["model_aua"][i] is not None]
    before = copy.deepcopy(arts)

    # K0 control
    res = [round(g["model_aua"][i] - _msum(g, i), 2) for i in valued]
    gaps = [(dates[i], r) for i, r in zip(valued, res) if abs(r) > 0.005]
    worst = max([abs(r) for r in res] or [0.0])
    arm("K0", bool(valued) and worst <= 0.02,
        "valued dates %d of %d; pre-fold residual max %.2f; %d date(s) off by a rounding cent or two"
        % (len(valued), n, worst, len(gaps)))

    gc = _load_consolidator(root)
    fn = getattr(gc, "apply_global_min_firms_fold", None)
    out = rep = None
    err = ""
    if fn is not None:
        try:
            out, rep = fn(arts)
        except BaseException as exc:                          # noqa: BLE001
            err = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    ok_run = out is not None and isinstance(rep, dict)
    arm("K1", ok_run, "returned (arts_out, report): fold_keys=%d suppressed dates=%s" % (
        len((rep or {}).get("fold_keys") or []), len((rep or {}).get("suppressed_dates") or [])) if ok_run
        else (err or "apply_global_min_firms_fold absent from mdpf_gold_consolidator"))

    def need(name: str, f) -> None:
        if not ok_run:
            arm(name, False, "no output to grade")
            return
        try:
            ok, detail = f()
        except BaseException as exc:                          # noqa: BLE001
            ok, detail = False, "%s: %s" % (type(exc).__name__, str(exc)[:200])
        arm(name, ok, detail)

    og = out["global"] if ok_run else None
    ibm = g.get("by_model") or {}
    obm = (og or {}).get("by_model") or {}

    def k2():
        top = sorted(og.keys()) == sorted(g.keys())
        neq = [k for k in g if k not in ("by_model", "meta") and og.get(k) != g.get(k)]
        meta_i = {k: v for k, v in (g.get("meta") or {}).items() if k != "by_model_channels"}
        meta_o = {k: v for k, v in (og.get("meta") or {}).items() if k not in ("by_model_channels", "by_model_fold")}
        stmt = ((og.get("meta") or {}).get("by_model_fold") or {})
        has = bool(stmt.get("statement")) and bool(stmt.get("per_model_detail_begins"))
        return (top and not neq and meta_i == meta_o and has,
                "top-level key set equal=%s; fields differing=%s; meta otherwise equal=%s; in-band statement present=%s (begins %s)"
                % (top, neq[:4], meta_i == meta_o, has, str(stmt.get("per_model_detail_begins"))[:10]))

    def pooled_at(i):
        """Independent: model-class dollars of the INPUT that are not emitted individually at i."""
        vals = []
        for k, e in ibm.items():
            if e.get("cohort_class") != "model":
                continue
            v = e["model_value"][i]
            if v is None:
                continue
            o = obm.get(k)
            if o is None or o["model_value"][i] is None:
                vals.append((k, v))
        return vals

    def k3():
        bad, removed, kept = [], [], 0
        for k, e in ibm.items():
            if e.get("cohort_class") != "model":
                continue
            o = obm.get(k)
            if o is None:
                removed.append(k)
                continue
            kept += 1
            for i in range(n):
                iv = e["model_value"][i]
                hv = len(_held(arts, k, i, dates)) >= 2
                want = iv if (hv and iv is not None) else None
                if o["model_value"][i] != want:
                    bad.append((k, dates[i]))
                    break
        return (not bad and bool(kept), "kept lines %d, removed lines %d, lines with a wrong date %s" % (kept, len(removed), bad[:3]))

    def k4():
        om = obm.get(FOLD_KEY)
        if om is None:
            return False, "%s absent from by_model" % FOLD_KEY
        wrong, over, emitted = [], [], 0
        for i in range(n):
            pool = pooled_at(i)
            tot = round(sum(v for _, v in pool), 2) if pool else None
            ov = om["model_value"][i]
            if ov is not None:
                emitted += 1
                if tot is None or round(ov, 2) != tot:
                    wrong.append(dates[i])
            elif pool:
                h = set()
                for k, v in pool:
                    h.update(_held(arts, k, i, dates))
                if len(h) >= 2:
                    over.append(dates[i])
        return (not wrong and not over and emitted > 0,
                "emitted on %d date(s); wrong sums %s; suppressed though held by >= 2 firms %s" % (emitted, wrong[:3], over[:3]))

    def k5():
        bad, nonzero = [], 0
        om = obm.get(FOLD_KEY) or {"model_value": [None] * n}
        for i in valued:
            b = round(g["model_aua"][i] - _msum(g, i), 2)
            a = round(g["model_aua"][i] - _msum(og, i), 2)
            diff = round(a - b, 2)
            pool = pooled_at(i)
            want = round(sum(v for _, v in pool), 2) if (om["model_value"][i] is None and pool) else 0.0
            if diff != want:
                bad.append((dates[i], round(diff - want, 2)))
            if diff != 0:
                nonzero += 1
        return (not bad, "valued dates %d; dates where the gap moved %d (each equal to its suppressed dollars, no level printed); mismatches %s"
                % (len(valued), nonzero, bad[:3]))

    def k6():
        bad = []
        for k, e in obm.items():
            if e.get("cohort_class") != "model":
                continue
            for i, v in enumerate(e["model_value"]):
                if v is None:
                    continue
                if k == FOLD_KEY:
                    h = set()
                    for pk, _ in pooled_at_emitted(i):
                        h.update(_held(arts, pk, i, dates))
                else:
                    h = set(_held(arts, k, i, dates))
                if len(h) < 2:
                    bad.append((k, dates[i]))
        return (not bad, "every emitted model-class value held by >= 2 firms; violations %s" % bad[:3])

    def pooled_at_emitted(i):
        out_l = []
        for k, e in ibm.items():
            if e.get("cohort_class") != "model" or e["model_value"][i] is None:
                continue
            if k not in obm or obm[k]["model_value"][i] is None:
                out_l.append((k, e["model_value"][i]))
        return out_l

    def k7():
        removed = [k for k, e in ibm.items() if e.get("cohort_class") == "model" and k not in obm]
        names = [ibm[k].get("display_name") for k in removed if ibm[k].get("display_name")]
        # free text counts: search the bare names anywhere in the object, with the kept lines' own display_name
        # fields stripped first (a kept line's name is not a leak and may contain a removed name as a substring)
        import re
        probe = dict(og)
        probe["by_model"] = {k: {f: v for f, v in e.items() if f != "display_name"} for k, e in obm.items()}
        txt = json.dumps(probe, sort_keys=True)
        leak_keys = [k for k in removed if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(k), txt)]
        leak_names = [x for x in names if x in txt]
        return (not leak_keys and not leak_names and bool(removed),
                "%d removed line(s); keys surviving %s; display names surviving %s" % (len(removed), leak_keys[:3], leak_names[:3]))

    def k8():
        same = all(out.get(f) is arts[f] for f in FIRMS)
        eq = all(arts[f] == before[f] for f in FIRMS)
        return same and eq, "firm scopes same objects=%s; deep-equal to pre-fold copies=%s" % (same, eq)

    def k9():
        bad = [k for k, e in ibm.items() if e.get("cohort_class") != "model" and obm.get(k) != e]
        nonmodel = [k for k, e in ibm.items() if e.get("cohort_class") != "model"]
        return not bad and bool(nonmodel), "%d non-model-class line(s) (SMA, tax) deep-equal; differing %s" % (len(nonmodel), bad[:3])

    def k10():
        nl = rep.get("null_lines") or {}
        want = {}
        for k, e in ibm.items():
            if e.get("cohort_class") != "model" or k in obm:
                continue
            if e["model_value"][-1] is None:
                last = [(i, v) for i, v in enumerate(e["model_value"]) if v is not None]
                if last:
                    want[k] = (round(last[-1][1], 2), dates[last[-1][0]])
        got = {k: (round(float(v.get("last_value")), 2), str(v.get("last_value_date"))[:10]) for k, v in nl.items()}
        return got == want and bool(want), "null lines %d: reported %s" % (len(want), {k: got.get(k) for k in sorted(want)})

    need("K2", k2)
    need("K3", k3)
    need("K4", k4)
    need("K5", k5)
    need("K6", k6)
    need("K7", k7)
    need("K8", k8)
    need("K9", k9)
    need("K10", k10)

    k = sum(1 for a in arms if a)
    print("ROUND 6 COMPARATOR: %d of %d arms" % (k, 11))
    return 0 if k == 11 and len(arms) == 11 else 1


if __name__ == "__main__":
    sys.exit(main())
