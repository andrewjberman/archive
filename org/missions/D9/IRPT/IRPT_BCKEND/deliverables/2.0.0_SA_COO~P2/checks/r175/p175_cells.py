"""IRPT_BCKEND round 175 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB175-1  IB-pr-507  READ-ONLY census of the investor-reporting host bundle: live object vs repository HEAD, member by member (CTO round-175 analysis section 3 item 1)
    AC1  the record's shape and arithmetic (denominators, one row per member, equal flags agree with the hashes)
    AC2  the check re-derives from git: every member's head_member_sha256 is the blob at HEAD; the guard's declared members all appear; every differing member carries commits
    AC3  the host's way of reading the bundle is cited (file, line, quote), and the bound counters read 0 with the live object's ETag unchanged before and after
  IB175-2  IB-pr-508  the tolerance test's import order is repaired (row W356-S3)
    AC1  test_runner_jsonschema_tolerance.py collects and passes alone
    AC2  the three builder suites pass together (rc 0)
    AC3  the repair touched that one test file only, in at most 12 changed lines
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
GOLD = "data/assets/scripts/gold/investor_reporting/"
CENSUS = D + "0.9.0_WK_IRPT_BCKEND~359/IB175-1_host_bundle_census.json"
REPAIR = D + "0.9.0_WK_IRPT_BCKEND~360/IB175-2_import_order.json"
TOL = GOLD + "tests/test_runner_jsonschema_tolerance.py"
BOUND_ZERO = ("aws_writes_made", "objects_uploaded", "functions_invoked", "ssm_commands_sent", "hosts_started", "accounts_written", "figures_written")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB175"))
    sys.exit(1)


def run(cmd, timeout=100, cwd=None):
    try:
        p = subprocess.run(cmd, cwd=str(cwd or ROOT), capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        fail("timeout: %s" % " ".join(map(str, cmd))[:100])
    except FileNotFoundError as e:
        fail("not found: %s" % e)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def load(rel):
    f = ROOT / rel
    if not f.is_file():
        fail("no %s" % rel)
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        fail("%s is not JSON: %s" % (rel, e))


def is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def is_sha(x):
    return isinstance(x, str) and re.fullmatch(r"[0-9a-f]{64}", x) is not None


def cite_resolves(rel, line, quote, what):
    f = ROOT / str(rel)
    if not f.is_file():
        fail("%s: file %r does not exist" % (what, rel))
    if not is_int(line) or line < 1 or not str(quote).strip():
        fail("%s: needs an integer line and a non-empty quote" % what)
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    window = re.sub(r"\s+", " ", "\n".join(lines[max(0, line - 4):line + 3]))
    if re.sub(r"\s+", " ", str(quote).strip()) not in window:
        fail("%s: the quote is not within 3 lines of %s:%s" % (what, rel, line))


def py_counts(out):
    out = re.sub(r"\x1b\[[0-9;]*m", "", out)
    m = {k: int(v) for v, k in re.findall(r"(\d+) (passed|failed|error|errors)", out)}
    return m.get("passed", 0), m.get("failed", 0), m.get("error", 0) + m.get("errors", 0)


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB175-1":
        r = load(CENSUS)
        mem = r.get("members") or []
        if arm == "AC1":
            den = r.get("denominator") or {}
            if not mem or den.get("members_in_live_bundle") != len(mem):
                fail("denominator.members_in_live_bundle must equal the number of member rows (%d)" % len(mem))
            differing = [m for m in mem if m.get("equal") is False]
            if den.get("members_differing") != len(differing):
                fail("denominator.members_differing must equal the rows with equal false (%d)" % len(differing))
            live = r.get("live_object") or {}
            for k in ("bucket", "key", "etag", "last_modified"):
                if not str(live.get(k, "")).strip():
                    fail("live_object.%s is required" % k)
            for m in mem:
                if not is_sha(m.get("live_member_sha256")) or not is_sha(m.get("head_member_sha256")):
                    fail("member %r needs 64-hex live_member_sha256 and head_member_sha256" % m.get("name"))
                if m.get("equal") is not (m["live_member_sha256"] == m["head_member_sha256"]):
                    fail("member %r: the equal flag disagrees with its hashes" % m.get("name"))
            print("OK: %d members, %d differing" % (len(mem), len(differing)))
        elif arm == "AC2":
            for m in mem:
                rp = m.get("repo_path")
                if not rp:
                    continue
                rc = subprocess.run(["git", "-C", str(ROOT), "show", "HEAD:%s" % rp], capture_output=True, timeout=60)
                if rc.returncode != 0:
                    fail("%s is not a blob at HEAD" % rp)
                import hashlib
                h = hashlib.sha256(rc.stdout).hexdigest()
                if h != m.get("head_member_sha256") and h != m.get("head_member_sha256_lf_normalised"):
                    fail("%s: head_member_sha256 is not the blob at HEAD" % rp)
            sys.path.insert(0, str(ROOT / ".tools"))
            import safe_deploy_core as sdc
            declared = set(sdc.find_bundle("investor_reporting")[2]["members"])
            named = {m.get("repo_path") for m in mem}
            absent = sorted(declared - named)
            if absent:
                fail("the guard's declared members missing from the census: %s" % absent[:3])
            for m in mem:
                if m.get("equal") is False and not (m.get("commits_since_live") or []):
                    fail("differing member %r carries no commits_since_live" % m.get("name"))
            print("OK: the head hashes are the blobs at HEAD and all %d declared members appear" % len(declared))
        elif arm == "AC3":
            h = r.get("host_reads_bundle") or {}
            if len(h.get("sites") or []) < 1:
                fail("host_reads_bundle.sites needs at least one cited site")
            for s in h["sites"]:
                cite_resolves(s.get("file"), s.get("line"), s.get("quote"), "host read site")
            for k in BOUND_ZERO:
                if r.get(k) != 0:
                    fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
            live = r.get("live_object") or {}
            if not live.get("etag") or live.get("etag") != r.get("etag_after"):
                fail("the live object's ETag after the census must equal the one before (etag_after)")
            raw = json.dumps(r)
            if re.search(r"(?<![0-9a-fA-F-])\d{9,}(?![0-9a-fA-F])", raw):
                fail("the record carries a long digit run")
            print("OK: the host's read is cited; the bound counters read 0; the ETag is unchanged")
        else:
            fail("unknown criterion")
    elif cell == "IB175-2":
        if arm == "AC1":
            rc, out = run([sys.executable, "-m", "pytest", TOL, "-q", "--no-header", "-p", "no:cacheprovider"], timeout=110)
            p, f, e = py_counts(out)
            if rc != 0 or p < 1 or f or e:
                fail("%s: %d passed, %d failed, %d errors" % (TOL, p, f, e))
            print("OK: the tolerance test passes alone (%d)" % p)
        elif arm == "AC2":
            files = [GOLD + "tests/test_holdings_49f.py", GOLD + "tests/test_holdings_inf.py", TOL]
            rc, out = run([sys.executable, "-m", "pytest"] + files + ["-q", "--no-header", "-p", "no:cacheprovider"], timeout=115)
            p, f, e = py_counts(out)
            if rc != 0 or p < 37 or f or e:
                fail("the three suites together: rc %s, %d passed, %d failed, %d errors (37 passed at least: 22 + 14 + the tolerance test)" % (rc, p, f, e))
            print("OK: the three suites pass together (%d)" % p)
        elif arm == "AC3":
            r = load(REPAIR)
            base = str(r.get("base_commit", ""))
            if not re.fullmatch(r"[0-9a-f]{8,40}", base):
                fail("base_commit must be a commit id")
            rc, out = run(["git", "diff", "--numstat", base, "HEAD", "--", GOLD])
            rows = [x.split("\t") for x in out.strip().splitlines() if x.strip()]
            names = sorted(x[2].replace("\\", "/") for x in rows if len(x) == 3)
            if names != [TOL]:
                fail("the repair must touch exactly %s under %s, touched %s" % (TOL, GOLD, names))
            n = sum(int(x[0]) + int(x[1]) for x in rows if x[0].isdigit() and x[1].isdigit())
            if n > 12:
                fail("the repair changed %d lines (12 at most)" % n)
            print("OK: one test file, %d changed lines" % n)
        else:
            fail("unknown criterion")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
