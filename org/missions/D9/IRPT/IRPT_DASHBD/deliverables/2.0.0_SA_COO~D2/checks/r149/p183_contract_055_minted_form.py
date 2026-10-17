"""IRPT_DASHBD round 149, workstream CONTRACT055 (issuer 2.0.0_SA_COO~D2) -- DB-b-317, the CTO's ruling (packet-5 analysis, 1.0.0_SA_CTO~DELL2 @ee3383bf1e, ruling 2): contract 0.5.5 for the MINTED account id, in ONE drain with its producer
of that form. Contract 0.5.5: `account_id` is the issued opaque (minted) id, a new field `account_id_form` (value `minted`) travels on every account entry so a consumer can reject a raw id BY FIELD, the order rule is
"ascending by account_id" (the minted id, stable). The reader (`_filled_mint`, DB-b-310) adds the field and sorts ascending by the minted id; the publisher's `validate_filled_report` refuses an entry without the field, with another
value, with a non-minted id or out of order. LOCAL (no apply): the deploy of the reader and validator is a later signed pair.

  DB183-1-AC1  the diff: the contract JSON changes only at the agreed paths (version 0.5.5, the field, the order rule, the source note); handler.py only in `_filled_mint` and new functions of its first block; publisher.py only in `validate_filled_report` and the account-field constant of its second block; the two filled-report test files
  DB183-1-AC2  the behaviour: the composed document carries account_id_form minted on every entry, accounts ascending by the minted id with each entry's own last4, and the validator refuses a missing form, another form, a raw-looking id and an out-of-order list
  DB183-1-AC3  the tests: at least four NEW tests carry `form` or `ascending` in their name, and both filled-report test files pass

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest <reference_root>      green on a reference tree, red on single-fault mutants
"""
import copy
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "63c01c34e4"  # the tree after DB-b-310 and the ledger closures: the reader mints and does not yet sort or carry the form
CONTRACT = "org/standards/IRPT_DASHBD_PERFORMANCE_REPORT_CONTRACT.json"
ALLOWED_PATHS = ("contract_version", "lineage", "open_changes", "document.shape", "document.filled_report.", "document.row_dimensions.account.")


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, str(HERE / rel))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


Q = load("p178_for_183", "p178_filled_reader_mints_ids.py")
P = Q.P
Fail, need, rd, cut_block, func_span = Q.Fail, Q.need, Q.rd, Q.cut_block, Q.func_span
LAMBDA, HANDLER, PUBLISHER, LOCALS = Q.LAMBDA, Q.HANDLER, Q.PUBLISHER, Q.LOCALS
T_PUBLISH, T_READER, PRODUCER, FIRM, TABLE = Q.T_PUBLISH, Q.T_READER, Q.PRODUCER, Q.FIRM, Q.TABLE
BEGIN, END = Q.BEGIN, Q.END


def git_show(root, rel):
    r = subprocess.run(["git", "-C", str(root), "show", "%s:%s" % (BASE, rel)], capture_output=True)
    need(r.returncode == 0, "cannot read %s at the base %s" % (rel, BASE))
    return r.stdout


def leaves(x, path=""):
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            out.update(leaves(v, path + ("." if path else "") + k))
        return out
    if isinstance(x, list):
        out = {}
        for i, v in enumerate(x):
            out.update(leaves(v, "%s[%d]" % (path, i)))
        out["%s#len" % path] = len(x)
        return out
    return {path: x}


def func_names(text):
    return re.findall(r"^def (\w+)\(", text, flags=re.M)


