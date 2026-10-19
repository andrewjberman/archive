"""IRPT_DASHBD round 132, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the LIVE read cell, Inflection only (cell DB-i-19).

CTO round-131 analysis (msg 8916, erratum @b81e9bc3c4): after the IB-pr-596 first scheduled fire, ONE live read cell: the live
silver and the wrapper's output for the landed days, rows counted against the Scope feed's OWN manifest (the bronze envelope of
each day), trading days taken from lib/trading_calendar.py (never a local weekday helper). Inflection only, no second arm.

The worker runs the round-129 run script's run_real() on the landed silver into a PRIVATE directory (the real run), and reads each
landed day's bronze envelope through the GET-only reader for its manifest (universe_rows, households_failed, per-household
row_count, households_without_id). It saves a private extract; the repo record carries counts and verdict words only.

  DBI132-1-AC1  the record is complete and carries no identifier or date; the script is a tracked file hashed as recorded, with
                no write, vendor-call or secret token, built on InflectionSilverReader; the extract's hash equals the recorded
                one; run status RAN; every count equals the checker's recompute from the extract: per-day agreement of the
                silver row count with the bronze manifest, the trading-day count from lib/trading_calendar.py, accounts x
                trading days = rows_present + rows_absent, trading_days_unaccounted 0; no write, no push, no deploy.

The checker's self-test builds its extract from the feed's OWN writer (the feed's run() over its offline fakes), never by hand.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest [<repo_root>]
"""
import copy
import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT_DEFAULT = HERE.parents[8]
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
REC_REL = D + "0.9.0_WK_IRPT_DASHBD~319/SCOPE_LIVE_READ_R132.json"
MAX_S3_READS = 400
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "delete_object", "delete_objects", "copy_object", "put_item", "update_item",
                "create_multipart_upload", "put_parameter", "invoke(", "start_execution")
VENDOR_TOKENS = ("requests.", "urllib.request", "http.client", "orionadvisor", "Authorization", "orion_session_jwt")
RUN_KEYS = {"status", "contract_version", "partitions_read", "s3_reads", "calendar_days_read", "calendar_days_incomplete", "rows_present",
            "rows_absent", "absent_by_reason", "accounts_in_feed", "accounts_mapped", "accounts_unmapped", "trading_days_unaccounted",
            "market_value_eod_claim_counts", "boundary", "chain", "method_version_used", "out_dir_private"}
REC_KEYS = {"script", "extract", "run", "days_total", "days_manifest_agree", "days_manifest_disagree", "days_with_failed_households",
            "trading_days_in_window", "expected_rows", "rows_accounted", "verdict", "reads", "files_in_repo_private", "served_values_changed",
            "pushed", "deployed", "basis_words"}


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def trading_days_between(root, first, last):
    """The trading days from lib/trading_calendar.py of the repository under test (never a local helper)."""
    sys.path.insert(0, str(root))
    from lib import trading_calendar as tc
    return [d.isoformat() for d in tc.trading_days_between(first, last)]


def recompute(extract, root):
    days = extract["days"]
    need(days, "the extract holds no day")
    names = sorted(days)
    agree = disagree = failed = 0
    for d in names:
        e = days[d]
        ok = e["silver_rows"] == sum(e["call_row_counts"]) and e["households_failed"] == 0 and e["universe_rows"] >= e["silver_rows"]
        agree += bool(ok)
        disagree += not ok
        failed += e["households_failed"] > 0
    tdays = trading_days_between(root, names[0], names[-1])
    return {"days_total": len(names), "days_manifest_agree": agree, "days_manifest_disagree": disagree, "days_with_failed_households": failed,
            "trading_days_in_window": len(tdays)}


def no_identifiers(rec):
    """No run of 8 or more digits, except in a sha256 value or a path or file field; no ISO date anywhere."""
    rec = json.loads(json.dumps(rec))
    for outer, inner in (("extract", "path"), ("script", "file")):
        if isinstance(rec.get(outer), dict) and inner in rec[outer]:
            rec[outer][inner] = ""
    text = re.sub(r"[0-9a-f]{64}", "", json.dumps(rec))
    for m in re.finditer(r"\d{8,}", text):
        need(False, "a run of 8 or more digits in the record: %s" % m.group(0)[:3])
    need(re.search(r"\d{4}-\d{2}-\d{2}", text) is None, "a date is in the record")
    need("date=" not in text, "a partition name is in the record")


