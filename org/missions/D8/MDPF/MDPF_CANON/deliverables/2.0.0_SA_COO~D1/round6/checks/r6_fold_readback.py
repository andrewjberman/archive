#!/usr/bin/env python3
"""MDPF_CANON round 6, cell CN-f-1 -- the ISSUER'S acceptance read of the first SCHEDULED fire that carries the Global min-firms fold.

Read-only against the SERVED objects (list/get/head + one lambda config/code read). Run it on the first fire that mints a new as-of date
after the fold deploy (2026-10-14 13:30Z at the earliest). Prints dates, counts and differences; never an account id, never a client level.

  python r6_fold_readback.py read [--date YYYY-MM-DD] [--prior YYYY-MM-DD]
        newest global aggregate-aua-timeseries date by default; --prior defaults to the previous dated global key.
  python r6_fold_readback.py refused --date YYYY-MM-DD [--expect-version <VersionId>]
        the CTO's third arm (ADDENDUM 6): a one-firm-as-of day publishes NO global object; the prior object is untouched.
  python r6_fold_readback.py selftest
        builds a folded global object OFFLINE from the real served 2026-10-09 objects through the merged fold, runs R1-R6 on it, then
        plants three defects and requires each to turn the named arm RED.

Arms (a line `  <ARM> PASS|FAIL <detail>` each, then `ROUND 6 READBACK: k of n arms`; exit 0 only when every arm passes):
  R1 no emitted global model-class line (other_models included) is held by < 2 firms on any date it carries a value
  R2 meta.by_model_fold: min_firms 2, per_model_detail_begins == first date any kept line is emitted, statement names no model
  R3 top-level key sets equal the prior object's (aggregate-aua-timeseries, aum-metrics, account-distribution, category-views)
  R4 headline arrays equal the prior object's on every common date
  R5 differential identity from served bytes: (after residual - before residual) == suppressed dollars, to the cent, every valued date
  R6 the three firm scopes' aggregate-aua-timeseries are value-equal to the prior date's on the common dates
  R7 account-distribution: against the PRIOR dated A4 object (the staged runner object is frozen at 2026-08-18, row S5): total within roster drift;
     folded keys gone; other_models count within tolerance of the sum of the prior day's removed counts
  R8 category-views: Models > Custom node aum at the as-of equals the sum of the custom-class by_model values at the as-of
  R9 manifest: run.code.commit == deployed package BUILD_MANIFEST commit == function env MDPF_GOLD_COMMIT; errors empty; 16 A4 objects
"""
from __future__ import annotations

import copy
import importlib
import io
import json
import os
import re
import subprocess
import sys

BUCKET = "opal-data-assets"
PREFIX = "portal/gold/mdpf"
TYPE_TS = "aggregate-aua-timeseries"
TYPES = ("aggregate-aua-timeseries", "aum-metrics", "account-distribution", "category-views")
SCOPES = ("global", "49financial", "inflection", "cottonwood")
FIRMS = ("49financial", "inflection", "cottonwood")
FOLD_KEY = "other_models"
HEADLINE = ("opal_aggregate_aua", "model_aua", "non_model_aua", "tax_additive_aua", "sma_additive_aua", "account_count_total")
LAMBDA = "mdpf-gold-lambda"
CENT = 0.005


# ------------------------------------------------------------------------------------------------ S3 reads
def _s3():
    import boto3
    from botocore.config import Config
    return boto3.client("s3", region_name="us-east-1", config=Config(read_timeout=30, connect_timeout=10,
                                                                      retries={"max_attempts": 2}))


def _keys(s3, scope: str, typ: str) -> list:
    out, tok = [], None
    while True:
        kw = {"Bucket": BUCKET, "Prefix": "%s/%s/%s/" % (PREFIX, scope, typ)}
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        out += [o["Key"] for o in r.get("Contents", []) if o["Key"].endswith(".json")]
        if not r.get("IsTruncated"):
            return sorted(out)
        tok = r.get("NextContinuationToken")


def _json(s3, key: str, bucket: str = BUCKET) -> dict:
    return json.loads(s3.get_object(Bucket=bucket, Key=key)["Body"].read())


def _date_of(key: str) -> str:
    return key.rsplit("/", 1)[-1][:-5]


# ------------------------------------------------------------------------------------------------ arithmetic
def _idx(a: dict) -> dict:
    return {d: j for j, d in enumerate(a.get("dates") or [])}


