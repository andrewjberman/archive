"""IRPT_BCKEND round 53 (workstream ~P, issuer 2.0.0_SA_COO~P) -- the rest of S175 / S260 under CTO batch 253's class rule:
rows W124-S1 (25 bare MaintainedSourceRefused raises in two more _scope files) and W124-S2 (loaders.py opaque_firm_for raises
BucketUnmapped for a malformed server artifact, which is NOT_READY, not FIRM_BINDING).

Usage: python <this file> <repo_root> <criterion_id>
  IB53-1-AC1  the new test file (TESTS) passes with at least 3 tests naming W124-S1, W124-S2 and NOT_READY, AND the _authz and
              _scope suites pass with 0 failed. Base: FAIL (no test file).
  IB53-1-AC2  no `raise MaintainedSourceRefused(` remains in canonical_profile_reads.py or retained_input_authorizer.py, the
              census (CENSUS) lists every refusal-subclass raise in those two files with line, subclass and code (count
              equal to the raises), and loaders.py opaque_firm_for no longer raises BucketUnmapped. Base: FAIL.
  IB53-1-AC3  a GUARD: the worker's own commits since base touch only the grant and nothing under infra/aws/terraform/.
              Base: PASS.
Prints "<id> PASS" or "<id> FAIL" as the last line.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "80e1455217"
IR = "infra/aws/lambda/investor-reporting"
W = "org/missions/D9/IRPT/IRPT_BCKEND/deliverables/0.9.0_WK_IRPT_BCKEND~125/"
TESTS = IR + "/_authz/tests/test_reason_codes_W124.py"
CENSUS = W + "W124_RAISE_SITE_CENSUS.json"
FILES = (IR + "/_scope/canonical_profile_reads.py", IR + "/_scope/retained_input_authorizer.py")
LOADERS = IR + "/_authz/loaders.py"
AUTHOR = "0.9.0_WK_IRPT_BCKEND~125"
WORDS = ("W124-S1", "W124-S2", "NOT_READY")
GRANT = (IR + "/_authz/", IR + "/_scope/", W, "org/missions/D9/IRPT/IRPT_BCKEND/surprise-channel/investigations/INVESTIGATION_v1.md",
         "org/missions/D9/IRPT/IRPT_BCKEND/task-orders/IRPT_BCKEND.TO-IB-pr-322.")


def _pytest(root, target):
    r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", target], cwd=str(root / IR),
                       capture_output=True, text=True, timeout=900)
    out = re.sub(r"\x1b\[[0-9;]*m", "", (r.stdout or "") + (r.stderr or ""))
    last = ([ln for ln in out.splitlines() if ln.strip()] or ["(no output)"])[-1]
    return r.returncode, last


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cid = sys.argv[2] if len(sys.argv) > 2 else ""

    def fail(msg):
        print("FAIL: " + msg)
        print("%s FAIL" % (cid or "IB53-1"))
        sys.exit(1)

    if cid == "IB53-1-AC1":
        t = root / TESTS
        if not t.is_file():
            fail("no %s" % TESTS)
        src = t.read_bytes().decode("utf-8")
        missing = [w for w in WORDS if w not in src]
        if missing:
            fail("the tests never name %s" % missing)
        rc, last = _pytest(root, "_authz/tests/test_reason_codes_W124.py")
        m = re.search(r"(\d+) passed", last)
        if rc or not m or int(m.group(1)) < 3 or re.search(r"\d+ (failed|error)", last):
            fail("new tests: %s" % last)
        print("OK: new tests %s" % last)
        for target in ("_authz/tests/", "_scope/tests/"):
            rc, last = _pytest(root, target)
            print("%s -> rc %d :: %s" % (target, rc, last))
            if rc or re.search(r"\d+ (failed|error)", last):
                fail("%s: %s" % (target, last))
    elif cid == "IB53-1-AC2":
        raises = 0
        for f in FILES:
            src = (root / f).read_bytes().decode("utf-8")
            bare = [i + 1 for i, ln in enumerate(src.splitlines()) if re.search(r"raise MaintainedSourceRefused\(", ln)]
            if bare:
                fail("%s: bare raises remain at lines %s" % (f, bare[:12]))
            raises += sum(1 for ln in src.splitlines() if re.search(r"raise MaintainedSource(Unauthorized|Unready|InvalidInput)\(", ln))
        p = root / CENSUS
        if not p.is_file():
            fail("no %s" % CENSUS)
        sites = json.loads(p.read_bytes().decode("utf-8")).get("sites") or []
        for s in sites:
            if not all(s.get(k) for k in ("file", "line", "subclass", "public_reason_code")):
                fail("census site lacks file/line/subclass/public_reason_code: %r" % s)
        if len(sites) != raises:
            fail("census lists %d sites; the two files raise a subclass at %d lines" % (len(sites), raises))
        src = (root / LOADERS).read_bytes().decode("utf-8")
        m = re.search(r"def opaque_firm_for\(.*?(?=\ndef |\Z)", src, re.S)
        if not m or "raise BucketUnmapped" in m.group(0):
            fail("loaders.py opaque_firm_for still raises BucketUnmapped (or is missing)")
        print("OK: 0 bare raises in the two files; %d sites classified; opaque_firm_for no longer raises BucketUnmapped" % len(sites))
    elif cid == "IB53-1-AC3":
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
