"""IRPT_DASHBD round 134 (derived from the round-131 checker; the REGRESSION LEG of p134_dates.py): the ONE KEY NORMALISATION and the COTTONWOOD / 49 FINANCIAL producers
on the 19-column schema.

  DB-f-1701 (~1701) CTO round-130 ruling (msg 9245): the mapping's keys and the producer's lookup use ONE function (strip surrounding whitespace, nothing
                    else, case kept), defined once in `account_transaction.py` (`normalise_key`, `pair_key`, `keyed_map`) and imported by the
                    Cottonwood producer; every row carries `source_action_raw`, the source value exactly as received (an 18th column); two source
                    values that normalise to one key are a finding and the loader REFUSES. This checker feeds the producers EVERY DISTINCT live
                    source value of the issuer's committed live censuses (Cottonwood's 87 Actions and 33 pairs exactly as received, 49 Financial's
                    160 codes) and requires each to look up to its mapping row and never read CODE_NOT_IN_MAPPING unless the table rules it UNMAPPED.
                    DBF131-1-AC2 (the key function; the full live domain per producer, denominators printed; the tests of both producers)

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
D = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/2.0.0_SA_COO~F2/"
CENSUS49 = D + "R124_LIVE_SILVER_CENSUS_49F.json"
CENSUS3 = D + "R128_LIVE_SOURCE_CENSUS_3FIRMS.json"
CW = "data/assets/scripts/gold/irpt_reporting/account_transaction_cottonwood.py"
CW_TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_account_transaction_cottonwood.py"
F49 = "data/assets/scripts/gold/irpt_reporting/account_transaction.py"
F49_TEST = "data/assets/scripts/gold/irpt_reporting/tests/test_account_transaction.py"
UNMAPPED = "UNMAPPED"
NOT_IN = "CODE_NOT_IN_MAPPING"
BY_TABLE = "UNMAPPED_BY_TABLE"
COLUMNS = ("firm", "account_id", "business_date", "trade_date", "settle_date", "action", "txn_type", "symbol", "asset_name", "units",
           "price", "amount", "fee", "custodian", "flow_class", "source_txn_id", "coverage", "source_action_raw", "business_date_claim")
TITLE_WORDS = ("pair", "action", "flow", "fee", "settle", "identifier", "custodian", "external", "schema", "unmapped", "new code", "vocabulary",
               "whitespace", "every live", "collide", "raw")


class Fail(Exception):
    pass


def need(cond, msg):
    if not cond:
        raise Fail(msg)


def norm(v):
    """The checker's own reference for the ruled function: strip surrounding whitespace, nothing else (case kept)."""
    return v.strip()


def pair_norm(v):
    return " | ".join(norm(part) for part in v.split(" | ", 1))


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


def cw_frame(rows):
    import pandas as pd
    return pd.DataFrame(rows)


def base_row(**k):
    row = {"AccountID": "00000000001", "Trade Date": "2026-03-10", "Settle Date": "2026-03-12", "Return Date": "2026-03-10",
           "Transaction Type": "T", "Transaction Sub Type": "S", "Action": "A", "External Flow": "None", "Units": 4.0, "Price": 2.5,
           "Market Value": 10.0, "Transaction Fee": 1.0, "Account Fee": 0.5, "Symbol": "TEST", "Asset Name": "Test Asset",
           "Custodian": "  Some Custodian ", "TransactionID": " TID-1 "}
    row.update(k)
    return row


def line49(fee_cols, **kw):
    base = {"account_id": "0000000001", "business_date": "2026-01-05", "trade_date": "2026-01-05", "tran_srcde": "CHE", "tr_cd": "FC",
            "sb_cd": "XX", "quantity": 10.0, "price": 2.5, "gross_amount": 25.0, "debit_credit": "C", "ticker_symbol": "TEST1",
            "cusip": "000000000", "settlmnt_date": "2026-01-07", "cashiering_transaction_identifier": "ID-TEST-0"}
    base.update({c: None for c in fee_cols})
    base.update(kw)
    return base


