"""IRPT_ANLREQ AR-g-86 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g86_checks.py g86       the Opal producer's price stage answers its direct cases (a priced run on fakes), and the
                                      ten named new tests exist and pass
    python ar_g86_checks.py regress   the producer's existing test files (run one at a time) still pass, 163 tests in all

Prints one RESULT line: AR-G86-OK / AR-G86-FAIL or AR-G86-REGRESS-OK / AR-G86-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import json
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/ycharts/research/"
T = R + "tests/"
NEW_TESTS = {
    T + "test_opal_producer_prices.py": [
        "test_priced_run_values_a_return_and_a_drawdown_from_the_buy_and_hold_series",
        "test_each_price_carries_its_source_as_a_claim",
        "test_unpriced_symbol_is_named_in_the_report_and_the_run_still_completes",
        "test_nothing_priced_runs_without_prices_and_says_so",
        "test_tier_error_text_never_reaches_the_record",
        "test_rows_after_as_of_are_never_used",
        "test_pricing_off_is_unchanged_and_calls_no_reader",
        "test_pricing_on_needs_as_of_and_readers",
        "test_package_render_uses_the_same_price_stage",
        "test_only_the_price_call_is_kept_in_the_map",
    ],
}
EXISTING = [T + "test_opal_producer.py", T + "test_opal_packager.py", T + "test_layout_overview.py", T + "test_portfolio_series.py",
            T + "test_price_source.py", T + "test_swap_replacement.py", T + "test_layout_commentary.py", T + "test_held_data.py"]
FIRM = "cottonwood"
AS_OF = "2026-10-14"
BASE = "2024-07-14"  # point k is the 14th of month BASE + k; k = 27 is 2026-10-14
AMOUNTS = {"AAA": 500.0, "BBB": 300.0, "CCC": 200.0}
# monthly return factors, k = 1..27: AAA +2% except k = 20 (-10%); BBB +1%; CCC +1.5%
FACT = {"AAA": lambda k: 0.90 if k == 20 else 1.02, "BBB": lambda k: 1.01, "CCC": lambda k: 1.015}
MINI = {"schema": "synthetic", "report_type": "OVERVIEW", "template_id": "synthetic", "source_pdf": "synthetic",
        "calls": [{"name": "portfolio_info", "method": "GET", "path": "/x/info", "params": {}},
                  {"name": "portfolio_level_series", "method": "GET", "path": "/x/series", "params": {}},
                  {"name": "benchmark_level_series", "method": "GET", "path": "/x/bench", "params": {}}],
        "elements": [
            {"id": "m.title", "page": 1, "kind": "text", "label": "Title", "source": "BUILDER_ONLY"},
            {"id": "m.info", "page": 1, "kind": "text", "label": "Name", "source": {"call": "portfolio_info", "field": "$..name"}},
            {"id": "m.ret1y", "page": 2, "kind": "number", "label": "Return 1y",
             "source": {"computed": "OWN_SERIES", "call": "portfolio_level_series", "field": "$.chart_data[0][0].raw_data",
                        "statistic": "total_return_1y"}},
            {"id": "m.mdd1y", "page": 2, "kind": "number", "label": "Max drawdown 1y",
             "source": {"computed": "OWN_SERIES", "call": "portfolio_level_series", "field": "$.chart_data[0][0].raw_data",
                        "statistic": "max_drawdown_1y"}},
            {"id": "m.sharpe1y", "page": 2, "kind": "number", "label": "Sharpe 1y",
             "source": {"computed": "OWN_SERIES", "call": "portfolio_level_series", "field": "$.chart_data[0][0].raw_data",
                        "statistic": "sharpe_1y"}},
            {"id": "m.bench", "page": 2, "kind": "chart", "label": "Benchmark",
             "source": {"call": "benchmark_level_series", "field": "$.chart_data[0][0].raw_data"}}]}


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_run(targets, extra=()):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *extra, *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error|skipped)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0, text


def month_date(k):
    total = 2024 * 12 + 6 + k  # 2024-07 is month index 6 of year 2024 (0 based)
    return "%04d-%02d-14" % (total // 12, total % 12 + 1)


def levels(sym, upto=27):
    out, v = [], 100.0
    for k in range(0, upto + 1):
        if k:
            v *= FACT[sym](k)
        out.append((month_date(k), v))
    return out


def portfolio(syms, k):
    """Buy-and-hold level at point k over syms, 100 at point 0 (all start together), independent of the code under test."""
    amounts = [AMOUNTS[s] for s in syms]
    return 100.0 * sum(a * levels(s)[k][1] / 100.0 for a, s in zip(amounts, syms)) / sum(amounts)


def expected(syms):
    end, start = portfolio(syms, 27), portfolio(syms, 15)  # the 1y window starts at point 15 (2025-10-14)
    path = [start] + [portfolio(syms, k) for k in range(16, 28)]
    peak, worst = path[0], 0.0
    for v in path:
        peak = max(peak, v)
        worst = min(worst, v / peak - 1.0)
    return (end / start - 1.0) * 100.0, worst * 100.0


def close(a, b):
    return isinstance(a, (int, float)) and abs(a - b) <= 1e-7 * max(1.0, abs(b))


def reader_of(table, log=None, boom=None):
    def reader(symbol, start, end):
        if log is not None:
            log.append((symbol, start, end))
        if boom is not None and symbol in boom:
            raise RuntimeError("secret-xyz-token")
        return list(table.get(symbol, []))
    return reader


def readers_all():
    return {"estate": reader_of({"AAA": levels("AAA")}), "yfinance": reader_of({"BBB": levels("BBB")}),
            "ycharts": reader_of({"CCC": levels("CCC")})}


def load():
    here = T
    sys.path.insert(0, here)
    sys.path.insert(0, R)
    import test_opal_producer as tp
    return tp


def run(tp, **over):
    stores = tp.make_stores(map=MINI, **over)
    return stores, tp.op.produce(tp.REQ, tp.FIRM, stores)


def entries(record):
    return {e["id"]: e for e in record["elements"]}


def document(stores):
    return stores["reports"].persisted[0]["report"]


def cases(tp):
    out = {}
    stores, rec = run(tp, pricing=True, price_readers=readers_all(), as_of=AS_OF)
    e, doc = entries(rec), document(stores)
    want_ret, want_mdd = expected(["AAA", "BBB", "CCC"])
    out["a return element is a VALUE in the trace"] = e["m.ret1y"]["status"] == "VALUE" and e["m.mdd1y"]["status"] == "VALUE"
    sect = {s["section_id"]: s for s in doc["sections"]}
    out["the report sections hold the hand-computed return and drawdown"] = (
        sect["m.ret1y"]["status"] == "VALUE" and close(float(sect["m.ret1y"]["value"]), want_ret)
        and sect["m.mdd1y"]["status"] == "VALUE" and close(float(sect["m.mdd1y"]["value"]), want_mdd) and want_mdd < -1.0)
    out["a statistic that needs a risk-free series says so"] = (
        e["m.sharpe1y"]["status"] == "NOT_AVAILABLE" and e["m.sharpe1y"]["reason"] == "INPUT_MISSING:risk_free")
    out["a vendor-sourced element stays NOT_IN_THIS_VERSION"] = (
        e["m.info"]["status"] == "NOT_AVAILABLE" and e["m.info"]["reason"] == "NOT_IN_THIS_VERSION"
        and e["m.bench"]["status"] == "NOT_AVAILABLE" and e["m.bench"]["reason"] == "NOT_IN_THIS_VERSION")
    out["the series is named prices in the trace"] = e["m.ret1y"]["inputs"] == ["prices"] and "prices" in doc["effective_inputs"]["inputs_as_of"]
    pr = rec.get("prices", {})
    syms = pr.get("symbols", {})
    out["each price carries its source as a claim"] = (
        [syms.get(s, {}).get("source") for s in ("AAA", "BBB", "CCC")] == ["estate", "yfinance", "ycharts"]
        and pr.get("sources_used") == ["estate", "ycharts", "yfinance"] and pr.get("missing") == [] and close(pr.get("coverage"), 1.0)
        and pr.get("as_of") == AS_OF and syms.get("CCC", {}).get("last_date") == AS_OF)
    out["the document says it is priced and where from"] = (
        doc["effective_inputs"]["settings"].get("pricing") is True and doc["effective_inputs"]["settings"].get("price_as_of") == AS_OF
        and doc["effective_inputs"]["settings"].get("price_sources") == {"AAA": "estate", "BBB": "yfinance", "CCC": "ycharts"}
        and doc["effective_inputs"]["inputs_as_of"]["prices"] == AS_OF)
    out["a fully priced run carries no NO_PRICING and no UNPRICED disclosure"] = [d["disclosure_id"] for d in doc["disclosures"]] == ["WEIGHTING"]
    off_stores, off_rec = run(tp)
    page_on, page_off = stores["html"][0], off_stores["html"][0]
    line = tp.lo.NOT_IN_THIS_VERSION_LINE
    out["the page prints fewer not-in-this-version lines when priced"] = page_on.count(line) < page_off.count(line)

    miss_stores, miss = run(tp, pricing=True, as_of=AS_OF, price_readers={
        "estate": reader_of({"AAA": levels("AAA")}), "yfinance": reader_of({"BBB": levels("BBB")}), "ycharts": reader_of({})})
    me, mdoc, mp = entries(miss), document(miss_stores), miss.get("prices", {})
    want_ret2, _ = expected(["AAA", "BBB"])
    msect = {s["section_id"]: s for s in mdoc["sections"]}
    out["an unpriced symbol is named and the others are valued"] = (
        mp.get("missing") == ["CCC"] and mp.get("symbols", {}).get("CCC", {}).get("status") == "MISSING"
        and mp["symbols"]["CCC"].get("source") is None and len(mp["symbols"]["CCC"].get("attempts", [])) == 3
        and close(mp.get("coverage"), 0.8) and me["m.ret1y"]["status"] == "VALUE" and close(float(msect["m.ret1y"]["value"]), want_ret2))
    out["the unpriced disclosure is in words, first"] = mdoc["disclosures"][0] == {
        "disclosure_id": "UNPRICED", "text": "No price was found for: CCC. Return and risk figures cover the other holdings only."}

    none_stores, none = run(tp, pricing=True, as_of=AS_OF, price_readers={"estate": reader_of({}), "yfinance": reader_of({}), "ycharts": reader_of({})})
    ne, ndoc = entries(none), document(none_stores)
    out["nothing priced: the run completes and says so"] = (
        ne["m.ret1y"]["status"] == "NOT_AVAILABLE" and ne["m.ret1y"]["reason"] == "INPUT_MISSING:portfolio_level_series"
        and none["prices"]["missing"] == ["AAA", "BBB", "CCC"] and close(none["prices"]["coverage"], 0.0)
        and ndoc["disclosures"][0]["text"] == "No price was found for: AAA, BBB, CCC. Return and risk figures cover the other holdings only.")

    err_stores, err = run(tp, pricing=True, as_of=AS_OF, price_readers={
        "estate": reader_of({"AAA": levels("AAA")}, boom={"AAA"}), "yfinance": reader_of({"AAA": levels("AAA"), "BBB": levels("BBB")}),
        "ycharts": reader_of({"CCC": levels("CCC")})})
    wrote = b"".join(p["Body"] if isinstance(p["Body"], bytes) else str(p["Body"]).encode() for p in err_stores["objects"].puts)
    blob = wrote + json.dumps(document(err_stores), sort_keys=True).encode()
    a_attempts = err["prices"]["symbols"]["AAA"]["attempts"]
    out["a failing tier is an attempt, its text is never kept"] = (
        err["prices"]["symbols"]["AAA"]["source"] == "yfinance" and a_attempts[0] == {"tier": "estate", "outcome": "ERROR:RuntimeError"}
        and b"secret-xyz-token" not in blob)

    late = {s: levels(s) for s in AMOUNTS}
    late["AAA"] = late["AAA"] + [("2026-10-15", 99999.0)]
    cut_stores, cut = run(tp, pricing=True, as_of=AS_OF, price_readers={
        "estate": reader_of(late), "yfinance": reader_of({}), "ycharts": reader_of({})})
    out["a row after as_of is never used"] = (
        cut["prices"]["symbols"]["AAA"]["last_date"] == AS_OF and close(float({s["section_id"]: s for s in document(cut_stores)["sections"]}["m.ret1y"]["value"]), want_ret))

    log = []
    spy = {t: reader_of({s: levels(s) for s in AMOUNTS}, log) for t in ("estate", "yfinance", "ycharts")}
    off2_stores, off2 = run(tp, price_readers=spy, as_of=AS_OF)
    odoc = document(off2_stores)
    oe = entries(off2)
    out["pricing off: no reader is called and nothing is priced"] = (
        log == [] and "prices" not in off2 and [d["disclosure_id"] for d in odoc["disclosures"]] == ["NO_PRICING", "WEIGHTING"]
        and odoc["effective_inputs"]["settings"].get("pricing") is False and "price_sources" not in odoc["effective_inputs"]["settings"]
        and oe["m.ret1y"]["reason"] == "NOT_IN_THIS_VERSION" and oe["m.info"]["reason"] == "NOT_IN_THIS_VERSION")

    log2 = []
    spy2 = {t: reader_of({s: levels(s) for s in AMOUNTS}, log2) for t in ("estate",)}
    run(tp, pricing=True, price_readers=spy2, as_of=AS_OF)
    out["the window is ten years to as_of"] = bool(log2) and all(x[1] == "2016-10-14" and x[2] == AS_OF for x in log2)

    out["only the price call is kept in the map when pricing is on, none when off"] = (
        [c["name"] for c in tp.op._opal_map(MINI, pricing=True)["calls"]] == ["portfolio_level_series"]
        and tp.op._opal_map(MINI)["calls"] == [] and tp.op._opal_map(MINI, pricing=False)["calls"] == [])

    refusals = []
    for over in ({"pricing": True, "price_readers": readers_all()}, {"pricing": True, "as_of": AS_OF},
                 {"pricing": True, "price_readers": readers_all(), "as_of": "2026-13-45"}):
        s = tp.make_stores(map=MINI, **over)
        try:
            tp.op.produce(tp.REQ, tp.FIRM, s)
            refusals.append("NO-REFUSAL")
        except tp.op.ProducerRefused as exc:
            refusals.append(str(exc) if not s["objects"].puts and not s["reports"].persisted else "WROTE")
    out["pricing on without as_of or readers is refused before any write"] = refusals == [
        "store required: as_of", "store required: price_readers", "store required: as_of"]

    log3 = []
    spy3 = {"estate": reader_of({"AAA": levels("AAA")}, log3), "yfinance": reader_of({"BBB": levels("BBB")}, log3),
            "ycharts": reader_of({"CCC": levels("CCC")}, log3)}
    pk = tp.make_stores(map=MINI, pricing=True, price_readers=spy3, as_of=AS_OF)
    got = tp.op.produce_package(tp.REQ, tp.FIRM, pk, {"text": "Draft commentary text."})
    pk_off = tp.make_stores(map=MINI)
    tp.op.produce_package(tp.REQ, tp.FIRM, pk_off, {"text": "Draft commentary text."})
    out["the package render takes the same price stage"] = (
        len(log3) >= 3 and isinstance(got, dict) and got.get("sha256")
        and pk["html"][0].count(line) < pk_off["html"][0].count(line))
    return out


def main(mode):
    if mode == "g86":
        try:
            tp = load()
        except Exception as exc:
            print("AR-G86-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        try:
            got = cases(tp)
        except Exception as exc:
            print("AR-G86-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:240]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        missing = []
        for path, names in NEW_TESTS.items():
            rc, line, passed, text = pytest_run([path], extra=("--collect-only",))
            have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", text))
            missing += [n for n in names if n not in have]
        rc, line, passed, text = pytest_run(list(NEW_TESTS))
        need = sum(len(v) for v in NEW_TESTS.values())
        print("direct cases %d, wrong %s" % (len(got), wrong or "none"))
        print("named tests missing: %s" % (missing or "none"))
        print("new tests: %s" % line)
        if wrong or missing or rc != 0 or bad_count(line) or passed < need:
            print("AR-G86-FAIL wrong=%s missing=%s rc=%d passed=%d (need >= %d)" % (wrong or "none", missing or "none", rc, passed, need))
            return 1
        print("AR-G86-OK direct=%d named=%d passed=%d" % (len(got), need, passed))
        return 0
    if mode == "regress":
        total, bad = 0, []
        for path in EXISTING:
            rc, line, passed, text = pytest_run([path])
            print("%s: %s" % (path.split("/")[-1], line[:70]))
            total += passed
            if rc != 0 or bad_count(line) or passed == 0:
                bad.append(path.split("/")[-1])
        if bad or total < 163:
            print("AR-G86-REGRESS-FAIL files=%s passed=%d (need >= 163)" % (bad or "none", total))
            return 1
        print("AR-G86-REGRESS-OK passed=%d" % total)
        return 0
    print("usage: ar_g86_checks.py g86|regress")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