def _val(entry, i):
    arr = (entry or {}).get("model_value") or []
    return arr[i] if i is not None and i < len(arr) else None


def _is_model(entry) -> bool:
    return (entry or {}).get("cohort_class") == "model"


def _held_firms(firms: dict, key: str, date: str) -> list:
    out = []
    for f in FIRMS:
        a = (firms or {}).get(f)
        if not a:
            continue
        j = _idx(a).get(date)
        v = _val((a.get("by_model") or {}).get(key), j)
        if v is not None and v > 0:
            out.append(f)
    return out


def _model_sum(g: dict, i: int) -> float:
    s = 0.0
    for e in (g.get("by_model") or {}).values():
        if _is_model(e):
            v = _val(e, i)
            if v is not None:
                s += v
    return s


# ------------------------------------------------------------------------------------------------ arms R1-R6
def r1(new_g, firms) -> tuple:
    dates = new_g.get("dates") or []
    bad, lines, pairs = [], 0, 0
    for k, e in (new_g.get("by_model") or {}).items():
        if not _is_model(e):
            continue
        lines += 1
        for i, d in enumerate(dates):
            if _val(e, i) is None:
                continue
            pairs += 1
            n = len(_held_firms(firms, k, d)) if k != FOLD_KEY else None
            if n is not None and n < 2:
                bad.append((k, d, n))
    # the fold line is held by the union of the firms holding any line it pooled: graded as >= 2 firms hold a value on that date
    # in at least two scopes' objects (a pooled line is a firm's own line, so the union is read from the firms' own by_model)
    fold = (new_g.get("by_model") or {}).get(FOLD_KEY)
    fold_bad = []
    if fold:
        pooled_keys = [k for k in (new_g.get("meta") or {}).get("by_model_channels", {})]
        for i, d in enumerate(dates):
            if _val(fold, i) is None:
                continue
            union = set()
            for f in FIRMS:
                a = (firms or {}).get(f)
                if not a:
                    continue
                j = _idx(a).get(d)
                for k2, e2 in (a.get("by_model") or {}).items():
                    if not _is_model(e2) or k2 in (new_g.get("by_model") or {}):
                        continue                         # a line still shown individually was not pooled
                    v2 = _val(e2, j)
                    if v2 is not None and v2 > 0:
                        union.add(f)
            if len(union) < 2:
                fold_bad.append((FOLD_KEY, d, len(union)))
        del pooled_keys
    bad += fold_bad
    ok = not bad
    return ok, ("lines=%d line-dates=%d violations=%d%s" % (lines, pairs, len(bad), "" if ok else " first=%s" % bad[:5]))


def r2(new_g, prior_g) -> tuple:
    meta = new_g.get("meta") or {}
    f = meta.get("by_model_fold")
    if not isinstance(f, dict):
        return False, "meta.by_model_fold absent"
    dates = new_g.get("dates") or []
    first = None
    for i, d in enumerate(dates):
        for k, e in (new_g.get("by_model") or {}).items():
            if k != FOLD_KEY and _is_model(e) and _val(e, i) is not None:
                first = d
                break
        if first:
            break
    stmt = str(f.get("statement") or "")
    names = set()
    for k, e in (prior_g.get("by_model") or {}).items():
        names.add(k)
        if (e or {}).get("display_name"):
            names.add(e["display_name"])
    hits = sorted(n for n in names if len(n) >= 3 and re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(n), stmt, re.I))
    ok = f.get("min_firms") == 2 and f.get("per_model_detail_begins") == first and bool(stmt) and not hits
    return ok, ("min_firms=%s begins=%s first-kept-date=%s statement_len=%d model names in statement=%s"
                % (f.get("min_firms"), f.get("per_model_detail_begins"), first, len(stmt), hits))


def r3(pairs: list) -> tuple:
    """pairs: list of (label, new_obj, prior_obj_or_None)."""
    bad, n = [], 0
    for label, new, prior in pairs:
        if prior is None:
            continue
        n += 1
        a, b = set(new.keys()), set(prior.keys())
        if a != b:
            bad.append("%s +%s -%s" % (label, sorted(a - b), sorted(b - a)))
    return (not bad and n > 0), "types compared=%d%s" % (n, "" if not bad else " DIFF " + "; ".join(bad))


