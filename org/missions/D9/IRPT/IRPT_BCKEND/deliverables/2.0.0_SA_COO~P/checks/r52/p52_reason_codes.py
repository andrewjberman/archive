"""IRPT_BCKEND round 52 (workstream ~P, issuer 2.0.0_SA_COO~P) -- S260 + S175 reason codes (CTO batch 253 @35e313ec06):
BucketUnmapped -> FIRM_BINDING; MaintainedSourceRefused split into subclasses declaring public_reason_code.

Usage: python <this file> <repo_root> <criterion_id>
  IB52-1-AC1  the new test file (TESTS) passes with at least 4 tests naming S260, S175, FIRM_BINDING, NOT_READY and
              NOT_AUTHORIZED, AND the _authz and _scope suites pass with 0 failed. Base: FAIL (no test file).
  IB52-1-AC2  the raise-site census: in _scope/maintained_sources.py no `raise MaintainedSourceRefused(` remains (every site
              raises a subclass), and CENSUS lists every raise site with line, subclass and public_reason_code, its count
              equal to the subclass raises in the file, plus `unexpected_before` / `unexpected_after`. Base: FAIL.
  IB52-1-AC3  a GUARD: the worker's own commits since base touch only the grant and nothing under infra/aws/terraform/.
              Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "033795b666"
IR = "infra/aws/lambda/investor-reporting"
W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~124/"
TESTS = IR + "/_authz/tests/test_reason_codes_S260_S175.py"
CENSUS = W + "S175_RAISE_SITE_CENSUS.json"
MS = IR + "/_scope/maintained_sources.py"
AUTHOR = "0.9.0_WK_IRPT_BCKEND~124"
WORDS = ("S260", "S175", "FIRM_BINDING", "NOT_READY", "NOT_AUTHORIZED")
GRANT = (IR + "/_authz/", IR + "/_scope/", W, "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md",
         "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-321.")


def _pytest(root, cwd, target):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target], cwd=str(root / cwd),
                       capture_output=True, text=True, timeout=900)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
    last = ([ln for ln in out.splitlines() if ln.strip()] or ["(no output)"])[-1]
    return r.returncode, last


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB52-1"))
        sys.exit(1)

    if cid == "IB52-1-AC1":
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        missing = [w for w in WORDS if w not in src]
        if missing:
            fail("the tests never name %s" % missing)
        rc, last = _pytest(root, IR, "_authz/tests/test_reason_codes_S260_S175.py")
        m = re.search(r"(\d+) passed", last)
        if rc or not m or int(m.group(1)) < 4 or re.search(r"\d+ (failed|error)", last):
            fail("new tests: %s" % last)
        print("OK: new tests %s" % last)
        for target in ("_authz/tests/", "_scope/tests/"):
            rc, last = _pytest(root, IR, target)
            print("%s -> rc %d :: %s" % (target, rc, last))
            if rc or re.search(r"\d+ (failed|error)", last):
                fail("%s: %s" % (target, last))
    elif cid == "IB52-1-AC2":
        src = (root / MS).read_bytes().decode("utf-8")
        bare = [i + 1 for i, ln in enumerate(src.splitlines()) if re.search(r"raise MaintainedSourceRefused\(", ln)]
        if bare:
            fail("bare MaintainedSourceRefused raises remain at lines %s" % bare[:12])
        raises = [i + 1 for i, ln in enumerate(src.splitlines()) if re.search(r"raise \w*(Refused|Unready|Unauthorized|Invalid)\w*\(", ln)]
        p = root / CENSUS
        if not p.is_file():
            fail("no %s" % CENSUS)
        c = json.loads(p.read_bytes().decode("utf-8"))
        sites = c.get("sites") or []
        for k in ("unexpected_before", "unexpected_after"):
            if k not in c:
                fail("census lacks %r" % k)
        for s in sites:
            if not all(s.get(f) for f in ("line", "subclass", "public_reason_code")):
                fail("census site lacks line/subclass/public_reason_code: %r" % s)
        if len(sites) != len(raises):
            fail("census lists %d sites; the file raises a refusal subclass at %d lines" % (len(sites), len(raises)))
        print("OK: 0 bare raises; %d sites classified; UNEXPECTED %s -> %s"
              % (len(sites), c["unexpected_before"], c["unexpected_after"]))
    elif cid == "IB52-1-AC3":
        r = subprocess.run(["git", "log", "%s..HEAD" % BASE, "--author=%s" % AUTHOR, "--name-only", "--format="],
                           cwd=str(root), capture_output=True)
        changed = sorted(set(ln for ln in r.stdout.decode("utf-8").splitlines() if ln.strip()))
        bad = [c for c in changed if c.startswith("infra/aws/terraform/") or not c.startswith(GRANT)]
        if bad:
            fail("out-of-grant changes: %s" % bad[:8])
        print("OK: %d changed path(s), all inside the grant" % len(changed))
    else:
        fail("unknown criterion %r" % cid)
    print("%s PASS" % cid)


if __name__ == "__main__":
    main()
