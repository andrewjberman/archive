"""Control for AR467-y-AC3: four mutants of the packager text must each make check_audit_wired.verdict() print BAD, and the real
packager must print OK. The mutants are built in memory from the real text; the packager file is never written.
Prints one line: CONTROL-FIRED m1=BAD m2=BAD m3=BAD m4=BAD real=OK, or CONTROL-MISSED <why>. ASCII only."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
CHECK = HERE.parent / "check_audit_wired.py"
spec = importlib.util.spec_from_file_location("check_audit_wired", str(CHECK))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

AUDIT_LINE = '    result["audit"] = _write_audit(ports, tenant, record, result)\n'
ANSWER_LINE = '    answer = ports["attach"](ticket_id, payload)\n'
WRITER_LINE = '        audit.write_audit(document, put)\n'
READY_RETURN = ('    return _attach(ports, ticket_id, tenant, report_ref, original_ref, None, None, request_id, _revision(record), record,\n')


def _once(text, anchor):
    assert text.count(anchor) == 1, "control anchor not found exactly once: %r" % anchor.strip()[:60]


def mutants(real):
    """m1: the audit helper is called twice in the shared tail; m2: the helper runs BEFORE the attach call in the tail;
    m3: the writer itself is called twice inside the helper; m4: the helper is also called on the READY path, outside the tail."""
    for anchor in (AUDIT_LINE, ANSWER_LINE, WRITER_LINE, READY_RETURN):
        _once(real, anchor)
    m1 = real.replace(AUDIT_LINE, AUDIT_LINE + AUDIT_LINE)
    m2 = real.replace(AUDIT_LINE, "").replace(ANSWER_LINE, AUDIT_LINE + ANSWER_LINE)
    m3 = real.replace(WRITER_LINE, WRITER_LINE + WRITER_LINE)
    m4 = real.replace(READY_RETURN, '    _write_audit(ports, tenant, record, {})\n' + READY_RETURN)
    return m1, m2, m3, m4


def main():
    real = checker.PACKAGER.read_text(encoding="utf-8")
    try:
        m1, m2, m3, m4 = mutants(real)
    except AssertionError as exc:
        print("CONTROL-MISSED %s" % exc)
        return 1
    v = [checker.verdict(text) for text in (m1, m2, m3, m4)]
    real_line = checker.verdict(real)
    fired = all(line.startswith("AUDIT-WIRED-BAD") for line in v) and real_line.startswith("AUDIT-WIRED-OK")
    if not fired:
        print("CONTROL-MISSED " + " | ".join(v + [real_line]))
        return 1
    print("CONTROL-FIRED m1=BAD m2=BAD m3=BAD m4=BAD real=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
