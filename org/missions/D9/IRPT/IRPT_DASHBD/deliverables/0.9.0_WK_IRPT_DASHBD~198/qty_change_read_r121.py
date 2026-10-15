"""IRPT_DASHBD round 121, workstream B-49F (worker 0.9.0_WK_IRPT_DASHBD~198) -- DB-b-244, the 2026-04-21 quantity read.

What moved the quantities of the GRADED_DISAGREED accounts of the 49 Financial account_return_daily partition of
2026-04-21 (CTO analysis @9d4bd6adf3, ruling 3): the (account, security) pairs whose quantity changed between the
custodian dim_position partitions of 2026-04-20 and 2026-04-21, the custodian fact_trn rows of 2026-04-21 for the same
accounts (by tr_cd|sb_cd, with the CRO classification rules of those codes), the securities that carry the change, the
event words of the leading security, and whether a corporate-action or share-class-conversion source is readable.

READ-ONLY. GET only, three kinds of object: the account_return_daily data.parquet of 2026-04-21 (for the flagged
accounts), the custodian dim_position data.parquet of 2026-04-20 and 2026-04-21, and the custodian fact_trn
data.parquet of 2026-04-21. The bucket and the prefixes are read FROM data/assets/scripts/gold/irpt_reporting/sources.json
(the one entry that carries positions_prefix); the gold address comes from lib/opal_naming.py address().
Writes: one counts-only private file under the worker's private evidence folder. Nothing else.

Definitions (the round-121 checker recounts every number from the same sources):
  security of a position or transaction row = cusip, else ticker_symbol (a row with neither is not counted).
  A pair (account, security) is CHANGED when its quantity differs between the two days; a pair held on one day only
  is changed; a null equals a null.
  top_securities = the five securities with the most distinct changed accounts (ties: security ascending).
  by_code = fact_trn rows of the flagged accounts keyed "tr_cd|sb_cd"; code_rules = the distinct CRO rule words of those codes.

Usage: python -I <this file> <repo_root>
"""
import hashlib
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

FIRM_KEY = "49financial"
DAY0 = "2026-04-20"
DAY1 = "2026-04-21"
GUARD_GD = "GRADED_DISAGREED"
SOURCES_REL = "data/assets/scripts/gold/irpt_reporting/sources.json"
FG_REL = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~186/RD_FLOW_GUARD_READ_R118.json"
CLASS_REL = "org/tier1_exec/4.0.0_SA_CRO/deliverables/SCHWAB_TRANSACTION_CODE_CLASSIFICATION_20260811.json"
PRIVATE_DIR = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~198"
PRIVATE_NAME = "qty_change_read_r121_counts.json"
POS_COLS = ["account_id", "cusip", "ticker_symbol", "quantity_settled_unsettled"]
TRN_COLS = ["account_id", "cusip", "ticker_symbol", "tr_cd", "sb_cd", "transaction_detail_description"]
TOP_N = 5
MISSING = object()
DIGIT = re.compile(r"[0-9]")


class Stop(Exception):
    pass


class Reader(object):
    """GET only. There is deliberately no method that changes a remote object."""

    def __init__(self):
        import boto3
        self._s3 = boto3.client("s3")
        self.gets = 0

    def table(self, bucket, key, cols):
        import pyarrow.parquet as pq
        self.gets += 1
        body = self._s3.get_object(Bucket=bucket, Key=key)["Body"].read()
        return pq.read_table(io.BytesIO(body), columns=cols).to_pydict()


def security(cusip, ticker):
    return cusip or ticker or None


def masked(text):
    """A description with every digit replaced by a hash mark: words kept, any identifier run removed."""
    return DIGIT.sub("#", text or "")


def positions(t, dis):
    """(account, security) -> quantity for the flagged accounts; a later row for the same pair replaces an earlier one."""
    out = {}
    for i, a in enumerate(t["account_id"]):
        sec = security(t["cusip"][i], t["ticker_symbol"][i])
        if a in dis and sec:
            out[(a, sec)] = t["quantity_settled_unsettled"][i]
    return out


def transactions(t, dis):
    rows = []
    for i, a in enumerate(t["account_id"]):
        if a in dis:
            rows.append((a, security(t["cusip"][i], t["ticker_symbol"][i]), t["tr_cd"][i], t["sb_cd"][i], t["transaction_detail_description"][i]))
    return rows


def changed_pairs(p0, p1):
    out = set()
    for k in set(p0) | set(p1):
        if p0.get(k, MISSING) != p1.get(k, MISSING):
            out.add(k)
    return out


