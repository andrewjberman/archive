"""IRPT_DASHBD round 132, workstream F-SHIP ~F2 (issuer 2.0.0_SA_COO~F2) -- FWD-5: the INFLECTION PRODUCER under the CTO's round-131 rulings (msg 9342).

  DB-f-1801 (~1801) `account_transaction_inflection.py` (1) takes business_date from the ONE shared function (first NYSE trading day on or after the
                    trade date; the transDate stays the trade_date as received; a Saturday transDate rolls to Monday), (2) serves price from
                    navPrice ONLY on a line that carries a fund family (`fundFamilyName`) and has units and a positive navPrice, and every other
                    line serves price null with the reason code NAV_PRICE_FUND_ONLY (units zero: ZERO_UNITS; navPrice not positive:
                    NAV_NOT_POSITIVE), counted by `price_null_census(frame)` and carried in the manifest, (3) refuses to write a row under a
                    partition day other than its business_date, (4) drops a Complete line that offsets a Reversed original (CTO ruling 1:
                    `reversed_keys_of(frame)` and `split_complete(frame, reversed_keys=...)`, counted OFFSET_OF_REVERSED). Every round-131 Inflection rule still holds (status Complete only, the one key
                    function, source_action_raw, 48 live descriptions).
                    DBF132-1-AC3

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
       python <this file> --selftest                        the pure helpers on synthetic arms
"""
import copy
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

CONTRACT = "org/standards/IRPT_DASHBD_ACCOUNT_TRANSACTION_CONTRACT.json"
WORDS = "data/assets/scripts/gold/irpt_reporting/transaction_words.json"
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/"
CENSUS3 = D + "R128_LIVE_SOURCE_CENSUS_3FIRMS.json"
FIELDS = D + "R131_INFLECTION_FIELD_CENSUS.json"
INF = "data/assets/scripts/gold/irpt_reporting/account_transaction_inflection.py"
INF_TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_account_transaction_inflection.py"
F49 = "data/assets/scripts/gold/irpt_reporting/account_transaction.py"
UNMAPPED = "UNMAPPED"
NOT_IN = "CODE_NOT_IN_MAPPING"
BY_TABLE = "UNMAPPED_BY_TABLE"
COLUMNS = ("firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units",
           "price", "amount", "fee", "custodian", "flow_class", "source_txn_id", "coverage", "source_action_raw")
TITLE_WORDS = ("status", "description", "flow", "price", "raw", "account", "date", "unmapped", "new code", "schema", "vocabulary", "whitespace",
               "every live", "collide", "custodian", "identifier", "fund", "roll", "reason", "partition", "offset")
STATUSES = ("Complete", "Inactive", "Pending", "Pending Corporate Action", "Rejected", "Reversed")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def norm(v):
    return v.strip()


def test_names(text):
    return [m.group(1).replace("_", " ") for m in re.finditer(r"^def (test_\w+)", text, re.M)]


def missing_words(names, words):
    low = " | ".join(names).lower()
    return [w for w in words if w not in low]


def pytest_counts(out):
    p = re.findall(r"(\d+) passed", out)
    f = re.findall(r"(\d+) failed", out)
    e = re.findall(r"(\d+) error", out)
    return (int(p[-1]) if p else 0), (int(f[-1]) if f else 0), (int(e[-1]) if e else 0)


def schema_hash_of(fields):
    return hashlib.sha256("\n".join(sorted("%s:%s" % (n, t) for n, t in fields)).encode("ascii")).hexdigest()


def load_module(root, rel, name):
    p = Path(root) / rel
    need(p.is_file(), "missing " + rel)
    spec = importlib.util.spec_from_file_location(name, p)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(p.parent))
    spec.loader.exec_module(mod)
    return mod


def run_pytest(root, rel, minimum):
    run = subprocess.run([sys.executable, "-m", "pytest", rel, "-q", "-p", "no:cacheprovider"], cwd=str(root), capture_output=True,
                         text=True, timeout=600)
    passed, failed, errors = pytest_counts((run.stdout or "") + (run.stderr or ""))
    need(run.returncode == 0 and failed == 0 and errors == 0, "pytest %s rc=%s failed=%s errors=%s" % (rel, run.returncode, failed, errors))
    need(passed >= minimum, "%s: only %d tests pass (%d required)" % (rel, passed, minimum))


