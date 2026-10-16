"""IRPT_DASHBD round 149, workstream FILLEDRD (issuer 2.0.0_SA_COO~D2) -- DB-b-302, the hop-2 READER of the 49 Financial publish function (CTO ruling msg 9439): reporting-publish/handler.py
`read_filled_report_gold(firm, client_id, s3=None, directory=None)` composes a client's filled report from the gold table filled_report_values; publisher.validate_filled_report accepts the contract's per-window window_status (row S123); and the publish role's read and list grant gains that one prefix
(reporting-publish/locals.tf). The filled-report switch stays OFF; nothing is deployed by this cell.

  DB170-1-AC1  the diff: handler.py and publisher.py change only inside their FILLED-REPORT-A block; locals.tf gains exactly the filled table local and its prefix in the read list; every other file of the root, publisher.py and the source map are byte-identical to the base
  DB170-1-AC2  the reader's behaviour over a fake S3 and a synthetic directory: present, absent (no partition, no rows, no relationship id, client not in the directory), refused, newest partition only, pagination, no write, the pass wiring
  DB170-1-AC3  the worker's tests: the stub test is gone, the new test file holds present, absent and refused tests, and both test files pass under pytest

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>      runs the criteria on a reference tree and on single-fault mutants of its handler
"""
import difflib
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "2cbe7bbcac43013a4fde53c3a73e70f4913827ba"
LAMBDA = "infra/aws/lambda/investor-reporting/reporting-publish/"
HANDLER = LAMBDA + "handler.py"
PUBLISHER = LAMBDA + "publisher.py"
TESTS_DIR = LAMBDA + "tests/"
OLD_TEST = TESTS_DIR + "test_filled_report_publish.py"
NEW_TEST = TESTS_DIR + "test_filled_report_reader.py"
TF = "infra/aws/terraform/investor-reporting/reporting-publish/"
LOCALS = TF + "locals.tf"
TF_OTHERS = [TF + n for n in ("iam.tf", "lambda.tf", "main.tf", "schedule.tf")]
SOURCE_MAP = "infra/aws/lambda/ci/lambda-source-map.json"
PRODUCER = "data/assets/scripts/gold/irpt_reporting/filled_report_values.py"
BEGIN, END = "# BEGIN FILLED-REPORT-A", "# END FILLED-REPORT-A"
FIRM = "49financial"
TABLE = "filled_report_values"


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def git_show(root, rel):
    r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (BASE, rel)], capture_output=True)
    need(r.returncode == 0, "cannot read %s at the base %s" % (rel, BASE[:10]))
    return r.stdout


def rd(root, rel):
    p = Path(root) / rel
    need(p.is_file(), "no %s" % rel)
    return p.read_bytes()


def cut_block(text, index=0):
    """(the text without the index-th FILLED-REPORT-A block's body, that body). The markers themselves stay in the outside text."""
    starts = [m.start() for m in re.finditer(re.escape(BEGIN), text)]
    ends = [m.start() for m in re.finditer(re.escape(END), text)]
    need(len(starts) == len(ends) and len(starts) > index and all(s < e for s, e in zip(starts, ends)), "the FILLED-REPORT-A block markers are missing or out of order")
    i, j = starts[index], ends[index]
    return text[:i] + text[j:], text[i:j]


def section(txt, head):
    m = re.search(r"^%s.*?(?=^def |^class |\Z)" % re.escape(head), txt, flags=re.S | re.M)
    need(m, "no %s" % head)
    return m.group(0)


