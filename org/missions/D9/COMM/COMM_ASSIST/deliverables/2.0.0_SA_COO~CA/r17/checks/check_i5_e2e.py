"""CA-i-5 AC3: the whole answer path works, end to end, on a FORGED answer -- it travels folder -> forwarder -> queue -> assistant and is REFUSED, and nothing else happens.

Prints:  I5-E2E ok=<True|False> forwarded=<n> refused=<reason|none> waited_s=<n> reason=<text>
Run on dell2 AFTER the install. It writes ONE answer file for a draft that is waiting now, signed by a THROWAWAY key (never the pinned one), runs the installed forwarder once, then reads the
draft's state row for up to 150 seconds: the assistant must have recorded a refusal with reason `bad-signature` for that tag. The action is `drop` and the notes say it is a test; the signature
cannot verify, so no draft is touched. It does not use muse's key and cannot act in Andrew's name.
"""
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

FUNC = "teams-global-chat-assist-handler-lambda"
TABLE = "teams-global-chat-assist-table"


def aws(*args):
    r = subprocess.run([shutil.which("aws"), *args, "--output", "json"], capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        raise RuntimeError("aws %s rc=%s: %s" % (args[0], r.returncode, (r.stderr or "")[:140].strip()))
    return json.loads(r.stdout) if r.stdout.strip() else {}


def refusals(object_id):
    with tempfile.TemporaryDirectory() as d:
        key = Path(d) / "key.json"
        key.write_text(json.dumps({"pk": {"S": object_id}, "sk": {"S": "state"}}), encoding="ascii")
        item = aws("dynamodb", "get-item", "--table-name", TABLE, "--key", "file://" + str(key).replace("\\", "/"), "--consistent-read").get("Item")
    return (json.loads(item["data"]["S"]).get("muse_refusals") or []) if item else []


def main():
    forwarded, refused, waited, why = 0, "none", 0, ""
    try:
        dev = subprocess.run([sys.executable, "lib/devices.py", "this"], capture_output=True, text=True, timeout=60).stdout.strip()
        if dev != "dell2":
            raise RuntimeError("this box is %r, not dell2 (run from the repository root)" % dev)
        root = Path(os.environ.get("MUSE_READER_ROOT") or (Path.home() / "muse-reader"))
        rows = json.loads((root / "drafts.json").read_text(encoding="utf-8")).get("items") or []
        row = next((r for r in rows if r.get("tag") and r.get("object_id") and r.get("version") is not None), None)
        if not row:
            raise RuntimeError("no waiting draft to aim the test at")
        live = (aws("lambda", "get-function-configuration", "--function-name", FUNC).get("Environment") or {}).get("Variables") or {}
        now = datetime.datetime.now(datetime.timezone.utc)
        payload = json.dumps({"tag": row["tag"], "action": "drop", "notes": "ISSUER-E2E-REFUSAL-TEST, signed by a throwaway key", "version": row["version"],
                              "seq": row.get("seq"), "signed_at": now.strftime("%Y-%m-%dT%H:%M:%SZ")}, sort_keys=True)
        before = len(refusals(row["object_id"]))
        with tempfile.TemporaryDirectory() as d:
            k = Path(d) / "throwaway"
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", str(k)], check=True, capture_output=True, timeout=60)
            p = Path(d) / "payload.json"
            p.write_bytes(payload.encode("utf-8"))
            subprocess.run(["ssh-keygen", "-q", "-Y", "sign", "-f", str(k), "-n", "muse-answer@opal", str(p)], check=True, capture_output=True, timeout=60)
            sig = Path(str(p) + ".sig").read_text(encoding="ascii")
        name = "e2e-%s.json" % now.strftime("%Y%m%dT%H%M%SZ")
        (root / "answers" / name).write_text(json.dumps({"payload": payload, "signature": sig}, sort_keys=True), encoding="utf-8")
        env = dict(os.environ, MUSE_MAILBOX_URL=live["LDO_MAILBOX_URL"], MUSE_LDO_ID=live["LDO_ID"])
        r = subprocess.run([sys.executable, "data/transcripts/scripts/muse_reader/forwarder.py", "--root", str(root)], capture_output=True, text=True, timeout=100, env=env)
        forwarded = 1 if "sent=1" in (r.stdout or "") else 0
        if not forwarded:
            raise RuntimeError("the forwarder did not report sent=1: %s" % ((r.stdout or "") + (r.stderr or ""))[:160])
        start = time.time()
        while time.time() - start < 150:
            waited = int(time.time() - start)
            new = refusals(row["object_id"])[before:]
            hit = [x for x in new if x.get("tag") == row["tag"] and x.get("reason") == "bad-signature"]
            if hit:
                refused = hit[-1]["reason"]
                break
            time.sleep(10)
        if refused != "bad-signature":
            why = "no bad-signature refusal recorded for %s within 150 seconds" % row["tag"]
    except Exception as exc:
        why = why or "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I5-E2E ok=%s forwarded=%d refused=%s waited_s=%d reason=%s" % (not why, forwarded, refused, waited, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
