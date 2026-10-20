"""Control for AR467-y-AC3: three mutants of the packager text must each make check_audit_wired.verdict() print BAD, and the real
packager must print OK. The mutants are built in memory from the real text; the packager file is never written.
Prints one line: CONTROL-FIRED m1=BAD m2=BAD m3=BAD real=OK, or CONTROL-MISSED <why>. ASCII only."""
import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
CHECK = HERE.parent / "check_audit_wired.py"
spec = importlib.util.spec_from_file_location("check_audit_wired", str(CHECK))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

ATTACH_LINE = '    result, record, tenant = _attach_commentary(body, ports)\n'
AUDIT_LINE = '    result["audit"] = _write_audit(ports, tenant, record, result)\n'
WRITER_LINE = '        audit.write_audit(document, put)\n'


def mutants(real):
    """m1: the audit helper is called twice in the commentary path; m2: the audit helper runs BEFORE the attach;
    m3: the writer itself is called twice inside the audit helper."""
    assert real.count(ATTACH_LINE + AUDIT_LINE) == 1, "control anchor not found once in the packager text"
    assert real.count(WRITER_LINE) == 1, "writer anchor not found once in the packager text"
    m1 = real.replace(ATTACH_LINE + AUDIT_LINE, ATTACH_LINE + AUDIT_LINE + AUDIT_LINE)
    m2 = real.replace(ATTACH_LINE + AUDIT_LINE, AUDIT_LINE + ATTACH_LINE)
    m3 = real.replace(WRITER_LINE, WRITER_LINE + WRITER_LINE)
    return m1, m2, m3


def main():
    real = checker.PACKAGER.read_text(encoding="utf-8")
    try:
        m1, m2, m3 = mutants(real)
    except AssertionError as exc:
        print("CONTROL-MISSED %s" % exc)
        return 1
    v = [checker.verdict(text) for text in (m1, m2, m3)]
    real_line = checker.verdict(real)
    fired = all(line.startswith("AUDIT-WIRED-BAD") for line in v) and real_line.startswith("AUDIT-WIRED-OK")
    if not fired:
        print("CONTROL-MISSED " + " | ".join(v + [real_line]))
        return 1
    print("CONTROL-FIRED m1=BAD m2=BAD m3=BAD real=OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
