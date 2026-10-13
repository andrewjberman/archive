"""CA-h-2 AC2: the muse reader folder on this box is refreshed BY ITS SCHEDULED TASK, not by hand.

Folder: env MUSE_READER_ROOT, else <home>/muse-reader. Task name: MuseReaderRefresh.
Prints:  H2-SCHEDULED ok=<True|False> task=<found|absent> last_result=<n> age_min=<n> ok=<n> absent=<n> unreadable=<n> reason=<text>
Passes only if the task exists, its last result is 0, INDEX.json run_at is under 35 minutes old and within 2 minutes of the
task's LastRunTime (so the folder was written by the task), drafts and open_calls are ok, and nothing is unreadable.
"""
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

TASK = "MuseReaderRefresh"


def ps(cmd):
    r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd], capture_output=True, text=True, timeout=60)
    return r.returncode, (r.stdout or "").strip()


def main():
    root = Path(os.environ.get("MUSE_READER_ROOT") or (Path.home() / "muse-reader"))
    task, last_result, age, counts, why = "absent", "NA", "NA", {"ok": "NA", "absent": "NA", "unreadable": "NA"}, ""
    try:
        rc, out = ps("$t=Get-ScheduledTask -TaskName %s -ErrorAction Stop; $i=Get-ScheduledTaskInfo -TaskName %s; "
                     "'{0}|{1}' -f $i.LastTaskResult,$i.LastRunTime.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')" % (TASK, TASK))
        if rc != 0 or "|" not in out:
            why = "scheduled task %s not found" % TASK
        else:
            task = "found"
            last_result, last_run = out.splitlines()[-1].split("|", 1)
            idx = json.loads((root / "INDEX.json").read_text(encoding="utf-8"))
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            run_at = datetime.datetime.strptime(idx["run_at"], fmt)
            last_run_dt = datetime.datetime.strptime(last_run, fmt)
            now = datetime.datetime.utcnow()
            age = round((now - run_at).total_seconds() / 60.0, 1)
            st = {k: v["status"] for k, v in idx["sources"].items()}
            counts = {k: sum(1 for s in st.values() if s == k) for k in ("ok", "absent", "unreadable")}
            if last_result != "0":
                why = "last task result %s" % last_result
            elif age > 35:
                why = "INDEX.json is %s minutes old" % age
            elif abs((run_at - last_run_dt).total_seconds()) > 120:
                why = "INDEX.json run_at is not within 2 minutes of the task's last run (written by hand?)"
            elif st.get("drafts") != "ok" or st.get("open_calls") != "ok":
                why = "drafts or open_calls not ok: %s" % st
            elif counts["unreadable"]:
                why = "a source is unreadable"
    except Exception as exc:
        why = str(exc)[:200]
    print("H2-SCHEDULED ok=%s task=%s last_result=%s age_min=%s ok=%s absent=%s unreadable=%s reason=%s"
          % (not why, task, last_result, age, counts["ok"], counts["absent"], counts["unreadable"], why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
