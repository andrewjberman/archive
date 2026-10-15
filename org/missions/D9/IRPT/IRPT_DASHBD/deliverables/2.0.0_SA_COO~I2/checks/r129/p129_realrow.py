"""IRPT_DASHBD round 129, workstream B-IN (issuer 2.0.0_SA_COO~I2) -- the first-real-row RUN script (cell DB-i-16).

The CTO (msg 8736, open call 5df4): build the run script NOW on fixtures so the first real run is a same-day act when the feed's
first silver lands. The script reads the feed's silver through the GET-only reader, feeds run() (the round-127 wrapper) into a
PRIVATE local directory, and prints counts: the Orion boundary measure (does startValue(t+1) equal endValue(t) where both exist),
and a chain check over a 238-to-365-day window. No S3 write, no vendor call. Every case below is SYNTHETIC.

  DBI129-1-AC1  run_real() on fixtures: the RAN record equals the wrapper's golden counts; no silver reads NO_SILVER_YET and writes
                nothing; a read cap reads STOPPED_AT_CAP and writes nothing; a non-empty output directory is refused.
  DBI129-1-AC2  the measures: boundary pairs / equal / max relative difference (bp) on a fixture with known answers; the chain
                check reads OK on a 299-day window and MISMATCH on an altered row, WINDOW_TOO_SHORT under 238 days.
  DBI129-1-AC3  the script holds no write, vendor or AWS-client token and no s3:// literal, reads only through the reader; the
                records carry only whitelisted keys with no date and no 8-digit run; its test file passes (at least 8) and names
                a mutant test.

NOTE (stated, not hidden): the chain check compares the table's chained rows with the product of the silver's own daily factors for
the same days (a consistency check of the adapter and wrapper on real rows). A comparison with Orion's REPORTED period return needs
a vendor call and a window the backfill provides, and is outside this script.

Usage: python -I <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python -I <this file> --selftest
"""
import ast
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/"
SCRIPT_REL = D + "0.9.0_WK_IRPT_DASHBD~316/run_scope_feed_real.py"
TEST_REL = D + "0.9.0_WK_IRPT_DASHBD~316/test_run_scope_feed_real.py"
FORBIDDEN_IMPORTS = {"boto3", "botocore", "requests", "urllib", "urllib3", "socket", "http", "ftplib", "smtplib"}
WRITE_TOKENS = ("put_object", "upload_file", "upload_fileobj", "delete_object", "copy_object", "put_item", "update_item", "invoke(",
                "start_execution", "Authorization", "orion_session_jwt", "requests.")
TOP_RAN = {"status", "contract_version", "partitions_read", "s3_reads", "calendar_days_read", "calendar_days_incomplete", "rows_present",
           "rows_absent", "absent_by_reason", "accounts_in_feed", "accounts_mapped", "accounts_unmapped", "trading_days_unaccounted",
           "market_value_eod_claim_counts", "boundary", "chain", "method_version_used", "out_dir_private"}
TOP_STOP = {"status", "partitions_listed", "s3_reads"}
FIRM = "FIRM-SYNTH"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


P124 = _load("p124_run", HERE.parent / "r124" / "p124_run.py")
P123 = P124.P123
silver_of, dim_of = P124.silver_of, P124.dim_of


class FakeReader:
    """A GET-only reader over synthetic frames: list_partitions / read_parquet / latest_partition, a read counter, nothing else."""

    def __init__(self, tables):
        self.tables = tables
        self.reads = 0

    def list_partitions(self, uri):
        self.reads += 1
        return sorted(self.tables.get(uri.rstrip("/").split("/")[-1], {}))

    def read_parquet(self, uri):
        self.reads += 1
        parts = uri.split("/")
        return self.tables[parts[-3]][parts[-2]]

    def latest_partition(self, uri):
        names = self.list_partitions(uri)
        return names[-1], self.read_parquet(uri.rstrip("/") + "/" + names[-1] + "/data.parquet")


def weekdays(lo, hi):
    import datetime as dt
    a, b = dt.date.fromisoformat(lo), dt.date.fromisoformat(hi)
    return [(a + dt.timedelta(days=i)).isoformat() for i in range((b - a).days + 1) if (a + dt.timedelta(days=i)).weekday() < 5]


def run_script(mod, reader, out, dim_ids, tdays_fn=weekdays, max_reads=400):
    return mod.run_real(reader, str(out), list(dim_ids), tdays_fn, FIRM, 0, max_reads)


def calendar_trading(lo, hi):
    return [t for t in P123.TRADING if lo <= t <= hi]


