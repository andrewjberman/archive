#!/usr/bin/env python
"""YCD-u-6 checks: python u6_checks.py <schema|regen|census>   (run from the worktree root).

One argument, one RESULT line. ASCII only. No vendor call, no AWS call, no install, no write under portal/.

  schema  the v1 AnalysisReport schema is byte-frozen (sha256 equal to its merge-base copy), and every
          AnalysisReport v2 fixture under _contracts/fixtures/ validates against the v2 schema exactly as
          its file name says (valid / invalid).
  regen   the portal's changed generator (gen-wire.ts, imported from the portal tree and driven by bun from
          inside portal/ with --no-install) renders AnalysisReport to a temporary directory; its body is
          compared with the committed contracts/wire/AnalysisReport.ts with the leading header comment
          block excluded from both.
  census  every reader of either AnalysisReport schema file (printed-denominator searches) is named, and
          the python tests among them are run on a CLOUD export and on HEAD; PASS when none is newly red.
"""
import concurrent.futures
import difflib
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=str(HERE)).decode().strip())
LAMBDA = "infra/aws/lambda/investor-reporting"
V1_REL = "docs/contracts/investor-reporting/v1/AnalysisReport.schema.json"
V2_REL = LAMBDA + "/_contracts/AnalysisReport.v2.schema.json"
FIXTURES = ROOT / LAMBDA / "_contracts/fixtures"
PORTAL = ROOT / "portal"
TS_REL = "src/pages/InvestorReporting/contracts/wire/AnalysisReport.ts"
GEN_REL = "src/pages/InvestorReporting/__tests__/fe-s-13/gen-wire.ts"


def git(*args, cwd=None):
    return subprocess.check_output(["git"] + list(args), cwd=str(cwd or ROOT))


def sha(b):
    return hashlib.sha256(b.replace(b"\r\n", b"\n")).hexdigest()


def find_bun():
    found = shutil.which("bun")
    if found:
        return found
    base = os.environ.get("LOCALAPPDATA", "")
    hits = glob.glob(os.path.join(base, "Microsoft", "WinGet", "Packages", "Oven-sh.Bun*", "bun-windows-x64", "bun.exe"))
    if hits:
        return hits[0]
    raise SystemExit("bun not found")


