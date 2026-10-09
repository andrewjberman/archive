"""TO-DB-b-106 (IRPT_DASHBD round 52, DB-b-106): read Black Diamond's OWN landed transaction dates against Opal's served gold dates for each
FLOW_TIMING and INCOME_DATE segment of the V2 tie-out. READ-ONLY: S3 GETs/LISTs only; zero vendor calls.

BD side: s3://opal-data-assets/blackdiamond/49financial/silver_legacy/transactions/date=*/*.parquet (49 Financial's landed BD transaction record);
  account key = tie-out account without leading zeros = BD account_number (checked against blackdiamond/49f/silver/dim_account_xref).
  FLOW_TIMING: rows labelled external_flow Contribution|Withdrawal (fees included, BD labels them), dated by return_date.
  INCOME_DATE: rows with a non-zero income field, dated by return_date.
Opal side: s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/ external_flow / income_received on business_date.
Per segment, the dates of non-zero events on each side inside [start, end] are compared as SETS. confirmed = BD record covers the whole segment and
the two date sets are equal. Anything else is UNEXPLAINED with both date lists and a code (the code says WHY it is not confirmed; a code is not a cause).
Usage: python bd_dates_two_sided.py <txn_pickle> <gold_pickle> <segs_pickle> <xref_pickle> <out_private_json> <out_repo_json>
(the pickles are the S3 reads cached in .scratch; the private record holds account numbers and stays outside the repo.)
"""
import collections
import hashlib
import json
import pickle
import sys

BD_SOURCE = "s3://opal-data-assets/blackdiamond/49financial/silver_legacy/transactions/ (date=*/*.parquet, landed BD transactions; xref blackdiamond/49f/silver/dim_account_xref/date=2026-09-28/data.parquet)"
OPAL_SOURCE = "s3://opal-data-49financial/irpt/49financial/gold/account_return_daily/ (external_flow, income_received)"


def fnum(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def main():
    rows = pickle.load(open(sys.argv[1], "rb"))
    gold, _n = pickle.load(open(sys.argv[2], "rb"))
    segs = pickle.load(open(sys.argv[3], "rb"))
    xref = pickle.load(open(sys.argv[4], "rb"))
    by = collections.defaultdict(list)
    anyday = set()
    for r in rows:
        by[r["acct"]].append(r)
        for k in ("ret", "trade"):
            if r[k]:
                anyday.add(r[k])
    cov_end = max(r["ret"] for r in rows if r["ret"])
    out = []
    for sg in segs:
        a, s, e, reason = sg["account"], sg["segment"]["start"], sg["segment"]["end"], sg["reason"]
        ba = xref[a]["bd_account_number"] if a in xref else None
        flow = reason == "FLOW_TIMING"
        ce = min(e, cov_end)
        g = gold.get(a, {})
        idx = 0 if flow else 1
        opal = {d: v[idx] for d, v in g.items() if s <= d <= e and abs(v[idx]) >= 0.005}
        bd = collections.defaultdict(float)
        for r in by.get(ba, []):
            if not r["ret"] or not (s <= r["ret"] <= ce):
                continue
            if flow and r["flow"] in ("Contribution", "Withdrawal"):
                bd[r["ret"]] += fnum(r["mv"])
            elif not flow and fnum(r["income"]):
                bd[r["ret"]] += fnum(r["income"])
        bd = {d: v for d, v in bd.items() if abs(v) >= 0.005}
        opal_c = {d: v for d, v in opal.items() if d <= ce}
        tail = sorted(d for d in opal if d > ce)
        only_o = sorted(set(opal_c) - set(bd))
        only_b = sorted(set(bd) - set(opal_c))
        absent = [d for d in only_o if d not in anyday]
        genuine_o = [d for d in only_o if d in anyday]
        amt = sorted(d for d in set(bd) & set(opal_c) if abs(bd[d] - opal_c[d]) > max(1.0, 0.001 * abs(opal_c[d])))
        code = []
        if ba is None:
            code.append("NO_BD_ACCOUNT_IN_XREF")
        elif not by.get(ba):
            code.append("NO_BD_TXN_FOR_ACCOUNT")
        if absent:
            code.append("BD_RECORD_ABSENT_DAY")
        if genuine_o or only_b:
            code.append("DATE_SETS_DIFFER")
        if tail:
            code.append("BD_RECORD_ENDS_BEFORE_OPAL_EVENTS")
        if not opal and not bd:
            code.append("NO_EVENT_EITHER_SIDE")
        verdict = "confirmed" if not code else "UNEXPLAINED"
        note = "dates compared as sets on %s; %d Opal event dates, %d BD event dates inside the BD record's reach (BD record ends %s)" % (
            "return_date" if True else "", len(opal), len(bd), cov_end)
        if code:
            note += "; codes %s; opal-only dates on days the BD record holds rows: %s; opal-only dates on days the BD record holds NO row for any account: %s; " \
                    "bd-only dates: %s; opal dates after the BD record ends: %s" % (",".join(code), genuine_o, absent, only_b, tail)
        if amt:
            note += "; amounts differ on %d shared dates" % len(amt)
        out.append({"account": a, "segment": {"start": s, "end": e}, "reason": reason, "verdict": verdict, "codes": code,
                    "bd_date": ",".join(sorted(bd)), "opal_date": ",".join(sorted(opal)), "note": note})
    bv = dict(collections.Counter(x["verdict"] for x in out))
    bc = collections.Counter()
    for x in out:
        for c in (x["codes"] or ["NONE"]):
            bc[(x["reason"], x["verdict"], c)] += 1
    rec = {"measured_by": "0.9.0_WK_IRPT_DASHBD~81", "claim": "measured", "task_order": "IRPT_DASHBD.TO-DB-b-106", "bd_source": BD_SOURCE,
           "opal_source": OPAL_SOURCE, "bd_record_last_return_date": cov_end, "vendor_calls": 0, "by_verdict": bv,
           "by_reason_verdict_code": ["%s|%s|%s=%d" % (k[0], k[1], k[2], v) for k, v in sorted(bc.items())], "segments": out}
    pb = (json.dumps(rec, indent=1) + "\n").encode("utf-8")
    open(sys.argv[5], "wb").write(pb)
    repo = {"bd_source": BD_SOURCE, "vendor_calls": 0, "by_verdict": bv, "n_segments": len(out),
            "private_record": {"path": sys.argv[5], "sha256": hashlib.sha256(pb).hexdigest()}}
    open(sys.argv[6], "wb").write((json.dumps(repo, indent=1) + "\n").encode("utf-8"))
    print("OK: %d segments; by_verdict %s" % (len(out), bv))
    for k, v in sorted(bc.items()):
        print(k, v)


if __name__ == "__main__":
    main()
