"""CA-i-5 AC1 (run BEFORE the install): this box (dell2) is ready to host the answer forwarder.

Prints:  I5-PRE ok=<True|False> device=<name> rows=<n> object_id=<n> seq_key=<n> forwarder=<bool> mailbox=<bool> identity=<bool> reason=<text>
Reads only: the device name, the live reader folder's drafts.json (every row must carry object_id and the seq key), the forwarder file in this checkout, the AWS identity (a dell2
agent user in AdministratorAccessOpalCapital) and the live assistant's environment (LDO_MAILBOX_URL and LDO_ID present). Folder: env MUSE_READER_ROOT, else <home>/muse-reader.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

GROUP = "AdministratorAccessOpalCapital"
FUNC = "teams-global-chat-assist-handler-lambda"


def aws(*args):
    exe = shutil.which("aws")
    if not exe:
        raise RuntimeError("aws not found on PATH")
    r = subprocess.run([exe, *args, "--output", "json"], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError("aws %s rc=%s: %s" % (args[0], r.returncode, (r.stderr or "")[:140].strip()))
    return json.loads(r.stdout)


def main():
    dev, rows, oid, seqk, fwd, mailbox, ident, why = "NA", 0, 0, 0, False, False, False, ""
    try:
        dev = subprocess.run([sys.executable, "lib/devices.py", "this"], capture_output=True, text=True, timeout=60).stdout.strip()
        root = Path(os.environ.get("MUSE_READER_ROOT") or (Path.home() / "muse-reader"))
        d = json.loads((root / "drafts.json").read_text(encoding="utf-8"))
        items = d.get("items") or []
        rows = len(items)
        oid = sum(1 for i in items if isinstance(i.get("object_id"), str) and i["object_id"])
        seqk = sum(1 for i in items if "seq" in i)
        fwd = Path("data/transcripts/scripts/muse_reader/forwarder.py").is_file()
        env = (aws("lambda", "get-function-configuration", "--function-name", FUNC).get("Environment") or {}).get("Variables") or {}
        mailbox = bool(env.get("LDO_MAILBOX_URL")) and bool(env.get("LDO_ID"))
        user = aws("sts", "get-caller-identity")["Arn"].rsplit("/", 1)[-1]
        ident = "dell2" in user.lower() and GROUP in [g["GroupName"] for g in aws("iam", "list-groups-for-user", "--user-name", user)["Groups"]]
        if dev != "dell2":
            why = "this box is %r, not dell2 (run from the repository root)" % dev
        elif status_bad(rows, oid, seqk):
            why = "drafts.json rows=%d object_id=%d seq_key=%d: the reader folder is not on the round-17 script yet" % (rows, oid, seqk)
        elif not fwd:
            why = "forwarder.py is not in this checkout"
        elif not mailbox:
            why = "the live assistant's environment gives no LDO_MAILBOX_URL / LDO_ID"
        elif not ident:
            why = "the caller is not a dell2 user in %s" % GROUP
    except Exception as exc:
        why = why or "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I5-PRE ok=%s device=%s rows=%d object_id=%d seq_key=%d forwarder=%s mailbox=%s identity=%s reason=%s"
          % (not why, dev, rows, oid, seqk, fwd, mailbox, ident, why or "none"))


def status_bad(rows, oid, seqk):
    return rows == 0 or oid != rows or seqk != rows


if __name__ == "__main__":
    sys.exit(main() or 0)
