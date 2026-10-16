"""IRPT_DASHBD round 149, workstream PORTALFIRMGATE (issuer 2.0.0_SA_COO~D2) -- DB-b-314, the CTO's ruling (msg 9933, after the page owner's R154 check): the Performance tab mounts PerformanceTemplateView
ONLY for a 49 Financial client (the one firm whose filled-report data path is being built); Cottonwood joins when its filled report publishes; Inflection never, and Inflection keeps its PATH A performance.
ON the DB-b-309 branch cand/dell2/irpt-49f-performance-template-mount, a follow-up commit on top of 75a71ae3. CLIENT-FACING; the cell lives in the PORTAL repo (<root>/portal).

  DBP181-1-AC1  the diff: only ReportingTab.tsx (at most 8 changed lines) and the one new test file changed since 75a71ae3; the mount sits behind a 49financial test
  DBP181-1-AC2  the tests: the cell's test file names the three firms and passes (49 Financial mounts the template, Cottonwood and Inflection do not, Inflection keeps its PATH A performance)
  DBP181-1-AC3  the proof: every irpt-dashbd test, the typecheck and the production build pass, and the build carries neither the banner nor the fixture

Usage: python <this file> <repo_root> <criterion_id>      prints "<id> PASS" or "<id> FAIL" last
"""
import re
import shutil
import sys
from pathlib import Path

P175 = None


def load_p175():
    global P175
    if P175 is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("p175_for_181", str(Path(__file__).resolve().parent / "p175_portal_template_mount.py"))
        P175 = importlib.util.module_from_spec(spec)
        sys.modules["p175_for_181"] = P175
        spec.loader.exec_module(P175)
    return P175


IR = "src/pages/InvestorReporting/"
BRANCH = "cand/dell2/irpt-49f-performance-template-mount"
BASE = "75a71ae39089baf9fdddcc34cd3075dea4b31701"
TAB = IR + "tabs/reporting/ReportingTab.tsx"
TESTS = IR + "__tests__/irpt-dashbd/"
TEST_PREFIX = "performance-template-firm-gate"


def check_diff(root):
    p175 = load_p175()
    p = p175.portal(root)
    br, _ = p175.git(p, "rev-parse", "--abbrev-ref", "HEAD")
    p175.need(br.strip() == BRANCH, "the portal branch must stay %s (the head Andrew smokes), it is %s" % (BRANCH, br.strip()))
    _, rc = p175.git(p, "merge-base", "--is-ancestor", BASE, "HEAD")
    p175.need(rc == 0, "the DB-b-309 head %s is not an ancestor of this branch" % BASE[:8])
    out, rc = p175.git(p, "diff", "--name-only", BASE, "HEAD")
    p175.need(rc == 0, "cannot diff against %s" % BASE[:8])
    changed = {x for x in out.splitlines() if x.strip()}
    p175.need(changed, "nothing changed since the DB-b-309 head")
    extra = [f for f in changed if f != TAB and not (f.startswith(TESTS) and f.rsplit("/", 1)[-1].startswith(TEST_PREFIX))]
    p175.need(not extra, "portal files outside the agreed write set changed: %s" % extra[:4])
    p175.need(TAB in changed and any(f.startswith(TESTS + TEST_PREFIX) for f in changed), "ReportingTab.tsx and a test file named %s* must both be in the diff" % TEST_PREFIX)
    stat, _ = p175.git(p, "diff", "--numstat", BASE, "HEAD", "--", TAB)
    nums = stat.split()
    p175.need(len(nums) >= 2 and nums[0].isdigit() and int(nums[0]) + int(nums[1]) <= 8, "ReportingTab.tsx may change only by the firm test around the one mount (at most 8 lines): %s" % stat.strip())
    tab = (p / TAB).read_text(encoding="utf-8")
    i = tab.find("<PerformanceTemplateView")
    p175.need(i != -1 and tab.count("<PerformanceTemplateView") == 1, "ReportingTab.tsx must still mount <PerformanceTemplateView exactly once")
    window = tab[max(0, i - 400):i]
    p175.need(re.search(r"49financial", window) is not None, "the mount must sit behind a test for the 49financial firm (the string '49financial' within 400 characters before the mount)")
    return True


def check_tests(root):
    p175 = load_p175()
    p = p175.portal(root)
    files = [f for f in (p / TESTS).glob(TEST_PREFIX + "*") if f.is_file()]
    p175.need(files, "no test file named %s* under %s" % (TEST_PREFIX, TESTS))
    text = " ".join(f.read_text(encoding="utf-8") for f in files).lower()
    for firm in ("49 financial", "cottonwood", "inflection"):
        p175.need(firm in text or firm.replace(" ", "") in text, "the test file does not name the firm %s" % firm)
    p175.need("path a" in text, "the test file must prove that Inflection keeps its PATH A performance (the words 'PATH A')")
    bun = shutil.which("bun")
    p175.need(bun is not None, "bun is not on the PATH")
    r = p175.run([bun, "test", str((files[0]).relative_to(p))], p, 600)
    p175.need(r.returncode == 0, "the cell's tests failed: %s" % (r.stdout + r.stderr)[-800:].replace("\n", " | "))
    p175.need(re.search(r"\b[3-9]\d* pass", r.stdout + r.stderr) is not None or re.search(r"\b\d+ pass", r.stdout + r.stderr) is not None, "bun printed no pass count")
    return True


def check_proof(root):
    p175 = load_p175()
    p = p175.portal(root)
    p175.need(any(f.name.startswith(TEST_PREFIX) for f in (p / TESTS).glob('*')), "the cell's test file %s* is missing" % TEST_PREFIX)
    return p175.check_proof(root)


CHECKS = {"DBP181-1-AC1": check_diff, "DBP181-1-AC2": check_tests, "DBP181-1-AC3": check_proof}

if __name__ == "__main__":
    try:
        CHECKS[sys.argv[2]](sys.argv[1])
        print({"DBP181-1-AC1": "OK: only ReportingTab.tsx (a few lines) and the one new test file changed since the DB-b-309 head, and the template mount sits behind a 49financial test",
               "DBP181-1-AC2": "OK: the cell's test file names the three firms and PATH A and passes",
               "DBP181-1-AC3": "OK: every irpt-dashbd test passes, the typecheck passes and the production build carries neither the banner nor the fixture"}[sys.argv[2]])
        print(sys.argv[2] + " PASS")
    except Exception as ex:  # a failed read or clause is a FAIL, not a traceback
        print("FAIL: " + str(ex))
        print(sys.argv[2] + " FAIL")
        sys.exit(1)