def r4(new_g, prior_g) -> tuple:
    na, pa = _idx(new_g), _idx(prior_g)
    last = (prior_g.get("dates") or [None])[-1]       # the prior object's own as-of is restated by the next fire: excluded, named
    common = [d for d in na if d in pa and d != last]
    bad = []
    for fld in HEADLINE:
        for d in common:
            x = (new_g.get(fld) or [None] * 0)
            y = (prior_g.get(fld) or [None] * 0)
            xi, yi = na[d], pa[d]
            xv = x[xi] if xi < len(x) else None
            yv = y[yi] if yi < len(y) else None
            if xv != yv:
                bad.append((fld, d))
    return not bad, "fields=%d common-dates=%d (prior as-of %s excluded) unequal=%d%s" % (
        len(HEADLINE), len(common), last, len(bad), "" if not bad else " first=%s" % bad[:5])


def r5(new_g, prior_g) -> tuple:
    na, pa = _idx(new_g), _idx(prior_g)
    last = (prior_g.get("dates") or [None])[-1]       # the prior object's own as-of is restated by the next fire: excluded
    common = [d for d in na if d in pa and d != last]
    bad, checked, pre_resid, kept_bad = [], 0, 0, []
    nb, pb = new_g.get("by_model") or {}, prior_g.get("by_model") or {}
    for d in common:
        i, j = na[d], pa[d]
        # lines still shown individually must equal the prior value; non-model-class lines (SMA, tax) must equal
        for k, e in nb.items():
            if k == FOLD_KEY or k not in pb:
                continue
            v, w = _val(e, i), _val(pb[k], j)
            if v is not None and (w is None or abs(v - w) >= CENT):
                kept_bad.append((k, d))
            if not _is_model(e) and v != w:
                kept_bad.append((k, d))
        ma_n = (new_g.get("model_aua") or [None] * 0)
        ma_p = (prior_g.get("model_aua") or [None] * 0)
        mn = ma_n[i] if i < len(ma_n) else None
        mp = ma_p[j] if j < len(ma_p) else None
        if mn is None or mp is None:
            continue
        before_sum = sum(v for v in (_val(e, j) for e in pb.values() if _is_model(e)) if v is not None)
        after_sum = _model_sum(new_g, i)
        pool = 0.0
        for k, e in pb.items():
            if not _is_model(e):
                continue
            wv = _val(e, j)
            if wv is None:
                continue
            nv = _val(nb.get(k), i) if k in nb and k != FOLD_KEY else None
            if nv is None:
                pool += wv
        om = _val(nb.get(FOLD_KEY), i)
        suppressed = pool - (om or 0.0)
        checked += 1
        if abs(mp - before_sum) >= CENT:
            pre_resid += 1
        diff = (mn - after_sum) - (mp - before_sum)
        if abs(diff - suppressed) >= CENT:
            bad.append((d, round(diff - suppressed, 2)))
    ok = not bad and not kept_bad and checked > 0
    return ok, ("valued dates checked=%d identity violations=%d kept/other-class line differences=%d; pre-existing residual on %d of %d dates%s"
                % (checked, len(bad), len(kept_bad), pre_resid, checked,
                   "" if ok else " first=%s" % (bad[:3] + kept_bad[:3])))


def r6(firms_new: dict, firms_prior: dict) -> tuple:
    bad, n = [], 0
    for f in FIRMS:
        a, b = (firms_new or {}).get(f), (firms_prior or {}).get(f)
        if not a or not b:
            bad.append((f, "absent"))
            continue
        ai, bi = _idx(a), _idx(b)
        lastb = (b.get("dates") or [None])[-1]        # the prior object's own as-of is restated by the next fire: excluded
        common = [d for d in ai if d in bi and d != lastb]
        for d in common:
            n += 1
            i, j = ai[d], bi[d]
            for fld in HEADLINE:
                x, y = a.get(fld) or [], b.get(fld) or []
                if (x[i] if i < len(x) else None) != (y[j] if j < len(y) else None):
                    bad.append((f, d, fld))
            for k, e in (a.get("by_model") or {}).items():
                if _val(e, i) != _val((b.get("by_model") or {}).get(k), j):
                    bad.append((f, d, k))
    return not bad, "firm scopes=%d firm-dates compared=%d unequal=%d%s" % (len(FIRMS), n, len(bad),
                                                                            "" if not bad else " first=%s" % bad[:4])