# ------------------------------------------------------------------------------------------------ AC1
def check_diff(root):
    new_c, old_c = json.loads(rd(root, CONTRACT).decode("utf-8")), json.loads(git_show(root, CONTRACT).decode("utf-8"))
    need(new_c.get("contract_version") == "0.5.5", "contract_version must read 0.5.5, it reads %s" % new_c.get("contract_version"))
    a, b = leaves(old_c), leaves(new_c)
    changed = sorted(k for k in set(a) | set(b) if a.get(k, "<absent>") != b.get(k, "<absent>"))
    stray = [k for k in changed if not k.startswith(ALLOWED_PATHS)]
    need(not stray, "the contract changed outside the agreed paths: %s" % stray[:4])
    fr = new_c["document"]["filled_report"]
    need(fr["account_entry_fields"][:2] == ["account_id", "account_id_form"] and len(fr["account_entry_fields"]) == 5, "account_entry_fields must read [account_id, account_id_form, last4, first_data_date, window_status]: %s" % fr["account_entry_fields"])
    text = json.dumps(new_c["document"], ensure_ascii=True)
    need("minted" in text and "ascending" in new_c["document"]["row_dimensions"]["account"]["order"] and "ascending" in new_c["document"]["shape"], "the shape and the account order rule must say ascending, and the document must say minted")
    need("minted" in new_c["document"]["row_dimensions"]["account"]["sources"]["account_id"], "sources.account_id must name the minted id")
    new_h, old_h = rd(root, HANDLER).decode("utf-8"), git_show(root, HANDLER).decode("utf-8")
    need("\r" not in new_h and new_h.count(BEGIN) == old_h.count(BEGIN) == 2, "handler.py: LF line endings and both FILLED-REPORT-A blocks")
    out_n, in_n = cut_block(new_h, 0)
    out_o, in_o = cut_block(old_h, 0)
    need(out_n == out_o, "handler.py differs from the base outside the first FILLED-REPORT-A block")
    for name in func_names(in_o):
        if name in ("_filled_mint", "read_filled_report_gold"):
            continue
        need(name in func_names(in_n) and func_span(in_n, name) == func_span(in_o, name), "handler.py: %s must be byte-identical to the base" % name)
    new_p, old_p = rd(root, PUBLISHER).decode("utf-8"), git_show(root, PUBLISHER).decode("utf-8")
    need("\r" not in new_p and new_p.count(BEGIN) == old_p.count(BEGIN) == 2, "publisher.py: LF line endings and both FILLED-REPORT-A blocks")
    out_n, in_n = cut_block(new_p, 1)
    out_o, in_o = cut_block(old_p, 1)
    need(out_n == out_o, "publisher.py differs from the base outside its second FILLED-REPORT-A block (no new import)")
    for name in func_names(in_o):
        if name == "validate_filled_report":
            continue
        need(name in func_names(in_n) and func_span(in_n, name) == func_span(in_o, name), "publisher.py: %s must be byte-identical to the base" % name)
    need(func_span(in_n, "validate_filled_report") != func_span(in_o, "validate_filled_report"), "validate_filled_report is unchanged")
    need(rd(root, LOCALS) == git_show(root, LOCALS), "locals.tf must be byte-identical to the base")
    return True


