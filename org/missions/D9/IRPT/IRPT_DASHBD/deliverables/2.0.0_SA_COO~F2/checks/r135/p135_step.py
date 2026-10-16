"""IRPT_DASHBD round 135, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the INFLECTION TRANSACTION STEP for the Orion gold dispatch chain (CTO msgs 9486, 9625).

  DB-f-2102 (~2102) `data/inf/scripts/gold/INF_G_01.account_transaction_gold.py`, a thin LAUNCHER with a pinned, deterministic BUNDLE. Every Orion silver `fact_transactions`
                    partition is a CUMULATIVE SNAPSHOT of the whole history, so a run reads ONE snapshot (the newest partition not after the run day), derives the Reversed keys from
                    THAT snapshot, runs the Inflection producer, and emits the lines BY THEIR BUSINESS DATE; it never treats a partition as that day's transactions, and no source
                    line appears on more than one emitted day (counted over the full output). The chain syncs scripts FLAT by basename and the producer modules locate the repo by
                    `parents[5]`, so the producer closure ships as ONE zip in the repo layout, pinned by sha256 in the launcher, built deterministically from a committed manifest;
                    this checker runs the launcher from a flat directory with only the zip beside it.
                    DBF135-2-AC1 (the one-snapshot run, the no-repeat criterion, the S6 report), AC2 (the bundle: manifest, deterministic zip, pin, flat-directory runner simulation)

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

LAUNCHER = "data/inf/scripts/gold/INF_G_01.account_transaction_gold.py"
MANIFEST = "data/inf/scripts/gold/INF_G_01.bundle.json"
TESTS = "data/inf/scripts/gold/tests/test_INF_G_01_account_transaction_gold.py"
INF_PRODUCER_TESTS = "data/assets/scripts/gold/irpt_reporting/tests/test_account_transaction_inflection.py"
ADAPTER = "data/assets/scripts/gold/irpt_reporting/adapters/inflection_account_return_daily.py"
SYNC_DIRS = ("data/inf/scripts/gold", "data/inf/scripts/silver", "data/inf/scripts/bronze", "data/inf/manual_api")
GOLD_KEY = "irpt/inflection/gold/account_transaction/"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


# ---------------------------------------------------------------- a fake S3 (the calls the launcher and the producer's writer make)
class FakeS3:
    def __init__(self):
        self.store = {}
        self.gets = []
        self.puts = []

    def put_object(self, Bucket, Key, Body=b"", **kw):  # noqa: N803
        data = Body.read() if hasattr(Body, "read") else Body
        self.store[(Bucket, Key)] = data
        self.puts.append((Bucket, Key))
        return {"ETag": "x", "VersionId": "v"}

    def get_object(self, Bucket, Key, **kw):  # noqa: N803
        if (Bucket, Key) not in self.store:
            raise KeyError("NoSuchKey %s" % Key)
        self.gets.append((Bucket, Key))
        return {"Body": io.BytesIO(self.store[(Bucket, Key)])}

    def list_objects_v2(self, Bucket, Prefix="", Delimiter=None, **kw):  # noqa: N803
        keys = sorted(k for (b, k) in self.store if b == Bucket and k.startswith(Prefix))
        if Delimiter:
            prefixes = sorted({Prefix + k[len(Prefix):].split(Delimiter, 1)[0] + Delimiter for k in keys if Delimiter in k[len(Prefix):]})
            contents = [{"Key": k, "Size": len(self.store[(Bucket, k)])} for k in keys if Delimiter not in k[len(Prefix):]]
            return {"CommonPrefixes": [{"Prefix": p} for p in prefixes], "Contents": contents, "IsTruncated": False, "KeyCount": len(prefixes) + len(contents)}
        return {"Contents": [{"Key": k, "Size": len(self.store[(Bucket, k)])} for k in keys], "IsTruncated": False, "KeyCount": len(keys)}

    def head_object(self, Bucket, Key, **kw):  # noqa: N803
        if (Bucket, Key) not in self.store:
            raise KeyError("404")
        return {"ContentLength": len(self.store[(Bucket, Key)])}

    def get_paginator(self, name):
        outer = self

        class P:
            def paginate(self, **kw):
                yield outer.list_objects_v2(**kw)

        return P()


def line(i, day, status="Complete", desc="Buy Exchange", amount=100.0, units=4.0, ticker="TEST", acct=7000001):
    return {"id": i, "productName": "Test Product", "ticker": ticker, "accountId": acct, "custodianName": "Some Custodian", "status": status, "transDate": day,
            "transactionDescription": desc, "transAmount": amount, "navPrice": 25.0, "noUnits": units, "fundFamilyName": "Test Fund Family"}


def parquet_bytes(rows):
    import pandas as pd
    buf = io.BytesIO()
    pd.DataFrame(rows).to_parquet(buf, index=False)
    return buf.getvalue()


def put_snapshot(s3, bucket, prefix, day, rows):
    s3.store[(bucket, "%sdate=%s/part-0.parquet" % (prefix, day))] = parquet_bytes(rows)


def emitted_rows(s3):
    import pyarrow.parquet as pq
    out = []
    for (b, k), data in sorted(s3.store.items()):
        if GOLD_KEY in k and k.endswith("/data.parquet"):
            t = pq.read_table(io.BytesIO(data)).to_pandas()
            for r in t.to_dict("records"):
                out.append((k.split("date=")[1].split("/")[0], r))
    return out


def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_launcher(root):
    p = Path(root) / LAUNCHER
    need(p.is_file(), "missing " + LAUNCHER)
    spec = importlib.util.spec_from_file_location("INF_G_01_under_check", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sequence_problems(rows_by_day):
    """No source line appears on more than one emitted day, counted over the full output (CTO msg 9625). rows_by_day: [(day, row)]."""
    seen, pr = {}, []
    for day, r in rows_by_day:
        sid = r.get("source_txn_id")
        if sid in seen:
            pr.append("source line %s emitted on %s and on %s" % (sid, seen[sid], day))
        seen[sid] = day
    return pr


def ac1(root):
    L = load_launcher(root)
    for fn in ("newest_partition", "read_snapshot", "plan", "check_no_repeat", "emit", "run", "s6_report", "main", "bootstrap", "build_bundle"):
        need(callable(getattr(L, fn, None)), "the launcher has no %s" % fn)
    adapter = Path(root, ADAPTER).read_text(encoding="utf-8")
    need("orion" in adapter and getattr(L, "ORION_BUCKET", None) == "opal-data-assets" and getattr(L, "ORION_PREFIX", None) == "orion/inflection/silver/fact_transactions/",
         "ORION_BUCKET and ORION_PREFIX must be opal-data-assets and orion/inflection/silver/fact_transactions/ (the adapter's silver)")
    # two cumulative snapshots: S2 = S1 + new lines + a status change
    s3 = FakeS3()
    s1 = [line(1, "2026-10-12"), line(2, "2026-10-13", desc="Client Contribution", amount=500.0, units=0.0), line(3, "2026-10-13", status="Pending"),
          line(4, "2026-10-10")]
    s2 = [dict(r) for r in s1]
    s2[2] = line(3, "2026-10-13")
    s2 += [line(6, "2026-10-14"), line(7, "2026-10-14", status="Rejected"),
           line(8, "2026-10-09", status="Reversed", units=0.0, ticker="OFFX", amount=-5.0, desc="Foreign Dividend Tax"),
           line(9, "2026-10-09", units=0.0, ticker="OFFX", amount=5.0, desc="Foreign Dividend Tax")]
    put_snapshot(s3, L.ORION_BUCKET, L.ORION_PREFIX, "2026-10-14", s1)
    put_snapshot(s3, L.ORION_BUCKET, L.ORION_PREFIX, "2026-10-15", s2)
    need(L.newest_partition(s3, L.ORION_BUCKET, L.ORION_PREFIX, "2026-10-15") == "2026-10-15", "newest_partition must pick the newest partition not after the run day")
    need(L.newest_partition(s3, L.ORION_BUCKET, L.ORION_PREFIX, "2026-10-14") == "2026-10-14" and
         L.newest_partition(s3, L.ORION_BUCKET, L.ORION_PREFIX, "2026-12-31") == "2026-10-15", "newest_partition must pick the newest not after the run day")
    try:
        L.newest_partition(s3, L.ORION_BUCKET, L.ORION_PREFIX, "2026-10-01")
    except SystemExit as e:
        need("partition" in str(e).lower(), "the refusal for a run day before the first partition must name the partition: %s" % e)
    else:
        raise Fail("newest_partition accepted a run day before the first partition")
    # a full upload run: ONE snapshot is read, lines are emitted by their business date, no source line twice
    s3.gets.clear()
    summary = L.run(s3, "2026-10-15", upload=True)
    need(s3.gets and all("date=2026-10-15/" in k for _, k in s3.gets), "the run read a partition other than the newest: %s" % sorted({k for _, k in s3.gets})[:3])
    out = emitted_rows(s3)
    days = sorted({d for d, _ in out})
    need(days == ["2026-10-12", "2026-10-13", "2026-10-14"], "the lines must be emitted under their business dates (10-10 rolls to 10-12): %s" % days)
    ids = sorted(r["source_txn_id"] for _, r in out)
    need(ids == ["1", "2", "3", "4", "6"], "the emitted lines must be the Complete lines of the ONE snapshot, minus the offset of the Reversed original: %s" % ids)
    need(not sequence_problems(out), "; ".join(sequence_problems(out)))
    need(isinstance(summary, dict) and summary.get("snapshot") == "2026-10-15" and summary.get("rows_in") == len(s2) and summary.get("rows_out") == 5,
         "run must return {snapshot, rows_in, rows_out, ...}: %s" % (summary,))
    ex = summary.get("excluded") or {}
    need(ex.get("Rejected") == 1 and ex.get("Reversed") == 1 and ex.get("OFFSET_OF_REVERSED") == 1, "the summary must carry the excluded counts by status and the offset: %s" % (ex,))
    # the earlier snapshot, by the run day
    s3b = FakeS3()
    s3b.store.update(s3.store)
    for k in [k for k in s3b.store if GOLD_KEY in k[1]]:
        del s3b.store[k]
    L.run(s3b, "2026-10-14", upload=True)
    need(sorted(r["source_txn_id"] for _, r in emitted_rows(s3b)) == ["1", "2", "4"], "run day 2026-10-14 must emit the Complete lines of the 10-14 snapshot only")
    # since, dry run, the no-repeat guard
    s3c = FakeS3()
    s3c.store.update({k: v for k, v in s3.store.items() if GOLD_KEY not in k[1]})
    L.run(s3c, "2026-10-15", upload=True, since="2026-10-13")
    need(sorted({d for d, _ in emitted_rows(s3c)}) == ["2026-10-13", "2026-10-14"], "since must drop the business dates before it")
    s3d = FakeS3()
    s3d.store.update({k: v for k, v in s3.store.items() if GOLD_KEY not in k[1]})
    L.run(s3d, "2026-10-15", upload=False)
    need(not s3d.puts, "a dry run must make no put_object call")
    dup = {"2026-03-10": [{"source_txn_id": "A"}], "2026-03-11": [{"source_txn_id": "A"}]}
    try:
        L.check_no_repeat(dup)
    except SystemExit as e:
        need("repeat" in str(e).lower(), "the no-repeat refusal must say repeated: %s" % e)
    else:
        raise Fail("check_no_repeat accepted a source line on two emitted days")
    L.check_no_repeat({"2026-03-10": [{"source_txn_id": "A"}], "2026-03-11": [{"source_txn_id": "B"}]})
    # the S6 report: one equal-amount Buy or Income Reinvested line per event, printed N of M
    import pandas as pd
    ev = pd.DataFrame([line(21, "2026-10-12", desc="Dividend Paid from Cash", amount=-10.0, units=0.0, acct=7100001),
                       line(22, "2026-10-12", desc="Income Paid", amount=-10.0, units=0.0, acct=7100001),
                       line(23, "2026-10-12", desc="Buy Exchange", amount=10.0, acct=7100001),
                       line(24, "2026-10-12", desc="Dividend Paid from Cash", amount=-20.0, units=0.0, acct=7100002),
                       line(25, "2026-10-12", desc="Income Paid", amount=-20.0, units=0.0, acct=7100002)])
    rep = L.s6_report(ev)
    need(rep.get("events") == 2 and rep.get("with_equal_amount_line") == 1 and rep.get("missing") == 1,
         "s6_report must count the S6 events and those carrying an equal-amount Buy or Income Reinvested line: %s" % (rep,))
    need("1 of 2" in str(rep.get("printed", "")), "s6_report must print N of M ('1 of 2'): %s" % (rep,))
    # main: dry run through an injected client
    rc = L.main(["--date", "2026-10-15", "--dry-run"], s3=s3d)
    need(rc == 0, "main --dry-run must return 0")
    test_text = Path(root, TESTS).read_text(encoding="utf-8") if Path(root, TESTS).is_file() else ""
    names = [m.group(1) for m in re.finditer(r"^def (test_\w+)", test_text, re.M)]
    need(len(names) >= 30, "the launcher's test file must hold at least 30 tests (found %d)" % len(names))
    low = " | ".join(names).lower()
    for w in ("snapshot", "repeat", "business", "bundle", "reversed", "dry", "since", "s6"):
        need(w in low, "the launcher's test names lack %r" % w)
    run = subprocess.run([sys.executable, "-m", "pytest", TESTS, "-q", "-p", "no:cacheprovider"], cwd=str(root), capture_output=True, text=True, timeout=600)
    need(run.returncode == 0, "pytest %s failed: %s" % (TESTS, (run.stdout or "")[-300:]))
    run = subprocess.run([sys.executable, "-m", "pytest", INF_PRODUCER_TESTS, "-q", "-p", "no:cacheprovider"], cwd=str(root), capture_output=True, text=True, timeout=600)
    need(run.returncode == 0, "pytest %s failed (the contract moved to 0.5.1; the row-filter test must read the latest-snapshot record): %s" % (INF_PRODUCER_TESTS, (run.stdout or "")[-300:]))


def closure_problems(manifest, root):
    """The manifest lists every file of the bundle with its sha256 (equal to the repo file), sorted, no tests, and records the basename collisions with the chain's synced dirs."""
    pr = []
    files = manifest.get("files")
    if not (isinstance(files, list) and files and all(isinstance(f, dict) and "path" in f and "sha256" in f for f in files)):
        return ["the manifest must hold files: [{path, sha256}]"]
    paths = [f["path"] for f in files]
    if paths != sorted(paths):
        pr.append("manifest files must be sorted by path")
    for f in files:
        p = Path(root, f["path"])
        if not p.is_file():
            pr.append("manifest file missing: %s" % f["path"])
        elif sha256_file(p) != f["sha256"]:
            pr.append("manifest sha256 differs from the repo file: %s" % f["path"])
        if "/tests/" in f["path"] or Path(f["path"]).name.startswith("test_"):
            pr.append("a test file is in the bundle: %s" % f["path"])
    for need_path in ("data/assets/scripts/gold/irpt_reporting/account_transaction.py", "data/assets/scripts/gold/irpt_reporting/account_transaction_inflection.py",
                      "data/assets/scripts/gold/irpt_reporting/transaction_words.json", "lib/opal_naming.py", "lib/trading_calendar.py"):
        if need_path not in paths:
            pr.append("the bundle lacks %s" % need_path)
    synced = {}
    for d in SYNC_DIRS:
        for p in Path(root, d).glob("*"):
            if p.is_file():
                synced.setdefault(p.name, []).append(p)
    real = sorted(n for n in {Path(f["path"]).name for f in files} if n in synced)
    if manifest.get("basename_collisions_with_synced_dirs") != real:
        pr.append("manifest.basename_collisions_with_synced_dirs must be %r (the bundle is a zip, not synced flat, so a collision is recorded and harmless)" % (real,))
    return pr