# ------------------------------------------------------------------------------------------------ live arms R7-R9
def r7(dist: dict, staged: dict) -> tuple:
    """AMENDED 2026-10-14 ~00:4xZ (issuer): the reference is the PRIOR dated A4 global account-distribution, NOT the staged runner object.
    The staged gold/mdpf_revamp/global/account_distribution.json has been frozen since 2026-08-18 (period 2026-08-17, row S5), so no served total
    can equal it. The fold leaves `total` unchanged by design, but the roster drifts a few accounts a day, so the counts are compared with a
    stated tolerance and both numbers are printed. When the prior object is itself already folded (second folded day onward) only the structure is
    checked: the fold key set is stable and no unfolded key reappears."""
    if not staged:
        return False, "no prior dated global account-distribution to compare against"
    nb, sb = dist.get("by_model") or {}, staged.get("by_model") or {}
    nm = (dist.get("meta") or {}).get("account_count_by_model_key") or {}
    sm = (staged.get("meta") or {}).get("account_count_by_model_key") or {}
    nt = int((dist.get("total") or {}).get("account_count") or 0)
    st = int((staged.get("total") or {}).get("account_count") or 0)
    drift_ok = abs(nt - st) <= max(10, int(0.01 * st))
    prior_folded = FOLD_KEY in sm
    removed_keys = sorted(set(sm) - set(nm))
    added = sorted(set(nm) - set(sm))
    removed_names = sorted(set(sb) - set(nb))
    other_names = sorted(set(nb) - set(sb))
    if prior_folded:
        reappeared = sorted(set(nm) - set(sm))
        ok = drift_ok and not reappeared
        return ok, ("prior object already folded: unfolded keys that reappeared=%s; total new=%d prior=%d (drift ok=%s)"
                    % (reappeared, nt, st, drift_ok))
    rm_count = sum(int((sb[n] or {}).get("account_count") or 0) for n in removed_names)
    got = None
    for n in other_names:
        got = int((nb[n] or {}).get("account_count") or 0)
    tol = max(3, int(0.03 * rm_count))
    count_ok = got is not None and abs(got - rm_count) <= tol
    ok = (FOLD_KEY in added and len(other_names) == 1 and count_ok and bool(removed_keys)
          and FOLD_KEY not in removed_keys and drift_ok)
    return ok, ("removed model keys=%d removed entries=%d added keys=%s; other_models account_count=%s vs sum of the prior day's removed=%d "
                "(tolerance %d, roster drift between days); total new=%d prior=%d (drift ok=%s)"
                % (len(removed_keys), len(removed_names), added, got, rm_count, tol, nt, st, drift_ok))


def r8(cv: dict, new_g: dict) -> tuple:
    models = (cv.get("nodes") or {}).get("Models") or {}
    custom = None
    ch = models.get("children") or {}
    items = ch.items() if isinstance(ch, dict) else enumerate(ch)
    for _k, v in items:
        if isinstance(v, dict) and v.get("display_label") == "Custom":
            custom = v
    if custom is None:
        return False, "Models > Custom node absent"
    ids = [m.get("member_id") for m in custom.get("members") or []]
    last = len(new_g.get("dates") or []) - 1
    s = 0.0
    for k in ids:
        v = _val((new_g.get("by_model") or {}).get(k), last)
        if v is not None:
            s += v
    aum = custom.get("aum")
    ok = aum is not None and abs(aum - s) < CENT
    return ok, "node path Models > Custom; members=%d; node aum vs by_model sum differs by %s" % (
        len(ids), "n/a" if aum is None else "%.2f" % (aum - s))


def r9(s3, as_of: str) -> tuple:
    import urllib.request
    import zipfile
    import boto3
    pre = "%s/_manifests/%s/" % (PREFIX, as_of)
    ks = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=pre).get("Contents", []))
    if not ks:
        return False, "no manifest under %s" % pre
    m = _json(s3, ks[-1])
    lam = boto3.client("lambda", region_name="us-east-1")
    env = (lam.get_function_configuration(FunctionName=LAMBDA).get("Environment") or {}).get("Variables") or {}
    loc = lam.get_function(FunctionName=LAMBDA)["Code"]["Location"]
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(loc, timeout=60).read()))
    bm = json.loads(z.read("BUILD_MANIFEST.json"))
    pkg = ((bm.get("source_vintage") or {}).get("commit"))
    run = ((m.get("run") or {}).get("code") or {}).get("commit")
    envc = env.get("MDPF_GOLD_COMMIT")
    a4 = sorted({w.get("key") for w in (m.get("writes") or [])
                 if re.match(r"^%s/(%s)/(%s)/[0-9-]+\.json$" % (re.escape(PREFIX), "|".join(SCOPES), "|".join(TYPES)), w.get("key") or "")})
    errs = m.get("errors")
    ok = bool(run) and run == pkg == envc and not errs and len(a4) == 16
    return ok, ("manifest=%s run.code.commit=%s package=%s env=%s equal=%s; errors=%s; A4 object keys=%d"
                % (ks[-1].rsplit("/", 1)[-1], (run or "")[:10], (pkg or "")[:10], (envc or "")[:10],
                   run == pkg == envc, "empty" if not errs else json.dumps(errs)[:120], len(a4)))


