"""IRPT_DASHBD round 149, workstream FILLEDRD3 (issuer 2.0.0_SA_COO~D2) -- DB-b-310, the hop-2 reader MINTS the account ids it composes (row IRPT_DASHBD-D2-W247-S1): the table's account rows carry the RAW custodial
account id as `row_key`, the reader (DB-b-306) joins through the minted ids but still writes the RAW id into the composed document (household.accounts[].account_id, the account-grain by_row keys and the
account-named chart lines). The summary builder and the directory carry only the MINTED opaque id, so a client-facing document must too. The reader mints each of the household's raw ids with the handler's own
ids.opaque_account(firm, raw); every other key (the asset-class keys of an allocation, a chart line such as "Total") is left as it is.

  DB178-1-AC1  the diff: handler.py differs from the base only in read_filled_report_gold, _filled_compose and NEW functions of the first FILLED-REPORT-A block; publisher.py and locals.tf are byte-identical
  DB178-1-AC2  the behaviour: account_id, the account-grain by_row keys and the account-named chart lines are minted; class keys and other lines are not; no raw id remains in the serialized document
  DB178-1-AC3  the tests: at least four NEW tests carry `mint` in their name, and both filled-report test files pass

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>      green on a reference tree, red on single-fault mutants of its handler
"""
import importlib.util
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "923e562c61"  # the DB-b-306 tip: the reader that joins through the minted ids and still composes the raw id


def load_p174():
    spec = importlib.util.spec_from_file_location("p174_for_178", str(HERE / "p174_filled_reader_accounts.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["p174_for_178"] = mod
    spec.loader.exec_module(mod)
    return mod


P = load_p174()
Fail, need, rd, cut_block, func_span = P.Fail, P.need, P.rd, P.cut_block, P.func_span
LAMBDA, HANDLER, PUBLISHER, LOCALS = P.LAMBDA, P.HANDLER, P.PUBLISHER, P.LOCALS
T_PUBLISH, T_READER, PRODUCER, FIRM, TABLE = P.T_PUBLISH, P.T_READER, P.PRODUCER, P.FIRM, P.TABLE
BEGIN, END = P.BEGIN, P.END


def git_show(root, rel):
    r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (BASE, rel)], capture_output=True)
    need(r.returncode == 0, "cannot read %s at the base %s" % (rel, BASE))
    return r.stdout


def func_names(text):
    return re.findall(r"^def (\w+)\(", text, flags=re.M)


# ------------------------------------------------------------------------------------------------ AC1
def check_diff(root):
    new_h, old_h = rd(root, HANDLER).decode("utf-8"), git_show(root, HANDLER).decode("utf-8")
    need("\r" not in new_h, "handler.py must keep LF line endings")
    need(new_h.count(BEGIN) == old_h.count(BEGIN) == 2 and new_h.count(END) == old_h.count(END) == 2, "the two FILLED-REPORT-A blocks must both remain")
    out_new, in_new = cut_block(new_h, 0)
    out_old, in_old = cut_block(old_h, 0)
    need(out_new == out_old, "handler.py differs from the base outside the first FILLED-REPORT-A block")
    changed = {"read_filled_report_gold", "_filled_compose"}
    for name in func_names(in_old):
        if name in changed:
            continue
        need(name in func_names(in_new), "%s was removed from the block" % name)
        need(func_span(in_new, name) == func_span(in_old, name), "%s must be byte-identical to the base" % name)
    need(func_span(in_new, "read_filled_report_gold") != func_span(in_old, "read_filled_report_gold") or func_span(in_new, "_filled_compose") != func_span(in_old, "_filled_compose"),
         "neither read_filled_report_gold nor _filled_compose changed")
    for head in ("FILLED_REPORT_SWITCH = ", "class NotYetAvailable(Exception):"):
        need(head in in_new, "the block must still define %s" % head.split(" =")[0])
    for rel in (PUBLISHER, LOCALS):
        need(rd(root, rel) == git_show(root, rel), "%s must be byte-identical to the base" % rel.rsplit("/", 1)[-1])
    return True


