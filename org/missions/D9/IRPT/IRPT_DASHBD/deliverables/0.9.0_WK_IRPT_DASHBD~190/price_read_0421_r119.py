"""IRPT_DASHBD round 119 (worker 0.9.0_WK_IRPT_DASHBD~190) -- DB-b-236, the 2026-04-21 price read (order Amendment 1).

READ-ONLY. Four analyses on the 49 Financial gold and the custodian position silver the producer declares:
  1. The account profile: the GRADED_DISAGREED accounts of account_return_daily 2026-04-21 against the
     holdings_performance_daily partition of the same day (no holdings row, status, excluded counts, excluded-weight bands).
  2. The security level: bucket and positions_prefix are READ FROM data/assets/scripts/gold/irpt_reporting/sources.json
     (the one entry carrying positions_prefix; nothing typed). Exactly two dim_position partitions are read, date=2026-04-20
     and date=2026-04-21, with the columns account_id, cusip, ticker_symbol, quantity_settled_unsettled, closing_price,
     secprice_lstupdte. Over the (account, security) pairs of the GRADED_DISAGREED accounts held on both days, classes by
     precedence: absent, stale, flat, moved (pair_counts), and the flagged pairs (absent, stale, flat) by security.
  3. The return triangle: for each GRADED_DISAGREED account with a pair priced on both days and a positive previous account
     value, R_pos against the holdings gold return and against the account value return, with the 2026-04-21 tolerance.
  4. A positive control on synthetic pairs and one synthetic triangle account.

Reads: GET only: account_return_daily data.parquet for 2026-04-20 and 2026-04-21, holdings_performance_daily data.parquet
for 2026-04-21, the 2026-04-21 account_return_daily manifest.json, and the two dim_position data.parquet objects.
Writes: one counts-only private file under the worker's private evidence folder. Nothing else; no record is written here.

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
PREV_DAY = "2026-04-20"
TABLE_ACCT = "account_return_daily"
TABLE_HOLD = "holdings_performance_daily"
SOURCES_REL = "data/assets/scripts/gold/irpt_reporting/sources.json"
REGISTRY_REL = "data/firm_registry.json"
FG_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~186/RD_FLOW_GUARD_READ_R118.json"
FOLDER = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~190/"
ANALYSIS_REL = FOLDER + "price_read_0421_r119.py"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~190"
PRIVATE_NAME = "price_read_0421_r119_counts.json"
BANDS = ("zero", "le_1pct", "1_to_10pct", "gt_10pct")
GUARD_GD = "GRADED_DISAGREED"
PAIR_KEYS = ("total", "absent", "stale", "flat", "moved")
FLAGGED = ("absent", "stale", "flat")
PRICE_SOURCE = "custodian closing_price, dim_position"
CLASS_WORDS = "not carried by this source"
POS_COLS = ["account_id", "cusip", "ticker_symbol", "quantity_settled_unsettled", "closing_price", "secprice_lstupdte"]


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


def split_uri(uri):
    rest = uri[len("s3://"):]
    bucket, _, key = rest.partition("/")
    return bucket, key


def gold_key(naming, table, day):
    bucket, key = split_uri(naming.address("irpt", FIRM_KEY, "gold", table, "date=%s" % day))
    return bucket, key.rstrip("/") + "/"


def read_cols(reader, bucket, key, cols):
    import pyarrow.parquet as pq
    body = reader.get(bucket, key)
    t = pq.read_table(io.BytesIO(body), columns=cols).to_pydict()
    return t, pq.read_schema(io.BytesIO(body)).names


def position_source(repo):
    """bucket and positions_prefix from the one sources.json entry that carries positions_prefix; nothing typed."""
    with open(os.path.join(repo, SOURCES_REL), "rb") as fh:
        doc = json.loads(fh.read().decode("utf-8"))
    hits = [(k, v) for k, v in doc.items() if isinstance(v, dict) and "positions_prefix" in v]
    if len(hits) != 1:
        raise Stop("sources.json carries %d entries with positions_prefix; exactly one is required" % len(hits))
    name, entry = hits[0]
    if not (entry.get("bucket") and entry.get("positions_prefix")):
        raise Stop("the positions entry lacks bucket or positions_prefix")
    return name, entry["bucket"], entry["positions_prefix"]


def band_of(w):
    if w is None or w == 0:
        return "zero"
    if w <= 0.01:
        return "le_1pct"
    if w <= 0.10:
        return "1_to_10pct"
    return "gt_10pct"


def profile(disagreed, holdings):
    """disagreed: set of account ids; holdings: dict account -> (status, excluded_count, excluded_weight)."""
    by_status = {}
    ex_zero = 0
    ex_pos = 0
    no_row = 0
    bands = dict((b, 0) for b in BANDS)
    for a in sorted(disagreed):
        h = holdings.get(a)
        if h is None:
            no_row += 1
            continue
        st = str(h[0])
        by_status[st] = by_status.get(st, 0) + 1
        if (h[1] or 0) > 0:
            ex_pos += 1
        else:
            ex_zero += 1
        bands[band_of(h[2])] += 1
    return {"accounts": len(disagreed), "no_holdings_row": no_row, "by_status": dict(sorted(by_status.items())),
            "excluded_count_zero": ex_zero, "excluded_count_positive": ex_pos, "excluded_weight_bands": bands}


def pair_class(price_t, price_0, lstupdte_t, day):
    if price_t is None:
        return "absent"
    if lstupdte_t is not None and str(lstupdte_t)[:10] < day:
        return "stale"
    if price_0 is not None and price_t == price_0:
        return "flat"
    return "moved"


def qty(r):
    q = r.get("quantity_settled_unsettled")
    return 0.0 if q is None else float(q)


def sec_key(r):
    return (r["account_id"], r.get("cusip") or r.get("ticker_symbol"))


def classify_pairs(accounts, rows_t, rows_0, day):
    """(account, security, class) for every pair held with quantity above zero on both days by an account in `accounts`."""
    prev = {}
    for r in rows_0:
        if r["account_id"] in accounts and qty(r) > 0 and sec_key(r)[1]:
            prev[sec_key(r)] = r
    out = []
    seen = set()
    for r in rows_t:
        if r["account_id"] not in accounts or not qty(r) > 0 or not sec_key(r)[1]:
            continue
        k = sec_key(r)
        if k in seen or k not in prev:
            continue
        seen.add(k)
        out.append((k[0], k[1], pair_class(r.get("closing_price"), prev[k].get("closing_price"), r.get("secprice_lstupdte"), day)))
    return out


def pair_counts(pairs):
    out = dict((k, 0) for k in PAIR_KEYS)
    for _a, _s, c in pairs:
        out["total"] += 1
        out[c] += 1
    return out


def triangle(dis_pv, mv0, rows_t, rows_0, tau):
    """dis_pv: account -> (p_gold, V1); mv0: account -> V0. R_pos per account over its pairs priced on both days."""
    prev = dict((sec_key(r), r) for r in rows_0 if r["account_id"] in dis_pv and qty(r) > 0 and sec_key(r)[1])
    num = {}
    den = {}
    seen = set()
    for r in rows_t:
        k = sec_key(r)
        if k in prev and k not in seen and r.get("closing_price") is not None and prev[k].get("closing_price") is not None:
            seen.add(k)
            q0 = qty(prev[k])
            p0 = float(prev[k]["closing_price"])
            p1 = float(r["closing_price"])
            num[k[0]] = num.get(k[0], 0.0) + q0 * (p1 - p0)
            den[k[0]] = den.get(k[0], 0.0) + q0 * p0
    out = {"accounts": 0, "agrees_holdings_gold": 0, "agrees_account_value": 0, "both": 0, "neither": 0, "tolerance": tau}
    for a, (pg, v) in dis_pv.items():
        v0 = mv0.get(a)
        if a not in num or not den[a] > 0 or not v0 or not float(v0) > 0 or pg is None or v is None:
            continue
        rpos = num[a] / den[a]
        vv = float(v) / float(v0) - 1.0
        ap = abs(rpos - float(pg)) <= tau
        av = abs(rpos - vv) <= tau
        out["accounts"] += 1
        out["agrees_holdings_gold"] += int(ap)
        out["agrees_account_value"] += int(av)
        out["both"] += int(ap and av)
        out["neither"] += int((not ap) and (not av))
    return out


def securities_of(pairs):
    """Flagged pairs grouped by (security, class): at most 25 entries, most affected first."""
    groups = {}
    for a, s, c in pairs:
        if c in FLAGGED:
            groups.setdefault((s, c), set()).add(a)
    ordered = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0][0], kv[0][1]))
    return [{"security": s, "security_class": CLASS_WORDS, "price_source": PRICE_SOURCE, "price_state": c,
             "accounts_affected": len(accs), "claim": "measured"} for (s, c), accs in ordered[:25]]


def positive_control():
    rows_0 = [
        {"account_id": "p1", "cusip": "C1", "ticker_symbol": None, "quantity_settled_unsettled": 5, "closing_price": 1.0,
         "secprice_lstupdte": "2026-04-20"},
        {"account_id": "p2", "cusip": "C2", "ticker_symbol": None, "quantity_settled_unsettled": 5, "closing_price": 1.0,
         "secprice_lstupdte": "2026-04-20"},
        {"account_id": "p3", "cusip": "C3", "ticker_symbol": None, "quantity_settled_unsettled": 5, "closing_price": 2.0,
         "secprice_lstupdte": "2026-04-20"},
        {"account_id": "p4", "cusip": "C4", "ticker_symbol": None, "quantity_settled_unsettled": 5, "closing_price": 1.0,
         "secprice_lstupdte": "2026-04-20"},
    ]
    rows_t = [
        {"account_id": "p1", "cusip": "C1", "ticker_symbol": None, "quantity_settled_unsettled": 5, "closing_price": 1.0,
         "secprice_lstupdte": "2026-04-21"},
        {"account_id": "p2", "cusip": "C2", "ticker_symbol": None, "quantity_settled_unsettled": 5, "closing_price": None,
         "secprice_lstupdte": "2026-04-21"},
        {"account_id": "p3", "cusip": "C3", "ticker_symbol": None, "quantity_settled_unsettled": 5, "closing_price": 2.0,
         "secprice_lstupdte": "2026-04-20"},
        {"account_id": "p4", "cusip": "C4", "ticker_symbol": None, "quantity_settled_unsettled": 5, "closing_price": 1.1,
         "secprice_lstupdte": "2026-04-21"},
    ]
    observed = classify_pairs(set(["p1", "p2", "p3", "p4"]), rows_t, rows_0, DAY)
    obs = dict(((a, s), c) for a, s, c in observed)
    exp = {("p1", "C1"): "flat", ("p2", "C2"): "absent", ("p3", "C3"): "stale", ("p4", "C4"): "moved"}
    tri_rows_0 = [{"account_id": "t1", "cusip": "C9", "ticker_symbol": None, "quantity_settled_unsettled": 10, "closing_price": 100.0,
                   "secprice_lstupdte": "2026-04-20"}]
    tri_rows_t = [{"account_id": "t1", "cusip": "C9", "ticker_symbol": None, "quantity_settled_unsettled": 10, "closing_price": 98.0,
                   "secprice_lstupdte": "2026-04-21"}]
    tri = triangle({"t1": (-0.02, 900.0)}, {"t1": 1000.0}, tri_rows_t, tri_rows_0, 0.001244)
    tri_exp = {"accounts": 1, "agrees_holdings_gold": 1, "agrees_account_value": 0, "both": 0, "neither": 0, "tolerance": 0.001244}
    passed = obs == exp and tri == tri_exp
    return {"passed": bool(passed),
            "description": "four synthetic pairs through the pair classifier (a flat price, an absent price, a stale "
                           "secprice_lstupdte, a moved price) and one synthetic account through the return triangle "
                           "(R_pos -0.02 against a holdings return of -0.02 and an account value return of -0.1, tolerance 0.001244)",
            "expected": "; ".join("%s/%s=%s" % (a, s, c) for (a, s), c in sorted(exp.items())) + "; triangle " + json.dumps(tri_exp, sort_keys=True),
            "observed": "; ".join("%s/%s=%s" % (a, s, c) for (a, s), c in sorted(obs.items())) + "; triangle " + json.dumps(tri, sort_keys=True)}


def main(argv):
    repo = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    fg = json.loads(Path(repo, FG_REL).read_bytes().decode("utf-8"))
    d0 = fg["dates"][0]
    if d0["date"] != DAY:
        raise Stop("the flow-guard record's first date is not %s" % DAY)
    value_rows = d0["by_cause"]["VALUE"] + d0["by_cause"]["FLOW_AND_VALUE"]
    print("FLOW-GUARD RECORD %s: VALUE %d + FLOW_AND_VALUE %d = value_rows %d"
          % (DAY, d0["by_cause"]["VALUE"], d0["by_cause"]["FLOW_AND_VALUE"], value_rows))

    pc = positive_control()
    print("POSITIVE CONTROL: passed=%s" % pc["passed"])
    if not pc["passed"]:
        raise Stop("the positive control failed: %s" % pc["observed"])

    sys.path.insert(0, repo)
    from lib import opal_naming as naming
    with open(os.path.join(repo, REGISTRY_REL), "rb") as fh:
        registry = json.loads(fh.read().decode("utf-8"))
    firms = [f for f in registry.get("firms", []) if f.get("firm_id") == FIRM_KEY]
    if len(firms) != 1:
        raise Stop("the registry does not enumerate exactly one row for the firm")
    src_name, pos_bucket, pos_prefix = position_source(repo)

    reader = Reader()
    b, k = gold_key(naming, TABLE_ACCT, DAY)
    ar, ar_names = read_cols(reader, b, k + "data.parquet", ["account_id", "guard_state", "holdings_price_return", "market_value_eod"])
    b0, k0 = gold_key(naming, TABLE_ACCT, PREV_DAY)
    ar0, _n0 = read_cols(reader, b0, k0 + "data.parquet", ["account_id", "market_value_eod"])
    bm = b
    man = json.loads(reader.get(bm, k + "manifest.json").decode("utf-8"))
    try:
        tau = float(man["thresholds"]["tolerance"])
    except (KeyError, TypeError, ValueError):
        raise Stop("the 2026-04-21 manifest carries no numeric thresholds.tolerance; a BLOCKING row is owed")
    bh, kh = gold_key(naming, TABLE_HOLD, DAY)
    hp, hp_names = read_cols(reader, bh, kh + "data.parquet", ["account_id", "status", "excluded_count", "excluded_weight"])

    guard_counts = {}
    disagreed = set()
    dis_pv = {}
    for a, g, p, v in zip(ar["account_id"], ar["guard_state"], ar["holdings_price_return"], ar["market_value_eod"]):
        guard_counts[str(g)] = guard_counts.get(str(g), 0) + 1
        if g == GUARD_GD:
            disagreed.add(a)
            dis_pv[a] = (p, v)
    mv0 = dict(zip(ar0["account_id"], ar0["market_value_eod"]))
    holdings = {}
    hp_dups = 0
    for a, s, c, w in zip(hp["account_id"], hp["status"], hp["excluded_count"], hp["excluded_weight"]):
        if a in holdings:
            hp_dups += 1
        holdings[a] = (s, c, w)
    if hp_dups:
        raise Stop("the holdings partition carries %d duplicate account rows; a BLOCKING row is owed" % hp_dups)
    prof = profile(disagreed, holdings)
    if sum(prof["excluded_weight_bands"].values()) != prof["accounts"] - prof["no_holdings_row"]:
        raise Stop("excluded-weight bands do not sum")
    if prof["excluded_count_zero"] + prof["excluded_count_positive"] != prof["accounts"] - prof["no_holdings_row"]:
        raise Stop("excluded counts do not sum")
    if sum(prof["by_status"].values()) != prof["accounts"] - prof["no_holdings_row"]:
        raise Stop("by_status does not sum")

    def positions(day):
        t, names = read_cols(reader, pos_bucket, "%sdate=%s/data.parquet" % (pos_prefix, day), POS_COLS)
        return [dict(zip(t.keys(), vals)) for vals in zip(*t.values())], names
    rows_t, pos_names_t = positions(DAY)
    rows_0, pos_names_0 = positions(PREV_DAY)
    pairs = classify_pairs(disagreed, rows_t, rows_0, DAY)
    pcounts = pair_counts(pairs)
    flagged_total = pcounts["absent"] + pcounts["stale"] + pcounts["flat"]
    secs = securities_of(pairs)
    tri = triangle(dis_pv, mv0, rows_t, rows_0, tau)
    if not secs:
        raise Stop("no flagged pair: the security list would be empty; a BLOCKING row is owed")

    sec_block = {
        "state": "READ",
        "words": ("The security grain exists in the custodian position silver that the producer declares in sources.json "
                  "(entry " + src_name + "): dim_position, one row per account and security per day. Its 2026-04-20 and 2026-04-21 partitions "
                  "were read with the six declared columns. Pairs are the (account, security) pairs of the GRADED_DISAGREED "
                  "accounts held with positive quantity on both days; the security is the cusip, else the ticker. Classes by "
                  "precedence: absent (no closing price on 2026-04-21), stale (secprice_lstupdte before 2026-04-21), flat "
                  "(closing price equal to the previous day's), moved (the rest). The custodian position source carries no "
                  "security class: no class table was read, as the order grants no such read, so the class is the words "
                  + CLASS_WORDS + "."),
        "source": {"file": SOURCES_REL + " (entry " + src_name + ")",
                   "table": "dim_position, custodian position silver, partitions date=2026-04-20 and date=2026-04-21",
                   "words": "bucket and positions_prefix read from the declared entry; exactly two partitions read; no other prefix of the source touched"},
        "pair_counts": pcounts,
        "securities": secs,
        "by_price_source": {PRICE_SOURCE: flagged_total},
        "by_security_class": {CLASS_WORDS: flagged_total},
        "claim": "measured",
    }

    os.makedirs(PRIVATE_DIR, exist_ok=True)
    private = {"scope": "counts only: partition row counts, guard-state counts, column counts, profile, pair and triangle counts",
               "account_return_rows": len(ar["account_id"]), "guard_state_counts": dict(sorted(guard_counts.items())),
               "holdings_rows": len(hp["account_id"]), "holdings_columns": len(hp_names),
               "position_rows_2026_04_21": len(rows_t), "position_rows_2026_04_20": len(rows_0),
               "position_columns_2026_04_21": len(pos_names_t), "profile": prof, "pair_counts": pcounts,
               "flagged_pairs": flagged_total, "securities_listed": len(secs), "triangle": tri, "s3_reads": reader.gets}
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(private, indent=2, sort_keys=True) + "\n")

    out = {"date": DAY, "value_rows": value_rows, "account_profile": prof, "security_level": sec_block,
           "return_triangle": tri, "positive_control": pc, "s3_reads": reader.gets,
           "analysis_sha256": hashlib.sha256(Path(os.path.abspath(__file__)).read_bytes()).hexdigest(),
           "analysis_file": ANALYSIS_REL}
    print("RESULT JSON: " + json.dumps(out, sort_keys=True, indent=1))
    print("COUNTS: account_return_rows %d; guard_state_counts %s; holdings_rows %d; holdings_columns %d; position_rows %d and %d; "
          "s3_reads %d" % (len(ar["account_id"]), dict(sorted(guard_counts.items())), len(hp["account_id"]), len(hp_names),
                           len(rows_t), len(rows_0), reader.gets))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Stop as e:
        print("STOP: %s" % e)
        sys.exit(3)