def frame(rows):
    import pandas as pd
    return pd.DataFrame(rows)


def base_row(**k):
    """An Inflection fact_transactions line with the columns the producer reads (avgPrice is deliberately absent: the producer must not read it)."""
    row = {"id": 900001, "productName": "  Test Product ", "fundFamilyName": " Test Fund Family ", "ticker": " TEST ", "accountId": 7000001, "custodianName": " Some Custodian ",
           "status": "Complete", "transDate": "2026-03-10", "transactionDescription": "Buy Exchange", "transAmount": 100.0, "navPrice": 25.0,
           "noUnits": 4.0}
    row.update(k)
    return row


def judge(o, desc, m):
    """A producer row against the contract's mapping row for the description: never CODE_NOT_IN_MAPPING; UNMAPPED_BY_TABLE iff the table rules the
    description UNMAPPED; otherwise the mapping's word and flow class. Returns a problem string or None."""
    if o["coverage"] == NOT_IN:
        return "description %r read CODE_NOT_IN_MAPPING" % desc
    if m["opal_type"] == UNMAPPED:
        if o["coverage"] != BY_TABLE:
            return "description %r is UNMAPPED in the table but read %s" % (desc, o["coverage"])
    else:
        if o["coverage"] != "MEASURED" or o["txn_type"] != m["opal_type"]:
            return "description %r gave %r / %s, the mapping says %r" % (desc, o["txn_type"], o["coverage"], m["opal_type"])
    if o["flow_class"] != m["flow_class"]:
        return "description %r flow_class %r, the mapping says %r" % (desc, o["flow_class"], m["flow_class"])
    return None


def live_problems(mod, con, census3):
    """Every DISTINCT live description (47) of the committed census EXACTLY AS RECEIVED, each again padded with blanks, plus the contract's own
    rows (48) so the not-yet-observed one is exercised too."""
    by = {norm(m["source_value"]): m for m in con["source_mapping"] if m["firm"] == "inflection"}
    live = list(census3["firms"]["inflection"]["values"]["transactionDescription"])
    allv = list(dict.fromkeys(live + [m["source_value"] for m in by.values()]))
    rows, meta, pr = [], [], []
    for i, d in enumerate(allv):
        for variant in (d, " " + norm(d), norm(d) + "  "):
            rows.append(base_row(id=1000 + len(rows), transactionDescription=variant))
            meta.append((d, variant))
    out = mod.normalize_trn(frame(rows), "inflection")
    need(len(out) == len(rows), "normalize_trn did not return one row per input row")
    for o, (d, variant) in zip(out, meta):
        m = by.get(norm(d))
        if m is None:
            pr.append("description %r: the contract has no row for it" % d)
            continue
        bad = judge(o, d, m)
        if bad:
            pr.append(bad)
        if o["source_action_raw"] != variant:
            pr.append("description %r: source_action_raw %r is not the value as received %r" % (d, o["source_action_raw"], variant))
    return pr, {"live_descriptions": len(live), "contract_descriptions": len(by), "domain": len(allv), "lines": len(rows)}