def judge(out, kind, sv, mrow, word_field, word_col):
    """One producer row against its mapping row: never CODE_NOT_IN_MAPPING; UNMAPPED_BY_TABLE iff the table rules it UNMAPPED; otherwise the
    mapping's own word. Returns a problem string or None."""
    if out["coverage"] == NOT_IN:
        return "%s %r read CODE_NOT_IN_MAPPING" % (kind, sv)
    if mrow[word_field] == UNMAPPED:
        return None if out["coverage"] == BY_TABLE else "%s %r is UNMAPPED in the table but read %s" % (kind, sv, out["coverage"])
    if out["coverage"] != "MEASURED":
        return "%s %r read %s, not MEASURED" % (kind, sv, out["coverage"])
    if out[word_col] != mrow[word_field]:
        return "%s %r gave %r, the mapping says %r" % (kind, sv, out[word_col], mrow[word_field])
    return None


def live_cottonwood_problems(mod, con, census3):
    """Every DISTINCT live Action (87) and pair (33) of the committed census, EXACTLY AS RECEIVED, and each Action again padded with blanks."""
    cm = con["cottonwood_mapping"]
    by_act = {norm(r["source_value"]): r for r in cm["actions"]}
    by_pair = {pair_norm(r["source_value"]): r for r in cm["type_pairs"]}
    live = census3["firms"]["cottonwood"]
    acts = list(live["values"]["Action"])
    pairs = ["%s | %s" % (p["transaction_type"], p["transaction_sub_type"]) for p in live["pairs"]]
    base_pair = next(r for r in cm["type_pairs"] if r["opal_type"] != UNMAPPED)
    bt, bs = base_pair["source_value"].split(" | ", 1)
    base_act = next(r["source_value"] for r in cm["actions"] if r["opal_action"] != UNMAPPED)
    rows, meta = [], []
    pr = []
    for a in acts:
        for variant in (a, norm(a) + " ", " " + norm(a)):
            rows.append(base_row(**{"Transaction Type": bt, "Transaction Sub Type": bs, "Action": variant}))
            meta.append(("action", a, by_act.get(norm(a)), "opal_action", "action", variant))
    for p in pairs:
        t, st = p.split(" | ", 1)
        rows.append(base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": base_act}))
        meta.append(("pair", p, by_pair.get(pair_norm(p)), "opal_type", "txn_type", None))
    out = mod.normalize_trn(cw_frame(rows), "cottonwood")
    need(len(out) == len(rows), "normalize_trn did not return one row per input row")
    for o, (kind, sv, mrow, wf, wc, variant) in zip(out, meta):
        if mrow is None:
            pr.append("%s %r: the contract has no row for the live value" % (kind, sv))
            continue
        bad = judge(o, kind, sv, mrow, wf, wc)
        if bad:
            pr.append(bad)
        if kind == "action" and o["source_action_raw"] != variant:
            pr.append("action %r: source_action_raw %r is not the value as received %r" % (sv, o["source_action_raw"], variant))
    padded = sum(1 for a in acts if a != norm(a))
    return pr, {"live_actions": len(acts), "live_pairs": len(pairs), "live_actions_with_blank_padding": padded, "lines": len(rows)}


def live_49f_problems(mod, con, census49, fee_cols):
    """Every DISTINCT live 49 Financial tran_srcde (160) of the committed census through the producer."""
    by_code = {norm(m["source_value"]): m for m in con["source_mapping"] if m["firm"] == "49financial"}
    codes = list(census49["codes"])
    frame = cw_frame([line49(fee_cols, tran_srcde=c) for c in codes])
    out = mod.normalize_trn(frame, mod.supported_firm())
    need(len(out) == len(codes), "the 49 Financial normalize_trn did not return one row per input row")
    pr = []
    for o, c in zip(out, codes):
        m = by_code.get(norm(c))
        if m is None:
            pr.append("code %r: the contract has no row for the live value" % c)
            continue
        bad = judge(o, "code", c, m, "opal_type", "txn_type")
        if bad:
            pr.append(bad)
        elif m["opal_type"] != UNMAPPED and o["flow_class"] != m["flow_class"]:
            pr.append("code %r: flow_class %r, the mapping says %r" % (c, o["flow_class"], m["flow_class"]))
        if o["source_action_raw"] != c:
            pr.append("code %r: source_action_raw %r is not the value as received" % (c, o["source_action_raw"]))
    return pr, {"live_codes": len(codes), "lines": len(codes)}


def collision_problems(mod_cw, mod49, words):
    """A words file where two source values normalise to one key must REFUSE at load (a rule-24 finding), for both producers."""
    pr = []
    bad_cw = copy.deepcopy(words)
    first = bad_cw["cottonwood_mapping"]["actions"][0]
    bad_cw["cottonwood_mapping"]["actions"].append(dict(first, source_value=first["source_value"] + " "))
    try:
        mod_cw.normalize_trn(cw_frame([base_row()]), "cottonwood", words=bad_cw)
    except SystemExit as e:
        if "collide" not in str(e).lower() and "normalise to one key" not in str(e).lower():
            pr.append("the Cottonwood refusal for a key collision does not say collide: %s" % e)
    else:
        pr.append("the Cottonwood producer accepted two Action values that normalise to one key")
    bad_49 = copy.deepcopy(words)
    row = next(m for m in bad_49["source_mapping"] if m["firm"] == "49financial")
    bad_49["source_mapping"].append(dict(row, source_value=row["source_value"] + " "))
    try:
        fee_cols = tuple(words["fee_basis"]["49financial"]["columns"])
        mod49.normalize_trn(cw_frame([line49(fee_cols)]), mod49.supported_firm(), words=bad_49)
    except SystemExit as e:
        if "collide" not in str(e).lower() and "normalise to one key" not in str(e).lower():
            pr.append("the 49 Financial refusal for a key collision does not say collide: %s" % e)
    else:
        pr.append("the 49 Financial producer accepted two codes that normalise to one key")
    return pr


def ac_all(root):
    con = json.loads((Path(root) / CONTRACT).read_text(encoding="utf-8"))
    words = json.loads((Path(root) / "data/assets/scripts/gold/irpt_reporting/transaction_words.json").read_text(encoding="utf-8"))
    census3 = json.loads((Path(root) / CENSUS3).read_text(encoding="utf-8"))
    census49 = json.loads((Path(root) / CENSUS49).read_text(encoding="utf-8"))
    names = test_names((Path(root) / CW_TEST).read_text(encoding="utf-8")) if (Path(root) / CW_TEST).is_file() else []
    need(names, "missing test file " + CW_TEST)
    names49 = test_names((Path(root) / F49_TEST).read_text(encoding="utf-8"))
    mw = missing_words(names + names49, TITLE_WORDS)
    need(not mw, "the test names of the two producers lack " + repr(mw))
    run_pytest(root, CW_TEST, 46)
    run_pytest(root, F49_TEST, 44)
    m49 = load_module(root, F49, "account_transaction_49_under_check")
    mod = load_module(root, CW, "account_transaction_cottonwood_under_check")
    # the ONE function, defined once and shared
    for fn in ("normalise_key", "pair_key", "keyed_map"):
        need(callable(getattr(m49, fn, None)), "account_transaction.%s is missing (the one key function, defined once)" % fn)
    need(m49.normalise_key("  Buy Money Market ") == "Buy Money Market" and m49.normalise_key("BUY") == "BUY" and m49.normalise_key(None) is None,
         "normalise_key must strip surrounding whitespace and nothing else (case kept; None stays None)")
    need(m49.pair_key("T ", " S") == "T | S", "pair_key must join the two normalised parts with ' | '")
    cw_src = (Path(root) / CW).read_text(encoding="utf-8")
    need("def normalise_key" not in cw_src and "def pair_key" not in cw_src and "def keyed_map" not in cw_src,
         "the Cottonwood producer re-implements the key function: it must import it")
    # the schema: 18 columns, names, order, hash
    fields = [(f.name, str(f.type)) for f in mod.ARROW_SCHEMA]
    need([n for n, _ in fields] == list(COLUMNS) and schema_hash_of(fields) == con["schema_hash"], "ARROW_SCHEMA is not the contract's (names, order, hash)")
    need([f.name for f in m49.ARROW_SCHEMA] == list(COLUMNS), "the 49 Financial ARROW_SCHEMA is not the contract's 19 columns")
    # a small set of exact behaviours
    cm = con["cottonwood_mapping"]
    pairs = {r["source_value"]: r for r in cm["type_pairs"]}
    actions = {r["source_value"]: r for r in cm["actions"]}
    none_pair = next(k for k, r in pairs.items() if r["opal_type"] != UNMAPPED and r["flow_class_none"] is not None)
    t, st = none_pair.split(" | ", 1)
    act = next(k for k, r in actions.items() if r["opal_action"] != UNMAPPED)
    rows = mod.normalize_trn(cw_frame([
        base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": act}),
        base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": act, "External Flow": "Contribution"}),
        base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": act, "External Flow": "Withdrawal"}),
        base_row(**{"Transaction Type": t, "Transaction Sub Type": st, "Action": None, "Symbol": "  ", "TransactionID": ""}),
        base_row(**{"Transaction Type": "ZZ_NEW", "Transaction Sub Type": "ZZ_NEW", "Action": act}),
    ]), "cottonwood")
    need(isinstance(rows, list) and len(rows) == 5, "normalize_trn did not return one row per input row")
    for r in rows:
        need(list(r.keys()) == list(COLUMNS), "a row's keys are not the contract's columns in order")
        need(r["firm"] == "cottonwood" and r["custodian"] == "some custodian", "firm or the lower-cased, stripped custodian is wrong")
        need(str(r["settle_date"]) == "2026-03-12" and r["fee"] == 1.5, "settle_date or the stated fee sum is wrong")
    a, b, c, d, e = rows
    need(a["txn_type"] == pairs[none_pair]["opal_type"] and a["flow_class"] == pairs[none_pair]["flow_class_none"]
         and a["coverage"] == "MEASURED" and a["action"] == actions[act]["opal_action"], "the mapped row is wrong")
    need(a["source_txn_id"] == "TID-1" and a["symbol"] == "TEST", "identifier or symbol not read and stripped")
    need(a["source_action_raw"] == act and d["source_action_raw"] is None and e["source_action_raw"] == act,
         "source_action_raw must be the Action exactly as received (None when the line has none)")
    need(b["flow_class"] == "EXTERNAL_IN" and c["flow_class"] == "EXTERNAL_OUT", "the External Flow rule is wrong")
    need(d["symbol"] is None and d["source_txn_id"] is None, "an empty symbol or identifier must be null")
    need(d["action"] == con["type_action"][d["txn_type"]], "a line with no Action must derive its action from the pair")
    need(e["txn_type"] == UNMAPPED and e["flow_class"] == "UNRESOLVED" and e["coverage"] == NOT_IN and e["action"] is None,
         "a pair the mapping lacks must read UNMAPPED, UNRESOLVED, CODE_NOT_IN_MAPPING, counted and never dropped")
    mod.check_transaction_rows(rows)
    try:
        mod.check_transaction_rows([dict(rows[0], txn_type="Not A Word")])
    except SystemExit:
        pass
    else:
        raise Fail("check_transaction_rows accepted a word outside the vocabulary")
    need(m49.custodian() == m49.custodian().lower(), "the 49 Financial custodian is not lower-cased")
    # the full live domain, denominators printed (CTO msg 9245 item 3)
    pr_cw, n_cw = live_cottonwood_problems(mod, con, census3)
    fee_cols = tuple(con["fee_basis"]["49financial"]["columns"])
    pr_49, n_49 = live_49f_problems(m49, con, census49, fee_cols)
    print("domain Cottonwood %s" % (n_cw,))
    print("domain 49 Financial %s" % (n_49,))
    need(n_cw["live_actions"] == 87 and n_cw["live_pairs"] == 33 and n_cw["live_actions_with_blank_padding"] == 3,
         "the Cottonwood live census is not the 87 Actions / 33 pairs / 3 padded the ruling names: %s" % (n_cw,))
    need(n_49["live_codes"] == 160, "the 49 Financial live census is not the 160 codes the ruling names: %s" % (n_49,))
    need(not pr_cw, "%d Cottonwood live values misread (first: %s)" % (len(pr_cw), "; ".join(pr_cw[:4])))
    need(not pr_49, "%d 49 Financial live codes misread (first: %s)" % (len(pr_49), "; ".join(pr_49[:4])))
    col = collision_problems(mod, m49, words)
    need(not col, "; ".join(col))


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
    arm("words-green", missing_words(["pair action flow fee settle identifier custodian external schema unmapped new code vocabulary whitespace "
                                      "every live collide raw"], TITLE_WORDS), [])
    arm("words-red", missing_words(["pair"], TITLE_WORDS), list(TITLE_WORDS[1:]))
    arm("pytest", pytest_counts("2 failed, 21 passed in 1s"), (21, 2, 0))
    arm("hash-order", schema_hash_of([("a", "string"), ("b", "double")]) == schema_hash_of([("b", "double"), ("a", "string")]), True)
    arm("columns", (len(COLUMNS), COLUMNS[-1]), (19, "business_date_claim"))
    arm("norm", (norm(" a b "), norm("BUY"), pair_norm("T | S ")), ("a b", "BUY", "T | S"))
    mrow = {"opal_action": "Trade", "opal_type": "Buy"}
    arm("judge-green", judge({"coverage": "MEASURED", "action": "Trade"}, "action", "x", mrow, "opal_action", "action"), None)
    arm("judge-not-in", judge({"coverage": NOT_IN, "action": None}, "action", "x", mrow, "opal_action", "action"),
        "action 'x' read CODE_NOT_IN_MAPPING")
    arm("judge-wrong-word", judge({"coverage": "MEASURED", "action": "Other"}, "action", "x", mrow, "opal_action", "action"),
        "action 'x' gave 'Other', the mapping says 'Trade'")
    arm("judge-unmapped-ok", judge({"coverage": BY_TABLE, "action": None}, "code", "x", {"opal_type": UNMAPPED}, "opal_type", "txn_type"), None)
    arm("judge-unmapped-red", judge({"coverage": "MEASURED", "txn_type": "Buy"}, "code", "x", {"opal_type": UNMAPPED}, "opal_type", "txn_type"),
        "code 'x' is UNMAPPED in the table but read MEASURED")

    class Stub:
        @staticmethod
        def normalize_trn(frame, firm, words=None):
            return [{"coverage": NOT_IN, "action": None, "txn_type": UNMAPPED, "source_action_raw": None} for _ in range(len(frame))]

    census3 = {"firms": {"cottonwood": {"values": {"Action": {"A ": 3}}, "pairs": [{"transaction_type": "T", "transaction_sub_type": "S"}]}}}
    con = {"cottonwood_mapping": {"type_pairs": [{"source_value": "T | S", "opal_type": "Buy", "flow_class_none": "INTERNAL"}],
                                  "actions": [{"source_value": "A ", "opal_action": "Trade"}]}}
    pr, cnt = live_cottonwood_problems(Stub, con, census3)
    arm("live-red", (len(pr) > 0, cnt["live_actions_with_blank_padding"], cnt["lines"]), (True, 1, 4))

    class Good:
        @staticmethod
        def normalize_trn(frame, firm, words=None):
            out = []
            for rec in frame.to_dict("records"):
                out.append({"coverage": "MEASURED", "action": "Trade", "txn_type": "Buy", "source_action_raw": rec["Action"]})
            return out

    arm("live-green", live_cottonwood_problems(Good, con, census3)[0], [])
    print("selftest %s" % ("FAIL" if bad else "PASS (%d arms)" % count))
    return 1 if bad else 0


def main(argv):
    if len(argv) == 2 and argv[1] == "--selftest":
        return selftest()
    if len(argv) != 3:
        print(__doc__)
        return 2
    root, ac = argv[1], argv[2]
    if ac != "DBF131-1-AC2":
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
