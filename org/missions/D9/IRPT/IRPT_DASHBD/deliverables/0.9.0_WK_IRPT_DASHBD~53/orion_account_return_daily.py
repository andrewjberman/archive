"""IRPT_DASHBD reporting adapter for the ORION custody source -- `account_return_daily`, OFFLINE (TO-DB-b-72, TO-DB-b-76, FWD-11).

The Opal-shape daily total return (C-METHOD) for the firm whose custody data arrives through Orion, built through its OWN
adapter (C-ADAPTERS) and tied out like for like (C-TIEOUT) against Orion's own GROSS-of-fees return for the same window.

    r_t = (V_t - F_t) / V_(t-1) - 1          (the 49 Financial producer's method; GROSS of advisory fees)

  V_t   the account's value: the sum of the Orion position snapshot's current_value for the account on day t.
  F_t   net EXTERNAL flow over the calendar days in (previous trading day, t], capital-in positive (the skipped-day rule):
        the RATIFIED taxonomy's NNA contributions and distributions (data/inf/scripts/silver/orion_cashflow_taxonomy.yaml),
        plus the advisory fee added back (which is what makes the figure gross of fees).
  t-1   the previous TRADING day (lib/trading_calendar.py).

The two classes round 36 departed from the taxonomy on (the Internal Account Journal pair; Federal/State Tax Withheld) are
NOT flows here: they are read, counted and FLAGGED in the record, and their effect is probed beside the headline.

Every Orion type id and every vendor column is in orion_sources.json beside this file. The firm is not named in this file:
the run is given the registry key on its command line and everything else is derived from the registry. Orion's gross
figure and fee figures are read from the CSVs orion_gross_fee_pull.py landed in --scratch.

Usage (from the repo root):
  python <this file> --registry-key <key> --end YYYY-MM-DD --scratch .scratch --record <INF_GROSS_FEE_TIEOUT.json path>
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE
while ROOT != ROOT.parent and not (ROOT / "lib" / "opal_naming.py").is_file():
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT / "lib"))
import opal_naming  # noqa: E402
import trading_calendar as tc  # noqa: E402

DECLARATION = HERE / "orion_sources.json"
CONTRACT = ROOT / "org" / "standards" / "IRPT_DASHBD_ACCOUNT_RETURN_DAILY_CONTRACT.json"
SCHEMA_VERSION = "1.0"
METHOD_VERSION = 3
TOLERANCE_PP = 0.35
TRADING_DAYS_PER_YEAR = 252.0
HASH_SALT = "irpt-r36-orion"  # unchanged from round 36 so a hashed account key means the same account
FEE_RAIL_UNUSED = "FEE_RAIL_UNUSED"
PARQUET_TYPES = {"string": "string", "double": "float64", "int64": "int64"}

CLASSES = {
    "LINK_BROKEN_NO_BASE": "The geometric link breaks inside the window: at least one trading day has no return because the "
                           "prior-day value is absent or not positive (a closed, emptied or not yet funded account), so "
                           "nothing compounds across it.",
    "DEPARTURE_FLOW_CLASS": "Misses on the ratified flow set and lands within tolerance of Orion's gross figure once the two "
                            "departing classes (Internal Account Journal pair, Federal/State Tax Withheld) are treated as flows.",
    "OTHER_FEE_ADDBACK": "Misses on the ratified flow set and lands within tolerance once the Return-bucket trading and "
                         "administrative fees (Trading Expense, ADR Fee, Administrative Fee and Adjustment, Wire Fee) are added "
                         "back as well; the departing classes alone do not reach it.",
    "DEPARTURE_AND_OTHER_FEE": "Misses on the ratified set, and reaches tolerance only with both the departing classes and the "
                               "other fees applied.",
    "RESIDUAL_LARGE_FLOW": "No flow or fee variant reaches tolerance, and the window holds a single day whose flow is at least "
                           "10 percent of the prior value (timing of a large flow against the vendor's valuation).",
    "RESIDUAL_NO_LARGE_FLOW": "No flow or fee variant reaches tolerance and no day carries a large flow: the gap is not "
                              "explained by anything this adapter reads; its size is the evidence.",
}


def load_declaration():
    doc = json.loads(DECLARATION.read_bytes().decode("utf-8"))
    return doc


def hashed(account_id):
    return hashlib.sha256(("%s|%s" % (HASH_SALT, account_id)).encode("ascii")).hexdigest()[:16]


def resolve_scope(registry_key, src):
    """(firm, bucket) from the registry; the bucket is the routed legacy alias, never typed."""
    row = opal_naming.lookup(registry_key)
    firm = row.get("firm") or row.get("long")
    rule = src["bucket_resolution"]
    hits = []
    for alias in row.get("aliases", []):
        if rule["plane"] in alias.get("planes", []) and (alias.get("routed") or not rule["require_routed"]):
            hits.append(alias["spelling"])
    if len(hits) != 1:
        raise SystemExit("REFUSED: %d routed bucket alias(es) for registry key %r; exactly one is required"
                         % (len(hits), registry_key))
    return firm, hits[0], row.get("bucket")


def read_parquet(s3, bucket, key, columns=None):
    last = None
    for _ in range(4):
        try:
            body = s3.get_object(Bucket=bucket, Key=key)["Body"].read()
            return pd.read_parquet(io.BytesIO(body), columns=columns)
        except Exception as exc:  # noqa: BLE001 - retried, then raised
            last = exc
    raise SystemExit("REFUSED: read of %s failed after 4 tries: %r" % (key, last))


def snapshot_sums(s3, bucket, src, day):
    key = "%ssnapshot_date=%s/data.parquet" % (src["positions_prefix"], day)
    try:
        frame = read_parquet(s3, bucket, key, [src["account_column"], src["value_column"]])
    except SystemExit:
        return day, None
    sums = frame.groupby(src["account_column"])[src["value_column"]].sum(min_count=1)
    return day, sums


def fetch_values(s3, bucket, src, days, accounts, cache_path, workers):
    """Wide frame: index calendar day (str), columns account id (int), value float; absent = NaN."""
    have = {}
    if cache_path.is_file():
        old = pd.read_parquet(cache_path)
        for c in old.columns:
            have[c] = old[c]
    need = [d for d in days if d not in have]
    with ThreadPoolExecutor(workers) as ex:
        for day, sums in ex.map(lambda d: snapshot_sums(s3, bucket, src, d), need):
            if sums is None:
                have[day] = pd.Series(dtype="float64")
            else:
                have[day] = sums.astype("float64")
    store = pd.DataFrame({d: have[d] for d in sorted(have)})
    store.columns = [str(c) for c in store.columns]
    store.to_parquet(cache_path)
    wide = store.reindex(index=accounts, columns=days).T
    wide.index = days
    return wide


def classify_flow_rows(trn, src):
    """Orion transactions -> frame account, day, cls, amount (signed by the class). Refuses id/description drift."""
    types = src["types"]
    by_desc = {}
    by_id = {}
    for cls, entries in types.items():
        for entry in entries:
            by_desc[entry["desc"]] = cls
            if entry["id"] is not None:
                by_id[int(entry["id"])] = (cls, entry["desc"])
    dcol, icol = src["transactions_type_desc_column"], src["transactions_type_id_column"]
    trn = trn[trn[src["transactions_status_column"]].isin(src["accepted_status"])]
    trn = trn[trn[dcol].isin(by_desc)].copy()
    for tid, grp in trn.groupby(icol):
        if pd.isna(tid):
            continue
        want = by_id.get(int(tid))
        if want is not None and set(grp[dcol].unique()) != {want[1]}:
            raise SystemExit("REFUSED: type id %s carries descriptions %r, declared %r" % (tid, sorted(grp[dcol].unique()), want[1]))
    trn["cls"] = trn[dcol].map(by_desc)
    amt = pd.to_numeric(trn[src["transactions_amount_column"]], errors="coerce")
    sign = trn["cls"].map({"EXTERNAL_IN": 1.0, "EXTERNAL_OUT": -1.0, "INTER_ACCOUNT_IN": 1.0, "INTER_ACCOUNT_OUT": -1.0,
                           "TAX_WITHHELD": -1.0, "INCOME_CASH": 1.0})
    trn["amount"] = np.where(trn["cls"].isin(["ADVISORY_FEE", "OTHER_FEE"]), amt, amt.abs() * sign)
    trn["day"] = trn[src["transactions_date_column"]].astype(str).str[:10]
    trn["account"] = trn[src["transactions_account_column"]].astype("int64")
    return trn[["account", "day", "cls", "amount"]]


def calendar_matrix(flows, classes, days, accounts):
    """Cumulative sum over calendar days (rows) of the named classes, per account (columns)."""
    sel = flows[flows["cls"].isin(classes)]
    piv = sel.pivot_table(index="day", columns="account", values="amount", aggfunc="sum")
    piv = piv.reindex(index=days, columns=accounts).fillna(0.0)
    return np.cumsum(piv.to_numpy(dtype="float64"), axis=0)


def annualise(cum, years):
    base = np.maximum(1.0 + cum, 0.0)
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(years > 0, base ** (1.0 / years) - 1.0, np.nan)




def check_taxonomy(src):
    """The ratified flow set is read from the taxonomy file; the declaration must name exactly it as EXTERNAL_IN/OUT."""
    import yaml
    tax = yaml.safe_load((ROOT / src["taxonomy"]["path"]).read_bytes().decode("utf-8"))
    bucket = src["taxonomy"]["ratified_flow_bucket"]
    ratified = {x["type_desc"]: x["nna_direction"] for x in tax["types"] if x["bucket"] == bucket}
    declared = {}
    for cls, direction in (("EXTERNAL_IN", "in"), ("EXTERNAL_OUT", "out")):
        for entry in src["types"][cls]:
            declared[entry["desc"]] = direction
    if declared != ratified:
        raise SystemExit("REFUSED: declared flow set differs from the ratified taxonomy: only declared %r, only ratified %r"
                         % (sorted(set(declared.items()) - set(ratified.items())), sorted(set(ratified.items()) - set(declared.items()))))
    other = {x["type_desc"]: x["bucket"] for x in tax["types"]}
    placement = {}
    for cls in ("INTER_ACCOUNT_IN", "INTER_ACCOUNT_OUT", "TAX_WITHHELD", "ADVISORY_FEE", "OTHER_FEE", "INCOME_CASH"):
        placement[cls] = sorted({other.get(e["desc"], "ABSENT") for e in src["types"][cls]})
    return {"path": src["taxonomy"]["path"], "version": tax.get("version"), "ratified_flow_descriptions": len(ratified),
            "declared_equals_ratified": True, "bucket_of_declared_class": placement}


def parse_percent(series):
    return pd.to_numeric(series.astype(str).str.replace("%", "", regex=False).str.replace(",", "", regex=False).str.strip(), errors="coerce")


def parse_money(series):
    s = series.astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).str.strip()
    neg = s.str.startswith("(") | s.str.startswith("-")
    val = pd.to_numeric(s.str.replace("(", "", regex=False).str.replace(")", "", regex=False).str.replace("-", "", regex=False), errors="coerce")
    return val.where(~neg, -val)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry-key", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--scratch", required=True)
    ap.add_argument("--record", required=True)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args(argv)

    decl = load_declaration()
    src = decl["orion_fidelity"]
    cmp_ = decl["comparison"]
    gross_decl = cmp_["orion_account_performance_gross"]
    net_decl = cmp_["orion_account_performance_net_control"]
    fee_decl = decl["fee_sources"]
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    firm, bucket, _firm_bucket = resolve_scope(args.registry_key, src)
    s3 = boto3.client("s3", region_name="us-east-1")
    end = args.end
    taxonomy = check_taxonomy(src)

    # --- the sample: the landed account performance at the end snapshot (the accounts round 36 graded)
    perf = read_parquet(s3, bucket, "%ssnapshot_date=%s/data.parquet" % (net_decl["landed_prefix"], end))
    total_reported_rows = int(len(perf))
    perf = perf[perf[net_decl["landed_value_column"]].notna()].copy()
    perf["_start"] = perf["date_range_start"].astype(str).str[:10]
    perf["_end"] = perf["date_range_end"].astype(str).str[:10]
    if set(perf["_end"]) != {end}:
        raise SystemExit("REFUSED: window ends %r are not the snapshot %s" % (sorted(set(perf["_end"])), end))
    perf["account_id"] = perf["account_id"].astype("int64")
    perf = perf.drop_duplicates("account_id").set_index("account_id")
    accounts_all = [int(a) for a in perf.index]
    landed_net = perf[net_decl["landed_value_column"]].astype("float64") * 100.0

    # --- Orion's gross return for the same accounts and window, read live by orion_gross_fee_pull.py
    g = pd.read_csv(scratch / gross_decl["file"])
    if set(g[gross_decl["fee_method_column"]].dropna().unique()) != {gross_decl["fee_method_expected"]}:
        raise SystemExit("REFUSED: the gross file carries fee methods %r" % sorted(g[gross_decl["fee_method_column"]].dropna().unique()))
    g["_pp"] = parse_percent(g[gross_decl["value_column"]])
    g["_start"] = pd.to_datetime(g[gross_decl["window_start_column"]], format="%m/%d/%Y %I:%M %p").dt.strftime("%Y-%m-%d")
    g["_end"] = pd.to_datetime(g[gross_decl["window_end_column"]], format="%m/%d/%Y %I:%M %p").dt.strftime("%Y-%m-%d")
    g = g.drop_duplicates(gross_decl["account_column"]).set_index(gross_decl["account_column"])
    n = pd.read_csv(scratch / net_decl["file"])
    n["_pp"] = parse_percent(n[gross_decl["value_column"]])
    n = n.drop_duplicates(gross_decl["account_column"]).set_index(gross_decl["account_column"])
    have_gross = [a for a in accounts_all if a in g.index and not np.isnan(g.at[a, "_pp"])]
    without_gross = [a for a in accounts_all if a not in set(have_gross)]
    accounts = have_gross
    na = len(accounts)
    reported = g.loc[accounts, "_pp"].to_numpy(dtype="float64") / 100.0
    starts_live = g.loc[accounts, "_start"].tolist()
    ends_live = set(g.loc[accounts, "_end"])
    starts = perf.loc[accounts, "_start"].tolist()
    if starts_live != starts or ends_live != {end}:
        raise SystemExit("REFUSED: Orion's gross window (%s .. %s) is not the landed window (%s .. %s)" % (
            sorted(set(starts_live)), sorted(ends_live), sorted(set(starts)), end))

    # --- control: the unchanged (net) live read against the landed net figure
    live_net = n.loc[accounts, "_pp"].to_numpy(dtype="float64")
    drift = np.abs(live_net - landed_net.loc[accounts].to_numpy(dtype="float64"))
    net_control = {"accounts": na, "live_net_vs_landed_median_pp": round(float(np.nanmedian(drift)), 4),
                   "within_0.35pp": int((drift <= TOLERANCE_PP).sum()), "max_pp": round(float(np.nanmax(drift)), 4),
                   "meaning": "the live read (taken after the landed snapshot) of the SAME net-of-fee figure against the landed one"}

    # --- calendar and trading axes
    first_start = min(starts)
    load_from = (dt.date.fromisoformat(first_start) - dt.timedelta(days=10)).isoformat()
    days = [d.strftime("%Y-%m-%d") for d in pd.date_range(load_from, end)]
    didx = {d: i for i, d in enumerate(days)}
    tdays = [d.isoformat() for d in tc.trading_days_between(first_start, end)]
    prev_td = {d: tc.prev_trading_day(d).isoformat() for d in tdays}

    # --- inputs
    vals = fetch_values(s3, bucket, src, days, accounts, scratch / "orion_values_cache_gross.parquet", args.workers)
    absent_days = [d for d in days if vals.loc[d].isna().all()]
    V = vals.to_numpy(dtype="float64")
    trn = read_parquet(s3, bucket, src["transactions_key_template"].format(snapshot=end), src["transactions_columns"])
    flows = classify_flow_rows(trn, src)
    cum = {
        "ext": calendar_matrix(flows, ("EXTERNAL_IN", "EXTERNAL_OUT"), days, accounts),
        "journal": calendar_matrix(flows, ("INTER_ACCOUNT_IN", "INTER_ACCOUNT_OUT"), days, accounts),
        "tax": calendar_matrix(flows, ("TAX_WITHHELD",), days, accounts),
        "fee": calendar_matrix(flows, ("ADVISORY_FEE",), days, accounts),
        "ofee": calendar_matrix(flows, ("OTHER_FEE",), days, accounts),
        "income": calendar_matrix(flows, ("INCOME_CASH",), days, accounts),
    }

    nt = len(tdays)
    ti = np.array([didx[d] for d in tdays])
    pi = np.array([didx[prev_td[d]] for d in tdays])
    Vt, Vp = V[ti], V[pi]
    flow = {k: c[ti] - c[pi] for k, c in cum.items()}
    carried = (ti - pi).astype("int64")
    first_pos_idx = np.array([next((i for i in range(len(days)) if V[i, j] > 0), len(days)) for j in range(na)])
    start_arr = np.array(starts)
    tarr = np.array(tdays)
    in_window = (tarr[:, None] > start_arr[None, :])
    valid = (Vp > 0) & ~np.isnan(Vt) & ~np.isnan(Vp)

    def compound(parts):
        f = sum(flow[p] for p in parts)
        with np.errstate(divide="ignore", invalid="ignore"):
            fac = (Vt - f) / Vp
        prod = np.where(in_window & valid, fac, 1.0)
        return np.prod(prod, axis=0) - 1.0, (in_window & ~valid).sum(axis=0)

    ratified_gross = ("ext", "fee")
    years = in_window.sum(axis=0) / TRADING_DAYS_PER_YEAR
    cal_days = np.array([(dt.date.fromisoformat(end) - dt.date.fromisoformat(s)).days for s in starts], dtype="float64")
    variants = {"ratified_gross": ratified_gross, "plus_departing": ratified_gross + ("journal", "tax"),
                "plus_other_fees": ratified_gross + ("ofee",), "plus_departing_and_other_fees": ratified_gross + ("journal", "tax", "ofee")}
    ann = {}
    broken = None
    for label, parts in variants.items():
        cu, br = compound(parts)
        ann[label] = annualise(cu, years)
        if label == "ratified_gross":
            broken = br
    rep_pp = reported * 100.0
    computable = broken == 0
    gap = {k: np.abs(v * 100.0 - rep_pp) for k, v in ann.items()}
    within = {k: computable & (v <= TOLERANCE_PP) for k, v in gap.items()}

    # --- the output table: exactly the contract's columns, gross on the ratified flow set
    con = json.loads(CONTRACT.read_bytes().decode("utf-8"))
    columns = [c["name"] for c in con["columns"]]
    dtypes = {c["name"]: c["type"] for c in con["columns"]}
    f_gross = sum(flow[p] for p in ratified_gross)
    with np.errstate(divide="ignore", invalid="ignore"):
        r_all = (Vt - f_gross) / Vp - 1.0
        inc_ret = flow["income"] / Vp
        flow_ratio = np.abs(f_gross) / Vp
    rows = []
    for j, acct in enumerate(accounts):
        t0 = int(np.argmax(tarr >= start_arr[j]))
        for k in range(t0, nt):
            if np.isnan(Vt[k, j]) or didx[tdays[k]] < first_pos_idx[j]:
                continue
            ok = bool(valid[k, j])
            large = ok and bool(flow_ratio[k, j] >= src["large_flow_ratio"])
            rows.append((
                firm, str(acct).zfill(src["account_id_zero_pad"]), tdays[k], float(Vt[k, j]), float(f_gross[k, j]),
                float(flow["income"][k, j]), float(inc_ret[k, j]) if ok else None, float(r_all[k, j]) if ok else None,
                "TWR" if ok else "NOT_MEASURABLE", None, "NO_HOLDINGS_ROW", None, FEE_RAIL_UNUSED,
                ("LARGE_FLOW" if large else "MEASURED") if ok else "NOT_MEASURABLE",
                "NOT_GRADED_NO_NEIGHBOUR" if ok else "GUARD_NOT_REACHED", "PARTIAL_HISTORY", int(carried[k]),
                METHOD_VERSION, SCHEMA_VERSION))
    out = pd.DataFrame(rows, columns=columns)
    for name, typ in dtypes.items():
        out[name] = out[name].astype(PARQUET_TYPES[typ]) if typ != "string" else out[name].astype(object)
    out_path = scratch / "orion_account_return_daily_gross.parquet"
    out.to_parquet(out_path, index=False)
    output_columns = list(pd.read_parquet(out_path).columns)
    output_sha = hashlib.sha256(out_path.read_bytes()).hexdigest()

    # --- the tie-out and its misses
    max_flow = np.where(in_window & valid, flow_ratio, 0.0).max(axis=0)
    misses = []
    class_counts = Counter()
    for j, acct in enumerate(accounts):
        if within["ratified_gross"][j]:
            continue
        if not computable[j]:
            cls = "LINK_BROKEN_NO_BASE"
            evidence = {"days_without_return": int(broken[j]), "window_trading_days": int(in_window[:, j].sum())}
        elif within["plus_departing"][j]:
            cls = "DEPARTURE_FLOW_CLASS"
            evidence = {"gap_pp_with_departing_flows": round(float(gap["plus_departing"][j]), 4)}
        elif within["plus_other_fees"][j]:
            cls = "OTHER_FEE_ADDBACK"
            evidence = {"gap_pp_with_other_fees": round(float(gap["plus_other_fees"][j]), 4)}
        elif within["plus_departing_and_other_fees"][j]:
            cls = "DEPARTURE_AND_OTHER_FEE"
            evidence = {"gap_pp_with_both": round(float(gap["plus_departing_and_other_fees"][j]), 4)}
        else:
            cls = "RESIDUAL_LARGE_FLOW" if max_flow[j] >= src["large_flow_ratio"] else "RESIDUAL_NO_LARGE_FLOW"
            evidence = {"best_variant_gap_pp": round(float(min(gap[k][j] for k in gap)), 4),
                        "max_single_day_flow_to_base": round(float(max_flow[j]), 4)}
        class_counts[cls] += 1
        ours = None if not computable[j] else round(float(ann["ratified_gross"][j] * 100), 4)
        misses.append({"account": hashed(accounts[j]), "window": [starts[j], end], "ours_annualised_pct": ours,
                       "reported_annualised_pct": round(float(rep_pp[j]), 4),
                       "gap_pp": None if ours is None else round(abs(ours - float(rep_pp[j])), 4), "class": cls, "evidence": evidence})

    # --- probes: annualisation on the gross basis, and each flow variant, so every departure is reproducible
    annualisation_probe = {}
    for label, yrs in (("calendar_days_over_365", cal_days / 365.0), ("calendar_days_over_365.25", cal_days / 365.25),
                       ("trading_days_over_252", years)):
        row = {}
        for vlabel, parts in variants.items():
            cu, br = compound(parts)
            row[vlabel] = int(((br == 0) & (np.abs(annualise(cu, yrs) * 100.0 - rep_pp) <= TOLERANCE_PP)).sum())
        annualisation_probe[label] = row
    cu_net, _ = compound(("ext",))
    net_vs_gross_basis = {"opal_net_ratified_vs_orion_gross_within": int((computable & (np.abs(annualise(cu_net, years) * 100.0 - rep_pp) <= TOLERANCE_PP)).sum()),
                          "meaning": "Opal's NET compounding (fee left inside the return) against Orion's GROSS figure: the unlike-for-like pairing, printed so the gap the gross basis closes is visible"}

    # --- the departing classes, counted over the sample's rows in the window
    win_lo, win_hi = starts[0], end
    inside = flows[flows["account"].isin(accounts) & (flows["day"] > win_lo) & (flows["day"] <= win_hi)]
    dep = src["flow_sets"]["departing_classes"]
    flagged = []
    for name, members in dep.items():
        sel = inside[inside["cls"].isin(members)]
        descs = [e["desc"] for m in members for e in src["types"][m]]
        flagged.append({"class": name, "count": int(len(sel)), "accounts": int(sel["account"].nunique()), "descriptions": descs,
                        "ratified_bucket": sorted({b for m in members for b in taxonomy["bucket_of_declared_class"].get(m, [])}),
                        "treatment": "read and counted; NOT a flow in the headline (ratified taxonomy)",
                        "departure": src["inter_account_comment"] if name == "INTER_ACCOUNT_JOURNAL" else src["tax_withheld_comment"],
                        "window": [win_lo, win_hi], "status_filter": src["accepted_status"]})

    # --- fees: Orion's Advisory Fees Paid (Activity.Value, activityOptionId 11) over the same window, sliced
    fs = fee_decl["advisory_fees_paid"]
    uni = pd.read_csv(scratch / fs["file"]).drop_duplicates(fs["account_column"]).set_index(fs["account_column"])
    fee = parse_money(uni.reindex(accounts)[fs["value_column"]]).abs()
    fee.index = accounts
    sup = fee_decl["supervision"]
    am = read_parquet(s3, bucket, "%ssnapshot_date=%s/data.parquet" % (sup["prefix"], end), [sup["account_column"], sup["flag_column"]])
    am = am.drop_duplicates(sup["account_column"]).set_index(sup["account_column"])[sup["flag_column"]]
    flag_sup = pd.Series([am.get(a, np.nan) for a in accounts], index=accounts)
    bl = fee_decl["billing"]
    bdim = pd.read_csv(scratch / bl["file"]).drop_duplicates(bl["account_column"]).set_index(bl["account_column"])
    incl_all = bdim[bl["included_column"]].astype(str)
    incl = incl_all.reindex(accounts)
    bfee = parse_money(bdim.reindex(accounts)[bl["fee_amount_column"]])
    has_fee = fee.notna()
    sup_m = (flag_sup == True) & has_fee  # noqa: E712
    uns_m = (flag_sup == False) & has_fee  # noqa: E712
    bil_m = (incl == bl["included_values"]["billed"]) & has_fee
    unb_m = (incl == bl["included_values"]["unbilled"]) & has_fee
    broken_flag = ~incl.isin(list(bl["included_values"].values()))
    ledger = inside[inside["cls"] == "ADVISORY_FEE"].groupby("account")["amount"].sum().abs()
    fee_slices = {
        "supervised": round(float(fee[sup_m].sum()), 2), "unsupervised": round(float(fee[uns_m].sum()), 2),
        "supervision_total": round(float(fee[has_fee].sum()), 2),
        "billed": round(float(fee[bil_m].sum()), 2), "unbilled": round(float(fee[unb_m].sum()), 2),
        "billing_total": round(float(fee[has_fee].sum()), 2)}
    fee_detail = {
        "unit": "US dollars of advisory fees paid over the window, absolute value (Orion stores a fee as negative)",
        "window": [win_lo, win_hi], "accounts_in_sample": na,
        "accounts_with_a_fee_figure": int(has_fee.sum()), "accounts_without_a_fee_figure": int((~has_fee).sum()),
        "supervised_accounts": int(sup_m.sum()), "unsupervised_accounts": int(uns_m.sum()),
        "supervision_flag_unavailable_accounts": int((has_fee & flag_sup.isna()).sum()),
        "supervision_flag_unavailable_fees": round(float(fee[has_fee & flag_sup.isna()].sum()), 2),
        "supervision_basis": sup["basis"], "supervision_flag": "%s%s" % (sup["prefix"], sup["flag_column"]),
        "billed_accounts": int(bil_m.sum()), "unbilled_accounts": int(unb_m.sum()),
        "included_in_billing_flag_broken_in_sample": int(broken_flag.sum()),
        "included_in_billing_flag_broken_in_sample_with_a_fee": int((broken_flag & has_fee).sum()),
        "included_in_billing_flag_broken_fees": round(float(fee[broken_flag & has_fee].sum()), 2),
        "included_in_billing_flag_values_in_sample": {str(k): int(v) for k, v in incl.value_counts(dropna=False).items()},
        "included_in_billing_flag_broken_database_wide": {"broken": int((~incl_all.isin(list(bl["included_values"].values()))).sum()), "rows": int(len(incl_all))},
        "billing_fee_amount_sum_sample": round(float(bfee.abs().sum()), 2), "billing_fee_amount_accounts": int(bfee.notna().sum()),
        "billed_plus_unbilled_unreadable_note": "billed and unbilled are sums over the accounts whose flag Orion could read; the accounts with the flag broken are in included_in_billing_flag_broken_fees, so billed + unbilled + broken = billing_total",
        "by_bill_presence": {"accounts_with_a_bill_amount": int((bfee.fillna(0).abs() > 0).sum()), "fees_on_those_accounts": round(float(fee[(bfee.fillna(0).abs() > 0) & has_fee].sum()), 2),
                             "accounts_without": int((bfee.fillna(0).abs() == 0).sum()), "fees_on_those": round(float(fee[(bfee.fillna(0).abs() == 0) & has_fee].sum()), 2),
                             "meaning": "an alternative billed / unbilled cut that does not depend on the broken flag: an account has a Billing.FeeAmount or it has none"},
        "billing_fee_amount_meaning": "Billing.FeeAmount: the amount of the account's last bill cycle, a different quantity from fees paid over the window; printed beside, not substituted",
        "ledger_management_fee_and_credit_sum_sample": round(float(ledger.reindex(accounts).fillna(0).sum()), 2),
        "ledger_cross_check": "silver/transactions Management Fee plus Fee Credit rows (status Complete) for the same accounts and window, absolute net sum, against supervision_total"}
    fee_source = ("Orion Connect query API, saved query 'Unified Account Dim': Activity.Value with activityOptionId 11 (Advisory Fees Paid), "
                  "per account over the Rolling 3-Year window (PATH_DISCOVERY.md:181); billed / unbilled from Asset.IncludedInBilling of saved query 'Billing Dim' "
                  "(PATH_DISCOVERY.md:158); supervised / unsupervised from the account-level managed flag landed in silver/api_dims/accounts_v2 (inferred)")

    record = {
        "record_version": "1.0",
        "task_order": "IRPT_DASHBD.TO-DB-b-76",
        "source": "Orion Connect position snapshots (silver api_dims positions_mv, daily account value) and Orion transactions (silver, full-history snapshot %s), custodian Fidelity, read through the registry's routed legacy bucket alias" % end,
        "comparison_basis": "gross",
        "comparison_source": "Orion Connect query API (read-only), saved query 'Performance Dim' with the performance option's feeMethod overridden to Gross Of Fees: account-level TWR, Before-Tax, Gross of Fees, Annualized, window Rolling 3-Year (%s .. %s)" % (min(starts), end),
        "grain": "account-windows (one reported return per account over the source's own window)",
        "accounts": int(na),
        "denominator": int(na),
        "within": int(within["ratified_gross"].sum()),
        "tolerance_pp": TOLERANCE_PP,
        "comparison": "our total_return_daily (gross of the advisory fee, flows by the ratified taxonomy) compounded over the source's window, annualised by trading days / 252, against Orion's gross twr value, absolute gap in percentage points of the annual rate",
        "classes": list(CLASSES.keys()),
        "class_definitions": CLASSES,
        "class_counts": dict(class_counts),
        "misses": misses,
        "flagged_classes": flagged,
        "taxonomy": taxonomy,
        "fee_source": fee_source,
        "fee_slices": fee_slices,
        "fee_detail": fee_detail,
        "net_control": net_control,
        "output_columns": output_columns,
        "output_rows": int(len(out)),
        "output_sha256": output_sha,
        "sample": {
            "landed_rows_in_snapshot": total_reported_rows,
            "landed_with_value": len(accounts_all),
            "accounts_without_a_live_gross_figure": len(without_gross),
            "window_starts": [min(starts), max(starts)],
            "window_end": end,
            "window_trading_days_min_max": [int(in_window.sum(axis=0).min()), int(in_window.sum(axis=0).max())],
            "calendar_days_loaded": len(days),
            "calendar_days_with_no_snapshot_rows": absent_days,
            "accounts_funded_after_window_start": int(sum(1 for j in range(na) if first_pos_idx[j] > didx[starts[j]])),
        },
        "flow_variant_within": {k: int(v.sum()) for k, v in within.items()},
        "annualisation_probe": annualisation_probe,
        "unlike_for_like_pairing": net_vs_gross_basis,
        "flow_totals_rows": {k: int(v) for k, v in flows["cls"].value_counts().items()},
        "hash": "sha256(%s|account_id) first 16 hex" % HASH_SALT,
    }
    Path(args.record).write_text(json.dumps(record, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    print("OK: %d of %d account-windows within %.2f pp (gross vs gross) over %d account(s); misses by class %r"
          % (record["within"], record["denominator"], TOLERANCE_PP, record["accounts"], dict(class_counts)))
    print("OK: variants within %r" % record["flow_variant_within"])
    print("OK: flagged %r" % [(x["class"], x["count"], x["accounts"]) for x in flagged])
    print("OK: fee slices %r" % fee_slices)
    print("OK: output %d rows, %d columns, sha256 %s" % (len(out), len(output_columns), output_sha))


if __name__ == "__main__":
    main()