def ac_all(root):
    con = json.loads((Path(root) / CONTRACT).read_text(encoding="utf-8"))
    words = json.loads((Path(root) / WORDS).read_text(encoding="utf-8"))
    census3 = json.loads((Path(root) / CENSUS3).read_text(encoding="utf-8"))
    fields = json.loads((Path(root) / FIELDS).read_text(encoding="utf-8"))
    names = test_names((Path(root) / INF_TEST).read_text(encoding="utf-8")) if (Path(root) / INF_TEST).is_file() else []
    need(names, "missing test file " + INF_TEST)
    mw = missing_words(names, TITLE_WORDS)
    need(not mw, "the Inflection test names lack " + repr(mw))
    run_pytest(root, INF_TEST, 51)
    mod = load_module(root, INF, "account_transaction_inflection_under_check")
    fl = [(f.name, str(f.type)) for f in mod.ARROW_SCHEMA]
    need([n for n, _ in fl] == list(COLUMNS) and schema_hash_of(fl) == con["schema_hash"], "ARROW_SCHEMA is not the contract's (names, order, hash)")
    src = (Path(root) / INF).read_text(encoding="utf-8")
    need("def normalise_key" not in src and "def keyed_map" not in src, "the Inflection producer re-implements the key function: it must import it")
    need('"avgPrice"' not in src and "'avgPrice'" not in src, "the Inflection producer reads avgPrice, which is null on every row")
    # a mixed-status frame: the status rule
    mixed = frame([base_row(id=1), base_row(id=2, status="Rejected"), base_row(id=3, status="Pending"), base_row(id=4, status="Reversed"),
                   base_row(id=5, status="Pending Corporate Action"), base_row(id=6, status="Inactive"), base_row(id=7)])
    kept, excluded = mod.split_complete(mixed)
    need(len(kept) == 2 and excluded == {"Rejected": 1, "Pending": 1, "Reversed": 1, "Pending Corporate Action": 1, "Inactive": 1},
         "split_complete must keep the Complete lines and count the others per status: %s" % (excluded,))
    try:
        mod.split_complete(frame([base_row(status="Surprising")]))
    except SystemExit as e:
        need("status" in str(e).lower(), "the refusal of an unknown status must name the status")
    else:
        raise Fail("split_complete accepted a status outside the six")
    try:
        mod.normalize_trn(frame([base_row(status="Rejected")]), "inflection")
    except SystemExit:
        pass
    else:
        raise Fail("normalize_trn accepted a line that is not Complete (split_complete is the only door)")
    rf = con["row_filter"]["inflection"]
    need(rf["keep"] == ["Complete"] and sorted(rf["excluded_rows_per_status"]) == sorted(s for s in STATUSES if s != "Complete")
         and rf["excluded_rows_per_status"] == {k: v for k, v in fields["rows_per_status"].items() if k != "Complete"},
         "the contract's row_filter is not the issuer's R131 census")
    # one line, field by field
    rows = mod.normalize_trn(frame([
        base_row(), base_row(id=2, noUnits=0.0), base_row(id=3, navPrice=0.0), base_row(id=4, ticker="  ", productName=""),
        base_row(id=5, transactionDescription="A Description The Mapping Lacks"),
        base_row(id=6, accountId=7000002, transDate="2026-03-14", transAmount=-12.5, custodianName="X Y"),
        base_row(id=7, fundFamilyName="   "), base_row(id=8, fundFamilyName=None)]), "inflection")
    need(isinstance(rows, list) and len(rows) == 8, "normalize_trn did not return one row per input row")
    for r in rows:
        need(list(r.keys()) == list(COLUMNS), "a row's keys are not the contract's columns in order")
        need(r["firm"] == "inflection" and r["settle_date"] is None and r["fee"] is None, "firm, settle_date or fee is wrong (the last two are absent)")
    a, zero_units, zero_nav, blank, new, last, no_family_blank, no_family_null = rows
    need(a["account_id"] == "7000001" and str(a["business_date"]) == "2026-03-10" and a["business_date"] == a["trade_date"],
         "account_id is str(int(accountId)); a trading-day transDate is both business_date and trade_date")
    need(a["symbol"] == "TEST" and a["asset_name"] == "Test Product" and a["units"] == 4.0 and a["amount"] == 100.0, "symbol, asset_name, units or amount wrong")
    need(a["custodian"] == "some custodian" and a["source_txn_id"] == "900001", "custodian (stripped, lower-cased) or source_txn_id (str of id) wrong")
    need(a["price"] == 25.0 and zero_units["price"] is None and zero_nav["price"] is None,
         "price is navPrice on a fund-family line with units and a positive navPrice, else None")
    need(no_family_blank["price"] is None and no_family_null["price"] is None,
         "a unit-bearing line with a blank or null fundFamilyName must serve price None (NAV_PRICE_FUND_ONLY)")
    need(blank["symbol"] is None and blank["asset_name"] is None, "an empty ticker or product name must be null")
    need(new["coverage"] == NOT_IN and new["txn_type"] == UNMAPPED and new["flow_class"] == "UNRESOLVED" and new["action"] is None
         and new["source_action_raw"] == "A Description The Mapping Lacks", "a description the mapping lacks: UNMAPPED / UNRESOLVED / CODE_NOT_IN_MAPPING, counted, raw kept")
    need(last["amount"] == -12.5 and str(last["trade_date"]) == "2026-03-14" and str(last["business_date"]) == "2026-03-16",
         "a Saturday transDate keeps trade_date as received and rolls business_date to the next trading day (Monday); amount is transAmount as booked")
    # the Reversed offset rule (CTO ruling 1): a Complete line that offsets a Reversed original leaves with it
    rv = frame([base_row(id=31, accountId=7000009, ticker="OFFX", noUnits=0.0, transAmount=-5.0, status="Reversed"),
                base_row(id=32, accountId=7000009, ticker="OFFX", noUnits=0.0, transAmount=5.0),
                base_row(id=33, accountId=7000009, ticker="OFFX", noUnits=0.0, transAmount=6.0), base_row(id=34)])
    keys = mod.reversed_keys_of(rv)
    need(keys == {(7000009, "OFFX", 0.0, -5.0)}, "reversed_keys_of must return the set of (accountId, ticker, noUnits, transAmount) of the Reversed lines: %s" % (keys,))
    kept_rv, ex_rv = mod.split_complete(rv, reversed_keys=keys)
    need(sorted(int(x) for x in kept_rv["id"]) == [33, 34] and ex_rv == {"Reversed": 1, "OFFSET_OF_REVERSED": 1},
         "split_complete(reversed_keys=...) must drop the Complete line whose negated key is a Reversed key and count it OFFSET_OF_REVERSED: %s" % (ex_rv,))
    kept_nokeys, ex_nokeys = mod.split_complete(rv)
    need(len(kept_nokeys) == 3 and ex_nokeys == {"Reversed": 1}, "split_complete without reversed_keys must not drop offsets")
    # the reason census
    reasons = mod.price_null_census(frame([base_row(id=11), base_row(id=12, noUnits=0.0), base_row(id=13, navPrice=0.0),
                                           base_row(id=14, fundFamilyName=" "), base_row(id=15, fundFamilyName=None, noUnits=0.0)]))
    need(reasons == {"NAV_PRICE_FUND_ONLY": 1, "ZERO_UNITS": 2, "NAV_NOT_POSITIVE": 1},
         "price_null_census must count the null prices by reason code: %s" % (reasons,))
    mod.check_transaction_rows(rows)
    try:
        mod.check_transaction_rows([dict(rows[0], txn_type="Not A Word")])
    except SystemExit:
        pass
    else:
        raise Fail("check_transaction_rows accepted a word outside the vocabulary")
    # the full live domain, denominators printed
    pr, n = live_problems(mod, con, census3)
    print("domain Inflection %s" % (n,))
    need(n["live_descriptions"] == 47 and n["contract_descriptions"] == 48, "the live census is not the 47 descriptions / the contract's 48 the ruling names: %s" % (n,))
    need(not pr, "%d Inflection live descriptions misread (first: %s)" % (len(pr), "; ".join(pr[:4])))
    # the collision refusal
    bad = copy.deepcopy(words)
    row = next(m for m in bad["source_mapping"] if m["firm"] == "inflection")
    bad["source_mapping"].append(dict(row, source_value=row["source_value"] + " "))
    try:
        mod.normalize_trn(frame([base_row()]), "inflection", words=bad)
    except SystemExit as e:
        need("collide" in str(e).lower() or "normalise to one key" in str(e).lower(), "the refusal for a key collision must say collide: %s" % e)
    else:
        raise Fail("the Inflection producer accepted two descriptions that normalise to one key")
    # another firm refused; the writer makes no S3 call on upload=False
    try:
        mod.normalize_trn(frame([base_row()]), "someone_else")
    except SystemExit:
        pass
    else:
        raise Fail("normalize_trn accepted another firm")
    same_day = [r for r in rows if str(r["business_date"]) == "2026-03-10"]
    res = mod.emit_transaction_day(object(), same_day, "inflection", "2026-03-10", upload=False, excluded=excluded, price_reasons=reasons)
    need(res.get("landed") is False and res.get("rows") == len(same_day), "emit_transaction_day(upload=False) must make no call and land nothing")
    try:
        mod.emit_transaction_day(object(), rows, "inflection", "2026-03-10", upload=False)
    except SystemExit as e:
        need("partition" in str(e).lower(), "the refusal of a row under another partition day must say partition: %s" % e)
    else:
        raise Fail("emit_transaction_day accepted a row whose business_date is not the partition day")
    m49 = load_module(root, F49, "account_transaction_49_for_inflection_check")
    need(callable(getattr(m49, "normalise_key", None)), "account_transaction.normalise_key is missing")


