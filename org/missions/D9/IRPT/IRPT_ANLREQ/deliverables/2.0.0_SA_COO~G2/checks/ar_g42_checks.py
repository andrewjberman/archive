"""IRPT_ANLREQ AR-g-42 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g42_checks.py g42       the port presents a token and posts no login; an email in the binding is refused
    python ar_g42_checks.py regress   the four test sets still pass

Prints one RESULT line: AR-G42-OK / AR-G42-FAIL or AR-G42-REGRESS-OK / AR-G42-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import importlib.util
import json
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
B = "org/tier1_exec/2.0.0_SA_COO/deliverables/IRPT_MVP_P/"
TOKEN = "tok-EXAMPLE-not-a-real-token"
CONFIG = {"api_base": "https://example.invalid", "secret_name": "example/packager-token"}
PAYLOAD = {"report_ref": "RPT-x", "pdf_ref": "{}", "original_ref": None, "commentary_ref": "{}", "firm": "examplefirm"}


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


def refused(fn):
    try:
        fn()
    except Exception as exc:
        return type(exc).__name__ + ":" + str(exc)
    return "NO-REFUSAL"


def main(mode):
    if mode == "g42":
        for rel in ("ycharts/research", "reports", "ops", "_authz", "_scope", "_ids", "_keys", "intake",
                    "ycharts/generate", "ycharts/extract", "ycharts/session"):
            sys.path.insert(0, R + rel)
        facts = {}
        try:
            import opal_packager as op
            src = open(R + "ycharts/research/opal_packager.py", encoding="utf-8").read()
            facts["keys are api_base + secret_name"] = set(op.TICKET_PORTS_CONFIG_KEYS) == {"api_base", "secret_name"}
            facts["no login route in the module"] = "auth/login" not in src
            reads, calls = [], []

            def read_secret(name):
                reads.append(name)
                return json.dumps({"token": TOKEN, "sub": "svc-example"})

            def http(method, url, headers, body):
                calls.append((method, url, dict(headers or {})))
                return 200, b"{}"
            port = op.live_ticket_ports(dict(CONFIG), read_secret=read_secret, http=http)
            port["attach"]("TCK-20261011-0a1b2c3d", dict(PAYLOAD))
            facts["secret read by the bound name"] = reads == [CONFIG["secret_name"]]
            facts["one POST, to the package route"] = (len(calls) == 1 and calls[0][0] == "POST"
                                                       and calls[0][1].endswith("/api/scoped/tickets/TCK-20261011-0a1b2c3d/package"))
            facts["bearer token presented"] = bool(calls) and any(
                k.lower() == "authorization" and v == "Bearer " + TOKEN for k, v in calls[0][2].items())
            bad = op.live_ticket_ports(dict(CONFIG), read_secret=lambda name: json.dumps({"sub": "x"}), http=http)
            answer = refused(lambda: bad["attach"]("TCK-20261011-0a1b2c3d", dict(PAYLOAD)))
            facts["a secret with no token is refused by name"] = answer == "PackagerRefused:PACKAGER_TOKEN_UNREADABLE"
            reads2 = []

            def read2(name):
                reads2.append(name)
                return json.dumps({"token": TOKEN})
            state = {"n": 0}

            def http401(method, url, headers, body):
                state["n"] += 1
                return (401, b"{}") if state["n"] == 1 else (200, b"{}")
            again = op.live_ticket_ports(dict(CONFIG), read_secret=read2, http=http401)
            first = refused(lambda: again["attach"]("TCK-20261011-0a1b2c3d", dict(PAYLOAD)))
            again["attach"]("TCK-20261011-0a1b2c3d", dict(PAYLOAD))
            facts["a 401 is refused by name and the token is dropped"] = (first == "PackagerRefused:ATTACH_REFUSED:401"
                                                                         and len(reads2) == 2 and TOKEN not in first)
            old = op.live_ticket_ports({"api_base": CONFIG["api_base"], "email": "svc@example.invalid",
                                        "secret_name": "x"}, read_secret=read_secret, http=http)
            facts["a binding with an email gives the refusing port"] = (
                refused(lambda: old["attach"]("TCK-20261011-0a1b2c3d", dict(PAYLOAD))) == "PackagerRefused:PACKAGER_PRINCIPAL_UNSET")
            spec = importlib.util.spec_from_file_location("builder", B + "build_resident_package.py")
            builder = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(builder)
            q = "https://sqs.us-east-1.amazonaws.com/000000000000/example-commentary-ready"
            facts["builder accepts the two-key binding"] = builder.optional_bindings(
                commentary_ready_queue_url=q, packager=dict(CONFIG)) == {"commentary_ready_queue_url": q, "packager": CONFIG}
            facts["builder refuses an email"] = refused(lambda: builder.optional_bindings(
                commentary_ready_queue_url=q, packager=dict(CONFIG, email="svc@example.invalid"))) == "ValueError:BINDING_PACKAGER_KEYS"
            import resident_installed as ri
            facts["runtime keys are api_base + secret_name"] = set(ri.PACKAGER_KEYS) == {"api_base", "secret_name"}
        except Exception as exc:
            print("AR-G42-FAIL probe %s: %s" % (type(exc).__name__, str(exc)[:200].replace(TOKEN, "<token>")))
            return 1
        wrong = [k for k, ok in facts.items() if not ok]
        for k, ok in facts.items():
            print("%s: %s" % ("yes" if ok else "NO ", k))
        if wrong:
            print("AR-G42-FAIL %d of %d facts wrong: %s" % (len(wrong), len(facts), "; ".join(wrong)[:300]))
            return 1
        print("AR-G42-OK facts=%d" % len(facts))
        return 0
    if mode == "regress":
        sets = (("research", R + "ycharts/research/tests", 281), ("factory", R + "reports/tests/test_resident_installed.py", 19),
                ("binding", R + "reports/tests/test_resident_packager_binding.py", 18), ("builder", B + "test_build_resident_bindings.py", 26))
        failed, parts = [], []
        for name, target, need in sets:
            rc, line, passed = pytest_line(target)
            print("%s: %s" % (name, line))
            parts.append("%s=%d" % (name, passed))
            if rc != 0 or bad_count(line) or passed < need:
                failed.append("%s rc=%d passed=%d (need >= %d)" % (name, rc, passed, need))
        if failed:
            print("AR-G42-REGRESS-FAIL " + "; ".join(failed))
            return 1
        print("AR-G42-REGRESS-OK " + " ".join(parts))
        return 0
    raise SystemExit(__doc__)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
