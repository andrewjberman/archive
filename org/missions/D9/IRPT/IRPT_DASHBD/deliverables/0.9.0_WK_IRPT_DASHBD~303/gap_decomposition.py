"""IRPT_DASHBD round 115, cell DB-i-3 (TO IRPT_DASHBD.TO-DB-i-3, worker 0.9.0_WK_IRPT_DASHBD~303).

The QTD gap decomposition of the Inflection account returns. For a 12-household sample drawn from round 114's
private variant file (every household at 100 bp or more, plus the lowest-sha household of each other bin) it
computes the SIGNED gap between the Opal derivation and Orion's client factor under:
  base         round 114's all method, through the round-108 module (daily_returns / window_return)
  identity     the same method through a second code path (prefix-sum flows, an explicit loop): must equal base
  seven variants, each differing from base in exactly one named way (see DIFFERENCES below).

Inputs (all private, read only): the round-109 cached positions values, the account dimension, the round-109
gaps file (control only), round 114's private variant file (the sample), and the newest silver partitions of the
two granted fact tables through the round-108 GET-only reader. Outputs: one private parquet (the variant table),
one repo record (GAP_DECOMPOSITION_R115.json, beside this file), and a printed summary of counts and shares.
This script holds no object write, no vendor call and no secret read.

Usage: python -I <this file>   (run from the worktree root)
"""
import bisect
import datetime as dt
import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

PRIV = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD")
CACHE = PRIV / "0.9.0_WK_IRPT_DASHBD~174" / "work" / "positions_daily_cache.parquet"
DIM = PRIV / "0.9.0_WK_IRPT_DASHBD~171" / "ACCOUNT_DIM_DRY_RUN.parquet"
GAPS109 = PRIV / "0.9.0_WK_IRPT_DASHBD~174" / "TIEOUT_GAPS.parquet"
VAR114 = PRIV / "0.9.0_WK_IRPT_DASHBD~301" / "QTD_BASIS_VARIANTS.parquet"
OUT_DIR = PRIV / "0.9.0_WK_IRPT_DASHBD~303"
OUT = OUT_DIR / "GAP_DECOMPOSITION.parquet"

BASE_DAY = "2026-09-30"
WINDOW = "qtd"
BINS = ("lt_5bp", "5_25bp", "25_100bp", "ge_100bp")
VARIANTS = ("base", "identity", "gross_fees", "settle_timing", "flow_start_of_day", "flow_midday",
            "income_accrual", "ex_cash_value", "ex_cash_no_flows")
TESTED = ("gross_fees", "settle_timing", "flow_start_of_day", "flow_midday", "income_accrual",
          "ex_cash_value", "ex_cash_no_flows")
DIFFERENCES = {
    "gross_vs_net_of_fees": ["gross_fees"],
    "trade_vs_settlement_date": ["settle_timing"],
    "flow_timing_in_a_day": ["flow_start_of_day", "flow_midday"],
    "income_accrual": ["income_accrual"],
    "cash_sweep": ["ex_cash_value", "ex_cash_no_flows"],
}
FEE_TYPES = ("Management Fee", "Trading Expense", "ADR Fee", "Administrative Fee",
             "Administrative Fee Adjustment", "Wire Fee")
CREDIT_TYPE = "Fee Credit"
SETTLE_PAT = re.compile(r"settl", re.I)
ACCRUAL_PAT = re.compile(r"ex_?date|record_?date|pay_?date|accru|payable", re.I)
SETTLE_REASON = "the transactions frame carries no settlement date"
ACCRUAL_REASON = "the transactions frame carries no ex-date, record-date or pay-date column, so no accrual date exists"

