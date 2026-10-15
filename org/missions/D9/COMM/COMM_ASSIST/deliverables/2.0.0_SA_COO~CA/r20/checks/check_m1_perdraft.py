"""CA-l-1: the dell2 reader emits ONE drafts row per open mail draft (CA-k-1's reader half), checked on the checkout that dell2 actually runs.

Prints:  M1-PERDRAFT ok=<True|False> arms=<k> of 6 failed=<names|none> reason=<text>
Run from the ROOT of the checkout under test (on dell2: the repository root of the box's checkout), by relative path:
    python "org/missions/D9/COMM/COMM_ASSIST/deliverables/2.0.0_SA_COO~CA/r20/checks/check_m1_perdraft.py"
It loads data/transcripts/scripts/muse_reader/refresh.py of the CURRENT WORKING DIRECTORY (env M1_REFRESH may point at another copy of that file:
the test seam the issuer used to prove the base). Reads no AWS: aws_json is replaced by a fake that returns scan pages; nothing is written.

Contract (CA-k-1, merged 2d0a8f5027): read_drafts walks every state row (sk "state", "#index#" rows skipped); a mail object's state["pending_list"]
gives one row per entry (each with its own seq and tag), an object with only a legacy state["pending"] gives one row, a chat object's pending gives one.
Row keys: object_id, tag, kind, version, seq, status, texted_at, send_at, draft, chat_title, age_minutes, age_from.
Arms: two-rows-one-object, distinct-seq-and-tag, newest-and-oldest-both-present, legacy-single-row, chat-single-row, row-keys.
"""
import datetime
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path.cwd()
REFRESH = Path(os.environ.get("M1_REFRESH") or ROOT / "data" / "transcripts" / "scripts" / "muse_reader" / "refresh.py")
NOW = datetime.datetime(2026, 10, 15, 7, 0, 0, tzinfo=datetime.timezone.utc)
ROW_KEYS = {"object_id", "tag", "kind", "version", "seq", "status", "texted_at", "send_at", "draft", "chat_title", "age_minutes", "age_from"}
ARMS = ("two-rows-one-object", "distinct-seq-and-tag", "newest-and-oldest-both-present", "legacy-single-row", "chat-single-row", "row-keys")


def row(pk, state):
    return {"pk": {"S": pk}, "sk": {"S": "state"}, "data": {"S": json.dumps(state)}}


def mail_pending(seq, tag, texted_at, version=1):
    return {"tag": tag, "kind": "mail", "draft": "stand-in draft %d" % seq, "version": version, "texted_at": texted_at, "status": "texted",
            "seq": seq, "chat_title": "Pat Invented, invented-firm"}


def main():
    failed, why = [], ""
    try:
        spec = importlib.util.spec_from_file_location("refresh_under_check", REFRESH)
        R = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(R)

        older = mail_pending(5, "M105", "2026-10-15T06:10:00Z")
        newer = mail_pending(6, "M106", "2026-10-15T06:11:00Z")
        rows = [
            row("mail:owner", {"kind": "mail", "pending": newer, "pending_list": [older, newer], "draft_seq": 6}),
            row("mail:legacy", {"kind": "mail", "pending": mail_pending(2, "M102", "2026-10-15T05:00:00Z")}),
            row("19:chat@unq.gbl.spaces", {"title": "Chat One", "pending": {"tag": "C201", "kind": "chat", "version": 1, "seq": 9,
                                                                            "texted_at": "2026-10-15T06:30:00Z", "status": "texted", "draft": "d"}}),
            row("#index#sms-tag", {"x": 1}),
            row("mail:none", {"kind": "mail", "pending": None, "pending_list": []}),
        ]

        def fake_aws(args):
            if args[:2] == ["dynamodb", "scan"]:
                return json.dumps({"Items": rows, "ScannedCount": len(rows)})
            raise R.AwsError("unexpected call %s" % args[:2])

        R.aws_json = fake_aws
        items = R.make_readers(NOW)["drafts"]()
        by_obj = {}
        for i in items:
            by_obj.setdefault(i.get("object_id"), []).append(i)
        mail = by_obj.get("mail:owner", [])

        def arm(name, ok):
            if not ok:
                failed.append(name)

        arm("two-rows-one-object", len(mail) == 2)
        arm("distinct-seq-and-tag", len({i.get("seq") for i in mail}) == 2 and {i.get("tag") for i in mail} == {"M105", "M106"})
        arm("newest-and-oldest-both-present", {i.get("seq") for i in mail} == {5, 6})
        arm("legacy-single-row", [i.get("seq") for i in by_obj.get("mail:legacy", [])] == [2])
        arm("chat-single-row", len(by_obj.get("19:chat@unq.gbl.spaces", [])) == 1 and "mail:none" not in by_obj)
        arm("row-keys", bool(items) and all(set(i) == ROW_KEYS for i in items))
    except Exception as exc:  # noqa: BLE001 -- a crash is a failed check with its reason, never a pass
        why = "%s: %s" % (type(exc).__name__, str(exc)[:160])
        failed = list(ARMS)
    ok = not failed and not why
    print("M1-PERDRAFT ok=%s arms=%d of %d failed=%s reason=%s" % (ok, len(ARMS) - len(failed), len(ARMS), ",".join(failed) or "none", why or "none"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
