"""IRPT_DASHBD TO-DB-b-36 (round 24, workstream B) -- diagnosis of the round-23 activity-identity gaps. READ ONLY.

Reads the producer `account_activity_lots.py` and the served `account_return_daily.py` by import (neither is edited), reads S3
silver (get/list only, no write), and writes GAP_DIAGNOSIS_E1.json beside this file. Run from the worktree root:

    python <this file>            # uses .scratch/ caches when present, otherwise reads S3 (about 10 minutes cold)

The producer's own numbers are re-derived in two modes: AS-RUN (the pandas this machine carries) and COUNTERFACTUAL (the same
producer under `pd.options.future.infer_string = False`, i.e. the string-dtype behaviour of pandas 2.x). The counterfactual is an
evidence run, never a proposed fix and never written anywhere. ASCII only.
"""
import json
import pickle
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd
from botocore.config import Config

ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT / "data/assets/scripts/gold/irpt_reporting"))
sys.path.insert(0, str(ROOT / "lib"))
import account_activity_lots as aal  # noqa: E402
import account_return_daily as ard  # noqa: E402
import trading_calendar as tc  # noqa: E402

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
RECORD = ROOT / D / "0.9.0_WK_IRPT_DASHBD~20/ACTIVITY_LOTS_LOCAL_RUN.json"
OUT = ROOT / D / "0.9.0_WK_IRPT_DASHBD~21/GAP_DIAGNOSIS_E1.json"
CACHE = ROOT / ".scratch"
TOLERANCE = 0.05          # stated in the task order BEFORE the run: rounding of daily figures over 24 trading days
BUCKET = "opal-data-assets"
ROOTP = "schwab/08335338/silver/"
TERMS = ("beginning_value", "contributions", "withdrawals", "realized", "unrealized_change", "income", "ending_value")


def acct_of(frame):
    return frame["account_id"].astype(str).str.strip().str.zfill(10)


def num(s):
    return pd.to_numeric(s, errors="coerce")


def cached(name, build):
    p = CACHE / name
    if p.is_file():
        return pickle.loads(p.read_bytes())
    out = build()
    CACHE.mkdir(exist_ok=True)
    p.write_bytes(pickle.dumps(out))
    return out


# ---------------------------------------------------------------- the producer, re-run in two modes
def produce(s3, rec, cf):
    def build():
        pd.options.future.infer_string = not cf
        try:
            tables, run = aal.compute_local(s3, rec["days"], rec["accounts"], workers=12)
        finally:
            pd.options.future.infer_string = True
        return {"activity": tables[aal.TABLE_ACTIVITY], "realized": tables[aal.TABLE_REALIZED]}
    return cached("rerun_cf.pkl" if cf else "rerun.pkl", build)


def fetch_trn(s3, rec, src):
    def build():
        days = rec["days"]
        prev = str(tc.prev_trading_day(days[0]))[:10]
        pdays = [x for x in ard.partition_days(s3, src["bucket"], src["transactions_prefix"]) if prev < x <= days[-1]]
        frames = []
        for x in pdays:
            f = ard.read_partition(s3, src["bucket"], src["transactions_prefix"], x)
            f["_partition"] = x
            f["_pos"] = range(len(f))
            f["_acct"] = acct_of(f)
            frames.append(f)
        return pd.concat(frames, ignore_index=True)
    return cached("trn_all2.pkl", build)


def fetch_days(s3, table, days, accounts, cols=None, name=None):
    keep = set(accounts)

    def one(d):
        f = ard.read_partition(s3, BUCKET, ROOTP + table + "/", d, columns=cols)
        if f is None:
            return d, None
        f = f[acct_of(f).isin(keep)].copy()
        f["_acct"] = acct_of(f)
        f["_pos"] = f.index
        return d, f

    def build():
        with ThreadPoolExecutor(8) as pool:
            return dict(pool.map(one, days))
    return cached(name or ("%s_%d.pkl" % (table, len(keep))), build)


# ---------------------------------------------------------------- the rule, read from the declaration
def load_rule():
    doc = ard.load_declaration()
    src = ard.source_entry(doc, ard.declared_sources(doc)[0])
    table, keycols = ard.load_classification(src)
    return src, table, keycols