# ---------------------------------------------------------------------------------------------- schema arm
def arm_schema():
    import jsonschema
    mb = git("merge-base", "HEAD", "CLOUD").decode().strip()
    base = git("show", mb + ":" + V1_REL)
    now = (ROOT / V1_REL).read_bytes()
    frozen = sha(base) == sha(now)
    print("merge-base HEAD CLOUD = %s" % mb)
    print("v1 sha256 at merge-base %s ; in working tree %s ; frozen: %s" % (sha(base), sha(now), frozen))
    validator = jsonschema.Draft202012Validator(json.loads((ROOT / V2_REL).read_text(encoding="utf-8")))
    names = sorted(p.name for p in FIXTURES.glob("AnalysisReport.v2.*.json"))
    bad = []
    for name in names:
        stem = name[:-len(".json")].rsplit(".", 1)[-1]
        want = not stem.startswith("invalid")
        doc = json.loads((FIXTURES / name).read_text(encoding="utf-8"))["instance"]
        got = validator.is_valid(doc)
        print("  FIXTURE %s name says %s, validates as %s" % (name, "valid" if want else "invalid", "valid" if got else "invalid"))
        if got != want:
            bad.append(name)
    print("COUNT: %d AnalysisReport v2 fixtures under %s/_contracts/fixtures (glob AnalysisReport.v2.*.json); %d disagree with their name %s"
          % (len(names), LAMBDA, len(bad), bad))
    ok = frozen and len(names) > 0 and not bad
    print("RESULT: schema %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


# ---------------------------------------------------------------------------------------------- regen arm
def strip_header(text):
    """Drop the leading /** ... */ comment block (and blank lines after it)."""
    text = text.replace("\r\n", "\n")
    m = re.match(r"\s*/\*\*.*?\*/\n*", text, re.S)
    return text[m.end():] if m else text


def arm_regen():
    tmp = tempfile.mkdtemp(prefix="u6regen_")
    assert not str(Path(tmp).resolve()).startswith(str(PORTAL.resolve())), "temp dir inside portal"
    out = Path(tmp) / "AnalysisReport.ts"
    driver = Path(tmp) / "drive.ts"
    gen = (PORTAL / GEN_REL).resolve().as_posix()
    driver.write_text(
        "import { readFileSync, writeFileSync } from 'node:fs'\n"
        "import { renderModule, schemaFilePath, schemaRepoPath } from '%s'\n"
        "const text = readFileSync(schemaFilePath('AnalysisReport'), 'utf8')\n"
        "writeFileSync('%s', renderModule('AnalysisReport', text), 'utf8')\n"
        "console.log('SOURCE: ' + schemaRepoPath('AnalysisReport'))\n" % (gen, out.as_posix()), encoding="ascii")
    p = subprocess.run([find_bun(), "--no-install", str(driver)], cwd=str(PORTAL), capture_output=True, timeout=100)
    print("generator run (bun --no-install from portal/, out-dir %s): rc=%d %s"
          % (tmp, p.returncode, (p.stdout + p.stderr).decode("utf-8", "replace").strip()))
    if p.returncode or not out.exists():
        print("RESULT: regen FAIL")
        return 1
    gen_text = out.read_text(encoding="utf-8")
    committed = (PORTAL / TS_REL).read_text(encoding="utf-8")
    a = strip_header(gen_text).split("\n")
    b = strip_header(committed).split("\n")
    print("bodies (header excluded): generated %d lines, committed %d lines" % (len(a), len(b)))
    ident = a == b
    if not ident:
        for i in range(max(len(a), len(b))):
            la, lb = (a[i] if i < len(a) else "<EOF>"), (b[i] if i < len(b) else "<EOF>")
            if la != lb:
                print("FIRST DIFFERING BODY LINE %d:" % (i + 1))
                print("  generated: %s" % la)
                print("  committed: %s" % lb)
                break
        d = list(difflib.unified_diff(a, b, lineterm="", n=0))
        print("DIFF: %d lines only in generated, %d only in committed"
              % (sum(1 for x in d if x.startswith("-") and not x.startswith("---")),
                 sum(1 for x in d if x.startswith("+") and not x.startswith("+++"))))
    shutil.rmtree(tmp, ignore_errors=True)
    print("RESULT: regen %s" % ("PASS" if ident else "FAIL"))
    return 0 if ident else 1


# ---------------------------------------------------------------------------------------------- census arm
def lines(b):
    return [x for x in b.decode("utf-8", "replace").split("\n") if x]


ARCHIVE_PATHS = ["docs", "infra/aws/lambda", "lib", "deck_generation", "data/firm_registry.json"]


def export_tree(rev, dest):
    """git archive <rev> of the paths the reader tests need into dest (symlinks skipped); returns the file count."""
    import io
    import tarfile
    paths = [p for p in ARCHIVE_PATHS if git("ls-tree", "--name-only", rev, "--", p).strip()]
    data = git("archive", "--format=tar", rev, "--", *paths)
    with tarfile.open(fileobj=io.BytesIO(data)) as tf:
        members = [m for m in tf.getmembers() if not (m.issym() or m.islnk())]
        tf.extractall(str(dest), members=members, filter="data")
    return len(members), paths


def run_pytest(job):
    root, path = job
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--color=no", "-rfE", path],
                       cwd=str(root), capture_output=True, timeout=110)
    text = p.stdout.decode("utf-8", "replace")
    failed = set()
    for line in text.splitlines():
        if line.startswith("FAILED ") or line.startswith("ERROR "):
            failed.add(line.split(" ", 1)[1].split(" - ")[0].strip())
    last = [ln for ln in text.splitlines() if re.match(r"^\d+ (passed|failed|error|errors|skipped).* in [0-9.]+s", ln.strip())]
    return path, p.returncode, failed, (last[-1].strip() if last else text.strip()[-120:])


