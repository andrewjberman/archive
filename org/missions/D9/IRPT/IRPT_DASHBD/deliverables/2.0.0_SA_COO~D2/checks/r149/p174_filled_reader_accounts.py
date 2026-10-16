"""IRPT_DASHBD round 149, workstream FILLEDRD2 (issuer 2.0.0_SA_COO~D2) -- DB-b-306, the hop-2 READER re-cut (row IRPT_DASHBD-D2-S128): the reader drained in DB-b-302 maps a client to a household through the
directory's relationship id hashed with sha256, which matches NONE of the 4,012 households of the real filled_report_values partition. The measured join is through the ACCOUNTS: the table's `account.last4` rows
carry RAW custodial account ids as `row_key`, the directory's `ids.account_ids` are the MINTED opaque ids, and the handler's own `ids.opaque_account(firm, raw)` turns the first into the second (all 6,616 table
accounts match; 4,012 clients reach exactly one household, 764 none, none two). The partition holds millions of rows, so the reader indexes it ONCE per partition (cached by the object's ETag), never per client.

  DB174-1-AC1  the diff: handler.py differs from the base only inside the reader and its private helpers (first FILLED-REPORT-A block); publisher.py and locals.tf are byte-identical to the base
  DB174-1-AC2  the behaviour: the account join (one household composed, none NotYetAvailable, two PublishRefused, raw ids never match), one fetch of the partition across a pass, a rewritten partition is re-read, speed
  DB174-1-AC3  the tests: at least six NEW tests carry `accounts` in their name, the relationship-id rule is gone from the reader, and both filled-report test files pass

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>      green on a reference tree, red on single-fault mutants of its handler
"""
import hashlib
import importlib.util
import io
import re
import subprocess
import sys
import time
from pathlib import Path

BASE = "787619fad2"  # resolved to the full commit by git; the tree after DB-b-302, DB-b-305 and the re-pin
LAMBDA = "infra/aws/lambda/investor-reporting/reporting-publish/"
HANDLER = LAMBDA + "handler.py"
PUBLISHER = LAMBDA + "publisher.py"
LOCALS = "infra/aws/terraform/investor-reporting/reporting-publish/locals.tf"
T_PUBLISH = LAMBDA + "tests/test_filled_report_publish.py"
T_READER = LAMBDA + "tests/test_filled_report_reader.py"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/filled_report_values.py"
BEGIN, END = "# BEGIN FILLED-REPORT-A", "# END FILLED-REPORT-A"
FIRM = "49financial"
TABLE = "filled_report_values"
HERE = Path(__file__).resolve().parent


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git_show(root, rel):
    r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (BASE, rel)], capture_output=True)
    need(r.returncode == 0, "cannot read %s at the base %s" % (rel, BASE))
    return r.stdout