def selftest():
    bad = 0
    count = 0

    def arm(name, got, want):
        nonlocal bad, count
        count += 1
        if got != want:
            bad += 1
            print("SELFTEST FAIL %s: got %r want %r" % (name, got, want))

    arm("names", test_names("def test_a_b():\n    pass\ndef helper():\n    pass"), ["test a b"])
    arm("words-red", missing_words(["status"], TITLE_WORDS), list(TITLE_WORDS[1:]))
    arm("fund-family-in-base-row", base_row()["fundFamilyName"].strip(), "Test Fund Family")
    arm("pytest", pytest_counts("3 passed in 1s"), (3, 0, 0))
    arm("columns", (len(COLUMNS), COLUMNS[-1]), (18, "source_action_raw"))
    arm("statuses", len(STATUSES), 6)
    r = base_row()
    arm("base-no-avgprice", "avgPrice" in r, False)
    m_ok = {"opal_type": "Buy", "flow_class": "INTERNAL"}
    ok = {"coverage": "MEASURED", "txn_type": "Buy", "flow_class": "INTERNAL"}
    arm("judge-green", judge(ok, "d", m_ok), None)
    arm("judge-not-in", judge(dict(ok, coverage=NOT_IN), "d", m_ok), "description 'd' read CODE_NOT_IN_MAPPING")
    arm("judge-flow", judge(dict(ok, flow_class="FEE"), "d", m_ok), "description 'd' flow_class 'FEE', the mapping says 'INTERNAL'")
    arm("judge-unmapped", judge({"coverage": BY_TABLE, "txn_type": UNMAPPED, "flow_class": "INTERNAL"}, "d", {"opal_type": UNMAPPED, "flow_class": "INTERNAL"}), None)
    arm("judge-unmapped-red", judge(ok, "d", {"opal_type": UNMAPPED, "flow_class": "INTERNAL"}), "description 'd' is UNMAPPED in the table but read MEASURED")

    class Stub:
        @staticmethod
        def normalize_trn(fr, firm, words=None):
            return [{"coverage": NOT_IN, "txn_type": UNMAPPED, "flow_class": "UNRESOLVED", "source_action_raw": None} for _ in range(len(fr))]

    con = {"source_mapping": [{"firm": "inflection", "source_value": "Buy Exchange", "opal_type": "Buy", "flow_class": "INTERNAL"}]}
    c3 = {"firms": {"inflection": {"values": {"transactionDescription": {"Buy Exchange": 5}}}}}
    pr, n = live_problems(Stub, con, c3)
    arm("live-red", (len(pr) > 0, n["lines"], n["domain"]), (True, 3, 1))

    class Good:
        @staticmethod
        def normalize_trn(fr, firm, words=None):
            return [{"coverage": "MEASURED", "txn_type": "Buy", "flow_class": "INTERNAL", "source_action_raw": r["transactionDescription"]}
                    for r in fr.to_dict("records")]

    arm("live-green", live_problems(Good, con, c3)[0], [])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    if ac != "DBF132-1-AC3":
        print("%s FAIL (unknown criterion)" % ac)
        return 1
    try:
        ac_all(root)
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
