"""CA-j-5, the issuer's REAL RUN after the flip (run by 2.0.0_SA_COO~CA, never by the deploying seat): an UNMARKED `sms.reply` put on the assistant's mailbox is refused and recorded, and does nothing.

Prints:  K5-FORGED ok=<True|False> sent=<bool> state_row=<bool> refused=<bool> reason=<no-mark|...> kind=<...> unmarked_seen=<n> extra_keys=<sorted keys beyond the three> reason_text=<text>
The event goes to a DUMMY object `probe:ca-j-5-forged-<UTC stamp>` that is no chat, no draft and no owner object, with the shape the ingress sends (an `sms.reply` envelope with tag null, action drop,
notes empty) and NO mark. In enforce mode the handler's dispatch refuses it BEFORE any route runs: it writes the state row with mark_refusals (reason no-mark, kind sms.reply, tag None) and unmarked_seen 1, and
nothing else (no `pending`, no `kind`, no text). Any other state, or no state row within the wait, is a FAIL. It sends ONE event, reads ONE state row by key, prints metadata only, and reads no message content.
Needs the caller's identity to be allowed sqs:SendMessage on the mailbox and dynamodb:GetItem on the state table; if it is not, that is printed (a refusal is itself a finding about who can write the queue).
"""
import datetime
import json
import os
import subprocess
import sys
import time
import uuid

MAILBOX = "teams-global-chat-assist-queue.fifo"
TABLE = "teams-global-chat-assist-table"
WAIT_S = 150
EXE = "aws.cmd" if os.name == "nt" else "aws"


def aws(*args):
    r = subprocess.run([EXE, *args, "--output", "json"], capture_output=True, text=True, encoding="utf-8", timeout=90)
    if r.returncode != 0:
        return None, ((r.stderr or "").strip().splitlines() or ["rc=%d" % r.returncode])[-1]
    return (json.loads(r.stdout) if r.stdout.strip() else {}), None


def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    oid = "probe:ca-j-5-forged-" + now.strftime("%Y%m%dT%H%M%SZ")
    sent, state_row, refused, reason, kind, seen, extra, why = False, False, False, None, None, None, [], ""
    try:
        url, err = aws("sqs", "get-queue-url", "--queue-name", MAILBOX)
        if not url:
            raise RuntimeError("queue url: %s" % err)
        eid = "evt-forged-" + uuid.uuid4().hex
        env = {"ldo": 1, "ldo_id": "LDO-001", "object_id": oid, "event_id": eid, "kind": "sms.reply",
               "payload": {"tag": None, "action": "drop", "notes": ""}, "sent_at": now.strftime("%Y-%m-%dT%H:%M:%SZ")}
        _, err = aws("sqs", "send-message", "--queue-url", url["QueueUrl"], "--message-body", json.dumps(env, sort_keys=True),
                     "--message-group-id", oid, "--message-deduplication-id", eid)
        if err:
            raise RuntimeError("send refused: %s" % err)
        sent = True
        key = json.dumps({"pk": {"S": oid}, "sk": {"S": "state"}})
        deadline = time.time() + WAIT_S
        row = None
        while time.time() < deadline:
            doc, err = aws("dynamodb", "get-item", "--table-name", TABLE, "--key", key, "--consistent-read")
            if doc and doc.get("Item"):
                row = json.loads(doc["Item"]["data"]["S"])
                break
            time.sleep(10)
        if row is None:
            raise RuntimeError("no state row for the probe object within %d seconds" % WAIT_S)
        state_row = True
        refusals = row.get("mark_refusals") or []
        last = refusals[-1] if refusals else {}
        reason, kind, seen = last.get("reason"), last.get("kind"), row.get("unmarked_seen")
        extra = sorted(set(row) - {"mark_refusals", "unmarked_seen", "marks_seen"})
        refused = reason == "no-mark" and kind == "sms.reply" and last.get("tag") is None and seen == 1 and not extra
        if not refused:
            why = "the state is not exactly one no-mark refusal (reason=%s kind=%s unmarked_seen=%s extra=%s)" % (reason, kind, seen, extra)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("K5-FORGED ok=%s sent=%s state_row=%s refused=%s reason=%s kind=%s unmarked_seen=%s extra_keys=%s reason_text=%s object=%s"
          % (refused and not why, sent, state_row, refused, reason, kind, seen, extra, why or "none", oid))


if __name__ == "__main__":
    sys.exit(main() or 0)
