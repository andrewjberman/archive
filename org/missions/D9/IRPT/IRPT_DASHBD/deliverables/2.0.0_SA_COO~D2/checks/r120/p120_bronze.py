"""IRPT_DASHBD round 120, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-239, the Black Diamond BRONZE READ for the empty silver days and the
key-map count FINISHED (CTO analysis @5e358b0a8f ruling 3).

  DB-b-239 (~193) (1) Black Diamond silver `fact_allocations` has 144 date partitions of which 33 are EMPTY (2026-04-25 to 2026-07-09): does the BRONZE
                  layer hold those days (`bronze/allocations/ALLOCATIONS_DAILY_<date>.xlsx`), and is each bronze file itself empty (a tiny
                  workbook) or not? `gap_days` lists the empty silver days whose bronze object is at least that big. Verdict SOURCE_EMPTY (every empty silver day has a bronze object smaller than the smallest bronze object of a
                  non-empty silver day), SILVER_BUILD_GAP (some empty day has a bronze object at least that big), BRONZE_ABSENT (none has a bronze
                  object) or MIXED. (2) The Commonwealth-to-Black-Diamond key map of DB-b-235 over ALL non-empty allocation partitions: the exact
                  count of the history's distinct Commonwealth accounts it maps.   A READ; counts only; nothing written.   DB120-3-AC1

The checker RECOMPUTES from the silver and bronze (read-only): which silver partitions are empty (the row count of each data.parquet footer), the bronze
object sizes for those days (one LIST of bronze/allocations/), the verdict, and the key map over every non-empty partition (the union of the custodian
column under the record's normalisation) joined to the history ids file the worker wrote to the private folder (its sha256 is checked and three history
partitions are re-read to confirm their ids are in it).

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import io
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~193/RD_BD_BRONZE_AND_MAP_R120.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~193/bd_bronze_and_map_read_r120.py"
PRIVATE_ROOT = "C:/dev/_irpt_private_evidence_20261009/IRPT_DASHBD/0.9.0_WK_IRPT_DASHBD~193/"
BUCKET = "opal-data-assets"
SILVER = "blackdiamond/cottonwood/silver/"
BRONZE_ALLOC = "blackdiamond/cottonwood/bronze/allocations/"
FIRM = "cottonwood"
NORMS = ("exact", "strip_leading_zeros", "zero_pad_10")
VERDICTS = ("SOURCE_EMPTY", "SILVER_BUILD_GAP", "BRONZE_ABSENT", "MIXED")
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("49financial", "inflection", "orion/", "eclipse/", "opal-data-49financial", "opal-data-inflection")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item",
                "delete_item", "update_item", "write_table", "write_to_dataset", ".to_parquet(", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "date", "object_pattern")
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


def verdict_of(empty_days, sizes, nonempty_min):
    """sizes: date -> bytes (absent days missing). The precedence is in the module docstring."""
    present = [d for d in empty_days if d in sizes]
    if not present:
        return "BRONZE_ABSENT"
    if len(present) == len(empty_days) and all(sizes[d] < nonempty_min for d in present):
        return "SOURCE_EMPTY"
    if any(sizes[d] >= nonempty_min for d in present):
        return "SILVER_BUILD_GAP"
    return "MIXED"


def mapped_ids(ids, custodian_values, how):
    vals = {norm(v, how) for v in custodian_values if v is not None}
    return sum(1 for i in ids if norm(i, how) in vals)


# ------------------------------------------------------------------------------------------------ the recount (read-only)
def recount(root, rec):
    sys.path.insert(0, str(root))
    import boto3
    import pyarrow.parquet as pq
    from lib import opal_naming
    s3 = boto3.client("s3")
    parts, tok = [], None
    while True:
        kw = dict(Bucket=BUCKET, Prefix=SILVER + "fact_allocations/", Delimiter="/")
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        parts += [c["Prefix"].rstrip("/").rsplit("date=", 1)[1] for c in r.get("CommonPrefixes", []) if "date=" in c["Prefix"]]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    parts.sort()
    km = rec["key_map"]

    def one(d):
        body = s3.get_object(Bucket=BUCKET, Key="%sfact_allocations/date=%s/data.parquet" % (SILVER, d))["Body"].read()
        t = pq.read_table(io.BytesIO(body), columns=[km["custodian_column"]])
        return d, t.num_rows, t.column(km["custodian_column"]).to_pylist()
    with ThreadPoolExecutor(8) as ex:
        got = list(ex.map(one, parts))
    empty = [d for d, n, _ in got if n == 0]
    nonempty = [d for d, n, _ in got if n > 0]
    custodian = [v for _, n, vals in got if n > 0 for v in vals]
    sizes, tok = {}, None
    while True:
        kw = dict(Bucket=BUCKET, Prefix=BRONZE_ALLOC)
        if tok:
            kw["ContinuationToken"] = tok
        r = s3.list_objects_v2(**kw)
        for o in r.get("Contents", []):
            m = re.search(r"ALLOCATIONS_DAILY_(\d{4}-\d{2}-\d{2})\.xlsx$", o["Key"])
            if m:
                sizes[m.group(1)] = o["Size"]
        if not r.get("IsTruncated"):
            break
        tok = r["NextContinuationToken"]
    nonempty_min = min(sizes[d] for d in nonempty if d in sizes)
    out = {"partitions": len(parts), "empty": empty, "nonempty": nonempty, "sizes": sizes, "nonempty_min": nonempty_min,
           "verdict": verdict_of(empty, sizes, nonempty_min), "mapped_history": None, "mapped_frontier": None, "frontier": None}
    # the history ids file (private, worker-written) joined to the exact union
    hf = km["history_ids_file"]
    p = Path(str(hf["path"]))
    need(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == hf["sha256"], "the history ids file is missing or its sha256 differs")
    ids = [x for x in p.read_text(encoding="utf-8").split("\n") if x]
    out["history_ids"] = len(set(ids))
    out["mapped_history"] = mapped_ids(set(ids), custodian, km["normalization"])
    addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=%s" % km["frontier_date"])
    gb, gk = addr[len("s3://"):].split("/", 1)
    fr = pq.read_table(io.BytesIO(s3.get_object(Bucket=gb, Key=gk.rstrip("/") + "/data.parquet")["Body"].read()), columns=["account_id"]).to_pydict()["account_id"]
    out["frontier"] = len(set(fr))
    out["mapped_frontier"] = mapped_ids(set(fr), custodian, km["normalization"])
    # three history partitions re-read: their ids must be in the file
    pl = []
    tok = None
    base = gk.rsplit("date=", 1)[0]
    r = s3.list_objects_v2(Bucket=gb, Prefix=base, Delimiter="/", MaxKeys=1000)
    pl = sorted(c["Prefix"] for c in r.get("CommonPrefixes", []))
    for pre in (pl[0], pl[len(pl) // 2], pl[-1]):
        b = s3.get_object(Bucket=gb, Key=pre + "data.parquet")["Body"].read()
        got_ids = set(pq.read_table(io.BytesIO(b), columns=["account_id"]).to_pydict()["account_id"])
        need(got_ids <= set(ids), "a history partition holds ids the worker's history file lacks")
    return out


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, truth, analysis_text, tracked, analysis_sha):
    exp = {"silver", "bronze", "key_map", "words", "analysis", "reads", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(nes(rec["words"]) and rec["claim"] in CLAIMS, "words or claim")
    s = rec["silver"]
    need(isinstance(s, dict) and set(s) == {"partitions", "empty_days", "nonempty_days", "claim"} and s["claim"] in CLAIMS, "silver form")
    need(s["partitions"] == truth["partitions"] and s["empty_days"] == truth["empty"] and s["nonempty_days"] == len(truth["nonempty"]),
         "silver: record %s/%s/%s, recount %s/%s/%s" % (s.get("partitions"), len(s.get("empty_days", [])), s.get("nonempty_days"), truth["partitions"], len(truth["empty"]), len(truth["nonempty"])))
    b = rec["bronze"]
    need(isinstance(b, dict) and set(b) == {"object_pattern", "empty_day_objects", "nonempty_day_bytes_min", "gap_days", "verdict", "words", "claim"} and b["claim"] in CLAIMS and nes(b["words"]),
         "bronze form")
    need(b["nonempty_day_bytes_min"] == truth["nonempty_min"], "nonempty_day_bytes_min: record %s, recount %s" % (b["nonempty_day_bytes_min"], truth["nonempty_min"]))
    objs = b["empty_day_objects"]
    need(isinstance(objs, list) and [o.get("date") for o in objs] == truth["empty"], "empty_day_objects must list the empty days, in order")
    for o in objs:
        need(set(o) == {"date", "present", "bytes"} and isinstance(o["present"], bool), "an empty_day_objects entry")
        want = truth["sizes"].get(o["date"])
        need((want is None and o["present"] is False and o["bytes"] is None) or (want is not None and o["present"] is True and o["bytes"] == want),
             "bronze object of %s: record %s/%s, recount %s" % (o["date"], o["present"], o["bytes"], want))
    gap = [d for d in truth["empty"] if d in truth["sizes"] and truth["sizes"][d] >= truth["nonempty_min"]]
    need(b["gap_days"] == gap, "gap_days (empty silver days whose bronze object is as big as a non-empty day's): record %s, recount %s" % (b["gap_days"], gap))
    need(b["verdict"] in VERDICTS and b["verdict"] == truth["verdict"], "verdict: record %s, recount %s" % (b.get("verdict"), truth["verdict"]))
    km = rec["key_map"]
    need(isinstance(km, dict) and set(km) == {"table", "key_column", "custodian_column", "normalization", "partitions_read", "frontier_date", "history_ids_file",
                                               "history_ids_total", "mapped_history_ids", "frontier_ids", "mapped_frontier_ids", "claim"} and km["claim"] in CLAIMS,
         "key_map form")
    need(km["normalization"] in NORMS and km["table"] == "fact_allocations", "key_map normalization or table")
    need(km["partitions_read"] == len(truth["nonempty"]), "partitions_read must be ALL %d non-empty partitions" % len(truth["nonempty"]))
    hf = km["history_ids_file"]
    need(isinstance(hf, dict) and set(hf) == {"path", "sha256", "ids"} and str(hf["path"]).replace("\\", "/").startswith(PRIVATE_ROOT) and is_int(hf["ids"]), "history_ids_file form")
    need(km["history_ids_total"] == truth["history_ids"] == hf["ids"], "history_ids_total: record %s, file %s" % (km["history_ids_total"], truth["history_ids"]))
    need(km["mapped_history_ids"] == truth["mapped_history"], "mapped_history_ids: record %s, recount %s" % (km["mapped_history_ids"], truth["mapped_history"]))
    need(km["frontier_ids"] == truth["frontier"] and km["mapped_frontier_ids"] == truth["mapped_frontier"], "frontier counts: record %s/%s, recount %s/%s" %
         (km["frontier_ids"], km["mapped_frontier_ids"], truth["frontier"], truth["mapped_frontier"]))
    need(km["mapped_history_ids"] <= km["history_ids_total"], "mapped above total")
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
    need(cid == "DB120-3-AC1", "unknown criterion %s" % cid)
    rec = load(root, REC_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no analysis script")
    truth = recount(root, rec)
    check_record(rec, truth, ap.read_text(encoding="utf-8"), is_tracked(root, ANALYSIS_REL), hashlib.sha256(ap.read_bytes()).hexdigest())
    print("OK: bronze and key map: %d silver partitions, %d empty (recounted); bronze verdict %s (recounted from the object sizes); key map over all %d non-empty "
          "partitions maps %d of %d history ids and %d of %d frontier ids (recounted)" %
          (truth["partitions"], len(truth["empty"]), truth["verdict"], len(truth["nonempty"]), truth["mapped_history"], truth["history_ids"], truth["mapped_frontier"], truth["frontier"]))
    return True


def selftest(root):
    need(verdict_of(["a", "b"], {}, 100) == "BRONZE_ABSENT", "absent")
    need(verdict_of(["a", "b"], {"a": 10, "b": 20}, 100) == "SOURCE_EMPTY", "source empty")
    need(verdict_of(["a", "b"], {"a": 10, "b": 500}, 100) == "SILVER_BUILD_GAP", "silver build gap")
    need(verdict_of(["a", "b"], {"a": 10}, 100) == "MIXED", "mixed")
    need(mapped_ids({"007", "9"}, ["7", None], "strip_leading_zeros") == 1 and mapped_ids({"007"}, ["7"], "exact") == 0, "mapped_ids")
    truth = {"partitions": 4, "empty": ["2026-05-01", "2026-05-02"], "nonempty": ["2026-05-03", "2026-05-04"], "sizes": {"2026-05-01": 4300, "2026-05-02": 4300, "2026-05-03": 5600},
             "nonempty_min": 5600, "verdict": "SOURCE_EMPTY", "history_ids": 10, "mapped_history": 6, "frontier": 12, "mapped_frontier": 5}

    def good():
        return {"silver": {"partitions": 4, "empty_days": ["2026-05-01", "2026-05-02"], "nonempty_days": 2, "claim": "measured"},
                "bronze": {"object_pattern": "allocations/ALLOCATIONS_DAILY_<date>.xlsx", "nonempty_day_bytes_min": 5600, "gap_days": [], "verdict": "SOURCE_EMPTY", "words": "w", "claim": "measured",
                           "empty_day_objects": [{"date": "2026-05-01", "present": True, "bytes": 4300}, {"date": "2026-05-02", "present": True, "bytes": 4300}]},
                "key_map": {"table": "fact_allocations", "key_column": "AccountID", "custodian_column": "NFS Account Number", "normalization": "exact", "partitions_read": 2,
                            "frontier_date": "2026-06-22", "history_ids_file": {"path": PRIVATE_ROOT + "h.txt", "sha256": "ab" * 32, "ids": 10}, "history_ids_total": 10,
                            "mapped_history_ids": 6, "frontier_ids": 12, "mapped_frontier_ids": 5, "claim": "measured"},
                "words": "w", "analysis": {"file": ANALYSIS_REL, "sha256": "cd" * 32, "tracked": True},
                "reads": {"s3_reads": 9, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured",
                "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}

    def grade(rec, text="x = 1", tracked=True, h="cd" * 32):
        try:
            return check_record(rec, truth, text, tracked, h)
        except Fail:
            return False
    need(grade(good()) is True, "GREEN arm failed")
    for mut, why in ((lambda r: r["silver"].update(empty_days=["2026-05-01"]), "an empty-day list that differs"),
                     (lambda r: r["bronze"]["empty_day_objects"][0].update(bytes=4301), "a bronze size that differs"),
                     (lambda r: r["bronze"].update(verdict="SILVER_BUILD_GAP"), "a verdict that differs"),
                     (lambda r: r["bronze"].update(nonempty_day_bytes_min=5601), "the non-empty minimum"),
                     (lambda r: r["bronze"].update(gap_days=["2026-05-01"]), "a gap_days list that differs"),
                     (lambda r: r["key_map"].update(mapped_history_ids=7), "a mapped count that differs"),
                     (lambda r: r["key_map"].update(partitions_read=1), "not all partitions read"),
                     (lambda r: r["key_map"].update(normalization="made_up"), "an unknown normalisation"),
                     (lambda r: r["key_map"].update(mapped_frontier_ids=6), "a frontier count that differs"),
                     (lambda r: r.update(words="ids 1234567890"), "a digit run"), (lambda r: r.update(pushed=True), "a push flag")):
        r = json.loads(json.dumps(good()))
        mut(r)
        need(grade(r) is False, "RED: " + why)
    need(grade(good(), tracked=False) is False, "RED: an untracked script must fail")
    need(grade(good(), text="s3.put_object(Bucket=b)") is False, "RED: a write call must fail")
    need(grade(good(), text="b = 'opal-data-49financial'") is False, "RED: another firm's place must fail")
    need(grade(good(), h="00" * 32) is False, "RED: a hash mismatch must fail")
    print("selftest OK: verdict and mapping arms, 1 green and 14 red record arms")


if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2 and sys.argv[1] == "--selftest":
            selftest(sys.argv[2] if len(sys.argv) > 2 else ".")
            sys.exit(0)
        if len(sys.argv) != 3:
            print("usage: p120_bronze.py <repo_root> <criterion_id>")
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