# ------------------------------------------------------------------------------------------------ AC1: the diff
def check_diff(root):
    new_h, old_h = rd(root, HANDLER).decode("utf-8"), git_show(root, HANDLER).decode("utf-8")
    need("\r" not in new_h, "handler.py must keep LF line endings")
    need(new_h.count(BEGIN) == old_h.count(BEGIN) == 2 and new_h.count(END) == old_h.count(END) == 2, "the two FILLED-REPORT-A blocks must both remain")
    out_new, in_new = cut_block(new_h, 0)
    out_old, in_old = cut_block(old_h, 0)
    need(out_new == out_old, "handler.py differs from the base outside the first FILLED-REPORT-A block (module imports, summaries pass, the inline event branch and the lambda handler stay byte for byte)")
    for name in ("FILLED_REPORT_SWITCH = ", "class NotYetAvailable(Exception):", "def filled_report_enabled(", "def run_filled_report(", "def filled_report_fire(", "def read_filled_report_gold("):
        need(name in in_new, "the block must still define %s" % name.split("(")[0].split(" =")[0])
    for head in ("def filled_report_enabled(", "def run_filled_report(", "def filled_report_fire("):
        need(section(in_new, head) == section(in_old, head), "%s must be byte-identical to the base" % head)
    need("the filled-report gold table is not built yet" not in in_new, "the stub's raise must be gone")
    new_p, old_p = rd(root, PUBLISHER).decode("utf-8"), git_show(root, PUBLISHER).decode("utf-8")
    need("\r" not in new_p, "publisher.py must keep LF line endings")
    need(new_p.count(BEGIN) == old_p.count(BEGIN) == 2 and new_p.count(END) == old_p.count(END) == 2, "publisher.py keeps its two FILLED-REPORT-A blocks")
    pout_new, pin_new = cut_block(new_p, 1)
    pout_old, pin_old = cut_block(old_p, 1)
    need(pout_new == pout_old, "publisher.py differs from the base outside the body of its second FILLED-REPORT-A block (PUBLISHER_VERSION and the series path stay byte for byte)")
    for name in ("FILLED_HOUSEHOLD_FIELDS = ", "FILLED_ACCOUNT_FIELDS = ", "FILLED_WINDOW_STATUS = ", "FILLED_ABSENT_KINDS = ", "def validate_filled_report(", "def publish_filled_report(", "def report_address("):
        need(name in pin_new, "publisher.py: the block must still define %s" % name.split("(")[0].split(" =")[0])
    for head in ("def publish_filled_report(", "def report_address(", "def _filled_value_ok(", "def _filled_absent_ok("):
        need(section(pin_new, head) == section(pin_old, head), "publisher.py: %s must be byte-identical to the base" % head)
    need(rd(root, SOURCE_MAP) == git_show(root, SOURCE_MAP), "the source map must be byte-identical to the base (the re-pin is a later cell)")
    for f in TF_OTHERS:
        need(rd(root, f) == git_show(root, f), "%s must be byte-identical to the base" % f)
    lo_new, lo_old = rd(root, LOCALS).decode("utf-8"), git_show(root, LOCALS).decode("utf-8")
    need("\r" not in lo_new, "locals.tf must keep LF line endings")
    removed, added = [], []
    for line in difflib.unified_diff(lo_old.splitlines(), lo_new.splitlines(), lineterm="", n=0):
        if line.startswith(("---", "+++", "@@")):
            continue
        (removed if line.startswith("-") else added).append(line[1:])
    code_added = [a.strip() for a in added if a.strip() and not a.strip().startswith("#")]
    need(not [r for r in removed if r.strip()], "locals.tf: no line may be removed or changed (additions only): %s" % [r.strip() for r in removed if r.strip()][:2])
    need(len(code_added) == 2, "locals.tf: exactly two code lines are added (the table local and its prefix), got %d: %s" % (len(code_added), code_added[:4]))
    need(any(re.fullmatch(r'irpt_rp_gold_table_filled\s*=\s*"filled_report_values"', a) for a in code_added), "locals.tf: the new local irpt_rp_gold_table_filled = \"filled_report_values\" is missing")
    need('"irpt/${local.irpt_rp_firm}/gold/${local.irpt_rp_gold_table_filled}/",' in code_added, "locals.tf: the read prefix \"irpt/${local.irpt_rp_firm}/gold/${local.irpt_rp_gold_table_filled}/\" is missing")
    m = re.search(r"irpt_rp_gold_read_prefixes\s*=\s*\[(.*?)\]", lo_new, flags=re.S)
    need(m, "locals.tf: the read prefixes list is missing")
    entries = re.findall(r'"([^"]+)"', m.group(1))
    need(len(entries) == 3 and entries[0].endswith("gold_table_returns}/") and entries[1].endswith("gold_table_method}/") and entries[2].endswith("gold_table_filled}/"), "locals.tf: the read list must be returns, method, filled in that order: %s" % entries)
    need(re.search(r"irpt_rp_platinum_write_arns\s*=", lo_new) and re.search(r"irpt_rp_gold_list_conditions\s*=\s*\[for p in local\.irpt_rp_gold_read_prefixes", lo_new), "locals.tf: the write arns and the list conditions (built from the read prefixes) stay")
    return True


