"""CA-i-7: Andrew can work a received-mail draft to the end by text -- notes redraft it, his 1 approves it and hands back the final draft to paste --
and NOTHING is ever sent to anyone in his name.

Prints:  I7-MAIL ok=<True|False> arms=<n> of 6 failed=<names|none> reason=<text>
Uses the mail-reply test harness (tests/test_inbound_mail_reply.py: Ctx, World, mail_item, reply) with a stand-in for the drafting model that
returns "FIRSTDRAFT" for a first draft and "REDRAFT <notes>" when the prompt carries Andrew's notes. No AWS, no network, no gateway.
Result words the build must return from tenant.on_sms_reply for a mail item: redraft -> "redrafted"; his 1 -> "mail-approved";
a 1 or notes aimed at a draft that moved on -> "unseen"; 0 -> "dropped"; #dev -> "job-opened" (these two are unchanged).
"""
import contextlib
import importlib.util
import io
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "infra" / "aws" / "terraform" / "modules" / "ldo" / "runtime"))


def main():
    failed, why = [], ""
    try:
        spec = importlib.util.spec_from_file_location("mail_harness", ROOT / "data/transcripts/scripts/tests/test_inbound_mail_reply.py")
        H = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(H)
        a, t = H.a, H.t

        def drafting_model(system, user, send=None):
            if "NOTESMARK" in user:
                return "REDRAFT " + user.split("NOTESMARK", 1)[1].split()[0]
            return "FIRSTDRAFT"

        def fresh():
            w = H.World()
            a.kimi = drafting_model
            with contextlib.redirect_stdout(io.StringIO()):
                state, tag = H.mail_item(w)
            return w, state, tag

        def say(state, tag, action, notes="", version=None):
            payload = {"tag": tag, "action": action, "notes": notes}
            if version is not None:
                payload["version"] = version
            ctx = H.Ctx("mail:owner", "sms.reply", payload, state=state, sent_at=a.iso(H.LATER))
            with contextlib.redirect_stdout(io.StringIO()):
                return t.on_sms_reply(ctx)

        def arm(name, fn):
            try:
                if not fn():
                    failed.append(name)
            except Exception as exc:
                failed.append("%s(%s: %s)" % (name, type(exc).__name__, str(exc)[:50]))

        def notes_redraft():
            w, st, tag = fresh()
            before = st["pending"]["version"]
            res = say(st, tag, "edit", "NOTESMARK shorter")
            p = st["pending"]
            return res == "redrafted" and p["version"] == before + 1 and "REDRAFT" in p["draft"] and "shorter" in p["draft"] \
                and any("REDRAFT" in body for _, body in w.texts)

        def one_approves_and_hands_back():
            w, st, tag = fresh()
            say(st, tag, "edit", "NOTESMARK shorter")
            res = say(st, tag, "send")
            last = w.texts[-1][1]
            return res == "mail-approved" and st.get("pending") is None and "REDRAFT" in last and "paste" in last.lower()

        def stale_one_is_refused():
            w, st, tag = fresh()
            say(st, tag, "edit", "NOTESMARK shorter")           # now version 2
            before = dict(st["pending"])
            res = say(st, tag, "send", version=1)
            return res == "unseen" and st["pending"] == before

        def stale_notes_are_refused():
            w, st, tag = fresh()
            say(st, tag, "edit", "NOTESMARK shorter")
            before = dict(st["pending"])
            res = say(st, tag, "edit", "NOTESMARK longer", version=1)
            return res == "unseen" and st["pending"] == before

        def zero_and_dev_unchanged():
            w, st, tag = fresh()
            r0 = say(st, tag, "drop")
            w2, st2, tag2 = fresh()
            rd = say(st2, tag2, "dev", "fix the export")
            return r0 == "dropped" and st["pending"] is None and rd == "job-opened"

        def never_sends_anything():
            w, st, tag = fresh()
            say(st, tag, "edit", "NOTESMARK shorter")
            say(st, tag, "send")
            return w.chat_sends == [] and w.posted == []

        for name, fn in (("notes-redraft", notes_redraft), ("one-approves-and-hands-back", one_approves_and_hands_back),
                         ("stale-one-refused", stale_one_is_refused), ("stale-notes-refused", stale_notes_are_refused),
                         ("zero-and-dev-unchanged", zero_and_dev_unchanged), ("nothing-sent", never_sends_anything)):
            arm(name, fn)
    except Exception as exc:
        why = "%s: %s" % (type(exc).__name__, str(exc)[:200])
        failed.append("harness")
    print("I7-MAIL ok=%s arms=%d of 6 failed=%s reason=%s" % (not failed, 0 if "harness" in failed else 6 - len(failed),
                                                              ";".join(failed) or "none", why or "none"))


if __name__ == "__main__":
    sys.exit(main() or 0)
