"""IB-pr-460 consumer arm (offline; ASCII). Run as
    python -I consumer_arm_460.py <worktree_root> <answers_json> <out_json>
Loads the drafter's own make_draft_store (data/transcripts/scripts/commentary/lambda_handler.py, the worktree's committed bytes) and hands it a
FAKE lambda client whose invoke answers, in turn, (a) today's two-member first-persist answer and (b) the built three-member answer (both
taken from the cell's answers file, produced by the tested store). Nothing is invoked in AWS: boto3 is never imported, sockets are refused.
Records what existing_draft (get_ref) and persist_draft (put) return for each, so the one consumer's behaviour on the new member is shown."""
import io
import json
import socket
import sys

root, answers_path, out_path = sys.argv[1:4]
sys.dont_write_bytecode = True
sys.path.insert(0, root)


def _refuse(self, *a, **k):
    raise OSError("OFFLINE-GUARD")


socket.socket.connect = _refuse
from data.transcripts.scripts.commentary import lambda_handler as lh  # noqa: E402

A = json.load(open(answers_path, encoding="utf-8"))
REF = A["first_persist_without_ticket_id"]["commentary_ref"]


class Client:
    def __init__(self, answers):
        self.answers, self.calls = list(answers), []

    def invoke(self, FunctionName, InvocationType, Payload):
        self.calls.append((FunctionName, InvocationType, json.loads(Payload.decode("ascii"))))
        return {"Payload": io.BytesIO(json.dumps(self.answers.pop(0)).encode("utf-8"))}


def run(put_answer):
    c = Client([put_answer, {"status": "OK", "commentary_ref": REF}])
    existing, persist = lh.make_draft_store(c, "synthetic-draft-store-function")
    got = persist("synthetic-firm-one", "REQ-" + "a" * 24, {"draft_text": "A synthetic draft.", "request_id": "REQ-" + "a" * 24, "provenance": {"model": "m"}, "generated_at": "t"})
    again = existing("synthetic-firm-one", "REQ-" + "a" * 24)
    return {"persist_draft_returns": got, "existing_draft_returns": again, "payload_ops": [x[2]["op"] for x in c.calls], "payload_keys": [sorted(x[2]) for x in c.calls]}


out = {"today_two_member_answer": run(A["first_persist_without_ticket_id"]), "built_three_member_answer": run(A["first_persist_with_ticket_id"]),
       "stored_fields": list(lh._STORED_FIELDS)}
out["same"] = out["today_two_member_answer"] == out["built_three_member_answer"]
out["persist_returns_exactly_the_stored_fields"] = sorted(out["built_three_member_answer"]["persist_draft_returns"]) == sorted(lh._STORED_FIELDS)
with open(out_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(json.dumps(out, indent=1, sort_keys=True) + "\n")
print("same=%s exact_fields=%s" % (out["same"], out["persist_returns_exactly_the_stored_fields"]))
