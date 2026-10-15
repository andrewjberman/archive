"""IRPT_DASHBD round 114, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the two Inflection reads that let the CTO rule the tie-out tolerance.

  DB-i-1 (~301) the QTD tie-out of round 109 re-run under three value bases (all rows, active rows only, cash lines excluded): the gap distribution per basis and
                the count of households that move down a bin. A READ: nothing is written to AWS.                                                  DBI114-1-AC1
  DB-i-2 (~302) the two Orion trading days with no fact_positions partition (2026-07-01, 2026-09-28): which Orion layers hold them, what a bridge across the gap
                would touch, and who owns the producer. A READ: nothing is written.                                                                DBI114-2-AC1

The checker grades FORM and INTERNAL CONSISTENCY, and RECOMPUTES: for DBI114-1 the round-109 QTD bins from the private gaps file, the per-variant bins from the worker's private
variant file, and the control (basis `all` equals round 109 household by household); for DBI114-2 the library calendar's answer for each date and the partition presence of
each silver table by a fresh LIST through the round-108 reader.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]         the pure helpers on synthetic arms
"""
import hashlib
import json
import re
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC1_REL = D + "0.9.0_WK_IRPT_DASHBD~301/BASIS_VARIANTS_R114.json"
REC2_REL = D + "0.9.0_WK_IRPT_DASHBD~302/DATE_GAP_READ_R114.json"
GAPS109 = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~174/TIEOUT_GAPS.parquet"
PRIV = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/"
CLAIMS = ("measured", "inferred", "held", "absent")
VARIANTS = ("all", "active_only", "ex_cash")
BINS = ("lt_5bp", "5_25bp", "25_100bp", "ge_100bp")
EDGES = (5.0, 25.0, 100.0)
DATES = ("2026-07-01", "2026-09-28")
HOUSEHOLDS = 320
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "prefix", "where")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item", "update_item", "write_table", "to_parquet", "write_dataset")
FOREIGN = ("cottonwood", "blackdiamond", "schwab", "opal-data-cottonwood")
ORION_SILVER = "s3://opal-data-assets/orion/inflection/silver/"


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def bin_of(gap):
    for i, e in enumerate(EDGES):
        if gap < e:
            return BINS[i]
    return BINS[3]


def bins_of(gaps):
    """gaps: iterable of float or None -> (compared, not_comparable, {bin: n})."""
    out = {b: 0 for b in BINS}
    comp = nc = 0
    for g in gaps:
        if g is None or g != g:
            nc += 1
        else:
            comp += 1
            out[bin_of(abs(g))] += 1
    return comp, nc, out


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "record absent: " + rel)
    return json.loads(p.read_text(encoding="utf-8"))


def walk(o, key=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v, key)
    else:
        yield key, o


def no_identifiers(rec):
    for k, v in walk(rec):
        if isinstance(v, str) and LONG_DIGITS.search(v):
            need(any(t in k for t in DIGIT_OK_KEYS), "a run of 8 or more digits under key %r" % k)


def script_clean(root, rel, recorded_sha):
    p = Path(root) / rel
    need(p.is_file(), "script absent: " + rel)
    need(sha(p) == recorded_sha, "script sha256 differs from the record")
    text = p.read_text(encoding="utf-8").lower()
    for t in WRITE_TOKENS:
        need(t not in text, "write token in script: " + t)
    for f in FOREIGN:
        need(f not in text, "foreign firm name in script: " + f)


def common_flags(rec):
    r = rec.get("reads", {})
    for k in ("vendor_calls", "s3_writes", "dynamodb_writes", "secret_reads"):
        need(r.get(k) == 0, "reads.%s must be 0" % k)
    need(isinstance(r.get("s3_reads"), int) and r["s3_reads"] >= 0, "reads.s3_reads must be an integer")
    for k in ("files_in_repo_private", "served_values_changed", "pushed", "deployed"):
        need(rec.get(k) is False, "%s must be false" % k)


