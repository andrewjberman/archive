"""CA-i-3: the forwarder CLI sends ONE well-formed SQS FIFO message through the AWS CLI, takes the queue URL only from the environment,
and refuses loudly when it is unset.

Prints:  I3-CLI ok=<True|False> calls=<n> reason=<text>
The AWS CLI is replaced by a stub named in MUSE_AWS_BIN that records its argv. No network, no AWS.
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path.cwd()
OBJ = "19:jane@unq.gbl.spaces"
URL = "https://sqs.example.invalid/000000000000/test-mailbox.fifo"


def stub(d):
    rec = Path(d) / "calls.jsonl"
    py = Path(d) / "stub_aws.py"
    py.write_text("import json,sys\nopen(%r,'a').write(json.dumps(sys.argv[1:])+'\\n')\nprint(json.dumps({'MessageId':'m-1'}))\n" % str(rec), encoding="utf-8")
    if os.name == "nt":
        exe = Path(d) / "stub_aws.cmd"
        exe.write_text('@echo off\r\n"%s" "%s" %%*\r\n' % (sys.executable, py), encoding="ascii")
    else:
        exe = Path(d) / "stub_aws.sh"
        exe.write_text('#!/bin/sh\nexec "%s" "%s" "$@"\n' % (sys.executable, py), encoding="ascii")
        exe.chmod(0o755)
    return str(exe), rec


def opt(argv, name):
    return argv[argv.index(name) + 1] if name in argv else None


def main():
    why, calls = "", 0
    try:
        with tempfile.TemporaryDirectory() as d:
            root = Path(d) / "folder"
            (root / "answers").mkdir(parents=True)
            (root / "drafts.json").write_text(json.dumps({"source": "drafts", "read_at": "2026-10-13T22:30:00Z", "status": "ok",
                                                         "last_good_at": "2026-10-13T22:30:00Z", "error": None,
                                                         "items": [{"tag": "C123", "object_id": OBJ, "version": 1}]}), encoding="utf-8")
            payload = json.dumps({"tag": "C123", "action": "send", "notes": "", "version": 1, "signed_at": "2026-10-13T22:29:00Z"}, sort_keys=True)
            (root / "answers" / "a.json").write_text(json.dumps({"payload": payload, "signature": "-----BEGIN SSH SIGNATURE-----\nAAAA\n-----END SSH SIGNATURE-----\n"}),
                                                   encoding="utf-8")
            exe, rec = stub(d)
            cmd = [sys.executable, str(ROOT / "data/transcripts/scripts/muse_reader/forwarder.py"), "--root", str(root)]
            env = dict(os.environ, MUSE_AWS_BIN=exe, MUSE_MAILBOX_URL=URL, MUSE_LDO_ID="test-ldo")
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=100, env=env, cwd=str(ROOT))
            lines = [json.loads(x) for x in rec.read_text(encoding="utf-8").splitlines()] if rec.exists() else []
            calls = len(lines)
            if r.returncode != 0 or calls != 1:
                why = "rc=%s calls=%d stderr=%s" % (r.returncode, calls, (r.stderr or "")[:120])
            else:
                argv = lines[0]
                body = opt(argv, "--message-body")
                if body and body.startswith("file://"):
                    body = Path(body[7:].lstrip("/") if os.name == "nt" and body[7:8] == "/" and body[9:10] == ":" else body[7:]).read_text(encoding="utf-8")
                env_doc = json.loads(body)
                if argv[:2] != ["sqs", "send-message"] or opt(argv, "--queue-url") != URL:
                    why = "wrong command or queue url: %s" % argv[:4]
                elif opt(argv, "--message-group-id") in (None, "") or not opt(argv, "--message-deduplication-id"):
                    why = "missing group or dedup id"
                elif env_doc.get("kind") != "muse.reply" or env_doc.get("object_id") != OBJ or "answer" not in env_doc.get("payload", {}):
                    why = "envelope wrong: %s" % sorted(env_doc)
                elif env_doc.get("event_id") != opt(argv, "--message-deduplication-id") and not str(env_doc.get("event_id", "")).startswith("muse-"):
                    why = "event id not muse-<sha256>"
            if not why:
                env2 = {k: v for k, v in env.items() if k != "MUSE_MAILBOX_URL"}
                before = calls
                r2 = subprocess.run(cmd, capture_output=True, text=True, timeout=100, env=env2, cwd=str(ROOT))
                after = len(rec.read_text(encoding="utf-8").splitlines())
                if r2.returncode == 0 or "MUSE_MAILBOX_URL" not in ((r2.stdout or "") + (r2.stderr or "")) or after != before:
                    why = "unset MUSE_MAILBOX_URL not refused loudly (rc=%s)" % r2.returncode
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I3-CLI ok=%s calls=%d reason=%s" % (not why, calls, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
