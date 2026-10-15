"""IRPT_DASHBD round 114, cell DB-i-1 (TO IRPT_DASHBD.TO-DB-i-1, worker 0.9.0_WK_IRPT_DASHBD~301).

Re-runs the round-109 quarter-to-date tie-out of the Inflection account returns under three value bases:
  all          every row of each positions day (round 109's basis; the control)
  active_only  only the rows whose isActive flag is true (the cache's v_active)
  ex_cash      every row less the cash lines (the cache's v_all minus v_cash)
Only the value series changes between bases. The flows, the axis, the window and the source's figure are the
same under every basis. The method is the round-109 module's: daily_returns on the household sums, then
window_return over the quarter-to-date window (the trading days after the base day through the as-of day).

Inputs (all private, read only): the round-109 cached positions values, the account dimension, the round-109
gaps file (control only), the newest silver partition of the two granted fact tables through the round-108
GET-only reader. Output: one private parquet (the variant file) and a printed summary of counts only.
This script holds no object write, no vendor call and no secret read.

Usage: python -I <this file>
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

PRIV = Path("C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD")
CACHE = PRIV / "0.9.0_WK_IRPT_DASHBD~174" / "work" / "positions_daily_cache.parquet"
DIM = PRIV / "0.9.0_WK_IRPT_DASHBD~171" / "ACCOUNT_DIM_DRY_RUN.parquet"
GAPS = PRIV / "0.9.0_WK_IRPT_DASHBD~174" / "TIEOUT_GAPS.parquet"
OUT = PRIV / "0.9.0_WK_IRPT_DASHBD~301" / "QTD_BASIS_VARIANTS.parquet"

BASE_DAY = "2026-09-30"
WINDOW = "qtd"
VARIANTS = ("all", "active_only", "ex_cash")
BINS = ("lt_5bp", "5_25bp", "25_100bp", "ge_100bp")
ORDER = {b: i for i, b in enumerate(BINS)}


def _find_root() -> Path:
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


def bin_of(gap_bp: float) -> str:
    if gap_bp < 5.0:
        return "lt_5bp"
    if gap_bp < 25.0:
        return "5_25bp"
    if gap_bp < 100.0:
        return "25_100bp"
    return "ge_100bp"


def digest(household: str) -> str:
    return hashlib.sha256(household.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    # 1. the account dimension: account -> household (Orion's client key, carried as household_id)
    dim = pq.read_table(DIM, columns=["account_id", "household_id"]).to_pylist()
    acc_hh = {}
    dim_no_household = 0
    for r in dim:
        a = key_of(r["account_id"])
        h = key_of(r["household_id"])
        if a is None:
            continue
        if h is None:
            dim_no_household += 1
            continue
        acc_hh[a] = h
    households = sorted(set(acc_hh.values()))

    # 2. the performance axis: NYSE trading days from the base day to the cache's newest day
    cache_dates = pq.read_table(CACHE, columns=["date"]).column("date")
    as_of = max(cache_dates.to_pylist())
    axis = [d.isoformat() for d in tc.trading_days_between(BASE_DAY, as_of)]
    window_days = [d for d in axis if d > BASE_DAY]
    start = (dt.date.fromisoformat(BASE_DAY) + dt.timedelta(days=1)).isoformat()
    cache_day_set = set(cache_dates.unique().to_pylist())
    missing_window_days = [d for d in window_days if d not in cache_day_set]

    # 3. the cached positions values on the axis days only (the base day and the window)
    cache = pq.read_table(CACHE, columns=["acc", "date", "v_all", "v_cash", "v_active", "nan_rows"])
    cache = cache.filter(pc.is_in(cache["date"], value_set=pa.array(axis)))
    acc_day = {}
    unknown_accounts = set()
    for r in cache.to_pylist():
        a = key_of(r["acc"])
        if a not in acc_hh:
            unknown_accounts.add(a)
            continue
        vals = (r["v_all"], r["v_cash"], r["v_active"])
        absent = (r["nan_rows"] or 0) > 0 or any(v is None or v != v for v in vals)
        acc_day[(a, r["date"])] = None if absent else vals
    sums = {b: {} for b in VARIANTS}
    absent_hh_day = set()
    for (a, d), vals in acc_day.items():
        h = acc_hh[a]
        if vals is None:
            absent_hh_day.add((h, d))
            continue
        v_all, v_cash, v_active = vals
        per = {"all": v_all, "active_only": v_active, "ex_cash": v_all - v_cash}
        for b in VARIANTS:
            sums[b][(h, d)] = sums[b].get((h, d), 0.0) + per[b]

    # 4. the newest silver partitions, through the round-108 GET-only reader
    reader = iad.InflectionSilverReader()
    tx_name, tx = reader.latest_partition(iar.ORION_SILVER + "fact_transactions")
    flows, _income, tx_counts = iar.flows_of(tx, accounts=set(acc_hh))
    del tx
    window_flow_dates = {d for d in set().union(*[set(m) for m in flows.values()]) if BASE_DAY < d <= as_of} if flows else set()
    bad_date_keys = sum(1 for m in flows.values() for d in m if len(d) != 10)
    hh_flows = {}
    for a, dmap in flows.items():
        h = acc_hh.get(a)
        if h is None:
            continue
        for d, x in dmap.items():
            if d in window_flow_dates:
                hh_flows.setdefault(h, {})
                hh_flows[h][d] = hh_flows[h].get(d, 0.0) + x

    pf_name, pf = reader.latest_partition(iar.ORION_SILVER + "fact_performance")
    pf = pf[pf["date"].isin([BASE_DAY, as_of])]
    perf = {}
    perf_dup = 0
    perf_households = set()
    for cid, d, f in zip(pf["client_id"].tolist(), pf["date"].tolist(), pf["factor"].tolist()):
        h = key_of(cid)
        perf_households.add(h)
        if (h, d) in perf:
            perf_dup += 1
        perf[(h, d)] = None if (f is None or f != f) else float(f)
    del pf

    # 5. the three bases, household by household
    results = {b: {} for b in VARIANTS}
    reason_counts = {b: {} for b in VARIANTS}
    for b in VARIANTS:
        for h in households:
            vals = {d: sums[b][(hh, d)] for (hh, d) in [(h, x) for x in axis] if (hh, d) in sums[b]
                    and (hh, d) not in absent_hh_day}
            fl = hh_flows.get(h, {})
            axis_sub = [d for d in axis if d >= BASE_DAY]
            daily = iar.daily_returns(vals, fl, axis_sub)
            derived = iar.window_return(daily, start, as_of, trading_days=axis_sub)
            reasons = []
            if derived is None:
                reasons.append(_derived_reason(vals, axis_sub, start))
            f0 = perf.get((h, BASE_DAY))
            f1 = perf.get((h, as_of))
            orion = None
            if h not in perf_households:
                reasons.append("no performance row for this household in the newest partition")
            elif f0 is None or f1 is None:
                reasons.append("no index level for this household on the base or the end date")
            elif f0 <= 0:
                reasons.append("non-positive index level on the base date")
            else:
                orion = f1 / f0 - 1.0
            if derived is None or orion is None:
                reason = "; ".join(reasons) if reasons else "not computable"
                gap = None
            else:
                gap = abs(derived - orion) * 10000.0
                reason = None
            if reason:
                for part in reason.split("; "):
                    reason_counts[b][part] = reason_counts[b].get(part, 0) + 1
            results[b][h] = (gap, reason)

    # 6. the control: basis all against round 109's qtd rows, household by household
    gap_rows = pq.read_table(GAPS).to_pylist()
    gap109 = {r["household_sha256"]: r["gap_bp"] for r in gap_rows if r["window"] == WINDOW}
    control_diff = 0
    control_null_mismatch = 0
    for h in households:
        ours = results["all"][h][0]
        theirs = gap109.get(digest(h), "absent")
        if theirs == "absent":
            control_diff += 1
            continue
        if (ours is None) != (theirs is None):
            control_diff += 1
            control_null_mismatch += 1
        elif ours is not None and abs(ours - theirs) > 0.01:
            control_diff += 1

    # 7. the summary (counts only) and the moved-down count
    summary = {}
    for b in VARIANTS:
        comp = [results[b][h][0] for h in households if results[b][h][0] is not None]
        bins = {k: 0 for k in BINS}
        for g in comp:
            bins[bin_of(g)] += 1
        summary[b] = {
            "clients_compared": len(comp),
            "not_comparable": len(households) - len(comp),
            "bins": bins,
            "reasons": reason_counts[b],
        }
    moved = {}
    for b in ("active_only", "ex_cash"):
        n = 0
        for h in households:
            g_all = results["all"][h][0]
            g_b = results[b][h][0]
            if g_all is None or g_b is None:
                continue
            if ORDER[bin_of(g_b)] < ORDER[bin_of(g_all)]:
                n += 1
        moved[b] = n

    # 8. the private variant file: one row per household per variant
    out_rows = {"household_sha256": [], "variant": [], "gap_bp": [], "reason": []}
    for b in VARIANTS:
        for h in households:
            gap, reason = results[b][h]
            out_rows["household_sha256"].append(digest(h))
            out_rows["variant"].append(b)
            out_rows["gap_bp"].append(gap)
            out_rows["reason"].append(reason)
    table = pa.table({
        "household_sha256": pa.array(out_rows["household_sha256"], pa.string()),
        "variant": pa.array(out_rows["variant"], pa.string()),
        "gap_bp": pa.array(out_rows["gap_bp"], pa.float64()),
        "reason": pa.array(out_rows["reason"], pa.string()),
    })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(table, OUT)

    print(json.dumps({
        "script_sha256": sha256_file(Path(__file__).resolve()),
        "variant_file_sha256": sha256_file(OUT),
        "variant_file_rows": table.num_rows,
        "window": WINDOW,
        "window_start": start,
        "base_day": BASE_DAY,
        "as_of_day": as_of,
        "axis_days": len(axis),
        "window_days": len(window_days),
        "window_days_missing_from_cache": len(missing_window_days),
        "dim_accounts": len(acc_hh),
        "dim_accounts_without_household": dim_no_household,
        "households": len(households),
        "cache_accounts_not_in_dim": len(unknown_accounts),
        "control": {"qtd_rows": sum(1 for r in gap_rows if r["window"] == WINDOW),
                    "differing_households": control_diff,
                    "null_mismatch": control_null_mismatch},
        "newest_partitions": {"fact_transactions": tx_name, "fact_performance": pf_name},
        "transactions": {"rows": tx_counts["rows"], "complete": tx_counts["complete"],
                         "unresolved": tx_counts["unresolved"], "null_amount": tx_counts["null_amount"],
                         "by_class": tx_counts["by_class"], "bad_date_keys": bad_date_keys},
        "performance": {"duplicate_keys": perf_dup, "households_with_row": len(perf_households & set(households))},
        "variants": summary,
        "moved_down_a_bin": moved,
        "reader_reads": reader.reads,
    }, indent=1, sort_keys=True))


def _derived_reason(vals: dict, axis_sub: list, start: str) -> str:
    """The first plain-words reason a window day cannot be measured."""
    prev = None
    for t in axis_sub:
        if t >= start:
            if t not in vals:
                return "no positions value on a window day"
            if prev is None or prev not in vals:
                return "no base value on a window day"
            if vals[prev] <= 0:
                return "non-positive base value on a window day"
        prev = t
    return "the window return is not computable"


if __name__ == "__main__":
    main()
