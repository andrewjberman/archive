"""IRPT_ANLREQ AR-g-93 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g93_checks.py g93       the Opal producer prices the benchmark (SPY) and the risk-free rate (BIL) through the same chain,
                                      hands them to the layout, and names them in words (hand-computed beta, alpha, Sharpe, Sortino),
                                      and the six named new tests exist and pass
    python ar_g93_checks.py regress   the producer's existing test files (run one at a time) still pass

Prints one RESULT line: AR-G93-OK / AR-G93-FAIL or AR-G93-REGRESS-OK / AR-G93-REGRESS-FAIL; rc 0 only on OK. ASCII only. It borrows the
fakes and the hand-computed series of ar_g86_checks.py (same folder).
"""
import copy
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ar_g86_checks as g86  # noqa: E402

T = g86.T
NEW_TESTS = {
    T + "test_opal_producer_benchmark.py": [
        "test_beta_alpha_sharpe_and_sortino_are_valued_from_spy_and_bil",
        "test_the_report_names_the_benchmark_and_the_risk_free_rate_in_words",
        "test_an_unpriced_benchmark_leaves_beta_and_alpha_input_missing_and_says_so",
        "test_an_unpriced_risk_free_rate_leaves_alpha_sharpe_and_sortino_input_missing_and_says_so",
        "test_each_benchmark_price_carries_its_source_and_the_trace_inputs_stay_clean",
        "test_pricing_off_reads_neither_the_benchmark_nor_the_risk_free_rate",
    ],
}
EXISTING = g86.EXISTING + [T + "test_opal_producer_prices.py", T + "test_opal_producer_page_wording.py"]
MIN_TOTAL = 177
SPY_F = lambda k: 1.012 if k % 2 == 0 else 0.996  # noqa: E731
BIL_F = lambda k: 1.003  # noqa: E731
BENCH_TEXT = "Benchmark: SPY, a proxy for the S&P 500 Total Return index."
RF_TEXT = "Risk-free rate: BIL, 1-3 Month T-Bill ETF."
BENCH_MISSING = "Benchmark: SPY, a proxy for the S&P 500 Total Return index, could not be priced; beta and alpha are not available."
RF_MISSING = "Risk-free rate: BIL, 1-3 Month T-Bill ETF, could not be priced; alpha, Sharpe and Sortino are not available."


def _stat(statistic, label):
    return {"id": "m." + statistic, "page": 2, "kind": "number", "label": label,
            "source": {"computed": "OWN_SERIES", "call": "portfolio_level_series", "field": "$.chart_data[0][0].raw_data",
                       "statistic": statistic}}


MINI = copy.deepcopy(g86.MINI)
MINI["elements"] = [e for e in MINI["elements"] if e["id"] != "m.sharpe1y"] + [
    _stat("beta_1y", "Beta 1y"), _stat("alpha_1y", "Alpha 1y"), _stat("sharpe_1y", "Sharpe 1y"), _stat("sortino_1y", "Sortino 1y")]


def series_of(factor):
    out, v = [], 100.0
    for k in range(28):
        if k:
            v *= factor(k)
        out.append((g86.month_date(k), v))
    return out


def readers(spy=True, bil=True, spy_extra=(), log=None, boom=()):
    """estate: AAA and SPY; yfinance: BBB and BIL; ycharts: CCC. A symbol left out is served by no tier."""
    estate = {"AAA": g86.levels("AAA")}
    yfin = {"BBB": g86.levels("BBB")}
    if spy:
        estate["SPY"] = series_of(SPY_F) + list(spy_extra)
    if bil:
        yfin["BIL"] = series_of(BIL_F)
    return {"estate": g86.reader_of(estate, log, boom), "yfinance": g86.reader_of(yfin, log, boom),
            "ycharts": g86.reader_of({"CCC": g86.levels("CCC")}, log, boom)}


def monthly(level_at):
    return [level_at(k) / level_at(k - 1) - 1.0 for k in range(16, 28)]


def expected():
    rp = monthly(lambda k: g86.portfolio(["AAA", "BBB", "CCC"], k))
    rb = monthly(lambda k: series_of(SPY_F)[k][1])
    rf = monthly(lambda k: series_of(BIL_F)[k][1])
    n = 12
    mp, mb, mf = sum(rp) / n, sum(rb) / n, sum(rf) / n
    var_b = sum((b - mb) ** 2 for b in rb) / (n - 1)
    beta = sum((a - mp) * (b - mb) for a, b in zip(rp, rb)) / (n - 1) / var_b
    alpha = ((mp - mf) - beta * (mb - mf)) * 12.0 * 100.0
    ex = [a - f for a, f in zip(rp, rf)]
    mean = sum(ex) / n
    sharpe = mean * math.sqrt(12.0) / math.sqrt(sum((x - mean) ** 2 for x in ex) / (n - 1))
    sortino = mean * math.sqrt(12.0) / math.sqrt(sum(min(x, 0.0) ** 2 for x in ex) / n)
    return {"m.beta_1y": beta, "m.alpha_1y": alpha, "m.sharpe_1y": sharpe, "m.sortino_1y": sortino}


