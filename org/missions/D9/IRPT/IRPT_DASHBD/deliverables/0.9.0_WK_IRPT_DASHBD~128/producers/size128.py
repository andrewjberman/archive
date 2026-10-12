"""TO-DB-b-159 (~128): the size of a change of flow convention, on a private copy of the served daily account returns.
Reads only the private copy written by read128.py. Restates every account-day under END, START and MID with the relink formulas of
~121 y1_place.py relink (lines 38-54; the same formulas as ~108 class90.py and ~111 s2_read.py), compares END with the served return
(the control), bands the daily differences and the three windows. Counts only go to the record; the per-account-day table stays private.
Holds no account id, amount or return literal. Usage: python -I size128.py
"""
import collections
import datetime as dt
import json
import pickle

import pyarrow as pa
import pyarrow.parquet as pq

P = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~128/"
TOL = 1e-6          # control tolerance: 1e-6 of a return = 0.01 basis point
NOISE = 1e-12       # 'differing' floor: above float64 round-off on a ratio of two sums (1e-12 = 1e-8 bp)
BP = 1e-4
BANDS = ("under_1bp", "from_1_to_10bp", "over_10bp")


def band(x):
    b = abs(x) / BP
    return "under_1bp" if b < 1.0 else ("from_1_to_10bp" if b <= 10.0 else "over_10bp")


def conv_return(conv, v0, v1, fl):
    # ~121 y1_place.py relink, lines 44-52, one day
    if conv == "START":
        den = v0 + fl
        return v1 / den - 1.0 if den else None
    if conv == "MID":
        den = v0 + fl / 2.0
        return (v1 - fl / 2.0) / den - 1.0 if den else None
    return (v1 - fl) / v0 - 1.0


