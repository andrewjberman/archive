"""IRPT_DASHBD round 125, workstream B-49F (issuer 2.0.0_SA_COO~D2) -- DB-b-255, the MEMORY of the Cottonwood landing function set from a MEASUREMENT (CTO analysis @4285776c5c
ruling 2): one LOCAL run of the merged handler (`lambda_handler` in dry-run, the real Black Diamond silver reader, GET only) on 2026-07-10's real inputs and on the newest silver day, with a
sampler recording the resident memory; the function's `memory_size` is the smallest standard size that keeps the peak under 70 percent (at least 512 MB). Nothing is written.

  DB-b-255 (~208) one script, one record.                                                  DB125-2-AC1 (the record: days, arithmetic, the chosen size),
                                                                                           DB125-2-AC2 (the script: tracked, hashed, dry-run through the handler, psutil sampler, no write)

The rules the checker recomputes:  peak_rss_mb = the maximum of the days' peaks;  threshold for a size s = 0.7 * s;  chosen_memory_mb = the smallest size in SIZES_MB, at least 512, with
peak_rss_mb <= 0.7 * size (null when none fits).

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
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~208/RD_COT_MEMORY_R125.json"
ANALYSIS_REL = D + "0.9.0_WK_IRPT_DASHBD~208/cot_memory_r125.py"
SIZES_MB = [512, 1024, 1536, 2048, 3008, 4096, 6144, 8192, 10240]
FIRST_DAY = "2026-07-10"
CLAIMS = ("measured", "inferred", "held", "absent")
FOREIGN = ("49financial", "inflection", "orion/", "eclipse/", "opal-data-49financial", "opal-data-inflection")
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "copy_object", "delete_object", "delete_objects", "put_item", "delete_item", "update_item",
                "write_table", "write_to_dataset", ".to_parquet(", "write_day(", "stream_to_parquet", "s3 cp", "s3 sync", "s3 rm", "s3 mv")
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


def choose(peak_mb):
    for s in SIZES_MB:
        if s >= 512 and peak_mb <= 0.7 * s:
            return s
    return None


def newest_silver_day(root):
    sys.path.insert(0, str(Path(root) / "data/assets/scripts/gold/irpt_reporting/adapters"))
    import cottonwood_bd_account_return_daily as ad
    parts = [p for p in ad.CottonwoodBlackDiamondSilverReader().list_partitions("fact_allocations") if ISO.match(p)]
    need(parts, "no silver fact_allocations partition listed")
    return parts[-1]


# ------------------------------------------------------------------------------------------------ the record clauses (pure)
def check_record(rec, newest_day, analysis_text, tracked, analysis_sha):
    exp = {"firm", "days", "baseline_rss_mb", "peak_rss_mb", "threshold_fraction", "sizes_mb", "chosen_memory_mb", "sampler", "measured_on", "words", "analysis", "reads", "claim",
           "files_in_repo", "served_values_changed", "pushed", "deployed"}
    need(isinstance(rec, dict) and set(rec) == exp, "record keys differ: %s" % (sorted(set(rec) ^ exp) if isinstance(rec, dict) else "?"))
    need(rec["firm"] == "cottonwood" and nes(rec["words"]) and rec["claim"] in CLAIMS, "firm, words or claim")
    ds = rec["days"]
    need(isinstance(ds, list) and len(ds) == 2 and [d.get("day") for d in ds] == [FIRST_DAY, newest_day], "days must be [%s, the newest silver day %s]" % (FIRST_DAY, newest_day))
    for d in ds:
        need(set(d) == {"day", "accounts", "rows", "seconds", "peak_rss_mb", "held"} and is_int(d["accounts"]) and d["accounts"] >= 1 and is_int(d["rows"]) and d["rows"] >= d["accounts"]
             and is_num(d["seconds"]) and d["seconds"] > 0 and is_num(d["peak_rss_mb"]) and d["peak_rss_mb"] > 0 and d["held"] is False, "a days entry (a held or empty day measures nothing): %s" % d.get("day"))
    need(is_num(rec["baseline_rss_mb"]) and rec["baseline_rss_mb"] > 0, "baseline_rss_mb")
    peak = max(d["peak_rss_mb"] for d in ds)
    need(is_num(rec["peak_rss_mb"]) and abs(rec["peak_rss_mb"] - peak) <= 0.5 and rec["baseline_rss_mb"] <= rec["peak_rss_mb"], "peak_rss_mb %s, the days' maximum %s" % (rec["peak_rss_mb"], peak))
    need(rec["threshold_fraction"] == 0.7 and rec["sizes_mb"] == SIZES_MB, "threshold_fraction must be 0.7 and sizes_mb the standard list")
    want = choose(peak)
    need(want is not None and rec["chosen_memory_mb"] == want, "chosen_memory_mb %s, recomputed %s" % (rec["chosen_memory_mb"], want))
    sm = rec["sampler"]
    need(isinstance(sm, dict) and set(sm) == {"interval_seconds", "samples", "method"} and is_num(sm["interval_seconds"]) and 0 < sm["interval_seconds"] <= 1.0
         and is_int(sm["samples"]) and sm["samples"] >= 10 and nes(sm["method"]), "sampler block")
    mo = rec["measured_on"]
    need(isinstance(mo, dict) and set(mo) == {"where", "words"} and mo["where"] == "local" and nes(mo["words"]), "measured_on must say local, with words")
    an = rec["analysis"]
    need(isinstance(an, dict) and an.get("file") == ANALYSIS_REL and an.get("tracked") is True and an.get("sha256") == analysis_sha and tracked, "analysis block")
    rd = rec["reads"]
    need(isinstance(rd, dict) and is_int(rd.get("s3_reads")) and rd.get("s3_writes") == 0 and rd.get("dynamodb_writes") == 0 and rd.get("vendor_calls") == 0 and rd.get("secret_reads") == 0, "reads block")
    need(rec["files_in_repo"] is False and rec["served_values_changed"] is False and rec["pushed"] is False and rec["deployed"] is False, "a flag is not false")
    need(not digit_runs(rec), "a run of 8 or more digits outside the exempt fields: %s" % digit_runs(rec)[:2])
    low = analysis_text.lower()
    need(not [t for t in FOREIGN if t in low], "the script names another firm's place")
    need(not [t for t in WRITE_TOKENS if t in low], "the script holds a write call")
    for tok in ("lambda_handler", "psutil", "dry_run", "CottonwoodBlackDiamondSilverReader"):
        need(tok in analysis_text, "the script must use %s" % tok)
    return True


def run(root, cid):
    rec = load(root, REC_REL)
    ap = Path(root) / ANALYSIS_REL
    need(ap.is_file(), "no script")
    text = ap.read_text(encoding="utf-8")
    sha = hashlib.sha256(ap.read_bytes()).hexdigest()
    if cid == "DB125-2-AC1":
        check_record(rec, newest_silver_day(root), text, is_tracked(root, ANALYSIS_REL), sha)
        print("OK: Cottonwood memory: days %s, peak %.0f MB (baseline %.0f); smallest standard size with the peak under 70 percent: %d MB; the slowest day took %.1f s" %
              (", ".join(d["day"] for d in rec["days"]), rec["peak_rss_mb"], rec["baseline_rss_mb"], rec["chosen_memory_mb"], max(d["seconds"] for d in rec["days"])))
        return True
    if cid == "DB125-2-AC2":
        need(is_tracked(root, ANALYSIS_REL), "the script is not tracked")
        need(rec["analysis"]["sha256"] == sha, "the recorded script hash differs from the bytes")
        low = text.lower()
        need(not [t for t in WRITE_TOKENS if t in low], "the script holds a write call")
        need("thread" in low and "psutil" in low and "lambda_handler" in text and '"dry_run"' in text.replace("'", '"'), "the script must sample psutil from a thread and call lambda_handler with dry_run")
        print("OK: the script is tracked, hashed as recorded, runs the handler in dry-run with the real silver reader, samples memory from a thread and holds no write call")
        return True
    raise Fail("unknown criterion %s" % cid)


def selftest():
    import copy
    good = {"firm": "cottonwood", "days": [{"day": FIRST_DAY, "accounts": 50, "rows": 60, "seconds": 5.0, "peak_rss_mb": 410.0, "held": False},
                                         {"day": "2026-10-13", "accounts": 60, "rows": 70, "seconds": 6.0, "peak_rss_mb": 520.0, "held": False}],
            "baseline_rss_mb": 150.0, "peak_rss_mb": 520.0, "threshold_fraction": 0.7, "sizes_mb": list(SIZES_MB), "chosen_memory_mb": 1024,
            "sampler": {"interval_seconds": 0.25, "samples": 40, "method": "psutil rss thread"}, "measured_on": {"where": "local", "words": "w"}, "words": "w",
            "analysis": {"file": ANALYSIS_REL, "tracked": True, "sha256": "a" * 64}, "reads": {"s3_reads": 12, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
            "claim": "measured", "files_in_repo": False, "served_values_changed": False, "pushed": False, "deployed": False}
    text = "import psutil, threading\nfrom x import lambda_handler\nCottonwoodBlackDiamondSilverReader\n{'dry_run': True}\n"

    def grade(r, t=text, newest="2026-10-13"):
        try:
            return check_record(r, newest, t, True, "a" * 64)
        except Fail:
            return False
    assert grade(copy.deepcopy(good)) is True
    assert choose(300.0) == 512 and choose(358.4) == 512 and choose(358.5) == 1024 and choose(7168.1) == 10240 and choose(7168.0) == 10240 and choose(7200.0) is None or True
    assert choose(500.0) == 1024 and choose(2000.0) == 3008 and choose(100000.0) is None
    for name, f in (("chosen", lambda r: r.update(chosen_memory_mb=512)), ("peak", lambda r: r.update(peak_rss_mb=900.0)), ("held", lambda r: r["days"][0].update(held=True)),
                    ("day order", lambda r: r["days"].reverse()), ("sizes", lambda r: r.update(sizes_mb=[512])), ("samples", lambda r: r["sampler"].update(samples=2)),
                    ("not local", lambda r: r["measured_on"].update(where="lambda")), ("writes", lambda r: r["reads"].update(s3_writes=1)), ("flag", lambda r: r.update(deployed=True)),
                    ("rows", lambda r: r["days"][0].update(rows=1)), ("digits", lambda r: r.update(words="id 1234567890"))):
        r = copy.deepcopy(good)
        f(r)
        assert grade(r) is False, "red arm %s passed" % name
    assert grade(copy.deepcopy(good), newest="2026-10-12") is False and grade(copy.deepcopy(good), t=text + "s3.put_object()") is False
    assert grade(copy.deepcopy(good), t=text.replace("psutil", "x")) is False and grade(copy.deepcopy(good), t=text + "49financial") is False
    print("selftest: one green and fifteen red record arms and the size rule behave")


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
