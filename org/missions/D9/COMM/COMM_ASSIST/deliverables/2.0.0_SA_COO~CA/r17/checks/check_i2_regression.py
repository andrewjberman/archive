"""CA-i-2 AC2: the assistant's existing flow tests still pass after the receiver change (the text path is the fallback and must not move).

Prints:  I2-REGRESSION ok=<True|False> passed=<n> failed=<n> reason=<text>
Runs pytest over data/transcripts/scripts/tests/test_teams_chat_tenant.py from the current directory, no network, bounded to 100 seconds.
"""
import re
import subprocess
import sys

TARGET = "data/transcripts/scripts/tests/test_teams_chat_tenant.py"


def main():
    passed = failed = 0
    why = ""
    try:
        r = subprocess.run([sys.executable, "-m", "pytest", TARGET, "-q", "-x", "-p", "no:cacheprovider"], capture_output=True, text=True, timeout=100)
        tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
        m_p, m_f = re.search(r"(\d+) passed", tail[0]), re.search(r"(\d+) failed", tail[0])
        passed, failed = int(m_p.group(1)) if m_p else 0, int(m_f.group(1)) if m_f else 0
        if r.returncode != 0 or failed or passed == 0:
            why = "pytest rc=%s: %s" % (r.returncode, tail[0][:120])
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:160])
    print("I2-REGRESSION ok=%s passed=%d failed=%d reason=%s" % (not why, passed, failed, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
