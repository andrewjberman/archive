#!/usr/bin/env python
"""YCD-v-6 checks: python v6_checks.py <typecheck|tests>   (run from the worktree root).

One argument, one RESULT line. ASCII only. No vendor call, no AWS call, no install, no write under portal/.

  typecheck  `bun --no-install run typecheck` (tsc -b --noEmit) inside portal/; PASS only at rc 0 with no error line.
  tests      the portal InvestorReporting test set is run at portal d1b21c97 and at the worktree's portal, each in its OWN
             temporary tree (the suite's generator tests WRITE into contracts/wire/, so neither run may touch the real
             portal). Both trees get the same workspace data (docs/contracts and the lambda _contracts, from the
             worktree) and the same linked node_modules. PASS only when no test green at d1b21c97 is red at HEAD.
"""
import concurrent.futures
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from io import BytesIO
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=str(HERE)).decode().strip())
PORTAL = ROOT / "portal"
PIN = "d1b21c97"
LAMBDA = "infra/aws/lambda/investor-reporting"
SUITE = "src/pages/InvestorReporting"


def find_bun():
    found = shutil.which("bun")
    if found:
        return found
    import glob
    base = os.environ.get("LOCALAPPDATA", "")
    hits = glob.glob(os.path.join(base, "Microsoft", "WinGet", "Packages", "Oven-sh.Bun*", "bun-windows-x64", "bun.exe"))
    if hits:
        return hits[0]
    raise SystemExit("bun not found")


def arm_typecheck():
    p = subprocess.run([find_bun(), "--no-install", "run", "typecheck"], cwd=str(PORTAL), capture_output=True, timeout=115)
    out = (p.stdout + p.stderr).decode("utf-8", "replace")
    errs = [ln for ln in out.splitlines() if "error TS" in ln]
    by_file = Counter(ln.split("(")[0] for ln in errs)
    print("portal HEAD %s ; bun --no-install run typecheck: rc=%d ; %d error line(s)"
          % (subprocess.check_output(["git", "-C", str(PORTAL), "rev-parse", "--short=8", "HEAD"]).decode().strip(), p.returncode, len(errs)))
    for name, n in sorted(by_file.items()):
        print("  %d error(s) in %s" % (n, name))
    for ln in errs[:5]:
        print("  " + ln)
    ok = p.returncode == 0 and not errs
    print("RESULT: typecheck %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


def link_node_modules(dest):
    target = os.path.realpath(str(PORTAL / "node_modules"))
    subprocess.run(["cmd", "/c", "mklink", "/J", str(dest), target], check=True, capture_output=True)


def build_tree(tmp, which):
    """tmp/<which>/portal = the portal sources; tmp/<which>/{docs,infra} = workspace data the suite reads."""
    top = Path(tmp) / which
    pdir = top / "portal"
    pdir.mkdir(parents=True)
    if which == "base":
        data = subprocess.check_output(["git", "-C", str(PORTAL), "archive", "--format=tar", PIN])
        with tarfile.open(fileobj=BytesIO(data)) as tf:
            members = [m for m in tf.getmembers() if not (m.issym() or m.islnk())]  # symlinks point outside the tree
            tf.extractall(str(pdir), members=members, filter="data")
    else:
        names = subprocess.check_output(["git", "-C", str(PORTAL), "ls-files", "-z"]).decode("utf-8").split("\0")
        for n in names:
            if n and (PORTAL / n).is_file():
                dst = pdir / n
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(str(PORTAL / n), str(dst))
    shutil.copytree(str(ROOT / "docs/contracts"), str(top / "docs/contracts"))
    shutil.copytree(str(ROOT / LAMBDA / "_contracts"), str(top / LAMBDA / "_contracts"),
                    ignore=shutil.ignore_patterns("__pycache__", "tests"))
    link_node_modules(pdir / "node_modules")
    return pdir


def run_suite(pdir):
    xml = pdir.parent / "junit.xml"
    p = subprocess.run([find_bun(), "--no-install", "test", SUITE, "--reporter=junit", "--reporter-outfile=" + str(xml)],
                       cwd=str(pdir), capture_output=True, timeout=300)
    return p.returncode, xml


def read_junit(xml):
    """{key: 'pass'|'fail'|'skip'} with key = (file, suite chain, test name, occurrence)."""
    results, seen = {}, Counter()

    def walk(node, chain):
        for child in node:
            if child.tag == "testsuite":
                walk(child, chain + [child.get("name", "")])
            elif child.tag == "testcase":
                state = "pass"
                for sub in child:
                    if sub.tag in ("failure", "error"):
                        state = "fail"
                    elif sub.tag == "skipped" and state == "pass":
                        state = "skip"
                base = (child.get("file", ""), tuple(chain), child.get("name", ""))
                seen[base] += 1
                results[base + (seen[base],)] = state
    walk(ET.parse(str(xml)).getroot(), [])
    return results


def arm_tests():
    tmp = tempfile.mkdtemp(prefix="v6tests_")
    try:
        head = subprocess.check_output(["git", "-C", str(PORTAL), "rev-parse", "--short=8", "HEAD"]).decode().strip()
        base_dir, head_dir = build_tree(tmp, "base"), build_tree(tmp, "head")
        print("trees built under %s (base = portal %s archive, head = portal working tree at %s); suite = %s"
              % (tmp, PIN, head, SUITE))
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
            fb, fh = ex.submit(run_suite, base_dir), ex.submit(run_suite, head_dir)
            (rcb, xb), (rch, xh) = fb.result(), fh.result()
        b, h = read_junit(xb), read_junit(xh)

        def count(r):
            c = Counter(r.values())
            return "%d tests: %d pass, %d fail, %d skip" % (len(r), c["pass"], c["fail"], c["skip"])
        print("base %s: bun rc=%d ; %s" % (PIN, rcb, count(b)))
        print("head %s: bun rc=%d ; %s" % (head, rch, count(h)))
        green_base = [k for k, v in b.items() if v == "pass"]
        regress = [k for k in green_base if h.get(k) != "pass"]
        newly_green = [k for k, v in h.items() if v == "pass" and b.get(k) != "pass"]
        print("green at %s: %d ; of those not green at head: %d ; green at head and not at base: %d"
              % (PIN, len(green_base), len(regress), len(newly_green)))
        for k in regress[:15]:
            print("  REGRESSED %s :: %s :: %s -> %s" % (k[0], " > ".join(k[1]), k[2], h.get(k, "absent")))
        ok = bool(green_base) and bool(h) and not regress
        print("RESULT: tests %s" % ("PASS" if ok else "FAIL"))
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    arms = {"typecheck": arm_typecheck, "tests": arm_tests}
    if len(sys.argv) != 2 or sys.argv[1] not in arms:
        print("usage: v6_checks.py <typecheck|tests>")
        sys.exit(2)
    sys.exit(arms[sys.argv[1]]())
