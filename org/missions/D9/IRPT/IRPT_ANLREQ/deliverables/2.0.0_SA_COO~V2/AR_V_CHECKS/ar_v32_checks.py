#!/usr/bin/env python3
"""IRPT_ANLREQ round 4, cell AR-v-32 (2.0.0_SA_COO~V2): the checks of the applier's record.

The applier (0.7.0_AE_CloudOps~AQ2) writes ONE record, A_RUN_AR_V32.txt, one token-led line per fact. These checks read
that record only (no network, no AWS); the issuer re-reads the live row and ticket itself at the drain.

  status    B1, B2, A1 and S1 hold: the row was clean, the ticket had no package, the failure was written, the status
            route answered it. Prints V32-STATUS-OK or V32-STATUS-FAIL <word>.
  page      P1 and P2 and R2 hold: the words showed under the ticket, the page stayed intact, the canvas read
            rgb(244, 246, 250), a screenshot file exists, the origin was http://localhost:5174.
            Prints V32-PAGE-OK or V32-PAGE-FAIL <word>.
  restore   R1 holds (the minted staff user row read ABSENT on a consistent read) and no line of the record carries a
            password or a hash. Prints V32-RESTORE-OK or V32-RESTORE-FAIL <word>.
  --self-test   runs each check on a good record and on each one-line mutant of it; prints V32-SELFTEST-OK.

--record PATH overrides the default record path.
"""
import re
import sys
import tempfile
from pathlib import Path

DEFAULT = "org/tier2_senior/0.7.0_AE_CloudOps~AQ2/deliverables/irpt_anlreq_arv32/A_RUN_AR_V32.txt"
TICKET = "TCK-20261015-944c84f8"
CODE = "COMMENTARY_DRAFT_REFUSED"
CANVAS = "rgb(244, 246, 250)"
ORIGIN = "http://localhost:5174"


def _lines(path):
    p = Path(path)
    if not p.is_file():
        return None
    return p.read_text(encoding="utf-8", errors="replace").splitlines()


def _line(lines, token):
    hits = [ln for ln in lines if ln.startswith(token + " ")]
    return hits[0] if len(hits) == 1 else None


def check_status(lines):
    b1 = _line(lines, "B1")
    if not b1 or "hop_failure=ABSENT" not in b1:
        return "B1"
    b2 = _line(lines, "B2")
    if not b2 or TICKET not in b2 or "package=ABSENT" not in b2:
        return "B2"
    a1 = _line(lines, "A1")
    if not a1 or ("code=" + CODE) not in a1 or not re.search(r"\bat=\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d", a1):
        return "A1"
    s1 = _line(lines, "S1")
    if not s1 or ("public_reason_code=" + CODE) not in s1 or "action=NONE" not in s1 or "http=200" not in s1:
        return "S1"
    return None


def check_page(lines):
    p1 = _line(lines, "P1")
    if not p1 or TICKET not in p1:
        return "P1"
    for need in ("words_shown=YES", "step_named=YES", "page_intact=YES", "blank_row=NO"):
        if need not in p1:
            return "P1:" + need
    p2 = _line(lines, "P2")
    if not p2 or ("canvas=" + CANVAS) not in p2:
        return "P2"
    m = re.search(r"screenshot=(\S+\.png)", p2)
    if not m or not Path(m.group(1)).is_file() or Path(m.group(1)).stat().st_size < 1000:
        return "P2:screenshot"
    r2 = _line(lines, "R2")
    if not r2 or ("origin=" + ORIGIN) not in r2 or r2.split("origin=", 1)[1].strip() != ORIGIN:
        return "R2"
    return None


def check_restore(lines):
    r1 = _line(lines, "R1")
    if not r1 or "users_row=ABSENT" not in r1 or "consistent=YES" not in r1:
        return "R1"
    for ln in lines:
        low = ln.lower()
        if "passwordhash" in low or re.search(r"password\s*[=:]\s*\S", low) or "$2b$" in ln:
            return "SECRET-IN-RECORD"
    return None


CHECKS = {"status": check_status, "page": check_page, "restore": check_restore}


def run(sub, path):
    lines = _lines(path)
    if lines is None:
        return "V32-%s-FAIL no-record" % sub.upper()
    why = CHECKS[sub](lines)
    return "V32-%s-OK" % sub.upper() if why is None else "V32-%s-FAIL %s" % (sub.upper(), why)


def _good(png):
    return [
        "B1 job_row tenant=49financial state=READY hop_failure=ABSENT",
        "B2 ticket %s status=in_progress package=ABSENT" % TICKET,
        "A1 job_row hop_failure code=%s at=2026-10-16T16:00:00Z" % CODE,
        "S1 status_route http=200 public_reason_code=%s action=NONE" % CODE,
        "P1 page ticket=%s words_shown=YES step_named=YES page_intact=YES blank_row=NO" % TICKET,
        "P2 canvas=%s screenshot=%s" % (CANVAS, png),
        "R2 browser origin=%s" % ORIGIN,
        "R1 users_row=ABSENT consistent=YES",
    ]


def selftest():
    with tempfile.TemporaryDirectory() as d:
        png = Path(d) / "s.png"
        png.write_bytes(b"\x89PNG" + b"0" * 2000)
        good = _good(str(png))
        rec = Path(d) / "r.txt"
        rec.write_text("\n".join(good) + "\n", encoding="utf-8")
        for sub in CHECKS:
            if run(sub, rec) != "V32-%s-OK" % sub.upper():
                return "good record refused by " + sub
        mutants = [  # (check, index of the line to damage, replacement)
            ("status", 0, "B1 job_row state=READY hop_failure=PRESENT"),
            ("status", 1, "B2 ticket %s status=in_progress package=PRESENT" % TICKET),
            ("status", 2, "A1 job_row hop_failure code=PACKAGER_REFUSED at=2026-10-16T16:00:00Z"),
            ("status", 3, "S1 status_route http=404 public_reason_code=%s action=NONE" % CODE),
            ("page", 4, "P1 page ticket=%s words_shown=NO step_named=YES page_intact=YES blank_row=NO" % TICKET),
            ("page", 5, "P2 canvas=rgb(0, 0, 0) screenshot=%s" % png),
            ("page", 6, "R2 browser origin=https://d2n2nzpeqf34ge.cloudfront.net"),
            ("restore", 7, "R1 users_row=PRESENT consistent=YES"),
        ]
        for sub, i, bad in mutants:
            lines = list(good)
            lines[i] = bad
            rec.write_text("\n".join(lines) + "\n", encoding="utf-8")
            if run(sub, rec).endswith("-OK"):
                return "mutant %s/%d passed" % (sub, i)
        leak = list(good) + ["X note password=hunter2hunter2hunter2hunter2"]
        rec.write_text("\n".join(leak) + "\n", encoding="utf-8")
        if run("restore", rec).endswith("-OK"):
            return "secret in record passed"
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = selftest()
        print("V32-SELFTEST-OK" if why is None else "V32-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    if not argv or argv[0] not in CHECKS:
        print("usage: ar_v32_checks.py status|page|restore [--record PATH] | --self-test")
        return 2
    path = argv[argv.index("--record") + 1] if "--record" in argv else DEFAULT
    out = run(argv[0], path)
    print(out)
    return 0 if out.endswith("-OK") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
