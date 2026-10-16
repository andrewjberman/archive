#!/usr/bin/env python3
"""IRPT_ANLREQ round 4, cell AR-v-32, SITTING 2 (2.0.0_SA_COO~V2): the checks of the applier's record.

The applier (0.7.0_AE_CloudOps~IB2) writes ONE record, A_RUN_AR_V33.txt, one token-led line per fact. These checks read that
record only (no network, no AWS); the issuer re-reads the live rows and tickets itself at the drain.

  arma      F1 (the fixture write), B1/B2/A1 (the rows read before), S1 (the status route answered the failure's code and
            words for the arm-A request) and P1/P2 (the words showed under the arm-A ticket, the page stayed intact, the
            canvas read rgb(244, 246, 250), a screenshot exists, the origin was http://localhost:5174).
            Prints V33-ARMA-OK or V33-ARMA-FAIL <word>.
  armb      B3 (the packaged ticket), S3 (the page made NO status read for its request: it has no irpt-jobs row, so the
            "row also failed" half of arm B is OWED to the first packaged ticket that has one) and P3 (the packaged ticket
            shows NO failure words and its package block shows). Prints V33-ARMB-OK or V33-ARMB-FAIL <word>.
  restore   R1 (the minted staff user ABSENT, consistent), R3 (the fixture's report_ref ABSENT and the ticket's item hash
            equal to its pre-write hash), and no line carries a password or a hash. Prints V33-RESTORE-OK or -FAIL <word>.
  --self-test   a good record, nine one-line mutants and a record with a password line; prints V33-SELFTEST-OK.

--record PATH overrides the default record path.
"""
import re
import sys
import tempfile
from pathlib import Path

DEFAULT = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_arv33/A_RUN_AR_V33.txt"
TICKET_A = "TCK-20261015-944c84f8"
TICKET_B = "TCK-20261014-2965a5e0"
REQ_A = "REQ-d47252fe74634d0c5cdd8067"
REQ_B = "REQ-28a5ca6be3b7f438a9ca8217"
CODE = "COMMENTARY_DRAFT_REFUSED"
CANVAS = "rgb(244, 246, 250)"
ORIGIN = "http://localhost:5174"


def _lines(path):
    p = Path(path)
    return p.read_text(encoding="utf-8", errors="replace").splitlines() if p.is_file() else None


def _line(lines, token):
    hits = [ln for ln in lines if ln.startswith(token + " ")]
    return hits[0] if len(hits) == 1 else None


def check_arma(lines):
    f1 = _line(lines, "F1")
    if not f1 or TICKET_A not in f1 or ("request_id=" + REQ_A) not in f1 or "written=YES" not in f1 or "recorded_by=fixture" not in f1:
        return "F1"
    b1 = _line(lines, "B1")
    if not b1 or "hop_failure=ABSENT" not in b1:
        return "B1"
    b2 = _line(lines, "B2")
    if not b2 or TICKET_A not in b2 or "package=ABSENT" not in b2 or "report_ref=ABSENT" not in b2:
        return "B2"
    a1 = _line(lines, "A1")
    if not a1 or ("code=" + CODE) not in a1 or not re.search(r"\bat=\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d", a1):
        return "A1"
    s1 = _line(lines, "S1")
    if not s1 or "http=200" not in s1 or ("public_reason_code=" + CODE) not in s1 or "action=NONE" not in s1 or ("request_id=" + REQ_A) not in s1:
        return "S1"
    p1 = _line(lines, "P1")
    if not p1 or TICKET_A not in p1:
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
    if not r2 or r2.split("origin=", 1)[-1].strip() != ORIGIN:
        return "R2"
    return None


def check_armb(lines):
    b3 = _line(lines, "B3")
    if not b3 or TICKET_B not in b3 or "package=PRESENT" not in b3:
        return "B3"
    s3 = _line(lines, "S3")
    if not s3 or ("request_id=" + REQ_B) not in s3 or "count=0" not in s3:
        return "S3"
    p3 = _line(lines, "P3")
    if not p3 or TICKET_B not in p3:
        return "P3"
    for need in ("words_shown=NO", "package_block=YES", "page_intact=YES"):
        if need not in p3:
            return "P3:" + need
    m = re.search(r"screenshot=(\S+\.png)", p3)
    if not m or not Path(m.group(1)).is_file() or Path(m.group(1)).stat().st_size < 1000:
        return "P3:screenshot"
    return None