# ------------------------------------------------------------------------------------------------ drivers
def _report(arms: list, label: str = "ROUND 6 READBACK") -> int:
    k = sum(1 for a in arms if a)
    print("%s: %d of %d arms" % (label, k, len(arms)))
    return 0 if k == len(arms) and arms else 1


def cmd_read(argv: list) -> int:
    date = prior = None
    if "--date" in argv:
        date = argv[argv.index("--date") + 1]
    if "--prior" in argv:
        prior = argv[argv.index("--prior") + 1]
    s3 = _s3()
    gk = _keys(s3, "global", TYPE_TS)
    dates = [_date_of(k) for k in gk]
    date = date or dates[-1]
    if date not in dates:
        print("  FAIL: no global %s object for %s (newest %s)" % (TYPE_TS, date, dates[-1]))
        return 1
    prior = prior or dates[dates.index(date) - 1]
    new_g = _json(s3, "%s/global/%s/%s.json" % (PREFIX, TYPE_TS, date))
    prior_g = _json(s3, "%s/global/%s/%s.json" % (PREFIX, TYPE_TS, prior))
    firms_new = {f: _json(s3, "%s/%s/%s/%s.json" % (PREFIX, f, TYPE_TS, date)) for f in FIRMS}
    firms_prior = {f: _json(s3, "%s/%s/%s/%s.json" % (PREFIX, f, TYPE_TS, prior)) for f in FIRMS}
    print("  read: global %s (prior %s); %d dates, %d model-class lines" % (
        date, prior, len(new_g.get("dates") or []), sum(1 for e in (new_g.get("by_model") or {}).values() if _is_model(e))))
    arms = []

    def arm(name, res):
        ok, detail = res
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        arms.append(bool(ok))

    other = {}
    for typ in TYPES[1:]:
        ks = _keys(s3, "global", typ)
        other[typ] = (_json(s3, ks[-1]), _json(s3, ks[-2]) if len(ks) > 1 else None)
    arm("R1", r1(new_g, firms_new))
    arm("R2", r2(new_g, prior_g))
    arm("R3", r3([(TYPE_TS, new_g, prior_g)] + [(t, a, b) for t, (a, b) in other.items()]))
    arm("R4", r4(new_g, prior_g))
    arm("R5", r5(new_g, prior_g))
    arm("R6", r6(firms_new, firms_prior))
    arm("R7", r7(other["account-distribution"][0], other["account-distribution"][1]))
    arm("R8", r8(other["category-views"][0], new_g))
    arm("R9", r9(s3, new_g.get("as_of_last") or date))
    return _report(arms)


def cmd_refused(argv: list) -> int:
    if "--date" not in argv:
        print("usage: refused --date YYYY-MM-DD [--expect-version V]")
        return 2
    date = argv[argv.index("--date") + 1]
    expect = argv[argv.index("--expect-version") + 1] if "--expect-version" in argv else None
    s3 = _s3()
    arms = []
    for typ in TYPES:
        ks = _keys(s3, "global", typ)
        has = any(_date_of(k) == date for k in ks)
        print("  %s: global object for %s %s; newest key %s" % (typ, date, "EXISTS" if has else "absent",
                                                              _date_of(ks[-1]) if ks else "none"))
    ks = _keys(s3, "global", TYPE_TS)
    newest = ks[-1]
    ver = s3.head_object(Bucket=BUCKET, Key=newest).get("VersionId")
    print("  newest global %s: %s VersionId=%s" % (TYPE_TS, _date_of(newest), ver))
    absent = not any(_date_of(k) == date for k in ks)
    arms.append(absent)
    print("  F1 %s: no global %s object was written for %s" % ("PASS" if absent else "FAIL", TYPE_TS, date))
    if expect:
        same = ver == expect
        arms.append(same)
        print("  F2 %s: prior object VersionId %s the expected one" % ("PASS" if same else "FAIL", "equals" if same else "DIFFERS from"))
    pre = "%s/_manifests/" % PREFIX
    mk = sorted(o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=pre + date + "/").get("Contents", []))
    if mk:
        m = _json(s3, mk[-1])
        e = (m.get("errors") or {}).get("global")
        print("  manifest %s errors.global: %s" % (mk[-1].rsplit("/", 1)[-1], (str(e)[:300] if e else "none")))
    return _report(arms, "ROUND 6 REFUSED")