VARIANT_WORDS = {
    "gross_fees": "Each fee transaction (the six fee types) is an external outflow of its absolute amount on its "
                  "transaction date and each Fee Credit an external inflow of its absolute amount; taxes stay in "
                  "the value; every other input is the base method's.",
    "settle_timing": "The external flows would be dated by a settlement date instead of the transaction date; the "
                     "transactions frame carries no settlement-date column, so the variant cannot be formed.",
    "flow_start_of_day": "Each day's external flow is assumed at the start of the day: the day's return is the end "
                         "value over the start value plus the flow, minus one; every other input is the base method's.",
    "flow_midday": "Each day's external flow is assumed at mid-day: the day's return is the end value less the flow "
                   "over the start value plus half the flow, minus one; every other input is the base method's.",
    "income_accrual": "Income would be counted when it accrues, dated by an ex-date, record-date or pay-date; the "
                      "transactions frame carries no such column, so the variant cannot be formed.",
    "ex_cash_value": "The account value is the positions value less the cash lines, with the external flows "
                     "unchanged; every other input is the base method's.",
    "ex_cash_no_flows": "The account value is the positions value less the cash lines, and the external flows and "
                        "income are left out entirely: a return on the invested securities only.",
}
STATUS_NOT_TESTABLE = "NOT_TESTABLE"
STATUS_TESTED = "TESTED"


def _find_root():
    here = Path(__file__).resolve()
    for anc in here.parents:
        if (anc / "lib" / "trading_calendar.py").is_file() and (anc / "data").is_dir():
            return anc
    raise SystemExit("repo root not found above this file")


ROOT = _find_root()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "data" / "assets" / "scripts" / "gold" / "irpt_reporting" / "adapters"))
from lib import trading_calendar as tc  # noqa: E402
import inflection_account_dim as iad  # noqa: E402
import inflection_account_return_daily as iar  # noqa: E402

RECORD = Path(__file__).resolve().parent / "GAP_DECOMPOSITION_R115.json"


def key_of(raw):
    """A household or account key as the dimension carries it: a string, no '.0', None when blank or null."""
    if raw is None:
        return None
    if isinstance(raw, float):
        if raw != raw:
            return None
        if raw.is_integer():
            return str(int(raw))
    if isinstance(raw, int):
        return str(raw)
    text = str(raw).strip()
    return text or None


def bin_of(gap_abs):
    if gap_abs < 5.0:
        return "lt_5bp"
    if gap_abs < 25.0:
        return "5_25bp"
    if gap_abs < 100.0:
        return "25_100bp"
    return "ge_100bp"


def digest(household):
    return hashlib.sha256(household.encode("utf-8")).hexdigest()


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _cumulative(flows):
    """Sorted flow dates and their prefix sums, for the flows of one household."""
    dates = sorted(flows)
    pref = [0.0]
    for d in dates:
        pref.append(pref[-1] + flows[d])
    return dates, pref


def _flow_between(dates, pref, p, t):
    """The external flow dated in (p, t]: the skipped-day rule, read off the prefix sums."""
    return pref[bisect.bisect_right(dates, t)] - pref[bisect.bisect_right(dates, p)]


def qtd_value(vals, flows, axis_sub, start, end, mode):
    """(value, reason): the chained QTD return over the window days start..end by one method.

    mode eod    r_t = (V_t - F_t) / V_(t-1) - 1               (the base method)
    mode start  r_t = V_t / (V_(t-1) + F_t) - 1               (a flow at the start of the day)
    mode mid    r_t = (V_t - F_t) / (V_(t-1) + 0.5 F_t) - 1   (a flow at mid-day)
    mode nof    r_t = V_t / V_(t-1) - 1                        (no flows at all; F_t = 0)
    None, never zero, when a value is missing or a denominator is not positive.
    """
    dates, pref = _cumulative(flows)
    prev = {axis_sub[i]: axis_sub[i - 1] for i in range(1, len(axis_sub))}
    total = 1.0
    for t in axis_sub:
        if t not in prev or t < start or t > end:
            continue
        p = prev[t]
        vt, vp = vals.get(t), vals.get(p)
        if vt is None:
            return None, "no positions value on a window day"
        if vp is None:
            return None, "no positions value on the day before a window day"
        if vp <= 0:
            return None, "non-positive positions value on the day before a window day"
        f = 0.0 if mode == "nof" else _flow_between(dates, pref, p, t)
        if mode in ("eod", "nof"):
            r = (vt - f) / vp - 1.0
        elif mode == "start":
            den = vp + f
            if den <= 0:
                return None, "the start-of-day denominator is not positive"
            r = vt / den - 1.0
        elif mode == "mid":
            den = vp + 0.5 * f
            if den <= 0:
                return None, "the mid-day denominator is not positive"
            r = (vt - f) / den - 1.0
        else:
            raise ValueError("unknown mode " + mode)
        total *= 1.0 + r
    return total - 1.0, None


