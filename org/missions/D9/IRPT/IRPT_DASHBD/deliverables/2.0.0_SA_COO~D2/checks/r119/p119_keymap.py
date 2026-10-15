"""IRPT_DASHBD round 119, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-235, the Commonwealth-to-Black-Diamond KEY-MAP READ
(CTO analysis @d856067e84 ruling 3).

  DB-b-235 (~189) does the Black Diamond silver of Cottonwood hold a map from the Commonwealth custodian number (the key of Cottonwood's
                  account_return_daily history to 2026-06-22) to the Black Diamond account key (the key of the household frame and of the
                  Black Diamond silver)? A READ: counts, names and words only; nothing written.                    DB119-3-AC1

The checker RECOMPUTES from the gold and the silver (read-only LIST and GET): the silver table list, the columns of each table the record names, and
the coverage: the account ids of the Cottonwood account_return_daily frontier partition (the Commonwealth keys) that appear in the map table's
custodian column over the partitions the record names, under the normalisation the record declares (exact, strip_leading_zeros or zero_pad_10).

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
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~189/RD_KEY_MAP_READ_R119.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~189/key_map_read_r119.py"
BUCKET = "opal-data-assets"
SILVER = "blackdiamond/cottonwood/silver/"
FIRM = "cottonwood"
NORMS = ("exact", "strip_leading_zeros", "zero_pad_10")
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("49financial", "inflection", "orion/", "eclipse/", "opal-data-49financial", "opal-data-inflection")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item",
                "delete_item", "update_item", "write_table", "write_to_dataset", ".to_parquet(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "date")
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


def norm(x, how):
    s = str(x).strip()
    if how == "strip_leading_zeros":
        return s.lstrip("0")
    if how == "zero_pad_10":
        return s.zfill(10)
    return s


def mapped_count(frontier_ids, custodian_values, how):
    vals = {norm(v, how) for v in custodian_values if v is not None}
    return sum(1 for a in frontier_ids if norm(a, how) in vals)


# ------------------------------------------------------------------------------------------------ the recount (read-only)
def recount(root, rec):
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    from lib import opal_naming
    s3 = boto3.client("s3")
    tabs, tok = [], None
    while True:
        kw = dict(Bucket=BUCKET, Prefix=SILVER, Delimiter="/")
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        tabs += [c["Prefix"][len(SILVER):].strip("/") for c in r.get("CommonPrefixes", [])]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    out = {"tables_listed": len(tabs), "tables": sorted(tabs), "columns": {}, "coverage": None}

    def part(table, day):
        body = s3.get_object(Bucket=BUCKET, Key="%s%s/date=%s/data.parquet" % (SILVER, table, day))["Body"].read()
        return pq.read_table(io.BytesIO(body))
    for c in rec["candidates"]:
        t = part(c["table"], c["partition_date"])
        out["columns"][c["table"]] = set(t.schema.names)
    mp = rec["map"]
    if mp.get("exists"):
        ids, vals = None, []
        addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=%s" % rec["frontier"]["date"])
        gb, gk = addr[len("s3://"):].split("/", 1)
        body = s3.get_object(Bucket=gb, Key=gk.rstrip("/") + "/data.parquet")["Body"].read()
        ids = pq.read_table(io.BytesIO(body), columns=["account_id"]).to_pydict()["account_id"]
        for d in mp["partitions_read"]:
            t = part(mp["table"], d)
            vals += t.column(mp["custodian_column"]).to_pylist()
        out["coverage"] = {"frontier_ids": len(set(ids)), "mapped": mapped_count(set(ids), vals, mp["normalization"])}
    return out


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, truth, analysis_text, tracked, analysis_sha):
    exp = {"tables_listed", "tables_with_partitions", "candidates", "frontier", "map", "history", "seam_words", "analysis", "reads", "claim",
           "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["tables_listed"] == truth["tables_listed"], "tables_listed: record %s, recount %s" % (rec["tables_listed"], truth["tables_listed"]))
    need(is_int(rec["tables_with_partitions"]) and 0 < rec["tables_with_partitions"] <= rec["tables_listed"], "tables_with_partitions")
    cands = rec["candidates"]
    need(isinstance(cands, list) and len(cands) >= 1, "at least one candidate table")
    for c in cands:
        need(set(c) == {"table", "partition_date", "account_key_columns", "custodian_number_columns", "claim"} and c["claim"] in CLAIMS
             and ISO.match(str(c["partition_date"])) and c["table"] in truth["tables"], "a candidate entry: %s" % c.get("table"))
        for k in ("account_key_columns", "custodian_number_columns"):
            need(isinstance(c[k], list) and all(nes(x) for x in c[k]), "%s form" % k)
            cols = truth["columns"].get(c["table"], set())
            need(all(x in cols for x in c[k]), "a column the record names is not in %s: %s" % (c["table"], [x for x in c[k] if x not in cols]))
    fr = rec["frontier"]
    need(isinstance(fr, dict) and set(fr) == {"date", "account_ids", "claim"} and ISO.match(str(fr["date"])) and is_int(fr["account_ids"]) and fr["claim"] in CLAIMS,
         "frontier form")
    mp = rec["map"]
    need(isinstance(mp, dict) and isinstance(mp.get("exists"), bool) and nes(mp.get("words")) and mp.get("claim") in CLAIMS, "map form")
    if mp["exists"]:
        need(set(mp) == {"exists", "table", "key_column", "custodian_column", "normalization", "partitions_read", "coverage", "words", "claim"},
             "an existing map carries table, key_column, custodian_column, normalization, partitions_read, coverage")
        need(mp["table"] in truth["columns"] and mp["key_column"] in truth["columns"][mp["table"]] and mp["custodian_column"] in truth["columns"][mp["table"]],
             "the map's columns must be columns of the map table (as listed by the recount)")
        need(mp["normalization"] in NORMS, "normalization must be one of %s" % (NORMS,))
        need(isinstance(mp["partitions_read"], list) and 1 <= len(mp["partitions_read"]) <= 10 and all(ISO.match(str(d)) for d in mp["partitions_read"]), "partitions_read")
        cv = mp["coverage"]
        need(isinstance(cv, dict) and set(cv) == {"frontier_ids", "mapped", "unmapped"} and all(is_int(cv[k]) and cv[k] >= 0 for k in cv), "coverage form")
        t = truth["coverage"]
        need(cv["frontier_ids"] == t["frontier_ids"] == fr["account_ids"] and cv["mapped"] == t["mapped"] and cv["unmapped"] == t["frontier_ids"] - t["mapped"],
             "coverage: record %s, recount %s" % (cv, t))
    else:
        need(set(mp) == {"exists", "words", "claim"}, "an absent map carries exists, words and claim only")
        need("SOURCE_BREAK" in rec["seam_words"], "with no map the seam words must say SOURCE_BREAK")
    need(nes(rec["seam_words"]), "seam_words")
    h = rec["history"]
    need(isinstance(h, dict) and set(h) == {"distinct_commonwealth_ids", "partitions", "claim"} and is_int(h["distinct_commonwealth_ids"]) and is_int(h["partitions"])
         and h["claim"] in CLAIMS and h["partitions"] > 0, "history form")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == ANALYSIS_REL and an.get("tracked") is True and an.get("sha256") == analysis_sha and tracked, "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["claim"] in CLAIMS and rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False
         and rec["deployed"] is False, "claim or a flag")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    low = analysis_text.lower()
    need(not [t for t in FOREIGN if t in low], "the analysis script names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the analysis script holds a write call")
    return True


def run(root, cid):
    need(cid == "DB119-3-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root, rec)
    check_record(rec, truth, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), hashlib.sha256(ap.read_bytes()).hexdigest())
    cv = truth["coverage"]
    print("OK: key-map read: %d silver tables (recounted); map %s; %s" % (truth["tables_listed"], "EXISTS" if rec["map"]["exists"] else "ABSENT",
          ("coverage %d of %d Commonwealth ids at the frontier (recounted)" % (cv["mapped"], cv["frontier_ids"])) if cv else "seam words say SOURCE_BREAK"))
    return True


def selftest(root):
    need(norm(" 00123 ", "exact") == "00123" and norm("00123", "strip_leading_zeros") == "123" and norm("123", "zero_pad_10") == "0000000123", "norm")
    need(mapped_count({"00123", "999"}, ["123", None], "strip_leading_zeros") == 1 and mapped_count({"00123"}, ["123"], "exact") == 0, "mapped_count")
    truth = {"tables_listed": 14, "tables": ["fact_allocations", "fact_transactions"],
             "columns": {"fact_allocations": {"AccountID", "Account Number", "Original Account Number"}},
             "coverage": {"frontier_ids": 12, "mapped": 9}}

    def good():
        return {"tables_listed": 14, "tables_with_partitions": 9,
                "candidates": [{"table": "fact_allocations", "partition_date": "2026-10-13", "account_key_columns": ["AccountID"],
                                "custodian_number_columns": ["Account Number", "Original Account Number"], "claim": "measured"}],
                "frontier": {"date": "2026-06-22", "account_ids": 12, "claim": "measured"},
                "map": {"exists": True, "table": "fact_allocations", "key_column": "AccountID", "custodian_column": "Account Number",
                        "normalization": "strip_leading_zeros", "partitions_read": ["2026-04-22", "2026-10-13"],
                        "coverage": {"frontier_ids": 12, "mapped": 9, "unmapped": 3}, "words": "the allocations hold both", "claim": "measured"},
                "history": {"distinct_commonwealth_ids": 400, "partitions": 3325, "claim": "measured"}, "seam_words": "the history joins through the map",
                "analysis": {"file": ANALYSIS_REL, "sha256": "ab" * 32, "tracked": True},
                "reads": {"s3_reads": 20, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured",
                "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(rec, text="x = 1", tracked=True, h="ab" * 32, tr=truth):
        try:
            return check_record(rec, tr, text, tracked, h)
        except Fail:
            return False
    need(grade(good()) is True, "GREEN arm failed")
    r = good()
    r["tables_listed"] = 15
    need(grade(r) is False, "RED: a table count that differs from the recount must fail")
    r = good()
    r["candidates"][0]["custodian_number_columns"] = ["Made Up Column"]
    need(grade(r) is False, "RED: a column that is not in the table must fail")
    r = good()
    r["map"]["coverage"]["mapped"] = 10
    r["map"]["coverage"]["unmapped"] = 2
    need(grade(r) is False, "RED: a coverage that differs from the recount must fail")
    r = good()
    r["map"]["normalization"] = "made_up"
    need(grade(r) is False, "RED: an unknown normalisation must fail")
    r = good()
    r["map"] = {"exists": False, "words": "no map", "claim": "measured"}
    need(grade(r) is False, "RED: no map with seam words that do not say SOURCE_BREAK must fail")
    r = good()
    r["map"] = {"exists": False, "words": "no map", "claim": "measured"}
    r["seam_words"] = "Cottonwood history before 2026-06-23 is SOURCE_BREAK at the seam"
    need(grade(r, tr=dict(truth, coverage=None)) is True, "GREEN: no map with SOURCE_BREAK seam words")
    r = good()
    r["seam_words"] = "ids 1234567890"
    need(grade(r) is False, "RED: a long digit run must fail")
    need(grade(good(), tracked=False) is False, "RED: an untracked script must fail")
    need(grade(good(), text="s3.put_object(Bucket=b)") is False, "RED: a write call must fail")
    need(grade(good(), text="b = 'opal-data-49financial'") is False, "RED: another firm's place must fail")
    need(grade(good(), h="cd" * 32) is False, "RED: a hash mismatch must fail")
    r = good()
    r["pushed"] = True
    need(grade(r) is False, "RED: a push flag must fail")
    print("selftest OK: norm and coverage arms, 2 green and 11 red record arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p119_keymap.py <repo_root> <criterion_id>")
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
