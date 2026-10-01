"""MDPF_HEALGAP hookup, CTO condition 3 -- an OFFLINE REHEARSAL of Global's fold on the catch-up's restored points.

The catch-up's own dry runs built with the upload off, so no slice and no Global fold ever ran on the restored
values. This probe folds them, with ZERO S3 writes:

  1. the 49 Financial, Inflection, Cottonwood and Global artifacts the Gold function STAGED on its last scheduled
     run are read (four small objects under gold/mdpf_revamp/);
  2. CONTROL: `build_global_artifact` on the three staged firm artifacts must reproduce the staged Global one;
  3. the Cottonwood artifact is composed twice by the slice's own `build_composed`: as it is today (it must equal
     the staged one), and with the catch-up's planned partitions REPLACED IN MEMORY by what the builder would
     write (the slice's partition read is patched for those keys only);
  4. REHEARSAL: `build_global_artifact` on the staged 49 Financial and Inflection artifacts and the rehearsed
     Cottonwood one. Its own gates run (composition, cross-axis coherence). Then aum-metrics and the category
     tree are built from it.

A first version ran the whole build twice; the laptop link lost the Inflection scope to S3 read errors three
times on 2026-10-01 (12:07Z, 15:31Z, 15:58Z), so the two large legs are taken from the staged artifacts instead.

Usage, from the workspace root:
  py -3.12 org/missions/D8/MDPF/MDPF_TAXSMA/deliverables/4.0.0_SA_CRO/probes/healgap_global_fold_rehearsal.py"""
from __future__ import annotations

import copy
import json
import os
import re
import sys

ROOT = os.getcwd()
for _p in ("data/mdpf/scripts/gold", "data/mdpf/scripts/silver", "data/assets/scripts/gold"):
    sys.path.insert(0, os.path.join(ROOT, *_p.split("/")))

import boto3  # noqa: E402
from botocore.config import Config  # noqa: E402

_real_client = boto3.client


def _patient_client(*args, **kwargs):
    kwargs.setdefault("config", Config(read_timeout=600, connect_timeout=30,
                                       retries={"max_attempts": 6, "mode": "standard"}))
    return _real_client(*args, **kwargs)


boto3.client = _patient_client

import build_cottonwood_mdpf_slice as slice_mod  # noqa: E402
import build_dim_model_portfolio as bdmp  # noqa: E402
import dim_mdpf_aggregate_aua_timeseries as spine  # noqa: E402
import dim_mdpf_aum_metrics as aum_metrics  # noqa: E402
import mdpf_gold_catchup as catchup  # noqa: E402
import mdpf_gold_consolidator as gc  # noqa: E402

PROCESS_TIME_FIELDS = ("generated_at", "process_time", "last_updated", "source_vintage_age_hours", "built_at")
STAGING = "gold/mdpf_revamp/%s/aggregate_aua_timeseries.json"


def staged(s3, scope):
    head = s3.head_object(Bucket=bdmp.ASSETS_BUCKET, Key=STAGING % scope)
    doc = json.loads(s3.get_object(Bucket=bdmp.ASSETS_BUCKET, Key=STAGING % scope)["Body"].read())
    return doc, head["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")


def planned_builds(s3):
    gold_by_date, rekey = slice_mod.cottonwood_gold_by_date(s3)
    holdings_avail = slice_mod.holdings_available_dates(s3)
    axis = slice_mod.self_derived_axis(gold_by_date, holdings_avail)
    assignment_dates = set()
    for page in s3.get_paginator("list_objects_v2").paginate(
            Bucket=bdmp.ASSETS_BUCKET, Prefix=bdmp.SILVER_PREFIX + "fact_model_assignment/"):
        for obj in page.get("Contents", []):
            for seg in obj["Key"].split("/"):
                if seg.startswith("date="):
                    assignment_dates.add(seg[len("date="):])
    return catchup.plan(axis, holdings_avail, rekey["partition_to_value_date"], assignment_dates,
                        slice_mod.trading_days_between)