def grade_run(mod):
    dim_ids = sorted(P123.MAP)
    feed = silver_of(P123.feed())
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rec = run_script(mod, FakeReader({"scope_account_returns": feed}), out, dim_ids, tdays_fn=calendar_trading)
        need(rec.get("status") == "RAN", "status must read RAN: %r" % rec.get("status"))
        for k, v in (("partitions_read", 7), ("calendar_days_read", 7), ("calendar_days_incomplete", 0), ("rows_present", 17), ("rows_absent", 11),
                     ("accounts_in_feed", 7), ("accounts_mapped", 6), ("accounts_unmapped", 1), ("trading_days_unaccounted", 0)):
            need(rec.get(k) == v, "record %s: got %r want %r" % (k, rec.get(k), v))
        need(rec.get("market_value_eod_claim_counts") == {"inferred": 13, "measured": 4}, "claim counts")
        need(rec.get("method_version_used") == 0 and rec.get("out_dir_private") is True, "method_version_used / out_dir_private")
        need(isinstance(rec.get("s3_reads"), int) and rec["s3_reads"] == 8, "s3_reads must be 1 LIST + 7 GETs = 8: %r" % rec.get("s3_reads"))
        need(any(Path(out).glob("date=*")) and (Path(out) / "run_record.json").is_file(), "the wrapper did not write its partitions and run record")
        try:
            run_script(mod, FakeReader({"scope_account_returns": feed}), out, dim_ids, tdays_fn=calendar_trading)
        except ValueError:
            pass
        else:
            raise Fail("a non-empty output directory was not refused")
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rd = FakeReader({})
        rec = run_script(mod, rd, out, dim_ids)
        need(rec.get("status") == "NO_SILVER_YET" and set(rec) == TOP_STOP, "NO_SILVER_YET record: %r" % sorted(rec))
        need(rec.get("partitions_listed") == 0 and rec.get("s3_reads") == 1, "NO_SILVER_YET reads: %r" % rec)
        need(not out.exists(), "NO_SILVER_YET wrote a directory")
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rd = FakeReader({"scope_account_returns": feed})
        rec = run_script(mod, rd, out, dim_ids, tdays_fn=calendar_trading, max_reads=5)
        need(rec.get("status") == "STOPPED_AT_CAP" and set(rec) == TOP_STOP, "STOPPED_AT_CAP record: %r" % sorted(rec))
        need(rec.get("partitions_listed") == 7 and rd.reads == 1, "a capped run must make only the LIST (reads %d)" % rd.reads)
        need(not out.exists(), "STOPPED_AT_CAP wrote a directory")


def boundary_world():
    """One account, three calendar days: end(d1) = start(d2) (equal), end(d2) = 1.01 x start(d3) (100 bp)."""
    rows = [P123.ret("3001", "2026-07-06", 1.001, 100.0, 101.0), P123.ret("3001", "2026-07-07", 1.002, 101.0, 202.0),
            P123.ret("3001", "2026-07-08", 1.003, 200.0, None)]
    return silver_of(rows)


def grade_measures(mod):
    pairs, equal, bp = mod.measure_boundary(boundary_world())
    need(pairs == 2 and equal == 1 and bp is not None and abs(bp - 100.0) <= 0.01, "boundary measure: got %r want (2, 1, 100.0)" % ((pairs, equal, bp),))
    pairs0, equal0, bp0 = mod.measure_boundary(silver_of(P123.feed()))
    need(pairs0 == 0 and equal0 == 0 and bp0 is None, "a feed with no end values has 0 pairs and bp None: %r" % ((pairs0, equal0, bp0),))
    rows, trading, _product = P124.chain_world()
    silver = silver_of(rows)
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "out"
        rec = mod.run_real(FakeReader({"scope_account_returns": silver}), str(out), ["2001"], weekdays, FIRM, 0, 400)
        ch = rec.get("chain") or {}
        need(ch.get("status") == "OK" and ch.get("window_calendar_days") == 299 and ch.get("accounts_checked") == 1 and ch.get("accounts_matching") == 1,
             "299-day chain: %r" % ch)
        need(ch.get("max_abs_diff_bp") is not None and ch["max_abs_diff_bp"] <= 1e-6, "299-day chain max diff: %r" % ch.get("max_abs_diff_bp"))
        table_rows = []
        import pyarrow.parquet as pq
        for p in sorted(Path(out).glob("date=*")):
            table_rows.extend(pq.read_table(str(p / "data.parquet")).to_pylist())
        res = mod.chain_check(table_rows, silver, trading, rows[0]["day"], rows[-1]["day"])
        need(res["status"] == "OK", "chain_check on the unaltered rows must read OK: %r" % res)
        bad = [dict(r) for r in table_rows]
        bad[10]["total_return_daily"] = bad[10]["total_return_daily"] + 0.001
        res = mod.chain_check(bad, silver, trading, rows[0]["day"], rows[-1]["day"])
        need(res["status"] == "MISMATCH" and res["accounts_matching"] == 0, "an altered row must read MISMATCH: %r" % res)
    feed = silver_of(P123.feed())
    with tempfile.TemporaryDirectory() as td:
        rec = run_script(mod, FakeReader({"scope_account_returns": feed}), Path(td) / "out", sorted(P123.MAP), tdays_fn=calendar_trading)
        need((rec.get("chain") or {}).get("status") == "WINDOW_TOO_SHORT", "a 7-day window must read WINDOW_TOO_SHORT: %r" % rec.get("chain"))
        need(rec["boundary"] == {"pairs": 0, "pairs_equal": 0, "max_rel_diff_bp": None}, "boundary record on the feed fixture: %r" % rec["boundary"])


