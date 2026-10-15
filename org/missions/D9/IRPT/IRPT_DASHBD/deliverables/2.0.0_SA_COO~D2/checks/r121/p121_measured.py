"""IRPT_DASHBD round 121, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-242, the MEASURED RUN of the hop-1 `filled_report_values` stage (CTO analysis
@9d4bd6adf3 ruling 2): the stage of the 49 Financial reporting-gold handler (round 120, DB-b-237) run LOCAL against the real gold, nothing written, with the time
of reading its inputs and of building one day, so that the apply pair states a number and chooses between SHARING the 07:41 fire and an OWN INVOCATION.

  DB-b-242 (~196) one script that imports the handler of the landed tree, builds the stage's inputs for the 49 Financial population with `filled_inputs` and one
                  day's rows with `filled_day_rows` (upload never called), timing each; a record of counts and seconds; no S3 write of any kind.
                                                                                           DB121-1-AC1 (the record: form, arithmetic, verdict, day),
                                                                                           DB121-1-AC2 (the script: tracked, hashed, calls the stage, no write call)

The rule (CTO ruling 2): fire_estimate_seconds = read_inputs_seconds + max_days_per_fire * build_day_seconds / days_built; verdict OWN_INVOCATION when the estimate is
over 600 seconds, otherwise SHARE_FIRE. The record's day must be the newest account_return_daily partition of the firm (the checker lists S3).

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest [<repo_root>]          the pure helpers and the record clauses on synthetic arms
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~196/RD_STAGE_MEASURED_R121.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~196/stage_measure_r121.py"
HANDLER_REL = "infra/aws/lambda/investor-reporting/reporting-gold/handler.py"
FIRM = "49financial"
THRESHOLD = 600.0
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


def estimate(read_s, build_s, days_built, max_days):
    return read_s + max_days * build_s / days_built


def verdict_of(est):
    return "OWN_INVOCATION" if est > THRESHOLD else "SHARE_FIRE"


def handler_max_days(text):
    m = re.search(r"^MAX_DAYS_PER_FIRE\s*=\s*(\d+)", text, re.M)
    need(m is not None, "the handler has no MAX_DAYS_PER_FIRE")
    return int(m.group(1))


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
    return days[-1], len(days)


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, max_days, newest_day, analysis_text, tracked, analysis_sha):
    exp = {"firm", "day", "max_days_per_fire", "threshold_seconds", "accounts", "households", "rows", "days_built", "read_inputs_seconds", "build_day_seconds",
           "fire_estimate_seconds", "verdict", "measured_on", "words", "analysis", "reads", "claim", "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == FIRM and nes(rec["words"]) and rec["claim"] in CLAIMS, "firm, words or claim")
    need(rec["day"] == newest_day, "day %s is not the newest returns partition %s" % (rec["day"], newest_day))
    need(rec["max_days_per_fire"] == max_days, "max_days_per_fire %s differs from the handler's %s" % (rec["max_days_per_fire"], max_days))
    need(rec["threshold_seconds"] == THRESHOLD, "threshold_seconds must be 600")
    for k in ("accounts", "households", "rows", "days_built"):
        need(is_int(rec[k]) and rec[k] >= 1, "%s must be an integer of at least 1" % k)
    need(rec["households"] <= rec["accounts"] and rec["rows"] >= rec["households"], "counts out of bounds (households <= accounts, rows >= households)")
    for k in ("read_inputs_seconds", "build_day_seconds", "fire_estimate_seconds"):
        need(is_num(rec[k]) and rec[k] > 0, "%s must be a positive number" % k)
    est = estimate(rec["read_inputs_seconds"], rec["build_day_seconds"], rec["days_built"], max_days)
    need(abs(est - rec["fire_estimate_seconds"]) <= 0.5, "fire_estimate_seconds %s, recomputed %.3f" % (rec["fire_estimate_seconds"], est))
    need(rec["verdict"] == verdict_of(rec["fire_estimate_seconds"]), "verdict %s does not follow the 600 second rule" % rec["verdict"])
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
    need("filled_inputs" in analysis_text and "filled_day_rows" in analysis_text, "the script must call the stage's filled_inputs and filled_day_rows")
    return True


def run(root, cid):
    rec = load(root, REC_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no script")
    text = ap.read_text(encoding="utf-8")
    sha = hashlib.sha256(ap.read_bytes()).hexdigest()
    max_days = handler_max_days((Path(root) / HANDLER_REL).read_text(encoding="utf-8"))
    if cid == "DB121-1-AC1":
        newest, n = newest_returns_day(root)
        check_record(rec, max_days, newest, text, is_tracked(root, ANALYSIS_REL), sha)
        print("OK: stage measured: day %s (newest of %d returns partitions), %d households, %d rows, read %.1fs, build %.1fs, estimate %.1fs -> %s" %
              (rec["day"], n, rec["households"], rec["rows"], rec["read_inputs_seconds"], rec["build_day_seconds"], rec["fire_estimate_seconds"], rec["verdict"]))
        return True
    if cid == "DB121-1-AC2":
        need(is_tracked(root, ANALYSIS_REL), "the script is not tracked")
        need(rec["analysis"]["sha256"] == sha, "the recorded script hash differs from the bytes")
        low = text.lower()
        need(not [t for t in WRITE_TOKENS if t in low], "the script holds a write call")
        need("filled_inputs" in text and "filled_day_rows" in text and "handler" in low, "the script must import the handler and call filled_inputs and filled_day_rows")
        print("OK: the script is tracked, hashed as recorded, calls the stage's two reading functions and holds no write call")
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    good = {"firm": FIRM, "day": "2026-10-13", "max_days_per_fire": 10, "threshold_seconds": 600.0, "accounts": 100, "households": 40, "rows": 5000, "days_built": 1,
            "read_inputs_seconds": 50.0, "build_day_seconds": 5.0, "fire_estimate_seconds": 100.0, "verdict": "SHARE_FIRE", "measured_on": {"where": "local", "words": "x"},
            "words": "w", "analysis": {"file": ANALYSIS_REL, "tracked": True, "sha256": "a" * 64}, "reads": {"s3_reads": 3, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0,
            "secret_reads": 0}, "claim": "measured", "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}
    text = "import handler\nfilled_inputs(a)\nfilled_day_rows(b)\n"
    arms = [("green", good, True)]
    import copy

    def mut(f):
        r = copy.deepcopy(good)
        f(r)
        return r
    arms += [("estimate wrong", mut(lambda r: r.update(fire_estimate_seconds=90.0)), False),
             ("verdict wrong", mut(lambda r: r.update(read_inputs_seconds=700.0, fire_estimate_seconds=750.0)), False),
             ("not the newest day", mut(lambda r: r.update(day="2026-10-12")), False),
             ("write flag", mut(lambda r: r["reads"].update(s3_writes=1)), False),
             ("extra key", mut(lambda r: r.update(extra=1)), False),
             ("households over accounts", mut(lambda r: r.update(households=200)), False),
             ("not local", mut(lambda r: r["measured_on"].update(where="lambda")), False)]
    for name, rec, ok in arms:
        try:
            check_record(rec, 10, "2026-10-13", text, True, "a" * 64)
            got = True
        except Fail:
            got = False
        assert got == ok, "selftest arm %s: expected %s" % (name, ok)
    for name, t in (("write call", text + "s3.put_object()"), ("no stage call", "import handler\n")):
        try:
            check_record(good, 10, "2026-10-13", t, True, "a" * 64)
            raise AssertionError("selftest arm %s should fail" % name)
        except Fail:
            pass
    assert verdict_of(600.0) == "SHARE_FIRE" and verdict_of(600.5) == "OWN_INVOCATION"
    assert abs(estimate(50.0, 5.0, 1, 10) - 100.0) < 1e-9
    assert handler_max_days("X = 1\nMAX_DAYS_PER_FIRE = 10\n") == 10
    print("selftest: %d record arms and 2 text arms behave; the verdict and estimate rules hold" % len(arms))


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