# ------------------------------------------------------------------------------------------------ AC2: the behaviour
def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def rich_doc(ref, flavour=0):
    return {"household": {"household_ref": ref, "as_of": "2026-10-15", "first_data_date": "2024-01-02" if not flavour else "2025-03-03",
                          "accounts": [{"account_id": "acct_A", "last4": "0001", "first_data_date": "2024-01-02", "window_status": {"qtd": "MEASURED", "ytd": "MEASURED", "last_12_months": "MEASURED", "since_inception": "MEASURED"}},
                                       {"account_id": "acct_B", "last4": "0002", "first_data_date": "2025-06-02", "window_status": {"qtd": "NOT_SPANNED", "ytd": "NOT_SPANNED", "last_12_months": "NOT_SPANNED", "since_inception": "MEASURED"}}]},
            "values": {"pvs.qtd.beginning_value": {"absent": "no source yet for this figure", "kind": "NO_SOURCE_YET"}, "pvs.ytd.total_return": 1.5 + flavour, "label.household": "Synthetic household",
                       "hold.allocation": {"by_row": {"equity": 42.0, "cash": "UNHELD", "bonds": {"absent": "the class holds nothing", "kind": "INSUFFICIENT_HISTORY"}}},
                       "chart.growth": [{"name": "Synthetic", "points": [{"date": "2026-10-13", "value": 100.0}, {"date": "2026-10-14", "value": 101.5}]}, {"name": "Other", "points": [{"date": "2026-10-14", "value": 7.0}]}]}}


class FakeS3(object):
    """GET and LIST only, listing in pages of three; a write method raises. Records every key fetched."""
    def __init__(self, objects):
        self.objects, self.fetched = dict(objects), []

    def list_objects_v2(self, Bucket, Prefix="", Delimiter=None, ContinuationToken=None, **kw):
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
        out["Contents"] = [{"Key": v, "Size": len(self.objects[(Bucket, v)])} for t, v in page if t == "K"]
        return out

    def get_object(self, Bucket, Key, **kw):
        if (Bucket, Key) not in self.objects:
            raise KeyError("NoSuchKey " + Key)
        self.fetched.append(Key)
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
    pq.write_table(tbl, buf)
    return buf.getvalue()


