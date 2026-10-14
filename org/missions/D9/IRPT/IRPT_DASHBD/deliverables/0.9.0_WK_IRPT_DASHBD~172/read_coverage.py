"""DB-b-212 read script (IRPT_DASHBD round 108, worker 0.9.0_WK_IRPT_DASHBD~172).

Read-only. Two reads that decide Inflection's coverage words:
  Read A  do Orion's returns include dividends (one account chosen by a hash rule, one window)?
  Read B  are Eclipse tax lots populated (lot-level fields in the Eclipse silver tables)?
Reads only under the two granted Inflection prefixes. Holds no write call and names no other firm.
Prints counts, decisions and words only; no account id, name, dollar figure or percentage is printed
(the chosen account is named by the sha256 of its id only).

Usage: python -I read_coverage.py <repo_root>
"""
import datetime as dt
import hashlib
from decimal import Decimal
import io
import json
import re
import sys
from pathlib import Path

import boto3
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
import yaml

BUCKET = "opal-data-assets"
GRANTED = ("s3://opal-data-assets/orion/inflection/", "s3://opal-data-assets/eclipse/inflection/")
ORION_SILVER = "s3://opal-data-assets/orion/inflection/silver/"
ECLIPSE_SILVER = "s3://opal-data-assets/eclipse/inflection/silver/"
ECLIPSE_RECON = "s3://opal-data-assets/eclipse/inflection/reconstructed/"
ECLIPSE_META = "s3://opal-data-assets/eclipse/inflection/meta/"
ECLIPSE_TABLES = ("fact_model_composition", "fact_models", "fact_portfolios_full", "fact_portfolios_simple")
TAXONOMY_REL = "data/inf/scripts/silver/orion_cashflow_taxonomy.yaml"
INCOME_RE = re.compile(r"(?i)dividend|income|interest")
TAX_RE = re.compile(r"(?i)tax")
LOT_RE = re.compile(r"(?i)lot|acqui|cost_?basis|open_?date")
DATE_RE = re.compile(r"/date=(\d{4}-\d{2}-\d{2})/")
CLIENT = boto3.client("s3")
CALLS = {"list": 0, "get": 0}


def key_of(uri):
    assert any(uri.startswith(g) for g in GRANTED), "not a granted prefix: %s" % uri
    return uri[len("s3://%s/" % BUCKET):]


def list_keys(uri):
    keys = []
    for page in CLIENT.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=key_of(uri)):
        CALLS["list"] += 1
        keys += [o["Key"] for o in page.get("Contents", [])]
    return keys


def partitions(uri):
    """date -> object key, one data partition per date under a granted silver prefix."""
    out = {}
    for k in list_keys(uri):
        m = DATE_RE.search(k)
        if m:
            out.setdefault(m.group(1), k)
    return out


def get_bytes(key):
    CALLS["get"] += 1
    return CLIENT.get_object(Bucket=BUCKET, Key=key)["Body"].read()


def read_table(key, columns=None):
    return pq.read_table(io.BytesIO(get_bytes(key)), columns=columns)


def day_runs(dates):
    """maximal runs of consecutive calendar days among ISO date strings."""
    ds = [dt.date.fromisoformat(x) for x in sorted(dates)]
    out, cur = [], []
    for d in ds:
        if cur and (d - cur[-1]).days == 1:
            cur.append(d)
        else:
            if cur:
                out.append(cur)
            cur = [d]
    if cur:
        out.append(cur)
    return out


def taxonomy_maps(root):
    tax = yaml.safe_load((root / TAXONOMY_REL).read_bytes().decode("utf-8"))
    ent = {e["type_desc"]: e for e in tax["types"] if isinstance(e, dict) and e.get("type_desc")}
    nna_in = {k for k, e in ent.items() if e.get("bucket") == "NNA" and e.get("nna_direction") == "in"}
    nna_out = {k for k, e in ent.items() if e.get("bucket") == "NNA" and e.get("nna_direction") == "out"}
    income_ret = {k for k, e in ent.items() if e.get("bucket") == "Return" and INCOME_RE.search(k) and not TAX_RE.search(k)}
    return nna_in, nna_out, income_ret, len(ent)


