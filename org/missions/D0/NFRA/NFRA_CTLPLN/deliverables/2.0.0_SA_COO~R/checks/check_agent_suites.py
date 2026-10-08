"""Issuer's bound check for NFRA_CTLPLN workstream INBOUND (round 7 on): the Teams agent's existing suites still pass.
Runs the seven pytest files from their own folder (they import a sibling test module) and the mail-reply script.
Offline; no network. Last line: AGENT-SUITE ok=<True|False> pytest_rc=<n> mail_reply_rc=<n>."""
from __future__ import annotations

import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 8)))
TESTS = os.path.join(ROOT, "data", "transcripts", "scripts", "tests")
FILES = ["test_teams_chat_tenant.py", "test_teams_chat_assist.py", "test_teams_chat_stale_eod.py",
         "test_teams_chat_eod_republish.py", "test_teams_chat_natural.py", "test_teams_chat_jobs.py", "test_eod_voice.py"]


def main() -> int:
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *FILES], cwd=TESTS,
                       capture_output=True, text=True, timeout=110)
    tail = (p.stdout or "").strip().splitlines()[-1:] or [""]
    print("pytest:", tail[0])
    m = subprocess.run([sys.executable, os.path.join(TESTS, "test_inbound_mail_reply.py")], cwd=ROOT,
                       capture_output=True, text=True, timeout=60)
    mt = (m.stdout or "").strip().splitlines()[-1:] or [""]
    print("mail_reply:", mt[0])
    ok = p.returncode == 0 and m.returncode == 0
    print("AGENT-SUITE ok=%s pytest_rc=%d mail_reply_rc=%d" % (ok, p.returncode, m.returncode))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
