"""IRPT_BCKEND round 172 (workstream ~P, issuer 2.0.0_SA_COO~P2) -- checks of two orders.

Usage: python <this file> <repo_root> <criterion_id>; prints "<id> PASS" or "<id> FAIL" last.

  IB172-1  IB-pr-501  READ: which packaged HoldingsSnapshot schema copies are validated at serve (CTO round-172 analysis section 4 item 1)
    AC1  the record names exactly the functions the source map packages the copy in, with the denominators
    AC2  every reader cited resolves (file, line, quote) and carries a use from the closed set
    AC3  validated_at_serve agrees with the readers; the minimal re-pin members are named only for a validated copy; the bound counters 0
  IB172-2  IB-pr-502  the fe-s-18 generator reproduces the committed bytes the portal's tests consume (rows W350-S1, W346-S3)
    AC1  running the fe-s-18 generator leaves the smoke, fe-s-16 and fe-s-32 fixture folders byte-equal to the committed files (end-of-line differences ignored)
    AC2  the six portal tests that consume the fe-s-18 maps pass (28 or more, none failed)
    AC3  the decision record names each generator output, its consuming test (file, line, quote), and the outputs are unchanged since the portal base
"""
import json
import re
import subprocess
import sys
from pathlib import Path

PROJ = "org/missions/D9/IRPT/IRPT_BCKEND/"
D = PROJ + "deliverables/"
SRCMAP = "infra/aws/lambda/ci/lambda-source-map.json"
COPY = "contracts/HoldingsSnapshot.schema.json"
PIR = "src/pages/InvestorReporting/"
READ_REC = D + "0.9.0_WK_IRPT_BCKEND~352/IB172-1_serve_validation_read.json"
DEC_REC = D + "0.9.0_WK_IRPT_BCKEND~353/IB172-2_fe_s_18_truth_decision.json"
USES = {"VALIDATES_AT_SERVE", "PRESENCE_ONLY", "TEST_ONLY", "NOT_READ"}
BOUND_ZERO = ("functions_invoked", "sign_ins_made", "aws_writes_made", "accounts_written", "figures_written", "vendor_requests_sent")
ROOT = Path(".")
CID = ""


def fail(msg):
    print("FAIL: " + msg)
    print("%s FAIL" % (CID or "IB172"))
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
    """The cited file exists and the quote sits within 3 lines of the cited line."""
    f = ROOT / str(rel)
    if not f.is_file():
        fail("%s: file %r does not exist" % (what, rel))
    if not is_int(line) or line < 1 or not str(quote).strip():
        fail("%s: needs an integer line and a non-empty quote" % what)
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    window = "\n".join(lines[max(0, line - 4):line + 3])
    q = re.sub(r"\s+", " ", str(quote).strip())
    if q not in re.sub(r"\s+", " ", window):
        fail("%s: the quote is not within 3 lines of %s:%s" % (what, rel, line))


def source_map_packagers():
    fns = load(SRCMAP).get("functions") or {}
    return sorted(n for n, v in fns.items() if COPY in json.dumps(v)), len(fns)