def build_in_memory(s3, adate, vdate):
    """What `build_dim_model_portfolio.main(["--date", A, "--value-date", V, "--upload"])` would write, as the
    slice would read it back (through the same arrow schema), without writing."""
    roster = bdmp.silver_table(s3, "fact_model_roster", adate)
    blend = bdmp.silver_table(s3, "fact_model_blend", adate)
    assignment = bdmp.silver_table(s3, "fact_model_assignment", adate)
    values = bdmp.account_values(s3, vdate)
    df, report = bdmp.build(roster, blend, assignment, values, adate, vdate)
    return bdmp.to_arrow(df).to_pandas(), bdmp.reconcile(df, roster, report)


def _strip(o):
    if isinstance(o, dict):
        return {k: _strip(v) for k, v in o.items() if k not in PROCESS_TIME_FIELDS and k != "_leg_source_key"}
    if isinstance(o, list):
        return [_strip(v) for v in o]
    return o


def _leaves(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                yield "%s/%s" % (path, k)
            else:
                yield from _leaves(a[k], b[k], "%s/%s" % (path, k))
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            yield from _leaves(x, y, "%s[%d]" % (path, i))
    elif a != b:
        yield path


def compare(label, a, b, five=()):
    """Print where two artifacts differ; every indexed series path is resolved to its axis date."""
    a, b = _strip(json.loads(json.dumps(a, default=str))), _strip(json.loads(json.dumps(b, default=str)))
    leaves = list(_leaves(a, b))
    dates = b.get("dates") or []
    by_date, other = {}, []
    for p in leaves:
        idx = re.findall(r"\[(\d+)\]", p)
        named = [d for d in five if ("/%s" % d) in p]
        if idx and int(idx[0]) < len(dates) and not p.startswith("/meta"):
            by_date.setdefault(dates[int(idx[0])], []).append(p)
        elif named:
            by_date.setdefault(named[0], []).append(p)
        else:
            other.append(p)
    off = sorted(d for d in by_date if d not in five)
    print("%s: %d differing leaf path(s) | dates touched %s | dates OUTSIDE the five %s | paths with no date %d %s" % (
        label, len(leaves), sorted(by_date), off, len(other), other[:6]))
    return len(leaves), off, other


def main() -> int:
    s3 = boto3.client("s3")
    a49, w49 = staged(s3, "49financial")
    ainf, winf = staged(s3, "inflection")
    acot_staged, wcot = staged(s3, "cottonwood")
    g_staged, wg = staged(s3, "global")
    print("STAGED (the Gold function's last scheduled run): 49financial %s, inflection %s, cottonwood %s, global %s; "
          "axes end %s / %s / %s / %s" % (w49, winf, wcot, wg, a49["dates"][-1], ainf["dates"][-1],
                                          acot_staged["dates"][-1], g_staged["dates"][-1]))

    g_control = spine.build_global_artifact(copy.deepcopy(a49), copy.deepcopy(ainf), copy.deepcopy(acot_staged))
    n, _off, _other = compare("CONTROL 1 (offline fold of the staged legs vs the staged Global)", g_staged, g_control)
    print("  -> the offline fold %s the function's own Global" % ("REPRODUCES" if n == 0 else "DOES NOT reproduce"))

    builds, skipped = planned_builds(s3)
    five = sorted(b["value_date"] for b in builds)
    print("PLAN: %d build(s) %s | skipped %d" % (
        len(builds), [(b["assignment_date"], b["value_date"]) for b in builds], len(skipped)))
    frames = {}
    for b in builds:
        df, fails = build_in_memory(s3, b["assignment_date"], b["value_date"])
        print("  in-memory partition date=%s value_date=%s: Opal dollars %.2f, reconcile %s" % (
            b["assignment_date"], b["value_date"], round(float(df[df.is_opal].dollar_value.sum()), 2),
            "PASS" if not fails else "FAIL %s" % fails))
        frames[slice_mod.COTTONWOOD_GOLD + "date=%s/data.parquet" % b["assignment_date"]] = df

    acot_base = slice_mod.build_composed(s3)
    n, _off, _other = compare("CONTROL 2 (the slice composed offline today vs the staged Cottonwood)", acot_staged, acot_base)
    print("  -> the offline slice %s the function's own Cottonwood artifact" % ("REPRODUCES" if n == 0 else "DIFFERS FROM"))

    real_read, served = slice_mod._read_parquet, []

    def patched(s3_, key):
        if key in frames:
            served.append(key)
            return frames[key].copy()
        return real_read(s3_, key)

    slice_mod._read_parquet = patched
    try:
        acot_reh = slice_mod.build_composed(s3)
    finally:
        slice_mod._read_parquet = real_read
    print("patched partition reads served: %d (distinct keys %d of %d)" % (len(served), len(set(served)), len(frames)))
    compare("COTTONWOOD (rehearsed vs composed today)", acot_base, acot_reh, five)

    try:
        g_reh = spine.build_global_artifact(copy.deepcopy(a49), copy.deepcopy(ainf), copy.deepcopy(acot_reh))
    except (Exception, SystemExit) as exc:  # noqa: BLE001 -- the refusal IS the finding
        print("GLOBAL FOLD REFUSED on the rehearsed Cottonwood artifact: %s: %s" % (type(exc).__name__, str(exc)[:900]))
        return 1
    print("GLOBAL FOLD: built on the rehearsed Cottonwood artifact; its composition and coherence gates raised nothing")
    g_base = spine.build_global_artifact(copy.deepcopy(a49), copy.deepcopy(ainf), copy.deepcopy(acot_base))
    compare("GLOBAL (rehearsed vs folded today)", g_base, g_reh, five)
    for d in five:
        if d in g_base["dates"] and d in g_reh["dates"]:
            ia, ib = g_base["dates"].index(d), g_reh["dates"].index(d)
            ic = acot_reh["dates"].index(d) if d in acot_reh["dates"] else None
            print("  %s: cottonwood model_aua %s | global model_aua %s -> %s | global opal_aggregate_aua %s -> %s | point_class %s -> %s" % (
                d, acot_reh["model_aua"][ic] if ic is not None else None, g_base["model_aua"][ia], g_reh["model_aua"][ib],
                g_base["opal_aggregate_aua"][ia], g_reh["opal_aggregate_aua"][ib],
                (g_base.get("point_class") or [None] * len(g_base["dates"]))[ia],
                (g_reh.get("point_class") or [None] * len(g_reh["dates"]))[ib]))

    firms = {"49financial": a49, "inflection": ainf, "cottonwood": acot_reh}
    for name, fn in (
            ("aum-metrics (global)", lambda: aum_metrics.build_aum_metrics(copy.deepcopy(g_reh), copy.deepcopy(firms))),
            ("category tree (global)", lambda: gc._shape_category_views(
                gc._shape_timeseries(copy.deepcopy(g_reh), "global", None, None), "global", None)),
            ("category tree (cottonwood)", lambda: gc._shape_category_views(
                gc._shape_timeseries(copy.deepcopy(acot_reh), "cottonwood", None, None), "cottonwood", None))):
        try:
            out = fn()
            print("DOWNSTREAM %s: built (%s)" % (name, "total.aum %s" % (out.get("total") or {}).get("aum")
                                                 if "total" in (out or {}) else "sums %s" % (out or {}).get("sums")))
        except (Exception, SystemExit) as exc:  # noqa: BLE001 -- reported, the next one still runs
            print("DOWNSTREAM %s: REFUSED %s: %s" % (name, type(exc).__name__, str(exc)[:400]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
