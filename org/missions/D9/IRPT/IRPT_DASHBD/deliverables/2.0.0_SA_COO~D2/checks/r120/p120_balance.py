"""IRPT_DASHBD round 120, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-238, the BALANCE-LAG READ (CTO analysis @5e358b0a8f ruling 2).

  DB-b-238 (~192) the custodian balance source (`dim_balance`: net_mv_positions, net_mv_plus_cash, margin_balance) against the custodian position source
                  (`dim_position`: quantity_settled_unsettled, market_value_settled_unsettled, closing_price) for the 943 accounts the guard
                  disagreed on 2026-04-21, over 2026-04-20 -> 04-21, 04-21 -> 04-22 and 04-20 -> 04-22; and the same shape on the other five
                  dates. A READ: counts and shares only; nothing written.                                         DB120-2-AC1

Per account of the GRADED_DISAGREED set, for an interval t0 -> t1, over the pairs (account, security = cusip else ticker) held (quantity above zero) on
t0 and present with a market value and a closing price on t1 and a closing price on t0:
  R  = sum q0 * (p1 - p0) / sum q0 * p0                 the price-only return at the previous day's quantities
  dP = sum mv1 / sum mv0 - 1  (over those pairs)          the position file's own market-value change
  dB = net_mv_positions(t1) / net_mv_positions(t0) - 1    the balance file's positions component change
  dT = (net_mv_plus_cash + margin_balance)(t1) / (...)(t0) - 1    the producer's account value change
  Q  = the account holds at least one such pair whose quantity differs between t0 and t1
An account counts when its sum q0 * p0 and sum mv0 and net_mv_positions(t0) and (net_mv_plus_cash + margin_balance)(t0) are above zero and the
t1 balance values exist. With tau = the 2026-04-21 manifest tolerance: balance_positions_agrees_position_mv counts |dB - dP| <= tau;
position_mv_agrees_price_return |dP - R| <= tau; balance_positions_agrees_price_return |dB - R| <= tau; balance_total_agrees_balance_positions
|dT - dB| <= tau; accounts_with_quantity_change counts Q. The checker recomputes the three intervals to the unit from the custodian sources.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~192/RD_BALANCE_LAG_R120.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~192/balance_lag_read_r120.py"
FG_REL = D + "0.9.0_WK_IRPT_DASHBD~186/RD_FLOW_GUARD_READ_R118.json"
DAYS = ("2026-04-20", "2026-04-21", "2026-04-22")
INTERVALS = (("2026-04-20", "2026-04-21"), ("2026-04-21", "2026-04-22"), ("2026-04-20", "2026-04-22"))
OTHERS = ("2026-07-02", "2026-10-13", "2026-09-22", "2026-10-06", "2026-09-16")
FIRM = "49financial"
CLAIMS = ("measured", "inferred", "held", "absent")
COUNT_KEYS = ("accounts", "balance_positions_agrees_position_mv", "position_mv_agrees_price_return", "balance_positions_agrees_price_return",
              "balance_total_agrees_balance_positions", "accounts_with_quantity_change")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item",
                "delete_item", "update_item", "write_table", "write_to_dataset", ".to_parquet(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage")
ISO = re.compile(r"\d{4}-\d{2}-\d{2}$")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def nes(x):
    return isinstance(x, str) and x.strip() != ""


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def digit_runs(x, key=""):
    if isinstance(x, dict):
        return [h for k, v in x.items() for h in digit_runs(v, str(k))]
    if isinstance(x, list):
        return [h for v in x for h in digit_runs(v, key)]
    if isinstance(x, str) and key not in DIGIT_OK_KEYS:
        return LONG_DIGITS.findall(x)
    return []


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return json.loads(p.read_bytes().decode("utf-8"))


def is_tracked(root, rel):
    return subprocess.run(["git", "-C", str(root), "ls-files", "--error-unmatch", rel], capture_output=True, text=True).returncode == 0


def fl(x):
    return None if x is None else float(x)


# ------------------------------------------------------------------------------------------------ the interval counts (pure)
def interval_counts(accounts, bal0, bal1, pos0, pos1, tau):
    """accounts: set. bal*: account -> (net_mv_positions, total) with total = net_mv_plus_cash + margin_balance (None-safe).
    pos*: (account, security) -> (q, mv, p). Returns the six counts."""
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


def recount(root):
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    from lib import opal_naming
    s3 = boto3.client("s3")
    src = json.loads((Path(root) / "data/assets/scripts/gold/irpt_reporting/sources.json").read_bytes().decode("utf-8"))
    ent = next(v for k, v in src.items() if isinstance(v, dict) and "positions_prefix" in v)
    bucket, ppre, bpre = ent["bucket"], ent["positions_prefix"], ent["balance_prefix"]

    def part(prefix, day, cols):
        body = s3.get_object(Bucket=bucket, Key="%sdate=%s/data.parquet" % (prefix, day))["Body"].read()
        return pq.read_table(io.BytesIO(body), columns=cols).to_pydict()
    addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=2026-04-21")
    gb, gk = addr[len("s3://"):].split("/", 1)
    g = pq.read_table(io.BytesIO(s3.get_object(Bucket=gb, Key=gk.rstrip("/") + "/data.parquet")["Body"].read()), columns=["account_id", "guard_state"]).to_pydict()
    dis = {a for a, s in zip(g["account_id"], g["guard_state"]) if s == "GRADED_DISAGREED"}
    tau = float(json.loads(s3.get_object(Bucket=gb, Key=gk.rstrip("/") + "/manifest.json")["Body"].read().decode("utf-8"))["thresholds"]["tolerance"])
    bal, pos = {}, {}
    for d in DAYS:
        t = part(bpre, d, ["account_id", "net_mv_positions", "net_mv_plus_cash", "margin_balance"])
        bal[d] = {a: (fl(t["net_mv_positions"][i]), (fl(t["net_mv_plus_cash"][i]) or 0.0) + (fl(t["margin_balance"][i]) or 0.0))
                  for i, a in enumerate(t["account_id"]) if a in dis}
        t = part(ppre, d, ["account_id", "cusip", "ticker_symbol", "quantity_settled_unsettled", "market_value_settled_unsettled", "closing_price"])
        P = {}
        for i, a in enumerate(t["account_id"]):
            sec = t["cusip"][i] or t["ticker_symbol"][i]
            if a in dis and sec:
                P[(a, sec)] = (fl(t["quantity_settled_unsettled"][i]), fl(t["market_value_settled_unsettled"][i]), fl(t["closing_price"][i]))
        pos[d] = P
    res = {"tolerance": tau, "flagged": len(dis), "intervals": {}}
    for d0, d1 in INTERVALS:
        res["intervals"]["%s>%s" % (d0, d1)] = interval_counts(dis, bal[d0], bal[d1], pos[d0], pos[d1], tau)
    return res


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, truth, fg, analysis_text, tracked, analysis_sha):
    exp = {"date", "accounts_flagged", "tolerance", "intervals", "other_dates", "source", "words", "analysis", "reads", "claim",
           "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["date"] == "2026-04-21" and nes(rec["words"]) and rec["claim"] in CLAIMS, "date, words or claim")
    d0 = fg["dates"][0]
    need(rec["accounts_flagged"] == d0["rows_graded_disagreed"] == truth["flagged"], "accounts_flagged: record %s, flow-guard record %s, recount %s" %
         (rec["accounts_flagged"], d0["rows_graded_disagreed"], truth["flagged"]))
    need(isinstance(rec["tolerance"], float) and abs(rec["tolerance"] - truth["tolerance"]) < 1e-12, "tolerance differs from the manifest")
    iv = rec["intervals"]
    need(isinstance(iv, list) and [(x.get("from"), x.get("to")) for x in iv] == list(INTERVALS), "intervals must be the three, in order")
    for x in iv:
        need(set(x) == {"from", "to"} | set(COUNT_KEYS) | {"claim"} and x["claim"] in CLAIMS and all(is_int(x[k]) and x[k] >= 0 for k in COUNT_KEYS), "an interval entry")
        t = truth["intervals"]["%s>%s" % (x["from"], x["to"])]
        for k in COUNT_KEYS:
            need(x[k] == t[k], "interval %s to %s, %s: record %s, recount %s" % (x["from"], x["to"], k, x[k], t[k]))
        need(all(x[k] <= x["accounts"] for k in COUNT_KEYS), "a count exceeds the accounts")
    od = rec["other_dates"]
    need(isinstance(od, list) and [x.get("date") for x in od] == list(OTHERS), "other_dates must be the five, in order")
    for x in od:
        need(set(x) == {"date", "prior_date", "accounts_flagged", "accounts", "balance_positions_agrees_position_mv", "position_mv_agrees_price_return", "claim"}
             and ISO.match(str(x["prior_date"])) and x["prior_date"] < x["date"] and x["claim"] in CLAIMS and all(is_int(x[k]) and x[k] >= 0 for k in
             ("accounts_flagged", "accounts", "balance_positions_agrees_position_mv", "position_mv_agrees_price_return")), "an other_dates entry")
        need(x["accounts"] <= x["accounts_flagged"] and x["balance_positions_agrees_position_mv"] <= x["accounts"] and x["position_mv_agrees_price_return"] <= x["accounts"],
             "other date %s: counts exceed their bounds" % x["date"])
    need(isinstance(rec["source"], dict) and set(rec["source"]) == {"file", "words"} and all(nes(rec["source"][k]) for k in rec["source"]), "source form")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == ANALYSIS_REL and an.get("tracked") is True and an.get("sha256") == analysis_sha and tracked, "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    low = analysis_text.lower()
    need(not [t for t in FOREIGN if t in low], "the analysis script names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the analysis script holds a write call")
    return True


def run(root, cid):
    need(cid == "DB120-2-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    fg = load(root, FG_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root)
    check_record(rec, truth, fg, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), hashlib.sha256(ap.read_bytes()).hexdigest())
    first = truth["intervals"]["2026-04-20>2026-04-21"]
    print("OK: balance-lag read: %d flagged accounts; 04-20 to 04-21 recounted: %s; all three intervals equal the recount to the unit" % (truth["flagged"], first))
    return True


def selftest(root):
    pos0 = {("a", "S1"): (10.0, 1000.0, 100.0), ("a", "S2"): (10.0, 1000.0, 100.0), ("b", "S1"): (10.0, 1000.0, 100.0), ("x", "S1"): (5.0, 5.0, 1.0)}
    pos1 = {("a", "S1"): (10.0, 980.0, 98.0), ("a", "S2"): (10.0, 980.0, 98.0), ("b", "S1"): (11.0, 1078.0, 98.0), ("x", "S1"): (5.0, 5.0, 1.0)}
    bal0 = {"a": (2000.0, 2100.0), "b": (1000.0, 1100.0)}
    bal1 = {"a": (1960.0, 2060.0), "b": (1078.0, 1178.0)}
    c = interval_counts({"a", "b"}, bal0, bal1, pos0, pos1, 0.001)
    need(c["accounts"] == 2 and c["balance_positions_agrees_position_mv"] == 2 and c["position_mv_agrees_price_return"] == 1
         and c["balance_positions_agrees_price_return"] == 1 and c["accounts_with_quantity_change"] == 1, "interval_counts: %s" % c)
    need(interval_counts({"a"}, bal0, {}, pos0, pos1, 0.001)["accounts"] == 0, "a missing balance leaves the account uncounted")
    truth = {"flagged": 5, "tolerance": 0.001244, "intervals": {"%s>%s" % i: dict(c) for i in INTERVALS}}
    fg = {"dates": [{"rows_graded_disagreed": 5}]}

    def good():
        return {"date": "2026-04-21", "accounts_flagged": 5, "tolerance": 0.001244,
                "intervals": [dict(c, **{"from": a, "to": b, "claim": "measured"}) for a, b in INTERVALS],
                "other_dates": [{"date": d, "prior_date": "2026-01-01", "accounts_flagged": 9, "accounts": 8, "balance_positions_agrees_position_mv": 7,
                                 "position_mv_agrees_price_return": 1, "claim": "measured"} for d in OTHERS],
                "source": {"file": "f", "words": "w"}, "words": "w", "analysis": {"file": ANALYSIS_REL, "sha256": "ab" * 32, "tracked": True},
                "reads": {"s3_reads": 9, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured",
                "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(rec, text="x = 1", tracked=True, h="ab" * 32):
        try:
            return check_record(rec, truth, fg, text, tracked, h)
        except Fail:
            return False
    need(grade(good()) is True, "GREEN arm failed")
    r = good()
    r["intervals"][0]["accounts"] = 1
    need(grade(r) is False, "RED: a count that differs from the recount must fail")
    r = good()
    r["accounts_flagged"] = 6
    need(grade(r) is False, "RED: accounts_flagged that differs must fail")
    r = good()
    r["intervals"] = r["intervals"][::-1]
    need(grade(r) is False, "RED: intervals out of order must fail")
    r = good()
    r["other_dates"][0]["accounts"] = 99
    need(grade(r) is False, "RED: other-date counts above their bound must fail")
    r = good()
    r["tolerance"] = 0.002
    need(grade(r) is False, "RED: a tolerance that differs from the manifest must fail")
    r = good()
    r["words"] = "ids 1234567890"
    need(grade(r) is False, "RED: a long digit run must fail")
    need(grade(good(), tracked=False) is False, "RED: an untracked script must fail")
    need(grade(good(), text="s3.put_object(Bucket=b)") is False, "RED: a write call must fail")
    need(grade(good(), text="b = 'opal-data-cottonwood'") is False, "RED: another firm's place must fail")
    need(grade(good(), h="cd" * 32) is False, "RED: a hash mismatch must fail")
    r = good()
    r["pushed"] = True
    need(grade(r) is False, "RED: a push flag must fail")
    print("selftest OK: interval arms, 1 green and 11 red record arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p120_balance.py <repo_root> <criterion_id>")
            sys.exit(2)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
    except Exception as e:
        print("FAIL: %s: %s" % (type(e).__name__, str(e)[:200]))
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
