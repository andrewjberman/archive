"""MDPF_REVAMP parity harness (DT lane) -- compare a PUBLISHED portal/ artifact to
its SERVED legacy counterpart. Grounds on LIVE S3, never a self-report. Parity bar
= impl package s6 + the pre-swap baseline + CTO's D1=serve-real bar (2026-07-20).

D1 = SERVE REAL/COMPLETE DATA (Andrew, 2026-07-20): the revamp CORRECTS 3 legacy
artifacts, each a NAMED delta -- (1) real history vs interpolated backfill (+10-40%
2024-25, converging), (2) full-envelope custody +$20M, (3) complete 49F model +$4.1M
(the legacy feeder's model-tier enumeration gap). So a value delta is EXPECTED iff it
matches the DS-supplied NAMED-DELTA LEDGER; anything else is UNEXPLAINED.

THE (a)-(d) BAR (CTO, value-parity streak):
  (a) shape parity holds (incl. the history arrays),
  (b) each value delta MATCHES the named-delta ledger (magnitude + sign),
  (c) NO OTHER unexplained delta,
  (d) the clean cross-sections tie + date-drift converges same-cycle (run the streak
      SAME-CYCLE: a date-aligned gold vs served has no date-drift; any residual delta
      is then either a ledger-named correction or unexplained).
Tight 0.1% tolerance so any UNEXPECTED delta still surfaces named.

VERDICT: SHAPE_FAIL (missing/unexpected-extra) > UNEXPLAINED_DELTA (a delta with no
ledger match) > NAMED_DELTA_PASS (only ledger-matched deltas) > PASS (no delta).
NO ledger -> every value delta is UNEXPLAINED (fail-safe: the ledger must be supplied
to pass value parity; run account_distribution SAME-CYCLE so there is nothing to explain).

MODES:
  --artifact <name> --firm <firm> [--ledger <ledger.json>]
  --all [--ledger <ledger.json>]
  --self-test        identity + mutant discrimination (snapshot + history/ledger) --
                     a comparator that cannot fail is not a comparator

LEDGER FORMAT (DS supplies, keyed "<artifact>/<firm>"; per field-path pattern):
  { "aggregate_aua_timeseries/49financial": {
      "model_aua":               {"sign":"+","pct_range":[10,40],"date_before":"2026-01-01","note":"D1 real-history correction (converging)"},
      "partner_custody_total":   {"sign":"+","abs":20000000,"tol_pct":25,"note":"full-envelope custody +$20M"},
      "by_model.*.model_value":  {"sign":"+","pct_range":[0,45],"note":"complete-model / enumeration-gap correction"} } }
  Match iff: the field-path pattern is a substring of the leaf path (glob '*' allowed),
  the sign matches, the magnitude is in pct_range (relative) OR within tol_pct of abs
  (absolute), and dates[i] satisfies date_before/date_after if present.

NOTES: account_distribution keys by_model on DISPLAY NAME; aggregate on MODEL_KEY --
each compared to its OWN served, never cross-normalized. Spec extras (basis/meta) allowed.
"""
from __future__ import annotations

import argparse
import copy
import fnmatch
import json
import sys

import boto3
from botocore.exceptions import ClientError

SERVED_BUCKET = "opal-data-portal-v2"
PUBLISHED_BUCKET = "opal-data-assets"
REL_TOL = 0.001  # 0.1% -- deliberately tighter than the F2 band so deltas surface NAMED
ALLOWED_EXTRAS = {"basis", "meta", "source_vintage_last"}

ARTIFACTS = {
    ("aggregate_aua_timeseries", "global"): {
        "served": "json/mdpf/global/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/global/aggregate_aua_timeseries.json"},
    ("aggregate_aua_timeseries", "49financial"): {
        "served": "json/mdpf/49financial/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/49financial/aggregate_aua_timeseries.json"},
    ("aggregate_aua_timeseries", "inflection"): {
        "served": "json/mdpf/inflection/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/inflection/aggregate_aua_timeseries.json"},
    ("account_distribution", "49financial"): {
        "served": "json/mdpf/49financial/account-distribution.json",
        "published": "portal/model-portfolios/49financial/account_distribution.json"},
    ("account_distribution", "inflection"): {
        "served": "json/mdpf/inflection/account-distribution.json",
        "published": "portal/model-portfolios/inflection/account_distribution.json"},
    ("non_model_assets", "global"): {
        "served": "json/portfolios/non_model_assets.json",
        "published": "portal/portfolios/global/non_model_assets.json"},
    ("aum_metrics", "global"): {
        "served": "json/portfolios/aum-metrics.json",
        "published": "portal/portfolios/global/aum_metrics.json"},
    ("aum_timeseries", "global"): {
        "served": "json/portfolios/aum-timeseries.json",
        "published": "portal/portfolios/global/aum_timeseries.json"},
    ("account_distribution", "global"): {
        "served": "json/portfolios/account-distribution.json",
        "published": "portal/portfolios/global/account_distribution.json"},
}


