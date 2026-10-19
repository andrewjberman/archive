"""IRPT_BCKEND workstream ~PM round 15 (issuer 2.0.0_SA_COO~P2) -- the check of one READ order: why 49 Financial's holdings gate refuses the 2026-10-16 candidate on a third lost account (row D2-S240; IB2 msg 10712).

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

This check grades the SHAPE and the CITATIONS of the findings, never their truth: whether the account really holds positions or the partitions really fail the 95 percent floor is a JUDGMENT the issuer grades by re-reading the source itself.

  IBHX1  IB-hx-1  the findings file
    AC1  deliverables/0.9.0_WK_IRPT_BCKEND~458/IBhx1_findings.json has the fixed fields: exactly three accounts (one gone_not_exempt, two exempt_listed) with distinct 12-hex hashed ids and non-negative integer source-presence counts, exactly four partition records whose percent equals floor(account_count*100/prior_account_count), four lost_count_per_fire records (the fires 2026-10-14, 10-15, 10-16, 10-19), a decision line whose cited file:line exists at HEAD with the stated hash, a reason and a verdict from the closed sets
    AC2  nothing in the worker's deliverables folder carries a raw account identifier: no cli_ or acc_ ids, no 9-or-more digit run, no e-mail address, no hex run of 13 to 63 characters
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

DELIVD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~458"
FINDINGS = DELIVD + "/IBhx1_findings.json"
REASONS = ("HAS_POSITIONS_IN_A_SOURCE_TABLE", "PARTITION_INCOMPLETE", "PRIOR_PARTITION_ABSENT", "CLOSED_MARKER_MISSING", "OTHER")
VERDICTS = ("BUILD_FAULT_ACCOUNT_HAS_SOURCE_POSITIONS", "SOURCE_ABSENT_BUT_EXEMPTION_TESTS_FAIL", "CLOSURE_WITHOUT_MARKER", "UNDETERMINED")
TABLES = ("positions", "balance")
DAYS = ("candidate", "prior")
fail = P6.fail


def _line_hash(rel, line):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("cited file %s does not exist at HEAD" % rel)
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    if not isinstance(line, int) or line < 1 or line > len(lines):
        fail("cited line %r is outside %s (%d lines)" % (line, rel, len(lines)))
    return hashlib.sha256(lines[line - 1].strip().encode("utf-8")).hexdigest()


def _nonneg(x):
    return isinstance(x, int) and not isinstance(x, bool) and x >= 0


def ac1(_):
    f = P6.ROOT / FINDINGS
    if not f.is_file():
        fail("no %s" % FINDINGS)
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as exc:
        fail("findings do not parse: %s" % exc)
    if d.get("firm") != "49financial" or d.get("candidate_day") != "2026-10-16" or d.get("prior_day") != "2026-10-15":
        fail("firm must read 49financial, candidate_day 2026-10-16 and prior_day 2026-10-15")
    accts = d.get("accounts")
    if not isinstance(accts, list) or len(accts) != 3:
        fail("accounts must hold exactly three records (one gone_not_exempt, two exempt_listed)")
    roles = sorted(a.get("role") for a in accts if isinstance(a, dict))
    if roles != ["exempt_listed", "exempt_listed", "gone_not_exempt"]:
        fail("roles must be one gone_not_exempt and two exempt_listed; found %s" % roles)
    ids = [a.get("hashed_id") for a in accts]
    if len(set(ids)) != 3 or not all(isinstance(x, str) and re.fullmatch(r"[0-9a-f]{12}", x) for x in ids):
        fail("each account needs a distinct hashed_id of 12 lowercase hex characters (the first 12 of a sha256, never the id)")
    for a in accts:
        for tb in TABLES:
            row = (a.get("source_rows") or {}).get(tb)
            if not isinstance(row, dict) or not all(_nonneg(row.get(day)) for day in DAYS):
                fail("each account needs source_rows.%s.{candidate,prior} as non-negative integers" % tb)
        if not isinstance(a.get("closed_marker"), bool):
            fail("each account needs a boolean closed_marker")
    parts = d.get("partitions")
    if not isinstance(parts, list) or len(parts) != 4:
        fail("partitions must hold exactly four records (positions and balance, candidate and prior)")
    seen = set()
    for p in parts:
        ok = isinstance(p, dict) and p.get("table") in TABLES and p.get("day") in DAYS and _nonneg(p.get("account_count")) and _nonneg(p.get("prior_account_count")) and _nonneg(p.get("percent_of_prior"))
        if not ok:
            fail("each partition record needs table, day, account_count, prior_account_count and percent_of_prior")
        seen.add((p["table"], p["day"]))
        want = (p["account_count"] * 100) // p["prior_account_count"] if p["prior_account_count"] else None
        if want is None or p["percent_of_prior"] != want:
            fail("percent_of_prior must equal floor(account_count*100/prior_account_count) with a non-zero prior count")
    if seen != {(t, dy) for t in TABLES for dy in DAYS}:
        fail("the four partition records must be positions and balance for candidate and prior, once each")
    lcf = d.get("lost_count_per_fire")
    if not isinstance(lcf, list) or len(lcf) != 4:
        fail("lost_count_per_fire must hold exactly four records, one per refusing fire")
    if sorted(r.get("fire_date") for r in lcf if isinstance(r, dict)) != ["2026-10-14", "2026-10-15", "2026-10-16", "2026-10-19"]:
        fail("lost_count_per_fire must name the fire dates 2026-10-14, 2026-10-15, 2026-10-16 and 2026-10-19, once each")
    if not all(_nonneg(r.get("account_lost_count")) and _nonneg(r.get("listed_absent_at_source")) for r in lcf):
        fail("each lost_count_per_fire record needs non-negative integers account_lost_count and listed_absent_at_source")
    dl = d.get("decision_line") or {}
    if not isinstance(dl.get("file"), str) or not isinstance(dl.get("line"), int) or not isinstance(dl.get("excerpt_sha256"), str):
        fail("decision_line must carry file, line and excerpt_sha256")
    if _line_hash(dl["file"], dl["line"]) != dl["excerpt_sha256"]:
        fail("decision_line: the sha256 of the stripped line %s:%d differs from the stated hash" % (dl["file"], dl["line"]))
    if not isinstance(dl.get("what"), str) or not (10 <= len(dl["what"]) <= 300):
        fail("decision_line.what must be a sentence of 10 to 300 characters")
    if d.get("why_not_exempt") not in REASONS:
        fail("why_not_exempt must be one of %s" % ", ".join(REASONS))
    if d.get("verdict") not in VERDICTS:
        fail("verdict must be one of %s" % ", ".join(VERDICTS))
    ev = d.get("evidence_for_verdict")
    if not isinstance(ev, str) or not (10 <= len(ev) <= 400):
        fail("evidence_for_verdict must be 10 to 400 characters")
    rd = d.get("reads") or {}
    if rd.get("aws_writes") != 0 or rd.get("s3_puts") != 0:
        fail("reads.aws_writes and reads.s3_puts must be 0")
    print("OK: findings well formed; three accounts, four consistent partition records, the decision line matches its line at HEAD")


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
    print("OK: %d file(s) scanned, no raw account identifier, e-mail, long digit run or odd-length hex run" % len(files))


def ac3(_):
    p = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % p.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in p.stdout.split() if x.strip()]
    if not files:
        fail("the worker's commit is empty")
    bad = [x for x in files if not (x.startswith(DELIVD + "/") or "INVESTIGATION_v1.md" in x or "TO-IB-hx-1" in x)]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    if FINDINGS not in files:
        fail("the commit must contain %s" % FINDINGS)
    print("OK: one commit, the findings file in it, nothing outside the order's paths, no write under infra/ or data/")


CHECKS = {"IBHX1-AC1": ac1, "IBHX1-AC2": ac2, "IBHX1-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p258_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