def grade_static(mod, root):
    sp = Path(root) / SCRIPT_REL
    src = sp.read_bytes().decode("ascii")
    tree = ast.parse(src)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    need(not (names & FORBIDDEN_IMPORTS), "forbidden import(s): %s" % sorted(names & FORBIDDEN_IMPORTS))
    for t in WRITE_TOKENS:
        need(t not in src, "script holds a write, vendor or client token: %s" % t)
    need("s3://" not in src, "script names an s3:// address")
    need("InflectionSilverReader" in src, "the script must build its reader from InflectionSilverReader")
    need(hasattr(mod, "main") and hasattr(mod, "run_real") and hasattr(mod, "measure_boundary") and hasattr(mod, "chain_check"), "missing main / run_real / measure_boundary / chain_check")
    dim_ids = sorted(P123.MAP)
    with tempfile.TemporaryDirectory() as td:
        rec = run_script(mod, FakeReader({"scope_account_returns": silver_of(P123.feed())}), Path(td) / "out", dim_ids, tdays_fn=calendar_trading)
        need(set(rec) == TOP_RAN, "RAN record keys differ from the whitelist: %s" % sorted(set(rec) ^ TOP_RAN))
        text = json.dumps(rec)
        need(re.search(r"\d{8,}", text) is None, "an 8-digit run in the record")
        need(re.search(r"\d{4}-\d{2}-\d{2}", text) is None and "date=" not in text, "a date in the record")
    tf = Path(root) / TEST_REL
    need(tf.is_file(), "no test file at %s" % TEST_REL)
    tsrc = tf.read_bytes().decode("ascii")
    need(re.search(r"^def test_\w*mutant\w*\(", tsrc, re.M) is not None, "no test named test_*mutant*")
    r = subprocess.run([sys.executable, "-I", "-m", "pytest", "-q", "-p", "no:cacheprovider", str(tf)], cwd=str(root), capture_output=True, text=True, timeout=100)
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    need(r.returncode == 0, "pytest rc %s: %s" % (r.returncode, tail[0]))
    m = re.search(r"(\d+) passed", r.stdout or "")
    need(m is not None and int(m.group(1)) >= 8, "fewer than 8 passed tests: %s" % tail[0])


def selftest():
    w = boundary_world()
    need(len(w) == 3, "boundary_world drifted")
    r = FakeReader({"scope_account_returns": silver_of(P123.feed())})
    need(r.list_partitions("s3://x/orion/inflection/silver/scope_account_returns") == sorted(silver_of(P123.feed())) and r.reads == 1, "FakeReader drifted")
    need(len(weekdays("2026-07-02", "2026-07-08")) == 5, "weekdays drifted")
    print("selftest PASS")


def main(argv):
    if len(argv) >= 2 and argv[1] == "--selftest":
        try:
            selftest()
        except Fail as exc:
            print("REASON: %s" % exc)
            print("selftest FAIL")
            return 1
        return 0
    root, cid = Path(argv[1]).resolve(), argv[2]
    try:
        sp = root / SCRIPT_REL
        need(sp.is_file(), "no script at %s" % SCRIPT_REL)
        mod = _load("run_scope_feed_real_under_test", sp)
        if cid == "DBI129-1-AC1":
            grade_run(mod)
        elif cid == "DBI129-1-AC2":
            grade_measures(mod)
        elif cid == "DBI129-1-AC3":
            grade_static(mod, root)
        else:
            raise Fail("unknown criterion %s" % cid)
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