def check_behaviour(root):
    root = Path(root)
    sys.path[:0] = [str(root / LAMBDA.rstrip("/")), str(root)]
    for m in ("handler", "publisher"):
        sys.modules.pop(m, None)
    import handler as h  # noqa: E402
    import publisher as p  # noqa: E402
    from lib import opal_naming  # noqa: E402
    frv = load_mod(root / PRODUCER, "frv_ref_170")
    probe = str(opal_naming.address("irpt", FIRM, "gold", TABLE, "date=0000-00-00", "data.parquet"))
    bucket, _, key = probe[len("s3://"):].partition("/")
    base_key = key.rsplit("/date=", 1)[0]

    def day_key(d):
        return "%s/date=%s/data.parquet" % (base_key, d)

    def ref_of(rel):
        return hashlib.sha256(rel.encode("utf-8")).hexdigest()
    CID, REL = "cli_X1", "rel_X1"
    directory = {"entries": [{"ids": {"client_id": CID, "relationship_id": REL, "account_ids": ["acct_A", "acct_B"]}}, {"ids": {"client_id": "cli_NOREL", "account_ids": ["acct_C"]}},
                             {"ids": {"client_id": "cli_Y1", "relationship_id": "rel_Y1", "account_ids": ["acct_D"]}}]}
    doc = rich_doc(ref_of(REL))
    other = rich_doc(ref_of("rel_Y1"), flavour=1)
    old_doc = rich_doc(ref_of(REL), flavour=2)
    rows = frv.to_rows(doc, ref_of(REL), FIRM, "2026-10-15", "0.5.4") + frv.to_rows(other, ref_of("rel_Y1"), FIRM, "2026-10-15", "0.5.4")
    old_rows = frv.to_rows(old_doc, ref_of(REL), FIRM, "2026-10-14", "0.5.4")
    read = lambda s3, cid=CID, d=directory: h.read_filled_report_gold(FIRM, cid, s3=s3, directory=d)  # noqa: E731

    # present: the newest partition only, the other household ignored, equal to the contract document, no write
    objs = {(bucket, day_key("2026-10-14")): parquet_bytes(frv, old_rows), (bucket, day_key("2026-10-15")): parquet_bytes(frv, rows)}
    s3 = FakeS3(objs)
    got = read(s3)
    need(got == doc, "present: the composed document differs from the contract document of the household")
    need(set(got) == {"household", "values"} and got["household"]["household_ref"] == ref_of(REL), "present: the document's keys or household_ref differ")
    need(s3.fetched == [day_key("2026-10-15")], "present: only the newest partition's data.parquet may be read, read: %s" % [k.rsplit("/", 2)[-2] for k in s3.fetched])
    p.validate_filled_report(got)
    # the validator: the producer's per-window shape is accepted; the one-word shape and every other shape of window_status is refused by name
    for label, mutate in (("a single word", lambda d: d["household"]["accounts"][0].__setitem__("window_status", "MEASURED")),
                          ("a missing window", lambda d: d["household"]["accounts"][0]["window_status"].pop("ytd")),
                          ("an extra window", lambda d: d["household"]["accounts"][0]["window_status"].__setitem__("mtd", "MEASURED")),
                          ("an unknown word", lambda d: d["household"]["accounts"][0]["window_status"].__setitem__("qtd", "STALE")),
                          ("a null window", lambda d: d["household"]["accounts"][0]["window_status"].__setitem__("qtd", None))):
        bad_doc = json.loads(json.dumps(got))
        mutate(bad_doc)
        try:
            p.validate_filled_report(bad_doc)
        except p.PublishRefused:
            continue
        raise Fail("the validator accepted window_status as %s" % label)
    # pagination: many older partitions, the newest on the last page
    many = {(bucket, day_key("2026-09-%02d" % d)): parquet_bytes(frv, old_rows) for d in range(1, 10)}
    many[(bucket, day_key("2026-10-15"))] = parquet_bytes(frv, rows)
    need(read(FakeS3(many)) == doc, "pagination: the newest partition of ten must be found across the listing pages")
    # absent forms: each raises NotYetAvailable and reads no parquet when the mapping fails first
    for label, store, cid, dr in (("no partition", {}, CID, directory), ("no rows for the household", {(bucket, day_key("2026-10-15")): parquet_bytes(frv, frv.to_rows(other, ref_of("rel_Y1"), FIRM, "2026-10-15", "0.5.4"))}, CID, directory),
                                  ("client without a relationship id", objs, "cli_NOREL", directory), ("client not in the directory", objs, "cli_NOBODY", directory)):
        s3 = FakeS3(store)
        try:
            read(s3, cid, dr)
        except h.NotYetAvailable:
            if label in ("client without a relationship id", "client not in the directory"):
                need(not s3.fetched, "%s: no gold object may be read before the mapping holds" % label)
            continue
        except Exception as exc:  # noqa: BLE001
            raise Fail("%s: raised %s, not NotYetAvailable" % (label, type(exc).__name__))
        raise Fail("%s: returned a document; it must raise NotYetAvailable (never a zero, never a default)" % label)
    # refused: a household-grain member with two rows is not composable and must surface as PublishRefused, never ValueError
    bad = [dict(r) for r in rows if r["household_ref"] == ref_of(REL)]
    dup = dict(next(r for r in bad if r["member_id"] == "pvs.ytd.total_return"))
    dup["value_number"] = 9.0
    bad.append(dup)
    try:
        read(FakeS3({(bucket, day_key("2026-10-15")): parquet_bytes(frv, bad)}))
    except p.PublishRefused:
        pass
    except Exception as exc:  # noqa: BLE001
        raise Fail("refused: a malformed household raised %s, not PublishRefused" % type(exc).__name__)
    else:
        raise Fail("refused: a malformed household returned a document")
    # the pass wiring: switch on, the real reader, one put at the builder address, the bytes are the document
    puts = {}
    out = h.run_filled_report(FIRM, [CID, "cli_NOREL"], lambda a, b: puts.__setitem__(a, b), reader=lambda f, c: h.read_filled_report_gold(f, c, s3=FakeS3(objs), directory=directory), environ={"FILLED_REPORT_PASS": "1"})
    need(out["written"] == 1 and out["not_available"] == ["cli_NOREL"] and out["refused"] == [], "the pass: one written, the no-relationship client not available, none refused: %s" % out)
    need(list(puts) == [p.report_address(FIRM, CID)] and json.loads(puts[p.report_address(FIRM, CID)]) == doc, "the pass: the one put is at the builder address and its bytes are the document")
    # round trip equivalence with the producer's own inverse over every form
    refdoc = frv.rows_to_document(frv.to_rows(doc, ref_of(REL), FIRM, "2026-10-15", "0.5.4"))[ref_of(REL)]
    need(refdoc == got, "the reader's document differs from the producer's own rows_to_document")
    return True


