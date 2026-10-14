#!/usr/bin/env python3
"""Round 110, cell DB-b-219: the shared as-of helper never shows an invented clock.

Run as:  python -I <this file> <root> <CRITERION_ID>      (root = the worktree root; the portal is root/portal)

  DB110-4-AC1  the new test file exists, holds the required cases, and passes under two runtime zones (bun test)
  DB110-4-AC2  the old pin of the invented clock is re-pinned, and the neighbours' existing tests pass (bun test)
  DB110-4-AC3  no product file builds its own 17:00 timestamp, the date path of formatPanelTimestamp does not make a
               5pm instant, and the worker's record is complete and bound to a portal commit

Prints `<ID> PASS` or `<ID> FAIL` with the reason. Stdlib only; every subprocess is bounded.
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

RECORD = "org/missions/D9/IRPT/IRPT_DASHBD/deliverables/0.9.0_WK_IRPT_DASHBD~176/ASOF_R110.json"
NEW_TEST = "src/lib/__tests__/as-of-no-invented-clock.test.ts"
OLD_PIN_TEST = "src/lib/__tests__/create5pm-et.test.ts"
NEIGHBOURS = [
    OLD_PIN_TEST,
    "src/pages/Positioning/panels/footer-date-format.test.ts",
    "src/pages/Positioning/shared/PageEnd.test.tsx",
    "src/pages/InvestorReporting/__tests__/dsgn-irptv1/iv-e-45.face-batch.test.tsx",
]
VERDICT = "VERDICT: ASOF-NO-INVENTED-CLOCK-OK"
PROD_RELEASE = "6a5926fc"
TEST_RX = re.compile(r"(^|/)(__tests__|__harness__|__fixtures__|__mocks__)/|\.(test|spec)\.[cm]?[jt]sx?$|\.harness\.cjs$")


class Fail(Exception):
    pass


def need(cond, why):
    if not cond:
        raise Fail(why)


def read(p):
    return Path(p).read_bytes().decode("utf-8")


def bun():
    b = shutil.which("bun")
    need(b, "bun is not on PATH")
    return b


def bun_test(portal, files, tz):
    env = dict(os.environ)
    env["TZ"] = tz
    r = subprocess.run([bun(), "test"] + files, cwd=str(portal), env=env, capture_output=True, timeout=100)
    out = (r.stdout + r.stderr).decode("utf-8", "replace")
    return r.returncode, out


def check_ac1(root):
    portal = root / "portal"
    f = portal / NEW_TEST
    need(f.is_file(), "the new test file %s does not exist" % NEW_TEST)
    src = read(f)
    for tok in ("setSystemTime", "2026-10-14T18:37:00Z", "p ET", VERDICT, "create5pmETDate", "DataAsOfCompact"):
        need(tok in src, "the test file must hold %r (the required case or the verdict line)" % tok)
    for tz in ("UTC", "America/Los_Angeles"):
        rc, out = bun_test(portal, [NEW_TEST], tz)
        need(rc == 0 and VERDICT in out, "bun test %s under TZ=%s: rc=%d, verdict line %s" % (NEW_TEST, tz, rc, "present" if VERDICT in out else "absent"))
    print("OK: the new test holds the required cases and passes under TZ=UTC and TZ=America/Los_Angeles")


def check_ac2(root):
    portal = root / "portal"
    old = read(portal / OLD_PIN_TEST)
    need("endsWith(', 5:00p ET')" not in old, "%s still pins the invented clock on a date-only footer (endsWith(', 5:00p ET'))" % OLD_PIN_TEST)
    need("getUTCHours" in old, "%s must keep pinning the 5pm instant create5pmETDate returns for calculations" % OLD_PIN_TEST)
    for n in NEIGHBOURS:
        need((portal / n).is_file(), "neighbour test %s is missing" % n)
    rc, out = bun_test(portal, NEIGHBOURS, "UTC")
    need(rc == 0, "bun test of the %d neighbour test files failed (rc=%d): %s" % (len(NEIGHBOURS), rc, out.strip().splitlines()[-1] if out.strip() else ""))
    print("OK: the old pin is re-pinned and %d neighbour test files pass" % len(NEIGHBOURS))


def body_of(text, head):
    i = text.find(head)
    need(i >= 0, "%r not found" % head)
    j = text.find("\n}\n", i)
    return text[i:j if j > 0 else len(text)]


def check_ac3(root):
    portal = root / "portal"
    src = portal / "src"
    need(src.is_dir(), "portal/src is missing")
    seen = 0
    for p in src.rglob("*"):
        if p.suffix not in (".ts", ".tsx") or TEST_RX.search(p.as_posix()):
            continue
        seen += 1
        for ln, line in enumerate(read(p).splitlines(), 1):
            s = line.strip()
            if "17:00:00" in s and not s.startswith(("*", "//", "/*")):
                raise Fail("%s:%d builds its own 17:00 timestamp: %s" % (p.relative_to(portal).as_posix(), ln, s[:100]))
    du = read(src / "lib/dateUtils.ts")
    need("create5pmETDate" not in body_of(du, "export function formatPanelTimestamp("), "formatPanelTimestamp still builds a 5pm instant for display")
    da = read(src / "components/DataAsOf.tsx")
    need("utcHour" not in da, "DataAsOf.tsx still builds a 5pm instant (utcHour) for display")
    r = json.loads(read(root / RECORD))
    pt = r.get("portal") or {}
    need(pt.get("branch") == "wk-IRPT_DASHBD-176-portal" and re.fullmatch(r"[0-9a-f]{7,40}", str(pt.get("commit") or "")), "portal %r: the branch wk-IRPT_DASHBD-176-portal and a commit" % pt)
    g = subprocess.run(["git", "-C", str(portal), "cat-file", "-t", pt["commit"]], capture_output=True, text=True, timeout=60)
    need(g.returncode == 0 and g.stdout.strip() == "commit", "the portal commit %s does not exist in the portal repo" % pt["commit"])
    a = subprocess.run(["git", "-C", str(portal), "merge-base", "--is-ancestor", PROD_RELEASE, pt["commit"]], capture_output=True, timeout=60)
    need(a.returncode == 0, "the portal commit must descend from the PROD release %s" % PROD_RELEASE)
    fc = pt.get("files_changed")
    need(isinstance(fc, list) and fc and all(str(x).startswith("src/") for x in fc), "files_changed must list portal files under src/")
    c = r.get("callers") or {}
    need(all(isinstance(c.get(k), int) and c.get(k) >= 0 for k in ("files_scanned", "date_only_callers", "real_timestamp_callers")) and c["files_scanned"] >= 25, "callers must carry integer files_scanned (at least 25), date_only_callers and real_timestamp_callers")
    t = r.get("tests") or {}
    need(t.get("mutant_failed") is True and t.get("lint_errors") == 0 and t.get("typecheck_errors") == 0 and (t.get("suite_after") or {}).get("new_failing_ids") == [], "tests: mutant_failed true, lint 0, typecheck 0, no new failing test")
    need(r.get("pushed") is False and r.get("deployed") is False, "pushed and deployed must be false (the issuer pushes the candidate)")
    print("OK: %d product files scanned, none builds a 17:00 timestamp; the display paths make no 5pm instant; record bound to a portal commit descending from %s" % (seen, PROD_RELEASE))


CHECKS = {"DB110-4-AC1": check_ac1, "DB110-4-AC2": check_ac2, "DB110-4-AC3": check_ac3}


def main(argv):
    if len(argv) != 3 or argv[2] not in CHECKS:
        print("usage: p110_asof.py <root> <%s>" % "|".join(CHECKS))
        return 2
    cid = argv[2]
    try:
        CHECKS[cid](Path(argv[1]).resolve())
    except Fail as e:
        print("FAIL: %s" % e)
        print("%s FAIL" % cid)
        return 1
    except (OSError, ValueError, KeyError, subprocess.TimeoutExpired) as e:
        print("FAIL: %s: %s" % (type(e).__name__, e))
        print("%s FAIL" % cid)
        return 1
    print("%s PASS" % cid)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
