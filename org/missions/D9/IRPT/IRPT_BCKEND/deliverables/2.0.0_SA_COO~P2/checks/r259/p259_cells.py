"""IRPT_BCKEND workstream ~PM round 16 (issuer 2.0.0_SA_COO~P2) -- the check of one READ order: every reader of the directory's client key, and what a re-key (an account moving from an account-level key to a relationship-level key) moves for each (CTO ruling on row D2-S239, msg 10788: "list every reader of the client key (pages, HMAC lists, exports) and state what the re-key moves for each").

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

This check grades the SHAPE and the CITATIONS of the findings, never their truth: whether a reader really behaves as stated is a JUDGMENT the issuer grades by re-reading the cited lines itself.

  IBCW3  IB-cw-3  the findings file
    AC1  deliverables/0.9.0_WK_IRPT_BCKEND~459/IBcw3_findings.json has the fixed fields: at least four readers with distinct ids, kinds from the closed set (REFRESH_COMPARE, HMAC_LIST and RUNNER among them), every cited file:line existing at HEAD with the stated hash, closed-set keyed_on and rekey_effect, a census naming the terms searched (client_id, entry_key, relationship_id among them) with consistent counts, and a cited release_path
    AC2  nothing in the worker's deliverables folder carries a raw identifier: no cli_ or acc_ ids, no 9-or-more digit run, no e-mail address, no hex run of 13 to 63 characters
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

DELIVD = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~459"
FINDINGS = DELIVD + "/IBcw3_findings.json"
KINDS = ("PAGE", "API", "HMAC_LIST", "EXPORT", "REFRESH_COMPARE", "RUNNER", "TEST", "OTHER")
KEYED = ("client_id", "relationship_id", "entry_key", "account_ids", "other")
EFFECTS = ("NONE", "KEY_CHANGES_ENTRY_REMAINS", "ENTRY_LOST", "UNKNOWN")
MUST_KINDS = ("REFRESH_COMPARE", "HMAC_LIST", "RUNNER")
MUST_TERMS = ("client_id", "entry_key", "relationship_id")
fail = P6.fail


def _line_hash(rel, line):
    f = P6.ROOT / rel
    if not f.is_file():
        fail("cited file %s does not exist at HEAD" % rel)
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    if not isinstance(line, int) or isinstance(line, bool) or line < 1 or line > len(lines):
        fail("cited line %r is outside %s (%d lines)" % (line, rel, len(lines)))
    return hashlib.sha256(lines[line - 1].strip().encode("utf-8")).hexdigest()


def _cite(obj, what):
    if not isinstance(obj, dict) or not isinstance(obj.get("file"), str) or not isinstance(obj.get("line"), int) or not isinstance(obj.get("excerpt_sha256"), str):
        fail("%s must carry file, line and excerpt_sha256" % what)
    got = _line_hash(obj["file"], obj["line"])
    if got != obj["excerpt_sha256"]:
        fail("%s: the sha256 of the stripped line %s:%d is %s, the findings state %s" % (what, obj["file"], obj["line"], got[:12], obj["excerpt_sha256"][:12]))
    if not isinstance(obj.get("what"), str) or not (10 <= len(obj["what"]) <= 300):
        fail("%s.what must be a sentence of 10 to 300 characters" % what)


def _count(x):
    return isinstance(x, int) and not isinstance(x, bool) and x >= 0


def ac1(_):
    f = P6.ROOT / FINDINGS
    if not f.is_file():
        fail("no %s" % FINDINGS)
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as exc:
        fail("findings do not parse: %s" % exc)
    if d.get("firm") != "cottonwood":
        fail("firm must read cottonwood")
    rs = d.get("readers")
    if not isinstance(rs, list) or len(rs) < 4:
        fail("readers must hold at least four records")
    ids = [r.get("id") for r in rs if isinstance(r, dict)]
    if len(ids) != len(rs) or len(set(ids)) != len(ids) or not all(isinstance(i, str) and re.fullmatch(r"R[0-9]{2}", i) for i in ids):
        fail("each reader needs a distinct id of the form R01, R02, ...")
    for r in rs:
        _cite(r, "reader %s" % r["id"])
        if r.get("kind") not in KINDS:
            fail("reader %s: kind must be one of %s" % (r["id"], ", ".join(KINDS)))
        if r.get("keyed_on") not in KEYED:
            fail("reader %s: keyed_on must be one of %s" % (r["id"], ", ".join(KEYED)))
        if r.get("rekey_effect") not in EFFECTS:
            fail("reader %s: rekey_effect must be one of %s" % (r["id"], ", ".join(EFFECTS)))
    kinds = {r["kind"] for r in rs}
    gone = [k for k in MUST_KINDS if k not in kinds]
    if gone:
        fail("the readers must include a %s; missing %s" % (", ".join(MUST_KINDS), ", ".join(gone)))
    c = d.get("census") or {}
    terms = c.get("terms")
    if not isinstance(terms, list) or not all(isinstance(t, str) and t for t in terms):
        fail("census.terms must be a list of the strings searched")
    miss = [t for t in MUST_TERMS if t not in terms]
    if miss:
        fail("census.terms must include %s; missing %s" % (", ".join(MUST_TERMS), ", ".join(miss)))
    if not (_count(c.get("files_scanned")) and c["files_scanned"] > 0 and _count(c.get("files_with_hits")) and c["files_with_hits"] <= c["files_scanned"]):
        fail("census needs files_scanned > 0 and files_with_hits <= files_scanned (integers)")
    if c["files_with_hits"] < len({r["file"] for r in rs}):
        fail("census.files_with_hits (%d) is below the number of distinct files the readers cite (%d)" % (c["files_with_hits"], len({r["file"] for r in rs})))
    _cite(d.get("release_path") or {}, "release_path")
    rd = d.get("reads") or {}
    if rd.get("aws_writes") != 0 or rd.get("s3_puts") != 0:
        fail("reads.aws_writes and reads.s3_puts must be 0")
    print("OK: findings well formed; %d readers, every citation matches its line at HEAD, the census names the terms, the release path is cited" % len(rs))


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
            fail("%s carries a hex run of 13 to 63 characters (a full sha256 is 64)" % p.name)
    print("OK: %d file(s) scanned, no raw identifier, e-mail, long digit run or odd-length hex run" % len(files))


def ac3(_):
    p = subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], cwd=str(P6.ROOT), capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        fail("git diff HEAD~1 HEAD failed: %s" % p.stderr.strip()[:200])
    files = [x.replace("\\", "/") for x in p.stdout.split() if x.strip()]
    if not files:
        fail("the worker's commit is empty")
    bad = [x for x in files if not (x.startswith(DELIVD + "/") or "INVESTIGATION_v1.md" in x or "TO-IB-cw-3" in x)]
    if bad:
        fail("the commit touches files outside the order's paths: %s" % bad)
    if FINDINGS not in files:
        fail("the commit must contain %s" % FINDINGS)
    print("OK: one commit, the findings file in it, nothing outside the order's paths, no write under infra/ or data/")


CHECKS = {"IBCW3-AC1": ac1, "IBCW3-AC2": ac2, "IBCW3-AC3": ac3}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[2] not in CHECKS:
        print("usage: p259_cells.py <repo_root> <%s>" % "|".join(CHECKS))
        sys.exit(2)
    P6.ROOT, P6.CID = Path(sys.argv[1]).resolve(), sys.argv[2]
    CHECKS[sys.argv[2]](None)
    print("%s PASS" % sys.argv[2])
