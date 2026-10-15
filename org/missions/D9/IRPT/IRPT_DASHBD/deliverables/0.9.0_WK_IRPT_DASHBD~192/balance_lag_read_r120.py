"""IRPT_DASHBD round 120 (worker 0.9.0_WK_IRPT_DASHBD~192) -- DB-b-238, the balance-lag read (CTO analysis ruling 2).

READ-ONLY. The custodian balance source (dim_balance) against the custodian position source (dim_position), for the
GRADED_DISAGREED accounts of the 49 Financial account_return_daily partition of 2026-04-21:
  1. The three intervals 2026-04-20 to 04-21, 04-21 to 04-22 and 04-20 to 04-22: the six counts, with the definitions of
     the round-120 checker (R, dP, dB, dT, Q; tau = the 2026-04-21 manifest tolerance).
  2. The other five dates, in order: for each, the interval from its previous trading day to it, over its own
     GRADED_DISAGREED accounts, with the same definitions and the same tau.

Reads: GET only. The account_return_daily data.parquet and manifest.json of 2026-04-21, the account_return_daily
data.parquet of each other date, and the dim_balance and dim_position data.parquet objects of the dates named above.
The bucket and both prefixes are READ FROM data/assets/scripts/gold/irpt_reporting/sources.json (the one entry that
carries positions_prefix); the gold addresses come from lib/opal_naming.py address().
Writes: one counts-only private file under the worker's private evidence folder. Nothing else.

Usage: python -I <this file> <repo_root>
"""
import hashlib
import io
import json
import os
import sys
from pathlib import Path

FIRM_KEY = "49financial"
DAY = "2026-04-21"
DAYS = ("2026-04-20", "2026-04-21", "2026-04-22")
INTERVALS = (("2026-04-20", "2026-04-21"), ("2026-04-21", "2026-04-22"), ("2026-04-20", "2026-04-22"))
OTHERS = ("2026-07-02", "2026-10-13", "2026-09-22", "2026-10-06", "2026-09-16")
TABLE_ACCT = "account_return_daily"
GUARD_GD = "GRADED_DISAGREED"
SOURCES_REL = "data/assets/scripts/gold/irpt_reporting/sources.json"
FG_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~186/RD_FLOW_GUARD_READ_R118.json"
FOLDER = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~192/"
ANALYSIS_REL = FOLDER + "balance_lag_read_r120.py"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~192"
PRIVATE_NAME = "balance_lag_read_r120_counts.json"
COUNT_KEYS = ("accounts", "balance_positions_agrees_position_mv", "position_mv_agrees_price_return",
              "balance_positions_agrees_price_return", "balance_total_agrees_balance_positions", "accounts_with_quantity_change")
BAL_COLS = ["account_id", "net_mv_positions", "net_mv_plus_cash", "margin_balance"]
POS_COLS = ["account_id", "cusip", "ticker_symbol", "quantity_settled_unsettled", "market_value_settled_unsettled", "closing_price"]


class Stop(Exception):
    pass