def main():
    D = pickle.load(open(P + "gold_copy.pkl", "rb"))
    rows = D["rows"]
    by = collections.defaultdict(list)
    for r in rows:
        by[r["account_id"]].append(r)
    last = max(r["business_date"] for r in rows)
    first_part = min(r["business_date"] for r in rows)
    ctl = collections.Counter()
    daily = {k: {"differing_days": 0, "bands": dict.fromkeys(BANDS, 0), "any_nonzero": 0} for k in ("end_vs_start", "end_vs_mid")}
    flow_days = 0
    flow_days_total = 0
    cols = collections.defaultdict(list)
    series = {}   # account -> list of (date, served_r, rEND, rSTART, rMID) with None for a null day
    ctl_notes = collections.Counter()
    for a, v in by.items():
        v.sort(key=lambda x: x["business_date"])
        s = []
        for i, d in enumerate(v):
            sr = d["total_return_daily"]
            fl = d["external_flow"] or 0.0
            if fl:
                flow_days_total += 1
            status = "NULL_SERVED"
            e = st = m = None
            if sr is not None:
                v0 = v[i - 1]["market_value_eod"] if i else None
                if not v0 or v0 <= 0:
                    status = "NO_PRIOR_LEFT_AS_SERVED"
                    e = st = m = sr
                else:
                    v1 = d["market_value_eod"]
                    re_ = conv_return("END", v0, v1, fl)
                    if abs(re_ - sr) <= TOL:
                        status = "REPRODUCES"
                        e = sr
                        st = conv_return("START", v0, v1, fl)
                        m = conv_return("MID", v0, v1, fl)
                        if st is None or m is None:
                            status = "DEN_ZERO_LEFT_AS_SERVED"
                            st = m = sr
                        elif fl:
                            flow_days += 1
                            for k, x in (("end_vs_start", st), ("end_vs_mid", m)):
                                df = abs(e - x)
                                if df > 0:
                                    daily[k]["any_nonzero"] += 1
                                if df > NOISE:
                                    daily[k]["differing_days"] += 1
                                    daily[k]["bands"][band(df)] += 1
                    else:
                        status = "END_NOT_EQUAL_LEFT_AS_SERVED"
                        ctl_notes[(d["carried_days"], bool(fl))] += 1
                        e = st = m = sr
                ctl[status] += 1
            s.append((d["business_date"], sr, e, st, m))
            cols["account_id"].append(a)
            cols["business_date"].append(d["business_date"])
            cols["flow"].append(fl)
            cols["market_value_eod"].append(d["market_value_eod"])
            cols["r_served"].append(sr)
            cols["r_end"].append(e)
            cols["r_start"].append(st)
            cols["r_mid"].append(m)
            cols["restate_status"].append(status)
            cols["return_basis"].append(d["return_basis"])
            cols["day_quality"].append(d["day_quality"])
            cols["guard_state"].append(d["guard_state"])
            cols["carried_days"].append(d["carried_days"])
        series[a] = s
    pq.write_table(pa.table(dict(cols)), P + "account_day_table.parquet")
    print("control", dict(ctl), "not-equal by (carried_days, has flow):", dict(ctl_notes))
    print("daily", daily, "flow_days", flow_days, "flow_days_total", flow_days_total)

    # windows at the last served date; anchors by the publisher's rule (publisher.py window_anchor / window_return, lines 275-310)
    asof = dt.date.fromisoformat(last)
    anchors = {"mtd": (asof.replace(day=1) - dt.timedelta(days=1)).isoformat(), "ytd": dt.date(asof.year - 1, 12, 31).isoformat(), "itd": None}
    win = {w: {k: {"accounts": 0, "bands": dict.fromkeys(BANDS, 0), "any_nonzero": 0} for k in ("end_vs_start", "end_vs_mid")} for w in anchors}
    at_asof = 0
    notcar = {w: collections.Counter() for w in anchors}
    for a, s in series.items():
        if not s or s[-1][0] != last:
            continue
        at_asof += 1
        first = s[0][0]
        for w, anc in anchors.items():
            anc2 = first if anc is None else anc
            if first > anc2:
                notcar[w]["not_spanned"] += 1
                continue
            g = {"e": 1.0, "s": 1.0, "m": 1.0}
            broke = False
            for d, sr, e, st, m in s:
                if d <= anc2:
                    continue
                if sr is None:
                    broke = True
                    break
                g["e"] *= 1.0 + e
                g["s"] *= 1.0 + st
                g["m"] *= 1.0 + m
            if broke:
                notcar[w]["break"] += 1
                continue
            for k, x in (("end_vs_start", g["s"]), ("end_vs_mid", g["m"])):
                df = abs(g["e"] - x)
                win[w][k]["accounts"] += 1
                win[w][k]["bands"][band(df) if df > NOISE else "under_1bp"] += 1
                if df > 0:
                    win[w][k]["any_nonzero"] += 1
    print("accounts at as_of", at_asof, "windows", win, "not carried", {w: dict(c) for w, c in notcar.items()})

    rec = {
        "served_accounts": len(by),
        "account_days": len(rows),
        "date_range": {"first_partition": first_part, "last_partition": last, "partitions": len(D["dates"])},
        "on_a_copy": True,
        "s3_writes": 0,
        "s3_reads": {"bucket_prefix": "opal-data-49financial/irpt/49financial/gold/account_return_daily/", "partitions_read": len(D["dates"]),
                     "newest_partition_last_modified_utc": max(m["last_modified_utc"] for m in D["meta"].values())},
        "end_reproduces": {"account_days": sum(1 for r in rows if r["total_return_daily"] is not None), "equal_within": "0.01 basis point (1e-6 of a return)",
                           "reproduces": ctl["REPRODUCES"] + ctl["DEN_ZERO_LEFT_AS_SERVED"],
                           "not_equal": ctl["END_NOT_EQUAL_LEFT_AS_SERVED"], "no_prior_value_left_as_served": ctl["NO_PRIOR_LEFT_AS_SERVED"],
                           "null_served_days_not_restated": sum(1 for r in rows if r["total_return_daily"] is None)},
        "daily": {k: {"differing_days": v["differing_days"], "bands": v["bands"], "flow_days": flow_days,
                      "differing_strictly_above_zero": v["any_nonzero"]} for k, v in daily.items()},
        "flow_days_total_all_rows": flow_days_total,
        "windows": {"as_of": last, "accounts_with_series_through_as_of": at_asof,
                    **{w: {k: {"accounts": x["accounts"], "bands": x["bands"], "differing_strictly_above_zero": x["any_nonzero"]}
                           for k, x in win[w].items()} for w in win},
                    "not_carried": {w: dict(c) for w, c in notcar.items()}},
    }
    json.dump(rec, open(P + "record_counts_draft.json", "w"), indent=1)
    print("draft written (private)")


if __name__ == "__main__":
    main()
