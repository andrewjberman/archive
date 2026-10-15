"""IRPT_DASHBD round 121, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-244, the 2026-04-21 QUANTITY READ (CTO analysis @9d4bd6adf3 ruling 3): what moved the quantities of the
accounts the flow guard disagreed on, by event word, by security, and by the presence of a same-day transaction row; before any guard change.

  DB-b-244 (~198) over the 943 GRADED_DISAGREED accounts of the 49 Financial account_return_daily partition of 2026-04-21: the (account, security) pairs whose quantity differs
                  between the custodian position partitions of 2026-04-20 and 2026-04-21; the custodian transaction rows (fact_trn) of 2026-04-21 for the same accounts, by
                  (tr_cd, sb_cd) and the rules the CRO classification table gives those codes; the securities that account for the change; whether a corporate-action or
                  share-class-conversion source exists.  A READ: counts by security and by event word; nothing written.      DB121-3-AC1

Definitions (the checker recounts every number to the unit):
  security of a position or transaction row = cusip, else ticker_symbol (a row with neither is not counted).
  A pair (account, security) is CHANGED when its quantity_settled_unsettled differs between the two days (a pair held on one day only is changed; a null equals a null).
  accounts_with_change / securities_changed = distinct accounts / securities among the changed pairs.
  top_securities = the five securities with the most distinct changed accounts (ties: security ascending): {security, accounts_changed, pairs_changed}; top1_share = the first's
  accounts_changed / accounts_with_change, rounded to 4 places.
  trn_rows / trn_accounts = the fact_trn rows of 2026-04-21 for the flagged accounts / their distinct accounts; by_code = counts keyed "tr_cd|sb_cd".
  same_day_row_pairs = changed pairs with at least one such trn row on the same (account, security); changed_pairs_without_row = pairs_changed - same_day_row_pairs.
  ic_by_security = the five securities with the most tr_cd == "IC" rows: {security, rows, accounts} (rows descending, ties security ascending).
  code_rules[key] = the sorted distinct `rule` values of the CRO classification table rows with that (tr_cd, sb_cd) (any tran_srcde).

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
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~198/RD_QTY_CHANGE_0421_R121.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~198/qty_change_read_r121.py"
FG_REL = D + "0.9.0_WK_IRPT_DASHBD~186/RD_FLOW_GUARD_READ_R118.json"
CLASS_REL = "org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
DAY0, DAY1 = "2026-04-20", "2026-04-21"
FIRM = "49financial"
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item",
                "update_item", "write_table", "write_to_dataset", ".to_parquet(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "security", "by_code", "code_rules")


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


# ------------------------------------------------------------------------------------------------ the counts (pure)
def counts(p0, p1, trn_rows):
    """p0, p1: {(account, security): quantity}; trn_rows: [(account, security_or_None, tr_cd, sb_cd)]."""
    changed = {k for k in set(p0) | set(p1) if p0.get(k) != p1.get(k)}
    acc_by_sec, pairs_by_sec = defaultdict(set), Counter()
    for a, s in changed:
        acc_by_sec[s].add(a)
        pairs_by_sec[s] += 1
    ranked = sorted(acc_by_sec, key=lambda s: (-len(acc_by_sec[s]), s))[:5]
    accounts_with_change = {a for a, _s in changed}
    top = [{"security": s, "accounts_changed": len(acc_by_sec[s]), "pairs_changed": pairs_by_sec[s]} for s in ranked]
    trn_pairs = {(a, s) for a, s, _t, _b in trn_rows if s}
    by_code = Counter("%s|%s" % (t, b) for _a, _s, t, b in trn_rows)
    ic_rows, ic_acc = Counter(), defaultdict(set)
    for a, s, t, _b in trn_rows:
        if t == "IC" and s:
            ic_rows[s] += 1
            ic_acc[s].add(a)
    ic_top = [{"security": s, "rows": ic_rows[s], "accounts": len(ic_acc[s])} for s in sorted(ic_rows, key=lambda s: (-ic_rows[s], s))[:5]]
    same = len(changed & trn_pairs)
    return {"pairs_changed": len(changed), "securities_changed": len(acc_by_sec), "accounts_with_change": len(accounts_with_change),
            "top_securities": top, "top1_share": round(top[0]["accounts_changed"] / len(accounts_with_change), 4) if top and accounts_with_change else 0.0,
            "trn_rows": len(trn_rows), "trn_accounts": len({a for a, _s, _t, _b in trn_rows}), "by_code": dict(sorted(by_code.items())),
            "same_day_row_pairs": same, "changed_pairs_without_row": len(changed) - same, "ic_by_security": ic_top}


def code_rules(table, keys):
    out = {}
    for k in keys:
        t, b = k.split("|")
        out[k] = sorted({str(r.get("rule")) for r in table if r.get("tr_cd") == t and r.get("sb_cd") == b})
    return out


def recount(root):
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
        t = part(ent["positions_prefix"], d, ["account_id", "cusip", "ticker_symbol", "quantity_settled_unsettled"])
        P = {}
        for i, a in enumerate(t["account_id"]):
            sec = t["cusip"][i] or t["ticker_symbol"][i]
            if a in dis and sec:
                P[(a, sec)] = t["quantity_settled_unsettled"][i]
        pos[d] = P
    t = part(ent["transactions_prefix"], DAY1, ["account_id", "cusip", "ticker_symbol", "tr_cd", "sb_cd"])
    rows = [(a, (t["cusip"][i] or t["ticker_symbol"][i]) or None, t["tr_cd"][i], t["sb_cd"][i]) for i, a in enumerate(t["account_id"]) if a in dis]
    res = counts(pos[DAY0], pos[DAY1], rows)
    res["flagged"] = len(dis)
    res["code_rules"] = code_rules(json.loads((Path(root) / CLASS_REL).read_bytes().decode("utf-8")), list(res["by_code"]))
    return res


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, truth, fg, analysis_text, tracked, analysis_sha):
    exp = {"date", "prior_date", "accounts_flagged", "pairs_changed", "securities_changed", "accounts_with_change", "top_securities", "top1_share", "trn_rows", "trn_accounts",
           "by_code", "code_rules", "same_day_row_pairs", "changed_pairs_without_row", "ic_by_security", "corporate_action_source", "words", "analysis", "reads", "claim",
           "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["date"] == DAY1 and rec["prior_date"] == DAY0 and nes(rec["words"]) and rec["claim"] in CLAIMS, "dates, words or claim")
    need(rec["accounts_flagged"] == fg["dates"][0]["rows_graded_disagreed"] == truth["flagged"], "accounts_flagged: record %s, flow-guard record %s, recount %s" %
         (rec["accounts_flagged"], fg["dates"][0]["rows_graded_disagreed"], truth["flagged"]))
    for k in ("pairs_changed", "securities_changed", "accounts_with_change", "top_securities", "top1_share", "trn_rows", "trn_accounts", "by_code", "code_rules",
              "same_day_row_pairs", "changed_pairs_without_row", "ic_by_security"):
        need(rec[k] == truth[k], "%s: record %s, recount %s" % (k, json.dumps(rec[k])[:200], json.dumps(truth[k])[:200]))
    cs = rec["corporate_action_source"]
    need(isinstance(cs, dict) and set(cs) == {"found", "where", "words"} and isinstance(cs["found"], bool) and nes(cs["words"]) and
         (not cs["found"] or nes(cs["where"])), "corporate_action_source form (found, where when found, words)")
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
    need(cid == "DB121-3-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    fg = load(root, FG_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root)
    check_record(rec, truth, fg, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), hashlib.sha256(ap.read_bytes()).hexdigest())
    print("OK: quantity read: %d flagged, %d pairs changed over %d securities and %d accounts; top security share %.4f; %d trn rows, %d changed pairs with a same-day row; "
          "every number equals the recount" % (truth["flagged"], truth["pairs_changed"], truth["securities_changed"], truth["accounts_with_change"], truth["top1_share"],
                                               truth["trn_rows"], truth["same_day_row_pairs"]))
    return True


def selftest():
    p0 = {("a1", "S1"): 10.0, ("a2", "S1"): 5.0, ("a2", "S2"): 1.0, ("a3", "S3"): None}
    p1 = {("a1", "S1"): 12.0, ("a2", "S1"): 0.0, ("a2", "S2"): 1.0, ("a3", "S3"): None, ("a3", "S4"): 3.0}
    rows = [("a1", "S1", "IC", "RO"), ("a2", "S1", "IC", "RO"), ("a2", None, "FC", "FC"), ("a9", "S9", "TR", "TR")]
    c = counts(p0, p1, rows)
    assert c["pairs_changed"] == 3 and c["securities_changed"] == 2 and c["accounts_with_change"] == 3, c
    assert c["top_securities"][0] == {"security": "S1", "accounts_changed": 2, "pairs_changed": 2} and c["top1_share"] == round(2 / 3, 4)
    assert c["trn_rows"] == 4 and c["trn_accounts"] == 3 and c["by_code"] == {"FC|FC": 1, "IC|RO": 2, "TR|TR": 1}
    assert c["same_day_row_pairs"] == 2 and c["changed_pairs_without_row"] == 1 and c["ic_by_security"] == [{"security": "S1", "rows": 2, "accounts": 2}]
    assert code_rules([{"tr_cd": "IC", "sb_cd": "RO", "rule": "corp-actions"}, {"tr_cd": "IC", "sb_cd": "RO", "rule": "x"}], ["IC|RO", "ZZ|ZZ"]) == {"IC|RO": ["corp-actions", "x"], "ZZ|ZZ": []}
    truth = dict(c, flagged=4, code_rules={"IC|RO": ["corp-actions"]})
    rec = {"date": DAY1, "prior_date": DAY0, "accounts_flagged": 4, "pairs_changed": c["pairs_changed"], "securities_changed": c["securities_changed"], "accounts_with_change": c["accounts_with_change"],
           "top_securities": c["top_securities"], "top1_share": c["top1_share"], "trn_rows": c["trn_rows"], "trn_accounts": c["trn_accounts"], "by_code": c["by_code"],
           "code_rules": truth["code_rules"], "same_day_row_pairs": c["same_day_row_pairs"], "changed_pairs_without_row": c["changed_pairs_without_row"],
           "ic_by_security": c["ic_by_security"], "corporate_action_source": {"found": False, "where": "", "words": "none found"}, "words": "w",
           "analysis": {"file": ANALYSIS_REL, "tracked": True, "sha256": "a" * 64}, "reads": {"s3_reads": 3, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
           "claim": "measured", "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}
    fg = {"dates": [{"rows_graded_disagreed": 4}]}
    import copy
    assert check_record(rec, truth, fg, "x = 1", True, "a" * 64)
    for name, mut in (("pairs", lambda r: r.update(pairs_changed=99)), ("top", lambda r: r["top_securities"][0].update(accounts_changed=9)), ("flagged", lambda r: r.update(accounts_flagged=5)),
                      ("found without where", lambda r: r["corporate_action_source"].update(found=True)), ("flag", lambda r: r.update(pushed=True)),
                      ("digit run", lambda r: r.update(words="id 123456789012")), ("extra key", lambda r: r.update(z=1)), ("write count", lambda r: r["reads"].update(s3_writes=2))):
        r = copy.deepcopy(rec)
        mut(r)
        try:
            check_record(r, truth, fg, "x = 1", True, "a" * 64)
            raise AssertionError("red arm %s passed" % name)
        except Fail:
            pass
    for name, text in (("write call", "s3.put_object()"), ("foreign place", "opal-data-inflection")):
        try:
            check_record(rec, truth, fg, text, True, "a" * 64)
            raise AssertionError("red arm %s passed" % name)
        except Fail:
            pass
    print("selftest: the counts, the rule lookup, one green and ten red record arms behave")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest()
            print("selftest PASS")
            sys.exit(0)
        root, cid = sys.argv[1], sys.argv[2]
        run(root, cid)
        print("%s PASS" % cid)
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % (sys.argv[2] if len(sys.argv) > 2 else "?"))
        sys.exit(1)