def orion_read(root):
    nna_in, nna_out, income_ret, n_tax = taxonomy_maps(root)
    res = {"taxonomy_types": n_tax, "nna_in_types": len(nna_in), "nna_out_types": len(nna_out), "income_removal_types": sorted(income_ret)}

    # ---- A1: the transaction universe (newest cumulative partition) and the income-type column
    tparts = partitions(ORION_SILVER + "fact_transactions/")
    newest_t = max(tparts)
    t = read_table(tparts[newest_t], ["accountId", "clientId", "transDate", "transAmount", "transTypeId",
                                      "transactionDescription", "status"])
    res["txn_partition"] = newest_t
    res["txn_rows"] = t.num_rows
    desc_all = t["transactionDescription"].to_pylist()
    income_desc = {d for d in set(desc_all) if d and INCOME_RE.search(d) and not TAX_RE.search(d)}
    res["income_descriptions"] = sorted(income_desc)
    complete = pc.equal(t["status"], "Complete")
    inc_mask = pc.and_(pc.is_in(t["transactionDescription"], value_set=pa_array(income_desc)), complete)
    cand = set(t["accountId"].filter(inc_mask).to_pylist())
    res["accounts_with_income_transactions"] = len(cand)
    hashes = sorted((hashlib.sha256(str(a).encode("utf-8")).hexdigest(), a) for a in cand)
    chosen_hash, chosen = hashes[0]
    res["account_ref_sha256"] = chosen_hash
    acct_mask = pc.and_(pc.equal(t["accountId"], chosen), complete)
    at = t.filter(acct_mask)
    res["account_transactions_complete"] = at.num_rows
    res["account_income_transactions_all_time"] = at.filter(pc.is_in(at["transactionDescription"], value_set=pa_array(income_desc))).num_rows
    client_ids = set(at["clientId"].to_pylist())
    res["account_client_ids"] = len(client_ids)
    client = sorted(client_ids)[0] if client_ids else None

    # ---- A2: the window both tables cover. The performance partitions are cumulative: the newest one
    # carries the client's factor for every date it covers, so one read serves the whole window.
    pparts = partitions(ORION_SILVER + "fact_positions/")
    qparts = partitions(ORION_SILVER + "fact_performance/")
    newest_q = max(qparts)
    pt_q = read_table(qparts[newest_q], ["client_id", "date", "factor"])
    res["perf_partition"] = newest_q
    res["perf_partitions_listed"] = len(qparts)
    perf_client = pt_q.filter(pc.equal(pt_q["client_id"], client)) if client is not None else pt_q.slice(0, 0)
    fac_all = {}
    for dte, f in zip(perf_client["date"].to_pylist(), perf_client["factor"].to_pylist()):
        if f is not None:
            fac_all[dte] = f
    both = sorted(set(pparts) & set(fac_all))
    runs = [r for r in day_runs(both) if len(r) >= 2]
    if not runs:
        res["window"] = "NONE: no unbroken run of two or more days covered by both tables for the client"
        return res
    win = max(runs, key=lambda r: (len(r), r[-1]))
    dates = [d.isoformat() for d in win]
    res["window_days"] = len(dates)
    res["window_start"] = dates[0]
    res["window_end"] = dates[-1]
    res["window_positions_partitions"] = len(pparts)
    res["performance_dates_for_client"] = len(fac_all)

    # ---- A3: daily market values of the account (positions partitions of the window)
    V = {}
    Vc = {}
    client_accts = sorted(set(t.filter(pc.equal(t["clientId"], client))["accountId"].to_pylist())) if client is not None else []
    cset = pa.array(client_accts, type=pa.int64())
    for d in dates:
        pt = read_table(pparts[d], ["accountId", "currentValue"])
        V[d] = pc.sum(pt["currentValue"].filter(pc.equal(pt["accountId"], chosen))).as_py() or 0.0
        Vc[d] = pc.sum(pt["currentValue"].filter(pc.is_in(pt["accountId"], value_set=cset))).as_py() or 0.0
    # the window is the longest unbroken run inside that stretch on which the account carries a positive value
    pos_runs = []
    cur = []
    for d in dates:
        if V[d] > 0:
            cur.append(d)
        else:
            if len(cur) >= 2:
                pos_runs.append(cur)
            cur = []
    if len(cur) >= 2:
        pos_runs.append(cur)
    res["positive_value_runs_in_coverage"] = len(pos_runs)
    if not pos_runs:
        res["window"] = "NONE: no unbroken run of two or more days with a positive account value inside the coverage"
        return res
    dates = max(pos_runs, key=lambda r: (len(r), r[-1]))
    res["window_days"] = len(dates)
    res["window_start"] = dates[0]
    res["window_end"] = dates[-1]
    res["client_accounts_in_transactions"] = len(set(t.filter(pc.equal(t["clientId"], client))["accountId"].to_pylist())) if client is not None else 0

    # ---- A4: daily external flows (NNA, by taxonomy direction) and income removed for the WITHOUT figure
    F = {d: 0.0 for d in dates}
    Inc = {d: 0.0 for d in dates}
    n_txn = 0
    n_div = 0
    unmapped = set()
    dset = set(dates)
    for tr_date, desc, amt, st in zip(at["transDate"].to_pylist(), at["transactionDescription"].to_pylist(),
                                      at["transAmount"].to_pylist(), at["status"].to_pylist()):
        if tr_date not in dset or amt is None:
            continue
        n_txn += 1
        if desc in nna_in:
            F[tr_date] += abs(amt)
        elif desc in nna_out:
            F[tr_date] -= abs(amt)
        elif desc in income_ret:
            Inc[tr_date] += amt
            n_div += 1
        elif desc not in ent_names(root):
            unmapped.add(desc)
    res["transactions_checked"] = n_txn
    res["dividend_flows"] = n_div
    res["unmapped_description_types_in_window"] = len(unmapped)

    # ---- A5: daily returns with and without income, linked over the window
    r_with, r_without, skipped = [], [], 0
    for prev, d in zip(dates[:-1], dates[1:]):
        if V[prev] <= 0:
            skipped += 1
            continue
        r_with.append((V[d] - F[d]) / V[prev] - 1.0)
        r_without.append((V[d] - F[d] - Inc[d]) / V[prev] - 1.0)
    res["days_skipped_nonpositive_base"] = skipped
    res["days_linked"] = len(r_with)
    R_with = 1.0
    for r in r_with:
        R_with *= 1.0 + r
    R_without = 1.0
    for r in r_without:
        R_without *= 1.0 + r
    R_with -= 1.0
    R_without -= 1.0

    # ---- A5b: the same two figures for ALL the client's accounts together (the performance table is keyed by client)
    ct = t.filter(pc.and_(pc.is_in(t["accountId"], value_set=cset), complete))
    Fc = {d: 0.0 for d in dates}
    Ic = {d: 0.0 for d in dates}
    n_div_c = 0
    for tr_date, desc, amt in zip(ct["transDate"].to_pylist(), ct["transactionDescription"].to_pylist(),
                                  ct["transAmount"].to_pylist()):
        if tr_date not in dset or amt is None:
            continue
        if desc in nna_in:
            Fc[tr_date] += abs(amt)
        elif desc in nna_out:
            Fc[tr_date] -= abs(amt)
        elif desc in income_ret:
            Ic[tr_date] += amt
            n_div_c += 1
    rc_with, rc_without, skipped_c = [], [], 0
    for prev, d in zip(dates[:-1], dates[1:]):
        if Vc[prev] <= 0:
            skipped_c += 1
            continue
        rc_with.append((Vc[d] - Fc[d]) / Vc[prev] - 1.0)
        rc_without.append((Vc[d] - Fc[d] - Ic[d]) / Vc[prev] - 1.0)
    Rc_with = 1.0
    for r in rc_with:
        Rc_with *= 1.0 + r
    Rc_without = 1.0
    for r in rc_without:
        Rc_without *= 1.0 + r
    Rc_with -= 1.0
    Rc_without -= 1.0
    res["client_level_accounts"] = len(client_accts)
    res["client_level_days_skipped_nonpositive_base"] = skipped_c
    res["client_level_dividend_flows"] = n_div_c

    # ---- A6: the performance table's reported figure for the account's client, over the same days
    fac = {d: fac_all[d] for d in dates[1:] if d in fac_all}
    missing_perf = [d for d in dates[1:] if d not in fac_all]
    res["performance_days_missing_for_client"] = len(missing_perf)
    if client is None or missing_perf:
        res["reported"] = "NOT_ESTABLISHED: the performance table carries no factor for the client on some window days"
        return res
    vals = [fac[d] for d in dates[1:]]
    med_dev = sorted(abs(v - 1.0) for v in vals)[len(vals) // 2]
    if daily_form(med_dev):
        form = "daily factors, linked by product over the window days"
        R_rep = 1.0
        for v in vals:
            R_rep *= v
        R_rep -= 1.0
    else:
        form = "an index level, read as the ratio of the last window day to the first"
        R_rep = vals[-1] / fac_all[dates[0]] - 1.0 if dates[0] in fac_all else vals[-1] / vals[0] - 1.0
    res["performance_form"] = form
    dec = max(-Decimal(repr(float(v))).as_tuple().exponent for v in vals)
    resolution = 10.0 ** (-min(max(dec, 1), 15))
    floor = len(vals) * 0.5 * resolution if daily_form(med_dev) else 0.5 * resolution

    # ---- A7: the decision (words only)
    gap = abs(R_with - R_without)
    tol = max(floor, gap / 4.0)
    dw = abs(R_rep - R_with)
    dwo = abs(R_rep - R_without)
    if n_div == 0:
        ans, why = "NOT_ESTABLISHED", "the account has no dividend or income flow inside the window"
    elif gap <= floor:
        ans, why = "NOT_ESTABLISHED", "the two computed windows differ by less than the resolution of the performance factor"
    elif dw <= tol and dwo > tol:
        ans, why = "YES", "the reported window return sits within the tolerance of the with-income figure and outside it for the without-income figure"
    elif dwo <= tol and dw > tol:
        ans, why = "NO", "the reported window return sits within the tolerance of the without-income figure and outside it for the with-income figure"
    else:
        ans, why = "NOT_ESTABLISHED", "the reported window return sits within the tolerance of neither figure, or of both"
    res["answer"] = ans
    res["answer_why"] = why
    res["tolerance_rule"] = "a quarter of the gap between the two computed figures, and at least the factor resolution over the window"
    res["gap_above_resolution"] = bool(gap > floor)
    res["reported_within_tol_of_with"] = bool(dw <= tol)
    res["reported_within_tol_of_without"] = bool(dwo <= tol)
    res["reported_between_the_two_computed_figures"] = bool(min(R_with, R_without) <= R_rep <= max(R_with, R_without))
    c_ans, c_why = decide(R_rep, Rc_with, Rc_without, floor, n_div_c)
    res["client_level_answer"] = c_ans
    res["client_level_answer_why"] = c_why
    res["client_level_reported_within_tol_of_with"] = bool(abs(R_rep - Rc_with) <= max(floor, abs(Rc_with - Rc_without) / 4.0))
    res["client_level_reported_within_tol_of_without"] = bool(abs(R_rep - Rc_without) <= max(floor, abs(Rc_with - Rc_without) / 4.0))
    return res


def decide(R_rep, R_with, R_without, floor, n_div):
    """YES / NO / NOT_ESTABLISHED: the reported figure must sit within a quarter of the gap (and the resolution) of one figure only."""
    gap = abs(R_with - R_without)
    tol = max(floor, gap / 4.0)
    dw = abs(R_rep - R_with)
    dwo = abs(R_rep - R_without)
    if n_div == 0:
        return "NOT_ESTABLISHED", "the window holds no dividend or income flow"
    if gap <= floor:
        return "NOT_ESTABLISHED", "the two computed windows differ by less than the resolution of the performance factor"
    if dw <= tol and dwo > tol:
        return "YES", "the reported window return sits within the tolerance of the with-income figure and outside it for the without-income figure"
    if dwo <= tol and dw > tol:
        return "NO", "the reported window return sits within the tolerance of the without-income figure and outside it for the with-income figure"
    return "NOT_ESTABLISHED", "the reported window return sits within the tolerance of neither figure, or of both"


def daily_form(med_dev):
    return med_dev < 0.02


_ENT = {}


def ent_names(root):
    if not _ENT:
        tax = yaml.safe_load((root / TAXONOMY_REL).read_bytes().decode("utf-8"))
        _ENT["names"] = {e["type_desc"] for e in tax["types"] if isinstance(e, dict) and e.get("type_desc")}
    return _ENT["names"]


def pa_array(values):
    import pyarrow as pa
    return pa.array(sorted(values), type=pa.string())


def eclipse_read():
    LOT_IN_TABLES = {}
    rows_with_lot = 0
    partitions_scanned = {}
    for tname in ECLIPSE_TABLES:
        parts = partitions(ECLIPSE_SILVER + tname + "/")
        partitions_scanned[tname] = len(parts)
        lot_cols_seen = set()
        for d in sorted(parts):
            body = get_bytes(parts[d])
            schema = pq.read_schema(io.BytesIO(body))
            lot_cols = [n for n in schema.names if LOT_RE.search(n)]
            if lot_cols:
                lot_cols_seen.update(lot_cols)
                tb = pq.read_table(io.BytesIO(body), columns=lot_cols)
                mask = None
                for c in lot_cols:
                    nn = pc.is_valid(tb[c])
                    mask = nn if mask is None else pc.or_(mask, nn)
                rows_with_lot += pc.sum(pc.cast(mask, "int64")).as_py() or 0
        LOT_IN_TABLES[tname] = sorted(lot_cols_seen)
    recon_keys = list_keys(ECLIPSE_RECON)
    recon_lot_keys = 0
    for k in recon_keys:
        if k.endswith(".json"):
            doc = json.loads(get_bytes(k).decode("utf-8"))
            recon_lot_keys += _lot_key_count(doc)
    meta_names = list_keys(ECLIPSE_META)
    meta_lot_names = sum(1 for k in meta_names if LOT_RE.search(k.rsplit("/", 1)[-1]))
    return {
        "tables_checked": list(ECLIPSE_TABLES),
        "partitions_scanned_per_table": partitions_scanned,
        "lot_token_columns_per_table": LOT_IN_TABLES,
        "rows_with_lot_fields": rows_with_lot,
        "populated": rows_with_lot > 0,
        "reconstructed_objects": len(recon_keys),
        "reconstructed_lot_keys": recon_lot_keys,
        "meta_objects": len(meta_names),
        "meta_lot_named_objects": meta_lot_names,
    }


def _lot_key_count(node):
    n = 0
    if isinstance(node, dict):
        for k, v in node.items():
            if LOT_RE.search(str(k)):
                n += 1
            n += _lot_key_count(v)
    elif isinstance(node, list):
        for v in node:
            n += _lot_key_count(v)
    return n


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    orion = orion_read(root)
    eclipse = eclipse_read()
    out = {"orion": orion, "eclipse": eclipse, "reads": {"list_calls": CALLS["list"], "get_calls": CALLS["get"],
                                                        "s3_reads": CALLS["list"] + CALLS["get"],
                                                        "s3_writes": 0, "vendor_calls": 0, "secret_reads": 0, "dynamodb_writes": 0}}
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
