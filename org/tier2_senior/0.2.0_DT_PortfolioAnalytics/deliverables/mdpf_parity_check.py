"""MDPF_REVAMP parity harness (DT lane) -- compare a PUBLISHED portal/ artifact to
its SERVED legacy counterpart. Shape + latest-cross-section parity ONLY; NO
historical byte-diff (aggregate_aua_timeseries history is D1/D2-HELD). Grounds on
LIVE S3, never a self-report. Parity bar = impl package s6 + the pre-swap baseline.

MODES:
  --artifact <name> --firm <firm>   one artifact (served vs published)
  --all                             every in-scope pair
  --self-test                       served-vs-served identity + served-vs-mutant
                                    discrimination -- proves the harness discriminates
                                    (a comparator that cannot fail is not a comparator)

NOTES (load-bearing):
  * account_distribution keys by_model on DISPLAY NAME; aggregate_aua_timeseries on
    MODEL_KEY. Each is compared to its OWN served counterpart -- NEVER cross-normalized.
  * The revamp artifact carries spec-mandated fields the legacy served one lacks
    (basis, meta, ...) -> whitelisted as ALLOWED_EXTRAS, never a parity failure.
  * timeseries: shape + LAST array element only (the latest cross-section). The
    historical arrays await Andrew's D1/D2 -> carried as a named delta, NOT diffed here.
"""
from __future__ import annotations

import argparse
import copy
import json
import sys

import boto3
from botocore.exceptions import ClientError

SERVED_BUCKET = "opal-data-portal-v2"
PUBLISHED_BUCKET = "opal-data-assets"
REL_TOL = 0.001  # 0.1% latest-cross-section tolerance

# Extras the revamp artifact carries that the legacy served one lacks -- spec-
# mandated, ALLOWED (never a parity failure). Grounded on the live served TO-3
# (top keys: firm_id, firm_name, generated_at, period, source, total, by_model --
# NO basis; the revamp adds basis:schwab-rps per the spec).
ALLOWED_EXTRAS = {"basis", "meta", "source_vintage_last"}

ARTIFACTS = {
    ("aggregate_aua_timeseries", "global"): {
        "served": "json/mdpf/global/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/global/aggregate_aua_timeseries.json",
        "kind": "timeseries"},
    ("aggregate_aua_timeseries", "49financial"): {
        "served": "json/mdpf/49financial/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/49financial/aggregate_aua_timeseries.json",
        "kind": "timeseries"},
    ("aggregate_aua_timeseries", "inflection"): {
        "served": "json/mdpf/inflection/aggregate-aua-timeseries.json",
        "published": "portal/model-portfolios/inflection/aggregate_aua_timeseries.json",
        "kind": "timeseries"},
    ("account_distribution", "49financial"): {
        "served": "json/mdpf/49financial/account-distribution.json",
        "published": "portal/model-portfolios/49financial/account_distribution.json",
        "kind": "snapshot"},
    ("account_distribution", "inflection"): {
        "served": "json/mdpf/inflection/account-distribution.json",
        "published": "portal/model-portfolios/inflection/account_distribution.json",
        "kind": "snapshot"},
    ("non_model_assets", "global"): {
        "served": "json/portfolios/non_model_assets.json",
        "published": "portal/portfolios/global/non_model_assets.json",
        "kind": "timeseries"},
    ("aum_metrics", "global"): {
        "served": "json/portfolios/aum-metrics.json",
        "published": "portal/portfolios/global/aum_metrics.json",
        "kind": "snapshot"},
    ("aum_timeseries", "global"): {
        "served": "json/portfolios/aum-timeseries.json",
        "published": "portal/portfolios/global/aum_timeseries.json",
        "kind": "timeseries"},
    ("account_distribution", "global"): {
        "served": "json/portfolios/account-distribution.json",
        "published": "portal/portfolios/global/account_distribution.json",
        "kind": "snapshot"},
}


def _s3():
    return boto3.client("s3", region_name="us-east-1")


def _get(bucket, key):
    try:
        body = _s3().get_object(Bucket=bucket, Key=key)["Body"].read()
        return json.loads(body)
    except ClientError as e:
        if e.response["Error"]["Code"] in ("NoSuchKey", "404", "NoSuchBucket"):
            return None
        raise


