"""IRPT_ANLREQ AR-g-95 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g95_checks.py g95       the upload door ignores and journals a sent price_date and prices at the derived T-1 (direct cases on
                                     the validator and the service), and the five named new tests exist and pass
    python ar_g95_checks.py regress   nine existing test files (run one at a time) still pass, 156 tests in all

Prints one RESULT line: AR-G95-OK / AR-G95-FAIL or AR-G95-REGRESS-OK / AR-G95-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import importlib.util
import io
import re
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

R = "infra/aws/lambda/investor-reporting/"
T = R + "intake/tests/"
NEW_TESTS = {
    T + "test_price_date_ignored.py": [
        "test_a_sent_price_date_is_dropped_from_the_options_and_logged_as_a_closed_token",
        "test_a_malformed_or_odd_price_date_is_ignored_too",
        "test_the_same_upload_with_and_without_a_price_date_is_the_same_revision",
        "test_a_shares_file_is_priced_at_the_derived_t_minus_1_whatever_date_is_sent",
        "test_a_dollars_file_ignores_a_sent_date_and_resolves_no_price",
    ],
}
EXISTING = [T + "test_uploads.py", T + "test_price_date_default.py", T + "test_uploads_refusal_class.py", T + "test_uploads_on_behalf.py",
            T + "test_load_input_owner_typed.py", T + "test_unresolved_keep.py", T + "test_template_reader.py",
            R + "ycharts/generate/tests/test_y5_proxy_corrections.py", R + "ops/tests/test_prospect_dates.py"]
MIN_TOTAL = 156
TOKEN = "IRPT_UPLOAD price_date_ignored=1"


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
    sys.path.insert(0, str(here))
    spec = importlib.util.spec_from_file_location("price_date_harness", here / "test_price_date_default.py")
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    import uploads
    out = {}

    def validate(**changes):
        buf = io.StringIO()
        with redirect_stdout(buf):
            options = uploads.validate_upload(base.payload(base.SHARES, **changes))[3]
        return options, buf.getvalue()
    opts, said = validate(price_date="2026-09-21")
    out["a sent price_date is dropped and one closed token is journalled"] = opts["price_date"] is None and said == TOKEN + "\n"
    opts_none, said_none = validate(price_date=None)
    opts_absent, said_absent = validate()
    out["no token when no date is sent"] = said_none == "" and said_absent == "" and opts_none["price_date"] is None
    odd = [validate(price_date=v) for v in ("2026-13-45", "yesterday", 5, ["2026-09-21"], "x" * 500)]
    out["a malformed or odd value is ignored too and never printed"] = all(
        o["price_date"] is None and s == TOKEN + "\n" for o, s in odd)
    out["the options of the same upload with and without a date are identical"] = opts == opts_absent
    out["the other valuation guard stands"] = (
        refusal(lambda: uploads.validate_upload(base.payload(base.SHARES, reference_notional="9" * 65))).endswith("VALUATION_OPTION")
        and refusal(lambda: uploads.validate_upload(base.payload(base.SHARES, reference_notional=5))).endswith("VALUATION_OPTION"))
    case = base.PriceDateDefaultTests("test_a_dollars_file_with_no_date_is_untouched")
    case.setUp()
    seen = []
    real = uploads.default_price_date

    def spy(value, *a, **k):
        seen.append(value)
        return real(value, *a, **k)
    with patch.object(base.portfolio, "_new_york_today", return_value=base.WEDNESDAY, create=True), patch.object(uploads, "default_price_date", spy), \
            redirect_stdout(io.StringIO()):
        shares = case.create(base.payload(base.SHARES, price_date="2026-09-21"))
    derived = base.PRIOR[base.WEDNESDAY]
    out["a SHARES file is priced at the derived T-1, whatever date is sent"] = (
        shares["state"] == "NORMALIZED" and case.service.resolve_prices.call_args.args[-1] == derived
        and [r["price"]["as_of"] for r in shares["portfolio"]["rows"]] == [derived])
    out["the door asks for the derived date, never the sent one"] = seen == [None]
    case.setUp()
    with patch.object(base.portfolio, "_new_york_today", return_value=base.WEDNESDAY, create=True), redirect_stdout(io.StringIO()):
        malformed = case.create(base.payload(base.SHARES, price_date="2026-13-45"))
    out["a malformed date no longer refuses"] = malformed["state"] == "NORMALIZED" and case.service.resolve_prices.call_args.args[-1] == derived
    case.setUp()
    with patch.object(base.portfolio, "_new_york_today", return_value=base.WEDNESDAY, create=True), redirect_stdout(io.StringIO()):
        first = case.create(base.payload(base.SHARES, price_date="2026-09-21"))
        second = case.create(base.payload(base.SHARES))
    out["the same upload with and without a date is one revision"] = first == second
    case.setUp()
    with redirect_stdout(io.StringIO()):
        dollars = case.create(base.payload("Ticker,Market Value,Currency\nAAPL,10.01,USD\n", price_date="2026-09-21"))
    out["a dollars file ignores a sent date and resolves no price"] = dollars["state"] == "NORMALIZED" and case.service.resolve_prices.call_count == 0
    return out


def main(mode):
    if mode == "g95":
        try:
            got = cases()
        except Exception as exc:
            print("AR-G95-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:240]))
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
            print("AR-G95-FAIL wrong=%s missing=%s rc=%d passed=%d (need >= %d)" % (wrong or "none", missing or "none", rc, passed, need))
            return 1
        print("AR-G95-OK direct=%d named=%d passed=%d" % (len(got), need, passed))
        return 0
    if mode == "regress":
        total, bad = 0, []
        for path in EXISTING:
            rc, line, passed, text = pytest_run([path])
            print("%s: %s" % (path.split("/")[-1], line[:70]))
            total += passed
            if rc != 0 or bad_count(line) or passed == 0:
                bad.append(path.split("/")[-1])
        if bad or total < MIN_TOTAL:
            print("AR-G95-REGRESS-FAIL files=%s passed=%d (need >= %d)" % (bad or "none", total, MIN_TOTAL))
            return 1
        print("AR-G95-REGRESS-OK passed=%d" % total)
        return 0
    print("usage: ar_g95_checks.py g95|regress")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
