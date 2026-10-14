#!/usr/bin/env python3
"""portfolios_card.py -- the /portfolios BEFORE and AFTER numbers for the Global fold card (2.0.0_SA_COO~D1, MDPF_CANON).

READ-ONLY. It re-derives, from the served Global objects, the four numbers the Model Portfolios page shows and the
fold (CN-f-1) changes, exactly as portal/src/pages/ModelPortfolios.tsx derives them at the HEAD of this tree:

  H  Total Holdings headline  = distribution.total.account_count + the account_count of every by_model key that
                                getCanonicalModelName maps into BLEND_ARCHETYPES        (page :1238-1245)
  C  archetype cards          = aum-metrics by_model rows, names canonicalised, then rollBlendsIntoArchetypeModels:
                                each blend's aum/2 and its full account_count added to BOTH of its archetypes
                                                                                          (page :690-723, :163-224)
  T  trend series             = the global aggregate-aua-timeseries by_model lines with cohort_class != 'sma',
                                names canonicalised, then rollBlendsIntoArchetypeSeries (blend/2 into both targets)
                                                                                          (page :782-857, :171-204)
  Q  quarter cells            = aum-metrics by_model rows' q0..q3 (a cell is ABSENT when change, growth and
                                priorLevel are all null), for the five canonical models

Subcommands:
  before                    print the numbers from the newest UNFOLDED dated objects and (unless refused) pin them to
                            portfolios_card_before.snapshot.json beside this file. Refuses to pin a snapshot built from a
                            folded object (meta.by_model_fold present).
  after [--date D]          recompute from the dated objects at or before D (the same rule) and print a before/after
                            table with deltas against the pinned snapshot. D is the run date: the distribution is keyed by
                            run date and aum-metrics / aggregate-aua-timeseries by the frontier date, so each type takes its
                            newest key <= D. --date is optional: with no --date, D is the date of the NEWEST
                            account-distribution key (the one run-date-keyed type, so its newest key is the latest run); a
                            wall-clock default would read the previous run before the fire. Use --source platinum to read
                            the served platinum copies instead.
                            The FIRST stdout line states what was read: PORTFOLIOS-CARD READ date=D (how) and the full key
                            of each of the three types. With --source a4, a second line WARNs when a newer account-distribution
                            key exists than D.

Run after a fire:  python portfolios_card.py after        (D = the newest account-distribution key, the run date)
                   python portfolios_card.py after --date 2026-10-14   (an explicit D; the first line says "explicit")
No account id is read into any output (the objects carry none at this grain); dollars and counts are printed because
the card to Andrew states them.
"""
import argparse
import json
import os
import re
import sys

import boto3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, *([".."] * 9)))
SNAP = os.path.join(HERE, "portfolios_card_before.snapshot.json")
A4_BUCKET = "opal-data-assets"
PLAT_BUCKET = "opal-data-portal-v2"
A4_TYPES = ("aum-metrics", "account-distribution", "aggregate-aua-timeseries")
CORE = ("Ultra-Short Term", "Short Term", "Intermediate Term", "Long Term", "Ultra-Long Term")
BLEND_ARCHETYPES = {"50/50 ST/INT": ("Short Term", "Intermediate Term"), "50/50 INT/LT": ("Intermediate Term", "Long Term")}
COLORS_TS = os.path.join(ROOT, "portal", "src", "lib", "modelPortfolioColors.ts")


def canonical_map():
    """The page's CANONICAL_MODEL_NAME, parsed from its own source so it cannot drift from HEAD."""
    src = open(COLORS_TS, encoding="utf-8").read()
    i = src.index("const CANONICAL_MODEL_NAME")
    j = src.index("\n}\n", i)
    pairs = re.findall(r"""['"]([^'"]+)['"]\s*:\s*['"]([^'"]+)['"]""", src[i:j])
    return dict(pairs)


CMAP = canonical_map()


def canon(name):
    return CMAP.get(name, name) if name else name


def s3():
    return boto3.client("s3", region_name="us-east-1")


def a4_keys(c, t, scope="global"):
    ks = []
    for p in c.get_paginator("list_objects_v2").paginate(Bucket=A4_BUCKET, Prefix="portal/gold/mdpf/%s/%s/" % (scope, t)):
        ks += [(o["Key"], o["LastModified"]) for o in p.get("Contents", []) if o["Key"].endswith(".json")]
    return sorted(ks)


