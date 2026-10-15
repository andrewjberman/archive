"""IRPT_ANLREQ AR-g-98 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g98_checks.py g98       swap_pass.load_pool and swap_pass.swap_holdings answer 60 direct cases on fakes (the pool file's
                                     refusals and its 30-day edge, in-place replacement keeping the amount, the pick rule, the
                                     left-out words, merges, the record's keys), the module is stdlib-only with no clock, network or
                                     environment read, and the thirteen named new tests exist and pass
    python ar_g98_checks.py regress   six existing test files (run one at a time) still pass, 59 tests in all, and the branch changed
                                     only the cell's own files (measured against the merge-base with box/dell2)

Prints one RESULT line: AR-G98-OK / AR-G98-FAIL or AR-G98-REGRESS-OK / AR-G98-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

R = "infra/aws/lambda/investor-reporting/"
RES = R + "ycharts/research/"
MODULE = RES + "swap_pass.py"
BUILDER = RES + "build_swap_pool.py"
NEW_TESTS = {
    RES + "tests/test_swap_pass.py": [
        "test_load_pool_reads_a_dated_held_snapshot_and_flags_a_stale_one",
        "test_load_pool_refuses_every_malformed_snapshot_with_a_stable_code",
        "test_an_unresolved_row_is_replaced_in_place_keeping_the_amount_and_naming_the_client_ticker",
        "test_a_row_with_no_class_or_no_priced_candidate_is_left_out_and_named_not_analysed",
        "test_a_replacement_already_held_merges_its_amount",
        "test_the_pick_is_the_longest_history_ties_to_the_first_ticker_and_resolved_rows_pass_through",
        "test_the_record_carries_the_pool_vintage_and_the_stale_words",
        "test_a_history_port_with_prefetch_is_asked_once_for_the_same_class_candidates",
    ],
    RES + "tests/test_build_swap_pool.py": [
        "test_plain_and_typed_items_build_the_same_snapshot",
        "test_rows_without_a_ticker_or_class_are_skipped_and_counted",
        "test_the_snapshot_loads_through_swap_pass_and_carries_the_claim_and_date",
        "test_the_summary_line_states_rows_classes_the_largest_class_and_the_request_bound",
        "test_a_bad_date_or_an_unreadable_export_is_refused_with_nothing_written",
    ],
}
REGRESS = [RES + "tests/test_swap_replacement.py", RES + "tests/test_runner_unresolved.py", RES + "tests/test_opal_producer.py",
           RES + "tests/test_opal_producer_prices.py", RES + "tests/test_opal_producer_benchmark.py",
           R + "ycharts/generate/tests/test_normalized_input_unresolved.py"]
MIN_TOTAL = 59
OWN_FILES = (MODULE, BUILDER, RES + "tests/test_swap_pass.py", RES + "tests/test_build_swap_pool.py")
ISSUER = ("org/missions/D9/IRPT/IRPT_ANLREQ/decompositions/", "org/missions/D9/IRPT/IRPT_ANLREQ/deliverables/2.0.0_SA_COO~G2/checks/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/", "org/tier1_exec/2.0.0_SA_COO~G2/",
          "org/missions/D9/IRPT/IRPT_ANLREQ/surprise-channel/investigations/INVESTIGATION_v1.md")
CLASS_EQ = {"asset_class": "equity", "sub_asset_class": "USLargeCap"}
POOL_ROWS = [{"ticker": "AAA", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
             {"ticker": "BBB", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
             {"ticker": "CCC", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
             {"ticker": "DDD", "asset_class": "fixed_income", "sub_asset_class": "UltraShortDuration"},
             {"ticker": "EEE", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
             {"ticker": "KNOWNX", "asset_class": "fixed_income", "sub_asset_class": "UltraShortDuration"}]


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


def refusal(fn, *args):
    try:
        fn(*args)
    except Exception as exc:
        return type(exc).__name__ + ":" + str(exc)
    return "NO-REFUSAL"


def cases():
    sys.path.insert(0, str(Path(RES).resolve()))
    import swap_pass as sp
    out = []

    def case(name, ok, why=""):
        out.append((name, bool(ok), why))

    tmp = Path(tempfile.mkdtemp(prefix="g98_"))

    def pool_file(name="pool.json", **changes):
        doc = {"schema": "irpt-swap-pool.v1", "pool_as_of": "2026-09-01", "pool_claim": "held", "rows": [dict(r) for r in POOL_ROWS]}
        doc.update(changes)
        path = tmp / name
        path.write_text(json.dumps(doc), encoding="utf-8")
        return str(path)

    # the pool file
    p = sp.load_pool(pool_file(), "2026-09-11")
    case("P1-loads-and-dates-the-pool", (p["pool_as_of"], p["pool_claim"], p["rows_count"], p["stale_days"], p["stale"]) == ("2026-09-01", "held", 6, 10, False), str(p)[:160])
    case("P2-30-days-is-fresh", sp.load_pool(pool_file(), "2026-10-01")["stale"] is False)
    case("P3-31-days-is-stale", sp.load_pool(pool_file(), "2026-10-02")["stale"] is True)
    for tag, changes, code in (("claim", {"pool_claim": "measured"}, "POOL_CLAIM_NOT_HELD"), ("asof", {"pool_as_of": "2026-02-30"}, "POOL_AS_OF_INVALID"),
                               ("future", {"pool_as_of": "2026-12-31"}, "POOL_DATED_IN_FUTURE"), ("empty", {"rows": []}, "POOL_ROWS"),
                               ("schema", {"schema": "v2"}, "POOL_SHAPE"),
                               ("lower", {"rows": [{"ticker": "aaa", "asset_class": "a", "sub_asset_class": "b"}]}, "POOL_ROW"),
                               ("dup", {"rows": [POOL_ROWS[0], POOL_ROWS[0]]}, "POOL_ROW"),
                               ("blank", {"rows": [{"ticker": "AAA", "asset_class": " ", "sub_asset_class": "b"}]}, "POOL_ROW"),
                               ("extra", {"rows": [{"ticker": "AAA", "asset_class": "a", "sub_asset_class": "b", "x": 1}]}, "POOL_ROW")):
        case("P4-refuses-" + tag, code in refusal(sp.load_pool, pool_file("p_%s.json" % tag, **changes), "2026-10-15"), refusal(sp.load_pool, pool_file("q_%s.json" % tag, **changes), "2026-10-15"))
    case("P5-unreadable", "POOL_UNREADABLE" in refusal(sp.load_pool, str(tmp / "nope.json"), "2026-10-15"))
    case("P6-bad-today", "POOL_TODAY_INVALID" in refusal(sp.load_pool, pool_file(), "yesterday"))
    pool = sp.load_pool(pool_file(), "2026-09-11")
    hist = {"AAA": 300, "BBB": 900, "CCC": 900, "DDD": 50, "EEE": 100}
    # the pass
    rows = [{"ticker": "xx1", "amount": "40.25", "resolution": "UNRESOLVED"}, {"ticker": "AAA", "amount": "10"}]
    before = json.dumps(rows, sort_keys=True)
    res = sp.swap_holdings(rows, pool, classify=lambda s: CLASS_EQ, history_days=hist.get)
    case("S1-replaced-in-place-with-amount", res["rows"] == [{"ticker": "BBB", "amount": "40.25", "client_ticker": "XX1"}, {"ticker": "AAA", "amount": "10"}], str(res["rows"]))
    case("S2-input-not-mutated", json.dumps(rows, sort_keys=True) == before)
    case("S3-tie-goes-to-the-first-ticker", res["swaps"][0]["proxy"] == "BBB" and res["swaps"][0]["history_days"] == 900)
    keys = {"proxy_for", "proxy", "status", "method", "confidence", "low_confidence", "sources", "pool_as_of", "pool_claim", "pool_stale",
            "candidates_priced", "dropped_reasons", "merged", "named", "history_days"}
    case("S4-record-keys", set(res["swaps"][0]) == keys, str(sorted(set(res["swaps"][0]) ^ keys)))
    case("S5-record-vintage", (res["swaps"][0]["pool_as_of"], res["swaps"][0]["pool_claim"], res["swaps"][0]["pool_stale"], res["swaps"][0]["low_confidence"]) == ("2026-09-01", "held", False, False))
    case("S6-record-words", res["swaps"][0]["named"] == "XX1 is replaced by BBB (same asset class and sub asset class; longest Yahoo history, 900 days).", res["swaps"][0]["named"])
    fl2 = sp.swap_holdings([{"ticker": "Q", "amount": "1", "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ,
                           history_days=lambda t: (_ for _ in ()).throw(RuntimeError("x")) if t == "AAA" else (None if t == "EEE" else hist.get(t)))
    case("S8-dropped-reasons-count-why", fl2["swaps"][0]["dropped_reasons"] == {"HISTORY_ERROR": 1, "NOT_PRICED_BY_YAHOO": 1}, str(fl2["swaps"][0]["dropped_reasons"]))
    case("S7-no-amount-in-the-record", "40.25" not in json.dumps(res["swaps"]))
    left = sp.swap_holdings([{"ticker": "BREIT", "amount": "7", "resolution": "UNRESOLVED"}, {"ticker": "AAA", "amount": "3"}], pool, history_days=hist.get)
    case("L1-no-class-is-left-out", [r["ticker"] for r in left["rows"]] == ["AAA"] and left["swaps"][0]["status"] == "NO_REPLACEMENT" and left["swaps"][0]["why"] == "NO_CLASS")
    case("L2-left-out-words", left["swaps"][0]["named"] == "BREIT is not analysed; Opal Staff will manage the replacement.", left["swaps"][0]["named"])
    case("L3-left-out-has-no-proxy", left["swaps"][0]["proxy"] is None and left["swaps"][0]["confidence"] is None)
    boom = sp.swap_holdings([{"ticker": "Q", "amount": "1", "resolution": "UNRESOLVED"}], pool, classify=lambda s: (_ for _ in ()).throw(RuntimeError("x")), history_days=hist.get)
    case("L4-a-raising-classifier-is-no-class", boom["swaps"][0]["why"] == "NO_CLASS" and boom["rows"] == [])
    own = sp.swap_holdings([{"ticker": "KNOWNX", "amount": "9", "resolution": "UNRESOLVED"}], pool, history_days=hist.get)
    case("L5-the-pool-row-gives-the-class", own["swaps"][0]["status"] == "REPLACED" and own["swaps"][0]["proxy"] == "DDD", str(own["swaps"][0]["status"]) + str(own["swaps"][0].get("why")))
    none_priced = sp.swap_holdings([{"ticker": "Q", "amount": "1", "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ, history_days=lambda t: None)
    case("L6-none-priced-is-left-out", none_priced["swaps"][0]["why"] == "NONE_PRICED" and none_priced["rows"] == [])

    def flaky(ticker):
        if ticker == "BBB":
            raise RuntimeError("down")
        return hist.get(ticker)
    fl = sp.swap_holdings([{"ticker": "Q", "amount": "1", "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ, history_days=flaky)
    case("L7-a-raising-history-drops-that-candidate", fl["swaps"][0]["proxy"] == "CCC", str(fl["swaps"][0]["proxy"]))
    # merges
    m1 = sp.swap_holdings([{"ticker": "Q", "amount": "5", "resolution": "UNRESOLVED"}, {"ticker": "BBB", "amount": "10"}], pool, classify=lambda s: CLASS_EQ, history_days=hist.get)
    case("M1-merges-into-a-later-held-row", m1["rows"] == [{"ticker": "BBB", "amount": "15.0"}] and m1["swaps"][0]["merged"] is True, str(m1["rows"]))
    m2 = sp.swap_holdings([{"ticker": "BBB", "amount": 10.0}, {"ticker": "Q", "amount": 5.0, "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ, history_days=hist.get)
    case("M2-merges-into-an-earlier-held-row", m2["rows"] == [{"ticker": "BBB", "amount": 15.0}], str(m2["rows"]))
    m3 = sp.swap_holdings([{"ticker": "Y1", "amount": 1.0, "resolution": "UNRESOLVED"}, {"ticker": "Y2", "amount": 2.0, "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ, history_days=hist.get)
    case("M3-two-swaps-to-one-replacement-merge", m3["rows"] == [{"ticker": "BBB", "amount": 3.0, "client_ticker": "Y1"}] and [x["merged"] for x in m3["swaps"]] == [False, True], str(m3["rows"]))
    total_before = sum(float(r["amount"]) for r in [{"amount": 1.5}, {"amount": 2.5}, {"amount": 4.0}])
    m4 = sp.swap_holdings([{"ticker": "Y1", "amount": 1.5, "resolution": "UNRESOLVED"}, {"ticker": "AAA", "amount": 2.5}, {"ticker": "Y3", "amount": 4.0, "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ, history_days=hist.get)
    case("M4-amounts-are-conserved", abs(sum(float(r["amount"]) for r in m4["rows"]) - total_before) < 1e-9, str(m4["rows"]))
    # stale
    stale = sp.load_pool(pool_file(), "2026-10-20")
    st = sp.swap_holdings([{"ticker": "Q", "amount": "1", "resolution": "UNRESOLVED"}], stale, classify=lambda s: CLASS_EQ, history_days=hist.get)["swaps"][0]
    case("T1-stale-pool-still-swaps-and-says-so", st["status"] == "REPLACED" and st["pool_stale"] is True and st["named"].endswith(
        "The replacement pool was built on 2026-09-01, 49 days before this run, which is older than 30 days."), st["named"][-120:])
    case("T2-deterministic", sp.swap_holdings(rows, pool, classify=lambda s: CLASS_EQ, history_days=hist.get) == res)
    case("T3-rows-without-a-resolution-pass-through-in-order", sp.swap_holdings([{"ticker": "B", "amount": "1"}, {"ticker": "A", "amount": "2"}], pool, history_days=hist.get)["rows"] == [{"ticker": "B", "amount": "1"}, {"ticker": "A", "amount": "2"}])
    # the batched history port
    class Port:
        def __init__(self, fail=False):
            self.asked, self.fail = [], fail

        def prefetch(self, tickers):
            self.asked.append(list(tickers))
            if self.fail:
                raise RuntimeError("down")

        def __call__(self, ticker):
            return hist.get(ticker)

    port = Port()
    pf = sp.swap_holdings([{"ticker": "Q", "amount": "1", "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ, history_days=port)
    case("B1-prefetch-once-with-the-sorted-class-candidates", port.asked == [["AAA", "BBB", "CCC", "EEE"]] and pf["swaps"][0]["proxy"] == "BBB", str(port.asked))
    port2 = Port()
    sp.swap_holdings([{"ticker": "AAA", "amount": "1", "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ, history_days=port2)
    case("B2-the-missing-symbol-is-not-a-candidate", port2.asked == [["BBB", "CCC", "EEE"]], str(port2.asked))
    port3 = Port(fail=True)
    pf3 = sp.swap_holdings([{"ticker": "Q", "amount": "1", "resolution": "UNRESOLVED"}], pool, classify=lambda s: CLASS_EQ, history_days=port3)
    case("B3-a-raising-prefetch-is-tolerated", pf3["swaps"][0]["proxy"] == "BBB")
    port4 = Port()
    sp.swap_holdings([{"ticker": "BREIT", "amount": "1", "resolution": "UNRESOLVED"}], pool, history_days=port4)
    case("B4-no-class-no-prefetch", port4.asked == [])
    port5 = Port()
    sp.swap_holdings([{"ticker": "Q1", "amount": "1", "resolution": "UNRESOLVED"}, {"ticker": "Q2", "amount": "1", "resolution": "UNRESOLVED"}], pool,
                     classify=lambda s: CLASS_EQ, history_days=port5)
    case("B5-once-per-unresolved-row", len(port5.asked) == 2, str(len(port5.asked)))
    # the pool builder
    import contextlib
    import hashlib
    import io
    import build_swap_pool as bp
    items = [{"ticker": "SPY", "asset_class": "equity", "sub_asset_class": "USLargeCap", "name": "n"},
             {"ticker": "IVV", "asset_class": "equity", "sub_asset_class": "USLargeCap"},
             {"ticker": "SGOV", "asset_class": "fixed_income", "sub_asset_class": "UltraShortDuration"}]

    def build(name, data, as_of="2026-10-12"):
        src = tmp / (name + ".json")
        src.write_text(json.dumps(data), encoding="utf-8")
        dst = tmp / (name + ".pool.json")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = bp.main(["--items", str(src), "--as-of", as_of, "--out", str(dst)])
        return rc, dst, buf.getvalue().strip().splitlines()

    rc1, d1, _ = build("plain", items)
    rc2, d2, _ = build("typed", {"Items": [{k: {"S": v} for k, v in i.items()} for i in items]})
    case("BP1-plain-and-typed-items-build-equal-bytes", rc1 == rc2 == 0 and d1.read_bytes() == d2.read_bytes())
    doc = json.loads(d1.read_text(encoding="utf-8"))
    case("BP2-file-shape", set(doc) == {"schema", "pool_as_of", "pool_claim", "rows"} and doc["pool_claim"] == "held" and doc["pool_as_of"] == "2026-10-12"
         and [r["ticker"] for r in doc["rows"]] == ["IVV", "SGOV", "SPY"] and all(set(r) == {"ticker", "asset_class", "sub_asset_class"} for r in doc["rows"]))
    case("BP3-ascii", d1.read_bytes().isascii())
    case("BP4-loads-through-load-pool", sp.load_pool(str(d1), "2026-10-15")["rows_count"] == 3)
    rows, skipped = bp.build_rows(items + [{"asset_class": "a", "sub_asset_class": "b"}, {"ticker": "x y", "asset_class": "a", "sub_asset_class": "b"},
                                           {"ticker": "NC", "asset_class": "a"}, {"ticker": "SPY", "asset_class": "o", "sub_asset_class": "o"}, 5])
    case("BP5-skips-are-counted-by-reason", skipped == {"BAD_TICKER": 2, "DUPLICATE": 1, "NOT_AN_ITEM": 1, "NO_CLASS": 1} and [r["ticker"] for r in rows] == ["IVV", "SGOV", "SPY"], str(skipped))
    case("BP6-first-duplicate-wins", next(r for r in rows if r["ticker"] == "SPY")["asset_class"] == "equity")
    for count, bound in ((1, 1), (50, 1), (51, 2), (101, 3)):
        many = [{"ticker": "E%03d" % i, "asset_class": "equity", "sub_asset_class": "USLargeCap"} for i in range(count)]
        rc, dst, lines = build("many%d" % count, many)
        want = "SWAP-POOL rows=%d skipped=0 classes=1 max_class=%d max_requests_per_holding=%d as_of=2026-10-12 sha256=%s" % (count, count, bound, hashlib.sha256(dst.read_bytes()).hexdigest())
        case("BP7-summary-and-request-bound-%d" % count, rc == 0 and lines and lines[-1] == want, (lines or ["-"])[-1][:140])
    rc3, d3, l3 = build("baddate", items, as_of="2026-13-01")
    case("BP8-bad-date-refused-nothing-written", rc3 == 2 and not d3.exists() and l3 and l3[-1].startswith("SWAP-POOL-REFUSED"))
    with contextlib.redirect_stdout(io.StringIO()):
        rc4 = bp.main(["--items", str(tmp / "absent.json"), "--as-of", "2026-10-12", "--out", str(tmp / "z.json")])
    case("BP9-unreadable-export-refused", rc4 == 2 and not (tmp / "z.json").exists())
    btext = Path(BUILDER).read_text(encoding="utf-8")
    bbanned = [w for w in ("os.environ", "getenv", "boto3", "import requests", "urllib", "yfinance", "socket", "subprocess", "time.time", "date.today", "datetime.now", "utcnow") if w in btext]
    case("BP10-builder-hygiene", not bbanned and all(ord(c) < 128 for c in btext), str(bbanned))
    # hygiene of the module itself
    text = Path(MODULE).read_text(encoding="utf-8")
    banned = [w for w in ("os.environ", "getenv", "print(", "boto3", "import requests", "urllib", "yfinance", "socket", "subprocess", "time.time", "date.today", "datetime.now", "utcnow", "import random") if w in text]
    case("H1-module-hygiene", not banned, str(banned))
    case("H2-ascii", all(ord(c) < 128 for c in text))
    return out


def g98():
    try:
        out = cases()
    except Exception as exc:
        print("AR-G98-FAIL the cases could not run: %s: %s" % (type(exc).__name__, str(exc)[:200]))
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
        print("AR-G98-FAIL %d of %d cases failed or a named test is missing: %s" % (len(failed), len(out), str(bad)[:300]))
        return 1
    print("AR-G98-OK %d cases, %d named tests pass" % (len(out), sum(len(v) for v in NEW_TESTS.values())))
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
    order = "org/missions/D9/IRPT/IRPT_ANLREQ/task-orders/IRPT_ANLREQ.TO-AR-g-98."
    stray = [p for p in diff if p not in OWN_FILES and not p.startswith(ISSUER) and not p.startswith(folder) and not p.startswith(order)]
    if bad or total < MIN_TOTAL or stray:
        print("AR-G98-REGRESS-FAIL total=%d (want at least %d) bad=%s stray=%s" % (total, MIN_TOTAL, str(bad)[:200], str(stray[:5])))
        return 1
    print("AR-G98-REGRESS-OK %d tests in %d files, %d changed paths all the cell's own" % (total, len(REGRESS), len(diff)))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "g98":
        sys.exit(g98())
    if mode == "regress":
        sys.exit(regress())
    print("usage: ar_g98_checks.py g98 | regress")
    sys.exit(2)
