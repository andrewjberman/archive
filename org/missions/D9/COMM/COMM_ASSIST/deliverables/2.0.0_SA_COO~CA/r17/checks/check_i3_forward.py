"""CA-i-3: the dell2 forwarder moves a muse answer file onto the mailbox once, and refuses a malformed or unknown-tag file locally.

Prints:  I3-FORWARD ok=<True|False> arms=<n> of 6 failed=<names|none> reason=<text>
Imports data.transcripts.scripts.muse_reader.forwarder from the current directory; forward(root, send, now) is the interface:
send(object_id, kind, payload, event_id) is a callable; nothing here touches AWS. The forwarder does NOT verify signatures (the receiver does).
"""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
NOW = "2026-10-13T22:30:00Z"
TAG = "C123"
OBJ = "19:jane@unq.gbl.spaces"


def answer_file(root, name, tag=TAG, signature="-----BEGIN SSH SIGNATURE-----\nAAAA\n-----END SSH SIGNATURE-----\n"):
    payload = json.dumps({"tag": tag, "action": "send", "notes": "", "version": 1, "signed_at": "2026-10-13T22:29:00Z"}, sort_keys=True)
    body = json.dumps({"payload": payload, "signature": signature}, sort_keys=True)
    p = Path(root) / "answers" / name
    p.write_bytes(body.encode("utf-8"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def fresh_root(drafts=True):
    d = Path(tempfile.mkdtemp())
    (d / "answers").mkdir()
    rows = [{"tag": TAG, "object_id": OBJ, "version": 1}] if drafts else []
    (d / "drafts.json").write_text(json.dumps({"source": "drafts", "read_at": NOW, "status": "ok", "last_good_at": NOW,
                                               "error": None, "items": rows}), encoding="utf-8")
    return d


def main():
    failed, why = [], ""
    try:
        from data.transcripts.scripts.muse_reader import forwarder as fw

        def arm(name, fn):
            try:
                if not fn():
                    failed.append(name)
            except Exception as exc:
                failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:50]))

        def once():
            d, sent = fresh_root(), []
            sha = answer_file(d, "a.json")
            fw.forward(d, lambda *args: sent.append(args) or args[3], NOW)
            ok = len(sent) == 1 and sent[0][0] == OBJ and sent[0][1] == "muse.reply" and str(sent[0][3]).startswith("muse-")
            ok = ok and set(sent[0][2].keys()) == {"answer"} and set(sent[0][2]["answer"].keys()) == {"payload", "signature"}
            marker = list((d / "answers" / "done").glob("*.json"))
            return ok and len(marker) == 1 and json.loads(marker[0].read_text(encoding="utf-8")).get("tag") == TAG and sha in str(sent[0][3])

        def twice():
            d, sent = fresh_root(), []
            answer_file(d, "a.json")
            def send(*args):
                sent.append(args)
                return args[3]
            fw.forward(d, send, NOW)
            fw.forward(d, send, NOW)
            return len(sent) == 1

        def same_bytes_new_name():
            d, sent = fresh_root(), []
            answer_file(d, "a.json")
            def send(*args):
                sent.append(args)
                return args[3]
            fw.forward(d, send, NOW)
            answer_file(d, "b-copy.json")
            fw.forward(d, send, NOW)
            return len(sent) == 1

        def malformed():
            d, sent = fresh_root(), []
            (d / "answers" / "bad.json").write_text("{not json", encoding="utf-8")
            (d / "answers" / "nosig.json").write_text(json.dumps({"payload": "{}"}), encoding="utf-8")
            fw.forward(d, lambda *args: sent.append(args) or args[3], NOW)
            return sent == [] and len(list((d / "answers" / "rejected").glob("*.json"))) == 2

        def unknown_tag():
            d, sent = fresh_root(), []
            answer_file(d, "a.json", tag="C999")
            fw.forward(d, lambda *args: sent.append(args) or args[3], NOW)
            rej = list((d / "answers" / "rejected").glob("*.json"))
            return sent == [] and len(rej) == 1 and "tag" in rej[0].read_text(encoding="utf-8").lower()

        def failing_send():
            d, sent = fresh_root(), []
            answer_file(d, "a.json")
            (d / "answers" / "z.json").write_bytes(
                (d / "answers" / "a.json").read_bytes().replace(b"AAAA", b"BBBB"))   # a second, different file
            calls = {"n": 0}

            def flaky(*args):
                calls["n"] += 1
                if calls["n"] == 1:
                    raise RuntimeError("queue unavailable")
                sent.append(args)
                return args[3]
            fw.forward(d, flaky, NOW)                      # one fails, the other still goes
            first_done = len(list((d / "answers" / "done").glob("*.json")))
            fw.forward(d, flaky, NOW)                      # the failed one retries
            return len(sent) == 2 and first_done == 1 and len(list((d / "answers" / "done").glob("*.json"))) == 2

        for name, fn in (("valid-once", once), ("same-file-twice", twice), ("same-bytes-new-name", same_bytes_new_name),
                         ("malformed-rejected", malformed), ("unknown-tag-rejected", unknown_tag), ("failed-send-retries", failing_send)):
            arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("import")
    print("I3-FORWARD ok=%s arms=%d of 6 failed=%s reason=%s" % (not failed, 6 - len(failed) if "import" not in failed else 0,
                                                                  ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
