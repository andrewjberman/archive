"""CA-i-8: the text that carries a received-mail draft tells Andrew how to answer it: 1 approves, notes redraft, 0 drops, #dev opens a job.

Prints:  I8-FOOTER ok=<True|False> has_one=<bool> has_notes=<bool> has_zero=<bool> has_dev=<bool> reason=<text>
Texts one mail item through the mail-reply test harness (mail_requests.on_mail_messages) and reads the last line block of the text he receives.
No AWS, no network.
"""
import contextlib
import importlib.util
import io
import re
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "infra" / "aws" / "terraform" / "modules" / "ldo" / "runtime"))


def main():
    flags = {"one": False, "notes": False, "zero": False, "dev": False}
    why = ""
    try:
        spec = importlib.util.spec_from_file_location("mail_harness", ROOT / "data/transcripts/scripts/tests/test_inbound_mail_reply.py")
        H = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(H)
        w = H.World()
        with contextlib.redirect_stdout(io.StringIO()):
            H.mail_item(w)
        text = w.texts[-1][1]
        tail = text.strip().splitlines()[-1].lower()
        flags["one"] = bool(re.search(r"(^|[^0-9#])1([^0-9]|$)", tail))
        flags["notes"] = "notes" in tail and "redraft" in tail
        flags["zero"] = bool(re.search(r"(^|[^0-9#])0([^0-9]|$)", tail))
        flags["dev"] = "#dev" in tail
        if not all(flags.values()):
            why = "last line of the text is %r" % tail[:160]
        elif "paste" not in tail and "approve" not in tail:
            why = "the last line does not say what 1 does: %r" % tail[:160]
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I8-FOOTER ok=%s has_one=%s has_notes=%s has_zero=%s has_dev=%s reason=%s"
          % (not why, flags["one"], flags["notes"], flags["zero"], flags["dev"], why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
