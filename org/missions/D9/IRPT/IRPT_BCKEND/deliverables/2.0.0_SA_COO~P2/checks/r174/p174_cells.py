"""IRPT_BCKEND round 174 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB174-1  IB-pr-505  the builder validates its own snapshot against the repository's v1 schema BEFORE it writes, and a planted member refuses the build (row W354-S2)
    AC1  the worker's new test file passes (3 or more, none failed)
    AC2  the issuer's probe: the valid fixture validates, the same fixture with account_id removed validates, the same fixture with a planted member on the ACCOUNT node is refused
    AC3  the read record: the build path's validation call sites resolve (file, line, quote), and the build refuses on an invalid snapshot
  IB174-2  IB-pr-506  the portal wire union and type follow the contract's enum, multi_asset included (row D2-S127)
    AC1  the IVE48-AC1 test passes
    AC2  the whole InvestorReporting folder fails no more than its four pre-existing tests and passes at least 1214
    AC3  the worker's new test passes (2 or more, none failed) and names multi_asset
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
GOLD = "data/assets/scripts/gold/investor_reporting/"
FIXTURE = "infra/aws/lambda/investor-reporting/_contracts/fixtures/HoldingsSnapshot.valid.json"
READ_REC = D + "0.9.0_WK_IRPT_BCKEND~356/IB174-1_build_validation_read.json"
PIR = "src/pages/InvestorReporting/"
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB174"))
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


def bun_counts(out):
    out = re.sub(r"\x1b\[[0-9;]*m", "", out)
    p = re.findall(r"^\s*(\d+) pass\s*$", out, re.M)
    f = re.findall(r"^\s*(\d+) fail\s*$", out, re.M)
    return (int(p[-1]) if p else None), (int(f[-1]) if f else 0)


def py_counts(out):
    out = re.sub(r"\x1b\[[0-9;]*m", "", out)
    m = {k: int(v) for v, k in re.findall(r"(\d+) (passed|failed|error|errors)", out)}
    return m.get("passed", 0), m.get("failed", 0), m.get("error", 0) + m.get("errors", 0)


PROBE = r"""
import sys, json, copy
sys.path.insert(0, %r)
import holdings_snapshot as hs
d = json.load(open(%r, encoding="utf-8"))["instance"]
res = {}
res["valid"] = hs.validate_snapshot(d)[0]
b = copy.deepcopy(d)
for n in b["nodes"]:
    if n.get("node_kind") == "ACCOUNT":
        n.pop("account_id", None)
res["without_account_id"] = hs.validate_snapshot(b)[0]
c = copy.deepcopy(d)
for n in c["nodes"]:
    if n.get("node_kind") == "ACCOUNT":
        n["planted_member"] = "x"
        break
ok, errs = hs.validate_snapshot(c)
res["planted"] = ok
res["planted_names_member"] = any("planted_member" in e for e in errs)
print(json.dumps(res))
"""


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB174-1":
        if arm == "AC1":
            tf = GOLD + "tests/test_build_refuses_planted_member.py"
            if not (ROOT / tf).is_file():
                fail("no %s" % tf)
            rc, out = run([sys.executable, "-m", "pytest", tf, "-q", "--no-header", "-p", "no:cacheprovider"], timeout=110)
            p, f, e = py_counts(out)
            if rc != 0 or p < 3 or f or e:
                fail("%s: %d passed, %d failed, %d errors (3 passed and none failed are required)" % (tf, p, f, e))
            print("OK: %d tests pass" % p)
        elif arm == "AC2":
            rc, out = run([sys.executable, "-I", "-c", PROBE % (str(ROOT / GOLD), str(ROOT / FIXTURE))], timeout=100)
            if rc != 0:
                fail("the probe did not run: %s" % re.sub(r"\s+", " ", out)[-200:])
            try:
                r = json.loads(out[out.rindex("{"):])
            except ValueError:
                fail("the probe printed no result: %s" % out[-200:])
            if r.get("valid") is not True or r.get("without_account_id") is not True:
                fail("the valid fixture, with and without account_id, must validate: %s" % r)
            if r.get("planted") is not False or r.get("planted_names_member") is not True:
                fail("a planted ACCOUNT-node member must be refused with an error naming it: %s" % r)
            print("OK: the valid fixture validates with and without account_id; a planted member is refused")
        elif arm == "AC3":
            r = load(READ_REC)
            sites = r.get("call_sites") or []
            if len(sites) < 2:
                fail("at least two validation call sites (the build and the land hook) are required")
            for s in sites:
                cite_resolves(s.get("file"), s.get("line"), s.get("quote"), "call site")
            if r.get("refuses_on_invalid") is not True:
                fail("refuses_on_invalid must be true, with the refusing line cited in `refusal`")
            ref = r.get("refusal") or {}
            cite_resolves(ref.get("file"), ref.get("line"), ref.get("quote"), "refusal")
            print("OK: %d call site(s) and the refusal resolve" % len(sites))
        else:
            fail("unknown criterion")
    elif cell == "IB174-2":
        T = PIR + "__tests__/"
        if arm == "AC1":
            rc, out = run(["bun", "test", T + "dsgn-irptv1/iv-e-48.new-classes.test.tsx"], timeout=110, cwd=ROOT / "portal")
            p, f = bun_counts(out)
            if rc != 0 or not p or f:
                fail("IVE48-AC1: rc %s, %s pass, %s fail" % (rc, p, f))
            print("OK: IVE48-AC1 passes")
        elif arm == "AC2":
            rc, out = run(["bun", "test", PIR.rstrip("/")], timeout=115, cwd=ROOT / "portal")
            p, f = bun_counts(out)
            if p is None or p < 1214 or f > 4:
                fail("the whole folder: %s pass, %s fail (at least 1214 pass and at most 4 fail are required)" % (p, f))
            print("OK: the folder reads %d pass, %d fail" % (p, f))
        elif arm == "AC3":
            tf = T + "dsgn-irptv1/ib-174-multi-asset-label.test.ts"
            if not (ROOT / "portal" / tf).is_file():
                fail("no portal/%s" % tf)
            if "multi_asset" not in (ROOT / "portal" / tf).read_text(encoding="utf-8"):
                fail("the new test must name multi_asset")
            rc, out = run(["bun", "test", tf], timeout=110, cwd=ROOT / "portal")
            p, f = bun_counts(out)
            if rc != 0 or not p or p < 2 or f:
                fail("the new test: rc %s, %s pass, %s fail (2 pass and none failed are required)" % (rc, p, f))
            print("OK: the new multi_asset test passes (%d)" % p)
        else:
            fail("unknown criterion")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