def arm_census():
    tracked = lines(git("ls-files"))
    p_tracked = lines(git("-C", str(PORTAL), "ls-files"))
    a = lines(git("grep", "-l", "-I", "-E", r"AnalysisReport(\.v2)?\.schema"))
    c = lines(git("grep", "-l", "-I", "-E", r"glob\(.*schema\.json", "--", LAMBDA + "/*.py"))
    b = lines(git("-C", str(PORTAL), "grep", "-l", "-I", "-E",
                  r"AnalysisReport(\.v2)?\.schema|SERVED_V2_SCHEMAS|schemaFilePath", "--", "src"))
    a_live = [x for x in a if not x.startswith("org/")]
    a_org = [x for x in a if x.startswith("org/")]
    print("SEARCH A: git grep -l -I -E 'AnalysisReport(\\.v2)?\\.schema' over %d tracked outer files: %d hits (%d under org/ = records, "
          "not readers; %d outside org/)" % (len(tracked), len(a), len(a_org), len(a_live)))
    print("SEARCH B: git -C portal grep -l -I -E 'AnalysisReport(\\.v2)?\\.schema|SERVED_V2_SCHEMAS|schemaFilePath' -- src over %d tracked "
          "portal files: %d hits" % (len(p_tracked), len(b)))
    print("SEARCH C: git grep -l -I -E 'glob\\(.*schema\\.json' -- %s/*.py (loaders that read EVERY schema file, so both): %d hits"
          % (LAMBDA, len(c)))
    readers = sorted(set(a_live) | set(c))
    print("READERS (outer, outside org/): %d" % len(readers))
    tests = []
    for r in readers:
        base = r.rsplit("/", 1)[-1]
        is_py_test = r.endswith(".py") and (base.startswith("test_") or "/tests/" in r)
        kind = "python test" if is_py_test else ("schema file" if r.endswith(".schema.json") else
                                                 ("python code" if r.endswith(".py") else "document/manifest"))
        print("  READER [%s] %s" % (kind, r))
        if is_py_test and base.startswith("test_"):
            tests.append(r)
        elif is_py_test:
            print("    (not a pytest file by name: not run)")
    print("READERS (portal, TypeScript, not python tests: named, not run here): %d" % len(b))
    for r in sorted(b):
        print("  READER [portal ts] portal/%s" % r)
    print("PYTHON TESTS TO RUN: %d" % len(tests))
    tmp = tempfile.mkdtemp(prefix="u6census_")
    failed_new = []
    try:
        trees = {}
        for label, rev in (("CLOUD", "CLOUD"), ("HEAD", "HEAD")):
            dest = Path(tmp) / label
            dest.mkdir()
            n, paths = export_tree(rev, dest)
            trees[label] = dest
            print("TREE %s = git archive %s (%s) of %s : %d files" % (label, rev, git("rev-parse", "--short=10", rev).decode().strip(), paths, n))
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
            for label in ("CLOUD", "HEAD"):
                jobs = [(trees[label], t) for t in tests]
                results[label] = {path: (rc, failed, summary) for path, rc, failed, summary in ex.map(run_pytest, jobs)}
        for t in tests:
            c_rc, c_failed, c_sum = results["CLOUD"][t]
            h_rc, h_failed, h_sum = results["HEAD"][t]
            new_red = sorted(h_failed - c_failed)
            print("  TEST %s  CLOUD: %s | HEAD: %s%s" % (t, c_sum, h_sum, ("  NEWLY RED: %s" % new_red) if new_red else ""))
            if new_red or (h_rc != 0 and not h_failed and c_rc == 0):
                failed_new.append(t)
        red_both = sum(1 for t in tests if results["HEAD"][t][1] and results["HEAD"][t][1] == results["CLOUD"][t][1])
        print("RED ON BOTH CLOUD AND HEAD (same failing set, not newly red): %d test file(s)" % red_both)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    failed = failed_new
    needed = [V2_REL.replace("/AnalysisReport.v2.schema.json", "/tests/test_analysisreport_v2.py")]
    missing = [n for n in needed if n not in tests]
    print("TESTS: %d run on each of CLOUD and HEAD, %d newly red %s; required test missing from the census: %s" % (len(tests), len(failed), failed, missing))
    ok = bool(readers) and bool(tests) and not failed and not missing
    print("RESULT: census %s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    arms = {"schema": arm_schema, "regen": arm_regen, "census": arm_census}
    if len(sys.argv) != 2 or sys.argv[1] not in arms:
        print("usage: u6_checks.py <schema|regen|census>")
        sys.exit(2)
    sys.exit(arms[sys.argv[1]]())