def sign_of(row_tr_cd, side, src):
    first = str(side).strip().upper()[:1]
    if str(row_tr_cd).strip().upper() == str(src["cash_code_value"]).upper():
        v = {str(k).upper(): float(x) for k, x in src["direction_map"].items()}.get(first)
        return v
    if str(row_tr_cd).strip().upper() == str(src["inkind_code_value"]).upper():
        return {str(k).upper(): float(x) for k, x in src["inkind_direction_map"].items()}.get(first)
    return None


def rowkey(r):
    return "fact_trn/date=%s/row=%d" % (r["_partition"], int(r["_pos"]))


def rowdesc(r):
    return {"row": rowkey(r), "key": "%s/%s/%s" % (r["tran_srcde"], r["tr_cd"], r["sb_cd"]), "side": r["debit_credit"],
            "gross_amount": float(r["gross_amount"]), "quantity": float(r["quantity"]), "price": float(r["price"]),
            "cusip": str(r["cusip"]).strip()}


def prep(trn):
    t = trn.copy()
    for c in ("tran_srcde", "tr_cd", "sb_cd", "debit_credit"):
        t[c] = t[c].astype(str).str.strip()
    t["gross"] = num(t["gross_amount"]).fillna(0.0)
    return t


# ---------------------------------------------------------------- main
def main():
    rec = json.loads(RECORD.read_bytes().decode("utf-8"))
    rec_gaps = {r["account_id"]: float(r["gap"]) for r in rec["window_identity"]["accounts_above_one_cent"]}
    s3 = boto3.client("s3", config=Config(max_pool_connections=32, retries={"max_attempts": 6, "mode": "adaptive"}))
    src, ctable, keycols = load_rule()
    days = rec["days"]
    start, end = days[0], days[-1]
    prev0 = str(tc.prev_trading_day(start))[:10]

    asrun = produce(s3, rec, cf=False)
    cfrun = produce(s3, rec, cf=True)

    def windows(run):
        rows = run["activity"]
        out = {}
        for a in sorted({r["account_id"] for r in rows}):
            w = aal.window_reconciliation(rows, a, start, end)
            if w:
                out[a] = w
        return out
    w_asrun, w_cf = windows(asrun), windows(cfrun)
    graded = sorted(w_asrun)
    above = {a: w["gap"] for a, w in w_asrun.items() if abs(w["gap"]) > aal.CENT}
    reproduction = {
        "accounts_graded": len(graded), "above_one_cent": len(above),
        "same_set_as_round_23": sorted(above) == sorted(rec_gaps),
        "max_abs_gap_difference": max(abs(above[a] - rec_gaps[a]) for a in rec_gaps),
    }
    assert reproduction["same_set_as_round_23"] and reproduction["max_abs_gap_difference"] < 1e-6, reproduction
    cf_above = {a: w["gap"] for a, w in w_cf.items() if abs(w["gap"]) > aal.CENT}

    trn = prep(fetch_trn(s3, rec, src))
    trn = trn[trn["_acct"].isin(set(graded))].copy()
    pdays = sorted(trn["_partition"].unique())
    assert pdays == days, "partitions are not the trading days: carried-day logic would differ"
    keys = list(zip(trn["tran_srcde"], trn["tr_cd"], trn["sb_cd"]))
    trn["cls"] = [ctable.get(k, {"partition": "<unkeyed>"})["partition"] for k in keys]
    trn["final"] = [ctable.get(k, {"final": "UNRESOLVED"})["final"] for k in keys]
    trn["cat"] = [ctable.get(k, {"category": ""})["category"] for k in keys]
    trn["sign"] = [sign_of(a, b, src) for a, b in zip(trn["tr_cd"], trn["debit_credit"])]
    is_cash = trn["tr_cd"].str.upper() == str(src["cash_code_value"]).upper()
    is_ic = trn["tr_cd"].str.upper() == str(src["inkind_code_value"]).upper()
    cond = trn["final"].isna()                                  # CONDITIONAL-BY-COUNTERPARTY (None in the rule's table)
    income_cat = is_cash & trn["cat"].str.contains(ard.INCOME_CATEGORY_RE, na=False)
    wd = trn["sb_cd"].str.upper() == ard.WITHHOLDING_CODE
    trn["is_cash"], trn["is_ic"], trn["cond"] = is_cash, is_ic, cond

    # ------------------------------------------------ (2) the type census: key x side, as the rule reads it
    def maps_to(r):
        r = dict(r, sign=(None if pd.isna(r["sign"]) else r["sign"]), final=(None if pd.isna(r["final"]) else r["final"]))
        if r["is_cash"]:
            if r["final"] in ("EXTERNAL", "FEE-MANAGEMENT") and r["sign"] is not None:
                return "contributions" if r["sign"] > 0 else "withdrawals"
            if bool(re.search(ard.INCOME_CATEGORY_RE, r["cat"])) and r["sign"] is not None and r["sign"] > 0 \
                    and r["sb_cd"].upper() != ard.WITHHOLDING_CODE:
                return "income"
            return None
        if r["is_ic"] and r["final"] == "EXTERNAL" and r["sign"] is not None:
            return "contributions" if r["sign"] > 0 else "withdrawals"
        return None
    trn["maps"] = [maps_to(r) for r in trn.to_dict("records")]

    # sweeps are value-neutral only if each account-day's signed sweep legs net to zero -- MEASURED here, not assumed
    sw = trn[trn["tran_srcde"].isin(["BKSWP", "BRSWP"]) & trn["is_cash"]].copy()
    sw["signed"] = sw["gross"] * sw["sign"]
    swd = sw.groupby(["_acct", "_partition"])["signed"].sum()
    sweep_check = {"account_days_with_sweep_legs": int(len(swd)), "account_days_net_nonzero": int((swd.abs() > 0.005).sum())}

    def moves_value(key, r):
        if r["tran_srcde"] in ("BKSWP", "BRSWP"):
            return sweep_check["account_days_net_nonzero"] > 0, "BKSWP/BRSWP legs net to zero on every account-day (sweep_check)"
        if not r["is_cash"] and not r["is_ic"]:
            return False, "a trade leg swaps cash for a security at the trade price; its gain reaches the identity through the lots"
        if r["is_cash"]:
            if r["final"] in ("EXTERNAL", "FEE-MANAGEMENT", "FEE-ADMIN") or r["cond"]:
                return True, "cash crosses the account boundary or is an expense of the account (table class %s)" % r["cls"]
            if bool(re.search(ard.INCOME_CATEGORY_RE, r["cat"])):
                return True, "cash received or withheld as income/tax (category %s)" % r["cat"]
            return True, "cash row not otherwise classed"
        if r["final"] == "EXTERNAL" or r["cond"]:
            return True, "securities cross the account boundary (table class %s)" % r["cls"]
        return True, ("an in-kind position removal with no cash leg: on acct#2fcb1889 2026-10-02 the day's identity gap equals the "
                      "cost basis of the lots the adjusting entry removed (see gap_classes)")
    census = []
    grp = trn.groupby(["tran_srcde", "tr_cd", "sb_cd", "debit_credit"], sort=True)
    for (a, b, c, side), g in grp:
        r = g.iloc[0]
        mv, why = moves_value((a, b, c), r)
        sgn = None if pd.isna(r["sign"]) else r["sign"]
        census.append({
            "type": "%s/%s/%s/%s" % (a, b, c, side), "row_count": int(len(g)), "accounts": int(g["_acct"].nunique()),
            "sign": "UNSIGNED" if sgn is None else ("+" if sgn > 0 else "-"),
            "maps_to_term": (None if pd.isna(r["maps"]) else r["maps"]), "moves_value": bool(mv), "moves_value_basis": why,
            "table_class": r["cls"], "table_category": r["cat"],
            "intended_term_if_resolved": ("contributions" if sgn and sgn > 0 else "withdrawals") if (r["cond"] and sgn) else None,
            "as_executed_note": ("CONDITIONAL-BY-COUNTERPARTY: _final is NaN not None under pandas %s, so no stage resolves the row "
                                 "and the flow rule never reads it" % pd.__version__) if r["cond"] else None})
    unmapped = sorted(c["type"] for c in census if c["moves_value"] and c["maps_to_term"] is None)

    # ------------------------------------------------ the evidence that the CONDITIONAL rows are dropped (as-run vs counterfactual)
    cond_rows = trn[trn["cond"]]
    proof_days = sorted(cond_rows["_partition"].unique())
    full = fetch_trn(s3, rec, src)
    flow_proof = []
    for d in proof_days:
        accts = sorted(cond_rows[cond_rows["_partition"] == d]["_acct"].unique())
        pd.options.future.infer_string = True
        fc1 = ard.FlowCache(s3, src, ctable, keycols, accts)
        f1 = fc1.get(d)[0]
        pd.options.future.infer_string = False
        try:
            fc2 = ard.FlowCache(s3, src, ctable, keycols, accts)
            f2 = fc2.get(d)[0]
        finally:
            pd.options.future.infer_string = True
        keysel = ("ft_excluded_class-nan_rows", "resolved_text-counterpart", "resolved_pair-match", "external-by-default")
        flow_proof.append({
            "day": d, "accounts_with_conditional_rows": len(accts),
            "flow_as_run": {a: round(f1.get(a, 0.0), 2) for a in accts}, "flow_counterfactual": {a: round(f2.get(a, 0.0), 2) for a in accts},
            "census_as_run": {k: fc1.census[d].get(k) for k in keysel}, "census_counterfactual": {k: fc2.census[d].get(k) for k in keysel}})

    # ------------------------------------------------ (1) the largest gap, term by term
    big = max(above, key=lambda a: abs(above[a]))
    mine = trn[trn["_acct"] == big]
    act = sorted((r for r in asrun["activity"] if r["account_id"] == big), key=lambda r: r["business_date"])
    rld = fetch_days(s3, "fact_rld", days, [big], name="rld_big.pkl")
    ulots = {t: fetch_days(s3, t, [prev0] + days, [big], name="%s_big.pkl" % t) for t in ("fact_uln", "fact_ult")}
    bal = fetch_days(s3, "dim_balance", [prev0] + days, [big], cols=["account_id"] + ard.value_columns(src), name="bal_big.pkl")

    def value_row(d):
        f = bal[d]
        v = ard.equity_value(f, src)
        return float(v.sum()), len(f), ["dim_balance/date=%s/account_id=%s" % (d, big)] * len(f)

    def ugain(d):
        n, tot, keys_ = 0, 0.0, []
        for t, fr in ulots.items():
            f = fr.get(d)
            if f is None or not len(f):
                continue
            n += len(f)
            tot += float(num(f["unrealized_gain_loss"]).sum())
            keys_ += ["%s/date=%s/event_id=%s/cusip=%s/acquired=%s" % (t, d, str(r["event_id"]).strip(), str(r["cusip"]).strip(),
                                                                     str(r["acquired_date"])[:10]) for _, r in f.iterrows()]
        return tot, n, keys_
    beg, n_b, k_b = value_row(prev0)
    endv, n_e, k_e = value_row(end)
    # flows: the producer's classifier on each day, as run; rows that carry them are the boundary-crossing classed rows
    nets = {}
    for d in days:
        day = full[full["_partition"] == d].drop(columns=["_partition", "_pos", "_acct"])
        pd.options.future.infer_string = True
        f1, _, _, _, _ = ard.classify_and_sum(day.copy(), src, ctable, keycols, accounts=[big])
        nets[d] = f1.get(big, 0.0)
    contributions = sum(v for v in nets.values() if v > 0)
    withdrawals = -sum(v for v in nets.values() if v < 0)
    flow_rows = mine[mine["is_cash"] & mine["final"].isin(["EXTERNAL", "FEE-MANAGEMENT"])]
    byday = flow_rows.assign(s=flow_rows["gross"] * flow_rows["sign"]).groupby("_partition")["s"].sum().to_dict()
    for d in days:
        assert abs(byday.get(d, 0.0) - nets[d]) < 0.005, (d, byday.get(d), nets[d])
    c_rows = [rowkey(r) for _, r in flow_rows.iterrows() if r["sign"] > 0]
    w_rows = [rowkey(r) for _, r in flow_rows.iterrows() if r["sign"] < 0]
    realized_rows = []
    realized_v = 0.0
    for d, f in rld.items():
        if f is not None and len(f):
            realized_v += float(num(f["gain_loss_dollars"]).sum())
            realized_rows += ["fact_rld/date=%s/close_event_id=%s/open=%s" % (d, r["close_event_id"], r["close_open_event_id"])
                              for _, r in f.iterrows()]
    u_b, nu_b, ku_b = ugain(prev0)
    u_e, nu_e, ku_e = ugain(end)
    inc = mine[mine["is_cash"] & income_cat[mine.index] & (mine["sign"] > 0) & ~wd[mine.index]]
    income_v = float((inc["gross"] * inc["sign"]).sum())
    prod_w = w_asrun[big]
    terms = {
        "beginning_value": {"value": round(beg, 2), "row_count": n_b, "source_rows": k_b[:1], "source": "dim_balance %s" % prev0},
        "contributions": {"value": round(contributions, 2), "row_count": len(c_rows), "source_rows": c_rows,
                          "source": "fact_trn boundary-crossing credits, day-netted by the producer's classifier"},
        "withdrawals": {"value": round(withdrawals, 2), "row_count": len(w_rows), "source_rows": w_rows,
                        "source": "fact_trn boundary-crossing debits, day-netted by the producer's classifier"},
        "realized": {"value": round(realized_v, 2), "row_count": len(realized_rows), "source_rows": realized_rows,
                     "source": "fact_rld rows of the account over the %d partitions" % len(days)},
        "unrealized_change": {"value": round(u_e - u_b, 4), "row_count": nu_b + nu_e, "source_rows": ku_b + ku_e,
                              "source": "fact_uln + fact_ult unrealized_gain_loss, end day less %s" % prev0},
        "income": {"value": round(income_v, 2), "row_count": int(len(inc)), "source_rows": [rowkey(r) for _, r in inc.iterrows()],
                   "source": "fact_trn cash credits whose table category is dividend/interest/coupon and sb_cd is not WD"},
        "ending_value": {"value": round(endv, 2), "row_count": n_e, "source_rows": k_e[:1], "source": "dim_balance %s" % end}}
    for t in TERMS:
        pv = {"beginning_value": prod_w["beginning_value"], "contributions": prod_w["contributions"], "withdrawals": prod_w["withdrawals"],
              "realized": prod_w["realized"], "unrealized_change": prod_w["unrealized_change"], "income": prod_w["income"],
              "ending_value": prod_w["ending_value"]}[t]
        terms[t]["producer_value"] = pv
        terms[t]["difference_to_producer"] = round(terms[t]["value"] - pv, 4)
    recomputed_gap = round(beg + contributions - withdrawals + realized_v + (u_e - u_b) + income_v - endv, 4)

    # the gap, day by day, against the CONDITIONAL cash rows the rule never read
    cash_cond = mine[mine["cond"] & mine["is_cash"]].assign(s=lambda x: x["gross"] * x["sign"])
    miss = cash_cond.groupby("_partition")["s"].sum().to_dict()
    daily = []
    for r in act:
        d = r["business_date"]
        g = r["identity_gap"] or 0.0
        m = miss.get(d, 0.0)
        daily.append({"day": d, "gap": g, "conditional_cash_not_read": round(m, 2), "gap_less_cash_effect": round(g + m, 4)})
    cash_part = round(-sum(miss.values()), 2)
    inkind_rows = mine[mine["cond"] & mine["is_ic"]]
    cf_big = w_cf[big]

    # ------------------------------------------------ (3) the gaps classed
    first = {r["account_id"]: r["gap"] for r in rec["window_identity"]["accounts_above_one_cent"]}
    need = [a for a in sorted(first) if abs(first[a]) > TOLERANCE]
    lot_days = [prev0] + days
    lots = {t: fetch_days(s3, t, lot_days, need, name="%s_need.pkl" % t) for t in ("fact_uln", "fact_ult")}

    def lot_totals(a, d):
        parts = [lots[t].get(d) for t in lots]
        parts = [p[p["_acct"] == a] for p in parts if p is not None and len(p)]
        f = pd.concat(parts) if parts else None
        if f is None or not len(f):
            return {"cb": 0.0, "ocb": 0.0, "n": 0}
        return {"cb": float(num(f["cost_basis_unamortized"]).sum()), "ocb": float(num(f["original_cost_basis"]).sum()), "n": len(f)}
    causes = {}
    for a in need:
        g = first[a]
        m = trn[trn["_acct"] == a]
        arows = {r["business_date"]: r for r in asrun["activity"] if r["account_id"] == a}
        cond_cash = m[m["cond"] & m["is_cash"]].assign(s=lambda x: x["gross"] * x["sign"])
        miss_a = cond_cash.groupby("_partition")["s"].sum().to_dict()
        admin = m[m["is_cash"] & (m["final"] == "FEE-ADMIN")]
        tax = m[m["is_cash"] & wd[m.index] & ~m["cond"]]
        adm = float((admin["gross"] * admin["sign"]).sum()) if len(admin) else 0.0
        tx = float((tax["gross"] * tax["sign"]).sum()) if len(tax) else 0.0
        comp = {"conditional_cash_not_read": round(-sum(miss_a.values()), 4), "fee_admin_not_mapped": round(-adm, 4),
                "withholding_tax_not_mapped": round(-tx, 4), "basis_moved_without_flow": 0.0, "basis_wedge_on_new_lots": 0.0}
        days_used = {"basis_moved_without_flow": [], "basis_wedge_on_new_lots": []}
        prevt = lot_totals(a, prev0)
        table_days = []
        for d in days:
            cur = lot_totals(a, d)
            dcb, docb = cur["cb"] - prevt["cb"], cur["ocb"] - prevt["ocb"]
            wedge = dcb - docb
            has_tr = bool(((m["_partition"] == d) & ~m["is_cash"] & ~m["is_ic"]).any())
            gd = arows[d]["identity_gap"] if d in arows and arows[d]["identity_gap"] is not None else 0.0
            gd_cash = gd + miss_a.get(d, 0.0)
            used = None
            if wedge >= TOLERANCE and abs(gd + wedge) <= TOLERANCE:
                comp["basis_wedge_on_new_lots"] += -wedge
                used = "basis_wedge_on_new_lots"
            elif abs(dcb) >= TOLERANCE and not has_tr and abs(gd_cash + dcb) <= TOLERANCE:
                comp["basis_moved_without_flow"] += -dcb
                used = "basis_moved_without_flow"
            if used:
                days_used[used].append(d)
            if used or abs(gd) > TOLERANCE:
                table_days.append({"day": d, "gap": gd, "conditional_cash_not_read": round(miss_a.get(d, 0.0), 2),
                                   "delta_cost_basis": round(dcb, 2), "delta_original_cost_basis": round(docb, 2),
                                   "delta_wedge": round(wedge, 2), "trade_rows_that_day": has_tr, "attributed_to": used})
            prevt = cur
        comp = {k: round(v, 4) for k, v in comp.items()}
        explained = round(sum(comp.values()), 4)
        ev = [rowdesc(r) for _, r in m[m["cond"] | (m["is_cash"] & (m["final"] == "FEE-ADMIN")) | (m["is_cash"] & wd[m.index])
                                         | (m["is_ic"] & (m["final"] != "EXTERNAL"))].iterrows()]
        for d in days_used["basis_wedge_on_new_lots"]:
            for t in lots:
                f = lots[t].get(d)
                if f is None or not len(f):
                    continue
                f = f[(f["_acct"] == a) & ((num(f["cost_basis_unamortized"]) - num(f["original_cost_basis"])).abs() > 0.004)
                      & ((f["orgpurch_date"].astype(str).str[:10] == d) | (f["acquired_date"].astype(str).str[:10] == d))]
                for _, r in f.iterrows():
                    ev.append({"row": "%s/date=%s/event_id=%s/cusip=%s" % (t, d, str(r["event_id"]).strip(), str(r["cusip"]).strip()),
                               "cost_basis_unamortized": float(r["cost_basis_unamortized"]),
                               "original_cost_basis": float(r["original_cost_basis"]),
                               "acquired_date": str(r["acquired_date"])[:10], "orgpurch_date": str(r["orgpurch_date"])[:10]})
        causes[a] = {"gap": g, "components": {k: v for k, v in comp.items() if v}, "days": days_used, "explained": explained,
                     "residual": round(g - explained, 4), "counterfactual_gap": cf_above.get(a, 0.0), "gap_days": table_days,
                     "evidence_rows": ev}
    big_c = causes[big]
    cause = (
        "The journals and transfers of assets that moved this account's value are CONDITIONAL-BY-COUNTERPARTY rows in the shared code "
        "table, and the served flow rule never reads them: classify_and_sum assigns _final = None for that class and resolves it later "
        "with `_final is None`, but on pandas %s the list assignment turns the None into NaN, so no stage resolves a row and the row is "
        "not even counted as UNRESOLVED (census key ft_excluded_class-nan_rows). Window gap %.2f = %.2f from %d cash journals "
        "(JNL cash rows, signed net %.2f of value moved) that no term carries + %.2f from the cost basis of the in-kind lots that arrived or left (%d "
        "JNL/TOA legs; the lot table moves only the gain, so the basis part has no term) on %s; a +958,986.00 / -958,986.00 pair on "
        "%s nets to zero (the lot table lags the balance by one trading day on an in-kind journal out). Residual %.4f. "
        "Counterfactually (the same producer with the None kept) every journal enters the flow and the window gap becomes %.2f -- a "
        "SECOND cause that fixing the first exposes: an in-kind arrival carries a lot whose whole value is gain (cost basis 0 until "
        "the custodian posts it) and the flow also counts the arrival, so the identity needs an in-kind term."
        % (pd.__version__, above[big], big_c["components"].get("conditional_cash_not_read", 0.0), len(cash_cond),
           -cash_part, big_c["components"].get("basis_moved_without_flow", 0.0), len(inkind_rows),
           ", ".join(big_c["days"]["basis_moved_without_flow"]), "2026-09-25 / 2026-09-28", big_c["residual"], cf_big["gap"]))
    evidence = [rowdesc(r) for _, r in mine[mine["cond"]].iterrows()]
    largest = {
        "account_id": big, "window": "%s..%s" % (start, end), "beginning_taken_on": prev0,
        "round_23_gap": above[big], "recomputed_gap": recomputed_gap, "terms": terms, "cause": cause, "evidence_rows": evidence,
        "gap_by_day": [x for x in daily if abs(x["gap"]) > TOLERANCE or x["conditional_cash_not_read"]],
        "gap_decomposition": {"components": big_c["components"], "residual": big_c["residual"], "counterfactual_window_gap": cf_big["gap"],
                              "flow_proof_for_this_account": [p for p in flow_proof if big in p["flow_as_run"]]}}
    return {"rec": rec, "above": above, "cf_above": cf_above, "census": census, "unmapped": unmapped, "sweep_check": sweep_check,
            "flow_proof": flow_proof, "largest": largest, "causes": causes, "first": first, "reproduction": reproduction,
            "n_types_rows": int(len(trn)), "graded": graded, "w_asrun": w_asrun, "w_cf": w_cf}