def check_restore(lines):
    r1 = _line(lines, "R1")
    if not r1 or "users_row=ABSENT" not in r1 or "consistent=YES" not in r1:
        return "R1"
    r3 = _line(lines, "R3")
    if not r3 or TICKET_A not in r3 or "report_ref=ABSENT" not in r3 or "item_hash_equals_pre=YES" not in r3:
        return "R3"
    for ln in lines:
        low = ln.lower()
        if "passwordhash" in low or re.search(r"password\s*[=:]\s*\S", low) or "$2b$" in ln:
            return "SECRET-IN-RECORD"
    return None


CHECKS = {"arma": check_arma, "armb": check_armb, "restore": check_restore}


def run(sub, path):
    lines = _lines(path)
    if lines is None:
        return "V33-%s-FAIL no-record" % sub.upper()
    why = CHECKS[sub](lines)
    return "V33-%s-OK" % sub.upper() if why is None else "V33-%s-FAIL %s" % (sub.upper(), why)


def _good(png_a, png_b):
    return [
        "F1 fixture ticket=%s request_id=%s written=YES recorded_by=fixture:AR-v-32-s2" % (TICKET_A, REQ_A),
        "B1 job_row tenant=49financial request_id=%s state=READY hop_failure=ABSENT" % REQ_A,
        "B2 ticket %s status=in_progress package=ABSENT report_ref=ABSENT" % TICKET_A,
        "A1 job_row hop_failure code=%s at=2026-10-16T17:20:00Z" % CODE,
        "S1 status_route request_id=%s http=200 public_reason_code=%s action=NONE" % (REQ_A, CODE),
        "P1 page ticket=%s words_shown=YES step_named=YES page_intact=YES blank_row=NO" % TICKET_A,
        "P2 canvas=%s screenshot=%s" % (CANVAS, png_a),
        "R2 browser origin=%s" % ORIGIN,
        "B3 ticket %s status=open package=PRESENT" % TICKET_B,
        "S3 status_reads request_id=%s count=0" % REQ_B,
        "P3 page ticket=%s words_shown=NO package_block=YES page_intact=YES screenshot=%s" % (TICKET_B, png_b),
        "R1 users_row=ABSENT consistent=YES",
        "R3 ticket %s report_ref=ABSENT item_hash_equals_pre=YES" % TICKET_A,
    ]


def selftest():
    with tempfile.TemporaryDirectory() as d:
        pa, pb = Path(d) / "a.png", Path(d) / "b.png"
        for p in (pa, pb):
            p.write_bytes(b"\x89PNG" + b"0" * 2000)
        good = _good(str(pa), str(pb))
        rec = Path(d) / "r.txt"
        rec.write_text("\n".join(good) + "\n", encoding="utf-8")
        for sub in CHECKS:
            if run(sub, rec) != "V33-%s-OK" % sub.upper():
                return "good record refused by " + sub
        mutants = [
            ("arma", 0, "F1 fixture ticket=%s request_id=REQ-000000000000000000000000 written=YES recorded_by=fixture:x" % TICKET_A),
            ("arma", 2, "B2 ticket %s status=in_progress package=ABSENT report_ref=PRESENT" % TICKET_A),
            ("arma", 4, "S1 status_route request_id=%s http=200 public_reason_code=ANALYSIS_REQUIRES_ATTENTION action=NONE" % REQ_A),
            ("arma", 5, "P1 page ticket=%s words_shown=NO step_named=NO page_intact=YES blank_row=NO" % TICKET_A),
            ("armb", 8, "B3 ticket %s status=open package=ABSENT" % TICKET_B),
            ("armb", 9, "S3 status_reads request_id=%s count=2" % REQ_B),
            ("armb", 10, "P3 page ticket=%s words_shown=YES package_block=YES page_intact=YES screenshot=%s" % (TICKET_B, pb)),
            ("restore", 11, "R1 users_row=PRESENT consistent=YES"),
            ("restore", 12, "R3 ticket %s report_ref=PRESENT item_hash_equals_pre=NO" % TICKET_A),
        ]
        for sub, i, bad in mutants:
            lines = list(good)
            lines[i] = bad
            rec.write_text("\n".join(lines) + "\n", encoding="utf-8")
            if run(sub, rec).endswith("-OK"):
                return "mutant %s/%d passed" % (sub, i)
        rec.write_text("\n".join(good + ["X note password=hunter2hunter2hunter2hunter2"]) + "\n", encoding="utf-8")
        if run("restore", rec).endswith("-OK"):
            return "secret in record passed"
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = selftest()
        print("V33-SELFTEST-OK" if why is None else "V33-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    if not argv or argv[0] not in CHECKS:
        print("usage: ar_v33_checks.py arma|armb|restore [--record PATH] | --self-test")
        return 2
    path = argv[argv.index("--record") + 1] if "--record" in argv else DEFAULT
    out = run(argv[0], path)
    print(out)
    return 0 if out.endswith("-OK") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