# ------------------------------------------------------------------------------------------------ AC2
def expected(doc, mint):
    """The contract document with every raw account id minted, the form set on every entry, the accounts ascending by the minted id."""
    out = json.loads(json.dumps(doc))
    m = {a["account_id"]: mint(a["account_id"]) for a in out["household"]["accounts"]}
    for a in out["household"]["accounts"]:
        a["account_id"] = m[a["account_id"]]
        a["account_id_form"] = "minted"
    out["household"]["accounts"].sort(key=lambda a: a["account_id"])
    for v in out["values"].values():
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
    frv = P.load_mod(root / PRODUCER, "frv_ref_183")
    ids = h._ids_module()
    mint = lambda raw: ids.opaque_account(FIRM, raw)  # noqa: E731
    raws = ["RAWACC%03dQ" % n for n in range(1, 9)]
    pick = None
    for i in range(len(raws) - 3):
        sub = raws[i:i + 4]
        if [mint(r) for r in sub] != sorted(mint(r) for r in sub):
            pick = sub
            break
    need(pick is not None, "checker: no 4-subset of the synthetic raw ids changes order when minted")
    probe = str(opal_naming.address("irpt", FIRM, "gold", TABLE, "date=0000-00-00", "data.parquet"))
    bucket, _, key = probe[len("s3://"):].partition("/")
    day_key = lambda d: "%s/date=%s/data.parquet" % (key.rsplit("/date=", 1)[0], d)  # noqa: E731
    d1 = Q.doc_of("hh1", pick)
    for k, a in enumerate(d1["household"]["accounts"]):
        a["last4"] = "%04d" % (k + 1)
    d2 = Q.doc_of("hh2", ["RAWACC099Q"])
    rows = frv.to_rows(d1, "hh1", FIRM, "2026-10-15", "0.5.5") + frv.to_rows(d2, "hh2", FIRM, "2026-10-15", "0.5.5")
    directory = {"entries": [{"ids": {"client_id": "cli_1", "account_ids": [mint(r) for r in pick]}},
                             {"ids": {"client_id": "cli_2", "account_ids": [mint("RAWACC099Q")]}},
                             {"ids": {"client_id": "cli_two", "account_ids": [mint(pick[0]), mint("RAWACC099Q")]}}]}
    s3 = P.FakeS3({(bucket, day_key("2026-10-15")): P.parquet_bytes(frv, rows)})
    got = h.read_filled_report_gold(FIRM, "cli_1", s3=s3, directory=directory)
    want = expected(d1, mint)
    accts = got["household"]["accounts"]
    need(all(a.get("account_id_form") == "minted" for a in accts), "every account entry must carry account_id_form minted: %s" % [a.get("account_id_form") for a in accts])
    need([a["account_id"] for a in accts] == sorted(a["account_id"] for a in accts), "the accounts must be ascending by the minted account_id")
    need(got == want, "present: the composed document differs from the contract document (minted ids, the form on every entry, ascending order, each entry keeping its own last4)")
    p.validate_filled_report(got)

    def refused(doc, label):
        try:
            p.validate_filled_report(doc)
        except p.PublishRefused:
            return
        except Exception as exc:  # noqa: BLE001
            raise Fail("%s: raised %s, not PublishRefused" % (label, type(exc).__name__))
        raise Fail("%s: the validator accepted it; it must raise PublishRefused" % label)
    a = copy.deepcopy(got)
    del a["household"]["accounts"][0]["account_id_form"]
    refused(a, "a missing account_id_form")
    a = copy.deepcopy(got)
    a["household"]["accounts"][0]["account_id_form"] = "custodian"
    refused(a, "account_id_form other than minted")
    a = copy.deepcopy(got)
    a["household"]["accounts"][0]["account_id"] = pick[0]
    refused(a, "a raw-looking account_id with form minted")
    a = copy.deepcopy(got)
    a["household"]["accounts"].reverse()
    refused(a, "accounts out of ascending order")
    a = copy.deepcopy(got)
    a["household"]["accounts"][0]["extra"] = 1
    refused(a, "an extra account field")
    need(h.read_filled_report_gold(FIRM, "cli_2", s3=s3, directory=directory) == expected(d2, mint), "the one-account household differs from its minted contract document")
    try:
        h.read_filled_report_gold(FIRM, "cli_two", s3=P.FakeS3({(bucket, day_key("2026-10-15")): P.parquet_bytes(frv, rows)}), directory=directory)
    except p.PublishRefused:
        pass
    else:
        raise Fail("two households: must raise PublishRefused")
    puts = {}
    out = h.run_filled_report(FIRM, ["cli_1", "cli_two"], lambda ad, bd: puts.__setitem__(ad, bd), reader=lambda f, c: h.read_filled_report_gold(f, c, s3=s3, directory=directory), environ={"FILLED_REPORT_PASS": "1"})
    need(out["written"] == 1 and out["refused"] == ["cli_two"], "the pass: one written, the two-household client refused: %s" % out)
    body = list(puts.values())[0]
    need(b"account_id_form" in body and all(r.encode("ascii") not in body for r in pick), "the written document carries the form and no raw custodian id")
    return True