def run_flat(root, launcher_text_path, zip_path, work):
    """The runner simulation: ONLY the launcher in a flat directory, the bundle zip named by an environment variable, a clean interpreter, a different cwd."""
    flat = Path(work, "flat")
    flat.mkdir()
    dest = flat / Path(LAUNCHER).name
    dest.write_bytes(Path(launcher_text_path).read_bytes())
    code = (
        "import importlib.util, json, sys\n"
        "spec = importlib.util.spec_from_file_location('L', sys.argv[1])\n"
        "L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)\n"
        "import pandas as pd\n"
        "frame = pd.DataFrame([{'id': 1, 'productName': 'P', 'ticker': 'T', 'accountId': 7, 'custodianName': 'C', 'status': 'Complete', 'transDate': '2026-03-14', "
        "'transactionDescription': 'Buy Exchange', 'transAmount': 100.0, 'navPrice': 25.0, 'noUnits': 4.0, 'fundFamilyName': 'F'}])\n"
        "by_day, excluded, reasons = L.plan(frame)\n"
        "print(json.dumps({'days': sorted(by_day), 'ids': [r['source_txn_id'] for rows in by_day.values() for r in rows]}))\n")
    env = dict(os.environ)
    env["INF_IRPT_BUNDLE_LOCAL"] = str(zip_path)
    env.pop("PYTHONPATH", None)
    run = subprocess.run([sys.executable, "-I", "-c", code, str(dest)], cwd=str(flat), env=env, capture_output=True, text=True, timeout=300)
    return run


