"""IRPT_ANLREQ AR-g-100 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g100_checks.py g100     the Opal producer runs the swap pass on UNRESOLVED holdings (direct cases on fakes: the replacement, the
                                     left-out holding, the disclosures and settings, the refusals, the unchanged paths), and the eight named
                                     new tests exist and pass
    python ar_g100_checks.py regress   six existing test files (run one at a time) still pass, 67 tests in all, and the branch changed only
                                     the cell's own files (measured against the merge-base with box/dell2)

Prints one RESULT line: AR-G100-OK / AR-G100-FAIL or AR-G100-REGRESS-OK / AR-G100-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

R = "infra/aws/lambda/investor-reporting/"
RES = R + "ycharts/research/"
T = RES + "tests/"
NEW_TESTS = {
    T + "test_opal_producer_swap.py": [
        "test_an_unresolved_holding_is_replaced_before_anything_is_classified",
        "test_every_substitution_is_named_first_in_the_disclosures_and_the_settings_say_which_pool",
        "test_a_holding_with_no_class_is_left_out_and_named_not_analysed_and_the_run_goes_on",
        "test_a_run_with_nothing_analysable_left_refuses_before_any_write",
        "test_without_a_swap_store_an_unresolved_holding_refuses_as_it_always_did_and_the_read_is_unchanged",
        "test_a_run_with_the_swap_store_and_no_unresolved_holding_is_byte_for_byte_the_run_without_it",
        "test_a_stale_pool_still_swaps_and_the_disclosure_and_settings_say_so",
        "test_the_packager_path_reads_the_same_effective_rows_and_the_two_request_sizes_agree",
    ],
}
REGRESS = [T + "test_opal_producer.py", T + "test_opal_producer_prices.py", T + "test_opal_producer_benchmark.py",
           T + "test_opal_producer_page_wording.py", T + "test_opal_packager.py", T + "test_runner_unresolved.py"]
MIN_TOTAL = 67
OWN_FILES = (RES + "opal_producer.py", T + "test_opal_producer_swap.py")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
EQ = {"asset_class": "equity", "sub_asset_class": "Fixture Large Blend"}


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_run(targets):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def cases():
    here = Path(T).resolve()
    for p in (here, here.parent, here.parents[1] / "generate", here.parents[1] / "session", here.parents[4] / "lib"):
        sys.path.insert(0, str(p))
    import opal_producer as op
    import runner
    import swap_pass
    import test_opal_producer as tp
    import tempfile
    from boto3.dynamodb.types import TypeSerializer
    out = []

    def case(name, ok, why=""):
        out.append((name, bool(ok), why))

    tmp = Path(tempfile.mkdtemp(prefix="g100_"))

    def world(extra, unresolved=True):
        data = json.loads(json.dumps(tp._json("frozen_input.json")))
        for symbol, amount in extra:
            row = {"security_id": symbol, "original": {"symbol": symbol, "quantity": {"value": amount, "unit": "USD"}}}
            if unresolved:
                row["resolution"] = "UNRESOLVED"
            data["resolved"]["document"]["rows"].append(row)
        blob = json.dumps(data).encode()
        record = {"composition_ref": {"artifact_id": "art-1", "sha256": hashlib.sha256(blob).hexdigest()}}
        rid = tp.REQ["request_id"]
        items = {(tp.FIRM, "analysis#%s#1" % rid): {"tenant": {"S": tp.FIRM}, "request_revision": {"S": "analysis#%s#1" % rid}, "record": {"S": json.dumps(record)}},
                 (tp.FIRM, "ARTIFACT#art-1"): {"tenant": {"S": tp.FIRM}, "request_revision": {"S": "ARTIFACT#art-1"},
                                               "blob": TypeSerializer().serialize({"bucket": "opal-data-irpt", "key": "k/comp.json", "version_id": "v9"})}}
        return tp.HostDynamo(items), tp.HostS3({("opal-data-irpt", "k/comp.json", "v9"): blob})

    def pool(as_of="2026-10-01", name="pool.json"):
        rows = [{"ticker": t, "asset_class": "equity", "sub_asset_class": "Fixture Large Blend"} for t in ("AAA", "DDD", "EEE")]
        path = tmp / name
        path.write_text(json.dumps({"schema": swap_pass.SCHEMA, "pool_as_of": as_of, "pool_claim": "held", "rows": rows}), encoding="utf-8")
        return swap_pass.load_pool(str(path), "2026-10-06")

    days = {"AAA": 300, "DDD": 900, "EEE": 900}

    class Classifier(tp.FakeClassifier):
        def __init__(self, extra):
            super().__init__()
            self.rows.update(extra)

    known = {"QQQ": dict(ticker="QQQ", name="Client Fund", **EQ), "DDD": dict(ticker="DDD", name="Fixture Delta", **EQ)}

    def stores(w, classifier=None, **over):
        s = tp.make_stores()
        s["dynamodb"], s["s3"] = w
        s["classifier"] = classifier or Classifier(known)
        s["swap"] = {"pool": pool(), "history_days": days.get}
        s.update(over)
        return s

    # W1: the replacement
    s1 = stores(world([("QQQ", "250")]))
    swap_obj = s1["swap"]["pool"]
    snapshot = json.dumps(swap_obj, sort_keys=True)
    rec = op.produce(tp.REQ, tp.FIRM, s1)
    case("W1-effective-rows-in-place-with-the-clients-amount", rec["holdings"]["rows"] == [{"ticker": "AAA", "amount": "500"}, {"ticker": "BBB", "amount": "300"},
                                                                                      {"ticker": "CCC", "amount": "200"}, {"ticker": "DDD", "amount": "250"}], str(rec["holdings"]["rows"]))
    case("W1-record-swaps-without-amounts", len(rec.get("swaps", [])) == 1 and rec["swaps"][0]["proxy_for"] == "QQQ" and rec["swaps"][0]["proxy"] == "DDD"
         and "250" not in json.dumps(rec["swaps"]), str(rec.get("swaps"))[:160])
    written = json.loads(tp.stored(s1, "run.json")["Body"])
    case("W1-run-json-carries-the-swaps", written["swaps"] == json.loads(json.dumps(rec["swaps"])))
    case("W1-pool-not-mutated", json.dumps(swap_obj, sort_keys=True) == snapshot)
    doc = s1["reports"].persisted[0]["report"]
    case("W2-disclosure-order-pricing-off", [d["disclosure_id"] for d in doc["disclosures"]] == ["SWAP", "NO_PRICING", "WEIGHTING"], str([d["disclosure_id"] for d in doc["disclosures"]]))
    case("W2-disclosure-words", doc["disclosures"][0]["text"] == "QQQ is replaced by DDD (same asset class and sub asset class; longest Yahoo history, 900 days).", doc["disclosures"][0]["text"])
    case("W2-settings", doc["effective_inputs"]["settings"].get("swap") == {"pool_as_of": "2026-10-01", "pool_claim": "held", "pool_stale": False, "swapped": 1, "left_out": 0},
         str(doc["effective_inputs"]["settings"].get("swap")))
    try:
        import jsonschema
        schema = json.loads(Path(tp.SCHEMA_V2).read_text(encoding="utf-8"))
        errors = list(jsonschema.Draft202012Validator(schema).iter_errors(doc)) if hasattr(jsonschema, "Draft202012Validator") else []
        case("W2-document-validates-against-the-v2-schema", not errors, str(errors[:1])[:200])
    except ImportError:
        case("W2-document-validates-against-the-v2-schema", True, "jsonschema absent: skipped")
    case("W3-the-client-ticker-is-not-in-the-computed-holdings", all(r["ticker"] != "QQQ" for r in rec["holdings"]["rows"]) and "QQQ" in s1["classifier"].calls and "DDD" in s1["classifier"].calls)
    # W4: two swapped holdings keep the row order and are named in row order
    s4 = stores(world([("QQQ", "10"), ("BREIT", "20")]))
    rec4 = op.produce(tp.REQ, tp.FIRM, s4)
    texts = [d["text"] for d in s4["reports"].persisted[0]["report"]["disclosures"] if d["disclosure_id"] == "SWAP"]
    case("W4-disclosures-in-row-order", len(texts) == 2 and texts[0].startswith("QQQ is replaced by DDD") and texts[1] == "BREIT is not analysed; Opal Staff will manage the replacement.", str(texts))
    case("W4-counts", s4["reports"].persisted[0]["report"]["effective_inputs"]["settings"]["swap"]["swapped"] == 1 and s4["reports"].persisted[0]["report"]["effective_inputs"]["settings"]["swap"]["left_out"] == 1)
    case("W4-left-out-row-is-gone", [r["ticker"] for r in rec4["holdings"]["rows"]] == ["AAA", "BBB", "CCC", "DDD"])
    # W5: the explicit classify override is used
    asked = []
    s5 = stores(world([("OTHER", "5")]), classifier=tp.FakeClassifier())
    s5["swap"]["classify"] = lambda sym: (asked.append(sym), dict(EQ))[1]
    op.produce(tp.REQ, tp.FIRM, s5)
    case("W5-classify-override-used-for-the-missing-ticker", asked == ["OTHER"] and s5["swap"]["classify"] is not None, str(asked))
    # W6: stale pool
    s6 = stores(world([("QQQ", "250")]))
    s6["swap"]["pool"] = pool(as_of="2026-08-01", name="old.json")
    op.produce(tp.REQ, tp.FIRM, s6)
    d6 = s6["reports"].persisted[0]["report"]
    case("W6-stale-pool-says-so", d6["disclosures"][0]["text"].endswith("The replacement pool was built on 2026-08-01, 66 days before this run, which is older than 30 days.") and d6["effective_inputs"]["settings"]["swap"]["pool_stale"] is True, d6["disclosures"][0]["text"][-90:])
    # W7: pricing on: the swap disclosures lead the priced list
    s7 = stores(world([("QQQ", "250")]), pricing=True, as_of="2026-10-05", price_readers={"estate": lambda symbol, start, end: []})
    op.produce(tp.REQ, tp.FIRM, s7)
    ids7 = [d["disclosure_id"] for d in s7["reports"].persisted[0]["report"]["disclosures"]]
    case("W7-swap-first-in-the-priced-disclosures", ids7[0] == "SWAP" and ids7[-1] == "WEIGHTING" and "BENCHMARK" in ids7, str(ids7))
    # W8: refusals
    w8 = world([("BREIT", "50")])
    data8 = json.loads(w8[1].blobs[("opal-data-irpt", "k/comp.json", "v9")])
    data8["resolved"]["document"]["rows"] = [r for r in data8["resolved"]["document"]["rows"] if r.get("resolution") == "UNRESOLVED"]
    blob8 = json.dumps(data8).encode()
    w8[1].blobs[("opal-data-irpt", "k/comp.json", "v9")] = blob8
    key8 = (tp.FIRM, "analysis#%s#1" % tp.REQ["request_id"])
    rec8 = json.loads(w8[0].items[key8]["record"]["S"])
    rec8["composition_ref"]["sha256"] = hashlib.sha256(blob8).hexdigest()
    w8[0].items[key8]["record"] = {"S": json.dumps(rec8)}
    s8 = stores(w8, classifier=tp.FakeClassifier())
    try:
        op.produce(tp.REQ, tp.FIRM, s8)
        refused = "NO-REFUSAL"
    except op.ProducerRefused as exc:
        refused = str(exc)
    case("W8-nothing-left-refuses-before-any-write", refused == "NO_ANALYSABLE_HOLDINGS" and s8["objects"].puts == [] and s8["reports"].persisted == [], refused)
    for tag, bad in (("no-pool", {"history_days": days.get}), ("no-port", {"pool": pool()}), ("not-callable", {"pool": pool(), "history_days": 5})):
        s = stores(world([("QQQ", "1")]))
        s["swap"] = bad
        try:
            op.produce(tp.REQ, tp.FIRM, s)
            r = "NO-REFUSAL"
        except op.ProducerRefused as exc:
            r = str(exc)
        case("W8-malformed-swap-store-" + tag, r == "store required: swap" and s["objects"].puts == [], r)
    # W9: unchanged paths
    seen = []
    real = runner.read_holdings

    def spy(*a, **k):
        seen.append(k)
        return real(*a, **k)
    runner.read_holdings = spy
    try:
        s9 = stores(world([("QQQ", "250")]))
        del s9["swap"]
        try:
            op.produce(tp.REQ, tp.FIRM, s9)
            r9 = "NO-REFUSAL"
        except runner.HoldingsUnreadable as exc:
            r9 = str(exc)
        case("W9-no-swap-store-refuses-unresolved-as-before", r9 == "UNRESOLVED_ROW" and seen == [{"revision": 1}], "%s %s" % (r9, seen))
        seen.clear()
        s9b = tp.make_stores()
        s9b["swap"] = {"pool": pool(), "history_days": days.get}
        op.produce(tp.REQ, tp.FIRM, s9b)
        case("W9-swap-store-asks-the-reader-to-allow-unresolved", seen == [{"revision": 1, "allow_unresolved": True}], str(seen))
    finally:
        runner.read_holdings = real
    ticks = [1.0, 2.0, 3.0, 4.0]
    a = op.produce(tp.REQ, tp.FIRM, tp.make_stores(timer=iter(ticks).__next__))
    sb = tp.make_stores(timer=iter(ticks).__next__)
    sb["swap"] = {"pool": pool(), "history_days": days.get}
    b = op.produce(tp.REQ, tp.FIRM, sb)
    case("W9-no-unresolved-row-is-byte-for-byte-today", "swaps" not in b and json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True))
    case("W9-no-swap-keys-without-a-swap", "swap" not in sb["reports"].persisted[0]["report"]["effective_inputs"]["settings"] and
         [d["disclosure_id"] for d in sb["reports"].persisted[0]["report"]["disclosures"]] == ["NO_PRICING", "WEIGHTING"])
    # W10: the packager path
    _m, holdings, run_doc, classified, _h = op._read_stage(tp.REQ, tp.FIRM, stores(world([("QQQ", "250")])))
    case("W10-read-stage-gives-the-effective-rows", holdings["rows"] == [{"ticker": "AAA", "amount": "500"}, {"ticker": "BBB", "amount": "300"}, {"ticker": "CCC", "amount": "200"}, {"ticker": "DDD", "amount": "250"}]
         and run_doc["swaps"][0]["proxy"] == "DDD" and "DDD" in classified, str(holdings["rows"])[:200])
    # W11: determinism
    r1, r2 = op.produce(tp.REQ, tp.FIRM, stores(world([("QQQ", "250")], True), timer=iter(ticks).__next__)), op.produce(tp.REQ, tp.FIRM, stores(world([("QQQ", "250")], True), timer=iter(ticks).__next__))
    case("W11-deterministic", json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True))
    return out


def g100():
    try:
        out = cases()
    except Exception as exc:
        print("AR-G100-FAIL the cases could not run: %s: %s" % (type(exc).__name__, str(exc)[:200]))
        return 1
    failed = [(n, why) for n, ok, why in out if not ok]
    for name, why in failed:
        print("CASE-FAIL", name, why)
    bad = list(failed)
    for path, names in NEW_TESTS.items():
        text = Path(path).read_text(encoding="utf-8") if Path(path).is_file() else ""
        missing = [n for n in names if not re.search(r"^def %s\(" % re.escape(n), text, re.M)]
        if missing:
            bad.append(("missing named tests in " + path, missing))
            continue
        rc, line, passed = pytest_run([path])
        if rc != 0 or bad_count(line) or passed < len(names):
            bad.append(("named tests", line))
    if bad:
        print("AR-G100-FAIL %d of %d cases failed or a named test is missing: %s" % (len(failed), len(out), str(bad)[:300]))
        return 1
    print("AR-G100-OK %d cases, %d named tests pass" % (len(out), sum(len(v) for v in NEW_TESTS.values())))
    return 0


def regress():
    total, bad = 0, []
    for path in REGRESS:
        rc, line, passed = pytest_run([path])
        total += passed
        if rc != 0 or bad_count(line):
            bad.append((Path(path).name, line))
    diff = subprocess.run(["git", "diff", "--name-only", "box/dell2...HEAD"], capture_output=True, text=True).stdout.split()
    folder = "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/0.9.0_WK_IRPT_ANLREQ~"
    order = "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-100."
    stray = [p for p in diff if p not in OWN_FILES and not p.startswith(ISSUER) and not p.startswith(folder) and not p.startswith(order)]
    if bad or total < MIN_TOTAL or stray:
        print("AR-G100-REGRESS-FAIL total=%d (want at least %d) bad=%s stray=%s" % (total, MIN_TOTAL, str(bad)[:200], str(stray[:5])))
        return 1
    print("AR-G100-REGRESS-OK %d tests in %d files, %d changed paths all the cell's own" % (total, len(REGRESS), len(diff)))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "g100":
        sys.exit(g100())
    if mode == "regress":
        sys.exit(regress())
    print("usage: ar_g100_checks.py g100 | regress")
    sys.exit(2)