def _selftest_world(root: str, date: str = "2026-10-09"):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    for sub in ("scripts/silver", "scripts/gold"):
        p = os.path.normpath(os.path.join(root, "data", "mdpf", sub))
        if p not in sys.path:
            sys.path.insert(0, p)
    if root not in sys.path:
        sys.path.insert(0, root)
    gc = importlib.import_module("mdpf_gold_consolidator")
    s3 = _s3()
    arts = {sc: _json(s3, "%s/%s/%s/%s.json" % (PREFIX, sc, TYPE_TS, date)) for sc in SCOPES}
    out, rep = gc.apply_global_min_firms_fold(copy.deepcopy(arts))
    return arts, out, rep


def cmd_selftest(argv: list) -> int:
    root = os.environ.get("R6_ROOT") or subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    arts, out, rep = _selftest_world(root)
    prior_g = arts["global"]
    firms = {f: arts[f] for f in FIRMS}
    new_g = out["global"]
    print("  selftest world: folded %s lines at as-of %s; other_models emitted on %s dates; suppressed dates=%s"
          % (len(rep.get("fold_keys") or []), rep.get("as_of"), rep.get("other_models_emitted_dates"),
             len(rep.get("suppressed_dates") or [])))

    def grade(g):
        return {"R1": r1(g, firms), "R2": r2(g, prior_g), "R3": r3([(TYPE_TS, g, prior_g)]), "R4": r4(g, prior_g),
                "R5": r5(g, prior_g), "R6": r6(firms, firms)}

    good = grade(new_g)
    allok = True
    for name in ("R1", "R2", "R3", "R4", "R5", "R6"):
        ok, detail = good[name]
        print("  %s %s: %s" % (name, "PASS" if ok else "FAIL", detail))
        allok = allok and ok
    plants = []
    d1 = copy.deepcopy(new_g)                         # a one-firm line left emitted
    one = None
    for k in rep.get("fold_keys") or []:
        if len([f for f in FIRMS if _val((firms[f].get("by_model") or {}).get(k), _idx(firms[f]).get(rep["as_of"]))
                and _val((firms[f].get("by_model") or {}).get(k), _idx(firms[f]).get(rep["as_of"])) > 0]) == 1:
            one = k
            break
    if one:
        d1["by_model"][one] = copy.deepcopy(prior_g["by_model"][one])
    plants.append(("D1 one-firm line left emitted (%s)" % (one or "none found"), d1, "R1"))
    d2 = copy.deepcopy(new_g)                         # a headline array changed by 0.01
    for i in range(len(d2["model_aua"]) - 5, -1, -1):  # a mid-history date: the prior object's own as-of is excluded from R4
        if d2["model_aua"][i] is not None:
            d2["model_aua"][i] = round(d2["model_aua"][i] + 0.01, 2)
            break
    plants.append(("D2 model_aua changed by 0.01", d2, "R4"))
    d3 = copy.deepcopy(new_g)                         # a model name in the in-band statement
    nm = next(iter(rep.get("fold_keys") or ["opal_fixed_income"]))
    d3["meta"]["by_model_fold"]["statement"] += " The line %s is folded." % nm
    plants.append(("D3 model key in the statement (%s)" % nm, d3, "R2"))
    for label, g, want in plants:
        res = grade(g)
        red = not res[want][0]
        print("  PLANT %s -> %s %s" % (label, want, "RED (expected)" if red else "NOT RED (BAD)"))
        allok = allok and red
    print("ROUND 6 READBACK SELFTEST: %s" % ("OK" if allok else "FAILED"))
    return 0 if allok else 1


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in ("read", "refused", "selftest"):
        print(__doc__)
        return 2
    return {"read": cmd_read, "refused": cmd_refused, "selftest": cmd_selftest}[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    sys.exit(main())
