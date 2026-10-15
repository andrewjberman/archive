"""IRPT_DASHBD round 122, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-248, the 2026-04-21 CONVERSION READ (CTO analysis @e690365741 ruling 2): for each in-kind receipt of the leading
security of 2026-04-21 (the `IC|RO` rows on CUSIP 922908736 that round 121 counted), is there a same-day DELIVERY of another security in the same account, of matching value?
Yes means an internal EXCHANGE (no external flow, no return effect); no means the custodian feed lacks the delivery leg (CONVERSION_LEG_ABSENT). A READ: counts only; nothing written.

  DB-b-248 (~202) the receipts (value = quantity x price of the IC|RO rows), the position legs (quantity that FELL between 2026-04-20 and 04-21 in the same account, at the 04-20
                  closing price), their match to the receipt within 1 and 5 percent, the other in-kind rows, the legs by security, and the changed pairs with no same-day transaction row
                  by security.                                                                      DB122-3-AC1

Definitions (the checker recounts every number to the unit; money is float, no dollar figure is recorded, only counts):
  flagged = the GRADED_DISAGREED accounts of the 49 Financial account_return_daily partition of 2026-04-21;  S = the first security of RD_QTY_CHANGE_0421_R121.json top_securities.
  v_a = sum of quantity * price over the fact_trn rows of 2026-04-21 of account a with tr_cd IC, sb_cd RO and security S (security = cusip else ticker);  receipts = accounts with v_a > 0.
  L_a = sum over pairs (a, s), s != S, with q1 < q0 (quantity_settled_unsettled on 04-21 and 04-20; a pair absent on 04-21 has q1 = 0) of (q0 - q1) * closing_price(04-20).
  receipts_with_leg = receipts with L_a > 0;  matched_1pct / matched_5pct = receipts with |L_a - v_a| <= 0.01 / 0.05 * v_a;
  receipts_with_other_ic_row = receipts having an fact_trn row of 2026-04-21 with tr_cd IC on a security other than S.
  legs_by_security = the five securities with the most receipt accounts holding a leg of that security (L > 0), {security, accounts}, accounts descending, ties security ascending.
  unexplained_by_security = the changed pairs of the flagged accounts (round 121's definition, quantity differs 04-20 vs 04-21) with NO fact_trn row of 04-21 on the same (account,
  security), counted by security: {security, pairs}, pairs descending, ties security ascending (all of them, not five).
  verdict = EXCHANGE_LEGS_PRESENT when matched_1pct >= 0.95 * receipts;  CONVERSION_LEG_ABSENT when receipts_with_leg <= 0.05 * receipts;  otherwise MIXED.

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import io
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~202/RD_CONVERSION_READ_R122.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~202/conversion_read_r122.py"
QTY_REL = D + "0.9.0_WK_IRPT_DASHBD~198/RD_QTY_CHANGE_0421_R121.json"
DAY0, DAY1 = "2026-04-20", "2026-04-21"
FIRM = "49financial"
CLAIMS = ("measured", "inferred", "held", "absent")
VERDICTS = ("EXCHANGE_LEGS_PRESENT", "CONVERSION_LEG_ABSENT", "MIXED")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item",
                "update_item", "write_table", "write_to_dataset", ".to_parquet(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "security", "legs_by_security", "unexplained_by_security")


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
def counts(S, p0, p1, trn):
    """p0, p1: {(account, security): (quantity, closing_price)}; trn: [(account, security_or_None, tr_cd, sb_cd, quantity, price)]."""
    v = defaultdict(float)
    for a, s, t, b, q, p in trn:
        if t == "IC" and b == "RO" and s == S and q is not None and p is not None:
            v[a] += q * p
    receipts = {a: x for a, x in v.items() if x > 0}
    legs = defaultdict(float)
    leg_acc = defaultdict(set)
    for (a, s), (q0, px0) in p0.items():
        if a not in receipts or s == S or q0 is None or px0 is None:
            continue
        q1 = (p1.get((a, s)) or (0.0, None))[0] or 0.0
        if q1 < q0:
            legs[a] += (q0 - q1) * px0
            leg_acc[s].add(a)
    n = len(receipts)
    with_leg = sum(1 for a in receipts if legs.get(a, 0.0) > 0)
    m1 = sum(1 for a, x in receipts.items() if abs(legs.get(a, 0.0) - x) <= 0.01 * x)
    m5 = sum(1 for a, x in receipts.items() if abs(legs.get(a, 0.0) - x) <= 0.05 * x)
    other_ic = len({a for a, s, t, b, q, p in trn if t == "IC" and s and s != S and a in receipts})
    top = sorted(leg_acc, key=lambda s: (-len(leg_acc[s]), s))[:5]
    trn_pairs = {(a, s) for a, s, _t, _b, _q, _p in trn if s}
    changed = {k for k in set(p0) | set(p1) if (p0.get(k) or (None,))[0] != (p1.get(k) or (None,))[0]}
    unexpl = Counter(s for (a, s) in changed if (a, s) not in trn_pairs)
    verdict = "EXCHANGE_LEGS_PRESENT" if n and m1 >= 0.95 * n else ("CONVERSION_LEG_ABSENT" if n and with_leg <= 0.05 * n else "MIXED")
    return {"receipts": n, "receipts_with_leg": with_leg, "matched_1pct": m1, "matched_5pct": m5, "receipts_with_other_ic_row": other_ic,
            "legs_by_security": [{"security": s, "accounts": len(leg_acc[s])} for s in top],
            "unexplained_by_security": [{"security": s, "pairs": unexpl[s]} for s in sorted(unexpl, key=lambda s: (-unexpl[s], s))], "verdict": verdict}


def recount(root, security):
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    from lib import opal_naming
    s3 = boto3.client("s3")
    src = json.loads((Path(root) / "data/assets/scripts/gold/irpt_reporting/sources.json").read_bytes().decode("utf-8"))
    ent = next(v for k, v in src.items() if isinstance(v, dict) and "positions_prefix" in v)
    bucket = ent["bucket"]

    def part(prefix, day, cols):
        body = s3.get_object(Bucket=bucket, Key="%sdate=%s/data.parquet" % (prefix, day))["Body"].read()
        return pq.read_table(io.BytesIO(body), columns=cols).to_pydict()
    addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=%s" % DAY1)
    gb, gk = addr[len("s3://"):].split("/", 1)
    g = pq.read_table(io.BytesIO(s3.get_object(Bucket=gb, Key=gk.rstrip("/") + "/data.parquet")["Body"].read()), columns=["account_id", "guard_state"]).to_pydict()
    dis = {a for a, s in zip(g["account_id"], g["guard_state"]) if s == "GRADED_DISAGREED"}
    pos = {}
    for d in (DAY0, DAY1):
        t = part(ent["positions_prefix"], d, ["account_id", "cusip", "ticker_symbol", "quantity_settled_unsettled", "closing_price"])
        P = {}
        for i, a in enumerate(t["account_id"]):
            sec = t["cusip"][i] or t["ticker_symbol"][i]
            if a in dis and sec:
                P[(a, sec)] = (fl(t["quantity_settled_unsettled"][i]), fl(t["closing_price"][i]))
        pos[d] = P
    t = part(ent["transactions_prefix"], DAY1, ["account_id", "cusip", "ticker_symbol", "tr_cd", "sb_cd", "quantity", "price"])
    trn = [(a, (t["cusip"][i] or t["ticker_symbol"][i]) or None, t["tr_cd"][i], t["sb_cd"][i], fl(t["quantity"][i]), fl(t["price"][i]))
           for i, a in enumerate(t["account_id"]) if a in dis]
    res = counts(security, pos[DAY0], pos[DAY1], trn)
    res["flagged"] = len(dis)
    return res


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, truth, security, analysis_text, tracked, analysis_sha):
    exp = {"date", "prior_date", "security", "tolerance_primary", "tolerance_secondary", "receipts", "receipts_with_leg", "matched_1pct", "matched_5pct", "receipts_with_other_ic_row",
           "legs_by_security", "unexplained_by_security", "verdict", "words", "analysis", "reads", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["date"] == DAY1 and rec["prior_date"] == DAY0 and nes(rec["words"]) and rec["claim"] in CLAIMS, "dates, words or claim")
    need(rec["security"] == security, "security %s is not round 121's leading security %s" % (rec["security"], security))
    need(rec["tolerance_primary"] == 0.01 and rec["tolerance_secondary"] == 0.05, "the tolerances must be 0.01 and 0.05")
    for k in ("receipts", "receipts_with_leg", "matched_1pct", "matched_5pct", "receipts_with_other_ic_row", "legs_by_security", "unexplained_by_security", "verdict"):
        need(rec[k] == truth[k], "%s: record %s, recount %s" % (k, json.dumps(rec[k])[:200], json.dumps(truth[k])[:200]))
    need(rec["verdict"] in VERDICTS, "verdict outside the three")
    need(rec["matched_1pct"] <= rec["matched_5pct"] <= rec["receipts"] and rec["receipts_with_leg"] <= rec["receipts"], "counts out of bounds")
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
    need(cid == "DB122-3-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    security = load(root, QTY_REL)["top_securities"][0]["security"]
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root, security)
    check_record(rec, truth, security, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), hashlib.sha256(ap.read_bytes()).hexdigest())
    print("OK: conversion read: %d receipts of %s, %d with a position leg, %d matched within 1%% and %d within 5%%, verdict %s; every number equals the recount" %
          (truth["receipts"], security, truth["receipts_with_leg"], truth["matched_1pct"], truth["matched_5pct"], truth["verdict"]))
    return True


def selftest():
    import copy
    S = "SSS"
    p0 = {("a1", S): (0.0, 50.0), ("a1", "M1"): (10.0, 100.0), ("a2", "M1"): (10.0, 100.0), ("a3", "X"): (1.0, 10.0)}
    p1 = {("a1", S): (10.0, 100.0), ("a1", "M1"): (0.0, 100.0), ("a2", S): (5.0, 100.0), ("a2", "M1"): (10.0, 100.0), ("a3", "X"): (2.0, 10.0)}
    trn = [("a1", S, "IC", "RO", 10.0, 100.0), ("a2", S, "IC", "RO", 5.0, 100.0), ("a2", "Q", "IC", "IC", 1.0, 1.0), ("a1", "M1", "TR", "TR", 1.0, 1.0)]
    c = counts(S, p0, p1, trn)
    assert c["receipts"] == 2 and c["receipts_with_leg"] == 1 and c["matched_1pct"] == 1 and c["matched_5pct"] == 1 and c["receipts_with_other_ic_row"] == 1, c
    assert c["legs_by_security"] == [{"security": "M1", "accounts": 1}] and c["unexplained_by_security"] == [{"security": "X", "pairs": 1}] and c["verdict"] == "MIXED", c
    absent = counts(S, {("a1", "M1"): (10.0, 100.0)}, {("a1", S): (10.0, 100.0), ("a1", "M1"): (10.0, 100.0)}, [("a1", S, "IC", "RO", 10.0, 100.0)])
    assert absent["verdict"] == "CONVERSION_LEG_ABSENT" and absent["receipts_with_leg"] == 0
    both = counts(S, {("a1", "M1"): (10.0, 100.0)}, {("a1", S): (10.0, 100.0)}, [("a1", S, "IC", "RO", 10.0, 100.0)])
    assert both["verdict"] == "EXCHANGE_LEGS_PRESENT" and both["matched_1pct"] == 1
    rec = {"date": DAY1, "prior_date": DAY0, "security": S, "tolerance_primary": 0.01, "tolerance_secondary": 0.05, "receipts": c["receipts"], "receipts_with_leg": c["receipts_with_leg"],
           "matched_1pct": c["matched_1pct"], "matched_5pct": c["matched_5pct"], "receipts_with_other_ic_row": c["receipts_with_other_ic_row"], "legs_by_security": c["legs_by_security"],
           "unexplained_by_security": c["unexplained_by_security"], "verdict": c["verdict"], "words": "w", "analysis": {"file": ANALYSIS_REL, "tracked": True, "sha256": "a" * 64},
           "reads": {"s3_reads": 3, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured", "files_in_repo": False,
           "served_values_changed": False, "pushed": False, "deployed": False}
    assert check_record(rec, c, S, "x = 1", True, "a" * 64)
    for name, f in (("receipts", lambda r: r.update(receipts=9)), ("verdict", lambda r: r.update(verdict="EXCHANGE_LEGS_PRESENT")), ("security", lambda r: r.update(security="ZZZ")),
                    ("tolerance", lambda r: r.update(tolerance_primary=0.02)), ("flag", lambda r: r.update(pushed=True)), ("extra", lambda r: r.update(z=1)),
                    ("unexplained", lambda r: r["unexplained_by_security"].pop()), ("digits", lambda r: r.update(words="id 123456789012")), ("writes", lambda r: r["reads"].update(s3_writes=1))):
        r = copy.deepcopy(rec)
        f(r)
        try:
            check_record(r, c, S, "x = 1", True, "a" * 64)
            raise AssertionError("red arm %s passed" % name)
        except Fail:
            pass
    for t in ("s3.put_object()", "opal-data-cottonwood"):
        try:
            check_record(rec, c, S, t, True, "a" * 64)
            raise AssertionError("text arm passed")
        except Fail:
            pass
    print("selftest: the counts (mixed, absent, present), one green and eleven red record arms behave")


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