def gap_of(value, value_reason, orion, orion_reason):
    """(signed gap bp, reason): (derived - orion) * 10000, null with a reason when either side is absent."""
    if value is None:
        return None, value_reason or "the window return is not computable"
    if orion is None:
        return None, orion_reason
    return (value - orion) * 10000.0, None


def share(base_gap, var_gap):
    """Explained share (base - variant) / base on the signed gaps; null when either is null or |base| < 0.01 bp."""
    if base_gap is None or var_gap is None or abs(base_gap) < 0.01:
        return None
    return (base_gap - var_gap) / base_gap


def main():
    # 1. the account dimension: account -> household (Orion's client key)
    dim = pq.read_table(DIM, columns=["account_id", "household_id"]).to_pylist()
    acc_hh = {}
    for r in dim:
        a, h = key_of(r["account_id"]), key_of(r["household_id"])
        if a is None or h is None:
            continue
        acc_hh[a] = h
    households = sorted(set(acc_hh.values()))
    dig_to_hh = {digest(h): h for h in households}

    # 2. the performance axis: NYSE trading days from the base day to the cache's newest day
    cache_dates = pq.read_table(CACHE, columns=["date"]).column("date")
    as_of = max(cache_dates.to_pylist())
    axis = [d.isoformat() for d in tc.trading_days_between(BASE_DAY, as_of)]
    axis_sub = [d for d in axis if d >= BASE_DAY]
    start = (dt.date.fromisoformat(BASE_DAY) + dt.timedelta(days=1)).isoformat()

    # 3. the cached positions values on the axis days; a household-day with any absent account is absent
    cache = pq.read_table(CACHE, columns=["acc", "date", "v_all", "v_cash", "v_active", "nan_rows"])
    cache = cache.filter(pc.is_in(cache["date"], value_set=pa.array(axis)))
    sums = {"all": {}, "ex_cash": {}}
    absent_hh_day = set()
    unknown_accounts = 0
    for r in cache.to_pylist():
        a = key_of(r["acc"])
        if a not in acc_hh:
            unknown_accounts += 1
            continue
        h, d = acc_hh[a], r["date"]
        vals = (r["v_all"], r["v_cash"], r["v_active"])
        absent = (r["nan_rows"] or 0) > 0 or any(v is None or v != v for v in vals)
        if absent:
            absent_hh_day.add((h, d))
            continue
        sums["all"][(h, d)] = sums["all"].get((h, d), 0.0) + vals[0]
        sums["ex_cash"][(h, d)] = sums["ex_cash"].get((h, d), 0.0) + (vals[0] - vals[1])

    def vals_for(h, basis):
        return {d: sums[basis][(h, d)] for d in axis_sub
                if (h, d) in sums[basis] and (h, d) not in absent_hh_day}

    # 4. the newest transactions partition, through the round-108 GET-only reader
    reader = iad.InflectionSilverReader()
    tx_name, tx = reader.latest_partition(iar.ORION_SILVER + "fact_transactions")
    tx_columns = list(tx.columns)
    hits = [c for c in tx_columns if SETTLE_PAT.search(c) or ACCRUAL_PAT.search(c)]
    if hits:
        raise SystemExit("a settlement or accrual column appeared (%s): a rule is needed before this run" % hits)
    for t in FEE_TYPES + (CREDIT_TYPE,):
        assert iar.TYPE_CLASS[t] == "IN_VALUE", t
    flows_all, _income, tx_counts = iar.flows_of(tx, accounts=set(acc_hh))
    fee_adj, fee_rows = {}, {"fee": 0, "credit": 0, "null_amount": 0}
    for acc_raw, desc, amt, dte, st in zip(tx["accountId"].tolist(), tx["transactionDescription"].tolist(),
                                           tx["transAmount"].tolist(), tx["transDate"].tolist(),
                                           tx["status"].tolist()):
        if st != iar.STATUS_COMPLETE or (desc not in FEE_TYPES and desc != CREDIT_TYPE):
            continue
        a = key_of(acc_raw)
        if a not in acc_hh or not isinstance(dte, str):
            continue
        if amt is None or amt != amt:
            fee_rows["null_amount"] += 1
            continue
        if desc in FEE_TYPES:
            fee_adj.setdefault(a, {})
            fee_adj[a][dte] = fee_adj[a].get(dte, 0.0) - abs(float(amt))
            fee_rows["fee"] += 1
        else:
            fee_adj.setdefault(a, {})
            fee_adj[a][dte] = fee_adj[a].get(dte, 0.0) + abs(float(amt))
            fee_rows["credit"] += 1

    # the external flows per household, restricted to the window (BASE_DAY, as_of]; the gross-of-fees flows add the fees
    hh_flows = {h: {} for h in households}
    hh_flows_gross = {h: {} for h in households}
    for a, dmap in flows_all.items():
        h = acc_hh.get(a)
        for d, x in dmap.items():
            if h is not None and BASE_DAY < d <= as_of:
                hh_flows[h][d] = hh_flows[h].get(d, 0.0) + x
    for h in households:
        hh_flows_gross[h] = dict(hh_flows[h])
    for a, dmap in fee_adj.items():
        h = acc_hh[a]
        for d, x in dmap.items():
            if BASE_DAY < d <= as_of:
                hh_flows_gross[h][d] = hh_flows_gross[h].get(d, 0.0) + x

    # 5. the newest performance partition: Orion's factor on the base day and the as-of day
    pf_name, pf = reader.latest_partition(iar.ORION_SILVER + "fact_performance")
    pf = pf[pf["date"].isin([BASE_DAY, as_of])]
    perf, perf_hh, perf_dup = {}, set(), 0
    for cid, d, f in zip(pf["client_id"].tolist(), pf["date"].tolist(), pf["factor"].tolist()):
        h = key_of(cid)
        perf_hh.add(h)
        if (h, d) in perf:
            perf_dup += 1
        perf[(h, d)] = None if (f is None or f != f) else float(f)

    def orion_of(h):
        if h not in perf_hh:
            return None, "no performance row for this household in the newest partition"
        f0, f1 = perf.get((h, BASE_DAY)), perf.get((h, as_of))
        if f0 is None or f1 is None:
            return None, "no index level for this household on the base or the end date"
        if f0 <= 0:
            return None, "non-positive index level on the base date"
        return f1 / f0 - 1.0, None

    # 6. the sample: round 114's all-basis gaps (absolute, bp), by the rule
    g114 = {}
    for r in pq.read_table(VAR114, columns=["household_sha256", "variant", "gap_bp"]).to_pylist():
        if r["variant"] == "all" and r["gap_bp"] is not None and r["gap_bp"] == r["gap_bp"]:
            g114[r["household_sha256"]] = r["gap_bp"]
    by_bin = {b: [] for b in BINS}
    for h_dig, g in g114.items():
        by_bin[bin_of(abs(g))].append(h_dig)
    sample = list(by_bin["ge_100bp"])
    for b in ("lt_5bp", "5_25bp", "25_100bp"):
        if by_bin[b]:
            sample.append(sorted(by_bin[b])[0])
    sample = sorted(sample)
    sample_hh = {s: dig_to_hh[s] for s in sample}
    bin_counts = {b: sum(1 for s in sample if bin_of(abs(g114[s])) == b) for b in BINS}

    # 7. every variant, household by household
    res = {v: {} for v in VARIANTS}
    for s in sample:
        h = sample_hh[s]
        orion, orion_reason = orion_of(h)
        vals_all, vals_ex = vals_for(h, "all"), vals_for(h, "ex_cash")
        fl, flg = hh_flows[h], hh_flows_gross[h]
        # base: the round-109 module's functions, exactly as the round-109 and round-114 tie-outs call them
        daily = iar.daily_returns(vals_all, fl, axis_sub)
        base_val = iar.window_return(daily, start, as_of, trading_days=axis_sub)
        base_reason = None if base_val is not None else qtd_value(vals_all, fl, axis_sub, start, as_of, "eod")[1]
        res["base"][s] = gap_of(base_val, base_reason, orion, orion_reason)
        # identity: the same method through the second path (qtd_value, prefix sums)
        res["identity"][s] = gap_of(*qtd_value(vals_all, fl, axis_sub, start, as_of, "eod"), orion, orion_reason)
        res["gross_fees"][s] = gap_of(*qtd_value(vals_all, flg, axis_sub, start, as_of, "eod"), orion, orion_reason)
        res["settle_timing"][s] = (None, SETTLE_REASON)
        res["flow_start_of_day"][s] = gap_of(*qtd_value(vals_all, fl, axis_sub, start, as_of, "start"),
                                             orion, orion_reason)
        res["flow_midday"][s] = gap_of(*qtd_value(vals_all, fl, axis_sub, start, as_of, "mid"), orion, orion_reason)
        res["income_accrual"][s] = (None, ACCRUAL_REASON)
        res["ex_cash_value"][s] = gap_of(*qtd_value(vals_ex, fl, axis_sub, start, as_of, "eod"), orion, orion_reason)
        res["ex_cash_no_flows"][s] = gap_of(*qtd_value(vals_ex, {}, axis_sub, start, as_of, "nof"),
                                            orion, orion_reason)

    # 8. controls: base against round 114's all gap, identity against base
    base_vs_114 = 0
    for s in sample:
        b = res["base"][s][0]
        if b is None or abs(abs(b) - abs(g114[s])) > 0.01:
            base_vs_114 += 1
    ident_vs_base = 0
    for s in sample:
        b, i = res["base"][s][0], res["identity"][s][0]
        if (b is None) != (i is None) or (b is not None and abs(b - i) > 0.01):
            ident_vs_base += 1
    if base_vs_114 or ident_vs_base:
        print(json.dumps({"BLOCKING": True, "base_differs_from_round114": base_vs_114,
                          "identity_differs_from_base": ident_vs_base}, sort_keys=True))
        sys.exit(3)

    # 9. the shares, the statuses, the private table
    shares = {v: {s: share(res["base"][s][0], res[v][s][0]) for s in sample} for v in TESTED}
    status = {}
    for v in VARIANTS:
        n_gap = sum(1 for s in sample if res[v][s][0] is not None)
        status[v] = STATUS_TESTED if n_gap >= 1 else STATUS_NOT_TESTABLE
    best = {}
    for s in sample:
        vals_s = [shares[v][s] for v in TESTED if shares[v][s] is not None]
        best[s] = max(vals_s) if vals_s else None
    n_half = sum(1 for s in sample if best[s] is not None and best[s] >= 0.5)
    rows = {"household_sha256": [], "variant": [], "signed_gap_bp": [], "reason": []}
    for v in VARIANTS:
        for s in sample:
            gap, reason = res[v][s]
            rows["household_sha256"].append(s)
            rows["variant"].append(v)
            rows["signed_gap_bp"].append(gap)
            rows["reason"].append(reason)
    table = pa.table({
        "household_sha256": pa.array(rows["household_sha256"], pa.string()),
        "variant": pa.array(rows["variant"], pa.string()),
        "signed_gap_bp": pa.array(rows["signed_gap_bp"], pa.float64()),
        "reason": pa.array(rows["reason"], pa.string()),
    })
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, OUT)
    out_sha = sha256_file(OUT)

    # 10. summaries (counts, bp and shares only; no household is printed)
    summary = {}
    for v in TESTED:
        vals_v = [shares[v][s] for s in sample if shares[v][s] is not None]
        summary[v] = {
            "status": status[v],
            "gaps_computed": sum(1 for s in sample if res[v][s][0] is not None),
            "moved_closer_share_above_0": sum(1 for x in vals_v if x > 0),
            "share_count": len(vals_v),
            "median_share": (round(statistics.median(vals_v), 4) if vals_v else None),
        }
    tested_med = {v: summary[v]["median_share"] for v in TESTED if summary[v]["median_share"] is not None}
    top = max(tested_med, key=lambda v: tested_med[v]) if tested_med else None
    low = min(tested_med, key=lambda v: tested_med[v]) if tested_med else None
    n_s = len(sample)
    cols_text = ", ".join(tx_columns)
    basis_words = (
        "Transactions frame: newest partition " + tx_name + ", " + str(len(tx_columns)) + " columns: " + cols_text + ". "
        "No settlement-date, ex-date, record-date, pay-date or accrual column is carried, so the trade-against-settlement "
        "variant and the income-accrual variant are NOT_TESTABLE: " + SETTLE_REASON + "; " + ACCRUAL_REASON + ". "
        "Control: base (the round-109 module functions over the all-basis values and the window flows) matched round 114's "
        "all gap on " + str(n_s - base_vs_114) + " of " + str(n_s) + " sampled households, the absolute gaps agreeing within "
        "0.01 bp. Identity (the same method through the second path) differed from base on "
        + str(ident_vs_base) + " of " + str(n_s) + " sampled households. "
        "The flow variants and the cash variants change one input each and are compared with base on the same households. "
        "Largest median share among the tested variants: " + str(top) + "; smallest: " + str(low) + "; medians are "
        "over the households with a computable share. " + str(len(tx_columns)) + " columns were read; fee rows used for "
        "the gross variant: " + str(fee_rows["fee"]) + " fee and " + str(fee_rows["credit"]) + " credit, with "
        + str(fee_rows["null_amount"]) + " null amounts skipped as flows_of skips them."
    )
    record = {
        "script": {"file": Path(__file__).resolve().relative_to(ROOT).as_posix(), "sha256": sha256_file(Path(__file__))},
        "window": WINDOW,
        "sample_size": n_s,
        "sample_households_sha256": sample,
        "variant_file": {"path": OUT.as_posix(), "sha256": out_sha},
        "differences": DIFFERENCES,
        "variants": {v: {
            "status": status[v],
            "claim": "measured" if status[v] == STATUS_TESTED else "absent",
            "words": VARIANT_WORDS[v],
        } for v in TESTED},
        "explained_share": {v: {s: shares[v][s] for s in sample} for v in TESTED},
        "households_with_a_single_difference_explaining_half": n_half,
        "basis_words": basis_words,
        "reads": {"vendor_calls": 0, "s3_writes": 0, "dynamodb_writes": 0, "secret_reads": 0,
                  "s3_reads": int(reader.reads)},
        "files_in_repo_private": False,
        "served_values_changed": False,
        "pushed": False,
        "deployed": False,
    }
    RECORD.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "sample_size": n_s,
        "sample_bins": bin_counts,
        "transactions": {"partition": tx_name, "columns": len(tx_columns), "rows": tx_counts["rows"],
                         "complete": tx_counts["complete"], "unresolved": tx_counts["unresolved"],
                         "null_amount": tx_counts["null_amount"]},
        "performance": {"partition": pf_name, "duplicate_keys": perf_dup},
        "unknown_cache_accounts": unknown_accounts,
        "control_base_vs_round114_differing": base_vs_114,
        "control_identity_vs_base_differing": ident_vs_base,
        "status": status,
        "variants": summary,
        "households_with_a_single_difference_explaining_half": n_half,
        "variant_file_rows": table.num_rows,
        "variant_file_sha256": out_sha,
        "script_sha256": sha256_file(Path(__file__)),
        "reader_reads": reader.reads,
    }, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
