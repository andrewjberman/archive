#!/usr/bin/env python3
"""IRPT_ANLREQ round 5, cell AR-v-34 (2.0.0_SA_COO~V2): the checks of the applier's record for FWD-1 window 4's request.

The applier (0.7.0_AE_CloudOps~IB2) writes ONE record, A_RUN_AR_V34.txt, one token-led line per fact. The window-4 ticket and
request ids are NOT known when this file is pinned, so they are read from the record's own line L0 and every other line must
carry the same two ids. These checks read the record only (no network, no AWS); the issuer re-reads live rows at the drain.

  phase1    (the REAL link, before the package) L1 (the ticket's report_ref was recorded by the filing's step 4, never a
            fixture), B1/B2 (the row clean and no package before the drive), A1 (the failure stands), S1 (the status route
            answered the failure's code, action NONE), P1/P2 (the words showed, the page intact, canvas rgb(244, 246, 250),
            a screenshot exists, origin http://localhost:5174). Prints V34-PHASE1-OK or V34-PHASE1-FAIL <word>.
  phase2    (PACKAGED AND FAILED) B3 (the package is attached), A2 (a driven failure stands on the same row), S3 (the page
            made ZERO status reads for the request), P3 (the package block shows and NO failure words show, page intact,
            screenshot). Prints V34-PHASE2-OK or V34-PHASE2-FAIL <word>.
  restore   R1 and R2 (each minted staff user ABSENT, consistent) and the pair of row restores X1/X2 (each driven failure
            removed, the job row's item hash equal to its PRE), and no line carries a password or a hash. Prints
            V34-RESTORE-OK or V34-RESTORE-FAIL <word>.
  --self-test   a good record, nine one-line mutants and a record with a password line; prints V34-SELFTEST-OK.

--record PATH overrides the default record path.
"""
import re
import sys
import tempfile
from pathlib import Path

DEFAULT = "org/tier2_senior/0.7.0_AE_CloudOps~IB2/deliverables/irpt_anlreq_arv34/A_RUN_AR_V34.txt"
CANVAS = "rgb(244, 246, 250)"
ORIGIN = "http://localhost:5174"
TICKET_RE = re.compile(r"\bticket=(TCK-\d{8}-[0-9a-f]{8})\b")
REQ_RE = re.compile(r"\brequest_id=(REQ-[0-9a-f]{24})\b")


def _lines(path):
    p = Path(path)
    return p.read_text(encoding="utf-8", errors="replace").splitlines() if p.is_file() else None


def _line(lines, token):
    hits = [ln for ln in lines if ln.startswith(token + " ")]
    return hits[0] if len(hits) == 1 else None


def _ids(lines):
    l0 = _line(lines, "L0")
    if not l0:
        return None, None
    t, r = TICKET_RE.search(l0), REQ_RE.search(l0)
    return (t.group(1) if t else None), (r.group(1) if r else None)


def _shot(line):
    m = re.search(r"screenshot=(\S+\.png)", line or "")
    return bool(m) and Path(m.group(1)).is_file() and Path(m.group(1)).stat().st_size >= 1000


def check_phase1(lines):
    tk, rq = _ids(lines)
    if not tk or not rq:
        return "L0"
    l1 = _line(lines, "L1")
    if not l1 or tk not in l1 or rq not in l1 or "recorded_by=fixture" in l1 or "recorded_by=" not in l1 or "report_ref=PRESENT" not in l1:
        return "L1"
    b1 = _line(lines, "B1")
    if not b1 or rq not in b1 or "hop_failure=ABSENT" not in b1:
        return "B1"
    b2 = _line(lines, "B2")
    if not b2 or tk not in b2 or "package=ABSENT" not in b2:
        return "B2"
    a1 = _line(lines, "A1")
    if not a1 or rq not in a1 or "hop_failure=PRESENT" not in a1 or not re.search(r"\bcode=[A-Z_]+", a1):
        return "A1"
    code = re.search(r"\bcode=([A-Z_]+)", a1).group(1)
    s1 = _line(lines, "S1")
    if not s1 or rq not in s1 or "http=200" not in s1 or ("public_reason_code=" + code) not in s1 or "action=NONE" not in s1:
        return "S1"
    p1 = _line(lines, "P1")
    if not p1 or tk not in p1:
        return "P1"
    for need in ("words_shown=YES", "step_named=YES", "page_intact=YES", "blank_row=NO"):
        if need not in p1:
            return "P1:" + need
    p2 = _line(lines, "P2")
    if not p2 or ("canvas=" + CANVAS) not in p2:
        return "P2"
    if not _shot(p2):
        return "P2:screenshot"
    r3 = _line(lines, "R3")
    if not r3 or r3.split("origin=", 1)[-1].strip() != ORIGIN:
        return "R3"
    return None


def check_phase2(lines):
    tk, rq = _ids(lines)
    if not tk or not rq:
        return "L0"
    b3 = _line(lines, "B3")
    if not b3 or tk not in b3 or "package=PRESENT" not in b3:
        return "B3"
    a2 = _line(lines, "A2")
    if not a2 or rq not in a2 or "hop_failure=PRESENT" not in a2:
        return "A2"
    s3 = _line(lines, "S3")
    if not s3 or rq not in s3 or "count=0" not in s3:
        return "S3"
    p3 = _line(lines, "P3")
    if not p3 or tk not in p3:
        return "P3"
    for need in ("words_shown=NO", "package_block=YES", "page_intact=YES"):
        if need not in p3:
            return "P3:" + need
    if not _shot(p3):
        return "P3:screenshot"
    return None