def main():
    global ROOT, CID
    ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    CID = sys.argv[2] if len(sys.argv) > 2 else ""
    cell, arm = CID[:7], CID[8:]
    if cell == "IB172-1":
        r = load(READ_REC)
        pk = r.get("packagers") or []
        if arm == "AC1":
            want, total = source_map_packagers()
            got = sorted(p.get("function") for p in pk)
            if got != want:
                fail("packagers must be exactly %s (the source map's), read %s" % (want, got))
            den = r.get("denominator") or {}
            if den.get("functions_in_source_map") != total or den.get("functions_packaging_the_copy") != len(want):
                fail("denominator must read functions_in_source_map %d and functions_packaging_the_copy %d, reads %s" % (total, len(want), den))
            print("OK: %d packager(s) of %d functions, as the source map has them" % (len(want), total))
        elif arm == "AC2":
            n = 0
            for p in pk:
                rd = p.get("readers") or []
                if not rd and not (p.get("searched_paths") or []):
                    fail("%s: no reader cited and no searched_paths named" % p.get("function"))
                for x in rd:
                    if x.get("use") not in USES:
                        fail("%s: use %r is not one of %s" % (p.get("function"), x.get("use"), sorted(USES)))
                    cite_resolves(x.get("file"), x.get("line"), x.get("quote"), "%s reader" % p.get("function"))
                    n += 1
            if not pk:
                fail("no packagers in the record")
            print("OK: %d reader citation(s) resolve" % n)
        elif arm == "AC3":
            for p in pk:
                v = any(x.get("use") == "VALIDATES_AT_SERVE" for x in (p.get("readers") or []))
                if p.get("validated_at_serve") is not v:
                    fail("%s: validated_at_serve %r disagrees with its readers (%r)" % (p.get("function"), p.get("validated_at_serve"), v))
                mem = p.get("minimal_repin_members")
                if not isinstance(mem, list):
                    fail("%s: minimal_repin_members must be a list" % p.get("function"))
                if v and not mem:
                    fail("%s: validated at serve, so its minimal re-pin members must be named" % p.get("function"))
                if not v and mem:
                    fail("%s: not validated at serve, so minimal_repin_members must be empty" % p.get("function"))
                for m in mem:
                    if not (ROOT / str(m)).is_file():
                        fail("%s: re-pin member %r is not a repo file" % (p.get("function"), m))
            for k in BOUND_ZERO:
                if r.get(k) != 0:
                    fail("the bound counter %s must read 0, reads %r" % (k, r.get(k)))
            print("OK: validated_at_serve agrees with the readers; re-pin members named only where validated")
        else:
            fail("unknown criterion")
    elif cell == "IB172-2":
        gen = PIR + "__tests__/fe-s-18/gen-fixtures.ts"
        folders = [PIR + "fixtures/smoke", PIR + "__tests__/fe-s-16", PIR + "__tests__/fe-s-32"]
        if arm == "AC1":
            rc, out = run(["bun", "run", gen], timeout=100, cwd=ROOT / "portal")
            if rc != 0:
                fail("the fe-s-18 generator did not run: %s" % re.sub(r"\s+", " ", out)[-160:])
            pd = subprocess.run(["git", "-C", str(ROOT / "portal"), "diff", "--ignore-cr-at-eol", "--stat", "--"] + folders, capture_output=True, timeout=60)
            diff = pd.stdout.decode("utf-8", "replace")
            if pd.returncode != 0 or diff.strip():
                fail("the fe-s-18 generator drifts from the committed bytes: %s" % re.sub(r"\s+", " ", diff)[:200])
            print("OK: the fe-s-18 generator runs and reproduces the committed fixtures")
        elif arm == "AC2":
            T = PIR + "__tests__/"
            files = [T + "fe-s-18/paired.test.ts", T + "fe-s-18/manifest.test.ts", T + "fe-s-32/holdings-in-a-browser.test.ts",
                     T + "fe-s-19/mounted-from-wire.test.ts", T + "fe-s-31/every-page.test.ts", T + "fe-s-33/fixtures-reach.test.ts"]
            rc, out = run(["bun", "test"] + files, timeout=110, cwd=ROOT / "portal")
            out = re.sub(r"\x1b\[[0-9;]*m", "", out)
            m = re.search(r"(\d+) pass", out)
            f = re.search(r"(\d+) fail", out)
            if rc != 0 or not m or int(m.group(1)) < 28 or (f and int(f.group(1)) != 0):
                fail("the six portal tests: rc %s, %s pass, %s fail" % (rc, m.group(1) if m else "?", f.group(1) if f else "?"))
            print("OK: the six consuming portal tests pass")
        elif arm == "AC3":
            r = load(DEC_REC)
            outs = r.get("outputs") or []
            names = sorted(o.get("file") for o in outs)
            need = sorted([PIR + "fixtures/smoke/fe-s-18-frozen.json", PIR + "fixtures/smoke/fe-s-18-holdings-observed.json",
                           PIR + "fixtures/smoke/fe-s-18-holdings-target.json", PIR + "fixtures/smoke/fe-s-18-holdings-missing-attribution.json",
                           PIR + "__tests__/fe-s-32/holdings-no-answer.json", PIR + "fixtures/smoke/fe-s-16-print-prehistory.json"])
            if names != need:
                fail("the record must name exactly the six generator outputs %s, names %s" % (need, names))
            for o in outs:
                c = o.get("consumed_by") or []
                if not c:
                    fail("%s: no consuming test cited" % o.get("file"))
                for x in c:
                    cite_resolves("portal/" + str(x.get("test")), x.get("line"), x.get("quote"), "%s consumer" % o.get("file"))
            base = r.get("portal_base")
            if not re.fullmatch(r"[0-9a-f]{8,40}", str(base)):
                fail("portal_base must be a commit id")
            pd = subprocess.run(["git", "-C", str(ROOT / "portal"), "diff", "--ignore-cr-at-eol", "--stat", str(base), "HEAD", "--"] + [o["file"] for o in outs],
                                capture_output=True, timeout=60)
            if pd.returncode != 0 or pd.stdout.decode("utf-8", "replace").strip():
                fail("a generator output differs from the portal base: %s" % pd.stdout.decode("utf-8", "replace")[:160])
            print("OK: six outputs, each with a resolving consumer, unchanged since the base")
        else:
            fail("unknown criterion")
    else:
        fail("unknown criterion %r" % CID)
    print("%s PASS" % CID)


if __name__ == "__main__":
    main()
