"""IRPT_ANLREQ AR-g-67 checks (issuer 2.0.0_SA_COO~G2). Run from the worktree root.

    python ar_g67_checks.py g67       the ticket-confirmation module answers its twelve direct cases, and the eight named new tests exist and pass
    python ar_g67_checks.py regress   seven existing test files (run one at a time) still pass, 65 tests in all

Prints one RESULT line: AR-G67-OK / AR-G67-FAIL or AR-G67-REGRESS-OK / AR-G67-REGRESS-FAIL; rc 0 only on OK. ASCII only.
"""
import importlib.util
import re
import subprocess
import sys

R = "infra/aws/lambda/investor-reporting/"
MODULE = R + "ycharts/generate/ticket_confirmation.py"
NEW_TESTS = {
    R + "ycharts/generate/tests/test_ticket_stamp.py": [
        "test_accept_records_ticket_confirmed_true_only_when_the_service_says_true",
        "test_client_cannot_send_ticket_confirmed",
        "test_confirm_failure_leaves_the_record_unstamped_and_the_request_accepted",
        "test_replay_returns_the_prior_record_unchanged",
    ],
    R + "ycharts/generate/tests/test_producer_for_ticket.py": [
        "test_producer_for_admits_a_confirmed_record",
        "test_producer_for_refuses_an_unconfirmed_ticket_record",
        "test_producer_for_keeps_the_allow_list",
        "test_opal_stores_uses_the_same_choice",
    ],
}
EXISTING = [R + "ycharts/generate/tests/test_acceptance_actor.py", R + "ycharts/generate/tests/test_commentary_requested_member.py",
            R + "ycharts/generate/tests/test_ready_signal_ticket_gate.py", R + "ycharts/generate/tests/test_producer_actor.py",
            R + "ycharts/generate/tests/test_opal_thread_integration.py", R + "reports/tests/test_resident_installed.py",
            R + "reports/tests/test_generate_installed.py"]
TID = "TCK-20261015-0a1b2c3d"
EMAIL = "staff.user@opalinvest.com"


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


class Table:
    """A fake low-level DynamoDB client: one get_item answer, counted, or an exception."""

    def __init__(self, item=None, boom=None):
        self.item, self.boom, self.calls = item, boom, []

    def get_item(self, **kw):
        self.calls.append(kw)
        if self.boom is not None:
            raise self.boom
        return {"Item": self.item} if self.item is not None else {}


def ticket(**over):
    base = {"ticket_id": {"S": TID}, "ticket_type": {"S": "analysis_request"}, "source": {"S": "dashboard_form:analysis"},
            "requester": {"M": {"email": {"S": EMAIL}, "name": {"S": "A Person"}, "firm": {"S": "49financial"}}}}
    base.update(over)
    return {k: v for k, v in base.items() if v is not None}


def cases(tc):
    out = {}
    t = Table(ticket())
    confirm = tc.make_confirm_ticket(t, "opal-tickets")
    out["a matching ticket confirms, with one consistent GetItem"] = (
        confirm(TID, EMAIL) is True and len(t.calls) == 1 and t.calls[0].get("TableName") == "opal-tickets"
        and t.calls[0].get("Key") == {"ticket_id": {"S": TID}} and t.calls[0].get("ConsistentRead") is True)
    out["the filer match ignores case"] = tc.make_confirm_ticket(Table(ticket()), "opal-tickets")(TID, EMAIL.upper()) is True
    out["another type is not confirmed"] = tc.make_confirm_ticket(Table(ticket(ticket_type={"S": "trade_request"})), "opal-tickets")(TID, EMAIL) is False
    out["a non-dashboard source is not confirmed"] = tc.make_confirm_ticket(Table(ticket(source={"S": "svc_create"})), "opal-tickets")(TID, EMAIL) is False
    out["another filer is not confirmed"] = tc.make_confirm_ticket(Table(ticket()), "opal-tickets")(TID, "someone.else@opalinvest.com") is False
    out["an absent ticket is not confirmed"] = tc.make_confirm_ticket(Table(None), "opal-tickets")(TID, EMAIL) is False
    out["a missing requester is not confirmed"] = tc.make_confirm_ticket(Table(ticket(requester=None)), "opal-tickets")(TID, EMAIL) is False
    boom = Table(boom=RuntimeError("secret-xyz-token"))
    try:
        got = tc.make_confirm_ticket(boom, "opal-tickets")(TID, EMAIL)
    except Exception:
        got = "RAISED"
    out["a read error is False, never raised"] = got is False and len(boom.calls) == 1
    t2 = Table(ticket())
    bad = [tc.make_confirm_ticket(t2, "opal-tickets")(x, EMAIL) for x in ("TCK-1", "", None, 5, TID + "x", "tck-20261015-0a1b2c3d")]
    out["a malformed ticket id is False with no read"] = bad == [False] * 6 and t2.calls == []
    t3 = Table(ticket())
    bad = [tc.make_confirm_ticket(t3, "opal-tickets")(TID, x) for x in ("", None, 5, "   ")]
    out["a blank principal is False with no read"] = bad == [False] * 4 and t3.calls == []
    refused = []
    for name in ("", None, 5):
        try:
            tc.make_confirm_ticket(Table(), name)
            refused.append("NO-REFUSAL")
        except ValueError as exc:
            refused.append(str(exc))
    out["a blank table name is refused"] = refused == ["TICKET_TABLE"] * 3
    out["the result is a plain bool"] = type(tc.make_confirm_ticket(Table(ticket()), "opal-tickets")(TID, EMAIL)) is bool
    return out


def main(mode):
    if mode == "g67":
        try:
            spec = importlib.util.spec_from_file_location("ticket_confirmation", MODULE)
            tc = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(tc)
            tc.make_confirm_ticket
        except Exception as exc:
            print("AR-G67-FAIL import %s: %s" % (type(exc).__name__, str(exc)[:160]))
            return 1
        try:
            got = cases(tc)
        except Exception as exc:
            print("AR-G67-FAIL a case raised %s: %s" % (type(exc).__name__, str(exc)[:200]))
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
            print("AR-G67-FAIL wrong=%s missing=%s rc=%d passed=%d (need >= %d)" % (wrong or "none", missing or "none", rc, passed, need))
            return 1
        print("AR-G67-OK direct=%d named=%d passed=%d" % (len(got), need, passed))
        return 0
    if mode == "regress":
        total, bad = 0, []
        for path in EXISTING:
            rc, line, passed, text = pytest_run([path])
            print("%s: %s" % (path.split("/")[-1], line[:70]))
            total += passed
            if rc != 0 or bad_count(line) or passed == 0:
                bad.append(path.split("/")[-1])
        if bad or total < 65:
            print("AR-G67-REGRESS-FAIL files=%s passed=%d (need >= 65)" % (bad or "none", total))
            return 1
        print("AR-G67-REGRESS-OK passed=%d" % total)
        return 0
    print("usage: ar_g67_checks.py g67|regress")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
