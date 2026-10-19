"""IRPT_BCKEND workstream ~PM round 14 (issuer 2.0.0_SA_COO~P2) -- the check of one READ order: which build stage drops the 6 Cottonwood clients the runner's guard refused on 2026-10-14, and what they share (CTO ruling on row D2-S239, msg 10699).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

This check grades the SHAPE and the CITATIONS of the findings, never their truth: whether the named stage really drops the clients is a JUDGMENT the issuer grades by re-tracing it itself.

  IBCW1  IB-cw-1  the findings file
    AC1  deliverables/0.9.0_WK_IRPT_BCKEND~456/IBcw1_findings.json has the fixed fields; 6 distinct hashed ids; every file:line it cites exists at HEAD and the sha256 of that stripped line equals the stated excerpt hash; the parked-link check is recorded as done first; counts are consistent
    AC2  nothing in the worker's deliverables folder carries a raw client identifier: no cli_ or acc_ ids, no 9-or-more digit run, no e-mail address, no hex run of 13 to 63 characters
    AC3  the worker's ONE commit (HEAD~1..HEAD) touches only the order's paths (its deliverables folder, the surprise file, the order) and writes no file under infra/ or data/
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "r196"))
import p196_cells as P6  # noqa: E402

DELIVD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~456"
FINDINGS = DELIVD + "/IBcw1_findings.json"
VERDICTS = ("BUILD_FAULT", "GENUINE_REMOVAL", "UNDETERMINED")
fail = P6.fail


def _line_hash(rel, line):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("cited file %s does not exist at HEAD" % rel)
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    if not isinstance(line, int) or line < 1 or line > len(lines):
        fail("cited line %r is outside %s (%d lines)" % (line, rel, len(lines)))
    return hashlib.sha256(lines[line - 1].strip().encode("utf-8")).hexdigest()


def _cite(obj, what):
    if not isinstance(obj, dict) or not isinstance(obj.get("file"), str) or not isinstance(obj.get("line"), int) or not isinstance(obj.get("excerpt_sha256"), str):
        fail("%s must carry file, line and excerpt_sha256" % what)
    got = _line_hash(obj["file"], obj["line"])
    if got != obj["excerpt_sha256"]:
        fail("%s: the sha256 of the stripped line %s:%d is %s, the findings state %s" % (what, obj["file"], obj["line"], got[:12], obj["excerpt_sha256"][:12]))


def ac1(_):
    f = P6.ROOT / FINDINGS
    if not f.is_file():
        fail("no %s" % FINDINGS)
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as exc:
        fail("findings do not parse: %s" % exc)
    if d.get("firm") != "cottonwood" or d.get("as_of") != "2026-10-14":
        fail("firm must read cottonwood and as_of 2026-10-14")
    ids = d.get("dropped_hashed_ids")
    if d.get("dropped_count") != 6 or not isinstance(ids, list) or len(ids) != 6 or len(set(ids)) != 6:
        fail("dropped_count must be 6 with six distinct hashed ids")
    if not all(isinstance(x, str) and re.fullmatch(r"[0-9a-f]{12}", x) for x in ids):
        fail("every hashed id must be 12 lowercase hex characters (the first 12 of a sha256, never the id)")
    st = d.get("stage") or {}
    _cite(st, "stage")
    if not isinstance(st.get("what"), str) or not (10 <= len(st["what"]) <= 300):
        fail("stage.what must be a sentence of 10 to 300 characters")
    pl = d.get("parked_link") or {}
    if pl.get("checked_first") is not True or not isinstance(pl.get("what"), str) or not pl["what"].strip() or not isinstance(pl.get("used_by_build"), bool):
        fail("parked_link must read checked_first true, a non-empty what and a boolean used_by_build")
    if pl.get("used_by_build") is True:
        _cite(pl, "parked_link")
    attrs = (d.get("shared") or {}).get("attributes")
    if not isinstance(attrs, list) or not attrs:
        fail("shared.attributes must be a non-empty list")
    for a in attrs:
        ok = isinstance(a, dict) and isinstance(a.get("name"), str) and a["name"].strip()
        ok = ok and all(isinstance(a.get(k), int) for k in ("dropped_with", "dropped_total", "retained_with", "retained_total"))
        ok = ok and a["dropped_total"] == 6 and 0 <= a["dropped_with"] <= 6 and a["retained_total"] >= a["retained_with"] >= 0
        if not ok:
            fail("each shared attribute needs a name and consistent integer counts (dropped_total 6, retained_with <= retained_total)")
    if d.get("verdict") not in VERDICTS:
        fail("verdict must be one of %s" % ", ".join(VERDICTS))
    ev = d.get("evidence_for_verdict")
    if not isinstance(ev, str) or not (10 <= len(ev) <= 400):
        fail("evidence_for_verdict must be 10 to 400 characters")
    rd = d.get("reads") or {}
    if rd.get("aws_writes") != 0 or rd.get("s3_puts") != 0:
        fail("reads.aws_writes and reads.s3_puts must be 0")
    print("OK: findings well formed; stage and parked-link citations match their lines at HEAD; six hashed ids; counts consistent")


FORBIDDEN = (
    (re.compile(r"\bcli_[0-9a-fA-F]{6,}"), "a cli_ client id"),
    (re.compile(r"\bacc_[0-9a-fA-F]{12,}"), "an acc_ account id"),
    (re.compile(r"(?<![0-9A-Za-z])\d{9,}(?![0-9A-Za-z])"), "a 9-or-more digit run"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "an e-mail address"),
)
HEXRUN = re.compile(r"(?<![0-9a-fA-F])[0-9a-fA-F]{13,63}(?![0-9a-fA-F])")


def ac2(_):
    root = P6.ROOT / DELIVD
    if not root.is_dir():
        fail("no folder %s" % DELIVD)
    files = [p for p in root.rglob("*") if p.is_file()]
    if not files:
        fail("the deliverables folder is empty")
    for p in files:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for rx, what in FORBIDDEN:
            if rx.search(t):
                fail("%s carries %s" % (p.name, what))
        if HEXRUN.search(t):
            fail("%s carries a hex run of 13 to 63 characters (hashed ids are exactly 12; a full sha256 is 64)" % p.name)
    print("OK: %d file(s) scanned, no raw client identifier, e-mail, long digit run or odd-length hex run" % len(files))


def ac3(_):
    p = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % p.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in p.stdout.split() if x.strip()]
    if not files:
        fail("the worker's commit is empty")
    bad = [x for x in files if not (x.startswith(DELIVD + "/") or "INVESTIGATION_v1.md" in x or "TO-IB-cw-1" in x)]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    if not any(x == FINDINGS for x in files):
        fail("the commit must contain %s" % FINDINGS)
    print("OK: one commit, the findings file in it, nothing outside the order's paths, no write under infra/ or data/")


CHECKS = {"IBCW1-AC1": ac1, "IBCW1-AC2": ac2, "IBCW1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p257_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