def _shape(obj, path=""):
    """Structure fingerprint: recursive set of key-paths (array element 0 only)."""
    out = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            out.add(p)
            out |= _shape(v, p)
    elif isinstance(obj, list) and obj:
        out |= _shape(obj[0], f"{path}[]")
    return out


def _leaf_scalars(obj, path=""):
    """number leaves keyed by path; lists -> LAST element (latest cross-section)."""
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(_leaf_scalars(v, f"{path}.{k}" if path else k))
    elif isinstance(obj, list) and obj:
        out.update(_leaf_scalars(obj[-1], f"{path}[-1]"))
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out[path] = float(obj)
    return out


def _cmp(served, published):
    s_shape, p_shape = _shape(served), _shape(published)
    missing = sorted(s_shape - p_shape)  # served-not-published -> FAIL
    extra = sorted(k for k in p_shape - s_shape
                   if k.split(".")[-1].split("[")[0] not in ALLOWED_EXTRAS)
    s_leaf, p_leaf = _leaf_scalars(served), _leaf_scalars(published)
    deltas = []
    for k in sorted(set(s_leaf) & set(p_leaf)):
        sv, pv = s_leaf[k], p_leaf[k]
        if abs(sv - pv) / max(abs(sv), 1.0) > REL_TOL:
            deltas.append((k, sv, pv))
    return {"missing": missing, "extra": extra, "deltas": deltas,
            "shape_ok": not missing, "latest_ok": not deltas}


def check_pair(name, firm, spec):
    served = _get(SERVED_BUCKET, spec["served"])
    if served is None:
        return {"name": name, "firm": firm, "verdict": "SERVED_ABSENT",
                "note": f"served {spec['served']} not found"}
    published = _get(PUBLISHED_BUCKET, spec["published"])
    if published is None:
        return {"name": name, "firm": firm, "verdict": "PUBLISHED_ABSENT",
                "note": f"published {spec['published']} absent (awaiting publisher); "
                        f"served shape-validated ({len(_shape(served))} key-paths)"}
    r = _cmp(served, published)
    r["verdict"] = "PASS" if (r["shape_ok"] and r["latest_ok"]) else "DELTA"
    r["name"], r["firm"] = name, firm
    return r


def self_test():
    spec = ARTIFACTS[("account_distribution", "49financial")]
    served = _get(SERVED_BUCKET, spec["served"])
    if served is None:
        print("SELF-TEST: cannot fetch served TO-3 -- SKIP")
        return None
    ident = _cmp(served, served)
    ok_ident = ident["shape_ok"] and ident["latest_ok"]
    mut = copy.deepcopy(served)
    mut["total"]["account_count"] = served["total"]["account_count"] + 100
    disc = _cmp(served, mut)
    ok_disc = not disc["latest_ok"]
    print(f"SELF-TEST identity(served vs served): shape_ok+latest_ok = {ok_ident}")
    print(f"SELF-TEST discrimination(served vs +100 mutant): perturbation DETECTED = {ok_disc}")
    print(f"SELF-TEST {'PASS' if ok_ident and ok_disc else 'FAIL'} "
          f"(a comparator that cannot fail is not a comparator)")
    return ok_ident and ok_disc


def _report(r):
    v = r["verdict"]
    head = f"[{v}] {r['name']} / {r['firm']}"
    if v in ("SERVED_ABSENT", "PUBLISHED_ABSENT"):
        print(f"{head} -- {r['note']}")
        return
    print(head)
    if r["missing"]:
        print(f"    MISSING (served-not-published, FAIL): {r['missing']}")
    if r["extra"]:
        print(f"    EXTRA (unexpected, not whitelisted): {r['extra']}")
    for k, sv, pv in r["deltas"]:
        print(f"    DELTA {k}: served={sv:,.4f} published={pv:,.4f}")
    if v == "PASS":
        print("    shape identical (allowing spec extras) + latest cross-section ties")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--artifact")
    ap.add_argument("--firm")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return 0 if self_test() else 1
    if args.all:
        for (name, firm), spec in ARTIFACTS.items():
            _report(check_pair(name, firm, spec))
        return 0
    if args.artifact and args.firm:
        spec = ARTIFACTS.get((args.artifact, args.firm))
        if not spec:
            print(f"no in-scope artifact ({args.artifact}, {args.firm})")
            return 1
        _report(check_pair(args.artifact, args.firm, spec))
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
