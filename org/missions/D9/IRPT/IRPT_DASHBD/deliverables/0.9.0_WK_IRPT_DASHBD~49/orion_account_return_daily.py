"""IRPT_DASHBD reporting adapter for the ORION custody source -- `account_return_daily`, OFFLINE (TO-DB-b-72, FWD-11).

The Opal-shape daily total return (C-METHOD) for the firm whose custody data arrives through Orion, built through its OWN
adapter (C-ADAPTERS) and tied out against the source's own reported figures (C-TIEOUT). It reads S3 and writes only local
files. Nothing is served, and no byte goes back to S3.

    r_t = (V_t - F_t) / V_(t-1) - 1          (the 49 Financial producer's method; GROSS of advisory fees)

  V_t   the account's value: the sum of the Orion position snapshot's current_value for the account on day t.
  F_t   net EXTERNAL flow over the calendar days in (previous trading day, t], capital-in positive (the skipped-day rule):
        ratified NNA contributions and distributions, inter-account journals, tax withheld, and the advisory fee (added
        back, which is what makes the figure gross of fees).
  t-1   the previous TRADING day (lib/trading_calendar.py).

Every Orion type id and every vendor column is in orion_sources.json beside this file. The firm is not named in this file:
the run is given the registry key on its command line and everything else is derived from the registry.

Usage (from the repo root):
  python <this file> --registry-key <key> --end YYYY-MM-DD --scratch .scratch --record <INF_RETURNS_TIEOUT.json path>
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import re
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
METHOD_VERSION = 2
TOLERANCE_PP = 0.35
TRADING_DAYS_PER_YEAR = 252.0
HASH_SALT = "irpt-r36-orion"
FEE_RAIL_UNUSED = "FEE_RAIL_UNUSED"
PARQUET_TYPES = {"string": "string", "double": "float64", "int64": "int64"}

CLASSES = {
    "LINK_BROKEN_NO_BASE": "The geometric link breaks inside the window: at least one trading day has no return because the "
                           "prior-day value is absent or not positive (a closed, emptied or not yet funded account), so "
                           "nothing compounds across it.",
    "FEE_BASIS_GROSS_VS_NET": "Our figure is GROSS of advisory fees (contract) and the comparison source is NET of fees. The "
                              "gross figure misses, and the same inputs with the fee left inside the return land within "
                              "tolerance of the reported figure.",
    "NET_RESIDUAL_LARGE_FLOW": "The gross figure and the net-of-fee recomputation both miss, and the window holds a single day "
                               "whose flow is at least 10 percent of the prior value (timing of a large flow against the "
                               "vendor's valuation).",
    "NET_RESIDUAL_NO_LARGE_FLOW": "Both miss and no day carries a large flow: the gap is not explained by fee basis or by "
                                  "a large flow; its size on the net basis is the evidence.",
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
    trn["amount"] = np.where(trn["cls"] == "ADVISORY_FEE", amt, amt.abs() * sign)
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


def eclipse_lots_census(s3, bucket, src, snapshot, sample_accounts):
    """lots_status per sampled account from the Eclipse tables the firm already lands. Reads columns only."""
    pre = src["tables_prefix_template"].format(snapshot=snapshot)
    bpre = src["bronze_prefix_template"].format(snapshot=snapshot)
    pat = re.compile(src["lot_column_pattern"], re.I)
    inspected = []
    lot_tables = []
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=pre)
    for obj in resp.get("Contents", []):
        if not obj["Key"].endswith(".parquet"):
            continue
        body = s3.get_object(Bucket=bucket, Key=obj["Key"])["Body"].read()
        frame = pd.read_parquet(io.BytesIO(body))
        hits = [c for c in frame.columns if pat.search(str(c))]
        inspected.append({"table": obj["Key"].rsplit("/", 1)[-1], "rows": int(len(frame)), "columns": int(len(frame.columns)),
                          "lot_like_columns": hits})
        if hits:
            lot_tables.append(obj["Key"])
    bronze = [o["Key"].rsplit("/", 1)[-1] for o in s3.list_objects_v2(Bucket=bucket, Prefix=bpre).get("Contents", [])]
    bronze_lot_like = [b for b in bronze if pat.search(b)]
    status = {}
    for acct in sample_accounts:
        status[hashed(acct)] = "POPULATED" if lot_tables else "NO_LOTS"
    if lot_tables:
        raise SystemExit("STOP: lot-like column(s) found in %r; per-account lot rows must be read and counted before any "
                         "account is graded POPULATED" % lot_tables)
    return status, {"eclipse_tables_inspected": inspected, "eclipse_bronze_objects": len(bronze),
                    "eclipse_bronze_lot_like_names": bronze_lot_like, "eclipse_tables_with_lot_columns": 0}


def derived_lots_count(s3, bucket, accounts):
    """Context only: the firm's own FIFO lots built from transactions (not Eclipse); never promotes a status."""
    resp = s3.list_objects_v2(Bucket=bucket, Prefix="gold/lots/lots_latest.parquet")
    if not resp.get("Contents"):
        return None
    frame = read_parquet(s3, bucket, "gold/lots/lots_latest.parquet", ["account_id"])
    ids = set(int(a) for a in accounts)
    inside = frame[frame["account_id"].isin(ids)]
    return {"rows": int(len(inside)), "accounts_with_rows": int(inside["account_id"].nunique()),
            "origin": "derived FIFO from transactions by the firm's own gold script, not Eclipse tax lots"}


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
    cmp_ = decl["comparison"]["orion_account_performance"]
    lots_decl = decl["eclipse_lots"]
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    firm, bucket, _firm_bucket = resolve_scope(args.registry_key, src)
    s3 = boto3.client("s3", region_name="us-east-1")
    end = args.end

    # --- the reported source: Orion's own account-level performance at the end snapshot
    perf = read_parquet(s3, bucket, "%ssnapshot_date=%s/data.parquet" % (cmp_["prefix"], end))
    total_reported_rows = int(len(perf))
    perf = perf[perf[cmp_["value_column"]].notna()].copy()
    perf["_start"] = perf[cmp_["window_start_column"]].astype(str).str[:10]
    perf["_end"] = perf[cmp_["window_end_column"]].astype(str).str[:10]
    if set(perf["_end"]) != {end}:
        raise SystemExit("REFUSED: window ends %r are not the snapshot %s" % (sorted(set(perf["_end"])), end))
    perf[cmp_["account_column"]] = perf[cmp_["account_column"]].astype("int64")
    perf = perf.drop_duplicates(cmp_["account_column"]).set_index(cmp_["account_column"])
    accounts = [int(a) for a in perf.index]
    reported = perf[cmp_["value_column"]].astype("float64").to_numpy()
    starts = perf["_start"].tolist()
    methods = {c: sorted(perf[c].astype(str).unique()) for c in cmp_["method_columns"]}
    windows = sorted(perf[cmp_["window_name_column"]].astype(str).unique())

    # --- calendar and trading axes
    first_start = min(starts)
    load_from = (dt.date.fromisoformat(first_start) - dt.timedelta(days=10)).isoformat()
    days = [d.strftime("%Y-%m-%d") for d in pd.date_range(load_from, end)]
    didx = {d: i for i, d in enumerate(days)}
    tdays = [d.isoformat() for d in tc.trading_days_between(first_start, end)]
    prev_td = {}
    for d in tdays:
        prev_td[d] = tc.prev_trading_day(d).isoformat()

    # --- inputs
    vals = fetch_values(s3, bucket, src, days, accounts, scratch / "orion_values_cache.parquet", args.workers)
    absent_days = [d for d in days if vals.loc[d].isna().all()]
    V = vals.to_numpy(dtype="float64")
    trn = read_parquet(s3, bucket, src["transactions_key_template"].format(snapshot=end), src["transactions_columns"])
    flows = classify_flow_rows(trn, src)
    cum = {
        "ext": calendar_matrix(flows, ("EXTERNAL_IN", "EXTERNAL_OUT"), days, accounts),
        "journal": calendar_matrix(flows, ("INTER_ACCOUNT_IN", "INTER_ACCOUNT_OUT"), days, accounts),
        "tax": calendar_matrix(flows, ("TAX_WITHHELD",), days, accounts),
        "fee": calendar_matrix(flows, ("ADVISORY_FEE",), days, accounts),
        "income": calendar_matrix(flows, ("INCOME_CASH",), days, accounts),
    }

    # --- per trading day, per account: base, value, flow windows
    nt, na = len(tdays), len(accounts)
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

    def factors(parts):
        f = sum(flow[p] for p in parts) if parts else np.zeros_like(Vt)
        with np.errstate(divide="ignore", invalid="ignore"):
            return (Vt - f) / Vp

    def compound(parts):
        fac = factors(parts)
        used = in_window & valid
        prod = np.where(used, fac, 1.0)
        cumulative = np.prod(prod, axis=0) - 1.0
        broken = (in_window & ~valid).sum(axis=0)
        return cumulative, broken

    gross_parts = ("ext", "journal", "tax", "fee")
    net_parts = ("ext", "journal", "tax")
    years = in_window.sum(axis=0) / TRADING_DAYS_PER_YEAR
    cum_g, broken = compound(gross_parts)
    cum_n, _ = compound(net_parts)
    ann_g = annualise(cum_g, years)
    ann_n = annualise(cum_n, years)

    # --- the output table: exactly the contract's columns
    con = json.loads(CONTRACT.read_bytes().decode("utf-8"))
    columns = [c["name"] for c in con["columns"]]
    dtypes = {c["name"]: c["type"] for c in con["columns"]}
    fee_net_f = sum(flow[p] for p in gross_parts)
    with np.errstate(divide="ignore", invalid="ignore"):
        r_all = (Vt - fee_net_f) / Vp - 1.0
        inc_ret = flow["income"] / Vp
        flow_ratio = np.abs(fee_net_f) / Vp
    rows = []
    for j, acct in enumerate(accounts):
        t0 = int(np.argmax(tarr >= start_arr[j]))
        for k in range(t0, nt):
            if np.isnan(Vt[k, j]) or didx[tdays[k]] < first_pos_idx[j]:
                continue
            ok = bool(valid[k, j])
            large = ok and bool(flow_ratio[k, j] >= src["large_flow_ratio"])
            rows.append((
                firm, str(acct).zfill(src["account_id_zero_pad"]), tdays[k], float(Vt[k, j]), float(fee_net_f[k, j]),
                float(flow["income"][k, j]), float(inc_ret[k, j]) if ok else None, float(r_all[k, j]) if ok else None,
                "TWR" if ok else "NOT_MEASURABLE", None, "NO_HOLDINGS_ROW", None, FEE_RAIL_UNUSED,
                ("LARGE_FLOW" if large else "MEASURED") if ok else "NOT_MEASURABLE",
                "NOT_GRADED_NO_NEIGHBOUR" if ok else "GUARD_NOT_REACHED", "PARTIAL_HISTORY", int(carried[k]),
                METHOD_VERSION, SCHEMA_VERSION))
    out = pd.DataFrame(rows, columns=columns)
    for name, typ in dtypes.items():
        out[name] = out[name].astype(PARQUET_TYPES[typ]) if typ != "string" else out[name].astype(object)
    out_path = scratch / "orion_account_return_daily.parquet"
    out.to_parquet(out_path, index=False)
    written = pd.read_parquet(out_path)
    output_columns = list(written.columns)
    output_sha = hashlib.sha256(out_path.read_bytes()).hexdigest()

    # --- the tie-out
    rep_pp = reported * 100.0
    gap_g = np.abs(ann_g * 100.0 - rep_pp)
    gap_n = np.abs(ann_n * 100.0 - rep_pp)
    computable = broken == 0
    within_g = computable & (gap_g <= TOLERANCE_PP)
    within_n = computable & (gap_n <= TOLERANCE_PP)
    max_flow = np.where(in_window & valid, flow_ratio, 0.0).max(axis=0)
    misses = []
    class_counts = Counter()
    for j, acct in enumerate(accounts):
        if within_g[j]:
            continue
        if not computable[j]:
            cls = "LINK_BROKEN_NO_BASE"
            evidence = {"days_without_return": int(broken[j]), "window_trading_days": int(in_window[:, j].sum())}
        elif within_n[j]:
            cls = "FEE_BASIS_GROSS_VS_NET"
            evidence = {"net_basis_annualised_pct": round(float(ann_n[j] * 100), 4), "net_basis_gap_pp": round(float(gap_n[j]), 4)}
        else:
            cls = "NET_RESIDUAL_LARGE_FLOW" if max_flow[j] >= src["large_flow_ratio"] else "NET_RESIDUAL_NO_LARGE_FLOW"
            evidence = {"net_basis_annualised_pct": round(float(ann_n[j] * 100), 4), "net_basis_gap_pp": round(float(gap_n[j]), 4),
                        "max_single_day_flow_to_base": round(float(max_flow[j]), 4)}
        class_counts[cls] += 1
        ours = None if not computable[j] else round(float(ann_g[j] * 100), 4)
        misses.append({"account": hashed(acct), "window": [starts[j], end], "ours_annualised_pct": ours,
                       "reported_annualised_pct": round(float(rep_pp[j]), 4), "class": cls, "evidence": evidence})

    # --- probes (so the departures declared in the declaration are reproducible, not remembered)
    def probe_net(parts, yrs):
        cu, br = compound(parts)
        an = annualise(cu, yrs)
        return int(((br == 0) & (np.abs(an * 100.0 - rep_pp) <= TOLERANCE_PP)).sum())

    cal_days = np.array([(dt.date.fromisoformat(end) - dt.date.fromisoformat(s)).days for s in starts], dtype="float64")
    annualisation_probe = {}
    for label, yrs in (("calendar_days_over_365", cal_days / 365.0), ("calendar_days_over_365.25", cal_days / 365.25),
                       ("trading_days_over_252", years)):
        annualisation_probe[label] = {"net_basis_within": probe_net(net_parts, yrs),
                                      "gross_basis_within": probe_net(gross_parts, yrs)}
    flow_set_probe = {}
    for label, parts in (("ext_only", ("ext",)), ("ext_plus_journal", ("ext", "journal")),
                         ("ext_journal_tax", ("ext", "journal", "tax"))):
        flow_set_probe[label] = {"calendar_days_over_365_net_within": probe_net(parts, cal_days / 365.0),
                                 "trading_days_over_252_net_within": probe_net(parts, years)}

    # --- lots
    lots_status, lots_evidence = eclipse_lots_census(s3, bucket, lots_decl, end, accounts)
    lots_evidence["derived_fifo_lots_in_sample"] = derived_lots_count(s3, bucket, accounts)
    lots_evidence["status_census"] = dict(Counter(lots_status.values()))

    gaps_n = gap_n[computable]
    record = {
        "record_version": "1.0",
        "task_order": "IRPT_DASHBD.TO-DB-b-72",
        "source": "Orion Connect position snapshots (silver api_dims positions_mv, daily account value) and Orion transactions (silver, full-history snapshot %s), custodian Fidelity, read through the registry's routed legacy bucket alias" % end,
        "comparison_source": "Orion Connect account performance (silver api_dims performance, snapshot %s): account-level TWR, %s, %s, %s, %s, window %s" % (
            end, "/".join(methods["twr_calc_method"]), "/".join(methods["twr_tax_method"]), "/".join(methods["twr_fee_method"]),
            "/".join(methods["twr_annualized"]), "/".join(windows)),
        "grain": "account-windows (one reported return per account over the source's own window)",
        "accounts": int(na),
        "denominator": int(na),
        "within": int(within_g.sum()),
        "tolerance_pp": TOLERANCE_PP,
        "comparison": "our total_return_daily compounded over the source's window, annualised by trading days / 252, against twr_value, absolute gap in percentage points of the annual rate",
        "classes": list(CLASSES.keys()),
        "class_definitions": CLASSES,
        "class_counts": dict(class_counts),
        "misses": misses,
        "lots_status": lots_status,
        "lots_evidence": lots_evidence,
        "output_columns": output_columns,
        "output_rows": int(len(out)),
        "output_sha256": output_sha,
        "sample": {
            "reported_rows_in_snapshot": total_reported_rows,
            "reported_with_value": int(na),
            "window_starts": [min(starts), max(starts)],
            "window_end": end,
            "window_trading_days_min_max": [int(in_window.sum(axis=0).min()), int(in_window.sum(axis=0).max())],
            "calendar_days_loaded": len(days),
            "calendar_days_with_no_snapshot_rows": absent_days,
            "accounts_funded_after_window_start": int(sum(1 for j in range(na) if first_pos_idx[j] > didx[starts[j]])),
        },
        "net_basis": {
            "within_net_basis": int(within_n.sum()),
            "meaning": "the same inputs with the advisory fee left inside the return (NET), compared with the net-of-fee reported figure",
            "median_net_gap_pp_over_computable": round(float(np.median(gaps_n)), 4) if gaps_n.size else None,
        },
        "annualisation_probe": annualisation_probe,
        "flow_set_probe": flow_set_probe,
        "flow_totals_rows": {k: int(v) for k, v in flows["cls"].value_counts().items()},
        "reported_figure_methods": methods,
        "hash": "sha256(%s|account_id) first 16 hex" % HASH_SALT,
    }
    Path(args.record).write_text(json.dumps(record, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    print("OK: %d of %d account-windows within %.2f pp over %d account(s); misses by class %r; net-basis within %d"
          % (record["within"], record["denominator"], TOLERANCE_PP, record["accounts"], dict(class_counts), record["net_basis"]["within_net_basis"]))
    print("OK: output %d rows, %d columns, sha256 %s" % (len(out), len(output_columns), output_sha))
    print("OK: lots_status census %r" % lots_evidence["status_census"])


if __name__ == "__main__":
    main()