LABEL = {
    "conditional_cash_not_read": "CONDITIONAL_FLOW_NOT_READ",
    "fee_admin_not_mapped": "FEE_ADMIN_HAS_NO_TERM",
    "withholding_tax_not_mapped": "WITHHELD_TAX_HAS_NO_TERM",
    "basis_moved_without_flow": "LOT_BASIS_MOVED_WITHOUT_FLOW",
    "basis_wedge_on_new_lots": "LOT_BASIS_ABOVE_ORIGINAL_COST",
}
WHAT = {
    "conditional_cash_not_read": "cash journal / transfer-of-assets rows classed CONDITIONAL-BY-COUNTERPARTY that the flow rule drops "
                                 "(NaN _final under pandas %s)" % pd.__version__,
    "fee_admin_not_mapped": "an FEE-ADMIN debit (table class FEE-ADMIN): it leaves the account and no term takes it",
    "withholding_tax_not_mapped": "a withheld-tax debit (sb_cd WD): neither flow nor income by ruling, and no term takes it",
    "basis_moved_without_flow": "a lot's cost basis moved with no value movement (in-kind lots leaving, or a basis posted days after an "
                                "in-kind receipt), which shifts unrealized gain with nothing in the flow",
    "basis_wedge_on_new_lots": "new lots whose cost_basis_unamortized exceeds the original cost actually paid (a basis adjustment, "
                               "consistent with a wash-sale carry-over: acquired_date earlier than orgpurch_date on the lot), so the "
                               "lot's gain is understated against the cash that moved",
}