def run(tp, **over):
    stores = tp.make_stores(map=MINI, **over)
    return stores, tp.op.produce(tp.REQ, tp.FIRM, stores)


def cases(tp):
    out = {}
    want = expected()
    stores, rec = run(tp, pricing=True, price_readers=readers(), as_of=g86.AS_OF)
    doc = g86.document(stores)
    sect = {s["section_id"]: s for s in doc["sections"]}
    out["beta, alpha, Sharpe and Sortino are valued from SPY and BIL, hand-computed"] = all(
        sect[k]["status"] == "VALUE" and g86.close(float(sect[k]["value"]), v) for k, v in want.items())
    out["the trace inputs of every element stay clean (prices only)"] = all(
        x["inputs"] == ["prices"] for x in rec["elements"] if x["id"] in ("m.ret1y", "m.mdd1y") or x["id"] in want)
    pr = rec["prices"]
    out["each of SPY and BIL carries its source as a claim, apart from the holdings"] = (
        pr["benchmark"]["symbol"] == "SPY" and pr["benchmark"]["status"] == "PRICED" and pr["benchmark"]["source"] == "estate"
        and pr["risk_free"]["symbol"] == "BIL" and pr["risk_free"]["status"] == "PRICED" and pr["risk_free"]["source"] == "yfinance"
        and "SPY" not in pr["symbols"] and "BIL" not in pr["symbols"] and pr["missing"] == [])
    st = doc["effective_inputs"]["settings"]
    out["the document states both sources"] = (
        st.get("price_benchmark") == {"symbol": "SPY", "source": "estate"} and st.get("price_risk_free") == {"symbol": "BIL", "source": "yfinance"}
        and st.get("price_sources") == {"AAA": "estate", "BBB": "yfinance", "CCC": "ycharts"})
    out["the report names them in words, in order, before the weighting note"] = doc["disclosures"] == [
        {"disclosure_id": "BENCHMARK", "text": BENCH_TEXT}, {"disclosure_id": "RISK_FREE", "text": RF_TEXT},
        {"disclosure_id": "WEIGHTING", "text": doc["disclosures"][-1]["text"]}]
    shown = "{:,.4f}".format(want["m.beta_1y"]).rstrip("0").rstrip(".")
    out["the page prints the beta"] = shown in "\n".join(stores["html"])

    s2, r2 = run(tp, pricing=True, price_readers=readers(spy=False), as_of=g86.AS_OF)
    e2, d2 = g86.entries(r2), g86.document(s2)
    sect2 = {s["section_id"]: s for s in d2["sections"]}
    out["an unpriced benchmark: beta and alpha read INPUT_MISSING:benchmark, the rest are valued, and it is said"] = (
        e2["m.beta_1y"]["reason"] == "INPUT_MISSING:benchmark" and e2["m.alpha_1y"]["reason"] == "INPUT_MISSING:benchmark"
        and sect2["m.sharpe_1y"]["status"] == "VALUE" and sect2["m.sortino_1y"]["status"] == "VALUE"
        and d2["disclosures"][0] == {"disclosure_id": "BENCHMARK", "text": BENCH_MISSING}
        and r2["prices"]["benchmark"]["status"] == "MISSING" and r2["prices"]["benchmark"]["source"] is None
        and r2["prices"]["missing"] == [] and g86.close(r2["prices"]["coverage"], 1.0))
    s3, r3 = run(tp, pricing=True, price_readers=readers(bil=False), as_of=g86.AS_OF)
    e3, d3 = g86.entries(r3), g86.document(s3)
    sect3 = {s["section_id"]: s for s in d3["sections"]}
    out["an unpriced risk-free rate: alpha, Sharpe and Sortino read INPUT_MISSING:risk_free, beta is valued, and it is said"] = (
        all(e3[k]["reason"] == "INPUT_MISSING:risk_free" for k in ("m.alpha_1y", "m.sharpe_1y", "m.sortino_1y"))
        and sect3["m.beta_1y"]["status"] == "VALUE" and d3["disclosures"][1] == {"disclosure_id": "RISK_FREE", "text": RF_MISSING})
    ready = readers(spy=False, bil=False)
    ready["ycharts"] = g86.reader_of({})
    s4, r4 = run(tp, pricing=True, price_readers=ready, as_of=g86.AS_OF)
    d4 = g86.document(s4)
    out["with a holding unpriced as well, the order is UNPRICED, BENCHMARK, RISK_FREE, WEIGHTING"] = (
        [d["disclosure_id"] for d in d4["disclosures"]] == ["UNPRICED", "BENCHMARK", "RISK_FREE", "WEIGHTING"]
        and d4["disclosures"][0]["text"] == "No price was found for: CCC. Return and risk figures cover the other holdings only.")
    s5, r5 = run(tp, pricing=True, price_readers=readers(spy_extra=[("2026-10-15", 99999.0)]), as_of=g86.AS_OF)
    out["a benchmark row after as_of is never used"] = (
        r5["prices"]["benchmark"]["last_date"] == g86.AS_OF
        and all(g86.close(float({s["section_id"]: s for s in g86.document(s5)["sections"]}[k]["value"]), v) for k, v in want.items()))
    s6, r6 = run(tp, pricing=True, price_readers=readers(boom={"SPY"}), as_of=g86.AS_OF)
    blob = (b"".join(p["Body"] if isinstance(p["Body"], bytes) else str(p["Body"]).encode() for p in s6["objects"].puts)
            + json.dumps(g86.document(s6), sort_keys=True).encode())
    out["a failing benchmark reader is an attempt; its text is never kept"] = (
        r6["prices"]["benchmark"]["status"] == "MISSING" and b"secret-xyz-token" not in blob
        and r6["prices"]["benchmark"]["attempts"][0] == {"tier": "estate", "outcome": "ERROR:RuntimeError"})
    log = []
    s7, r7 = run(tp, price_readers=readers(log=log), as_of=g86.AS_OF)
    d7 = g86.document(s7)
    out["pricing off: neither SPY nor BIL is read and nothing about them is stated"] = (
        log == [] and "prices" not in r7 and [d["disclosure_id"] for d in d7["disclosures"]] == ["NO_PRICING", "WEIGHTING"]
        and "price_benchmark" not in d7["effective_inputs"]["settings"])
    log2 = []
    pk = tp.make_stores(map=MINI, pricing=True, price_readers=readers(log=log2), as_of=g86.AS_OF)
    tp.op.produce_package(tp.REQ, tp.FIRM, pk, {"text": "Draft commentary text."})
    out["the package render reads SPY and BIL too and prints the beta"] = (
        {"SPY", "BIL"} <= {x[0] for x in log2} and shown in "\n".join(pk["html"]))
    return out