# ------------------------------------------------------------------------------------------------ AC3: the tests
def check_tests(root):
    root = Path(root)
    new_t = rd(root, NEW_TEST).decode("utf-8")
    old_t = rd(root, OLD_TEST).decode("utf-8")
    need("test_the_shipped_reader_raises_not_yet_available" not in old_t, "the stub test must be gone from %s" % OLD_TEST.rsplit("/", 1)[-1])
    names = re.findall(r"^def (test_\w+)\(", new_t, flags=re.M)
    need(len(names) >= 8, "the new test file holds at least 8 tests, found %d" % len(names))
    for word in ("present", "absent", "refused"):
        need(any(word in n for n in names), "no test name in the new file carries the word %s" % word)
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "--color=no", str(root / OLD_TEST), str(root / NEW_TEST)], capture_output=True, text=True, cwd=str(root))
    need(r.returncode == 0, "pytest failed: %s" % (r.stdout + r.stderr)[-400:].replace("\n", " | "))
    need(re.search(r"\b\d+ passed\b", r.stdout) is not None, "pytest printed no pass count")
    return True


CHECKS = {"DB170-1-AC1": check_diff, "DB170-1-AC2": check_behaviour, "DB170-1-AC3": check_tests}


def selftest(ref_root):
    """The criteria must be green on the reference tree and red on each single-fault mutant of its reader."""
    ref = Path(ref_root)
    for cid, fn in CHECKS.items():
        fn(ref)
    handler = ref / HANDLER
    original = handler.read_bytes()
    muts = {
        "reads the oldest partition": (b"sorted(days)[-1]", b"sorted(days)[0]"),
        "returns an empty document on absent": (b'raise NotYetAvailable("the filled-report gold table holds no partition yet")', b"return {}"),
        "lets ValueError escape": (b"except (ValueError, KeyError, TypeError) as exc:", b"except KeyError as exc:"),
        "writes an object": (b"body = s3.get_object(", b's3.put_object(Bucket=bucket, Key="x", Body=b"")\n    body = s3.get_object('),
    }
    n = 0
    try:
        for label, (a, b) in muts.items():
            need(a in original, "selftest: the reference reader lacks the anchor for the mutant '%s'" % label)
            handler.write_bytes(original.replace(a, b, 1))
            try:
                check_behaviour(ref)
            except (Fail, AssertionError, Exception):  # noqa: BLE001
                n += 1
                continue
            raise AssertionError("mutant passed: " + label)
    finally:
        handler.write_bytes(original)
    # a diff mutant: a changed line outside the block
    txt = original.decode("utf-8")
    handler.write_bytes(txt.replace("def lambda_handler(event, context=None):", "def lambda_handler(event, context=None):  # touched", 1).encode("utf-8"))
    try:
        try:
            check_diff(ref)
        except Fail:
            n += 1
        else:
            raise AssertionError("diff mutant passed: a line outside the block changed")
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
        print({"DB170-1-AC1": "OK: handler.py changes only inside the first FILLED-REPORT-A block (the switch, the pass and the inline branch stay byte for byte); locals.tf gains exactly the filled table local and its read prefix; the other root files, publisher.py and the source map are byte-identical to the base",
               "DB170-1-AC2": "OK: the reader returns the contract document of the client's household from the newest partition only (paged listing, other households ignored), raises NotYetAvailable for every absent form without a read or a write, raises PublishRefused for a malformed household, and the pass writes one object at the builder address",
               "DB170-1-AC3": "OK: the stub test is gone, the new test file holds present, absent and refused tests, and both test files pass"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