def script_clean(root, rel, want_sha):
    p = Path(root) / rel
    need(p.is_file(), "script %s is not a tracked file" % rel)
    b = p.read_bytes()
    need(sha(b) == want_sha, "script hash differs from the record")
    src = b.decode("ascii")
    for t in WRITE_TOKENS:
        need(t not in src, "script holds a write or invoke token: %s" % t)
    for t in VENDOR_TOKENS:
        need(t not in src, "script holds a vendor-call token: %s" % t)
    need("InflectionSilverReader" in src, "script must read through InflectionSilverReader (GET-only, granted prefixes)")
    need("trading_calendar" in src, "script must take trading days from lib/trading_calendar.py")
    need("def weekdays" not in src, "script defines its own weekdays helper")


def check(root, rec_rel=REC_REL, calendar_root=None):
    root = Path(root)
    calendar_root = Path(calendar_root) if calendar_root else root
    rec = json.loads((root / rec_rel).read_bytes().decode("ascii"))
    need(set(rec) == REC_KEYS, "record keys differ from the whitelist: %s" % sorted(set(rec) ^ REC_KEYS))
    no_identifiers(rec)
    for k in ("served_values_changed", "pushed", "deployed", "files_in_repo_private"):
        need(rec.get(k) is False, "%s must be false" % k)
    r = rec["reads"]
    need(set(r) == {"s3_reads", "s3_writes", "dynamodb_writes", "vendor_calls", "secret_reads"}, "reads keys")
    for k in ("s3_writes", "dynamodb_writes", "vendor_calls", "secret_reads"):
        need(r[k] == 0, "reads.%s must be 0" % k)
    need(isinstance(r["s3_reads"], int) and 0 < r["s3_reads"] <= MAX_S3_READS, "reads.s3_reads must be 1..%d" % MAX_S3_READS)
    need(isinstance(rec["basis_words"], str) and len(rec["basis_words"]) >= 200, "basis_words (>= 200 characters) missing")
    script_clean(root, rec["script"]["file"], rec["script"]["sha256"])
    ex = rec["extract"]
    ep = Path(ex.get("path", ""))
    need(ep.is_file() and sha(ep.read_bytes()) == ex.get("sha256"), "the private extract is missing or its hash differs")
    extract = json.loads(ep.read_bytes().decode("utf-8"))
    run = rec["run"]
    need(set(run) == RUN_KEYS, "run record keys differ from the whitelist: %s" % sorted(set(run) ^ RUN_KEYS))
    need(run["status"] == "RAN", "the run did not run: status %r" % run["status"])
    want = recompute(extract, calendar_root)
    for k, v in want.items():
        need(rec[k] == v, "%s: record %r recount %r" % (k, rec[k], v))
    need(run["calendar_days_read"] == want["days_total"], "run.calendar_days_read differs from the extract's day count")
    expected = run["accounts_in_feed"] * want["trading_days_in_window"]
    need(rec["expected_rows"] == expected, "expected_rows: record %r recount %r" % (rec["expected_rows"], expected))
    accounted = run["rows_present"] + run["rows_absent"]
    need(rec["rows_accounted"] == accounted, "rows_accounted differs from rows_present + rows_absent")
    need(accounted == expected, "rows accounted (%d) differ from accounts x trading days (%d)" % (accounted, expected))
    need(run["trading_days_unaccounted"] == 0, "trading_days_unaccounted must be 0")
    verdict = "MANIFEST_AGREES" if want["days_manifest_disagree"] == 0 else "MANIFEST_DISAGREES"
    need(rec["verdict"] == verdict, "verdict: record %r recount %r" % (rec["verdict"], verdict))


# ---- self-test: the extract and run record come from the feed's OWN writer ------------------------------------------------
def build_good(root, td):
    """A GOOD record built from the feed's own run() (r131 helper) and the round-129 run script; returns (root_for_check, rel)."""
    p131 = _load("p131_feedwriter", HERE.parent / "r131" / "p131_feedwriter.py")
    p129 = p131.P129
    script_src = Path(root) / p129.SCRIPT_REL
    mod = _load("run_scope_feed_real_for_r132", script_src)
    silver = p131.feed_partitions(root)
    out = Path(td) / "out"
    run = mod.run_real(p129.FakeReader({"scope_account_returns": silver}), str(out), [str(a) for a in p131.ACCOUNTS], p131.weekdays, "FIRM-SYNTH", 0, 400)
    days = {}
    for name, frame in silver.items():
        d = name[len("date="):]
        days[d] = {"silver_rows": int(len(frame)), "universe_rows": int(len(frame)), "households_failed": 0,
                   "call_row_counts": [int(len(frame))], "households_without_id": 0}
    ex_path = Path(td) / "extract.json"
    ex_path.write_text(json.dumps({"days": days}))
    live = Path(td) / "repo"
    (live / D / "0.9.0_WK_IRPT_DASHBD~319").mkdir(parents=True)
    sp = live / D / "0.9.0_WK_IRPT_DASHBD~319" / "live_read.py"
    sp.write_bytes(b"from inflection_account_dim import InflectionSilverReader\nfrom lib import trading_calendar\nreader = InflectionSilverReader()\n")
    want = recompute({"days": days}, root)
    rec = {"script": {"file": sp.relative_to(live).as_posix(), "sha256": sha(sp.read_bytes())},
           "extract": {"path": str(ex_path), "sha256": sha(ex_path.read_bytes())}, "run": run, **want,
           "expected_rows": run["accounts_in_feed"] * want["trading_days_in_window"], "rows_accounted": run["rows_present"] + run["rows_absent"],
           "verdict": "MANIFEST_AGREES", "reads": {"s3_reads": 9, "s3_writes": 0, "dynamodb_writes": 0, "vendor_calls": 0, "secret_reads": 0},
           "files_in_repo_private": False, "served_values_changed": False, "pushed": False, "deployed": False, "basis_words": "w" * 220}
    rp = live / REC_REL
    rp.write_text(json.dumps(rec))
    return live, rec, ex_path, days