def counts(changed, rows):
    acc_by_sec = defaultdict(set)
    pairs_by_sec = Counter()
    for a, s in changed:
        acc_by_sec[s].add(a)
        pairs_by_sec[s] += 1
    ranked = sorted(acc_by_sec, key=lambda s: (-len(acc_by_sec[s]), s))[:TOP_N]
    accounts = set(a for a, _s in changed)
    top = [{"security": s, "accounts_changed": len(acc_by_sec[s]), "pairs_changed": pairs_by_sec[s]} for s in ranked]
    trn_pairs = set((a, s) for a, s, _t, _b, _d in rows if s)
    by_code = Counter("%s|%s" % (t, b) for _a, _s, t, b, _d in rows)
    ic_rows = Counter()
    ic_acc = defaultdict(set)
    for a, s, t, _b, _d in rows:
        if t == "IC" and s:
            ic_rows[s] += 1
            ic_acc[s].add(a)
    ic_top = [{"security": s, "rows": ic_rows[s], "accounts": len(ic_acc[s])}
              for s in sorted(ic_rows, key=lambda s: (-ic_rows[s], s))[:TOP_N]]
    same = len(changed & trn_pairs)
    share = round(top[0]["accounts_changed"] / float(len(accounts)), 4) if top and accounts else 0.0
    return {"pairs_changed": len(changed), "securities_changed": len(acc_by_sec), "accounts_with_change": len(accounts),
            "top_securities": top, "top1_share": share, "trn_rows": len(rows), "trn_accounts": len(set(a for a, _s, _t, _b, _d in rows)),
            "by_code": dict(sorted(by_code.items())), "same_day_row_pairs": same, "changed_pairs_without_row": len(changed) - same,
            "ic_by_security": ic_top}


def code_rules(table, keys):
    out = {}
    for k in keys:
        t, b = k.split("|")
        out[k] = sorted(set(str(r.get("rule")) for r in table if r.get("tr_cd") == t and r.get("sb_cd") == b))
    return out


def leading_security_words(top_sec, changed, p0, p1, rows):
    """The event words of the leading security: its fact_trn rows, its codes, its description texts (masked), and the direction of its changes."""
    srows = [r for r in rows if r[1] == top_sec]
    codes = Counter("%s|%s" % (r[2], r[3]) for r in srows)
    texts = Counter(masked(r[4]) for r in srows)
    same_accts = set(r[0] for r in srows)
    mine = [k for k in changed if k[1] == top_sec]
    up = down = nulls = 0
    for k in mine:
        q0, q1 = p0.get(k), p1.get(k)
        if q0 is None or q1 is None:
            nulls += 1
        elif q1 > q0:
            up += 1
        elif q1 < q0:
            down += 1
    with_row = set((a, s) for a, s, _t, _b, _d in rows if s == top_sec)
    return {"security": top_sec, "rows": len(srows), "accounts_with_row": len(same_accts), "codes": dict(sorted(codes.items())),
            "distinct_texts": len(texts), "top_texts": [{"text": t, "rows": n} for t, n in texts.most_common(TOP_N)],
            "changed_pairs": len(mine), "changed_pairs_with_same_day_row": len([k for k in mine if k in with_row]),
            "direction": {"up": up, "down": down, "null_either_day": nulls}}


def unrowed_words(changed, rows):
    trn_pairs = set((a, s) for a, s, _t, _b, _d in rows if s)
    left = [k for k in changed if k not in trn_pairs]
    accts = set(a for a, _s in left)
    by_sec = Counter(s for _a, s in left)
    return {"pairs": len(left), "accounts": len(accts), "top_securities": [{"security": s, "pairs": n} for s, n in by_sec.most_common(TOP_N)]}


def corp_action_words(table, rows):
    rules = Counter(str(r.get("rule")) for r in table)
    ca = [r for r in table if "corp" in str(r.get("rule", "")).lower() or "corp" in str(r.get("category", "")).lower()
          or "share" in str(r.get("desc", "")).lower() or "convers" in str(r.get("desc", "")).lower()]
    keys = sorted(set("%s|%s" % (r.get("tr_cd"), r.get("sb_cd")) for r in ca))
    kset = set(keys)
    hits = [r for r in rows if "%s|%s" % (r[2], r[3]) in kset]
    return {"table_rules": dict(sorted(rules.items())), "candidate_rows_in_table": len(ca), "candidate_keys": keys,
            "candidate_descs": sorted(set(str(r.get("desc")) for r in ca))[:TOP_N * 4],
            "flagged_rows_with_candidate_key": len(hits), "flagged_accounts_with_candidate_key": len(set(r[0] for r in hits))}


