"""CA-i-11: the muse reader's draft rows carry the draft's seq, so a muse answer can be bound to the one draft it was shown.

Prints:  I11-SEQ ok=<True|False> with_seq=<value|none> without_seq=<value|absent> reason=<text>
Calls refresh._draft_row on a pending that carries seq and on one that does not. The row must carry `seq` (the number) for the first and `seq` = null (the key present)
for the second: absent is never shown as zero. No AWS.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))


def main():
    with_seq, without, why = "none", "absent", ""
    try:
        from data.transcripts.scripts.muse_reader import refresh
        base = {"tag": "C123", "kind": "chat", "version": 2, "status": "texted", "texted_at": "2026-10-13T20:00:00Z", "draft": "x"}
        a = refresh._draft_row({"title": "t"}, dict(base, seq=7), "19:abc")
        b = refresh._draft_row({"title": "t"}, dict(base), "19:abc")
        with_seq = a.get("seq", "absent")
        without = b.get("seq", "absent") if "seq" in b else "absent"
        if with_seq != 7:
            why = "the row for a draft with seq 7 carries seq=%r" % (with_seq,)
        elif "seq" not in b or b["seq"] is not None:
            why = "the row for a draft with no seq must carry the key with null, not %r" % (without,)
        elif a.get("object_id") != "19:abc" or a.get("tag") != "C123":
            why = "an existing field of the row changed"
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
    print("I11-SEQ ok=%s with_seq=%s without_seq=%s reason=%s" % (not why, with_seq, without, why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