# ------------------------------------------------------------------------------------------------ AC2
def doc_of(ref, accounts, points=3):
    ws = {w: "MEASURED" for w in ("qtd", "ytd", "last_12_months", "since_inception")}
    pts = lambda base: [{"date": "2026-%02d-%02d" % (1 + i // 28, 1 + i % 28), "value": base + i} for i in range(points)]  # noqa: E731
    lines = [{"name": a, "points": pts(10.0 * (k + 1))} for k, a in enumerate(accounts)] + [{"name": "Total", "points": pts(100.0)}]
    return {"household": {"household_ref": ref, "as_of": "2026-10-15", "first_data_date": "2024-01-02",
                          "accounts": [{"account_id": a, "last4": "0001", "first_data_date": "2024-01-02", "window_status": dict(ws)} for a in accounts]},
            "values": {"pvs.ytd.total_return": 1.5, "label.household": "Synthetic",
                       "hold.allocation": {"by_row": {"equity": 42.0, "bonds": {"absent": "none held", "kind": "NO_SOURCE_YET"}}},
                       "pvs.ytd.ending_value": {"by_row": {a: 1000.0 + k for k, a in enumerate(accounts)}},
                       "pvs.ytd.beginning_value": {"by_row": {a: {"absent": "no opening row", "kind": "NO_SOURCE_YET"} for a in accounts}},
                       "chart.growth": lines}}


def minted(doc, mint):
    """The contract document of the same household with every raw account id replaced by its minted id."""
    raws = [a["account_id"] for a in doc["household"]["accounts"]]
    m = {r: mint(r) for r in raws}
    out = json.loads(json.dumps(doc))
    for a in out["household"]["accounts"]:
        a["account_id"] = m[a["account_id"]]
    for mid, v in out["values"].items():
        if isinstance(v, dict) and "by_row" in v:
            v["by_row"] = {m.get(k, k): x for k, x in v["by_row"].items()}
        elif isinstance(v, list):
            for line in v:
                line["name"] = m.get(line["name"], line["name"])
    return out


def check_behaviour(root):
    root = Path(root)
    sys.path[:0] = [str(root / LAMBDA.rstrip("/")), str(root)]
    for m in ("handler", "publisher"):
        sys.modules.pop(m, None)
    import handler as h  # noqa: E402
    import publisher as p  # noqa: E402
    from lib import opal_naming  # noqa: E402
    frv = P.load_mod(root / PRODUCER, "frv_ref_178")
    ids = h._ids_module()
    mint = lambda raw: ids.opaque_account(FIRM, raw)  # noqa: E731
    probe = str(opal_naming.address("irpt", FIRM, "gold", TABLE, "date=0000-00-00", "data.parquet"))
    bucket, _, key = probe[len("s3://"):].partition("/")
    base_key = key.rsplit("/date=", 1)[0]
    day_key = lambda d: "%s/date=%s/data.parquet" % (base_key, d)  # noqa: E731
    raw1, raw2, raw3, raw4 = "RAWACC001A", "RAWACC002B", "RAWACC003C", "RAWACC004D"
    d1, d2, d3 = doc_of("hh1", [raw1, raw2]), doc_of("hh2", [raw3]), doc_of("hh3", [raw4])
    rows = []
    for ref, doc in (("hh1", d1), ("hh2", d2), ("hh3", d3)):
        rows += frv.to_rows(doc, ref, FIRM, "2026-10-15", "0.5.4")
    directory = {"entries": [
        {"ids": {"client_id": "cli_1", "account_ids": [mint(raw1), mint(raw2)]}},
        {"ids": {"client_id": "cli_2", "account_ids": [mint(raw3)]}},
        {"ids": {"client_id": "cli_two", "account_ids": [mint(raw1), mint(raw3)]}},
        {"ids": {"client_id": "cli_none", "account_ids": [mint("RAWACC999Z")]}}]}
    read = lambda s3, cid, dr=directory: h.read_filled_report_gold(FIRM, cid, s3=s3, directory=dr)  # noqa: E731
    store = lambda: P.FakeS3({(bucket, day_key("2026-10-15")): P.parquet_bytes(frv, rows)})  # noqa: E731
    s3 = store()
    got = read(s3, "cli_1")
    want = minted(d1, mint)
    need(want != d1 and mint(raw1) != raw1 and mint(raw2) != raw2, "selftest of the checker: the minted id equals the raw id")
    need(got == want, "present: the composed document differs from the contract document with its account ids minted (account_id, the account-grain by_row keys, the account-named chart lines); got accounts %s" % [a["account_id"] for a in got["household"]["accounts"]])
    p.validate_filled_report(got)
    text = json.dumps(got, sort_keys=True)
    for raw in (raw1, raw2):
        need(raw not in text, "the raw account id %s is still in the serialized document" % raw)
    need(got["values"]["hold.allocation"]["by_row"].keys() == {"equity", "bonds"}, "the asset-class keys of the allocation must stay as they are")
    need([ln["name"] for ln in got["values"]["chart.growth"]][-1] == "Total", "a chart line that is not an account (Total) must keep its name")
    need(sorted(got["values"]["pvs.ytd.ending_value"]["by_row"]) == sorted([mint(raw1), mint(raw2)]), "the account-grain by_row keys must be exactly the minted ids")
    need(read(s3, "cli_2") == minted(d2, mint), "the second client's household differs from its minted contract document")
    for cid, label in (("cli_none", "accounts that match no household"), ("cli_nobody", "a client not in the directory")):
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
        raise Fail("two households: a client whose accounts span two households returned a document")
    need(s3.gets.count(day_key("2026-10-15")) == 1, "one pass must fetch the newest partition once, fetched %d times" % s3.gets.count(day_key("2026-10-15")))
    # a document read twice is the same document, and the reader leaves no state in the cached table
    need(read(s3, "cli_1") == want and s3.gets.count(day_key("2026-10-15")) == 1, "a second read of the same client must return the same minted document without a second fetch")
    # speed: the minting adds no per-row cost worth a minute
    big_rows, big_dir = [], []
    for i in range(400):
        raw = "BIGACC%05d" % i
        big_rows += frv.to_rows(doc_of("bh%04d" % i, [raw], points=480), "bh%04d" % i, FIRM, "2026-10-15", "0.5.4")
        big_dir.append({"ids": {"client_id": "big_%04d" % i, "account_ids": [mint(raw)]}})
    big = P.FakeS3({(bucket, day_key("2026-10-15")): P.parquet_bytes(frv, big_rows)})
    bd = {"entries": big_dir}
    t0 = time.time()
    first = h.read_filled_report_gold(FIRM, "big_0000", s3=big, directory=bd)
    for i in range(1, 400):
        h.read_filled_report_gold(FIRM, "big_%04d" % i, s3=big, directory=bd)
    elapsed = time.time() - t0
    need(first["household"]["accounts"][0]["account_id"] == mint("BIGACC00000") and big.gets.count(day_key("2026-10-15")) == 1, "the big pass must mint and fetch the partition once")
    need(elapsed < 25, "400 clients over %d rows took %.1f s (limit 25 s)" % (len(big_rows), elapsed))
    puts = {}
    s3p = store()
    out = h.run_filled_report(FIRM, ["cli_1", "cli_two", "cli_none"], lambda a, b: puts.__setitem__(a, b), reader=lambda f, c: read(s3p, c), environ={"FILLED_REPORT_PASS": "1"})
    need(out["written"] == 1 and out["refused"] == ["cli_two"] and out["not_available"] == ["cli_none"], "the pass: %s" % out)
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
    need(len([n for n in new if "mint" in n]) >= 4, "at least four NEW tests carry mint in their name, found %s" % sorted(new))
    block = cut_block(rd(root, HANDLER).decode("utf-8"), 0)[1]
    need("opaque_account" in block, "the block must mint with the handler's own ids.opaque_account")
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "--color=no", str(root / T_PUBLISH), str(root / T_READER)], capture_output=True, text=True, cwd=str(root))
    need(r.returncode == 0, "pytest failed: %s" % (r.stdout + r.stderr)[-400:].replace("\n", " | "))
    need(re.search(r"\d+ passed", r.stdout) is not None, "pytest printed no pass count")
    return True


CHECKS = {"DB178-1-AC1": check_diff, "DB178-1-AC2": check_behaviour, "DB178-1-AC3": check_tests}


def selftest(ref_root):
    ref = Path(ref_root)
    for fn in CHECKS.values():
        fn(ref)
    handler = ref / HANDLER
    original = handler.read_bytes()
    txt = original.decode("utf-8")
    muts = {
        "account_id is left raw": ('a["account_id"] = mint[a["account_id"]]', 'a["account_id"] = a["account_id"]'),
        "by_row keys are left raw": ('v["by_row"] = {mint.get(k, k): x for k, x in v["by_row"].items()}', 'v["by_row"] = dict(v["by_row"])'),
        "chart line names are left raw": ('line["name"] = mint.get(line["name"], line["name"])', 'line["name"] = line["name"]'),
        "class keys are minted too": ('v["by_row"] = {mint.get(k, k): x for k, x in v["by_row"].items()}', 'v["by_row"] = {ids.opaque_account(firm, k): x for k, x in v["by_row"].items()}'),
        "the minting uses another firm": ('mint = {a["account_id"]: ids.opaque_account(firm, a["account_id"])', 'mint = {a["account_id"]: ids.opaque_account("cottonwood", a["account_id"])'),
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
        print({"DB178-1-AC1": "OK: handler.py differs from the base only in read_filled_report_gold, _filled_compose and new functions of the first block; publisher.py and locals.tf are byte-identical",
               "DB178-1-AC2": "OK: account_id, the account-grain by_row keys and the account-named chart lines are minted; the class keys and other lines are not; no raw id remains in the serialized document; one fetch, two households refused, speed inside the limit",
               "DB178-1-AC3": "OK: four or more new mint tests exist, the block mints with the handler's own ids.opaque_account, and both filled-report test files pass"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
