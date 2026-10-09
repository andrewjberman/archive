"""TO-DB-b-100 (IRPT_DASHBD round 49, DB-b-100): the 74 W73-S1 DEFECT segments, each read on BOTH sides.

READ-ONLY: S3 GETs/LISTs only; zero vendor calls; no S3 write. Writes, beside this file, W73_S1_EVIDENCE.json and W73_S1_RESOLUTION.json.

Usage: python resolve_w73_s1.py <repo_root> [--cache <tieout pickle>] [--trn-cache <pickle>] [--bal-cache <pickle>]

Per segment (row IRPT_DASHBD-D2-W73-S1 of ~73/UNEXPLAINED_CLASSIFIED.json):
  OUR side   the served daily gold (market value, external flow) the tie-out read, and the custodian's own balance table for the same
             dates (dim_balance: net_mv_plus_cash + margin_balance) -- the producer's value is checked against its source.
  BD side    Black Diamond's landed bronze point for the same range (beginning/ending market value, netAdditions, netGains).
  CAUSE      each dollar gap is matched to custodian rows (fact_trn) it equals:
             - flow gap  = the SERVICE FEE rows (FEE-ADMIN, not the ADR fee) in the window, or a net-zero securities transfer valued at the
                           prior close;
             - boundary value gap = income the custodian paid AFTER the boundary day whose ex-date is on or before it (exact subset of those
                           rows), or, where no exact set exists, bounded by those rows plus the next money-market payment.
  A segment whose every dollar gap is matched is BD_SIDE (BD's record carries something the custodian's ledger does not at that date);
  a gap with no match would be left for a producer review and the script says so.
"""
import importlib.util
import io
import itertools
import json
import pickle
import sys
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import boto3
import pandas as pd
import pyarrow.parquet as pq
from botocore.config import Config

HERE = Path(__file__).resolve().parent
ROOT_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
CLASSIFIED = ROOT_REL + "0.9.0_WK_IRPT_DASHBD~73/UNEXPLAINED_CLASSIFIED.json"
V2PY = ROOT_REL + "0.9.0_WK_IRPT_DASHBD~35/tieout_compound_v2.py"
V2JSON = ROOT_REL + "0.9.0_WK_IRPT_DASHBD~35/TIEOUT_COMPOUND_V2.json"
CLASS_TABLE = "org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
ROW_ID = "IRPT_DASHBD-D2-W73-S1"
BUCKET = "opal-data-assets"
TRN = "schwab/08335338/silver/fact_trn/"
BAL = "schwab/08335338/silver/dim_balance/"
POS = "schwab/08335338/silver/dim_position/"
INC_RE = "divid|interest|coupon"
TRN_COLS = ["account_id", "tr_cd", "sb_cd", "tran_srcde", "tran_date", "exdivdnd_date", "quantity", "gross_amount",
            "debit_credit", "cusip", "ticker_symbol"]
TOL = 0.02


def load_mod(root, rel, name):
    sp = importlib.util.spec_from_file_location(name, str(root / rel))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def days_of(s3, prefix):
    out = set()
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix + "date=", Delimiter="/"):
        for c in page.get("CommonPrefixes", []) or []:
            out.add(c["Prefix"].rstrip("/").split("date=")[-1])
    return sorted(out)


def read_day(s3, prefix, day, cols):
    frames = []
    r = s3.list_objects_v2(Bucket=BUCKET, Prefix="%sdate=%s/" % (prefix, day))
    for o in r.get("Contents", []):
        if o["Key"].endswith(".parquet"):
            frames.append(pq.read_table(io.BytesIO(s3.get_object(Bucket=BUCKET, Key=o["Key"])["Body"].read()), columns=cols).to_pandas())
    if not frames:
        return None
    f = pd.concat(frames, ignore_index=True)
    f["account_id"] = f["account_id"].astype(str).str.strip().str.zfill(10)
    return f


def d(s):
    return dt.date.fromisoformat(s)