def load(c, bucket, key):
    return json.loads(c.get_object(Bucket=bucket, Key=key)["Body"].read())


def pick(c, t, date, source):
    """The newest dated key <= date for type t (A4), or the platinum served copy."""
    if source == "platinum":
        key = "platinum/mdpf/global/%s.json" % t
        h = c.head_object(Bucket=PLAT_BUCKET, Key=key)
        return load(c, PLAT_BUCKET, key), key, h["LastModified"].strftime("%Y-%m-%dT%H:%M:%SZ")
    ks = [k for k in a4_keys(c, t) if k[0].split("/")[-1][:-5] <= date]
    if not ks:
        raise SystemExit("no %s key at or before %s" % (t, date))
    key, lm = ks[-1]
    return load(c, A4_BUCKET, key), key, lm.strftime("%Y-%m-%dT%H:%M:%SZ")


def newest_date(c):
    return max(a4_keys(c, t)[-1][0].split("/")[-1][:-5] for t in A4_TYPES)


def r2(x):
    return None if x is None else round(float(x), 2)


def total_holdings(dist):
    tot = dist.get("total") or {}
    base = tot.get("account_count") or 0
    blend = {}
    for k, st in (dist.get("by_model") or {}).items():
        if canon(k) in BLEND_ARCHETYPES:
            blend[k] = st.get("account_count") or 0
    return {"total_account_count": base, "blend_counts": blend, "total_holdings": base + sum(blend.values())}


def cards(am):
    rows = []
    for m in am.get("by_model") or []:
        rows.append({"model": canon(m["model_name"]), "raw_name": m["model_name"], "aum": r2(m.get("aum") or 0),
                     "account_count": m.get("account_count") or 0})
    raw = {r["model"]: dict(r) for r in rows}
    out = {k: dict(v) for k, v in raw.items()}
    blends_in = {}
    for blend, targets in BLEND_ARCHETYPES.items():
        b = out.get(blend)
        if not b:
            continue
        blends_in[blend] = {"aum": b["aum"], "account_count": b["account_count"]}
        for t in targets:
            if t in out:
                out[t]["aum"] = r2(out[t]["aum"] + b["aum"] / 2)
                out[t]["account_count"] += b["account_count"]
            else:
                out[t] = {"model": t, "raw_name": b["raw_name"], "aum": r2(b["aum"] / 2), "account_count": b["account_count"]}
        del out[blend]
    return {"raw": raw, "rolled": out, "blends": blends_in}


def trend(ts):
    dates = ts.get("dates") or []
    series = {}
    for k, e in (ts.get("by_model") or {}).items():
        if e.get("cohort_class") == "sma":
            continue
        name = canon(e.get("display_name") or k)
        series[name] = list(e.get("model_value") or [None] * len(dates))
    for blend, targets in BLEND_ARCHETYPES.items():
        bs = series.pop(blend, None)
        if bs is None:
            continue
        for t in targets:
            half = [None if v is None else v / 2 for v in bs]
            if t not in series:
                series[t] = half
                continue
            series[t] = [h if a is None else (a if h is None else a + h) for a, h in zip(series[t], half)]
    nn = {n: sum(1 for v in s if v is not None) for n, s in series.items()}
    core_first = None
    for i, d in enumerate(dates):
        if any(series.get(c) and series[c][i] is not None for c in CORE):
            core_first = d
            break
    return {"series_count": len(series), "series": sorted(series), "dates_total": len(dates),
            "dates_with_values": nn, "first_core_value_date": core_first, "last_date": dates[-1] if dates else None}


def quarter_cells(am):
    out = {}
    for m in am.get("by_model") or []:
        name = canon(m["model_name"])
        if name not in CORE:
            continue
        out[name] = {}
        for q in ("q0", "q1", "q2", "q3"):
            c = m.get(q)
            absent = c is None or (c.get("change") is None and c.get("growth") is None and c.get("priorLevel") is None)
            out[name][q] = "absent" if absent else "present"
    return out