def check_1(root):
    import pyarrow.parquet as pq
    rec = load(root, REC1_REL)
    no_identifiers(rec)
    common_flags(rec)
    script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 80, "basis_words missing")
    need(rec.get("window") == "qtd", "window must be qtd")
    # round-109 control, recounted from the private gaps file
    g109 = pq.read_table(GAPS109).to_pandas()
    q = g109[g109["window"] == "qtd"]
    need(len(q) == HOUSEHOLDS, "round-109 qtd rows != 320")
    c109, nc109, b109 = bins_of(list(q["gap_bp"]))
    # the worker's private variant file
    vf = rec["variant_file"]
    need(Path(vf["path"]).is_file() and vf["path"].replace("\\", "/").startswith(PRIV), "variant file absent or outside the private folder")
    need(sha(vf["path"]) == vf["sha256"], "variant file sha256 differs from the record")
    t = pq.read_table(vf["path"]).to_pandas()
    need(list(t.columns) == ["household_sha256", "variant", "gap_bp", "reason"], "variant file columns")
    need(len(t) == HOUSEHOLDS * len(VARIANTS), "variant file rows != 320 x 3")
    for v in VARIANTS:
        tv = t[t["variant"] == v]
        need(len(tv) == HOUSEHOLDS and tv["household_sha256"].nunique() == HOUSEHOLDS, "variant %s: not one row per household" % v)
        nulls = tv[tv["gap_bp"].isna()]
        need(all(isinstance(x, str) and x.strip() for x in nulls["reason"]), "variant %s: a null gap without a reason" % v)
        comp, nc, bins = bins_of(list(tv["gap_bp"]))
        r = rec["variants"][v]
        need(r["clients_compared"] == comp and r["not_comparable"] == nc and r["bins"] == bins, "variant %s: record counts differ from the recount" % v)
        need(r.get("claim") in CLAIMS, "variant %s: claim" % v)
    # the control: basis `all` is round 109, household by household
    ta = t[t["variant"] == "all"].set_index("household_sha256")["gap_bp"]
    tq = q.set_index("household_sha256")["gap_bp"]
    need(set(ta.index) == set(tq.index), "control: household sets differ")
    diff = 0
    for h in tq.index:
        a, b = ta[h], tq[h]
        if (a != a) != (b != b):
            diff += 1
        elif a == a and abs(abs(a) - abs(b)) > 0.01:
            diff += 1
    need(diff == 0, "control: basis all differs from round 109 on %d households" % diff)
    need(rec["variants"]["all"]["bins"] == b109 and rec["variants"]["all"]["not_comparable"] == nc109, "control: record bins differ from round 109")
    # households that move down at least one bin, recomputed
    order = {b: i for i, b in enumerate(BINS)}
    for v in ("active_only", "ex_cash"):
        tv = t[t["variant"] == v].set_index("household_sha256")["gap_bp"]
        n = 0
        for h in ta.index:
            if ta[h] == ta[h] and tv[h] == tv[h] and order[bin_of(abs(tv[h]))] < order[bin_of(abs(ta[h]))]:
                n += 1
        need(rec["moved_down_a_bin"].get(v) == n, "moved_down_a_bin.%s differs from the recount (%d)" % (v, n))


