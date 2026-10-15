"""IRPT_ANLREQ AR-g-96 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g96_checks.py g96       the door's findings follow the v0.19 decision tree (direct cases on the freeze, the corrections, the
                                     word tables and the suggestion gate), and the six named new tests exist and pass
    python ar_g96_checks.py regress   fifteen existing and new test files (run one at a time) pass, 225 tests in all

Prints one RESULT line: AR-G96-OK / AR-G96-FAIL or AR-G96-REGRESS-OK / AR-G96-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

R = "infra/aws/lambda/investor-reporting/"
T = R + "intake/tests/"
G = R + "ycharts/generate/tests/"
NEW_TESTS = {
    T + "test_decision_tree_findings.py": [
        "test_not_found_offers_replace_and_no_and_never_names_a_proxy",
        "test_a_ticker_that_exists_but_cannot_be_priced_files_unresolved_with_the_staff_words",
        "test_a_proxy_naming_correction_for_a_not_covered_ticker_is_refused_but_replace_and_no_are_accepted",
        "test_no_files_unresolved_and_replace_is_checked_again_naming_the_files_own_row",
        "test_a_retry_class_asks_for_a_retry_and_the_suggestion_gate_still_adds_yes_first",
        "test_no_word_in_either_table_and_no_finding_the_door_emits_says_proxy_or_stand_in",
    ],
}
REGRESS = [T + "test_uploads.py", T + "test_price_date_default.py", T + "test_uploads_refusal_class.py", T + "test_uploads_on_behalf.py",
           T + "test_load_input_owner_typed.py", T + "test_unresolved_keep.py", T + "test_template_reader.py", T + "test_kept_holding.py",
           T + "test_correction_words.py", T + "test_price_date_ignored.py", G + "test_y5_proxy_corrections.py", G + "test_y4_check_gate.py",
           G + "test_resolve_upload.py", G + "test_normalized_input_unresolved.py", R + "ops/tests/test_prospect_dates.py"]
MIN_TOTAL = 225
TREE = ["REPLACE_FILE", "REPLACE_TICKER", "FILE_UNRESOLVED"]
STAFF = "Opal Staff will manage the replacement."
GATED = {"symbol": "TIMXX", "state": "UNAVAILABLE", "reason": "PROVIDER_ENTITLEMENT_UNVERIFIED", "provider_receipt": None}


def bad_count(line):
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_run(targets, extra=()):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", *extra, *targets],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    text = out.stdout + out.stderr
    lines = [ln for ln in text.splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0, text


def refusal(fn, *args):
    try:
        fn(*args)
    except Exception as exc:
        return type(exc).__name__ + ":" + str(exc)
    return "NO-REFUSAL"


def cases():
    here = Path(T).resolve()
    for p in (here, here.parent, here.parents[1] / "ops"):
        sys.path.insert(0, str(p))
    import portfolio
    import upload_suggestions
    import uploads
    import status
    from test_kept_holding import FakeChecker, codes, finding, freeze, resolve
    out = []

    def case(name, ok, why=""):
        out.append((name, bool(ok), why))

    # D1: a ticker that does not exist: Replace and No beside the typo prompt; no proxy action anywhere
    results, _ = resolve(["MISSING", "AAPL"], found=("AAPL",))
    r1 = freeze(b"Ticker,Dollars\nMISSING,10\nAAPL,90\n", results["results"])
    item = finding(r1, "TICKER_NOT_FOUND")
    case("D1-not-found-offers-the-tree", r1["state"] == "NEEDS_CORRECTION" and item["actions"] == TREE and item["value"] == "MISSING",
         json.dumps(item)[:200])
    case("D1-no-name-proxy-in-the-findings", "NAME_PROXY" not in json.dumps(r1["findings"]))
    # D2: a ticker that exists but cannot be priced files UNRESOLVED, a NOTICE, outside the totals
    results, _ = resolve(["AAPL"], found=("AAPL",))
    r2 = freeze(b"Ticker,Dollars\nAAPL,90\nTIMXX,10\n", results["results"] + [GATED])
    f2 = r2["findings"]
    case("D2-gated-files-normalized-with-one-notice", r2["state"] == "NORMALIZED" and codes(r2) == ["TICKER_DATA_NOT_ENTITLED"], str(codes(r2)))
    if f2:
        case("D2-notice-words-and-shape", (f2[0]["severity"], f2[0]["actions"], f2[0]["row"], f2[0]["column"], f2[0]["value"]) == (
            "NOTICE", ["REVIEW"], 3, "A", "TIMXX") and f2[0]["description"] == "Row 3: TIMXX is not covered by our price data. " + STAFF,
            json.dumps(f2[0])[:240])
    doc = r2.get("frozen", {}).get("document", {"rows": [], "holdings": {"rows": [], "total_dollars": None}})
    row = next((r for r in doc["rows"] if r["original"]["symbol"] == "TIMXX"), {})
    case("D2-row-is-unresolved-not-covered", (row.get("resolution"), row.get("method"), row.get("price"), row.get("provider_receipt_sha256"),
                                              row.get("security_id"), row.get("price_source")) == ("UNRESOLVED", "NOT_COVERED", None, None, "TIMXX", None),
         json.dumps(row)[:200])
    case("D2-outside-the-holdings-totals", [r["security_id"] for r in doc["holdings"]["rows"]] == ["AAPL"] and doc["holdings"]["total_dollars"] == "90")
    # D3: the same, on a weight file: the residual counts the unresolved row's dollars
    r3 = freeze(b"Ticker,Target Weight\nAAPL,0.9\nTIMXX,0.1\n", results["results"] + [GATED], reference_notional="1000")
    d3 = r3.get("frozen", {}).get("document", {"disclosures": {}})
    case("D3-weight-file-files-and-the-residual-counts-the-row", r3["state"] == "NORMALIZED" and d3["disclosures"].get("rounding_residual_dollars") in ("0", "0.0", "0.00"),
         str(r3.get("state")) + " " + str(d3["disclosures"].get("rounding_residual_dollars")))
    # D4: a bad amount on a not-covered row is still an error
    r4 = freeze(b"Ticker,Dollars\nAAPL,90\nTIMXX,abc\n", results["results"] + [GATED])
    case("D4-bad-amount-still-needs-correction", r4["state"] == "NEEDS_CORRECTION" and "AMOUNT_NOT_A_NUMBER" in codes(r4), str(codes(r4)))
    # D5: corrections: no proxy for a not-covered ticker, Replace and No for a missing one
    case("D5-proxy-correction-for-not-covered-refused", "CORRECTIONS_INVALID" in refusal(
        portfolio.template_corrections, [{"finding_code": "TICKER_DATA_NOT_ENTITLED", "from_value": "TIMXX", "to_value": "SGOV"}]))
    case("D5-equal-pair-for-not-covered-refused", "CORRECTIONS_INVALID" in refusal(
        portfolio.template_corrections, [{"finding_code": "TICKER_DATA_NOT_ENTITLED", "from_value": "TIMXX", "to_value": "TIMXX"}]))
    case("D5-replace-and-no-accepted", refusal(portfolio.template_corrections, [
        {"finding_code": "TICKER_NOT_FOUND", "from_value": "AAAA", "to_value": "BBBB"},
        {"finding_code": "TICKER_NOT_FOUND", "from_value": "CCCC", "to_value": "CCCC"}]) == "NO-REFUSAL")
    # D6: No files the typed symbol UNRESOLVED; Replace is checked again; a failing replacement names the file's row with the tree
    r6 = freeze(b"Ticker,Dollars\nMISSING,10\nAAPL,90\n", results["results"] + [{"symbol": "MISSING", "state": "NOT_FOUND", "reason": "X",
                "provider_receipt": {"complete": True}}], corrections=[{"finding_code": "TICKER_NOT_FOUND", "from_value": "MISSING", "to_value": "MISSING"}])
    row6 = next((r for r in r6.get("frozen", {"document": {"rows": []}})["document"]["rows"] if r["original"]["symbol"] == "MISSING"), {})
    case("D6-no-files-unresolved-kept-as-typed", r6["state"] == "NORMALIZED" and (row6.get("resolution"), row6.get("method")) == ("UNRESOLVED", "KEPT_AS_TYPED"), str(r6["state"]))
    res7, _ = resolve(["BADD", "AAPL"], found=("AAPL",))
    r7 = freeze(b"Ticker,Dollars\nMISSING,10\nAAPL,90\n", res7["results"], corrections=[{"finding_code": "TICKER_NOT_FOUND", "from_value": "MISSING", "to_value": "BADD"}])
    i7 = finding(r7, "TICKER_NOT_FOUND") if "TICKER_NOT_FOUND" in codes(r7) else {}
    case("D6-failing-replace-names-the-files-row-with-the-tree", r7["state"] == "NEEDS_CORRECTION" and i7.get("value") == "MISSING" and i7.get("actions") == TREE)
    res8, _ = resolve(["GOOD", "AAPL"], found=("GOOD", "AAPL"))
    r8 = freeze(b"Ticker,Dollars\nMISSING,10\nAAPL,90\n", res8["results"], corrections=[{"finding_code": "TICKER_NOT_FOUND", "from_value": "MISSING", "to_value": "GOOD"}])
    case("D6-good-replace-normalizes-with-the-new-symbol", r8["state"] == "NORMALIZED" and "GOOD" in [r["security_id"] for r in r8["frozen"]["document"]["rows"]], str(r8["state"]))
    # D7: the retry classes ask for a retry, name no proxy
    entry = {"state": "CHECK_FAILED", "rows": 0, "last_close": None, "reason": "TIMEOUT"}
    res9, _ = resolve(["TIMXX"], checker=FakeChecker({"TIMXX": entry}))
    i9 = finding(freeze(b"Ticker,Dollars\nTIMXX,1000\n", res9["results"]), "TICKER_CHECK_FAILED")
    case("D7-check-failed-words", i9["actions"] == ["REPLACE_FILE"] and i9["description"] == (
        "TIMXX could not be checked just now (the price history service did not answer in time); upload again in a few minutes."), json.dumps(i9)[:240])
    nc = {"symbol": "ZZ11", "state": "UNAVAILABLE", "reason": "YFINANCE_NOT_CHECKED", "not_checked": "UPLOAD_LIMIT", "provider_receipt": None}
    i10 = finding(freeze(b"Ticker,Dollars\nZZ11,5\n", [nc]), "TICKER_NOT_CHECKED")
    case("D7-not-checked-words", i10["actions"] == ["REPLACE_FILE"] and i10["description"] == (
        "ZZ11 was not checked in this upload (the limit is 10 unknown tickers per upload); upload again."), json.dumps(i10)[:240])
    # D8: the word tables: equal, no proxy talk, the two new sentences, the old constant gone
    equal = uploads.CORRECTION_WORDS == status.CORRECTION_WORDS
    case("D8-word-tables-equal", equal)
    case("D8-no-proxy-talk-in-any-word", not [c for c, w in uploads.CORRECTION_WORDS.items() if re.search(r"proxy|stand in|stand-in|stand-ins", w, re.I)])
    case("D8-the-two-sentences", uploads.CORRECTION_WORDS["TICKER_DATA_NOT_ENTITLED"] == "This holding is not covered by our price data. " + STAFF
         and uploads.CORRECTION_WORDS["TICKER_NOT_FOUND"] == ("Our data provider does not recognize this ticker, so it may be a typo. Accept the suggestion, type the "
                                                              "correct ticker, or leave it for Opal Staff, who will manage the replacement."))
    case("D8-proxy-codes-constant-retired", not hasattr(uploads, "PROXY_CODES") and "TICKER_DATA_NOT_ENTITLED" not in portfolio.CORRECTABLE_FINDINGS)
    # D9: the door's words pass through; the notice keeps its own sentence
    shaped = uploads._with_correction_words(f2 + r1["findings"])
    by = {s["code"]: s for s in shaped}
    case("D9-door-words", by["TICKER_DATA_NOT_ENTITLED"]["description"] == f2[0]["description"] and by["TICKER_DATA_NOT_ENTITLED"]["actions"] == ["REVIEW"]
         and by["TICKER_NOT_FOUND"]["description"] == uploads.CORRECTION_WORDS["TICKER_NOT_FOUND"] and by["TICKER_NOT_FOUND"]["actions"] == TREE)
    # D10: the suggestion gate still puts Yes first
    verified = {"AAPL": {"state": "FOUND", "reason": "EXACT_PROVIDER_MATCH", "candidates": [{"id": "AAPL", "features_needed": []}], "provider_receipt": {"sha256": "b" * 64}}}
    sug, _ = upload_suggestions.suggest_for(r1["findings"], r1["template"], advisory=lambda kind, symbol, **kw: {"result": {"suggestion": "AAPL"}}, verify=lambda s: verified)
    case("D10-yes-first", sug[0]["actions"] == ["ACCEPT_SUGGESTION"] + TREE, str(sug[0]["actions"]))
    # D11: the frozen input is deterministic
    again = freeze(b"Ticker,Dollars\nAAPL,90\nTIMXX,10\n", results["results"] + [GATED])
    case("D11-deterministic", again["frozen"]["input_id"] == r2["frozen"]["input_id"])
    return out


def g96():
    try:
        out = cases()
    except Exception as exc:
        print("AR-G96-FAIL the cases could not run: %s: %s" % (type(exc).__name__, str(exc)[:200]))
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
        rc, line, passed, _ = pytest_run([path])
        if rc != 0 or bad_count(line) or passed < len(names):
            bad.append(("named tests", line))
    if bad:
        print("AR-G96-FAIL %d of %d cases failed or a named test is missing: %s" % (len(failed), len(out), str(bad)[:300]))
        return 1
    print("AR-G96-OK %d cases, %d named tests pass" % (len(out), sum(len(v) for v in NEW_TESTS.values())))
    return 0


def regress():
    total, bad = 0, []
    for path in REGRESS:
        rc, line, passed, _ = pytest_run([path])
        total += passed
        if rc != 0 or bad_count(line):
            bad.append((Path(path).name, line))
    if bad or total < MIN_TOTAL:
        print("AR-G96-REGRESS-FAIL total=%d (want at least %d) bad=%s" % (total, MIN_TOTAL, str(bad)[:300]))
        return 1
    print("AR-G96-REGRESS-OK %d tests in %d files" % (total, len(REGRESS)))
    return 0


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "g96":
        sys.exit(g96())
    if mode == "regress":
        sys.exit(regress())
    print("usage: ar_g96_checks.py g96 | regress")
    sys.exit(2)