def main(argv):
    repo = os.path.abspath(argv[1] if len(argv) > 1 else ".")
    fg = json.loads(Path(repo, FG_REL).read_bytes().decode("utf-8"))
    d0 = fg["dates"][0]
    if d0["date"] != DAY1:
        raise Stop("the flow-guard record's first date is not %s" % DAY1)
    sys.path.insert(0, repo)
    from lib import opal_naming as naming
    src = json.loads(Path(repo, SOURCES_REL).read_bytes().decode("utf-8"))
    hits = [v for v in src.values() if isinstance(v, dict) and "positions_prefix" in v]
    if len(hits) != 1:
        raise Stop("sources.json carries %d entries with positions_prefix; exactly one is required" % len(hits))
    ent = hits[0]
    if not (ent.get("bucket") and ent.get("positions_prefix") and ent.get("transactions_prefix")):
        raise Stop("the positions entry lacks bucket, positions_prefix or transactions_prefix")
    bucket = ent["bucket"]
    rest = naming.address("irpt", FIRM_KEY, "gold", "account_return_daily", "date=%s" % DAY1)[len("s3://"):]
    gbucket, _sep, gkey = rest.partition("/")

    reader = Reader()
    g = reader.table(gbucket, gkey.rstrip("/") + "/data.parquet", ["account_id", "guard_state"])
    gold_rows = len(g["account_id"])
    dis = set(a for a, s in zip(g["account_id"], g["guard_state"]) if s == GUARD_GD)
    pos = {}
    for d in (DAY0, DAY1):
        t = reader.table(bucket, ent["positions_prefix"] + "date=%s/data.parquet" % d, POS_COLS)
        pos[d] = positions(t, dis)
    t = reader.table(bucket, ent["transactions_prefix"] + "date=%s/data.parquet" % DAY1, TRN_COLS)
    rows = transactions(t, dis)

    changed = changed_pairs(pos[DAY0], pos[DAY1])
    held_one_day_null = len([k for k in set(pos[DAY0]) ^ set(pos[DAY1]) if (pos[DAY0][k] if k in pos[DAY0] else pos[DAY1][k]) is None])
    res = counts(changed, rows)
    res["flagged"] = len(dis)
    res["code_rules"] = code_rules(json.loads(Path(repo, CLASS_REL).read_bytes().decode("utf-8")), list(res["by_code"]))

    table = json.loads(Path(repo, CLASS_REL).read_bytes().decode("utf-8"))
    lead = leading_security_words(res["top_securities"][0]["security"], changed, pos[DAY0], pos[DAY1], rows) if res["top_securities"] else {}
    desc_by_code = defaultdict(Counter)
    for _a, _s, tc, bc, dsc in rows:
        desc_by_code["%s|%s" % (tc, bc)][masked(dsc)] += 1
    out = {"date": DAY1, "prior_date": DAY0, "gold_rows": gold_rows, "guard_rows_graded_disagreed_record": d0["rows_graded_disagreed"],
           "numbers": res, "leading_security": lead, "unrowed": unrowed_words(changed, rows),
           "desc_by_code": {k: {"distinct_texts": len(v), "top": v.most_common(3)} for k, v in sorted(desc_by_code.items())},
           "corp_action": corp_action_words(table, rows), "held_one_day_null_pairs": held_one_day_null,
           "s3_gets": reader.gets, "analysis_sha256": None}
    out["analysis_sha256"] = hashlib.sha256(Path(os.path.abspath(__file__)).read_bytes()).hexdigest()
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    with open(os.path.join(PRIVATE_DIR, PRIVATE_NAME), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("gold_rows=%d flagged=%d guard_record=%s" % (gold_rows, len(dis), d0["rows_graded_disagreed"]))
    print("NUMBERS: " + json.dumps(res, sort_keys=True))
    print("LEADING: " + json.dumps(lead, sort_keys=True))
    print("UNROWED: " + json.dumps(out["unrowed"], sort_keys=True))
    print("CORP: " + json.dumps(out["corp_action"], sort_keys=True))
    print("DESC_BY_CODE: " + json.dumps(out["desc_by_code"], sort_keys=True))
    print("held_one_day_null_pairs=%d s3_gets=%d" % (held_one_day_null, reader.gets))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except Stop as e:
        print("STOP: %s" % e)
        sys.exit(3)