def check_restore(lines):
    tk, rq = _ids(lines)
    if not tk or not rq:
        return "L0"
    for tok in ("R1", "R2"):
        r = _line(lines, tok)
        if not r or "users_row=ABSENT" not in r or "consistent=YES" not in r:
            return tok
    for tok in ("X1", "X2"):
        x = _line(lines, tok)
        if not x or rq not in x or "hop_failure=ABSENT" not in x or "item_hash_equals_pre=YES" not in x:
            return tok
    for ln in lines:
        low = ln.lower()
        if "passwordhash" in low or re.search(r"password\s*[=:]\s*\S", low) or "$2b$" in ln:
            return "SECRET-IN-RECORD"
    return None


CHECKS = {"phase1": check_phase1, "phase2": check_phase2, "restore": check_restore}


def run(sub, path):
    lines = _lines(path)
    if lines is None:
        return "V34-%s-FAIL no-record" % sub.upper()
    why = CHECKS[sub](lines)
    return "V34-%s-OK" % sub.upper() if why is None else "V34-%s-FAIL %s" % (sub.upper(), why)


def _good(pa, pb):
    tk, rq = "TCK-20261016-0a1b2c3d", "REQ-0123456789abcdef01234567"
    return [
        "L0 window4 ticket=%s request_id=%s" % (tk, rq),
        "L1 ticket=%s request_id=%s report_ref=PRESENT recorded_by=fwd1-staff@opal.invalid" % (tk, rq),
        "B1 job_row request_id=%s state=READY hop_failure=ABSENT" % rq,
        "B2 ticket=%s status=in_progress package=ABSENT" % tk,
        "A1 job_row request_id=%s hop_failure=PRESENT code=COMMENTARY_DRAFT_REFUSED at=2026-10-16T20:00:00Z" % rq,
        "S1 status_route request_id=%s http=200 public_reason_code=COMMENTARY_DRAFT_REFUSED action=NONE" % rq,
        "P1 page ticket=%s words_shown=YES step_named=YES page_intact=YES blank_row=NO" % tk,
        "P2 canvas=%s screenshot=%s" % (CANVAS, pa),
        "R3 browser origin=%s" % ORIGIN,
        "B3 ticket=%s status=in_progress package=PRESENT" % tk,
        "A2 job_row request_id=%s hop_failure=PRESENT code=COMMENTARY_DRAFT_REFUSED at=2026-10-16T21:00:00Z" % rq,
        "S3 status_reads request_id=%s count=0" % rq,
        "P3 page ticket=%s words_shown=NO package_block=YES page_intact=YES screenshot=%s" % (tk, pb),
        "R1 users_row=ABSENT consistent=YES",
        "R2 users_row=ABSENT consistent=YES",
        "X1 job_row request_id=%s hop_failure=ABSENT item_hash_equals_pre=YES" % rq,
        "X2 job_row request_id=%s hop_failure=ABSENT item_hash_equals_pre=YES" % rq,
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
            if run(sub, rec) != "V34-%s-OK" % sub.upper():
                return "good record refused by " + sub
        mutants = [
            ("phase1", 1, good[1].replace("recorded_by=fwd1-staff@opal.invalid", "recorded_by=fixture:AR-v-32-s2")),
            ("phase1", 3, good[3].replace("package=ABSENT", "package=PRESENT")),
            ("phase1", 5, good[5].replace("COMMENTARY_DRAFT_REFUSED", "ANALYSIS_REQUIRES_ATTENTION")),
            ("phase1", 6, good[6].replace("words_shown=YES", "words_shown=NO")),
            ("phase2", 9, good[9].replace("package=PRESENT", "package=ABSENT")),
            ("phase2", 11, good[11].replace("count=0", "count=2")),
            ("phase2", 12, good[12].replace("words_shown=NO", "words_shown=YES")),
            ("restore", 15, good[15].replace("item_hash_equals_pre=YES", "item_hash_equals_pre=NO")),
            ("restore", 14, good[14].replace("users_row=ABSENT", "users_row=PRESENT")),
        ]
        for sub, i, bad in mutants:
            lines = list(good)
            lines[i] = bad
            rec.write_text("\n".join(lines) + "\n", encoding="utf-8")
            if run(sub, rec).endswith("-OK"):
                return "mutant %s/%d passed" % (sub, i)
        rec.write_text("\n".join(good + ["X9 note password=hunter2hunter2hunter2hunter2"]) + "\n", encoding="utf-8")
        if run("restore", rec).endswith("-OK"):
            return "secret in record passed"
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = selftest()
        print("V34-SELFTEST-OK" if why is None else "V34-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    if not argv or argv[0] not in CHECKS:
        print("usage: ar_v34_checks.py phase1|phase2|restore [--record PATH] | --self-test")
        return 2
    path = argv[argv.index("--record") + 1] if "--record" in argv else DEFAULT
    out = run(argv[0], path)
    print(out)
    return 0 if out.endswith("-OK") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