def _s3():
    return boto3.client("s3", region_name="us-east-1")


def _get(bucket, key):
    try:
        return json.loads(_s3().get_object(Bucket=bucket, Key=key)["Body"].read())
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchKey", "404", "NoSuchBucket"):
            return None
        raise


def _shape(obj, path=""):
    out = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            out.add(p)
            out |= _shape(v, p)
    elif isinstance(obj, list) and obj:
        out |= _shape(obj[0], f"{path}[]")
    return out


def _shape_diff(served, published):
    s, p = _shape(served), _shape(published)
    missing = sorted(s - p)
    extra = sorted(k for k in p - s if k.split(".")[-1].split("[")[0] not in ALLOWED_EXTRAS)
    return missing, extra


def _leaves(obj, path="", idx=None):
    """All numeric leaves keyed by path; array elements as path[i]. Records the array
    index of the LAST path component so the ledger can date-scope it."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(_leaves(v, f"{path}.{k}" if path else k, idx))
    elif isinstance(obj, list) and obj:
        for i, el in enumerate(obj):
            out.update(_leaves(el, f"{path}[{i}]", i))
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out[path] = (float(obj), idx)
    return out


def _fieldbase(leafpath):
    """Strip [i] indices -> the ledger-matchable field path (e.g. by_model.Long Term.model_value[3] -> by_model.Long Term.model_value)."""
    import re
    return re.sub(r"\[\d+\]", "", leafpath)


def _ledger_match(leafpath, idx_date, sv, pv, entries):
    delta = pv - sv
    sign = "+" if delta > 0 else "-"
    base = _fieldbase(leafpath)
    for pat, spec in entries.items():
        if not (pat == base or pat in base or fnmatch.fnmatch(base, pat)):
            continue
        if spec.get("sign", "any") not in ("any", sign):
            continue
        db, da = spec.get("date_before"), spec.get("date_after")
        if db and idx_date and idx_date >= db:
            continue
        if da and idx_date and idx_date < da:
            continue
        if "pct_range" in spec:
            lo, hi = spec["pct_range"]
            if lo <= abs(delta) / max(abs(sv), 1.0) * 100.0 <= hi:
                return spec.get("note", pat)
        if "abs" in spec:
            tol = spec.get("tol_pct", 10) / 100.0 * abs(spec["abs"])
            if abs(abs(delta) - abs(spec["abs"])) <= tol:
                return spec.get("note", pat)
    return None


def compare(served, published, entries=None):
    entries = entries or {}
    missing, extra = _shape_diff(served, published)
    dates = served.get("dates") if isinstance(served, dict) else None
    ls, lp = _leaves(served), _leaves(published)
    expected, unexplained = [], []
    for k in sorted(set(ls) & set(lp)):
        sv, idxs = ls[k]
        pv, _ = lp[k]
        if abs(sv - pv) / max(abs(sv), 1.0) <= REL_TOL:
            continue
        idx_date = dates[idxs] if (dates and idxs is not None and 0 <= idxs < len(dates)) else None
        note = _ledger_match(k, idx_date, sv, pv, entries)
        (expected if note else unexplained).append((k, sv, pv, note))
    return {"missing": missing, "extra": extra, "expected": expected, "unexplained": unexplained,
            "shape_ok": not (missing or extra)}


def check_pair(name, firm, spec, ledger):
    served = _get(SERVED_BUCKET, spec["served"])
    if served is None:
        return {"name": name, "firm": firm, "verdict": "SERVED_ABSENT", "note": spec["served"]}
    published = _get(PUBLISHED_BUCKET, spec["published"])
    if published is None:
        return {"name": name, "firm": firm, "verdict": "PUBLISHED_ABSENT",
                "note": f"{spec['published']} absent (awaiting publisher); served shape {len(_shape(served))} paths"}
    entries = (ledger or {}).get(f"{name}/{firm}", {})
    r = compare(served, published, entries)
    if not r["shape_ok"]:
        r["verdict"] = "SHAPE_FAIL"
    elif r["unexplained"]:
        r["verdict"] = "UNEXPLAINED_DELTA"
    elif r["expected"]:
        r["verdict"] = "NAMED_DELTA_PASS"
    else:
        r["verdict"] = "PASS"
    r["name"], r["firm"], r["ledger_n"] = name, firm, len(entries)
    return r


def self_test():
    spec = ARTIFACTS[("account_distribution", "49financial")]
    served = _get(SERVED_BUCKET, spec["served"])
    if served is None:
        print("SELF-TEST: cannot fetch served TO-3 -- SKIP")
        return None
    ok = True
    ident = compare(served, served)
    ok &= ident["shape_ok"] and not ident["expected"] and not ident["unexplained"]
    mut = copy.deepcopy(served)
    mut["total"]["account_count"] += 100
    ok &= bool(compare(served, mut)["unexplained"])
    # history + ledger: +20% pre-2026 (EXPECTED) + an unrelated +50% (UNEXPLAINED)
    ts_s = {"dates": ["2025-06-01", "2026-06-01"], "model_aua": [100.0, 200.0], "x": [50.0, 60.0]}
    ts_p = {"dates": ["2025-06-01", "2026-06-01"], "model_aua": [120.0, 200.0], "x": [50.0, 90.0]}
    led = {"model_aua": {"sign": "+", "pct_range": [10, 40], "date_before": "2026-01-01", "note": "D1 history"}}
    r = compare(ts_s, ts_p, led)
    exp_ok = any(k == "model_aua[0]" for k, *_ in r["expected"])
    unexp_ok = any(k == "x[1]" for k, *_ in r["unexplained"])
    ok &= exp_ok and unexp_ok
    print(f"SELF-TEST snapshot identity(tie)+mutant(+100 detected): {ident['shape_ok'] and not ident['unexplained']} / {bool(compare(served, mut)['unexplained'])}")
    print(f"SELF-TEST history+ledger: EXPECTED(model_aua[0] +20% pre-26)={exp_ok}; UNEXPLAINED(x[1] +50%)={unexp_ok}")
    print(f"SELF-TEST {'PASS' if ok else 'FAIL'} -- classifies EXPECTED vs UNEXPLAINED (a comparator that can't fail proves nothing)")
    return ok


def _report(r):
    v = r["verdict"]
    head = f"[{v}] {r['name']}/{r['firm']}" + (f" (ledger:{r.get('ledger_n',0)})" if "ledger_n" in r else "")
    if v in ("SERVED_ABSENT", "PUBLISHED_ABSENT"):
        print(f"{head} -- {r['note']}")
        return
    print(head)
    if r["missing"]:
        print(f"    (a) SHAPE MISSING: {r['missing'][:6]}{' ...+%d' % (len(r['missing'])-6) if len(r['missing'])>6 else ''}")
    if r["extra"]:
        print(f"    (a) SHAPE EXTRA: {r['extra'][:6]}{' ...+%d' % (len(r['extra'])-6) if len(r['extra'])>6 else ''}")
    for k, sv, pv, note in r["expected"][:10]:
        print(f"    (b) NAMED {k}: {sv:,.2f}->{pv:,.2f} [{note}]")
    if len(r["expected"]) > 10:
        print(f"    (b) ...+{len(r['expected'])-10} more named")
    for k, sv, pv, _ in r["unexplained"][:12]:
        print(f"    (c) UNEXPLAINED {k}: {sv:,.2f}->{pv:,.2f}")
    if len(r["unexplained"]) > 12:
        print(f"    (c) ...+{len(r['unexplained'])-12} more UNEXPLAINED")
    if v == "PASS":
        print("    shape identical + all values tie")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifact")
    ap.add_argument("--firm")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--ledger")
    args = ap.parse_args()
    if args.self_test:
        return 0 if self_test() else 1
    ledger = json.load(open(args.ledger, encoding="utf-8")) if args.ledger else None
    if args.all:
        for (name, firm), spec in ARTIFACTS.items():
            _report(check_pair(name, firm, spec, ledger))
        return 0
    if args.artifact and args.firm:
        spec = ARTIFACTS.get((args.artifact, args.firm))
        if not spec:
            print(f"no in-scope artifact ({args.artifact}, {args.firm})")
            return 1
        _report(check_pair(args.artifact, args.firm, spec, ledger))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
