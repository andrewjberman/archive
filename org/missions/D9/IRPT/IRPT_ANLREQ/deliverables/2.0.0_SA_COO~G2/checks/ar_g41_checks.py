"""IRPT_ANLREQ AR-g-41 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g41_checks.py g41       optional_bindings answers its six cases, and the two new test files pass
    python ar_g41_checks.py regress   the resident factory tests and the research tests still pass

Prints one RESULT line: AR-G41-OK / AR-G41-FAIL or AR-G41-REGRESS-OK / AR-G41-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import importlib.util
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
B = "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/"
Q1 = "https://sqs.us-east-1.amazonaws.com/000000000000/example-analysis-ready"
Q2 = "https://sqs.us-east-1.amazonaws.com/000000000000/example-commentary-ready"
PK = {"api_base": "https://example.invalid", "email": "svc-example@example.invalid", "secret_name": "example/name"}


def bad_count(line):
    """Failed tests plus errors named in a pytest summary line. `1 xfailed` is an expected failure and is not counted."""
    return sum(int(n) for n in re.findall(r"(?<![A-Za-z])([0-9]+) (?:failed|errors?)(?![A-Za-z])", line))


def pytest_line(target):
    out = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", target],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln for ln in (out.stdout + out.stderr).splitlines() if re.search(r"[0-9]+ (passed|failed|error)", ln)]
    line = lines[-1].strip() if lines else "(no summary line)"
    m = re.search(r"([0-9]+) passed", line)
    return out.returncode, line, int(m.group(1)) if m else 0


def refusal(fn, **kw):
    try:
        fn(**kw)
    except ValueError as exc:
        return str(exc)
    except Exception as exc:  # the wrong exception type is itself a finding
        return "WRONG-TYPE:" + type(exc).__name__
    return "NO-REFUSAL"


def main(mode):
    if mode == "g41":
        try:
            spec = importlib.util.spec_from_file_location("builder", B + "build_resident_package.py")
            builder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(builder)
            fn = builder.optional_bindings
        except Exception as exc:
            print("AR-G41-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        got = {"empty": fn() == {},
               "full": fn(analysis_ready_queue_url=Q1, commentary_ready_queue_url=Q2, packager=dict(PK))
               == {"analysis_ready_queue_url": Q1, "commentary_ready_queue_url": Q2, "packager": PK},
               "i3 only": fn(analysis_ready_queue_url=Q1) == {"analysis_ready_queue_url": Q1}}
        tokens = {"BINDING_QUEUE_URL:analysis_ready_queue_url": refusal(fn, analysis_ready_queue_url="http://not-sqs"),
                  "BINDING_PACKAGER_REQUIRED": refusal(fn, commentary_ready_queue_url=Q2),
                  "BINDING_PACKAGER_WITHOUT_QUEUE": refusal(fn, packager=dict(PK)),
                  "BINDING_PACKAGER_KEYS": refusal(fn, commentary_ready_queue_url=Q2, packager={"api_base": PK["api_base"]})}
        wrong = [k for k, ok in got.items() if not ok] + [k for k, v in tokens.items() if v != k]
        rc1, line1, passed1 = pytest_line(B + "test_build_resident_bindings.py")
        rc2, line2, passed2 = pytest_line(R + "reports/tests/test_resident_packager_binding.py")
        print("cases %s | refusals %s" % (got, tokens))
        print("builder tests: %s" % line1)
        print("runtime tests: %s" % line2)
        if wrong or rc1 != 0 or bad_count(line1) or passed1 < 5 or rc2 != 0 or bad_count(line2) or passed2 < 6:
            print("AR-G41-FAIL %s; builder rc=%d passed=%d (need >= 5); runtime rc=%d passed=%d (need >= 6)" % (
                ", ".join(wrong) or "cases ok", rc1, passed1, rc2, passed2))
            return 1
        print("AR-G41-OK cases=3 refusals=4 builder=%d runtime=%d" % (passed1, passed2))
        return 0
    if mode == "regress":
        rc1, line1, passed1 = pytest_line(R + "reports/tests/test_resident_installed.py")
        rc2, line2, passed2 = pytest_line(R + "ycharts/research/tests")
        print("resident factory: %s" % line1)
        print("research: %s" % line2)
        if rc1 != 0 or bad_count(line1) or passed1 < 19 or rc2 != 0 or bad_count(line2) or passed2 < 281:
            print("AR-G41-REGRESS-FAIL factory rc=%d passed=%d (need >= 19); research rc=%d passed=%d (need >= 281)" % (
                rc1, passed1, rc2, passed2))
            return 1
        print("AR-G41-REGRESS-OK factory=%d research=%d" % (passed1, passed2))
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
