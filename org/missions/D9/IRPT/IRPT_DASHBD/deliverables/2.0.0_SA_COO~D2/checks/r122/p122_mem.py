"""IRPT_DASHBD round 122, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-246, the PEAK MEMORY AND PER-DAY TIME of the hop-1 `filled_report_values` stage on the real day (CTO analysis
@e690365741 ruling 1, first cell): round 121 measured one day at 4,012 households and 4,693,967 rows (85.3 s to read the inputs, 76.3 s to build the day) and left the memory of that
day unmeasured. This cell measures the PEAK RESIDENT MEMORY of the stage's two reading functions on that day, LOCAL and read-only, against 70 percent of the function's configured memory,
and states the chunk rule when it is over.

  DB-b-246 (~200) one script that imports the handler, runs `filled_inputs` and `filled_day_rows` for the newest returns day while a sampler thread records the process's resident
                  set size (psutil), and a record of counts, seconds and megabytes; no write of any kind.
                                                                                           DB122-1-AC1 (the record: form, arithmetic, verdict, chunk rule),
                                                                                           DB122-1-AC2 (the script: tracked, hashed, samples the memory, calls the stage, no write call)

The rules the checker recomputes:  configured_memory_mb = the `memory_size` in the reporting-gold lambda.tf;  threshold_mb = 0.7 * configured_memory_mb;
day_seconds = read_inputs_seconds + build_day_seconds;  verdict = CHUNK when peak_rss_mb > threshold_mb, otherwise WHOLE_DAY;
when CHUNK:  per_household_mb = (peak_rss_mb - peak_after_inputs_mb) / households  and  households_per_chunk = max(1, floor((threshold_mb - peak_after_inputs_mb) / per_household_mb)).

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~200/RD_STAGE_MEMORY_R122.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~200/stage_memory_r122.py"
LAMBDA_TF_REL = "infra/aws/terraform/investor-reporting/reporting-gold/lambda.tf"
FIRM = "49financial"
FRACTION = 0.7
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("inflection", "cottonwood", "orion/", "eclipse/", "opal-data-inflection", "opal-data-cottonwood")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item",
                "update_item", "write_table", "write_to_dataset", ".to_parquet(", "emit_filled(", "filled_write(", "filled_stage(", "stream_to_parquet",
                "s3 cp", "s3 sync", "s3 rm", "s3 mv")
LONG_DIGITS = re.compile(r"\d{8,}")
DIGIT_OK_KEYS = ("sha256", "path", "file", "key", "where", "vintage", "day")
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


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


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


def configured_memory(text):
    m = re.search(r"^\s*memory_size\s*=\s*(\d+)", text, re.M)
    need(m is not None, "lambda.tf has no memory_size")
    return int(m.group(1))


def chunk_rule(threshold_mb, after_inputs_mb, peak_mb, households):
    per = (peak_mb - after_inputs_mb) / households
    if per <= 0:
        return None
    return max(1, int(math.floor((threshold_mb - after_inputs_mb) / per)))


def newest_returns_day(root):
    sys.path.insert(0, str(root))
    import boto3
    from lib import opal_naming
    s3 = boto3.client("s3")
    addr = opal_naming.address("irpt", FIRM, "gold", "account_return_daily", "date=2000-01-03")
    bucket, key = addr[len("s3://"):].split("/", 1)
    prefix = key.rsplit("/date=", 1)[0] + "/"
    days, token = [], None
    while True:
        kw = {"Bucket": bucket, "Prefix": prefix, "Delimiter": "/"}
        if token:
            kw["ContinuationToken"] = token
        r = s3.list_objects_v2(**kw)
        days += [c["Prefix"][len(prefix):].strip("/")[len("date="):] for c in r.get("CommonPrefixes", [])]
        if not r.get("IsTruncated"):
            break
        token = r.get("NextContinuationToken")
    days = sorted(d for d in days if ISO.match(d))
    need(days, "no returns partition listed")
    return days


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, configured, listed_days, analysis_text, tracked, analysis_sha):
    exp = {"firm", "day", "configured_memory_mb", "threshold_fraction", "threshold_mb", "accounts", "households", "rows", "read_inputs_seconds", "build_day_seconds",
           "day_seconds", "baseline_rss_mb", "peak_after_inputs_mb", "peak_rss_mb", "sampler", "verdict", "chunk_rule", "measured_on", "words", "analysis", "reads", "claim",
           "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == FIRM and nes(rec["words"]) and rec["claim"] in CLAIMS, "firm, words or claim")
    need(rec["day"] in listed_days, "day %s is not a returns partition the checker lists (it was the newest when measured; a later partition does not void the record)" % rec["day"])
    need(rec["configured_memory_mb"] == configured, "configured_memory_mb %s differs from lambda.tf's %s" % (rec["configured_memory_mb"], configured))
    need(rec["threshold_fraction"] == FRACTION, "threshold_fraction must be 0.7")
    thr = FRACTION * configured
    need(abs(rec["threshold_mb"] - thr) <= 0.5, "threshold_mb %s, recomputed %.1f" % (rec["threshold_mb"], thr))
    for k in ("accounts", "households", "rows"):
        need(is_int(rec[k]) and rec[k] >= 1, "%s must be an integer of at least 1" % k)
    need(rec["households"] <= rec["accounts"] and rec["rows"] >= rec["households"], "counts out of bounds (households <= accounts, rows >= households)")
    for k in ("read_inputs_seconds", "build_day_seconds", "day_seconds", "baseline_rss_mb", "peak_after_inputs_mb", "peak_rss_mb"):
        need(is_num(rec[k]) and rec[k] > 0, "%s must be a positive number" % k)
    need(abs(rec["day_seconds"] - (rec["read_inputs_seconds"] + rec["build_day_seconds"])) <= 0.5, "day_seconds must equal read plus build")
    need(rec["baseline_rss_mb"] <= rec["peak_after_inputs_mb"] <= rec["peak_rss_mb"], "memory marks must satisfy baseline <= after inputs <= peak")
    sm = rec["sampler"]
    need(isinstance(sm, dict) and set(sm) == {"interval_seconds", "samples", "method"} and is_num(sm["interval_seconds"]) and 0 < sm["interval_seconds"] <= 1.0
         and is_int(sm["samples"]) and sm["samples"] >= 10 and nes(sm["method"]), "sampler block (interval at most 1 s, at least 10 samples, a method)")
    want = "CHUNK" if rec["peak_rss_mb"] > thr else "WHOLE_DAY"
    need(rec["verdict"] == want, "verdict %s does not follow the 70 percent line (peak %.1f, threshold %.1f)" % (rec["verdict"], rec["peak_rss_mb"], thr))
    cr = rec["chunk_rule"]
    if want == "WHOLE_DAY":
        need(cr is None, "chunk_rule must be null when the verdict is WHOLE_DAY")
    else:
        need(isinstance(cr, dict) and set(cr) == {"households_per_chunk", "basis"} and is_int(cr["households_per_chunk"]) and nes(cr["basis"]), "chunk_rule block")
        exp_n = chunk_rule(thr, rec["peak_after_inputs_mb"], rec["peak_rss_mb"], rec["households"])
        need(exp_n is not None and abs(cr["households_per_chunk"] - exp_n) <= 1, "households_per_chunk %s, recomputed %s" % (cr["households_per_chunk"], exp_n))
    mo = rec["measured_on"]
    need(isinstance(mo, dict) and set(mo) == {"where", "words"} and mo["where"] == "local" and nes(mo["words"]), "measured_on must say local, with words")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == ANALYSIS_REL and an.get("tracked") is True and an.get("sha256") == analysis_sha and tracked, "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0
         and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    low = analysis_text.lower()
    need(not [t for t in FOREIGN if t in low], "the script names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the script holds a write call or calls a writing stage function")
    need("filled_inputs" in analysis_text and "filled_day_rows" in analysis_text and "psutil" in low, "the script must call filled_inputs and filled_day_rows and sample the memory with psutil")
    return True


def run(root, cid):
    rec = load(root, REC_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no script")
    text = ap.read_text(encoding="utf-8")
    sha = hashlib.sha256(ap.read_bytes()).hexdigest()
    if cid == "DB122-1-AC1":
        configured = configured_memory((Path(root) / LAMBDA_TF_REL).read_text(encoding="utf-8"))
        check_record(rec, configured, newest_returns_day(root), text, is_tracked(root, ANALYSIS_REL), sha)
        print("OK: stage memory: day %s, %d households, %d rows, peak %.0f MB against %.0f MB (70%% of %d) -> %s%s; one day takes %.1f s" %
              (rec["day"], rec["households"], rec["rows"], rec["peak_rss_mb"], rec["threshold_mb"], configured, rec["verdict"],
               "" if rec["chunk_rule"] is None else " (%d households per chunk)" % rec["chunk_rule"]["households_per_chunk"], rec["day_seconds"]))
        return True
    if cid == "DB122-1-AC2":
        need(is_tracked(root, ANALYSIS_REL), "the script is not tracked")
        need(rec["analysis"]["sha256"] == sha, "the recorded script hash differs from the bytes")
        low = text.lower()
        need(not [t for t in WRITE_TOKENS if t in low], "the script holds a write call")
        need("filled_inputs" in text and "filled_day_rows" in text and "handler" in low and "psutil" in low and "thread" in low,
             "the script must import the handler, call filled_inputs and filled_day_rows, and sample psutil from a thread")
        print("OK: the script is tracked, hashed as recorded, samples the resident memory from a thread, calls the stage's two reading functions and holds no write call")
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    good = {"firm": FIRM, "day": "2026-10-13", "configured_memory_mb": 3008, "threshold_fraction": 0.7, "threshold_mb": 2105.6, "accounts": 100, "households": 40, "rows": 5000,
            "read_inputs_seconds": 80.0, "build_day_seconds": 70.0, "day_seconds": 150.0, "baseline_rss_mb": 200.0, "peak_after_inputs_mb": 900.0, "peak_rss_mb": 2800.0,
            "sampler": {"interval_seconds": 0.5, "samples": 300, "method": "psutil rss thread"}, "verdict": "CHUNK", "chunk_rule": {"households_per_chunk": 25, "basis": "w"},
            "measured_on": {"where": "local", "words": "w"}, "words": "w", "analysis": {"file": ANALYSIS_REL, "tracked": True, "sha256": "a" * 64},
            "reads": {"s3_reads": 600, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0}, "claim": "measured", "files_in_repo": False,
            "served_values_changed": False, "pushed": False, "deployed": False}
    good["chunk_rule"]["households_per_chunk"] = chunk_rule(2105.6, 900.0, 2800.0, 40)
    text = "import handler\nimport psutil\nimport threading\nfilled_inputs(a)\nfilled_day_rows(b)\n"

    def grade(rec, t=text):
        try:
            return check_record(rec, 3008, ["2026-10-12", "2026-10-13", "2026-10-14"], t, True, "a" * 64)
        except Fail:
            return False
    assert grade(good) is True
    whole = copy.deepcopy(good)
    whole.update(peak_rss_mb=1500.0, verdict="WHOLE_DAY", chunk_rule=None)
    assert grade(whole) is True

    def mut(f, base=good):
        r = copy.deepcopy(base)
        f(r)
        return r
    for name, r in (("verdict wrong", mut(lambda r: r.update(verdict="WHOLE_DAY", chunk_rule=None))), ("whole with chunk rule", mut(lambda r: r.update(peak_rss_mb=1500.0, verdict="WHOLE_DAY"), good)),
                    ("chunk rule off", mut(lambda r: r["chunk_rule"].update(households_per_chunk=99))), ("threshold off", mut(lambda r: r.update(threshold_mb=1000.0))),
                    ("marks out of order", mut(lambda r: r.update(peak_after_inputs_mb=3000.0))), ("day seconds", mut(lambda r: r.update(day_seconds=10.0))),
                    ("few samples", mut(lambda r: r["sampler"].update(samples=3))), ("not listed", mut(lambda r: r.update(day="2026-10-01"))), ("write flag", mut(lambda r: r["reads"].update(s3_writes=1))),
                    ("configured", mut(lambda r: r.update(configured_memory_mb=2048)))):
        assert grade(r) is False, "red arm %s passed" % name
    assert grade(good, t="import handler\nfilled_inputs\nfilled_day_rows\n") is False
    assert grade(good, t=text + "s3.put_object()") is False
    assert chunk_rule(2000.0, 1000.0, 1000.0, 10) is None and chunk_rule(2000.0, 1000.0, 2000.0, 10) == 10
    assert configured_memory("x\n  memory_size = 3008\n") == 3008
    print("selftest: two green and ten red record arms, two text arms, the chunk rule behave")


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
