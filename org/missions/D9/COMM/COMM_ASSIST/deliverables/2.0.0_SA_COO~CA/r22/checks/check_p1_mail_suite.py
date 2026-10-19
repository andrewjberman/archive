"""CA-p-1 AC2: the four existing mail test files all still pass (the bound; it PASSES at the base).

Runs, from the repository root, each of
  data/transcripts/scripts/tests/test_inbound_mail_draft.py  (last line MAIL-DRAFT ok=True)
  data/transcripts/scripts/tests/test_inbound_mail.py        (last line INBOUND-MAIL-TEST ok=True)
  data/transcripts/scripts/tests/test_inbound_mail_reply.py  (last line INBOUND-MAIL-REPLY-TEST ok=True)
  data/transcripts/scripts/tests/test_inbound_mail_poll.py   (last line MAIL-POLL ok=True)
under a 100 second limit each, and prints one line per file and a last line P1-MAILSUITE ok=True|False tests=<passed> of 4.
Finds the repository from the current directory's git toplevel; the seam P1_ROOT points it at another copy. No network, no AWS.
"""
import os
import subprocess
import sys

ROOT = os.environ.get("P1_ROOT") or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                                                   text=True, check=True).stdout.strip()
TESTS = (("test_inbound_mail_draft.py", "MAIL-DRAFT ok=True"), ("test_inbound_mail.py", "INBOUND-MAIL-TEST ok=True"),
         ("test_inbound_mail_reply.py", "INBOUND-MAIL-REPLY-TEST ok=True"), ("test_inbound_mail_poll.py", "MAIL-POLL ok=True"))


def main():
    passed = 0
    for name, want in TESTS:
        path = os.path.join(ROOT, "data", "transcripts", "scripts", "tests", name)
        try:
            out = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=100, cwd=ROOT).stdout
            last = (out.strip().splitlines() or [""])[-1]
        except subprocess.TimeoutExpired:
            last = "TIMEOUT"
        ok = want in last
        print("%s ok=%s last=%s" % (name, ok, last[:90]))
        passed += 1 if ok else 0
    print("P1-MAILSUITE ok=%s tests=%d of %d" % (passed == len(TESTS), passed, len(TESTS)))
    return 0 if passed == len(TESTS) else 1


if __name__ == "__main__":
    sys.exit(main())