def is_folded(o):
    """True when the object carries the Global fold: the in-band statement or the Other Models line."""
    if (o.get("meta") or {}).get("by_model_fold"):
        return True
    bm = o.get("by_model")
    if isinstance(bm, dict):
        return any(k in ("other_models", "Other Models") for k in bm)
    if isinstance(bm, list):
        return any(isinstance(r, dict) and r.get("model_name") in ("Other Models", "other_models") for r in bm)
    return False


def compute(c, date, source):
    am, am_key, am_lm = pick(c, "aum-metrics", date, source)
    ds, ds_key, ds_lm = pick(c, "account-distribution", date, source)
    ts, ts_key, ts_lm = pick(c, "aggregate-aua-timeseries", date, source)
    folded = [t for t, o in (("aum-metrics", am), ("account-distribution", ds), ("aggregate-aua-timeseries", ts))
              if is_folded(o)]
    cq = quarter_cells(am)
    return {
        "objects": {"aum-metrics": [am_key, am_lm], "account-distribution": [ds_key, ds_lm],
                    "aggregate-aua-timeseries": [ts_key, ts_lm]},
        "folded_types": folded,
        "H": total_holdings(ds),
        "C": cards(am),
        "T": trend(ts),
        "Q": cq,
        "Q_absent_core": sum(1 for m in cq.values() for v in m.values() if v == "absent"),
        "Q_cells_core": sum(len(m) for m in cq.values()),
        "am_total": {k: am.get("total", {}).get(k) for k in ("aum", "account_count")},
    }


def platinum_equal(c, date):
    out = {}
    for t in A4_TYPES:
        try:
            pl, pkey, plm = pick(c, t, date, "platinum")
            a4, akey, _ = pick(c, t, date, "a4")
        except Exception as e:  # noqa: BLE001 -- a read failure is reported, never read as equal
            out[t] = "unread: %s" % str(e)[:60]
            continue
        strip = lambda d: {k: v for k, v in d.items() if k != "_provenance"}  # noqa: E731
        out[t] = "EQUAL to %s (platinum written %s)" % (akey.split("/")[-1], plm) if strip(pl) == strip(a4) else \
            "DIFFERS from %s (platinum written %s)" % (akey.split("/")[-1], plm)
    return out


def show(res, title):
    print("== %s" % title)
    for t, (k, lm) in res["objects"].items():
        print("  %-26s %-16s written %s" % (t, k.split("/")[-1], lm))
    print("  folded objects among them: %s" % (res["folded_types"] or "none (all unfolded)"))
    h = res["H"]
    print("H  Total Holdings headline: %s  (= total.account_count %s + blend counts %s)" %
          (h["total_holdings"], h["total_account_count"], h["blend_counts"] or "none"))
    print("C  archetype cards (aum, accounts):  AS THE PAGE SHOWS IT (after the blend roll-in)")
    for n, r in res["C"]["rolled"].items():
        raw = res["C"]["raw"].get(n)
        print("     %-18s %16.2f  %6d   raw before roll-in: %s" % (
            n, r["aum"], r["account_count"], ("%.2f / %d" % (raw["aum"], raw["account_count"])) if raw else "n/a (card is the roll-in only)"))
    print("   blends rolled in: %s" % (res["C"]["blends"] or "none"))
    t = res["T"]
    print("T  trend: %d model series after the blend roll; %d dates; first date a canonical model has a value: %s; last %s" %
          (t["series_count"], t["dates_total"], t["first_core_value_date"], t["last_date"]))
    print("   dates with a value per series: %s" % t["dates_with_values"])
    print("Q  core quarter cells absent: %d of %d" % (res["Q_absent_core"], res["Q_cells_core"]))
    for n in CORE:
        if n in res["Q"]:
            print("     %-18s %s" % (n, " ".join("%s=%s" % (q, v) for q, v in res["Q"][n].items())))