def ac2(root):
    L = load_launcher(root)
    mpath = Path(root, MANIFEST)
    need(mpath.is_file(), "missing " + MANIFEST)
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    pr = closure_problems(manifest, root)
    need(not pr, "; ".join(pr[:5]))
    with tempfile.TemporaryDirectory() as td:
        z1, z2 = Path(td, "a.zip"), Path(td, "b.zip")
        h1 = L.build_bundle(str(root), str(z1))
        h2 = L.build_bundle(str(root), str(z2))
        need(h1 == h2 == sha256_file(z1) == sha256_file(z2), "build_bundle must be deterministic and return the zip's sha256")
        need(getattr(L, "EXPECTED_BUNDLE_SHA256", None) == h1, "EXPECTED_BUNDLE_SHA256 in the launcher (%s) must equal the built bundle's sha256 (%s)" % (getattr(L, "EXPECTED_BUNDLE_SHA256", None), h1))
        with zipfile.ZipFile(z1) as zf:
            names = sorted(zf.namelist())
            need(names == sorted(f["path"] for f in manifest["files"]), "the zip's members must be exactly the manifest's files in the repo layout")
            for f in manifest["files"]:
                need(hashlib.sha256(zf.read(f["path"])).hexdigest() == f["sha256"], "zip member differs from the manifest: %s" % f["path"])
        run = run_flat(root, Path(root, LAUNCHER), z1, td)
        need(run.returncode == 0, "the flat-directory runner simulation failed (rc %s): %s" % (run.returncode, ((run.stderr or "") + (run.stdout or ""))[-400:]))
        got = json.loads((run.stdout or "").strip().splitlines()[-1])
        need(got == {"days": ["2026-03-16"], "ids": ["1"]}, "the flat run must plan the Saturday line under Monday: %s" % (got,))
        # a bundle with a different hash is refused
        bad = Path(td, "bad.zip")
        bad.write_bytes(z1.read_bytes() + b"\0")
        os.makedirs(Path(td, "second"))
        run2 = run_flat(root, Path(root, LAUNCHER), bad, Path(td, "second"))
        need(run2.returncode != 0 and "sha256" in ((run2.stderr or "") + (run2.stdout or "")).lower(), "a bundle whose sha256 differs from the launcher's pin must be refused (naming sha256)")


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    s3 = FakeS3()
    s3.put_object("b", "x/date=2026-01-01/part.parquet", Body=b"1")
    s3.put_object("b", "x/date=2026-01-02/part.parquet", Body=b"2")
    r = s3.list_objects_v2("b", Prefix="x/", Delimiter="/")
    arm("fake-prefixes", [p["Prefix"] for p in r["CommonPrefixes"]], ["x/date=2026-01-01/", "x/date=2026-01-02/"])
    arm("fake-get", s3.get_object("b", "x/date=2026-01-01/part.parquet")["Body"].read(), b"1")
    pages = list(s3.get_paginator("list_objects_v2").paginate(Bucket="b", Prefix="x/"))
    arm("fake-paginate", len(pages[0]["Contents"]), 2)
    arm("sequence-green", sequence_problems([("d1", {"source_txn_id": "A"}), ("d2", {"source_txn_id": "B"})]), [])
    arm("sequence-red", len(sequence_problems([("d1", {"source_txn_id": "A"}), ("d2", {"source_txn_id": "A"})])), 1)
    arm("line-keys", sorted(line(1, "2026-03-10"))[:3], ["accountId", "custodianName", "fundFamilyName"])
    arm("parquet-roundtrip", len(parquet_bytes([line(1, "2026-03-10")])) > 100, True)
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "a.py").write_text("x", encoding="utf-8")
        m = {"files": [{"path": "a.py", "sha256": hashlib.sha256(b"x").hexdigest()}], "basename_collisions_with_synced_dirs": []}
        p = closure_problems(m, td)
        arm("closure-needs-the-modules", any("lacks" in x for x in p), True)
        arm("closure-hash", closure_problems({"files": [{"path": "a.py", "sha256": "0" * 64}]}, td)[0].startswith("manifest sha256 differs"), True)
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    table = {"DBF135-2-AC1": ac1, "DBF135-2-AC2": ac2}
    if ac not in table:
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        table[ac](root)
    except Fail as e:
        print("reason: %s" % e)
        print("%s FAIL" % ac)
        return 1
    except Exception as e:  # noqa: BLE001
        print("reason: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % ac)
        return 1
    print("%s PASS" % ac)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
