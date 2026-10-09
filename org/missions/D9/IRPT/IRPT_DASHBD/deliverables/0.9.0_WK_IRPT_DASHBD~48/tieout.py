"""Tie-out of the adapter's total_return_daily against the firm's OWN reported source (C-TIEOUT, PRD v0.8 @3eb7dbcf36).

The reported source is the Commonwealth delivery landed in the data store: the silver `performance` table (one row per
account x reporting period, PerfType TWR, PerfNum in percent) joined through the delivery's own `crosswalk` table, which
maps a Commonwealth account to the current custody account. Reads only: S3 get/list through boto3, nothing written
except the record JSON. Usage: python tieout.py <repo_root> <adapter.parquet> <record.json>
"""
import datetime as dt
import hashlib
import io
import json
import sys
from pathlib import Path

import pandas as pd

TOL_PP = 0.35
DELIVERY = "2026-06-23"           # the date the vendor's own files carry (CTO endpoint call 2), not the landing day
WINDOW_FROM = dt.date(2026, 6, 1)  # Commonwealth reports for dates after this fall in or beside the source's coverage
CLASSES = [
    "WINDOW_ENDS_BEFORE_SOURCE_COVERAGE",
    "WINDOW_STARTS_BEFORE_SOURCE_BASE",
    "ACCOUNT_NOT_HELD_IN_WINDOW",
    "DAY_NOT_MEASURABLE_IN_WINDOW",
    "NO_TRADING_DAY_IN_WINDOW",
    "RETURN_DIFFERS_BEYOND_TOLERANCE",
]


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main(root, pq_path, rec_path):
    sys.path.insert(0, str(Path(root) / "lib"))
    import boto3
    import opal_naming
    import pyarrow.parquet as pq
    import trading_calendar as cal
    decl = json.loads((Path(__file__).resolve().parent / "adapter_source.json").read_bytes().decode("utf-8"))
    entry = [v for k, v in decl.items() if isinstance(v, dict)][0]
    row = opal_naming.lookup(entry["registry_key"])
    firm, src_system = row["firm"], row["vendor"]
    cmp_system = "commonwealth"
    s3 = boto3.client("s3")

    def get(system, table, obj):
        u = opal_naming.address(system, firm, "silver", table, "date=%s" % DELIVERY, object=obj)
        b, k = u[len("s3://"):].split("/", 1)
        return pq.read_table(io.BytesIO(s3.get_object(Bucket=b, Key=k)["Body"].read())).to_pandas(), u

    perf, perf_uri = get(cmp_system, "performance", "reporting_period=Month/part-00000.parquet")
    xw, xw_uri = get(cmp_system, "crosswalk", "crosswalk.parquet")
    xw = xw[xw.status == "MATCHED"][["commonwealth_account", "current_account"]]
    out = pd.read_parquet(pq_path)
    first_part = min(out.business_date)
    first_part = dt.date.fromisoformat(first_part)
    ret = {(r.account_id, r.business_date): (r.total_return_daily, r.day_quality)
           for r in out.itertuples()}
    held = set(zip(out.account_id, out.business_date))

    perf = perf[(perf.PerfType == "TWR") & (perf.EndDate >= WINDOW_FROM)].merge(
        xw, left_on="Account_Number", right_on="commonwealth_account")
    perf = perf.sort_values(["current_account", "StartDate", "EndDate"]).reset_index(drop=True)

    within, misses, per_class = 0, [], {c: 0 for c in CLASSES}
    for r in perf.itertuples():
        acct = r.current_account
        td = [d for d in cal.trading_days_between(r.StartDate, r.EndDate)]
        base = {"account_key": sha("tieout|" + acct)[:16], "window": [r.StartDate.isoformat(), r.EndDate.isoformat()],
                "reported_pp": float(r.PerfNum), "adapter_pp": None}
        cls, ev = None, None
        base["source_rows_in_window"] = sum(1 for d in td if (acct, d.isoformat()) in held)
        base["trading_days_in_window"] = len(td)
        if not td:
            cls, ev = "NO_TRADING_DAY_IN_WINDOW", "the window holds no trading day under lib/trading_calendar.py"
        elif td[-1] < first_part:
            cls = "WINDOW_ENDS_BEFORE_SOURCE_COVERAGE"
            ev = "last trading day %s precedes the source's first value partition %s" % (td[-1], first_part)
        elif cal.prev_trading_day(td[0]) < first_part:
            cls = "WINDOW_STARTS_BEFORE_SOURCE_BASE"
            ev = ("the base value for the window is the prior trading day %s, before the source's first value partition %s; "
                  "the source cannot compound the window" % (cal.prev_trading_day(td[0]), first_part))
            sub = [d for d in td if d >= first_part + dt.timedelta(days=1) and cal.prev_trading_day(d) >= first_part]
            vals = [ret.get((acct, d.isoformat()), (None, None))[0] for d in sub]
            if sub and all(v is not None and v == v for v in vals):
                g = 1.0
                for v in vals:
                    g *= 1.0 + v
                base["adapter_partial_pp"] = round((g - 1.0) * 100.0, 6)
                base["adapter_partial_window"] = [sub[0].isoformat(), sub[-1].isoformat()]
        else:
            vals = []
            for d in td:
                if (acct, d.isoformat()) not in held:
                    cls, ev = "ACCOUNT_NOT_HELD_IN_WINDOW", "no value row for %s" % d
                    break
                v, q = ret[(acct, d.isoformat())]
                if v is None or v != v:
                    cls, ev = "DAY_NOT_MEASURABLE_IN_WINDOW", "%s is %s" % (d, q)
                    break
                vals.append(v)
            if cls is None:
                g = 1.0
                for v in vals:
                    g *= 1.0 + v
                base["adapter_pp"] = round((g - 1.0) * 100.0, 6)
                if abs(base["adapter_pp"] - r.PerfNum) <= TOL_PP:
                    within += 1
                    continue
                cls = "RETURN_DIFFERS_BEYOND_TOLERANCE"
                ev = "compounded %d trading days; |difference| %.4f pp" % (len(vals), abs(base["adapter_pp"] - r.PerfNum))
        base["class"], base["evidence"] = cls, ev
        per_class[cls] += 1
        misses.append(base)

    cols = list(pq.read_table(pq_path).schema.names)
    rec = {
        "source": src_system,
        "comparison_source": "%s (Portfolio Accounting Performance delivery dated %s, silver performance table, Month rows, TWR, "
                             "mapped to custody accounts through the same delivery's crosswalk, status MATCHED)" % (cmp_system, DELIVERY),
        "accounts": int(perf.current_account.nunique()),
        "denominator": int(len(perf)),
        "denominator_grain": "account-windows: one Commonwealth Month row (PerfNum, percent) per matched account with EndDate on or after %s" % WINDOW_FROM,
        "within": int(within),
        "tolerance_pp": TOL_PP,
        "classes": CLASSES,
        "class_definitions": {
            "WINDOW_ENDS_BEFORE_SOURCE_COVERAGE": "the reported window ends before the source's first value partition: the source holds no value anywhere in it",
            "WINDOW_STARTS_BEFORE_SOURCE_BASE": "the reported window starts so early that its base day (the prior trading day) precedes the source's first value partition, so the source cannot compound the whole window; source_rows_in_window of trading_days_in_window days are held",
            "ACCOUNT_NOT_HELD_IN_WINDOW": "the window is inside the source's coverage but the account has no value row on some day of it",
            "DAY_NOT_MEASURABLE_IN_WINDOW": "every day is held but one is NOT_MEASURABLE (no positive prior value), so the link breaks",
            "NO_TRADING_DAY_IN_WINDOW": "the reported window holds no trading day",
            "RETURN_DIFFERS_BEYOND_TOLERANCE": "the window is fully compounded from MEASURED or LARGE_FLOW days and differs from the reported figure by more than the tolerance",
        },
        "class_counts": per_class,
        "misses": misses,
        "output_columns": cols,
        "output_rows": int(len(out)),
        "output_accounts": int(out.account_id.nunique()),
        "output_sha256": hashlib.sha256(Path(pq_path).read_bytes()).hexdigest(),
        "notes": "Commonwealth-reported returns for this firm WERE found on S3 (per the issuer's ruling on PRD v0.8 note msg 2350), so Commonwealth is the comparison_source; it is the unregistered candidate source, not a registered one. No window it reports overlaps the source's value coverage for the same account: see surprise rows IRPT_DASHBD-W48-S1 and IRPT_DASHBD-W48-S2. within=0 is a measurement of that gap, not of the adapter's arithmetic.",
        "reads": {"comparison_performance": perf_uri.rsplit("/", 2)[0], "comparison_crosswalk": xw_uri.rsplit("/", 1)[0]},
    }
    Path(rec_path).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print("denominator %d account-windows over %d accounts; within %d; misses %d; classes %s" %
          (rec["denominator"], rec["accounts"], within, len(misses), per_class))


if __name__ == "__main__":
    main(*sys.argv[1:4])