# ------------------------------------------------------------------------------------------------ AC3
def check_tests(root):
    root = Path(root)
    new = set()
    for rel in (T_PUBLISH, T_READER):
        txt = rd(root, rel).decode("utf-8")
        base_txt = git_show(root, rel).decode("utf-8")
        new |= set(re.findall(r"^def (test_\w+)\(", txt, flags=re.M)) - set(re.findall(r"^def (test_\w+)\(", base_txt, flags=re.M))
    need(len([n for n in new if "form" in n or "ascending" in n]) >= 4, "at least four NEW tests carry form or ascending in their name, found %s" % sorted(new))
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", "--color=no", str(root / T_PUBLISH), str(root / T_READER)], capture_output=True, text=True, cwd=str(root))
    need(r.returncode == 0, "pytest failed: %s" % (r.stdout + r.stderr)[-400:].replace("\n", " | "))
    need(re.search(r"\d+ passed", r.stdout) is not None, "pytest printed no pass count")
    return True


CHECKS = {"DB183-1-AC1": check_diff, "DB183-1-AC2": check_behaviour, "DB183-1-AC3": check_tests}


def selftest(ref_root):
    ref = Path(ref_root)
    for fn in CHECKS.values():
        fn(ref)
    handler, publisher = ref / HANDLER, ref / PUBLISHER
    h0, p0 = handler.read_bytes(), publisher.read_bytes()
    muts = {
        "the form is not set": (handler, 'entry["account_id_form"] = "minted"', "pass"),
        "the accounts are not sorted": (handler, 'doc["household"]["accounts"].sort(key=lambda e: e["account_id"])', "pass"),
        "the validator ignores the form": (publisher, 'if entry["account_id_form"] != "minted":', "if False:"),
        "the validator ignores the order": (publisher, "if ids != sorted(ids):", "if False:"),
        "the validator accepts a raw-looking id": (publisher, "raise PublishRefused(\"an account entry's account_id is not a minted opaque id\")", "pass"),
    }
    n = 0
    try:
        for label, (path, a, b) in muts.items():
            txt = path.read_bytes().decode("utf-8")
            need(a in txt, "selftest: the reference lacks the anchor for '%s'" % label)
            path.write_bytes(txt.replace(a, b, 1).encode("utf-8"))
            try:
                check_behaviour(ref)
            except (Fail, AssertionError, Exception):  # noqa: BLE001
                n += 1
                path.write_bytes(h0 if path == handler else p0)
                continue
            raise AssertionError("mutant passed: " + label)
        handler.write_bytes(h0.decode("utf-8").replace("def lambda_handler(event, context=None):", "def lambda_handler(event, context=None):  # touched", 1).encode("utf-8"))
        try:
            check_diff(ref)
        except Fail:
            n += 1
        else:
            raise AssertionError("diff mutant passed")
    finally:
        handler.write_bytes(h0)
        publisher.write_bytes(p0)
    print("selftest: green on the reference and red on %d single-fault mutants" % n)
    print("selftest PASS")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest(sys.argv[2])
        sys.exit(0)
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DB183-1-AC1": "OK: the contract reads 0.5.5 and changed only at the agreed paths; handler.py changed only in _filled_mint and new functions; publisher.py only in validate_filled_report; locals.tf untouched",
               "DB183-1-AC2": "OK: the composed document carries account_id_form minted on every entry, the accounts ascending by the minted id with each entry's own last4, and the validator refuses a missing form, another form, a raw-looking id, an out-of-order list and an extra field",
               "DB183-1-AC3": "OK: four or more new form/ascending tests exist and both filled-report test files pass"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
