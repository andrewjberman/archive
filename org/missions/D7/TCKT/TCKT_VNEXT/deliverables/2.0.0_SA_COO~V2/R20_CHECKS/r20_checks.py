#!/usr/bin/env python3
"""TCKT_VNEXT round 20 -- the issuer's checks for cell R20-pt-1 (the Ticket Center's meeting outcome line and coordinator controls).

  pt-outcome   the ten named tests of `src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx` all exist and `bun test` of that
               file passes with no failure. Prints R20-PT-OK pass=<n> or R20-PT-BAD <reason>.
  portal-tsc   `bun x tsc -b` in the portal worktree exits 0. Prints R20-TSC-OK or R20-TSC-BAD rc=<n>.
  --self-test  a good and a bad fixture file for the name scan (no bun, no portal). Prints R20-SELFTEST-OK.

Usage: python r20_checks.py pt-outcome --portal <portal dir>   |   python r20_checks.py portal-tsc --portal <portal dir>
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TEST = Path("src/pages/TicketCenter/__tests__/meeting-outcome-visibility.test.tsx")
NAMES = [
    "shows the waiting words on an open meeting ticket with no outcome",
    "shows the confirmed outcome on a completed meeting ticket",
    "shows the proposed times on a completed meeting ticket",
    "shows nothing for a completed meeting ticket that has no meeting outcome",
    "shows the outcome line to a viewer who is not the coordinator",
    "shows the coordinator's controls to a viewer in routing.primary",
    "matches the viewer's email to routing.primary without regard to case",
    "hides the coordinator's controls from a viewer who is not in routing.primary",
    "never shows the coordinator's controls on a completed ticket",
    "draws no outcome line for a ticket that is not a meeting request",
]
STRIP = re.compile(r"\x1b\[[0-9;]*m")


def missing_names(src):
    return [n for n in NAMES if ("'%s'" % n) not in src and ('"%s"' % n) not in src and ("`%s`" % n) not in src]


def pt_outcome(portal):
    test = Path(portal) / TEST
    if not test.exists():
        return "R20-PT-BAD absent: %s" % test.as_posix()
    miss = missing_names(test.read_text(encoding="utf-8"))
    if miss:
        return "R20-PT-BAD missing test(s): %s" % "; ".join(miss)
    bun = shutil.which("bun")
    if not bun:
        return "R20-PT-BAD bun not on PATH"
    r = subprocess.run([bun, "test", TEST.as_posix()], cwd=str(portal), capture_output=True, text=True, timeout=170)
    out = STRIP.sub("", r.stdout + r.stderr)
    passed = int((re.search(r"(\d+) pass", out) or [0, 0])[1])
    failed = int((re.search(r"(\d+) fail", out) or [0, 0])[1])
    if r.returncode != 0 or failed or passed < len(NAMES):
        return "R20-PT-BAD rc=%d pass=%d fail=%d of %d" % (r.returncode, passed, failed, len(NAMES))
    return "R20-PT-OK pass=%d" % passed


def portal_tsc(portal):
    bun = shutil.which("bun")
    if not bun:
        return "R20-TSC-BAD bun not on PATH"
    r = subprocess.run([bun, "x", "tsc", "-b"], cwd=str(portal), capture_output=True, text=True, timeout=170)
    return "R20-TSC-OK" if r.returncode == 0 else "R20-TSC-BAD rc=%d" % r.returncode


def selftest():
    good = "\n".join("test('%s', () => {})" % n for n in NAMES)
    bad = "\n".join("test('%s', () => {})" % n for n in NAMES[:-1])
    if missing_names(good):
        return "good fixture refused"
    if missing_names(bad) != [NAMES[-1]]:
        return "bad fixture not caught"
    with tempfile.TemporaryDirectory() as d:
        if not pt_outcome(d).startswith("R20-PT-BAD absent"):
            return "absent file not refused"
    return None


def main(argv):
    if argv[:1] == ["--self-test"]:
        why = selftest()
        print("R20-SELFTEST-OK" if why is None else "R20-SELFTEST-FAIL " + why)
        return 0 if why is None else 1
    if len(argv) < 3 or argv[0] not in ("pt-outcome", "portal-tsc") or argv[1] != "--portal":
        print("usage: r20_checks.py pt-outcome|portal-tsc --portal <dir> | --self-test")
        return 2
    out = pt_outcome(argv[2]) if argv[0] == "pt-outcome" else portal_tsc(argv[2])
    print(out)
    return 0 if out.endswith("OK") or " OK" in out or "-OK" in out else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