def table(b, a):
    rows = []
    rows.append(("Total Holdings", b["H"]["total_holdings"], a["H"]["total_holdings"]))
    for n in sorted(set(b["C"]["rolled"]) | set(a["C"]["rolled"])):
        rb, ra = b["C"]["rolled"].get(n), a["C"]["rolled"].get(n)
        rows.append(("card %s AUM" % n, rb["aum"] if rb else None, ra["aum"] if ra else None))
        rows.append(("card %s accounts" % n, rb["account_count"] if rb else None, ra["account_count"] if ra else None))
    rows.append(("trend series count", b["T"]["series_count"], a["T"]["series_count"]))
    rows.append(("trend first per-model date", b["T"]["first_core_value_date"], a["T"]["first_core_value_date"]))
    rows.append(("core quarter cells absent", b["Q_absent_core"], a["Q_absent_core"]))
    rows.append(("aum-metrics total.aum", b["am_total"]["aum"], a["am_total"]["aum"]))
    rows.append(("aum-metrics total.account_count", b["am_total"]["account_count"], a["am_total"]["account_count"]))
    print("%-44s %20s %20s %16s" % ("item", "BEFORE", "AFTER", "DELTA"))
    nonzero = 0
    for item, x, y in rows:
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            d = round(y - x, 2)
            ds = "%.2f" % d if isinstance(x, float) or isinstance(y, float) else str(int(d))
        else:
            d, ds = (0 if x == y else 1), ("0" if x == y else "changed")
        nonzero += 1 if d else 0
        print("%-44s %20s %20s %16s" % (item, x, y, ds))
    return nonzero


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pb = sub.add_parser("before")
    pb.add_argument("--source", choices=("a4", "platinum"), default="a4")
    pb.add_argument("--refresh", action="store_true", help="overwrite an existing pinned snapshot")
    pa = sub.add_parser("after")
    pa.add_argument("--date", default=None,
                    help="the run date D; optional: with no --date, D is the newest account-distribution key")
    pa.add_argument("--source", choices=("a4", "platinum"), default="a4")
    pa.add_argument("--before-date", default=None, help="recompute the before side at this date instead of the pinned snapshot")
    args = ap.parse_args(argv)
    c = s3()
    if args.cmd == "before":
        d = newest_date(c)
        res = compute(c, d, args.source)
        show(res, "BEFORE (newest dated global objects, run-date key %s, source %s)" % (d, args.source))
        print("platinum served copies vs the newest A4:")
        for t, v in platinum_equal(c, d).items():
            print("   %-26s %s" % (t, v))
        if res["folded_types"]:
            print("NOT PINNED: %s already carry the fold; this is not a before side." % res["folded_types"])
            return 1
        if os.path.exists(SNAP) and not args.refresh:
            print("snapshot already pinned at %s (use --refresh to overwrite)" % SNAP)
            return 0
        res["pinned_run_date_key"] = d
        json.dump(res, open(SNAP, "w", encoding="utf-8", newline="\n"), indent=1, sort_keys=True)
        print("pinned: %s" % SNAP)
        return 0
    # The newest account-distribution key is listed for the default date and, on the a4 source, for the newer-key WARN.
    newest = None
    if args.date is None or args.source == "a4":
        dist_keys = a4_keys(c, "account-distribution")
        newest = dist_keys[-1][0] if dist_keys else None
    if args.date is None:
        if newest is None:
            raise SystemExit("no account-distribution key under the A4 prefix: pass --date D")
        d_read, how = newest.split("/")[-1][:-5], "default: newest account-distribution key"
    else:
        d_read, how = args.date, "explicit"
    after = compute(c, d_read, args.source)
    objs = after["objects"]
    print("PORTFOLIOS-CARD READ date=%s (%s) account-distribution=%s aum-metrics=%s aggregate-aua-timeseries=%s"
          % (d_read, how, objs["account-distribution"][0], objs["aum-metrics"][0], objs["aggregate-aua-timeseries"][0]))
    if args.source == "a4" and newest is not None and newest.split("/")[-1][:-5] > d_read:
        print("WARN: a newer account-distribution key exists (%s); the objects after %s were NOT read"
              % (newest.split("/")[-1], d_read))
    if args.before_date:
        before = compute(c, args.before_date, args.source)
    elif os.path.exists(SNAP):
        before = json.load(open(SNAP, encoding="utf-8"))
    else:
        raise SystemExit("no pinned snapshot: run `before` first or pass --before-date")
    show(after, "AFTER (dated global objects at or before %s, source %s)" % (d_read, args.source))
    print()
    print("== BEFORE (pinned): %s" % {t: k[0].split("/")[-1] for t, k in before["objects"].items()})
    n = table(before, after)
    print("ROWS WITH A DELTA: %d" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