def selftest(root):
    root = Path(root).resolve()
    with tempfile.TemporaryDirectory() as td:
        live, rec, ex_path, days = build_good(root, td)
        sp_rel = rec["script"]["file"]

        def trial(label, mutate=None, extract_mutate=None, script_bytes=None, expect_fail=True):
            r = copy.deepcopy(rec)
            if mutate:
                mutate(r)
            if extract_mutate:
                e = {"days": copy.deepcopy(days)}
                extract_mutate(e)
                ex_path.write_text(json.dumps(e))
                r["extract"]["sha256"] = sha(ex_path.read_bytes())
            if script_bytes is not None:
                (live / sp_rel).write_bytes(script_bytes)
                r["script"]["sha256"] = sha(script_bytes)
            (live / REC_REL).write_text(json.dumps(r))
            try:
                check(live, calendar_root=root)
                got_fail = False
            except Fail as exc:
                got_fail = True
                why = str(exc)[:60]
            finally:
                ex_path.write_text(json.dumps({"days": days}))
                (live / sp_rel).write_bytes(b"from inflection_account_dim import InflectionSilverReader\nfrom lib import trading_calendar\nreader = InflectionSilverReader()\n")
            need(got_fail == expect_fail, "selftest %s: expected %s" % (label, "FAIL" if expect_fail else "PASS"))
            print("selftest %-34s -> %s" % (label, ("FAIL (%s)" % why) if got_fail else "PASS"))

        trial("GOOD", expect_fail=False)
        trial("wrong verdict", lambda r: r.update(verdict="MANIFEST_DISAGREES"))
        trial("wrong day count", lambda r: r.update(days_total=r["days_total"] + 1))
        trial("rows not accounted", lambda r: r["run"].update(rows_absent=r["run"]["rows_absent"] + 1))
        trial("trading days unaccounted", lambda r: r["run"].update(trading_days_unaccounted=1))
        trial("run not RAN", lambda r: r["run"].update(status="NO_SILVER_YET"))
        trial("s3 write read as zero", lambda r: r["reads"].update(s3_writes=1))
        trial("a date in the record", lambda r: r.update(basis_words=r["basis_words"] + " 2026-10-16"))
        trial("manifest disagrees in the extract", extract_mutate=lambda e: e["days"][sorted(e["days"])[0]].update(silver_rows=999))
        trial("script with a put_object", script_bytes=b"from inflection_account_dim import InflectionSilverReader\nfrom lib import trading_calendar\ns3.put_object()\n")
        trial("script with its own weekdays", script_bytes=b"from inflection_account_dim import InflectionSilverReader\nfrom lib import trading_calendar\ndef weekdays(a, b):\n    pass\n")
    print("selftest PASS")


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        try:
            selftest(argv[2] if len(argv) > 2 else ROOT_DEFAULT)
        except Fail as exc:
            print("REASON: %s" % exc)
            print("selftest FAIL")
            return 1
        return 0
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        need(cid == "DBI132-1-AC1", "unknown criterion %s" % cid)
        check(root)
    except FileNotFoundError as exc:
        print("REASON: no such file: %s" % Path(str(exc.filename)).name)
        print("%s FAIL" % cid)
        return 1
    except Fail as exc:
        print("REASON: %s" % exc)
        print("%s FAIL" % cid)
        return 1
    except Exception as exc:  # a crash is a FAIL with its type named, never a pass
        print("REASON: %s: %s" % (type(exc).__name__, str(exc)[:300]))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