def rd(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return p.read_bytes()


def cut_block(text, index=0):
    starts = [m.start() for m in re.finditer(re.escape(BEGIN), text)]
    ends = [m.start() for m in re.finditer(re.escape(END), text)]
    need(len(starts) == len(ends) and len(starts) > index and all(s < e for s, e in zip(starts, ends)), "the FILLED-REPORT-A block markers are missing or out of order")
    i, j = starts[index], ends[index]
    return text[:i] + text[j:], text[i:j]


def func_span(text, name):
    m = re.search(r"^def %s\(.*?(?=^def |^class |^# END FILLED-REPORT-A|\Z)" % re.escape(name), text, flags=re.S | re.M)
    need(m, "no def %s" % name)
    return m.group(0)


# ------------------------------------------------------------------------------------------------ AC1
def check_diff(root):
    new_h, old_h = rd(root, HANDLER).decode("utf-8"), git_show(root, HANDLER).decode("utf-8")
    need("\r" not in new_h, "handler.py must keep LF line endings")
    need(new_h.count(BEGIN) == old_h.count(BEGIN) == 2 and new_h.count(END) == old_h.count(END) == 2, "the two FILLED-REPORT-A blocks must both remain")
    out_new, in_new = cut_block(new_h, 0)
    out_old, in_old = cut_block(old_h, 0)
    need(out_new == out_old, "handler.py differs from the base outside the first FILLED-REPORT-A block")
    for head in ("filled_report_enabled", "run_filled_report", "filled_report_fire"):
        need(func_span(in_new, head) == func_span(in_old, head), "%s must be byte-identical to the base" % head)
    for name in ("FILLED_REPORT_SWITCH = ", "class NotYetAvailable(Exception):", "def read_filled_report_gold("):
        need(name in in_new, "the block must still define %s" % name.split("(")[0].split(" =")[0])
    need(func_span(in_new, "read_filled_report_gold") != func_span(in_old, "read_filled_report_gold"), "read_filled_report_gold is unchanged")
    for rel in (PUBLISHER, LOCALS):
        need(rd(root, rel) == git_show(root, rel), "%s must be byte-identical to the base" % rel.rsplit("/", 1)[-1])
    return True


# ------------------------------------------------------------------------------------------------ AC2
def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def doc_of(ref, accounts, points=3):
    ws = {w: "MEASURED" for w in ("qtd", "ytd", "last_12_months", "since_inception")}
    return {"household": {"household_ref": ref, "as_of": "2026-10-15", "first_data_date": "2024-01-02",
                          "accounts": [{"account_id": a, "last4": "0001", "first_data_date": "2024-01-02", "window_status": dict(ws)} for a in accounts]},
            "values": {"pvs.ytd.total_return": 1.5, "label.household": "Synthetic", "hold.allocation": {"by_row": {"equity": 42.0, "bonds": {"absent": "none held", "kind": "NO_SOURCE_YET"}}},
                       "chart.growth": [{"name": "S", "points": [{"date": "2026-%02d-%02d" % (1 + i // 28, 1 + i % 28), "value": 100.0 + i} for i in range(points)]}]}}


class FakeS3(object):
    """GET and LIST only (pages of three); the listing of a key carries its ETag; every get is recorded."""
    def __init__(self, objects):
        self.objects, self.gets, self.lists = dict(objects), [], 0

    def list_objects_v2(self, Bucket, Prefix="", Delimiter=None, ContinuationToken=None, **kw):
        self.lists += 1
        keys = sorted(k for (b, k) in self.objects if b == Bucket and k.startswith(Prefix))
        if Delimiter:
            seen, items = set(), []
            for k in keys:
                rest = k[len(Prefix):]
                if Delimiter in rest:
                    cp = Prefix + rest.split(Delimiter)[0] + Delimiter
                    if cp not in seen:
                        seen.add(cp)
                        items.append(("P", cp))
                else:
                    items.append(("K", k))
        else:
            items = [("K", k) for k in keys]
        start = int(ContinuationToken or 0)
        page = items[start:start + 3]
        out = {"IsTruncated": start + 3 < len(items), "KeyCount": len(page)}
        if out["IsTruncated"]:
            out["NextContinuationToken"] = str(start + 3)
        out["CommonPrefixes"] = [{"Prefix": v} for t, v in page if t == "P"]
        out["Contents"] = [{"Key": v, "Size": len(self.objects[(Bucket, v)]), "ETag": '"%s"' % hashlib.md5(self.objects[(Bucket, v)]).hexdigest()} for t, v in page if t == "K"]
        return out

    def get_object(self, Bucket, Key, **kw):
        if (Bucket, Key) not in self.objects:
            raise KeyError("NoSuchKey " + Key)
        self.gets.append(Key)
        return {"Body": io.BytesIO(self.objects[(Bucket, Key)])}

    def get_paginator(self, name):
        s3 = self

        class P(object):
            def paginate(self, **kw):
                tok = None
                while True:
                    r = s3.list_objects_v2(ContinuationToken=tok, **kw)
                    yield r
                    if not r.get("IsTruncated"):
                        return
                    tok = r["NextContinuationToken"]
        return P()

    def put_object(self, *a, **k):
        raise AssertionError("the reader wrote an object")

    def __getattr__(self, name):
        raise AssertionError("the reader called s3.%s; only list_objects_v2, get_paginator and get_object are allowed" % name)


def parquet_bytes(frv, rows):
    import pyarrow as pa
    import pyarrow.parquet as pq
    schema = pa.schema([(c, pa.float64() if c == "value_number" else pa.string()) for c in frv.COLUMNS])
    tbl = pa.Table.from_pydict({c: [r[c] for r in rows] for c in frv.COLUMNS}, schema=schema)
    buf = io.BytesIO()
    pq.write_table(tbl, buf, row_group_size=50000)
    return buf.getvalue()


def check_behaviour(root):
    root = Path(root)
    sys.path[:0] = [str(root / LAMBDA.rstrip("/")), str(root)]
    for m in ("handler", "publisher"):
        sys.modules.pop(m, None)
    import handler as h  # noqa: E402
    import publisher as p  # noqa: E402
    from lib import opal_naming  # noqa: E402
    frv = load_mod(root / PRODUCER, "frv_ref_174")
    ids = h._ids_module()
    mint = lambda raw: ids.opaque_account(FIRM, raw)  # noqa: E731
    probe = str(opal_naming.address("irpt", FIRM, "gold", TABLE, "date=0000-00-00", "data.parquet"))
    bucket, _, key = probe[len("s3://"):].partition("/")
    base_key = key.rsplit("/date=", 1)[0]
    day_key = lambda d: "%s/date=%s/data.parquet" % (base_key, d)  # noqa: E731
    d1, d2, d3 = doc_of("hh1", ["RAWACC001A", "RAWACC002B"]), doc_of("hh2", ["RAWACC003C"]), doc_of("hh3", ["RAWACC004D"])
    rows = []
    for ref, doc in (("hh1", d1), ("hh2", d2), ("hh3", d3)):
        rows += frv.to_rows(doc, ref, FIRM, "2026-10-15", "0.5.4")
    old_rows = frv.to_rows(doc_of("hh1", ["RAWACC001A", "RAWACC002B"], points=2), "hh1", FIRM, "2026-10-14", "0.5.4")
    directory = {"entries": [
        {"ids": {"client_id": "cli_1", "account_ids": [mint("RAWACC001A"), mint("RAWACC002B")]}},
        {"ids": {"client_id": "cli_2", "account_ids": [mint("RAWACC003C")]}},
        {"ids": {"client_id": "cli_two", "account_ids": [mint("RAWACC001A"), mint("RAWACC003C")]}},
        {"ids": {"client_id": "cli_none", "account_ids": [mint("RAWACC999Z")]}},
        {"ids": {"client_id": "cli_noacc"}},
        {"ids": {"client_id": "cli_raw", "account_ids": ["RAWACC003C"]}}]}
    read = lambda s3, cid, dr=directory: h.read_filled_report_gold(FIRM, cid, s3=s3, directory=dr)  # noqa: E731

    def store(extra=None):
        objs = {(bucket, day_key("2026-10-14")): parquet_bytes(frv, old_rows), (bucket, day_key("2026-10-15")): parquet_bytes(frv, rows)}
        objs.update(extra or {})
        return FakeS3(objs)
    s3 = store()
    got = read(s3, "cli_1")
    need(got == d1, "present: the document of the client's household (two accounts, one household) differs from the contract document")
    p.validate_filled_report(got)
    need(read(s3, "cli_2") == d2, "present: the second client's household differs")
    need(s3.gets.count(day_key("2026-10-15")) == 1 and day_key("2026-10-14") not in s3.gets, "one pass must fetch the newest partition's data.parquet ONCE and the older one never; fetched %s" % [k.rsplit("/", 2)[-2] for k in s3.gets])
    for cid, label in (("cli_none", "accounts that match no household"), ("cli_noacc", "a client with no account ids"), ("cli_nobody", "a client not in the directory"), ("cli_raw", "directory ids equal to the RAW table ids (no minting is a join of nothing)")):
        try:
            read(store(), cid)
        except h.NotYetAvailable:
            continue
        except Exception as exc:  # noqa: BLE001
            raise Fail("%s: raised %s, not NotYetAvailable" % (label, type(exc).__name__))
        raise Fail("%s: returned a document; it must raise NotYetAvailable" % label)
    try:
        read(store(), "cli_two")
    except p.PublishRefused:
        pass
    except Exception as exc:  # noqa: BLE001
        raise Fail("two households: raised %s, not PublishRefused" % type(exc).__name__)
    else:
        raise Fail("two households: a client whose accounts span two households returned a document; households are never merged")
    try:
        read(FakeS3({}), "cli_1")
    except h.NotYetAvailable:
        pass
    else:
        raise Fail("no partition: must raise NotYetAvailable")
    # a partition rewritten under the same key is re-read (the cache is keyed by the object's ETag)
    d1b = doc_of("hh1", ["RAWACC001A", "RAWACC002B"], points=5)
    rows_b = frv.to_rows(d1b, "hh1", FIRM, "2026-10-15", "0.5.4")
    s3.objects[(bucket, day_key("2026-10-15"))] = parquet_bytes(frv, rows_b)
    need(read(s3, "cli_1") == d1b, "a partition rewritten under the same key must be re-read (cache keyed by ETag)")
    # speed: 400 households of about 500 rows each (200 thousand rows), one client each; a per-client scan cannot finish
    big_rows, big_dir = [], []
    for i in range(400):
        raw = "BIGACC%05d" % i
        big_rows += frv.to_rows(doc_of("bh%04d" % i, [raw], points=480), "bh%04d" % i, FIRM, "2026-10-15", "0.5.4")
        big_dir.append({"ids": {"client_id": "big_%04d" % i, "account_ids": [mint(raw)]}})
    big = FakeS3({(bucket, day_key("2026-10-15")): parquet_bytes(frv, big_rows)})
    bd = {"entries": big_dir}
    t0 = time.time()
    first = h.read_filled_report_gold(FIRM, "big_0000", s3=big, directory=bd)
    for i in range(1, 400):
        h.read_filled_report_gold(FIRM, "big_%04d" % i, s3=big, directory=bd)
    elapsed = time.time() - t0
    need(first["household"]["household_ref"] == "bh0000" and big.gets.count(day_key("2026-10-15")) == 1, "the big pass must fetch the partition once and return the right household")
    need(elapsed < 25, "400 clients over %d rows took %.1f s; the partition must be indexed once per pass, not scanned per client (limit 25 s)" % (len(big_rows), elapsed))
    # the pass wiring
    puts = {}
    s3p = store()
    out = h.run_filled_report(FIRM, ["cli_1", "cli_two", "cli_none"], lambda a, b: puts.__setitem__(a, b), reader=lambda f, c: read(s3p, c), environ={"FILLED_REPORT_PASS": "1"})
    need(out["written"] == 1 and out["refused"] == ["cli_two"] and out["not_available"] == ["cli_none"], "the pass: one written, the two-household client refused, the unmatched client not available: %s" % out)
    return True


# ------------------------------------------------------------------------------------------------ AC3
def check_tests(root):
    root = Path(root)
    new = set()
    for rel in (T_PUBLISH, T_READER):
        txt = rd(root, rel).decode("utf-8")
        try:
            base_txt = git_show(root, rel).decode("utf-8")
        except Fail:
            base_txt = ""
        new |= set(re.findall(r"^def (test_\w+)\(", txt, flags=re.M)) - set(re.findall(r"^def (test_\w+)\(", base_txt, flags=re.M))
    need(len([n for n in new if "accounts" in n]) >= 6, "at least six NEW tests carry accounts in their name, found %s" % sorted(new))
    reader = func_span(cut_block(rd(root, HANDLER).decode("utf-8"), 0)[1], "read_filled_report_gold")
    need("relationship" not in reader and "sha256" not in reader, "the relationship-id and sha256 rule must be gone from the reader")
    helper_text = cut_block(rd(root, HANDLER).decode("utf-8"), 0)[1]
    need("read_dictionary" in helper_text, "the partition must be read with pq.read_table(..., read_dictionary=[its string columns]) so 4.7 million rows stay near 300 MB, not a gigabyte")
    need("opaque_account" in reader or "_ids_module" in cut_block(rd(root, HANDLER).decode("utf-8"), 0)[1], "the reader must mint the table's raw account ids with the handler's own ids.opaque_account")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "--color=no", str(root / T_PUBLISH), str(root / T_READER)], capture_output=True, text=True, cwd=str(root))
    need(r.returncode == 0, "pytest failed: %s" % (r.stdout + r.stderr)[-400:].replace("\n", " | "))
    need(re.search(r"\d+ passed", r.stdout) is not None, "pytest printed no pass count")
    return True


CHECKS = {"DB174-1-AC1": check_diff, "DB174-1-AC2": check_behaviour, "DB174-1-AC3": check_tests}


def selftest(ref_root):
    ref = Path(ref_root)
    for fn in CHECKS.values():
        fn(ref)
    handler = ref / HANDLER
    original = handler.read_bytes()
    txt = original.decode("utf-8")
    muts = {
        "the minting is skipped": ("acct.setdefault(ids.opaque_account(firm, raw), set())", "acct.setdefault(raw, set())"),
        "two households are merged": ("raise publisher.PublishRefused(\"the client's accounts span more than one household", "pass  # \""),
        "the partition is re-read per client": ("_FILLED_CACHE[\"entry\"] = entry", "_FILLED_CACHE.clear()"),
        "no partition returns an empty document": ("raise NotYetAvailable(\"the filled-report gold table holds no partition yet\")", "return {}"),
    }
    n = 0
    try:
        for label, (a, b) in muts.items():
            need(a in txt, "selftest: the reference lacks the anchor for '%s'" % label)
            handler.write_bytes(txt.replace(a, b, 1).encode("utf-8"))
            try:
                check_behaviour(ref)
            except (Fail, AssertionError, Exception):  # noqa: BLE001
                n += 1
                continue
            raise AssertionError("mutant passed: " + label)
        handler.write_bytes(txt.replace("def lambda_handler(event, context=None):", "def lambda_handler(event, context=None):  # touched", 1).encode("utf-8"))
        try:
            check_diff(ref)
        except Fail:
            n += 1
        else:
            raise AssertionError("diff mutant passed")
    finally:
        handler.write_bytes(original)
    print("selftest: green on the reference and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2])
        sys.exit(0)
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DB174-1-AC1": "OK: handler.py differs from the base only inside the reader and its helpers (the switch, the pass and the event branch stay byte for byte); publisher.py and locals.tf are byte-identical to the base",
               "DB174-1-AC2": "OK: the reader joins through the minted account ids (one household composed, none or no accounts NotYetAvailable, two households PublishRefused, raw ids never match), fetches the partition once per pass, re-reads a rewritten partition, and serves 400 clients over 200 thousand rows well inside the limit",
               "DB174-1-AC3": "OK: six or more new accounts tests exist, the relationship-id rule is gone from the reader, it mints with the handler's own ids.opaque_account, and both filled-report test files pass"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
