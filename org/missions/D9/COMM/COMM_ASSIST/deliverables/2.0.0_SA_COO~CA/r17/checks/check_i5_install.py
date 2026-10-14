"""CA-i-5 AC2 (run AFTER the install): the answer forwarder is installed on dell2 and scheduled, with its address taken from the live assistant.

Prints:  I5-INSTALL ok=<True|False> task=<found|absent> last_result=<n> env_url=<bool> env_ldo=<bool> folders=<bool> reason=<text>
Passes only if: this box is dell2; the scheduled task MuseAnswerForward exists and its last result is 0; the user-level environment variables MUSE_MAILBOX_URL and MUSE_LDO_ID
equal the LDO_MAILBOX_URL and LDO_ID the live handler function carries; and answers/, answers/done/ and answers/rejected/ exist in the reader folder
(env MUSE_READER_ROOT, else <home>/muse-reader). Read-only.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

TASK = "MuseAnswerForward"
FUNC = "teams-global-chat-assist-handler-lambda"


def ps(cmd):
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd], capture_output=True, text=True, timeout=60)
    return r.returncode, (r.stdout or "").strip()


def main():
    task, last, env_url, env_ldo, folders, why = "absent", "NA", False, False, False, ""
    try:
        dev = subprocess.run([sys.executable, "lib/devices.py", "this"], capture_output=True, text=True, timeout=60).stdout.strip()
        if dev != "dell2":
            raise RuntimeError("this box is %r, not dell2 (run from the repository root)" % dev)
        exe = shutil.which("aws")
        r = subprocess.run([exe, "lambda", "get-function-configuration", "--function-name", FUNC, "--output", "json"], capture_output=True, text=True, timeout=60)
        live = (json.loads(r.stdout).get("Environment") or {}).get("Variables") or {}
        rc, out = ps("[Environment]::GetEnvironmentVariable('MUSE_MAILBOX_URL','User') + '|' + [Environment]::GetEnvironmentVariable('MUSE_LDO_ID','User')")
        have_url, _, have_ldo = out.partition("|")
        env_url = bool(live.get("LDO_MAILBOX_URL")) and have_url == live.get("LDO_MAILBOX_URL")
        env_ldo = bool(live.get("LDO_ID")) and have_ldo == live.get("LDO_ID")
        rc, out = ps("(Get-ScheduledTaskInfo -TaskName %s -ErrorAction Stop).LastTaskResult" % TASK)
        if rc == 0 and out.lstrip("-").isdigit():
            task, last = "found", out
        root = Path(os.environ.get("MUSE_READER_ROOT") or (Path.home() / "muse-reader"))
        folders = all((root / "answers" / s).is_dir() for s in ("", "done", "rejected"))
        if task != "found":
            why = "scheduled task %s not found" % TASK
        elif last != "0":
            why = "last task result %s" % last
        elif not env_url or not env_ldo:
            why = "the user environment does not equal the live handler's LDO_MAILBOX_URL / LDO_ID"
        elif not folders:
            why = "answers/, answers/done/ or answers/rejected/ is missing"
    except Exception as exc:
        why = why or "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I5-INSTALL ok=%s task=%s last_result=%s env_url=%s env_ldo=%s folders=%s reason=%s" % (not why, task, last, env_url, env_ldo, folders, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