def check_2(root):
    sys.path.insert(0, str(Path(root)))
    from lib import trading_calendar as tc
    rec = load(root, REC2_REL)
    no_identifiers(rec)
    common_flags(rec)
    need(isinstance(rec.get("basis_words"), str) and len(rec["basis_words"]) > 80, "basis_words missing")
    d = rec["dates"]
    need(sorted(d) == sorted(DATES), "dates must be exactly the two named")
    tables = rec["silver_tables"]
    need(isinstance(tables, list) and "fact_positions" in tables and len(tables) >= 3, "silver_tables must list the Orion silver tables found")
    # a fresh LIST of every named table through the round-108 reader
    sys.path.insert(0, str(Path(root) / "data/assets/scripts/gold/irpt_reporting/adapters"))
    import inflection_account_dim as iad
    rd = iad.InflectionSilverReader()
    import boto3
    cl = boto3.client("s3")
    resp = cl.list_objects_v2(Bucket="opal-data-assets", Prefix="orion/inflection/silver/", Delimiter="/")
    found = sorted(cp["Prefix"].split("/")[-2] for cp in resp.get("CommonPrefixes", []))
    need(sorted(tables) == found, "silver_tables differs from a fresh LIST of the Orion silver prefix")
    for date in DATES:
        e = d[date]
        need(e["trading_day"] is tc.is_trading_day(date), "%s: trading_day differs from lib/trading_calendar" % date)
        need(e.get("claim") in CLAIMS, "%s: claim" % date)
        for tb in tables:
            parts = rd.list_partitions(ORION_SILVER + tb)
            need(e["partition_present"][tb] is (("date=" + date) in parts), "%s %s: partition presence differs from a fresh LIST" % (date, tb))
    b = rec["bridge"]
    need(b.get("claim") in CLAIMS, "bridge.claim")
    for date in DATES:
        x = b[date]
        need(isinstance(x["accounts_valued_before"], int) and isinstance(x["accounts_with_external_flow_in_gap"], int), "%s: bridge counts" % date)
        need(0 <= x["accounts_with_external_flow_in_gap"] <= x["accounts_valued_before"], "%s: flow accounts exceed valued accounts" % date)
    o = rec["owner"]
    need((Path(root) / o["producer_file"]).is_file(), "owner.producer_file is not a repo file")
    need(isinstance(o.get("schedule_words"), str) and len(o["schedule_words"]) > 20, "owner.schedule_words")
    need(isinstance(o.get("unrecorded_cause_words"), str), "owner.unrecorded_cause_words")


CHECKS = {"DBI114-1-AC1": check_1, "DBI114-2-AC1": check_2}


def selftest():
    arms = []

    def arm(name, ok):
        arms.append((name, ok))

    arm("bin edges", [bin_of(x) for x in (0.0, 4.99, 5.0, 24.9, 25.0, 99.9, 100.0, 5000)] == ["lt_5bp", "lt_5bp", "5_25bp", "5_25bp", "25_100bp", "25_100bp", "ge_100bp", "ge_100bp"])
    arm("bins_of", bins_of([1.0, -30.0, None, float("nan"), 150.0]) == (3, 2, {"lt_5bp": 1, "5_25bp": 0, "25_100bp": 1, "ge_100bp": 1}))
    arm("no_identifiers red", _raises(lambda: no_identifiers({"x": "id 12345678"})))
    arm("no_identifiers green", not _raises(lambda: no_identifiers({"sha256": "1" * 64, "n": 3})))
    arm("flags red", _raises(lambda: common_flags({"reads": {"vendor_calls": 1}})))
    ok = {"reads": {"vendor_calls": 0, "s3_writes": 0, "dynamodb_writes": 0, "secret_reads": 0, "s3_reads": 4}, "files_in_repo_private": False, "served_values_changed": False, "pushed": False, "deployed": False}
    arm("flags green", not _raises(lambda: common_flags(ok)))
    for n, v in arms:
        print(("ok   " if v else "FAIL ") + n)
    return all(v for _, v in arms)


def _raises(fn):
    try:
        fn()
    except Fail:
        return True
    return False


def main(argv):
    if argv and argv[0] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if len(argv) != 2 or argv[1] not in CHECKS:
        print("usage: <root> <criterion>")
        sys.exit(2)
    try:
        CHECKS[argv[1]](argv[0])
    except Fail as e:
        print("%s FAIL: %s" % (argv[1], e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    except Exception as e:  # a checker error is a FAIL, never a pass
        print("%s FAIL: checker error %s: %s" % (argv[1], type(e).__name__, e))
        print("%s FAIL" % argv[1])
        sys.exit(1)
    print("%s PASS" % argv[1])


if __name__ == "__main__":
    main(sys.argv[1:])
