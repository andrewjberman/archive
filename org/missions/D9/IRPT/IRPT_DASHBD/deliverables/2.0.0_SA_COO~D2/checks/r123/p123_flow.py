"""IRPT_DASHBD round 123, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-251, the IN-KIND-AS-FLOW READ (CTO analysis @1ffd4f5afb ruling 2): with no exchange leg in the feed
(round 122: CONVERSION_LEG_ABSENT), the 920 in-kind receipts of CUSIP 922908736 on 2026-04-21 may be EXTERNAL in-kind transfers into the accounts. Read: does adding each account's
`IC|RO` receipt value to its external flow on 2026-04-21 reconcile the holdings guard within its tolerance? Counts only; nothing written; no classification change is made or proposed.

  DB-b-251 (~205) for the flagged accounts that hold a receipt: the guard difference as the gold serves it (the receipt not a flow), with the receipt added as an INFLOW, and, as a
                  direction control, as an OUTFLOW; the counts that agree, the improvement, and where the rest fall.                  DB123-2-AC1

Definitions (the checker recounts every number to the unit; money is float, no dollar amount is recorded):
  cohort = the accounts of the 49 Financial account_return_daily partition of 2026-04-21 whose guard_state is GRADED_DISAGREED, that have a gold row on 2026-04-20 with
  market_value_eod > 0, a non-null holdings_price_return and carried_days == 1 on 2026-04-21, and a receipt;  receipt_accounts = the accounts (flagged or not) with a receipt.
  receipt value v = sum of quantity * price over the fact_trn rows of 2026-04-21 with tr_cd IC, sb_cd RO and security S (cusip else ticker; S = round 121's leading security).
  V1 = market_value_eod (04-21), V0 = market_value_eod (04-20), F = external_flow (04-21, null = 0), p = holdings_price_return + income_return (null income = 0), tol = the manifest tolerance.
  The producer's single-chain return:  r = (V1 - F') / V0 - 1,  diff = |r - p|,  F' = F (before), F + v (inflow), F - v (outflow).
  agree_before / agree_after_inflow / agree_after_outflow = cohort accounts with diff <= tol;  improved_after_inflow = diff(inflow) < diff(before);
  diff_buckets_after_inflow = counts of diff(inflow)/tol in (<=1, <=2, <=10, >10).
  verdict = IN_KIND_RECONCILES when agree_after_inflow >= 0.95 * cohort;  NOT_RECONCILED when agree_after_inflow <= 0.05 * cohort;  otherwise PARTIAL.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import io
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~205/RD_INKIND_FLOW_READ_R123.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~205/inkind_flow_read_r123.py"
QTY_REL = D + "0.9.0_WK_IRPT_DASHBD~198/RD_QTY_CHANGE_0421_R121.json"
DAY0, DAY1 = "2026-04-20", "2026-04-21"
FIRM = "49financial"
CLAIMS = ("measured", "inferred", "held", "absent")
VERDICTS = ("IN_KIND_RECONCILES", "NOT_RECONCILED", "PARTIAL")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item",
                "update_item", "write_table", "write_to_dataset", ".to_parquet(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "security")
KEYS = ("receipt_accounts", "cohort", "agree_before", "agree_after_inflow", "agree_after_outflow", "improved_after_inflow", "diff_buckets_after_inflow", "verdict")


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


# ------------------------------------------------------------------------------------------------ the counts (pure)
def counts(rows, receipts, tol):
    """rows: {account: dict(state, V1, V0, F, price_r, income_r, carried)}; receipts: {account: v}."""
    cohort = []
    for a, v in receipts.items():
        r = rows.get(a)
        if v <= 0 or r is None or r["state"] != "GRADED_DISAGREED" or r["V0"] is None or not r["V0"] > 0 or r["price_r"] is None or r["carried"] != 1 or r["V1"] is None:
            continue
        cohort.append((r, v))
    out = {"receipt_accounts": sum(1 for v in receipts.values() if v > 0), "cohort": len(cohort), "agree_before": 0, "agree_after_inflow": 0, "agree_after_outflow": 0,
           "improved_after_inflow": 0, "diff_buckets_after_inflow": {"le_1x": 0, "le_2x": 0, "le_10x": 0, "gt_10x": 0}}
    for r, v in cohort:
        p = r["price_r"] + (r["income_r"] or 0.0)
        F = r["F"] or 0.0

        def diff(flow):
            return abs((r["V1"] - flow) / r["V0"] - 1.0 - p)
        d0, d1, d2 = diff(F), diff(F + v), diff(F - v)
        out["agree_before"] += int(d0 <= tol)
        out["agree_after_inflow"] += int(d1 <= tol)
        out["agree_after_outflow"] += int(d2 <= tol)
        out["improved_after_inflow"] += int(d1 < d0)
        k = "le_1x" if d1 <= tol else ("le_2x" if d1 <= 2 * tol else ("le_10x" if d1 <= 10 * tol else "gt_10x"))
        out["diff_buckets_after_inflow"][k] += 1
    n = out["cohort"]
    a = out["agree_after_inflow"]
    out["verdict"] = "IN_KIND_RECONCILES" if n and a >= 0.95 * n else ("NOT_RECONCILED" if n and a <= 0.05 * n else "PARTIAL")
    return out


def recount(root, security):
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    from lib import opal_naming
    s3 = boto3.client("s3")
    src = json.loads((Path(root) / "data/assets/scripts/gold/irpt_reporting/sources.json").read_bytes().decode("utf-8"))
    ent = next(v for k, v in src.items() if isinstance(v, dict) and "positions_prefix" in v)

    def gold(day):
        addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=%s" % day)
        gb, gk = addr[len("s3://"):].split("/", 1)
        body = s3.get_object(Bucket=gb, Key=gk.rstrip("/") + "/data.parquet")["Body"].read()
        return pq.read_table(io.BytesIO(body)).to_pydict(), gb, gk
    g1, gb, gk = gold(DAY1)
    g0, _b, _k = gold(DAY0)
    tol = float(json.loads(s3.get_object(Bucket=gb, Key=gk.rstrip("/") + "/manifest.json")["Body"].read().decode("utf-8"))["thresholds"]["tolerance"])
    i0 = {a: i for i, a in enumerate(g0["account_id"])}
    rows = {}
    for i, a in enumerate(g1["account_id"]):
        j = i0.get(a)
        rows[a] = {"state": g1["guard_state"][i], "V1": fl(g1["market_value_eod"][i]), "V0": (fl(g0["market_value_eod"][j]) if j is not None else None),
                   "F": fl(g1["external_flow"][i]), "price_r": fl(g1["holdings_price_return"][i]), "income_r": fl(g1["income_return"][i]), "carried": g1["carried_days"][i]}
    body = s3.get_object(Bucket=ent["bucket"], Key="%sdate=%s/data.parquet" % (ent["transactions_prefix"], DAY1))["Body"].read()
    t = pq.read_table(io.BytesIO(body), columns=["account_id", "cusip", "ticker_symbol", "tr_cd", "sb_cd", "quantity", "price"]).to_pydict()
    v = defaultdict(float)
    for i, a in enumerate(t["account_id"]):
        if t["tr_cd"][i] == "IC" and t["sb_cd"][i] == "RO" and (t["cusip"][i] or t["ticker_symbol"][i]) == security and t["quantity"][i] is not None and t["price"][i] is not None:
            v[a] += float(t["quantity"][i]) * float(t["price"][i])
    res = counts(rows, dict(v), tol)
    res["tolerance"] = tol
    return res


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, truth, security, analysis_text, tracked, analysis_sha):
    exp = {"date", "prior_date", "security", "tolerance", "formula", *KEYS, "words", "analysis", "reads", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["date"] == DAY1 and rec["prior_date"] == DAY0 and nes(rec["words"]) and nes(rec["formula"]) and rec["claim"] in CLAIMS, "dates, formula, words or claim")
    need(rec["security"] == security, "security %s is not round 121's leading security %s" % (rec["security"], security))
    need(isinstance(rec["tolerance"], float) and abs(rec["tolerance"] - truth["tolerance"]) < 1e-12, "tolerance differs from the manifest's")
    for k in KEYS:
        need(rec[k] == truth[k], "%s: record %s, recount %s" % (k, json.dumps(rec[k])[:160], json.dumps(truth[k])[:160]))
    need(rec["verdict"] in VERDICTS, "verdict outside the three")
    need(rec["agree_after_inflow"] <= rec["cohort"] <= rec["receipt_accounts"] and rec["improved_after_inflow"] <= rec["cohort"], "counts out of bounds")
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
    need(cid == "DB123-2-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    security = load(root, QTY_REL)["top_securities"][0]["security"]
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root, security)
    check_record(rec, truth, security, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), hashlib.sha256(ap.read_bytes()).hexdigest())
    print("OK: in-kind-as-flow read: %d receipt accounts, cohort %d; guard agrees before %d, after the receipt as an inflow %d (as an outflow %d); verdict %s; every number equals the recount" %
          (truth["receipt_accounts"], truth["cohort"], truth["agree_before"], truth["agree_after_inflow"], truth["agree_after_outflow"], truth["verdict"]))
    return True


def selftest():
    import copy
    tol = 0.001
    base = {"state": "GRADED_DISAGREED", "V1": 1100.0, "V0": 1000.0, "F": 0.0, "price_r": 0.0, "income_r": 0.0, "carried": 1}
    rows = {"a1": dict(base), "a2": dict(base, V1=1000.0), "a3": dict(base, state="GRADED_AGREED"), "a4": dict(base, carried=2), "a5": dict(base, price_r=None), "a6": dict(base, V0=0.0)}
    receipts = {"a1": 100.0, "a2": 50.0, "a3": 10.0, "a4": 10.0, "a5": 10.0, "a6": 10.0, "a7": 5.0, "a8": 0.0}
    c = counts(rows, receipts, tol)
    # a1: r = (1100-0)/1000-1 = 0.1 (diff 0.1 before); inflow 100 -> r = 0 (agree); outflow -> 0.2.   a2: before r=0 (agree), inflow 50 -> -0.05 (disagree).
    assert c["receipt_accounts"] == 7 and c["cohort"] == 2 and c["agree_before"] == 1 and c["agree_after_inflow"] == 1 and c["agree_after_outflow"] == 0 and c["improved_after_inflow"] == 1, c
    assert c["diff_buckets_after_inflow"] == {"le_1x": 1, "le_2x": 0, "le_10x": 0, "gt_10x": 1} and c["verdict"] == "PARTIAL", c
    allok = counts({"a1": dict(base)}, {"a1": 100.0}, tol)
    assert allok["verdict"] == "IN_KIND_RECONCILES"
    none = counts({"a1": dict(base)}, {"a1": 1.0}, tol)
    assert none["verdict"] == "NOT_RECONCILED"
    rec = {"date": DAY1, "prior_date": DAY0, "security": "SSS", "tolerance": tol, "formula": "r = (V1 - F) / V0 - 1", **{k: c[k] for k in KEYS}, "words": "w",
           "analysis": {"file": ANALYSIS_REL, "tracked": True, "sha256": "a" * 64}, "reads": {"s3_reads": 3, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
           "claim": "measured", "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}
    truth = dict(c, tolerance=tol)
    assert check_record(rec, truth, "SSS", "x = 1", True, "a" * 64)
    for name, f in (("cohort", lambda r: r.update(cohort=9)), ("verdict", lambda r: r.update(verdict="IN_KIND_RECONCILES")), ("security", lambda r: r.update(security="ZZZ")),
                    ("tolerance", lambda r: r.update(tolerance=0.002)), ("flag", lambda r: r.update(deployed=True)), ("extra", lambda r: r.update(z=1)),
                    ("bucket", lambda r: r["diff_buckets_after_inflow"].update(le_1x=5)), ("digits", lambda r: r.update(words="id 123456789012")), ("writes", lambda r: r["reads"].update(s3_writes=1))):
        r = copy.deepcopy(rec)
        f(r)
        try:
            check_record(r, truth, "SSS", "x = 1", True, "a" * 64)
            raise AssertionError("red arm %s passed" % name)
        except Fail:
            pass
    for t in ("s3.put_object()", "opal-data-cottonwood"):
        try:
            check_record(rec, truth, "SSS", t, True, "a" * 64)
            raise AssertionError("text arm passed")
        except Fail:
            pass
    print("selftest: the counts (partial, reconciled, not), one green and eleven red record arms behave")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        run(sys.argv[1], sys.argv[2])
        print("%s PASS" % sys.argv[2])
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