def subset_exact(cands, gap, maxn=20):
    """cands = [(key, amount)]; the smallest subset whose sum equals gap within TOL, else None."""
    if len(cands) > maxn:
        return None
    if abs(sum(a for _, a in cands) - gap) <= TOL:
        return list(cands)
    for n in range(1, len(cands)):
        for comb in itertools.combinations(cands, n):
            if abs(sum(a for _, a in comb) - gap) <= TOL:
                return list(comb)
    return None


def main():
    root = Path(sys.argv[1]).resolve()

    def opt(name):
        return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None

    s3 = boto3.client("s3", region_name="us-east-1", config=Config(max_pool_connections=40, retries={"max_attempts": 8, "mode": "standard"}))
    v2m = load_mod(root, V2PY, "v2")
    plan, (n_obj, bronze, gold, n_part, n_gold_accts) = v2m.load(root, opt("--cache"))
    bdacct = {r["account"]: str(r["bd_account"]) for r in plan["request_list"]}
    v2 = json.loads((root / V2JSON).read_bytes().decode("utf-8"))
    vx = {(x["account"], x["segment"]["start"], x["segment"]["end"]): x for x in v2["segments"]}
    cls = json.loads((root / CLASSIFIED).read_bytes().decode("utf-8"))
    segs = [x for x in cls["classified"] if x.get("row") == ROW_ID]
    if len(segs) != 74:
        print("STOP: %d segments carry row %s, want 74" % (len(segs), ROW_ID))
        sys.exit(2)
    accts = sorted({x["account"] for x in segs})

    # ---- Black Diamond's landed points (S3 GET)
    need = {}
    for x in segs:
        need.setdefault(bdacct[x["account"]], set()).add((x["segment"]["start"], x["segment"]["end"]))

    def bdget(a):
        key = "blackdiamond/49financial/bronze/reporting_performance/pull=20261004/acct=%s.json" % a
        b = json.loads(s3.get_object(Bucket=BUCKET, Key=key)["Body"].read().decode("utf-8"))
        out = {}
        for lv in b.get("levels") or []:
            dd = lv.get("descriptor") or {}
            if dd.get("level") != "Account" or str(dd.get("levelId")) != a:
                continue
            for p in lv.get("dateRangePoints") or []:
                k = (p["dateRange"]["startDate"][:10], p["dateRange"]["endDate"][:10])
                if k in need[a]:
                    out[k] = {kk: vv for kk, vv in p.items() if kk != "dateRange" and not isinstance(vv, (dict, list))}
        return a, out

    with ThreadPoolExecutor(16) as ex:
        bdx = dict(ex.map(bdget, list(need)))

    # ---- the custodian's ledger for these accounts (fact_trn), with the classification table
    tcache = opt("--trn-cache")
    if tcache and Path(tcache).is_file():
        df = pd.read_pickle(tcache)
    else:
        D = days_of(s3, TRN)

        def rd(day):
            f = read_day(s3, TRN, day, TRN_COLS)
            if f is None:
                return None
            f = f[f["account_id"].isin(accts)].copy()
            f["_pd"] = day
            return f

        with ThreadPoolExecutor(24) as ex:
            res = list(ex.map(rd, D))
        df = pd.concat([x for x in res if x is not None], ignore_index=True)
        if tcache:
            df.to_pickle(tcache)
    tab = json.loads((root / CLASS_TABLE).read_bytes().decode("utf-8"))
    T = {(str(r["tran_srcde"]).strip(), str(r["tr_cd"]).strip(), str(r["sb_cd"]).strip()): (r.get("partition"), r.get("category")) for r in tab}
    keys = list(zip(df.tran_srcde.astype(str).str.strip(), df.tr_cd.astype(str).str.strip(), df.sb_cd.astype(str).str.strip()))
    df["part"] = [T.get(k, ("<unkeyed>", ""))[0] for k in keys]
    df["cat"] = [T.get(k, ("<unkeyed>", ""))[1] for k in keys]
    df["trc"] = df.tr_cd.astype(str).str.strip()
    df["sg"] = pd.to_numeric(df.gross_amount, errors="coerce").abs() * df.debit_credit.astype(str).str.strip().str[:1].str.upper().map({"C": 1, "D": -1})
    df["E"] = df.exdivdnd_date.map(lambda v: str(v)[:10] if (v is not None and v == v) else "None")
    inc = df[(df.trc == "FC") & (df.sg > 0) & df.cat.astype(str).str.contains(INC_RE, case=False)]
    fee = df[(df.part == "FEE-ADMIN") & (df.tran_srcde.astype(str).str.strip() != "ADRF") & (df.trc == "FC")]

    # ---- the custodian's balance on the boundary dates (dim_balance), for the producer-vs-source check
    bal_dates = set()
    for x in segs:
        g = gold[x["account"]]
        ds = sorted(g)
        prev = [q for q in ds if q < x["segment"]["start"]]
        first = [q for q in ds if q >= x["segment"]["start"]][0]
        bal_dates.update([prev[-1] if prev else first, x["segment"]["end"]])
    bcache = opt("--bal-cache")
    if bcache and Path(bcache).is_file():
        bal = pickle.load(open(bcache, "rb"))
    else:
        def rb(day):
            f = read_day(s3, BAL, day, ["account_id", "net_mv_plus_cash", "margin_balance"])
            if f is None:
                return day, {}
            f = f[f["account_id"].isin(accts)]
            eq = pd.to_numeric(f["net_mv_plus_cash"], errors="coerce") + pd.to_numeric(f["margin_balance"], errors="coerce")
            return day, dict(zip(f["account_id"], eq))

        with ThreadPoolExecutor(24) as ex:
            bal = dict(ex.map(rb, sorted(bal_dates)))
        if bcache:
            pickle.dump(bal, open(bcache, "wb"))

    pos_close = {}

    def close_of(day, cusip):
        k = (day, cusip)
        if k not in pos_close:
            f = read_day(s3, POS, day, ["account_id", "cusip", "closing_price"])
            v = None
            if f is not None:
                m = f[f["cusip"].astype(str).str.strip() == cusip]
                if len(m):
                    v = float(m["closing_price"].iloc[0])
            pos_close[k] = v
        return pos_close[k]

    # ---- the income-accrual simulation (INFERRED; shown beside the dollar read, never used to decide a disposition)
    def sim_return(a, s):
        g = gold[a]
        ds = sorted(g)
        seg = [q for q in ds if s["start"] <= q <= s["end"]]
        prev = [q for q in ds if q < s["start"]]
        order = ([prev[-1]] if prev else []) + seg
        ia, fa = inc[inc.account_id == a], fee[fee.account_id == a]
        acc = []
        for _, r in ia.iterrows():
            P, E = r["_pd"], r["E"]
            if E != "None":
                if E < P:
                    acc.append((E, P, float(r["sg"]), False))
            else:
                pr = ia[(ia.ticker_symbol == r["ticker_symbol"]) & (ia._pd < P) & (ia.E == "None")]
                st = pr._pd.max() if len(pr) else (d(P) - dt.timedelta(days=30)).isoformat()
                acc.append((st, P, float(r["sg"]), True))

        def A(t):
            tot = 0.0
            for st, P, amt, mm in acc:
                if mm:
                    if st < t < P:
                        tot += amt * (d(t) - d(st)).days / max(1, (d(P) - d(st)).days)
                elif st <= t < P:
                    tot += amt
            return tot

        p, tprev, Vprev = 1.0, None, None
        for i, t in enumerate(order):
            V = (g[t]["mv"] or 0.0) + A(t)
            if i == 0:
                Vprev, tprev = V, t
                continue
            F = (g[t]["flow"] or 0.0) + fa[(fa._pd > tprev) & (fa._pd <= t)].sg.sum()
            if g[t]["r"] is not None and Vprev > 0:
                p *= (V - F) / Vprev
            Vprev, tprev = V, t
        return p - 1.0

    def accrual_read(a, D0, gap, label):
        """Match a boundary-value gap to income the custodian paid after D0 with ex-date on or before D0."""
        hi = (d(D0) + dt.timedelta(days=60)).isoformat()
        w = inc[(inc.account_id == a) & (inc._pd > D0) & (inc._pd <= hi)]
        ex = w[(w.E != "None") & (w.E <= D0)]
        cands = [(i, float(v)) for i, v in zip(ex.index, ex.sg)]
        m = subset_exact(cands, gap)

        def rows_of(idx):
            return [{"business_date": df.at[i, "_pd"], "ex_date": df.at[i, "E"], "source_code": str(df.at[i, "tran_srcde"]).strip(),
                     "ticker": str(df.at[i, "ticker_symbol"]).strip(), "amount": round(float(df.at[i, "sg"]), 2)} for i in idx]

        if m:
            return {"kind": "BD_INCOME_ACCRUED_AT_%s" % label, "tier": "EXACT_SET", "boundary_day": D0, "gap": round(gap, 2),
                    "matched_sum": round(sum(v for _, v in m), 2), "candidate_rows_considered": len(cands),
                    "rows": rows_of([i for i, _ in m])}
        mm = w[w.E == "None"]
        first_mm = {}
        for i, r in mm.iterrows():
            first_mm.setdefault(r["ticker_symbol"], i)
        mm_next = sum(float(df.at[i, "sg"]) for i in first_mm.values())
        ex_total = sum(v for _, v in cands)
        if 0 < gap <= ex_total + mm_next + TOL:
            return {"kind": "BD_INCOME_ACCRUED_AT_%s" % label, "tier": "BOUNDED_BY_PAID_INCOME", "boundary_day": D0, "gap": round(gap, 2),
                    "exdated_paid_after_total": round(ex_total, 2), "next_money_market_payment_total": round(mm_next, 2),
                    "gap_over_next_payment": round(gap / mm_next, 4) if mm_next else None,
                    "rows": rows_of([i for i, _ in cands] + list(first_mm.values()))}
        # an in-kind reinvestment dated on or before the boundary but posted after it (valued at the fund's $1 unit)
        late = df[(df.account_id == a) & (df.trc == "IC") & (df._pd > D0) & (df._pd <= hi) & (df.tran_date.astype(str).str[:10] <= D0)
                  & (df.tran_srcde.astype(str).str.strip() == "DIV")]
        late_total = float(pd.to_numeric(late.quantity, errors="coerce").abs().sum())
        if 0 < gap <= late_total + TOL:
            return {"kind": "BD_INCOME_ACCRUED_AT_%s" % label, "tier": "BOUNDED_BY_LATE_POSTED_REINVEST", "boundary_day": D0, "gap": round(gap, 2),
                    "late_posted_reinvest_total": round(late_total, 2),
                    "rows": [{"business_date": r["_pd"], "effective_date": str(r["tran_date"])[:10], "source_code": str(r["tran_srcde"]).strip(),
                              "units": round(abs(float(r["quantity"])), 2)} for _, r in late.iterrows()]}
        all_total = float(w.sg.sum())
        if 0 < gap <= all_total + TOL:
            return {"kind": "BD_INCOME_ACCRUED_AT_%s" % label, "tier": "BOUNDED_BY_NEXT_60D_INCOME", "boundary_day": D0, "gap": round(gap, 2),
                    "income_paid_within_60_days_total": round(all_total, 2), "income_rows": int(len(w))}
        return {"kind": "BD_VALUE_ABOVE_CUSTODIAN_EQUITY_AT_%s" % label, "tier": "UNATTRIBUTED", "boundary_day": D0, "gap": round(gap, 2),
                "income_paid_within_60_days_total": round(all_total, 2), "ledger_last_day": str(df._pd.max()),
                "note": "no custodian ledger row or bound accounts for this gap; the served series equals the custodian equity on this day"}

    evidence, resolution, unmatched = [], [], []
    for x in segs:
        a, s = x["account"], x["segment"]
        g = gold[a]
        ds = sorted(g)
        seg = [q for q in ds if s["start"] <= q <= s["end"]]
        prev = [q for q in ds if q < s["start"]]
        days = [g[q] for q in seg if g[q]["r"] is not None]
        prevd = prev[-1] if prev else seg[0]
        o_bmv = g[prevd]["mv"] or 0.0
        o_emv = days[-1]["mv"] or 0.0
        o_flow = sum(q["flow"] or 0.0 for q in days)
        o_gain = o_emv - o_bmv - o_flow
        b = bdx[bdacct[a]][(s["start"], s["end"])]
        bmv, emv, nadd, ngain = b["beginningMarketValue"], b["endingMarketValue"], b["netAdditions"], b["netGains"]
        gaps = {"bmv": bmv - o_bmv, "emv": emv - o_emv, "net_additions": nadd - o_flow, "net_gains": ngain - o_gain}
        causes = []
        # flows
        if abs(gaps["net_additions"]) > TOL:
            wf = fee[(fee.account_id == a) & (fee._pd > prevd) & (fee._pd <= s["end"])]
            fsum = float(wf.sg.sum())
            left = gaps["net_additions"] - fsum
            if len(wf) and abs(left) <= TOL:
                causes.append({"kind": "BD_FEE_ADMIN_AS_NET_ADDITION", "tier": "EXACT_SET", "gap": round(gaps["net_additions"], 2),
                               "matched_sum": round(fsum, 2),
                               "rows": [{"business_date": r["_pd"], "source_code": str(r["tran_srcde"]).strip(), "amount": round(float(r["sg"]), 2)}
                                        for _, r in wf.iterrows()]})
            else:
                base = fsum if len(wf) and abs(fsum) > TOL and abs(left) < abs(gaps["net_additions"]) else 0.0
                rem = gaps["net_additions"] - base
                ic = df[(df.account_id == a) & (df.trc == "IC") & (df._pd > prevd) & (df._pd <= s["end"])]
                found = None
                for (day, cusip), grp in ic.groupby(["_pd", "cusip"]):
                    sides = grp.debit_credit.astype(str).str.strip().str[:1].str.upper()
                    q = pd.to_numeric(grp.quantity, errors="coerce").abs()
                    if sides.eq("S").sum() >= 1 and sides.eq("L").sum() >= 1 and abs(q[sides == "S"].sum() - q[sides == "L"].sum()) < 1e-6:
                        pd_ = [q2 for q2 in ds if q2 < day]
                        px = close_of(pd_[-1], str(cusip).strip()) if pd_ else None
                        if px and abs(-q[sides == "S"].sum() * px - rem) <= TOL:
                            found = (day, str(cusip).strip(), float(q[sides == "S"].sum()), px, pd_[-1])
                if found:
                    if base:
                        causes.append({"kind": "BD_FEE_ADMIN_AS_NET_ADDITION", "tier": "EXACT_SET", "gap": round(base, 2), "matched_sum": round(base, 2)})
                    causes.append({"kind": "BD_TRANSFER_LEG_AS_WITHDRAWAL", "tier": "EXACT_VALUE", "gap": round(rem, 2), "business_date": found[0],
                                   "quantity_each_side": found[2], "prior_close": found[3], "prior_close_day": found[4],
                                   "note": "SHORT and LONG legs of one security transfer net to zero in the same account; the custodian position file "
                                           "carries the same quantity before and after; BD's net additions carry the short leg at the prior close"})
                else:
                    causes.append({"kind": "UNMATCHED_FLOW_GAP", "tier": "NONE", "gap": round(gaps["net_additions"], 2)})
        # boundary values
        if abs(gaps["bmv"]) > TOL:
            causes.append(accrual_read(a, prevd, gaps["bmv"], "START"))
        if abs(gaps["emv"]) > TOL:
            causes.append(accrual_read(a, s["end"], gaps["emv"], "END"))
        bad = [c for c in causes if c["tier"] == "NONE"]
        cust0, cust1 = bal.get(prevd, {}).get(a), bal.get(s["end"], {}).get(a)
        v = vx[(a, s["start"], s["end"])]
        key = "%s|%s|%s" % (a, s["start"], s["end"])
        ev = {"key": key, "account": a, "segment": s,
              "our_side": {"claim": "measured", "source": "served account_return_daily gold as read by the tie-out; custodian dim_balance for the same dates",
                           "beginning_value_day": prevd, "beginning_value": round(o_bmv, 2), "ending_value_day": s["end"], "ending_value": round(o_emv, 2),
                           "external_flow": round(o_flow, 2), "gain": round(o_gain, 2), "linked_days": len(days),
                           "custodian_equity_beginning_day": None if cust0 is None else round(float(cust0), 2),
                           "custodian_equity_ending_day": None if cust1 is None else round(float(cust1), 2),
                           "series_equals_custodian": bool(cust0 is not None and cust1 is not None and abs(cust0 - o_bmv) <= 0.011 and abs(cust1 - o_emv) <= 0.011)},
              "black_diamond_side": {"claim": "measured", "source": "bronze reporting_performance pull=20261004", "beginning_value": round(bmv, 2),
                                     "ending_value": round(emv, 2), "net_additions": round(nadd, 2), "net_gains": round(ngain, 2),
                                     "fees": b.get("fees"), "income": b.get("income"), "days_held": b.get("daysHeld"),
                                     "own_identity_residual": round(emv - bmv - nadd - ngain, 2)},
              "gaps_bd_minus_ours": {k: round(vv, 2) for k, vv in gaps.items()},
              "causes": causes,
              "return_read": {"claim": "inferred", "opal_return_served": v["opal_return"], "bd_return": v["bd_return"], "bd_gross_return": v["bd_gross_return"],
                              "note": "return after re-stating our daily series to BD's income-accrual and service-fee convention, with money-market "
                                      "accrual spread linearly between payments; shown for the reader, not used to decide the disposition",
                              "restated_return": round(sim_return(a, s), 6)}}
        ev["return_read"]["restated_minus_bd_gross_pp"] = round((ev["return_read"]["restated_return"] - v["bd_gross_return"]) * 100.0, 3)
        evidence.append(ev)
        if bad or not ev["our_side"]["series_equals_custodian"]:
            unmatched.append(key)
        names = []
        for c in causes:
            if c["kind"] not in names:
                names.append(c["kind"])
        resolution.append({"account": a, "segment": s, "disposition": "UNRESOLVED" if (bad or not ev["our_side"]["series_equals_custodian"]) else "BD_SIDE",
                           "cause": "+".join(names) if names else "NO_DOLLAR_GAP_OVER_TOLERANCE",
                           "evidence": ("org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~75/W73_S1_EVIDENCE.json#" + key)})
    (HERE / "W73_S1_EVIDENCE.json").write_bytes((json.dumps(
        {"measured_by": "0.9.0_WK_IRPT_DASHBD~75", "task_order": "IRPT_DASHBD.TO-DB-b-100", "row": ROW_ID, "vendor_calls": 0, "s3_writes": 0,
         "segments_total": len(evidence), "segments": evidence}, indent=1) + "\n").encode("utf-8"))
    (HERE / "W73_S1_RESOLUTION.json").write_bytes((json.dumps(
        {"measured_by": "0.9.0_WK_IRPT_DASHBD~75", "task_order": "IRPT_DASHBD.TO-DB-b-100", "row": ROW_ID, "segments": resolution}, indent=1) + "\n").encode("utf-8"))
    by = {}
    for r in resolution:
        by[r["disposition"]] = by.get(r["disposition"], 0) + 1
    print("OK: %d segments; dispositions %s; unmatched %s" % (len(resolution), by, unmatched))


if __name__ == "__main__":
    main()
