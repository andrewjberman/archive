"""IRPT_DASHBD reporting adapter for the ORION custody source -- `account_return_daily`, OFFLINE (TO-DB-b-72, -76, -80, FWD-11).

The Opal-shape daily total return (C-METHOD) for the firm whose custody data arrives through Orion, built through its OWN
adapter (C-ADAPTERS) and tied out like for like (C-TIEOUT) on BOTH bases, each against a LANDED Orion figure:

    r_t = (V_t - F_t) / V_(t-1) - 1

  V_t   the account's value: the sum of the Orion position snapshot's current_value for the account on day t.
  F_t   net flow across the account's boundary over the calendar days in (previous trading day, t], capital-in positive (the
        skipped-day rule). The flow set is read from the RATIFIED taxonomy (data/inf/scripts/silver/orion_cashflow_taxonomy.yaml):
        every NNA entry (bucket NNA, nna_direction) plus every entry carrying `account_boundary` (in|out); an entry that also
        carries `account_boundary_when: before_tax_return` counts only because this run's basis IS before tax.
        NET basis: F_t is that set (the advisory fee stays inside the return); compared with the landed net twr_value.
        GROSS basis: the advisory fee (Management Fee, Fee Credit) is added back as capital out too; compared with the landed
        twr_gross_value of the DB-b-79 silver.
  t-1   the previous TRADING day (lib/trading_calendar.py).

There is ONE source of truth for the boundary classes, the taxonomy file: orion_sources.json names the ids of the tagged entries
and the run REFUSES when the file's tagged entries differ. No live Orion call is made: the gross comes from the landed silver
(address read from ORION_GROSS_SILVER.json), the net from the landed performance silver.

Usage (from the repo root):
  python <this file> --registry-key <key> --end YYYY-MM-DD --scratch .scratch --record <INF_TIEOUT_R38.json path>
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import sys
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
METHOD_VERSION = 4
TOLERANCE_PP = 0.35
BASIS = "before_tax_return"  # the basis the vendor figures are reported on (Before-Tax); qualifies account_boundary_when
TRADING_DAYS_PER_YEAR = 252.0
HASH_SALT = "irpt-r36-orion"  # unchanged from round 36 so a hashed account key means the same account
FEE_RAIL_UNUSED = "FEE_RAIL_UNUSED"
PARQUET_TYPES = {"string": "string", "double": "float64", "int64": "int64"}



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
    """The ratified flow sets are read from the taxonomy file; the declaration must name exactly them."""
    import yaml
    tc_ = src["taxonomy"]
    tax = yaml.safe_load((ROOT / tc_["path"]).read_bytes().decode("utf-8"))
    bucket = tc_["ratified_flow_bucket"]
    ratified = {x["type_desc"]: x["nna_direction"] for x in tax["types"] if x["bucket"] == bucket}
    declared = {}
    for cls, direction in (("EXTERNAL_IN", "in"), ("EXTERNAL_OUT", "out")):
        for entry in src["types"][cls]:
            declared[entry["desc"]] = direction
    if declared != ratified:
        raise SystemExit("REFUSED: declared flow set differs from the ratified taxonomy: only declared %r, only ratified %r"
                         % (sorted(set(declared.items()) - set(ratified.items())), sorted(set(ratified.items()) - set(declared.items()))))
    # account_boundary: (direction, qualifier) per tagged entry, read from the ratified file
    kb, kq = tc_["boundary_key"], tc_["boundary_qualifier_key"]
    tagged = {x["type_desc"]: (x[kb], x.get(kq)) for x in tax["types"] if kb in x}
    boundary_cls = {"INTER_ACCOUNT_IN": ("in", None), "INTER_ACCOUNT_OUT": ("out", None), "TAX_WITHHELD": ("out", tc_["boundary_basis_applied"])}
    declared_b = {}
    for cls, key in boundary_cls.items():
        for entry in src["types"][cls]:
            declared_b[entry["desc"]] = key
    if declared_b != tagged:
        raise SystemExit("REFUSED: declared boundary classes differ from the %s keys of the ratified taxonomy: only declared %r, only ratified %r"
                         % (kb, sorted(set(declared_b.items()) - set(tagged.items())), sorted(set(tagged.items()) - set(declared_b.items()))))
    other = {x["type_desc"]: x["bucket"] for x in tax["types"]}
    placement = {}
    for cls in ("INTER_ACCOUNT_IN", "INTER_ACCOUNT_OUT", "TAX_WITHHELD", "ADVISORY_FEE", "OTHER_FEE", "INCOME_CASH"):
        placement[cls] = sorted({other.get(e["desc"], "ABSENT") for e in src["types"][cls]})
    return {"path": tc_["path"], "version": tax.get("version"), "types_entries": len(tax["types"]),
            "ratified_flow_descriptions": len(ratified), "declared_equals_ratified": True,
            "account_boundary_entries": {k: {"account_boundary": v[0], "account_boundary_when": v[1]} for k, v in sorted(tagged.items())},
            "declared_equals_account_boundary_keys": True, "bucket_of_declared_class": placement}


def read_landed_gross(s3, gross_decl):
    """The landed gross silver of DB-b-79: the address and as_of are read from its record, never typed."""
    rec = json.loads((ROOT / gross_decl["landed_record"]).read_bytes().decode("utf-8"))
    addr = rec[gross_decl["landed_address_key"]]
    if not addr.startswith("s3://") or "/silver/" not in addr:
        raise SystemExit("REFUSED: landed gross address %r is not an s3 silver address" % addr)
    bucket, _, prefix = addr[len("s3://"):].partition("/")
    frame = read_parquet(s3, bucket, "%s/%s" % (prefix, gross_decl["object"]))
    return addr, rec[gross_decl["as_of_key"]], frame


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
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    firm, bucket, _firm_bucket = resolve_scope(args.registry_key, src)
    s3 = boto3.client("s3", region_name="us-east-1")
    end = args.end
    taxonomy = check_taxonomy(src)

    # --- the NET figure: the landed account performance at the end snapshot (the accounts round 36 graded)
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

    # --- the GROSS figure: the landed gross silver, same accounts and window
    gross_addr, gross_as_of, g = read_landed_gross(s3, gross_decl)
    if gross_as_of != end:
        raise SystemExit("REFUSED: landed gross as_of %r is not the snapshot %s" % (gross_as_of, end))
    if set(g[gross_decl["fee_method_column"]].dropna().unique()) != {gross_decl["fee_method_expected"]}:
        raise SystemExit("REFUSED: the gross silver carries fee methods %r" % sorted(g[gross_decl["fee_method_column"]].dropna().unique()))
    g["_pp"] = pd.to_numeric(g[gross_decl["value_column"]], errors="coerce")
    g["_start"] = g[gross_decl["window_start_column"]].astype(str).str[:10]
    g["_end"] = g[gross_decl["window_end_column"]].astype(str).str[:10]
    g[gross_decl["account_column"]] = g[gross_decl["account_column"]].astype("int64")
    g = g.drop_duplicates(gross_decl["account_column"]).set_index(gross_decl["account_column"])
    have_gross = [a for a in accounts_all if a in g.index and not np.isnan(g.at[a, "_pp"])]
    without_gross = [a for a in accounts_all if a not in set(have_gross)]
    accounts = have_gross  # ONE sample for both bases
    na = len(accounts)
    reported_gross_pp = g.loc[accounts, "_pp"].to_numpy(dtype="float64")
    reported_net_pp = landed_net.loc[accounts].to_numpy(dtype="float64")
    starts_gross = g.loc[accounts, "_start"].tolist()
    starts = perf.loc[accounts, "_start"].tolist()
    if starts_gross != starts or set(g.loc[accounts, "_end"]) != {end}:
        raise SystemExit("REFUSED: the landed gross window (%s .. %s) is not the landed net window (%s .. %s)" % (
            sorted(set(starts_gross)), sorted(set(g.loc[accounts, "_end"])), sorted(set(starts)), end))

    # --- calendar and trading axes
    first_start = min(starts)
    load_from = (dt.date.fromisoformat(first_start) - dt.timedelta(days=10)).isoformat()
    days = [d.strftime("%Y-%m-%d") for d in pd.date_range(load_from, end)]
    didx = {d: i for i, d in enumerate(days)}
    tdays = [d.isoformat() for d in tc.trading_days_between(first_start, end)]
    prev_td = {d: tc.prev_trading_day(d).isoformat() for d in tdays}

    # --- inputs
    vals = fetch_values(s3, bucket, src, days, accounts, scratch / "orion_values_cache_r38.parquet", args.workers)
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

    # the headline flow sets are the ratified file's: NNA entries + account_boundary entries (tax pair on the before-tax basis)
    fs = src["flow_sets"]
    part_of = {"EXTERNAL_IN": "ext", "EXTERNAL_OUT": "ext", "INTER_ACCOUNT_IN": "journal", "INTER_ACCOUNT_OUT": "journal",
               "TAX_WITHHELD": "tax", "ADVISORY_FEE": "fee"}
    net_parts = tuple(sorted({part_of[c] for c in fs["ratified_net"]}))
    gross_parts = tuple(sorted({part_of[c] for c in fs["ratified_gross"]}))
    nna_only = tuple(sorted({part_of[c] for c in fs["nna_only_reference"]}))
    years = in_window.sum(axis=0) / TRADING_DAYS_PER_YEAR
    cal_days = np.array([(dt.date.fromisoformat(end) - dt.date.fromisoformat(s)).days for s in starts], dtype="float64")
    cu_net, br = compound(net_parts)
    cu_gross, _ = compound(gross_parts)
    computable = br == 0
    gap_net = np.abs(annualise(cu_net, years) * 100.0 - reported_net_pp)
    gap_gross = np.abs(annualise(cu_gross, years) * 100.0 - reported_gross_pp)
    within_net = computable & (gap_net <= TOLERANCE_PP)
    within_gross = computable & (gap_gross <= TOLERANCE_PP)

    # --- the output table: exactly the contract's columns, gross on the ratified flow set
    con = json.loads(CONTRACT.read_bytes().decode("utf-8"))
    columns = [c["name"] for c in con["columns"]]
    dtypes = {c["name"]: c["type"] for c in con["columns"]}
    f_gross = sum(flow[p] for p in gross_parts)
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
    out_path = scratch / "orion_account_return_daily_r38.parquet"
    out.to_parquet(out_path, index=False)
    output_columns = list(pd.read_parquet(out_path).columns)
    output_sha = hashlib.sha256(out_path.read_bytes()).hexdigest()

    # --- probes: the same sample with the NNA-only set (before the account_boundary keys) and the annualisation choices
    def within_of(parts, yrs, reported):
        cu, b = compound(parts)
        return int(((b == 0) & (np.abs(annualise(cu, yrs) * 100.0 - reported) <= TOLERANCE_PP)).sum())

    flow_set_probe = {
        "net": {"nna_only": within_of(nna_only, years, reported_net_pp), "with_account_boundary": int(within_net.sum())},
        "gross": {"nna_only_plus_fee": within_of(nna_only + ("fee",), years, reported_gross_pp), "with_account_boundary_plus_fee": int(within_gross.sum())}}
    annualisation_probe = {}
    for label, yrs in (("calendar_days_over_365", cal_days / 365.0), ("calendar_days_over_365.25", cal_days / 365.25),
                       ("trading_days_over_252", years)):
        annualisation_probe[label] = {"net": within_of(net_parts, yrs, reported_net_pp), "gross": within_of(gross_parts, yrs, reported_gross_pp)}
    unlike = {"net_compounding_vs_landed_gross_within": within_of(net_parts, years, reported_gross_pp),
              "meaning": "Opal's NET compounding (fee left inside the return) against Orion's GROSS figure: the unlike-for-like pairing, printed so the gap the gross basis closes is visible"}

    # --- the boundary classes, counted over the sample's rows in the window
    win_lo, win_hi = min(starts), end
    inside = flows[flows["account"].isin(accounts) & (flows["day"] > win_lo) & (flows["day"] <= win_hi)]
    flagged = []
    for name, members in fs["boundary_classes"].items():
        sel = inside[inside["cls"].isin(members)]
        flagged.append({"class": name, "count": int(len(sel)), "accounts": int(sel["account"].nunique()),
                        "descriptions": [e["desc"] for m in members for e in src["types"][m]],
                        "ratified_bucket": sorted({b for m in members for b in taxonomy["bucket_of_declared_class"].get(m, [])}),
                        "treatment": "a flow in the headline, by the ratified account_boundary key (read from the taxonomy file)",
                        "window": [win_lo, win_hi], "status_filter": src["accepted_status"]})

    record = {
        "record_version": "1.0",
        "task_order": "IRPT_DASHBD.TO-DB-b-80",
        "source": "Orion Connect position snapshots (silver api_dims positions_mv, daily account value) and Orion transactions (silver, full-history snapshot %s), custodian Fidelity, read through the registry's routed legacy bucket alias" % end,
        "gross_source": gross_addr,
        "as_of": gross_as_of,
        "net_source": "s3://%s/%ssnapshot_date=%s/data.parquet (column %s, landed)" % (bucket, net_decl["landed_prefix"], end, net_decl["landed_value_column"]),
        "grain": "account-windows (one reported return per account over the source's own window)",
        "tolerance_pp": TOLERANCE_PP,
        "accounts": int(na),
        "gross": {"denominator": int(na), "within": int(within_gross.sum()), "flow_set": list(fs["ratified_gross"])},
        "net": {"denominator": int(na), "within": int(within_net.sum()), "flow_set": list(fs["ratified_net"])},
        "comparison": "our total_return_daily compounded over the source's window, annualised by trading days / 252, against the landed Orion figure of the same basis; absolute gap in percentage points of the annual rate; ONE sample for both bases; flows by the ratified taxonomy including its account_boundary keys (tax pair on the before-tax basis)",
        "not_computable_link_broken": int((~computable).sum()),
        "flow_set_probe": flow_set_probe,
        "taxonomy": taxonomy,
        "boundary_classes": flagged,
        "annualisation_probe": annualisation_probe,
        "unlike_for_like_pairing": unlike,
        "output_columns": output_columns,
        "output_rows": int(len(out)),
        "output_sha256": output_sha,
        "sample": {
            "landed_net_rows_in_snapshot": total_reported_rows,
            "landed_net_with_value": len(accounts_all),
            "accounts_without_a_landed_gross_figure": len(without_gross),
            "window_starts": [min(starts), max(starts)],
            "window_end": end,
            "window_trading_days_min_max": [int(in_window.sum(axis=0).min()), int(in_window.sum(axis=0).max())],
            "calendar_days_loaded": len(days),
            "calendar_days_with_no_snapshot_rows": absent_days,
            "accounts_funded_after_window_start": int(sum(1 for j in range(na) if first_pos_idx[j] > didx[starts[j]])),
        },
        "flow_totals_rows": {k: int(v) for k, v in flows["cls"].value_counts().items()},
        "hash": "sha256(%s|account_id) first 16 hex" % HASH_SALT,
    }
    Path(args.record).write_text(json.dumps(record, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    print("OK: gross %d of %d, net %d of %d within %.2f pp over %d account(s); gross from %s as of %s"
          % (record["gross"]["within"], na, record["net"]["within"], na, TOLERANCE_PP, na, gross_addr, gross_as_of))
    print("OK: flow-set probe %r" % flow_set_probe)
    print("OK: boundary classes %r" % [(x["class"], x["count"], x["accounts"]) for x in flagged])
    print("OK: output %d rows, %d columns, sha256 %s" % (len(out), len(output_columns), output_sha))


if __name__ == "__main__":
    main()