def main(mode):
    if mode == "g93":
        try:
            tp = g86.load()
        except Exception as exc:
            print("AR-G93-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        try:
            got = cases(tp)
        except Exception as exc:
            print("AR-G93-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:240]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        missing = []
        for path, names in NEW_TESTS.items():
            rc, line, passed, text = g86.pytest_run([path], extra=("--collect-only",))
            have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", text))
            missing += [n for n in names if n not in have]
        rc, line, passed, text = g86.pytest_run(list(NEW_TESTS))
        need = sum(len(v) for v in NEW_TESTS.values())
        print("direct cases %d, wrong %s" % (len(got), wrong or "none"))
        print("named tests missing: %s" % (missing or "none"))
        print("new tests: %s" % line)
        if wrong or missing or rc != 0 or g86.bad_count(line) or passed < need:
            print("AR-G93-FAIL wrong=%s missing=%s rc=%d passed=%d (need >= %d)" % (wrong or "none", missing or "none", rc, passed, need))
            return 1
        print("AR-G93-OK direct=%d named=%d passed=%d" % (len(got), need, passed))
        return 0
    if mode == "regress":
        total, bad = 0, []
        for path in EXISTING:
            rc, line, passed, text = g86.pytest_run([path])
            print("%s: %s" % (path.split("/")[-1], line[:70]))
            total += passed
            if rc != 0 or g86.bad_count(line) or passed == 0:
                bad.append(path.split("/")[-1])
        if bad or total < MIN_TOTAL:
            print("AR-G93-REGRESS-FAIL files=%s passed=%d (need >= %d)" % (bad or "none", total, MIN_TOTAL))
            return 1
        print("AR-G93-REGRESS-OK passed=%d" % total)
        return 0
    print("usage: ar_g93_checks.py g93|regress")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