def assemble(res):
    rec = res["rec"]
    rows = []
    for r in rec["window_identity"]["accounts_above_one_cent"]:
        a, g = r["account_id"], float(r["gap"])
        if abs(g) <= TOLERANCE:
            rows.append({"account_id": a, "gap": g, "class": "ROUNDING",
                         "cause": "|gap| <= %.2f: rounding of the daily figures over 24 trading days" % TOLERANCE})
            continue
        c = res["causes"][a]
        parts = ["%s %+.4f (%s)" % (LABEL[k], v, WHAT[k]) for k, v in c["components"].items()]
        rows.append({"account_id": a, "gap": g, "class": "MISSING-TERM",
                     "cause": "; ".join(parts) + "; residual %+.4f" % c["residual"],
                     "cause_types": [LABEL[k] for k in c["components"]], "components": c["components"],
                     "attributed_days": c["days"], "residual": c["residual"], "counterfactual_gap": c["counterfactual_gap"],
                     "gap_days": c["gap_days"], "evidence_rows": c["evidence_rows"]})
    counts = {k: sum(1 for x in rows if x["class"] == k) for k in ("ROUNDING", "MISSING-TERM")}
    by_cause = defaultdict(int)
    for x in rows:
        for t in x.get("cause_types", []):
            by_cause[t] += 1
    return {
        "task_order": "IRPT_DASHBD.TO-DB-b-36", "worker": "0.9.0_WK_IRPT_DASHBD~21",
        "window": "%s..%s" % (rec["days"][0], rec["days"][-1]),
        "environment": {"pandas": pd.__version__, "python": sys.version.split()[0],
                        "note": "the producer was run read-only in two modes: as-run and counterfactual (infer_string False); "
                                "the counterfactual is evidence, never a proposed edit and never written to S3"},
        "reproduction_of_round_23": res["reproduction"],
        "largest_gap_window": res["largest"],
        "type_census": res["census"],
        "type_census_scope": {"source": "fact_trn, %d partitions of the window" % len(rec["days"]), "accounts": len(res["graded"]),
                              "rows": res["n_types_rows"],
                              "type_grain": "tran_srcde/tr_cd/sb_cd/debit_credit; a key whose sides carry opposite signs is two types",
                              "sign_rule": "FC rows: C=+ D=- (direction_map); IC rows: L=+ S=- (inkind_direction_map); every other row UNSIGNED",
                              "maps_to_term_is": "as EXECUTED by the producer on this machine; intended_term_if_resolved says what the rule intends",
                              "moves_value_is": "the row changes the account's whole value (crosses the boundary, is income, an expense, "
                                                "a tax, or a position removed) -- sweeps and trade legs do not"},
        "unmapped_value_movers": res["unmapped"],
        "sweep_check": res["sweep_check"],
        "conditional_class_evidence": res["flow_proof"],
        "gap_classes": {"tolerance": TOLERANCE, "tolerance_stated": "before the run, in the task order: 0.05 per account-window",
                        "counts": counts, "cause_counts": dict(by_cause), "rows": rows,
                        "counterfactual": {"above_one_cent": len(res["cf_above"]), "above_tolerance": sum(
                            1 for v in res["cf_above"].values() if abs(v) > TOLERANCE),
                            "note": "with the CONDITIONAL rows resolved the flow term moves acct#f0faa651, acct#9a0972ea, acct#2fcb1889 and "
                                    "acct#2ef9eee4; two close, two become other gaps (in-kind lots)"}},
    }


if __name__ == "__main__":
    res = main()
    out = assemble(res)
    OUT.write_text(json.dumps(out, indent=1, default=str) + chr(10), encoding="utf-8")
    print("wrote", OUT.name, out["gap_classes"]["counts"], "unmapped", len(out["unmapped_value_movers"]))
