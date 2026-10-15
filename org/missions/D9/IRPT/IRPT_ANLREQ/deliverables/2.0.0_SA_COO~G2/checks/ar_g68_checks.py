"""IRPT_ANLREQ AR-g-68 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g68_checks.py g68       template_corrections answers its six direct cases, and the eight named new tests exist and pass
    python ar_g68_checks.py regress   the four existing test files (kept holding, Y-5 corrections, normalized input, runner) still pass

Prints one RESULT line: AR-G68-OK / AR-G68-FAIL or AR-G68-REGRESS-OK / AR-G68-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
NEW_TESTS = {
    R + "intake/tests/test_unresolved_keep.py": [
        "test_keep_pair_files_the_row_as_unresolved",
        "test_unresolved_row_has_no_receipt_and_stays_out_of_the_vendor_holdings",
        "test_keep_pair_on_a_found_symbol_files_nothing_extra",
        "test_frozen_unresolved_document_replays_and_verifies",
        "test_shares_basis_still_refuses_an_unresolved_row",
    ],
    R + "ycharts/generate/tests/test_normalized_input_unresolved.py": [
        "test_vendor_path_refuses_an_unresolved_row_with_recipe_refused",
    ],
    R + "ycharts/research/tests/test_runner_unresolved.py": [
        "test_read_holdings_refuses_unresolved_by_default",
        "test_read_holdings_with_allow_unresolved_returns_the_marker",
    ],
}
EXISTING = [R + "intake/tests/test_kept_holding.py", R + "ycharts/generate/tests/test_y5_proxy_corrections.py",
            R + "ycharts/generate/tests/test_normalized_input.py", R + "ycharts/research/tests/test_runner.py"]
FOUND = {"finding_code": "TICKER_NOT_FOUND", "from_value": "BREIT", "to_value": "BREIT"}


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


def direct_cases():
    sys.path[:0] = [R + "intake", R, R + "ycharts/generate", R + "ycharts/research"]
    import portfolio as p

    def corr(items):
        try:
            return ("ok", p.template_corrections(items))
        except p.PortfolioRefused as exc:
            return ("refused", str(exc))
        except Exception as exc:
            return ("wrong:" + type(exc).__name__, "")
    out = {}
    kind, val = corr([dict(FOUND)])
    out["exact equal pair for TICKER_NOT_FOUND accepted"] = kind == "ok" and val == [dict(FOUND)]
    out["equal pair for another code refused"] = corr([dict(FOUND, finding_code="TICKER_DATA_NOT_ENTITLED")]) == ("refused", "CORRECTIONS_INVALID")
    out["case-only pair still refused"] = corr([dict(FOUND, from_value="TIMXX", to_value="timxx")]) == ("refused", "CORRECTIONS_INVALID")
    out["an ordinary pair is unchanged"] = corr([dict(FOUND, to_value="SGOV")]) == ("ok", [dict(FOUND, to_value="SGOV")])
    kind, val = corr([dict(FOUND)])
    out["the accepted output replays"] = kind == "ok" and corr(val) == (kind, val)
    out["a repeated from_value is still refused"] = corr([dict(FOUND), dict(FOUND, to_value="SGOV")]) == ("refused", "CORRECTIONS_INVALID")
    return out


def main(mode):
    if mode == "g68":
        try:
            got = direct_cases()
        except Exception as exc:
            print("AR-G68-FAIL import/direct %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        wrong = [k for k, ok in got.items() if not ok]
        missing, collected = [], {}
        for path, names in NEW_TESTS.items():
            rc, line, passed, text = pytest_run([path], extra=("--collect-only",))
            have = set(re.findall(r"::(test_[A-Za-z0-9_]+)", text))
            collected[path] = have
            missing += [n for n in names if n not in have]
        rc, line, passed, text = pytest_run(list(NEW_TESTS))
        print("direct cases %d, wrong %s" % (len(got), wrong or "none"))
        print("named tests missing: %s" % (missing or "none"))
        print("new tests: %s" % line)
        need = sum(len(v) for v in NEW_TESTS.values())
        if wrong or missing or rc != 0 or bad_count(line) or passed < need:
            print("AR-G68-FAIL wrong=%s missing=%s rc=%d passed=%d (need >= %d)" % (wrong or "none", missing or "none", rc, passed, need))
            return 1
        print("AR-G68-OK direct=%d named=%d passed=%d" % (len(got), need, passed))
        return 0
    if mode == "regress":
        rc, line, passed, text = pytest_run(EXISTING)
        print("existing tests: %s" % line)
        if rc != 0 or bad_count(line) or passed < 108:
            print("AR-G68-REGRESS-FAIL rc=%d passed=%d (need >= 108)" % (rc, passed))
            return 1
        print("AR-G68-REGRESS-OK passed=%d" % passed)
        return 0
    print("usage: ar_g68_checks.py g68|regress")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