class Reader(object):
    """GET only. There is deliberately no method that changes a remote object."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.gets = 0

    def get(self, bucket, key):
        self.gets += 1
        return self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()


def fl(x):
    return None if x is None else float(x)


def read_table(reader, bucket, key, cols):
    import pyarrow.parquet as pq
    body = reader.get(bucket, key)
    return pq.read_table(io.BytesIO(body), columns=cols).to_pydict()


def gold_prefix(naming, table_name, day):
    """bucket and the key prefix (with a trailing slash) of one gold partition, from the address builder."""
    rest = naming.address("irpt", FIRM_KEY, "gold", table_name, "date=%s" % day)[len("s3://"):]
    bucket, _, key = rest.partition("/")
    return bucket, key.rstrip("/") + "/"


def source(repo):
    """bucket, positions_prefix and balance_prefix from the one sources.json entry that carries positions_prefix."""
    with open(os.path.join(repo, SOURCES_REL), "rb") as fh:
        doc = json.loads(fh.read().decode("utf-8"))
    hits = [v for v in doc.values() if isinstance(v, dict) and "positions_prefix" in v]
    if len(hits) != 1:
        raise Stop("sources.json carries %d entries with positions_prefix; exactly one is required" % len(hits))
    ent = hits[0]
    if not (ent.get("bucket") and ent.get("positions_prefix") and ent.get("balance_prefix")):
        raise Stop("the positions entry lacks bucket, positions_prefix or balance_prefix")
    return ent["bucket"], ent["positions_prefix"], ent["balance_prefix"]


def flagged_set(reader, naming, day):
    """GRADED_DISAGREED accounts of the account_return_daily partition of the day; also its bucket and prefix."""
    bucket, prefix = gold_prefix(naming, TABLE_ACCT, day)
    t = read_table(reader, bucket, prefix + "data.parquet", ["account_id", "guard_state"])
    dis = set(a for a, s in zip(t["account_id"], t["guard_state"]) if s == GUARD_GD)
    return dis, bucket, prefix


def tolerance(reader, bucket, prefix):
    man = json.loads(reader.get(bucket, prefix + "manifest.json").decode("utf-8"))
    return float(man["thresholds"]["tolerance"])


def balances(reader, bucket, bal_prefix, day, dis):
    """account -> (net_mv_positions, net_mv_plus_cash + margin_balance), for the flagged accounts."""
    t = read_table(reader, bucket, bal_prefix + "date=%s/data.parquet" % day, BAL_COLS)
    out = {}
    for i, a in enumerate(t["account_id"]):
        if a in dis:
            out[a] = (fl(t["net_mv_positions"][i]), (fl(t["net_mv_plus_cash"][i]) or 0.0) + (fl(t["margin_balance"][i]) or 0.0))
    return out


def positions(reader, bucket, pos_prefix, day, dis):
    """(account, security) -> (quantity, market value, closing price); the security is the cusip, else the ticker."""
    t = read_table(reader, bucket, pos_prefix + "date=%s/data.parquet" % day, POS_COLS)
    out = {}
    for i, a in enumerate(t["account_id"]):
        sec = t["cusip"][i] or t["ticker_symbol"][i]
        if a in dis and sec:
            out[(a, sec)] = (fl(t["quantity_settled_unsettled"][i]), fl(t["market_value_settled_unsettled"][i]), fl(t["closing_price"][i]))
    return out


def interval_counts(accounts, bal0, bal1, pos0, pos1, tau):
    """The six counts of one interval. accounts: set. bal*: account -> (net_mv_positions, total). pos*: (account, security) -> (q, mv, p)."""
    acc = {}
    for key, (q0, mv0, p0) in pos0.items():
        if key[0] not in accounts or q0 is None or not q0 > 0 or p0 is None or mv0 is None:
            continue
        x = pos1.get(key)
        if x is None or x[1] is None or x[2] is None:
            continue
        q1, mv1, p1 = x
        r = acc.setdefault(key[0], [0.0, 0.0, 0.0, 0.0, False])
        r[0] += q0 * (p1 - p0)
        r[1] += q0 * p0
        r[2] += mv0
        r[3] += mv1
        r[4] = r[4] or (q1 != q0)
    out = {k: 0 for k in COUNT_KEYS}
    for a, (num, den, m0, m1, qchg) in acc.items():
        b0, b1 = bal0.get(a), bal1.get(a)
        if b0 is None or b1 is None or not den > 0 or not m0 > 0:
            continue
        p0n, t0 = b0
        p1n, t1 = b1
        if p0n is None or p1n is None or t0 is None or t1 is None or not p0n > 0 or not t0 > 0:
            continue
        rr, dp, db, dt = num / den, m1 / m0 - 1.0, p1n / p0n - 1.0, t1 / t0 - 1.0
        out["accounts"] += 1
        out["balance_positions_agrees_position_mv"] += int(abs(db - dp) <= tau)
        out["position_mv_agrees_price_return"] += int(abs(dp - rr) <= tau)
        out["balance_positions_agrees_price_return"] += int(abs(db - rr) <= tau)
        out["balance_total_agrees_balance_positions"] += int(abs(dt - db) <= tau)
        out["accounts_with_quantity_change"] += int(qchg)
    return out


def main(argv):
    repo = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    fg = json.loads(Path(repo, FG_REL).read_bytes().decode("utf-8"))
    d0 = fg["dates"][0]
    if d0["date"] != DAY:
        raise Stop("the flow-guard record's first date is not %s" % DAY)
    sys.path.insert(0, repo)
    from lib import opal_naming as naming
    from lib import trading_calendar as cal
    bucket, pos_prefix, bal_prefix = source(repo)

    reader = Reader()
    dis, abucket, aprefix = flagged_set(reader, naming, DAY)
    if len(dis) != d0["rows_graded_disagreed"]:
        raise Stop("the flagged set (%d) differs from the flow-guard record (%s)" % (len(dis), d0["rows_graded_disagreed"]))
    tau = tolerance(reader, abucket, aprefix)

    bal = {}
    pos = {}
    for d in DAYS:
        bal[d] = balances(reader, bucket, bal_prefix, d, dis)
        pos[d] = positions(reader, bucket, pos_prefix, d, dis)
    intervals = []
    for d_from, d_to in INTERVALS:
        c = interval_counts(dis, bal[d_from], bal[d_to], pos[d_from], pos[d_to], tau)
        intervals.append(dict(c, **{"from": d_from, "to": d_to}))

    others = []
    for d in OTHERS:
        prior = str(cal.prev_trading_day(d))
        dsd, _b, _p = flagged_set(reader, naming, d)
        tb = {prior: balances(reader, bucket, bal_prefix, prior, dsd), d: balances(reader, bucket, bal_prefix, d, dsd)}
        tp = {prior: positions(reader, bucket, pos_prefix, prior, dsd), d: positions(reader, bucket, pos_prefix, d, dsd)}
        c = interval_counts(dsd, tb[prior], tb[d], tp[prior], tp[d], tau)
        others.append({"date": d, "prior_date": prior, "accounts_flagged": len(dsd), "accounts": c["accounts"],
                       "balance_positions_agrees_position_mv": c["balance_positions_agrees_position_mv"],
                       "position_mv_agrees_price_return": c["position_mv_agrees_price_return"]})

    result = {"date": DAY, "accounts_flagged": len(dis), "tolerance": tau, "intervals": intervals, "other_dates": others,
              "s3_reads": reader.gets, "flow_guard_rows_graded_disagreed": d0["rows_graded_disagreed"],
              "analysis_file": ANALYSIS_REL,
              "analysis_sha256": hashlib.sha256(Path(os.path.abspath(__file__)).read_bytes()).hexdigest()}
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("RESULT JSON: " + json.dumps(result, sort_keys=True, indent=1))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Stop as e:
        print("STOP: %s" % e)
        sys.exit(3)
